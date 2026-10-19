"""Comprehensive Test Suite for Stream C: Orchestration, Watchdog & Evaluation Resilience.

Covers C2C Hardening Requirements:
- R5: Pointer-Prompt Protocol (lean static system prompts <= 5 KB, dynamic pointer work orders <= 300 B).
- R5: Swift-Dispatch SLA (ready-made Subagents array, heaviest unit first sorting).
- R5: Pre-Stage-5 Cleanup protocol (purging stale/errored subagents before verification).
- R5: Automated Budget Watchdog (transcript.jsonl parsing, turn runaway > 40, token runaway > 5M, script loops >= 5).
- R5: Stateful Resumption Checkpoints (work/state.json persistence and recovery across halts).
- R6.2: Native Batch Slicing (<= 12 items per judge, double-blind item evaluation).
- R6.2: Incomplete Evaluation Detection & Blind Re-dispatch in judge.py.
"""

from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict, List

SKILL_DIR = Path(__file__).parent.parent / ".agents" / "skills" / "content-to-course"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from budget_guard import (
    DEFAULT_MAX_SCRIPT_LOOPS,
    DEFAULT_MAX_TOKENS,
    DEFAULT_MAX_TURNS,
    SubagentMetrics,
    evaluate_watchdog_rules,
    generate_repair_redispatch,
    load_state_checkpoint,
    parse_transcript,
    scan_work_transcripts,
    update_state_checkpoint,
)
from dispatch import (
    build_dispatch,
    dispatch_authors,
    dispatch_cta,
    dispatch_judges,
    dispatch_repair,
    generate_define_subagent_specs,
    load_system_prompt,
    make_pointer_prompt,
    pre_stage5_cleanup,
)
from judge import (
    check_judge_completeness,
    emit_judge_redispatch,
    split_judge_batch,
)


class TestPointerPromptProtocol(unittest.TestCase):
    """Verifies R5 Lean System Prompts (<= 5 KB) and Dynamic Pointer Prompts (<= 300 B)."""

    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp(prefix="c2c_stream_c_pointer_")
        self.work_dir = Path(self.test_dir) / "work"
        self.work_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_lean_system_prompts_size_and_contract(self) -> None:
        """All lean static system prompts must be strictly <= 5120 bytes (5 KB)."""
        lean_dir = SKILL_DIR / "system_prompts" / "lean"
        self.assertTrue(lean_dir.is_dir(), f"Lean system prompts directory missing: {lean_dir}")

        expected_prompts = [
            "prompt_shard_author.md",
            "prompt_cta_architect.md",
            "prompt_blind_judge.md",
            "prompt_cta_harmonizer.md",
            "prompt_repair.md",
        ]

        for fname in expected_prompts:
            p_file = lean_dir / fname
            self.assertTrue(p_file.is_file(), f"Missing lean prompt: {fname}")
            size = p_file.stat().st_size
            self.assertLessEqual(
                size,
                5120,
                f"Lean prompt {fname} exceeds 5 KB limit! Size: {size} bytes",
            )
            content = p_file.read_text(encoding="utf-8")
            self.assertGreater(len(content.strip()), 100, f"Lean prompt {fname} appears empty or truncated")

    def test_load_system_prompt_lean_mode(self) -> None:
        """load_system_prompt respects lean=True and loads lean prompt version."""
        lean_author = load_system_prompt("prompt_shard_author.md", lean=True)
        orig_author = load_system_prompt("prompt_shard_author.md", lean=False)
        self.assertLess(len(lean_author.encode("utf-8")), len(orig_author.encode("utf-8")))
        self.assertLessEqual(len(lean_author.encode("utf-8")), 5120)

    def test_generate_define_subagent_specs_lean_mode(self) -> None:
        """generate_define_subagent_specs creates lean subagent definitions <= 5 KB each."""
        types_res = generate_define_subagent_specs(self.work_dir, lean=True)
        self.assertIn("types", types_res)
        for t_spec in types_res["types"]:
            sys_prompt = t_spec.get("system_prompt") or t_spec.get("SystemPrompt", "")
            type_name = t_spec.get("name") or t_spec.get("TypeName", "unknown")
            self.assertLessEqual(
                len(sys_prompt.encode("utf-8")),
                5120,
                f"Subagent type {type_name} system prompt exceeds 5 KB",
            )

    def test_make_pointer_prompt_under_300_bytes(self) -> None:
        """make_pointer_prompt generates a concise prompt <= 300 bytes referencing disk payload."""
        prompt = make_pointer_prompt(
            role="Shard Author C-01-01",
            item_file_rel="work/dispatch/items/author_item_01.json",
            done_signal="DONE: work/shards/shard_01.json",
        )
        prompt_bytes = len(prompt.encode("utf-8"))
        self.assertLessEqual(
            prompt_bytes,
            300,
            f"Pointer prompt exceeds 300 B SLA limit! Actual size: {prompt_bytes} bytes",
        )
        self.assertIn("author_item_01.json", prompt)
        self.assertIn("view_file", prompt)
        self.assertIn("DONE: work/shards/shard_01.json", prompt)

    def test_dispatch_authors_pointer_mode_creates_disk_items_and_lean_prompts(self) -> None:
        """dispatch_authors in pointer mode writes Turn-0 disk JSON and issues <=300 B prompts."""
        # Setup mock course work dir
        pre_shard_manifest = {
            "shards": [
                {
                    "shard_index": 1,
                    "competencies": ["C-01-01"],
                    "estimated_questions": 4,
                },
                {
                    "shard_index": 2,
                    "competencies": ["C-01-02", "C-01-03"],
                    "estimated_questions": 8,
                },
            ]
        }
        (self.work_dir / "pre_shard_manifest.json").write_text(
            json.dumps(pre_shard_manifest, indent=2), encoding="utf-8"
        )

        cta_data = {
            "competencies": [
                {
                    "id": "C-01-01",
                    "title": "Thermodynamic Work",
                    "description": "Calculate work done in isobaric process",
                    "distractors": [{"id": "D-01-01", "wrong_belief": "used V instead of delta V"}],
                },
                {
                    "id": "C-01-02",
                    "title": "Heat Transfer",
                    "description": "Calculate conduction through a composite slab",
                    "distractors": [{"id": "D-01-02", "wrong_belief": "inverted thermal conductivity"}],
                },
                {
                    "id": "C-01-03",
                    "title": "Entropy",
                    "description": "Calculate entropy change in reversible process",
                    "distractors": [{"id": "D-01-03", "wrong_belief": "used Celsius instead of Kelvin"}],
                },
            ]
        }
        (self.work_dir / "cta.json").write_text(json.dumps(cta_data, indent=2), encoding="utf-8")

        res = dispatch_authors(self.work_dir, pointer=True)
        self.assertIn("Subagents", res)
        subagents = res["Subagents"]
        self.assertEqual(len(subagents), 2)

        # Heaviest shard first SLA: Shard 2 (8 questions) should be dispatched before Shard 1 (4 questions)
        self.assertIn("shard_02", subagents[0]["Role"].lower())
        self.assertIn("shard_01", subagents[1]["Role"].lower())

        # Check prompt sizes and disk files
        for sub in subagents:
            prompt_bytes = len(sub["Prompt"].encode("utf-8"))
            self.assertLessEqual(
                prompt_bytes,
                300,
                f"Author pointer prompt exceeds 300 B: {prompt_bytes} bytes",
            )
            self.assertIn("work/dispatch/items/author_", sub["Prompt"])

        # Check that disk items exist and contain Turn-0 payload
        item1 = self.work_dir / "dispatch" / "items" / "author_01.json"
        item2 = self.work_dir / "dispatch" / "items" / "author_02.json"
        self.assertTrue(item1.is_file(), "Author item 01 missing on disk")
        self.assertTrue(item2.is_file(), "Author item 02 missing on disk")

        content1 = json.loads(item1.read_text(encoding="utf-8"))
        self.assertIn("assigned_competencies", content1)
        self.assertIn("compile_command", content1)
        self.assertIn("work_order", content1)

    def test_dispatch_cta_mapreduce_heaviest_first_and_pointer(self) -> None:
        """dispatch_cta in mapreduce mode sorts heaviest unit first and writes pointer orders."""
        pre_cta = {
            "mode": "mapreduce",
            "parts": [
                {"part_index": 1, "title": "Intro", "slide_count": 5},
                {"part_index": 2, "title": "Core Mechanics", "slide_count": 35},
                {"part_index": 3, "title": "Advanced", "slide_count": 18},
            ],
        }
        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps(pre_cta, indent=2), encoding="utf-8")

        res = dispatch_cta(self.work_dir, pointer=True)
        subagents = res["Subagents"]
        self.assertEqual(len(subagents), 3)

        # Heaviest unit first: Part 2 (35 slides), then Part 3 (18 slides), then Part 1 (5 slides)
        self.assertIn("part_02", subagents[0]["Role"].lower())
        self.assertIn("part_03", subagents[1]["Role"].lower())
        self.assertIn("part_01", subagents[2]["Role"].lower())

        # Check pointer prompt size
        for sub in subagents:
            prompt_bytes = len(sub["Prompt"].encode("utf-8"))
            self.assertLessEqual(prompt_bytes, 300)
            self.assertIn("cta_", sub["Prompt"])


class TestJudgeNativeBatching(unittest.TestCase):
    """Verifies R6.2 Native Batch Slicing (<= 12 items) and Incomplete Evaluation Detection."""

    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp(prefix="c2c_stream_c_judge_")
        self.work_dir = Path(self.test_dir) / "work"
        self.work_dir.mkdir(parents=True, exist_ok=True)
        self.verif_dir = self.work_dir / "verification"
        self.verif_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_split_judge_batch_strict_limit_12(self) -> None:
        """split_judge_batch splits items into slices of at most 12 items."""
        raw_items = [{"id": f"Q-{i:02d}", "question": f"Question {i}"} for i in range(1, 31)]
        batches = split_judge_batch(raw_items, max_items_per_judge=12)
        # 30 items -> [12, 12, 6]
        self.assertEqual(len(batches), 3)
        self.assertEqual(len(batches[0]), 12)
        self.assertEqual(len(batches[1]), 12)
        self.assertEqual(len(batches[2]), 6)

    def test_dispatch_judges_pointer_mode_and_blind_integrity(self) -> None:
        """dispatch_judges creates batches <= 12 items with blind items (no answer/canonical code)."""
        shards_dir = self.work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)

        questions = []
        for i in range(1, 16):
            questions.append({
                "id": f"C-01-{i:02d}",
                "prompt": f"Solve problem {i}",
                "code": f"ans = {i} * 2",  # Should be stripped for blind judge!
                "canonical_solution": f"{i*2}",  # Should be stripped!
                "distractors": [{"id": f"D-01-{i:02d}", "text": "wrong"}],
            })

        shard_payload = {"questions": questions}
        (shards_dir / "shard_01.json").write_text(json.dumps(shard_payload, indent=2), encoding="utf-8")

        res = dispatch_judges(self.work_dir, pointer=True, max_items_per_judge=12)
        subagents = res["Subagents"]

        # 15 items sliced into Batch 1 (12 items) and Batch 2 (3 items) -> 2 subagents total
        self.assertEqual(len(subagents), 2)

        # Verify pointer prompt sizes
        for sub in subagents:
            prompt_bytes = len(sub["Prompt"].encode("utf-8"))
            self.assertLessEqual(prompt_bytes, 300)
            self.assertIn("judge_", sub["Prompt"])

        # Check that disk items are strictly blind (no 'code' or 'canonical_solution')
        judge_items_dir = self.work_dir / "dispatch" / "items"
        for item_path in judge_items_dir.glob("judge_*.json"):
            item_data = json.loads(item_path.read_text(encoding="utf-8"))
            self.assertIn("items", item_data)
            self.assertLessEqual(len(item_data["items"]), 12)
            for itm in item_data["items"]:
                self.assertNotIn("code", itm, "Leak: code present in blind judge item!")
                self.assertNotIn("canonical_solution", itm, "Leak: solution in blind judge item!")

    def test_check_judge_completeness_and_redispatch(self) -> None:
        """check_judge_completeness detects missing evaluations and emit_judge_redispatch slices them."""
        # Expected 6 items
        all_items = [{"id": f"C-01-{i:02d}", "prompt": f"Q {i}"} for i in range(1, 7)]
        (self.verif_dir / "judge_batch_01.json").write_text(json.dumps(all_items, indent=2), encoding="utf-8")

        # Judge 1 only evaluated items 1 to 3 (items 4, 5, 6 missing/truncated)
        judge_1_resp = {
            "evaluations": [
                {"id": "C-01-01", "verdict": "pass"},
                {"id": "C-01-02", "verdict": "pass"},
                {"id": "C-01-03", "verdict": "pass"},
            ]
        }
        # Judge 2 evaluated items 1 to 3
        judge_2_resp = {
            "evaluations": [
                {"id": "C-01-01", "verdict": "pass"},
                {"id": "C-01-02", "verdict": "pass"},
                {"id": "C-01-03", "verdict": "pass"},
            ]
        }
        (self.verif_dir / "judge_responses_01.json").write_text(json.dumps(judge_1_resp, indent=2), encoding="utf-8")
        (self.verif_dir / "judge_responses_02.json").write_text(json.dumps(judge_2_resp, indent=2), encoding="utf-8")

        status = check_judge_completeness(self.work_dir)
        self.assertFalse(status["is_complete"])
        self.assertIn("C-01-04", status["missing_ids"])
        self.assertIn("C-01-05", status["missing_ids"])
        self.assertIn("C-01-06", status["missing_ids"])

        # Emit re-dispatch for missing items
        redispatch_res = emit_judge_redispatch(self.work_dir, max_items_per_judge=12)
        self.assertEqual(redispatch_res["missing_count"], 3)
        self.assertIn("Subagents", redispatch_res)
        self.assertGreaterEqual(len(redispatch_res["Subagents"]), 2)  # At least 2 judges for the missing batch


class TestBudgetWatchdog(unittest.TestCase):
    """Verifies R5 Automated Budget Watchdog (budget_guard.py)."""

    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp(prefix="c2c_stream_c_watchdog_")
        self.work_dir = Path(self.test_dir) / "work"
        self.work_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_watchdog_detects_turn_runaway(self) -> None:
        """Watchdog flags subagent with > 40 turns as runaway."""
        metrics = SubagentMetrics(
            subagent_id="author_subagent_1",
            role="c2c_shard_author",
            transcript_path="dummy",
            turn_count=42,
            total_tokens=100_000,
            is_completed=False,
        )
        report = evaluate_watchdog_rules(metrics, max_turns=40, max_tokens=5_000_000)
        self.assertTrue(report.is_runaway)
        self.assertEqual(report.recommended_action, "kill_and_redispatch")
        self.assertTrue(any("Turn count 42 exceeds SLA limit 40" in r for r in report.runaway_reasons))

    def test_watchdog_detects_token_runaway(self) -> None:
        """Watchdog flags subagent with > 5M tokens as runaway."""
        metrics = SubagentMetrics(
            subagent_id="author_subagent_2",
            role="c2c_shard_author",
            transcript_path="dummy",
            turn_count=15,
            total_tokens=5_250_000,
            is_completed=False,
        )
        report = evaluate_watchdog_rules(metrics, max_turns=40, max_tokens=5_000_000)
        self.assertTrue(report.is_runaway)
        self.assertEqual(report.recommended_action, "kill_and_redispatch")
        self.assertTrue(any("Token burn 5,250,000 exceeds SLA limit" in r for r in report.runaway_reasons))

    def test_watchdog_detects_script_looping(self) -> None:
        """Watchdog flags subagent with >= 5 consecutive script failures as runaway."""
        metrics = SubagentMetrics(
            subagent_id="author_subagent_3",
            role="c2c_shard_author",
            transcript_path="dummy",
            turn_count=12,
            total_tokens=200_000,
            max_consecutive_script_failures=6,
            is_completed=False,
        )
        report = evaluate_watchdog_rules(metrics, max_script_loops=5)
        self.assertTrue(report.is_runaway)
        self.assertEqual(report.recommended_action, "kill_and_redispatch")
        self.assertTrue(any("Script loop detected" in r for r in report.runaway_reasons))

    def test_watchdog_parses_real_transcript_and_ignores_completed(self) -> None:
        """Watchdog parses jsonl transcript entries and recognizes completion signal."""
        t_file = self.work_dir / "transcript.jsonl"
        lines = [
            json.dumps({"role": "system", "content": "You are Shard Author"}),
            json.dumps({"role": "assistant", "content": "Working...", "usage": {"input_tokens": 1000, "output_tokens": 500}}),
            json.dumps({"role": "tool", "tool": "run_command", "args": {"CommandLine": "python compile_shard.py"}}),
            json.dumps({"role": "tool_output", "output": "Compilation error line 10", "exit_code": 1}),
            json.dumps({"role": "assistant", "content": "Fixed! DONE: work/shards/shard_01.json", "usage": {"input_tokens": 800, "output_tokens": 400}}),
        ]
        t_file.write_text("\n".join(lines), encoding="utf-8")

        metrics = parse_transcript(t_file)
        self.assertEqual(metrics.turn_count, 2)
        self.assertEqual(metrics.total_tokens, 2700)
        self.assertTrue(metrics.is_completed)
        self.assertIn("shard_01.json", metrics.completion_signal or "")

        report = evaluate_watchdog_rules(metrics)
        self.assertFalse(report.is_runaway)
        self.assertEqual(report.recommended_action, "completed")

    def test_generate_repair_redispatch_for_unfinished_units(self) -> None:
        """generate_repair_redispatch identifies unfinished competencies and emits c2c_repair."""
        # Setup course work dir with CTA having C-01-01 and C-01-02
        cta_data = {
            "competencies": [
                {"id": "C-01-01", "title": "Fluid Dynamics"},
                {"id": "C-01-02", "title": "Bernoulli Principle"},
            ]
        }
        (self.work_dir / "cta.json").write_text(json.dumps(cta_data, indent=2), encoding="utf-8")

        # Shard 01 has C-01-01 completed
        shards_dir = self.work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)
        shard_data = {"questions": [{"id": "C-01-01", "prompt": "Fluid problem"}]}
        (shards_dir / "shard_01.json").write_text(json.dumps(shard_data, indent=2), encoding="utf-8")
        # C-01-02 is NOT in shards/ -> Unfinished!

        # Fake runaway subagent report
        runaway_metrics = SubagentMetrics(
            subagent_id="author_shard_2",
            role="c2c_shard_author",
            transcript_path="dummy",
            turn_count=45,
            is_completed=False,
            assigned_competency_ids=["C-01-02"],
        )
        from budget_guard import SubagentWatchdogReport
        runaway_report = SubagentWatchdogReport(
            subagent_id="author_shard_2",
            role="c2c_shard_author",
            unit_id="shard_02",
            is_runaway=True,
            runaway_reasons=["Turn count 45 exceeds 40"],
            metrics=runaway_metrics,
            recommended_action="kill_and_redispatch",
        )

        res = generate_repair_redispatch(self.work_dir, [runaway_report])
        self.assertEqual(res["unfinished_count"], 1)
        subagents = res["Subagents"]
        self.assertEqual(len(subagents), 1)
        self.assertEqual(subagents[0]["TypeName"], "c2c_repair")
        self.assertIn("C-01-02", subagents[0]["Role"])
        self.assertIn("watchdog_repair_", subagents[0]["Prompt"])


class TestStatefulResumptionAndCleanup(unittest.TestCase):
    """Verifies R5 Resumption Checkpoints (state.json) and Pre-Stage-5 Cleanup."""

    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp(prefix="c2c_stream_c_resumption_")
        self.work_dir = Path(self.test_dir) / "work"
        self.work_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_state_checkpoint_lifecycle(self) -> None:
        """state.json records stages and survives cross-process checkpointing."""
        st1 = update_state_checkpoint(self.work_dir, "stage1_plan", "completed", {"units": 4})
        self.assertEqual(st1["current_stage"], "stage1_plan")
        self.assertEqual(st1["stages"]["stage1_plan"]["status"], "completed")

        st2 = update_state_checkpoint(self.work_dir, "stage2_cta", "in_progress")
        self.assertEqual(st2["current_stage"], "stage2_cta")
        self.assertEqual(st2["stages"]["stage1_plan"]["status"], "completed")
        self.assertEqual(st2["stages"]["stage2_cta"]["status"], "in_progress")

        # Load back independently
        loaded = load_state_checkpoint(self.work_dir)
        self.assertEqual(loaded["current_stage"], "stage2_cta")
        self.assertIn("stage1_plan", loaded["stages"])

    def test_pre_stage5_cleanup_purges_errored_subagents(self) -> None:
        """pre_stage5_cleanup purges transient 429/aborted subagent records."""
        # Setup initial state with an errored subagent
        init_state = {
            "current_stage": "stage4_repair",
            "stages": {"stage4_repair": {"status": "completed"}},
            "subagents": {
                "author_01": {"status": "completed"},
                "author_02_429": {"status": "errored", "error": "Rate limit 429 encountered"},
            },
        }
        (self.work_dir / "state.json").write_text(json.dumps(init_state, indent=2), encoding="utf-8")

        res = pre_stage5_cleanup(self.work_dir)
        self.assertEqual(res["status"], "ok")
        self.assertIn("author_02_429", res["purged"])

        # Check state.json updated
        updated_state = load_state_checkpoint(self.work_dir)
        self.assertEqual(updated_state["subagents"]["author_02_429"]["status"], "purged_pre_stage5")
        self.assertIn("pre_stage5_cleanup", updated_state["stages"])


if __name__ == "__main__":
    unittest.main()
