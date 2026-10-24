"""Dry-run tests for C2C v3.21 Multi-Instance Zero-Collision Isolation (solow_01..10)
and End-to-End Incremental --append Mode (Competency/Distractor ID Remapping, Units, Questions & CTA Markdown).
"""

from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict

import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT_DIR / ".agents" / "skills" / "content-to-course"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))
if str(ROOT_DIR / "src") not in sys.path:
    sys.path.insert(0, str(ROOT_DIR / "src"))

from check_templates import check_templates_file_or_dir
from course_publisher import CoursePublisher
from dispatch import dispatch_cta
from run import PipelineRunner

FIXTURES_DIR = (
    (ROOT_DIR / "courses" / "fixtures")
    if (ROOT_DIR / "courses" / "fixtures").exists()
    else (ROOT_DIR / "tests" / "validator" / "fixtures")
)


class TestMultiInstanceZeroCollisionDryRun:
    """Dry-run tests verifying that 10 concurrent Solow instances (solow_01..solow_10) never collide."""

    def test_10_solow_instances_isolated_work_dirs_and_dispatch_paths(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)
        content_dir = tmp_path / "content" / "solow"
        content_dir.mkdir(parents=True)
        pdf_1 = content_dir / "solow_part1.pdf"
        pdf_2 = content_dir / "solow_part2.pdf"
        pdf_1.write_bytes(b"%PDF-1.4 dummy 1")
        pdf_2.write_bytes(b"%PDF-1.4 dummy 2")

        work_dirs = set()
        for i in range(1, 11):
            cid = f"solow_{i:02d}"
            runner = PipelineRunner(
                pdf=[pdf_1, pdf_2],
                course_id=cid,
                output_dir=tmp_path / "courses",
            )
            assert runner.course_id == cid
            expected_work = Path("courses") / cid / "work"
            assert runner.work_dir == expected_work
            work_dirs.add(runner.work_dir.resolve())

            manifest_data = {
                "course_id": cid,
                "cta_mode": "direct",
                "granularity": "standard",
                "total_pages": 20,
                "documents": [
                    {"doc_name": "solow_part1.pdf", "path": "content/solow/solow_part1.pdf", "valid_page_range": [1, 10], "total_pages": 10},
                    {"doc_name": "solow_part2.pdf", "path": "content/solow/solow_part2.pdf", "valid_page_range": [1, 10], "total_pages": 10},
                ],
            }
            (runner.work_dir / "pre_cta_manifest.json").write_text(json.dumps(manifest_data), encoding="utf-8")

            cta_res = dispatch_cta(runner.work_dir, pointer=False)
            cta_prompt = cta_res["Subagents"][0]["Prompt"]
            assert f"courses/{cid}/work/cta_data.py" in cta_prompt
            assert f"courses/{cid}/work/cta.json" in cta_prompt
            assert "--input courses/" in cta_prompt

            for other_i in range(1, 11):
                if other_i != i:
                    assert f"solow_{other_i:02d}" not in cta_prompt

        assert len(work_dirs) == 10

    def test_compile_cta_cli_input_output_flags_isolated_per_instance(self, tmp_path: Path) -> None:
        """Verifies compile_cta.py --input <path> --output <path> --manifest <path> writes strictly to the target instance."""
        inst_work = tmp_path / "courses" / "solow_07" / "work"
        inst_work.mkdir(parents=True)

        manifest = {
            "files": [{"doc": "solow.pdf", "total_pages": 15, "valid_page_range": [1, 15]}],
        }
        manifest_file = inst_work / "pre_cta_manifest.json"
        manifest_file.write_text(json.dumps(manifest), encoding="utf-8")

        cta_py = inst_work / "cta_data.py"
        cta_py.write_text(
            'COURSE_ID = "solow_07"\n'
            'TITLE = "Modelo de Solow 07"\n\n'
            'COMPETENCIES = [\n'
            '    (\n'
            '        "Concept",\n'
            '        "C-01",\n'
            '        "Diferencial con \\rho y \\left( \\frac{a}{b} \\right) y \\rightarrow",\n'
            '        "Relación fundamental: $\\alpha + \\beta = \\bar{k}$ evaluada con \\tau y \\theta.",\n'
            '        "Understand",\n'
            '        "solow.pdf",\n'
            '        1,\n'
            '        [],\n'
            '        [\n'
            '            ("D-01-01", "Asume que \\text{diff} es nulo", "Diferencia es no nula", "$0$", "Revisar \\times y \\nu.", None),\n'
            '            ("D-01-02", "Cree que \\neq implica divergencia", "No implica divergencia", "$0$", "Operador \\nabla no converge", None),\n'
            '            ("D-01-03", "Aproxima vector \\vec{x} sin \\varepsilon", "Vector y perturbación válidos", "$0$", "Verificar marco estocástico", None),\n'
            '            ("D-01-04", "Omite ajuste dinámico", "Ajuste dinámico requerido", "$0$", "Revisar ecuación de balance", "Omite derivación temporal"),\n'
            '            ("D-01-05", "Confunde tasas de crecimiento", "Tasas bien definidas", "$0$", "Revisar parágrafo teórico", "Omite sustitución"),\n'
            '            ("D-01-06", "Error en condición terminal", "Condición transversal requerida", "$0$", "Verificar límite infinito", None),\n'
            '        ],\n'
            '    ),\n'
            ']\n',
            encoding="utf-8",
        )

        out_json = inst_work / "cta.json"
        cmd = [
            sys.executable,
            str(SKILL_DIR / "compile_cta.py"),
            "--input",
            str(cta_py),
            "--output",
            str(out_json),
            "--manifest",
            str(manifest_file),
        ]
        proc = subprocess.run(cmd, cwd=str(tmp_path), capture_output=True, text=True)
        assert proc.returncode == 0, f"compile_cta CLI failed: {proc.stderr}"
        assert out_json.is_file()
        assert not (tmp_path / "work" / "cta.json").exists()

    def test_check_templates_isolates_check_attempts_inside_instance_work_dir(self, tmp_path: Path) -> None:
        """Verifies .check_attempts is created inside courses/<id>/work/.check_attempts, never shared."""
        inst_work = tmp_path / "courses" / "solow_03" / "work"
        tpl_dir = inst_work / "templates"
        shards_dir = inst_work / "shards"
        tpl_dir.mkdir(parents=True)
        shards_dir.mkdir(parents=True)

        dummy_shard_py = shards_dir / "shard_01_data.py"
        dummy_shard_py.write_text("TEMPLATES = []\n", encoding="utf-8")
        bad_tpl = tpl_dir / "C-01.json"
        bad_tpl.write_text(json.dumps({"competency_id": "C-01", "templates": []}), encoding="utf-8")

        check_templates_file_or_dir(
            target_path=[bad_tpl],
            cta_path=None,
            num_dry_run_seeds=5,
            strict=False,
            shard_py=dummy_shard_py,
            shard_id="shard_01",
        )
        assert (inst_work / ".check_attempts").is_dir()
        assert not (tmp_path / "work" / ".check_attempts").exists()


class TestAppendModeDryRun:
    """Dry-run tests for --append mode: work_append isolation, ID collision remapping, units & CTA markdown merge."""

    def test_pipeline_runner_append_flag_uses_work_append_and_cleans_stale_prepare(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)
        orig_runner = PipelineRunner(course_id="solow_model")
        assert orig_runner.work_dir == Path("courses/solow_model/work")
        orig_marker = orig_runner.work_dir / "cta.json"
        orig_marker.write_text('{"course_id": "solow_model"}', encoding="utf-8")

        append_runner = PipelineRunner(course_id="solow_model", append=True)
        assert append_runner.work_dir == Path("courses/solow_model/work_append")
        assert orig_marker.is_file()

    def test_course_publisher_append_remaps_colliding_competencies_distractors_questions_and_cta_md(self, tmp_path: Path) -> None:
        courses_dir = tmp_path / "courses"
        courses_dir.mkdir(parents=True)
        publisher = CoursePublisher(courses_dir=courses_dir)
        publisher._run_cli_validator = lambda json_path, strict=False: True  # type: ignore[assignment]

        valid_fixture = json.loads((FIXTURES_DIR / "28_valid_complete_course.json").read_text(encoding="utf-8"))

        # 1. Publish Initial Base Course from valid fixture
        base_course = copy.deepcopy(valid_fixture)
        base_course["course_id"] = "solow_incremental"
        base_course["course_title"] = "Modelo de Crecimiento de Solow"
        base_course["units"] = [{"id": "U-01", "name": "Unidad 1: Acumulación Básica de Capital"}]
        for idx, d in enumerate(base_course["competencies"][0].setdefault("distractors", []), 1):
            d["id"] = f"D-C01-0{idx}"
        if not base_course["competencies"][0].get("distractors"):
            base_course["competencies"][0]["distractors"] = [{"id": f"D-C01-0{i}", "name": f"Arquetipo base {i}"} for i in range(1, 7)]

        orig_comp_count = len(base_course["competencies"])
        orig_q_count = len(base_course["questions"])
        first_cid = base_course["competencies"][0]["id"]  # e.g. "Hab-01" or "C-01"
        first_cname = base_course["competencies"][0].get("name") or base_course["competencies"][0].get("title") or "Base Comp"

        base_cta_md = f"# Análisis de Competencias: Solow\n\n- **{first_cid}**: {first_cname} (`D-C01-01`)\n"

        res1 = publisher.publish(
            course_data=base_course,
            output_dir=courses_dir,
            strict=False,
            cta_markdown=base_cta_md,
            append=False,
        )
        assert res1.success, f"Initial publish failed: {res1.error_message}"
        assert res1.total_competencies == orig_comp_count
        assert res1.total_questions == orig_q_count

        # 2. Build Incremental Batch with colliding competency IDs (same IDs as base_course, but NEW names and NEW questions!)
        append_batch = copy.deepcopy(valid_fixture)
        append_batch["course_id"] = "solow_incremental"
        append_batch["course_title"] = "Modelo de Crecimiento de Solow"
        append_batch["units"] = [{"id": "U-02", "name": "Unidad 2: Regla de Oro y Progreso Tecnológico"}]

        for idx, c in enumerate(append_batch["competencies"], 1):
            c["name"] = f"Regla de Oro de Phelps Parte {idx}"
            c["title"] = f"Regla de Oro de Phelps Parte {idx}"
            c["distractors"] = [{"id": f"D-01-0{i}", "name": f"Arquetipo Phelps {i}"} for i in range(1, 7)]

        for idx, q in enumerate(append_batch["questions"], 1):
            q["stem"] = f"[Nuevo Módulo Phelps #{idx}] {q['stem']}"

        append_cta_md = f"### Nuevas Competencias\n- **{first_cid}**: Regla de Oro de Phelps Parte 1 (`D-01-01`)\n"

        res2 = publisher.publish(
            course_data=append_batch,
            output_dir=courses_dir,
            strict=False,
            cta_markdown=append_cta_md,
            append=True,
        )
        assert res2.success, f"Append publish failed: {res2.error_message}"
        assert res2.total_competencies == orig_comp_count * 2
        assert res2.total_questions == orig_q_count * 2

        merged_json = json.loads((courses_dir / "solow_incremental.json").read_text(encoding="utf-8"))
        comp_ids = [c["id"] for c in merged_json["competencies"]]
        assert len(set(comp_ids)) == orig_comp_count * 2, f"Competency IDs were not uniquely remapped: {comp_ids}"

        # Verify units were merged cleanly
        unit_names = [u["name"] for u in merged_json.get("units", [])]
        assert "Unidad 1: Acumulación Básica de Capital" in unit_names
        assert "Unidad 2: Regla de Oro y Progreso Tecnológico" in unit_names

        # Verify CTA Markdown appended and remapped first_cid -> new_cid
        remapped_first_cid = comp_ids[orig_comp_count]
        assert remapped_first_cid != first_cid
        merged_md = (courses_dir / "competence_analysis_solow_incremental.md").read_text(encoding="utf-8")
        assert "## Actualización Incremental (Append)" in merged_md
        assert f"- **{remapped_first_cid}**: Regla de Oro de Phelps Parte 1" in merged_md

        # 3. Append to EXISTING competency (exact same name as base_course[0]) + 1 duplicate question + 1 new question
        same_comp_batch = copy.deepcopy(base_course)
        same_comp_batch["competencies"] = [copy.deepcopy(base_course["competencies"][0])]
        dup_q = copy.deepcopy(base_course["questions"][0])
        new_q = copy.deepcopy(base_course["questions"][0])
        new_q["id"] = "Q-NEW-999"
        new_q["stem"] = f"[Pregunta Extra de Refuerzo] {new_q['stem']}"
        same_comp_batch["questions"] = [dup_q, new_q]

        res3 = publisher.publish(
            course_data=same_comp_batch,
            output_dir=courses_dir,
            strict=False,
            append=True,
        )
        assert res3.success, f"Same-competency append failed: {res3.error_message}"
        assert res3.total_competencies == orig_comp_count * 2  # No duplicate competency added
        assert res3.total_questions == (orig_q_count * 2) + 1  # Only 1 new question added (duplicate skipped)
