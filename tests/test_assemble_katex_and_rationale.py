"""Tests for KaTeX sanitization shielding and distractor error_rationale author preservation / safe inheritance.

Validates:
1. sanitize_katex_syntax does NOT corrupt fractions with multiple subscripts/superscripts (b_{IV} - b_{LS}).
2. sanitize_katex_syntax continues to repair genuine dropped numerator closing braces (\\frac{a_{1}{b}).
3. assemble_question preserves author-provided error_rationale in MC7 and MS even when cta_distractors_map has broken LaTeX or conflicting text.
4. assemble_question safely inherits from cta_distractors_map when author rationale is omitted or generic, skipping broken LaTeX manifestations and falling back to wrong_belief / omitted_step / remediation_hint.
"""

import sys
from pathlib import Path
from typing import Any, Dict

import pytest

# Ensure skills root is in sys.path
_skill_root = Path(__file__).resolve().parents[1] / ".agents" / "skills" / "content-to-course"
if str(_skill_root) not in sys.path:
    sys.path.insert(0, str(_skill_root))

from engine.assemble import (
    assemble_question,
    format_template_string,
    sanitize_katex_syntax,
    _resolve_distractor_rationale,
    _is_generic_placeholder,
    _is_katex_valid,
)
from engine.invariants import check_instance_invariants, validate_katex_syntax


# ==============================================================================
# 1. KaTeX Fraction Shielding Tests
# ==============================================================================

def test_sanitize_katex_hausman_variance_fractions_intact():
    """Verify KaTeX sanitization leaves balanced fractions with subscripts/superscripts completely intact."""
    cases = [
        r"$H = \frac{(b_{IV} - b_{LS})^2}{\text{Var}(b_{IV}) - \text{Var}(b_{LS})}$",
        r"$H = \frac{(b_{IV} - b_{LS})^2}{\text{Var}[b_{IV}] + \text{Var}[b_{LS}]}$",
        r"$\dfrac{(b_{IV} - b_{LS})^2}{\text{Var}(b_{IV}) - \text{Var}(b_{LS})}$",
        r"$\tfrac{(b_{IV} - b_{LS})^2}{\text{Var}[b_{IV}] + \text{Var}[b_{LS}]}$",
        r"$\frac{x_{1}^2 + y_{2}^3}{z_{3}^4 - w_{4}^5}$",
        r"$\frac{(a_{1} - a_{2})^2}{\sigma_{1}^2 + \sigma_{2}^2}$",
    ]
    for expr in cases:
        sanitized = sanitize_katex_syntax(expr)
        assert sanitized == expr, f"Expression was corrupted by sanitize_katex_syntax:\nOriginal: {expr}\nResult:   {sanitized}"
        assert "_}{" not in sanitized, f"Corrupted subscript detected in: {sanitized}"
        assert "^}{" not in sanitized, f"Corrupted superscript detected in: {sanitized}"


def test_sanitize_katex_fraction_shielded_even_with_loose_braces_elsewhere():
    """Verify that even if an unclosed brace exists elsewhere in the string, balanced fractions are NOT corrupted."""
    target_frac = r"\frac{(b_{IV} - b_{LS})^2}{\text{Var}[b_{IV}] + \text{Var}[b_{LS}]}"
    loose_text = f"Considere el contraste de especificación ${target_frac}$ con {{parametro_no_cerrado"
    
    sanitized = sanitize_katex_syntax(loose_text)
    assert target_frac in sanitized, "Target fraction was corrupted when loose brace existed elsewhere"
    assert "_}{LS}" not in sanitized, "Corruption b_}{LS} detected!"
    assert "_}{" not in sanitized


def test_sanitize_katex_repairs_genuine_missing_numerator_brace():
    """Verify that genuine missing numerator closing braces are cleanly repaired."""
    test_cases = [
        (r"\frac{a_{1}{b}", r"\frac{a_{1}}{b}"),
        (r"\dfrac{\hat{\theta}{V}", r"\dfrac{\hat{\theta}}{V}"),
        (r"\tfrac{x^{2}{y}", r"\tfrac{x^{2}}{y}"),
        (r"\frac{a{b}", r"\frac{a}{b}"),
    ]
    for raw, expected in test_cases:
        repaired = sanitize_katex_syntax(raw)
        assert repaired == expected, f"Failed to repair {raw}: got {repaired}, expected {expected}"
        assert "_}{" not in repaired
        assert "^}{" not in repaired


# ==============================================================================
# 2. Distractor Rationale Helper Unit Tests
# ==============================================================================

def test_is_generic_placeholder():
    """Verify identification of generic boilerplate placeholders vs explicit author rationales."""
    generic_samples = [
        "",
        "   ",
        "Distractor.",
        "distractor",
        "Opción incorrecta.",
        "opcion incorrecta",
        "Incorrecto.",
        "incorrecta",
        "Static",
        "Dummy rationale",
        "Placeholder distractor",
        "Distractor derivado de error de procedimiento o misconception",
        "Opción inválida derivada de una concepción errónea del concepto o propiedad.",
    ]
    for g in generic_samples:
        assert _is_generic_placeholder(g), f"Expected '{g}' to be recognized as generic placeholder"

    author_samples = [
        "El estudiante omite el sesgo de selección en la ecuación estructural.",
        "Confunde la varianza asintótica del estimador IV con la del estimador OLS.",
        "Asume erróneamente que la matriz de instrumentos es ortogonal a los residuos.",
    ]
    for a in author_samples:
        assert not _is_generic_placeholder(a), f"Expected '{a}' to be recognized as explicit author rationale"


def test_resolve_distractor_rationale_preserves_author_explicit():
    """Verify that explicit author rationale is preserved regardless of CTA map contents."""
    d_dict = {
        "value": "$b_{OLS}$",
        "error_rationale": "El autor indica explícitamente que OLS sufre de sesgo de variable omitida.",
    }
    cta_map = {
        "D-01": {
            "manifestation": r"$H = \frac{(b_{IV} - b_{LS})^2{\text{Var}[b_{IV}]}$",  # Broken LaTeX
            "wrong_belief": "Belief texto",
        }
    }
    resolved = _resolve_distractor_rationale(d_dict, "D-01", cta_map, "Fallback por defecto")
    assert resolved == "El autor indica explícitamente que OLS sufre de sesgo de variable omitida."


def test_resolve_distractor_rationale_skips_broken_latex_manifestation():
    """Verify that when author rationale is empty, CTA manifestation with broken LaTeX is skipped in favor of wrong_belief."""
    d_dict = {
        "value": "$b_{OLS}$",
        "error_rationale": None,
    }
    cta_map = {
        "D-02": {
            "manifestation": r"Error con KaTeX desbalanceado $H = \frac{(b_{IV} - b_{LS})^2",  # Unclosed macro & $
            "wrong_belief": "El estudiante asume homocedasticidad sin verificar la prueba de White.",
            "omitted_step": "Omitió calcular la matriz de covarianza robusta.",
            "remediation_hint": "Utilice estimadores consistentes con heterocedasticidad.",
        }
    }
    resolved = _resolve_distractor_rationale(d_dict, "D-02", cta_map, "Fallback por defecto")
    assert resolved == "El estudiante asume homocedasticidad sin verificar la prueba de White."


# ==============================================================================
# 3. Full Question Assembly Integration Tests (MC7 & MS)
# ==============================================================================

def test_assemble_question_preserves_author_error_rationale_mc7():
    """assemble_question preserves author error_rationale in MC7 options even if CTA map has conflicting or broken LaTeX."""
    template = {
        "id": "TPL-MC7-AUTHOR-RAT",
        "competency_id": "COMP-STAT-01",
        "interaction_type": "multiple_choice_7_options",
        "bloom": "Analyze",
        "difficulty": "hard",
        "stem": "Determine el estadístico de prueba asintótico para $H_0$.",
        "hints": ["Paso 1: Identificar estimadores", "Paso 2: Calcular diferencia", "Paso 3: Evaluar varianza"],
        "detailed_solution": "Solución detallada paso a paso.",
    }
    author_rationale_1 = "RATIONALE AUTOR: El estudiante invierte el orden de los estimadores en la forma cuadrática."
    gen_result = {
        "vars": {"n": 500},
        "correct": "$H = (b_{IV} - b_{LS})' [\\text{Var}(b_{IV}) - \\text{Var}(b_{LS})]^{-1} (b_{IV} - b_{LS})$",
        "distractors": [
            {
                "distractor_id": "D-STAT-01",
                "value": "$H = (b_{LS} - b_{IV})' [\\text{Var}(b_{IV}) + \\text{Var}(b_{LS})]^{-1} (b_{LS} - b_{IV})$",
                "error_rationale": author_rationale_1,
            },
            {"distractor_id": "D-STAT-02", "value": "$H = 1.0$", "error_rationale": ""},
            {"distractor_id": "D-STAT-03", "value": "$H = 2.0$", "error_rationale": None},
            {"distractor_id": "D-STAT-04", "value": "$H = 3.0$", "error_rationale": "Static"},
            {"distractor_id": "D-STAT-05", "value": "$H = 4.0$", "error_rationale": "Opción incorrecta."},
            {"distractor_id": "D-STAT-06", "value": "$H = 5.0$", "error_rationale": "Distractor."},
        ],
    }
    cta_map = {
        "D-STAT-01": {
            "manifestation": r"Manifestation conflictiva con LaTeX roto $H = \frac{(b_{IV} - b_{LS})^2",
            "wrong_belief": "Belief genérico",
        },
        "D-STAT-02": {
            "manifestation": r"Manifestation válida con $H = \frac{(b_{IV} - b_{LS})^2}{\text{Var}[b_{IV}] + \text{Var}[b_{LS}]}$",
            "wrong_belief": "Belief 2",
        },
        "D-STAT-03": {
            "manifestation": r"LaTeX desbalanceado $H = \frac{(b_{IV} - b_{LS})^2",
            "wrong_belief": "Belief 3: Heredado correctamente al fallar manifestation.",
        },
    }

    assembled = assemble_question(
        template=template,
        gen_result=gen_result,
        competency_id="COMP-STAT-01",
        question_index=1,
        cta_distractors_map=cta_map,
        seed=123,
    )

    options = assembled["options"]
    assert len(options) == 7

    # 1. Option for D-STAT-01 MUST have author_rationale_1 intact
    opt_d1 = next(o for o in options if o.get("distractor_id") == "D-STAT-01")
    assert opt_d1["error_rationale"] == author_rationale_1, "Author rationale was overwritten by CTA map!"

    # 2. Option for D-STAT-02 had empty author rationale, so it inherited valid manifestation
    opt_d2 = next(o for o in options if o.get("distractor_id") == "D-STAT-02")
    assert r"\frac{(b_{IV} - b_{LS})^2}{\text{Var}[b_{IV}] + \text{Var}[b_{LS}]}" in opt_d2["error_rationale"]
    assert "_}{LS}" not in opt_d2["error_rationale"]

    # 3. Option for D-STAT-03 had broken manifestation KaTeX, so it safely inherited wrong_belief
    opt_d3 = next(o for o in options if o.get("distractor_id") == "D-STAT-03")
    assert opt_d3["error_rationale"] == "Belief 3: Heredado correctamente al fallar manifestation."

    # Validate all invariants pass on assembled question
    is_valid, errors = check_instance_invariants(assembled, "multiple_choice_7_options")
    assert is_valid, f"Assembled question failed invariants: {errors}"


def test_assemble_question_preserves_author_error_rationale_ms():
    """assemble_question preserves author error_rationale in MS options and inherits cleanly when omitted."""
    template = {
        "id": "TPL-MS-AUTHOR-RAT",
        "competency_id": "COMP-MS-01",
        "interaction_type": "multiple_select",
        "stem": "Seleccione las propiedades válidas de los estimadores.",
        "hints": ["Hint 1", "Hint 2", "Hint 3"],
        "detailed_solution": "Solución detallada.",
    }
    author_rat_ms = "AUTOR MS: La consistencia no garantiza insesgadez en muestras pequeñas."
    gen_result = {
        "vars": {},
        "options": [
            {"content": "El estimador IV es consistente bajo supuestos de rango.", "is_correct": True},
            {"content": "El estimador OLS es insesgado bajo exogeneidad estricta.", "is_correct": True},
            {
                "content": "La consistencia implica que el estimador es insesgado para cualquier tamaño muestral.",
                "is_correct": False,
                "distractor_id": "D-MS-01",
                "error_rationale": author_rat_ms,
            },
            {
                "content": "La varianza de OLS es siempre mayor que la de IV.",
                "is_correct": False,
                "distractor_id": "D-MS-02",
                "error_rationale": None,
            },
        ],
    }
    cta_map = {
        "D-MS-01": {
            "manifestation": r"Texto que NO debe sobreescribir al autor con $H = \frac{(b_{IV} - b_{LS})^2",
        },
        "D-MS-02": {
            "manifestation": r"Error con LaTeX desbalanceado $H = \frac{1",
            "wrong_belief": "Belief MS: OLS es más eficiente que IV bajo homocedasticidad y exogeneidad.",
        },
    }

    assembled = assemble_question(
        template=template,
        gen_result=gen_result,
        competency_id="COMP-MS-01",
        question_index=1,
        cta_distractors_map=cta_map,
        seed=42,
    )

    opt_d1 = next(o for o in assembled["options"] if o.get("distractor_id") == "D-MS-01")
    assert opt_d1["error_rationale"] == author_rat_ms, "Author MS rationale was overwritten!"

    opt_d2 = next(o for o in assembled["options"] if o.get("distractor_id") == "D-MS-02")
    assert opt_d2["error_rationale"] == "Belief MS: OLS es más eficiente que IV bajo homocedasticidad y exogeneidad."

    is_valid, errors = check_instance_invariants(assembled, "multiple_select")
    assert is_valid, f"MS question failed invariants: {errors}"


# ==============================================================================
# 4. Advanced Adversarial & KaTeX Hardening Tests
# ==============================================================================

def test_sanitize_katex_advanced_nested_matrices_and_operators():
    """Verify complex fractions with matrices, operators, and multiple scripts remain 100% intact."""
    complex_expressions = [
        r"$\frac{\begin{pmatrix} a & b \\ c & d \end{pmatrix}}{\det(X'_{i}X_{i})}$",
        r"$\dfrac{(X'_{i}X_{i})^{-1} X'_{i}y_{i} - \hat{\beta}_{2SLS}}{\operatorname{Var}[b_{IV}] + \operatorname{Var}[b_{LS}]}$",
        r"$\cfrac{\hat{\beta}_{2SLS}' (X'X) \hat{\beta}_{2SLS}}{\text{Var}[b_{IV}]}$",
        r"$\tfrac{(X'_{i}X_{i})^{-1} \sum_{i=1}^{n} X'_{i} y_{i}}{\sigma^2}$",
        r"$\frac{b_{IV} - b_{LS}}{\sqrt{\operatorname{Var}(b_{IV}) - \operatorname{Var}(b_{LS})}}$",
    ]
    for expr in complex_expressions:
        # Case 1: Perfectly balanced
        sanitized = sanitize_katex_syntax(expr)
        assert sanitized == expr, f"Corrupted balanced expression: {expr} -> {sanitized}"
        assert "_}{" not in sanitized
        assert "^}{" not in sanitized

        # Case 2: Loose brace outside the fraction
        loose_prefix = f"Considere {{parametro_no_cerrado y la fórmula {expr}"
        sanitized_prefix = sanitize_katex_syntax(loose_prefix)
        assert expr in sanitized_prefix, f"Fraction corrupted when loose brace preceded: {loose_prefix}"
        assert "_}{" not in sanitized_prefix
        assert "^}{" not in sanitized_prefix

        loose_suffix = f"Evaluando {expr} bajo el supuesto {{hipotesis_abierta"
        sanitized_suffix = sanitize_katex_syntax(loose_suffix)
        assert expr in sanitized_suffix, f"Fraction corrupted when loose brace succeeded: {loose_suffix}"
        assert "_}{" not in sanitized_suffix
        assert "^}{" not in sanitized_suffix


def test_sanitize_katex_repairs_subscript_fraction_and_numeric_den():
    """Verify genuine missing numerator braces and numeric denominators are safely repaired."""
    repair_cases = [
        (r"\frac{b_{IV}{b_{LS}}", r"\frac{b_{IV}}{b_{LS}}"),
        (r"\dfrac{x_{1}{y_{2}}", r"\dfrac{x_{1}}{y_{2}}"),
        (r"\tfrac{s}3", r"\tfrac{s}{3}"),
        (r"\frac{k}{2.5}", r"\frac{k}{2.5}"),
        (r"\dfrac{\sigma^2}4", r"\dfrac{\sigma^2}{4}"),
    ]
    for raw, expected in repair_cases:
        res = sanitize_katex_syntax(raw)
        assert res == expected, f"Expected {expected}, got {res} for raw {raw}"
        assert "_}{" not in res
        assert "^}{" not in res


def test_resolve_distractor_rationale_rejects_broken_author_katex_safely():
    """Verify that an author rationale containing unrepairable broken KaTeX is rejected and falls back safely."""
    d_dict_broken = {
        "value": "$b_{OLS}$",
        "error_rationale": r"El autor escribió fórmula rota $H = \frac{(b_{IV} - b_{LS})^2",  # Unclosed math and macro
    }
    cta_map = {
        "D-SAFE-01": {
            "wrong_belief": "El estudiante confunde la varianza muestral con la asintótica.",
        }
    }
    # Should skip the broken author rationale and inherit wrong_belief
    resolved = _resolve_distractor_rationale(
        d_dict=d_dict_broken,
        d_id="D-SAFE-01",
        cta_distractors_map=cta_map,
        default_fallback="Fallback seguro.",
    )
    assert resolved == "El estudiante confunde la varianza muestral con la asintótica."
    assert validate_katex_syntax(resolved, "distractor_rationale") == []

    # If CTA map also absent, falls back to default_fallback
    resolved_fallback = _resolve_distractor_rationale(
        d_dict=d_dict_broken,
        d_id=None,
        cta_distractors_map=None,
        default_fallback="Fallback seguro sin LaTeX roto.",
    )
    assert resolved_fallback == "Fallback seguro sin LaTeX roto."
    assert validate_katex_syntax(resolved_fallback, "distractor_rationale") == []


def test_resolve_distractor_rationale_handles_none_null_na_generic():
    """Verify that 'None', 'null', 'N/A' strings are detected as generic and inherit from CTA map."""
    generics = ["None", "null", "N/A", "n/a", "   ", "dummy", "static"]
    cta_map = {
        "D-GEN-01": {
            "remediation_hint": "Recuerde aplicar el estimador de variables instrumentales en dos etapas.",
        }
    }
    for g in generics:
        d_dict = {"value": "x", "error_rationale": g}
        resolved = _resolve_distractor_rationale(
            d_dict=d_dict,
            d_id="D-GEN-01",
            cta_distractors_map=cta_map,
            default_fallback="Fallback por defecto.",
        )
        assert resolved == "Recuerde aplicar el estimador de variables instrumentales en dos etapas.", f"Failed for generic '{g}'"


def test_assemble_question_mc7_and_ms_strips_giveaway_and_interpolates_vars():
    """Verify giveaway prefix stripping and variable interpolation in distractor rationales for MC7 and MS."""
    template_mc7 = {
        "id": "TPL-MC7-GIVEAWAY",
        "competency_id": "COMP-GIVEAWAY-01",
        "interaction_type": "multiple_choice_7_options",
        "bloom": "Apply",
        "difficulty": "medium",
        "stem": "Stem con @n@ observaciones.",
        "hints": ["Hint 1", "Hint 2", "Hint 3"],
        "detailed_solution": "Solución paso a paso.",
    }
    gen_result_mc7 = {
        "vars": {"n": 500, "param_val": 42},
        "correct": "$H = 100$",
        "distractors": [
            {
                "distractor_id": "D-01",
                "value": "$H = 10$",
                "error_rationale": "Inversión de roles: Asume n = @n@ en vez de param = @param_val@.",
            },
            {"distractor_id": "D-02", "value": "$H = 20$", "error_rationale": "Omisión de límites: Olvida el límite superior."},
            {"distractor_id": "D-03", "value": "$H = 30$", "error_rationale": "Error de signo: Invierte el signo del sesgo."},
            {"distractor_id": "D-04", "value": "$H = 40$", "error_rationale": "Confusión de conceptos: Confunde consistencia con insesgadez."},
            {"distractor_id": "D-05", "value": "$H = 50$", "error_rationale": "Falsa generalización: Generaliza fuera del dominio."},
            {"distractor_id": "D-06", "value": "$H = 60$", "error_rationale": "Asumiendo erróneamente: Asume varianza unitaria."},
        ],
    }

    assembled_mc7 = assemble_question(
        template=template_mc7,
        gen_result=gen_result_mc7,
        competency_id="COMP-GIVEAWAY-01",
        question_index=1,
        cta_distractors_map=None,
        seed=999,
    )

    opt_d1 = next(o for o in assembled_mc7["options"] if o.get("distractor_id") == "D-01")
    assert "Inversión de roles:" not in opt_d1["error_rationale"]
    assert "Asume n = 500 en vez de param = 42." in opt_d1["error_rationale"]
    assert validate_katex_syntax(opt_d1["error_rationale"], "distractor_rationale") == []

    is_valid_mc7, errors_mc7 = check_instance_invariants(assembled_mc7, "multiple_choice_7_options")
    assert is_valid_mc7, f"MC7 question invariants failed: {errors_mc7}"

    # Test MS equivalent with giveaway prefix
    template_ms = {
        "id": "TPL-MS-GIVEAWAY",
        "competency_id": "COMP-GIVEAWAY-02",
        "interaction_type": "multiple_select",
        "stem": "Seleccione opciones.",
        "hints": ["H1", "H2", "H3"],
        "detailed_solution": "Solución.",
    }
    gen_result_ms = {
        "vars": {"alpha": "0.05"},
        "options": [
            {"content": "Opción correcta 1", "is_correct": True},
            {"content": "Opción correcta 2", "is_correct": True},
            {
                "content": "Opción incorrecta 1",
                "is_correct": False,
                "distractor_id": "D-MS-01",
                "error_rationale": "Error de signo: Se utilizó un nivel de significancia erróneo de @alpha@.",
            },
            {
                "content": "Opción incorrecta 2",
                "is_correct": False,
                "distractor_id": "D-MS-02",
                "error_rationale": "Confusión de conceptos: Rechaza H0 cuando p > alpha.",
            },
        ],
    }
    assembled_ms = assemble_question(
        template=template_ms,
        gen_result=gen_result_ms,
        competency_id="COMP-GIVEAWAY-02",
        question_index=1,
        cta_distractors_map=None,
        seed=101,
    )
    opt_ms1 = next(o for o in assembled_ms["options"] if o.get("distractor_id") == "D-MS-01")
    assert "Error de signo:" not in opt_ms1["error_rationale"]
    assert "Se utilizó un nivel de significancia erróneo de 0.05." in opt_ms1["error_rationale"]
    assert validate_katex_syntax(opt_ms1["error_rationale"], "distractor_rationale") == []

    is_valid_ms, errors_ms = check_instance_invariants(assembled_ms, "multiple_select")
    assert is_valid_ms, f"MS question invariants failed: {errors_ms}"
