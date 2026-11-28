import json
from pathlib import Path

from plan_shards import plan_shards
from dispatch import dispatch_authors


def _make_work(tmp_path: Path):
    work = tmp_path / "work"
    work.mkdir()
    (work / "pre_cta_manifest.json").write_text(
        json.dumps({"source_files": ["content/doc.pdf"]}),
        encoding="utf-8",
    )
    cta = {
        "course_id": "test_p1_4",
        "title": "Test P1.4",
        "competencies": [
            {
                "id": "Hab-01",
                "name": "Skill 1",
                "type": "skill",
                "recommended_modalities": ["open_symbolic", "unstructured_model", "adversarial_break"],
                "distractors": [{"id": f"D-01-0{i}", "name": f"d{i}", "wrong_belief": "w"} for i in range(1, 7)],
                "assumptions": [{"id": "A-01-01", "statement": "s", "violation_consequence": "c"}],
            },
            {
                "id": "Con-01",
                "name": "Concept 1",
                "type": "concept",
                "recommended_modalities": ["multiple_choice_7_options", "fill_in_the_blank", "concept_matching"],
                "distractors": [{"id": f"D-02-0{i}", "name": f"d{i}", "wrong_belief": "w"} for i in range(1, 7)],
                "assumptions": [{"id": "A-02-01", "statement": "s", "violation_consequence": "c"}],
            },
        ],
    }
    cta_p = work / "cta.json"
    cta_p.write_text(json.dumps(cta, indent=2), encoding="utf-8")
    return work, cta_p


def test_split_heavy_skills_arm_c(tmp_path: Path):
    work, cta_p = _make_work(tmp_path)
    res = plan_shards(cta_p, work / "shards", templates_per_modality=4, split_heavy_skills=True)
    shards = res["shards"]
    assert len(shards) == 3
    assert [s["shard_id"] for s in shards] == ["shard_01a", "shard_01b", "shard_02"]
    assert shards[0]["split_part"] == 1
    assert shards[0]["split_k"] == 2
    assert shards[0]["split_min_archetypes"] == 2
    assert shards[1]["split_part"] == 2
    assert shards[2]["templates_per_modality"] == 4

    manifest = dispatch_authors(work_dir=str(work), templates_per_modality=4)
    assert len(manifest["Subagents"]) == 3
    md_contents = [f.read_text(encoding="utf-8") for f in (work / "dispatch" / "items").glob("author_*.md")]
    p1 = next(v for v in md_contents if "`shard_01a`" in v)
    p2 = next(v for v in md_contents if "`shard_01b`" in v)
    p3 = next(v for v in md_contents if "`shard_02`" in v)
    assert "--templates-per-modality 2" in p1 and "--min-archetypes 2" in p1
    assert "T-Hab-01-07..12" in p2
    assert "--templates-per-modality 4" in p3


def test_adaptive_k_arm_d(tmp_path: Path):
    work, cta_p = _make_work(tmp_path)
    res = plan_shards(cta_p, work / "shards", templates_per_modality=4, adaptive_k=True)
    shards = res["shards"]
    assert len(shards) == 2
    assert shards[0]["competency_ids"] == ["Hab-01"]
    assert shards[0]["templates_per_modality"] == 4
    assert shards[1]["competency_ids"] == ["Con-01"]
    assert shards[1]["templates_per_modality"] == 3

    manifest = dispatch_authors(work_dir=str(work), templates_per_modality=4)
    assert len(manifest["Subagents"]) == 2
    md_contents = [f.read_text(encoding="utf-8") for f in (work / "dispatch" / "items").glob("author_*.md")]
    p1 = next(v for v in md_contents if "`shard_01`" in v)
    p2 = next(v for v in md_contents if "`shard_02`" in v)
    assert "--templates-per-modality 4" in p1
    assert "--templates-per-modality 3" in p2
