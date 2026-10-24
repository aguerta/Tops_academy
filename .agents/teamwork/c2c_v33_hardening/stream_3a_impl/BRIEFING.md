# BRIEFING: Stream 3A Pre-Flight Sanity Check & Architecture Alignment

**Role:** Stream 3A Implementer (`impl_3a`)  
**Date:** 2026-10-24  
**Workspace:** `d:/Augusto/personal_portfolio/Tops_academy`  
**Teamwork Directory:** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_3a_impl`  

---

## 1. Pre-Flight File Verification & Signatures

### 1.1 Production & Target Files
- **`subagent_types.json`**: Located at `.agents/skills/content-to-course/subagent_types.json`. Currently 87,078 bytes containing outdated v3.21 prompt strings. `dispatch.get_type_definitions(lean=False)` returns the 4 canonical subagent definitions (`c2c_cta_architect`, `c2c_shard_author`, `c2c_judge`, `c2c_repair`) with full v3.3 system prompts from `system_prompts/*.md`.
- **`courses/asyntotic_estatistics_v2.json`**: Verified present (32 competencies: 10 `Hab-*`, 16 `C-*`, 6 `H-*`). Used for V4 and V8.
- **`content/estadistica_asintotica/`**: Verified present containing both real Greene PDFs used in `ab30cf91`:
  1. `ECONOMETRIC ANALTYSIS FIFTH EDITION  -  William H_ Greene ... -93.pdf` (1.49 MB)
  2. `Econometric Analysis (Greene) ... -923-946.pdf` (2.1 MB)
- **`tests/test_forensic_replay_ab30cf91.py`**: New target file for the 8 forensic vectors V1..V8.
- **`reports/c2c_audits/CERTIFICACION_HARDENING_C2C_V33.md`**: New target certification report.

---

## 2. Pre-Flight Baseline Test Suite Analysis

Executing `& "d:\Augusto\personal_portfolio\Tops_academy\.venv\Scripts\python.exe" -m pytest tests -q` resulted in:
**712 passed, 2 skipped, 4 failed in 69.30s**.

The 4 failures are all in pre-existing test files outside Stream 3A Write Boundaries, caused by hardened invariants and contract improvements introduced in Stage 1 & 2:

1. **`tests/test_c2c_error_aggregation.py:83`** (`test_dry_run_invariant_failure_aggregated_into_single_error`):
   - **Conflict**: Test asserts `"semillas 100..149 (50 semillas)" in err`. In `check_templates.py:2066-2085`, `check_unrendered_placeholders_in_instance` and `check_instance_invariants` both register seed failures for the same seed, doubling the count to `100 semillas`.
   - **File**: `check_templates.py` / `tests/test_c2c_error_aggregation.py` (outside write boundary).

2. **`tests/test_c2c_solow2_architectural_improvements.py:1182`** (`test_dispatch_payload_size_subagent_specs_and_cta_mapreduce_full_prompt_integrity`):
   - **Conflict**: Test asserts `'granularity' in direct_prompt.lower()`. Stream 2A/1B made `pointer=True` the universal default for `dispatch_cta`, producing a compact pointer prompt (`Work order: cta_01.json. Read with view_file...`) which delegates granularity to the disk payload.
   - **File**: `tests/test_c2c_solow2_architectural_improvements.py` (outside write boundary).

3. **`tests/test_c2c_v321_multi_instance_and_append.py:76`** (`test_10_solow_instances_isolated_work_dirs_and_dispatch_paths`):
   - **Conflict**: Test asserts `'--input courses/' in cta_prompt`. Under universal `pointer=True`, the prompt is a concise pointer prompt without CLI flags.
   - **File**: `tests/test_c2c_v321_multi_instance_and_append.py` (outside write boundary).

4. **`tests/test_engine_invariants_adversarial.py:1404`** (`test_tpl_var_missing_placeholder_and_variants`):
   - **Conflict**: Test asserts exact string `"TPL-VAR violation in 'TPL-NO-PLACEHOLDER': stem must contain at least one placeholder '{var}' or 'stem_variants' must be present."`. Stream 1A updated `check_templates.py:2143` to include `'@var@'`.
   - **File**: `tests/test_engine_invariants_adversarial.py` (outside write boundary).

Per Mandatory Execution Protocol Step 0, an escalation `BLOCKER::` will be sent to the Orchestrator regarding these 4 out-of-boundary tests.

---

## 3. Implementation Plan for Stream 3A

### Task 1: Synchronize `subagent_types.json`
- Regenerate `.agents/skills/content-to-course/subagent_types.json` using `dispatch.get_type_definitions(lean=False)`.
- Format as standard formatted JSON array with indent=2, utf-8 encoding.
- Verify 4 subagent types (`c2c_cta_architect`, `c2c_shard_author`, `c2c_judge`, `c2c_repair`) reflect the hardened v3.3 system prompts with 100% parity.

### Task 2: Build `tests/test_forensic_replay_ab30cf91.py`
Implement 8 deterministic, fast (< 10s total runtime) forensic replay tests:
- **`test_v1_bootstrap_zero_raster_multi_pdf_and_stdout_cap`**:
  Execute `run_stage_bootstrap` on the real Greene PDFs in `content/estadistica_asintotica/` outputting to `tmp_path / "work"`. Assert `< 3.0s`, `0` PNGs, only Greene PDFs ingested, `stdout <= 1500` B, `types/*.json` lean prompts `<= 5 KB`, compact pointer work orders, and active lockfile.
- **`test_v2_part_01_patch_ledger_zero_false_rejection`**:
  Execute `compile_cta` or `patch_ledger` against real Greene orphan math expressions (`Q_{zx}^{-1}`, `(Z'X)^{-1}`, `\sqrt{n}(\hat{\beta} - \beta) \xrightarrow{d} \mathcal{N}(0, V)`). Assert `degraded_pct == 0.0`, all healed over `total_evaluated_fields`, compiles cleanly on Attempt #1.
- **`test_v3_append_continuous_ids_and_base_prerequisites`**:
  Simulate `--append` against a base course (`H-01..04`, `C-01..18`, `Hab-01..10`), verify `next_ids_by_prefix` injection, DAG prerequisite preservation, and non-resetting IDs starting at `H-05`, `C-19`, `Hab-11`.
- **`test_v4_plan_shards_weighted_isolation_32_greene_competencies`**:
  Run `plan_shards` on `courses/asyntotic_estatistics_v2.json`. Verify 10 `Hab-*` are 100% isolated (1 per shard), placed at the front of `Wave 1` (`wave_index == 1`, `max_wave_size == 10`).
- **`test_v5_shard_06_katex_sandwich_and_delta_placeholder_block`**:
  Instantiate IV/2SLS sandwich matrix with `@var@` and single-letter math vars (`d`, `k`, `\xrightarrow{d}`, `\mathbb{R}^k`). Verify 0 R-20 errors. Then verify broken template leaking uninterpolated `{delta}` or `@delta@` is deterministically blocked.
- **`test_v6_shard_08_zero_disk_mutation_and_shard_fixes_and_circuit_breaker`**:
  Verify failed compilation leaves data file untouched. Write `shard_fixes/C-08.py` and verify `compile_shard.py` splices cleanly. Verify `[NO-CHANGE]` on identical reruns and `[CIRCUIT BREAKER]` on 3 identical error hashes.
- **`test_v7_dual_hook_guard_and_budget_guard_planner_response`**:
  Verify `c2c_hook_guard.process_hook` permissions under lockfile (worker denied `compile_shard.py` reads and shell bypasses, Director denied raw shard data and raw judge responses, Director allowed `run.py` and `state.json`, fast allow when no lock). Feed 108 `PLANNER_RESPONSE` transcript steps to `budget_guard.py` and verify straggler detection.
- **`test_v8_judge_option_shuffle_and_coherent_pointer_mode`**:
  Run `generate_judge_batch` and `dispatch_judges(pointer=True)` across >= 35 MC7 items. Assert uniform distribution across A..G (no single letter > 35%) and no contradictory read bans.

### Task 3: Full Repository Pytest & Certification Report
- Run all tests.
- Produce `reports/c2c_audits/CERTIFICACION_HARDENING_C2C_V33.md`.
