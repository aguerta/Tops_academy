import json
import re

with open('courses/estadistica3_regresion.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

questions = data['questions']

def test_latex_delimiters(text):
    errors = []
    # check for triple dollars
    if '$$$' in text:
        errors.append('Triple dollar $$$ found')
    # strip $$...$$
    # replace $$ with special token
    parts = text.split('$$')
    if len(parts) % 2 == 0:
        errors.append('Unpaired display math $$')
    
    # Now check inline $ within each part
    # but be careful with escaped \$
    for idx, part in enumerate(parts):
        # if idx is odd, this part is inside $$...$$
        if idx % 2 == 1:
            # inside display math, should not have single $
            if '$' in part:
                errors.append(f'Single $ inside $$ display math: {part[:40]}')
        else:
            # outside display math
            clean = part.replace(r'\$', '')
            dollar_count = clean.count('$')
            if dollar_count % 2 != 0:
                errors.append(f'Unpaired inline $: {part[:60]}')
    return errors

all_errors = []
for q in questions:
    q_errors = []
    errs = test_latex_delimiters(q['stem'])
    for e in errs:
        q_errors.append(('stem', e, q['stem'][:80]))
    
    if q.get('detailed_solution'):
        errs = test_latex_delimiters(q['detailed_solution'])
        for e in errs:
            q_errors.append(('detailed_solution', e, q['detailed_solution'][:80]))
            
    for i, h in enumerate(q.get('hints', [])):
        errs = test_latex_delimiters(h)
        for e in errs:
            q_errors.append((f'hint_{i+1}', e, h[:80]))
            
    for opt in q.get('options', []):
        errs = test_latex_delimiters(opt.get('content', ''))
        for e in errs:
            q_errors.append((f"opt_{opt.get('option_id', '')}", e, opt.get('content', '')[:80]))
            
    if q_errors:
        all_errors.append((q['id'], q_errors))

print(f"Total questions with LaTeX delimiter errors: {len(all_errors)}")
for qid, errs in all_errors:
    print(f"Question {qid}:")
    for field, err_msg, snippet in errs:
        print(f"   [{field}] {err_msg} -> snippet: {snippet}")
