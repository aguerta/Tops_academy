import json
import random
import sys

sys.stdout.reconfigure(encoding='utf-8')

course_path = "courses/pde_course.json"
with open(course_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

comp_cat = {c['id']: c['category'] for c in data['competencies']}
comp_name = {c['id']: c['name'] for c in data['competencies']}

strata = {}
for q in data['questions']:
    cat = comp_cat[q['competency_id']]
    qtype = q['type']
    key = (cat, qtype)
    if key not in strata:
        strata[key] = []
    strata[key].append(q)

random.seed(42)
sample = []
for key in sorted(strata.keys()):
    items = strata[key]
    selected = random.sample(items, 5)
    sample.extend(selected)

print(f"Total sampled questions: {len(sample)}")
comps_in_sample = set(q['competency_id'] for q in sample)
print(f"Competencies represented: {len(comps_in_sample)} / {len(comp_cat)}")

output_data = []
for idx, q in enumerate(sample, 1):
    cid = q['competency_id']
    cat = comp_cat[cid]
    item_info = {
        "sample_index": idx,
        "id": q['id'],
        "competency_id": cid,
        "competency_category": cat,
        "competency_name": comp_name[cid],
        "type": q['type'],
        "difficulty": q.get('difficulty'),
        "bloom_level": q.get('bloom_taxonomy_level'),
        "context_application": q.get('context_application'),
        "stem": q.get('stem'),
        "options": q.get('options'),
        "correct_answer": q.get('correct_answer'),
        "hints": q.get('hints'),
        "detailed_solution": q.get('detailed_solution'),
        "misconception_warning": q.get('misconception_warning') or q.get('common_misconception_warning')
    }
    output_data.append(item_info)
    print(f"[{idx:02d}] ID: {q['id']} | Comp: {cid} ({cat}) | Type: {q['type']} | Diff: {q.get('difficulty')}")

with open(".agents/teamwork/auditor_m4_questions/sample_45.json", "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print("Saved sample_45.json successfully.")
