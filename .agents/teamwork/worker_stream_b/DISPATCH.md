# Dispatch: Gate 1 Stream B (Template Engine & Author Pipeline Worker)

## Identity
- Role: Stream B Implementation Worker (Template Engine & Author Pipeline)
- Type: teamwork_preview_worker
- Working Directory: d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/worker_stream_b/
- Parent Conversation ID: e831bfe5-b034-48b8-9c7e-f1ebfdfd3200

## Scope & Requirements
1. **R2 (P1 Stage 3 Diagnostics, Tool Isolation & Circuit Breakers)**:
   - Tool Isolation:
     - Forbid author subagents from reading `compile_shard.py` in `dispatch.py` (remove from READ-allowed, add to PROHIBIDO).
   - Diagnostics Enhancement (`check_templates.py` `TPL-DRY`):
     - Print first failing seed, parameters, `type(exc).__name__: str(exc)`, and last 3 call frames mapped to `shard_XX_data.py` lines (`_format_dry_failure`).
   - Stateful SHA-256 Circuit Breaker in `check_templates.py`:
     - Store `{attempts, last_hash, halted}` with SHA-256 of competency source.
     - Changed hash is re-evaluated; pass clears the halt. Same-hash repeat failures trigger terminal STOP: "STOP, send_message the Director".
   - Bounded Compilation in `compile_shard.py`:
     - Print `[COMPILE n/6]` and terminal STOP at limit.
     - Graceful missing-file error handling: a `.py` input that does not exist returns a clear error and never calls `mkdir`. Infer `shard_id` and `work_dir` from path.
   - Standardize author prompt (`prompt_shard_author.md`):
     - Canonical 15-line template pattern.
     - Enforce parameter space >= 500 combinations.
     - Forbid reading other `shard_*_data.py`.
2. **R6.1 (P5 Author Adaptive Sizing & Syntax Normalization)**:
   - Dynamic Shard Sizing in `plan_shards.py`:
     - `comps_per_shard = clamp(ceil(N / 8), 2, 6)` with up to 8 concurrent authors.
   - Syntax Normalization in `compile_shard.py` and `assemble.py`:
     - Normalize non-variable double curly braces (`{{token}}` -> `{token}`) when `token` is not a variable before R-20 validation.
   - Add unit tests in `tests/test_latex_engine.py` and `tests/test_compile_shard.py`.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## 2026-10-19T04:22:02Z
You are the Stream B Implementation Worker (Template Engine & Author Pipeline).
Your working directory is: d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/worker_stream_b/

You MUST read and follow:
1. d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/ORIGINAL_REQUEST.md (under header ## 2026-10-19T03:49:57Z)
2. d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/worker_stream_b/DISPATCH.md
3. d:/Augusto/Downloads/c2c_hardening_plan.md (§5 P1 and P5)
4. d:/Augusto/personal_portfolio/Tops_academy/reports/c2c_audits/master_forensic_synthesis_7_runs.md (§3.3)

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Your write boundaries:
- .agents/skills/content-to-course/check_templates.py
- .agents/skills/content-to-course/compile_shard.py
- .agents/skills/content-to-course/plan_shards.py
- .agents/skills/content-to-course/system_prompts/prompt_shard_author.md
- tests/test_latex_engine.py (NEW)
- tests/test_compile_shard.py

Key Objectives:
1. R2 (P1 Stage 3 Diagnostics, Tool Isolation & Circuit Breakers):
   - Tool isolation:
     * Forbid author subagents from reading compile_shard.py or check_templates.py in prompt_shard_author.md and dispatch.py (mark as PROHIBIDO).
   - Diagnostics enhancement in check_templates.py (TPL-DRY):
     * Helper _format_dry_failure: print first failing seed, parameters, type(exc).__name__: str(exc), and last 3 traceback frames mapped to shard_XX_data.py source lines.
   - Stateful SHA-256 Circuit Breaker in check_templates.py:
     * Store {attempts, last_hash, halted} with SHA-256 of competency source.
     * Changed hash is re-evaluated; pass clears the halt. Same-hash repeat failures trigger terminal STOP: "STOP, send_message the Director".
   - Bounded compilation in compile_shard.py:
     * Print [COMPILE n/6] and terminal STOP at limit.
     * Graceful missing-file error handling: a .py input that does not exist returns a clear error and never calls mkdir. Infer shard_id and work_dir from path.
   - Standardize author prompt (prompt_shard_author.md):
     * Canonical 15-line template pattern.
     * Enforce parameter space >= 500 combinations.
     * Forbid reading other shard_*_data.py.
2. R6.1 (P5 Author Adaptive Sizing & Syntax Normalization):
   - Adaptive Shard Sizing in plan_shards.py:
     * comps_per_shard = clamp(ceil(N / 8), 2, 6) with up to 8 concurrent authors.
   - Syntax Normalization in compile_shard.py:
     * Normalize non-variable double curly braces ({{token}} -> {token}) when token is not a declared variable, before R-20 validation.
   - Add unit tests in tests/test_latex_engine.py:
     * Test \frac{S_{xy}}{S_{xx}}, K^{0.5}, \operatorname{arccot}, {alpha} substitution, {{0.5}} normalization.
   - Update tests/test_compile_shard.py to cover missing-file handling, [COMPILE n/6], and dry-run diagnostics.

Targeted test execution:
Run: python -m pytest tests/test_latex_engine.py tests/test_compile_shard.py -v
Ensure all tests pass. Write handoff.md and send_message to parent orchestrator.
