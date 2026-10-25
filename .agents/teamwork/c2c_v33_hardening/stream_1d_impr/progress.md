# PROGRESS: Stream 1D — Improver (`impr_1d`)

- **Stream:** 1D (Watchdog Conectado a `<appDataDir>/brain/` y Guardrail Dual `.agents/hooks.json`)
- **Improver:** Phase 2 Mejorador (`impr_1d`)
- **Recipient:** Orchestrator (`d0ce22db-904e-4856-b353-59975bfb5874`) & Phase 3 Auditor
- **Status:** COMPLETED & CERTIFIED (40/40 tests passing)

---

## 1. Summary of Hardening Delivered

### A. Lifecycle Hook Guard (`.agents/skills/content-to-course/c2c_hook_guard.py`)
1. **Adversarial Shell Inspection Blocking**:
   - Closed critical loophole where subagents could run PowerShell/CMD commands (`Get-Content`, `gc`, `type`, `cat`, `more`, `head`, `tail`, `Select-String`, `sls`, `grep`, `findstr`, `Copy-Item`, `cp`, `move`, `mv`) to inspect or leak protected compiler/validator/ground truth source files.
   - Closed `.NET` file read attempts in PowerShell (`[System.IO.File]::ReadAllText(...)`).
   - Closed `python -c` script inspection attempts targeting forbidden files.
   - Enforced hard block on ANY command referencing `judge_ground_truth.json`.
   - Distinguishes compiler CLI execution (`python compile_shard.py ...` or `& "d:\path\python.exe" compile_shard.py ...` via dedicated `PYTHON_EXEC_PATTERN`), ensuring legitimate compiler execution is 100% permitted.
2. **Windows Path Normalization & Canonicalization**:
   - Added robust URL decoding (`urllib.parse.unquote`), file URI normalization (`file:///`), Windows backslash conversion (`\` -> `/`), and leading `./` stripping in `_normalize_path`.
   - Case-insensitive matching and path traversal (`..\`, `../`) checks prevent evasion techniques.
3. **Write Protection on Compiler & Engine**:
   - Expanded `WORKER_DENIED_WRITE_SUBSTRINGS` to block worker `write_file` / `edit_file` / `notebook_edit` on `compile_shard.py`, `check_templates.py`, `compile_cta.py`, `check_cta.py`, `cta_merge.py`, `engine/`, `validator/`, `judge_ground_truth.json`.
4. **Director Diet Precision**:
   - Verified Director is ALLOWED to read `work/dispatch/items/*.json`, `work/dispatch/types/*.json`, `work/logs/*.log`, `work/state.json`, and `work/judge_report.json`.
   - Verified Director is DENIED reading or editing `*_data.py`, `shard_fixes/*.py`, and `judge_responses*.json`.
5. **Auditor Exemption Mechanism**:
   - Added support for `"exempt_conversation_ids": [...]` in `.c2c_subagent_lock.json`. Any conversation ID listed in this array bypasses restrictions for auditor/QA inspections.
6. **docs/hooks.md Schema Compatibility**:
   - Tolerates both camelCase (`conversationId`, `toolCall`, `stepIdx`) and snake_case (`conversation_id`, `tool_call`) payloads.
   - Stdout strictly complies with `{"decision": "allow" | "deny", "reason": "..."}` schema.
   - Preserves exit code 0 invariant and fail-open exception handling.
   - Performance benchmark: 1,000 evaluations complete in < 250ms (< 0.25ms per check).

### B. Budget Watchdog (`.agents/skills/content-to-course/budget_guard.py`)
1. **Live Truncated JSONL Graceful Handling**:
   - Uses `errors="replace"` on `read_text` to guard against mid-write incomplete multi-byte UTF-8 sequences.
   - Skips partial/truncated trailing JSON lines without crashing or corrupting turn counts.
   - Only counts valid JSON entries in fallback turn estimation (`parsed_entries_count`).
2. **Brain Transcript Resolution Fallback**:
   - Supports discovering both `transcript.jsonl` and `transcript_full.jsonl` in `.system_generated/logs/` and `brain/<id>/`.
3. **Empty File Handling**:
   - Returns zeroed metrics gracefully without raising exceptions.

### C. Test Suite Expansion (`tests/test_watchdog_and_hooks.py`)
- Expanded from 12 to 24 comprehensive unit and adversarial tests (+100% test coverage).
- Total tests passing across Stream 1D and Stream C resilience: **40 passed in 0.68s**.

---

## 2. Test Execution Log

```
pytest tests/test_watchdog_and_hooks.py tests/test_orchestration_resilience.py -v
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0
collected 40 items

tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_auditor_exemption_in_lockfile PASSED [  2%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_cli_subprocess_stdin_stdout_robustness PASSED [  5%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_director_allowed_logs_and_dispatch_types PASSED [  7%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_director_context_diet_enforcement PASSED [ 10%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_docs_hooks_contract_schema_and_variations PASSED [ 12%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_fast_passthrough_when_no_active_lock PASSED [ 15%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_hook_guard_performance_benchmark PASSED [ 17%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_hooks_template_json_structure_and_cwd_execution PASSED [ 20%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_passthrough_when_lock_is_stale_or_inactive PASSED [ 22%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_windows_path_normalization_and_traversal_safety PASSED [ 25%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_worker_allowed_compiler_execution_commands PASSED [ 27%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_worker_allowed_safe_operations PASSED [ 30%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_worker_denied_deleting_check_attempts_and_nested_quote_python_c PASSED [ 32%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_worker_denied_modifying_compiler_and_engine PASSED [ 35%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_worker_denied_modifying_skills_and_check_attempts PASSED [ 37%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_worker_denied_powershell_and_shell_read_commands PASSED [ 40%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_worker_denied_reading_compiler_engine_and_truth PASSED [ 42%]
tests/test_watchdog_and_hooks.py::TestBudgetWatchdogBrainAndRedispatch::test_cumulative_context_token_estimator_on_compact_transcript PASSED [ 45%]
tests/test_watchdog_and_hooks.py::TestBudgetWatchdogBrainAndRedispatch::test_generate_repair_redispatch_with_modular_shard_fixes_and_schedule PASSED [ 47%]
tests/test_watchdog_and_hooks.py::TestBudgetWatchdogBrainAndRedispatch::test_parse_real_antigravity_brain_transcript_108_turns PASSED [ 50%]
tests/test_watchdog_and_hooks.py::TestBudgetWatchdogBrainAndRedispatch::test_parse_transcript_empty_file PASSED [ 52%]
tests/test_watchdog_and_hooks.py::TestBudgetWatchdogBrainAndRedispatch::test_parse_transcript_with_truncated_live_line PASSED [ 55%]
tests/test_watchdog_and_hooks.py::TestBudgetWatchdogBrainAndRedispatch::test_resolve_brain_transcript_with_app_data_dir PASSED [ 57%]
tests/test_watchdog_and_hooks.py::TestBudgetWatchdogBrainAndRedispatch::test_resolve_brain_transcript_with_transcript_full_fallback PASSED [ 60%]
tests/test_orchestration_resilience.py::TestPointerPromptProtocol::test_dispatch_authors_pointer_mode_creates_disk_items_and_lean_prompts PASSED [ 62%]
tests/test_orchestration_resilience.py::TestPointerPromptProtocol::test_dispatch_cta_mapreduce_heaviest_first_and_pointer PASSED [ 65%]
tests/test_orchestration_resilience.py::TestPointerPromptProtocol::test_generate_define_subagent_specs_lean_mode PASSED [ 67%]
tests/test_orchestration_resilience.py::TestPointerPromptProtocol::test_lean_system_prompts_size_and_contract PASSED [ 70%]
tests/test_orchestration_resilience.py::TestPointerPromptProtocol::test_load_system_prompt_lean_mode PASSED [ 72%]
tests/test_orchestration_resilience.py::TestPointerPromptProtocol::test_make_pointer_prompt_under_300_bytes PASSED [ 75%]
tests/test_orchestration_resilience.py::TestJudgeNativeBatching::test_check_judge_completeness_and_redispatch PASSED [ 77%]
tests/test_orchestration_resilience.py::TestJudgeNativeBatching::test_dispatch_judges_pointer_mode_and_blind_integrity PASSED [ 80%]
tests/test_orchestration_resilience.py::TestJudgeNativeBatching::test_split_judge_batch_strict_limit_12 PASSED [ 82%]
tests/test_orchestration_resilience.py::TestBudgetWatchdog::test_generate_repair_redispatch_for_unfinished_units PASSED [ 85%]
tests/test_orchestration_resilience.py::TestBudgetWatchdog::test_watchdog_detects_script_looping PASSED [ 87%]
tests/test_orchestration_resilience.py::TestBudgetWatchdog::test_watchdog_detects_token_runaway PASSED [ 90%]
tests/test_orchestration_resilience.py::TestBudgetWatchdog::test_watchdog_detects_turn_runaway PASSED [ 92%]
tests/test_orchestration_resilience.py::TestBudgetWatchdog::test_watchdog_parses_real_transcript_and_ignores_completed PASSED [ 95%]
tests/test_orchestration_resilience.py::TestStatefulResumptionAndCleanup::test_pre_stage5_cleanup_purges_errored_subagents PASSED [ 97%]
tests/test_orchestration_resilience.py::TestStatefulResumptionAndCleanup::test_state_checkpoint_lifecycle PASSED [100%]

============================= 40 passed in 0.68s ==============================
```
