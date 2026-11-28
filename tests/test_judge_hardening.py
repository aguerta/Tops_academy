"""Focused hardening tests for judge.py (Stream 1C - pipeline_hardening_v7)."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

SKILL_DIR = Path(__file__).resolve().parent.parent / ".agents" / "skills" / "content-to-course"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from judge import (  # noqa: E402
    MC7_STEM_SOLUBILITY_INSTRUCTIONS,
    _build_mc7_judge_contract,
    compare_judge_responses,
    compute_proportional_judge_budget,
    generate_judge_batch,
    resolve_neuro_symbolic_verdict,
)


class TestKernelOverrideAntiFalseConsensus:
    """Tests the 3 anti-false-consensus guards in resolve_neuro_symbolic_verdict & compare_judge_responses."""

    def test_guard_a_fib_integer_rounding_diff_one_blocks_override(self):
        res = resolve_neuro_symbolic_verdict(
            kernel_verified=True,
            kernel_refuted=False,
            llm_verdict="FAIL",
            failure_category="calculation_error",
            failure_reasons=["Judge calculated 10 (ceil) vs expected 9 (round)"],
            interaction_type="fill_in_the_blank",
            solver_answer="10",
            correct_answer="9",
        )
        assert res["verdict"] == "FAIL"
        assert res["passed"] is False
        assert res["kernel_override"] is False

    def test_guard_a_mc7_numeric_integer_rounding_diff_one_blocks_override(self):
        res = resolve_neuro_symbolic_verdict(
            kernel_verified=True,
            kernel_refuted=False,
            llm_verdict="FAIL",
            failure_category="math_error",
            failure_reasons=["Numeric mismatch"],
            interaction_type="multiple_choice_7_options",
            solver_answer=41.0,
            correct_answer=42.0,
        )
        assert res["verdict"] == "FAIL"
        assert res["passed"] is False
        assert res["kernel_override"] is False

    def test_guard_a_allows_override_when_diff_is_not_integer_rounding_one(self):
        res = resolve_neuro_symbolic_verdict(
            kernel_verified=True,
            kernel_refuted=False,
            llm_verdict="FAIL",
            failure_category="math_error",
            failure_reasons=["Minor decimal drift 10.05 vs 10.00"],
            interaction_type="fill_in_the_blank",
            solver_answer="10.05",
            correct_answer="10.00",
        )
        assert res["verdict"] == "PASS"
        assert res["passed"] is True
        assert res["kernel_override"] is True

    def test_guard_b_multiple_select_rejection_blocks_override(self):
        res = resolve_neuro_symbolic_verdict(
            kernel_verified=True,
            kernel_refuted=False,
            llm_verdict="FAIL",
            failure_category="calculation_error",
            failure_reasons=["Judge rejected option C"],
            interaction_type="multiple_select",
            solver_answer=["A", "B"],
            correct_answer=["A", "B", "C"],
        )
        assert res["verdict"] == "FAIL"
        assert res["passed"] is False
        assert res["kernel_override"] is False

    def test_guard_c_two_or_more_failed_seeds_blocks_override(self):
        res = resolve_neuro_symbolic_verdict(
            kernel_verified=True,
            kernel_refuted=False,
            llm_verdict="FAIL",
            failure_category="calculation_error",
            failure_reasons=["Stochastic arithmetic error"],
            interaction_type="fill_in_the_blank",
            solver_answer="15.4",
            correct_answer="12.0",
            template_failed_seeds=2,
        )
        assert res["verdict"] == "FAIL"
        assert res["passed"] is False
        assert res["kernel_override"] is False

    def test_compare_judge_responses_blocks_override_on_multi_seed_failures_and_rounding(self):
        gt = {
            "T1_judge_1": {
                "item_id": "T1_judge_1",
                "template_id": "T1",
                "competency_id": "C1",
                "interaction_type": "fill_in_the_blank",
                "correct_value": "10",
                "tolerance": 0.01,
                "kernel_verified": True,
                "kernel_refuted": False,
            },
            "T1_judge_2": {
                "item_id": "T1_judge_2",
                "template_id": "T1",
                "competency_id": "C1",
                "interaction_type": "fill_in_the_blank",
                "correct_value": "20",
                "tolerance": 0.01,
                "kernel_verified": True,
                "kernel_refuted": False,
            },
            "T2_judge_1": {
                "item_id": "T2_judge_1",
                "template_id": "T2",
                "competency_id": "C2",
                "interaction_type": "fill_in_the_blank",
                "correct_value": "8",
                "tolerance": 0.01,
                "kernel_verified": True,
                "kernel_refuted": False,
            },
        }
        responses = {
            "T1_judge_1": "15",  # non-rounding diff, but T1 has 2 failed seeds
            "T1_judge_2": "25",
            "T2_judge_1": "9",   # integer rounding diff == 1.0
        }
        report = compare_judge_responses(responses=responses, ground_truth=gt)
        assert report["passed"] is False
        assert report["kernel_override_count"] == 0
        assert "T1" in report["failed_templates"]
        assert "T2" in report["failed_templates"]


class TestMC7StemSolubilityContract:
    """Tests MC7 stem-only derivation schema and flaw_detected enforcement."""

    def test_mc7_contract_requires_derived_value_from_stem_only_and_flaw_detected(self):
        contract = _build_mc7_judge_contract(has_numeric_options=True)
        assert contract["requires_stem_only_derivation"] is True
        assert contract["has_numeric_options"] is True
        assert "derived_value_from_stem_only" in MC7_STEM_SOLUBILITY_INSTRUCTIONS
        assert "flaw_detected" in MC7_STEM_SOLUBILITY_INSTRUCTIONS
        schema = contract["response_schema"]
        assert "symbolic_formula" in schema
        assert "derived_value_from_stem_only" in schema
        assert "flaw_detected" in schema

    def test_generate_judge_batch_attaches_mc7_solubility_contract(self, tmp_path: Path):
        tpl_path = tmp_path / "templates.json"
        work_dir = tmp_path / "work"
        template = {
            "id": "T_MC7_01",
            "competency_id": "C_01",
            "interaction_type": "multiple_choice_7_options",
            "stem": "Calculate 2 + @x@.",
            "hints": ["Hint 1", "Hint 2", "Hint 3"],
            "solution": "The sum is 2 + @x@.",
            "generate_py": (
                "def generate(rng):\n"
                "    x = rng.randint(1, 5)\n"
                "    ans = 2 + x\n"
                "    return {\n"
                "        'vars': {'x': x},\n"
                "        'correct': str(ans),\n"
                "        'distractors': [\n"
                "            {'value': str(ans + i), 'distractor_id': f'D-0{i}', 'error_rationale': f'off by {i}'}\n"
                "            for i in range(1, 7)\n"
                "        ],\n"
                "    }\n"
            ),
            "verifier_code": (
                "def verify(res):\n"
                "    return int(res['correct']) == 2 + int(res['vars']['x'])\n"
            ),
        }
        tpl_path.write_text(json.dumps([template]), encoding="utf-8")

        batch_p, _ = generate_judge_batch(
            templates_path=tpl_path,
            work_dir=work_dir,
            samples_per_template=1,
        )
        batch = json.loads(batch_p.read_text(encoding="utf-8"))
        assert len(batch) == 1
        item = batch[0]
        assert item["interaction_type"] == "multiple_choice_7_options"
        assert "judge_instructions" in item
        assert "derived_value_from_stem_only" in item["judge_instructions"]
        assert "response_schema" in item
        assert "symbolic_formula" in item["response_schema"]
        assert "derived_value_from_stem_only" in item["response_schema"]
        assert "flaw_detected" in item["response_schema"]
        assert item["answer_contract"]["has_numeric_options"] is True

    def test_mc7_flaw_detected_from_reverse_engineering_blocks_kernel_override(self):
        gt = {
            "T_MC7_judge_1": {
                "item_id": "T_MC7_judge_1",
                "template_id": "T_MC7",
                "competency_id": "C1",
                "interaction_type": "multiple_choice_7_options",
                "correct_letter": "A",
                "correct_content": "42",
                "kernel_verified": True,
                "kernel_refuted": False,
            }
        }
        responses = [
            {
                "item_id": "T_MC7_judge_1",
                "symbolic_formula": "N/A",
                "derived_value_from_stem_only": None,
                "answer": "A",
                "flaw_detected": True,
                "flaw_description": "Stem omits definition of alpha; requires reverse-engineering from options A..G",
            }
        ]
        report = compare_judge_responses(responses=responses, ground_truth=gt)
        assert report["passed"] is False
        assert report["kernel_override_count"] == 0
        assert "T_MC7" in report["failed_templates"]


class TestRoundsHistoryAndRound1Preservation:
    """Tests immutable judge_report_round_1.json backup and rounds_history tracking."""

    def _make_gt(self):
        return {
            "T1_judge_1": {
                "item_id": "T1_judge_1",
                "template_id": "T1",
                "competency_id": "shard_01",
                "interaction_type": "fill_in_the_blank",
                "correct_value": "10",
                "tolerance": 0.01,
                "kernel_verified": False,
                "kernel_refuted": False,
            }
        }

    def test_preserves_round_1_report_and_tracks_rounds_history(self, tmp_path: Path):
        work_dir = tmp_path / "work"
        work_dir.mkdir(parents=True)
        gt = self._make_gt()

        # Round 1: fails without --shards
        r1 = compare_judge_responses(
            responses={"T1_judge_1": "99"},
            ground_truth=gt,
            cycle=1,
            work_dir=work_dir,
        )
        assert r1["passed"] is False
        assert len(r1["rounds_history"]) == 1
        assert r1["rounds_history"][0]["round"] == 1
        assert r1["rounds_history"][0]["passed"] is False
        assert not (work_dir / "judge_report_round_1.json").exists()

        round_1_snapshot_before = (work_dir / "judge_report.json").read_text(encoding="utf-8")

        # Round 2: partial re-judge with shards -> must backup round 1 immutably
        r2 = compare_judge_responses(
            responses={"T1_judge_1": "10"},
            ground_truth=gt,
            cycle=2,
            work_dir=work_dir,
            shards=["shard_01"],
        )
        round_1_file = work_dir / "judge_report_round_1.json"
        assert round_1_file.is_file()
        assert round_1_file.read_text(encoding="utf-8") == round_1_snapshot_before

        assert r2["passed"] is True
        assert len(r2["rounds_history"]) == 2
        assert r2["rounds_history"][0]["round"] == 1
        assert r2["rounds_history"][0]["passed"] is False
        assert r2["rounds_history"][1]["round"] == 2
        assert r2["rounds_history"][1]["passed"] is True
        assert r2["rounds_history"][1]["rejudged_shards"] == ["shard_01"]

        # Round 3: subsequent re-judge must NOT overwrite judge_report_round_1.json
        r3 = compare_judge_responses(
            responses={"T1_judge_1": "10"},
            ground_truth=gt,
            cycle=3,
            work_dir=work_dir,
            shards=["shard_02"],
        )
        assert round_1_file.read_text(encoding="utf-8") == round_1_snapshot_before
        assert len(r3["rounds_history"]) == 3
        assert r3["rounds_history"][2]["round"] == 3
        assert r3["rounds_history"][2]["rejudged_shards"] == ["shard_02"]

    def test_cli_compare_accepts_shards_flag(self, tmp_path: Path):
        work_dir = tmp_path / "work"
        work_dir.mkdir(parents=True)
        gt = self._make_gt()
        (work_dir / "judge_ground_truth.json").write_text(json.dumps(gt), encoding="utf-8")

        # Seed a Round 1 judge_report.json
        round_1_payload = {
            "cycle": 1,
            "passed": False,
            "failed_templates": ["T1"],
            "failed_competencies": ["shard_01"],
        }
        (work_dir / "judge_report.json").write_text(json.dumps(round_1_payload), encoding="utf-8")

        resp_p = work_dir / "judge_responses_1.json"
        resp_p.write_text(json.dumps({"T1_judge_1": "10"}), encoding="utf-8")

        proc = subprocess.run(
            [
                sys.executable,
                str(SKILL_DIR / "judge.py"),
                "compare",
                "--work-dir",
                str(work_dir),
                "--responses",
                str(resp_p),
                "--cycle",
                "2",
                "--shards",
                "shard_01",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        assert proc.returncode == 0, proc.stderr
        assert (work_dir / "judge_report_round_1.json").is_file()
        final_report = json.loads((work_dir / "judge_report.json").read_text(encoding="utf-8"))
        assert len(final_report["rounds_history"]) == 2
        assert final_report["rounds_history"][1]["rejudged_shards"] == ["shard_01"]

    @pytest.mark.parametrize("m20_type", ["proof_dag", "unstructured_model", "adversarial_break", "concept_matching"])
    @pytest.mark.parametrize("cat", ["", "math_error"])
    def test_guard_d_structured_m20_blocks_kernel_override(self, m20_type: str, cat: str):
        res = resolve_neuro_symbolic_verdict(
            kernel_verified=True,
            kernel_refuted=False,
            llm_verdict="FAIL",
            failure_category=cat,
            failure_reasons=["Disagreement on structured M20 item"],
            interaction_type=m20_type,
        )
        assert res["verdict"] == "FAIL"
        assert res["passed"] is False
        assert res["kernel_override"] is False

    @pytest.mark.parametrize(
        "total_templates,expected",
        [
            (276, (143, 165, 10)),
            (320, (143, 165, 10)),
            (321, (145, 167, 10)),
            (400, (180, 207, 11)),
            (600, (220, 253, 13)),
        ],
    )
    def test_p2_3_compute_proportional_judge_budget(self, total_templates: int, expected: tuple):
        assert compute_proportional_judge_budget(total_templates) == expected
