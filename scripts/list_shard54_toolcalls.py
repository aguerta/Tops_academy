import json
from pathlib import Path

t_path = Path("C:/Users/augus/.gemini/antigravity/brain/c8ce1688-5927-4b17-a8c5-9db55ccc2cb6/.system_generated/logs/transcript.jsonl")

with open(t_path, "r", encoding="utf-8") as f:
    entries = [json.loads(line) for line in f if line.strip()]

for i, e in enumerate(entries):
    tcs = e.get("tool_calls", [])
    for tc in tcs:
        name = tc.get("name")
        args = tc.get("args", {})
        cmd = args.get("CommandLine") or args.get("Path") or args.get("AbsolutePath") or args.get("Message")
        print(f"Turn {i} -> Tool: {name} | Arg: {str(cmd)[:120]}")
