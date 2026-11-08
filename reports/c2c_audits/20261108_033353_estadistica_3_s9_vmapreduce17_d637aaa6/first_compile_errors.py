import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

audit_dir = "reports/c2c_audits/20261108_033353_estadistica_3_s9_vmapreduce17_d637aaa6"

with open(f"{audit_dir}/telemetry.json", "r", encoding="utf-8") as f:
    telem = json.load(f)

print("=== FIRST COMPILE ERROR PER SHARD ===")
for s in telem["subagents"]:
    label = s.get("label", "")
    if "Shard" not in label:
        continue
    sid = s.get("shard_id")
    fails = s.get("failed_commands", [])
    if not fails:
        print(f"\n[{sid}] 0 FAILS (CLEAN PASS)")
        continue
    
    first_fail = fails[0]
    snip = first_fail.get("snippet", "")
    print(f"\n[{sid}] (Total Fails: {len(fails)}) First fail at Step {first_fail.get('step_index')}:")
    for l in snip.splitlines()[:8]:
        print("  ", l)
