# DISPATCH: Stream 3A — Final Integration Implementer (`impl_3a`)

- **Orchestrator Conversation ID (`Recipient` for `send_message`):** `d0ce22db-904e-4856-b353-59975bfb5874`
- **Teamwork Directory (Governance Docs):** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_3a_impl`
- **Exclusive Production/Test/Report Write Boundaries:**
  1. `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/subagent_types.json`
  2. `d:/Augusto/personal_portfolio/Tops_academy/tests/test_forensic_replay_ab30cf91.py` *(new)*
  3. `d:/Augusto/personal_portfolio/Tops_academy/reports/c2c_audits/CERTIFICACION_HARDENING_C2C_V33.md` *(new)*
  4. `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/check_templates.py` *(authorized in Tier A Escalation #5: deduplicate `seed={seed_val}` in `raw_inv_failures[canon_key][1]` at lines 2066–2086 so `test_c2c_error_aggregation.py` passes untouched)*
  5. `d:/Augusto/personal_portfolio/Tops_academy/tests/test_c2c_solow2_architectural_improvements.py` *(authorized in Tier A Escalation #5: line 1169 `pointer=False` / `item_files[0]` alignment)*
  6. `d:/Augusto/personal_portfolio/Tops_academy/tests/test_c2c_v321_multi_instance_and_append.py` *(authorized in Tier A Escalation #5: line 72 `pointer=False` / `item_files[0]` alignment)*
  7. `d:/Augusto/personal_portfolio/Tops_academy/tests/test_engine_invariants_adversarial.py` *(authorized in Tier A Escalation #5: line 1404 TPL-VAR message alignment including `'@var@'`)*

> **CRITICAL RULES:**
> - **DO NOT** create `.agents/hooks.json` yourself (the Orchestrator will activate `.agents/hooks.json` from `.agents/hooks.template.json` at the very end of Stage 3 after all subagent code/tests are audited!).
> - **DO NOT** leave any active `.c2c_subagent_lock.json` inside `REPO_ROOT` (`courses/*` or `work*/`) — all test runs MUST output to `tmp_path`!
> - **NEVER** pass `ArtifactMetadata` when calling `write_file` or `edit_file`.
> - If running the full repository `pytest` suite uncovers ANY cross-stream edge case in a Stage 1 or Stage 2 file, escalate via `BLOCKER::` to Orchestrator `d0ce22db-904e-4856-b353-59975bfb5874` (Tier A) before touching files outside your boundary.

## Step 0: Mandatory Pre-Flight Sanity Check
Inspect `dispatch.py` (`generate_define_subagent_specs` / how `subagent_types.json` is built or synchronized), check `content/` for the real Greene PDFs used in `ab30cf91` (and `courses/asyntotic_estatistics_v2.json`), and inspect `tests/test_skill.py` or any test referencing `subagent_types.json`. Write `stream_3a_impl/BRIEFING.md` before editing.

## Scope of Implementation (Global Sync + 8-Vector Forensic Replay `ab30cf91` + Full Repo Certification)

### 1. Synchronize `.agents/skills/content-to-course/subagent_types.json`
- Regenerate `.agents/skills/content-to-course/subagent_types.json` using the official generator in `dispatch.py` so all 4 C2C subagent types (`c2c_cta_architect`, `c2c_shard_author`, `c2c_blind_judge`, `c2c_repair`) reflect the hardened v3.3 system prompts from Stage 2B with 100% parity.

### 2. Build `tests/test_forensic_replay_ab30cf91.py` (Deterministic `< 10s` Suite on Real `ab30cf91` Vectors)
Implement 8 explicit, non-mocked forensic tests (`V1..V8`, all writing temporary artifacts strictly inside `tmp_path`):
- **V1 (`bootstrap` Zero-Raster Multi-PDF & `stdout <= 1.5 KB`):** Run `run.py --stage bootstrap` against the 2 real Greene PDFs in `content/` (or skipping gracefully ONLY if `content/` PDFs are absent, though verify they exist first — they are in workspace `content`!) outputting to `tmp_path / "work"`. Assert execution completes in `< 3.0s`, `0` PNG files created, `0` unrelated PDFs from `content/` ingested, `stdout <= 1500` bytes, `work/dispatch/types/*.json` lean specs (`<= 5 KB` prompts) exist, `cta_work_orders.json` uses compact pointers, and `work/.c2c_subagent_lock.json` is active and valid.
- **V2 (`part_01` `PATCH_LEDGER_ALERT` Zero False Rejection):** Compile a CTA candidate containing real Greene orphan math expressions (`Q_{zx}^{-1}`, `(Z'X)^{-1}`, `\sqrt{n}(\hat{\beta} - \beta) \xrightarrow{d} \mathcal{N}(0, V)`). Assert `degraded_pct == 0.0` (classified strictly as `healed` over real `total_evaluated_fields`), compiling cleanly on Attempt #1.
- **V3 (`--append` End-to-End Continuous IDs & Base Prerequisites):** Simulate `prepare --append` against a base course (`H-01..H-04`, `C-01..C-18`, `Hab-01..Hab-10`) -> `dispatch_cta` -> `compile_cta` -> `check_cta` -> `cta_merge`. Assert `dispatch_cta` injects `next_ids_by_prefix` (`H: 5, C: 19, Hab: 11`) + `existing_competencies_outline`, new competencies referencing base `C-01` pass DAG validation, and merged IDs start at `H-05 / C-19 / Hab-11` without resetting to `01`.
- **V4 (`plan_shards` Weighted Isolation on 32 Greene Competencies):** Run `plan_shards` on the 32 competencies of `courses/asyntotic_estatistics_v2.json` (10 `Hab`, 18 `C`, 4 `H`). Assert all 10 `Hab-*` skills are **100% isolated (`1 Hab/shard`)** and placed at the front of `Wave 1` (`wave_index == 1`, `max_wave_size == 10`).
- **V5 (`shard_06` KaTeX `@var@` Sandwich Matrix + `{delta}` Placeholder Block):**
  - Instantiate an IV/2SLS sandwich matrix template using raw strings `r"..."` + `@a11@`, `@k_dim@`, `\xrightarrow{d}`, `\mathbb{R}^{k}` with single-letter vars `{"d": 2, "k": 3, ...}` -> assert 0 `R-20` / invariant errors.
  - Compile/validate a broken template leaking uninterpolated `{delta}` or `@delta@` (the exact `Judge 04` `Hab-04` bug of `ab30cf91`) -> assert deterministic hard block BEFORE Stage 5!
- **V6 (`shard_08` Zero-Disk-Mutation + `shard_fixes/C-08.py` + `shard_13` Circuit Breaker):**
  - Verify failed compilation leaves `shard_08_data.py` byte-for-byte unchanged on disk.
  - Write a modular override `work/shards/shard_fixes/C-08.py` and verify `compile_shard.py` splices it cleanly and compiles `C-08.json`.
  - Verify identical broken re-runs return `[NO-CHANGE]` without advancing `distinct_compiles`, while 3 distinct edits producing the same normalized `err_hash` trip `[CIRCUIT BREAKER]`.
- **V7 (Dual `c2c_hook_guard.py` + `budget_guard.py` 108-Turn `PLANNER_RESPONSE` Watchdog):**
  - With a lockfile in `tmp_path`, verify `c2c_hook_guard.process_hook` DENIES worker reads of `compile_shard.py` and shell `Get-Content` bypasses, DENIES Director reads/edits of `shard_06_data.py` / `shard_fixes/C-08.py` / `judge_responses_01.json`, ALLOWS Director `run.py` & `state.json`, and ALLOWS everything in `< 15ms` when no active lock exists.
  - Feed a synthetic transcript with 108 `"type": "PLANNER_RESPONSE"` steps (matching `shard_06`'s real `ab30cf91` schema) to `budget_guard.py` and assert straggler detection + `c2c_repair` order targeting `shard_fixes/`.
- **V8 (`judge.py` Cryptographic Option Shuffle + Coherent Pointer Mode):**
  - Run `generate_judge_batch` + `dispatch_judges(pointer=True)` across >= 35 MC7 items (or templates derived from `asyntotic_estatistics_v2`). Assert uniform letter distribution across `A..G` (no single letter `> 35%`, eliminating the 100%-`B`/`C` clustering of `ab30cf91`) and zero `"NO EJECUTES view_file"` contradiction inside `judge_XX.json`.

### 3. Run the ENTIRE Repository `pytest` Suite & Emit Certification Report
- Execute `& "d:\Augusto\personal_portfolio\Tops_academy\.venv\Scripts\python.exe" -m pytest tests -q` and record exact total passed/skipped/time.
- Write `reports/c2c_audits/CERTIFICACION_HARDENING_C2C_V33.md` in Spanish documenting:
  - Executive summary of C2C v3.3 architecture & SLAs (`<= 60–90s` initialization, `~12–16` Director turns, 100% bottleneck closure `#1–#13` + Milestones 3, 4, 7).
  - Traceability matrix mapping every bottleneck (`#1..#13`) and every `ab30cf91` error category (`1..12`) to the exact files modified and tests (`V1..V8` + stream suites) proving resolution.
  - Full repository `pytest` metrics and execution time of `test_forensic_replay_ab30cf91.py`.

Write `progress.md` and `handoff.md` in `stream_3a_impl/`, and `send_message` `DONE:: stream_3a_impl | ...` to `d0ce22db-904e-4856-b353-59975bfb5874`.
