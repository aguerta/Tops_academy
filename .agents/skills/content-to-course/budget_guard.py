"""Automated Budget Watchdog for C2C Multi-Agent Orchestrations (C2C v3.22).

Monitors live subagent execution transcripts (transcript.jsonl) to detect and mitigate:
1. Turn runaway (> 40 turns)
2. Token burn runaway (> 5M tokens)
3. Tool script looping (repeated compile_shard.py, check_cta.py, or view_file loops without progress)

When runaway conditions are detected, budget_guard identifies unfinished competencies/units
and automatically generates targeted repair re-dispatch payloads (c2c_repair).
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

logger = logging.getLogger("budget_guard")

# Default SLA limits
DEFAULT_MAX_TURNS = 40
DEFAULT_MAX_TOKENS = 5_000_000
DEFAULT_MAX_SCRIPT_LOOPS = 5

MONITORED_SCRIPTS = [
    "compile_shard.py",
    "check_cta.py",
    "check_templates.py",
    "compile_cta.py",
    "cta_merge.py",
]


@dataclass
class SubagentMetrics:
    subagent_id: str
    role: str
    transcript_path: str
    turn_count: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    tool_calls_count: int = 0
    tool_histogram: Dict[str, int] = field(default_factory=dict)
    script_execution_counts: Dict[str, int] = field(default_factory=dict)
    consecutive_script_failures: int = 0
    max_consecutive_script_failures: int = 0
    is_completed: bool = False
    completion_signal: Optional[str] = None
    last_active_timestamp: Optional[str] = None
    unit_id: Optional[str] = None
    assigned_competency_ids: List[str] = field(default_factory=list)


@dataclass
class SubagentWatchdogReport:
    subagent_id: str
    role: str
    unit_id: Optional[str]
    is_runaway: bool
    runaway_reasons: List[str]
    metrics: SubagentMetrics
    recommended_action: str  # "continue", "kill_and_redispatch", "completed"


def parse_transcript(transcript_path: Union[str, Path]) -> SubagentMetrics:
    """Parses a transcript.jsonl file and extracts operational metrics."""
    path = Path(transcript_path).resolve()
    subagent_id = path.parent.name if path.parent.name not in ("transcripts", "work", "dispatch") else path.stem
    metrics = SubagentMetrics(
        subagent_id=subagent_id,
        role="unknown",
        transcript_path=path.as_posix(),
    )

    if not path.is_file():
        return metrics

    lines: List[str] = []
    try:
        content = path.read_text(encoding="utf-8")
        lines = [line.strip() for line in content.splitlines() if line.strip()]
    except Exception as e:
        logger.warning("Could not read transcript %s: %s", path, e)
        return metrics

    script_regex = re.compile(r"|".join(re.escape(s) for s in MONITORED_SCRIPTS))
    consecutive_script_failures = 0
    max_consecutive = 0

    for line in lines:
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue

        if entry.get("role") in ("assistant", "model") or entry.get("type") in ("assistant_turn", "model_turn"):
            metrics.turn_count += 1

        # Check timestamp
        ts = entry.get("timestamp") or entry.get("time") or entry.get("created_at")
        if ts:
            metrics.last_active_timestamp = str(ts)

        # Check subagent identity / role
        role = entry.get("role") or entry.get("agent_role") or entry.get("TypeName")
        if role and metrics.role == "unknown":
            metrics.role = str(role)

        unit = entry.get("unit_id") or entry.get("shard_id") or entry.get("part_id")
        if unit and not metrics.unit_id:
            metrics.unit_id = str(unit)

        # Token counting: check metadata or estimate
        usage = entry.get("usage") or entry.get("token_usage") or {}
        if isinstance(usage, dict):
            inp = usage.get("input_tokens") or usage.get("prompt_tokens") or 0
            outp = usage.get("output_tokens") or usage.get("completion_tokens") or 0
            tot = usage.get("total_tokens") or (inp + outp)
            metrics.input_tokens += int(inp)
            metrics.output_tokens += int(outp)
            metrics.total_tokens += int(tot)
        else:
            # Fallback estimation: ~4 chars per token
            text_len = len(line)
            est_tokens = max(1, text_len // 4)
            metrics.total_tokens += est_tokens

        # Check tool calls
        tool_call = entry.get("tool_name") or entry.get("tool") or entry.get("toolAction")
        if not tool_call and "function_call" in entry:
            tool_call = entry["function_call"].get("name")
        if not tool_call and "tool_calls" in entry and isinstance(entry["tool_calls"], list):
            for tc in entry["tool_calls"]:
                if isinstance(tc, dict):
                    tname = tc.get("name") or tc.get("function", {}).get("name")
                    if tname:
                        tool_call = tname
                        break

        if tool_call:
            metrics.tool_calls_count += 1
            t_str = str(tool_call)
            metrics.tool_histogram[t_str] = metrics.tool_histogram.get(t_str, 0) + 1

        # Inspect script execution inside run_command or command line arguments
        raw_cmd = ""
        if isinstance(entry.get("args"), dict):
            raw_cmd = str(entry["args"].get("CommandLine") or entry["args"].get("cmd") or "")
        elif isinstance(entry.get("tool_input"), dict):
            raw_cmd = str(entry["tool_input"].get("CommandLine") or entry["tool_input"].get("cmd") or "")
        elif "command" in entry:
            raw_cmd = str(entry.get("command"))
        elif tool_call in ("run_command", "bash", "execute_command"):
            raw_cmd = str(entry.get("CommandLine") or entry.get("content") or "")

        # Also detect view_file calls on forbidden tool scripts
        if tool_call == "view_file":
            target_path = ""
            if isinstance(entry.get("args"), dict):
                target_path = str(entry["args"].get("AbsolutePath") or "")
            for s in MONITORED_SCRIPTS:
                if s in target_path:
                    metrics.script_execution_counts[s] = metrics.script_execution_counts.get(s, 0) + 1

        if raw_cmd:
            matches = script_regex.findall(raw_cmd)
            for m in matches:
                metrics.script_execution_counts[m] = metrics.script_execution_counts.get(m, 0) + 1

            # Check exit status or error in output
            output = str(entry.get("output") or entry.get("result") or "")
            is_error = "FAIL" in output or "Error" in output or "Traceback" in output or entry.get("exit_code", 0) != 0
            if matches and is_error:
                consecutive_script_failures += 1
                max_consecutive = max(max_consecutive, consecutive_script_failures)
            elif matches and not is_error and "OK" in output:
                consecutive_script_failures = 0

        # Check completion signal
        msg_text = str(entry.get("content") or entry.get("message") or "")
        done_m = re.search(r"DONE:\s*([^\n\r]+)", msg_text)
        if done_m:
            metrics.is_completed = True
            metrics.completion_signal = done_m.group(0).strip()

        # Extract assigned competencies if present in initial prompt
        if "COMPETENCIES" in msg_text or "Competencia:" in msg_text:
            found_cids = re.findall(r"(?:Competencia:\s*`?([A-Za-z0-9_\-]+)`?|###\s*Competencia:\s*`?([A-Za-z0-9_\-]+)`?)", msg_text)
            for c1, c2 in found_cids:
                cid = c1 or c2
                if cid and cid not in metrics.assigned_competency_ids:
                    metrics.assigned_competency_ids.append(cid)

    if metrics.turn_count == 0 and lines:
        metrics.turn_count = len(lines)

    metrics.consecutive_script_failures = consecutive_script_failures
    metrics.max_consecutive_script_failures = max_consecutive
    return metrics


def evaluate_watchdog_rules(
    metrics: SubagentMetrics,
    max_turns: int = DEFAULT_MAX_TURNS,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    max_script_loops: int = DEFAULT_MAX_SCRIPT_LOOPS,
) -> SubagentWatchdogReport:
    """Evaluates watchdog rules against metrics and flags runaway subagents."""
    runaway_reasons: List[str] = []

    # 1. Turn runaway limit
    if metrics.turn_count > max_turns:
        runaway_reasons.append(
            f"Turn limit exceeded: Turn count {metrics.turn_count} exceeds SLA limit {max_turns}"
        )

    # 2. Token runaway limit
    if metrics.total_tokens > max_tokens:
        runaway_reasons.append(
            f"Token burn limit exceeded: Token burn {metrics.total_tokens:,} exceeds SLA limit {max_tokens:,}"
        )

    # 3. Tool script looping
    total_script_calls = sum(metrics.script_execution_counts.values())
    if (metrics.max_consecutive_script_failures >= max_script_loops or total_script_calls >= max_script_loops) and not metrics.is_completed:
        runaway_reasons.append(
            f"Script loop detected: Tool script loop with {metrics.max_consecutive_script_failures} consecutive failures or {total_script_calls} calls without progress"
        )

    is_runaway = len(runaway_reasons) > 0 and not metrics.is_completed

    if metrics.is_completed:
        rec_action = "completed"
    elif is_runaway:
        rec_action = "kill_and_redispatch"
    else:
        rec_action = "continue"

    return SubagentWatchdogReport(
        subagent_id=metrics.subagent_id,
        role=metrics.role,
        unit_id=metrics.unit_id,
        is_runaway=is_runaway,
        runaway_reasons=runaway_reasons,
        metrics=metrics,
        recommended_action=rec_action,
    )


def scan_work_transcripts(
    work_dir: Union[str, Path],
    max_turns: int = DEFAULT_MAX_TURNS,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    max_script_loops: int = DEFAULT_MAX_SCRIPT_LOOPS,
) -> List[SubagentWatchdogReport]:
    """Scans all transcript files in work_dir and evaluates watchdog rules."""
    work = Path(work_dir).resolve()
    reports: List[SubagentWatchdogReport] = []

    # Search paths for transcripts
    candidates: List[Path] = []
    candidates.extend(work.glob("transcripts/*.jsonl"))
    candidates.extend(work.glob("transcripts/**/transcript.jsonl"))
    candidates.extend(work.glob("dispatch/transcripts/*.jsonl"))
    candidates.extend(work.glob("*.jsonl"))

    seen: Set[str] = set()
    for cand in sorted(candidates):
        cand_str = cand.resolve().as_posix()
        if cand_str in seen:
            continue
        seen.add(cand_str)

        metrics = parse_transcript(cand)
        report = evaluate_watchdog_rules(
            metrics,
            max_turns=max_turns,
            max_tokens=max_tokens,
            max_script_loops=max_script_loops,
        )
        reports.append(report)

    return reports


def identify_unfinished_competencies(
    work_dir: Union[str, Path],
    runaway_reports: List[SubagentWatchdogReport],
) -> List[Dict[str, Any]]:
    """Identifies competencies from runaway or failed subagents that have not passed validation."""
    work = Path(work_dir).resolve()
    templates_dir = work / "templates"
    cta_file = work / "cta.json"

    all_comps: Dict[str, Dict[str, Any]] = {}
    if cta_file.is_file():
        try:
            cta_data = json.loads(cta_file.read_text(encoding="utf-8"))
            for c in cta_data.get("competencies", []):
                if isinstance(c, dict) and "id" in c:
                    all_comps[c["id"]] = c
        except Exception:
            pass

    # Check which templates exist and are valid
    certified_cids: Set[str] = set()
    if templates_dir.is_dir():
        for tf in templates_dir.glob("*.json"):
            try:
                tdata = json.loads(tf.read_text(encoding="utf-8"))
                cid = tdata.get("competency_id") or tf.stem
                if cid:
                    certified_cids.add(cid)
            except Exception:
                pass

    unfinished: List[Dict[str, Any]] = []
    for rep in runaway_reports:
        if not rep.is_runaway:
            continue

        cids = rep.metrics.assigned_competency_ids
        unit_id = rep.unit_id or rep.metrics.unit_id

        # If cids wasn't parsed from transcript, try pre_shard_manifest or shard files
        if not cids and unit_id:
            shard_manifest = work / "shards" / "pre_shard_manifest.json"
            if shard_manifest.is_file():
                try:
                    sm_data = json.loads(shard_manifest.read_text(encoding="utf-8"))
                    for s in sm_data.get("shards", []):
                        if s.get("shard_id") == unit_id:
                            cids = s.get("competency_ids", [])
                            break
                except Exception:
                    pass

        for cid in cids:
            if cid not in certified_cids:
                unfinished.append({
                    "competency_id": cid,
                    "unit_id": unit_id or "unknown",
                    "subagent_id": rep.subagent_id,
                    "reasons": rep.runaway_reasons,
                    "info": all_comps.get(cid, {}),
                })

    return unfinished


def generate_repair_redispatch(
    work_dir: Union[str, Path],
    runaway_reports: List[SubagentWatchdogReport],
) -> Dict[str, Any]:
    """Generates targeted repair re-dispatch payload for unfinished competencies."""
    work = Path(work_dir).resolve()
    unfinished = identify_unfinished_competencies(work, runaway_reports)

    if not unfinished:
        logger.info("Watchdog: No unfinished competencies found for re-dispatch.")
        return {"Subagents": [], "unfinished_count": 0, "item_files": []}

    dispatch_items_dir = work / "dispatch" / "items"
    dispatch_items_dir.mkdir(parents=True, exist_ok=True)

    subagents: List[Dict[str, Any]] = []
    item_files: List[str] = []

    for idx, item in enumerate(unfinished, start=1):
        cid = item["competency_id"]
        unit_id = item["unit_id"]
        reasons = item["reasons"]
        reasons_str = "; ".join(reasons)

        out_py = f"work/shards/{unit_id}_data.py"
        out_json = f"work/shards/{unit_id}.json"

        work_order_data = {
            "TypeName": "c2c_repair",
            "Role": f"Watchdog Repair Engineer {cid}",
            "Model": "flash",
            "Workspace": "inherit",
            "unit_id": unit_id,
            "competency_id": cid,
            "diagnostics": {
                "watchdog_aborted": True,
                "reasons": reasons,
                "failing_unit": unit_id,
            },
            "output_python": out_py,
            "output_json": out_json,
            "compile_command": f"python .agents/skills/content-to-course/compile_shard.py --input {out_py} --output {out_json} --cta work/cta.json --manifest work/pre_cta_manifest.json",
            "instructions": f"Fix the failing template for {cid} in {out_py} surgically, re-compile and finish with DONE: {out_json}",
        }

        item_file = dispatch_items_dir / f"watchdog_repair_{idx:02d}.json"
        item_file.write_text(json.dumps(work_order_data, indent=2, ensure_ascii=False), encoding="utf-8")
        item_files.append(item_file.resolve().as_posix())

        item_rel = f"work/dispatch/items/{item_file.name}"
        pointer_prompt = (
            f"You are Watchdog Repair Engineer {cid}. "
            f"Your work order is `{item_rel}`. Read it first with `view_file`, "
            f"repair `{cid}` in `{out_py}`, compile and certify. "
            f"Finalize strictly with: `DONE: {out_json}`."
        )

        subagent_spec = {
            "TypeName": "c2c_repair",
            "Role": f"Watchdog Repair Engineer {cid}",
            "Model": "flash",
            "Prompt": pointer_prompt,
        }
        subagents.append(subagent_spec)

    result_payload = {
        "Subagents": subagents,
        "unfinished_count": len(unfinished),
        "item_files": item_files,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }

    # Persist watchdog redispatch audit file
    audit_file = work / "dispatch" / "watchdog_redispatch.json"
    audit_file.parent.mkdir(parents=True, exist_ok=True)
    audit_file.write_text(json.dumps(result_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    return result_payload


def update_state_checkpoint(
    work_dir: Union[str, Path],
    stage: str,
    status: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Updates state.json checkpoint to support seamless resumption across 429/404 halts."""
    work = Path(work_dir).resolve()
    state_file = work / "state.json"
    work.mkdir(parents=True, exist_ok=True)

    state: Dict[str, Any] = {
        "course_id": work.parent.name if work.name == "work" else work.name,
        "current_stage": stage,
        "stages": {},
        "subagents": {},
        "last_checkpoint": datetime.now(timezone.utc).isoformat(),
    }

    if state_file.is_file():
        try:
            state = json.loads(state_file.read_text(encoding="utf-8"))
        except Exception as e:
            logger.warning("Could not read existing state.json: %s", e)

    state["current_stage"] = stage
    state["last_checkpoint"] = datetime.now(timezone.utc).isoformat()
    stage_entry = state.setdefault("stages", {}).setdefault(stage, {})
    stage_entry["status"] = status
    stage_entry["updated_at"] = datetime.now(timezone.utc).isoformat()

    if metadata:
        stage_entry.update(metadata)

    state_file.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    return state


def load_state_checkpoint(work_dir: Union[str, Path]) -> Dict[str, Any]:
    """Loads state.json from work_dir, returning an empty skeleton if not found."""
    work = Path(work_dir).resolve()
    state_file = work / "state.json"
    if state_file.is_file():
        try:
            return json.loads(state_file.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"current_stage": "initial", "stages": {}, "subagents": {}}


def main() -> None:
    parser = argparse.ArgumentParser(description="Automated Budget Watchdog for C2C Pipelines")
    parser.add_argument("--work-dir", default="work", help="Working directory containing transcripts")
    parser.add_argument("--transcript", default=None, help="Inspect a specific transcript file")
    parser.add_argument("--max-turns", type=int, default=DEFAULT_MAX_TURNS, help="Max turns allowed")
    parser.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS, help="Max tokens allowed")
    parser.add_argument("--max-script-loops", type=int, default=DEFAULT_MAX_SCRIPT_LOOPS, help="Max script loops")
    parser.add_argument("--redispatch", action="store_true", help="Generate repair re-dispatch for runaways")
    parser.add_argument("--checkpoint", help="Record checkpoint stage into state.json")
    parser.add_argument("--status", default="completed", help="Status for checkpoint")

    args = parser.parse_args()

    if args.checkpoint:
        st = update_state_checkpoint(args.work_dir, args.checkpoint, args.status)
        print(f"[+] Checkpoint saved for stage '{args.checkpoint}' with status '{args.status}'.")
        print(json.dumps(st, indent=2, ensure_ascii=False))
        return

    if args.transcript:
        metrics = parse_transcript(args.transcript)
        report = evaluate_watchdog_rules(
            metrics,
            max_turns=args.max_turns,
            max_tokens=args.max_tokens,
            max_script_loops=args.max_script_loops,
        )
        print(json.dumps({
            "subagent_id": report.subagent_id,
            "role": report.role,
            "is_runaway": report.is_runaway,
            "runaway_reasons": report.runaway_reasons,
            "recommended_action": report.recommended_action,
            "metrics": asdict(report.metrics),
        }, indent=2, ensure_ascii=False))
        sys.exit(2 if report.is_runaway else 0)

    # Scan work-dir transcripts
    reports = scan_work_transcripts(
        args.work_dir,
        max_turns=args.max_turns,
        max_tokens=args.max_tokens,
        max_script_loops=args.max_script_loops,
    )

    runaways = [r for r in reports if r.is_runaway]
    print(f"[+] Watchdog Scanned {len(reports)} subagents in '{args.work_dir}': {len(runaways)} runaway(s) detected.")

    for r in reports:
        status_flag = "RUNAWAY" if r.is_runaway else ("COMPLETED" if r.metrics.is_completed else "OK")
        print(f"  * [{status_flag}] Subagent: {r.subagent_id} | Turns: {r.metrics.turn_count} | Tokens: {r.metrics.total_tokens:,} | Action: {r.recommended_action}")
        if r.runaway_reasons:
            for reason in r.runaway_reasons:
                print(f"    - Alert: {reason}")

    if args.redispatch and runaways:
        print("[+] Generating repair re-dispatch payload for runaway subagents...")
        redispatch_payload = generate_repair_redispatch(args.work_dir, runaways)
        print(json.dumps(redispatch_payload, indent=2, ensure_ascii=False))

    sys.exit(2 if runaways else 0)


if __name__ == "__main__":
    main()
