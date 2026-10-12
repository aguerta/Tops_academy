import sys
from pathlib import Path

sys.path.insert(0, str(Path("tests").resolve()))
import test_blind_guess_empirical as tb

course = tb.load_course("courses/pde_course.json")

def inspect_item(qid):
    q = next(x for x in course["questions"] if x["id"] == qid)
    opts = [o["content"] for o in q["options"]]
    scores = tb.compute_centroid_scores(opts)
    print(f"\n==================== {qid} ({q.get('competency_id')}) ====================")
    for o, s, opt_obj in zip(opts, scores, q["options"]):
        is_c = opt_obj.get("is_correct")
        mark = " [KEY]" if is_c else "      "
        print(f"{mark} Score: {s:.3f} | {o}")

for qid in ["Q-H03-059", "Q-H01-017", "Q-H06-114", "Q-Hab08-477", "Q-C01-141", "Q-C02-177", "Q-H05-081", "Q-H07-128"]:
    inspect_item(qid)
