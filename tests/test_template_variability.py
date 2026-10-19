"""Automated tests for template variability self-check and max-2 sharding policy.

Tests:
1. Template with narrow domain without variants fails competency diversity gate (TPL-VAR).
2. Template with stem_variants passes diversity gate.
3. test_shard_max_two: Verifies that partition_competencies_into_shards and determine_shard_count
   strictly generate shards with at most 2 competencies per shard:
   - 16 comps -> 8 shards of 2
   - 17 comps -> 8 shards of 2 and 1 shard of 1
   - 3 comps -> 1 shard of 2 and 1 shard of 1
   - 1 comp -> 1 shard of 1
"""

import json
from pathlib import Path
import pytest

# Ensure skill directory is on sys.path
SKILL_DIR = Path(__file__).resolve().parent.parent / ".agents" / "skills" / "content-to-course"
import sys
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from check_templates import check_competency_diversity, check_templates_file_or_dir
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
        "hints": ["Hint 1", "Hint 2", "Hint 3"],
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
        "hints": ["Hint 1", "Hint 2", "Hint 3"],
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
                "cross_check_py": "def verify(res):\n    return True",
                "hints": ["h1", "h2", "h3"],
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
                "cross_check_py": "def verify(res):\n    return True",
                "hints": ["h1", "h2", "h3"],
                "solution": "sol {v}",
                "distractor_ids": [],
            }
        ]
    }
    tpl_file.write_text(json.dumps(tpl_data_pass, indent=2), encoding="utf-8")

    valid_pass, errors_pass = check_templates_file_or_dir(tpl_file, cta_path=cta_file, num_dry_run_seeds=10)
    assert valid_pass, f"Expected validation to pass, but got errors: {errors_pass}"
    assert len(errors_pass) == 0


def test_shard_max_two():
    """Verify that determine_shard_count and partition_competencies_into_shards enforce max 2 competencies per shard.
    
    Checks:
    - 16 comps -> 8 shards of 2
    - 17 comps -> 8 shards of 2 and 1 shard of 1
    - 3 comps  -> 1 shard of 2 and 1 shard of 1
    - 1 comp   -> 1 shard of 1
    - No shard ever contains more than 2 competencies
    """
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

