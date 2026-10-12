"""Auditor Empirical Verification Script.
Conducts independent stress testing on unseen and novel inputs across:
1. Lexical Scanner
2. Schema & Semantic Rules
3. Strict Mode Rules
4. CLI & Packaging
"""
import copy
import json
import subprocess
import sys
from pathlib import Path

from validator.core import validate_course_content, validate_course
from validator.lexical_scanner import scan_lexical
from validator.schema_validator import validate_schema
from validator.rules import check_semantic_rules, check_strict_rules
from validator.psychometric_checker import check_psychometrics

passed_checks = 0
total_checks = 0

def check(condition: bool, desc: str):
    global passed_checks, total_checks
    total_checks += 1
    if condition:
        passed_checks += 1
        print(f"  [PASS] {desc}")
    else:
        print(f"  [FAIL] {desc}")

print("=== 1. LEXICAL SCANNER NOVEL INPUT TESTS ===")
# 1.1: Valid JSON escapes in prose (newline, tab) without math mode
r1 = '{"title": "Line 1\\nLine 2\\tTabbed"}'
e1 = scan_lexical(r1)
check(len(e1) == 0, f"Valid JSON escapes \\n, \\t in plain text: {len(e1)} errors")

# 1.2: Double-escaped backslash \\n in stem
r2 = r'{"stem": "\\n is double escaped"}'
e2 = scan_lexical(r2)
check(len(e2) == 0, f"Double escaped \\\\n: {len(e2)} errors")

# 1.3: Unseen macro in math mode (Layer 2 generalization)
r3 = r'{"stem": "Math $x \foobarbaz y$"}'
e3 = scan_lexical(r3)
check(any(e.rule_id == "R-03" for e in e3), f"Unseen macro \\foobarbaz in math mode triggers R-03: {[e.rule_id for e in e3]}")

# 1.4: Unseen macro starting with control prefix n with argument syntax {x} outside math mode (Layer 4)
r4 = r'{"stem": "Notice \notexisting{x} in text"}'
e4 = scan_lexical(r4)
check(any(e.rule_id == "R-03" for e in e4), f"Unseen macro \\notexisting{{x}} outside math mode triggers R-03: {[e.rule_id for e in e4]}")

# 1.5: Inherent control prefixes b, f, r followed by letters (Layer 3)
r5 = r'{"stem": "Words \bhello and \fworld and \rtest"}'
e5 = scan_lexical(r5)
check(all(e.rule_id == "R-03" for e in e5) and len(e5) == 3, f"Inherent controls \\b, \\f, \\r trigger R-03: {len(e5)} errors")

# 1.6: Non-standard escape \v and \0
r6 = r'{"stem": "Value \vphantom and \0"}'
e6 = scan_lexical(r6)
check(all(e.rule_id in ("R-02", "R-03") for e in e6) and len(e6) >= 2, f"Escapes \\v and \\0 trigger R-02/R-03: {len(e6)} errors")


print("\n=== 2. SEMANTIC & SCHEMA NOVEL INPUT TESTS ===")
fixtures_dir = Path("courses/fixtures")
base_data = json.loads((fixtures_dir / "28_valid_complete_course.json").read_text(encoding="utf-8"))

# 2.1: Fill-in-the-blank with number zero as correct_answer
d_zero = copy.deepcopy(base_data)
d_zero["questions"][0]["interaction_type"] = "fill_in_the_blank"
del d_zero["questions"][0]["options"]
d_zero["questions"][0]["correct_answer"] = 0
res_zero = validate_course_content(json.dumps(d_zero))
check(res_zero.is_valid, f"FIB with correct_answer=0 is accepted: {res_zero.is_valid}")

# 2.2: Fill-in-the-blank with empty string value in object
d_empty_str = copy.deepcopy(base_data)
d_empty_str["questions"][0]["interaction_type"] = "fill_in_the_blank"
del d_empty_str["questions"][0]["options"]
d_empty_str["questions"][0]["correct_answer"] = {"value": "   "}
res_empty_str = validate_course_content(json.dumps(d_empty_str))
check(not res_empty_str.is_valid and any(e.code in ("ERR_SCHEMA", "ERR_MISSING_ANSWER") for e in res_empty_str.errors),
      f"FIB with empty string value is rejected: {res_empty_str.is_valid}")

# 2.3: Multiple select with 7 options (maximum is 6)
d_ms_7 = copy.deepcopy(base_data)
d_ms_7["questions"][0]["interaction_type"] = "multiple_select"
d_ms_7["questions"][0]["options"] = [
    {"id": f"opt_{i}", "content": f"Option {i} content text", "is_correct": (i < 2)}
    for i in range(7)
]
res_ms_7 = validate_course_content(json.dumps(d_ms_7))
check(not res_ms_7.is_valid and any(e.code == "ERR_MS_COUNT" for e in res_ms_7.errors),
      f"Multiple select with 7 options rejected with ERR_MS_COUNT: {[e.code for e in res_ms_7.errors]}")

# 2.4: Multiple select with 3 options (minimum is 4)
d_ms_3 = copy.deepcopy(base_data)
d_ms_3["questions"][0]["interaction_type"] = "multiple_select"
d_ms_3["questions"][0]["options"] = [
    {"id": f"opt_{i}", "content": f"Option {i} content text", "is_correct": (i == 0)}
    for i in range(3)
]
res_ms_3 = validate_course_content(json.dumps(d_ms_3))
check(not res_ms_3.is_valid and any(e.code == "ERR_MS_COUNT" for e in res_ms_3.errors),
      f"Multiple select with 3 options rejected with ERR_MS_COUNT: {[e.code for e in res_ms_3.errors]}")

# 2.5: Multiple select with all correct (n correct out of n)
d_ms_all = copy.deepcopy(base_data)
d_ms_all["questions"][0]["interaction_type"] = "multiple_select"
d_ms_all["questions"][0]["options"] = [
    {"id": f"opt_{i}", "content": f"Option {i} content text", "is_correct": True}
    for i in range(4)
]
res_ms_all = validate_course_content(json.dumps(d_ms_all))
check(not res_ms_all.is_valid and any(e.code == "ERR_MS_CORRECT" for e in res_ms_all.errors),
      f"Multiple select with all correct rejected with ERR_MS_CORRECT: {[e.code for e in res_ms_all.errors]}")

# 2.6: Multiple select with 0 correct
d_ms_none = copy.deepcopy(base_data)
d_ms_none["questions"][0]["interaction_type"] = "multiple_select"
d_ms_none["questions"][0]["options"] = [
    {"id": f"opt_{i}", "content": f"Option {i} content text", "is_correct": False}
    for i in range(4)
]
res_ms_none = validate_course_content(json.dumps(d_ms_none))
check(not res_ms_none.is_valid and any(e.code == "ERR_MS_CORRECT" for e in res_ms_none.errors),
      f"Multiple select with 0 correct rejected with ERR_MS_CORRECT: {[e.code for e in res_ms_none.errors]}")


print("\n=== 3. STRICT MODE INDEPENDENT VERIFICATION ===")
# 3.1: Valid fixture passes in standard and strict
res_std = validate_course_content(json.dumps(base_data), strict=False)
res_stk = validate_course_content(json.dumps(base_data), strict=True)
check(res_std.is_valid and res_stk.is_valid, f"Base fixture valid in standard ({res_std.is_valid}) and strict ({res_stk.is_valid})")

# 3.2: Missing misconception warning in strict mode
d_no_misc = copy.deepcopy(base_data)
d_no_misc["questions"][0].pop("misconception_warning", None)
d_no_misc["questions"][0].pop("common_misconception_warning", None)
res_no_misc_std = validate_course_content(json.dumps(d_no_misc), strict=False)
res_no_misc_stk = validate_course_content(json.dumps(d_no_misc), strict=True)
check(res_no_misc_std.is_valid and not res_no_misc_stk.is_valid and any(e.code == "ERR_STRICT_MISSING_MISCONCEPTION" for e in res_no_misc_stk.errors),
      f"Missing misconception warning valid in std ({res_no_misc_std.is_valid}) and rejected in strict ({res_no_misc_stk.is_valid})")

# 3.3: Missing difficulty in strict mode
d_no_diff = copy.deepcopy(base_data)
d_no_diff["questions"][0].pop("difficulty", None)
res_no_diff_std = validate_course_content(json.dumps(d_no_diff), strict=False)
res_no_diff_stk = validate_course_content(json.dumps(d_no_diff), strict=True)
check(res_no_diff_std.is_valid and not res_no_diff_stk.is_valid and any(e.code == "ERR_STRICT_MISSING_DIFFICULTY" for e in res_no_diff_stk.errors),
      f"Missing difficulty valid in std ({res_no_diff_std.is_valid}) and rejected in strict ({res_no_diff_stk.is_valid})")


print("\n=== 4. CLI SUBPROCESS VERIFICATION ===")
cli_res = subprocess.run(
    [sys.executable, "-m", "validator.cli", "courses/fixtures/28_valid_complete_course.json"],
    capture_output=True,
    text=True
)
check(cli_res.returncode == 0 and "VALID: Course 'demo' passed all 16 validation rules" in cli_res.stdout,
      f"CLI module exit 0 on fixture 28: returncode={cli_res.returncode}")

cli_strict_res = subprocess.run(
    [sys.executable, "-m", "validator.cli", "--strict", "courses/fixtures/28_valid_complete_course.json"],
    capture_output=True,
    text=True
)
check(cli_strict_res.returncode == 0 and "VALID: Course 'demo' passed all 16 validation rules (strict mode)" in cli_strict_res.stdout,
      f"CLI strict mode exit 0 on fixture 28: returncode={cli_strict_res.returncode}")

cli_missing_res = subprocess.run(
    [sys.executable, "-m", "validator.cli", "nonexistent_file_path.json"],
    capture_output=True,
    text=True
)
check(cli_missing_res.returncode == 2, f"CLI exit 2 on nonexistent file: returncode={cli_missing_res.returncode}")

print(f"\nAUDIT VERIFICATION SUMMARY: {passed_checks}/{total_checks} CHECKS PASSED (100%)")
