"""Unit tests for incremental template compilation, templates_report persistence, and dispatch_repair improvements.

Validates Stream 1C implementation:
1. dispatch_repair with comma-separated --ids:
   - Parses and flattens IDs like "C-05,C-11,H-02".
   - Generates distinct subagents pointing to prompts/repair/repair_c05.json, repair_c11.json, repair_h02.json without collision.
2. templates_report.json error extraction:
   - Reads errors_by_cid and flat errors list into diagnostics.template_errors without falling back to manual_request.
3. run_stage_templates persistence & incremental skip:
   - Writes work/reports/templates_report.json on both PASS and FAIL (before raising ValueError).
   - Skips recompiling shard data files when templates in work/templates/<cid>.json are up-to-date with respect to shard_XX_data.py and shard_fixes.
"""

from __future__ import annotations

import io
import json
import os
import shutil
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

SKILL_DIR = Path(__file__).resolve().parent.parent / ".agents" / "skills" / "content-to-course"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from dispatch import dispatch_repair, build_dispatch
from run import PipelineRunner


class TestRunTemplatesAndDispatchRepair(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp(prefix="c2c_v36_stream1c_test_")
        self.work_dir = Path(self.test_dir) / "work"
        self.work_dir.mkdir(parents=True, exist_ok=True)

        # Standard minimal CTA
        self.distractors_c05 = [
            {"id": f"D-05-{i:02d}", "name": f"Distractor {i}", "wrong_belief": f"Error {i}", "omitted_step": f"Step {i}"}
            for i in range(1, 7)
        ]
        self.distractors_c11 = [
            {"id": f"D-11-{i:02d}", "name": f"Distractor {i}", "wrong_belief": f"Error {i}", "omitted_step": f"Step {i}"}
            for i in range(1, 7)
        ]
        self.distractors_h02 = [
            {"id": f"D-02-{i:02d}", "name": f"Distractor {i}", "wrong_belief": f"Error {i}", "omitted_step": f"Step {i}"}
            for i in range(1, 7)
        ]

        self.cta_data = {
            "course_id": "test_c2c_v36",
            "competencies": [
                {
                    "id": "C-05",
                    "type": "knowledge",
                    "name": "Competencia Cinco",
                    "description_latex": r"$\alpha + \beta$",
                    "distractors": self.distractors_c05,
                },
                {
                    "id": "C-11",
                    "type": "skill",
                    "name": "Competencia Once",
                    "description_latex": r"$\int x dx$",
                    "distractors": self.distractors_c11,
                },
                {
                    "id": "H-02",
                    "type": "ability",
                    "name": "Habilidad Dos",
                    "description_latex": r"$\sigma^2$",
                    "distractors": self.distractors_h02,
                },
            ],
        }
        (self.work_dir / "cta.json").write_text(json.dumps(self.cta_data), encoding="utf-8")

        # Shard manifest
        self.shards_dir = self.work_dir / "shards"
        self.shards_dir.mkdir(parents=True, exist_ok=True)
        (self.shards_dir / "pre_shard_manifest.json").write_text(json.dumps({
            "shards": [
                {"shard_id": "shard_01", "competency_ids": ["C-05"]},
                {"shard_id": "shard_02", "competency_ids": ["C-11"]},
                {"shard_id": "shard_03", "competency_ids": ["H-02"]},
            ]
        }), encoding="utf-8")

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir, ignore_errors=True)

    # =========================================================================
    # 1. dispatch_repair with comma-separated --ids
    # =========================================================================
    def test_dispatch_repair_comma_separated_ids_and_no_pointer_collision(self) -> None:
        """dispatch_repair with ids='C-05,C-11,H-02' splits 3 competencies and generates unique pointers."""
        res = dispatch_repair(self.work_dir, ids=["C-05,C-11,H-02"], pointer=True)
        subagents = res.get("Subagents", [])
        self.assertEqual(len(subagents), 3)

        # 1. Pointers must refer to prompts/repair/repair_<cid_norm>.json without colliding on repair_01.json
        p0 = subagents[0]["Prompt"]
        p1 = subagents[1]["Prompt"]
        p2 = subagents[2]["Prompt"]

        self.assertIn("prompts/repair/repair_c05.json", p0)
        self.assertIn("prompts/repair/repair_c11.json", p1)
        self.assertIn("prompts/repair/repair_h02.json", p2)

        # 2. Files on disk in work/prompts/repair/
        prompts_repair_dir = self.work_dir / "prompts" / "repair"
        self.assertTrue((prompts_repair_dir / "repair_c05.json").is_file())
        self.assertTrue((prompts_repair_dir / "repair_c11.json").is_file())
        self.assertTrue((prompts_repair_dir / "repair_h02.json").is_file())

        # Also items_dir should have them
        items_dir = self.work_dir / "dispatch" / "items"
        self.assertTrue((items_dir / "repair_01.json").is_file())
        self.assertTrue((items_dir / "repair_02.json").is_file())
        self.assertTrue((items_dir / "repair_03.json").is_file())

        # 3. Test string with spaces and commas: ids='C-05, C-11'
        res2 = dispatch_repair(self.work_dir, ids="C-05, C-11", pointer=True)
        self.assertEqual(len(res2["Subagents"]), 2)
        self.assertIn("prompts/repair/repair_c05.json", res2["Subagents"][0]["Prompt"])
        self.assertIn("prompts/repair/repair_c11.json", res2["Subagents"][1]["Prompt"])

    # =========================================================================
    # 2. templates_report.json error injection into repair items
    # =========================================================================
    def test_dispatch_repair_injects_templates_report_errors(self) -> None:
        """dispatch_repair extracts errors from templates_report.json into repair work orders."""
        reports_dir = self.work_dir / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        report_data = {
            "status": "FAIL",
            "total_templates": 6,
            "total_seeds_run": 300,
            "errors": [
                "C-05 syntax error: missing bracket in generator",
                "Division by zero in seed 42 for C-11",
                "Unexpected invariant violation in H-02: bounds exceeded",
            ],
            "warnings": [],
            "errors_by_cid": {
                "C-05": ["C-05 syntax error: missing bracket in generator"],
                "C-11": ["Division by zero in seed 42 for C-11"],
            },
            "failed_competencies": ["C-05", "C-11", "H-02"],
        }
        (reports_dir / "templates_report.json").write_text(json.dumps(report_data), encoding="utf-8")

        res = dispatch_repair(self.work_dir, ids=["C-05,C-11,H-02"], pointer=True)
        subagents = res["Subagents"]
        self.assertEqual(len(subagents), 3)

        # Inspect work/prompts/repair/repair_c05.json
        c05_order = json.loads((self.work_dir / "prompts" / "repair" / "repair_c05.json").read_text(encoding="utf-8"))
        diag_c05 = c05_order.get("diagnostics", {})
        self.assertFalse(diag_c05.get("manual_request", False))
        self.assertIn("C-05 syntax error: missing bracket in generator", diag_c05.get("template_errors", []))
        self.assertIn("### Errores Diagnosticados en Templates:", c05_order.get("Prompt", ""))
        self.assertIn("- `C-05 syntax error: missing bracket in generator`", c05_order.get("Prompt", ""))

        # Inspect work/prompts/repair/repair_c11.json
        c11_order = json.loads((self.work_dir / "prompts" / "repair" / "repair_c11.json").read_text(encoding="utf-8"))
        diag_c11 = c11_order.get("diagnostics", {})
        self.assertFalse(diag_c11.get("manual_request", False))
        self.assertIn("Division by zero in seed 42 for C-11", diag_c11.get("template_errors", []))
        self.assertIn("### Errores Diagnosticados en Templates:", c11_order.get("Prompt", ""))
        self.assertIn("- `Division by zero in seed 42 for C-11`", c11_order.get("Prompt", ""))

        # Inspect H-02 (matched via flat errors string)
        h02_order = json.loads((self.work_dir / "prompts" / "repair" / "repair_h02.json").read_text(encoding="utf-8"))
        diag_h02 = h02_order.get("diagnostics", {})
        self.assertFalse(diag_h02.get("manual_request", False))
        self.assertIn("Unexpected invariant violation in H-02: bounds exceeded", diag_h02.get("template_errors", []))
        self.assertIn("### Errores Diagnosticados en Templates:", h02_order.get("Prompt", ""))
        self.assertIn("- `Unexpected invariant violation in H-02: bounds exceeded`", h02_order.get("Prompt", ""))

    def test_dispatch_repair_deduplicates_ids_preserving_order(self) -> None:
        """dispatch_repair deduplicates --ids 'C-05, C-11, C-05' preserving order of appearance."""
        # 1. String with duplicate IDs
        res = dispatch_repair(self.work_dir, ids="C-05, C-11, C-05", pointer=True)
        subagents = res["Subagents"]
        self.assertEqual(len(subagents), 2)
        self.assertIn("repair_c05.json", subagents[0]["Prompt"])
        self.assertIn("repair_c11.json", subagents[1]["Prompt"])

        # 2. Combined list with duplicates across elements
        res2 = dispatch_repair(self.work_dir, ids=["C-11, C-05", "C-11", "C-05"], pointer=True)
        subagents2 = res2["Subagents"]
        self.assertEqual(len(subagents2), 2)
        self.assertIn("repair_c11.json", subagents2[0]["Prompt"])
        self.assertIn("repair_c05.json", subagents2[1]["Prompt"])

    def test_dispatch_repair_supports_dict_failed_competencies_and_diagnostics(self) -> None:
        """dispatch_repair parses failed_competencies as dict with errors list and populates prompt."""
        reports_dir = self.work_dir / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        report_data = {
            "status": "FAIL",
            "failed_competencies": {
                "C-05": {
                    "errors": ["Schema violation in C-05: missing question_type"]
                }
            },
            "errors": [],
        }
        (reports_dir / "templates_report.json").write_text(json.dumps(report_data), encoding="utf-8")

        res = dispatch_repair(self.work_dir, ids=["C-05"], pointer=True)
        subagents = res["Subagents"]
        self.assertEqual(len(subagents), 1)

        c05_order = json.loads((self.work_dir / "prompts" / "repair" / "repair_c05.json").read_text(encoding="utf-8"))
        diag = c05_order.get("diagnostics", {})
        self.assertIn("Schema violation in C-05: missing question_type", diag.get("template_errors", []))
        self.assertFalse(diag.get("manual_request", False))
        self.assertIn("- `Schema violation in C-05: missing question_type`", c05_order.get("Prompt", ""))

    def test_errors_by_cid_no_prefix_collision(self) -> None:
        """errors_by_cid does not falsely associate C-010 error to C-01 or C-10 error to C-1."""
        templates_dir = self.work_dir / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        report_file = self.work_dir / "reports" / "templates_report.json"

        # CTA with both C-01 and C-010
        cta_collision = {
            "course_id": "test_collision",
            "competencies": [
                {"id": "C-01", "name": "Uno", "type": "knowledge", "distractors": self.distractors_c05},
                {"id": "C-010", "name": "Diez", "type": "knowledge", "distractors": self.distractors_c11},
            ],
        }
        (self.work_dir / "cta.json").write_text(json.dumps(cta_collision), encoding="utf-8")

        # Create dummy template files
        (templates_dir / "C-01.json").write_text(json.dumps([{"id": "t1"}]), encoding="utf-8")
        (templates_dir / "C-010.json").write_text(json.dumps([{"id": "t2"}]), encoding="utf-8")

        runner = PipelineRunner(work_dir=self.work_dir)
        fake_errors = [
            "Competency C-010 failed invariant: value out of bounds",
            "Error in work/templates/C-010.json: syntax check error",
        ]
        with patch("run.check_templates_file_or_dir", return_value=(False, fake_errors)):
            with self.assertRaises(ValueError):
                runner.run_stage_templates()

        self.assertTrue(report_file.is_file())
        rep = json.loads(report_file.read_text(encoding="utf-8"))
        errors_by_cid = rep.get("errors_by_cid", {})

        # C-010 must have errors, C-01 must have NO errors
        self.assertIn("C-010", errors_by_cid)
        self.assertEqual(len(errors_by_cid["C-010"]), 2)
        self.assertNotIn("C-01", errors_by_cid)
        self.assertEqual(rep["failed_competencies"], ["C-010"])

        # Also verify dispatch_repair isolates them
        # Set shard map for C-01 and C-010
        (self.shards_dir / "pre_shard_manifest.json").write_text(json.dumps({
            "shards": [
                {"shard_id": "shard_01", "competency_ids": ["C-01"]},
                {"shard_id": "shard_02", "competency_ids": ["C-010"]},
            ]
        }), encoding="utf-8")

        disp_res = dispatch_repair(self.work_dir, ids=["C-01, C-010"], pointer=True)
        c01_order = json.loads((self.work_dir / "prompts" / "repair" / "repair_c01.json").read_text(encoding="utf-8"))
        c010_order = json.loads((self.work_dir / "prompts" / "repair" / "repair_c010.json").read_text(encoding="utf-8"))

        # C-01 has no template errors from C-010
        self.assertNotIn("Competency C-010 failed invariant: value out of bounds", c01_order.get("diagnostics", {}).get("template_errors", []))
        # C-010 has the template error
        self.assertIn("Competency C-010 failed invariant: value out of bounds", c010_order.get("diagnostics", {}).get("template_errors", []))

    def test_run_stage_templates_invalidates_cache_on_newer_shard_fix_or_cta(self) -> None:
        """run_stage_templates recompiles shard when shard_fix or cta.json is newer than template."""
        templates_dir = self.work_dir / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        shard_data_p = self.shards_dir / "shard_01_data.py"
        shard_data_p.write_text("# Shard 01 data\n", encoding="utf-8")

        # Shard data created at t - 200
        now = time.time()
        os.utime(shard_data_p, (now - 200, now - 200))

        # Template C-05.json created at t - 100
        c05_json = templates_dir / "C-05.json"
        c05_json.write_text(json.dumps([{"id": "tpl_dummy"}]), encoding="utf-8")
        os.utime(c05_json, (now - 100, now - 100))

        # CTA created at t - 300
        cta_file = self.work_dir / "cta.json"
        os.utime(cta_file, (now - 300, now - 300))

        # 1. Shard fix created at t (newer than template C-05.json)
        shard_fixes_dir = self.shards_dir / "shard_fixes"
        shard_fixes_dir.mkdir(parents=True, exist_ok=True)
        fix_p = shard_fixes_dir / "C-05.py"
        fix_p.write_text("# surgical fix\n", encoding="utf-8")
        os.utime(fix_p, (now, now))

        runner = PipelineRunner(work_dir=self.work_dir)

        # Mock compile_shard mod
        mock_compile = unittest.mock.MagicMock(return_value=(True, []))
        with patch.dict("sys.modules", {"compile_shard": unittest.mock.MagicMock(compile_shard=mock_compile)}):
            with patch("run.check_templates_file_or_dir", return_value=(True, [])):
                with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                    runner.run_stage_templates()
                    output = mock_stdout.getvalue()

        # Cache must NOT be skipped because fix_p is newer than c05_json!
        self.assertNotIn("Skipping compilation for shard_01_data.py", output)
        mock_compile.assert_called_once()

        # 2. Now touch c05_json so it's newer than fix_p (at now + 100)
        os.utime(c05_json, (now + 100, now + 100))
        mock_compile.reset_mock()
        with patch.dict("sys.modules", {"compile_shard": unittest.mock.MagicMock(compile_shard=mock_compile)}):
            with patch("run.check_templates_file_or_dir", return_value=(True, [])):
                with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                    runner.run_stage_templates()
                    output2 = mock_stdout.getvalue()

        self.assertIn("Skipping compilation for shard_01_data.py (templates up-to-date).", output2)
        mock_compile.assert_not_called()

        # 3. Now touch cta.json so it's newer than c05_json (at now + 200)
        os.utime(cta_file, (now + 200, now + 200))
        mock_compile.reset_mock()
        with patch.dict("sys.modules", {"compile_shard": unittest.mock.MagicMock(compile_shard=mock_compile)}):
            with patch("run.check_templates_file_or_dir", return_value=(True, [])):
                with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                    runner.run_stage_templates()
                    output3 = mock_stdout.getvalue()

        # Recompiles because cta.json is newer!
        self.assertNotIn("Skipping compilation for shard_01_data.py", output3)
        mock_compile.assert_called_once()

    # =========================================================================
    # 3. run_stage_templates: templates_report.json persistence and incremental skip
    # =========================================================================
    def test_run_stage_templates_persists_report_on_fail_and_pass(self) -> None:
        """run_stage_templates creates work/reports/templates_report.json on both PASS and FAIL."""
        templates_dir = self.work_dir / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        report_file = self.work_dir / "reports" / "templates_report.json"

        # 1. Invalid template: should write report with FAIL and raise ValueError
        invalid_template = [{
            "id": "tpl_01",
            "competency_id": "C-05",
            # missing required schema fields to induce failure
        }]
        (templates_dir / "C-05.json").write_text(json.dumps(invalid_template), encoding="utf-8")

        runner = PipelineRunner(work_dir=self.work_dir)
        with self.assertRaises(ValueError):
            runner.run_stage_templates()

        self.assertTrue(report_file.is_file(), "templates_report.json must be written even when validation fails!")
        rep_fail = json.loads(report_file.read_text(encoding="utf-8"))
        self.assertEqual(rep_fail["status"], "FAIL")
        self.assertGreater(len(rep_fail["errors"]), 0)
        self.assertIn("C-05", rep_fail["failed_competencies"])
        self.assertIn("C-05", rep_fail["errors_by_cid"])

    def test_run_stage_templates_skips_up_to_date_shards(self) -> None:
        """run_stage_templates skips compile_shard when templates are newer than shard data files."""
        templates_dir = self.work_dir / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)

        now = time.time()
        shard_data_p = self.shards_dir / "shard_01_data.py"
        shard_data_p.write_text("# Shard 01 data\n", encoding="utf-8")
        os.utime(shard_data_p, (now - 100, now - 100))

        # Ensure cta.json is older than templates
        cta_file = self.work_dir / "cta.json"
        if cta_file.is_file():
            os.utime(cta_file, (now - 200, now - 200))

        # Template C-05.json newer than shard_01_data.py
        c05_json = templates_dir / "C-05.json"
        c05_json.write_text(json.dumps([{"id": "tpl_dummy"}]), encoding="utf-8")
        os.utime(c05_json, (now, now))

        runner = PipelineRunner(work_dir=self.work_dir)

        # Mock check_templates_file_or_dir to avoid full dry-run on dummy template
        with patch("run.check_templates_file_or_dir", return_value=(True, [])):
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                runner.run_stage_templates()
                output = mock_stdout.getvalue()

        self.assertIn("Skipping compilation for shard_01_data.py (templates up-to-date).", output)

        report_file = self.work_dir / "reports" / "templates_report.json"
        self.assertTrue(report_file.is_file())
        rep_pass = json.loads(report_file.read_text(encoding="utf-8"))
        self.assertEqual(rep_pass["status"], "PASS")
        self.assertEqual(len(rep_pass["errors"]), 0)


if __name__ == "__main__":
    unittest.main()
