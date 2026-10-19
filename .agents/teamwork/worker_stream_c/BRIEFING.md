# BRIEFING — 2026-10-19T05:05:00Z

## Mission
Implement Stream C (Orchestration, Watchdog & Evaluation) for the Content-to-Course (C2C) hardening: Pointer-Prompt Protocol, Swift-Dispatch SLA, Pre-Stage-5 Cleanup, Automated Budget Watchdog (budget_guard.py), Stateful Resumption Checkpoints (state.json), Judge Native Batching (<=12 items), Incomplete Evaluation Detection & Blind Re-dispatch, and comprehensive resilience tests.

## 🔒 My Identity
- Archetype: teamwork_preview_worker
- Roles: implementer, qa, specialist
- Working directory: d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/worker_stream_c/
- Original parent: e831bfe5-b034-48b8-9c7e-f1ebfdfd3200
- Milestone: Gate 1 Stream C

## 🔒 Key Constraints
- Write boundaries:
  - `.agents/skills/content-to-course/dispatch.py`
  - `.agents/skills/content-to-course/judge.py`
  - `.agents/skills/content-to-course/budget_guard.py` (NEW)
  - `.agents/skills/content-to-course/system_prompts/` (lean prompt refactor)
  - `tests/test_orchestration_resilience.py` (NEW)
- MANDATORY INTEGRITY MANDATE: Genuine implementation, no cheating, no hardcoded bypasses, no dummy facades.
- Tests must pass via `python -m pytest tests/test_orchestration_resilience.py -v`.
- Follow Handoff Protocol with 5 components.

## Current Parent
- Conversation ID: e831bfe5-b034-48b8-9c7e-f1ebfdfd3200
- Updated: 2026-10-19T04:22:02Z

## Task Summary
- **What to build**:
  1. R5: Pointer-Prompt Protocol in dispatch.py (lean system prompts <= 5 KB, pointer dynamic work orders ~200 B <= 300 B).
  2. R5: Swift-Dispatch SLA (ready-made Subagents JSON array, heaviest unit first).
  3. R5: Pre-Stage-5 Cleanup protocol (`manage_subagents(kill_all)` & state.json error purging).
  4. R5: Automated Budget Watchdog (`budget_guard.py`): reads live `transcript.jsonl`, flags runaway subagents (>40 turns, >5M tokens, or script-looping), kill & re-dispatch repair subagent for unfinished units.
  5. R5: Stateful Resumption Checkpoints (`work/state.json`) for seamless 429/404 handling.
  6. R6.2: Native Batch Slicing in `dispatch.py` and `judge.py` (`dispatch-judges`, <= 12 items per batch, `--max-items-per-judge` default 12, judges double-blind).
  7. R6.2: Incomplete Evaluation Detection in `judge.py` (`judge_responses_XX.json` validation, auto emit re-dispatch items for missing IDs).
  8. Automated test suite in `tests/test_orchestration_resilience.py`.
- **Success criteria**:
  - All resilience tests pass cleanly with pytest (16/16 passed).
  - All regression tests pass cleanly (30/30 passed).
  - Zero hardcoding or fake mocks.
  - Auditor verification ready.
- **Interface contracts**: `c2c_hardening_plan.md` (§5 P4, P6), `master_forensic_synthesis_7_runs.md` (§3.4, §3.5).
- **Code layout**: Source in `.agents/skills/content-to-course/`, tests in `tests/test_orchestration_resilience.py`, metadata in `.agents/teamwork/worker_stream_c/`.

## Key Decisions Made
- Created 5 lean static system prompts under `.agents/skills/content-to-course/system_prompts/lean/` (each 1.6 KB to 3.6 KB, strictly <= 5 KB) while preserving original full prompts for backward compatibility.
- Implemented `make_pointer_prompt` with dynamic work order reference and strict done signal (~200 B <= 300 B limit).
- Built `budget_guard.py` with standalone CLI and API to parse transcripts, enforce turn/token/script limits, generate repair re-dispatch for unfinished competencies, and manage `state.json` checkpoints.
- Enhanced `judge.py` with `split_judge_batch` (batch size <= 12), `check_judge_completeness` (detecting truncated responses and missing item IDs across diverse schema formats), and `emit_judge_redispatch` (slicing only missing IDs into blind batches).
- Added `pre_stage5_cleanup` to purge transient 429/aborted subagents before Stage 5 verification.

## Artifact Index
- `.agents/skills/content-to-course/budget_guard.py` — Automated Budget Watchdog and state checkpointing
- `.agents/skills/content-to-course/dispatch.py` — Dispatcher with Pointer-Prompt Protocol, Swift-Dispatch SLA, and Native Judge Slicing
- `.agents/skills/content-to-course/judge.py` — Judge batch splitting (<= 12 items), completeness checking, and re-dispatch generation
- `.agents/skills/content-to-course/system_prompts/lean/` — 5 lean static system prompts (<= 5 KB)
- `tests/test_orchestration_resilience.py` — Comprehensive resilience test suite (16 tests)

## Change Tracker
- **Files modified**:
  - `.agents/skills/content-to-course/dispatch.py`: Added pointer prompts, lean type definitions, heaviest unit first sorting, judge batch slicing, CLI flags/subcommands, and pre-stage-5 cleanup.
  - `.agents/skills/content-to-course/judge.py`: Added items_per_judge=12 default, list/Path polymorphic split_judge_batch, check_judge_completeness, and emit_judge_redispatch with Subagents generation.
  - `.agents/skills/content-to-course/budget_guard.py`: NEW automated budget watchdog module with transcript monitoring and state checkpointing.
  - `.agents/skills/content-to-course/system_prompts/lean/*`: 5 NEW lean static system prompts <= 5 KB.
  - `tests/test_orchestration_resilience.py`: NEW test suite with 16 comprehensive resilience tests.
- **Build status**: All 30 tests PASSED (0.47s)
- **Pending issues**: None

## Quality Status
- **Build/test result**: 16/16 resilience tests PASSED, 30/30 full suite PASSED
- **Lint status**: Clean (Python py_compile clean, strict typed contracts)
- **Tests added/modified**: 16 tests in `tests/test_orchestration_resilience.py`

## Loaded Skills
- None explicitly loaded as external skills; C2C skill in repo being modified.
