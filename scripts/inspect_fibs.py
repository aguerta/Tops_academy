import json

with open('courses/estadistica3_regresion.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

fibs = [q for q in data['questions'] if q['type'] == 'fill_in_the_blank']
print(f"Total FIB: {len(fibs)}")
for q in fibs[::15]:
    ans = q['correct_answer']
    print(f"{q['id']} ({q['competency_id']}): stem='{q['stem'][:55]}...' ans={ans.get('value')} tol={ans.get('tolerance')} equivs={ans.get('accepted_equivalents')}")
