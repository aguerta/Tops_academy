"""Test suite for KaTeX Over-escape Safeguards (Rule R-23).

Verifies:
1. Lexical scanner pre-parse detection of over-escaped LaTeX commands (ERR_LATEX_OVERESCAPE).
2. Lexical error consolidation across repeated occurrences.
3. Legitimate linebreaks in multiline matrix/cases environments without false positives.
4. Semantic memory detection of over-escaped LaTeX commands in question fields.
5. Invariant enforcement against inline math linebreaks outside matrix/cases (ERR_LATEX_INLINE_NEWLINE).
6. KaTeX unsupported macro detection (\\centernot -> ERR_LATEX_UNSUPPORTED_MACRO).
7. KaTeX parse error prevention for unescaped underscores in \\text{...} (ERR_LATEX_SYNTAX).
8. Full regression verification on all 4 published courses in courses/*.json (0 R-23 errors).
"""
from __future__ import annotations

import json
from pathlib import Path
import pytest

from validator.core import validate_course_content
from validator.lexical_scanner import scan_lexical
from validator.rules import check_extended_quality_rules

REPO_ROOT = Path(__file__).resolve().parent.parent


# =============================================================================
# 1. Lexical Scanner: ERR_LATEX_OVERESCAPE (R-23)
# =============================================================================

@pytest.mark.parametrize("cmd", [
    "frac", "text", "to", "mathbb", "right", "alpha",
    "beta", "theta", "rho", "varepsilon", "times", "Rightarrow",
])
def test_scan_lexical_detects_overescaped_latex_commands(cmd: str) -> None:
    """Raw JSON containing \\\\\\\\cmd must trigger R-23 ERR_LATEX_OVERESCAPE."""
    raw_json = f'{{"stem": "Formula: \\\\\\\\{cmd}{{x}}"}}\n'
    errors = scan_lexical(raw_json)
    r23_errors = [e for e in errors if e.rule_id == "R-23" and e.code == "ERR_LATEX_OVERESCAPE"]
    assert len(r23_errors) == 1
    err = r23_errors[0]
    assert cmd in err.message
    assert "evaluates to" in err.message
    assert "linebreak + literal text in KaTeX" in err.message


def test_scan_lexical_overescape_consolidation() -> None:
    """Multiple identical over-escapes across lines consolidate when consolidate=True."""
    raw_json = (
        '{\n'
        '  "stem": "First \\\\\\\\frac{1}{2}",\n'
        '  "solution": "Second \\\\\\\\frac{3}{4}",\n'
        '  "misconception": "Third \\\\\\\\frac{5}{6}"\n'
        '}\n'
    )
    raw_errors = scan_lexical(raw_json, consolidate=False)
    r23_raw = [e for e in raw_errors if e.rule_id == "R-23" and e.code == "ERR_LATEX_OVERESCAPE"]
    assert len(r23_raw) == 3

    consolidated_errors = scan_lexical(raw_json, consolidate=True)
    r23_cons = [e for e in consolidated_errors if e.rule_id == "R-23" and e.code == "ERR_LATEX_OVERESCAPE"]
    assert len(r23_cons) == 1
    assert r23_cons[0].details.get("consolidated_count") == 3
    assert len(r23_cons[0].lines) == 3


# =============================================================================
# 2. Legitimate Multiline Matrix / Cases Linebreaks (0 errors)
# =============================================================================

@pytest.mark.parametrize("env", ["bmatrix", "pmatrix", "matrix", "cases"])
def test_legitimate_matrix_cases_linebreaks_allowed(env: str) -> None:
    """Legitimate row breaks \\\\\\\\ followed by space/digit/sign in matrix/cases environments must not trigger R-23."""
    # In raw JSON text, a LaTeX linebreak \\ is encoded as \\\\ followed by space or newline
    raw_json = (
        '{\n'
        f'  "stem": "Matrix: $\\\\begin{{{env}}} 1 & 2 \\\\\\\\ 3 & 4 \\\\end{{{env}}}$"\n'
        '}\n'
    )
    errors = scan_lexical(raw_json)
    r23_errors = [e for e in errors if e.rule_id == "R-23"]
    assert len(r23_errors) == 0

    parsed = json.loads(raw_json)
    rule_errors = check_extended_quality_rules(parsed)
    r23_rule_errors = [e for e in rule_errors if e.rule_id == "R-23"]
    assert len(r23_rule_errors) == 0


# =============================================================================
# 3. Memory Detection: ERR_LATEX_OVERESCAPE, ERR_LATEX_INLINE_NEWLINE, ERR_LATEX_UNSUPPORTED_MACRO, ERR_LATEX_SYNTAX
# =============================================================================

def test_check_extended_quality_rules_detects_overescape_in_memory() -> None:
    """Memory text with \\\\frac (2 backslashes in memory) triggers ERR_LATEX_OVERESCAPE."""
    data = {
        "course_id": "test_course",
        "questions": [
            {
                "id": "Q-01",
                "stem": "Considere \\\\frac{a}{b}",
            }
        ]
    }
    errors = check_extended_quality_rules(data)
    over_errs = [e for e in errors if e.rule_id == "R-23" and e.code == "ERR_LATEX_OVERESCAPE"]
    assert len(over_errs) == 1
    assert "Over-escaped LaTeX command '\\\\frac' detected in memory" in over_errs[0].message
    assert over_errs[0].item_id == "Q-01"


def test_check_extended_quality_rules_detects_inline_linebreak() -> None:
    """Forbidden linebreak \\\\ inside inline math $...$ outside matrix/cases triggers ERR_LATEX_INLINE_NEWLINE."""
    data = {
        "course_id": "test_course",
        "questions": [
            {
                "id": "Q-02",
                "stem": "Sea la expresión $a \\\\ b$ en el plano.",
            }
        ]
    }
    errors = check_extended_quality_rules(data)
    nl_errs = [e for e in errors if e.rule_id == "R-23" and e.code == "ERR_LATEX_INLINE_NEWLINE"]
    assert len(nl_errs) == 1
    assert "Forbidden linebreak '\\\\' inside inline math" in nl_errs[0].message
    assert nl_errs[0].item_id == "Q-02"


def test_inline_matrix_with_linebreak_allowed() -> None:
    """Inline math with \\\\ inside matrix environment does not trigger ERR_LATEX_INLINE_NEWLINE."""
    data = {
        "course_id": "test_course",
        "questions": [
            {
                "id": "Q-03",
                "stem": r"Sea $M = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}$ una matriz.",
            }
        ]
    }
    errors = check_extended_quality_rules(data)
    nl_errs = [e for e in errors if e.rule_id == "R-23" and e.code == "ERR_LATEX_INLINE_NEWLINE"]
    assert len(nl_errs) == 0


def test_check_extended_quality_rules_detects_unsupported_macro_centernot() -> None:
    """Unsupported macro \\centernot triggers ERR_LATEX_UNSUPPORTED_MACRO."""
    data = {
        "course_id": "test_course",
        "questions": [
            {
                "id": "Q-04",
                "stem": r"Condición $A \centernot\Rightarrow B$ necesaria.",
            }
        ]
    }
    errors = check_extended_quality_rules(data)
    macro_errs = [e for e in errors if e.rule_id == "R-23" and e.code == "ERR_LATEX_UNSUPPORTED_MACRO"]
    assert len(macro_errs) == 1
    assert "\\centernot" in macro_errs[0].message
    assert "\\nRightarrow" in macro_errs[0].message


def test_check_extended_quality_rules_detects_unescaped_underscore_in_text() -> None:
    """Unescaped underscore inside \\text{...} triggers ERR_LATEX_SYNTAX (R-20)."""
    data = {
        "course_id": "test_course",
        "questions": [
            {
                "id": "Q-05",
                "stem": r"Sea $\text{textVar[barx_n] = O(n)}$ el orden de convergencia.",
            }
        ]
    }
    errors = check_extended_quality_rules(data)
    syntax_errs = [e for e in errors if e.rule_id == "R-20" and e.code == "ERR_LATEX_SYNTAX" and "Unescaped underscore" in e.message]
    assert len(syntax_errs) == 1
    assert "Unescaped underscore '_' inside '\\text{textVar[barx_n] = O(n)}'" in syntax_errs[0].message


def test_escaped_underscore_in_text_allowed() -> None:
    """Escaped underscore \\_ inside \\text{...} is valid and does not trigger error."""
    data = {
        "course_id": "test_course",
        "questions": [
            {
                "id": "Q-06",
                "stem": r"Sea $\text{variable\_nombre}$ el identificador.",
            }
        ]
    }
    errors = check_extended_quality_rules(data)
    syntax_errs = [e for e in errors if e.code == "ERR_LATEX_SYNTAX" and "Unescaped underscore" in e.message]
    assert len(syntax_errs) == 0


# =============================================================================
# 4. Real Multi-Course Regression Test (All 4 Courses Published)
# =============================================================================

@pytest.mark.parametrize("course_filename", [
    "saul_control_optimo.json",
    "gavilano_pre_parcial.json",
    "asyntotic_estatistics_v7.json",
    "solow_growth_model.json",
])
def test_real_published_courses_zero_r23_errors(course_filename: str) -> None:
    """All 4 published courses must pass scan_lexical and validate_course_content with 0 R-23 errors."""
    course_path = REPO_ROOT / "courses" / course_filename
    assert course_path.exists(), f"Course file not found: {course_path}"

    raw_text = course_path.read_text(encoding="utf-8")

    # End-to-end course validation: validate_course_content runs Pass 1 (scan_lexical)
    # followed by Pass 2/3 (extended quality and strict rules in memory) with strict=True.
    result = validate_course_content(raw_text, strict=True)
    r23_all = [e for e in result.errors if e.rule_id == "R-23"]
    assert len(r23_all) == 0, f"{course_filename} has R-23 errors: {r23_all}"


# =============================================================================
# 5. Adversarial Hardening Cases (Mejorador Phase 2)
# =============================================================================

def test_compact_matrix_row_break_vs_overescape_raw_json() -> None:
    """Compact matrix row break \\\\\\\\frac (6 backslashes in raw JSON) must NOT trigger R-23, while 4 and 8 backslashes DO."""
    # 6 backslashes in raw JSON (\\\frac in memory): \\ row break + \frac command
    raw_6_bs = r'{"stem": "$\\begin{bmatrix} 1 & 2 \\\\\\frac{3}{4} & 5 \\end{bmatrix}$"}'
    errs_6 = scan_lexical(raw_6_bs)
    r23_6 = [e for e in errs_6 if e.rule_id == "R-23"]
    assert len(r23_6) == 0

    parsed_6 = json.loads(raw_6_bs)
    rule_errs_6 = check_extended_quality_rules({"questions": [{"id": "Q-01", "stem": parsed_6["stem"]}]})
    assert len([e for e in rule_errs_6 if e.rule_id == "R-23"]) == 0

    # 4 backslashes in raw JSON (\\frac in memory): over-escaped command
    raw_4_bs = r'{"stem": "$\\begin{bmatrix} 1 & 2 \\\\frac{3}{4} & 5 \\end{bmatrix}$"}'
    errs_4 = scan_lexical(raw_4_bs)
    r23_4 = [e for e in errs_4 if e.rule_id == "R-23" and e.code == "ERR_LATEX_OVERESCAPE"]
    assert len(r23_4) == 1

    # 8 backslashes in raw JSON (\\\\frac in memory): over-escaped command
    raw_8_bs = r'{"stem": "$\\begin{bmatrix} 1 & 2 \\\\\\\\frac{3}{4} & 5 \\end{bmatrix}$"}'
    errs_8 = scan_lexical(raw_8_bs)
    r23_8 = [e for e in errs_8 if e.rule_id == "R-23" and e.code == "ERR_LATEX_OVERESCAPE"]
    assert len(r23_8) == 1


def test_compact_matrix_row_break_memory_parity() -> None:
    """In memory: 3 backslashes (odd parity >= 3) within matrix produces 0 errors, while 2 and 4 backslashes trigger ERR_LATEX_OVERESCAPE."""
    # 3 backslashes: row break + \frac
    data_3 = {
        "questions": [
            {
                "id": "Q-ODD",
                "stem": r"$\begin{bmatrix} 1 & 2 \\\frac{3}{4} & 5 \end{bmatrix}$",
            }
        ]
    }
    errs_3 = check_extended_quality_rules(data_3)
    assert len([e for e in errs_3 if e.rule_id == "R-23"]) == 0

    # 2 backslashes: over-escape
    data_2 = {
        "questions": [
            {
                "id": "Q-EVEN-2",
                "stem": r"$\begin{bmatrix} 1 & 2 \\frac{3}{4} & 5 \end{bmatrix}$",
            }
        ]
    }
    errs_2 = check_extended_quality_rules(data_2)
    over_2 = [e for e in errs_2 if e.rule_id == "R-23" and e.code == "ERR_LATEX_OVERESCAPE"]
    assert len(over_2) == 1

    # 4 backslashes: over-escape
    data_4 = {
        "questions": [
            {
                "id": "Q-EVEN-4",
                "stem": r"$\begin{bmatrix} 1 & 2 \\\\frac{3}{4} & 5 \end{bmatrix}$",
            }
        ]
    }
    errs_4 = check_extended_quality_rules(data_4)
    over_4 = [e for e in errs_4 if e.rule_id == "R-23" and e.code == "ERR_LATEX_OVERESCAPE"]
    assert len(over_4) == 1


def test_nested_and_multiple_matrices_in_single_math_block_allowed() -> None:
    """Nested environments (pmatrix within matrix/cases) and multiple matrices in single $...$ block pass without ERR_LATEX_INLINE_NEWLINE."""
    # Nested environments
    nested_data = {
        "questions": [
            {
                "id": "Q-NESTED",
                "stem": (
                    r"Considere el sistema $"
                    r"\begin{matrix} "
                    r"A = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix} \\ "
                    r"f(x) = \begin{cases} 1 & x \ge 0 \\ 0 & x < 0 \end{cases} "
                    r"\end{matrix}$."
                ),
            }
        ]
    }
    errs_nested = check_extended_quality_rules(nested_data)
    assert len([e for e in errs_nested if e.rule_id == "R-23"]) == 0

    # Multiple matrices in single math block
    multi_data = {
        "questions": [
            {
                "id": "Q-MULTI",
                "stem": (
                    r"Sean $A = \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix} "
                    r"\text{ y } B = \begin{bmatrix} 5 & 6 \\ 7 & 8 \end{bmatrix}$ dos matrices."
                ),
            }
        ]
    }
    errs_multi = check_extended_quality_rules(multi_data)
    assert len([e for e in errs_multi if e.rule_id == "R-23"]) == 0


def test_illegal_inline_linebreak_outside_nested_matrix_detected() -> None:
    """Linebreak outside nested matrix inside $...$ triggers ERR_LATEX_INLINE_NEWLINE."""
    data = {
        "questions": [
            {
                "id": "Q-ILLEGAL-NL",
                "stem": (
                    r"Sea $\begin{matrix} \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix} \end{matrix} "
                    r"\\ \text{ilegal}$ fuera de entorno."
                ),
            }
        ]
    }
    errs = check_extended_quality_rules(data)
    nl_errs = [e for e in errs if e.rule_id == "R-23" and e.code == "ERR_LATEX_INLINE_NEWLINE"]
    assert len(nl_errs) == 1
    assert nl_errs[0].item_id == "Q-ILLEGAL-NL"


def test_fill_in_the_blank_correct_answer_string_overescape_detected() -> None:
    """Over-escaped LaTeX in fill_in_the_blank string correct_answer triggers ERR_LATEX_OVERESCAPE."""
    data = {
        "course_id": "test_course",
        "questions": [
            {
                "id": "Q-FIB-STR",
                "interaction_type": "fill_in_the_blank",
                "stem": "Complete la expresión.",
                "correct_answer": r"\\frac{1}{2}",
            }
        ]
    }
    errs = check_extended_quality_rules(data)
    over_errs = [e for e in errs if e.rule_id == "R-23" and e.code == "ERR_LATEX_OVERESCAPE"]
    assert len(over_errs) == 1
    assert "correct_answer" in over_errs[0].message
    assert over_errs[0].item_id == "Q-FIB-STR"


def test_fill_in_the_blank_correct_answer_dict_overescape_detected() -> None:
    """Over-escaped LaTeX in fill_in_the_blank dict correct_answer triggers ERR_LATEX_OVERESCAPE on each field."""
    data = {
        "course_id": "test_course",
        "questions": [
            {
                "id": "Q-FIB-DICT",
                "interaction_type": "fill_in_the_blank",
                "stem": "Complete la expresión.",
                "correct_answer": {
                    "value": r"\\frac{a}{b}",
                    "expression": r"$x = \\frac{a}{b}$",
                    "canonical_algebraic": r"\\frac{a}{b}",
                    "accepted_equivalents": [r"\\frac{a}{b}", "0.5"],
                },
            }
        ]
    }
    errs = check_extended_quality_rules(data)
    over_errs = [e for e in errs if e.rule_id == "R-23" and e.code == "ERR_LATEX_OVERESCAPE"]
    # All 4 occurrences must be detected
    assert len(over_errs) == 4
    messages = [e.message for e in over_errs]
    assert any("correct_answer.value" in m for m in messages)
    assert any("correct_answer.expression" in m for m in messages)
    assert any("correct_answer.canonical_algebraic" in m for m in messages)
    assert any("correct_answer.accepted_equivalents[0]" in m for m in messages)


def test_fill_in_the_blank_correct_answer_clean_latex_allowed() -> None:
    """Clean LaTeX in fill_in_the_blank correct_answer passes without R-23 errors."""
    data = {
        "course_id": "test_course",
        "questions": [
            {
                "id": "Q-FIB-CLEAN",
                "interaction_type": "fill_in_the_blank",
                "stem": "Complete la expresión.",
                "correct_answer": {
                    "value": r"\frac{a}{b}",
                    "expression": r"$x = \frac{a}{b}$",
                    "canonical_algebraic": r"\frac{a}{b}",
                    "accepted_equivalents": [r"\frac{a}{b}", "0.5"],
                },
            }
        ]
    }
    errs = check_extended_quality_rules(data)
    r23_errs = [e for e in errs if e.rule_id == "R-23"]
    assert len(r23_errs) == 0


def test_adversarial_edge_cases_matrices_and_delimiters() -> None:
    """Endurece casos borde: cadenas vacías, saltos con opciones [4pt], múltiples bloques inline/display y delimitadores con escape."""
    # 1. Cadenas vacías
    assert len(scan_lexical("")) == 0
    empty_res = check_extended_quality_rules({"questions": [{"id": "Q-EMPTY", "stem": "", "correct_answer": ""}]})
    assert len([e for e in empty_res if e.rule_id == "R-23"]) == 0

    # 2. Saltos de fila en matriz con opciones de espaciado vertical [4pt] y espacios
    matrix_spacing = {
        "questions": [
            {
                "id": "Q-SPACING",
                "stem": r"$\begin{pmatrix} 1 & 2 \\\\[4pt] 3 & 4 \\   [10pt] 5 & 6 \end{pmatrix}$",
            }
        ]
    }
    spacing_res = check_extended_quality_rules(matrix_spacing)
    assert len([e for e in spacing_res if e.rule_id == "R-23"]) == 0

    # 3. Múltiples bloques $...$ y $$...$$ en una misma cadena
    multi_blocks = {
        "questions": [
            {
                "id": "Q-BLOCKS",
                "stem": (
                    r"Texto con $x = 1$, luego $$y = \begin{pmatrix} a \\ b \end{pmatrix}$$, "
                    r"y finalmente $z = \begin{matrix} 1 \\ 2 \end{matrix}$."
                ),
            }
        ]
    }
    blocks_res = check_extended_quality_rules(multi_blocks)
    assert len([e for e in blocks_res if e.rule_id == "R-23"]) == 0

    # 4. Bloques mixtos donde uno contiene un salto ilegal
    mixed_illegal = {
        "questions": [
            {
                "id": "Q-MIXED",
                "stem": r"Válido $x = 1$, ilegal $a \\ b$ aquí, y válido $y = 2$.",
            }
        ]
    }
    mixed_res = check_extended_quality_rules(mixed_illegal)
    nl_errs = [e for e in mixed_res if e.rule_id == "R-23" and e.code == "ERR_LATEX_INLINE_NEWLINE"]
    assert len(nl_errs) == 1
    assert nl_errs[0].item_id == "Q-MIXED"

    # 5. Escaped dollar \$ coexistiendo con saltos legítimos de matriz
    escaped_dollar = {
        "questions": [
            {
                "id": "Q-DOLLAR",
                "stem": r"El precio es \$50 para $\begin{matrix} 1 & 2 \\ 3 & 4 \end{matrix}$ unidades.",
            }
        ]
    }
    dollar_res = check_extended_quality_rules(escaped_dollar)
    assert len([e for e in dollar_res if e.rule_id in ("R-20", "R-23")]) == 0
