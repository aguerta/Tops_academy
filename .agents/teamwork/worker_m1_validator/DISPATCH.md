## 2026-10-11T01:07:24Z

You are the Milestone 1 Worker for the "Top's Academy" project.
Your working directory is: g:\Mi unidad\Competence_analyser\.agents\teamwork\worker_m1_validator
Read g:\Mi unidad\Competence_analyser\.agents\teamwork\ORIGINAL_REQUEST.md immediately.
Read g:\Mi unidad\Competence_analyser\PROJECT.md and g:\Mi unidad\Competence_analyser\.agents\teamwork\spec_miner_format\format_spec.md for the complete specification.

Write ownership: You exclusively own `src/validator/`, `tests/validator/`, and `courses/fixtures/`.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Your task:
1. Implement the complete Exercise Bank Format Validator in Python (`src/validator/`):
   - `lexical_scanner.py`: Pre-parse lexical pass scanning raw file characters for:
     * Invalid JSON escapes (e.g. `\Delta`, `\sigma`, `\alpha`, etc.)
     * Silent control character escapes (`\b` 0x08, `\t` 0x09, `\f` 0x0C, `\n` 0x0A, `\r` 0x0D, `\0` 0x00, `\v` 0x0B) where a LaTeX command was accidentally unescaped (e.g. `\text`, `\frac`, `\nu`, `\tau`, `\rho`, `\beta`, `\theta`)
     * Unescaped newlines/quotes inside strings
   - `schema_validator.py`: JSON Schema (Draft-07) validation for course metadata, competencies, questions, graphs, options, hints, solutions, and misconception warnings.
   - `rules.py` & `psychometric_checker.py`:
     * Question types: `multiple_choice_7_options` (must have exactly 7 options, exactly 1 correct); `multiple_select` (correct count between 1 and n-1); `fill_in_the_blank` (has expression/value).
     * Hints: between 3 and 5 hints per question.
     * Duplicate IDs: all question IDs and competency IDs must be unique.
     * Referential integrity: every question `competency_id` must match a declared competency in the course.
     * Minimum question counts: >= 30 questions for each Skill [Hab] competency; >= 20 questions for each Fact [H] / Concept [C] competency.
     * Anti-giveaway per item: correct option length cannot be more than 20% longer than the longest distractor, nor more than 20% shorter than the shortest distractor (bound: [0.80 * min(D), 1.20 * max(D)]).
     * Anti-giveaway per course: across all multiple-choice items in the course, the correct option cannot be the longest option (strictly or tied) in more than 25% of items, nor the shortest in more than 25%.
   - `cli.py`: Command-line tool runnable via `python -m src.validator.cli <file>` (and entry point `validate-course`).
     * Exits 0 on valid course.
     * Exits 1 on validation errors with formatted diagnostic messages detailing rule ID, question/competency ID, and reason.
     * Exits 2 on missing file or internal I/O errors.
2. Build comprehensive automated test suite and fixtures in `tests/validator/`:
   - Automated tests (`test_validator.py`) using `pytest`.
   - Fixture suite covering ALL 16 rules, including:
     * Original `system_prompts/output_example_exercises.json` unmodified (MUST fail with exit 1).
     * Skill competency with 29 questions (MUST fail with exit 1).
     * Fact/Concept competency with 19 questions (MUST fail with exit 1).
     * Item length giveaway too long (>20% longer) (MUST fail with exit 1).
     * Item length giveaway too short (>20% shorter) (MUST fail with exit 1).
     * Course length giveaway longest >25% (MUST fail with exit 1).
     * Course length giveaway shortest >25% (MUST fail with exit 1).
     * LaTeX invalid escape (`\Delta`) (MUST fail with exit 1).
     * LaTeX silent control escape (`\text`, `\frac`, `\nu`) (MUST fail with exit 1).
     * MCQ with 6 or 8 options (MUST fail with exit 1).
     * MCQ with 0 or 2 correct (MUST fail with exit 1).
     * Multi-select with 0 or all correct (MUST fail with exit 1).
     * Hints <3 or >5 (MUST fail with exit 1).
     * Duplicate IDs (MUST fail with exit 1).
     * Missing competency reference (MUST fail with exit 1).
     * Fully valid baseline course (MUST exit 0).
3. Execute the tests (`python -m pytest tests/validator` and CLI invocations against all fixtures). Confirm all pass.
4. Write your completion report in `g:\Mi unidad\Competence_analyser\.agents\teamwork\worker_m1_validator\handoff.md` with:
   - All files created
   - Test execution commands and full passing output
   - Fixture verification results
5. Send a message to parent when finished.
