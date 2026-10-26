import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Load judge report
with open('courses/estadistica_3_pre_parcial_v2/work/judge_report.json', 'r', encoding='utf-8') as f:
    report = json.load(f)

print("Report Disagreements / Discordances:")
for d in report.get('disagreements', []):
    print(" ", d)

# Check each judge in batch 2 (11 to 20)
print("\n--- Details per Judge in Batch 02 ---")
total_items_b2 = 0
disagreements_b2 = []

# Load ground truth if exists
with open('courses/estadistica_3_pre_parcial_v2/work/judge_ground_truth.json', 'r', encoding='utf-8') as f:
    gt = json.load(f)

print("GT type:", type(gt))
if isinstance(gt, dict):
    print("GT keys:", list(gt.keys())[:10])
    gt_map = gt
elif isinstance(gt, list):
    print("GT len:", len(gt))
    gt_map = {item.get('item_id', str(i)): item for i, item in enumerate(gt)}


for idx in range(11, 21):
    fname = f"courses/estadistica_3_pre_parcial_v2/work/judge_batch_{idx:02d}.json"
    with open(fname, 'r', encoding='utf-8') as jf:
        items = json.load(jf)
    total_items_b2 += len(items)
    
    # check agreement with ground truth
    judge_agreements = 0
    judge_disagreements = 0
    templates_covered = set()
    competencies_covered = set()
    
    for item in items:
        iid = item.get('item_id')
        tid = item.get('template_id')
        cid = item.get('competency_id')
        if tid: templates_covered.add(tid)
        if cid: competencies_covered.add(cid)
        
        # compare answer
        gt_item = gt_map.get(iid)
        # What is the field in judge vs gt?
        # Let's see the fields in item
        # item has: stem, options, selected_option / answer / response?
    
    print(f"Judge {idx:02d}: {len(items)} items | Templates: {sorted(list(templates_covered))} | Competencies: {sorted(list(competencies_covered))}")
    print(f"  First item keys: {list(items[0].keys())}")
    # print answer comparison keys
    first_item = items[0]
    gt_first = gt_map.get(first_item['item_id'], {})
    print(f"  Sample Item ID: {first_item['item_id']}")
    print(f"  Judge chosen answer / response keys: {[k for k in first_item.keys() if 'answer' in k or 'response' in k or 'choice' in k or 'solution' in k or 'selected' in k]}")
    print(f"  GT keys: {[k for k in gt_first.keys() if 'answer' in k or 'response' in k or 'choice' in k or 'solution' in k or 'selected' in k]}")

print(f"\nTotal items evaluated in Batch 02: {total_items_b2}")
