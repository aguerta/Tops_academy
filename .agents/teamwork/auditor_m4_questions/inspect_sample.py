import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

start = int(sys.argv[1]) if len(sys.argv) > 1 else 1
end = int(sys.argv[2]) if len(sys.argv) > 2 else 10

with open('.agents/teamwork/auditor_m4_questions/sample_45.json', 'r', encoding='utf-8') as f:
    sample = json.load(f)

for item in sample:
    idx = item["sample_index"]
    if idx < start or idx > end:
        continue
    print("=" * 80)
    print(f"SAMPLE #{idx:02d} | ID: {item['id']} | Comp: {item['competency_id']} ({item['competency_category']}) | Type: {item['type']} | Diff: {item['difficulty']}")
    print(f"Comp Name: {item['competency_name']}")
    print(f"Stem:\n{item['stem']}")
    print("-" * 40)
    if item['type'] in ('multiple_choice_7_options', 'multiple_select'):
        print(f"Designated Correct Answer: {item['correct_answer']}")
        print("Options:")
        for opt in item['options']:
            flag = "[CORRECT]" if opt.get('is_correct') else "         "
            print(f"  {flag} ({opt.get('option_id') or opt.get('id')}): {opt.get('content')}")
            if opt.get('error_rationale'):
                print(f"        Rationale: {opt.get('error_rationale')}")
    else:
        print(f"Designated Correct Answer: {item['correct_answer']}")
    print("-" * 40)
    print("Hints:")
    for h_i, h in enumerate(item['hints'], 1):
        print(f"  Hint {h_i}: {h}")
    print("-" * 40)
    print(f"Detailed Solution:\n{item['detailed_solution']}")
    print("-" * 40)
    print(f"Misconception Warning:\n{item.get('misconception_warning')}")
    print("\n")
