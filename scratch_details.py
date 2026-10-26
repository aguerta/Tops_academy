import json

with open('reports/c2c_audits/20261026_015938_estadistica_3_pre_parcial_v2_857d5b79/agentic_batches/orchestrator_payload.json', 'r', encoding='utf-8') as f:
    p = json.load(f)

oa = p['orchestrator_audit']
m = oa['metrics']
td = oa['time_decomposition']
ic = oa['interventions_count']
inv = oa['interventions']

print("=== ORCHESTRATOR METRICS ===")
for k in ['conversation_id', 'label', 'start_time', 'end_time', 'duration_seconds', 'duration_minutes', 'turns_count', 
          'input_tokens', 'output_tokens', 'cache_read_tokens', 'thinking_tokens', 'active_tokens', 'total_tokens', 
          'thinking_chars', 'thinking_turns_count', 'tool_calls_count', 'tool_calls_by_name', 'tool_errors_count', 
          'failed_commands', 'from_v3_telemetry_snapshot']:
    print(f"{k}: {m.get(k)}")

print("\n=== TIME DECOMPOSITION ===")
for k, v in td.items():
    print(f"{k}: {v}")

print("\n=== INTERVENTIONS ===")
print(f"Count: {ic}")
print(f"Details: {inv}")

print("\n=== ERROR THINKING TRACES ===")
for t in m.get('error_thinking_traces', []):
    print(t)

print("\n=== STEPS ===")
for i, s in enumerate(m.get('steps', [])):
    print(f"Step {i+1} (idx {s.get('step_index')}): time={s.get('created_at')} in={s.get('input_tokens')} out={s.get('output_tokens')} cache={s.get('cache_read_tokens')} tools={s.get('tools')}")
