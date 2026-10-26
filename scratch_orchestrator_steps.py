import json

with open('reports/c2c_audits/20261026_015938_estadistica_3_pre_parcial_v2_857d5b79/agentic_batches/orchestrator_payload.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

om = data['orchestrator_audit']['metrics']
steps = om.get('steps', [])

print(f"Total steps in orchestrator metrics: {len(steps)}")
for i, s in enumerate(steps):
    tools = s.get('tools', [])
    err = s.get('had_error', False)
    # print all steps with tools or errors or large output/input
    if err or tools:
        print(f"Step {s.get('step_index')} [{s.get('created_at')}]: tools={tools} had_error={err} in={s.get('input_tokens')} out={s.get('output_tokens')} cache={s.get('cache_read_tokens')}")

print("\n--- ALL KEYS IN STEP OBJECTS ---")
if steps:
    print(list(steps[0].keys()))

