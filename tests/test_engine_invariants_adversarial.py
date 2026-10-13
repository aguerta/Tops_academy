"""Adversarial Empirical Stress Testing Suite for Content-to-Course v2 Engine & Invariants.

Performs adversarial challenge testing across 5 critical dimensions:
1. Duplicate Rejection (instantiate.py): Static parameters, static stems with dynamic vars,
   whitespace variations, and finite parameter state exhaustion.
2. Invariant Checks (invariants.py & check_templates.py): Multiple correct answers, zero correct,
   identical distractors, distractor matching correct, hint bounds, stem bounds, answer leaks,
   FIB/MS structural invariants.
3. Diversity Metric (diversity.py): Masked stem extraction, low diversity failure, high diversity pass,
   strict >= 0.5 threshold boundary verification.
4. Anti-Giveaway Balance (assemble.py): A-G uniform placement distribution (Chi-squared test over 1400 runs),
   item length anti-giveaway bounds [0.8*min, 1.2*max], and course-wide distribution checks.
5. Quota Scaling (instantiate.py): Skill >= 30, Fact/Concept >= 20, interaction type coverage across MC7, FIB, MS.
"""
from __future__ import annotations

import math
import random
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

import pytest

# Ensure skill and repo roots are on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / ".agents" / "skills" / "content-to-course"

for p in [str(SKILL_DIR), str(REPO_ROOT)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from check_templates import check_single_template
from engine.assemble import (
    OPTION_LETTERS,
    assemble_question,
    check_course_giveaway_distribution,
    format_template_string,
    sanitize_katex_syntax,
)
from engine.diversity import evaluate_competency_diversity, mask_stem_numbers
from engine.instantiate import (
    allocate_template_quotas,
    get_competency_quota,
    instantiate_competency,
    instantiate_template,
)
from engine.invariants import check_instance_invariants, validate_katex_syntax


# =============================================================================
# 1. DUPLICATE REJECTION ADVERSARIAL TESTS
# =============================================================================
class TestDuplicateRejectionAdversarial:
    """Stress tests deduplication logic for parameter tuples and rendered stems in instantiate.py."""

    def test_duplicate_parameters_rejected_static_vars(self):
        """Templates that output static variables across all seeds must be rejected on duplicate attempts."""
        static_template = {
            "id": "TPL-STATIC-VARS",
            "interaction_type": "multiple_choice_7_options",
            "stem": "Determine the value of variable $x = {x}$ and $y = {y}$.",
            "hints": [
                "Consider the given parameter values.",
                "Review the relationship between x and y.",
                "Combine the values to find the result.",
            ],
            "detailed_solution": "The values are x={x} and y={y}.",
            "distractor_ids": ["D1", "D2", "D3", "D4", "D5", "D6"],
            "generate_py": (
                "def generate(rng):\n"
                "    return {\n"
                "        'vars': {'x': 10, 'y': 20},\n"
                "        'correct': 'Valor exacto 30',\n"
                "        'distractors': [\n"
                "            {'value': f'Valor exacto {v}', 'distractor_id': f'D{i+1}'}\n"
                "            for i, v in enumerate([31, 32, 33, 34, 35, 36])\n"
                "        ]\n"
                "    }\n"
            ),
        }

        # 1 instance can succeed
        q1 = instantiate_template(
            template=static_template,
            competency_id="Hab-01",
            target_count=1,
            max_attempts=20,
        )
        assert len(q1) == 1

        # Asking for 2 instances MUST fail because seeds 2..N generate duplicate param tuple ('x', '10'), ('y', '20')
        with pytest.raises(ValueError) as excinfo:
            instantiate_template(
                template=static_template,
                competency_id="Hab-01",
                target_count=2,
                max_attempts=30,
            )
        assert "could only generate 1/2 unique invariant instances" in str(excinfo.value)

    def test_duplicate_stems_rejected_despite_dynamic_vars(self):
        """When parameters change but the rendered stem remains identical, duplicate stems must be rejected."""
        dynamic_params_static_stem_template = {
            "id": "TPL-STATIC-STEM",
            "interaction_type": "multiple_choice_7_options",
            # Stem deliberately does NOT use {k}, so rendered stem is 100% constant
            "stem": "Determine which of the following is the standard ordinary differential equation.",
            "hints": [
                "Recall the definition of ordinary differential equations.",
                "Check the number of independent variables involved.",
                "Verify whether partial derivatives are present.",
            ],
            "detailed_solution": "An ordinary differential equation contains only one independent variable.",
            "distractor_ids": ["D1", "D2", "D3", "D4", "D5", "D6"],
            "generate_py": (
                "def generate(rng):\n"
                "    k = rng.randint(1, 100000)\n"
                "    return {\n"
                "        'vars': {'k': k},\n"
                "        'correct': 'Opcion correcta valida 24',\n"  # len 25
                "        'distractors': [\n"
                "            {'value': f'Opcion distractor nro {i+1}', 'distractor_id': f'D{i+1}'}\n"  # len 24
                "            for i in range(6)\n"
                "        ]\n"
                "    }\n"
            ),
        }

        # Requesting 2 instances must fail because the rendered stem collides on attempt 2
        with pytest.raises(ValueError) as excinfo:
            instantiate_template(
                template=dynamic_params_static_stem_template,
                competency_id="Hab-01",
                target_count=2,
                max_attempts=30,
            )
        assert "could only generate 1/2 unique invariant instances" in str(excinfo.value)

    def test_whitespace_normalization_duplicate_rejection(self):
        """Stems that differ only by spacing/whitespace must be normalized and rejected as duplicates."""
        whitespace_template = {
            "id": "TPL-WHITESPACE-STEM",
            "interaction_type": "multiple_choice_7_options",
            "stem": "Compute the derivative {sp}of the function.",
            "hints": [
                "Examine the functional form.",
                "Apply the chain rule.",
                "Simplify the expression.",
            ],
            "detailed_solution": "The derivative is computed directly.",
            "distractor_ids": ["D1", "D2", "D3", "D4", "D5", "D6"],
            "generate_py": (
                "def generate(rng):\n"
                "    sp = ' ' * rng.randint(1, 5)\n"
                "    return {\n"
                "        'vars': {'sp': sp},\n"
                "        'correct': 'Solucion valida base',\n"
                "        'distractors': [\n"
                "            {'value': f'Distractor opcion {i+1}', 'distractor_id': f'D{i+1}'}\n"
                "            for i in range(6)\n"
                "        ]\n"
                "    }\n"
            ),
        }

        # Whitespace normalization re.sub(r'\s+', ' ', ...) will reduce all stems to 'Compute the derivative of the function.'
        with pytest.raises(ValueError) as excinfo:
            instantiate_template(
                template=whitespace_template,
                competency_id="Hab-01",
                target_count=2,
                max_attempts=25,
            )
        assert "could only generate 1/2 unique invariant instances" in str(excinfo.value)

    def test_finite_parameter_space_exhaustion_raises_error(self):
        """A template with only 3 possible parameter tuples cannot fulfill a quota of 5."""
        finite_template = {
            "id": "TPL-FINITE-SPACE",
            "interaction_type": "multiple_choice_7_options",
            "stem": "Determine the state for mode {mode}.",
            "hints": [
                "Check the current operational state.",
                "Consult the lookup table for the mode.",
                "Conclude the matching parameter.",
            ],
            "detailed_solution": "The state is derived from mode {mode}.",
            "distractor_ids": ["D1", "D2", "D3", "D4", "D5", "D6"],
            "generate_py": (
                "def generate(rng):\n"
                "    m = rng.randint(1, 3)\n"  # Only 1, 2, or 3
                "    return {\n"
                "        'vars': {'mode': m},\n"
                "        'correct': f'Estado regularizado {m}',\n"
                "        'distractors': [\n"
                "            {'value': f'Estado alternativo {m}_{i}', 'distractor_id': f'D{i+1}'}\n"
                "            for i in range(6)\n"
                "        ]\n"
                "    }\n"
            ),
        }

        with pytest.raises(ValueError) as excinfo:
            instantiate_template(
                template=finite_template,
                competency_id="Hab-01",
                target_count=5,
                max_attempts=50,
            )
        # Should generate at most 3
        assert "could only generate" in str(excinfo.value)
        assert "/5 unique invariant instances" in str(excinfo.value)

    def test_high_entropy_parameters_succeed(self):
        """A well-parameterized template smoothly generates all requested unique instances."""
        healthy_template = {
            "id": "TPL-HEALTHY",
            "interaction_type": "multiple_choice_7_options",
            "stem": "Calculate ${a}x + {b} = 0$.",
            "hints": [
                "Subtract the constant term {b} from both sides.",
                "Divide both sides by the coefficient {a}.",
                "State the solution x = -{b}/{a}.",
            ],
            "detailed_solution": "Solving yields x = -{b}/{a}.",
            "distractor_ids": ["D1", "D2", "D3", "D4", "D5", "D6"],
            "generate_py": (
                "def generate(rng):\n"
                "    a = rng.randint(2, 50)\n"
                "    b = rng.randint(51, 100)\n"
                "    return {\n"
                "        'vars': {'a': a, 'b': b},\n"
                "        'correct': f'x = -{b}/{a}',\n"
                "        'distractors': [\n"
                "            {'value': f'x = -{b+i}/{a}', 'distractor_id': f'D{i+1}'}\n"
                "            for i in range(1, 7)\n"
                "        ]\n"
                "    }\n"
            ),
        }

        res = instantiate_template(
            template=healthy_template,
            competency_id="Hab-01",
            target_count=5,
            max_attempts=50,
        )
        assert len(res) == 5
        # Verify all stems and ids are distinct
        stems = [q["stem"] for q in res]
        assert len(set(stems)) == 5


# =============================================================================
# 2. INVARIANT CHECKS ADVERSARIAL TESTS
# =============================================================================
class TestInvariantChecksAdversarial:
    """Stress tests psychometric and structural invariant enforcement in invariants.py."""

    def _build_valid_mc7(self) -> Dict[str, Any]:
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

    def test_mc7_multiple_correct_answers_rejected(self):
        """MC7 with 2 correct answers must be caught and rejected."""
        q = self._build_valid_mc7()
        q["options"][1]["is_correct"] = True  # Now 2 correct options
        is_valid, errors = check_instance_invariants(q, "multiple_choice_7_options")
        assert not is_valid
        assert any("MC7 must have exactly 1 correct option (found 2)" in e for e in errors)

    def test_mc7_zero_correct_answers_rejected(self):
        """MC7 with zero correct answers must be rejected."""
        q = self._build_valid_mc7()
        q["options"][0]["is_correct"] = False  # Now 0 correct options
        is_valid, errors = check_instance_invariants(q, "multiple_choice_7_options")
        assert not is_valid
        assert any("MC7 must have exactly 1 correct option (found 0)" in e for e in errors)

    def test_mc7_identical_distractors_rejected(self):
        """MC7 with two duplicate distractors must be rejected."""
        q = self._build_valid_mc7()
        q["options"][2]["content"] = q["options"][1]["content"]  # Duplicate content
        is_valid, errors = check_instance_invariants(q, "multiple_choice_7_options")
        assert not is_valid
        assert any("Duplicate option content detected" in e for e in errors)

    def test_mc7_distractor_matches_correct_rejected(self):
        """MC7 where an incorrect option matches the correct option text must be rejected."""
        q = self._build_valid_mc7()
        q["options"][3]["content"] = q["options"][0]["content"]  # Matches correct option
        is_valid, errors = check_instance_invariants(q, "multiple_choice_7_options")
        assert not is_valid
        assert any("Distractor identical to correct answer" in e or "Duplicate option content detected" in e for e in errors)

    def test_mc7_cardinality_violations(self):
        """MC7 with not exactly 7 options (e.g. 6 or 8) must be rejected."""
        q = self._build_valid_mc7()
        q["options"].pop()  # 6 options
        is_valid, errors = check_instance_invariants(q, "multiple_choice_7_options")
        assert not is_valid
        assert any("MC7 requires exactly 7 options (found 6)" in e for e in errors)

        q2 = self._build_valid_mc7()
        q2["options"].append({"id": "opt_h", "content": "R^2 = 0.900", "is_correct": False})  # 8 options
        is_valid2, errors2 = check_instance_invariants(q2, "multiple_choice_7_options")
        assert not is_valid2
        assert any("MC7 requires exactly 7 options (found 8)" in e for e in errors2)

    def test_mc7_empty_option_content(self):
        """MC7 with an empty string or whitespace option content must be rejected."""
        q = self._build_valid_mc7()
        q["options"][4]["content"] = "   "
        is_valid, errors = check_instance_invariants(q, "multiple_choice_7_options")
        assert not is_valid
        assert any("has empty content" in e for e in errors)

    def test_stem_length_violation(self):
        """Questions with stems shorter than 5 characters or empty must be rejected."""
        q = self._build_valid_mc7()
        q["stem"] = "Why?"
        is_valid, errors = check_instance_invariants(q, "multiple_choice_7_options")
        assert not is_valid
        assert any("Stem must be a non-empty string with at least 5 characters" in e for e in errors)

    def test_hints_scaffolding_violations(self):
        """Questions with <3 or >5 hints, or empty hints, must be rejected."""
        q = self._build_valid_mc7()
        q["hints"] = ["Solo una pista.", "Segunda pista."]  # 2 hints
        is_valid, errors = check_instance_invariants(q, "multiple_choice_7_options")
        assert not is_valid
        assert any("Instance must have between 3 and 5 hints" in e for e in errors)

        q["hints"] = [f"Pista {i}" for i in range(6)]  # 6 hints
        is_valid, errors = check_instance_invariants(q, "multiple_choice_7_options")
        assert not is_valid
        assert any("Instance must have between 3 and 5 hints" in e for e in errors)

        q["hints"] = ["Pista 1", "  ", "Pista 3"]  # Empty hint
        is_valid, errors = check_instance_invariants(q, "multiple_choice_7_options")
        assert not is_valid
        assert any("Hint 2 must be a non-empty string" in e for e in errors)

    def test_mc7_length_anti_giveaway_bounds(self):
        """MC7 where correct option is < 0.80*min(D) or > 1.20*max(D) must be rejected."""
        q = self._build_valid_mc7()
        # Distractors: lengths all exactly 40 characters
        for i in range(1, 7):
            q["options"][i]["content"] = f"Distractor_{i}_" + "X" * (40 - len(f"Distractor_{i}_"))
        assert all(len(q["options"][i]["content"]) == 40 for i in range(1, 7))

        # Case 1: Correct option too short: 25 chars < 0.80 * 40 = 32
        q["options"][0]["content"] = "Corta respuesta correcta"
        assert len(q["options"][0]["content"]) == 24
        is_valid, errors = check_instance_invariants(q, "multiple_choice_7_options", strict_length_bounds=True)
        assert not is_valid
        assert any("Length anti-giveaway violation: correct option too short" in e for e in errors)

        # Case 2: Correct option too long: 60 chars > 1.20 * 40 = 48
        q["options"][0]["content"] = "Esta respuesta correcta es excesivamente larga y detallada para el ejercicio"
        assert len(q["options"][0]["content"]) > 48
        is_valid2, errors2 = check_instance_invariants(q, "multiple_choice_7_options", strict_length_bounds=True)
        assert not is_valid2
        assert any("Length anti-giveaway violation: correct option too long" in e for e in errors2)

    def test_answer_leak_in_stem_or_hints(self):
        """Verbatim leaks of the non-trivial correct answer in the stem or first hint must be caught."""
        q = self._build_valid_mc7()
        q["options"][0]["content"] = "solucion_especifica"
        q["stem"] = "Dado que solucion_especifica es la respuesta, elija la correcta."
        is_valid, errors = check_instance_invariants(q, "multiple_choice_7_options")
        assert not is_valid
        assert any("Correct answer 'solucion_especifica' leaked verbatim in stem text" in e for e in errors)

        q2 = self._build_valid_mc7()
        q2["options"][0]["content"] = "solucion_especifica"
        q2["hints"][0] = "Recuerde que solucion_especifica es el valor esperado."
        is_valid2, errors2 = check_instance_invariants(q2, "multiple_choice_7_options")
        assert not is_valid2
        assert any("Correct answer 'solucion_especifica' leaked verbatim in first hint" in e for e in errors2)

    def test_fib_invariants_violations(self):
        """FIB instances missing answers, empty answers, or empty answer dictionaries must be rejected."""
        q_missing = {
            "stem": "Compute the determinant of the matrix.",
            "hints": ["Hint 1", "Hint 2", "Hint 3"],
            "interaction_type": "fill_in_the_blank",
        }
        is_valid, errors = check_instance_invariants(q_missing, "fill_in_the_blank")
        assert not is_valid
        assert any("FIB instance must provide a correct answer" in e for e in errors)

        q_empty_scalar = dict(q_missing, correct_answer="   ")
        is_valid, errors = check_instance_invariants(q_empty_scalar, "fill_in_the_blank")
        assert not is_valid
        assert any("FIB scalar answer is empty" in e for e in errors)

        q_empty_dict = dict(q_missing, correct_answer={"tolerance": 0.001})
        is_valid, errors = check_instance_invariants(q_empty_dict, "fill_in_the_blank")
        assert not is_valid
        assert any("FIB answer dict missing value/expression/canonical_algebraic" in e for e in errors)

    def test_ms_invariants_violations(self):
        """MS instances with <4 or >6 options, zero correct, all correct, or duplicate options must be rejected."""
        base_ms = {
            "stem": "Select all valid assumptions of the classical linear regression model.",
            "hints": ["Review Gauss-Markov assumptions.", "Check exogeneity.", "Verify homoscedasticity."],
            "interaction_type": "multiple_select",
            "options": [
                {"content": "Homoscedasticity of error terms", "is_correct": True, "error_rationale": None},
                {"content": "Strict exogeneity of regressors", "is_correct": True, "error_rationale": None},
                {"content": "Endogeneity of error terms", "is_correct": False, "error_rationale": "Viola el supuesto de exogeneidad estricta."},
                {"content": "Perfect multicollinearity", "is_correct": False, "error_rationale": "Impide invertir la matriz de regresores."},
            ],
        }
        # Valid baseline
        valid, errs = check_instance_invariants(base_ms, "multiple_select")
        assert valid, errs

        # Violation 1: Less than 4 options
        q_3opts = dict(base_ms, options=base_ms["options"][:3])
        v1, errs1 = check_instance_invariants(q_3opts, "multiple_select")
        assert not v1
        assert any("MS requires 4 to 6 options" in e for e in errs1)

        # Violation 2: Zero correct options
        q_0correct = {
            **base_ms,
            "options": [
                {"content": f"Opcion {i}", "is_correct": False, "error_rationale": f"Rationale distractor {i}"}
                for i in range(4)
            ],
        }
        v2, errs2 = check_instance_invariants(q_0correct, "multiple_select")
        assert not v2
        assert any("MS correct count must be between 1 and 3 (found 0 correct" in e for e in errs2)

        # Violation 3: All options correct
        q_allcorrect = {
            **base_ms,
            "options": [{"content": f"Opcion {i}", "is_correct": True, "error_rationale": None} for i in range(4)],
        }
        v3, errs3 = check_instance_invariants(q_allcorrect, "multiple_select")
        assert not v3
        assert any("MS correct count must be between 1 and 3 (found 4 correct" in e for e in errs3)

        # Violation 4: Duplicate option content in MS
        q_dup = {
            **base_ms,
            "options": [
                {"content": "Misma opcion repetida", "is_correct": True, "error_rationale": None},
                {"content": "Misma opcion repetida", "is_correct": False, "error_rationale": "Rationale distractor"},
                {"content": "Tercera opcion", "is_correct": False, "error_rationale": "Rationale 3"},
                {"content": "Cuarta opcion", "is_correct": False, "error_rationale": "Rationale 4"},
            ],
        }
        v4, errs4 = check_instance_invariants(q_dup, "multiple_select")
        assert not v4
        assert any("Duplicate option content detected in MS" in e for e in errs4)

    def test_check_templates_dry_run_catches_invariant_violations(self):
        """check_single_template must catch invariant violations during the 50-seed dry run."""
        bad_tpl = {
            "id": "TPL-DRY-RUN-FAIL",
            "interaction_type": "multiple_choice_7_options",
            "stem": "Determine the variance of {x}.",
            "hints": ["Hint 1", "Hint 2", "Hint 3"],
            "detailed_solution": "Solution text here.",
            "distractor_ids": ["D1", "D2", "D3", "D4", "D5", "D6"],
            "generate_py": (
                "def generate(rng):\n"
                "    # Deliberately produces a distractor identical to the correct answer on seed 105\n"
                "    val = '42'\n"
                "    d_val = '42' if rng.randint(0, 5) == 0 else '99'\n"
                "    return {\n"
                "        'vars': {'x': rng.randint(1, 100)},\n"
                "        'correct': val,\n"
                "        'distractors': [\n"
                "            {'value': d_val if i == 0 else f'val_{i}', 'distractor_id': f'D{i+1}'}\n"
                "            for i in range(6)\n"
                "        ]\n"
                "    }\n"
            ),
        }

        declared_dids = {"D1", "D2", "D3", "D4", "D5", "D6"}
        errs = check_single_template(
            template=bad_tpl,
            competency_id="Hab-01",
            declared_distractor_ids=declared_dids,
            num_dry_run_seeds=20,
        )
        assert len(errs) > 0
        assert any("invariant violation" in e or "TPL-D4 violation" in e for e in errs)

    def test_katex_syntax_unbalanced_inline_dollar_rejected(self):
        """Instances with unbalanced inline '$' delimiters must be rejected."""
        q = self._build_valid_mc7()
        q["stem"] = "Calcule el valor de $x + 1 para el parámetro $k$."
        is_valid, errors = check_instance_invariants(q, "multiple_choice_7_options")
        assert not is_valid
        assert any("Unbalanced inline math delimiter '$'" in e for e in errors)

    def test_katex_syntax_unbalanced_display_dollar_rejected(self):
        """Instances with unbalanced display '$$' delimiters must be rejected."""
        q = self._build_valid_mc7()
        q["stem"] = "Calcule $$x = 10 para el parámetro dado."
        is_valid, errors = check_instance_invariants(q, "multiple_choice_7_options")
        assert not is_valid
        assert any("Unbalanced display math delimiter '$$'" in e for e in errors)

    def test_katex_syntax_triple_dollar_rejected(self):
        """Instances with triple dollar '$$$' delimiters must be rejected."""
        q = self._build_valid_mc7()
        q["stem"] = "Evalúe $$$x = 5$$$ directamente para el estimador."
        is_valid, errors = check_instance_invariants(q, "multiple_choice_7_options")
        assert not is_valid
        assert any("Triple dollar delimiter '$$$'" in e for e in errors)

    def test_katex_syntax_residual_double_curly_braces_rejected(self):
        """Instances with residual f-string double braces '{{' or '}}' must be rejected."""
        q = self._build_valid_mc7()
        q["stem"] = r"Determine $\frac{{k}}{{L}}$ para el modelo."
        is_valid, errors = check_instance_invariants(q, "multiple_choice_7_options")
        assert not is_valid
        assert any("Residual double curly braces" in e for e in errors)

        # In option content
        q2 = self._build_valid_mc7()
        q2["options"][1]["content"] = "e^{{gt}}"
        is_valid2, errors2 = check_instance_invariants(q2, "multiple_choice_7_options")
        assert not is_valid2
        assert any("Residual double curly braces" in e for e in errors2)

    def test_katex_syntax_unsubstituted_placeholders_rejected(self):
        """Instances with unsubstituted template variables '{var}' must be rejected."""
        q = self._build_valid_mc7()
        q["stem"] = "Determine the value of variable {unsubstituted_param} in the model."
        is_valid, errors = check_instance_invariants(q, "multiple_choice_7_options")
        assert not is_valid
        assert any("Unsubstituted template variable '{unsubstituted_param}'" in e for e in errors)

        # Unsubstituted in hint
        q2 = self._build_valid_mc7()
        q2["hints"][0] = "Revise el valor de {unsubstituted_hint} cuidadosamente."
        is_valid2, errors2 = check_instance_invariants(q2, "multiple_choice_7_options")
        assert not is_valid2
        assert any("Unsubstituted template variable '{unsubstituted_hint}'" in e for e in errors2)

    def test_katex_syntax_valid_complex_math_accepted(self):
        """Legitimate KaTeX constructs (matrices, fractions, derivatives, subscripts) must be accepted."""
        q = self._build_valid_mc7()
        q["stem"] = (
            r"Sea la matriz $\begin{bmatrix} a & b \\ c & d \end{bmatrix}$ con "
            r"estimadores $\beta_{1}$ y $R^{2}$ y derivada $\frac{dy}{dx}$."
        )
        q["hints"] = [
            r"Verifique la traza $\text{tr}(A) = 0$.",
            r"Compruebe que la segunda derivada cumple $\phi''(k) < 0$.",
            r"El costo del parámetro es \$50 en la especificación.",
        ]
        q["detailed_solution"] = (
            r"La solución implica $\sum_{i=1}^{n} e_{i} = 0$ y $\phi''(k) < 0$."
        )
        is_valid, errors = check_instance_invariants(q, "multiple_choice_7_options")
        assert is_valid, f"Unexpected errors on valid KaTeX: {errors}"

    def test_katex_nested_accent_unclosed_rejected(self):
        """validate_katex_syntax must reject unclosed nested accent/style macros."""
        unclosed_cases = [
            r"Estimador $\hat{\boldsymbol{\beta}$ no converge.",
            r"Matriz $\bar{\mathbf{X}$ = 0 singular.",
            r"Error $\tilde{\boldsymbol{\epsilon}$ residual.",
            r"Vector $\hat{\mathbf{y}$ proyectado.",
        ]
        for tc in unclosed_cases:
            errs = validate_katex_syntax(tc, "stem")
            assert len(errs) > 0, f"Expected error for unclosed nested macro in '{tc}'"
            assert any("nested" in e.lower() or "unclosed" in e.lower() for e in errs)

        valid_cases = [
            r"Estimador $\hat{\boldsymbol{\beta}}$ converge.",
            r"Matriz $\bar{\mathbf{X}}$ simétrica.",
            r"Error $\tilde{\boldsymbol{\epsilon}}$ normal.",
            r"Vector $\hat{\mathbf{y}}$ proyectado.",
        ]
        for vc in valid_cases:
            errs = validate_katex_syntax(vc, "stem")
            assert not any("nested" in e.lower() for e in errs), f"Unexpected error for valid '{vc}': {errs}"

    def test_katex_macro_arity_rejected(self):
        """validate_katex_syntax must reject 2-argument macros missing arguments."""
        invalid_cases = [
            r"Fracción incompleta $\frac{a}$.",
            r"Fracción sin segundo argumento $\frac{a} + b$.",
            r"Fracción con denominador no cerrado $\frac{X_i - \bar{X}{\sum (X_i - \bar{X})^2}$.",
            r"Binomio incompleto $\binom{n}$.",
            r"Overset incompleto $\overset{def}$.",
            r"Underset incompleto $\underset{x \to 0}$.",
        ]
        for tc in invalid_cases:
            errs = validate_katex_syntax(tc, "stem")
            assert len(errs) > 0, f"Expected error for '{tc}'"
            assert any("macro" in e.lower() or "argument" in e.lower() or "requires 2" in e.lower() or "unclosed" in e.lower() for e in errs)

        valid_cases = [
            r"Fracción correcta $\frac{a}{b}$.",
            r"Fracción anidada $\frac{\frac{a}{b}}{c}$.",
            r"Binomio correcto $\binom{n}{k}$.",
            r"Overset correcto $\overset{\text{def}}{=}$.",
            r"Underset correcto $\underset{x \to 0}{\lim}$.",
        ]
        for vc in valid_cases:
            errs = validate_katex_syntax(vc, "stem")
            assert not any("requires 2" in e.lower() or "missing" in e.lower() for e in errs), f"Unexpected error for valid '{vc}': {errs}"

    def test_katex_in_distractor_error_rationale_rejected(self):
        """check_instance_invariants must validate KaTeX syntax in distractor error_rationale and misconception warning."""
        q = self._build_valid_mc7()
        q["options"][1]["error_rationale"] = r"Confusión con $\frac{a}$ incompleta."
        is_valid, errors = check_instance_invariants(q, "multiple_choice_7_options")
        assert not is_valid
        assert any("error_rationale" in e for e in errors)
        assert any("frac" in e.lower() or "argument" in e.lower() for e in errors)

        q2 = self._build_valid_mc7()
        q2["options"][2]["error_rationale"] = r"Error con $\hat{\boldsymbol{\beta}$ mal cerrado."
        is_valid2, errors2 = check_instance_invariants(q2, "multiple_choice_7_options")
        assert not is_valid2
        assert any("error_rationale" in e for e in errors2)
        assert any("nested" in e.lower() or "unclosed" in e.lower() for e in errors2)

        q3 = self._build_valid_mc7()
        q3["common_misconception_warning"] = r"Advertencia con $\hat{\boldsymbol{\beta}$ mal cerrado."
        is_valid3, errors3 = check_instance_invariants(q3, "multiple_choice_7_options")
        assert not is_valid3
        assert any("common_misconception_warning" in e for e in errors3)

    def test_katex_unclosed_environments_and_delimiters_rejected(self):
        """validate_katex_syntax must reject unclosed LaTeX environments and scalable delimiters."""
        unclosed_envs = [
            r"Matriz no cerrada $\begin{pmatrix} 1 & 2 \\ 3 & 4$.",
            r"Entorno discordante $\begin{bmatrix} 1 & 2 \end{pmatrix}$.",
            r"Casos sin cerrar $\begin{cases} x, & x > 0 \\ 0, & x \le 0$.",
            r"Aligned sin cerrar $\begin{aligned} a &= b \\ c &= d$.",
        ]
        for tc in unclosed_envs:
            errs = validate_katex_syntax(tc, "stem")
            assert len(errs) > 0, f"Expected error for '{tc}'"
            assert any("environment" in e.lower() or "unclosed" in e.lower() or "mismatched" in e.lower() for e in errs)

        unclosed_delims = [
            r"Paréntesis sin cerrar $\left( \frac{a}{b} )$.",
            r"Corchete sin cerrar $\left[ \frac{a}{b} ]$.",
            r"Llave sin cerrar $\left\{ x \}$.",
        ]
        for tc in unclosed_delims:
            errs = validate_katex_syntax(tc, "stem")
            assert len(errs) > 0, f"Expected error for '{tc}'"
            assert any("scalable delimiter" in e.lower() for e in errs)

        valid_syntax = [
            r"Matriz cerrada $\begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}$.",
            r"Casos cerrados $\begin{cases} x, & x > 0 \\ 0, & x \le 0 \end{cases}$.",
            r"Delimitadores cerrados $\left( \frac{a}{b} \right) + \left[ \frac{c}{d} \right] + \left\{ x \right\}$.",
        ]
        for vc in valid_syntax:
            errs = validate_katex_syntax(vc, "stem")
            assert not any("environment" in e.lower() or "scalable delimiter" in e.lower() for e in errs), f"Unexpected error for valid '{vc}': {errs}"

    def test_mc7_missing_error_rationale_rejected(self):
        """MC7 with missing or empty error_rationale on distractors must be rejected."""
        q = self._build_valid_mc7()
        q["options"][1]["error_rationale"] = None
        is_valid, errors = check_instance_invariants(q, "multiple_choice_7_options")
        assert not is_valid
        assert any("MC7 option 2 with is_correct=False must possess a non-empty 'error_rationale'" in e for e in errors)

        q2 = self._build_valid_mc7()
        q2["options"][2]["error_rationale"] = "   "
        is_valid2, errors2 = check_instance_invariants(q2, "multiple_choice_7_options")
        assert not is_valid2
        assert any("MC7 option 3 with is_correct=False must possess a non-empty 'error_rationale'" in e for e in errors2)

    def test_ms_missing_error_rationale_rejected(self):
        """MS with missing or empty error_rationale on incorrect options must be rejected."""
        base_ms = {
            "stem": "Select all valid assumptions of the classical linear regression model.",
            "hints": ["Review Gauss-Markov assumptions.", "Check exogeneity.", "Verify homoscedasticity."],
            "interaction_type": "multiple_select",
            "options": [
                {"content": "Homoscedasticity of error terms", "is_correct": True, "error_rationale": None},
                {"content": "Strict exogeneity of regressors", "is_correct": True, "error_rationale": None},
                {"content": "Endogeneity of error terms", "is_correct": False, "error_rationale": None},  # Missing!
                {"content": "Perfect multicollinearity", "is_correct": False, "error_rationale": "Viola el rango pleno."},
            ],
        }
        is_valid, errors = check_instance_invariants(base_ms, "multiple_select")
        assert not is_valid
        assert any("MS option 3 with is_correct=False must possess a non-empty 'error_rationale'" in e for e in errors)

    def test_assemble_sanitizes_katex_and_fstring_braces(self):
        """assemble_question automatically sanitizes $$$, f-string {{x}}, and option contents."""
        tpl = {
            "id": "TPL-SANITY",
            "interaction_type": "multiple_choice_7_options",
            "stem": r"Determine $\frac{{k}}{{L}}$ and $$$x$$$ for variable {val}.",
            "hints": [
                r"Pista 1 con $e^{{gt}}$ y {val}.",
                r"Pista 2 con delimitador $$$y$$$.",
                r"Pista 3 con $\dot{{k}}$ limpio.",
            ],
            "detailed_solution": r"Solución con $\frac{{a}}{{b}}$ y $$$c$$$.",
            "distractor_ids": ["D1", "D2", "D3", "D4", "D5", "D6"],
        }
        gen_res = {
            "vars": {"val": 42},
            "correct": r"e^{{gt}} = 42",
            "distractors": [
                {"value": rf"e^{{gt}} = {42 + i}", "distractor_id": f"D{i}"}
                for i in range(1, 7)
            ],
        }

        q = assemble_question(tpl, gen_res, "Hab-01", 1, seed=42)
        assert "$$$" not in q["stem"]
        assert "{{" not in q["stem"] and "}}" not in q["stem"]
        assert r"\frac{k}{L}" in q["stem"]
        assert "$$x$$" in q["stem"]
        assert "42" in q["stem"]

        # Check hints
        for h in q["hints"]:
            assert "$$$" not in h
            assert "{{" not in h and "}}" not in h

        # Check options
        for opt in q["options"]:
            assert "{{" not in opt["content"] and "}}" not in opt["content"]

        is_valid, errors = check_instance_invariants(q, "multiple_choice_7_options")
        assert is_valid, f"Sanitized question should pass invariants: {errors}"

    def test_assemble_ms_auto_assigns_distractor_rationales(self):
        """assemble_question automatically assigns default or CTA rationales to MS distractors."""
        tpl = {
            "id": "TPL-MS-RATIONALE",
            "interaction_type": "multiple_select",
            "stem": "Select the valid options for condition {c}.",
            "hints": ["Hint 1", "Hint 2", "Hint 3"],
            "detailed_solution": "Solution.",
        }
        gen_res = {
            "vars": {"c": "alpha"},
            "options": [
                {"text": "Opción correcta 1", "is_correct": True},
                {"text": "Opción correcta 2", "is_correct": True},
                {"text": "Opción incorrecta sin rationale", "is_correct": False},
                {"text": "Otra opción incorrecta con distractor", "is_correct": False, "distractor_id": "D-ERR-01"},
            ],
        }
        cta_map = {
            "D-ERR-01": {
                "manifestation": "Error atribuible a inversión de hipótesis nula.",
                "remediation_hint": "Revise la definición de hipótesis nula.",
            }
        }

        q = assemble_question(tpl, gen_res, "Hab-01", 1, cta_distractors_map=cta_map, seed=1)
        assert len(q["options"]) == 4

        # Verify all incorrect options have non-empty error_rationale
        for opt in q["options"]:
            if not opt["is_correct"]:
                assert opt["error_rationale"] is not None
                assert len(opt["error_rationale"].strip()) > 0
                if opt.get("distractor_id") == "D-ERR-01":
                    assert opt["error_rationale"] == "Error atribuible a inversión de hipótesis nula."
                else:
                    assert "Opción inválida derivada de una concepción errónea" in opt["error_rationale"]

        is_valid, errors = check_instance_invariants(q, "multiple_select")
        assert is_valid, f"Assembled MS question should pass invariants: {errors}"


# =============================================================================
# 3. DIVERSITY METRIC ADVERSARIAL TESTS
# =============================================================================
class TestDiversityMetricAdversarial:
    """Stress tests masked stem diversity calculations in diversity.py."""

    def test_mask_stem_numbers_patterns(self):
        """Verifies that numbers, matrices, arrays, and fractions are correctly normalized."""
        sample_stem = (
            r"Sea la matriz $\begin{bmatrix} 1.5 & -2.0 \\ 3.1e-2 & 4 \end{bmatrix}$ y "
            r"la tabla $\begin{array}{cc} x & y \\ 10 & 20 \end{array}$. "
            r"Calcule $\frac{3}{4} + 12.5$ para $k = 42$."
        )
        masked = mask_stem_numbers(sample_stem)
        assert "[BMATRIX]" in masked
        assert "[ARRAY]" in masked
        assert "[FRAC]" in masked
        assert "[NUM]" in masked
        # Verify no raw numbers remain
        assert "1.5" not in masked
        assert "-2.0" not in masked
        assert "42" not in masked

    def test_low_diversity_stem_set_fails_threshold(self):
        """A set of stems differing only by numbers must have unique/total << 0.5 and fail."""
        stems = [
            f"Calcule el valor de la integral definida de x^{i} en el intervalo [0, {i+2}]."
            for i in range(30)
        ]
        res = evaluate_competency_diversity(stems, min_diversity_ratio=0.5)
        assert res["total"] == 30
        assert res["unique_masked"] == 1
        assert res["diversity_ratio"] == round(1 / 30, 4)
        assert res["passes"] is False

    def test_high_diversity_stem_set_passes_threshold(self):
        """A set of stems with diverse structural phrasing must pass with ratio >= 0.5."""
        diverse_templates = [
            "Determine la derivada de primer orden respecto a x.",
            "Calcule la matriz de covarianzas del vector aleatorio.",
            "Verifique la condicion de ortogonalidad entre los residuos.",
            "Estime el error estandar de regresion para la muestra.",
            "Demuestre la consistencia asintotica del estimador MCO.",
            "Identifique la presencia de autocorrelacion serial en los errores.",
            "Formule la hipotesis nula del test de homocedasticidad de White.",
            "Calcule el estadistico de prueba F para significancia conjunta.",
            "Interprete el intervalo de confianza al nivel de significancia dado.",
            "Determine el grado de colinealidad usando el factor de inflacion de varianza.",
        ]
        # Construct 30 stems by pairing 10 templates with 3 variations each
        stems = [f"{t} Parámetro #{i}." for i, t in enumerate(diverse_templates * 3)]
        res = evaluate_competency_diversity(stems, min_diversity_ratio=0.5)
        assert res["total"] == 30
        # There are at least 10 unique structural templates
        assert res["unique_masked"] >= 10
        # Diversity ratio must exceed 10/30 = 0.33, let's verify exact ratio
        assert res["diversity_ratio"] == round(res["unique_masked"] / 30, 4)

    def test_diversity_exact_50_percent_boundary(self):
        """Exactly 10 unique masked stems out of 20 must produce ratio=0.50 and passes=True."""
        words = ["alfa", "bravo", "coca", "delta", "eco", "foxtrot", "golf", "hotel", "india", "juliet"]
        stems = []
        for w in words:
            stems.append(f"Estructura sintactica conceptual de {w}.")
            stems.append(f"Estructura sintactica conceptual de {w}.")  # Duplicate of pattern w
        assert len(stems) == 20

        res = evaluate_competency_diversity(stems, min_diversity_ratio=0.5)
        assert res["total"] == 20
        assert res["unique_masked"] == 10
        assert res["diversity_ratio"] == 0.50
        assert res["passes"] is True

    def test_diversity_sub_50_percent_boundary(self):
        """9 unique masked stems out of 20 produces ratio=0.45 and passes=False."""
        words = ["alfa", "bravo", "coca", "delta", "eco", "foxtrot", "golf", "hotel", "india"]
        stems = []
        # 9 patterns across 20 stems: 8 words duplicated twice (16 stems), 1 word repeated 4 times (4 stems)
        for w in words[:8]:
            stems.extend([f"Estructura sintactica conceptual de {w}.", f"Estructura sintactica conceptual de {w}."])
        stems.extend([f"Estructura sintactica conceptual de {words[8]}."] * 4)
        assert len(stems) == 20

        res = evaluate_competency_diversity(stems, min_diversity_ratio=0.5)
        assert res["total"] == 20
        assert res["unique_masked"] == 9
        assert res["diversity_ratio"] == 0.45
        assert res["passes"] is False

    def test_diversity_empty_stems(self):
        """Empty stems list safely returns zero metrics without ZeroDivisionError."""
        res = evaluate_competency_diversity([])
        assert res["total"] == 0
        assert res["unique_masked"] == 0
        assert res["diversity_ratio"] == 0.0
        assert res["passes"] is False


# =============================================================================
# 4. ANTI-GIVEAWAY BALANCE ADVERSARIAL TESTS
# =============================================================================
class TestAntiGiveawayBalanceAdversarial:
    """Stress tests option shuffling uniformity and length giveaway distribution."""

    def test_mc7_option_placement_uniform_distribution(self):
        """Across 1,400 MC7 assembled instances, correct option placement among A-G must be uniform."""
        base_tpl = {
            "id": "TPL-SHUFFLE",
            "interaction_type": "multiple_choice_7_options",
            "stem": "Determine the parameter.",
            "hints": ["Hint 1", "Hint 2", "Hint 3"],
            "detailed_solution": "Solution.",
        }
        gen_res = {
            "vars": {},
            "correct": "Valor correcto uniforme",
            "distractors": [
                {"value": f"Valor distractor {i}", "distractor_id": f"D{i}"}
                for i in range(1, 7)
            ],
        }

        letter_counts = {letter: 0 for letter in OPTION_LETTERS}
        sample_size = 1400

        for seed in range(sample_size):
            q = assemble_question(
                template=base_tpl,
                gen_result=gen_res,
                competency_id="Hab-01",
                question_index=seed + 1,
                seed=seed,
            )
            correct_letter = q["correct_answer"]
            assert correct_letter in letter_counts
            letter_counts[correct_letter] += 1

        # Statistical analysis: Chi-Squared goodness-of-fit test against uniform distribution (k=7)
        # Expected count per letter: 1400 / 7 = 200
        expected = sample_size / len(OPTION_LETTERS)
        chi2 = sum(((count - expected) ** 2) / expected for count in letter_counts.values())

        # Chi-squared critical value for df=6 at alpha=0.01 is 16.81
        # If chi2 < 16.81, we cannot reject the null hypothesis that positions are uniformly distributed
        assert chi2 < 16.81, f"Option distribution biased: counts={letter_counts}, chi2={chi2:.2f}"

        # Each position should roughly be within [160, 240] (11.4% to 17.1%)
        for letter, count in letter_counts.items():
            freq = count / sample_size
            assert 0.11 <= freq <= 0.18, f"Letter {letter} frequency {freq:.3f} out of expected bounds"

    def test_course_giveaway_distribution_rejects_longest_skew(self):
        """If correct option is longest in > 25% of MC7 items, course giveaway distribution must fail."""
        biased_questions = []
        for i in range(20):
            # In 10 out of 20 items (50% > 25%), make correct option the longest
            is_longest = i < 10
            c_content = "Respuesta Correcta Extraordinariamente Larga y Detallada" if is_longest else "Respuesta normal"
            d_content = "Corta dist" if is_longest else "Distractor normal de tamano"

            q = {
                "interaction_type": "multiple_choice_7_options",
                "options": [
                    {"content": c_content, "is_correct": True},
                    {"content": d_content, "is_correct": False},
                    {"content": d_content, "is_correct": False},
                    {"content": d_content, "is_correct": False},
                    {"content": d_content, "is_correct": False},
                    {"content": d_content, "is_correct": False},
                    {"content": d_content, "is_correct": False},
                ],
            }
            biased_questions.append(q)

        passes, stats = check_course_giveaway_distribution(biased_questions)
        assert passes is False
        assert stats["longest_ratio"] == 0.50
        assert stats["longest_ratio"] > 0.25

    def test_course_giveaway_distribution_rejects_shortest_skew(self):
        """If correct option is shortest in > 25% of MC7 items, course giveaway distribution must fail."""
        biased_questions = []
        for i in range(20):
            # In 8 out of 20 items (40% > 25%), make correct option the shortest
            is_shortest = i < 8
            c_content = "X" if is_shortest else "Respuesta con longitud promedio"
            d_content = "Distractor con longitud mucho mas amplia y desarrollada" if is_shortest else "Distractor promedio"

            q = {
                "interaction_type": "multiple_choice_7_options",
                "options": [
                    {"content": c_content, "is_correct": True},
                    {"content": d_content, "is_correct": False},
                    {"content": d_content, "is_correct": False},
                    {"content": d_content, "is_correct": False},
                    {"content": d_content, "is_correct": False},
                    {"content": d_content, "is_correct": False},
                    {"content": d_content, "is_correct": False},
                ],
            }
            biased_questions.append(q)

        passes, stats = check_course_giveaway_distribution(biased_questions)
        assert passes is False
        assert stats["shortest_ratio"] == 0.40
        assert stats["shortest_ratio"] > 0.25

    def test_course_giveaway_distribution_accepts_balanced_course(self):
        """When correct option is longest in <= 25% and shortest in <= 25%, course passes."""
        balanced_questions = []
        for i in range(20):
            # Longest in 2 items (10%), shortest in 2 items (10%), intermediate in 16 items (80%)
            if i < 2:
                lens = [30, 20, 20, 20, 20, 20, 20]
            elif i < 4:
                lens = [15, 25, 25, 25, 25, 25, 25]
            else:
                lens = [20, 25, 22, 18, 20, 24, 19]

            q = {
                "interaction_type": "multiple_choice_7_options",
                "options": [
                    {"content": "A" * lens[0], "is_correct": True},
                    {"content": "B" * lens[1], "is_correct": False},
                    {"content": "C" * lens[2], "is_correct": False},
                    {"content": "D" * lens[3], "is_correct": False},
                    {"content": "E" * lens[4], "is_correct": False},
                    {"content": "F" * lens[5], "is_correct": False},
                    {"content": "G" * lens[6], "is_correct": False},
                ],
            }
            balanced_questions.append(q)

        passes, stats = check_course_giveaway_distribution(balanced_questions)
        assert passes is True
        assert stats["longest_ratio"] == 0.10
        assert stats["shortest_ratio"] == 0.10


# =============================================================================
# 5. QUOTA SCALING ADVERSARIAL TESTS
# =============================================================================
class TestQuotaScalingAdversarial:
    """Stress tests competency quota scaling and balanced template allocation in instantiate.py."""

    def test_competency_quota_mapping(self):
        """Skill variants scale to 30; Fact/Concept variants scale to 20."""
        # Skills
        for s in ["skill", "hab", "habilidad", "SKILL", " Hab ", "HABILIDAD"]:
            assert get_competency_quota(s) == 30

        # Facts & Concepts
        for c in ["concept", "concepto", "fact", "hecho", "FACT", " Concept ", "HECHO", "other"]:
            assert get_competency_quota(c) == 20

    def test_template_quota_allocation_fairness(self):
        """Verifies quota distribution across templates fulfills targets without remainder loss."""
        # Skill: 30 questions across 6 templates -> exactly 5 each
        mock_templates = [{"id": f"TPL-{i}"} for i in range(1, 7)]
        q_map_skill = allocate_template_quotas(mock_templates, 30)
        assert sum(q_map_skill.values()) == 30
        assert all(v == 5 for v in q_map_skill.values())

        # Concept: 20 questions across 6 templates -> 20 // 6 = 3, remainder = 2 -> two get 4, four get 3
        q_map_concept = allocate_template_quotas(mock_templates, 20)
        assert sum(q_map_concept.values()) == 20
        assert sorted(q_map_concept.values()) == [3, 3, 3, 3, 4, 4]

    def _create_full_competency_templates(self) -> List[Dict[str, Any]]:
        """Build 6 complete parametric templates (2 MC7, 2 FIB, 2 MS)."""
        return [
            # MC7 Template 1
            {
                "id": "TPL-MC7-1",
                "interaction_type": "multiple_choice_7_options",
                "stem": "{verb} the slope coefficient estimator $\\beta_{1}$ for sample covariance ${cov}$ and variance ${var}$.",
                "hints": [
                    "Recall the OLS formula beta_1 = cov(X,Y) / var(X).",
                    "Substitute cov={cov} and var={var}.",
                    "Perform the division to obtain the coefficient.",
                ],
                "detailed_solution": "The estimator is beta_1 = {cov} / {var}.",
                "distractor_ids": ["D1", "D2", "D3", "D4", "D5", "D6"],
                "generate_py": (
                    "def generate(rng):\n"
                    "    verbs = ['Determine', 'Calculate', 'Estimate', 'Find', 'Evaluate', 'Compute', 'Deduce', 'State']\n"
                    "    verb = verbs[rng.randint(0, len(verbs) - 1)]\n"
                    "    cov = rng.randint(10, 50)\n"
                    "    var = rng.randint(2, 8)\n"
                    "    val = f'{cov/var:.3f}'\n"
                    "    return {\n"
                    "        'vars': {'verb': verb, 'cov': cov, 'var': var},\n"
                    "        'correct': f'beta_1 = {val}',\n"
                    "        'distractors': [\n"
                    "            {'value': f'beta_1 = {cov/(var+i):.3f}', 'distractor_id': f'D{i}'}\n"
                    "            for i in range(1, 7)\n"
                    "        ]\n"
                    "    }\n"
                ),
            },
            # MC7 Template 2
            {
                "id": "TPL-MC7-2",
                "interaction_type": "multiple_choice_7_options",
                "stem": "{verb} the sum of squared errors $SSE$ given $SST = {sst}$ and $SSR = {ssr}$.",
                "hints": [
                    "Recall the identity SST = SSR + SSE.",
                    "Rearrange to solve for SSE = SST - SSR.",
                    "Substitute sst={sst} and ssr={ssr}.",
                ],
                "detailed_solution": "SSE is obtained by subtraction.",
                "distractor_ids": ["D1", "D2", "D3", "D4", "D5", "D6"],
                "generate_py": (
                    "def generate(rng):\n"
                    "    verbs = ['Compute', 'Calculate', 'Determine', 'Evaluate', 'Obtain', 'Find', 'Isolate', 'Derive']\n"
                    "    verb = verbs[rng.randint(0, len(verbs) - 1)]\n"
                    "    sst = rng.randint(100, 200)\n"
                    "    ssr = rng.randint(20, 80)\n"
                    "    sse = sst - ssr\n"
                    "    return {\n"
                    "        'vars': {'verb': verb, 'sst': sst, 'ssr': ssr},\n"
                    "        'correct': f'SSE = {sse:03d}',\n"
                    "        'distractors': [\n"
                    "            {'value': f'SSE = {sse+i*5:03d}', 'distractor_id': f'D{i}'}\n"
                    "            for i in range(1, 7)\n"
                    "        ]\n"
                    "    }\n"
                ),
            },
            # FIB Template 1
            {
                "id": "TPL-FIB-1",
                "interaction_type": "fill_in_the_blank",
                "stem": "{phrase} the degrees of freedom for residuals in a model with $N = {n}$ and $k = {k}$ regressors.",
                "hints": [
                    "Recall that residual degrees of freedom equals n - k - 1.",
                    "Substitute n={n} and k={k}.",
                    "Subtract k and 1 from n.",
                ],
                "detailed_solution": "df = n - k - 1.",
                "generate_py": (
                    "def generate(rng):\n"
                    "    phrases = ['Calculate', 'Determine', 'Find', 'Evaluate', 'Obtain', 'Deduce', 'Report', 'Specify']\n"
                    "    phrase = phrases[rng.randint(0, len(phrases) - 1)]\n"
                    "    n = rng.randint(30, 100)\n"
                    "    k = rng.randint(2, 6)\n"
                    "    df = n - k - 1\n"
                    "    return {\n"
                    "        'vars': {'phrase': phrase, 'n': n, 'k': k},\n"
                    "        'correct': str(df),\n"
                    "        'tolerance': 0.001\n"
                    "    }\n"
                ),
            },
            # FIB Template 2
            {
                "id": "TPL-FIB-2",
                "interaction_type": "fill_in_the_blank",
                "stem": "{phrase} the t-statistic for a parameter estimate ${b}$ with standard error ${se}$.",
                "hints": [
                    "Recall the test statistic t = b / se.",
                    "Substitute the values b={b} and se={se}.",
                    "Divide the coefficient by its standard error.",
                ],
                "detailed_solution": "t = b / se.",
                "generate_py": (
                    "def generate(rng):\n"
                    "    phrases = ['Determine', 'Calculate', 'Find', 'Compute', 'Obtain', 'Estimate', 'Assess', 'Evaluate']\n"
                    "    phrase = phrases[rng.randint(0, len(phrases) - 1)]\n"
                    "    b = rng.randint(10, 40)\n"
                    "    se = rng.randint(2, 5)\n"
                    "    t_stat = round(b / se, 2)\n"
                    "    return {\n"
                    "        'vars': {'phrase': phrase, 'b': b, 'se': se},\n"
                    "        'correct': str(t_stat),\n"
                    "        'tolerance': 0.01\n"
                    "    }\n"
                ),
            },
            # MS Template 1
            {
                "id": "TPL-MS-1",
                "interaction_type": "multiple_select",
                "stem": "Select all properties guaranteed by the Gauss-Markov theorem {scenario} for model {m_id}.",
                "hints": [
                    "Recall what BLUE stands for.",
                    "Identify linearity and unbiasedness.",
                    "Verify minimum variance property.",
                ],
                "detailed_solution": "OLS estimators are Best Linear Unbiased Estimators.",
                "generate_py": (
                    "def generate(rng):\n"
                    "    scenarios = ['under classical assumptions', 'in multiple regression', 'for standard regressors', 'in econometric models', 'under spherical errors', 'in linear estimation', 'for random samples', 'in matrix form']\n"
                    "    scenario = scenarios[rng.randint(0, len(scenarios) - 1)]\n"
                    "    mid = rng.randint(1, 500)\n"
                    "    return {\n"
                    "        'vars': {'scenario': scenario, 'm_id': mid},\n"
                    "        'options': [\n"
                    "            {'text': 'Linearidad en los parametros', 'is_correct': True},\n"
                    "            {'text': 'Insesgadez del estimador OLS', 'is_correct': True},\n"
                    "            {'text': 'Varianza minima entre lineales insesgados', 'is_correct': True},\n"
                    "            {'text': 'Normalidad exacta en muestras pequenas', 'is_correct': False},\n"
                    "            {'text': 'Sesgo asintotico no nulo', 'is_correct': False}\n"
                    "        ]\n"
                    "    }\n"
                ),
            },
            # MS Template 2
            {
                "id": "TPL-MS-2",
                "interaction_type": "multiple_select",
                "stem": "Which of the following conditions lead to violation of spherical disturbances {context} dataset {d_id}?",
                "hints": [
                    "Recall spherical disturbance conditions.",
                    "Consider non-constant variance.",
                    "Consider correlated errors.",
                ],
                "detailed_solution": "Heteroscedasticity and autocorrelation violate spherical errors.",
                "generate_py": (
                    "def generate(rng):\n"
                    "    contexts = ['in empirical survey', 'in observational panel', 'in macroeconomic cross-section', 'in regression residuals', 'in sample disturbance vectors', 'in econometric estimation', 'in cross-sectional studies', 'in longitudinal data']\n"
                    "    context = contexts[rng.randint(0, len(contexts) - 1)]\n"
                    "    did = rng.randint(1, 500)\n"
                    "    return {\n"
                    "        'vars': {'context': context, 'd_id': did},\n"
                    "        'options': [\n"
                    "            {'text': 'Presencia de heterocedasticidad', 'is_correct': True},\n"
                    "            {'text': 'Autocorrelacion serial entre residuos', 'is_correct': True},\n"
                    "            {'text': 'Homocedasticidad uniforme', 'is_correct': False},\n"
                    "            {'text': 'Independencia temporal de perturbaciones', 'is_correct': False}\n"
                    "        ]\n"
                    "    }\n"
                ),
            },
        ]

    def test_full_skill_competency_instantiation_30_questions(self):
        """Instantiating a Skill competency yields exactly >= 30 questions distributed across MC7, FIB, MS."""
        skill_comp = {"id": "Hab-01", "type": "skill", "name": "Estimacion OLS"}
        templates = self._create_full_competency_templates()

        result = instantiate_competency(skill_comp, templates)

        assert result["competency_id"] == "Hab-01"
        assert result["quota_target"] == 30
        assert result["total_generated"] >= 30
        assert len(result["questions"]) == 30

        # Verify representation of all interaction types
        counts = result["counts_by_type"]
        assert counts.get("multiple_choice_7_options", 0) >= 10
        assert counts.get("fill_in_the_blank", 0) >= 10
        assert counts.get("multiple_select", 0) >= 10

        # Verify all questions pass invariants
        for q in result["questions"]:
            valid, errs = check_instance_invariants(q, q["interaction_type"])
            assert valid, f"Question {q['id']} failed invariants: {errs}"

        # Verify diversity stats
        assert result["diversity_stats"]["total"] == 30
        assert result["diversity_stats"]["passes"] is True

    def test_full_concept_competency_instantiation_20_questions(self):
        """Instantiating a Concept competency yields exactly >= 20 questions distributed across MC7, FIB, MS."""
        concept_comp = {"id": "Conc-01", "type": "concept", "name": "Supuestos OLS"}
        templates = self._create_full_competency_templates()

        result = instantiate_competency(concept_comp, templates)

        assert result["competency_id"] == "Conc-01"
        assert result["quota_target"] == 20
        assert result["total_generated"] >= 20
        assert len(result["questions"]) == 20

        # Verify representation of all interaction types
        counts = result["counts_by_type"]
        assert counts.get("multiple_choice_7_options", 0) >= 6
        assert counts.get("fill_in_the_blank", 0) >= 6
        assert counts.get("multiple_select", 0) >= 6

        # Verify all questions pass invariants
        for q in result["questions"]:
            valid, errs = check_instance_invariants(q, q["interaction_type"])
            assert valid, f"Question {q['id']} failed invariants: {errs}"

        # Verify diversity stats
        assert result["diversity_stats"]["total"] == 20
        assert result["diversity_stats"]["passes"] is True



# =============================================================================
# 6. TPL-VAR AND STEM VARIANTS ADVERSARIAL TESTS
# =============================================================================
class TestTplVarAndStemVariants:
    """Tests early variability validation (TPL-VAR) and stem_variants deterministic assembly."""

    def test_tpl_var_empty_vars_violation(self):
        """Templates generating empty vars dictionaries must trigger TPL-VAR violation."""
        tpl = {
            "id": "TPL-EMPTY-VARS",
            "interaction_type": "fill_in_the_blank",
            "stem": "Respuesta fija sin variables.",
            "hints": ["Hint 1", "Hint 2", "Hint 3"],
            "detailed_solution": "Solucion fija.",
            "distractor_ids": [],
            "generate_py": (
                "def generate(rng):\n"
                "    return {'vars': {}, 'correct': '42', 'distractors': []}\n"
            ),
        }
        errs = check_single_template(
            template=tpl,
            competency_id="Hab-01",
            declared_distractor_ids=set(),
            num_dry_run_seeds=50,
        )
        assert any(
            "TPL-VAR violation in 'TPL-EMPTY-VARS': 'vars' dictionary is empty. Templates must generate dynamic variables." in e
            for e in errs
        )

    def test_tpl_var_missing_placeholder_and_variants(self):
        """Templates without placeholders and without stem_variants must trigger TPL-VAR violation."""
        tpl = {
            "id": "TPL-NO-PLACEHOLDER",
            "interaction_type": "fill_in_the_blank",
            "stem": "Respuesta fija sin ningun placeholder en el enunciado.",
            "hints": ["Hint 1", "Hint 2", "Hint 3"],
            "detailed_solution": "Solucion fija.",
            "distractor_ids": [],
            "generate_py": (
                "def generate(rng):\n"
                "    x = rng.randint(1, 100)\n"
                "    return {'vars': {'x': x}, 'correct': str(x), 'distractors': []}\n"
            ),
        }
        errs = check_single_template(
            template=tpl,
            competency_id="Hab-01",
            declared_distractor_ids=set(),
            num_dry_run_seeds=50,
        )
        assert any(
            "TPL-VAR violation in 'TPL-NO-PLACEHOLDER': stem must contain at least one placeholder '{var}' or 'stem_variants' must be present." in e
            for e in errs
        )

    def test_tpl_var_narrow_domain_violation(self):
        """Templates producing fewer than 4 unique instances across 50 seeds must trigger TPL-VAR violation."""
        tpl = {
            "id": "TPL-NARROW",
            "interaction_type": "fill_in_the_blank",
            "stem": "El valor del parametro binario es {b}.",
            "hints": ["Hint 1", "Hint 2", "Hint 3"],
            "detailed_solution": "Solucion para {b}.",
            "distractor_ids": [],
            "generate_py": (
                "def generate(rng):\n"
                "    # Binary parameter: only 2 unique values across 50 seeds\n"
                "    b = rng.choice(['cero', 'uno'])\n"
                "    return {'vars': {'b': b}, 'correct': b, 'distractors': []}\n"
            ),
        }
        errs = check_single_template(
            template=tpl,
            competency_id="Hab-01",
            declared_distractor_ids=set(),
            num_dry_run_seeds=50,
        )
        assert any(
            "TPL-VAR violation in 'TPL-NARROW': Only 2/4 unique instances generated across 50 seeds. Parameter domain is too narrow or missing stem variations." in e
            for e in errs
        )

    def test_stem_variants_deterministic_selection_and_formatting(self):
        """assemble_question deterministically selects variants based on seed % len(variants)."""
        tpl = {
            "id": "TPL-VARIANTS",
            "interaction_type": "fill_in_the_blank",
            "stem": "Enunciado fallback con {val}.",
            "stem_variants": [
                "Variante primera con valor {val}.",
                "Variante segunda con parametro {val}.",
                "Variante tercera evaluando {val}.",
            ],
            "hints": ["H1", "H2", "H3"],
            "solution": "Solucion {val}.",
            "distractor_ids": [],
        }
        gen_res = {"vars": {"val": 99}, "correct": "99", "distractors": []}

        q0 = assemble_question(tpl, gen_res, "Hab-01", 1, seed=0)
        q1 = assemble_question(tpl, gen_res, "Hab-01", 2, seed=1)
        q2 = assemble_question(tpl, gen_res, "Hab-01", 3, seed=2)
        q3 = assemble_question(tpl, gen_res, "Hab-01", 4, seed=3)

        assert q0["stem"] == "Variante primera con valor 99."
        assert q1["stem"] == "Variante segunda con parametro 99."
        assert q2["stem"] == "Variante tercera evaluando 99."
        assert q3["stem"] == "Variante primera con valor 99."  # seed 3 % 3 == 0

    def test_stem_variants_satisfies_tpl_var_and_expands_capacity(self):
        """A template with sufficient stem_variants and dynamic vars passes TPL-VAR."""
        tpl = {
            "id": "TPL-PASS-VARIANTS",
            "interaction_type": "fill_in_the_blank",
            "stem": "Fallback stem.",
            "stem_variants": [
                "Variante A evaluando {p}.",
                "Variante B evaluando {p}.",
                "Variante C evaluando {p}.",
                "Variante D evaluando {p}.",
                "Variante E evaluando {p}.",
            ],
            "hints": ["Hint 1", "Hint 2", "Hint 3"],
            "detailed_solution": "Solucion para {p}.",
            "distractor_ids": [],
            "generate_py": (
                "def generate(rng):\n"
                "    p = rng.randint(10, 100)\n"
                "    return {'vars': {'p': p}, 'correct': str(p), 'distractors': []}\n"
            ),
        }
        errs = check_single_template(
            template=tpl,
            competency_id="Hab-01",
            declared_distractor_ids=set(),
            num_dry_run_seeds=50,
        )
        assert len(errs) == 0


if __name__ == "__main__":
    pytest.main(["-v", __file__])
