# Original Request & Approved /grill-me Decisions — C2C v3.3 Pipeline Hardening

## User Mandate
1. Contrast `reports/c2c_audits/ANALISIS_DETALLADO_BOTTLENECKS_Y_TIEMPOS_ETAPAS_C2C.md` with `FUTURE_MILESTONES.md`, `/google-antigravity-sdk`, and `/content-to-course`.
2. Close **100% of efficiency bottlenecks (#1–#13)** at once, including:
   - **Initialization SLA:** Reduce from 4–6+ minutes down to **<= 60–90 seconds** (Zero-Raster PDF ingest, multi-PDF `sources` fix, single `run.py --stage bootstrap` CLI command with silent `lean=True` specs and `pointer=True` default).
   - **Director Conversation Oversaturation:** Eliminate the 84-turn / 18.4-min CLI bloat of `ab30cf91` (`pointer=True` universal default, `stdout <= 1.5 KB` cap with verbose logs in `work/logs/`, Silent Reactive Barrier Protocol on partial `DONE` wakeups, and `PreToolUse` hook preventing Director from reading/editing `*_data.py`).
   - **KaTeX-Python Decoupling:** PrairieLearn orthogonal `@var@` / `@var:fmt@` tokens in raw strings `r"..."` across `MC7`, `FIB`, `MS`, `hints`, and `solution`, keeping `{var}` backward-compatible, banning `rf"..."`, and blocking uninterpolated `@ident@` / `{key}` placeholders.
   - **Shard Compiler & Authoring Hardening:** Unified SHA-256 `(source_sha256, err_hash)` circuit breaker (`same_error_streak >= 3` or `distinct_compiles > 10`, idempotent `[NO-CHANGE]`), Zero-Disk-Mutation on failed compiles, modular overrides `work/shards/shard_fixes/<CID>.py`, surgical `TPL-VAR`/`R-16` diagnostics (zero fake text padding in `calibrate_option_lengths`).
   - **Weighted Sharding (Milestone 7.4):** Max **1 `Skill` (`Hab-*`) isolated per shard**, `Concept`/`Fact` in contiguous groups of 2 (up to 3 `Fact` when `N >= 30`), ordered `Heaviest-First` in waves `<= 10`.
   - **Watchdog & Platform Hooks:** Connect `budget_guard.py` to `<appDataDir>/brain/<id>/.system_generated/logs/transcript.jsonl` (`PLANNER_RESPONSE`), conditional `.agents/hooks.json` (`c2c_hook_guard.py`) active only during live C2C lockfile runs.
   - **Forensic Closure Bundle:** `judge.py` per-item cryptographic option shuffle `crc32(template_id:idx:seed)` + coherent Pointer Mode (`judge_XX.json` allowed read), `patch_ledger.py` separating deterministic LaTeX `healed` from semantic `degraded` over real `total_evaluated_fields`, end-to-end `--append` (`delta_manifest.json` wired through `dispatch_cta`, `compile_cta`, `cta_merge`), `delete_course.py` regression test on `work_append/`, and `.venv/Scripts/python.exe` + `PYTHONPATH` auto-resolution.
3. **Methodology (`/teamwork-preview` + Flash Triads):**
   - Orchestrator = High-reasoning model (Dispatch-Only & Escalation Resolver).
   - Every stream runs `Implementador -> Mejorador -> Auditor` using `Model="flash"`.
   - Mandatory Pre-Flight Sanity Check & 2-tier `BLOCKER::` escalation protocol.

## Baseline Git Status Prior to Stage 1
Pre-existing modified/untracked files before C2C v3.3 teamwork began:
- Modified: `compile_shard.py`, `dispatch.py`, `plan_shards.py`, `run.py`, `subagent_types.json`, `system_prompts/lean/prompt_shard_author.md`, `system_prompts/prompt_shard_author.md`, `reports/c2c_audits/*`, `tests/test_compile_shard.py`.
- Untracked: `courses/asyntotic_estatistics_v2.json`, `courses/competence_analysis_asyntotic_estatistics_v2.md`, `docs/future_milestones/`, `reports/**`, `test_out/`, `test_shard_02.json/`, `tests/test_c2c_case_2b_mastery.py`.
