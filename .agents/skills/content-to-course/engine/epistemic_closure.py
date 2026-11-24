"""Static Epistemic Closure Auditor (M17): checks S_sol <= S_stem U S_std without blocking Stage 4."""

import re
from typing import Any, Dict, Iterable, List, Set

from engine.katex_ast import (
    AccentMacroNode,
    AtomNode,
    BinaryMacroNode,
    GroupNode,
    KaTeXAST,
    KaTeXNode,
    MatrixEnvNode,
    SeqNode,
    TextMacroNode,
    UnaryMacroNode,
)

# Standard LaTeX commands, layout/relation operators, and named math functions
STANDARD_LATEX_COMMANDS: Set[str] = {
    "sin", "cos", "tan", "cot", "sec", "csc",
    "arcsin", "arccos", "arctan", "sinh", "cosh", "tanh",
    "ln", "log", "exp", "max", "min", "sup", "inf", "arg", "argmax", "argmin",
    "lim", "limsup", "liminf", "det", "tr", "dim", "ker", "rank", "diag", "plim",
    "Var", "Cov", "Corr", "Pr", "E", "SE", "SD", "df",
    "sum", "prod", "int", "iint", "iiint", "oint",
    "frac", "dfrac", "tfrac", "cfrac", "binom", "dbinom", "tbinom", "sqrt",
    "left", "right", "big", "Big", "bigg", "Bigg",
    "cdot", "times", "div", "pm", "mp", "circ", "bullet", "star",
    "le", "leq", "ge", "geq", "neq", "ne", "approx", "equiv", "sim", "simeq", "propto",
    "to", "rightarrow", "leftarrow", "Rightarrow", "Leftarrow", "leftrightarrow", "Leftrightarrow", "mapsto",
    "in", "notin", "subset", "subseteq", "supset", "supseteq", "cup", "cap", "setminus", "emptyset", "varnothing",
    "forall", "exists", "nexists", "land", "lor", "neg", "lnot",
    "partial", "nabla", "infty", "prime", "degree",
    "quad", "qquad", "hspace", "vspace", "phantom", "hline", "vdots", "cdots", "ddots", "dots", "ldots",
    "begin", "end", "array", "aligned", "cases", "matrix", "pmatrix", "bmatrix", "vmatrix",
    "style", "color", "textcolor", "boxed", "cancel", "bcancel", "xcancel",
    "mid", "parallel", "perp", "angle", "triangle",
    "pmod", "bmod", "mod",
}

# Standard mathematical/statistical constants & canonical auxiliary resolution symbols (S_std)
STD_MATH_SYMBOLS: Set[str] = {
    "e", "i", "j", "d", "pi", r"\pi", r"\infty",
    "C", "C_0", "C_1", "C_2", "c_0", "c_1", "c_2",
    "u", "v", "h",
    r"\lambda", r"\mu",
    "Z", "z", "t", "F", r"\chi",
    "H_0", "H_1", "H", "p", "n",
}

_GREEK_COMMANDS: Set[str] = {
    "alpha", "beta", "gamma", "delta", "epsilon", "varepsilon", "zeta", "eta",
    "theta", "vartheta", "iota", "kappa", "lambda", "mu", "nu", "xi",
    "rho", "varrho", "sigma", "varsigma", "tau", "upsilon", "phi", "varphi",
    "chi", "psi", "omega",
    "Gamma", "Delta", "Theta", "Lambda", "Xi", "Pi", "Sigma", "Upsilon", "Phi", "Psi", "Omega",
}

_PLAIN_FUNCTION_WORDS: Set[str] = {
    "sin", "cos", "tan", "cot", "sec", "csc", "arcsin", "arccos", "arctan",
    "ln", "log", "exp", "sqrt", "abs", "max", "min", "sup", "inf", "plim",
    "lim", "det", "tr", "Var", "Cov", "Corr", "Pr", "sum", "prod", "int",
    "pi", "inf", "infty", "and", "or", "if", "else", "for", "then",
}

_TWO_LETTER_OP_LABELS: Set[str] = {
    "df", "gl", "SE", "SD", "EE", "CV", "CI", "IC", "RC", "tr", "ln", "lg",
    "si", "no", "en", "de", "al", "es", "la", "el", "lo", "un", "su", "se",
}

_COMMON_DIFFERENTIAL_LETTERS: Set[str] = {
    "x", "y", "z", "t", "u", "v", "s", "p", "q", "k", "c", "r", "w", "h",
    "K", "L", "Y", "C", "I", "A", "S", "P", "Q", "X", "T",
}

_MATH_DELIM_RE = re.compile(r"\$\$(.*?)\$\$|\$([^\$]+?)\$", flags=re.DOTALL)
_CMD_RE = re.compile(r"\\([a-zA-Z]+)")
_IDENT_RE = re.compile(r"([a-zA-Z]+(?:_[a-zA-Z0-9]+)?)")
_SUPERSCRIPT_MODIFIER_RE = re.compile(r"(?<=[A-Za-z0-9\}\)])\s*\^\s*(?:\{\s*[cT*]\s*\}|[cT*])(?![A-Za-z0-9])")
_SIGMA_ALGEBRA_RE = re.compile(r"\$\\sigma\$-?\s*[aá]lgebra", re.IGNORECASE)
_PROB_EXPECT_OP_RE = re.compile(r"\b(?:E\s*\[|P\s*\()")
_DIFF_SUB_RE = re.compile(r"^d([A-Za-z])(?:_([A-Za-z0-9]+))?$")


def extract_math_segments(text: str, treat_raw_as_math: bool = False) -> List[str]:
    """Extract LaTeX math segments ($...$, $$...$$) or treat bare symbolic text as math."""
    if not isinstance(text, str) or not text.strip():
        return []
    cleaned = _SIGMA_ALGEBRA_RE.sub(" sigma-algebra ", text)
    matches = list(_MATH_DELIM_RE.finditer(cleaned))
    if matches:
        return [
            (m.group(1) if m.group(0).startswith("$$") else m.group(2)).strip()
            for m in matches
            if (m.group(1) if m.group(0).startswith("$$") else m.group(2)).strip()
        ]
    if treat_raw_as_math:
        stripped = cleaned.strip()
        if re.fullmatch(r"-?\d+(?:[.,]\d+)?(?:\s*%)?", stripped):
            return []
        return [stripped]
    return []


def _extract_bound_vars(math_str: str) -> Set[str]:
    """Detect variables bound locally by quantifiers, sums, products, limits, integration constants, or operators."""
    bound: Set[str] = set()
    # \sum_{i=1}, \prod_{k=1}, \bigcup_{i \in I}, \lim_{h \to 0}
    for m in re.finditer(
        r"\\(?:sum|prod|lim|limsup|liminf|max|min|sup|inf|bigcup|bigcap|argmax|argmin)\s*_\s*\{\s*(\\[a-zA-Z]+|[a-zA-Z]+)\s*(?:=|\\in|\\to|->)",
        math_str,
    ):
        bound.add(m.group(1))
    # Quantifiers: \forall x, \exists \delta
    for m in re.finditer(r"\\(?:forall|exists)\s*(\\[a-zA-Z]+|[a-zA-Z])", math_str):
        bound.add(m.group(1))
    # Integral differentials: \int ... d x  or  dt
    if r"\int" in math_str or r"\frac{d" in math_str:
        for m in re.finditer(r"(?:\\,|\\;|\\:|\s|\b)d\s*(\\[a-zA-Z]+|[a-zA-Z])\b", math_str):
            bound.add(m.group(1))
    # Lowercase integration constant '= c' or '+ c' (explicitly introduced as integration constant)
    if re.search(r"(?:=|\+)\s*c\b", math_str):
        bound.add("c")
    # Probability / expectation operators written without \mathbb or \Pr (e.g. E[X], P(A))
    if re.search(r"\bE\s*\[", math_str):
        bound.add("E")
    if re.search(r"\bP\s*\(", math_str):
        bound.add("P")
    return bound


def _collect_ast_symbols(node: KaTeXNode, symbols: Set[str]) -> None:
    """Recursively collect mathematical symbol tokens from a KaTeXAST node."""
    if isinstance(node, TextMacroNode):
        return
    if isinstance(node, UnaryMacroNode):
        if node.macro in ("operatorname", "mathbb", "mathcal"):
            return
        _collect_ast_symbols(node.arg, symbols)
        return
    if isinstance(node, AccentMacroNode):
        _collect_ast_symbols(node.arg, symbols)
        return
    if isinstance(node, BinaryMacroNode):
        _collect_ast_symbols(node.arg1, symbols)
        _collect_ast_symbols(node.arg2, symbols)
        return
    if isinstance(node, MatrixEnvNode):
        _collect_ast_symbols(node.body, symbols)
        return
    if isinstance(node, (GroupNode, SeqNode)):
        children = node.children
        idx = 0
        while idx < len(children):
            cur = children[idx]
            # Handle braced subscript following a single symbol/atom: e.g. F_{\dot{x}} -> F_{x} or x_{t+1}
            if (
                idx + 1 < len(children)
                and isinstance(cur, AtomNode)
                and (cur.text or "").rstrip().endswith("_")
                and isinstance(children[idx + 1], (GroupNode, AtomNode))
            ):
                _collect_ast_symbols(cur, symbols)
                _collect_ast_symbols(children[idx + 1], symbols)
                idx += 2
                continue
            _collect_ast_symbols(cur, symbols)
            idx += 1
        return
    if isinstance(node, AtomNode):
        raw = _SUPERSCRIPT_MODIFIER_RE.sub("", (node.text or "").strip())
        if not raw:
            return
        if raw.startswith("\\"):
            m_cmd = _CMD_RE.match(raw)
            if m_cmd:
                cmd = m_cmd.group(1)
                if cmd in _GREEK_COMMANDS:
                    symbols.add(f"\\{cmd}")
                elif cmd not in STANDARD_LATEX_COMMANDS and len(cmd) > 1:
                    return
            return
        for m_id in _IDENT_RE.finditer(raw):
            tok = m_id.group(1)
            if tok in _PLAIN_FUNCTION_WORDS or tok in _TWO_LETTER_OP_LABELS:
                continue
            if tok in STD_MATH_SYMBOLS:
                symbols.add(tok)
                continue
            m_diff = _DIFF_SUB_RE.match(tok)
            if m_diff and m_diff.group(1) in _COMMON_DIFFERENTIAL_LETTERS:
                var_letter = m_diff.group(1)
                sub_part = m_diff.group(2)
                symbols.add(f"{var_letter}_{sub_part}" if sub_part else var_letter)
                if sub_part:
                    symbols.add(var_letter)
                continue
            if "_" in tok:
                base, sub = tok.split("_", 1)
                if base in _PLAIN_FUNCTION_WORDS:
                    continue
                if len(base) == 1:
                    symbols.add(tok)
                    symbols.add(base)
                    if len(sub) == 1 and sub.isalpha() and sub not in ("t", "i", "j", "k", "n", "m"):
                        symbols.add(sub)
                elif len(base) <= 2:
                    symbols.add(tok)
                continue
            if len(tok) == 1:
                symbols.add(tok)
            elif len(tok) == 2:
                if tok[1].isdigit() and tok[0] in ("x", "y", "z", "k", "p", "q", "a", "b", "c", "n"):
                    symbols.add(tok)
                    symbols.add(tok[0])
                elif tok.isalpha():
                    symbols.add(tok[0])
                    symbols.add(tok[1])


def extract_symbols_from_text(
    text: str,
    treat_raw_as_math: bool = False,
    strip_bound: bool = False,
) -> Set[str]:
    """Extract free mathematical symbols from LaTeX segments inside text."""
    symbols: Set[str] = set()
    for seg in extract_math_segments(text, treat_raw_as_math=treat_raw_as_math):
        seg_clean = _SUPERSCRIPT_MODIFIER_RE.sub("", seg)
        seg_syms: Set[str] = set()
        ast_node = KaTeXAST.parse(seg_clean)
        _collect_ast_symbols(ast_node, seg_syms)
        if strip_bound:
            bound = _extract_bound_vars(seg_clean)
            seg_syms -= bound
            resolved_syms: Set[str] = set()
            for sym in seg_syms:
                if "_" in sym:
                    base, sub = sym.split("_", 1)
                    if sub in bound:
                        resolved_syms.add(base)
                        continue
                resolved_syms.add(sym)
            seg_syms = resolved_syms
        symbols.update(seg_syms)
    return symbols


def _is_subscripted_known_symbol(sym: str, allowed: Set[str]) -> bool:
    """Return True if sym is Base_Sub where Base and all subscript parts are digits, '*', or already allowed."""
    if "_" not in sym:
        return False
    base, sub = sym.split("_", 1)
    if base not in allowed:
        return False
    if not sub or sub.isdigit() or sub in ("*", "max", "min", "eq", "opt", "0", "1", "2"):
        return True
    if sub in allowed:
        return True
    # Partial derivatives / repeated indices like f_{KK} or f_{xx}
    return all(ch in allowed or ch.isdigit() for ch in sub)


def _iter_context_texts(instance: Dict[str, Any], norm_type: str) -> Iterable[str]:
    """Yield prompt/context fields visible to the student before answering (never options or solutions)."""
    for key in ("stem", "context", "scenario", "case_text", "problem_statement"):
        val = instance.get(key)
        if isinstance(val, str) and val.strip():
            yield val

    if norm_type == "concept_matching":
        cm = instance.get("concept_matching")
        if isinstance(cm, dict):
            for prem in cm.get("premises") or []:
                if isinstance(prem, dict) and isinstance(prem.get("content"), str):
                    yield prem["content"]
    elif norm_type in ("proof_dag", "adversarial_break"):
        block = instance.get(norm_type)
        if isinstance(block, dict):
            for st_item in block.get("steps") or []:
                if isinstance(st_item, dict) and isinstance(st_item.get("content"), str):
                    yield st_item["content"]
    elif norm_type == "unstructured_model":
        um = instance.get("unstructured_model")
        if isinstance(um, dict):
            p1 = um.get("phase1_variables")
            if isinstance(p1, dict) and isinstance(p1.get("prompt"), str):
                yield p1["prompt"]


def check_epistemic_closure(
    instance: Dict[str, Any],
    interaction_type: str = "",
) -> List[str]:
    """Check static epistemic closure S_sol <= S_stem U S_std; returns warning strings."""
    if not isinstance(instance, dict):
        return []

    norm_type = str(interaction_type or instance.get("interaction_type") or "").strip().lower()
    stem_syms: Set[str] = set()
    for ctx_txt in _iter_context_texts(instance, norm_type):
        stem_syms.update(extract_symbols_from_text(ctx_txt, treat_raw_as_math=False, strip_bound=False))

    sol_syms: Set[str] = set()
    for sol_key in ("detailed_solution", "solution"):
        sol_val = instance.get(sol_key)
        if isinstance(sol_val, str) and sol_val.strip():
            sol_syms.update(extract_symbols_from_text(sol_val, treat_raw_as_math=False, strip_bound=True))

    if norm_type in ("open_symbolic", "sym", "symbolic"):
        exp_ans = instance.get(
            "expected_answer",
            instance.get("correct_answer", instance.get("correct")),
        )
        if isinstance(exp_ans, dict):
            exp_ans = exp_ans.get("expression") or exp_ans.get("canonical_algebraic") or exp_ans.get("value")
        if isinstance(exp_ans, str) and exp_ans.strip():
            sol_syms.update(extract_symbols_from_text(exp_ans, treat_raw_as_math=True, strip_bound=True))

    allowed = stem_syms | STD_MATH_SYMBOLS
    missing = sorted(
        sym for sym in sol_syms
        if sym not in allowed
        and not (sym.startswith("\\") and sym[1:] in STD_MATH_SYMBOLS)
        and not _is_subscripted_known_symbol(sym, allowed)
    )
    if not missing:
        return []

    qid = instance.get("id") or instance.get("template_id") or "question"
    joined = ", ".join(missing)
    return [
        f"[EPISTEMIC-CLOSURE-WARNING] '{qid}': Símbolos en solución/respuesta ({joined}) "
        f"no aparecen definidos en stem (S_sol <= S_stem U S_std)."
    ]


_BACKTICK_IDENT_RE = re.compile(r"`\s*([A-Za-z_][A-Za-z0-9_]*)\s*`")
_SHORT_TEXT_IDENT_RE = re.compile(r"\\(?:text|mathrm)\{\s*([A-Za-z][A-Za-z0-9_]{0,3})\s*\}")
_ANS_LATEX_OR_IDENT_RE = re.compile(r"\\([A-Za-z]+)|([A-Za-z][A-Za-z0-9_]*)")
_SCI_NOTATION_RE = re.compile(r"\b\d+(?:\.\d+)?[eE][+-]?\d+\b")

_SYMBOLIC_STD_CONSTS: Set[str] = {
    "e", "i", "pi", "inf", "infty", "c0", "c1", "c2", "C0", "C1", "C2", "C",
    "true", "false", "nan", "NaN", "t",
}


def extract_open_symbolic_answer_symbols(expr_text: str) -> Set[str]:
    """Extract whole symbolic identifiers from an ASCII/mathjs open_symbolic expected_answer."""
    if not isinstance(expr_text, str) or not expr_text.strip():
        return set()
    stripped = expr_text.strip().strip("$")
    if re.fullmatch(r"-?\d+(?:[.,]\d+)?(?:\s*%)?", stripped):
        return set()
    cleaned = _SCI_NOTATION_RE.sub(" ", stripped)
    found: Set[str] = set()
    for m in _ANS_LATEX_OR_IDENT_RE.finditer(cleaned):
        cmd, ident = m.group(1), m.group(2)
        if cmd:
            if cmd in _GREEK_COMMANDS:
                found.add(f"\\{cmd}")
            continue
        if ident:
            if ident in _PLAIN_FUNCTION_WORDS or ident.lower() in _PLAIN_FUNCTION_WORDS:
                continue
            found.add(ident)
    return found


def _extract_stem_declared_symbols_for_symbolic(stem_text: str) -> Set[str]:
    """Collect declared math symbols, backtick identifiers, and ASCII aliases from stem."""
    declared: Set[str] = set()
    if not isinstance(stem_text, str) or not stem_text.strip():
        return declared

    base_syms = extract_symbols_from_text(stem_text, treat_raw_as_math=False, strip_bound=False)
    for sym in base_syms:
        declared.add(sym)
        if "_" in sym:
            declared.add(sym.replace("_", ""))
        if sym.startswith("\\"):
            declared.add(sym[1:])

    for bt in _BACKTICK_IDENT_RE.findall(stem_text):
        declared.add(bt)
        declared.add(bt.replace("_", ""))

    for seg in extract_math_segments(stem_text, treat_raw_as_math=False):
        for short_txt in _SHORT_TEXT_IDENT_RE.findall(seg):
            if short_txt not in _PLAIN_FUNCTION_WORDS and short_txt not in STANDARD_LATEX_COMMANDS:
                declared.add(short_txt)
        for multi in re.findall(r"\b([A-Za-z][A-Za-z0-9_]{1,4})\b", seg):
            if multi not in _PLAIN_FUNCTION_WORDS and multi not in STANDARD_LATEX_COMMANDS:
                declared.add(multi)

    return declared


def check_open_symbolic_answer_closure(
    instance: Dict[str, Any],
    interaction_type: str = "",
) -> List[str]:
    """Surgical hard gate [TPL-EPISTEMIC-CLOSURE] for open_symbolic expected_answer symbols."""
    if not isinstance(instance, dict):
        return []

    norm_type = str(interaction_type or instance.get("interaction_type") or "").strip().lower()
    if norm_type not in ("open_symbolic", "sym", "symbolic"):
        return []

    exp_ans = instance.get(
        "expected_answer",
        instance.get("correct_answer", instance.get("correct")),
    )
    if isinstance(exp_ans, dict):
        exp_ans = (
            exp_ans.get("expression")
            or exp_ans.get("canonical_algebraic")
            or exp_ans.get("value")
        )
    if not isinstance(exp_ans, str) or not exp_ans.strip():
        return []

    ans_syms = extract_open_symbolic_answer_symbols(exp_ans)
    if not ans_syms:
        return []

    stem_allowed: Set[str] = set()
    for ctx_txt in _iter_context_texts(instance, norm_type):
        stem_allowed.update(_extract_stem_declared_symbols_for_symbolic(ctx_txt))

    allowed = stem_allowed | STD_MATH_SYMBOLS | _SYMBOLIC_STD_CONSTS
    allowed_aliases = set(allowed)
    for item in allowed:
        if "_" in item:
            allowed_aliases.add(item.replace("_", ""))
        if item.startswith("\\"):
            allowed_aliases.add(item[1:])

    missing = sorted(
        sym for sym in ans_syms
        if sym not in allowed_aliases
        and not (sym.startswith("\\") and sym[1:] in allowed_aliases)
        and not _is_subscripted_known_symbol(sym, allowed_aliases)
    )
    if not missing:
        return []

    qid = instance.get("id") or instance.get("template_id") or "question"
    joined = ", ".join(missing)
    return [
        f"[TPL-EPISTEMIC-CLOSURE] '{qid}': expected_answer simbólica usa símbolo(s) ({joined}) "
        f"no declarados en stem ({exp_ans!r}). Declara explícitamente toda variable requerida en stem_variants."
    ]
