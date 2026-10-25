# BRIEFING: Stream 1D Improver Pre-Flight & Hardening Architecture Plan

- **Stream:** 1D (Watchdog Conectado a `<appDataDir>/brain/` y Guardrail Dual `.agents/hooks.json`)
- **Agent:** Phase 2 Mejorador (`impr_1d`)
- **Status:** PRE-FLIGHT VERIFIED — PROCEEDING TO HARDENING (No blockers detected)

---

## 1. Implementer Review & Gap Analysis

The Phase 1 Implementer delivered working foundations:
- Fast path (< 15 ms) when outside active C2C runs.
- Basic dual-role segregation between Director and Worker subagents.
- Transcript parsing for Antigravity `PLANNER_RESPONSE` steps and cumulative token estimation.
- 28/28 tests passing.

However, the scrutiny identified the following critical edge cases and attack vectors:

### A. Antigravity Hook Schema & Input Compatibility
- **Docs Specification (`docs/hooks.md`)**:
  - `PreToolUse` stdin sends camelCase fields: `toolCall` (`name`, `args`), `conversationId`, `stepIdx`, `workspacePaths`, etc.
  - Output stdout expects `{"decision": "allow" | "deny" | "ask" | "force_ask", "reason": "..."}`.
  - The guard must tolerate variations in input formatting (`conversationId` vs `conversation_id`, `toolName` vs `tool_name`, `args` vs `arguments` vs `tool_input` vs `toolInput`) and always emit compliant stdout JSON.

### B. Shell Command Bypassing & Path Normalization in `c2c_hook_guard.py`
- **Shell Command Inspection Loophole**:
  - The implementer only checked `run_command` for `.check_attempts` deletion and long `python -c` snippets.
  - A worker subagent could bypass file read restrictions by executing shell commands like:
    - PowerShell: `Get-Content compile_shard.py`, `gc check_templates.py`, `type judge_ground_truth.json`, `cat .check_attempts/shard_01.json`
    - Shell / CMD: `cat`, `type`, `more`, `head`, `tail`, `grep`, `Select-String`, `python -c "open('compile_shard.py').read()"`
  - We must detect and block these shell read attempts targeting protected compiler/validator/ground truth targets.
- **Path Traversal & Windows Path Canonicalization**:
  - Mixed slashes (`D:\path` vs `d:/path`), URL-encoded paths (`compile%5Fshard.py`), relative paths with `.\` or `../`, and Windows case insensitivity (`COMPILE_SHARD.PY`) must be normalized and checked against forbidden targets.

### C. Director Diet Precision & Auditor Exemption
- **Exemptions**:
  - An auditor subagent or human reviewer might need read access across the board. The guard should support an optional `"exempt_conversation_ids": [...]` list in `.c2c_subagent_lock.json`.
- **Director Diet Scope**:
  - Ensure Director can view `work/dispatch/items/*.json`, `work/dispatch/types/*.json`, and `work/logs/*.log`.
  - Director must be denied reading or editing `*_data.py`, `shard_fixes/*.py`, and `judge_responses*.json`.

### D. Budget Watchdog Robustness
- **Live Truncated JSONL**:
  - Subagents writing live transcripts can produce a trailing partial line. `budget_guard.py` must handle `errors="replace"`, malformed trailing lines, and empty files without crashing.
- **Transcript File Fallback**:
  - Support discovery of both `transcript.jsonl` and `transcript_full.jsonl`.
- **Windows Path Formatting**:
  - Verify that `compile_command` in `generate_repair_redispatch` uses standard normalized quotes and valid python executable paths.

---

## 2. Hardening Action Plan

1. **`c2c_hook_guard.py`**:
   - Add robust path normalization (`urllib.parse.unquote`, `os.path.normpath`, lowercase matching).
   - Add shell command inspection for file read/inspection attempts (`Get-Content`, `gc`, `type`, `cat`, `more`, `head`, `tail`, `Select-String`, `grep`) on protected targets.
   - Add support for `"exempt_conversation_ids"` in `.c2c_subagent_lock.json`.
   - Ensure resilient input parsing (`conversationId` / `conversation_id`, `toolCall.name` / `tool_name`, `args` / `toolInput`).
   - Guarantee strict schema compliance with `docs/hooks.md`.

2. **`budget_guard.py`**:
   - Support `errors="replace"` when reading files.
   - Handle truncated trailing JSONL lines gracefully.
   - Support discovery of both `transcript.jsonl` and `transcript_full.jsonl` in `resolve_brain_transcript` and `scan_work_transcripts`.

3. **`tests/test_watchdog_and_hooks.py`**:
   - Add tests for PowerShell / shell command read blocking (`Get-Content compile_shard.py`, `type judge_ground_truth.json`, etc.).
   - Add tests for Windows path variations (casing, backslashes, relative `.\`, URL-encoded).
   - Add tests for `exempt_conversation_ids` lockfile option.
   - Add tests for live truncated JSONL lines in `budget_guard.py`.
   - Add tests for `transcript_full.jsonl` resolution.
   - Verify zero regression in existing test suite.
