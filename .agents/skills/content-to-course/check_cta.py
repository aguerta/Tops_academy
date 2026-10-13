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
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import jsonschema

# Add skills root to sys.path
_skills_root = Path(__file__).parent.resolve()
if str(_skills_root) not in sys.path:
    sys.path.insert(0, str(_skills_root))

from engine.invariants import validate_katex_syntax

RAW_LATEX_PATTERNS = [
    # 1. Backslashed LaTeX macros (unambiguous LaTeX)
    r"\\(?:dot|ddot|bar|hat|tilde|vec|frac|dfrac|tfrac|cfrac|sqrt|alpha|beta|gamma|delta|epsilon|varepsilon|zeta|eta|theta|iota|kappa|lambda|mu|nu|xi|pi|rho|sigma|tau|upsilon|phi|chi|psi|omega|Gamma|Delta|Theta|Lambda|Xi|Pi|Sigma|Phi|Psi|Omega|partial|int|sum|prod|infty|times|cdot|approx|leq|geq|neq)\b",
    # 2. LaTeX commands without backslash: MUST have immediate '{' (no whitespace) with concise math argument
    r"(?<!\\)\b(?:dot|ddot|bar|hat|tilde|vec)\{[a-zA-Z0-9_+\-*^./]{1,4}\}",
    r"(?<!\\)\b(?:frac|dfrac|tfrac|cfrac|sqrt)\{[a-zA-Z0-9_+\-*^./]+\}",
    # 3. Subscripts/superscripts without math delimiters: e.g. k_{t+1} or x^{2}
    r"(?<!\\)[_^]\{[a-zA-Z0-9_+\-*./]+\}",
]


class JsonLineLocator:
    """Builds an index from JSON file text to line numbers (1-indexed) for IDs and fields."""

    def __init__(self, file_path_or_text: Optional[Union[str, Path]] = None):
        self.id_to_line: Dict[str, int] = {}
        self.id_to_lines: Dict[str, List[int]] = {}
        self.item_field_to_line: Dict[Tuple[str, str], int] = {}
        if not file_path_or_text:
            return

        text = ""
        if isinstance(file_path_or_text, Path):
            if file_path_or_text.is_file():
                try:
                    text = file_path_or_text.read_text(encoding="utf-8")
                except Exception:
                    pass
        elif isinstance(file_path_or_text, str):
            if "\n" not in file_path_or_text and Path(file_path_or_text).is_file():
                try:
                    text = Path(file_path_or_text).read_text(encoding="utf-8")
                except Exception:
                    pass
            else:
                text = file_path_or_text

        self._build_index(text)

    def _build_index(self, text: str) -> None:
        if not text:
            return

        token_pattern = re.compile(r'("(?:\\.|[^"\\])*")|([{}])')
        stack: List[Dict[str, Any]] = []
        line_no = 1
        last_idx = 0

        for m in token_pattern.finditer(text):
            start = m.start()
            line_no += text.count("\n", last_idx, start)
            last_idx = start

            string_val, brace = m.groups()
            if brace == "{":
                stack.append({"fields": {}, "id": None, "id_line": None})
            elif brace == "}":
                if stack:
                    top = stack.pop()
                    item_id = top.get("id")
                    if item_id:
                        id_line = top.get("id_line") or line_no
                        if item_id not in self.id_to_line:
                            self.id_to_line[item_id] = id_line
                        self.id_to_lines.setdefault(item_id, []).append(id_line)
                        for fname, fline in top.get("fields", {}).items():
                            if (item_id, fname) not in self.item_field_to_line:
                                self.item_field_to_line[(item_id, fname)] = fline
            elif string_val and stack:
                after = text[m.end():m.end() + 20]
                col_match = re.match(r"^\s*:\s*", after)
                if col_match:
                    key = string_val[1:-1]
                    val_start = m.end() + col_match.end()
                    if key == "id":
                        val_match = re.match(r'^"((?:\\.|[^"\\])*)"', text[val_start:val_start + 200])
                        if val_match:
                            stack[-1]["id"] = val_match.group(1)
                            stack[-1]["id_line"] = line_no
                    else:
                        stack[-1]["fields"][key] = line_no

    def get_line(self, item_id: str, field_name: Optional[str] = None) -> Optional[int]:
        if field_name and (item_id, field_name) in self.item_field_to_line:
            return self.item_field_to_line[(item_id, field_name)]
        lines = self.id_to_lines.get(item_id)
        if lines:
            return lines[0]
        return self.id_to_line.get(item_id)

    def get_lines(self, item_id: str, field_name: Optional[str] = None) -> List[int]:
        if field_name and (item_id, field_name) in self.item_field_to_line:
            return [self.item_field_to_line[(item_id, field_name)]]
        lines = self.id_to_lines.get(item_id)
        if lines:
            return lines
        val = self.id_to_line.get(item_id)
        return [val] if val is not None else []


def build_json_line_index(file_path: Union[str, Path]) -> Dict[str, int]:
    """Builds an index mapping element IDs to line numbers (1-indexed)."""
    return JsonLineLocator(file_path).id_to_line


def load_schema(schema_name: str = "cta.schema.json") -> Dict[str, Any]:
    """Load JSON Schema from schemas directory."""
    schema_path = Path(__file__).parent / "schemas" / schema_name
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_cta_schema(
    cta_data: Dict[str, Any],
    locator: Optional[JsonLineLocator] = None,
) -> List[str]:
    """Validate cta_data against cta.schema.json."""
    schema = load_schema("cta.schema.json")
    validator = jsonschema.Draft7Validator(schema)
    errors = []
    schema_errs_by_type: Dict[Tuple[str, str], List[str]] = {}
    for err in validator.iter_errors(cta_data):
        loc = " -> ".join(str(p) for p in err.path)
        comp_id = None
        if err.path and len(err.path) >= 2 and err.path[0] == "competencies":
            c_idx = err.path[1]
            if isinstance(c_idx, int) and isinstance(cta_data.get("competencies"), list) and c_idx < len(cta_data["competencies"]):
                comp_id = cta_data["competencies"][c_idx].get("id")
        schema_errs_by_type.setdefault((loc, err.message), []).append(comp_id or f"index_{err.path[1] if len(err.path) > 1 else '?'}")

    for (loc, msg), items in schema_errs_by_type.items():
        if len(items) > 1:
            loc_items = []
            for item in items:
                line_info = f" (línea {locator.get_line(item)})" if locator and locator.get_line(item) else ""
                loc_items.append(f"{item}{line_info}")
            errors.append(f"Schema violation at [{loc}]: {msg} en {len(items)} competencias: {', '.join(loc_items)}.")
        else:
            item = items[0]
            line_info = f" (línea {locator.get_line(item)})" if locator and locator.get_line(item) else ""
            errors.append(f"Schema violation at [{loc}]{line_info}: {msg}")
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
    for field in ["manifestation", "remediation_hint", "wrong_belief", "omitted_step"]:
        val = d.get(field)
        if isinstance(val, str) and val.strip():
            # Check for raw LaTeX outside $...$ or $$...$$
            text_outside_math = re.sub(r"\$\$.*?\$\$|\$.*?\$", "", val, flags=re.DOTALL)
            has_raw_latex = any(re.search(p, text_outside_math) for p in RAW_LATEX_PATTERNS)
            if has_raw_latex:
                errors.append(f"Distractor '{did}' en '{field}' contiene comandos LaTeX sin delimitar por '$...$': {val}")

            clean_dollars = val.replace(r"\$", "")
            if "$" in clean_dollars:
                errors.extend(validate_katex_syntax(val, f"distractor '{did}' {field}"))
    return errors


def check_cta_katex(
    cta_data: Dict[str, Any],
    locator: Optional[JsonLineLocator] = None,
) -> List[str]:
    """Inspect KaTeX math in competencies and distractors using validate_katex_syntax.

    Inspects:
    - competencies[].name
    - competencies[].description_latex and competencies[].description
    - distractors[].manifestation, remediation_hint, wrong_belief, omitted_step
    unconditionally auditing for raw LaTeX outside '$...$' and validating KaTeX syntax.
    """
    errors: List[str] = []
    if isinstance(cta_data, list):
        competencies = cta_data
    elif isinstance(cta_data, dict):
        competencies = cta_data.get("competencies", [])
    else:
        return errors

    raw_latex_items: Dict[str, List[Tuple[str, str]]] = {}
    katex_syntax_items: Dict[str, List[Tuple[str, str]]] = {}

    for idx, comp in enumerate(competencies):
        if not isinstance(comp, dict):
            continue
        cid = comp.get("id", f"comp_at_index_{idx}")

        # competencies[].name
        c_name = comp.get("name")
        if isinstance(c_name, str) and c_name.strip():
            text_outside_math = re.sub(r"\$\$.*?\$\$|\$.*?\$", "", c_name, flags=re.DOTALL)
            if any(re.search(p, text_outside_math) for p in RAW_LATEX_PATTERNS):
                raw_latex_items.setdefault("name", []).append((cid, c_name))
            if "$" in c_name.replace(r"\$", ""):
                for kv in validate_katex_syntax(c_name, f"competency '{cid}' name"):
                    katex_syntax_items.setdefault(kv, []).append((cid, "name"))

        # competencies[].description_latex and competencies[].description
        for desc_key in ("description_latex", "description"):
            c_desc = comp.get(desc_key)
            if isinstance(c_desc, str) and c_desc.strip():
                text_outside_math = re.sub(r"\$\$.*?\$\$|\$.*?\$", "", c_desc, flags=re.DOTALL)
                if any(re.search(p, text_outside_math) for p in RAW_LATEX_PATTERNS):
                    raw_latex_items.setdefault(desc_key, []).append((cid, c_desc))
                if "$" in c_desc.replace(r"\$", ""):
                    for kv in validate_katex_syntax(c_desc, f"competency '{cid}' {desc_key}"):
                        katex_syntax_items.setdefault(kv, []).append((cid, desc_key))

        # distractors[] math validation
        for d in comp.get("distractors", []):
            if not isinstance(d, dict):
                continue
            did = d.get("id", "UNKNOWN")
            for field in ["manifestation", "remediation_hint", "wrong_belief", "omitted_step"]:
                val = d.get(field)
                if isinstance(val, str) and val.strip():
                    text_outside_math = re.sub(r"\$\$.*?\$\$|\$.*?\$", "", val, flags=re.DOTALL)
                    if any(re.search(p, text_outside_math) for p in RAW_LATEX_PATTERNS):
                        raw_latex_items.setdefault(field, []).append((did, val))
                    clean_dollars = val.replace(r"\$", "")
                    if "$" in clean_dollars:
                        for kv in validate_katex_syntax(val, f"distractor '{did}' {field}"):
                            katex_syntax_items.setdefault(kv, []).append((did, field))

    # Format aggregated raw LaTeX errors
    for field, items in raw_latex_items.items():
        if len(items) > 1:
            loc_strs = []
            for tid, val in items:
                ln = locator.get_line(tid, field) if locator else (locator.get_line(tid) if locator else None)
                l_info = f" (línea {ln})" if ln else ""
                loc_strs.append(f"'{tid}'{l_info}")
            errors.append(
                f"LaTeX sin delimitar por '$...$' detectado en campo '{field}' de {len(items)} distractores/competencias: {', '.join(loc_strs)}."
            )
        else:
            tid, val = items[0]
            ln = locator.get_line(tid, field) if locator else (locator.get_line(tid) if locator else None)
            l_info = f" (línea {ln})" if ln else ""
            if field in ("name", "description_latex", "description") or not (tid.startswith("D-") or tid.startswith("distractor")):
                errors.append(f"Competency '{tid}' {field} contiene comandos LaTeX sin delimitar por '$...$': {val}")
            else:
                errors.append(f"Distractor '{tid}'{l_info} en '{field}' contiene comandos LaTeX sin delimitar por '$...$': {val}")

    # Format aggregated KaTeX syntax errors
    for kv, items in katex_syntax_items.items():
        if len(items) > 1:
            loc_strs = []
            for tid, f in items:
                ln = locator.get_line(tid, f) if locator else (locator.get_line(tid) if locator else None)
                l_info = f" (línea {ln})" if ln else ""
                loc_strs.append(f"{tid}.{f}{l_info}")
            errors.append(f"Error de sintaxis KaTeX en {len(items)} campos: {', '.join(loc_strs)}: {kv}")
        else:
            tid, f = items[0]
            ln = locator.get_line(tid, f) if locator else (locator.get_line(tid) if locator else None)
            l_info = f" (línea {ln})" if ln else ""
            errors.append(f"{kv}{l_info}")

    return errors


def _validate_competencies_rules(
    competencies: List[Dict[str, Any]],
    manifest_data: Optional[Dict[str, Any]] = None,
    comp_validator: Optional[jsonschema.Draft7Validator] = None,
    is_part: bool = False,
    locator: Optional[JsonLineLocator] = None,
) -> List[str]:
    errors: List[str] = []
    manifest_pages_set = _build_manifest_pages_set(manifest_data)
    seen_distractor_ids: Set[str] = set()

    comp_schema_errs: Dict[Tuple[str, str], List[str]] = {}
    d1_under_3: List[Tuple[str, int]] = []
    d1_skill_under_6: List[Tuple[str, int]] = []
    d1_skill_under_2_omitted: List[Tuple[str, int]] = []

    d2_missing_id: List[str] = []
    d2_duplicates: List[str] = []
    d2_empty_wb_os: List[str] = []
    missing_evidence: List[Tuple[str, str, Any, str]] = []

    for idx, comp in enumerate(competencies):
        if not isinstance(comp, dict):
            continue
        cid = comp.get("id", f"comp_at_index_{idx}")

        if comp_validator:
            for err in comp_validator.iter_errors(comp):
                loc = " -> ".join(str(p) for p in err.path)
                comp_schema_errs.setdefault((loc, err.message), []).append(cid)

        ctype = comp.get("type", "").lower()
        distractors = comp.get("distractors", [])

        # Rule CTA-D1: >=3 distractors per comp, >=6 per Skill with >=2 omitted_step
        if len(distractors) < 3:
            d1_under_3.append((cid, len(distractors)))

        if ctype == "skill":
            if len(distractors) < 6:
                d1_skill_under_6.append((cid, len(distractors)))

            omitted_count = sum(1 for d in distractors if isinstance(d, dict) and d.get("omitted_step"))
            if omitted_count < 2:
                d1_skill_under_2_omitted.append((cid, omitted_count))

        # Rule CTA-D2: unique IDs within part / global, non-null wrong_belief or omitted_step
        for d in distractors:
            if not isinstance(d, dict):
                continue
            did = d.get("id", "")
            if not did:
                d2_missing_id.append(cid)
                continue

            if did in seen_distractor_ids:
                d2_duplicates.append(did)
            seen_distractor_ids.add(did)

            wb = d.get("wrong_belief")
            os_step = d.get("omitted_step")
            if not wb and not os_step:
                d2_empty_wb_os.append(did)

            # Check distractor evidence
            ev = d.get("evidence")
            if manifest_pages_set and ev:
                ev_err = _check_evidence_in_manifest(ev, manifest_pages_set, f"Distractor '{did}'")
                if ev_err:
                    missing_evidence.append((f"Distractor '{did}'", str(ev.get("doc") or ev.get("pdf") or ""), ev.get("page"), did))

        # Check competency evidence
        if manifest_pages_set and comp.get("evidence"):
            for ev in comp.get("evidence", []):
                ev_err = _check_evidence_in_manifest(ev, manifest_pages_set, f"Competency '{cid}'")
                if ev_err:
                    missing_evidence.append((f"Competency '{cid}'", str(ev.get("doc") or ev.get("pdf") or ""), ev.get("page"), cid))

    # Format schema errors
    for (loc, msg), cids in comp_schema_errs.items():
        if len(cids) > 1:
            loc_items = [f"{c}" + (f" (línea {locator.get_line(c)})" if locator and locator.get_line(c) else "") for c in cids]
            errors.append(f"Competency schema violation at [{loc}]: {msg} en {len(cids)} competencias: {', '.join(loc_items)}.")
        else:
            c = cids[0]
            line_info = f" (línea {locator.get_line(c)})" if locator and locator.get_line(c) else ""
            errors.append(f"Competency '{c}' schema violation at [{loc}]{line_info}: {msg}")

    # Format CTA-D1 errors
    if len(d1_under_3) > 1:
        loc_items = [f"{c}" + (f" (línea {locator.get_line(c)})" if locator and locator.get_line(c) else "") + f" [{cnt} distractores]" for c, cnt in d1_under_3]
        errors.append(f"CTA-D1 violation: Competencias con cuota insuficiente (<3 distractores): {', '.join(loc_items)} (mínimo 3 requerido).")
    elif len(d1_under_3) == 1:
        c, cnt = d1_under_3[0]
        line_info = f" (línea {locator.get_line(c)})" if locator and locator.get_line(c) else ""
        errors.append(f"CTA-D1 violation: Competency '{c}'{line_info} has {cnt} distractors (minimum 3 required).")

    if len(d1_skill_under_6) > 1:
        loc_items = [f"{c}" + (f" (línea {locator.get_line(c)})" if locator and locator.get_line(c) else "") + f" [{cnt} distractores]" for c, cnt in d1_skill_under_6]
        errors.append(f"CTA-D1 violation: Competencias tipo Skill con cuota insuficiente (<6 distractores): {', '.join(loc_items)} (mínimo 6 requerido).")
    elif len(d1_skill_under_6) == 1:
        c, cnt = d1_skill_under_6[0]
        line_info = f" (línea {locator.get_line(c)})" if locator and locator.get_line(c) else ""
        errors.append(f"CTA-D1 violation: Skill '{c}'{line_info} has {cnt} distractors (minimum 6 required).")

    if len(d1_skill_under_2_omitted) > 1:
        loc_items = [f"{c}" + (f" (línea {locator.get_line(c)})" if locator and locator.get_line(c) else "") + f" [{cnt} con omitted_step]" for c, cnt in d1_skill_under_2_omitted]
        errors.append(f"CTA-D1 violation: Competencias tipo Skill con distractores insuficientes con omitted_step (<2): {', '.join(loc_items)} (mínimo 2 requerido).")
    elif len(d1_skill_under_2_omitted) == 1:
        c, cnt = d1_skill_under_2_omitted[0]
        line_info = f" (línea {locator.get_line(c)})" if locator and locator.get_line(c) else ""
        errors.append(f"CTA-D1 violation: Skill '{c}'{line_info} has {cnt} distractors with omitted_step (minimum 2 required).")

    # Format CTA-D2 errors
    if len(d2_missing_id) > 1:
        loc_items = [f"'{c}'" + (f" (línea {locator.get_line(c)})" if locator and locator.get_line(c) else "") for c in d2_missing_id]
        errors.append(f"CTA-D2 violation: Distractor missing 'id' en {len(d2_missing_id)} distractores en competencias: {', '.join(loc_items)}.")
    elif len(d2_missing_id) == 1:
        c = d2_missing_id[0]
        line_info = f" (línea {locator.get_line(c)})" if locator and locator.get_line(c) else ""
        errors.append(f"CTA-D2 violation in '{c}'{line_info}: distractor missing id.")

    if len(d2_duplicates) > 1:
        unique_dups = sorted(set(d2_duplicates))
        loc_items = []
        for did in unique_dups:
            lines = locator.get_lines(did) if locator else []
            lines_str = f" (líneas {', '.join(str(l) for l in sorted(set(lines)))})" if len(lines) > 1 else (f" (línea {lines[0]})" if lines else "")
            loc_items.append(f"'{did}'{lines_str}")
        scope_str = "within competency part" if is_part else "across competencies"
        errors.append(f"CTA-D2 violation: Duplicate distractor ids found {scope_str}: {', '.join(loc_items)} ({len(d2_duplicates)} ocurrencias).")
    elif len(d2_duplicates) == 1:
        did = d2_duplicates[0]
        lines = locator.get_lines(did) if locator else []
        lines_str = f" (líneas {', '.join(str(l) for l in sorted(set(lines)))})" if len(lines) > 1 else (f" (línea {lines[0]})" if lines else "")
        scope_str = "within competency part" if is_part else "across competencies"
        errors.append(f"CTA-D2 violation: Duplicate distractor id '{did}'{lines_str} found {scope_str}.")

    if len(d2_empty_wb_os) > 1:
        loc_items = [f"'{did}'" + (f" (línea {locator.get_line(did)})" if locator and locator.get_line(did) else "") for did in d2_empty_wb_os]
        errors.append(f"CTA-D2 violation: Ambos wrong_belief y omitted_step están vacíos o nulos en distractores: {', '.join(loc_items)} ({len(d2_empty_wb_os)} distractores afectados).")
    elif len(d2_empty_wb_os) == 1:
        did = d2_empty_wb_os[0]
        line_info = f" (línea {locator.get_line(did)})" if locator and locator.get_line(did) else ""
        errors.append(f"CTA-D2 violation in distractor '{did}'{line_info}: both wrong_belief and omitted_step are null/empty.")

    # Format Evidence errors
    if len(missing_evidence) > 1:
        loc_items = [f"{lbl}" + (f" (línea {locator.get_line(iid)})" if locator and locator.get_line(iid) else "") + f" ({doc}, pág {pg})" for lbl, doc, pg, iid in missing_evidence]
        errors.append(f"Evidencia citada no encontrada en manifest (not found in manifest) para {len(missing_evidence)} elementos: {', '.join(loc_items)}.")
    elif len(missing_evidence) == 1:
        lbl, doc, pg, iid = missing_evidence[0]
        line_info = f" (línea {locator.get_line(iid)})" if locator and locator.get_line(iid) else ""
        errors.append(f"{lbl}{line_info} cites evidence ({doc}, page {pg}) not found in manifest.")

    return errors


def check_cta_part(
    data: Any,
    manifest_data: Optional[Dict[str, Any]] = None,
    file_path: Optional[Union[str, Path]] = None,
    locator: Optional[JsonLineLocator] = None,
) -> Tuple[bool, List[str]]:
    """Validate sectional CTA part (cta_part_XX.json).

    Enforces local competency schema, CTA-D1 & CTA-D2 quotas, and evidence validity
    without requiring globally unique IDs or complete cross-section prerequisite closures.
    """
    errors: List[str] = []
    if locator is None:
        locator = JsonLineLocator(file_path)

    if isinstance(data, list):
        competencies = data
    elif isinstance(data, dict):
        competencies = data.get("competencies", [])
    else:
        return False, ["cta_part data must be a JSON object with 'competencies' or a JSON array."]

    if not competencies:
        return False, ["cta_part contains zero competencies."]

    base_schema = load_schema("cta.schema.json")
    comp_subschema = base_schema.get("definitions", {}).get("competency", {})
    comp_schema = {
        "$schema": base_schema.get("$schema", "http://json-schema.org/draft-07/schema#"),
        "definitions": base_schema.get("definitions", {}),
        **comp_subschema,
    }
    comp_validator = jsonschema.Draft7Validator(comp_schema)

    part_errors = _validate_competencies_rules(
        competencies=competencies,
        manifest_data=manifest_data,
        comp_validator=comp_validator,
        is_part=True,
        locator=locator,
    )
    errors.extend(part_errors)

    katex_errors = check_cta_katex(data if isinstance(data, dict) else {"competencies": data}, locator=locator)
    errors.extend(katex_errors)

    return len(errors) == 0, errors


def validate_cta_rules(
    cta_data: Dict[str, Any],
    manifest_data: Optional[Dict[str, Any]] = None,
    file_path: Optional[Union[str, Path]] = None,
    locator: Optional[JsonLineLocator] = None,
) -> Tuple[bool, List[str]]:
    """Validate all cognitive and psychometric rules on cta.json."""
    errors = []
    if locator is None:
        locator = JsonLineLocator(file_path)

    # 1. JSON Schema validation
    schema_errs = validate_cta_schema(cta_data, locator=locator)
    errors.extend(schema_errs)

    competencies = cta_data.get("competencies", [])
    if not competencies:
        errors.append("cta.json contains zero competencies.")
        return False, errors

    comp_errors = _validate_competencies_rules(
        competencies=competencies,
        manifest_data=manifest_data,
        comp_validator=None,
        is_part=False,
        locator=locator,
    )
    errors.extend(comp_errors)

    # 3. Prerequisites DAG check
    dag_errors = check_prerequisites_dag(competencies)
    errors.extend(dag_errors)

    # 4. KaTeX syntax validation
    katex_errors = check_cta_katex(cta_data, locator=locator)
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
        valid, errors = check_cta_part(cta_data, manifest_data, file_path=cta_file)
        if not valid:
            print(f"FAIL: {len(errors)} validation errors in cta_part:")
            for e in errors:
                print(f"  - {e}")
            sys.exit(1)
        print("PASS: cta_part satisfies local schema, CTA-D1, CTA-D2, and evidence constraints.")
        sys.exit(0)

    valid, errors = validate_cta_rules(cta_data, manifest_data, file_path=cta_file)
    if not valid:
        print(f"FAIL: {len(errors)} validation errors in cta.json:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print("PASS: cta.json satisfies all schema, CTA-D1, CTA-D2, and evidence constraints.")
    sys.exit(0)


if __name__ == "__main__":
    main()
