"""Question invariant evaluation for content-to-course v2.

Evaluates 100% of instances against strict psychometric and correctness rules:
- 1 correct answer (for MC7)
- Distractors distinct from correct and each other (TPL-D4)
- Cross-check verification passes
- No answer leaks in stem or progressive hints
- Interaction type structural constraints:
    * MC7: exactly 7 options, 1 correct, length anti-giveaway bounded
    * FIB: non-empty answer, tolerance or accepted equivalents
    * MS: 4-6 options, 1 to n-1 correct
- Scaffolding: 3 to 5 hints
"""

import functools
import re
import threading
from typing import Any, Dict, List, Optional, Tuple, Union

try:
    import pykatex
except ImportError:
    pykatex = None


_KATEX_LOCK = threading.Lock()
_KATEX_NUM_SKELETON_RE = re.compile(r"(?<![\\#'\"a-zA-Z0-9_])\d+(?:\.\d+)?")


def _normalize_katex_numeric_skeleton(math_content: str) -> str:
    """Collapse standalone numeric literals to canonical tokens to prevent LRU cache thrashing across seeds."""
    return _KATEX_NUM_SKELETON_RE.sub(
        lambda m: "1.2" if "." in m.group(0) else "1",
        math_content,
    )


def _render_katex_raw(math_content: str, is_display: bool) -> Tuple[bool, Optional[str]]:
    """Thread-safe native call to pykatex.renderToString without C stderr warning pipe stalls."""
    if pykatex is None:
        return True, None
    strict_mode = getattr(pykatex, "STRICT_IGNORE", "ignore")
    with _KATEX_LOCK:
        try:
            pykatex.renderToString(math_content, is_display, strict=strict_mode)
            return True, None
        except Exception as e:
            msg = str(e).replace("\u0332", "^")
            return False, msg


@functools.lru_cache(maxsize=32768)
def _render_katex_cached(math_content: str, is_display: bool) -> Tuple[bool, Optional[str]]:
    """Cached KaTeX render check over normalized or raw math expressions."""
    return _render_katex_raw(math_content, is_display)


def _render_katex_safe(math_content: str, is_display: bool) -> Tuple[bool, Optional[str]]:
    """Render math content using thread-safe pykatex with numeric-skeleton LRU caching.

    Cleans combining low-line character '\u0332' to ensure Windows cp1252 safety.
    """
    if pykatex is None:
        return True, None
    norm_math = _normalize_katex_numeric_skeleton(math_content)
    ok, err = _render_katex_cached(norm_math, is_display)
    if ok:
        return True, None
    if norm_math != math_content:
        return _render_katex_raw(math_content, is_display)
    return ok, err


class InvariantViolationError(Exception):
    """Raised when an instance violates mathematical or structural invariants."""
    pass


ANTONYM_PAIRS: List[Tuple[str, str]] = [
    ("converge", "diverge"),
    ("convergencia", "divergencia"),
    ("equilibrio", "desequilibrio"),
    ("estabilidad", "inestabilidad"),
    ("estable", "inestable"),
    ("crece", "decrece"),
    ("creciente", "decreciente"),
    ("aumenta", "disminuye"),
    ("positivo", "negativo"),
    ("máximo", "mínimo"),
]


_LATEX_ARG_MACROS = {
    # Text / formatting / math style macros that take 1 argument: \text{...}, \mathbf{...}
    "text", "textbf", "textit", "textrm", "textsf", "texttt", "textsc", "textmd", "textup", "textsl",
    "mathbf", "boldsymbol", "bm", "mathit", "mathrm", "mathcal", "mathbb",
    "mathfrak", "mathsf", "mathtt", "mathscr", "symbf", "operatorname",
    # Accents that take 1 argument: \hat{...}, \dot{...}
    "dot", "ddot", "dddot", "ddddot", "hat", "bar", "tilde", "vec", "acute", "grave", "check",
    "breve", "mathring", "widehat", "widetilde", "widecheck", "overline", "underline",
    # Extensible arrows & relation macros that take arguments e.g. \xrightarrow{d}, \xleftarrow{n}
    "xrightarrow", "xleftarrow", "xleftrightarrow", "xLeftarrow", "xRightarrow", "xLeftrightarrow",
    "xhookleftarrow", "xhookrightarrow", "xmapsto", "xtwoheadleftarrow", "xtwoheadrightarrow",
    "xleftharpoondown", "xleftharpoonup", "xrightharpoondown", "xrightharpoonup",
    # Structural / environment macros
    "begin", "end", "sqrt", "substack", "prescript", "pmod", "pod",
    # 2-arg macros
    "frac", "dfrac", "tfrac", "cfrac", "binom", "dbinom", "tbinom",
    "overset", "underset", "stackrel",
}

MATH_ACCENT_COMMANDS = (
    r"dot|ddot|hat|bar|tilde|vec|breve|check|acute|grave|mathring|"
    r"textbf|textit|textrm|textsf|texttt|mathrm|mathbf|mathit|mathsf|mathtt|"
    r"mathcal|mathbb|mathfrak|mathscr|operatorname|sqrt|frac|dfrac|tfrac|"
    r"binom|overset|underset|stackrel"
)

_PL_TOKEN_PATTERN = re.compile(r"@([A-Za-z_][A-Za-z0-9_]*(?::[^@\s{}]+)?)@")


def _unwrap_text_in_math(text: Optional[str]) -> str:
    """Unwrap \\text{...} and \\textrm{...} from inside KaTeX math delimiters ($...$ and $$...$$)."""
    if not text or not isinstance(text, str):
        return ""

    def _unwrap_math_block(match: re.Match) -> str:
        raw_block = match.group(0)
        is_display = raw_block.startswith("$$") and raw_block.endswith("$$") and len(raw_block) >= 4
        delim = "$$" if is_display else "$"
        content = raw_block[len(delim) : -len(delim)]

        pattern = re.compile(r"\\(text|textrm|mathrm)\s*\{")
        if not pattern.search(content):
            return raw_block

        pieces = []
        last_idx = 0
        for m in pattern.finditer(content):
            if m.start() < last_idx:
                continue
            before = content[last_idx:m.start()]
            if before.strip():
                pieces.append(f"{delim}{before}{delim}")
            start_brace = m.end() - 1
            depth = 1
            pos = start_brace + 1
            n = len(content)
            while pos < n and depth > 0:
                ch = content[pos]
                if ch == "\\" and pos + 1 < n:
                    pos += 2
                    continue
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                pos += 1
            if depth == 0:
                inner = content[start_brace + 1 : pos - 1]
                pieces.append(f" {inner} ")
                last_idx = pos
            else:
                rem = content[m.start():]
                if rem.strip():
                    pieces.append(f"{delim}{rem}{delim}")
                last_idx = len(content)
                break
        after = content[last_idx:]
        if after.strip():
            pieces.append(f"{delim}{after}{delim}")
        return "".join(pieces)

    res = re.sub(r"\$\$[\s\S]*?\$\$", _unwrap_math_block, text)
    res = re.sub(r"\$[^\$]*\$", _unwrap_math_block, res)
    return res


def check_synthetic_boilerplate_distractors(
    correct_content: Optional[str],
    distractor_contents: List[str],
) -> List[str]:
    """Detects trivial synthetic boilerplate distractor options (R-18).
    
    Catches:
    1. Symmetric antonym inversion ('converge con X' vs 'diverge con Y').
    2. Repetitive skeleton boilerplate (>=4 distractors with identical phrase structure).
    """
    errors: List[str] = []
    if not distractor_contents:
        return errors

    def _skeleton(s: str) -> str:
        s_low = s.lower()
        s_low = re.sub(r"\b\d+(?:\.\d+)?\b", "<NUM>", s_low)
        s_low = re.sub(r"[^\w\s<>+\-*/=^\\{}()]", " ", s_low)
        return re.sub(r"\s+", " ", s_low).strip()

    # 1. Repetitive prose skeleton across distractors (>= 4 share same skeleton of >= 20 chars)
    # Ignore test dummy fixtures and pure mathematical/numerical expressions (< 10 prose letters outside $...$)
    skel_counts: Dict[str, List[str]] = {}
    for d in distractor_contents:
        if re.search(r"\b(?:distractor|dummy|placeholder)\b", d, re.IGNORECASE):
            continue
        unwrapped_d = _unwrap_text_in_math(d)
        prose_outside = re.sub(r"\$\$[\s\S]*?\$\$|\$[^\$]*\$", " ", unwrapped_d)
        if len(re.sub(r"[^a-zA-ZáéíóúñÁÉÍÓÚÑ]", "", prose_outside)) < 10:
            continue
        sk = _skeleton(unwrapped_d)
        if len(sk) >= 20:
            skel_counts.setdefault(sk, []).append(d)
    for sk, group in skel_counts.items():
        if len(group) >= 4:
            errors.append(
                f"Synthetic boilerplate distractor pattern detected: repetitive trivial template across {len(group)} options ('{group[0][:60]}...')."
            )
            break

    # 2. Symmetric antonym pairing with correct answer
    if correct_content:
        unwrapped_correct = _unwrap_text_in_math(correct_content)
        c_low = unwrapped_correct.lower()
        for w1, w2 in ANTONYM_PAIRS:
            has_w1 = bool(re.search(rf"\b{w1}\b", c_low))
            has_w2 = bool(re.search(rf"\b{w2}\b", c_low))
            if has_w1 and not has_w2:
                c_norm = re.sub(rf"\b{w1}\b", "<SYM>", c_low)
                c_sk = _skeleton(c_norm)
                for d in distractor_contents:
                    unwrapped_d = _unwrap_text_in_math(d)
                    d_low = unwrapped_d.lower()
                    if re.search(rf"\b{w2}\b", d_low):
                        d_norm = re.sub(rf"\b{w2}\b", "<SYM>", d_low)
                        d_sk = _skeleton(d_norm)
                        if c_sk == d_sk and len(c_sk) >= 15:
                            errors.append(
                                f"Synthetic boilerplate distractor pattern detected: symmetric antonym pair ('{w1}' vs '{w2}') in '{d[:60]}...'."
                            )
                            break
            elif has_w2 and not has_w1:
                c_norm = re.sub(rf"\b{w2}\b", "<SYM>", c_low)
                c_sk = _skeleton(c_norm)
                for d in distractor_contents:
                    unwrapped_d = _unwrap_text_in_math(d)
                    d_low = unwrapped_d.lower()
                    if re.search(rf"\b{w1}\b", d_low):
                        d_norm = re.sub(rf"\b{w1}\b", "<SYM>", d_low)
                        d_sk = _skeleton(d_norm)
                        if c_sk == d_sk and len(c_sk) >= 15:
                            errors.append(
                                f"Synthetic boilerplate distractor pattern detected: symmetric antonym pair ('{w2}' vs '{w1}') in '{d[:60]}...'."
                            )
                            break
    return errors


# ============================================================================
# Item-Level Pedagogical & Psychometric Linters (Shift-Left from Audit Engine)
# ============================================================================

_TELLTALE_PATTERNS = [
    re.compile(r"\b(err[oó]neamente|incorrectamente|falsamente)\b", re.IGNORECASE),
    re.compile(r"\b(derivada\s+err[oó]nea|f[oó]rmula\s+err[oó]nea|c[aá]lculo\s+err[oó]neo)\b", re.IGNORECASE),
    re.compile(r"\b(omitiendo\s+(elevar|multiplicar|dividir|sumar|restar))\b", re.IGNORECASE),
    re.compile(r"\b(confundiendo\s+con|al\s+rev[eé]s)\b", re.IGNORECASE),
    re.compile(r"\b(factorizando\s+err[oó]neamente|con\s+signos\s+positivos\s+incorrectos)\b", re.IGNORECASE),
]

_PARENTHETICAL_TELLTALE_PAT = re.compile(
    r"\(\s*(?:confusi[oó]n|error|omisi[oó]n|sesgo|falsamente|definici[oó]n\s+err[oó]nea|desplazamiento\s+err[oó]neo|c[aá]lculo\s+err[oó]neo)[^)]*\)",
    re.IGNORECASE,
)

_SYNTHETIC_PREFIX_PAT = re.compile(r"^\s*(?:Opci[oó]n|Alternativa|Variante)\s+(?:alterna\s+)?\d+\s*:?", re.IGNORECASE)

_PADDING_SUFFIX_PAT = re.compile(
    r",\s*(?:para\s+los\s+par[aá]metros\s+bajo\s+an[aá]lisis|bajo\s+las\s+condiciones\s+del\s+modelo|seg[uú]n\s+el\s+marco\s+te[oó]rico\s+establecido|en\s+el\s+contexto\s+del\s+sistema\s+analizado|seg[uú]n\s+los\s+supuestos\s+cl[aá]sicos\s+del\s+modelo|bajo\s+las\s+hip[oó]tesis\s+del\s+modelo|para\s+la\s+muestra\s+de\s+datos\s+observada|de\s+acuerdo\s+con\s+la\s+teor[ií]a\s+econom[eé]trica|en\s+la\s+formulaci[oó]n\s+matricial\s+considerada|en\s+el\s+contexto\s+del\s+contraste\s+analizado|en\s+el\s+marco\s+de\s+la\s+especificaci[oó]n)(?:,\s*[^.]{10,60})?\s*\.?\s*$",
    re.IGNORECASE,
)

_FORALL_EPS_PAT = re.compile(r"(?:para\s+todo(?:\s+margen)?\s+\$?\\(?:var)?epsilon\s*>\s*0|\\forall\s+\\(?:var)?epsilon\s*>\s*0)", re.IGNORECASE)
_BOUND_CONSTANT_FORALL_PAT = re.compile(r"(?:para\s+todo(?:\s+\w+)?|\\forall)\s+\$?\\(?:var)?epsilon\s*=\s*-?\d+(?:\.\d+)?", re.IGNORECASE)
_HARDCODED_INEQ_PAT = re.compile(r"(?:\\le|\\ge|<|>)\s*0\.\d+")

_POISONED_CONSIDER_PAT = re.compile(
    r"asegurando\s+considerar\s+adecuadamente:\s*(omitir|confundir|ignorar|olvidar|suponer\s+err[oó]neamente|asumir\s+que|reemplazar\s+err[oó]neamente|dividir\s+err[oó]neamente|no\s+elevar)",
    re.IGNORECASE,
)
_SYMBOLIC_POISON_PAT = re.compile(
    r"(?:asegurando\s+considerar\s+adecuadamente|eval[uú]e\s+posibles\s+desv[ií]os\s+al\s+considerar):\s*\$",
    re.IGNORECASE,
)
_CONSIDER_EXTRACT_PAT = re.compile(
    r"(?:asegurando\s+considerar\s+adecuadamente|eval[uú]e\s+posibles\s+desv[ií]os\s+al\s+considerar):\s*(.+)$",
    re.IGNORECASE,
)
_STUB_HINT_PAT = re.compile(r"^(?:C|H|Hab|Fact|Concept|Skill)-\d+$", re.IGNORECASE)


def check_item_level_options_integrity(
    options: List[Dict[str, Any]],
    interaction_type: str = "multiple_choice_7_options",
) -> List[str]:
    """Inspects option contents for telltales, synthetic cloning, padding, and vacuous quantifiers."""
    errors: List[str] = []
    if not isinstance(options, list):
        return errors

    correct_texts = []
    distractor_texts = []

    for opt_idx, opt in enumerate(options):
        if not isinstance(opt, dict):
            continue
        text = str(opt.get("content") if "content" in opt else (opt.get("text") or opt.get("value") or "")).strip()
        is_correct = bool(opt.get("is_correct", False))

        if is_correct:
            correct_texts.append(text)
        else:
            distractor_texts.append(text)

            # 1. Distractor confessions / telltale cues in visible text
            for pat in _TELLTALE_PATTERNS:
                m = pat.search(text)
                if m:
                    errors.append(
                        f"Metainformación delatora en distractor visible opción {opt_idx + 1}: '{m.group(0)}'"
                    )
                    break

            # 2. Cloned synthetic prefix
            m_syn = _SYNTHETIC_PREFIX_PAT.search(text)
            if m_syn:
                errors.append(
                    f"Distractor con prefijo sintético de clonación ('{m_syn.group(0).strip()}') en opción {opt_idx + 1}"
                )

        # 3. Parenthetical telltale clue (checked on all options)
        m_pt = _PARENTHETICAL_TELLTALE_PAT.search(text)
        if m_pt:
            errors.append(
                f"Metainformación delatora parentética en opción visible {opt_idx + 1}: '{m_pt.group(0)}'"
            )

        # 4. Length-padding suffixes (anti-gaming)
        m_pad = _PADDING_SUFFIX_PAT.search(text)
        if m_pad:
            errors.append(
                f"Relleno artificial de longitud en opción {opt_idx + 1} para evadir [R-15]: '{m_pad.group(0).strip()}'"
            )

        # 5. Vacuous universal quantifier instantiation
        has_bound_const = bool(_BOUND_CONSTANT_FORALL_PAT.search(text))
        has_vacuous_forall = False
        if _FORALL_EPS_PAT.search(text):
            prefix_part = _FORALL_EPS_PAT.split(text)[0]
            if "\\varepsilon" not in prefix_part and "\\epsilon" not in prefix_part and _HARDCODED_INEQ_PAT.search(prefix_part):
                has_vacuous_forall = True
        if has_bound_const or has_vacuous_forall:
            errors.append(
                f"Corrupción matemática de cuantificador universal en opción {opt_idx + 1}: "
                f"sustituye '\\varepsilon' por constante numérica dejando 'para todo \\varepsilon > 0' vacuo."
            )

    return errors


def check_item_level_scaffolding_integrity(
    hints: List[Any],
    correct_texts: Optional[List[str]] = None,
    distractor_texts: Optional[List[str]] = None,
) -> List[str]:
    """Audits hints for anti-socratic poisoning, stub hints, and premature answer leaks."""
    errors: List[str] = []
    if not isinstance(hints, list) or not hints:
        return errors

    clean_hints = [h.get("text", "") if isinstance(h, dict) else str(h) for h in hints]
    c_texts = [ct.strip("$").strip() for ct in (correct_texts or []) if len(ct.strip("$").strip()) >= 15]
    d_cores = [dt.strip("$").strip().rstrip(".") for dt in (distractor_texts or []) if len(dt.strip("$").strip()) >= 12]

    for h_idx, h_txt in enumerate(clean_hints):
        if not h_txt or not isinstance(h_txt, str):
            continue
        h_clean = h_txt.strip()

        # 1. Stub competency ID hints check
        if _STUB_HINT_PAT.match(h_clean):
            errors.append(f"Pista {h_idx + 1} es un ID de competencia stub ('{h_clean}') en lugar de andamiaje socrático.")

        # 2. Poisoned hints
        m_pois = _POISONED_CONSIDER_PAT.search(h_txt) or _SYMBOLIC_POISON_PAT.search(h_txt)
        if m_pois:
            errors.append(
                f"Envenenamiento anti-socrático en pista {h_idx + 1}: instruye 'considerar adecuadamente' un distractor o error conceptual ('{m_pois.group(0)[:60]}')."
            )
        elif "asegurando considerar adecuadamente:" in h_txt.lower():
            m_ext = _CONSIDER_EXTRACT_PAT.search(h_txt)
            if m_ext:
                injected = m_ext.group(1).strip().rstrip(".").strip("$").strip()
                for dc in d_cores:
                    if dc and (dc in injected or (len(injected) >= 14 and injected in dc)):
                        errors.append(
                            f"Envenenamiento anti-socrático en pista {h_idx + 1}: inyecta fórmula de distractor tras 'considerar adecuadamente': '{injected[:60]}'."
                        )
                        break

        # 3. Premature answer leak in early hints (leaving the final hint for operational review)
        if h_idx < max(1, len(clean_hints) - 1):
            for ct in c_texts:
                if ct in h_txt:
                    errors.append(
                        f"Fuga prematura de clave correcta en Pista {h_idx + 1} antes del andamiaje final: '{ct[:60]}'."
                    )
                    break

    return errors


def check_scaffolding_answer_leaks(hints: List[Any]) -> List[str]:
    """Detects mechanical answer leaks in scaffolding hints (R-19)."""
    errors: List[str] = []
    if not hints or not isinstance(hints, list):
        return errors

    elimination_patterns = [
        re.compile(r"\b(?:descarte|elimine|descartar|eliminar|descarta|elimina)\b.{1,50}\b(?:respuestas|opciones|alternativas|las\s+que|aquellas)\b", re.IGNORECASE),
        re.compile(r"\b(?:descarte|elimine|descarta|elimina)\s+(?:las|cualquier|todas|los)\b", re.IGNORECASE),
        re.compile(r"\b(?:descarte|elimine|descarta|elimina)\s+(?:opciones|respuestas)\b", re.IGNORECASE),
    ]

    for idx, h in enumerate(hints):
        text = h.get("text", "") if isinstance(h, dict) else str(h)
        for pat in elimination_patterns:
            m = pat.search(text)
            if m:
                snippet = m.group(0)
                errors.append(
                    f"Scaffolding answer leak detected in hint {idx + 1}: mechanical elimination rule ('{snippet}') leaks answer selection."
                )
                break
    return errors



def check_unrendered_placeholders(
    text: str,
    context: str = "text",
    variables: Optional[Dict[str, Any]] = None,
) -> List[str]:
    """Deterministically detect unresolved PrairieLearn (@var@/@var:fmt@) and uninterpolated ({var}/{var:fmt}) placeholders.
    
    Catches:
    1. Any unresolved PrairieLearn token @ident@ or @ident:fmt@.
    2. Any uninterpolated {key} (or {key:fmt}) where key is in variables, OR standalone {ident}
       outside LaTeX macro arguments, avoiding false positives on legitimate LaTeX like
       \\frac{delta}{2}, \\frac{delta}{n}, \\text{delta}, x_{delta}, x^{delta}, \\begin{matrix}, \\operatorname{plim}.
    """
    errors: List[str] = []
    if not isinstance(text, str):
        return errors
    if not text.strip():
        return errors

    # 1. Detect unresolved PrairieLearn tokens: @var@ or @var:fmt@
    for m in _PL_TOKEN_PATTERN.finditer(text):
        token = m.group(1)
        errors.append(f"Unresolved PrairieLearn template token '@{token}@' detected in {context}.")

    # 2. Detect uninterpolated template variables: {var} or {var:fmt}
    math_spans = [m_s.span() for m_s in re.finditer(r"\$\$[\s\S]*?\$\$|\$[^\$]+?\$", text)]
    def is_in_math_span(pos: int) -> bool:
        return any(s_pos <= pos < e_pos for s_pos, e_pos in math_spans)

    for m in re.finditer(r"\{([a-zA-Z0-9_,\s:.+\-%]+)\}", text):
        inner = m.group(1).strip()
        letters = re.findall(r"[a-zA-Z]", inner)
        if ":" not in inner and letters and all(c.isupper() for c in letters):
            continue
        if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*(?::[^{}\s]+)?$", inner):
            continue
        var_name = inner
        var_key = inner.split(":")[0]
        start = m.start()
        prefix = text[:start].rstrip()

        # Legitimate LaTeX: preceded by escape '\' (odd number of backslashes), subscript '_', or superscript '^'
        num_slashes_before = len(text[:start]) - len(text[:start].rstrip("\\"))
        if num_slashes_before % 2 == 1:
            continue
        if ":" not in inner and (
            (start > 0 and text[start - 1] in ("_", "^"))
            or prefix.endswith(("_", "^"))
        ):
            continue

        # Legitimate LaTeX: immediately followed by subscript '_' or superscript '^' (e.g. {k}^*, {r}_t)
        after = text[m.end():].lstrip()
        if after.startswith(("^", "_")):
            continue

        # Legitimate LaTeX: argument of a valid LaTeX macro e.g. \frac, \text, \mathbf, \begin, \sqrt[...]
        m_cmd = re.search(r"\\([a-zA-Z]+)\*?(\[[^\]]*\])?\s*$", prefix)
        if ":" not in inner and m_cmd and m_cmd.group(1) in _LATEX_ARG_MACROS:
            continue

        # Legitimate LaTeX: subsequent argument of a multi-arg LaTeX command e.g. \frac{a}{b}, \frac{d\dot{k}}{dk}
        if ":" not in inner:
            is_subsequent_latex_arg = False
            s = prefix
            while s.endswith("}"):
                depth = 0
                idx = len(s) - 1
                while idx >= 0:
                    if s[idx] == "}":
                        depth += 1
                    elif s[idx] == "{":
                        depth -= 1
                        if depth == 0:
                            break
                    idx -= 1
                if depth == 0 and idx >= 0:
                    s = s[:idx].rstrip()
                    m_sub = re.search(r"\\([a-zA-Z]+)\*?(\[[^\]]*\])?$", s)
                    if m_sub and m_sub.group(1) in _LATEX_ARG_MACROS:
                        is_subsequent_latex_arg = True
                        break
                else:
                    break

            if is_subsequent_latex_arg:
                continue

            # Check if this was an unescaped LaTeX math command (already reported separately in validate_katex_syntax)
            if re.search(rf"\b({MATH_ACCENT_COMMANDS})\s*$", prefix):
                continue

        # If variable key is known in variables, it MUST NOT be left as {var_key}
        # If variable is not in variables: short variables (<=2 chars) inside math blocks without format spec are allowed
        is_known_var = bool(variables and var_key in variables)
        if not is_known_var and is_in_math_span(start) and ":" not in inner and not inner.endswith(("_val", "_num", "_str", "_res")) and inner.isalpha() and len(inner) <= 2:
            continue

        errors.append(f"Unsubstituted template variable '{{{var_name}}}' detected in {context}.")

    return errors


def validate_katex_syntax(
    text: str,
    context: str,
    allow_template_vars: bool = False,
    variables: Optional[Dict[str, Any]] = None,
) -> List[str]:
    """Validate KaTeX delimiter balance, absence of $$$, {{/}}, macro arity, environments, delimiters, and unsubstituted {var}."""
    errors: List[str] = []
    if not isinstance(text, str):
        return errors
    if not text.strip():
        return errors

    # 1. Triple dollar delimiters
    if "$$$" in text:
        errors.append(f"Triple dollar delimiter '$$$' detected in {context}.")

    # 2. Residual double curly braces (paired template placeholders like {{var}} or empty/orphan {{...}})
    if re.search(r"\{\{\s*\}\}", text):
        errors.append(f"Empty double curly braces ('{{{{}}}}') detected in {context}.")
    if not allow_template_vars:
        if re.search(r"\{\{\s*[a-zA-Z0-9_]+\s*\}\}", text) or re.search(r"(?<!\\)\{\{", text):
            errors.append(f"Residual double curly braces ('{{{{' or '}}}}') detected in {context}.")

    # 3. Balanced '$' delimiters (stripping only odd-backslash escaped dollars \$)
    clean_text = re.sub(r"(?<!\\)(?:\\\\)*\\\$", "", text)
    if clean_text.count("$$") % 2 != 0:
        errors.append(f"Unbalanced display math delimiter '$$' in {context}.")
    else:
        inline_text = clean_text.replace("$$", "")
        if inline_text.count("$") % 2 != 0:
            errors.append(f"Unbalanced inline math delimiter '$' in {context}.")

    # 4. Balanced curly braces and pykatex rendering check inside LaTeX math blocks
    math_matches = re.finditer(r"\$\$(.*?)\$\$|\$([^\$]+?)\$", text, flags=re.DOTALL)
    for mb in math_matches:
        raw_match = mb.group(0)
        is_disp = raw_match.startswith("$$")
        block = mb.group(1) if is_disp else mb.group(2)
        if not block:
            continue
        clean_block = block.replace(r"\{", "").replace(r"\}", "")
        if clean_block.count("{") != clean_block.count("}"):
            errors.append(f"Unbalanced curly braces in LaTeX math expression in {context}: '{clean_block[:60]}...'")

        # PyKaTeX rendering verification with LRU cache
        has_tmpl_token = bool(re.search(r"@[A-Za-z0-9_]+@|\{[a-zA-Z0-9_]+\}", block))
        if not (allow_template_vars and has_tmpl_token):
            success, render_err = _render_katex_safe(block.strip(), is_disp)
            if not success and render_err:
                errors.append(f"KaTeX parse error in {context}: {render_err}")

    # 5. Unclosed nested accent/style macros (e.g. \hat{\boldsymbol{\beta}} with missing outer brace)
    accent_macros = r"(?:hat|bar|tilde|vec|dot|ddot|acute|grave|check|breve|mathring|widehat|widetilde|overline|underline)"
    style_macros = r"(?:boldsymbol|mathbf|bm|mathit|mathrm|mathcal|text|symbf)"
    nested_accent_pattern = re.compile(
        rf"\\({accent_macros})\s*\{{\s*\\({style_macros})\{{([^{{}}]*)\}}(?!\s*\}})"
    )
    for m in nested_accent_pattern.finditer(text):
        accent_name = m.group(1)
        style_name = m.group(2)
        inner_content = m.group(3)
        errors.append(
            f"Unclosed nested macro brace detected in {context}: '\\{accent_name}{{\\{style_name}{{{inner_content}}}}}' requires closing brace '}}'."
        )

    # 6. Macro arity validation (\frac, \binom, \overset, \underset, etc. require 2 arguments)
    two_arg_macros = re.compile(r"\\(frac|dfrac|tfrac|cfrac|binom|overset|underset)\b")
    for m in two_arg_macros.finditer(text):
        macro_name = m.group(1)
        pos = m.end()
        # skip whitespace
        while pos < len(text) and text[pos].isspace():
            pos += 1

        # Must start with '{'
        if pos >= len(text) or text[pos] != "{":
            errors.append(f"LaTeX macro '\\{macro_name}' missing argument brackets '{{...}}' in {context}.")
            continue

        # Parse first argument
        depth1 = 1
        pos += 1
        while pos < len(text) and depth1 > 0:
            ch = text[pos]
            if ch == "$" and not (pos > 0 and text[pos - 1] == "\\"):
                break
            if ch == "\\" and pos + 1 < len(text):
                pos += 2
                continue
            if ch == "{":
                depth1 += 1
            elif ch == "}":
                depth1 -= 1
            pos += 1

        if depth1 != 0:
            errors.append(f"LaTeX macro '\\{macro_name}' has unclosed first argument in {context}.")
            continue

        # Skip whitespace between arguments
        while pos < len(text) and text[pos].isspace():
            pos += 1

        # Must start with '{' for second argument
        if pos >= len(text) or text[pos] != "{":
            errors.append(f"LaTeX macro '\\{macro_name}' requires 2 arguments, but second argument is missing in {context}.")
            continue

        # Parse second argument
        depth2 = 1
        pos += 1
        while pos < len(text) and depth2 > 0:
            ch = text[pos]
            if ch == "$" and not (pos > 0 and text[pos - 1] == "\\"):
                break
            if ch == "\\" and pos + 1 < len(text):
                pos += 2
                continue
            if ch == "{":
                depth2 += 1
            elif ch == "}":
                depth2 -= 1
            pos += 1

        if depth2 != 0:
            errors.append(f"LaTeX macro '\\{macro_name}' has unclosed second argument in {context}.")
            continue

    # 7. Unclosed LaTeX environments (\begin{env} ... \end{env})
    env_matches = re.finditer(r"\\(begin|end)\{([a-zA-Z*]+)\}", text)
    env_stack: List[str] = []
    for em in env_matches:
        action = em.group(1)
        env_name = em.group(2)
        if action == "begin":
            env_stack.append(env_name)
        else:
            if not env_stack:
                errors.append(f"Unmatched LaTeX environment close '\\end{{{env_name}}}' in {context}.")
            else:
                last_env = env_stack.pop()
                if last_env != env_name:
                    errors.append(
                        f"Mismatched LaTeX environment: '\\begin{{{last_env}}}' closed by '\\end{{{env_name}}}' in {context}."
                    )
    while env_stack:
        env_name = env_stack.pop()
        errors.append(f"Unclosed LaTeX environment '\\begin{{{env_name}}}' in {context}.")

    # 8. Unclosed scalable delimiters (\left( ... \right), \left[ ... \right], \left\{ ... \right\})
    left_paren = len(re.findall(r"\\left\s*\(", text))
    right_paren = len(re.findall(r"\\right\s*\)", text))
    if left_paren > right_paren:
        errors.append(f"Unclosed scalable delimiter '\\left(' without matching '\\right)' in {context}.")
    elif right_paren > left_paren:
        errors.append(f"Unmatched scalable delimiter '\\right)' without matching '\\left(' in {context}.")

    left_bracket = len(re.findall(r"\\left\s*\[", text))
    right_bracket = len(re.findall(r"\\right\s*\]", text))
    if left_bracket > right_bracket:
        errors.append(f"Unclosed scalable delimiter '\\left[' without matching '\\right]' in {context}.")
    elif right_bracket > left_bracket:
        errors.append(f"Unmatched scalable delimiter '\\right]' without matching '\\left[' in {context}.")

    left_brace = len(re.findall(r"\\left\s*\\\{", text))
    right_brace = len(re.findall(r"\\right\s*\\\}", text))
    if left_brace > right_brace:
        errors.append(f"Unclosed scalable delimiter '\\left\\{{' without matching '\\right\\}}' in {context}.")
    elif right_brace > left_brace:
        errors.append(f"Unmatched scalable delimiter '\\right\\}}' without matching '\\left\\{{' in {context}.")

    total_left = len(re.findall(r"\\left\b", text))
    total_right = len(re.findall(r"\\right\b", text))
    if total_left > total_right and left_paren == right_paren and left_bracket == right_bracket and left_brace == right_brace:
        errors.append(f"Unclosed scalable delimiter '\\left' without matching '\\right' in {context}.")
    elif total_right > total_left and left_paren == right_paren and left_bracket == right_bracket and left_brace == right_brace:
        errors.append(f"Unmatched scalable delimiter '\\right' without matching '\\left' in {context}.")

    # 9. Unescaped LaTeX math commands: dot{w}, bar{k}, frac{a}{b}, etc.
    # Must be caught even when allow_template_vars=True
    MATH_ACCENT_COMMANDS = (
        r"dot|ddot|hat|bar|tilde|vec|breve|check|acute|grave|mathring|"
        r"textbf|textit|textrm|textsf|texttt|mathrm|mathbf|mathit|mathsf|mathtt|"
        r"mathcal|mathbb|mathfrak|mathscr|operatorname|sqrt|frac|dfrac|tfrac|"
        r"binom|overset|underset|stackrel"
    )
    for m_cmd in re.finditer(rf"(?<!\\)\b({MATH_ACCENT_COMMANDS})\s*\{{([^{{}}\n]+)\}}", text):
        cmd_name = m_cmd.group(1)
        arg = m_cmd.group(2).strip()
        errors.append(
            f"Unescaped LaTeX math command '{cmd_name}{{{arg}}}' detected in {context}. "
            f"Must be prefixed with '\\' and enclosed in '$...$' (e.g. '$\\{cmd_name}{{{arg}}}$')."
        )

    # 10. Unsubstituted template variables: {var} or {var:.4f} and unresolved PrairieLearn tokens @var@
    # Explicitly permit uppercase set/tuple notation (e.g. {K}, {Y}, {K, L}) in text
    if not (allow_template_vars or context.startswith("stem_variants")):
        errors.extend(check_unrendered_placeholders(text, context, variables=variables))

    # 11. Over-escaped LaTeX commands: \\frac, \\text, \\to, \\alpha, etc. in memory (R-23)
    # Uses negative lookbehind (?<!\\) and requires an even number of backslashes (\\, \\\\, etc.)
    # to avoid false positives on matrix row breaks immediately preceding a command (e.g. \\\frac = \\ + \frac).
    for m_over in re.finditer(r"(?<!\\)(?:\\\\)+([a-zA-Z]+)", text):
        cmd_name = m_over.group(1)
        errors.append(
            f"Over-escaped LaTeX command '\\\\{cmd_name}' detected in {context} (R-23). "
            f"Use single backslash '\\{cmd_name}' in memory."
        )

    # 12. Forbidden linebreak '\\' inside inline math '$...$' outside matrix/cases environment (R-23)
    no_disp = re.sub(r"\$\$[\s\S]*?\$\$", "", re.sub(r"(?<!\\)(?:\\\\)*\\\$", "", text))
    env_cleaner = re.compile(
        r"\\begin\s*\{+\s*((?:[a-zA-Z]*matrix|cases|aligned|array|split|gathered)\*?)\s*\}+"
        r"((?:(?!\\begin)[\s\S])*?)"
        r"\\end\s*\{+\s*\1\s*\}+"
    )
    for m_inl in re.finditer(r"\$([^\$]+)\$", no_disp):
        inner_no_env = m_inl.group(1)
        # Iteratively strip innermost environments first to safely support nested environments
        for _ in range(10):
            inner_no_env, n_replaced = env_cleaner.subn("", inner_no_env)
            if n_replaced == 0:
                break
        if re.search(r"\\\\(?![a-zA-Z])", inner_no_env):
            errors.append(
                f"Forbidden linebreak '\\\\' inside inline math '$...$' outside matrix/cases environment in {context} (R-23)."
            )

    # 13. Unsupported macros (\centernot) and unescaped underscores in \text{...} (R-23)
    if re.search(r"\\centernot\b", text):
        errors.append(
            f"Unsupported LaTeX macro '\\centernot' detected in {context} (R-23); "
            f"use '\\nRightarrow', '\\nrightarrow', or '\\not'."
        )
    for m_txt in re.finditer(r"\\text\s*\{([^{}$]*)\}", text):
        if re.search(r"(?<!\\)_", m_txt.group(1)):
            errors.append(
                f"Unescaped underscore '_' inside '\\text{{{m_txt.group(1)}}}' in {context} causes KaTeX ParseError."
            )

    # 14. KaTeX prose overflow in text macros (\text{...}, \textrm{...}, \mathrm{...})
    # Blocks exceeding 45 characters must be rejected with [KATEX-PROSE-OVERFLOW]
    prose_macro_pat = re.compile(r"\\(text|textrm|mathrm)\s*\{")
    for m in prose_macro_pat.finditer(text):
        start_brace = m.end() - 1
        depth = 1
        pos = start_brace + 1
        n = len(text)
        while pos < n and depth > 0:
            ch = text[pos]
            if ch == "\\" and pos + 1 < n:
                pos += 2
                continue
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
            pos += 1
        if depth == 0:
            inner = text[start_brace + 1 : pos - 1]
            if len(inner) > 45:
                macro_name = m.group(1)
                snippet = inner[:30] + "..." if len(inner) > 30 else inner
                errors.append(
                    f"[KATEX-PROSE-OVERFLOW] KaTeX text macro '\\{macro_name}{{{snippet}}}' exceeds 45 characters "
                    f"({len(inner)} chars) in {context}. Split into markdown prose outside math delimiters."
                )
            inner_text_only = re.sub(r"\$\$[\s\S]*?\$\$|\$[^\$]+?\$", "", inner)
            if re.search(r"(?<!\\)_", inner_text_only):
                macro_name = m.group(1)
                errors.append(
                    f"Unescaped underscore '_' inside '\\{macro_name}{{{inner}}}' in {context} causes KaTeX ParseError."
                )

    # 15. LaTeX math commands with backslash exposed outside math delimiters '$...$' or '$$...$$'
    # Skips purely algebraic fields (e.g. canonical_algebraic or expression in FIB) which are mathematical formulas by specification
    if not ("canonical_algebraic" in context or "expression" in context):
        clean_no_math = re.sub(r"\$\$[\s\S]*?\$\$", "", clean_text)
        clean_no_math = re.sub(r"\$[^\$]*?\$", "", clean_no_math)
        EXPOSED_LATEX_CMD = (
            r"operatorname|frac|dfrac|tfrac|cfrac|binom|sqrt|mathrm|mathbf|mathbb|mathcal|mathscr|mathfrak|"
            r"bar|hat|tilde|vec|dot|ddot|acute|grave|check|breve|mathring|widehat|widetilde|overline|underline|"
            r"sum|prod|int|iint|iiint|oint|lim|limsup|liminf|infty|"
            r"Rightarrow|rightarrow|Leftarrow|leftarrow|Leftrightarrow|leftrightarrow|xrightarrow|xleftarrow|"
            r"le|ge|leq|geq|neq|approx|equiv|sim|simeq|subset|supset|subseteq|supseteq|notin|cap|cup|"
            r"times|div|pm|mp|cdot|cdots|ldots|ddots|partial|nabla|begin|end"
        )
        for m_exp in re.finditer(rf"(?<!\\)\\(?:{EXPOSED_LATEX_CMD})\b", clean_no_math):
            cmd = m_exp.group(0)
            errors.append(
                f"LaTeX command '{cmd}' exposed outside '$...$' delimiters in {context}. "
                f"Enclose the mathematical expression in '$...$' (e.g. '${cmd}...$')."
            )

    # 16. Vacuous quantifiers (e.g. \forall x = 1, \exists y = 0)
    for m_vac in re.finditer(r"\\(?:forall|exists)\s+[a-zA-Z\\]+\s*=\s*[-+]?\d", text):
        errors.append(f"Vacuous quantifier detected in {context}: '{m_vac.group(0)}'.")

    # 17. Newtonian dot accents on digits (e.g. \dot{0}, \dot{1})
    for m_dot in re.finditer(r"\\dot\{\s*\d+\s*\}", text):
        errors.append(f"Newtonian dot accent on digits detected in {context}: '{m_dot.group(0)}'.")

    return errors


def check_instance_invariants(
    instance: Dict[str, Any],
    interaction_type: str,
    strict_length_bounds: bool = True,
    variables: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    """Check whether a generated question instance satisfies all invariant rules.
    
    Args:
        instance: The dictionary of generated parameters/options/hints.
        interaction_type: "multiple_choice_7_options", "fill_in_the_blank", or "multiple_select".
        strict_length_bounds: Whether to enforce the 0.80/1.20 length bound on MC7.
        variables: Optional generator variables dict to detect unrendered placeholders.
        
    Returns:
        (is_valid, list_of_error_messages)
    """
    errors: List[str] = []
    effective_vars = variables if variables is not None else (instance.get("vars") or instance.get("variables"))

    stem = instance.get("stem", "")
    if not stem or not isinstance(stem, str) or len(stem.strip()) < 5:
        errors.append("Stem must be a non-empty string with at least 5 characters.")
    if isinstance(stem, str) and stem:
        errors.extend(validate_katex_syntax(stem, "stem", variables=effective_vars))

    hints = instance.get("hints", [])
    if not isinstance(hints, list):
        errors.append(f"Instance hints must be a list (found {type(hints).__name__}).")
    else:
        if not (3 <= len(hints) <= 5):
            errors.append(f"Instance must have between 3 and 5 hints (found {len(hints)}).")
        for idx, hint in enumerate(hints):
            if not isinstance(hint, str) or not hint.strip():
                errors.append(f"Hint {idx + 1} must be a non-empty string.")
            else:
                errors.extend(validate_katex_syntax(hint, f"hint {idx + 1}", variables=effective_vars))

    for sol_key in ("detailed_solution", "solution"):
        solution = instance.get(sol_key)
        if isinstance(solution, str) and solution:
            errors.extend(validate_katex_syntax(solution, sol_key, variables=effective_vars))

    for misc_key in ("misconception_warning", "common_misconception_warning"):
        misc = instance.get(misc_key)
        if isinstance(misc, str) and misc:
            errors.extend(validate_katex_syntax(misc, misc_key, variables=effective_vars))

    options_raw = instance.get("options")
    corr_texts_extracted: List[str] = []
    dist_texts_extracted: List[str] = []
    if isinstance(options_raw, list):
        for idx, opt in enumerate(options_raw):
            if isinstance(opt, dict):
                c = opt.get("content")
                if isinstance(c, str):
                    errors.extend(validate_katex_syntax(c, f"option {idx + 1} content", variables=effective_vars))
                r = opt.get("error_rationale")
                if isinstance(r, str) and r:
                    errors.extend(validate_katex_syntax(r, f"option {idx + 1} error_rationale", variables=effective_vars))
                val_txt = str(opt.get("content") if "content" in opt else (opt.get("text") or opt.get("value") or "")).strip()
                if opt.get("is_correct"):
                    corr_texts_extracted.append(val_txt)
                else:
                    dist_texts_extracted.append(val_txt)

        # Item-level options integrity (telltales, synthetic clone prefix, padding, vacuous quantifiers)
        errors.extend(check_item_level_options_integrity(options_raw, interaction_type))

    # 1. Multiple Choice 7 options
    if interaction_type == "multiple_choice_7_options":
        options = instance.get("options", [])
        if not isinstance(options, list):
            errors.append(f"MC7 requires a list of options (found {type(options).__name__}).")
        else:
            if len(options) != 7:
                errors.append(f"MC7 requires exactly 7 options (found {len(options)}).")

            correct_count = 0
            correct_content = None
            distractor_contents = []

            seen_contents = set()
            for idx, opt in enumerate(options):
                if not isinstance(opt, dict):
                    errors.append(f"Option {idx + 1} is not a valid dictionary.")
                    continue
                
                content = str(opt.get("content", "")).strip()
                if not content:
                    errors.append(f"Option {idx + 1} has empty content.")
                
                # Check option text uniqueness
                norm_content = re.sub(r"\s+", " ", content)
                if norm_content in seen_contents:
                    errors.append(f"Duplicate option content detected: '{content}'")
                seen_contents.add(norm_content)

                if opt.get("is_correct") is True:
                    correct_count += 1
                    correct_content = content
                else:
                    distractor_contents.append(content)
                    rationale = opt.get("error_rationale")
                    if rationale is None or not isinstance(rationale, str) or not rationale.strip():
                        errors.append(
                            f"MC7 option {idx + 1} with is_correct=False must possess a non-empty 'error_rationale'."
                        )

            if correct_count != 1:
                errors.append(f"MC7 must have exactly 1 correct option (found {correct_count}).")

            # Check that distractors are distinct from correct answer
            if correct_content is not None:
                for d in distractor_contents:
                    if d.strip() == correct_content.strip():
                        errors.append(f"Distractor identical to correct answer: '{d}'")

            # Check length anti-giveaway bounds:
            # 0.80 * min(len(D)) <= len(correct) <= 1.20 * max(len(D))
            if strict_length_bounds and correct_content and distractor_contents:
                d_lens = [len(d) for d in distractor_contents]
                min_d = min(d_lens)
                max_d = max(d_lens)
                c_len = len(correct_content)

                if min_d > 0 and max_d > 0:
                    lower_bound = 0.80 * min_d
                    upper_bound = 1.20 * max_d
                    if c_len < lower_bound:
                        errors.append(
                            f"Length anti-giveaway violation: correct option too short ({c_len} chars < {lower_bound:.1f} = 0.80 * min(D))."
                        )
                    elif c_len > upper_bound:
                        errors.append(
                            f"Length anti-giveaway violation: correct option too long ({c_len} chars > {upper_bound:.1f} = 1.20 * max(D))."
                        )

            # Check answer leak in stem or early hints
            if correct_content and len(correct_content) >= 5 and not correct_content.isdigit():
                # Avoid trivial matches like single numbers
                if isinstance(stem, str) and correct_content in stem:
                    errors.append(f"Correct answer '{correct_content}' leaked verbatim in stem text.")
                if hints and len(hints) >= 1 and isinstance(hints[0], str) and correct_content in hints[0]:
                    errors.append(f"Correct answer '{correct_content}' leaked verbatim in first hint.")

            # Check synthetic boilerplate distractor pattern
            bp_errors = check_synthetic_boilerplate_distractors(correct_content, distractor_contents)
            errors.extend(bp_errors)

    # 2. Fill in the blank
    elif interaction_type == "fill_in_the_blank":
        ans = instance.get("correct_answer")
        if ans is None:
            ans = instance.get("correct")
        
        if ans is None:
            errors.append("FIB instance must provide a correct answer.")
        else:
            if isinstance(ans, dict):
                val = ans.get("value") or ans.get("expression") or ans.get("canonical_algebraic")
                if val is None or str(val).strip() == "":
                    errors.append("FIB answer dict missing value/expression/canonical_algebraic.")
                for field in ("value", "expression", "canonical_algebraic"):
                    fval = ans.get(field)
                    if isinstance(fval, str) and fval:
                        errors.extend(validate_katex_syntax(fval, f"correct_answer.{field}", variables=effective_vars))
                for eq_idx, eq in enumerate(ans.get("accepted_equivalents", []) or ans.get("equivalents", [])):
                    if isinstance(eq, str) and eq:
                        errors.extend(validate_katex_syntax(eq, f"correct_answer.accepted_equivalents[{eq_idx}]", variables=effective_vars))
                    elif isinstance(eq, (int, float)):
                        pass
                    else:
                        errors.append(f"Accepted equivalent [{eq_idx}] has invalid type: {type(eq).__name__}")
            elif isinstance(ans, (int, float, str)):
                if str(ans).strip() == "":
                    errors.append("FIB scalar answer is empty.")
                elif isinstance(ans, str):
                    errors.extend(validate_katex_syntax(ans, "correct_answer", variables=effective_vars))
            else:
                errors.append(f"FIB answer format invalid: {type(ans)}")

    # 3. Multiple select
    elif interaction_type == "multiple_select":
        options = instance.get("options", [])
        if not isinstance(options, list):
            errors.append(f"MS requires a list of options (found {type(options).__name__}).")
        else:
            if not (4 <= len(options) <= 6):
                errors.append(f"MS requires 4 to 6 options (found {len(options)}).")

            correct_count = 0
            seen_contents = set()
            for idx, opt in enumerate(options):
                if not isinstance(opt, dict):
                    errors.append(f"Option {idx + 1} is not a valid dictionary.")
                    continue
                content = str(opt.get("content", "")).strip()
                if not content:
                    errors.append(f"Option {idx + 1} has empty content.")
                norm_content = re.sub(r"\s+", " ", content)
                if norm_content in seen_contents:
                    errors.append(f"Duplicate option content detected in MS: '{content}'")
                seen_contents.add(norm_content)

                if opt.get("is_correct") is True:
                    correct_count += 1
                else:
                    rationale = opt.get("error_rationale")
                    if rationale is None or not isinstance(rationale, str) or not rationale.strip():
                        errors.append(
                            f"MS option {idx + 1} with is_correct=False must possess a non-empty 'error_rationale'."
                        )

            # Invariant: 1 <= correct_count <= len(options) - 1
            if len(options) > 0 and not (1 <= correct_count <= len(options) - 1):
                errors.append(
                    f"MS correct count must be between 1 and {len(options) - 1} (found {correct_count} correct out of {len(options)} options)."
                )

            ms_distractors = [
                str(opt.get("content", "")) for opt in options if opt.get("is_correct") is False
            ]
            bp_errors = check_synthetic_boilerplate_distractors(None, ms_distractors)
            errors.extend(bp_errors)

    # Scaffolding progressive hint answer leak and item-level integrity checks across all interaction types
    raw_hints = instance.get("hints", [])
    if isinstance(raw_hints, list) and raw_hints:
        leak_errors = check_scaffolding_answer_leaks(raw_hints)
        errors.extend(leak_errors)
        scaf_errors = check_item_level_scaffolding_integrity(
            raw_hints,
            correct_texts=corr_texts_extracted,
            distractor_texts=dist_texts_extracted,
        )
        errors.extend(scaf_errors)

    return (len(errors) == 0, errors)

