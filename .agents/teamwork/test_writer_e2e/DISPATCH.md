## 2026-10-11T01:07:24Z
You are the E2E Test Suite Writer for the "Top's Academy" project.
Your working directory is: g:\Mi unidad\Competence_analyser\.agents\teamwork\test_writer_e2e
Read g:\Mi unidad\Competence_analyser\.agents\teamwork\ORIGINAL_REQUEST.md immediately.
Read g:\Mi unidad\Competence_analyser\PROJECT.md and g:\Mi unidad\Competence_analyser\.agents\teamwork\explorer_ui_survey\ui_spec.md.

Write ownership: You exclusively own `tests/e2e/`, `TEST_INFRA.md`, and `TEST_READY.md`.

Your task:
1. Create `TEST_INFRA.md` at project root (`g:\Mi unidad\Competence_analyser\TEST_INFRA.md`) following the template in instructions:
   - Test philosophy (opaque-box, requirement-driven derived from ORIGINAL_REQUEST.md).
   - Feature inventory mapping to test tiers.
   - Test architecture: Playwright (Node or Python, runnable with one command, e.g. `npm.cmd run test:e2e` or `python -m pytest tests/e2e`), pass/fail semantics, headless browser configuration.
   - 4-Tier test methodology (Tier 1 Feature coverage, Tier 2 Boundary & Corner, Tier 3 Cross-feature combinations, Tier 4 Real-world application scenarios).
2. Implement the automated headless browser test suite in `tests/e2e/`:
   - Setup Playwright test configuration for headless execution on Windows (Chrome/Chromium).
   - Implement tests covering ALL Platform Acceptance Criteria in ORIGINAL_REQUEST.md:
     * Library lists every course in `courses/` folder; copying a new valid course file into the folder makes it appear after reload with no code change.
     * An invalid course file shows an error for that course while other courses still work.
     * Course overview shows one unit per competency, mastery legend, and course mastery %.
     * Full practice session: wrong answer -> incorrect feedback; hint reveal shows hints in order; correct answer -> "Good work" toast & step-by-step solution available; completion screen shows score.
     * Randomization: across repeated sessions of the same unit, both question order and option order differ (asserting orders are not identical and do not mirror JSON order), while grading stays correct after shuffling.
     * Each interaction type graded correctly, including equivalent algebraic answers (`1-(alpha+n)*sigma` accepted for `1 - \alpha\sigma - n\sigma`; `0.5` accepted for `1/2`) and all-or-nothing for multiple-select.
     * Mastery level changes after practice and persists after reload.
     * Quiz, unit test, and course challenge (~30 questions drawn across units) can be started and completed.
     * Question with graph renders graph (verified via DOM/canvas/svg elements).
     * No console errors during test run; all tests pass.
   - Also prepare automated test runner for visual fidelity screenshot capture (capturing the 6 platform states so reviewer agent can compare against reference screenshots).
3. Provide sample mock/test courses in `courses/test_fixtures/` to allow running the test suite independently.
4. When the test harness and test cases are ready, publish `TEST_READY.md` at project root with command, coverage summary, and feature checklist.
5. Write your handoff report in `g:\Mi unidad\Competence_analyser\.agents\teamwork\test_writer_e2e\handoff.md` and send a message to parent.
