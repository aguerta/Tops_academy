import json
from pathlib import Path

t_path = Path("C:/Users/augus/.gemini/antigravity/brain/c8ce1688-5927-4b17-a8c5-9db55ccc2cb6/.system_generated/logs/transcript.jsonl")

with open(t_path, "r", encoding="utf-8") as f:
    entries = [json.loads(line) for line in f if line.strip()]

for i in range(0, 29):
    e = entries[i]
    ts = e.get("created_at")
    stype = e.get("type")
    status = e.get("status")
    print(f"--- STEP {i:02d} ({ts}) type={stype} status={status} ---")
    if "tool" in e or "tools" in e:
        print(f"  Tool: {e.get('tool')} | Tools: {e.get('tools')}")
    if "error" in e:
        print(f"  Error: {str(e.get('error'))[:200]}")
    if "content" in e:
        c = str(e.get("content"))
        print(f"  Content snippet: {c[:200]}...")
    if "thinking" in e:
        th = str(e.get("thinking"))
        print(f"  Thinking snippet: {th[:200]}...")
    if "input_tokens" in e:
        print(f"  Tokens: in={e.get('input_tokens')}, out={e.get('output_tokens')}, cache={e.get('cache_read_tokens')}")
