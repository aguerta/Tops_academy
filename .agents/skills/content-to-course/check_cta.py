"""CTA validator for content-to-course v2.

Validates cta.json against cta.schema.json and enforces:
- CTA-D1: >=3 distractors per comp, >=6 per Skill with >=2 having omitted_step non-null
- CTA-D2: Unique distractor IDs, prefixed with competency ID; wrong_belief or omitted_step non-null
- Evidence verification: all cited documents and pages exist in manifest.json
- DAG acyclicity: prerequisites form a directed acyclic graph without cycles
"""

import argparse
import json
import math
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import jsonschema

# Add skills root to sys.path
_skills_root = Path(__file__).parent.resolve()
if str(_skills_root) not in sys.path:
    sys.path.insert(0, str(_skills_root))

from engine.invariants import validate_katex_syntax
try:
    from engine.stage_contract import (
        MIN_MODALITIES_PER_COMPETENCY as _MIN_MODALITIES_PER_COMPETENCY,
        MAX_MODALITIES_PER_COMPETENCY as _MAX_MODALITIES_PER_COMPETENCY,
        MIN_COMPS_FOR_CTA_BLOOM_GATE as _MIN_COMPS_FOR_CTA_BLOOM_GATE,
        compute_cta_bloom_portfolio_metrics,
    )
except ImportError:
    _MIN_MODALITIES_PER_COMPETENCY = 2
    _MAX_MODALITIES_PER_COMPETENCY = 4
    _MIN_COMPS_FOR_CTA_BLOOM_GATE = 5
    compute_cta_bloom_portfolio_metrics = None  # type: ignore[assignment]

try:
    import pykatex
except ImportError:
    pykatex = None


class ValidationResult(tuple):
    """Tuple subclass (valid, errors) with optional warnings property."""

    def __new__(cls, valid: bool, errors: List[str], warnings: Optional[List[str]] = None):
        return super().__new__(cls, (valid, errors))

    def __init__(self, valid: bool, errors: List[str], warnings: Optional[List[str]] = None):
        self.valid = valid
        self.errors = errors
        self.warnings = warnings or []


def _validate_pykatex_math_span(span: str, is_display: bool = False) -> Optional[str]:
    """Render math span using pykatex, safely sanitizing combining characters on ParseError."""
    if not pykatex or not span:
        return None
    strict_mode = getattr(pykatex, "STRICT_ERROR", "error")
    try:
        pykatex.renderToString(span, is_display, strict=strict_mode)
        return None
    except Exception as exc:
        # 1. Non-ASCII accented Latin characters inside \text{}, \textrm{}, \mathrm{} are supported by web KaTeX
        if re.search(r"[^\x00-\x7F]", span):
            ascii_span = "".join(
                ch for ch in unicodedata.normalize("NFD", span) if unicodedata.category(ch) != "Mn"
            )
            try:
                pykatex.renderToString(ascii_span, is_display, strict=strict_mode)
                return None
            except Exception:
                pass
        # 2. Bare braced identifiers {x}
        if re.search(r"(?<![a-zA-Z\\])\{[a-zA-Z0-9_]{1,6}\}", span):
            fallback_span = re.sub(r"(?<![a-zA-Z\\])\{([a-zA-Z0-9_]{1,6})\}", r"\1", span)
            try:
                pykatex.renderToString(fallback_span, is_display, strict=strict_mode)
                return None
            except Exception:
                pass
        clean_msg = str(exc).replace("\u0332", "^")
        return clean_msg

LATEX_CMD_NAMES = (
    r"frac|dfrac|tfrac|cfrac|sqrt|sum|prod|int|oint|lim|infty|partial|nabla|"
    r"alpha|beta|gamma|delta|epsilon|varepsilon|zeta|eta|theta|vartheta|iota|kappa|lambda|mu|nu|xi|pi|rho|sigma|tau|upsilon|phi|varphi|chi|psi|omega|"
    r"Gamma|Delta|Theta|Lambda|Xi|Pi|Sigma|Upsilon|Phi|Psi|Omega|"
    r"cdot|times|div|pm|mp|leq|geq|neq|approx|equiv|sim|simeq|propto|in|notin|subset|subseteq|cup|cap|forall|exists|"
    r"Rightarrow|implies|iff|Leftrightarrow|to|rightarrow|leftarrow|xrightarrow|"
    r"hat|bar|tilde|vec|dot|ddot|mathcal|mathbb|mathbf|boldsymbol|text|operatorname|left|right|begin|end|"
    r"quad|qquad|ln|log|exp|det|dim|ker|min|max|sup|inf"
)
LATEX_CMD_RE = re.compile(rf"\\(?:{LATEX_CMD_NAMES})(?![a-zA-Z])")

RAW_LATEX_PATTERNS = [
    # 1. Backslashed LaTeX macros (unambiguous LaTeX)
    rf"\\(?:{LATEX_CMD_NAMES})(?![a-zA-Z])",


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


def check_prerequisites_dag(
    competencies: List[Dict[str, Any]],
    allowed_prereq_ids: Optional[Union[Set[str], List[str], Tuple[str, ...]]] = None,
) -> List[str]:
    """Ensure prerequisite references exist, form an acyclic graph, and satisfy connectivity and root ratio."""
    errors = []
    comp_ids = {c["id"] for c in competencies}
    allowed_set = set(allowed_prereq_ids) if allowed_prereq_ids else set()
    valid_ids = comp_ids | allowed_set

    adj: Dict[str, List[str]] = {cid: [] for cid in comp_ids}
    for comp in competencies:
        cid = comp["id"]
        for prereq in comp.get("prerequisites", []):
            if prereq not in valid_ids:
                errors.append(f"Competency '{cid}' references non-existent prerequisite '{prereq}'.")
            elif prereq in comp_ids:
                adj[cid].append(prereq)

    # Cycle detection using DFS
    visited: Dict[str, int] = {}  # 0: unvisited, 1: visiting, 2: visited

    def dfs(node: str, path: List[str]) -> bool:
        visited[node] = 1
        for neighbor in sorted(adj.get(node, [])):
            if visited.get(neighbor) == 1:
                if neighbor in path:
                    idx = path.index(neighbor)
                    cycle_str = " -> ".join(path[idx:] + [neighbor])
                else:
                    cycle_str = " -> ".join(path + [neighbor])
                errors.append(f"Cycle detected in prerequisites: {cycle_str}")
                return False
            if visited.get(neighbor, 0) == 0:
                if not dfs(neighbor, path + [neighbor]):
                    return False
        visited[node] = 2
        return True

    for cid in sorted(comp_ids):
        if visited.get(cid, 0) == 0:
            dfs(cid, [cid])

    # Graph connectivity and root ratio checks
    n = len(competencies)
    if n >= 2:
        # Undirected graph for connected components
        undirected_adj: Dict[str, Set[str]] = {c["id"]: set() for c in competencies}
        base_anchor = "__BASE_COURSE__"
        has_base_anchor = False

        for comp in competencies:
            cid = comp["id"]
            for prereq in comp.get("prerequisites", []):
                if prereq in comp_ids:
                    undirected_adj[cid].add(prereq)
                    undirected_adj[prereq].add(cid)
                elif allowed_set and prereq in allowed_set:
                    if not has_base_anchor:
                        undirected_adj[base_anchor] = set()
                        has_base_anchor = True
                    undirected_adj[cid].add(base_anchor)
                    undirected_adj[base_anchor].add(cid)

        # Count connected components using BFS
        visited_nodes: Set[str] = set()
        components = 0
        for node in list(undirected_adj.keys()):
            if node not in visited_nodes:
                components += 1
                queue = [node]
                visited_nodes.add(node)
                while queue:
                    curr = queue.pop(0)
                    for neighbor in undirected_adj.get(curr, set()):
                        if neighbor not in visited_nodes:
                            visited_nodes.add(neighbor)
                            queue.append(neighbor)

        if components > 1:
            errors.append(
                f"Prerequisite DAG is disconnected ({components} components detected for {n} competencies). "
                f"Curriculum must form a single connected component."
            )

        # Root ratio check (competencies without any prerequisite dependencies)
        root_nodes = [
            c["id"]
            for c in competencies
            if not [p for p in c.get("prerequisites", []) if p]
        ]
        num_roots = len(root_nodes)
        max_roots = max(1, math.floor(0.20 * n))
        if num_roots > max_roots:
            errors.append(
                f"Too many root competencies ({num_roots}/{n} = {num_roots/n:.1%}). "
                f"Maximum allowed root ratio is 20% (max {max_roots} roots for {n} competencies). "
                f"Root competencies found: {', '.join(root_nodes)}."
            )

    return errors


def _build_manifest_pages_set(manifest_data: Optional[Dict[str, Any]]) -> Optional[Set[Tuple[str, Any]]]:
    """Index valid pages from pre_cta_manifest.json or legacy manifest for rapid evidence matching."""
    if not manifest_data:
        return None
    manifest_pages_set: Set[Tuple[str, Any]] = set()

    manifest_file_entries = manifest_data.get("files") or manifest_data.get("documents") or []
    for f in manifest_file_entries:
        doc = str(f.get("doc") or f.get("name") or "").strip().lower()
        doc_stem = Path(doc).stem.lower()
        doc_slug = str(f.get("doc_slug", "")).strip().lower()
        v_range = f.get("valid_page_range", [1, f.get("total_pages", 1)])
        start_p = int(v_range[0]) if len(v_range) > 0 else 1
        end_p = int(v_range[1]) if len(v_range) > 1 else int(f.get("total_pages", 1))

        for p in range(start_p, end_p + 1):
            for k in (doc, doc_stem, doc_slug):
                if k:
                    manifest_pages_set.add((k, p))
                    manifest_pages_set.add((k, str(p)))

    # 2. Legacy items or pages format
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

    # 3. Support part manifest top-level fields (page_count, total_pages, slice_range)
    total_part_p = manifest_data.get("page_count") or manifest_data.get("total_pages")
    if total_part_p:
        try:
            tp = int(total_part_p)
            for d_field in ["doc", "file", "name", "part_file", "source_file"]:
                d_val = str(manifest_data.get(d_field, "")).strip().lower()
                if d_val:
                    d_stem = Path(d_val).stem.lower()
                    for p in range(1, tp + 1):
                        manifest_pages_set.add((d_val, p))
                        manifest_pages_set.add((d_val, str(p)))
                        manifest_pages_set.add((d_stem, p))
                        manifest_pages_set.add((d_stem, str(p)))
        except (ValueError, TypeError):
            pass

    return manifest_pages_set


def _check_evidence_detailed(
    evidence: Optional[Dict[str, Any]],
    manifest_data: Optional[Dict[str, Any]],
    manifest_pages_set: Optional[Set[Tuple[str, Any]]],
    item_type: str,
    item_id: str,
    locator: Optional[JsonLineLocator] = None,
) -> Optional[str]:
    """Verify evidence citation against pre_cta_manifest.json with exact CTA-EV and CTA-DOCS messages."""
    if not manifest_data or not evidence:
        return None

    raw_doc = str(evidence.get("doc") or evidence.get("pdf") or "").strip()
    ev_doc = raw_doc.lower()
    ev_doc_stem = Path(ev_doc).stem.lower()
    ev_page = evidence.get("page")

    if not ev_doc or ev_page is None:
        return None

    # Check if doc exists in manifest
    known_docs: Dict[str, Tuple[int, int]] = {}
    files_list = manifest_data.get("files") or manifest_data.get("documents") or []
    for f in files_list:
        d_name = str(f.get("doc") or f.get("name") or f.get("doc_name") or "").strip()
        d_stem = Path(d_name).stem
        d_slug = str(f.get("doc_slug", "")).strip()
        v_range = f.get("valid_page_range", [1, f.get("total_pages", 1)])
        r_tuple = (int(v_range[0]) if len(v_range) > 0 else 1, int(v_range[1]) if len(v_range) > 1 else int(f.get("total_pages", 1)))
        if d_name:
            known_docs[d_name.lower()] = r_tuple
            known_docs[d_stem.lower()] = r_tuple
        if d_slug:
            known_docs[d_slug.lower()] = r_tuple

    # Legacy items/pages fallback if files not present
    if not known_docs:
        for it in manifest_data.get("items", manifest_data.get("pages", [])):
            d = str(it.get("doc", "")).strip()
            if d:
                known_docs[d.lower()] = (1, 999999)
                known_docs[Path(d).stem.lower()] = (1, 999999)

    line_no = locator.get_line(item_id) if locator else None
    line_tag = f"[Línea {line_no}] " if line_no else ""

    if ev_doc not in known_docs and ev_doc_stem not in known_docs:
        avail_docs = ", ".join(sorted(set(str(f.get("doc") or f.get("name") or "") for f in files_list if (f.get("doc") or f.get("name"))))) if files_list else "ninguno"
        return f"[CTA-DOCS] {line_tag}{item_type} '{item_id}': doc='{raw_doc}' no existe en pre_cta_manifest.json. Documentos disponibles: {avail_docs}."

    start_p, end_p = known_docs.get(ev_doc) or known_docs.get(ev_doc_stem, (1, 1))
    try:
        page_int = int(ev_page)
        if not (start_p <= page_int <= end_p):
            return f"[CTA-EV] {line_tag}{item_type} '{item_id}': doc='{raw_doc}' cita page={ev_page} fuera del rango de páginas PDF válidas {start_p}..{end_p} en pre_cta_manifest.json. Usa el número de página del PDF ({start_p}..{end_p}), NO la numeración impresa del libro."
    except (ValueError, TypeError):
        return f"[CTA-EV] {line_tag}{item_type} '{item_id}': doc='{raw_doc}' cita page='{ev_page}' que no es un entero válido."

    return None


def check_cta_prose_overflow(text: str, ctx: str) -> List[str]:
    """Detects KaTeX text macros exceeding 45 characters, causing mobile overflow.

    Checks \\text{}, \\textrm{}, \\mathrm{} within LaTeX formulas or strings.
    Emits canonical error tag [KATEX-PROSE-OVERFLOW].
    """
    if not isinstance(text, str) or not text:
        return []
    errors: List[str] = []
    pattern = re.compile(r"(?<![a-zA-Z])\\(text|textrm|mathrm)\s*\{")
    for m in pattern.finditer(text):
        start_idx = m.end()
        macro_name = m.group(1)
        depth = 1
        i = start_idx
        while i < len(text) and depth > 0:
            if text[i] == "\\":
                i += 2
                continue
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
            if depth == 0:
                break
            i += 1
        if depth == 0:
            inner_content = text[start_idx:i]
            if len(inner_content) > 45:
                preview = inner_content[:40] + "..." if len(inner_content) > 40 else inner_content
                errors.append(
                    f"[KATEX-PROSE-OVERFLOW] In {ctx}: \\{macro_name}{{{preview}}} block exceeds 45 chars ({len(inner_content)})."
                )
    return errors


_CTA_MATH_SPAN_RE = re.compile(
    r"(?<!\\)\$\$(?:\\.|[^$]|(?<!\\)\$(?!\$))*?(?<!\\)\$\$|(?<!\\)\$(?:\\.|[^$\\])+\$",
    re.DOTALL,
)
_CTA_MATH_ITER_RE = re.compile(
    r"(?<!\\)\$\$(.*?)(?<!\\)\$\$|(?<!\\)\$((?:\\.|[^$\\])+)\$",
    re.DOTALL,
)


def _validate_katex_syntax_safe(text: str, context: str, allow_template_vars: bool = True) -> List[str]:
    """Masks odd-backslash escaped dollars (\\$) before calling validate_katex_syntax
    so monetary spans like $\\$1$ are not split mid-token by legacy [^$] matchers.
    """
    masked = re.sub(r"(?<!\\)((?:\\\\)*)\\\$", r"\1USD", text)
    return validate_katex_syntax(masked, context, allow_template_vars=allow_template_vars)


def validate_distractor_math(d: Dict[str, Any], did: str) -> List[str]:
    """Audit all distractor text fields unconditionally for raw/orphaned LaTeX and KaTeX errors."""
    errors: List[str] = []
    for field in ["manifestation", "remediation_hint", "wrong_belief", "correct_belief", "omitted_step", "trigger"]:
        val = d.get(field)
        if isinstance(val, str) and val.strip():
            errors.extend(check_cta_prose_overflow(val, f"distractor '{did}' {field}"))
            # Check for corrupted ASCII control characters
            if any(c in val for c in ("\x07", "\x08", "\x0b", "\x0c", "\x0d")):
                errors.append(
                    f"Distractor ({did}): Corrupted ASCII control character (unescaped LaTeX backslash like \\rho, \\frac, \\alpha, \\beta) in '{field}'"
                )
            # Check for raw LaTeX outside $...$ or $$...$$
            text_outside_math = _CTA_MATH_SPAN_RE.sub("", val)
            has_raw_latex = any(re.search(p, text_outside_math) for p in RAW_LATEX_PATTERNS)
            if has_raw_latex:
                errors.append(f"Distractor '{did}' en '{field}' contiene comandos LaTeX sin delimitar por '$...$': {val}")

            clean_dollars = re.sub(r"(?<!\\)((?:\\\\)*)\\\$", r"\1", val)
            if "$" in clean_dollars:
                errors.extend(_validate_katex_syntax_safe(val, f"distractor '{did}' {field}", allow_template_vars=True))
    return errors


def check_cta_katex(
    cta_data: Dict[str, Any],
    locator: Optional[JsonLineLocator] = None,
) -> List[str]:
    """Inspect KaTeX math in competencies and distractors using validate_katex_syntax.

    Inspects:
    - competencies[].name
    - competencies[].description_latex and competencies[].description
    - competencies[].source_examples
    - distractors[].manifestation, remediation_hint, wrong_belief, correct_belief, omitted_step, trigger
    unconditionally auditing for raw LaTeX outside '$...$', prose overflow and validating KaTeX syntax.
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
            errors.extend(check_cta_prose_overflow(c_name, f"competency '{cid}' name"))
            if any(c in c_name for c in ("\x07", "\x08", "\x0b", "\x0c", "\x0d")):
                errors.append(
                    f"Competency ({cid}): Corrupted ASCII control character (unescaped LaTeX backslash like \\rho, \\frac, \\alpha, \\beta) in 'name'"
                )
            text_outside_math = _CTA_MATH_SPAN_RE.sub("", c_name)
            if any(re.search(p, text_outside_math) for p in RAW_LATEX_PATTERNS):
                raw_latex_items.setdefault("name", []).append((cid, c_name))
            if "$" in re.sub(r"(?<!\\)((?:\\\\)*)\\\$", r"\1", c_name):
                for kv in _validate_katex_syntax_safe(c_name, f"competency '{cid}' name", allow_template_vars=True):
                    katex_syntax_items.setdefault(kv, []).append((cid, "name"))
                for m_span in _CTA_MATH_ITER_RE.finditer(c_name):
                    m_text = m_span.group(1) if m_span.group(1) is not None else m_span.group(2)
                    m_disp = m_span.group(1) is not None
                    pk_err = _validate_pykatex_math_span(m_text, m_disp)
                    if pk_err:
                        katex_syntax_items.setdefault(f"KaTeX parse error: {pk_err}", []).append((cid, "name"))

        # competencies[].description_latex and competencies[].description
        for desc_key in ("description_latex", "description"):
            c_desc = comp.get(desc_key)
            if isinstance(c_desc, str) and c_desc.strip():
                errors.extend(check_cta_prose_overflow(c_desc, f"competency '{cid}' {desc_key}"))
                if any(c in c_desc for c in ("\x07", "\x08", "\x0b", "\x0c", "\x0d")):
                    errors.append(
                        f"Competency ({cid}): Corrupted ASCII control character (unescaped LaTeX backslash like \\rho, \\frac, \\alpha, \\beta) in '{desc_key}'"
                    )
                text_outside_math = _CTA_MATH_SPAN_RE.sub("", c_desc)
                if any(re.search(p, text_outside_math) for p in RAW_LATEX_PATTERNS):
                    raw_latex_items.setdefault(desc_key, []).append((cid, c_desc))
                if "$" in re.sub(r"(?<!\\)((?:\\\\)*)\\\$", r"\1", c_desc):
                    for kv in _validate_katex_syntax_safe(c_desc, f"competency '{cid}' {desc_key}", allow_template_vars=True):
                        katex_syntax_items.setdefault(kv, []).append((cid, desc_key))
                    for m_span in _CTA_MATH_ITER_RE.finditer(c_desc):
                        m_text = m_span.group(1) if m_span.group(1) is not None else m_span.group(2)
                        m_disp = m_span.group(1) is not None
                        pk_err = _validate_pykatex_math_span(m_text, m_disp)
                        if pk_err:
                            katex_syntax_items.setdefault(f"KaTeX parse error: {pk_err}", []).append((cid, desc_key))

        # competencies[].source_examples
        src_exs = comp.get("source_examples")
        if isinstance(src_exs, list):
            for ex_idx, ex_item in enumerate(src_exs):
                if isinstance(ex_item, str) and ex_item.strip():
                    errors.extend(check_cta_prose_overflow(ex_item, f"competency '{cid}' source_examples[{ex_idx}]"))
        elif isinstance(src_exs, str) and src_exs.strip():
            errors.extend(check_cta_prose_overflow(src_exs, f"competency '{cid}' source_examples"))

        # distractors[] math validation
        for d in comp.get("distractors", []):
            if not isinstance(d, dict):
                continue
            did = d.get("id", "UNKNOWN")
            for field in ["manifestation", "remediation_hint", "wrong_belief", "correct_belief", "omitted_step", "trigger"]:
                val = d.get(field)
                if isinstance(val, str) and val.strip():
                    errors.extend(check_cta_prose_overflow(val, f"distractor '{did}' {field}"))
                    if any(c in val for c in ("\x07", "\x08", "\x0b", "\x0c", "\x0d")):
                        errors.append(
                            f"Distractor ({did}): Corrupted ASCII control character (unescaped LaTeX backslash like \\rho, \\frac, \\alpha, \\beta) in '{field}'"
                        )
                    text_outside_math = _CTA_MATH_SPAN_RE.sub("", val)
                    if any(re.search(p, text_outside_math) for p in RAW_LATEX_PATTERNS):
                        raw_latex_items.setdefault(field, []).append((did, val))
                    clean_dollars = re.sub(r"(?<!\\)((?:\\\\)*)\\\$", r"\1", val)
                    if "$" in clean_dollars:
                        for kv in _validate_katex_syntax_safe(val, f"distractor '{did}' {field}", allow_template_vars=True):
                            katex_syntax_items.setdefault(kv, []).append((did, field))
                        for m_span in _CTA_MATH_ITER_RE.finditer(val):
                            m_text = m_span.group(1) if m_span.group(1) is not None else m_span.group(2)
                            m_disp = m_span.group(1) is not None
                            pk_err = _validate_pykatex_math_span(m_text, m_disp)
                            if pk_err:
                                katex_syntax_items.setdefault(f"KaTeX parse error: {pk_err}", []).append((did, field))

        # assumptions[] math validation
        for a in comp.get("assumptions", []):
            if not isinstance(a, dict):
                continue
            aid = a.get("id", f"A-{cid}")
            for field in ["statement_latex", "violation_consequence", "name", "role_in_proof"]:
                val = a.get(field)
                if isinstance(val, str) and val.strip():
                    errors.extend(check_cta_prose_overflow(val, f"assumption '{aid}' {field}"))
                    if any(c in val for c in ("\x07", "\x08", "\x0b", "\x0c", "\x0d")):
                        errors.append(
                            f"Assumption ({aid}): Corrupted ASCII control character (unescaped LaTeX backslash) in '{field}'"
                        )
                    text_outside_math = _CTA_MATH_SPAN_RE.sub("", val)
                    if any(re.search(p, text_outside_math) for p in RAW_LATEX_PATTERNS):
                        raw_latex_items.setdefault(field, []).append((aid, val))
                    clean_dollars = re.sub(r"(?<!\\)((?:\\\\)*)\\\$", r"\1", val)
                    if "$" in clean_dollars:
                        for kv in _validate_katex_syntax_safe(val, f"assumption '{aid}' {field}", allow_template_vars=True):
                            katex_syntax_items.setdefault(kv, []).append((aid, field))
                        for m_span in _CTA_MATH_ITER_RE.finditer(val):
                            m_text = m_span.group(1) if m_span.group(1) is not None else m_span.group(2)
                            m_disp = m_span.group(1) is not None
                            pk_err = _validate_pykatex_math_span(m_text, m_disp)
                            if pk_err:
                                katex_syntax_items.setdefault(f"KaTeX parse error: {pk_err}", []).append((aid, field))

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
                eff_tid = tid if (tid and tid != "UNKNOWN") else "COMP"
                ln = locator.get_line(eff_tid, f) if locator else (locator.get_line(eff_tid) if locator else None)
                l_info = f" (línea {ln})" if ln else ""
                loc_strs.append(f"{eff_tid}.{f}{l_info}")
            errors.append(f"Error de sintaxis KaTeX en {len(items)} campos: {', '.join(loc_strs)}: {kv}")
        else:
            tid, f = items[0]
            eff_tid = tid if (tid and tid != "UNKNOWN") else "COMP"
            ln = locator.get_line(eff_tid, f) if locator else (locator.get_line(eff_tid) if locator else None)
            l_info = f" (línea {ln})" if ln else ""
            if eff_tid in kv:
                errors.append(f"{kv}{l_info}")
            else:
                errors.append(f"In '{eff_tid}'.{f}{l_info}: {kv}")

    return list(dict.fromkeys(errors))


_VALID_RECOMMENDED_MODALITIES = frozenset({
    "multiple_choice_7_options",
    "multiple_select",
    "fill_in_the_blank",
    "open_symbolic",
    "proof_dag",
    "adversarial_break",
    "unstructured_model",
    "invariant_canvas",
    "concept_matching",
})


def _validate_competencies_rules(
    competencies: List[Dict[str, Any]],
    manifest_data: Optional[Dict[str, Any]] = None,
    comp_validator: Optional[jsonschema.Draft7Validator] = None,
    is_part: bool = False,
    locator: Optional[JsonLineLocator] = None,
    require_assumptions: bool = False,
    require_modalities: bool = True,
    warnings: Optional[List[str]] = None,
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

        # Rule CTA-PREFIX-TYPE-MISMATCH: Canonical ID prefixes must match competency category
        # (accepts Spanish 'H-' = Hecho = fact as well as 'F-' / 'Fact-' = fact)
        cid_low = str(cid or "").lower()
        for prefixes, valid_types, expected_rule in (
            (("hab-", "skill-"), ("skill",), "Hab-/Skill- -> skill"),
            (("h-", "f-", "fact-"), ("fact",), "H- (Hecho) / F- (Fact) -> fact"),
            (("c-", "concept-"), ("concept",), "C-/Concept- -> concept"),
            (("pre-",), ("fact", "concept"), "PRE- -> fact/concept"),
        ):
            if cid_low.startswith(prefixes) and ctype in ("fact", "concept", "skill") and ctype not in valid_types:
                line_no_pfx = locator.get_line(cid) if locator else None
                line_tag_pfx = f" [Línea {line_no_pfx}]" if line_no_pfx else ""
                warn_pfx = (
                    f"WARNING: [CTA-PREFIX-TYPE-MISMATCH]{line_tag_pfx} Competency '{cid}' declares type='{ctype}' "
                    f"incompatible with ID prefix (expected {expected_rule})."
                )
                if warnings is not None:
                    warnings.append(warn_pfx)
                print(warn_pfx, file=sys.stderr)
                break
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

        # Rule CTA-ASSUMPTIONS-MISSING: Skill or Concept must declare >= 1 valid assumption with len >= 10
        if require_assumptions and ctype in ("skill", "concept"):
            assumptions = comp.get("assumptions")
            line_no = locator.get_line(cid) if locator else None
            line_tag = f" [Línea {line_no}]" if line_no else ""
            if not assumptions or not isinstance(assumptions, list) or len(assumptions) == 0:
                errors.append(
                    f"[CTA-ASSUMPTIONS-MISSING]{line_tag} Competency '{cid}' ({ctype}) requires at least 1 valid assumption."
                )
            else:
                valid_cnt = 0
                for a_idx, a in enumerate(assumptions, start=1):
                    if isinstance(a, dict):
                        stmt = str(a.get("statement_latex") or "").strip()
                        viol = str(a.get("violation_consequence") or "").strip()
                        if len(stmt) >= 10 and len(viol) >= 10:
                            valid_cnt += 1
                        else:
                            errors.append(
                                f"[CTA-ASSUMPTIONS-MISSING]{line_tag} Competency '{cid}' assumption #{a_idx} must have statement_latex and violation_consequence of at least 10 chars."
                            )
                    else:
                        errors.append(
                            f"[CTA-ASSUMPTIONS-MISSING]{line_tag} Competency '{cid}' assumption #{a_idx} is not a valid dictionary."
                        )
                if valid_cnt == 0 and not any("[CTA-ASSUMPTIONS-MISSING]" in e and cid in e for e in errors):
                    errors.append(
                        f"[CTA-ASSUMPTIONS-MISSING]{line_tag} Competency '{cid}' ({ctype}) requires at least 1 valid assumption (len >= 10)."
                    )

        rec_mods = comp.get("recommended_modalities")
        line_no_rm = locator.get_line(cid, "recommended_modalities") if locator else None
        if not line_no_rm and locator:
            line_no_rm = locator.get_line(cid)
        line_tag_rm = f" [Línea {line_no_rm}]" if line_no_rm else ""
        if rec_mods is None:
            if require_modalities:
                errors.append(
                    f"[CTA-MODALITY-MISSING]{line_tag_rm} Competency '{cid}' requires "
                    f"{_MIN_MODALITIES_PER_COMPETENCY}..{_MAX_MODALITIES_PER_COMPETENCY} canonical recommended_modalities in contract v2."
                )
        elif not isinstance(rec_mods, list):
            errors.append(
                f"[CTA-MODALITY-INVALID]{line_tag_rm} Competency '{cid}' recommended_modalities must be a list of canonical modality strings."
            )
        elif len(rec_mods) == 0:
            if require_modalities:
                errors.append(
                    f"[CTA-MODALITY-MISSING]{line_tag_rm} Competency '{cid}' has empty recommended_modalities; "
                    f"contract v2 requires {_MIN_MODALITIES_PER_COMPETENCY}..{_MAX_MODALITIES_PER_COMPETENCY} canonical modalities."
                )
        else:
            invalid_rm = False
            for rm in rec_mods:
                if not isinstance(rm, str) or rm not in _VALID_RECOMMENDED_MODALITIES:
                    invalid_rm = True
                    errors.append(
                        f"[CTA-MODALITY-INVALID]{line_tag_rm} Competency '{cid}' has invalid recommended_modality '{rm}'. "
                        f"Allowed: {sorted(_VALID_RECOMMENDED_MODALITIES)}"
                    )
            if not invalid_rm and (ctype == "skill" or str(cid).startswith("Hab-")) and "multiple_choice_7_options" in rec_mods:
                errors.append(
                    f"[M20-MC7-CAP]{line_tag_rm} Competency '{cid}' (skill) cannot include 'multiple_choice_7_options' (MC7) "
                    f"in recommended_modalities (0 MC7 allowed in Skill competencies)."
                )
            if not invalid_rm and "multiple_choice_7_options" in rec_mods and len(distractors) < 6:
                errors.append(
                    f"[CTA-MC7-DISTRACTORS]{line_tag_rm} Competency '{cid}' ({ctype}) includes "
                    f"'multiple_choice_7_options' (MC7) in recommended_modalities but only declares "
                    f"{len(distractors)} distractors (MC7 requires >= 6 distinct distractors; "
                    f"either declare >= 6 distractors or remove 'multiple_choice_7_options')."
                )
            if require_modalities and not invalid_rm:
                unique_rm_count = len(set(m for m in rec_mods if isinstance(m, str)))
                if unique_rm_count != len(rec_mods):
                    errors.append(
                        f"[CTA-MODALITY-RANGE]{line_tag_rm} Competency '{cid}' has duplicate entries in recommended_modalities ({rec_mods}). "
                        f"Must declare {_MIN_MODALITIES_PER_COMPETENCY}..{_MAX_MODALITIES_PER_COMPETENCY} unique canonical modalities."
                    )
                if not (_MIN_MODALITIES_PER_COMPETENCY <= len(rec_mods) <= _MAX_MODALITIES_PER_COMPETENCY):
                    errors.append(
                        f"[CTA-MODALITY-RANGE]{line_tag_rm} Competency '{cid}' declares {len(rec_mods)} recommended_modalities; "
                        f"required range is {_MIN_MODALITIES_PER_COMPETENCY}..{_MAX_MODALITIES_PER_COMPETENCY}."
                    )

        # Calibrated competency warnings (no hard-fail):
        if warnings is not None:
            desc_val = comp.get("description_latex")
            if desc_val is not None and isinstance(desc_val, str):
                desc_str = desc_val.strip()
                if len(desc_str) < 80:
                    line_no = locator.get_line(cid, "description_latex") if locator else (locator.get_line(cid) if locator else None)
                    line_tag = f" (línea {line_no})" if line_no else ""
                    warnings.append(
                        f"[CTA-DESC-SHORT]{line_tag} Competency '{cid}' description_latex has fewer than 80 chars ({len(desc_str)}): '{desc_str}'"
                    )

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

            # Hard-fail: manifestation == correct_belief
            manif = str(d.get("manifestation") or "").strip()
            cb = str(d.get("correct_belief") or "").strip()
            norm_m = manif.replace("$", "").strip()
            norm_cb = cb.replace("$", "").strip()
            if norm_m and norm_cb and norm_m == norm_cb:
                line_no = locator.get_line(did, "manifestation") if locator else (locator.get_line(did) if locator else None)
                line_tag = f" (línea {line_no})" if line_no else ""
                errors.append(
                    f"CTA-DISTRACTOR violation: Distractor '{did}'{line_tag} manifestation '{manif}' is identical to correct_belief."
                )

            # Calibrated warnings (no hard-fail):
            if warnings is not None:
                # [CTA-MANIF-NEQ]: manifestation contains \ne or \neq appearing to be mechanical inversion of correct_belief
                if r"\ne" in manif or r"\neq" in manif:
                    cb_sub_ne = re.sub(r"\s*=\s*", r" \\ne ", norm_cb).replace(" ", "")
                    cb_sub_neq = re.sub(r"\s*=\s*", r" \\neq ", norm_cb).replace(" ", "")
                    m_compact = norm_m.replace(" ", "")
                    if m_compact in (cb_sub_ne, cb_sub_neq):
                        line_no = locator.get_line(did, "manifestation") if locator else (locator.get_line(did) if locator else None)
                        line_tag = f" (línea {line_no})" if line_no else ""
                        warnings.append(
                            f"[CTA-MANIF-NEQ]{line_tag} Distractor '{did}' manifestation '{manif}' appears to be a mechanical negation of correct_belief."
                        )

                # [CTA-HINT-SHORT]: calibrated soft-warning band 70..79 chars (< 70 hard-fails via cta.schema.json minLength: 70)
                hint = str(d.get("remediation_hint") or "").strip()
                if hint and 70 <= len(hint) < 80:
                    line_no = locator.get_line(did, "remediation_hint") if locator else (locator.get_line(did) if locator else None)
                    line_tag = f" (línea {line_no})" if line_no else ""
                    warnings.append(
                        f"[CTA-HINT-SHORT]{line_tag} Distractor '{did}' remediation_hint is in calibrated warning band 70-79 chars ({len(hint)} < 80): '{hint}'"
                    )

            # Check distractor evidence
            ev = d.get("evidence")
            if manifest_data and ev:
                ev_err = _check_evidence_detailed(ev, manifest_data, manifest_pages_set, "Distractor", did, locator=locator)
                if ev_err:
                    errors.append(ev_err)

        # Check competency evidence
        if manifest_data and comp.get("evidence"):
            for ev in comp.get("evidence", []):
                ev_err = _check_evidence_detailed(ev, manifest_data, manifest_pages_set, "Competencia", cid, locator=locator)
                if ev_err:
                    errors.append(ev_err)

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

    return errors


def check_cta_part(
    data: Any,
    manifest_data: Optional[Dict[str, Any]] = None,
    file_path: Optional[Union[str, Path]] = None,
    locator: Optional[JsonLineLocator] = None,
    require_assumptions: bool = False,
    require_modalities: Optional[bool] = None,
    warnings_out: Optional[List[str]] = None,
) -> ValidationResult:
    """Validate sectional CTA part (cta_part_XX.json).

    Enforces local competency schema, CTA-D1 & CTA-D2 quotas, and evidence validity
    without requiring globally unique IDs or complete cross-section prerequisite closures.
    """
    errors: List[str] = []
    if locator is None:
        locator = JsonLineLocator(file_path)

    raw_cv = int(data.get("contract_version", data.get("CTA_CONTRACT_VERSION", 1))) if isinstance(data, dict) else 1
    eff_require_assumptions = bool(require_assumptions or raw_cv >= 2)
    eff_require_modalities = (raw_cv >= 2) if require_modalities is None else bool(require_modalities)

    if isinstance(data, list):
        competencies = data
    elif isinstance(data, dict):
        competencies = data.get("competencies", [])
    else:
        return ValidationResult(False, ["cta_part data must be a JSON object with 'competencies' or a JSON array."])

    if not competencies:
        return ValidationResult(False, ["cta_part contains zero competencies."])

    base_schema = load_schema("cta.schema.json")
    comp_subschema = base_schema.get("definitions", {}).get("competency", {})
    comp_schema = {
        "$schema": base_schema.get("$schema", "http://json-schema.org/draft-07/schema#"),
        "definitions": base_schema.get("definitions", {}),
        **comp_subschema,
    }
    comp_validator = jsonschema.Draft7Validator(comp_schema)

    part_warnings: List[str] = []
    part_errors = _validate_competencies_rules(
        competencies=competencies,
        manifest_data=manifest_data,
        comp_validator=comp_validator,
        is_part=True,
        locator=locator,
        require_assumptions=eff_require_assumptions,
        require_modalities=eff_require_modalities,
        warnings=part_warnings,
    )
    errors.extend(part_errors)

    katex_errors = check_cta_katex(data if isinstance(data, dict) else {"competencies": data}, locator=locator)
    errors.extend(katex_errors)

    if warnings_out is not None:
        warnings_out.extend(part_warnings)

    unique_errors = list(dict.fromkeys(errors))
    return ValidationResult(len(unique_errors) == 0, unique_errors, part_warnings)


def check_cta_bloom_portfolio(
    competencies: List[Dict[str, Any]],
    exclude_ids: Optional[Set[str]] = None,
    warnings: Optional[List[str]] = None,
    enforce_hard_fail: bool = True,
) -> List[str]:
    """Validate adaptive portfolio Bloom floor across eligible contract v2 competencies."""
    if compute_cta_bloom_portfolio_metrics is None:
        return []
    metrics = compute_cta_bloom_portfolio_metrics(competencies, exclude_ids=exclude_ids)
    if not metrics.get("active_gate") or metrics.get("passes"):
        return []

    weak_parts: List[str] = []
    for wc in metrics.get("weak_competencies", []):
        weak_parts.append(
            f"{wc['id']} ({wc['type']}, expected={wc['expected_bloom']:.2f}, "
            f"assumptions={wc['assumptions_count']}, mods={wc['recommended_modalities']})"
        )
    weak_str = "; ".join(weak_parts) if weak_parts else "ninguna"
    msg = (
        f"[CTA-BLOOM-FLOOR] Portafolio de modalidades por debajo del piso cognitivo adaptativo "
        f"(evaluadas {metrics['eligible_competencies']} competencias): "
        f"expected_bloom_index={metrics['expected_bloom_index']:.3f} (piso {metrics['adaptive_bloom_floor']:.3f}), "
        f"evaluate_capable={metrics['evaluate_capable_ratio']*100:.1f}% (piso {metrics['adaptive_eval_floor']*100:.1f}%), "
        f"low_modalities={metrics['low_modality_ratio']*100:.1f}% (tope {metrics['adaptive_low_cap']*100:.1f}%). "
        f"Brechas: {', '.join(metrics['violations'])}. "
        f"Competencias más débiles a promover: {weak_str}. "
        f"Acción: usa la 5.ª clave 'adjust_modalities' en cta_harmonize.json para reemplazar modalidades bajas "
        f"(MC7/concept_matching) por modalidades Evaluate-capable (adversarial_break, proof_dag, multiple_select, "
        f"o unstructured_model solo si assumptions_count >= 1) sin mutar nodos [BASE]."
    )
    if enforce_hard_fail:
        return [msg]
    if warnings is not None:
        warnings.append(msg)
    return []


_DISAMBIG_STOPWORDS: Set[str] = {
    "de", "la", "el", "en", "y", "a", "o", "e", "los", "las", "del", "al",
    "un", "una", "unos", "unas", "por", "para", "con", "sin", "sobre", "su",
    "sus", "que", "se", "es", "son", "como", "entre", "the", "of", "and",
    "in", "to", "for", "with", "on", "by", "as", "an", "or", "is", "are",
    "concepto", "concept", "hecho", "fact", "habilidad", "skill",
    "competencia", "competency", "description", "descripcion",
}


def _normalize_disambig_text(text: str) -> str:
    """Fold accents, strip non-alphanumeric chars, and lowercase for lexical comparison."""
    if not text:
        return ""
    folded = "".join(
        ch for ch in unicodedata.normalize("NFKD", str(text))
        if unicodedata.category(ch) != "Mn"
    ).lower()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", folded)).strip()


def _tokenize_disambig_text(text: str, cid: str = "") -> Set[str]:
    """Extract normalized non-stopword alphanumeric tokens (len >= 2), excluding own CID tokens."""
    norm = _normalize_disambig_text(text)
    if not norm:
        return set()
    cid_toks = set(_normalize_disambig_text(cid).split()) if cid else set()
    return {
        t for t in norm.split()
        if len(t) >= 2 and t not in _DISAMBIG_STOPWORDS and t not in cid_toks
    }


def _skeleton_without_index(name: str, cid: str) -> str:
    """Mask ID and trailing/ordinal index tokens so intentionally indexed pairs are distinguished."""
    s = _normalize_disambig_text(name)
    cid_norm = _normalize_disambig_text(cid)
    if cid_norm:
        s = re.sub(rf"\b{re.escape(cid_norm)}\b", " ", s)
    s = re.sub(r"\b(?:[pv]?\d+|i{1,3}|iv|vi{0,3})\b", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def check_cta_disambiguation(
    competencies: List[Dict[str, Any]],
    existing_comp_ids: Optional[Set[str]] = None,
    locator: Optional[JsonLineLocator] = None,
    warnings: Optional[List[str]] = None,
) -> List[str]:
    """D1 curricular disambiguation gate across same-category competencies."""
    errors: List[str] = []
    base_ids = set(existing_comp_ids or ())
    prepared: List[Dict[str, Any]] = []

    for idx, comp in enumerate(competencies):
        if not isinstance(comp, dict):
            continue
        cid = str(comp.get("id") or f"comp_{idx}")
        ctype = str(comp.get("type") or "").strip().lower()
        if ctype not in ("fact", "concept", "skill"):
            continue
        name = str(comp.get("name") or "")
        desc = str(comp.get("description_latex") or comp.get("description") or "")
        norm_name = _normalize_disambig_text(name)
        skel_name = _skeleton_without_index(name, cid)
        name_tokens = _tokenize_disambig_text(name, cid=cid)
        tokens = _tokenize_disambig_text(f"{name} {desc}", cid=cid)
        prepared.append({
            "id": cid,
            "type": ctype,
            "norm_name": norm_name,
            "skel_name": skel_name,
            "name_tokens": name_tokens,
            "tokens": tokens,
            "desc_len": len(desc.strip()),
        })

    for i in range(len(prepared)):
        c1 = prepared[i]
        for j in range(i + 1, len(prepared)):
            c2 = prepared[j]
            if c1["type"] != c2["type"]:
                continue
            if base_ids and c1["id"] in base_ids and c2["id"] in base_ids:
                continue

            norm1, norm2 = c1["norm_name"], c2["norm_name"]
            if (
                norm1 != norm2
                and c1["skel_name"]
                and c1["skel_name"] == c2["skel_name"]
            ):
                continue

            nt1, nt2 = c1["name_tokens"], c2["name_tokens"]
            name_sim = 0.0
            if norm1 and norm2 and norm1 == norm2:
                name_sim = 1.0
            elif len(nt1) >= 2 and len(nt2) >= 2:
                nt_union = nt1 | nt2
                if nt_union:
                    name_sim = len(nt1 & nt2) / len(nt_union)

            toks1, toks2 = c1["tokens"], c2["tokens"]
            jaccard = 0.0
            if len(toks1) >= 4 and len(toks2) >= 4:
                union = toks1 | toks2
                if union:
                    jaccard = len(toks1 & toks2) / len(union)

            line_no = locator.get_line(c1["id"]) if locator else None
            line_tag = f" [Línea {line_no}]" if line_no else ""
            high_jaccard = jaccard >= 0.45 and (
                (c1["desc_len"] >= 80 and c2["desc_len"] >= 80) or name_sim > 0.0
            )
            if name_sim >= 0.60 or high_jaccard:
                errors.append(
                    f"[CTA-OVERLAP-HIGH]{line_tag} Solapamiento curricular severo en categoría '{c1['type']}' "
                    f"entre '{c1['id']}' y '{c2['id']}' (name_sim={name_sim:.2f}, jaccard={jaccard:.2f}). "
                    f"Desambigua alcance/evaluación o fusionalas antes de particionar shards."
                )
            elif jaccard >= 0.30:
                if warnings is not None:
                    warnings.append(
                        f"WARNING: [CTA-OVERLAP-WARN]{line_tag} Solapamiento moderado en categoría '{c1['type']}' "
                        f"entre '{c1['id']}' y '{c2['id']}' (jaccard={jaccard:.2f}, name_sim={name_sim:.2f}). "
                        f"Verifica frontera pedagógica clara."
                    )

    return errors


def validate_cta_rules(
    cta_data: Dict[str, Any],
    manifest_data: Optional[Dict[str, Any]] = None,
    file_path: Optional[Union[str, Path]] = None,
    locator: Optional[JsonLineLocator] = None,
    allowed_prereq_ids: Optional[Set[str]] = None,
    require_assumptions: bool = False,
    require_modalities: Optional[bool] = None,
    warnings_out: Optional[List[str]] = None,
    exclude_bloom_ids: Optional[Set[str]] = None,
    enforce_bloom_gate: Optional[bool] = None,
) -> ValidationResult:
    """Validate all cognitive and psychometric rules on cta.json."""
    errors = []
    if locator is None:
        locator = JsonLineLocator(file_path)

    raw_cv = int(cta_data.get("contract_version", cta_data.get("CTA_CONTRACT_VERSION", 1))) if isinstance(cta_data, dict) else 1
    eff_require_assumptions = bool(require_assumptions or raw_cv >= 2)
    eff_require_modalities = (raw_cv >= 2) if require_modalities is None else bool(require_modalities)

    # 1. JSON Schema validation
    schema_errs = validate_cta_schema(cta_data, locator=locator)
    errors.extend(schema_errs)

    competencies = cta_data.get("competencies", [])
    if not competencies:
        errors.append("cta.json contains zero competencies.")
        return ValidationResult(False, errors)

    comp_warnings: List[str] = []
    comp_errors = _validate_competencies_rules(
        competencies=competencies,
        manifest_data=manifest_data,
        comp_validator=None,
        is_part=False,
        locator=locator,
        require_assumptions=eff_require_assumptions,
        require_modalities=eff_require_modalities,
        warnings=comp_warnings,
    )
    errors.extend(comp_errors)

    # Extract base competency IDs (for --append mode) before Bloom portfolio & DAG checks
    delta_info = None
    if manifest_data and isinstance(manifest_data, dict):
        delta_info = manifest_data.get("delta") or manifest_data.get("existing_course")
    existing_comp_ids: Set[str] = set()
    if isinstance(delta_info, dict):
        existing_comp_ids = set(delta_info.get("existing_competency_ids", []))
    if allowed_prereq_ids:
        existing_comp_ids = existing_comp_ids | set(allowed_prereq_ids)

    # 2b. Portfolio Bloom quality gate [CTA-BLOOM-FLOOR] (global CTA only, v2+, >= 5 delta comps)
    if eff_require_modalities and enforce_bloom_gate is not False:
        eff_exclude_bloom = (set(exclude_bloom_ids or ()) | existing_comp_ids) or None
        bloom_errors = check_cta_bloom_portfolio(
            competencies=competencies,
            exclude_ids=eff_exclude_bloom,
            warnings=comp_warnings,
            enforce_hard_fail=True,
        )
        errors.extend(bloom_errors)

    # 3. Curricular disambiguation gate (D1 overlap check on delta/new pairs)
    disambig_errors = check_cta_disambiguation(
        competencies=competencies,
        existing_comp_ids=existing_comp_ids,
        locator=locator,
        warnings=comp_warnings,
    )
    errors.extend(disambig_errors)

    # 4. Prerequisites DAG check (respecting base competencies in --append mode)
    dag_errors = check_prerequisites_dag(competencies, allowed_prereq_ids=existing_comp_ids)
    errors.extend(dag_errors)

    # 5. KaTeX syntax validation
    katex_errors = check_cta_katex(cta_data, locator=locator)
    errors.extend(katex_errors)

    if warnings_out is not None:
        warnings_out.extend(comp_warnings)

    unique_errors = list(dict.fromkeys(errors))
    return ValidationResult(len(unique_errors) == 0, unique_errors, comp_warnings)


def main():
    parser = argparse.ArgumentParser(description="Validate cta.json taxonomy and distractors")
    parser.add_argument("cta_path", help="Path to cta.json or cta_part_XX.json")
    parser.add_argument("--work", "--work-dir", dest="work", default=None, help="Working directory containing pre_cta_manifest.json")
    parser.add_argument("--manifest", help="Optional path to pre_cta_manifest.json for evidence verification")
    parser.add_argument(
        "--part",
        action="store_true",
        help="Validate sectional CTA part (cta_part_XX.json) without cross-section closing",
    )
    parser.add_argument(
        "--require-assumptions",
        action="store_true",
        default=False,
        help="Require assumptions for Skill and Concept competencies (auto-activated if contract_version >= 2)",
    )
    parser.add_argument(
        "--no-require-modalities",
        action="store_true",
        default=False,
        help="Allow omitting recommended_modalities in contract v2 (legacy v1 compatibility)",
    )
    parser.add_argument(
        "--no-bloom-gate",
        action="store_true",
        default=False,
        help="Bypass the [CTA-BLOOM-FLOOR] portfolio gate (for retrospective audits)",
    )
    args = parser.parse_args()

    cta_file = Path(args.cta_path).resolve()
    if not cta_file.exists():
        print(f"Error: file not found at {cta_file}", file=sys.stderr)
        sys.exit(1)

    work_dir = Path(args.work).resolve() if args.work else cta_file.parent
    if work_dir.name == "cta_parts":
        work_dir = work_dir.parent

    manifest_p = None
    if args.manifest:
        manifest_p = Path(args.manifest).resolve()
    else:
        part_candidates = list(cta_file.parent.glob("part_manifest*.json"))
        if part_candidates:
            manifest_p = part_candidates[0]
        elif (work_dir / "pre_cta_manifest.json").is_file():
            manifest_p = work_dir / "pre_cta_manifest.json"
        elif (cta_file.parent.parent / "pre_cta_manifest.json").is_file():
            manifest_p = cta_file.parent.parent / "pre_cta_manifest.json"
        else:
            manifest_p = work_dir / "pre_cta_manifest.json"

    if not manifest_p or not manifest_p.is_file():
        print("BLOCKER:: No existe pre_cta_manifest.json", file=sys.stderr)
        sys.exit(2)

    with open(manifest_p, "r", encoding="utf-8") as f:
        manifest_data = json.load(f)

    with open(cta_file, "r", encoding="utf-8") as f:
        cta_data = json.load(f)

    locator = JsonLineLocator(cta_file)

    contract_ver = int(cta_data.get("contract_version", cta_data.get("CTA_CONTRACT_VERSION", 1))) if isinstance(cta_data, dict) else 1
    eff_req_assumptions = bool(args.require_assumptions or contract_ver >= 2)
    eff_req_modalities: Optional[bool] = False if args.no_require_modalities else None

    if args.part:
        res = check_cta_part(
            cta_data,
            manifest_data,
            file_path=cta_file,
            locator=locator,
            require_assumptions=eff_req_assumptions,
            require_modalities=eff_req_modalities,
        )
        valid, errors = res[0], res[1]
        for w in getattr(res, "warnings", []):
            print(f"WARNING: {w}", file=sys.stderr)
        if not valid:
            print(f"FAIL: {len(errors)} validation errors in cta_part:", file=sys.stderr)
            for e in errors:
                print(f"  - {e}", file=sys.stderr)
            sys.exit(1)
        print("PASS: cta_part satisfies local schema, CTA-D1, CTA-D2, and evidence constraints.")
        sys.exit(0)

    res = validate_cta_rules(
        cta_data,
        manifest_data,
        file_path=cta_file,
        locator=locator,
        require_assumptions=eff_req_assumptions,
        require_modalities=eff_req_modalities,
        enforce_bloom_gate=(False if args.no_bloom_gate else None),
    )
    valid, errors = res[0], res[1]
    for w in getattr(res, "warnings", []):
        print(f"WARNING: {w}", file=sys.stderr)
    if not valid:
        print(f"FAIL: {len(errors)} validation errors in cta.json:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    print("PASS: cta.json satisfies all schema, CTA-D1, CTA-D2, and evidence constraints.")
    sys.exit(0)


if __name__ == "__main__":
    main()


# Public alias for pipeline compatibility
check_cta_file = validate_cta_rules
