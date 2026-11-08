import json
from datetime import datetime

audit_dir = "reports/c2c_audits/20261108_033353_estadistica_3_s9_vmapreduce17_d637aaa6"

with open(f"{audit_dir}/telemetry.json", "r", encoding="utf-8") as f:
    telem = json.load(f)

with open(f"{audit_dir}/shard_timing_profile.json", "r", encoding="utf-8") as f:
    timing = json.load(f)

timing_by_shard = {s["shard_id"]: s for s in timing["all_shards"]}

results = []
for s in telem["subagents"]:
    label = s.get("label", "")
    if "Shard" not in label:
        continue
    shard_id = s.get("shard_id")
    steps = s.get("steps", [])
    
    first_write = None
    first_compile = None
    tools_before_write = []
    
    prev_dt = None
    step_times = []
    for st in steps:
        dt_str = st.get("created_at")
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00")) if dt_str else None
        elapsed = (dt - prev_dt).total_seconds() if (prev_dt and dt) else 0.0
        prev_dt = dt
        st_data = dict(st)
        st_data["elapsed"] = elapsed
        step_times.append(st_data)
        
        tools = st.get("tools", [])
        if not first_write:
            if "write_file" in tools:
                first_write = st_data
            else:
                tools_before_write.extend(tools)
        elif not first_compile:
            if "run_command" in tools:
                first_compile = st_data

    # The time taken to generate first_write is the elapsed time until the next step!
    first_write_duration = 0.0
    if first_write:
        fw_idx = step_times.index(first_write)
        if fw_idx + 1 < len(step_times):
            first_write_duration = step_times[fw_idx + 1]["elapsed"]
    
    t_prof = timing_by_shard.get(shard_id, {})
    results.append({
        "shard_id": shard_id,
        "pre_compile_s": t_prof.get("pre_1st_compile_s"),
        "tools_before_write": tools_before_write,
        "write_tokens": first_write.get("output_tokens") if first_write else 0,
        "write_duration_s": first_write_duration,
        "tok_per_sec": (first_write.get("output_tokens", 0) / first_write_duration) if first_write_duration > 0 else 0,
        "total_wall_s": s.get("duration_seconds")
    })

results.sort(key=lambda x: x["shard_id"])
print(f"{'Shard':<10} | {'PreComp(s)':<10} | {'ToolsBeforeWrite':<18} | {'WriteTokens':<12} | {'WriteDur(s)':<12} | {'Tok/Sec':<8}")
print("-" * 80)
for r in results:
    tbw = ",".join(r["tools_before_write"]) if r["tools_before_write"] else "none"
    print(f"{r['shard_id']:<10} | {r['pre_compile_s']:<10.1f} | {tbw:<18} | {r['write_tokens']:<12} | {r['write_duration_s']:<12.1f} | {r['tok_per_sec']:<8.1f}")
