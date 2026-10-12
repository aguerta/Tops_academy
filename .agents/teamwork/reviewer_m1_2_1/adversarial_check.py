import json
import subprocess
import sys
from pathlib import Path

# Add repo root to sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from validator.lexical_scanner import scan_lexical
from validator.core import validate_course_content, validate_course
from validator.schema_validator import validate_schema
from validator.rules import check_semantic_rules, check_strict_rules
from validator.psychometric_checker import check_psychometrics

# 1. Test all 16 prompt LaTeX commands
cmds = [
    r"\ne", r"\not", r"\norm", r"\boxed", r"\therefore", r"\thickspace",
    r"\textcolor", r"\bigcap", r"\bigcup", r"\bigoplus", r"\bigotimes",
    r"\rank", r"\bm", r"\tr", r"\ref", r"\newline"
]

print("=== 1. Checking 16 LaTeX commands from dispatch ===")
for cmd in cmds:
    raw = '{"stem": "Formula: ' + cmd + '{x}"}'
    errs = scan_lexical(raw)
    r03_errs = [e for e in errs if e.rule_id == "R-03"]
    assert len(r03_errs) > 0, f"LaTeX command {cmd} was not caught as R-03! Got: {[e.to_dict() for e in errs]}"
    print(f"  [OK] {cmd} caught as R-03: {r03_errs[0].message}")

# 2. Test multiple_select options enforcement (R-12)
print("=== 2. Checking multiple_select options enforcement (R-12) ===")
# Missing options
course_ms_missing = {
    "schema_version": "1.0.0",
    "course_id": "c1",
    "course_title": "Course 1",
    "description": "Course 1 description",
    "language": "es",
    "created_at": "2026-10-11T00:00:00Z",
    "competencies": [{"id": "Hab-01", "name": "Skill 1", "category": "Skill", "description": "Skill description"}],
    "questions": [
        {
            "id": "Q-001",
            "competency_id": "Hab-01",
            "interaction_type": "multiple_select",
            "stem": "Select all that apply",
            "hints": ["h1", "h2", "h3"]
        }
    ]
}
res_ms_missing = validate_course_content(json.dumps(course_ms_missing))
assert not res_ms_missing.is_valid
ms_err_codes = [e.code for e in res_ms_missing.errors]
print(f"  [OK] multiple_select missing options rejected with: {ms_err_codes}")
assert "ERR_SCHEMA" in ms_err_codes or "ERR_MS_COUNT" in ms_err_codes

# Null options
course_ms_null = json.loads(json.dumps(course_ms_missing))
course_ms_null["questions"][0]["options"] = None
res_ms_null = validate_course_content(json.dumps(course_ms_null))
assert not res_ms_null.is_valid
print(f"  [OK] multiple_select null options rejected with: {[e.code for e in res_ms_null.errors]}")

# Options < 4 (e.g. 3)
course_ms_3 = json.loads(json.dumps(course_ms_missing))
course_ms_3["questions"][0]["options"] = [
    {"id": "o1", "content": "1", "is_correct": True},
    {"id": "o2", "content": "2", "is_correct": False},
    {"id": "o3", "content": "3", "is_correct": False},
]
res_ms_3 = validate_course_content(json.dumps(course_ms_3))
assert not res_ms_3.is_valid
assert any(e.code == "ERR_MS_COUNT" for e in res_ms_3.errors)
print(f"  [OK] multiple_select 3 options rejected with ERR_MS_COUNT")

# Options > 6 (e.g. 7)
course_ms_7 = json.loads(json.dumps(course_ms_missing))
course_ms_7["questions"][0]["options"] = [
    {"id": f"o{i}", "content": f"{i}", "is_correct": i == 1}
    for i in range(1, 8)
]
res_ms_7 = validate_course_content(json.dumps(course_ms_7))
assert not res_ms_7.is_valid
assert any(e.code == "ERR_MS_COUNT" for e in res_ms_7.errors)
print(f"  [OK] multiple_select 7 options rejected with ERR_MS_COUNT")

# 3. Test correct_answer enforced on fill_in_the_blank
print("=== 3. Checking fill_in_the_blank correct_answer enforcement ===")
course_fib_missing = {
    "schema_version": "1.0.0",
    "course_id": "c1",
    "course_title": "Course 1",
    "description": "Course 1 description",
    "language": "es",
    "created_at": "2026-10-11T00:00:00Z",
    "competencies": [{"id": "Hab-01", "name": "Skill 1", "category": "Skill", "description": "Skill description"}],
    "questions": [
        {
            "id": "Q-001",
            "competency_id": "Hab-01",
            "interaction_type": "fill_in_the_blank",
            "stem": "Enter answer",
            "hints": ["h1", "h2", "h3"]
        }
    ]
}
res_fib_missing = validate_course_content(json.dumps(course_fib_missing))
assert not res_fib_missing.is_valid
fib_err_codes = [e.code for e in res_fib_missing.errors]
print(f"  [OK] fill_in_the_blank missing correct_answer rejected with: {fib_err_codes}")
assert "ERR_SCHEMA" in fib_err_codes or "ERR_MISSING_ANSWER" in fib_err_codes

# Empty string
course_fib_empty_str = json.loads(json.dumps(course_fib_missing))
course_fib_empty_str["questions"][0]["correct_answer"] = ""
res_fib_empty_str = validate_course_content(json.dumps(course_fib_empty_str))
assert not res_fib_empty_str.is_valid
print(f"  [OK] fill_in_the_blank empty string rejected")

# Empty dict {}
course_fib_empty_dict = json.loads(json.dumps(course_fib_missing))
course_fib_empty_dict["questions"][0]["correct_answer"] = {}
res_fib_empty_dict = validate_course_content(json.dumps(course_fib_empty_dict))
assert not res_fib_empty_dict.is_valid
print(f"  [OK] fill_in_the_blank empty dict {{}} rejected")

# Empty list []
course_fib_empty_list = json.loads(json.dumps(course_fib_missing))
course_fib_empty_list["questions"][0]["correct_answer"] = []
res_fib_empty_list = validate_course_content(json.dumps(course_fib_empty_list))
assert not res_fib_empty_list.is_valid
print(f"  [OK] fill_in_the_blank empty list [] rejected")

# Dict with empty expression and empty value
course_fib_empty_val = json.loads(json.dumps(course_fib_missing))
course_fib_empty_val["questions"][0]["correct_answer"] = {"expression": "   "}
res_fib_empty_val = validate_course_content(json.dumps(course_fib_empty_val))
assert not res_fib_empty_val.is_valid
print(f"  [OK] fill_in_the_blank whitespace expression rejected")

# 4. Packaging and entry point verification
print("=== 4. Checking packaging and entrypoint imports ===")
import validator
from validator.core import validate_course as vc_rel
from validator.cli import main as cli_main
print("  [OK] validator package imported successfully via top-level 'validator'")

# 5. Strict mode testing
print("=== 5. Checking --strict mode rules ===")
path_28 = Path("courses/fixtures/28_valid_complete_course.json")
data_28 = json.loads(path_28.read_text(encoding="utf-8"))
res_28_strict = validate_course_content(json.dumps(data_28), strict=True)
assert res_28_strict.is_valid, f"Fixture 28 failed strict mode: {res_28_strict.errors}"
print("  [OK] Fixture 28 passes strict mode")

# Mutate to missing misconception
data_28_no_misc = json.loads(json.dumps(data_28))
data_28_no_misc["questions"][0].pop("misconception_warning", None)
data_28_no_misc["questions"][0].pop("common_misconception_warning", None)
res_no_misc_normal = validate_course_content(json.dumps(data_28_no_misc), strict=False)
assert res_no_misc_normal.is_valid, "Normal mode should tolerate missing misconception"
res_no_misc_strict = validate_course_content(json.dumps(data_28_no_misc), strict=True)
assert not res_no_misc_strict.is_valid
assert any(e.code == "ERR_STRICT_MISSING_MISCONCEPTION" for e in res_no_misc_strict.errors)
print("  [OK] Strict mode enforces misconception warning (ERR_STRICT_MISSING_MISCONCEPTION)")

# Mutate to missing difficulty
data_28_no_diff = json.loads(json.dumps(data_28))
data_28_no_diff["questions"][0].pop("difficulty", None)
res_no_diff_normal = validate_course_content(json.dumps(data_28_no_diff), strict=False)
assert res_no_diff_normal.is_valid
res_no_diff_strict = validate_course_content(json.dumps(data_28_no_diff), strict=True)
assert not res_no_diff_strict.is_valid
assert any(e.code == "ERR_STRICT_MISSING_DIFFICULTY" for e in res_no_diff_strict.errors)
print("  [OK] Strict mode enforces difficulty (ERR_STRICT_MISSING_DIFFICULTY)")

print("\nALL ADVERSARIAL CHECKS PASSED PERFECTLY!")
