import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Load telemetry
telemetry_path = 'reports/c2c_audits/20261026_015938_estadistica_3_pre_parcial_v2_857d5b79/telemetry.json'
with open(telemetry_path, 'r', encoding='utf-8') as f:
    telem = json.load(f)

# Batch 02 IDs
batch_path = 'reports/c2c_audits/20261026_015938_estadistica_3_pre_parcial_v2_857d5b79/agentic_batches/judges_batch_02.json'
with open(batch_path, 'r', encoding='utf-8') as f:
    batch = json.load(f)

ids_to_judge = {s['conversation_id']: s['label'] for s in batch['subagents']}

print("Found IDs in Batch 02:", len(ids_to_judge))

# Search in telemetry subagents
for sa in telem.get('subagents', []):
    cid = sa.get('conversation_id')
    if cid in ids_to_judge:
        label = ids_to_judge[cid]
        print(f"\n==================== {label} ({cid}) ====================")
        print(f"Duration: {sa.get('duration_seconds')}s, Turns: {sa.get('turns_count')}")
        print(f"Tokens: In={sa.get('input_tokens')}, Out={sa.get('output_tokens')}, Cache={sa.get('cache_read_tokens')}, Thinking={sa.get('thinking_tokens')}")
        for st in sa.get('steps', []):
            s_idx = st.get('step_index')
            tools = st.get('tools')
            print(f"  Step {s_idx}: tools={tools}, in={st.get('input_tokens')}, out={st.get('output_tokens')}")
            # check tool calls args
            if 'tool_details' in st:
                for td in st['tool_details']:
                    name = td.get('name')
                    args = td.get('args', {})
                    if name == 'write_file':
                        path = args.get('Path') or args.get('path')
                        content_len = len(args.get('Content', ''))
                        print(f"    -> write_file Path: {path} (length: {content_len} chars)")
                    elif name == 'view_file':
                        path = args.get('AbsolutePath') or args.get('path')
                        print(f"    -> view_file Path: {path}")
                    elif name == 'send_message':
                        msg = args.get('Message', '')
                        print(f"    -> send_message: {msg[:100]}...")
            if 'thinking' in st:
                print(f"    -> thinking snippet: {st['thinking'][:120]}...")
