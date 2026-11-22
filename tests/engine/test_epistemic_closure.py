"""Tests for M17 static Epistemic Closure Auditor (S_sol <= S_stem U S_std)."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOT = REPO_ROOT / ".agents" / "skills" / "content-to-course"
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

from engine.epistemic_closure import (
    check_epistemic_closure,
    check_open_symbolic_answer_closure,
    extract_symbols_from_text,
)


def test_catches_undefined_symbols_in_solution_and_open_symbolic():
    """Undefined parameters/functions in solution or symbolic expected_answer trigger [EPISTEMIC-CLOSURE-WARNING]."""
    inst_missing_alpha = {
        "id": "Q-01",
        "stem": "Maximiza $U(x, y) = x y$ sujeto a $p_x x + p_y y = m$.",
        "detailed_solution": (
            "Aplicando Lagrange con multiplicador $\\lambda$, se obtiene "
            "$\\frac{\\alpha x}{y} = \\frac{p_x}{p_y}$ y el parámetro $k = 2$."
        ),
    }
    warnings = check_epistemic_closure(inst_missing_alpha, "multiple_choice_7_options")
    assert len(warnings) == 1
    assert "[EPISTEMIC-CLOSURE-WARNING]" in warnings[0]
    assert r"\alpha" in warnings[0]
    assert "k" in warnings[0]
    assert r"\lambda" not in warnings[0]

    inst_symbolic = {
        "id": "Q-02",
        "stem": "Deriva $f(x) = 3 x^2$ respecto a $x$.",
        "detailed_solution": "La derivada respecto a $x$ es $6 x$.",
        "expected_answer": "m * x^2",
    }
    warnings_sym = check_epistemic_closure(inst_symbolic, "open_symbolic")
    assert len(warnings_sym) == 1
    assert "m" in warnings_sym[0]


def test_allows_bound_variables_differentials_and_standard_notation():
    """Standard operators, differentials, sums, accents, and Lagrangian auxiliaries produce zero warnings."""
    inst_valid = {
        "id": "Q-03",
        "stem": (
            "Dada la muestra $x_1, \\dots, x_n$ con media $\\mu$, varianza $\\sigma^2$ y parámetro $\\beta$, "
            "calcula el estimador y evalúa $\\int_0^b k x^2 dx$."
        ),
        "detailed_solution": (
            "Usamos el sumatorio $\\sum_{i=1}^{n} (x_i - \\bar{x})^2$, la estadística estándar "
            "$Z = \\frac{\\bar{x} - \\mu}{\\sigma / \\sqrt{n}} \\in \\mathbb{R}$, el operador "
            "$\\operatorname{Var}(\\hat{\\beta})$ con $\\text{unidades monetarias}$, multiplicadores "
            "$\\lambda, \\mu$ y constantes $e, \\pi, C$, dando $\\frac{k b^3}{3}$."
        ),
    }
    warnings = check_epistemic_closure(inst_valid, "fill_in_the_blank")
    assert warnings == []


def test_numeric_open_symbolic_and_empty_context_safe():
    """Numeric open_symbolic expected_answer and missing fields do not raise false warnings."""
    inst_num = {
        "id": "Q-04",
        "stem": "Evalúa $f(x) = 2x$ en $x = 3$.",
        "detailed_solution": "Sustituyendo $x = 3$ obtenemos $f(3) = 6$.",
        "expected_answer": "6",
    }
    assert check_epistemic_closure(inst_num, "open_symbolic") == []
    assert extract_symbols_from_text("", treat_raw_as_math=True) == set()


def test_katex_parser_terminates_on_unmatched_brace_and_trailing_backslash():
    """Regression: malformed '}' or trailing '\\' must never spin KaTeXParser indefinitely."""
    from engine.katex_ast import KaTeXAST

    assert KaTeXAST.parse("x + 1}") is not None
    assert KaTeXAST.parse("x\\") is not None
    assert KaTeXAST.parse("\\sqrt{x}} + y") is not None
    assert extract_symbols_from_text("$x + 1}$ y $y\\$") >= {"x", "y"}


def test_surgical_hard_gate_open_symbolic_expected_answer():
    """Hard gate blocks undefined open_symbolic answer variables while passing valid notations."""
    # Must block genuine undefined symbols in expected_answer
    broken = {
        "id": "Q-SYM-BAD",
        "stem": "Deriva $f(x) = 3 x^2$ respecto a $x$.",
        "expected_answer": "m * x^2",
    }
    errs = check_open_symbolic_answer_closure(broken, "open_symbolic")
    assert len(errs) == 1
    assert "[TPL-EPISTEMIC-CLOSURE]" in errs[0]
    assert "(m)" in errs[0]

    # Must ignore non-open_symbolic items cleanly
    assert check_open_symbolic_answer_closure(broken, "fill_in_the_blank") == []
    assert check_open_symbolic_answer_closure(broken, "multiple_choice_7_options") == []

    # Real patterns: backticked vars (`y`, `vx`, `ve`, `sx`, `se`), c_1->c1 alias, and \text{se}
    valid_cases = [
        {
            "id": "Q-Hab15-784",
            "stem": r"A partir de la CPO $e^{-4t} + 2\lambda C = 0$, formule $C$ en función de `y` $= \lambda e^{4t}$:",
            "expected_answer": {"expression": "(8-2*y)**(-1/2)"},
        },
        {
            "id": "Q-Hab16-820",
            "stem": r"En $\min \int_0^1 4 u^2\,dt$ con $\dot{x}=6x+u$ y $\lambda(t)=c_1 e^{-6t}$, formule el control óptimo:",
            "expected_answer": "-(c1/8)*exp(-6*t)",
        },
        {
            "id": "Q-Hab18-1075",
            "stem": r"Escriba $\text{plim}\,\hat{\beta}$ en función de `vx` y `ve`:",
            "expected_answer": "8*vx/(vx+ve)",
        },
        {
            "id": "Q-Hab18-1082",
            "stem": r"Con $\beta=9$, señal `sx` ($\sigma_x$) y ruido $5 \cdot \text{se}$, exprese $\text{plim}\,\hat{\beta}$:",
            "expected_answer": "9*sx**2/(sx**2+(5*se)**2)",
        },
    ]
    for case in valid_cases:
        assert check_open_symbolic_answer_closure(case, "open_symbolic") == []
