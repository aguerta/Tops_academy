"""Tests for KaTeX over-escaping safeguards and shard healing under R-23.

Verifies:
1. validate_katex_syntax and check_instance_invariants reject over-escaped commands (\\frac, \\text, etc.) with R-23.
2. validate_katex_syntax permits matrix and cases environments containing '\\' in inline and display math.
3. validate_katex_syntax rejects inline linebreaks '\\' outside matrix/cases, \\centernot, and unescaped '_' in \\text{...}.
4. heal_shard_source_text heals raw and non-raw strings, producing exactly 1 backslash per LaTeX command in memory.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / ".agents" / "skills" / "content-to-course"

for p in [str(SKILL_DIR), str(REPO_ROOT)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from compile_shard import heal_shard_source_text
from engine.invariants import check_instance_invariants, validate_katex_syntax


def _build_valid_mc7() -> Dict[str, Any]:
    """Factory for a pristine, invariant-compliant MC7 item."""
    return {
        "id": "Q-HAB01-001",
        "interaction_type": "multiple_choice_7_options",
        "stem": "Determine the coefficient of determination for the given regression model.",
        "hints": [
            "Recall the definition of R-squared in linear regression.",
            "Compute the ratio of explained sum of squares to total sum of squares.",
            "Interpret the result as the proportion of explained variance.",
        ],
        "options": [
            {"id": "opt_a", "content": "R^2 = 0.852", "is_correct": True, "error_rationale": None},
            {"id": "opt_b", "content": "R^2 = 0.810", "is_correct": False, "error_rationale": "Distractor B"},
            {"id": "opt_c", "content": "R^2 = 0.795", "is_correct": False, "error_rationale": "Distractor C"},
            {"id": "opt_d", "content": "R^2 = 0.871", "is_correct": False, "error_rationale": "Distractor D"},
            {"id": "opt_e", "content": "R^2 = 0.834", "is_correct": False, "error_rationale": "Distractor E"},
            {"id": "opt_f", "content": "R^2 = 0.860", "is_correct": False, "error_rationale": "Distractor F"},
            {"id": "opt_g", "content": "R^2 = 0.825", "is_correct": False, "error_rationale": "Distractor G"},
        ],
    }


# =============================================================================
# 1. OVER-ESCAPED COMMANDS (R-23)
# =============================================================================
class TestKaTeXOverescapedCommandsR23:
    """Verifies that \\frac, \\text, \\to, \\mathbb, \\right, \\alpha, \\beta are rejected with R-23."""

    OVERESCAPED_COMMANDS = [
        ("frac", r"Calcule $\\frac{1}{2}$"),
        ("text", r"Observe $\\text{constante}$"),
        ("to", r"Límite cuando $x \\to 0$"),
        ("mathbb", r"Espacio $\\mathbb{R}^n$"),
        ("right", r"Intervalo $\\left( a, b \\right)$"),
        ("alpha", r"Parámetro $\\alpha = 0.05$"),
        ("beta", r"Pendiente $\\beta = 1.25$"),
    ]

    @pytest.mark.parametrize("cmd, snippet", OVERESCAPED_COMMANDS)
    def test_validate_katex_syntax_rejects_overescaped_command(self, cmd: str, snippet: str):
        errors = validate_katex_syntax(snippet, "stem")
        assert len(errors) > 0, f"Expected R-23 error for over-escaped command '\\\\{cmd}'"
        assert any("R-23" in e and f"\\\\{cmd}" in e for e in errors), f"Missing R-23 diagnostic: {errors}"

    @pytest.mark.parametrize("cmd, snippet", OVERESCAPED_COMMANDS)
    def test_check_instance_invariants_rejects_overescaped_command_in_stem(self, cmd: str, snippet: str):
        item = _build_valid_mc7()
        item["stem"] = f"Determine el valor bajo {snippet}."
        is_valid, errors = check_instance_invariants(item, "multiple_choice_7_options")
        assert not is_valid
        assert any("R-23" in e for e in errors), f"check_instance_invariants failed to reject R-23: {errors}"

    def test_check_instance_invariants_rejects_overescaped_command_in_hints_and_options(self):
        item = _build_valid_mc7()
        item["hints"][0] = r"Revise la constante $\\alpha$."
        item["options"][0]["content"] = r"$\\frac{1}{2}$"
        is_valid, errors = check_instance_invariants(item, "multiple_choice_7_options")
        assert not is_valid
        assert any("R-23" in e and "hint 1" in e for e in errors)
        assert any("R-23" in e and "option 1 content" in e for e in errors)

    def test_matrix_row_break_before_command_discrimination(self):
        # 3 backslashes: row break '\\' + '\frac' without space in matrix -> valid, NOT R-23
        matrix_compact = r"$\begin{bmatrix} 1 & 2 \\\frac{3}{4} & 5 \end{bmatrix}$"
        errs_compact = validate_katex_syntax(matrix_compact, "stem")
        assert not any("R-23" in e for e in errs_compact), f"Unexpected R-23 on compact row break: {errs_compact}"

        # 2 backslashes: row break '\\' + space + '\frac' -> valid, NOT R-23
        matrix_spaced = r"$\begin{bmatrix} 1 & 2 \\ \frac{3}{4} & 5 \end{bmatrix}$"
        errs_spaced = validate_katex_syntax(matrix_spaced, "stem")
        assert not any("R-23" in e for e in errs_spaced), f"Unexpected R-23 on spaced row break: {errs_spaced}"

        # 2 backslashes with [4pt] spacing: '\\[4pt]\frac' -> valid, NOT R-23
        matrix_bracket = r"$\begin{bmatrix} 1 & 2 \\[4pt]\frac{3}{4} & 5 \end{bmatrix}$"
        errs_bracket = validate_katex_syntax(matrix_bracket, "stem")
        assert not any("R-23" in e for e in errs_bracket), f"Unexpected R-23 on bracket row break: {errs_bracket}"

        # 4 backslashes: row break '\\' + over-escaped '\\frac' -> MUST reject R-23
        matrix_overescaped = r"$\begin{bmatrix} 1 & 2 \\\\frac{3}{4} & 5 \end{bmatrix}$"
        errs_over = validate_katex_syntax(matrix_overescaped, "stem")
        assert any("R-23" in e and r"\\frac" in e for e in errs_over), f"Expected R-23 on 4 backslashes: {errs_over}"


# =============================================================================
# 2. MATRIX AND CASES ENVIRONMENTS (PERMITTED)
# =============================================================================
class TestKaTeXMatrixAndCasesAllowedR23:
    """Verifies that bmatrix, pmatrix, and other multiline environments are permitted."""

    def test_bmatrix_allowed_inline_and_display(self):
        inline_bmatrix = r"Dada la matriz $\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}$ determine su determinante."
        display_bmatrix = r"Dada la matriz $$\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}$$ determine su determinante."

        errs_inline = validate_katex_syntax(inline_bmatrix, "stem")
        assert not errs_inline, f"Unexpected errors in inline bmatrix: {errs_inline}"

        errs_display = validate_katex_syntax(display_bmatrix, "stem")
        assert not errs_display, f"Unexpected errors in display bmatrix: {errs_display}"

    def test_pmatrix_allowed_inline_and_display(self):
        inline_pmatrix = r"Considere el vector $\begin{pmatrix} a \\ b \end{pmatrix}$ en el plano."
        display_pmatrix = r"Considere el vector $$\begin{pmatrix} a \\ b \end{pmatrix}$$ en el plano."

        errs_inline = validate_katex_syntax(inline_pmatrix, "stem")
        assert not errs_inline, f"Unexpected errors in inline pmatrix: {errs_inline}"

        errs_display = validate_katex_syntax(display_pmatrix, "stem")
        assert not errs_display, f"Unexpected errors in display pmatrix: {errs_display}"

    def test_bmatrix_with_template_double_braces(self):
        template_matrix = r"Sea la matriz $\begin{{bmatrix}} 1 & 2 \\ 3 & 4 \end{{bmatrix}}$."
        errs = validate_katex_syntax(template_matrix, "stem", allow_template_vars=True)
        assert not errs, f"Unexpected errors in template bmatrix: {errs}"

    def test_cases_and_aligned_allowed_inline(self):
        inline_cases = r"Definida por $f(x) = \begin{cases} 1 & x > 0 \\ 0 & x \le 0 \end{cases}$ continua."
        inline_aligned = r"Se deduce $\begin{aligned} x &= y \\ z &= w \end{aligned}$ en el sistema."

        errs_cases = validate_katex_syntax(inline_cases, "stem")
        assert not errs_cases, f"Unexpected errors in inline cases: {errs_cases}"

        errs_aligned = validate_katex_syntax(inline_aligned, "stem")
        assert not errs_aligned, f"Unexpected errors in inline aligned: {errs_aligned}"

    def test_nested_matrix_environments(self):
        nested = r"Considere el bloque $\begin{pmatrix} \begin{matrix} 1 \\ 2 \end{matrix} & 0 \\ 0 & 1 \end{pmatrix}$."
        errs = validate_katex_syntax(nested, "stem")
        assert not errs, f"Unexpected error in nested matrix: {errs}"

    def test_multiple_matrices_in_single_inline_block(self):
        # As seen in asyntotic_estatistics_v7.json Q-530
        stem = r"$\text{plim } A = \begin{pmatrix} 6 & 0 \\ 0 & 9 \end{pmatrix}, \text{plim } b = \begin{pmatrix} 47 \\ 49 \end{pmatrix}$"
        errs = validate_katex_syntax(stem, "stem")
        assert not errs, f"Unexpected error in multi-matrix inline block: {errs}"

    def test_multiple_inline_and_display_blocks(self):
        multi = (
            r"Dada la ecuación $$A = \begin{pmatrix} 1 \\ 2 \end{pmatrix}$$ "
            r"y el vector $v = \begin{pmatrix} 3 \\ 4 \end{pmatrix}$, calcule $x$."
        )
        errs = validate_katex_syntax(multi, "stem")
        assert not errs, f"Unexpected error in multi-block string: {errs}"

    def test_residual_double_curly_braces_rule2_behavior(self):
        # When allow_template_vars=False (default):
        assert any("Residual double curly braces" in e for e in validate_katex_syntax("El valor es {{var}}.", "stem"))
        assert any("Residual double curly braces" in e for e in validate_katex_syntax("El valor es {{.", "stem"))
        assert any("Residual double curly braces" in e for e in validate_katex_syntax(r"$\begin{{bmatrix}} 1 \end{{bmatrix}}$", "stem"))

        # When allow_template_vars=True:
        assert not validate_katex_syntax("El valor es {{var}}.", "stem", allow_template_vars=True)
        assert not validate_katex_syntax(r"$\begin{{bmatrix}} 1 & 2 \\ 3 & 4 \end{{bmatrix}}$", "stem", allow_template_vars=True)


# =============================================================================
# 3. FORBIDDEN INLINE LINEBREAKS AND UNSUPPORTED MACROS (R-23)
# =============================================================================
class TestKaTeXForbiddenInlineLinebreakAndBadMacrosR23:
    """Verifies rejection of inline '\\', \\centernot, and unescaped '_' in \\text{...}."""

    def test_inline_linebreak_outside_matrix_rejected(self):
        bad_inline = r"Sea el sistema $x = 1 \\ y = 2$ para las variables."
        errors = validate_katex_syntax(bad_inline, "stem")
        assert len(errors) > 0
        assert any("Forbidden linebreak" in e and "R-23" in e for e in errors)

    def test_centernot_rejected(self):
        bad_centernot = r"La proposición $\centernot\Rightarrow$ no es válida."
        errors = validate_katex_syntax(bad_centernot, "stem")
        assert len(errors) > 0
        assert any("\\centernot" in e and "R-23" in e for e in errors)

    def test_unescaped_underscore_in_text_rejected(self):
        bad_text = r"Considere el término $\text{textVar[barx_n] = O(n)}$ del algoritmo."
        errors = validate_katex_syntax(bad_text, "stem")
        assert len(errors) > 0
        assert any("Unescaped underscore '_'" in e and "barx_n" in e for e in errors)

    def test_escaped_underscore_in_text_accepted(self):
        valid_text = r"Considere el término $\text{textVar[barx\_n] = O(n)}$ del algoritmo."
        errors = validate_katex_syntax(valid_text, "stem")
        assert not errors, f"Unexpected errors for escaped underscore: {errors}"

    def test_inline_linebreak_between_two_matrices_rejected(self):
        bad_two_matrices = r"$\begin{pmatrix} 1 \\ 2 \end{pmatrix} \\ \begin{pmatrix} 3 \\ 4 \end{pmatrix}$"
        errors = validate_katex_syntax(bad_two_matrices, "stem")
        assert any("Forbidden linebreak" in e and "R-23" in e for e in errors)

    def test_inline_linebreak_with_bracket_spacing_rejected(self):
        bad_bracket_lb = r"Sea el sistema $x = 1 \\[4pt] y = 2$ en el dominio."
        errors = validate_katex_syntax(bad_bracket_lb, "stem")
        assert any("Forbidden linebreak" in e and "R-23" in e for e in errors)

    def test_trailing_inline_linebreak_rejected(self):
        bad_trailing = r"Considere $x = 1 \\$ en los reales."
        errors = validate_katex_syntax(bad_trailing, "stem")
        assert any("Forbidden linebreak" in e and "R-23" in e for e in errors)

    def test_empty_and_non_string_inputs_safe(self):
        assert validate_katex_syntax("", "stem") == []
        assert validate_katex_syntax("   \n\t  ", "stem") == []
        assert validate_katex_syntax(None, "stem") == []  # type: ignore[arg-type]
        assert validate_katex_syntax(42, "stem") == []  # type: ignore[arg-type]
        assert validate_katex_syntax(["lista"], "stem") == []  # type: ignore[arg-type]


# =============================================================================
# 4. SHARD SOURCE TEXT HEALING (R-23)
# =============================================================================
class TestCompileShardHealingR23:
    """Verifies that heal_shard_source_text cures raw and non-raw strings without overescape."""

    def test_heal_raw_string_with_implies(self):
        raw_source = 'stem = r"$\\frac{1}{2} \\implies x$"\n'
        modified, healed = heal_shard_source_text(raw_source)
        assert modified
        assert r"\Rightarrow" in healed
        assert r"\implies" not in healed

        ns: Dict[str, Any] = {}
        exec(healed, ns)
        val = ns["stem"]
        # In memory: 1 backslash before frac, 1 backslash before Rightarrow
        assert val == "$\\frac{1}{2} \\Rightarrow x$"
        assert len(re.findall(r"\\\\([a-zA-Z]+)", val)) == 0

    def test_heal_raw_string_with_double_backslash_frac(self):
        raw_source = 'stem = r"$\\\\frac{1}{2}$"\n'
        modified, healed = heal_shard_source_text(raw_source)
        assert modified
        assert 'r"$\\frac{1}{2}$"' in healed

        ns: Dict[str, Any] = {}
        exec(healed, ns)
        val = ns["stem"]
        assert val == "$\\frac{1}{2}$"
        assert len(re.findall(r"\\\\([a-zA-Z]+)", val)) == 0

    def test_heal_non_raw_string_with_frac_and_implies(self):
        non_raw_source = 'stem = "$\\\\frac{1}{2} \\\\implies x$"\n'
        modified, healed = heal_shard_source_text(non_raw_source)
        assert modified
        # In non-raw source: "\\frac{1}{2} \\Rightarrow x"
        assert "$\\\\frac{1}{2} \\\\Rightarrow x$" in healed

        ns: Dict[str, Any] = {}
        exec(healed, ns)
        val = ns["stem"]
        # Evaluated in memory: exactly 1 backslash per LaTeX command
        assert val == "$\\frac{1}{2} \\Rightarrow x$"
        assert len(re.findall(r"\\\\([a-zA-Z]+)", val)) == 0

    def test_heal_centernot_conversions(self):
        raw_source = 's1 = r"$\\centernot\\Rightarrow$"\ns2 = r"$\\centernot\\implies$"\n'
        modified, healed = heal_shard_source_text(raw_source)
        assert modified
        assert r"\nRightarrow" in healed
        assert r"\centernot" not in healed

        ns: Dict[str, Any] = {}
        exec(healed, ns)
        assert ns["s1"] == "$\\nRightarrow$"
        assert ns["s2"] == "$\\nRightarrow$"

    def test_fallback_does_not_corrupt_raw_strings(self):
        raw_code = 's = r"$\\alpha + \\beta$"\n'
        # Calling heal_shard_source_text on clean raw string should make no unwanted changes
        modified, healed = heal_shard_source_text(raw_code)
        assert not modified or 'r"$\\alpha' in healed
        ns: Dict[str, Any] = {}
        exec(healed, ns)
        assert len(re.findall(r"\\\\([a-zA-Z]+)", ns["s"])) == 0

    def test_heal_raw_string_preserves_matrix_row_breaks(self):
        # In raw string, '\\ ' is the matrix row break
        raw_source = 'matrix = r"$\\begin{bmatrix} 1 & 2 \\\\ 3 & 4 \\end{bmatrix}$"\n'
        modified, healed = heal_shard_source_text(raw_source)
        # Should not alter row breaks
        ns: Dict[str, Any] = {}
        exec(healed, ns)
        val = ns["matrix"]
        assert r"\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}" in val
        errs = validate_katex_syntax(val, "matrix")
        assert not any("R-23" in e for e in errs), f"Unexpected R-23 on healed matrix: {errs}"

    def test_heal_raw_string_preserves_compact_matrix_row_break_with_frac(self):
        # 3 backslashes: '\\' row break followed directly by '\frac'
        raw_source = 'matrix = r"$\\begin{bmatrix} 1 & 2 \\\\\\frac{3}{4} & 5 \\end{bmatrix}$"\n'
        modified, healed = heal_shard_source_text(raw_source)
        ns: Dict[str, Any] = {}
        exec(healed, ns)
        val = ns["matrix"]
        assert r"\\\frac{3}{4}" in val
        errs = validate_katex_syntax(val, "matrix")
        assert not any("R-23" in e for e in errs), f"Unexpected R-23 on compact healed matrix: {errs}"

    def test_heal_non_raw_string_preserves_matrix_row_breaks(self):
        # In non-raw string, '\\\\' in code evaluates to '\\' in memory
        non_raw_source = 'matrix = "$\\\\begin{bmatrix} 1 & 2 \\\\\\\\ 3 & 4 \\\\end{bmatrix}$"\n'
        modified, healed = heal_shard_source_text(non_raw_source)
        ns: Dict[str, Any] = {}
        exec(healed, ns)
        val = ns["matrix"]
        assert r"\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}" in val
        errs = validate_katex_syntax(val, "matrix")
        assert not any("R-23" in e for e in errs), f"Unexpected R-23 on healed non-raw matrix: {errs}"


# =============================================================================
# 5. ZERO FALSE POSITIVES ON PUBLISHED REAL COURSES
# =============================================================================
class TestRealCoursesKaTeXZeroFalsePositives:
    """Verifies that all questions with matrices across the 4 published courses have 0 R-23 errors."""

    COURSES = [
        "asyntotic_estatistics_v7.json",
        "gavilano_pre_parcial.json",
        "saul_control_optimo.json",
        "solow_growth_model.json",
    ]

    MATRIX_KEYWORDS = ("matrix", "pmatrix", "bmatrix", "vmatrix", "Vmatrix", "cases", "aligned", "array")

    def test_all_matrix_questions_in_real_courses_have_zero_r23_errors(self):
        courses_dir = REPO_ROOT / "courses"
        assert courses_dir.is_dir(), f"Courses directory not found: {courses_dir}"

        total_matrix_checked = 0
        total_questions_scanned = 0
        violations = []

        for course_filename in self.COURSES:
            course_path = courses_dir / course_filename
            assert course_path.is_file(), f"Course file not found: {course_path}"

            with open(course_path, "r", encoding="utf-8") as f:
                course_data = json.load(f)

            questions = course_data.get("questions", [])
            total_questions_scanned += len(questions)

            for q in questions:
                qid = q.get("id", "unknown")
                fields_to_check = [("stem", q.get("stem", ""))]

                for idx, hint in enumerate(q.get("hints", [])):
                    h_text = hint.get("text", "") if isinstance(hint, dict) else str(hint)
                    fields_to_check.append((f"hint_{idx}", h_text))

                for idx, opt in enumerate(q.get("options", [])):
                    o_text = opt.get("content", "") if isinstance(opt, dict) else str(opt)
                    fields_to_check.append((f"option_{idx}", o_text))

                if "explanation" in q:
                    fields_to_check.append(("explanation", q.get("explanation", "")))

                for field_name, text in fields_to_check:
                    if isinstance(text, str) and any(kw in text for kw in self.MATRIX_KEYWORDS):
                        total_matrix_checked += 1
                        errs = validate_katex_syntax(text, f"{course_filename}:{qid}:{field_name}")
                        r23_errs = [e for e in errs if "R-23" in e]
                        if r23_errs:
                            violations.append((course_filename, qid, field_name, r23_errs))

        # Must have verified a non-trivial number of real matrix occurrences
        assert total_questions_scanned >= 4000, f"Expected >4000 questions, got {total_questions_scanned}"
        assert total_matrix_checked >= 100, f"Expected >=100 matrix occurrences, got {total_matrix_checked}"
        assert len(violations) == 0, f"Found {len(violations)} R-23 violations in real courses: {violations[:5]}"

