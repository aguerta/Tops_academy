"""Tests for Error Aggregation and Line Consolidation in /content-to-course and validator platform.

Verifies:
1. Multi-seed invariant error grouping in dry-run (e.g. seeds 100..149 consolidated into 1 diagnostic block).
2. Production contract parity error grouping across questions (e.g. Q-001..Q-020 consolidated into 1 diagnostic block).
3. JSON source line indexing and line tracking in CTA parts and cta.json.
4. Multi-line consolidation of corrupted LaTeX escape sequences in AST check.
5. Multi-line consolidation in ValidationError, lexical scanner, and format_cli_output.
"""

import json
import sys
from pathlib import Path
import pytest

_skills_root = Path(__file__).parent.parent / ".agents" / "skills" / "content-to-course"
if str(_skills_root) not in sys.path:
    sys.path.insert(0, str(_skills_root))

from check_templates import (
    check_single_template,
    check_production_parity_for_competency,
    format_diagnostic_error,
)
from engine.sandbox import (
    check_latex_escape_corruption_structured,
    check_latex_escape_corruption,
)
from check_cta import (
    JsonLineLocator,
    build_json_line_index,
    check_cta_part,
    validate_cta_rules,
    check_cta_katex,
)
from validator.models import ValidationError, ValidationResult
from validator.cli import format_cli_output, consolidate_validation_errors
from validator.lexical_scanner import scan_lexical, consolidate_lexical_errors


class TestTemplateErrorAggregation:
    """Verifies invariant error aggregation across seeds in check_templates."""

    def test_dry_run_invariant_failure_aggregated_into_single_error(self):
        """When an invariant error affects all 50 dry-run seeds, exactly 1 diagnostic error is produced."""
        # Template where stem references undeclared variable {k_star}
        template_with_unreplaced_var = {
            "id": "T-AGGREGATION-TEST",
            "interaction_type": "multiple_choice_7_options",
            "stem": "En el modelo, el capital óptimo es {k_star} y el parámetro es {a}.",
            "hints": ["Hint 1", "Hint 2", "Hint 3"],
            "detailed_solution": "Solución con {a}",
            "distractor_ids": ["D1", "D2", "D3", "D4", "D5", "D6"],
            "generate_py": (
                "def generate(rng):\n"
                "    a = rng.randint(1, 10)\n"
                "    # Note: k_star is never declared in vars!\n"
                "    return {\n"
                "        'vars': {'a': a},\n"
                "        'correct': f'Respuesta {a}',\n"
                "        'distractors': [\n"
                "            {'value': f'Dist {i}_{a}', 'distractor_id': f'D{i+1}'}\n"
                "            for i in range(6)\n"
                "        ]\n"
                "    }\n"
            ),
        }

        declared_dids = {"D1", "D2", "D3", "D4", "D5", "D6"}
        errors = check_single_template(
            template=template_with_unreplaced_var,
            competency_id="C-TEST",
            declared_distractor_ids=declared_dids,
            num_dry_run_seeds=50,
        )

        # Invariant failure for {k_star} must appear as exactly ONE error instead of 50
        k_star_errors = [e for e in errors if "{k_star}" in e]
        assert len(k_star_errors) == 1, f"Expected 1 consolidated error for {k_star}, got {len(k_star_errors)}"

        err = k_star_errors[0]
        # Must contain aggregated seeds range
        assert "semillas 100..149 (50 semillas)" in err
        # Must retain full prescriptive guidance
        assert "[-] [R-20: SINTAXIS / LLAVES]" in err
        assert "UBICACIÓN:" in err
        assert "CAUSA:" in err
        assert "ACTION REQUIRED:" in err
        assert "ACCIONES CORRECTIVAS:" in err
        assert "NOTA PARA EL AGENTE:" in err

    def test_production_parity_giveaway_aggregated_across_questions(self):
        """When 20 questions share the same giveaway error (R-18), parity check consolidates them."""
        # Create 20 questions that violate R-18 (giveaway language in option)
        questions = []
        for i in range(1, 21):
            qid = f"Q-TEST-{i:03d}"
            questions.append({
                "id": qid,
                "template_id": "T-TEST-01",
                "type": "multiple_choice_7_options",
                "interaction_type": "multiple_choice_7_options",
                "stem": f"Pregunta número {i}.",
                "options": [
                    {"content": "Resultado correcto", "is_correct": True},
                    {"content": "Resultado alternativo asumiendo erróneamente que x=0", "is_correct": False, "error_rationale": "Confusión"},
                    {"content": "Resultado 2", "is_correct": False, "error_rationale": "R2"},
                    {"content": "Resultado 3", "is_correct": False, "error_rationale": "R3"},
                    {"content": "Resultado 4", "is_correct": False, "error_rationale": "R4"},
                    {"content": "Resultado 5", "is_correct": False, "error_rationale": "R5"},
                    {"content": "Resultado 6", "is_correct": False, "error_rationale": "R6"},
                ],
                "hints": ["Hint 1", "Hint 2", "Hint 3"],
                "solution": "Solución paso a paso",
                "difficulty": "medium",
                "competency_id": "C-TEST",
            })

        comp_obj = {
            "id": "C-TEST",
            "name": "Competencia de Prueba",
            "type": "concept",
            "description": "Descripción",
        }

        parity_errors = check_production_parity_for_competency(
            cid="C-TEST",
            competency=comp_obj,
            questions=questions,
            strict=False,
        )

        r18_errors = [e for e in parity_errors if "R-18" in e]
        # Should be consolidated into 1 error block instead of 20
        assert len(r18_errors) == 1, f"Expected 1 consolidated R-18 parity error, got {len(r18_errors)}"

        err = r18_errors[0]
        # Check that multiple reactivos are consolidated
        assert "(20 reactivos)" in err
        assert "Q-TEST-001" in err
        assert "Q-TEST-020" in err

    def test_ast_latex_corruption_grouped_with_lines(self):
        """Corrupted LaTeX escapes on multiple lines are grouped by command and list lines."""
        generate_py_code = (
            "def generate(rng):\n"
            "    f1 = '\\frac{a}{b}'\n"     # line 2: \frac
            "    b1 = '\\beta_0'\n"          # line 3: \beta
            "    f2 = '\\frac{c}{d}'\n"     # line 4: \frac
            "    f3 = '\\frac{e}{f}'\n"     # line 5: \frac
            "    return {'correct': 'ok'}\n"
        )

        structured = check_latex_escape_corruption_structured(generate_py_code)
        assert len(structured) == 4

        frac_items = [s for s in structured if s["cmd"] == r"\frac"]
        assert len(frac_items) == 3
        frac_lines = [s["line"] for s in frac_items]
        assert frac_lines == [2, 4, 5]

        # Verify check_single_template groups them
        template = {
            "id": "T-AST-GROUP",
            "interaction_type": "multiple_choice_7_options",
            "stem": "Determine el valor.",
            "hints": ["H1", "H2", "H3"],
            "detailed_solution": "Sol",
            "distractor_ids": ["D1", "D2", "D3", "D4", "D5", "D6"],
            "generate_py": generate_py_code,
        }

        errors = check_single_template(
            template=template,
            competency_id="C-TEST",
            declared_distractor_ids={"D1", "D2", "D3", "D4", "D5", "D6"},
            num_dry_run_seeds=5,
        )

        ast_errors = [e for e in errors if "AST: CORRUPCIÓN DE ESCAPE LATEX" in e]
        # 1 error for \frac, 1 error for \beta
        assert len(ast_errors) == 2
        frac_err = next(e for e in ast_errors if r"\frac" in e)
        assert "Líneas: 2, 4, 5 (3 ocurrencias)" in frac_err

    def test_dry_run_dynamic_distractor_collision_aggregated(self):
        """Dynamic distractor collision whose values change every seed is consolidated across all 50 seeds."""
        template = {
            "id": "T-D4-DYNAMIC-TEST",
            "interaction_type": "multiple_choice_7_options",
            "stem": "Resuelva x = {a}",
            "hints": ["Hint 1", "Hint 2", "Hint 3"],
            "detailed_solution": "Solución con {a}",
            "distractor_ids": ["D1", "D2", "D3", "D4", "D5", "D6"],
            "generate_py": (
                "def generate(rng):\n"
                "    a = rng.randint(1, 100)\n"
                "    return {\n"
                "        'vars': {'a': a},\n"
                "        'correct': str(a),\n"
                "        'distractors': [\n"
                "            {'value': str(a), 'distractor_id': 'D1'},\n"
                "            {'value': str(a+1), 'distractor_id': 'D2'},\n"
                "            {'value': str(a+2), 'distractor_id': 'D3'},\n"
                "            {'value': str(a+3), 'distractor_id': 'D4'},\n"
                "            {'value': str(a+4), 'distractor_id': 'D5'},\n"
                "            {'value': str(a+5), 'distractor_id': 'D6'},\n"
                "        ]\n"
                "    }\n"
            ),
        }

        errors = check_single_template(
            template=template,
            competency_id="C-TEST",
            declared_distractor_ids={"D1", "D2", "D3", "D4", "D5", "D6"},
            num_dry_run_seeds=50,
        )

        d4_errors = [e for e in errors if "DISTRACTOR IDÉNTICO A RESPUESTA CORRECTA" in e]
        # Exactly 1 consolidated diagnostic error block instead of 50-100
        assert len(d4_errors) == 1, f"Expected 1 consolidated D4 error, got: {len(d4_errors)}"
        assert "semillas 100..149 (50 semillas)" in d4_errors[0]

    def test_undeclared_distractor_ids_consolidated_in_single_diagnostic(self):
        """When multiple distractor IDs are not declared in CTA, a single consolidated error is emitted."""
        template = {
            "id": "T-UNDECLARED-DIDS",
            "interaction_type": "multiple_choice_7_options",
            "stem": "Calcule el valor de {a}",
            "hints": ["H1", "H2", "H3"],
            "detailed_solution": "Sol",
            "distractor_ids": ["D-UNKNOWN-1", "D-UNKNOWN-2", "D-UNKNOWN-3", "D-VALID-1", "D-VALID-2", "D-VALID-3"],
            "generate_py": (
                "def generate(rng):\n"
                "    return {'vars': {'a': 1}, 'correct': '1', 'distractors': [{'value': str(i), 'distractor_id': f'D{i}'} for i in range(6)]}\n"
            ),
        }

        errors = check_single_template(
            template=template,
            competency_id="C-TEST",
            declared_distractor_ids={"D-VALID-1", "D-VALID-2", "D-VALID-3"},
            num_dry_run_seeds=5,
        )

        tpl_d1_errors = [e for e in errors if "TPL-D1" in e]
        assert len(tpl_d1_errors) == 1
        assert "D-UNKNOWN-1" in tpl_d1_errors[0]
        assert "D-UNKNOWN-2" in tpl_d1_errors[0]
        assert "D-UNKNOWN-3" in tpl_d1_errors[0]
        assert "(3 distractores)" in tpl_d1_errors[0]

    def test_stem_variants_katex_syntax_errors_consolidated(self):
        """When multiple stem_variants have the same KaTeX syntax error, they are consolidated."""
        template = {
            "id": "T-VARIANTS-KATEX",
            "interaction_type": "multiple_choice_7_options",
            "stem": "Calcule $x + y$",
            "stem_variants": [
                "Variante 1 con delimitador sin cerrar $x + 1",
                "Variante 2 con delimitador sin cerrar $y + 2",
                "Variante 3 con delimitador sin cerrar $z + 3",
            ],
            "hints": ["H1", "H2", "H3"],
            "detailed_solution": "Sol",
            "distractor_ids": ["D1", "D2", "D3", "D4", "D5", "D6"],
            "generate_py": (
                "def generate(rng):\n"
                "    return {'vars': {'a': 1}, 'correct': '1', 'distractors': [{'value': str(i), 'distractor_id': f'D{i}'} for i in range(6)]}\n"
            ),
        }

        errors = check_single_template(
            template=template,
            competency_id="C-TEST",
            declared_distractor_ids={"D1", "D2", "D3", "D4", "D5", "D6"},
            num_dry_run_seeds=5,
        )

        unbalanced_errors = [e for e in errors if "matemática inline no balanceados" in e and "stem_variants" in e]
        assert len(unbalanced_errors) == 1
        assert "stem_variants[0], stem_variants[1], stem_variants[2]" in unbalanced_errors[0]


class TestCtaLineIndexingAndConsolidation:
    """Verifies JSON line indexing and error consolidation in check_cta."""

    def test_json_line_locator_indexes_ids_and_fields(self, tmp_path: Path):
        """JsonLineLocator accurately tracks 1-indexed line numbers for competency and distractor IDs."""
        json_content = (
            '{\n'                                   # 1
            '  "competencies": [\n'                 # 2
            '    {\n'                               # 3
            '      "id": "C-01",\n'                 # 4
            '      "name": "Concept 1",\n'          # 5
            '      "distractors": [\n'              # 6
            '        {\n'                           # 7
            '          "id": "D-C01-01",\n'         # 8
            '          "wrong_belief": null,\n'     # 9
            '          "omitted_step": null\n'      # 10
            '        },\n'                          # 11
            '        {\n'                           # 12
            '          "id": "D-C01-02",\n'         # 13
            '          "wrong_belief": null,\n'     # 14
            '          "omitted_step": null\n'      # 15
            '        }\n'                           # 16
            '      ]\n'                             # 17
            '    }\n'                               # 18
            '  ]\n'                                 # 19
            '}\n'                                   # 20
        )
        part_file = tmp_path / "part_01.json"
        part_file.write_text(json_content, encoding="utf-8")

        locator = JsonLineLocator(part_file)
        assert locator.get_line("C-01") == 4
        assert locator.get_line("D-C01-01") == 8
        assert locator.get_line("D-C01-02") == 13
        assert locator.get_line("D-C01-01", "wrong_belief") == 9

        index_dict = build_json_line_index(part_file)
        assert index_dict["C-01"] == 4
        assert index_dict["D-C01-01"] == 8

    def test_check_cta_part_aggregates_cta_d2_empty_fields_with_lines(self, tmp_path: Path):
        """Multiple distractors with both wrong_belief and omitted_step null are consolidated citing lines."""
        json_content = (
            '{\n'                                   # 1
            '  "competencies": [\n'                 # 2
            '    {\n'                               # 3
            '      "id": "C-01",\n'                 # 4
            '      "name": "Concepto de Prueba",\n' # 5
            '      "type": "concept",\n'            # 6
            '      "bloom_level": "Understand",\n'  # 7
            '      "distractors": [\n'              # 8
            '        {\n'                           # 9
            '          "id": "D-C01-01",\n'         # 10
            '          "name": "D1",\n'             # 11
            '          "wrong_belief": null,\n'     # 12
            '          "omitted_step": null,\n'     # 13
            '          "manifestation": "M1"\n'     # 14
            '        },\n'                          # 15
            '        {\n'                           # 16
            '          "id": "D-C01-02",\n'         # 17
            '          "name": "D2",\n'             # 18
            '          "wrong_belief": null,\n'     # 19
            '          "omitted_step": null,\n'     # 20
            '          "manifestation": "M2"\n'     # 21
            '        },\n'                          # 22
            '        {\n'                           # 23
            '          "id": "D-C01-03",\n'         # 24
            '          "name": "D3",\n'             # 25
            '          "wrong_belief": null,\n'     # 26
            '          "omitted_step": null,\n'     # 27
            '          "manifestation": "M3"\n'     # 28
            '        }\n'                           # 29
            '      ]\n'                             # 30
            '    }\n'                               # 31
            '  ]\n'                                 # 32
            '}\n'                                   # 33
        )
        part_file = tmp_path / "cta_part_01.json"
        part_file.write_text(json_content, encoding="utf-8")

        data = json.loads(json_content)
        is_valid, errors = check_cta_part(data, file_path=part_file)

        assert not is_valid
        d2_errors = [e for e in errors if "CTA-D2" in e]
        # Exactly 1 consolidated error block for the 3 distractors
        assert len(d2_errors) == 1, f"Expected 1 consolidated CTA-D2 error, got: {d2_errors}"

        d2_msg = d2_errors[0]
        assert "'D-C01-01' (línea 10)" in d2_msg
        assert "'D-C01-02' (línea 17)" in d2_msg
        assert "'D-C01-03' (línea 24)" in d2_msg
        assert "(3 distractores afectados)" in d2_msg

    def test_check_cta_part_aggregates_insufficient_distractors(self, tmp_path: Path):
        """Multiple competencies with insufficient distractors are consolidated into a single message."""
        json_content = (
            '{\n'
            '  "competencies": [\n'
            '    {"id": "C-01", "name": "C1", "type": "concept", "distractors": [{"id": "D1", "name": "D1", "wrong_belief": "W"}]},\n'
            '    {"id": "C-02", "name": "C2", "type": "concept", "distractors": [{"id": "D2", "name": "D2", "wrong_belief": "W"}]},\n'
            '    {"id": "C-03", "name": "C3", "type": "concept", "distractors": [{"id": "D3", "name": "D3", "wrong_belief": "W"}]}\n'
            '  ]\n'
            '}\n'
        )
        part_file = tmp_path / "part_short.json"
        part_file.write_text(json_content, encoding="utf-8")

        data = json.loads(json_content)
        is_valid, errors = check_cta_part(data, file_path=part_file)

        assert not is_valid
        d1_errors = [e for e in errors if "CTA-D1 violation: Competencias con cuota insuficiente" in e]
        assert len(d1_errors) == 1
        assert "C-01" in d1_errors[0]
        assert "C-02" in d1_errors[0]
        assert "C-03" in d1_errors[0]

    def test_json_line_locator_nested_and_reversed_keys(self, tmp_path: Path):
        """JsonLineLocator correctly resolves line numbers when fields appear before 'id' and within nested scopes."""
        json_content = (
            '{\n'                                   # 1
            '  "competencies": [\n'                 # 2
            '    {\n'                               # 3
            '      "name": "Concepto 1",\n'         # 4 (before id)
            '      "id": "C-01",\n'                 # 5
            '      "distractors": [\n'              # 6
            '        {\n'                           # 7
            '          "name": "D1",\n'             # 8 (before id)
            '          "wrong_belief": "Error 1",\n'# 9 (before id)
            '          "id": "D-01"\n'              # 10
            '        },\n'                          # 11
            '        {\n'                           # 12
            '          "id": "D-02",\n'             # 13
            '          "name": "D2"\n'              # 14 (after id)
            '        }\n'                           # 15
            '      ]\n'                             # 16
            '    }\n'                               # 17
            '  ]\n'                                 # 18
            '}\n'                                   # 19
        )
        part_file = tmp_path / "part_reversed.json"
        part_file.write_text(json_content, encoding="utf-8")

        locator = JsonLineLocator(part_file)
        assert locator.get_line("C-01") == 5
        assert locator.get_line("C-01", "name") == 4
        assert locator.get_line("D-01") == 10
        assert locator.get_line("D-01", "name") == 8
        assert locator.get_line("D-01", "wrong_belief") == 9
        assert locator.get_line("D-02") == 13
        assert locator.get_line("D-02", "name") == 14

    def test_json_line_locator_duplicate_ids_tracks_all_lines(self, tmp_path: Path):
        """JsonLineLocator tracks all line numbers where duplicate IDs appear."""
        json_content = (
            '{\n'
            '  "distractors": [\n'
            '    {"id": "D-DUP", "wrong_belief": "W1"},\n' # line 3
            '    {"id": "D-DUP", "wrong_belief": "W2"}\n'  # line 4
            '  ]\n'
            '}\n'
        )
        test_file = tmp_path / "part_dups.json"
        test_file.write_text(json_content, encoding="utf-8")

        locator = JsonLineLocator(test_file)
        lines = locator.get_lines("D-DUP")
        assert lines == [3, 4]

    def test_check_cta_part_aggregates_duplicate_distractor_ids_with_lines(self, tmp_path: Path):
        """Duplicate distractor IDs are consolidated into a single message citing line numbers."""
        json_content = (
            '{\n'
            '  "competencies": [\n'
            '    {\n'
            '      "id": "C-01", "name": "C1", "type": "concept",\n'
            '      "distractors": [\n'
            '        {"id": "D-DUP", "name": "D1", "wrong_belief": "W1"},\n' # line 5
            '        {"id": "D-DUP", "name": "D2", "wrong_belief": "W2"},\n' # line 6
            '        {"id": "D-03", "name": "D3", "wrong_belief": "W3"}\n'
            '      ]\n'
            '    }\n'
            '  ]\n'
            '}\n'
        )
        part_file = tmp_path / "part_dup_ids.json"
        part_file.write_text(json_content, encoding="utf-8")

        data = json.loads(json_content)
        is_valid, errors = check_cta_part(data, file_path=part_file)

        assert not is_valid
        dup_errors = [e for e in errors if "Duplicate distractor id" in e]
        assert len(dup_errors) == 1
        assert "D-DUP" in dup_errors[0]
        assert "(líneas 6, 7)" in dup_errors[0]

    def test_check_cta_part_aggregates_missing_distractor_ids(self, tmp_path: Path):
        """Multiple distractors missing 'id' are consolidated into a single message."""
        json_content = (
            '{\n'
            '  "competencies": [\n'
            '    {\n'
            '      "id": "C-01", "name": "C1", "type": "concept",\n'
            '      "distractors": [\n'
            '        {"name": "No ID 1", "wrong_belief": "W1"},\n'
            '        {"name": "No ID 2", "wrong_belief": "W2"},\n'
            '        {"id": "D-03", "name": "D3", "wrong_belief": "W3"}\n'
            '      ]\n'
            '    }\n'
            '  ]\n'
            '}\n'
        )
        part_file = tmp_path / "part_missing_ids.json"
        part_file.write_text(json_content, encoding="utf-8")

        data = json.loads(json_content)
        is_valid, errors = check_cta_part(data, file_path=part_file)

        assert not is_valid
        missing_id_errors = [e for e in errors if "distractor missing id" in e or "Distractor missing 'id'" in e]
        assert len(missing_id_errors) == 1
        assert "2 distractores en competencias: 'C-01'" in missing_id_errors[0]


class TestValidatorModelAndCliConsolidation:
    """Verifies ValidationError multi-line formatting and CLI consolidation."""

    def test_validation_error_formatted_with_multiple_lines(self):
        """ValidationError with lines outputs consolidated lines string."""
        err = ValidationError(
            rule_id="R-03",
            code="ERR_LATEX_CORRUPT",
            message="LaTeX corruption detected: '\\frac' has single backslash",
            lines=[12, 15, 18, 22, 30],
        )

        formatted = err.formatted()
        assert "líneas: 12, 15, 18, 22, 30 - 5 ocurrencias" in formatted
        assert "Rule R-03: [ERR_LATEX_CORRUPT]" in formatted

    def test_format_cli_output_consolidates_repeated_errors(self):
        """format_cli_output groups repeated errors sharing rule_id and canonical message."""
        raw_errors = [
            ValidationError(rule_id="R-03", code="ERR_LATEX_CORRUPT", message="LaTeX corruption detected at line 10", line=10),
            ValidationError(rule_id="R-03", code="ERR_LATEX_CORRUPT", message="LaTeX corruption detected at line 15", line=15),
            ValidationError(rule_id="R-03", code="ERR_LATEX_CORRUPT", message="LaTeX corruption detected at line 20", line=20),
            ValidationError(rule_id="R-02", code="ERR_LATEX_SYNTAX", message="Invalid escape sequence at line 5", line=5),
        ]

        result = ValidationResult(
            file_path="test_course.json",
            is_valid=False,
            errors=raw_errors,
        )

        cli_output = format_cli_output(result)

        # Output must report 4 detected errors in total count
        assert "FAILED: 4 errors detected." in cli_output
        # But R-03 must appear as 1 consolidated diagnostic line
        r03_lines = [line for line in cli_output.splitlines() if "Rule R-03" in line]
        assert len(r03_lines) == 1, f"Expected 1 consolidated R-03 line, got: {r03_lines}"
        assert "líneas: 10, 15, 20 - 3 ocurrencias" in r03_lines[0]

    def test_scan_lexical_with_consolidate_flag(self):
        """scan_lexical(consolidate=True) consolidates multiple occurrences of same escape error."""
        json_payload = (
            '{\n'
            '  "q1": "\\frac{1}{2}",\n'     # line 2: R-03 \frac
            '  "q2": "\\Delta x",\n'         # line 3: R-02 \Delta
            '  "q3": "\\frac{3}{4}",\n'     # line 4: R-03 \frac
            '  "q4": "\\frac{5}{6}"\n'      # line 5: R-03 \frac
            '}\n'
        )

        # Unconsolidated scan returns 4 individual errors
        unconsolidated = scan_lexical(json_payload, consolidate=False)
        assert len(unconsolidated) == 4

        # Consolidated scan groups the 3 \frac errors into 1
        consolidated = scan_lexical(json_payload, consolidate=True)
        assert len(consolidated) == 2

        frac_err = next(e for e in consolidated if e.rule_id == "R-03")
        assert frac_err.lines == [2, 4, 5]
        assert "líneas: 2, 4, 5 - 3 ocurrencias" in frac_err.formatted()
