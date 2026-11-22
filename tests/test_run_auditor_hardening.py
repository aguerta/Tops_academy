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


# ---------------------------------------------------------------------------
# 4. Gemini 4 Hydrogen USD Cost Valuation across audit_engine, unified & run.py
# ---------------------------------------------------------------------------


def test_compute_hydrogen_cost_usd_exact_math() -> None:
    # 1M uncached input ($1.50) + 1M output ($7.50) + 1M cache read ($0.075) = $9.0750
    res = audit_engine.compute_hydrogen_cost_usd(
        input_tokens=1_000_000,
        output_tokens=1_000_000,
        cache_read_tokens=1_000_000,
    )
    assert res["input_usd"] == pytest.approx(1.50, abs=1e-4)
    assert res["output_usd"] == pytest.approx(7.50, abs=1e-4)
    assert res["cache_read_usd"] == pytest.approx(0.075, abs=1e-4)
    assert res["total_usd"] == pytest.approx(9.075, abs=1e-4)

    # Zero / None safety
    zero = audit_engine.compute_hydrogen_cost_usd(0, 0, 0)
    assert zero == {"input_usd": 0.0, "output_usd": 0.0, "cache_read_usd": 0.0, "total_usd": 0.0}


def test_stage_costs_sum_equals_total_cost_and_renders_in_reports(tmp_path: Path, monkeypatch) -> None:
    brain_dir = tmp_path / "brain"
    root_cid = "aaaa1111-2222-3333-4444-555566667777"
    cta_cid = "bbbb1111-2222-3333-4444-555566667777"
    auth_cid = "cccc1111-2222-3333-4444-555566667777"
    rep_cid = "dddd1111-2222-3333-4444-555566667777"
    jdg_cid = "eeee1111-2222-3333-4444-555566667777"

    def _write_thread(cid: str, records: list[dict]) -> None:
        ldir = brain_dir / cid / ".system_generated" / "logs"
        ldir.mkdir(parents=True, exist_ok=True)
        (ldir / "transcript.jsonl").write_text(
            "\n".join(json.dumps(r) for r in records),
            encoding="utf-8",
        )

    _write_thread(
        cta_cid,
        [
            {"type": "USER_INPUT", "step_index": 0, "created_at": "2026-11-20T10:00:00Z", "content": "Role: CTA Architect part_01"},
            {"type": "PLANNER_RESPONSE", "step_index": 1, "created_at": "2026-11-20T10:00:20Z", "input_tokens": 100_000, "output_tokens": 10_000, "cache_read_tokens": 200_000, "content": "DONE: part_01"},
        ],
    )
    _write_thread(
        auth_cid,
        [
            {"type": "USER_INPUT", "step_index": 0, "created_at": "2026-11-20T10:01:00Z", "content": "You are Shard Author shard_01"},
            {"type": "PLANNER_RESPONSE", "step_index": 1, "created_at": "2026-11-20T10:02:00Z", "input_tokens": 400_000, "output_tokens": 50_000, "cache_read_tokens": 1_000_000, "content": "DONE: shard_01"},
        ],
    )
    _write_thread(
        rep_cid,
        [
            {"type": "USER_INPUT", "step_index": 0, "created_at": "2026-11-20T10:02:30Z", "content": "Role: Repair Engineer (SHARD_01)"},
            {"type": "PLANNER_RESPONSE", "step_index": 1, "created_at": "2026-11-20T10:02:50Z", "input_tokens": 50_000, "output_tokens": 5_000, "cache_read_tokens": 100_000, "content": "DONE: repaired"},
        ],
    )
    _write_thread(
        jdg_cid,
        [
            {"type": "USER_INPUT", "step_index": 0, "created_at": "2026-11-20T10:03:00Z", "content": "You are Blind Judge 01"},
            {"type": "PLANNER_RESPONSE", "step_index": 1, "created_at": "2026-11-20T10:03:20Z", "input_tokens": 150_000, "output_tokens": 20_000, "cache_read_tokens": 300_000, "content": "DONE: judged"},
        ],
    )

    root_records = [
        {
            "type": "PLANNER_RESPONSE",
            "step_index": 1,
            "created_at": "2026-11-20T10:00:00Z",
            "input_tokens": 200_000,
            "output_tokens": 15_000,
            "cache_read_tokens": 400_000,
            "content": "Dispatching waves",
            "tool_calls": [],
        },
        {
            "type": "SYSTEM_MESSAGE",
            "step_index": 2,
            "created_at": "2026-11-20T10:04:00Z",
            "content": (
                f"- [agent:c2c_cta_architect] CTA Architect part_01: done ({cta_cid})\n"
                f"- [agent:c2c_shard_author] Shard Author shard_01: done ({auth_cid})\n"
                f"- [agent:c2c_repair] Repair Engineer (SHARD_01): done ({rep_cid})\n"
                f"- [agent:c2c_judge] Blind Judge 01: done ({jdg_cid})\n"
            ),
        },
    ]

    monkeypatch.setattr(audit_engine, "get_brain_dir", lambda: brain_dir)
    auditor = audit_engine.ExecutionAuditor(root_records=root_records, root_conv_id=root_cid)
    workload = {
        "source_files": [{"name": "notes.pdf", "pages": 10, "size_bytes": 1024}],
        "total_input_bytes": 1024,
        "total_input_mb": 0.01,
        "total_pages_or_slides": 10,
        "pages_needing_vision": 0,
        "total_handouts": 0,
        "corpus_chars": 1000,
        "corpus_words": 150,
        "competencies_count": 5,
        "shards_count": 1,
        "shards_competencies_map": {"shard_01": {"competency_ids": ["C-01"], "count": 1}},
        "questions_count": 100,
        "cta_mode": "mapreduce",
        "course_id": "test_cost_course",
        "course_title": "Test Cost Course",
        "telemetry_snapshots": [],
    }
    audit_res = auditor.audit(workload)
    summary = audit_res["summary"]
    sc = summary["stage_costs_usd"]

    # Exact totals: in=900k ($1.35), out=100k ($0.75), cache=2M ($0.15) => $2.2500
    assert summary["pricing_model"] == "gemini-4-hydrogen"
    assert summary["total_cost_usd"] == pytest.approx(2.25, abs=1e-4)
    stage_sum = (
        sc["stage_1a_vision"]
        + sc["stage_1b_cta"]
        + sc["stage_3_authors"]
        + sc["stage_3b_repairs"]
        + sc["stage_5_judges"]
        + sc["orchestrator"]
        + sc["other_subagents"]
    )
    assert stage_sum == pytest.approx(summary["total_cost_usd"], abs=1e-3)
    assert audit_res["unit_economics"]["usd_per_question"] == pytest.approx(0.0225, abs=1e-4)
    assert audit_res["unit_economics"]["usd_per_competency"] == pytest.approx(0.45, abs=1e-4)

    # 1) audit_engine.ReportGenerator Markdown + Registry
    md = audit_engine.ReportGenerator.generate_markdown(audit_res)
    assert "Gemini 4 Hydrogen" in md
    assert "$2.2500 USD" in md
    assert "3.0a. Valorización Monetaria por Etapa" in md
    reg_mgr = audit_engine.HistoricalRegistry(tmp_path / "c2c_audits")
    reg_mgr.register_run(audit_res, "20261121_test_cost_course_aaaa1111")
    bench_md = reg_mgr.benchmark_md_file.read_text(encoding="utf-8")
    assert "Costo (USD)" in bench_md
    assert "$2.2500" in bench_md

    # 2) unified_audit_engine merged report (both new telemetry and fallback legacy telemetry without cost_usd)
    unified_scripts = str(REPO_ROOT / ".agents" / "skills" / "c2c-unified-auditor" / "scripts")
    if unified_scripts not in sys.path:
        sys.path.insert(0, unified_scripts)
    import unified_audit_engine  # type: ignore

    merged = unified_audit_engine.generate_merged_markdown_report(
        course_id="test_cost_course",
        conv_id=root_cid,
        qa_report={"course_metadata": {"unit_title": "Test Cost Course", "total_competencies": 5, "total_questions": 100}},
        payload_data={"audit_telemetry": {"dimension_summaries": {}}},
        telemetry_data=audit_res,
        traceback_data={},
    )
    assert "$2.2500 USD" in merged
    assert "Stage 3B: Repair Engineers" in merged

    legacy_tel = json.loads(json.dumps(audit_res))
    for k in ("total_cost_usd", "cost_breakdown_usd", "stage_costs_usd"):
        legacy_tel["summary"].pop(k, None)
    merged_legacy = unified_audit_engine.generate_merged_markdown_report(
        course_id="test_cost_course",
        conv_id=root_cid,
        qa_report={"course_metadata": {"unit_title": "Test Cost Course", "total_competencies": 5, "total_questions": 100}},
        payload_data={"audit_telemetry": {"dimension_summaries": {}}},
        telemetry_data=legacy_tel,
        traceback_data={},
    )
    assert "$2.2500 USD" in merged_legacy

    # 3) content-to-course run.py closeout summary formatter (full + fallback)
    import run as c2c_run  # type: ignore

    runner = c2c_run.PipelineRunner(course_id="test_cost_course", work_dir=tmp_path / "work")
    pub_summary = runner._format_run_audit_summary({"mode": "full_audit_engine", "telemetry": audit_res})
    assert "Costo Estimado (Hydrogen):" in pub_summary
    assert "$2.2500 USD" in pub_summary
    assert "TOTAL CORRIDA (Hydrogen):  $2.2500 USD" in pub_summary

    fb_summary = runner._format_run_audit_summary({
        "mode": "work_dir_fallback",
        "state": {
            "stages": {
                "01_cta": {"duration_seconds": 12.0, "status": "completed", "tokens": {"input": 100_000, "output": 10_000, "cached": 200_000}},
            },
            "total_tokens": {"input": 100_000, "output": 10_000, "cached": 200_000},
        },
    })
    assert "$0.2400 USD" in fb_summary
    assert "TOTAL CORRIDA (Hydrogen):  $0.2400 USD" in fb_summary


def test_audit_engine_r1_flaw_fallback_ignores_prompt_and_handles_null_content(tmp_path: Path) -> None:
    """Round-1 flaw fallback ignores prompt_blind_judge.md instructions and compile tracker handles null content & exit 137."""
    eng = _make_engine()
    eng.brain_dir = tmp_path

    # 1) _analyze_conversation: content=None + non-zero exit code 137 must not crash and must fail first compile
    records = [
        {
            "type": "PLANNER_RESPONSE",
            "step_index": 1,
            "input_tokens": 100,
            "output_tokens": 20,
            "cache_read_tokens": 0,
            "tool_calls": [
                {"name": "run_command", "args": {"CommandLine": "python compile_shard.py --shard 01"}}
            ],
        },
        {"type": "TOOL_RESPONSE", "step_index": 2, "content": None},
        {"type": "TOOL_RESPONSE", "step_index": 3, "content": "Command exited with code 137"},
    ]
    metrics = eng._analyze_conversation(records, "author-01", "Author 01")
    assert metrics["compile_attempts_count"] == 1
    assert metrics["compile_first_passed"] is False

    # 2) round_1_flaw_detected_count fallback ignores system prompt mentions and counts actual verdict write_file
    j_cid = "judge-conv-01"
    j_logs = tmp_path / j_cid / ".system_generated" / "logs"
    j_logs.mkdir(parents=True)
    judge_lines = [
        {
            "type": "USER_INPUT",
            "content": 'Scoring rubric: FAIL ("flaw_detected": true) example in prompt_blind_judge.md',
        },
        {
            "type": "PLANNER_RESPONSE",
            "thinking": 'Checking if "flaw_detected": true applies here.',
            "tool_calls": [
                {
                    "name": "write_file",
                    "args": {
                        "Path": "work/verification/judge_responses_01.json",
                        "Content": json.dumps({
                            "responses": {
                                "item_1": {"answer": "A", "flaw_detected": False},
                                "item_2": {"answer": "BLOCKED: missing var", "flaw_detected": True},
                            }
                        }),
                    },
                }
            ],
        },
    ]
    (j_logs / "transcript_full.jsonl").write_text(
        "\n".join(json.dumps(x) for x in judge_lines), encoding="utf-8"
    )

    work_dir = tmp_path / "work"
    work_dir.mkdir()
    (work_dir / "judge_report_round_1.json").write_text(
        json.dumps({"passed": False, "agreement_rate": 0.5, "total_items": 2, "disagreements": [{"id": "item_2"}]}),
        encoding="utf-8",
    )
    (work_dir / "judge_report.json").write_text(
        json.dumps({"passed": True, "agreement_rate": 1.0, "total_items": 2, "disagreements": []}),
        encoding="utf-8",
    )

    deep = eng._build_stage_deep_dives(
        subagents=[
            {
                "conversation_id": j_cid,
                "label": "Judge 01",
                "category": "judge",
                "spawn_step": 10,
                "duration_seconds": 5.0,
                "input_tokens": 100,
                "output_tokens": 50,
                "cache_read_tokens": 0,
                "active_tokens": 150,
                "total_tokens": 150,
                "tool_calls_count": 1,
                "tool_errors_count": 0,
            }
        ],
        orch_time={"barrier_wait_seconds": 0.0},
        workload={"work_dir": str(work_dir), "competencies_count": 1, "telemetry_snapshots": []},
        interventions=[],
        records=[],
    )
    assert deep["stage_5_judges"]["round_1_flaw_detected_count"] == 1
