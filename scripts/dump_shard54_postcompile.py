import json
import sys
from pathlib import Path

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

t_path = Path("C:/Users/augus/.gemini/antigravity/brain/c8ce1688-5927-4b17-a8c5-9db55ccc2cb6/.system_generated/logs/transcript.jsonl")

with open(t_path, "r", encoding="utf-8") as f:
    entries = [json.loads(line) for line in f if line.strip()]

for i in range(27, len(entries)):
    e = entries[i]
    ts = e.get("created_at")
    stype = e.get("type")
    status = e.get("status")
    print(f"=== STEP {i:02d} ({ts}) type={stype} status={status} ===")
    for k in ["tool", "tools", "error"]:
        if k in e:
            print(f"  {k}: {e[k]}")
    if "content" in e:
        c = str(e["content"]).replace('\r', '')
        print(f"  Content ({len(c)} chars): {c[:400]}...")
    if "thinking" in e:
        th = str(e["thinking"]).replace('\r', '')
        print(f"  Thinking ({len(th)} chars): {th[:300]}...")
    if "input_tokens" in e:
        print(f"  Tokens: in={e.get('input_tokens')}, out={e.get('output_tokens')}, cache={e.get('cache_read_tokens')}")
