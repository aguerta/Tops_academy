"""Tests focalizados para los linters de hardening en standardized_audit_engine.py."""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / ".agents" / "skills" / "course-qa-evaluator" / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from standardized_audit_engine import (  # noqa: E402
    DiagnosticRationaleAlignmentLinter,
    DomainImpossibleDistractorLinter,
    FibRoundingContractLinter,
    LintIssue,
    MsLengthBiasLinter,
    run_full_audit,
)


def _base_course(questions: list[dict]) -> dict:
    return {
        "course_id": "test_hardening",
        "title": "Estadística Hardening",
        "competencies": [{"id": "C1", "category": "Skill", "prerequisites": ["C0"]}],
        "questions": questions,
    }


# ---------------------------------------------------------------------------
# 1. DomainImpossibleDistractorLinter
# ---------------------------------------------------------------------------

def test_domain_impossible_negative_variance_flagged():
    linter = DomainImpossibleDistractorLinter()
    issues: list[LintIssue] = []
    course = _base_course([
        {
            "id": "q_var_neg",
            "competency_id": "C1",
            "stem": "Calcule la varianza muestral de los datos observados.",
            "options": [
                {"text": "4.5", "is_correct": True},
                {"text": "-2.1", "is_correct": False},
                {"text": "3.2", "is_correct": False},
            ],
        },
        {
            "id": "q_ecm_neg",
            "competency_id": "C1",
            "stem": "Determine el ECM del estimador insesgado.",
            "options": [
                {"text": "0.18", "is_correct": True},
                {"text": "$ -0.05 $", "is_correct": False},
            ],
        },
        {
            "id": "q_n_neg",
            "competency_id": "C1",
            "stem": "¿Cuál es el tamaño de muestra mínimo requerido?",
            "options": [
                {"text": "30", "is_correct": True},
                {"text": "-12", "is_correct": False},
            ],
        },
    ])
    summary = linter.run(course, issues)
    assert summary["negative_non_neg_magnitude_count"] == 3
    assert summary["domain_impossible_items_count"] == 3
    assert len(issues) == 3
    assert all(iss.severity == "critical" for iss in issues)


def test_domain_impossible_prob_gt_one_flagged_and_bounds_excluded():
    linter = DomainImpossibleDistractorLinter()
    issues: list[LintIssue] = []
    course = _base_course([
        {
            "id": "q_prob_gt1",
            "competency_id": "C1",
            "stem": "Calcule la probabilidad de que X sea mayor que 2.",
            "options": [
                {"text": "0.35", "is_correct": True},
                {"text": "1.25", "is_correct": False},
            ],
        },
        {
            "id": "q_chebyshev_ok",
            "competency_id": "C1",
            "stem": "Usando la desigualdad de Chebyshev, obtenga una cota superior para la probabilidad.",
            "options": [
                {"text": "0.25", "is_correct": True},
                {"text": "1.50", "is_correct": False},
            ],
        },
        {
            "id": "q_prob_pct_ok",
            "competency_id": "C1",
            "stem": "Determine la probabilidad exacta del evento A.",
            "options": [
                {"text": "45%", "is_correct": True},
                {"text": "65%", "is_correct": False},
            ],
        },
        {
            "id": "q_var_valid_ok",
            "competency_id": "C1",
            "stem": "Calcule la desviación estándar de la muestra.",
            "options": [
                {"text": "2.4", "is_correct": True},
                {"text": "1.8", "is_correct": False},
            ],
        },
    ])
    summary = linter.run(course, issues)
    assert summary["prob_gt_one_count"] == 1
    assert summary["domain_impossible_items_count"] == 1
    assert [iss.item_id for iss in issues] == ["q_prob_gt1"]


# ---------------------------------------------------------------------------
# 2. FibRoundingContractLinter
# ---------------------------------------------------------------------------

def test_fib_rounding_contract_flags_uncontracted_3_decimals():
    linter = FibRoundingContractLinter()
    issues: list[LintIssue] = []
    course = _base_course([
        {
            "id": "fib_bad",
            "competency_id": "C1",
            "type": "fill_in_the_blank",
            "allow_calculator": False,
            "stem": "Calcule el valor esperado de X.",
            "correct_answer": "0.125",
        },
        {
            "id": "fib_bad_float",
            "competency_id": "C1",
            "type": "fib",
            "allow_calculator": False,
            "stem": "Determine el coeficiente.",
            "correct_answer": 1.3456,
        },
    ])
    summary = linter.run(course, issues)
    assert summary["fib_uncontracted_rounding_count"] == 2
    assert {iss.item_id for iss in issues} == {"fib_bad", "fib_bad_float"}
    assert all(iss.severity == "warning" for iss in issues)


def test_fib_rounding_contract_allows_explicit_rounding_calc_or_short_decimals():
    linter = FibRoundingContractLinter()
    issues: list[LintIssue] = []
    course = _base_course([
        {
            "id": "fib_with_instruction",
            "competency_id": "C1",
            "type": "fill_in_the_blank",
            "allow_calculator": False,
            "stem": "Calcule el valor esperado y redondee a 3 decimales.",
            "correct_answer": "0.125",
        },
        {
            "id": "fib_with_calc",
            "competency_id": "C1",
            "type": "fill_in_the_blank",
            "allow_calculator": True,
            "stem": "Calcule el valor esperado.",
            "correct_answer": "0.125",
        },
        {
            "id": "fib_two_decimals",
            "competency_id": "C1",
            "type": "fill_in_the_blank",
            "allow_calculator": False,
            "stem": "Calcule el valor esperado.",
            "correct_answer": "0.25",
        },
    ])
    summary = linter.run(course, issues)
    assert summary["fib_uncontracted_rounding_count"] == 0
    assert issues == []


# ---------------------------------------------------------------------------
# 3. MsLengthBiasLinter
# ---------------------------------------------------------------------------

def test_ms_length_bias_flags_when_gt_60_pct_exceed_115x():
    linter = MsLengthBiasLinter()
    issues: list[LintIssue] = []
    ms_biased = lambda qid: {
        "id": qid,
        "competency_id": "C1",
        "type": "multiple_select",
        "options": [
            {"text": "Opción correcta muy detallada y extensa", "is_correct": True},
            {"text": "Opción falsa corta", "is_correct": False},
        ],
    }
    ms_balanced = {
        "id": "ms_ok",
        "competency_id": "C1",
        "type": "multiple_select",
        "options": [
            {"text": "Texto corto equivalente", "is_correct": True},
            {"text": "Texto corto alternativo", "is_correct": False},
        ],
    }
    # 3 de 4 biased = 75% > 60%
    course = _base_course([ms_biased("ms_1"), ms_biased("ms_2"), ms_biased("ms_3"), ms_balanced])
    summary = linter.run(course, issues)
    assert summary["total_ms_items"] == 4
    assert summary["biased_ms_items_count"] == 3
    assert summary["biased_ms_pct"] == 75.0
    assert len(issues) == 1
    assert issues[0].severity == "warning"


def test_ms_length_bias_does_not_flag_at_or_below_60_pct():
    linter = MsLengthBiasLinter()
    issues: list[LintIssue] = []
    ms_biased = lambda qid: {
        "id": qid,
        "competency_id": "C1",
        "type": "multiple_select",
        "options": [
            {"text": "Opción correcta muy detallada y extensa", "is_correct": True},
            {"text": "Opción falsa corta", "is_correct": False},
        ],
    }
    ms_balanced = lambda qid: {
        "id": qid,
        "competency_id": "C1",
        "type": "multiple_select",
        "options": [
            {"text": "Misma longitud A", "is_correct": True},
            {"text": "Misma longitud B", "is_correct": False},
        ],
    }
    # 3 de 5 biased = 60.0% (no supera 60%)
    course = _base_course([
        ms_biased("ms_1"),
        ms_biased("ms_2"),
        ms_biased("ms_3"),
        ms_balanced("ms_4"),
        ms_balanced("ms_5"),
    ])
    summary = linter.run(course, issues)
    assert summary["biased_ms_pct"] == 60.0
    assert issues == []


def test_ms_length_bias_ignores_within_r15_ms_tolerance():
    linter = MsLengthBiasLinter()
    issues: list[LintIssue] = []
    # Ratio = 71 / 64.5 = 1.101 <= 1.15 and abs diff = 6.5 < 8.0 (aligned with [R-15-MS])
    ms_grey_zone = {
        "id": "ms_grey",
        "competency_id": "C1",
        "type": "multiple_select",
        "options": [
            {"text": "Aunque w/p=29 cambie, L(t)=132 e^(0.03t) es totalmente inelástica", "is_correct": True},
            {"text": "Si w/p=29, persiste desempleo L_emp < 132 e^(0.03t) en equilibrio", "is_correct": False},
        ],
    }
    course = _base_course([ms_grey_zone])
    summary = linter.run(course, issues)
    assert summary["biased_ms_items_count"] == 0
    assert issues == []


# ---------------------------------------------------------------------------
# 4. DiagnosticRationaleAlignmentLinter: numeric literal normalization
# ---------------------------------------------------------------------------

def test_diagnostic_rationale_numeric_normalization_detects_template_recycling():
    linter = DiagnosticRationaleAlignmentLinter()
    issues: list[LintIssue] = []
    # 60 distractors whose rationales only differ by numeric literals
    questions = []
    for i in range(1, 31):
        questions.append({
            "id": f"q_{i}",
            "competency_id": "C1",
            "options": [
                {"text": f"{i * 2}", "is_correct": True},
                {"text": f"{i * 2 + 1}", "is_correct": False, "error_rationale": f"Confundiste el parámetro {i} con {i + 0.5}."},
                {"text": f"{i * 2 + 2}", "is_correct": False, "error_rationale": f"Confundiste el parámetro {i * 3} con {i * 3 + 1.25}."},
            ],
        })
    course = _base_course(questions)
    summary = linter.run(course, issues)
    assert summary["total_rationales"] == 60
    assert summary["unique_rationales"] == 1
    assert summary["rationale_uniqueness_pct"] < 15.0
    assert any(iss.dimension == "D3_scaffolding" and "Reciclaje masivo" in iss.message for iss in issues)


def test_diagnostic_rationale_numeric_normalization_preserves_diverse_templates():
    linter = DiagnosticRationaleAlignmentLinter()
    issues: list[LintIssue] = []
    questions = []
    for i in range(1, 31):
        questions.append({
            "id": f"q_{i}",
            "competency_id": "C1",
            "options": [
                {"text": f"{i}", "is_correct": True},
                {"text": f"{i + 1}", "is_correct": False, "error_rationale": f"Error conceptual tipo alfa_{i}: omitiste el factor de corrección."},
                {"text": f"{i + 2}", "is_correct": False, "error_rationale": f"Error conceptual tipo beta_{i}: invertiste el numerador y denominador."},
            ],
        })
    course = _base_course(questions)
    summary = linter.run(course, issues)
    assert summary["total_rationales"] == 60
    assert summary["unique_rationales"] == 60
    assert summary["rationale_uniqueness_pct"] == 100.0
    assert not any("Reciclaje masivo" in iss.message for iss in issues)


# ---------------------------------------------------------------------------
# 5. Registry Integration
# ---------------------------------------------------------------------------

def test_run_full_audit_includes_new_linters():
    course = _base_course([
        {
            "id": "q_int",
            "competency_id": "C1",
            "type": "fill_in_the_blank",
            "allow_calculator": False,
            "stem": "Calcule la varianza.",
            "correct_answer": "0.123",
            "hints": ["h1", "h2", "h3"],
            "detailed_solution": {"steps": ["s1"]},
        }
    ])
    report = run_full_audit(course)
    summaries = report["dimension_summaries"]
    assert "domain_impossible_distractor_linter" in summaries
    assert "fib_rounding_contract_linter" in summaries
    assert "ms_length_bias_linter" in summaries
    assert summaries["fib_rounding_contract_linter"]["fib_uncontracted_rounding_count"] == 1
