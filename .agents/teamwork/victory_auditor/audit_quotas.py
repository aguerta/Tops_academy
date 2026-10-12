import json

for path in ['courses/pde_course.json', 'courses/demo_course.json']:
    with open(path, encoding='utf-8') as f:
        c = json.load(f)
    print('='*50)
    print(f"Course: {c.get('course_id')} ({path})")
    print(f"Total competencies: {len(c.get('competencies', []))}")
    print(f"Total questions: {len(c.get('questions', []))}")
    
    comp_map = {comp['id']: comp for comp in c.get('competencies', [])}
    comp_counts = {}
    for q in c.get('questions', []):
        cid = q['competency_id']
        comp_counts[cid] = comp_counts.get(cid, 0) + 1
        
    for comp in c.get('competencies', []):
        cat = comp.get('category')
        cid = comp['id']
        cnt = comp_counts.get(cid, 0)
        req = 30 if cat == 'Skill' else 20
        assert cnt >= req, f"{cid} ({cat}) has {cnt} < {req}"
        print(f"  {cid} [{cat}]: {cnt} questions (req >= {req}) -> OK")
        
    type_counts = {}
    for q in c.get('questions', []):
        t = q.get('interaction_type')
        type_counts[t] = type_counts.get(t, 0) + 1
    print(f"Interaction types: {type_counts}")
    assert len(type_counts) == 3, 'Missing interaction types'
    print("ALL QUOTAS AND TYPES VERIFIED!")
