# DISPATCH: Stream 1D — Implementer (`impl_1d`)

- **Orchestrator Conversation ID (`Recipient` for `send_message`):** `d0ce22db-904e-4856-b353-59975bfb5874`
- **Teamwork Directory:** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1d_impl`
- **Role:** `Phase 1 Implementador — Stream 1D (Watchdog Conectado a <appDataDir>/brain/ y Guardrail Dual .agents/hooks.json)`

## 1. Strict Write Boundaries (ONLY touch these files + your Teamwork Directory)
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/budget_guard.py`
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/hooks.template.json` *(new — DO NOT create `.agents/hooks.json` yet! Antigravity hot-reloads `.agents/hooks.json` live with `cwd = .agents/`, so Stage 1 writes and validates `.agents/hooks.template.json` and Stage 3 activates `.agents/hooks.json` after full certification!)*
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/c2c_hook_guard.py` *(new)*
- `d:/Augusto/personal_portfolio/Tops_academy/tests/test_watchdog_and_hooks.py` *(new)*
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1d_impl/{BRIEFING.md,progress.md,handoff.md}`

*(Forbidden: STRICTLY FORBIDDEN to create `.agents/hooks.json` in Stage 1! Do NOT edit `run.py`, `dispatch.py`, `compile_shard.py`, or any other file outside the list above!)*

## 2. Technical Specifications
1. **Step 0 Pre-Flight Sanity Check:**
   - Read `budget_guard.py`, any existing tests for `budget_guard` (`tests/test_*budget*` or `tests/test_*watchdog*`), and `C:\Users\augus\.gemini\antigravity\builtin\skills\agy-customizations\docs\hooks.md` (to verify exact Antigravity `hooks.json` schema, stdin JSON keys, stdout JSON format, and exit codes!). Record findings in `BRIEFING.md`. Escalate via `BLOCKER::` if any hard conflict blocks your order.
2. **Real Antigravity Brain Transcript Resolution & Parsing (`budget_guard.py`):**
   - Today `budget_guard.py` looks only in `work/transcripts/*.jsonl` and misses Antigravity's real transcript schema!
   - Add automatic discovery of `<appDataDir>/brain/<subagent_id>/.system_generated/logs/transcript.jsonl`:
     - Support `--app-data-dir`, `ANTIGRAVITY_APP_DATA_DIR`, and default Windows/POSIX paths (`~/.gemini/antigravity`, `~/.gemini/antigravity-ide`, `~/.gemini/antigravity-cli`).
     - Accept `--subagent-ids id1,id2,...` OR read active spawned subagent IDs from `work/state.json` / `work/dispatch/*.json` (and keep full backward compatibility with `--transcript` and `work/transcripts/*.jsonl` for existing unit tests!).
   - Upgrade `parse_transcript()` to natively parse Antigravity's real JSONL step format (`"type": "PLANNER_RESPONSE"` / `"source": "MODEL"`, `"tool_calls"` array containing `name`/`tool_name` + arguments `Path`/`TargetFile`/`CommandLine`, `"thinking"` character count, explicit `usage`/`tokens` if present, PLUS a deterministic cumulative context/cache token estimator when compact `transcript.jsonl` omits explicit token usage so a 100-turn agent is reliably flagged for `> 40` turns and `> 5M` estimated cached tokens!).
   - Detect forbidden tool-introspection loops (`compile_shard.py`, `check_templates.py`, `compile_cta.py`, `engine/`).
   - Update `generate_repair_redispatch()` so rescue work orders use `.venv/Scripts/python.exe` (when present), `--work "<work_dir>" --shard <unit_id>`, instruct writing modular `work/shards/shard_fixes/<CID>.py`, and include `"next_schedule_seconds": 300` in the report JSON whenever incomplete/non-aborted units are still running.
3. **Conditional Dual-Role Antigravity Hook (`.agents/hooks.template.json` + `c2c_hook_guard.py`):**
   - **CRITICAL LIVE RUNTIME LESSON (`cwd = .agents/`):** When Antigravity executes `.agents/hooks.json`, its subprocess working directory (`cwd`) is **`d:\Augusto\personal_portfolio\Tops_academy\.agents`** (the directory containing `hooks.json`, NOT the repository root!).
     - Therefore:
       1. Write `.agents/hooks.template.json` (NEVER `.agents/hooks.json` during Stage 1!) using `"command": "python skills/content-to-course/c2c_hook_guard.py"` (relative to `.agents/`)!
       2. Inside `c2c_hook_guard.py`, NEVER rely on `Path.cwd()` to locate `courses/`! Always resolve `REPO_ROOT = Path(__file__).resolve().parents[3]` (`c2c_hook_guard.py` -> `content-to-course` -> `skills` -> `.agents` -> `<repo_root>`) so `REPO_ROOT / "courses"` works identically whether `cwd` is `.agents/` or `<repo_root>`!
       3. `c2c_hook_guard.py` MUST use **pure Python stdlib only** and ALWAYS exit with code `0` (communicating `"allow"` vs `"deny"` strictly via JSON stdout `{"decision": "allow"}` or `{"decision": "deny", "reason": "..."}`, NEVER exiting with code `2`!).
   - Configure `.agents/hooks.template.json` using the exact Antigravity `PreToolUse` format matching file/command tools (`read_file|view_file|write_file|write_to_file|edit_file|replace_file_content|multi_replace_file_content|run_command`), invoking `python skills/content-to-course/c2c_hook_guard.py`.
   - In `tests/test_watchdog_and_hooks.py`, explicitly test invoking the exact command string from `.agents/hooks.template.json` via `subprocess.run(..., cwd=repo_root / ".agents")` to prove `cwd = .agents/` works with exit code `0`!
   - **CRITICAL ZERO-INTERFERENCE RULE (Outside Active C2C Runs):**
     - `c2c_hook_guard.py` scans `courses/*/work*/.c2c_subagent_lock.json` (plus optional `C2C_LOCK_FILE` env var for testing).
     - If NO lockfile exists, OR all lockfiles are older than `7200` seconds (2 hours) / marked `"active": false`, immediately output `{"decision": "allow"}` and `sys.exit(0)` in `< 15 ms`! (**CRITICAL:** Right now, our own `c2c_v33_hardening` teamwork subagents are running in this workspace without `.c2c_subagent_lock.json`—so `c2c_hook_guard.py` MUST allow 100% of calls when no active `.c2c_subagent_lock.json` exists!)
   - **When an Active `.c2c_subagent_lock.json` Exists (`{"active": true, "director_conversation_id": "...", "work_dir": "..."}`):**
     - **Case A — Caller IS the C2C Director (`conversationId == director_conversation_id`):**
       - Enforce the **Director Context Diet**: DENY (`{"decision": "deny", "reason": "C2C v3.3 Director Diet: Do not read or edit worker *_data.py or judge_responses files directly. Delegate repairs via dispatch.py --role repair."}`) if the Director attempts to `read_file`/`view_file`/`write_file`/`edit_file` any `*_data.py`, `shard_fixes/*.py`, or `judge_responses_*.json`! Allow all CLI `run_command` orchestration and reading compact manifests/reports (`state.json`, `judge_report.json`, `dispatch/types/*.json`, `dispatch/*.json`).
     - **Case B — Caller IS a C2C Worker Subagent (`conversationId != director_conversation_id` and `director_conversation_id` is non-empty):**
       - DENY `read_file`/`view_file` targeting internal validator/compiler source or ground truth: `compile_shard.py`, `check_templates.py`, `compile_cta.py`, `check_cta.py`, `/engine/`, `/validator/`, `src/validator/`, `.check_attempts`, `judge_ground_truth.json`, or `SKILL.md`.
       - DENY `write_file`/`edit_file` targeting `.check_attempts` or internal `.agents/skills/` scripts.
       - DENY `run_command` that deletes/modifies `.check_attempts` or runs complex nested-quote `python -c` (`python -c` with escaped quotes `\"` or length `> 120` chars; instruct using a script or official compiler CLI).
     - On any unexpected JSON parse error in stdin, fail-open (`{"decision": "allow"}`) so the IDE never bricks.

## 3. Required Tests & Verification
- Create `tests/test_watchdog_and_hooks.py` testing:
  - Fast pass-through (`< 50ms`) when no `.c2c_subagent_lock.json` exists or lock is stale (`> 2h`).
  - Worker subagent denied reading `compile_shard.py`, `engine/assemble.py`, `judge_ground_truth.json`, `.check_attempts`, and denied nested-quote `python -c`, while allowed reading `content/*.pdf`, `work/dispatch/items/author_01.json`, and writing `work/shards/shard_01_data.py` or `work/shards/shard_fixes/Hab-03.py`.
  - Director (`conversationId == director_conversation_id`) denied reading/editing `work/shards/shard_06_data.py` or `work/cta_data.py`, while allowed reading `work/state.json` and `work/judge_report.json`.
  - `budget_guard.py` resolving `<appDataDir>/brain/<id>/.system_generated/logs/transcript.jsonl` with 108 `PLANNER_RESPONSE` steps (modeled on `shard_06` of `ab30cf91`), flagging turn/token breach + tool-read loop, and emitting modular `shard_fixes` repair order + `next_schedule_seconds: 300`.
- Run `& "d:\Augusto\personal_portfolio\Tops_academy\.venv\Scripts\python.exe" -m pytest tests/test_watchdog_and_hooks.py -q` plus any existing `budget_guard` tests!
