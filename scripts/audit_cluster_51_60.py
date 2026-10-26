import json

with open('reports/c2c_audits/20261026_002637_estadistica_3_pre_parcial_821334d0/telemetry.json', 'r', encoding='utf-8') as f:
    telem = json.load(f)

# Find all subagents for shard_51 to shard_60
shards_map = {}
for sa in telem['subagents']:
    sid = sa.get('shard_id')
    if sid and sid in [f'shard_{i:02d}' for i in range(51, 61)]:
        shards_map[sid] = sa

print(f"Found {len(shards_map)} subagents in telemetry matching shards 51-60.")

# Print key details of each shard
for sid in sorted(shards_map.keys()):
    sa = shards_map[sid]
    print(f"==================================================")
    print(f"SHARD: {sid} | Conv: {sa['conversation_id']}")
    print(f"Duration: {sa['duration_seconds']}s ({sa['duration_minutes']} min)")
    print(f"Start: {sa['start_time']} -> End: {sa['end_time']}")
    print(f"Turns: {sa['turns_count']} | Tools called: {sa['tool_calls_count']}")
    print(f"Tool calls breakdown: {sa['tool_calls_by_name']}")
    print(f"Tool errors count: {sa['tool_errors_count']}")
    print(f"Failed commands: {len(sa['failed_commands'])}")
    for fc in sa['failed_commands']:
        print(f"  Fail at step {fc.get('step_index')}: {fc.get('snippet')[:100]}...")
    print(f"Active Tokens: {sa['active_tokens']:,} (Input: {sa['input_tokens']:,}, Output: {sa['output_tokens']:,}, Thinking: {sa['thinking_tokens']:,})")
    print(f"Cache Read Tokens: {sa['cache_read_tokens']:,} | Total Tokens: {sa['total_tokens']:,}")
    print(f"Competencies: {sa['competencies']} (count: {sa['competencies_count']})")
    print(f"Thinking turns count: {sa['thinking_turns_count']} | chars: {sa['thinking_chars']}")
    print(f"Error thinking traces: {len(sa['error_thinking_traces'])}")
    for ett in sa['error_thinking_traces']:
        print(f"  Trace step {ett.get('step_index')}: {ett.get('thinking_snippet')[:120]}...")
    print(f"Steps count in record: {len(sa['steps'])}")
