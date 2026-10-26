import json

path = 'reports/c2c_audits/20261026_015938_estadistica_3_pre_parcial_v2_857d5b79/telemetry.json'
with open(path, 'r', encoding='utf-8') as f:
    telem = json.load(f)

print("telemetry.json top keys:", list(telem.keys()) if isinstance(telem, dict) else len(telem))

# Look for orchestrator or conversation 857d5b79-79a1-4b2f-aaed-9e5c9f6511d5
if isinstance(telem, dict):
    if 'orchestrator' in telem:
        print("orchestrator key present in telem")
    if 'conversations' in telem:
        print("conversations present, count:", len(telem['conversations']))
    if 'stages' in telem:
        print("stages present, count:", len(telem['stages']))

with open('reports/c2c_audits/20261026_015938_estadistica_3_pre_parcial_v2_857d5b79/agentic_batches/orchestrator_payload.json', 'r', encoding='utf-8') as f:
    payload = json.load(f)

print("orchestrator_payload keys:", list(payload.keys()))
print("orchestrator_audit keys:", list(payload['orchestrator_audit'].keys()))
print("orchestrator_audit metrics keys:", list(payload['orchestrator_audit']['metrics'].keys()))
