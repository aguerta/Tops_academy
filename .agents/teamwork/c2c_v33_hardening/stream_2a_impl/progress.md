# Stream 2A Implementation Progress (`stream_2a_impl`)

**Date:** 2026-10-24  
**Implementer:** `impl_2a` (Phase 1 of 3)  
**Status:** Completed & Tested (Ready for Phase 2 Improver)

---

## Completed Tasks

1. **Step 0 — Mandatory Pre-Flight Sanity Check & Tier A Escalation:**
   - Evaluated `run.py`, `dispatch.py`, `judge.py`, `c2c_hook_guard.py` (lines 93–220), `plan_shards.py` (lines 708–775), and existing dispatch/judge test suites.
   - Identified test contradictions regarding `compile_shard.py` in `ROLE_SPECS` and legacy inline `Prompt` assertions.
   - Documented verification in `stream_2a_impl/BRIEFING.md`.
   - Escalated to Orchestrator via `send_message` with `BLOCKER::`.
   - Received official approvals `APPROVED_TIER_A` expanding write boundaries to include:
     - `tests/test_c2c_v321_comp3_dispatch.py`
     - `tests/test_pipeline_reparations.py`
     - `tests/test_dispatch_scope.py`
     - `tests/test_c2c_v31_adversarial_plan.py`

2. **Universal Director Context Diet (`dispatch.py`):**
   - Changed default parameter to `pointer: bool = True` across `dispatch_cta()`, `dispatch_authors()`, `dispatch_judges()`, and `build_dispatch()`.
   - Updated CLI `dispatch.py` and `run.py` with `--no-pointer`.
   - Ensured `make_pointer_prompt` formats ultra-compact (~210–270 bytes, strictly <= 300 bytes) prompts referencing disk JSON work orders.
   - Ensured `work/dispatch/items/*.json` preserves 100% of rich work order context and compilation commands.

3. **Python `.venv` Auto-Resolution, Delta Ingestion & `ROLE_SPECS` Hardening (`dispatch.py`):**
   - Implemented `_resolve_repo_python_and_env()` helper returning `(repo_root_posix, python_exe_posix, cmd_prefix)`.
   - Formatted all generated `compile_cmd` strings using explicit POSIX-slashed `.venv` python executable and PowerShell/cross-platform invocation prefix (`$env:PYTHONPATH=...; & "..."`).
   - Implemented `--append` Delta Context injection in `dispatch_cta()` reading `delta_manifest.json` / `pre_cta_manifest.json["delta"]` and injecting `next_ids_by_prefix` and `existing_competencies_outline` with anti-duplication warnings into `work/dispatch/cta_work_orders.json` and item files.
   - Updated `ROLE_SPECS`:
     - `compile_shard.py` moved from `read` into `forbidden` for `author` and `repair`.
     - `work/shards/shard_fixes/<CID>.py` added to `write` for `author` and `repair`.

4. **Cryptographic Option Shuffle (`crc32`) & Incremental Streaming (`judge.py`):**
   - Integrated `zlib.crc32(f"{template_id}:{inst_idx}:{seed}".encode("utf-8")) & 0xFFFFFFFF` into `generate_judge_batch()`, passing `seed=option_shuffle_seed` to `assemble_question()`.
   - Validated that correct answer letters distribute uniformly across `A..G` (no single letter > 35% across 40 MC7 items).
   - In `dispatch_judges(pointer=True)`: allowed READ explicitly set to `[work/dispatch/items/judge_XX.json]` and replaced contradictory `"NO EJECUTES view_file"` with `"PROHIBIDO leer cualquier archivo del curso, templates, shards o ground truth distinto de este lote asignado"`.
   - Implemented incremental judge batching via `ready_only: bool = False`, recording evaluated competencies in `work/verification/evaluated_competencies.json` and skipping already-evaluated templates.
   - Added `--ready-only` flag to `judge.py prepare` CLI.

5. **Atomic Bootstrap Stage, Wave Status & Output Capping (`run.py`):**
   - Implemented `@contextlib.contextmanager def cap_stdout_to_log(work_dir, stage_name, max_bytes=1500)` capping console stdout at `<= 1500 bytes` and persisting full verbose output to `work/logs/<stage>.log`.
   - Implemented atomic stage `run_stage_bootstrap(self)`:
     - Pre-processes input course via `run_stage_prepare()`.
     - Generates lean subagent specs via `generate_define_subagent_specs(self.work_dir, lean=True)`.
     - Dispatches CTA via `dispatch_cta(self.work_dir, pointer=not self.no_pointer)`.
     - Writes active `work/.c2c_subagent_lock.json` conforming to `c2c_hook_guard.py` schema.
     - Emits concise JSON summary on stdout (`<= 1.5 KB`) and full log in `work/logs/bootstrap.log`.
   - Implemented `run_stage_unlock(self)` unlinking `.c2c_subagent_lock.json`.
   - Implemented lock release on successful `run_stage_publish()`.
   - Implemented `run_stage_wave_status(self)` reading `pre_shard_manifest.json` and checking compiled templates + circuit breakers in `.check_attempts/`, printing a crystal-clear `<= 5`-line summary of completed / pending / circuit-broken shards per wave in `< 150ms`.
   - Added auxiliary stages: `bootstrap`, `unlock`, `wave-status`, `dispatch-cta`, `dispatch-authors`, `dispatch-judges`, `judge-generate`.
   - Updated `main()` CLI with `--director-id`, `--wave`, `--no-pointer`, `--sources`, `--source-dir`, and `--unlock`.

6. **Comprehensive Verification Suite (`tests/test_bootstrap_and_wave_streaming.py`):**
   - Test 1: `run.py --stage bootstrap` end-to-end (`< 3s`, zero PNGs, lean specs, pointer work orders, active lockfile, lock release on unlock).
   - Test 2: `pointer=True` default across `dispatch_cta`, `dispatch_authors`, `dispatch_judges` + `--no-pointer` backward compatibility.
   - Test 3: `.venv` Python auto-resolution, `delta_manifest.json` injection, and `ROLE_SPECS` isolation.
   - Test 4: `dispatch_authors --wave 1` vs `--wave 2` filtering + `run.py --stage wave-status` printing `<= 5` lines.
   - Test 5: `judge.py` `crc32` per-item option shuffle producing uniform distribution across `A..G` + coherent `judge_XX.json` instructions + `--ready-only` incremental judge streaming.
   - Test 6: `cap_stdout_to_log` utility capping console output at `<= 1500 bytes` while persisting full verbose output to disk.

7. **Test Results:**
   - `tests/test_bootstrap_and_wave_streaming.py`: 6/6 passed (100%).
   - `tests/test_c2c_v321_comp3_dispatch.py`: 7/7 passed (100%).
   - `tests/test_pipeline_reparations.py`: 18/18 passed (100%).
   - `tests/test_orchestration_resilience.py`: 16/16 passed (100%).
   - `tests/test_dispatch_scope.py`: 11/11 passed (100%).
   - `tests/test_c2c_v31_adversarial_plan.py`: 12/12 passed (100%).
   - Total battery: **70 passed, 0 failures, 0 warnings** in 5.65s.
