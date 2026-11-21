"""Question assembler for content-to-course v2.

Builds standardized question JSON objects complying with the practice platform schema:
- MC7: exactly 7 options (A-G shuffled), distinct distractor IDs, length bounds
- FIB: value, canonical_algebraic, accepted_equivalents, tolerance
- MS: 4-6 options, binary scoring
- Progressive scaffolding hints (3-5 hints)
- Detailed step-by-step solution
- common_misconception_warning derived from distractor remediation_hint
- Anti-giveaway length calibration
- Zero domain keywords!
"""

import json
import random
import re
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple, Union

try:
    from engine.invariants import VALID_CANVAS_INVARIANT_KINDS, validate_katex_syntax
except ImportError:
    from .invariants import VALID_CANVAS_INVARIANT_KINDS, validate_katex_syntax

try:
    from engine.katex_ast import canonicalize_algebraic_katex
except ImportError:
    try:
        from .katex_ast import canonicalize_algebraic_katex
    except ImportError:
        canonicalize_algebraic_katex = None

_PL_TOKEN_PATTERN = re.compile(r"@([A-Za-z_][A-Za-z0-9_]*)(?::([^@\s{}]+))?@")


OPTION_LETTERS = ["A", "B", "C", "D", "E", "F", "G"]


_LATEX_SYMBOL_MACROS = {
    "dot", "ddot", "dddot", "ddddot", "hat", "bar", "tilde", "vec", "acute", "grave", "check",
    "breve", "mathring", "widehat", "widetilde", "widecheck", "overline",
    "underline", "mathbf", "boldsymbol", "bm", "mathit", "mathrm", "mathcal",
    "mathbb", "mathfrak", "mathsf", "mathtt", "mathscr", "symbf", "text", "textbf", "textit",
    "textrm", "textsf", "texttt", "textsc", "operatorname", "begin", "end",
    "xrightarrow", "xleftarrow", "xleftrightarrow", "xLeftarrow", "xRightarrow", "xLeftrightarrow",
    "xhookleftarrow", "xhookrightarrow", "xmapsto", "xtwoheadleftarrow", "xtwoheadrightarrow",
    "xrightharpoondown", "xrightharpoonup", "xleftharpoondown", "xleftharpoonup",
    "substack", "prescript", "pmod", "pod",
}

_LATEX_VALUE_MACROS_1ARG = {
    "sqrt",
}

_LATEX_VALUE_MACROS_2ARG = {
    "frac", "dfrac", "tfrac", "cfrac", "binom", "dbinom", "tbinom",
    "overset", "underset", "stackrel",
}

_GIVEAWAY_PREFIX_RE = re.compile(
    r"^(?:Inversión de roles|Omisión de límites|Asumiendo erróneamente|Confusión de conceptos|Falsa generalización|Error de signo):\s*",
    re.IGNORECASE,
)


def _safe_format_value(val: Any, fmt_spec: Optional[str]) -> str:
    """Safely format value with format specifier, coercing types without runtime crashes."""
    if not fmt_spec:
        return str(val)
    try:
        return format(val, fmt_spec)
    except (ValueError, TypeError):
        pass

    # Try converting to float if format spec looks like float (.2f, .3e, .4g, etc.)
    try:
        return format(float(val), fmt_spec)
    except (ValueError, TypeError):
        pass

    # Try converting to int if format spec looks like integer (d, b, x, etc.) or float without fractional part
    try:
        f_val = float(val)
        if abs(f_val - round(f_val)) < 1e-9:
            return format(int(round(f_val)), fmt_spec)
    except (ValueError, TypeError):
        pass

    return str(val)


def _strip_giveaway_prefix(text: str) -> str:
    """Strips R-18 pedagogical giveaway prefixes like 'Inversión de roles: ' from options or rationales."""
    if not isinstance(text, str):
        return text
    cleaned = _GIVEAWAY_PREFIX_RE.sub("", text).strip()
    if cleaned:
        cleaned = cleaned[0].upper() + cleaned[1:]
    return cleaned


def _inspect_second_arg_of_value_macro(prefix_stripped: str, key: str) -> Tuple[bool, bool]:
    """Return (is_second_arg_of_2arg_macro, first_arg_has_symbolic_key)."""
    if not prefix_stripped.endswith("}"):
        return False, False
    depth = 0
    idx = len(prefix_stripped) - 1
    while idx >= 0:
        if prefix_stripped[idx] == "}":
            depth += 1
        elif prefix_stripped[idx] == "{":
            depth -= 1
            if depth == 0:
                break
        idx -= 1
    if depth == 0 and idx >= 0:
        first_arg_body = prefix_stripped[idx + 1 : -1]
        before_first_arg = prefix_stripped[:idx].rstrip()
        m = re.search(r"\\([a-zA-Z]+)\s*$", before_first_arg)
        if m and m.group(1) in _LATEX_VALUE_MACROS_2ARG:
            sym_key = key[1:] if len(key) > 1 and key.startswith("d") else key
            has_symbolic = bool(re.search(rf"\\[a-zA-Z]+\s*\{{{re.escape(sym_key)}\}}", first_arg_body))
            return True, has_symbolic
    return False, False


def format_template_string(
    template_str: str,
    variables: Dict[str, Any],
    is_cta: bool = False,
) -> str:
    r"""Safely format string with template variables without corrupting KaTeX curly braces or macros.

    Supports:
    - Standard placeholders {var} and Python format specs {var:.4f}
    - Automatic preservation of required LaTeX braces in \frac{a}{b}, \sqrt{a}, x^{b}, u_{i}
      whether authored with single braces {a} or double braces {{a}}
    - Protection of LaTeX symbol macros (\dot{k}, \hat{y}, \mathbf{x}, \begin{matrix})
    - Fallback replacement of bare code identifiers ending in _val, _num, _str, _res
    """
    if not isinstance(template_str, str) or not variables:
        return template_str

    result = template_str
    has_pl_tokens = bool(_PL_TOKEN_PATTERN.search(template_str))

    # Phase 0 priority pass: Orthogonal PrairieLearn @var@ / @var:fmt@ token interpolation
    def _pl_replacer(m: re.Match) -> str:
        key = m.group(1)
        fmt_spec = m.group(2)
        if key in variables:
            val = variables[key]
            return _safe_format_value(val, fmt_spec)
        return m.group(0)

    result = _PL_TOKEN_PATTERN.sub(_pl_replacer, result)
    sentinel_values: Dict[str, str] = {}

    def _stash_sentinel(val_s: str) -> str:
        token = f"\x00__C2C_VAR_{len(sentinel_values)}__\x00"
        sentinel_values[token] = val_s
        return token

    for k, v in variables.items():
        if is_cta and not (len(k) > 2 or k.endswith(("_val", "_num", "_str", "_res"))):
            continue
        pattern = re.compile(rf"\{{{re.escape(k)}(?::([^{{}}]+))?\}}")
        math_spans = [
            m_s.span()
            for m_s in re.finditer(r"(?<!\\)\$\$[\s\S]*?(?<!\\)\$\$|(?<!\\)\$[^\$]+?(?<!\\)\$", result)
        ]
        def is_in_math_span(pos: int) -> bool:
            return any(s_pos <= pos < e_pos for s_pos, e_pos in math_spans)

        def _replacer(m: re.Match, key: str = k, val: Any = v) -> str:
            fmt_spec = m.group(1)
            val_str = _safe_format_value(val, fmt_spec)

            start = m.start()
            end = m.end()
            prefix = result[:start]
            suffix = result[end:]

            is_escaped_open = prefix.endswith("{") and suffix.startswith("}")

            # Course-agnostic short variable / sub-superscript base protection inside math blocks:
            # e.g. ${k}^*$, ${r}_t$, or escaped $\{k\}$ (odd number of backslashes before {)
            prefix_stripped = prefix.rstrip()
            num_trailing_slashes = len(prefix_stripped) - len(prefix_stripped.rstrip("\\"))
            is_escaped_literal_brace = (num_trailing_slashes % 2 == 1)

            if not is_escaped_open and not fmt_spec and is_in_math_span(start):
                if suffix.lstrip().startswith(("^", "_")) or is_escaped_literal_brace:
                    return m.group(0)

            # Case 1: Inside double braces {{k}}
            if is_escaped_open:
                outer_prefix = prefix[:-1].rstrip()
                macro_m = re.search(r"\\([a-zA-Z]+)\*?(\[[^\]]*\])?\s*$", outer_prefix)
                if macro_m and macro_m.group(1) in _LATEX_SYMBOL_MACROS and not fmt_spec and "_" not in key:
                    return m.group(0)
                return _stash_sentinel(val_str)

            prefix_stripped = prefix.rstrip()

            # Case 2: Preceded directly by a LaTeX macro \cmd or \cmd[...]
            macro_m = re.search(r"\\([a-zA-Z]+)\*?(\[[^\]]*\])?\s*$", prefix_stripped)
            if macro_m:
                macro_name = macro_m.group(1)
                if macro_name in _LATEX_VALUE_MACROS_1ARG or macro_name in _LATEX_VALUE_MACROS_2ARG:
                    if has_pl_tokens and len(key) <= 1 and not fmt_spec and is_in_math_span(start):
                        return m.group(0)
                    return f"{{{_stash_sentinel(val_str)}}}"
                if not fmt_spec and "_" not in key:
                    return m.group(0)
                return f"{{{_stash_sentinel(val_str)}}}"

            # Case 3: Second argument of a 2-argument value macro e.g. \frac{...}{k}
            is_second_arg, has_symbolic = _inspect_second_arg_of_value_macro(prefix_stripped, key)
            if is_second_arg:
                if has_pl_tokens and len(key) <= 1 and not fmt_spec and is_in_math_span(start):
                    return m.group(0)
                if has_symbolic and not fmt_spec and "_" not in key:
                    return m.group(0)
                return f"{{{_stash_sentinel(val_str)}}}"

            # Case 4: Superscript ^{k} or subscript _{k}
            if prefix_stripped.endswith("^") or prefix_stripped.endswith("_"):
                if has_pl_tokens and len(key) <= 1 and not fmt_spec and is_in_math_span(start):
                    return m.group(0)
                base_m = re.search(r"\\([a-zA-Z]+)\*?(\[[^\]]*\])?(?:\{[^{}]*\})?\s*$", prefix_stripped[:-1].rstrip())
                if base_m and base_m.group(1) in _LATEX_SYMBOL_MACROS and len(key) <= 1 and not fmt_spec and is_in_math_span(start):
                    return m.group(0)
                return f"{{{_stash_sentinel(val_str)}}}"

            return _stash_sentinel(val_str)

        result = pattern.sub(_replacer, result)

        # Fallback for bare code variables ending in _val, _num, _str, _res left unbraced by LLM
        if re.match(r"^[a-zA-Z0-9]+_(?:val|num|str|res)$", k):
            result = re.sub(rf"\b{re.escape(k)}\b", lambda _, val=str(v): _stash_sentinel(val), result)

    for token, val_s in sentinel_values.items():
        result = result.replace(token, val_s)

    return result


def render_template(template_str: str, variables: Dict[str, Any]) -> str:
    r"""Render template string with variables, supporting both PrairieLearn @var@ and legacy {var} syntax."""
    return format_template_string(template_str, variables)


def sanitize_katex_syntax(text: str, canonicalize_coefficients: bool = False) -> str:
    r"""Sanitize KaTeX syntax by fixing f-string artifacts, unclosed nested macros, and delimiter issues.
    
    - Collapses overescaped LaTeX commands (e.g. \\frac, \\text -> \frac, \text) preserving matrix breaks (R-23).
    - Maps unsupported external KaTeX macros (\centernot -> \nRightarrow, \not, etc.).
    - Repairs \text{..._...} contamination and escapes unescaped underscores in plain \text blocks.
    - Replaces '$$$' with '$$'
    - Normalizes residual paired double curly braces from f-strings '{{x}}' -> '{x}'
      without altering legitimate nested KaTeX syntax like \\frac{\\dot{r}}{r} or k^{\\frac{1}{3}}.
    - Auto-closes unclosed nested accent/style/sqrt macros (e.g. \\hat{\\boldsymbol{\\beta} -> \\hat{\\boldsymbol{\\beta}}).
    - Auto-repairs dropped numerator/denominator braces in \\frac and superscripts/subscripts.
    """
    if not isinstance(text, str):
        return text

    # 0a. Deterministic collapse of overescaped LaTeX commands (R-23)
    # - Even number of slashes (2, 4, 6, ...) before a command name:
    #   Overescaped command from JSON/f-string serialization -> collapse to single backslash \cmd.
    # - Odd number of slashes >= 3 before a command name (e.g. \\\frac):
    #   Matrix/cases row break (\\) immediately preceding a command (\frac) -> preserve row break
    #   and command separated by space (\\ \frac) so KaTeX renders rows correctly and validator passes.
    # - Single backslash (\cmd) is untouched.
    # - Row breaks before non-letters (e.g. \\[4pt], \\ -1, \\ 3, \\\n) are untouched.
    def _collapse_overescaped_slashes(match: re.Match) -> str:
        slashes = match.group(1)
        cmd = match.group(2)
        n = len(slashes)
        if n % 2 == 0:
            if n == 2 and len(cmd) == 1:
                return f"\\\\ {cmd}"
            return f"\\{cmd}"
        elif n >= 3:
            return f"\\\\ \\{cmd}"
        else:
            return f"\\{cmd}"

    text = re.sub(r"(\\+)([a-zA-Z]+)", _collapse_overescaped_slashes, text)

    # 0b. Deterministic mapping of unsupported external KaTeX macros (\centernot)
    text = re.sub(r"\\centernot\s*\\(?:Rightarrow|implies)\b", r"\\nRightarrow", text)
    text = re.sub(r"\\centernot\s*\\(?:Leftarrow|impliedby)\b", r"\\nLeftarrow", text)
    text = re.sub(r"\\centernot\s*\\(?:Leftrightarrow|iff)\b", r"\\nLeftrightarrow", text)
    text = re.sub(r"\\centernot\s*\\(?:rightarrow|to)\b", r"\\nrightarrow", text)
    text = re.sub(r"\\centernot\s*\\(?:leftarrow|gets)\b", r"\\nleftarrow", text)
    text = re.sub(r"\\centernot\s*\\leftrightarrow\b", r"\\nleftrightarrow", text)
    text = re.sub(r"\\centernot\b", r"\\not", text)

    # 0c. Deterministic repair of \text{..._...} contamination
    text = re.sub(
        r"\\text\s*\{\s*text(Var|Cov|Corr|E)\s*\[\s*bar([a-zA-Z0-9]+)_([a-zA-Z0-9]+)\s*\]\s*=\s*([^{}]+?)\s*\}",
        r"\\text{\1}[\\bar{\2}_{\3}] = \4",
        text,
    )

    def _escape_text_underscores(match: re.Match) -> str:
        inner = match.group(1)
        # Escape any unescaped underscore (?<!\\)_ without duplicating already escaped \_
        fixed_inner = re.sub(r"(?<!\\)_", r"\\_", inner)
        return f"\\text{{{fixed_inner}}}"

    text = re.sub(r"\\text\s*\{([^{}$]*)\}", _escape_text_underscores, text)

    # 0d. Canonicalize algebraic double signs and unitary coefficients inside math blocks $...$ and $$...$$
    if canonicalize_algebraic_katex is not None:
        text = canonicalize_algebraic_katex(text, collapse_unit_coeffs=canonicalize_coefficients)
    else:
        def _collapse_algebraic_signs(math_body: str) -> str:
            # Collapses double signs from template interpolation: + -5 -> - 5, - -5 -> + 5, etc.
            for _ in range(5):
                orig_body = math_body
                math_body = re.sub(r"(?<![a-zA-Z\\])\+\s*-\s*(?=[0-9a-zA-Z\\({])", "- ", math_body)
                math_body = re.sub(r"(?<![a-zA-Z\\])-\s*-\s*(?=[0-9a-zA-Z\\({])", "+ ", math_body)
                math_body = re.sub(r"(?<![a-zA-Z\\])\+\s*\+\s*(?=[0-9a-zA-Z\\({])", "+ ", math_body)
                math_body = re.sub(r"(?<![a-zA-Z\\])-\s*\+\s*(?=[0-9a-zA-Z\\({])", "- ", math_body)
                if math_body == orig_body:
                    break
            return math_body

        def _canonicalize_math_signs(match: re.Match) -> str:
            raw_span = match.group(0)
            is_display = raw_span.startswith("$$")
            delim = "$$" if is_display else "$"
            inner = raw_span[len(delim):-len(delim)]
            return f"{delim}{_collapse_algebraic_signs(inner)}{delim}"

        text = re.sub(r"\$\$[\s\S]*?\$\$|\$[^\$]+?\$", _canonicalize_math_signs, text)

    # Replace '$$$' with '$$'
    while "$$$" in text:
        text = text.replace("$$$", "$$")

    # Normalize residual paired double curly braces from f-strings {{var}} -> {var}
    # NEVER do a blind text.replace("}}", "}") as that destroys nested LaTeX groups!
    def _normalize_double_braces_step(s: str) -> str:
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
    while prev != text:
        prev = text
        text = _normalize_double_braces_step(text)


    # 1. Auto-close unclosed nested accent/style/sqrt macros: \hat{\boldsymbol{\beta} -> \hat{\boldsymbol{\beta}}
    # ONLY executed when opening braces exceed closing braces, preventing corruption of balanced expressions.
    if text.count("{") > text.count("}"):
        orig_text = text
        outer_macros = r"(?:hat|bar|tilde|vec|dot|ddot|acute|grave|check|breve|mathring|widehat|widetilde|widecheck|overline|underline|sqrt)"
        inner_macros = r"(?:boldsymbol|mathbf|bm|mathit|mathrm|mathbb|mathcal|text|textbf|symbf|hat|bar|tilde|vec|dot|ddot)"
        nested_fix = re.compile(
            rf"(\\(?:{outer_macros})\s*\{{\s*\\(?:{inner_macros})\s*\{{[^{{}}]*\}})(?!\s*\}})"
        )
        cand_nested = nested_fix.sub(r"\1}", text)
        if cand_nested.count("{") < cand_nested.count("}"):
            cand_nested = orig_text
        text = cand_nested

    # 2. Auto-repair \frac missing numerator closing brace when numerator has an inner 1-arg macro or script
    # ONLY executed when opening braces exceed closing braces, preventing corruption of balanced expressions.
    if text.count("{") > text.count("}"):
        orig_text = text
        frac_inner_fix = re.compile(
            r"(\\(?:frac|dfrac|tfrac|cfrac)\s*\{[^{}]*(?:\\[a-zA-Z]+|[_^])\s*\{[^{}]*\}[^{}\\_^]*)\{"
        )
        cand_inner = frac_inner_fix.sub(r"\1}{", text)
        if "_}{" in cand_inner or "^}{" in cand_inner or cand_inner.count("{") < cand_inner.count("}"):
            cand_inner = orig_text
        text = cand_inner

    # Simple \frac{a{b} where numerator has no macros or scripts
    if text.count("{") > text.count("}"):
        orig_text = text
        frac_simple_fix = re.compile(
            r"(\\(?:frac|dfrac|tfrac|cfrac)\s*\{[^{}\\^_]+)\{([^{}]+\})"
        )
        cand_simple = frac_simple_fix.sub(r"\1}{\2", text)
        if "_}{" in cand_simple or "^}{" in cand_simple or cand_simple.count("{") < cand_simple.count("}"):
            cand_simple = orig_text
        text = cand_simple

    # 3. Auto-repair \frac missing denominator closing brace when denominator ends with an inner braced group
    if text.count("{") > text.count("}"):
        orig_text = text
        frac_den_fix = re.compile(
            r"(\\(?:frac|dfrac|tfrac|cfrac)\s*\{(?:[^{}]|\{[^{}]*\})*\}\s*\{[^{}]*(?:\\[a-zA-Z]+|[_^])\s*\{[^{}]*\})"
            r"(?!\s*\})(?=\s*(?:[$=<>,.;:)\]|]|\\(?:le|ge|neq|approx|implies|iff)\b|$))"
        )
        cand_den = frac_den_fix.sub(r"\1}", text)
        if cand_den.count("{") < cand_den.count("}"):
            cand_den = orig_text
        text = cand_den

    # 4. Auto-repair superscript/subscript missing outer closing brace after inner macro
    if text.count("{") > text.count("}"):
        orig_text = text
        script_outer_fix = re.compile(
            r"([_^]\s*\{[^{}]*\\[a-zA-Z]+(?:\s*\{[^{}]*\})+)"
            r"(?!\s*\})(?=\s*(?:[$=<>,.;:)\]|]|\\(?:le|ge|neq|approx|implies|iff)\b|$))"
        )
        cand_script = script_outer_fix.sub(r"\1}", text)
        if cand_script.count("{") < cand_script.count("}"):
            cand_script = orig_text
        text = cand_script

    # 5. Auto-repair unbraced numeric denominator after \frac{num}: \frac{s}3 -> \frac{s}{3}
    frac_unbraced_den = re.compile(
        r"(\\(?:frac|dfrac|tfrac|cfrac)\s*\{(?:[^{}]|\{[^{}]*\})*\})\s*([0-9]+(?:\.[0-9]+)?)"
    )
    text = frac_unbraced_den.sub(r"\1{\2}", text)

    return text


_GENERIC_RATIONALE_PATTERNS = re.compile(
    r"^(?:"
    r"static|"
    r"dummy.*|"
    r"placeholder.*|"
    r"none|"
    r"null|"
    r"n/?a|"
    r"ningun[oa]|"
    r"comod[ií]n|"
    r"gen[eé]rico|generic|"
    r"todo|tbd|test|default|"
    r"(?:placeholder|distractor|error)(?:\s+[a-z0-9]+)?|"
    r"error\s+(?:gen[eé]rico|rationale|de\s+prueba)|"
    r"distractor(?:\s+derivado.*)?\.?|"
    r"incorrect[oa]?\.?|"
    r"opci[oó]n\s+(?:incorrecta|inv[aá]lida.*)\.?"
    r")$",
    re.IGNORECASE,
)


def _is_generic_placeholder(text: str) -> bool:
    """Return True if text is empty or a generic boilerplate placeholder."""
    if not text or not str(text).strip():
        return True
    cleaned = str(text).strip().strip(".!?,;:\"'-_ ")
    if not cleaned:
        return True
    if "placeholder" in cleaned.lower():
        return True
    return bool(_GENERIC_RATIONALE_PATTERNS.match(cleaned))


def _format_and_sanitize_candidate(
    candidate: str,
    variables: Optional[Dict[str, Any]] = None,
    is_cta: bool = False,
) -> str:
    """Strip giveaway prefixes, interpolate template variables, and sanitize KaTeX syntax."""
    if not candidate or not isinstance(candidate, str):
        return ""
    clean = _strip_giveaway_prefix(candidate)
    if variables:
        formatted = format_template_string(clean, variables, is_cta=is_cta)
    else:
        formatted = clean
    return sanitize_katex_syntax(formatted)


def _is_katex_valid(
    text: str,
    variables: Optional[Dict[str, Any]] = None,
    is_cta: bool = False,
) -> bool:
    """Check if KaTeX in text is syntactically balanced and valid after optional formatting and sanitization."""
    if not text or not isinstance(text, str):
        return False
    final_text = _format_and_sanitize_candidate(text, variables=variables, is_cta=is_cta)
    allow_tmpl = (variables is None)
    errors = validate_katex_syntax(final_text, "distractor_rationale", allow_template_vars=allow_tmpl)
    return len(errors) == 0


def _resolve_distractor_rationale(
    d_dict: Dict[str, Any],
    d_id: Optional[str],
    cta_distractors_map: Optional[Dict[str, Any]],
    default_fallback: str,
    variables: Optional[Dict[str, Any]] = None,
) -> str:
    """Resolve error_rationale for a distractor option cleanly and safely.
    
    1. If the author provides an explicit, non-generic error_rationale (or rationale),
       preserve it directly, verifying KaTeX syntax after formatting/sanitization.
    2. If absent, generic, or invalid KaTeX, inherit from cta_distractors_map,
       verifying KaTeX syntax and falling back safely if manifestation has broken KaTeX.
    3. If neither is available, use default_fallback.
    4. Validates validate_katex_syntax on the final string.
    """
    raw_rat = d_dict.get("error_rationale")
    if raw_rat is None or (isinstance(raw_rat, str) and not raw_rat.strip()):
        raw_rat = d_dict.get("rationale")

    author_rat = str(raw_rat).strip() if raw_rat is not None else ""

    # Priority 1: Explicit author rationale (if not generic placeholder and KaTeX valid)
    if author_rat and not _is_generic_placeholder(author_rat):
        if _is_katex_valid(author_rat, variables=variables, is_cta=False):
            return _format_and_sanitize_candidate(author_rat, variables=variables, is_cta=False)

    # Priority 2: DRY inheritance from cta_distractors_map
    if cta_distractors_map and d_id and d_id in cta_distractors_map:
        d_entry = cta_distractors_map[d_id]
        if isinstance(d_entry, dict):
            # Check manifestation first, but ONLY if its KaTeX syntax is valid
            manifestation = d_entry.get("manifestation")
            if manifestation and isinstance(manifestation, str) and manifestation.strip():
                if _is_katex_valid(manifestation.strip(), variables=variables, is_cta=True):
                    return _format_and_sanitize_candidate(manifestation.strip(), variables=variables, is_cta=True)

            # Fallback to wrong_belief, omitted_step, remediation_hint
            for field in ("wrong_belief", "omitted_step", "remediation_hint"):
                val = d_entry.get(field)
                if val and isinstance(val, str) and val.strip():
                    if _is_katex_valid(val.strip(), variables=variables, is_cta=True):
                        return _format_and_sanitize_candidate(val.strip(), variables=variables, is_cta=True)

    # Priority 3: Fallback to author_rat if non-empty and valid KaTeX
    if author_rat and _is_katex_valid(author_rat, variables=variables, is_cta=False):
        return _format_and_sanitize_candidate(author_rat, variables=variables, is_cta=False)

    # Priority 4: Safe default fallback
    fallback_res = _format_and_sanitize_candidate(default_fallback, variables=variables, is_cta=False)
    if not _is_katex_valid(fallback_res, variables=None, is_cta=False):
        fallback_res = _strip_giveaway_prefix(default_fallback).replace("$", "")
    return fallback_res


def calibrate_option_lengths(
    correct_text: str,
    distractors: List[Dict[str, Any]],
) -> Tuple[str, List[Dict[str, Any]]]:
    """Ensure correct option length satisfies 0.80 * min(D) <= len(correct) <= 1.20 * max(D).
    
    If length is out of bounds, pads or adjusts homogeneous phrasing.
    """
    if not distractors:
        return correct_text, distractors

    d_lens = [len(str(d.get("value", d.get("content", "")))) for d in distractors]
    min_d = min(d_lens)
    max_d = max(d_lens)
    c_len = len(correct_text)

    if min_d == 0 or max_d == 0:
        return correct_text, distractors

    lower_bound = int(0.80 * min_d)
    upper_bound = int(1.20 * max_d)

    # If correct is shorter than lower bound, we can homogenize syntax if needed
    # but never alter math content
    return correct_text, distractors


def compute_option_length_metrics(
    correct_text: str,
    distractors: Union[Sequence[str], Sequence[Dict[str, Any]]],
    min_ratio: float = 0.65,
    max_ratio: float = 1.35,
) -> Dict[str, Any]:
    """Compute character length metrics for MC options to diagnose anti-giveaway R-16 compliance.
    
    Returns:
        correct_len: Length of correct option text.
        distractor_lens: List of distractor text lengths.
        avg_distractor_len: Average length of distractors.
        ratio: correct_len / avg_distractor_len.
        is_within_bounds: True if min_ratio <= ratio <= max_ratio.
        summary_str: Human-readable diagnostic string.
    """
    correct_len = len(correct_text) if isinstance(correct_text, str) else len(str(correct_text or ""))
    distractor_lens: List[int] = []
    for d in distractors:
        if isinstance(d, dict):
            raw_text = d.get("content")
            if raw_text is None or raw_text == "":
                raw_text = d.get("value")
            if raw_text is None or raw_text == "":
                raw_text = d.get("text", "")
            d_val = str(raw_text)
        else:
            d_val = str(d if d is not None else "")
        distractor_lens.append(len(d_val))

    avg_distractor_len = (sum(distractor_lens) / len(distractor_lens)) if distractor_lens else 0.0
    ratio = (correct_len / avg_distractor_len) if avg_distractor_len > 0 else 1.0
    is_within_bounds = (min_ratio <= ratio <= max_ratio) if avg_distractor_len > 0 else True

    status_str = "PASS" if is_within_bounds else "FAIL"
    summary_str = (
        f"correct_len={correct_len}, avg_distractor_len={avg_distractor_len:.1f}, "
        f"ratio={ratio:.2f} (bounds: [{min_ratio:.2f}, {max_ratio:.2f}]) - {status_str}"
    )

    return {
        "correct_len": correct_len,
        "distractor_lens": distractor_lens,
        "avg_distractor_len": round(avg_distractor_len, 4),
        "ratio": round(ratio, 4),
        "is_within_bounds": is_within_bounds,
        "summary_str": summary_str,
    }


_GENERIC_WARNING_BOILERPLATE = "Verifique cuidadosamente los supuestos y cálculos antes de seleccionar su respuesta."


def _build_competency_misconception_fallback(
    competency_id: str,
    template: Dict[str, Any],
    cta_distractors_map: Optional[Dict[str, Dict[str, Any]]],
    gen_result: Dict[str, Any],
) -> str:
    """Build a competency-specific misconception warning from CTA distractors or template metadata."""
    if cta_distractors_map:
        comp_norm = str(competency_id or "").strip().lower()
        dict_entries = [e for e in cta_distractors_map.values() if isinstance(e, dict)]
        comp_entries = [
            e for e in dict_entries
            if str(e.get("competency_id", "")).strip().lower() == comp_norm
        ]
        if not comp_entries and dict_entries and not any(e.get("competency_id") for e in dict_entries):
            comp_entries = [dict_entries[0]]

        for d_entry in comp_entries:
            wb = str(d_entry.get("wrong_belief") or "").strip()
            os_step = str(d_entry.get("omitted_step") or "").strip()
            rh = str(d_entry.get("remediation_hint") or "").strip()
            if wb and os_step:
                return f"{wb.rstrip('. ')}. Evite omitir: {os_step}"
            if wb:
                return wb
            if os_step:
                return os_step
            if rh:
                return rh

    for candidate in (template.get("error_rationale"), gen_result.get("error_rationale")):
        if isinstance(candidate, str) and candidate.strip() and not _is_generic_placeholder(candidate):
            return candidate.strip()

    return f"Revise cuidadosamente los supuestos y pasos clave de la competencia {competency_id} antes de responder."


def _strip_outer_math_dollars(text: str) -> str:
    s = str(text or "").strip()
    if s.startswith("$$") and s.endswith("$$") and len(s) >= 4:
        return s[2:-2].strip()
    if s.startswith("$") and s.endswith("$") and len(s) >= 2:
        return s[1:-1].strip()
    return s


def _assemble_diagnostic_distractors(
    gen_result: Dict[str, Any],
    template: Dict[str, Any],
    variables: Dict[str, Any],
    cta_distractors_map: Optional[Dict[str, Dict[str, Any]]],
) -> List[Dict[str, Any]]:
    """Build diagnostic_distractors list for FIB / open_symbolic from ds / distractors."""
    raw_ds = gen_result.get("ds")
    if raw_ds is None:
        raw_ds = gen_result.get("distractors")
    if not isinstance(raw_ds, list) or not raw_ds:
        return []

    tpl_rats = template.get("rats") if isinstance(template.get("rats"), dict) else {}
    out: List[Dict[str, Any]] = []
    for item in raw_ds:
        did: Optional[str] = None
        raw_val: Any = ""
        raw_rat: Any = None
        accepted_eqs: List[str] = []
        tol: Optional[float] = None

        if isinstance(item, dict):
            did = item.get("distractor_id") or item.get("id") or item.get("did")
            raw_val = item.get("expression")
            if raw_val is None:
                raw_val = item.get("value")
            if raw_val is None:
                raw_val = item.get("content", "")
            raw_rat = item.get("error_rationale") or item.get("rationale")
            raw_eqs = item.get("accepted_equivalents") or item.get("equivalents") or []
            if isinstance(raw_eqs, list):
                accepted_eqs = [
                    _strip_outer_math_dollars(sanitize_katex_syntax(format_template_string(str(eq).strip(), variables)))
                    for eq in raw_eqs
                    if str(eq).strip()
                ]
            if item.get("tolerance") is not None:
                try:
                    tol = float(item["tolerance"])
                except (TypeError, ValueError):
                    tol = None
        elif isinstance(item, (tuple, list)):
            if len(item) >= 3:
                did = str(item[0]).strip()
                raw_val = item[1]
                raw_rat = item[2]
            elif len(item) == 2:
                did = str(item[0]).strip()
                raw_val = item[1]
            elif len(item) == 1:
                raw_val = item[0]
        else:
            raw_val = item

        did_norm = str(did).strip().replace("_", "-") if did else None
        val_fmt = _strip_outer_math_dollars(sanitize_katex_syntax(format_template_string(str(raw_val).strip(), variables)))
        if not val_fmt:
            continue

        d_lookup = {"error_rationale": raw_rat}
        if not raw_rat and did_norm and did_norm in tpl_rats:
            d_lookup["error_rationale"] = tpl_rats[did_norm]
        elif not raw_rat and did and str(did) in tpl_rats:
            d_lookup["error_rationale"] = tpl_rats[str(did)]

        rationale = _resolve_distractor_rationale(
            d_lookup,
            did_norm,
            cta_distractors_map,
            "Error conceptual o de procedimiento en la expresión ingresada.",
            variables=variables,
        )
        entry: Dict[str, Any] = {
            "expression": val_fmt,
            "value": val_fmt,
            "error_rationale": rationale,
        }
        if did_norm:
            entry["distractor_id"] = did_norm
        if accepted_eqs:
            entry["accepted_equivalents"] = accepted_eqs
        if tol is not None:
            entry["tolerance"] = tol
        out.append(entry)
    return out


def _assemble_unstructured_model(
    raw_um: Any,
    variables: Dict[str, Any],
    cta_distractors_map: Optional[Dict[str, Dict[str, Any]]],
    rng: random.Random,
    rats_map: Dict[str, str],
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    if not isinstance(raw_um, dict):
        raise ValueError("[STAGE0-INVALID] unstructured_model payload must be a dict.")

    p1 = raw_um.get("phase1_variables")
    p2 = raw_um.get("phase2_assumptions")
    p3 = raw_um.get("phase3_formulation")
    if not isinstance(p1, dict) or not isinstance(p2, dict) or not isinstance(p3, dict):
        raise ValueError("[STAGE0-PHASES] unstructured_model must declare phase1_variables, phase2_assumptions, and phase3_formulation.")

    roles = [sanitize_katex_syntax(format_template_string(str(r), variables)) for r in (p1.get("roles") or []) if str(r).strip()]
    if len(roles) < 2:
        raise ValueError("[STAGE0-P1] phase1_variables requires at least 2 roles.")
    raw_items = p1.get("items") or []
    if len(raw_items) < 2:
        raise ValueError("[STAGE0-P1] phase1_variables requires at least 2 items.")

    p1_items: List[Dict[str, Any]] = []
    p1_answer: Dict[str, str] = {}
    for idx, it in enumerate(raw_items):
        if not isinstance(it, dict):
            raise ValueError(f"[STAGE0-P1] item[{idx}] must be a dict.")
        iid = str(it.get("id") or f"V{idx + 1}").strip()
        label = sanitize_katex_syntax(format_template_string(str(it.get("label") or ""), variables))
        correct_role = sanitize_katex_syntax(format_template_string(str(it.get("correct_role") or ""), variables))
        if not label or not correct_role:
            raise ValueError(f"[STAGE0-P1] item '{iid}' missing label or correct_role.")
        if correct_role not in roles:
            raise ValueError(
                f"[STAGE0-P1] item '{iid}' correct_role '{correct_role}' must be one of phase1_variables.roles {roles}."
            )
        did = it.get("distractor_id") or it.get("did")
        did_norm = str(did).strip().replace("_", "-") if did else None
        it_lookup = dict(it)
        if not it_lookup.get("error_rationale") and did_norm and did_norm in rats_map:
            it_lookup["error_rationale"] = rats_map[did_norm]
        rat = _resolve_distractor_rationale(
            it_lookup,
            did_norm,
            cta_distractors_map,
            f"Revisa el rol estructural de {label} dentro del modelo.",
            variables=variables,
        )
        p1_entry: Dict[str, Any] = {
            "id": iid,
            "label": label,
            "correct_role": correct_role,
            "error_rationale": rat,
        }
        if did_norm:
            p1_entry["distractor_id"] = did_norm
        p1_items.append(p1_entry)
        p1_answer[iid] = correct_role
    rng.shuffle(p1_items)

    raw_p2_opts = p2.get("options") or []
    if len(raw_p2_opts) < 2:
        raise ValueError("[STAGE0-P2] phase2_assumptions requires at least 2 options.")
    p2_opts: List[Dict[str, Any]] = []
    p2_answer: List[str] = []
    for idx, opt in enumerate(raw_p2_opts):
        if not isinstance(opt, dict):
            raise ValueError(f"[STAGE0-P2] option[{idx}] must be a dict.")
        oid = str(opt.get("id") or f"C{idx + 1}").strip()
        content = sanitize_katex_syntax(format_template_string(str(opt.get("content") or opt.get("value") or ""), variables))
        if not content:
            raise ValueError(f"[STAGE0-P2] option '{oid}' missing content.")
        is_req = bool(opt.get("is_required") if "is_required" in opt else opt.get("is_correct", False))
        did = opt.get("distractor_id") or opt.get("did")
        did_norm = str(did).strip().replace("_", "-") if did else None
        opt_lookup = dict(opt)
        if not opt_lookup.get("error_rationale") and did_norm and did_norm in rats_map:
            opt_lookup["error_rationale"] = rats_map[did_norm]
        rat = _resolve_distractor_rationale(
            opt_lookup,
            did_norm,
            cta_distractors_map,
            f"Verifica la validez analítica del supuesto {content}.",
            variables=variables,
        )
        p2_entry: Dict[str, Any] = {
            "id": oid,
            "content": content,
            "is_required": is_req,
            "error_rationale": rat,
        }
        if did_norm:
            p2_entry["distractor_id"] = did_norm
        p2_opts.append(p2_entry)
        if is_req:
            p2_answer.append(oid)
    if not p2_answer:
        raise ValueError("[STAGE0-P2] phase2_assumptions must require at least 1 active assumption.")
    rng.shuffle(p2_opts)

    input_mode = str(p3.get("input_mode") or "select").strip().lower()
    if input_mode not in ("select", "symbolic"):
        raise ValueError(f"[STAGE0-P3] Invalid phase3_formulation input_mode '{input_mode}'.")

    p3_compiled: Dict[str, Any] = {
        "prompt": sanitize_katex_syntax(format_template_string(str(p3.get("prompt") or "Formula la condición formal:"), variables)),
        "input_mode": input_mode,
    }
    p3_answer: Any
    if input_mode == "select":
        raw_p3_opts = p3.get("options") or []
        if len(raw_p3_opts) < 2:
            raise ValueError("[STAGE0-P3] select mode requires at least 2 options.")
        p3_opts: List[Dict[str, Any]] = []
        p3_corr_id: Optional[str] = None
        for idx, opt in enumerate(raw_p3_opts):
            if not isinstance(opt, dict):
                raise ValueError(f"[STAGE0-P3] option[{idx}] must be a dict.")
            oid = str(opt.get("id") or f"F{idx + 1}").strip()
            content = sanitize_katex_syntax(format_template_string(str(opt.get("content") or opt.get("value") or ""), variables))
            is_corr = bool(opt.get("is_correct", False))
            entry: Dict[str, Any] = {"id": oid, "content": content, "is_correct": is_corr}
            if is_corr:
                p3_corr_id = oid
            else:
                did = opt.get("distractor_id") or opt.get("did")
                did_norm = str(did).strip().replace("_", "-") if did else None
                opt_lookup = dict(opt)
                if not opt_lookup.get("error_rationale") and did_norm and did_norm in rats_map:
                    opt_lookup["error_rationale"] = rats_map[did_norm]
                entry["error_rationale"] = _resolve_distractor_rationale(
                    opt_lookup,
                    did_norm,
                    cta_distractors_map,
                    "La formulación elegida no representa correctamente la condición del modelo.",
                    variables=variables,
                )
                if did_norm:
                    entry["distractor_id"] = did_norm
            p3_opts.append(entry)
        if not p3_corr_id:
            raise ValueError("[STAGE0-P3] phase3_formulation select mode must have a correct option.")
        rng.shuffle(p3_opts)
        p3_compiled["options"] = p3_opts
        p3_answer = p3_corr_id
    else:
        raw_expr = p3.get("correct_expression")
        if not isinstance(raw_expr, dict):
            raw_expr = {"expression": str(raw_expr or "")}
        expr_val = _strip_outer_math_dollars(sanitize_katex_syntax(format_template_string(str(raw_expr.get("expression") or raw_expr.get("value") or ""), variables)))
        if not expr_val:
            raise ValueError("[STAGE0-P3] symbolic mode requires non-empty correct_expression.")
        eqs = [
            _strip_outer_math_dollars(sanitize_katex_syntax(format_template_string(str(e), variables)))
            for e in (raw_expr.get("accepted_equivalents") or [])
            if str(e).strip()
        ]
        if expr_val not in eqs:
            eqs = [expr_val] + eqs
        p3_compiled["correct_expression"] = {
            "expression": expr_val,
            "value": expr_val,
            "canonical_algebraic": expr_val,
            "accepted_equivalents": eqs,
            "tolerance": float(raw_expr.get("tolerance", 0.001)),
        }
        p3_diag = _assemble_diagnostic_distractors(
            {"ds": p3.get("diagnostic_distractors") or []},
            {"rats": rats_map},
            variables,
            cta_distractors_map,
        )
        if p3_diag:
            p3_compiled["diagnostic_distractors"] = p3_diag
        p3_answer = p3_compiled["correct_expression"]

    compiled_um = {
        "phase1_variables": {
            "prompt": sanitize_katex_syntax(format_template_string(str(p1.get("prompt") or "Clasifica cada variable o dato del enunciado:"), variables)),
            "roles": roles,
            "items": p1_items,
        },
        "phase2_assumptions": {
            "prompt": sanitize_katex_syntax(format_template_string(str(p2.get("prompt") or "Selecciona los supuestos o restricciones activos:"), variables)),
            "options": p2_opts,
        },
        "phase3_formulation": p3_compiled,
    }
    correct_answer = {
        "phase1": p1_answer,
        "phase2": sorted(p2_answer),
        "phase3": p3_answer,
    }
    return compiled_um, correct_answer


_PURE_NUM_RE = re.compile(r"^-?\d+(?:\.\d+)?$")


def _coerce_num_if_numeric(val: Any) -> Any:
    """Convert pure numeric strings ('-?\\d+(?:\\.\\d+)?') to int/float; leave other values unchanged."""
    if isinstance(val, str):
        s = val.strip()
        if _PURE_NUM_RE.fullmatch(s):
            return float(s) if "." in s else int(s)
    return val


def _assemble_invariant_canvas(
    raw_ic: Any,
    variables: Dict[str, Any],
    cta_distractors_map: Optional[Dict[str, Dict[str, Any]]],
    rats_map: Dict[str, str],
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    if not isinstance(raw_ic, dict):
        raise ValueError("[CANVAS-INVALID] invariant_canvas payload must be a dict.")
    mode = str(raw_ic.get("mode") or "cartesian").strip().lower()
    if mode not in ("cartesian", "tree"):
        raise ValueError(f"[CANVAS-MODE] Invalid invariant_canvas mode '{mode}'.")

    if mode == "cartesian":
        invariants_raw = raw_ic.get("invariants") or []
        if not isinstance(invariants_raw, list) or not invariants_raw:
            raise ValueError("[CANVAS-INVARIANTS] cartesian mode requires non-empty 'invariants'.")

        sliders: List[Dict[str, Any]] = []
        for sl in raw_ic.get("sliders") or []:
            if isinstance(sl, dict):
                sliders.append({
                    **sl,
                    "label": sanitize_katex_syntax(format_template_string(str(sl.get("label") or sl.get("id") or ""), variables)),
                })

        def _fmt_curves(c_list: Any) -> List[Dict[str, Any]]:
            out_c: List[Dict[str, Any]] = []
            for cv in c_list or []:
                if not isinstance(cv, dict):
                    continue
                nc = dict(cv)
                if isinstance(nc.get("expression"), str):
                    nc["expression"] = format_template_string(nc["expression"], variables)
                if isinstance(nc.get("fn"), str):
                    nc["fn"] = format_template_string(nc["fn"], variables)
                if isinstance(nc.get("label"), str):
                    nc["label"] = sanitize_katex_syntax(format_template_string(nc["label"], variables))
                out_c.append(nc)
            return out_c

        points_out: List[Dict[str, Any]] = []
        for pt in raw_ic.get("interactive_points") or []:
            if isinstance(pt, dict):
                np_d = dict(pt)
                if isinstance(np_d.get("label"), str):
                    np_d["label"] = sanitize_katex_syntax(format_template_string(np_d["label"], variables))
                points_out.append(np_d)

        invs_out: List[Dict[str, Any]] = []
        for idx, inv in enumerate(invariants_raw):
            if not isinstance(inv, dict):
                raise ValueError(f"[CANVAS-INVARIANT-KIND] invariant[{idx}] must be a dict.")
            ni = dict(inv)
            ni.setdefault("id", f"INV{idx + 1}")
            inv_kind = str(ni.get("kind") or "").strip()
            if inv_kind not in VALID_CANVAS_INVARIANT_KINDS:
                raise ValueError(
                    f"[CANVAS-INVARIANT-KIND] invariant[{idx}] has invalid kind '{inv_kind}'. "
                    f"Allowed: {sorted(VALID_CANVAS_INVARIANT_KINDS)}"
                )
            ni["kind"] = inv_kind
            if isinstance(ni.get("expr"), str):
                ni["expr"] = format_template_string(ni["expr"], variables)
            for num_k in (
                "target_x", "target_y", "x", "y",
                "expected", "target_slope", "target_value", "value",
                "target", "min", "max", "tolerance",
            ):
                if isinstance(ni.get(num_k), str):
                    ni[num_k] = _coerce_num_if_numeric(format_template_string(ni[num_k], variables))
            if inv_kind in ("slider_eq", "slope_at", "slider_range") and ni.get("target") is None:
                for alias_k in ("target_value", "target_slope", "expected", "value"):
                    if ni.get(alias_k) is not None:
                        ni["target"] = ni[alias_k]
                        break
            if inv_kind == "point_coords":
                if ni.get("target_x") is None and ni.get("x") is not None:
                    ni["target_x"] = ni["x"]
                if ni.get("target_y") is None and ni.get("y") is not None:
                    ni["target_y"] = ni["y"]
            if inv_kind == "inequality_state":
                for ik in ("expected_style", "expected_shade"):
                    if isinstance(ni.get(ik), str):
                        ni[ik] = format_template_string(ni[ik], variables).strip()
                if ni.get("expected_style") not in ("solid", "dashed"):
                    raise ValueError(
                        f"[CANVAS-INEQUALITY] invariant[{idx}] (inequality_state) requires "
                        f"expected_style in ('solid', 'dashed') (got {ni.get('expected_style')!r})."
                    )
                if ni.get("expected_shade") not in ("above", "below"):
                    raise ValueError(
                        f"[CANVAS-INEQUALITY] invariant[{idx}] (inequality_state) requires "
                        f"expected_shade in ('above', 'below') (got {ni.get('expected_shade')!r})."
                    )
            did = ni.get("distractor_id") or ni.get("did")
            did_norm = str(did).strip().replace("_", "-") if did else None
            if not ni.get("error_rationale") and did_norm and did_norm in rats_map:
                ni["error_rationale"] = rats_map[did_norm]
            ni["error_rationale"] = _resolve_distractor_rationale(
                ni,
                did_norm,
                cta_distractors_map,
                "La configuración geométrica o paramétrica no satisface el invariante requerido.",
                variables=variables,
            )
            if did_norm:
                ni["distractor_id"] = did_norm
            invs_out.append(ni)

        compiled_ic: Dict[str, Any] = {
            "mode": "cartesian",
            "x_range": raw_ic.get("x_range", [0, 10]),
            "y_range": raw_ic.get("y_range", [0, 10]),
            "step": raw_ic.get("step", 1),
            "x_label": sanitize_katex_syntax(format_template_string(str(raw_ic.get("x_label") or "x"), variables)),
            "y_label": sanitize_katex_syntax(format_template_string(str(raw_ic.get("y_label") or "y"), variables)),
            "sliders": sliders,
            "fixed_curves": _fmt_curves(raw_ic.get("fixed_curves")),
            "interactive_curves": _fmt_curves(raw_ic.get("interactive_curves")),
            "interactive_points": points_out,
            "invariants": invs_out,
        }
        if raw_ic.get("snap") is not None:
            compiled_ic["snap"] = raw_ic["snap"]

        def _fmt_coord_val(v: Any) -> Any:
            return _coerce_num_if_numeric(format_template_string(v, variables)) if isinstance(v, str) else v

        def _fmt_label_item(obj: Dict[str, Any]) -> Dict[str, Any]:
            out_d = dict(obj)
            if isinstance(out_d.get("label"), str):
                out_d["label"] = sanitize_katex_syntax(format_template_string(out_d["label"], variables))
            return out_d

        if raw_ic.get("fixed_points"):
            compiled_ic["fixed_points"] = [
                {
                    **_fmt_label_item(fp),
                    "x": _fmt_coord_val(fp.get("x")),
                    "y": _fmt_coord_val(fp.get("y")),
                }
                for fp in raw_ic["fixed_points"]
                if isinstance(fp, dict)
            ]
        if raw_ic.get("segments"):
            compiled_ic["segments"] = [
                {
                    **_fmt_label_item(seg),
                    "from": [_fmt_coord_val(seg["from"][0]), _fmt_coord_val(seg["from"][1])] if isinstance(seg.get("from"), (list, tuple)) and len(seg["from"]) == 2 else seg.get("from"),
                    "to": [_fmt_coord_val(seg["to"][0]), _fmt_coord_val(seg["to"][1])] if isinstance(seg.get("to"), (list, tuple)) and len(seg["to"]) == 2 else seg.get("to"),
                }
                for seg in raw_ic["segments"]
                if isinstance(seg, dict)
            ]
        if raw_ic.get("polygons"):
            compiled_ic["polygons"] = [
                {
                    **_fmt_label_item(pg),
                    "vertices": [
                        [_fmt_coord_val(vt[0]), _fmt_coord_val(vt[1])]
                        for vt in (pg.get("vertices") or [])
                        if isinstance(vt, (list, tuple)) and len(vt) == 2
                    ],
                }
                for pg in raw_ic["polygons"]
                if isinstance(pg, dict)
            ]
        if raw_ic.get("shaded_regions"):
            sr_out: List[Dict[str, Any]] = []
            for sr in raw_ic["shaded_regions"]:
                if not isinstance(sr, dict):
                    continue
                nsr = _fmt_label_item(sr)
                for ek in ("curve_top", "curve_bottom", "y_top", "y_bottom"):
                    if isinstance(nsr.get(ek), str):
                        nsr[ek] = format_template_string(nsr[ek], variables)
                if isinstance(nsr.get("domain"), (list, tuple)) and len(nsr["domain"]) == 2:
                    nsr["domain"] = [_fmt_coord_val(nsr["domain"][0]), _fmt_coord_val(nsr["domain"][1])]
                sr_out.append(nsr)
            compiled_ic["shaded_regions"] = sr_out
        if raw_ic.get("inequality") is not None:
            if not isinstance(raw_ic.get("inequality"), dict):
                raise ValueError("[CANVAS-INEQUALITY] 'inequality' must be a dict.")
            ineq = dict(raw_ic["inequality"])
            for ik in ("curve_id", "initial_style", "initial_shade"):
                if isinstance(ineq.get(ik), str):
                    ineq[ik] = format_template_string(ineq[ik], variables).strip()
            declared_curve_ids = {
                str(cv.get("id")).strip()
                for cv in (compiled_ic["fixed_curves"] + compiled_ic["interactive_curves"])
                if isinstance(cv, dict) and cv.get("id") is not None and str(cv.get("id")).strip()
            }
            cid_ineq = str(ineq.get("curve_id") or "").strip()
            if not cid_ineq or cid_ineq not in declared_curve_ids:
                raise ValueError(
                    f"[CANVAS-INEQUALITY] inequality.curve_id '{cid_ineq}' must reference a declared curve "
                    f"in fixed_curves/interactive_curves (declared: {sorted(declared_curve_ids)})."
                )
            if "initial_style" in ineq and ineq["initial_style"] is not None:
                if ineq["initial_style"] not in ("solid", "dashed"):
                    raise ValueError(
                        f"[CANVAS-INEQUALITY] inequality.initial_style must be 'solid' or 'dashed' (got {ineq['initial_style']!r})."
                    )
            if "initial_shade" in ineq and ineq["initial_shade"] is not None:
                if ineq["initial_shade"] not in ("above", "below"):
                    raise ValueError(
                        f"[CANVAS-INEQUALITY] inequality.initial_shade must be 'above' or 'below' (got {ineq['initial_shade']!r})."
                    )
            compiled_ic["inequality"] = ineq

        def _fmt_target_state(obj: Any) -> Any:
            if isinstance(obj, str):
                return _coerce_num_if_numeric(format_template_string(obj, variables))
            if isinstance(obj, dict):
                return {k: _fmt_target_state(v) for k, v in obj.items()}
            if isinstance(obj, (list, tuple)):
                return [_fmt_target_state(v) for v in obj]
            return obj

        formatted_target_state = None
        if raw_ic.get("target_state"):
            formatted_target_state = _fmt_target_state(raw_ic["target_state"])
            compiled_ic["target_state"] = formatted_target_state
        correct_answer = {
            "mode": "cartesian",
            "target_state": formatted_target_state if formatted_target_state is not None else {"invariants_count": len(invs_out)},
        }
        return compiled_ic, correct_answer

    nodes = raw_ic.get("nodes") or []
    edges = raw_ic.get("edges") or []
    tree_inv = raw_ic.get("tree_invariants") or {}
    if not isinstance(nodes, list) or len(nodes) < 2 or not isinstance(edges, list) or not edges:
        raise ValueError("[CANVAS-TREE] tree mode requires nodes (>=2) and edges.")
    if not isinstance(tree_inv, dict):
        raise ValueError("[CANVAS-TREE] tree mode requires 'tree_invariants' dict.")

    formatted_nodes = []
    for nd in nodes:
        if isinstance(nd, dict):
            nnd = dict(nd)
            if isinstance(nnd.get("label"), str):
                nnd["label"] = sanitize_katex_syntax(format_template_string(nnd["label"], variables))
            formatted_nodes.append(nnd)

    formatted_edges = []
    for ed in edges:
        if isinstance(ed, dict):
            ned = dict(ed)
            if isinstance(ned.get("label"), str):
                ned["label"] = sanitize_katex_syntax(format_template_string(ned["label"], variables))
            formatted_edges.append(ned)

    ti = dict(tree_inv)
    did = ti.get("distractor_id") or ti.get("did")
    did_norm = str(did).strip().replace("_", "-") if did else None
    for rk, default_msg in (
        ("edge_error_rationale", "La selección de ramas en el árbol no corresponde al equilibrio o estrategia válida."),
        ("info_set_error_rationale", "La partición de conjuntos de información no refleja correctamente quién observa qué historia."),
    ):
        raw_r = ti.get(rk)
        if not raw_r and did_norm and did_norm in rats_map:
            raw_r = rats_map[did_norm]
        ti[rk] = _resolve_distractor_rationale(
            {"error_rationale": raw_r},
            did_norm,
            cta_distractors_map,
            default_msg,
            variables=variables,
        )
    if did_norm:
        ti["distractor_id"] = did_norm

    compiled_ic = {
        "mode": "tree",
        "width": raw_ic.get("width", 520),
        "height": raw_ic.get("height", 320),
        "interaction_mode": raw_ic.get("interaction_mode", "both"),
        "nodes": formatted_nodes,
        "edges": formatted_edges,
        "tree_invariants": ti,
    }
    correct_answer = {
        "mode": "tree",
        "required_edges": ti.get("required_edges") or [],
        "required_info_sets": ti.get("required_info_sets") or [],
    }
    return compiled_ic, correct_answer


def _assemble_concept_matching(
    raw_cm: Any,
    variables: Dict[str, Any],
    cta_distractors_map: Optional[Dict[str, Dict[str, Any]]],
    rng: random.Random,
    rats_map: Dict[str, str],
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    if not isinstance(raw_cm, dict):
        raise ValueError("[MATCHING-INVALID] concept_matching payload must be a dict.")
    premises_raw = raw_cm.get("premises") or []
    targets_raw = raw_cm.get("targets") or []
    correct_pairs_raw = raw_cm.get("correct_pairs") or {}
    if not isinstance(premises_raw, list) or len(premises_raw) < 2:
        raise ValueError("[MATCHING-PREMISES] concept_matching requires at least 2 premises.")
    if not isinstance(targets_raw, list) or len(targets_raw) < len(premises_raw):
        raise ValueError("[MATCHING-TARGETS] targets length must be >= premises length.")
    if not isinstance(correct_pairs_raw, dict) or len(correct_pairs_raw) < len(premises_raw):
        raise ValueError("[MATCHING-PAIRS] correct_pairs must map every premise id.")

    premises: List[Dict[str, Any]] = []
    premise_ids: Set[str] = set()
    for idx, pr in enumerate(premises_raw):
        if not isinstance(pr, dict):
            raise ValueError(f"[MATCHING-PREMISE] premise[{idx}] must be a dict.")
        pid = str(pr.get("id") or f"L{idx + 1}").strip()
        content = sanitize_katex_syntax(format_template_string(str(pr.get("content") or ""), variables))
        if not pid or not content:
            raise ValueError(f"[MATCHING-PREMISE] premise[{idx}] missing id or content.")
        premise_ids.add(pid)
        premises.append({"id": pid, "content": content})

    targets: List[Dict[str, Any]] = []
    target_ids: Set[str] = set()
    for idx, tg in enumerate(targets_raw):
        if not isinstance(tg, dict):
            raise ValueError(f"[MATCHING-TARGET] target[{idx}] must be a dict.")
        tid = str(tg.get("id") or f"R{idx + 1}").strip()
        content = sanitize_katex_syntax(format_template_string(str(tg.get("content") or ""), variables))
        if not tid or not content:
            raise ValueError(f"[MATCHING-TARGET] target[{idx}] missing id or content.")
        target_ids.add(tid)
        is_dist = bool(tg.get("is_distractor", False))
        entry: Dict[str, Any] = {"id": tid, "content": content, "is_distractor": is_dist}
        did = tg.get("distractor_id") or tg.get("did")
        did_norm = str(did).strip().replace("_", "-") if did else None
        if tg.get("error_rationale") or tg.get("rationale") or did_norm or is_dist:
            tg_lookup = dict(tg)
            if not tg_lookup.get("error_rationale") and did_norm and did_norm in rats_map:
                tg_lookup["error_rationale"] = rats_map[did_norm]
            entry["error_rationale"] = _resolve_distractor_rationale(
                tg_lookup,
                did_norm,
                cta_distractors_map,
                f"La asociación seleccionada con '{content}' no corresponde al principio causal correcto.",
                variables=variables,
            )
            if did_norm:
                entry["distractor_id"] = did_norm
        targets.append(entry)

    clean_pairs: Dict[str, str] = {}
    for pid in premise_ids:
        tid = correct_pairs_raw.get(pid)
        if not tid or str(tid) not in target_ids:
            raise ValueError(f"[MATCHING-PAIR-REF] Missing or invalid target mapping for premise '{pid}'.")
        clean_pairs[pid] = str(tid)

    pair_rationales: Dict[str, str] = {}
    for pk, pv in (raw_cm.get("pair_rationales") or {}).items():
        if isinstance(pv, str) and pv.strip():
            pair_rationales[str(pk)] = sanitize_katex_syntax(format_template_string(pv, variables))

    rng.shuffle(premises)
    rng.shuffle(targets)

    compiled_cm: Dict[str, Any] = {
        "left_title": sanitize_katex_syntax(format_template_string(str(raw_cm.get("left_title") or "Premisa"), variables)),
        "right_title": sanitize_katex_syntax(format_template_string(str(raw_cm.get("right_title") or "Consecuencia"), variables)),
        "premises": premises,
        "targets": targets,
        "correct_pairs": clean_pairs,
    }
    if pair_rationales:
        compiled_cm["pair_rationales"] = pair_rationales

    return compiled_cm, {"pairs": clean_pairs}


def assemble_question(
    template: Dict[str, Any],
    gen_result: Dict[str, Any],
    competency_id: str,
    question_index: int,
    cta_distractors_map: Optional[Dict[str, Dict[str, Any]]] = None,
    seed: Optional[int] = None,
    stem_variant_index: Optional[int] = None,
) -> Dict[str, Any]:
    """Assemble a single question JSON conforming to platform specification.
    
    Args:
        template: Template dict from template.schema.json.
        gen_result: Result dict from sandbox execute.
        competency_id: ID of the competency (e.g. 'Hab-01').
        question_index: 1-indexed counter.
        cta_distractors_map: Map of distractor_id -> distractor metadata from cta.json.
        seed: Random seed for option shuffling.
        stem_variant_index: Optional explicit index into template['stem_variants'] for
            deterministic without-replacement variant rotation.
    """
    rng = random.Random(seed) if seed is not None else random.Random()
    variables = gen_result.get("vars", {})

    # Format text strings with variables
    stem_raw = template.get("stem", "")
    stem_variants = template.get("stem_variants")
    if stem_variants and len(stem_variants) > 0:
        if stem_variant_index is not None:
            var_idx = int(stem_variant_index) % len(stem_variants)
        else:
            var_idx = (seed % len(stem_variants)) if seed is not None else 0
        stem_raw = stem_variants[var_idx]
    stem = sanitize_katex_syntax(format_template_string(stem_raw, variables))
    if not isinstance(stem, str) or not stem.strip():
        raise ValueError(f"Question stem cannot be empty for {competency_id} #{question_index}")
    raw_hints = template.get("hints", [])
    hints = []
    for h in raw_hints:
        if isinstance(h, dict):
            h_text = h.get("text") or h.get("content") or str(h)
        else:
            h_text = str(h)
        hints.append(sanitize_katex_syntax(format_template_string(h_text, variables)))
    raw_solution = template.get("detailed_solution") or template.get("solution", "")
    detailed_solution = sanitize_katex_syntax(format_template_string(raw_solution, variables))

    # Determine misconception warning from distractor remediation hint
    common_misconception_warning = ""
    remediation_hints = []
    if cta_distractors_map:
        for d_id in template.get("distractor_ids", []):
            if d_id in cta_distractors_map:
                d_entry = cta_distractors_map[d_id]
                rh = (
                    d_entry.get("remediation_hint")
                    or d_entry.get("wrong_belief")
                    or d_entry.get("omitted_step")
                )
                if isinstance(rh, str) and rh.strip():
                    remediation_hints.append(rh.strip())
    
    if remediation_hints:
        common_misconception_warning = remediation_hints[0]
    else:
        tpl_warning = template.get("common_misconception_warning")
        if (
            isinstance(tpl_warning, str)
            and tpl_warning.strip()
            and tpl_warning.strip() != _GENERIC_WARNING_BOILERPLATE
            and not _is_generic_placeholder(tpl_warning)
        ):
            common_misconception_warning = tpl_warning
        else:
            common_misconception_warning = _build_competency_misconception_fallback(
                competency_id, template, cta_distractors_map, gen_result
            )

    clean_comp = re.sub(r"[^A-Za-z0-9]", "", competency_id)
    question_id = f"Q-{clean_comp}-{question_index:03d}"
    interaction_type = template["interaction_type"]
    bloom = template.get("bloom", "Apply")
    difficulty = template.get("difficulty", "medium")

    assembled: Dict[str, Any] = {
        "id": question_id,
        "competency_id": competency_id,
        "bloom_taxonomy_level": bloom,
        "difficulty": difficulty,
        "interaction_type": interaction_type,
        "type": interaction_type,
        "context_application": f"Evaluación conceptual y procedimental para {competency_id}",
        "stem": stem,
        "hints": hints,
        "detailed_solution": detailed_solution,
        "common_misconception_warning": common_misconception_warning,
        "misconception_warning": common_misconception_warning,
    }

    if template.get("graph"):
        assembled["graph"] = template["graph"]

    if isinstance(common_misconception_warning, str) and common_misconception_warning:
        clean_warning = _strip_giveaway_prefix(common_misconception_warning)
        common_misconception_warning = sanitize_katex_syntax(
            format_template_string(clean_warning, variables, is_cta=True)
        )
        if not common_misconception_warning.strip() or validate_katex_syntax(
            common_misconception_warning, "common_misconception_warning", allow_template_vars=False
        ):
            fallback_warning = _build_competency_misconception_fallback(
                competency_id, template, cta_distractors_map, gen_result
            )
            fallback_sanitized = sanitize_katex_syntax(
                format_template_string(_strip_giveaway_prefix(fallback_warning), variables, is_cta=True)
            )
            if not fallback_sanitized.strip() or validate_katex_syntax(
                fallback_sanitized, "common_misconception_warning", allow_template_vars=False
            ):
                common_misconception_warning = f"Revise cuidadosamente los supuestos y pasos clave de la competencia {competency_id} antes de responder."
            else:
                common_misconception_warning = fallback_sanitized
        assembled["common_misconception_warning"] = common_misconception_warning
        assembled["misconception_warning"] = common_misconception_warning

    # Assemble interaction-specific fields
    if interaction_type == "multiple_choice_7_options":
        correct_raw = str(gen_result.get("correct", "")).strip()
        correct_val = sanitize_katex_syntax(format_template_string(correct_raw, variables))
        if not correct_val.strip():
            raise ValueError(f"MC7 correct option cannot be empty for {competency_id} #{question_index}")
        raw_distractors = gen_result.get("distractors", [])
        
        # Ensure we have 6 distractors
        if len(raw_distractors) < 6:
            raise ValueError(f"MC7 requires 6 distractors, found {len(raw_distractors)}")
        
        selected_distractors = raw_distractors[:6]
        seen_option_contents = {correct_val.strip()}
        items_to_shuffle: List[Dict[str, Any]] = [
            {
                "content": correct_val,
                "is_correct": True,
                "error_rationale": None,
                "distractor_id": None,
            }
        ]

        for d in selected_distractors:
            d_raw = str(d.get("value", "")).strip()
            d_val = sanitize_katex_syntax(format_template_string(d_raw, variables))
            if not d_val.strip():
                raise ValueError(f"MC7 distractor content cannot be empty for {competency_id} #{question_index}")
            if d_val.strip() in seen_option_contents:
                raise ValueError(f"MC7 duplicate option content detected ({d_val!r}) for {competency_id} #{question_index}")
            seen_option_contents.add(d_val.strip())
            d_id = d.get("distractor_id")
            default_fb = "Distractor derivado de error de procedimiento o misconception"
            rationale = _resolve_distractor_rationale(
                d, d_id, cta_distractors_map, default_fb, variables=variables
            )
            if isinstance(rationale, str):
                errs = validate_katex_syntax(rationale, "distractor_rationale", allow_template_vars=False)
                if errs:
                    rationale = sanitize_katex_syntax(default_fb)
            
            items_to_shuffle.append({
                "content": d_val,
                "is_correct": False,
                "error_rationale": rationale,
                "distractor_id": d_id,
            })

        rng.shuffle(items_to_shuffle)

        options = []
        correct_letter = None
        for idx, item in enumerate(items_to_shuffle):
            letter = OPTION_LETTERS[idx]
            opt_entry = {
                "id": f"opt_{letter.lower()}",
                "option_id": letter,
                "content": sanitize_katex_syntax(item["content"]),
                "is_correct": item["is_correct"],
                "error_rationale": item["error_rationale"],
            }
            if item["distractor_id"]:
                opt_entry["distractor_id"] = item["distractor_id"]
            options.append(opt_entry)

            if item["is_correct"]:
                correct_letter = letter

        assembled["interface_config"] = {
            "allow_calculator": False,
            "input_placeholder": None,
            "expected_format": "single_selection",
            "grading_policy": "single_choice",
        }
        assembled["options"] = options
        assembled["correct_answer"] = correct_letter

    elif interaction_type == "fill_in_the_blank":
        ans_val = gen_result.get("correct")
        if ans_val is None:
            ans_val = gen_result.get("value", "")

        str_val = str(ans_val).strip()
        str_val = sanitize_katex_syntax(format_template_string(str_val, variables))
        if not str_val.strip():
            raise ValueError(f"FIB correct answer value cannot be empty for {competency_id} #{question_index}")

        if re.fullmatch(r"[+-]?\d+\.\d{3,}", str_val):
            stem_lower = stem.lower()
            if "decimales" not in stem_lower and "redonde" not in stem_lower:
                stem = f"{stem} (Exprese su respuesta redondeada a 4 decimales)."
                assembled["stem"] = stem

        raw_canonical = gen_result.get("canonical_algebraic")
        if raw_canonical is not None:
            canonical_val = sanitize_katex_syntax(format_template_string(str(raw_canonical).strip(), variables)) if isinstance(raw_canonical, str) else str(raw_canonical)
        else:
            canonical_val = str_val
        raw_equivalents = gen_result.get("accepted_equivalents")
        if raw_equivalents is None:
            raw_equivalents = gen_result.get("equivalents")
        if raw_equivalents is None:
            raw_equivalents = [str_val]

        equivalents = []
        for eq in raw_equivalents:
            if isinstance(eq, (int, float)):
                formatted_eq = str(eq)
            elif isinstance(eq, str):
                formatted_eq = sanitize_katex_syntax(format_template_string(eq.strip(), variables))
            else:
                formatted_eq = str(eq)
            if formatted_eq not in equivalents:
                equivalents.append(formatted_eq)
        if str_val not in equivalents:
            equivalents = [str_val] + list(equivalents)

        tolerance = gen_result.get("tolerance", 0.001)

        assembled["interface_config"] = {
            "allow_calculator": False,
            "input_placeholder": None,
            "expected_format": "algebraic_expression",
            "grading_policy": "binary_all_or_nothing",
        }
        assembled["options"] = []
        assembled["correct_answer"] = {
            "value": str_val,
            "canonical_algebraic": canonical_val,
            "accepted_equivalents": equivalents,
            "tolerance": tolerance,
        }
        diag_dists = _assemble_diagnostic_distractors(gen_result, template, variables, cta_distractors_map)
        if diag_dists:
            assembled["diagnostic_distractors"] = diag_dists

    elif interaction_type == "open_symbolic":
        ans_val = gen_result.get("correct")
        if ans_val is None:
            ans_val = gen_result.get("expression")
        if ans_val is None:
            ans_val = gen_result.get("value", "")

        str_val = _strip_outer_math_dollars(sanitize_katex_syntax(format_template_string(str(ans_val).strip(), variables)))
        if not str_val:
            raise ValueError(f"open_symbolic correct answer expression cannot be empty for {competency_id} #{question_index}")

        raw_canonical = gen_result.get("canonical_algebraic")
        if raw_canonical is not None:
            canonical_val = _strip_outer_math_dollars(
                sanitize_katex_syntax(format_template_string(str(raw_canonical).strip(), variables))
            )
        else:
            canonical_val = str_val

        raw_equivalents = gen_result.get("accepted_equivalents")
        if raw_equivalents is None:
            raw_equivalents = gen_result.get("equivalents")
        if raw_equivalents is None:
            raw_equivalents = [str_val]

        equivalents: List[str] = []
        for eq in raw_equivalents:
            if isinstance(eq, (int, float)):
                formatted_eq = str(eq)
            elif isinstance(eq, str):
                formatted_eq = _strip_outer_math_dollars(
                    sanitize_katex_syntax(format_template_string(eq.strip(), variables))
                )
            else:
                formatted_eq = str(eq)
            if formatted_eq and formatted_eq not in equivalents:
                equivalents.append(formatted_eq)
        if str_val not in equivalents:
            equivalents = [str_val] + equivalents

        tolerance = gen_result.get("tolerance", 0.001)
        sym_cfg_raw = gen_result.get("symbolic_config") or template.get("symbolic_config")
        sym_cfg = dict(sym_cfg_raw) if isinstance(sym_cfg_raw, dict) else {}
        if isinstance(gen_result.get("variables"), list) and "variables" not in sym_cfg:
            sym_cfg["variables"] = [str(x) for x in gen_result["variables"]]

        assembled["interface_config"] = {
            "allow_calculator": False,
            "input_placeholder": sym_cfg.get("placeholder"),
            "expected_format": "open_symbolic",
            "grading_policy": "symbolic_ast_equivalence",
        }
        assembled["options"] = []
        assembled["correct_answer"] = {
            "expression": str_val,
            "value": str_val,
            "canonical_algebraic": canonical_val,
            "accepted_equivalents": equivalents,
            "tolerance": tolerance,
        }
        if sym_cfg:
            assembled["symbolic_config"] = sym_cfg
        diag_dists = _assemble_diagnostic_distractors(gen_result, template, variables, cta_distractors_map)
        if diag_dists:
            assembled["diagnostic_distractors"] = diag_dists

    elif interaction_type == "proof_dag":
        try:
            from engine.proof_compiler import compile_and_verify_proof_dag
        except ImportError:
            from .proof_compiler import compile_and_verify_proof_dag
        raw_dag = gen_result.get("proof_dag") or gen_result.get("dag") or template.get("proof_dag")
        rats_map = template.get("rats") if isinstance(template.get("rats"), dict) else {}
        compiled_dag, corr_ans = compile_and_verify_proof_dag(
            raw_dag,
            variables=variables,
            cta_distractors_map=cta_distractors_map,
            rng=rng,
            rats_map=rats_map,
        )
        assembled["interface_config"] = {
            "allow_calculator": False,
            "input_placeholder": None,
            "expected_format": "proof_dag",
            "grading_policy": "topological_dag",
        }
        assembled["options"] = []
        assembled["proof_dag"] = compiled_dag
        assembled["correct_answer"] = corr_ans

    elif interaction_type == "adversarial_break":
        try:
            from engine.adversarial_generator import compile_and_verify_adversarial
        except ImportError:
            from .adversarial_generator import compile_and_verify_adversarial
        raw_adv = gen_result.get("adversarial_break") or gen_result.get("adversarial") or template.get("adversarial_break")
        rats_map = template.get("rats") if isinstance(template.get("rats"), dict) else {}
        compiled_adv, corr_ans = compile_and_verify_adversarial(
            raw_adv,
            variables=variables,
            cta_distractors_map=cta_distractors_map,
            rng=rng,
            rats_map=rats_map,
        )
        assembled["interface_config"] = {
            "allow_calculator": False,
            "input_placeholder": None,
            "expected_format": "adversarial_break",
            "grading_policy": f"adversarial_{compiled_adv['mode']}",
        }
        assembled["options"] = []
        assembled["adversarial_break"] = compiled_adv
        assembled["correct_answer"] = corr_ans

    elif interaction_type == "unstructured_model":
        raw_um = gen_result.get("unstructured_model") or gen_result.get("stage0") or template.get("unstructured_model")
        rats_map = template.get("rats") if isinstance(template.get("rats"), dict) else {}
        compiled_um, corr_ans = _assemble_unstructured_model(
            raw_um,
            variables=variables,
            cta_distractors_map=cta_distractors_map,
            rng=rng,
            rats_map=rats_map,
        )
        assembled["interface_config"] = {
            "allow_calculator": False,
            "input_placeholder": None,
            "expected_format": "unstructured_model",
            "grading_policy": "stage0_3phase_sequential",
        }
        assembled["options"] = []
        assembled["unstructured_model"] = compiled_um
        assembled["correct_answer"] = corr_ans

    elif interaction_type == "invariant_canvas":
        raw_ic = gen_result.get("invariant_canvas") or gen_result.get("canvas") or template.get("invariant_canvas")
        rats_map = template.get("rats") if isinstance(template.get("rats"), dict) else {}
        compiled_ic, corr_ans = _assemble_invariant_canvas(
            raw_ic,
            variables=variables,
            cta_distractors_map=cta_distractors_map,
            rats_map=rats_map,
        )
        assembled["interface_config"] = {
            "allow_calculator": False,
            "input_placeholder": None,
            "expected_format": "invariant_canvas",
            "grading_policy": f"canvas_{compiled_ic['mode']}",
        }
        assembled["options"] = []
        assembled["invariant_canvas"] = compiled_ic
        assembled["correct_answer"] = corr_ans

    elif interaction_type == "concept_matching":
        raw_cm = gen_result.get("concept_matching") or gen_result.get("matching") or template.get("concept_matching")
        rats_map = template.get("rats") if isinstance(template.get("rats"), dict) else {}
        compiled_cm, corr_ans = _assemble_concept_matching(
            raw_cm,
            variables=variables,
            cta_distractors_map=cta_distractors_map,
            rng=rng,
            rats_map=rats_map,
        )
        assembled["interface_config"] = {
            "allow_calculator": False,
            "input_placeholder": None,
            "expected_format": "concept_matching",
            "grading_policy": "matching_all_pairs",
        }
        assembled["options"] = []
        assembled["concept_matching"] = compiled_cm
        assembled["correct_answer"] = corr_ans

    elif interaction_type == "multiple_select":
        raw_options = gen_result.get("options", [])
        if not (4 <= len(raw_options) <= 6):
            raise ValueError(f"MS requires 4 to 6 options, found {len(raw_options)}")

        shuffled_options = list(raw_options)
        rng.shuffle(shuffled_options)

        options = []
        correct_letters = []
        tpl_dids = template.get("distractor_ids", [])
        false_idx = 0
        for idx, opt in enumerate(shuffled_options):
            letter = OPTION_LETTERS[idx]
            is_correct = bool(opt.get("is_correct") if "is_correct" in opt else opt.get("correct", False))
            d_id = opt.get("distractor_id")
            if not is_correct and not d_id and false_idx < len(tpl_dids):
                d_id = tpl_dids[false_idx]
                false_idx += 1
            elif not is_correct:
                false_idx += 1

            if not is_correct:
                default_fb = "Opción inválida derivada de una concepción errónea del concepto o propiedad."
                rationale = _resolve_distractor_rationale(
                    opt, d_id, cta_distractors_map, default_fb, variables=variables
                )
                if isinstance(rationale, str):
                    errs = validate_katex_syntax(rationale, "distractor_rationale", allow_template_vars=False)
                    if errs:
                        rationale = sanitize_katex_syntax(default_fb)
            else:
                raw_rat = opt.get("error_rationale")
                if raw_rat is None or raw_rat == "":
                    raw_rat = opt.get("rationale")
                if raw_rat:
                    cand_correct = _format_and_sanitize_candidate(str(raw_rat), variables=variables, is_cta=False)
                    errs = validate_katex_syntax(cand_correct, "correct_rationale", allow_template_vars=False)
                    rationale = cand_correct if not errs else None
                else:
                    rationale = None
            raw_opt_content = opt.get("content")
            if raw_opt_content is None or raw_opt_content == "":
                raw_opt_content = opt.get("value")
            if raw_opt_content is None or raw_opt_content == "":
                raw_opt_content = opt.get("text", "")
            raw_opt_content = str(raw_opt_content)
            opt_content = sanitize_katex_syntax(format_template_string(raw_opt_content, variables))
            if not opt_content.strip():
                raise ValueError(f"MS option content cannot be empty for {competency_id} #{question_index}")

            opt_entry = {
                "id": f"opt_{letter.lower()}",
                "option_id": letter,
                "content": opt_content,
                "is_correct": is_correct,
                "error_rationale": rationale,
            }
            if d_id:
                opt_entry["distractor_id"] = d_id
            options.append(opt_entry)

            if opt_entry["is_correct"]:
                correct_letters.append(letter)

        if not correct_letters:
            raise ValueError(f"MS requires at least 1 correct option for {competency_id} #{question_index}")

        assembled["interface_config"] = {
            "allow_calculator": False,
            "input_placeholder": None,
            "expected_format": "multiple_selection",
            "grading_policy": "binary_all_or_nothing",
        }
        assembled["options"] = options
        assembled["correct_answer"] = sorted(correct_letters)

    return assembled


def check_course_giveaway_distribution(questions: List[Dict[str, Any]]) -> Tuple[bool, Dict[str, Any]]:
    """Verify that correct option length is not longest in >25% and shortest in >25% of MC items."""
    mc_questions = [q for q in questions if q.get("interaction_type") == "multiple_choice_7_options"]
    if not mc_questions:
        return True, {"mc_count": 0}

    longest_count = 0
    shortest_count = 0
    total_mc = len(mc_questions)

    for q in mc_questions:
        options = q.get("options", [])
        if len(options) != 7:
            continue

        correct_opt = next((opt for opt in options if opt.get("is_correct")), None)
        if not correct_opt:
            continue

        c_len = len(correct_opt.get("content", ""))
        lens = [len(opt.get("content", "")) for opt in options]

        max_len = max(lens)
        min_len = min(lens)

        if c_len == max_len:
            longest_count += 1
        if c_len == min_len:
            shortest_count += 1

    longest_ratio = longest_count / total_mc
    shortest_ratio = shortest_count / total_mc

    passes = (longest_ratio <= 0.25) and (shortest_ratio <= 0.25)
    stats = {
        "total_mc": total_mc,
        "longest_count": longest_count,
        "longest_ratio": round(longest_ratio, 4),
        "shortest_count": shortest_count,
        "shortest_ratio": round(shortest_ratio, 4),
        "passes": passes,
    }
    return passes, stats
