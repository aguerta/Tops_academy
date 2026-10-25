# DISPATCH: Stream 1D — Improver (`impr_1d`)

- **Orchestrator Conversation ID (`Recipient` for `send_message`):** `d0ce22db-904e-4856-b353-59975bfb5874`
- **Teamwork Directory:** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1d_impr`
- **Implementer Handoff to Audit & Improve:** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1d_impl/handoff.md`
- **Role:** `Phase 2 Mejorador — Stream 1D (Watchdog <appDataDir>/brain/ & Hook Dual c2c_hook_guard.py)`

## 1. Strict Write Boundaries (ONLY touch these files + your Teamwork Directory)
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/budget_guard.py`
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/hooks.template.json` *(CRITICAL: NEVER create `.agents/hooks.json`!)*
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/c2c_hook_guard.py`
- `d:/Augusto/personal_portfolio/Tops_academy/tests/test_watchdog_and_hooks.py`
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1d_impr/{BRIEFING.md,progress.md,handoff.md}`

## 2. Hardening & Scrutiny Objectives
1. Read `stream_1d_impl/handoff.md`, `budget_guard.py`, `.agents/hooks.template.json`, `c2c_hook_guard.py`, `tests/test_watchdog_and_hooks.py`, and `C:\Users\augus\.gemini\antigravity\builtin\skills\agy-customizations\docs\hooks.md`.
2. Scrutinize & harden edge cases:
   - **Exact Antigravity Hook JSON Contract:** Check `docs/hooks.md` for exact stdin payload keys (`conversationId` vs `conversation_id`, `toolName` vs `tool_name`, `toolInput` vs `tool_input`, nested `Path` / `TargetFile` / `CommandLine`) and exact stdout response schema (`decision` / `hookSpecificOutput` / `permissionDecision`—verify exact keys documented in `docs/hooks.md` so Antigravity's JSON hook parser accepts 100% of allow/deny responses without schema errors!).
   - **Path Normalization & Traversal Safety in `c2c_hook_guard.py`:** Handle mixed Windows slashes (`D:\Augusto\...` vs `d:/Augusto/...`), URL-encoded or relative paths (`.\.agents\skills\content-to-course\compile_shard.py`, `../.check_attempts/`), case-insensitivity on Windows (`COMPILE_SHARD.PY`), and PowerShell commands attempting `Get-Content` / `type` / `cat` on `compile_shard.py`, `check_templates.py`, or `judge_ground_truth.json`!
   - **Director Diet Precision:** Ensure the Director IS allowed to read `work/dispatch/items/*.json` or `work/dispatch/types/*.json` and `work/logs/*.log`, while DENIED reading/editing `*_data.py`, `shard_fixes/*.py`, and `judge_responses_*.json`. Also support an optional `"exempt_conversation_ids": [...]` list in `.c2c_subagent_lock.json` just in case an auditor agent needs read access!
   - **`budget_guard.py` Robustness:** Handle malformed/truncated trailing JSONL lines gracefully (common when reading a live `transcript.jsonl` while a subagent is mid-write!), support both `transcript.jsonl` and `transcript_full.jsonl` fallback if needed, and verify Windows `.venv\Scripts\python.exe` path formatting in `generate_repair_redispatch()`.
   - Expand `tests/test_watchdog_and_hooks.py` with adversarial cases covering all of the above (mixed Windows backslashes, `Get-Content compile_shard.py` via `run_command`, truncated live JSONL line in `budget_guard.py`, exact `docs/hooks.md` stdin/stdout schema check).
3. Run `& "d:\Augusto\personal_portfolio\Tops_academy\.venv\Scripts\python.exe" -m pytest tests/test_watchdog_and_hooks.py tests/test_orchestration_resilience.py -q`.
4. Write `BRIEFING.md`, `progress.md`, and `handoff.md`, then `send_message` starting with `DONE:: stream_1d_impr`.
