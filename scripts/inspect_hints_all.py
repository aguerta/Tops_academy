import json

with open('courses/estadistica3_regresion.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

questions = data['questions']

print("=== CHECK HINT PROGRESSION SAMPLES ===")
# Sample 1 question from each competency
comp_seen = set()
for q in questions:
    cid = q['competency_id']
    if cid not in comp_seen:
        comp_seen.add(cid)
        print(f"\n--- {cid} ({q['type']}): {q['id']} ---")
        print(f"Stem: {q['stem'][:70]}...")
        for i, h in enumerate(q['hints']):
            print(f"  Hint {i+1}: {h}")
        print(f"  Misconception: {q.get('misconception_warning') or q.get('common_misconception_warning')}")
        print(f"  Solution snippet: {q.get('detailed_solution', '')[:80]}...")
