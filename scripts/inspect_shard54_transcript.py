import json
from pathlib import Path

t_path = Path("C:/Users/augus/.gemini/antigravity/brain/c8ce1688-5927-4b17-a8c5-9db55ccc2cb6/.system_generated/logs/transcript.jsonl")

with open(t_path, "r", encoding="utf-8") as f:
    lines = [json.loads(line) for line in f if line.strip()]

print(f"Total entries in shard_54 transcript: {len(lines)}")
print("Entry types / keys:", [list(entry.keys()) for entry in lines[:5]])

for i, entry in enumerate(lines):
    ts = entry.get("timestamp") or entry.get("time") or entry.get("created_at")
    etype = entry.get("type") or entry.get("event") or entry.get("role")
    tool = entry.get("tool") or entry.get("tool_name")
    action = entry.get("toolAction") or entry.get("toolSummary")
    print(f"[{i:02d}] ts={ts} type={etype} tool={tool} summary={action} keys={list(entry.keys())[:6]}")
