import json
import re

with open('courses/estadistica3_regresion.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

questions = data['questions']
comps = data['competencies']

print('--- QUESTION COUNT & COMP STATS ---')
comp_ids = [c['id'] for c in comps]
q_comp_counts = {}
for q in questions:
    cid = q['competency_id']
    q_comp_counts[cid] = q_comp_counts.get(cid, 0) + 1

for c in comps:
    print(f"{c['id']} ({c['category']}): {q_comp_counts.get(c['id'], 0)} questions | {c['name'][:50]}")

print('\n--- HINTS ANALYSIS ---')
hint_lens = [len(q.get('hints', [])) for q in questions]
print(f"Min hints: {min(hint_lens)}, Max hints: {max(hint_lens)}, Avg hints: {sum(hint_lens)/len(hint_lens):.2f}")
under_3_hints = [q['id'] for q in questions if len(q.get('hints', [])) < 3]
print(f"Questions with < 3 hints: {len(under_3_hints)}")
zero_hints = [q['id'] for q in questions if len(q.get('hints', [])) == 0]
print(f"Questions with 0 hints: {len(zero_hints)}")

print('\n--- QUESTION TYPES ---')
types = {}
for q in questions:
    t = q.get('type')
    types[t] = types.get(t, 0) + 1
print('Types:', types)

print('\n--- BLOOM TAXONOMY & DIFFICULTY ---')
blooms = {}
diffs = {}
for q in questions:
    b = q.get('bloom_taxonomy_level')
    blooms[b] = blooms.get(b, 0) + 1
    d = q.get('difficulty')
    diffs[d] = diffs.get(d, 0) + 1
print('Bloom levels:', blooms)
print('Difficulties:', diffs)

print('\n--- FEEDBACK / ERROR RATIONALES ---')
mc_questions = [q for q in questions if q.get('type') == 'multiple_choice_7_options']
total_mc_options = 0
distractor_rationales = 0
for q in mc_questions:
    opts = q.get('options', [])
    for opt in opts:
        if not opt.get('is_correct', False):
            total_mc_options += 1
            if opt.get('error_rationale'):
                distractor_rationales += 1

print(f"MC distractor rationales: {distractor_rationales}/{total_mc_options} ({(distractor_rationales/total_mc_options)*100:.1f}%)")

misconceptions = [q['id'] for q in questions if q.get('misconception_warning') or q.get('common_misconception_warning')]
print(f"Questions with misconception warnings: {len(misconceptions)}/{len(questions)}")

solutions = [q['id'] for q in questions if q.get('detailed_solution')]
print(f"Questions with detailed solution: {len(solutions)}/{len(questions)}")
