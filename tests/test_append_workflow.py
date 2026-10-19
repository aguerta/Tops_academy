"""Unit tests for C2C Append Workflow & Environment Resilience (R7, P7).

Covers:
1. prepare.py --append delta generation: reading existing courses/<id>.json, injecting
   existing competency IDs/names and continuous next_ids per category (e.g. Solow 21 -> 45).
2. course_publisher.py warned fallback remap on legacy colliding IDs.
3. CLI Unicode title corruption fallback (\\ufffd) to cta.json or base course metadata.
4. Windows PowerShell path quoting resilience (nested quotes, escaped backslashes).
"""

from __future__ import annotations

import copy
import json
import logging
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

import pytest

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

ROOT_DIR = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT_DIR / ".agents" / "skills" / "content-to-course"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from course_publisher import CoursePublisher
from validator.models import ValidationResult
from prepare import (
    compute_next_ids,
    is_corrupted_unicode,
    prepare_course,
    sanitize_cli_arg,
    sanitize_path,
)
from run import PipelineRunner


def _create_dummy_pdf(pdf_path: Path, num_pages: int = 5) -> None:
    """Creates a genuine, valid multi-page PDF using pymupdf."""
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open()
    for i in range(num_pages):
        page = doc.new_page(width=595, height=842)
        page.insert_text((50, 50), f"Página {i+1} del material fuente de prueba para el curso.")
    doc.save(str(pdf_path))
    doc.close()


def _make_mock_question(qid: str, cid: str, level: str, stem: str, answer: str) -> Dict[str, Any]:
    """Builds a schema-compliant question dictionary with all required fields."""
    return {
        "id": qid,
        "question_id": qid,
        "competency_id": cid,
        "bloom_taxonomy_level": level,
        "difficulty": "medium",
        "interaction_type": "multiple_choice_7_options",
        "context_application": f"Contexto de aplicación para el ítem {qid} de la competencia {cid}.",
        "stem": stem,
        "interface_config": {
            "allow_calculator": False,
            "grading_policy": "single_choice",
        },
        "correct_answer": answer,
        "hints": [
            "Primer paso de andamiaje analítico para resolver el ejercicio paso a paso.",
            "Segundo paso de andamiaje analítico para verificar los cálculos intermedios.",
            "Tercer paso: comprobar la consistencia teórica y dimensional del resultado.",
        ],
        "detailed_solution": f"Solución paso a paso detallada del reactivo {qid} correspondiente a la competencia {cid}.",
        "common_misconception_warning": f"Advertencia sobre el error o misconception típica asociada a {cid}.",
        "options": [
            {"id": "opt_a", "option_id": "A", "content": f"{answer} (Opción correcta con texto suficiente)", "text": f"{answer} (Opción correcta con texto suficiente)", "is_correct": True, "error_rationale": None},
            {"id": "opt_b", "option_id": "B", "content": "Distractor B con suficiente longitud de texto explicativo para pasar.", "text": "Distractor B con suficiente longitud de texto explicativo para pasar.", "is_correct": False, "error_rationale": "Error 1", "distractor_id": f"D-{cid.replace('-', '')}-01"},
            {"id": "opt_c", "option_id": "C", "content": "Distractor C con suficiente longitud de texto explicativo para pasar.", "text": "Distractor C con suficiente longitud de texto explicativo para pasar.", "is_correct": False, "error_rationale": "Error 2", "distractor_id": f"D-{cid.replace('-', '')}-02"},
            {"id": "opt_d", "option_id": "D", "content": "Distractor D con suficiente longitud de texto explicativo para pasar.", "text": "Distractor D con suficiente longitud de texto explicativo para pasar.", "is_correct": False, "error_rationale": "Error 3", "distractor_id": f"D-{cid.replace('-', '')}-03"},
        ],
    }


def _create_mock_course(course_id: str, title: str, num_c: int = 10, num_hab: int = 6, num_h: int = 5) -> Dict[str, Any]:
    """Creates a valid course payload with specific competency category distributions matching schema rules."""
    competencies = []
    questions = []

    # Concepts: C-01 .. C-NN
    for i in range(1, num_c + 1):
        cid = f"C-{i:02d}"
        competencies.append({
            "id": cid,
            "code": cid,
            "competency_id": cid,
            "name": f"Concepto Teórico #{i}",
            "description": f"Descripción completa del concepto teórico #{i} para validación psicométrica.",
            "category": "Concept",
            "type": "Concept",
            "level": "Understand",
            "mastery_target": 100,
            "distractors": [{"id": f"D-{cid.replace('-', '')}-{d:02d}", "name": f"D{d}"} for d in range(1, 7)],
        })
        for q_idx in range(1, 4):
            qid = f"Q-{cid.replace('-', '')}-{q_idx:02d}"
            questions.append(_make_mock_question(
                qid=qid,
                cid=cid,
                level="Understand",
                stem=f"Considere el modelo teórico fundamental en el reactivo {qid}. ¿Cuál es la propiedad de {cid}?",
                answer="Opción teórica correcta del modelo de equilibrio",
            ))

    # Skills: Hab-01 .. Hab-NN
    for i in range(1, num_hab + 1):
        cid = f"Hab-{i:02d}"
        competencies.append({
            "id": cid,
            "code": cid,
            "competency_id": cid,
            "name": f"Habilidad Práctica #{i}",
            "description": f"Descripción completa de la habilidad práctica #{i} para validación psicométrica.",
            "category": "Skill",
            "type": "Skill",
            "level": "Apply",
            "mastery_target": 100,
            "distractors": [{"id": f"D-{cid.replace('-', '')}-{d:02d}", "name": f"D{d}"} for d in range(1, 7)],
        })
        for q_idx in range(1, 4):
            qid = f"Q-{cid.replace('-', '')}-{q_idx:02d}"
            questions.append(_make_mock_question(
                qid=qid,
                cid=cid,
                level="Apply",
                stem=f"Considere el ejercicio práctico en el reactivo {qid}. ¿Cómo se aplica la regla de {cid}?",
                answer="Resultado del procedimiento algorítmico y derivación práctica",
            ))

    # Facts: H-01 .. H-NN
    for i in range(1, num_h + 1):
        cid = f"H-{i:02d}"
        competencies.append({
            "id": cid,
            "code": cid,
            "competency_id": cid,
            "name": f"Hecho Empírico #{i}",
            "description": f"Descripción completa del hecho empírico #{i} para validación psicométrica.",
            "category": "Fact",
            "type": "Fact",
            "level": "Remember",
            "mastery_target": 100,
            "distractors": [{"id": f"D-{cid.replace('-', '')}-{d:02d}", "name": f"D{d}"} for d in range(1, 7)],
        })
        for q_idx in range(1, 4):
            qid = f"Q-{cid.replace('-', '')}-{q_idx:02d}"
            questions.append(_make_mock_question(
                qid=qid,
                cid=cid,
                level="Remember",
                stem=f"Considere la evidencia empírica en el reactivo {qid}. ¿Cuál es el hecho estilizado en {cid}?",
                answer="Constatación empírica demostrada en series históricas de datos",
            ))

    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "schema_version": "1.0.0",
        "course_id": course_id,
        "course_title": title,
        "title": title,
        "description": f"Curso completo de {title} con validación psicométrica estricta.",
        "language": "es",
        "created_at": "2026-10-19T00:00:00Z",
        "competencies": competencies,
        "questions": questions,
    }


class TestPrepareAppendDeltaWorkflow:
    """Tests prepare --append delta injection and continuous sequential ID assignment."""

    def test_compute_next_ids_with_solow_baseline_21(self) -> None:
        """Verifies compute_next_ids on a 21-competency course (10 Concept, 6 Skill, 5 Fact)."""
        base_course = _create_mock_course("solow_model", "Modelo de Solow", num_c=10, num_hab=6, num_h=5)
        assert len(base_course["competencies"]) == 21

        next_ids = compute_next_ids(base_course["competencies"])
        assert next_ids["max_numbers_by_prefix"]["C-"] == 10
        assert next_ids["max_numbers_by_prefix"]["Hab-"] == 6
        assert next_ids["max_numbers_by_prefix"]["H-"] == 5

        # Continuous non-overlapping sequence starts at:
        assert next_ids["next_ids_by_prefix"]["C-"] == "C-11"
        assert next_ids["next_ids_by_prefix"]["Hab-"] == "Hab-07"
        assert next_ids["next_ids_by_prefix"]["H-"] == "H-06"
        assert next_ids["next_competency_index"] == 22

    def test_prepare_append_delta_injection_solow_21_to_45(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """End-to-end regression: prepare --append injects delta metadata and publishes Solow 21 -> 45 cleanly."""
        monkeypatch.chdir(tmp_path)
        courses_dir = tmp_path / "courses"
        courses_dir.mkdir(parents=True)

        # 1. Base course: 21 competencies (10 C, 6 Hab, 5 H), 63 questions
        base_course = _create_mock_course("solow_model", "Modelo de Crecimiento de Solow", num_c=10, num_hab=6, num_h=5)
        base_json_file = courses_dir / "solow_model.json"
        base_json_file.write_text(json.dumps(base_course, indent=2, ensure_ascii=False), encoding="utf-8")

        # 2. Genuine multi-page PDF using pymupdf
        pdf_file = tmp_path / "content" / "solow_append.pdf"
        _create_dummy_pdf(pdf_file, num_pages=5)

        work_append = tmp_path / "courses" / "solow_model" / "work_append"

        # 3. Execute prepare_course in append mode
        manifest = prepare_course(
            input_path=pdf_file,
            work_dir=work_append,
            course_id="solow_model",
            courses_dir=courses_dir,
            append=True,
            title="Modelo de Crecimiento de Solow",
        )

        assert manifest["append_mode"] is True
        assert "delta" in manifest
        delta = manifest["delta"]
        assert delta["total_existing_competencies"] == 21
        assert delta["total_existing_questions"] == 63
        assert delta["next_ids_by_prefix"]["C-"] == "C-11"
        assert delta["next_ids_by_prefix"]["Hab-"] == "Hab-07"
        assert delta["next_ids_by_prefix"]["H-"] == "H-06"
        assert len(delta["existing_competency_ids"]) == 21

        # Check pre_cta_manifest.json on disk has delta info
        saved_manifest = json.loads((work_append / "pre_cta_manifest.json").read_text(encoding="utf-8"))
        assert saved_manifest["append_mode"] is True
        assert saved_manifest["delta"]["next_ids_by_prefix"]["C-"] == "C-11"

        # Check dedicated delta_manifest.json exists
        delta_file = work_append / "delta_manifest.json"
        assert delta_file.is_file()

        # 4. Generate 24 new delta competencies starting from the continuous next_ids:
        # 12 concepts: C-11 .. C-22
        # 6 skills: Hab-07 .. Hab-12
        # 6 facts: H-06 .. H-11
        # Total new = 24. Final total = 21 + 24 = 45!
        delta_comps = []
        delta_questions = []

        for i in range(11, 23):  # 12 concepts: C-11 to C-22
            cid = f"C-{i:02d}"
            delta_comps.append({
                "id": cid,
                "code": cid,
                "competency_id": cid,
                "name": f"Modelo Solow Delta Concepto #{i}",
                "description": f"Descripción completa del concepto delta #{i} para validación psicométrica.",
                "category": "Concept",
                "type": "Concept",
                "level": "Analyze",
                "mastery_target": 100,
                "distractors": [{"id": f"D-{cid.replace('-', '')}-{d:02d}", "name": f"D{d}"} for d in range(1, 7)],
            })
            for q_idx in range(1, 4):
                qid = f"Q-{cid.replace('-', '')}-{q_idx:02d}"
                delta_questions.append(_make_mock_question(
                    qid=qid,
                    cid=cid,
                    level="Analyze",
                    stem=f"Considere el modelo delta en el reactivo {qid}. ¿Cuál es la implicancia de {cid}?",
                    answer="Respuesta Delta teórica del modelo de crecimiento continuo",
                ))

        for i in range(7, 13):  # 6 skills: Hab-07 to Hab-12
            cid = f"Hab-{i:02d}"
            delta_comps.append({
                "id": cid,
                "code": cid,
                "competency_id": cid,
                "name": f"Modelo Solow Delta Habilidad #{i}",
                "description": f"Descripción completa de la habilidad delta #{i} para validación psicométrica.",
                "category": "Skill",
                "type": "Skill",
                "level": "Evaluate",
                "mastery_target": 100,
                "distractors": [{"id": f"D-{cid.replace('-', '')}-{d:02d}", "name": f"D{d}"} for d in range(1, 7)],
            })
            for q_idx in range(1, 4):
                qid = f"Q-{cid.replace('-', '')}-{q_idx:02d}"
                delta_questions.append(_make_mock_question(
                    qid=qid,
                    cid=cid,
                    level="Evaluate",
                    stem=f"Considere el procedimiento delta en el reactivo {qid}. ¿Cómo se evalúa {cid}?",
                    answer="Respuesta Delta analítica de cálculo diferencial avanzado",
                ))

        for i in range(6, 12):  # 6 facts: H-06 to H-11
            cid = f"H-{i:02d}"
            delta_comps.append({
                "id": cid,
                "code": cid,
                "competency_id": cid,
                "name": f"Modelo Solow Delta Hecho #{i}",
                "description": f"Descripción completa del hecho empírico delta #{i} para validación psicométrica.",
                "category": "Fact",
                "type": "Fact",
                "level": "Remember",
                "mastery_target": 100,
                "distractors": [{"id": f"D-{cid.replace('-', '')}-{d:02d}", "name": f"D{d}"} for d in range(1, 7)],
            })
            for q_idx in range(1, 4):
                qid = f"Q-{cid.replace('-', '')}-{q_idx:02d}"
                delta_questions.append(_make_mock_question(
                    qid=qid,
                    cid=cid,
                    level="Remember",
                    stem=f"Considere la observación empírica delta en el reactivo {qid}. ¿Cuál es la constatación de {cid}?",
                    answer="Respuesta Delta de regularidad empírica macroeconómica",
                ))

        assert len(delta_comps) == 24
        assert len(delta_questions) == 72

        delta_batch = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "schema_version": "1.0.0",
            "course_id": "solow_model",
            "course_title": "Modelo de Crecimiento de Solow",
            "description": "Curso completo de Modelo de Crecimiento de Solow con validación psicométrica estricta.",
            "language": "es",
            "created_at": "2026-10-19T00:00:00Z",
            "competencies": delta_comps,
            "questions": delta_questions,
        }

        # 5. Publish with CoursePublisher in append mode
        publisher = CoursePublisher(courses_dir=courses_dir)
        publisher._run_cli_validator = lambda p, strict=True: True  # bypass external subprocess
        monkeypatch.setattr(
            "course_publisher.validate_course_content",
            lambda raw, file_path=None, strict=False: ValidationResult(is_valid=True, file_path=file_path, errors=[]),
        )

        pub_result = publisher.publish(delta_batch, append=True, strict=False)
        assert pub_result.success is True, f"Publish error: {pub_result.error_message}"
        assert pub_result.total_competencies == 45  # 21 base + 24 delta
        assert pub_result.total_questions == 63 + 72  # 135 total questions

        # Verify disk persistence
        merged_on_disk = json.loads(base_json_file.read_text(encoding="utf-8"))
        final_ids = [c["id"] for c in merged_on_disk["competencies"]]
        assert len(final_ids) == 45
        assert len(set(final_ids)) == 45
        # Confirm C-01..C-22, Hab-01..Hab-12, H-01..H-11 are all present
        for i in range(1, 23):
            assert f"C-{i:02d}" in final_ids
        for i in range(1, 13):
            assert f"Hab-{i:02d}" in final_ids
        for i in range(1, 12):
            assert f"H-{i:02d}" in final_ids

    def test_course_publisher_warned_fallback_remap_when_unaware_of_delta(self, tmp_path: Path, caplog: pytest.LogCaptureFixture, monkeypatch: pytest.MonkeyPatch) -> None:
        """When an append batch arrives with colliding legacy IDs (e.g. C-01 with new name),
        CoursePublisher must log a warning and remap as a warned fallback.
        """
        courses_dir = tmp_path / "courses"
        courses_dir.mkdir(parents=True)

        base_course = _create_mock_course("solow_model", "Modelo de Solow", num_c=5, num_hab=2, num_h=2)
        base_json = courses_dir / "solow_model.json"
        base_json.write_text(json.dumps(base_course, indent=2), encoding="utf-8")

        # Create colliding batch restarting at C-01 with different name
        colliding_comp = {
            "id": "C-01",
            "code": "C-01",
            "competency_id": "C-01",
            "name": "Completamente Distinto Concepto Delta",
            "description": "Descripción completa de competencia distinta para probar colisión y fallback remap.",
            "category": "Concept",
            "type": "Concept",
            "level": "Analyze",
            "mastery_target": 100,
            "distractors": [{"id": "D-C01-01", "name": "Dist 1"}],
        }
        colliding_batch = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "schema_version": "1.0.0",
            "course_id": "solow_model",
            "course_title": "Modelo de Solow",
            "description": "Curso con colisión.",
            "language": "es",
            "created_at": "2026-10-19T00:00:00Z",
            "competencies": [colliding_comp],
            "questions": [_make_mock_question(
                qid="Q-C01-99",
                cid="C-01",
                level="Analyze",
                stem="Nueva pregunta sobre concepto delta con longitud suficiente para superar el esquema.",
                answer="Opción A correcta con longitud adecuada.",
            )],
        }

        publisher = CoursePublisher(courses_dir=courses_dir)
        publisher._run_cli_validator = lambda p, strict=True: True
        monkeypatch.setattr(
            "course_publisher.validate_course_content",
            lambda raw, file_path=None, strict=False: ValidationResult(is_valid=True, file_path=file_path, errors=[]),
        )

        with caplog.at_level(logging.WARNING):
            result = publisher.publish(colliding_batch, append=True, strict=False)

        assert result.success is True, f"Publication failed: {result.error_message}"
        # Verify fallback remap warning was logged
        assert any("FALLBACK REMAP" in record.message for record in caplog.records)

        merged = json.loads(base_json.read_text(encoding="utf-8"))
        merged_ids = [c["id"] for c in merged["competencies"]]
        # Original C-01 is preserved, and colliding comp is remapped to C-06
        assert "C-01" in merged_ids
        assert "C-06" in merged_ids
        assert len(merged["competencies"]) == len(base_course["competencies"]) + 1


class TestMangledUnicodeTitleFallback:
    """Tests resilience against corrupted Unicode characters (\ufffd) in CLI --title."""

    def test_is_corrupted_unicode(self) -> None:
        assert is_corrupted_unicode("Estad\ufffdstica: Regresi\ufffdn") is True
        assert is_corrupted_unicode("Macroeconom\uFFFD a") is True
        assert is_corrupted_unicode("Estadística: Regresión") is False
        assert is_corrupted_unicode(None) is False
        assert is_corrupted_unicode("") is False

    def test_pipeline_runner_mangled_title_fallback_to_cta_json(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """PipelineRunner falls back to clean title in cta.json when --title contains \\ufffd."""
        monkeypatch.chdir(tmp_path)
        work_dir = tmp_path / "courses" / "stats_course" / "work"
        work_dir.mkdir(parents=True)

        cta_data = {
            "course_id": "stats_course",
            "title": "Estadística: Regresión y Correlación",
            "competencies": [],
        }
        (work_dir / "cta.json").write_text(json.dumps(cta_data, ensure_ascii=False), encoding="utf-8")

        # Pass corrupted title from PowerShell
        mangled_title = "Estad\ufffdstica: Regresi\ufffdn y Correlaci\ufffdn"
        runner = PipelineRunner(
            course_id="stats_course",
            title=mangled_title,
            work_dir=work_dir,
            output_dir=tmp_path / "courses",
        )

        assert runner.title == "Estadística: Regresión y Correlación"
        assert not is_corrupted_unicode(runner.title)

    def test_prepare_course_mangled_title_fallback_to_existing_course(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """prepare_course recovers clean title from existing course JSON in append mode."""
        monkeypatch.chdir(tmp_path)
        courses_dir = tmp_path / "courses"
        courses_dir.mkdir(parents=True)

        base_course = _create_mock_course("macro_solow", "Macroeconomía: Crecimiento y Dinámica")
        (courses_dir / "macro_solow.json").write_text(json.dumps(base_course, ensure_ascii=False), encoding="utf-8")

        pdf_file = tmp_path / "content" / "dummy.pdf"
        _create_dummy_pdf(pdf_file, num_pages=2)

        work_dir = tmp_path / "courses" / "macro_solow" / "work_append"

        manifest = prepare_course(
            input_path=pdf_file,
            work_dir=work_dir,
            course_id="macro_solow",
            courses_dir=courses_dir,
            append=True,
            title="Macroeconom\ufffda: Crecimiento y Din\ufffdmica",
        )

        assert manifest.get("course_title") == "Macroeconomía: Crecimiento y Dinámica"
        assert not is_corrupted_unicode(manifest.get("course_title"))

    def test_course_publisher_mangled_title_fallback(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """CoursePublisher recovers clean title from existing course if parsed course_title is mangled."""
        courses_dir = tmp_path / "courses"
        courses_dir.mkdir(parents=True)

        base_course = _create_mock_course("eco_101", "Economía Abierta y Balanza de Pagos")
        (courses_dir / "eco_101.json").write_text(json.dumps(base_course, ensure_ascii=False), encoding="utf-8")

        # Incoming batch with corrupted title but valid schema fields
        incoming = copy.deepcopy(base_course)
        incoming["course_title"] = "Econom\ufffda Abierta y Balanza de Pagos"
        incoming["title"] = "Econom\ufffda Abierta y Balanza de Pagos"

        publisher = CoursePublisher(courses_dir=courses_dir)
        publisher._run_cli_validator = lambda p, strict=True: True
        monkeypatch.setattr(
            "course_publisher.validate_course_content",
            lambda raw, file_path=None, strict=False: ValidationResult(is_valid=True, file_path=file_path, errors=[]),
        )

        res = publisher.publish(incoming, append=True, strict=False)
        assert res.success is True, f"Publish error: {res.error_message}"
        assert res.course_title == "Economía Abierta y Balanza de Pagos"
        assert not is_corrupted_unicode(res.course_title)


class TestWindowsPathEscapingResilience:
    """Tests handling of Windows shells (PowerShell/cmd) quote-wrapping and backslash anomalies."""

    def test_sanitize_cli_arg_varieties(self) -> None:
        # Standard double-quoted string
        assert sanitize_cli_arg('"d:\\Augusto\\courses\\solow"') == "d:\\Augusto\\courses\\solow"
        # Escaped nested quotes like \"path\"
        assert sanitize_cli_arg(r'\"d:\Augusto\courses\solow\"') == "d:\\Augusto\\courses\\solow"
        # Double escaped nested quotes
        assert sanitize_cli_arg('"\\"C:\\My Folder\\course\\""') == "C:\\My Folder\\course"
        # Single-quoted string
        assert sanitize_cli_arg("'courses/solow/work'") == "courses/solow/work"
        # Stray trailing backslash (except drive root)
        assert sanitize_cli_arg("courses/solow/work\\") == "courses/solow/work"
        # Drive root preserved
        assert sanitize_cli_arg("C:\\") == "C:\\"

    def test_sanitize_path_returns_clean_path(self) -> None:
        p1 = sanitize_path(r'\"D:\Augusto\Courses\solow\"')
        assert p1 == Path("D:/Augusto/Courses/solow")

        p2 = sanitize_path('"courses/solow/work"')
        assert p2 == Path("courses/solow/work")

        assert sanitize_path(None) is None

    def test_pipeline_runner_initialization_with_quoted_cli_arguments(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Verifies PipelineRunner handles Windows quote-wrapped arguments without throwing WinError 123."""
        monkeypatch.chdir(tmp_path)
        quoted_work = f'"{tmp_path / "quoted_work"}"'
        quoted_cid = '"solow_quoted"'
        quoted_title = '"Curso Solow Quoted"'

        runner = PipelineRunner(
            course_id=quoted_cid,
            title=quoted_title,
            work_dir=quoted_work,
            output_dir=f'"{tmp_path / "courses"}"',
        )

        assert runner.course_id == "solow_quoted"
        assert runner.title == "Curso Solow Quoted"
        assert runner.work_dir.is_dir()
        assert not str(runner.work_dir).startswith('"')
        assert not str(runner.work_dir).endswith('"')
