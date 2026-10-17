"""Comprehensive integration test suite for pipeline optimizations.

Tests:
1. Ingest patch consolidation & CTA sequential ordering schema
2. Template TPL-VAR enforcement, stem_variants, and diversity gate
3. Self-contained shards with embedded DSL & canonical blind judge normalization
4. Platform frontend build validation & component keyboard hooks
"""

import json
import os
import sys
import tempfile
from pathlib import Path
import pytest
import jsonschema

SKILL_DIR = Path(__file__).parent.parent / ".agents" / "skills" / "content-to-course"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from ingest import ingest_course
from plan_shards import plan_shards
from engine.assemble import assemble_question
from engine.diversity import evaluate_competency_diversity
from check_templates import check_single_template
from judge import compare_judge_responses, generate_judge_batch


# ==============================================================================
# 1. INGEST & CTA SEQUENTIAL ORDER TESTS
# ==============================================================================

def test_ingest_course_document_ordering(tmp_path):
    """Verify that ingest_course discovers and orders files naturally into pre_cta_manifest.json."""
    try:
        import pymupdf
    except ImportError:
        import fitz as pymupdf

    in_dir = tmp_path / "inputs"
    in_dir.mkdir(parents=True)
    for fname in ["lecture10.pdf", "lecture2.pdf", "lecture1.pdf"]:
        doc = pymupdf.open()
        doc.new_page()
        doc.save(str(in_dir / fname))
        doc.close()

    work_dir = tmp_path / "work"
    manifest = ingest_course(in_dir, work_dir, course_id="test_order")
    assert manifest["total_files"] == 3
    docs = [f["doc"] for f in manifest["files"]]
    assert docs == ["lecture1.pdf", "lecture2.pdf", "lecture10.pdf"]
    subpart_docs = [s["doc"] for s in manifest["subparts"]]
    assert subpart_docs == ["lecture1.pdf", "lecture2.pdf", "lecture10.pdf"]


def test_cta_schema_supports_session_and_unit_index():
    """Verify that cta.schema.json validates competencies with session and unit_index."""
    schema_path = SKILL_DIR / "schemas" / "cta.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    jsonschema.Draft7Validator.check_schema(schema)

    sample_cta = {
        "course_id": "test_course",
        "title": "Test Course",
        "macro_competency": "Macro competencia de prueba para validación de esquema con sesiones.",
        "competencies": [
            {
                "id": "H-01",
                "type": "fact",
                "name": "Definir función de producción neoclásica",
                "description_latex": "La función agregada $Q = F(K, L)$ es homogénea de grado 1.",
                "bloom": "Remember",
                "prerequisites": [],
                "session": "Sesión 1: Fundamentos",
                "unit_index": 1,
                "distractors": [
                    {
                        "id": "D-H01-01",
                        "name": "Confusión conceptual",
                        "wrong_belief": "Creer que es homogénea de grado 0",
                        "correct_belief": "Es homogénea de grado 1",
                        "omitted_step": None,
                        "trigger": "Pregunta de grado de homogeneidad",
                        "manifestation": "Grado 0",
                        "error_type": "conceptual_swap",
                        "severity": "medium",
                        "origin": "source",
                        "evidence": {"doc": "doc1.pdf", "page": 1},
                        "remediation_hint": "Recuerda que la homogeneidad lineal implica grado 1."
                    }
                ]
            }
        ]
    }
    jsonschema.validate(instance=sample_cta, schema=schema)


# ==============================================================================
# 2. TEMPLATE TPL-VAR, STEM_VARIANTS & DIVERSITY TESTS
# ==============================================================================

def test_tpl_var_rejects_empty_vars():
    """Verify that check_single_template rejects templates generating empty vars."""
    cta_path = SKILL_DIR.parent.parent.parent / "courses" / "solow_model" / "work" / "cta.json"
    if not cta_path.exists():
        pytest.skip("Solow CTA not found")

    bad_template = {
        "id": "T-BAD-01",
        "competency_id": "Hab-01",
        "interaction_type": "multiple_choice_7",
        "stem": "¿Cuál es la tasa de ahorro?",
        "options": {
            "opt_a": "0.20",
            "opt_b": "0.30",
            "opt_c": "0.40",
            "opt_d": "0.50",
            "opt_e": "0.60",
            "opt_f": "0.70",
            "opt_g": "0.80"
        },
        "correct_option": "opt_a",
        "hints": ["Pista 1", "Pista 2", "Pista 3"],
        "detailed_solution": "Solución fija",
        "generate_py": (
            "def generate(rng):\n"
            "    return {'vars': {}, 'correct': 'opt_a', 'distractors': []}\n"
        )
    }

    errors = check_single_template(
        template=bad_template,
        competency_id="Hab-01",
        declared_distractor_ids=set(),
        cta_distractors_map={},
        num_dry_run_seeds=50,
    )
    assert any("TPL-VAR" in err for err in errors), f"Expected TPL-VAR error, got {errors}"


def test_stem_variants_selection_and_diversity():
    """Verify that stem_variants are deterministically selected and produce diverse stems."""
    template_with_variants = {
        "id": "T-VAR-01",
        "competency_id": "Hab-01",
        "interaction_type": "fill_in_the_blank",
        "stem": "Forma base {val}",
        "stem_variants": [
            "Considere un modelo con parámetro k={val}. Calcule el producto.",
            "Dado el nivel de capital k={val}, determine el producto por trabajador.",
            "Suponga que la economía se encuentra en k={val}. ¿Cuál es la producción?"
        ],
        "hints": ["Pista 1", "Pista 2", "Pista 3"],
        "detailed_solution": "El producto es {val}.",
        "generate_py": (
            "def generate(rng):\n"
            "    v = rng.randint(10, 100)\n"
            "    return {'vars': {'val': v}, 'correct': v, 'equivalents': [str(v)]}\n"
        )
    }

    # Assemble instances across different seeds
    instances = []
    for seed in [1, 2, 3, 4, 5]:
        gen_result = {"vars": {"val": seed * 10}, "correct": seed * 10}
        inst = assemble_question(
            template=template_with_variants,
            gen_result=gen_result,
            competency_id="Hab-01",
            question_index=seed,
            seed=seed,
        )
        instances.append(inst)

    stems = [inst["stem"] for inst in instances]
    unique_stems = set(stems)
    assert len(unique_stems) >= 3, f"Expected varied stems, got: {stems}"


# ==============================================================================
# 3. SELF-CONTAINED SHARDS & BLIND JUDGE NORMALIZATION TESTS
# ==============================================================================

def test_plan_shards_dsl_reference_and_k_cap(tmp_path):
    """Verify that plan_shards embeds DSL reference and supports up to K=8 shards."""
    cta_source = SKILL_DIR.parent.parent.parent / "courses" / "solow_model" / "work" / "cta.json"
    if not cta_source.exists():
        pytest.skip("Solow CTA not found")

    res = plan_shards(cta_path=cta_source, output_dir=tmp_path / "shards", k=8)
    assert res["total_shards"] <= 8

    # Inspect shard 1
    shard_1_file = Path(res["shards"][0]["shard_file"])
    data = json.loads(shard_1_file.read_text(encoding="utf-8"))
    assert "dsl_reference" in data, "Shard must contain embedded dsl_reference for self-containment"
    dsl = data["dsl_reference"]
    assert "canonical_examples" in dsl
    assert "multiple_choice_7_options" in dsl["canonical_examples"]


def test_judge_canonical_option_comparison():
    """Verify that judge compares options canonically (e.g. 'B' matches 'opt_b')."""
    gt = {
        "item_1": {
            "interaction_type": "multiple_choice_7_options",
            "correct_letter": "B",
            "correct_content": "42"
        },
        "item_2": {
            "interaction_type": "fill_in_the_blank",
            "correct_value": "12.50",
            "tolerance": 0.01
        }
    }

    # Case 1: judge gave "opt_b"
    res1 = compare_judge_responses({"item_1": "opt_b", "item_2": "12.5"}, gt)
    assert res1["agreement_rate"] == 1.0

    # Case 2: judge gave "OPT_B" and float
    res2 = compare_judge_responses({"item_1": "OPT_B", "item_2": "12.500"}, gt)
    assert res2["agreement_rate"] == 1.0

    # Case 3: judge gave "B"
    res3 = compare_judge_responses({"item_1": "B", "item_2": "12.5"}, gt)
    assert res3["agreement_rate"] == 1.0

    # Case 4: mismatch
    res4 = compare_judge_responses({"item_1": "A", "item_2": "99.9"}, gt)
    assert res4["agreement_rate"] == 0.0
