"""Unit tests for the 4 new deterministic audit linters added via /learn:
1. ClonedDistractorValueLinter
2. ParentheticalTelltaleLinter
3. ArchetypeEntropyLinter
4. UninterpolatedMathVariableLinter
"""
import sys
from pathlib import Path
import pytest

_engine_dir = Path(__file__).resolve().parents[1] / ".agents" / "skills" / "course-qa-evaluator" / "scripts"
if str(_engine_dir) not in sys.path:
    sys.path.insert(0, str(_engine_dir))

from standardized_audit_engine import (
    run_full_audit,
    ClonedDistractorValueLinter,
    ParentheticalTelltaleLinter,
    ArchetypeEntropyLinter,
    UninterpolatedMathVariableLinter,
)


def test_cloned_distractor_value_linter():
    course_data = {
        "course_id": "test_course",
        "competencies": [{"id": "C-01"}],
        "questions": [
            {
                "id": "Q-01",
                "competency_id": "C-01",
                "options": [
                    {"text": "Opción correcta: $x = 5$", "is_correct": True},
                    {"text": "Opción alterna 4: $x = 5$", "is_correct": False},
                ]
            },
            {
                "id": "Q-02",
                "competency_id": "C-01",
                "options": [
                    {"text": "$10$", "is_correct": True},
                    {"text": "$10$", "is_correct": False},
                ]
            }
        ]
    }
    issues = []
    summary = ClonedDistractorValueLinter().run(course_data, issues)
    assert summary["cloned_distractor_items_count"] == 2
    assert len(issues) == 2
    assert issues[0].severity == "critical"


def test_parenthetical_telltale_linter():
    course_data = {
        "course_id": "test_course",
        "competencies": [{"id": "C-01"}],
        "questions": [
            {
                "id": "Q-01",
                "competency_id": "C-01",
                "options": [
                    {"text": "$0.75$ (confusión con la proporción ruido a señal)", "is_correct": False},
                    {"text": "$0.50$ (definición errónea de varianza)", "is_correct": False},
                    {"text": "$0.25$", "is_correct": True},
                ]
            }
        ]
    }
    issues = []
    summary = ParentheticalTelltaleLinter().run(course_data, issues)
    assert summary["parenthetical_telltale_count"] == 1
    assert len(issues) == 2
    assert issues[0].severity == "critical"


def test_archetype_entropy_linter():
    # 20 questions with identical structural skeleton
    questions = []
    for i in range(20):
        questions.append({
            "id": f"Q-{i:02d}",
            "competency_id": "C-01",
            "stem": f"Considere el modelo de Solow con tasa de ahorro $s = 0.{i}$ y depreciación $\\delta = 0.05$. Calcule el capital estacionario.",
        })
    course_data = {
        "course_id": "test_course",
        "competencies": [{"id": "C-01"}],
        "questions": questions
    }
    issues = []
    summary = ArchetypeEntropyLinter().run(course_data, issues)
    assert summary["monotonous_competencies_count"] == 1
    assert "C-01" in summary["monotonous_competencies"]
    assert len(issues) == 1
    assert issues[0].severity == "warning"


def test_uninterpolated_math_variable_linter():
    course_data = {
        "course_id": "test_course",
        "competencies": [{"id": "C-01"}],
        "questions": [
            {
                "id": "Q-01",
                "competency_id": "C-01",
                "stem": "El valor del estimador es $\\hat{\\beta} = {sigma2} / n$.",
                "detailed_solution": "Calculamos $x - -4$ directamente.",
                "options": [{"text": "Valor", "is_correct": True}]
            }
        ]
    }
    issues = []
    summary = UninterpolatedMathVariableLinter().run(course_data, issues)
    assert summary["uninterpolated_math_items_count"] == 1
    assert len(issues) >= 1


def test_full_audit_integration():
    course_data = {
        "course_id": "test_integration",
        "competencies": [{"id": "C-01", "name": "Concepto 1", "type": "Concept", "prerequisites": []}],
        "questions": [
            {
                "id": "Q-01",
                "competency_id": "C-01",
                "stem": "Enunciado limpio $x = 1$.",
                "hints": ["Pista 1", "Pista 2", "Pista 3"],
                "detailed_solution": "Solución detallada paso a paso.",
                "options": [
                    {"text": "Opción A", "is_correct": True, "error_rationale": "Correcto"},
                    {"text": "Opción B", "is_correct": False, "error_rationale": "Falso"},
                ]
            }
        ]
    }
    report = run_full_audit(course_data)
    assert "cloned_distractor_value_linter" in report["dimension_summaries"]
    assert "parenthetical_telltale_linter" in report["dimension_summaries"]
    assert "archetype_entropy_linter" in report["dimension_summaries"]
    assert "uninterpolated_math_variable_linter" in report["dimension_summaries"]
