"""Tests for Component 3: Scope-Lock, Subagent Dispatch Payload Generator,
Judge Batch Subdivision, and Multi-Response Comparison.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
import pytest

SKILL_DIR = Path(__file__).parent.parent / ".agents" / "skills" / "content-to-course"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from dispatch import (
    ROLE_SPECS,
    build_dispatch,
    dispatch_cta,
    dispatch_authors,
    dispatch_judges,
    generate_define_subagent_specs,
    load_system_prompt,
    snapshot_work_dir,
    scope_check,
)
from judge import (
    split_judge_batch,
    compare_judge_responses,
)

PROMPTS_DIR = SKILL_DIR / "system_prompts"


# ==============================================================================
# 1. TEST SYSTEM PROMPTS: SCOPE-LOCK & DONE CONTRACTS (v3.2)
# ==============================================================================

def test_all_system_prompts_have_scope_lock_and_done():
    """Verify that active prompts in system_prompts/ have ## 0. SCOPE-LOCK and DONE: rule."""
    active_prompts = ["prompt_cta_architect.md", "prompt_shard_author.md", "prompt_blind_judge.md"]
    for pf_name in active_prompts:
        pf = PROMPTS_DIR / pf_name
        assert pf.is_file(), f"Missing system prompt file: {pf_name}"
        content = pf.read_text(encoding="utf-8")
        assert "## 0. SCOPE-LOCK" in content, (
            f"Prompt {pf.name} missing '## 0. SCOPE-LOCK' section"
        )
        assert "DONE:" in content, (
            f"Prompt {pf.name} missing 'DONE:' termination contract"
        )


def test_prompt_shard_author_contracts():
    """Verify that prompt_shard_author.md authorizes compile_shard.py, includes multi-domain examples and tuple line error recovery."""
    content = (PROMPTS_DIR / "prompt_shard_author.md").read_text(encoding="utf-8")
    assert "compile_shard.py" in content, "prompt_shard_author.md must mention compile_shard.py"
    assert "Física" in content or "Fisica" in content, "Must include Physics domain example"
    assert "Sistemas Distribuidos" in content or "Distribuidos" in content, "Must include Distributed Systems domain example"
    assert "Líneas" in content or "Line" in content or "line" in content or "línea" in content, "Must include tuple-line error resolution"


# ==============================================================================
# 2. TEST ZERO-BUNDLE DISPATCH AND 100% UNTRUNCATED PROMPTS (<46,080 BYTES)
# ==============================================================================

def test_define_subagent_specs_zero_bundle_under_45kb(tmp_path: Path):
    """Verify generate_define_subagent_specs generates type json files < 46080 bytes with 100% full system prompts."""
    res = generate_define_subagent_specs(tmp_path)
    assert len(res["types"]) == 4
    types_dir = tmp_path / "dispatch" / "types"
    assert types_dir.is_dir()

    for spec in res["types"]:
        tname = spec["name"]
        clean_name = tname.replace("-", "_")
        tfile = types_dir / f"{clean_name}.json"
        assert tfile.is_file()
        file_size = tfile.stat().st_size
        assert file_size < 46080, f"Type file {tfile.name} exceeded 46,080 bytes: {file_size}"
        data = json.loads(tfile.read_text(encoding="utf-8"))
        assert len(data["system_prompt"]) > 500
        # No truncation markers
        assert "[TRUNCADO]" not in data["system_prompt"]
        assert "..." not in data["system_prompt"][:50]


def test_build_dispatch_cta_zero_bundle(tmp_path: Path):
    """Verify dispatch_cta and build_dispatch for CTA role generate item files < 46080 bytes."""
    manifest = {
        "course_id": "test_c",
        "cta_mode": "direct",
        "total_files": 1,
        "total_pages": 5,
        "files": [{"doc": "doc.pdf", "file_index": 0, "type": "pdf", "total_pages": 5}],
        "subparts": [],
    }
    (tmp_path / "pre_cta_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    res = dispatch_cta(tmp_path)
    assert len(res["Subagents"]) >= 1
    assert len(res["item_files"]) >= 1

    item_path = Path(res["item_files"][0])
    assert item_path.is_file()
    assert item_path.stat().st_size < 46080, f"CTA item file exceeded 46,080 bytes: {item_path.stat().st_size}"

    # Verify build_dispatch integration
    b_res = build_dispatch("cta", tmp_path)
    assert len(b_res["Subagents"]) >= 1

    # Verify legacy vision role raises ValueError
    with pytest.raises(ValueError, match="vision"):
        build_dispatch("vision", tmp_path)


def test_build_dispatch_authors_zero_bundle(tmp_path: Path):
    """Verify dispatch_authors generates author item files < 46080 bytes without COMPACT_AUTHOR_DIGEST and without pre-seeding templates."""
    pre_cta = {
        "course_id": "test_c",
        "cta_mode": "direct",
        "total_files": 1,
        "total_pages": 5,
        "files": [{"doc": "doc.pdf", "file_index": 0, "type": "pdf", "total_pages": 5}],
        "subparts": [],
    }
    (tmp_path / "pre_cta_manifest.json").write_text(json.dumps(pre_cta), encoding="utf-8")

    shards_dir = tmp_path / "shards"
    shards_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "total_shards": 2,
        "total_competencies": 4,
        "shards": [
            {
                "shard_id": "shard_01",
                "shard_index": 1,
                "competency_ids": ["C-01", "C-02"],
                "competencies": [{"id": "C-01", "name": "C1"}, {"id": "C-02", "name": "C2"}],
                "shard_data_path": str((shards_dir / "shard_01_data.py").as_posix()),
                "templates_dir": str((tmp_path / "templates").as_posix()),
            },
            {
                "shard_id": "shard_02",
                "shard_index": 2,
                "competency_ids": ["C-03", "C-04"],
                "competencies": [{"id": "C-03", "name": "C3"}, {"id": "C-04", "name": "C4"}],
                "shard_data_path": str((shards_dir / "shard_02_data.py").as_posix()),
                "templates_dir": str((tmp_path / "templates").as_posix()),
            },
        ],
    }
    (shards_dir / "pre_shard_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    res = dispatch_authors(tmp_path)
    assert len(res["Subagents"]) == 2
    assert len(res["item_files"]) == 2

    for item_file in res["item_files"]:
        ifile = Path(item_file)
        assert ifile.is_file()
        assert ifile.stat().st_size < 46080, f"Author item file exceeded 46,080 bytes: {ifile.stat().st_size}"
        data = json.loads(ifile.read_text(encoding="utf-8"))
        prompt = data["Prompt"]
        assert "COMPACT_AUTHOR_DIGEST" not in prompt

    # Verify templates were NOT pre-seeded in work/templates/
    templates_dir = tmp_path / "templates"
    if templates_dir.is_dir():
        assert len(list(templates_dir.glob("*.json"))) == 0


def test_build_dispatch_judge_never_reads_ground_truth(tmp_path: Path):
    """CRITICAL: Blind Judge dispatch must generate in-prompt payload <46080 bytes and NEVER read ground_truth."""
    (tmp_path / "judge_batch_01.json").write_text(
        json.dumps([{"question_id": "Q-01", "question_type": "multiple_choice", "stem_es": "¿Cuánto es 2+2?", "options": ["A: 4", "B: 5"]}]),
        encoding="utf-8",
    )
    (tmp_path / "judge_ground_truth.json").write_text(json.dumps({"Q-01": "A"}), encoding="utf-8")

    res = dispatch_judges(tmp_path)
    assert len(res["Subagents"]) == 1
    assert len(res["item_files"]) == 1

    item_file = Path(res["item_files"][0])
    assert item_file.is_file()
    assert item_file.stat().st_size < 46080

    prompt = res["Subagents"][0]["Prompt"]
    assert "judge_ground_truth.json" not in prompt.lower().split("prohibido")[0]
    assert "Q-01" in prompt
    assert "¿Cuánto es 2+2?" in prompt


# ==============================================================================
# 3. TEST SCOPE_CHECK: WRITE VIOLATION DETECTION
# ==============================================================================

def test_scope_check_clean_writes(tmp_path: Path):
    """Verify that allowed writes produce is_clean=True and empty violations."""
    # 1. Author writes allowed template file
    snap_author = snapshot_work_dir(tmp_path)
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir(parents=True, exist_ok=True)
    (templates_dir / "C-01.json").write_text('{"templates": []}', encoding="utf-8")

    is_clean, violations = scope_check(tmp_path, role="author", snapshot=snap_author)
    assert is_clean is True
    assert violations == []

    # 2. Judge writes allowed response file
    snap_judge = snapshot_work_dir(tmp_path)
    (tmp_path / "judge_responses_01.json").write_text('{"responses": {}}', encoding="utf-8")
    is_clean, violations = scope_check(tmp_path, role="judge", snapshot=snap_judge)
    assert is_clean is True
    assert violations == []


def test_scope_check_detects_unauthorized_writes(tmp_path: Path):
    """Verify that unauthorized writes are detected with is_clean=False and listed."""
    snap = snapshot_work_dir(tmp_path)

    # 1. Author illegally touches engine file
    engine_dir = tmp_path / "engine"
    engine_dir.mkdir(parents=True, exist_ok=True)
    (engine_dir / "sandbox.py").write_text("# modified code", encoding="utf-8")

    is_clean, violations = scope_check(tmp_path, role="author", snapshot=snap)
    assert is_clean is False
    assert any("sandbox.py" in v for v in violations)

    # 2. Judge illegally overwrites ground truth
    (tmp_path / "judge_ground_truth.json").write_text('{"tampered": true}', encoding="utf-8")
    is_clean, violations = scope_check(tmp_path, role="judge", snapshot=snap)
    assert is_clean is False
    assert any("judge_ground_truth.json" in v for v in violations)


# ==============================================================================
# 4. TEST SPLIT_JUDGE_BATCH: STRATIFIED BATCH SUBDIVISION
# ==============================================================================

def test_split_judge_batch_empty_and_small(tmp_path: Path):
    """Verify split_judge_batch behavior when empty or batch size <= items_per_judge."""
    # Case A: No file -> returns []
    assert split_judge_batch(tmp_path) == []

    # Case B: Small batch (8 items) -> 1 batch containing all 8 items
    items = [{"item_id": f"item_{i}", "competency_id": "C-01"} for i in range(8)]
    (tmp_path / "judge_batch.json").write_text(json.dumps(items), encoding="utf-8")

    splits = split_judge_batch(tmp_path, max_judges=4, items_per_judge=40)
    assert len(splits) == 1
    assert splits[0].name == "judge_batch_01.json"

    saved_items = json.loads(splits[0].read_text(encoding="utf-8"))
    assert len(saved_items) == 8


def test_split_judge_batch_stratified_multi_judge(tmp_path: Path):
    """Verify that split_judge_batch stratifies items across judges by competency."""
    # 90 items across 3 competencies: C-01 (30), C-02 (30), C-03 (30)
    items = []
    for c in ["C-01", "C-02", "C-03"]:
        for i in range(30):
            items.append({"item_id": f"{c}_{i}", "competency_id": c})

    (tmp_path / "judge_batch.json").write_text(json.dumps(items), encoding="utf-8")

    # With items_per_judge=40: ceil(90 / 40) = 3 judges
    splits = split_judge_batch(tmp_path, max_judges=4, items_per_judge=40)
    assert len(splits) == 3
    assert [p.name for p in splits] == [
        "judge_batch_01.json",
        "judge_batch_02.json",
        "judge_batch_03.json",
    ]

    all_split_items = []
    for sp in splits:
        batch_items = json.loads(sp.read_text(encoding="utf-8"))
        assert len(batch_items) == 30
        # Check stratification: every batch has items from all 3 competencies!
        c_counts = {}
        for itm in batch_items:
            cid = itm["competency_id"]
            c_counts[cid] = c_counts.get(cid, 0) + 1
        assert c_counts["C-01"] == 10
        assert c_counts["C-02"] == 10
        assert c_counts["C-03"] == 10
        all_split_items.extend(batch_items)

    # Verify no loss or duplication
    assert len(all_split_items) == 90
    assert {itm["item_id"] for itm in all_split_items} == {itm["item_id"] for itm in items}


# ==============================================================================
# 5. TEST COMPARE_JUDGE_RESPONSES: AUTO-DISCOVERY & MERGING
# ==============================================================================

def test_compare_judge_responses_autodiscovery(tmp_path: Path):
    """Verify that compare_judge_responses automatically discovers and merges split judge responses."""
    gt = {
        "item_1": {"interaction_type": "multiple_choice_7_options", "correct_letter": "A", "correct_content": "Alpha"},
        "item_2": {"interaction_type": "multiple_choice_7_options", "correct_letter": "B", "correct_content": "Beta"},
        "item_3": {"interaction_type": "fill_in_the_blank", "correct_value": 42.0},
    }
    (tmp_path / "judge_ground_truth.json").write_text(json.dumps(gt), encoding="utf-8")

    # Judge 1 solved items 1 and 2
    resp_1 = {
        "responses": {
            "item_1": {"answer": "A"},
            "item_2": {"answer": "B"},
        }
    }
    (tmp_path / "judge_responses_01.json").write_text(json.dumps(resp_1), encoding="utf-8")

    # Judge 2 solved item 3
    resp_2 = {
        "responses": {
            "item_3": {"answer": 42.0},
        }
    }
    (tmp_path / "judge_responses_02.json").write_text(json.dumps(resp_2), encoding="utf-8")

    # Call without responses parameter -> auto-discovers in work_dir
    report = compare_judge_responses(work_dir=tmp_path)

    assert report["total_items"] == 3
    assert report["agreed_items"] == 3
    assert report["agreement_rate"] == 1.0
    assert report["passed"] is True
    assert len(report["discordances"]) == 0
