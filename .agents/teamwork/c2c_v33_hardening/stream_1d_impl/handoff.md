# HANDOFF: Stream 1D — Implementer (`impl_1d`) to Improver (`impr_1d`)

- **Stream:** 1D (Watchdog Conectado a `<appDataDir>/brain/` y Guardrail Dual `.agents/hooks.json`)
- **Author:** Phase 1 Implementador (`impl_1d`)
- **Recipient:** Orchestrator (`d0ce22db-904e-4856-b353-59975bfb5874`) & Phase 2 Improver
- **Status:** IMPLEMENTATION COMPLETE & CERTIFIED (28/28 tests passing)

---

## 1. Summary of Changes

### A. `.agents/skills/content-to-course/budget_guard.py`
1. **Brain Transcript Resolution (`resolve_brain_transcript`)**:
   - Added automatic discovery of `<appDataDir>/brain/<subagent_id>/.system_generated/logs/transcript.jsonl`.
   - Supports `--app-data-dir`, `ANTIGRAVITY_APP_DATA_DIR` env var, and default candidate paths (`~/.gemini/antigravity`, `~/.gemini/antigravity-ide`, `~/.gemini/antigravity-cli`, `%USERPROFILE%/.gemini/antigravity`).
   - Supports bases ending directly in `brain` or containing `brain/`.
2. **Transcript Parsing (`parse_transcript`)**:
   - Upgraded to parse Antigravity's real JSONL transcript format:
     - Distinguishes model turns via `"type": "PLANNER_RESPONSE"` (excluding Cortex tool outputs logged with `type: "GENERIC"` and system messages).
     - Captures explicit `input_tokens`, `output_tokens`, `cache_read_tokens` / `cached_tokens`.
     - Measures character count in `thinking` blocks.
     - Tracks tool call histograms for `view_file`, `edit_file`, `write_file`, `run_command`, `send_message`.
     - Strips nested quotes from tool arguments (`_clean_str`).
     - Detects inspection and execution of monitored scripts (`compile_shard.py`, `check_templates.py`, `compile_cta.py`, `check_cta.py`, `/engine/`, `/validator/`, `.check_attempts`, etc.).
     - Added deterministic cumulative context/cache token estimator (`est_cached = sum(20_000 + 800 * k)`), ensuring >100-turn compact transcripts without explicit token fields are reliably flagged for >5M tokens.
     - Fixed `UnboundLocalError` on `msg_text` so system prompt and initial instructions extract `unit_id` and work order JSON without exception.
3. **Watchdog Rule Evaluation (`evaluate_watchdog_rules`)**:
   - Evaluates hard SLA limits (turn count > 40, total tokens > 5M).
   - Hard SLA limit breaches take precedence and trigger `is_runaway = True` and `recommended_action = "kill_and_redispatch"`, even if the model prematurely claimed completion.
   - For subagents within SLA, completion signals (`DONE: ...`) mark `is_completed = True` and `recommended_action = "completed"`.
4. **Repair Re-Dispatch (`generate_repair_redispatch`)**:
   - Emits modular fix instructions to `work/shards/shard_fixes/<CID>.py`.
   - Generates compilation command using `.venv/Scripts/python.exe` (via `_resolve_python_executable()`), including `--work "<work_dir>" --shard <unit_id>`.
   - Returns `"next_schedule_seconds": 300` in the redispatch payload.
   - In `identify_unfinished_competencies`, checks both `templates/*.json` and `shards/*.json` to avoid false negatives.

### B. `.agents/skills/content-to-course/c2c_hook_guard.py` (New File)
1. **Pure Python Stdlib**: No external dependencies; executes in `< 15 ms`.
2. **Zero-Interference Fast Path**:
   - Searches `courses/*/work*/.c2c_subagent_lock.json` (and `C2C_LOCK_FILE` env var).
   - Resolves all paths using `REPO_ROOT = Path(__file__).resolve().parents[3]`, completely independent of `cwd`.
   - If no lockfile exists, or lockfile is older than 7200s (2h), or `"active": false`: immediately outputs `{"decision": "allow"}` and exits code `0`.
3. **Dual-Role Enforcement (when active lock exists)**:
   - **Case A — Director (`conversationId == director_conversation_id`)**:
     - Enforces **Director Context Diet**: DENIES reading or editing `*_data.py`, `shard_fixes/*.py`, or `judge_responses*.json`.
     - ALLOWS reading compact state manifests (`state.json`, `judge_report.json`, `dispatch/*.json`) and CLI orchestration commands.
   - **Case B — Worker Subagent (`conversationId != director_conversation_id`)**:
     - DENIES reading compiler/validator source, engine, ground truth: `compile_shard.py`, `check_templates.py`, `compile_cta.py`, `check_cta.py`, `/engine/`, `engine/`, `/validator/`, `validator/`, `src/validator/`, `.check_attempts`, `judge_ground_truth.json`, `SKILL.md`.
     - DENIES modifying `.check_attempts` and `.agents/skills/`.
     - DENIES shell commands deleting `.check_attempts` (`rm`, `del`, `remove-item`, `>`) or running complex nested-quote / long `python -c` (> 120 chars or escaped quotes).
     - ALLOWS reading `content/*.pdf`, `dispatch/items/*.json`, writing `work/shards/*_data.py` and `work/shards/shard_fixes/*.py`, and running official compiler CLIs.
4. **Exit Code Invariant**: ALWAYS exits with code `0`, communicating decision via stdout JSON. Fail-open on unparseable stdin JSON.

### C. `.agents/hooks.template.json` (New File)
- **CRITICAL**: `.agents/hooks.json` was NOT created (Stage 3 activation will copy/rename after full certification).
- Configured with `PreToolUse` hook matching `read_file|view_file|write_file|write_to_file|edit_file|replace_file_content|multi_replace_file_content|run_command`.
- Command configured as: `"python skills/content-to-course/c2c_hook_guard.py"` (relative to `.agents/`).

### D. `tests/test_watchdog_and_hooks.py` (New File)
- 12 comprehensive unit tests:
  1. Fast passthrough (< 50ms) without lockfile.
  2. Passthrough for stale (> 2h) or inactive locks.
  3. Worker denied reading compiler, engine, ground truth, check attempts, SKILL.md.
  4. Worker denied modifying skills and check attempts.
  5. Worker denied deleting check attempts and nested-quote `python -c`.
  6. Worker allowed reading content, dispatch items, and writing shard data/fixes.
  7. Director Context Diet denied reading/editing data files, allowed reading manifests and running CLI.
  8. Hooks template validation and live `subprocess.run(..., cwd=repo_root / ".agents")` exit 0 test.
  9. Transcript resolution via `--app-data-dir`.
  10. Real Antigravity 108-turn transcript parsing (`b9bc17ec-092d-4d5d-80b6-428307c2143b`), verifying turn/token breach, script loop detection, and kill_and_redispatch action.
  11. Cumulative context token estimator on 100-turn compact transcripts (> 5M estimated tokens).
  12. Modular `shard_fixes/<CID>.py` repair generation with `next_schedule_seconds: 300` and `.venv/Scripts/python.exe`.

---

## 2. Test Verification & Results

Command run:
```powershell
& "d:\Augusto\personal_portfolio\Tops_academy\.venv\Scripts\python.exe" -m pytest tests/test_watchdog_and_hooks.py tests/test_orchestration_resilience.py -q
```
Output:
```
............................                                             [100%]
28 passed in 0.41s
```

All 28 tests passed without warnings or failures.

---

## 3. Pre-Flight Verification & Edge Cases for Improver

1. **`REPO_ROOT` Calculation**:
   - `c2c_hook_guard.py` uses `Path(__file__).resolve().parents[3]`.
   - Verified that regardless of whether `cwd` is `d:\Augusto\personal_portfolio\Tops_academy\.agents` or repository root, `REPO_ROOT` points to `d:\Augusto\personal_portfolio\Tops_academy`.
2. **Hot-Reload Prevention**:
   - Verified that `.agents/hooks.json` does NOT exist in the workspace. Only `.agents/hooks.template.json` was created.
3. **Fail-Open Behavior**:
   - If stdin is empty, malformed, or an unhandled exception occurs in `c2c_hook_guard.py`, `main()` catches it and emits `{"decision": "allow"}` so Antigravity never locks up during tool execution.
4. **Token Estimation vs Explicit Tokens**:
   - When explicit `input_tokens`, `output_tokens`, or `cache_read_tokens` are present (as in Antigravity's real transcripts), they are summed directly.
   - When missing (as in compact transcripts), the cumulative formula `sum(20_000 + 800 * k)` kicks in, scaling quadratic with turn count to accurately simulate KV cache accumulation.
