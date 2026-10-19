"""Unit Tests for LaTeX Engine & Syntax Normalization (Content-to-Course v3.22 Stream B).

Tests:
1. Subindices inside \\frac:
   - Preserves \\hat{\\beta}_1 = \\frac{S_{xy}}{S_{xx}} without corrupting subindices.
2. Exponents with decimals:
   - Preserves K^{0.5} and L^{0.5} without KeyError in template interpolation.
3. Operator macros:
   - Preserves \\operatorname{arccot}(y/x) without KeyError.
4. Variable substitution:
   - Replaces {alpha} when alpha is a declared variable in vars dict.
5. Double curly braces normalization:
   - Normalizes non-variable {{0.5}} to {0.5}.
   - Normalizes {{\\operatorname{arccot}}} to {\\operatorname{arccot}}.
   - Preserves declared variables when protected.
6. Integration with KaTeX validation and assemble_question:
   - Validates KaTeX syntax passes cleanly with normalized expressions.
"""

import re
import sys
from pathlib import Path
from typing import Any, Dict

import pytest

# Ensure skills root is in sys.path
_skill_root = Path(__file__).resolve().parents[1] / ".agents" / "skills" / "content-to-course"
if str(_skill_root) not in sys.path:
    sys.path.insert(0, str(_skill_root))

from compile_shard import normalize_double_braces
from engine.assemble import format_template_string, assemble_question, sanitize_katex_syntax
from engine.invariants import validate_katex_syntax


class TestLatexEngineNormalization:
    """Tests for LaTeX preservation, variable substitution, and double-brace normalization."""

    def test_frac_subindices_preservation(self):
        r"""Verify \frac{S_{xy}}{S_{xx}} is not corrupted by assemble format_template_string."""
        template_str = r"Calcule la pendiente estimada $\hat{\beta}_1 = \frac{S_{xy}}{S_{xx}}$ para el modelo."
        variables = {"n": 50, "x_bar": 12.5}
        result = format_template_string(template_str, variables)
        assert r"\frac{S_{xy}}{S_{xx}}" in result
        assert "S_{xy}" in result
        assert "S_{xx}" in result

        # Verify KaTeX validation passes with no errors
        errors = validate_katex_syntax(result, "test_frac")
        assert not errors, f"KaTeX errors found: {errors}"

    def test_k_exponent_decimals(self):
        r"""Verify K^{0.5} is preserved and does not trigger KeyError in format_template_string."""
        template_str = r"La función de producción Cobb-Douglas es $Y = K^{0.5} L^{0.5}$."
        variables = {"A": 1.0, "alpha": 0.5}
        result = format_template_string(template_str, variables)
        assert r"K^{0.5}" in result
        assert r"L^{0.5}" in result

        # Verify KaTeX validation passes
        errors = validate_katex_syntax(result, "test_exponent")
        assert not errors, f"KaTeX errors found: {errors}"

    def test_operatorname_arccot_preservation(self):
        r"""Verify \operatorname{arccot}(y/x) is preserved without KeyError."""
        template_str = r"El ángulo característico se define como $\theta = \operatorname{arccot}\left(\frac{y}{x}\right)$."
        variables = {"x": 3, "y": 4}
        result = format_template_string(template_str, variables)
        assert r"\operatorname{arccot}" in result

        errors = validate_katex_syntax(result, "test_arccot")
        assert not errors, f"KaTeX errors found: {errors}"

    def test_alpha_variable_substitution(self):
        r"""Verify {alpha} is substituted when 'alpha' is a declared variable."""
        template_str = r"Con un nivel de significancia $\alpha = {alpha}$, rechace $H_0$ si $p < {alpha}$."
        variables = {"alpha": 0.05}
        result = format_template_string(template_str, variables)
        assert "0.05" in result
        assert "{alpha}" not in result
        assert r"$\alpha = 0.05$" in result

    def test_double_brace_decimal_normalization(self):
        r"""Verify {{0.5}} is normalized to {0.5} when 0.5 is not a declared variable."""
        raw_text = r"Considere el exponente $K^{{0.5}}$ y $L^{{0.5}}$."
        declared_vars = {"A", "K_val"}
        normalized = normalize_double_braces(raw_text, declared_vars=declared_vars)
        assert normalized == r"Considere el exponente $K^{0.5}$ y $L^{0.5}$."
        assert "{{" not in normalized
        assert "}}" not in normalized

        # Ensure R-20 / KaTeX validation passes
        errors = validate_katex_syntax(normalized, "test_norm_decimal")
        assert not errors, f"KaTeX syntax errors: {errors}"

    def test_double_brace_operator_and_subscript_normalization(self):
        r"""Verify {{\operatorname{arccot}}} and {{S_{xy}}} are normalized."""
        raw_text = r"Fórmula: ${{\operatorname{arccot}}}\left(\frac{{{S_{xy}}}}{{{S_{xx}}}}\right)$."
        declared_vars = set()
        normalized = normalize_double_braces(raw_text, declared_vars=declared_vars)
        assert r"\operatorname{arccot}" in normalized
        assert r"S_{xy}" in normalized
        assert r"S_{xx}" in normalized
        assert "{{" not in normalized
        assert r"\frac{S_{xy}}{S_{xx}}" in normalized

        # Ensure KaTeX syntax validation passes cleanly on normalized text
        errors = validate_katex_syntax(normalized, "test_norm_op_subscript")
        assert not errors, f"KaTeX syntax errors: {errors}"


    def test_double_brace_declared_var_protection(self):
        r"""Verify declared variables in {{var}} are preserved if intended for variable substitution."""
        raw_text = r"El valor de {{0.5}} es numérico, pero {{param_x}} es una variable."
        declared_vars = {"param_x"}
        normalized = normalize_double_braces(raw_text, declared_vars=declared_vars)
        # 0.5 is not in declared_vars, so {{0.5}} -> {0.5}
        assert "{0.5}" in normalized
        assert "{{0.5}}" not in normalized
        # param_x is in declared_vars, so {{param_x}} is kept for formatting
        assert "{{param_x}}" in normalized

    def test_sanitize_katex_syntax_residual_double_braces(self):
        r"""Verify sanitize_katex_syntax handles residual double braces from f-strings."""
        text = r"Solución: $\beta = \frac{{S_{xy}}}{{S_{xx}}} = {beta_val}$."
        sanitized = sanitize_katex_syntax(text)
        assert r"\frac{S_{xy}}{S_{xx}}" in sanitized
        assert "{{" not in sanitized or "{{beta_val}}" in sanitized
