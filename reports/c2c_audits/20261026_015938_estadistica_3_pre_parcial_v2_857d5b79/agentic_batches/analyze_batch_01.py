import json

batch_path = "reports/c2c_audits/20261026_015938_estadistica_3_pre_parcial_v2_857d5b79/agentic_batches/cta_batch_01.json"

with open(batch_path, "r", encoding="utf-8") as f:
    data = json.load(f)

subagents = data["subagents"]

print("=== COMPETENCIES ANALYSIS ===")
for sa in subagents:
    c_count = sa.get("competencies_count", 0)
    tpc = sa.get("tokens_per_competency", 0)
    print(f"{sa['label']} | Comps: {c_count} | Tokens/Comp: {tpc:,.1f} | Model: {sa.get('model')}")
    comps = sa.get("competencies", [])
    print(f"  First few comps: {comps[:4]}")

print("\n=== STEP ERROR DETAILS ===")
for sa in subagents:
    print(f"\n--- {sa['label']} ---")
    steps = sa.get("steps", [])
    for st in steps:
        # Check what fields are in step
        step_idx = st.get("step_index")
        tools = st.get("tools", [])
        # see if any error field exists
        extra_keys = [k for k in st.keys() if k not in ["step_index", "created_at", "input_tokens", "output_tokens", "cache_read_tokens", "tools"]]
        if extra_keys:
            print(f"  Step {step_idx} extra keys: {extra_keys}")

# Let's inspect the actual telemetry or raw json of one subagent's conversation if available
