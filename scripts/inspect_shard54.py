import json

with open('reports/c2c_audits/20261026_002637_estadistica_3_pre_parcial_821334d0/telemetry.json', 'r', encoding='utf-8') as f:
    telem = json.load(f)

for sa in telem['subagents']:
    sid = sa.get('shard_id')
    if sid == 'shard_54':
        print("=== SHARD 54 FULL TELEMETRY KEYS ===")
        print(sa.keys())
        print("Failed commands detail:")
        print(json.dumps(sa.get('failed_commands', []), indent=2))
        print("Error thinking traces detail:")
        print(json.dumps(sa.get('error_thinking_traces', []), indent=2))
        print("Steps:")
        for s in sa.get('steps', []):
            print(s)
