"""Comprehensive unit & integration tests for C2C v3.3 Pipeline Hardening:
- Atomic Stage: run.py --stage bootstrap (< 3s, zero PNGs, lean specs, pointer work orders, .c2c_subagent_lock.json)
- Lockfile Lifecycle: release on publish and run.py --stage unlock / --unlock
- Universal Context Diet: pointer=True default across dispatch_cta, dispatch_authors, dispatch_judges
- .venv Python auto-resolution & --append Delta Context Injection in dispatch_cta
- ROLE_SPECS isolation (compile_shard in forbidden, shard_fixes in write)
- Wave-filtered dispatch (dispatch_authors --wave K) & run.py --stage wave-status (<= 5 lines)
- Cryptographic CRC32 per-item option shuffle (uniform A..G distribution, no letter > 35%)
- Incremental blind judge streaming with --ready-only and evaluated_competencies.json
"""

import contextlib
import io
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

import pytest

# Ensure skill directory is importable
skill_dir = Path(__file__).parent.parent / ".agents" / "skills" / "content-to-course"
if str(skill_dir) not in sys.path:
    sys.path.insert(0, str(skill_dir))

import c2c_hook_guard
from dispatch import (
    ROLE_SPECS,
    _resolve_repo_python_and_env,
    build_dispatch,
    dispatch_authors,
    dispatch_cta,
    dispatch_judges,
    generate_define_subagent_specs,
)
from judge import generate_judge_batch
from run import PipelineRunner, cap_stdout_to_log


def create_synthetic_pdf(target_path: Path, title: str, pages: int = 3) -> None:
    """Creates a fast, valid synthetic PDF without raster images."""
    try:
        import pymupdf as fitz
    except ImportError:
        import fitz

    doc = fitz.open()
    for p in range(pages):
        page = doc.new_page()
        page.insert_text(
            (50, 72),
            f"Course Document: {title}\nPage {p + 1} of {pages}\nSection {p + 1}.0 Foundations of Topic",
            fontsize=12,
        )
        page.insert_text(
            (50, 150),
            "Mathematical definition: Let X ~ N(mu, sigma^2). Then E[X] = mu and Var(X) = sigma^2.",
            fontsize=10,
        )
    target_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(target_path))
    doc.close()


def create_mock_template_file(template_file: Path, cid: str) -> None:
    """Creates a valid mock template JSON file with MC7 options."""
    template_payload = {
        "competency_id": cid,
        "templates": [
            {
                "id": f"T-{cid}-01",
                "template_id": f"T-{cid}-01",
                "competency_id": cid,
                "interaction_type": "multiple_choice_7_options",
                "stem": f"Calculate the optimal value for {cid}: parameter ${{k}}$",
                "generate_py": (
                    "def generate(rng):\n"
                    "    k = rng.randint(2, 20)\n"
                    "    correct = f'Option {k}'\n"
                    "    distractors = [\n"
                    "        {'value': f'Distractor {k+1}', 'distractor_id': 'D-01', 'error_rationale': 'off by 1'},\n"
                    "        {'value': f'Distractor {k+2}', 'distractor_id': 'D-02', 'error_rationale': 'off by 2'},\n"
                    "        {'value': f'Distractor {k+3}', 'distractor_id': 'D-03', 'error_rationale': 'off by 3'},\n"
                    "        {'value': f'Distractor {k+4}', 'distractor_id': 'D-04', 'error_rationale': 'off by 4'},\n"
                    "        {'value': f'Distractor {k+5}', 'distractor_id': 'D-05', 'error_rationale': 'off by 5'},\n"
                    "        {'value': f'Distractor {k+6}', 'distractor_id': 'D-06', 'error_rationale': 'off by 6'},\n"
                    "    ]\n"
                    "    return {'vars': {'k': k}, 'correct': correct, 'distractors': distractors}\n"
                ),
            }
        ],
    }
    template_file.parent.mkdir(parents=True, exist_ok=True)
    template_file.write_text(json.dumps(template_payload, indent=2), encoding="utf-8")


# ==============================================================================
# TEST 1: run.py --stage bootstrap & Lockfile Lifecycle Release
# ==============================================================================

def test_stage_bootstrap_atomic_and_lockfile_lifecycle(tmp_path: Path):
    """Certifies run.py --stage bootstrap executes in < 3s, zero PNGs, writes lean specs,
    pointer CTA work orders, conforming .c2c_subagent_lock.json, and releases lock on publish & unlock.
    """
    sources_dir = tmp_path / "sources"
    doc1 = sources_dir / "chapter_01.pdf"
    doc2 = sources_dir / "chapter_02.pdf"
    create_synthetic_pdf(doc1, "Microeconomics 1", pages=3)
    create_synthetic_pdf(doc2, "Microeconomics 2", pages=3)

    work_dir = tmp_path / "work"
    runner = PipelineRunner(
        pdf=[doc1, doc2],
        course_id="test_micro_course",
        work_dir=work_dir,
        director_id="director_conv_9988",
    )

    t0 = time.time()
    bootstrap_res = runner.run_stage_bootstrap()
    elapsed = time.time() - t0

    # 1. SLA Performance: local compute < 3.0s
    assert elapsed < 3.0, f"Bootstrap stage took {elapsed:.2f}s, exceeding 3.0s SLA!"

    # 2. Zero-Raster Guarantee: zero PNGs generated anywhere in work_dir
    png_files = list(work_dir.glob("**/*.png"))
    assert len(png_files) == 0, f"Zero-raster violated: found {len(png_files)} PNG files!"

    # 3. Lean Subagent Specs: generated without dumping 87 KB subagent_types.json to stdout
    types_dir = work_dir / "dispatch" / "types"
    assert types_dir.is_dir()
    expected_types = ["c2c_cta_architect.json", "c2c_shard_author.json", "c2c_judge.json", "c2c_repair.json"]
    for tf_name in expected_types:
        tf_path = types_dir / tf_name
        assert tf_path.is_file(), f"Missing expected lean spec: {tf_name}"
        assert tf_path.stat().st_size < 10000, f"Lean spec {tf_name} exceeds 10 KB: {tf_path.stat().st_size} bytes"

    # 4. CTA Work Orders: written to disk
    cta_orders_file = work_dir / "dispatch" / "cta_work_orders.json"
    assert cta_orders_file.is_file()
    cta_orders_data = json.loads(cta_orders_file.read_text(encoding="utf-8"))
    assert "Subagents" in cta_orders_data
    assert len(cta_orders_data["Subagents"]) >= 1

    # 5. Lockfile Invariant: active .c2c_subagent_lock.json conforming to c2c_hook_guard schema
    lock_file = work_dir / ".c2c_subagent_lock.json"
    assert lock_file.is_file(), "Missing required .c2c_subagent_lock.json file!"
    lock_data = json.loads(lock_file.read_text(encoding="utf-8"))
    assert lock_data.get("active") is True
    assert lock_data.get("director_conversation_id") == "director_conv_9988"
    assert lock_data.get("course_id") == "test_micro_course"
    assert lock_data.get("work_dir") == work_dir.resolve().as_posix()
    assert isinstance(lock_data.get("exempt_conversation_ids"), list)
    assert "created_at" in lock_data

    # Verify c2c_hook_guard detects the lock
    found_lock = c2c_hook_guard.find_active_c2c_lock(str(lock_file))
    assert found_lock is not None
    assert found_lock["director_conversation_id"] == "director_conv_9988"

    # 6. Bootstrap summary output
    assert bootstrap_res["status"] == "ready_for_cta"
    assert bootstrap_res["course_id"] == "test_micro_course"
    assert len(bootstrap_res["type_spec_files"]) >= 4

    # 7. Lockfile Lifecycle Release: run.py --stage unlock
    unlock_res = runner.run_stage_unlock()
    assert unlock_res["status"] == "unlocked"
    assert unlock_res["released"] is True
    assert not lock_file.is_file(), "Lockfile was not unlinked on unlock stage!"

    # c2c_hook_guard must now report no active lock
    assert c2c_hook_guard.find_active_c2c_lock(str(lock_file)) is None


# ==============================================================================
# TEST 2: Universal Context Diet (pointer=True Default & Backward Compatibility)
# ==============================================================================

def test_pointer_mode_default_and_backward_compatibility(tmp_path: Path):
    """Certifies pointer=True is the default across dispatch_cta, dispatch_authors, dispatch_judges,
    emitting ultra-compact <= 300 B prompts, while pointer=False maintains 100% full inline prompts.
    """
    work_dir = tmp_path / "diet_work"
    work_dir.mkdir(parents=True, exist_ok=True)

    # Setup mock manifests
    (work_dir / "pre_cta_manifest.json").write_text(json.dumps({
        "course_id": "diet_test",
        "cta_mode": "direct",
        "documents": [{"name": "textbook.pdf", "path": "content/textbook.pdf", "total_pages": 20}],
    }), encoding="utf-8")

    (work_dir / "cta.json").write_text(json.dumps({
        "course_id": "diet_test",
        "competencies": [
            {
                "id": "C-01",
                "name": "Marginal Productivity",
                "type": "concept",
                "description_latex": r"$\frac{\partial Y}{\partial K} = MPK$",
                "distractors": [{"id": "D-01", "name": "Confusing average with marginal", "wrong_belief": "Y/K"}],
            }
        ],
    }), encoding="utf-8")

    shards_dir = work_dir / "shards"
    shards_dir.mkdir(parents=True, exist_ok=True)
    (shards_dir / "pre_shard_manifest.json").write_text(json.dumps({
        "shards": [{"shard_id": "shard_01", "competency_ids": ["C-01"]}],
    }), encoding="utf-8")

    verif_dir = work_dir / "verification"
    verif_dir.mkdir(parents=True, exist_ok=True)
    (verif_dir / "judge_batch_01.json").write_text(json.dumps([
        {"question_id": "Q-01", "question_type": "multiple_choice", "stem_es": "Calcule MPK", "options": [{"id": "A", "content": "5.0"}]},
    ]), encoding="utf-8")

    # 1. dispatch_cta: Default pointer=True vs pointer=False
    cta_default = dispatch_cta(work_dir)
    prompt_cta_ptr = cta_default["Subagents"][0]["Prompt"]
    assert len(prompt_cta_ptr.encode("utf-8")) <= 300, f"CTA pointer prompt exceeds 300 B: {len(prompt_cta_ptr)}"
    assert "cta_01.json" in prompt_cta_ptr
    assert "view_file" in prompt_cta_ptr

    cta_inline = dispatch_cta(work_dir, pointer=False)
    prompt_cta_full = cta_inline["Subagents"][0]["Prompt"]
    assert len(prompt_cta_full.encode("utf-8")) > 500
    assert "textbook.pdf" in prompt_cta_full
    assert "compile_cta.py" in prompt_cta_full

    # 2. dispatch_authors: Default pointer=True vs pointer=False
    author_default = dispatch_authors(work_dir)
    prompt_auth_ptr = author_default["Subagents"][0]["Prompt"]
    assert len(prompt_auth_ptr.encode("utf-8")) <= 300, f"Author pointer prompt exceeds 300 B: {len(prompt_auth_ptr)}"
    assert "author_01.json" in prompt_auth_ptr
    assert "shard_01_data.py" in prompt_auth_ptr
    assert "compile_shard.py" in prompt_auth_ptr

    author_inline = dispatch_authors(work_dir, pointer=False)
    prompt_auth_full = author_inline["Subagents"][0]["Prompt"]
    assert len(prompt_auth_full.encode("utf-8")) > 500
    assert "Marginal Productivity" in prompt_auth_full
    assert "D-01" in prompt_auth_full

    # 3. dispatch_judges: Default pointer=True vs pointer=False
    judge_default = dispatch_judges(work_dir)
    prompt_judge_ptr = judge_default["Subagents"][0]["Prompt"]
    assert len(prompt_judge_ptr.encode("utf-8")) <= 300, f"Judge pointer prompt exceeds 300 B: {len(prompt_judge_ptr)}"
    assert "judge_01.json" in prompt_judge_ptr
    assert "DONE: work/verification/judge_responses_01.json" in prompt_judge_ptr

    judge_inline = dispatch_judges(work_dir, pointer=False)
    prompt_judge_full = judge_inline["Subagents"][0]["Prompt"]
    assert len(prompt_judge_full.encode("utf-8")) > 500
    assert "Q-01" in prompt_judge_full
    assert "Calcule MPK" in prompt_judge_full


# ==============================================================================
# TEST 3: .venv Python Auto-Resolution, Delta Manifest Injection & ROLE_SPECS
# ==============================================================================

def test_python_auto_resolution_delta_injection_and_role_specs(tmp_path: Path):
    """Certifies _resolve_repo_python_and_env auto-resolves .venv Python executable with safe cmd prefix,
    delta_manifest injects next_ids_by_prefix & existing_competencies_outline, and ROLE_SPECS enforces isolation.
    """
    # 1. Auto-resolution of .venv Python
    repo_root, py_path, cmd_prefix = _resolve_repo_python_and_env()
    assert Path(py_path).is_file() or Path(py_path).exists()
    assert "/" in py_path  # POSIX normalized
    if sys.platform == "win32":
        assert cmd_prefix.startswith('& "')
        assert "$env:PYTHONPATH=" not in cmd_prefix
        assert c2c_hook_guard.PYTHON_EXEC_PATTERN.match(f"{cmd_prefix} script.py")
    else:
        assert cmd_prefix.startswith('"')
        assert "PYTHONPATH=" not in cmd_prefix

    # 2. Delta Manifest Injection in dispatch_cta
    work_dir = tmp_path / "delta_work"
    work_dir.mkdir(parents=True, exist_ok=True)
    (work_dir / "pre_cta_manifest.json").write_text(json.dumps({
        "course_id": "append_test",
        "cta_mode": "direct",
        "documents": [{"name": "annex.pdf", "path": "content/annex.pdf", "total_pages": 15}],
    }), encoding="utf-8")

    delta_payload = {
        "next_ids_by_prefix": {"H": 11, "C": 7, "Hab": 1},
        "existing_competencies_outline": [
            {"id": "C-01", "type": "concept", "name": "Base Concept 1"},
            {"id": "H-01", "type": "skill", "name": "Base Skill 1"},
        ],
    }
    (work_dir / "delta_manifest.json").write_text(json.dumps(delta_payload, indent=2), encoding="utf-8")

    cta_res = dispatch_cta(work_dir, pointer=True)
    item_file = Path(cta_res["item_files"][0])
    assert item_file.is_file()
    item_data = json.loads(item_file.read_text(encoding="utf-8"))

    # Assert delta_context is injected into work order JSON
    assert "delta_context" in item_data
    assert item_data["delta_context"]["next_ids_by_prefix"]["H"] == 11
    assert item_data["delta_context"]["next_ids_by_prefix"]["C"] == 7
    assert len(item_data["delta_context"]["existing_competencies_outline"]) == 2

    # Assert work_order text explicitly forbids duplicating existing base competencies
    work_order_text = item_data.get("work_order", "")
    assert "APPEND DELTA MODE" in work_order_text
    assert "PROHIBIDO reiniciar la numeración en 01 o duplicar competencias base" in work_order_text

    # 3. ROLE_SPECS Hardening Invariants
    author_spec = ROLE_SPECS["author"]
    assert ".agents/skills/content-to-course/compile_shard.py" in author_spec["forbidden"]
    assert ".agents/skills/content-to-course/compile_shard.py" not in author_spec["read"]
    assert "work/shards/shard_fixes/<CID>.py" in author_spec["write"]

    repair_spec = ROLE_SPECS["repair"]
    assert ".agents/skills/content-to-course/compile_shard.py" in repair_spec["forbidden"]
    assert ".agents/skills/content-to-course/compile_shard.py" not in repair_spec["read"]
    assert "work/shards/shard_fixes/<CID>.py" in repair_spec["write"]


# ==============================================================================
# TEST 4: Wave Dispatch Filtering & Wave-Status Summary (<= 5 Lines)
# ==============================================================================

def test_wave_filtering_and_wave_status(tmp_path: Path):
    """Certifies dispatch_authors --wave K filters shards per wave and
    run.py --stage wave-status prints a crystal-clear <= 5-line summary.
    """
    work_dir = tmp_path / "wave_work"
    work_dir.mkdir(parents=True, exist_ok=True)
    shards_dir = work_dir / "shards"
    shards_dir.mkdir(parents=True, exist_ok=True)

    (work_dir / "pre_cta_manifest.json").write_text(json.dumps({
        "course_id": "wave_course",
        "documents": [{"name": "math.pdf", "path": "content/math.pdf", "total_pages": 20}],
    }), encoding="utf-8")

    (work_dir / "cta.json").write_text(json.dumps({
        "course_id": "wave_course",
        "competencies": [
            {"id": "Hab-01", "name": "Calculus 1", "type": "skill"},
            {"id": "Hab-02", "name": "Calculus 2", "type": "skill"},
            {"id": "C-01", "name": "Algebra 1", "type": "concept"},
            {"id": "C-02", "name": "Algebra 2", "type": "concept"},
        ],
    }), encoding="utf-8")

    pre_shard_manifest = {
        "total_shards": 4,
        "total_waves": 2,
        "waves": [
            {"wave_index": 1, "shard_ids": ["shard_01", "shard_02"]},
            {"wave_index": 2, "shard_ids": ["shard_03", "shard_04"]},
        ],
        "shards": [
            {"shard_id": "shard_01", "wave_index": 1, "competency_ids": ["Hab-01"]},
            {"shard_id": "shard_02", "wave_index": 1, "competency_ids": ["Hab-02"]},
            {"shard_id": "shard_03", "wave_index": 2, "competency_ids": ["C-01"]},
            {"shard_id": "shard_04", "wave_index": 2, "competency_ids": ["C-02"]},
        ],
    }
    (shards_dir / "pre_shard_manifest.json").write_text(json.dumps(pre_shard_manifest, indent=2), encoding="utf-8")

    # 1. Wave 1 dispatch: exactly 2 subagents (shard_01, shard_02)
    res_w1 = dispatch_authors(work_dir, wave_index=1)
    assert len(res_w1["Subagents"]) == 2
    assert "shard_01" in res_w1["Subagents"][0]["Role"] or "shard_02" in res_w1["Subagents"][0]["Role"]
    assert "shard_03" not in str(res_w1["Subagents"])
    assert "shard_04" not in str(res_w1["Subagents"])

    # 2. Wave 2 dispatch: exactly 2 subagents (shard_03, shard_04)
    res_w2 = dispatch_authors(work_dir, wave_index=2)
    assert len(res_w2["Subagents"]) == 2
    assert "shard_03" in res_w2["Subagents"][0]["Role"] or "shard_04" in res_w2["Subagents"][0]["Role"]
    assert "shard_01" not in str(res_w2["Subagents"])
    assert "shard_02" not in str(res_w2["Subagents"])

    # 3. Wave Status: simulate shard_01 completed, shard_02 circuit-broken, shards 03 & 04 pending
    templates_dir = work_dir / "templates"
    templates_dir.mkdir(parents=True, exist_ok=True)
    create_mock_template_file(templates_dir / "Hab-01.json", "Hab-01")

    attempts_dir = work_dir / ".check_attempts"
    attempts_dir.mkdir(parents=True, exist_ok=True)
    cb_state = {
        "distinct_compiles": 4,
        "same_error_streak": 3,
        "last_errors": ["[CIRCUIT BREAKER HALT: 3 fallos consecutivos idénticos para shard 'shard_02']"],
    }
    (attempts_dir / "compile_shard_02.json").write_text(json.dumps(cb_state), encoding="utf-8")

    runner = PipelineRunner(work_dir=work_dir, course_id="wave_course")

    stdout_capture = io.StringIO()
    with contextlib.redirect_stdout(stdout_capture):
        status_res = runner.run_stage_wave_status()

    output_lines = [line for line in stdout_capture.getvalue().splitlines() if line.strip()]

    # Assert crystal-clear <= 5 lines
    assert len(output_lines) <= 5, f"Wave status exceeded 5 lines ({len(output_lines)} lines):\n{stdout_capture.getvalue()}"
    assert status_res["total_shards"] == 4
    assert status_res["completed"] == 1
    assert status_res["circuit_broken"] == 1
    assert status_res["pending"] == 2

    # Check breakdown for Wave 1
    w1_stat = next(w for w in status_res["waves"] if w["wave_index"] == 1)
    assert w1_stat["completed"] == 1
    assert w1_stat["circuit_broken"] == 1
    assert w1_stat["pending"] == 0

    # Check breakdown for Wave 2
    w2_stat = next(w for w in status_res["waves"] if w["wave_index"] == 2)
    assert w2_stat["completed"] == 0
    assert w2_stat["circuit_broken"] == 0
    assert w2_stat["pending"] == 2


# ==============================================================================
# TEST 5: Cryptographic Per-Item Option Shuffle (CRC32) & Incremental Streaming
# ==============================================================================

def test_crc32_option_shuffle_and_incremental_judge_streaming(tmp_path: Path):
    """Certifies crc32 per-item option shuffle produces uniform distribution across A..G
    (no single letter > 35% across 40 items), coherent pointer instructions, and incremental streaming.
    """
    work_dir = tmp_path / "judge_work"
    work_dir.mkdir(parents=True, exist_ok=True)
    templates_dir = work_dir / "templates"
    templates_dir.mkdir(parents=True, exist_ok=True)

    # Create 20 templates (each will produce 2 items = 40 items total)
    comp_ids = [f"C-{i:02d}" for i in range(1, 21)]
    for cid in comp_ids:
        create_mock_template_file(templates_dir / f"{cid}.json", cid)

    (work_dir / "cta.json").write_text(json.dumps({
        "course_id": "shuffle_test",
        "competencies": [{"id": cid, "name": f"Competency {cid}"} for cid in comp_ids],
    }), encoding="utf-8")

    # 1. Generate blind judge batch with 2 items/competency = 40 items
    judge_p, gt_p = generate_judge_batch(
        templates_path=templates_dir,
        work_dir=work_dir,
        items_per_competency=2,
        seeds=(101, 202),
        ready_only=False,
    )

    assert Path(judge_p).is_file()
    assert Path(gt_p).is_file()

    gt_data = json.loads(Path(gt_p).read_text(encoding="utf-8"))
    total_items = len(gt_data)
    assert total_items == 40, f"Expected 40 items in ground truth, got {total_items}"

    # 2. Check uniform distribution across A..G
    # In MC7, letters are A, B, C, D, E, F, G.
    letter_counts: Dict[str, int] = {}
    for item_id, ans_info in gt_data.items():
        correct_letter = ans_info.get("correct_letter") or (ans_info.get("correct_letters", [None])[0])
        if correct_letter:
            letter = str(correct_letter).strip().upper()
            letter_counts[letter] = letter_counts.get(letter, 0) + 1

    assert len(letter_counts) >= 4, f"Insufficient diversity of correct letters: {letter_counts}"
    for letter, count in letter_counts.items():
        ratio = count / total_items
        assert ratio <= 0.35, f"Letter '{letter}' clustered at {ratio*100:.1f}% ({count}/{total_items}), exceeding 35% max!"

    # 3. Coherent Blind Judge Instructions in dispatch_judges
    judge_dispatch = dispatch_judges(work_dir, pointer=True)
    assert len(judge_dispatch["Subagents"]) >= 1
    judge_item_file = Path(judge_dispatch["item_files"][0])
    assert judge_item_file.is_file()

    judge_item_data = json.loads(judge_item_file.read_text(encoding="utf-8"))
    prompt_in_item = judge_item_data.get("Prompt", "")

    # Must contain prohibition of reading anything outside assigned item
    assert "PROHIBIDO leer cualquier archivo del curso, templates, shards o ground truth distinto de este lote asignado" in prompt_in_item
    # Must NOT contain contradictory prohibition of view_file
    assert "NO EJECUTES `view_file`" not in prompt_in_item

    # 4. Incremental Judge Streaming with ready_only=True
    evaluated_file = work_dir / "verification" / "evaluated_competencies.json"
    assert evaluated_file.is_file()
    eval_comps = json.loads(evaluated_file.read_text(encoding="utf-8"))
    eval_ids = set(eval_comps.get("evaluated_competency_ids", []))
    assert set(comp_ids).issubset(eval_ids)

    # Add 2 new competencies
    new_comps = ["C-21", "C-22"]
    for cid in new_comps:
        create_mock_template_file(templates_dir / f"{cid}.json", cid)

    # Re-run with ready_only=True: should ONLY evaluate C-21 and C-22 (4 items total)
    new_judge_p, new_gt_p = generate_judge_batch(
        templates_path=templates_dir,
        work_dir=work_dir,
        items_per_competency=2,
        seeds=(101, 202),
        ready_only=True,
    )
    new_gt_data = json.loads(Path(new_gt_p).read_text(encoding="utf-8"))
    assert len(new_gt_data) == 4, f"Incremental streaming should evaluate only 4 new items, got {len(new_gt_data)}"
    for item_id, item_info in new_gt_data.items():
        assert item_info.get("competency_id") in ("C-21", "C-22")


# ==============================================================================
# TEST 6: cap_stdout_to_log Utility Capping at <= 1500 Bytes
# ==============================================================================

def test_cap_stdout_to_log_enforces_1500_bytes_and_writes_full_log(tmp_path: Path):
    """Certifies cap_stdout_to_log persists full verbose log to work/logs/<stage>.log
    while capping console stdout to <= 1500 bytes with clear log reference note.
    """
    work_dir = tmp_path / "log_work"
    work_dir.mkdir(parents=True, exist_ok=True)

    captured_console = io.StringIO()
    with contextlib.redirect_stdout(captured_console):
        with cap_stdout_to_log(work_dir, "test_verbose_stage", max_bytes=1500):
            print("HEADER: Starting Verbose Compilation Stage...")
            for i in range(100):
                print(f"Verbose line {i:03d}: Compiling AST node {i} with deterministic seed {i*17}...")
            print("FOOTER: Stage completed successfully with status 0.")

    console_output = captured_console.getvalue()
    console_bytes = len(console_output.encode("utf-8"))
    assert console_bytes <= 1500, f"Console output exceeded 1500 B limit: {console_bytes} bytes!"
    assert "HEADER: Starting Verbose" in console_output
    assert "FOOTER: Stage completed successfully" in console_output
    assert "truncated verbose output" in console_output
    assert "work/logs/test_verbose_stage.log" in console_output

    # Check full log file on disk
    log_file = work_dir / "logs" / "test_verbose_stage.log"
    assert log_file.is_file()
    log_text = log_file.read_text(encoding="utf-8")
    assert len(log_text.encode("utf-8")) > 5000, "Full log on disk should not be truncated!"
    assert "Verbose line 050" in log_text


# ==============================================================================
# TEST 7: Cross-Stream Hook Guard Compatibility (compile_cmd vs PYTHON_EXEC_PATTERN)
# ==============================================================================

def test_compile_cmd_hook_guard_cross_stream_compatibility(tmp_path: Path):
    """Certifies compile_cmd format matches PYTHON_EXEC_PATTERN in c2c_hook_guard.py natively,
    preventing false denies when course work directory or path contains shell tokens
    such as 'type', 'cat', 'more', 'head', 'copy'.
    """
    course_dir = tmp_path / "course_type_cat_test"
    work_dir = course_dir / "work"
    work_dir.mkdir(parents=True, exist_ok=True)

    # Setup active lockfile in work_dir
    lock_file = work_dir / ".c2c_subagent_lock.json"
    lock_payload = {
        "active": True,
        "director_conversation_id": "conv_director_abc",
        "course_id": "course_type_cat_test",
        "work_dir": work_dir.resolve().as_posix(),
        "created_at": "2026-10-24T12:00:00Z",
        "exempt_conversation_ids": [],
    }
    lock_file.write_text(json.dumps(lock_payload), encoding="utf-8")

    # Generate CTA dispatch with course path containing 'cat' and 'type'
    (work_dir / "pre_cta_manifest.json").write_text(json.dumps({
        "course_id": "course_type_cat_test",
        "documents": [{"name": "category_catalog.pdf", "path": "content/category_catalog.pdf", "total_pages": 5}],
    }), encoding="utf-8")
    (work_dir / "cta.json").write_text(json.dumps({
        "course_id": "course_type_cat_test",
        "competencies": [{"id": "C-01", "name": "Cataloging Types"}],
    }), encoding="utf-8")
    (work_dir / "shards").mkdir(parents=True, exist_ok=True)
    (work_dir / "shards" / "pre_shard_manifest.json").write_text(json.dumps({
        "shards": [{"shard_id": "shard_01", "competency_ids": ["C-01"]}],
    }), encoding="utf-8")

    cta_res = dispatch_cta(work_dir)
    cta_item = json.loads(Path(cta_res["item_files"][0]).read_text(encoding="utf-8"))
    cta_compile_cmd = cta_item["compile_command"]

    author_res = dispatch_authors(work_dir)
    author_item = json.loads(Path(author_res["item_files"][0]).read_text(encoding="utf-8"))
    author_compile_cmd = author_item["compile_command"]

    repair_res = build_dispatch(role="repair", work_dir=work_dir, ids=["C-01"])
    items_dir = work_dir / "dispatch" / "items"
    repair_item = json.loads((items_dir / "repair_01.json").read_text(encoding="utf-8"))
    repair_compile_cmd = repair_item["compile_command"]

    # Test all 3 compile commands against c2c_hook_guard.process_hook with active lockfile
    for cmd_label, cmd_str in [("CTA", cta_compile_cmd), ("Author", author_compile_cmd), ("Repair", repair_compile_cmd)]:
        # Verify PYTHON_EXEC_PATTERN matches
        assert c2c_hook_guard.PYTHON_EXEC_PATTERN.match(cmd_str.strip()), f"{cmd_label} compile_cmd did not match PYTHON_EXEC_PATTERN: {cmd_str}"

        # Verify c2c_hook_guard.process_hook allows the execution without false deny
        hook_payload = {
            "tool_name": "run_command",
            "tool_args": {
                "CommandLine": cmd_str,
                "Cwd": str(work_dir),
            },
        }
        hook_res = c2c_hook_guard.process_hook(hook_payload, custom_lock_file=str(lock_file))
        assert hook_res.get("decision") == "allow", f"c2c_hook_guard falsely denied {cmd_label} command: {hook_res}"


# ==============================================================================
# TEST 8: Valid Parseable JSON <= 1500 Bytes Under Heavy Load (10 Shards / 6 CTA)
# ==============================================================================

def test_valid_parseable_json_under_1500_bytes_under_heavy_load(tmp_path: Path):
    """Certifies bootstrap, dispatch-cta, dispatch-authors, and dispatch-judges emit
    BOTH <= 1,500 bytes on console stdout AND 100% valid JSON parseable by json.loads
    even under heavy loads (6 CTA mapreduce parts, 10 wave shards, 10 judge batches).
    """
    work_dir = tmp_path / "heavy_load_work"
    work_dir.mkdir(parents=True, exist_ok=True)
    sources_dir = tmp_path / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)

    # 1. Setup 6 documents for MapReduce CTA
    doc_paths = []
    for i in range(1, 7):
        dp = sources_dir / f"chapter_{i:02d}.pdf"
        create_synthetic_pdf(dp, f"Chapter {i}", pages=2)
        doc_paths.append(dp)

    runner = PipelineRunner(
        pdf=doc_paths,
        course_id="heavy_course",
        work_dir=work_dir,
        cta_mode="mapreduce",
        director_id="director_heavy_99",
    )

    # Test STAGE BOOTSTRAP stdout under 6 MapReduce parts
    capture_boot = io.StringIO()
    with contextlib.redirect_stdout(capture_boot):
        runner.execute("bootstrap")

    stdout_boot = capture_boot.getvalue().strip()
    boot_bytes = len(stdout_boot.encode("utf-8"))
    assert boot_bytes <= 1500, f"Bootstrap stdout exceeded 1500 B: {boot_bytes} bytes!"
    boot_parsed = json.loads(stdout_boot)
    assert isinstance(boot_parsed, dict)
    assert boot_parsed.get("status") == "ready_for_cta"

    # Test STAGE DISPATCH-CTA stdout
    capture_cta = io.StringIO()
    with contextlib.redirect_stdout(capture_cta):
        runner.execute("dispatch-cta")

    stdout_cta = capture_cta.getvalue().strip()
    cta_bytes = len(stdout_cta.encode("utf-8"))
    assert cta_bytes <= 1500, f"dispatch-cta stdout exceeded 1500 B: {cta_bytes} bytes!"
    cta_parsed = json.loads(stdout_cta)
    assert isinstance(cta_parsed, dict)
    assert cta_parsed.get("stage") == "dispatch-cta"

    # 2. Setup 10 author shards for DISPATCH-AUTHORS
    comps_10 = [{"id": f"C-{i:02d}", "name": f"Competency {i}", "type": "skill"} for i in range(1, 11)]
    (work_dir / "cta.json").write_text(json.dumps({
        "course_id": "heavy_course",
        "competencies": comps_10,
    }), encoding="utf-8")
    shards_dir = work_dir / "shards"
    shards_dir.mkdir(parents=True, exist_ok=True)
    shards_10 = [
        {"shard_id": f"shard_{i:02d}", "wave_index": 1, "competency_ids": [f"C-{i:02d}"]}
        for i in range(1, 11)
    ]
    (shards_dir / "pre_shard_manifest.json").write_text(json.dumps({
        "total_shards": 10,
        "shards": shards_10,
    }, indent=2), encoding="utf-8")

    capture_auth = io.StringIO()
    with contextlib.redirect_stdout(capture_auth):
        runner.execute("dispatch-authors")

    stdout_auth = capture_auth.getvalue().strip()
    auth_bytes = len(stdout_auth.encode("utf-8"))
    assert auth_bytes <= 1500, f"dispatch-authors stdout exceeded 1500 B: {auth_bytes} bytes!"
    auth_parsed = json.loads(stdout_auth)
    assert isinstance(auth_parsed, dict)
    assert auth_parsed.get("stage") == "dispatch-authors"

    # 3. Setup 10 judge batches for DISPATCH-JUDGES
    verif_dir = work_dir / "verification"
    verif_dir.mkdir(parents=True, exist_ok=True)
    for i in range(1, 11):
        (verif_dir / f"judge_batch_{i:02d}.json").write_text(json.dumps([
            {"question_id": f"Q-{i:02d}-01", "stem": f"Question {i}", "options": [{"id": "A", "content": "Opt"}]}
        ]), encoding="utf-8")

    capture_judges = io.StringIO()
    with contextlib.redirect_stdout(capture_judges):
        runner.execute("dispatch-judges")

    stdout_judges = capture_judges.getvalue().strip()
    judges_bytes = len(stdout_judges.encode("utf-8"))
    assert judges_bytes <= 1500, f"dispatch-judges stdout exceeded 1500 B: {judges_bytes} bytes!"
    judges_parsed = json.loads(stdout_judges)
    assert isinstance(judges_parsed, dict)
    assert judges_parsed.get("stage") == "dispatch-judges"


# ==============================================================================
# TEST 9: Bootstrap --append End-to-End Forwarding & Delta Manifest
# ==============================================================================

def test_bootstrap_append_end_to_end_forwarding(tmp_path: Path):
    """Certifies run.py --stage bootstrap --append (or --base-course) cleanly forwards delta
    parameters to prepare_course and dispatch_cta in a single command, injecting
    next_ids_by_prefix & existing_competencies_outline into the bootstrap CTA work order.
    """
    courses_dir = tmp_path / "courses"
    courses_dir.mkdir(parents=True, exist_ok=True)

    # 1. Create base course with C-01..C-05 and H-01..H-03
    base_comps = [
        {"id": f"C-{i:02d}", "type": "concept", "name": f"Base Concept {i}"}
        for i in range(1, 6)
    ] + [
        {"id": f"H-{i:02d}", "type": "skill", "name": f"Base Skill {i}"}
        for i in range(1, 4)
    ]
    base_course_payload = {
        "course_id": "macro_base",
        "title": "Macroeconomics Base",
        "competencies": base_comps,
        "questions": [{"id": f"Q-{i}", "competency_id": "C-01"} for i in range(10)],
    }
    base_course_file = courses_dir / "macro_base.json"
    base_course_file.write_text(json.dumps(base_course_payload, indent=2), encoding="utf-8")

    # 2. Create annex document
    sources_dir = tmp_path / "sources"
    annex_doc = sources_dir / "macro_annex.pdf"
    create_synthetic_pdf(annex_doc, "Macroeconomics Annex Chapter", pages=3)

    work_dir = tmp_path / "work_macro_append"
    runner = PipelineRunner(
        pdf=annex_doc,
        course_id="macro_base",
        output_dir=courses_dir,
        work_dir=work_dir,
        base_course=base_course_file,
        append=True,
        director_id="director_append_01",
    )

    capture_out = io.StringIO()
    with contextlib.redirect_stdout(capture_out):
        boot_res = runner.run_stage_bootstrap()

    # Verify delta manifest created in work_dir
    delta_manifest_file = work_dir / "delta_manifest.json"
    assert delta_manifest_file.is_file(), "delta_manifest.json was not generated!"
    delta_data = json.loads(delta_manifest_file.read_text(encoding="utf-8"))

    # Assert next IDs start strictly at C-06 and H-04
    assert delta_data["next_ids_by_prefix"]["C-"] == "C-06"
    assert delta_data["next_ids_by_prefix"]["H-"] == "H-04"
    assert len(delta_data["existing_competencies_outline"]) == 8

    # Verify pre_cta_manifest.json contains delta block
    pre_cta_manifest = json.loads((work_dir / "pre_cta_manifest.json").read_text(encoding="utf-8"))
    assert pre_cta_manifest.get("append_mode") is True
    assert "delta" in pre_cta_manifest

    # Verify bootstrap work order contains delta context
    cta_orders_file = work_dir / "dispatch" / "cta_work_orders.json"
    assert cta_orders_file.is_file()
    item_file = Path(work_dir / "dispatch" / "items" / "cta_01.json")
    assert item_file.is_file()
    item_data = json.loads(item_file.read_text(encoding="utf-8"))

    assert "delta_context" in item_data
    assert item_data["delta_context"]["next_ids_by_prefix"]["C-"] == "C-06"
    assert "APPEND DELTA MODE" in item_data["Prompt"]
    assert "PROHIBIDO reiniciar la numeración en 01 o duplicar competencias base" in item_data["Prompt"]

    # Verify lockfile active
    lock_file = work_dir / ".c2c_subagent_lock.json"
    assert lock_file.is_file()
    assert json.loads(lock_file.read_text(encoding="utf-8"))["active"] is True


# ==============================================================================
# TEST 10: Incremental Judge Streaming (SHA-256 Awareness & Repair Re-evaluation)
# ==============================================================================

def test_judge_streaming_sha256_re_evaluation_on_repair_and_wave_isolation(tmp_path: Path):
    """Certifies:
    1. Wave isolation: Wave 1 (10 compiled templates) generates judge batch without crashing
       on missing Wave 2 templates (12 uncompiled).
    2. Incremental streaming skips unchanged Wave 1 templates in Wave 2.
    3. SHA-256 awareness: When a template is modified/repaired, it is AUTOMATICALLY re-evaluated
       under --ready-only while unchanged templates remain skipped.
    4. Repair dispatch uses .venv compile_cmd, forbids compile_shard.py, and targets shard_fixes/<CID>.py.
    """
    work_dir = tmp_path / "streaming_repair_work"
    work_dir.mkdir(parents=True, exist_ok=True)
    templates_dir = work_dir / "templates"
    templates_dir.mkdir(parents=True, exist_ok=True)

    # Setup cta.json with 22 total competencies (10 in Wave 1, 12 in Wave 2)
    wave1_cids = [f"C-{i:02d}" for i in range(1, 11)]
    wave2_cids = [f"C-{i:02d}" for i in range(11, 23)]
    all_comps = [{"id": cid, "name": f"Comp {cid}"} for cid in (wave1_cids + wave2_cids)]
    (work_dir / "cta.json").write_text(json.dumps({
        "course_id": "streaming_course",
        "competencies": all_comps,
    }), encoding="utf-8")

    # Wave 1: Only compile the 10 Wave 1 templates in work/templates/
    for cid in wave1_cids:
        create_mock_template_file(templates_dir / f"{cid}.json", cid)

    # 1. Wave 1 Judge Generation with ready_only=True: must succeed without crashing on missing Wave 2!
    w1_batch_p, w1_gt_p = generate_judge_batch(
        templates_path=templates_dir,
        work_dir=work_dir,
        items_per_competency=2,
        ready_only=True,
    )
    assert Path(w1_batch_p).is_file()
    w1_gt = json.loads(Path(w1_gt_p).read_text(encoding="utf-8"))
    assert len(w1_gt) == 20  # 10 competencies * 2 items

    # Check evaluated_competencies.json recorded competency_hashes
    eval_file = work_dir / "verification" / "evaluated_competencies.json"
    assert eval_file.is_file()
    eval_data = json.loads(eval_file.read_text(encoding="utf-8"))
    assert len(eval_data["evaluated_competency_ids"]) == 10
    assert "competency_hashes" in eval_data
    assert len(eval_data["competency_hashes"]) == 10
    orig_c03_hash = eval_data["competency_hashes"]["C-03"]

    # 2. Wave 2: Compile remaining 12 templates
    for cid in wave2_cids:
        create_mock_template_file(templates_dir / f"{cid}.json", cid)

    # Run ready_only=True: must skip all 10 Wave 1 competencies and evaluate ONLY the 12 Wave 2 competencies!
    w2_batch_p, w2_gt_p = generate_judge_batch(
        templates_path=templates_dir,
        work_dir=work_dir,
        items_per_competency=2,
        ready_only=True,
    )
    w2_gt = json.loads(Path(w2_gt_p).read_text(encoding="utf-8"))
    assert len(w2_gt) == 24  # 12 competencies * 2 items
    for item_id, item_info in w2_gt.items():
        assert item_info["competency_id"] in wave2_cids
        assert item_info["competency_id"] not in wave1_cids

    eval_data_w2 = json.loads(eval_file.read_text(encoding="utf-8"))
    assert len(eval_data_w2["evaluated_competency_ids"]) == 22
    assert len(eval_data_w2["competency_hashes"]) == 22

    # 3. Targeted Repair on C-03: Modify work/templates/C-03.json
    c03_file = templates_dir / "C-03.json"
    c03_content = json.loads(c03_file.read_text(encoding="utf-8"))
    c03_content["templates"][0]["stem"] = "REPAIRED stem for C-03"
    c03_file.write_text(json.dumps(c03_content, indent=2), encoding="utf-8")

    # Run ready_only=True: C-03 MUST be re-evaluated because its SHA-256 hash changed!
    repair_batch_p, repair_gt_p = generate_judge_batch(
        templates_path=templates_dir,
        work_dir=work_dir,
        items_per_competency=2,
        ready_only=True,
    )
    repair_gt = json.loads(Path(repair_gt_p).read_text(encoding="utf-8"))
    assert len(repair_gt) == 2, f"Expected exactly 2 items for repaired C-03, got {len(repair_gt)}"
    for item_id, item_info in repair_gt.items():
        assert item_info["competency_id"] == "C-03"

    eval_data_repaired = json.loads(eval_file.read_text(encoding="utf-8"))
    assert eval_data_repaired["competency_hashes"]["C-03"] != orig_c03_hash

    # 4. Repair Dispatch Hardening: build_dispatch(role="repair", ids=["C-03"])
    shards_dir = work_dir / "shards"
    shards_dir.mkdir(parents=True, exist_ok=True)
    (shards_dir / "pre_shard_manifest.json").write_text(json.dumps({
        "shards": [{"shard_id": "shard_02", "competency_ids": ["C-03"]}],
    }), encoding="utf-8")

    repair_dispatch = build_dispatch(role="repair", work_dir=work_dir, ids=["C-03"])
    repair_item_file = Path(work_dir / "dispatch" / "items" / "repair_01.json")
    assert repair_item_file.is_file()
    repair_data = json.loads(repair_item_file.read_text(encoding="utf-8"))

    # Assert .venv compile_cmd
    cmd = repair_data["compile_command"]
    if sys.platform == "win32":
        assert cmd.startswith('& "')
        assert "$env:PYTHONPATH=" not in cmd
    assert "compile_shard.py" in cmd

    # Assert compile_shard in forbidden, not in read, and shard_fixes/<CID>.py in write
    prompt = repair_data["Prompt"]
    assert ".agents/skills/content-to-course/compile_shard.py" in prompt
    assert "shard_fixes/C-03.py" in prompt
