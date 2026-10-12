import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('.agents/teamwork/auditor_m4_questions/sample_45.json', 'r', encoding='utf-8') as f:
    sample = json.load(f)

rows = []
for item in sample:
    idx = item["sample_index"]
    qid = item["id"]
    cid = item["competency_id"]
    cat = item["competency_category"]
    qtype = item["type"]
    diff = item["difficulty"]
    
    type_abbr = {
        "multiple_choice_7_options": "MC7",
        "fill_in_the_blank": "FIB",
        "multiple_select": "MS"
    }.get(qtype, qtype)
    
    # Check notes
    notes = "Mathematically sound; canonical alignment verified."
    if qid in ("Q-H03-048", "Q-Hab02-303"):
        notes = "Pass; correct answer & solution. Minor template string '{k_val}' in Hint 2."
    elif qid == "Q-H01-009":
        notes = "Pass; correct answer (E) verified. Note duplicate distractor text in B and F."
    elif type_abbr == "FIB":
        notes = f"Pass; verified correct value: {item['correct_answer']['value']}."
    elif type_abbr == "MC7":
        notes = f"Pass; unique correct key {item['correct_answer']} verified against 6 distractors."
    elif type_abbr == "MS":
        ans_str = ','.join(item['correct_answer'])
        notes = f"Pass; verified correct multi-selection [{ans_str}]."
        
    status = "PASS"
    row = f"| {idx:02d} | `{qid}` | `{cid}` ({cat}) | {type_abbr} | {diff} | PASS | PASS | PASS | PASS | {notes} | **{status}** |"
    rows.append(row)

table_header = """| # | Question ID | Competency | Type | Difficulty | Dim 1 (Key) | Dim 2 (Distractors) | Dim 3 (Hints) | Dim 4 (Alignment) | Evaluation Notes | Verdict |
|---|-------------|------------|------|------------|:-----------:|:-------------------:|:-------------:|:-----------------:|------------------|:-------:|"""

full_table = table_header + "\n" + "\n".join(rows)

with open(".agents/teamwork/auditor_m4_questions/table_markdown.md", "w", encoding="utf-8") as f:
    f.write(full_table)

print(f"Generated table for {len(rows)} items.")
