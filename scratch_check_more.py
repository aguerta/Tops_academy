import json

with open('reports/c2c_audits/20261026_015938_estadistica_3_pre_parcial_v2_857d5b79/telemetry.json', 'r', encoding='utf-8') as f:
    telem = json.load(f)

print("telemetry.json keys:", list(telem.keys()))

# Check orchestrator_audit in telem
if 'orchestrator_audit' in telem:
    print("orchestrator_audit keys in telem:", list(telem['orchestrator_audit'].keys()))

# Check thinking_traces_summary
if 'thinking_traces_summary' in telem:
    print("thinking_traces_summary:", json.dumps(telem['thinking_traces_summary'], indent=2)[:1000])

# Check if there is raw conversation or turns in telemetry.json or anywhere else
# Check subagents
print("Subagents count in telem:", len(telem.get('subagents', [])))

# Let's inspect traceback_deepdive
try:
    with open('reports/c2c_audits/20261026_015938_estadistica_3_pre_parcial_v2_857d5b79/traceback_deepdive_857d5b79.json', 'r', encoding='utf-8') as f:
        tb = json.load(f)
    print("traceback_deepdive keys:", list(tb.keys()) if isinstance(tb, dict) else len(tb))
    if isinstance(tb, dict):
        for k in tb:
            if isinstance(tb[k], list):
                print(f"  {k}: {len(tb[k])} items")
            else:
                print(f"  {k}: {type(tb[k])}")
except Exception as e:
    print("traceback_deepdive error:", e)
