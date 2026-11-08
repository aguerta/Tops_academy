import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

shards_map = {
    "shard_14": "68945e20-1ec1-420b-b326-9f3e96f5372d",
    "shard_03": "1122dea8-a345-48b0-9c4a-b8ac1cdc8fd1",
    "shard_01": "d2181ae1-9ad3-4a61-aade-8121a87fdb7f",
    "shard_18": "0d39880e-5419-46ae-b5de-22deed85e04a",
    "shard_24": "3c391d6c-d29e-4c58-b81d-c6701a4edeb4",
    "shard_20": "c9945df8-5ca8-4721-a4b0-379e498c0b52",
    "shard_16": "d2e5a4f7-111d-44a7-897b-9195b6c20530",
    "shard_26": "bbfeebfc-b3b0-4663-88bc-39be9bdaaa2f",
    "shard_21": "5e55e5fa-4c4f-4d64-9be1-08ec5d115e4f",
    "shard_25": "a3122c95-da25-4c6e-8519-75a7dfab06e7"
}

user_home = Path.home()

def inspect_transcript(shard_id, conv_id):
    t_file = user_home / ".gemini" / "antigravity" / "brain" / conv_id / ".system_generated" / "logs" / "transcript.jsonl"
    if not t_file.is_file():
        print(f"[{shard_id}] Transcript not found at {t_file}")
        return
    
    lines = t_file.read_text(encoding="utf-8", errors="ignore").splitlines()
    print("=" * 100)
    print(f"SHARD: {shard_id} (Conv: {conv_id}) | Total transcript lines: {len(lines)}")
    
    turn_idx = 0
    for l in lines:
        if not l.strip():
            continue
        try:
            entry = json.loads(l)
        except Exception:
            continue
        
        # Check event type
        # In AGY transcript.jsonl, lines can have different formats
        role = entry.get("role") or entry.get("type")
        content = entry.get("content") or entry.get("message", "")
        # Inspect tool calls
        tool_calls = []
        if "tool_calls" in entry:
            tool_calls = entry["tool_calls"]
        elif "tool_call" in entry:
            tool_calls = [entry["tool_call"]]
        elif "tools" in entry:
            tool_calls = entry["tools"]
            
        print(f"Line {turn_idx}: keys={list(entry.keys())[:6]} role={role}")
        turn_idx += 1
        if turn_idx > 10:
            print("... (truncated)")
            break

for sid, cid in [("shard_14", shards_map["shard_14"]), ("shard_01", shards_map["shard_01"])]:
    inspect_transcript(sid, cid)
