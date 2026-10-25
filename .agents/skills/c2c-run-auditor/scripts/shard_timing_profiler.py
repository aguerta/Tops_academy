#!/usr/bin/env python3
"""
shard_timing_profiler.py - Forensic Multi-Shard Timing & Bottleneck Profiler for C2C.

Decomposes shard author latencies into Pre-1st-Compile and Post-1st-Compile,
extracts error taxonomies per shard, identifies Gold Standard reference shards,
and pinpoints stragglers and remediation loops.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def parse_iso(ts: Optional[str]) -> Optional[datetime]:
    if not ts:
        return None
    try:
        ts_clean = str(ts).strip().replace("Z", "+00:00")
        return datetime.fromisoformat(ts_clean)
    except Exception:
        return None


def get_brain_dir() -> Path:
    override = os.environ.get("GEMINI_BRAIN_DIR") or os.environ.get("ANTIGRAVITY_BRAIN_DIR")
    if override and Path(override).exists():
        return Path(override)
    user_home = Path.home()
    candidates = [
        user_home / ".gemini" / "antigravity" / "brain",
        user_home / ".antigravity" / "brain",
    ]
    for c in candidates:
        if c.exists():
            return c
    return candidates[0]


def profile_conversation_shards(conv_id: str, run_dir: Optional[Path] = None) -> Dict[str, Any]:
    brain_dir = get_brain_dir()
    
    # 1. Locate audit run directory if not given
    if not run_dir:
        reports_dir = Path("reports/c2c_audits")
        candidates = sorted(reports_dir.glob(f"*_{conv_id[:8]}"), reverse=True)
        if candidates:
            run_dir = candidates[0]
        else:
            raise FileNotFoundError(f"No audit directory found for conversation {conv_id} under {reports_dir}")

    tel_path = run_dir / "telemetry.json"
    if not tel_path.exists():
        raise FileNotFoundError(f"telemetry.json not found in {run_dir}")

    with open(tel_path, "r", encoding="utf-8") as f:
        tel = json.load(f)

    stg3 = tel.get("stage_deep_dives", {}).get("stage_3_authors", {})
    shards_meta = stg3.get("shards", [])
    
    # Also read traceback deepdive if present
    tb_path = None
    for cand in run_dir.glob("traceback_deepdive_*.json"):
        tb_path = cand
        break
    tb_data = {}
    if tb_path and tb_path.exists():
        try:
            with open(tb_path, "r", encoding="utf-8") as f:
                tb_data = json.load(f)
        except Exception:
            pass
    tb_shards = tb_data.get("shards", {})

    results: List[Dict[str, Any]] = []

    for s in shards_meta:
        cid = s.get("conversation_id")
        label = s.get("label", "Unknown")
        shard_id = s.get("shard_id") or label
        wall_time = float(s.get("duration_seconds", 0.0))
        spawn_time = parse_iso(s.get("spawn_time") or s.get("start_time"))
        end_time = parse_iso(s.get("end_time"))
        
        t_path = brain_dir / cid / ".system_generated" / "logs" / "transcript.jsonl"
        
        first_compile_time = None
        compile_runs = 0
        compile_fails = 0
        error_snippets: List[str] = []
        error_codes: List[str] = []
        tool_counts: Dict[str, int] = {}
        first_thinking_snippet = ""
        cross_course_explorations: List[str] = []

        if t_path.exists():
            try:
                with open(t_path, "r", encoding="utf-8", errors="ignore") as tf:
                    for line_idx, line in enumerate(tf):
                        if not line.strip():
                            continue
                        rec = json.loads(line)
                        created_at = parse_iso(rec.get("created_at"))
                        
                        # Inspect thinking in turn 0/1
                        if line_idx <= 2 and not first_thinking_snippet:
                            th = rec.get("thinking", "")
                            if th:
                                first_thinking_snippet = th[:250].replace("\n", " ")

                        # Tool calls
                        for tc in rec.get("tool_calls", []):
                            tc_name = tc.get("name") or tc.get("function", {}).get("name", "")
                            tool_counts[tc_name] = tool_counts.get(tc_name, 0) + 1
                            args = tc.get("args") or tc.get("function", {}).get("arguments", {})
                            if isinstance(args, str):
                                try: args = json.loads(args)
                                except Exception: args = {}
                            
                            cmd = args.get("CommandLine", "") if isinstance(args, dict) else ""
                            if "compile_shard" in cmd or "compile" in cmd:
                                compile_runs += 1
                                if first_compile_time is None and created_at:
                                    first_compile_time = created_at
                            
                            # Check forbidden cross-course exploration
                            if "courses/" in cmd and "work/" in cmd:
                                m_c = re.findall(r"courses[/\\]([a-zA-Z0-9_\-]+)", cmd)
                                for c_name in m_c:
                                    if tel.get("meta", {}).get("course_id") and c_name != tel["meta"]["course_id"]:
                                        cross_course_explorations.append(c_name)

                        # Check failures in tool output
                        content = rec.get("content", "")
                        if "Command exited with code" in content and "code 0" not in content:
                            compile_fails += 1
                            # Extract error code or trace
                            for code_pat in [r"\[R-\d+\]", r"\[TPL-[A-Z]+\]", r"\[GATEKEEPER\]", r"SyntaxError[^\n]+", r"NameError[^\n]+", r"ValueError[^\n]+", r"ZeroDivisionError[^\n]+"]:
                                found = re.findall(code_pat, content)
                                for f_code in found:
                                    if f_code not in error_codes:
                                        error_codes.append(f_code)
                            # First non-empty lines of traceback
                            lines = [ln.strip() for ln in content.splitlines() if ln.strip() and not ln.startswith("Created At") and not ln.startswith("Completed At") and not ln.startswith("Command exited")]
                            if lines:
                                error_snippets.append(lines[-1][:100])
            except Exception as e:
                pass

        # Compute Pre and Post compile durations
        if first_compile_time and spawn_time:
            pre_compile_s = max(0.0, round((first_compile_time - spawn_time).total_seconds(), 1))
        else:
            pre_compile_s = round(wall_time * 0.7, 1) if compile_runs == 0 else 0.0

        if first_compile_time and end_time:
            post_compile_s = max(0.0, round((end_time - first_compile_time).total_seconds(), 1))
        else:
            post_compile_s = max(0.0, round(wall_time - pre_compile_s, 1))

        # Check traceback deepdive data for this shard
        tb_shard_info = tb_shards.get(label) or tb_shards.get(f"Author {shard_id}") or {}
        check_runs_total = tb_shard_info.get("check_runs_total", compile_runs)
        check_runs_failed = tb_shard_info.get("check_runs_failed", compile_fails)
        has_micro_loop = tb_shard_info.get("has_micro_loop", False)
        micro_loop_reason = tb_shard_info.get("micro_loop_reason", "")
        edits_count = tb_shard_info.get("edits_count", tool_counts.get("edit_file", 0))

        results.append({
            "shard_id": shard_id,
            "label": label,
            "conversation_id": cid,
            "wall_time_s": wall_time,
            "pre_1st_compile_s": pre_compile_s,
            "post_1st_compile_s": post_compile_s,
            "compile_runs": max(compile_runs, check_runs_total),
            "compile_fails": max(compile_fails, check_runs_failed),
            "edits_count": edits_count,
            "turns_count": s.get("turns_count", 0),
            "active_tokens": s.get("active_tokens", 0),
            "thinking_tokens": s.get("thinking_tokens", 0),
            "competencies_count": s.get("competencies_count", 0),
            "error_codes": error_codes,
            "error_snippets": error_snippets[:3],
            "has_micro_loop": has_micro_loop,
            "micro_loop_reason": micro_loop_reason,
            "cross_course_explorations": list(set(cross_course_explorations)),
            "first_thinking_snippet": first_thinking_snippet,
        })

    # Sort by wall_time descending
    results.sort(key=lambda x: x["wall_time_s"], reverse=True)
    
    # Identify Gold Standard Clean-Room:
    # 1 compile run, 0 compile fails, 0 edits post creation, lowest wall time
    cleanroom_candidates = [
        r for r in results 
        if r["compile_fails"] == 0 and r["compile_runs"] >= 1 and r["edits_count"] == 0
    ]
    gold_standard = min(cleanroom_candidates, key=lambda x: x["wall_time_s"]) if cleanroom_candidates else (min(results, key=lambda x: x["wall_time_s"]) if results else None)

    # Median wall time
    durations = [r["wall_time_s"] for r in results]
    median_dur = sorted(durations)[len(durations)//2] if durations else 0.0

    output = {
        "course_id": tel.get("meta", {}).get("course_id", "unknown"),
        "conversation_id": conv_id,
        "run_dir": str(run_dir),
        "total_shards": len(results),
        "median_wall_time_s": median_dur,
        "gold_standard_cleanroom": gold_standard,
        "top_5_stragglers": results[:5],
        "top_5_fastest": sorted(results, key=lambda x: x["wall_time_s"])[:5],
        "all_shards": results,
    }

    # Save to run_dir/shard_timing_profile.json
    out_json = run_dir / "shard_timing_profile.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    return output


def generate_markdown_table(profile: Dict[str, Any]) -> str:
    shards = profile.get("all_shards", [])
    gold = profile.get("gold_standard_cleanroom", {})
    gold_label = gold.get("label", "N/A") if gold else "N/A"
    gold_wall = gold.get("wall_time_s", 0.0) if gold else 0.0

    lines = []
    lines.append(f"### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)")
    lines.append(f"- **Total Shards Auditados:** `{profile.get('total_shards')}` | **Mediana de Pared:** `{profile.get('median_wall_time_s')}s`")
    lines.append(f"- **Gold Standard Clean-Room:** `{gold_label}` (`{gold_wall}s`, 0 fallos, 0 ediciones post-escritura)")
    lines.append("")
    lines.append("| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |")
    lines.append("| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |")

    for s in profile.get("all_shards", []):
        errs = ", ".join(s["error_codes"][:3]) if s["error_codes"] else "0 errores"
        diag = []
        if s["pre_1st_compile_s"] > 240.0:
            diag.append("Overthinking / Exploración lenta Pre-Compile")
        if s["compile_fails"] > 0:
            diag.append(f"Remediación ({s['compile_fails']} fallos)")
        if s["has_micro_loop"]:
            diag.append(f"Micro-bucle: {s['micro_loop_reason']}")
        if s["cross_course_explorations"]:
            diag.append(f"Exploración cross-course: {s['cross_course_explorations']}")
        if not diag:
            diag.append("Ejecución fluida (Pase limpio)")

        diag_str = "; ".join(diag)
        lines.append(f"| **{s['label']}** | `{s['wall_time_s']}s` | `{s['pre_1st_compile_s']}s` | `{s['post_1st_compile_s']}s` | `{s['compile_runs']} ({s['compile_fails']})` | `{s['edits_count']}` | `{errs}` | {diag_str} |")

    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Profile multi-shard timings for C2C conversation.")
    parser.add_argument("-c", "--conversation", required=True, help="Conversation UUID or prefix")
    parser.add_argument("-r", "--run-dir", default=None, help="Optional run directory path")
    args = parser.parse_args()

    rdir = Path(args.run_dir) if args.run_dir else None
    prof = profile_conversation_shards(args.conversation, rdir)
    print(f"[+] Shard profiling completed for {prof['course_id']} ({prof['total_shards']} shards)!")
    print(f"    - Median Wall Time: {prof['median_wall_time_s']}s")
    if prof.get('gold_standard_cleanroom'):
        g = prof['gold_standard_cleanroom']
        print(f"    - Gold Standard Clean-Room: {g['label']} ({g['wall_time_s']}s, {g['compile_runs']} compiles, {g['compile_fails']} fails)")
    print(f"    - Top Straggler: {prof['top_5_stragglers'][0]['label']} ({prof['top_5_stragglers'][0]['wall_time_s']}s)")
    
    # Save md snippet
    run_dir = Path(prof["run_dir"])
    md_table = generate_markdown_table(prof)
    with open(run_dir / "shard_timing_decomposition.md", "w", encoding="utf-8") as f:
        f.write(md_table)
    print(f"[+] Markdown table saved to {run_dir / 'shard_timing_decomposition.md'}")
