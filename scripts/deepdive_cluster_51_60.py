import json
import os
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

brain_dir = Path("C:/Users/augus/.gemini/antigravity/brain")
reports_dir = Path("reports/c2c_audits/20261026_002637_estadistica_3_pre_parcial_821334d0")

with open(reports_dir / "shard_timing_profile.json", "r", encoding="utf-8") as f:
    timing = json.load(f)

with open(reports_dir / "telemetry.json", "r", encoding="utf-8") as f:
    telem = json.load(f)

# Build subagents map
sa_map = {sa["shard_id"]: sa for sa in telem["subagents"] if sa.get("shard_id")}
time_map = {s["shard_id"]: s for s in timing["all_shards"]}

target_ids = [f"shard_{i:02d}" for i in range(51, 61)]

for sid in target_ids:
    s_time = time_map.get(sid, {})
    s_telem = sa_map.get(sid, {})
    cid = s_time.get("conversation_id")
    
    t_path = brain_dir / cid / ".system_generated" / "logs" / "transcript.jsonl"
    entries = []
    if t_path.exists():
        with open(t_path, "r", encoding="utf-8") as f:
            entries = [json.loads(line) for line in f if line.strip()]
            
    print(f"================================================================================")
    print(f"SHARD: {sid} | CID: {cid}")
    print(f"Wall Time: {s_time.get('wall_time_s')}s | Pre-1st: {s_time.get('pre_1st_compile_s')}s | Post-1st: {s_time.get('post_1st_compile_s')}s")
    print(f"Compiles: {s_time.get('compile_runs')} (Fails: {s_time.get('compile_fails')}) | Edits: {s_time.get('edits_count')} | Turns: {s_time.get('turns_count')}")
    print(f"Tokens: Active={s_telem.get('active_tokens'):,} (In={s_telem.get('input_tokens'):,}, Out={s_telem.get('output_tokens'):,}, Think={s_telem.get('thinking_tokens'):,}), CacheRead={s_telem.get('cache_read_tokens'):,}")
    print(f"Competencies: {s_telem.get('competencies')}")
    print(f"Tool Breakdown: {s_telem.get('tool_calls_by_name')}")
    print(f"Tool Errors: {s_telem.get('tool_errors_count')}")
    print(f"Failed Commands: {len(s_telem.get('failed_commands', []))}")
    for fc in s_telem.get('failed_commands', []):
        print(f"  Fail at step {fc.get('step_index')}: {fc.get('snippet', '').strip().replace(chr(10), ' | ')[:150]}")
        
    print(f"Transcript Entries: {len(entries)}")
    
    # Analyze tool sequence and timeline
    print("--- Tool Sequence & Key Events ---")
    first_compile_idx = None
    first_compile_ts = None
    for idx, e in enumerate(entries):
        ts = e.get("created_at")
        stype = e.get("type")
        status = e.get("status")
        tcs = e.get("tool_calls", [])
        content = str(e.get("content", ""))
        err = str(e.get("error", ""))
        
        # Check tool calls
        for tc in tcs:
            tname = tc.get("name")
            args = tc.get("args", {})
            arg_summary = ""
            if tname == "run_command":
                cmd = args.get("CommandLine", "")
                arg_summary = cmd[:80]
                if "compile_shard" in cmd and first_compile_idx is None:
                    first_compile_idx = idx
                    first_compile_ts = ts
            elif tname in ("view_file", "write_file", "edit_file"):
                arg_summary = Path(args.get("Path") or args.get("AbsolutePath", "")).name
                if tname == "edit_file":
                    arg_summary += f" (target len {len(args.get('Target', ''))})"
            elif tname == "send_message":
                arg_summary = f"Recipient={args.get('Recipient')[:8]} Msg={args.get('Message', '')[:40]}"
            print(f"  [{idx:02d}] {ts} TOOL CALL: {tname} -> {arg_summary}")
            
        if err:
            print(f"  [{idx:02d}] {ts} ERROR ({stype}/{status}): {err[:120]}")
        elif status == "ERROR":
            print(f"  [{idx:02d}] {ts} ERROR STATUS: {content[:120]}")
            
    print(f"First compile detected at step {first_compile_idx} ({first_compile_ts})")
