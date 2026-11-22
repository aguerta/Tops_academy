"""Tests for c2c_hook_guard anti-race-condition barrier on run_workflow / c2c_wave_workflow.py."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

import pytest


def _load_hook_guard():
    repo_root = Path(__file__).resolve().parents[2]
    guard_path = repo_root / ".agents" / "skills" / "content-to-course" / "c2c_hook_guard.py"
    spec = importlib.util.spec_from_file_location("c2c_hook_guard", guard_path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules["c2c_hook_guard"] = mod
    spec.loader.exec_module(mod)
    return mod


guard = _load_hook_guard()

BLOCKED_COMMANDS: List[str] = [
    "python .agents/skills/content-to-course/run.py --stage rejudge-compare --work-dir work",
    "python .agents/skills/content-to-course/run.py --stage judge-compare --work-dir work",
    "python .agents/skills/content-to-course/run.py --stage gates --work-dir work",
    "python .agents/skills/content-to-course/run.py --stage templates --work-dir work",
    "python .agents/skills/content-to-course/run.py --stage build --work-dir work",
    "python .agents/skills/content-to-course/run.py --stage verify --work-dir work",
    "python .agents/skills/content-to-course/run.py --stage publish --work-dir work",
    "python .agents/skills/content-to-course/run.py --stage repair-matrix --work-dir work",
    "python .agents/skills/content-to-course/dispatch.py dispatch-repair --work-dir work --ids C-1",
    "python .agents/skills/content-to-course/dispatch.py dispatch-judges --work-dir work",
    "python .agents/skills/content-to-course/dispatch.py dispatch-authors --work-dir work",
]


def _setup_director_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, director_id: str) -> tuple[Path, Path]:
    fake_home = tmp_path / "home"
    monkeypatch.setattr(guard, "USER_HOME", fake_home)
    guard._LOCK_CACHE.clear()
    guard._DIRECTOR_TRANSCRIPT_CACHE.clear()

    work_dir = tmp_path / "work"
    (work_dir / "dispatch").mkdir(parents=True)
    lock_path = work_dir / ".c2c_subagent_lock.json"
    lock_path.write_text(
        json.dumps(
            {
                "active": True,
                "director_conversation_id": director_id,
                "work_dir": str(work_dir),
            }
        ),
        encoding="utf-8",
    )

    t_dir = fake_home / ".gemini" / "antigravity" / "brain" / director_id / ".system_generated" / "logs"
    t_dir.mkdir(parents=True)
    return lock_path, t_dir / "transcript.jsonl"


def _make_cmd_payload(director_id: str, cmd: str) -> Dict[str, Any]:
    return {
        "conversationId": director_id,
        "toolCall": {
            "name": "run_command",
            "args": {"CommandLine": cmd},
        },
    }


@pytest.mark.parametrize("cmd", BLOCKED_COMMANDS)
def test_in_flight_run_workflow_task_blocks_downstream_stages_and_dispatches(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, cmd: str
):
    director_id = "dir-wf-001"
    lock_path, t_file = _setup_director_env(tmp_path, monkeypatch, director_id)

    events = [
        {
            "type": "PLANNER_RESPONSE",
            "source": "MODEL",
            "tool_calls": [
                {
                    "name": "run_workflow",
                    "arguments": {"workflow": "c2c_wave_workflow.py", "stage": "authors"},
                }
            ],
        },
        {
            "type": "GENERIC",
            "source": "SYSTEM",
            "content": (
                f"Tool is running as a background task with task id: {director_id}/task-77\n"
                "Task Description: Execute wave workflow"
            ),
        },
    ]
    t_file.write_text("\n".join(json.dumps(e) for e in events) + "\n", encoding="utf-8")

    denied = guard.process_hook(_make_cmd_payload(director_id, cmd), custom_lock_file=str(lock_path))
    assert denied["decision"] == "deny"
    assert "task-77" in denied["reason"]

    # Once task-77 finishes, the downstream command is allowed
    events.append(
        {
            "type": "GENERIC",
            "source": "SYSTEM",
            "content": f'Task id "{director_id}/task-77" finished with result: OK',
        }
    )
    t_file.write_text("\n".join(json.dumps(e) for e in events) + "\n", encoding="utf-8")

    allowed = guard.process_hook(_make_cmd_payload(director_id, cmd), custom_lock_file=str(lock_path))
    assert allowed == {"decision": "allow"}


def test_c2c_wave_workflow_in_task_description_blocks_until_failed_or_finished(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    director_id = "dir-wf-002"
    lock_path, t_file = _setup_director_env(tmp_path, monkeypatch, director_id)

    events = [
        {
            "type": "GENERIC",
            "source": "SYSTEM",
            "content": (
                "Tool is running as a background task with task id: task-77\n"
                "Task Description: python .agents/skills/content-to-course/c2c_wave_workflow.py --work-dir work"
            ),
        }
    ]
    t_file.write_text("\n".join(json.dumps(e) for e in events) + "\n", encoding="utf-8")

    for cmd in (
        "python .agents/skills/content-to-course/run.py --stage rejudge-compare --work-dir work",
        "python .agents/skills/content-to-course/dispatch.py dispatch-repair --work-dir work --ids C-1",
    ):
        denied = guard.process_hook(_make_cmd_payload(director_id, cmd), custom_lock_file=str(lock_path))
        assert denied["decision"] == "deny"
        assert "task-77" in denied["reason"]

    # Closure via failure message also clears the barrier
    events.append(
        {
            "type": "GENERIC",
            "source": "SYSTEM",
            "content": 'Task id "task-77" failed with exit code 1',
        }
    )
    t_file.write_text("\n".join(json.dumps(e) for e in events) + "\n", encoding="utf-8")

    for cmd in (
        "python .agents/skills/content-to-course/run.py --stage rejudge-compare --work-dir work",
        "python .agents/skills/content-to-course/dispatch.py dispatch-repair --work-dir work --ids C-1",
    ):
        allowed = guard.process_hook(_make_cmd_payload(director_id, cmd), custom_lock_file=str(lock_path))
        assert allowed == {"decision": "allow"}


def test_cross_course_isolation_allows_non_ascii_course_id(tmp_path):
    """Non-ASCII characters (e.g., ó) in course_id must not be truncated by Cross-Course Isolation."""
    guard._LOCK_CACHE.clear()
    worker_id = "worker-nonascii-1"
    lock_path = tmp_path / ".c2c_subagent_lock.json"
    lock_path.write_text(
        json.dumps(
            {
                "active": True,
                "director_conversation_id": "director-nonascii",
                "course_id": "mateco_4_optimización_v20",
                "active_subagents": [worker_id],
                "subagent_roles": {worker_id: "cta_harmonizer"},
            }
        ),
        encoding="utf-8",
    )

    own_read = {
        "conversation_id": worker_id,
        "toolCall": {
            "name": "read_file",
            "arguments": {
                "Path": "d:/Augusto/personal_portfolio/Tops_academy/courses/mateco_4_optimización_v20/work/cta_parts/part_01.json"
            },
        },
    }
    assert guard.process_hook(own_read, custom_lock_file=str(lock_path)) == {"decision": "allow"}

    sibling_read = {
        "conversation_id": worker_id,
        "toolCall": {
            "name": "read_file",
            "arguments": {
                "Path": "d:/Augusto/personal_portfolio/Tops_academy/courses/other_course/work/cta_parts/part_01.json"
            },
        },
    }
    denied = guard.process_hook(sibling_read, custom_lock_file=str(lock_path))
    assert denied["decision"] == "deny"
    assert "Cross-Course Isolation" in denied["reason"]

