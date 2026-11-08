import json
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")

audit_dir = Path("reports/c2c_audits/20261108_033353_estadistica_3_s9_vmapreduce17_d637aaa6")
with open(audit_dir / "shard_timing_profile.json", "r", encoding="utf-8") as f:
    timing = json.load(f)

shards_map = {s["shard_id"]: s["conversation_id"] for s in timing["all_shards"]}

user_home = Path.home()

def analyze_one(sid, cid):
    t_file = user_home / ".gemini" / "antigravity" / "brain" / cid / ".system_generated" / "logs" / "transcript.jsonl"
    if not t_file.is_file():
        print(f"File not found: {t_file}")
        return
    lines = [json.loads(l) for l in t_file.read_text(encoding="utf-8", errors="ignore").splitlines() if l.strip()]
    
    events = []
    prev_dt = None
    for entry in lines:
        t_type = entry.get("type")
        dt_str = entry.get("created_at")
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00")) if dt_str else None
        elapsed = (dt - prev_dt).total_seconds() if (prev_dt and dt) else 0.0
        prev_dt = dt
        step_idx = entry.get("step_index")
        
        if t_type == "PLANNER_RESPONSE":
            calls = entry.get("tool_calls", [])
            call_info = []
            for c in calls:
                name = c.get("name")
                args = c.get("args", {})
                arg_summary = ""
                if name == "view_file":
                    arg_summary = Path(args.get("AbsolutePath", "")).name
                elif name == "write_file":
                    p = Path(args.get("Path", "")).name
                    chars_cnt = len(str(args.get("Content", "")))
                    arg_summary = f"{p} ({chars_cnt}c)"
                elif name == "edit_file":
                    p = Path(args.get("Path", "")).name
                    arg_summary = f"{p}"
                elif name == "run_command":
                    arg_summary = "compile_shard"
                elif name == "send_message":
                    arg_summary = "msg"
                else:
                    arg_summary = str(list(args.keys()))
                call_info.append(f"{name}({arg_summary})")
            events.append(f"  Step {step_idx:2d} (+{elapsed:5.1f}s) MODEL -> [{', '.join(call_info)}]")
        elif t_type in ("GENERIC", "ERROR_MESSAGE"):
            content = entry.get("content", "")
            err = entry.get("error", "")
            if err:
                events.append(f"  Step {step_idx:2d} (+{elapsed:5.1f}s) TOOL  -> [ERR] {str(err)[:100]}")
            elif "Command exited with code 1" in str(content):
                fail_l = [cl.strip() for cl in str(content).splitlines() if cl.strip().startswith(("FAIL:", "[-] FAIL:", "[-] [", "SyntaxError", "Traceback"))]
                summary = fail_l[0][:100] if fail_l else "Exit Code 1"
                events.append(f"  Step {step_idx:2d} (+{elapsed:5.1f}s) TOOL  -> [FAIL] {summary}")
            elif "denied by pre-tool hook" in str(content):
                events.append(f"  Step {step_idx:2d} (+{elapsed:5.1f}s) TOOL  -> [DENIED] {str(content)[:100]}")
            else:
                events.append(f"  Step {step_idx:2d} (+{elapsed:5.1f}s) TOOL  -> [OK]")
                
    print(f"\n{'='*80}\nSHARD: {sid} (CID: {cid})\n{'='*80}")
    for e in events:
        print(e)

for s in ["shard_20", "shard_16", "shard_26", "shard_25", "shard_21"]:
    analyze_one(s, shards_map.get(s, ""))

