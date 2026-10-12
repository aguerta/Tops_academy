import json

with open('courses/sistemas_edos.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('--- CHECKING MISMATCHES IN sistemas_edos.json ---')
mismatches = []
for q in data['questions']:
    cid = q.get('competency_id')
    ctx = q.get('context_application', '')
    stem = q.get('stem') or q.get('prompt', '')
    if ('IS-LM' in stem or 'Goodwin' in stem) and cid not in ['C-05', 'Hab-01', 'Hab-02']:
        mismatches.append((q['id'], cid, ctx, stem[:60]))

print(f'Total mismatched questions found: {len(mismatches)}')
for qid, cid, ctx, s in mismatches[:15]:
    print(f'  {qid} [{cid}]: ctx="{ctx}" | stem="{s}"')
