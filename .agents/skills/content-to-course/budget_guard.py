"""Automated Budget Watchdog for C2C Multi-Agent Orchestrations (C2C v3.3).

Monitors live subagent execution transcripts (transcript.jsonl) to detect and mitigate:
1. Turn runaway (> 40 turns)
2. Token burn runaway (> 5M tokens)
3. Tool script looping (repeated compile_shard.py, check_cta.py, or view_file loops without progress)

When runaway conditions are detected, budget_guard identifies unfinished competencies/units
and automatically generates targeted repair re-dispatch payloads (c2c_repair).
"""

from __future__ import annotations

import argparse
import glob
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

REPO_ROOT = Path(__file__).resolve().parents[3]

MONITORED_SCRIPTS = [
    "compile_shard.py",
    "check_cta.py",
    "check_templates.py",
    "compile_cta.py",
    "cta_merge.py",
]

MONITORED_INSPECTION_TARGETS = [
    "compile_shard.py",
    "check_templates.py",
    "compile_cta.py",
    "check_cta.py",
    "engine/",
    "/engine/",
    "\\engine\\",
    "validator/",
    "/validator/",
    "\\validator\\",
    "src/validator/",
    ".check_attempts",
    "judge_ground_truth.json",
    "SKILL.md",
]


@dataclass
class SubagentMetrics:
    subagent_id: str
    role: str
    transcript_path: str
    turn_count: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cached_tokens: int = 0
    total_tokens: int = 0
    thinking_chars: int = 0
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


def resolve_brain_transcript(
    subagent_id: str,
    app_data_dir: Optional[Union[str, Path]] = None,
) -> Optional[Path]:
    """Resolves transcript.jsonl path for a given subagent ID in Antigravity brain storage."""
    sid = str(subagent_id).strip()
    if not sid:
        return None

    p_direct = Path(sid)
    if p_direct.is_file():
        return p_direct.resolve()

    bases: List[Path] = []
    if app_data_dir:
        bases.append(Path(app_data_dir).resolve())

    env_dir = os.environ.get("ANTIGRAVITY_APP_DATA_DIR")
    if env_dir:
        bases.append(Path(env_dir).resolve())

    home = Path.home()
    bases.extend([
        home / ".gemini" / "antigravity",
        home / ".gemini" / "antigravity-ide",
        home / ".gemini" / "antigravity-cli",
    ])
    user_prof = os.environ.get("USERPROFILE")
    if user_prof:
        bases.append(Path(user_prof) / ".gemini" / "antigravity")

    for base in bases:
        candidates = [
            base / "brain" / sid / ".system_generated" / "logs" / "transcript.jsonl",
            base / "brain" / sid / ".system_generated" / "logs" / "transcript_full.jsonl",
            base / sid / ".system_generated" / "logs" / "transcript.jsonl",
            base / sid / ".system_generated" / "logs" / "transcript_full.jsonl",
            base / "brain" / sid / "transcript.jsonl",
            base / "brain" / sid / "transcript_full.jsonl",
            base / sid / "transcript.jsonl",
            base / sid / "transcript_full.jsonl",
        ]
        for cand in candidates:
            if cand.is_file():
                return cand.resolve()

    return None


def _clean_str(val: Any) -> str:
    if val is None:
        return ""
    s = str(val).strip()
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        s = s[1:-1].strip()
    return s


def parse_transcript(transcript_path: Union[str, Path]) -> SubagentMetrics:
    """Parses a transcript.jsonl file (supporting Antigravity brain schema) and extracts operational metrics."""
    path = Path(transcript_path).resolve()

    # Identify subagent ID from directory hierarchy
    if path.parent.name == "logs" and len(path.parents) >= 3 and path.parents[1].name == ".system_generated":
        subagent_id = path.parents[2].name
    elif path.parent.name not in ("transcripts", "work", "dispatch"):
        subagent_id = path.parent.name
    else:
        subagent_id = path.stem

    metrics = SubagentMetrics(
        subagent_id=subagent_id,
        role="unknown",
        transcript_path=path.as_posix(),
    )

    if not path.is_file():
        return metrics

    lines: List[str] = []
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
        lines = [line.strip() for line in content.splitlines() if line.strip()]
    except Exception as e:
        logger.warning("Could not read transcript %s: %s", path, e)
        return metrics

    script_regex = re.compile(r"|".join(re.escape(s) for s in MONITORED_SCRIPTS))
    consecutive_script_failures = 0
    max_consecutive = 0
    has_explicit_tokens = False
    parsed_entries_count = 0

    for line in lines:
        try:
            entry = json.loads(line)
        except (json.JSONDecodeError, ValueError):
            continue

        if not isinstance(entry, dict):
            continue

        parsed_entries_count += 1

        msg_text = str(entry.get("content") or entry.get("message") or "")

        # 1. Turn counting: Antigravity PLANNER_RESPONSE / MODEL source or assistant / model role
        is_model_step = (
            entry.get("type") in ("PLANNER_RESPONSE", "assistant_turn", "model_turn")
            or (not entry.get("type") and entry.get("role") in ("assistant", "model"))
            or (entry.get("role") in ("assistant", "model") and entry.get("type") not in ("GENERIC", "SYSTEM_MESSAGE"))
        )
        if is_model_step:
            metrics.turn_count += 1

        # Check timestamp
        ts = entry.get("created_at") or entry.get("timestamp") or entry.get("time")
        if ts:
            metrics.last_active_timestamp = str(ts)

        # Check thinking character count
        thinking = entry.get("thinking")
        if thinking:
            metrics.thinking_chars += len(str(thinking))

        # Check subagent identity / role
        role = entry.get("role") or entry.get("agent_role") or entry.get("TypeName")
        if role and metrics.role == "unknown" and role not in ("model", "assistant", "system", "user"):
            metrics.role = str(role)

        unit = entry.get("unit_id") or entry.get("shard_id") or entry.get("part_id")
        if unit and not metrics.unit_id:
            metrics.unit_id = str(unit)

        # 2. Token counting: explicit tokens vs fallback estimation
        inp = entry.get("input_tokens") or 0
        outp = entry.get("output_tokens") or 0
        cache = entry.get("cache_read_tokens") or entry.get("cached_tokens") or 0
        tot = 0

        usage = entry.get("usage") or entry.get("token_usage") or {}
        if isinstance(usage, dict):
            inp = inp or usage.get("input_tokens") or usage.get("prompt_tokens") or 0
            outp = outp or usage.get("output_tokens") or usage.get("completion_tokens") or 0
            cache = cache or usage.get("cache_read_tokens") or usage.get("cached_tokens") or 0
            tot = usage.get("total_tokens") or 0

        if inp > 0 or outp > 0 or cache > 0 or tot > 0:
            inp_int = int(inp)
            outp_int = int(outp)
            cache_int = int(cache)
            tot_int = int(tot) if tot > 0 else (inp_int + outp_int + cache_int)
            metrics.input_tokens += inp_int
            metrics.output_tokens += outp_int
            metrics.cached_tokens += cache_int
            metrics.total_tokens += tot_int
            has_explicit_tokens = True

        # 3. Tool calls parsing
        collected_tool_calls: List[Dict[str, Any]] = []
        if isinstance(entry.get("tool_calls"), list):
            for tc in entry["tool_calls"]:
                if isinstance(tc, dict):
                    collected_tool_calls.append(tc)
        elif entry.get("tool_name") or entry.get("tool") or entry.get("toolAction"):
            tname = entry.get("tool_name") or entry.get("tool") or entry.get("toolAction")
            args = entry.get("args") or entry.get("tool_input") or {}
            collected_tool_calls.append({"name": tname, "args": args})
        elif "function_call" in entry and isinstance(entry["function_call"], dict):
            collected_tool_calls.append({
                "name": entry["function_call"].get("name"),
                "args": entry["function_call"].get("arguments") or {},
            })

        for tc in collected_tool_calls:
            tname = tc.get("name") or tc.get("function", {}).get("name")
            if not tname:
                continue
            metrics.tool_calls_count += 1
            t_str = str(tname)
            metrics.tool_histogram[t_str] = metrics.tool_histogram.get(t_str, 0) + 1

            targs = tc.get("args") or tc.get("arguments") or tc.get("parameters") or {}
            if isinstance(targs, str):
                try:
                    targs = json.loads(targs)
                except Exception:
                    targs = {}

            # Check view_file / read_file on forbidden inspection targets
            if t_str in ("view_file", "read_file"):
                target_path = _clean_str(targs.get("AbsolutePath") or targs.get("Path") or targs.get("file_path"))
                target_norm = target_path.replace("\\", "/").lower()
                for s in MONITORED_INSPECTION_TARGETS:
                    s_norm = s.replace("\\", "/").lower()
                    if s_norm in target_norm:
                        target_key = s.strip("/\\")
                        metrics.script_execution_counts[target_key] = metrics.script_execution_counts.get(target_key, 0) + 1

            # Check run_command script execution
            raw_cmd = ""
            if isinstance(targs, dict):
                raw_cmd = _clean_str(targs.get("CommandLine") or targs.get("cmd") or targs.get("command"))
            elif t_str in ("run_command", "bash", "execute_command"):
                raw_cmd = _clean_str(entry.get("CommandLine") or entry.get("content"))

            if raw_cmd:
                matches = script_regex.findall(raw_cmd)
                for m in matches:
                    metrics.script_execution_counts[m] = metrics.script_execution_counts.get(m, 0) + 1

                # Check consecutive failures
                output = str(entry.get("output") or entry.get("result") or "")
                is_error = "FAIL" in output or "Error" in output or "Traceback" in output or entry.get("exit_code", 0) != 0
                if matches and is_error:
                    consecutive_script_failures += 1
                    max_consecutive = max(max_consecutive, consecutive_script_failures)
                elif matches and not is_error and ("OK" in output or "passed" in output.lower()):
                    consecutive_script_failures = 0

            # Check completion signal inside send_message tool call
            if t_str == "send_message":
                msg_content = _clean_str(targs.get("Message") or targs.get("content"))
                done_m = re.search(r"DONE::?\s*([^\n\r]+)", msg_content)
                if done_m:
                    metrics.is_completed = True
                    metrics.completion_signal = done_m.group(0).strip()

        # Check completion signal in plain message content (only from model/assistant)
        if is_model_step:
            msg_text = str(entry.get("content") or entry.get("message") or "")
            done_m = re.search(r"DONE::?\s*([^\n\r]+)", msg_text)
            if done_m:
                metrics.is_completed = True
                metrics.completion_signal = done_m.group(0).strip()

        # Extract unit_id from initial system prompt / instructions
        if not metrics.unit_id:
            unit_m = re.search(r"(?:Shard Author|Author Shard|shard_id|unit_id|Shard)\s*[`: ]\s*([a-zA-Z0-9_\-]+)", msg_text, re.I)
            if unit_m:
                metrics.unit_id = unit_m.group(1).strip("`_")

        # Extract assigned competencies
        if "COMPETENCIES" in msg_text or "Competencia:" in msg_text or "assigned_competencies" in msg_text:
            found_cids = re.findall(r"(?:Competencia:\s*`?([A-Za-z0-9_\-]+)`?|###\s*Competencia:\s*`?([A-Za-z0-9_\-]+)`?)", msg_text)
            for c1, c2 in found_cids:
                cid = c1 or c2
                if cid and cid not in metrics.assigned_competency_ids:
                    metrics.assigned_competency_ids.append(cid)

        # Check referenced work order file to extract exact unit and competencies
        wo_m = re.search(r"(?:work order is|work order)\s*`?([a-zA-Z0-9_\-./\\]+\.json)`?", msg_text)
        if wo_m:
            wo_cand = Path(wo_m.group(1))
            wo_path = None
            if wo_cand.is_file():
                wo_path = wo_cand
            elif (REPO_ROOT / wo_cand).is_file():
                wo_path = REPO_ROOT / wo_cand
            elif (path.parent / wo_cand).is_file():
                wo_path = path.parent / wo_cand

            if wo_path and wo_path.is_file():
                try:
                    wo_data = json.loads(wo_path.read_text(encoding="utf-8"))
                    if not metrics.unit_id and wo_data.get("shard_id"):
                        metrics.unit_id = str(wo_data["shard_id"])
                    if metrics.role == "unknown" and wo_data.get("Role"):
                        metrics.role = str(wo_data["Role"])
                    for cid in wo_data.get("assigned_competencies", []):
                        cid_str = str(cid)
                        if cid_str and cid_str not in metrics.assigned_competency_ids:
                            metrics.assigned_competency_ids.append(cid_str)
                except Exception:
                    pass

    if metrics.turn_count == 0 and parsed_entries_count > 0:
        metrics.turn_count = parsed_entries_count

    # 4. Cumulative context/cache token estimator when compact transcript omits explicit token usage
    if not has_explicit_tokens:
        char_tokens = sum(max(1, len(l) // 4) for l in lines)
        if metrics.turn_count > 0:
            est_cached = sum((20_000 + 800 * k) for k in range(1, metrics.turn_count + 1))
            est_total = sum((20_300 + 800 * k) for k in range(1, metrics.turn_count + 1))
            metrics.total_tokens = max(char_tokens, est_total)
            metrics.cached_tokens = est_cached
        else:
            metrics.total_tokens = char_tokens

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
    if (metrics.max_consecutive_script_failures >= max_script_loops or total_script_calls >= max_script_loops):
        runaway_reasons.append(
            f"Script loop detected: Tool script loop with {metrics.max_consecutive_script_failures} consecutive failures or {total_script_calls} calls without progress"
        )

    is_hard_breach = (metrics.turn_count > max_turns) or (metrics.total_tokens > max_tokens)

    if is_hard_breach:
        is_runaway = True
        rec_action = "kill_and_redispatch"
    elif not metrics.is_completed and len(runaway_reasons) > 0:
        is_runaway = True
        rec_action = "kill_and_redispatch"
    elif metrics.is_completed:
        is_runaway = False
        rec_action = "completed"
    else:
        is_runaway = False
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
    subagent_ids: Optional[List[str]] = None,
    app_data_dir: Optional[Union[str, Path]] = None,
) -> List[SubagentWatchdogReport]:
    """Scans all transcript files in work_dir and Antigravity brain storage."""
    work = Path(work_dir).resolve()
    reports: List[SubagentWatchdogReport] = []

    # Search paths for transcripts
    candidates: List[Path] = []
    candidates.extend(work.glob("transcripts/*.jsonl"))
    candidates.extend(work.glob("transcripts/**/transcript*.jsonl"))
    candidates.extend(work.glob("dispatch/transcripts/*.jsonl"))
    candidates.extend(work.glob("*.jsonl"))

    # Discover subagents from work/state.json
    discovered_ids: Set[str] = set()
    if subagent_ids:
        discovered_ids.update(subagent_ids)

    state_file = work / "state.json"
    if state_file.is_file():
        try:
            st = json.loads(state_file.read_text(encoding="utf-8"))
            for item in st.get("subagents_summary", []):
                cid = item.get("conversation_id") or item.get("id")
                if cid:
                    discovered_ids.add(str(cid))
            subagents_map = st.get("subagents", {})
            if isinstance(subagents_map, dict):
                for k in subagents_map.keys():
                    discovered_ids.add(str(k))
            elif isinstance(subagents_map, list):
                for item in subagents_map:
                    cid = item.get("conversation_id") or item.get("id") or item.get("subagent_id")
                    if cid:
                        discovered_ids.add(str(cid))
        except Exception as e:
            logger.debug("Could not parse state.json for subagent IDs: %s", e)

    # Discover subagents from dispatch files
    for df in list(work.glob("dispatch/*.json")) + list(work.glob("dispatch/items/*.json")):
        try:
            d_data = json.loads(df.read_text(encoding="utf-8"))
            if isinstance(d_data, dict):
                for s in d_data.get("Subagents", []):
                    if isinstance(s, dict) and s.get("conversation_id"):
                        discovered_ids.add(str(s["conversation_id"]))
        except Exception:
            pass

    # Resolve brain transcripts for discovered IDs
    for sid in discovered_ids:
        brain_tr = resolve_brain_transcript(sid, app_data_dir=app_data_dir)
        if brain_tr:
            candidates.append(brain_tr)

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

    # Also check completed shard outputs for certified competencies
    shards_dir = work / "shards"
    if shards_dir.is_dir():
        for sf in shards_dir.glob("*.json"):
            if sf.name == "pre_shard_manifest.json":
                continue
            try:
                sdata = json.loads(sf.read_text(encoding="utf-8"))
                for q in sdata.get("questions", []):
                    qid = q.get("id") or q.get("competency_id")
                    if qid:
                        certified_cids.add(qid)
            except Exception:
                pass

    unfinished: List[Dict[str, Any]] = []
    for rep in runaway_reports:
        if not rep.is_runaway:
            continue

        cids = list(rep.metrics.assigned_competency_ids)
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


def _resolve_python_executable() -> str:
    """Finds best python executable: .venv/Scripts/python.exe if present, else sys.executable."""
    candidates = [
        REPO_ROOT / ".venv" / "Scripts" / "python.exe",
        Path(".venv/Scripts/python.exe").resolve(),
        Path(sys.prefix) / "Scripts" / "python.exe",
    ]
    for c in candidates:
        if c.is_file():
            return c.resolve().as_posix()
    return sys.executable


def generate_repair_redispatch(
    work_dir: Union[str, Path],
    runaway_reports: List[SubagentWatchdogReport],
) -> Dict[str, Any]:
    """Generates targeted repair re-dispatch payload with modular shard_fixes for unfinished competencies."""
    work = Path(work_dir).resolve()
    unfinished = identify_unfinished_competencies(work, runaway_reports)

    if not unfinished:
        logger.info("Watchdog: No unfinished competencies found for re-dispatch.")
        return {"Subagents": [], "unfinished_count": 0, "item_files": [], "next_schedule_seconds": 300}

    dispatch_items_dir = work / "dispatch" / "items"
    dispatch_items_dir.mkdir(parents=True, exist_ok=True)

    shard_fixes_dir = work / "shards" / "shard_fixes"
    shard_fixes_dir.mkdir(parents=True, exist_ok=True)

    python_bin = _resolve_python_executable()

    subagents: List[Dict[str, Any]] = []
    item_files: List[str] = []

    for idx, item in enumerate(unfinished, start=1):
        cid = item["competency_id"]
        unit_id = item["unit_id"]
        reasons = item["reasons"]

        fix_py = f"work/shards/shard_fixes/{cid}.py"
        out_py = f"work/shards/{unit_id}_data.py"
        out_json = f"work/shards/{unit_id}.json"

        compile_cmd = (
            f'"{python_bin}" .agents/skills/content-to-course/compile_shard.py '
            f'--work "{work.as_posix()}" --shard {unit_id} '
            f'--input {out_py} --output {out_json} '
            f'--cta {work.as_posix()}/cta.json --manifest {work.as_posix()}/pre_cta_manifest.json'
        )

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
            "modular_fix_file": fix_py,
            "output_python": out_py,
            "output_json": out_json,
            "compile_command": compile_cmd,
            "instructions": (
                f"Write modular fix for {cid} in {fix_py}, patch into {out_py}, "
                f"re-compile with --work \"{work.as_posix()}\" --shard {unit_id}, "
                f"and finish strictly with: DONE: {out_json}"
            ),
        }

        item_file = dispatch_items_dir / f"watchdog_repair_{idx:02d}.json"
        item_file.write_text(json.dumps(work_order_data, indent=2, ensure_ascii=False), encoding="utf-8")
        item_files.append(item_file.resolve().as_posix())

        item_rel = f"work/dispatch/items/{item_file.name}"
        pointer_prompt = (
            f"You are Watchdog Repair Engineer {cid}. "
            f"Your work order is `{item_rel}`. Read it first with `view_file`, "
            f"write modular fix `{fix_py}`, patch into `{out_py}`, compile and certify. "
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
        "next_schedule_seconds": 300,
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
    parser.add_argument("--app-data-dir", default=None, help="Antigravity appDataDir for brain transcripts")
    parser.add_argument("--subagent-ids", default=None, help="Comma-separated subagent IDs to inspect")
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

    subagent_id_list = [s.strip() for s in args.subagent_ids.split(",") if s.strip()] if args.subagent_ids else None

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

    # Scan work-dir and brain transcripts
    reports = scan_work_transcripts(
        args.work_dir,
        max_turns=args.max_turns,
        max_tokens=args.max_tokens,
        max_script_loops=args.max_script_loops,
        subagent_ids=subagent_id_list,
        app_data_dir=args.app_data_dir,
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
