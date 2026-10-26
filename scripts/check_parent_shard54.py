import json

parent_path = 'C:/Users/augus/.gemini/antigravity/brain/821334d0-216d-40c5-8920-dca90c0f0b26/.system_generated/logs/transcript.jsonl'
with open(parent_path, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'shard_54' in line:
            obj = json.loads(line)
            ts = obj.get('created_at')
            tcs = obj.get('tool_calls', [])
            content = str(obj.get('content', ''))
            print(f"Line {i} ({ts}) type={obj.get('type')}")
            for tc in tcs:
                print(f"  Tool: {tc.get('name')} args={str(tc.get('args'))[:150]}")
            if 'DONE' in content:
                print(f"  Content: {content[:150]}")
