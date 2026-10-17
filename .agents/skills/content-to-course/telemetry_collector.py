"""Deterministic Telemetry Collector for Content-to-Course (C2C) v3.2.

Fast, deterministic execution (< 30 ms) collecting:
- Stage snapshots in `work/telemetry/<stage_idx>_<stage_name>.json`
- Master pipeline state in `work/state.json`
- Subagent tree inspection with token breakdown (input, output, cached, thinking, total)
- Chronological thinking traces (`thinking_traces`) for diagnostic and forensic post-mortems
- Artifact counts across all stages
"""

from __future__ import annotations

import argparse
import datetime
import json
import logging
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger("telemetry_collector")


def get_brain_dir() -> Path:
    """Resolve the Antigravity brain directory."""
    env_brain = os.environ.get("ANTIGRAVITY_BRAIN_DIR")
    if env_brain and Path(env_brain).is_dir():
        return Path(env_brain)
    return Path(os.path.expanduser("~")) / ".gemini" / "antigravity" / "brain"


def find_conversation_id_for_work_dir(work_dir: Path) -> Optional[str]:
    """Auto-detect conversation ID whose transcript references this work directory."""
    # 1. Environment variable if set
    env_conv = os.environ.get("ANTIGRAVITY_CONVERSATION_ID")
    if env_conv:
        return env_conv.strip()

    brain_dir = get_brain_dir()
    if not brain_dir.exists():
        return None

    norm_work = str(work_dir.resolve()).replace("\\", "/").lower()
    work_name = work_dir.name.lower()
    course_name = work_dir.parent.name.lower() if work_dir.name == "work" else work_name

    # Check recently modified transcripts first (limit to 15 newest)
    transcripts = []
    try:
        for d in brain_dir.iterdir():
            if not d.is_dir():
                continue
            t_file = d / ".system_generated" / "logs" / "transcript.jsonl"
            if t_file.is_file():
                transcripts.append((t_file.stat().st_mtime, d.name, t_file))
    except Exception:
        return None

    transcripts.sort(key=lambda x: x[0], reverse=True)

    for _, conv_id, t_file in transcripts[:15]:
        try:
            with open(t_file, "r", encoding="utf-8", errors="ignore") as f:
                head = "".join(f.readline() for _ in range(60)).replace("\\", "/").lower()
                if norm_work in head or (work_dir.name.lower() == "work" and f"/courses/{course_name}/work" in head):
                    return conv_id
        except Exception:
            continue

    return None


def read_transcript_with_full_resolution(transcript_path: Path) -> List[Dict[str, Any]]:
    """Reads transcript.jsonl, and streaming-resolves only truncated steps from transcript_full.jsonl line-by-line."""
    records: List[Dict[str, Any]] = []
    if not transcript_path.is_file():
        return records

    truncated_steps: Dict[int, int] = {}  # step_index -> records index
    truncated_lines: Dict[int, int] = {}  # line_idx -> records index

    try:
        with open(transcript_path, "r", encoding="utf-8", errors="ignore") as f:
            for line_idx, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                    rec_idx = len(records)
                    records.append(rec)
                    if rec.get("truncated_fields"):
                        s_idx = rec.get("step_index")
                        if s_idx is not None:
                            truncated_steps[s_idx] = rec_idx
                        truncated_lines[line_idx] = rec_idx
                except Exception:
                    pass
    except Exception:
        return records

    if not truncated_steps and not truncated_lines:
        return records

    full_path = transcript_path.parent / "transcript_full.jsonl"
    if not full_path.is_file():
        return records

    needed_steps = set(truncated_steps.keys())
    needed_lines = set(truncated_lines.keys())
    _step_re = re.compile(r'\{"step_index":\s*(\d+)')

    try:
        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
            for line_idx, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue

                m = _step_re.match(line[:50])
                matched_step = int(m.group(1)) if m else None

                is_needed = False
                rec_idx = None

                if matched_step is not None and matched_step in needed_steps:
                    is_needed = True
                    rec_idx = truncated_steps[matched_step]
                elif line_idx in needed_lines:
                    is_needed = True
                    rec_idx = truncated_lines[line_idx]

                if is_needed and rec_idx is not None:
                    try:
                        full_rec = json.loads(line)
                        records[rec_idx] = full_rec
                    except Exception:
                        pass
                    if matched_step is not None and matched_step in needed_steps:
                        needed_steps.remove(matched_step)
                    if line_idx in needed_lines:
                        needed_lines.remove(line_idx)
                    if not needed_steps and not needed_lines:
                        break
    except Exception:
        pass

    return records


def resolve_full_step(step: Dict[str, Any], full_path: Path) -> Dict[str, Any]:
    """Reads un-truncated step from transcript_full.jsonl when truncated_fields is present."""
    if not step.get("truncated_fields") or not full_path.is_file():
        return step
    target_idx = step.get("step_index")
    _step_re = re.compile(r'\{"step_index":\s*(\d+)')
    try:
        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                m = _step_re.match(line[:50])
                if m and int(m.group(1)) != target_idx:
                    continue
                d = json.loads(line)
                if d.get("step_index") == target_idx:
                    return d
    except Exception:
        pass
    return step


def inspect_subagent_transcript(
    subagent_conv_id: str,
    meta: Dict[str, Any],
    brain_dir: Optional[Path] = None,
) -> Dict[str, Any]:
    """Deep inspects a single subagent transcript extracting metrics and thinking traces."""
    if brain_dir is None:
        brain_dir = get_brain_dir()

    t_path = brain_dir / subagent_conv_id / ".system_generated" / "logs" / "transcript.jsonl"

    role = meta.get("role", "subagent")
    type_name = meta.get("type_name", meta.get("type", "generic"))
    model = meta.get("model", "inherit")

    tokens = {
        "input": 0,
        "output": 0,
        "cached": 0,
        "thinking": 0,
        "total": 0,
    }
    turns_count = 0
    tool_calls_summary: Dict[str, int] = {}
    cli_errors: List[Dict[str, Any]] = []
    thinking_traces: List[Dict[str, Any]] = []

    if not t_path.is_file():
        return {
            "conversation_id": subagent_conv_id,
            "role": role,
            "type_name": type_name,
            "model": model,
            "tokens": tokens,
            "turns_count": turns_count,
            "duration_seconds": 0.0,
            "tool_calls_summary": tool_calls_summary,
            "cli_errors": cli_errors,
            "thinking_traces": thinking_traces,
        }

    records = read_transcript_with_full_resolution(t_path)
    timestamps: List[datetime.datetime] = []

    for i, rec in enumerate(records):
        ts_str = rec.get("created_at")
        if ts_str:
            try:
                ts = datetime.datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                timestamps.append(ts)
            except Exception:
                pass

        rec_type = rec.get("type")
        status = rec.get("status")

        if rec_type == "PLANNER_RESPONSE":
            turns_count += 1
            inp = rec.get("input_tokens", 0) or 0
            out = rec.get("output_tokens", 0) or 0
            cached = rec.get("cache_read_tokens", 0) or 0
            thinking_text = rec.get("thinking", "") or ""
            # Estimate thinking tokens if not explicitly in JSON (~4 chars/token)
            th_tokens = rec.get("thinking_tokens") or (len(thinking_text) // 4 if thinking_text else 0)

            tokens["input"] += inp
            tokens["output"] += out
            tokens["cached"] += cached
            tokens["thinking"] += th_tokens

            # Tool calls in step
            step_tools = []
            for tc in rec.get("tool_calls", []):
                tname = tc.get("name", "unknown")
                tool_calls_summary[tname] = tool_calls_summary.get(tname, 0) + 1
                step_tools.append(tname)

            # Check if next step was an error
            had_error = False
            if i + 1 < len(records):
                next_rec = records[i + 1]
                if next_rec.get("status") == "ERROR" or next_rec.get("type") == "ERROR_MESSAGE":
                    had_error = True
                elif "exited with code 1" in next_rec.get("content", ""):
                    had_error = True

            thinking_traces.append({
                "step_index": rec.get("step_index", i),
                "created_at": ts_str,
                "thinking": thinking_text,
                "tool_calls": step_tools,
                "had_error": had_error,
            })

        elif rec_type in ("GENERIC", "TOOL_RESPONSE") and (status == "ERROR" or "exited with code" in rec.get("content", "")):
            content = rec.get("content", "")
            is_err = status == "ERROR"
            if "exited with code" in content:
                code_m = re.search(r"exited with code\s+(\d+)", content)
                if code_m and int(code_m.group(1)) != 0:
                    is_err = True

            if is_err:
                cli_errors.append({
                    "step_index": rec.get("step_index", i),
                    "created_at": ts_str,
                    "snippet": content[:240].strip(),
                })

    tokens["total"] = tokens["input"] + tokens["output"] + tokens["cached"]

    duration_sec = 0.0
    if len(timestamps) >= 2:
        duration_sec = max(0.0, (timestamps[-1] - timestamps[0]).total_seconds())

    return {
        "conversation_id": subagent_conv_id,
        "role": role,
        "type_name": type_name,
        "model": model,
        "tokens": tokens,
        "turns_count": turns_count,
        "duration_seconds": round(duration_sec, 2),
        "tool_calls_summary": tool_calls_summary,
        "cli_errors": cli_errors[:10],
        "thinking_traces": thinking_traces,
    }


def extract_stage_subagents(
    root_conv_id: str,
    stage_name: str,
    brain_dir: Optional[Path] = None,
) -> List[Dict[str, Any]]:
    """Discovers and extracts subagents associated with this stage from root conversation."""
    if brain_dir is None:
        brain_dir = get_brain_dir()

    root_t = brain_dir / root_conv_id / ".system_generated" / "logs" / "transcript.jsonl"
    if not root_t.is_file():
        return []

    discovered: List[Dict[str, Any]] = []
    seen_cids = set()

    # Stage role filters
    stage_lower = stage_name.lower()
    stage_keywords = {
        "prepare": ["vision", "c2c-vision", "handout"],
        "cta": ["cta", "cta-direct", "cta-map", "cta-reduce", "c2c-cta", "architect", "part_"],
        "shard": ["shard"],
        "templates": ["author", "c2c-author", "shard_", "exercise"],
        "build": ["build"],
        "verify": ["judge", "c2c-judge", "repair", "c2c-repair"],
        "judge_compare": ["judge", "c2c-judge"],
        "publish": ["publish"],
    }
    keywords = stage_keywords.get(stage_lower, [stage_lower])

    try:
        with open(root_t, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    rec = json.loads(line)
                except Exception:
                    continue

                content = rec.get("content", "")
                if "conversationId" not in content and "manage_subagents" not in content and "Created the following subagents" not in content:
                    continue

                # Match array of subagents
                m_arr = re.search(r'\[\s*\{.*?"conversationId".*?\}\s*\]', content, re.DOTALL)
                if m_arr:
                    try:
                        arr = json.loads(m_arr.group(0))
                        for item in arr:
                            cid = item.get("conversationId")
                            if cid and cid not in seen_cids:
                                seen_cids.add(cid)
                                role = item.get("role", "")
                                tname = item.get("type", "")
                                model = item.get("model", "inherit")
                                if any(k in role.lower() or k in tname.lower() for k in keywords):
                                    discovered.append({
                                        "conversation_id": cid,
                                        "role": role,
                                        "type_name": tname,
                                        "model": model,
                                    })
                    except Exception:
                        pass

                # Individual conversationId matches
                cids = re.findall(r'"conversationId":\s*"([a-f0-9\-]{36})"', content)
                for cid in cids:
                    if cid not in seen_cids:
                        seen_cids.add(cid)
                        # Probe step 0 of subagent transcript to see if it matches stage
                        sub_meta = {"role": "Subagent", "type_name": "generic", "model": "inherit"}
                        sub_t0 = brain_dir / cid / ".system_generated" / "logs" / "transcript.jsonl"
                        if sub_t0.is_file():
                            try:
                                with open(sub_t0, "r", encoding="utf-8", errors="ignore") as sf:
                                    first_l = sf.readline()
                                    if first_l:
                                        d0 = json.loads(first_l)
                                        p0 = d0.get("content", "")
                                        if any(k in p0.lower() for k in keywords):
                                            discovered.append({
                                                "conversation_id": cid,
                                                "role": f"Subagent-{cid[:8]}",
                                                "type_name": "subagent",
                                                "model": "inherit",
                                            })
                            except Exception:
                                pass
    except Exception as e:
        logger.debug("Error scanning root transcript: %s", e)

    subagent_details = []
    for meta in discovered:
        detail = inspect_subagent_transcript(meta["conversation_id"], meta, brain_dir=brain_dir)
        subagent_details.append(detail)

    return subagent_details


def collect_artifact_counts(work_dir: Path) -> Dict[str, int]:
    """Computes exact counts of artifact entities across pipeline artifacts in work_dir."""
    counts = {
        "pages": 0,
        "competencies": 0,
        "shards": 0,
        "templates_compiled": 0,
        "questions_built": 0,
    }

    # 1. Pages
    pre_cta = work_dir / "pre_cta_manifest.json"
    if pre_cta.is_file():
        try:
            d = json.loads(pre_cta.read_text(encoding="utf-8"))
            counts["pages"] = d.get("total_pages") or d.get("total_items") or len(d.get("files", []))
        except Exception:
            pass

    # 2. Competencies
    cta_json = work_dir / "cta.json"
    if cta_json.is_file():
        try:
            d = json.loads(cta_json.read_text(encoding="utf-8"))
            counts["competencies"] = len(d.get("competencies", []))
        except Exception:
            pass
    elif (work_dir / "cta_data.py").is_file():
        try:
            text = (work_dir / "cta_data.py").read_text(encoding="utf-8")
            counts["competencies"] = len(re.findall(r"\(\s*['\"](?:H|C|Hab)-\d+['\"]", text))
        except Exception:
            pass

    # 3. Shards
    pre_shard = work_dir / "shards" / "pre_shard_manifest.json"
    if pre_shard.is_file():
        try:
            d = json.loads(pre_shard.read_text(encoding="utf-8"))
            counts["shards"] = d.get("total_shards", len(d.get("shards", [])))
        except Exception:
            pass
    if counts["shards"] == 0 and (work_dir / "shards").is_dir():
        counts["shards"] = len(list((work_dir / "shards").glob("shard_*.json")))

    # 4. Templates compiled
    templates_dir = work_dir / "templates"
    if templates_dir.is_dir():
        counts["templates_compiled"] = len(list(templates_dir.glob("*.json")))

    # 5. Questions built
    for cand in [work_dir / "course_verified.json", work_dir / "course.json"]:
        if cand.is_file():
            try:
                d = json.loads(cand.read_text(encoding="utf-8"))
                counts["questions_built"] = len(d.get("questions", []))
                break
            except Exception:
                pass

    return counts


def update_master_state(
    work_dir: Path,
    stage_snapshot: Dict[str, Any],
) -> Dict[str, Any]:
    """Updates work/state.json accumulating stage history, counts, tokens, and timestamps."""
    state_file = work_dir / "state.json"
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

    state: Dict[str, Any] = {
        "course_id": work_dir.parent.name if work_dir.name == "work" else work_dir.name,
        "started_at": now_iso,
        "updated_at": now_iso,
        "last_stage": f"{stage_snapshot['stage_idx']}_{stage_snapshot['stage_name']}",
        "status": stage_snapshot.get("status", "in_progress"),
        "stages": {},
        "artifact_counts": {},
        "tokens_total": {
            "input": 0,
            "output": 0,
            "cached": 0,
            "thinking": 0,
            "total": 0,
        },
        "subagents_summary": [],
    }

    if state_file.is_file():
        try:
            existing = json.loads(state_file.read_text(encoding="utf-8"))
            if isinstance(existing, dict):
                state["started_at"] = existing.get("started_at", state["started_at"])
                state["course_id"] = existing.get("course_id", state["course_id"])
                state["stages"] = existing.get("stages", {})
        except Exception:
            pass

    # Check for authoritative course_id in metadata or workspace manifests
    cand_cid = stage_snapshot.get("metadata", {}).get("course_id")
    if not cand_cid:
        for cand in [work_dir / "pre_cta_manifest.json", work_dir / "cta.json", work_dir / "shards" / "pre_shard_manifest.json"]:
            if cand.is_file():
                try:
                    d = json.loads(cand.read_text(encoding="utf-8"))
                    if d.get("course_id"):
                        cand_cid = d.get("course_id")
                        break
                except Exception:
                    pass
    if cand_cid:
        state["course_id"] = cand_cid

    state["updated_at"] = now_iso
    stage_key = f"{stage_snapshot['stage_idx']}_{stage_snapshot['stage_name']}"
    state["last_stage"] = stage_key
    state["stages"][stage_key] = {
        "stage_idx": stage_snapshot["stage_idx"],
        "stage_name": stage_snapshot["stage_name"],
        "status": stage_snapshot["status"],
        "recorded_at": stage_snapshot["recorded_at"],
        "duration_seconds": stage_snapshot.get("duration_seconds", 0.0),
        "subagents_count": len(stage_snapshot.get("subagents", [])),
        "tokens": stage_snapshot.get("stage_tokens", {}),
    }

    # Re-calculate totals across all stage files in work/telemetry
    telemetry_dir = work_dir / "telemetry"
    tot_tokens = {"input": 0, "output": 0, "cached": 0, "thinking": 0, "total": 0}
    all_subagents = []
    seen_cids = set()

    if telemetry_dir.is_dir():
        for snap_f in sorted(telemetry_dir.glob("*.json")):
            try:
                s_data = json.loads(snap_f.read_text(encoding="utf-8"))
                s_toks = s_data.get("stage_tokens", {})
                for k in tot_tokens:
                    tot_tokens[k] += s_toks.get(k, 0)
                for sa in s_data.get("subagents", []):
                    cid = sa.get("conversation_id")
                    if cid and cid not in seen_cids:
                        seen_cids.add(cid)
                        all_subagents.append({
                            "conversation_id": cid,
                            "role": sa.get("role"),
                            "type_name": sa.get("type_name"),
                            "tokens": sa.get("tokens"),
                            "turns_count": sa.get("turns_count"),
                            "duration_seconds": sa.get("duration_seconds"),
                        })
            except Exception:
                pass

    state["tokens_total"] = tot_tokens
    state["subagents_summary"] = all_subagents
    state["artifact_counts"] = collect_artifact_counts(work_dir)

    # Collect thinking traces metrics across subagents
    total_thinking_turns = 0
    total_thinking_chars = 0
    subagents_with_thinking = 0

    if telemetry_dir.is_dir():
        for snap_f in sorted(telemetry_dir.glob("*.json")):
            try:
                s_data = json.loads(snap_f.read_text(encoding="utf-8"))
                for sa in s_data.get("subagents", []):
                    traces = sa.get("thinking_traces", [])
                    if traces:
                        subagents_with_thinking += 1
                        for tr in traces:
                            th_txt = tr.get("thinking", "")
                            if th_txt:
                                total_thinking_turns += 1
                                total_thinking_chars += len(th_txt)
            except Exception:
                pass

    state["thinking_traces_summary"] = {
        "total_thinking_turns": total_thinking_turns,
        "total_thinking_chars": total_thinking_chars,
        "total_thinking_tokens": tot_tokens.get("thinking", 0),
        "subagents_with_thinking": subagents_with_thinking,
    }

    # Persist state.json atomically
    temp_state = state_file.with_suffix(".tmp")
    temp_state.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    temp_state.replace(state_file)

    return state


def record_stage_telemetry(
    work_dir: Union[str, Path],
    stage_idx: str,
    stage_name: str,
    status: str = "completed",
    metadata: Optional[Dict[str, Any]] = None,
    conv_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Records stage telemetry and updates master pipeline state in < 30 ms.
    
    Args:
        work_dir: Working directory of course.
        stage_idx: 2-character stage index ('00', '01', '02', '03', '04', '05', '05b', '06').
        stage_name: Stage identifier ('prepare', 'cta', 'shard', 'templates', 'build', 'verify', 'judge_compare', 'publish').
        status: Execution status ('completed', 'failed', 'in_progress').
        metadata: Optional dictionary with additional stage context, timings, or subagent IDs.
        conv_id: Antigravity conversation UUID. If None, auto-detected from brain directory.

    Returns:
        The generated stage snapshot dictionary.
    """
    t_start = time.perf_counter()
    w_dir = Path(work_dir).resolve()
    telemetry_dir = w_dir / "telemetry"
    telemetry_dir.mkdir(parents=True, exist_ok=True)

    meta = metadata.copy() if metadata else {}
    recorded_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # Resolve conversation ID
    resolved_conv = conv_id or find_conversation_id_for_work_dir(w_dir)

    subagents: List[Dict[str, Any]] = []
    # If subagents explicitly provided in metadata, use them
    if "subagents" in meta and isinstance(meta["subagents"], list):
        subagents = meta.pop("subagents")
    elif resolved_conv:
        try:
            subagents = extract_stage_subagents(resolved_conv, stage_name)
        except Exception as e:
            logger.debug("Could not extract stage subagents: %s", e)

    # Compute stage tokens sum
    stage_tokens = {"input": 0, "output": 0, "cached": 0, "thinking": 0, "total": 0}
    for sa in subagents:
        sa_t = sa.get("tokens", {})
        for k in stage_tokens:
            stage_tokens[k] += sa_t.get(k, 0)

    # Read timings.json if available
    stage_duration = 0.0
    timings_f = w_dir / "timings.json"
    if timings_f.is_file():
        try:
            t_data = json.loads(timings_f.read_text(encoding="utf-8"))
            stage_duration = t_data.get("stages", {}).get(stage_name, 0.0)
        except Exception:
            pass

    snapshot = {
        "stage_idx": stage_idx,
        "stage_name": stage_name,
        "status": status,
        "recorded_at": recorded_at,
        "duration_seconds": meta.get("duration_seconds", stage_duration),
        "conversation_id": resolved_conv,
        "stage_tokens": stage_tokens,
        "subagents": subagents,
        "metadata": meta,
        "collector_overhead_ms": round((time.perf_counter() - t_start) * 1000, 2),
    }

    # Save stage file: work/telemetry/<stage_idx>_<stage_name>.json
    stage_filename = f"{stage_idx}_{stage_name}.json"
    stage_file = telemetry_dir / stage_filename
    temp_stage = stage_file.with_suffix(".tmp")
    temp_stage.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding="utf-8")
    temp_stage.replace(stage_file)

    # Update master state.json
    try:
        update_master_state(w_dir, snapshot)
    except Exception as e:
        logger.warning("Could not update work/state.json: %s", e)

    return snapshot


def main() -> None:
    parser = argparse.ArgumentParser(description="Deterministic C2C Stage Telemetry Collector")
    parser.add_argument("--work", "--work-dir", required=True, help="Path to work directory")
    parser.add_argument("--stage-idx", required=True, help="Stage index (e.g. 00, 01, 02, 03, 04, 05, 05b, 06)")
    parser.add_argument("--stage-name", required=True, help="Stage name (e.g. prepare, cta, shard, templates, build, verify, publish)")
    parser.add_argument("--status", default="completed", help="Stage status (default: completed)")
    parser.add_argument("--conv-id", default=None, help="Antigravity conversation UUID (optional, auto-detected if omitted)")
    args = parser.parse_args()

    res = record_stage_telemetry(
        work_dir=args.work,
        stage_idx=args.stage_idx,
        stage_name=args.stage_name,
        status=args.status,
        conv_id=args.conv_id,
    )
    print(f"[+] Recorded stage telemetry: {res['stage_idx']}_{res['stage_name']} ({res['status']})")
    print(f"    Subagents found: {len(res['subagents'])}")
    print(f"    Total tokens in stage: {res['stage_tokens']['total']}")
    print(f"    Overhead: {res['collector_overhead_ms']} ms")


if __name__ == "__main__":
    main()
