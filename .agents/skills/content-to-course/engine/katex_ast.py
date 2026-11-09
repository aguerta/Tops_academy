"""KaTeX Abstract Syntax Tree (AST), Algebraic Canonicalizer, and Pydantic Shard Contract.

Implements Milestone 4 contracts:
- M4.1: ShardCompetenceContract (Pydantic Form-C Authoring Contract)
- M4.3: KaTeXAST Inductive Grammar & Validator (Lean TopsAcademyC2C.lean §7.2 specification)
- M4.3: PyKaTeX Exact-Column Validation
- M4.4: KaTeX Algebraic Canonicalizer & SymPy LaTeX Integration
"""

from __future__ import annotations

import re
import threading
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, Field, model_validator

try:
    import pykatex
except ImportError:
    pykatex = None

try:
    import sympy
except ImportError:
    sympy = None

_KATEX_LOCK = threading.Lock()

__all__ = [
    "ArchetypeKind",
    "ShardCompetenceContract",
    "KaTeXNode",
    "AtomNode",
    "TextMacroNode",
    "AccentMacroNode",
    "UnaryMacroNode",
    "BinaryMacroNode",
    "MatrixEnvNode",
    "RowBreakNode",
    "DoubleBraceNode",
    "QuantifierEqNode",
    "GroupNode",
    "SeqNode",
    "KaTeXAST",
    "validate_katex_ast",
    "pykatex_validate_with_column",
    "canonicalize_algebraic_katex",
    "sympy_to_katex",
]


# =============================================================================
# 1. Pydantic ShardCompetenceContract (M4.1)
# =============================================================================

class ArchetypeKind(str, Enum):
    DIRECT = "direct"
    INVERSE = "inverse"
    PERTURBATION = "perturbation"
    BOUNDARY_OR_EDGE_CASE = "boundary_or_edge_case"


class ShardCompetenceContract(BaseModel):
    competence_id: str
    archetype: ArchetypeKind
    assumption_tested_id: Optional[str] = Field(
        default=None,
        description="Obligatorio en BOUNDARY_OR_EDGE_CASE",
    )
    python_pure_logic: str = Field(
        default="",
        description="Solo generate(rng) -> dict y ver(cand, v) -> bool. Cero strings LaTeX.",
    )
    statement_variants_markdown: List[str] = Field(
        default_factory=list,
        description=">= 4 stems con tokens @PARAM@",
    )
    hints_markdown: List[str] = Field(
        default_factory=list,
        description="3 a 5 pistas socráticas progresivas",
    )
    solution_markdown: str = Field(
        default="",
        description="Explicación paso a paso con tokens @PARAM@",
    )
    distractors_markdown: List[Tuple[str, str, str]] = Field(
        default_factory=list,
        description="6 3-tuplas (did, val, rationale_con_@PARAM@)",
    )
    # Form-C bridge fields:
    id: Optional[str] = None
    qtype: str = "MC7"
    band: Tuple[str, str] = ("easy", "Apply")
    fmt: Optional[str] = None
    gen: Optional[Any] = None
    ver: Optional[Any] = None
    rats: Optional[Dict[str, str]] = None

    @model_validator(mode="after")
    def validate_shard_contract(self) -> "ShardCompetenceContract":
        # 1. BOUNDARY_OR_EDGE_CASE requires assumption_tested_id
        if self.archetype == ArchetypeKind.BOUNDARY_OR_EDGE_CASE:
            if not self.assumption_tested_id or not self.assumption_tested_id.strip():
                raise ValueError("assumption_tested_id es obligatorio cuando archetype == 'boundary_or_edge_case'")

        # 2. python_pure_logic must not contain raw LaTeX commands
        if self.python_pure_logic:
            forbidden_latex = [r"\frac{", r"\begin{", r"\text{", r"\sqrt{", "$$"]
            for f_cmd in forbidden_latex:
                if f_cmd in self.python_pure_logic:
                    raise ValueError(
                        "python_pure_logic no debe contener strings LaTeX; use tokens @PARAM@ en las plantillas markdown"
                    )

        # 3. statement_variants_markdown check: if provided, must have >= 3 variants
        if self.statement_variants_markdown and len(self.statement_variants_markdown) < 3:
            raise ValueError(
                "statement_variants_markdown debe contener al menos 3 variantes (recomendado >= 4)"
            )

        # 4. hints_markdown check: if provided, must have 3 to 5 hints
        if self.hints_markdown and not (3 <= len(self.hints_markdown) <= 5):
            raise ValueError("hints_markdown debe contener entre 3 y 5 pistas")

        return self

    def to_form_c_dict(self) -> Dict[str, Any]:
        """Convert contract instance into a Form-C compatible dictionary for compile_shard.py."""
        gen_fn = self.gen
        ver_fn = self.ver

        if (not callable(gen_fn) or not callable(ver_fn)) and self.python_pure_logic.strip():
            isolated_ns: Dict[str, Any] = {
                "__builtins__": __builtins__,
            }
            exec(self.python_pure_logic, isolated_ns)

            if not callable(gen_fn):
                if "generate" in isolated_ns and callable(isolated_ns["generate"]):
                    gen_fn = isolated_ns["generate"]
                else:
                    for k, v in isolated_ns.items():
                        if callable(v) and (k.startswith("gen_") or k == "gen"):
                            gen_fn = v
                            break

            if not callable(ver_fn):
                if "verify" in isolated_ns and callable(isolated_ns["verify"]):
                    ver_fn = isolated_ns["verify"]
                elif "ver" in isolated_ns and callable(isolated_ns["ver"]):
                    ver_fn = isolated_ns["ver"]
                else:
                    for k, v in isolated_ns.items():
                        if callable(v) and (k.startswith("ver_")):
                            ver_fn = v
                            break

        if callable(gen_fn) and self.distractors_markdown:
            orig_gen = gen_fn
            distractor_defs = list(self.distractors_markdown)

            def wrapped_gen(*args: Any, **kwargs: Any) -> Any:
                res = orig_gen(*args, **kwargs)
                if isinstance(res, dict) and "distractors" not in res:
                    res["distractors"] = [(did, val, rat) for did, val, rat in distractor_defs]
                return res

            gen_fn = wrapped_gen

        rats_dict = dict(self.rats) if self.rats else {}
        if self.distractors_markdown:
            for did, _, rat in self.distractors_markdown:
                if did not in rats_dict:
                    rats_dict[did] = rat

        return {
            "id": self.id or f"Q-{self.competence_id}-001",
            "cid": self.competence_id,
            "qtype": self.qtype,
            "archetype": self.archetype.value if hasattr(self.archetype, "value") else str(self.archetype),
            "assumption_id": self.assumption_tested_id,
            "band": self.band,
            "gen": gen_fn,
            "ver": ver_fn,
            "stems": list(self.statement_variants_markdown),
            "hints": list(self.hints_markdown),
            "sol": self.solution_markdown,
            "fmt": self.fmt,
            "rats": rats_dict,
        }


# =============================================================================
# 2. KaTeXAST Inductive Grammar & Validation (M4.3 — Lean §7.2)
# =============================================================================

class KaTeXNode:
    """Base class for inductive KaTeX AST nodes."""
    pass


@dataclass
class AtomNode(KaTeXNode):
    text: str


@dataclass
class TextMacroNode(KaTeXNode):
    macro: str
    content: str


@dataclass
class AccentMacroNode(KaTeXNode):
    macro: str
    arg: KaTeXNode


@dataclass
class UnaryMacroNode(KaTeXNode):
    macro: str
    arg: KaTeXNode


@dataclass
class BinaryMacroNode(KaTeXNode):
    macro: str
    arg1: KaTeXNode
    arg2: KaTeXNode


@dataclass
class MatrixEnvNode(KaTeXNode):
    env_name: str
    body: KaTeXNode


@dataclass
class RowBreakNode(KaTeXNode):
    pass


@dataclass
class DoubleBraceNode(KaTeXNode):
    inner: str


@dataclass
class QuantifierEqNode(KaTeXNode):
    raw: str


@dataclass
class GroupNode(KaTeXNode):
    children: List[KaTeXNode]


@dataclass
class SeqNode(KaTeXNode):
    children: List[KaTeXNode]


def _flatten_ast_text(node: KaTeXNode) -> str:
    """Extract concatenated plain text from AST node tree."""
    if isinstance(node, AtomNode):
        return node.text
    if isinstance(node, TextMacroNode):
        return node.content
    if isinstance(node, (AccentMacroNode, UnaryMacroNode)):
        return _flatten_ast_text(node.arg)
    if isinstance(node, BinaryMacroNode):
        return _flatten_ast_text(node.arg1) + _flatten_ast_text(node.arg2)
    if isinstance(node, (GroupNode, SeqNode)):
        return "".join(_flatten_ast_text(c) for c in node.children)
    if isinstance(node, MatrixEnvNode):
        return _flatten_ast_text(node.body)
    if isinstance(node, DoubleBraceNode):
        return node.inner
    if isinstance(node, QuantifierEqNode):
        return node.raw
    return ""


class KaTeXParser:
    """Recursive descent parser generating KaTeX AST nodes from LaTeX math strings."""

    def __init__(self, s: str):
        self.s = s
        self.pos = 0
        self.n = len(s)

    def _skip_whitespace(self) -> None:
        while self.pos < self.n and self.s[self.pos].isspace():
            self.pos += 1

    def parse_all(self) -> KaTeXNode:
        nodes: List[KaTeXNode] = []
        while self.pos < self.n:
            node = self.parse_item()
            if node is not None:
                nodes.append(node)
        if len(nodes) == 1:
            return nodes[0]
        return SeqNode(children=nodes)

    def _extract_braced_raw(self) -> str:
        self._skip_whitespace()
        if self.pos < self.n and self.s[self.pos] == "{":
            self.pos += 1
            start = self.pos
            depth = 1
            while self.pos < self.n and depth > 0:
                ch = self.s[self.pos]
                if ch == "\\" and self.pos + 1 < self.n:
                    self.pos += 2
                    continue
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                self.pos += 1
            end = self.pos - 1 if depth == 0 else self.pos
            return self.s[start:end]
        return ""

    def _parse_argument(self) -> KaTeXNode:
        self._skip_whitespace()
        if self.pos >= self.n:
            return AtomNode(text="")
        if self.s[self.pos] == "{":
            self.pos += 1
            start = self.pos
            depth = 1
            while self.pos < self.n and depth > 0:
                ch = self.s[self.pos]
                if ch == "\\" and self.pos + 1 < self.n:
                    self.pos += 2
                    continue
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                self.pos += 1
            end = self.pos - 1 if depth == 0 else self.pos
            inner_str = self.s[start:end]
            inner_node = KaTeXAST.parse(inner_str)
            if isinstance(inner_node, SeqNode):
                return GroupNode(children=inner_node.children)
            if isinstance(inner_node, GroupNode):
                return inner_node
            return GroupNode(children=[inner_node] if inner_node else [])

        # Single non-braced token argument
        if self.s[self.pos] == "\\":
            m = re.match(r"\\([a-zA-Z]+|\S)", self.s[self.pos:])
            if m:
                self.pos += len(m.group(0))
                return AtomNode(text=m.group(0))
        ch = self.s[self.pos]
        self.pos += 1
        return AtomNode(text=ch)

    def parse_item(self) -> Optional[KaTeXNode]:
        if self.pos >= self.n:
            return None

        # 1. Double curly braces {{...}}
        if self.s.startswith("{{", self.pos):
            start = self.pos
            self.pos += 2
            inner_start = self.pos
            depth = 0
            while self.pos < self.n:
                if self.s.startswith("}}", self.pos) and depth == 0:
                    inner = self.s[inner_start : self.pos]
                    self.pos += 2
                    return DoubleBraceNode(inner=inner)
                if self.s[self.pos] == "{":
                    depth += 1
                    self.pos += 1
                elif self.s[self.pos] == "}":
                    if depth > 0:
                        depth -= 1
                    self.pos += 1
                else:
                    self.pos += 1
            return AtomNode(text=self.s[start:self.pos])

        # 2. Vacuous quantifier equality: \forall \varepsilon = 0.05
        m_quant = re.match(
            r"\\(forall|exists)\s*(\\[a-zA-Z]+|[a-zA-Z0-9_]+)\s*=\s*(-?\d+(?:\.\d+)?|[a-zA-Z0-9_]+)",
            self.s[self.pos:],
        )
        if m_quant:
            raw = m_quant.group(0)
            self.pos += len(raw)
            return QuantifierEqNode(raw=raw)

        # 3. Environments: \begin{env} ... \end{env}
        m_env = re.match(r"\\begin\s*\{([a-zA-Z*]+)\}", self.s[self.pos:])
        if m_env:
            env_name = m_env.group(1)
            self.pos += m_env.end()
            body_start = self.pos
            depth = 1
            end_pat = re.compile(rf"\\(begin|end)\s*\{{{re.escape(env_name)}\}}")
            body_end = self.pos
            while self.pos < self.n:
                m_sub = end_pat.search(self.s, self.pos)
                if not m_sub:
                    body_end = self.n
                    self.pos = self.n
                    break
                if m_sub.group(1) == "begin":
                    depth += 1
                    self.pos = m_sub.end()
                else:
                    depth -= 1
                    if depth == 0:
                        body_end = m_sub.start()
                        self.pos = m_sub.end()
                        break
                    self.pos = m_sub.end()
            body_str = self.s[body_start:body_end]
            body_node = KaTeXAST.parse(body_str)
            return MatrixEnvNode(env_name=env_name, body=body_node)

        # 4. Row break: \\ (when not immediately followed by an alphabet letter forming an overescape)
        if self.s.startswith(r"\\", self.pos):
            if not re.match(r"^\\\\[a-zA-Z]", self.s[self.pos:]):
                self.pos += 2
                return RowBreakNode()
            self.pos += 1
            return AtomNode(text="\\")

        # 5. Group: {...}
        if self.s[self.pos] == "{":
            self.pos += 1
            start = self.pos
            depth = 1
            while self.pos < self.n and depth > 0:
                ch = self.s[self.pos]
                if ch == "\\" and self.pos + 1 < self.n:
                    self.pos += 2
                    continue
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                self.pos += 1
            end = self.pos - 1 if depth == 0 else self.pos
            inner_str = self.s[start:end]
            inner_node = KaTeXAST.parse(inner_str)
            if isinstance(inner_node, SeqNode):
                return GroupNode(children=inner_node.children)
            if isinstance(inner_node, GroupNode):
                return inner_node
            return GroupNode(children=[inner_node] if inner_node else [])

        # 6. LaTeX Commands: \macro
        if self.s[self.pos] == "\\":
            m_cmd = re.match(r"\\([a-zA-Z]+|\S)", self.s[self.pos:])
            if m_cmd:
                cmd_full = m_cmd.group(0)
                cmd_name = m_cmd.group(1)
                self.pos += len(cmd_full)

                # Text macros
                if cmd_name in ("text", "textrm", "mathrm", "textbf", "textit", "textsf", "texttt", "textsc"):
                    content = self._extract_braced_raw()
                    return TextMacroNode(macro=cmd_name, content=content)

                # Binary macros
                if cmd_name in ("frac", "dfrac", "tfrac", "cfrac", "binom", "dbinom", "tbinom", "overset", "underset", "stackrel"):
                    arg1 = self._parse_argument()
                    arg2 = self._parse_argument()
                    return BinaryMacroNode(macro=cmd_name, arg1=arg1, arg2=arg2)

                # Accent macros
                if cmd_name in (
                    "dot", "ddot", "dddot", "ddddot", "hat", "bar", "tilde", "vec",
                    "acute", "grave", "check", "breve", "mathring", "widehat", "widetilde",
                    "widecheck", "overline", "underline"
                ):
                    arg = self._parse_argument()
                    return AccentMacroNode(macro=cmd_name, arg=arg)

                # Unary macros
                if cmd_name in (
                    "sqrt", "mathbf", "boldsymbol", "bm", "mathit", "mathcal", "mathbb",
                    "mathfrak", "mathsf", "mathtt", "mathscr", "symbf", "operatorname"
                ):
                    self._skip_whitespace()
                    if self.pos < self.n and self.s[self.pos] == "[":
                        opt_end = self.s.find("]", self.pos)
                        if opt_end != -1:
                            self.pos = opt_end + 1
                    arg = self._parse_argument()
                    return UnaryMacroNode(macro=cmd_name, arg=arg)

                return AtomNode(text=cmd_full)

        # 7. Atom literal sequence
        start = self.pos
        while (
            self.pos < self.n
            and self.s[self.pos] not in ("\\", "{", "}")
            and not self.s.startswith("{{", self.pos)
        ):
            self.pos += 1
        return AtomNode(text=self.s[start:self.pos])


class KaTeXAST:
    """Namespace providing AST parsing, structural validation, and inductive proof checking."""

    @staticmethod
    def parse(math_str: str) -> KaTeXNode:
        """Parse LaTeX math string into a KaTeXAST inductive tree."""
        if not math_str:
            return SeqNode(children=[])
        parser = KaTeXParser(math_str)
        return parser.parse_all()

    @staticmethod
    def is_valid(node: KaTeXNode, in_matrix: bool = False) -> Tuple[bool, List[str]]:
        """Validate an inductive KaTeX AST node according to Lean TopsAcademyC2C.lean §7.2."""
        errors: List[str] = []

        if isinstance(node, TextMacroNode):
            if len(node.content) > 45:
                snippet = node.content[:30] + "..." if len(node.content) > 30 else node.content
                errors.append(
                    f"[KATEX-AST-PROSE-OVERFLOW] KaTeX text macro '\\{node.macro}{{{snippet}}}' exceeds 45 characters "
                    f"({len(node.content)} chars). Split into markdown prose outside math delimiters."
                )
            non_math = re.sub(r"\$\$[\s\S]*?\$\$|\$[^\$]+?\$", "", node.content)
            if re.search(r"(?<!\\)_", non_math):
                errors.append(
                    f"[KATEX-AST-RAW-UNDERSCORE] Unescaped underscore '_' inside '\\{node.macro}{{{node.content}}}' "
                    f"causes KaTeX ParseError."
                )

        elif isinstance(node, RowBreakNode):
            if not in_matrix:
                errors.append(
                    "[KATEX-AST-ILLEGAL-ROWBREAK] Forbidden linebreak '\\\\' inside math expression outside matrix/cases environment."
                )

        elif isinstance(node, DoubleBraceNode):
            errors.append(
                f"[KATEX-AST-DOUBLE-BRACES] Residual double curly braces '{{{{{node.inner}}}}}' detected."
            )

        elif isinstance(node, AccentMacroNode):
            if node.macro in ("dot", "ddot"):
                plain = _flatten_ast_text(node.arg).strip()
                if plain.isdigit():
                    errors.append(
                        f"[KATEX-AST-NEWTONIAN-DIGIT] Newtonian fluxion dot accent '\\{node.macro}{{{plain}}}' applied to numeric literal."
                    )
            _, sub = KaTeXAST.is_valid(node.arg, in_matrix)
            errors.extend(sub)

        elif isinstance(node, QuantifierEqNode):
            errors.append(
                f"[KATEX-AST-VACUOUS-QUANTIFIER] Vacuous quantifier equality detected: '{node.raw}'."
            )

        elif isinstance(node, MatrixEnvNode):
            _, sub = KaTeXAST.is_valid(node.body, in_matrix=True)
            errors.extend(sub)

        elif isinstance(node, UnaryMacroNode):
            _, sub = KaTeXAST.is_valid(node.arg, in_matrix)
            errors.extend(sub)

        elif isinstance(node, BinaryMacroNode):
            _, sub1 = KaTeXAST.is_valid(node.arg1, in_matrix)
            _, sub2 = KaTeXAST.is_valid(node.arg2, in_matrix)
            errors.extend(sub1)
            errors.extend(sub2)

        elif isinstance(node, (GroupNode, SeqNode)):
            for child in node.children:
                _, sub = KaTeXAST.is_valid(child, in_matrix)
                errors.extend(sub)

        return len(errors) == 0, errors

    @staticmethod
    def isValid(node: KaTeXNode, in_matrix: bool = False) -> bool:
        """Boolean alias for is_valid."""
        ok, _ = KaTeXAST.is_valid(node, in_matrix)
        return ok


def validate_katex_ast(text: str, allow_template_vars: bool = False) -> List[str]:
    """Validate mathematical expressions in text or pure formulas against inductive KaTeXAST rules."""
    errors: List[str] = []
    if not isinstance(text, str) or not text.strip():
        return errors

    math_matches = list(re.finditer(r"\$\$(.*?)\$\$|\$([^\$]+?)\$", text, flags=re.DOTALL))
    if math_matches:
        for mb in math_matches:
            raw_match = mb.group(0)
            is_disp = raw_match.startswith("$$")
            block = mb.group(1) if is_disp else mb.group(2)
            if not block or not block.strip():
                continue
            probe = re.sub(r"@[a-zA-Z0-9_]+@", "x", block) if allow_template_vars else block
            node = KaTeXAST.parse(probe)
            _, sub_errs = KaTeXAST.is_valid(node)
            errors.extend(sub_errs)
    else:
        probe = re.sub(r"@[a-zA-Z0-9_]+@", "x", text) if allow_template_vars else text
        if any(c in probe for c in ("\\", "{", "}", "^", "_")) or probe.strip().startswith(("{{", "=")):
            node = KaTeXAST.parse(probe)
            _, sub_errs = KaTeXAST.is_valid(node)
            errors.extend(sub_errs)

    return errors


# =============================================================================
# 3. PyKaTeX Validation with Exact Column (M4.3)
# =============================================================================

def pykatex_validate_with_column(
    math_content: str,
    is_display: bool = False,
) -> Tuple[bool, Optional[str], Optional[int]]:
    """Thread-safe validation using pykatex, extracting exact column location on error."""
    if pykatex is None:
        return True, None, None

    strict_mode = getattr(pykatex, "STRICT_IGNORE", "ignore")
    with _KATEX_LOCK:
        try:
            pykatex.renderToString(math_content, is_display, strict=strict_mode)
            return True, None, None
        except Exception as e:
            clean_msg = str(e).replace("\u0332", "^")
            col_int: Optional[int] = None
            m_pos = re.search(r"\b(?:at\s+)?position\s+(\d+)\b", clean_msg, re.IGNORECASE)
            if m_pos:
                try:
                    col_int = int(m_pos.group(1))
                except ValueError:
                    col_int = None
            elif "at end of input" in clean_msg.lower():
                col_int = len(math_content)
            elif "^" in clean_msg:
                for line in clean_msg.splitlines():
                    if "^" in line:
                        col_int = line.find("^")
                        break
            return False, clean_msg, col_int


# =============================================================================
# 4. Algebraic Canonicalizer & SymPy LaTeX Generation (M4.4)
# =============================================================================

def _collapse_algebraic_signs_and_coeffs(math_body: str, collapse_unit_coeffs: bool = True) -> str:
    """Helper to canonicalize double signs and unitary coefficients in pure math string."""
    # 1. Collapses double signs: + -5 -> - 5, - -5 -> + 5, etc.
    for _ in range(5):
        orig_body = math_body
        math_body = re.sub(r"(?<![a-zA-Z\\])\+\s*-\s*(?=[0-9a-zA-Z\\({])", "- ", math_body)
        math_body = re.sub(r"(?<![a-zA-Z\\])-\s*-\s*(?=[0-9a-zA-Z\\({])", "+ ", math_body)
        math_body = re.sub(r"(?<![a-zA-Z\\])\+\s*\+\s*(?=[0-9a-zA-Z\\({])", "+ ", math_body)
        math_body = re.sub(r"(?<![a-zA-Z\\])-\s*\+\s*(?=[0-9a-zA-Z\\({])", "- ", math_body)
        if math_body == orig_body:
            break

    if not collapse_unit_coeffs:
        return math_body

    # 2. Collapses unitary coefficients: 1 x -> x, -1 x -> -x, 1*x -> x, 1 \cdot x -> x
    greek_letters = (
        r"alpha|beta|gamma|delta|epsilon|varepsilon|zeta|eta|theta|vartheta|"
        r"iota|kappa|varkappa|lambda|mu|nu|xi|pi|varpi|rho|varrho|sigma|varsigma|"
        r"tau|upsilon|phi|varphi|chi|psi|omega|Gamma|Delta|Theta|Lambda|Xi|Pi|Sigma|Upsilon|Phi|Psi|Omega"
    )
    var_macros = r"mathbf|boldsymbol|bm|mathit|mathrm|mathcal|symbf|hat|bar|dot|ddot|tilde|vec"
    target_var = (
        rf"(?:\\(?:{greek_letters})\b|"
        rf"\\(?:{var_macros})\s*\{{[^{{}}]+\}}|"
        rf"[a-zA-Z](?![a-zA-Z])(?:\^\{{[^{{}}]*\}}|\^[a-zA-Z0-9]|_\{{[^{{}}]*\}}|_[a-zA-Z0-9])*)"
    )

    sep = r"(?:\s*\\cdot\s*|\s*\*\s*|\s+)"

    # Negative unitary coefficient: -1 x, -1*x, -1 \cdot x -> -x
    math_body = re.sub(
        rf"(?<![_^])(?<![_^]{{)(^|[\s=+\-\(\[\{{])(?<![\d.])-\s*1{sep}(?={target_var})",
        r"\g<1>-",
        math_body,
    )
    # Positive unitary coefficient: 1 x, 1*x, 1 \cdot x -> x
    math_body = re.sub(
        rf"(?<![_^])(?<![_^]{{)(^|[\s=+\-\(\[\{{])(?<![\d.])1{sep}(?={target_var})",
        r"\g<1>",
        math_body,
    )
    return math_body


def canonicalize_algebraic_katex(
    text: str,
    whole_is_math: bool = False,
    collapse_unit_coeffs: bool = True,
) -> str:
    """Canonicalize algebraic KaTeX expressions, collapsing double signs and unitary coefficients."""
    if not isinstance(text, str) or not text:
        return text

    if whole_is_math or ("$" not in text and not re.search(r"[a-záéíóúñ]{4,}\s+[a-záéíóúñ]{4,}", text, re.IGNORECASE)):
        return _collapse_algebraic_signs_and_coeffs(text, collapse_unit_coeffs=collapse_unit_coeffs)

    def _replace_math_span(match: re.Match) -> str:
        raw_span = match.group(0)
        is_display = raw_span.startswith("$$")
        delim = "$$" if is_display else "$"
        inner = raw_span[len(delim) : -len(delim)]
        return f"{delim}{_collapse_algebraic_signs_and_coeffs(inner, collapse_unit_coeffs=collapse_unit_coeffs)}{delim}"

    return re.sub(r"\$\$[\s\S]*?\$\$|\$[^\$]+?\$", _replace_math_span, text)


def sympy_to_katex(expr: Any) -> str:
    """Generate canonical KaTeX string from a SymPy expression or mathematical object."""
    if sympy is not None and hasattr(expr, "__class__") and hasattr(sympy, "latex"):
        try:
            raw_latex = sympy.latex(expr)
            return canonicalize_algebraic_katex(raw_latex, whole_is_math=True)
        except Exception:
            pass
    raw_str = str(expr)
    return canonicalize_algebraic_katex(raw_str, whole_is_math=True)
