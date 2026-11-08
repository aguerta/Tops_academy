import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

audit_dir = "reports/c2c_audits/20261108_033353_estadistica_3_s9_vmapreduce17_d637aaa6"

with open(f"{audit_dir}/traceback_deepdive_d637aaa6.json", "r", encoding="utf-8") as f:
    tb = json.load(f)

print("=== SEARCHING PRE-TOOL HOOK IN ERRORS ===")
for cat, items in tb.get("error_taxonomy", {}).items():
    for it in items:
        s = str(it)
        if "hook" in s.lower() or "denied" in s.lower():
            ag = it.get("agent")
            step = it.get("step_index", it.get("step"))
            print(f"Agent: {ag} (step {step}) | Cat: {cat}")
            print(f"  Item: {s[:400]}")
            print("-" * 60)

