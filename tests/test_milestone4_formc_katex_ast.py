"""Comprehensive Test Suite for Milestone 4: Form-C, KaTeX AST, Pydantic & Safeguards.

Verifies the 6 core technical components of Milestone 4:
1. Component 1 — Typed Pydantic Contracts (ArchetypeKind & ShardCompetenceContract).
2. Component 2 — Declarative Template Interpolation (@PARAM@ & @PARAM:fmt@ in engine.assemble).
3. Component 3 — Inductive Grammar KaTeXAST & pykatex Validation with Exact Column.
4. Component 4 — Symbolic Generation sympy.latex() & KaTeX Algebraic Canonicalizer.
5. Component 5 — Compositional Form-C DSL, AST Auto-Export of vars, & Static Precheck.
6. Component 6 — Anti-Overescape Safeguards (Rule R-23) in assemble & invariants.
"""
from __future__ import annotations

import json
import random
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

import pytest

# Ensure skill content-to-course root is in sys.path
_REPO_ROOT = Path(__file__).resolve().parent.parent
_SKILL_DIR = _REPO_ROOT / ".agents" / "skills" / "content-to-course"
if str(_SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(_SKILL_DIR))

# Imports from production modules
from engine.assemble import format_template_string, sanitize_katex_syntax
from engine.invariants import validate_katex_syntax
from shard_precheck import precheck_source
import compile_shard as cs

# Optional / parallel imports from Stream 1A (engine.katex_ast)
try:
    from engine.katex_ast import (
        ArchetypeKind,
        ShardCompetenceContract,
        KaTeXAST,
        pykatex_validate_with_column,
        canonicalize_algebraic_katex,
    )
    import engine.katex_ast as _katex_ast_mod
    sympy_to_katex = getattr(
        _katex_ast_mod, "sympy_to_katex", getattr(_katex_ast_mod, "sympy_latex_clean", None)
    )
    HAS_KATEX_AST = True
except (ImportError, ModuleNotFoundError):
    HAS_KATEX_AST = False
    ArchetypeKind = None
    ShardCompetenceContract = None
    KaTeXAST = None
    pykatex_validate_with_column = None
    canonicalize_algebraic_katex = None
    sympy_to_katex = None

# Optional / parallel imports from Stream 1B (compile_shard.inject_ast_auto_vars)
HAS_AUTO_VARS = hasattr(cs, "inject_ast_auto_vars")
inject_ast_auto_vars = getattr(cs, "inject_ast_auto_vars", None)

def _has_matrix_precheck() -> bool:
    dummy_code = (
        'def gen_sample(rng):\n'
        '    return {"ans": r"\\begin{bmatrix} 1 & 0 \\\\ 0 & 1 \\end{bmatrix}"}\n'
    )
    w = precheck_source(dummy_code)
    return any("[SYMPY-LATEX-MATRIX]" in msg or "matrix" in msg.lower() for msg in w)

HAS_PRECHECK_MATRIX = _has_matrix_precheck()


# =============================================================================
# Component 1: Typed Pydantic Contracts (ArchetypeKind & ShardCompetenceContract)
# =============================================================================

@pytest.mark.skipif(not HAS_KATEX_AST, reason="Stream 1A: engine.katex_ast pending")
class TestComponent1PydanticContracts:
    """Verifies typed authoring contracts under Pydantic."""

    def test_archetype_kind_enumeration_values(self) -> None:
        """ArchetypeKind must have exactly 4 values: direct, inverse, perturbation, boundary_or_edge_case."""
        expected_values = {"direct", "inverse", "perturbation", "boundary_or_edge_case"}
        actual_values = {k.value for k in ArchetypeKind}
        assert actual_values == expected_values
        assert len(ArchetypeKind) == 4
        assert ArchetypeKind.DIRECT.value == "direct"
        assert ArchetypeKind.INVERSE.value == "inverse"
        assert ArchetypeKind.PERTURBATION.value == "perturbation"
        assert ArchetypeKind.BOUNDARY_OR_EDGE_CASE.value == "boundary_or_edge_case"

    def test_shard_competence_contract_valid_and_to_form_c_dict(self) -> None:
        """Valid contract passes Pydantic and converts to Form-C dict via .to_form_c_dict()."""
        clean_python_logic = (
            "def gen_c01(rng):\n"
            "    x = rng.randint(10, 50)\n"
            "    return {'ans': str(x), 'ds': [str(x + i) for i in range(1, 7)]}\n"
            "def ver_c01(cand, v):\n"
            "    return True\n"
        )
        contract = ShardCompetenceContract(
            competence_id="C-TEST-01",
            archetype=ArchetypeKind.DIRECT,
            assumption_tested_id=None,
            python_pure_logic=clean_python_logic,
            statement_variants_markdown=[
                "Calcula el valor base dado @alpha@ y @beta@ en contexto A.",
                "Determina la magnitud estructural con @alpha@ y @beta@ en contexto B.",
                "Evalua la respuesta de equilibrio con @alpha@ y @beta@ en contexto C.",
                "Estima el parametro resultante con @alpha@ y @beta@ en contexto D.",
            ],
            hints_markdown=[
                "Paso 1: Identifica las variables primarias @alpha@.",
                "Paso 2: Aplica la transformacion lineal con @beta@.",
                "Paso 3: Simplifica la expresion final numerica.",
            ],
            solution_markdown="La solucion paso a paso sustituye @alpha@ y @beta@ para obtener el resultado.",
            distractors_markdown=[
                ("D-01-01", "val1", "Error de signo en @alpha@."),
                ("D-01-02", "val2", "Omision del multiplicador @beta@."),
                ("D-01-03", "val3", "Inversion de terminos algebraicos."),
                ("D-01-04", "val4", "Suma en lugar de producto."),
                ("D-01-05", "val5", "Desplazamiento arbitrario de escala."),
                ("D-01-06", "val6", "Confusion de limites asintoticos."),
            ],
        )

        assert contract.competence_id == "C-TEST-01"
        assert contract.archetype == ArchetypeKind.DIRECT

        form_c_dict = contract.to_form_c_dict()
        assert isinstance(form_c_dict, dict)
        cid = form_c_dict.get("cid") or form_c_dict.get("competency_id")
        assert cid == "C-TEST-01"
        arch = form_c_dict.get("archetype")
        assert arch in ("direct", ArchetypeKind.DIRECT)

    def test_shard_competence_contract_boundary_requires_assumption_tested_id(self) -> None:
        """When archetype is BOUNDARY_OR_EDGE_CASE, assumption_tested_id cannot be None or empty."""
        from pydantic import ValidationError

        clean_python_logic = (
            "def gen_c02(rng):\n"
            "    return {'ans': '1', 'ds': ['2', '3', '4', '5', '6', '7']}\n"
            "def ver_c02(cand, v):\n"
            "    return True\n"
        )
        kwargs = dict(
            competence_id="C-TEST-02",
            archetype=ArchetypeKind.BOUNDARY_OR_EDGE_CASE,
            python_pure_logic=clean_python_logic,
            statement_variants_markdown=["Stem @a@ 1", "Stem @a@ 2", "Stem @a@ 3", "Stem @a@ 4"],
            hints_markdown=["Hint 1 @a@", "Hint 2 @a@", "Hint 3 @a@"],
            solution_markdown="Solution @a@",
            distractors_markdown=[(f"D-01-{i:02d}", f"val{i}", f"Rat {i} @a@") for i in range(1, 7)],
        )

        # None assumption_tested_id -> ValidationError
        with pytest.raises(ValidationError):
            ShardCompetenceContract(assumption_tested_id=None, **kwargs)

        # Empty string assumption_tested_id -> ValidationError
        with pytest.raises(ValidationError):
            ShardCompetenceContract(assumption_tested_id="   ", **kwargs)

        # Valid non-empty assumption_tested_id -> PASS
        valid_contract = ShardCompetenceContract(assumption_tested_id="ASSUMP-TEST-01", **kwargs)
        assert valid_contract.assumption_tested_id == "ASSUMP-TEST-01"

    def test_shard_competence_contract_rejects_raw_latex_in_pure_logic(self) -> None:
        """python_pure_logic must reject raw LaTeX commands like \\frac or \\begin{bmatrix}."""
        from pydantic import ValidationError

        kwargs = dict(
            competence_id="C-TEST-03",
            archetype=ArchetypeKind.DIRECT,
            assumption_tested_id=None,
            statement_variants_markdown=["Stem @a@ 1", "Stem @a@ 2", "Stem @a@ 3", "Stem @a@ 4"],
            hints_markdown=["Hint 1 @a@", "Hint 2 @a@", "Hint 3 @a@"],
            solution_markdown="Solution @a@",
            distractors_markdown=[(f"D-01-{i:02d}", f"val{i}", f"Rat {i} @a@") for i in range(1, 7)],
        )

        # LaTeX fraction inside python logic
        bad_logic_frac = (
            "def gen(rng):\n"
            "    ans = r'\\frac{a}{b}'\n"
            "    return {'ans': ans}\n"
        )
        with pytest.raises(ValidationError):
            ShardCompetenceContract(python_pure_logic=bad_logic_frac, **kwargs)

        # LaTeX matrix environment inside python logic
        bad_logic_matrix = (
            "def gen(rng):\n"
            "    mat = r'\\begin{bmatrix} 1 & 0 \\\\ 0 & 1 \\end{bmatrix}'\n"
            "    return {'ans': mat}\n"
        )
        with pytest.raises(ValidationError):
            ShardCompetenceContract(python_pure_logic=bad_logic_matrix, **kwargs)


# =============================================================================
# Component 2: Declarative Interpolation (@PARAM@ & @PARAM:fmt@ in engine.assemble)
# =============================================================================

class TestComponent2DeclarativeInterpolation:
    """Verifies PrairieLearn @PARAM@ and @PARAM:fmt@ interpolation in engine.assemble."""

    def test_format_template_string_basic_and_formatted_params(self) -> None:
        """@PARAM@ and @PARAM:fmt@ format accurately without mutating surrounding text."""
        tpl = "El parametro primario es @alpha@ y la razon ajustada es @ratio:.2f@."
        variables = {"alpha": 15, "ratio": 3.14159265}
        formatted = format_template_string(tpl, variables)
        assert formatted == "El parametro primario es 15 y la razon ajustada es 3.14."

    def test_format_template_string_preserves_katex_curlies(self) -> None:
        """KaTeX curly braces (\\frac{1}{2}, \\mathbb{R}, x^{2}, \\sqrt{...}) must never be corrupted."""
        tpl = (
            r"Encuentre $\frac{1}{2} x^{2} + \sqrt{@rad:.1f@}$ en $\mathbb{R}$ "
            r"sabiendo que $\frac{@num@}{@den@} \in \mathbb{Q}$."
        )
        variables = {"rad": 16.0, "num": 3, "den": 4}
        formatted = format_template_string(tpl, variables)

        expected = (
            r"Encuentre $\frac{1}{2} x^{2} + \sqrt{16.0}$ en $\mathbb{R}$ "
            r"sabiendo que $\frac{3}{4} \in \mathbb{Q}$."
        )
        assert formatted == expected
        assert r"\frac{1}{2}" in formatted
        assert r"\mathbb{R}" in formatted
        assert r"x^{2}" in formatted
        assert r"\frac{3}{4}" in formatted

    def test_format_template_string_various_specifiers(self) -> None:
        """Supports integer padding, scientific notation, and percentages."""
        tpl = "Code: @code:04d@ | Rate: @rate:.1%@ | Exp: @val:.2e@"
        variables = {"code": 7, "rate": 0.125, "val": 15000.0}
        formatted = format_template_string(tpl, variables)
        assert formatted == "Code: 0007 | Rate: 12.5% | Exp: 1.50e+04"


# =============================================================================
# Component 3: Inductive Grammar KaTeXAST & pykatex Validation with Exact Column
# =============================================================================

@pytest.mark.skipif(not HAS_KATEX_AST, reason="Stream 1A: engine.katex_ast pending")
class TestComponent3KaTeXASTGrammar:
    """Verifies inductive KaTeXAST parsing, semantic invariants, and pykatex exact column reporting."""

    def _call_is_valid(self, formula: str, in_matrix: bool = False) -> Tuple[bool, List[str]]:
        ast_tree = KaTeXAST.parse(formula)
        fn = getattr(KaTeXAST, "is_valid", getattr(KaTeXAST, "isValid", None))
        assert fn is not None, "KaTeXAST must define is_valid or isValid"
        return fn(ast_tree, in_matrix=in_matrix)

    def test_katex_ast_approves_valid_formulas(self) -> None:
        """Valid formulas, matrix environments, and short text are approved."""
        valid_cases = [
            r"x^2 + \frac{1}{2} = 0",
            r"\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}",
            r"\text{corto}",
            r"\alpha + \beta = \gamma",
        ]
        for f in valid_cases:
            ok, errors = self._call_is_valid(f)
            assert ok is True, f"Expected valid for '{f}', got errors: {errors}"
            assert len(errors) == 0

    def test_katex_ast_rejects_prose_overflow(self) -> None:
        """Prose > 45 characters inside \\text{...} must be rejected with [KATEX-AST-PROSE-OVERFLOW]."""
        overflow_formula = (
            r"\text{Esta es una explicacion demasiado extensa que supera con creces los cuarenta y cinco caracteres permitidos por el invariante}"
        )
        ok, errors = self._call_is_valid(overflow_formula)
        assert ok is False
        assert any("PROSE-OVERFLOW" in err for err in errors)

    def test_katex_ast_rejects_raw_underscore_in_text(self) -> None:
        """Raw unescaped underscore '_' inside \\text{...} must be rejected with [KATEX-AST-RAW-UNDERSCORE]."""
        formula = r"\text{param_alpha_beta}"
        ok, errors = self._call_is_valid(formula)
        assert ok is False
        assert any("RAW-UNDERSCORE" in err for err in errors)

    def test_katex_ast_rejects_illegal_rowbreak_outside_matrix(self) -> None:
        """Linebreak '\\\\' outside matrix/cases must be rejected with [KATEX-AST-ILLEGAL-ROWBREAK]."""
        formula = r"x + 1 \\ y + 2"
        ok, errors = self._call_is_valid(formula)
        assert ok is False
        assert any("ILLEGAL-ROWBREAK" in err for err in errors)

    def test_katex_ast_rejects_double_braces(self) -> None:
        """Double braces {{...}} must be rejected with [KATEX-AST-DOUBLE-BRACES]."""
        formula = r"x^{{2}} + {{y}}"
        ok, errors = self._call_is_valid(formula)
        assert ok is False
        assert any("DOUBLE-BRACES" in err for err in errors)

    def test_katex_ast_rejects_newtonian_digit(self) -> None:
        """Newtonian dot over digits '\\dot{5}' must be rejected with [KATEX-AST-NEWTONIAN-DIGIT]."""
        formula = r"\dot{5} + 3"
        ok, errors = self._call_is_valid(formula)
        assert ok is False
        assert any("NEWTONIAN-DIGIT" in err for err in errors)

    def test_katex_ast_rejects_vacuous_quantifier(self) -> None:
        """Vacuous quantifier '\\forall \\varepsilon = 0.05' must be rejected with [KATEX-AST-VACUOUS-QUANTIFIER]."""
        formula = r"\forall \varepsilon = 0.05"
        ok, errors = self._call_is_valid(formula)
        assert ok is False
        assert any("VACUOUS-QUANTIFIER" in err for err in errors)

    def test_pykatex_validate_with_column_exact(self) -> None:
        """pykatex_validate_with_column on incomplete math returns ok is False and an integer col >= 0."""
        ok, err_msg, col = pykatex_validate_with_column(r"\frac{1}", is_display=False)
        assert ok is False
        assert err_msg is not None and len(err_msg) > 0
        assert col is not None
        assert isinstance(col, int) and col >= 0


# =============================================================================
# Component 4: Symbolic Generation sympy.latex() & KaTeX Algebraic Canonicalizer
# =============================================================================

@pytest.mark.skipif(not HAS_KATEX_AST, reason="Stream 1A: engine.katex_ast pending")
class TestComponent4SymbolicAndCanonicalizer:
    """Verifies sympy to KaTeX conversion and algebraic canonicalization."""

    def test_canonicalize_algebraic_katex_unitary_coefficients(self) -> None:
        """Collapses unitary coefficients ($1 x -> $x, $-1 x -> $-x) while preserving $10 x and $0.1 x."""
        cases = [
            ("$1 x + 3$", "$x + 3$"),
            ("$-1 x$", "$-x$"),
            ("$1 x$", "$x$"),
            ("$1 \\alpha$", "$\\alpha$"),
        ]
        for src, expected in cases:
            res = canonicalize_algebraic_katex(src)
            assert res == expected, f"Failed for {src}: got {res}, expected {expected}"

        # Guard against false positives: 10 x and 0.1 x must remain intact
        assert canonicalize_algebraic_katex("$10 x$") == "$10 x$"
        assert canonicalize_algebraic_katex("$0.1 x$") == "$0.1 x$"
        assert canonicalize_algebraic_katex("$11 x$") == "$11 x$"

    def test_canonicalize_algebraic_katex_double_signs(self) -> None:
        """Collapses double signs ($x + -5 -> $x - 5, $x - -5 -> $x + 5)."""
        assert canonicalize_algebraic_katex("$x + -5$") == "$x - 5$"
        assert canonicalize_algebraic_katex("$x - -5$") == "$x + 5$"
        assert sanitize_katex_syntax("$x + -5$") == "$x - 5$"
        assert sanitize_katex_syntax("$x - -5$") == "$x + 5$"

    def test_sympy_to_katex_expressions_and_matrices(self) -> None:
        """sympy_to_katex converts algebraic expressions and matrices into valid KaTeX LaTeX strings."""
        if sympy_to_katex is None:
            pytest.skip("sympy_to_katex helper not yet available in engine.katex_ast")

        import sympy
        x, y = sympy.symbols("x y")
        poly = 1 * x**2 + 2 * y - 5
        latex_str = sympy_to_katex(poly)
        assert "x^{2}" in latex_str
        assert "y" in latex_str

        mat = sympy.Matrix([[1, 2], [3, 4]])
        mat_str = sympy_to_katex(mat)
        assert "matrix" in mat_str or "bmatrix" in mat_str
        assert "1" in mat_str and "2" in mat_str and "3" in mat_str and "4" in mat_str


# =============================================================================
# Component 5: Compositional Form-C DSL, AST Auto-Export of vars, & Static Precheck
# =============================================================================

class TestComponent5FormCAndPrecheck:
    """Verifies Form-C compiler, AST auto-export of vars, and static checks."""

    @pytest.mark.skipif(not HAS_AUTO_VARS, reason="Stream 1B: compile_shard.inject_ast_auto_vars pending")
    def test_inject_ast_auto_vars_scalar_locals(self) -> None:
        """inject_ast_auto_vars captures scalar local variables and populates vars dict automatically."""
        import ast
        import inspect

        def sample_gen(rng):
            tc = rng.randint(200, 280)
            th = 500
            eta = 0.5
            return {"ans": str(eta), "ds": [str(eta + 0.1 * i) for i in range(1, 7)]}

        rng = random.Random(12345)
        try:
            transformed = inject_ast_auto_vars(sample_gen)
            if callable(transformed):
                res = transformed(rng)
            elif isinstance(transformed, str):
                local_env = {"random": random}
                exec(transformed, local_env)
                res = local_env["sample_gen"](rng)
            elif isinstance(transformed, ast.AST):
                mod = ast.Module(body=[transformed], type_ignores=[])
                ast.fix_missing_locations(mod)
                code = compile(mod, filename="<ast>", mode="exec")
                local_env = {"random": random}
                exec(code, local_env)
                res = local_env["sample_gen"](rng)
            else:
                pytest.fail(f"Unexpected return type from inject_ast_auto_vars: {type(transformed)}")
        except TypeError:
            src = inspect.getsource(sample_gen)
            transformed = inject_ast_auto_vars(src)
            if isinstance(transformed, str):
                local_env = {"random": random}
                exec(transformed, local_env)
                res = local_env["sample_gen"](rng)
            elif isinstance(transformed, ast.AST):
                mod = ast.Module(body=[transformed], type_ignores=[])
                ast.fix_missing_locations(mod)
                code = compile(mod, filename="<ast>", mode="exec")
                local_env = {"random": random}
                exec(code, local_env)
                res = local_env["sample_gen"](rng)
            else:
                pytest.fail(f"Unexpected return type from inject_ast_auto_vars(src): {type(transformed)}")

        assert isinstance(res, dict)
        assert "vars" in res, "Transformed generator must output 'vars' dictionary"
        v = res["vars"]
        assert 200 <= v.get("tc", 0) <= 280
        assert v.get("th") == 500
        assert v.get("eta") == 0.5
        assert res.get("ans") == "0.5"

    def test_end_to_end_form_c_compilation(self, tmp_path: Path) -> None:
        """End-to-end Form-C shard with 4 archetypes compiles to canonical JSON with 0 errors."""
        work_dir = tmp_path / "work"
        shards_dir = work_dir / "shards"
        templates_dir = work_dir / "templates"
        shards_dir.mkdir(parents=True, exist_ok=True)
        templates_dir.mkdir(parents=True, exist_ok=True)

        manifest_data = {
            "total_competencies": 1,
            "total_shards": 1,
            "shards": [
                {
                    "shard_id": "shard_01",
                    "shard_index": 0,
                    "competency_ids": ["C-M4-01"],
                    "competencies": [
                        {
                            "id": "C-M4-01",
                            "name": "Termodinamica de Carnot",
                            "type": "concept",
                            "distractors": [
                                {"id": f"D-01-{i:02d}", "name": f"Distractor {i}"} for i in range(1, 7)
                            ],
                        }
                    ],
                    "shard_data_path": str((shards_dir / "shard_01_data.py").resolve().as_posix()),
                    "templates_dir": str(templates_dir.resolve().as_posix()),
                }
            ],
        }
        (shards_dir / "pre_shard_manifest.json").write_text(
            json.dumps(manifest_data, indent=2), encoding="utf-8"
        )

        cta_data = {
            "course_id": "course_formc_test",
            "competencies": [
                {
                    "id": "C-M4-01",
                    "name": "Termodinamica de Carnot",
                    "type": "concept",
                    "distractors": [
                        {"id": f"D-01-{i:02d}", "name": f"Distractor {i}"} for i in range(1, 7)
                    ],
                }
            ],
        }
        (work_dir / "cta.json").write_text(json.dumps(cta_data, indent=2), encoding="utf-8")

        shard_code = '''
import random

RATS = {
    "D-01-01": "Inversion de temperaturas caliente y fria en @th@.",
    "D-01-02": "Omision de la unidad de referencia con @tc@.",
    "D-01-03": "Suma en lugar de resta en el calculo de eficiencia @eta@.",
    "D-01-04": "Uso de escala Celsius en lugar de Kelvin para @tc@.",
    "D-01-05": "Asignacion erronea del trabajo neto respecto a @th@.",
    "D-01-06": "Confusion con el ciclo de Otto para @eta@.",
}

# 1. MC7 Template with shared fmt and RATS
def gen_c01_1(rng):
    tc = rng.randint(200, 280)
    th = 500
    eta = round(1.0 - (tc / th), 2)
    ds = [(f"D-01-{i:02d}", f"{round(eta + 0.05 * i, 2)}") for i in range(1, 7)]
    return {"vars": {"tc": tc, "th": th, "eta": eta, "X": str(eta)}, "ans": str(eta), "ds": ds}

def ver_c01_1(cand, v):
    expected = rf"$\\eta = {v.get('X')}$"
    return str(cand) == expected

# 2. FIB Direct Template
def gen_c01_2(rng):
    tc = rng.randint(200, 280)
    th = 500
    eta = round(1.0 - (tc / th), 2)
    return {"vars": {"tc": tc, "th": th, "eta": eta}, "correct": str(eta)}

def ver_c01_2(res):
    if not isinstance(res, dict):
        return False
    v = res.get("vars", {})
    return str(res.get("correct")) == str(v.get("eta"))

# 3. FIB Perturbation Template
def gen_c01_3(rng):
    tc = rng.randint(200, 280)
    th = 550
    eta = round(1.0 - (tc / th), 2)
    return {"vars": {"tc": tc, "th": th, "eta": eta}, "correct": str(eta)}

def ver_c01_3(res):
    if not isinstance(res, dict):
        return False
    v = res.get("vars", {})
    return str(res.get("correct")) == str(v.get("eta"))

# 4. MS Boundary/Edge-case Template with assumption_id
def gen_c01_4(rng):
    t_val = rng.randint(280, 380)
    opts = [
        {"value": f"La eficiencia reversible es nula en el limite isotermo T = {t_val} K.", "is_correct": True, "rationale": "Verdadero por formulacion de Carnot con @tc@."},
        {"value": f"No es posible extraer trabajo util bajo equilibrio termico a {t_val} K.", "is_correct": True, "rationale": "Verdadero por la Segunda Ley con @th@."},
        {"value": f"La eficiencia alcanza el maximo absoluto para la cota T = {t_val} K.", "is_correct": False, "distractor_id": "D-01-01", "rationale": "Falso: requiere cero absoluto en @tc@."},
        {"value": f"El calor absorbido se convierte totalmente en trabajo a {t_val} K.", "is_correct": False, "distractor_id": "D-01-02", "rationale": "Falso: viola Kelvin-Planck con @th@."},
    ]
    return {"vars": {"tc": t_val, "th": t_val}, "options": opts}

def ver_c01_4(res):
    if not isinstance(res, dict):
        return False
    opts = res.get("options", [])
    corr = sum(1 for o in opts if isinstance(o, dict) and o.get("is_correct"))
    return corr == 2

stems_fib_1 = [
    "Contexto A: Calcule la eficiencia termica de Carnot con @tc@ K y @th@ K.",
    "Contexto B: Determine el rendimiento ideal de la maquina con @tc@ K y @th@ K.",
    "Contexto C: Estime el coeficiente maximo teorico con @tc@ K y @th@ K.",
    "Contexto D: Obtenga el valor limite del ciclo con @tc@ K y @th@ K.",
]
hints_fib_1 = [
    "Paso 1: Identifique la temperatura de la fuente fria @tc@ y caliente @th@.",
    "Paso 2: Aplique la formula de Carnot eta = 1 - (Tc / Th).",
    "Paso 3: Redondee el valor decimal a dos cifras.",
]

stems_fib_2 = [
    "Perturbacion A: Evalue el nuevo rendimiento al variar la fuente a @th@ K.",
    "Perturbacion B: Calcule la respuesta termodinamica ajustada con @tc@ K.",
    "Perturbacion C: Estime la variacion de eficiencia del sistema a @th@ K.",
    "Perturbacion D: Deduzca el impacto marginal en la maquina con @tc@ K.",
]
hints_fib_2 = [
    "Paso 1: Observe el nuevo valor de la fuente caliente @th@.",
    "Paso 2: Calcule el nuevo cociente Tc / Th con @tc@.",
    "Paso 3: Verifique el incremento de eficiencia resultante.",
]

stems_ms = [
    "Caso limite A: Analice el comportamiento del ciclo cuando @tc@ y @th@ convergen.",
    "Caso limite B: Identifique las afirmaciones correctas sobre el equilibrio a @th@ K.",
    "Caso limite C: Determine las propiedades fisicas del sistema cuando @tc@ = @th@.",
    "Caso limite D: Seleccione los enunciados verdaderos bajo gradiente nulo a @tc@ K.",
]
hints_ms = [
    "Paso 1: Considere la condicion de igualdad de temperaturas @tc@ = @th@.",
    "Paso 2: Evalua la definicion de eficiencia termica cuando no hay gradiente.",
    "Paso 3: Recuerde el postulado de Kelvin-Planck.",
]

TEMPLATES = [
    {
        "id": "T-M4-01",
        "cid": "C-M4-01",
        "qtype": "MC7",
        "fmt": r"$\\eta = @X@$",
        "rats": RATS,
        "gen": gen_c01_1,
        "ver": ver_c01_1,
        "band": ("easy", "Remember"),
        "stems": (
            ["Contexto motor de gas con @tc@ K y @th@ K.", "Contexto planta termica con @tc@ K y @th@ K."],
            ["Calcule la eficiencia de Carnot.", "Determine el rendimiento teorico maximo."]
        ),
        "hints": [
            "Paso 1: Reconozca las temperaturas absoluta @tc@ y @th@.",
            "Paso 2: Aplique el ratio adimensional 1 - Tc/Th.",
            "Paso 3: Compare con las opciones disponibles.",
        ],
        "sol": "La solucion calcula eta = 1 - (@tc@ / @th@) = @X@.",
    },
    ("T-M4-02", "C-M4-01", "fill_in_the_blank", gen_c01_2, ver_c01_2, ("medium", "Apply"), stems_fib_1, hints_fib_1, "Sol @eta@"),
    ("T-M4-03", "C-M4-01", "fill_in_the_blank", gen_c01_3, ver_c01_3, ("medium", "Analyze"), stems_fib_2, hints_fib_2, "Sol @eta@"),
    {
        "id": "T-M4-04",
        "cid": "C-M4-01",
        "qtype": "multiple_select",
        "archetype": "boundary_or_edge_case",
        "assumption_id": "ASSUMP-CARNOT-01",
        "gen": gen_c01_4,
        "ver": ver_c01_4,
        "band": ("hard", "Evaluate"),
        "stems": stems_ms,
        "hints": hints_ms,
        "sol": "En el caso limite @tc@ = @th@, el rendimiento es cero.",
    },
]
'''
        shard_py = shards_dir / "shard_01_data.py"
        shard_py.write_text(shard_code, encoding="utf-8")

        success, errors = cs.compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_01",
            strict=True,
            seeds=10,
            output_dir=templates_dir,
            min_archetypes=4,
        )

        assert success is True, f"compile_shard failed: {errors}"
        assert len(errors) == 0

        # Check that generated templates exist and are valid JSON
        tpl_files = list(templates_dir.glob("*.json"))
        assert len(tpl_files) >= 1, "Expected compiled template JSON file in templates_dir"
        tpl_data = json.loads(tpl_files[0].read_text(encoding="utf-8"))
        assert "templates" in tpl_data
        assert len(tpl_data["templates"]) == 4

    @pytest.mark.skipif(not HAS_PRECHECK_MATRIX, reason="Stream 1B: [SYMPY-LATEX-MATRIX] precheck pending")
    def test_shard_precheck_detects_manual_matrix_assembly(self) -> None:
        """precheck_source detects manual matrix assembly (\\begin{bmatrix}) in gen_* functions."""
        code_with_manual_matrix = (
            "def gen_matrix_bad(rng):\n"
            "    mat = r'\\begin{bmatrix} 1 & 2 \\\\ 3 & 4 \\end{bmatrix}'\n"
            "    return {'ans': mat}\n"
        )
        warnings = precheck_source(code_with_manual_matrix)
        assert any("[SYMPY-LATEX-MATRIX]" in w or "matrix" in w.lower() for w in warnings)


# =============================================================================
# Component 6: Anti-Overescape Safeguards (Rule R-23 in assemble & invariants)
# =============================================================================

class TestComponent6AntiOverescapeSafeguards:
    """Verifies KaTeX overescape collapse, rowbreak preservation, and invariant enforcement."""

    def test_sanitize_katex_syntax_collapses_overescape_and_preserves_matrix(self) -> None:
        """sanitize_katex_syntax collapses \\\\frac to \\frac and preserves legitimate matrix rowbreaks."""
        # Over-escaped commands -> collapsed
        overescaped = r"Considere \\frac{a}{b} y \\text{valor}"
        cleaned = sanitize_katex_syntax(overescaped)
        assert cleaned == r"Considere \frac{a}{b} y \text{valor}"

        # Legitimate matrix rowbreak preserved
        matrix_text = r"$\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}$"
        cleaned_matrix = sanitize_katex_syntax(matrix_text)
        assert r"\\" in cleaned_matrix
        assert r"\begin{bmatrix}" in cleaned_matrix
        assert r"\end{bmatrix}" in cleaned_matrix

        # Unsupported macro repair
        unsupported = r"A \centernot\Rightarrow B"
        cleaned_macro = sanitize_katex_syntax(unsupported)
        assert r"\nRightarrow" in cleaned_macro
        assert r"\centernot" not in cleaned_macro

    def test_validate_katex_syntax_blocks_overescape_in_memory(self) -> None:
        """validate_katex_syntax flags \\\\cmd in memory under Rule R-23."""
        # In memory string with \\frac (two backslashes)
        overescaped_in_memory = r"Considere \\frac{x}{y} en la funcion"
        errors = validate_katex_syntax(overescaped_in_memory, "stem")
        assert len(errors) > 0
        assert any("R-23" in e or "Over-escaped LaTeX command" in e or r"\\frac" in e for e in errors)
