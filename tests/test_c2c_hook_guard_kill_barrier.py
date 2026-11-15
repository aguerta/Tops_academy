"""Tests for c2c_hook_guard kill/kill_all N/N wave output barrier."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Dict

import pytest


def _load_hook_guard():
    repo_root = Path(__file__).resolve().parents[1]
    guard_path = repo_root / ".agents" / "skills" / "content-to-course" / "c2c_hook_guard.py"
    spec = importlib.util.spec_from_file_location("c2c_hook_guard", guard_path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules["c2c_hook_guard"] = mod
    spec.loader.exec_module(mod)
    return mod


guard = _load_hook_guard()


def _make_director_kill_payload(director_id: str, action: str, conv_ids=None) -> Dict[str, Any]:
    args: Dict[str, Any] = {"Action": action}
    if conv_ids is not None:
        args["ConversationIds"] = conv_ids
    return {
        "conversationId": director_id,
        "toolCall": {
            "name": "manage_subagents",
            "args": args,
        },
    }


def _setup_lock(work_dir: Path, director_id: str = "dir-uuid-001") -> Path:
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
    return lock_path


def test_cta_wave_denies_kill_and_kill_all_when_json_missing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(guard, "USER_HOME", tmp_path / "home")
    guard._LOCK_CACHE.clear()

    work_dir = tmp_path / "work"
    dispatch_dir = work_dir / "dispatch"
    items_dir = dispatch_dir / "items"
    items_dir.mkdir(parents=True)

    lock_path = _setup_lock(work_dir)

    out_1 = work_dir / "cta_parts" / "part_01.json"
    out_2 = work_dir / "cta_parts" / "part_02.json"
    out_1.parent.mkdir(parents=True, exist_ok=True)
    out_1.write_text('{"ok": true}', encoding="utf-8")
    # out_2 intentionally missing

    item_1 = items_dir / "cta_01.json"
    item_2 = items_dir / "cta_02.json"
    item_1.write_text(json.dumps({"output_json": str(out_1)}), encoding="utf-8")
    item_2.write_text(json.dumps({"output_json": str(out_2)}), encoding="utf-8")

    (dispatch_dir / "cta.json").write_text(
        json.dumps({"stage": "cta", "item_files": [str(item_1), str(item_2)]}),
        encoding="utf-8",
    )

    res_kill = guard.process_hook(
        _make_director_kill_payload("dir-uuid-001", "kill", ["worker-uuid-1"]),
        custom_lock_file=str(lock_path),
    )
    assert res_kill["decision"] == "deny"
    assert "part_02.json" in res_kill["reason"]

    res_kill_all = guard.process_hook(
        _make_director_kill_payload("dir-uuid-001", "kill_all"),
        custom_lock_file=str(lock_path),
    )
    assert res_kill_all["decision"] == "deny"
    assert "part_02.json" in res_kill_all["reason"]


def test_shards_wave_denies_when_missing_and_allows_kill_all_when_complete(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setattr(guard, "USER_HOME", tmp_path / "home")
    guard._LOCK_CACHE.clear()

    work_dir = tmp_path / "work"
    dispatch_dir = work_dir / "dispatch"
    items_dir = dispatch_dir / "items"
    shards_dir = work_dir / "shards"
    tpl_dir = work_dir / "templates"
    items_dir.mkdir(parents=True)
    shards_dir.mkdir(parents=True)
    tpl_dir.mkdir(parents=True)

    lock_path = _setup_lock(work_dir)

    s1_json = shards_dir / "shard_01.json"
    s2_json = shards_dir / "shard_02.json"
    s1_json.write_text(json.dumps({"shard_id": "shard_01", "compiled_status": "PASS"}), encoding="utf-8")
    (shards_dir / "shard_01.cert.json").write_text(
        json.dumps({"artifact_id": "shard_01", "passed_50_seeds": True}),
        encoding="utf-8",
    )
    # s2_json missing initially

    (tpl_dir / "C-1.json").write_text("{}", encoding="utf-8")
    # C-2.json missing initially

    item_1 = items_dir / "shard_01.json"
    item_2 = items_dir / "shard_02.json"
    item_1.write_text(
        json.dumps(
            {
                "shard_id": "shard_01",
                "output_json": str(s1_json),
                "assigned_competencies": ["C-1"],
            }
        ),
        encoding="utf-8",
    )
    item_2.write_text(
        json.dumps(
            {
                "shard_id": "shard_02",
                "output_json": str(s2_json),
                "assigned_competencies": ["C-2"],
            }
        ),
        encoding="utf-8",
    )

    (dispatch_dir / "shards_wave_1.json").write_text(
        json.dumps({"stage": "shards", "item_files": [str(item_1), str(item_2)]}),
        encoding="utf-8",
    )

    denied = guard.process_hook(
        _make_director_kill_payload("dir-uuid-001", "kill_all"),
        custom_lock_file=str(lock_path),
    )
    assert denied["decision"] == "deny"
    assert "shard_02.json" in denied["reason"] or "C-2.json" in denied["reason"]

    # Create remaining outputs WITH certification
    s2_json.write_text(json.dumps({"shard_id": "shard_02", "compiled_status": "PASS"}), encoding="utf-8")
    (shards_dir / "shard_02.cert.json").write_text(
        json.dumps({"artifact_id": "shard_02", "passed_50_seeds": True}),
        encoding="utf-8",
    )
    (tpl_dir / "C-2.json").write_text("{}", encoding="utf-8")

    allowed = guard.process_hook(
        _make_director_kill_payload("dir-uuid-001", "kill_all"),
        custom_lock_file=str(lock_path),
    )
    assert allowed == {"decision": "allow"}


def test_individual_kill_allowed_when_all_cids_have_blocked_transcript(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    fake_home = tmp_path / "home"
    monkeypatch.setattr(guard, "USER_HOME", fake_home)
    guard._LOCK_CACHE.clear()

    work_dir = tmp_path / "work"
    dispatch_dir = work_dir / "dispatch"
    items_dir = dispatch_dir / "items"
    items_dir.mkdir(parents=True)

    lock_path = _setup_lock(work_dir)

    missing_out = work_dir / "shards" / "shard_01.json"
    item_1 = items_dir / "shard_01.json"
    item_1.write_text(
        json.dumps(
            {
                "shard_id": "shard_01",
                "output_json": str(missing_out),
                "assigned_competencies": ["C-1"],
            }
        ),
        encoding="utf-8",
    )
    (dispatch_dir / "shards.json").write_text(
        json.dumps({"stage": "shards", "item_files": [str(item_1)]}),
        encoding="utf-8",
    )

    blocked_uuid = "worker-blocked-1234"
    t_dir = fake_home / ".gemini" / "antigravity" / "brain" / blocked_uuid / ".system_generated" / "logs"
    t_dir.mkdir(parents=True)
    (t_dir / "transcript.jsonl").write_text(
        '{"event": "done", "text": "BLOCKED: missing source PDF page"}\n',
        encoding="utf-8",
    )

    # Individual kill on BLOCKED worker is allowed even though wave JSONs are missing
    res_blocked = guard.process_hook(
        _make_director_kill_payload("dir-uuid-001", "kill", [blocked_uuid]),
        custom_lock_file=str(lock_path),
    )
    assert res_blocked == {"decision": "allow"}

    # If a non-blocked worker is included, individual kill must still be denied
    res_mixed = guard.process_hook(
        _make_director_kill_payload("dir-uuid-001", "kill", [blocked_uuid, "worker-normal-9999"]),
        custom_lock_file=str(lock_path),
    )
    assert res_mixed["decision"] == "deny"


def test_judges_wave_requires_output_size_over_20_bytes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(guard, "USER_HOME", tmp_path / "home")
    guard._LOCK_CACHE.clear()

    work_dir = tmp_path / "work"
    dispatch_dir = work_dir / "dispatch"
    items_dir = dispatch_dir / "items"
    items_dir.mkdir(parents=True)

    lock_path = _setup_lock(work_dir)

    judge_out = work_dir / "judge_responses_01.json"
    judge_out.write_text("{}", encoding="utf-8")  # <= 20 bytes

    item_1 = items_dir / "judge_01.json"
    item_1.write_text(json.dumps({"output_target": str(judge_out)}), encoding="utf-8")
    (dispatch_dir / "judges.json").write_text(
        json.dumps({"stage": "judges", "item_files": [str(item_1)]}),
        encoding="utf-8",
    )

    denied = guard.process_hook(
        _make_director_kill_payload("dir-uuid-001", "kill_all"),
        custom_lock_file=str(lock_path),
    )
    assert denied["decision"] == "deny"

    judge_out.write_text('{"verdicts": [{"id": "Q1", "pass": true}]}', encoding="utf-8")
    allowed = guard.process_hook(
        _make_director_kill_payload("dir-uuid-001", "kill_all"),
        custom_lock_file=str(lock_path),
    )
    assert allowed == {"decision": "allow"}


def test_authors_manifest_denies_failed_shard_even_when_json_exists(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setattr(guard, "USER_HOME", tmp_path / "home")
    guard._LOCK_CACHE.clear()

    work_dir = tmp_path / "work"
    dispatch_dir = work_dir / "dispatch"
    items_dir = dispatch_dir / "items"
    shards_dir = work_dir / "shards"
    tpl_dir = work_dir / "templates"
    items_dir.mkdir(parents=True)
    shards_dir.mkdir(parents=True)
    tpl_dir.mkdir(parents=True)

    lock_path = _setup_lock(work_dir)

    s1_json = shards_dir / "shard_01.json"
    # Simulate compile_shard failure: receipt + template exist, but compiled_status=FAIL and no .cert.json
    s1_json.write_text(json.dumps({"shard_id": "shard_01", "compiled_status": "FAIL"}), encoding="utf-8")
    (tpl_dir / "C-1.json").write_text("{}", encoding="utf-8")

    item_1 = items_dir / "author_01.json"
    item_1.write_text(
        json.dumps({"shard_id": "shard_01", "output_json": str(s1_json), "assigned_competencies": ["C-1"]}),
        encoding="utf-8",
    )
    (dispatch_dir / "authors.json").write_text(
        json.dumps({"stage": "authors", "item_files": [str(item_1)]}),
        encoding="utf-8",
    )

    denied = guard.process_hook(
        _make_director_kill_payload("dir-uuid-001", "kill_all"),
        custom_lock_file=str(lock_path),
    )
    assert denied["decision"] == "deny"
    assert "cert.json" in denied["reason"] or "PASS" in denied["reason"]

    # Certify shard_01 cleanly
    s1_json.write_text(json.dumps({"shard_id": "shard_01", "compiled_status": "PASS"}), encoding="utf-8")
    (shards_dir / "shard_01.cert.json").write_text(
        json.dumps({"artifact_id": "shard_01", "passed_50_seeds": True}),
        encoding="utf-8",
    )
    allowed = guard.process_hook(
        _make_director_kill_payload("dir-uuid-001", "kill_all"),
        custom_lock_file=str(lock_path),
    )
    assert allowed == {"decision": "allow"}


def test_repair_wave_denies_stale_cert_and_allows_fresh_cert(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    import os
    from datetime import datetime, timezone

    monkeypatch.setattr(guard, "USER_HOME", tmp_path / "home")
    guard._LOCK_CACHE.clear()

    work_dir = tmp_path / "work"
    dispatch_dir = work_dir / "dispatch"
    items_dir = dispatch_dir / "items"
    shards_dir = work_dir / "shards"
    tpl_dir = work_dir / "templates"
    items_dir.mkdir(parents=True)
    shards_dir.mkdir(parents=True)
    tpl_dir.mkdir(parents=True)

    lock_path = _setup_lock(work_dir)
    now_ts = datetime.now(timezone.utc).timestamp()
    stale_ts = now_ts - 600.0

    s1_json = shards_dir / "shard_01.json"
    s1_cert = shards_dir / "shard_01.cert.json"
    s1_json.write_text(
        json.dumps({"shard_id": "shard_01", "compiled_status": "PASS", "compiled_at": stale_ts}),
        encoding="utf-8",
    )
    s1_cert.write_text(
        json.dumps({"artifact_id": "shard_01", "passed_50_seeds": True, "created_at": stale_ts}),
        encoding="utf-8",
    )
    os.utime(s1_json, (stale_ts, stale_ts))
    os.utime(s1_cert, (stale_ts, stale_ts))
    (tpl_dir / "C-1.json").write_text("{}", encoding="utf-8")

    item_1 = items_dir / "repair_01.json"
    item_1.write_text(
        json.dumps({"shard_id": "shard_01", "output_json": str(s1_json), "expected_templates": ["C-1"]}),
        encoding="utf-8",
    )
    dispatch_iso = datetime.fromtimestamp(now_ts, tz=timezone.utc).isoformat()
    (dispatch_dir / "repair.json").write_text(
        json.dumps({"role": "repair", "dispatched_at": dispatch_iso, "item_files": [str(item_1)]}),
        encoding="utf-8",
    )

    denied = guard.process_hook(
        _make_director_kill_payload("dir-uuid-001", "kill_all"),
        custom_lock_file=str(lock_path),
    )
    assert denied["decision"] == "deny"
    assert "stale pre-repair" in denied["reason"]

    # Refresh receipt + cert after dispatched_at
    fresh_ts = now_ts + 5.0
    s1_json.write_text(
        json.dumps({"shard_id": "shard_01", "compiled_status": "PASS", "compiled_at": fresh_ts}),
        encoding="utf-8",
    )
    s1_cert.write_text(
        json.dumps({"artifact_id": "shard_01", "passed_50_seeds": True, "created_at": fresh_ts}),
        encoding="utf-8",
    )
    allowed = guard.process_hook(
        _make_director_kill_payload("dir-uuid-001", "kill_all"),
        custom_lock_file=str(lock_path),
    )
    assert allowed == {"decision": "allow"}


def test_cta_parts_requires_pass_marker(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(guard, "USER_HOME", tmp_path / "home")
    guard._LOCK_CACHE.clear()

    work_dir = tmp_path / "work"
    dispatch_dir = work_dir / "dispatch"
    items_dir = dispatch_dir / "items"
    cta_parts_dir = work_dir / "cta_parts"
    attempts_dir = cta_parts_dir / ".check_attempts"
    items_dir.mkdir(parents=True)
    attempts_dir.mkdir(parents=True)

    lock_path = _setup_lock(work_dir)
    out_1 = cta_parts_dir / "part_01.json"
    out_1.write_text('{"competencies": [{"id": "C-1"}]}', encoding="utf-8")

    item_1 = items_dir / "cta_01.json"
    item_1.write_text(json.dumps({"output_json": str(out_1)}), encoding="utf-8")
    (dispatch_dir / "cta.json").write_text(
        json.dumps({"stage": "cta", "item_files": [str(item_1)]}),
        encoding="utf-8",
    )

    denied = guard.process_hook(
        _make_director_kill_payload("dir-uuid-001", "kill_all"),
        custom_lock_file=str(lock_path),
    )
    assert denied["decision"] == "deny"
    assert "pass_cta_part_01.json" in denied["reason"]

    (attempts_dir / "pass_cta_part_01.json").write_text(json.dumps({"status": "PASS"}), encoding="utf-8")
    allowed = guard.process_hook(
        _make_director_kill_payload("dir-uuid-001", "kill_all"),
        custom_lock_file=str(lock_path),
    )
    assert allowed == {"decision": "allow"}


def test_director_transcript_blocks_kill_all_and_templates_while_subagents_pending(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    fake_home = tmp_path / "home"
    monkeypatch.setattr(guard, "USER_HOME", fake_home)
    guard._LOCK_CACHE.clear()

    work_dir = tmp_path / "work"
    (work_dir / "dispatch").mkdir(parents=True)
    lock_path = _setup_lock(work_dir, director_id="dir-wave-uuid")

    t_dir = fake_home / ".gemini" / "antigravity" / "brain" / "dir-wave-uuid" / ".system_generated" / "logs"
    t_dir.mkdir(parents=True)
    t_file = t_dir / "transcript.jsonl"
    events = [
        {"source": "MODEL", "type": "GENERIC", "content": 'Created the following subagent:\n{\n  "conversationId": "sub-1"\n}'},
        {"source": "MODEL", "type": "GENERIC", "content": 'Created the following subagent:\n{\n  "conversationId": "sub-2"\n}'},
        {"source": "SYSTEM", "type": "SYSTEM_MESSAGE", "content": "<SYSTEM_MESSAGE>\n[Message] sender=sub-1 content=DONE: work/shards/shard_01.json\n</SYSTEM_MESSAGE>"},
    ]
    t_file.write_text("\n".join(json.dumps(e) for e in events) + "\n", encoding="utf-8")

    denied_kill = guard.process_hook(
        _make_director_kill_payload("dir-wave-uuid", "kill_all"),
        custom_lock_file=str(lock_path),
    )
    assert denied_kill["decision"] == "deny"
    assert "sub-2" in denied_kill["reason"]

    denied_stage = guard.process_hook(
        {
            "conversationId": "dir-wave-uuid",
            "toolCall": {
                "name": "run_command",
                "args": {"CommandLine": "python .agents/skills/content-to-course/run.py --stage templates --work-dir work"},
            },
        },
        custom_lock_file=str(lock_path),
    )
    assert denied_stage["decision"] == "deny"
    assert "sub-2" in denied_stage["reason"]

    # Second subagent finishes
    events.append(
        {"source": "SYSTEM", "type": "SYSTEM_MESSAGE", "content": "<SYSTEM_MESSAGE>\n[Message] sender=sub-2 content=DONE: work/shards/shard_02.json\n</SYSTEM_MESSAGE>"}
    )
    t_file.write_text("\n".join(json.dumps(e) for e in events) + "\n", encoding="utf-8")

    assert guard.process_hook(
        _make_director_kill_payload("dir-wave-uuid", "kill_all"),
        custom_lock_file=str(lock_path),
    ) == {"decision": "allow"}
    assert guard.process_hook(
        {
            "conversationId": "dir-wave-uuid",
            "toolCall": {
                "name": "run_command",
                "args": {"CommandLine": "python .agents/skills/content-to-course/run.py --stage templates --work-dir work"},
            },
        },
        custom_lock_file=str(lock_path),
    ) == {"decision": "allow"}


def test_pending_wave_reports_short_labels_instead_of_uuids(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    fake_home = tmp_path / "home"
    monkeypatch.setattr(guard, "USER_HOME", fake_home)
    guard._LOCK_CACHE.clear()

    work_dir = tmp_path / "work"
    (work_dir / "dispatch").mkdir(parents=True)
    lock_path = _setup_lock(work_dir, director_id="dir-short-lbl")

    t_dir = fake_home / ".gemini" / "antigravity" / "brain" / "dir-short-lbl" / ".system_generated" / "logs"
    t_dir.mkdir(parents=True)
    t_file = t_dir / "transcript.jsonl"
    events = [
        {
            "type": "PLANNER_RESPONSE",
            "source": "MODEL",
            "tool_calls": [
                {"name": "invoke_subagent", "arguments": {"Role": "Cognitive Task Analysis Architect part_01"}},
                {"name": "invoke_subagent", "arguments": {"Role": "Cognitive Task Analysis Architect part_05"}},
            ],
        },
        {"source": "MODEL", "type": "GENERIC", "content": 'Created the following subagent:\n{"conversationId": "8dd0e26a-b151-41f6-9c52-1475c59914fa"}'},
        {"source": "MODEL", "type": "GENERIC", "content": 'Created the following subagent:\n{"conversationId": "394a6431-e5b4-4c61-a8fb-5c4b96495c4d"}'},
        {"source": "SYSTEM", "type": "SYSTEM_MESSAGE", "content": "<SYSTEM_MESSAGE>\n[Message] sender=8dd0e26a-b151-41f6-9c52-1475c59914fa content=DONE: work/cta_parts/part_01.json\n</SYSTEM_MESSAGE>"},
    ]
    t_file.write_text("\n".join(json.dumps(e) for e in events) + "\n", encoding="utf-8")

    denied = guard.process_hook(
        _make_director_kill_payload("dir-short-lbl", "kill_all"),
        custom_lock_file=str(lock_path),
    )
    assert denied["decision"] == "deny"
    assert "part_05" in denied["reason"]
    assert "394a6431" not in denied["reason"]
