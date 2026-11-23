"""Tests for plan_shards capacity scaling (DEFAULT_COMPS_PER_SHARD=3, MAX_SKILLS_PER_SHARD=2)
and explicit competency type priority over ID prefixes.
"""

import json
import sys
from pathlib import Path

_skill_dir = Path(__file__).resolve().parents[1] / ".agents" / "skills" / "content-to-course"
if str(_skill_dir) not in sys.path:
    sys.path.insert(0, str(_skill_dir))

from plan_shards import (  # noqa: E402
    DEFAULT_COMPS_PER_SHARD,
    DEFAULT_MAX_WAVE_SIZE,
    MAX_SKILLS_PER_SHARD,
    is_concept_competency,
    is_fact_competency,
    is_skill_competency,
    partition_competencies_weighted,
    plan_shards,
)


def _make_competencies(num_skills: int, num_non_skills: int):
    comps = []
    for i in range(1, num_skills + 1):
        comps.append({
            "id": f"Hab-{i:02d}",
            "name": f"Skill {i:02d}",
            "type": "skill",
            "distractors": [{"id": f"D-Hab-{i:02d}-01", "evidence": {"doc": "doc.pdf"}}],
            "evidence": [{"doc": "doc.pdf"}],
        })
    for j in range(1, num_non_skills + 1):
        is_fact = (j % 2 == 1)
        cid = f"H-{(j + 1) // 2:02d}" if is_fact else f"C-{j // 2:02d}"
        comps.append({
            "id": cid,
            "name": f"Comp {cid}",
            "type": "fact" if is_fact else "concept",
            "distractors": [{"id": f"D-{cid}-01", "evidence": {"doc": "doc.pdf"}}],
            "evidence": [{"doc": "doc.pdf"}],
        })
    return comps


def _seed_workspace(tmp_path: Path, competencies, course_id: str = "cap_course"):
    work_dir = tmp_path / "work"
    shards_dir = work_dir / "shards"
    shards_dir.mkdir(parents=True, exist_ok=True)

    cta_path = work_dir / "cta.json"
    cta_path.write_text(
        json.dumps({"course_id": course_id, "title": course_id, "competencies": competencies}, indent=2),
        encoding="utf-8",
    )
    pre_cta_path = work_dir / "pre_cta_manifest.json"
    pre_cta_path.write_text(
        json.dumps({"course_id": course_id, "files": [{"doc": "doc.pdf", "path": "content/doc.pdf"}]}, indent=2),
        encoding="utf-8",
    )
    return cta_path, shards_dir


def test_capacity_constants():
    assert DEFAULT_COMPS_PER_SHARD == 2
    assert MAX_SKILLS_PER_SHARD == 1
    assert DEFAULT_MAX_WAVE_SIZE == 100


def test_35_skills_35_non_skills_vlean43_capacity(tmp_path):
    """35 skills + 35 non-skills -> 35/1 + ceil(35/2) = 35 + 18 = 53 shards, skills first."""
    comps = _make_competencies(35, 35)
    cta_path, shards_dir = _seed_workspace(tmp_path, comps, course_id="vlean43_sim")

    manifest = plan_shards(cta_path, shards_dir)
    shards = manifest["shards"]

    assert manifest["total_competencies"] == 70
    assert manifest["total_shards"] == 53
    assert len(shards) == 53

    # First 35 shards must be pure 1:1 skill shards
    skill_shards = shards[:35]
    non_skill_shards = shards[35:]
    assert len(skill_shards) == 35
    assert len(non_skill_shards) == 18

    for s in skill_shards:
        assert 1 <= s["competency_count"] <= MAX_SKILLS_PER_SHARD
        assert all(is_skill_competency(c) for c in s["competencies"])

    for s in non_skill_shards:
        assert 1 <= s["competency_count"] <= DEFAULT_COMPS_PER_SHARD
        assert all(not is_skill_competency(c) for c in s["competencies"])


def test_15_skills_25_non_skills_capacity():
    """15 skills + 25 non-skills -> 15/1 + ceil(25/2) = 15 + 13 = 28 shards."""
    comps = _make_competencies(15, 25)
    raw_shards = partition_competencies_weighted(comps)

    skill_shards = [s for s in raw_shards if s["is_skill"]]
    non_skill_shards = [s for s in raw_shards if not s["is_skill"]]

    assert len(skill_shards) == 15
    assert len(non_skill_shards) == 13
    assert len(raw_shards) == 28
    assert all(len(s["competency_ids"]) == 1 for s in skill_shards)
    assert all(1 <= len(s["competency_ids"]) <= 2 for s in non_skill_shards)


def test_explicit_type_overrides_id_prefix():
    """H-05 promoted to type='concept' must classify as concept and NOT fact."""
    promoted = {"id": "H-05", "type": "concept"}
    assert is_concept_competency(promoted) is True
    assert is_fact_competency(promoted) is False
    assert is_skill_competency(promoted) is False

    demoted = {"id": "C-05", "type": "fact"}
    assert is_fact_competency(demoted) is True
    assert is_concept_competency(demoted) is False
