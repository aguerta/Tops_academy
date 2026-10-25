# BRIEFING: Stream 1D Pre-Flight Verification & Execution Plan

- **Stream:** 1D (Watchdog Conectado a `<appDataDir>/brain/` y Guardrail Dual `.agents/hooks.json`)
- **Agent:** Phase 1 Implementador (`impl_1d`)
- **Status:** READY TO EXECUTE (No blockers detected)

---

## 1. Pre-Flight Verification Findings

### A. Existing Code & Test Baseline
- Inspected `budget_guard.py` (554 lines).
  - Existing `parse_transcript` only looks for `"role": "assistant"|"model"` and basic token dictionaries or `len(line)//4`.
  - Missing native Antigravity format: `"source": "MODEL"`, `"type": "PLANNER_RESPONSE"`, `"thinking"`, explicit top-level `input_tokens`/`output_tokens`/`cache_read_tokens`, and cumulative context token estimation when tokens are omitted.
  - Monitored scripts list currently misses `engine/` or full forbidden inspection targets.
  - Transcript scanner only globs `work/transcripts/*.jsonl` and `work/dispatch/transcripts/*.jsonl`. Does not resolve Antigravity's real storage at `<appDataDir>/brain/<subagent_id>/.system_generated/logs/transcript.jsonl`.
- Tested baseline with `tests/test_orchestration_resilience.py`:
  - 16 tests passed in 0.24s.
  - Existing signatures: `parse_transcript`, `evaluate_watchdog_rules`, `scan_work_transcripts`, `identify_unfinished_competencies`, `generate_repair_redispatch`, `update_state_checkpoint`, `load_state_checkpoint`. All existing parameters and returned dictionary keys must remain fully backward-compatible.

### B. Antigravity Hooks Specification (`hooks.md`)
- Inspected `C:\Users\augus\.gemini\antigravity\builtin\skills\agy-customizations\docs\hooks.md`:
  - Format: Top-level hook name mapping to event arrays (`PreToolUse`, `PostToolUse`, etc.).
  - `PreToolUse` is grouped with `"matcher"` and `"hooks"` list.
  - Stdin payload: JSON with `toolCall` (`name`, `args`), `conversationId`, `stepIdx`, `workspacePaths`, `transcriptPath`, etc.
  - Stdout contract: JSON with `{"decision": "allow" | "deny" | "ask"}` and optional `reason`.
  - Tool names matched: `read_file|view_file|write_file|write_to_file|edit_file|replace_file_content|multi_replace_file_content|run_command`.

### C. Ground Truth Verification
- Inspected real transcript on disk: `C:\Users\augus\.gemini\antigravity\brain\b9bc17ec-092d-4d5d-80b6-428307c2143b\.system_generated\logs\transcript.jsonl` (corresponding to Shard Author shard_06 in asyntotic_estatistics_v2).
  - Verified 108 `PLANNER_RESPONSE` steps, 17 `run_command` calls to `compile_shard.py`, and token usage fields (`input_tokens`, `output_tokens`, `cache_read_tokens`).

---

## 2. Execution Plan

### Step 1: Implement `c2c_hook_guard.py`
- Pure Python stdlib (`sys`, `os`, `json`, `glob`, `time`, `re`, `pathlib`).
- Zero-interference rule:
  - Check `C2C_LOCK_FILE` env var, else scan `courses/*/work*/.c2c_subagent_lock.json`.
  - If no lockfile exists or lockfile is older than 7200s (2 hours) or `"active": false`: immediately emit `{"decision": "allow"}` and `sys.exit(0)`.
- If active lockfile exists (`active: true`, non-empty `director_conversation_id`):
  - Read stdin JSON (with fail-open on decode error).
  - Extract tool name, args, and `conversationId`.
  - If caller is Director (`conversationId == director_conversation_id`):
    - DENY reading/editing `*_data.py`, `shard_fixes/*.py`, or `judge_responses*.json`.
    - ALLOW compact manifests (`state.json`, `judge_report.json`, `dispatch/*.json`, etc.) and `run_command`.
  - If caller is Worker Subagent (`conversationId != director_conversation_id`):
    - DENY reading `compile_shard.py`, `check_templates.py`, `compile_cta.py`, `check_cta.py`, `/engine/`, `/validator/`, `src/validator/`, `.check_attempts`, `judge_ground_truth.json`, `SKILL.md`.
    - DENY writing/editing `.check_attempts`, `.agents/skills/`.
    - DENY `run_command` modifying/deleting `.check_attempts`, or nested-quote `python -c` (escaped quotes `\"` or len > 120 chars).
    - ALLOW reading content (`content/*.pdf`, `dispatch/items/*.json`), writing `*_data.py` or `shard_fixes/*.py`, running compiler CLIs.

### Step 2: Configure `.agents/hooks.json`
- Define `PreToolUse` hook matching `read_file|view_file|write_file|write_to_file|edit_file|replace_file_content|multi_replace_file_content|run_command`.
- Command: `python .agents/skills/content-to-course/c2c_hook_guard.py`.

### Step 3: Upgrade `budget_guard.py`
- Brain transcript resolution:
  - Support finding brain transcripts in `<appDataDir>/brain/<id>/.system_generated/logs/transcript.jsonl`.
  - Support `--app-data-dir`, `ANTIGRAVITY_APP_DATA_DIR`, default candidate directories (`~/.gemini/antigravity`, `~/.gemini/antigravity-ide`, `~/.gemini/antigravity-cli`).
  - Support `--subagent-ids` or discover subagent IDs from `state.json` / `dispatch/*.json`.
- Transcript parser:
  - Recognize `"type": "PLANNER_RESPONSE"`, `"source": "MODEL"`.
  - Clean tool call argument paths/commands (strip outer quotes).
  - Track `thinking` character counts.
  - Count explicit `input_tokens`, `output_tokens`, `cache_read_tokens` / `cached_tokens`.
  - Implement cumulative context/cache token estimator for compact transcripts without explicit usage (guaranteeing > 40 turns & > 5M tokens flags runaway for 100-turn transcripts).
  - Detect tool introspection loops targeting `compile_shard.py`, `check_templates.py`, `compile_cta.py`, `engine/`.
- Repair redispatch:
  - Use `.venv/Scripts/python.exe` (or `sys.executable`).
  - Include `--work "<work_dir>" --shard <unit_id>`.
  - Instruct writing modular `work/shards/shard_fixes/<CID>.py`.
  - Include `"next_schedule_seconds": 300` when incomplete units are detected.

### Step 4: Write `tests/test_watchdog_and_hooks.py`
- Full test coverage for:
  1. Fast pass-through (< 50ms) without lockfile or with stale lockfile.
  2. Worker subagent allowed reading content / writing shard data, denied reading protected compiler/engine/truth files, denied nested-quote `python -c`.
  3. Director denied reading/editing worker data files, allowed reading state/manifests and running commands.
  4. Real brain transcript parsing on 108-step `PLANNER_RESPONSE` transcript (or synthetic equivalent), verifying turn/token breach, tool loop detection, repair order with `shard_fixes`, and `next_schedule_seconds: 300`.

### Step 5: Run Pytest Suite & Handoff
- Run `& "d:\Augusto\personal_portfolio\Tops_academy\.venv\Scripts\python.exe" -m pytest tests/test_watchdog_and_hooks.py tests/test_orchestration_resilience.py -q`.
- Write `progress.md` and `handoff.md`.
- Send completion message to orchestrator `d0ce22db-904e-4856-b353-59975bfb5874`.
