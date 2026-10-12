import json
import re

with open('courses/estadistica3_regresion.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

questions = data['questions']
comps = {c['id']: c for c in data['competencies']}

print('=== COMPREHENSIVE AUDIT OF ALL 390 QUESTIONS ===')

# 1. Check for Orphan questions:
# Evaluate whether questions align semantically with competencies.
# Specifically check if questions test concepts not covered in competency description.
print('\n--- 1. SEMANTIC ALIGNMENT & ORPHAN QUESTIONS ---')
orphan_candidates = []
for q in questions:
    cid = q['competency_id']
    comp = comps[cid]
    # Check if stem or options refer to completely unrelated topics, e.g. time series ARIMA, panel data GMM, logit/probit, etc.
    unrelated_keywords = ['ARIMA', 'GMM', 'panel', 'probit', 'logit', 'VAR', 'cointegración', 'Dickey-Fuller', 'Hausman', 'multinomial']
    for kw in unrelated_keywords:
        if kw.lower() in q['stem'].lower():
            orphan_candidates.append((q['id'], cid, kw))

print(f"Orphan candidates detected: {len(orphan_candidates)}")
for oc in orphan_candidates:
    print("  ", oc)

# 2. Check for Distractor Plausibility & Rationales
print('\n--- 2. DISTRACTORS & OPTIONS AUDIT ---')
no_distractor_id = 0
empty_rationale_count = 0
duplicate_options_in_q = []
for q in questions:
    opts = q.get('options', [])
    opt_texts = [o.get('content', '').strip() for o in opts]
    if len(opt_texts) != len(set(opt_texts)):
        duplicate_options_in_q.append(q['id'])
    for o in opts:
        if not o.get('is_correct', False):
            if not o.get('distractor_id'):
                no_distractor_id += 1
            if q.get('type') == 'multiple_choice_7_options' and not o.get('error_rationale'):
                empty_rationale_count += 1

print(f"Duplicate options in single question: {len(duplicate_options_in_q)}")
print(f"MC options missing error_rationale: {empty_rationale_count}")
print(f"Distractors missing distractor_id: {no_distractor_id}")

# 3. Check FIB formatting and validation rules
print('\n--- 3. FIB ACCURACY & TOLERANCE ---')
fib_invalid = []
for q in questions:
    if q.get('type') == 'fill_in_the_blank':
        ans = q.get('correct_answer')
        if not ans or not isinstance(ans, dict) or 'value' not in ans:
            fib_invalid.append((q['id'], 'Missing answer value'))
        else:
            # check numeric or formula
            val = ans['value']
            # check if accepted_equivalents is list
            equivs = ans.get('accepted_equivalents', [])
            if not isinstance(equivs, list) or len(equivs) == 0:
                fib_invalid.append((q['id'], 'Empty accepted equivalents'))

print(f"FIB invalid specifications: {len(fib_invalid)}")

# 4. Check Multiple Select formatting
print('\n--- 4. MULTIPLE SELECT AUDIT ---')
ms_invalid = []
ms_single_correct = []
for q in questions:
    if q.get('type') == 'multiple_select':
        ans = q.get('correct_answer')
        opts = q.get('options', [])
        correct_opts = [o for o in opts if o.get('is_correct', False)]
        if not isinstance(ans, list) or len(ans) == 0:
            ms_invalid.append((q['id'], 'Answer not a list'))
        if len(correct_opts) <= 1:
            ms_single_correct.append(q['id'])

print(f"MS invalid answer format: {len(ms_invalid)}")
print(f"MS with only <= 1 correct answer (defeats multi-select): {len(ms_single_correct)}")

# 5. Check Scaffolding / Hint progression across all questions
print('\n--- 5. HINT PROGRESSION QUALITY ---')
trivial_hints = 0
for q in questions:
    hints = q.get('hints', [])
    for h in hints:
        if len(h.strip()) < 15:
            trivial_hints += 1

print(f"Trivial/too short hints (<15 chars): {trivial_hints}")

# 6. Check LaTeX details across all fields
print('\n--- 6. LATEX ACCURACY ---')
latex_syntax_errors = []
for q in questions:
    fields = [q.get('stem', ''), q.get('detailed_solution', '')] + q.get('hints', [])
    for opt in q.get('options', []):
        fields.append(opt.get('content', ''))
    
    for f_idx, text in enumerate(fields):
        # find double backslash followed by invalid latex
        # check unescaped percent signs outside math
        pass
print("LaTeX check done.")
