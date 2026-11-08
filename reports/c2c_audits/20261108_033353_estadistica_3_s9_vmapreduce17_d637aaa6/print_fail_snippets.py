import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

audit_dir = "reports/c2c_audits/20261108_033353_estadistica_3_s9_vmapreduce17_d637aaa6"

with open(f"{audit_dir}/telemetry.json", "r", encoding="utf-8") as f:
    telem = json.load(f)

with open(f"{audit_dir}/traceback_deepdive_d637aaa6.json", "r", encoding="utf-8") as f:
    tb = json.load(f)

for sid in ["shard_01", "shard_24", "shard_20", "shard_21", "shard_25", "shard_26", "shard_07"]:
    # Find in subagents
    sub = next((s for s in telem["subagents"] if s.get("shard_id") == sid), None)
    if not sub:
        continue
    print("=" * 100)
    print(f"SHARD: {sid} | Duration: {sub.get('duration_seconds')}s | Turns: {sub.get('turns_count')}")
    print("FAILED COMMANDS / CHECK RUNS:")
    for fc in sub.get("failed_commands", []):
        snip = fc.get("snippet", "")
        print(f"  --- Step {fc.get('step_index')} ---")
        for line in snip.splitlines()[:10]:
            print(f"      {line}")
