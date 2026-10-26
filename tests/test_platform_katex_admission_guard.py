"""Tests for KaTeX Admission Guard and Runtime Auto-Repair (R-23 Safeguard).

Verifies Point 4 of the Definite KaTeX Protection Protocol:
1. validate_platform_course rejects over-escaped LaTeX commands (\\\\frac, \\\\text, \\\\to, \\\\mathbb, \\\\right, \\\\alpha),
   unsupported macros (\\centernot), and illegal inline line breaks ($a \\ b$) reporting R-23.
2. validate_platform_course accepts legitimate matrices (\\begin{bmatrix}, \\begin{pmatrix}) in inline ($...$)
   and display ($$...$$) modes.
3. repair_platform_course_katex deterministically repairs over-escaped commands, maps \\centernot,
   fixes template contamination, and preserves matrix row breaks intact.
4. scan_courses auto-repairs corrupted R-23 courses on disk and serves them with status 'valid'.
5. All 4 real production courses in courses/*.json pass validate_platform_course at 100%.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

import run_platform
from run_platform import (
    COURSES_DIR,
    repair_platform_course_katex,
    scan_courses,
    validate_platform_course,
)


def _build_course_json(stem_content: str, hints: list[str] | None = None, option_content: str = "1") -> str:
    """Helper to build a valid structure course JSON with custom math content."""
    course_dict = {
        "course_id": "guard_test_course",
        "title": "KaTeX Admission Guard Test Course",
        "competencies": [{"id": "COMP-01", "name": "Mathematical Precision"}],
        "questions": [
            {
                "id": "Q-GUARD-01",
                "interaction_type": "multiple_choice_7_options",
                "stem": stem_content,
                "hints": hints or ["Hint 1", "Hint 2", "Hint 3"],
                "options": [
                    {"id": "A", "content": option_content, "is_correct": True},
                    {"id": "B", "content": "2", "is_correct": False},
                    {"id": "C", "content": "3", "is_correct": False},
                    {"id": "D", "content": "4", "is_correct": False},
                    {"id": "E", "content": "5", "is_correct": False},
                    {"id": "F", "content": "6", "is_correct": False},
                    {"id": "G", "content": "7", "is_correct": False},
                ],
            }
        ],
    }
    return json.dumps(course_dict, ensure_ascii=False)


# =============================================================================
# 1. Validation Rejection Tests (Pass 1 & Pass 4 reporting R-23)
# =============================================================================

class TestPlatformKatexAdmissionRejection:
    """Verifies that validate_platform_course strictly rejects corrupted LaTeX and unsupported KaTeX."""

    @pytest.mark.parametrize(
        "cmd",
        ["frac", "text", "to", "mathbb", "right", "alpha"],
    )
    def test_validate_rejects_raw_overescaped_commands(self, cmd: str):
        """Pass 1 must catch raw 4-backslash over-escaped commands and report R-23."""
        raw_json = _build_course_json("Solve expression")
        corrupted_raw = raw_json.replace("Solve expression", f"\\\\\\\\{cmd}{{x}}")
        is_valid, msg = validate_platform_course(corrupted_raw)
        assert is_valid is False
        assert "R-23" in str(msg)
        assert "over-escaped" in str(msg).lower() or cmd in str(msg)

    def test_validate_rejects_raw_centernot(self):
        """Pass 1 must catch unsupported \\centernot macro and report R-23."""
        raw_json = _build_course_json("Evaluate implication")
        corrupted_raw = raw_json.replace("Evaluate implication", "A \\\\centernot\\\\Rightarrow B")
        is_valid, msg = validate_platform_course(corrupted_raw)
        assert is_valid is False
        assert "R-23" in str(msg)
        assert "centernot" in str(msg)

    def test_validate_rejects_in_memory_overescaped_command(self):
        """Pass 4 must catch over-escaped commands in memory (\\frac, \\text) across fields."""
        sample = {
            "course_id": "test_c",
            "title": "Test Course",
            "competencies": [{"id": "C-1", "name": "Comp 1"}],
            "questions": [
                {
                    "id": "Q-1",
                    "interaction_type": "multiple_choice_7_options",
                    "stem": "Calculate value",
                    "hints": [r"Use \\text{hint}"],
                    "options": [{"id": "A", "content": "1", "is_correct": True}],
                }
            ],
        }
        raw_json = json.dumps(sample)
        is_valid, msg = validate_platform_course(raw_json)
        assert is_valid is False
        assert "R-23" in str(msg)

    def test_validate_rejects_inline_linebreak_outside_matrix(self):
        """Pass 4 must reject '\\' within inline math '$...$' when outside matrix/system environments."""
        corrupted = _build_course_json(r"Consider $a \\ b$ in the formula")
        is_valid, msg = validate_platform_course(corrupted)
        assert is_valid is False
        assert "R-23" in str(msg)
        assert "inline math" in str(msg).lower()

    def test_validate_rejects_inline_linebreak_in_options_and_hints(self):
        """Pass 4 must check hints and options for illegal inline line breaks."""
        corrupted_opt = _build_course_json("Valid stem", option_content=r"$x \\ y$")
        is_valid, msg = validate_platform_course(corrupted_opt)
        assert is_valid is False
        assert "R-23" in str(msg)

        corrupted_hint = _build_course_json("Valid stem", hints=[r"$u \\ v$"])
        is_valid, msg = validate_platform_course(corrupted_hint)
        assert is_valid is False
        assert "R-23" in str(msg)

    def test_validate_rejects_overescaped_competency_description(self):
        """Rejects over-escaped LaTeX commands in competencies[*].description."""
        sample = {
            "course_id": "test_c",
            "title": "Test Course",
            "competencies": [
                {
                    "id": "COMP-MATH-01",
                    "name": "Precision in Proofs",
                    "description": r"Calcula la derivada usando \\frac{df}{dx} y límite.",
                }
            ],
            "questions": [
                {
                    "id": "Q-1",
                    "interaction_type": "multiple_choice_7_options",
                    "stem": "Solve for x",
                    "options": [{"id": "A", "content": "1", "is_correct": True}],
                }
            ],
        }
        raw_json = json.dumps(sample)
        is_valid, msg = validate_platform_course(raw_json)
        assert is_valid is False
        assert "R-23" in str(msg)
        assert "over-escaped" in str(msg).lower()

    def test_validate_rejects_inline_linebreak_in_competency_description(self):
        """Pass 4 must reject illegal inline line breaks in competencies[*].description."""
        sample = {
            "course_id": "test_c",
            "title": "Test Course",
            "competencies": [
                {
                    "id": "COMP-MATH-01",
                    "name": "Precision in Proofs",
                    "description": r"Calcula la derivada $a \\ b$ y límite.",
                }
            ],
            "questions": [
                {
                    "id": "Q-1",
                    "interaction_type": "multiple_choice_7_options",
                    "stem": "Solve for x",
                    "options": [{"id": "A", "content": "1", "is_correct": True}],
                }
            ],
        }
        raw_json = json.dumps(sample)
        is_valid, msg = validate_platform_course(raw_json)
        assert is_valid is False
        assert "R-23" in str(msg)
        assert "competency 'COMP-MATH-01' (description)" in str(msg)
        assert "inline math" in str(msg).lower()

    def test_validate_rejects_overescaped_competency_name(self):
        """Rejects over-escaped LaTeX commands in competencies[*].name."""
        sample = {
            "course_id": "test_c",
            "title": "Test Course",
            "competencies": [
                {
                    "id": "COMP-02",
                    "name": r"Propiedades de \\alpha y \\beta",
                    "description": "Valid description",
                }
            ],
            "questions": [
                {
                    "id": "Q-1",
                    "interaction_type": "multiple_choice_7_options",
                    "stem": "Solve for x",
                    "options": [{"id": "A", "content": "1", "is_correct": True}],
                }
            ],
        }
        raw_json = json.dumps(sample)
        is_valid, msg = validate_platform_course(raw_json)
        assert is_valid is False
        assert "R-23" in str(msg)
        assert "over-escaped" in str(msg).lower()

    def test_validate_rejects_inline_linebreak_in_competency_name(self):
        """Pass 4 must reject illegal inline line breaks in competencies[*].name."""
        sample = {
            "course_id": "test_c",
            "title": "Test Course",
            "competencies": [
                {
                    "id": "COMP-02",
                    "name": r"Propiedades de $u \\ v$",
                    "description": "Valid description",
                }
            ],
            "questions": [
                {
                    "id": "Q-1",
                    "interaction_type": "multiple_choice_7_options",
                    "stem": "Solve for x",
                    "options": [{"id": "A", "content": "1", "is_correct": True}],
                }
            ],
        }
        raw_json = json.dumps(sample)
        is_valid, msg = validate_platform_course(raw_json)
        assert is_valid is False
        assert "R-23" in str(msg)
        assert "competency 'COMP-02' (name)" in str(msg)
        assert "inline math" in str(msg).lower()

    def test_validate_rejects_overescaped_fill_in_the_blank_canonical_algebraic(self):
        """Rejects over-escaped LaTeX in fill_in_the_blank correct_answer.canonical_algebraic."""
        sample = {
            "course_id": "test_c",
            "title": "Test Course",
            "competencies": [{"id": "COMP-01", "name": "Algebraic Entry"}],
            "questions": [
                {
                    "id": "Q-FITB-01",
                    "interaction_type": "fill_in_the_blank",
                    "stem": "Ingresa la forma canónica:",
                    "correct_answer": {
                        "canonical_algebraic": r"\\alpha + \\beta^2",
                        "accepted_equivalents": ["x + y"],
                    },
                }
            ],
        }
        raw_json = json.dumps(sample)
        is_valid, msg = validate_platform_course(raw_json)
        assert is_valid is False
        assert "R-23" in str(msg)
        assert "over-escaped" in str(msg).lower()

    def test_validate_rejects_inline_linebreak_in_canonical_algebraic(self):
        """Pass 4 must reject illegal inline line breaks in correct_answer.canonical_algebraic."""
        sample = {
            "course_id": "test_c",
            "title": "Test Course",
            "competencies": [{"id": "COMP-01", "name": "Algebraic Entry"}],
            "questions": [
                {
                    "id": "Q-FITB-01",
                    "interaction_type": "fill_in_the_blank",
                    "stem": "Ingresa la forma canónica:",
                    "correct_answer": {
                        "canonical_algebraic": r"$x \\ y$",
                        "accepted_equivalents": ["x + y"],
                    },
                }
            ],
        }
        raw_json = json.dumps(sample)
        is_valid, msg = validate_platform_course(raw_json)
        assert is_valid is False
        assert "R-23" in str(msg)
        assert "canonical_algebraic" in str(msg)
        assert "inline math" in str(msg).lower()

    def test_validate_rejects_overescaped_fill_in_the_blank_accepted_equivalents(self):
        """Rejects over-escaped LaTeX in fill_in_the_blank correct_answer.accepted_equivalents."""
        sample = {
            "course_id": "test_c",
            "title": "Test Course",
            "competencies": [{"id": "COMP-01", "name": "Algebraic Entry"}],
            "questions": [
                {
                    "id": "Q-FITB-02",
                    "interaction_type": "fill_in_the_blank",
                    "stem": "Ingresa la forma canónica:",
                    "correct_answer": {
                        "canonical_algebraic": "x + y",
                        "accepted_equivalents": [r"y + \\frac{x}{1}"],
                    },
                }
            ],
        }
        raw_json = json.dumps(sample)
        is_valid, msg = validate_platform_course(raw_json)
        assert is_valid is False
        assert "R-23" in str(msg)
        assert "over-escaped" in str(msg).lower()

    def test_validate_rejects_inline_linebreak_in_accepted_equivalents(self):
        """Pass 4 must reject illegal inline line breaks in correct_answer.accepted_equivalents."""
        sample = {
            "course_id": "test_c",
            "title": "Test Course",
            "competencies": [{"id": "COMP-01", "name": "Algebraic Entry"}],
            "questions": [
                {
                    "id": "Q-FITB-02",
                    "interaction_type": "fill_in_the_blank",
                    "stem": "Ingresa la forma canónica:",
                    "correct_answer": {
                        "canonical_algebraic": "x + y",
                        "accepted_equivalents": [r"$u \\ v$"],
                    },
                }
            ],
        }
        raw_json = json.dumps(sample)
        is_valid, msg = validate_platform_course(raw_json)
        assert is_valid is False
        assert "R-23" in str(msg)
        assert "accepted_equivalents" in str(msg)
        assert "inline math" in str(msg).lower()

    def test_validate_rejects_overescaped_misconception_warning(self):
        """Rejects over-escaped LaTeX in common_misconception_warning."""
        sample = {
            "course_id": "test_c",
            "title": "Test Course",
            "competencies": [{"id": "COMP-01", "name": "Misconceptions"}],
            "questions": [
                {
                    "id": "Q-MISC-01",
                    "interaction_type": "multiple_choice_7_options",
                    "stem": "Identify optimal control",
                    "common_misconception_warning": r"No confundir con \\lambda_t transverso.",
                    "options": [{"id": "A", "content": "1", "is_correct": True}],
                }
            ],
        }
        raw_json = json.dumps(sample)
        is_valid, msg = validate_platform_course(raw_json)
        assert is_valid is False
        assert "R-23" in str(msg)
        assert "over-escaped" in str(msg).lower()

    def test_validate_rejects_inline_linebreak_in_misconception_warning(self):
        """Pass 4 must reject illegal inline line breaks in common_misconception_warning."""
        sample = {
            "course_id": "test_c",
            "title": "Test Course",
            "competencies": [{"id": "COMP-01", "name": "Misconceptions"}],
            "questions": [
                {
                    "id": "Q-MISC-01",
                    "interaction_type": "multiple_choice_7_options",
                    "stem": "Identify optimal control",
                    "common_misconception_warning": r"Atención con $z \\ w$ aquí.",
                    "options": [{"id": "A", "content": "1", "is_correct": True}],
                }
            ],
        }
        raw_json = json.dumps(sample)
        is_valid, msg = validate_platform_course(raw_json)
        assert is_valid is False
        assert "R-23" in str(msg)
        assert "misconception_warning" in str(msg)
        assert "inline math" in str(msg).lower()

    def test_validate_rejects_overescaped_course_metadata(self):
        """Rejects over-escaped LaTeX in course-level title and description."""
        sample = {
            "course_id": "test_c",
            "title": r"Curso de \\text{Optimización}",
            "description": "Valid description",
            "competencies": [{"id": "COMP-01", "name": "Comp"}],
            "questions": [
                {
                    "id": "Q-1",
                    "interaction_type": "multiple_choice_7_options",
                    "stem": "Question",
                    "options": [{"id": "A", "content": "1", "is_correct": True}],
                }
            ],
        }
        raw_json = json.dumps(sample)
        is_valid, msg = validate_platform_course(raw_json)
        assert is_valid is False
        assert "R-23" in str(msg)
        assert "over-escaped" in str(msg).lower()

    def test_validate_rejects_inline_linebreak_in_course_description(self):
        """Pass 4 must reject illegal inline line breaks in course-level description."""
        sample = {
            "course_id": "test_c",
            "title": "Curso Válido",
            "description": r"Descripción con $m \\ n$ inline.",
            "competencies": [{"id": "COMP-01", "name": "Comp"}],
            "questions": [
                {
                    "id": "Q-1",
                    "interaction_type": "multiple_choice_7_options",
                    "stem": "Question",
                    "options": [{"id": "A", "content": "1", "is_correct": True}],
                }
            ],
        }
        raw_json = json.dumps(sample)
        is_valid, msg = validate_platform_course(raw_json)
        assert is_valid is False
        assert "R-23" in str(msg)
        assert "course description" in str(msg)
        assert "inline math" in str(msg).lower()


# =============================================================================
# 2. Validation Acceptance Tests (Legitimate Matrices in Inline & Display)
# =============================================================================

class TestPlatformKatexAdmissionAcceptance:
    """Verifies that validate_platform_course accepts legitimate matrices in inline and display modes."""

    def test_validate_accepts_bmatrix_inline(self):
        r"""Inline $\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}$ must be valid."""
        raw = _build_course_json(r"Given $\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}$, find determinant.")
        is_valid, payload = validate_platform_course(raw)
        assert is_valid is True, f"Failed on inline bmatrix: {payload}"
        assert isinstance(payload, dict)

    def test_validate_accepts_pmatrix_inline(self):
        r"""Inline $\begin{pmatrix} 0 & 1/2 \\ 1/2 & 0 \end{pmatrix}$ must be valid."""
        raw = _build_course_json(r"Matrix $\begin{pmatrix} 0 & 1/2 \\ 1/2 & 0 \end{pmatrix}$ is symmetric.")
        is_valid, payload = validate_platform_course(raw)
        assert is_valid is True, f"Failed on inline pmatrix: {payload}"
        assert isinstance(payload, dict)

    def test_validate_accepts_bmatrix_display(self):
        r"""Display $$\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}$$ must be valid."""
        raw = _build_course_json(r"Calculate $$\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}$$")
        is_valid, payload = validate_platform_course(raw)
        assert is_valid is True, f"Failed on display bmatrix: {payload}"

    def test_validate_accepts_pmatrix_display(self):
        r"""Display $$\begin{pmatrix} 0 & 1/2 \\ 1/2 & 0 \end{pmatrix}$$ must be valid."""
        raw = _build_course_json(r"Consider $$\begin{pmatrix} 0 & 1/2 \\ 1/2 & 0 \end{pmatrix}$$")
        is_valid, payload = validate_platform_course(raw)
        assert is_valid is True, f"Failed on display pmatrix: {payload}"

    def test_validate_accepts_cases_and_aligned_environments(self):
        r"""Cases and aligned environments inside inline and display must be valid."""
        raw_cases = _build_course_json(r"Function $f(x) = \begin{cases} 1 & x \ge 0 \\ 0 & x < 0 \end{cases}$")
        is_valid, payload = validate_platform_course(raw_cases)
        assert is_valid is True, f"Failed on cases environment: {payload}"


# =============================================================================
# 3. Deterministic Runtime Repair Tests
# =============================================================================

class TestPlatformKatexRepair:
    """Verifies repair_platform_course_katex deterministic fixes and matrix preservation."""

    def test_repair_deterministic_fixes(self):
        """Verifies repair of \\\\frac, \\\\to, \\centernot\\Rightarrow and template contamination."""
        corrupted_raw = (
            '{"questions": [{"stem": "\\\\\\\\frac{1}{2} + \\\\\\\\to '
            '\\\\centernot\\\\Rightarrow \\\\text{textVar[barx_n] = O(n)}"}]}'
        )
        repaired, fixes = repair_platform_course_katex(corrupted_raw)
        assert fixes >= 4
        # Check collapsed commands
        assert r"\\frac" in repaired and r"\\\\frac" not in repaired
        assert r"\\to" in repaired and r"\\\\to" not in repaired
        # Check mapped macro
        assert r"\\nRightarrow" in repaired and r"centernot" not in repaired
        # Check template repair
        stem_val = json.loads(repaired)["questions"][0]["stem"]
        assert r"\text{Var}[\bar{x}_n] = O(n)" in stem_val

    def test_repair_preserves_matrix_row_breaks(self):
        r"""Verifies matrix row breaks (\\\\ followed by space, digit, sign, corchete) remain untouched."""
        raw_matrix = (
            '{"questions": [{"stem": "\\\\begin{pmatrix} 1 & 2 \\\\\\\\ 3 & 4 \\\\end{pmatrix}"}]}'
        )
        repaired, fixes = repair_platform_course_katex(raw_matrix)
        assert fixes == 0
        assert r"\begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}" in json.loads(repaired)["questions"][0]["stem"]

    @pytest.mark.parametrize(
        "macro,expected",
        [
            (r"\centernot\Rightarrow", r"\nRightarrow"),
            (r"\centernot\implies", r"\nRightarrow"),
            (r"\centernot\Leftarrow", r"\nLeftarrow"),
            (r"\centernot\impliedby", r"\nLeftarrow"),
            (r"\centernot\Leftrightarrow", r"\nLeftrightarrow"),
            (r"\centernot\iff", r"\nLeftrightarrow"),
            (r"\centernot\rightarrow", r"\nrightarrow"),
            (r"\centernot\to", r"\nrightarrow"),
            (r"\centernot\leftarrow", r"\nleftarrow"),
            (r"\centernot\gets", r"\nleftarrow"),
            (r"\centernot\leftrightarrow", r"\nleftrightarrow"),
            (r"\centernot", r"\not"),
        ],
    )
    def test_repair_all_centernot_arrow_variants(self, macro: str, expected: str):
        r"""repair_platform_course_katex must translate all arrow variants of \centernot."""
        raw = f'{{"questions": [{{"stem": "A {macro} B"}}]}}'
        repaired, fixes = repair_platform_course_katex(raw)
        assert fixes >= 1
        stem = json.loads(repaired)["questions"][0]["stem"]
        assert expected in stem
        assert "centernot" not in stem

    def test_repair_inline_line_break_outside_matrix(self):
        """repair_platform_course_katex replaces invalid inline line breaks with spaces while preserving matrices."""
        raw = (
            r'{"questions": [{"stem": "Solve $a \\\\ b$ and $\\begin{pmatrix} 1 & 2 \\\\ 3 & 4 \\end{pmatrix}$ and $$c \\\\ d$$"}]}'
        )
        repaired, fixes = repair_platform_course_katex(raw)
        assert fixes == 1
        stem = json.loads(repaired)["questions"][0]["stem"]
        assert "$a  b$" in stem
        assert r"\begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}" in stem
        assert r"$$c \\ d$$" in stem

    def test_repair_matrix_row_break_adjacent_to_command_without_space(self):
        r"""repair_platform_course_katex normalizes 6 raw backslashes (\\ immediately preceding \cmd) into '\\ \cmd'."""
        raw_stem = r"\begin{pmatrix} 1 & 2 \\\frac{3}{4} & 5 \end{pmatrix}"
        raw = json.dumps({"questions": [{"stem": raw_stem}]})
        repaired, fixes = repair_platform_course_katex(raw)
        assert fixes >= 1
        stem = json.loads(repaired)["questions"][0]["stem"]
        assert r"\begin{pmatrix} 1 & 2 \\ \frac{3}{4} & 5 \end{pmatrix}" in stem


# =============================================================================
# 4. scan_courses Auto-Repair Integration Test
# =============================================================================

class TestPlatformScanCoursesAutoRepair:
    """Verifies that scan_courses detects R-23 errors, auto-repairs on disk, and serves valid course."""

    def test_scan_courses_autorepairs_and_serves_valid(self, tmp_path, monkeypatch):
        """Temporary course with over-escaped KaTeX is auto-repaired and served as valid."""
        monkeypatch.setattr(run_platform, "COURSES_DIR", tmp_path)

        # Build corrupted course content with over-escaped LaTeX in valid JSON formatting
        valid_json = _build_course_json("Normal stem")
        corrupted_json = valid_json.replace(
            "Normal stem",
            "\\\\\\\\frac{1}{2} + \\\\\\\\to \\\\mathbb{R} + \\\\centernot\\\\Rightarrow"
        )
        # Verify it fails validation initially with R-23
        is_valid_initial, err_msg = validate_platform_course(corrupted_json)
        assert is_valid_initial is False
        assert "R-23" in str(err_msg)

        # Write to disk in temp dir
        test_file = tmp_path / "test_overescape_course.json"
        test_file.write_text(corrupted_json, encoding="utf-8")

        # Scan courses
        discovered = scan_courses()
        assert len(discovered) == 1
        record = discovered[0]
        assert record.get("status") == "valid", f"Course was not marked valid: {record.get('error_message')}"
        assert record.get("id") == "guard_test_course"

        # Verify disk file was auto-repaired and now passes validation
        persisted_content = test_file.read_text(encoding="utf-8")
        is_valid_disk, _ = validate_platform_course(persisted_content)
        assert is_valid_disk is True, "Persisted file on disk failed validation after auto-repair"

    def test_scan_courses_autorepairs_competency_description_and_fill_in_the_blank(self, tmp_path, monkeypatch):
        """scan_courses must auto-repair overescaped competency description, fitb, and illegal inline break."""
        monkeypatch.setattr(run_platform, "COURSES_DIR", tmp_path)

        corrupted = {
            "course_id": "auto_repair_full_test",
            "title": "Auto Repair Full Test Course",
            "competencies": [
                {
                    "id": "COMP-01",
                    "name": "Integration Test",
                    "description": r"Formulación con \\frac{dy}{dx} sobreescapada.",
                }
            ],
            "questions": [
                {
                    "id": "Q-FITB-AUTO",
                    "interaction_type": "fill_in_the_blank",
                    "stem": r"Calcula $u \\ v$ en la ecuación:",
                    "hints": ["Hint 1", "Hint 2", "Hint 3"],
                    "correct_answer": {
                        "canonical_algebraic": r"\\alpha + \\beta",
                        "accepted_equivalents": [r"\\beta + \\alpha"],
                    },
                }
            ],
        }
        corrupted_raw = json.dumps(corrupted, ensure_ascii=False)
        is_valid_initial, err_msg = validate_platform_course(corrupted_raw)
        assert is_valid_initial is False
        assert "R-23" in str(err_msg)

        test_file = tmp_path / "test_fitb_course.json"
        test_file.write_text(corrupted_raw, encoding="utf-8")

        discovered = scan_courses()
        assert len(discovered) == 1
        record = discovered[0]
        assert record.get("status") == "valid", f"Course was not marked valid: {record.get('error_message')}"
        assert record.get("id") == "auto_repair_full_test"

        persisted = test_file.read_text(encoding="utf-8")
        is_valid_disk, _ = validate_platform_course(persisted)
        assert is_valid_disk is True


# =============================================================================
# 5. Real Production Courses Validation (100% Pass)
# =============================================================================

class TestRealCoursesAdmission:
    """Verifies all production courses in courses/ pass validate_platform_course 100%."""

    def test_real_courses_pass_validation_100_percent(self):
        assert COURSES_DIR.exists(), f"Courses directory not found at {COURSES_DIR}"
        course_files = sorted(list(COURSES_DIR.glob("*.json")))
        assert len(course_files) >= 4, f"Expected at least 4 courses, found {len(course_files)}"

        for f in course_files:
            content = f.read_text(encoding="utf-8")
            is_valid, payload = validate_platform_course(content)
            assert is_valid is True, f"Real course '{f.name}' failed validate_platform_course: {payload}"
            assert isinstance(payload, dict)
            assert len(payload.get("questions", [])) > 0
            assert len(payload.get("competencies", [])) > 0

    def test_real_courses_repair_idempotence(self):
        """repair_platform_course_katex must be 100% idempotent on all real production courses (fixes == 0)."""
        assert COURSES_DIR.exists(), f"Courses directory not found at {COURSES_DIR}"
        course_files = sorted(list(COURSES_DIR.glob("*.json")))
        assert len(course_files) >= 4, f"Expected at least 4 courses, found {len(course_files)}"

        for f in course_files:
            content = f.read_text(encoding="utf-8")
            repaired, fixes = repair_platform_course_katex(content)
            assert fixes == 0, f"Course '{f.name}' had {fixes} fixes instead of 0"
            assert repaired == content, f"Course '{f.name}' was modified by repair_platform_course_katex"


# =============================================================================
# 6. FUTURE_MILESTONES Parity Tests
# =============================================================================

class TestFutureMilestonesParity:
    """Verifies byte-for-byte exact parity between FUTURE_MILESTONES.md and docs mirror."""

    def test_future_milestones_byte_parity(self):
        root_milestones = Path(__file__).resolve().parent.parent / "FUTURE_MILESTONES.md"
        docs_milestones = Path(__file__).resolve().parent.parent / "docs" / "future_milestones" / "FUTURE_MILESTONES.md"

        assert root_milestones.exists(), f"Missing root FUTURE_MILESTONES.md at {root_milestones}"
        assert docs_milestones.exists(), f"Missing mirror FUTURE_MILESTONES.md at {docs_milestones}"

        root_bytes = root_milestones.read_bytes()
        docs_bytes = docs_milestones.read_bytes()

        assert root_bytes == docs_bytes, "FUTURE_MILESTONES.md and docs/future_milestones/FUTURE_MILESTONES.md are not identical byte-by-byte"
        assert len(root_bytes) > 1000
