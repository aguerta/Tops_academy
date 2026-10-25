# Stream 2A Implementation Handoff (`stream_2a_impl`)

**From:** Implementer (`Phase 1 of 3: Implementador`)  
**To:** Improver (`Phase 2 of 3: Mejorador`)  
**Orchestrator Conversation ID:** `d0ce22db-904e-4856-b353-59975bfb5874`  
**Date:** 2026-10-24  
**Status:** COMPLETE (70/70 tests GREEN)

---

## 1. Summary of Changes by File

### 1. [dispatch.py](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/dispatch.py)
- **`_resolve_repo_python_and_env()`:** Added cross-platform auto-resolution of `.venv/Scripts/python.exe` (Windows) or `.venv/bin/python` (POSIX) with safe command prefix (`$env:PYTHONPATH="..."; & "..."` on Windows).
- **`make_pointer_prompt()`:** Compacted template string to strictly guarantee `<= 300 bytes` (~210–270 bytes actual size) across all roles.
- **`ROLE_SPECS` Hardening:**
  - `compile_shard.py` moved from `read` into `forbidden` for `author` and `repair`.
  - Added `work/shards/shard_fixes/<CID>.py` to allowed `write` for `author` and `repair`.
- **`dispatch_cta()`:**
  - Default changed to `pointer: bool = True`.
  - `compile_cmd` formatted with `.venv` python.
  - Injects `next_ids_by_prefix` and `existing_competencies_outline` from `delta_manifest.json` / `pre_cta_manifest.json["delta"]` into work order JSON and adds anti-duplication warnings.
  - Writes `work/dispatch/cta_work_orders.json`.
- **`dispatch_authors()`:**
  - Default changed to `pointer: bool = True`.
  - Added `wave_index: Optional[int] = None` filtering to limit dispatched authors per wave.
  - `compile_cmd` formatted with `.venv` python.
- **`dispatch_judges()`:**
  - Default changed to `pointer: bool = True`.
  - In pointer mode, allowed `READ` is set to `[work/dispatch/items/judge_XX.json]`.
  - Replaced contradictory `"NO EJECUTES view_file"` with `"PROHIBIDO leer cualquier archivo del curso, templates, shards o ground truth distinto de este lote asignado"`.
  - Supported `ready_only: bool = False`.
- **`build_dispatch()`:** Default changed to `pointer: bool = True`, passing `wave_index` and `ready_only`.
- **CLI `main()`:** Added `--wave` and `--no-pointer` arguments.

### 2. [judge.py](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/judge.py)
- **Cryptographic Option Shuffle (`crc32`):**
  - Imported `zlib`.
  - In `generate_judge_batch()`: computes deterministic per-item option shuffle seed:
    `option_shuffle_seed = zlib.crc32(f"{template_id}:{inst_idx}:{seed}".encode("utf-8")) & 0xFFFFFFFF`
    and passes `seed=option_shuffle_seed` to `assemble_question()`.
  - Yields uniform distribution across `A..G` (no single letter > 35% across 40 MC7 items).
- **Incremental Judge Streaming:**
  - Added `ready_only: bool = False` to `generate_judge_batch()`.
  - Reads and updates evaluated competency IDs in `work/verification/evaluated_competencies.json`.
  - Skips already-evaluated competencies when `ready_only=True`.
- **CLI `main()`:** Added `--ready-only` flag to `prepare` command.

### 3. [run.py](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/run.py)
- **`cap_stdout_to_log(work_dir, stage_name, max_bytes=1500)`:** Context manager wrapping stage executions in `execute()`, capping console stdout to `<= 1500 bytes` (showing head + tail with log reference note) and writing full verbose output to `work/logs/<stage_name>.log`.
- **`PipelineRunner.__init__()`:** Added arguments `director_id`, `wave`, `no_pointer`, `sources`, `source_dir`, and `unlock`.
- **`run_stage_bootstrap()`:**
  - Atomically runs `self.run_stage_prepare()`.
  - Calls `generate_define_subagent_specs(self.work_dir, lean=True)`.
  - Calls `dispatch_cta(self.work_dir, pointer=not self.no_pointer)`.
  - Writes active `work/.c2c_subagent_lock.json` matching `c2c_hook_guard.py` schema.
  - Emits compact JSON summary on stdout (`<= 1.5 KB`) and full verbose log in `work/logs/bootstrap.log`.
  - Local compute duration `< 0.15s` (SLA `< 3s`).
- **`run_stage_unlock()`:** Sets `"active": false` and unlinks `work/.c2c_subagent_lock.json`.
- **`run_stage_publish()`:** Automatically unlinks `work/.c2c_subagent_lock.json` when publication succeeds.
- **`run_stage_wave_status()`:**
  - Reads `pre_shard_manifest.json` (`shards` + `waves`).
  - Checks compiled `work/templates/<CID>.json` and circuit breakers in `.check_attempts/`.
  - Prints a crystal-clear `<= 5`-line summary of completed / pending / circuit-broken shards per wave in `< 150ms`.
- **Auxiliary Stages:** Registered `bootstrap`, `unlock`, `wave-status`, `dispatch-cta`, `dispatch-authors`, `dispatch-judges`, `judge-generate`.
- **CLI `main()`:** Registered new stage choices and arguments (`--director-id`, `--wave`, `--no-pointer`, `--sources`, `--source-dir`, `--unlock`).

### 4. [tests/test_bootstrap_and_wave_streaming.py](file:///d:/Augusto/personal_portfolio/Tops_academy/tests/test_bootstrap_and_wave_streaming.py) *(new)*
- 6 comprehensive tests covering:
  1. `test_stage_bootstrap_atomic_and_lockfile_lifecycle` (duration < 3s, zero PNGs, lean specs, pointer work orders, active lockfile, lock release on unlock).
  2. `test_pointer_mode_default_and_backward_compatibility` (`pointer=True` default <= 300 B prompts, `pointer=False` full inline prompts).
  3. `test_python_auto_resolution_delta_injection_and_role_specs` (`.venv` auto-resolution, `delta_manifest.json` injection, `ROLE_SPECS` isolation).
  4. `test_wave_filtering_and_wave_status` (`dispatch_authors --wave K` filtering, `wave-status` <= 5 lines).
  5. `test_crc32_option_shuffle_and_incremental_judge_streaming` (uniform A..G distribution, no letter > 35%, coherent judge pointer instructions, `--ready-only` incremental streaming).
  6. `test_cap_stdout_to_log_enforces_1500_bytes_and_writes_full_log` (stdout capped <= 1500 B, full verbose log persisted to disk).

### 5. Authorized Tier A Test Updates
- [tests/test_c2c_v321_comp3_dispatch.py](file:///d:/Augusto/personal_portfolio/Tops_academy/tests/test_c2c_v321_comp3_dispatch.py):
  - Updated `test_scope_lock_introspection_policy` asserting `compile_shard.py` in `forbidden`, not in `read`, and `shard_fixes/<CID>.py` in `write`.
  - Passed `pointer=False` where testing legacy inline Turn-0 prompt rendering.
  - Added pointer mode verification for judges.
- [tests/test_pipeline_reparations.py](file:///d:/Augusto/personal_portfolio/Tops_academy/tests/test_pipeline_reparations.py):
  - Line 331: updated `ROLE_SPECS["author"]` assertion asserting `compile_shard.py` in `forbidden` and not in `read`.
- [tests/test_dispatch_scope.py](file:///d:/Augusto/personal_portfolio/Tops_academy/tests/test_dispatch_scope.py):
  - Line 181: passed `pointer=False` for legacy inline prompt assertions and verified default pointer mode puts items inside `item_file`.
- [tests/test_c2c_v31_adversarial_plan.py](file:///d:/Augusto/personal_portfolio/Tops_academy/tests/test_c2c_v31_adversarial_plan.py):
  - Line 856: passed `pointer=False` to `build_dispatch(role='judge')` so legacy Zero-Warmup inline prompt assertions remain valid.

---

## 2. Invariants Guaranteed & Maintained

1. **Strict File Isolation:** Only files in Stream 2A Write Boundaries were touched. No files under `system_prompts/` or `SKILL.md` were modified (Stream 2B operated in parallel).
2. **Zero Workspace Artifact Pollution:** No brain `ArtifactMetadata` passed to `write_file`/`edit_file`.
3. **Hermetic Lockfile Lifecycle:** All tests use `tmp_path`; zero `.c2c_subagent_lock.json` files left in `REPO_ROOT` or `courses/*`.
4. **Director Context Diet SLA:** Pointer prompts are strictly `<= 300 bytes` across all roles while `work/dispatch/items/*.json` preserves 100% of rich work orders.
5. **Console Output Cap SLA:** Stage console stdout strictly capped at `<= 1,500 bytes` with full verbose logs preserved on disk.
6. **Zero-Raster Ingest:** No PNG tiles created during bootstrap or PDF ingestion.

---

## 3. Recommended Scrutiny Areas for Improver (Phase 2)

1. **PowerShell Quote Escaping in `cmd_prefix`:** Verify if complex nested quotes in PowerShell require further simplification if called inside specific sub-shells.
2. **Windows Path Separators in `evaluated_competencies.json`:** Verify that competency IDs containing dashes/underscores serialize identically across all operating systems.
3. **Concurrency of Multiple Waves:** Ensure that if Wave 1 and Wave 2 are dispatched concurrently in separate Director sessions, the work directories or IDs do not collide.
4. **`wave-status` with > 10 Waves:** Confirm formatting aesthetics when course documents are sharded into more than 4 waves.

---

## 4. Verification Command & Exact Test Results

```powershell
& "d:\Augusto\personal_portfolio\Tops_academy\.venv\Scripts\python.exe" -m pytest tests/test_bootstrap_and_wave_streaming.py tests/test_c2c_v321_comp3_dispatch.py tests/test_pipeline_reparations.py tests/test_orchestration_resilience.py tests/test_dispatch_scope.py tests/test_c2c_v31_adversarial_plan.py -q
```

**Result:**
```
......................................................................   [100%]
70 passed in 5.65s
```
- `tests/test_bootstrap_and_wave_streaming.py`: 6 passed
- `tests/test_c2c_v321_comp3_dispatch.py`: 7 passed
- `tests/test_pipeline_reparations.py`: 18 passed
- `tests/test_orchestration_resilience.py`: 16 passed
- `tests/test_dispatch_scope.py`: 11 passed
- `tests/test_c2c_v31_adversarial_plan.py`: 12 passed
- **Total: 70 passed, 0 failed, 0 warnings.**
