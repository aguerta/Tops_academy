"""Test suite for content-to-course v3 architecture upgrades.

Tests:
- Single-pass prepare_corpus and density scoring
- Dynamic competency sharding (plan_shards)
- Lazy sandbox import speedup and functional correctness
- Stage 3 instantiation signature compatibility and deterministic CRC32 seeding
"""

import json
import os
import sys
import tempfile
import time
import zlib
from pathlib import Path

import pytest

# Ensure skill directory is in sys.path
SKILL_DIR = Path(__file__).parent.parent / ".agents" / "skills" / "content-to-course"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from engine.instantiate import instantiate_competency
from engine.sandbox import execute_sandbox_instance
from ingest import prepare_corpus
from plan_shards import determine_shard_count, plan_shards


def test_prepare_corpus_outputs_and_density(tmp_path):
    """Test that prepare_corpus generates corpus.md, density.json, budget.json, and manifest.json."""
    sample_pdf = Path("content/estadistica3_Cano/EST3_LEC01_26_2.pdf")
    if not sample_pdf.exists():
        pytest.skip("Sample PDF not found.")

    res = prepare_corpus(
        input_path=sample_pdf,
        output_dir=tmp_path,
        vision="auto",
    )

    manifest_file = tmp_path / "pages" / "manifest.json"
    corpus_file = tmp_path / "corpus.md"
    density_file = tmp_path / "density.json"
    budget_file = tmp_path / "budget.json"

    assert manifest_file.exists(), "manifest.json was not created"
    assert corpus_file.exists(), "corpus.md was not created"
    assert density_file.exists(), "density.json was not created"
    assert budget_file.exists(), "budget.json was not created"

    density_data = json.loads(density_file.read_text(encoding="utf-8"))
    assert len(density_data) > 0

    budget_data = json.loads(budget_file.read_text(encoding="utf-8"))
    assert "total_estimated_tokens" in budget_data
    assert "pages_requiring_vision" in budget_data
    assert budget_data["vision_strategy"] in ("direct_cta", "parallel_patchers")


def test_plan_shards_partitioning(tmp_path):
    """Test that plan_shards partitions competencies deterministically into K shards."""
    cta_source = SKILL_DIR / "examples" / "edo" / "cta.json"
    if not cta_source.exists():
        cta_source = SKILL_DIR / "examples" / "edp" / "cta.json"

    res = plan_shards(cta_path=cta_source, output_dir=tmp_path / "shards")
    assert res["total_shards"] >= 1
    assert res["total_competencies"] >= 1

    manifest_file = tmp_path / "shards" / "manifest.json"
    assert manifest_file.exists()

    all_sharded_ids = []
    for s in res["shards"]:
        all_sharded_ids.extend(s["competency_ids"])
        s_file = Path(s["shard_file"])
        assert s_file.exists()
        s_content = json.loads(s_file.read_text(encoding="utf-8"))
        assert "competencies" in s_content
        assert "expected_templates" in s_content

    # Every competency assigned exactly once
    assert len(all_sharded_ids) == len(set(all_sharded_ids))
    assert len(all_sharded_ids) == res["total_competencies"]


def test_lazy_sandbox_execution_speed():
    """Verify that sandbox execution starts up quickly with lazy imports."""
    code = (
        "def generate(rng):\n"
        "    n = rng.randint(10, 20)\n"
        "    return {'vars': {'n': n}, 'correct': str(n * 2), 'distractors': []}\n"
    )
    t0 = time.time()
    res = execute_sandbox_instance(code, seed=42)
    elapsed = time.time() - t0

    assert res["vars"]["n"] >= 10
    assert int(res["correct"]) == res["vars"]["n"] * 2
    # Execution should be rapid (under 1.0 second on Windows)
    assert elapsed < 1.0, f"Execution was too slow: {elapsed:.2f}s"


def test_lazy_sandbox_functional_with_numpy():
    """Verify that templates using numpy work correctly with lazy loading."""
    code = (
        "def generate(rng):\n"
        "    arr = np.array([1, 2, 3])\n"
        "    s = int(np.sum(arr))\n"
        "    return {'vars': {'s': s}, 'correct': str(s), 'distractors': []}\n"
    )
    res = execute_sandbox_instance(code, seed=42)
    assert res["correct"] == "6"


def test_stage3_instantiation_signature_robustness():
    """Test that instantiate_competency handles legacy and modern signatures without TypeError."""
    comp_dict = {
        "id": "C-01",
        "type": "concept",
        "name": "Concepto de prueba",
    }
    dummy_template = {
        "id": "T-C01-01",
        "interaction_type": "fill_in_the_blank",
        "stem": "Respuesta: {x}",
        "hints": [
            "Pista 1: Observe el valor generado.",
            "Pista 2: Ingrese el valor como número entero.",
            "Pista 3: La respuesta correcta coincide con el valor numérico.",
        ],
        "detailed_solution": "El valor final es {x}.",
        "generate_py": (
            "def generate(rng):\n"
            "    x = rng.randint(1, 1000)\n"
            "    return {'vars': {'x': x}, 'correct': x, 'equivalents': [str(x)]}\n"
        ),
    }

    # Call with modern dict
    res_dict = instantiate_competency(
        competency=comp_dict,
        templates=[dummy_template],
        seed_offset_base=1000,
    )
    assert "questions" in res_dict
    assert len(res_dict["questions"]) == 20

    # Call with legacy kwargs
    res_legacy = instantiate_competency(
        competency_id="C-01",
        category="concept",
        templates=[dummy_template],
        quota=5,
        base_seed=1000,
    )
    assert "questions" in res_legacy
    assert len(res_legacy["questions"]) == 5


def test_deterministic_crc32_seeding():
    """Verify that zlib.crc32 generates strictly deterministic seeds across calls."""
    cid = "Hab-01"
    seed1 = zlib.crc32(cid.encode("utf-8")) % 10000
    seed2 = zlib.crc32(cid.encode("utf-8")) % 10000
    assert seed1 == seed2
    assert isinstance(seed1, int)
