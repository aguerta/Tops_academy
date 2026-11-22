"""Tests for Stream 1A: Telemetry & Conversation ID Hardening."""

import ast
import contextlib
import io
import json
import os
import sys
import time
from pathlib import Path
from typing import Optional

import pytest

SKILL_DIR = Path(__file__).resolve().parents[2] / ".agents" / "skills" / "content-to-course"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

import telemetry_collector
from run import PipelineRunner


def _write_transcript(brain_dir: Path, conv_id: str, lines: list[str], mtime_offset: float = 0.0) -> Path:
    t_file = brain_dir / conv_id / ".system_generated" / "logs" / "transcript.jsonl"
    t_file.parent.mkdir(parents=True, exist_ok=True)
    t_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    if mtime_offset != 0.0:
        now = time.time() + mtime_offset
        os.utime(t_file, (now, now))
    return t_file


def _create_synthetic_pdf(target_path: Path, title: str = "Hardening Test") -> None:
    try:
        import pymupdf as fitz
    except ImportError:
        import fitz

    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 72), f"{title}\nSection 1: Foundations\nLet X ~ N(0, 1).", fontsize=11)
    doc.save(str(target_path))
    doc.close()


def test_find_conversation_id_precedence_chain(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify strict precedence: env (ANTIGRAVITY_CONVERSATION_ID / C2C_DIRECTOR_ID) -> lockfile -> state.json -> brain."""
    work_dir = tmp_path / "courses" / "demo_course" / "work"
    work_dir.mkdir(parents=True)
    brain_dir = tmp_path / "brain"
    brain_dir.mkdir()

    monkeypatch.setenv("ANTIGRAVITY_BRAIN_DIR", str(brain_dir))
    monkeypatch.delenv("ANTIGRAVITY_CONVERSATION_ID", raising=False)
    monkeypatch.delenv("C2C_DIRECTOR_ID", raising=False)

    # Populate all 4 sources with distinct IDs
    _write_transcript(
        brain_dir,
        "conv-brain-004",
        [json.dumps({"role": "user", "text": f"Run director for {work_dir.as_posix()}"})],
    )
    (work_dir / "state.json").write_text(
        json.dumps({"conversation_id": "conv-state-003"}), encoding="utf-8"
    )
    (work_dir / ".c2c_subagent_lock.json").write_text(
        json.dumps({"director_conversation_id": "conv-lock-002"}), encoding="utf-8"
    )
    monkeypatch.setenv("C2C_DIRECTOR_ID", "conv-env-director-001b")
    monkeypatch.setenv("ANTIGRAVITY_CONVERSATION_ID", "conv-env-ag-001a")

    assert telemetry_collector.find_conversation_id_for_work_dir(work_dir) == "conv-env-ag-001a"

    monkeypatch.delenv("ANTIGRAVITY_CONVERSATION_ID")
    assert telemetry_collector.find_conversation_id_for_work_dir(work_dir) == "conv-env-director-001b"

    monkeypatch.delenv("C2C_DIRECTOR_ID")
    assert telemetry_collector.find_conversation_id_for_work_dir(work_dir) == "conv-lock-002"

    (work_dir / ".c2c_subagent_lock.json").unlink()
    assert telemetry_collector.find_conversation_id_for_work_dir(work_dir) == "conv-state-003"

    (work_dir / "state.json").unlink()
    assert telemetry_collector.find_conversation_id_for_work_dir(work_dir) == "conv-brain-004"


@pytest.mark.parametrize(
    "worker_header",
    [
        "[SCOPE-LOCK] Write only to shard_01.py",
        "You are Shard Author for shard_01",
        "You are CTA Architect for unit 1",
        "You are Repair Engineer fixing shard_02",
        "You are Blind Judge evaluating competency",
        "Work order: implement shard 01 without touching anything else",
    ],
)
def test_brain_fallback_rejects_worker_transcripts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, worker_header: str
) -> None:
    """Worker subagent transcripts in brain/ must be skipped even when newer than director transcript."""
    work_dir = tmp_path / "courses" / "demo_course" / "work"
    work_dir.mkdir(parents=True)
    brain_dir = tmp_path / "brain"
    brain_dir.mkdir()

    monkeypatch.setenv("ANTIGRAVITY_BRAIN_DIR", str(brain_dir))
    monkeypatch.delenv("ANTIGRAVITY_CONVERSATION_ID", raising=False)
    monkeypatch.delenv("C2C_DIRECTOR_ID", raising=False)

    # Older valid director transcript
    _write_transcript(
        brain_dir,
        "conv-director-valid",
        [json.dumps({"role": "user", "text": f"python run.py --stage bootstrap --work-dir {work_dir.as_posix()}"})],
        mtime_offset=-60.0,
    )
    # Newer worker transcript referencing the exact same work_dir
    _write_transcript(
        brain_dir,
        "conv-worker-noise",
        [json.dumps({"role": "user", "text": f"{worker_header} | work_dir={work_dir.as_posix()}"})],
        mtime_offset=60.0,
    )

    assert telemetry_collector.find_conversation_id_for_work_dir(work_dir) == "conv-director-valid"


def test_brain_fallback_allows_work_order_with_bootstrap_command(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A director transcript containing 'Work order:' together with 'run.py --stage bootstrap' is NOT rejected."""
    work_dir = tmp_path / "courses" / "demo_course" / "work"
    work_dir.mkdir(parents=True)
    brain_dir = tmp_path / "brain"
    brain_dir.mkdir()

    monkeypatch.setenv("ANTIGRAVITY_BRAIN_DIR", str(brain_dir))
    monkeypatch.delenv("ANTIGRAVITY_CONVERSATION_ID", raising=False)
    monkeypatch.delenv("C2C_DIRECTOR_ID", raising=False)

    _write_transcript(
        brain_dir,
        "conv-director-bootstrap",
        [
            json.dumps(
                {
                    "role": "user",
                    "text": f"Work order: execute run.py --stage bootstrap for {work_dir.as_posix()}",
                }
            )
        ],
    )

    assert telemetry_collector.find_conversation_id_for_work_dir(work_dir) == "conv-director-bootstrap"


def test_run_stage_bootstrap_emits_workflow_script_path_and_telemetry_conv_id(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """--stage bootstrap must emit an existing absolute workflow_script_path and pass conv_id to telemetry."""
    pdf_path = tmp_path / "sample.pdf"
    _create_synthetic_pdf(pdf_path)

    work_dir = tmp_path / "work"
    expected_cid = "director-conv-bootstrap-123"
    monkeypatch.delenv("ANTIGRAVITY_CONVERSATION_ID", raising=False)
    monkeypatch.delenv("C2C_DIRECTOR_ID", raising=False)

    runner = PipelineRunner(
        course_id="hardening_test_course",
        pdf=str(pdf_path),
        work_dir=str(work_dir),
        director_id=expected_cid,
    )

    stdout_buf = io.StringIO()
    with contextlib.redirect_stdout(stdout_buf):
        summary = runner.run_stage_bootstrap()

    printed = json.loads(stdout_buf.getvalue().strip())
    for payload in (summary, printed):
        wf_path_str = payload.get("workflow_script_path")
        assert wf_path_str, "workflow_script_path missing from bootstrap output"
        wf_path = Path(wf_path_str)
        assert wf_path.is_absolute(), f"workflow_script_path must be absolute: {wf_path}"
        assert wf_path.is_file(), f"workflow_script_path does not exist: {wf_path}"
        assert wf_path.name == "c2c_wave_workflow.py"

    snap_file = work_dir / "telemetry" / "00b_bootstrap.json"
    assert snap_file.is_file()
    snap = json.loads(snap_file.read_text(encoding="utf-8"))
    assert snap["conversation_id"] == expected_cid


def test_all_record_stage_telemetry_calls_in_run_py_pass_conv_id() -> None:
    """Static guard: every record_stage_telemetry(...) call in run.py must pass conv_id=self._resolve_conversation_id()."""
    run_py = SKILL_DIR / "run.py"
    tree = ast.parse(run_py.read_text(encoding="utf-8-sig"))

    calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            name: Optional[str] = None
            if isinstance(func, ast.Name):
                name = func.id
            elif isinstance(func, ast.Attribute):
                name = func.attr
            if name == "record_stage_telemetry":
                calls.append(node)

    assert len(calls) >= 10, f"Expected >= 10 record_stage_telemetry calls, found {len(calls)}"
    for call in calls:
        conv_kw = [kw for kw in call.keywords if kw.arg == "conv_id"]
        assert conv_kw, f"record_stage_telemetry at line {call.lineno} missing conv_id keyword"
        val_src = ast.unparse(conv_kw[0].value)
        assert val_src == "self._resolve_conversation_id()", (
            f"record_stage_telemetry at line {call.lineno} has conv_id={val_src}, "
            "expected self._resolve_conversation_id()"
        )
