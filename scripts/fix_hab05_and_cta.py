import json

# 1. Update work/cta.json
cta_path = 'work/cta.json'
with open(cta_path, 'r', encoding='utf-8') as f:
    cta_data = json.load(f)

for comp in cta_data.get('competencies', []):
    for d in comp.get('distractors', []):
        hint = d.get('remediation_hint')
        if hint:
            hint = hint.replace(r'\frac{\dot{k}}{k}', r'\dot{k}/k')
            hint = hint.replace(r'\frac{\dot{K}}{K}', r'\dot{K}/K')
            hint = hint.replace(r'\frac{\dot{L}}{L}', r'\dot{L}/L')
            hint = hint.replace(r'\frac{\dot{I}}{I}', r'\dot{I}/I')
            d['remediation_hint'] = hint
        wb = d.get('wrong_belief')
        if wb:
            wb = wb.replace(r'\frac{\dot{k}}{k}', r'\dot{k}/k')
            wb = wb.replace(r'\frac{\dot{K}}{K}', r'\dot{K}/K')
            wb = wb.replace(r'\frac{\dot{L}}{L}', r'\dot{L}/L')
            d['wrong_belief'] = wb
        man = d.get('manifestation')
        if man:
            man = man.replace(r'\frac{\dot{k}}{k}', r'\dot{k}/k')
            man = man.replace(r'\frac{\dot{K}}{K}', r'\dot{K}/K')
            man = man.replace(r'\frac{\dot{L}}{L}', r'\dot{L}/L')
            d['manifestation'] = man

with open(cta_path, 'w', encoding='utf-8') as f:
    json.dump(cta_data, f, indent=2, ensure_ascii=False)
print('Updated work/cta.json')

# 2. Update work/templates/Hab-05.json
h5_path = 'work/templates/Hab-05.json'
with open(h5_path, 'r', encoding='utf-8') as f:
    h5_data = json.load(f)

for t in h5_data.get('templates', []):
    code = t.get('generate_py', '')
    code = code.replace(r'\\frac{{\\dot{{k}}}}{{k}}', r'\\dot{{k}}/k')
    code = code.replace(r'\\frac{{\\dot{{K}}}}{{K}}', r'\\dot{{K}}/K')
    code = code.replace(r'\\frac{{\\dot{{L}}}}{{L}}', r'\\dot{{L}}/L')
    t['generate_py'] = code

with open(h5_path, 'w', encoding='utf-8') as f:
    json.dump(h5_data, f, indent=2, ensure_ascii=False)
print('Updated work/templates/Hab-05.json')
