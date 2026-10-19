# Dispatch: Gate 0 Forensic Auditor

## Identity
- Role: Gate 0 Forensic Auditor
- Type: teamwork_preview_auditor
- Working Directory: d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/auditor_gate0/
- Parent Conversation ID: e831bfe5-b034-48b8-9c7e-f1ebfdfd3200

## Assigned Mission
Perform strict independent adversarial forensics on Gate 0 (Requirement 1 / P0 Data Safety & Legacy Artifact Purge).
You MUST verify:
1. `delete_course.py`:
   - Inspect `clean_orphan_course_dirs`.
   - Confirm it CANNOT delete any workspace containing `work/state.json`, `work/pre_cta_manifest.json`, `work/cta_data.py`, or any file modified in the last 24 hours.
   - Confirm `COURSES_DIR` override via environment variable is functional.
2. `tests/test_delete_course.py`:
   - Inspect test implementations.
   - Confirm `test_clean_orphan_dirs` is strictly isolated using `tmp_path` and `monkeypatch`.
   - Confirm tests verify: live workspace survives, recent file survives, old orphan is cleaned, real `courses/` directory is never touched.
   - Run `python -m pytest tests/test_delete_course.py -q` and inspect results.
3. `assemble.py`:
   - Confirm `frac_simple_fix` regex uses `[^{}\\^_]+` instead of `[^{}\\]+`.
4. Legacy Purge:
   - Check `dispatch.py`, `run.py`, `SKILL.md`, `system_prompts/`, `README.md`, `PROJECT.md`.
   - Verify zero occurrences of `corpus.md` and `section_*.md` fallbacks or misleading stdout prints.
5. Anti-Cheating & Integrity:
   - Zero mocks, zero hardcoded bypasses, zero weakened assertions.
   - If any violation is found, report INTEGRITY VIOLATION (binary veto). If completely genuine, robust, and verified, certify formal PASS.

Output:
Write `handoff.md` with:
- Detailed verification evidence chain
- Verdict: PASS or INTEGRITY VIOLATION / FAIL
- Message parent orchestrator via `send_message`.

## 2026-10-19T04:14:41Z
You are the Gate 0 Independent Forensic Auditor.
Your working directory is: d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/auditor_gate0/

You MUST read and follow:
1. d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/ORIGINAL_REQUEST.md (under header ## 2026-10-19T03:49:57Z)
2. d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/auditor_gate0/DISPATCH.md
3. Worker handoff: d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/worker_gate0/handoff.md
4. d:/Augusto/Downloads/c2c_hardening_plan.md (§5 P0 Data safety)
5. d:/Augusto/personal_portfolio/Tops_academy/reports/c2c_audits/master_forensic_synthesis_7_runs.md (§3.1)

Your mission:
Perform an independent adversarial forensic audit of Gate 0 (Requirement 1 / P0 Data Safety & Legacy Artifact Purge).
Inspect the code changes made by worker_gate0:
1. `.agents/skills/delete-course/scripts/delete_course.py`:
   - Verify `clean_orphan_course_dirs` and `is_active_workspace`.
   - Verify it prevents deletion of any directory containing `work/state.json`, `work/pre_cta_manifest.json`, `work/cta_data.py`, or any file modified <24 hours ago.
   - Verify `COURSES_DIR` override via env var.
2. `tests/test_delete_course.py`:
   - Verify `test_clean_orphan_dirs` is strictly isolated using `tmp_path` and `monkeypatch`.
   - Verify tests check live workspaces, recent files, old orphans, and untouched real `courses/`.
   - Execute the test suite yourself: `python -m pytest tests/test_delete_course.py -v` (or via `pytest.cmd`).
3. `assemble.py`:
   - Verify the 2-line LaTeX regex fix `frac_simple_fix` (`[^{}\\^_]+`).
4. Legacy Purge:
   - Check `dispatch.py`, `run.py`, `SKILL.md`, `system_prompts/`, `README.md`, `PROJECT.md`.
   - Verify zero unmitigated residual references, fallbacks, or stdout prints for `corpus.md` and `section_*.md`.
5. Anti-Cheating & Integrity Analysis:
   - Check git diff and files for artificial mocks, hardcoded bypasses, weakened assertions, or test evasion.
   - Perform worst-case pipeline stress analysis and document boundaries/assumptions.

If any cheat or integrity violation is found, output verdict INTEGRITY VIOLATION.
If fully genuine, robust, and verified, output verdict PASS.
Write a comprehensive `handoff.md` in your working directory and notify the parent orchestrator via `send_message`.
