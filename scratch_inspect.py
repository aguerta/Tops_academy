import json

with open('reports/c2c_audits/20261026_015938_estadistica_3_pre_parcial_v2_857d5b79/agentic_batches/orchestrator_payload.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=== ORCHESTRATOR AUDIT METRICS ===")
for k, v in data['orchestrator_audit']['metrics'].items():
    if k not in ['steps', 'error_thinking_traces']:
        print(f"  {k}: {v}")

print("\n=== ERROR THINKING TRACES ===")
for trace in data['orchestrator_audit']['metrics'].get('error_thinking_traces', []):
    print(trace)

print("\n=== TIME DECOMPOSITION ===")
for k, v in data['orchestrator_audit'].get('time_decomposition', {}).items():
    print(f"  {k}: {v}")

print("\n=== INTERVENTIONS ===")
print("count:", data['orchestrator_audit'].get('interventions_count'))
print("items:", data['orchestrator_audit'].get('interventions'))

print("\n=== SUMMARY ===")
for k, v in data['summary'].items():
    print(f"  {k}: {v}")

print("\n=== WORKLOAD ===")
for k, v in data['workload'].items():
    if k not in ['source_files', 'shards_competencies_map', 'telemetry_snapshots']:
        print(f"  {k}: {v}")

print("\n=== UNIT ECONOMICS ===")
for k, v in data['unit_economics'].items():
    print(f"  {k}: {v}")

print("\n=== BOTTLENECKS ===")
for b in data.get('bottlenecks', []):
    print(f"  [{b.get('severity')}] {b.get('title')}: {b.get('description')}")
