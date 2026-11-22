import json
import sys
from pathlib import Path

import pytest


AUDITOR_SCRIPTS_DIR = (
    Path(__file__).resolve().parents[2]
    / ".agents"
    / "skills"
    / "c2c-run-auditor"
    / "scripts"
)
if str(AUDITOR_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(AUDITOR_SCRIPTS_DIR))

from audit_engine import ExecutionAuditor  # noqa: E402


def _run_stage_5(tmp_path: Path, judge_report: dict) -> dict:
    work_dir = tmp_path / "work"
    work_dir.mkdir(parents=True, exist_ok=True)
    (work_dir / "judge_report.json").write_text(
        json.dumps(judge_report), encoding="utf-8"
    )
    auditor = ExecutionAuditor(root_records=[], root_conv_id="conv-test-1d")
    workload = {
        "work_dir": str(work_dir),
        "competencies_count": 6,
        "telemetry_snapshots": [],
    }
    stages = auditor._build_stage_deep_dives(
        subagents=[],
        orch_time={},
        workload=workload,
        interventions=[],
        records=[],
    )
    return stages["stage_5_judges"]


def test_round_1_failed_not_masked_by_post_rejudge_top_level(tmp_path: Path) -> None:
    """Top-level post-rejudge judge_report.json must not mask Round 1 failures in rounds_history."""
    judge_report = {
        "passed": True,
        "agreement_rate": 1.0,
        "total_items": 12,
        "disagreements": [],
        "rounds_history": [
            {"round": 1, "passed": False, "failed": 12},
        ],
    }

    s5 = _run_stage_5(tmp_path, judge_report)

    assert s5["round_1_discrepancies_count"] == 12
    assert s5["round_1_passed"] is False
    assert s5["passed_first_attempt"] is False
    assert s5["has_rejudge"] is True
    assert s5["final_passed"] is True
    assert "12 discrepancia(s)" in s5["summary_desc"]
    assert "APROBADO POST-REJUDGE" in s5["badge"]


def test_round_1_failed_with_disagreements_list_and_multiple_rounds(tmp_path: Path) -> None:
    """Round 1 disagreements list is counted when failed key is absent across multiple rounds."""
    judge_report = {
        "passed": True,
        "agreement_rate": 1.0,
        "total_items": 10,
        "disagreements": [],
        "rounds_history": [
            {
                "round": 1,
                "passed": False,
                "disagreements": [{"id": "q1"}, {"id": "q2"}, {"id": "q3"}],
                "agreement_rate": 0.7,
            },
            {
                "round": 2,
                "passed": True,
                "disagreements": [],
                "agreement_rate": 1.0,
            },
        ],
    }

    s5 = _run_stage_5(tmp_path, judge_report)

    assert s5["round_1_discrepancies_count"] == 3
    assert s5["round_1_passed"] is False
    assert s5["round_1_agreement_rate"] == pytest.approx(0.7)
    assert s5["passed_first_attempt"] is False
    assert s5["has_rejudge"] is True
    assert s5["final_passed"] is True


def test_round_1_passed_clean_first_attempt(tmp_path: Path) -> None:
    """Clean Round 1 in rounds_history with 0 discrepancies passes on first attempt."""
    judge_report = {
        "passed": True,
        "agreement_rate": 1.0,
        "total_items": 10,
        "disagreements": [],
        "rounds_history": [
            {"round": 1, "passed": True, "failed": 0, "agreement_rate": 1.0},
        ],
    }

    s5 = _run_stage_5(tmp_path, judge_report)

    assert s5["round_1_discrepancies_count"] == 0
    assert s5["round_1_passed"] is True
    assert s5["passed_first_attempt"] is True
    assert s5["has_rejudge"] is False
    assert s5["final_passed"] is True


def test_round_1_passed_false_with_zero_failed_blocks_first_attempt(tmp_path: Path) -> None:
    """Even if failed == 0, passed=False in Round 1 must prevent passed_first_attempt=True."""
    judge_report = {
        "passed": True,
        "agreement_rate": 1.0,
        "total_items": 10,
        "disagreements": [],
        "rounds_history": [
            {"round": 1, "passed": False, "failed": 0},
        ],
    }

    s5 = _run_stage_5(tmp_path, judge_report)

    assert s5["round_1_discrepancies_count"] == 0
    assert s5["round_1_passed"] is False
    assert s5["passed_first_attempt"] is False
    assert s5["has_rejudge"] is True
