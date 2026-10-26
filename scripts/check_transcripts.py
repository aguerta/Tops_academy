import json
from pathlib import Path

brain_dir = Path("C:/Users/augus/.gemini/antigravity/brain")

with open('reports/c2c_audits/20261026_002637_estadistica_3_pre_parcial_821334d0/shard_timing_profile.json', 'r', encoding='utf-8') as f:
    timing = json.load(f)

cluster_shards = [s for s in timing['all_shards'] if s['shard_id'] in [f'shard_{i:02d}' for i in range(51, 61)]]
cluster_shards.sort(key=lambda x: x['shard_id'])

print(f"Checking transcript availability for {len(cluster_shards)} shards:")
for s in cluster_shards:
    cid = s['conversation_id']
    t_path = brain_dir / cid / ".system_generated" / "logs" / "transcript.jsonl"
    print(f"{s['shard_id']} ({cid}): exists = {t_path.exists()} (size: {t_path.stat().st_size if t_path.exists() else 0} bytes)")
