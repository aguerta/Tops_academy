"""Automated tests for template variability self-check, strict gates, and max-2 sharding policy.

Tests:
1. Template with narrow domain without variants fails competency diversity gate (TPL-VAR).
2. Template with stem_variants passes diversity gate.
3. test_shard_max_two: Verifies partition_competencies_into_shards and determine_shard_count.
4. TPL-STATIC-OPT: Unconditional mono-key blocking (even when vars == {}).
5. TPL-DYNAMIC-RATIONALE: Distractor varying across seeds with static rationale is rejected.
6. Multimodal TPL-D3 distractor coverage (MC7 6/6 vs MS >= 2 vs FIB 0).
7. Calibrated stem diversity: unmasked >= 0.85 with masked >= 0.25 passes.
"""

import copy
import json
from pathlib import Path
import pytest

# Ensure skill directory is on sys.path
SKILL_DIR = Path(__file__).resolve().parent.parent / ".agents" / "skills" / "content-to-course"
import sys
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from check_templates import (
    check_single_template,
    check_competency_diversity,
    check_templates_file_or_dir,
)
from plan_shards import determine_shard_count, partition_competencies_into_shards


def test_narrow_domain_without_variants_fails_diversity_gate():
    """A template with a narrow domain and no stem variants must fail the diversity gate."""
    narrow_template = {
        "id": "T-TEST-01",
        "competency_id": "C-TEST",
        "interaction_type": "fill_in_the_blank",
        "difficulty": "easy",
        "bloom": "Apply",
        "stem": "Determine el valor escalar constante {val} para el parámetro.",
        "generate_py": (
            "def generate(rng):\n"
            "    val = rng.choice([1, 2])\n"
            "    return {'vars': {'val': val}, 'correct': str(val), 'value': str(val), 'distractors': []}\n"
        ),
        "hints": [
            "Identifique el parámetro escalar presente en la expresión del problema.",
            "Aplique la definición formal para evaluar la magnitud correspondiente.",
            "Verifique que el resultado numérico sea compatible con el dominio.",
        ],
        "solution": "Solution {val}",
        "distractor_ids": [],
    }

    comp_def = {
        "id": "C-TEST",
        "name": "Test Competency",
        "type": "concept",
        "distractors": [],
    }

    errors = check_competency_diversity(
        templates=[narrow_template],
        competency=comp_def,
        num_seeds=20,
    )

    assert len(errors) > 0, "Narrow template without variants must fail diversity check"
    assert any("TPL-VAR VIOLATION" in e for e in errors)
    assert any("ACTION REQUIRED" in e for e in errors)


def test_template_with_stem_variants_passes_diversity_gate():
    """A template with distinct stem_variants must pass the diversity gate."""
    varied_template = {
        "id": "T-TEST-02",
        "competency_id": "C-TEST",
        "interaction_type": "fill_in_the_blank",
        "difficulty": "easy",
        "bloom": "Apply",
        "stem": "Determine el valor del parámetro {val}.",
        "stem_variants": [
            "Determine el valor del parámetro {val}.",
            "Para la configuración dada, halle el escalar {val}.",
            "Calcule la magnitud numérica del factor {val}.",
            "Identifique el valor cuantificado del término {val}.",
            "Establezca el valor analítico correspondiente a {val}.",
            "Evalúe directamente el coeficiente escalar {val}.",
        ],
        "generate_py": (
            "def generate(rng):\n"
            "    val = rng.randint(10, 100)\n"
            "    return {'vars': {'val': val}, 'correct': str(val), 'value': str(val), 'distractors': []}\n"
        ),
        "hints": [
            "Identifique el parámetro escalar presente en la expresión del problema.",
            "Aplique la definición formal para evaluar la magnitud correspondiente.",
            "Verifique que el resultado numérico sea compatible con el dominio.",
        ],
        "solution": "Solution {val}",
        "distractor_ids": [],
    }

    comp_def = {
        "id": "C-TEST",
        "name": "Test Competency",
        "type": "concept",
        "distractors": [],
    }

    errors = check_competency_diversity(
        templates=[varied_template],
        competency=comp_def,
        num_seeds=10,
    )

    assert len(errors) == 0, f"Template with variants should pass diversity check, but got: {errors}"


def test_check_templates_file_or_dir_variability_gate(tmp_path):
    """File-level validator check_templates_file_or_dir integrates competency diversity."""
    cta_data = {
        "course_id": "test_course",
        "title": "Test Course",
        "competencies": [
            {
                "id": "C-01",
                "name": "Competency 1",
                "type": "concept",
                "distractors": [],
            }
        ]
    }
    cta_file = tmp_path / "cta.json"
    cta_file.write_text(json.dumps(cta_data, indent=2), encoding="utf-8")

    # 1. Narrow template without variants -> should fail
    tpl_data_fail = {
        "competency_id": "C-01",
        "templates": [
            {
                "id": "T-C01-01",
                "competency_id": "C-01",
                "interaction_type": "fill_in_the_blank",
                "difficulty": "easy",
                "bloom": "Apply",
                "stem": "Encuentre el valor fijo {v}.",
                "generate_py": "def generate(rng):\n    v = rng.choice([1, 2])\n    return {'vars': {'v': v}, 'correct': str(v), 'value': str(v), 'distractors': []}\n",
                "cross_check_py": "def verify(res):\n    return int(res['correct']) in [1, 2]",
                "hints": [
                    "Identifique el parámetro numérico en el enunciado proporcionado.",
                    "Aplique la fórmula analítica correspondiente para evaluar la variable.",
                    "Asegúrese de redondear o verificar la solución de acuerdo con la consigna.",
                ],
                "solution": "sol {v}",
                "distractor_ids": [],
            }
        ]
    }
    tpl_file = tmp_path / "C-01.json"
    tpl_file.write_text(json.dumps(tpl_data_fail, indent=2), encoding="utf-8")

    valid_fail, errors_fail = check_templates_file_or_dir(tpl_file, cta_path=cta_file, num_dry_run_seeds=20)
    assert not valid_fail, "Expected validation to fail for narrow domain without variants"
    assert any("TPL-VAR" in e for e in errors_fail)

    # 2. Template with variants and wide domain -> should pass
    tpl_data_pass = {
        "competency_id": "C-01",
        "templates": [
            {
                "id": "T-C01-01",
                "competency_id": "C-01",
                "interaction_type": "fill_in_the_blank",
                "difficulty": "easy",
                "bloom": "Apply",
                "stem": "Encuentre el valor fijo {v}.",
                "stem_variants": [
                    "Encuentre el valor fijo {v}.",
                    "Calcule la magnitud del parámetro {v}.",
                    "Determine el coeficiente numérico {v}.",
                    "Halle el valor escalar correspondiente a {v}.",
                    "Evalúe analíticamente la expresión {v}.",
                    "Identifique el valor matemático para {v}.",
                ],
                "generate_py": "def generate(rng):\n    v = rng.randint(10, 200)\n    return {'vars': {'v': v}, 'correct': str(v), 'value': str(v), 'distractors': []}\n",
                "cross_check_py": "def verify(res):\n    return int(res['correct']) >= 10",
                "hints": [
                    "Identifique el parámetro numérico en el enunciado proporcionado.",
                    "Aplique la fórmula analítica correspondiente para evaluar la variable.",
                    "Asegúrese de redondear o verificar la solución de acuerdo con la consigna.",
                ],
                "solution": "sol {v}",
                "distractor_ids": [],
            }
        ]
    }
    tpl_file.write_text(json.dumps(tpl_data_pass, indent=2), encoding="utf-8")

    valid_pass, errors_pass = check_templates_file_or_dir(tpl_file, cta_path=cta_file, num_dry_run_seeds=10)
    assert valid_pass, f"Expected validation to pass, but got errors: {errors_pass}"
    assert len(errors_pass) == 0


def test_tpl_static_opt_unconditional_mono_key_blocked():
    """TPL-STATIC-OPT: Template that outputs constant correct answer must be rejected unconditionally, even if vars is empty."""
    # Case A: Author leaves vars == {} attempting to fake non-parametric template
    tpl_empty_vars = {
        "id": "T-STATIC-EMPTY-VARS",
        "competency_id": "C-CONCEPT",
        "interaction_type": "multiple_choice_7_options",
        "difficulty": "easy",
        "bloom": "Understand",
        "stem": "¿Cuál es la propiedad fundamental de la convergencia uniforme?",
        "stem_variants": [
            "¿Cuál es la propiedad fundamental de la convergencia uniforme?",
            "Identifique la característica esencial que define la convergencia uniforme:",
            "Para sucesiones funcionales, ¿qué propiedad asegura la convergencia uniforme?",
        ],
        "generate_py": (
            "def generate(rng):\n"
            "    return {\n"
            "        'vars': {},\n"
            "        'correct': 'Preserva la continuidad de las funciones límite en el intervalo.',\n"
            "        'distractors': [\n"
            "            {'value': f'Opción errónea {i}', 'distractor_id': f'D{i+1}', 'error_rationale': f'Explicación {i}'}\n"
            "            for i in range(6)\n"
            "        ]\n"
            "    }\n"
        ),
        "cross_check_py": "def verify(res):\n    return 'continuidad' in res['correct']",
        "hints": [
            "Recuerde el teorema de conservación de continuidad para límites uniformes.",
            "Analice si la convergencia puntual basta o se requiere cota global uniforme.",
            "La continuidad se preserva cuando el supremo de la diferencia tiende a cero.",
        ],
        "solution": "La convergencia uniforme preserva la continuidad del límite funcional.",
        "distractor_ids": ["D1", "D2", "D3", "D4", "D5", "D6"],
    }

    errs = check_single_template(
        template=tpl_empty_vars,
        competency_id="C-CONCEPT",
        declared_distractor_ids={"D1", "D2", "D3", "D4", "D5", "D6"},
        num_dry_run_seeds=20,
        strict=True,
    )
    assert any("TPL-STATIC-OPT" in e for e in errs), f"Expected TPL-STATIC-OPT for empty vars mono-key, got: {errs}"


def test_tpl_dynamic_rationale_slot_variation_enforced():
    """TPL-DYNAMIC-RATIONALE: Distractor varying in content across seeds MUST also vary its error_rationale."""
    tpl_static_rationale = {
        "id": "T-STATIC-RAT",
        "competency_id": "Hab-01",
        "interaction_type": "multiple_choice_7_options",
        "difficulty": "medium",
        "bloom": "Apply",
        "stem": "Determine el valor escalar para el parámetro {k}.",
        "generate_py": (
            "def generate(rng):\n"
            "    k = rng.randint(5, 50)\n"
            "    return {\n"
            "        'vars': {'k': k},\n"
            "        'correct': f'Respuesta correcta con k={k}',\n"
            "        'distractors': [\n"
            "            {'value': f'Distractor {i} con valor {k + i + 1}', 'distractor_id': f'D{i+1}', 'error_rationale': 'Rationale estático idéntico en todas las semillas.'}\n"
            "            for i in range(6)\n"
            "        ]\n"
            "    }\n"
        ),
        "cross_check_py": "def verify(res):\n    return int(res['vars']['k']) >= 5",
        "hints": [
            "Identifique el parámetro escalar presente en la expresión del problema.",
            "Aplique la definición formal para evaluar la magnitud correspondiente.",
            "Verifique que el resultado numérico sea compatible con el dominio.",
        ],
        "solution": "Solución con {k}",
        "distractor_ids": ["D1", "D2", "D3", "D4", "D5", "D6"],
    }

    errs = check_single_template(
        template=tpl_static_rationale,
        competency_id="Hab-01",
        declared_distractor_ids={"D1", "D2", "D3", "D4", "D5", "D6"},
        num_dry_run_seeds=20,
        strict=True,
    )
    assert any("TPL-DYNAMIC-RATIONALE" in e for e in errs), f"Expected TPL-DYNAMIC-RATIONALE for static rationale on dynamic distractor, got: {errs}"


def test_tpl_static_opt_empty_vars_mono_key_fib_and_ms():
    """TPL-STATIC-OPT: fill_in_the_blank and multiple_select with empty vars producing mono-key must fail under strict=True."""
    # 1. fill_in_the_blank with vars == {}
    tpl_fib = {
        "id": "T-FIB-STATIC",
        "competency_id": "C-TEST-FIB",
        "interaction_type": "fill_in_the_blank",
        "difficulty": "easy",
        "bloom": "Apply",
        "stem": "Determine el valor constante del parámetro numérico.",
        "generate_py": "def generate(rng):\n    return {'vars': {}, 'correct': '42', 'value': '42', 'distractors': []}\n",
        "cross_check_py": "def verify(res):\n    return int(res['correct']) == 42",
        "hints": [
            "Identifique el parámetro escalar presente en el enunciado.",
            "Aplique la definición formal para evaluar la magnitud requerida.",
            "Verifique que la respuesta numérica sea compatible con las unidades.",
        ],
        "solution": "La solución constante es 42.",
        "distractor_ids": [],
    }
    errs_fib = check_single_template(
        template=tpl_fib,
        competency_id="C-TEST-FIB",
        declared_distractor_ids=set(),
        num_dry_run_seeds=20,
        strict=True,
    )
    assert any("TPL-STATIC-OPT" in e for e in errs_fib), f"Expected TPL-STATIC-OPT for FIB mono-key, got: {errs_fib}"

    # 2. multiple_select with vars == {}
    tpl_ms = {
        "id": "T-MS-STATIC",
        "competency_id": "C-TEST-MS",
        "interaction_type": "multiple_select",
        "difficulty": "medium",
        "bloom": "Analyze",
        "stem": "Seleccione todas las afirmaciones verdaderas respecto al modelo analizado:",
        "generate_py": (
            "def generate(rng):\n"
            "    return {\n"
            "        'vars': {},\n"
            "        'options': [\n"
            "            {'content': 'Afirmación verdadera A sobre el sistema.', 'is_correct': True, 'distractor_id': None},\n"
            "            {'content': 'Afirmación verdadera B sobre el sistema.', 'is_correct': True, 'distractor_id': None},\n"
            "            {'content': 'Afirmación falsa C sobre el sistema.', 'is_correct': False, 'distractor_id': 'D1', 'error_rationale': 'Explicación del error C.'},\n"
            "            {'content': 'Afirmación falsa D sobre el sistema.', 'is_correct': False, 'distractor_id': 'D2', 'error_rationale': 'Explicación del error D.'},\n"
            "        ],\n"
            "        'distractors': []\n"
            "    }\n"
        ),
        "cross_check_py": "def verify(res):\n    return any(opt['is_correct'] for opt in res['options'])",
        "hints": [
            "Identifique las afirmaciones verdaderas basadas en las propiedades formales.",
            "Descarte las afirmaciones que contradicen las condiciones dadas.",
            "Seleccione las opciones que satisfacen simultáneamente todos los criterios.",
        ],
        "solution": "Las opciones A y B son verdaderas.",
        "distractor_ids": ["D1", "D2"],
    }
    errs_ms = check_single_template(
        template=tpl_ms,
        competency_id="C-TEST-MS",
        declared_distractor_ids={"D1", "D2"},
        num_dry_run_seeds=20,
        strict=True,
    )
    assert any("TPL-STATIC-OPT" in e for e in errs_ms), f"Expected TPL-STATIC-OPT for MS mono-key, got: {errs_ms}"


def test_tpl_dynamic_rationale_ms_slot_variation_enforced():
    """TPL-DYNAMIC-RATIONALE: multiple_select distractor varying in content across seeds MUST also vary rationale."""
    tpl_ms_dynamic_slot = {
        "id": "T-MS-DYN-SLOT",
        "competency_id": "Hab-02",
        "interaction_type": "multiple_select",
        "difficulty": "medium",
        "bloom": "Analyze",
        "stem": "Seleccione las afirmaciones correctas para el parámetro {k}:",
        "generate_py": (
            "def generate(rng):\n"
            "    k = rng.randint(5, 50)\n"
            "    return {\n"
            "        'vars': {'k': k},\n"
            "        'options': [\n"
            "            {'content': f'Afirmación verdadera con k={k}', 'is_correct': True, 'distractor_id': None},\n"
            "            {'content': f'Segunda afirmación verdadera con k={k}', 'is_correct': True, 'distractor_id': None},\n"
            "            {'content': f'Afirmación errónea con valor k={k+1}', 'is_correct': False, 'distractor_id': 'D1', 'error_rationale': 'Rationale estático invariante entre semillas.'},\n"
            "            {'content': f'Afirmación errónea con valor k={k+2}', 'is_correct': False, 'distractor_id': 'D2', 'error_rationale': f'Rationale dinámico con valor k={k}.'},\n"
            "        ],\n"
            "        'distractors': []\n"
            "    }\n"
        ),
        "cross_check_py": "def verify(res):\n    return int(res['vars']['k']) >= 5",
        "hints": [
            "Identifique las condiciones de validez analítica en la consigna.",
            "Descarte la opción errónea evaluando el parámetro k.",
            "Verifique la consistencia lógica de las afirmaciones seleccionadas.",
        ],
        "solution": "Solución con {k}",
        "distractor_ids": ["D1", "D2"],
    }
    errs = check_single_template(
        template=tpl_ms_dynamic_slot,
        competency_id="Hab-02",
        declared_distractor_ids={"D1", "D2"},
        num_dry_run_seeds=20,
        strict=True,
    )
    assert any("TPL-DYNAMIC-RATIONALE" in e for e in errs), f"Expected TPL-DYNAMIC-RATIONALE for MS dynamic distractor with static rationale, got: {errs}"


def test_tpl_dynamic_rationale_competency_pool_uniqueness_and_conceptual_invariant():
    """TPL-DYNAMIC-RATIONALE: verifies >=30 distractor pool uniqueness < 35% fails, while conceptual invariant distractor does not generate false positives."""
    comp_def = {
        "id": "C-POOL-RAT",
        "name": "Pool Rationale Diversity",
        "type": "concept",
        "distractors": [{"id": f"D{i+1}", "name": f"D{i+1}"} for i in range(6)],
    }

    # Low uniqueness pool (< 35% unique rationales among >= 30 distractors)
    questions_low = [
        {
            "interaction_type": "multiple_choice_7_options",
            "stem": f"Pregunta conceptual número {i} sobre el modelo.",
            "options": [
                {"content": "Correcta", "is_correct": True},
                {"content": f"Opción A {i}", "is_correct": False, "error_rationale": "Rationale repetido idéntico A."},
                {"content": f"Opción B {i}", "is_correct": False, "error_rationale": "Rationale repetido idéntico B."},
            ],
        }
        for i in range(15)  # 15 * 2 = 30 distractors with only 2 unique rationales (6.7% < 35%)
    ]
    # Check competency diversity pool check
    errs_low = check_competency_diversity(
        templates=[],
        competency=comp_def,
        questions=questions_low,
        strict=True,
    )
    assert any("TPL-DYNAMIC-RATIONALE" in e for e in errs_low), f"Expected pool uniqueness rejection, got: {errs_low}"

    # Conceptual invariant distractor in rotation: content does NOT vary across seeds
    tpl_conceptual_rot = {
        "id": "T-CONCEPT-ROT",
        "competency_id": "C-CONCEPT-ROT",
        "interaction_type": "multiple_choice_7_options",
        "difficulty": "easy",
        "bloom": "Understand",
        "stem": "Identifique la propiedad correcta para la configuración {idx}:",
        "generate_py": (
            "def generate(rng):\n"
            "    idx = rng.randint(1, 10)\n"
            "    return {\n"
            "        'vars': {'idx': idx},\n"
            "        'correct': f'Propiedad válida correspondiente al caso {idx}.',\n"
            "        'distractors': [\n"
            "            {'value': 'Distractor puramente conceptual invariante.', 'distractor_id': 'D1', 'error_rationale': 'El concepto invariante no aplica al caso analizado.'},\n"
            "            {'value': f'Distractor variable con caso {idx+1}', 'distractor_id': 'D2', 'error_rationale': f'El caso {idx+1} difiere del valor {idx}.'},\n"
            "            {'value': f'Distractor variable con caso {idx+2}', 'distractor_id': 'D3', 'error_rationale': f'El caso {idx+2} difiere del valor {idx}.'},\n"
            "            {'value': f'Distractor variable con caso {idx+3}', 'distractor_id': 'D4', 'error_rationale': f'El caso {idx+3} difiere del valor {idx}.'},\n"
            "            {'value': f'Distractor variable con caso {idx+4}', 'distractor_id': 'D5', 'error_rationale': f'El caso {idx+4} difiere del valor {idx}.'},\n"
            "            {'value': f'Distractor variable con caso {idx+5}', 'distractor_id': 'D6', 'error_rationale': f'El caso {idx+5} difiere del valor {idx}.'},\n"
            "        ]\n"
            "    }\n"
        ),
        "cross_check_py": "def verify(res):\n    return int(res['vars']['idx']) >= 1",
        "hints": [
            "Identifique la configuración específica en la consigna.",
            "Aplique la propiedad analítica formal correspondiente al caso.",
            "Descarte las afirmaciones que no satisfacen la definición.",
        ],
        "solution": "Solución para caso {idx}",
        "distractor_ids": ["D1", "D2", "D3", "D4", "D5", "D6"],
    }
    errs_concept = check_single_template(
        template=tpl_conceptual_rot,
        competency_id="C-CONCEPT-ROT",
        declared_distractor_ids={"D1", "D2", "D3", "D4", "D5", "D6"},
        num_dry_run_seeds=20,
        strict=True,
    )
    # The invariant distractor D1 has len(u_contents) == 1, so it must NOT trigger TPL-DYNAMIC-RATIONALE slot violation
    assert not any("TPL-DYNAMIC-RATIONALE" in e for e in errs_concept), f"Conceptual invariant distractor must not trigger false positive, got: {errs_concept}"


def test_multimodal_tpl_d3_coverage(tmp_path):
    """Rule TPL-D3: verifies multimodal distractor coverage (100% FIB, FIB + MS with >= 2 IDs, and MC7 with 6/6)."""
    # 1. 100% FIB competency: passes without distractors
    cta_fib = {
        "course_id": "test_fib_course",
        "title": "Test FIB Course",
        "competencies": [{"id": "C-FIB", "name": "FIB Comp", "type": "skill", "distractors": []}],
    }
    cta_fib_file = tmp_path / "cta_fib.json"
    cta_fib_file.write_text(json.dumps(cta_fib, indent=2), encoding="utf-8")

    tpl_fib_data = {
        "competency_id": "C-FIB",
        "templates": [
            {
                "id": "T-FIB-01",
                "competency_id": "C-FIB",
                "interaction_type": "fill_in_the_blank",
                "difficulty": "easy",
                "bloom": "Apply",
                "stem": "Determine el valor escalar {v}.",
                "stem_variants": [
                    "Determine el valor escalar {v}.",
                    "Calcule el valor escalar {v}.",
                    "Halle la magnitud escalar {v}.",
                    "Evalúe el parámetro numérico {v}.",
                    "Identifique el escalar {v}.",
                    "Establezca el valor analítico {v}.",
                ],
                "generate_py": "def generate(rng):\n    v = rng.randint(10, 200)\n    return {'vars': {'v': v}, 'correct': str(v), 'value': str(v), 'distractors': []}\n",
                "cross_check_py": "def verify(res):\n    return int(res['vars']['v']) >= 10",
                "hints": [
                    "Identifique el parámetro numérico en el enunciado proporcionado.",
                    "Aplique la fórmula analítica correspondiente para evaluar la variable.",
                    "Asegúrese de redondear o verificar la solución de acuerdo con la consigna.",
                ],
                "solution": "sol {v}",
                "distractor_ids": [],
            }
        ],
    }
    tpl_fib_file = tmp_path / "C-FIB.json"
    tpl_fib_file.write_text(json.dumps(tpl_fib_data, indent=2), encoding="utf-8")
    valid_fib, errs_fib = check_templates_file_or_dir(tpl_fib_file, cta_path=cta_fib_file, num_dry_run_seeds=10)
    assert valid_fib, f"100% FIB must pass TPL-D3 without false blocks, got: {errs_fib}"

    # 2. FIB + MS competency with >= 2 declared distractor IDs referenced in MS: passes
    cta_ms = {
        "course_id": "test_ms_course",
        "title": "Test MS Course",
        "competencies": [
            {
                "id": "C-MS",
                "name": "MS Comp",
                "type": "skill",
                "distractors": [{"id": f"D{i+1}", "name": f"Distractor {i+1}"} for i in range(6)],
            }
        ],
    }
    cta_ms_file = tmp_path / "cta_ms.json"
    cta_ms_file.write_text(json.dumps(cta_ms, indent=2), encoding="utf-8")

    tpl_ms_pass_data = {
        "competency_id": "C-MS",
        "templates": [
            {
                "id": "T-MS-PASS",
                "competency_id": "C-MS",
                "interaction_type": "multiple_select",
                "difficulty": "medium",
                "bloom": "Analyze",
                "stem": "Seleccione las afirmaciones correctas para {k}:",
                "stem_variants": [
                    "Seleccione las afirmaciones correctas para {k}:",
                    "Para el parámetro {k}, identifique las opciones válidas:",
                    "Considere el factor {k} y marque las propiedades verdaderas:",
                    "Halle todas las opciones consistentes con {k}:",
                    "Evalúe cuáles afirmaciones aplican para {k}:",
                    "Determine las características verdaderas de {k}:",
                ],
                "generate_py": (
                    "def generate(rng):\n"
                    "    k = rng.randint(10, 100)\n"
                    "    return {\n"
                    "        'vars': {'k': k},\n"
                    "        'options': [\n"
                    "            {'content': f'Afirmación verdadera A con k={k}', 'is_correct': True, 'distractor_id': None},\n"
                    "            {'content': f'Afirmación verdadera B con k={k}', 'is_correct': True, 'distractor_id': None},\n"
                    "            {'content': f'Afirmación falsa C con k={k+1}', 'is_correct': False, 'distractor_id': 'D1', 'error_rationale': f'Error D1 con k={k}'},\n"
                    "            {'content': f'Afirmación falsa D con k={k+2}', 'is_correct': False, 'distractor_id': 'D2', 'error_rationale': f'Error D2 con k={k}'},\n"
                    "        ],\n"
                    "        'distractors': []\n"
                    "    }\n"
                ),
                "cross_check_py": "def verify(res):\n    return int(res['vars']['k']) >= 10",
                "hints": [
                    "Identifique las condiciones de validez analítica en la consigna.",
                    "Descarte la opción errónea evaluando el parámetro k.",
                    "Verifique la consistencia lógica de las afirmaciones seleccionadas.",
                ],
                "solution": "sol {k}",
                "distractor_ids": ["D1", "D2"],  # >= 2 IDs
            }
        ],
    }
    tpl_ms_pass_file = tmp_path / "C-MS.json"
    tpl_ms_pass_file.write_text(json.dumps(tpl_ms_pass_data, indent=2), encoding="utf-8")
    valid_ms, errs_ms = check_templates_file_or_dir(tpl_ms_pass_file, cta_path=cta_ms_file, num_dry_run_seeds=10)
    assert valid_ms, f"MS with >= 2 IDs must pass TPL-D3, got: {errs_ms}"

    # 3. MS competency referencing only 1 distractor ID: fails TPL-D3
    tpl_ms_fail_data = copy.deepcopy(tpl_ms_pass_data)
    tpl_ms_fail_data["templates"][0]["distractor_ids"] = ["D1"]
    tpl_ms_fail_file = tmp_path / "C-MS-FAIL.json"
    tpl_ms_fail_file.write_text(json.dumps(tpl_ms_fail_data, indent=2), encoding="utf-8")
    valid_ms_fail, errs_ms_fail = check_templates_file_or_dir(tpl_ms_fail_file, cta_path=cta_ms_file, num_dry_run_seeds=10)
    assert not valid_ms_fail
    assert any("TPL-D3" in e for e in errs_ms_fail)



def test_calibrated_stem_diversity_passes():
    """Calibrated stem diversity allows 3 genuine stems with unmasked ratio >= 0.85 when masked ratio >= 0.25."""
    comp_def = {"id": "C-CALIB", "name": "Calibrated Stem Diversity", "type": "skill", "distractors": []}
    raw_stems = [
        [
            "Determine el valor analítico para el parámetro {k} en el sistema.",
            "Para el sistema analizado, halle el parámetro {k} correspondiente.",
            "Obtenga el valor numérico exacto de {k} en la formulación.",
        ],
        [
            "Calcule la magnitud escalar correspondiente a {k} en el sistema.",
            "Estime la magnitud física dada por {k} según las condiciones.",
            "A partir de la ecuación, determine la magnitud {k} del modelo.",
        ],
        [
            "Evalúe la expresión del parámetro {k} en el sistema.",
            "Efectúe la evaluación del término {k} para los datos provistos.",
            "Computar el valor específico de {k} satisfaciendo las restricciones.",
        ],
    ]
    templates = [
        {
            "id": f"T-CALIB-{i:02d}",
            "competency_id": "C-CALIB",
            "interaction_type": "fill_in_the_blank",
            "difficulty": "medium",
            "bloom": "Apply",
            "stem": raw_stems[i - 1][0],
            "stem_variants": raw_stems[i - 1],
            "generate_py": (
                "def generate(rng):\n"
                "    k = rng.randint(10, 500)\n"
                "    return {'vars': {'k': k}, 'correct': str(k), 'value': str(k), 'distractors': []}\n"
            ),
            "cross_check_py": "def verify(res):\n    return int(res['vars']['k']) >= 10",
            "hints": [
                "Identifique el parámetro numérico en el enunciado proporcionado.",
                "Aplique la fórmula analítica correspondiente para evaluar la variable.",
                "Asegúrese de redondear o verificar la solución de acuerdo con la consigna.",
            ],
            "solution": "Solución para {k}",
            "distractor_ids": [],
        }
        for i in range(1, 4)
    ]

    errors = check_competency_diversity(
        templates=templates,
        competency=comp_def,
        num_seeds=30,
        strict=True,
    )
    assert not any("TPL-VAR VIOLATION" in e for e in errors), f"Calibrated stems should pass diversity, got: {errors}"


def test_shard_max_two():
    """Verify determine_shard_count and partition_competencies_into_shards enforce max 2 competencies per shard."""
    def make_comps(n: int):
        return [{"id": f"C-{i:02d}", "name": f"Comp {i}", "type": "concept"} for i in range(1, n + 1)]

    # Case 1: 16 competencies
    comps16 = make_comps(16)
    k16 = determine_shard_count(comps16, max_comps_per_shard=2)
    assert k16 == 8, f"Expected 8 shards for 16 competencies, got {k16}"
    shards16 = partition_competencies_into_shards(comps16, k16)
    assert len(shards16) == 8
    assert all(len(s["competency_ids"]) == 2 for s in shards16)
    flat_ids16 = [cid for s in shards16 for cid in s["competency_ids"]]
    assert flat_ids16 == [c["id"] for c in comps16]

    # Case 2: 17 competencies (odd)
    comps17 = make_comps(17)
    k17 = determine_shard_count(comps17, max_comps_per_shard=2)
    assert k17 == 9, f"Expected 9 shards for 17 competencies, got {k17}"
    shards17 = partition_competencies_into_shards(comps17, k17)
    assert len(shards17) == 9
    counts17 = [len(s["competency_ids"]) for s in shards17]
    assert counts17 == [2] * 8 + [1]
    assert all(c <= 2 for c in counts17)
    flat_ids17 = [cid for s in shards17 for cid in s["competency_ids"]]
    assert flat_ids17 == [c["id"] for c in comps17]

    # Case 3: 3 competencies
    comps3 = make_comps(3)
    k3 = determine_shard_count(comps3, max_comps_per_shard=2)
    assert k3 == 2, f"Expected 2 shards for 3 competencies, got {k3}"
    shards3 = partition_competencies_into_shards(comps3, k3)
    assert len(shards3) == 2
    counts3 = [len(s["competency_ids"]) for s in shards3]
    assert counts3 == [2, 1]
    assert all(c <= 2 for c in counts3)
    flat_ids3 = [cid for s in shards3 for cid in s["competency_ids"]]
    assert flat_ids3 == [c["id"] for c in comps3]

    # Case 4: 1 competency
    comps1 = make_comps(1)
    k1 = determine_shard_count(comps1, max_comps_per_shard=2)
    assert k1 == 1, f"Expected 1 shard for 1 competency, got {k1}"
    shards1 = partition_competencies_into_shards(comps1, k1)
    assert len(shards1) == 1
    assert len(shards1[0]["competency_ids"]) == 1
    assert shards1[0]["competency_ids"] == ["C-01"]


def test_shard_default_amortized_v32():
    """Verify that determine_shard_count uses v3.22 adaptive formula clamp(ceil(N/8), 2, 6)."""
    comps16 = [{"id": f"C-{i:02d}", "name": f"Comp {i}", "type": "concept"} for i in range(1, 17)]
    k16 = determine_shard_count(comps16)
    assert k16 == 8, f"Expected 8 shards for 16 competencies under v3.22 (2 comps/shard), got {k16}"
    shards16 = partition_competencies_into_shards(comps16, k16)
    assert len(shards16) == 8
    assert all(len(s["competency_ids"]) <= 2 for s in shards16)


def test_examples_templates_strict_validation():
    """Execute check_templates.py in strict=True mode against examples/edo/templates and examples/edp/templates with 0 errors."""
    edo_dir = SKILL_DIR / "examples" / "edo"
    edp_dir = SKILL_DIR / "examples" / "edp"

    valid_edo, errs_edo = check_templates_file_or_dir(
        target_path=edo_dir / "templates",
        cta_path=edo_dir / "cta.json",
        num_dry_run_seeds=15,
        strict=True,
    )
    assert valid_edo, f"EDO templates failed in strict=True mode: {errs_edo}"
    assert len(errs_edo) == 0

    valid_edp, errs_edp = check_templates_file_or_dir(
        target_path=edp_dir / "templates",
        cta_path=edp_dir / "cta.json",
        num_dry_run_seeds=15,
        strict=True,
    )
    assert valid_edp, f"EDP templates failed in strict=True mode: {errs_edp}"
    assert len(errs_edp) == 0

