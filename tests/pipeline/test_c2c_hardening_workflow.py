"""Tests for c2c_wave_workflow.py hardening:
- _resolve_director_id priority (args -> .c2c_subagent_lock.json -> state.json)
- run_cli subprocess env propagation (ANTIGRAVITY_CONVERSATION_ID, C2C_DIRECTOR_ID)
- --director-id propagation in all run.py invocations (post_cta_pipeline & repair_and_rejudge)
- Atomic repair_and_rejudge mode (explicit ids & repair-matrix consolidation)
- Unlimited parallel(subagents, ...) fan-out
"""

import asyncio
import json
import os
import sys
import time
import types
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple
from unittest.mock import patch

import pytest

WORKFLOW_PATH = (
    Path(__file__).resolve().parents[2]
    / ".agents"
    / "skills"
    / "content-to-course"
    / "workflows"
    / "c2c_wave_workflow.py"
)


def _load_workflow_module(
    wf_args: Optional[Dict[str, Any]] = None,
    parallel_fn: Optional[Callable[..., Any]] = None,
) -> Tuple[types.ModuleType, List[str], List[str]]:
    """Load c2c_wave_workflow.py in an isolated module namespace without top-level await."""
    source = WORKFLOW_PATH.read_text(encoding="utf-8")
    marker = 'if "parallel" in globals():'
    if marker in source:
        source = source.split(marker, 1)[0]

    logs: List[str] = []
    phases: List[str] = []

    async def _default_parallel(items: List[Any], fn: Callable[[Any], Any]) -> List[Any]:
        return [await fn(item) for item in items]

    async def _default_agent(**kwargs: Any) -> str:
        return f"OK:{kwargs.get('role', '')}"

    mod = types.ModuleType("c2c_wave_workflow_test")
    mod.__file__ = str(WORKFLOW_PATH)
    mod.__dict__.update(
        {
            "args": dict(wf_args or {}),
            "log": logs.append,
            "phase": phases.append,
            "parallel": parallel_fn or _default_parallel,
            "agent": _default_agent,
        }
    )
    exec(compile(source, str(WORKFLOW_PATH), "exec"), mod.__dict__)
    return mod, logs, phases


def _write_fresh_json(path: Path, payload: Any) -> None:
    """Write JSON and bump mtime forward to avoid Windows NTFS timestamp-resolution flakiness."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")
    fresh_ts = time.time() + 2.0
    os.utime(path, (fresh_ts, fresh_ts))


def _write_manifest(path: Path, count: int, prefix: str = "Worker") -> None:
    subagents = [
        {
            "Prompt": f"Execute {prefix} #{i}",
            "TypeName": "self",
            "Role": f"{prefix} {i}",
            "Model": "inherit",
        }
        for i in range(1, count + 1)
    ]
    _write_fresh_json(path, {"Subagents": subagents})


# ==============================================================================
# 1. _resolve_director_id priority & fallbacks
# ==============================================================================


def test_resolve_director_id_priority_and_fallbacks(tmp_path: Path) -> None:
    work_dir = tmp_path / "work"
    work_dir.mkdir(parents=True, exist_ok=True)

    # Empty when nothing is present
    mod, _, _ = _load_workflow_module({"work_dir": str(work_dir)})
    assert mod._resolve_director_id(work_dir) == ""

    # Fallback 3: state.json -> conversation_id
    (work_dir / "state.json").write_text(
        json.dumps({"conversation_id": "state-conv-003"}), encoding="utf-8"
    )
    assert mod._resolve_director_id(work_dir) == "state-conv-003"

    # Fallback 2: .c2c_subagent_lock.json -> director_conversation_id overrides state.json
    (work_dir / ".c2c_subagent_lock.json").write_text(
        json.dumps({"active": True, "director_conversation_id": "lock-conv-002"}),
        encoding="utf-8",
    )
    assert mod._resolve_director_id(work_dir) == "lock-conv-002"

    # Priority 1: _WF_ARGS["director_id"] overrides lockfile and state.json
    mod._WF_ARGS["director_id"] = "arg-conv-001"
    assert mod._resolve_director_id(work_dir) == "arg-conv-001"


def test_resolve_director_id_handles_corrupt_json(tmp_path: Path) -> None:
    work_dir = tmp_path / "work"
    work_dir.mkdir(parents=True, exist_ok=True)
    (work_dir / ".c2c_subagent_lock.json").write_text("{corrupt", encoding="utf-8")
    (work_dir / "state.json").write_text(
        json.dumps({"conversation_id": "state-fallback-ok"}), encoding="utf-8"
    )
    mod, _, _ = _load_workflow_module({"work_dir": str(work_dir)})
    assert mod._resolve_director_id(work_dir) == "state-fallback-ok"


# ==============================================================================
# 2. run_cli env propagation
# ==============================================================================


def test_run_cli_propagates_director_env(tmp_path: Path) -> None:
    work_dir = tmp_path / "work"
    work_dir.mkdir(parents=True, exist_ok=True)
    mod, _, _ = _load_workflow_module({"work_dir": str(work_dir)})

    captured_kwargs: List[Dict[str, Any]] = []

    class _FakeProc:
        returncode = 0

        async def communicate(self) -> Tuple[bytes, None]:
            return b"ok\n", None

    async def _fake_exec(*argv: Any, **kwargs: Any) -> _FakeProc:
        captured_kwargs.append(kwargs)
        return _FakeProc()

    with patch.object(mod.asyncio, "create_subprocess_exec", side_effect=_fake_exec):
        # 1. No director_id & no env_extra -> no custom env dict injected
        asyncio.run(mod.run_cli("echo hi", "no-env"))
        assert "env" not in captured_kwargs[-1]

        # 2. Explicit env_extra propagates both ANTIGRAVITY_CONVERSATION_ID and C2C_DIRECTOR_ID
        asyncio.run(
            mod.run_cli(
                "echo hi",
                "with-env-extra",
                env_extra={"C2C_DIRECTOR_ID": "dir-xyz-789"},
            )
        )
        env2 = captured_kwargs[-1]["env"]
        assert env2["C2C_DIRECTOR_ID"] == "dir-xyz-789"
        assert env2["ANTIGRAVITY_CONVERSATION_ID"] == "dir-xyz-789"

        # 3. Fallback resolution from lockfile when env_extra is omitted
        (work_dir / ".c2c_subagent_lock.json").write_text(
            json.dumps({"director_conversation_id": "lock-dir-456"}), encoding="utf-8"
        )
        asyncio.run(mod.run_cli("echo hi", "from-lockfile"))
        env3 = captured_kwargs[-1]["env"]
        assert env3["C2C_DIRECTOR_ID"] == "lock-dir-456"
        assert env3["ANTIGRAVITY_CONVERSATION_ID"] == "lock-dir-456"


# ==============================================================================
# 3. repair_and_rejudge mode (explicit IDs & repair-matrix consolidation)
# ==============================================================================


def test_repair_and_rejudge_with_explicit_ids_sequence(tmp_path: Path) -> None:
    work_dir = tmp_path / "work"
    dispatch_dir = work_dir / "dispatch"
    dispatch_dir.mkdir(parents=True, exist_ok=True)

    wave_calls: List[int] = []

    async def _fake_parallel(items: List[Any], fn: Callable[[Any], Any]) -> List[Any]:
        wave_calls.append(len(items))
        return [await fn(item) for item in items]

    mod, _, phases = _load_workflow_module(
        {
            "work_dir": str(work_dir),
            "mode": "repair_and_rejudge",
            "ids": ["C-01", "H-02"],
            "director_id": "dir-abc-123",
        },
        parallel_fn=_fake_parallel,
    )

    cli_calls: List[Tuple[str, str, Optional[Dict[str, str]]]] = []

    async def _fake_run_cli(
        cmd: str,
        summary: str,
        env_extra: Optional[Dict[str, str]] = None,
    ) -> str:
        cli_calls.append((summary, cmd, env_extra))
        if summary == "C2C dispatch repair":
            _write_manifest(dispatch_dir / "repair.json", 3, "Repair")
        elif summary == "C2C stage surgical rejudge":
            _write_manifest(dispatch_dir / "judges.json", 4, "Rejudge")
        return "Command exited with code 0."

    mod.run_cli = _fake_run_cli

    summary = asyncio.run(mod.run_c2c_workflow())

    assert summary["mode"] == "repair_and_rejudge"
    assert summary["ids"] == ["C-01", "H-02"]
    assert summary["repairs_completed"] == 3
    assert summary["rejudges_completed"] == 4
    assert wave_calls == [3, 4]

    # Exact sequence: repair-matrix is skipped when explicit ids are passed
    summaries = [c[0] for c in cli_calls]
    assert summaries == [
        "C2C dispatch repair",
        "C2C post-repair stage templates",
        "C2C post-repair stage build",
        "C2C stage surgical rejudge",
        "C2C stage rejudge-compare",
        "C2C post-repair stage gates",
    ]

    # Verify --ids in dispatch-repair & rejudge, and --director-id + env_extra in all run.py calls
    assert "--ids C-01 H-02" in cli_calls[0][1]
    for call_summary, cmd, env_extra in cli_calls:
        assert env_extra == {
            "ANTIGRAVITY_CONVERSATION_ID": "dir-abc-123",
            "C2C_DIRECTOR_ID": "dir-abc-123",
        }
        if "run.py" in cmd:
            assert "--director-id dir-abc-123" in cmd, f"Missing --director-id in {call_summary}: {cmd}"
    assert "--stage rejudge --ids C-01 H-02" in cli_calls[3][1]
    assert "Atomic Repair & Surgical Rejudge" in phases


def test_repair_and_rejudge_auto_consolidates_via_repair_matrix(tmp_path: Path) -> None:
    work_dir = tmp_path / "work"
    dispatch_dir = work_dir / "dispatch"
    dispatch_dir.mkdir(parents=True, exist_ok=True)
    (work_dir / ".c2c_subagent_lock.json").write_text(
        json.dumps({"active": True, "director_conversation_id": "lock-dir-999"}),
        encoding="utf-8",
    )

    mod, _, _ = _load_workflow_module(
        {
            "work_dir": str(work_dir),
            "mode": "repair_and_rejudge",
        }
    )

    cli_calls: List[Tuple[str, str, Optional[Dict[str, str]]]] = []

    async def _fake_run_cli(
        cmd: str,
        summary: str,
        env_extra: Optional[Dict[str, str]] = None,
    ) -> str:
        cli_calls.append((summary, cmd, env_extra))
        if summary == "C2C stage repair-matrix":
            _write_fresh_json(
                work_dir / "repair_matrix.json",
                {"failing_competencies": ["C-03", "H-04"]},
            )
        elif summary == "C2C dispatch repair":
            _write_manifest(dispatch_dir / "repair.json", 2, "Repair")
        elif summary == "C2C stage surgical rejudge":
            _write_manifest(dispatch_dir / "judges.json", 2, "Rejudge")
        return "Command exited with code 0."

    mod.run_cli = _fake_run_cli

    summary = asyncio.run(mod.run_c2c_workflow())

    assert summary["ids"] == ["C-03", "H-04"]
    assert summary["repairs_completed"] == 2
    assert summary["rejudges_completed"] == 2
    assert [c[0] for c in cli_calls] == [
        "C2C stage repair-matrix",
        "C2C dispatch repair",
        "C2C post-repair stage templates",
        "C2C post-repair stage build",
        "C2C stage surgical rejudge",
        "C2C stage rejudge-compare",
        "C2C post-repair stage gates",
    ]
    assert "--ids C-03 H-04" in cli_calls[1][1]
    assert "--stage rejudge --ids C-03 H-04" in cli_calls[4][1]
    for _, cmd, env_extra in cli_calls:
        assert env_extra == {
            "ANTIGRAVITY_CONVERSATION_ID": "lock-dir-999",
            "C2C_DIRECTOR_ID": "lock-dir-999",
        }
        if "run.py" in cmd:
            assert "--director-id lock-dir-999" in cmd


def test_repair_and_rejudge_no_failing_ids_exits_early(tmp_path: Path) -> None:
    work_dir = tmp_path / "work"
    work_dir.mkdir(parents=True, exist_ok=True)
    mod, _, _ = _load_workflow_module(
        {"work_dir": str(work_dir), "mode": "repair_and_rejudge"}
    )

    cli_calls: List[str] = []

    async def _fake_run_cli(
        cmd: str,
        summary: str,
        env_extra: Optional[Dict[str, str]] = None,
    ) -> str:
        cli_calls.append(summary)
        if summary == "C2C stage repair-matrix":
            (work_dir / "repair_matrix.json").write_text(
                json.dumps({"failing_competencies": []}), encoding="utf-8"
            )
        return "Command exited with code 0."

    mod.run_cli = _fake_run_cli
    summary = asyncio.run(mod.run_c2c_workflow())

    assert summary["ids"] == []
    assert summary["repairs_completed"] == 0
    assert summary["rejudges_completed"] == 0
    assert cli_calls == ["C2C stage repair-matrix"]


# ==============================================================================
# 4. post_cta_pipeline director_id propagation & unlimited parallel fan-out
# ==============================================================================


def test_post_cta_pipeline_propagates_director_id_to_all_run_py_calls(tmp_path: Path) -> None:
    work_dir = tmp_path / "work"
    dispatch_dir = work_dir / "dispatch"
    dispatch_dir.mkdir(parents=True, exist_ok=True)
    (work_dir / "state.json").write_text(
        json.dumps({"conversation_id": "state-dir-777"}), encoding="utf-8"
    )

    mod, _, _ = _load_workflow_module(
        {"work_dir": str(work_dir), "mode": "post_cta_pipeline"}
    )

    cli_calls: List[Tuple[str, str, Optional[Dict[str, str]]]] = []

    async def _fake_run_cli(
        cmd: str,
        summary: str,
        env_extra: Optional[Dict[str, str]] = None,
    ) -> str:
        cli_calls.append((summary, cmd, env_extra))
        if summary == "C2C dispatch authors":
            _write_manifest(dispatch_dir / "authors.json", 2, "Author")
        elif summary == "C2C dispatch judges":
            _write_manifest(dispatch_dir / "judges.json", 2, "Judge")
        elif summary == "C2C stage gates" and len(cli_calls) < 8:
            _write_fresh_json(
                work_dir / "repair_matrix.json",
                {"failing_competencies": ["C-01"]},
            )
        elif summary == "C2C stage repair-matrix":
            _write_fresh_json(
                work_dir / "repair_matrix.json",
                {"failing_competencies": ["C-01"]},
            )
        elif summary == "C2C dispatch repair":
            _write_manifest(dispatch_dir / "repair.json", 1, "Repair")
        elif summary == "C2C stage surgical rejudge":
            _write_manifest(dispatch_dir / "judges.json", 1, "Rejudge")
        return "Command exited with code 0."

    mod.run_cli = _fake_run_cli
    summary = asyncio.run(mod.run_c2c_workflow())

    assert summary["authors_completed"] == 2
    assert summary["judges_completed"] == 2
    assert summary["repairs_completed"] == 1

    run_py_calls = [(s, c, e) for s, c, e in cli_calls if "run.py" in c]
    assert len(run_py_calls) == 11
    for call_summary, cmd, env_extra in run_py_calls:
        assert "--director-id state-dir-777" in cmd, f"Missing --director-id in {call_summary}: {cmd}"
        assert env_extra == {
            "ANTIGRAVITY_CONVERSATION_ID": "state-dir-777",
            "C2C_DIRECTOR_ID": "state-dir-777",
        }


def test_run_wave_from_manifest_unlimited_parallel_fanout(tmp_path: Path) -> None:
    manifest = tmp_path / "authors.json"
    _write_manifest(manifest, 12, "Author")

    fanout_sizes: List[int] = []

    async def _fake_parallel(items: List[Any], fn: Callable[[Any], Any]) -> List[Any]:
        fanout_sizes.append(len(items))
        return [await fn(item) for item in items]

    mod, _, _ = _load_workflow_module({}, parallel_fn=_fake_parallel)
    results = asyncio.run(mod.run_wave_from_manifest(str(manifest), "Unlimited Fan-Out"))

    assert len(results) == 12
    assert fanout_sizes == [12]



# ==============================================================================
# 5. Quota backoff and rejudge checkpoint
# ==============================================================================


def test_quota_error_gets_extended_retries(tmp_path: Path) -> None:
    manifest = tmp_path / "authors.json"
    _write_manifest(manifest, 1, "Author")
    mod, _, _ = _load_workflow_module(
        {"quota_retry_backoff_s": [0.0], "retry_backoff_s": [0.0], "startup_stagger_s": 0.0}
    )
    calls = {"n": 0}

    async def _flaky_agent(**kwargs: Any) -> str:
        calls["n"] += 1
        if calls["n"] <= 4:
            raise RuntimeError("RESOURCE_EXHAUSTED (code 429)")
        return "DONE: ok"

    mod.agent = _flaky_agent
    results = asyncio.run(mod.run_wave_from_manifest(str(manifest), "Quota"))
    assert results == ["DONE: ok"]
    assert calls["n"] == 5
    assert mod._is_quota_error("HTTP 429")
    assert not mod._is_quota_error("syntax error")


def test_rejudge_checkpoint_resumes_without_repair_wave(tmp_path: Path) -> None:
    work_dir = tmp_path / "work"
    dispatch_dir = work_dir / "dispatch"
    dispatch_dir.mkdir(parents=True, exist_ok=True)
    _write_fresh_json(work_dir / ".rejudge_pending.json", {"ids": ["C-05"], "built_at": time.time() + 5})

    mod, _, _ = _load_workflow_module(
        {"work_dir": str(work_dir), "mode": "repair_and_rejudge", "ids": ["C-05"], "director_id": "d1"}
    )
    summaries: List[str] = []

    async def _fake_run_cli(cmd: str, summary: str, env_extra: Optional[Dict[str, str]] = None) -> str:
        summaries.append(summary)
        if summary == "C2C stage surgical rejudge":
            _write_manifest(dispatch_dir / "judges.json", 1, "Rejudge")
        return "Command exited with code 0."

    mod.run_cli = _fake_run_cli
    asyncio.run(mod.run_c2c_workflow())
    assert "C2C dispatch repair" not in summaries
    assert summaries == [
        "C2C stage surgical rejudge",
        "C2C stage rejudge-compare",
        "C2C post-repair stage gates",
    ]
    assert not (work_dir / ".rejudge_pending.json").exists()


def test_full_pipeline_runs_internal_stage6b_when_gates_exit_nonzero(tmp_path: Path) -> None:
    work_dir = tmp_path / "work"
    dispatch_dir = work_dir / "dispatch"
    shards_dir = work_dir / "shards"
    dispatch_dir.mkdir(parents=True, exist_ok=True)
    shards_dir.mkdir(parents=True, exist_ok=True)
    # Mark shards already compiled so post_cta skips Stage 2-3
    (shards_dir / "pre_shard_manifest.json").write_text(json.dumps({"shards": [{"shard_id": "shard_01"}]}), encoding="utf-8")
    (shards_dir / "shard_01.json").write_text(json.dumps({"templates": []}), encoding="utf-8")

    mod, _, _ = _load_workflow_module(
        {"work_dir": str(work_dir), "mode": "post_cta_pipeline", "max_repair_rounds": 2, "director_id": "d1"}
    )
    summaries: List[str] = []
    gates_calls = {"n": 0}

    async def _fake_run_cli(cmd: str, summary: str, env_extra: Optional[Dict[str, str]] = None) -> str:
        summaries.append(summary)
        if summary == "C2C dispatch judges":
            _write_manifest(dispatch_dir / "judges.json", 1, "Judge")
        elif summary == "C2C stage gates":
            gates_calls["n"] += 1
            (work_dir / "repair_matrix.json").write_text(
                json.dumps({"failing_competencies": ["C-01"]}), encoding="utf-8"
            )
            raise RuntimeError("CLI command failed (C2C stage gates) with exit code 1")
        elif summary == "C2C stage repair-matrix":
            (work_dir / "repair_matrix.json").write_text(
                json.dumps({"failing_competencies": ["C-01"]}), encoding="utf-8"
            )
        elif summary == "C2C dispatch repair":
            _write_manifest(dispatch_dir / "repair.json", 1, "Repair")
        elif summary == "C2C stage surgical rejudge":
            _write_manifest(dispatch_dir / "judges.json", 1, "Rejudge")
        elif summary == "C2C post-repair stage gates":
            # Clean pass on post-repair gates
            return "Command exited with code 0."
        return "Command exited with code 0."

    mod.run_cli = _fake_run_cli
    res = asyncio.run(mod.run_c2c_workflow())
    assert gates_calls["n"] == 1
    assert res["repair_rounds_executed"] == 1
    assert res["remaining_failing_ids"] == []
    assert "C2C stage repair-matrix" in summaries
    assert "C2C stage surgical rejudge" in summaries


def test_repair_and_rejudge_runs_lqas_when_rejudge_triggers_override(tmp_path: Path) -> None:
    work_dir = tmp_path / "work"
    dispatch_dir = work_dir / "dispatch"
    dispatch_dir.mkdir(parents=True, exist_ok=True)
    _write_fresh_json(work_dir / ".rejudge_pending.json", {"ids": ["C-01"], "built_at": time.time() + 5})

    mod, _, _ = _load_workflow_module(
        {"work_dir": str(work_dir), "mode": "repair_and_rejudge", "ids": ["C-01"], "director_id": "d1"}
    )
    summaries: List[str] = []

    async def _fake_run_cli(cmd: str, summary: str, env_extra: Optional[Dict[str, str]] = None) -> str:
        summaries.append(summary)
        if summary == "C2C stage surgical rejudge":
            _write_manifest(dispatch_dir / "judges.json", 1, "Rejudge")
        elif summary == "C2C stage rejudge-compare":
            _write_fresh_json(
                work_dir / "judge_report_rejudge.json",
                {"lqas_followup_required": True, "single_seed_override_templates": ["T-C01-02"]},
            )
        elif summary == "C2C stage lqas-rejudge":
            _write_manifest(dispatch_dir / "judges.json", 1, "LQAS")
        return "Command exited with code 0."

    mod.run_cli = _fake_run_cli
    asyncio.run(mod.run_c2c_workflow())
    assert "C2C stage lqas-rejudge" in summaries
    assert "C2C stage lqas-compare" in summaries


def test_quota_circuit_breaker_aborts_wave_on_long_reset(tmp_path: Path) -> None:
    import pytest

    manifest = tmp_path / "judges.json"
    _write_manifest(manifest, 5, "Judge")
    mod, _, _ = _load_workflow_module(
        {"quota_retry_backoff_s": [0.0], "retry_backoff_s": [0.0], "startup_stagger_s": 0.0, "max_concurrency": 1}
    )
    calls = {"n": 0}

    async def _quota_failing_agent(**kwargs: Any) -> str:
        calls["n"] += 1
        raise RuntimeError("RESOURCE_EXHAUSTED (code 429): Individual quota reached. Resets in 4h23m50s")

    mod.agent = _quota_failing_agent
    with pytest.raises(mod.QuotaPausedError, match=r"PAUSED_QUOTA"):
        asyncio.run(mod.run_wave_from_manifest(str(manifest), "Quota Breaker"))
    # Must abort immediately on long reset instead of 5 workers x 5 attempts = 25 calls
    assert calls["n"] < 5


def test_course_budget_guard_flags_overrun() -> None:
    import sys

    c2c_dir = str((Path(__file__).resolve().parents[2] / ".agents" / "skills" / "content-to-course").resolve())
    if c2c_dir not in sys.path:
        sys.path.insert(0, c2c_dir)
    from budget_guard import check_course_budget

    over, msg = check_course_budget(25_000_000)
    assert over is True
    assert msg and "COURSE_BUDGET_EXCEEDED" in msg

    ok, msg_ok = check_course_budget(10_000_000)
    assert ok is False
    assert msg_ok is None
