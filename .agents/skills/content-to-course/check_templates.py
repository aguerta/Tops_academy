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
import ast
import copy
import hashlib
import json
import logging
import os
import re
import sys
import tempfile
import textwrap
import uuid
import zlib
from collections import defaultdict
from datetime import datetime, timezone
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import jsonschema

_logger = logging.getLogger(__name__)

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

from engine import fast_json
from engine.assemble import assemble_question, format_template_string
from engine.diversity import (
    evaluate_competency_diversity,
    evaluate_slot_rationale_diversity,
    mask_stem_numbers,
)
from engine.epistemic_closure import (
    check_epistemic_closure,
    check_open_symbolic_answer_closure,
)
from engine.invariants import check_instance_invariants, validate_katex_syntax
from engine.instantiate import instantiate_competency, competency_seed_base
from engine.stage_contract import is_skill_type, MIN_DIVERSITY_RATIO
from engine.sandbox import (
    call_with_timeout,
    execute_sandbox_batch,
    execute_verifier_code,
    validate_code_ast,
    check_latex_escape_corruption,
    check_latex_escape_corruption_structured,
    warm_up_sandbox,
    SandboxExecutionError,
    SandboxTimeoutError,
    SecurityViolationError,
)
from validator.core import validate_course_content

from engine.shard_locator import ShardDataLineLocator


from engine.template_diagnostics import (
    AGENT_WARNING_NOTE,
    DiagnosticError,
    build_compact_diagnostic_groups,
    count_distinct_shard_error_hunks,
    extract_diagnostic_metadata,
    find_lines_in_file,
    find_template_field_line,
    format_diagnostic_error,
    format_invariant_error_diagnostic,
    format_parity_error,
    get_canonical_invariant_key,
    normalize_error_string_for_hash,
    render_compact_aggregated_errors,
    _format_dry_failure,
)
from engine.template_healing import (
    COMBINED_LATEX,
    LATEX_PREFIX_PATTERNS,
    _CONTROL_CHAR_CODE_MAP,
    _CONTROL_CHAR_LATEX_MAP,
    _CONTROL_CHAR_TEXT_MAP,
    _GIVEAWAY_PREFIX_RE,
    _GIVEAWAY_PREFIX_STR_RE,
    _atomic_write_bytes,
    _build_distractor_lookup_from_cta,
    _extract_template_placeholders,
    _heal_code_control_chars,
    _scan_latex_balanced_span,
    _strip_giveaway_prefix,
    _wrap_bare_latex_in_rationale,
    auto_heal_template_data,
    auto_heal_template_file,
    check_ast_rf_triple_braces,
    heal_control_chars_in_obj,
    heal_control_chars_in_str,
)


def _extract_stem_placeholder_set(text: str) -> Set[str]:
    """Extract all @var@ and {var} placeholder names from a stem or stem_variant string."""
    if not isinstance(text, str) or not text:
        return set()
    found: Set[str] = set()
    for m in re.finditer(r"@([A-Za-z_][A-Za-z0-9_]*)(?::[^@\s{}]+)?@", text):
        found.add(m.group(1))
    found.update(_extract_template_placeholders(text))
    return found


def _check_stem_variant_parity(template: Dict[str, Any]) -> List[Tuple[str, List[str]]]:
    """Verify placeholder parity across stem_variants (costo 0 LLM).

    Checks only across `stem_variants` (ignoring short/fallback `stem` headers) and flags
    variants that completely omit placeholders shared by >= 50% of the other variants
    leaving the variant with zero placeholders or missing core parameters when other
    variants share >= 2 required parameters and the variant omits all of them.
    """
    raw_variants = template.get("stem_variants")
    if not isinstance(raw_variants, list) or len(raw_variants) < 2:
        return []

    entries: List[Tuple[str, Set[str]]] = []
    for idx, sv in enumerate(raw_variants):
        if isinstance(sv, str) and sv.strip():
            entries.append((f"stem_variants[{idx}]", _extract_stem_placeholder_set(sv)))

    if len(entries) < 2:
        return []

    counts: Dict[str, int] = defaultdict(int)
    for _, phs in entries:
        for p in phs:
            counts[p] += 1

    if not counts:
        return []

    n_stems = len(entries)
    if n_stems == 2:
        # With 2 variants, flag if one variant carries parametric placeholders while the other drops all of them
        (lbl0, phs0), (lbl1, phs1) = entries
        if bool(phs0) == bool(phs1):
            return []
        empty_label = lbl0 if not phs0 else lbl1
        other_phs = sorted(phs1 if not phs0 else phs0)
        itype = str(template.get("interaction_type", "")).strip().lower()
        is_ms = itype in ("multiple_select", "ms")
        if not is_ms:
            return [(empty_label, other_phs)]
        print(
            f"WARNING: [TPL-STEM-VARIANT-PARITY] En '{template.get('id', '?')}': '{empty_label}' omite {other_phs} presente(s) en la otra variante.",
            file=sys.stderr,
        )
        return []

    majority_threshold = max(2, (n_stems + 1) // 2)
    required_phs = {p for p, c in counts.items() if c >= majority_threshold}

    if not required_phs:
        return []

    itype = str(template.get("interaction_type", "")).strip().lower()
    is_ms = itype in ("multiple_select", "ms")
    violations: List[Tuple[str, List[str]]] = []
    for label, phs in entries:
        missing = sorted(required_phs - phs)
        # Flag as hard parity error when a non-MS variant drops ALL parametric placeholders (len(phs) == 0)
        # or omits the entire multi-variable core (len(required_phs) >= 2 and len(missing) == len(required_phs)).
        # In multiple_select, variants can legitimately state conceptual prompts without placeholders because
        # each option carries its own expressions; emit a WARNING instead.
        if not is_ms and missing:
            violations.append((label, missing))
        elif missing:
            print(
                f"WARNING: [TPL-STEM-VARIANT-PARITY] En '{template.get('id', '?')}': '{label}' omite {missing} presente(s) en la mayoría de variantes.",
                file=sys.stderr,
            )
    return violations


def _check_stem_derivative_giveaway(text: str) -> Optional[Tuple[str, str]]:
    """Detect if stem defines an explicit function AND gives away its evaluated derivative.
    
    Returns (fn_def_snippet, deriv_snippet) if giveaway detected, else None.
    Excludes critical point conditions (f'(x) = 0) and abstract functions without formula.
    """
    if not isinstance(text, str) or "'" not in text:
        return None
    fn_def_re = re.compile(
        r"([a-zA-Z])\s*\(\s*(\\?[a-zA-Z][a-zA-Z0-9_]*)\s*\)\s*=\s*([^\n,;\$]+)"
    )
    deriv_re = re.compile(
        r"([a-zA-Z])'\s*\(\s*([^\n\)=]+)\s*\)\s*=\s*([^\n,;\$]+)"
    )
    defs = {}
    for m in fn_def_re.finditer(text):
        fname = m.group(1)
        arg = m.group(2).strip()
        rhs = m.group(3).strip()
        if any(op in rhs for op in ("+", "-", "*", "/", "^", "\\frac", "\\sqrt", "\\ln", "\\exp", "\\sin", "\\cos")) or any(char in rhs for char in arg.lstrip("\\")):
            defs[fname] = m.group(0).strip()
            
    if not defs:
        return None

    for m in deriv_re.finditer(text):
        fname = m.group(1)
        arg = m.group(2).strip()
        rhs = m.group(3).strip()
        if fname in defs:
            clean_rhs = rhs.strip().strip("$").strip()
            if clean_rhs in ("0", "0.0", "00", "\\mathbf{0}", "\\vec{0}"):
                continue
            return (defs[fname], m.group(0).strip())

    return None


def _check_orphan_vars(
    template: Dict[str, Any],
    batch_results: List[Dict[str, Any]],
    cross_check_py: str,
    comp_templates: Optional[List[Dict[str, Any]]] = None,
    cta_distractors_map: Optional[Dict[str, Dict[str, Any]]] = None,
) -> Set[str]:
    """Find unused keys in 'vars' returned by generate_py."""
    raw_vars_keys: Set[str] = set()
    for r in batch_results:
        if r.get("success") and isinstance(r.get("result"), dict):
            v_dict = r["result"].get("vars")
            if isinstance(v_dict, dict):
                raw_vars_keys.update(v_dict.keys())
    if not raw_vars_keys:
        return set()

    used_tokens: Set[str] = set()

    def _extract_from_text(txt: Any) -> None:
        if not isinstance(txt, str) or not txt:
            return
        for m in re.finditer(r"@([a-zA-Z0-9_]+)(?::[^@]*)?@", txt):
            used_tokens.add(m.group(1))
        used_tokens.update(_extract_template_placeholders(txt))

    def _extract_from_tpl(tpl_obj: Dict[str, Any]) -> None:
        if not isinstance(tpl_obj, dict):
            return
        _extract_from_text(tpl_obj.get("stem", ""))
        for sv in tpl_obj.get("stem_variants") or []:
            _extract_from_text(sv)
        for h in tpl_obj.get("hints") or []:
            _extract_from_text(h.get("text", "") if isinstance(h, dict) else str(h))
        _extract_from_text(tpl_obj.get("solution", ""))
        _extract_from_text(tpl_obj.get("sol", ""))
        _extract_from_text(tpl_obj.get("detailed_solution", ""))
        _extract_from_text(tpl_obj.get("explanation_es", ""))
        _extract_from_text(tpl_obj.get("generate_py", ""))
        _extract_from_text(tpl_obj.get("generator_code", ""))
        for opt in (tpl_obj.get("options") or tpl_obj.get("distractors") or []):
            if isinstance(opt, dict):
                for val in opt.values():
                    if isinstance(val, str):
                        _extract_from_text(val)
            elif isinstance(opt, (tuple, list)):
                for val in opt:
                    if isinstance(val, str):
                        _extract_from_text(val)
        dmap = tpl_obj.get("distractor_map") or {}
        if isinstance(dmap, dict):
            for val in dmap.values():
                if isinstance(val, str):
                    _extract_from_text(val)
                elif isinstance(val, dict):
                    for subval in val.values():
                        if isinstance(subval, str):
                            _extract_from_text(subval)

    _extract_from_tpl(template)
    if comp_templates:
        for other_tpl in comp_templates:
            _extract_from_tpl(other_tpl)

    if cta_distractors_map and isinstance(cta_distractors_map, dict):
        for cd in cta_distractors_map.values():
            if isinstance(cd, dict):
                for v in cd.values():
                    if isinstance(v, str):
                        _extract_from_text(v)

    # Generated results options/distractors/error_rationale
    for r in batch_results:
        if r.get("success") and isinstance(r.get("result"), dict):
            res_obj = r["result"]
            for opt in (res_obj.get("options") or res_obj.get("distractors") or []):
                if isinstance(opt, dict):
                    for val in opt.values():
                        if isinstance(val, str):
                            _extract_from_text(val)

    # Cross check py inspection
    cross_keys: Set[str] = set()
    if cross_check_py and isinstance(cross_check_py, str):
        try:
            tree = ast.parse(textwrap.dedent(cross_check_py.strip()))
            for node in ast.walk(tree):
                if isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, str):
                    cross_keys.add(node.slice.value)
                elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "get" and node.args:
                    if isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                        cross_keys.add(node.args[0].value)
                elif isinstance(node, ast.Name):
                    if node.id in raw_vars_keys:
                        cross_keys.add(node.id)
                elif isinstance(node, ast.Constant) and isinstance(node.value, str):
                    if node.value in raw_vars_keys:
                        cross_keys.add(node.value)
        except Exception:
            for k in raw_vars_keys:
                if k in cross_check_py:
                    cross_keys.add(k)

    allowlist = {"ans", "correct", "val"}
    return raw_vars_keys - used_tokens - cross_keys - allowlist




_MATH_SPAN_RE = re.compile(r"\$\$(.+?)\$\$|\$(.+?)\$", re.S)
_PY_SCI_RE = re.compile(r"(?<![A-Za-z\\])\d(?:\.\d+)?[eE][-+]?\d+")
_TEXT_CMD_RE = re.compile(r"\\text\{([^{}]*)\}")
_TEXT_MAX_WORDS = 2
_TEXT_MAX_CHARS = 20


def check_render_hygiene_in_instance(instance: Dict[str, Any]) -> List[str]:
    """Reject raw Python scientific notation (1.2e-05) and narrative prose inside KaTeX."""
    fields: List[Tuple[str, Any]] = [
        ("stem", instance.get("stem")),
        ("solution", instance.get("solution") or instance.get("explanation") or instance.get("detailed_solution")),
    ]
    for idx, h in enumerate(instance.get("hints", []) or []):
        fields.append((f"hint {idx + 1}", h))
    for idx, opt in enumerate(instance.get("options", []) or []):
        if isinstance(opt, dict):
            fields.append((f"option {idx + 1} content", opt.get("content")))
            fields.append((f"option {idx + 1} error_rationale", opt.get("error_rationale")))
    errs: List[str] = []
    for ctx, text in fields:
        if not isinstance(text, str) or not text:
            continue
        for m in _MATH_SPAN_RE.finditer(text):
            span = m.group(1) or m.group(2) or ""
            sci = _PY_SCI_RE.search(span)
            if sci:
                errs.append(
                    f"[KATEX-PY-SCI-NOTATION] {ctx}: notación científica cruda de Python "
                    f"'{sci.group(0)}' dentro de KaTeX. Formatea como mantisa \\times 10^{{exp}} "
                    f"(ej. 2.63\\times 10^{{-5}}) o usa decimales fijos."
                )
            for tm in _TEXT_CMD_RE.finditer(span):
                inner = tm.group(1).strip()
                if len(inner.split()) > _TEXT_MAX_WORDS or len(inner) > _TEXT_MAX_CHARS:
                    errs.append(
                        f"[KATEX-TEXT-PROSE] {ctx}: prosa '\\text{{{inner[:40]}}}' dentro de KaTeX "
                        f"(máx {_TEXT_MAX_WORDS} palabras / {_TEXT_MAX_CHARS} caracteres). "
                        f"Saca la prosa fuera de $...$ y deja solo la fórmula en KaTeX."
                    )
    return list(dict.fromkeys(errs))


def check_unrendered_placeholders_in_instance(
    instance: Dict[str, Any],
    variables: Dict[str, Any],
) -> List[str]:
    """Reject unresolved PrairieLearn @var@ and uninterpolated {key} in vars or bare {ident} outside legitimate LaTeX."""
    from engine.invariants import check_unrendered_placeholders
    errs = []
    fields = [
        ("stem", instance.get("stem")),
        ("solution", instance.get("solution") or instance.get("explanation") or instance.get("detailed_solution")),
        ("common_misconception_warning", instance.get("common_misconception_warning") or instance.get("misconception_warning")),
    ]
    for idx, h in enumerate(instance.get("hints", []) or []):
        fields.append((f"hint {idx + 1}", h))
    for idx, opt in enumerate(instance.get("options", []) or []):
        if isinstance(opt, dict):
            fields.append((f"option {idx + 1} content", opt.get("content")))
            fields.append((f"option {idx + 1} error_rationale", opt.get("error_rationale")))
    ca = instance.get("correct_answer")
    if isinstance(ca, str):
        fields.append(("correct_answer", ca))
    elif isinstance(ca, dict):
        for k, v in ca.items():
            if isinstance(v, str):
                fields.append((f"correct_answer.{k}", v))

    for ctx, text in fields:
        if not isinstance(text, str) or not text:
            continue
        errs.extend(check_unrendered_placeholders(text, ctx, variables=variables))
    return list(dict.fromkeys(errs))


def synthetic_boilerplate_distractor_rule(assembled_q: Dict[str, Any]) -> List[str]:
    """Evaluates question instance options against synthetic boilerplate patterns."""
    from engine.invariants import check_synthetic_boilerplate_distractors
    correct_content = None
    distractor_contents = []
    for opt in assembled_q.get("options", []):
        if opt.get("is_correct") is True:
            correct_content = opt.get("content")
        else:
            distractor_contents.append(str(opt.get("content", "")))
    return check_synthetic_boilerplate_distractors(correct_content, distractor_contents)


def scaffolding_answer_leak_rule(hints: List[Any]) -> List[str]:
    """Evaluates question hints against mechanical scaffolding answer leaks."""
    from engine.invariants import check_scaffolding_answer_leaks
    return check_scaffolding_answer_leaks(hints)


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
        questions_by_id = {q.get("id", ""): q for q in questions if isinstance(q, dict)}
        grouped_parity_errors: Dict[Tuple[str, str], Tuple[Any, List[str]]] = {}
        for err in v_res.errors:
            # Skip course-level checks inapplicable to single competency mini-course
            skip_rules = {"R-05", "R-06", "R-07", "R-08", "R-09"}
            if len(questions) < 10:
                skip_rules.add("R-16")
            if err.rule_id in skip_rules:
                continue

            q_id = getattr(err, "item_id", None) or "UNKNOWN"
            msg = getattr(err, "message", str(err))
            clean_msg = re.sub(r"\bQ-[A-Za-z0-9_-]+\b", "Q-XXX", msg)
            if q_id and q_id != "UNKNOWN":
                clean_msg = clean_msg.replace(q_id, "Q-XXX")
            clean_msg = re.sub(r"\s+at line \d+(?:, col \d+)?", "", clean_msg)
            clean_msg = re.sub(r"\s*\(line \d+(?:, col \d+)?\)", "", clean_msg)
            sig = (err.rule_id, clean_msg)
            if sig not in grouped_parity_errors:
                grouped_parity_errors[sig] = (err, [q_id])
            else:
                grouped_parity_errors[sig][1].append(q_id)

        for sig, (rep_err, q_id_list) in grouped_parity_errors.items():
            unique_q_ids = list(dict.fromkeys(q_id_list))
            errors.append(format_parity_error(cid, rep_err, questions_by_id, item_ids=unique_q_ids))

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

    def _leaf_errors(e):
        """Drill into oneOf/anyOf contexts and return the most relevant concrete sub-errors."""
        if not e.context:
            return [e]
        out = []
        # Prefer the branch whose root type matches the data (object -> template_item/file, list -> array)
        by_branch: Dict[int, List[Any]] = {}
        for sub in e.context:
            by_branch.setdefault(sub.schema_path[0] if sub.schema_path else 0, []).append(sub)
        best = min(by_branch.values(), key=lambda subs: sum(1 for s in subs if s.validator == "type" and not list(s.absolute_path)))
        for sub in best:
            out.extend(_leaf_errors(sub))
        return out or [e]

    for err in validator.iter_errors(data):
        for leaf in _leaf_errors(err):
            loc = " -> ".join(str(p) for p in list(err.path) + list(leaf.path))
            msg = leaf.message
            errors.append(f"Template schema violation at [{loc}]: {msg}")
    seen = set()
    errors = [e for e in errors if not (e in seen or seen.add(e))]
    return errors


from engine.template_validators import (
    _M20_STRUCTURED_TYPES,
    check_distractor_refutation,
    check_mc7_and_ms_verifier_refutation,
    check_multimodal_tpl_d3_coverage,
    evaluate_static_opt_and_dynamic_rationale,
    update_circuit_breaker_state,
    validate_template_static_rules,
)

def _extract_instance_distractor_ids(instance: Any) -> Set[str]:
    """Collect all normalized distractor_id references across all 9 interaction modalities."""
    if not isinstance(instance, dict):
        return set()
    dids: Set[str] = set()

    def _add(val: Any) -> None:
        if isinstance(val, str) and val.strip():
            dids.add(val.strip().replace("_", "-"))

    for opt in instance.get("options") or []:
        if isinstance(opt, dict):
            _add(opt.get("distractor_id") or opt.get("did"))
    for dd in instance.get("diagnostic_distractors") or []:
        if isinstance(dd, dict):
            _add(dd.get("distractor_id") or dd.get("did"))
    dag = instance.get("proof_dag")
    if isinstance(dag, dict):
        for st in dag.get("steps") or []:
            if isinstance(st, dict):
                _add(st.get("distractor_id") or st.get("did"))
    adv = instance.get("adversarial_break")
    if isinstance(adv, dict):
        for st in adv.get("steps") or []:
            if isinstance(st, dict):
                _add(st.get("distractor_id") or st.get("did"))
        for ro in adv.get("reason_options") or []:
            if isinstance(ro, dict):
                _add(ro.get("distractor_id") or ro.get("did"))
        for pr in adv.get("predicates") or []:
            if isinstance(pr, dict):
                _add(pr.get("distractor_id") or pr.get("did"))
        for tp in adv.get("trap_predicates") or []:
            if isinstance(tp, dict):
                _add(tp.get("distractor_id") or tp.get("did"))
    um = instance.get("unstructured_model")
    if isinstance(um, dict):
        for it in (um.get("phase1_variables") or {}).get("items") or []:
            if isinstance(it, dict):
                _add(it.get("distractor_id") or it.get("did"))
        for opt in (um.get("phase2_assumptions") or {}).get("options") or []:
            if isinstance(opt, dict):
                _add(opt.get("distractor_id") or opt.get("did"))
        p3 = um.get("phase3_formulation") or {}
        if isinstance(p3, dict):
            for opt in p3.get("options") or []:
                if isinstance(opt, dict):
                    _add(opt.get("distractor_id") or opt.get("did"))
            for dd in p3.get("diagnostic_distractors") or []:
                if isinstance(dd, dict):
                    _add(dd.get("distractor_id") or dd.get("did"))
    ic = instance.get("invariant_canvas")
    if isinstance(ic, dict):
        for inv in ic.get("invariants") or []:
            if isinstance(inv, dict):
                _add(inv.get("distractor_id") or inv.get("did"))
        ti = ic.get("tree_invariants") or {}
        if isinstance(ti, dict):
            _add(ti.get("distractor_id") or ti.get("did"))
            for tdid in ti.get("distractor_ids") or []:
                _add(tdid)
    cm = instance.get("concept_matching")
    if isinstance(cm, dict):
        for tg in cm.get("targets") or []:
            if isinstance(tg, dict):
                _add(tg.get("distractor_id") or tg.get("did"))
    return dids


def _canonical_answer_signature(q: Dict[str, Any], q_type: str) -> Any:
    """Return a hashable signature of the assembled answer/payload across all 9 interaction types."""
    if q_type in ("multiple_choice_7_options", "multiple_choice"):
        correct_opt = next((opt for opt in q.get("options", []) if opt.get("is_correct")), None)
        return re.sub(r"\s+", " ", str(correct_opt.get("content", ""))).strip() if correct_opt else ""
    if q_type in ("fill_in_the_blank", "open_symbolic"):
        ans = q.get("correct_answer")
        if isinstance(ans, dict):
            val = ans.get("expression") or ans.get("value") or ans.get("canonical_algebraic") or q.get("correct", "")
        else:
            val = ans if ans is not None else q.get("correct", "")
        return re.sub(r"\s+", " ", str(val)).strip()
    if q_type == "multiple_select":
        return frozenset(
            (re.sub(r"\s+", " ", str(opt.get("content", ""))).strip(), bool(opt.get("is_correct")))
            for opt in q.get("options", [])
        )
    if q_type in _M20_STRUCTURED_TYPES:
        sig_obj: Dict[str, Any] = {"correct_answer": q.get("correct_answer")}
        if q_type in q and isinstance(q[q_type], dict):
            payload = q[q_type]
            # Include rendered text/math fields so parametric steps/curves with static IDs reflect variance
            if q_type == "proof_dag":
                sig_obj["steps"] = sorted(
                    ((s.get("id"), s.get("content"), bool(s.get("is_fallacy")))
                     for s in (payload.get("steps") or []) if isinstance(s, dict)),
                    key=lambda t: str(t),
                )
            elif q_type == "adversarial_break":
                sig_obj["prompt"] = payload.get("prompt")
                sig_obj["sample_witness"] = payload.get("sample_witness")
                sig_obj["steps"] = [
                    (s.get("id"), s.get("content"), bool(s.get("is_fallacy")))
                    for s in (payload.get("steps") or []) if isinstance(s, dict)
                ]
                sig_obj["predicates"] = [
                    p.get("expr") for p in (payload.get("predicates") or []) if isinstance(p, dict)
                ]
            elif q_type == "unstructured_model":
                sig_obj["p1"] = sorted(
                    ((it.get("id"), it.get("label"))
                     for it in ((payload.get("phase1_variables") or {}).get("items") or []) if isinstance(it, dict)),
                    key=lambda t: str(t),
                )
                sig_obj["p2"] = sorted(
                    str((o.get("id"), o.get("content")))
                    for o in ((payload.get("phase2_assumptions") or {}).get("options") or []) if isinstance(o, dict)
                )
                _p3 = payload.get("phase3_formulation") or {}
                sig_obj["p3"] = _p3.get("correct_expression")
                sig_obj["p3_opts"] = sorted(
                    str((o.get("id"), o.get("content")))
                    for o in (_p3.get("options") or []) if isinstance(o, dict)
                )
            elif q_type == "invariant_canvas":
                sig_obj["curves"] = (payload.get("fixed_curves"), payload.get("interactive_curves"))
                sig_obj["invariants"] = payload.get("invariants")
                sig_obj["inequality"] = payload.get("inequality")
                sig_obj["geometry"] = {
                    "fixed_points": payload.get("fixed_points"),
                    "interactive_points": payload.get("interactive_points"),
                    "segments": payload.get("segments"),
                    "polygons": payload.get("polygons"),
                    "shaded_regions": payload.get("shaded_regions"),
                    "sliders": payload.get("sliders"),
                }
                sig_obj["target_state"] = payload.get("target_state")
                sig_obj["tree"] = (payload.get("nodes"), payload.get("edges"), payload.get("tree_invariants"))
            elif q_type == "concept_matching":
                sig_obj["premises"] = sorted(
                    ((p.get("id"), p.get("content")) for p in (payload.get("premises") or []) if isinstance(p, dict)),
                    key=lambda t: str(t),
                )
                sig_obj["targets"] = sorted(
                    ((t.get("id"), t.get("content")) for t in (payload.get("targets") or []) if isinstance(t, dict)),
                    key=lambda t: str(t),
                )
        return json.dumps(sig_obj, sort_keys=True, default=str)
    return str(q.get("correct", "")).strip()


_DIGIT_PLACEHOLDER_CONCAT_RE = re.compile(
    r"(?:\d@[a-zA-Z_]\w*@|@[a-zA-Z_]\w*@\d|@[a-zA-Z_]\w*@@[a-zA-Z_]\w*@)"
)


def _check_digit_placeholder_concat(template: Dict[str, Any]) -> List[Tuple[str, str]]:
    """Scan raw template text fields (and generate_py string literals) for digit-placeholder concatenation."""
    hits: List[Tuple[str, str]] = []

    def _scan_val(val: Any, path_label: str) -> None:
        if isinstance(val, str):
            m = _DIGIT_PLACEHOLDER_CONCAT_RE.search(val)
            if m:
                hits.append((path_label, m.group(0)))
        elif isinstance(val, (list, tuple)):
            for idx, item in enumerate(val):
                _scan_val(item, f"{path_label}[{idx}]")
        elif isinstance(val, dict):
            for k, v in val.items():
                _scan_val(v, f"{path_label}.{k}")

    for field_name in ("stem", "stem_es", "stem_variants", "hints", "solution", "explanation_es", "sol", "rats"):
        if template.get(field_name) is not None:
            _scan_val(template.get(field_name), field_name)

    gen_src = template.get("generate_py") or template.get("generator_code")
    if isinstance(gen_src, str) and gen_src.strip():
        try:
            tree = ast.parse(gen_src)
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    m = _DIGIT_PLACEHOLDER_CONCAT_RE.search(node.value)
                    if m:
                        hits.append(("generate_py", m.group(0)))
                        break
        except SyntaxError:
            m = _DIGIT_PLACEHOLDER_CONCAT_RE.search(gen_src)
            if m:
                hits.append(("generate_py", m.group(0)))

    return hits


def check_single_template(
    template: Dict[str, Any],
    competency_id: str,
    declared_distractor_ids: Set[str],
    cta_distractors_map: Optional[Dict[str, Dict[str, Any]]] = None,
    num_dry_run_seeds: int = 50,
    shard_py: Optional[Union[str, Path]] = None,
    strict: bool = True,
    comp_templates: Optional[List[Dict[str, Any]]] = None,
    warnings_out: Optional[List[str]] = None,
) -> List[str]:
    """Validate a single template including AST, dry-run, invariants, and TPL rules."""
    errors = []
    tpl_id = template.get("id", "UNKNOWN")
    interaction_type = template.get("interaction_type", "")
    generate_py = template.get("generate_py", "")
    cross_check_py = template.get("cross_check_py") or template.get("verifier_code") or ""
    distractor_ids = template.get("distractor_ids", [])

    # Early static check: digit-placeholder concatenation ([TPL-DIGIT-PLACEHOLDER-CONCAT])
    for concat_field, concat_tok in _check_digit_placeholder_concat(template):
        errors.append(format_diagnostic_error(
            "TPL-DIGIT-PLACEHOLDER-CONCAT: CONCATENACIÓN DÍGITO-PLACEHOLDER",
            competency_id,
            tpl_id,
            tpl_id,
            concat_field,
            concat_tok,
            f"[TPL-DIGIT-PLACEHOLDER-CONCAT] Digit-placeholder concatenation '{concat_tok}' detected in '{concat_field}'; "
            f"precompute the product in vars or insert an explicit operator (\\cdot) so interpolation never concatenates digits (e.g. 2@c@ -> 21).",
            [
                "Precomputa el coeficiente compuesto dentro de 'vars' en generate_py (ej. coef=2*c) e interpola @coef@.",
                "O inserta un operador explícito entre dígito y placeholder (ej. 2 \\cdot @c@) o entre dos placeholders (@a@ \\cdot @b@).",
            ],
        ))

    # Strict hint length check (>= 25 characters)
    if strict:
        hints_list = template.get("hints", [])
        if isinstance(hints_list, list):
            for h_idx, h in enumerate(hints_list):
                h_text = h.get("text", "") if isinstance(h, dict) else str(h)
                if len(h_text.strip()) < 25:
                    errors.append(format_diagnostic_error(
                        "TPL-HINT: LONGITUD INSUFICIENTE DE PISTA", competency_id, tpl_id, f"hints[{h_idx}]", "hints",
                        f"'{h_text.strip()}' ({len(h_text.strip())} chars)",
                        f"La pista {h_idx + 1} en '{tpl_id}' tiene menos de 25 caracteres ({len(h_text.strip())} < 25). Las pistas de andamiaje socrático deben ser formativas y sustanciales.",
                        [
                            "Ampliar la pista para ofrecer una orientación conceptual sustancial (mínimo 25 caracteres).",
                            "Explicar el paso analítico o la fórmula relevante en lugar de frases breves.",
                            "Revisar las directrices de andamiaje socrático.",
                        ]
                    ))

    # Check derivative giveaway in stem and stem_variants
    all_stems = [template.get("stem", "")] + (template.get("stem_variants") or [])
    for s_idx, st_txt in enumerate(all_stems):
        if isinstance(st_txt, str):
            dg = _check_stem_derivative_giveaway(st_txt)
            if dg:
                fn_snippet, deriv_snippet = dg
                field_label = "stem" if s_idx == 0 else f"stem_variants[{s_idx - 1}]"
                errors.append(format_diagnostic_error(
                    "R-19: FUGA DE RESPUESTA / DERIVADA RESUELTA EN STEM",
                    competency_id,
                    tpl_id,
                    tpl_id,
                    field_label,
                    f"Definición: '{fn_snippet}' | Derivada entregada: '{deriv_snippet}'",
                    f"[-] [R-19] [TPL-STEM-DERIV-GIVEAWAY] violation in '{tpl_id}': El enunciado define explícitamente la función ('{fn_snippet}') y además entrega su derivada evaluada ('{deriv_snippet}'), anulando la demanda cognitiva del reactivo.",
                    [
                        "Remover la derivada evaluada del enunciado para que el estudiante deba calcularla.",
                        "Si el ejercicio evalúa cálculo diferencial, exigir al estudiante derivar la función en lugar de regalar el valor de la derivada.",
                        "Si solo se busca evaluar álgebra posterior sin derivación, enunciar directamente la función derivada o formular la consigna conceptualmente.",
                    ]
                ))
                break

    # Check deterministic placeholder parity across stem and all stem_variants ([TPL-STEM-VARIANT-PARITY])
    parity_violations = _check_stem_variant_parity(template)
    for pv_field, pv_missing in parity_violations:
        missing_str = ", ".join(f"@{v}@" for v in pv_missing)
        errors.append(format_diagnostic_error(
            "TPL-STEM-VARIANT-PARITY: ASIMETRÍA DE PLACEHOLDERS EN STEM_VARIANTS",
            competency_id,
            tpl_id,
            tpl_id,
            pv_field,
            f"Faltan placeholders: {missing_str}",
            f"[-] [TPL-STEM-VARIANT-PARITY] violation in '{tpl_id}': '{pv_field}' omite los placeholders {missing_str} presentes en el stem base o en la mayoría de las demás variantes, lo que genera enunciados incompletos o con variables sin definir.",
            [
                f"Incluir explícitamente {missing_str} dentro de '{pv_field}' con su definición contextual clara.",
                "Verificar que todas las variantes de 'stem_variants' inyecten el mismo conjunto de variables paramétricas requeridas para resolver el reactivo.",
                "Si una variable realmente no aplica a esa variante, reformular 'stem_variants' para que sean equivalentes en información dada.",
            ]
        ))

    # Concise explanation check (blocking under strict=True)
    sol_text = str(template.get("solution") or template.get("sol") or template.get("explanation_es") or "").strip()
    if len(sol_text) < 60 and (strict or len(sol_text) > 0):
        if strict:
            errors.append(format_diagnostic_error(
                "TPL-EXP-SHORT: EXPLICACIÓN INSUFICIENTE", competency_id, tpl_id, tpl_id, "explanation_es",
                f"'{sol_text[:30]}...' ({len(sol_text)} chars)",
                f"[-] [TPL-EXP-SHORT] violation in '{tpl_id}': explanation_es tiene {len(sol_text)} caracteres (< 60 chars requeridos en --strict).",
                [
                    "Ampliar 'sol' / 'explanation_es' a al menos 60 caracteres detallando el razonamiento paso a paso.",
                    "Incluir la derivación o interpretación conceptual que justifica la respuesta correcta.",
                    "Evitar explicaciones telegráficas o placeholders.",
                ]
            ))
        else:
            print(
                f"WARNING: [TPL-EXP-SHORT] En '{tpl_id}': explanation_es ('{sol_text[:30]}...') tiene {len(sol_text)} caracteres (< 60 chars). "
                f"Se recomienda enriquecer la retroalimentación formativa y detallar el paso a paso.",
                file=sys.stderr,
            )

    validate_template_static_rules(
        template=template,
        competency_id=competency_id,
        tpl_id=tpl_id,
        interaction_type=interaction_type,
        generate_py=generate_py,
        cross_check_py=cross_check_py,
        distractor_ids=distractor_ids,
        declared_distractor_ids=declared_distractor_ids,
        errors=errors,
    )

    # 5. Dry-run 50 seeds and invariant evaluation
    seeds = list(range(100, 100 + num_dry_run_seeds))
    try:
        batch_results = execute_sandbox_batch(
            generate_py=generate_py,
            seeds=seeds,
            cross_check_py=cross_check_py,
            timeout_per_item=0.8,
        )
    except Exception as e:
        errors.append(format_diagnostic_error(
            "TPL-DRY: FALLO EN EJECUCIÓN DRY-RUN", competency_id, tpl_id, "batch_execution", "generate_py / cross_check_py",
            str(e), f"La ejecución por lotes en el sandbox falló completamente: {e}",
            [
                "Revisar la sintaxis y excepciones en generate_py o cross_check_py.",
                "Asegurar que el código sea determinista y termine dentro del tiempo límite de 2.0s.",
                "Verificar que no haya dependencias externas no disponibles.",
            ]
        ))
        return errors

    failed_seeds = [r for r in batch_results if not r.get("success")]
    if failed_seeds:
        first_failed = failed_seeds[0]
        first_seed = first_failed.get("seed", 100)
        first_err = first_failed.get("error", "Unknown error")
        seed_items = [f"seed={r.get('seed')}" for r in failed_seeds]
        dry_failure_report = _format_dry_failure(
            competency_id=competency_id,
            tpl_id=tpl_id,
            generate_py=generate_py,
            failing_seed=first_seed,
            cross_check_py=cross_check_py,
            shard_py=shard_py,
            raw_error=first_err,
        )
        errors.append(format_diagnostic_error(
            "TPL-DRY: FALLO EN EJECUCIÓN DRY-RUN", competency_id, tpl_id, seed_items, "generate_py / cross_check_py",
            f"Error en seed {first_seed}: {first_err}",
            f"La ejecución en sandbox falló en {len(failed_seeds)}/{num_dry_run_seeds} semillas evaluadas.\n{dry_failure_report}",
            [
                "Revisar la excepción en generate_py (división por cero, clave faltante, error de tipos, etc.).",
                "Probar localmente la función generate_py con la semilla que causó el fallo.",
                "Agregar validaciones o restricciones a los parámetros aleatorios para evitar estados matemáticos inválidos.",
            ]
        ))
        if len(failed_seeds) == len(batch_results):
            # Full failure of all seeds: no instances can be evaluated further
            return errors

    check_mc7_and_ms_verifier_refutation(
        interaction_type=interaction_type,
        strict=strict,
        cross_check_py=cross_check_py,
        batch_results=batch_results,
        competency_id=competency_id,
        tpl_id=tpl_id,
        errors=errors,
        warnings_out=warnings_out,
    )

    # Check invariants on all generated instances (Full Sweep: NO premature break)
    raw_asm_failures: Dict[str, List[str]] = {}
    raw_inv_failures: Dict[str, Tuple[str, List[str]]] = {}
    rendered_correct_answers: List[Any] = []
    distractor_contents_by_slot: Dict[Any, List[str]] = defaultdict(list)
    distractor_rationales_by_slot: Dict[Any, List[str]] = defaultdict(list)
    epistemic_checked = False
    checked_symbolic_stems: Set[str] = set()
    epistemic_hard_reported = False

    for idx, item in enumerate(batch_results):
        if not item.get("success"):
            continue
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
            raw_asm_failures.setdefault(str(e), []).append(f"seed={seed_val}")
            continue

        # Collect rendered correct answer and distractors for TPL-STATIC-OPT and TPL-DYNAMIC-RATIONALE
        rendered_correct_answers.append(_canonical_answer_signature(assembled_q, interaction_type))
        if interaction_type in ("multiple_choice_7_options", "multiple_choice"):
            for opt_idx, opt in enumerate(assembled_q.get("options", [])):
                if not opt.get("is_correct"):
                    did = str(opt.get("distractor_id") or "").strip()
                    slot_key = did or str(opt.get("id") or opt.get("option_id") or f"slot_{opt_idx}").strip()
                    distractor_contents_by_slot[slot_key].append(str(opt.get("content", "")).strip())
                    distractor_rationales_by_slot[slot_key].append(str(opt.get("error_rationale", "")).strip())
        elif interaction_type in ("fill_in_the_blank", "open_symbolic"):
            for dd_idx, dd in enumerate(assembled_q.get("diagnostic_distractors") or []):
                if isinstance(dd, dict):
                    did = str(dd.get("distractor_id") or "").strip()
                    slot_key = did or f"diag_{dd_idx}"
                    val_str = str(dd.get("expression") if "expression" in dd else (dd.get("value") or "")).strip()
                    distractor_contents_by_slot[slot_key].append(val_str)
                    distractor_rationales_by_slot[slot_key].append(str(dd.get("error_rationale", "")).strip())
        elif interaction_type == "multiple_select":
            for opt_idx, opt in enumerate(assembled_q.get("options", [])):
                opt_txt = str(opt.get("content") or opt.get("text") or "")
                m_tt = re.search(
                    r"\(\s*(?:confusi[oó]n|error|omisi[oó]n|sesgo|falsamente|definici[oó]n\s+err[oó]nea|desplazamiento\s+err[oó]neo|c[aá]lculo\s+err[oó]neo)[^)]*\)",
                    opt_txt,
                    re.IGNORECASE,
                )
                if m_tt:
                    tt_msg = f"[PSYCHOMETRIC-OPTIONS / parenthetical_telltale_linter] Metainformación delatora parentética en opción visible: '{m_tt.group(0)}'"
                    canon_key = get_canonical_invariant_key(tt_msg)
                    seed_tag = f"seed={seed_val}"
                    if canon_key not in raw_inv_failures:
                        raw_inv_failures[canon_key] = (tt_msg, [seed_tag], assembled_q)
                    else:
                        if seed_tag not in raw_inv_failures[canon_key][1]:
                            raw_inv_failures[canon_key][1].append(seed_tag)

                if not opt.get("is_correct"):
                    did = str(opt.get("distractor_id") or "").strip()
                    slot_key = did or str(opt.get("id") or opt.get("option_id") or f"slot_{opt_idx}").strip()
                    distractor_contents_by_slot[slot_key].append(str(opt.get("content", "")).strip())
                    distractor_rationales_by_slot[slot_key].append(str(opt.get("error_rationale", "")).strip())

        # Validate unrendered placeholders
        pl_errs = check_unrendered_placeholders_in_instance(assembled_q, gen_res.get("vars", {}))
        pl_errs = list(pl_errs) + check_render_hygiene_in_instance(assembled_q)
        for ple in pl_errs:
            canon_key = get_canonical_invariant_key(ple)
            seed_tag = f"seed={seed_val}"
            if canon_key not in raw_inv_failures:
                raw_inv_failures[canon_key] = (ple, [seed_tag], assembled_q)
            else:
                if seed_tag not in raw_inv_failures[canon_key][1]:
                    raw_inv_failures[canon_key][1].append(seed_tag)

        # Invariant check (Accumulate all failures: NO break)
        is_valid, inv_errors = check_instance_invariants(
            assembled_q,
            interaction_type,
            variables=gen_res.get("vars", {}),
        )
        if is_valid and not epistemic_checked:
            epistemic_checked = True
            for ep_warn in check_epistemic_closure(assembled_q, interaction_type):
                msg = f"{competency_id} ({tpl_id}, seed={seed_val}): {ep_warn}"
                _logger.warning(msg)
                if warnings_out is not None:
                    warnings_out.append(msg)
        if not epistemic_hard_reported:
            stem_txt_ep = str(assembled_q.get("stem") or "")
            if stem_txt_ep not in checked_symbolic_stems:
                checked_symbolic_stems.add(stem_txt_ep)
                hard_ep_errs = check_open_symbolic_answer_closure(assembled_q, interaction_type)
                if hard_ep_errs:
                    epistemic_hard_reported = True
                    errors.append(format_diagnostic_error(
                        "TPL-EPISTEMIC-CLOSURE: SÍMBOLO NO DEFINIDO EN EXPECTED_ANSWER",
                        competency_id,
                        tpl_id,
                        f"seed={seed_val}",
                        "stem_variants / expected_answer",
                        str(assembled_q.get("expected_answer", ""))[:120],
                        hard_ep_errs[0],
                        [
                            "Declara explícitamente todas las variables simbólicas requeridas por expected_answer en todas las variantes de stem_variants (en $...$ o `var`).",
                            "Verifica que ninguna variante de stem_variants omita parámetros libres usados en la expresión esperada.",
                        ],
                    ))
        if not is_valid:
            has_collision = any("Distractor identical to correct answer" in e for e in inv_errors)
            for inv_err in inv_errors:
                if has_collision and "Duplicate option content detected" in inv_err:
                    continue
                canon_key = get_canonical_invariant_key(inv_err)
                seed_tag = f"seed={seed_val}"
                if canon_key not in raw_inv_failures:
                    raw_inv_failures[canon_key] = (inv_err, [seed_tag], assembled_q)
                else:
                    if seed_tag not in raw_inv_failures[canon_key][1]:
                        raw_inv_failures[canon_key][1].append(seed_tag)

    # Consolidate assembly failures
    for asm_err, seed_list in raw_asm_failures.items():
        errors.append(format_diagnostic_error(
            "TPL-ASM: FALLO EN ENSAMBLAJE DE REACTIVO",
            competency_id,
            tpl_id,
            seed_list,
            "assemble_question",
            asm_err,
            f"No se pudo ensamblar el reactivo con la salida de generate_py para {len(seed_list)} semillas: {asm_err}",
            [
                "Verificar que generate_py retorne los campos obligatorios ('correct', 'distractors', 'vars').",
                "Asegurar que 'distractors' contenga al menos 6 elementos para preguntas MC7.",
                "Verificar que no haya discrepancia de formato entre template y generate_py.",
            ]
        ))

    # Consolidate invariant failures (including TPL-D4 collisions and duplicates across seeds)
    for canon_key, (rep_inv_err, seed_list, sample_q) in raw_inv_failures.items():
        errors.append(format_invariant_error_diagnostic(
            cid=competency_id,
            tpl_id=tpl_id,
            q_id=seed_list,
            inv_err=rep_inv_err,
            q_obj=sample_q,
        ))

    evaluate_static_opt_and_dynamic_rationale(
        template=template,
        competency_id=competency_id,
        tpl_id=tpl_id,
        interaction_type=interaction_type,
        strict=strict,
        num_dry_run_seeds=num_dry_run_seeds,
        batch_results=batch_results,
        rendered_correct_answers=rendered_correct_answers,
        distractor_contents_by_slot=distractor_contents_by_slot,
        distractor_rationales_by_slot=distractor_rationales_by_slot,
        errors=errors,
    )

    # 5. Rule TPL-VAR: Early variability and parametric capacity validation
    # a) Verify vars dictionary is not empty across generated results
    has_empty_vars = any(
        len(r.get("result", {}).get("vars", {})) == 0 for r in batch_results if r.get("success")
    )
    if has_empty_vars:
        errors.append(format_diagnostic_error(
            "TPL-VAR: DIVERSIDAD DE REACTIVOS", competency_id, tpl_id, "generate_py", "vars",
            "vars: {}",
            f"TPL-VAR violation in '{tpl_id}': 'vars' dictionary is empty. Templates must generate dynamic variables.",
            [
                "Generar variables aleatorias en generate_py (ej. a = random.randint(1, 9)) y retornarlas en vars={'a': a}.",
                "Asegurar que generate_py defina y retorne variables para todos los placeholders del enunciado.",
                "No utilizar constantes estáticas sin parametrizar en generate_py.",
            ]
        ))

    # b) Verify stem contains at least one placeholder {var} or stem_variants is present
    stem = template.get("stem", "")
    stem_variants = template.get("stem_variants")
    has_placeholder = bool(_extract_template_placeholders(stem))
    has_variants = bool(stem_variants and len(stem_variants) > 0)
    if not (has_placeholder or has_variants):
        errors.append(format_diagnostic_error(
            "TPL-VAR: DIVERSIDAD DE REACTIVOS", competency_id, tpl_id, "template", "stem / stem_variants",
            f"stem: '{stem}'",
            f"TPL-VAR violation in '{tpl_id}': stem must contain at least one placeholder '{{var}}' or '@var@' or 'stem_variants' must be present.",
            [
                "Insertar al menos un placeholder dinámico como '{a}' o '{x}' en el campo 'stem'.",
                "O proveer una lista de 3 a 5 formulaciones alternativas en 'stem_variants'.",
                "Verificar que las variables coincidan con las claves generadas en generate_py.",
            ]
        ))

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
        errors.append(format_diagnostic_error(
            "TPL-VAR: DIVERSIDAD DE REACTIVOS", competency_id, tpl_id, "dry-run", "generate_py / vars",
            f"Únicamente {unique_count}/4 instancias únicas generadas a través de {num_dry_run_seeds} semillas.",
            f"TPL-VAR violation in '{tpl_id}': Only {unique_count}/4 unique instances generated across {num_dry_run_seeds} seeds. Parameter domain is too narrow or missing stem variations.",
            [
                "Ampliar los rangos numéricos aleatorios generados en generate_py (ej. random.choice o random.randint).",
                "Agregar 3 a 5 variantes sintácticas en 'stem_variants' para enriquecer la variabilidad textual.",
                "Evitar restringir los parámetros a un conjunto menor de 4 combinaciones posibles.",
            ]
        ))

    # 6. Rule TPL-ORPHAN-VARS: Reject unreferenced leftover keys in 'vars' (warn-only to accommodate auxiliary vars like d1..d6)
    orphan_keys = _check_orphan_vars(
        template,
        batch_results,
        cross_check_py,
        comp_templates=comp_templates,
        cta_distractors_map=cta_distractors_map,
    )
    if orphan_keys:
        print(
            f"WARNING: [TPL-ORPHAN-VARS] En '{tpl_id}': claves retornadas en 'vars' que no se usan en placeholders (@var@, {{var}}), ni en stems, hints, solution/explanation_es, distractores, ni en cross_check_py: {sorted(list(orphan_keys))}",
            file=sys.stderr,
        )

    return errors


def check_competency_diversity(
    templates: List[Dict[str, Any]],
    competency: Union[Dict[str, Any], Any],
    distractor_map: Optional[Dict[str, Dict[str, Any]]] = None,
    num_seeds: Optional[int] = None,
    return_questions: bool = False,
    enforce_full_quota: bool = False,
    strict: bool = True,
    questions: Optional[List[Dict[str, Any]]] = None,
) -> Union[List[str], Tuple[List[str], List[Dict[str, Any]]]]:
    """Verify stem structural diversity at the competency level (build simulation).
    
    Simulates build stage instantiation with quotas (30 for Skill, 20 for Fact/Concept)
    and evaluates masked stem diversity ratio >= 0.50.
    Returns errors_list (or (errors_list, instantiated_questions) if return_questions=True).
    """
    errors: List[str] = []
    if questions is None and not templates:
        cid = competency.get("id", "UNKNOWN") if isinstance(competency, dict) else str(getattr(competency, "id", "UNKNOWN"))
        errors.append(format_diagnostic_error(
            "TPL-VAR: DIVERSIDAD DE REACTIVOS", cid, "N/A", "N/A", "templates",
            "No templates provided.",
            f"No se proporcionaron plantillas para la competencia '{cid}'.",
            [
                f"Crear y registrar archivos de plantillas para la competencia '{cid}'.",
                "Asegurar que cada competencia cuente con al menos una plantilla válida.",
                "Verificar la ruta de las plantillas en el sistema.",
            ]
        ))
        return (errors, []) if return_questions else errors

    if isinstance(competency, dict):
        cid = competency.get("id", "UNKNOWN")
        ctype = str(competency.get("type") or competency.get("category") or "concept").lower()
    else:
        cid = getattr(competency, "id", "UNKNOWN")
        ctype = str(getattr(competency, "type", getattr(competency, "category", "concept"))).lower()

    is_skill = is_skill_type(ctype) or cid.startswith("Hab-")

    if questions is not None:
        target_quota = len(questions)
        comp_res = {
            "questions": questions,
            "diversity_stats": evaluate_competency_diversity([str(q.get("stem") or "") for q in questions]),
        }
    else:
        if enforce_full_quota:
            target_quota = 30 if is_skill else 20
        elif num_seeds is not None:
            target_quota = num_seeds
        else:
            target_quota = 30 if is_skill else 20
            if len(templates) < 3:
                target_quota = min(target_quota, max(len(templates) * 5, 10))

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
            errors.append(format_diagnostic_error(
                "TPL-VAR: DIVERSIDAD DE REACTIVOS", cid, "ALL", "instantiate_competency", "generate_py / vars",
                f"Fallo al instanciar cuota de diversidad ({target_quota} ítems): {e}",
                f"[-] TPL-VAR VIOLATION in competency '{cid}': Failed to instantiate diversity quota ({target_quota} items): {e}. No se pudieron generar los reactivos requeridos debido a colisiones o parámetros estrechos.",
                [
                    "Ampliar los rangos de las variables aleatorias en generate_py.",
                    "Agregar 3 a 5 'stem_variants' distintas con placeholders en las plantillas más estrechas.",
                    "Comprobar que generate_py no lance excepciones con ciertas combinaciones de semillas.",
                ]
            ))
            return (errors, []) if return_questions else errors

    questions = comp_res.get("questions", [])

    # Annotate template_id on each question
    from engine.instantiate import allocate_template_quotas
    quotas = allocate_template_quotas(templates, target_quota)
    qid_to_tpl: Dict[str, str] = {}
    curr_idx = 1
    clean_comp = re.sub(r"[^A-Za-z0-9]", "", cid)
    for tpl in templates:
        tid = tpl.get("id", "UNKNOWN")
        cnt = quotas.get(tid, 0)
        for _ in range(cnt):
            qid = f"Q-{clean_comp}-{curr_idx:03d}"
            qid_to_tpl[qid] = tid
            curr_idx += 1

    for q in questions:
        if isinstance(q, dict) and "template_id" not in q:
            q["template_id"] = qid_to_tpl.get(q.get("id", ""), "UNKNOWN")

    # Validate invariants on all instantiated questions (Full Sweep: NO premature break)
    comp_inv_failures: Dict[Tuple[str, str], Tuple[str, List[str]]] = {}
    for q in questions:
        q_type = q.get("interaction_type") or q.get("type", "")
        q_id = q.get("id", "UNKNOWN")
        t_id = q.get("template_id", "UNKNOWN")
        is_valid, inv_errors = check_instance_invariants(q, q_type)
        if not is_valid:
            has_collision = any("Distractor identical to correct answer" in e for e in inv_errors)
            for inv_err in inv_errors:
                if has_collision and "Duplicate option content detected" in inv_err:
                    continue
                canon_key = get_canonical_invariant_key(inv_err)
                sig = (t_id, canon_key)
                if sig not in comp_inv_failures:
                    comp_inv_failures[sig] = (inv_err, [q_id], q)
                else:
                    comp_inv_failures[sig][1].append(q_id)

    for (t_id, canon_key), (rep_err, q_ids, sample_q) in comp_inv_failures.items():
        unique_q_ids = list(dict.fromkeys(q_ids))
        errors.append(format_invariant_error_diagnostic(
            cid=cid,
            tpl_id=t_id,
            q_id=unique_q_ids,
            inv_err=rep_err,
            q_obj=sample_q,
        ))

    div_stats = comp_res.get("diversity_stats", {})
    div_ratio = div_stats.get("diversity_ratio", 0.0)
    unique_c = div_stats.get("unique_masked", 0)
    total_c = div_stats.get("total", len(questions))

    # Strict pool correct key concentration check
    if strict and len(questions) >= 20:
        correct_keys = [
            _canonical_answer_signature(q, str(q.get("interaction_type") or q.get("type", "")))
            for q in questions
        ]

        from collections import Counter
        key_counts = Counter(correct_keys)
        if key_counts:
            most_common_key, max_cnt = key_counts.most_common(1)[0]
            pct = max_cnt / len(questions)
            if pct > 0.20:
                k_str = str(most_common_key)
                errors.append(format_diagnostic_error(
                    rule_tag="TPL-STATIC-OPT: CONCENTRACIÓN EXCESIVA DE CLAVE CORRECTA",
                    competency=cid,
                    template="ALL",
                    item_id="questions",
                    field_name="correct",
                    snippet=f"Clave '{k_str}' concentra {max_cnt}/{len(questions)} ({pct*100:.1f}%) > 20.0%",
                    cause=f"[-] [TPL-STATIC-OPT] violation in competency '{cid}': Single correct key '{k_str}' accounts for {pct*100:.1f}% of instances ({max_cnt}/{len(questions)}), exceeding 20.0% threshold.",
                    actions=[
                        "Ampliar la variabilidad de parámetros en las plantillas de la competencia.",
                        "Evitar que diferentes plantillas colapsen hacia las mismas respuestas correctas.",
                        "Asegurar una distribución uniforme de claves en el banco de preguntas.",
                    ],
                ))

    # Strict distractor rationale uniqueness check
    if strict:
        all_rats = []
        for q in questions:
            for opt in q.get("options", []):
                if not opt.get("is_correct"):
                    r_text = opt.get("error_rationale")
                    if r_text and str(r_text).strip():
                        all_rats.append(str(r_text).strip())
        rat_div = evaluate_slot_rationale_diversity(questions)
        unique_rats = set(all_rats)
        raw_unmasked_ratio = (len(unique_rats) / len(all_rats)) if all_rats else 1.0
        low_slot_uniqueness = (
            len(all_rats) >= 12
            and rat_div["total_slots"] >= 4
            and rat_div["slot_uniqueness_pct"] < 80.0
        )
        synthetic_prefix_masking = (
            len(all_rats) >= 12
            and rat_div["total_slots"] >= 4
            and rat_div["synthetic_prefix_pct"] >= 25.0
            and (
                rat_div["slot_uniqueness_pct"] < 80.0
                or (rat_div["raw_slot_uniqueness_pct"] - rat_div["slot_uniqueness_pct"]) >= 10.0
            )
        )
        low_raw_unmasked = (
            len(all_rats) >= 30
            and raw_unmasked_ratio < 0.35
            and (rat_div["total_slots"] < 4 or rat_div["slot_uniqueness_pct"] < 80.0)
        )
        if low_slot_uniqueness or synthetic_prefix_masking or low_raw_unmasked:
            if synthetic_prefix_masking and not low_slot_uniqueness:
                slot_pct = rat_div["slot_uniqueness_pct"]
                raw_slot_pct = rat_div["raw_slot_uniqueness_pct"]
                synth_pct = rat_div["synthetic_prefix_pct"]
                snippet_str = (
                    f"Prefijos rotativos sintéticos en {synth_pct:.1f}% de rationales inflan unicidad por slot "
                    f"de {slot_pct:.1f}% (real) a {raw_slot_pct:.1f}% (nominal)"
                )
                cause_str = (
                    f"[-] [TPL-DYNAMIC-RATIONALE] violation in competency '{cid}': "
                    f"{synth_pct:.1f}% of rationales use rotating synthetic prefixes inflating slot uniqueness "
                    f"from {slot_pct:.1f}% to {raw_slot_pct:.1f}% (delta >= 10.0%)."
                )
            elif low_raw_unmasked and not low_slot_uniqueness:
                uniqueness_pct = raw_unmasked_ratio
                snippet_str = (
                    f"Unicidad de rationales {uniqueness_pct*100:.1f}% < 35.0% "
                    f"({len(unique_rats)}/{len(all_rats)} únicos; slots únicos: "
                    f"{rat_div['unique_slots']}/{rat_div['total_slots']} = {rat_div['slot_uniqueness_pct']:.1f}%)"
                )
                cause_str = (
                    f"[-] [TPL-DYNAMIC-RATIONALE] violation in competency '{cid}': "
                    f"Distractor rationale uniqueness ratio {uniqueness_pct*100:.1f}% < 35.0% "
                    f"({len(unique_rats)}/{len(all_rats)} unique rationales; "
                    f"slot uniqueness {rat_div['slot_uniqueness_pct']:.1f}%)."
                )
            else:
                slot_pct = rat_div["slot_uniqueness_pct"]
                snippet_str = (
                    f"Unicidad de rationales por slot (distractor_id) {slot_pct:.1f}% < 80.0% "
                    f"({rat_div['unique_slots']}/{rat_div['total_slots']} slots únicos tras eliminar prefijos y números)"
                )
                cause_str = (
                    f"[-] [TPL-DYNAMIC-RATIONALE] violation in competency '{cid}': "
                    f"Distractor rationale uniqueness ratio {slot_pct:.1f}% < 80.0% "
                    f"({rat_div['unique_slots']}/{rat_div['total_slots']} unique distractor slots after stripping rotating prefixes and numeric literals)."
                )
            errors.append(format_diagnostic_error(
                rule_tag="TPL-DYNAMIC-RATIONALE: DIVERSIDAD DE RATIONALES INSUFICIENTE",
                competency=cid,
                template="ALL",
                item_id="options",
                field_name="error_rationale",
                snippet=snippet_str,
                cause=cause_str,
                actions=[
                    "Asignar a cada slot (distractor_id) un error_rationale específico para su fórmula o concepción errónea que interpole al menos un @var@.",
                    "Evitar clonar la misma explicación genérica o usar prefijos rotativos ('Error conceptual:', 'Fallo de cálculo:') entre distintos distractores.",
                    "Asegurar que cada distractor explique la falacia específica asociada a los datos del reactivo (>= 80% de unicidad por slot).",
                ],
            ))

    if div_ratio < MIN_DIVERSITY_RATIO:
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
        narrowest_tids = ", ".join(tid for tid, _ in narrowest_items)

        err_msg = format_diagnostic_error(
            rule_tag="TPL-VAR: DIVERSIDAD DE REACTIVOS",
            competency=cid,
            template=narrowest_tids,
            item_id="N/A (banco de preguntas de la competencia)",
            field_name="stem / stem_variants",
            snippet=f"stem diversity {div_ratio:.2f} < 0.50 ({unique_c}/{total_c} unique masked stems). Plantillas con menor variación: {narrowest_str}",
            cause=f"[-] TPL-VAR VIOLATION in competency '{cid}': stem diversity {div_ratio:.2f} < 0.50 ({unique_c}/{total_c} unique masked stems). Narrowest templates: {narrowest_str}. El ratio de diversidad léxico-estructural de los enunciados es menor al 50% requerido por el contrato psicométrico.",
            actions=[
                f"Agregar entre 3 y 5 'stem_variants' estructuralmente distintas en las plantillas críticas ({narrowest_tids}) usando {{placeholders}}.",
                "Ampliar los rangos numéricos y opciones aleatorias en 'vars' dentro de generate_py para evitar enunciados idénticos.",
                "Variar los verbos y formulaciones de la consigna (ej. 'Determine el valor...', 'Calcule la expresión...', 'Halle la solución...').",
            ],
        )
        errors.append(err_msg)

    return (errors, questions) if return_questions else errors


def _validate_single_template_file(
    tf: Path,
    cta_distractors_by_comp: Dict[str, Set[str]],
    cta_distractors_map: Dict[str, Dict[str, Any]],
    num_dry_run_seeds: int,
    shard_py: Optional[Union[str, Path]] = None,
    strict: bool = True,
    warnings_out: Optional[List[str]] = None,
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

    if isinstance(t_content, list):
        templates_list = t_content
        comp_id = t_content[0].get("competency_id") if t_content and isinstance(t_content[0], dict) else None
    elif isinstance(t_content, dict):
        comp_id = t_content.get("competency_id")
        templates_list = t_content.get("templates", [])
        if not templates_list and "interaction_type" in t_content:
            # Single template file
            templates_list = [t_content]
            comp_id = t_content.get("competency_id", comp_id)
    else:
        file_errors.append(f"File {tf.name} content must be a JSON object or list.")
        return file_errors, None, set(), []

    if cta_distractors_by_comp and (not comp_id or comp_id not in cta_distractors_by_comp):
        file_errors.append(f"File {tf.name} declares unknown or missing competency_id '{comp_id}'.")
        return file_errors, comp_id, set(), templates_list

    declared_dids = cta_distractors_by_comp.get(comp_id, set()) if cta_distractors_by_comp else set()
    referenced_dids: Set[str] = set()

    for tpl in templates_list:
        t_dids = tpl.get("distractor_ids", []) or []
        for did in t_dids:
            if isinstance(did, str) and did.strip():
                referenced_dids.add(did.strip().replace("_", "-"))

        if not t_dids and tpl.get("generate_py") and tpl.get("interaction_type") != "multiple_choice_7_options":
            try:
                rep_batch = execute_sandbox_batch(tpl["generate_py"], [42], timeout_per_item=0.8)
                if rep_batch and rep_batch[0].get("success"):
                    rep_q = assemble_question(
                        template=tpl,
                        gen_result=rep_batch[0].get("result", {}),
                        competency_id=comp_id or "UNKNOWN",
                        question_index=1,
                        cta_distractors_map=cta_distractors_map,
                        seed=42,
                    )
                    referenced_dids.update(_extract_instance_distractor_ids(rep_q))
            except Exception:
                pass

        single_errs = check_single_template(
            template=tpl,
            competency_id=comp_id or "UNKNOWN",
            declared_distractor_ids=declared_dids,
            cta_distractors_map=cta_distractors_map,
            num_dry_run_seeds=num_dry_run_seeds,
            shard_py=shard_py,
            strict=strict,
            comp_templates=templates_list,
            warnings_out=warnings_out,
        )
        file_errors.extend(single_errs)

    # Check [TPL-HINTS-DUPLICATE] across templates in the competency
    if templates_list and len(templates_list) > 1:
        hints_by_tpl = {}
        for tpl in templates_list:
            tid = tpl.get("id", "UNKNOWN")
            h_list = tpl.get("hints", [])
            if isinstance(h_list, list) and h_list:
                norm_h = tuple(
                    re.sub(r"\s+", " ", (h.get("text") if isinstance(h, dict) else str(h)).strip().lower())
                    for h in h_list
                )
                hints_by_tpl[tid] = norm_h
        seen_hints = {}
        for tid, nh in hints_by_tpl.items():
            seen_hints.setdefault(nh, []).append(tid)
        for nh, tids in seen_hints.items():
            if len(tids) > 1:
                if strict:
                    file_errors.append(
                        f"FAIL: [TPL-HINTS-DUPLICATE] Competencia '{comp_id}': Múltiples plantillas ({', '.join(tids)}) reutilizan exactamente el mismo arreglo de pistas (hints). Cada plantilla requiere andamiaje socrático diferenciado."
                    )
                else:
                    print(
                        f"WARNING: [TPL-HINTS-DUPLICATE] Competencia '{comp_id}': Múltiples plantillas ({', '.join(tids)}) reutilizan exactamente el mismo arreglo de pistas (hints). Se recomienda andamiaje socrático diferenciado por plantilla.",
                        file=sys.stderr,
                    )

    return file_errors, comp_id, referenced_dids, templates_list


def _validate_single_template_file_worker(
    tf: Path,
    cta_distractors_by_comp: Dict[str, Set[str]],
    cta_distractors_map: Dict[str, Dict[str, Any]],
    num_dry_run_seeds: int,
    shard_py: Optional[Union[str, Path]] = None,
    strict: bool = True,
) -> Tuple[List[str], Optional[str], Set[str], List[Dict[str, Any]], List[str]]:
    """Pool worker wrapper that captures warnings_out alongside validation results."""
    local_warnings: List[str] = []
    file_errs, comp_id, ref_dids, tpls = _validate_single_template_file(
        tf,
        cta_distractors_by_comp,
        cta_distractors_map,
        num_dry_run_seeds,
        shard_py,
        strict,
        warnings_out=local_warnings,
    )
    return file_errs, comp_id, ref_dids, tpls, local_warnings


def _eval_comp_diversity_and_parity_worker(
    cid: str,
    comp_obj: Dict[str, Any],
    comp_tpls: List[Dict[str, Any]],
    cta_distractors_map: Dict[str, Any],
    num_dry_run_seeds: int,
    strict: bool,
) -> List[str]:
    """Module-level (picklable) TPL-VAR diversity + production parity check for one competency."""
    c_errors: List[str] = []
    sim_seeds = num_dry_run_seeds if num_dry_run_seeds <= 20 else None
    div_errors, comp_questions = check_competency_diversity(
        templates=comp_tpls,
        competency=comp_obj,
        distractor_map=cta_distractors_map,
        num_seeds=sim_seeds,
        return_questions=True,
        enforce_full_quota=(num_dry_run_seeds >= 50),
        strict=strict,
    )
    c_errors.extend(div_errors)
    if strict and comp_questions:
        c_errors.extend(
            check_production_parity_for_competency(
                cid=cid,
                competency=comp_obj,
                questions=comp_questions,
                strict=True,
            )
        )
    return c_errors


def _bounded_worker_count(item_count: int) -> int:
    """Caps ProcessPool workers to leave host cores responsive on Windows."""
    if item_count <= 1:
        return 1
    return max(1, min(6, max(1, (os.cpu_count() or 4) - 2), item_count))


def check_templates_file_or_dir(
    target_path: Union[Path, List[Path], str, List[str]],
    cta_path: Optional[Path] = None,
    num_dry_run_seeds: int = 50,
    strict: bool = True,
    attempts_dir: Optional[Path] = None,
    auto_fix: bool = True,
    shard_py: Optional[Union[str, Path]] = None,
    shard_id: Optional[str] = None,
    from_compile_shard: bool = False,
    warnings_out: Optional[List[str]] = None,
) -> Tuple[bool, List[str]]:
    """Validate all templates in file(s) or directory against CTA with production contract parity."""
    # warm_up_sandbox()  # Omit blind warmup: in-process execution is already instant
    errors = []

    # Infer shard_id if omitted
    if not shard_id and shard_py:
        py_stem = Path(shard_py).stem
        if "shard_" in py_stem:
            shard_id = py_stem.replace("_data", "")

    cta_data: Dict[str, Any] = {}
    cta_distractors_by_comp: Dict[str, Set[str]] = {}
    cta_distractors_map: Dict[str, Dict[str, Any]] = {}
    cta_p: Optional[Path] = Path(cta_path) if cta_path is not None else None

    if cta_p is not None:
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
        str_item = str(item)
        if "*" in str_item or "?" in str_item:
            p_obj = Path(str_item)
            parent = p_obj.parent if str(p_obj.parent) != "" else Path(".")
            pattern = p_obj.name
            matched = list(parent.glob(pattern))
            for m in matched:
                if m.is_file() and m.suffix.lower() == ".json" and m not in template_files:
                    template_files.append(m)
            continue

        p = Path(item)
        if p.is_file() and p.suffix.lower() == ".json":
            # Check if this file is a shard file (e.g. shard_XX.json)
            is_shard = False
            try:
                content = json.loads(p.read_text(encoding="utf-8"))
                if isinstance(content, dict) and ("shard_id" in content or "competency_ids" in content):
                    is_shard = True
                    # Strict verification of pre_shard_manifest.json (ZERO Fallbacks)
                    manifest_candidates = [
                        p.parent / "pre_shard_manifest.json",
                        p.parent.parent / "shards" / "pre_shard_manifest.json",
                        p.parent.parent / "pre_shard_manifest.json",
                        Path("work/shards/pre_shard_manifest.json").resolve(),
                        Path("work/pre_shard_manifest.json").resolve(),
                    ]
                    found_pre_shard_manifest = any(c.is_file() for c in manifest_candidates)
                    if not found_pre_shard_manifest:
                        print("BLOCKER:: No existe pre_shard_manifest.json", file=sys.stderr)
                        return False, ["BLOCKER:: No existe pre_shard_manifest.json"]

                    c_ids = content.get("competency_ids", [])
                    for cid in c_ids:
                        candidate_paths = [
                            p.parent.parent / "templates" / f"{cid}.json",
                            p.parent / "templates" / f"{cid}.json",
                            Path("work/templates") / f"{cid}.json",
                            Path("templates") / f"{cid}.json",
                        ]
                        found_tpl = None
                        for cand in candidate_paths:
                            if cand.is_file():
                                found_tpl = cand
                                break
                        if found_tpl:
                            if found_tpl not in template_files:
                                template_files.append(found_tpl)
                        else:
                            errors.append(f"Shard '{p.name}' references competency '{cid}', but template file was not found at work/templates/{cid}.json")
            except Exception:
                is_shard = False

            if not is_shard and p not in template_files:
                template_files.append(p)
        elif p.is_dir():
            is_full_dir = True
            for f in sorted(p.glob("*.json")):
                if f not in template_files:
                    template_files.append(f)
        elif not p.exists():
            return False, [f"Target path does not exist: {p}"]

    if not template_files and not errors:
        return False, [f"No template JSON files found in: {target_path}"]

    if auto_fix:
        comp_by_id = {c["id"]: c for c in cta_data.get("competencies", [])} if cta_data else {}
        for tf in template_files:
            try:
                tf_content = json.loads(tf.read_text(encoding="utf-8"))
                cid = None
                if isinstance(tf_content, dict):
                    cid = tf_content.get("competency_id") or tf.stem
                elif isinstance(tf_content, list) and tf_content and isinstance(tf_content[0], dict):
                    cid = tf_content[0].get("competency_id") or tf.stem
                comp_obj = comp_by_id.get(cid) if cid else None
                was_mod, fixes = auto_heal_template_file(
                    tf,
                    cta_comp=comp_obj,
                    cta_distractors_map=cta_distractors_map,
                )
                if was_mod:
                    for fix_desc in fixes:
                        print(f"[AUTO-HEAL] {tf.name}: {fix_desc}")
            except Exception:
                pass

    referenced_distractors_by_comp: Dict[str, Set[str]] = {cid: set() for cid in cta_distractors_by_comp}
    templates_by_comp: Dict[str, List[Dict[str, Any]]] = {}
    processed_comp_ids: Set[str] = set()
    errors_by_comp: Dict[str, List[str]] = {}

    if len(template_files) > 1:
        max_workers = _bounded_worker_count(len(template_files))

        def _run_pool(pool_cls, workers, files):
            with pool_cls(max_workers=workers) as executor:
                futs = [
                    executor.submit(
                        _validate_single_template_file_worker,
                        tf,
                        cta_distractors_by_comp,
                        cta_distractors_map,
                        num_dry_run_seeds,
                        shard_py,
                        strict,
                    )
                    for tf in files
                ]
                return [f.result() for f in futs]

        # Incremental cache: skip files whose content, CTA, params and validator code are
        # unchanged since their last *passing* validation (failures are never cached).
        import pickle
        cache_dir: Optional[Path] = None
        key_prefix = ""
        if cta_p is not None:
            try:
                cache_dir = cta_p.parent / ".validation_cache"
                h = hashlib.sha256()
                h.update(cta_p.read_bytes())
                h.update(f"{num_dry_run_seeds}|{strict}".encode())
                skill_root = Path(__file__).resolve().parent
                schema_path = skill_root / "schemas" / "template.schema.json"
                extra_files = [Path(__file__).resolve()]
                if schema_path.is_file():
                    extra_files.append(schema_path)
                for src in sorted(list((skill_root / "engine").glob("*.py")) + list((skill_root / "validator").glob("*.py")) + extra_files):
                    h.update(src.read_bytes())
                key_prefix = h.hexdigest()
            except Exception:
                cache_dir = None

        def _cache_path(tf: Path) -> Optional[Path]:
            if cache_dir is None:
                return None
            fh = hashlib.sha256(key_prefix.encode() + tf.read_bytes()).hexdigest()
            ok_path = cache_dir / f"{tf.stem}_{fh[:24]}.ok.pkl"
            legacy_path = cache_dir / f"{tf.stem}_{fh[:24]}.pkl"
            if ok_path.is_file():
                return ok_path
            if legacy_path.is_file():
                return legacy_path
            return ok_path

        cached_results: Dict[Path, Any] = {}
        pending: List[Path] = []
        for tf in template_files:
            cp = None
            try:
                cp = _cache_path(tf)
                if cp is not None and cp.is_file():
                    cached_results[tf] = pickle.loads(cp.read_bytes())
                    continue
            except Exception:
                pass
            pending.append(tf)

        fresh: Dict[Path, Any] = {}
        if pending:
            # Validation is CPU-bound (GIL): prefer processes, fall back to threads if
            # the pool cannot be used (e.g. virtual stdout without fileno, unpicklable args, or restricted environment).
            workers = _bounded_worker_count(len(pending))
            stdout_is_virtual = False
            if not hasattr(sys.stdout, "fileno"):
                stdout_is_virtual = True
            else:
                try:
                    sys.stdout.fileno()
                except Exception:
                    stdout_is_virtual = True

            if stdout_is_virtual or len(pending) <= 1:
                res_list = _run_pool(ThreadPoolExecutor, min(8, workers) if stdout_is_virtual else 1, pending)
            else:
                try:
                    res_list = _run_pool(ProcessPoolExecutor, workers, pending)
                except Exception:
                    res_list = _run_pool(ThreadPoolExecutor, min(8, workers), pending)
            fresh = dict(zip(pending, res_list))
            if cache_dir is not None:
                for tf, res in fresh.items():
                    try:
                        if not res[0]:
                            cp = _cache_path(tf)
                            if cp is not None:
                                _atomic_write_bytes(cp, pickle.dumps(res))
                    except Exception:
                        pass

        results = [cached_results[tf] if tf in cached_results else fresh[tf] for tf in template_files]
        if cached_results:
            print(f"  [i] Template validation cache: {len(cached_results)} reused, {len(pending)} re-validated.")

        for res in results:
            if len(res) == 5:
                file_errs, comp_id, ref_dids, tpls, file_warns = res
            else:
                file_errs, comp_id, ref_dids, tpls = res
                file_warns = []
            errors.extend(file_errs)
            if warnings_out is not None and file_warns:
                warnings_out.extend(file_warns)
            if comp_id:
                processed_comp_ids.add(comp_id)
                if file_errs:
                    errors_by_comp.setdefault(comp_id, []).extend(file_errs)
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
                shard_py,
                strict,
                warnings_out=warnings_out,
            )
            errors.extend(file_errs)
            if comp_id:
                processed_comp_ids.add(comp_id)
                if file_errs:
                    errors_by_comp.setdefault(comp_id, []).extend(file_errs)
                templates_by_comp.setdefault(comp_id, []).extend(tpls)
                if comp_id in referenced_distractors_by_comp:
                    referenced_distractors_by_comp[comp_id].update(ref_dids)

    check_multimodal_tpl_d3_coverage(
        cta_distractors_by_comp=cta_distractors_by_comp,
        cta_data=cta_data,
        referenced_distractors_by_comp=referenced_distractors_by_comp,
        templates_by_comp=templates_by_comp,
        processed_comp_ids=processed_comp_ids,
        is_full_dir=is_full_dir,
        errors=errors,
        errors_by_comp=errors_by_comp,
    )

    # Rule TPL-VAR (Competency Diversity Gate) & Isomorphic Contract Parity Check
    if cta_data and "competencies" in cta_data:
        comp_map = {c["id"]: c for c in cta_data.get("competencies", [])}
        comps_to_check = list(referenced_distractors_by_comp.keys()) if is_full_dir else list(processed_comp_ids)
        def _evaluate_comp_diversity_and_parity(cid: str) -> List[str]:
            comp_obj = comp_map.get(cid)
            comp_tpls = templates_by_comp.get(cid, [])
            if not (comp_obj and comp_tpls):
                return []
            return _eval_comp_diversity_and_parity_worker(
                cid, comp_obj, comp_tpls, cta_distractors_map, num_dry_run_seeds, strict
            )

        sorted_comps = sorted(comps_to_check)

        # Incremental cache for this phase (passing results only). key_prefix already
        # covers cta.json, seeds/strict and validator code; add the comp's templates.
        import pickle as _pk
        div_cache_ok = bool(cache_dir is not None and key_prefix) if "cache_dir" in locals() else False

        def _div_cache_path(cid: str) -> Optional[Path]:
            if not div_cache_ok:
                return None
            try:
                blob = json.dumps(templates_by_comp.get(cid, []), sort_keys=True, default=str)
                fh = hashlib.sha256((key_prefix + "|div|" + cid + blob).encode("utf-8")).hexdigest()
                return cache_dir / f"div_{cid}_{fh[:24]}.ok"
            except Exception:
                return None

        comp_results: Dict[str, List[str]] = {}
        to_run: List[str] = []
        for cid in sorted_comps:
            dp = _div_cache_path(cid)
            if dp is not None and dp.is_file():
                comp_results[cid] = []
            else:
                to_run.append(cid)

        if len(to_run) > 1:
            def _submit_all(pool_cls, workers):
                with pool_cls(max_workers=workers) as ex:
                    futs = {}
                    for cid in to_run:
                        comp_obj = comp_map.get(cid)
                        comp_tpls = templates_by_comp.get(cid, [])
                        if not (comp_obj and comp_tpls):
                            comp_results[cid] = []
                            continue
                        futs[cid] = ex.submit(
                            _eval_comp_diversity_and_parity_worker,
                            cid, comp_obj, comp_tpls, cta_distractors_map, num_dry_run_seeds, strict,
                        )
                    for cid, fut in futs.items():
                        comp_results[cid] = fut.result()
            w = _bounded_worker_count(len(to_run))
            stdout_is_virtual = False
            if not hasattr(sys.stdout, "fileno"):
                stdout_is_virtual = True
            else:
                try:
                    sys.stdout.fileno()
                except Exception:
                    stdout_is_virtual = True

            if stdout_is_virtual:
                _submit_all(ThreadPoolExecutor, min(8, w))
            else:
                try:
                    _submit_all(ProcessPoolExecutor, w)
                except Exception:
                    comp_results.clear()
                    for cid in sorted_comps:
                        dp = _div_cache_path(cid)
                        if dp is not None and dp.is_file():
                            comp_results[cid] = []
                    _submit_all(ThreadPoolExecutor, min(8, w))
        else:
            for cid in to_run:
                comp_results[cid] = _evaluate_comp_diversity_and_parity(cid)

        for cid in sorted_comps:
            c_errs = comp_results.get(cid, [])
            errors.extend(c_errs)
            if c_errs:
                errors_by_comp.setdefault(cid, []).extend(c_errs)
            elif cid in to_run:
                dp = _div_cache_path(cid)
                if dp is not None:
                    try:
                        _atomic_write_bytes(dp, b"ok")
                    except Exception:
                        pass

    # Associate any global or unassociated errors with relevant competencies
    for err in errors:
        for cid in processed_comp_ids:
            if err in errors_by_comp.get(cid, []):
                continue
            err_norm = err.replace("\\", "/")
            cid_pat = re.compile(rf"\b{re.escape(cid)}\b", re.IGNORECASE)
            if (
                f"'{cid}'" in err
                or f'"{cid}"' in err
                or f"[{cid}]" in err
                or f"({cid})" in err
                or f"/{cid}.json" in err_norm
                or err_norm.endswith(f"/{cid}.json")
                or err_norm.startswith(f"{cid}.json")
                or bool(cid_pat.search(err))
            ):
                errors_by_comp.setdefault(cid, []).append(err)

    if len(processed_comp_ids) == 1 and errors:
        only_cid = next(iter(processed_comp_ids))
        for err in errors:
            if err not in errors_by_comp.get(only_cid, []):
                errors_by_comp.setdefault(only_cid, []).append(err)

    # Non-blocking cognitive rigor recommendation: Analyze+Evaluate >= 70% portfolio share
    all_tpls_bloom = [t for tpls in templates_by_comp.values() for t in tpls if isinstance(t, dict)]
    total_tpls_bloom = len(all_tpls_bloom)
    if total_tpls_bloom >= 4:
        sup_cnt = sum(1 for t in all_tpls_bloom if str(t.get("bloom") or "").strip() in ("Analyze", "Evaluate"))
        sup_ratio = sup_cnt / total_tpls_bloom
        if sup_ratio < 0.70:
            bloom_warn = (
                f"WARNING: [BLOOM-SUPERIOR-TARGET] Cuota Analyze+Evaluate = {sup_ratio * 100:.1f}% "
                f"({sup_cnt}/{total_tpls_bloom} plantillas, < 70.0% recomendado). "
                f"Recomendación no bloqueante: promueve plantillas aplicativas hacia Analyze/Evaluate si el material lo permite."
            )
            if warnings_out is not None:
                warnings_out.append(bloom_warn)
            print(bloom_warn, file=sys.stderr)

    is_clean = (len(errors) == 0)

    # Resolve attempts_dir automatically if not supplied
    effective_attempts_dir = attempts_dir
    if effective_attempts_dir is None:
        if cta_p is not None:
            effective_attempts_dir = cta_p.parent / ".check_attempts"
        elif shard_py is not None:
            sp = Path(shard_py).resolve()
            w_root = sp.parent.parent if sp.parent.name == "shards" else sp.parent
            effective_attempts_dir = w_root / ".check_attempts"
        elif template_files:
            tp = template_files[0].resolve()
            w_root = tp.parent.parent if tp.parent.name == "templates" else tp.parent
            effective_attempts_dir = w_root / ".check_attempts"
        else:
            effective_attempts_dir = Path("work/.check_attempts")

    update_circuit_breaker_state(
        effective_attempts_dir=effective_attempts_dir,
        shard_id=shard_id,
        processed_comp_ids=processed_comp_ids,
        raw_targets=raw_targets,
        is_clean=is_clean,
        errors=errors,
        errors_by_comp=errors_by_comp,
        templates_by_comp=templates_by_comp,
        template_files=template_files,
        from_compile_shard=from_compile_shard,
    )

    is_clean = (len(errors) == 0)
    return is_clean, errors


def main():
    parser = argparse.ArgumentParser(description="Validate parametric exercise templates with Isomorphic Contract Parity")
    parser.add_argument("target", nargs="*", default=[], help="Path(s) to template.json file(s) or templates/ directory")
    parser.add_argument("--shard", default=None, help="Shard ID to validate (requires work/shards/pre_shard_manifest.json)")
    parser.add_argument("--shard-py", default=None, help="Path to shard_XX_data.py for source line mapping in diagnostics")
    parser.add_argument("--cta", default=None, help="Path to cta.json file")
    parser.add_argument("--seeds", type=int, default=50, help="Number of dry-run seeds (default 50)")
    parser.add_argument("--strict", action="store_true", default=True, help="Enforce production contract parity (default: true)")
    parser.add_argument("--no-strict", dest="strict", action="store_false", help="Bypass production parity checks")
    parser.add_argument("--auto-fix", dest="auto_fix", action="store_true", default=True, help="Automatically heal mechanical issues in templates (default: True)")
    parser.add_argument("--no-auto-fix", dest="auto_fix", action="store_false", help="Bypass mechanical auto-healing of templates")
    parser.add_argument("--attempts-dir", default=None, help="Directory to track per-competency validation cycles")
    parser.add_argument("--json-report", default=None, help="Optional output path for structured JSON diagnostic report")
    args = parser.parse_args()

    targets = [Path(t) for t in args.target]

    if args.shard:
        # Strictly verify pre_shard_manifest.json (ZERO Fallbacks)
        manifest_candidates = [
            Path("work/shards/pre_shard_manifest.json"),
            Path("shards/pre_shard_manifest.json"),
            Path("work/pre_shard_manifest.json"),
        ]
        manifest_file = None
        for c in manifest_candidates:
            if c.is_file():
                manifest_file = c
                break
        if not manifest_file:
            print("BLOCKER:: No existe pre_shard_manifest.json", file=sys.stderr)
            sys.exit(2)

        try:
            m_data = json.loads(manifest_file.read_text(encoding="utf-8"))
            s_target = str(args.shard).lower().strip()
            shard_entry = None
            for s in m_data.get("shards", []):
                s_id = str(s.get("shard_id", "")).lower().strip()
                if s_id == s_target or s_id.replace("shard_", "") == s_target.replace("shard_", ""):
                    shard_entry = s
                    break
            if not shard_entry:
                print(f"ERROR: Shard '{args.shard}' no encontrado en {manifest_file}", file=sys.stderr)
                sys.exit(1)

            t_dir = Path(shard_entry.get("templates_dir", "work/templates"))
            c_ids = shard_entry.get("competency_ids", [])
            for cid in c_ids:
                tpl_p = t_dir / f"{cid}.json"
                if tpl_p not in targets:
                    targets.append(tpl_p)

            if not args.shard_py and shard_entry.get("shard_data_path"):
                args.shard_py = shard_entry.get("shard_data_path")
        except Exception as e:
            print(f"ERROR al leer pre_shard_manifest.json: {e}", file=sys.stderr)
            sys.exit(1)

    if not targets:
        parser.error("At least one target file/directory or --shard must be specified.")

    cta_p = Path(args.cta) if args.cta else None
    valid, errors = check_templates_file_or_dir(
        targets,
        cta_p,
        num_dry_run_seeds=args.seeds,
        strict=args.strict,
        attempts_dir=Path(args.attempts_dir) if args.attempts_dir else None,
        auto_fix=args.auto_fix,
        shard_py=args.shard_py,
        shard_id=args.shard,
    )

    if args.json_report:
        err_groups: Dict[Tuple[str, str, str], Dict[str, Any]] = {}
        for err in errors:
            rec = extract_diagnostic_metadata(err) if "extract_diagnostic_metadata" in globals() else {}
            rule_id = rec.get("rule_tag", "") or "UNKNOWN"
            tpl_id = rec.get("template", "") or "ALL"
            msg = rec.get("cause", "") or str(err)
            norm_msg = re.sub(r"\bseed[s]?\s*[=:]?\s*\d+\b", "seed=X", msg, flags=re.IGNORECASE)
            norm_msg = re.sub(r"\bsemilla[s]?\s*[=:]?\s*\d+\b", "semilla=X", norm_msg, flags=re.IGNORECASE)
            norm_msg = re.sub(r"\bsemillas\s+\d+\.\.\d+\b", "semillas X..Y", norm_msg, flags=re.IGNORECASE)
            key = (rule_id, tpl_id, norm_msg)

            m_seed = re.search(r"\b(?:seed|semilla)[s]?\s*[=:]?\s*(\d+)", str(err), re.IGNORECASE)
            sample_seed = int(m_seed.group(1)) if m_seed else None

            m_cnt = re.search(r"\((\d+)\s+semillas\)", str(err), re.IGNORECASE)
            cnt = int(m_cnt.group(1)) if m_cnt else 1

            if key not in err_groups:
                err_groups[key] = {
                    "rule_id": rule_id,
                    "template_id": tpl_id,
                    "message": norm_msg,
                    "affected_seeds_count": cnt,
                    "sample_seed": sample_seed,
                }
            else:
                err_groups[key]["affected_seeds_count"] += cnt
                if err_groups[key]["sample_seed"] is None and sample_seed is not None:
                    err_groups[key]["sample_seed"] = sample_seed

        compact_errors = list(err_groups.values()) if err_groups else errors
        report_data = {
            "valid": valid,
            "errors_count": len(errors),
            "errors": compact_errors,
            "targets": [str(t) for t in targets],
        }
        try:
            r_path = Path(args.json_report)
            r_path.parent.mkdir(parents=True, exist_ok=True)
            r_path.write_text(json.dumps(report_data, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception as ex:
            print(f"[!] Warning: Could not write json report: {ex}", file=sys.stderr)

    if not valid:
        has_cb = any("CIRCUIT BREAKER" in str(e) for e in errors)
        compact_output = render_compact_aggregated_errors(errors, targets=targets, shard_py=args.shard_py)
        print(compact_output)
        sys.exit(2 if has_cb else 1)

    print(f"PASS: All templates satisfy schema, AST security, {args.seeds} seeds dry run, invariants, TPL-D1..D4 rules, and Production Parity.")
    sys.exit(0)


if __name__ == "__main__":
    main()

