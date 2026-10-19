# Dispatch: Gate 1 Stream C (Orchestration, Watchdog & Evaluation Worker)

## Identity
- Role: Stream C Implementation Worker (Orchestration, Watchdog & Evaluation)
- Type: teamwork_preview_worker
- Working Directory: d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/worker_stream_c/
- Parent Conversation ID: e831bfe5-b034-48b8-9c7e-f1ebfdfd3200

## Scope & Requirements
1. **R5 (P4 Director Pointer Prompts & Budget Watchdog)**:
   - Pointer-Prompt Protocol in `dispatch.py`:
     - Lean static system prompts (<= 5 KB) containing role and hard rules.
     - Ultra-compact (~300 B) dynamic work orders referencing disk JSON payloads (`work/dispatch/items/author_XX.json` or `judge_XX.json`).
     - Director never types large work orders into `invoke_subagent.Prompt`.
   - Swift-Dispatch SLA (<= 20 seconds from dispatch command completion to `invoke_subagent`):
     - `dispatch.py` prints ready-made `Subagents` JSON array (TypeName, Role, Model flash, Prompt) ordered heaviest unit first.
     - Stage 0 overlap: run prepare and define-types concurrently.
   - Pre-Stage-5 Cleanup:
     - `manage_subagents(kill_all)` prior to Stage 5 to clear stale errored entries.
   - Automated Budget Watchdog (`budget_guard.py`):
     - Reads live `transcript.jsonl` of active subagents.
     - Flags runaway subagents exceeding 40 turns, 5M tokens, or looping on tool scripts (`compile_shard.py`, `check_cta.py`).
     - Supports killing and re-dispatching repair subagents for unfinished units.
   - Stateful Resumption Checkpoints:
     - Checkpoint each stage into `work/state.json` to handle 429/404 API rate limits seamlessly.
2. **R6.2 (P6 Judge Native Batching & Blind Re-dispatch)**:
   - Native Batch Slicing in `dispatch.py` (`dispatch-judges`):
     - Slices blind judge evaluations at <= 12 items per batch (`judge_batch_NN.json`).
     - Flag `--max-items-per-judge` default 12.
     - Ensures judges stay blind (no ground truth in item files).
   - Incomplete Evaluation Detection in `judge.py`:
     - Detects truncated or missing responses (`judge_responses_XX.json`).
     - Automatically emits re-dispatch items for only missing IDs.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## 2026-10-19T04:22:02Z
You are the Stream C Implementation Worker (Orchestration, Watchdog & Evaluation).
Your working directory is: d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/worker_stream_c/

You MUST read and follow:
1. d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/ORIGINAL_REQUEST.md (under header ## 2026-10-19T03:49:57Z)
2. d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/worker_stream_c/DISPATCH.md
3. d:/Augusto/Downloads/c2c_hardening_plan.md (§5 P4 and P6)
4. d:/Augusto/personal_portfolio/Tops_academy/reports/c2c_audits/master_forensic_synthesis_7_runs.md (§3.4, §3.5)

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Your write boundaries:
- .agents/skills/content-to-course/dispatch.py
- .agents/skills/content-to-course/judge.py
- .agents/skills/content-to-course/budget_guard.py (NEW)
- .agents/skills/content-to-course/system_prompts/ (lean prompt refactor)
- tests/test_orchestration_resilience.py (NEW)

Key Objectives:
1. R5 (P4 Director Pointer Prompts & Budget Watchdog):
   - Pointer-Prompt Protocol in dispatch.py:
     * Lean static system prompts (<= 5 KB) containing role and hard rules.
     * Ultra-compact (~300 B) dynamic work orders referencing disk JSON payloads (work/dispatch/items/author_XX.json or judge_XX.json).
     * Director never types large work orders into invoke_subagent.Prompt.
   - Swift-Dispatch SLA (<= 20 seconds from dispatch command completion to invoke_subagent):
     * dispatch.py prints ready-made Subagents JSON array (TypeName, Role, Model flash, Prompt) ordered heaviest unit first.
   - Pre-Stage-5 Cleanup:
     * manage_subagents(kill_all) prior to Stage 5 to clear stale errored entries.
   - Automated Budget Watchdog (budget_guard.py):
     * Reads live transcript.jsonl of active subagents.
     * Flags runaway subagents exceeding 40 turns, 5M tokens, or looping on tool scripts (compile_shard.py, check_cta.py).
     * Supports killing and re-dispatching repair subagents for unfinished units.
   - Stateful Resumption Checkpoints:
     * Checkpoint each stage into work/state.json to handle 429/404 API rate limits seamlessly.
2. R6.2 (P6 Judge Native Batching & Blind Re-dispatch):
   - Native Batch Slicing in dispatch.py (dispatch-judges):
     * Slices blind judge evaluations at <= 12 items per batch (judge_batch_NN.json).
     * Flag --max-items-per-judge default 12.
     * Ensures judges stay blind (no ground truth in item files).
   - Incomplete Evaluation Detection in judge.py:
     * Detects truncated or missing responses (judge_responses_XX.json).
     * Automatically emits re-dispatch items for only missing IDs.
   - Add unit tests in tests/test_orchestration_resilience.py:
     * Test pointer prompt generation (<=300 B prompt header, <=5 KB system prompt).
     * Test judge batch slicing at <=12 items.
     * Test budget_guard.py runaway detection.
     * Test state.json checkpointing and resumption.

Targeted test execution:
Run: python -m pytest tests/test_orchestration_resilience.py -v
Ensure all tests pass. Write handoff.md and send_message to parent orchestrator.
