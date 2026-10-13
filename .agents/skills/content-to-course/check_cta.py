"""CTA validator for content-to-course v2.

Validates cta.json against cta.schema.json and enforces:
- CTA-D1: >=3 distractors per comp, >=6 per Skill with >=2 having omitted_step non-null
- CTA-D2: Unique distractor IDs, prefixed with competency ID; wrong_belief or omitted_step non-null
- Evidence verification: all cited documents and pages exist in manifest.json
- DAG acyclicity: prerequisites form a directed acyclic graph without cycles
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import jsonschema

# Add skills root to sys.path
_skills_root = Path(__file__).parent.resolve()
if str(_skills_root) not in sys.path:
    sys.path.insert(0, str(_skills_root))

from engine.invariants import validate_katex_syntax


def load_schema(schema_name: str = "cta.schema.json") -> Dict[str, Any]:
    """Load JSON Schema from schemas directory."""
    schema_path = Path(__file__).parent / "schemas" / schema_name
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_cta_schema(cta_data: Dict[str, Any]) -> List[str]:
    """Validate cta_data against cta.schema.json."""
    schema = load_schema("cta.schema.json")
    validator = jsonschema.Draft7Validator(schema)
    errors = []
    for err in validator.iter_errors(cta_data):
        loc = " -> ".join(str(p) for p in err.path)
        errors.append(f"Schema violation at [{loc}]: {err.message}")
    return errors


def check_prerequisites_dag(competencies: List[Dict[str, Any]]) -> List[str]:
    """Ensure prerequisite references exist and form an acyclic graph."""
    errors = []
    comp_ids = {c["id"] for c in competencies}

    adj: Dict[str, List[str]] = {cid: [] for cid in comp_ids}
    for comp in competencies:
        cid = comp["id"]
        for prereq in comp.get("prerequisites", []):
            if prereq not in comp_ids:
                errors.append(f"Competency '{cid}' references non-existent prerequisite '{prereq}'.")
            else:
                adj[cid].append(prereq)

    # Cycle detection using DFS
    visited: Dict[str, int] = {}  # 0: unvisited, 1: visiting, 2: visited

    def dfs(node: str, path: List[str]) -> bool:
        visited[node] = 1
        for neighbor in adj.get(node, []):
            if visited.get(neighbor) == 1:
                cycle_str = " -> ".join(path + [neighbor])
                errors.append(f"Cycle detected in prerequisites: {cycle_str}")
                return False
            if visited.get(neighbor, 0) == 0:
                if not dfs(neighbor, path + [neighbor]):
                    return False
        visited[node] = 2
        return True

    for cid in comp_ids:
        if visited.get(cid, 0) == 0:
            dfs(cid, [cid])

    return errors


def _build_manifest_pages_set(manifest_data: Optional[Dict[str, Any]]) -> Optional[Set[Tuple[str, Any]]]:
    """Index valid pages from manifest.json for rapid evidence matching."""
    if not manifest_data:
        return None
    manifest_pages_set: Set[Tuple[str, Any]] = set()
    for item in manifest_data.get("items", manifest_data.get("pages", [])):
        doc = str(item.get("doc", "")).lower()
        doc_stem = Path(doc).stem.lower()
        p_val = item.get("page", 0)
        try:
            page_int = int(p_val)
            manifest_pages_set.add((doc, page_int))
            manifest_pages_set.add((doc_stem, page_int))
        except (ValueError, TypeError):
            pass
        p_str = str(p_val).strip()
        manifest_pages_set.add((doc, p_str))
        manifest_pages_set.add((doc_stem, p_str))
    return manifest_pages_set


def _check_evidence_in_manifest(
    evidence: Optional[Dict[str, Any]],
    manifest_pages_set: Optional[Set[Tuple[str, Any]]],
    item_label: str,
) -> Optional[str]:
    """Verify an evidence citation exists in manifest pages set."""
    if not manifest_pages_set or not evidence:
        return None
    ev_doc = str(evidence.get("doc") or evidence.get("pdf") or "").lower()
    ev_page = evidence.get("page")
    if ev_doc and ev_page is not None:
        ev_doc_stem = Path(ev_doc).stem.lower()
        ev_str = str(ev_page).strip()
        ev_matches = (
            (ev_doc, ev_str) in manifest_pages_set
            or (ev_doc_stem, ev_str) in manifest_pages_set
        )
        try:
            ev_int = int(ev_page)
            if (ev_doc, ev_int) in manifest_pages_set or (ev_doc_stem, ev_int) in manifest_pages_set:
                ev_matches = True
        except (ValueError, TypeError):
            pass
        if not ev_matches:
            return f"{item_label} cites evidence ({ev_doc}, page {ev_page}) not found in manifest."
    return None


def validate_distractor_math(d: Dict[str, Any], did: str) -> List[str]:
    """Audit all distractor text fields unconditionally for raw/orphaned LaTeX and KaTeX errors."""
    errors: List[str] = []
    latex_patterns = [
        r"\b(?:dot|ddot|bar|hat|tilde|vec|frac|dfrac|tfrac|cfrac|sqrt)\s*\{",
        r"\\(?:dot|ddot|bar|hat|tilde|vec|frac|dfrac|tfrac|cfrac|sqrt|alpha|beta|gamma|delta|epsilon|varepsilon|zeta|eta|theta|iota|kappa|lambda|mu|nu|xi|pi|rho|sigma|tau|upsilon|phi|chi|psi|omega|Gamma|Delta|Theta|Lambda|Xi|Pi|Sigma|Phi|Psi|Omega)\b",
        r"(?<!\\)[_^]\{",
    ]
    for field in ["manifestation", "remediation_hint", "wrong_belief", "omitted_step"]:
        val = d.get(field)
        if isinstance(val, str) and val.strip():
            # Check for raw LaTeX outside $...$ or $$...$$
            text_outside_math = re.sub(r"\$\$.*?\$\$|\$.*?\$", "", val, flags=re.DOTALL)
            has_raw_latex = any(re.search(p, text_outside_math) for p in latex_patterns)
            if has_raw_latex:
                errors.append(f"Distractor '{did}' en '{field}' contiene comandos LaTeX sin delimitar por '$...$': {val}")

            clean_dollars = val.replace(r"\$", "")
            if "$" in clean_dollars:
                errors.extend(validate_katex_syntax(val, f"distractor '{did}' {field}"))
    return errors


def check_cta_katex(cta_data: Dict[str, Any]) -> List[str]:
    """Inspect KaTeX math in competencies and distractors using validate_katex_syntax.

    Inspects:
    - competencies[].name
    - competencies[].description_latex and competencies[].description
    - distractors[].manifestation, remediation_hint, wrong_belief, omitted_step
    unconditionally auditing for raw LaTeX outside '$...$' and validating KaTeX syntax.
    """
    errors: List[str] = []
    latex_patterns = [
        r"\b(?:dot|ddot|bar|hat|tilde|vec|frac|dfrac|tfrac|cfrac|sqrt)\s*\{",
        r"\\(?:dot|ddot|bar|hat|tilde|vec|frac|dfrac|tfrac|cfrac|sqrt|alpha|beta|gamma|delta|epsilon|varepsilon|zeta|eta|theta|iota|kappa|lambda|mu|nu|xi|pi|rho|sigma|tau|upsilon|phi|chi|psi|omega|Gamma|Delta|Theta|Lambda|Xi|Pi|Sigma|Phi|Psi|Omega)\b",
        r"(?<!\\)[_^]\{",
    ]
    if isinstance(cta_data, list):
        competencies = cta_data
    elif isinstance(cta_data, dict):
        competencies = cta_data.get("competencies", [])
    else:
        return errors

    for idx, comp in enumerate(competencies):
        if not isinstance(comp, dict):
            continue
        cid = comp.get("id", f"comp_at_index_{idx}")

        # competencies[].name
        c_name = comp.get("name")
        if isinstance(c_name, str) and c_name.strip():
            text_outside_math = re.sub(r"\$\$.*?\$\$|\$.*?\$", "", c_name, flags=re.DOTALL)
            if any(re.search(p, text_outside_math) for p in latex_patterns):
                errors.append(f"Competency '{cid}' name contiene comandos LaTeX sin delimitar por '$...$': {c_name}")
            if "$" in c_name.replace(r"\$", ""):
                errors.extend(validate_katex_syntax(c_name, f"competency '{cid}' name"))

        # competencies[].description_latex and competencies[].description
        for desc_key in ("description_latex", "description"):
            c_desc = comp.get(desc_key)
            if isinstance(c_desc, str) and c_desc.strip():
                text_outside_math = re.sub(r"\$\$.*?\$\$|\$.*?\$", "", c_desc, flags=re.DOTALL)
                if any(re.search(p, text_outside_math) for p in latex_patterns):
                    errors.append(f"Competency '{cid}' {desc_key} contiene comandos LaTeX sin delimitar por '$...$': {c_desc}")
                if "$" in c_desc.replace(r"\$", ""):
                    errors.extend(validate_katex_syntax(c_desc, f"competency '{cid}' {desc_key}"))

        # distractors[] math validation
        for d in comp.get("distractors", []):
            if not isinstance(d, dict):
                continue
            did = d.get("id", "UNKNOWN")
            errors.extend(validate_distractor_math(d, did))

    return errors


def check_cta_part(
    data: Any,
    manifest_data: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    """Validate sectional CTA part (cta_part_XX.json).

    Enforces local competency schema, CTA-D1 & CTA-D2 quotas, and evidence validity
    without requiring globally unique IDs or complete cross-section prerequisite closures.
    """
    errors: List[str] = []

    if isinstance(data, list):
        competencies = data
    elif isinstance(data, dict):
        competencies = data.get("competencies", [])
    else:
        return False, ["cta_part data must be a JSON object with 'competencies' or a JSON array."]

    if not competencies:
        return False, ["cta_part contains zero competencies."]

    # Load competency schema definition
    base_schema = load_schema("cta.schema.json")
    comp_subschema = base_schema.get("definitions", {}).get("competency", {})
    comp_schema = {
        "$schema": base_schema.get("$schema", "http://json-schema.org/draft-07/schema#"),
        "definitions": base_schema.get("definitions", {}),
        **comp_subschema,
    }
    comp_validator = jsonschema.Draft7Validator(comp_schema)

    manifest_pages_set = _build_manifest_pages_set(manifest_data)
    local_distractor_ids: Set[str] = set()

    for idx, comp in enumerate(competencies):
        cid = comp.get("id", f"comp_at_index_{idx}")

        # Validate schema of individual competency
        for err in comp_validator.iter_errors(comp):
            loc = " -> ".join(str(p) for p in err.path)
            errors.append(f"Competency '{cid}' schema violation at [{loc}]: {err.message}")

        ctype = comp.get("type", "").lower()
        distractors = comp.get("distractors", [])

        # Rule CTA-D1: >=3 distractors per comp, >=6 per Skill with >=2 omitted_step
        if len(distractors) < 3:
            errors.append(
                f"CTA-D1 violation: Competency '{cid}' has {len(distractors)} distractors (minimum 3 required)."
            )

        if ctype == "skill":
            if len(distractors) < 6:
                errors.append(
                    f"CTA-D1 violation: Skill '{cid}' has {len(distractors)} distractors (minimum 6 required)."
                )

            omitted_count = sum(1 for d in distractors if d.get("omitted_step"))
            if omitted_count < 2:
                errors.append(
                    f"CTA-D1 violation: Skill '{cid}' has {omitted_count} distractors with omitted_step (minimum 2 required)."
                )

        # Rule CTA-D2: unique IDs within part, non-null wrong_belief or omitted_step
        for d in distractors:
            did = d.get("id", "")
            if not did:
                errors.append(f"CTA-D2 violation in '{cid}': distractor missing id.")
                continue

            if did in local_distractor_ids:
                errors.append(
                    f"CTA-D2 violation: Duplicate distractor id '{did}' found within competency part."
                )
            local_distractor_ids.add(did)

            wb = d.get("wrong_belief")
            os_step = d.get("omitted_step")
            if not wb and not os_step:
                errors.append(
                    f"CTA-D2 violation in distractor '{did}': both wrong_belief and omitted_step are null/empty."
                )

            # Check distractor evidence
            ev_err = _check_evidence_in_manifest(
                d.get("evidence"), manifest_pages_set, f"Distractor '{did}'"
            )
            if ev_err:
                errors.append(ev_err)

        # Check competency evidence in manifest
        if comp.get("evidence"):
            for ev in comp.get("evidence", []):
                ev_err = _check_evidence_in_manifest(
                    ev, manifest_pages_set, f"Competency '{cid}'"
                )
                if ev_err:
                    errors.append(ev_err)

    # KaTeX syntax validation
    katex_errors = check_cta_katex(data if isinstance(data, dict) else {"competencies": data})
    errors.extend(katex_errors)

    return len(errors) == 0, errors


def validate_cta_rules(
    cta_data: Dict[str, Any],
    manifest_data: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    """Validate all cognitive and psychometric rules on cta.json."""
    errors = []

    # 1. JSON Schema validation
    schema_errs = validate_cta_schema(cta_data)
    errors.extend(schema_errs)

    competencies = cta_data.get("competencies", [])
    if not competencies:
        errors.append("cta.json contains zero competencies.")
        return False, errors

    # Check manifest pages index if provided
    manifest_pages_set = _build_manifest_pages_set(manifest_data)

    all_distractor_ids: Set[str] = set()

    for comp in competencies:
        cid = comp["id"]
        ctype = comp.get("type", "").lower()
        distractors = comp.get("distractors", [])

        # Rule CTA-D1: >=3 distractors per comp, >=6 per Skill with >=2 omitted_step
        if len(distractors) < 3:
            errors.append(f"CTA-D1 violation: Competency '{cid}' has {len(distractors)} distractors (minimum 3 required).")

        if ctype == "skill":
            if len(distractors) < 6:
                errors.append(f"CTA-D1 violation: Skill '{cid}' has {len(distractors)} distractors (minimum 6 required).")
            
            omitted_count = sum(1 for d in distractors if d.get("omitted_step"))
            if omitted_count < 2:
                errors.append(
                    f"CTA-D1 violation: Skill '{cid}' has {omitted_count} distractors with omitted_step (minimum 2 required)."
                )

        # Rule CTA-D2: unique IDs, non-null wrong_belief or omitted_step
        for d in distractors:
            did = d.get("id", "")
            if not did:
                errors.append(f"CTA-D2 violation in '{cid}': distractor missing id.")
                continue

            if did in all_distractor_ids:
                errors.append(f"CTA-D2 violation: Duplicate distractor id '{did}' found across competencies.")
            all_distractor_ids.add(did)

            # Check that wrong_belief or omitted_step is non-null
            wb = d.get("wrong_belief")
            os_step = d.get("omitted_step")
            if not wb and not os_step:
                errors.append(
                    f"CTA-D2 violation in distractor '{did}': both wrong_belief and omitted_step are null/empty."
                )

            # Check evidence in manifest if manifest provided
            ev_err = _check_evidence_in_manifest(
                d.get("evidence"), manifest_pages_set, f"Distractor '{did}'"
            )
            if ev_err:
                errors.append(ev_err)

        # Check competency evidence in manifest
        if comp.get("evidence"):
            for ev in comp.get("evidence", []):
                ev_err = _check_evidence_in_manifest(
                    ev, manifest_pages_set, f"Competency '{cid}'"
                )
                if ev_err:
                    errors.append(ev_err)

    # 3. Prerequisites DAG check
    dag_errors = check_prerequisites_dag(competencies)
    errors.extend(dag_errors)

    # 4. KaTeX syntax validation
    katex_errors = check_cta_katex(cta_data)
    errors.extend(katex_errors)

    return len(errors) == 0, errors


def main():
    parser = argparse.ArgumentParser(description="Validate cta.json taxonomy and distractors")
    parser.add_argument("cta_path", help="Path to cta.json or cta_part_XX.json")
    parser.add_argument("--manifest", help="Optional path to manifest.json for evidence verification")
    parser.add_argument(
        "--part",
        action="store_true",
        help="Validate sectional CTA part (cta_part_XX.json) without cross-section closing",
    )
    args = parser.parse_args()

    cta_file = Path(args.cta_path)
    if not cta_file.exists():
        print(f"Error: file not found at {cta_file}")
        sys.exit(1)

    with open(cta_file, "r", encoding="utf-8") as f:
        cta_data = json.load(f)

    manifest_data = None
    if args.manifest:
        m_file = Path(args.manifest)
        if m_file.exists():
            with open(m_file, "r", encoding="utf-8") as f:
                manifest_data = json.load(f)

    if args.part:
        valid, errors = check_cta_part(cta_data, manifest_data)
        if not valid:
            print(f"FAIL: {len(errors)} validation errors in cta_part:")
            for e in errors:
                print(f"  - {e}")
            sys.exit(1)
        print("PASS: cta_part satisfies local schema, CTA-D1, CTA-D2, and evidence constraints.")
        sys.exit(0)

    valid, errors = validate_cta_rules(cta_data, manifest_data)
    if not valid:
        print(f"FAIL: {len(errors)} validation errors in cta.json:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print("PASS: cta.json satisfies all schema, CTA-D1, CTA-D2, and evidence constraints.")
    sys.exit(0)


if __name__ == "__main__":
    main()
