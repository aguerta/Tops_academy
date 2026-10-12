import json
import re

with open('courses/estadistica3_regresion.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

questions = data['questions']
comps = {c['id']: c for c in data['competencies']}

print('=== 1. LATEX DELIMITER AUDIT ===')
latex_issues = []
for q in questions:
    texts_to_check = [q.get('stem', '')]
    if 'hints' in q:
        texts_to_check.extend(q['hints'])
    if 'detailed_solution' in q:
        texts_to_check.append(q['detailed_solution'])
    for opt in q.get('options', []):
        texts_to_check.append(opt.get('content', ''))
    
    for t in texts_to_check:
        # Check odd number of non-escaped single dollar signs
        # remove escaped dollars
        t_clean = t.replace(r'\$', '')
        # count $$
        double_dollars = t_clean.count('$$')
        t_without_double = t_clean.replace('$$', '')
        single_dollars = t_without_double.count('$')
        if single_dollars % 2 != 0:
            latex_issues.append((q['id'], 'Unbalanced single $', t[:80]))
        if double_dollars % 2 != 0:
            latex_issues.append((q['id'], 'Unbalanced double $$', t[:80]))

print(f"Total latex delimiter issues found: {len(latex_issues)}")
if latex_issues:
    for issue in latex_issues[:10]:
        print("  ", issue)

print('\n=== 2. HINTS PROGRESSION AUDIT ===')
# Check hints progression: hint 1 vs hint 2 vs hint 3
hints_sample = []
for i in [0, 50, 100, 150, 200, 250, 300, 350]:
    q = questions[i]
    hints_sample.append((q['id'], q['hints']))

for qid, h in hints_sample[:3]:
    print(f"Question {qid} hints:")
    for idx, hint in enumerate(h):
        print(f"  Level {idx+1}: {hint}")

print('\n=== 3. FILL IN THE BLANK AUDIT ===')
fib_questions = [q for q in questions if q.get('type') == 'fill_in_the_blank']
print(f"Total FIB: {len(fib_questions)}")
fib_keys = set()
for q in fib_questions:
    fib_keys.update(q.keys())
print("FIB keys:", fib_keys)
if fib_questions:
    sample_fib = fib_questions[0]
    print("Sample FIB:", json.dumps({k: sample_fib[k] for k in ['id', 'stem', 'correct_answer', 'interface_config'] if k in sample_fib}, indent=2, ensure_ascii=False))

print('\n=== 4. MULTIPLE SELECT AUDIT ===')
ms_questions = [q for q in questions if q.get('type') == 'multiple_select']
print(f"Total MS: {len(ms_questions)}")
if ms_questions:
    sample_ms = ms_questions[0]
    print("Sample MS:", json.dumps({k: sample_ms[k] for k in ['id', 'stem', 'options', 'correct_answer'] if k in sample_ms}, indent=2, ensure_ascii=False))

print('\n=== 5. CHECK QUESTION UNIQUENESS / STEM VARIETY ===')
stems = [q['stem'] for q in questions]
unique_stems = set(stems)
print(f"Total stems: {len(stems)}, Unique stems: {len(unique_stems)}")
if len(stems) != len(unique_stems):
    print("Stem duplicate count:", len(stems) - len(unique_stems))
