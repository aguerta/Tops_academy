import json
import sys

# Load batch file
batch_path = "reports/c2c_audits/20261026_015938_estadistica_3_pre_parcial_v2_857d5b79/agentic_batches/shards_batch_08.json"
timing_path = "reports/c2c_audits/20261026_015938_estadistica_3_pre_parcial_v2_857d5b79/shard_timing_profile.json"

with open(batch_path, "r", encoding="utf-8") as f:
    batch = json.load(f)

with open(timing_path, "r", encoding="utf-8") as f:
    timing = json.load(f)

timing_map = {s["shard_id"]: s for s in timing.get("all_shards", [])}

analysis = {
    "total_shards": len(batch["subagents"]),
    "shards": []
}

total_in = 0
total_out = 0
total_cache = 0
total_think = 0
total_active = 0
total_tokens = 0
total_duration_s = 0

for s in batch["subagents"]:
    sid = s.get("shard_id")
    prof = timing_map.get(sid, {})
    
    in_tok = s.get("input_tokens", 0)
    out_tok = s.get("output_tokens", 0)
    cache_tok = s.get("cache_read_tokens", 0)
    think_tok = s.get("thinking_tokens", 0)
    act_tok = s.get("active_tokens", 0)
    tot_tok = s.get("total_tokens", 0)
    dur_s = s.get("duration_seconds", 0)
    
    total_in += in_tok
    total_out += out_tok
    total_cache += cache_tok
    total_think += think_tok
    total_active += act_tok
    total_tokens += tot_tok
    total_duration_s += dur_s
    
    # Analyze tool calls and errors
    tool_calls = s.get("tool_calls_by_name", {})
    tool_errors_count = s.get("tool_errors_count", 0)
    
    # Pre vs Post compile from timing profile
    pre_s = prof.get("pre_1st_compile_s", 0)
    post_s = prof.get("post_1st_compile_s", 0)
    compile_runs = prof.get("compile_runs", 0)
    compile_fails = prof.get("compile_fails", 0)
    edits = prof.get("edits_count", 0)
    
    # Inspect steps for tool errors and thinking traces
    steps = s.get("steps", [])
    step_errors = []
    for step_idx, step in enumerate(steps):
        # check tool error
        res = step.get("tool_step_result", {})
        err = res.get("error") if isinstance(res, dict) else None
        tool_name = step.get("tool_name")
        thought = step.get("thought", "")
        if err or res.get("exit_code", 0) != 0 or "Error" in str(res):
            step_errors.append({
                "step_index": step_idx,
                "tool_name": tool_name,
                "error": str(err)[:200] if err else str(res)[:200],
                "thought_before": thought[:300] if thought else ""
            })
            
    err_traces = s.get("error_thinking_traces", [])
    
    analysis["shards"].append({
        "shard_id": sid,
        "label": s.get("label"),
        "conversation_id": s.get("conversation_id"),
        "duration_s": dur_s,
        "duration_min": s.get("duration_minutes", 0),
        "input_tokens": in_tok,
        "output_tokens": out_tok,
        "cache_read_tokens": cache_tok,
        "thinking_tokens": think_tok,
        "active_tokens": act_tok,
        "total_tokens": tot_tok,
        "turns_count": s.get("turns_count", 0),
        "tool_calls_count": s.get("tool_calls_count", 0),
        "tool_calls_by_name": tool_calls,
        "tool_errors_count": tool_errors_count,
        "failed_commands": s.get("failed_commands", []),
        "competencies": s.get("competencies", []),
        "competencies_count": s.get("competencies_count", 0),
        "tokens_per_competency": s.get("tokens_per_competency", 0),
        "pre_1st_compile_s": pre_s,
        "post_1st_compile_s": post_s,
        "compile_runs": compile_runs,
        "compile_fails": compile_fails,
        "edits_count": edits,
        "step_errors": step_errors,
        "error_thinking_traces_count": len(err_traces),
        "error_thinking_traces": err_traces,
        "has_micro_loop": prof.get("has_micro_loop", False),
        "micro_loop_reason": prof.get("micro_loop_reason", "")
    })

analysis["aggregates"] = {
    "total_input_tokens": total_in,
    "total_output_tokens": total_out,
    "total_cache_read_tokens": total_cache,
    "total_thinking_tokens": total_think,
    "total_active_tokens": total_active,
    "total_tokens": total_tokens,
    "total_duration_s": total_duration_s,
    "total_duration_min": round(total_duration_s / 60, 2),
    "mean_duration_s": round(total_duration_s / len(batch["subagents"]), 2),
    "max_duration_s": max(s["duration_s"] for s in analysis["shards"]),
    "min_duration_s": min(s["duration_s"] for s in analysis["shards"]),
}

with open("reports/c2c_audits/20261026_015938_estadistica_3_pre_parcial_v2_857d5b79/agentic_batches/batch_08_analysis.json", "w", encoding="utf-8") as f:
    json.dump(analysis, f, indent=2, ensure_ascii=False)

print("Analysis successfully written to batch_08_analysis.json")
