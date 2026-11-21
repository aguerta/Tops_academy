"""Extracted compilation phase steps and shared helpers for compile_shard."""

import ast
import collections
import hashlib
import inspect
import json
import re
import sys
import textwrap
import time
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from engine.invariants import validate_katex_syntax
from engine.shard_ast_transforms import (
    EvaluationContext,
    _QTYPE_TO_INTERACTION,
    _check_intra_competency_anti_clone,
    _wrap_gen_raw_with_auto_vars,
    extract_function_code,
)
from engine.shard_locator import ShardDataLineLocator, _find_diagnostic_line
from engine.stage_contract import (
    ARCHETYPE_KINDS as _S4_ARCHETYPE_KINDS,
    MAX_MODALITIES_PER_COMPETENCY as _S4_MAX_MODS,
    MIN_MODALITIES_PER_COMPETENCY as _S4_MIN_MODS,
    competency_contract as _s4_competency_contract,
    is_skill_type as _s4_is_skill_type,
    quota_for_competency as _s4_quota_for_competency,
    required_templates_for_competency as _s4_required_templates,
    required_unique_stems as _s4_required_unique_stems,
    stems_advice as _s4_stems_advice,
)
from engine.template_healing import (
    _atomic_write_json,
    _find_telltale_in_option,
    _strip_giveaway_prefix,
    auto_heal_template_data,
    detect_frankenstein_sum,
    heal_control_chars_in_obj,
    heal_shard_source_text,
    is_trivial_verifier,
    normalize_double_braces,
    parse_katex_number,
    pykatex_warnings,
)

ACTIVE_INTERACTION_TYPES: Set[str] = {
    "fill_in_the_blank",
    "multiple_select",
    "open_symbolic",
    "proof_dag",
    "adversarial_break",
    "unstructured_model",
    "invariant_canvas",
    "concept_matching",
}

PURE_PRODUCTION_TYPES: Set[str] = {
    "fill_in_the_blank",
    "open_symbolic",
    "proof_dag",
    "adversarial_break",
    "unstructured_model",
    "invariant_canvas",
}

STRUCTURED_M20_TYPES: Set[str] = {
    "proof_dag",
    "adversarial_break",
    "unstructured_model",
    "invariant_canvas",
    "concept_matching",
}

_STRUCTURED_PAYLOAD_KEYS = (
    "proof_dag",
    "dag",
    "adversarial_break",
    "adversarial",
    "unstructured_model",
    "stage0",
    "invariant_canvas",
    "canvas",
    "concept_matching",
    "matching",
    "symbolic_config",
    "accepted_equivalents",
)


def _extract_m20_structured_dids(interaction_type: str, compiled: Any) -> List[str]:
    """Extract normalized distractor_ids from a compiled M20 structured modality payload."""
    if not isinstance(compiled, dict):
        return []
    raw_dids: List[str] = []

    def _add_did(obj: Any) -> None:
        if isinstance(obj, dict):
            did = obj.get("distractor_id") or obj.get("did")
            if isinstance(did, str) and did.strip():
                raw_dids.append(did.strip().replace("_", "-"))

    if interaction_type == "proof_dag":
        from engine.proof_compiler import extract_proof_dag_distractor_ids
        return extract_proof_dag_distractor_ids(compiled)
    if interaction_type == "adversarial_break":
        from engine.adversarial_generator import extract_adversarial_distractor_ids
        return extract_adversarial_distractor_ids(compiled)
    if interaction_type == "unstructured_model":
        for item in (compiled.get("phase1_variables") or {}).get("items") or []:
            _add_did(item)
        for opt in (compiled.get("phase2_assumptions") or {}).get("options") or []:
            _add_did(opt)
        p3 = compiled.get("phase3_formulation") or {}
        for opt in p3.get("options") or []:
            _add_did(opt)
        for dd in p3.get("diagnostic_distractors") or []:
            _add_did(dd)
    elif interaction_type == "invariant_canvas":
        for inv in compiled.get("invariants") or []:
            _add_did(inv)
        ti = compiled.get("tree_invariants") or {}
        if isinstance(ti, dict):
            _add_did(ti)
            for tdid in ti.get("distractor_ids") or []:
                if isinstance(tdid, str) and tdid.strip():
                    raw_dids.append(tdid.strip().replace("_", "-"))
    elif interaction_type == "concept_matching":
        for tg in compiled.get("targets") or []:
            _add_did(tg)
    return list(dict.fromkeys(raw_dids))


def _structured_payload_fingerprint(res: Dict[str, Any]) -> str:
    """Return deterministic JSON fingerprint for structured M20 keys present in a generator dict."""
    sub = {k: res[k] for k in _STRUCTURED_PAYLOAD_KEYS if k in res and res[k] is not None}
    return json.dumps(sub, sort_keys=True, default=str) if sub else ""




def normalize_form_c_template(t: Any) -> Any:
    """Normalizes template entry: converts ShardCompetenceContract or Pydantic BaseModel to Form-C dict.

    Transparently supports:
    1. Instances of ShardCompetenceContract (with to_form_c_dict())
    2. Pydantic BaseModel instances (with model_dump())
    3. Form-C dicts (unchanged)
    4. Form-B 9-tuples (unchanged)
    """
    if hasattr(t, "to_form_c_dict") and callable(getattr(t, "to_form_c_dict")):
        return t.to_form_c_dict()
    if hasattr(t, "model_dump") and callable(getattr(t, "model_dump")):
        data = dict(t.model_dump())
        field_mapping = {
            "competence_id": "cid",
            "archetype": "archetype",
            "assumption_tested_id": "assumption_id",
            "statement_variants_markdown": "stems",
            "hints_markdown": "hints",
            "solution_markdown": "sol",
        }
        out = {}
        for k, v in data.items():
            mapped_k = field_mapping.get(k, k)
            out[mapped_k] = v
        # Preserve non-dumped callables or attributes on the model
        for attr in ("gen", "ver", "generator_code", "verifier_code", "fmt", "rats", "band", "qtype", "id", "cid"):
            if attr not in out and hasattr(t, attr):
                out[attr] = getattr(t, attr)
        return out
    return t


def _format_with_fmt(val_str: str, fmt_str: Optional[str]) -> str:
    """Applies @X@ template format string once without duplicating prefix or suffix."""
    if not val_str or not fmt_str or "@X@" not in fmt_str:
        return val_str
    pfx, sfx = fmt_str.split("@X@", 1)
    if pfx and sfx:
        if val_str.startswith(pfx) and val_str.endswith(sfx):
            return val_str
    elif pfx:
        if val_str.startswith(pfx):
            return val_str
    elif sfx:
        if val_str.endswith(sfx):
            return val_str
    return fmt_str.replace("@X@", val_str)


def _make_sandbox_rng(seed: int):
    """Creates a random.Random instance with _LazyNPRNG attached, matching engine.sandbox."""
    import random
    rng = random.Random(seed)
    try:
        from engine.sandbox import _LazyNPRNG
        rng.np = _LazyNPRNG(seed)
    except Exception:
        pass
    return rng


def build_adapted_mc7_generator(
    base_gen_code: str,
    cid: str,
    cta_distractors: List[Dict[str, Any]],
    strict: bool = True,
    rats_map: Optional[Dict[str, str]] = None,
    fmt: Optional[str] = None,
) -> str:
    """Wraps an MC7 generator function to assemble options list with 1 correct and distractors.

    In strict mode:
    - Eliminates magical multipliers and synthetic positional assignment.
    - Rejects 2-tuples (did, val) unless declared in rats_map/RATS, and requires 3-tuples.
    - Ensures distractor IDs match declared CTA distractors.
    """
    declared_ids_list = [d.get("id") for d in cta_distractors if isinstance(d, dict) and d.get("id")]
    declared_ids_repr = ("{" + ",".join(repr(x) for x in sorted(declared_ids_list)) + "}") if declared_ids_list else "set()"
    strict_repr = "True" if strict else "False"
    relevant_rats = {k: v for k, v in (rats_map or {}).items() if not declared_ids_list or k in declared_ids_list}

    base = base_gen_code.rstrip()
    if base.endswith("generate = generate_params"):
        base = base[:-len("generate = generate_params")].rstrip()

    if fmt and "@X@" in fmt:
        pfx, sfx = fmt.split("@X@", 1)
        if pfx and sfx:
            cond = f"(not s or (s.startswith({repr(pfx)}) and s.endswith({repr(sfx)})))"
        elif pfx:
            cond = f"(not s or s.startswith({repr(pfx)}))"
        elif sfx:
            cond = f"(not s or s.endswith({repr(sfx)}))"
        else:
            cond = "False"
        fmt_helper = f'lambda s: (s if {cond} else {repr(fmt)}.replace("@X@", s))'
    else:
        fmt_helper = "lambda s: s"

    if not relevant_rats:
        if fmt and "@X@" in fmt:
            fmt_def = f"f={fmt_helper}"
            f_c = 'f(str(r.get("correct") if r.get("correct") is not None else r.get("ans","")).strip())'
            f_w = "f(str(d[1]).strip())"
        else:
            fmt_def = ""
            f_c = 'str(r.get("correct") if r.get("correct") is not None else r.get("ans","")).strip()'
            f_w = "str(d[1]).strip()"
        wrapper = f"""{base}
_c2c_gen_inner=generate_params
def generate_params(rng):
 r=_c2c_gen_inner(rng)
 if isinstance(r,(tuple,list)):r={{"vars":r[0] if isinstance(r[0],dict) else {{"val":r[0]}},"correct":str(r[1]) if len(r)>1 else "","distractors":r[2] if len(r)>2 else []}}
 elif not isinstance(r,dict):return r
 {fmt_def}
 ids,st={declared_ids_repr},{strict_repr}
 ds=[]
 for d in (r.get("distractors") or r.get("ds") or []):
  if isinstance(d,(tuple,list)) and len(d)>=3:
   did=str(d[0]).strip().replace("_","-")
   if ids and did not in ids and st:raise ValueError(f"Distractor ID '{{did}}' no esta declarado en cta.json ({cid}).")
   w={f_w};ds.append({{"value":w,"content":w,"distractor_id":did,"error_rationale":str(d[2]),"is_correct":False}})
  elif isinstance(d,(tuple,list)) and len(d)==2 and not st:
   did=str(d[0]).strip().replace("_","-");w={f_w}
   ds.append({{"value":w,"content":w,"distractor_id":did,"error_rationale":"","is_correct":False}})
  elif isinstance(d,dict):
   did=d.get("distractor_id") or d.get("id")
   if did:did=str(did).strip().replace("_","-")
   if did and ids and did not in ids and st:raise ValueError(f"Distractor ID '{{did}}' no esta declarado en cta.json ({cid}).")
   raw_w=str(d.get("value") if d.get("value") is not None else (d.get("content") or d.get("ans",""))).strip()
   w=f(raw_w) if {bool(fmt and "@X@" in fmt)} else raw_w
   rat=str(d.get("error_rationale") or d.get("rationale") or "")
   ds.append({{"value":w,"content":w,"distractor_id":did,"error_rationale":rat,"is_correct":False}})
  elif st:raise ValueError(f"[TPL-MC7-STRICT] 3-tupla requerida: {{d!r}}")
 c={f_c}
 r["correct"],r["distractors"],r["options"]=c,ds,[{{"value":c,"content":c,"is_correct":True}}]+ds
 return r
generate=generate_params
"""
    else:
        rats_map_repr = json.dumps(relevant_rats, separators=(",", ":"))
        ids_code = "set(rats)" if (set(relevant_rats) >= set(declared_ids_list)) else f"{declared_ids_repr}|set(rats)"
        wrapper = f"""{base}
_c2c_gen_inner=generate_params
def generate_params(rng):
 r=_c2c_gen_inner(rng)
 if isinstance(r,(tuple,list)):r={{"vars":r[0] if isinstance(r[0],dict) else {{"val":r[0]}},"correct":str(r[1]) if len(r)>1 else "","distractors":r[2] if len(r)>2 else []}}
 elif not isinstance(r,dict):return r
 rats,st,f={rats_map_repr},{strict_repr},{fmt_helper}
 ids={ids_code}
 c=f(str(r.get("correct") if r.get("correct") is not None else r.get("ans","")).strip())
 r["correct"],ds=c,[]
 for d in (r.get("distractors") or r.get("ds") or []):
  if isinstance(d,dict):v,i,t=str(d.get("value") if d.get("value") is not None else (d.get("content") or d.get("ans",""))).strip(),d.get("distractor_id") or d.get("id"),d.get("error_rationale") or d.get("rationale")
  elif isinstance(d,(tuple,list)) and len(d)>=2:
   d0=str(d[0]).strip().replace("_","-")
   i,v=(d0,str(d[1]).strip()) if (d0.startswith("D-") or d0 in ids) else (str(d[1]).strip().replace("_","-"),str(d[0]).strip())
   t=str(d[2]).strip() if len(d)>2 else rats.get(i)
   if not t and st:raise ValueError(f"[TPL-MC7-STRICT] 3-tupla requerida: {{d!r}}")
  elif st:raise ValueError(f"Distractor escalar no permitido: {{d!r}}")
  else:i,t,v=None,"",str(d[0] if isinstance(d,(tuple,list)) and d else d).strip()
  if i and ids and i not in ids and st:raise ValueError(f"Distractor ID '{{i}}' no esta declarado en cta.json ({cid}).")
  w=f(v);ds.append({{"value":w,"content":w,"distractor_id":i,"error_rationale":t or "","is_correct":False}})
 r["distractors"],r["options"]=ds,[{{"value":c,"content":c,"is_correct":True}}]+ds
 return r
generate=generate_params
"""
    return wrapper




def compile_tuple_records_to_templates(
    tuple_records: List[Dict[str, Any]],
    cta_comp_map: Dict[str, Dict[str, Any]],
    strict: bool,
    module_rats: Dict[str, str],
    norm_shard_id: str,
    templates_by_cid: Dict[str, List[Dict[str, Any]]],
    gen_callables_by_cid: Dict[str, List[Any]],
    deferred_hints_dup_errors: List[str],
    deferred_verifier_errors: List[str],
    step5_err_fn: Any,
    fail_fn: Any,
) -> Optional[Tuple[bool, List[str]]]:
    """Compile normalized Form-B/Form-C tuple records into canonical template dicts grouped by competency."""
    for t_idx, rec in enumerate(tuple_records):
        t = normalize_form_c_template(rec["tuple"])
        rec["tuple"] = t
        curr_loc = rec["locator"]
        curr_p = rec["file_path"]
        orig_idx = rec["orig_idx"]

        # Determine format (Form-C dict vs Form-B 9-tuple)
        is_form_c = isinstance(t, dict)
        if is_form_c:
            tpl_id = str(t.get("id") or t.get("tpl_id") or t.get("template_id") or "").strip()
            cid = str(t.get("cid") or t.get("competency_id") or "").strip()
            qtype_in = str(t.get("qtype") or t.get("question_type") or "").strip().lower()
            qtype = _QTYPE_TO_INTERACTION.get(qtype_in, qtype_in)
            gen_raw = t.get("gen") or t.get("generator_code") or t.get("generate_py")
            ver_raw = t.get("ver") or t.get("verifier_code") or t.get("cross_check_py")
            diff_raw = t.get("band") or t.get("difficulty_bloom")
            if not diff_raw and t.get("difficulty") and t.get("bloom"):
                diff_raw = (t.get("difficulty"), t.get("bloom"))
            stems_raw = t.get("stems") or t.get("stem_variants") or t.get("stem")
            hints_raw = t.get("hints")
            sol_raw = str(t.get("sol") or t.get("solution") or t.get("explanation_es") or "")
            archetype = t.get("archetype")
            assumption_id = t.get("assumption_id")
            fmt_str = t.get("fmt")
            tpl_rats = t.get("rats") if isinstance(t.get("rats"), dict) else {}
        elif isinstance(t, (list, tuple)) and len(t) == 9:
            tpl_id = str(t[0]).strip()
            cid = str(t[1]).strip()
            qtype = str(t[2]).strip().lower()
            gen_raw = t[3]
            ver_raw = t[4]
            diff_raw = t[5]
            stems_raw = t[6]
            hints_raw = t[7]
            sol_raw = str(t[8])
            archetype = None
            assumption_id = None
            fmt_str = None
            tpl_rats = {}
        else:
            err_msg = f"FAIL: Entrada en índice {orig_idx} no cumple el contrato Form-B de 9 elementos ni Form-C dict: {repr(t)}"
            if step5_err_fn(err_msg):
                return fail_fn(err_msg)
            continue

        target_kc = cid
        target_misc = []
        src_ref = {"doc": "manifest.pdf", "page": 1, "quote": ""}

        # Determine difficulty and bloom (element must be 2-tuple (difficulty, bloom))
        if not isinstance(diff_raw, (list, tuple)) or len(diff_raw) != 2:
            err_msg = (
                f"FAIL: El elemento de dificultad en tupla {orig_idx} ('{tpl_id}') debe ser explícitamente "
                f"una 2-tupla (difficulty, bloom) (ej. ('easy', 'Remember')), se recibió: {repr(diff_raw)}."
            )
            if step5_err_fn(err_msg):
                return fail_fn(err_msg)
            difficulty = "easy"
            bloom = "Remember"
        else:
            difficulty = str(diff_raw[0]).lower().strip()
            bloom = str(diff_raw[1]).capitalize().strip()

            if difficulty not in ("easy", "medium", "hard"):
                err_msg = (
                    f"FAIL: Dificultad inválida '{difficulty}' en tupla {orig_idx} ('{tpl_id}'). "
                    f"Debe ser 'easy', 'medium' o 'hard'."
                )
                if step5_err_fn(err_msg):
                    return fail_fn(err_msg)
            if bloom not in ("Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"):
                err_msg = (
                    f"FAIL: Nivel de Bloom inválido '{bloom}' en tupla {orig_idx} ('{tpl_id}'). "
                    f"Debe ser Remember, Understand, Apply, Analyze, Evaluate o Create."
                )
                if step5_err_fn(err_msg):
                    return fail_fn(err_msg)

        # Determine interaction_type
        interaction_type = _QTYPE_TO_INTERACTION.get(qtype, qtype)
        if interaction_type == "fill_in_the_blank":
            target_misc = []

        # Stems Cartesian expansion if 2-tuple of (contexts, questions)
        if isinstance(stems_raw, (list, tuple)) and len(stems_raw) == 2:
            ctxs, qsts = stems_raw[0], stems_raw[1]
            if isinstance(ctxs, (list, tuple)) and isinstance(qsts, (list, tuple)) and len(ctxs) >= 2 and len(qsts) >= 2:
                stems_raw = [f"{str(c).strip()} {str(q).strip()}" for c in ctxs for q in qsts]

        # Extract functions using originating file locator
        tuple_info = curr_loc.get_tuple_info(orig_idx) or curr_loc.get_tuple_info(cid) or {}
        gen_fn_name = tuple_info.get("gen_fn_name") or getattr(gen_raw, "__name__", None)
        ver_fn_name = tuple_info.get("ver_fn_name") or getattr(ver_raw, "__name__", None)

        gen_code = extract_function_code(gen_raw, "generate_params", locator=curr_loc, fn_name_hint=gen_fn_name)
        gen_raw = _wrap_gen_raw_with_auto_vars(gen_raw, gen_code)
        ver_code = extract_function_code(ver_raw, "verify", locator=curr_loc, fn_name_hint=ver_fn_name)

        # Check if ver_raw is a 2-argument verifier ver(cand, v)
        is_two_arg_ver = False
        if callable(ver_raw):
            try:
                sig = inspect.signature(ver_raw)
                pos_params = [
                    p for p in sig.parameters.values()
                    if p.default == inspect.Parameter.empty and p.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
                ]
                # Solo 2 argumentos posicionales OBLIGATORIOS => ver(cand, v).
                # Firmas con opcionales (res, v=None) o *args reciben la instancia completa.
                if len(pos_params) == 2:
                    is_two_arg_ver = True
            except Exception:
                pass

        if is_two_arg_ver:
            base_v = ver_code.rstrip()
            if base_v.endswith("cross_check = verify"):
                base_v = base_v[:-len("cross_check = verify")].rstrip()
            ver_code = f"""{base_v}
_v=verify
def verify(inst):
 if not isinstance(inst,dict):return False
 c=inst["correct"] if ("correct" in inst and inst["correct"] is not None) else inst.get("ans")
 try:return _v(c,inst.get("vars",{{}}))
 except Exception:return False
cross_check=verify
"""

        def run_ver(c_val, vars_d, inst_d):
            if not callable(ver_raw):
                return True
            try:
                if is_two_arg_ver:
                    return ver_raw(c_val, vars_d)
                else:
                    return ver_raw(inst_d)
            except TypeError:
                try:
                    return ver_raw(inst_d)
                except TypeError:
                    return ver_raw(c_val, vars_d)

        # Check non-trivial verifier
        ver_is_trivial, ver_reason = is_trivial_verifier(ver_code, ver_raw)
        if ver_is_trivial:
            err_msg = (
                f"FAIL: [TPL-VERIFIER] El verificador ver_fn '{ver_fn_name}' en '{tpl_id}' es trivial ({ver_reason}). "
                f"Debe evaluar condiciones lógicas o matemáticas reales sobre el resultado generado."
            )
            if step5_err_fn(err_msg):
                return fail_fn(err_msg)

        # Verifier AST Hygiene checks
        if ver_fn_name and curr_loc and hasattr(curr_loc, "functions") and ver_fn_name in curr_loc.functions:
            s_v, e_v = curr_loc.functions[ver_fn_name]
            v_src = "\n".join(curr_loc.lines[s_v - 1 : e_v])
            try:
                v_ast = ast.parse(textwrap.dedent(v_src))
                for sub in ast.walk(v_ast):
                    if isinstance(sub, ast.Try):
                        for h in sub.handlers:
                            for s in h.body:
                                if isinstance(s, ast.Return) and isinstance(s.value, ast.Constant) and bool(s.value.value) is True:
                                    err_msg = (
                                        f"FAIL: [VERIFIER-SWALLOWED-EXCEPTION] El verificador ver_fn '{ver_fn_name}' en '{tpl_id}' (Líneas {s_v}..{e_v} en {curr_p.name}) "
                                        f"contiene un bloque try/except que retorna True en el manejador de excepción. Los errores de validación deben resultar en False."
                                    )
                                    if step5_err_fn(err_msg):
                                        return fail_fn(err_msg)
                    elif isinstance(sub, ast.Raise):
                        exc_n = ""
                        if isinstance(sub.exc, ast.Call) and isinstance(sub.exc.func, ast.Name):
                            exc_n = sub.exc.func.id
                        elif isinstance(sub.exc, ast.Name):
                            exc_n = sub.exc.id
                        err_msg = (
                            f"FAIL: [TPL-DEBUG-ARTIFACT] El verificador ver_fn '{ver_fn_name}' en '{tpl_id}' contiene una sentencia 'raise {exc_n}'. "
                            f"Los verificadores deben retornar booleanos sin sentencias 'raise' de depuración."
                        )
                        if step5_err_fn(err_msg):
                            return fail_fn(err_msg)
                    elif isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name) and sub.func.id in ("breakpoint", "print"):
                        err_msg = f"FAIL: [TPL-DEBUG-ARTIFACT] El verificador ver_fn '{ver_fn_name}' en '{tpl_id}' contiene una llamada a '{sub.func.id}()'."
                        if step5_err_fn(err_msg):
                            return fail_fn(err_msg)
                    elif isinstance(sub, ast.Import) and any(a.name == "pdb" for a in sub.names):
                        err_msg = f"FAIL: [TPL-DEBUG-ARTIFACT] El verificador ver_fn '{ver_fn_name}' en '{tpl_id}' importa 'pdb'."
                        if step5_err_fn(err_msg):
                            return fail_fn(err_msg)
            except Exception:
                pass

        # Generator AST Hygiene checks (tracing call graph from gen_fn to local private helpers)
        if gen_fn_name and curr_loc and hasattr(curr_loc, "functions") and gen_fn_name in curr_loc.functions:
            reachable_fns = []
            queue = [gen_fn_name]
            seen_fns = set()
            from shard_precheck import is_bounded_while
            while queue:
                curr_fn = queue.pop(0)
                if curr_fn in seen_fns:
                    continue
                seen_fns.add(curr_fn)
                if curr_fn in curr_loc.functions:
                    reachable_fns.append(curr_fn)
                    s_fn, e_fn = curr_loc.functions[curr_fn]
                    fn_src = "\n".join(curr_loc.lines[s_fn - 1 : e_fn])
                    try:
                        parsed_fn = ast.parse(textwrap.dedent(fn_src))
                        for child in ast.walk(parsed_fn):
                            if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                                callee = child.func.id
                                if callee in curr_loc.functions and callee not in seen_fns:
                                    queue.append(callee)
                    except Exception:
                        pass

            for curr_fn in reachable_fns:
                s_g, e_g = curr_loc.functions[curr_fn]
                g_src = "\n".join(curr_loc.lines[s_g - 1 : e_g])
                try:
                    g_ast = ast.parse(textwrap.dedent(g_src))
                    for sub in ast.walk(g_ast):
                        if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name) and sub.func.id in ("breakpoint", "print"):
                            err_msg = f"FAIL: [TPL-DEBUG-ARTIFACT] La función '{curr_fn}' en '{tpl_id}' contiene una llamada a '{sub.func.id}()'."
                            if step5_err_fn(err_msg):
                                return fail_fn(err_msg)
                        elif isinstance(sub, ast.Import) and any(a.name == "pdb" for a in sub.names):
                            err_msg = f"FAIL: [TPL-DEBUG-ARTIFACT] La función '{curr_fn}' en '{tpl_id}' importa 'pdb'."
                            if step5_err_fn(err_msg):
                                return fail_fn(err_msg)
                        elif isinstance(sub, ast.Raise):
                            exc_n = ""
                            if isinstance(sub.exc, ast.Call) and isinstance(sub.exc.func, ast.Name):
                                exc_n = sub.exc.func.id
                            elif isinstance(sub.exc, ast.Name):
                                exc_n = sub.exc.id
                            err_msg = (
                                f"FAIL: [TPL-DEBUG-ARTIFACT] La función '{curr_fn}' en '{tpl_id}' contiene una sentencia 'raise {exc_n}'. "
                                f"Las funciones generadoras de ítems deben retornar un diccionario de variables y opciones, sin sentencias 'raise' de depuración."
                            )
                            if step5_err_fn(err_msg):
                                return fail_fn(err_msg)
                    if "clean_ds" in curr_fn:
                        err_msg = (
                            f"FAIL: [TPL-AD-HOC-PERTURBATION] La función '{curr_fn}' en '{tpl_id}' utiliza perturbación ad-hoc ('clean_ds'). "
                            f"Los distractores deben originarse en modelos de error conceptuales o algebraicos."
                        )
                        if step5_err_fn(err_msg):
                            return fail_fn(err_msg)
                    for sub in ast.walk(g_ast):
                        if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name) and "clean_ds" in sub.func.id:
                            err_msg = f"FAIL: [TPL-AD-HOC-PERTURBATION] La función '{curr_fn}' en '{tpl_id}' invoca la función de perturbación '{sub.func.id}'."
                            if step5_err_fn(err_msg):
                                return fail_fn(err_msg)
                        elif isinstance(sub, ast.While):
                            for w_sub in ast.walk(sub):
                                if isinstance(w_sub, ast.BinOp) and isinstance(w_sub.op, ast.Add):
                                    if isinstance(w_sub.right, ast.Constant) and isinstance(w_sub.right.value, float):
                                        err_msg = f"FAIL: [TPL-AD-HOC-PERTURBATION] Bucle while de perturbación numérica ad-hoc detectado en '{curr_fn}' de '{tpl_id}'."
                                        if step5_err_fn(err_msg):
                                            return fail_fn(err_msg)
                                    if isinstance(w_sub.right, ast.Call) and getattr(w_sub.right.func, "id", "") in ("uniform", "random"):
                                        err_msg = f"FAIL: [TPL-AD-HOC-PERTURBATION] Bucle while con perturbación flotante aleatoria detectado en '{curr_fn}' de '{tpl_id}'."
                                        if step5_err_fn(err_msg):
                                            return fail_fn(err_msg)
                            if not is_bounded_while(sub):
                                is_const_true = isinstance(sub.test, ast.Constant) and bool(sub.test.value) is True
                                if is_const_true:
                                    line_no = _find_diagnostic_line(curr_loc, curr_fn, orig_idx)
                                    err_msg = (
                                        f"FAIL: [TPL-UNBOUNDED-LOOP] [TPL-DRY] En '{tpl_id}' (Línea {line_no} en {curr_p.name}): "
                                        f"Bucle while constante sin cota iterativa explícita verificable (while True) detectado en '{curr_fn}'. "
                                        f"Use 'for _ in range(N):' o bucles con cota iterativa verificable (ej. 'while tries < 50: tries += 1') para evitar timeouts."
                                    )
                                    if step5_err_fn(err_msg):
                                        return fail_fn(err_msg)
                                else:
                                    print(
                                        f"WARNING: [TPL-UNBOUNDED-LOOP] En '{tpl_id}': Bucle while en '{curr_fn}' sin contador explícito verificado. "
                                        f"Asegúrese de que el bucle converge rápidamente.",
                                        file=sys.stderr,
                                    )
                except Exception:
                    pass

        # Stems validation: require at least 3 distinct author-written stems
        if not isinstance(stems_raw, (list, tuple)) or len(stems_raw) < 3:
            err_msg = (
                f"FAIL: La plantilla '{tpl_id}' debe proporcionar al menos 3 enunciados distintos en stems "
                f"(se recibieron {len(stems_raw) if isinstance(stems_raw, (list, tuple)) else 0})."
            )
            if step5_err_fn(err_msg):
                return fail_fn(err_msg)
            cleaned_stems = [str(s).strip() for s in stems_raw if str(s).strip()] if isinstance(stems_raw, (list, tuple)) else []
        else:
            cleaned_stems = [str(s).strip() for s in stems_raw if str(s).strip()]
            if len(set(cleaned_stems)) < 3:
                err_msg = (
                    f"FAIL: La plantilla '{tpl_id}' contiene enunciados duplicados en stems "
                    f"(se encontraron {len(set(cleaned_stems))} únicos, se requieren >= 3)."
                )
                if step5_err_fn(err_msg):
                    return fail_fn(err_msg)
        stem_es = cleaned_stems[0] if cleaned_stems else ""
        stem_variants = cleaned_stems

        # Strict stem grammar & LaTeX symbol consistency check [TPL-STEM-GRAMMAR]
        if strict and stem_variants:
            for s_idx, sv in enumerate(stem_variants):
                clean_sv = re.sub(r"\$\$[\s\S]*?\$\$", " ", sv)
                clean_sv = re.sub(r"\$[^\$]*?\$", " ", clean_sv)
                clean_for_punct = re.sub(
                    r"\b(?:p\.\s*ej|ej|etc|vs|cap|pág|pag|vol|art|inc)\.",
                    "ABBR",
                    clean_sv,
                    flags=re.IGNORECASE,
                )
                clean_for_punct = re.sub(
                    r"\b(?:i\.i\.d|v\.a|c\.s|p\.p|s\.t|d\.f|a\.s)\.",
                    "ABBR",
                    clean_for_punct,
                )
                m_dot = re.search(r"\.\s+[a-záéíóúñ]", clean_for_punct)
                if m_dot:
                    line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, sv)
                    err_msg = (
                        f"FAIL: [TPL-STEM-GRAMMAR] Error mecánico de puntuación en stem_variants[{s_idx}] de '{tpl_id}' "
                        f"(Línea {line_no} en {curr_p.name}): punto seguido de minúscula ('{m_dot.group(0)}'). "
                        f"Revise la unión o puntuación del enunciado."
                    )
                    if step5_err_fn(err_msg):
                        return fail_fn(err_msg)
                m_comma = re.search(r",\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]{2,}", clean_for_punct)
                if m_comma:
                    line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, sv)
                    err_msg = (
                        f"FAIL: [TPL-STEM-GRAMMAR] Error mecánico de puntuación en stem_variants[{s_idx}] de '{tpl_id}' "
                        f"(Línea {line_no} en {curr_p.name}): coma seguida de mayúscula ('{m_comma.group(0)}'). "
                        f"Revise la unión mecánica o puntuación del enunciado."
                    )
                    if step5_err_fn(err_msg):
                        return fail_fn(err_msg)

            if len(stem_variants) > 1:
                var_sym_sets = []
                for sv in stem_variants:
                    raw_syms = set(re.findall(r"\$([A-Za-z]_[A-Za-z0-9{}]+)\$", sv))
                    norm_syms = {s.replace("{", "").replace("}", "") for s in raw_syms}
                    var_sym_sets.append(norm_syms)
                all_syms = set().union(*var_sym_sets)
                if all_syms:
                    for sym in sorted(all_syms):
                        missing_in = [
                            i for i, sym_set in enumerate(var_sym_sets)
                            if sym not in sym_set and f"@{sym}@" not in stem_variants[i] and f"@{sym.lower()}@" not in stem_variants[i] and sym not in stem_variants[i]
                        ]
                        if missing_in and len(missing_in) < len(stem_variants):
                            line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, stem_variants[missing_in[0]])
                            err_msg = (
                                f"FAIL: [TPL-STEM-GRAMMAR] Inconsistencia de símbolos LaTeX entre stem_variants en '{tpl_id}' "
                                f"(Línea {line_no} en {curr_p.name}): el símbolo '${sym}$' está presente en unas variantes pero ausente en la variante {missing_in[0]} sin parámetro @...@ equivalente."
                            )
                            if step5_err_fn(err_msg):
                                return fail_fn(err_msg)

        # Reject adjacent unseparated placeholders (e.g. '@n@@b@' -> '0.0645') [TPL-ADJACENT-PLACEHOLDERS]
        _adj_placeholder_re = re.compile(r"@[a-zA-Z0-9_]+(?::[^@\s]*)?@@[a-zA-Z0-9_]+(?::[^@\s]*)?@")
        _adj_texts = list(stem_variants or [])
        if sol_raw:
            _adj_texts.append(sol_raw)
        if isinstance(hints_raw, (list, tuple)):
            _adj_texts.extend(str(h) for h in hints_raw if h)
        for _atxt in _adj_texts:
            m_adj = _adj_placeholder_re.search(_atxt)
            if m_adj:
                line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, _atxt)
                err_msg = (
                    f"FAIL: [TPL-ADJACENT-PLACEHOLDERS] Placeholders adyacentes sin operador ni espacio "
                    f"('{m_adj.group(0)}') en '{tpl_id}' (Línea {line_no} en {curr_p.name}). "
                    f"Inserta un operador (ej. '\\cdot', '+', '-') o espacio entre variables."
                )
                if step5_err_fn(err_msg):
                    return fail_fn(err_msg)

        # Reject artificial Frankenstein sums of incompatible units in FIB / MC7 stems
        if interaction_type in ("fill_in_the_blank", "multiple_choice_7_options") and stem_variants:
            for s_idx, sv in enumerate(stem_variants):
                frankenstein_pair = detect_frankenstein_sum(sv)
                if frankenstein_pair:
                    u1, u2 = frankenstein_pair
                    line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, sv)
                    err_msg = (
                        f"FAIL: [TPL-FRANKENSTEIN-SUM] En stem_variants[{s_idx}] de '{tpl_id}' "
                        f"(Línea {line_no} en {curr_p.name}): El enunciado solicita una suma o índice compuesto "
                        f"artificial combinando magnitudes con unidades incompatibles ('{u1}' + '{u2}'). "
                        f"Replantea el reactivo para evaluar una sola magnitud o una suma homogénea."
                    )
                    if step5_err_fn(err_msg):
                        return fail_fn(err_msg)

        # Hints validation: require 3 to 5 author hints, >= 25 chars, no anti-socratic catchphrases, no literal wrong_belief copy
        cta_comp = cta_comp_map.get(cid, {})
        cta_distractors = cta_comp.get("distractors", [])
        if not isinstance(hints_raw, (list, tuple)) or not (3 <= len(hints_raw) <= 5):
            err_msg = (
                f"FAIL: La plantilla '{tpl_id}' debe definir entre 3 y 5 pistas explícitas (hints) "
                f"(se recibieron {len(hints_raw) if isinstance(hints_raw, (list, tuple)) else 0})."
            )
            if step5_err_fn(err_msg):
                return fail_fn(err_msg)

        hints = []
        anti_socratic_patterns = [
            "evita el error",
            "recuerda no confundir",
            "no confundas",
            "cuidado con el error",
            "no cometas el error",
            "error común",
        ]
        cta_wrong_beliefs = [
            str(d.get("wrong_belief") or "").strip().lower()
            for d in cta_distractors if isinstance(d, dict) and d.get("wrong_belief")
        ]
        if isinstance(hints_raw, (list, tuple)):
            for h_idx, h_item in enumerate(hints_raw, start=1):
                h_text = _strip_giveaway_prefix(str(h_item).strip())
                if len(h_text) < 25:
                    err_msg = f"FAIL: La pista {h_idx} de '{tpl_id}' tiene menos de 25 caracteres ({len(h_text)} < 25): '{h_text}'."
                    if step5_err_fn(err_msg):
                        return fail_fn(err_msg)
                h_lower = h_text.lower()
                for pat in anti_socratic_patterns:
                    if pat in h_lower:
                        err_msg = f"FAIL: La pista {h_idx} de '{tpl_id}' contiene una muletilla anti-socrática prohibida ('{pat}'): '{h_text}'."
                        if step5_err_fn(err_msg):
                            return fail_fn(err_msg)
                for wb in cta_wrong_beliefs:
                    if len(wb) >= 12 and wb in h_lower:
                        err_msg = f"FAIL: La pista {h_idx} de '{tpl_id}' copia literalmente la concepción errónea de cta.json ('{wb}')."
                        if step5_err_fn(err_msg):
                            return fail_fn(err_msg)
                hints.append(h_text)

        # Retrieve CTA declared distractor IDs
        clean_cta_distractors = []
        for d in cta_distractors:
            if isinstance(d, dict):
                cd = dict(d)
                for rkey in ("wrong_belief", "omitted_step", "remediation_hint", "manifestation"):
                    if isinstance(cd.get(rkey), str):
                        cd[rkey] = _strip_giveaway_prefix(cd[rkey])
                clean_cta_distractors.append(cd)
            else:
                clean_cta_distractors.append(d)

        cta_declared_ids = {d.get("id") for d in clean_cta_distractors if isinstance(d, dict) and d.get("id")}
        combined_rats = {**module_rats, **tpl_rats}

        # Adapt MC7 generator if applicable
        if interaction_type == "multiple_choice_7_options":
            gen_code = build_adapted_mc7_generator(
                gen_code, cid, clean_cta_distractors, strict=strict, rats_map=combined_rats, fmt=fmt_str
            )

        # Determine declared vars from generator callable (with timeout guard) or sandbox or AST
        sample_res = None
        sample_dict: Dict[str, Any] = {}
        declared_vars: Set[str] = set()
        if callable(gen_raw):
            try:
                from engine.sandbox import call_with_timeout
                sample_res = call_with_timeout(
                    gen_raw,
                    args=(_make_sandbox_rng(42),),
                    timeout=0.4,
                    seed=42,
                )
            except Exception:
                pass

        if sample_res is None and gen_code:
            try:
                from engine.sandbox import run_code_in_env
                sample_res = run_code_in_env(gen_code, "generate", seed=42, timeout=0.5)
            except Exception:
                pass

        if isinstance(sample_res, dict):
            if "ans" in sample_res and "correct" not in sample_res:
                sample_res["correct"] = sample_res["ans"]
            if "ds" in sample_res and "distractors" not in sample_res:
                sample_res["distractors"] = sample_res["ds"]
            if "vars" not in sample_res:
                c_val = sample_res.get("correct") or sample_res.get("ans") or ""
                sample_res["vars"] = {"ans": c_val} if c_val else {}
            if "vars" in sample_res and isinstance(sample_res["vars"], dict):
                declared_vars = set(str(k) for k in sample_res["vars"].keys())
        elif isinstance(sample_res, (tuple, list)) and len(sample_res) >= 1 and isinstance(sample_res[0], dict):
            declared_vars = set(str(k) for k in sample_res[0].keys())

        if not declared_vars and gen_code:
            try:
                _gtree = ast.parse(textwrap.dedent(gen_code.strip()))
                for _gnode in ast.walk(_gtree):
                    if isinstance(_gnode, ast.Dict):
                        for _gk, _gv in zip(_gnode.keys, _gnode.values):
                            if isinstance(_gk, ast.Constant) and _gk.value == "vars":
                                if isinstance(_gv, ast.Dict):
                                    declared_vars.update(
                                        str(k.value) for k in _gv.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)
                                    )
                                elif isinstance(_gv, ast.Name):
                                    _vname = _gv.id
                                    for _anode in ast.walk(_gtree):
                                        if isinstance(_anode, ast.Assign) and isinstance(_anode.value, ast.Dict):
                                            if any(isinstance(t, ast.Name) and t.id == _vname for t in _anode.targets):
                                                declared_vars.update(
                                                    str(k.value) for k in _anode.value.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)
                                                )
            except Exception:
                m_vars = re.search(r"['\"]vars['\"]\s*:\s*\{([^}]+)\}", gen_code)
                if m_vars:
                    var_names = re.findall(r"['\"]([a-zA-Z_][a-zA-Z0-9_]*)['\"]\s*:", m_vars.group(1))
                    declared_vars = set(var_names)

        # Distractor validation, dynamic rationale check, and KaTeX guards on sample_res
        if sample_res is not None and isinstance(sample_res, (dict, tuple, list)):
            if isinstance(sample_res, (tuple, list)):
                if len(sample_res) >= 3:
                    s_vars = sample_res[0] if isinstance(sample_res[0], dict) else {}
                    s_corr = str(sample_res[1])
                    s_dists = sample_res[2] if isinstance(sample_res[2], list) else []
                    sample_dict = {"vars": s_vars, "correct": s_corr, "distractors": s_dists}
                elif len(sample_res) == 2:
                    s_vars = sample_res[0] if isinstance(sample_res[0], dict) else {}
                    s_corr = str(sample_res[1])
                    sample_dict = {"vars": s_vars, "correct": s_corr, "distractors": []}
                else:
                    sample_dict = {}
            else:
                sample_dict = sample_res

            # Apply fmt_str to sample_dict if defined
            if fmt_str and "@X@" in fmt_str and sample_dict.get("correct"):
                c_val_s = str(sample_dict["correct"]).strip()
                sample_dict["correct"] = _format_with_fmt(c_val_s, fmt_str)

            # Parametric indicators for dynamic rationale check
            has_var_in_correct = bool(re.search(r"@([a-zA-Z0-9_]+)@", str(sample_dict.get("correct", ""))))
            has_var_in_stem = bool(re.search(r"@([a-zA-Z0-9_]+)@", stem_es)) or any(bool(re.search(r"@([a-zA-Z0-9_]+)@", s)) for s in stem_variants)

            # FIB & Open Symbolic KaTeX / diagnostic_distractors guard
            if interaction_type in ("fill_in_the_blank", "open_symbolic"):
                raw_corr_obj = sample_dict.get("correct", "")
                if interaction_type == "open_symbolic" and isinstance(raw_corr_obj, dict):
                    corr_str = str(
                        raw_corr_obj.get("expression")
                        or raw_corr_obj.get("value")
                        or raw_corr_obj.get("canonical_algebraic")
                        or ""
                    ).strip()
                else:
                    corr_str = str(raw_corr_obj).strip()
                if corr_str.startswith("$") and corr_str.endswith("$") and len(corr_str) >= 2:
                    line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, corr_str)
                    err_msg = (
                        f"FAIL: [TPL-FIB-KATEX] La respuesta {interaction_type} en '{tpl_id}' ('{corr_str}') (Línea {line_no} en {curr_p.name}) contiene delimitadores '$' externos. "
                        f"En Frontend (FeedbackToast) se formatea automáticamente en modo matemático; retire los '$' externos."
                    )
                    if step5_err_fn(err_msg):
                        return fail_fn(err_msg)
                fib_katex_errs = validate_katex_syntax(corr_str, f"{interaction_type} correct answer in '{tpl_id}'", allow_template_vars=True)
                if fib_katex_errs:
                    line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, corr_str)
                    err_msg = f"FAIL: [TPL-KATEX] En '{tpl_id}' (Línea {line_no} en {curr_p.name}): {fib_katex_errs[0]}"
                    if step5_err_fn(err_msg):
                        return fail_fn(err_msg)

            # Warn-only PyKaTeX render check (does not affect pass/fail)
            _is_fib = interaction_type in ("fill_in_the_blank", "open_symbolic")
            _pykatex_corr = corr_str if _is_fib else sample_dict.get("correct", "")
            for _w in pykatex_warnings(_pykatex_corr, f"correct in '{tpl_id}'", whole_is_math=_is_fib):
                print(_w, file=sys.stderr)
            for _d in (sample_dict.get("distractors") or []):
                _dv = _d.get("value") or _d.get("expression") if isinstance(_d, dict) else (_d[1] if isinstance(_d, (tuple, list)) and len(_d) > 1 else _d)
                for _w in pykatex_warnings(_dv, f"distractor in '{tpl_id}'"):
                    print(_w, file=sys.stderr)

            # Orphan vars check (calibrated warn-only)
            if sample_dict and isinstance(sample_dict.get("vars"), dict):
                raw_vars_keys = set(sample_dict["vars"].keys())
                used_tokens: Set[str] = set()
                for text_field in (stem_variants or []) + [sol_raw] + (hints or []):
                    if text_field:
                        used_tokens.update(re.findall(r"@([a-zA-Z0-9_]+)(?::[^@]*)?@", str(text_field)))
                for opt_item in (sample_dict.get("distractors") or sample_dict.get("options") or []):
                    if isinstance(opt_item, dict):
                        for v_val in opt_item.values():
                            if isinstance(v_val, str):
                                used_tokens.update(re.findall(r"@([a-zA-Z0-9_]+)(?::[^@]*)?@", v_val))
                    elif isinstance(opt_item, (tuple, list)):
                        for v_val in opt_item:
                            if isinstance(v_val, str):
                                used_tokens.update(re.findall(r"@([a-zA-Z0-9_]+)(?::[^@]*)?@", v_val))
                for r_text in (combined_rats or {}).values():
                    if isinstance(r_text, str):
                        used_tokens.update(re.findall(r"@([a-zA-Z0-9_]+)(?::[^@]*)?@", r_text))

                ast_inspected_keys: Set[str] = set()
                if ver_code:
                    try:
                        v_ast = ast.parse(textwrap.dedent(ver_code.strip()))
                        for v_node in ast.walk(v_ast):
                            if isinstance(v_node, ast.Subscript) and isinstance(v_node.slice, ast.Constant) and isinstance(v_node.slice.value, str):
                                ast_inspected_keys.add(v_node.slice.value)
                            elif isinstance(v_node, ast.Call) and isinstance(v_node.func, ast.Attribute) and v_node.func.attr == "get" and v_node.args:
                                if isinstance(v_node.args[0], ast.Constant) and isinstance(v_node.args[0].value, str):
                                    ast_inspected_keys.add(v_node.args[0].value)
                    except Exception:
                        pass

                orphan_keys = raw_vars_keys - used_tokens - ast_inspected_keys - {"ans", "correct", "val"}
                if orphan_keys:
                    print(
                        f"[!] Warning: [TPL-ORPHAN-VARS] En '{tpl_id}': claves retornadas en 'vars' que no se usan en placeholders @...@ ni en ver_fn: {sorted(list(orphan_keys))}",
                        file=sys.stderr,
                    )

            # MC7 and FIB / Open Symbolic diagnostic distractor checks
            if interaction_type in ("multiple_choice_7_options", "fill_in_the_blank", "open_symbolic"):
                is_mc7_tpl = interaction_type == "multiple_choice_7_options"
                if is_mc7_tpl:
                    s_corr_raw = str(sample_dict.get("correct", "")).strip()
                    if s_corr_raw:
                        corr_katex_errs = validate_katex_syntax(s_corr_raw, f"correct answer in '{tpl_id}'", allow_template_vars=True)
                        if corr_katex_errs:
                            line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, s_corr_raw)
                            err_msg = f"FAIL: [TPL-KATEX] En '{tpl_id}' (Línea {line_no} en {curr_p.name}): {corr_katex_errs[0]}"
                            if step5_err_fn(err_msg):
                                return fail_fn(err_msg)
                        if strict:
                            m_tt = _find_telltale_in_option(s_corr_raw, is_distractor=False)
                            if m_tt:
                                line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, s_corr_raw)
                                err_msg = (
                                    f"FAIL: [TPL-TELLTALE / parenthetical_telltale_linter / distractor_integrity_linter] En '{tpl_id}' (Línea {line_no} en {curr_p.name}): "
                                    f"la opción visible contiene metainformación delatora: '{m_tt}'. "
                                    f"Elimina palabras y coletillas delatoras del texto visible de la opción y traslada explicaciones conceptuales a 'error_rationale' o 'sol'."
                                )
                                if step5_err_fn(err_msg):
                                    return fail_fn(err_msg)
                dists_list = sample_dict.get("distractors") or sample_dict.get("ds") or []
                if isinstance(dists_list, list) and dists_list:
                    dids_found = []
                    for d_idx, d_item in enumerate(dists_list, start=1):
                        did = None
                        rat = ""
                        val = ""
                        is_regex_trap = False
                        if isinstance(d_item, dict):
                            did = d_item.get("distractor_id") or d_item.get("id") or d_item.get("did")
                            if isinstance(did, str):
                                did = did.strip().replace("_", "-")
                            rat = str(d_item.get("error_rationale") or d_item.get("rationale") or "")
                            if not rat and did and did in combined_rats:
                                rat = combined_rats[did]
                            val = str(
                                d_item.get("value")
                                if "value" in d_item
                                else (d_item.get("expression") or d_item.get("content") or d_item.get("pattern") or "")
                            )
                            is_regex_trap = (
                                str(d_item.get("match_type") or d_item.get("kind") or "").lower() == "regex"
                                or ("pattern" in d_item and "value" not in d_item and "expression" not in d_item)
                            )
                        elif isinstance(d_item, (tuple, list)):
                            if len(d_item) >= 3:
                                did = str(d_item[0]).strip().replace("_", "-")
                                val = str(d_item[1]).strip()
                                rat = str(d_item[2]).strip()
                            elif len(d_item) == 2:
                                did_cand = str(d_item[0]).strip().replace("_", "-")
                                orig_did0 = str(d_item[0]).strip()
                                if did_cand in combined_rats or orig_did0 in combined_rats:
                                    did = did_cand
                                    val = str(d_item[1]).strip()
                                    rat = combined_rats.get(did_cand) or combined_rats[orig_did0]
                                elif strict:
                                    line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, str(d_item[0]))
                                    err_tag = "[TPL-MC7-STRICT]" if is_mc7_tpl else "[TPL-DIAG-DISTRACTOR]"
                                    err_msg = (
                                        f"FAIL: {err_tag} En modo estricto, la 2-tupla (distractor_id, value) sin entrada en RATS está prohibida en {interaction_type} ('{tpl_id}') (Línea {line_no} en {curr_p.name}). "
                                        f"Cada distractor debe ser una 3-tupla (distractor_id, value, error_rationale) con error_rationale >= 20 caracteres: {repr(d_item)}"
                                    )
                                    if step5_err_fn(err_msg):
                                        return fail_fn(err_msg)
                                    did = did_cand
                                    val = str(d_item[1]).strip()
                                else:
                                    did = did_cand
                                    val = str(d_item[1]).strip()

                        if is_mc7_tpl and fmt_str and "@X@" in fmt_str and val:
                            val = _format_with_fmt(val, fmt_str)

                        if val and not is_regex_trap:
                            val_katex_errs = validate_katex_syntax(val, f"distractor '{did}' value in '{tpl_id}'", allow_template_vars=True)
                            if val_katex_errs:
                                line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, did or val)
                                err_msg = f"FAIL: [TPL-KATEX] En '{tpl_id}' (Línea {line_no} en {curr_p.name}): {val_katex_errs[0]}"
                                if step5_err_fn(err_msg):
                                    return fail_fn(err_msg)
                            if is_mc7_tpl and strict:
                                m_tt = _find_telltale_in_option(val, is_distractor=True)
                                if m_tt:
                                    line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, did or val)
                                    err_msg = (
                                        f"FAIL: [TPL-TELLTALE / parenthetical_telltale_linter / distractor_integrity_linter] En '{tpl_id}' (Línea {line_no} en {curr_p.name}): "
                                        f"la opción visible contiene metainformación delatora: '{m_tt}'. "
                                        f"Elimina palabras y coletillas delatoras del texto visible de la opción y traslada explicaciones conceptuales a 'error_rationale' o 'sol'."
                                    )
                                    if step5_err_fn(err_msg):
                                        return fail_fn(err_msg)
                        if rat:
                            rat_katex_errs = validate_katex_syntax(rat, f"distractor '{did}' rationale in '{tpl_id}'", allow_template_vars=True)
                            if rat_katex_errs:
                                line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, did or rat)
                                err_msg = f"FAIL: [TPL-KATEX] En '{tpl_id}' (Línea {line_no} en {curr_p.name}): {rat_katex_errs[0]}"
                                if step5_err_fn(err_msg):
                                    return fail_fn(err_msg)

                        if did:
                            dids_found.append(did)
                            if cta_declared_ids and did not in cta_declared_ids:
                                line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, did)
                                err_msg = (
                                    f"FAIL: Distractor ID '{did}' en '{tpl_id}' (Línea {line_no} en {curr_p.name}) no está declarado en cta.json para la competencia '{cid}'. "
                                    f"Distractores obligatorios declarados en cta.json: {sorted(cta_declared_ids)}."
                                )
                                if step5_err_fn(err_msg):
                                    return fail_fn(err_msg)

                        if strict:
                            rat_s = rat.strip()
                            norm_rat_s = re.sub(r"@[A-Za-z0-9_]+@", "X", rat_s)
                            if len(rat_s) < 20:
                                line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, did or rat)
                                rat_tag = "[TPL-MC7-RATIONALE]" if is_mc7_tpl else "[TPL-DIAG-RATIONALE]"
                                err_msg = (
                                    f"FAIL: {rat_tag} El distractor '{did}' en '{tpl_id}' (Línea {line_no} en {curr_p.name}) tiene error_rationale de longitud {len(rat_s)} (< 20 caracteres): '{rat}'."
                                )
                                if step5_err_fn(err_msg):
                                    return fail_fn(err_msg)
                            elif len(norm_rat_s) < 50:
                                line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, did or rat)
                                rat_tag = "[TPL-MC7-RATIONALE]" if is_mc7_tpl else "[TPL-DIAG-RATIONALE]"
                                deferred_hints_dup_errors.append(
                                    f"FAIL: {rat_tag} El distractor '{did}' en '{tpl_id}' (Línea {line_no} en {curr_p.name}) tiene error_rationale demasiado corto tras interpolación de @var@ "
                                    f"(raw={len(rat_s)}c, normalizado @var@->X={len(norm_rat_s)}c < 50c): '{rat}'."
                                )
                            # Dynamic rationale check [TPL-DYNAMIC-RATIONALE]
                            if declared_vars:
                                has_var_in_val = bool(re.search(r"@([a-zA-Z0-9_]+)@", val))
                                is_param_dist = has_var_in_val or has_var_in_correct or has_var_in_stem
                                if is_param_dist:
                                    rat_tokens = set(re.findall(r"@([a-zA-Z0-9_]+)@", rat))
                                    valid_rat_tokens = rat_tokens.intersection(declared_vars)
                                    if not valid_rat_tokens:
                                        line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, did or rat)
                                        err_msg = (
                                            f"FAIL: [TPL-DYNAMIC-RATIONALE] El distractor '{did}' en la plantilla paramétrica '{tpl_id}' (Línea {line_no} en {curr_p.name}) tiene una explicación estática sin variables ('{rat}'). "
                                            f"Debe incluir al menos un token @var@ declarado en vars ({', '.join(sorted(declared_vars))}) para explicar dinámicamente el desvío."
                                        )
                                        if step5_err_fn(err_msg):
                                            return fail_fn(err_msg)
                    target_misc = list(dict.fromkeys(dids_found))

            # MS checks
            if interaction_type == "multiple_select":
                opts_list = sample_dict.get("options") or []
                ms_dids = []
                for opt in opts_list:
                    if isinstance(opt, dict) and not opt.get("is_correct"):
                        did = opt.get("distractor_id") or opt.get("id") or opt.get("did")
                        rat = str(opt.get("error_rationale") or opt.get("rationale") or "")
                        val = str(opt.get("value") if "value" in opt else (opt.get("content") or ""))
                        if val:
                            opt_katex_errs = validate_katex_syntax(val, f"option '{did}' value in '{tpl_id}'", allow_template_vars=True)
                            if opt_katex_errs:
                                line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, did or val)
                                err_msg = f"FAIL: [TPL-KATEX] En '{tpl_id}' (Línea {line_no} en {curr_p.name}): {opt_katex_errs[0]}"
                                if step5_err_fn(err_msg):
                                    return fail_fn(err_msg)
                            if strict:
                                m_tt = _find_telltale_in_option(val, is_distractor=True)
                                if m_tt:
                                    line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, did or val)
                                    err_msg = (
                                        f"FAIL: [TPL-TELLTALE / parenthetical_telltale_linter / distractor_integrity_linter] En '{tpl_id}' (Línea {line_no} en {curr_p.name}): "
                                        f"la opción visible contiene metainformación delatora: '{m_tt}'. "
                                        f"Elimina palabras y coletillas delatoras del texto visible de la opción y traslada explicaciones conceptuales a 'error_rationale' o 'sol'."
                                    )
                                    if step5_err_fn(err_msg):
                                        return fail_fn(err_msg)
                        if rat:
                            opt_rat_errs = validate_katex_syntax(rat, f"option '{did}' rationale in '{tpl_id}'", allow_template_vars=True)
                            if opt_rat_errs:
                                line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, did or rat)
                                err_msg = f"FAIL: [TPL-KATEX] En '{tpl_id}' (Línea {line_no} en {curr_p.name}): {opt_rat_errs[0]}"
                                if step5_err_fn(err_msg):
                                    return fail_fn(err_msg)
                        if did:
                            norm_did = str(did).replace("_", "-")
                            ms_dids.append(norm_did)
                            if cta_declared_ids and norm_did not in cta_declared_ids:
                                line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, str(did))
                                err_msg = (
                                    f"FAIL: Distractor ID '{did}' en opción falsa de '{tpl_id}' (Línea {line_no} en {curr_p.name}) no está declarado en cta.json para la competencia '{cid}'."
                                )
                                if step5_err_fn(err_msg):
                                    return fail_fn(err_msg)
                        if strict:
                            if not did:
                                line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, val)
                                err_msg = f"FAIL: [TPL-MS-DISTRACTOR-ID] Opción falsa en multiple_select ('{tpl_id}') (Línea {line_no} en {curr_p.name}) carece de distractor_id."
                                if step5_err_fn(err_msg):
                                    return fail_fn(err_msg)
                            rat_s = rat.strip()
                            norm_rat_s = re.sub(r"@[A-Za-z0-9_]+@", "X", rat_s)
                            if len(rat_s) < 20:
                                line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, did or rat)
                                err_msg = (
                                    f"FAIL: [TPL-MS-RATIONALE] La opción falsa '{did}' en '{tpl_id}' (Línea {line_no} en {curr_p.name}) tiene error_rationale de longitud {len(rat_s)} (< 20 caracteres): '{rat}'."
                                )
                                if step5_err_fn(err_msg):
                                    return fail_fn(err_msg)
                            elif len(norm_rat_s) < 50:
                                line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, did or rat)
                                deferred_hints_dup_errors.append(
                                    f"FAIL: [TPL-MS-RATIONALE] La opción falsa '{did}' en '{tpl_id}' (Línea {line_no} en {curr_p.name}) tiene error_rationale demasiado corto tras interpolación de @var@ "
                                    f"(raw={len(rat_s)}c, normalizado @var@->X={len(norm_rat_s)}c < 50c): '{rat}'."
                                )
                            # Dynamic rationale check [TPL-DYNAMIC-RATIONALE]
                            if declared_vars:
                                has_var_in_val = bool(re.search(r"@([a-zA-Z0-9_]+)@", val))
                                is_param_opt = has_var_in_val or has_var_in_correct or has_var_in_stem
                                if is_param_opt:
                                    rat_tokens = set(re.findall(r"@([a-zA-Z0-9_]+)@", rat))
                                    valid_rat_tokens = rat_tokens.intersection(declared_vars)
                                    if not valid_rat_tokens:
                                        line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, did or rat)
                                        err_msg = (
                                            f"FAIL: [TPL-DYNAMIC-RATIONALE] La opción falsa '{did}' en la plantilla paramétrica '{tpl_id}' (Línea {line_no} en {curr_p.name}) tiene una explicación estática sin variables ('{rat}'). "
                                            f"Debe incluir al menos un token @var@ declarado en vars ({', '.join(sorted(declared_vars))})."
                                        )
                                        if step5_err_fn(err_msg):
                                            return fail_fn(err_msg)
                target_misc = list(dict.fromkeys(ms_dids))

            # Bloom Superior structured modalities (Shift-Left structural check + distractor_ids extraction)
            if interaction_type in STRUCTURED_M20_TYPES:
                sample_vars = sample_dict.get("vars") if isinstance(sample_dict.get("vars"), dict) else {}
                cta_dmap = {d["id"]: d for d in clean_cta_distractors if isinstance(d, dict) and d.get("id")}
                compiled_m20: Optional[Dict[str, Any]] = None
                try:
                    if interaction_type == "proof_dag":
                        from engine.proof_compiler import compile_and_verify_proof_dag
                        raw_p = sample_dict.get("proof_dag") or sample_dict.get("dag") or (t.get("proof_dag") if is_form_c else None)
                        compiled_m20, _ = compile_and_verify_proof_dag(
                            raw_p,
                            variables=sample_vars,
                            cta_distractors_map=cta_dmap,
                            rng=_make_sandbox_rng(42),
                            rats_map=combined_rats,
                        )
                    elif interaction_type == "adversarial_break":
                        from engine.adversarial_generator import compile_and_verify_adversarial
                        raw_p = sample_dict.get("adversarial_break") or sample_dict.get("adversarial") or (t.get("adversarial_break") if is_form_c else None)
                        compiled_m20, _ = compile_and_verify_adversarial(
                            raw_p,
                            variables=sample_vars,
                            cta_distractors_map=cta_dmap,
                            rng=_make_sandbox_rng(42),
                            rats_map=combined_rats,
                        )
                    elif interaction_type == "unstructured_model":
                        from engine.assemble import _assemble_unstructured_model
                        raw_p = sample_dict.get("unstructured_model") or sample_dict.get("stage0") or (t.get("unstructured_model") if is_form_c else None)
                        compiled_m20, _ = _assemble_unstructured_model(
                            raw_p,
                            variables=sample_vars,
                            cta_distractors_map=cta_dmap,
                            rng=_make_sandbox_rng(42),
                            rats_map=combined_rats,
                        )
                    elif interaction_type == "invariant_canvas":
                        from engine.assemble import _assemble_invariant_canvas
                        raw_p = sample_dict.get("invariant_canvas") or sample_dict.get("canvas") or (t.get("invariant_canvas") if is_form_c else None)
                        compiled_m20, _ = _assemble_invariant_canvas(
                            raw_p,
                            variables=sample_vars,
                            cta_distractors_map=cta_dmap,
                            rats_map=combined_rats,
                        )
                    elif interaction_type == "concept_matching":
                        from engine.assemble import _assemble_concept_matching
                        raw_p = sample_dict.get("concept_matching") or sample_dict.get("matching") or (t.get("concept_matching") if is_form_c else None)
                        compiled_m20, _ = _assemble_concept_matching(
                            raw_p,
                            variables=sample_vars,
                            cta_distractors_map=cta_dmap,
                            rng=_make_sandbox_rng(42),
                            rats_map=combined_rats,
                        )
                except ValueError as m20_err:
                    line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx)
                    err_tag = {
                        "proof_dag": "TPL-M20-PROOF-DAG",
                        "adversarial_break": "TPL-M20-ADVERSARIAL",
                        "unstructured_model": "TPL-M20-UNSTRUCTURED-MODEL",
                        "invariant_canvas": "TPL-M20-INVARIANT-CANVAS",
                        "concept_matching": "TPL-M20-CONCEPT-MATCHING",
                    }[interaction_type]
                    err_msg = f"FAIL: [{err_tag}] En '{tpl_id}' (Línea {line_no} en {curr_p.name}): {m20_err}"
                    if step5_err_fn(err_msg):
                        return fail_fn(err_msg)

                if compiled_m20 is not None:
                    m20_dids = _extract_m20_structured_dids(interaction_type, compiled_m20)
                    for norm_did in m20_dids:
                        if cta_declared_ids and norm_did not in cta_declared_ids:
                            line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, norm_did)
                            err_msg = (
                                f"FAIL: Distractor ID '{norm_did}' en {interaction_type} de '{tpl_id}' (Línea {line_no} en {curr_p.name}) no está declarado en cta.json para la competencia '{cid}'."
                            )
                            if step5_err_fn(err_msg):
                                return fail_fn(err_msg)
                    target_misc = m20_dids

        # Soundness and Distractor Refutation Dry-Run (seeds 42, 43, 44)
        if callable(gen_raw) and callable(ver_raw) and strict:
            import random
            tautology_recorded = False
            for test_seed in (42, 43, 44):
                try:
                    rng_test = _make_sandbox_rng(test_seed)
                    EvaluationContext.set(template_id=tpl_id, gen_fn=gen_fn_name, archetype=orig_idx, seed=test_seed)
                    from engine.sandbox import call_with_timeout
                    res_test = call_with_timeout(gen_raw, args=(rng_test,), timeout=0.8, seed=test_seed)
                except Exception:
                    continue
                if not isinstance(res_test, dict):
                    continue
                if "ans" in res_test and "correct" not in res_test:
                    res_test["correct"] = res_test["ans"]
                if "ds" in res_test and "distractors" not in res_test:
                    res_test["distractors"] = res_test["ds"]
                if "vars" not in res_test:
                    c_val = res_test.get("correct") or res_test.get("ans") or ""
                    res_test["vars"] = {"ans": c_val} if c_val else {}
                raw_c_test = res_test.get("correct")
                if isinstance(raw_c_test, dict) and interaction_type == "open_symbolic":
                    c_test = str(
                        raw_c_test.get("expression")
                        or raw_c_test.get("value")
                        or raw_c_test.get("canonical_algebraic")
                        or ""
                    ).strip()
                elif isinstance(raw_c_test, (dict, list)):
                    c_test = ""
                else:
                    c_test = str(raw_c_test or "").strip()
                v_test = res_test.get("vars", {}) if isinstance(res_test.get("vars"), dict) else {}
                if fmt_str and "@X@" in fmt_str and c_test and not isinstance(raw_c_test, dict):
                    c_test = _format_with_fmt(c_test, fmt_str)
                    res_test["correct"] = c_test

                # Soundness check
                is_instance_verifier = (
                    (not c_test and isinstance(res_test.get("options"), list))
                    or (interaction_type in STRUCTURED_M20_TYPES)
                )
                if callable(ver_raw) and is_instance_verifier:
                    # Multiple Select & structured M20 modalities: el verificador recibe la instancia completa.
                    try:
                        from engine.sandbox import call_with_timeout
                        sound_res = call_with_timeout(ver_raw, args=(res_test,), timeout=0.8, seed=test_seed)
                    except TypeError:
                        sound_res = run_ver(c_test, v_test, res_test)
                else:
                    sound_res = run_ver(c_test, v_test, res_test)
                if hasattr(sound_res, "item"):
                    sound_res = sound_res.item()
                if sound_res is not True:
                    line_no = _find_diagnostic_line(curr_loc, ver_fn_name, orig_idx)
                    err_msg = (
                        f"FAIL: [TPL-VERIFIER-UNSOUND] El verificador ver_fn '{ver_fn_name}' en '{tpl_id}' (Línea {line_no} en {curr_p.name}) "
                        f"no retornó True para la instancia válida generada (semilla {test_seed}, resultado: {sound_res})."
                    )
                    if step5_err_fn(err_msg):
                        return fail_fn(err_msg)
                    break

                # Distractor refutation (scalar MC7 / FIB / non-regex open_symbolic)
                dists_test = res_test.get("distractors") or []
                if (
                    interaction_type in ("multiple_choice_7_options", "fill_in_the_blank", "open_symbolic")
                    and isinstance(dists_test, list)
                    and not tautology_recorded
                ):
                    for d_t in dists_test:
                        d_val = ""
                        is_regex_trap = False
                        if isinstance(d_t, dict):
                            is_regex_trap = (
                                str(d_t.get("match_type") or d_t.get("kind") or "").lower() == "regex"
                                or ("pattern" in d_t and "value" not in d_t and "expression" not in d_t)
                            )
                            d_val = str(
                                d_t.get("value")
                                if "value" in d_t
                                else (d_t.get("expression") or d_t.get("content", ""))
                            ).strip()
                        elif isinstance(d_t, (tuple, list)) and len(d_t) >= 2:
                            d_val = str(d_t[1]).strip()
                        elif isinstance(d_t, (tuple, list)) and len(d_t) == 1:
                            d_val = str(d_t[0]).strip()
                        elif isinstance(d_t, (str, int, float)):
                            d_val = str(d_t).strip()
                        if is_regex_trap:
                            continue
                        if fmt_str and "@X@" in fmt_str and d_val:
                            d_val = _format_with_fmt(d_val, fmt_str)
                        if d_val and d_val != c_test:
                            mutated = {**res_test, "correct": d_val}
                            refute_res = run_ver(d_val, v_test, mutated)
                            if hasattr(refute_res, "item"):
                                refute_res = refute_res.item()
                            if refute_res is True:
                                line_no = _find_diagnostic_line(curr_loc, ver_fn_name, orig_idx, d_val)
                                deferred_verifier_errors.append(
                                    f"[-] [VERIFIER-TAUTOLOGY-DETECTED] {cid}.json ({curr_p.name}): El verificador ver_fn '{ver_fn_name}' en '{tpl_id}' (Línea {line_no} en {curr_p.name}) "
                                    f"retornó True para el distractor falso '{d_val}'. El verificador no refuta respuestas incorrectas (tautología)."
                                )
                                tautology_recorded = True
                                break

                # Multiple Select adversarial verification
                is_ms = (interaction_type == "multiple_select") or (isinstance(res_test.get("options"), list) and not res_test.get("distractors"))
                if is_ms and isinstance(res_test.get("options"), list) and not tautology_recorded:
                    opts_t = res_test.get("options") or []
                    t_indices = [i for i, o in enumerate(opts_t) if isinstance(o, dict) and o.get("is_correct") is True]
                    f_indices = [i for i, o in enumerate(opts_t) if isinstance(o, dict) and o.get("is_correct") is False]
                    if t_indices and f_indices:
                        import copy
                        def _call_ms_ver(cand_res):
                            try:
                                from engine.sandbox import call_with_timeout
                                r_res = call_with_timeout(ver_raw, args=(cand_res,), timeout=0.8, seed=test_seed)
                            except TypeError:
                                r_res = run_ver("", cand_res.get("vars", {}), cand_res)
                            except Exception:
                                r_res = False
                            if hasattr(r_res, "item"):
                                r_res = r_res.item()
                            return r_res is True

                        # a) Invert is_correct between one True and one False option
                        mut_a = copy.deepcopy(res_test)
                        mut_a["options"][t_indices[0]]["is_correct"] = False
                        mut_a["options"][f_indices[0]]["is_correct"] = True
                        pass_a = _call_ms_ver(mut_a)

                        # b) Corrupt distractor_id
                        pass_b = None
                        did_idx = next((i for i in f_indices if opts_t[i].get("distractor_id")), None)
                        if did_idx is not None:
                            mut_b = copy.deepcopy(res_test)
                            mut_b["options"][did_idx]["distractor_id"] = "__INVALID_DID__"
                            pass_b = _call_ms_ver(mut_b)

                        # c1) Empty error_rationale (and Form-C alias rationale) in false option only
                        mut_c1 = copy.deepcopy(res_test)
                        mut_c1["options"][f_indices[0]]["error_rationale"] = ""
                        if "rationale" in mut_c1["options"][f_indices[0]]:
                            mut_c1["options"][f_indices[0]]["rationale"] = ""
                        pass_c1 = _call_ms_ver(mut_c1)

                        # c2) Mutate value/content to sentinel in true option only
                        mut_c2 = copy.deepcopy(res_test)
                        mut_c2["options"][t_indices[0]]["value"] = "__MUTATED__"
                        if "content" in mut_c2["options"][t_indices[0]]:
                            mut_c2["options"][t_indices[0]]["content"] = "__MUTATED__"
                        pass_c2 = _call_ms_ver(mut_c2)

                        # c3) Mutate value/content to syntactically valid but false LaTeX assertion in true option only
                        false_latex = "$1 = 2$" if str(opts_t[t_indices[0]].get("value", "")).strip() == "$0 = 1$" else "$0 = 1$"
                        mut_c3 = copy.deepcopy(res_test)
                        mut_c3["options"][t_indices[0]]["value"] = false_latex
                        if "content" in mut_c3["options"][t_indices[0]]:
                            mut_c3["options"][t_indices[0]]["content"] = false_latex
                        pass_c3 = _call_ms_ver(mut_c3)

                        is_taut = (
                            (pass_a is True)
                            or (pass_b is True)
                            or (pass_c1 is True)
                            or (pass_c2 is True)
                            or (pass_c3 is True)
                        )
                        if is_taut:
                            line_no = _find_diagnostic_line(curr_loc, ver_fn_name, orig_idx)
                            deferred_verifier_errors.append(
                                f"[-] [VERIFIER-TAUTOLOGY-DETECTED] {cid}.json ({curr_p.name}): El verificador ver_fn '{ver_fn_name}' en '{tpl_id}' (Línea {line_no} en {curr_p.name}) "
                                f"retornó True para mutaciones adversariales de multiple_select (inversión de is_correct / opciones mutadas). El verificador no refuta respuestas incorrectas (tautología)."
                            )
                            tautology_recorded = True
                            break
            EvaluationContext.reset(norm_shard_id)

        # Vacuous quantifier check in stem_variants
        if strict:
            vacuous_re = re.compile(r"(?:\\forall|\bpara\s+todo\b)\s*\\?[a-zA-Z_]+\s*=\s*\d+|(?:\\exists|\bexiste\b)\s*\\?[a-zA-Z_]+\s*=\s*\d+", re.IGNORECASE)
            for s_idx, sv in enumerate(stem_variants):
                m_vac = vacuous_re.search(sv)
                if m_vac:
                    line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, sv)
                    err_msg = (
                        f"FAIL: [TPL-VACUOUS-QUANTIFIER] Cuantificador vacuo detectado en stem_variants[{s_idx}] de '{tpl_id}' (Línea {line_no} en {curr_p.name}): '{m_vac.group(0)}'. "
                        f"No se permite asignar un valor literal constante a una variable cuantificada."
                    )
                    if step5_err_fn(err_msg):
                        return fail_fn(err_msg)

            if interaction_type in ("fill_in_the_blank", "multiple_choice_7_options"):
                for h_idx, h_val in enumerate(hints):
                    if "@ans@" in str(h_val):
                        line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, str(h_val))
                        err_msg = (
                            f"FAIL: [TPL-HINT-LEAK] La pista {h_idx + 1} de '{tpl_id}' (Línea {line_no} en {curr_p.name}) contiene el token '@ans@'. "
                            f"Las pistas deben ser de andamiaje socrático y no referenciar la respuesta final."
                        )
                        if step5_err_fn(err_msg):
                            return fail_fn(err_msg)

            if sample_dict and sample_dict.get("correct"):
                corr_val_str = str(sample_dict["correct"]).replace("$", "").strip()
                if len(corr_val_str) >= 15 and corr_val_str.lower() not in ("remember", "understand", "apply"):
                    for h_idx, h_val in enumerate(hints):
                        if corr_val_str.lower() in str(h_val).lower():
                            line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, str(h_val))
                            err_msg = (
                                f"FAIL: [TPL-HINT-LEAK] La pista {h_idx + 1} de '{tpl_id}' (Línea {line_no} en {curr_p.name}) filtra la respuesta correcta ('{corr_val_str}'). "
                                f"Las pistas deben ser de andamiaje socrático y no revelar la respuesta final."
                            )
                            if step5_err_fn(err_msg):
                                return fail_fn(err_msg)

        # Normalize non-variable double curly braces {{token}} -> {token} before R-20 validation
        stem_es = normalize_double_braces(stem_es, declared_vars)
        stem_variants = [normalize_double_braces(sv, declared_vars) for sv in stem_variants]
        hints = [normalize_double_braces(h, declared_vars) for h in hints]
        healed_solution = normalize_double_braces(sol_raw, declared_vars)
        healed_solution = re.sub(
            r"\{\{([A-Za-z0-9_]+)\}\}",
            lambda m: f"{{{m.group(1)}}}" if m.group(1) not in declared_vars else m.group(0),
            healed_solution,
        )

        for s_idx, sv in enumerate(stem_variants):
            sv_katex = validate_katex_syntax(sv, f"stem_variant[{s_idx}] in '{tpl_id}'", allow_template_vars=True)
            if sv_katex:
                line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, sv)
                err_msg = f"FAIL: [TPL-KATEX] En '{tpl_id}' (Línea {line_no} en {curr_p.name}): {sv_katex[0]}"
                if step5_err_fn(err_msg):
                    return fail_fn(err_msg)
        for h_idx, h_text in enumerate(hints):
            h_katex = validate_katex_syntax(h_text, f"hint[{h_idx}] in '{tpl_id}'", allow_template_vars=True)
            if h_katex:
                line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, h_text)
                err_msg = f"FAIL: [TPL-KATEX] En '{tpl_id}' (Línea {line_no} en {curr_p.name}): {h_katex[0]}"
                if step5_err_fn(err_msg):
                    return fail_fn(err_msg)
        sol_katex = validate_katex_syntax(healed_solution, f"explanation_es in '{tpl_id}'", allow_template_vars=True)
        if sol_katex:
            line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, sol_raw)
            err_msg = f"FAIL: [TPL-KATEX] En '{tpl_id}' (Línea {line_no} en {curr_p.name}): {sol_katex[0]}"
            if step5_err_fn(err_msg):
                return fail_fn(err_msg)

        if 0 < len(sol_raw.strip()) < 60:
            if strict:
                line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, sol_raw)
                deferred_hints_dup_errors.append(
                    f"FAIL: [TPL-EXP-SHORT] En '{tpl_id}' (Línea {line_no} en {curr_p.name}): sol / explanation_es ('{sol_raw.strip()[:30]}...') "
                    f"tiene {len(sol_raw.strip())} caracteres (< 60 chars requeridos en --strict)."
                )
            else:
                print(
                    f"WARNING: [TPL-EXP-SHORT] En '{tpl_id}': sol / explanation_es ('{sol_raw.strip()[:30]}...') tiene {len(sol_raw.strip())} caracteres (< 60 chars).",
                    file=sys.stderr,
                )


        canonical_dict: Dict[str, Any] = {
            "template_id": tpl_id,
            "competency_id": cid,
            "gen_fn_name": gen_fn_name,
            "question_type": qtype,
            "stem_es": stem_es,
            "stem_variants": stem_variants,
            "generator_code": gen_code,
            "verifier_code": ver_code,
            "explanation_es": healed_solution,
            "target_kc": target_kc,
            "target_misconceptions": target_misc,
            "source_reference": src_ref,
            # Schema compatibility fields
            "id": tpl_id,
            "interaction_type": interaction_type,
            "difficulty": difficulty,
            "bloom": bloom,
            "stem": stem_es,
            "generate_py": gen_code,
            "cross_check_py": ver_code,
            "solution": healed_solution,
            "distractor_ids": target_misc,
            "hints": hints,
            "source_file": curr_p.name,
        }
        if archetype:
            canonical_dict["archetype"] = archetype
        if assumption_id:
            canonical_dict["assumption_id"] = assumption_id
        _has_scalar_ds = interaction_type in ("fill_in_the_blank", "open_symbolic") and bool(
            sample_dict.get("distractors") or sample_dict.get("ds")
        )
        if combined_rats and (interaction_type in STRUCTURED_M20_TYPES or _has_scalar_ds):
            canonical_dict["rats"] = combined_rats
        if is_form_c and isinstance(t.get("symbolic_config"), dict):
            canonical_dict["symbolic_config"] = t["symbolic_config"]

        # Apply mechanical auto-healing
        auto_heal_template_data(canonical_dict, cta_comp=cta_comp)
        canonical_dict = heal_control_chars_in_obj(canonical_dict)

        templates_by_cid.setdefault(cid, []).append(canonical_dict)
        gen_callables_by_cid.setdefault(cid, []).append(gen_raw)


    return None


def evaluate_m3_and_m20_archetype_gates(
    expected_cids: List[str],
    templates_by_cid: Dict[str, List[Dict[str, Any]]],
    gen_callables_by_cid: Dict[str, List[Any]],
    cta_comp_map: Dict[str, Dict[str, Any]],
    cta_contract_version: int,
    shard_entry: Dict[str, Any],
    shard_data_path: Optional[Path],
    fix_files_by_cid: Dict[str, Path],
    locator: Any,
    healed_source: str,
    raw_source: str,
    strict: bool,
    seeds: int,
    norm_shard_id: str,
    fail_total: bool,
    eff_k: int,
    eff_min_arch: int,
) -> List[str]:
    """Enforce [M3-ARCHETYPES], M20 active/MC7 quotas, anti-clone, and stem diversity gates."""
    # Milestone 3 Tri-Band Multimodal Enforcement Gate [M3-ARCHETYPES]
    m3_errors: List[str] = []
    if strict:
        target_cids = expected_cids if expected_cids else list(templates_by_cid.keys())
        shard_data_name = shard_data_path.name if shard_data_path else f"{norm_shard_id}_data.py"

        def _fn_declares_arch(fn_node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> bool:
            all_args = getattr(fn_node.args, "posonlyargs", []) + fn_node.args.args + getattr(fn_node.args, "kwonlyargs", [])
            return any(a.arg == "arch" for a in all_args)

        def _fn_uses_arch_in_body(fn_node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> bool:
            for b_stmt in fn_node.body:
                for sub in ast.walk(b_stmt):
                    if isinstance(sub, ast.Name) and sub.id == "arch" and isinstance(sub.ctx, ast.Load):
                        # Filter out dummy loads like _ = arch or dummy = arch or unused = arch
                        if isinstance(b_stmt, ast.Assign):
                            if any(isinstance(tgt, ast.Name) and tgt.id in ("_", "dummy", "unused") for tgt in b_stmt.targets):
                                continue
                        # Filter out bare statement expressions like `arch` or `arch == arch`
                        if isinstance(b_stmt, ast.Expr):
                            if isinstance(b_stmt.value, ast.Name) and b_stmt.value.id == "arch":
                                continue
                            if isinstance(b_stmt.value, ast.Compare):
                                if isinstance(b_stmt.value.left, ast.Name) and b_stmt.value.left.id == "arch":
                                    if any(isinstance(comp, ast.Name) and comp.id == "arch" for comp in b_stmt.value.comparators):
                                        continue
                        return True
            return False

        for cid in target_cids:
            tpls = templates_by_cid.get(cid, [])
            gen_callables = gen_callables_by_cid.get(cid, [])
            is_modular_fix = bool(cid in fix_files_by_cid and fix_files_by_cid[cid].is_file())
            source_name = fix_files_by_cid[cid].name if is_modular_fix else shard_data_name

            # AST analysis de la fuente efectiva de esta competencia
            cid_sources: List[str] = []
            if is_modular_fix:
                try:
                    _, _healed_fix_ast = heal_shard_source_text(fix_files_by_cid[cid].read_text(encoding="utf-8"))
                    cid_sources.append(_healed_fix_ast)
                except Exception:
                    pass
            else:
                if healed_source:
                    cid_sources.append(healed_source)
                elif raw_source:
                    cid_sources.append(raw_source)
                elif shard_data_path and shard_data_path.is_file():
                    try:
                        cid_sources.append(shard_data_path.read_text(encoding="utf-8"))
                    except Exception:
                        pass

            for t in tpls:
                gen_c = t.get("generator_code") or t.get("generate_py") or ""
                if gen_c and gen_c not in cid_sources:
                    cid_sources.append(gen_c)

            cid_ast_funcs: Dict[str, Union[ast.FunctionDef, ast.AsyncFunctionDef]] = {}
            for src_txt in cid_sources:
                try:
                    parsed_tree = ast.parse(textwrap.dedent(src_txt.strip()))
                    for ast_node in ast.walk(parsed_tree):
                        if isinstance(ast_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            cid_ast_funcs[ast_node.name] = ast_node
                        elif (
                            isinstance(ast_node, ast.Assign)
                            and len(ast_node.targets) == 1
                            and isinstance(ast_node.targets[0], ast.Name)
                            and isinstance(ast_node.value, ast.Lambda)
                        ):
                            fn_id = ast_node.targets[0].id
                            synthetic_fn = ast.FunctionDef(
                                name=fn_id,
                                args=ast_node.value.args,
                                body=[ast.Return(value=ast_node.value.body)],
                                decorator_list=[],
                                returns=None,
                                lineno=getattr(ast_node, "lineno", 1),
                            )
                            cid_ast_funcs[fn_id] = synthetic_fn
                except Exception:
                    pass

            # Assumption link and 4 archetype kinds validation
            has_cta_truth = cid in cta_comp_map
            cta_comp_raw = cta_comp_map.get(cid, {})
            assumptions_list = cta_comp_raw.get("assumptions") or []
            decl_assump_ids = {
                (a.get("id") if isinstance(a, dict) else str(a)).strip()
                for a in assumptions_list
                if (a.get("id") if isinstance(a, dict) else a)
            }
            if has_cta_truth:
                for et in tpls:
                    raw_aid = et.get("assumption_id")
                    if raw_aid is not None and str(raw_aid).strip() != "":
                        a_id = str(raw_aid).strip()
                        if a_id not in decl_assump_ids:
                            m3_errors.append(
                                f"{cid}.json ({source_name}): [TPL-ASSUMPTION-LINK] La plantilla '{et.get('id')}' en la competencia '{cid}' "
                                f"declara assumption_id='{a_id}', pero no existe en los supuestos declarados en cta.json ({sorted(list(decl_assump_ids))})."
                            )

            if assumptions_list and eff_min_arch >= 4:
                tpl_archs = [t.get("archetype") for t in tpls if t.get("archetype")]
                if len(tpl_archs) >= 4 or any(t.get("archetype") for t in tpls):
                    missing_archs = set(_S4_ARCHETYPE_KINDS) - set(tpl_archs)
                    if missing_archs:
                        m3_errors.append(
                            f"{cid}.json ({source_name}): [M3-ARCHETYPES] La competencia '{cid}' declara supuestos en cta.json pero sus plantillas no cubren todos los arquetipos requeridos ({_S4_ARCHETYPE_KINDS}). Faltan: {sorted(list(missing_archs))}."
                        )
                    edge_tpls = [t for t in tpls if t.get("archetype") == "boundary_or_edge_case"]
                    if edge_tpls:
                        for et in edge_tpls:
                            a_id = et.get("assumption_id")
                            if not a_id or a_id not in decl_assump_ids:
                                m3_errors.append(
                                    f"{cid}.json ({source_name}): [TPL-ASSUMPTION-LINK] La plantilla de borde '{et.get('id')}' en la competencia '{cid}' "
                                    f"debe vincularse a un assumption_id válido declarado en cta.json ({sorted(list(decl_assump_ids))}). Encontrado: '{a_id}'."
                                )

            if eff_min_arch >= 3 and len(tpls) < eff_min_arch:
                m3_errors.append(
                    f"{cid}.json ({source_name}): [M3-ARCHETYPES] La competencia '{cid}' define solo {len(tpls)} plantilla(s) en TEMPLATES, "
                    f"pero el contrato Tri-Banda exige mínimo {eff_min_arch} plantillas/arquetipos por competencia."
                )
            if eff_min_arch >= 3 and (fail_total or len(tpls) >= eff_min_arch):
                # Verificación Tri-Banda de dificultad
                diffs = {t.get("difficulty") for t in tpls}
                if not {"easy", "medium", "hard"}.issubset(diffs):
                    missing_diffs = sorted(list({"easy", "medium", "hard"} - diffs))
                    m3_errors.append(
                        f"{cid}.json ({source_name}): [M3-ARCHETYPES] Cobertura incompleta de bandas de dificultad para '{cid}'. "
                        f"Se requieren las 3 bandas {{'easy', 'medium', 'hard'}}, faltan: {missing_diffs}."
                    )

                # Verificación de diversidad de Bloom (>= 2 distintos)
                blooms = {t.get("bloom") for t in tpls if t.get("bloom")}
                if len(blooms) < 2:
                    m3_errors.append(
                        f"{cid}.json ({source_name}): [M3-ARCHETYPES] Diversidad cognitiva insuficiente para '{cid}'. "
                        f"Se requieren al menos 2 niveles Bloom distintos por competencia (encontrados: {sorted(list(blooms))})."
                    )

                # Verificación de práctica activa (FIB o MS)
                cta_c = cta_comp_map.get(cid, {})
                c_type = str(cta_c.get("type", "")).lower()
                is_skill = cid.startswith("Hab-") or c_type in ("skill", "habilidad")
                if is_skill:
                    low_tpls = [
                        f"{t.get('id') or t.get('tpl_id') or '?'}={t.get('bloom')}"
                        for t in tpls
                        if t.get("bloom") in ("Remember", "Understand")
                    ]
                    if low_tpls:
                        m3_errors.append(
                            f"{cid}.json ({source_name}): [M3-SKILL-BLOOM] Habilidad '{cid}' tiene plantillas "
                            f"con Bloom bajo ({', '.join(low_tpls)}). Toda plantilla de una Skill debe ser "
                            f"Apply/Analyze/Evaluate/Create: reetiqueta el Bloom si el ítem ya exige "
                            f"calcular/aplicar, o reescribe el ítem; si es puramente conceptual, muévelo a una "
                            f"competencia Concept."
                        )

                # CTA-Architect-driven modality plan enforcement (2 <= M <= 4 mandatory in v2, >= eff_k per active modality, [M20-MC7-CAP] & [M20-ACTIVE-QUOTA])
                raw_rec_mods = cta_c.get("recommended_modalities")
                allowed_mods_list: List[str] = []
                if isinstance(raw_rec_mods, list):
                    for rm in raw_rec_mods:
                        rm_norm = _QTYPE_TO_INTERACTION.get(
                            str(rm).strip().lower(),
                            str(rm).strip().lower(),
                        )
                        if rm_norm and rm_norm not in allowed_mods_list:
                            allowed_mods_list.append(rm_norm)

                actual_mods_seq = [
                    _QTYPE_TO_INTERACTION.get(
                        str(t.get("interaction_type") or t.get("question_type") or "").strip().lower(),
                        str(t.get("interaction_type") or t.get("question_type") or "").strip().lower(),
                    )
                    for t in tpls
                ]

                # [M20-MC7-CAP]: 0 MC7 in Skill competencies; <= 1 MC7 in Concept/Fact/Prerequisite competencies
                mc7_count = sum(1 for m in actual_mods_seq if m == "multiple_choice_7_options")
                if is_skill and "multiple_choice_7_options" in allowed_mods_list:
                    m3_errors.append(
                        f"{cid}.json ({source_name}): [M20-MC7-CAP] Competencia de habilidad '{cid}' incluye "
                        f"'multiple_choice_7_options' en cta.json['recommended_modalities'], pero MC7 está prohibido "
                        f"en competencias Skill (máximo 0 MC7 permitido)."
                    )
                if is_skill and mc7_count > 0:
                    m3_errors.append(
                        f"{cid}.json ({source_name}): [M20-MC7-CAP] Competencia de habilidad '{cid}' define "
                        f"{mc7_count} plantilla(s) 'multiple_choice_7_options' (MC7), pero MC7 está prohibido "
                        f"en competencias Skill (máximo 0 MC7 permitido; usa modalidades activas)."
                    )
                elif (not is_skill) and mc7_count > 1:
                    m3_errors.append(
                        f"{cid}.json ({source_name}): [M20-MC7-CAP] Competencia '{cid}' define {mc7_count} plantillas "
                        f"'multiple_choice_7_options' (MC7), excediendo el tope máximo de 1 plantilla MC7 por competencia."
                    )

                # [M20-ACTIVE-QUOTA]: >= 80% active modalities (>= 75% only when N <= 4 and (K == 1 or legacy CTA without recommended_modalities))
                if len(tpls) >= eff_min_arch:
                    active_count = sum(1 for m in actual_mods_seq if m in ACTIVE_INTERACTION_TYPES)
                    active_ratio = active_count / float(len(tpls)) if len(tpls) > 0 else 0.0
                    min_active_ratio = 0.75 if (len(tpls) <= 4 and (eff_k == 1 or not allowed_mods_list)) else 0.80
                    if active_ratio + 1e-9 < min_active_ratio:
                        m3_errors.append(
                            f"{cid}.json ({source_name}): [M20-ACTIVE-QUOTA] Competencia '{cid}' tiene solo "
                            f"{active_count}/{len(tpls)} ({active_ratio * 100:.1f}%) plantillas en modalidades activas, "
                            f"por debajo del mínimo requerido de {min_active_ratio * 100:.0f}% (>= 80% activo con <= 1 MC7)."
                        )

                if cta_contract_version >= 2 and eff_k >= 2:
                    if len(allowed_mods_list) == 0 or not (_S4_MIN_MODS <= len(allowed_mods_list) <= _S4_MAX_MODS):
                        m3_errors.append(
                            f"{cid}.json ({source_name}): [CTA-MODALITY-PLAN] Competencia '{cid}' en contrato v2 "
                            f"debe declarar entre {_S4_MIN_MODS} y {_S4_MAX_MODS} modalidades canónicas en "
                            f"cta.json['recommended_modalities'] (encontradas {len(allowed_mods_list)}: {allowed_mods_list})."
                        )

                if allowed_mods_list:
                    allowed_mods = set(allowed_mods_list)
                    unexpected_mods = sorted({m for m in actual_mods_seq if m and m not in allowed_mods})
                    if unexpected_mods:
                        m3_errors.append(
                            f"{cid}.json ({source_name}): [CTA-MODALITY-PLAN] Competencia '{cid}' usa modalidad(es) "
                            f"no autorizada(s) por el CTA Architect ({unexpected_mods}). "
                            f"Modalidades permitidas en cta.json para '{cid}': {allowed_mods_list}."
                        )
                    has_mc7_plan = ("multiple_choice_7_options" in allowed_mods) and not is_skill
                    eff_min_tpls = _s4_required_templates(
                        len(allowed_mods_list),
                        templates_per_modality=eff_k,
                        min_archetypes=eff_min_arch,
                        has_mc7=has_mc7_plan,
                    )
                    if len(tpls) < eff_min_tpls:
                        m3_errors.append(
                            f"{cid}.json ({source_name}): [CTA-MODALITY-PLAN] Competencia '{cid}' requiere mínimo "
                            f"{eff_min_tpls} plantillas para cubrir {allowed_mods_list} con K={eff_k}/modalidad activa "
                            f"(<= 1 MC7 y >= 80% activo), pero solo declara {len(tpls)}."
                        )
                    if eff_k >= 2:
                        mod_counts = collections.Counter(m for m in actual_mods_seq if m)
                        _active_allowed = [m for m in allowed_mods_list if m != "multiple_choice_7_options"]
                        for m_req in allowed_mods_list:
                            if is_skill and m_req == "multiple_choice_7_options":
                                continue
                            if m_req == "multiple_choice_7_options":
                                req_k_for_m = 1
                            elif has_mc7_plan and len(_active_allowed) == 1:
                                req_k_for_m = max(4, eff_k)
                            else:
                                req_k_for_m = eff_k
                            cnt = int(mod_counts.get(m_req, 0))
                            if cnt < req_k_for_m:
                                m3_errors.append(
                                    f"{cid}.json ({source_name}): [CTA-MODALITY-PLAN] Competencia '{cid}' requiere "
                                    f"al menos {req_k_for_m} plantilla(s) para la modalidad recomendada '{m_req}' "
                                    f"(plan: {allowed_mods_list}), pero '{m_req}' solo tiene {cnt}/{req_k_for_m}."
                                )
                    elif len(tpls) >= len(allowed_mods) and len(allowed_mods) >= 2:
                        missing_rec = sorted(allowed_mods - set(actual_mods_seq))
                        if missing_rec:
                            m3_errors.append(
                                f"{cid}.json ({source_name}): [CTA-MODALITY-PLAN] Competencia '{cid}' omitió modalidad(es) "
                                f"designada(s) por el CTA Architect ({missing_rec}). Plan requerido: {allowed_mods_list}."
                            )

                if eff_min_arch >= 4 and is_skill:
                    high_blooms = {"Apply", "Analyze", "Evaluate", "Create"}
                    if not any(b in high_blooms for b in blooms):
                        m3_errors.append(
                            f"{cid}.json ({source_name}): [M3-ARCHETYPES] Diversidad cognitiva insuficiente para habilidad '{cid}'. "
                            f"Se requiere al menos 1 nivel Bloom de aplicación o superior ({sorted(list(high_blooms))})."
                        )

                # Verificación 1 — Enunciados (stem_es) distintos por arquetipo & detección de clones
                distinct_stems = {t.get("stem_es", "").strip() for t in tpls if t.get("stem_es", "").strip()}
                norm_gen_codes = {
                    re.sub(r"def\s+gen_[a-zA-Z0-9_]+_\d+\s*\(", "def _gen_wrapper_(", t.get("generator_code", "").strip())
                    for t in tpls
                }

                if len(distinct_stems) < len(tpls):
                    m3_errors.append(
                        f"{cid}.json ({source_name}): [M3-ARCHETYPES] Competencia '{cid}' repite el mismo enunciado (stem_es) entre sus plantillas ({len(distinct_stems)} únicos de {len(tpls)} plantillas). Cada plantilla debe tener su propio enunciado distintivo."
                    )
                elif len(norm_gen_codes) < min(eff_min_arch, 2):
                    m3_errors.append(
                        f"{cid}.json ({source_name}): [M3-ARCHETYPES] Las {len(tpls)} tuplas de '{cid}' en TEMPLATES son clones idénticos (mismo generador)."
                    )

                # 4 Candados Deterministas Anti-Clon intra-competencia
                m3_errors.extend(
                    _check_intra_competency_anti_clone(
                        cid=cid,
                        source_name=source_name,
                        tpls=tpls,
                        gen_callables=gen_callables,
                        cid_ast_funcs=cid_ast_funcs,
                        eff_k=eff_k,
                        norm_shard_id=norm_shard_id,
                    )
                )

                # Verificación 2 — AST analysis de la fuente efectiva de esta competencia
                cid_clean = cid.lower().replace("-", "_")
                cid_compact = cid.lower().replace("-", "")
                cid_candidate_funcs: Set[str] = set()

                for t in tpls:
                    g_fn = t.get("gen_fn_name")
                    if g_fn and g_fn in cid_ast_funcs:
                        cid_candidate_funcs.add(g_fn)
                        w_node = cid_ast_funcs[g_fn]
                        for b_stmt in w_node.body:
                            for sub in ast.walk(b_stmt):
                                if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name):
                                    if sub.func.id in cid_ast_funcs:
                                        cid_candidate_funcs.add(sub.func.id)

                for fname, fnode in cid_ast_funcs.items():
                    if _fn_declares_arch(fnode):
                        fname_low = fname.lower()
                        has_cid_match = bool(
                            re.search(rf"(?<![a-z0-9]){re.escape(cid_clean)}(?![a-z0-9])", fname_low)
                            or re.search(rf"(?<![a-z0-9]){re.escape(cid_compact)}(?![a-z0-9])", fname_low)
                        )
                        if has_cid_match:
                            cid_candidate_funcs.add(fname)
                        elif is_modular_fix or len(target_cids) == 1:
                            cid_candidate_funcs.add(fname)

                checked_fn_names: Set[str] = set()
                for func_name in sorted(cid_candidate_funcs):
                    if func_name in checked_fn_names:
                        continue
                    checked_fn_names.add(func_name)
                    fn_node = cid_ast_funcs.get(func_name)
                    if fn_node and _fn_declares_arch(fn_node):
                        if not _fn_uses_arch_in_body(fn_node):
                            m3_errors.append(
                                f"{cid}.json ({source_name}): [M3-ARCHETYPES] Competencia '{cid}': la función generadora '{func_name}' recibe el parámetro 'arch' pero nunca lo utiliza en su cuerpo, produciendo salidas idénticas en los 4 arquetipos. Ramifica con 'if arch == 1 / elif arch == 2 / elif arch == 3 / else' para variar el problema matemático por arquetipo."
                            )
                    # Pillar 3: Detect artificial debug exceptions in generator functions
                    if fn_node:
                        for sub_ast in ast.walk(fn_node):
                            if isinstance(sub_ast, ast.Raise):
                                exc_name = ""
                                if isinstance(sub_ast.exc, ast.Call) and isinstance(sub_ast.exc.func, ast.Name):
                                    exc_name = sub_ast.exc.func.id
                                elif isinstance(sub_ast.exc, ast.Name):
                                    exc_name = sub_ast.exc.id
                                m3_errors.append(
                                    f"{cid}.json ({source_name}): [TPL-DEBUG-ARTIFACT] La función generadora '{func_name}' contiene una sentencia 'raise {exc_name or ''}' en su cuerpo. Las funciones generadoras de ítems deben retornar un diccionario de variables y opciones, sin sentencias 'raise' de depuración."
                                )
                                break

                # Verificación 3 — Detección de Evasión Trivial y Clones Matemáticos Puros (seed=100 & seed=101)
                if eff_min_arch >= 3 and len(tpls) >= 3:
                    def _eval_tuple_output(t_idx: int, seed_val: int) -> Optional[Tuple[str, str, str]]:
                        c_call = gen_callables[t_idx] if t_idx < len(gen_callables) else None
                        if callable(c_call):
                            try:
                                import random
                                from engine.sandbox import call_with_timeout, _LazyNPRNG
                                rng = random.Random(seed_val)
                                try:
                                    rng.np = _LazyNPRNG(seed_val)
                                except Exception:
                                    pass
                                res = call_with_timeout(
                                    c_call,
                                    args=(rng,),
                                    timeout=0.4,
                                    seed=seed_val,
                                )
                                if isinstance(res, dict):
                                    if "vars" not in res:
                                        c_val = res.get("correct") or res.get("ans") or ""
                                        res["vars"] = {"ans": c_val} if c_val else {}
                                    c_v = str(res.get("correct", ""))
                                    v_d = res.get("vars", {})
                                    v_s = json.dumps(v_d, sort_keys=True, default=str) if isinstance(v_d, dict) else str(v_d)
                                    opts = res.get("options", [])
                                    opts_s = ""
                                    if isinstance(opts, list) and opts:
                                        simplified_opts = [
                                            (str(o.get("value") or o.get("content", "")), bool(o.get("is_correct")))
                                            for o in opts if isinstance(o, dict)
                                        ]
                                        opts_s = json.dumps(sorted(simplified_opts), default=str)
                                    struct_s = _structured_payload_fingerprint(res)
                                    if struct_s:
                                        opts_s = f"{opts_s}|{struct_s}"
                                    return (c_v, v_s, opts_s)
                                elif isinstance(res, (tuple, list)) and len(res) >= 1 and isinstance(res[0], dict):
                                    v_d = res[0]
                                    v_s = json.dumps(v_d, sort_keys=True, default=str)
                                    return ("", v_s, "")
                            except Exception:
                                pass

                        gen_c = tpls[t_idx].get("generator_code") or tpls[t_idx].get("generate_py") or ""
                        if gen_c:
                            try:
                                from engine.sandbox import run_code_in_env
                                res = run_code_in_env(gen_c, "generate", seed=seed_val, timeout=0.5)
                                if isinstance(res, dict):
                                    if "vars" not in res:
                                        c_val = res.get("correct") or res.get("ans") or ""
                                        res["vars"] = {"ans": c_val} if c_val else {}
                                    c_v = str(res.get("correct", ""))
                                    v_d = res.get("vars", {})
                                    v_s = json.dumps(v_d, sort_keys=True, default=str) if isinstance(v_d, dict) else str(v_d)
                                    opts = res.get("options", [])
                                    opts_s = ""
                                    if isinstance(opts, list) and opts:
                                        simplified_opts = [
                                            (str(o.get("value") or o.get("content", "")), bool(o.get("is_correct")))
                                            for o in opts if isinstance(o, dict)
                                        ]
                                        opts_s = json.dumps(sorted(simplified_opts), default=str)
                                    struct_s = _structured_payload_fingerprint(res)
                                    if struct_s:
                                        opts_s = f"{opts_s}|{struct_s}"
                                    return (c_v, v_s, opts_s)
                            except Exception:
                                pass
                        return None

                    outs_100 = [_eval_tuple_output(i, 100) for i in range(len(tpls))]
                    valid_100 = [o for o in outs_100 if o is not None]
                    if is_skill and eff_min_arch >= 3 and len(valid_100) == len(tpls) and len(set(valid_100)) < len(valid_100):
                        m3_errors.append(
                            f"{cid}.json ({source_name}): [M3-ARCHETYPES] Competencia de habilidad '{cid}': las plantillas generan salidas matemáticas duplicadas en seed=100 ({len(set(valid_100))} únicas de {len(tpls)} plantillas). Cada arquetipo de habilidad debe formular una variante matemática distinta."
                        )
                    elif len(valid_100) == len(tpls) and len(set(valid_100)) < 2:
                        outs_101 = [_eval_tuple_output(i, 101) for i in range(len(tpls))]
                        valid_101 = [o for o in outs_101 if o is not None]
                        if len(valid_101) == len(tpls) and len(set(valid_101)) < 2:
                            m3_errors.append(
                                f"{cid}.json ({source_name}): [M3-ARCHETYPES] Competencia '{cid}': las {len(tpls)} tuplas generan salidas matemáticas idénticas (mismo 'correct', 'vars' y 'options' en la misma semilla). Las plantillas deben producir al menos 2 variantes matemáticas distintas."
                            )

            # Verificación 4 — Detección de Distractores por Multiplicador Arbitrario [DIAG-MAGIC-MULT] y Pistas Parentéticas [PSYCHOMETRIC-OPTIONS]
            _magic_mults = (1.333, 0.667, 1.667, 0.333, 1.25, 0.75, 1.5, 0.5, 2.1, 0.45, 1.85, 0.15)
            _distinctive_magic = {1.333, 0.667, 1.667, 0.333, 2.1, 0.45, 1.85, 0.15}
            # Shift-left: a SINGLE distractor with an exact fixed ratio (e.g. n->4n => ME/4 = 0.5*ans) in >=80% of seeds is systematic and collides with the final audit.
            _isolated_exact_mults = (0.5, 0.75, 1.5, 1.25)
            _ISO_MIN_FRACTION = 0.8
            _num_re = re.compile(r"-?\d+\.\d+|-?\d+")

            def _check_func_has_magic_mult(fn_node: ast.AST) -> bool:
                for sub_n in ast.walk(fn_node):
                    if isinstance(sub_n, ast.Constant) and isinstance(sub_n.value, (int, float)):
                        val = float(sub_n.value)
                        for mf in _magic_mults:
                            if abs(val - mf) <= 0.01:
                                return True
                    if isinstance(sub_n, ast.BinOp) and isinstance(sub_n.op, (ast.Mult, ast.Div, ast.FloorDiv)):
                        left_names = {n.id for n in ast.walk(sub_n.left) if isinstance(n, ast.Name)}
                        right_names = {n.id for n in ast.walk(sub_n.right) if isinstance(n, ast.Name)}
                        ans_indicators = {"ans", "correct", "corr", "c_val", "c_num", "target"}
                        if (left_names & ans_indicators) or (right_names & ans_indicators):
                            return True
                        if (
                            isinstance(sub_n.left, ast.Constant)
                            and isinstance(sub_n.right, ast.Constant)
                            and isinstance(sub_n.left.value, (int, float))
                            and isinstance(sub_n.right.value, (int, float))
                        ):
                            try:
                                if float(sub_n.right.value) != 0:
                                    r_val = float(sub_n.left.value) / float(sub_n.right.value)
                                    for mf in _magic_mults:
                                        if abs(r_val - mf) <= 0.01:
                                            return True
                            except Exception:
                                pass
                        if isinstance(sub_n.right, ast.Constant) and isinstance(sub_n.right.value, (int, float)):
                            try:
                                if float(sub_n.right.value) != 0:
                                    inv_factor = 1.0 / float(sub_n.right.value)
                                    for mf in _magic_mults:
                                        if abs(inv_factor - mf) <= 0.01:
                                            return True
                                    if float(sub_n.right.value) in (2.0, 3.0, 4.0, 5.0):
                                        return True
                            except Exception:
                                pass
                return False

            try:
                import zlib
                from engine.assemble import format_template_string
                _seed_base = 42 + (zlib.crc32(cid.encode("utf-8")) % 10000)
            except Exception:
                _seed_base = 10000
                format_template_string = None

            for t_idx_m, tpl_m in enumerate(tpls):
                itype_curr = tpl_m.get("interaction_type") or tpl_m.get("qtype")
                if itype_curr not in ("multiple_choice_7_options", "multiple_choice", "multiple_select"):
                    continue
                c_call_m = gen_callables[t_idx_m] if t_idx_m < len(gen_callables) else None
                if not callable(c_call_m):
                    continue
                tpl_id_m = tpl_m.get("id") or tpl_m.get("template_id") or f"T-{cid}-{t_idx_m+1:02d}"
                gen_fn_m = tpl_m.get("gen_fn_name") or getattr(c_call_m, "__name__", "gen_fn")

                tpl_seed_off = _seed_base + (t_idx_m * 500)
                eval_seeds = [tpl_seed_off + s_i for s_i in range(300)]
                hit_seeds: List[int] = []
                iso_valid_seeds = 0
                iso_hit_seeds: List[int] = []
                iso_hit_ratio: Optional[float] = None
                hit_mults_sample: List[float] = []
                hit_evidence_sample: Optional[Dict[str, Any]] = None
                iso_hit_evidence: Optional[Dict[str, Any]] = None
                corr_answers_sample: List[str] = []
                dist_samples_by_key: Dict[Any, List[str]] = defaultdict(list)
                telltale_sample: Optional[Tuple[str, str]] = None
                for s_val in eval_seeds:
                    try:
                        EvaluationContext.set(template_id=tpl_id_m, gen_fn=gen_fn_m, archetype=t_idx_m + 1, seed=s_val)
                        from engine.sandbox import call_with_timeout
                        rng_m = _make_sandbox_rng(s_val)
                        res_m = call_with_timeout(c_call_m, args=(rng_m,), timeout=0.8, seed=s_val)
                        if not isinstance(res_m, dict):
                            continue
                        if "vars" not in res_m:
                            c_val = res_m.get("correct") or res_m.get("ans") or ""
                            res_m["vars"] = {"ans": c_val} if c_val else {}
                        vars_m = res_m.get("vars", {}) if isinstance(res_m.get("vars"), dict) else {}

                        if itype_curr == "multiple_select":
                            opts_raw = res_m.get("options") or []
                            for opt_item in opts_raw:
                                if not isinstance(opt_item, dict):
                                    continue
                                val_raw = str(opt_item.get("value") if "value" in opt_item else (opt_item.get("content") or ""))
                                opt_txt = format_template_string(val_raw, vars_m) if format_template_string else val_raw
                                is_corr_opt = bool(opt_item.get("is_correct"))
                                if not telltale_sample:
                                    tt_found = _find_telltale_in_option(opt_txt, is_distractor=not is_corr_opt)
                                    if tt_found:
                                        telltale_sample = (tt_found, "distractor" if not is_corr_opt else "correct")
                            continue

                        corr_raw = str(res_m.get("correct") or res_m.get("ans") or "")
                        corr_txt = format_template_string(corr_raw, vars_m) if format_template_string else corr_raw
                        corr_answers_sample.append(corr_txt.strip())
                        if not telltale_sample:
                            tt_c = _find_telltale_in_option(corr_txt, is_distractor=False)
                            if tt_c:
                                telltale_sample = (tt_c, "correct")

                        dists_raw = res_m.get("distractors") or res_m.get("ds") or []
                        if isinstance(dists_raw, list):
                            for d_idx, d_item in enumerate(dists_raw):
                                d_k = f"d_{d_idx}"
                                if isinstance(d_item, dict):
                                    d_k = d_item.get("distractor_id") or d_k
                                    d_v = str(d_item.get("value") if "value" in d_item else (d_item.get("content") or ""))
                                elif isinstance(d_item, (tuple, list)) and len(d_item) >= 2:
                                    d_k = str(d_item[0])
                                    d_v = str(d_item[1])
                                elif isinstance(d_item, (tuple, list)) and len(d_item) == 1:
                                    d_k = str(d_item[0])
                                    d_v = str(d_item[0])
                                else:
                                    d_v = str(d_item)
                                d_txt_fmt = format_template_string(d_v, vars_m) if format_template_string else d_v
                                dist_samples_by_key[d_k].append(d_txt_fmt.strip())

                        if not isinstance(dists_raw, list) or len(dists_raw) < 4:
                            continue
                        c_nums = _num_re.findall(corr_txt)
                        if not c_nums:
                            continue
                        try:
                            c_val = parse_katex_number(c_nums[-1])
                        except Exception:
                            continue
                        if abs(c_val) <= 1e-6 or abs(c_val) in (1.0, 2.0, 4.0):
                            continue
                        matched_m: List[float] = []
                        iso_valid_seeds += 1
                        _iso_hit_here = False
                        for d_idx, d_item in enumerate(dists_raw):
                            if isinstance(d_item, (tuple, list)) and len(d_item) >= 2:
                                d_raw = str(d_item[1])
                            elif isinstance(d_item, dict):
                                d_raw = str(d_item.get("value") or d_item.get("content") or "")
                            else:
                                continue
                            d_txt = format_template_string(d_raw, vars_m) if format_template_string else d_raw
                            if not telltale_sample:
                                tt_d = _find_telltale_in_option(d_txt, is_distractor=True)
                                if tt_d:
                                    telltale_sample = (tt_d, "distractor")
                            d_nums = _num_re.findall(d_txt)
                            if not d_nums:
                                continue
                            try:
                                d_val = parse_katex_number(d_nums[-1])
                            except Exception:
                                continue
                            # Guard 1: Skip conceptual distractors sharing the same numerical value as correct answer
                            if abs(d_val - c_val) <= 1e-4:
                                continue
                            actual_ratio = d_val / c_val if abs(c_val) > 1e-9 else 0.0
                            for m_factor in _magic_mults:
                                # Ratio check with 5% relative tolerance AND absolute rounding check to reject small-number false positives
                                expected_round = round(c_val * m_factor, 3)
                                if m_factor == 0.333:
                                    expected_div = round(c_val / 3.0, 3)
                                elif m_factor == 0.667:
                                    expected_div = round(c_val * 2.0 / 3.0, 3)
                                elif m_factor == 1.333:
                                    expected_div = round(c_val * 4.0 / 3.0, 3)
                                elif m_factor == 1.667:
                                    expected_div = round(c_val * 5.0 / 3.0, 3)
                                else:
                                    expected_div = expected_round
                                if abs(actual_ratio - m_factor) <= 0.05 and (abs(d_val - expected_round) <= 0.0015 or abs(d_val - expected_div) <= 0.0015):
                                    matched_m.append(m_factor)
                                    if not hit_evidence_sample and m_factor in _distinctive_magic:
                                        hit_evidence_sample = {
                                            "seed": s_val,
                                            "dist_idx": d_idx + 1,
                                            "dist_raw": d_raw,
                                            "dist_txt": d_txt,
                                            "d_val": d_val,
                                            "c_val": c_val,
                                            "factor": m_factor,
                                            "ratio": actual_ratio,
                                        }
                                    break
                            for m_iso in _isolated_exact_mults:
                                if abs(actual_ratio - m_iso) <= 0.05 and abs(d_val - round(c_val * m_iso, 3)) <= 0.0015:
                                    _iso_hit_here = True
                                    iso_hit_ratio = m_iso
                                    if not iso_hit_evidence:
                                        iso_hit_evidence = {
                                            "seed": s_val,
                                            "dist_idx": d_idx + 1,
                                            "dist_raw": d_raw,
                                            "dist_txt": d_txt,
                                            "d_val": d_val,
                                            "c_val": c_val,
                                            "factor": m_iso,
                                            "ratio": actual_ratio,
                                        }
                                    break
                        if _iso_hit_here:
                            iso_hit_seeds.append(s_val)
                        dist_hits = [m_f for m_f in matched_m if m_f in _distinctive_magic]
                        if len(dist_hits) >= 2 or len(matched_m) >= 4:
                            hit_seeds.append(s_val)
                            if not hit_mults_sample:
                                hit_mults_sample = dist_hits[:3] or matched_m[:3]
                                if not hit_evidence_sample and matched_m:
                                    hit_evidence_sample = {
                                        "seed": s_val,
                                        "dist_idx": 1,
                                        "dist_raw": "",
                                        "dist_txt": "",
                                        "d_val": 0.0,
                                        "c_val": c_val,
                                        "factor": matched_m[0],
                                        "ratio": 0.0,
                                    }
                    except Exception as e_seed:
                        m3_errors.append(
                            f"{cid}.json ({source_name}): [TPL-EXEC-ERROR] En '{tpl_id_m}' (semilla {s_val}), la función generadora falló con excepción: {type(e_seed).__name__}: {e_seed}"
                        )
                        break
                EvaluationContext.reset(norm_shard_id)

                if telltale_sample:
                    eff_loc = fix_files_by_cid.get(cid) if is_modular_fix else shard_data_path
                    loc_obj = ShardDataLineLocator(eff_loc) if eff_loc and eff_loc.is_file() else locator
                    t_info_m = loc_obj.find_tuple_for_question(cid, template_id=tpl_id_m) if loc_obj else None
                    s_off, e_off, _ = loc_obj.find_offending_lines(t_info_m, "distractor_integrity_linter", telltale_sample[0]) if loc_obj else (1, 1, [])
                    m3_errors.append(
                        f"{cid}.json ({source_name}): [PSYCHOMETRIC-OPTIONS / parenthetical_telltale_linter / distractor_integrity_linter] En '{tpl_id_m}' (función '{gen_fn_m}', Líneas {s_off}..{e_off} en {source_name}), "
                        f"la opción visible contiene metainformación delatora: '{telltale_sample[0]}'. "
                        "Elimina palabras y coletillas delatoras del texto visible de la opción y traslada explicaciones conceptuales a 'error_rationale' o 'sol'."
                    )

                _MAGIC_MULT_MIN_FRACTION = 0.07
                _magic_min_hits = max(1, int(_MAGIC_MULT_MIN_FRACTION * iso_valid_seeds) + 1) if iso_valid_seeds > 0 else 22
                if len(hit_seeds) >= _magic_min_hits:
                    eff_loc = fix_files_by_cid.get(cid) if is_modular_fix else shard_data_path
                    loc_obj = ShardDataLineLocator(eff_loc) if eff_loc and eff_loc.is_file() else locator
                    t_info_m = loc_obj.find_tuple_for_question(cid, template_id=tpl_id_m) if loc_obj else None
                    s_off, e_off, _ = loc_obj.find_offending_lines(t_info_m, "diagnostic_rationale_alignment_linter", "multiplicador") if loc_obj else (1, 1, [])
                    evid_str = ""
                    if hit_evidence_sample and hit_evidence_sample.get("dist_txt"):
                        evid_str = (
                            f" [Evidencia semilla {hit_evidence_sample['seed']}: distractor #{hit_evidence_sample['dist_idx']} "
                            f"'{hit_evidence_sample['dist_txt']}' (val={hit_evidence_sample['d_val']}) vs correcto={hit_evidence_sample['c_val']} "
                            f"-> ratio={hit_evidence_sample['ratio']:.3f} (~x{hit_evidence_sample['factor']})]"
                        )
                    m3_errors.append(
                        f"{cid}.json ({source_name}): [DIAG-MAGIC-MULT] En '{tpl_id_m}' (función '{gen_fn_m}', Líneas {s_off}..{e_off} en {source_name}), "
                        f"los distractores numéricos en {len(hit_seeds)}/{iso_valid_seeds or len(eval_seeds)} semillas (>{_MAGIC_MULT_MIN_FRACTION*100:.0f}%, ej. seed={hit_seeds[0]}) coinciden con multiplicadores arbitrarios prohibidos ({hit_mults_sample}) respecto a la respuesta correcta.{evid_str} "
                        f"PROHIBIDO ajustar multiplicadores decimales; reemplace la expresión por la fórmula algebraica del error conceptual."
                    )
                if iso_valid_seeds >= 10 and len(iso_hit_seeds) >= _ISO_MIN_FRACTION * iso_valid_seeds and len(hit_seeds) == 0:
                    eff_loc = fix_files_by_cid.get(cid) if is_modular_fix else shard_data_path
                    loc_obj = ShardDataLineLocator(eff_loc) if eff_loc and eff_loc.is_file() else locator
                    t_info_m = loc_obj.find_tuple_for_question(cid, template_id=tpl_id_m) if loc_obj else None
                    s_off, e_off, _ = loc_obj.find_offending_lines(t_info_m, "diagnostic_rationale_alignment_linter", "multiplicador") if loc_obj else (1, 1, [])
                    iso_evid_str = ""
                    if iso_hit_evidence and iso_hit_evidence.get("dist_txt"):
                        iso_evid_str = (
                            f" [Evidencia semilla {iso_hit_evidence['seed']}: distractor #{iso_hit_evidence['dist_idx']} "
                            f"'{iso_hit_evidence['dist_txt']}' (val={iso_hit_evidence['d_val']}) vs correcto={iso_hit_evidence['c_val']} "
                            f"-> ratio={iso_hit_evidence['ratio']:.3f} (~x{iso_hit_evidence['factor']})]"
                        )
                    m3_errors.append(
                        f"{cid}.json ({source_name}): [DIAG-MAGIC-MULT] En '{tpl_id_m}' (funcion '{gen_fn_m}', Lineas {s_off}..{e_off} en {source_name}), "
                        f"un distractor numerico equivale a {iso_hit_ratio} x respuesta correcta en {len(iso_hit_seeds)}/{iso_valid_seeds} semillas (razon fija sistematica, colisiona con el linter final).{iso_evid_str} "
                        f"PROHIBIDO ajustar multiplicadores decimales; reemplace la expresión por la fórmula algebraica del error conceptual."
                    )
                if strict and len(set(corr_answers_sample)) <= 1 and len(corr_answers_sample) >= 10:
                    first_ans_str = str(corr_answers_sample[0]) if corr_answers_sample else ""
                    eff_loc = fix_files_by_cid.get(cid) if is_modular_fix else shard_data_path
                    loc_obj = ShardDataLineLocator(eff_loc) if eff_loc and eff_loc.is_file() else locator
                    t_info_m = loc_obj.find_tuple_for_question(cid, template_id=tpl_id_m) if loc_obj else None
                    s_off, e_off, _ = loc_obj.find_offending_lines(t_info_m, "TPL-STATIC-OPT", "correct") if loc_obj else (1, 1, [])
                    m3_errors.append(
                        f"{cid}.json ({source_name}): [TPL-STATIC-OPT] En '{tpl_id_m}' (función '{gen_fn_m}', Líneas {s_off}..{e_off} en {source_name}), "
                        f"mono-clave fija detectada en {len(corr_answers_sample)} semillas: '{first_ans_str}'. "
                        f"La respuesta correcta debe ser dinámica y depender de parámetros generados (@var@)."
                    )

                # Constant distractor check [TPL-CONST-DISTRACTOR]
                def _is_pure_conceptual_prose(val_str: str) -> bool:
                    if not isinstance(val_str, str):
                        return False
                    s = val_str.strip()
                    if any(ch in s for ch in "0123456789@$=<>*/^_"):
                        return False
                    words = [w for w in s.split() if w.isalpha()]
                    return len(words) >= 4

                if strict and len(set(corr_answers_sample[:50])) >= 5:
                    for d_k, d_v_list in dist_samples_by_key.items():
                        eval_vals = d_v_list[:50]
                        if len(eval_vals) >= 10:
                            v_counts = collections.Counter(eval_vals)
                            for s_val_str, freq in v_counts.items():
                                if _is_pure_conceptual_prose(s_val_str):
                                    continue
                                if freq > 5 and len(set(eval_vals)) <= max(2, len(eval_vals) // 10):
                                    eff_loc = fix_files_by_cid.get(cid) if is_modular_fix else shard_data_path
                                    loc_obj = ShardDataLineLocator(eff_loc) if eff_loc and eff_loc.is_file() else locator
                                    t_info_m = loc_obj.find_tuple_for_question(cid, template_id=tpl_id_m) if loc_obj else None
                                    s_off, e_off, _ = loc_obj.find_offending_lines(t_info_m, "TPL-CONST-DISTRACTOR", "distractor") if loc_obj else (1, 1, [])
                                    m3_errors.append(
                                        f"{cid}.json ({source_name}): [TPL-CONST-DISTRACTOR] En '{tpl_id_m}' (función '{gen_fn_m}', Líneas {s_off}..{e_off} en {source_name}): "
                                        f"el distractor '{d_k}' devuelve el mismo valor escalar idéntico '{s_val_str}' en {freq} semillas distintas (> 5), "
                                        f"a pesar de que param_space varía dinámicamente ({len(set(corr_answers_sample[:50]))} respuestas correctas distintas en 50 semillas). "
                                        f"Los distractores deben ser dinámicos y depender de parámetros generados (@var@)."
                                    )
                                    break

            # Verificación 4b — Detección Temprana de Mono-Clave [TPL-STATIC-OPT] para FIB, open_symbolic y MS
            if strict:
                for t_idx_m, tpl_m in enumerate(tpls):
                    itype_m = tpl_m.get("interaction_type") or tpl_m.get("question_type")
                    if itype_m not in ("fill_in_the_blank", "open_symbolic", "multiple_select"):
                        continue
                    c_call_m = gen_callables[t_idx_m] if t_idx_m < len(gen_callables) else None
                    if not callable(c_call_m):
                        continue
                    tpl_id_m = tpl_m.get("id") or tpl_m.get("template_id") or f"T-{cid}-{t_idx_m+1:02d}"
                    gen_fn_m = tpl_m.get("gen_fn_name") or getattr(c_call_m, "__name__", "gen_fn")
                    tpl_seed_off = _seed_base + (t_idx_m * 500)
                    eval_seeds = [tpl_seed_off + s_i for s_i in range(50 if itype_m == "multiple_select" else 20)]
                    corr_samples: List[str] = []
                    dist_samples_ms: Dict[str, List[str]] = defaultdict(list)
                    for s_val in eval_seeds:
                        try:
                            EvaluationContext.set(template_id=tpl_id_m, gen_fn=gen_fn_m, archetype=t_idx_m + 1, seed=s_val)
                            from engine.sandbox import call_with_timeout
                            res_m = call_with_timeout(c_call_m, args=(_make_sandbox_rng(s_val),), timeout=0.8, seed=s_val)
                            if not isinstance(res_m, dict):
                                continue
                            vars_m = res_m.get("vars", {}) if isinstance(res_m.get("vars"), dict) else {}
                            if itype_m in ("fill_in_the_blank", "open_symbolic"):
                                raw_cm = res_m.get("correct", res_m.get("ans", ""))
                                if isinstance(raw_cm, dict):
                                    c_raw = str(raw_cm.get("expression") or raw_cm.get("value") or raw_cm.get("canonical_algebraic") or "")
                                else:
                                    c_raw = str(raw_cm)
                                c_txt = format_template_string(c_raw, vars_m) if format_template_string else c_raw
                                corr_samples.append(c_txt.strip())
                            else:  # multiple_select
                                opts_m = res_m.get("options", [])
                                corr_set = tuple(sorted([
                                    (format_template_string(str(o.get("content") or o.get("value") or ""), vars_m) if format_template_string else str(o.get("content") or o.get("value") or "")).strip()
                                    for o in opts_m if isinstance(o, dict) and o.get("is_correct")
                                ]))
                                corr_samples.append(str(corr_set))
                                for opt_idx, o in enumerate(opts_m):
                                    if isinstance(o, dict) and not o.get("is_correct"):
                                        did_o = o.get("distractor_id") or f"opt_{opt_idx}"
                                        raw_v = str(o.get("content") or o.get("value") or "")
                                        fmt_v = (format_template_string(raw_v, vars_m) if format_template_string else raw_v).strip()
                                        dist_samples_ms[did_o].append(fmt_v)
                        except Exception:
                            pass
                    EvaluationContext.reset(norm_shard_id)
                    if len(set(corr_samples)) <= 1 and len(corr_samples) >= 10:
                        first_ans_str = str(corr_samples[0]) if corr_samples else ""
                        eff_loc = fix_files_by_cid.get(cid) if is_modular_fix else shard_data_path
                        loc_obj = ShardDataLineLocator(eff_loc) if eff_loc and eff_loc.is_file() else locator
                        t_info_m = loc_obj.find_tuple_for_question(cid, template_id=tpl_id_m) if loc_obj else None
                        s_off, e_off, _ = loc_obj.find_offending_lines(t_info_m, "TPL-STATIC-OPT", "correct") if loc_obj else (1, 1, [])
                        m3_errors.append(
                            f"{cid}.json ({source_name}): [TPL-STATIC-OPT] En '{tpl_id_m}' (función '{gen_fn_m}', Líneas {s_off}..{e_off} en {source_name}), "
                            f"mono-clave fija detectada en {len(corr_samples)} semillas: '{first_ans_str}'. "
                            f"La respuesta correcta debe ser dinámica y depender de parámetros generados (@var@)."
                        )

                    # Constant distractor check in MS [TPL-CONST-DISTRACTOR]
                    if itype_m == "multiple_select" and len(set(corr_samples[:50])) >= 5:
                        for did_o, d_vals in dist_samples_ms.items():
                            eval_vals = d_vals[:50]
                            if len(eval_vals) >= 10:
                                v_counts = collections.Counter(eval_vals)
                                for s_val_str, freq in v_counts.items():
                                    if _is_pure_conceptual_prose(s_val_str):
                                        continue
                                    if freq > 5 and len(set(eval_vals)) <= max(2, len(eval_vals) // 10):
                                        eff_loc = fix_files_by_cid.get(cid) if is_modular_fix else shard_data_path
                                        loc_obj = ShardDataLineLocator(eff_loc) if eff_loc and eff_loc.is_file() else locator
                                        t_info_m = loc_obj.find_tuple_for_question(cid, template_id=tpl_id_m) if loc_obj else None
                                        s_off, e_off, _ = loc_obj.find_offending_lines(t_info_m, "TPL-CONST-DISTRACTOR", "distractor") if loc_obj else (1, 1, [])
                                        m3_errors.append(
                                            f"{cid}.json ({source_name}): [TPL-CONST-DISTRACTOR] En '{tpl_id_m}' (función '{gen_fn_m}', Líneas {s_off}..{e_off} en {source_name}): "
                                            f"la opción falsa '{did_o}' devuelve el mismo valor escalar idéntico '{s_val_str}' en {freq} semillas distintas (> 5), "
                                            f"a pesar de que param_space varía dinámicamente ({len(set(corr_samples[:50]))} respuestas correctas distintas en 50 semillas). "
                                            f"Las opciones deben ser dinámicas y depender de parámetros generados (@var@)."
                                        )
                                        break

                # Verificación 5 — Compuerta de Diversidad de Enunciados [STEM-DIVERSITY-GATE] (Paridad con run.py --stage build)
                if eff_min_arch >= 3 and len(tpls) >= 3 and seeds >= 30:
                    try:
                        from engine.diversity import mask_stem_numbers as _mask_stem_nums
                    except Exception:
                        def _mask_stem_nums(st: str) -> str:
                            return re.sub(r"\b\d+(?:\.\d+)?\b", "[NUM]", re.sub(r"\s+", " ", st.strip()))

                    # Stage 2 -> Stage 4 contract parity: quota/threshold come from the manifest
                    # (written by plan_shards from engine.stage_contract), never hardcoded here.
                    _s4c = (shard_entry.get("stage4_contract") or {}).get(cid) if isinstance(shard_entry, dict) else None
                    if not isinstance(_s4c, dict):
                        # Legacy manifest without stage4_contract: compute from cta_comp_map / cid prefix (never leak prior loop state).
                        _cta_c_legacy = cta_comp_map.get(cid, {})
                        _legacy_type = str(_cta_c_legacy.get("type", "")).lower()
                        _legacy_skill = cid.startswith("Hab-") or _legacy_type in ("skill", "habilidad")
                        _s4c = _s4_competency_contract("skill" if _legacy_skill else "concept")
                    is_true_skill = _s4_is_skill_type(_s4c.get("type", ""))
                    quota_build = max(
                        int(_s4c["quota"]),
                        _s4_quota_for_competency(_s4c.get("type", "concept"), len(tpls)),
                    )
                    req_unique_stems = _s4_required_unique_stems(quota_build)
                    all_masked_stems: Set[str] = set()
                    stem_line_ranges: List[str] = []
                    eff_loc_s = fix_files_by_cid.get(cid) if is_modular_fix else shard_data_path
                    loc_obj_s = ShardDataLineLocator(eff_loc_s) if eff_loc_s and eff_loc_s.is_file() else locator

                    for t_idx_s, tpl_s in enumerate(tpls):
                        tpl_id_s = tpl_s.get("id") or tpl_s.get("template_id") or f"T-{cid}-{t_idx_s+1:02d}"
                        t_quota_cap = (quota_build // len(tpls)) + (1 if t_idx_s < (quota_build % len(tpls)) else 0)
                        sv_list = tpl_s.get("stem_variants") or ([tpl_s.get("stem_es")] if tpl_s.get("stem_es") else [])
                        c_call_s = gen_callables[t_idx_s] if t_idx_s < len(gen_callables) else None
                        sample_vars_list: List[Dict[str, Any]] = []
                        if callable(c_call_s):
                            for s_try in (100, 101, 102):
                                try:
                                    EvaluationContext.set(template_id=tpl_id_s, gen_fn=tpl_s.get("gen_fn_name") or "gen_fn", archetype=t_idx_s + 1, seed=s_try)
                                    from engine.sandbox import call_with_timeout
                                    r_try = call_with_timeout(c_call_s, args=(_make_sandbox_rng(s_try),), timeout=0.8, seed=s_try)
                                    if isinstance(r_try, dict) and isinstance(r_try.get("vars"), dict):
                                        sample_vars_list.append(r_try["vars"])
                                except Exception:
                                    pass
                            EvaluationContext.reset(norm_shard_id)
                        tpl_masked_stems: List[str] = []
                        for sv_raw in sv_list:
                            sv_str = str(sv_raw).strip()
                            if not sv_str:
                                continue
                            if sample_vars_list and format_template_string:
                                for sv_vars in sample_vars_list:
                                    rendered_sv = format_template_string(sv_str, sv_vars)
                                    m_st = _mask_stem_nums(rendered_sv)
                                    if m_st not in tpl_masked_stems:
                                        tpl_masked_stems.append(m_st)
                            else:
                                dummy_sv = re.sub(r"@[a-zA-Z0-9_]+(?::[^@]+)?@", "100", sv_str)
                                m_st = _mask_stem_nums(dummy_sv)
                                if m_st not in tpl_masked_stems:
                                    tpl_masked_stems.append(m_st)
                        all_masked_stems.update(tpl_masked_stems[:t_quota_cap])

                        if loc_obj_s:
                            t_info_s = loc_obj_s.find_tuple_for_question(cid, template_id=tpl_id_s)
                            s_ln, e_ln, _ = loc_obj_s.find_offending_lines(t_info_s, "anti_gaming_psychometric_linter", "stem")
                            rng_lbl = f"L{s_ln}..L{e_ln}" if s_ln != e_ln else f"L{s_ln}"
                            if rng_lbl not in stem_line_ranges:
                                stem_line_ranges.append(rng_lbl)

                    if len(all_masked_stems) < req_unique_stems:
                        cat_label = "skills" if is_true_skill else "concepts/facts"
                        _adv = _s4_stems_advice(
                            "skill" if is_true_skill else "concept",
                            min_archetypes=max(len(tpls), eff_min_arch),
                            quota=quota_build,
                        )
                        req_per_tpl = _adv["per_tpl"]
                        tot_rec = _adv["total"]
                        lines_ctx = f" [{', '.join(stem_line_ranges)} en {source_name}]" if stem_line_ranges else ""
                        m3_errors.append(
                            f"{cid}.json ({source_name}): [STEM-DIVERSITY-GATE] Diagnostic: Stem diversity gate failed for competency '{cid}' "
                            f"(only {len(all_masked_stems)} stems, required >= {req_unique_stems} unique, quota {quota_build} for {cat_label}){lines_ctx}. "
                            f"Provide >= {req_per_tpl} distinct syntactic stems per template (totaling >= {tot_rec})."
                        )

    return m3_errors


def promote_staged_templates_atomically(
    att_dir: Path,
    cert_path: Path,
    compile_att_file: Path,
    cta_p: Optional[Path],
    final_paths_by_cid: Dict[str, Path],
    norm_shard_id: str,
    receipt_p: Optional[Path],
    seeds: int,
    shard_data_path: Optional[Path],
    shard_id: str,
    shards_dir: Path,
    source_sha256: str,
    staged_paths: List[Path],
    strict: bool,
    templates_by_cid: Dict[str, List[Dict[str, Any]]],
    compiler_file_path: Path,
) -> Tuple[bool, List[str]]:
    """Clear attempt/error artifacts on PASS and atomically promote staged templates."""
    # Clear compilation attempts on success (pass clears the halt)
    if compile_att_file.is_file():
        try:
            compile_att_file.unlink()
        except Exception:
            pass
    clean_log = (shard_data_path.parent if (shard_data_path and hasattr(shard_data_path, "parent") and shard_data_path.parent.is_dir()) else shards_dir) / f"{shard_id}_compile_error.log"
    if clean_log.is_file():
        try:
            clean_log.unlink()
        except Exception:
            pass

    # Promote validated staged templates atomically to final templates_dir only on PASS
    final_compiled_paths: List[Path] = []
    for cid_p, staged_cp in zip(templates_by_cid.keys(), staged_paths):
        final_cp = final_paths_by_cid[cid_p]
        if staged_cp.is_file():
            try:
                _atomic_write_json(final_cp, json.loads(staged_cp.read_text(encoding="utf-8")))
            except Exception:
                pass
        final_compiled_paths.append(final_cp)
    compiled_paths = final_compiled_paths

    pass_marker = att_dir / f"pass_{norm_shard_id}.json"
    pass_payload = {
        "shard_id": shard_id,
        "status": "PASS",
        "source_sha256": source_sha256,
        "template_counts": {cid: len(tpls) for cid, tpls in templates_by_cid.items()},
        "timestamp": time.time(),
    }
    _atomic_write_json(pass_marker, pass_payload)

    cert_payload = {
        "schema_version": 1,
        "stage": "shard",
        "artifact_id": shard_id,
        "source_sha256": source_sha256,
        "cta_sha256": hashlib.sha256(cta_p.read_bytes()).hexdigest() if (cta_p and cta_p.is_file()) else "",
        "compiler_sha256": hashlib.sha256(Path(compiler_file_path).read_bytes()).hexdigest(),
        "contract_version": 2,
        "template_shas": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in compiled_paths if p.is_file()},
        "passed_50_seeds": bool(seeds >= 50 and strict),
        "created_at": time.time(),
    }
    _atomic_write_json(cert_path, cert_payload)

    if receipt_p:
        try:
            r_data = {}
            if receipt_p.is_file():
                try:
                    r_data = json.loads(receipt_p.read_text(encoding="utf-8"))
                except Exception:
                    r_data = {}
            r_data["shard_id"] = shard_id
            r_data["compiled_status"] = "PASS"
            r_data["has_syntax_error"] = False
            r_data["error_count"] = 0
            r_data["compilation_errors"] = []
            r_data["compiled_templates"] = [p.as_posix() for p in compiled_paths]
            r_data["compiled_at"] = time.time()
            _atomic_write_json(receipt_p, r_data)
        except Exception:
            pass

    total_archetypes = sum(len(tpls) for tpls in templates_by_cid.values())
    written_files_str = ", ".join(p.as_posix() for p in compiled_paths)
    print(f"[+] PASS: Shard '{shard_id}' compilado exitosamente ({len(compiled_paths)} competencias, {total_archetypes} plantillas/arquetipos en [{written_files_str}], {seeds} semillas dry-run validadas). STOP: No ejecutes más herramientas y emite tu señal DONE.")
    return True, []


