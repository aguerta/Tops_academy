import json

with open("reports/c2c_audits/20261026_015938_estadistica_3_pre_parcial_v2_857d5b79/agentic_batches/batch_08_analysis.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("=== AGGREGATES ===")
for k, v in data["aggregates"].items():
    if isinstance(v, (int, float)):
        print(f"  {k}: {v:,.2f}" if isinstance(v, float) else f"  {k}: {v:,}")
    else:
        print(f"  {k}: {v}")

print("\n=== RANKING BY WALL TIME ===")
sorted_by_time = sorted(data["shards"], key=lambda x: x["duration_s"])
for s in sorted_by_time:
    sid = s['shard_id']
    wall = s['duration_s']
    m = s['duration_min']
    pre = s['pre_1st_compile_s']
    post = s['post_1st_compile_s']
    runs = s['compile_runs']
    edits = s['edits_count']
    turns = s['turns_count']
    errs = s['tool_errors_count']
    tot = s['total_tokens']
    comp = s['competencies_count']
    print(f"{sid} | wall: {wall}s ({m}m) | pre: {pre}s | post: {post}s | compiles: {runs} | edits: {edits} | turns: {turns} | errs: {errs} | total_tok: {tot:,} | comp: {comp}")

print("\n=== RANKING BY TOTAL TOKENS ===")
sorted_by_tok = sorted(data["shards"], key=lambda x: x["total_tokens"])
for s in sorted_by_tok:
    sid = s['shard_id']
    tot = s['total_tokens']
    inp = s['input_tokens']
    out = s['output_tokens']
    cache = s['cache_read_tokens']
    thk = s['thinking_tokens']
    act = s['active_tokens']
    print(f"{sid} | total: {tot:,} | in: {inp:,} | out: {out:,} | cache: {cache:,} | think: {thk:,} | act: {act:,}")

print("\n=== TOOL CALLS BREAKDOWN ===")
tool_totals = {}
tool_errors_total = 0
for s in data["shards"]:
    tool_errors_total += s["tool_errors_count"]
    for tname, cnt in s["tool_calls_by_name"].items():
        tool_totals[tname] = tool_totals.get(tname, 0) + cnt
print("Tool calls aggregate across batch 08:", tool_totals)
print("Total tool calls:", sum(tool_totals.values()))
print("Total tool errors:", tool_errors_total)

print("\n=== DETAILED ERRORS & THINKING TRACES ===")
for s in data["shards"]:
    print(f"\n--- {s['shard_id']} (Errors: {s['tool_errors_count']}, Turns: {s['turns_count']}, Edits: {s['edits_count']}) ---")
    if s["step_errors"]:
        print(f"  Step errors ({len(s['step_errors'])}):")
        for se in s["step_errors"]:
            print(f"    Step {se['step_index']} [{se['tool_name']}]: err='{se['error'][:150]}'")
            if se['thought_before']:
                print(f"      Thought before: {se['thought_before'][:150]}...")
    if s["error_thinking_traces"]:
        print(f"  Error thinking traces count: {len(s['error_thinking_traces'])}")
        for idx, ett in enumerate(s["error_thinking_traces"]):
            print(f"    Trace #{idx+1}: {str(ett)[:200]}...")
