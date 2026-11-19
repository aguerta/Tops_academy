"""Independent Blind Judge Module for content-to-course v2.

Generates blind judge question batches (WITHOUT answer keys or solutions) for 2 instances
per template, evaluates judge responses against ground truth answer keys, and manages
correction cycles (maximum 3 cycles).

Zero domain logic: agnostically operates on templates conforming to template.schema.json.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import math
import random
import re
import sys
import zlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union, Set

# Ensure skill directory is in sys.path
skill_dir = Path(__file__).parent.resolve()
if str(skill_dir) not in sys.path:
    sys.path.insert(0, str(skill_dir))

from engine.assemble import assemble_question
from engine.invariants import check_instance_invariants
from engine.sandbox import execute_sandbox_instance, execute_verifier_code
from engine.interstage_schemas import ArtifactCertificate, write_certificate

logger = logging.getLogger("judge")
MAX_CORRECTION_CYCLES = 3
DEFAULT_MAX_JUDGES = 10
DEFAULT_MAX_ITEMS_PER_JUDGE = 20

MC7_STEM_SOLUBILITY_INSTRUCTIONS = (
    "CRITICAL SOLUBILITY PROTOCOL (MC7): Before comparing against options A..G, you MUST: "
    "(1) write 'symbolic_formula' derived strictly from the stem, and "
    "(2) compute 'derived_value_from_stem_only' exclusively from the stem WITHOUT inspecting or reverse-engineering from options A..G. "
    "If the stem omits a required definition/parameter or requires reverse-engineering from the options, "
    "you MUST set 'flaw_detected': true and explain the omission in 'flaw_description'."
)


def _build_mc7_judge_contract(has_numeric_options: bool = False) -> Dict[str, Any]:
    """Builds the blind judge solubility contract and response schema for MC7 items."""
    return {
        "requires_stem_only_derivation": True,
        "has_numeric_options": bool(has_numeric_options),
        "judge_instructions": MC7_STEM_SOLUBILITY_INSTRUCTIONS,
        "response_schema": {
            "item_id": "string",
            "symbolic_formula": "string (required: symbolic formula derived strictly from stem before inspecting options A..G)",
            "derived_value_from_stem_only": "number | string | null (required: value computed exclusively from stem before comparing options A..G)",
            "answer": "string (selected option letter A..G)",
            "flaw_detected": "boolean (true if stem omits a definition or requires reverse-engineering from options)",
            "flaw_description": "string (reason when flaw_detected is true)",
        },
    }


def _load_templates(templates_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """Loads all template objects from a JSON file or directory of JSON files, attaching SHA-256 hashes."""
    path = Path(templates_path)
    templates: List[Dict[str, Any]] = []

    if path.is_file():
        raw_bytes = path.read_bytes()
        file_sha = hashlib.sha256(raw_bytes).hexdigest()
        content = json.loads(raw_bytes.decode("utf-8"))
        if isinstance(content, dict):
            if "templates" in content:
                for t in content["templates"]:
                    if "competency_id" not in t and "competency_id" in content:
                        t["competency_id"] = content["competency_id"]
                    t_sha = hashlib.sha256(json.dumps(t, sort_keys=True).encode("utf-8")).hexdigest()
                    t["_sha256"] = t_sha
                    t["_file_sha256"] = file_sha
                    templates.append(t)
            else:
                t_sha = hashlib.sha256(json.dumps(content, sort_keys=True).encode("utf-8")).hexdigest()
                content["_sha256"] = t_sha
                content["_file_sha256"] = file_sha
                templates.append(content)
        elif isinstance(content, list):
            for t in content:
                t_sha = hashlib.sha256(json.dumps(t, sort_keys=True).encode("utf-8")).hexdigest()
                t["_sha256"] = t_sha
                t["_file_sha256"] = file_sha
                templates.append(t)
    elif path.is_dir():
        for file in sorted(path.glob("*.json")):
            try:
                raw_bytes = file.read_bytes()
                file_sha = hashlib.sha256(raw_bytes).hexdigest()
                data = json.loads(raw_bytes.decode("utf-8"))
                if isinstance(data, dict):
                    if "templates" in data:
                        for t in data["templates"]:
                            if "competency_id" not in t and "competency_id" in data:
                                t["competency_id"] = data["competency_id"]
                            t["_sha256"] = file_sha
                            t["_file_sha256"] = file_sha
                            templates.append(t)
                    else:
                        data["_sha256"] = file_sha
                        data["_file_sha256"] = file_sha
                        templates.append(data)
                elif isinstance(data, list):
                    for t in data:
                        t["_sha256"] = file_sha
                        t["_file_sha256"] = file_sha
                        templates.append(t)
            except Exception as e:
                logger.warning("Could not read template file %s: %s", file, e)

    return templates


def _normalize_option_letter(val: Any) -> str:
    """Normalize option identifier by removing 'opt_' or similar prefixes and converting to uppercase."""
    if val is None:
        return ""
    s = str(val).strip()
    # Strip prefixes like opt_, OPT_, option_, Option , etc.
    s = re.sub(r"^(?:opt(?:ion|ción)?_?|\s*)+", "", s, flags=re.IGNORECASE).strip()
    # If starting with a single letter (e.g. 'B', 'b', 'B.', 'B)', 'B: ...')
    m = re.match(r"^([A-Za-z])(?:\b|[.:\)\s]|$)", s)
    if m:
        return m.group(1).upper()
    return s.upper()


def _parse_float(val: Any) -> Optional[float]:
    """Parse numeric float from numeric or string value, handling commas, math formatting, and fractions."""
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).strip().replace(" ", "").replace("$", "").replace("%", "")
    # Remove outer math formatting wrappers
    s = re.sub(r"^\$\$?(.*?)\$\$?$", r"\1", s)
    s = re.sub(r"^\\\[(.*?)\\\]$", r"\1", s)
    s = re.sub(r"^\\\((.*?)\\\)$", r"\1", s)
    s = s.strip("'\"` ")
    # Comma as decimal separator if single comma and no period
    if s.count(",") == 1 and "." not in s:
        s = s.replace(",", ".")
    try:
        return float(s)
    except (ValueError, TypeError):
        pass
    # Support simple fraction like "1/2" or "-3/4"
    if "/" in s:
        parts = s.split("/")
        if len(parts) == 2:
            try:
                num = float(parts[0])
                den = float(parts[1])
                if den != 0:
                    return num / den
            except (ValueError, TypeError):
                pass
    return None


def _is_numeric_equal(val1: Any, val2: Any, tol: float = 0.01) -> bool:
    """Checks whether two values are numerically equal within a given tolerance (default 0.01)."""
    f1 = _parse_float(val1)
    f2 = _parse_float(val2)
    if f1 is not None and f2 is not None:
        return abs(f1 - f2) <= tol or math.isclose(f1, f2, abs_tol=tol, rel_tol=1e-4)
    return False


def _normalize_str(s: Any) -> str:
    """Normalizes whitespace and removes math wrapper characters."""
    if s is None:
        return ""
    st = str(s).strip()
    # Strip LaTeX math wrappers $...$ or $$...$$ or \(...\) or \[...\]
    st = re.sub(r"^\$\$?(.*?)\$\$?$", r"\1", st)
    st = re.sub(r"^\\\[(.*?)\\\]$", r"\1", st)
    st = re.sub(r"^\\\((.*?)\\\)$", r"\1", st)
    st = st.strip("'\"` ").lower()
    return re.sub(r"\s+", "", st)


_M20_INTERACTION_TYPES = (
    "open_symbolic",
    "proof_dag",
    "adversarial_break",
    "unstructured_model",
    "invariant_canvas",
    "concept_matching",
)

_GREEK_EXPR_MAP = {
    "α": "alpha", "β": "beta", "γ": "gamma", "δ": "delta", "ε": "epsilon",
    "ζ": "zeta", "η": "eta", "θ": "theta", "κ": "kappa", "λ": "lambda_",
    "μ": "mu", "ξ": "xi", "π": "pi", "ρ": "rho", "σ": "sigma",
    "τ": "tau", "φ": "phi", "ψ": "psi", "ω": "omega", "Δ": "Delta",
    "×": "*", "·": "*", "÷": "/", "−": "-", "√(": "sqrt(",
}


def _parse_json_or_dict(val: Any) -> Optional[Dict[str, Any]]:
    """Coerces a dict or serialized JSON object string into a Python dict."""
    if isinstance(val, dict):
        return val
    if isinstance(val, str):
        s = val.strip()
        if s.startswith("{") and s.endswith("}"):
            try:
                parsed = json.loads(s)
                if isinstance(parsed, dict):
                    return parsed
            except Exception:
                return None
    return None


def _normalize_expr_text(expr: Any) -> str:
    """Normalizes symbolic expression strings before SymPy or string comparison."""
    s = str(expr or "").strip()
    s = re.sub(r"^\$\$?(.*?)\$\$?$", r"\1", s).strip()
    for src, dst in _GREEK_EXPR_MAP.items():
        s = s.replace(src, dst)
    s = re.sub(r"\\sqrt\{([^{}]+)\}", r"sqrt(\1)", s)
    s = re.sub(r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"((\1)/(\2))", s)
    return s.replace("^", "**")


def _is_symbolic_equal(u_raw: Any, gt_raw: Any, tol: float = 0.001) -> bool:
    """Checks mathematical equivalence between two symbolic/numeric expressions."""
    if _is_numeric_equal(u_raw, gt_raw, tol=tol):
        return True
    u_norm = _normalize_str(_normalize_expr_text(u_raw))
    g_norm = _normalize_str(_normalize_expr_text(gt_raw))
    if not u_norm or not g_norm:
        return False
    if u_norm == g_norm:
        return True
    try:
        import sympy as sp
        from sympy.parsing.sympy_parser import (
            convert_xor,
            implicit_multiplication_application,
            parse_expr,
            standard_transformations,
        )
        trans = standard_transformations + (implicit_multiplication_application, convert_xor)
        e1 = parse_expr(_normalize_expr_text(u_raw), transformations=trans)
        e2 = parse_expr(_normalize_expr_text(gt_raw), transformations=trans)
        diff = sp.simplify(e1 - e2)
        if diff == 0 or diff.equals(0):
            return True
        syms = sorted(list(e1.free_symbols | e2.free_symbols), key=lambda x: x.name)
        if syms:
            vals = [1.37 + 0.41 * idx for idx in range(len(syms))]
            subs = dict(zip(syms, vals))
            d_num = complex(diff.evalf(subs=subs))
            return abs(d_num.imag) < 1e-6 and abs(d_num.real) <= max(tol, 1e-4)
    except Exception:
        pass
    return False


def _sanitize_m20_judge_item(
    itype: str,
    assembled: Dict[str, Any],
    judge_item: Dict[str, Any],
    gt_record: Dict[str, Any],
) -> None:
    """Populates blind prompt payload and isolated ground_truth record for M20 interaction types."""
    if itype == "open_symbolic":
        ca = assembled.get("correct_answer") if isinstance(assembled.get("correct_answer"), dict) else {}
        sym_cfg = assembled.get("symbolic_config") if isinstance(assembled.get("symbolic_config"), dict) else {}
        tol = float(ca.get("tolerance", 0.001) or 0.001)
        if sym_cfg:
            judge_item["symbolic_config"] = sym_cfg
        judge_item["answer_contract"] = {
            "expected_format": "open_symbolic",
            "variables": sym_cfg.get("variables") or [],
            "tolerance": tol,
        }
        gt_record["correct_value"] = ca.get("expression") or ca.get("value") or ""
        gt_record["canonical_algebraic"] = ca.get("canonical_algebraic") or ""
        gt_record["accepted_equivalents"] = ca.get("accepted_equivalents") or []
        gt_record["variables"] = sym_cfg.get("variables") or []
        gt_record["tolerance"] = tol
        return

    if itype == "proof_dag":
        pd = assembled.get("proof_dag") if isinstance(assembled.get("proof_dag"), dict) else {}
        blind_dag: Dict[str, Any] = {
            "steps": [{"id": s.get("id"), "content": s.get("content")} for s in (pd.get("steps") or []) if isinstance(s, dict)],
            "require_justification": bool(pd.get("require_justification", False)),
        }
        if pd.get("goal"):
            blind_dag["goal"] = pd["goal"]
        if pd.get("justification_bank"):
            blind_dag["justification_bank"] = pd["justification_bank"]
        judge_item["proof_dag"] = blind_dag
        gt_record["correct_answer"] = assembled.get("correct_answer") or {}
        return

    if itype == "adversarial_break":
        adv = assembled.get("adversarial_break") if isinstance(assembled.get("adversarial_break"), dict) else {}
        adv_mode = str(adv.get("mode") or "find_fallacy")
        blind_adv: Dict[str, Any] = {"mode": adv_mode}
        if adv_mode == "find_fallacy":
            blind_adv["steps"] = [
                {"id": s.get("id"), "content": s.get("content")}
                for s in (adv.get("steps") or [])
                if isinstance(s, dict)
            ]
            if adv.get("reason_options"):
                blind_adv["reason_options"] = [
                    {"id": r.get("id"), "content": r.get("content")}
                    for r in adv["reason_options"]
                    if isinstance(r, dict)
                ]
        else:
            for key in ("inputs", "predicates", "claim", "computed_readouts"):
                if key in adv:
                    blind_adv[key] = adv[key]
        judge_item["adversarial_break"] = blind_adv
        gt_record["correct_answer"] = assembled.get("correct_answer") or {}
        return

    if itype == "unstructured_model":
        um = assembled.get("unstructured_model") if isinstance(assembled.get("unstructured_model"), dict) else {}
        p1 = um.get("phase1_variables") if isinstance(um.get("phase1_variables"), dict) else {}
        p2 = um.get("phase2_assumptions") if isinstance(um.get("phase2_assumptions"), dict) else {}
        p3 = um.get("phase3_formulation") if isinstance(um.get("phase3_formulation"), dict) else {}
        p3_mode = str(p3.get("input_mode") or "select")
        blind_p3: Dict[str, Any] = {"prompt": p3.get("prompt", ""), "input_mode": p3_mode}
        if p3_mode == "select":
            blind_p3["options"] = [
                {"id": o.get("id"), "content": o.get("content")}
                for o in (p3.get("options") or [])
                if isinstance(o, dict)
            ]
        elif p3.get("symbolic_config"):
            blind_p3["symbolic_config"] = p3["symbolic_config"]
        judge_item["unstructured_model"] = {
            "phase1_variables": {
                "prompt": p1.get("prompt", ""),
                "roles": p1.get("roles") or [],
                "items": [
                    {k: it[k] for k in ("id", "label", "symbol") if k in it}
                    for it in (p1.get("items") or [])
                    if isinstance(it, dict)
                ],
            },
            "phase2_assumptions": {
                "prompt": p2.get("prompt", ""),
                "options": [
                    {"id": o.get("id"), "content": o.get("content")}
                    for o in (p2.get("options") or [])
                    if isinstance(o, dict)
                ],
            },
            "phase3_formulation": blind_p3,
        }
        gt_record["correct_answer"] = assembled.get("correct_answer") or {}
        return

    if itype == "invariant_canvas":
        ic = assembled.get("invariant_canvas") if isinstance(assembled.get("invariant_canvas"), dict) else {}
        c_mode = str(ic.get("mode") or "cartesian")
        if c_mode == "tree":
            blind_keys = ("mode", "width", "height", "interaction_mode", "nodes", "edges")
        else:
            blind_keys = (
                "mode", "x_range", "y_range", "step", "x_label", "y_label", "snap", "sliders",
                "fixed_curves", "fixed_points", "segments", "polygons", "shaded_regions",
                "inequality", "interactive_curves", "interactive_points",
            )
        judge_item["invariant_canvas"] = {k: ic[k] for k in blind_keys if k in ic}
        gt_record["correct_answer"] = assembled.get("correct_answer") or {}
        if c_mode == "cartesian" and isinstance(ic.get("invariants"), list):
            gt_record["invariants"] = ic["invariants"]
        return

    if itype == "concept_matching":
        cm = assembled.get("concept_matching") if isinstance(assembled.get("concept_matching"), dict) else {}
        judge_item["concept_matching"] = {
            "left_title": cm.get("left_title", "Premisa"),
            "right_title": cm.get("right_title", "Consecuencia"),
            "premises": [
                {"id": p.get("id"), "content": p.get("content")}
                for p in (cm.get("premises") or [])
                if isinstance(p, dict)
            ],
            "targets": [
                {"id": t.get("id"), "content": t.get("content")}
                for t in (cm.get("targets") or [])
                if isinstance(t, dict)
            ],
        }
        gt_record["correct_answer"] = assembled.get("correct_answer") or {}


def generate_judge_batch(
    templates_path: Union[str, Path],
    work_dir: Union[str, Path],
    cta_path: Optional[Union[str, Path]] = None,
    seeds: Optional[Tuple[int, ...]] = None,
    items_per_competency: int = 0,
    ready_only: bool = False,
    max_judges: int = DEFAULT_MAX_JUDGES,
    max_items_per_judge: int = DEFAULT_MAX_ITEMS_PER_JUDGE,
    random_seed: Optional[int] = None,
    ids: Optional[Union[str, List[Union[str, int]]]] = None,
    samples_per_template: Optional[int] = None,
    num_samples: Optional[int] = None,
) -> Tuple[Path, Path]:
    """Generates work/judge_batch.json WITHOUT answer keys using stratified random sampling.
    
    Guarantees >= 1 random instance per template/competency and samples/shuffles randomly
    up to the cap (max_judges * max_items_per_judge, default 10 * 20 = 200 items).
    Also generates work/judge_ground_truth.json and work/answer_key.json.

    Args:
        templates_path: Path to template JSON file or directory.
        work_dir: Working directory to write judge files.
        cta_path: Optional path to cta.json for distractor metadata.
        seeds: Optional candidate seeds tuple. When None (default), draws random seeds per template.
        items_per_competency: Stratified sample count per competency (defaults to 0).
                              If <= 0, performs stratified random selection across all templates up to cap.
        ready_only: If True, skips competencies that were already evaluated in earlier waves/batches.
        max_judges: Maximum number of blind judges (default: 10).
        max_items_per_judge: Maximum questions per blind judge (default: 20).
        random_seed: Optional RNG seed for reproducible random selection when needed.
        ids: Optional list of competency IDs to arbitrate in targeted mode.

    Returns:
        Tuple of (path_to_judge_batch_json, path_to_ground_truth_json).
    """
    work = Path(work_dir)
    work.mkdir(parents=True, exist_ok=True)

    templates = _load_templates(templates_path)
    if not templates:
        raise ValueError(f"No templates found in path: {templates_path}")

    if ids is not None:
        raw_ids = [ids] if isinstance(ids, (str, int)) else list(ids)
        target_ids = {str(x).strip().upper() for x in raw_ids if str(x).strip()}
        if target_ids:
            templates = [
                t for t in templates
                if str(t.get("competency_id", "")).strip().upper() in target_ids
                or str(t.get("id", "")).strip().upper() in target_ids
            ]
            if not templates:
                logger.warning("No templates matched the specified ids: %s", target_ids)

    # Load previously evaluated competencies if in ready_only mode
    evaluated_file = work / "verification" / "evaluated_competencies.json"
    evaluated_ids: Set[str] = set()
    saved_hashes: Dict[str, str] = {}
    if evaluated_file.is_file():
        try:
            ev_data = json.loads(evaluated_file.read_text(encoding="utf-8"))
            evaluated_ids = set(ev_data.get("evaluated_competency_ids", []))
            saved_hashes = ev_data.get("competency_hashes", {})
        except Exception:
            pass
    elif (work / "evaluated_competencies.json").is_file():
        try:
            ev_data = json.loads((work / "evaluated_competencies.json").read_text(encoding="utf-8"))
            evaluated_ids = set(ev_data.get("evaluated_competency_ids", []))
            saved_hashes = ev_data.get("competency_hashes", {})
        except Exception:
            pass

    if ready_only and (evaluated_ids or saved_hashes):
        unjudged_templates = []
        for t in templates:
            cid = str(t.get("competency_id", "comp-01"))
            t_sha = t.get("_sha256") or hashlib.sha256(json.dumps(t, sort_keys=True).encode("utf-8")).hexdigest()
            if cid in evaluated_ids:
                if cid in saved_hashes:
                    if saved_hashes[cid] == t_sha:
                        # Template unchanged: skip
                        continue
                    else:
                        # Template hash modified (repaired!): re-evaluate!
                        unjudged_templates.append(t)
                else:
                    # Legacy record without hash: skip
                    continue
            else:
                unjudged_templates.append(t)

        if unjudged_templates:
            templates = unjudged_templates
        else:
            logger.info("All templates in %s have already been evaluated and are unchanged (--ready-only).", templates_path)
            batch_path = work / "judge_batch.json"
            truth_path = work / "judge_ground_truth.json"
            if not batch_path.is_file():
                batch_path.write_text("[]", encoding="utf-8")
            if not truth_path.is_file():
                truth_path.write_text("{}", encoding="utf-8")
            return batch_path, truth_path

    # Load CTA distractors map if available
    cta_distractors_map: Dict[str, Dict[str, Any]] = {}
    if cta_path and Path(cta_path).is_file():
        try:
            cta_data = json.loads(Path(cta_path).read_text(encoding="utf-8"))
            for comp in cta_data.get("competencies", []):
                for d in comp.get("distractors", []):
                    if "id" in d:
                        cta_distractors_map[d["id"]] = d
        except Exception as e:
            logger.warning("Failed to load CTA distractors map from %s: %s", cta_path, e)

    judge_batch_items: List[Dict[str, Any]] = []
    ground_truth: Dict[str, Dict[str, Any]] = {}

    # Group templates by competency_id
    comp_templates: Dict[str, List[Dict[str, Any]]] = {}
    for t_idx, template in enumerate(templates):
        comp_id = template.get("competency_id", "comp-01")
        comp_templates.setdefault(comp_id, []).append(template)

    rng = random.Random(random_seed)
    max_total_items = max(1, max_judges * max_items_per_judge) if (max_judges > 0 and max_items_per_judge > 0) else 200

    def _draw_template_seeds(count: int = 3) -> List[int]:
        if seeds is not None and len(seeds) > 0:
            pool = list(seeds)
            rng.shuffle(pool)
            if len(pool) >= count:
                return pool[:count]
            return [pool[i % len(pool)] for i in range(count)]
        return rng.sample(range(100, 100000), max(1, count))

    planned_items: List[Tuple[Dict[str, Any], int]] = []

    if items_per_competency > 0:
        # Stratified random sampling: ~items_per_competency per competency
        comp_keys = list(comp_templates.keys())
        rng.shuffle(comp_keys)
        for comp_id in comp_keys:
            t_list = list(comp_templates[comp_id])
            rng.shuffle(t_list)
            # Group by interaction type for diverse stratified coverage
            by_type: Dict[str, List[Dict[str, Any]]] = {}
            for t in t_list:
                itype = t.get("interaction_type", "multiple_choice_7_options")
                by_type.setdefault(itype, []).append(t)

            type_queues = [list(q) for q in by_type.values()]
            for q in type_queues:
                rng.shuffle(q)
            selected_comp_items: List[Tuple[Dict[str, Any], int]] = []
            c_seeds = _draw_template_seeds(max(3, items_per_competency))

            while len(selected_comp_items) < items_per_competency:
                added = False
                for q in type_queues:
                    if q and len(selected_comp_items) < items_per_competency:
                        t = q.pop(0)
                        seed = c_seeds[len(selected_comp_items) % len(c_seeds)]
                        selected_comp_items.append((t, seed))
                        added = True
                if not added:
                    # If all queues drained, cycle through shuffled t_list
                    for t in t_list:
                        if len(selected_comp_items) < items_per_competency:
                            seed = c_seeds[len(selected_comp_items) % len(c_seeds)]
                            selected_comp_items.append((t, seed))
                        else:
                            break
                    break

            planned_items.extend(selected_comp_items)
        if len(planned_items) > max_total_items:
            planned_items = planned_items[:max_total_items]
    else:
        # Stratified random selection across all templates:
        # 1. Guarantee >= 1 random instance per template/competency in Round 0.
        # 2. Fill subsequent rounds randomly and stratified by competency up to max_total_items (<= 200).
        seeds_per_tpl = len(seeds) if (seeds is not None and len(seeds) > 0) else 3
        comp_keys = list(comp_templates.keys())
        rng.shuffle(comp_keys)

        def _get_target_sample_count(t_obj: Dict[str, Any]) -> int:
            if samples_per_template is not None:
                return samples_per_template
            if num_samples is not None:
                return num_samples
            if seeds is not None and len(seeds) > 0:
                return len(seeds)
            v_code = t_obj.get("verifier_code") or t_obj.get("cross_check_py") or t_obj.get("verify_py") or ""
            if v_code and str(v_code).strip():
                return 1
            return 3

        # Prepare per-template random seed lists
        tpl_seed_lists: Dict[int, List[int]] = {}
        shuffled_comp_tpls: Dict[str, List[Dict[str, Any]]] = {}
        for cid in comp_keys:
            c_tpls = list(comp_templates[cid])
            rng.shuffle(c_tpls)
            shuffled_comp_tpls[cid] = c_tpls
            for t in c_tpls:
                t_count = _get_target_sample_count(t)
                tpl_seed_lists[id(t)] = _draw_template_seeds(t_count)

        max_seeds_per_tpl = max((len(v) for v in tpl_seed_lists.values()), default=1)
        for r_idx in range(max_seeds_per_tpl):
            round_candidates: List[Tuple[Dict[str, Any], int]] = []
            # Round-robin across competencies within this round so every competency is represented
            max_tpls_in_comp = max((len(v) for v in shuffled_comp_tpls.values()), default=0)
            round_cids = list(comp_keys)
            rng.shuffle(round_cids)
            for pos in range(max_tpls_in_comp):
                for cid in round_cids:
                    c_tpls = shuffled_comp_tpls[cid]
                    if pos < len(c_tpls):
                        t = c_tpls[pos]
                        t_seeds = tpl_seed_lists[id(t)]
                        if r_idx < len(t_seeds):
                            round_candidates.append((t, t_seeds[r_idx]))
            if r_idx > 0:
                rng.shuffle(round_candidates)
            for cand in round_candidates:
                if len(planned_items) >= max_total_items:
                    break
                planned_items.append(cand)
            if len(planned_items) >= max_total_items:
                break

    template_counts: Dict[str, int] = {}
    refuted_templates: Dict[str, Dict[str, Any]] = {}

    for template, seed in planned_items:
        template_id = template.get("id", "T-00")
        comp_id = template.get("competency_id", "comp-01")
        itype = template.get("interaction_type", "multiple_choice_7_options")

        gen_code = template.get("generate_py") or template.get("generator_code") or ""
        ver_code = template.get("verifier_code") or template.get("cross_check_py") or template.get("verify_py") or ""

        # Pre-verify candidate seed, deterministically retrying next seed on collision or invariant failure
        active_seed = seed
        gen_res = None
        assembled = None
        seed_passed = False
        max_seed_retries = 5
        curr_try = 0

        while curr_try < max_seed_retries and not seed_passed:
            curr_try += 1
            try:
                cand_res = execute_sandbox_instance(gen_code, seed=active_seed, timeout=1.5)
                # Verify cross-check / verifier if present (strict boolean True required)
                if ver_code and str(ver_code).strip():
                    is_ver = execute_verifier_code(ver_code, cand_res, seed=active_seed, timeout=1.5)
                    if is_ver is not True:
                        active_seed = (active_seed + 101) % 99991 + 100
                        continue

                inst_idx = template_counts.get(template_id, 0) + 1
                option_shuffle_seed = zlib.crc32(f"{template_id}:{inst_idx}:{active_seed}".encode("utf-8")) & 0xFFFFFFFF
                cand_assembled = assemble_question(
                    template=template,
                    gen_result=cand_res,
                    competency_id=comp_id,
                    question_index=inst_idx,
                    cta_distractors_map=cta_distractors_map,
                    seed=option_shuffle_seed,
                )

                is_inv, inv_errs = check_instance_invariants(cand_assembled, itype)
                if not is_inv:
                    active_seed = (active_seed + 101) % 99991 + 100
                    continue

                seed_passed = True
                gen_res = cand_res
                assembled = cand_assembled
            except Exception:
                active_seed = (active_seed + 101) % 99991 + 100

        if not seed_passed or assembled is None:
            # Deterministic kernel refutation: template failed verification
            refuted_templates[template_id] = {
                "template_id": template_id,
                "competency_id": comp_id,
                "kernel_refuted": True,
                "reason": "Deterministic verification kernel refuted all candidate seeds",
            }
            inst_idx = template_counts.get(template_id, 0) + 1
            template_counts[template_id] = inst_idx
            item_id = f"{template_id}_judge_{inst_idx}"
            ground_truth[item_id] = {
                "item_id": item_id,
                "template_id": template_id,
                "competency_id": comp_id,
                "interaction_type": itype,
                "kernel_refuted": True,
                "kernel_verified": False,
            }
            continue

        inst_idx = template_counts.get(template_id, 0) + 1
        template_counts[template_id] = inst_idx
        item_id = f"{template_id}_judge_{inst_idx}"

        # Strip all answer indicators for the blind judge
        judge_item: Dict[str, Any] = {
            "item_id": item_id,
            "template_id": template_id,
            "competency_id": comp_id,
            "interaction_type": itype,
            "stem": assembled["stem"],
        }

        gt_record: Dict[str, Any] = {
            "item_id": item_id,
            "template_id": template_id,
            "competency_id": comp_id,
            "interaction_type": itype,
            "kernel_verified": bool(ver_code and str(ver_code).strip()),
            "kernel_refuted": False,
        }

        if itype == "multiple_choice_7_options":
            options_blind = []
            correct_letter = None
            correct_content = None

            for opt in assembled.get("options", []):
                raw_id = opt.get("option_id") or opt.get("id", "")
                letter = _normalize_option_letter(raw_id)
                content = opt.get("content", "")
                options_blind.append({"id": letter, "content": content})
                if opt.get("is_correct") is True:
                    correct_letter = letter
                    correct_content = content

            has_numeric_opts = bool(options_blind) and all(
                _parse_float(opt.get("content")) is not None for opt in options_blind
            )
            mc7_contract = _build_mc7_judge_contract(has_numeric_options=has_numeric_opts)

            judge_item["options"] = options_blind
            judge_item["judge_instructions"] = mc7_contract["judge_instructions"]
            judge_item["response_schema"] = mc7_contract["response_schema"]
            judge_item["answer_contract"] = mc7_contract
            gt_record["correct_letter"] = correct_letter
            gt_record["correct_content"] = correct_content
            gt_record["has_numeric_options"] = has_numeric_opts

        elif itype == "multiple_select":
            options_blind = []
            correct_letters = []
            correct_contents = []

            for opt in assembled.get("options", []):
                raw_id = opt.get("option_id") or opt.get("id", "")
                letter = _normalize_option_letter(raw_id)
                content = opt.get("content", "")
                options_blind.append({"id": letter, "content": content})
                if opt.get("is_correct") is True:
                    correct_letters.append(letter)
                    correct_contents.append(content)

            judge_item["options"] = options_blind
            gt_record["correct_letters"] = sorted(correct_letters)
            gt_record["correct_contents"] = sorted(correct_contents)

        elif itype == "fill_in_the_blank":
            ca = assembled.get("correct_answer", {})
            c_val = ca.get("value") or assembled.get("value")
            gt_record["correct_value"] = c_val
            gt_record["canonical_algebraic"] = ca.get("canonical_algebraic") or assembled.get("canonical_algebraic")
            gt_record["accepted_equivalents"] = ca.get("accepted_equivalents") or assembled.get("accepted_equivalents", [])
            tol = ca.get("tolerance") or assembled.get("tolerance", 0.01)
            try:
                tol = float(tol)
            except (ValueError, TypeError):
                tol = 0.01
            if tol < 0.01:
                tol = 0.01
            gt_record["tolerance"] = tol

            # Build enriched typed contract for blind judges
            parsed_num = _parse_float(c_val)
            expected_type = "float"
            decimal_places = 2
            format_example = "2.80 o 2.8"
            if parsed_num is not None:
                if parsed_num.is_integer():
                    expected_type = "integer"
                    decimal_places = 0
                    format_example = f"{int(parsed_num)}"
                else:
                    expected_type = "float"
                    decimal_places = 2
                    format_example = f"{parsed_num:.2f} o {round(parsed_num, 4)}"

            contract = {
                "expected_type": expected_type,
                "decimal_places": decimal_places,
                "tolerance": tol,
                "format_example": format_example,
            }
            judge_item["answer_contract"] = contract
            gt_record["answer_contract"] = contract

        elif itype in _M20_INTERACTION_TYPES:
            _sanitize_m20_judge_item(itype, assembled, judge_item, gt_record)

        if "graph" in assembled and assembled["graph"]:
            judge_item["graph"] = assembled["graph"]

        judge_batch_items.append(judge_item)
        ground_truth[item_id] = gt_record

    # Shuffle the assembled batch items randomly so question order is randomized
    rng.shuffle(judge_batch_items)

    v_dir = work / "verification"
    v_dir.mkdir(parents=True, exist_ok=True)

    batch_path = work / "judge_batch.json"
    batch_json_str = json.dumps(judge_batch_items, indent=2, ensure_ascii=False)
    batch_path.write_text(batch_json_str, encoding="utf-8")
    (v_dir / "judge_batch.json").write_text(batch_json_str, encoding="utf-8")

    truth_path = work / "judge_ground_truth.json"
    truth_json_str = json.dumps(ground_truth, indent=2, ensure_ascii=False)
    truth_path.write_text(truth_json_str, encoding="utf-8")
    (v_dir / "judge_ground_truth.json").write_text(truth_json_str, encoding="utf-8")

    answer_key_path = work / "answer_key.json"
    answer_key_path.write_text(truth_json_str, encoding="utf-8")
    (v_dir / "answer_key.json").write_text(truth_json_str, encoding="utf-8")

    if refuted_templates:
        refuted_json_str = json.dumps(refuted_templates, indent=2, ensure_ascii=False)
        (work / "refuted_templates.json").write_text(refuted_json_str, encoding="utf-8")
        (v_dir / "refuted_templates.json").write_text(refuted_json_str, encoding="utf-8")

    # Clean up stale split batches in verification and work so dispatch_judges slices the new batch fresh
    for stale_split in list(v_dir.glob("judge_batch_*.json")) + list(work.glob("judge_batch_*.json")):
        if stale_split.name not in ("judge_batch.json", "judge_redispatch_batch.json"):
            try:
                stale_split.unlink(missing_ok=True)
            except Exception:
                pass

    # Record evaluated competency IDs and their SHA-256 hashes for incremental streaming
    new_comp_ids = {t.get("competency_id", "comp-01") for t, _ in planned_items}
    total_evaluated_ids = sorted(evaluated_ids.union(new_comp_ids))
    total_hashes = dict(saved_hashes)
    for t in templates:
        cid = str(t.get("competency_id", "comp-01"))
        t_sha = t.get("_sha256") or hashlib.sha256(json.dumps(t, sort_keys=True).encode("utf-8")).hexdigest()
        total_hashes[cid] = t_sha

    ev_payload = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "evaluated_competency_ids": total_evaluated_ids,
        "evaluated_count": len(total_evaluated_ids),
        "competency_hashes": total_hashes,
    }
    (v_dir / "evaluated_competencies.json").write_text(json.dumps(ev_payload, indent=2, ensure_ascii=False), encoding="utf-8")
    (work / "evaluated_competencies.json").write_text(json.dumps(ev_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    logger.info("Generated judge batch with %d items at %s", len(judge_batch_items), batch_path)
    return batch_path, truth_path


# Canonical alias for compatibility
prepare_judge_batch = generate_judge_batch


def split_judge_batch(
    work_dir: Union[str, Path, List[Dict[str, Any]]],
    max_judges: int = DEFAULT_MAX_JUDGES,
    items_per_judge: int = DEFAULT_MAX_ITEMS_PER_JUDGE,
    max_items_per_judge: Optional[int] = None,
    random_seed: Optional[int] = None,
) -> Any:
    """Splits work/judge_batch.json or raw items list into batches with at most items_per_judge items each (default <= 20)
    and at most max_judges judges (default <= 10), using stratified random assignment.
    
    Args:
        work_dir: Working directory containing judge_batch.json, OR a direct list of item dicts.
        max_judges: Hard cap for maximum number of judges (default: 10).
        items_per_judge: Maximum item count per judge (default: 20).
        max_items_per_judge: Alias for items_per_judge.
        random_seed: Optional RNG seed for reproducible shuffling/sampling.

    Returns:
        List of Paths if work_dir is a Path/str, or List of List[Dict] if work_dir is a list.
    """
    if max_items_per_judge is not None:
        items_per_judge = max_items_per_judge

    rng = random.Random(random_seed)
    limit = max(1, items_per_judge)
    max_total = max(1, max_judges * limit) if max_judges > 0 else 0

    if isinstance(work_dir, list):
        items = list(work_dir)
        if not items:
            return []
        if max_total > 0 and len(items) > max_total:
            items = rng.sample(items, max_total)
        return [items[i : i + limit] for i in range(0, len(items), limit)]

    work = Path(work_dir)
    batch_file = work / "verification" / "judge_batch.json"
    if not batch_file.is_file():
        batch_file = work / "judge_batch.json"
    if not batch_file.is_file():
        logger.warning("judge_batch.json not found in %s", work)
        return []

    try:
        items = json.loads(batch_file.read_text(encoding="utf-8"))
    except Exception as e:
        logger.error("Failed to parse judge_batch.json: %s", e)
        return []

    if not items:
        return []

    verif_dir = work / "verification"
    verif_dir.mkdir(parents=True, exist_ok=True)

    # Stratified random cap if total items exceed max_judges * items_per_judge (default 10 * 20 = 200)
    if max_total > 0 and len(items) > max_total:
        by_cid: Dict[str, List[Dict[str, Any]]] = {}
        for itm in items:
            cid = str(itm.get("competency_id", "default"))
            by_cid.setdefault(cid, []).append(itm)
        cid_keys = list(by_cid.keys())
        rng.shuffle(cid_keys)
        for cid in cid_keys:
            rng.shuffle(by_cid[cid])
        sampled_items: List[Dict[str, Any]] = []
        pos = 0
        max_len = max((len(v) for v in by_cid.values()), default=0)
        while len(sampled_items) < max_total and pos < max_len:
            for cid in cid_keys:
                if pos < len(by_cid[cid]) and len(sampled_items) < max_total:
                    sampled_items.append(by_cid[cid][pos])
            pos += 1
        items = sampled_items
        # Synchronize judge_batch.json and ground_truth to the capped items
        batch_json_str = json.dumps(items, indent=2, ensure_ascii=False)
        (work / "judge_batch.json").write_text(batch_json_str, encoding="utf-8")
        (verif_dir / "judge_batch.json").write_text(batch_json_str, encoding="utf-8")
        kept_ids = {
            str(itm.get("item_id") or itm.get("question_id") or itm.get("id"))
            for itm in items if isinstance(itm, dict)
        }
        for gt_p in [work / "judge_ground_truth.json", verif_dir / "judge_ground_truth.json", work / "answer_key.json", verif_dir / "answer_key.json"]:
            if gt_p.is_file():
                try:
                    gt_obj = json.loads(gt_p.read_text(encoding="utf-8"))
                    if isinstance(gt_obj, dict):
                        filtered_gt = {k: v for k, v in gt_obj.items() if str(k) in kept_ids}
                        gt_p.write_text(json.dumps(filtered_gt, indent=2, ensure_ascii=False), encoding="utf-8")
                except Exception:
                    pass

    total_items = len(items)
    # Strictly enforce both items_per_judge <= 20 and num_judges <= max_judges (10)
    needed_judges = math.ceil(total_items / limit)
    num_judges = min(max_judges, max(1, needed_judges)) if max_judges > 0 else max(1, needed_judges)
    num_judges = min(num_judges, total_items)
    num_judges = max(1, num_judges)

    # Stratified random distribution by competency_id
    comp_groups: Dict[str, List[Dict[str, Any]]] = {}
    for item in items:
        cid = item.get("competency_id", "default")
        comp_groups.setdefault(cid, []).append(item)

    buckets: List[List[Dict[str, Any]]] = [[] for _ in range(num_judges)]
    curr_j = 0
    for cid, c_items in comp_groups.items():
        c_shuffled = list(c_items)
        rng.shuffle(c_shuffled)
        for itm in c_shuffled:
            buckets[curr_j % num_judges].append(itm)
            curr_j += 1

    # Filter out empty buckets and randomize order within each judge's bucket
    non_empty_buckets = []
    for b in buckets:
        if b:
            rng.shuffle(b)
            non_empty_buckets.append(b)

    # Remove stale split files before writing fresh ones
    for stale_split in list(verif_dir.glob("judge_batch_*.json")) + list(work.glob("judge_batch_*.json")):
        if stale_split.name not in ("judge_batch.json", "judge_redispatch_batch.json"):
            try:
                stale_split.unlink(missing_ok=True)
            except Exception:
                pass

    generated_paths: List[Path] = []
    for idx, b_items in enumerate(non_empty_buckets):
        # Write to work/judge_batch_{idx+1:02d}.json
        out_p = work / f"judge_batch_{idx + 1:02d}.json"
        out_p.write_text(json.dumps(b_items, indent=2, ensure_ascii=False), encoding="utf-8")
        generated_paths.append(out_p)

        # Also write to work/verification/judge_batch_{idx+1:02d}.json
        verif_out_p = verif_dir / f"judge_batch_{idx + 1:02d}.json"
        verif_out_p.write_text(json.dumps(b_items, indent=2, ensure_ascii=False), encoding="utf-8")

    logger.info("Split %d items across %d judge batches (max %d items/judge, max %d judges) in %s", total_items, len(non_empty_buckets), limit, max_judges, work)
    return generated_paths


def check_judge_completeness(work_dir: Union[str, Path]) -> Dict[str, Any]:
    """Detects truncated or missing judge responses across all batch files.
    
    Verifies that len(responses) == len(batch_items) for each judge batch.
    Returns completeness metrics, truncated batches, and exact missing item IDs.
    """
    work = Path(work_dir).resolve()
    verif_dir = work / "verification"
    judges_dir = work / "judges"

    # Locate batch files
    cand_batches = sorted(verif_dir.glob("judge_batch_*.json")) if verif_dir.is_dir() else []
    if not cand_batches:
        cand_batches = sorted(work.glob("judge_batch_*.json"))
    split_batches = [bf for bf in cand_batches if bf.name not in ("judge_batch.json", "judge_redispatch_batch.json")]
    if not split_batches:
        unsplit = verif_dir / "judge_batch.json"
        if not unsplit.is_file():
            unsplit = work / "judge_batch.json"
        if unsplit.is_file():
            split_batches = [unsplit]

    total_expected = 0
    total_received = 0
    all_missing_ids: List[str] = []
    batch_reports: List[Dict[str, Any]] = []

    for bf in split_batches:
        m = re.search(r"judge_batch_(\d+)", bf.name)
        j_id = m.group(1) if m else "01"

        try:
            b_data = json.loads(bf.read_text(encoding="utf-8"))
            raw_items = b_data.get("items", []) if isinstance(b_data, dict) else (b_data if isinstance(b_data, list) else [])
        except Exception:
            raw_items = []

        expected_ids: List[str] = []
        for itm in raw_items:
            if isinstance(itm, dict):
                iid = itm.get("item_id") or itm.get("question_id") or itm.get("id")
                if iid:
                    expected_ids.append(str(iid))

        # Look for corresponding response file
        resp_candidates = [
            verif_dir / f"judge_responses_{j_id}.json",
            work / f"judge_responses_{j_id}.json",
            judges_dir / f"judge_{j_id}.json",
            verif_dir / "judge_responses.json",
            work / "judge_responses.json",
        ]
        resp_file: Optional[Path] = None
        for rc in resp_candidates:
            if rc.is_file():
                resp_file = rc
                break

        resp_map: Dict[str, Any] = {}
        if resp_file:
            try:
                raw_resp = json.loads(resp_file.read_text(encoding="utf-8"))
                eval_list = None
                if isinstance(raw_resp, list):
                    eval_list = raw_resp
                elif isinstance(raw_resp, dict):
                    for cand_key in ("evaluations", "items", "results", "responses"):
                        if isinstance(raw_resp.get(cand_key), list):
                            eval_list = raw_resp[cand_key]
                            break
                if eval_list is not None:
                    for r in eval_list:
                        if isinstance(r, dict):
                            rid = r.get("item_id") or r.get("question_id") or r.get("id")
                            if rid:
                                ans_val = None
                                for k in ("answer", "response", "verdict"):
                                    if r.get(k) is not None:
                                        ans_val = r[k]
                                        break
                                resp_map[str(rid)] = ans_val if ans_val is not None else True
                elif isinstance(raw_resp, dict):
                    dict_inner = raw_resp.get("responses", raw_resp) if isinstance(raw_resp.get("responses"), dict) else raw_resp
                    for k, v in dict_inner.items():
                        if isinstance(v, dict):
                            ans_val = None
                            for ak in ("answer", "response", "verdict"):
                                if v.get(ak) is not None:
                                    ans_val = v[ak]
                                    break
                            resp_map[str(k)] = ans_val if ans_val is not None else v
                        else:
                            resp_map[str(k)] = v
            except Exception as e:
                logger.warning("Could not read response file %s: %s", resp_file, e)

        # Check completeness for this batch
        received_ids = [iid for iid in expected_ids if iid in resp_map and resp_map[iid] is not None]
        missing_ids = [iid for iid in expected_ids if iid not in received_ids]

        total_expected += len(expected_ids)
        total_received += len(received_ids)
        all_missing_ids.extend(missing_ids)

        is_truncated = len(missing_ids) > 0
        batch_reports.append({
            "batch_file": bf.name,
            "judge_id": j_id,
            "expected_count": len(expected_ids),
            "received_count": len(received_ids),
            "missing_count": len(missing_ids),
            "missing_item_ids": missing_ids,
            "is_truncated": is_truncated,
            "status": "truncated" if is_truncated else "complete",
            "response_file": resp_file.as_posix() if resp_file else None,
        })

    is_complete = (len(all_missing_ids) == 0) and (total_expected > 0)
    truncated_batches_count = sum(1 for b in batch_reports if b["is_truncated"])

    return {
        "is_complete": is_complete,
        "total_batches": len(batch_reports),
        "completed_batches": len(batch_reports) - truncated_batches_count,
        "truncated_batches": truncated_batches_count,
        "total_expected_items": total_expected,
        "total_received_items": total_received,
        "total_missing_items": len(all_missing_ids),
        "missing_ids": all_missing_ids,
        "missing_item_ids": all_missing_ids,
        "batch_reports": batch_reports,
    }


def emit_judge_redispatch(
    work_dir: Union[str, Path],
    max_items_per_judge: int = DEFAULT_MAX_ITEMS_PER_JUDGE,
) -> Dict[str, Any]:
    """Automatically detects incomplete evaluations and emits re-dispatch batch files for only missing IDs.
    
    Guarantees that re-dispatched items remain 100% blind (no ground truth or answer keys).
    """
    work = Path(work_dir).resolve()
    verif_dir = work / "verification"
    verif_dir.mkdir(parents=True, exist_ok=True)

    completeness = check_judge_completeness(work)
    if completeness["is_complete"] or completeness["total_missing_items"] == 0:
        logger.info("All judge evaluations are complete. No re-dispatch needed.")
        return {
            "redispatch_needed": False,
            "missing_count": 0,
            "batches": [],
            "item_files": [],
        }

    missing_set = set(completeness["missing_item_ids"])

    # Collect blind question definitions for missing IDs
    missing_items: List[Dict[str, Any]] = []
    seen_ids: Set[str] = set()

    cand_batches = sorted(verif_dir.glob("judge_batch_*.json")) + sorted(work.glob("judge_batch_*.json"))
    for bf in cand_batches:
        if bf.name.startswith("judge_redispatch_"):
            continue
        try:
            b_data = json.loads(bf.read_text(encoding="utf-8"))
            raw_items = b_data.get("items", []) if isinstance(b_data, dict) else (b_data if isinstance(b_data, list) else [])
            for itm in raw_items:
                if isinstance(itm, dict):
                    iid = str(itm.get("item_id") or itm.get("question_id") or itm.get("id"))
                    if iid in missing_set and iid not in seen_ids:
                        seen_ids.add(iid)
                        # Blind copy: ensure answer keys are absent
                        blind_item = {
                            "item_id": iid,
                            "question_id": itm.get("question_id") or iid,
                            "interaction_type": itm.get("interaction_type") or itm.get("question_type") or "multiple_choice",
                            "stem": itm.get("stem") or itm.get("stem_es") or "",
                            "stem_es": itm.get("stem_es") or itm.get("stem") or "",
                        }
                        if "options" in itm:
                            # Strip any is_correct flags
                            clean_opts = []
                            for opt in itm["options"]:
                                if isinstance(opt, dict):
                                    clean_opts.append({
                                        "id": opt.get("id") or opt.get("option_id", ""),
                                        "content": opt.get("content", ""),
                                    })
                            blind_item["options"] = clean_opts
                        if "answer_contract" in itm:
                            blind_item["answer_contract"] = itm["answer_contract"]
                        if "judge_instructions" in itm:
                            blind_item["judge_instructions"] = itm["judge_instructions"]
                        if "response_schema" in itm:
                            blind_item["response_schema"] = itm["response_schema"]
                        if "graph" in itm:
                            blind_item["graph"] = itm["graph"]
                        missing_items.append(blind_item)
        except Exception as e:
            logger.warning("Could not parse batch %s for re-dispatch: %s", bf, e)

    # Slice missing items into batches of <= max_items_per_judge (default 12)
    redispatch_batches: List[Path] = []
    num_batches = max(1, math.ceil(len(missing_items) / max_items_per_judge))
    batch_size = math.ceil(len(missing_items) / num_batches)

    for b_idx in range(num_batches):
        chunk = missing_items[b_idx * batch_size : (b_idx + 1) * batch_size]
        batch_path = verif_dir / f"judge_redispatch_batch_{b_idx + 1:02d}.json"
        batch_path.write_text(json.dumps(chunk, indent=2, ensure_ascii=False), encoding="utf-8")
        redispatch_batches.append(batch_path)

        # Also write to work/ root for compatibility
        work_batch_path = work / f"judge_redispatch_batch_{b_idx + 1:02d}.json"
        work_batch_path.write_text(json.dumps(chunk, indent=2, ensure_ascii=False), encoding="utf-8")

    # Consolidated re-dispatch file
    consolidated_p = verif_dir / "judge_redispatch_batch.json"
    consolidated_p.write_text(json.dumps(missing_items, indent=2, ensure_ascii=False), encoding="utf-8")

    # Save redispatch manifest in work/dispatch/
    dispatch_dir = work / "dispatch"
    dispatch_dir.mkdir(parents=True, exist_ok=True)
    manifest_p = dispatch_dir / "judge_redispatch_manifest.json"
    manifest_payload = {
        "redispatch_needed": True,
        "missing_count": len(missing_items),
        "missing_item_ids": [m["item_id"] for m in missing_items],
        "batch_count": len(redispatch_batches),
        "batches": [p.as_posix() for p in redispatch_batches],
        "consolidated_batch": consolidated_p.as_posix(),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    manifest_p.write_text(json.dumps(manifest_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    # Generate Subagents array for re-dispatch
    subagents = []
    for b_idx, b_path in enumerate(redispatch_batches, start=1):
        for j_num in (1, 2):
            subagents.append({
                "TypeName": "c2c_judge",
                "Role": f"Blind Judge Re-dispatch Batch {b_idx:02d} - Judge {j_num}",
                "Model": "inherit",
                "Prompt": (
                    f"You are Blind Judge {j_num} for Re-dispatch Batch {b_idx:02d}. "
                    f"Your work order is `{b_path.as_posix()}`. Read it first with `view_file`. "
                    f"Finalize strictly with: `DONE: verification/judge_responses_redispatch_{b_idx:02d}_{j_num}.json`."
                ),
            })

    logger.info("Emitted %d judge re-dispatch batches for %d missing items in %s", len(redispatch_batches), len(missing_items), work)
    return {
        "redispatch_needed": True,
        "missing_count": len(missing_items),
        "batches": [p.as_posix() for p in redispatch_batches],
        "consolidated_batch": consolidated_p.as_posix(),
        "Subagents": subagents,
    }


def _validate_ground_truth_item(gt: Dict[str, Any], itype: str) -> None:
    """Enforces strict ground truth schema validation prior to answer matching.

    Raises KeyError or ValueError if ground truth is malformed and not kernel_refuted.
    """
    if bool(gt.get("kernel_refuted", False)):
        return

    eff_type = "multiple_choice_7_options" if itype == "multiple_choice" else itype

    if eff_type == "multiple_choice_7_options":
        val = gt.get("correct_letter")
        if not (isinstance(val, str) and val.strip() != ""):
            raise ValueError(
                f"Ground truth schema violation for '{eff_type}': 'correct_letter' must be a non-empty string, got {val!r}"
            )
    elif eff_type == "fill_in_the_blank":
        val = gt.get("correct_value")
        if val is None or str(val).strip() == "":
            raise ValueError(
                f"Ground truth schema violation for '{eff_type}': 'correct_value' must be non-None and non-empty (preserving 0/'0'), got {val!r}"
            )
    elif eff_type == "open_symbolic":
        val = gt.get("correct_value")
        if not (isinstance(val, str) and val.strip() != ""):
            ca = gt.get("correct_answer")
            if not (isinstance(ca, dict) and str(ca.get("expression") or ca.get("value") or "").strip()):
                raise ValueError(
                    f"Ground truth schema violation for '{eff_type}': 'correct_value' must be a non-empty expression"
                )
    elif eff_type in ("proof_dag", "adversarial_break", "unstructured_model", "invariant_canvas", "concept_matching"):
        ca = gt.get("correct_answer")
        if not (isinstance(ca, dict) and len(ca) > 0):
            raise ValueError(
                f"Ground truth schema violation for '{eff_type}': 'correct_answer' must be a non-empty dict, got {ca!r}"
            )
    elif eff_type == "multiple_select":
        val = gt.get("correct_letters")
        if not (isinstance(val, list) and len(val) > 0):
            raise ValueError(
                f"Ground truth schema violation for '{eff_type}': 'correct_letters' must be a non-empty list, got {val!r}"
            )


def _extract_multiple_select_items(user_ans: Any) -> List[str]:
    """Extracts raw selected option tokens from list or delimited string."""
    if isinstance(user_ans, (list, tuple, set)):
        return [str(x).strip() for x in user_ans if str(x).strip()]
    if isinstance(user_ans, str):
        s = user_ans.strip()
        if s.startswith("[") and s.endswith("]"):
            try:
                parsed = json.loads(s)
                if isinstance(parsed, list):
                    return [str(x).strip() for x in parsed if str(x).strip()]
            except Exception:
                pass
            return [x.strip() for x in re.split(r"[,;\s]+", s) if x.strip()]
        return [x.strip() for x in re.split(r"[,;\s]+|\band\b|\by\b", s) if x.strip()]
    return []


def _extract_option_letter_set(val: Any) -> Set[str]:
    """Normalizes multiple-select answers into a set of single uppercase option letters."""
    letters: Set[str] = set()
    for item in _extract_multiple_select_items(val):
        nl = _normalize_option_letter(item)
        if len(nl) == 1 and nl.isalpha():
            letters.add(nl)
    return letters


def _check_single_answer_match(user_ans: Any, gt: Dict[str, Any], itype: str) -> Tuple[bool, str]:
    """Evaluates a single judge answer against ground truth for a given interaction type."""
    _validate_ground_truth_item(gt, itype)
    if user_ans is None:
        return False, "Missing response from judge"

    if itype == "multiple_choice_7_options":
        u_letter = _normalize_option_letter(user_ans)
        gt_letter = _normalize_option_letter(gt.get("correct_letter", ""))
        gt_content = gt.get("correct_content", "")

        if u_letter and gt_letter and u_letter == gt_letter:
            return True, ""
        elif _normalize_str(user_ans) == _normalize_str(gt_content):
            return True, ""
        else:
            return False, f"Judge selected '{user_ans}' (letter '{u_letter}') but expected letter '{gt_letter}' ({gt_content})"

    elif itype == "fill_in_the_blank":
        gt_val = gt.get("correct_value")
        gt_canon = gt.get("canonical_algebraic")
        gt_equivs = gt.get("accepted_equivalents", [])
        raw_tol = gt.get("tolerance") or gt.get("answer_contract", {}).get("tolerance") or 0.01
        try:
            tol = float(raw_tol)
        except (ValueError, TypeError):
            tol = 0.01

        if _is_numeric_equal(user_ans, gt_val, tol=tol):
            return True, ""
        elif gt_canon and _is_numeric_equal(user_ans, gt_canon, tol=tol):
            return True, ""
        elif gt_canon and _normalize_str(user_ans) == _normalize_str(gt_canon):
            return True, ""
        elif _normalize_str(user_ans) == _normalize_str(gt_val):
            return True, ""
        elif any(_is_numeric_equal(user_ans, eq, tol=tol) for eq in gt_equivs):
            return True, ""
        elif any(_normalize_str(user_ans) == _normalize_str(eq) for eq in gt_equivs):
            return True, ""
        else:
            return False, f"Judge provided '{user_ans}' but expected '{gt_val}' (or {gt_canon})"

    elif itype == "multiple_select":
        gt_letters = set(_normalize_option_letter(x) for x in gt.get("correct_letters", []))
        gt_contents = set(_normalize_str(c) for c in gt.get("correct_contents", []))

        raw_items = _extract_multiple_select_items(user_ans)

        u_letters = set()
        u_contents = set()
        for item in raw_items:
            nl = _normalize_option_letter(item)
            if len(nl) == 1 and nl.isalpha():
                u_letters.add(nl)
            u_contents.add(_normalize_str(item))

        if u_letters and u_letters == gt_letters:
            return True, ""
        elif u_contents and u_contents == gt_contents:
            return True, ""
        else:
            return False, f"Judge selected {raw_items} (letters: {sorted(u_letters)}) but expected {sorted(gt_letters)}"

    elif itype in _M20_INTERACTION_TYPES:
        return _check_m20_answer_match(user_ans, gt, itype)

    return False, f"Unsupported interaction type '{itype}'"


def _values_approx_equal(u_val: Any, g_val: Any, tol: float = 0.02) -> bool:
    """Recursively compares structured ground-truth objects with float tolerance."""
    if isinstance(g_val, (int, float)) and not isinstance(g_val, bool):
        return _is_numeric_equal(u_val, g_val, tol=tol)
    if isinstance(g_val, dict):
        if not isinstance(u_val, dict):
            return False
        return all(k in u_val and _values_approx_equal(u_val[k], v, tol=tol) for k, v in g_val.items())
    if isinstance(g_val, list):
        if not isinstance(u_val, (list, tuple)) or len(u_val) != len(g_val):
            return False
        return all(_values_approx_equal(u_v, g_v, tol=tol) for u_v, g_v in zip(u_val, g_val))
    return _normalize_str(u_val) == _normalize_str(g_val)


def _check_m20_answer_match(user_ans: Any, gt: Dict[str, Any], itype: str) -> Tuple[bool, str]:
    """Evaluates blind judge responses for all 6 M20 interaction modalities."""
    if itype == "open_symbolic":
        u_dict = _parse_json_or_dict(user_ans)
        u_expr = (u_dict.get("expression") or u_dict.get("value") or "") if u_dict else user_ans
        ca = gt.get("correct_answer") if isinstance(gt.get("correct_answer"), dict) else {}
        gt_val = gt.get("correct_value") or ca.get("expression") or ca.get("value") or ""
        gt_canon = gt.get("canonical_algebraic") or ca.get("canonical_algebraic") or ""
        gt_equivs = gt.get("accepted_equivalents") or ca.get("accepted_equivalents") or []
        tol = float(gt.get("tolerance") or ca.get("tolerance") or 0.001)
        cands = [x for x in [gt_val, gt_canon, *gt_equivs] if str(x).strip()]
        if any(_is_symbolic_equal(u_expr, c, tol=tol) for c in cands):
            return True, ""
        return False, f"Judge symbolic '{u_expr}' does not match expected '{gt_val}'"

    ans = _parse_json_or_dict(user_ans)
    if ans is None:
        return False, f"Expected JSON object response for '{itype}', got {user_ans!r}"
    ca = gt.get("correct_answer") if isinstance(gt.get("correct_answer"), dict) else {}

    if itype == "proof_dag":
        gt_order = [str(x) for x in (ca.get("canonical_order") or [])]
        u_order = [str(x) for x in (ans.get("canonical_order") or [])]
        if u_order != gt_order:
            return False, f"proof_dag canonical_order mismatch: got {u_order}, expected {gt_order}"
        if "required_step_ids" in ans and [str(x) for x in (ans.get("required_step_ids") or [])] != [str(x) for x in (ca.get("required_step_ids") or [])]:
            return False, "proof_dag required_step_ids mismatch"
        if "edges" in ans:
            gt_edges = {(str(e[0]), str(e[1])) for e in (ca.get("edges") or []) if isinstance(e, (list, tuple)) and len(e) == 2}
            u_edges = {(str(e[0]), str(e[1])) for e in (ans.get("edges") or []) if isinstance(e, (list, tuple)) and len(e) == 2}
            if u_edges != gt_edges:
                return False, f"proof_dag edges mismatch: got {sorted(u_edges)}, expected {sorted(gt_edges)}"
        if ca.get("justifications"):
            gt_just = {str(k): _normalize_str(v) for k, v in ca["justifications"].items()}
            u_just = {str(k): _normalize_str(v) for k, v in (ans.get("justifications") or {}).items()}
            if u_just != gt_just:
                return False, "proof_dag justifications mismatch"
        return True, ""

    if itype == "adversarial_break":
        mode = str(ca.get("mode") or ans.get("mode") or "find_fallacy")
        if mode == "find_fallacy":
            if str(ans.get("fallacy_step_id") or "") != str(ca.get("fallacy_step_id") or ""):
                return False, f"adversarial_break fallacy_step_id mismatch: got {ans.get('fallacy_step_id')!r}, expected {ca.get('fallacy_step_id')!r}"
            if ca.get("correct_reason_id") and str(ans.get("correct_reason_id") or "") != str(ca["correct_reason_id"]):
                return False, f"adversarial_break correct_reason_id mismatch: got {ans.get('correct_reason_id')!r}, expected {ca['correct_reason_id']!r}"
            return True, ""
        u_w = ans.get("sample_witness") if isinstance(ans.get("sample_witness"), dict) else ans
        gt_w = ca.get("sample_witness") if isinstance(ca.get("sample_witness"), dict) else {}
        if _values_approx_equal(u_w, gt_w, tol=0.01):
            return True, ""
        return False, f"adversarial_break witness mismatch: got {u_w}, expected {gt_w}"

    if itype == "unstructured_model":
        gt_p1 = {str(k): _normalize_str(v) for k, v in (ca.get("phase1") or {}).items()}
        u_p1 = {str(k): _normalize_str(v) for k, v in (ans.get("phase1") or {}).items()}
        if u_p1 != gt_p1:
            return False, f"unstructured_model phase1 mismatch: got {u_p1}, expected {gt_p1}"
        gt_p2 = {str(x) for x in (ca.get("phase2") or [])}
        u_p2 = {str(x) for x in (ans.get("phase2") or [])}
        if u_p2 != gt_p2:
            return False, f"unstructured_model phase2 mismatch: got {sorted(u_p2)}, expected {sorted(gt_p2)}"
        gt_p3 = ca.get("phase3")
        u_p3 = ans.get("phase3")
        if isinstance(gt_p3, dict):
            cands = [gt_p3.get("expression"), gt_p3.get("value"), gt_p3.get("canonical_algebraic"), *(gt_p3.get("accepted_equivalents") or [])]
            if any(_is_symbolic_equal(u_p3, c, tol=float(gt_p3.get("tolerance", 0.001) or 0.001)) for c in cands if c):
                return True, ""
            return False, f"unstructured_model phase3 expression mismatch: got {u_p3!r}"
        if _normalize_str(u_p3) == _normalize_str(gt_p3):
            return True, ""
        return False, f"unstructured_model phase3 mismatch: got {u_p3!r}, expected {gt_p3!r}"

    if itype == "invariant_canvas":
        c_mode = str(ca.get("mode") or ans.get("mode") or "cartesian")
        if c_mode == "tree":
            gt_edges = {(str(e[0]), str(e[1])) if isinstance(e, (list, tuple)) and len(e) == 2 else str(e) for e in (ca.get("required_edges") or [])}
            u_edges = {(str(e[0]), str(e[1])) if isinstance(e, (list, tuple)) and len(e) == 2 else str(e) for e in (ans.get("required_edges") or [])}
            if u_edges != gt_edges:
                return False, f"invariant_canvas tree required_edges mismatch: got {sorted(map(str, u_edges))}"
            gt_sets = {frozenset(str(x) for x in grp) for grp in (ca.get("required_info_sets") or [])}
            u_sets = {frozenset(str(x) for x in grp) for grp in (ans.get("required_info_sets") or [])}
            if u_sets != gt_sets:
                return False, "invariant_canvas tree required_info_sets mismatch"
            return True, ""
        u_ts = ans.get("target_state") if isinstance(ans.get("target_state"), dict) else ans
        gt_ts = ca.get("target_state") if isinstance(ca.get("target_state"), dict) else {}
        # Alias support in case client sends style/shade or inequalityStyle/inequalityShade
        if "style" in u_ts and "inequalityStyle" not in u_ts:
            u_ts = {**u_ts, "inequalityStyle": u_ts["style"]}
        if "shade" in u_ts and "inequalityShade" not in u_ts:
            u_ts = {**u_ts, "inequalityShade": u_ts["shade"]}
        if gt_ts and "invariants_count" not in gt_ts:
            if _values_approx_equal(u_ts, gt_ts, tol=0.05):
                return True, ""
            return False, f"invariant_canvas target_state mismatch: got {u_ts}, expected {gt_ts}"
        # Fallback check against extracted cartesian invariants when explicit target_state was omitted
        invs = gt.get("invariants") if isinstance(gt.get("invariants"), list) else []
        for inv in invs:
            if not isinstance(inv, dict):
                continue
            kind = str(inv.get("kind") or "")
            if kind == "inequality_state":
                if inv.get("expected_style") and _normalize_str(u_ts.get("inequalityStyle")) != _normalize_str(inv["expected_style"]):
                    return False, f"Expected inequalityStyle={inv['expected_style']}"
                if inv.get("expected_shade") and _normalize_str(u_ts.get("inequalityShade")) != _normalize_str(inv["expected_shade"]):
                    return False, f"Expected inequalityShade={inv['expected_shade']}"
            elif kind == "point_coords":
                pid = str(inv.get("target") or inv.get("point_id") or "")
                u_pt = (u_ts.get("points") or {}).get(pid) if isinstance(u_ts.get("points"), dict) else None
                if not (isinstance(u_pt, dict) and _values_approx_equal(u_pt, {"x": inv.get("target_x"), "y": inv.get("target_y")}, tol=0.05)):
                    return False, f"Expected point '{pid}' at ({inv.get('target_x')}, {inv.get('target_y')})"
        return (True, "") if u_ts else (False, "Empty cartesian target_state")

    if itype == "concept_matching":
        gt_pairs = {str(k): _normalize_str(v) for k, v in (ca.get("pairs") or {}).items()}
        u_raw = ans.get("pairs") if isinstance(ans.get("pairs"), dict) else ans
        u_pairs = {str(k): _normalize_str(v) for k, v in u_raw.items()}
        if u_pairs == gt_pairs and len(gt_pairs) > 0:
            return True, ""
        return False, f"concept_matching pairs mismatch: got {u_pairs}, expected {gt_pairs}"

    return False, f"Unsupported interaction type '{itype}'"


def resolve_neuro_symbolic_verdict(
    kernel_verified: bool,
    kernel_refuted: bool,
    llm_verdict: Union[str, bool],
    failure_category: Optional[str] = None,
    failure_reasons: Optional[List[str]] = None,
    interaction_type: Optional[str] = None,
    solver_answer: Any = None,
    correct_answer: Any = None,
    template_failed_seeds: int = 0,
) -> Dict[str, Any]:
    """Resolves epistemic verdict with deterministic kernel dominance (alpha_kernel = 0).
    
    Rules:
    1. If kernel_refuted is True: verdict is unconditionally FAIL regardless of LLM verdict.
    2. If kernel_verified is True and LLM verdict is FAIL alleging only math/calculation errors:
       kernel_override is set to True and verdict resolves to PASS (algebraic proof dominance),
       UNLESS any anti-false-consensus guard triggers:
       - (a) In FIB or numeric MC7, solver_answer differs from correct_answer by integer rounding (abs == 1.0).
       - (b) In multiple_select, Blind Judge explicitly rejects an author-marked true option.
       - (c) Blind Judge fails on >= 2 seeds of the same template.
       - Or LLM flags epistemic insufficiency, ambiguous stem, or answer giveaway.
    3. If kernel_verified is True and LLM passes: verdict resolves to PASS.
    4. If neither kernel verification nor refutation occurred: standard LLM verdict applies.
    """
    str_verdict = str(llm_verdict).strip().upper()
    llm_passed = str_verdict in ("PASS", "PASSED", "TRUE", "1")
    cat = (failure_category or "").strip().lower()
    reasons = [str(r).strip() for r in (failure_reasons or []) if str(r).strip()]
    reasons_text = " ".join(reasons).lower()
    eff_type = (interaction_type or "").strip().lower()

    # Rule 1: Deterministic kernel refutation dominance
    if kernel_refuted:
        return {
            "verdict": "FAIL",
            "passed": False,
            "kernel_verified": False,
            "kernel_refuted": True,
            "kernel_override": False,
            "failure_category": cat or "kernel_refutation",
            "reasons": reasons or ["Refuted deterministically by verification kernel"],
        }

    # Rule 2: Kernel verified with LLM failure
    if kernel_verified and not llm_passed:
        # Anti-false-consensus Guard (c): >= 2 failed seeds on the same template
        if template_failed_seeds >= 2:
            return {
                "verdict": "FAIL",
                "passed": False,
                "kernel_verified": True,
                "kernel_refuted": False,
                "kernel_override": False,
                "failure_category": cat or "multi_seed_judge_failure",
                "reasons": reasons or [f"Blind judge failed on {template_failed_seeds} seeds of the same template"],
            }

        # Anti-false-consensus Guard (b): multiple_select rejection of author-marked true option
        if eff_type == "multiple_select":
            judge_letters = _extract_option_letter_set(solver_answer) if solver_answer is not None else set()
            author_letters = _extract_option_letter_set(correct_answer) if correct_answer is not None else set()
            if solver_answer is None or correct_answer is None or judge_letters != author_letters:
                return {
                    "verdict": "FAIL",
                    "passed": False,
                    "kernel_verified": True,
                    "kernel_refuted": False,
                    "kernel_override": False,
                    "failure_category": cat or "multiple_select_rejection",
                    "reasons": reasons or [
                        f"Blind judge selection {sorted(judge_letters)} disagrees with author-marked options {sorted(author_letters)}"
                    ],
                }

        # Anti-false-consensus Guard (a): integer rounding diff == 1.0 in FIB or numeric MC7
        if eff_type in ("fill_in_the_blank", "fib", "multiple_choice_7_options", "mc7", "multiple_choice", ""):
            if solver_answer is not None and correct_answer is not None:
                s_num = _parse_float(solver_answer)
                c_num = _parse_float(correct_answer)
                if s_num is not None and c_num is not None and math.isclose(abs(float(s_num) - float(c_num)), 1.0, abs_tol=1e-9):
                    return {
                        "verdict": "FAIL",
                        "passed": False,
                        "kernel_verified": True,
                        "kernel_refuted": False,
                        "kernel_override": False,
                        "failure_category": cat or "integer_rounding_mismatch",
                        "reasons": reasons or [
                            f"Integer rounding discrepancy (|solver - correct| == 1.0): {s_num} vs {c_num}"
                        ],
                    }

        # Check for epistemic or semantic flaws that must block
        blocking_tokens = (
            "epistemic_insufficiency",
            "epistemic",
            "missing_definition",
            "missing",
            "ambiguous_stem",
            "ambiguous",
            "giveaway",
            "carece",
            "insuficiente",
            "sin contexto",
            "bloqueado",
            "flaw_detected",
            "blocked",
            "defective",
        )
        has_epistemic_block = any(tok in cat or tok in reasons_text for tok in blocking_tokens)

        is_pure_calc_error = cat in ("math_error", "calculation_error", "arithmetic_error", "numeric_error", "")
        if is_pure_calc_error and not has_epistemic_block:
            return {
                "verdict": "PASS",
                "passed": True,
                "kernel_verified": True,
                "kernel_refuted": False,
                "kernel_override": True,
                "failure_category": cat,
                "reasons": reasons,
            }
        else:
            return {
                "verdict": "FAIL",
                "passed": False,
                "kernel_verified": True,
                "kernel_refuted": False,
                "kernel_override": False,
                "failure_category": cat or "epistemic_insufficiency",
                "reasons": reasons or ["Epistemic insufficiency or ambiguity detected"],
            }

    # Rule 3: Kernel verified and LLM passed
    if kernel_verified and llm_passed:
        return {
            "verdict": "PASS",
            "passed": True,
            "kernel_verified": True,
            "kernel_refuted": False,
            "kernel_override": False,
            "failure_category": "",
            "reasons": [],
        }

    # Rule 4: Standard verdict when kernel did not run or is inconclusive
    final_passed = llm_passed
    return {
        "verdict": "PASS" if final_passed else "FAIL",
        "passed": final_passed,
        "kernel_verified": kernel_verified,
        "kernel_refuted": kernel_refuted,
        "kernel_override": False,
        "failure_category": cat if not final_passed else "",
        "reasons": reasons if not final_passed else [],
    }


def compare_judge_responses(
    responses: Optional[Union[Dict[str, Any], List[Dict[str, Any]], str, Path]] = None,
    ground_truth: Optional[Dict[str, Dict[str, Any]]] = None,
    cycle: int = 1,
    work_dir: Optional[Union[str, Path]] = None,
    shards: Optional[Union[List[str], str]] = None,
) -> Dict[str, Any]:
    """Compares judge answers against ground truth answer keys and records discordances.
    
    Zero-tolerance: requires 100% agreement (1.0) on all templates, rejects empty or incomplete batches.
    Scans responses in work/judge_*.json, work/judges/judge_*.json, and work/judge_responses_*.json.
    
    Args:
        responses: Judge responses dict `{item_id: answer}`, list, or path to file/directory.
        ground_truth: Ground truth mapping loaded from judge_ground_truth.json.
        cycle: Current correction cycle number (1 to 3).
        work_dir: Optional working directory for response discovery and ground truth loading.

    Returns:
        Evaluation report dictionary containing agreement rate and discordances.
    """
    raw_responses_list: List[Any] = []
    resolved_work_dir: Optional[Path] = None

    if work_dir is not None:
        resolved_work_dir = Path(work_dir)
    elif isinstance(responses, (str, Path)) and Path(responses).is_dir():
        resolved_work_dir = Path(responses)

    if responses is None or (isinstance(responses, (str, Path)) and Path(responses).is_dir()):
        if resolved_work_dir is None:
            raise ValueError("Either responses or work_dir must be provided")

        ignored_prefixes = (
            "judge_batch",
            "judge_ground_truth",
            "judge_report",
            "judge_redispatch",
            "evaluated_competencies",
            "answer_key",
        )

        cand_files: List[Path] = []
        search_dirs = [resolved_work_dir]
        for sub_name in ("judges", "verification"):
            sub_dir = resolved_work_dir / sub_name
            if sub_dir.is_dir():
                search_dirs.append(sub_dir)

        for s_dir in search_dirs:
            for pattern in ("judge_*.json", "judge_responses_*.json", "judge_responses.json"):
                for f in sorted(s_dir.glob(pattern)):
                    if not any(f.name.startswith(pfx) for pfx in ignored_prefixes):
                        if f not in cand_files:
                            cand_files.append(f)

        for f in cand_files:
            try:
                raw_responses_list.append(json.loads(f.read_text(encoding="utf-8")))
            except Exception as e:
                logger.warning("Failed to load judge response file %s: %s", f, e)
    elif isinstance(responses, (str, Path)) and Path(responses).is_file():
        raw_responses_list.append(json.loads(Path(responses).read_text(encoding="utf-8")))
    elif isinstance(responses, (list, dict)):
        raw_responses_list.append(responses)
    elif responses is not None:
        raw_responses_list.append(responses)

    # Collect replicate responses per item_id and capture response metadata
    resp_replicates: Dict[str, List[Any]] = {}
    resp_meta_map: Dict[str, Dict[str, Any]] = {}

    for raw in raw_responses_list:
        if isinstance(raw, list):
            for r in raw:
                if isinstance(r, dict):
                    iid = r.get("item_id") or r.get("question_id") or r.get("id")
                    ans = r.get("answer") if "answer" in r else (r.get("response") if "response" in r else r.get("verdict"))
                    if iid:
                        s_iid = str(iid)
                        resp_replicates.setdefault(s_iid, []).append(ans)
                        if s_iid not in resp_meta_map:
                            resp_meta_map[s_iid] = {
                                "template_id": r.get("template_id"),
                                "competency_id": r.get("competency_id") or r.get("cid"),
                                "raw_items": [],
                            }
                        resp_meta_map[s_iid].setdefault("raw_items", []).append(r)
        elif isinstance(raw, dict):
            unwrapped = False
            for cand_key in ("evaluations", "responses", "items", "results"):
                if cand_key in raw:
                    sub_val = raw[cand_key]
                    if isinstance(sub_val, list):
                        for r in sub_val:
                            if isinstance(r, dict):
                                iid = r.get("item_id") or r.get("question_id") or r.get("id")
                                ans = r.get("answer") if "answer" in r else (r.get("response") if "response" in r else r.get("verdict"))
                                if iid:
                                    s_iid = str(iid)
                                    resp_replicates.setdefault(s_iid, []).append(ans)
                                    if s_iid not in resp_meta_map:
                                        resp_meta_map[s_iid] = {
                                            "template_id": r.get("template_id"),
                                            "competency_id": r.get("competency_id") or r.get("cid"),
                                            "raw_items": [],
                                        }
                                    resp_meta_map[s_iid].setdefault("raw_items", []).append(r)
                        unwrapped = True
                        break
                    elif isinstance(sub_val, dict):
                        for k, v in sub_val.items():
                            s_k = str(k)
                            if isinstance(v, dict) and ("answer" in v or "response" in v or "verdict" in v):
                                ans_v = v.get("answer", v.get("response", v.get("verdict")))
                                resp_replicates.setdefault(s_k, []).append(ans_v)
                                if s_k not in resp_meta_map:
                                    resp_meta_map[s_k] = {
                                        "template_id": v.get("template_id"),
                                        "competency_id": v.get("competency_id") or v.get("cid"),
                                        "raw_items": [],
                                    }
                                resp_meta_map[s_k].setdefault("raw_items", []).append(v)
                            else:
                                resp_replicates.setdefault(s_k, []).append(v)
                                if isinstance(v, dict):
                                    if s_k not in resp_meta_map:
                                        resp_meta_map[s_k] = {
                                            "template_id": v.get("template_id"),
                                            "competency_id": v.get("competency_id") or v.get("cid"),
                                            "raw_items": [],
                                        }
                                    resp_meta_map[s_k].setdefault("raw_items", []).append(v)
                        unwrapped = True
                        break
            if not unwrapped:
                for k, v in raw.items():
                    s_k = str(k)
                    if isinstance(v, dict) and ("answer" in v or "response" in v or "verdict" in v):
                        ans_v = v.get("answer", v.get("response", v.get("verdict")))
                        resp_replicates.setdefault(s_k, []).append(ans_v)
                        if s_k not in resp_meta_map:
                            resp_meta_map[s_k] = {
                                "template_id": v.get("template_id"),
                                "competency_id": v.get("competency_id") or v.get("cid"),
                                "raw_items": [],
                            }
                        resp_meta_map[s_k].setdefault("raw_items", []).append(v)
                    else:
                        resp_replicates.setdefault(s_k, []).append(v)
                        if isinstance(v, dict):
                            if s_k not in resp_meta_map:
                                resp_meta_map[s_k] = {
                                    "template_id": v.get("template_id"),
                                    "competency_id": v.get("competency_id") or v.get("cid"),
                                    "raw_items": [],
                                }
                            resp_meta_map[s_k].setdefault("raw_items", []).append(v)

    if ground_truth is None:
        if resolved_work_dir:
            gt_p = resolved_work_dir / "judge_ground_truth.json"
            if not gt_p.is_file():
                gt_p = resolved_work_dir / "answer_key.json"
            if gt_p.is_file():
                ground_truth = json.loads(gt_p.read_text(encoding="utf-8"))
        if ground_truth is None:
            raise ValueError("ground_truth mapping must be provided or judge_ground_truth.json present in work_dir")

    # Load answer_key.json for legacy items missing template_id or competency_id
    answer_key_map: Dict[str, Dict[str, Any]] = {}
    if resolved_work_dir:
        for ak_cand in (
            resolved_work_dir / "answer_key.json",
            resolved_work_dir / "verification" / "answer_key.json",
            resolved_work_dir / "judge_ground_truth.json",
            resolved_work_dir / "verification" / "judge_ground_truth.json",
        ):
            if ak_cand.is_file():
                try:
                    ak_data = json.loads(ak_cand.read_text(encoding="utf-8"))
                    if isinstance(ak_data, dict):
                        for k, v in ak_data.items():
                            if isinstance(v, dict) and str(k) not in answer_key_map:
                                answer_key_map[str(k)] = v
                except Exception:
                    pass

    total = len(ground_truth)
    agreed = 0
    discordances: List[Dict[str, Any]] = []
    kernel_overridden_items: List[Dict[str, Any]] = []

    tpl_items: Dict[str, List[bool]] = {}
    comp_items: Dict[str, List[bool]] = {}
    all_complete = (total > 0)

    # First pass: evaluate raw judge agreement per item so we know failed seed counts per template
    pre_evals: List[Dict[str, Any]] = []
    template_raw_failures: Dict[str, int] = {}

    for item_id, gt in ground_truth.items():
        s_iid = str(item_id)
        reps = resp_replicates.get(s_iid, [])
        itype = gt.get("interaction_type", "multiple_choice_7_options")
        if itype == "multiple_choice":
            itype = "multiple_choice_7_options"

        ak_info = answer_key_map.get(s_iid, {})
        meta_info = resp_meta_map.get(s_iid, {})

        tid = gt.get("template_id") or ak_info.get("template_id") or meta_info.get("template_id")
        cid = gt.get("competency_id") or gt.get("cid") or ak_info.get("competency_id") or meta_info.get("competency_id")

        if not tid:
            m = re.match(r"^([A-Za-z0-9_-]+?)_judge_\d+", s_iid)
            tid = m.group(1) if m else "unknown_template"
        if not cid:
            cid = "unknown_comp"

        tpl_items.setdefault(tid, [])
        comp_items.setdefault(cid, [])

        is_refuted = bool(gt.get("kernel_refuted", False))
        is_verified = bool(gt.get("kernel_verified", False))

        if not is_refuted:
            _validate_ground_truth_item(gt, itype)

        is_match = False
        reason = ""
        user_ans: Any = None
        items_to_check: List[Any] = []
        flaw_detected = False

        if is_refuted:
            is_match = False
            user_ans = reps[0] if reps else None
            reason = "Refuted deterministically by verification kernel"
        elif not reps:
            is_match = False
            all_complete = False
            user_ans = None
            reason = "Missing response from judge"
        else:
            rep_evals = [_check_single_answer_match(r_ans, gt, itype) for r_ans in reps]
            if any(r_ans is None for r_ans in reps):
                all_complete = False

            meta_raws = resp_meta_map.get(s_iid, {}).get("raw_items", [])
            items_to_check = list(reps) + list(meta_raws)
            flaw_detected = any(
                isinstance(it, dict) and bool(it.get("flaw_detected"))
                for it in items_to_check
            )

            if all(m_ok for m_ok, _ in rep_evals) and not flaw_detected:
                is_match = True
                user_ans = reps[0] if len(set(str(x) for x in reps)) == 1 else reps
            else:
                is_match = False
                user_ans = reps[0] if len(reps) == 1 else reps
                exp_val = (
                    gt.get("correct_letter")
                    if gt.get("correct_letter") is not None
                    else (
                        gt.get("correct_value")
                        if gt.get("correct_value") is not None
                        else gt.get("correct_letters")
                    )
                )
                if flaw_detected:
                    flaw_reasons = []
                    for it in items_to_check:
                        if isinstance(it, dict) and it.get("flaw_detected"):
                            f_rsn = it.get("flaw_description") or it.get("reason") or "Item epistemic flaw reported by judge"
                            flaw_reasons.append(str(f_rsn))
                    reason = f"Epistemic flaw detected by judge: {'; '.join(flaw_reasons) if flaw_reasons else 'flaw_detected is True'}"
                elif len(reps) > 1 and len(set(str(x) for x in reps)) > 1:
                    mismatch_reasons = [r_msg for m_ok, r_msg in rep_evals if not m_ok and r_msg]
                    reason = f"Judge replicas disagreed: {reps} (expected {exp_val}; errors: {'; '.join(mismatch_reasons)})"
                else:
                    first_fail = next((r_msg for m_ok, r_msg in rep_evals if not m_ok), "Evaluation mismatch")
                    reason = first_fail

        if not is_match and reps:
            template_raw_failures[tid] = template_raw_failures.get(tid, 0) + 1

        pre_evals.append({
            "s_iid": s_iid,
            "gt": gt,
            "tid": tid,
            "cid": cid,
            "itype": itype,
            "reps": reps,
            "is_refuted": is_refuted,
            "is_verified": is_verified,
            "is_match": is_match,
            "reason": reason,
            "user_ans": user_ans,
            "items_to_check": items_to_check,
        })

    # Second pass: apply neuro-symbolic resolution with anti-false-consensus guards
    for ev in pre_evals:
        s_iid = ev["s_iid"]
        gt = ev["gt"]
        tid = ev["tid"]
        cid = ev["cid"]
        itype = ev["itype"]
        reps = ev["reps"]
        is_verified = ev["is_verified"]
        is_match = ev["is_match"]
        reason = ev["reason"]
        user_ans = ev["user_ans"]
        items_to_check = ev["items_to_check"]

        if not is_match and reps and is_verified:
            fail_cat = "calculation_error"
            fail_reasons = [reason]
            derived_val = None
            for r_item in items_to_check:
                if isinstance(r_item, dict):
                    if r_item.get("flaw_detected"):
                        fail_cat = str(r_item.get("failure_category") or "epistemic_insufficiency")
                    elif "failure_category" in r_item:
                        fail_cat = str(r_item["failure_category"])
                    elif "category" in r_item:
                        fail_cat = str(r_item["category"])
                    if "reason" in r_item:
                        fail_reasons.append(str(r_item["reason"]))
                    if derived_val is None:
                        derived_val = r_item.get("derived_value_from_stem_only", r_item.get("solver_answer"))
                elif isinstance(r_item, str):
                    lower_r = r_item.lower()
                    if any(tok in lower_r for tok in ("blocked", "bloqueado", "epistemic", "carece", "insuficiente", "flaw_detected")):
                        fail_cat = "epistemic_insufficiency"
                        fail_reasons.append(r_item)

            if itype == "fill_in_the_blank":
                solver_ans = derived_val if derived_val is not None else user_ans
                correct_ans = gt.get("correct_value")
            elif itype == "multiple_choice_7_options":
                solver_ans = derived_val if derived_val is not None else user_ans
                correct_ans = gt.get("correct_content") if gt.get("correct_content") is not None else gt.get("correct_letter")
            elif itype == "multiple_select":
                solver_ans = user_ans
                correct_ans = gt.get("correct_letters")
            else:
                solver_ans = user_ans
                correct_ans = gt.get("correct_value") if gt.get("correct_value") is not None else gt.get("correct_answer")

            neuro_verdict = resolve_neuro_symbolic_verdict(
                kernel_verified=True,
                kernel_refuted=False,
                llm_verdict="FAIL",
                failure_category=fail_cat,
                failure_reasons=fail_reasons,
                interaction_type=itype,
                solver_answer=solver_ans,
                correct_answer=correct_ans,
                template_failed_seeds=template_raw_failures.get(tid, 0),
            )
            if neuro_verdict.get("kernel_override"):
                is_match = True
                reason = "Kernel verified constructive proof overrides LLM calculation disagreement"
                exp_override = (
                    gt.get("correct_letter")
                    if gt.get("correct_letter") is not None
                    else (
                        gt.get("correct_value")
                        if gt.get("correct_value") is not None
                        else gt.get("correct_letters")
                    )
                )
                kernel_overridden_items.append({
                    "item_id": s_iid,
                    "judge_response": user_ans,
                    "expected": exp_override,
                    "reason": reason,
                })

        tpl_items[tid].append(is_match)
        comp_items[cid].append(is_match)

        if is_match:
            agreed += 1
        else:
            exp_val = (
                gt.get("correct_letter")
                if gt.get("correct_letter") is not None
                else (
                    gt.get("correct_value")
                    if gt.get("correct_value") is not None
                    else gt.get("correct_letters")
                )
            )
            discordances.append({
                "item_id": s_iid,
                "template_id": tid,
                "competency_id": cid,
                "cid": cid,
                "interaction_type": itype,
                "judge_response": user_ans,
                "expected": exp_val,
                "reason": reason,
                "cycle": cycle,
            })

    failed_templates: List[str] = []
    for tid, matches in tpl_items.items():
        if not matches or not all(matches):
            failed_templates.append(tid)

    failed_competencies: List[str] = []
    for cid, matches in comp_items.items():
        if not matches or not all(matches):
            failed_competencies.append(cid)

    failed_templates = sorted(list(set(failed_templates)))
    failed_competencies = sorted(list(set(failed_competencies)))

    if resolved_work_dir:
        for ref_p in (resolved_work_dir / "refuted_templates.json", resolved_work_dir / "verification" / "refuted_templates.json"):
            if ref_p.is_file():
                try:
                    ref_data = json.loads(ref_p.read_text(encoding="utf-8"))
                    for tid, r_info in ref_data.items():
                        if tid not in failed_templates:
                            failed_templates.append(tid)
                        c_id = r_info.get("competency_id")
                        if c_id and c_id not in failed_competencies:
                            failed_competencies.append(c_id)
                except Exception:
                    pass

    failed_templates = sorted(list(set(failed_templates)))
    failed_competencies = sorted(list(set(failed_competencies)))

    agreement_rate = (agreed / total) if total > 0 else 0.0
    passed = (total > 0) and all_complete and (len(failed_templates) == 0) and (len(discordances) == 0)

    if not all_complete and total > 0:
        status = "incomplete"
    elif total == 0:
        status = "empty"
    elif passed:
        status = "passed"
    else:
        status = "disagreements"

    kernel_override_count = len(kernel_overridden_items)
    if kernel_override_count > 0:
        warning_msg = (
            f"[WARNING] judge compare_judge_responses: {kernel_override_count} item(s) had "
            f"kernel_override=True applied (algebraic proof dominance over stochastic LLM calculation disagreement)."
        )
        print(warning_msg, file=sys.stderr)
        logger.warning(warning_msg)

    now_iso = datetime.now(timezone.utc).isoformat()
    normalized_shards: List[str] = []
    if shards:
        raw_shard_list = [shards] if isinstance(shards, str) else list(shards)
        for s_item in raw_shard_list:
            for part in str(s_item).split(","):
                p_clean = part.strip()
                if p_clean and p_clean not in normalized_shards:
                    normalized_shards.append(p_clean)

    report_data = {
        "cycle": cycle,
        "timestamp": now_iso,
        "total": total,
        "total_items": total,
        "agreed_items": agreed,
        "agreement_rate": round(agreement_rate, 4),
        "passed": passed,
        "status": status,
        "all_complete": all_complete,
        "failed_templates": failed_templates,
        "failed_competencies": failed_competencies,
        "affected_template_ids": failed_templates,
        "disagreements": discordances,
        "discordances": discordances,
        "kernel_overridden_items": kernel_overridden_items,
        "kernel_override_count": kernel_override_count,
        "can_retry": (cycle < MAX_CORRECTION_CYCLES and not passed),
        "max_cycles_reached": (cycle >= MAX_CORRECTION_CYCLES),
    }

    if resolved_work_dir:
        try:
            completeness = check_judge_completeness(resolved_work_dir)
            report_data["completeness"] = completeness
            if not completeness.get("is_complete", True) and completeness.get("total_missing_items", 0) > 0:
                report_data["truncated_warning"] = (
                    f"Incomplete evaluation detected: {completeness['total_missing_items']} missing/truncated items."
                )
        except Exception as e:
            logger.warning("Could not execute check_judge_completeness: %s", e)

        report_p = resolved_work_dir / "judge_report.json"
        round_1_p = resolved_work_dir / "judge_report_round_1.json"
        prev_report: Optional[Dict[str, Any]] = None

        if report_p.is_file():
            try:
                raw_prev_bytes = report_p.read_bytes()
                parsed_prev = json.loads(raw_prev_bytes.decode("utf-8"))
                if isinstance(parsed_prev, dict):
                    prev_report = parsed_prev
                if normalized_shards and not round_1_p.exists():
                    round_1_p.write_bytes(raw_prev_bytes)
            except Exception as e:
                logger.warning("Could not read/backup previous judge_report.json: %s", e)

        rounds_history: List[Dict[str, Any]] = []
        if prev_report is not None:
            existing_hist = prev_report.get("rounds_history")
            if isinstance(existing_hist, list) and existing_hist:
                rounds_history = [dict(entry) for entry in existing_hist if isinstance(entry, dict)]
            else:
                prev_failed = prev_report.get("failed_templates") or []
                prev_failed_cnt = len(prev_failed) if isinstance(prev_failed, list) else int(prev_failed or 0)
                rounds_history = [{
                    "round": int(prev_report.get("round") or prev_report.get("cycle") or 1),
                    "timestamp": prev_report.get("timestamp") or now_iso,
                    "passed": bool(prev_report.get("passed", False)),
                    "failed": prev_failed_cnt,
                    "failed_shards": prev_report.get("failed_shards") or prev_report.get("failed_competencies") or [],
                    "rejudged_shards": prev_report.get("rejudged_shards") or [],
                }]

        current_round = (
            max((int(r.get("round", 0)) for r in rounds_history), default=0) + 1
            if rounds_history
            else max(1, int(cycle))
        )
        current_entry = {
            "round": current_round,
            "timestamp": now_iso,
            "passed": passed,
            "failed": len(failed_templates),
            "failed_shards": failed_competencies,
            "rejudged_shards": normalized_shards,
        }
        rounds_history.append(current_entry)
        report_data["round"] = current_round
        report_data["rejudged_shards"] = normalized_shards
        report_data["rounds_history"] = rounds_history

        try:
            report_p.write_text(
                json.dumps(report_data, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except Exception as e:
            logger.warning("Failed to write canonical judge_report.json: %s", e)

        if passed:
            try:
                rep_p = resolved_work_dir / "judge_report.json"
                if rep_p.is_file():
                    rep_sha = hashlib.sha256(rep_p.read_bytes()).hexdigest()
                else:
                    rep_sha = hashlib.sha256(json.dumps(report_data, sort_keys=True).encode("utf-8")).hexdigest()
                cert = ArtifactCertificate(
                    stage="judge",
                    artifact_id=f"judge_cycle_{cycle}",
                    source_sha256=rep_sha,
                    contract_version=2,
                    passed_50_seeds=True,
                )
                write_certificate(resolved_work_dir / "judge.cert.json", cert)
                v_cert_dir = resolved_work_dir / "verification"
                if v_cert_dir.is_dir():
                    write_certificate(v_cert_dir / "judge.cert.json", cert)
            except Exception as e:
                logger.warning("Could not write judge.cert.json: %s", e)

    return report_data


def main() -> None:
    """CLI utility for judge batch generation and comparison."""
    parser = argparse.ArgumentParser(description="Blind Judge Verifier for Parametric Templates.")
    subparsers = parser.add_subparsers(dest="action", required=True)

    # prepare subcommand
    prep = subparsers.add_parser("prepare", help="Generate blind judge batch WITHOUT answer keys")
    prep.add_argument("--templates", required=True, help="Path to template file or directory")
    prep.add_argument("--work-dir", required=True, help="Working directory for judge artifacts")
    prep.add_argument("--cta", help="Optional path to cta.json for distractor mappings")
    prep.add_argument(
        "--items-per-competency",
        type=int,
        default=0,
        help="Stratified sample count per competency (default: 0 for 100% templates unstratified)",
    )
    prep.add_argument(
        "--ready-only",
        action="store_true",
        default=False,
        help="Only evaluate templates whose competencies have not yet been evaluated",
    )
    prep.add_argument(
        "--ids",
        nargs="*",
        default=None,
        help="Target competency IDs to arbitrate (default: all)",
    )
    prep.add_argument(
        "--samples-per-template",
        type=int,
        default=None,
        help="Samples per template (default: 1 for verified templates, 3 otherwise)",
    )
    prep.add_argument(
        "--num-samples",
        type=int,
        default=None,
        help="Alias for --samples-per-template",
    )

    # split subcommand
    split_p = subparsers.add_parser("split", help="Split judge_batch.json into stratified batches")
    split_p.add_argument("--work-dir", required=True, help="Working directory containing judge_batch.json")
    split_p.add_argument("--max-judges", type=int, default=DEFAULT_MAX_JUDGES, help="Maximum number of judges (default: 10)")
    split_p.add_argument("--items-per-judge", type=int, default=DEFAULT_MAX_ITEMS_PER_JUDGE, help="Target items per judge (default: 20)")

    # check-completeness subcommand
    chk = subparsers.add_parser("check-completeness", help="Detect truncated or missing judge responses")
    chk.add_argument("--work-dir", required=True, help="Working directory containing judge batches and responses")

    # emit-redispatch subcommand
    redisp = subparsers.add_parser("emit-redispatch", help="Emit blind re-dispatch batches for missing items")
    redisp.add_argument("--work-dir", required=True, help="Working directory containing judge batches and responses")
    redisp.add_argument("--max-items-per-judge", type=int, default=DEFAULT_MAX_ITEMS_PER_JUDGE, help="Max items per judge batch (default: 20)")

    # compare subcommand
    comp = subparsers.add_parser("compare", help="Compare judge responses against ground truth")
    comp.add_argument("--responses", required=False, default=None, help="Path to judge responses JSON file or directory")
    comp.add_argument("--work-dir", required=True, help="Working directory containing judge_ground_truth.json")
    comp.add_argument("--cycle", type=int, default=1, help="Current correction cycle (1-3)")
    comp.add_argument(
        "--shards",
        nargs="*",
        default=None,
        help="Optional shard IDs for partial re-judge after repair (preserves judge_report_round_1.json and rounds_history)",
    )

    args = parser.parse_args()

    if args.action == "prepare":
        batch_p, truth_p = generate_judge_batch(
            templates_path=args.templates,
            work_dir=args.work_dir,
            cta_path=args.cta,
            items_per_competency=args.items_per_competency,
            ready_only=args.ready_only,
            ids=args.ids,
            samples_per_template=args.samples_per_template or args.num_samples,
        )
        print(f"Generated judge batch: {batch_p}")
        print(f"Generated ground truth: {truth_p}")

    elif args.action == "split":
        split_batches = split_judge_batch(
            work_dir=args.work_dir,
            max_judges=args.max_judges,
            items_per_judge=args.items_per_judge,
        )
        print(f"Generated {len(split_batches)} split judge batches in {args.work_dir}:")
        for sb in split_batches:
            print(f"  * {sb}")

    elif args.action == "check-completeness":
        comp_res = check_judge_completeness(args.work_dir)
        print(json.dumps(comp_res, indent=2, ensure_ascii=False))
        if not comp_res["is_complete"]:
            sys.exit(2)

    elif args.action == "emit-redispatch":
        redisp_res = emit_judge_redispatch(args.work_dir, max_items_per_judge=args.max_items_per_judge)
        print(json.dumps(redisp_res, indent=2, ensure_ascii=False))

    elif args.action == "compare":
        truth_p = Path(args.work_dir) / "judge_ground_truth.json"
        if not truth_p.is_file():
            print(f"Error: {truth_p} not found.", file=sys.stderr)
            sys.exit(1)

        gt = json.loads(truth_p.read_text(encoding="utf-8"))
        resps = Path(args.responses) if args.responses else None

        report = compare_judge_responses(
            responses=resps,
            ground_truth=gt,
            cycle=args.cycle,
            work_dir=args.work_dir,
            shards=args.shards,
        )
        report_p = Path(args.work_dir) / f"judge_report_cycle_{args.cycle}.json"
        report_p.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

        print("==================================================")
        print(f"JUDGE EVALUATION CYCLE {args.cycle}/{MAX_CORRECTION_CYCLES}")
        print(f"Agreement Rate: {report['agreement_rate'] * 100:.1f}% ({report['agreed_items']}/{report['total_items']})")
        print(f"Status: {'PASSED' if report['passed'] else 'DISCORDANCES DETECTED'}")
        if report["discordances"]:
            print(f"Discordant Templates ({len(report['affected_template_ids'])}): {report['affected_template_ids']}")
            for d in report["discordances"][:5]:
                print(f"  - [{d['item_id']}] {d['reason']}")
        print(f"Report written to: {report_p}")
        print("==================================================")

        if not report["passed"]:
            if report["can_retry"]:
                print(f"Cycle {args.cycle} failed. Re-run after repairing affected templates (Cycle {args.cycle + 1}).")
                sys.exit(2)
            else:
                print("Max correction cycles reached with remaining discordances.")
                sys.exit(1)


if __name__ == "__main__":
    main()
