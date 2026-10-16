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
import hashlib
import json
import os
import re
import sys
import zlib
from collections import defaultdict
from datetime import datetime, timezone
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
from engine.invariants import check_instance_invariants, validate_katex_syntax
from engine.instantiate import instantiate_competency, competency_seed_base
from engine.sandbox import (
    execute_sandbox_batch,
    validate_code_ast,
    check_latex_escape_corruption,
    check_latex_escape_corruption_structured,
    warm_up_sandbox,
    SandboxExecutionError,
    SandboxTimeoutError,
    SecurityViolationError,
)
from validator.core import validate_course_content


AGENT_WARNING_NOTE = (
    "NOTA PARA EL AGENTE: NO abras ni inspecciones el código de check_templates.py ni rules.py. "
    "Corrige directamente el texto en tu script generador."
)


class DiagnosticError(str):
    """Enriched diagnostic error string with structured metadata for canonical aggregation."""
    rule_tag: str
    competency: str
    template: str
    item_id: Union[str, List[str]]
    field_name: str
    snippet: str
    cause: str
    actions: List[str]
    lines: List[int]
    file_path: Optional[str]

    def __new__(
        cls,
        content: str,
        rule_tag: str = "",
        competency: str = "",
        template: str = "",
        item_id: Union[str, List[str]] = "",
        field_name: str = "",
        snippet: str = "",
        cause: str = "",
        actions: Optional[List[str]] = None,
        lines: Optional[List[int]] = None,
        file_path: Optional[str] = None,
    ):
        obj = super().__new__(cls, content)
        obj.rule_tag = rule_tag
        obj.competency = competency
        obj.template = template
        obj.item_id = item_id
        obj.field_name = field_name
        obj.snippet = snippet
        obj.cause = cause
        obj.actions = actions or []
        obj.lines = list(lines) if lines else []
        obj.file_path = file_path
        return obj


def format_diagnostic_error(
    rule_tag: str,
    competency: str,
    template: str,
    item_id: Union[str, List[str]],
    field_name: str,
    snippet: str,
    cause: str,
    actions: List[str],
    lines: Optional[List[int]] = None,
    file_path: Optional[str] = None,
) -> DiagnosticError:
    """Format validation error with enriched surgical and prescriptive diagnostics."""
    if isinstance(item_id, list):
        if not item_id:
            items_str = "N/A"
        elif len(item_id) > 5 and all(str(x).startswith("seed=") for x in item_id):
            seed_ints = sorted(int(str(x).split("=")[1]) for x in item_id if "=" in str(x))
            items_str = f"semillas {seed_ints[0]}..{seed_ints[-1]} ({len(item_id)} semillas)"
        elif len(item_id) > 6:
            items_str = f"{item_id[0]}, {item_id[1]}, ... {item_id[-1]} ({len(item_id)} reactivos)"
        elif len(item_id) > 1:
            items_str = ", ".join(str(x) for x in item_id)
        elif len(item_id) == 1:
            items_str = str(item_id[0])
        else:
            items_str = str(item_id)

        if len(item_id) > 1 or "semillas" in items_str or "reactivos" in items_str:
            reactivo_label = "Reactivos"
        else:
            reactivo_label = "Reactivo"
    else:
        items_str = str(item_id)
        reactivo_label = "Reactivo"

    if lines:
        unique_lines = sorted(set(lines))
        if len(unique_lines) == 1:
            lines_str = f", Línea: {unique_lines[0]}"
        else:
            lines_str = f", Líneas: {', '.join(str(l) for l in unique_lines)} ({len(lines)} ocurrencias)"
    else:
        lines_str = ""

    actions_formatted = "\n".join(f"      {idx + 1}. {act}" for idx, act in enumerate(actions))
    primary_action = actions[0] if actions else "Corrige el archivo generador."
    raw_str = (
        f"[-] [{rule_tag}]\n"
        f"    UBICACIÓN: Competencia: '{competency}', Plantilla: '{template}', {reactivo_label}: '{items_str}'{lines_str}, Campo: '{field_name}'\n"
        f"    FRAGMENTO INFRACTOR: {snippet}\n"
        f"    CAUSA: {cause}\n"
        f"    ACTION REQUIRED: {primary_action}\n"
        f"    ACCIONES CORRECTIVAS:\n"
        f"{actions_formatted}\n"
        f"    {AGENT_WARNING_NOTE}"
    )
    return DiagnosticError(
        raw_str,
        rule_tag=rule_tag,
        competency=competency,
        template=template,
        item_id=item_id,
        field_name=field_name,
        snippet=snippet,
        cause=cause,
        actions=actions,
        lines=lines or [],
        file_path=file_path,
    )


def find_lines_in_file(fpath: Path, pattern: str) -> List[int]:
    """Scan file lines for a pattern or snippet to dynamically identify offending lines."""
    if not fpath.is_file() or not pattern:
        return []
    try:
        lines = fpath.read_text(encoding="utf-8", errors="replace").splitlines()
        clean_pat = pattern.strip()
        if len(clean_pat) > 50:
            clean_pat = clean_pat[:50].strip()
        found = []
        for idx, line in enumerate(lines, start=1):
            if clean_pat in line:
                found.append(idx)
        return found
    except Exception:
        return []


def find_template_field_line(fpath: Path, tpl_id: str, field_name: Optional[str] = None) -> List[int]:
    """Scan file lines to locate template ID block and optionally field_name within that block."""
    if not fpath.is_file() or not tpl_id:
        return []
    try:
        lines = fpath.read_text(encoding="utf-8", errors="replace").splitlines()
        tpl_idx = -1
        # Find template id line
        for idx, l in enumerate(lines, start=1):
            if f'"{tpl_id}"' in l or f"'{tpl_id}'" in l:
                tpl_idx = idx
                break
        if tpl_idx == -1:
            return []
        if not field_name:
            return [tpl_idx]
        # Search forward for field_name until next template id or end of object
        field_target = f'"{field_name}"'
        field_target_alt = f"'{field_name}'"
        for idx in range(tpl_idx, min(tpl_idx + 150, len(lines) + 1)):
            line_str = lines[idx - 1]
            if field_target in line_str or field_target_alt in line_str:
                return [idx]
            # Stop if we hit the next template
            if idx > tpl_idx and ('"id":' in line_str or "'id':" in line_str):
                break
        return [tpl_idx]
    except Exception:
        return []


def extract_diagnostic_metadata(err: Union[str, DiagnosticError]) -> Dict[str, Any]:
    """Extract canonical diagnostic metadata from DiagnosticError or traditional formatted string."""
    if isinstance(err, DiagnosticError) and getattr(err, "rule_tag", None):
        return {
            "rule_tag": err.rule_tag,
            "competency": err.competency,
            "template": err.template,
            "field_name": err.field_name,
            "snippet": err.snippet,
            "cause": err.cause,
            "action": err.actions[0] if err.actions else "Corregir archivo",
            "lines": list(err.lines),
            "file_path": err.file_path,
        }

    err_str = str(err)
    m_rule = re.search(r"^\[-\]\s*\[([^\]]+)\]", err_str, re.MULTILINE)
    m_loc = re.search(r"UBICACI[ÓO]N:\s*Competencia:\s*'([^']*)',\s*Plantilla:\s*'([^']*)'.*?Campo:\s*'([^']*)'", err_str)
    m_lines = re.search(r"L[íi]neas?:\s*([0-9,\s]+)", err_str)
    m_cause = re.search(r"CAUSA:\s*(.+)", err_str)
    m_act = re.search(r"ACTION REQUIRED:\s*(.+)", err_str)
    m_snip = re.search(r"FRAGMENTO INFRACTOR:\s*(.+)", err_str)

    rule_tag = m_rule.group(1).strip() if m_rule else "GENERAL: VALIDATION_ERROR"
    comp = m_loc.group(1).strip() if m_loc else ""
    tpl = m_loc.group(2).strip() if m_loc else ""
    field_name = m_loc.group(3).strip() if m_loc else ""
    cause = m_cause.group(1).strip() if m_cause else err_str.splitlines()[0]
    action = m_act.group(1).strip() if m_act else "Corregir el archivo infractor."
    snippet = m_snip.group(1).strip() if m_snip else ""

    lines: List[int] = []
    if m_lines:
        for num in re.findall(r"\d+", m_lines.group(1)):
            lines.append(int(num))

    return {
        "rule_tag": rule_tag,
        "competency": comp,
        "template": tpl,
        "field_name": field_name,
        "snippet": snippet,
        "cause": cause,
        "action": action,
        "lines": lines,
        "file_path": None,
    }


_CONTROL_CHAR_TEXT_MAP = {
    "\x0c": r"\f",   # \frac, \forall -> 1 backslash in text (len 2: '\', 'f')
    "\x08": r"\b",   # \beta, \bar, \binom, \begin -> 1 backslash in text (len 2: '\', 'b')
    "\x07": r"\a",   # \alpha, \approx -> 1 backslash in text (len 2: '\', 'a')
    "\x0b": r"\v",   # \vec, \varepsilon -> 1 backslash in text (len 2: '\', 'v')
}

_CONTROL_CHAR_CODE_MAP = {
    "\x0c": r"\\f",   # In standard Python string literal, \\f escapes backslash for compiler
    "\x08": r"\\b",
    "\x07": r"\\a",
    "\x0b": r"\\v",
}

_CONTROL_CHAR_LATEX_MAP = _CONTROL_CHAR_TEXT_MAP


def _heal_code_control_chars(code_str: str) -> str:
    """Restores corrupted ASCII control characters in Python code strings.
    Distinguishes raw string literals (r'...') where single backslash is needed
    from standard string literals ('...') where double backslash is needed for AST.
    """
    if not any(c in code_str for c in _CONTROL_CHAR_TEXT_MAP):
        return code_str

    try:
        import io, tokenize
        tokens = list(tokenize.tokenize(io.BytesIO(code_str.encode("utf-8")).readline))
        new_tokens = []
        token_modified = False
        for tok in tokens:
            if tok.type == tokenize.STRING:
                val = tok.string
                if any(c in val for c in _CONTROL_CHAR_TEXT_MAP):
                    is_raw = val.startswith(("r", "R", "fr", "rf", "FR", "RF", "br", "rb", "BR", "RB"))
                    mapping = _CONTROL_CHAR_TEXT_MAP if is_raw else _CONTROL_CHAR_CODE_MAP
                    new_val = val
                    for ctrl, repl in mapping.items():
                        new_val = new_val.replace(ctrl, repl)
                    new_tokens.append(tokenize.TokenInfo(tok.type, new_val, tok.start, tok.end, tok.line))
                    token_modified = True
                    continue
            new_tokens.append(tok)
        if token_modified:
            res = tokenize.untokenize(new_tokens).decode("utf-8")
            ast.parse(res)
            return res
    except Exception:
        pass

    # Fallback to standard code mapping
    new_code = code_str
    for ctrl, repl in _CONTROL_CHAR_CODE_MAP.items():
        new_code = new_code.replace(ctrl, repl)
    try:
        ast.parse(new_code)
        return new_code
    except Exception:
        return code_str


def _extract_template_placeholders(text: str) -> Set[str]:
    """Extract template variable placeholders {var} or {var:spec} excluding LaTeX macro arguments like \\text{x}, \\begin{env}, \\dot{k}."""
    placeholders: Set[str] = set()
    for m in re.finditer(r"(?<!\{)\{([a-zA-Z_][a-zA-Z0-9_]*)(?::([^}]+))?\}(?!\})", text):
        var_name = m.group(1)
        fmt_spec = m.group(2)
        start = m.start()
        prefix = text[:start].rstrip()

        # If it has a format spec like {x:.2f}, it is unconditionally a Python template placeholder
        if fmt_spec:
            placeholders.add(var_name)
            continue

        # Check if preceded by a LaTeX command e.g. \text{var}, \sqrt{var}, \dot{var}, \begin{var}
        if re.search(r"\\[a-zA-Z]+(\[[^\]]*\])?\s*$", prefix):
            continue

        # Check if preceded by second argument of 2-arg macro e.g. \frac{a}{b}
        if prefix.endswith("}"):
            depth = 0
            idx = len(prefix) - 1
            while idx >= 0:
                if prefix[idx] == "}":
                    depth += 1
                elif prefix[idx] == "{":
                    depth -= 1
                    if depth == 0:
                        break
                idx -= 1
            if depth == 0 and idx >= 0:
                before_first_arg = prefix[:idx].rstrip()
                if re.search(r"\\(frac|dfrac|tfrac|cfrac|binom|dbinom|tbinom|overset|underset|stackrel)\s*$", before_first_arg):
                    continue

        # Check if subscript or superscript single letter without format spec: e.g. x_{i} or x^{k}
        if (prefix.endswith("_") or prefix.endswith("^")) and len(var_name) <= 2:
            continue

        placeholders.add(var_name)
    return placeholders


def auto_heal_template_data(
    data: Dict[str, Any],
    cta_comp: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    """Applies strictly mechanical, non-semantic auto-healing to a loaded template dict:
    1. Restores corrupted ASCII control chars in text (single backslash) and code (AST safe).
    2. Auto-exports local variables computed in generate(rng) into 'vars' dict
       when referenced as {var_name} in stem, stem_variants, hints, or solution.
    3. Populates missing error_rationale in multiple_select incorrect options from cta_comp distractors.
    """
    modified = False
    fixes: List[str] = []

    # Build distractor lookup from cta_comp / cta_data
    distractor_lookup: Dict[str, str] = {}
    if cta_comp and isinstance(cta_comp, dict):
        if isinstance(cta_comp.get("distractors"), list):
            for d in cta_comp["distractors"]:
                if isinstance(d, dict) and d.get("id"):
                    rationale = d.get("wrong_belief") or d.get("remediation_hint") or d.get("name") or ""
                    if rationale:
                        distractor_lookup[str(d["id"])] = str(rationale)
        elif isinstance(cta_comp.get("competencies"), list):
            target_cid = data.get("competency_id") if isinstance(data, dict) else None
            for c in cta_comp["competencies"]:
                if not target_cid or c.get("id") == target_cid:
                    for d in c.get("distractors", []):
                        if isinstance(d, dict) and d.get("id"):
                            rationale = d.get("wrong_belief") or d.get("remediation_hint") or d.get("name") or ""
                            if rationale:
                                distractor_lookup[str(d["id"])] = str(rationale)
        elif all(isinstance(v, dict) for v in cta_comp.values()):
            for did, d in cta_comp.items():
                if isinstance(d, dict):
                    rationale = d.get("wrong_belief") or d.get("remediation_hint") or d.get("name") or ""
                    if rationale:
                        distractor_lookup[str(did)] = str(rationale)

    templates_list: List[Dict[str, Any]] = []
    if isinstance(data, dict):
        if "templates" in data and isinstance(data["templates"], list):
            templates_list = data["templates"]
        elif "interaction_type" in data:
            templates_list = [data]
    elif isinstance(data, list):
        templates_list = data

    for tpl in templates_list:
        if not isinstance(tpl, dict):
            continue
        tid = tpl.get("id", "T-XX")

        # 1. Heal control characters in stem, solution, detailed_solution
        for s_field in ("stem", "solution", "detailed_solution"):
            val = tpl.get(s_field)
            if isinstance(val, str):
                new_val = val
                for ctrl, repl in _CONTROL_CHAR_TEXT_MAP.items():
                    if ctrl in new_val:
                        new_val = new_val.replace(ctrl, repl)
                if new_val != val:
                    tpl[s_field] = new_val
                    modified = True
                    fixes.append(f"{tid}.{s_field}: restored ASCII control char to LaTeX backslash")

        # Heal control characters in Python code fields
        for c_field in ("generate_py", "cross_check_py"):
            c_val = tpl.get(c_field)
            if isinstance(c_val, str) and any(ctrl in c_val for ctrl in _CONTROL_CHAR_TEXT_MAP):
                new_c_val = _heal_code_control_chars(c_val)
                if new_c_val != c_val:
                    tpl[c_field] = new_c_val
                    modified = True
                    fixes.append(f"{tid}.{c_field}: restored ASCII control char to LaTeX backslash in Python code")

        # Heal control characters in list fields: stem_variants, hints
        for list_field in ("stem_variants", "hints"):
            items = tpl.get(list_field)
            if isinstance(items, list):
                for i, item in enumerate(items):
                    if isinstance(item, str):
                        new_item = item
                        for ctrl, repl in _CONTROL_CHAR_TEXT_MAP.items():
                            if ctrl in new_item:
                                new_item = new_item.replace(ctrl, repl)
                        if new_item != item:
                            items[i] = new_item
                            modified = True
                            fixes.append(f"{tid}.{list_field}[{i}]: restored ASCII control char")

        # 2. Auto-export local variables in generate_py referenced as {var} in text fields
        gen_py = tpl.get("generate_py", "")
        if isinstance(gen_py, str) and "def generate" in gen_py:
            text_blob = " ".join(
                [str(tpl.get("stem", "")), str(tpl.get("solution", "")), str(tpl.get("detailed_solution", ""))]
                + [str(x) for x in tpl.get("stem_variants", [])]
                + [str(x) for x in tpl.get("hints", [])]
            )
            referenced_vars = _extract_template_placeholders(text_blob)
            if referenced_vars:
                try:
                    tree = ast.parse(gen_py)
                    assigned_locals: Set[str] = set()
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Assign):
                            for target in node.targets:
                                if isinstance(target, ast.Name):
                                    assigned_locals.add(target.id)
                                elif isinstance(target, ast.Tuple):
                                    for elt in target.elts:
                                        if isinstance(elt, ast.Name):
                                            assigned_locals.add(elt.id)
                        elif isinstance(node, ast.AnnAssign):
                            if isinstance(node.target, ast.Name):
                                assigned_locals.add(node.target.id)

                    missing_vars = (referenced_vars & assigned_locals) - {"rng"}
                    if missing_vars:
                        # Case 2A: 'vars': { ... } is returned as a dict literal in return statement
                        m_vars_dict = re.search(r"(['\"]vars['\"]\s*:\s*\{)([^}]*)(\})", gen_py)
                        if m_vars_dict:
                            vars_body = m_vars_dict.group(2)
                            existing_keys = set(re.findall(r"['\"]([a-zA-Z_][a-zA-Z0-9_]*)['\"]\s*:", vars_body))
                            missing_export = sorted(missing_vars - existing_keys)
                            if missing_export:
                                add_pairs = ", ".join(f"'{v}': {v}" for v in missing_export)
                                if vars_body.strip():
                                    sep = " " if vars_body.rstrip().endswith(",") else ", "
                                else:
                                    sep = ""
                                new_vars_segment = f"{m_vars_dict.group(1)}{vars_body}{sep}{add_pairs}{m_vars_dict.group(3)}"
                                new_gp = gen_py[:m_vars_dict.start()] + new_vars_segment + gen_py[m_vars_dict.end():]
                                try:
                                    ast.parse(new_gp)
                                    tpl["generate_py"] = new_gp
                                    gen_py = new_gp
                                    modified = True
                                    fixes.append(f"{tid}.generate_py: auto-exported {missing_export} into 'vars'")
                                except Exception:
                                    pass
                        else:
                            # Case 2B: 'vars': var_name where var_name is an assigned dict (e.g. vars_dict = {...})
                            m_vars_var = re.search(r"['\"]vars['\"]\s*:\s*([a-zA-Z_][a-zA-Z0-9_]*)", gen_py)
                            if m_vars_var:
                                vname = m_vars_var.group(1)
                                m_assign = re.search(rf"(\b{re.escape(vname)}\s*=\s*\{{)([^}}]*)(\}})", gen_py)
                                if m_assign:
                                    vbody = m_assign.group(2)
                                    existing_keys = set(re.findall(r"['\"]([a-zA-Z_][a-zA-Z0-9_]*)['\"]\s*:", vbody))
                                    missing_export = sorted(missing_vars - existing_keys)
                                    if missing_export:
                                        add_pairs = ", ".join(f"'{v}': {v}" for v in missing_export)
                                        sep = " " if vbody.rstrip().endswith(",") else (", " if vbody.strip() else "")
                                        new_vseg = f"{m_assign.group(1)}{vbody}{sep}{add_pairs}{m_assign.group(3)}"
                                        new_gp = gen_py[:m_assign.start()] + new_vseg + gen_py[m_assign.end():]
                                        try:
                                            ast.parse(new_gp)
                                            tpl["generate_py"] = new_gp
                                            gen_py = new_gp
                                            modified = True
                                            fixes.append(f"{tid}.generate_py: auto-exported {missing_export} into '{vname}'")
                                        except Exception:
                                            pass
                            else:
                                # Case 2C: 'vars' key is completely missing from return { ... }
                                m_ret = re.search(r"(\breturn\s*\{)(.*)", gen_py, re.DOTALL)
                                if m_ret:
                                    missing_export = sorted(missing_vars)
                                    if missing_export:
                                        add_pairs = ", ".join(f"'{v}': {v}" for v in missing_export)
                                        inject_str = f"\n        'vars': {{{add_pairs}}},"
                                        new_gp = gen_py[:m_ret.start(1) + len(m_ret.group(1))] + inject_str + gen_py[m_ret.start(1) + len(m_ret.group(1)):]
                                        try:
                                            ast.parse(new_gp)
                                            tpl["generate_py"] = new_gp
                                            gen_py = new_gp
                                            modified = True
                                            fixes.append(f"{tid}.generate_py: injected missing 'vars' dict with {missing_export}")
                                        except Exception:
                                            pass
                except Exception:
                    pass

        # 3. Auto-fill missing error_rationale in multiple_select from CTA distractor lookup
        if tpl.get("interaction_type") == "multiple_select" and distractor_lookup and isinstance(tpl.get("generate_py"), str):
            gp = tpl["generate_py"]
            for did, rat in distractor_lookup.items():
                safe_rat = rat.replace("\\", "\\\\").replace("'", "\\'")

                # Pattern 1: distractor_id followed by error_rationale: None or "" or ''
                p1 = rf"(['\"]distractor_id['\"]\s*:\s*['\"]{re.escape(did)}['\"]\s*,\s*['\"]error_rationale['\"]\s*:\s*)(None|['\"]['\"])"
                new_gp = re.sub(p1, rf"\1'{safe_rat}'", gp)

                # Pattern 2: error_rationale: None or "" or '' followed by distractor_id
                p2 = rf"(['\"]error_rationale['\"]\s*:\s*)(None|['\"]['\"])(\s*,\s*['\"]distractor_id['\"]\s*:\s*['\"]{re.escape(did)}['\"])"
                new_gp = re.sub(p2, rf"\1'{safe_rat}'\3", new_gp)

                # Pattern 3: option dict contains distractor_id, but error_rationale is missing entirely
                def _inject_missing_rat(m: re.Match) -> str:
                    d_str = m.group(0)
                    if "error_rationale" not in d_str:
                        return re.sub(
                            rf"(['\"]distractor_id['\"]\s*:\s*['\"]{re.escape(did)}['\"])",
                            rf"\1, 'error_rationale': '{safe_rat}'",
                            d_str,
                            count=1,
                        )
                    return d_str

                new_gp = re.sub(
                    rf"\{{[^{{}}]*['\"]distractor_id['\"]\s*:\s*['\"]{re.escape(did)}['\"][^{{}}]*\}}",
                    _inject_missing_rat,
                    new_gp,
                )

                if new_gp != gp:
                    try:
                        ast.parse(new_gp)
                        gp = new_gp
                        modified = True
                        fixes.append(f"{tid}.generate_py: auto-populated error_rationale for {did} from CTA")
                    except Exception:
                        pass
            tpl["generate_py"] = gp

    return modified, fixes


def auto_heal_template_file(
    tpl_path: Path,
    cta_comp: Optional[Dict[str, Any]] = None,
    cta_distractors_map: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    """Applies strictly mechanical, non-semantic auto-healing in-place to a template JSON file.

    1. Restores corrupted ASCII control chars (\\x0c -> \\\\f, \\x08 -> \\\\b, etc.)
    2. Auto-exports local variables computed in generate(rng) to 'vars' dict when used in {placeholders}
    3. Auto-fills missing error_rationale in multiple_select options from CTA distractor lookup

    Returns (was_modified, list_of_applied_fixes).
    """
    p = Path(tpl_path)
    if not p.is_file():
        return False, []

    try:
        content = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return False, []

    comp_context = cta_comp if cta_comp is not None else cta_distractors_map
    modified, fixes = auto_heal_template_data(content, cta_comp=comp_context)
    if modified:
        p.write_text(json.dumps(content, indent=2, ensure_ascii=False), encoding="utf-8")
    return modified, fixes


def render_compact_aggregated_errors(
    errors: List[Union[str, DiagnosticError]],
    targets: Optional[List[Path]] = None,
    max_output_lines: int = 35,
) -> str:
    """Render canonical LLM-optimized single-line aggregated error output grouped by rule."""
    if not errors:
        return ""

    has_cb = any("CIRCUIT BREAKER" in str(e) for e in errors)
    header = (
        f"FAIL: CIRCUIT BREAKER TRIPPED ({len(errors)} errores en templates):"
        if has_cb
        else f"FAIL: {len(errors)} validaciones fallidas en templates:"
    )

    records = []
    for err in errors:
        rec = extract_diagnostic_metadata(err)
        fpath = rec["file_path"]
        if not fpath and rec["competency"]:
            cid = rec["competency"]
            cand1 = Path("work/templates") / f"{cid}.json"
            cand2 = Path("templates") / f"{cid}.json"
            if cand1.is_file():
                fpath = str(cand1.as_posix())
            elif cand2.is_file():
                fpath = str(cand2.as_posix())
            elif targets:
                for t in targets:
                    if t.stem == cid or cid in t.stem:
                        fpath = str(t.as_posix())
                        break
            if not fpath:
                fpath = f"work/templates/{cid}.json"
        elif not fpath and targets:
            fpath = str(targets[0].as_posix())
        else:
            fpath = fpath or "work/templates"

        rec["file_path"] = fpath

        # Locate lines dynamically if not present
        if not rec["lines"] and rec["file_path"]:
            p = Path(rec["file_path"])
            if p.is_file():
                search_term = rec["snippet"] or rec["template"]
                if search_term and len(search_term) >= 3:
                    rec["lines"] = find_lines_in_file(p, search_term)
                if not rec["lines"] and rec.get("template"):
                    rec["lines"] = find_template_field_line(p, rec["template"], rec.get("field_name"))

        records.append(rec)

    # Group by rule_tag -> file_path -> (cause, action) -> lines
    grouped: Dict[str, Dict[str, Dict[Tuple[str, str], List[int]]]] = defaultdict(
        lambda: defaultdict(lambda: defaultdict(list))
    )

    for r in records:
        rtag = r["rule_tag"]
        fp = r["file_path"]
        scause = r["cause"]
        if len(scause) > 95:
            scause = scause[:92] + "..."
        sact = r["action"]
        if len(sact) > 85:
            sact = sact[:82] + "..."

        grouped[rtag][fp][(scause, sact)].extend(r["lines"])

    out_lines = [header, ""]

    for rtag, file_map in grouped.items():
        m_rid = re.match(r"^([A-Za-z0-9_-]+)", rtag)
        short_rid = m_rid.group(1) if m_rid else rtag
        out_lines.append(f"[-] [{rtag}]")

        for fp, err_map in file_map.items():
            for (cause, act), l_list in err_map.items():
                uniq_lines = sorted(set(l_list))
                if uniq_lines:
                    if len(uniq_lines) > 5:
                        lines_str = f":L{uniq_lines[0]}-{uniq_lines[-1]} ({len(uniq_lines)} líneas)"
                    else:
                        lines_str = f":L{','.join(str(x) for x in uniq_lines)}"
                else:
                    lines_str = ""

                # Canonical single-line output containing: RULE, FILE, LINES, CAUSE, ACTION
                out_lines.append(f"  • [{short_rid}] {fp}{lines_str} -> Causa: {cause} | Acción: {act}")
        out_lines.append("")

    return "\n".join(out_lines).strip()


def get_canonical_invariant_key(inv_err: str) -> str:
    """Derive canonical grouping key for invariant errors to aggregate dynamic values across seeds."""
    clean = inv_err.strip()
    if "Distractor identical to correct answer" in clean:
        return "Distractor identical to correct answer"
    if "Duplicate option content detected" in clean:
        return "Duplicate option content detected"
    if "Length anti-giveaway violation" in clean:
        if "too short" in clean:
            return "Length anti-giveaway: correct option too short"
        return "Length anti-giveaway: correct option too long"
    if "leaked verbatim in stem text" in clean:
        return "Correct answer leaked verbatim in stem text"
    if "leaked verbatim in first hint" in clean:
        return "Correct answer leaked verbatim in first hint"
    if "Synthetic boilerplate distractor" in clean:
        return "Synthetic boilerplate distractor pattern detected"
    if "Scaffolding answer leak" in clean:
        return "Scaffolding answer leak detected in hint"
    m_var = re.search(r"Unsubstituted template variable '\{([^}]+)\}' detected in (.+)", clean)
    if m_var:
        return f"Unsubstituted variable '{{{m_var.group(1)}}}' in {m_var.group(2).rstrip('.')}"
    m_math = re.search(r"(Unbalanced curly braces in LaTeX math expression in [^:]+)", clean)
    if m_math:
        return m_math.group(1)
    norm = re.sub(r"'[^']*'", "'...'", clean)
    norm = re.sub(r"\b\d+\b", "N", norm)
    return norm


def format_invariant_error_diagnostic(
    cid: str,
    tpl_id: str,
    q_id: Union[str, List[str]],
    inv_err: str,
    q_obj: Optional[Dict[str, Any]] = None,
) -> str:
    """Formats an error from check_instance_invariants into the enriched diagnostic structure."""
    inv_clean = inv_err.strip()

    # Case A0: Unescaped LaTeX math command
    if "Unescaped LaTeX math command" in inv_clean:
        m_cmd = re.search(r"Unescaped LaTeX math command '([^']+)' detected in (.+?)\.", inv_clean)
        snippet = m_cmd.group(1) if m_cmd else "cmd{var}"
        field_name = m_cmd.group(2).rstrip(".") if m_cmd else "text"
        cause = f"Comando matemático LaTeX '{snippet}' sin barra invertida '\\' o sin delimitadores '$...$' detectado en '{field_name}'."
        actions = [
            f"Reemplazar por notación KaTeX válida delimitada por '$' (ej. '$\\{snippet}$').",
            "PROHIBIDO declarar variables matemáticas en el diccionario 'vars' retornado por generate_py.",
            "Asegurar que todas las expresiones matemáticas estén estrictamente delimitadas por '$...$'.",
        ]
        return format_diagnostic_error("R-20: SINTAXIS / LLAVES", cid, tpl_id, q_id, field_name, snippet, cause, actions)

    # Case A: Unsubstituted template variable '{var}'
    m_var = re.search(r"Unsubstituted template variable '\{([^}]+)\}' detected in (.+)", inv_clean)
    if m_var:
        var_name = m_var.group(1)
        field_name = m_var.group(2).rstrip(".")
        snippet = f"{{{var_name}}}"
        is_distractor_context = "option" in field_name.lower() or "rationale" in field_name.lower()
        if is_distractor_context:
            cause = (
                f"Subcadena '{{{var_name}}}' detectada dentro del texto del distractor/opción en '{field_name}'. "
                f"NO corresponde a un parámetro dinámico de generate_py, sino a sintaxis matemática o texto de distractor."
            )
            actions = [
                f"Si '{{{var_name}}}' es parte de notación matemática, delimítela en '$...$' (ej. '$\\dot{{{var_name}}}$' o '$\\bar{{{var_name}}}$') en el template.",
                f"PROHIBIDO declarar '{var_name}' en el diccionario 'vars' retornado por generate_py (provoca aberraciones sintácticas en cascada).",
                f"Quitar las llaves '{{}}' si es texto plano literal no paramétrico.",
            ]
        else:
            cause = f"Llaves '{{{var_name}}}' no declaradas en el diccionario 'vars' generado en generate_py o no sustituidas en el campo '{field_name}'."
            actions = [
                f"Usar '${var_name}$' si se trata de notación matemática en LaTeX.",
                "Quitar las llaves '{}' si es texto plano literal no paramétrico.",
                f"Declarar '{var_name}' en el diccionario 'vars' retornado por generate_py (SOLO si es un parámetro dinámico del stem o hints, NUNCA para distractores).",
            ]
        return format_diagnostic_error("R-20: SINTAXIS / LLAVES", cid, tpl_id, q_id, field_name, snippet, cause, actions)

    # Case B: Triple dollar delimiter '$$$'
    if "$$$" in inv_clean:
        m_ctx = re.search(r"detected in (.+)", inv_clean)
        field_name = m_ctx.group(1).rstrip(".") if m_ctx else "stem / hint / text"
        snippet = "$$$"
        cause = f"Delimitador matemático triple '$$$' inválido detectado en '{field_name}'."
        actions = [
            "Reemplazar '$$$' por '$$' si se trata de un bloque matemático en display mode.",
            "Reemplazar '$$$' por '$' si es matemática inline.",
            "Asegurar que los delimitadores de apertura y cierre coincidan sin signos de dólar redundantes.",
        ]
        return format_diagnostic_error("R-20: SINTAXIS / LLAVES", cid, tpl_id, q_id, field_name, snippet, cause, actions)

    # Case C: Unbalanced display math delimiter '$$'
    if "Unbalanced display math delimiter '$$'" in inv_clean:
        m_ctx = re.search(r"in (.+)", inv_clean)
        field_name = m_ctx.group(1).rstrip(".") if m_ctx else "stem / hint / text"
        snippet = "$$"
        cause = f"Delimitadores '$$' de display math no balanceados en '{field_name}' (número impar de '$$')."
        actions = [
            "Asegurarse de que cada '$$' de apertura tenga un '$$' de cierre.",
            "No mezclar '$$' con '$' en la misma expresión matemática.",
            "Escapar cualquier símbolo de dólar literal como '\\$'.",
        ]
        return format_diagnostic_error("R-20: SINTAXIS / LLAVES", cid, tpl_id, q_id, field_name, snippet, cause, actions)

    # Case D: Unbalanced inline math delimiter '$'
    if "Unbalanced inline math delimiter '$'" in inv_clean:
        m_ctx = re.search(r"in (.+)", inv_clean)
        field_name = m_ctx.group(1).rstrip(".") if m_ctx else "stem / hint / text"
        snippet = "$"
        cause = f"Delimitadores '$' de matemática inline no balanceados en '{field_name}' (número impar de '$')."
        actions = [
            "Verificar que cada '$' de apertura cuente con su correspondiente '$' de cierre.",
            "Escapar cualquier símbolo de dólar literal o de moneda como '\\$'.",
            "Evitar saltos de línea o texto no matemático dentro del bloque '$...$'.",
        ]
        return format_diagnostic_error("R-20: SINTAXIS / LLAVES", cid, tpl_id, q_id, field_name, snippet, cause, actions)

    # Case E: Residual double curly braces '{{' or '}}'
    if "Residual double curly braces" in inv_clean:
        m_ctx = re.search(r"detected in (.+)", inv_clean)
        field_name = m_ctx.group(1).rstrip(".") if m_ctx else "stem / hint / text"
        snippet = "{{ o }}"
        cause = f"Llaves dobles residuales '{{' o '}}' provenientes de formato o f-string de Python en '{field_name}'."
        actions = [
            "Usar llaves simples '{...}' para grupos en LaTeX en lugar de llaves dobles '{{...}}'.",
            "Revisar el escape de llaves en f-strings dentro de generate_py.",
            "Utilizar raw strings r'...' para expresiones KaTeX.",
        ]
        return format_diagnostic_error("R-20: SINTAXIS / LLAVES", cid, tpl_id, q_id, field_name, snippet, cause, actions)

    # Case F: Unbalanced curly braces in LaTeX math expression
    if "Unbalanced curly braces in LaTeX math expression" in inv_clean:
        m_ctx = re.search(r"in ([^:]+):\s*'(.*)'", inv_clean)
        field_name = m_ctx.group(1).strip() if m_ctx else "math expression"
        snippet = m_ctx.group(2) if m_ctx else "{ o }"
        cause = f"Llaves curvas '{{' y '}}' desbalanceadas dentro de la fórmula LaTeX en '{field_name}': '{snippet}'."
        actions = [
            "Contar y balancear las llaves '{' y '}' en la expresión LaTeX.",
            "Si se usaron llaves literales escapadas '\\{', asegurar que la barra invertida esté presente.",
            "Revisar macros de LaTeX con múltiples argumentos como \\frac{a}{b} donde falte una llave de cierre.",
        ]
        return format_diagnostic_error("R-20: SINTAXIS / LLAVES", cid, tpl_id, q_id, field_name, snippet, cause, actions)

    # Case F2: Unclosed nested LaTeX macro or accent
    if "Unclosed nested macro brace detected" in inv_clean or "nested macro" in inv_clean:
        m_ctx = re.search(r"in ([^:]+):", inv_clean)
        field_name = m_ctx.group(1).strip() if m_ctx else "math expression"
        return format_diagnostic_error(
            "R-20: SINTAXIS / LLAVES", cid, tpl_id, q_id, field_name, inv_clean,
            f"Acento o macro anidado de LaTeX sin cerrar correctamente en '{field_name}'.",
            [
                "Asegurar que macros anidados como \\hat{\\boldsymbol{\\beta}} tengan ambas llaves de cierre '}}'.",
                "Revisar expresiones matemáticas con acentos combinados con estilos vectoriales o matriciales.",
                "Balancear todas las llaves en la fórmula.",
            ],
        )

    # Case F3: Macro arity / unclosed argument
    if "requires 2 arguments" in inv_clean or "unclosed first argument" in inv_clean or "unclosed second argument" in inv_clean or "missing argument brackets" in inv_clean:
        m_ctx = re.search(r"in ([^.]+)", inv_clean)
        field_name = m_ctx.group(1).strip() if m_ctx else "math expression"
        return format_diagnostic_error(
            "R-20: SINTAXIS / LLAVES", cid, tpl_id, q_id, field_name, inv_clean,
            f"Macro de LaTeX (como \\frac, \\binom, \\overset) con aridad incorrecta o argumento incompleto en '{field_name}'.",
            [
                "Comprobar que \\frac posea tanto numerador como denominador: \\frac{num}{den}.",
                "Cerrar adecuadamente cada bloque de llaves '{...}'.",
                "Evitar macros con argumentos incompletos antes del cierre del delimitador '$'.",
            ],
        )

    # Case F4: Unclosed or mismatched LaTeX environment
    if "LaTeX environment" in inv_clean:
        m_ctx = re.search(r"in ([^.]+)", inv_clean)
        field_name = m_ctx.group(1).strip() if m_ctx else "math expression"
        return format_diagnostic_error(
            "R-20: SINTAXIS / LLAVES", cid, tpl_id, q_id, field_name, inv_clean,
            f"Entorno LaTeX sin cerrar o con cierre discordante en '{field_name}'.",
            [
                "Asegurar que cada \\begin{env} tenga su correspondiente \\end{env}.",
                "Verificar entornos matriciales o de casos como pmatrix, bmatrix, cases, aligned.",
                "Comprobar que no haya errores tipográficos en el nombre del entorno.",
            ],
        )

    # Case F5: Unclosed or unmatched scalable delimiter
    if "scalable delimiter" in inv_clean:
        m_ctx = re.search(r"in ([^.]+)", inv_clean)
        field_name = m_ctx.group(1).strip() if m_ctx else "math expression"
        return format_diagnostic_error(
            "R-20: SINTAXIS / LLAVES", cid, tpl_id, q_id, field_name, inv_clean,
            f"Delimitador escalable \\left o \\right sin emparejar en '{field_name}'.",
            [
                "Emparejar cada \\left( con \\right), \\left[ con \\right], \\left\\{ con \\right\\}.",
                "Si se requiere un delimitador invisible, usar \\left. o \\right..",
                "Verificar la simetría de paréntesis y corchetes en las fórmulas matemáticas.",
            ],
        )

    # Case G: Distractor identical to correct answer (TPL-D4)
    if "Distractor identical to correct answer" in inv_clean:
        m_d = re.search(r"Distractor identical to correct answer:\s*'(.*)'", inv_clean)
        snippet = m_d.group(1) if m_d else inv_clean
        cause = f"TPL-D4 violation in '{tpl_id}': distractor matches correct answer '{snippet}' (invariant violation). Un distractor generado en generate_py es idéntico a la respuesta correcta."
        actions = [
            "Verificar en generate_py que los distractores nunca tomen el valor de la clave correcta.",
            "Añadir una guarda en generate_py que desplace o regenere el distractor si colisiona con 'correct'.",
            "Comprobar casos particulares donde parámetros aleatorios anulen la diferencia.",
        ]
        return format_diagnostic_error("TPL-D4: TPL-D4 violation: DISTRACTOR IDÉNTICO A RESPUESTA CORRECTA", cid, tpl_id, q_id, "options", snippet, cause, actions)

    # Case H: Length anti-giveaway violation (R-15)
    if "Length anti-giveaway violation" in inv_clean:
        cause = "La longitud de la respuesta correcta difiere significativamente del rango de los distractores (fuera de 0.80x - 1.20x)."
        actions = [
            "Calibrar la longitud de la respuesta correcta o de los distractores para que tengan una extensión homogénea.",
            "Homogeneizar el nivel de detalle y formato matemático entre todas las opciones.",
            "Asegurar que 0.80 * min(len(D)) <= len(correct) <= 1.20 * max(len(D)).",
        ]
        return format_diagnostic_error("R-15: EQUILIBRIO DE LONGITUD", cid, tpl_id, q_id, "options", inv_clean, cause, actions)

    # Case I: Answer leak (R-19)
    if "leaked verbatim in" in inv_clean:
        cause = "El valor o texto de la respuesta correcta aparece textualmente en el stem o en la primera pista, revelando la clave."
        actions = [
            "Remover la mención textual de la respuesta del enunciado de la pregunta o de la primera pista.",
            "Reformular la primera pista para que oriente sobre el método conceptual sin dar el resultado numérico/algebraico.",
            "Verificar que la consigna plantee el problema requiriendo el cálculo en lugar de enunciar la solución.",
        ]
        return format_diagnostic_error("R-19: FUGA DE RESPUESTA", cid, tpl_id, q_id, "stem / hints[0]", inv_clean, cause, actions)

    # Case J: Missing error_rationale
    if "must possess a non-empty 'error_rationale'" in inv_clean:
        is_ms = "MS option" in inv_clean
        rule_tag = "R-22: RATIONALE EN MULTIPLE_SELECT" if is_ms else "R-17: RATIONALE FALTANTE EN DISTRACTOR"
        m_opt = re.search(r"option\s+(\d+)", inv_clean, re.IGNORECASE)
        opt_idx = m_opt.group(1) if m_opt else "X"
        field_name = f"options[{opt_idx}].error_rationale"
        cause = f"La opción distractora {opt_idx} con is_correct=False carece de un 'error_rationale' explicativo."
        actions = [
            "Agregar una explicación diagnóstica en 'error_rationale' para cada opción con is_correct=False.",
            "Describir la falacia conceptual o error procedimental que lleva a seleccionar dicha opción.",
            "Asegurar que el texto de rationale no sea una cadena vacía ni un placeholder genérico.",
        ]
        return format_diagnostic_error(rule_tag, cid, tpl_id, q_id, field_name, "(vacío o ausente)", cause, actions)

    # Case K: Duplicate options
    if "Duplicate option content detected" in inv_clean:
        m_opt = re.search(r"detected(?:\s+in\s+MS)?:\s*'(.*)'", inv_clean)
        snippet = m_opt.group(1) if m_opt else inv_clean
        cause = f"Dos o más opciones tienen contenido idéntico ('{snippet}')."
        actions = [
            "Garantizar que todos los distractores generados en generate_py sean disjuntos y únicos.",
            "Agregar una comprobación en generate_py que descarte o regenere opciones repetidas.",
            "Variar las fórmulas de perturbación para producir valores distintos.",
        ]
        return format_diagnostic_error("TPL-D4: OPCIONES DUPLICADAS", cid, tpl_id, q_id, "options", snippet, cause, actions)

    # Case L: Synthetic boilerplate distractor pattern
    if "Synthetic boilerplate distractor" in inv_clean:
        m_s = re.search(r"pattern detected:\s*(.*)", inv_clean)
        snippet = m_s.group(1) if m_s else inv_clean
        cause = "Opciones distractoras generadas mediante plantilla sintética repetitiva o inversión simétrica trivial ('converge' vs 'diverge')."
        actions = [
            "Reemplazar distractores boilerplate por modelos de error y confusiones conceptuales reales.",
            "Diversificar la redacción y argumentos analíticos de cada opción distractora.",
            "Evitar variaciones triviales donde solo se cambie un término opuesto o un parámetro numérico.",
        ]
        return format_diagnostic_error("R-18: DISTRACTORES BOILERPLATE SINTÉTICOS", cid, tpl_id, q_id, "options", snippet, cause, actions)

    # Case M: Scaffolding answer leak in hints
    if "Scaffolding answer leak" in inv_clean:
        m_s = re.search(r"hint\s+\d+:\s*(.*)", inv_clean)
        snippet = m_s.group(1) if m_s else inv_clean
        cause = "La pista (scaffolding) proporciona una regla mecánica de descarte que delata directamente la respuesta correcta."
        actions = [
            "Reescribir la pista para proporcionar guía pedagógica sin dar instrucciones explícitas de descarte mecánico.",
            "Fomentar la deducción del estudiante a partir de ecuaciones y principios teóricos.",
            "Eliminar frases como 'Descarte las respuestas...' o 'Elimine opciones...' del texto de hints.",
        ]
        return format_diagnostic_error("R-19: FUGA DE RESPUESTA EN ANDAMIAJE", cid, tpl_id, q_id, "hints", snippet, cause, actions)

    # Fallback Invariant
    return format_diagnostic_error(
        rule_tag="INVARIANT: invariant violation",
        competency=cid,
        template=tpl_id,
        item_id=q_id,
        field_name="instance",
        snippet=inv_clean,
        cause=f"Template '{tpl_id}' invariant violation ({q_id}): {inv_clean}",
        actions=[
            "Revisar la salida de generate_py para cumplir con los requerimientos estructurales del reactivo.",
            "Asegurar que todos los campos requeridos estén presentes y sean del tipo esperado.",
            "Verificar que el reactivo cumpla con la especificación de interaction_type.",
        ],
    )


def format_parity_error(
    cid: str,
    err: Any,
    questions_by_id: Dict[str, Dict[str, Any]],
    item_ids: Optional[Union[str, List[str]]] = None,
) -> str:
    """Formats a ValidationError from production parity check with prescriptive diagnosis."""
    rule_id = getattr(err, "rule_id", "PARITY")
    msg = getattr(err, "message", str(err))
    if item_ids is not None:
        item_id = item_ids
        rep_id = item_ids[0] if isinstance(item_ids, list) and item_ids else (item_ids if isinstance(item_ids, str) else "UNKNOWN")
    else:
        item_id = getattr(err, "item_id", None) or "UNKNOWN"
        rep_id = item_id

    q = questions_by_id.get(rep_id, {})
    tpl_id = q.get("template_id") or "UNKNOWN"

    # Rule R-20
    if rule_id == "R-20":
        m_field = re.search(r"in\s+([a-zA-Z0-9_.\[\]]+):", msg)
        field_name = m_field.group(1) if m_field else "stem / options / text"

        if "Unreplaced template variable" in msg:
            m_s = re.search(r"Unreplaced template variable\(s\) found:\s*(.*)", msg)
            snippet = m_s.group(1) if m_s else "{var}"
            is_distractor_context = "option" in field_name.lower() or "rationale" in field_name.lower()
            clean_var = snippet.replace('{','').replace('}','')
            if is_distractor_context:
                cause = (
                    f"Subcadena '{snippet}' detectada dentro del texto del distractor/opción en '{field_name}'. "
                    f"NO corresponde a un parámetro dinámico de generate_py."
                )
                actions = [
                    f"Si '{snippet}' es notación matemática, delimítela en '$...$' (ej. '$\\dot{{{clean_var}}}$' o '$\\bar{{{clean_var}}}$') en el template.",
                    f"PROHIBIDO declarar '{clean_var}' en el diccionario 'vars' retornado por generate_py (provoca aberraciones sintácticas en cascada).",
                    "Quitar las llaves '{}' si es texto plano literal no paramétrico.",
                ]
            else:
                cause = f"Llaves '{snippet}' no declaradas en el diccionario 'vars' retornado por generate_py o no reemplazadas en '{field_name}'."
                actions = [
                    f"Usar '${clean_var}$' si se trata de notación matemática en LaTeX.",
                    "Quitar las llaves '{}' si es texto plano literal no paramétrico.",
                    f"Agregar la clave sin llaves al diccionario 'vars' retornado por generate_py (SOLO si es parámetro dinámico del stem/hints, NUNCA para distractores).",
                ]
            return format_diagnostic_error("R-20: SINTAXIS / LLAVES", cid, tpl_id, item_id, field_name, snippet, cause, actions)

        if "Unbalanced display math delimiters '$$'" in msg:
            return format_diagnostic_error(
                "R-20: SINTAXIS / LLAVES", cid, tpl_id, item_id, field_name, "$$",
                f"Delimitadores '$$' de display math no balanceados en '{field_name}' (número impar de '$$').",
                [
                    "Asegurarse de que cada '$$' de apertura tenga un '$$' de cierre.",
                    "No mezclar '$$' con '$' en la misma expresión.",
                    "Escapar cualquier símbolo de dólar literal como '\\$'.",
                ]
            )

        if "Unbalanced inline math delimiters '$'" in msg:
            return format_diagnostic_error(
                "R-20: SINTAXIS / LLAVES", cid, tpl_id, item_id, field_name, "$",
                f"Delimitadores '$' de matemática en línea no balanceados en '{field_name}' (número impar de '$').",
                [
                    "Verificar que cada '$' de apertura cuente con su correspondiente '$' de cierre.",
                    "Escapar cualquier símbolo de dólar literal como '\\$'.",
                    "Comprobar que no haya saltos de línea dentro del bloque '$...$'.",
                ]
            )

        if "Forbidden triple math delimiter '$$$'" in msg:
            return format_diagnostic_error(
                "R-20: SINTAXIS / LLAVES", cid, tpl_id, item_id, field_name, "$$$",
                f"Delimitador matemático triple '$$$' inválido detectado en '{field_name}'.",
                [
                    "Reemplazar '$$$' por '$$' si es bloque matemático en display mode.",
                    "Reemplazar '$$$' por '$' si es matemática inline.",
                    "Asegurar que los delimitadores de apertura y cierre coincidan.",
                ]
            )

        if "Residual double braces" in msg:
            return format_diagnostic_error(
                "R-20: SINTAXIS / LLAVES", cid, tpl_id, item_id, field_name, "{{ o }}",
                f"Llaves dobles residuales '{{' o '}}' provenientes de f-strings en Python dentro de '{field_name}'.",
                [
                    "Usar llaves simples '{...}' para grupos en LaTeX en lugar de llaves dobles '{{...}}'.",
                    "Revisar el escape de llaves en f-strings dentro de generate_py.",
                    "Utilizar raw strings r'...' para expresiones KaTeX.",
                ]
            )

        if "Unbalanced curly braces in LaTeX math block" in msg:
            m_s = re.search(r"LaTeX math block:\s*'(.*)'", msg)
            snippet = m_s.group(1) if m_s else "{ o }"
            return format_diagnostic_error(
                "R-20: SINTAXIS / LLAVES", cid, tpl_id, item_id, field_name, snippet,
                f"Llaves curvas '{{' y '}}' desbalanceadas dentro de la fórmula LaTeX en '{field_name}': '{snippet}'.",
                [
                    "Contar y balancear las llaves '{' y '}' en la expresión LaTeX.",
                    "Asegurar que llaves literales estén escapadas como '\\{'.",
                    "Revisar macros de LaTeX como \\frac{a}{b} donde falte una llave de cierre.",
                ]
            )

        if "Leaked raw code variable identifier" in msg:
            m_s = re.search(r"identifier\(s\) found:\s*(.*)", msg)
            snippet = m_s.group(1) if m_s else "identificador de código"
            return format_diagnostic_error(
                "R-20: SINTAXIS / LLAVES", cid, tpl_id, item_id, field_name, snippet,
                f"Identificador interno de código filtrado al texto del reactivo ({snippet}).",
                [
                    "Eliminar o formatear las variables internas de código antes de insertarlas en el texto.",
                    "Reemplazar identificadores crudos (_val, _num, _str) por su valor formateado o símbolo matemático.",
                    "Verificar que el texto dirigido al estudiante sea completamente natural y pedagógico.",
                ]
            )

        return format_diagnostic_error(
            "R-20: SINTAXIS / LLAVES", cid, tpl_id, item_id, field_name, msg,
            f"Error de sintaxis KaTeX o delimitadores en '{field_name}'.",
            [
                "Revisar la sintaxis de KaTeX y los delimitadores '$' y '$$'.",
                "Asegurar que todas las llaves '{' y '}' estén balanceadas.",
                "Verificar que no queden placeholders sin sustituir.",
            ]
        )

    # Rule R-18
    if rule_id == "R-18":
        m_field = re.search(r"Option '([^']+)'", msg)
        opt_id = m_field.group(1) if m_field else "option"
        field_name = f"options[{opt_id}].content"
        m_s = re.search(r"visible content:\s*'(.*)'", msg)
        snippet = m_s.group(1) if m_s else msg
        cause = "Uso de términos metalingüísticos o autocríticos ('confundiendo', 'asumiendo erróneamente', etc.) en el texto visible de la opción que revelan al estudiante que es un distractor."
        actions = [
            "Reescribir el contenido de la opción como una afirmación objetiva o resultado alternativo plausible sin juzgar su veracidad en el texto visible.",
            "Mover la justificación del error ('confundiendo...', 'asumiendo erróneamente...') exclusivamente al campo 'error_rationale'.",
            "Asegurar que todas las opciones mantengan una apariencia neutra y verosímil sin dar pistas psicométricas.",
        ]
        return format_diagnostic_error("R-18: META-INFORMACIÓN / GIVEAWAY", cid, tpl_id, item_id, field_name, snippet, cause, actions)

    # Rule R-19
    if rule_id == "R-19":
        field_name = "stem"
        m_s = re.search(r"answer '([^']+)' leaked", msg)
        snippet = m_s.group(1) if m_s else msg
        cause = "El valor o clave de la respuesta correcta aparece textualmente dentro del stem del reactivo (fuga de respuesta), o hay sustitución que corrompió un operador (ej. \\dot<número>)."
        actions = [
            "Remover el valor o expresión de respuesta del enunciado (stem) reemplazándolo por una consigna neutra o línea de completación.",
            "Asegurar que las variables de LaTeX no sustituyan números directamente dentro de macros sin llaves.",
            "Verificar que la consigna plantee el problema requiriendo el cálculo en lugar de mostrar la solución.",
        ]
        return format_diagnostic_error("R-19: FUGA DE RESPUESTA / SINTAXIS", cid, tpl_id, item_id, field_name, snippet, cause, actions)

    # Rule R-22
    if rule_id == "R-22":
        m_field = re.search(r"Option '([^']+)'", msg)
        opt_id = m_field.group(1) if m_field else "option"
        field_name = f"options[{opt_id}].error_rationale"
        cause = "Opción incorrecta (is_correct=False) en ítem de selección múltiple (multiple_select) carece de 'error_rationale' diagnóstico formativo."
        actions = [
            "Agregar una explicación diagnóstica en 'error_rationale' para cada opción con is_correct=False.",
            "Explicar la falacia conceptual o el cálculo incorrecto que conduce a seleccionar dicha opción.",
            "Asegurarse de que el texto de rationale no esté vacío ni sea un placeholder genérico.",
        ]
        return format_diagnostic_error("R-22: RATIONALE EN MULTIPLE_SELECT", cid, tpl_id, item_id, field_name, "(vacío o ausente)", cause, actions)

    # Rule R-17
    if rule_id == "R-17":
        m_field = re.search(r"Option '([^']+)'", msg)
        opt_id = m_field.group(1) if m_field else "option"
        field_name = f"options[{opt_id}].error_rationale"
        m_s = re.search(r"error_rationale':\s*'(.*)'", msg)
        snippet = m_s.group(1) if m_s else "(vacío o placeholder)"
        cause = "El campo 'error_rationale' contiene un placeholder genérico prohibido (ej. 'placeholder', 'distractor', 'error') o está vacío."
        actions = [
            "Redactar una explicación pedagógica formativa sobre el error que comete el estudiante al elegir la opción.",
            "Eliminar palabras prohibidas como 'placeholder', 'distractor', 'error', 'n/a' o 'ninguno'.",
            "Describir la confusión conceptual o error algebraico/aritmético subyacente.",
        ]
        return format_diagnostic_error("R-17: RATIONALE GENÉRICO / PLACEHOLDER", cid, tpl_id, item_id, field_name, snippet, cause, actions)

    # Rule R-15
    if rule_id == "R-15":
        cause = "La longitud de la respuesta correcta difiere significativamente del rango de los distractores (fuera de 0.80x - 1.20x), constituyendo una pista visual."
        actions = [
            "Calibrar la longitud de la respuesta correcta o de los distractores para que tengan una extensión homogénea.",
            "Homogeneizar el nivel de detalle y formato matemático entre todas las opciones.",
            "Asegurar que 0.80 * min(len(D)) <= len(correct) <= 1.20 * max(len(D)).",
        ]
        return format_diagnostic_error("R-15: EQUILIBRIO DE LONGITUD", cid, tpl_id, item_id, "options", msg, cause, actions)

    # Rule S-01
    if rule_id == "S-01":
        return format_diagnostic_error(
            "S-01: SOLUCIÓN PASO A PASO OBLIGATORIA", cid, tpl_id, item_id, "solution / detailed_solution",
            "(vacío o ausente)",
            "El reactivo carece de una solución explicativa paso a paso requerida en modo strict.",
            [
                "Agregar el campo 'detailed_solution' o 'solution' en la plantilla con la resolución paso a paso.",
                "Describir el procedimiento matemático o conceptual completo para llegar a la respuesta correcta.",
                "Asegurar que la solución esté redactada con KaTeX válido.",
            ]
        )

    # Rule S-02
    if rule_id == "S-02":
        return format_diagnostic_error(
            "S-02: MISCONCEPTION WARNING OBLIGATORIO", cid, tpl_id, item_id, "misconception_warning",
            "(vacío o ausente)",
            "El reactivo carece de una advertencia de error común ('misconception_warning') requerida en modo strict.",
            [
                "Agregar el campo 'misconception_warning' o 'common_misconception_warning' en la plantilla.",
                "O asociar distractor_ids que tengan 'remediation_hint' definido en cta.json.",
                "Explicar brevemente el error más común que deben evitar los estudiantes.",
            ]
        )

    # Rule S-03
    if rule_id == "S-03":
        return format_diagnostic_error(
            "S-03: DIFICULTAD EXPLÍCITA", cid, tpl_id, item_id, "difficulty",
            "(inválido o ausente)",
            "El reactivo no especifica un nivel de dificultad válido ('easy', 'medium', 'hard') en modo strict.",
            [
                "Declarar 'difficulty': 'easy', 'medium' o 'hard' en la plantilla.",
                "Alinear la dificultad con el nivel de Bloom y la complejidad del problema.",
                "No dejar el campo vacío ni con valores no reconocidos.",
            ]
        )

    # Generic Fallback
    action_fallback = "Revisa la regla y ajusta el generador o las variantes."
    return format_diagnostic_error(
        f"{rule_id}: CONTRATO DE VALIDACIÓN", cid, tpl_id, item_id, "question",
        msg,
        f"Violación de la regla {rule_id}: {msg}",
        [
            action_fallback,
            "Verificar la estructura y tipos de datos de los reactivos producidos.",
            "Corregir directamente en el script generador o archivo de plantillas.",
        ]
    )

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
            if err.rule_id in ("R-05", "R-06", "R-07", "R-08", "R-09", "R-16"):
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

    # 5. Dry-run 50 seeds and invariant evaluation
    seeds = list(range(100, 100 + num_dry_run_seeds))
    try:
        batch_results = execute_sandbox_batch(
            generate_py=generate_py,
            seeds=seeds,
            cross_check_py=cross_check_py,
            timeout_per_item=2.0,
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
        first_err = failed_seeds[0].get("error", "Unknown error")
        seed_items = [f"seed={r.get('seed')}" for r in failed_seeds]
        errors.append(format_diagnostic_error(
            "TPL-DRY: FALLO EN EJECUCIÓN DRY-RUN", competency_id, tpl_id, seed_items, "generate_py / cross_check_py",
            f"Error en seed {failed_seeds[0].get('seed')}: {first_err}",
            f"La ejecución en sandbox falló en {len(failed_seeds)}/{num_dry_run_seeds} semillas evaluadas.",
            [
                "Revisar la excepción en generate_py (división por cero, clave faltante, error de tipos, etc.).",
                "Probar localmente la función generate_py con la semilla que causó el fallo.",
                "Agregar validaciones o restricciones a los parámetros aleatorios para evitar estados matemáticos inválidos.",
            ]
        ))
        if len(failed_seeds) == len(batch_results):
            # Full failure of all seeds: no instances can be evaluated further
            return errors

    # Check invariants on all generated instances (Full Sweep: NO premature break)
    raw_asm_failures: Dict[str, List[str]] = {}
    raw_inv_failures: Dict[str, Tuple[str, List[str]]] = {}

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

        # Invariant check (Accumulate all failures: NO break)
        is_valid, inv_errors = check_instance_invariants(assembled_q, interaction_type)
        if not is_valid:
            has_collision = any("Distractor identical to correct answer" in e for e in inv_errors)
            for inv_err in inv_errors:
                if has_collision and "Duplicate option content detected" in inv_err:
                    continue
                canon_key = get_canonical_invariant_key(inv_err)
                if canon_key not in raw_inv_failures:
                    raw_inv_failures[canon_key] = (inv_err, [f"seed={seed_val}"])
                else:
                    raw_inv_failures[canon_key][1].append(f"seed={seed_val}")

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
    for canon_key, (rep_inv_err, seed_list) in raw_inv_failures.items():
        errors.append(format_invariant_error_diagnostic(
            cid=competency_id,
            tpl_id=tpl_id,
            q_id=seed_list,
            inv_err=rep_inv_err,
            q_obj=None,
        ))

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
    has_placeholder = bool(re.search(r"\{[A-Za-z0-9_]+(?::[^{}]+)?\}", stem))
    has_variants = bool(stem_variants and len(stem_variants) > 0)
    if not (has_placeholder or has_variants):
        errors.append(format_diagnostic_error(
            "TPL-VAR: DIVERSIDAD DE REACTIVOS", competency_id, tpl_id, "template", "stem / stem_variants",
            f"stem: '{stem[:60]}...'",
            f"TPL-VAR violation in '{tpl_id}': stem must contain at least one placeholder '{{var}}' or 'stem_variants' must be present.",
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
                    comp_inv_failures[sig] = (inv_err, [q_id])
                else:
                    comp_inv_failures[sig][1].append(q_id)

    for (t_id, canon_key), (rep_err, q_ids) in comp_inv_failures.items():
        unique_q_ids = list(dict.fromkeys(q_ids))
        errors.append(format_invariant_error_diagnostic(
            cid=cid,
            tpl_id=t_id,
            q_id=unique_q_ids,
            inv_err=rep_err,
            q_obj=None,
        ))

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
    auto_fix: bool = True,
) -> Tuple[bool, List[str]]:
    """Validate all templates in file(s) or directory against CTA with production contract parity."""
    # warm_up_sandbox()  # Omit blind warmup: in-process execution is already instant
    errors = []

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
                errors.append(format_diagnostic_error(
                    rule_tag="TPL-D3: COBERTURA COMPLETA DE DISTRACTORES",
                    competency=cid,
                    template="[Todas las plantillas de la competencia]",
                    item_id="N/A",
                    field_name="distractor_ids",
                    snippet=f"Distractores sin cubrir: {sorted(uncovered)} ({len(uncovered)}/{len(declared_set)})",
                    cause="Existen distractores definidos en cta.json que ninguna plantilla de la competencia está utilizando.",
                    actions=[
                        f"Asignar los distractores sin cubrir ({sorted(uncovered)}) en las plantillas existentes de '{cid}'.",
                        "O crear plantillas adicionales que ejerciten los conceptos erróneos representados por estos distractores.",
                        "Asegurar que el 100% de los distractores de cta.json tengan al menos una plantilla que los emplee.",
                    ],
                ))

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

    # Resolve attempts_dir automatically if not supplied
    effective_attempts_dir = attempts_dir
    if effective_attempts_dir is None:
        if cta_p is not None:
            effective_attempts_dir = cta_p.parent / ".check_attempts"
        elif template_files:
            effective_attempts_dir = template_files[0].parent / ".check_attempts"
        else:
            effective_attempts_dir = Path("work/.check_attempts")

    # Circuit breaker and attempt tracking
    if effective_attempts_dir is not None:
        try:
            att_path = Path(effective_attempts_dir)
            att_path.mkdir(parents=True, exist_ok=True)
            # Derive deterministic scope key for circuit breaker isolation across concurrent shards
            if processed_comp_ids:
                scope_raw = "_".join(sorted(processed_comp_ids))
            elif targets:
                scope_raw = "_".join(sorted(str(t) for t in targets))
            else:
                scope_raw = "global"

            if len(scope_raw) > 32:
                scope_key = hashlib.sha256(scope_raw.encode("utf-8")).hexdigest()[:12]
            else:
                scope_key = re.sub(r"[^a-zA-Z0-9_-]", "_", scope_raw)

            cb_file = att_path / f"circuit_breaker_{scope_key}.json"
            legacy_cb_file = att_path / "circuit_breaker.json"

            if not is_clean:
                # Compute deterministic error fingerprint
                normalized_errs = sorted([re.sub(r"at 0x[0-9a-fA-F]+", "", e.strip()) for e in errors])
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
                cb_file.write_text(json.dumps(cb_data, indent=2, ensure_ascii=False), encoding="utf-8")

                if cb_data["consecutive_count"] >= 3:
                    cb_msg = (
                        f"[-] [CIRCUIT BREAKER: FALLOS CONSECUTIVOS IDÉNTICOS]\n"
                        f"    UBICACIÓN: Subagente de autoría de plantillas\n"
                        f"    CAUSA: Se han detectado 3 ejecuciones consecutivas de check_templates.py con exactamente el mismo número ({len(errors)}) y tipo de errores sin ningún progreso.\n"
                        f"    ACTION REQUIRED: Detener de inmediato las llamadas a herramientas y responder:\n"
                        f"    BLOCKED: CONTRACT_ERROR - Circuit breaker activado tras 3 fallos consecutivos idénticos.\n"
                        f"    PROHIBIDO reintentar modificaciones a ciegas sin consultar al orquestador."
                    )
                    errors.append(cb_msg)
            else:
                # Clear circuit breaker on clean pass
                if cb_file.is_file():
                    cb_file.unlink()
                if legacy_cb_file.is_file():
                    legacy_cb_file.unlink()

            # Per-competency budget halt tracking
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
                    if f_att.is_file():
                        f_att.unlink()
        except Exception:
            pass

    is_clean = (len(errors) == 0)
    return is_clean, errors


def main():
    parser = argparse.ArgumentParser(description="Validate parametric exercise templates with Isomorphic Contract Parity")
    parser.add_argument("target", nargs="+", help="Path(s) to template.json file(s) or templates/ directory")
    parser.add_argument("--cta", default=None, help="Path to cta.json file")
    parser.add_argument("--seeds", type=int, default=50, help="Number of dry-run seeds (default 50)")
    parser.add_argument("--strict", action="store_true", default=True, help="Enforce production contract parity (default: true)")
    parser.add_argument("--no-strict", dest="strict", action="store_false", help="Bypass production parity checks")
    parser.add_argument("--auto-fix", dest="auto_fix", action="store_true", default=True, help="Automatically heal mechanical issues in templates (default: True)")
    parser.add_argument("--no-auto-fix", dest="auto_fix", action="store_false", help="Bypass mechanical auto-healing of templates")
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
        auto_fix=args.auto_fix,
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
        has_cb = any("CIRCUIT BREAKER" in str(e) for e in errors)
        compact_output = render_compact_aggregated_errors(errors, targets=targets)
        print(compact_output)
        sys.exit(2 if has_cb else 1)

    print(f"PASS: All templates satisfy schema, AST security, {args.seeds} seeds dry run, invariants, TPL-D1..D4 rules, and Production Parity.")
    sys.exit(0)


if __name__ == "__main__":
    main()

