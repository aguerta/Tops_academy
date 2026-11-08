import json
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")

shards_map = {
    "shard_14": "68945e20-1ec1-420b-b326-9f3e96f5372d",
    "shard_03": "1122dea8-a345-48b0-9c4a-b8ac1cdc8fd1",
    "shard_01": "d2181ae1-9ad3-4a61-aade-8121a87fdb7f",
    "shard_18": "0d39880e-5419-46ae-b5de-22deed85e04a",
    "shard_24": "3c391d6c-d29e-4c58-b81d-c6701a4edeb4",
    "shard_07": "2f10c44f-b3ce-47dd-88aa-ca1389724dfa",
    "shard_29": "f7ecc3f9-2431-4142-9ab4-2c83f35b910f",
    "shard_16": "d2e5a4f7-111d-44a7-897b-9195b6c20530",
    "shard_26": "bbfeebfc-b3b0-4663-88bc-39be9bdaaa2f",
    "shard_20": "c9945df8-5ca8-4721-a4b0-379e498c0b52",
    "shard_21": "5e55e5fa-4c4f-4d64-9be1-08ec5d115e4f",
    "shard_25": "a3122c95-da25-4c6e-8519-75a7dfab06e7"
}

user_home = Path.home()

def analyze_shard_transcript(sid, cid):
    t_file = user_home / ".gemini" / "antigravity" / "brain" / cid / ".system_generated" / "logs" / "transcript.jsonl"
    if not t_file.is_file():
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
                    lines_cnt = len(str(args.get("Content", "")).splitlines())
                    chars_cnt = len(str(args.get("Content", "")))
                    arg_summary = f"{p} ({lines_cnt} lines, {chars_cnt} chars)"
                elif name == "edit_file":
                    p = Path(args.get("Path", "")).name
                    t_len = len(str(args.get("Target", "")))
                    r_len = len(str(args.get("Replacement", "")))
                    arg_summary = f"{p} (target: {t_len}c, rep: {r_len}c)"
                elif name == "run_command":
                    cmd = args.get("CommandLine", "")
                    if "compile_shard.py" in cmd:
                        arg_summary = "compile_shard"
                    else:
                        arg_summary = cmd[:50]
                elif name == "send_message":
                    arg_summary = f"msg to {args.get('Recipient')}"
                else:
                    arg_summary = str(list(args.keys()))
                call_info.append(f"{name}({arg_summary})")
            
            in_tok = entry.get("input_tokens", 0)
            out_tok = entry.get("output_tokens", 0)
            events.append({
                "step": step_idx,
                "elapsed": elapsed,
                "type": "MODEL",
                "calls": call_info,
                "in_tok": in_tok,
                "out_tok": out_tok
            })
            
        elif t_type in ("GENERIC", "ERROR_MESSAGE"):
            content = entry.get("content", "")
            err = entry.get("error", "")
            status = "OK"
            summary = ""
            if err:
                status = "ERR"
                summary = str(err)[:120]
            elif "Command exited with code 1" in str(content):
                status = "FAIL"
                lines_c = str(content).splitlines()
                # find fail line
                for cl in lines_c:
                    if cl.startswith("FAIL:") or cl.startswith("[-] FAIL:") or cl.startswith("[-] ["):
                        summary = cl[:120]
                        break
                if not summary:
                    summary = lines_c[-1][:120] if lines_c else "exit code 1"
            elif "denied by pre-tool hook" in str(content):
                status = "DENIED"
                summary = str(content)[:120]
            elif t_type == "ERROR_MESSAGE":
                status = "SYS_ERR"
                summary = str(entry)[:120]
            else:
                summary = "OK (" + str(content)[:50].strip().replace("\n", " ") + ")"
                
            events.append({
                "step": step_idx,
                "elapsed": elapsed,
                "type": "TOOL_RESULT",
                "status": status,
                "summary": summary
            })

    print(f"\n{'='*100}")
    print(f"SHARD SUMMARY: {sid} (CID: {cid})")
    print(f"{'='*100}")
    for ev in events:
        if ev["type"] == "MODEL":
            c_str = ", ".join(ev["calls"])
            print(f"  Step {ev['step']:2d} (+{ev['elapsed']:5.1f}s) MODEL -> calls: [{c_str}] | in: {ev['in_tok']} | out: {ev['out_tok']}")
        else:
            print(f"  Step {ev['step']:2d} (+{ev['elapsed']:5.1f}s) TOOL  -> [{ev['status']}] {ev['summary']}")

for sid in ["shard_14", "shard_03", "shard_01", "shard_18", "shard_24", "shard_07", "shard_20", "shard_16", "shard_26"]:
    analyze_shard_transcript(sid, shards_map[sid])
