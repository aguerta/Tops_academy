import json
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

# 1. Load judges_batch_02.json
batch_path = 'reports/c2c_audits/20261026_015938_estadistica_3_pre_parcial_v2_857d5b79/agentic_batches/judges_batch_02.json'
with open(batch_path, 'r', encoding='utf-8') as f:
    batch = json.load(f)

subagents = batch['subagents']
print(f"Total Subagents in Batch 02: {len(subagents)}")

# Aggregate Metrics
total_in = sum(s['input_tokens'] for s in subagents)
total_out = sum(s['output_tokens'] for s in subagents)
total_cache = sum(s['cache_read_tokens'] for s in subagents)
total_thinking = sum(s['thinking_tokens'] for s in subagents)
total_active = sum(s['active_tokens'] for s in subagents)
total_tokens_all = sum(s['total_tokens'] for s in subagents)
total_duration = sum(s['duration_seconds'] for s in subagents)
min_duration = min(s['duration_seconds'] for s in subagents)
max_duration = max(s['duration_seconds'] for s in subagents)
avg_duration = total_duration / len(subagents)

print("\n--- AGGREGATE METRICS ---")
print(f"Total Duration: {total_duration:.2f}s ({total_duration/60:.2f} min)")
print(f"Min Duration: {min_duration:.2f}s, Max Duration: {max_duration:.2f}s, Avg Duration: {avg_duration:.2f}s")
print(f"Input Tokens: {total_in:,}")
print(f"Output Tokens: {total_out:,}")
print(f"Cache Read Tokens: {total_cache:,}")
print(f"Thinking Tokens: {total_thinking:,}")
print(f"Active Tokens: {total_active:,}")
print(f"Total Tokens: {total_tokens_all:,}")

# Tools aggregation
tool_calls = {}
tool_errors = 0
for s in subagents:
    tool_errors += s.get('tool_errors_count', 0)
    for tname, tcount in s.get('tool_calls_by_name', {}).items():
        tool_calls[tname] = tool_calls.get(tname, 0) + tcount

print("\n--- TOOLS BREAKDOWN ---")
print("Tool calls:", tool_calls)
print("Tool errors:", tool_errors)
total_calls = sum(tool_calls.values())
print(f"Total tool calls: {total_calls}, Failure rate: {tool_errors/total_calls*100:.2f}%" if total_calls > 0 else "0 calls")

# Individual Ranking
sorted_by_duration = sorted(subagents, key=lambda x: x['duration_seconds'])
print("\n--- RANKING BY DURATION (Fastest to Slowest) ---")
for s in sorted_by_duration:
    print(f"{s['label']:16} | {s['duration_seconds']:6.1f}s | {s['turns_count']} turns | in: {s['input_tokens']:,} | out: {s['output_tokens']:,} | think: {s['thinking_tokens']:,} | total: {s['total_tokens']:,}")

# Look at verdicts in work/judge_batch_*.json
print("\n--- VERDICTS & DECISIONS INSPECTION ---")
judge_files = sorted([f for f in os.listdir('courses/estadistica_3_pre_parcial_v2/work') if f.startswith('judge_batch_') and f.endswith('.json')])
print("Found judge files in work:", judge_files)

for idx in range(11, 21):
    fname = f"courses/estadistica_3_pre_parcial_v2/work/judge_batch_{idx:02d}.json"
    if os.path.exists(fname):
        with open(fname, 'r', encoding='utf-8') as jf:
            jdata = json.load(jf)
            print(f"\n--- Judge {idx:02d} Content Sample ---")
            if isinstance(jdata, dict):
                print(f"Keys: {list(jdata.keys())}")
                for k in list(jdata.keys())[:5]:
                    v_str = str(jdata[k])
                    print(f"  {k}: {v_str[:120]}")
            elif isinstance(jdata, list):
                print(f"List length: {len(jdata)}")
                if len(jdata) > 0:
                    print(f"First item: {str(jdata[0])[:150]}")

# Also check judge_report.json
judge_report_path = 'courses/estadistica_3_pre_parcial_v2/work/judge_report.json'
if os.path.exists(judge_report_path):
    with open(judge_report_path, 'r', encoding='utf-8') as rf:
        rep = json.load(rf)
        print("\n--- JUDGE REPORT.JSON SUMMARY ---")
        if isinstance(rep, dict):
            print("Keys:", list(rep.keys()))
            for k in list(rep.keys()):
                print(f"Key {k}: {str(rep[k])[:200]}")
