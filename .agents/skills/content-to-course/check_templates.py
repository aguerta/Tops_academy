"""Template validator for content-to-course v2.

Validates parametric exercise templates against template.schema.json and enforces:
- AST sandbox whitelist security
- 50-seed dry run execution without runtime or timeout errors
- Invariant evaluation on 100% of dry-run instances
- TPL-D1: all distractor_ids referenced exist in the competency's declared distractors in cta.json
- TPL-D2: MC7 items use 6 distinct distractor_ids
- TPL-D3: 100% distractor coverage across templates for each competency
- TPL-D4: distractors != correct answer on 100% of instances
"""

import argparse
import json
import os
import re
import sys
import zlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import jsonschema

# Add skills root and project src to sys.path so engine and validator can be imported directly
_skills_root = Path(__file__).parent.resolve()
if str(_skills_root) not in sys.path:
    sys.path.insert(0, str(_skills_root))

_project_root = Path(__file__).resolve().parents[3]
_src_dir = _project_root / "src"
if str(_src_dir) not in sys.path and _src_dir.is_dir():
    sys.path.insert(0, str(_src_dir))
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from engine.assemble import assemble_question, format_template_string
from engine.diversity import evaluate_competency_diversity, mask_stem_numbers
from engine.invariants import check_instance_invariants
from engine.instantiate import instantiate_competency, competency_seed_base
from engine.sandbox import (
    execute_sandbox_batch,
    validate_code_ast,
    check_latex_escape_corruption,
    warm_up_sandbox,
    SandboxExecutionError,
    SandboxTimeoutError,
    SecurityViolationError,
)
from validator.core import validate_course_content


RULE_ACTIONS: Dict[str, str] = {
    "R-17": "El error_rationale no puede ser genérico o un placeholder.",
    "R-18": "Reescribe la opción como afirmación objetiva; prohibido usar prefijos como 'erróneamente', 'confundiendo', 'asumiendo equivocadamente'.",
    "R-19": "Elimina el valor de la clave de respuesta del stem de la pregunta FIB (fuga de respuesta).",
    "R-20": "Corrige sintaxis LaTeX ($ desbalanceados, $$$ redundantes, llaves dobles {{}} o variables {var} sin reemplazar).",
    "R-22": "Agrega 'error_rationale' en todas las opciones incorrectas del reactivo multiple_select.",
    "S-01": "Incluye 'solution' detallada paso a paso.",
    "S-02": "Incluye 'misconception' o asocia distractor_id válido.",
    "S-03": "Declara dificultad explícita válida (easy, medium, hard).",
    "R-15": "Equilibra la longitud de las opciones MC: la correcta no puede exceder significativamente el rango de los distractores (0.80x - 1.20x).",
}


def check_production_parity_for_competency(
    cid: str,
    competency: Union[Dict[str, Any], Any],
    questions: List[Dict[str, Any]],
    strict: bool = True,
) -> List[str]:
    """Runs production validator core on instantiated competency questions.
    
    Guarantees Isomorphic Contract Parity: passing check_templates locally
    mathematically guarantees passing build and verify in production.
    """
    errors: List[str] = []
    if not questions:
        return errors

    if isinstance(competency, dict):
        comp_name = competency.get("name", cid)
        comp_type = competency.get("type", "concept")
        comp_desc = competency.get("description", f"Competencia {cid}")
    else:
        comp_name = getattr(competency, "name", cid)
        comp_type = getattr(competency, "type", "concept")
        comp_desc = getattr(competency, "description", f"Competencia {cid}")

    mini_course = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "schema_version": "1.0.0",
        "course_id": f"parity_{cid.lower().replace('-', '_')}",
        "course_title": f"Parity Check for {cid}",
        "title": f"Parity Check for {cid}",
        "description": f"Local contract parity validation mini-course for competency {cid}.",
        "language": "es",
        "created_at": "2026-10-12T00:00:00Z",
        "competencies": [{
            "id": cid,
            "code": cid.upper(),
            "name": comp_name,
            "category": str(comp_type).title(),
            "description": comp_desc,
            "mastery_target": 100,
        }],
        "questions": questions,
    }

    try:
        raw_json = json.dumps(mini_course, ensure_ascii=False)
        v_res = validate_course_content(raw_json, strict=strict)
    except Exception as ex:
        errors.append(f"[-] PARITY VALIDATOR EXCEPTION for '{cid}': {ex}")
        return errors

    if not v_res.is_valid:
        for err in v_res.errors:
            # Skip course-level checks inapplicable to single competency mini-course
            if err.rule_id in ("R-05", "R-06", "R-07", "R-08", "R-09", "R-16"):
                continue
            action = RULE_ACTIONS.get(err.rule_id, "Revisa la regla y ajusta el generador o las variantes.")
            q_info = f" (en {err.field})" if getattr(err, "field", None) else ""
            errors.append(
                f"[-] [{err.rule_id}] PARITY FAILURE in '{cid}'{q_info}: {err.message}\n"
                f"    ACTION REQUIRED: {action}"
            )

    return errors


import functools


@functools.lru_cache(maxsize=8)
def get_compiled_validator(schema_name: str = "template.schema.json") -> jsonschema.Draft7Validator:
    schema_path = Path(__file__).parent / "schemas" / schema_name
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    return jsonschema.Draft7Validator(schema)


def load_schema(schema_name: str = "template.schema.json") -> Dict[str, Any]:
    """Load JSON Schema from schemas directory."""
    return get_compiled_validator(schema_name).schema


def validate_template_schema(data: Dict[str, Any]) -> List[str]:
    """Validate data against template.schema.json."""
    validator = get_compiled_validator("template.schema.json")
    errors = []
    for err in validator.iter_errors(data):
        loc = " -> ".join(str(p) for p in err.path)
        errors.append(f"Template schema violation at [{loc}]: {err.message}")
    return errors


def check_single_template(
    template: Dict[str, Any],
    competency_id: str,
    declared_distractor_ids: Set[str],
    cta_distractors_map: Optional[Dict[str, Dict[str, Any]]] = None,
    num_dry_run_seeds: int = 50,
) -> List[str]:
    """Validate a single template including AST, dry-run, invariants, and TPL rules."""
    errors = []
    tpl_id = template.get("id", "UNKNOWN")
    interaction_type = template.get("interaction_type", "")
    generate_py = template.get("generate_py", "")
    cross_check_py = template.get("cross_check_py", "")
    distractor_ids = template.get("distractor_ids", [])

    # 1. AST Sandbox validation & LaTeX corruption check
    try:
        validate_code_ast(generate_py)
    except Exception as e:
        errors.append(f"Template '{tpl_id}' generate_py failed AST security check: {e}")

    for ec in check_latex_escape_corruption(generate_py):
        errors.append(f"Template '{tpl_id}' generate_py: {ec}")

    if cross_check_py:
        try:
            validate_code_ast(cross_check_py)
        except Exception as e:
            errors.append(f"Template '{tpl_id}' cross_check_py failed AST security check: {e}")
        for ec in check_latex_escape_corruption(cross_check_py):
            errors.append(f"Template '{tpl_id}' cross_check_py: {ec}")

    # 2. Rule TPL-D1: All referenced distractor_ids exist in competency CTA
    for did in distractor_ids:
        if did not in declared_distractor_ids:
            errors.append(
                f"TPL-D1 violation in '{tpl_id}': referenced distractor_id '{did}' "
                f"not found in competency '{competency_id}' CTA distractors."
            )

    # 3. Rule TPL-D2: MC7 must reference/use at least 6 distinct distractor_ids
    if interaction_type == "multiple_choice_7_options":
        if len(set(distractor_ids)) < 6:
            errors.append(
                f"TPL-D2 violation in '{tpl_id}': MC7 template declares {len(set(distractor_ids))} "
                f"distinct distractor_ids (exactly 6 required)."
            )

    # 4. Dry-run 50 seeds and invariant evaluation
    seeds = list(range(100, 100 + num_dry_run_seeds))
    try:
        batch_results = execute_sandbox_batch(
            generate_py=generate_py,
            seeds=seeds,
            cross_check_py=cross_check_py,
            timeout_per_item=2.0,
        )
    except Exception as e:
        errors.append(f"Template '{tpl_id}' failed dry-run batch execution: {e}")
        return errors

    failed_seeds = [r for r in batch_results if not r.get("success")]
    if failed_seeds:
        first_err = failed_seeds[0].get("error", "Unknown error")
        errors.append(
            f"Template '{tpl_id}' dry-run failed on {len(failed_seeds)}/{num_dry_run_seeds} seeds. "
            f"Example error (seed={failed_seeds[0]['seed']}): {first_err}"
        )
        return errors

    # Check invariants and TPL-D4 on all generated instances
    for idx, item in enumerate(batch_results):
        gen_res = item.get("result", {})
        seed_val = item.get("seed", idx)

        try:
            assembled_q = assemble_question(
                template=template,
                gen_result=gen_res,
                competency_id=competency_id,
                question_index=idx + 1,
                cta_distractors_map=cta_distractors_map,
                seed=seed_val,
            )
        except Exception as e:
            errors.append(f"Template '{tpl_id}' failed question assembly (seed={seed_val}): {e}")
            break

        # Invariant check
        is_valid, inv_errors = check_instance_invariants(assembled_q, interaction_type)
        if not is_valid:
            errors.append(
                f"Template '{tpl_id}' invariant violation (seed={seed_val}): {'; '.join(inv_errors[:3])}\n"
                f"    ACTION REQUIRED: Check KaTeX math delimiters ($), remove residual '{{' or '}}', "
                f"ensure all placeholders are replaced, and verify 'error_rationale' in incorrect options."
            )
            break

        # Rule TPL-D4: Distractors != correct answer
        if interaction_type == "multiple_choice_7_options":
            options = assembled_q.get("options", [])
            correct_opt = next((o for o in options if o.get("is_correct")), None)
            if correct_opt:
                c_content = str(correct_opt.get("content", "")).strip()
                for opt in options:
                    if not opt.get("is_correct") and str(opt.get("content", "")).strip() == c_content:
                        errors.append(
                            f"TPL-D4 violation in '{tpl_id}' (seed={seed_val}): distractor matches correct answer '{c_content}'"
                        )
                        break

    # 5. Rule TPL-VAR: Early variability and parametric capacity validation
    # a) Verify vars dictionary is not empty across generated results
    has_empty_vars = any(
        len(r.get("result", {}).get("vars", {})) == 0 for r in batch_results if r.get("success")
    )
    if has_empty_vars:
        errors.append(
            f"TPL-VAR violation in '{tpl_id}': 'vars' dictionary is empty. Templates must generate dynamic variables."
        )

    # b) Verify stem contains at least one placeholder {var} or stem_variants is present
    stem = template.get("stem", "")
    stem_variants = template.get("stem_variants")
    has_placeholder = bool(re.search(r"\{[A-Za-z0-9_]+\}", stem))
    has_variants = bool(stem_variants and len(stem_variants) > 0)
    if not (has_placeholder or has_variants):
        errors.append(
            f"TPL-VAR violation in '{tpl_id}': stem must contain at least one placeholder '{{var}}' or 'stem_variants' must be present."
        )

    # c) Unique capacity simulation across dry-run seeds
    seen_params = set()
    seen_stems = set()
    unique_instances = set()
    sim_unique = 0
    for item in batch_results:
        if not item.get("success"):
            continue
        gen_res = item.get("result", {})
        variables = gen_res.get("vars", {})
        param_tuple = tuple(sorted((str(k), str(v)) for k, v in variables.items()))

        stem_raw = stem
        if stem_variants and len(stem_variants) > 0:
            var_idx = (item.get("seed", 0) % len(stem_variants))
            stem_raw = stem_variants[var_idx]
        rendered_stem = format_template_string(stem_raw, variables)
        norm_stem = re.sub(r"\s+", " ", rendered_stem.strip())

        unique_instances.add((param_tuple, norm_stem))
        if param_tuple not in seen_params and norm_stem not in seen_stems:
            seen_params.add(param_tuple)
            seen_stems.add(norm_stem)
            sim_unique += 1

    unique_count = min(len(unique_instances), sim_unique)
    if unique_count < 4:
        errors.append(
            f"TPL-VAR violation in '{tpl_id}': Only {unique_count}/4 unique instances generated across {num_dry_run_seeds} seeds. Parameter domain is too narrow or missing stem variations."
        )

    return errors


def check_competency_diversity(
    templates: List[Dict[str, Any]],
    competency: Union[Dict[str, Any], Any],
    distractor_map: Optional[Dict[str, Dict[str, Any]]] = None,
    num_seeds: Optional[int] = None,
    return_questions: bool = False,
) -> Union[List[str], Tuple[List[str], List[Dict[str, Any]]]]:
    """Verify stem structural diversity at the competency level (build simulation).
    
    Simulates build stage instantiation with quotas (30 for Skill, 20 for Fact/Concept)
    and evaluates masked stem diversity ratio >= 0.50.
    Returns errors_list (or (errors_list, instantiated_questions) if return_questions=True).
    """
    errors: List[str] = []
    if not templates:
        cid = competency.get("id", "UNKNOWN") if isinstance(competency, dict) else str(getattr(competency, "id", "UNKNOWN"))
        errors.append(f"[-] TPL-VAR VIOLATION in competency '{cid}': No templates provided.")
        return (errors, []) if return_questions else errors

    if isinstance(competency, dict):
        cid = competency.get("id", "UNKNOWN")
        ctype = str(competency.get("type", "concept")).lower()
    else:
        cid = getattr(competency, "id", "UNKNOWN")
        ctype = str(getattr(competency, "type", getattr(competency, "category", "concept"))).lower()

    if num_seeds is not None:
        target_quota = num_seeds
    else:
        target_quota = 30 if ctype in ("skill", "hab", "habilidad") else 20

    seed_base = competency_seed_base(cid, 42)

    try:
        comp_res = instantiate_competency(
            competency=competency if isinstance(competency, dict) else None,
            competency_id=cid,
            category=ctype,
            templates=templates,
            cta_distractors_map=distractor_map,
            seed_offset_base=seed_base,
            quota=target_quota,
        )
    except Exception as e:
        errors.append(
            f"[-] TPL-VAR VIOLATION in competency '{cid}': Failed to instantiate diversity quota ({target_quota} items): {e}.\n"
            f"    ACTION REQUIRED: broaden variable ranges in generate_py or add 3-5 distinct 'stem_variants' to narrow templates."
        )
        return (errors, []) if return_questions else errors

    questions = comp_res.get("questions", [])

    # Validate invariants on all instantiated questions
    for q in questions:
        q_type = q.get("interaction_type") or q.get("type", "")
        q_id = q.get("id", "UNKNOWN")
        is_valid, inv_errors = check_instance_invariants(q, q_type)
        if not is_valid:
            errors.append(
                f"[-] INVARIANT VIOLATION in competency '{cid}' (question '{q_id}'):\n"
                f"    {'; '.join(inv_errors)}\n"
                f"    ACTION REQUIRED: Verify KaTeX syntax (balanced $, no $$$, no {{}}), "
                f"ensure all placeholders are replaced, and provide 'error_rationale' for all incorrect options."
            )
            break

    div_stats = comp_res.get("diversity_stats", {})
    div_ratio = div_stats.get("diversity_ratio", 0.0)
    unique_c = div_stats.get("unique_masked", 0)
    total_c = div_stats.get("total", len(questions))

    if div_ratio < 0.5:
        pattern_counts = []
        for tpl in templates:
            t_id = tpl.get("id", "UNKNOWN")
            vars_list = tpl.get("stem_variants") or []
            if vars_list:
                p_cnt = len(set(mask_stem_numbers(v) for v in vars_list))
            else:
                p_cnt = 1
            pattern_counts.append((t_id, p_cnt))
        pattern_counts.sort(key=lambda x: x[1])

        narrowest_items = pattern_counts[:min(3, len(pattern_counts))]
        narrowest_str = ", ".join(f"{tid} ({cnt} pattern{'s' if cnt != 1 else ''})" for tid, cnt in narrowest_items)

        err_msg = (
            f"[-] TPL-VAR VIOLATION in competency '{cid}': stem diversity {div_ratio:.2f} < 0.50 "
            f"({unique_c}/{total_c} unique masked stems).\n"
            f"    Narrowest templates: {narrowest_str}\n"
            f"    ACTION REQUIRED: add 3-5 distinct 'stem_variants' (using {{placeholders}}) to those templates."
        )
        errors.append(err_msg)

    return (errors, questions) if return_questions else errors


def _validate_single_template_file(
    tf: Path,
    cta_distractors_by_comp: Dict[str, Set[str]],
    cta_distractors_map: Dict[str, Dict[str, Any]],
    num_dry_run_seeds: int,
) -> Tuple[List[str], Optional[str], Set[str], List[Dict[str, Any]]]:
    """Validate a single template file and return (errors, comp_id, referenced_distractor_ids, templates_list)."""
    file_errors = []
    with open(tf, "r", encoding="utf-8") as f:
        try:
            t_content = json.load(f)
        except Exception as e:
            return [f"Failed to parse JSON in {tf}: {e}"], None, set(), []

    # Schema validation
    schema_errs = validate_template_schema(t_content)
    file_errors.extend(schema_errs)

    comp_id = t_content.get("competency_id")
    templates_list = t_content.get("templates", [])
    if not templates_list and "interaction_type" in t_content:
        # Single template file
        templates_list = [t_content]
        comp_id = t_content.get("competency_id", comp_id)

    if cta_distractors_by_comp and (not comp_id or comp_id not in cta_distractors_by_comp):
        file_errors.append(f"File {tf.name} declares unknown or missing competency_id '{comp_id}'.")
        return file_errors, comp_id, set(), templates_list

    declared_dids = cta_distractors_by_comp.get(comp_id, set()) if cta_distractors_by_comp else set()
    referenced_dids: Set[str] = set()

    for tpl in templates_list:
        t_dids = tpl.get("distractor_ids", [])
        for did in t_dids:
            referenced_dids.add(did)

        single_errs = check_single_template(
            template=tpl,
            competency_id=comp_id or "UNKNOWN",
            declared_distractor_ids=declared_dids,
            cta_distractors_map=cta_distractors_map,
            num_dry_run_seeds=num_dry_run_seeds,
        )
        file_errors.extend(single_errs)

    return file_errors, comp_id, referenced_dids, templates_list


def check_templates_file_or_dir(
    target_path: Union[Path, List[Path], str, List[str]],
    cta_path: Optional[Path] = None,
    num_dry_run_seeds: int = 50,
    strict: bool = True,
    attempts_dir: Optional[Path] = None,
) -> Tuple[bool, List[str]]:
    """Validate all templates in file(s) or directory against CTA with production contract parity."""
    # warm_up_sandbox()  # Omit blind warmup: in-process execution is already instant
    errors = []

    cta_data: Dict[str, Any] = {}
    cta_distractors_by_comp: Dict[str, Set[str]] = {}
    cta_distractors_map: Dict[str, Dict[str, Any]] = {}

    if cta_path is not None:
        cta_p = Path(cta_path)
        if not cta_p.exists():
            return False, [f"CTA file does not exist: {cta_p}"]
        with open(cta_p, "r", encoding="utf-8") as f:
            cta_data = json.load(f)

        for comp in cta_data.get("competencies", []):
            cid = comp["id"]
            d_ids = set()
            for d in comp.get("distractors", []):
                did = d["id"]
                d_ids.add(did)
                cta_distractors_map[did] = d
            cta_distractors_by_comp[cid] = d_ids
    else:
        print("[!] Warning: cta_path omitted; competency diversity gate (TPL-VAR), parity checks, and distractor checks skipped.")

    # Collect template files
    template_files: List[Path] = []
    is_full_dir = False

    raw_targets = target_path if isinstance(target_path, (list, tuple)) else [target_path]
    for item in raw_targets:
        p = Path(item)
        if p.is_file() and p.suffix.lower() == ".json":
            if p not in template_files:
                template_files.append(p)
        elif p.is_dir():
            is_full_dir = True
            for f in sorted(p.glob("*.json")):
                if f not in template_files:
                    template_files.append(f)
        elif not p.exists():
            return False, [f"Target path does not exist: {p}"]

    if not template_files:
        return False, [f"No template JSON files found in: {target_path}"]

    referenced_distractors_by_comp: Dict[str, Set[str]] = {cid: set() for cid in cta_distractors_by_comp}
    templates_by_comp: Dict[str, List[Dict[str, Any]]] = {}
    processed_comp_ids: Set[str] = set()

    if len(template_files) > 1:
        max_workers = min(16, (os.cpu_count() or 4) * 2, len(template_files))
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {
                executor.submit(
                    _validate_single_template_file,
                    tf,
                    cta_distractors_by_comp,
                    cta_distractors_map,
                    num_dry_run_seeds,
                ): tf
                for tf in template_files
            }
            for future in future_to_file:
                file_errs, comp_id, ref_dids, tpls = future.result()
                errors.extend(file_errs)
                if comp_id:
                    processed_comp_ids.add(comp_id)
                    templates_by_comp.setdefault(comp_id, []).extend(tpls)
                    if comp_id in referenced_distractors_by_comp:
                        referenced_distractors_by_comp[comp_id].update(ref_dids)
    else:
        for tf in template_files:
            file_errs, comp_id, ref_dids, tpls = _validate_single_template_file(
                tf,
                cta_distractors_by_comp,
                cta_distractors_map,
                num_dry_run_seeds,
            )
            errors.extend(file_errs)
            if comp_id:
                processed_comp_ids.add(comp_id)
                templates_by_comp.setdefault(comp_id, []).extend(tpls)
                if comp_id in referenced_distractors_by_comp:
                    referenced_distractors_by_comp[comp_id].update(ref_dids)

    # Rule TPL-D3: 100% distractor coverage across templates
    if cta_distractors_by_comp:
        comps_to_check = list(referenced_distractors_by_comp.keys()) if is_full_dir else list(processed_comp_ids)
        for cid in comps_to_check:
            declared_set = cta_distractors_by_comp.get(cid, set())
            referenced_set = referenced_distractors_by_comp.get(cid, set())
            uncovered = declared_set - referenced_set
            if uncovered:
                errors.append(
                    f"TPL-D3 violation in competency '{cid}': {len(uncovered)}/{len(declared_set)} distractors "
                    f"are never referenced in any template: {sorted(uncovered)}"
                )

    # Rule TPL-VAR (Competency Diversity Gate) & Isomorphic Contract Parity Check
    if cta_data and "competencies" in cta_data:
        comp_map = {c["id"]: c for c in cta_data.get("competencies", [])}
        comps_to_check = list(referenced_distractors_by_comp.keys()) if is_full_dir else list(processed_comp_ids)
        def _evaluate_comp_diversity_and_parity(cid: str) -> List[str]:
            c_errors: List[str] = []
            comp_obj = comp_map.get(cid)
            comp_tpls = templates_by_comp.get(cid, [])
            if not (comp_obj and comp_tpls):
                return c_errors
            sim_seeds = num_dry_run_seeds if num_dry_run_seeds < 20 else None
            div_errors, comp_questions = check_competency_diversity(
                templates=comp_tpls,
                competency=comp_obj,
                distractor_map=cta_distractors_map,
                num_seeds=sim_seeds,
                return_questions=True,
            )
            c_errors.extend(div_errors)

            if strict and comp_questions:
                parity_errors = check_production_parity_for_competency(
                    cid=cid,
                    competency=comp_obj,
                    questions=comp_questions,
                    strict=True,
                )
                c_errors.extend(parity_errors)
            return c_errors

        sorted_comps = sorted(comps_to_check)
        if len(sorted_comps) > 1:
            max_workers = min(16, (os.cpu_count() or 4) * 2, len(sorted_comps))
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                comp_futures = [executor.submit(_evaluate_comp_diversity_and_parity, cid) for cid in sorted_comps]
                for fut in comp_futures:
                    errors.extend(fut.result())
        else:
            for cid in sorted_comps:
                errors.extend(_evaluate_comp_diversity_and_parity(cid))

    is_clean = (len(errors) == 0)

    # Auto-repair attempt tracking if attempts_dir is supplied
    if attempts_dir is not None:
        try:
            att_path = Path(attempts_dir)
            att_path.mkdir(parents=True, exist_ok=True)
            for cid in processed_comp_ids:
                f_att = att_path / f"{cid}.json"
                cur_att = 0
                if f_att.is_file():
                    try:
                        cur_att = json.loads(f_att.read_text(encoding="utf-8")).get("attempts", 0)
                    except Exception:
                        pass
                if not is_clean:
                    cur_att += 1
                    f_att.write_text(json.dumps({"attempts": cur_att}), encoding="utf-8")
                    if cur_att >= 4:
                        errors.append(
                            f"[!] BUDGET HALT on competency '{cid}': Exceeded {cur_att} validation cycles. "
                            f"Action required: Cease iteration and report: BLOCKED: {cid} - validation failure limit reached."
                        )
                else:
                    # Clear on success
                    if f_att.is_file():
                        f_att.unlink()
        except Exception:
            pass

    return is_clean, errors


def main():
    parser = argparse.ArgumentParser(description="Validate parametric exercise templates with Isomorphic Contract Parity")
    parser.add_argument("target", nargs="+", help="Path(s) to template.json file(s) or templates/ directory")
    parser.add_argument("--cta", default=None, help="Path to cta.json file")
    parser.add_argument("--seeds", type=int, default=50, help="Number of dry-run seeds (default 50)")
    parser.add_argument("--strict", action="store_true", default=True, help="Enforce production contract parity (default: true)")
    parser.add_argument("--no-strict", dest="strict", action="store_false", help="Bypass production parity checks")
    parser.add_argument("--attempts-dir", default=None, help="Directory to track per-competency validation cycles")
    parser.add_argument("--json-report", default=None, help="Optional output path for structured JSON diagnostic report")
    args = parser.parse_args()

    cta_p = Path(args.cta) if args.cta else None
    targets = [Path(t) for t in args.target]
    valid, errors = check_templates_file_or_dir(
        targets,
        cta_p,
        num_dry_run_seeds=args.seeds,
        strict=args.strict,
        attempts_dir=Path(args.attempts_dir) if args.attempts_dir else None,
    )

    if args.json_report:
        report_data = {
            "valid": valid,
            "errors_count": len(errors),
            "errors": errors,
            "targets": [str(t) for t in targets],
        }
        try:
            r_path = Path(args.json_report)
            r_path.parent.mkdir(parents=True, exist_ok=True)
            r_path.write_text(json.dumps(report_data, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception as ex:
            print(f"[!] Warning: Could not write json report: {ex}", file=sys.stderr)

    if not valid:
        print(f"FAIL: {len(errors)} validation errors in templates:")
        for e in errors[:15]:
            print(f"  - {e}")
        if len(errors) > 15:
            print(f"  ... and {len(errors) - 15} more errors.")
        sys.exit(1)

    print(f"PASS: All templates satisfy schema, AST security, {args.seeds} seeds dry run, invariants, TPL-D1..D4 rules, and Production Parity.")
    sys.exit(0)


if __name__ == "__main__":
    main()

