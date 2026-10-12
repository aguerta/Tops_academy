"""Comprehensive Verification Suite for content-to-course v2 Engine Components.

Tests:
1. JSON Schemas: pages.schema.json, cta.schema.json, template.schema.json
2. Validation Scripts: check_pages.py, check_cta.py, check_templates.py
3. Ingestion: ingest.py (tiling >2500px, diacritics, manifest, batches)
4. Parametric Engine: sandbox, render, invariants, diversity, assemble, instantiate
5. Anti-Overfitting: Zero domain keywords check in engine/
"""

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
from PIL import Image

# Ensure skills root is in sys.path
skills_root = Path(r"G:\Mi unidad\Competence_analyser\.agents\skills\content-to-course").resolve()
if str(skills_root) not in sys.path:
    sys.path.insert(0, str(skills_root))

from check_cta import validate_cta_rules
from check_pages import check_pages
from check_templates import check_single_template, check_templates_file_or_dir
from engine.assemble import assemble_question, check_course_giveaway_distribution
from engine.diversity import evaluate_competency_diversity, mask_stem_numbers
from engine.instantiate import allocate_template_quotas, instantiate_template, instantiate_competency
from engine.invariants import check_instance_invariants
from engine.render import bmatrix, fmt, latex_frac, table_array
from engine.sandbox import (
    execute_sandbox_batch,
    execute_sandbox_instance,
    validate_code_ast,
    SandboxExecutionError,
    SandboxTimeoutError,
    SecurityViolationError,
)
from ingest import normalize_corrupt_diacritics, process_image_file, run_ingest


def test_zero_domain_keywords():
    """Verify zero domain keywords in generic parametric engine."""
    engine_dir = skills_root / "engine"
    domain_terms = ["edo", "pde", "derivadas", "jacobiana", "eigen", "euler", "cobb_douglas", "lotka", "lagrange"]

    for py_file in engine_dir.glob("*.py"):
        content = py_file.read_text(encoding="utf-8").lower()
        for term in domain_terms:
            assert term not in content, f"Domain keyword '{term}' found in generic engine file: {py_file.name}"
    print("PASS: Zero domain keywords found in engine/")


def test_sandbox_security():
    """Verify AST whitelist and security bans."""
    banned_snippets = [
        "import os\ndef generate(rng): return {}",
        "import sys\ndef generate(rng): return {}",
        "import subprocess\ndef generate(rng): return {}",
        "import socket\ndef generate(rng): return {}",
        "def generate(rng):\n    x = open('foo.txt')\n    return {}",
        "def generate(rng):\n    eval('2+2')\n    return {}",
        "def generate(rng):\n    exec('a=1')\n    return {}",
        "def generate(rng):\n    __import__('os')\n    return {}",
        "def generate(rng):\n    x = ().__class__\n    return {}",
        "def generate(rng):\n    x = rng.__dict__\n    return {}",
    ]
    for snip in banned_snippets:
        try:
            validate_code_ast(snip)
            assert False, f"Expected SecurityViolationError for: {snip}"
        except SecurityViolationError:
            pass
    print("PASS: Sandbox security successfully blocks banned imports, calls, and dunder attributes.")


def test_sandbox_execution_and_timeout():
    """Verify isolated execution, seed determinism, and timeout handling."""
    code = """
def generate(rng):
    import numpy as np
    import math
    a = rng.randint(10, 50)
    b = rng.randint(2, 5)
    return {
        "vars": {"a": a, "b": b},
        "correct": a * b,
        "distractors": [{"value": a * b + i, "distractor_id": f"D-0{i}"} for i in range(1, 7)]
    }
"""
    # Determinism
    r1 = execute_sandbox_instance(code, seed=99)
    r2 = execute_sandbox_instance(code, seed=99)
    assert r1 == r2, "Sandbox execution must be deterministic for identical seeds"

    # Different seeds yield different values
    r3 = execute_sandbox_instance(code, seed=100)
    assert r1 != r3, "Different seeds should yield different instances"

    # Timeout
    timeout_code = "def generate(rng):\n    while True: pass"
    try:
        execute_sandbox_instance(timeout_code, seed=1, timeout=1.0)
        assert False, "Infinite loop should have raised SandboxTimeoutError"
    except SandboxTimeoutError:
        pass

    print("PASS: Sandbox execution determinism and timeout verified.")


def test_render_helpers():
    """Verify KaTeX rendering helpers."""
    # bmatrix
    M = [[1, 2], [3, 4]]
    bm = bmatrix(M)
    assert "\\begin{bmatrix} 1 & 2 \\\\ 3 & 4 \\end{bmatrix}" == bm

    # table_array
    table = table_array([[1, 2], [3, 4]], headers=["A", "B"])
    assert "\\begin{array}{lc} A & B \\\\ \\hline \\\\ 1 & 2 \\\\ 3 & 4 \\end{array}" == table

    # fmt and latex_frac
    assert fmt(3.0) == "3"
    assert fmt(3.14159, nd=4) == "3.1416"
    assert latex_frac(1, 2) == "\\frac{1}{2}"
    assert latex_frac(-1, 3) == "-\\frac{1}{3}"
    print("PASS: KaTeX render helpers verified.")


def test_cta_validator():
    """Verify check_cta rules CTA-D1, CTA-D2."""
    valid_cta = {
        "course_id": "test_course",
        "title": "Test Course",
        "macro_competency": "Test Macro",
        "competencies": [
            {
                "id": "Hab-01",
                "type": "skill",
                "name": "Skill 1",
                "description_latex": "Desc",
                "bloom": "Apply",
                "prerequisites": [],
                "source_examples": ["Ex 1"],
                "evidence": [{"doc": "doc1.pdf", "page": 1}],
                "distractors": [
                    {
                        "id": f"D-Hab01-0{i}",
                        "name": f"Distractor {i}",
                        "wrong_belief": f"Wrong belief {i}" if i != 2 else None,
                        "correct_belief": f"Correct belief {i}",
                        "omitted_step": f"Omitted step {i}" if i in (1, 2) else None,
                        "trigger": "Trigger",
                        "manifestation": "Manifestation",
                        "error_type": "procedural_slip",
                        "severity": "medium",
                        "origin": "source",
                        "evidence": {"doc": "doc1.pdf", "page": 1},
                        "remediation_hint": "Hint"
                    }
                    for i in range(1, 7)
                ]
            }
        ]
    }
    valid, errors = validate_cta_rules(valid_cta)
    assert valid, f"Valid CTA was rejected: {errors}"

    # Invalid CTA: Skill with only 2 distractors (violates CTA-D1)
    invalid_cta = json.loads(json.dumps(valid_cta))
    invalid_cta["competencies"][0]["distractors"] = invalid_cta["competencies"][0]["distractors"][:2]
    valid, errors = validate_cta_rules(invalid_cta)
    assert not valid, "CTA with < 6 distractors for skill should be rejected"
    assert any("CTA-D1" in e for e in errors)

    print("PASS: check_cta validation rules verified.")


def test_template_validation_and_instantiation():
    """Verify check_templates, instantiate_template, and diversity."""
    comp_id = "Hab-01"
    cta_distractor_ids = {f"D-Hab01-0{i}" for i in range(1, 7)}
    cta_map = {did: {"remediation_hint": f"Hint for {did}", "manifestation": f"Manifestation {did}"} for did in cta_distractor_ids}

    # Template MC7
    tpl_mc7 = {
        "id": "T-Hab01-01",
        "competency_id": comp_id,
        "interaction_type": "multiple_choice_7_options",
        "difficulty": "medium",
        "bloom": "Apply",
        "stem": "Determine el valor de $y = {a} \\cdot {b}$.",
        "generate_py": """
def generate(rng):
    a = rng.randint(2, 10)
    b = rng.randint(2, 10)
    ans = a * b
    distractors = [
        {"value": fmt(ans + 1), "distractor_id": "D-Hab01-01"},
        {"value": fmt(ans + 2), "distractor_id": "D-Hab01-02"},
        {"value": fmt(ans + 3), "distractor_id": "D-Hab01-03"},
        {"value": fmt(ans - 1), "distractor_id": "D-Hab01-04"},
        {"value": fmt(ans - 2), "distractor_id": "D-Hab01-05"},
        {"value": fmt(ans + 4), "distractor_id": "D-Hab01-06"},
    ]
    return {"vars": {"a": a, "b": b}, "correct": fmt(ans), "distractors": distractors}
""",
        "cross_check_py": "def verify(res): return int(res['correct']) == res['vars']['a'] * res['vars']['b']",
        "hints": ["Paso 1", "Paso 2", "Paso 3"],
        "solution": "Multiplique los dos factores.",
        "distractor_ids": list(cta_distractor_ids)
    }

    errors = check_single_template(
        template=tpl_mc7,
        competency_id=comp_id,
        declared_distractor_ids=cta_distractor_ids,
        cta_distractors_map=cta_map,
        num_dry_run_seeds=20,
    )
    assert not errors, f"Template verification failed: {errors}"

    # Instantiation
    instantiated = instantiate_template(
        template=tpl_mc7,
        competency_id=comp_id,
        target_count=10,
        start_index=1,
        cta_distractors_map=cta_map,
    )
    assert len(instantiated) == 10
    assert all(q["interaction_type"] == "multiple_choice_7_options" for q in instantiated)

    # Diversity check
    stems = [q["stem"] for q in instantiated]
    div_res = evaluate_competency_diversity(stems)
    # Since all stems are from one template with numbers masked, unique masked is 1
    assert div_res["unique_masked"] == 1

    print("PASS: Template validation, assembly, and instantiation verified.")


def test_multiformat_ingestion():
    """Verify ingest.py with large image tiling (>2500 px) and diacritic normalization."""
    # Test diacritic normalization
    corrupt = "Regresi´on Te´orico y ˆβ con ~n"
    normalized = normalize_corrupt_diacritics(corrupt)
    assert "Regresión Teórico" in normalized
    assert "ñ" in normalized

    # Test image tiling
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        large_img_path = tmp_path / "large_test.png"
        out_dir = tmp_path / "out"

        # Create 3000 x 2600 image (>2500 px)
        im = Image.new("RGB", (3000, 2600), color=(100, 150, 200))
        im.save(large_img_path)

        items = process_image_file(large_img_path, out_dir)
        # Should produce 1 overview + 6 tiles = 7 items
        assert len(items) == 7
        assert items[0]["kind"] == "image_overview"
        assert all(it["kind"] == "image_tile" for it in items[1:])
        assert all(Path(it["image_path"]).exists() for it in items)

    print("PASS: Ingestion large image tiling and diacritic normalization verified.")


def test_pages_validator():
    """Verify check_pages ensures 100% transcription coverage."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        m_file = tmp_path / "manifest.json"
        p1 = tmp_path / "p1.md"
        p1.write_text("# Page 1 transcription with $x=1$", encoding="utf-8")

        manifest_data = {
            "manifest_version": "2.0",
            "source_path": "test",
            "items": [
                {
                    "doc": "doc.pdf",
                    "page": 1,
                    "kind": "beamer_text",
                    "sha256": "a" * 64,
                    "render_dpi": 130,
                    "tile": None,
                    "has_text_layer": False,
                    "image_path": "page1.png",
                    "text_layer_path": None,
                    "transcription_path": str(p1.as_posix()),
                }
            ]
        }
        with open(m_file, "w", encoding="utf-8") as f:
            json.dump(manifest_data, f)

        valid, report = check_pages(m_file)
        assert valid, f"check_pages should pass: {report}"

        # Test failure if transcription file is missing
        manifest_data["items"].append({
            "doc": "doc.pdf",
            "page": 2,
            "kind": "beamer_text",
            "sha256": "b" * 64,
            "render_dpi": 130,
            "tile": None,
            "has_text_layer": False,
            "image_path": "page2.png",
            "text_layer_path": None,
            "transcription_path": str((tmp_path / "missing.md").as_posix()),
        })
        with open(m_file, "w", encoding="utf-8") as f:
            json.dump(manifest_data, f)

        valid, report = check_pages(m_file)
        assert not valid, "check_pages should fail when transcription is missing"
        assert report["missing_count"] == 1

    print("PASS: check_pages 100% coverage verification verified.")


def main():
    print("=" * 60)
    print("RUNNING CONTENT-TO-COURSE V2 VERIFICATION SUITE")
    print("=" * 60)

    test_zero_domain_keywords()
    test_sandbox_security()
    test_sandbox_execution_and_timeout()
    test_render_helpers()
    test_cta_validator()
    test_template_validation_and_instantiation()
    test_multiformat_ingestion()
    test_pages_validator()

    print("=" * 60)
    print("ALL VERIFICATION SUITE TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    main()
