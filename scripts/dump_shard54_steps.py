import json
from pathlib import Path

t_path = Path("C:/Users/augus/.gemini/antigravity/brain/c8ce1688-5927-4b17-a8c5-9db55ccc2cb6/.system_generated/logs/transcript.jsonl")

with open(t_path, "r", encoding="utf-8") as f:
    entries = [json.loads(line) for line in f if line.strip()]

for i, e in enumerate(entries):
    ts = e.get("created_at")
    stype = e.get("type")
    status = e.get("status")
    print(f"--- STEP {i} ({ts}) type={stype} status={status} ---")
    
    # Check for prompt / content
    if "content" in e:
        c = str(e["content"])
        if len(c) > 300:
            print(f"Content: {c[:250]}... [len {len(c)}]")
        else:
            print(f"Content: {c}")
            
    # Check for tools or actions
    if "tools" in e:
        print(f"Tools: {e['tools']}")
    if "tool" in e:
        print(f"Tool: {e['tool']}")
        
    # Check for error
    if "error" in e:
        print(f"Error: {str(e['error'])[:300]}")
        
    # Check for token metrics or thinking
    if "thinking" in e:
        th = str(e["thinking"])
        print(f"Thinking ({len(th)} chars): {th[:250]}...")
    if "input_tokens" in e:
        print(f"Tokens: in={e.get('input_tokens')}, out={e.get('output_tokens')}, cache={e.get('cache_read_tokens')}")

