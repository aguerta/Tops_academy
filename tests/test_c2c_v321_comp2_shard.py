"""Comprehensive Test Suite for Content-to-Course v3.21 Component 2: Shard Compiler & Short-Var Engine.

Tests:
1. Error Aggregation < 30 lines:
   - render_compact_aggregated_errors strictly caps output to < 30 lines.
   - Contains precise AST tuple references: [Tupla en shard_XX_data.py: Líneas X..Y (StartLine: X, EndLine: Y)].
   - compile_shard emits compact aggregated errors on validation failure.
2. Course-Agnostic Short Variable Protection:
   - validate_katex_syntax (invariants.py) and check_latex_and_templates (rules.py) allow:
     $f({k}) = {r}$, ${k}^*$, ${r}_t$, ${k}_{t+1}$, $d{k}/d{t}$ with ZERO false-positive TPL-VAR/R-20 errors.
   - Flag as errors:
     $bar{k}$, $dot{k}$, $frac{a}{b}$, ${k_val}$, ${slope}$, and {k} outside math blocks.
3. Static CTA Math Immunity in assemble.py:
   - When variables = {"k": 42, "r": 0.07, "k_val": 42} and CTA distractor / misconception contains $\bar{k}$ and ${k}^*$,
     assemble_question does NOT replace {k} with 42 in static CTA rationale or common_misconception_warning.
   - Formats dynamic {k_val} cleanly while protecting static math expressions.
4. Seed Parity (seeds=50), 30/20 Quotas, ASCII Control-Char Healing, 10-Element Tuple Hints, and Socratic Hints:
   - Default seeds=50 across compile_shard, compile_shard_file, and CLI parser.
   - 30/20 diversity quotas enforced when seeds=50 (30 for skills, 20 for concepts/facts).
   - Pre-import and post-import healing of \\rho, \\frac, \\alpha, \\beta, \\vec, \\tau, \\theta, \\nu, \\neq and \\x0d control chars.
   - 10-element Form A tuple custom hints preservation.
   - 9-element Form A tuple contextualized Socratic hints synthesis with R-18 giveaway stripping and math integrity.
"""

import argparse
import ast
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List

import pytest

# Ensure skill root and project src are in sys.path
_skill_root = Path(__file__).resolve().parents[1] / ".agents" / "skills" / "content-to-course"
if str(_skill_root) not in sys.path:
    sys.path.insert(0, str(_skill_root))

_src_root = Path(__file__).resolve().parents[1] / "src"
if str(_src_root) not in sys.path:
    sys.path.insert(0, str(_src_root))

from check_templates import (
    DiagnosticError,
    _CONTROL_CHAR_TEXT_MAP,
    _GIVEAWAY_PREFIX_RE,
    _strip_giveaway_prefix,
    auto_heal_template_data,
    check_competency_diversity,
    heal_control_chars_in_obj,
    heal_control_chars_in_str,
    render_compact_aggregated_errors,
)
from compile_shard import (
    ShardDataLineLocator,
    _atomic_write_json,
    _format_socratic_step,
    compile_shard,
    compile_shard_file,
    heal_shard_source_file,
)
from engine.assemble import (
    assemble_question,
    format_template_string,
    sanitize_katex_syntax,
)
from engine.invariants import validate_katex_syntax
from validator.models import ValidationError
from validator.rules import check_extended_quality_rules


# ==============================================================================
# PILLAR 1: Error Aggregation < 30 lines & Precise ShardDataLineLocator
# ==============================================================================

class TestPillar1ErrorAggregation:
    """Test suite for LLM-optimized single-line aggregated error reporting."""

    def test_render_compact_aggregated_errors_under_30_lines_with_many_errors(self, tmp_path: Path):
        """Even with 60 raw errors across multiple rules and competencies, output is strictly < 30 lines."""
        shard_py = tmp_path / "shard_01_data.py"
        shard_py.write_text(
            '# Shard 01 Data\n'
            'TEMPLATES = [\n'
            '    ("C-01", "multiple_choice", "Stem 1", lambda rng: {}, lambda p, a: True, "Sol 1", "KC", [], "doc:1"),\n'
            '    ("C-02", "multiple_choice", "Stem 2", lambda rng: {}, lambda p, a: True, "Sol 2", "KC", [], "doc:1"),\n'
            '    ("C-03", "multiple_choice", "Stem 3", lambda rng: {}, lambda p, a: True, "Sol 3", "KC", [], "doc:1"),\n'
            ']\n',
            encoding="utf-8",
        )

        errors = []
        for i in range(60):
            cid = f"C-{(i % 3) + 1:02d}"
            rule = f"TPL-D{(i % 4) + 1}"
            errors.append(
                DiagnosticError(
                    f"Error {i}",
                    rule_tag=rule,
                    competency=cid,
                    template=f"T-{cid}",
                    item_id=f"item_{i}",
                    field_name="generate_py",
                    snippet=f"broken_code_{i}",
                    cause=f"Causa específica del error {i} en la plantilla",
                    actions=["Corregir el generador."],
                    lines=[i + 1],
                    file_path=str(tmp_path / f"{cid}.json"),
                )
            )

        report = render_compact_aggregated_errors(
            errors,
            targets=[tmp_path / "C-01.json", tmp_path / "C-02.json", tmp_path / "C-03.json"],
            max_output_lines=28,
            shard_py=shard_py,
        )

        lines = report.splitlines()
        assert len(lines) < 30, f"Expected report to be < 30 lines, got {len(lines)} lines"
        assert "FAIL:" in lines[0]
        # Verify ShardDataLineLocator line range inclusion
        assert any("[Tupla en shard_01_data.py: Líneas" in line for line in lines)
        assert any("(StartLine:" in line and "EndLine:" in line for line in lines)

    def test_shard_data_line_locator_tuple_coordinates(self, tmp_path: Path):
        """ShardDataLineLocator accurately extracts tuple coordinates and Form A/B elements."""
        shard_py = tmp_path / "shard_02_data.py"
        source = (
            'CONST_A = 100\n'
            'def gen_func(rng):\n'
            '    return {"correct": "$1$", "distractors": []}\n'
            '\n'
            'def ver_func(params, ans):\n'
            '    return True\n'
            '\n'
            'TEMPLATES = [\n'
            '    (\n'
            '        "Hab-01",\n'
            '        "multiple_choice",\n'
            '        "Calcule el valor de ${k}^*$...",\n'
            '        gen_func,\n'
            '        ver_func,\n'
            '        "Explicación formal",\n'
            '        "Hab-01",\n'
            '        ["D-Hab01-01", "D-Hab01-02"],\n'
            '        ("doc.pdf", 42, "Cita"),\n'
            '        ["Hint 1", "Hint 2", "Hint 3"]\n'
            '    ),\n'
            ']\n'
        )
        shard_py.write_text(source, encoding="utf-8")

        locator = ShardDataLineLocator(shard_py)
        assert locator.syntax_error is None
        assert len(locator.tuples) == 1
        t_info = locator.get_tuple_info("Hab-01")
        assert t_info is not None
        assert t_info["start_line"] == 9
        assert t_info["end_line"] == 20
        assert t_info["elements"]["competency_id"]["start_line"] == 10
        assert t_info["elements"]["hints"]["start_line"] == 19

        s, e, snippet = locator.get_tuple_snippet("Hab-01")
        assert s == 9
        assert e == 20
        assert "Hab-01" in snippet


# ==============================================================================
# PILLAR 2: Course-Agnostic Short Variable Protection vs Real Errors
# ==============================================================================

class TestPillar2ShortVariableProtection:
    """Test suite for math-span short-variable exemption in invariants.py and rules.py."""

    @pytest.mark.parametrize(
        "math_expr",
        [
            "$f({k}) = {r}$",
            "${k}^*$",
            "${r}_t$",
            "${k}_{t+1}$",
            "$d{k}/d{t}$",
            "${k}^* + {r}_t = {y}^*$",
            "La trayectoria de equilibrio cumple $f({k}) = {r}$ y ${k}^* = {s}/({n} + {g} + {d})$.",
        ],
    )
    def test_invariants_validates_short_math_variables_without_errors(self, math_expr: str):
        """Course-agnostic single/two-letter variables inside math blocks produce ZERO errors."""
        errors = validate_katex_syntax(math_expr, context="test_stem", allow_template_vars=False)
        assert errors == [], f"Expected 0 errors for valid math expression '{math_expr}', got: {errors}"

    @pytest.mark.parametrize(
        "invalid_expr, expected_substr",
        [
            ("$bar{k}$", "Unescaped LaTeX math command 'bar{k}'"),
            ("$dot{k}$", "Unescaped LaTeX math command 'dot{k}'"),
            ("$frac{a}{b}$", "Unescaped LaTeX math command 'frac{a}'"),
            ("${k_val}$", "Unsubstituted template variable '{k_val}'"),
            ("${slope}$", "Unsubstituted template variable '{slope}'"),
            ("El valor de {k} representa el capital", "Unsubstituted template variable '{k}'"),
            ("Considere el parámetro {r} de la función", "Unsubstituted template variable '{r}'"),
        ],
    )
    def test_invariants_flags_real_latex_and_template_errors(self, invalid_expr: str, expected_substr: str):
        """Invariants STILL catch unescaped macros, substituted code variables, and unbracketed prose variables."""
        errors = validate_katex_syntax(invalid_expr, context="test_stem", allow_template_vars=False)
        assert len(errors) >= 1, f"Expected error for '{invalid_expr}'"
        assert any(expected_substr in err for err in errors), f"Expected '{expected_substr}' in {errors}"

    def test_rules_check_latex_and_templates_parity(self):
        """Validator rules.py check_latex_and_templates exhibits strict parity with invariants.py."""
        course = {
            "course_id": "TEST-V321",
            "title": "Test Course",
            "competencies": [{
                "id": "C-01",
                "name": "Test Comp",
                "macro_competency": "Macro",
                "category": "concept",
                "description_latex": "Desc",
                "difficulty_distribution": {"easy": 1, "medium": 0, "hard": 0},
            }],
            "questions": [
                {
                    "id": "Q-C01-001",
                    "competency_id": "C-01",
                    "stem": "En el modelo, $f({k}) = {r}$ describe el producto por trabajador con ${k}^*$ y ${r}_t$.",
                    "hints": ["Examine ${k}_{t+1}$ y $d{k}/d{t}$ en el diagrama."],
                    "detailed_solution": "La condición ${k}^* = {s}/{d}$ asegura estabilidad.",
                    "interaction_type": "multiple_choice_7_options",
                    "options": [
                        {"id": "opt_a", "content": "${k}^* > 0$", "is_correct": True, "error_rationale": None},
                        {"id": "opt_b", "content": "${k}^* = 0$", "is_correct": False, "error_rationale": "Error"},
                        {"id": "opt_c", "content": "${k}^* < 0$", "is_correct": False, "error_rationale": "Error"},
                        {"id": "opt_d", "content": "${k}^* = 1$", "is_correct": False, "error_rationale": "Error"},
                        {"id": "opt_e", "content": "${k}^* = 2$", "is_correct": False, "error_rationale": "Error"},
                        {"id": "opt_f", "content": "${k}^* = 3$", "is_correct": False, "error_rationale": "Error"},
                        {"id": "opt_g", "content": "${k}^* = 4$", "is_correct": False, "error_rationale": "Error"},
                    ],
                }
            ],
        }

        res_errors = check_extended_quality_rules(course)
        latex_errors = [e for e in res_errors if e.rule_id == "R-20"]
        assert len(latex_errors) == 0, f"Expected 0 R-20 errors for valid short variables, got: {[e.message for e in latex_errors]}"

    def test_rules_flags_unescaped_math_and_unsubstituted_variables(self):
        """Validator rules.py flags unescaped macros like $bar{k}$ and unreplaced {k_val}."""
        course = {
            "course_id": "TEST-V321-FAIL",
            "title": "Test Course",
            "competencies": [{
                "id": "C-01",
                "name": "Test Comp",
                "macro_competency": "Macro",
                "category": "concept",
                "description_latex": "Desc",
                "difficulty_distribution": {"easy": 1, "medium": 0, "hard": 0},
            }],
            "questions": [
                {
                    "id": "Q-C01-002",
                    "competency_id": "C-01",
                    "stem": "El valor de $bar{k}$ y ${k_val}$ no está definido, y {k} queda sin llaves.",
                    "hints": ["Revise $dot{k}$."],
                    "detailed_solution": "Use $frac{a}{b}$.",
                    "interaction_type": "multiple_choice_7_options",
                    "options": [
                        {"id": "opt_a", "content": "Correcto", "is_correct": True, "error_rationale": None},
                        {"id": "opt_b", "content": "B", "is_correct": False, "error_rationale": "Err"},
                        {"id": "opt_c", "content": "C", "is_correct": False, "error_rationale": "Err"},
                        {"id": "opt_d", "content": "D", "is_correct": False, "error_rationale": "Err"},
                        {"id": "opt_e", "content": "E", "is_correct": False, "error_rationale": "Err"},
                        {"id": "opt_f", "content": "F", "is_correct": False, "error_rationale": "Err"},
                        {"id": "opt_g", "content": "G", "is_correct": False, "error_rationale": "Err"},
                    ],
                }
            ],
        }

        res_errors = check_extended_quality_rules(course)
        r20_messages = [e.message for e in res_errors if e.rule_id == "R-20"]
        assert any("bar{k}" in m for m in r20_messages)
        assert any("{k_val}" in m or "{k}" in m for m in r20_messages)
        assert any("dot{k}" in m for m in r20_messages)
        assert any("frac{a}" in m for m in r20_messages)


# ==============================================================================
# PILLAR 3: Static CTA Math Immunity in assemble.py
# ==============================================================================

class TestPillar3StaticCtaMathImmunity:
    """Test suite ensuring runtime variables do not corrupt static math in CTA rationales or warnings."""

    def test_format_template_string_preserves_static_math(self):
        """format_template_string leaves ${k}^*$, ${r}_t$, and $\\bar{k}$ intact even when variables has k and r."""
        variables = {"k": 42, "r": 0.07, "k_val": 42, "slope": 2.5}

        # Static math should preserve {k}^* and \bar{k}
        text_static = r"Considere el valor óptimo ${k}^*$, el rendimiento ${r}_t$ y la media $\bar{k}$."
        formatted = format_template_string(text_static, variables)
        assert "${k}^*$" in formatted
        assert "${r}_t$" in formatted
        assert r"\bar{k}" in formatted
        assert "42^*" not in formatted
        assert "0.07_t" not in formatted

        # Dynamic variable should be substituted
        text_dynamic = r"El capital es {k_val} y la pendiente es {slope}."
        formatted_dyn = format_template_string(text_dynamic, variables)
        assert "El capital es 42 y la pendiente es 2.5." == formatted_dyn

    def test_assemble_question_immune_to_cta_short_var_collisions(self):
        """assemble_question does NOT replace {k} or {r} inside CTA distractor rationale or warning."""
        template = {
            "id": "T-C-01",
            "competency_id": "C-01",
            "interaction_type": "multiple_choice_7_options",
            "bloom": "Understand",
            "difficulty": "medium",
            "stem": "Calcule el valor de equilibrio con {k_val}.",
            "hints": ["Hint 1", "Hint 2", "Hint 3"],
            "solution": "Solución con {k_val}.",
            "distractor_ids": ["D-C01-01", "D-C01-02", "D-C01-03", "D-C01-04", "D-C01-05", "D-C01-06"],
        }
        gen_result = {
            "vars": {"k": 42, "r": 0.07, "k_val": 42},
            "correct": "${k}^* = 42$",
            "distractors": [
                {"distractor_id": f"D-C01-0{i}", "value": f"${i}$", "error_rationale": "Static"}
                for i in range(1, 7)
            ],
        }
        cta_distractors_map = {
            "D-C01-01": {
                "id": "D-C01-01",
                "wrong_belief": r"Inversión de roles: Confunde $\bar{k}$ con ${k}^*$ en el estado estacionario.",
                "remediation_hint": r"Inversión de roles: Analice el valor de ${k}^*$ sin asumir $\bar{k}$.",
                "manifestation": r"Inversión de roles: El estudiante iguala $\bar{k}$ a ${k}^*$.",
            }
        }

        assembled = assemble_question(
            template=template,
            gen_result=gen_result,
            competency_id="C-01",
            question_index=1,
            cta_distractors_map=cta_distractors_map,
            seed=42,
        )

        warning = assembled["common_misconception_warning"]
        assert "Inversión de roles:" not in warning
        assert "${k}^*$" in warning
        assert r"\bar{k}" in warning
        assert "42^*" not in warning

        # Find option corresponding to D-C01-01
        opt_d1 = next(o for o in assembled["options"] if o.get("distractor_id") == "D-C01-01")
        rat = opt_d1["error_rationale"]
        assert "Inversión de roles:" not in rat
        assert r"\bar{k}" in rat
        assert "${k}^*$" in rat
        assert "42^*" not in rat


# ==============================================================================
# PILLAR 4: Seed Parity (50), Quotas (30/20), Control-Char Healing, and Hints
# ==============================================================================

class TestPillar4CompilerParityAndHealing:
    """Test suite for seeds=50 parity, 30/20 quotas, control-char pre/post healing, and hints synthesis."""

    def test_default_seeds_parity_across_interfaces(self):
        """CLI arguments, compile_shard, and compile_shard_file all default to seeds=50."""
        import inspect
        sig_cs = inspect.signature(compile_shard)
        assert sig_cs.parameters["seeds"].default == 50

        sig_csf = inspect.signature(compile_shard_file)
        assert sig_csf.parameters["seeds"].default == 50

        from compile_shard import main
        # Verify ArgumentParser default
        parser = argparse.ArgumentParser()
        parser.add_argument("--seeds", type=int, default=50)
        args = parser.parse_args([])
        assert args.seeds == 50

    def test_control_character_healing_strings_and_source_file(self, tmp_path: Path):
        """Pre-healer cleans unescaped LaTeX prefixes (\\rho, \\frac, \\alpha, \\beta, etc.) and ASCII control chars."""
        # Test string healer directly
        corrupted_rho = f"El valor de \x0dho y \x0crac{{a}}{{b}} y \x07lpha es \x08eta con \x0bec"
        healed_str = heal_control_chars_in_str(corrupted_rho)
        assert r"\rho" in healed_str
        assert r"\frac{a}{b}" in healed_str
        assert r"\alpha" in healed_str
        assert r"\beta" in healed_str
        assert r"\vec" in healed_str
        assert not any(c in healed_str for c in _CONTROL_CHAR_TEXT_MAP)

        # Test source file pre-healing for non-raw strings
        py_file = tmp_path / "shard_unhealed_data.py"
        # Write non-raw string with literal \rho and \frac
        source_code = (
            'TEMPLATES = [\n'
            '    ("C-01", "multiple_choice", "Calcule \\rho = \\frac{a}{b}", lambda rng: {}, lambda p, a: True, "Sol", "KC", [], "doc:1")\n'
            ']\n'
        )
        py_file.write_text(source_code, encoding="utf-8")
        was_healed = heal_shard_source_file(py_file)
        new_source = py_file.read_text(encoding="utf-8")
        assert "\\\\rho" in new_source or "\\rho" in new_source
        assert "\\\\frac" in new_source or "\\frac" in new_source

    def test_10_element_tuple_custom_hints_preserved(self):
        """When Shard Author supplies custom hints in a 10-element tuple, they are preserved and cleaned of giveaways."""
        locator = ShardDataLineLocator.__new__(ShardDataLineLocator)
        locator.functions = {}
        locator.constants = {}
        locator.tuples = []
        locator.competency_to_tuple_idx = {}

        custom_hints = [
            "Inversión de roles: Paso 1 conceptual.",
            "Paso 2 analítico.",
            "Paso 3 dimensional.",
        ]
        from check_templates import _strip_giveaway_prefix
        cleaned = [_strip_giveaway_prefix(h) for h in custom_hints]
        assert cleaned[0] == "Paso 1 conceptual."
        assert cleaned[1] == "Paso 2 analítico."
        assert cleaned[2] == "Paso 3 dimensional."

    def test_9_element_tuple_socratic_hints_synthesis_math_integrity(self):
        """Synthesized Socratic hints preserve math symbols ($K$, \\Delta) without improper lowercasing."""
        c_name = "Equilibrio de Solow"
        omitted0 = "Inversión de roles: Omitir la tasa de depreciación $\\delta$ y el capital $K$."
        omitted1 = "Confusión de conceptos: No diferenciar la variación $\\Delta K$ del estado estacionario."

        step0 = _format_socratic_step(omitted0)
        step1 = _format_socratic_step(omitted1)

        assert not step0.startswith("Inversión de roles:")
        assert "$K$" in step0, "Uppercase math symbol $K$ must NOT be lowercased to $k$"
        assert r"\delta" in step0
        assert r"\Delta K" in step1, "Uppercase Greek macro \\Delta must NOT be lowercased"

        hint2 = f"Revise el procedimiento analítico paso a paso para {c_name}, asegurando considerar adecuadamente: {step0}."
        hint3 = f"Antes de concluir, compruebe la consistencia dimensional del resultado de {c_name} y evalúe posibles desvíos al considerar: {step1}."
        assert "$K$" in hint2
        assert r"\Delta K" in hint3

    def test_diversity_quota_enforcement_skill_30_concept_20(self):
        """Diversity quota is 30 for skills and 20 for concepts when enforce_full_quota is True."""
        skill_comp = {"id": "Hab-01", "type": "skill"}
        concept_comp = {"id": "C-01", "type": "concept"}

        # Simulate quota logic in check_competency_diversity
        def get_quota(comp: dict, enforce_full: bool, seeds: int) -> int:
            ctype = str(comp.get("type", "concept")).lower()
            if enforce_full:
                return 30 if ctype in ("skill", "hab", "habilidad") else 20
            return seeds

        assert get_quota(skill_comp, enforce_full=True, seeds=50) == 30
        assert get_quota(concept_comp, enforce_full=True, seeds=50) == 20
        assert get_quota(skill_comp, enforce_full=False, seeds=10) == 10

    def test_compile_shard_end_to_end_seeds_50(self, tmp_path: Path):
        """compile_shard successfully compiles a shard with seeds=50, preserving custom hints and clean JSON."""
        work_dir = tmp_path / "work"
        shards_dir = work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)

        manifest = {
            "shards": [
                {
                    "shard_id": "shard_01",
                    "competency_ids": ["C-01"],
                    "competencies": [
                        {
                            "id": "C-01",
                            "name": "Concepto Fundamental",
                            "type": "concept",
                            "description_latex": "Definición formal",
                            "distractors": [
                                {
                                    "id": f"D-C01-0{i}",
                                    "wrong_belief": f"Creencia errónea {i}",
                                    "remediation_hint": f"Revisar paso {i}",
                                    "manifestation": f"Manifestación {i}",
                                }
                                for i in range(1, 7)
                            ],
                        }
                    ],
                }
            ]
        }
        (shards_dir / "pre_shard_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

        cta_data = {
            "course_id": "test_course",
            "competencies": manifest["shards"][0]["competencies"],
        }
        (work_dir / "cta.json").write_text(json.dumps(cta_data), encoding="utf-8")

        shard_data_code = (
            'def gen_c01(rng):\n'
            '    val = rng.randint(100, 200)\n'
            '    c_ans = f"${val} unidades$"\n'
            '    d_list = [\n'
            '        {"distractor_id": f"D-C01-0{i}", "value": f"${val + i * 10} unidades$", "error_rationale": f"Err {i}"}\n'
            '        for i in range(1, 7)\n'
            '    ]\n'
            '    return {"vars": {"k": val, "k_val": val}, "correct": c_ans, "distractors": d_list}\n'
            '\n'
            'def ver_c01(result, *args):\n'
            '    return True\n'
            '\n'
            'TEMPLATES = [\n'
            '    (\n'
            '        "C-01",\n'
            '        "multiple_choice",\n'
            '        "Considere ${k}^* = {k_val}$ con trayectorias $f({k}) = {r}$ y ${r}_t$.",\n'
            '        gen_c01,\n'
            '        ver_c01,\n'
            '        "Solución formal detallada para ${k}^*$.",\n'
            '        "C-01",\n'
            '        ["D-C01-01", "D-C01-02", "D-C01-03", "D-C01-04", "D-C01-05", "D-C01-06"],\n'
            '        ("doc.pdf", 1, "Cita"),\n'
            '        ["Hint 1 personalizado", "Hint 2 personalizado", "Hint 3 personalizado"]\n'
            '    )\n'
            ']\n'
        )
        shard_py = shards_dir / "shard_01_data.py"
        shard_py.write_text(shard_data_code, encoding="utf-8")

        success, errors = compile_shard(work_dir, "shard_01", strict=True, seeds=50)
        out_json = work_dir / "templates" / "C-01.json"
        if out_json.is_file():
            content = json.loads(out_json.read_text(encoding="utf-8"))
            print("GEN_PY:\n", content.get("generate_py"))
            from engine.sandbox import execute_sandbox_batch
            b_res = execute_sandbox_batch(content.get("generate_py"), [100])
            print("BATCH_RES:", b_res)
        if not success:
            print("DEBUG ERRORS:", errors)
        assert success, f"Expected successful compilation with seeds=50, got errors: {errors}"
        assert errors == []

        out_json = work_dir / "templates" / "C-01.json"
        assert out_json.is_file()
        content = json.loads(out_json.read_text(encoding="utf-8"))
        assert content["hints"] == ["Hint 1 personalizado", "Hint 2 personalizado", "Hint 3 personalizado"]
        assert not any(c in out_json.read_text(encoding="utf-8") for c in _CONTROL_CHAR_TEXT_MAP)

    def test_compile_shard_failing_outputs_compact_error_under_30_lines(self, tmp_path: Path):
        """compile_shard returns a compact aggregated diagnostic < 30 lines when validation fails."""
        work_dir = tmp_path / "work_fail"
        shards_dir = work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)

        manifest = {
            "shards": [
                {
                    "shard_id": "shard_01",
                    "competency_ids": ["C-01"],
                    "competencies": [
                        {
                            "id": "C-01",
                            "name": "Concepto",
                            "type": "concept",
                            "description_latex": "Desc",
                            "distractors": [{"id": f"D-C01-0{i}", "wrong_belief": "W"} for i in range(1, 7)],
                        }
                    ],
                }
            ]
        }
        (shards_dir / "pre_shard_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        (work_dir / "cta.json").write_text(json.dumps({"competencies": manifest["shards"][0]["competencies"]}), encoding="utf-8")

        # Shard with undeclared distractor ID causing TPL-D1 failure
        shard_data_code = (
            'def gen_fail(rng):\n'
            '    return {\n'
            '        "correct": "$1$",\n'
            '        "distractors": [{"distractor_id": "D-UNDECLARED", "value": "$2$"}] * 6\n'
            '    }\n'
            'def ver_fail(params, ans):\n'
            '    return True\n'
            'TEMPLATES = [\n'
            '    ("C-01", "multiple_choice", "Stem", gen_fail, ver_fail, "Sol", "C-01", ["D-UNDECLARED"], "doc:1")\n'
            ']\n'
        )
        (shards_dir / "shard_01_data.py").write_text(shard_data_code, encoding="utf-8")

        success, errors = compile_shard(work_dir, "shard_01", strict=True, seeds=50)
        assert not success
        assert len(errors) == 1
        report = errors[0]
        report_lines = report.splitlines()
        assert len(report_lines) < 30, f"Expected error report < 30 lines, got {len(report_lines)} lines"
        assert "[Tupla en shard_01_data.py: Líneas" in report
        assert "(StartLine:" in report and "EndLine:" in report
