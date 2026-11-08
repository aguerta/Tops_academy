"""Comprehensive integration test suite for pipeline optimizations.

Tests:
1. Ingest patch consolidation & CTA sequential ordering schema
2. Template TPL-VAR enforcement, stem_variants, and diversity gate
3. Self-contained shards with embedded DSL & canonical blind judge normalization
4. Platform frontend build validation & component keyboard hooks
"""

import hashlib
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
from judge import compare_judge_responses, generate_judge_batch, resolve_neuro_symbolic_verdict
from course_publisher import CoursePublisher, check_prerequisites_dag, are_competencies_duplicate, build_specific_error_report
from engine.interstage_schemas import (
    ArtifactCertificate,
    CompileAttemptRecord,
    RejectionSpec,
    write_certificate,
    verify_certificate,
)
from validator.models import ValidationResult


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
    cta_path = SKILL_DIR / "courses" / "solow_model" / "work" / "cta.json"
    if not cta_path.exists():
        alt_cta = SKILL_DIR.parent.parent / "courses" / "solow_growth_model.json"
        if alt_cta.exists():
            cta_path = alt_cta
        else:
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
    cta_source = SKILL_DIR / "courses" / "solow_model" / "work" / "cta.json"
    if not cta_source.exists():
        alt_cta = SKILL_DIR.parent.parent / "courses" / "solow_growth_model.json"
        if alt_cta.exists():
            cta_source = alt_cta
        else:
            pytest.skip("Solow CTA not found")

    (tmp_path / "pre_cta_manifest.json").write_text(json.dumps({
        "course_id": "solow_model",
        "cta_mode": "direct",
        "documents": [{"name": "solow1956.pdf", "path": "content/Solow_model/solow1956.pdf", "total_pages": 20}],
    }), encoding="utf-8")

    res = plan_shards(cta_path=cta_source, output_dir=tmp_path / "shards", k=8)
    assert res["total_shards"] <= 8

    # Inspect shard 1 (supports v3 pre_shard_manifest schema and legacy shard_file)
    s0 = res["shards"][0]
    if "shard_file" in s0:
        shard_1_file = Path(s0["shard_file"])
        data = json.loads(shard_1_file.read_text(encoding="utf-8"))
        assert "dsl_reference" in data
    else:
        assert "shard_data_path" in s0
        assert "competency_ids" in s0
        assert (tmp_path / "shards" / "pre_shard_manifest.json").is_file()


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


def test_judge_sampling_three_seeds_full_template_coverage(tmp_path):
    """Verify generate_judge_batch samples 3 seeds across 100% of templates by default."""
    templates = []
    for i in range(1, 5):
        cid = "C-01" if i <= 2 else "C-02"
        templates.append({
            "id": f"T-0{i}",
            "competency_id": cid,
            "interaction_type": "fill_in_the_blank",
            "stem": f"Calculate parameter value {{val}} for template {i}",
            "hints": ["Hint 1", "Hint 2", "Hint 3"],
            "detailed_solution": "Solution is {val}",
            "generate_py": (
                "def generate(rng):\n"
                "    v = rng.randint(10, 100)\n"
                "    return {'vars': {'val': v}, 'correct': v, 'equivalents': [str(v)]}\n"
            ),
        })

    tpl_file = tmp_path / "templates.json"
    tpl_file.write_text(json.dumps(templates), encoding="utf-8")

    batch_path, gt_path = generate_judge_batch(tpl_file, work_dir=tmp_path)
    batch = json.loads(batch_path.read_text(encoding="utf-8"))
    gt = json.loads(gt_path.read_text(encoding="utf-8"))

    # 4 templates * 3 seeds (101, 202, 303) = 12 items
    assert len(batch) == 12
    assert len(gt) == 12

    covered_templates = {item["template_id"] for item in batch}
    assert covered_templates == {"T-01", "T-02", "T-03", "T-04"}

    for item in batch:
        assert "template_id" in item
        assert "competency_id" in item
        assert item["template_id"] in ("T-01", "T-02", "T-03", "T-04")
        assert item["competency_id"] in ("C-01", "C-02")


def test_judge_zero_tolerance_rejection_empty_or_incomplete(tmp_path):
    """Verify zero tolerance when judge responses are empty or incomplete."""
    # Case A: total == 0
    res_empty = compare_judge_responses(responses={}, ground_truth={})
    assert res_empty["total_items"] == 0
    assert res_empty["passed"] is False

    # Case B: incomplete items
    gt = {
        "item_1": {"interaction_type": "fill_in_the_blank", "correct_value": 10.0, "template_id": "T-01", "competency_id": "C-01"},
        "item_2": {"interaction_type": "fill_in_the_blank", "correct_value": 20.0, "template_id": "T-02", "competency_id": "C-02"},
    }
    # Only item_1 answered
    res_incomplete = compare_judge_responses(responses={"item_1": 10.0}, ground_truth=gt)
    assert res_incomplete["total_items"] == 2
    assert res_incomplete["passed"] is False


def test_judge_zero_tolerance_single_template_disagreement():
    """Verify that a single disagreement in any template marks passed=False and records failed_templates."""
    gt = {
        "item_1": {"interaction_type": "multiple_choice_7_options", "correct_letter": "A", "template_id": "T-01", "competency_id": "C-01"},
        "item_2": {"interaction_type": "multiple_choice_7_options", "correct_letter": "B", "template_id": "T-01", "competency_id": "C-01"},
        "item_3": {"interaction_type": "multiple_choice_7_options", "correct_letter": "C", "template_id": "T-02", "competency_id": "C-02"},
        "item_4": {"interaction_type": "multiple_choice_7_options", "correct_letter": "D", "template_id": "T-02", "competency_id": "C-02"},
    }
    # Judge agrees on item 1, 2, 3, but fails item 4 in T-02
    responses = {
        "item_1": "A",
        "item_2": "B",
        "item_3": "C",
        "item_4": "E",
    }
    res = compare_judge_responses(responses=responses, ground_truth=gt)
    assert res["passed"] is False
    assert "T-02" in res["failed_templates"]
    assert "C-02" in res["failed_competencies"]
    assert "T-01" not in res["failed_templates"]


def test_course_publisher_append_paraphrase_detection_and_prereqs_remap(tmp_path, monkeypatch):
    """Verify that append merges real paraphrases (Jaccard 0.40-0.54) and remaps prerequisites cleanly."""
    courses_dir = tmp_path / "courses"
    courses_dir.mkdir(parents=True)

    base_course = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "course_id": "stats_math",
        "course_title": "Mathematical Statistics",
        "competencies": [
            {
                "id": "C-01",
                "name": "Estimador BLUE y teorema de Gauss-Markov en $Y = X\\beta + u$",
                "description": "Demostración de insesgadez y varianza mínima para estimadores lineales en modelos con $\\beta$.",
                "category": "Concept",
                "type": "Concept",
                "level": "Analyze",
                "mastery_target": 100,
                "prerequisites": [],
                "distractors": [{"id": "D-C01-01", "name": "D1"}],
            }
        ],
        "questions": [
            {
                "id": "Q-C01-01",
                "competency_id": "C-01",
                "stem": "Determine the property of the OLS estimator.",
                "correct_answer": "It is BLUE under classical assumptions.",
                "options": [{"id": "A", "content": "It is BLUE under classical assumptions.", "is_correct": True}],
            }
        ],
    }
    base_file = courses_dir / "stats_math.json"
    base_file.write_text(json.dumps(base_course, indent=2), encoding="utf-8")

    # Incoming delta batch has:
    # C-99: Real paraphrase of C-01 with shared math symbol \beta and shared conceptual stems
    # C-02: New competency with prerequisite referencing C-99
    delta_batch = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "course_id": "stats_math",
        "course_title": "Mathematical Statistics",
        "competencies": [
            {
                "id": "C-99",
                "name": "Teorema de Gauss-Markov y propiedad BLUE con $y = X\\beta + \\varepsilon$",
                "description": "Prueba formal de varianza mínima e insesgadez en modelos lineales para $\\beta$.",
                "category": "Concept",
                "type": "Concept",
                "level": "Analyze",
                "mastery_target": 100,
                "prerequisites": [],
                "distractors": [{"id": "D-C99-01", "name": "D1"}],
            },
            {
                "id": "C-02",
                "name": "Contraste de hipótesis lineal para $\\beta$",
                "description": "Prueba de significancia individual mediante estadístico t.",
                "category": "Skill",
                "type": "Skill",
                "level": "Evaluate",
                "mastery_target": 100,
                "prerequisites": ["C-99"],
                "distractors": [{"id": "D-C02-01", "name": "D1"}],
            },
        ],
        "questions": [
            {
                "id": "Q-C99-01",
                "competency_id": "C-99",
                "stem": "Question about BLUE property.",
                "correct_answer": "Valid ans",
                "options": [{"id": "A", "content": "Valid ans", "is_correct": True}],
            },
            {
                "id": "Q-C02-01",
                "competency_id": "C-02",
                "stem": "Question about hypothesis test.",
                "correct_answer": "Valid ans 2",
                "options": [{"id": "A", "content": "Valid ans 2", "is_correct": True}],
            },
        ],
    }

    publisher = CoursePublisher(courses_dir=courses_dir)
    publisher._run_cli_validator = lambda p, strict=True: True
    monkeypatch.setattr(
        "course_publisher.validate_course_content",
        lambda raw, file_path=None, strict=False: ValidationResult(is_valid=True, file_path=file_path, errors=[]),
    )

    res = publisher.publish(delta_batch, append=True, strict=False)
    assert res.success is True

    # Check merged course on disk
    merged_data = json.loads(base_file.read_text(encoding="utf-8"))
    merged_c_ids = [c["id"] for c in merged_data["competencies"]]

    # C-99 was detected as duplicate of C-01 and merged!
    assert "C-01" in merged_c_ids
    assert "C-99" not in merged_c_ids
    assert "C-02" in merged_c_ids

    # Prerequisites of C-02 must be remapped from C-99 to C-01!
    c02 = next(c for c in merged_data["competencies"] if c["id"] == "C-02")
    assert c02["prerequisites"] == ["C-01"]

    # DAG check must pass without errors
    dag_errors = check_prerequisites_dag(merged_data["competencies"])
    assert len(dag_errors) == 0

    # Questions for C-99 must be remapped to C-01
    q_c01 = [q for q in merged_data["questions"] if q["competency_id"] == "C-01"]
    assert len(q_c01) == 2


def test_matiz3_paraphrase_composite_detection_adversary():
    """Verify Matiz 3: Sem-9 paraphrase competencies with Jaccard ~0.44 and shared LaTeX math are merged,
    while genuinely distinct competencies from the same topic are NOT merged."""
    comp_a = {
        "id": "C-01",
        "name": "Estimador por mínimos cuadrados y varianza formal con $\\hat{\\beta}$ y residuo $\\varepsilon$",
        "description": "Deducción de insesgadez y cálculo algebraico de varianza para $\\hat{\\beta}$ considerando error $\\varepsilon$.",
    }
    comp_b = {
        "id": "C-02",
        "name": "Propiedades de mínimos cuadrados y matriz de varianzas con $\\hat{\\beta}$ y perturbación $\\varepsilon$",
        "description": "Demostración analítica de varianza mínima e insesgadez para el estimador $\\hat{\\beta}$ con $\\varepsilon$.",
    }

    is_dup = are_competencies_duplicate(comp_b, comp_a)
    assert is_dup is True, "Expected paraphrase competencies sharing math symbols and content stems to merge"

    comp_c = {
        "id": "C-03",
        "name": "Inferencia y contraste de hipótesis lineal $R\\beta = r$ con estadístico F",
        "description": "Distribución asintótica y regiones de confianza para combinaciones lineales de parámetros.",
    }
    is_distinct = are_competencies_duplicate(comp_c, comp_a)
    assert is_distinct is False, "Expected distinct topic competency to NOT merge with OLS estimation competency"


def test_append_prerequisites_remap_avoids_self_loop_and_duplicates(tmp_path, monkeypatch):
    """Verify append remapping drops self-loops (cid in prerequisites) and eliminates duplicate prerequisites."""
    courses_dir = tmp_path / "courses"
    courses_dir.mkdir(parents=True)

    base_course = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "course_id": "math_base",
        "course_title": "Base Course",
        "competencies": [
            {
                "id": "C-01",
                "name": "Concepto Base 1",
                "description": "Fundamento inicial.",
                "prerequisites": [],
            }
        ],
        "questions": [
            {
                "id": "Q-01",
                "competency_id": "C-01",
                "stem": "Stem 1",
                "correct_answer": "Ans",
                "options": [{"id": "A", "content": "Ans", "is_correct": True}],
            }
        ],
    }
    base_file = courses_dir / "math_base.json"
    base_file.write_text(json.dumps(base_course, indent=2), encoding="utf-8")

    delta = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "course_id": "math_base",
        "course_title": "Base Course",
        "competencies": [
            {
                "id": "C-99",
                "name": "Concepto Base 1",
                "description": "Fundamento inicial duplicado.",
                "prerequisites": [],
            },
            {
                "id": "C-02",
                "name": "Concepto Habilitado 2",
                "description": "Dependencia compuesta.",
                "prerequisites": ["C-99", "C-01"],
            },
            {
                "id": "C-03",
                "name": "Concepto Habilitado 3",
                "description": "Dependencia con auto-bucle.",
                "prerequisites": ["C-03", "C-01"],
            },
        ],
        "questions": [
            {
                "id": "Q-C02-01",
                "competency_id": "C-02",
                "stem": "Stem for C-02",
                "correct_answer": "Ans",
                "options": [{"id": "A", "content": "Ans", "is_correct": True}],
            },
            {
                "id": "Q-C03-01",
                "competency_id": "C-03",
                "stem": "Stem for C-03",
                "correct_answer": "Ans",
                "options": [{"id": "A", "content": "Ans", "is_correct": True}],
            },
        ],
    }

    publisher = CoursePublisher(courses_dir=courses_dir)
    publisher._run_cli_validator = lambda p, strict=True: True
    monkeypatch.setattr(
        "course_publisher.validate_course_content",
        lambda raw, file_path=None, strict=False: ValidationResult(is_valid=True, file_path=file_path, errors=[]),
    )

    res = publisher.publish(delta, append=True, strict=False)
    assert res.success is True

    merged = json.loads(base_file.read_text(encoding="utf-8"))
    c02 = next(c for c in merged["competencies"] if c["id"] == "C-02")
    c03 = next(c for c in merged["competencies"] if c["id"] == "C-03")

    assert c02["prerequisites"] == ["C-01"]
    assert "C-03" not in c03["prerequisites"]
    assert c03["prerequisites"] == ["C-01"]

    dag_errs = check_prerequisites_dag(merged["competencies"])
    assert len(dag_errs) == 0


# ==============================================================================
# 5. STREAM 1E: INTERSTAGE SCHEMAS, JUDGE DOMINANCE, & PUBLISHER TESTS
# ==============================================================================

def test_artifact_certificate_tamper_detection(tmp_path):
    """Verify ArtifactCertificate SHA-256 seal and source tamper detection."""
    source_file = tmp_path / "course.json"
    source_content = b'{"course_id": "math101", "valid": true}'
    source_file.write_bytes(source_content)
    source_sha = hashlib.sha256(source_content).hexdigest()

    cert_path = tmp_path / "work" / "publish.cert.json"
    cert = ArtifactCertificate(
        stage="publish",
        artifact_id="publish_math101",
        source_sha256=source_sha,
        contract_version=2,
        passed_50_seeds=True,
    )
    written_path = write_certificate(cert_path, cert)
    assert written_path.is_file()

    # Valid certificate check
    assert verify_certificate(written_path, expected_source_bytes=source_content) is True
    assert verify_certificate(written_path, expected_source_path=source_file) is True

    # Tampered source content -> FAILS
    tampered_bytes = b'{"course_id": "math101", "tampered": true}'
    assert verify_certificate(written_path, expected_source_bytes=tampered_bytes) is False

    # Tampered certificate content (hash mismatch) -> FAILS
    cert_data = json.loads(written_path.read_text(encoding="utf-8"))
    cert_data["contract_version"] = 999
    written_path.write_text(json.dumps(cert_data), encoding="utf-8")
    assert verify_certificate(written_path, expected_source_bytes=source_content) is False


def test_rejection_spec_dual_keys_and_status_normalization(tmp_path):
    """Verify RejectionSpec normalizes status to REJECTED and synchronizes dual keys bidirectionally."""
    # Case 1: Input with lowercase status, only affected_shards, only groups
    raw_spec = {
        "status": "failed",
        "course_id": "test_sync",
        "affected_shards": ["shard_02", "shard_01"],
        "groups": {"R-20": [{"issue": "syntax"}]},
    }
    spec = RejectionSpec.from_dict(raw_spec)
    dumped = spec.to_dict()

    assert dumped["status"] == "REJECTED"
    assert dumped["failing_shards"] == ["shard_01", "shard_02"]
    assert dumped["affected_shards"] == ["shard_01", "shard_02"]
    assert "R-20" in dumped["grouped_by_rule"]
    assert dumped["grouped_by_rule"] == dumped["groups"]

    # Case 2: Round-trip file persistence
    out_file = tmp_path / "publish_rejection_spec.json"
    spec.write_json(out_file)
    loaded = RejectionSpec.from_file(out_file)
    assert loaded.status == "REJECTED"
    assert loaded.failing_shards == ["shard_01", "shard_02"]
    assert loaded.affected_shards == ["shard_01", "shard_02"]


def test_judge_canonical_one_seed_default_for_verified_templates(tmp_path):
    """Verify generate_judge_batch uses 1 verified canonical seed by default when verifier_code is present."""
    verified_template = {
        "id": "T-VERIF-01",
        "competency_id": "C-01",
        "interaction_type": "fill_in_the_blank",
        "stem": "Determine the value of @x@.",
        "hints": ["Hint 1", "Hint 2", "Hint 3"],
        "detailed_solution": "Solution is @x@.",
        "generate_py": (
            "def generate(rng):\n"
            "    x = rng.randint(10, 50)\n"
            "    return {'vars': {'x': x}, 'correct': x, 'equivalents': [str(x)]}\n"
        ),
        "verifier_code": (
            "def verify(res):\n"
            "    v = res.get('vars', {}).get('x')\n"
            "    return v is not None and v == res.get('correct')\n"
        ),
    }

    tpl_file = tmp_path / "verified_templates.json"
    tpl_file.write_text(json.dumps([verified_template]), encoding="utf-8")

    batch_path, gt_path = generate_judge_batch(tpl_file, work_dir=tmp_path)
    batch = json.loads(batch_path.read_text(encoding="utf-8"))
    gt = json.loads(gt_path.read_text(encoding="utf-8"))

    # Exactly 1 item sampled because template has non-empty verifier_code!
    assert len(batch) == 1
    assert len(gt) == 1
    first_item = list(gt.values())[0]
    assert first_item["kernel_verified"] is True
    assert first_item["kernel_refuted"] is False


def test_judge_kernel_refutation_on_broken_template(tmp_path):
    """Verify that templates failing verification across all candidate seeds are marked kernel_refuted = True."""
    broken_template = {
        "id": "T-BROKEN-01",
        "competency_id": "C-FAIL",
        "interaction_type": "fill_in_the_blank",
        "stem": "Broken stem @x@.",
        "hints": ["Hint 1", "Hint 2", "Hint 3"],
        "detailed_solution": "Sol",
        "generate_py": "def generate(rng): return {'vars': {'x': 1}, 'correct': 1}\n",
        # Verifier strictly returns False on every seed!
        "verifier_code": "def verify(res): return False\n",
    }

    tpl_file = tmp_path / "broken_templates.json"
    tpl_file.write_text(json.dumps([broken_template]), encoding="utf-8")

    batch_path, gt_path = generate_judge_batch(tpl_file, work_dir=tmp_path)
    batch = json.loads(batch_path.read_text(encoding="utf-8"))
    gt = json.loads(gt_path.read_text(encoding="utf-8"))

    # Not emitted to blind judge batch (zero token waste!)
    assert len(batch) == 0
    # Recorded in ground truth as refuted
    assert len(gt) == 1
    gt_record = list(gt.values())[0]
    assert gt_record["kernel_refuted"] is True
    assert gt_record["kernel_verified"] is False

    # Comparison fails immediately
    rep = compare_judge_responses(responses={}, ground_truth=gt, work_dir=tmp_path)
    assert rep["passed"] is False
    assert "T-BROKEN-01" in rep["failed_templates"]


def test_judge_resolve_neuro_symbolic_verdict_alpha_kernel_dominance():
    """Verify Bayesian dominance (alpha_kernel = 0) in resolve_neuro_symbolic_verdict."""
    # 1. Deterministic kernel refuted -> Unconditionally FAIL even if LLM voted PASS
    res1 = resolve_neuro_symbolic_verdict(
        kernel_verified=False,
        kernel_refuted=True,
        llm_verdict="PASS",
    )
    assert res1["passed"] is False
    assert res1["verdict"] == "FAIL"

    # 2. Kernel verified constructive proof overrides pure math calculation error
    res2 = resolve_neuro_symbolic_verdict(
        kernel_verified=True,
        kernel_refuted=False,
        llm_verdict="FAIL",
        failure_category="math_error",
        failure_reasons=["Numerical rounding mismatch at 4th decimal place"],
    )
    assert res2["passed"] is True
    assert res2["verdict"] == "PASS"
    assert res2["kernel_override"] is True

    # 3. Kernel verified BUT LLM flags epistemic insufficiency / missing definition -> BLOCKS (FAIL)
    res3 = resolve_neuro_symbolic_verdict(
        kernel_verified=True,
        kernel_refuted=False,
        llm_verdict="FAIL",
        failure_category="epistemic_insufficiency",
        failure_reasons=["Stem does not define parameter theta prior to calculation"],
    )
    assert res3["passed"] is False
    assert res3["verdict"] == "FAIL"
    assert res3["kernel_override"] is False


def test_course_publisher_rejection_spec_and_publish_cert(tmp_path, monkeypatch):
    """Verify CoursePublisher writes publish_rejection_spec.json on gate failure and emits publish.cert.json on success."""
    courses_dir = tmp_path / "courses"
    work_dir = tmp_path / "work"
    work_dir.mkdir(parents=True)

    # A. Test Rejection Spec Emission via build_specific_error_report
    course_payload = {
        "course_id": "test_gate_fail",
        "title": "Gate Fail Course",
        "competencies": [{"id": "C-01", "name": "Concept 1"}],
        "questions": [{"id": "Q-01", "competency_id": "C-01", "stem": "Test stem"}],
    }
    audit_report = {
        "all_issues": [
            {
                "linter": "anti_gaming_psychometric_linter",
                "severity": "critical",
                "item_id": "Q-01",
                "competency_id": "C-01",
                "message": "Opción correcta con relleno artificial de longitud.",
            }
        ]
    }
    structured = build_specific_error_report(
        parsed=course_payload,
        audit_report=audit_report,
        gate_failures=["Length-padded options detected"],
        work_dir=work_dir,
    )
    spec_file = work_dir / "publish_rejection_spec.json"
    assert spec_file.is_file()
    spec_data = json.loads(spec_file.read_text(encoding="utf-8"))
    assert spec_data["status"] == "REJECTED"
    assert "failing_shards" in spec_data
    assert "affected_shards" in spec_data
    assert "grouped_by_rule" in spec_data
    assert "groups" in spec_data

    # B. Test Successful Publication Stamping & Certificate Emission
    publisher = CoursePublisher(courses_dir=courses_dir)
    publisher._run_cli_validator = lambda p, strict=True: True
    monkeypatch.setattr(
        "course_publisher.validate_course_content",
        lambda raw, file_path=None, strict=False: ValidationResult(is_valid=True, file_path=file_path, errors=[]),
    )
    monkeypatch.setattr(
        "course_publisher._load_run_full_audit",
        lambda project_root=None: lambda data: {"mpri_score": 95.0, "hard_penalties": [], "all_issues": []},
    )

    valid_payload = {
        "course_id": "cert_course",
        "course_title": "Certified Course",
        "competencies": [{"id": "C-01", "name": "C1", "category": "Concept"}],
        "questions": [{"id": "Q-01", "competency_id": "C-01", "stem": "Stem", "interaction_type": "multiple_choice_7_options"}],
    }
    res = publisher.publish(valid_payload, work_dir=work_dir, strict=False)
    assert res.success is True

    # Verify stamped contract_version and min_archetypes
    pub_file = courses_dir / "cert_course.json"
    pub_data = json.loads(pub_file.read_text(encoding="utf-8"))
    assert pub_data["contract_version"] == 2
    assert pub_data["min_archetypes"] >= 4

    # Verify publish.cert.json emission and cryptographic validity
    cert_file = work_dir / "publish.cert.json"
    assert cert_file.is_file()
    assert verify_certificate(cert_file, expected_source_path=pub_file) is True


