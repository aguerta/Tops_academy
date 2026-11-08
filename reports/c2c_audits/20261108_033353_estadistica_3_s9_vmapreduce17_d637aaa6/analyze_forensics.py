import json
from datetime import datetime

audit_dir = "reports/c2c_audits/20261108_033353_estadistica_3_s9_vmapreduce17_d637aaa6"

with open(f"{audit_dir}/telemetry.json", "r", encoding="utf-8") as f:
    telem = json.load(f)

with open(f"{audit_dir}/shard_timing_profile.json", "r", encoding="utf-8") as f:
    timing = json.load(f)

timing_by_shard = {s["shard_id"]: s for s in timing["all_shards"]}

shards_data = []
for s in telem["subagents"]:
    label = s.get("label", "")
    if "Shard" not in label:
        continue
    shard_id = s.get("shard_id")
    steps = s.get("steps", [])
    
    # Calculate step intervals
    step_details = []
    prev_dt = None
    for st in steps:
        dt_str = st.get("created_at")
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00")) if dt_str else None
        elapsed = (dt - prev_dt).total_seconds() if (prev_dt and dt) else 0.0
        prev_dt = dt
        step_details.append({
            "step_index": st.get("step_index"),
            "created_at": dt_str,
            "elapsed_since_prev": elapsed,
            "in_tokens": st.get("input_tokens"),
            "out_tokens": st.get("output_tokens"),
            "tools": st.get("tools", [])
        })
    
    t_prof = timing_by_shard.get(shard_id, {})
    shards_data.append({
        "shard_id": shard_id,
        "label": label,
        "duration_seconds": s.get("duration_seconds"),
        "pre_1st_compile_s": t_prof.get("pre_1st_compile_s"),
        "post_1st_compile_s": t_prof.get("post_1st_compile_s"),
        "compile_runs": t_prof.get("compile_runs"),
        "compile_fails": t_prof.get("compile_fails"),
        "edits_count": t_prof.get("edits_count"),
        "turns_count": s.get("turns_count"),
        "active_tokens": s.get("active_tokens"),
        "output_tokens": s.get("output_tokens"),
        "thinking_tokens": s.get("thinking_tokens"),
        "step_details": step_details
    })

# Sort by duration_seconds descending
shards_data.sort(key=lambda x: x["duration_seconds"], reverse=True)

print("TOTAL SHARDS ANALYZED:", len(shards_data))
print("=" * 80)
for s in shards_data:
    print(f"\nSHARD: {s['shard_id']} | Total: {s['duration_seconds']:.1f}s | Pre: {s['pre_1st_compile_s']}s | Post: {s['post_1st_compile_s']}s | Fails: {s['compile_fails']}/{s['compile_runs']} | Edits: {s['edits_count']} | OutTok: {s['output_tokens']}")
    for st in s["step_details"]:
        tools_str = ",".join(st["tools"])
        print(f"  Step {st['step_index']:2d} (+{st['elapsed_since_prev']:5.1f}s): tools=[{tools_str}] | in={st['in_tokens']} | out={st['out_tokens']}")
