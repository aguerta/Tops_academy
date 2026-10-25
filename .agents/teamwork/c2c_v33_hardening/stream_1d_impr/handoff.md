# HANDOFF: Stream 1D — Improver (`impr_1d`) to Auditor (`audit_1d`)

- **Stream:** 1D (Watchdog Conectado a `<appDataDir>/brain/` y Guardrail Dual `.agents/hooks.json`)
- **Author:** Phase 2 Mejorador (`impr_1d`)
- **Recipient:** Orchestrator (`d0ce22db-904e-4856-b353-59975bfb5874`) & Phase 3 Auditor
- **Status:** HARDENING CERTIFIED (40/40 tests passing)

---

## 1. Summary of Improvements & Hardening Delivered

### A. Lifecycle Hook Guard (`.agents/skills/content-to-course/c2c_hook_guard.py`)
1. **Adversarial Shell Inspection Blocking**:
   - Defended against shell inspection commands:
     - PowerShell: `Get-Content`, `gc`, `Select-String`, `sls`, `Copy-Item`, `cp`, `Move-Item`, `mv`
     - Shell/CMD: `type`, `cat`, `more`, `head`, `tail`, `grep`, `findstr`
     - PowerShell .NET: `[System.IO.File]::ReadAllText(...)`
     - Python: `python -c "open('compile_shard.py').read()"`
   - Distinguishes compiler CLI execution (`python compile_shard.py ...` or `& "d:\path\python.exe" compile_shard.py ...`) via dedicated `PYTHON_EXEC_PATTERN` anchored at command start, so compiler scripts execute without false positives.
   - Enforces hard block on ANY command referencing `judge_ground_truth.json` or tampering with `.check_attempts`.
2. **Windows Path Traversal & Evasion Hardening**:
   - URL-decoded (`urllib.parse.unquote`), stripped `file:///` URIs, normalized slashes (`\` -> `/`), stripped `./` prefixes, and lowercased matching.
   - Blocks path traversal attempts (e.g., `..\.check_attempts\shard_01.json`).
3. **Compiler & Engine Modification Protection**:
   - Added write/edit tool guards on `compile_shard.py`, `check_templates.py`, `compile_cta.py`, `check_cta.py`, `cta_merge.py`, `engine/`, `validator/`, `judge_ground_truth.json`.
4. **Director Diet Precision**:
   - Allows Director to read `work/dispatch/items/*.json`, `work/dispatch/types/*.json`, `work/logs/*.log`, `work/state.json`, and `work/judge_report.json`.
   - Denies Director reading/editing `*_data.py`, `shard_fixes/*.py`, and `judge_responses*.json`.
5. **Auditor Exemption**:
   - Checks `exempt_conversation_ids` array in `.c2c_subagent_lock.json` to allow QA/auditor agents full inspection access.
6. **docs/hooks.md Schema Adherence**:
   - Strict camelCase and snake_case tolerance on stdin.
   - Valid stdout JSON `{"decision": "allow" | "deny", "reason": "..."}`.
   - Always exits code 0 with fail-open fallback.
   - Benchmark: 1,000 evaluations in < 250 ms (< 0.25 ms per call).

### B. Budget Watchdog (`.agents/skills/content-to-course/budget_guard.py`)
1. **Live Truncated JSONL Resilience**:
   - Safe reading via `read_text(encoding="utf-8", errors="replace")`.
   - Skips partial trailing lines during active subagent write cycles without throwing `JSONDecodeError`.
   - Computes fallback turn counts strictly from valid parsed JSON entries.
2. **Brain Transcript Resolution Fallback**:
   - Checks both `transcript.jsonl` and `transcript_full.jsonl` in `.system_generated/logs/` and `brain/<id>/`.
3. **Empty File Handling**:
   - Returns zeroed metrics without crashing.

### C. Unit & Adversarial Tests (`tests/test_watchdog_and_hooks.py`)
- Doubled test suite from 12 to 24 tests.
- 100% pass rate:
  - `tests/test_watchdog_and_hooks.py`: 24 passed in 0.52s.
  - `tests/test_orchestration_resilience.py`: 16 passed in 0.23s.
  - Total: **40 passed in 0.68s**.

---

## 2. Invariants & Verification Checklist

- [x] **Strict Write Boundaries**: Only modified `budget_guard.py`, `c2c_hook_guard.py`, `test_watchdog_and_hooks.py`, and `stream_1d_impr/*`.
- [x] **`.agents/hooks.json` Prevention**: Verified `Test-Path ".agents/hooks.json"` is `False`. Only `.agents/hooks.template.json` exists.
- [x] **Zero Destructive Git Commands**: No commits, resets, or checkouts executed.
- [x] **Performance SLA**: Hook guard executes in < 0.25 ms per evaluation (< 50 ms budget).
- [x] **No Artifact Metadata in Non-Artifact Files**: Clean file writes throughout.

---

## 3. Ready for Phase 3 Auditor

All improvement and hardening objectives from `DISPATCH.md` have been fulfilled and verified. Handing off to Phase 3 Auditor (`audit_1d`).
