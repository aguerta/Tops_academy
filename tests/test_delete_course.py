"""Automated test suite for the delete-course skill and deletion engine."""
from __future__ import annotations

import json
import os
import shutil
import sys
import time
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

SKILL_SCRIPTS_DIR = REPO_ROOT / ".agents" / "skills" / "delete-course" / "scripts"
if str(SKILL_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_SCRIPTS_DIR))

C2C_DIR = REPO_ROOT / ".agents" / "skills" / "content-to-course"
if str(C2C_DIR) not in sys.path:
    sys.path.insert(0, str(C2C_DIR))

import delete_course as delete_course_mod
from delete_course import (
    SecurityError,
    assert_path_safe,
    clean_orphan_course_dirs,
    delete_course,
    find_course_artifacts,
    is_active_workspace,
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

    def test_clean_orphan_dirs(self, tmp_path, monkeypatch):
        """Verify that clean_orphan_course_dirs is strictly isolated, never touches the
        real courses directory, preserves active workspaces and recent files, and only
        removes stale orphans older than 24h.
        """
        # Strictly isolate COURSES_DIR to tmp_path
        monkeypatch.setattr(delete_course_mod, "COURSES_DIR", tmp_path)
        monkeypatch.setenv("COURSES_DIR", str(tmp_path))

        # 1. Setup fixtures in isolated directory
        fixtures_dir = tmp_path / "fixtures"
        fixtures_dir.mkdir(parents=True, exist_ok=True)
        (fixtures_dir / "sample_fixture.json").write_text("{}", encoding="utf-8")

        # 2. Active course with JSON (should never be considered orphan)
        active_dir = tmp_path / "active_course_1"
        active_dir.mkdir(parents=True, exist_ok=True)
        (active_dir / "active.txt").write_text("course files", encoding="utf-8")
        (tmp_path / "active_course_1.json").write_text("{}", encoding="utf-8")

        # 3. Active in-progress workspace with state files (no JSON, but has work/pre_cta_manifest.json)
        # Even if timestamps are artificially aged > 24 hours, presence of state files MUST protect it.
        old_time = time.time() - (48 * 3600)
        state_ws = tmp_path / "in_progress_course_state"
        (state_ws / "work").mkdir(parents=True, exist_ok=True)
        state_manifest = state_ws / "work" / "pre_cta_manifest.json"
        state_manifest.write_text("{}", encoding="utf-8")
        os.utime(state_manifest, (old_time, old_time))
        os.utime(state_ws / "work", (old_time, old_time))
        os.utime(state_ws, (old_time, old_time))

        # 4. Active in-progress workspace with work/state.json
        state_ws2 = tmp_path / "in_progress_course_state2"
        (state_ws2 / "work").mkdir(parents=True, exist_ok=True)
        state_json = state_ws2 / "work" / "state.json"
        state_json.write_text("{}", encoding="utf-8")
        os.utime(state_json, (old_time, old_time))
        os.utime(state_ws2 / "work", (old_time, old_time))
        os.utime(state_ws2, (old_time, old_time))

        # 5. Active in-progress workspace with work/cta_data.py
        state_ws3 = tmp_path / "in_progress_course_state3"
        (state_ws3 / "work").mkdir(parents=True, exist_ok=True)
        cta_data = state_ws3 / "work" / "cta_data.py"
        cta_data.write_text("# cta data", encoding="utf-8")
        os.utime(cta_data, (old_time, old_time))
        os.utime(state_ws3 / "work", (old_time, old_time))
        os.utime(state_ws3, (old_time, old_time))

        # 6. Active workspace with recent file (< 24h old, no JSON, no state files)
        recent_ws = tmp_path / "recent_wip_course"
        recent_ws.mkdir(parents=True, exist_ok=True)
        recent_file = recent_ws / "wip_notes.txt"
        recent_file.write_text("in progress notes", encoding="utf-8")

        # 7. Old orphan directory (> 24h old, no JSON, no state files)
        stale_orphan = tmp_path / "old_stale_orphan"
        stale_orphan.mkdir(parents=True, exist_ok=True)
        stale_file = stale_orphan / "stale_temp.txt"
        stale_file.write_text("stale data", encoding="utf-8")
        os.utime(stale_file, (old_time, old_time))
        os.utime(stale_orphan, (old_time, old_time))

        # Record real courses directory state to verify it is NEVER touched
        real_courses_dir = REPO_ROOT / "courses"
        real_before = set(real_courses_dir.iterdir()) if real_courses_dir.exists() else set()

        # Execute clean_orphan_course_dirs in isolated environment
        cleaned = clean_orphan_course_dirs(dry_run=False)

        # Verify real courses directory was NEVER touched
        real_after = set(real_courses_dir.iterdir()) if real_courses_dir.exists() else set()
        assert real_before == real_after, "CRITICAL: The real courses/ directory was modified during isolated test!"

        # Assert stale orphan was deleted
        assert str(stale_orphan) in cleaned
        assert not stale_orphan.exists()

        # Assert active workspaces, active courses, and fixtures are PRESERVED
        assert fixtures_dir.is_dir()
        assert active_dir.is_dir()
        assert state_ws.is_dir()
        assert state_manifest.is_file()
        assert state_ws2.is_dir()
        assert state_json.is_file()
        assert state_ws3.is_dir()
        assert cta_data.is_file()
        assert recent_ws.is_dir()
        assert recent_file.is_file()

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


class TestActiveWorkspaceSafeguards:
    """Verifies that is_active_workspace correctly identifies active workspaces."""

    def test_is_active_workspace_with_pre_cta_manifest(self, tmp_path):
        ws = tmp_path / "course_ws"
        (ws / "work").mkdir(parents=True)
        manifest = ws / "work" / "pre_cta_manifest.json"
        manifest.write_text("{}", encoding="utf-8")
        # Artificially age the file to 50 hours ago
        old_time = time.time() - (50 * 3600)
        os.utime(manifest, (old_time, old_time))
        assert is_active_workspace(ws) is True

    def test_is_active_workspace_with_state_json(self, tmp_path):
        ws = tmp_path / "course_ws"
        (ws / "work").mkdir(parents=True)
        state_file = ws / "work" / "state.json"
        state_file.write_text("{}", encoding="utf-8")
        old_time = time.time() - (50 * 3600)
        os.utime(state_file, (old_time, old_time))
        assert is_active_workspace(ws) is True

    def test_is_active_workspace_with_cta_data(self, tmp_path):
        ws = tmp_path / "course_ws"
        (ws / "work").mkdir(parents=True)
        cta_file = ws / "work" / "cta_data.py"
        cta_file.write_text("# cta", encoding="utf-8")
        old_time = time.time() - (50 * 3600)
        os.utime(cta_file, (old_time, old_time))
        assert is_active_workspace(ws) is True

    def test_is_active_workspace_with_recent_file(self, tmp_path):
        ws = tmp_path / "course_ws"
        ws.mkdir(parents=True)
        recent_file = ws / "any_file.txt"
        recent_file.write_text("modified recently", encoding="utf-8")
        assert is_active_workspace(ws) is True

    def test_is_active_workspace_stale_files_no_state(self, tmp_path):
        ws = tmp_path / "course_ws"
        ws.mkdir(parents=True)
        stale_file = ws / "old_file.txt"
        stale_file.write_text("old content", encoding="utf-8")
        old_time = time.time() - (48 * 3600)
        os.utime(stale_file, (old_time, old_time))
        assert is_active_workspace(ws) is False

    def test_is_active_workspace_empty_dir(self, tmp_path):
        ws = tmp_path / "empty_ws"
        ws.mkdir(parents=True)
        assert is_active_workspace(ws) is False


class TestLatexRegexFracFix:
    """Verifies that frac_simple_fix preserves subscripts and superscripts inside LaTeX fractions."""

    def test_frac_preserves_subscripts(self):
        from engine.assemble import sanitize_katex_syntax

        # Regression test for \hat{\beta}_1 = \frac{S_{xy}}{S_{xx}} (Defect #6 / Run 2)
        raw = r"\hat{\beta}_1 = \frac{S_{xy}}{S_{xx}}"
        sanitized = sanitize_katex_syntax(raw)
        assert sanitized == raw, f"Expected {raw!r}, got {sanitized!r}"

    def test_frac_preserves_superscripts(self):
        from engine.assemble import sanitize_katex_syntax

        raw = r"\frac{K^{0.5}}{L^{0.5}}"
        sanitized = sanitize_katex_syntax(raw)
        assert sanitized == raw, f"Expected {raw!r}, got {sanitized!r}"

    def test_frac_preserves_nested_subscripts_and_superscripts(self):
        from engine.assemble import sanitize_katex_syntax

        raw = r"\frac{\sigma_{xy}^2}{\sigma_{xx}^2}"
        sanitized = sanitize_katex_syntax(raw)
        assert sanitized == raw, f"Expected {raw!r}, got {sanitized!r}"

    def test_frac_simple_fix_repairs_missing_numerator_close_brace(self):
        from engine.assemble import sanitize_katex_syntax

        # Simple \frac{a{b} missing numerator close brace should be repaired to \frac{a}{b}
        raw = r"\frac{a{b}"
        sanitized = sanitize_katex_syntax(raw)
        assert sanitized == r"\frac{a}{b}", f"Expected '\\frac{{a}}{{b}}', got {sanitized!r}"


class TestPurgeLegacyCorpusAndSections:
    """Verifies complete elimination of legacy corpus.md and section_*.md across pipeline."""

    def test_dispatch_py_has_no_legacy_corpus_or_section_fallbacks(self):
        dispatch_path = REPO_ROOT / ".agents" / "skills" / "content-to-course" / "dispatch.py"
        content = dispatch_path.read_text(encoding="utf-8")

        # Verify no section_*.md in dispatch.py
        assert "section_*.md" not in content, "Found legacy 'section_*.md' in dispatch.py"
        assert "work/sections" not in content, "Found legacy 'work/sections' in dispatch.py"

        # Verify no corpus.md fallback in dispatch.py
        assert "corpus.md" not in content, "Found legacy 'corpus.md' in dispatch.py"

        # Verify role cta-map reads part slices
        from dispatch import ROLE_SPECS
        cta_map_read = ROLE_SPECS.get("cta-map", {}).get("read", [])
        assert "work/parts/part_*/**" in cta_map_read, "Expected 'work/parts/part_*/**' in cta-map read paths"
        assert "work/parts/part_manifest_*.json" in cta_map_read, "Expected 'work/parts/part_manifest_*.json' in cta-map read paths"

    def test_run_py_has_no_legacy_corpus_prints(self):
        run_path = REPO_ROOT / ".agents" / "skills" / "content-to-course" / "run.py"
        content = run_path.read_text(encoding="utf-8")

        assert "Corpus file:" not in content, "Found legacy 'Corpus file:' print statement in run.py"
        assert "Stage 0: Lossless source partitioning & pre_cta_manifest generation" in content, (
            "Expected updated Stage 0 banner in run.py"
        )

    def test_system_prompts_have_no_legacy_corpus_or_section_references(self):
        prompts_dir = REPO_ROOT / ".agents" / "skills" / "content-to-course" / "system_prompts"
        c_analyser = (prompts_dir / "prompt_competence_analyser.md").read_text(encoding="utf-8")
        c_sectional = (prompts_dir / "prompt_cta_sectional.md").read_text(encoding="utf-8")

        assert "corpus.md" not in c_analyser, "Found legacy 'corpus.md' in prompt_competence_analyser.md"
        assert "work/sections" not in c_sectional, "Found legacy 'work/sections' in prompt_cta_sectional.md"
        assert "section_XX.md" not in c_sectional, "Found legacy 'section_XX.md' in prompt_cta_sectional.md"

    def test_skill_md_has_no_legacy_corpus_references(self):
        skill_path = REPO_ROOT / ".agents" / "skills" / "content-to-course" / "SKILL.md"
        content = skill_path.read_text(encoding="utf-8")

        assert "work/corpus.md" not in content, "Found legacy 'work/corpus.md' in SKILL.md"

    def test_dispatch_cta_items_have_zero_corpus_or_section_references(self, tmp_path):
        from dispatch import dispatch_cta

        # Direct mode
        manifest_data = {
            "course_id": "test_unit_purge",
            "total_pages": 5,
            "cta_mode": "direct",
            "documents": [
                {"doc_name": "sample.pdf", "path": "content/sample.pdf", "total_pages": 5}
            ],
        }
        (tmp_path / "pre_cta_manifest.json").write_text(json.dumps(manifest_data), encoding="utf-8")
        dispatch_cta(tmp_path, mode="direct")

        # Mapreduce mode
        manifest_mr = {
            "course_id": "test_unit_purge_mr",
            "total_pages": 10,
            "cta_mode": "mapreduce",
            "subparts": [
                {
                    "subpart_id": "part_01",
                    "doc": "sample.pdf",
                    "path": "content/sample.pdf",
                    "page_range": [1, 5],
                    "total_pages": 5,
                },
                {
                    "subpart_id": "part_02",
                    "doc": "sample.pdf",
                    "path": "content/sample.pdf",
                    "page_range": [6, 10],
                    "total_pages": 5,
                },
            ],
        }
        (tmp_path / "pre_cta_manifest.json").write_text(json.dumps(manifest_mr), encoding="utf-8")
        dispatch_cta(tmp_path, mode="mapreduce")

        # Inspect all generated dispatch artifacts
        dispatch_dir = tmp_path / "dispatch"
        assert dispatch_dir.is_dir()
        for f in dispatch_dir.rglob("*"):
            if f.is_file():
                txt = f.read_text(encoding="utf-8")
                assert "corpus.md" not in txt, f"Found legacy 'corpus.md' in {f}"
                assert "section_*.md" not in txt, f"Found legacy 'section_*.md' in {f}"
                assert "work/sections" not in txt, f"Found legacy 'work/sections' in {f}"

    def test_docs_have_no_legacy_corpus_references(self):
        readme_path = REPO_ROOT / "README.md"
        project_path = REPO_ROOT / "PROJECT.md"

        if readme_path.is_file():
            content = readme_path.read_text(encoding="utf-8")
            assert "work/corpus.md" not in content, "Found legacy 'work/corpus.md' in README.md"

        if project_path.is_file():
            content = project_path.read_text(encoding="utf-8")
            assert "Corpus Slicing" not in content, "Found legacy 'Corpus Slicing' in PROJECT.md"
