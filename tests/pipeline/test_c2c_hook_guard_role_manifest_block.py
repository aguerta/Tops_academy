"""Role-based blocking of manifests / cta.json for architect, shard and repair subagents."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Dict

import pytest


def _load():
    root = Path(__file__).resolve().parents[2]
    p = root / ".agents" / "skills" / "content-to-course" / "c2c_hook_guard.py"
    spec = importlib.util.spec_from_file_location("c2c_hook_guard", p)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["c2c_hook_guard"] = mod
    spec.loader.exec_module(mod)
    return mod


guard = _load()
DIRECTOR = "dir-role-001"


def _env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, worker_id: str, first_msg: str) -> str:
    home = tmp_path / "home"
    monkeypatch.setattr(guard, "USER_HOME", home)
    guard._LOCK_CACHE.clear()
    guard._DIRECTOR_TRANSCRIPT_CACHE.clear()
    guard._CALLER_ROLE_CACHE.clear()
    work = tmp_path / "work"
    work.mkdir()
    lock = work / ".c2c_subagent_lock.json"
    lock.write_text(
        json.dumps({"active": True, "director_conversation_id": DIRECTOR, "work_dir": str(work)}),
        encoding="utf-8",
    )
    brain = home / ".gemini" / "antigravity" / "brain"
    d = brain / DIRECTOR / ".system_generated" / "logs"
    d.mkdir(parents=True)
    (d / "transcript.jsonl").write_text(
        json.dumps({"type": "GENERIC", "source": "MODEL", "content": f"spawned {worker_id}"}) + "\n",
        encoding="utf-8",
    )
    w = brain / worker_id / ".system_generated" / "logs"
    w.mkdir(parents=True)
    (w / "transcript.jsonl").write_text(
        json.dumps({"type": "USER_INPUT", "content": first_msg}) + "\n", encoding="utf-8"
    )
    return str(lock)


def _payload(worker_id: str, tool: str, args: Dict[str, Any]) -> Dict[str, Any]:
    return {"conversationId": worker_id, "toolCall": {"name": tool, "args": args}}


ROLES = [
    ("w-arch", "You are CTA Architect part_01. [SCOPE-LOCK]"),
    ("w-shard", "Subagente `c2c_shard_author` shard_01"),
    ("w-rep", "Subagente `c2c_repair` Repair Engineer C-1"),
]


@pytest.mark.parametrize("worker_id,msg", ROLES)
@pytest.mark.parametrize("name", ["pre_cta_manifest.json", "pre_shard_manifest.json"])
def test_manifest_read_file_denied(tmp_path, monkeypatch, worker_id, msg, name):
    lock = _env(tmp_path, monkeypatch, worker_id, msg)
    r = guard.process_hook(
        _payload(worker_id, "read_file", {"Path": f"/x/work/{name}"}), custom_lock_file=lock
    )
    assert r["decision"] == "deny"


@pytest.mark.parametrize("worker_id,msg", ROLES)
@pytest.mark.parametrize(
    "cmd",
    [
        "Get-Content work/pre_cta_manifest.json",
        "cat work/shards/pre_shard_manifest.json",
    ],
)
def test_manifest_shell_denied(tmp_path, monkeypatch, worker_id, msg, cmd):
    lock = _env(tmp_path, monkeypatch, worker_id, msg)
    r = guard.process_hook(_payload(worker_id, "run_command", {"CommandLine": cmd}), custom_lock_file=lock)
    assert r["decision"] == "deny"


@pytest.mark.parametrize("worker_id,msg", ROLES[1:])
def test_cta_json_denied_for_shard_and_repair(tmp_path, monkeypatch, worker_id, msg):
    lock = _env(tmp_path, monkeypatch, worker_id, msg)
    (tmp_path / "work" / "cta.json").write_text("{}", encoding="utf-8")
    r = guard.process_hook(
        _payload(worker_id, "read_file", {"Path": str(tmp_path / "work" / "cta.json")}),
        custom_lock_file=lock,
    )
    assert r["decision"] == "deny"
    r2 = guard.process_hook(
        _payload(worker_id, "run_command", {"CommandLine": "cat work/cta.json"}),
        custom_lock_file=lock,
    )
    assert r2["decision"] == "deny"


def test_architect_may_run_compile_with_manifest(tmp_path, monkeypatch):
    lock = _env(tmp_path, monkeypatch, *ROLES[0])
    cmd = "python .agents/skills/content-to-course/compile_cta.py --manifest work/pre_cta_manifest.json"
    r = guard.process_hook(_payload("w-arch", "run_command", {"CommandLine": cmd}), custom_lock_file=lock)
    assert r["decision"] == "allow"
