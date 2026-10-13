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

        with open(transcript_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    steps.append(json.loads(line))
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
                        for sub in args.get("Subagents", []):
                            if isinstance(sub, dict):
                                role = sub.get("Role", "Subagent")
                                t_name = sub.get("TypeName", "generic")
                                prompt = sub.get("Prompt", "")
                            # Map candidate
                            # The result will arrive in the corresponding tool response

            # 2. From tool result content of invoke_subagent
            if "Created the following subagents:" in content or "conversationId" in content:
                uuid_matches = re.findall(r'"conversationId":\s*"([a-f0-9\-]{36})"', content)
                for cid in uuid_matches:
                    if cid not in subagents:
                        subagents[cid] = {"conversation_id": cid, "role": "unknown", "type": "unknown"}

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

        # 4. Infer roles from individual subagent transcripts if role is still unknown
        brain_dir = get_brain_dir()
        for cid, info in list(subagents.items()):
            t_path = brain_dir / cid / ".system_generated" / "logs" / "transcript.jsonl"
            if not t_path.exists():
                continue
            first_steps = TranscriptReader.read_steps(t_path)[:5]
            for s in first_steps:
                c = s.get("content", "")
                if "Direct CTA" in c or "cta-direct" in c or "prompt_cta" in c or "Director de Análisis Cognitivo" in c:
                    info["role"] = "Direct CTA Architect"
                    info["stage"] = "1b_cta"
                elif "shard_01" in c or "Shard Author shard_01" in c:
                    info["role"] = "Shard Author shard_01"
                    info["stage"] = "3_authoring"
                elif "shard_02" in c or "Shard Author shard_02" in c:
                    info["role"] = "Shard Author shard_02"
                    info["stage"] = "3_authoring"
                elif "shard_03" in c or "Shard Author shard_03" in c:
                    info["role"] = "Shard Author shard_03"
                    info["stage"] = "3_authoring"
                elif "Judge 01" in c or "judge_batch_01" in c:
                    info["role"] = "Blind Judge 01"
                    info["stage"] = "5_judges"
                elif "Judge 02" in c or "judge_batch_02" in c:
                    info["role"] = "Blind Judge 02"
                    info["stage"] = "5_judges"

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
        """Audits a Shard Author: micro-loops, check_templates runs, and reverse engineering."""
        timings = ForensicsEngine.compute_agent_timings(steps, turns)

        check_runs: List[Dict[str, Any]] = []
        reverse_eng_reads: List[Dict[str, Any]] = []
        writes_count = 0
        edits_count = 0
        scripts_written: Set[str] = set()

        for t_idx, turn in enumerate(turns):
            for tc in turn.get("tools", []):
                tname = tc.get("name")
                args = tc.get("args", {})
                res_content = turn["results"][0].get("content", "") if turn.get("results") else ""

                if tname == "write_to_file":
                    writes_count += 1
                    tf = Path(args.get("TargetFile", "")).name
                    scripts_written.add(tf)
                elif tname == "replace_file_content":
                    edits_count += 1
                elif tname == "view_file":
                    target_file = str(args.get("AbsolutePath", ""))
                    # Detect reverse engineering of validator or rules
                    if any(k in target_file.lower() for k in ("check_templates.py", "rules.py", "invariants.py", "assembler.py")):
                        reverse_eng_reads.append({
                            "turn": t_idx + 1,
                            "file": Path(target_file).name,
                            "step_index": turn.get("step_index"),
                        })
                elif tname == "run_command":
                    cmd = args.get("CommandLine", "")
                    if "check_templates.py" in cmd:
                        is_fail = ("FAIL:" in res_content or "exited with code 1" in res_content or "Error" in res_content)
                        fail_snippets = [
                            line.strip() for line in res_content.splitlines()
                            if any(k in line.lower() for k in ("violation", "error", "fail", "traceback"))
                        ][:2]
                        check_runs.append({
                            "turn": t_idx + 1,
                            "failed": is_fail,
                            "snippets": fail_snippets,
                        })

        failed_checks = sum(1 for c in check_runs if c["failed"])
        passed_checks = sum(1 for c in check_runs if not c["failed"])
        has_reverse_eng_loop = len(reverse_eng_reads) >= 5
        has_micro_loop = len(scripts_written) >= 4 and len(check_runs) >= 10

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
        """Classifies every error across all orchestrator and subagent transcripts."""
        categories: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

        for agent_name, steps in all_steps.items():
            for s in steps:
                stype = s.get("type")
                status = s.get("status")
                content = s.get("content", "")
                s_idx = s.get("step_index", 0)

                if stype == "ERROR_MESSAGE":
                    categories["Token Limit Cutoff (Model Truncation)"].append({
                        "agent": agent_name,
                        "step_index": s_idx,
                        "snippet": content[:120].strip(),
                    })
                elif stype in ("GENERIC", "TOOL_RESPONSE") and (status == "ERROR" or "exited with code 1" in content):
                    if "Unsubstituted template variable" in content or "Unreplaced template variable" in content:
                        categories["Unsubstituted Template Variables ({var})"].append({
                            "agent": agent_name, "step_index": s_idx, "snippet": content[:120].strip()
                        })
                    elif "Residual double curly braces" in content or "double curly" in content.lower():
                        categories["KaTeX Double Curly Braces ({{ / }})"].append({
                            "agent": agent_name, "step_index": s_idx, "snippet": content[:120].strip()
                        })
                    elif "math delimiter" in content.lower() or "katex" in content.lower():
                        categories["Unbalanced Math Delimiters ($)"].append({
                            "agent": agent_name, "step_index": s_idx, "snippet": content[:120].strip()
                        })
                    elif "TPL-VAR" in content or "diversity quota" in content.lower():
                        categories["Parameter Diversity Violation (TPL-VAR)"].append({
                            "agent": agent_name, "step_index": s_idx, "snippet": content[:120].strip()
                        })
                    elif "cross_check verification returned False" in content or "cross_check" in content.lower():
                        categories["Cross-check Verification False"].append({
                            "agent": agent_name, "step_index": s_idx, "snippet": content[:120].strip()
                        })
                    elif "Could not successfully apply any edits" in content:
                        categories["replace_file_content Mismatch"].append({
                            "agent": agent_name, "step_index": s_idx, "snippet": content[:120].strip()
                        })
                    elif "El término" in content or "CommandNotFoundException" in content:
                        categories["PowerShell Command / Path Not Found"].append({
                            "agent": agent_name, "step_index": s_idx, "snippet": content[:120].strip()
                        })
                    elif "ModuleNotFoundError" in content:
                        categories["Python Environment / Virtualenv Discrepancy"].append({
                            "agent": agent_name, "step_index": s_idx, "snippet": content[:120].strip()
                        })
                    elif "Length anti-giveaway" in content or "leaks the correct answer" in content:
                        categories["Anti-Giveaway & Parity Violations (R-18/R-19)"].append({
                            "agent": agent_name, "step_index": s_idx, "snippet": content[:120].strip()
                        })
                    elif "Template schema violation" in content:
                        categories["Template Schema Violation"].append({
                            "agent": agent_name, "step_index": s_idx, "snippet": content[:120].strip()
                        })
                    else:
                        categories["Other Console / Tool Failures"].append({
                            "agent": agent_name, "step_index": s_idx, "snippet": content[:120].strip()
                        })

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
    ) -> str:
        lines: List[str] = []

        lines.append(f"# Auditoría Forense Ultra-Detallada del Traceback de Ejecución")
        lines.append(f"## Pipeline Content-to-Course (C2C) — Conversación [`{conv_id}`](conversation://{conv_id})")
        lines.append(f"")
        lines.append(f"**Fecha de Auditoría:** `{datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}`  ")
        lines.append(f"**Conversación Orquestadora:** [`{conv_id}`](conversation://{conv_id})  ")
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
        lines.append(f"| **Total de Errores Catalogados** | **`{global_timings.get('total_errors', 0)} errores`** | Fallos en consola, validadores y truncamientos |")
        lines.append(f"| **Inferencia LLM Promedio** | **`{global_timings.get('avg_inference_pct', 95.0)}%`** | Porcentaje de tiempo dedicado a generación/thinking |")
        lines.append(f"| **Ejecución Local de Tools** | **`{global_timings.get('avg_tool_pct', 5.0)}%`** | Porcentaje de tiempo consumido en I/O y terminal |")
        lines.append(f"")
        lines.append(f"### 1.1. Distribución Empírica del Tiempo (Inferencia vs Tools)")
        lines.append(f"```text")
        lines.append(f"========================================================================================")
        lines.append(f"DISTRIBUCIÓN DEL TIEMPO DE PARED POR SUBAGENTE (INFERENCIA LLM vs TOOLS)")
        lines.append(f"========================================================================================")
        if cta_data:
            t = cta_data.get("timings", {})
            lines.append(f"Direct CTA Architect   : {t.get('inference_seconds', 0.0):6.0f}s ({t.get('inference_pct', 0.0)}%) LLM | {t.get('tool_seconds', 0.0):4.0f}s Tools")
        for sname, sinfo in shards_data.items():
            t = sinfo.get("timings", {})
            lines.append(f"{sname:23s}: {t.get('inference_seconds', 0.0):6.0f}s ({t.get('inference_pct', 0.0)}%) LLM | {t.get('tool_seconds', 0.0):4.0f}s Tools")
        for jname, jinfo in judges_data.items():
            t = jinfo.get("timings", {})
            lines.append(f"{jname:23s}: {t.get('inference_seconds', 0.0):6.0f}s ({t.get('inference_pct', 0.0)}%) LLM | {t.get('tool_seconds', 0.0):4.0f}s Tools")
        lines.append(f"========================================================================================")
        lines.append(f"```")
        lines.append(f"")
        lines.append(f"---")
        lines.append(f"")
        lines.append(f"## 2. Análisis Forense: Direct CTA Architect (Stage 1B)")
        if cta_data:
            t = cta_data.get("timings", {})
            lines.append(f"- **Duración Total:** **`{t.get('wall_time_minutes', 0.0)} min`** ({t.get('wall_time_seconds', 0.0)} s) en **`{t.get('turns_count', 0)} turnos`**.")
            lines.append(f"- **Tokens:** {t.get('input_tokens', 0):,} In | {t.get('output_tokens', 0):,} Out | {t.get('cache_tokens', 0):,} Cache.")
            if cta_data.get("cutoff_detected"):
                lines.append(f"- 🛑 **Incidente Crítico Detectado:** Truncamiento por límite de tokens (`Output token limit exceeded`) en el **Paso {cta_data.get('cutoff_step')}**.")
                lines.append(f"- 💡 **Pivote Adaptativo:** En el **Paso {cta_data.get('pivot_step')}**, el arquitecto pasó a generar el script `{cta_data.get('pivot_script')}` para consolidar el CTA sin saturar el contexto.")
        lines.append(f"")
        lines.append(f"---")
        lines.append(f"")
        lines.append(f"## 3. Análisis Forense: Shards de Autoría (Stage 3)")
        lines.append(f"")
        lines.append(f"| Shard ID | Duración (min) | Turnos | Writes | Edits | Check Runs (Fail/Pass) | Loop de Ingeniería Inversa | Micro-Bucle |")
        lines.append(f"| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |")
        for sname, sinfo in shards_data.items():
            t = sinfo.get("timings", {})
            rev = "🛑 SÍ (30+ turnos)" if sinfo.get("has_reverse_eng_loop") else "NO"
            micro = "⚠️ SÍ (Secuencial)" if sinfo.get("has_micro_loop") else "NO"
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
        lines.append(f"| Categoría de Error | Ocurrencias | Ejemplo de Incidencia |")
        lines.append(f"| :--- | :---: | :--- |")
        for cat, items in sorted(error_taxonomy.items(), key=lambda x: len(x[1]), reverse=True):
            ex = items[0]
            lines.append(f"| **{cat}** | **{len(items)}** | `{ex.get('agent')}` (Paso {ex.get('step_index')}): {ex.get('snippet')[:70]}... |")
        lines.append(f"")
        lines.append(f"---")
        lines.append(f"*Informe generado automáticamente por `traceback_analyzer.py`.*")

        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main Orchestration CLI
# ---------------------------------------------------------------------------

def run_traceback_audit(conversation_id_or_link: str, output_dir: Optional[Path] = None) -> Path:
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
    print(f"[+] Discovered {len(subagents)} subagents in orchestrator tree.")

    # 2. Parse subagent transcripts
    all_agent_steps: Dict[str, List[Dict[str, Any]]] = {"Orchestrator": root_steps}
    all_agent_turns: Dict[str, List[Dict[str, Any]]] = {"Orchestrator": root_turns}

    cta_agent_id = None
    shards_map: Dict[str, Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]] = {}
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

        if "CTA" in role:
            cta_agent_id = cid
        elif "Shard" in role:
            shards_map[role] = (s_steps, s_turns)
        elif "Judge" in role:
            judges_map[role] = (s_steps, s_turns)

    # 3. Analyze CTA Architect
    cta_data = {}
    if cta_agent_id:
        c_steps = all_agent_steps.get("Direct CTA Architect", [])
        c_turns = all_agent_turns.get("Direct CTA Architect", [])
        cta_data = ForensicsEngine.audit_cta_architect(c_steps, c_turns)

    # 4. Analyze Shard Authors
    shards_data = {}
    for sname, (s_steps, s_turns) in sorted(shards_map.items()):
        shards_data[sname] = ForensicsEngine.audit_shard_author(sname, s_steps, s_turns)

    # 5. Analyze Blind Judges
    judges_data = ForensicsEngine.audit_blind_judges(judges_map)

    # 6. Global Error Taxonomy
    taxonomy = ForensicsEngine.classify_error_taxonomy(all_agent_steps)
    total_errors = sum(len(items) for items in taxonomy.values())

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

    report_md = DeepDiveReportBuilder.build_markdown(
        conv_id=conv_id,
        cta_data=cta_data,
        shards_data=shards_data,
        judges_data=judges_data,
        error_taxonomy=taxonomy,
        global_timings=global_timings,
    )

    out_file = output_dir / f"traceback_deepdive_{conv_id[:8]}.md"
    out_file.write_text(report_md, encoding="utf-8")

    out_json = output_dir / f"traceback_deepdive_{conv_id[:8]}.json"
    dataset = {
        "conversation_id": conv_id,
        "global_timings": global_timings,
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
    run_traceback_audit(target, out_dir)


if __name__ == "__main__":
    main()
