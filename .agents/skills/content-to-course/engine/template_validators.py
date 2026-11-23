"""Extracted static/refutation/D3/circuit-breaker validators for check_templates."""

import copy
import hashlib
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from engine.invariants import validate_katex_syntax
from engine.sandbox import (
    check_latex_escape_corruption_structured,
    execute_verifier_code,
    validate_code_ast,
)
from engine.stage_contract import is_skill_type
from engine.template_diagnostics import (
    format_diagnostic_error,
    format_invariant_error_diagnostic,
    get_canonical_invariant_key,
    normalize_error_string_for_hash,
)

_M20_STRUCTURED_TYPES: Set[str] = {
    "proof_dag",
    "adversarial_break",
    "unstructured_model",
    "invariant_canvas",
    "concept_matching",
}




def check_distractor_refutation(
    cross_check_py: str,
    gen_result: Dict[str, Any],
    seed: int = 100,
) -> List[Tuple[str, Any]]:
    """Verify that replacing 'correct' with each distractor fails the verifier."""
    if not cross_check_py or not gen_result:
        return []
    distractors = gen_result.get("distractors", {})
    dist_items: List[Tuple[str, Any]] = []
    if isinstance(distractors, dict):
        dist_items = list(distractors.items())
    elif isinstance(distractors, list):
        for i, d in enumerate(distractors):
            if isinstance(d, dict):
                is_regex_trap = (
                    str(d.get("match_type") or d.get("kind") or "").lower() == "regex"
                    or ("pattern" in d and "value" not in d and "expression" not in d)
                )
                if is_regex_trap:
                    continue
                did = d.get("distractor_id") or f"d{i+1}"
                val = d.get("value")
                if val is None:
                    val = d.get("expression")
                if val is None:
                    val = d.get("content")
                if val is None:
                    val = d
                dist_items.append((did, val))
            else:
                dist_items.append((f"d{i+1}", d))
    else:
        return []

    unrefuted = []
    for d_key, d_val in dist_items:
        cand_res = dict(gen_result)
        cand_res["correct"] = d_val
        try:
            passed = execute_verifier_code(cross_check_py, cand_res, seed=seed)
        except TypeError:
            passed = True
        except Exception:
            passed = False
        if passed:
            unrefuted.append((str(d_key), d_val))
    return unrefuted




def validate_template_static_rules(
    template: Dict[str, Any],
    competency_id: str,
    tpl_id: str,
    interaction_type: str,
    generate_py: str,
    cross_check_py: str,
    distractor_ids: List[Any],
    declared_distractor_ids: Set[str],
    errors: List[str],
) -> None:
    """Validate AST sandbox safety, LaTeX escape corruption, TPL-D1, TPL-D2, and stem_variants syntax."""
    # 1. AST Sandbox validation & LaTeX corruption check
    try:
        validate_code_ast(generate_py)
    except Exception as e:
        errors.append(format_diagnostic_error(
            "AST: SEGURIDAD DEL GENERADOR", competency_id, tpl_id, tpl_id, "generate_py",
            str(e), f"El código de generate_py violó las reglas de seguridad del AST: {e}",
            [
                "Eliminar llamadas a funciones prohibidas o imports inseguros en generate_py.",
                "Usar únicamente módulos permitidos (math, random, fractions, sympy, etc.).",
                "Revisar la sintaxis de Python en generate_py.",
            ]
        ))

    corrupt_items = check_latex_escape_corruption_structured(generate_py)
    if corrupt_items:
        by_cmd: Dict[str, List[Dict[str, Any]]] = {}
        for ci in corrupt_items:
            by_cmd.setdefault(ci["cmd"], []).append(ci)
        for cmd, occurrences in by_cmd.items():
            lines_list = [o["line"] for o in occurrences if o.get("line") is not None]
            errors.append(format_diagnostic_error(
                "AST: CORRUPCIÓN DE ESCAPE LATEX", competency_id, tpl_id, tpl_id, "generate_py",
                f"'{cmd}'",
                f"Posible corrupción de escape de LaTeX en generate_py: comando '{cmd}' interpretado como carácter de control ({len(occurrences)} ocurrencias).",
                [
                    "Usar raw strings r'...' para literales que contengan barras invertidas '\\'.",
                    f"Evitar cadenas con escapes inválidos; escapar como '\\\\{cmd[1:]}'.",
                    "Verificar la generación de fórmulas KaTeX.",
                ],
                lines=lines_list,
            ))

    if cross_check_py:
        try:
            validate_code_ast(cross_check_py)
        except Exception as e:
            errors.append(format_diagnostic_error(
                "AST: SEGURIDAD DEL CROSS-CHECK", competency_id, tpl_id, tpl_id, "cross_check_py",
                str(e), f"El código de cross_check_py violó las reglas de seguridad del AST: {e}",
                [
                    "Eliminar llamadas a funciones prohibidas o imports inseguros en cross_check_py.",
                    "Usar únicamente módulos permitidos del sandbox.",
                    "Revisar la sintaxis de Python en cross_check_py.",
                ]
            ))
        cc_corrupt_items = check_latex_escape_corruption_structured(cross_check_py)
        if cc_corrupt_items:
            by_cmd_cc: Dict[str, List[Dict[str, Any]]] = {}
            for ci in cc_corrupt_items:
                by_cmd_cc.setdefault(ci["cmd"], []).append(ci)
            for cmd, occurrences in by_cmd_cc.items():
                lines_list = [o["line"] for o in occurrences if o.get("line") is not None]
                errors.append(format_diagnostic_error(
                    "AST: CORRUPCIÓN DE ESCAPE LATEX", competency_id, tpl_id, tpl_id, "cross_check_py",
                    f"'{cmd}'",
                    f"Posible corrupción de escape de LaTeX en cross_check_py: comando '{cmd}' interpretado como carácter de control ({len(occurrences)} ocurrencias).",
                    [
                        "Usar raw strings r'...' para literales que contengan barras invertidas '\\'.",
                        "Evitar cadenas con escapes inválidos.",
                        "Verificar la generación de fórmulas KaTeX.",
                    ],
                    lines=lines_list,
                ))

    # 2. Rule TPL-D1: All referenced distractor_ids exist in competency CTA
    missing_dids = [did for did in distractor_ids if did not in declared_distractor_ids]
    if len(missing_dids) > 1:
        errors.append(format_diagnostic_error(
            "TPL-D1: DISTRACTOR NO DECLARADO EN CTA", competency_id, tpl_id, tpl_id, "distractor_ids",
            f"{', '.join(missing_dids)} ({len(missing_dids)} distractores)",
            f"Los distractor_ids '{', '.join(missing_dids)}' referenciados en la plantilla no existen en la lista de distractores de '{competency_id}' en cta.json.",
            [
                f"Verificar los distractores declarados para '{competency_id}' en cta.json y usar los IDs exactos.",
                f"O declarar los distractores en la competencia '{competency_id}' dentro de cta.json.",
                "Corregir cualquier error tipográfico en el ID del distractor dentro del JSON de la plantilla.",
            ]
        ))
    elif len(missing_dids) == 1:
        did = missing_dids[0]
        errors.append(format_diagnostic_error(
            "TPL-D1: DISTRACTOR NO DECLARADO EN CTA", competency_id, tpl_id, tpl_id, "distractor_ids",
            f"'{did}'",
            f"El distractor_id '{did}' referenciado en la plantilla no existe en la lista de distractores de '{competency_id}' en cta.json.",
            [
                f"Verificar los distractores declarados para '{competency_id}' en cta.json y usar los IDs exactos.",
                f"O declarar el distractor '{did}' en la competencia '{competency_id}' dentro de cta.json.",
                "Corregir cualquier error tipográfico en el ID del distractor dentro del JSON de la plantilla.",
            ]
        ))

    # 3. Rule TPL-D2: MC7 must reference/use at least 6 distinct distractor_ids
    if interaction_type == "multiple_choice_7_options":
        if len(set(distractor_ids)) < 6:
            errors.append(format_diagnostic_error(
                "TPL-D2: REQUISITO DE 6 DISTRACTORES EN MC7", competency_id, tpl_id, tpl_id, "distractor_ids",
                f"{len(set(distractor_ids))} distractor_ids declarados: {distractor_ids}",
                "Las plantillas MC7 requieren exactamente 6 distractor_ids distintos para cubrir los 6 distractores psicométricos.",
                [
                    "Declarar al menos 6 distractor_ids únicos en el arreglo 'distractor_ids' de la plantilla.",
                    "Vincular cada uno de los 6 distractores generados en generate_py a un distractor_id declarado.",
                    "Revisar cta.json para seleccionar 6 distractores relevantes de la competencia.",
                ]
            ))

    # 4. Static validation of ALL stem_variants syntax with validate_katex_syntax
    stem_variants_list = template.get("stem_variants", [])
    if isinstance(stem_variants_list, list):
        variant_katex_errs: Dict[str, Tuple[str, List[str]]] = {}
        for idx, variant in enumerate(stem_variants_list):
            if isinstance(variant, str):
                for kv_err in validate_katex_syntax(variant, f"stem_variants[{idx}]"):
                    sig = get_canonical_invariant_key(kv_err)
                    if sig not in variant_katex_errs:
                        variant_katex_errs[sig] = (kv_err, [f"stem_variants[{idx}]"])
                    else:
                        variant_katex_errs[sig][1].append(f"stem_variants[{idx}]")

        for sig, (rep_err, var_items) in variant_katex_errs.items():
            errors.append(format_invariant_error_diagnostic(
                cid=competency_id,
                tpl_id=tpl_id,
                q_id=var_items,
                inv_err=rep_err,
            ))



def check_mc7_and_ms_verifier_refutation(
    interaction_type: str,
    strict: bool,
    cross_check_py: str,
    batch_results: List[Dict[str, Any]],
    competency_id: str,
    tpl_id: str,
    errors: List[str],
    warnings_out: Optional[List[str]] = None,
) -> None:
    """Verify MC7 distractor refutation and multiple_select verifier non-tautology."""
    # Strict Distractor Refutation check for MC7 templates with verifier
    if strict and cross_check_py and interaction_type == "multiple_choice_7_options":
        first_succ = next((r for r in batch_results if r.get("success")), None)
        if first_succ:
            unrefuted = check_distractor_refutation(
                cross_check_py=cross_check_py,
                gen_result=first_succ.get("result", {}),
                seed=first_succ.get("seed", 100),
            )
            if unrefuted:
                unrefuted_ids = [k for k, _ in unrefuted]
                errors.append(format_diagnostic_error(
                    "TPL-CROSS: DISTRACTOR NO REFUTADO",
                    competency_id,
                    tpl_id,
                    tpl_id,
                    "cross_check_py / distractors",
                    f"{len(unrefuted)} distractores aceptados como correctos por el verificador: {unrefuted_ids}",
                    f"[-] [TPL-CROSS] violation in '{tpl_id}': cross_check_py / verifier did not refute distractor(s) {unrefuted_ids}. Distractors must fail verification when substituted into correct.",
                    [
                        "Asegurar que verify(result) verifique rigurosamente las propiedades de la solución correcta.",
                        "Comprobar que los distractores violen la condición matemática evaluada en verify().",
                        "Refinar los distractores para que no satisfagan accidentalmente el invariante de la respuesta correcta.",
                    ]
                ))

    # Strict Verifier Tautology Check for MS templates with verifier
    if strict and cross_check_py and interaction_type == "multiple_select":
        first_succ = next((r for r in batch_results if r.get("success")), None)
        if first_succ:
            gen_res = first_succ.get("result", {})
            seed_val = first_succ.get("seed", 100)
            opts = gen_res.get("options")
            if isinstance(opts, list) and len(opts) >= 2:
                t_idxs = [i for i, o in enumerate(opts) if isinstance(o, dict) and o.get("is_correct")]
                f_idxs = [i for i, o in enumerate(opts) if isinstance(o, dict) and not o.get("is_correct")]
                if t_idxs and f_idxs:
                    # Mutation (a): invert is_correct
                    cand_a = copy.deepcopy(gen_res)
                    cand_a["options"][t_idxs[0]]["is_correct"] = False
                    cand_a["options"][f_idxs[0]]["is_correct"] = True
                    try:
                        passed_a = execute_verifier_code(cross_check_py, cand_a, seed=seed_val)
                    except Exception:
                        passed_a = False

                    # Mutation (b): invalidate distractor_id
                    passed_b = False
                    did_idx = next((i for i in f_idxs if opts[i].get("distractor_id")), None)
                    if did_idx is not None:
                        cand_b = copy.deepcopy(gen_res)
                        cand_b["options"][did_idx]["distractor_id"] = "__INVALID_DID__"
                        try:
                            passed_b = execute_verifier_code(cross_check_py, cand_b, seed=seed_val)
                        except Exception:
                            passed_b = False

                    # Mutation (c1): empty error_rationale in false option only
                    cand_c1 = copy.deepcopy(gen_res)
                    cand_c1["options"][f_idxs[0]]["error_rationale"] = ""
                    try:
                        passed_c1 = execute_verifier_code(cross_check_py, cand_c1, seed=seed_val)
                    except Exception:
                        passed_c1 = False

                    # Mutation (c2): mutate value/content to sentinel in true option only
                    cand_c2 = copy.deepcopy(gen_res)
                    cand_c2["options"][t_idxs[0]]["value"] = "__MUTATED__"
                    if "content" in cand_c2["options"][t_idxs[0]]:
                        cand_c2["options"][t_idxs[0]]["content"] = "__MUTATED__"
                    try:
                        passed_c2 = execute_verifier_code(cross_check_py, cand_c2, seed=seed_val)
                    except Exception:
                        passed_c2 = False

                    # Mutation (c3): mutate value/content to syntactically valid but false LaTeX assertion
                    false_latex = "$1 = 2$" if str(opts[t_idxs[0]].get("value", "")).strip() == "$0 = 1$" else "$0 = 1$"
                    cand_c3 = copy.deepcopy(gen_res)
                    cand_c3["options"][t_idxs[0]]["value"] = false_latex
                    if "content" in cand_c3["options"][t_idxs[0]]:
                        cand_c3["options"][t_idxs[0]]["content"] = false_latex
                    try:
                        passed_c3 = execute_verifier_code(cross_check_py, cand_c3, seed=seed_val)
                    except Exception:
                        passed_c3 = False

                    is_taut = (passed_a is True) or (passed_c2 is True) or (passed_c3 is True)
                    if is_taut:
                        errors.append(format_diagnostic_error(
                            "TPL-CROSS: VERIFICADOR MS TAUTOLOGICO",
                            competency_id,
                            tpl_id,
                            tpl_id,
                            "cross_check_py / options",
                            "El verificador multiple_select aceptó mutaciones inválidas (inversión de is_correct / opciones mutadas).",
                            f"[-] [TPL-CROSS] violation in '{tpl_id}': cross_check_py / verifier did not refute mutated options in multiple_select. The verifier is tautological and must reject incorrect option assignments.",
                            [
                                "Asegurar que verify(result) verifique rigurosamente cuáles opciones en 'options' son correctas e incorrectas.",
                                "Validar que las opciones correctas e incorrectas cumplan o violen las condiciones de la pregunta.",
                                "No limitarse a contar la cantidad de opciones (ej. len(options)==4 and sum(...)==2).",
                            ]
                        ))
                    else:
                        if passed_b is True:
                            warn_msg = f"WARNING: [TPL-CROSS-DID] En '{tpl_id}': El verificador multiple_select no validó 'distractor_id' en opciones incorrectas."
                            if warnings_out is not None:
                                warnings_out.append(warn_msg)
                            print(warn_msg, file=sys.stderr)
                        if passed_c1 is True:
                            warn_msg = f"WARNING: [TPL-CROSS-RATIONALE] En '{tpl_id}': El verificador multiple_select no validó 'error_rationale' en opciones incorrectas."
                            if warnings_out is not None:
                                warnings_out.append(warn_msg)
                            print(warn_msg, file=sys.stderr)



def evaluate_static_opt_and_dynamic_rationale(
    template: Dict[str, Any],
    competency_id: str,
    tpl_id: str,
    interaction_type: str,
    strict: bool,
    num_dry_run_seeds: int,
    batch_results: List[Dict[str, Any]],
    rendered_correct_answers: List[Any],
    distractor_contents_by_slot: Dict[Any, List[str]],
    distractor_rationales_by_slot: Dict[Any, List[str]],
    errors: List[str],
) -> None:
    """Evaluate [TPL-STATIC-OPT] key variability and [TPL-DYNAMIC-RATIONALE] rules."""
    # Evaluate [TPL-STATIC-OPT] under strict=True
    if strict and rendered_correct_answers:
        eval_answers = rendered_correct_answers
        N_eval = len(eval_answers)
        unique_correct = set(eval_answers)

        # Unconditional mono-key blocking: if N >= 2 and len(unique_correct) == 1, ALWAYS reject
        if N_eval >= 2 and len(unique_correct) == 1:
            first_ans = list(unique_correct)[0]
            first_str = str(first_ans)
            errors.append(format_diagnostic_error(
                "TPL-STATIC-OPT: MONO-CLAVE DETECTADA",
                competency_id,
                tpl_id,
                "dry-run",
                "correct / vars",
                f"Clave fija en {N_eval} semillas evaluadas: '{first_str}'",
                f"[-] [TPL-STATIC-OPT] violation in '{tpl_id}': Mono-clave detected across {N_eval} seeds ({len(unique_correct)} unique correct answers). Templates must generate dynamic correct answers.",
                [
                    "Parametrizar las variables en generate_py para que la respuesta correcta varíe dinámicamente entre semillas.",
                    "Evitar respuestas estáticas o dominios vacíos que produzcan siempre la misma clave.",
                    "Verificar que vars contenga parámetros que modifiquen el resultado numérico o simbólico.",
                ]
            ))
        elif num_dry_run_seeds >= 15:
            has_dynamic_vars = any(
                len(r.get("result", {}).get("vars", {})) > 0
                for r in batch_results if r.get("success")
            )
            if interaction_type == "multiple_select":
                min_req_ms = 5 if has_dynamic_vars else 2
                if len(unique_correct) < min_req_ms:
                    errors.append(format_diagnostic_error(
                        "TPL-STATIC-OPT: CONJUNTO DE OPCIONES ESTÁTICO",
                        competency_id,
                        tpl_id,
                        "dry-run",
                        "options",
                        f"Únicamente {len(unique_correct)}/{min_req_ms} conjuntos de opciones generados en {N_eval} semillas.",
                        f"[-] [TPL-STATIC-OPT] violation in '{tpl_id}': multiple_select template must generate at least {min_req_ms} distinct sets of correct options.",
                        [
                            "Parametrizar las opciones o su veracidad en generate_py.",
                            "Asegurar que la selección de afirmaciones correctas varíe según los parámetros.",
                        ]
                    ))
            elif interaction_type in _M20_STRUCTURED_TYPES:
                min_req_m20 = 4 if has_dynamic_vars else 2
                if len(unique_correct) < min_req_m20:
                    errors.append(format_diagnostic_error(
                        "TPL-STATIC-OPT: ESTRUCTURA ESTÁTICA",
                        competency_id,
                        tpl_id,
                        "dry-run",
                        interaction_type,
                        f"Únicamente {len(unique_correct)}/{min_req_m20} variantes generadas en {N_eval} semillas.",
                        f"[-] [TPL-STATIC-OPT] violation in '{tpl_id}': {interaction_type} template must generate at least {min_req_m20} distinct parametric instances.",
                        [
                            "Parametrizar los valores o restricciones del payload estructurado en generate_py.",
                        ]
                    ))
            else:
                cid_upper = str(competency_id or template.get("competency_id") or "").upper().strip()
                comp_type = str(template.get("competency_type") or "").strip()
                is_fact_concept_or_misc = (
                    cid_upper.startswith(("C-", "M-", "H-", "F-", "PRE-"))
                    or "CONCEPT" in cid_upper
                    or "MISCONCEPTION" in cid_upper
                    or "FACT" in cid_upper
                    or "HECHO" in cid_upper
                )
                if comp_type and is_skill_type(comp_type):
                    is_skill_or_hab = True
                elif comp_type and not is_skill_type(comp_type):
                    is_skill_or_hab = False
                elif is_fact_concept_or_misc:
                    is_skill_or_hab = False
                elif (
                    cid_upper.startswith("HAB-")
                    or is_skill_type(competency_id)
                    or any(s in cid_upper.lower() for s in ["skill", "hab"])
                ):
                    is_skill_or_hab = True
                else:
                    is_skill_or_hab = template.get("bloom", "") in ("Apply", "Analyze", "Evaluate", "Create")

                min_req = min(10, max(5, N_eval // 2)) if is_skill_or_hab else (min(5, N_eval) if has_dynamic_vars else min(4, N_eval))
                if len(unique_correct) < min_req:
                    errors.append(format_diagnostic_error(
                        "TPL-STATIC-OPT: BAJA VARIABILIDAD DE CLAVE",
                        competency_id,
                        tpl_id,
                        "dry-run",
                        "correct / vars",
                        f"Únicamente {len(unique_correct)}/{min_req} claves correctas únicas en {N_eval} semillas.",
                        f"[-] [TPL-STATIC-OPT] violation in '{tpl_id}': Only {len(unique_correct)}/{min_req} unique correct answers generated across {N_eval} seeds. Required threshold is >={min_req}.",
                        [
                            "Ampliar los rangos numéricos y combinaciones de parámetros en generate_py.",
                            "Asegurar que la clave correcta cambie frecuentemente entre semillas.",
                        ]
                    ))

    # Evaluate [TPL-DYNAMIC-RATIONALE]
    if strict and num_dry_run_seeds >= 15:
        for slot_key, contents_list in distractor_contents_by_slot.items():
            rats_list = distractor_rationales_by_slot.get(slot_key, [])
            u_contents = set(contents_list)
            u_rats = set(rats_list)
            if len(u_contents) > 1 and len(u_rats) == 1:
                rat_sample = list(u_rats)[0] if u_rats else "(vacío)"
                errors.append(format_diagnostic_error(
                    "TPL-DYNAMIC-RATIONALE: RATIONALE ESTÁTICO EN DISTRACTOR DINÁMICO",
                    competency_id,
                    tpl_id,
                    str(slot_key),
                    "error_rationale",
                    f"Distractor '{slot_key}' varía en contenido ({len(u_contents)} variantes) pero tiene error_rationale estático: '{rat_sample}'",
                    f"[-] [TPL-DYNAMIC-RATIONALE] violation in '{tpl_id}': Distractor '{slot_key}' varies across seeds ({len(u_contents)} unique contents) but its error_rationale remains static. Dynamic distractors must include dynamic rationale explaining the specific misconception with seed parameters.",
                    [
                        f"Incluir placeholders como @var@ o {{var}} en el error_rationale del distractor '{slot_key}'.",
                        "Explicar el error formativo contextualizado con los valores numéricos o simbólicos generados en la semilla.",
                        "Asegurar que error_rationale varíe dinámicamente cuando el distractor varía.",
                    ]
                ))



def check_multimodal_tpl_d3_coverage(
    cta_distractors_by_comp: Dict[str, Set[str]],
    cta_data: Optional[Dict[str, Any]],
    referenced_distractors_by_comp: Dict[str, Set[str]],
    templates_by_comp: Dict[str, List[Dict[str, Any]]],
    processed_comp_ids: Set[str],
    is_full_dir: bool,
    errors: List[str],
    errors_by_comp: Dict[str, List[str]],
) -> None:
    """Enforce Rule TPL-D3 multimodal distractor coverage across competencies."""
    # Rule TPL-D3: Multimodal distractor coverage across templates (M20 Anti-Descarte Decoupling)
    if cta_distractors_by_comp:
        comps_to_check = list(referenced_distractors_by_comp.keys()) if is_full_dir else list(processed_comp_ids)
        _bloom_sup_types = {
            "open_symbolic",
            "proof_dag",
            "adversarial_break",
            "unstructured_model",
            "invariant_canvas",
            "concept_matching",
        }
        comp_map_d3 = {c.get("id"): c for c in (cta_data or {}).get("competencies", []) if isinstance(c, dict)}
        for cid in comps_to_check:
            declared_set = {d.replace("_", "-") for d in (cta_distractors_by_comp.get(cid, set()) or set())}
            referenced_set = {d.replace("_", "-") for d in (referenced_distractors_by_comp.get(cid, set()) or set())}
            c_tpls = templates_by_comp.get(cid, [])
            has_mc7 = any(t.get("interaction_type") == "multiple_choice_7_options" for t in c_tpls)
            has_ms = any(t.get("interaction_type") == "multiple_select" for t in c_tpls)
            has_bloom_superior = any(t.get("interaction_type") in _bloom_sup_types for t in c_tpls)
            has_fib_ds = any(
                t.get("interaction_type") == "fill_in_the_blank" and bool(t.get("distractor_ids"))
                for t in c_tpls
            )
            _comp_meta = (comp_map_d3 or {}).get(cid) or {}
            _contract_v2 = (
                int((cta_data or {}).get("contract_version") or 1) >= 2
                or bool(_comp_meta.get("recommended_modalities"))
            )
            is_100_fib_legacy = (
                not _contract_v2
                and len(c_tpls) > 0
                and all(t.get("interaction_type") == "fill_in_the_blank" for t in c_tpls)
                and not referenced_set
            )
            is_legacy_pure_ms = (
                not _contract_v2
                and has_ms
                and not has_mc7
                and not has_bloom_superior
                and not has_fib_ds
                and not (declared_set and referenced_set and len(declared_set - referenced_set) == 0)
            )

            tpl_d3_failed = False
            snippet_msg = ""
            cause_msg = ""
            if is_100_fib_legacy:
                tpl_d3_failed = False
            elif is_legacy_pure_ms:
                valid_ref = referenced_set.intersection(declared_set)
                if len(valid_ref) < 2:
                    tpl_d3_failed = True
                    snippet_msg = f"Distractores cubiertos: {sorted(valid_ref)} ({len(valid_ref)}/2 requeridos para MS)"
                    cause_msg = "Las plantillas multiple_select requieren al menos 2 distractores declarados en cta.json."
            else:
                uncovered = declared_set - referenced_set
                if uncovered:
                    tpl_d3_failed = True
                    snippet_msg = f"Distractores sin cubrir: {sorted(uncovered)} ({len(uncovered)}/{len(declared_set)})"
                    cause_msg = (
                        "Existen distractores definidos en cta.json que ninguna plantilla de la competencia está cubriendo "
                        "en su semilla representativa a través de MC7 (si aplica en el plan), MS, FIB ('ds'), open_symbolic o modalidades Bloom Superior "
                        "(rotar distractores solo entre semillas sin incluirlos en la semilla representativa NO los cubre)."
                    )

            if tpl_d3_failed:
                err_diag = format_diagnostic_error(
                    rule_tag="TPL-D3: COBERTURA COMPLETA DE DISTRACTORES",
                    competency=cid,
                    template="[Todas las plantillas de la competencia]",
                    item_id="N/A",
                    field_name="distractor_ids",
                    snippet=snippet_msg,
                    cause=cause_msg,
                    actions=[
                        f"Cubrir los distractores faltantes de '{cid}' usando trampas diagnósticas ('ds') en FIB / open_symbolic, pasos falaces en proof_dag / adversarial_break, opciones de Phase 1-3 en unstructured_model o pares distractores en concept_matching / invariant_canvas.",
                        f"O declarar los distractor_ids faltantes en la semilla representativa de las plantillas de '{cid}' manteniendo fidelidad al plan de modalidades del CTA Architect.",
                        "Asegurar la cobertura diagnóstica completa de distractores requerida por el contrato psicométrico M20.",
                    ],
                )
                errors.append(err_diag)
                errors_by_comp.setdefault(cid, []).append(err_diag)



def update_circuit_breaker_state(
    effective_attempts_dir: Optional[Union[str, Path]],
    shard_id: Optional[str],
    processed_comp_ids: Set[str],
    raw_targets: List[Any],
    is_clean: bool,
    errors: List[str],
    errors_by_comp: Dict[str, List[str]],
    templates_by_comp: Dict[str, List[Dict[str, Any]]],
    template_files: List[Path],
    from_compile_shard: bool,
) -> None:
    """Update per-shard and per-competency SHA-256 circuit breakers and .check_attempts state."""
    # Circuit breaker and attempt tracking
    if effective_attempts_dir is not None:
        try:
            att_path = Path(effective_attempts_dir)
            att_path.mkdir(parents=True, exist_ok=True)

            def _safe_write_text(f_path: Path, text: str) -> None:
                tmp_p = f_path.with_name(f".{f_path.name}.tmp.{os.getpid()}_{uuid.uuid4().hex[:8]}")
                tmp_p.write_text(text, encoding="utf-8")
                try:
                    os.replace(tmp_p, f_path)
                except Exception:
                    try:
                        if f_path.is_file():
                            f_path.unlink()
                        os.replace(tmp_p, f_path)
                    except Exception:
                        f_path.write_text(text, encoding="utf-8")
                        if tmp_p.is_file():
                            try:
                                tmp_p.unlink()
                            except Exception:
                                pass

            # Derive deterministic scope key for circuit breaker isolation across concurrent shards
            shard_tag = f"{shard_id}_" if shard_id else ""
            if processed_comp_ids:
                scope_raw = f"{shard_tag}" + "_".join(sorted(processed_comp_ids))
            elif raw_targets:
                scope_raw = f"{shard_tag}" + "_".join(sorted(str(t) for t in raw_targets))
            else:
                scope_raw = f"{shard_tag}global"

            if len(scope_raw) > 32:
                scope_key = hashlib.sha256(scope_raw.encode("utf-8")).hexdigest()[:12]
            else:
                scope_key = re.sub(r"[^a-zA-Z0-9_-]", "_", scope_raw)

            cb_file = att_path / f"circuit_breaker_{scope_key}.json"
            legacy_cb_file = att_path / "circuit_breaker.json"
            err_hash = None

            if not is_clean:
                # Compute deterministic error fingerprint
                normalized_errs = sorted([normalize_error_string_for_hash(e) for e in errors])
                err_hash = hashlib.sha256("\n".join(normalized_errs).encode("utf-8")).hexdigest()

                cb_data = {"consecutive_count": 1, "last_hash": err_hash, "history": []}
                target_file = cb_file if cb_file.is_file() else (legacy_cb_file if legacy_cb_file.is_file() else None)
                if target_file and target_file.is_file():
                    try:
                        loaded = json.loads(target_file.read_text(encoding="utf-8"))
                        if loaded.get("last_hash") == err_hash:
                            cb_data["consecutive_count"] = loaded.get("consecutive_count", 1) + 1
                        else:
                            cb_data["consecutive_count"] = 1
                        cb_data["history"] = loaded.get("history", [])
                    except Exception:
                        pass

                cb_data["history"].append({
                    "hash": err_hash,
                    "error_count": len(errors),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
                cb_data["history"] = cb_data["history"][-10:]
                _safe_write_text(cb_file, json.dumps(cb_data, indent=2, ensure_ascii=False))

                if cb_data["consecutive_count"] >= 3:
                    cb_msg = (
                        f"[-] [CIRCUIT BREAKER: FALLOS CONSECUTIVOS IDÉNTICOS]\n"
                        f"    UBICACIÓN: Subagente de autoría de plantillas\n"
                        f"    CAUSA: Se han detectado 3 ejecuciones consecutivas de check_templates.py con exactamente el mismo número ({len(errors)}) y tipo de errores sin ningún progreso.\n"
                        f"    ACTION REQUIRED: Detener de inmediato las llamadas a herramientas y responder:\n"
                        f"    BLOCKED: CONTRACT_ERROR - Circuit breaker activado tras 3 fallos consecutivos idénticos.\n"
                        f"    STOP, send_message the Director."
                    )
                    errors.append(cb_msg)
            else:
                # Clear circuit breaker on clean pass
                if cb_file.is_file():
                    try:
                        cb_file.unlink()
                    except Exception:
                        pass
                if legacy_cb_file.is_file():
                    try:
                        legacy_cb_file.unlink()
                    except Exception:
                        pass

            # Per-competency budget halt tracking with shard isolation and stateful SHA-256 circuit breaker
            for cid in processed_comp_ids:
                cid_errs = errors_by_comp.get(cid, [])
                cid_is_clean = (len(cid_errs) == 0)

                if len(processed_comp_ids) == 1 and err_hash:
                    cid_err_hash = err_hash
                elif cid_errs:
                    cid_norm = sorted([normalize_error_string_for_hash(e) for e in cid_errs])
                    cid_err_hash = hashlib.sha256("\n".join(cid_norm).encode("utf-8")).hexdigest()
                else:
                    cid_err_hash = None

                att_fname = f"{shard_id}_{cid}.json" if shard_id else f"{cid}.json"
                f_att = att_path / att_fname
                att_data = {"attempts": 0, "last_hash": None, "last_err_hash": None, "halted": False}
                if f_att.is_file():
                    try:
                        loaded = json.loads(f_att.read_text(encoding="utf-8"))
                        if isinstance(loaded, dict):
                            att_data["attempts"] = loaded.get("attempts", 0)
                            att_data["last_hash"] = loaded.get("last_hash")
                            att_data["last_err_hash"] = loaded.get("last_err_hash")
                            att_data["halted"] = bool(loaded.get("halted", False))
                    except Exception:
                        pass

                # Compute SHA-256 of competency source
                comp_tpls = templates_by_comp.get(cid, [])
                comp_source_text = ""
                if comp_tpls:
                    comp_source_text = json.dumps(comp_tpls, sort_keys=True, ensure_ascii=False)
                else:
                    for tf in template_files:
                        if tf.stem == cid or f"{cid}.json" in tf.name:
                            if tf.is_file():
                                comp_source_text = tf.read_text(encoding="utf-8")
                            break
                if not comp_source_text:
                    comp_source_text = cid

                comp_hash = hashlib.sha256(comp_source_text.encode("utf-8")).hexdigest()
                last_hash = att_data.get("last_hash")
                last_err_hash = att_data.get("last_err_hash")
                was_halted = att_data.get("halted", False)
                hash_changed = (last_hash is not None and last_hash != comp_hash)
                err_changed = (cid_err_hash is not None and last_err_hash is not None and last_err_hash != cid_err_hash)

                if hash_changed or (from_compile_shard and err_changed):
                    # Changed hash is re-evaluated; clear previous halt and reset attempts
                    att_data["attempts"] = 0
                    att_data["halted"] = False
                    was_halted = False

                if cid_is_clean:
                    # Pass clears the halt and deletes any attempt files for this competency
                    targets_to_unlink = [f_att, att_path / f"{cid}.json"]
                    if shard_id:
                        targets_to_unlink.append(att_path / f"{shard_id}_{cid}.json")
                    for target_file in targets_to_unlink:
                        if target_file.is_file():
                            try:
                                target_file.unlink()
                            except Exception:
                                pass
                else:
                    if was_halted and not hash_changed and not (from_compile_shard and err_changed):
                        terminal_msg = (
                            f"[!] BUDGET HALT on competency '{cid}': Repeat failure with unchanged SHA-256 source hash ({comp_hash[:10]}). "
                            f"STOP, send_message the Director."
                        )
                        errors.append(terminal_msg)
                    else:
                        att_data["attempts"] = att_data.get("attempts", 0) + 1
                        att_data["last_hash"] = comp_hash
                        att_data["last_err_hash"] = cid_err_hash
                        if att_data["attempts"] >= 3:
                            if not (from_compile_shard and err_changed):
                                att_data["halted"] = True
                                terminal_msg = (
                                    f"[!] BUDGET HALT on competency '{cid}': Exceeded {att_data['attempts']} validation cycles with identical source hash ({comp_hash[:10]}). "
                                    f"STOP, send_message the Director."
                                )
                                errors.append(terminal_msg)
                        _safe_write_text(f_att, json.dumps(att_data, indent=2, ensure_ascii=False))
        except Exception:
            pass

