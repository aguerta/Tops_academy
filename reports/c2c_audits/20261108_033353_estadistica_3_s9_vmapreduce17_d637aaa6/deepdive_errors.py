import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

audit_dir = "reports/c2c_audits/20261108_033353_estadistica_3_s9_vmapreduce17_d637aaa6"

with open(f"{audit_dir}/traceback_deepdive_d637aaa6.json", "r", encoding="utf-8") as f:
    tb = json.load(f)

print("=== ERROR TAXONOMY OVERVIEW ===")
tax = tb.get("error_taxonomy", {})
for cat, items in tax.items():
    print(f"[{len(items):3d}] {cat}")

print("\n=== SAMPLE ERRORS BY CATEGORY ===")
for cat, items in tax.items():
    print(f"\n--- Category: {cat} ({len(items)} errors) ---")
    for it in items[:4]:
        ag = it.get("agent", "Unknown")
        step = it.get("step_index", it.get("step", "?"))
        err = it.get("error_message", it.get("snippet", it.get("raw_error", "")))
        err_short = err.replace("\n", " ")[:160]
        print(f"  Agent: {ag} (step {step}): {err_short}")

