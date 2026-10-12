import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path("tests").resolve()))
import test_blind_guess_empirical as tb

res = tb.run_blind_test(50, 42, "courses/pde_course.json")
correct_items = [r for r in res["items"] if r["is_adversarial_correct"]]
print(f"Total correct in sample (N=50): {len(correct_items)} / 50 ({len(correct_items)/50*100:.1f}%)")

from collections import Counter
c = Counter(r["competency_id"] for r in correct_items)
print("Correct count by competency in sample:")
for comp, cnt in c.most_common():
    print(f"  {comp}: {cnt}")

print("\nBreakdown of correct guesses in sample:")
for r in correct_items:
    q_id = r["question_id"]
    comp = r["competency_id"]
    rat = r["adversarial_rationale"]
    true_idx = r["true_correct_index"]
    guess_idx = r["adversarial_guess_index"]
    c_text = r["shuffled_options"][true_idx]
    print(f"\n[{q_id}] {comp} | Rationale: {rat}")
    print(f"  Correct Option: {c_text}")
    print(f"  All options:")
    for i, opt in enumerate(r["shuffled_options"]):
        marker = " [KEY]" if i == true_idx else ""
        guess_marker = " <-- GUESS" if i == guess_idx else ""
        print(f"    Opt {chr(65+i)}{marker}{guess_marker}: {opt}")
