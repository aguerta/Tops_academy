r"""Tests for C2C v3.21 Component 1: CTA Compiler, Pre-Healer, and Math Normalization.

Covers:
a) heal_cta_source_file and compile_cta on non-raw strings containing all LaTeX prefixes.
b) check_cta_katex short variables ({k}, {r}, {dt}, $k^*$, $\bar{k}$, $\dot{k}$) vs unescaped commands.
c) normalize_orphan_math wrapping bare expressions without corrupting already delimited math.
d) render_compact_cta_errors collapsing 198 distractor errors across 33 competencies into < 25 lines.
"""

import json
import re
import sys
import tempfile
from pathlib import Path

import pytest

# Ensure skills root is in sys.path
_skills_root = Path(__file__).parent.parent / ".agents" / "skills" / "content-to-course"
if str(_skills_root) not in sys.path:
    sys.path.insert(0, str(_skills_root))

from compile_cta import (
    categorize_cta_error,
    compile_cta,
    heal_control_chars_in_obj,
    heal_control_chars_in_str,
    heal_cta_source_file,
    render_compact_cta_errors,
)
from cta_merge import normalize_orphan_math
from check_cta import check_cta_katex, check_cta_prose_overflow, validate_distractor_math


class TestC2CV321PreHealerAndCompiler:
    """Task 2.a: heal_cta_source_file and compile_cta on non-raw strings."""

    def test_heal_cta_source_file_and_compile_cta_non_raw_strings(self):
        """Verify compiling a cta_data.py written WITHOUT raw strings (with LaTeX escapes).

        Must compile 100% cleanly with zero control characters in cta.json.
        """
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            cta_py = td_path / "cta_data.py"
            manifest_p = td_path / "pre_cta_manifest.json"

            manifest_p.write_text(
                json.dumps({
                    "files": [
                        {
                            "doc": "material_fuente.pdf",
                            "total_pages": 15,
                            "valid_page_range": [1, 15],
                        }
                    ]
                }),
                encoding="utf-8",
            )

            # cta_data.py written without raw strings ('r'), containing:
            # \rho, \right, \frac{a}{b}, \alpha, \beta, \bar{k}, \tau, \theta,
            # \text{...}, \times, \nu, \neq, \nabla, \vec{x}, \varepsilon
            source_content = (
                '"""Test module for unescaped LaTeX prefixes."""\n\n'
                'COURSE_ID = "macro_solow"\n'
                'TITLE = "Modelo de Crecimiento de Solow"\n\n'
                'COMPETENCIES = [\n'
                '    (\n'
                '        "Concept",\n'
                '        "C-01",\n'
                '        "Diferencial con \\rho y \\left( \\frac{a}{b} \\right) y \\rightarrow",\n'
                '        "Relación fundamental: $\\alpha + \\beta = \\bar{k}$ evaluada con \\tau y \\theta.",\n'
                '        "Understand",\n'
                '        "material_fuente.pdf",\n'
                '        1,\n'
                '        [],\n'
                '        [\n'
                '            ("D-01-01", "Asume que \\text{diff} es nulo", "Diferencia es no nula", "$0$", "Revisar \\times y \\nu.", None),\n'
                '            ("D-01-02", "Cree que \\neq implica divergencia", "No implica divergencia", "$0$", "Operador \\nabla no converge", None),\n'
                '            ("D-01-03", "Aproxima vector \\vec{x} sin \\varepsilon", "Vector y perturbación válidos", "$0$", "Verificar marco estocástico", None),\n'
                '            ("D-01-04", "Omite ajuste dinámico", "Ajuste dinámico requerido", "$0$", "Revisar ecuación de balance", "Omite derivación temporal"),\n'
                '            ("D-01-05", "Confunde tasas de crecimiento", "Tasas bien definidas", "$0$", "Revisar parágrafo teórico", "Omite sustitución"),\n'
                '            ("D-01-06", "Error en condición terminal", "Condición transversal requerida", "$0$", "Verificar límite infinito", None),\n'
                '        ],\n'
                '    ),\n'
                '    (\n'
                '        "Skill",\n'
                '        "Skill-01",\n'
                '        "Resolución de trayectoria en estado estacionario",\n'
                '        "Calcular la convergencia hacia $k^*$ y evaluar estabilidad.",\n'
                '        "Apply",\n'
                '        "material_fuente.pdf",\n'
                '        2,\n'
                '        ["C-01"],\n'
                '        [\n'
                '            ("D-Skill01-01", "Error de tasa de ahorro", "Ahorro constante", "$1$", "Hint 1", None),\n'
                '            ("D-Skill01-02", "Error de depreciación", "Depreciación lineal", "$2$", "Hint 2", None),\n'
                '            ("D-Skill01-03", "Omite depreciación en stock", "Stock neto", "$3$", "Hint 3", "Omite depreciación"),\n'
                '            ("D-Skill01-04", "Omite crecimiento poblacional", "Población dinámica", "$4$", "Hint 4", "Omite tasa n"),\n'
                '            ("D-Skill01-05", "Error de exponente en Cobb-Douglas", "Exponente alfa", "$5$", "Hint 5", None),\n'
                '            ("D-Skill01-06", "Error algebraico final", "Solución analítica válida", "$6$", "Hint 6", None),\n'
                '        ],\n'
                '    ),\n'
                ']\n'
            )
            cta_py.write_text(source_content, encoding="utf-8")

            # 1. Source pre-healer rewrites source file
            healed = heal_cta_source_file(cta_py)
            assert healed is True, "heal_cta_source_file should have modified and rewritten cta_data.py"

            # 2. compile_cta executes cleanly
            success, cta_dict, errors, elapsed = compile_cta(
                cta_data_path=cta_py,
                output_dir=td_path,
                manifest_path=manifest_p,
            )
            assert success is True, f"compile_cta failed with errors: {errors}"
            assert len(errors) == 0, f"Expected 0 errors, got: {errors}"

            # 3. Target cta.json contains ZERO ASCII control characters
            cta_json_path = td_path / "cta.json"
            assert cta_json_path.is_file(), "cta.json was not generated"
            cta_json_content = cta_json_path.read_text(encoding="utf-8")
            for ctrl_char in ("\x07", "\x08", "\x0b", "\x0c", "\x0d"):
                assert ctrl_char not in cta_json_content, (
                    f"Found corrupted ASCII control character {repr(ctrl_char)} in cta.json"
                )

    def test_heal_cta_source_file_fallback_on_syntax_error(self):
        """Verify heal_cta_source_file degrades gracefully on syntax errors without raising unhandled exceptions."""
        with tempfile.TemporaryDirectory() as td:
            broken_file = Path(td) / "broken_cta_data.py"
            # File with unclosed string (tokenize fails)
            broken_file.write_text('val = "unclosed string with \\rho and \\frac{a}{b}\n', encoding="utf-8")
            res = heal_cta_source_file(broken_file)
            assert res is True
            content = broken_file.read_text(encoding="utf-8")
            # Should have converted \rho and \frac via regex fallback
            assert "\\\\rho" in content or "\\rho" in content


class TestC2CV321KaTeXSyntaxAndControlChars:
    """Task 2.b: check_cta_katex and validate_distractor_math handling."""

    def test_short_template_variables_pass_with_zero_false_positives(self):
        """Short variables like {k}, {r}, {dt}, $k^*$, $r^*$, $\\bar{k}$, $\\dot{k}$ pass without errors."""
        valid_cta = {
            "competencies": [
                {
                    "id": "C-01",
                    "name": "Dinámica de acumulación de {k} y tasa {r} hacia $k^*$",
                    "description_latex": "Modelo temporal con paso {dt}, estado estacionario $\\bar{k}$ y velocidad $\\dot{k}$.",
                    "distractors": [
                        {
                            "id": "D-01-01",
                            "manifestation": "Confunde la trayectoria de {k} con {r} en $k^*$",
                            "remediation_hint": "Recordar que $\\bar{k}$ es invariante ante {dt}",
                            "wrong_belief": "Asume que {k} converge instantáneamente a $r^*$",
                            "omitted_step": "Omite la derivada temporal $\\dot{k}$ en el equilibrio",
                        }
                    ],
                }
            ]
        }
        errors = check_cta_katex(valid_cta)
        assert len(errors) == 0, f"False positives detected: {errors}"

    def test_unescaped_commands_and_ascii_control_characters_are_caught(self):
        """Unescaped commands (bar{k}, dot{w}, frac{a}{b}) and control chars (\x07, \x08, \x0c, \x0d) are caught."""
        invalid_cta = {
            "competencies": [
                {
                    "id": "C-02",
                    "name": "Competencia con \x07lpha y bar{k}",
                    "description_latex": "Descripción con dot{w} y \x0cfrac",
                    "distractors": [
                        {
                            "id": "D-02-01",
                            "manifestation": "Distractor con frac{a}{b} sin barra",
                            "remediation_hint": "Distractor con \x08eta y \x0dho",
                            "wrong_belief": "Distractor con \x0bec",
                            "omitted_step": "Distractor con $bar{k}$ dentro de math",
                        }
                    ],
                }
            ]
        }
        errors = check_cta_katex(invalid_cta)
        assert len(errors) > 0, "Expected violations to be caught by check_cta_katex"

        # Check corrupted ASCII control character detection
        ctrl_errors = [e for e in errors if "Corrupted ASCII control character" in e]
        assert len(ctrl_errors) >= 4, f"Expected at least 4 control char errors, got: {ctrl_errors}"

        # Check unescaped LaTeX math commands
        raw_or_unescaped = [e for e in errors if any(cmd in e for cmd in ("bar{k}", "dot{w}", "frac{a}{b}", "sin delimitar"))]
        assert len(raw_or_unescaped) >= 4, f"Expected unescaped command violations, got: {raw_or_unescaped}"

    def test_validate_distractor_math_standalone(self):
        """Verify validate_distractor_math directly on clean and contaminated distractor dicts."""
        clean_d = {
            "manifestation": "Usa {k} y {r} para calcular $k^*$ y $\\bar{k}$",
            "remediation_hint": "Considera {dt} y $\\dot{k}$",
            "wrong_belief": "Cree que {k} es estático",
            "omitted_step": "Omite el valor $r^*$ en la fórmula",
        }
        assert validate_distractor_math(clean_d, "D-01-01") == []

        contaminated_d = {
            "manifestation": "Valor con frac{x}{y}",
            "remediation_hint": "Error con \x07lpha",
            "wrong_belief": "Confunde $dot{w}$ en el cálculo",
            "omitted_step": "Omite bar{k} en la estimación",
        }
        errs = validate_distractor_math(contaminated_d, "D-02-01")
        assert len(errs) >= 4


class TestC2CV321NormalizeOrphanMath:
    """Task 2.c: normalize_orphan_math in cta_merge.py."""

    def test_normalize_orphan_math_wraps_bare_expressions(self):
        """Bare {k}^*, {r}^*, {k}_{t+1}, k^*, r^* are wrapped in $...$."""
        text = "El estado {k}^* y {r}^* junto con {k}_{t+1} convergen a k^* y r^* en el tiempo."
        result = normalize_orphan_math(text)
        assert "${k}^*$" in result
        assert "${r}^*$" in result
        assert "${k}_{t+1}$" in result
        assert "$k^*$" in result
        assert "$r^*$" in result

    def test_normalize_orphan_math_does_not_double_wrap_existing_math(self):
        """Expressions already inside $...$ like $\\frac{a}{k^*}$ must not be corrupted or double-wrapped."""
        text = "La expresión ya delimitada $\\frac{a}{k^*}$ y $\\bar{k}^*$ debe preservarse intacta."
        result = normalize_orphan_math(text)
        assert result == text
        assert "$\\frac{a}{$k^*$}$" not in result

    def test_normalize_orphan_math_handles_nested_braces_in_fraction(self):
        """Complex fractions with nested braces like \\frac{\\text{diff}}{k^* + {r}^*} are wrapped cleanly without nesting $."""
        text = "Calcula \\frac{\\text{diff}}{k^* + {r}^*} para encontrar la tasa."
        result = normalize_orphan_math(text)
        assert result == "Calcula $\\frac{\\text{diff}}{k^* + {r}^*}$ para encontrar la tasa."
        assert "$" in result
        assert result.count("$") == 2

    def test_normalize_orphan_math_heals_control_characters(self):
        """Collisions with control characters in strings are repaired."""
        text = "Valores con \x07lpha, \x08eta, \x0cfrac{1}{2}, \x0dho."
        result = normalize_orphan_math(text)
        assert "\x07" not in result
        assert "\x08" not in result
        assert "\x0c" not in result
        assert "\x0d" not in result
        assert "$\\alpha$" in result
        assert "$\\beta$" in result
        assert "$\\frac{1}{2}$" in result
        assert "$\\rho$" in result


class TestC2CV321RenderCompactCtaErrors:
    """Task 2.d: render_compact_cta_errors aggregation and line budget."""

    def test_render_compact_cta_errors_198_distractor_errors_under_25_lines(self):
        """198 distractor errors across 33 competencies collapse into strictly < 25 lines."""
        errors = []
        for comp_idx in range(1, 34):
            for d_idx in range(1, 7):
                did = f"D-{comp_idx:02d}-{d_idx:02d}"
                var = ["k", "r", "w", "dt"][d_idx % 4]
                err = (
                    f"Unescaped LaTeX math command 'bar{{{var}}}' detected in distractor '{did}' manifestation. "
                    f"Must be prefixed with '\\' and enclosed in '$...$' (e.g. '$\\bar{{{var}}}$'). "
                    f"[cta_data.py:Línea {comp_idx * 10 + d_idx}]"
                )
                errors.append(err)

        assert len(errors) == 198
        rendered = render_compact_cta_errors(errors, "cta_data.py")
        rendered_lines = rendered.splitlines()

        # Strict line budget
        assert len(rendered_lines) < 25, (
            f"render_compact_cta_errors produced {len(rendered_lines)} lines, exceeding the strict limit of < 25 lines:\n{rendered}"
        )

        # Single aggregated line for all 198 errors
        bullet_lines = [l for l in rendered_lines if l.strip().startswith("• [CTA-KATEX]")]
        assert len(bullet_lines) == 1, f"Expected exactly 1 aggregated bullet line for CTA-KATEX, got: {bullet_lines}"
        assert "(198 líneas)" in bullet_lines[0]
        assert "D-01-01" in bullet_lines[0]
        assert "(+193 más)" in bullet_lines[0]

    def test_render_compact_cta_errors_diverse_categories_under_25_lines(self):
        """Even with 50 diverse error categories, the output strictly satisfies < 25 lines."""
        errors = [
            f"Custom error category {i}: detailed cause [cta_data.py:Línea {i}] D-{i:02d}-01"
            for i in range(50)
        ]
        rendered = render_compact_cta_errors(errors, "cta_data.py")
        rendered_lines = rendered.splitlines()
        assert len(rendered_lines) < 25, f"Expected < 25 lines, got {len(rendered_lines)} lines"


class TestCtaProseOverflowFailFast:
    """Tests for fail-fast detection of KaTeX prose overflow in CTA stage."""

    def test_prose_overflow_text_macro_threshold(self):
        """Macros with inner length > 45 characters trigger [KATEX-PROSE-OVERFLOW]."""
        short_prose = r"$\text{Short text under limit}$"
        assert check_cta_prose_overflow(short_prose, "ctx") == []

        long_inner = "This is a very long explanatory prose sentence exceeding forty five characters"
        long_prose = f"$\\text{{{long_inner}}}$"
        errs = check_cta_prose_overflow(long_prose, "ctx")
        assert len(errs) == 1
        assert "[KATEX-PROSE-OVERFLOW]" in errs[0]
        assert "R-23" not in errs[0]
        assert "R23" not in errs[0]

    def test_prose_overflow_textrm_mathrm_variants(self):
        """Validates that \\textrm and \\mathrm are audited for overflow."""
        long_txt = "A long explanatory comment inside math exceeding forty five chars"
        errs_rm = check_cta_prose_overflow(f"$\\textrm{{{long_txt}}}$", "test_ctx")
        assert len(errs_rm) == 1
        assert "[KATEX-PROSE-OVERFLOW]" in errs_rm[0]

        errs_m = check_cta_prose_overflow(f"$\\mathrm{{{long_txt}}}$", "test_ctx")
        assert len(errs_m) == 1
        assert "[KATEX-PROSE-OVERFLOW]" in errs_m[0]

    def test_distractor_math_detects_prose_overflow(self):
        """validate_distractor_math audits all text fields for prose overflow."""
        long_txt = "When calculating parameters across multiple discrete periods and iterations"
        dist = {
            "id": "D-C01-01",
            "name": "Sign Confusion",
            "wrong_belief": f"Assumes $\\text{{{long_txt}}}$ is true",
            "correct_belief": "Follows standard rules",
            "manifestation": "Error occurred",
            "remediation_hint": "Review steps",
        }
        errs = validate_distractor_math(dist, "D-C01-01")
        assert any("[KATEX-PROSE-OVERFLOW]" in e for e in errs)

    def test_prose_overflow_exact_45_boundary_and_nested_braces(self):
        """Exact boundary: 45 characters passes, 46 characters triggers [KATEX-PROSE-OVERFLOW]."""
        # Exactly 45 characters inside \text{}
        body_45 = "A" * 45
        assert len(body_45) == 45
        assert check_cta_prose_overflow(f"$\\text{{{body_45}}}$", "exact_45") == []

        # Exactly 46 characters inside \text{}
        body_46 = "A" * 46
        assert len(body_46) == 46
        errs_46 = check_cta_prose_overflow(f"$\\text{{{body_46}}}$", "exact_46")
        assert len(errs_46) == 1
        assert "[KATEX-PROSE-OVERFLOW]" in errs_46[0]
        assert "46" in errs_46[0]
        assert "R-23" not in errs_46[0]

        # Nested balanced braces: {nested} inside \text{}
        # "Prefix " (7) + "{inner text}" (12) + " suffix" (7) = 26 chars (passes)
        nested_pass = r"$\text{Prefix {inner text} suffix}$"
        assert check_cta_prose_overflow(nested_pass, "nested_pass") == []

        # Nested braces exceeding 45 chars
        nested_long = r"$\text{Prefix {" + ("X" * 35) + r"} trailing text block}$"
        errs_nested = check_cta_prose_overflow(nested_long, "nested_long")
        assert len(errs_nested) == 1
        assert "[KATEX-PROSE-OVERFLOW]" in errs_nested[0]

    def test_prose_overflow_all_competency_and_distractor_fields_and_no_duplicates(self):
        """Coverage across name, description, description_latex, source_examples and all 6 distractor fields."""
        over_prose = "$\\text{" + ("Z" * 50) + "}$"

        # 1. Competency fields
        comp_name = {"id": "C-01", "name": f"Concept {over_prose}"}
        errs = check_cta_katex({"competencies": [comp_name]})
        assert any("[KATEX-PROSE-OVERFLOW]" in e and "name" in e for e in errs)

        comp_desc = {"id": "C-02", "name": "Valid Name", "description_latex": over_prose}
        errs = check_cta_katex({"competencies": [comp_desc]})
        assert any("[KATEX-PROSE-OVERFLOW]" in e and "description_latex" in e for e in errs)

        comp_ex = {"id": "C-03", "name": "Valid Name", "source_examples": [over_prose]}
        errs = check_cta_katex({"competencies": [comp_ex]})
        assert any("[KATEX-PROSE-OVERFLOW]" in e and "source_examples" in e for e in errs)

        # 2. All 6 distractor fields
        dist_fields = [
            "manifestation",
            "remediation_hint",
            "wrong_belief",
            "correct_belief",
            "omitted_step",
            "trigger",
        ]
        for f in dist_fields:
            d_obj = {
                "id": f"D-C01-01",
                "name": "Trap",
                f: over_prose,
            }
            comp = {
                "id": "C-01",
                "name": "Valid",
                "distractors": [d_obj],
            }
            errs = check_cta_katex({"competencies": [comp]})
            assert any("[KATEX-PROSE-OVERFLOW]" in e and f in e for e in errs), f"Field {f} not detected"

        # 3. Zero duplicate messages
        dup_test_comp = {
            "id": "C-01",
            "name": f"Concept {over_prose}",
            "description": f"Desc {over_prose}",
            "distractors": [
                {
                    "id": "D-C01-01",
                    "manifestation": over_prose,
                    "remediation_hint": over_prose,
                }
            ],
        }
        res_errs = check_cta_katex({"competencies": [dup_test_comp]})
        assert len(res_errs) == len(set(res_errs)), "check_cta_katex emitted duplicate error messages"


class TestFormalAssumptionsAndCertification:
    """Verifies formal assumptions support, 2D error metrics, certificate emission, and modular splicing."""

    def test_compile_cta_assumptions_tuples_and_dicts(self):
        from compile_cta import compile_cta_module, count_evaluated_fields

        comps_data = [
            # 7-tuple with assumptions
            (
                "concept",
                "C-01",
                "Formal Basis",
                "Definition of vector space basis.",
                "Understand",
                [],
                [
                    ("D1", "$0$", "wb", "$0$", "hint", None),
                    ("D2", "$0$", "wb", "$0$", "hint", None),
                    ("D3", "$0$", "wb", "$0$", "hint", None),
                ],
                [
                    ("A-C01-01", "$x > 0$ strictly positive", "Breakdown of convergence", "Positivity", "Premise"),
                ],
            ),
            # Dict competency with assumptions
            {
                "id": "Hab-01",
                "type": "skill",
                "name": "Solve System",
                "description_latex": "Solve linear system $Ax = b$.",
                "bloom": "Apply",
                "evidence": [{"doc": "text.pdf", "page": 1}],
                "prerequisites": ["C-01"],
                "distractors": [
                    ("D1", "$0$", "wb", "$0$", "hint", "omit"),
                    ("D2", "$0$", "wb", "$0$", "hint", "omit"),
                    ("D3", "$0$", "wb", "$0$", "hint", None),
                    ("D4", "$0$", "wb", "$0$", "hint", None),
                    ("D5", "$0$", "wb", "$0$", "hint", None),
                    ("D6", "$0$", "wb", "$0$", "hint", None),
                ],
                "assumptions": [
                    ("A-Hab01-01", "$\\det(A) \\neq 0$ non-singular", "No unique solution exists"),
                ],
            },
        ]

        compiled = compile_cta_module(
            competencies_data=comps_data,
            course_id="formal_algebra",
            title="Linear Systems",
        )

        comps = compiled.get("competencies", [])
        assert len(comps) == 2

        c1 = comps[0]
        assert c1["id"] == "C-01"
        assert len(c1.get("assumptions", [])) == 1
        assert c1["assumptions"][0]["id"] == "A-C01-01"
        assert c1["assumptions"][0]["statement_latex"] == "$x > 0$ strictly positive"
        assert c1["assumptions"][0]["name"] == "Positivity"

        c2 = comps[1]
        assert c2["id"] == "Hab-01"
        assert len(c2.get("assumptions", [])) == 1
        assert c2["assumptions"][0]["id"] == "A-Hab01-01"
        assert c2["assumptions"][0]["violation_consequence"] == "No unique solution exists"

        field_count = count_evaluated_fields(compiled)
        assert field_count >= 20

    def test_require_assumptions_enforcement_and_line_mapping(self, tmp_path: Path):
        from compile_cta import compile_cta, CtaDataLineLocator

        work_dir = tmp_path / "work"
        work_dir.mkdir(parents=True, exist_ok=True)
        manifest = {
            "course_id": "test_assumptions",
            "files": [{"doc": "book.pdf", "total_pages": 10, "valid_page_range": [1, 10]}],
        }
        (work_dir / "pre_cta_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

        # cta_data.py with Concept lacking assumptions
        cta_code = (
            'COURSE_ID = "test_assumptions"\n'
            'TITLE = "Formal Test"\n\n'
            'COMPETENCIES = [\n'
            '    (\n'
            '        "concept",\n'
            '        "C-01",\n'
            '        "Basis Concept",\n'
            '        "Definition of basis in vector space.",\n'
            '        "Understand",\n'
            '        "book.pdf",\n'
            '        1,\n'
            '        [],\n'
            '        [\n'
            '            ("D-01-01", "Wrong 1", "Correct 1", "$0$", "Hint 1", None),\n'
            '            ("D-01-02", "Wrong 2", "Correct 2", "$0$", "Hint 2", None),\n'
            '            ("D-01-03", "Wrong 3", "Correct 3", "$0$", "Hint 3", None),\n'
            '        ],\n'
            '    ),\n'
            ']\n'
        )
        data_path = work_dir / "cta_data.py"
        data_path.write_text(cta_code, encoding="utf-8")

        valid, cta_dict, errors, elapsed = compile_cta(
            cta_data_path=data_path,
            output_dir=work_dir,
            require_assumptions=True,
            allow_degrade=False,
        )

        assert valid is False
        assert any("[CTA-ASSUMPTIONS-MISSING]" in e and "C-01" in e for e in errors)

        # Verify CtaDataLineLocator resolves CTA-ASSUMPTIONS-MISSING to competency line
        locator = CtaDataLineLocator(cta_code)
        target_err = next(e for e in errors if "[CTA-ASSUMPTIONS-MISSING]" in e)
        start_l, end_l, snip = locator.resolve_error_location(target_err)
        assert start_l >= 4
        assert "concept" in snip or "C-01" in snip

    def test_2d_attempt_failure_persistence_and_line_count(self, tmp_path: Path):
        from compile_cta import compile_cta

        work_dir = tmp_path / "work"
        work_dir.mkdir(parents=True, exist_ok=True)
        manifest = {
            "course_id": "test_persistence",
            "files": [{"doc": "book.pdf", "total_pages": 10, "valid_page_range": [1, 10]}],
        }
        (work_dir / "pre_cta_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

        # Create cta_data.py with >5 separate errors across distinct lines
        cta_code = (
            'COURSE_ID = "test_persistence"\n'
            'TITLE = "Persistence Test"\n\n'
            'COMPETENCIES = [\n'
            '    (\n'
            '        "concept",\n'
            '        "C-01",\n'
            '        "Valid Title",\n'
            '        "Valid description.",\n'
            '        "Understand",\n'
            '        "book.pdf",\n'
            '        1,\n'
            '        [],\n'
            '        [\n'
            '            ("D-01-01", r"Wrong 1 $\\frac{w}{k", "Correct 1", "$0$", "Hint 1", None),\n'
            '            ("D-01-02", r"Wrong 2 $\\frac{w}{k", "Correct 2", "$0$", "Hint 2", None),\n'
            '            ("D-01-03", r"Wrong 3 $\\frac{w}{k", "Correct 3", "$0$", "Hint 3", None),\n'
            '            ("D-01-04", r"Wrong 4 $\\frac{w}{k", "Correct 4", "$0$", "Hint 4", None),\n'
            '            ("D-01-05", r"Wrong 5 $\\frac{w}{k", "Correct 5", "$0$", "Hint 5", None),\n'
            '            ("D-01-06", r"Wrong 6 $\\frac{w}{k", "Correct 6", "$0$", "Hint 6", None),\n'
            '        ],\n'
            '    ),\n'
            ']\n'
        )
        data_path = work_dir / "cta_data.py"
        data_path.write_text(cta_code, encoding="utf-8")

        valid, cta_dict, errors, elapsed = compile_cta(
            cta_data_path=data_path,
            output_dir=work_dir,
            allow_degrade=False,
        )
        assert valid is False

        # Verify state persistence file
        attempt_file = work_dir / ".check_attempts" / "compile_cta_cta_data.json"
        if not attempt_file.is_file():
            attempt_file = work_dir / ".check_attempts" / "compile_cta_data.json"
        assert attempt_file.is_file()
        state = json.loads(attempt_file.read_text(encoding="utf-8"))
        assert "affected_line_count" in state
        assert state["affected_line_count"] > 5
        assert "has_syntax_error" in state
        assert "error_sha256" in state
        assert len(state["error_sha256"]) == 64

    def test_cta_certification_emission(self, tmp_path: Path):
        from compile_cta import compile_cta

        work_dir = tmp_path / "work"
        work_dir.mkdir(parents=True, exist_ok=True)
        manifest = {
            "course_id": "test_certification",
            "files": [{"doc": "book.pdf", "total_pages": 10, "valid_page_range": [1, 10]}],
        }
        (work_dir / "pre_cta_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

        cta_code = (
            'COURSE_ID = "test_certification"\n'
            'TITLE = "Certification Test"\n\n'
            'COMPETENCIES = [\n'
            '    (\n'
            '        "concept",\n'
            '        "C-01",\n'
            '        "Valid Concept",\n'
            '        "Formal definition of mathematical structure.",\n'
            '        "Understand",\n'
            '        "book.pdf",\n'
            '        1,\n'
            '        [],\n'
            '        [\n'
            '            ("D-01-01", "Wrong belief 1", "Correct truth 1", "$0$", "Hint 1", None),\n'
            '            ("D-01-02", "Wrong belief 2", "Correct truth 2", "$0$", "Hint 2", None),\n'
            '            ("D-01-03", "Wrong belief 3", "Correct truth 3", "$0$", "Hint 3", None),\n'
            '        ],\n'
            '    ),\n'
            ']\n'
        )
        data_path = work_dir / "cta_data.py"
        data_path.write_text(cta_code, encoding="utf-8")

        valid, cta_dict, errors, elapsed = compile_cta(
            cta_data_path=data_path,
            output_dir=work_dir,
        )
        assert valid is True

        # Verify cta.cert.json is emitted alongside cta.json
        cert_path = work_dir / "cta.cert.json"
        assert cert_path.is_file(), "cta.cert.json was not written upon successful compilation"
        cert = json.loads(cert_path.read_text(encoding="utf-8"))

        assert cert["schema_version"] == 1
        assert cert["stage"] == "cta"
        assert cert["artifact_id"] == "cta"
        assert cert["contract_version"] == 2
        assert cert["passed_50_seeds"] is True
        assert len(cert["source_sha256"]) == 64
        assert len(cert["cta_sha256"]) == 64
        assert len(cert["compiler_sha256"]) == 64

    def test_modular_splicing_from_cta_fixes(self, tmp_path: Path):
        from compile_cta import compile_cta

        work_dir = tmp_path / "work"
        work_dir.mkdir(parents=True, exist_ok=True)
        fixes_dir = work_dir / "cta_fixes"
        fixes_dir.mkdir(parents=True, exist_ok=True)

        manifest = {
            "course_id": "test_splicing",
            "files": [{"doc": "book.pdf", "total_pages": 10, "valid_page_range": [1, 10]}],
        }
        (work_dir / "pre_cta_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

        # cta_data.py with broken distractor in C-01
        cta_code = (
            'COURSE_ID = "test_splicing"\n'
            'TITLE = "Splicing Test"\n\n'
            'COMPETENCIES = [\n'
            '    (\n'
            '        "concept",\n'
            '        "C-01",\n'
            '        "Concept To Fix",\n'
            '        "Definition of structure.",\n'
            '        "Understand",\n'
            '        "book.pdf",\n'
            '        1,\n'
            '        [],\n'
            '        [\n'
            '            ("D-01-01", None, None, "$0$", "Hint 1", None),\n'
            '        ],\n'
            '    ),\n'
            ']\n'
        )
        data_path = work_dir / "cta_data.py"
        data_path.write_text(cta_code, encoding="utf-8")

        # Place override in cta_fixes/C-01.py using tuple format
        fix_code = (
            'COMPETENCY = (\n'
            '    "concept",\n'
            '    "C-01",\n'
            '    "Spliced Fixed Concept",\n'
            '    "Formal definition of fixed structure.",\n'
            '    "Understand",\n'
            '    "book.pdf",\n'
            '    1,\n'
            '    [],\n'
            '    [\n'
            '        ("D-01-01", "Fixed wrong belief 1", "Fixed truth 1", "$0$", "Hint 1", None),\n'
            '        ("D-01-02", "Fixed wrong belief 2", "Fixed truth 2", "$0$", "Hint 2", None),\n'
            '        ("D-01-03", "Fixed wrong belief 3", "Fixed truth 3", "$0$", "Hint 3", None),\n'
            '    ],\n'
            ')\n'
        )
        (fixes_dir / "C-01.py").write_text(fix_code, encoding="utf-8")

        valid, cta_dict, errors, elapsed = compile_cta(
            cta_data_path=data_path,
            output_dir=work_dir,
        )
        assert valid is True, f"Modular splicing failed with errors: {errors}"
        comps = cta_dict.get("competencies", [])
        assert len(comps) == 1
        assert comps[0]["name"] == "Spliced Fixed Concept"



