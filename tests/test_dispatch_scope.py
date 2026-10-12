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
    snapshot_work_dir,
    scope_check,
)
from judge import (
    split_judge_batch,
    compare_judge_responses,
)

PROMPTS_DIR = SKILL_DIR / "system_prompts"


# ==============================================================================
# 1. TEST SYSTEM PROMPTS: SCOPE-LOCK & DONE CONTRACTS
# ==============================================================================

def test_all_system_prompts_have_scope_lock_and_done():
    """Verify that every prompt in system_prompts/ has ## 0. SCOPE-LOCK and DONE: rule."""
    prompt_files = list(PROMPTS_DIR.glob("prompt_*.md"))
    assert len(prompt_files) >= 7, f"Expected at least 7 prompts in {PROMPTS_DIR}, found {len(prompt_files)}"

    for pf in prompt_files:
        content = pf.read_text(encoding="utf-8")
        assert "## 0. SCOPE-LOCK (OBLIGATORIO)" in content, (
            f"Prompt {pf.name} missing '## 0. SCOPE-LOCK (OBLIGATORIO)' section"
        )
        assert "DONE:" in content, (
            f"Prompt {pf.name} missing 'DONE:' termination contract"
        )
        assert "Presupuesto de turnos sugerido:" in content, (
            f"Prompt {pf.name} missing turn budget suggestion"
        )
        assert "BLOCKED:" in content, (
            f"Prompt {pf.name} missing BLOCKED instruction for missing information"
        )


# ==============================================================================
# 2. TEST BUILD_DISPATCH: PAYLOAD STRUCTURE & PATH SPECIFICATIONS
# ==============================================================================

def test_build_dispatch_vision_with_manifest(tmp_path: Path):
    """Verify build_dispatch for 'vision' role using handouts manifest."""
    handouts_dir = tmp_path / "handouts"
    handouts_dir.mkdir(parents=True)

    manifest_data = {
        "shards": [
            {
                "shard_id": 1,
                "handout_ids": ["handout_001", "handout_002"],
                "docs": ["doc_A.pdf"],
            },
            {
                "shard_id": 2,
                "handout_ids": ["handout_003"],
                "docs": ["doc_B.pdf"],
            },
        ]
    }
    (handouts_dir / "handouts_manifest.json").write_text(json.dumps(manifest_data), encoding="utf-8")

    payload = build_dispatch(role="vision", work_dir=tmp_path)
    assert "Subagents" in payload
    subagents = payload["Subagents"]
    assert len(subagents) == 2

    # Check first subagent
    s1 = subagents[0]
    assert s1["TypeName"] in ("self", "c2c-vision")
    assert "Handout Vision Analyzer Shard 1" in s1["Role"]
    prompt1 = s1["Prompt"]
    assert "prompt_handout_transcriber.md" in prompt1
    assert "## SCOPE-LOCK (OBLIGATORIO)" in prompt1
    assert "work/handouts/handout_001.png" in prompt1
    assert "work/handouts/handout_001_text.md" in prompt1
    assert "work/handout_patches/patch_handout_001.md" in prompt1
    assert "código fuente" in prompt1
    assert "DONE: <archivos escritos>" in prompt1

    # Check audit file written
    audit_file = tmp_path / "dispatch" / "vision.json"
    assert audit_file.is_file()
    audit_data = json.loads(audit_file.read_text(encoding="utf-8"))
    assert audit_data["role"] == "vision"
    assert len(audit_data["Subagents"]) == 2


def test_build_dispatch_cta_map_and_reduce(tmp_path: Path):
    """Verify build_dispatch for 'cta-map' (with ready_only filter) and 'cta-reduce'."""
    sec_dir = tmp_path / "sections"
    sec_dir.mkdir(parents=True)

    sec_manifest = {
        "sections": [
            {"section_index": 1, "ready": True},
            {"section_index": 2, "ready": False},
        ]
    }
    (sec_dir / "sections_manifest.json").write_text(json.dumps(sec_manifest), encoding="utf-8")

    # cta-map ready_only=True
    map_payload = build_dispatch(role="cta-map", work_dir=tmp_path, ready_only=True)
    assert len(map_payload["Subagents"]) == 1
    m1 = map_payload["Subagents"][0]
    assert m1["Role"] == "CTA Section Mapper 01"
    assert "prompt_cta_sectional.md" in m1["Prompt"]
    assert "work/sections/section_01.md" in m1["Prompt"]
    assert "work/cta_parts/cta_part_01.json" in m1["Prompt"]

    # Calling again with ready_only should return 0 (already dispatched)
    map_payload_2 = build_dispatch(role="cta-map", work_dir=tmp_path, ready_only=True)
    assert len(map_payload_2["Subagents"]) == 0

    # cta-reduce
    reduce_payload = build_dispatch(role="cta-reduce", work_dir=tmp_path)
    assert len(reduce_payload["Subagents"]) == 1
    r1 = reduce_payload["Subagents"][0]
    assert r1["Role"] == "CTA Harmonizer"
    assert "prompt_cta_harmonizer.md" in r1["Prompt"]
    assert "work/cta_outline.json" in r1["Prompt"]
    assert "work/duplicate_candidates.json" in r1["Prompt"]
    assert "work/cta_harmonize.json" in r1["Prompt"]


def test_build_dispatch_author(tmp_path: Path):
    """Verify build_dispatch for 'author' role."""
    shards_dir = tmp_path / "shards"
    shards_dir.mkdir(parents=True)

    shards_manifest = {
        "shards": [
            {
                "shard_id": "shard_01",
                "shard_index": 1,
                "competency_ids": ["C-01", "C-02"],
            },
            {
                "shard_id": "shard_02",
                "shard_index": 2,
                "competency_ids": ["Hab-01"],
            },
        ]
    }
    (shards_dir / "manifest.json").write_text(json.dumps(shards_manifest), encoding="utf-8")

    payload = build_dispatch(role="author", work_dir=tmp_path)
    assert len(payload["Subagents"]) == 2

    a1 = payload["Subagents"][0]
    assert a1["Role"] == "Shard Author shard_01"
    assert "work/shards/shard_01.json" in a1["Prompt"]
    assert "work/templates/C-01.json" in a1["Prompt"]
    assert "work/templates/C-02.json" in a1["Prompt"]
    assert "engine/*" in a1["Prompt"]


def test_build_dispatch_judge_never_reads_ground_truth(tmp_path: Path):
    """CRITICAL: Blind Judge subagent prompt must NEVER contain ground_truth in READ."""
    # Create judge batches
    (tmp_path / "judge_batch_01.json").write_text(json.dumps([{"item_id": "1"}]), encoding="utf-8")
    (tmp_path / "judge_batch_02.json").write_text(json.dumps([{"item_id": "2"}]), encoding="utf-8")
    (tmp_path / "judge_ground_truth.json").write_text(json.dumps({"1": {}, "2": {}}), encoding="utf-8")

    payload = build_dispatch(role="judge", work_dir=tmp_path)
    assert len(payload["Subagents"]) == 2

    for judge_subagent in payload["Subagents"]:
        prompt = judge_subagent["Prompt"]

        # Parse sections of Prompt
        read_section = prompt.split("- WRITE permitido:")[0]
        forbidden_section = prompt.split("- PROHIBIDO:")[1] if "- PROHIBIDO:" in prompt else ""

        # Assert ground_truth NEVER in READ
        assert "ground_truth" not in read_section.lower(), (
            f"SECURITY VIOLATION: ground_truth was found in READ section of judge prompt:\n{read_section}"
        )
        assert "templates" not in read_section.lower(), (
            f"SECURITY VIOLATION: templates directory found in READ section of judge prompt:\n{read_section}"
        )

        # Assert explicitly listed in FORBIDDEN
        assert "judge_ground_truth.json" in forbidden_section
        assert "templates/*" in forbidden_section


# ==============================================================================
# 3. TEST SCOPE_CHECK: WRITE VIOLATION DETECTION
# ==============================================================================

def test_scope_check_clean_writes(tmp_path: Path):
    """Verify that allowed writes produce is_clean=True and empty violations."""
    # 1. Author writes allowed template file
    snap_author = snapshot_work_dir(tmp_path)
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir(parents=True)
    (templates_dir / "C-01.json").write_text('{"templates": []}', encoding="utf-8")

    is_clean, violations = scope_check(tmp_path, role="author", snapshot=snap_author)
    assert is_clean is True
    assert violations == []

    # 2. Vision writes allowed patch file
    snap_vision = snapshot_work_dir(tmp_path)
    patches_dir = tmp_path / "handout_patches"
    patches_dir.mkdir(parents=True)
    (patches_dir / "patch_handout_001.md").write_text("## <<DOC: x | PAGE: 1>>", encoding="utf-8")

    is_clean, violations = scope_check(tmp_path, role="vision", snapshot=snap_vision)
    assert is_clean is True
    assert violations == []

    # 3. Judge writes allowed response file
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
    engine_dir.mkdir(parents=True)
    (engine_dir / "sandbox.py").write_text("# modified code", encoding="utf-8")

    is_clean, violations = scope_check(tmp_path, role="author", snapshot=snap)
    assert is_clean is False
    assert any("sandbox.py" in v for v in violations)

    # 2. Judge illegally overwrites ground truth
    (tmp_path / "judge_ground_truth.json").write_text('{"tampered": true}', encoding="utf-8")
    is_clean, violations = scope_check(tmp_path, role="judge", snapshot=snap)
    assert is_clean is False
    assert any("judge_ground_truth.json" in v for v in violations)

    # 3. Vision analyzer illegally writes to corpus.md
    (tmp_path / "corpus.md").write_text("# corpus", encoding="utf-8")
    is_clean, violations = scope_check(tmp_path, role="vision", snapshot=snap)
    assert is_clean is False
    assert any("corpus.md" in v for v in violations)


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
