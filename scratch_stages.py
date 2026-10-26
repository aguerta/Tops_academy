import json

with open('reports/c2c_audits/20261026_015938_estadistica_3_pre_parcial_v2_857d5b79/agentic_batches/orchestrator_payload.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

stages = data.get('stage_telemetry_v3', [])
print(f"Total stages: {len(stages)}")
for s in stages:
    idx = s.get('stage_idx')
    name = s.get('stage_name')
    st = s.get('status')
    dur = s.get('duration_seconds', 0.0)
    subs = len(s.get('subagents', []))
    toks = s.get('stage_tokens', {})
    print(f"Stage {idx}: {name:<30} | {st:<10} | {dur:>7.1f}s | Subs: {subs:>2} | Tokens: Total={toks.get('total', 0):>10,}, In={toks.get('input', 0):>8,}, Out={toks.get('output', 0):>8,}, Cache={toks.get('cached', 0):>10,}, Think={toks.get('thinking', 0):>6,}")

print("\n--- ORCHESTRATOR ERROR THINKING TRACES ---")
traces = data['orchestrator_audit']['metrics'].get('error_thinking_traces', [])
for i, t in enumerate(traces):
    print(f"Trace {i+1}: Step {t.get('step_index')} at {t.get('created_at')}")
    print(f"  Snippet: {t.get('thinking_snippet')}\n")

print("\n--- ORCHESTRATOR STEPS WITH ERRORS OR SPECIFIC TOOLS ---")
for step in data['orchestrator_audit']['metrics'].get('steps', []):
    tools = step.get('tools', [])
    had_err = step.get('had_error', False)
    # Check if there are any errors or unusual things
    if had_err or 'schedule' in tools or 'manage_task' in tools:
        print(f"Step {step.get('step_index')} ({step.get('created_at')}): tools={tools}, had_error={had_err}, in={step.get('input_tokens')}, out={step.get('output_tokens')}, cache={step.get('cache_read_tokens')}")

