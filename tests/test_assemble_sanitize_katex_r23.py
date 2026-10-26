"""Unit & Integration Tests for KaTeX Overescape Safeguards (Content-to-Course R-23).

Tests:
1. Forensic overescaped commands collapse:
   - Verifies collapse of \\frac, \\text, \\Rightarrow, \\right, \\alpha, \\mathbb, \\to,
     \\beta, \\neq, \\times, \\forall, \\begin, \\rho, \\varepsilon, \\theta, \\bar.
   - Verifies collapse of multiple backslashes (\\\\frac, \\\\\\to).
2. Matrix and systems row breaks preservation:
   - Preserves row breaks '\\ ' in \\begin{pmatrix}, \\begin{bmatrix}, \\begin{cases},
     \\[4pt], and newline separated matrix rows.
3. \\centernot mapping to native KaTeX supported symbols:
   - \\centernot\\Rightarrow -> \\nRightarrow, \\centernot\\to -> \\nrightarrow,
     \\centernot\\Leftarrow -> \\nLeftarrow, \\centernot -> \\not.
4. \\text{..._...} contamination and unescaped underscore repair:
   - Repairs \\text{textVar[barx_n] = O(n)} -> \\text{Var}[\\bar{x}_n] = O(n).
   - Escapes unescaped underscores in plain text blocks: \\text{foo_bar} -> \\text{foo\\_bar}.
5. End-to-end assemble_question integration:
   - Verifies multiple_choice_7_options, fill_in_the_blank, and multiple_select reactives.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

import pytest

# Ensure skills root is in sys.path
_skill_root = Path(__file__).resolve().parents[1] / ".agents" / "skills" / "content-to-course"
if str(_skill_root) not in sys.path:
    sys.path.insert(0, str(_skill_root))

from engine.assemble import assemble_question, sanitize_katex_syntax
from engine.invariants import validate_katex_syntax


class TestKatexOverescapeSafeguards:
    """Test KaTeX overescape collapse, macro translation, and underscore safeguards."""

    @pytest.mark.parametrize(
        "cmd",
        [
            "frac",
            "text",
            "Rightarrow",
            "right",
            "alpha",
            "mathbb",
            "to",
            "beta",
            "neq",
            "times",
            "forall",
            "begin",
            "rho",
            "varepsilon",
            "theta",
            "bar",
        ],
    )
    def test_forensic_overescaped_commands_single_collapse(self, cmd: str):
        r"""Verify double-backslash \\cmd collapses cleanly to \cmd."""
        raw = f"\\\\{cmd}"
        expected = f"\\{cmd}"
        result = sanitize_katex_syntax(raw)
        assert result == expected, f"Failed collapsing double backslash for {cmd}: got {result}"

    def test_forensic_overescaped_commands_multi_slash(self):
        r"""Verify even multi-backslashes collapse to \cmd and odd multi-slashes preserve row breaks."""
        # 4 slashes (even)
        assert sanitize_katex_syntax(r"\\\\to") == r"\to"
        # 6 slashes (even)
        assert sanitize_katex_syntax(r"\\\\\\text{test}") == r"\text{test}"
        # 8 slashes (even)
        assert sanitize_katex_syntax(r"\\\\\\\\alpha") == r"\alpha"
        # 3 slashes (odd >= 3): row break (\\) followed by command (\cmd)
        assert sanitize_katex_syntax(r"\\\frac{1}{2}") == r"\\ \frac{1}{2}"
        # Compound math expression from forensic evidence
        raw = r"$\\\\alpha + \\\\beta \\\\neq \\\\frac{\\\\rho}{\\\\theta}$"
        expected = r"$\alpha + \beta \neq \frac{\rho}{\theta}$"
        assert sanitize_katex_syntax(raw) == expected

    def test_matrices_and_systems_row_breaks_preserved(self):
        r"""Verify that legitimate row breaks '\\ ' in matrices and cases are 100% preserved."""
        # Matrix with space after row break
        pmatrix = r"\begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}"
        assert sanitize_katex_syntax(pmatrix) == pmatrix

        # Bmatrix with digits and signs
        bmatrix = r"\begin{bmatrix} a & b \\ -c & +d \end{bmatrix}"
        assert sanitize_katex_syntax(bmatrix) == bmatrix

        # Cases environment with \text inside rows
        cases = r"\begin{cases} x & \\text{si } x \ge 0 \\ -x & \\text{si } x < 0 \end{cases}"
        expected_cases = r"\begin{cases} x & \text{si } x \ge 0 \\ -x & \text{si } x < 0 \end{cases}"
        assert sanitize_katex_syntax(cases) == expected_cases

        # Vertical spacing \\[4pt]
        vert_space = r"1 & 2 \\[4pt] 3 & 4"
        assert sanitize_katex_syntax(vert_space) == vert_space

        # Row break with newline
        newline_break = "1 & 2 \\\\\n3 & 4"
        assert sanitize_katex_syntax(newline_break) == newline_break

        # Row break followed by space and macro
        row_with_macro = r"1 & 2 \\ \frac{3}{4} & 5"
        assert sanitize_katex_syntax(row_with_macro) == row_with_macro

        # CRITICAL EDGE CASE: Row break immediately followed by command without space (3 slashes \\\frac)
        # Must preserve row break \\ and command \frac separated by space, avoiding row loss!
        matrix_3slashes = r"\begin{bmatrix} 1 & 2 \\\frac{3}{4} & 5 \end{bmatrix}"
        expected_3slashes = r"\begin{bmatrix} 1 & 2 \\ \frac{3}{4} & 5 \end{bmatrix}"
        assert sanitize_katex_syntax(matrix_3slashes) == expected_3slashes
        # Verify idempotence on 3 slashes result
        assert sanitize_katex_syntax(expected_3slashes) == expected_3slashes
        # Verify KaTeX validation passes with 0 errors
        assert not validate_katex_syntax(f"${expected_3slashes}$", "test_matrix_3slashes")

        # Additional 3-slash edge cases in pmatrix and cases
        pmatrix_3slashes = r"\begin{pmatrix} a & b \\\alpha & \beta \end{pmatrix}"
        expected_pmatrix = r"\begin{pmatrix} a & b \\ \alpha & \beta \end{pmatrix}"
        assert sanitize_katex_syntax(pmatrix_3slashes) == expected_pmatrix
        assert not validate_katex_syntax(f"${expected_pmatrix}$", "test_pmatrix_3slashes")

        cases_3slashes = r"\begin{cases} 1 & x > 0 \\\frac{1}{2} & x \le 0 \end{cases}"
        expected_cases_3 = r"\begin{cases} 1 & x > 0 \\ \frac{1}{2} & x \le 0 \end{cases}"
        assert sanitize_katex_syntax(cases_3slashes) == expected_cases_3
        assert not validate_katex_syntax(f"${expected_cases_3}$", "test_cases_3slashes")

    def test_centernot_mappings(self):
        r"""Verify \centernot macros are mapped to native KaTeX supported negated arrows/symbols."""
        assert sanitize_katex_syntax(r"A \centernot\Rightarrow B") == r"A \nRightarrow B"
        assert sanitize_katex_syntax(r"A \\centernot\\Rightarrow B") == r"A \nRightarrow B"
        assert sanitize_katex_syntax(r"A \centernot \implies B") == r"A \nRightarrow B"
        assert sanitize_katex_syntax(r"A \centernot\Leftarrow B") == r"A \nLeftarrow B"
        assert sanitize_katex_syntax(r"A \centernot\impliedby B") == r"A \nLeftarrow B"
        assert sanitize_katex_syntax(r"A \centernot\Leftrightarrow B") == r"A \nLeftrightarrow B"
        assert sanitize_katex_syntax(r"A \centernot\iff B") == r"A \nLeftrightarrow B"
        assert sanitize_katex_syntax(r"x \centernot\rightarrow y") == r"x \nrightarrow y"
        assert sanitize_katex_syntax(r"x \centernot\to y") == r"x \nrightarrow y"
        assert sanitize_katex_syntax(r"x \centernot\leftarrow y") == r"x \nleftarrow y"
        assert sanitize_katex_syntax(r"x \centernot\gets y") == r"x \nleftarrow y"
        assert sanitize_katex_syntax(r"x \centernot\leftrightarrow y") == r"x \nleftrightarrow y"
        assert sanitize_katex_syntax(r"\centernot P") == r"\not P"

        # Validate with KaTeX validator
        expr = r"$A \nRightarrow B \land x \nrightarrow y$"
        errors = validate_katex_syntax(expr, "test_centernot")
        assert not errors, f"KaTeX validation failed on mapped centernot: {errors}"

    def test_text_contamination_repair(self):
        r"""Verify repair of contaminated \text{textVar[barx_n] = O(n)} patterns."""
        raw = r"\text{textVar[barx_n] = O(n)}"
        expected = r"\text{Var}[\bar{x}_{n}] = O(n)"
        assert sanitize_katex_syntax(raw) == expected

        raw_cov = r"\text{textCov[barY_1] = 0}"
        expected_cov = r"\text{Cov}[\bar{Y}_{1}] = 0"
        assert sanitize_katex_syntax(raw_cov) == expected_cov

        raw_corr = r"\text{textCorr[barz_k] = 1}"
        expected_corr = r"\text{Corr}[\bar{z}_{k}] = 1"
        assert sanitize_katex_syntax(raw_corr) == expected_corr

        raw_e = r"\text{textE[barw_m] = \mu}"
        expected_e = r"\text{E}[\bar{w}_{m}] = \mu"
        assert sanitize_katex_syntax(raw_e) == expected_e

    def test_unescaped_underscores_in_text_blocks(self):
        r"""Verify plain \text{foo_bar} has underscores escaped to avoid KaTeX parse error without corrupting already escaped \_."""
        raw = r"$\text{foo_bar}$"
        expected = r"$\text{foo\_bar}$"
        assert sanitize_katex_syntax(raw) == expected

        raw_multi = r"$\text{loss_val_mse}$"
        expected_multi = r"$\text{loss\_val\_mse}$"
        assert sanitize_katex_syntax(raw_multi) == expected_multi

        # Multiple unescaped underscores
        raw_abc = r"$\text{a_b_c}$"
        expected_abc = r"$\text{a\_b\_c}$"
        assert sanitize_katex_syntax(raw_abc) == expected_abc
        assert sanitize_katex_syntax(expected_abc) == expected_abc

        # Mixed: already-escaped and unescaped underscores
        raw_mixed = r"$\text{foo\_bar_baz}$"
        expected_mixed = r"$\text{foo\_bar\_baz}$"
        assert sanitize_katex_syntax(raw_mixed) == expected_mixed
        assert sanitize_katex_syntax(expected_mixed) == expected_mixed

        # Already escaped should NEVER become \\_
        already = r"$\text{foo\_bar}$"
        assert sanitize_katex_syntax(already) == already
        assert r"\\_" not in sanitize_katex_syntax(already)

        # Math inside \text should not be touched
        math_in_text = r"$\text{valor $x_1$}$"
        assert sanitize_katex_syntax(math_in_text) == math_in_text

        # Validate with KaTeX validator across all variants
        for expr in [expected, expected_multi, expected_abc, expected_mixed]:
            errors = validate_katex_syntax(expr, "test_underscores")
            assert not errors, f"KaTeX validation failed on escaped underscores in {expr}: {errors}"

    def test_published_courses_matrices_and_all_strings_idempotency(self):
        r"""Verify 100% idempotency across all real published courses in courses/*.json.
        
        Ensures zero regressions or unintended alterations on:
        - 180+ real matrix and systems fields (\begin{pmatrix}, \begin{bmatrix}, \begin{matrix}, \begin{cases}).
        - All 220,000+ string fields across the 4 published courses.
        """
        courses_dir = Path(__file__).resolve().parents[1] / "courses"
        course_files = sorted(list(courses_dir.glob("*.json")))
        assert len(course_files) >= 4, f"Expected at least 4 published courses, found: {[f.name for f in course_files]}"

        total_strings = 0
        matrix_fields_count = 0
        diffs: List[str] = []

        matrix_triggers = (r"\begin{pmatrix}", r"\begin{bmatrix}", r"\begin{matrix}", r"\begin{cases}")

        for course_path in course_files:
            with open(course_path, "r", encoding="utf-8") as fp:
                data = json.load(fp)

            def _traverse(obj: Any, path: str = ""):
                nonlocal total_strings, matrix_fields_count
                if isinstance(obj, str):
                    total_strings += 1
                    if any(t in obj for t in matrix_triggers):
                        matrix_fields_count += 1
                    sanitized = sanitize_katex_syntax(obj)
                    if sanitized != obj:
                        diffs.append(f"{course_path.name} at {path}: orig={obj[:60]!r} != sanitized={sanitized[:60]!r}")
                elif isinstance(obj, list):
                    for idx, item in enumerate(obj):
                        _traverse(item, f"{path}[{idx}]")
                elif isinstance(obj, dict):
                    for k, v in obj.items():
                        _traverse(v, f"{path}.{k}")

            _traverse(data)

        assert matrix_fields_count >= 180, f"Expected >= 180 matrix fields, found {matrix_fields_count}"
        assert not diffs, f"Found {len(diffs)} idempotency differences in published courses:\n" + "\n".join(diffs[:10])


class TestAssembleQuestionSafeguardsIntegration:
    """Test end-to-end question assembly with overescaped inputs across interaction types."""

    def test_assemble_mc7_with_overescaped_math(self):
        r"""Verify assemble_question for multiple_choice_7_options sanitizes all fields."""
        template = {
            "stem": r"Calcule $\\\\frac{\\\\alpha}{\\\\beta}$ dado que $\\\\alpha = @a@$ y $\\\\beta = @b@$.",
            "hints": [
                r"Recuerde que $\\\\alpha$ y $\\\\beta$ son constantes.",
                r"Aplique $\\\\frac{@a@}{@b@}$.",
            ],
            "detailed_solution": r"La solución es $\\\\frac{@a@}{@b@} = @res@$. Además $\\\\forall x \\\\in \\\\mathbb{R}$.",
            "interaction_type": "multiple_choice_7_options",
            "bloom": "Apply",
            "difficulty": "medium",
            "distractor_ids": [f"D{i}" for i in range(1, 7)],
        }
        gen_result = {
            "vars": {"a": "4", "b": "2", "res": "2"},
            "correct": r"$\\\\frac{4}{2} = 2$",
            "distractors": [
                {"value": r"$\\\\frac{2}{4} = 0.5$", "distractor_id": "D1", "error_rationale": r"Inversión de $\\\\frac{a}{b}$"},
                {"value": r"$\\\\alpha \\\\times \\\\beta = 8$", "distractor_id": "D2", "error_rationale": r"Multiplicó en lugar de dividir"},
                {"value": r"$\\\\alpha - \\\\beta = 2$", "distractor_id": "D3", "error_rationale": r"Restó en lugar de dividir"},
                {"value": r"$\\\\alpha + \\\\beta = 6$", "distractor_id": "D4", "error_rationale": r"Sumó en lugar de dividir"},
                {"value": r"$\\\\centernot\\\\Rightarrow$", "distractor_id": "D5", "error_rationale": r"Uso de implicación falsa"},
                {"value": r"$\\\\text{textVar[barx_n] = O(n)}$", "distractor_id": "D6", "error_rationale": r"Confusión con varianza muestral"},
            ],
        }

        assembled = assemble_question(
            template=template,
            gen_result=gen_result,
            competency_id="Hab-01",
            question_index=1,
            seed=42,
        )

        assert assembled["interaction_type"] == "multiple_choice_7_options"
        # Check stem
        assert r"\frac{\alpha}{\beta}" in assembled["stem"]
        assert r"\\frac" not in assembled["stem"]

        # Check solution
        assert r"\forall x \in \mathbb{R}" in assembled["detailed_solution"]
        assert r"\\forall" not in assembled["detailed_solution"]
        assert r"\\mathbb" not in assembled["detailed_solution"]

        # Check options
        options = assembled["options"]
        assert len(options) == 7
        for opt in options:
            content = opt["content"]
            assert r"\\frac" not in content
            assert r"\\alpha" not in content
            assert r"\\centernot" not in content
            assert r"textVar" not in content
            if opt["error_rationale"]:
                assert r"\\frac" not in opt["error_rationale"]

        # KaTeX validation on all text fields
        assert not validate_katex_syntax(assembled["stem"], "stem")
        assert not validate_katex_syntax(assembled["detailed_solution"], "detailed_solution")
        for opt in options:
            assert not validate_katex_syntax(opt["content"], "option_content")
            if opt["error_rationale"]:
                assert not validate_katex_syntax(opt["error_rationale"], "error_rationale")

    def test_assemble_fib_with_overescaped_math(self):
        r"""Verify assemble_question for fill_in_the_blank sanitizes correct and equivalents."""
        template = {
            "stem": r"Determine el valor de $\\\\lim_{x \\\\to 0} \\\\frac{\\\\sin x}{x}$.",
            "hints": [r"Use regla de L'Hôpital o límite notable."],
            "detailed_solution": r"Por el límite notable, $\\\\lim_{x \\\\to 0} \\\\frac{\\\\sin x}{x} = 1$.",
            "interaction_type": "fill_in_the_blank",
            "bloom": "Understand",
            "difficulty": "easy",
        }
        gen_result = {
            "vars": {},
            "correct": r"\\\\frac{1}{1}",
            "canonical_algebraic": r"\\\\frac{1}{1}",
            "accepted_equivalents": [r"1", r"\\\\frac{1}{1}", r"\\\\frac{2}{2}"],
            "tolerance": 0.001,
        }

        assembled = assemble_question(
            template=template,
            gen_result=gen_result,
            competency_id="Hab-02",
            question_index=2,
            seed=100,
        )

        assert assembled["interaction_type"] == "fill_in_the_blank"
        assert r"\lim_{x \to 0}" in assembled["stem"]
        assert r"\\lim" not in assembled["stem"]
        assert r"\\to" not in assembled["stem"]

        ans = assembled["correct_answer"]
        assert ans["value"] == r"\frac{1}{1}"
        assert ans["canonical_algebraic"] == r"\frac{1}{1}"
        assert r"\frac{1}{1}" in ans["accepted_equivalents"]
        assert r"\frac{2}{2}" in ans["accepted_equivalents"]
        assert not any("\\\\" in eq for eq in ans["accepted_equivalents"])

    def test_assemble_multiple_select_with_matrices_and_overescapes(self):
        r"""Verify assemble_question for multiple_select preserves matrix breaks while cleaning overescapes."""
        matrix_latex = r"\begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}"
        template = {
            "stem": r"Seleccione todas las matrices ortogonales y propiedades verdaderas:",
            "hints": [r"Verifique $A^T A = I$."],
            "detailed_solution": r"La matriz identidad es simétrica y ortogonal.",
            "interaction_type": "multiple_select",
            "bloom": "Analyze",
            "difficulty": "hard",
        }
        gen_result = {
            "vars": {},
            "options": [
                {
                    "content": f"\\\\text{{Identidad: }} {matrix_latex}",
                    "is_correct": True,
                    "error_rationale": None,
                },
                {
                    "content": r"\\\\forall x \\\\in \\\\mathbb{R}^n, \\\\|Ax\\\\| = \\\\|x\\\\|",
                    "is_correct": True,
                    "error_rationale": None,
                },
                {
                    "content": r"$\\\\centernot\\\\Rightarrow \\\\det(A) = 0$",
                    "is_correct": False,
                    "error_rationale": r"Las matrices ortogonales tienen $\\\\det(A) = \\\\pm 1 \\\\neq 0$",
                },
                {
                    "content": r"$\\\\text{metric_loss_value}$",
                    "is_correct": False,
                    "error_rationale": r"Término no relacionado",
                },
            ],
        }

        assembled = assemble_question(
            template=template,
            gen_result=gen_result,
            competency_id="Hab-03",
            question_index=3,
            seed=7,
        )

        assert assembled["interaction_type"] == "multiple_select"
        options = assembled["options"]
        assert len(options) == 4

        # Check that matrix break '\\ ' is preserved in the identity option
        opt_matrix = next(opt for opt in options if "Identidad:" in opt["content"])
        assert matrix_latex in opt_matrix["content"]
        assert r"\begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}" in opt_matrix["content"]

        # Check that \\centernot was converted to \nRightarrow
        opt_neg = next(opt for opt in options if "det(A)" in opt["content"])
        assert r"\nRightarrow" in opt_neg["content"]
        assert r"\neq 0" in opt_neg["error_rationale"]

        # Check underscore escaping in text
        opt_loss = next(opt for opt in options if "metric" in opt["content"])
        assert r"\text{metric\_loss\_value}" in opt_loss["content"]

        # Validate with KaTeX validator
        for opt in options:
            assert not validate_katex_syntax(opt["content"], "ms_content")
            if opt["error_rationale"]:
                assert not validate_katex_syntax(opt["error_rationale"], "ms_rationale")
