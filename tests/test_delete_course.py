"""Automated test suite for the delete-course skill and deletion engine."""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

SKILL_SCRIPTS_DIR = REPO_ROOT / ".agents" / "skills" / "delete-course" / "scripts"
if str(SKILL_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_SCRIPTS_DIR))

from delete_course import (
    SecurityError,
    assert_path_safe,
    clean_orphan_course_dirs,
    delete_course,
    find_course_artifacts,
    stamp_individual_audit_json,
    stamp_individual_audit_md,
    stamp_suite_audit_table,
)
import run_platform


class TestSecurityInvariants:
    """Verifies that the content/ and fixtures directories are strictly immutable."""

    def test_content_dir_is_strictly_immutable(self):
        content_path = REPO_ROOT / "content" / "sample.pdf"
        with pytest.raises(SecurityError) as exc_info:
            assert_path_safe(content_path)
        assert "inmutable" in str(exc_info.value).lower()

    def test_contents_alias_is_strictly_immutable(self):
        contents_path = REPO_ROOT / "contents" / "nested" / "lecture.pdf"
        with pytest.raises(SecurityError) as exc_info:
            assert_path_safe(contents_path)
        assert "inmutable" in str(exc_info.value).lower()

    def test_fixtures_protected(self):
        fixtures_path = REPO_ROOT / "courses" / "fixtures" / "01_original_example_unmodified.json"
        with pytest.raises(SecurityError) as exc_info:
            assert_path_safe(fixtures_path)
        assert "fixtures" in str(exc_info.value).lower()

    def test_path_escape_blocked(self):
        escape_path = REPO_ROOT / ".." / "external_system_file.txt"
        with pytest.raises(SecurityError):
            assert_path_safe(escape_path)


class TestDeletionEngineOperations:
    """Verifies dry-run, real deletion, archive mode, and audit report stamping."""

    @pytest.fixture
    def dummy_course_setup(self):
        cid = "unit_test_dummy_course_99"
        json_path = REPO_ROOT / "courses" / f"{cid}.json"
        cta_path = REPO_ROOT / "courses" / f"competence_analysis_{cid}.md"
        dir_path = REPO_ROOT / "courses" / cid
        report_json = REPO_ROOT / "reports" / "qa_audits" / f"{cid}_qa_report.json"
        report_md = REPO_ROOT / "reports" / "qa_audits" / f"{cid}_qa_report.md"

        # Create dummy course
        dummy_data = {
            "course_id": cid,
            "title": "Curso Dummy de Prueba Unitaria",
            "competencies": [{"id": "C-01", "name": "Dummy Comp"}],
            "questions": [{
                "id": "Q-01",
                "type": "multiple_choice_7_options",
                "stem": "Dummy question?",
                "options": ["A", "B", "C", "D", "E", "F", "G"],
                "correct_answer": "A"
            }],
        }
        json_path.write_text(json.dumps(dummy_data), encoding="utf-8")
        cta_path.write_text("# Dummy CTA", encoding="utf-8")
        dir_path.mkdir(parents=True, exist_ok=True)
        (dir_path / "dummy_work.txt").write_text("intermediate work", encoding="utf-8")

        # Create dummy QA reports
        report_json.parent.mkdir(parents=True, exist_ok=True)
        report_json.write_text(json.dumps({
            "course_metadata": {"course_id": cid, "unit_title": "Curso Dummy"},
            "final_score": 18.0,
            "quality_tier": "EXCELENTE"
        }), encoding="utf-8")
        report_md.write_text(f"# Informe de Auditoría\n\n**Curso:** Curso Dummy (`{cid}`)\n", encoding="utf-8")

        yield {
            "cid": cid,
            "json_path": json_path,
            "cta_path": cta_path,
            "dir_path": dir_path,
            "report_json": report_json,
            "report_md": report_md,
        }

        # Cleanup in case test failed before engine deleted them
        json_path.unlink(missing_ok=True)
        cta_path.unlink(missing_ok=True)
        if dir_path.is_dir():
            shutil.rmtree(dir_path, ignore_errors=True)
        report_json.unlink(missing_ok=True)
        report_md.unlink(missing_ok=True)

    def test_dry_run_preserves_files(self, dummy_course_setup):
        cid = dummy_course_setup["cid"]
        res = delete_course(cid, dry_run=True)
        assert res["success"] is True
        assert res["dry_run"] is True

        # Ensure files still exist on disk
        assert dummy_course_setup["json_path"].is_file()
        assert dummy_course_setup["cta_path"].is_file()
        assert dummy_course_setup["dir_path"].is_dir()
        assert dummy_course_setup["report_json"].is_file()

    def test_real_deletion_removes_from_platform_and_stamps_audit(self, dummy_course_setup):
        cid = dummy_course_setup["cid"]
        
        # Verify course is initially visible in platform scan
        initial_scan = run_platform.scan_courses()
        assert any(c["id"] == cid for c in initial_scan)

        # Execute real deletion
        res = delete_course(cid, dry_run=False)
        assert res["success"] is True
        assert res["dry_run"] is False

        # Verify platform files and directory are GONE
        assert not dummy_course_setup["json_path"].exists()
        assert not dummy_course_setup["cta_path"].exists()
        assert not dummy_course_setup["dir_path"].exists()

        # Verify course is NO LONGER discovered by platform
        post_scan = run_platform.scan_courses()
        assert not any(c["id"] == cid for c in post_scan)

        # Verify QA audit reports are PRESERVED (NOT deleted)
        assert dummy_course_setup["report_json"].is_file()
        assert dummy_course_setup["report_md"].is_file()

        # Verify audit JSON content is stamped with ELIMINADO
        stamped_data = json.loads(dummy_course_setup["report_json"].read_text(encoding="utf-8"))
        assert stamped_data.get("platform_status") == "ELIMINADO"
        assert "deleted_at" in stamped_data
        assert stamped_data.get("course_metadata", {}).get("platform_status") == "ELIMINADO"

        # Verify audit MD content has deletion date and warning banner
        stamped_md = dummy_course_setup["report_md"].read_text(encoding="utf-8")
        assert "CURSO RETIRADO DE LA PLATAFORMA" in stamped_md
        assert "**Estado en Plataforma:** ELIMINADO" in stamped_md
        assert "**Fecha de Eliminación:**" in stamped_md

    def test_clean_orphan_dirs(self):
        orphan_dir = REPO_ROOT / "courses" / "temp_orphan_dir_unit_test"
        orphan_dir.mkdir(parents=True, exist_ok=True)
        (orphan_dir / "temp.txt").write_text("hello", encoding="utf-8")

        assert orphan_dir.is_dir()
        cleaned = clean_orphan_course_dirs(dry_run=False)
        assert str(orphan_dir) in cleaned
        assert not orphan_dir.exists()

        # Ensure fixtures is intact
        assert (REPO_ROOT / "courses" / "fixtures").is_dir()

    def test_archive_mode(self, dummy_course_setup):
        cid = dummy_course_setup["cid"]
        res = delete_course(cid, archive=True, dry_run=False)
        assert res["success"] is True

        # Platform files removed from courses/
        assert not dummy_course_setup["json_path"].exists()

        # Verify items were moved to archive
        archive_root = REPO_ROOT / "archive_rejected_courses"
        found_archived = list(archive_root.glob(f"{cid}_*"))
        assert len(found_archived) > 0

        # Cleanup archive test folder
        for af in found_archived:
            shutil.rmtree(af, ignore_errors=True)
