import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

audit_dir = "reports/c2c_audits/20261108_033353_estadistica_3_s9_vmapreduce17_d637aaa6"

with open(f"{audit_dir}/telemetry.json", "r", encoding="utf-8") as f:
    telem = json.load(f)

# Find subagents by shard_id
target_shards = ["shard_01", "shard_18", "shard_24", "shard_07", "shard_16", "shard_20", "shard_21", "shard_25", "shard_26", "shard_03", "shard_14"]

for s in telem["subagents"]:
    sid = s.get("shard_id")
    if sid not in target_shards:
        continue
    print("=" * 100)
    print(f"SUBAGENT: {s.get('label')} ({sid}) | Duration: {s.get('duration_seconds')}s | Turns: {s.get('turns_count')} | ActiveTok: {s.get('active_tokens')}")
    print(f"Tool calls by name: {s.get('tool_calls_by_name')}")
    print(f"Failed commands: {len(s.get('failed_commands', []))}")
    for fc in s.get("failed_commands", []):
        print(f"   [FAIL CMD]: {fc}")
    print(f"Error thinking traces: {len(s.get('error_thinking_traces', []))}")
    for ett in s.get("error_thinking_traces", [])[:3]:
        print(f"   [ERROR THINKING]: {ett}")

