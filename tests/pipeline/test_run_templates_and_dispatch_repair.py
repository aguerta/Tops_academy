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

SKILL_DIR = Path(__file__).resolve().parents[2] / ".agents" / "skills" / "content-to-course"
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

        # 1. Pointers must refer to prompts/repair/repair_<cid_norm>_data.md without colliding on repair_01.json
        p0 = subagents[0]["Prompt"]
        p1 = subagents[1]["Prompt"]
        p2 = subagents[2]["Prompt"]

        self.assertIn("prompts/repair/repair_c05_data.md", p0)
        self.assertIn("prompts/repair/repair_c11_data.md", p1)
        self.assertIn("prompts/repair/repair_h02_data.md", p2)

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
        self.assertIn("prompts/repair/repair_c05_data.md", res2["Subagents"][0]["Prompt"])
        self.assertIn("prompts/repair/repair_c11_data.md", res2["Subagents"][1]["Prompt"])

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
        self.assertTrue(
            "### Diagnóstico Consolidado de Fallos y Discordancias:" in c05_order.get("Prompt", "")
            or "### Errores Diagnosticados en Templates:" in c05_order.get("Prompt", "")
        )
        self.assertIn("- `C-05 syntax error: missing bracket in generator`", c05_order.get("Prompt", ""))

        # Inspect work/prompts/repair/repair_c11.json
        c11_order = json.loads((self.work_dir / "prompts" / "repair" / "repair_c11.json").read_text(encoding="utf-8"))
        diag_c11 = c11_order.get("diagnostics", {})
        self.assertFalse(diag_c11.get("manual_request", False))
        self.assertIn("Division by zero in seed 42 for C-11", diag_c11.get("template_errors", []))
        self.assertTrue(
            "### Diagnóstico Consolidado de Fallos y Discordancias:" in c11_order.get("Prompt", "")
            or "### Errores Diagnosticados en Templates:" in c11_order.get("Prompt", "")
        )
        self.assertIn("- `Division by zero in seed 42 for C-11`", c11_order.get("Prompt", ""))

        # Inspect H-02 (matched via flat errors string)
        h02_order = json.loads((self.work_dir / "prompts" / "repair" / "repair_h02.json").read_text(encoding="utf-8"))
        diag_h02 = h02_order.get("diagnostics", {})
        self.assertFalse(diag_h02.get("manual_request", False))
        self.assertIn("Unexpected invariant violation in H-02: bounds exceeded", diag_h02.get("template_errors", []))
        self.assertTrue(
            "### Diagnóstico Consolidado de Fallos y Discordancias:" in h02_order.get("Prompt", "")
            or "### Errores Diagnosticados en Templates:" in h02_order.get("Prompt", "")
        )
        self.assertIn("- `Unexpected invariant violation in H-02: bounds exceeded`", h02_order.get("Prompt", ""))

    def test_dispatch_repair_deduplicates_ids_preserving_order(self) -> None:
        """dispatch_repair deduplicates --ids 'C-05, C-11, C-05' preserving order of appearance."""
        # 1. String with duplicate IDs
        res = dispatch_repair(self.work_dir, ids="C-05, C-11, C-05", pointer=True)
        subagents = res["Subagents"]
        self.assertEqual(len(subagents), 2)
        self.assertIn("repair_c05_data.md", subagents[0]["Prompt"])
        self.assertIn("repair_c11_data.md", subagents[1]["Prompt"])

        # 2. Combined list with duplicates across elements
        res2 = dispatch_repair(self.work_dir, ids=["C-11, C-05", "C-11", "C-05"], pointer=True)
        subagents2 = res2["Subagents"]
        self.assertEqual(len(subagents2), 2)
        self.assertIn("repair_c11_data.md", subagents2[0]["Prompt"])
        self.assertIn("repair_c05_data.md", subagents2[1]["Prompt"])

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

        # Template files for all CTA competencies (M20 requires complete templates/ matching cta.json)
        for cid_extra in ("C-11", "H-02"):
            extra_json = templates_dir / f"{cid_extra}.json"
            extra_json.write_text(json.dumps([{"id": f"T-{cid_extra}-01"}]), encoding="utf-8")
            os.utime(extra_json, (now, now))
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

        # Template files matching all CTA competencies (M20 completeness check)
        for cid_extra in ("C-11", "H-02"):
            extra_json = templates_dir / f"{cid_extra}.json"
            extra_json.write_text(json.dumps([{"id": f"T-{cid_extra}-01"}]), encoding="utf-8")
            os.utime(extra_json, (now, now))
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

    def test_dispatch_judges_targeted_arbitration_with_ids(self) -> None:
        """dispatch_judges filters judge batches and payload strictly to targeted competencies when ids is passed."""
        from dispatch import dispatch_judges
        from judge import generate_judge_batch

        templates_dir = self.work_dir / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)

        # Create templates for C-01 and C-16
        code_c01 = (
            "def generate(rng):\n"
            "    return {'vars': {'x': 1}, 'correct': '10', 'distractors': [\n"
            "        {'distractor_id': f'D-01-{i:02d}', 'value': f'{10+i}', 'error_rationale': f'Rat {i} con @x@'}\n"
            "        for i in range(1, 7)\n"
            "    ]}\n"
        )
        c01_tpl = {
            "id": "T-C01-01",
            "template_id": "T-C01-01",
            "competency_id": "C-01",
            "interaction_type": "multiple_choice_7_options",
            "generator_code": code_c01,
            "generate_py": code_c01,
            "stem": "Stem 1 @x@",
            "stems": ["Stem 1 @x@", "Stem 2 @x@", "Stem 3 @x@"],
            "hints": ["Hint 1", "Hint 2", "Hint 3"],
            "explanation_es": "Sol",
        }
        code_c16 = (
            "def generate(rng):\n"
            "    return {'vars': {'x': 2}, 'correct': '20', 'distractors': [\n"
            "        {'distractor_id': f'D-16-{i:02d}', 'value': f'{20+i}', 'error_rationale': f'Rat {i} con @x@'}\n"
            "        for i in range(1, 7)\n"
            "    ]}\n"
        )
        c16_tpl = {
            "id": "T-C16-01",
            "template_id": "T-C16-01",
            "competency_id": "C-16",
            "interaction_type": "multiple_choice_7_options",
            "generator_code": code_c16,
            "generate_py": code_c16,
            "stem": "Stem 1 @x@",
            "stems": ["Stem 1 @x@", "Stem 2 @x@", "Stem 3 @x@"],
            "hints": ["Hint 1", "Hint 2", "Hint 3"],
            "explanation_es": "Sol",
        }
        (templates_dir / "C-01.json").write_text(json.dumps([c01_tpl]), encoding="utf-8")
        (templates_dir / "C-16.json").write_text(json.dumps([c16_tpl]), encoding="utf-8")

        # 1. Test generate_judge_batch with targeted ids
        batch_p, truth_p = generate_judge_batch(
            templates_path=templates_dir,
            work_dir=self.work_dir,
            ids=["C-16"],
        )
        batch_items = json.loads(batch_p.read_text(encoding="utf-8"))
        self.assertGreater(len(batch_items), 0)
        self.assertTrue(all(item["competency_id"] == "C-16" for item in batch_items))

        # 2. Test dispatch_judges with targeted ids
        res = dispatch_judges(self.work_dir, ids=["C-16"], pointer=False)
        self.assertIn("Subagents", res)
        self.assertGreater(len(res["Subagents"]), 0)
        # Parse items payload from prompt
        for sub in res["Subagents"]:
            prompt = sub["Prompt"]
            self.assertIn("T-C16-01", prompt)
            self.assertNotIn("T-C01-01", prompt)

    def test_templates_fast_path_cert_verification_and_invalidation(self) -> None:
        """Fast-path cryptographic verification checks shard_XX.cert.json (< 5 ms) and invalidates on source delta."""
        import hashlib
        import os
        from engine.interstage_schemas import ArtifactCertificate, write_certificate

        shards_dir = self.work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)
        shard_file = shards_dir / "shard_01_data.py"
        shard_content = "# Shard 01 data file\nTEMPLATES = []\n"
        shard_file.write_text(shard_content, encoding="utf-8")

        cta_file = self.work_dir / "cta.json"
        single_cta = {"course_id": "test_c2c_v36", "competencies": [self.cta_data["competencies"][0]]}
        cta_file.write_text(json.dumps(single_cta), encoding="utf-8")

        templates_dir = self.work_dir / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        tpl_file = templates_dir / "C-05.json"
        tpl_bytes = b'[{"id": "T-C05-01", "template_id": "T-C05-01"}]'
        tpl_file.write_bytes(tpl_bytes)

        base_ts = time.time()
        os.utime(shard_file, (base_ts - 10, base_ts - 10))
        os.utime(cta_file, (base_ts - 10, base_ts - 10))
        os.utime(tpl_file, (base_ts - 5, base_ts - 5))

        (shards_dir / "pre_shard_manifest.json").write_text(
            json.dumps({"shards": [{"shard_id": "shard_01", "competency_ids": ["C-05"]}]}),
            encoding="utf-8",
        )
        cta_bytes = cta_file.read_bytes()
        cta_hash = hashlib.sha256(cta_bytes).hexdigest()
        src_hash = hashlib.sha256(shard_file.read_bytes()).hexdigest()
        tpl_hash = hashlib.sha256(tpl_bytes).hexdigest()

        cert = ArtifactCertificate(
            stage="templates",
            artifact_id="shard_01",
            source_sha256=src_hash,
            cta_sha256=cta_hash,
            template_shas={"C-05.json": tpl_hash},
            passed_50_seeds=True,
        )
        cert_path = shards_dir / "shard_01.cert.json"
        write_certificate(cert_path, cert)

        runner = PipelineRunner(work_dir=self.work_dir, strict=False)

        with patch("run.check_templates_file_or_dir", return_value=(True, [])):
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                t0 = time.time()
                res = runner.run_stage_templates()
                elapsed = time.time() - t0
                output = mock_stdout.getvalue()

        self.assertIn("Fast-path < 5 ms", output)
        self.assertLess(elapsed, 1.0)
        self.assertEqual(res["status"], "PASS")

        # Invalidate by altering 1 byte in shard_01_data.py
        shard_file.write_text(shard_content + "# mutated\n", encoding="utf-8")
        mock_compile = unittest.mock.MagicMock(return_value=(True, []))
        with patch.dict("sys.modules", {"compile_shard": unittest.mock.MagicMock(compile_shard=mock_compile)}):
            with patch("run.check_templates_file_or_dir", return_value=(True, [])):
                with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout2:
                    runner.run_stage_templates()
                    output2 = mock_stdout2.getvalue()
        # Fast path must be bypassed when source sha changes
        self.assertNotIn("Fast-path < 5 ms", output2)

    def test_stage_gates_build_verify_qa_and_blocking(self) -> None:
        """Stage gates executes build, verify, QA dry-run, and repair-matrix, failing when checks fail."""
        runner = PipelineRunner(work_dir=self.work_dir)
        course_file = self.work_dir / "course.json"
        course_file.write_text(json.dumps({"course_id": "test_c", "questions": []}), encoding="utf-8")

        # Case 1: verification failure in gates
        with patch.object(runner, "run_stage_build", return_value={"status": "passed"}):
            with patch.object(runner, "run_stage_verify", side_effect=RuntimeError("Mock invariant failure")):
                with patch.object(runner, "run_stage_repair_matrix", return_value={"status": "CLEAN", "matrix": {}}):
                    with patch("sys.stdout", new_callable=io.StringIO):
                        res = runner.run_stage_gates()
                        self.assertEqual(res["status"], "FAIL")
                        self.assertFalse(res["gates_passed"])
                        self.assertFalse(res["verify_ok"])

        # Case 2: publish dry-run failure in gates
        mock_audit_res = {
            "mastery_path_readiness": {"mpri_score": 50.0},
            "hard_penalties": ["Low MPRI failure"],
            "all_issues": [{"severity": "critical", "message": "Critical failure"}],
            "risk_clusters": {},
        }
        with patch.object(runner, "run_stage_build", return_value={"status": "passed"}):
            with patch.object(runner, "run_stage_verify", return_value={"status": "passed"}):
                with patch("course_publisher._load_run_full_audit", return_value=lambda parsed: mock_audit_res):
                    with patch.object(runner, "run_stage_repair_matrix", return_value={"status": "REPAIR_NEEDED", "failing_competencies": ["C-05"], "matrix": {}}):
                        with patch("sys.stdout", new_callable=io.StringIO):
                            res = runner.run_stage_gates()
                            self.assertEqual(res["status"], "FAIL")
                            self.assertFalse(res["gates_passed"])
                            self.assertFalse(res["qa_ok"])
                            self.assertTrue((self.work_dir / "publish_rejection_spec.json").is_file())

    def test_stage_repair_matrix_reads_grouped_by_rule_and_diagnostics(self) -> None:
        """Stage repair-matrix reads grouped_by_rule and diagnostics_by_competency across spec files."""
        runner = PipelineRunner(work_dir=self.work_dir)

        spec_data = {
            "stage": "publish_qa_dry_run",
            "failing_shards": ["shard_01"],
            "affected_shards": ["shard_01"],
            "failing_competencies": ["C-05"],
            "grouped_by_rule": {
                "R-15": {
                    "shards": ["shard_01"],
                    "competencies": ["C-05"],
                    "count": 1,
                    "sample": "Length parity bias",
                }
            },
            "diagnostics_by_competency": {
                "C-05": ["Distractor length out of bounds"]
            },
        }
        (self.work_dir / "publish_rejection_spec.json").write_text(
            json.dumps(spec_data, indent=2), encoding="utf-8"
        )

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            res = runner.run_stage_repair_matrix()
            output = mock_stdout.getvalue()

        self.assertEqual(res["status"], "REPAIR_NEEDED")
        self.assertIn("C-05", res.get("failing_competencies", []))
        self.assertIn("shard_01", res.get("by_shard", {}))
        self.assertIn("C-05", res.get("matrix", {}))
        findings = res["matrix"]["C-05"]["findings"]
        self.assertTrue(any("R-15" in f for f in findings))
        self.assertTrue(any("Distractor length out of bounds" in f for f in findings))
        self.assertTrue((self.work_dir / "repair_matrix.json").is_file())

    # =========================================================================
    # 4. C2C v4.1 Stream 1C Hardening Tests
    # =========================================================================
    def test_all_dispatch_manifests_stamp_dispatched_at_iso8601_utc(self) -> None:
        """dispatch_cta, dispatch_cta_reduce, dispatch_authors, dispatch_judges, and dispatch_repair stamp dispatched_at (ISO-8601 UTC)."""
        from datetime import datetime
        from dispatch import dispatch_cta, dispatch_cta_reduce, dispatch_authors, dispatch_judges

        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "course_id": "test_c2c_v41",
            "cta_mode": "direct",
            "documents": [{"name": "lecture.pdf", "path": "content/lecture.pdf", "total_pages": 12}],
        }), encoding="utf-8")

        verif_dir = self.work_dir / "verification"
        verif_dir.mkdir(parents=True, exist_ok=True)
        (verif_dir / "judge_batch_01.json").write_text(json.dumps([
            {"question_id": "Q-05-01", "question_type": "multiple_choice", "stem_es": "Calcule X", "options": [{"id": "A", "content": "1"}]}
        ]), encoding="utf-8")

        cta_res = dispatch_cta(self.work_dir, pointer=True)
        reduce_res = dispatch_cta_reduce(self.work_dir, pointer=True)
        author_res = dispatch_authors(self.work_dir, pointer=True)
        judge_res = dispatch_judges(self.work_dir, pointer=True)
        repair_res = dispatch_repair(self.work_dir, ids=["C-05"], pointer=True)

        dispatch_dir = self.work_dir / "dispatch"
        manifest_files = [
            dispatch_dir / "cta.json",
            dispatch_dir / "cta_reduce.json",
            dispatch_dir / "authors.json",
            dispatch_dir / "author.json",
            dispatch_dir / "judges.json",
            dispatch_dir / "judge.json",
            dispatch_dir / "repair.json",
        ]
        for mf in manifest_files:
            self.assertTrue(mf.is_file(), f"Missing wave manifest: {mf}")
            data = json.loads(mf.read_text(encoding="utf-8"))
            ts = data.get("dispatched_at")
            self.assertIsInstance(ts, str, f"dispatched_at missing or not str in {mf.name}")
            parsed_dt = datetime.fromisoformat(ts)
            self.assertIsNotNone(parsed_dt.tzinfo, f"dispatched_at in {mf.name} must be timezone-aware UTC: {ts}")

        for res_dict in (cta_res, reduce_res, author_res, judge_res, repair_res):
            self.assertIn("dispatched_at", res_dict)
            self.assertIsNotNone(datetime.fromisoformat(res_dict["dispatched_at"]).tzinfo)

    def test_subagent_initial_prompt_includes_explicit_scope_lock_target_paths(self) -> None:
        """Each Subagents[i]['Prompt'] includes [SCOPE-LOCK] with explicit allowed READ/WRITE target paths."""
        from dispatch import dispatch_cta, dispatch_authors, dispatch_judges

        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "course_id": "test_c2c_v41",
            "cta_mode": "direct",
            "documents": [{"name": "lecture.pdf", "path": "content/lecture.pdf", "total_pages": 12}],
        }), encoding="utf-8")

        verif_dir = self.work_dir / "verification"
        verif_dir.mkdir(parents=True, exist_ok=True)
        (verif_dir / "judge_batch_01.json").write_text(json.dumps([
            {"question_id": "Q-05-01", "question_type": "multiple_choice", "stem_es": "Calcule X", "options": [{"id": "A", "content": "1"}]}
        ]), encoding="utf-8")

        cta_sub = dispatch_cta(self.work_dir, pointer=True)["Subagents"][0]["Prompt"]
        self.assertIn("[SCOPE-LOCK]", cta_sub)
        self.assertIn("READ", cta_sub)
        self.assertIn("WRITE", cta_sub)
        self.assertIn("cta_data.py", cta_sub)
        self.assertIn("compile_cta.py", cta_sub)
        self.assertIn("DONE:", cta_sub)

        auth_subs = dispatch_authors(self.work_dir, pointer=True)["Subagents"]
        auth_sub_01 = next(s["Prompt"] for s in auth_subs if "shard_01" in s["Role"])
        self.assertIn("[SCOPE-LOCK]", auth_sub_01)
        self.assertIn("READ", auth_sub_01)
        self.assertIn("WRITE", auth_sub_01)
        self.assertIn("shard_01_data.py", auth_sub_01)
        self.assertIn("compile_shard.py", auth_sub_01)
        self.assertIn("DONE:", auth_sub_01)

        judge_sub = dispatch_judges(self.work_dir, pointer=True)["Subagents"][0]["Prompt"]
        self.assertIn("[SCOPE-LOCK]", judge_sub)
        self.assertIn("READ", judge_sub)
        self.assertIn("WRITE", judge_sub)
        self.assertIn("judge_01.json", judge_sub)
        self.assertIn("judge_responses_01.json", judge_sub)
        self.assertIn("DONE:", judge_sub)

        rep_sub = dispatch_repair(self.work_dir, ids=["C-05"], pointer=True)["Subagents"][0]["Prompt"]
        self.assertIn("[SCOPE-LOCK]", rep_sub)
        self.assertIn("READ", rep_sub)
        self.assertIn("WRITE", rep_sub)
        self.assertIn("repair_c05_data.md", rep_sub)
        self.assertIn("shard_01_data.py", rep_sub)
        self.assertIn("compile_shard.py", rep_sub)
        self.assertIn("DONE:", rep_sub)

    def test_author_item_prompt_section3_is_compact_and_eliminates_done_space_pollution(self) -> None:
        """Section ## 3. in work/dispatch/items/author_01.json['Prompt'] is < 2,500 chars and does not contain literal 'DONE: '."""
        from dispatch import dispatch_cta, dispatch_authors, dispatch_judges, load_system_prompt

        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "course_id": "test_c2c_v41",
            "cta_mode": "direct",
            "documents": [{"name": "lecture.pdf", "path": "content/lecture.pdf", "total_pages": 12}],
        }), encoding="utf-8")
        verif_dir = self.work_dir / "verification"
        verif_dir.mkdir(parents=True, exist_ok=True)
        (verif_dir / "judge_batch_01.json").write_text(json.dumps([
            {"question_id": "Q-05-01", "question_type": "multiple_choice", "stem_es": "Calcule X", "options": [{"id": "A", "content": "1"}]}
        ]), encoding="utf-8")

        dispatch_cta(self.work_dir, pointer=True)
        dispatch_authors(self.work_dir, pointer=True)
        dispatch_judges(self.work_dir, pointer=True)
        dispatch_repair(self.work_dir, ids=["C-05"], pointer=True)

        items_dir = self.work_dir / "dispatch" / "items"
        author_item = json.loads((items_dir / "author_01.json").read_text(encoding="utf-8"))
        author_prompt = author_item["Prompt"]

        self.assertIn("## 3. INSTRUCCIONES DE EJECUCIÓN", author_prompt)
        sec3 = author_prompt.split("## 3. INSTRUCCIONES DE EJECUCIÓN", 1)[1]
        self.assertLess(len(sec3), 2500, f"Section 3 of author_01.json is too bloated: {len(sec3)} chars")
        self.assertNotIn(load_system_prompt("prompt_shard_author.md", lean=True).strip(), author_prompt)

        # Disk work orders read via read_file must NOT contain literal 'DONE: ' to prevent GENERIC step pollution
        for disk_item in [
            items_dir / "author_01.json",
            items_dir / "cta_01.json",
            items_dir / "judge_01.json",
            items_dir / "repair_01.json",
            self.work_dir / "prompts" / "repair" / "repair_c05.json",
        ]:
            self.assertTrue(disk_item.is_file(), f"Missing disk item: {disk_item}")
            disk_prompt = json.loads(disk_item.read_text(encoding="utf-8"))["Prompt"]
            self.assertNotIn("DONE:", disk_prompt, f"Disk work order {disk_item.name} must not contain 'DONE:'")
            self.assertIn("Cierre al aprobar:", disk_prompt)

    def test_dispatch_repair_consolidates_multiple_competencies_in_same_shard(self) -> None:
        """When multiple failing competencies belong to the same shard, Subagents consolidates them into 1 shard-level invocation while keeping per-competency work orders on disk."""
        # Map C-05 and C-11 to shard_01, and H-02 to shard_02
        (self.shards_dir / "pre_shard_manifest.json").write_text(json.dumps({
            "shards": [
                {"shard_id": "shard_01", "competency_ids": ["C-05", "C-11"]},
                {"shard_id": "shard_02", "competency_ids": ["H-02"]},
            ]
        }), encoding="utf-8")

        res = dispatch_repair(self.work_dir, ids=["C-05, C-11, H-02"], pointer=True)
        subagents = res.get("Subagents", [])
        # 2 affected shards -> 2 subagents (shard_01 consolidated for C-05 & C-11, shard_02 for H-02)
        self.assertEqual(len(subagents), 2, f"Expected 2 shard-consolidated repair subagents, got {len(subagents)}")

        s01_sub = subagents[0]
        self.assertEqual(s01_sub.get("shard_id"), "shard_01")
        self.assertEqual(s01_sub.get("assigned_competencies"), ["C-05", "C-11"])
        self.assertIn("[SCOPE-LOCK]", s01_sub["Prompt"])
        self.assertIn("repair_shard_01_data.md", s01_sub["Prompt"])
        self.assertIn("shard_01_data.py", s01_sub["Prompt"])
        self.assertIn("DONE: work/shards/shard_01.json", s01_sub["Prompt"])

        s02_sub = subagents[1]
        self.assertEqual(s02_sub.get("shard_id"), "shard_02")
        self.assertEqual(s02_sub.get("assigned_competencies"), ["H-02"])
        self.assertIn("repair_h02_data.md", s02_sub["Prompt"])

        # Per-competency work orders and pure-data payloads must exist on disk
        prompts_repair_dir = self.work_dir / "prompts" / "repair"
        self.assertTrue((prompts_repair_dir / "repair_c05.json").is_file())
        self.assertTrue((prompts_repair_dir / "repair_c11.json").is_file())
        self.assertTrue((prompts_repair_dir / "repair_h02.json").is_file())
        self.assertTrue((prompts_repair_dir / "repair_c05_data.md").is_file())
        self.assertTrue((prompts_repair_dir / "repair_c11_data.md").is_file())
        self.assertTrue((prompts_repair_dir / "repair_shard_01_data.md").is_file())
        self.assertTrue((prompts_repair_dir / "repair_h02_data.md").is_file())

    # =========================================================================
    # Stream 5A: Pure-Data Worker Payloads & Direct Initial Messages
    # =========================================================================
    def test_stream5a_direct_messages_and_pure_data_payloads(self) -> None:
        """All 5 roles emit compact pure-data payloads or direct initial messages without wrapper bloat."""
        from dispatch import dispatch_cta, dispatch_cta_reduce, dispatch_authors, dispatch_judges

        # 1. CTA Architect (slice mode): direct READ/Rango/WRITE/COMPILE/DONE, no cta_01.json or pre_cta_manifest.json
        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "course_id": "test_5a",
            "cta_mode": "mapreduce",
            "subparts": [
                {
                    "subpart_id": "part_01",
                    "doc": "doc.pdf",
                    "path": "work/slices/part_01/doc_p1_10.pdf",
                    "slice_path": "work/slices/part_01/doc_p1_10.pdf",
                    "page_range": [1, 10],
                    "total_pages": 10,
                }
            ],
        }), encoding="utf-8")
        cta_res = dispatch_cta(self.work_dir, mode="mapreduce", pointer=True)
        cta_prompt = cta_res["Subagents"][0]["Prompt"]
        self.assertLessEqual(len(cta_prompt.encode("utf-8")), 650)
        expected_slice_abs = (self.work_dir / "slices" / "part_01" / "doc_p1_10.pdf").resolve().as_posix()
        self.assertIn(f"READ: `{expected_slice_abs}`", cta_prompt)
        self.assertIn("Rango: `1..10`", cta_prompt)
        self.assertIn("WRITE:", cta_prompt)
        self.assertIn("COMPILE:", cta_prompt)
        self.assertIn("DONE:", cta_prompt)
        self.assertNotIn("cta_01.json", cta_prompt)
        self.assertNotIn("pre_cta_manifest.json", cta_prompt.split("COMPILE:")[0])
        cta_disk = json.loads((self.work_dir / "dispatch" / "items" / "cta_01.json").read_text(encoding="utf-8"))
        self.assertNotIn("pre_cta_manifest.json", cta_disk["Prompt"].split("WRITE permitido", 1)[0])

        # 2. CTA Harmonizer: direct READ/WRITE/RUN/DONE, no read_file cta_reduce_01.json, trimmed disk item
        (self.work_dir / "cta_parts").mkdir(parents=True, exist_ok=True)
        (self.work_dir / "cta_parts" / "part_01.json").write_text(json.dumps({"competencies": []}), encoding="utf-8")
        red_res = dispatch_cta_reduce(self.work_dir, pointer=True)
        red_prompt = red_res["Subagents"][0]["Prompt"]
        self.assertLessEqual(len(red_prompt.encode("utf-8")), 600)
        self.assertIn("cta_outline.json", red_prompt)
        self.assertIn("duplicate_candidates.json", red_prompt)
        self.assertIn("RUN:", red_prompt)
        self.assertIn("DONE:", red_prompt)
        self.assertNotIn("Work order:", red_prompt)
        red_disk = json.loads((self.work_dir / "dispatch" / "items" / "cta_reduce_01.json").read_text(encoding="utf-8"))
        self.assertNotIn("## 1. INSTRUCCIONES DE EJECUCIÓN", red_disk["Prompt"])

        # 3. Shard Author: pure-data author_01_data.md
        auth_res = dispatch_authors(self.work_dir, pointer=True)
        auth_prompt = next(s["Prompt"] for s in auth_res["Subagents"] if "shard_01" in s["Role"])
        self.assertLessEqual(len(auth_prompt.encode("utf-8")), 650)
        self.assertIn("author_01_data.md", auth_prompt)
        auth_data_md = (self.work_dir / "dispatch" / "items" / "author_01_data.md").read_text(encoding="utf-8")
        self.assertIn("## 2. ESPECIFICACIÓN TURN-0 COMPLETA DE COMPETENCIAS Y DISTRACTORES", auth_data_md)
        self.assertNotIn("TypeName", auth_data_md)
        self.assertNotIn("## 3. INSTRUCCIONES DE EJECUCIÓN", auth_data_md)

        # 4. Blind Judge: pure-data judge_01_items.json (JSON array only)
        verif_dir = self.work_dir / "verification"
        verif_dir.mkdir(parents=True, exist_ok=True)
        (verif_dir / "judge_batch_01.json").write_text(json.dumps([
            {"question_id": "Q-01", "question_type": "multiple_choice", "stem_es": "Calcule X", "options": [{"id": "A", "content": "1"}]}
        ]), encoding="utf-8")
        judge_res = dispatch_judges(self.work_dir, pointer=True)
        judge_prompt = judge_res["Subagents"][0]["Prompt"]
        self.assertLessEqual(len(judge_prompt.encode("utf-8")), 300)
        self.assertIn("judge_01_items.json", judge_prompt)
        judge_items_data = json.loads((self.work_dir / "dispatch" / "items" / "judge_01_items.json").read_text(encoding="utf-8"))
        self.assertIsInstance(judge_items_data, dict)
        self.assertEqual(list(judge_items_data.keys()), ["items"])
        self.assertEqual(judge_items_data["items"][0]["question_id"], "Q-01")

        # 5. Repair Engineer: pure-data repair_c05_data.md
        rep_res = dispatch_repair(self.work_dir, ids=["C-05"], pointer=True)
        rep_prompt = rep_res["Subagents"][0]["Prompt"]
        self.assertLessEqual(len(rep_prompt.encode("utf-8")), 650)
        self.assertIn("repair_c05_data.md", rep_prompt)
        rep_data_md = (self.work_dir / "prompts" / "repair" / "repair_c05_data.md").read_text(encoding="utf-8")
        self.assertIn("## 2. DIAGNÓSTICO DEL FALLO & COMPETENCE SLICE", rep_data_md)
        self.assertNotIn("TypeName", rep_data_md)
        self.assertNotIn("## 3. INSTRUCCIONES DE REPARACIÓN", rep_data_md)


if __name__ == "__main__":
    unittest.main()
