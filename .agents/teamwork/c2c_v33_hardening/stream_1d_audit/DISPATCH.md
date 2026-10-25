# DISPATCH: Stream 1D — Forensic Auditor (`audit_1d`)

- **Orchestrator Conversation ID (`Recipient` for `send_message`):** `d0ce22db-904e-4856-b353-59975bfb5874`
- **Teamwork Directory (ONLY allowed write target):** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1d_audit`
- **Artifacts to Audit:**
  - Original Stream Spec: `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1d_impl/DISPATCH.md`
  - Implementer Handoff: `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1d_impl/handoff.md`
  - Improver Spec & Handoff: `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1d_impr/{DISPATCH.md,handoff.md}`
  - Reference Docs: `C:\Users\augus\.gemini\antigravity\builtin\skills\agy-customizations\docs\hooks.md`
  - Audited Code & Tests (READ-ONLY):
    - `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/budget_guard.py`
    - `d:/Augusto/personal_portfolio/Tops_academy/.agents/hooks.template.json`
    - `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/c2c_hook_guard.py`
    - `d:/Augusto/personal_portfolio/Tops_academy/tests/test_watchdog_and_hooks.py`

## Audit Checklist
1. **Boundary & Safety Integrity:**
   - Verify `.agents/hooks.json` DOES NOT EXIST on disk (only `.agents/hooks.template.json` exists!).
   - Verify Stream 1D modified ONLY `budget_guard.py`, `.agents/hooks.template.json`, `c2c_hook_guard.py`, and `tests/test_watchdog_and_hooks.py` (ignoring files belonging to concurrent streams `1A`, `1B`, `1C`, `1E` and baseline dirty files in `ORIGINAL_REQUEST.md`).
2. **Protocol & Requirement Verification:**
   - Cross-check `.agents/hooks.template.json` and `c2c_hook_guard.py` stdin/stdout JSON keys against `C:\Users\augus\.gemini\antigravity\builtin\skills\agy-customizations\docs\hooks.md` (`PreToolUse` format, exit status `0`, `"decision": "allow"` / `"deny"`, `cwd = .agents/` relative path `"python skills/content-to-course/c2c_hook_guard.py"`, `REPO_ROOT = Path(__file__).resolve().parents[3]`, pure Python stdlib only).
   - Verify fast pass-through when no active `.c2c_subagent_lock.json` exists or lock is stale (`> 2h`).
   - Verify Director Context Diet (`conversationId == director_conversation_id` denied `*_data.py` / `shard_fixes/*.py` / `judge_responses_*.json`, allowed `state.json` / `judge_report.json` / `dispatch/**` / `logs/**`) and Worker isolation (denied reading/shell-catting `compile_shard.py`, `check_templates.py`, `engine/`, `judge_ground_truth.json`, `.check_attempts`, `SKILL.md`; allowed running official `compile_shard.py` / `compile_cta.py` CLI).
   - Verify `budget_guard.py` resolves `<appDataDir>/brain/<id>/.system_generated/logs/transcript.jsonl`, parses `PLANNER_RESPONSE`, handles truncated trailing JSONL lines, and outputs `shard_fixes/<CID>.py` repair orders + `next_schedule_seconds: 300`.
3. **Independent Test Execution:**
   - Run `& "d:\Augusto\personal_portfolio\Tops_academy\.venv\Scripts\python.exe" -m pytest tests/test_watchdog_and_hooks.py tests/test_orchestration_resilience.py -q`.
4. Write `BRIEFING.md`, `progress.md`, and `handoff.md` inside `stream_1d_audit/`, then `send_message` starting with `PASS:: stream_1d_audit | ...` or `REJECT:: stream_1d_audit | ...`.
