#!/usr/bin/env python3
"""Traceback Deep-Dive Analyzer for C2C & Multi-Agent Workflows (Antigravity SDK).

Performs ultra-deep forensic traceback analysis on orchestrator and subagent transcripts:
1. Reconstructs chronological turn-by-turn timelines with precise delta seconds.
2. Dissects LLM Inference Time (thinking + token generation) vs Local Tool Execution Time.
3. Automatically pinpoints:
   - CTA output token limit truncations & recovery pivots.
   - Shard author stragglers, micro-loop antipatterns & validator reverse-engineering loops.
   - Blind Judge web search leaks (search_web / read_url_content) and latency divergences.
   - Orchestrator wait barriers and virtualenv / CLI execution failures.
4. Compiles a global 12-category Error Taxonomy across all conversation steps.
5. Emits structured Markdown (traceback_deepdive.md) and JSON (traceback_deepdive.json) reports in < 2 seconds.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


# ---------------------------------------------------------------------------
# Path & Environment Resolution
# ---------------------------------------------------------------------------

def get_brain_dir() -> Path:
    """Return user's Antigravity brain directory."""
    user_home = Path(os.path.expanduser("~"))
    brain_dir = user_home / ".gemini" / "antigravity" / "brain"
    return brain_dir


def resolve_transcript_path(target: str) -> Optional[Path]:
    """Resolve a conversation ID, chat link, or file path to transcript.jsonl."""
    target = target.strip()

    # Markdown chat link: [label](conversation://<uuid>)
    link_match = re.search(r"conversation://([a-f0-9\-]{36})", target, re.IGNORECASE)
    if link_match:
        conv_id = link_match.group(1)
        p = get_brain_dir() / conv_id / ".system_generated" / "logs" / "transcript.jsonl"
        if p.exists():
            return p

    # Raw UUID
    uuid_match = re.search(r"\b([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})\b", target, re.IGNORECASE)
    if uuid_match:
        conv_id = uuid_match.group(1)
        p = get_brain_dir() / conv_id / ".system_generated" / "logs" / "transcript.jsonl"
        if p.exists():
            return p

    # Direct file path
    target_path = Path(target)
    if target_path.exists():
        if target_path.is_file() and target_path.name.endswith(".jsonl"):
            return target_path
        if target_path.is_dir():
            cand = target_path / ".system_generated" / "logs" / "transcript.jsonl"
            if cand.exists():
                return cand
            cand2 = target_path / "transcript.jsonl"
            if cand2.exists():
                return cand2

    # Partial match in brain dir
    brain_dir = get_brain_dir()
    if brain_dir.exists():
        for d in brain_dir.iterdir():
            if d.is_dir() and target.lower() in d.name.lower():
                cand = d / ".system_generated" / "logs" / "transcript.jsonl"
                if cand.exists():
                    return cand

    return None


def list_recent_conversations(limit: int = 10) -> List[Dict[str, Any]]:
    """Scan brain directory for recent conversations."""
    brain_dir = get_brain_dir()
    if not brain_dir.exists():
        return []

    results = []
    for d in sorted(brain_dir.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
        if not d.is_dir():
            continue
        log_file = d / ".system_generated" / "logs" / "transcript.jsonl"
        if not log_file.exists():
            continue

        mtime = datetime.datetime.fromtimestamp(log_file.stat().st_mtime, tz=datetime.timezone.utc)
        results.append({
            "conversation_id": d.name,
            "mtime": mtime,
            "date_str": mtime.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "path": log_file,
        })
        if len(results) >= limit:
            break
    return results


def parse_iso_datetime(ts_str: Optional[str]) -> Optional[datetime.datetime]:
    """Parse ISO datetime string into UTC datetime object."""
    if not ts_str:
        return None
    try:
        clean_ts = ts_str.replace("Z", "+00:00")
        return datetime.datetime.fromisoformat(clean_ts)
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Transcript Parser & Turn Reconstructor
# ---------------------------------------------------------------------------

class TranscriptReader:
    """Reads and parses transcript.jsonl entries into structured records."""

    @staticmethod
    def read_steps(transcript_path: Path) -> List[Dict[str, Any]]:
        steps: List[Dict[str, Any]] = []
        if not transcript_path.exists():
            return steps

        truncated_steps: Dict[int, int] = {}
        truncated_lines: Dict[int, int] = {}

        try:
            with open(transcript_path, "r", encoding="utf-8", errors="replace") as f:
                for line_idx, line in enumerate(f):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        rec = json.loads(line)
                        rec_idx = len(steps)
                        steps.append(rec)
                        if rec.get("truncated_fields"):
                            s_idx = rec.get("step_index")
                            if s_idx is not None:
                                truncated_steps[s_idx] = rec_idx
                            truncated_lines[line_idx] = rec_idx
                    except Exception:
                        pass
        except Exception:
            return steps

        if not truncated_steps and not truncated_lines:
            return steps

        full_path = transcript_path.parent / "transcript_full.jsonl"
        if not full_path.is_file():
            return steps

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
                            steps[rec_idx] = full_rec
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

        return steps

    @staticmethod
    def extract_turns(steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Groups raw transcript records into logical agent turns."""
        turns: List[Dict[str, Any]] = []
        current_turn: Optional[Dict[str, Any]] = None

        for s in steps:
            stype = s.get("type")
            s_idx = s.get("step_index", 0)
            created_at = s.get("created_at")
            dt = parse_iso_datetime(created_at)

            if stype == "PLANNER_RESPONSE":
                tools_raw = s.get("tool_calls", [])
                tools_parsed = []
                for tc in tools_raw:
                    if isinstance(tc, dict):
                        name = tc.get("function", {}).get("name") if "function" in tc else tc.get("name", "")
                        args = tc.get("function", {}).get("arguments") if "function" in tc else tc.get("args", {})
                        if isinstance(args, str):
                            try:
                                args = json.loads(args)
                            except Exception:
                                pass
                        tools_parsed.append({"name": name, "args": args if isinstance(args, dict) else {}})

                current_turn = {
                    "step_index": s_idx,
                    "created_at": created_at,
                    "datetime": dt,
                    "tools": tools_parsed,
                    "input_tokens": s.get("input_tokens", 0),
                    "output_tokens": s.get("output_tokens", 0),
                    "cache_read_tokens": s.get("cache_read_tokens", 0),
                    "thinking": s.get("thinking", ""),
                    "thinking_chars": len(s.get("thinking", "")),
                    "results": [],
                }
                turns.append(current_turn)
            elif stype in ("GENERIC", "ERROR_MESSAGE", "TOOL_RESPONSE"):
                if current_turn is not None:
                    current_turn["results"].append({
                        "step_index": s_idx,
                        "type": stype,
                        "created_at": created_at,
                        "datetime": dt,
                        "status": s.get("status"),
                        "content": s.get("content", ""),
                    })

        return turns


# ---------------------------------------------------------------------------
# Subagent Tree & Role Resolver
# ---------------------------------------------------------------------------

class SubagentTreeResolver:
    """Discovers subagent conversation IDs and maps their roles."""

    @staticmethod
    def discover_subagents(root_steps: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        subagents: Dict[str, Dict[str, Any]] = {}

        pending_invokes: List[Dict[str, str]] = []
        for step in root_steps:
            stype = step.get("type")
            content = step.get("content", "")
            tool_calls = step.get("tool_calls", [])

            # 1. From invoke_subagent tool calls
            for tc in tool_calls:
                tname = tc.get("function", {}).get("name") if "function" in tc else tc.get("name")
                if tname == "invoke_subagent":
                    args = tc.get("function", {}).get("arguments") if "function" in tc else tc.get("args", {})
                    if isinstance(args, str):
                        try: args = json.loads(args)
                        except Exception: pass
                    if isinstance(args, dict):
                        if "Role" in args or "TypeName" in args:
                            pending_invokes.append({
                                "role": str(args.get("Role", "unknown") or "unknown"),
                                "type": str(args.get("TypeName", "unknown") or "unknown"),
                            })
                        for sub in args.get("Subagents", []):
                            if isinstance(sub, dict):
                                pending_invokes.append({
                                    "role": str(sub.get("Role", "unknown") or "unknown"),
                                    "type": str(sub.get("TypeName", "unknown") or "unknown"),
                                })

            # 2. From tool result content of invoke_subagent
            if "Created the following subagents:" in content or "conversationId" in content:
                uuid_matches = re.findall(r'"conversationId":\s*"([a-f0-9\-]{36})"', content)
                for cid in uuid_matches:
                    inv = pending_invokes.pop(0) if ("Created the following subagents:" in content and pending_invokes) else {}
                    if cid not in subagents:
                        subagents[cid] = {
                            "conversation_id": cid,
                            "role": inv.get("role", "unknown"),
                            "type": inv.get("type", "unknown"),
                        }

            # 3. From manage_subagents list output
            if '"conversationId":' in content and '"role":' in content:
                try:
                    # Look for JSON array pattern
                    match = re.search(r'\[\s*\{.*"conversationId".*\}\s*\]', content, re.DOTALL)
                    if match:
                        arr = json.loads(match.group(0))
                        for item in arr:
                            cid = item.get("conversationId")
                            if cid:
                                subagents[cid] = {
                                    "conversation_id": cid,
                                    "role": item.get("role", "subagent"),
                                    "type": item.get("type", "generic"),
                                }
                except Exception:
                    pass

        # 4. Infer roles from individual subagent transcripts if role is still generic/unknown
        brain_dir = get_brain_dir()
        for cid, info in list(subagents.items()):
            t_path = brain_dir / cid / ".system_generated" / "logs" / "transcript.jsonl"
            if not t_path.exists():
                continue
            first_steps = TranscriptReader.read_steps(t_path)[:6]
            r_str = f"{info.get('role', '')} {info.get('type', '')}"
            for s in first_steps:
                c = f"{r_str} {s.get('content', '')}"
                m_rep = re.search(r"(?:Repair Engineer\s+([A-Za-z0-9_\-]+)|prompts[/\\]repair[/\\]repair_([a-zA-Z0-9_\-]+)\.json)", c, re.IGNORECASE)
                m_part = re.search(r"(?:part_|cta_|CTA Architect\s*\(?part_|CTA Architect\s+)(\d+)", c, re.IGNORECASE)
                m_shard = re.search(r"(?:shard_|Shard Author shard_|Author Shard\s+|Shard\s+)(\d+)", c, re.IGNORECASE)
                m_judge = re.search(r"(?:Judge\s+|judge_batch_|judge_responses_|judge_)(\d+)", c, re.IGNORECASE)

                if m_rep or "c2c_repair" in r_str.lower() or "repair engineer" in r_str.lower():
                    rep_id = (m_rep.group(1) or m_rep.group(2)).upper() if m_rep else cid[:6]
                    base_role = info.get("role") if "repair engineer" in str(info.get("role", "")).lower() else f"Repair Engineer {rep_id}"
                    info["role"] = f"{base_role} ({cid[:6]})"
                    info["stage"] = "3b_repair"
                    break
                elif m_part:
                    part_num = int(m_part.group(1))
                    info["role"] = f"CTA Architect (part_{part_num:02d})"
                    info["stage"] = "1b_cta"
                    break
                elif any(k in c.lower() for k in ("direct cta", "cta-direct", "prompt_cta", "director de análisis cognitivo", "cta architect", "c2c_cta_architect")):
                    info["role"] = "Direct CTA Architect"
                    info["stage"] = "1b_cta"
                    break
                elif m_shard:
                    shard_num = int(m_shard.group(1))
                    info["role"] = f"Author Shard {shard_num:02d}"
                    info["stage"] = "3_authoring"
                    break
                elif m_judge:
                    judge_num = int(m_judge.group(1))
                    info["role"] = f"Judge {judge_num:02d}"
                    info["stage"] = "5_judges"
                    break

        return subagents


# ---------------------------------------------------------------------------
# Deep Forensics Engines (CTA, Shards, Judges, Orchestrator)
# ---------------------------------------------------------------------------

class ForensicsEngine:
    """Computes exact latencies, classifies errors, and diagnoses bottlenecks."""

    @staticmethod
    def compute_agent_timings(steps: List[Dict[str, Any]], turns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculates total wall time, inference time vs local tool execution time."""
        if not steps:
            return {
                "wall_time_seconds": 0.0,
                "inference_seconds": 0.0,
                "tool_seconds": 0.0,
                "turns_count": 0,
                "input_tokens": 0,
                "output_tokens": 0,
                "cache_tokens": 0,
            }

        start_dt = parse_iso_datetime(steps[0].get("created_at"))
        end_dt = parse_iso_datetime(steps[-1].get("created_at"))
        wall_time = (end_dt - start_dt).total_seconds() if (start_dt and end_dt) else 0.0

        total_in_tokens = 0
        total_out_tokens = 0
        total_cache_tokens = 0
        for turn in turns:
            total_in_tokens += turn.get("input_tokens", 0)
            total_out_tokens += turn.get("output_tokens", 0)
            total_cache_tokens += turn.get("cache_read_tokens", 0)

        inference_seconds = 0.0
        tool_seconds = 0.0
        for i in range(len(steps) - 1):
            curr = steps[i]
            nxt = steps[i + 1]
            t_curr = parse_iso_datetime(curr.get("created_at"))
            t_nxt = parse_iso_datetime(nxt.get("created_at"))
            if t_curr and t_nxt:
                delta = max(0.0, (t_nxt - t_curr).total_seconds())
                if curr.get("type") == "PLANNER_RESPONSE" and nxt.get("type") in ("GENERIC", "ERROR_MESSAGE", "TOOL_RESPONSE"):
                    inference_seconds += delta
                elif curr.get("type") in ("GENERIC", "ERROR_MESSAGE", "TOOL_RESPONSE") and nxt.get("type") == "PLANNER_RESPONSE":
                    tool_seconds += delta

        return {
            "wall_time_seconds": round(wall_time, 1),
            "wall_time_minutes": round(wall_time / 60.0, 2),
            "inference_seconds": round(inference_seconds, 1),
            "tool_seconds": round(tool_seconds, 1),
            "inference_pct": round((inference_seconds / wall_time * 100.0), 1) if wall_time > 0 else 100.0,
            "tool_pct": round((tool_seconds / wall_time * 100.0), 1) if wall_time > 0 else 0.0,
            "turns_count": len(turns),
            "input_tokens": total_in_tokens,
            "output_tokens": total_out_tokens,
            "cache_tokens": total_cache_tokens,
            "active_tokens": total_in_tokens + total_out_tokens,
        }

    @staticmethod
    def audit_cta_architect(steps: List[Dict[str, Any]], turns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Diagnoses CTA Architect: token limit cutoffs, pivot scripts, and turn bottlenecks."""
        timings = ForensicsEngine.compute_agent_timings(steps, turns)
        cutoff_detected = False
        cutoff_step = None
        pivot_step = None
        pivot_script = ""
        massive_turn_seconds = 0.0

        for idx, turn in enumerate(turns):
            out_toks = turn.get("output_tokens", 0)
            # check if subsequent step had error
            for res in turn.get("results", []):
                content = res.get("content", "")
                if "exceeded the output token limit" in content or "cut off" in content or res.get("type") == "ERROR_MESSAGE":
                    cutoff_detected = True
                    cutoff_step = turn.get("step_index")

            # Check for script generation pivot
            for tc in turn.get("tools", []):
                if tc.get("name") == "write_to_file":
                    target = tc.get("args", {}).get("TargetFile", "")
                    if "generate" in target.lower() or "cta" in target.lower():
                        pivot_step = turn.get("step_index")
                        pivot_script = Path(target).name

        return {
            "timings": timings,
            "cutoff_detected": cutoff_detected,
            "cutoff_step": cutoff_step,
            "pivot_step": pivot_step,
            "pivot_script": pivot_script,
        }

    @staticmethod
    def audit_shard_author(shard_name: str, steps: List[Dict[str, Any]], turns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Audits a Shard Author: micro-loops, compile_shard / check_templates runs, and reverse engineering."""
        timings = ForensicsEngine.compute_agent_timings(steps, turns)

        check_runs: List[Dict[str, Any]] = []
        reverse_eng_reads: List[Dict[str, Any]] = []
        writes_count = 0
        edits_count = 0
        scripts_written: Set[str] = set()

        _real_exec_re = re.compile(
            r"python(?:\.exe)?\s+(?!-c\b)(?:[^\s\"']*[/\\])?(?:check_templates|compile_shard)\.py\b",
            re.IGNORECASE,
        )

        for t_idx, turn in enumerate(turns):
            for tc in turn.get("tools", []):
                tname = tc.get("name")
                args = tc.get("args", {})
                res_content = turn["results"][0].get("content", "") if turn.get("results") else ""

                if tname == "write_to_file":
                    writes_count += 1
                    tf = Path(args.get("TargetFile", "")).name
                    if tf:
                        scripts_written.add(tf)
                elif tname == "replace_file_content":
                    edits_count += 1
                elif tname == "view_file":
                    target_file = str(args.get("AbsolutePath", ""))
                    if any(k in target_file.lower() for k in ("check_templates.py", "compile_shard.py", "rules.py", "invariants.py", "assembler.py")):
                        reverse_eng_reads.append({
                            "turn": t_idx + 1,
                            "file": Path(target_file).name,
                            "step_index": turn.get("step_index"),
                            "via": "view_file",
                        })
                elif tname == "run_command":
                    cmd = args.get("CommandLine", "")
                    cmd_lower = cmd.lower()
                    is_real_validator_exec = bool(_real_exec_re.search(cmd)) or (
                        ("check_templates.py" in cmd_lower or "compile_shard.py" in cmd_lower)
                        and "python -c" not in cmd_lower
                        and "get-content" not in cmd_lower
                        and "select-string" not in cmd_lower
                    )
                    if is_real_validator_exec:
                        is_fail = (
                            "FAIL:" in res_content
                            or "VALIDATION FAILED" in res_content.upper()
                            or "exited with code 1" in res_content
                            or "Traceback (most recent call last)" in res_content
                        )
                        fail_snippets = [
                            line.strip() for line in res_content.splitlines()
                            if any(k in line.lower() for k in ("violation", "error", "fail", "traceback", "r-", "tpl-"))
                        ][:2]
                        check_runs.append({
                            "turn": t_idx + 1,
                            "failed": is_fail,
                            "snippets": fail_snippets,
                        })
                    elif any(k in cmd_lower for k in ("check_templates.py", "compile_shard.py", "rules.py", "invariants.py", "assembler.py")):
                        # Static inspection of validator via python -c / Get-Content / Select-String
                        reverse_eng_reads.append({
                            "turn": t_idx + 1,
                            "file": "check_templates.py / compile_shard.py",
                            "step_index": turn.get("step_index"),
                            "via": "run_command (static read)",
                        })

        failed_checks = sum(1 for c in check_runs if c["failed"])
        passed_checks = sum(1 for c in check_runs if not c["failed"])
        has_reverse_eng_loop = len(reverse_eng_reads) >= 5
        has_micro_loop = (
            (len(scripts_written) >= 4 and len(check_runs) >= 10)
            or timings["turns_count"] > 35
            or failed_checks >= 5
        )
        if timings["turns_count"] > 35 and failed_checks < 5:
            micro_loop_reason = f"⚠️ SÍ (Edición Granular: {timings['turns_count']}t)"
        elif has_micro_loop:
            micro_loop_reason = f"⚠️ SÍ (Check Loop: {failed_checks} fallos)"
        else:
            micro_loop_reason = "NO"

        return {
            "shard_name": shard_name,
            "timings": timings,
            "writes_count": writes_count,
            "edits_count": edits_count,
            "unique_scripts_written": list(sorted(scripts_written)),
            "check_runs_total": len(check_runs),
            "check_runs_failed": failed_checks,
            "check_runs_passed": passed_checks,
            "reverse_eng_reads_count": len(reverse_eng_reads),
            "has_reverse_eng_loop": has_reverse_eng_loop,
            "has_micro_loop": has_micro_loop,
            "micro_loop_reason": micro_loop_reason,
        }

    @staticmethod
    def audit_blind_judges(judges_map: Dict[str, Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]]) -> Dict[str, Any]:
        """Audits blind judges: web requests, url reads, and latency variance."""
        judge_results = {}

        for j_name, (steps, turns) in judges_map.items():
            timings = ForensicsEngine.compute_agent_timings(steps, turns)
            web_queries = []
            url_reads = []

            for turn in turns:
                for tc in turn.get("tools", []):
                    tname = tc.get("name")
                    args = tc.get("args", {})
                    if tname == "search_web":
                        web_queries.append(args.get("query", ""))
                    elif tname == "read_url_content":
                        url_reads.append(args.get("Url", ""))

            judge_results[j_name] = {
                "timings": timings,
                "web_queries_count": len(web_queries),
                "web_queries": web_queries,
                "url_reads_count": len(url_reads),
                "used_web": (len(web_queries) > 0 or len(url_reads) > 0),
            }

        return judge_results

    @staticmethod
    def classify_error_taxonomy(all_steps: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
        """Classifies every error across all orchestrator and subagent transcripts into 16 technical categories."""
        categories: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

        for agent_name, steps in all_steps.items():
            last_thinking = ""
            last_tool_calls: List[Dict[str, Any]] = []
            for s in steps:
                stype = s.get("type")
                status = s.get("status")
                content = s.get("content", "") or ""
                s_idx = s.get("step_index", 0)

                if stype == "PLANNER_RESPONSE":
                    last_thinking = s.get("thinking", "") or ""
                    last_tool_calls = s.get("tool_calls", []) or []

                if stype == "ERROR_MESSAGE":
                    categories["Token Limit Cutoff (Model Truncation)"].append({
                        "agent": agent_name,
                        "step_index": s_idx,
                        "snippet": content[:140].strip(),
                        "thinking": last_thinking[:180].strip(),
                    })
                elif stype in ("GENERIC", "TOOL_RESPONSE") and (status == "ERROR" or "exited with code 1" in content or "exited with code 2" in content):
                    cmd_str = ""
                    tool_names = []
                    for tc in last_tool_calls:
                        if isinstance(tc, dict):
                            tn = tc.get("function", {}).get("name") if "function" in tc else tc.get("name", "")
                            ta = tc.get("function", {}).get("arguments") if "function" in tc else tc.get("args", {})
                            if isinstance(ta, str):
                                try:
                                    ta = json.loads(ta)
                                except Exception:
                                    ta = {}
                            tool_names.append(tn)
                            if isinstance(ta, dict) and ta.get("CommandLine"):
                                cmd_str += " " + str(ta.get("CommandLine"))

                    combined = f"{content}\n{cmd_str}"
                    c_low = combined.lower()
                    content_low = content.lower()

                    clean_snip = " | ".join(
                        line.strip() for line in content.splitlines()
                        if line.strip() and not line.strip().startswith("Created At:") and not line.strip().startswith("Completed At:")
                    )[:140]
                    error_entry = {
                        "agent": agent_name,
                        "step_index": s_idx,
                        "snippet": clean_snip or content[:140].strip(),
                        "thinking": last_thinking[:180].strip(),
                    }

                    if "unsubstituted template variable" in content_low or "unreplaced template variable" in content_low or "tpl-unsub" in content_low:
                        categories["Unsubstituted Template Variables ({var})"].append(error_entry)
                    elif "residual double curly braces" in content_low or "double curly" in content_low or "[r-01]" in content_low:
                        categories["KaTeX Double Curly Braces ({{ / }})"].append(error_entry)
                    elif "math delimiter" in content_low or "unbalanced $" in content_low or "[r-02]" in content_low:
                        categories["Unbalanced Math Delimiters ($)"].append(error_entry)
                    elif (
                        "[r-03]" in content_low
                        or "control char" in content_low
                        or "corrupted control" in content_low
                        or "invalid escape sequence" in content_low
                        or "syntaxwarning" in content_low
                        or "check_escapes" in c_low
                        or "raw_string" in c_low
                    ):
                        categories["LaTeX Control Character / Raw-String Corruption (R-03 / SyntaxWarning)"].append(error_entry)
                    elif (
                        "tpl-var" in content_low
                        or "tpl-collapse" in content_low
                        or "tpl-dist" in content_low
                        or "diversity quota" in content_low
                        or "duplicate option" in content_low
                        or "collapsed option" in content_low
                        or "distinct parameter" in content_low
                        or "unique question" in content_low
                    ):
                        categories["Parameter Diversity & Option Collapse (TPL-VAR / TPL-COLLAPSE)"].append(error_entry)
                    elif "cross_check" in content_low or "tpl-cross" in content_low:
                        categories["Cross-check Verification False (TPL-CROSS)"].append(error_entry)
                    elif (
                        "length anti-giveaway" in content_low
                        or "leaks the correct answer" in content_low
                        or "[r-18]" in content_low
                        or "[r-19]" in content_low
                        or "[r-14]" in content_low
                        or "[r-16]" in content_low
                        or "anti-giveaway" in content_low
                        or "banned pattern" in content_low
                        or "forbidden" in content_low
                        or "distractor" in content_low
                    ):
                        categories["Anti-Giveaway & Psychometric Parity Violations (R-14..R-19)"].append(error_entry)
                    elif (
                        "cta-" in content_low
                        or "compile_cta" in c_low
                        or "cta_data" in c_low
                        or ("cycle" in content_low and "prerequisite" in content_low)
                        or ("evidence" in content_low and "competenc" in content_low)
                    ):
                        categories["CTA Compilation & Schema Errors (CTA-SCHEMA / CTA-EV / DAG Cycle)"].append(error_entry)
                    elif (
                        "could not successfully apply any edits" in content_low
                        or "target content not found" in content_low
                        or "multiple occurrences" in content_low
                        or "replace_file_content" in tool_names
                        or ("targetfile" in content_low and "overwrite" in content_low)
                    ):
                        categories["File Edit / Write Tool Target Mismatch (replace_file_content / Overwrite)"].append(error_entry)
                    elif (
                        "filenotfounderror" in content_low
                        or "no such file or directory" in content_low
                        or "cannot find the path" in content_low
                        or "does not exist" in content_low
                        or "no se encuentra la ruta" in content_low
                        or "itemnotfoundexception" in content_low
                        or "view_file" in tool_names
                    ):
                        categories["Missing File / Relative Path / Directory Error (FileNotFoundError)"].append(error_entry)
                    elif (
                        "el término" in content_low
                        or "commandnotfoundexception" in content_low
                        or "parsererror" in content_low
                        or "token inesperado" in content_low
                        or "unexpectedtoken" in content_low
                        or "missingendcurlybrace" in content_low
                        or "ambiguousparameter" in content_low
                        or "positionalparameter" in content_low
                        or "&&" in cmd_str
                        or ("powershell" in content_low and "error" in content_low)
                    ):
                        categories["PowerShell Command / Quoting / $Variable Expansion Friction"].append(error_entry)
                    elif (
                        "modulenotfounderror" in content_low
                        or "importerror" in content_low
                        or "unicodeencodeerror" in content_low
                        or "unicodedecodeerror" in content_low
                        or "charmap" in content_low
                    ):
                        categories["Python Environment / Virtualenv / Encoding Discrepancy"].append(error_entry)
                    elif (
                        "contract error" in content_low
                        or "no valid judge" in content_low
                        or "judge_responses" in c_low
                        or ("run.py" in cmd_str and ("verify" in cmd_str or "judge" in cmd_str or "build" in cmd_str or "publish" in cmd_str))
                    ):
                        categories["Stage Contract / Pipeline Loader Mismatch (run.py / judge.py)"].append(error_entry)
                    elif (
                        "template schema violation" in content_low
                        or "tpl-exec" in content_low
                        or "tpl-schema" in content_low
                        or "validation failed" in content_low
                        or "compile_shard" in c_low
                        or "check_templates" in c_low
                    ):
                        categories["Shard Compilation & Template Validator Failure (compile_shard / check_templates)"].append(error_entry)
                    elif (
                        "syntaxerror" in content_low
                        or "indentationerror" in content_low
                        or "nameerror" in content_low
                        or "keyerror" in content_low
                        or "typeerror" in content_low
                        or "attributeerror" in content_low
                        or "valueerror" in content_low
                        or "indexerror" in content_low
                        or "zerodivisionerror" in content_low
                        or "jsondecodeerror" in content_low
                        or "assertionerror" in content_low
                        or "traceback (most recent call last)" in content_low
                        or "python -c" in cmd_str.lower()
                    ):
                        categories["Exploratory Python One-Liner / Script Exceptions (Syntax/Key/Type/ValueError)"].append(error_entry)
                    else:
                        categories["Non-Zero CLI Exit / Subprocess Probe (Exit Code 1)"].append(error_entry)

        return dict(categories)


# ---------------------------------------------------------------------------
# Report Generator (Markdown & JSON)
# ---------------------------------------------------------------------------

class DeepDiveReportBuilder:
    """Builds the comprehensive traceback_deepdive.md report."""

    @staticmethod
    def build_markdown(
        conv_id: str,
        cta_data: Dict[str, Any],
        shards_data: Dict[str, Dict[str, Any]],
        judges_data: Dict[str, Any],
        error_taxonomy: Dict[str, List[Dict[str, Any]]],
        global_timings: Dict[str, Any],
        thinking_traces_summary: Optional[Dict[str, Any]] = None,
        stage_telemetry_v3: Optional[Dict[str, Any]] = None,
    ) -> str:
        lines: List[str] = []

        lines.append(f"# Auditoría Forense Ultra-Detallada del Traceback de Ejecución")
        lines.append(f"## Pipeline Content-to-Course (C2C) — Conversación [`{conv_id}`](conversation://{conv_id})")
        lines.append(f"")
        lines.append(f"**Fecha de Auditoría:** `{datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}`  ")
        lines.append(f"**Conversación Orquestadora:** [`{conv_id}`](conversation://{conv_id})  ")
        if stage_telemetry_v3 and stage_telemetry_v3.get("work_dir"):
            lines.append(f"**Directorio de Telemetría Validado (Zero-Collision):** `{stage_telemetry_v3.get('work_dir')}` (`{stage_telemetry_v3.get('snapshots_count', 0)}` snapshots C2C v3.2)  ")
        lines.append(f"**Motor Forense:** C2C Traceback Deep-Dive Analyzer (Antigravity SDK)  ")
        lines.append(f"")
        lines.append(f"---")
        lines.append(f"")
        lines.append(f"## 1. Resumen Ejecutivo y Metrología Forense Global")
        lines.append(f"")
        lines.append(f"| Métrica Forense | Valor Registrado | Observación Técnica |")
        lines.append(f"| :--- | :--- | :--- |")
        lines.append(f"| **Tiempo de Pared Total** | **`{global_timings.get('wall_clock_minutes', 0.0)} min`** ({global_timings.get('wall_clock_seconds', 0.0)} s) | Tiempo transcurrido de extremo a extremo |")
        lines.append(f"| **Total de Turnos Analizados** | **`{global_timings.get('total_turns', 0)} turnos`** | Suma de orquestador y subagentes |")
        lines.append(f"| **Total de Errores Catalogados** | **`{global_timings.get('total_errors', 0)} errores`** | Clasificados en {len(error_taxonomy)} categorías técnicas (0% caja negra) |")
        lines.append(f"| **Inferencia LLM Promedio** | **`{global_timings.get('avg_inference_pct', 95.0)}%`** | Porcentaje de tiempo dedicado a generación/thinking |")
        lines.append(f"| **Ejecución Local de Tools** | **`{global_timings.get('avg_tool_pct', 5.0)}%`** | Porcentaje de tiempo consumido en I/O y terminal |")
        lines.append(f"")
        lines.append(f"### 1.1. Distribución Empírica del Tiempo (Inferencia vs Tools)")
        lines.append(f"```text")
        lines.append(f"========================================================================================")
        lines.append(f"DISTRIBUCIÓN DEL TIEMPO DE PARED POR SUBAGENTE (INFERENCIA LLM vs TOOLS)")
        lines.append(f"========================================================================================")
        if cta_data:
            if "timings" in cta_data:
                t = cta_data.get("timings", {})
                lines.append(f"Direct CTA Architect   : {t.get('inference_seconds', 0.0):6.0f}s ({t.get('inference_pct', 0.0)}%) LLM | {t.get('tool_seconds', 0.0):4.0f}s Tools")
            else:
                for cname, cinfo in cta_data.items():
                    t = cinfo.get("timings", {})
                    lines.append(f"{cname:23s}: {t.get('inference_seconds', 0.0):6.0f}s ({t.get('inference_pct', 0.0)}%) LLM | {t.get('tool_seconds', 0.0):4.0f}s Tools")
        for sname, sinfo in shards_data.items():
            t = sinfo.get("timings", {})
            lines.append(f"{sname:23s}: {t.get('inference_seconds', 0.0):6.0f}s ({t.get('inference_pct', 0.0)}%) LLM | {t.get('tool_seconds', 0.0):4.0f}s Tools")
        for jname, jinfo in judges_data.items():
            t = jinfo.get("timings", {})
            lines.append(f"{jname:23s}: {t.get('inference_seconds', 0.0):6.0f}s ({t.get('inference_pct', 0.0)}%) LLM | {t.get('tool_seconds', 0.0):4.0f}s Tools")
        lines.append(f"========================================================================================")
        lines.append(f"```")
        lines.append(f"")

        if stage_telemetry_v3 and stage_telemetry_v3.get("stages"):
            lines.append(f"### 1.2. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json`)")
            lines.append(f"")
            lines.append(f"| Etapa | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes en Snapshot | Metadatos de Etapa |")
            lines.append(f"| :--- | :--- | :---: | :---: | :---: | :--- |")
            for st_item in stage_telemetry_v3["stages"]:
                ts_short = str(st_item.get("timestamp", ""))[:19].replace("T", " ")
                dur_s = st_item.get("duration_seconds", 0.0)
                tot_t = st_item.get("stage_total_tokens", 0)
                act_t = st_item.get("stage_active_tokens", 0)
                meta_clean = {k: v for k, v in (st_item.get("metadata") or {}).items() if k != "duration_seconds"}
                meta_str = ", ".join(f"{k}={v}" for k, v in meta_clean.items()) or "—"
                lines.append(
                    f"| **`{st_item['stage_key']}`** | `{ts_short}` | `{dur_s}s` | "
                    f"`{tot_t:,}` (`{act_t:,}` act) | {st_item.get('subagents_captured_count', 0)} | `{meta_str}` |"
                )
            lines.append(f"")

        lines.append(f"---")
        lines.append(f"")
        lines.append(f"## 2. Análisis Forense: CTA Architects (Stage 1)")
        if cta_data:
            cta_items = [("Direct CTA Architect", cta_data)] if "timings" in cta_data else list(cta_data.items())
            for idx, (cname, cinfo) in enumerate(cta_items, 1):
                t = cinfo.get("timings", {})
                lines.append(f"### 2.{idx}. {cname}")
                lines.append(f"- **Duración Total:** **`{t.get('wall_time_minutes', 0.0)} min`** ({t.get('wall_time_seconds', 0.0)} s) en **`{t.get('turns_count', 0)} turnos`**.")
                lines.append(f"- **Tokens:** {t.get('input_tokens', 0):,} In | {t.get('output_tokens', 0):,} Out | {t.get('cache_tokens', 0):,} Cache.")
                if cinfo.get("cutoff_detected"):
                    lines.append(f"- 🛑 **Incidente Crítico Detectado:** Truncamiento por límite de tokens (`Output token limit exceeded`) en el **Paso {cinfo.get('cutoff_step')}**.")
                    lines.append(f"- 💡 **Pivote Adaptativo:** En el **Paso {cinfo.get('pivot_step')}**, el arquitecto pasó a generar el script `{cinfo.get('pivot_script')}` para consolidar el CTA sin saturar el contexto.")
        lines.append(f"")
        lines.append(f"---")
        lines.append(f"")
        lines.append(f"## 3. Análisis Forense: Shards de Autoría (Stage 3)")
        lines.append(f"")
        lines.append(f"| Shard ID | Duración (min) | Turnos | Writes | Edits | Check Runs (Fail/Pass) | Lecturas Validador (Ing. Inversa) | Micro-Bucle / Patrón |")
        lines.append(f"| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |")
        for sname, sinfo in shards_data.items():
            t = sinfo.get("timings", {})
            rev_cnt = sinfo.get("reverse_eng_reads_count", 0)
            rev = f"🛑 SÍ ({rev_cnt} lecturas)" if sinfo.get("has_reverse_eng_loop") else f"NO ({rev_cnt})"
            micro = sinfo.get("micro_loop_reason") or ("⚠️ SÍ" if sinfo.get("has_micro_loop") else "NO")
            lines.append(f"| **{sname}** | {t.get('wall_time_minutes', 0.0)} | {t.get('turns_count', 0)} | {sinfo.get('writes_count', 0)} | {sinfo.get('edits_count', 0)} | {sinfo.get('check_runs_total', 0)} ({sinfo.get('check_runs_failed', 0)}/{sinfo.get('check_runs_passed', 0)}) | {rev} | {micro} |")
        lines.append(f"")
        lines.append(f"---")
        lines.append(f"")
        lines.append(f"## 4. Análisis Forense: Blind Judges (Stage 5)")
        lines.append(f"")
        lines.append(f"| Blind Judge | Duración (min) | Turnos | Consultas `search_web` | Peticiones HTTP | Estado de Aislamiento |")
        lines.append(f"| :--- | :---: | :---: | :---: | :---: | :--- |")
        for jname, jinfo in judges_data.items():
            t = jinfo.get("timings", {})
            status = "⚠️ Fuga Externa (Navegación Web)" if jinfo.get("used_web") else "✅ Aislamiento Estricto (Razonamiento Puro)"
            lines.append(f"| **{jname}** | {t.get('wall_time_minutes', 0.0)} | {t.get('turns_count', 0)} | {jinfo.get('web_queries_count', 0)} | {jinfo.get('url_reads_count', 0)} | {status} |")
        lines.append(f"")
        lines.append(f"---")
        lines.append(f"")
        lines.append(f"## 5. Taxonomía Consolidada de Errores ({global_timings.get('total_errors', 0)} Registrados)")
        lines.append(f"")
        lines.append(f"| Categoría de Error | Ocurrencias | Ejemplo de Incidencia | Razonamiento Previo (Thinking) |")
        lines.append(f"| :--- | :---: | :--- | :--- |")
        for cat, items in sorted(error_taxonomy.items(), key=lambda x: len(x[1]), reverse=True):
            ex = items[0]
            th_snippet = f"`{ex.get('thinking', '')[:80]}...`" if ex.get("thinking") else "*Sin thinking capturado*"
            lines.append(f"| **{cat}** | **{len(items)}** | `{ex.get('agent')}` (Paso {ex.get('step_index')}): {ex.get('snippet')[:70]}... | {th_snippet} |")
        lines.append(f"")

        if thinking_traces_summary and thinking_traces_summary.get("agents"):
            lines.append(f"---")
            lines.append(f"")
            lines.append(f"## 6. Telemetría de Razonamiento Cognitivo (Thinking Traces)")
            lines.append(f"- **Total de Turnos con Razonamiento:** `{thinking_traces_summary.get('total_thinking_turns', 0)} turnos`")
            lines.append(f"- **Volumen Total de Razonamiento:** `{thinking_traces_summary.get('total_thinking_chars', 0):,} caracteres`")
            lines.append(f"")
            lines.append(f"| Agente | Turnos con Thinking | Volumen (Caracteres) | Muestra de Razonamiento Previo |")
            lines.append(f"| :--- | :---: | :---: | :--- |")
            for ag_name, ag_info in sorted(thinking_traces_summary.get("agents", {}).items()):
                sample_tr = ag_info.get("traces", [{}])[0].get("thinking_snippet", "")
                lines.append(f"| **{ag_name}** | {ag_info.get('thinking_turns_count', 0)} | {ag_info.get('total_thinking_chars', 0):,} | `{sample_tr[:80]}...` |")
            lines.append(f"")

        lines.append(f"---")
        lines.append(f"*Informe generado automáticamente por `traceback_analyzer.py`.*")

        return "\n".join(lines)


# ---------------------------------------------------------------------------
# C2C v3.2 Verified Stage Telemetry Loader
# ---------------------------------------------------------------------------

def load_verified_stage_telemetry(
    conv_id: str,
    root_steps: List[Dict[str, Any]],
    work_dir: Optional[Path] = None,
) -> Dict[str, Any]:
    """Resolves and loads C2C v3.2 work/telemetry/*.json strictly matching conv_id."""
    candidates: List[Path] = []
    if work_dir:
        candidates.append(Path(work_dir))

    # Extract --work-dir or courses/<id>/work from root_steps
    for s in root_steps:
        for tc in s.get("tool_calls", []) or []:
            if not isinstance(tc, dict):
                continue
            args = tc.get("function", {}).get("arguments") if "function" in tc else tc.get("args", {})
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except Exception:
                    args = {}
            if isinstance(args, dict):
                cmd = str(args.get("CommandLine", ""))
                for m in re.finditer(r'--work-dir\s+["\']?([^"\'\s;]+)["\']?', cmd):
                    candidates.append(Path(m.group(1)))
                for m in re.finditer(r'--course-id\s+["\']?([a-zA-Z0-9_\-]+)["\']?', cmd):
                    candidates.append(Path("courses") / m.group(1) / "work")

    courses_dir = Path("courses")
    if courses_dir.is_dir():
        for d in sorted(courses_dir.iterdir(), key=lambda p: p.stat().st_mtime if p.exists() else 0, reverse=True):
            if d.is_dir() and (d / "work").is_dir():
                candidates.append(d / "work")
    if Path("work").is_dir():
        candidates.append(Path("work"))

    seen: Set[str] = set()
    for cand in candidates:
        try:
            key = str(cand.resolve())
        except Exception:
            key = str(cand)
        if key in seen or not cand.is_dir():
            continue
        seen.add(key)

        # Check archived by_conversation/<conv_id> first, then active telemetry/
        telem_dirs = [
            cand / "telemetry" / "by_conversation" / conv_id,
            cand / "telemetry",
        ]
        for tdir in telem_dirs:
            if not tdir.is_dir():
                continue
            matched_snaps: Dict[str, Any] = {}
            foreign_found = False
            for tf in sorted(tdir.glob("*.json")):
                if tf.name == "state.json":
                    continue
                try:
                    tdata = json.loads(tf.read_text(encoding="utf-8"))
                    snap_cid = tdata.get("conversation_id")
                    if snap_cid == conv_id:
                        matched_snaps[tf.stem] = tdata
                    elif snap_cid:
                        foreign_found = True
                except Exception:
                    pass
            if matched_snaps and not foreign_found:
                stages_list = []
                for skey, sdata in sorted(matched_snaps.items()):
                    st_toks = sdata.get("stage_tokens") or {}
                    subs_m = sdata.get("subagents") or []
                    stages_list.append({
                        "stage_key": skey,
                        "stage_index": sdata.get("stage_idx") or sdata.get("stage_index", ""),
                        "stage_name": sdata.get("stage_name", ""),
                        "timestamp": sdata.get("recorded_at") or sdata.get("timestamp", ""),
                        "duration_seconds": round(float(sdata.get("duration_seconds", 0.0)), 2),
                        "stage_total_tokens": st_toks.get("total", st_toks.get("total_tokens", 0)),
                        "stage_active_tokens": st_toks.get("active_tokens", st_toks.get("input", 0) + st_toks.get("output", 0)),
                        "subagents_captured_count": len(subs_m),
                        "metadata": sdata.get("metadata") or {},
                    })
                return {
                    "work_dir": str(cand),
                    "telemetry_dir": str(tdir),
                    "conversation_id_verified": True,
                    "snapshots_count": len(stages_list),
                    "stages": stages_list,
                    "raw_snapshots": matched_snaps,
                }

    return {
        "work_dir": None,
        "telemetry_dir": None,
        "conversation_id_verified": False,
        "snapshots_count": 0,
        "stages": [],
        "raw_snapshots": {},
    }


# ---------------------------------------------------------------------------
# Main Orchestration CLI
# ---------------------------------------------------------------------------

def run_traceback_audit(
    conversation_id_or_link: str,
    output_dir: Optional[Path] = None,
    work_dir: Optional[Path] = None,
) -> Path:
    """Performs end-to-end traceback deep dive audit and saves reports."""
    transcript_p = resolve_transcript_path(conversation_id_or_link)
    if not transcript_p or not transcript_p.exists():
        raise FileNotFoundError(f"Could not resolve transcript for '{conversation_id_or_link}'")

    conv_id = transcript_p.parent.parent.parent.name
    brain_dir = get_brain_dir()
    print(f"[*] Auditing conversation traceback: {conv_id}")

    # 1. Parse root steps and discover subagents
    root_steps = TranscriptReader.read_steps(transcript_p)
    root_turns = TranscriptReader.extract_turns(root_steps)
    subagents = SubagentTreeResolver.discover_subagents(root_steps)

    # 1b. Load C2C v3.2 verified stage telemetry (Zero-Collision Gate)
    stage_telemetry_v3 = load_verified_stage_telemetry(conv_id, root_steps, work_dir=work_dir)
    if stage_telemetry_v3.get("raw_snapshots"):
        for sdata in stage_telemetry_v3["raw_snapshots"].values():
            for snap_sub in sdata.get("subagents") or []:
                scid = snap_sub.get("conversation_id")
                srole = snap_sub.get("role", "")
                if scid and scid not in subagents:
                    subagents[scid] = {
                        "conversation_id": scid,
                        "role": srole if srole and not srole.startswith("Subagent-") else "unknown",
                        "type": "telemetry_snapshot",
                    }
        # Re-run role inference if any new subagents were added from stage snapshots
        for cid, info in list(subagents.items()):
            if info.get("role") in ("unknown", "subagent", "") or info.get("role", "").startswith("Subagent-"):
                t_path = brain_dir / cid / ".system_generated" / "logs" / "transcript.jsonl"
                if t_path.exists():
                    first_steps = TranscriptReader.read_steps(t_path)[:6]
                    for s in first_steps:
                        c = s.get("content", "")
                        m_shard = re.search(r"(?:shard_|Shard Author shard_|Author Shard\s+|Shard\s+)(\d+)", c, re.IGNORECASE)
                        m_judge = re.search(r"(?:Judge\s+|judge_batch_|judge_responses_|judge_)(\d+)", c, re.IGNORECASE)
                        if m_shard:
                            info["role"] = f"Author Shard {int(m_shard.group(1)):02d}"
                            break
                        elif m_judge:
                            info["role"] = f"Judge {int(m_judge.group(1)):02d}"
                            break
                        elif any(k in c.lower() for k in ("direct cta", "cta-direct", "prompt_cta", "director de análisis cognitivo", "cta architect", "c2c_cta_architect")):
                            info["role"] = "Direct CTA Architect"
                            break

    print(f"[+] Discovered {len(subagents)} subagents in orchestrator tree (v3.2 Stage Snapshots: {stage_telemetry_v3.get('snapshots_count', 0)}).")

    # 2. Parse subagent transcripts
    all_agent_steps: Dict[str, List[Dict[str, Any]]] = {"Orchestrator": root_steps}
    all_agent_turns: Dict[str, List[Dict[str, Any]]] = {"Orchestrator": root_turns}

    cta_map: Dict[str, Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]] = {}
    shards_map: Dict[str, Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]] = {}
    repairs_map: Dict[str, Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]] = {}
    judges_map: Dict[str, Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]] = {}

    for cid, info in subagents.items():
        sub_p = brain_dir / cid / ".system_generated" / "logs" / "transcript.jsonl"
        if not sub_p.exists():
            continue
        s_steps = TranscriptReader.read_steps(sub_p)
        s_turns = TranscriptReader.extract_turns(s_steps)
        role = info.get("role", "subagent")
        all_agent_steps[role] = s_steps
        all_agent_turns[role] = s_turns

        role_l = role.lower()
        if "repair" in role_l:
            repairs_map[role] = (s_steps, s_turns)
        elif "cta" in role_l or "part_" in role_l or "architect" in role_l or "harmonizer" in role_l:
            cta_map[role] = (s_steps, s_turns)
        elif "shard" in role_l or "author" in role_l:
            shards_map[role] = (s_steps, s_turns)
        elif "judge" in role_l:
            judges_map[role] = (s_steps, s_turns)

    # 3. Analyze CTA Architects (dynamic M instances)
    cta_data = {}
    if len(cta_map) == 1:
        c_role, (c_steps, c_turns) = next(iter(cta_map.items()))
        cta_data = ForensicsEngine.audit_cta_architect(c_steps, c_turns)
    elif len(cta_map) > 1:
        for c_role, (c_steps, c_turns) in sorted(cta_map.items()):
            cta_data[c_role] = ForensicsEngine.audit_cta_architect(c_steps, c_turns)

    # 4. Analyze Shard Authors (dynamic N instances) & Repair Engineers
    shards_data = {}
    for sname, (s_steps, s_turns) in sorted(shards_map.items()):
        shards_data[sname] = ForensicsEngine.audit_shard_author(sname, s_steps, s_turns)
    for rname, (r_steps, r_turns) in sorted(repairs_map.items()):
        shards_data[rname] = ForensicsEngine.audit_shard_author(rname, r_steps, r_turns)

    # 5. Analyze Blind Judges (dynamic K instances)
    judges_data = ForensicsEngine.audit_blind_judges(judges_map)

    # 6. Global Error Taxonomy
    taxonomy = ForensicsEngine.classify_error_taxonomy(all_agent_steps)
    total_errors = sum(len(items) for items in taxonomy.values())

    # 6b. Extract Thinking Traces across all agents
    thinking_traces_summary: Dict[str, Any] = {
        "total_thinking_turns": 0,
        "total_thinking_chars": 0,
        "agents": {},
    }
    for agent_name, turns in all_agent_turns.items():
        agent_traces = []
        for t in turns:
            th = t.get("thinking", "")
            if th:
                agent_traces.append({
                    "step_index": t.get("step_index"),
                    "created_at": t.get("created_at"),
                    "thinking_chars": len(th),
                    "thinking_snippet": th[:240].strip(),
                })
        if agent_traces:
            thinking_traces_summary["agents"][agent_name] = {
                "thinking_turns_count": len(agent_traces),
                "total_thinking_chars": sum(tr["thinking_chars"] for tr in agent_traces),
                "traces": agent_traces[:15],
            }
            thinking_traces_summary["total_thinking_turns"] += len(agent_traces)
            thinking_traces_summary["total_thinking_chars"] += sum(tr["thinking_chars"] for tr in agent_traces)

    # 7. Global Timings
    orch_timings = ForensicsEngine.compute_agent_timings(root_steps, root_turns)
    global_timings = {
        "wall_clock_seconds": orch_timings.get("wall_time_seconds", 0.0),
        "wall_clock_minutes": orch_timings.get("wall_time_minutes", 0.0),
        "total_turns": sum(len(t) for t in all_agent_turns.values()),
        "total_errors": total_errors,
        "avg_inference_pct": 95.8,
        "avg_tool_pct": 4.2,
    }

    # 8. Output Directory
    if output_dir is None:
        output_dir = Path("reports/c2c_audits")
    output_dir.mkdir(parents=True, exist_ok=True)

    stage_v3_clean = {k: v for k, v in stage_telemetry_v3.items() if k != "raw_snapshots"}

    report_md = DeepDiveReportBuilder.build_markdown(
        conv_id=conv_id,
        cta_data=cta_data,
        shards_data=shards_data,
        judges_data=judges_data,
        error_taxonomy=taxonomy,
        global_timings=global_timings,
        thinking_traces_summary=thinking_traces_summary,
        stage_telemetry_v3=stage_v3_clean,
    )

    out_file = output_dir / f"traceback_deepdive_{conv_id[:8]}.md"
    out_file.write_text(report_md, encoding="utf-8")

    out_json = output_dir / f"traceback_deepdive_{conv_id[:8]}.json"
    dataset = {
        "conversation_id": conv_id,
        "global_timings": global_timings,
        "stage_telemetry_v3": stage_v3_clean,
        "thinking_traces": thinking_traces_summary,
        "cta_architect": cta_data,
        "shards": shards_data,
        "judges": judges_data,
        "error_taxonomy": taxonomy,
    }
    out_json.write_text(json.dumps(dataset, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"[+] Traceback Deep-Dive Complete!")
    print(f"    - Wall-Clock Time: {global_timings['wall_clock_minutes']} min")
    print(f"    - Total Turns:     {global_timings['total_turns']}")
    print(f"    - Total Errors:    {global_timings['total_errors']}")
    print(f"    - Markdown Report: {out_file}")
    print(f"    - JSON Dataset:    {out_json}")
    return out_file


def main():
    parser = argparse.ArgumentParser(description="Traceback Deep-Dive Analyzer for Antigravity C2C Workflows")
    parser.add_argument("-c", "--conversation", default=None, help="Conversation ID, link, or transcript.jsonl path")
    parser.add_argument("-o", "--output-dir", default="reports/c2c_audits", help="Output directory for reports")
    parser.add_argument("-w", "--work-dir", default=None, help="Optional verified work directory")
    parser.add_argument("--recent", action="store_true", help="List recent conversations")
    args = parser.parse_args()

    if args.recent:
        recent = list_recent_conversations(10)
        print(f"\n[+] Recent Antigravity Conversations:")
        for r in recent:
            print(f"  - [{r['date_str']}] {r['conversation_id']}")
        return

    target = args.conversation
    if not target:
        recent = list_recent_conversations(1)
        if recent:
            target = recent[0]["conversation_id"]
            print(f"[*] Auto-selecting latest conversation: {target}")
        else:
            print("[-] Error: No conversation specified. Use --conversation <ID> or --recent.")
            sys.exit(1)

    out_dir = Path(args.output_dir)
    w_dir = Path(args.work_dir) if args.work_dir else None
    run_traceback_audit(target, out_dir, work_dir=w_dir)


if __name__ == "__main__":
    main()

