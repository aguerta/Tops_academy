import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
RUN_AUDITOR_SCRIPTS = REPO_ROOT / ".agents" / "skills" / "c2c-run-auditor" / "scripts"
C2C_SCRIPTS = REPO_ROOT / ".agents" / "skills" / "content-to-course"

for p in (str(RUN_AUDITOR_SCRIPTS), str(C2C_SCRIPTS)):
    if p not in sys.path:
        sys.path.insert(0, p)

import audit_engine  # noqa: E402
import shard_timing_profiler  # noqa: E402
import telemetry_collector  # noqa: E402


# ---------------------------------------------------------------------------
# 1. shard_timing_profiler.ERROR_CODE_RE
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "code",
    [
        "[TPL-HINTS-DUPLICATE]",
        "[TPL-VERIFIER-UNSOUND]",
        "[DIAG-MAGIC-MULT]",
        "[VERIFIER-TAUTOLOGY-DETECTED]",
        "[R-19]",
        "[TIMEOUT_INFINITE_LOOP]",
        "[INVARIANT]",
        "[CTA-MAP-ERR]",
        "[GATE-PRE-SHARD]",
    ],
)
def test_error_code_re_matches_all_new_codes(code: str) -> None:
    sample = f"Build failed with {code} during shard compilation."
    matches = shard_timing_profiler.ERROR_CODE_RE.findall(sample)
    assert code in matches


def test_profile_agent_record_extracts_new_error_codes(tmp_path: Path) -> None:
    cid = "conv-test-001"
    logs_dir = tmp_path / cid / ".system_generated" / "logs"
    logs_dir.mkdir(parents=True)
    transcript = logs_dir / "transcript.jsonl"
    records = [
        {
            "role": "tool",
            "createdAt": "2026-11-15T00:00:01Z",
            "content": (
                "Command exited with code 1\n"
                "[TPL-HINTS-DUPLICATE] duplicate hints\n"
                "[VERIFIER-TAUTOLOGY-DETECTED] tautology\n"
                "[TIMEOUT_INFINITE_LOOP] infinite loop\n"
                "[INVARIANT] violated\n"
            ),
        }
    ]
    transcript.write_text("\n".join(json.dumps(r) for r in records), encoding="utf-8")

    res = shard_timing_profiler._profile_agent_record(
        {
            "conversation_id": cid,
            "label": "Author Shard 01",
            "category": "author",
            "duration_seconds": 12.0,
        },
        tb_shards={},
        brain_dir=tmp_path,
    )
    assert set(res["error_codes"]) >= {
        "[TPL-HINTS-DUPLICATE]",
        "[VERIFIER-TAUTOLOGY-DETECTED]",
        "[TIMEOUT_INFINITE_LOOP]",
        "[INVARIANT]",
    }


# ---------------------------------------------------------------------------
# 2. audit_engine.py — judge_report_round_1.json & rounds_history handling
# ---------------------------------------------------------------------------


def _make_engine() -> audit_engine.ExecutionAuditor:
    eng = audit_engine.ExecutionAuditor.__new__(audit_engine.ExecutionAuditor)
    eng.root_conv_id = "root-conv-123"
    return eng


def test_audit_engine_reads_judge_report_round_1_never_claims_first_attempt(tmp_path: Path) -> None:
    work_dir = tmp_path / "work"
    work_dir.mkdir()

    (work_dir / "judge_report_round_1.json").write_text(
        json.dumps(
            {
                "passed": False,
                "agreement_rate": 0.75,
                "total_items": 8,
                "disagreements": [{"id": "q1"}, {"id": "q2"}],
            }
        ),
        encoding="utf-8",
    )
    (work_dir / "judge_report.json").write_text(
        json.dumps(
            {
                "passed": True,
                "agreement_rate": 1.0,
                "total_items": 8,
                "disagreements": [],
            }
        ),
        encoding="utf-8",
    )

    eng = _make_engine()
    deep = eng._build_stage_deep_dives(
        subagents=[],
        orch_time={"barrier_wait_seconds": 0.0},
        workload={"work_dir": str(work_dir), "competencies_count": 4, "telemetry_snapshots": []},
        interventions=[],
        records=[],
    )
    s5 = deep["stage_5_judges"]
    assert s5["passed_first_attempt"] is False
    assert s5["has_rejudge"] is True
    assert s5["round_1_discrepancies_count"] == 2
    assert s5["final_passed"] is True
    assert "100% ACUERDO AL PRIMER INTENTO" not in s5["badge"]
    assert "Ronda 1" in s5["summary_desc"]
    assert "Rejudge" in s5["summary_desc"]


def test_audit_engine_reads_rounds_history_never_claims_first_attempt(tmp_path: Path) -> None:
    work_dir = tmp_path / "work"
    work_dir.mkdir()

    (work_dir / "judge_report.json").write_text(
        json.dumps(
            {
                "passed": True,
                "agreement_rate": 1.0,
                "total_items": 10,
                "disagreements": [],
                "rounds_history": [
                    {"round": 1, "passed": False, "agreement_rate": 0.9, "disagreements": ["q3"]},
                    {"round": 2, "passed": True, "agreement_rate": 1.0, "disagreements": []},
                ],
            }
        ),
        encoding="utf-8",
    )

    eng = _make_engine()
    deep = eng._build_stage_deep_dives(
        subagents=[],
        orch_time={"barrier_wait_seconds": 0.0},
        workload={"work_dir": str(work_dir), "competencies_count": 5, "telemetry_snapshots": []},
        interventions=[],
        records=[],
    )
    s5 = deep["stage_5_judges"]
    assert s5["passed_first_attempt"] is False
    assert s5["has_rejudge"] is True
    assert s5["round_1_discrepancies_count"] == 1
    assert s5["final_passed"] is True
    assert "100% ACUERDO AL PRIMER INTENTO" not in s5["badge"]


def test_audit_engine_clean_first_attempt_still_passes(tmp_path: Path) -> None:
    work_dir = tmp_path / "work"
    work_dir.mkdir()

    (work_dir / "judge_report.json").write_text(
        json.dumps(
            {
                "passed": True,
                "agreement_rate": 1.0,
                "total_items": 6,
                "disagreements": [],
            }
        ),
        encoding="utf-8",
    )

    eng = _make_engine()
    deep = eng._build_stage_deep_dives(
        subagents=[],
        orch_time={"barrier_wait_seconds": 0.0},
        workload={"work_dir": str(work_dir), "competencies_count": 3, "telemetry_snapshots": []},
        interventions=[],
        records=[],
    )
    s5 = deep["stage_5_judges"]
    assert s5["passed_first_attempt"] is True
    assert "100% ACUERDO AL PRIMER INTENTO" in s5["badge"]


# ---------------------------------------------------------------------------
# 3. telemetry_collector.py — harmonizer & orchestrator cohorts in state.json
# ---------------------------------------------------------------------------


def test_telemetry_collector_infers_harmonizer_and_orchestrator_cohorts() -> None:
    assert telemetry_collector.infer_subagent_cohort("CTA Harmonizer", "cta-reduce") == "harmonizer"
    assert telemetry_collector.infer_subagent_cohort("Harmonizer", "") == "harmonizer"
    assert telemetry_collector.infer_subagent_cohort("Director (Orchestrator)", "") == "orchestrator"
    assert telemetry_collector.infer_subagent_cohort("Orchestrator", "") == "orchestrator"

    assert telemetry_collector.is_compiler_cohort("orchestrator", "Orchestrator") is False
    assert telemetry_collector.is_compiler_cohort("harmonizer", "CTA Harmonizer") is True


def test_telemetry_collector_state_json_includes_harmonizer_and_orchestrator(tmp_path: Path) -> None:
    work_dir = tmp_path / "work"
    telem_dir = work_dir / "telemetry"
    telem_dir.mkdir(parents=True)

    snapshot = {
        "stage_idx": "01",
        "stage_name": "cta",
        "status": "completed",
        "recorded_at": "2026-11-15T00:00:00Z",
        "duration_seconds": 45.0,
        "conversation_id": "conv-abc",
        "stage_tokens": {"input": 1000, "output": 500, "cached": 200, "thinking": 100, "total": 1800},
        "subagents": [
            {
                "conversation_id": "sub-orch",
                "role": "Director (Orchestrator)",
                "type_name": "orchestrator",
                "tokens": {"input": 400, "output": 200, "cached": 100, "thinking": 50, "total": 750},
                "turns_count": 3,
                "duration_seconds": 20.0,
            },
            {
                "conversation_id": "sub-harm",
                "role": "CTA Harmonizer",
                "type_name": "cta-reduce",
                "first_pass": True,
                "final_pass": True,
                "compiler_invocations": 1,
                "tokens": {"input": 600, "output": 300, "cached": 100, "thinking": 50, "total": 1050},
                "turns_count": 4,
                "duration_seconds": 25.0,
            },
        ],
    }
    (telem_dir / "01_cta.json").write_text(json.dumps(snapshot), encoding="utf-8")

    state = telemetry_collector.update_master_state(work_dir, snapshot)
    cohorts = state["cohorts_summary"]

    assert "harmonizer" in cohorts
    assert "orchestrator" in cohorts
    assert cohorts["harmonizer"]["count"] == 1
    assert cohorts["harmonizer"]["uses_compiler"] is True
    assert cohorts["harmonizer"]["fpy_ratio"] == "1/1"
    assert cohorts["orchestrator"]["count"] == 1
    assert cohorts["orchestrator"]["uses_compiler"] is False
    assert cohorts["orchestrator"]["fpy_ratio"] == "N/A"
