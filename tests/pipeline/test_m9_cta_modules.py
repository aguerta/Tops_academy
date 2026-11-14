"""Contract and unit tests for Milestone 9 CTA modules, PRE-XX prerequisites, and deterministic backfill."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import jsonschema

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / ".agents" / "skills" / "content-to-course"
SCRIPTS_DIR = REPO_ROOT / "scripts"

for p in (str(REPO_ROOT), str(SKILL_DIR), str(SCRIPTS_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

from compile_cta import compile_cta_module  # noqa: E402
from run import PipelineRunner  # noqa: E402
from scripts.backfill_m9_hierarchy import (  # noqa: E402
    backfill_courses,
    parse_competence_analysis_md,
)
from src.validator.core import validate_course_content  # noqa: E402
from src.validator.schema_validator import validate_schema  # noqa: E402


def _make_distractors(prefix: str = "D-PRE01") -> list[dict]:
    return [
        {
            "id": f"{prefix}-{i:02d}",
            "name": f"Error común {i}",
            "wrong_belief": f"Creencia errónea detallada sobre concepto {i} en la expresión.",
            "correct_belief": f"Forma correcta del concepto {i} en la derivación.",
            "trigger": f"Trigger {i}",
            "manifestation": f"Manifestación {i}",
            "error_type": "conceptual_swap",
            "severity": "high",
            "origin": "source",
            "evidence": {"doc": "apuntes.pdf", "page": 1},
            "remediation_hint": (
                f"Recuerda verificar cuidadosamente la definición formal del concepto {i} "
                "antes de sustituir en la ecuación principal."
            ),
        }
        for i in range(1, 7)
    ]


def _make_valid_question(comp_id: str, q_id: str) -> dict:
    return {
        "id": q_id,
        "question_id": q_id,
        "competency_id": comp_id,
        "bloom_taxonomy_level": "Apply",
        "difficulty": "easy",
        "interaction_type": "multiple_choice_7_options",
        "type": "multiple_choice_7_options",
        "context_application": f"Evaluación conceptual para {comp_id}",
        "stem": r"Bajo $\dot{K} = sQ$ y $k = K/L$, determine el producto por trabajador $q$ cuando $Q = 100$ y $L = 25$:",
        "hints": [
            r"La forma intensiva normaliza el producto dividiendo entre el trabajo $L$.",
            r"Evalúa $q = \frac{Q}{L}$ con los valores numéricos dados.",
            r"La relación capital-trabajo intensiva es $k = K/L$.",
        ],
        "detailed_solution": r"El producto intensivo es $q = \frac{100}{25} = 4$.",
        "common_misconception_warning": "Confunde producto agregado con producto por trabajador.",
        "misconception_warning": "Confunde producto agregado con producto por trabajador.",
        "interface_config": {
            "allow_calculator": False,
            "input_placeholder": None,
            "expected_format": "single_selection",
            "grading_policy": "single_choice",
        },
        "options": [
            {"id": "opt_a", "option_id": "A", "content": "$q = 4$", "is_correct": True, "error_rationale": None},
            {"id": "opt_b", "option_id": "B", "content": "$q = 2$", "is_correct": False, "error_rationale": "Divide incorrectamente por un factor adicional de 2."},
            {"id": "opt_c", "option_id": "C", "content": "$q = 5$", "is_correct": False, "error_rationale": "Aproxima erróneamente el cociente $100/25$."},
            {"id": "opt_d", "option_id": "D", "content": "$q = 10$", "is_correct": False, "error_rationale": "Calcula la raíz cuadrada del producto total $Q$."},
            {"id": "opt_e", "option_id": "E", "content": "$q = 25$", "is_correct": False, "error_rationale": "Confunde el producto por trabajador con el insumo $L$."},
            {"id": "opt_f", "option_id": "F", "content": "$q = 75$", "is_correct": False, "error_rationale": "Resta $L$ de $Q$ en lugar de dividir."},
            {"id": "opt_g", "option_id": "G", "content": "$q = 100$", "is_correct": False, "error_rationale": "Confunde el producto por trabajador con el producto agregado $Q$."},
        ],
        "correct_answer": "A",
    }


def test_cta_schema_accepts_pre_competency_and_modules() -> None:
    schema_path = SKILL_DIR / "schemas" / "cta.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    cta_doc = {
        "course_id": "m9_test_course",
        "title": "M9 Test Course",
        "macro_competency": "Dominio de pruebas M9",
        "modules": [
            {
                "id": "mod_1",
                "title": "Módulo 1",
                "source_file": "apuntes.pdf",
            }
        ],
        "competencies": [
            {
                "id": "PRE-01",
                "is_prerequisite": True,
                "type": "fact",
                "name": "Álgebra básica de derivadas",
                "description_latex": r"Regla de la potencia $\frac{d}{dx}x^n = n x^{n-1}$.",
                "bloom": "Remember",
                "session": "Prerrequisitos",
                "unit_index": 0,
                "prerequisites": [],
                "evidence": [{"doc": "apuntes.pdf", "page": 1}],
                "distractors": _make_distractors("D-PRE01"),
                "assumptions": [
                    {
                        "id": "A-PRE01-01",
                        "name": "Exponente real",
                        "statement_latex": r"$n \in \mathbb{R}$",
                        "violation_consequence": "No aplica la regla polinómica estándar.",
                        "role_in_proof": "Base de diferenciación.",
                    }
                ],
            }
        ],
    }

    jsonschema.validate(instance=cta_doc, schema=schema)


def test_course_schema_validator_accepts_pre_competency_and_modules() -> None:
    course_doc = {
        "schema_version": "1.0.0",
        "course_id": "m9_test_course",
        "course_title": "M9 Test Course",
        "description": "Curso de prueba para validar esquema de módulos y competencias PRE.",
        "language": "es",
        "created_at": "2026-11-14T00:00:00+00:00",
        "modules": [
            {
                "id": "mod_1",
                "title": "Módulo 1",
                "source_file": "apuntes.pdf",
            }
        ],
        "competencies": [
            {
                "id": "PRE-01",
                "code": "PRE-01",
                "name": "Álgebra básica",
                "category": "Fact",
                "description": "Regla básica de derivación.",
                "mastery_target": 100,
                "prerequisites": [],
                "is_prerequisite": True,
                "session": "Prerrequisitos",
                "unit_index": 0,
            }
        ],
        "questions": [_make_valid_question("PRE-01", "Q-PRE01-001")],
    }

    errors = validate_schema(course_doc)
    assert errors == []


def test_compile_cta_sets_is_prerequisite_for_pre_tuples_and_dicts() -> None:
    distractors_raw = [
        (
            f"Trampa {i}",
            f"Creencia incorrecta número {i} en la derivada.",
            f"Creencia correcta número {i}.",
            "$x^2$",
            f"Revisar cuidadosamente la regla de derivación número {i} paso a paso para evitar el error.",
            None,
        )
        for i in range(1, 7)
    ]

    tuple_item = (
        "fact",
        "PRE-01",
        "Derivada de potencia",
        r"$\frac{d}{dx}x^n = n x^{n-1}$",
        "Remember",
        "apuntes.pdf",
        1,
        [],
        distractors_raw,
        [("Regla real", r"$n \in \mathbb{R}$", "No aplica", "Base")],
    )
    dict_item = {
        "id": "PRE-02",
        "type": "concept",
        "name": "Regla de la cadena",
        "description_latex": r"$(f \circ g)'(x) = f'(g(x))g'(x)$",
        "bloom": "Understand",
        "doc": "apuntes.pdf",
        "page": 2,
        "prerequisites": ["PRE-01"],
        "distractors": distractors_raw,
        "assumptions": [],
    }

    cta = compile_cta_module(
        [tuple_item, dict_item],
        course_id="m9_compile_test",
        title="M9 Compile Test",
    )
    comps = {c["id"]: c for c in cta["competencies"]}
    assert comps["PRE-01"]["is_prerequisite"] is True
    assert comps["PRE-02"]["is_prerequisite"] is True
    assert comps["PRE-01"]["assumptions"][0]["id"] == "A-PRE01-01"


def test_run_stage_build_exports_m9_fields_to_course() -> None:
    with tempfile.TemporaryDirectory(prefix="m9_run_build_") as tmp:
        work_dir = Path(tmp) / "work"
        templates_dir = work_dir / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        out_dir = Path(tmp) / "courses"
        out_dir.mkdir(parents=True, exist_ok=True)

        cta_payload = {
            "course_id": "m9_run_test",
            "title": "M9 Run Test",
            "macro_competency": "Dominio de pruebas M9",
            "competencies": [
                {
                    "id": "PRE-01",
                    "is_prerequisite": True,
                    "type": "fact",
                    "name": "Derivada de potencia",
                    "description_latex": r"$\frac{d}{dx}x^n = nx^{n-1}$",
                    "bloom": "Remember",
                    "session": "Unidad 0: Prerrequisitos",
                    "unit_index": 0,
                    "prerequisites": [],
                    "evidence": [{"doc": "apuntes.pdf", "page": 1}],
                    "assumptions": [
                        {
                            "id": "A-PRE01-01",
                            "statement_latex": r"$n \in \mathbb{R}$",
                            "violation_consequence": "Falla la regla polinómica.",
                        }
                    ],
                    "distractors": _make_distractors("D-PRE01"),
                }
            ],
        }
        (work_dir / "cta.json").write_text(
            json.dumps(cta_payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        (templates_dir / "PRE-01.json").write_text(
            json.dumps([{"id": "T-PRE01-01", "competency_id": "PRE-01"}]),
            encoding="utf-8",
        )

        mock_question = _make_valid_question("PRE-01", "Q-PRE01-001")

        runner = PipelineRunner(
            course_id="m9_run_test",
            title="M9 Run Test",
            work_dir=work_dir,
            output_dir=out_dir,
        )

        with (
            patch("run.instantiate_competency", return_value=[mock_question]),
            patch("run.check_instance_invariants", return_value=None),
            patch(
                "run.evaluate_competency_diversity",
                return_value={"diversity_ratio": 1.0, "unique_masked": 1, "total": 1},
            ),
            patch("run.validate_course_content") as mock_val,
        ):
            mock_val.return_value.is_valid = True
            mock_val.return_value.errors = []
            runner.run_stage_build()

        exported = json.loads((work_dir / "course.json").read_text(encoding="utf-8"))
        comp = exported["competencies"][0]
        assert comp["id"] == "PRE-01"
        assert comp["is_prerequisite"] is True
        assert comp["session"] == "Unidad 0: Prerrequisitos"
        assert comp["evidence"] == [{"doc": "apuntes.pdf", "page": 1}]
        assert comp["assumptions"][0]["id"] == "A-PRE01-01"


def test_backfill_parses_md_and_preserves_r23_latex() -> None:
    md_sample = """# Cognitive Task Analysis (CTA): Fixture Course

### [C-01] Hipótesis dinámicas (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 2: Hipótesis dinámicas
- **Prerequisites:** None
- **Evidence Citations:** `solow.pdf` (page 2), `notes.pdf` (page 5)

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C01-01` | - | Ahorro canalizado $\\dot{K} = sQ$ con $\\phi(k)$ | Acumulación se desfasa. | - |
| `A-C01-02` | Continuidad | $K(t), L(t) \\in C^1$ | No aplica Leibniz. | Base diferencial |
"""
    parsed = parse_competence_analysis_md(md_sample)
    assert "C-01" in parsed
    assert parsed["C-01"]["session"] == "Unidad 2: Hipótesis dinámicas"
    assert parsed["C-01"]["evidence"] == [
        {"doc": "solow.pdf", "page": 2},
        {"doc": "notes.pdf", "page": 5},
    ]
    assumptions = parsed["C-01"]["assumptions"]
    assert len(assumptions) == 2
    assert assumptions[0] == {
        "id": "A-C01-01",
        "statement_latex": r"Ahorro canalizado $\dot{K} = sQ$ con $\phi(k)$",
        "violation_consequence": "Acumulación se desfasa.",
    }
    assert assumptions[1]["name"] == "Continuidad"
    assert assumptions[1]["role_in_proof"] == "Base diferencial"

    with tempfile.TemporaryDirectory(prefix="m9_backfill_") as tmp:
        cdir = Path(tmp) / "courses"
        cdir.mkdir(parents=True, exist_ok=True)
        (cdir / "competence_analysis_fixture_course.md").write_text(
            md_sample, encoding="utf-8"
        )
        course_payload = {
            "schema_version": "1.0.0",
            "course_id": "fixture_course",
            "course_title": "Fixture Course",
            "description": "Curso fixture para verificar backfill determinista y R-23.",
            "language": "es",
            "created_at": "2026-11-14T00:00:00+00:00",
            "competencies": [
                {
                    "id": "C-01",
                    "code": "C-01",
                    "name": "Hipótesis dinámicas",
                    "category": "Concept",
                    "description": r"Tasa de variación $\dot{K} = sQ$ y función $\phi(k)$.",
                    "mastery_target": 100,
                    "prerequisites": [],
                }
            ],
            "questions": [
                {
                    **_make_valid_question("C-01", f"Q-C01-{i:03d}"),
                    "stem": (
                        rf"Bajo $\dot{{K}} = sQ$ y $k = K/L$, determine el producto "
                        rf"por trabajador $q$ en el escenario {i} cuando $Q = 100$ y $L = 25$:"
                    ),
                }
                for i in range(1, 21)
            ],
        }
        course_path = cdir / "fixture_course.json"
        course_path.write_text(
            json.dumps(course_payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        summary = backfill_courses(courses_dir=cdir, work_dir=None, write=True)
        assert summary["courses_updated"] == 1
        assert summary["competencies_hydrated"] == 1

        updated_raw = course_path.read_text(encoding="utf-8")
        val = validate_course_content(updated_raw, file_path=str(course_path), strict=True)
        assert val.is_valid, f"Expected strict validation pass, got: {val.errors}"

        updated_data = json.loads(updated_raw)
        c01 = updated_data["competencies"][0]
        assert c01["session"] == "Unidad 2: Hipótesis dinámicas"
        assert len(c01["evidence"]) == 2
        assert len(c01["assumptions"]) == 2
        # Verify R-23: no over-escaped backslashes in serialized JSON
        assert "\\\\\\\\dot" not in updated_raw
        assert "\\\\\\\\phi" not in updated_raw
