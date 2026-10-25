# Stream 2A Improver Handoff (`stream_2a_impr`)

**From:** Improver (`Phase 2 of 3: Mejorador`)  
**To:** Auditor (`Phase 3 of 3: Auditor`)  
**Orchestrator Conversation ID:** `d0ce22db-904e-4856-b353-59975bfb5874`  
**Date:** 2026-10-24  
**Status:** COMPLETE (107/107 tests GREEN)

---

## 1. Summary of Improvements Made

### 1. [dispatch.py](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/dispatch.py)
- **`_resolve_repo_python_and_env()`:** Removed `$env:PYTHONPATH=...;` command prefix. Formatted Windows prefix as `& "<py_exe>"` and POSIX as `"<py_exe>"`. This guarantees 100% native compatibility with `PYTHON_EXEC_PATTERN` in `c2c_hook_guard.py` (`^\s*(?:&|call)?\s*["']...python.exe["']`), completely preventing false denials when course directories contain shell tokens (`type`, `cat`, `more`, `head`, `copy`).
- **`role="repair"` Dispatch Hardening:**
  - `compile_cmd` updated to use `.venv` `cmd_prefix`.
  - Added `.agents/skills/content-to-course/compile_shard.py` to `forbidden_paths` and verified exclusion from `read_paths`.
  - Added `work/shards/shard_fixes/<CID>.py` to `write_paths` and instructed authors/engineers to write modular patches there.
  - Added pointer mode support with compact instruction referencing `shard_fixes/<CID>.py`.
- **`dispatch_authors` & `dispatch_judges` Flexibility:**
  - Added `ids` parameter to `dispatch_authors` and `dispatch_judges` for surgical competency/shard filtering.

### 2. [run.py](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/run.py)
- **`format_compact_json_stdout(payload, work_dir, stage_name, work_orders_file, max_bytes=1450)`:**
  - Implemented cascading serializer ensuring console stdout is strictly `<= 1,500` bytes AND 100% valid parseable JSON:
    1. Tries `indent=2`.
    2. If `> 1,450` bytes, tries compact separators `(',', ':')`.
    3. If still `> 1,450` bytes, constructs a structured compact summary referencing disk work orders and stage logs.
- **JSON-Emitting Stages:**
  - Updated `run_stage_bootstrap`, `run_stage_dispatch_cta`, `run_stage_dispatch_authors`, and `run_stage_dispatch_judges` to emit their output via `format_compact_json_stdout`.
- **`--base-course` and `--append` End-to-End Forwarding:**
  - Added `base_course` parameter to `PipelineRunner.__init__` and `--base-course` CLI argument in `main()`.
  - Cleanly forwards delta parameters to `prepare_course`, injecting `next_ids_by_prefix` and `existing_competencies_outline` into `delta_manifest.json` and `pre_cta_manifest.json["delta"]`, which `dispatch_cta` seamlessly consumes.

### 3. [judge.py](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/judge.py)
- **SHA-256 Incremental Streaming & Repair Re-evaluation:**
  - Added SHA-256 template hashing in `_load_templates` and `generate_judge_batch`.
  - Recorded `competency_hashes: {cid: template_sha256}` in `evaluated_competencies.json`.
  - When `--ready-only` runs: unchanged templates are skipped, but **repaired/modified templates whose SHA-256 hash has changed are automatically re-evaluated**.
  - Synchronously writes batch and ground truth to both `work/` and `work/verification/`, purging stale `judge_batch_*.json` slices so `dispatch_judges` always slices fresh batches.
  - Handles wave isolation: generates judge batches for compiled Wave 1 templates without crashing on uncompiled Wave 2 templates.

### 4. [tests/test_bootstrap_and_wave_streaming.py](file:///d:/Augusto/personal_portfolio/Tops_academy/tests/test_bootstrap_and_wave_streaming.py)
- Updated `test_python_auto_resolution_delta_injection_and_role_specs` asserting clean `cmd_prefix` without `$env:PYTHONPATH=`.
- Added 4 new adversarial test cases:
  1. `test_compile_cmd_hook_guard_cross_stream_compatibility`: verifies `process_hook` returns `allow` under active worker lock with course paths containing `cat`, `type`, etc.
  2. `test_valid_parseable_json_under_1500_bytes_under_heavy_load`: verifies stdout `<= 1,500` B and `json.loads(stdout)` succeeds for 6 CTA parts, 10 wave shards, and 10 judge batches.
  3. `test_bootstrap_append_end_to_end_forwarding`: verifies single-command `--append` / `--base-course` delta injection into CTA work orders.
  4. `test_judge_streaming_sha256_re_evaluation_on_repair_and_wave_isolation`: verifies Wave 1 generation without Wave 2 templates, incremental skipping, automatic SHA-256 re-evaluation on template repair, and repair dispatch isolation.

---

## 2. Invariants Guaranteed & Maintained

1. **Strict File Isolation:** Only modified `run.py`, `dispatch.py`, `judge.py`, `test_bootstrap_and_wave_streaming.py`, and `stream_2a_impr/*`. Zero touches outside Write Boundaries.
2. **Zero Workspace Artifact Pollution:** Zero brain `ArtifactMetadata` passed to `write_file`/`edit_file`.
3. **Hermetic Test Isolation:** All tests strictly utilize `tmp_path`; zero `.c2c_subagent_lock.json` files left in repo root or `courses/*`.
4. **Director Context Diet & Output Cap SLA:** Console stdout for all dispatch and bootstrap stages strictly capped at `<= 1,500` bytes with valid parseable JSON.
5. **Worker Boundary Integrity:** Native `PYTHON_EXEC_PATTERN` matching prevents false denials during subagent script compilations.

---

## 3. Verification Command & Exact Test Results

```powershell
& "d:\Augusto\personal_portfolio\Tops_academy\.venv\Scripts\python.exe" -m pytest tests/test_bootstrap_and_wave_streaming.py tests/test_c2c_v321_comp3_dispatch.py tests/test_pipeline_reparations.py tests/test_orchestration_resilience.py tests/test_dispatch_scope.py tests/test_c2c_v31_adversarial_plan.py tests/test_skill.py -q
```

**Result:**
```
........................................................................ [ 67%]
...................................                                      [100%]
107 passed in 10.71s
```

- `tests/test_bootstrap_and_wave_streaming.py`: 10 passed
- `tests/test_c2c_v321_comp3_dispatch.py`: 7 passed
- `tests/test_pipeline_reparations.py`: 18 passed
- `tests/test_orchestration_resilience.py`: 16 passed
- `tests/test_dispatch_scope.py`: 11 passed
- `tests/test_c2c_v31_adversarial_plan.py`: 12 passed
- `tests/test_skill.py`: 33 passed
- **Total: 107 passed, 0 failed, 0 warnings.**
