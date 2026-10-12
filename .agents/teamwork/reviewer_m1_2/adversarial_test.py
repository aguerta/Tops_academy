"""Adversarial stress-testing suite for Milestone 1 validator."""
import json
import subprocess
import sys
from pathlib import Path

# Explicitly ensure repo root is in sys.path
REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.validator.core import validate_course, validate_course_content
from src.validator.lexical_scanner import scan_lexical
from src.validator.schema_validator import validate_schema
from src.validator.rules import check_semantic_rules
from src.validator.psychometric_checker import check_psychometrics
from src.validator.models import ValidationError, ValidationResult

results = []

def run_test(name, fn):
    try:
        fn()
        results.append((name, "PASS", ""))
        print(f"[PASS] {name}")
    except AssertionError as e:
        results.append((name, "FAIL", str(e)))
        print(f"[FAIL] {name}: {e}")
    except Exception as e:
        results.append((name, "ERROR", str(e)))
        print(f"[ERROR] {name}: {e}")

# ----------------------------------------------------
# 1. Lexical Scanner Stress Tests
# ----------------------------------------------------
def test_unlisted_latex_control_commands():
    # Test commands starting with b, f, n, r, t that might be missing from whitelist
    # \not (starts with \n)
    raw = '{"stem": "Considere \\not = 0"}'
    errs = scan_lexical(raw)
    assert any(e.rule_id == "R-03" for e in errs), f"Failed to detect single backslash \\not: {errs}"

run_test("test_unlisted_latex_control_commands_not", test_unlisted_latex_control_commands)

def test_latex_single_char_commands():
    # In math: \ne (not equal)?
    raw = '{"stem": "x \\ne y"}'
    errs = scan_lexical(raw)
    assert any(e.rule_id == "R-03" for e in errs), f"Failed to detect single backslash \\ne: {errs}"

run_test("test_latex_ne", test_latex_single_char_commands)

def test_latex_in_arrays_and_objects():
    # LaTeX inside deep nested structures (e.g. hints, solution, option content)
    raw = '''{
        "course_id": "test",
        "hints": [
            "Hint 1: \\alpha + \\beta",
            "Hint 2: \\frac{1}{2}"
        ]
    }'''
    errs = scan_lexical(raw)
    codes = [e.rule_id for e in errs]
    assert "R-02" in codes, f"Expected R-02 for \\alpha, got {codes}"
    assert "R-03" in codes, f"Expected R-03 for \\frac, got {codes}"

run_test("test_latex_in_arrays_and_objects", test_latex_in_arrays_and_objects)

def test_escaped_quotes_and_backslashes():
    # Complex escaped string with quotes and backslashes
    raw = r'{"stem": "Text with \" quote and \\ double backslash"}'
    errs = scan_lexical(raw)
    assert len(errs) == 0, f"Expected clean parse for valid escapes, got: {errs}"

run_test("test_escaped_quotes_and_backslashes", test_escaped_quotes_and_backslashes)

def test_unicode_escapes():
    raw_valid = r'{"stem": "\u0041\u0042"}'
    assert len(scan_lexical(raw_valid)) == 0
    raw_invalid = r'{"stem": "\u004G"}'
    errs = scan_lexical(raw_invalid)
    assert any(e.rule_id == "R-01" for e in errs)

run_test("test_unicode_escapes", test_unicode_escapes)

# ----------------------------------------------------
# 2. Psychometric Checker Stress Tests (R-15 & R-16)
# ----------------------------------------------------
def test_psychometrics_boundary_exact_20_percent():
    # Test EXACT 20.0% boundary:
    # Max distractor = 100.
    # len_c = 120. len_c > 1.20 * max_d -> 120 > 120.0 is False!
    # So 120 chars should be allowed.
    # 121 chars should be rejected (>20%).
    data_120 = {
        "course_id": "test",
        "questions": [{
            "id": "Q-1",
            "interaction_type": "multiple_choice_7_options",
            "options": [
                {"content": "a" * 100, "is_correct": False},
                {"content": "a" * 100, "is_correct": False},
                {"content": "a" * 100, "is_correct": False},
                {"content": "a" * 100, "is_correct": False},
                {"content": "a" * 100, "is_correct": False},
                {"content": "a" * 100, "is_correct": False},
                {"content": "a" * 120, "is_correct": True},
            ]
        }]
    }
    errs_120 = check_psychometrics(data_120)
    assert not any(e.rule_id == "R-15" for e in errs_120), f"120 chars should be allowed: {errs_120}"

    data_121 = {
        "course_id": "test",
        "questions": [{
            "id": "Q-1",
            "interaction_type": "multiple_choice_7_options",
            "options": [
                {"content": "a" * 100, "is_correct": False},
                {"content": "a" * 100, "is_correct": False},
                {"content": "a" * 100, "is_correct": False},
                {"content": "a" * 100, "is_correct": False},
                {"content": "a" * 100, "is_correct": False},
                {"content": "a" * 100, "is_correct": False},
                {"content": "a" * 121, "is_correct": True},
            ]
        }]
    }
    errs_121 = check_psychometrics(data_121)
    assert any(e.rule_id == "R-15" for e in errs_121), f"121 chars must trigger R-15: {errs_121}"

run_test("test_psychometrics_boundary_exact_20_percent", test_psychometrics_boundary_exact_20_percent)

def test_psychometrics_boundary_lower_exact_20_percent():
    # Min distractor = 100.
    # len_c = 80. len_c < 0.80 * min_d -> 80 < 80.0 is False!
    # So 80 chars should be allowed.
    # 79 chars should be rejected (<80%).
    data_80 = {
        "course_id": "test",
        "questions": [{
            "id": "Q-1",
            "interaction_type": "multiple_choice_7_options",
            "options": [
                {"content": "a" * 100, "is_correct": False},
                {"content": "a" * 100, "is_correct": False},
                {"content": "a" * 100, "is_correct": False},
                {"content": "a" * 100, "is_correct": False},
                {"content": "a" * 100, "is_correct": False},
                {"content": "a" * 100, "is_correct": False},
                {"content": "a" * 80, "is_correct": True},
            ]
        }]
    }
    errs_80 = check_psychometrics(data_80)
    assert not any(e.rule_id == "R-15" for e in errs_80), f"80 chars should be allowed: {errs_80}"

    data_79 = {
        "course_id": "test",
        "questions": [{
            "id": "Q-1",
            "interaction_type": "multiple_choice_7_options",
            "options": [
                {"content": "a" * 100, "is_correct": False},
                {"content": "a" * 100, "is_correct": False},
                {"content": "a" * 100, "is_correct": False},
                {"content": "a" * 100, "is_correct": False},
                {"content": "a" * 100, "is_correct": False},
                {"content": "a" * 100, "is_correct": False},
                {"content": "a" * 79, "is_correct": True},
            ]
        }]
    }
    errs_79 = check_psychometrics(data_79)
    assert any(e.rule_id == "R-15" for e in errs_79), f"79 chars must trigger R-15: {errs_79}"

run_test("test_psychometrics_boundary_lower_exact_20_percent", test_psychometrics_boundary_lower_exact_20_percent)

def test_psychometrics_r16_exact_25_percent():
    # 4 MC items: exactly 1 item longest (1/4 = 25.0%).
    # R-16 says "more than 25%", so exactly 25.0% should PASS.
    data_25 = {
        "course_id": "test",
        "questions": [
            {
                "id": f"Q-{i}",
                "interaction_type": "multiple_choice_7_options",
                "options": [
                    {"content": "a" * 80, "is_correct": False},
                    {"content": "a" * 120, "is_correct": False},
                    {"content": "a" * 100, "is_correct": False},
                    {"content": "a" * 100, "is_correct": False},
                    {"content": "a" * 100, "is_correct": False},
                    {"content": "a" * 100, "is_correct": False},
                    {"content": "a" * (120 if i == 0 else 100), "is_correct": True},
                ]
            }
            for i in range(4)
        ]
    }
    errs_25 = check_psychometrics(data_25)
    assert not any(e.rule_id == "R-16" for e in errs_25), f"Exactly 25% should pass R-16: {errs_25}"

run_test("test_psychometrics_r16_exact_25_percent", test_psychometrics_r16_exact_25_percent)

def test_psychometrics_ties_for_longest_or_shortest():
    # If all options are equal length (e.g. 100 chars each), correct option is TIED for longest AND tied for shortest!
    data_tied = {
        "course_id": "test_tied",
        "questions": [
            {
                "id": f"Q-{i}",
                "interaction_type": "multiple_choice_7_options",
                "options": [
                    {"content": "a" * 100, "is_correct": False},
                    {"content": "a" * 100, "is_correct": False},
                    {"content": "a" * 100, "is_correct": False},
                    {"content": "a" * 100, "is_correct": False},
                    {"content": "a" * 100, "is_correct": False},
                    {"content": "a" * 100, "is_correct": False},
                    {"content": "a" * 100, "is_correct": True},
                ]
            }
            for i in range(4)
        ]
    }
    errs_tied = check_psychometrics(data_tied)
    assert any(e.rule_id == "R-16" for e in errs_tied), f"All equal lengths should trigger R-16 due to tied longest/shortest: {errs_tied}"

run_test("test_psychometrics_ties_for_longest_or_shortest", test_psychometrics_ties_for_longest_or_shortest)

# ----------------------------------------------------
# 3. Semantic Rules Stress Tests
# ----------------------------------------------------
def test_empty_competency_and_question_lists():
    data = {
        "schema_version": "1.0.0",
        "course_id": "empty",
        "course_title": "Empty Course",
        "description": "A course with no items",
        "language": "es",
        "created_at": "2026-10-11",
        "competencies": [],
        "questions": []
    }
    res = validate_course_content(json.dumps(data))
    assert res.is_valid is False
    assert any(e.rule_id == "R-04" for e in res.errors)

run_test("test_empty_competency_and_question_lists", test_empty_competency_and_question_lists)

def test_fill_in_the_blank_structure():
    fixture_path = REPO_ROOT / "courses" / "fixtures" / "28_valid_complete_course.json"
    with open(fixture_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    fitb_questions = [q for q in data["questions"] if q["interaction_type"] == "fill_in_the_blank"]
    assert len(fitb_questions) > 0, "No FITB questions in fixture 28"
    
    sem_errs = check_semantic_rules(data)
    psy_errs = check_psychometrics(data)
    assert len(sem_errs) == 0, f"Semantic errors on valid course: {sem_errs}"
    assert len(psy_errs) == 0, f"Psychometric errors on valid course: {psy_errs}"

run_test("test_fill_in_the_blank_structure", test_fill_in_the_blank_structure)

def test_fill_in_the_blank_missing_answer():
    course_data = {
        "schema_version": "1.0.0",
        "course_id": "test",
        "course_title": "Test Course",
        "description": "Description 12345",
        "language": "es",
        "created_at": "2026-10-11",
        "competencies": [{"id": "Hab-01", "name": "Hab 01", "category": "Skill", "description": "desc 12345"}],
        "questions": [
            {
                "id": f"Q-{i}",
                "competency_id": "Hab-01",
                "interaction_type": "fill_in_the_blank",
                "stem": "Solve for x: $x + 1 = 2$",
                "hints": ["h1", "h2", "h3"]
                # Missing correct_answer completely!
            }
            for i in range(30)
        ]
    }
    raw = json.dumps(course_data)
    res = validate_course_content(raw)
    assert res.is_valid is False, "Validator should reject questions without correct_answer!"

run_test("test_fill_in_the_blank_missing_answer", test_fill_in_the_blank_missing_answer)

def test_missing_category_or_unrecognized_category():
    data = {
        "competencies": [
            {"id": "Hab-01", "name": "Skill 1", "category": "UnknownCategory", "description": "desc 123"}
        ],
        "questions": [
            {"id": f"Q-{i}", "competency_id": "Hab-01", "interaction_type": "fill_in_the_blank", "hints": ["h1", "h2", "h3"]}
            for i in range(10)
        ]
    }
    sch_errs = validate_schema(data)
    assert any(e.rule_id == "R-04" for e in sch_errs)

run_test("test_missing_category_or_unrecognized_category", test_missing_category_or_unrecognized_category)

# ----------------------------------------------------
# 4. Integrity Check Tests
# ----------------------------------------------------
def test_integrity_no_hardcoded_fixture_names_in_source():
    src_dir = REPO_ROOT / "src" / "validator"
    for py_file in src_dir.glob("*.py"):
        content = py_file.read_text(encoding="utf-8")
        assert "01_original_example_unmodified" not in content, f"Hardcoded fixture in {py_file}"
        assert "28_valid_complete_course" not in content, f"Hardcoded fixture in {py_file}"
        assert "fake" not in content.lower() or "mock" not in content.lower(), f"Suspicious dummy keyword in {py_file}"

run_test("test_integrity_no_hardcoded_fixture_names_in_source", test_integrity_no_hardcoded_fixture_names_in_source)

# ----------------------------------------------------
# Summary
# ----------------------------------------------------
print("\n" + "="*50)
print(f"Total tests: {len(results)}")
print(f"Passed: {sum(1 for _, s, _ in results if s == 'PASS')}")
print(f"Failed: {sum(1 for _, s, _ in results if s != 'PASS')}")
for name, status, msg in results:
    if status != "PASS":
        print(f"  FAILED: {name} -> {msg}")
