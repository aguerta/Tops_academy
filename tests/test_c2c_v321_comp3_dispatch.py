"""Comprehensive Test Suite for C2C v3.21 Component 3: Dispatch Load Inversion & Zero-Warmup Architecture.

Tests:
1. Load Inversion Invariant: Full uncompressed system prompts in work/dispatch/types/*.json
   (including prompt_cta_harmonizer.md for cta-reduce), with compact non-duplicating item prompts.
2. Turn-0 Complete Context in dispatch_authors: Full competency specification and 6 canonical
   distractors (D-XX-01..06) with wrong_belief, omitted_step, and compile_shard.py command.
3. Robustness across cta.json schemas (dict with list, dict with mapping, and pure list).
4. Scope-Lock Introspection Policy: ROLE_SPECS["author"] and ROLE_SPECS["repair"] read/forbidden paths.
5. dispatch_repair resolution from pre_shard_manifest.json without dependency on shard_*.json schemas.
6. dispatch_judges zero-warmup in-prompt payload and output path consistency (verification/judge_responses_XX.json).
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict, List

SKILL_DIR = Path(__file__).parent.parent / ".agents" / "skills" / "content-to-course"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from dispatch import (
    ROLE_SPECS,
    build_dispatch,
    build_scope_header,
    dispatch_authors,
    dispatch_cta,
    dispatch_judges,
    dispatch_repair,
    generate_define_subagent_specs,
    get_type_definitions,
    load_system_prompt,
    scope_check,
)


class TestC2CV321Comp3Dispatch(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp(prefix="c2c_v321_disp_test_")
        self.work_dir = Path(self.test_dir) / "courses" / "macro_test" / "work"
        self.work_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir, ignore_errors=True)

    # =========================================================================
    # 1. Load Inversion Invariant across all pipeline stages
    # =========================================================================
    def test_load_inversion_invariant_specs_vs_item_prompts(self) -> None:
        """Type specs in work/dispatch/types/ contain 100% full system prompts while items are concise and non-duplicating."""
        # 1. Generate type specifications
        specs_summary = generate_define_subagent_specs(self.work_dir)
        type_files = specs_summary.get("type_files", [])
        self.assertGreaterEqual(len(type_files), 5, "Expected at least 5 type definitions including c2c_cta_harmonizer")

        types_dir = self.work_dir / "dispatch" / "types"
        self.assertTrue(types_dir.is_dir())

        expected_types = {
            "c2c_cta_architect": "prompt_cta_architect.md",
            "c2c_shard_author": "prompt_shard_author.md",
            "c2c_judge": "prompt_blind_judge.md",
            "c2c_repair": "prompt_shard_author.md",
            "c2c_cta_harmonizer": "prompt_cta_harmonizer.md",
        }

        for type_name, prompt_filename in expected_types.items():
            type_file = types_dir / f"{type_name}.json"
            self.assertTrue(type_file.is_file(), f"Missing type spec file: {type_file}")
            raw_prompt = load_system_prompt(prompt_filename)

            spec_data = json.loads(type_file.read_text(encoding="utf-8"))
            self.assertEqual(spec_data["name"], type_name)
            self.assertEqual(
                spec_data["system_prompt"].strip(),
                raw_prompt.strip(),
                f"Type spec {type_name} must preserve 100% full uncompressed {prompt_filename}",
            )
            self.assertLess(type_file.stat().st_size, 46080)

        # 2. Setup fixtures for item prompt checks
        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "course_id": "macro_test",
            "cta_mode": "direct",
            "documents": [{"name": "textbook.pdf", "path": "content/textbook.pdf", "total_pages": 40, "valid_page_range": [1, 40]}],
        }), encoding="utf-8")

        distractors_c01 = [
            {"id": f"D-01-{i:02d}", "name": f"Distractor {i}", "wrong_belief": f"Falacia {i}", "omitted_step": "N/A"}
            for i in range(1, 7)
        ]
        cta_data = {
            "course_id": "macro_test",
            "competencies": [
                {
                    "id": "C-01",
                    "type": "concept",
                    "name": "Equilibrio Macroeconómico",
                    "description_latex": r"Condición $Y = C + I + G$",
                    "evidence": [{"doc": "textbook.pdf", "page": 12, "section": "1.2"}],
                    "distractors": distractors_c01,
                }
            ],
        }
        (self.work_dir / "cta.json").write_text(json.dumps(cta_data), encoding="utf-8")

        shards_dir = self.work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)
        (shards_dir / "pre_shard_manifest.json").write_text(json.dumps({
            "shards": [{"shard_id": "shard_01", "competency_ids": ["C-01"]}],
        }), encoding="utf-8")

        verif_dir = self.work_dir / "verification"
        verif_dir.mkdir(parents=True, exist_ok=True)
        (verif_dir / "judge_batch_01.json").write_text(json.dumps([
            {"question_id": "Q-01", "question_type": "multiple_choice", "stem_es": "Calcule Y", "options": [{"id": "A", "content": "100"}]},
        ]), encoding="utf-8")

        # 3. Assert compact non-duplicating item prompts for CTA
        cta_res = dispatch_cta(self.work_dir, mode="direct")
        cta_prompt = cta_res["Subagents"][0]["Prompt"]
        raw_cta = load_system_prompt("prompt_cta_architect.md")
        self.assertNotIn(raw_cta.strip(), cta_prompt)
        self.assertLess(len(cta_prompt), 3500)
        self.assertIn("SCOPE-LOCK", cta_prompt)
        self.assertIn("DONE:", cta_prompt)

        # 4. Assert compact non-duplicating item prompts for Authors
        author_res = dispatch_authors(self.work_dir)
        author_prompt = author_res["Subagents"][0]["Prompt"]
        raw_author = load_system_prompt("prompt_shard_author.md")
        self.assertNotIn(raw_author.strip(), author_prompt)
        self.assertLess(len(author_prompt), 4000)
        self.assertIn("SCOPE-LOCK", author_prompt)
        self.assertIn("DONE:", author_prompt)

        # 5. Assert compact non-duplicating item prompts for Judges
        judge_res = dispatch_judges(self.work_dir)
        judge_prompt = judge_res["Subagents"][0]["Prompt"]
        raw_judge = load_system_prompt("prompt_blind_judge.md")
        self.assertNotIn(raw_judge.strip(), judge_prompt)
        self.assertLess(len(judge_prompt), 3500)
        self.assertIn("SCOPE-LOCK", judge_prompt)
        self.assertIn("DONE:", judge_prompt)

        # 6. Assert compact non-duplicating item prompts for Repair
        (self.work_dir / "reports").mkdir(parents=True, exist_ok=True)
        (self.work_dir / "reports" / "templates_report.json").write_text(json.dumps({
            "results": [{"cid": "C-01", "status": "fail", "errors": ["AST violation"]}],
        }), encoding="utf-8")
        repair_res = dispatch_repair(self.work_dir)
        repair_prompt = repair_res["Subagents"][0]["Prompt"]
        self.assertNotIn(raw_author.strip(), repair_prompt)
        self.assertLess(len(repair_prompt), 3500)
        self.assertIn("SCOPE-LOCK", repair_prompt)
        self.assertIn("DONE:", repair_prompt)

        # 7. Assert compact non-duplicating item prompt for cta-reduce
        cta_parts_dir = self.work_dir / "cta_parts"
        cta_parts_dir.mkdir(parents=True, exist_ok=True)
        (cta_parts_dir / "part_01.json").write_text(json.dumps({"competencies": []}), encoding="utf-8")
        reduce_res = build_dispatch(role="cta-reduce", work_dir=self.work_dir)
        reduce_prompt = reduce_res["Subagents"][0]["Prompt"]
        raw_harmonizer = load_system_prompt("prompt_cta_harmonizer.md")
        self.assertNotIn(raw_harmonizer.strip(), reduce_prompt)
        self.assertLess(len(reduce_prompt), 3500)
        self.assertIn("SCOPE-LOCK", reduce_prompt)
        self.assertIn("DONE:", reduce_prompt)

    # =========================================================================
    # 2. Turn-0 Complete Context in dispatch_authors
    # =========================================================================
    def test_turn0_complete_context_in_dispatch_authors(self) -> None:
        """dispatch_authors injects competencies, quotas, LaTeX, sources, and all 6 distractors into author prompt."""
        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "course_id": "macro_test",
            "documents": [
                {"name": "capitulo_01.pdf", "path": "content/capitulo_01.pdf", "total_pages": 30, "valid_page_range": [1, 30]}
            ],
        }), encoding="utf-8")

        distractors_c01 = [
            {
                "id": f"D-01-{i:02d}",
                "name": f"Error Conceptual {i}",
                "wrong_belief": f"El estudiante asume que la propensión marginal es {i * 0.1}",
                "omitted_step": f"Omitir ajuste de tasa {i}",
                "common_misconception_warning": f"Alerta pedagógica {i}",
            }
            for i in range(1, 7)
        ]
        distractors_h01 = [
            {
                "id": f"D-02-{i:02d}",
                "name": f"Fallo en Derivación {i}",
                "wrong_belief": f"El estudiante confunde derivada parcial {i}",
                "omitted_step": f"Paso omitido en diferenciación {i}",
            }
            for i in range(1, 7)
        ]

        (self.work_dir / "cta.json").write_text(json.dumps({
            "course_id": "macro_test",
            "competencies": [
                {
                    "id": "C-01",
                    "type": "knowledge",
                    "name": "Multiplicador Keynesiano",
                    "description_latex": r"Calcular multiplicador $k = \frac{1}{1 - c(1 - t)}$",
                    "evidence": [{"doc": "capitulo_01.pdf", "page": 15, "section": "3.1"}],
                    "distractors": distractors_c01,
                },
                {
                    "id": "Hab-01",
                    "type": "skill",
                    "name": "Optimización Intertemporal",
                    "description_latex": r"Maximizar utilidad sujeta a $\sum c_t / (1+r)^t$",
                    "evidence": [{"doc": "capitulo_01.pdf", "page": 22, "section": "4.5"}],
                    "distractors": distractors_h01,
                },
            ],
        }), encoding="utf-8")

        shards_dir = self.work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)
        (shards_dir / "pre_shard_manifest.json").write_text(json.dumps({
            "shards": [
                {"shard_id": "shard_01", "competency_ids": ["C-01", "Hab-01"]},
            ],
        }), encoding="utf-8")

        res = dispatch_authors(self.work_dir, pointer=False)
        self.assertEqual(len(res["Subagents"]), 1)
        self.assertEqual(len(res["item_files"]), 1)

        item_path = Path(res["item_files"][0])
        self.assertTrue(item_path.is_file())
        self.assertLess(item_path.stat().st_size, 46080)

        prompt = res["Subagents"][0]["Prompt"]

        # Verify C-01 Turn-0 context
        self.assertIn("### Competencia: `C-01`", prompt)
        self.assertIn("Tipo:** `knowledge` (Cuota requerida: **20** reactivos)", prompt)
        self.assertIn("Multiplicador Keynesiano", prompt)
        self.assertIn(r"Calcular multiplicador $k = \frac{1}{1 - c(1 - t)}$", prompt)
        self.assertIn("`content/capitulo_01.pdf` (pág. 15, sección: '3.1')", prompt)
        for i in range(1, 7):
            self.assertIn(f"D-01-{i:02d}", prompt)
            self.assertIn(f"Error Conceptual {i}", prompt)
            self.assertIn(f"El estudiante asume que la propensión marginal es {i * 0.1}", prompt)
            self.assertIn(f"Omitir ajuste de tasa {i}", prompt)
            self.assertIn(f"Alerta pedagógica {i}", prompt)

        # Verify Hab-01 Turn-0 context
        self.assertIn("### Competencia: `Hab-01`", prompt)
        self.assertIn("Tipo:** `skill` (Cuota requerida: **30** reactivos)", prompt)
        self.assertIn("Optimización Intertemporal", prompt)
        self.assertIn(r"Maximizar utilidad sujeta a $\sum c_t / (1+r)^t$", prompt)
        for i in range(1, 7):
            self.assertIn(f"D-02-{i:02d}", prompt)
            self.assertIn(f"Fallo en Derivación {i}", prompt)
            self.assertIn(f"Paso omitido en diferenciación {i}", prompt)

        # Verify compilation contract & DONE signal
        self.assertIn("compile_shard.py", prompt)
        self.assertIn("--input", prompt)
        self.assertIn("--output", prompt)
        self.assertIn("DONE: work/shards/shard_01.json", prompt)

    # =========================================================================
    # 3. Robustness: cta.json formats (dict with mapping, dict with list, pure list)
    # =========================================================================
    def test_dispatch_authors_handles_all_cta_json_formats(self) -> None:
        """dispatch_authors cleanly parses cta.json whether competencies is a list, a dict mapping, or a top-level list."""
        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "course_id": "macro_test",
            "documents": [{"name": "doc.pdf", "path": "content/doc.pdf", "total_pages": 10}],
        }), encoding="utf-8")

        shards_dir = self.work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)
        (shards_dir / "pre_shard_manifest.json").write_text(json.dumps({
            "shards": [{"shard_id": "shard_01", "competency_ids": ["C-10"]}],
        }), encoding="utf-8")

        # Format A: competencies as dict mapping {"C-10": {...}}
        (self.work_dir / "cta.json").write_text(json.dumps({
            "competencies": {
                "C-10": {
                    "type": "concept",
                    "name": "Dict Mapping Competency",
                    "description_latex": "Definicion A",
                }
            }
        }), encoding="utf-8")
        res_a = dispatch_authors(self.work_dir, pointer=False)
        prompt_a = res_a["Subagents"][0]["Prompt"]
        self.assertIn("Dict Mapping Competency", prompt_a)
        self.assertIn("Definicion A", prompt_a)

        # Format B: top-level list of competencies
        (self.work_dir / "cta.json").write_text(json.dumps([
            {
                "id": "C-10",
                "type": "skill",
                "name": "List Top-level Competency",
                "description_latex": "Definicion B",
            }
        ]), encoding="utf-8")
        res_b = dispatch_authors(self.work_dir, pointer=False)
        prompt_b = res_b["Subagents"][0]["Prompt"]
        self.assertIn("List Top-level Competency", prompt_b)
        self.assertIn("Definicion B", prompt_b)

    # =========================================================================
    # 4. Scope-Lock Introspection Policy
    # =========================================================================
    def test_scope_lock_introspection_policy(self) -> None:
        """ROLE_SPECS author and repair forbid compile_shard.py in read, and strictly forbid check_templates, check_cta, src/validator."""
        # Author role
        author_spec = ROLE_SPECS["author"]
        self.assertIn(".agents/skills/content-to-course/compile_shard.py", author_spec["forbidden"])
        self.assertNotIn(".agents/skills/content-to-course/compile_shard.py", author_spec["read"])
        self.assertIn("work/shards/shard_fixes/<CID>.py", author_spec["write"])
        for forbidden_path in [
            ".agents/skills/content-to-course/check_templates.py",
            ".agents/skills/content-to-course/check_cta.py",
            "src/validator/**",
            "engine/*",
            "SKILL.md",
        ]:
            self.assertIn(forbidden_path, author_spec["forbidden"])

        # Repair role
        repair_spec = ROLE_SPECS["repair"]
        self.assertIn(".agents/skills/content-to-course/compile_shard.py", repair_spec["forbidden"])
        self.assertNotIn(".agents/skills/content-to-course/compile_shard.py", repair_spec["read"])
        self.assertIn("work/shards/shard_fixes/<CID>.py", repair_spec["write"])
        for forbidden_path in [
            ".agents/skills/content-to-course/check_templates.py",
            ".agents/skills/content-to-course/check_cta.py",
            "src/validator/**",
            "engine/*",
            "SKILL.md",
        ]:
            self.assertIn(forbidden_path, repair_spec["forbidden"])

        # Judge role
        judge_spec = ROLE_SPECS["judge"]
        self.assertIn("work/verification/judge_responses_*.json", judge_spec["write"])
        self.assertIn("judge_ground_truth.json", judge_spec["forbidden"])

        # Test scope_check detection
        shards_dir = self.work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)
        allowed_file = shards_dir / "shard_01_data.py"
        allowed_file.write_text("# clean author data\n", encoding="utf-8")
        is_clean, violations = scope_check(self.work_dir, "author", snapshot={})
        self.assertTrue(is_clean, f"Expected clean scope check, got: {violations}")

        disallowed_file = self.work_dir / "scratch" / "hack_script.py"
        disallowed_file.parent.mkdir(parents=True, exist_ok=True)
        disallowed_file.write_text("# unauthorized script\n", encoding="utf-8")
        is_clean_viol, violations_viol = scope_check(self.work_dir, "author", snapshot={})
        self.assertFalse(is_clean_viol)
        self.assertTrue(any("hack_script.py" in v for v in violations_viol))

    # =========================================================================
    # 5. dispatch_repair resolution from pre_shard_manifest.json
    # =========================================================================
    def test_dispatch_repair_resolution_from_pre_shard_manifest(self) -> None:
        """dispatch_repair maps failing competencies to shards via pre_shard_manifest.json even when shard_*.json has no competencies key."""
        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "course_id": "macro_test",
            "documents": [{"name": "book.pdf", "path": "content/book.pdf"}],
        }), encoding="utf-8")
        (self.work_dir / "cta.json").write_text(json.dumps({"course_id": "macro_test"}), encoding="utf-8")

        shards_dir = self.work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)
        # pre_shard_manifest maps C-01 to shard_01 and C-02 to shard_02
        (shards_dir / "pre_shard_manifest.json").write_text(json.dumps({
            "shards": [
                {"shard_id": "shard_01", "competency_ids": ["C-01"]},
                {"shard_id": "shard_02", "competency_ids": ["C-02"]},
            ]
        }), encoding="utf-8")

        # Shard JSONs deliberately omit the competencies list
        (shards_dir / "shard_01.json").write_text(json.dumps({"shard_id": "shard_01", "templates": []}), encoding="utf-8")
        (shards_dir / "shard_02.json").write_text(json.dumps({"shard_id": "shard_02", "templates": []}), encoding="utf-8")

        # Reports record failure for C-01 and discordance for C-02
        (self.work_dir / "reports").mkdir(parents=True, exist_ok=True)
        (self.work_dir / "reports" / "templates_report.json").write_text(json.dumps({
            "results": [{"cid": "C-01", "status": "fail", "errors": ["R-17 rationale missing"]}],
        }), encoding="utf-8")
        (self.work_dir / "judge_report.json").write_text(json.dumps({
            "disagreements": [{"cid": "C-02", "item_id": "Q-02-01", "reason": "Judge answered B vs Ground Truth A"}],
        }), encoding="utf-8")

        repair_payload = dispatch_repair(self.work_dir)
        subagents = repair_payload.get("Subagents", [])
        self.assertEqual(len(subagents), 2, "Expected 2 repair subagents for C-01 and C-02")

        c01_agent = next(s for s in subagents if "C-01" in s["Role"])
        c02_agent = next(s for s in subagents if "C-02" in s["Role"])

        # C-01 must be mapped to shard_01
        self.assertIn("shard_01", c01_agent["Prompt"])
        self.assertIn("R-17 rationale missing", c01_agent["Prompt"])
        self.assertIn("DONE: work/shards/shard_01.json", c01_agent["Prompt"])

        # C-02 must be mapped to shard_02
        self.assertIn("shard_02", c02_agent["Prompt"])
        self.assertIn("Judge answered B vs Ground Truth A", c02_agent["Prompt"])
        self.assertIn("DONE: work/shards/shard_02.json", c02_agent["Prompt"])

    # =========================================================================
    # 6. dispatch_judges Zero-Warmup payload and path consistency
    # =========================================================================
    def test_dispatch_judges_zero_warmup_and_path_consistency(self) -> None:
        """dispatch_judges writes out_target to verification/judge_responses_XX.json and includes in-prompt items."""
        verif_dir = self.work_dir / "verification"
        verif_dir.mkdir(parents=True, exist_ok=True)

        batch_items = [
            {
                "question_id": "Q-SOLOW-01",
                "question_type": "multiple_choice",
                "stem_es": "En el modelo de Solow, el ahorro es $sY$. Calcule k*.",
                "options": [
                    {"id": "A", "content": "$k^* = 4.0$"},
                    {"id": "B", "content": "$k^* = 5.0$"},
                ],
            },
            {
                "question_id": "Q-SOLOW-02",
                "question_type": "fill_in_the_blank",
                "stem_es": "Ingrese el valor numérico de la tasa de depreciación.",
                "options": [],
                "answer_contract": {
                    "expected_type": "float",
                    "decimal_places": 2,
                    "tolerance": 0.01,
                    "format_example": "0.05",
                },
            },
        ]
        (verif_dir / "judge_batch_01.json").write_text(json.dumps(batch_items), encoding="utf-8")

        res = dispatch_judges(self.work_dir, pointer=False)
        self.assertEqual(len(res["Subagents"]), 1)
        self.assertEqual(len(res["item_files"]), 1)

        item_path = Path(res["item_files"][0])
        self.assertTrue(item_path.is_file())
        self.assertLess(item_path.stat().st_size, 46080)

        prompt = res["Subagents"][0]["Prompt"]

        # Output target and DONE signal must point to verification/judge_responses_01.json
        expected_target = "work/verification/judge_responses_01.json"
        self.assertIn(f"- **Ruta de Salida Obligatoria:** `{expected_target}`", prompt)
        self.assertIn(f"DONE: {expected_target}", prompt)

        # In-prompt zero-warmup payload
        self.assertIn("Q-SOLOW-01", prompt)
        self.assertIn("En el modelo de Solow, el ahorro es $sY$. Calcule k*.", prompt)
        self.assertIn("Q-SOLOW-02", prompt)
        self.assertIn("answer_contract", prompt)
        self.assertIn("decimal_places", prompt)

        # Zero-warmup directives
        self.assertIn("NO EJECUTES `view_file`", prompt)
        self.assertIn("NO EJECUTES `run_command`", prompt)
        self.assertIn("1 SOLO TURNO", prompt)

        # Test pointer mode (v3.3 default)
        res_ptr = dispatch_judges(self.work_dir, pointer=True)
        prompt_ptr = res_ptr["Subagents"][0]["Prompt"]
        self.assertIn("judge_01.json", prompt_ptr)
        self.assertNotIn("NO EJECUTES `view_file`", prompt_ptr)
        self.assertIn(f"DONE: {expected_target}", prompt_ptr)


if __name__ == "__main__":
    unittest.main()
