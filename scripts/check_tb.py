import json

with open('reports/c2c_audits/20261026_002637_estadistica_3_pre_parcial_821334d0/traceback_deepdive_821334d0.json', 'r', encoding='utf-8') as f:
    tb = json.load(f)

print("Keys in tb['shards']:", list(tb.get('shards', {}).keys()))
print("Error taxonomy:", json.dumps(tb.get('error_taxonomy', {}), indent=2))
print("Global timings:", json.dumps(tb.get('global_timings', {}), indent=2))
