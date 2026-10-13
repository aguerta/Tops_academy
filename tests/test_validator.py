"""Comprehensive Consolidated Test Suite for Exercise Bank Format Validator.

Consolidates:
1. Lexical Scanner Tests (control characters, silent corruption, raw newlines, obscure LaTeX escapes)
2. Schema & Structure Validator Tests (root structure, required metadata, question schemas)
3. Semantic & Pedagogical Rules Tests (competencies, quotas, question types, hint counts)
4. Psychometric Anti-Giveaway Tests (item length bounding R-15, course distribution R-16)
5. Packaging, CLI & Strict Mode Tests (module entrypoint, strict mode flags, import isolation)
6. Challenger Edge Cases & Scale Tests (massive courses 450-1500 items, deep graphs, Unicode/BOM)
"""
from __future__ import annotations

import copy
import json
import math
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

import pytest

# Ensure repo root and src are on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "src"
for p in [str(SRC_DIR), str(REPO_ROOT)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from validator.cli import main as cli_main
from validator.core import validate_course, validate_course_content
from validator.lexical_scanner import scan_lexical
from validator.models import ValidationError, ValidationResult
from validator.psychometric_checker import check_psychometrics
from validator.rules import check_semantic_rules, check_strict_rules, check_extended_quality_rules
from validator.schema_validator import validate_schema

FIXTURES_DIR = (REPO_ROOT / "courses" / "fixtures") if (REPO_ROOT / "courses" / "fixtures").exists() else (REPO_ROOT / "tests" / "validator" / "fixtures")


# =============================================================================
# 1. 28-Fixture Catalog Matrix Tests
# =============================================================================

FIXTURE_CASES = [
    ("01_original_example_unmodified.json", 1, ["[ERR_INVALID_JSON]", "[ERR_LATEX_SYNTAX]"]),
    ("02_syntax_malformed_json.json", 1, ["[ERR_INVALID_JSON]"]),
    ("03_syntax_unescaped_quotes.json", 1, ["[ERR_INVALID_JSON]"]),
    ("04_syntax_raw_newlines.json", 1, ["[ERR_INVALID_JSON]"]),
    ("05_latex_invalid_escape.json", 1, [r"[ERR_LATEX_SYNTAX] Invalid escape sequence '\alpha'"]),
    ("06_latex_silent_corruption_tab.json", 1, [r"[ERR_LATEX_CORRUPT] LaTeX corruption detected: '\tau'"]),
    ("07_latex_silent_corruption_formfeed.json", 1, [r"[ERR_LATEX_CORRUPT] LaTeX corruption detected: '\frac'"]),
    ("08_latex_silent_corruption_backspace.json", 1, [r"[ERR_LATEX_CORRUPT] LaTeX corruption detected: '\beta'"]),
    ("09_schema_missing_course_title.json", 1, ["[ERR_SCHEMA] Missing required top-level field 'course_title'"]),
    ("10_duplicate_competency_ids.json", 1, ["[ERR_DUP_COMPETENCY] Duplicate competency ID found: 'Hab-01'"]),
    ("11_duplicate_question_ids.json", 1, ["[ERR_DUP_QUESTION] Duplicate question ID found: 'Q-001'"]),
    ("12_missing_competency_reference.json", 1, ["[ERR_MISSING_COMPETENCY] Question 'Q-001' references unknown competency 'Hab-99'"]),
    ("13_skill_29_questions.json", 1, ["[ERR_COUNT_SKILL] Competency 'Hab-01' (category 'Skill') has 29 questions; minimum required is 30"]),
    ("14_concept_19_questions.json", 1, ["[ERR_COUNT_CONCEPT] Competency 'C-01' (category 'Concept') has 19 questions; minimum required is 20"]),
    ("15_fact_19_questions.json", 1, ["[ERR_COUNT_CONCEPT] Competency 'H-01' (category 'Fact') has 19 questions; minimum required is 20"]),
    ("16_mc_6_options.json", 1, ["[ERR_MC_COUNT] Question 'Q-001' has 6 options; multiple-choice items must have exactly 7 options"]),
    ("17_mc_8_options.json", 1, ["[ERR_MC_COUNT] Question 'Q-001' has 8 options; multiple-choice items must have exactly 7 options"]),
    ("18_mc_0_correct.json", 1, ["[ERR_MC_CORRECT] Question 'Q-001' has 0 correct options"]),
    ("19_mc_2_correct.json", 1, ["[ERR_MC_CORRECT] Question 'Q-001' has 2 correct options"]),
    ("20_ms_all_correct.json", 1, ["[ERR_MS_CORRECT] Question 'Q-001' has 5 correct options out of 5; multiple-select items must have between 1 and n-1"]),
    ("21_ms_0_correct.json", 1, ["[ERR_MS_CORRECT] Question 'Q-001' has 0 correct options out of 5"]),
    ("22_hints_2_hints.json", 1, ["[ERR_HINT_COUNT] Question 'Q-001' has 2 hints; must have between 3 and 5 hints"]),
    ("23_hints_6_hints.json", 1, ["[ERR_HINT_COUNT] Question 'Q-001' has 6 hints; must have between 3 and 5 hints"]),
    ("24_giveaway_item_too_long.json", 1, ["[ERR_GIVEAWAY_ITEM] Question 'Q-001': correct option length"]),
    ("25_giveaway_item_too_short.json", 1, ["[ERR_GIVEAWAY_ITEM] Question 'Q-001': correct option length"]),
    ("26_giveaway_course_longest_30pct.json", 1, ["[ERR_GIVEAWAY_COURSE] Course 'demo': correct option is longest in 3/10 (30.0%)"]),
    ("27_giveaway_course_shortest_30pct.json", 1, ["[ERR_GIVEAWAY_COURSE] Course 'demo': correct option is shortest in 3/10 (30.0%)"]),
    ("28_valid_complete_course.json", 0, []),
]


@pytest.fixture
def base_valid_course() -> dict:
    """Loads the canonical passing 30-item course fixture."""
    path = FIXTURES_DIR / "28_valid_complete_course.json"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("filename, expected_exit, substrings", FIXTURE_CASES)
def test_all_fixtures_programmatic(filename: str, expected_exit: int, substrings: list[str]) -> None:
    """Verifies that each fixture produces the expected exit code and diagnostics programmatically."""
    fixture_path = FIXTURES_DIR / filename
    assert fixture_path.exists(), f"Fixture file not found: {fixture_path}"

    result: ValidationResult = validate_course(str(fixture_path))

    if expected_exit == 0:
        assert result.is_valid is True, f"Fixture {filename} expected valid, got errors: {result.errors}"
        assert len(result.errors) == 0
    else:
        assert result.is_valid is False, f"Fixture {filename} expected invalid, but passed validation"
        assert len(result.errors) > 0

        # Check required diagnostic substrings
        reported_msgs = [f"[{e.code}] {e.message}" for e in result.errors]
        all_reported = " \n ".join(reported_msgs)

        for sub in substrings:
            assert any(sub in rep for rep in reported_msgs) or (sub in all_reported), (
                f"Fixture {filename}: Expected diagnostic substring '{sub}' not found in:\n{all_reported}"
            )


@pytest.mark.parametrize("filename, expected_exit, substrings", FIXTURE_CASES)
def test_all_fixtures_cli(filename: str, expected_exit: int, substrings: list[str], capsys: pytest.CaptureFixture[str]) -> None:
    """Verifies that CLI invocation matches exit code and stderr/stdout output in-memory."""
    fixture_path = FIXTURES_DIR / filename
    assert fixture_path.exists(), f"Fixture file not found: {fixture_path}"

    exit_code = cli_main([str(fixture_path)])
    captured = capsys.readouterr()

    assert exit_code == expected_exit, (
        f"Fixture {filename}: CLI returned {exit_code}, expected {expected_exit}.\n"
        f"STDOUT:\n{captured.out}\nSTDERR:\n{captured.err}"
    )

    combined_output = captured.out + "\n" + captured.err
    for sub in substrings:
        assert sub in combined_output, (
            f"Fixture {filename}: CLI output missing expected substring '{sub}'.\n"
            f"Output was:\n{combined_output}"
        )


def test_cli_exit_code_2_on_missing_file(capsys: pytest.CaptureFixture[str]) -> None:
    """CLI must return exit code 2 when a file does not exist."""
    missing_file = REPO_ROOT / "courses" / "non_existent_file_xyz_123.json"
    exit_code = cli_main([str(missing_file)])
    captured = capsys.readouterr()
    assert exit_code == 2
    assert "[IO ERROR]" in captured.err or "Path does not exist" in captured.err or "File not found" in (captured.out + captured.err)


def test_cli_json_output_mode(capsys: pytest.CaptureFixture[str]) -> None:
    """CLI --json flag must output valid machine-readable JSON containing is_valid or all_valid."""
    fixture_path = FIXTURES_DIR / "28_valid_complete_course.json"
    exit_code = cli_main(["--json", str(fixture_path)])
    captured = capsys.readouterr()
    assert exit_code == 0
    parsed = json.loads(captured.out)
    assert parsed.get("all_valid") is True or parsed.get("is_valid") is True
    assert parsed.get("exit_code") == 0


def test_cli_directory_mode(capsys: pytest.CaptureFixture[str]) -> None:
    """CLI should support directory validation argument."""
    exit_code = cli_main([str(FIXTURES_DIR)])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "VALID: Course 'demo' passed all 16 validation rules" in captured.out
    assert "[VALIDATION FAILURE]" in captured.out


# =============================================================================
# 2. Lexical Scanner and LaTeX Escape Tests
# =============================================================================

class TestLexicalScanner:
    """Tests for raw string scanning and escape sequences."""

    def test_lexical_scanner_clean_latex(self) -> None:
        """Valid double-escaped LaTeX strings must produce zero lexical errors."""
        clean = '{"stem": "Calcular $\\\\alpha + \\\\beta = \\\\frac{1}{2}$ y $\\\\tau_0$"}'
        errors = scan_lexical(clean)
        assert len(errors) == 0

    def test_lexical_scanner_invalid_escapes(self) -> None:
        """Single backslash LaTeX like \\alpha must trigger ERR_LATEX_SYNTAX / R-02."""
        bad = r'{"stem": "Considere $\Delta$ y $\sigma$ y $\lambda$"}'
        errors = scan_lexical(bad)
        assert any(e.rule_id == "R-02" and r"\Delta" in e.message for e in errors)
        assert any(e.rule_id == "R-02" and r"\sigma" in e.message for e in errors)
        assert any(e.rule_id == "R-02" and r"\lambda" in e.message for e in errors)

    def test_lexical_scanner_control_char_corruption(self) -> None:
        """Single backslashes before LaTeX keywords producing control chars must trigger R-03."""
        bad = r'{"stem": "Evaluar $\text{tr}(A)$, $\frac{1}{2}$, $\nu$, $\tau$, $\beta$, $\theta$"}'
        errors = scan_lexical(bad)
        codes = {e.rule_id for e in errors}
        assert "R-03" in codes
        assert any(r"\text" in e.message for e in errors)
        assert any(r"\frac" in e.message for e in errors)
        assert any(r"\tau" in e.message for e in errors)
        assert any(r"\beta" in e.message for e in errors)

    def test_lexical_scanner_raw_newlines(self) -> None:
        """Literal unescaped newlines inside strings must trigger R-01."""
        bad = '{"stem": "Linea uno\nLinea dos"}'
        errors = scan_lexical(bad)
        assert any(e.rule_id == "R-01" and "Unescaped raw newline" in e.message for e in errors)


    @pytest.mark.parametrize("macro", [
        r"\\iint", r"\\oint", r"\\nabla", r"\\partial", r"\\approx",
        r"\\equiv", r"\\le", r"\\ge", r"\\sum_{k=1}^n", r"\\prod_{i=1}^m"
    ])
    def test_double_escaped_obscure_macros_pass(self, macro: str) -> None:
        content = f'{{"equation": "{macro}"}}'
        errs = scan_lexical(content)
        assert len(errs) == 0

    def test_complex_multiline_cases_environment_passes(self) -> None:
        raw_payload = r'{"solution": "f(x) = \\begin{cases} x^2 & x \\ge 0 \\\\ -x & x < 0 \\end{cases}"}'
        errs = scan_lexical(raw_payload)
        assert len(errs) == 0

    def test_single_backslash_escaped_curly_brace_detected(self) -> None:
        bad_json = r'{"math": "\{1, 2, 3\}"}'
        errs = scan_lexical(bad_json)
        assert any(e.code == "ERR_LATEX_SYNTAX" for e in errs)


# =============================================================================
# 3. Packaging, Entry Points, and Strict Mode Tests
# =============================================================================

class TestPackagingAndCLI:
    """Packaging isolation, console entrypoints, and --strict flag tests."""

    def test_import_validator_outside_repo(self, tmp_path: Path) -> None:
        """Verifies that validator can be imported from an external working directory."""
        repo_src = str(REPO_ROOT / "src")
        test_script = f"""
import sys
sys.path.insert(0, {repo_src!r})
import validator
from validator.core import validate_course
from validator.cli import main
print("IMPORT_OK")
"""
        proc = subprocess.run(
            [sys.executable, "-c", test_script],
            cwd=str(tmp_path),
            capture_output=True,
            text=True
        )
        assert proc.returncode == 0, f"External import failed: {proc.stderr}"
        assert "IMPORT_OK" in proc.stdout

    def test_cli_entrypoint_execution(self) -> None:
        """Verifies that validate-course console script or module executes fixture 28."""
        fixture_path = FIXTURES_DIR / "28_valid_complete_course.json"
        proc_module = subprocess.run(
            [sys.executable, "-m", "validator.cli", str(fixture_path)],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT)
        )
        assert proc_module.returncode == 0
        assert "VALID" in proc_module.stdout

    def test_strict_flag_semantics(self) -> None:
        """Verifies that --strict enforces solutions and misconception warnings."""
        fixture_path = FIXTURES_DIR / "28_valid_complete_course.json"
        data = json.loads(fixture_path.read_text(encoding="utf-8"))

        assert validate_course_content(json.dumps(data), strict=False).is_valid is True
        assert validate_course_content(json.dumps(data), strict=True).is_valid is True

        data_no_sol = copy.deepcopy(data)
        data_no_sol["questions"][0].pop("detailed_solution", None)
        data_no_sol["questions"][0].pop("solution", None)

        res_std = validate_course_content(json.dumps(data_no_sol), strict=False)
        assert res_std.is_valid is True

        res_strict = validate_course_content(json.dumps(data_no_sol), strict=True)
        assert res_strict.is_valid is False
        assert any(e.code == "ERR_STRICT_MISSING_SOLUTION" for e in res_strict.errors)


# =============================================================================
# 4. Question Types and Semantic Edge Cases
# =============================================================================

class TestInteractionTypesAndEdgeCases:
    """Stress tests across MC7, MS, and FIB question types."""

    def test_mc_empty_options_array_rejected(self, base_valid_course: dict) -> None:
        course = copy.deepcopy(base_valid_course)
        course["questions"][0]["options"] = []
        result = validate_course_content(json.dumps(course))
        assert not result.is_valid
        assert any("options" in e.message.lower() or e.code == "ERR_MC_COUNT" for e in result.errors)

    def test_mc_null_options_rejected(self, base_valid_course: dict) -> None:
        course = copy.deepcopy(base_valid_course)
        course["questions"][0]["options"] = None
        result = validate_course_content(json.dumps(course))
        assert not result.is_valid

    def test_ms_boundary_options(self, base_valid_course: dict) -> None:
        course = copy.deepcopy(base_valid_course)
        q = course["questions"][0]
        q["interaction_type"] = "multiple_select"

        # 3 options: fails (must be 4-6)
        q["options"] = [
            {"id": "opt_1", "content": "Opt 1", "is_correct": True},
            {"id": "opt_2", "content": "Opt 2", "is_correct": False, "error_rationale": "Razonamiento del error 2"},
            {"id": "opt_3", "content": "Opt 3", "is_correct": False, "error_rationale": "Razonamiento del error 3"},
        ]
        res3 = validate_course_content(json.dumps(course))
        assert not res3.is_valid
        assert any(e.code == "ERR_MS_COUNT" for e in res3.errors)

        # 4 options: passes
        q["options"].append({"id": "opt_4", "content": "Opt 4", "is_correct": False, "error_rationale": "Razonamiento del error 4"})
        res4 = validate_course_content(json.dumps(course))
        assert res4.is_valid

        # 6 options: passes
        q["options"].append({"id": "opt_5", "content": "Opt 5", "is_correct": False, "error_rationale": "Razonamiento del error 5"})
        q["options"].append({"id": "opt_6", "content": "Opt 6", "is_correct": False, "error_rationale": "Razonamiento del error 6"})
        res6 = validate_course_content(json.dumps(course))
        assert res6.is_valid

        # 7 options: fails
        q["options"].append({"id": "opt_7", "content": "Opt 7", "is_correct": False, "error_rationale": "Razonamiento del error 7"})
        res7 = validate_course_content(json.dumps(course))
        assert not res7.is_valid

    def test_fn_fill_in_the_blank_validation(self, base_valid_course: dict) -> None:
        course = copy.deepcopy(base_valid_course)
        q = course["questions"][0]
        q["interaction_type"] = "fill_in_the_blank"
        del q["options"]
        q["correct_answer"] = "x^2 + 2x + 1"
        res = validate_course_content(json.dumps(course))
        assert res.is_valid

        # Missing correct_answer: invalid
        del q["correct_answer"]
        res_fail = validate_course_content(json.dumps(course))
        assert not res_fail.is_valid


# =============================================================================
# 5. Psychometrics & Anti-Giveaway Precision Bounds
# =============================================================================

class TestPsychometricsAndAntiGiveaway:
    """Anti-giveaway bounds at precision limits."""

    def test_item_symmetry_checker(self) -> None:
        opts_symmetric = [
            {"id": "opt_1", "content": "a" * 80, "is_correct": False},
            {"id": "opt_2", "content": "a" * 90, "is_correct": False},
            {"id": "opt_3", "content": "a" * 100, "is_correct": False},
            {"id": "opt_4", "content": "a" * 110, "is_correct": False},
            {"id": "opt_5", "content": "a" * 120, "is_correct": False},
            {"id": "opt_6", "content": "a" * 130, "is_correct": False},
            {"id": "opt_c", "content": "a" * 105, "is_correct": True},
        ]
        q_sym = {"id": "Q-001", "interaction_type": "multiple_choice_7_options", "options": opts_symmetric}
        assert len(check_psychometrics({"course_id": "demo", "questions": [q_sym]})) == 0

    def test_psychometric_r15_boundaries(self, base_valid_course: dict) -> None:
        # Correct answer exactly 1.20 * max(D)
        course = copy.deepcopy(base_valid_course)
        q = course["questions"][0]
        # max distractor = 100 -> correct answer 120 (ratio 1.20)
        q["options"] = [
            {"id": "opt_1", "content": "x" * 100, "is_correct": False, "error_rationale": "Razonamiento del error 1"},
            {"id": "opt_2", "content": "x" * 90, "is_correct": False, "error_rationale": "Razonamiento del error 2"},
            {"id": "opt_3", "content": "x" * 95, "is_correct": False, "error_rationale": "Razonamiento del error 3"},
            {"id": "opt_4", "content": "x" * 92, "is_correct": False, "error_rationale": "Razonamiento del error 4"},
            {"id": "opt_5", "content": "x" * 88, "is_correct": False, "error_rationale": "Razonamiento del error 5"},
            {"id": "opt_6", "content": "x" * 85, "is_correct": False, "error_rationale": "Razonamiento del error 6"},
            {"id": "opt_c", "content": "x" * 120, "is_correct": True},
        ]
        res_pass = validate_course_content(json.dumps(course))
        assert res_pass.is_valid

        # Correct answer 121 (ratio 1.21 > 1.20) -> fails R-15
        q["options"][-1]["content"] = "x" * 121
        res_fail = validate_course_content(json.dumps(course))
        assert not res_fail.is_valid
        assert any(e.code == "ERR_GIVEAWAY_ITEM" for e in res_fail.errors)

    def test_psychometric_r16_course_distribution(self, base_valid_course: dict) -> None:
        course = copy.deepcopy(base_valid_course)
        # 30 items: 7 items longest = 7/30 = 23.33% <= 25% -> pass
        # 8 items longest = 8/30 = 26.67% > 25% -> fail
        for i in range(8):
            q = course["questions"][i]
            # Make correct option longest
            for opt in q["options"]:
                if opt["is_correct"]:
                    opt["content"] = "Longest correct answer content " + ("z" * 150)
                else:
                    opt["content"] = "Short distractor " + ("z" * 40)

        res = validate_course_content(json.dumps(course))
        assert not res.is_valid
        assert any(e.code == "ERR_GIVEAWAY_COURSE" for e in res.errors)


# =============================================================================
# 6. Coordinate Graph Models & Vector Specs
# =============================================================================

class TestCoordinateGraphs:
    """Coordinate graphing models and point/curve validation."""

    def test_deep_graphs_multiple_curves_and_asymptotes(self, base_valid_course: dict) -> None:
        course = copy.deepcopy(base_valid_course)
        q = course["questions"][0]
        q["graph"] = {
            "type": "coordinate_plane",
            "x_range": [-10, 10],
            "y_range": [-10, 10],
            "curves": [
                {"id": "c1", "fn": "x^2 - 4", "color": "#1865f2", "stroke_width": 2, "style": "solid"},
                {"id": "c2", "fn": "2*x + 1", "color": "#008800", "stroke_width": 2, "style": "dashed"},
                {"id": "c3", "fn": "3", "color": "#cc0000", "stroke_width": 1.5, "style": "dotted", "label": "Asintota x=3"}
            ],
            "points": [
                {"x": 2.0, "y": 0.0, "label": "(2, 0)", "color": "#1865f2", "style": "closed"},
                {"x": -2.0, "y": 0.0, "label": "(-2, 0)", "color": "#1865f2", "style": "open"}
            ],
            "grid": True,
            "axes": True
        }
        res = validate_course_content(json.dumps(course))
        assert res.is_valid, f"Deep graph failed: {res.errors}"

    def test_graph_invalid_curve_schema_rejected(self, base_valid_course: dict) -> None:
        course = copy.deepcopy(base_valid_course)
        course["questions"][0]["graph"] = {
            "x_range": ["invalid_range", 10],  # Must be numbers
            "curves": [{"fn": 12345}]  # fn must be string
        }
        res = validate_course_content(json.dumps(course))
        assert not res.is_valid


# =============================================================================
# 7. Scale, Multilingual, and Robustness
# =============================================================================

class TestScaleAndRobustness:
    """Performance benchmarks, massive courses, and Unicode robustness."""

    def test_scale_450_questions_r3_benchmark(self, base_valid_course: dict) -> None:
        """Requirement R3 scale: 15 competencies x 30 questions = 450 items under 3.0s."""
        course = copy.deepcopy(base_valid_course)
        course["course_id"] = "scale-r3-course"
        course["course_title"] = "Scale Course 15 Competencies"
        course["competencies"] = [
            {
                "id": f"Hab-{i:02d}",
                "name": f"Competencia {i:02d}",
                "category": "Skill",
                "description": f"Descripcion {i:02d}",
                "mastery_target": 100,
            }
            for i in range(1, 16)
        ]
        template_q = base_valid_course["questions"][0]
        all_q = []
        counter = 1
        for comp in course["competencies"]:
            for j in range(30):
                q = copy.deepcopy(template_q)
                q["id"] = f"Q-{counter:04d}"
                q["competency_id"] = comp["id"]
                all_q.append(q)
                counter += 1
        course["questions"] = all_q

        t0 = time.perf_counter()
        res = validate_course_content(json.dumps(course))
        elapsed = time.perf_counter() - t0

        assert res.is_valid, f"Scale course failed: {res.errors}"
        assert elapsed < 3.0, f"450 questions took {elapsed:.2f}s, expected < 3.0s"

    def test_multilingual_and_utf8_bom(self, base_valid_course: dict) -> None:
        course = copy.deepcopy(base_valid_course)
        course["language"] = "es"
        course["course_title"] = "Análisis Matemático y Ecuaciones Diferenciales: Ñandú & Möbius"
        res = validate_course_content(json.dumps(course))
        assert res.is_valid

        # BOM is rejected as invalid JSON per RFC 8259
        raw_bom = "\ufeff" + json.dumps(course)
        res_bom = validate_course_content(raw_bom)
        assert not res_bom.is_valid
        assert any(e.code == "ERR_INVALID_JSON" and "BOM" in e.message for e in res_bom.errors)

    @pytest.mark.parametrize("bad_root", ["", "   ", "[]", "123", '"str"', "true"])
    def test_malformed_roots_handled_cleanly(self, bad_root: str) -> None:
        res = validate_course_content(bad_root)
        assert not res.is_valid
        assert len(res.errors) > 0


# =============================================================================
# 8. Extended Quality Rules Tests (R-17, R-18, R-19, R-20, R-22)
# =============================================================================

class TestExtendedQualityRules:
    """Verifies extended quality rules:
    - R-17: ERR_PLACEHOLDER_RATIONALE (non-placeholder, non-empty error rationales)
    - R-18: ERR_META_GIVEAWAY (no psychometric error meta-info in visible options)
    - R-19: ERR_ANSWER_LEAK (no leaked answer assignment in fill_in_the_blank stems)
    - R-20: ERR_LATEX_SYNTAX (balanced $, no $$$, no {{}}, no unreplaced {var})
    - R-22: ERR_MS_MISSING_RATIONALE (mandatory error rationales in multiple_select)
    """

    # --- Rule R-17 Tests ---

    def test_r17_mc7_valid_rationales_pass(self, base_valid_course: dict) -> None:
        """Valid MC7 items with informative error rationales pass R-17."""
        course = copy.deepcopy(base_valid_course)
        errors = check_extended_quality_rules(course)
        assert not any(e.code == "ERR_PLACEHOLDER_RATIONALE" for e in errors)

    @pytest.mark.parametrize("bad_rationale", [None, "", "   ", "placeholder", "distractor", "distractor 1", "n/a", "N/A", "none", "error", "error genérico"])
    def test_r17_mc7_placeholder_rationale_rejected(self, base_valid_course: dict, bad_rationale: str | None) -> None:
        """MC7 distractors with null, empty, or placeholder rationales trigger ERR_PLACEHOLDER_RATIONALE."""
        course = copy.deepcopy(base_valid_course)
        q = course["questions"][0]
        for opt in q["options"]:
            if not opt["is_correct"]:
                opt["error_rationale"] = bad_rationale
                break

        res = validate_course_content(json.dumps(course))
        assert not res.is_valid
        assert any(e.rule_id == "R-17" and e.code == "ERR_PLACEHOLDER_RATIONALE" for e in res.errors)

    @pytest.mark.parametrize("bad_rationale", ["placeholder", "distractor", "n/a", "none"])
    def test_r17_ms_placeholder_rationale_rejected(self, base_valid_course: dict, bad_rationale: str) -> None:
        """Multiple-select distractors with placeholder rationales trigger ERR_PLACEHOLDER_RATIONALE."""
        course = copy.deepcopy(base_valid_course)
        q = course["questions"][0]
        q["interaction_type"] = "multiple_select"
        q["options"] = [
            {"id": "opt_1", "content": "Opt 1", "is_correct": True},
            {"id": "opt_2", "content": "Opt 2", "is_correct": False, "error_rationale": "Explicación diagnóstica válida"},
            {"id": "opt_3", "content": "Opt 3", "is_correct": False, "error_rationale": bad_rationale},
            {"id": "opt_4", "content": "Opt 4", "is_correct": False, "error_rationale": "Explicación diagnóstica válida 2"},
        ]
        res = validate_course_content(json.dumps(course))
        assert not res.is_valid
        assert any(e.rule_id == "R-17" and e.code == "ERR_PLACEHOLDER_RATIONALE" for e in res.errors)

    # --- Rule R-18 Tests ---

    def test_r18_clean_option_content_passes(self, base_valid_course: dict) -> None:
        """Clean mathematical option content passes R-18."""
        course = copy.deepcopy(base_valid_course)
        errors = check_extended_quality_rules(course)
        assert not any(e.code == "ERR_META_GIVEAWAY" for e in errors)

    @pytest.mark.parametrize("giveaway_text", [
        "sumando erróneamente los términos independientes",
        "restando erróneamente la derivada",
        "calculado erróneamente mediante suma",
        "asumiendo erróneamente que la matriz es simétrica",
        "confundiendo la tasa de ahorro con la depreciación",
        "15 (sumando erróneamente)",
    ])
    def test_r18_meta_giveaway_in_content_rejected(self, base_valid_course: dict, giveaway_text: str) -> None:
        """Option content containing diagnostic meta-information triggers ERR_META_GIVEAWAY."""
        course = copy.deepcopy(base_valid_course)
        q = course["questions"][0]
        q["options"][0]["content"] = giveaway_text

        res = validate_course_content(json.dumps(course))
        assert not res.is_valid
        assert any(e.rule_id == "R-18" and e.code == "ERR_META_GIVEAWAY" for e in res.errors)

    # --- Rule R-19 Tests ---

    def test_r19_clean_fill_in_the_blank_passes(self, base_valid_course: dict) -> None:
        """FIB question where answer is not leaked in the stem passes R-19."""
        course = copy.deepcopy(base_valid_course)
        q = course["questions"][0]
        q["interaction_type"] = "fill_in_the_blank"
        del q["options"]
        q["stem"] = "Dada la ecuación $2x + 1 = 11$, determine el valor de $x$."
        q["correct_answer"] = "5"

        res = validate_course_content(json.dumps(course))
        assert res.is_valid
        assert not any(e.code == "ERR_ANSWER_LEAK" for e in res.errors)

    @pytest.mark.parametrize("leaked_stem", [
        "Calcule el valor de $x$ sabiendo que $x = 5$.",
        "Calcule el valor sabiendo que la respuesta es 5.",
        "Si el resultado es igual a 5, determine el parámetro.",
        "Calcule el valor si $x = $5$$.",
    ])
    def test_r19_answer_leak_rejected(self, base_valid_course: dict, leaked_stem: str) -> None:
        """FIB question leaking correct answer in stem triggers ERR_ANSWER_LEAK."""
        course = copy.deepcopy(base_valid_course)
        q = course["questions"][0]
        q["interaction_type"] = "fill_in_the_blank"
        del q["options"]
        q["stem"] = leaked_stem
        q["correct_answer"] = "5"

        res = validate_course_content(json.dumps(course))
        assert not res.is_valid
        assert any(e.rule_id == "R-19" and e.code == "ERR_ANSWER_LEAK" for e in res.errors)

    def test_r19_answer_leak_dict_answer_rejected(self, base_valid_course: dict) -> None:
        """FIB with dictionary correct_answer leaked in stem triggers ERR_ANSWER_LEAK."""
        course = copy.deepcopy(base_valid_course)
        q = course["questions"][0]
        q["interaction_type"] = "fill_in_the_blank"
        del q["options"]
        q["stem"] = "Halle la antiderivada sabiendo que $F(x) = x^2 + 1$."
        q["correct_answer"] = {"value": "x^2 + 1", "expression": "x^2 + 1"}

        res = validate_course_content(json.dumps(course))
        assert not res.is_valid
        assert any(e.rule_id == "R-19" and e.code == "ERR_ANSWER_LEAK" for e in res.errors)

    # --- Rule R-20 Tests ---

    def test_r20_valid_latex_passes(self, base_valid_course: dict) -> None:
        """Course with clean KaTeX syntax, primes, and macros passes R-20."""
        course = copy.deepcopy(base_valid_course)
        q = course["questions"][0]
        q["stem"] = r"Considere el sistema lineal $\dot{x} = Ax$ con $\text{tr}(A) < 0$ y $\phi''(k) < 0$."
        q["solution"] = r"Paso 1: Evaluamos $\phi'(k)$ y $\phi''(k) < 0$ para todo $k > 0$."
        res = validate_course_content(json.dumps(course))
        assert res.is_valid
        assert not any(e.code == "ERR_LATEX_SYNTAX" for e in res.errors)

    def test_r20_triple_dollar_rejected(self, base_valid_course: dict) -> None:
        """Triple dollar delimiter '$$$' triggers ERR_LATEX_SYNTAX."""
        course = copy.deepcopy(base_valid_course)
        course["questions"][0]["stem"] = "Evalúe $$$x^2 + 1$$$ para x = 0."
        res = validate_course_content(json.dumps(course))
        assert not res.is_valid
        assert any(e.rule_id == "R-20" and "triple" in e.message for e in res.errors)

    @pytest.mark.parametrize("unbalanced_field, text", [
        ("stem", "Considere la función $f(x) = x^2 y su derivada."),
        ("solution", "El resultado display es $$x = 1 sin cerrar."),
    ])
    def test_r20_unbalanced_delimiters_rejected(self, base_valid_course: dict, unbalanced_field: str, text: str) -> None:
        """Unbalanced $ or $$ delimiters trigger ERR_LATEX_SYNTAX."""
        course = copy.deepcopy(base_valid_course)
        course["questions"][0][unbalanced_field] = text
        res = validate_course_content(json.dumps(course))
        assert not res.is_valid
        assert any(e.rule_id == "R-20" and "Unbalanced" in e.message for e in res.errors)

    @pytest.mark.parametrize("double_brace_text", [
        r"Considere $\frac{{a}}{b} = 1$.",
        r"Considere $e^{{gt}}$ en el modelo.",
        r"Sea $\phi{{k}}$ una función.",
    ])
    def test_r20_residual_double_braces_rejected(self, base_valid_course: dict, double_brace_text: str) -> None:
        """Residual double braces '{{' or '}}' inside math expressions trigger ERR_LATEX_SYNTAX."""
        course = copy.deepcopy(base_valid_course)
        course["questions"][0]["stem"] = double_brace_text
        res = validate_course_content(json.dumps(course))
        assert not res.is_valid
        assert any(e.rule_id == "R-20" and "double braces" in e.message for e in res.errors)

    @pytest.mark.parametrize("unreplaced_text", [
        "Considere la ecuación con constante {k_val}.",
        "Sea la pendiente {slope} de la recta.",
        "Calcule $f(x) = {coeff} x + {const}$.",
    ])
    def test_r20_unreplaced_template_vars_rejected(self, base_valid_course: dict, unreplaced_text: str) -> None:
        """Unreplaced template variables {var} trigger ERR_LATEX_SYNTAX."""
        course = copy.deepcopy(base_valid_course)
        course["questions"][0]["stem"] = unreplaced_text
        res = validate_course_content(json.dumps(course))
        assert not res.is_valid
        assert any(e.rule_id == "R-20" and "Unreplaced template variable" in e.message for e in res.errors)

    def test_r20_competency_katex_syntax_checked(self, base_valid_course: dict) -> None:
        """Competency with corrupt KaTeX syntax in description triggers ERR_LATEX_SYNTAX."""
        course = copy.deepcopy(base_valid_course)
        course["competencies"][0]["description"] = r"Estimar los coeficientes de \hat{\boldsymbol{\beta} en el modelo."
        res = validate_course_content(json.dumps(course))
        assert not res.is_valid
        assert any(e.rule_id == "R-20" and e.code == "ERR_LATEX_SYNTAX" for e in res.errors)

    def test_r20_option_error_rationale_katex_checked(self, base_valid_course: dict) -> None:
        """Option with corrupt KaTeX in error_rationale triggers ERR_LATEX_SYNTAX."""
        course = copy.deepcopy(base_valid_course)
        q = course["questions"][0]
        for opt in q["options"]:
            if not opt["is_correct"]:
                opt["error_rationale"] = r"Error al asumir que el estimador es \hat{\boldsymbol{\beta} sin cerrar."
                break
        res = validate_course_content(json.dumps(course))
        assert not res.is_valid
        assert any(e.rule_id == "R-20" and e.code == "ERR_LATEX_SYNTAX" for e in res.errors)

    def test_r20_nested_unclosed_macro_rejected(self, base_valid_course: dict) -> None:
        """Question stem with unclosed nested accent/style macro triggers ERR_LATEX_SYNTAX."""
        course = copy.deepcopy(base_valid_course)
        course["questions"][0]["stem"] = r"Calcule el valor esperado del vector \hat{\boldsymbol{\beta} bajo el modelo."
        res = validate_course_content(json.dumps(course))
        assert not res.is_valid
        assert any(e.rule_id == "R-20" and e.code == "ERR_LATEX_SYNTAX" for e in res.errors)

    def test_r20_macro_arity_frac_rejected(self, base_valid_course: dict) -> None:
        r"""Question with \frac{a} missing second argument triggers ERR_LATEX_SYNTAX."""
        course = copy.deepcopy(base_valid_course)
        course["questions"][0]["stem"] = r"Considere la fracción $\frac{a}$ en la formulación."
        res = validate_course_content(json.dumps(course))
        assert not res.is_valid
        assert any(e.rule_id == "R-20" and e.code == "ERR_LATEX_SYNTAX" for e in res.errors)

    def test_r20_unclosed_environments_rejected(self, base_valid_course: dict) -> None:
        r"""Question with \begin{pmatrix} without matching \end{pmatrix} triggers ERR_LATEX_SYNTAX."""
        course = copy.deepcopy(base_valid_course)
        course["questions"][0]["stem"] = r"Sea la matriz $A = \begin{pmatrix} 1 & 2 \\ 3 & 4$ sin cerrar."
        res = validate_course_content(json.dumps(course))
        assert not res.is_valid
        assert any(e.rule_id == "R-20" and e.code == "ERR_LATEX_SYNTAX" for e in res.errors)

    # --- Rule R-22 Tests ---

    def test_r22_ms_with_all_rationales_passes(self, base_valid_course: dict) -> None:
        """Multiple-select with all incorrect options having diagnostic rationales passes R-22."""
        course = copy.deepcopy(base_valid_course)
        q = course["questions"][0]
        q["interaction_type"] = "multiple_select"
        q["options"] = [
            {"id": "opt_1", "content": "Opt 1", "is_correct": True},
            {"id": "opt_2", "content": "Opt 2", "is_correct": False, "error_rationale": "Error de concepto en opt 2"},
            {"id": "opt_3", "content": "Opt 3", "is_correct": False, "error_rationale": "Error de signo en opt 3"},
            {"id": "opt_4", "content": "Opt 4", "is_correct": False, "error_rationale": "Error de cálculo en opt 4"},
        ]
        res = validate_course_content(json.dumps(course))
        assert res.is_valid
        assert not any(e.code == "ERR_MS_MISSING_RATIONALE" for e in res.errors)

    @pytest.mark.parametrize("bad_rationale", [None, "", "   "])
    def test_r22_ms_missing_or_empty_rationale_rejected(self, base_valid_course: dict, bad_rationale: str | None) -> None:
        """Multiple-select with missing or empty error_rationale on distractor triggers ERR_MS_MISSING_RATIONALE."""
        course = copy.deepcopy(base_valid_course)
        q = course["questions"][0]
        q["interaction_type"] = "multiple_select"
        q["options"] = [
            {"id": "opt_1", "content": "Opt 1", "is_correct": True},
            {"id": "opt_2", "content": "Opt 2", "is_correct": False, "error_rationale": "Error diagnóstico válido"},
            {"id": "opt_3", "content": "Opt 3", "is_correct": False, "error_rationale": bad_rationale},
            {"id": "opt_4", "content": "Opt 4", "is_correct": False, "error_rationale": "Error diagnóstico válido 2"},
        ]
        res = validate_course_content(json.dumps(course))
        assert not res.is_valid
        assert any(e.rule_id == "R-22" and e.code == "ERR_MS_MISSING_RATIONALE" for e in res.errors)

    def test_r22_ms_omitted_rationale_key_rejected(self, base_valid_course: dict) -> None:
        """Multiple-select with error_rationale key completely omitted triggers ERR_MS_MISSING_RATIONALE."""
        course = copy.deepcopy(base_valid_course)
        q = course["questions"][0]
        q["interaction_type"] = "multiple_select"
        q["options"] = [
            {"id": "opt_1", "content": "Opt 1", "is_correct": True},
            {"id": "opt_2", "content": "Opt 2", "is_correct": False, "error_rationale": "Error diagnóstico válido"},
            {"id": "opt_3", "content": "Opt 3", "is_correct": False},  # key omitted
            {"id": "opt_4", "content": "Opt 4", "is_correct": False, "error_rationale": "Error diagnóstico válido 2"},
        ]
        res = validate_course_content(json.dumps(course))
        assert not res.is_valid
        assert any(e.rule_id == "R-22" and e.code == "ERR_MS_MISSING_RATIONALE" for e in res.errors)

