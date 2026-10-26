import json
from pathlib import Path

t_path = Path("C:/Users/augus/.gemini/antigravity/brain/c8ce1688-5927-4b17-a8c5-9db55ccc2cb6/.system_generated/logs/transcript.jsonl")

with open(t_path, "r", encoding="utf-8") as f:
    entries = [json.loads(line) for line in f if line.strip()]

for i in [48, 49, 50, 51]:
    print(f"--- STEP {i} ---")
    print(json.dumps(entries[i], indent=2))
