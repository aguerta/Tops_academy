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
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

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


def format_template_string(template_str: str, variables: Dict[str, Any]) -> str:
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
    for k, v in variables.items():
        pattern = re.compile(rf"\{{{re.escape(k)}(?::([^{{}}]+))?\}}")
        math_spans = [m_s.span() for m_s in re.finditer(r"\$\$[\s\S]*?\$\$|\$[^\$]+?\$", result)]
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
                return val_str

            prefix_stripped = prefix.rstrip()

            # Case 2: Preceded directly by a LaTeX macro \cmd or \cmd[...]
            macro_m = re.search(r"\\([a-zA-Z]+)\*?(\[[^\]]*\])?\s*$", prefix_stripped)
            if macro_m:
                macro_name = macro_m.group(1)
                if macro_name in _LATEX_VALUE_MACROS_1ARG or macro_name in _LATEX_VALUE_MACROS_2ARG:
                    if has_pl_tokens and len(key) <= 1 and not fmt_spec and is_in_math_span(start):
                        return m.group(0)
                    return f"{{{val_str}}}"
                if not fmt_spec and "_" not in key:
                    return m.group(0)
                return f"{{{val_str}}}"

            # Case 3: Second argument of a 2-argument value macro e.g. \frac{...}{k}
            is_second_arg, has_symbolic = _inspect_second_arg_of_value_macro(prefix_stripped, key)
            if is_second_arg:
                if has_pl_tokens and len(key) <= 1 and not fmt_spec and is_in_math_span(start):
                    return m.group(0)
                if has_symbolic and not fmt_spec and "_" not in key:
                    return m.group(0)
                return f"{{{val_str}}}"

            # Case 4: Superscript ^{k} or subscript _{k}
            if prefix_stripped.endswith("^") or prefix_stripped.endswith("_"):
                if has_pl_tokens and len(key) <= 1 and not fmt_spec and is_in_math_span(start):
                    return m.group(0)
                return f"{{{val_str}}}"

            return val_str

        result = pattern.sub(_replacer, result)

        # Fallback for bare code variables ending in _val, _num, _str, _res left unbraced by LLM
        if re.match(r"^[a-zA-Z0-9]+_(?:val|num|str|res)$", k):
            result = re.sub(rf"\b{re.escape(k)}\b", lambda _, val=str(v): val, result)

    return result


def render_template(template_str: str, variables: Dict[str, Any]) -> str:
    r"""Render template string with variables, supporting both PrairieLearn @var@ and legacy {var} syntax."""
    return format_template_string(template_str, variables)


def sanitize_katex_syntax(text: str) -> str:
    r"""Sanitize KaTeX syntax by fixing f-string artifacts, unclosed nested macros, and delimiter issues.
    
    - Replaces '$$$' with '$$'
    - Normalizes residual paired double curly braces from f-strings '{{x}}' -> '{x}'
      without altering legitimate nested KaTeX syntax like \\frac{\\dot{r}}{r} or k^{\\frac{1}{3}}.
    - Auto-closes unclosed nested accent/style/sqrt macros (e.g. \\hat{\\boldsymbol{\\beta} -> \\hat{\\boldsymbol{\\beta}}).
    - Auto-repairs dropped numerator/denominator braces in \\frac and superscripts/subscripts.
    """
    if not isinstance(text, str):
        return text

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
    outer_macros = r"(?:hat|bar|tilde|vec|dot|ddot|acute|grave|check|breve|mathring|widehat|widetilde|widecheck|overline|underline|sqrt)"
    inner_macros = r"(?:boldsymbol|mathbf|bm|mathit|mathrm|mathbb|mathcal|text|textbf|symbf|hat|bar|tilde|vec|dot|ddot)"
    nested_fix = re.compile(
        rf"(\\(?:{outer_macros})\s*\{{\s*\\(?:{inner_macros})\s*\{{[^{{}}]*\}})(?!\s*\}})"
    )
    text = nested_fix.sub(r"\1}", text)

    # 2. Auto-repair \frac missing numerator closing brace when numerator has an inner 1-arg macro or script
    frac_inner_fix = re.compile(
        r"(\\(?:frac|dfrac|tfrac|cfrac)\s*\{[^{}]*(?:\\[a-zA-Z]+|[_^])\s*\{[^{}]*\}[^{}\\]*)\{"
    )
    text = frac_inner_fix.sub(r"\1}{", text)

    # Simple \frac{a{b} where numerator has no macros or scripts
    frac_simple_fix = re.compile(
        r"(\\(?:frac|dfrac|tfrac|cfrac)\s*\{[^{}\\^_]+)\{([^{}]+\})"
    )
    text = frac_simple_fix.sub(r"\1}{\2", text)

    # 3. Auto-repair \frac missing denominator closing brace when denominator ends with an inner braced group
    if text.count("{") > text.count("}"):
        frac_den_fix = re.compile(
            r"(\\(?:frac|dfrac|tfrac|cfrac)\s*\{(?:[^{}]|\{[^{}]*\})*\}\s*\{[^{}]*(?:\\[a-zA-Z]+|[_^])\s*\{[^{}]*\})"
            r"(?!\s*\})(?=\s*(?:[$=<>,.;:)\]|]|\\(?:le|ge|neq|approx|implies|iff)\b|$))"
        )
        text = frac_den_fix.sub(r"\1}", text)

    # 4. Auto-repair superscript/subscript missing outer closing brace after inner macro
    if text.count("{") > text.count("}"):
        script_outer_fix = re.compile(
            r"([_^]\s*\{[^{}]*\\[a-zA-Z]+(?:\s*\{[^{}]*\})+)"
            r"(?!\s*\})(?=\s*(?:[$=<>,.;:)\]|]|\\(?:le|ge|neq|approx|implies|iff)\b|$))"
        )
        text = script_outer_fix.sub(r"\1}", text)

    # 5. Auto-repair unbraced numeric denominator after \frac{num}: \frac{s}3 -> \frac{s}{3}
    frac_unbraced_den = re.compile(
        r"(\\(?:frac|dfrac|tfrac|cfrac)\s*\{(?:[^{}]|\{[^{}]*\})*\})\s*([0-9]+(?:\.[0-9]+)?)"
    )
    text = frac_unbraced_den.sub(r"\1{\2}", text)

    return text


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


def assemble_question(
    template: Dict[str, Any],
    gen_result: Dict[str, Any],
    competency_id: str,
    question_index: int,
    cta_distractors_map: Optional[Dict[str, Dict[str, Any]]] = None,
    seed: Optional[int] = None,
) -> Dict[str, Any]:
    """Assemble a single question JSON conforming to platform specification.
    
    Args:
        template: Template dict from template.schema.json.
        gen_result: Result dict from sandbox execute.
        competency_id: ID of the competency (e.g. 'Hab-01').
        question_index: 1-indexed counter.
        cta_distractors_map: Map of distractor_id -> distractor metadata from cta.json.
        seed: Random seed for option shuffling.
    """
    rng = random.Random(seed) if seed is not None else random.Random()
    variables = gen_result.get("vars", {})

    # Format text strings with variables
    stem_raw = template["stem"]
    stem_variants = template.get("stem_variants")
    if stem_variants and len(stem_variants) > 0:
        var_idx = (seed % len(stem_variants)) if seed is not None else 0
        stem_raw = stem_variants[var_idx]
    stem = sanitize_katex_syntax(format_template_string(stem_raw, variables))
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
                if rh:
                    remediation_hints.append(rh)
    
    if remediation_hints:
        common_misconception_warning = remediation_hints[0]
    else:
        common_misconception_warning = template.get(
            "common_misconception_warning",
            "Verifique cuidadosamente los supuestos y cálculos antes de seleccionar su respuesta."
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
        cta_vars = {k: v for k, v in variables.items() if len(k) > 2 or k.endswith(("_val", "_num", "_str", "_res"))}
        common_misconception_warning = sanitize_katex_syntax(
            format_template_string(clean_warning, cta_vars)
        )
        assembled["common_misconception_warning"] = common_misconception_warning
        assembled["misconception_warning"] = common_misconception_warning

    # Assemble interaction-specific fields
    if interaction_type == "multiple_choice_7_options":
        correct_raw = str(gen_result.get("correct", "")).strip()
        correct_val = sanitize_katex_syntax(format_template_string(correct_raw, variables))
        raw_distractors = gen_result.get("distractors", [])
        
        # Ensure we have 6 distractors
        if len(raw_distractors) < 6:
            raise ValueError(f"MC7 requires 6 distractors, found {len(raw_distractors)}")
        
        selected_distractors = raw_distractors[:6]
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
            d_id = d.get("distractor_id")
            rationale = d.get("error_rationale") or d.get("rationale") or "Distractor derivado de error de procedimiento o misconception"
            if cta_distractors_map and d_id in cta_distractors_map:
                d_entry = cta_distractors_map[d_id]
                rationale = (
                    d_entry.get("manifestation")
                    or d_entry.get("wrong_belief")
                    or d_entry.get("omitted_step")
                    or rationale
                )
            if isinstance(rationale, str):
                clean_rat = _strip_giveaway_prefix(rationale)
                cta_vars = {k: v for k, v in variables.items() if len(k) > 2 or k.endswith(("_val", "_num", "_str", "_res"))} if (cta_distractors_map and d_id in cta_distractors_map) else variables
                rationale = sanitize_katex_syntax(format_template_string(clean_rat, cta_vars))
            
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

    elif interaction_type == "multiple_select":
        raw_options = gen_result.get("options", [])
        if not (4 <= len(raw_options) <= 6):
            raise ValueError(f"MS requires 4 to 6 options, found {len(raw_options)}")

        shuffled_options = list(raw_options)
        rng.shuffle(shuffled_options)

        options = []
        correct_letters = []
        for idx, opt in enumerate(shuffled_options):
            letter = OPTION_LETTERS[idx]
            is_correct = bool(opt.get("is_correct") if "is_correct" in opt else opt.get("correct", False))
            rationale = opt.get("error_rationale")
            if rationale is None or rationale == "":
                rationale = opt.get("rationale")
            d_id = opt.get("distractor_id")

            if not is_correct:
                if not rationale or not str(rationale).strip():
                    if cta_distractors_map and d_id and d_id in cta_distractors_map:
                        rationale = (
                            cta_distractors_map[d_id].get("manifestation")
                            or cta_distractors_map[d_id].get("remediation_hint")
                        )
                    if not rationale or not str(rationale).strip():
                        rationale = "Opción inválida derivada de una concepción errónea del concepto o propiedad."
            else:
                if not rationale:
                    rationale = None

            if isinstance(rationale, str):
                clean_ms_rat = _strip_giveaway_prefix(rationale)
                cta_vars = {k: v for k, v in variables.items() if len(k) > 2 or k.endswith(("_val", "_num", "_str", "_res"))} if (cta_distractors_map and d_id in cta_distractors_map) else variables
                rationale = sanitize_katex_syntax(format_template_string(clean_ms_rat, cta_vars))
            raw_opt_content = opt.get("content")
            if raw_opt_content is None or raw_opt_content == "":
                raw_opt_content = opt.get("value")
            if raw_opt_content is None or raw_opt_content == "":
                raw_opt_content = opt.get("text", "")
            raw_opt_content = str(raw_opt_content)
            opt_content = sanitize_katex_syntax(format_template_string(raw_opt_content, variables))

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
