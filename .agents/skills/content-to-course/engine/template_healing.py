"""Shared template and shard source healing utilities for content-to-course."""

import ast
import json
import os
import re
import tempfile
import textwrap
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# Auto-curación de caracteres de control ASCII: previene escapes corruptos de LaTeX (\frac, \beta, \alpha, \vec) cuando alguien edita JSON directo
_CONTROL_CHAR_TEXT_MAP = {
    "\x0c": r"\f",   # \frac, \forall -> 1 backslash in text (len 2: '\', 'f')
    "\x08": r"\b",   # \beta, \bar, \binom, \begin -> 1 backslash in text (len 2: '\', 'b')
    "\x07": r"\a",   # \alpha, \approx -> 1 backslash in text (len 2: '\', 'a')
    "\x0b": r"\v",   # \vec, \varepsilon -> 1 backslash in text (len 2: '\', 'v')
    "\x0d": r"\r",   # \rho, \right, \Rightarrow, \rightarrow -> 1 backslash in text (len 2: '\', 'r')
}

_CONTROL_CHAR_CODE_MAP = {
    "\x0c": r"\\f",   # In standard Python string literal, \\f escapes backslash for compiler
    "\x08": r"\\b",
    "\x07": r"\\a",
    "\x0b": r"\\v",
    "\x0d": r"\\r",
}

_CONTROL_CHAR_LATEX_MAP = _CONTROL_CHAR_TEXT_MAP

LATEX_PREFIX_PATTERNS = [
    r"rho\b|right\b|Rightarrow\b|rightarrow\b|ightharpoondown\b|ightharpoonup\b|rightleftharpoons\b|rangle\b|rceil\b|rfloor\b|rgroup\b|rhd\b|rule\b|rVert\b",
    r"frac\b|forall\b|flat\b|frown\b|fbox\b",
    r"alpha\b|approx\b|angle\b|alert\b|arrow\b|asymp\b|acute\b",
    r"beta\b|bar\b|begin\b|binom\b|big\b|boldsymbol\b|backslash\b|boxed\b|bullet\b|bot\b|mathbb\b",
    r"tau\b|theta\b|text\b|times\b|to\b|triangle\b|tilde\b|tanh\b|tan\b|top\b",
    r"nu\b|neq\b|nabla\b|ni\b|not\b|natural\b",
    r"vec\b|varepsilon\b|vartheta\b|varphi\b|varpi\b|varrho\b|varsigma\b|vdots\b|vdash\b|vee\b|vert\b",
]
COMBINED_LATEX = "|".join(LATEX_PREFIX_PATTERNS)


def heal_control_chars_in_str(s: str) -> str:
    """Heals ASCII control characters resulting from unescaped LaTeX backslashes."""
    if not isinstance(s, str) or not s:
        return s

    s = s.replace("\r\n", "\n")

    # 1. LaTeX prefixes collided with control characters
    s = re.sub(r"\x07(lpha|pprox|ngle|lert|rrow|symp|cute)", r"\\a\1", s)
    s = re.sub(r"\x08(eta|ar|egin|inom|ig|oldsymbol|ackslash|oxed|ullet|ot)", r"\\b\1", s)
    s = re.sub(r"\x0b(ec|arepsilon|artheta|arphi|arpi|arrho|arsigma|dots|dash|ee|ert)", r"\\v\1", s)
    s = re.sub(r"\x0c(rac|orall|lat|rown|box)", r"\\f\1", s)
    s = re.sub(r"\x0d(ho|ight|ightarrow|ightharpoondown|ightharpoonup|ightleftharpoons|angle|ceil|floor|group|hd|ule|Vert)", r"\\r\1", s)
    s = re.sub(r"\x09(au|heta|ext|imes|o\b|riangle|tilde|tanh|tan\b|top\b)", r"\\t\1", s)
    s = re.sub(r"\x0a(u\b|eq\b|abla|i\b|ot\b|atural)", r"\\n\1", s)

    # 2. Bare control characters
    s = (
        s.replace("\x07", r"\a")
        .replace("\x08", r"\b")
        .replace("\x0b", r"\v")
        .replace("\x0c", r"\f")
        .replace("\x0d", r"\r")
    )
    return s


def heal_control_chars_in_obj(obj: Any) -> Any:
    """Recursively traverses dictionaries, lists, tuples and heals control chars in all strings."""
    if isinstance(obj, str):
        return heal_control_chars_in_str(obj)
    elif isinstance(obj, dict):
        return {
            (heal_control_chars_in_str(k) if isinstance(k, str) else k): heal_control_chars_in_obj(v)
            for k, v in obj.items()
        }
    elif isinstance(obj, list):
        return [heal_control_chars_in_obj(elem) for elem in obj]
    elif isinstance(obj, tuple):
        return tuple(heal_control_chars_in_obj(elem) for elem in obj)
    return obj


_MATH_SEGMENT_RE = re.compile(r"((?<!\\)\$\$[\s\S]*?(?<!\\)\$\$|(?<!\\)\$(?!\$)(?:\\.|[^$\\])+?(?<!\\)\$)")
_HEAL_SCI_RE = re.compile(r"(?<![A-Za-z0-9_\\])(\d+(?:\.\d+)?)[eE]([+-])(\d{2,})(?![A-Za-z0-9_])")


def heal_katex_display_str(text: str) -> str:
    """Apply safe mechanical KaTeX fixes inside $...$/$$...$$ display blocks only.

    Heals:
    - ASCII control chars via heal_control_chars_in_str
    - Digit-placeholder concatenation (e.g. 2@c@ -> 2 \\cdot @c@)
    - Adjacent placeholders inside math (e.g. @a@@b@ -> @a@ \\cdot @b@)
    - Leaked SymPy ** and sqrt(...) inside KaTeX math blocks
    - Raw Python scientific notation (e.g. 1e-05 -> 1 \\times 10^{-5})
    """
    if not isinstance(text, str) or not text:
        return text

    healed = heal_control_chars_in_str(text)
    if "$" not in healed:
        return healed

    def _repl_sci(m: re.Match) -> str:
        sign = "-" if m.group(2) == "-" else ""
        exp = m.group(3).lstrip("0") or "0"
        if exp == "0":
            sign = ""
        return rf"{m.group(1)} \times 10^{{{sign}{exp}}}"

    def _heal_math_segment(m: re.Match) -> str:
        block = m.group(1)
        delim = "$$" if block.startswith("$$") else "$"
        inner = block[len(delim):-len(delim)]
        if not inner:
            return block
        inner = re.sub(r"(\\[a-zA-Z]+)(@[a-zA-Z_]\w*(?::[^@\s]*)?@)", r"\1 \2", inner)
        # Wrap unbraced superscript/subscript placeholders: ^@var@ -> ^{@var@}, _@var@ -> _{@var@}
        inner = re.sub(r"([\^_])(@[a-zA-Z_]\w*(?::[^@\s]*)?@)", r"\1{\2}", inner)
        inner = re.sub(r"(?<![A-Za-z0-9_^\\])(\d+)@([a-zA-Z_]\w*)@", r"\1 \\cdot @\2@", inner)
        inner = re.sub(r"@([a-zA-Z_]\w*)@(?=\d)", r"@\1@ \\cdot ", inner)
        inner = re.sub(
            r"(@[a-zA-Z_]\w*(?::[^@\s]*)?@)(?=@[a-zA-Z_]\w*(?::[^@\s]*)?@)",
            r"\1 \\cdot ",
            inner,
        )
        inner = re.sub(r"([A-Za-z0-9_)\]])\*\*([A-Za-z0-9_]+)", r"\1^{\2}", inner)
        inner = re.sub(r"(?<![A-Za-z0-9_\\])(\d+)\*([A-Za-z(])", r"\1 \\cdot \2", inner)
        inner = re.sub(r"(?<![\\a-zA-Z])sqrt\(\s*([^()]+?)\s*\)", r"\\sqrt{\1}", inner)
        inner = _HEAL_SCI_RE.sub(_repl_sci, inner)
        return f"{delim}{inner}{delim}"

    return _MATH_SEGMENT_RE.sub(_heal_math_segment, healed)


def normalize_prose_outside_math(text: str) -> Tuple[str, List[str]]:
    """Apply safe, idempotent prose polish strictly outside $...$ / $$...$$ math blocks.

    - Collapses accidental double periods ('..') to '.' (preserving '...' ellipses).
    - Collapses multiple consecutive spaces ('  ') to a single space.
    Never modifies math segments, numbers, equations, or newline characters.
    """
    if not isinstance(text, str) or not text:
        return text, []

    parts = _MATH_SEGMENT_RE.split(text)
    changes: List[str] = []
    out_parts: List[str] = []
    double_period_collapsed = False
    multi_space_collapsed = False

    for idx, seg in enumerate(parts):
        if idx % 2 == 1:
            # Inside $...$ or $$...$$ math block: leave verbatim
            out_parts.append(seg)
            continue
        new_seg = re.sub(r"(?<!\.)\.\.(?!\.)", ".", seg)
        if new_seg != seg:
            double_period_collapsed = True
        new_seg2 = re.sub(r"[ ]{2,}", " ", new_seg)
        if new_seg2 != new_seg:
            multi_space_collapsed = True
        out_parts.append(new_seg2)

    if double_period_collapsed:
        changes.append("collapsed '..' to '.'")
    if multi_space_collapsed:
        changes.append("collapsed consecutive spaces")

    return "".join(out_parts), changes


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
    if not isinstance(text, str) or not text:
        return placeholders

    # 1. PrairieLearn tokens: @var@ or @var:fmt@
    for m in re.finditer(r"@([a-zA-Z_][a-zA-Z0-9_]*)(?::([^@\s{}]+))?@", text):
        placeholders.add(m.group(1))

    # 2. Python-style {var} tokens
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




_GIVEAWAY_PREFIX_RE = re.compile(
    r"^(?:Inversión de roles|Omisión de límites|Asumiendo erróneamente|Confusión de conceptos|Falsa generalización|Error de signo):\s*",
    re.IGNORECASE,
)
_GIVEAWAY_PREFIX_STR_RE = re.compile(
    r"(['\"])(?:Inversión de roles|Omisión de límites|Asumiendo erróneamente|Confusión de conceptos|Falsa generalización|Error de signo):\s*",
    re.IGNORECASE,
)


def _scan_latex_balanced_span(text: str, start: int) -> int:
    """Starting at start (index of backslash of LaTeX command), scans forward balancing nested braces."""
    n = len(text)
    if start >= n or text[start] != "\\":
        return start

    pos = start + 1
    while pos < n and text[pos].isalpha():
        pos += 1

    # Loop over arguments, subscripts, superscripts, or attached math symbols
    while pos < n:
        if text[pos] == "{":
            depth = 1
            pos += 1
            while pos < n and depth > 0:
                if text[pos] == "{":
                    depth += 1
                elif text[pos] == "}":
                    depth -= 1
                elif text[pos] == "\\" and pos + 1 < n and text[pos + 1] in "{}":
                    pos += 1
                pos += 1
            if depth > 0:
                break
        elif text[pos] in ("_", "^"):
            pos += 1
            if pos < n and text[pos] == "{":
                depth = 1
                pos += 1
                while pos < n and depth > 0:
                    if text[pos] == "{":
                        depth += 1
                    elif text[pos] == "}":
                        depth -= 1
                    elif text[pos] == "\\" and pos + 1 < n and text[pos + 1] in "{}":
                        pos += 1
                    pos += 1
                if depth > 0:
                    break
            elif pos < n and text[pos] == "\\":
                pos += 1
                while pos < n and text[pos].isalpha():
                    pos += 1
            elif pos < n and (text[pos].isalnum() or text[pos] in "+-"):
                pos += 1
            else:
                pos -= 1
                break
        elif text[pos] == "\\":
            cand_pos = pos + 1
            while cand_pos < n and text[cand_pos].isalpha():
                cand_pos += 1
            if cand_pos > pos + 1:
                pos = cand_pos
            else:
                break
        else:
            break

    # Optional relational operator or equals: e.g. \beta = 0 or \le 0.05
    rel_m = re.match(r"^\s*(?:=|<|>|\\le|\\ge|\\neq|\\approx)\s*", text[pos:])
    if rel_m:
        rel_end = pos + rel_m.end()
        rhs_pos = rel_end
        while rhs_pos < n and text[rhs_pos] not in ",;.$)":
            if text[rhs_pos] == "{":
                depth = 1
                rhs_pos += 1
                while rhs_pos < n and depth > 0:
                    if text[rhs_pos] == "{":
                        depth += 1
                    elif text[rhs_pos] == "}":
                        depth -= 1
                    rhs_pos += 1
                if depth > 0:
                    break
            elif text[rhs_pos].isspace() and (rhs_pos + 1 >= n or not (text[rhs_pos + 1].isalnum() or text[rhs_pos + 1] in "\\+-/*")):
                break
            else:
                rhs_pos += 1
        if rhs_pos > rel_end:
            pos = rhs_pos

    return pos


def _wrap_bare_latex_in_rationale(text: str) -> str:
    """Wraps bare or orphan LaTeX expressions in $...$ within rationale strings.

    Leaves existing $...$ and $$...$$ blocks intact.
    Detects LaTeX commands (e.g. \\frac, \\beta, \\hat, \\sigma, \\times) and math symbols
    that appear without $ delimiters and encloses them safely in KaTeX inline math,
    robustly balancing arbitrarily nested braces in subscripts and superscripts.
    """
    if not isinstance(text, str) or not text.strip():
        return text if isinstance(text, str) else ""

    text = heal_control_chars_in_str(text)

    # 1. Identify existing math spans: $...$ or $$...$$
    math_spans = []
    for m in re.finditer(r"\$\$[\s\S]*?\$\$|\$[^\$\n]*?\$", text):
        math_spans.append((m.start(), m.end()))

    def is_in_math(pos: int) -> bool:
        return any(s <= pos < e for s, e in math_spans)

    # 2. Find bare LaTeX command sequences scanning balanced nested braces
    matches = []
    cmd_iter = re.finditer(r"\\[a-zA-Z]+", text)
    curr_end = 0
    for m in cmd_iter:
        if m.start() < curr_end:
            continue
        if is_in_math(m.start()):
            continue
        span_end = _scan_latex_balanced_span(text, m.start())
        if span_end > m.start():
            matches.append((m.start(), span_end, text[m.start():span_end]))
            curr_end = span_end

    if not matches:
        return text

    out_parts = []
    last_idx = 0
    for start, end, s in matches:
        if start < last_idx:
            continue
        out_parts.append(text[last_idx:start])
        clean_s = s.rstrip(".,;")
        trailing = s[len(clean_s):]
        out_parts.append(f"${clean_s}${trailing}")
        last_idx = end
    out_parts.append(text[last_idx:])

    return "".join(out_parts)


def _strip_giveaway_prefix(text: str) -> str:
    cleaned = _GIVEAWAY_PREFIX_RE.sub("", text).strip()
    if cleaned:
        cleaned = cleaned[0].upper() + cleaned[1:]
    return cleaned


def _build_distractor_lookup_from_cta(
    cta_comp: Optional[Dict[str, Any]] = None,
    target_cid: Optional[str] = None,
) -> Dict[str, str]:
    """Extract clean KaTeX-wrapped giveaway-free rationales keyed by distractor_id from CTA context."""
    distractor_lookup: Dict[str, str] = {}
    if not cta_comp or not isinstance(cta_comp, dict):
        return distractor_lookup

    def _extract_rat(d: Dict[str, Any]) -> str:
        wb = d.get("wrong_belief") or d.get("manifestation") or ""
        om = d.get("omitted_step") or ""
        rem = d.get("remediation_hint") or ""
        if wb and om:
            rat = f"{wb.rstrip('.')}. Se debe considerar: {om.rstrip('.')}."
        elif wb:
            rat = wb
        elif rem:
            rat = rem
        elif om:
            rat = f"Error procedimental: {om}."
        else:
            rat = d.get("name") or ""
        if rat:
            return _wrap_bare_latex_in_rationale(_strip_giveaway_prefix(str(rat)))
        return ""

    if isinstance(cta_comp.get("distractors"), list):
        for d in cta_comp["distractors"]:
            if isinstance(d, dict) and d.get("id"):
                r = _extract_rat(d)
                if r:
                    distractor_lookup[str(d["id"])] = r
    elif isinstance(cta_comp.get("competencies"), list):
        for c in cta_comp["competencies"]:
            if not target_cid or c.get("id") == target_cid:
                for d in c.get("distractors", []):
                    if isinstance(d, dict) and d.get("id"):
                        r = _extract_rat(d)
                        if r:
                            distractor_lookup[str(d["id"])] = r
    elif all(isinstance(v, dict) for v in cta_comp.values()):
        for did, d in cta_comp.items():
            if isinstance(d, dict):
                r = _extract_rat(d)
                if r:
                    distractor_lookup[str(did)] = r

    return distractor_lookup


def auto_heal_template_data(
    data: Dict[str, Any],
    cta_comp: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    """Applies strictly mechanical, non-semantic auto-healing to a loaded template dict:
    1. Restores corrupted ASCII control chars in text (single backslash) and code (AST safe).
    2. Auto-exports local variables computed in generate(rng) into 'vars' dict
       when referenced as {var_name} in stem, stem_variants, hints, or solution.
    3. Populates missing error_rationale in multiple_select and multiple_choice_7_options from cta_comp distractors.
    4. Strips obvious R-18 giveaway prefixes from rationales and options.
    """
    modified = False
    fixes: List[str] = []

    # Build distractor lookup from cta_comp / cta_data
    target_cid = data.get("competency_id") if isinstance(data, dict) else None
    distractor_lookup: Dict[str, str] = _build_distractor_lookup_from_cta(cta_comp, target_cid=target_cid)

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

        # 1. Heal control characters, safe KaTeX display leaks, and outside-math prose polish
        for s_field in ("stem", "stem_es", "solution", "explanation_es", "detailed_solution"):
            val = tpl.get(s_field)
            if isinstance(val, str):
                new_val = heal_katex_display_str(val)
                new_val, prose_changes = normalize_prose_outside_math(new_val)
                if new_val != val:
                    tpl[s_field] = new_val
                    modified = True
                    note = ", ".join(prose_changes) if prose_changes else "healed KaTeX display / control chars"
                    fixes.append(f"{tid}.{s_field}: {note}")

        # Heal control characters in Python code fields
        for c_field in ("generate_py", "cross_check_py", "generator_code", "verifier_code"):
            c_val = tpl.get(c_field)
            if isinstance(c_val, str) and any(ctrl in c_val for ctrl in _CONTROL_CHAR_TEXT_MAP):
                new_c_val = _heal_code_control_chars(c_val)
                if new_c_val != c_val:
                    tpl[c_field] = new_c_val
                    modified = True
                    fixes.append(f"{tid}.{c_field}: restored ASCII control char to LaTeX backslash in Python code")

        # Heal control characters, safe KaTeX display leaks, and outside-math prose polish in list fields
        for list_field in ("stem_variants", "hints"):
            items = tpl.get(list_field)
            if isinstance(items, list):
                for i, item in enumerate(items):
                    if isinstance(item, str):
                        new_item = heal_katex_display_str(item)
                        new_item, prose_changes = normalize_prose_outside_math(new_item)
                        if new_item != item:
                            items[i] = new_item
                            modified = True
                            note = ", ".join(prose_changes) if prose_changes else "healed KaTeX display / control chars"
                            fixes.append(f"{tid}.{list_field}[{i}]: {note}")

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

                    def _collect_target_names(tgt: ast.AST) -> None:
                        if isinstance(tgt, ast.Name):
                            assigned_locals.add(tgt.id)
                        elif isinstance(tgt, (ast.Tuple, ast.List)):
                            for elt in tgt.elts:
                                _collect_target_names(elt)
                        elif isinstance(tgt, ast.Starred):
                            _collect_target_names(tgt.value)

                    gen_func_node = next(
                        (
                            n for n in ast.walk(tree)
                            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == "generate"
                        ),
                        None,
                    )
                    if gen_func_node is not None:
                        scope_stack: List[ast.AST] = list(gen_func_node.body)
                        while scope_stack:
                            node = scope_stack.pop()
                            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                                continue
                            if isinstance(node, ast.Assign):
                                for target in node.targets:
                                    _collect_target_names(target)
                            elif isinstance(node, ast.AnnAssign):
                                _collect_target_names(node.target)
                            elif isinstance(node, (ast.For, ast.AsyncFor)):
                                _collect_target_names(node.target)
                            elif isinstance(node, (ast.With, ast.AsyncWith)):
                                for item in node.items:
                                    if item.optional_vars is not None:
                                        _collect_target_names(item.optional_vars)
                            for child in ast.iter_child_nodes(node):
                                if not isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                                    scope_stack.append(child)

                    missing_vars = (referenced_vars & assigned_locals) - {"rng"}
                    if missing_vars:
                        # AST-safe helper to convert (lineno, col_offset) to character index in gen_py
                        gp_lines = gen_py.splitlines(keepends=True)
                        line_offsets = [0]
                        for _ln in gp_lines:
                            line_offsets.append(line_offsets[-1] + len(_ln))

                        def _ast_pos_to_idx(lineno: int, col_offset: int) -> int:
                            line_str = gp_lines[lineno - 1]
                            byte_prefix = line_str.encode("utf-8")[:col_offset]
                            return line_offsets[lineno - 1] + len(byte_prefix.decode("utf-8", errors="replace"))

                        def _inject_into_ast_dict(dict_node: ast.Dict, extra_existing: Optional[Set[str]] = None, label: str = "vars") -> bool:
                            existing_keys = {
                                k.value for k in dict_node.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)
                            }
                            if extra_existing:
                                existing_keys |= extra_existing
                            missing_export = sorted(missing_vars - existing_keys)
                            if not missing_export:
                                return True
                            if dict_node.end_lineno is None or dict_node.end_col_offset is None:
                                return False
                            end_idx = _ast_pos_to_idx(dict_node.end_lineno, dict_node.end_col_offset)
                            # Locate the exact closing '}' of this ast.Dict
                            close_brace_idx = end_idx - 1
                            if close_brace_idx < 0 or close_brace_idx >= len(gen_py) or gen_py[close_brace_idx] != "}":
                                return False
                            start_idx = _ast_pos_to_idx(dict_node.lineno, dict_node.col_offset)
                            inner_body = gen_py[start_idx + 1:close_brace_idx]
                            add_pairs = ", ".join(f"'{v}': {v}" for v in missing_export)
                            if inner_body.strip():
                                sep = " " if inner_body.rstrip().endswith(",") else ", "
                            else:
                                sep = ""
                            new_gp = gen_py[:close_brace_idx] + f"{sep}{add_pairs}" + gen_py[close_brace_idx:]
                            try:
                                ast.parse(new_gp)
                                tpl["generate_py"] = new_gp
                                nonlocal modified
                                modified = True
                                fixes.append(f"{tid}.generate_py: auto-exported {missing_export} into '{label}'")
                                return True
                            except Exception:
                                return False

                        # Locate 'vars' entry in AST Dicts (handling both inline dict and assigned dict variable)
                        vars_val_node = None
                        for dnode in ast.walk(tree):
                            if isinstance(dnode, ast.Dict):
                                for dk, dv in zip(dnode.keys, dnode.values):
                                    if isinstance(dk, ast.Constant) and dk.value == "vars" and dv is not None:
                                        vars_val_node = dv
                                        break
                            if vars_val_node is not None:
                                break

                        if isinstance(vars_val_node, ast.Dict):
                            # Case 2A: 'vars': { ... } inline dict literal (f-string / nested-brace safe via AST)
                            _inject_into_ast_dict(vars_val_node, label="vars")
                        elif isinstance(vars_val_node, ast.Name):
                            # Case 2B: 'vars': var_name where var_name = { ... } (never splits inside f"{b:.1f}")
                            vname = vars_val_node.id
                            target_dict_node: Optional[ast.Dict] = None
                            subscript_keys: Set[str] = set()
                            for anode in ast.walk(tree):
                                if isinstance(anode, ast.Assign):
                                    for tgt in anode.targets:
                                        if isinstance(tgt, ast.Name) and tgt.id == vname and isinstance(anode.value, ast.Dict):
                                            target_dict_node = anode.value
                                        elif (
                                            isinstance(tgt, ast.Subscript)
                                            and isinstance(tgt.value, ast.Name)
                                            and tgt.value.id == vname
                                            and isinstance(tgt.slice, ast.Constant)
                                            and isinstance(tgt.slice.value, str)
                                        ):
                                            subscript_keys.add(tgt.slice.value)
                            if target_dict_node is not None:
                                _inject_into_ast_dict(target_dict_node, extra_existing=subscript_keys, label=vname)
                        elif vars_val_node is None:
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

        # 3. Auto-fill missing error_rationale in multiple_select and multiple_choice_7_options from CTA distractor lookup
        if tpl.get("interaction_type") in ("multiple_select", "multiple_choice_7_options", "multiple_choice") and distractor_lookup and isinstance(tpl.get("generate_py"), str):
            gp = tpl["generate_py"]
            for did, rat in distractor_lookup.items():
                safe_rat = rat.replace("\\", "\\\\").replace("'", "\\'")

                # Pattern 1: distractor_id followed by error_rationale: None or "" or ''
                p1 = rf"(['\"](?:distractor_id|id)['\"]\s*:\s*['\"]{re.escape(did)}['\"]\s*,\s*['\"]error_rationale['\"]\s*:\s*)(None|['\"]['\"])"
                new_gp = re.sub(p1, lambda m: f"{m.group(1)}'{safe_rat}'", gp)

                # Pattern 2: error_rationale: None or "" or '' followed by distractor_id
                p2 = rf"(['\"]error_rationale['\"]\s*:\s*)(None|['\"]['\"])(\s*,\s*['\"](?:distractor_id|id)['\"]\s*:\s*['\"]{re.escape(did)}['\"])"
                new_gp = re.sub(p2, lambda m: f"{m.group(1)}'{safe_rat}'{m.group(3)}", new_gp)

                # Pattern 3: option dict contains distractor_id, but error_rationale is missing entirely
                def _inject_missing_rat(m: re.Match) -> str:
                    d_str = m.group(0)
                    if "error_rationale" not in d_str and "'rationale'" not in d_str and '"rationale"' not in d_str:
                        return re.sub(
                            rf"(['\"](?:distractor_id|id)['\"]\s*:\s*['\"]{re.escape(did)}['\"])",
                            lambda m2: f"{m2.group(1)}, 'error_rationale': '{safe_rat}'",
                            d_str,
                            count=1,
                        )
                    return d_str

                new_gp = re.sub(
                    rf"\{{[^{{}}]*['\"](?:distractor_id|id)['\"]\s*:\s*['\"]{re.escape(did)}['\"][^{{}}]*\}}",
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

        # 4. Strip R-18 giveaway prefixes and wrap bare LaTeX in distractor_archetypes and options
        if "distractor_archetypes" in tpl and isinstance(tpl["distractor_archetypes"], list):
            for da in tpl["distractor_archetypes"]:
                if isinstance(da, dict):
                    for rkey in ("rationale", "manifestation", "description"):
                        if isinstance(da.get(rkey), str):
                            old_r = da[rkey]
                            new_r = heal_katex_display_str(_wrap_bare_latex_in_rationale(_strip_giveaway_prefix(old_r)))
                            if new_r != old_r:
                                da[rkey] = new_r
                                modified = True
                                fixes.append(f"{tid}.distractor_archetypes: sanitized {rkey}")

        if "options" in tpl and isinstance(tpl["options"], list):
            for opt in tpl["options"]:
                if isinstance(opt, dict) and not opt.get("is_correct"):
                    did = opt.get("distractor_id") or opt.get("id")
                    cur_rat = opt.get("error_rationale")
                    if not cur_rat or str(cur_rat).strip() in ("", "None", "placeholder", "N/A", "error", "distractor"):
                        if did and did in distractor_lookup:
                            opt["error_rationale"] = distractor_lookup[did]
                            modified = True
                            fixes.append(f"{tid}.options: auto-populated error_rationale for {did} from CTA")
                    elif isinstance(cur_rat, str):
                        old_r = cur_rat
                        new_r = heal_katex_display_str(_wrap_bare_latex_in_rationale(_strip_giveaway_prefix(old_r)))
                        if new_r != old_r:
                            opt["error_rationale"] = new_r
                            modified = True
                            fixes.append(f"{tid}.options: sanitized error_rationale")

        if isinstance(tpl.get("generate_py"), str):
            gp_curr = tpl["generate_py"]
            gp_clean = _GIVEAWAY_PREFIX_STR_RE.sub(r"\1", gp_curr)
            if gp_clean != gp_curr:
                try:
                    ast.parse(gp_clean)
                    tpl["generate_py"] = gp_clean
                    modified = True
                    fixes.append(f"{tid}.generate_py: stripped giveaway prefixes")
                except Exception:
                    pass

    return modified, fixes


def _atomic_write_bytes(target_path: Path, data: bytes) -> None:
    """Atomically write bytes to target_path via tempfile + os.replace."""
    target_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path: Optional[Path] = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=str(target_path.parent),
            prefix=f".{target_path.name}.",
            suffix=".tmp",
            delete=False,
        ) as tmp_f:
            tmp_path = Path(tmp_f.name)
            tmp_f.write(data)
        os.replace(tmp_path, target_path)
    except Exception:
        if tmp_path is not None and tmp_path.exists():
            try:
                tmp_path.unlink()
            except Exception:
                pass
        raise


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
        _atomic_write_bytes(p, json.dumps(content, indent=2, ensure_ascii=False).encode("utf-8"))
    return modified, fixes




def check_ast_rf_triple_braces(source_text: str) -> List[str]:
    """Check for rf'...' or fr'...' strings containing '{{{' which corrupts KaTeX braces."""
    warnings = []
    if not source_text or not isinstance(source_text, str):
        return warnings
    for m in re.finditer(r"(?i)\b(rf|fr)(['\"]{1,3})([\s\S]*?)\2", source_text):
        if "{{{" in m.group(3):
            snippet = m.group(0)
            warnings.append(
                f"[!] Warning: Se detectó {m.group(1)}{m.group(2)}...{m.group(2)} conteniendo '{{{{{{' ({snippet}). "
                "Recomendación: Utilice raw strings r\"...\" con tokens @var@ para evitar la corrupción de llaves KaTeX."
            )
    return warnings


_FRANKENSTEIN_SUM_TRIGGER_RE = re.compile(
    r"\b(?:la\s+suma\s+del?|suma\s+entre|suma\s+total\s+del?|sumando|sume|sumar|[íi]ndice\s+compuesto)\b",
    re.IGNORECASE,
)

_FRANKENSTEIN_UNIT_GROUPS: List[Tuple[str, re.Pattern]] = [
    (
        "probabilidad",
        re.compile(
            r"\b(?:probabilidad(?:es)?|cota\s+(?:superior\s+|inferior\s+)?de\s+probabilidad|p-?valor(?:es)?|valor\s+p|nivel\s+de\s+(?:confianza|significancia))\b",
            re.IGNORECASE,
        ),
    ),
    (
        "varianza/ECM",
        re.compile(
            r"\b(?:varianza(?:s)?|error\s+cuadr[áa]tico\s+medio|ecm|mse)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "escala_lineal",
        re.compile(
            r"\b(?:desviaci[óo]n\s+(?:est[áa]ndar|t[íi]pica)|error\s+est[áa]ndar|(?:ancho|amplitud|longitud)\s+(?:del\s+)?intervalo|margen\s+de\s+error)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "tamaño_muestral",
        re.compile(
            r"\b(?:tama[ñn]o\s+(?:de\s+(?:la\s+)?)?muestra|tama[ñn]o\s+muestral|n[úu]mero\s+de\s+(?:observaciones|ensayos|muestras))\b",
            re.IGNORECASE,
        ),
    ),
    (
        "estadístico_Z",
        re.compile(
            r"\b(?:estad[íi]stico\s+(?:de\s+prueba\s+)?[zt]|valor\s+cr[íi]tico\s+[zt]|(?:puntaje|puntuaci[óo]n)\s+z)\b",
            re.IGNORECASE,
        ),
    ),
]


def detect_frankenstein_sum(stem: str) -> Optional[Tuple[str, str]]:
    """Detect artificial sums or composite indices combining incompatible statistical units in a stem."""
    if not stem:
        return None
    clean_stem = re.sub(r"\$\$[\s\S]*?\$\$|\$[^\$]*?\$", " ", str(stem))
    sentences = re.split(r"[.?!;\n]+", clean_stem)
    for sent in sentences:
        m = _FRANKENSTEIN_SUM_TRIGGER_RE.search(sent)
        if not m:
            continue
        post_trigger = sent[m.start():]
        matched = [name for name, pat in _FRANKENSTEIN_UNIT_GROUPS if pat.search(post_trigger)]
        if len(matched) < 2 and re.search(
            r"\b(?:ambos|ambas|dichos|dichas|estas\s+magnitudes|su\s+suma)\b",
            post_trigger,
            re.IGNORECASE,
        ):
            matched = [name for name, pat in _FRANKENSTEIN_UNIT_GROUPS if pat.search(sent)]
        if len(matched) >= 2:
            return matched[0], matched[1]
    return None


def _atomic_write_json(target_path: Path, data: Any) -> None:
    """Safely write JSON payload to file using atomic rename to prevent race conditions."""
    data = heal_control_chars_in_obj(data)
    target_path = Path(target_path).resolve()
    target_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = target_path.with_name(f".{target_path.name}.tmp.{os.getpid()}_{uuid.uuid4().hex[:8]}")
    if target_path.parent.name == "templates":
        payload_str = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    else:
        payload_str = json.dumps(data, indent=2, ensure_ascii=False)
    tmp_path.write_text(payload_str, encoding="utf-8")
    try:
        os.replace(tmp_path, target_path)
    except Exception:
        try:
            if target_path.is_file():
                target_path.unlink()
            os.replace(tmp_path, target_path)
        except Exception:
            target_path.write_text(payload_str, encoding="utf-8")
            if tmp_path.is_file():
                try:
                    tmp_path.unlink()
                except Exception:
                    pass




try:
    import pykatex as _pykatex
except ImportError:  # optional dependency: warn-only check is skipped when absent
    _pykatex = None

_PYKATEX_SPAN_RE = re.compile(r"(?<!\\)\$\$(.+?)(?<!\\)\$\$|(?<!\\)\$(.+?)(?<!\\)\$", re.DOTALL)
_PYKATEX_VAR_RE = re.compile(r"@[a-zA-Z0-9_]+@")


def pykatex_warnings(text: Any, context: str, whole_is_math: bool = False) -> List[str]:
    """Warn-only KaTeX render check (PyKaTeX). Never fails the compile.

    Template placeholders @var@ are replaced by '1' before rendering. Set C2C_PYKATEX=off to disable.
    """
    if _pykatex is None or not isinstance(text, str) or not text.strip():
        return []
    if os.environ.get("C2C_PYKATEX", "").lower() == "off":
        return []
    spans: List[Tuple[str, bool]] = []
    if whole_is_math and "$" not in text:
        spans.append((text, False))
    else:
        for m in _PYKATEX_SPAN_RE.finditer(text):
            if m.group(1) is not None:
                spans.append((m.group(1), True))
            else:
                spans.append((m.group(2), False))
    out: List[str] = []
    for span, display in spans:
        probe = _PYKATEX_VAR_RE.sub("1", span).strip()
        if not probe:
            continue
        try:
            strict_mode = getattr(_pykatex, "STRICT_ERROR", "error")
            _pykatex.renderToString(probe, display, strict=strict_mode)
        except Exception as exc:
            raw_msg = str(exc)
            col = None
            m_pos = re.search(r"position\s+(\d+)", raw_msg, re.IGNORECASE)
            if m_pos:
                col = m_pos.group(1)
            elif "\u0332" in raw_msg:
                colon_idx = raw_msg.rfind(":")
                snippet = raw_msg[colon_idx + 1:] if colon_idx != -1 else raw_msg
                clean_before = snippet[:snippet.find("\u0332")].replace("\u0332", "")
                col = str(len(clean_before))
            col_info = f" [col={col}]" if col is not None else ""
            msg = raw_msg.replace("\u0332", "^").strip().splitlines()[0]
            out.append(f"[!] Warning: [PYKATEX-WARN] {context}: {msg}{col_info} (span: {span!r})")
    return out


def heal_shard_source_text(source_text: str) -> Tuple[bool, str]:
    """Uses Python's tokenize module to inspect and heal non-raw string tokens and control characters in-memory.

    Heals unescaped LaTeX prefixes and ASCII control characters without modifying files on disk.
    Returns (modified, healed_text).
    """
    if not source_text:
        return False, source_text
    try:
        import io, tokenize
        clean_source = source_text.replace("\r\n", "\n")
        modified = (clean_source != source_text)
        tokens = list(tokenize.tokenize(io.BytesIO(clean_source.encode("utf-8")).readline))
        new_tokens = []
        for t in tokens:
            if t.type == tokenize.STRING:
                m = re.match(r"^([a-zA-Z]*)('''|\"\"\"|'|\")(.*)\2$", t.string, flags=re.DOTALL)
                if m:
                    prefix, q_delim, body = m.groups()
                    q_open = q_close = q_delim
                    is_raw = "r" in prefix.lower()
                    new_body = heal_control_chars_in_str(body)
                    if not is_raw:
                        new_body = re.sub(rf"(?<!\\)\\({COMBINED_LATEX})", r"\\\\\1", new_body)
                    else:
                        new_body = re.sub(r"(?<!\\)(?:\\\\)+([a-zA-Z]+)", r"\\\1", new_body)
                    if "$" in new_body:
                        _bs = r"\\" if is_raw else r"\\\\"
                        new_body = re.sub(r"(?<!\\)\\+centernot\s*\{?\s*\\+(?:Rightarrow|implies)\b\s*\}?", f"{_bs}nRightarrow", new_body)
                        new_body = re.sub(r"(?<!\\)\\+implies\b", f"{_bs}Rightarrow", new_body)
                        new_body = re.sub(r"(?<!\\)\\+iff\b", f"{_bs}Leftrightarrow", new_body)
                        new_body = re.sub(r"(?<!\\)\b(hat|bar|tilde|vec|dot|ddot|frac|dfrac|tfrac|sqrt|mathcal|mathbb|mathbf|boldsymbol|operatorname)\s*\{", rf"{_bs}\1{{", new_body)
                        if new_body.count("$$") == 1 and new_body.replace("$$", "").count("$") == 1:
                            new_body = new_body.replace("$$", "$")
                    if new_body != body:
                        modified = True
                        new_tokens.append(tokenize.TokenInfo(t.type, f"{prefix}{q_open}{new_body}{q_close}", t.start, t.end, t.line))
                        continue
            new_tokens.append(t)
        if not modified:
            return False, source_text
        rebuilt_text = tokenize.untokenize(new_tokens).decode("utf-8")
        return True, rebuilt_text
    except Exception:
        try:
            healed = heal_control_chars_in_str(source_text)
            has_raw = bool(re.search(r'\br["\']', source_text, re.IGNORECASE))
            if not has_raw:
                healed = re.sub(rf"(?<!\\)\\({COMBINED_LATEX})", r"\\\\\1", healed)
            return (healed != source_text), healed
        except Exception:
            return False, source_text


def heal_shard_source_file(py_path: Path) -> bool:
    """Uses Python's tokenize module to inspect and heal non-raw string tokens and control characters.

    Heals unescaped LaTeX prefixes and ASCII control characters in py_path before importing.
    Returns True if the file was modified and rewritten, False otherwise.
    """
    if not py_path.is_file():
        return False
    source_text = py_path.read_text(encoding="utf-8")
    modified, healed = heal_shard_source_text(source_text)
    if modified:
        py_path.write_text(healed.replace("\r\n", "\n"), encoding="utf-8", newline="\n")
    return modified


_parenthetical_telltale_re = re.compile(
    r"\(\s*(?:confusi[oó]n|error|omisi[oó]n|sesgo|falsamente|definici[oó]n\s+err[oó]nea|desplazamiento\s+err[oó]neo|c[aá]lculo\s+err[oó]neo)[^)]*\)",
    re.IGNORECASE,
)
_telltale_patterns = [
    re.compile(r"\b(err[oó]neamente|incorrectamente|falsamente)\b", re.IGNORECASE),
    re.compile(r"\b(derivada\s+err[oó]nea|f[oó]rmula\s+err[oó]nea|c[aá]lculo\s+err[oó]neo)\b", re.IGNORECASE),
    re.compile(r"\b(omitiendo\s+(elevar|multiplicar|dividir|sumar|restar))\b", re.IGNORECASE),
    re.compile(r"\b(confundiendo\s+con|al\s+rev[eé]s)\b", re.IGNORECASE),
    re.compile(r"\b(factorizando\s+err[oó]neamente|con\s+signos\s+positivos\s+incorrectos)\b", re.IGNORECASE),
]
_synthetic_prefix_re = re.compile(r"^\s*(?:Opci[oó]n|Alternativa|Variante)\s+(?:alterna\s+)?\d+\s*:?", re.IGNORECASE)


def parse_katex_number(val: Any) -> float:
    """Robustly parse a float from strings containing LaTeX formatting, delimiters, percentages, inequalities or macros."""
    if isinstance(val, (int, float)):
        return float(val)
    if not isinstance(val, str):
        val = str(val)
    s = val.replace(r"\le", "=").replace(r"\ge", "=").replace(r"\approx", "=").replace("<=", "=").replace(">=", "=")
    # Strip LaTeX formatting macros like \mathbf{...}, \operatorname{...}, \frac, etc.
    s = re.sub(r"\\[a-zA-Z]+", "", s)
    s = s.replace("$", "").replace(r"\%", "").replace("%", "").replace("{", "").replace("}", "").replace("\\", "").strip()
    s = s.split("=")[-1].strip()
    m = re.findall(r"-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?", s)
    if m:
        return float(m[-1])
    return float(s)



def _find_telltale_in_option(text: Any, is_distractor: bool = True) -> Optional[str]:
    """Find parenthetical cues, distractor confessions, or synthetic clone prefixes in option text."""
    if not isinstance(text, str) or not text.strip():
        return None
    m_pt = _parenthetical_telltale_re.search(text)
    if m_pt:
        return m_pt.group(0)
    if is_distractor:
        for p in _telltale_patterns:
            m_p = p.search(text)
            if m_p:
                return m_p.group(0)
        m_syn = _synthetic_prefix_re.search(text)
        if m_syn:
            return m_syn.group(0)
    return None


def is_trivial_verifier(ver_code: str, ver_fn_callable: Any = None) -> Tuple[bool, str]:
    """Inspect AST of verifier code to reject trivial verifiers like constant 'return True'."""
    if not ver_code or not ver_code.strip():
        return True, "verifier code is empty"
    clean_ver_code = textwrap.dedent(ver_code.strip())
    try:
        tree = ast.parse(clean_ver_code)
    except Exception as e:
        return True, f"verifier code syntax error: {e}"

    fn_node = None
    target_names = {"verify", "cross_check"}
    if ver_fn_callable and hasattr(ver_fn_callable, "__name__"):
        target_names.add(ver_fn_callable.__name__)

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name in target_names:
                fn_node = node
                break
    if not fn_node:
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                fn_node = node
                break

    if not fn_node:
        return True, "no function definition found in verifier code"

    body_stmts = [
        s for s in fn_node.body
        if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant) and isinstance(s.value.value, str))
    ]

    if not body_stmts:
        return True, "verifier function body has no operational statements"

    # Single return constant (e.g. return True, return 1, or return None)
    if len(body_stmts) == 1 and isinstance(body_stmts[0], ast.Return):
        ret_val = body_stmts[0].value
        if isinstance(ret_val, ast.Constant):
            return True, f"returns constant '{ret_val.value}' without evaluating conditions"
        if ret_val is None:
            return True, "returns None without evaluating conditions"

    # Check if arguments (instance / cand, v) are ever loaded in operational statements
    arg_names = [a.arg for a in (getattr(fn_node.args, "posonlyargs", []) + fn_node.args.args + getattr(fn_node.args, "kwonlyargs", []))]
    if arg_names:
        used_arg = False
        for s in body_stmts:
            for sub in ast.walk(s):
                if isinstance(sub, ast.Name) and sub.id in arg_names and isinstance(sub.ctx, ast.Load):
                    used_arg = True
                    break
            if used_arg:
                break
        if not used_arg:
            return True, f"arguments {arg_names} are never inspected in verifier function body"

    return False, ""


def normalize_double_braces(text: str, declared_vars: Optional[Set[str]] = None) -> str:
    r"""Normalize non-variable double curly braces {{token}} -> {token} when token is not a declared variable.

    Protects declared variables so that {var} can still be evaluated, while ensuring LaTeX braces like
    {{0.5}}, {{\operatorname{arccot}}}, {{S_{xy}}} are normalized to {0.5}, {\operatorname{arccot}}, {S_{xy}}
    before R-20 validation.
    """
    if not isinstance(text, str) or "{{" not in text:
        return text

    v_set = declared_vars or set()

    def _normalize_once(s: str) -> str:
        out = []
        i = 0
        n = len(s)
        while i < n:
            if s[i:i+2] == "{{":
                j = i + 2
                depth = 0
                found = False
                while j < n:
                    if s[j:j+2] == "}}" and depth == 0:
                        found = True
                        break
                    elif s[j] == "{":
                        depth += 1
                        j += 1
                    elif s[j] == "}":
                        if depth > 0:
                            depth -= 1
                            j += 1
                        else:
                            break
                    else:
                        j += 1

                if found:
                    token = s[i+2:j]
                    var_name = token.strip().split(":")[0].strip()
                    if v_set and var_name in v_set:
                        out.append(s[i:j+2])
                    else:
                        out.append("{" + token + "}")
                    i = j + 2
                else:
                    out.append(s[i])
                    i += 1
            else:
                out.append(s[i])
                i += 1
        return "".join(out)

    prev = None
    curr = text
    while prev != curr:
        prev = curr
        curr = _normalize_once(curr)
    return curr


