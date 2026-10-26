import json
import os
import statistics

batch_path = "reports/c2c_audits/20261026_015938_estadistica_3_pre_parcial_v2_857d5b79/agentic_batches/shards_batch_01.json"
timing_profile_path = "reports/c2c_audits/20261026_015938_estadistica_3_pre_parcial_v2_857d5b79/shard_timing_profile.json"
traceback_path = "reports/c2c_audits/20261026_015938_estadistica_3_pre_parcial_v2_857d5b79/traceback_deepdive_857d5b79.json"

with open(batch_path, "r", encoding="utf-8") as f:
    batch = json.load(f)

timing_profile = {}
if os.path.exists(timing_profile_path):
    with open(timing_profile_path, "r", encoding="utf-8") as f:
        timing_profile = json.load(f)

timing_by_shard = {s["shard_id"]: s for s in timing_profile.get("all_shards", [])}

subagents = batch.get("subagents", [])

print("=== DETAILED SUMMARY TABLE ===")
headers = ["Shard", "Duration (s)", "Duration (m)", "Turns", "Input T", "Output T", "Cache T", "Think T", "Active T", "Total T", "Pre-Comp (s)", "Post-Comp (s)", "Comp Runs", "Tools", "Errors"]
row_format = "{:<10} {:>12} {:>12} {:>6} {:>10} {:>10} {:>10} {:>10} {:>10} {:>11} {:>12} {:>13} {:>10} {:>6} {:>7}"
print(row_format.format(*headers))
print("-" * 155)

table_data = []

for s in subagents:
    label = s["label"]
    shard_id = label.replace("Shard Author ", "")
    tp = timing_by_shard.get(shard_id, {})
    dur_s = s.get("duration_seconds", 0)
    dur_m = s.get("duration_minutes", 0)
    turns = s.get("turns_count", 0)
    in_t = s.get("input_tokens", 0)
    out_t = s.get("output_tokens", 0)
    cache_t = s.get("cache_read_tokens", 0)
    think_t = s.get("thinking_tokens", 0)
    act_t = s.get("active_tokens", 0)
    tot_t = s.get("total_tokens", 0)
    pre_c = tp.get("pre_1st_compile_s", 0)
    post_c = tp.get("post_1st_compile_s", 0)
    comp_runs = tp.get("compile_runs", 0)
    tools = s.get("tool_calls_count", 0)
    errs = s.get("tool_errors_count", 0)
    
    table_data.append({
        "shard_id": shard_id,
        "label": label,
        "duration_s": dur_s,
        "duration_m": dur_m,
        "turns": turns,
        "input_tokens": in_t,
        "output_tokens": out_t,
        "cache_tokens": cache_t,
        "thinking_tokens": think_t,
        "active_tokens": act_t,
        "total_tokens": tot_t,
        "pre_compile_s": pre_c,
        "post_compile_s": post_c,
        "compile_runs": comp_runs,
        "compile_fails": tp.get("compile_fails", 0),
        "tool_calls": tools,
        "tool_errors": errs,
        "tool_calls_by_name": s.get("tool_calls_by_name", {}),
        "failed_commands": s.get("failed_commands", []),
        "error_traces": s.get("error_thinking_traces", []),
        "first_thinking": tp.get("first_thinking_snippet", ""),
        "has_micro_loop": tp.get("has_micro_loop", False),
        "micro_loop_reason": tp.get("micro_loop_reason", "")
    })
    
    print(row_format.format(
        shard_id,
        f"{dur_s:.1f}",
        f"{dur_m:.2f}",
        turns,
        f"{in_t:,}",
        f"{out_t:,}",
        f"{cache_t:,}",
        f"{think_t:,}",
        f"{act_t:,}",
        f"{tot_t:,}",
        f"{pre_c:.1f}" if pre_c is not None else "N/A",
        f"{post_c:.1f}" if post_c is not None else "N/A",
        str(comp_runs),
        tools,
        errs
    ))

print("-" * 155)

# Aggregates
tot_dur_s = sum(d["duration_s"] for d in table_data)
tot_dur_m = tot_dur_s / 60
tot_in = sum(d["input_tokens"] for d in table_data)
tot_out = sum(d["output_tokens"] for d in table_data)
tot_cache = sum(d["cache_tokens"] for d in table_data)
tot_think = sum(d["thinking_tokens"] for d in table_data)
tot_act = sum(d["active_tokens"] for d in table_data)
tot_tot = sum(d["total_tokens"] for d in table_data)
tot_pre_c = sum(d["pre_compile_s"] for d in table_data if d["pre_compile_s"] is not None)
tot_post_c = sum(d["post_compile_s"] for d in table_data if d["post_compile_s"] is not None)
tot_comp_runs = sum(d["compile_runs"] for d in table_data)
tot_tools = sum(d["tool_calls"] for d in table_data)
tot_errs = sum(d["tool_errors"] for d in table_data)

print(row_format.format(
    "TOTAL",
    f"{tot_dur_s:.1f}",
    f"{tot_dur_m:.2f}",
    sum(d["turns"] for d in table_data),
    f"{tot_in:,}",
    f"{tot_out:,}",
    f"{tot_cache:,}",
    f"{tot_think:,}",
    f"{tot_act:,}",
    f"{tot_tot:,}",
    f"{tot_pre_c:.1f}",
    f"{tot_post_c:.1f}",
    str(tot_comp_runs),
    tot_tools,
    tot_errs
))

durs = [d["duration_s"] for d in table_data]
print("\n=== LATENCY STATS ===")
print(f"Cumulative Wall Time: {tot_dur_s:.1f}s ({tot_dur_m:.2f} min)")
print(f"Mean Wall Time: {statistics.mean(durs):.1f}s ({statistics.mean(durs)/60:.2f} min)")
print(f"Median Wall Time: {statistics.median(durs):.1f}s ({statistics.median(durs)/60:.2f} min)")
print(f"Min Wall Time: {min(durs):.1f}s (Shard: {min(table_data, key=lambda x: x['duration_s'])['shard_id']})")
print(f"Max Wall Time: {max(durs):.1f}s (Shard: {max(table_data, key=lambda x: x['duration_s'])['shard_id']})")
print(f"Std Dev: {statistics.stdev(durs):.1f}s")

print("\n=== RANKING (FASTEST TO SLOWEST / STRAGGLERS) ===")
by_speed = sorted(table_data, key=lambda x: x["duration_s"])
for rank, d in enumerate(by_speed, 1):
    tag = " (FASTEST)" if rank == 1 else (" (STRAGGLER #1)" if rank == len(by_speed) else (" (STRAGGLER #2)" if rank == len(by_speed)-1 else ""))
    print(f"Rank {rank:2d}: {d['shard_id']} - {d['duration_s']:.1f}s ({d['duration_m']:.2f}m) | Pre={d['pre_compile_s']}s, Post={d['post_compile_s']}s, Compiles={d['compile_runs']}, Turns={d['turns']}{tag}")

print("\n=== PRE vs POST COMPILES ANALYSIS ===")
pre_times = [d["pre_compile_s"] for d in table_data if d["pre_compile_s"] is not None]
post_times = [d["post_compile_s"] for d in table_data if d["post_compile_s"] is not None]
print(f"Total Pre-Compile Time: {sum(pre_times):.1f}s ({sum(pre_times)/tot_dur_s*100:.1f}%)")
print(f"Total Post-Compile Time: {sum(post_times):.1f}s ({sum(post_times)/tot_dur_s*100:.1f}%)")
print(f"Pre-Compile Mean: {statistics.mean(pre_times):.1f}s, Median: {statistics.median(pre_times):.1f}s")
print(f"Post-Compile Mean: {statistics.mean(post_times):.1f}s, Median: {statistics.median(post_times):.1f}s")

# Check which shards did 2 compiles vs 1 compile
single_comp = [d for d in table_data if d["compile_runs"] == 1]
multi_comp = [d for d in table_data if d["compile_runs"] > 1]
print(f"Single compile shards ({len(single_comp)}): {[d['shard_id'] for d in single_comp]}")
print(f"Multi-compile shards ({len(multi_comp)}): {[d['shard_id'] for d in multi_comp]}")

print("\n=== TOOL ANALYSIS ===")
tool_totals = {}
for d in table_data:
    for t_name, cnt in d["tool_calls_by_name"].items():
        tool_totals[t_name] = tool_totals.get(t_name, 0) + cnt

for t_name, cnt in sorted(tool_totals.items(), key=lambda x: x[1], reverse=True):
    print(f"  {t_name:15}: {cnt:3d} calls ({cnt/tot_tools*100:5.1f}%)")
print(f"Total tool calls: {tot_tools}")
print(f"Total tool errors: {tot_errs} ({tot_errs/tot_tools*100:.1f}% error rate)")
