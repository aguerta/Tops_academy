# Milestone 4 Execution Plan — Generation 3

## Goal
Attain final certification and closure of the "Top's Academy" project.

## Concrete Steps

### Step 1: Distractor Homogeneity & Centroid Calibration in `batch_generator.py`
- Dispatch worker `worker_distractor_calibration` to:
  1. Inspect `tests/test_blind_guess_empirical.py` and `.agents/skills/content-to-course/batch_generator.py`.
  2. Analyze the heuristic solver in `test_blind_guess_empirical.py` (which exploits length outliers, token overlap with other options, or centroid clustering).
  3. Calibrate distractors in `batch_generator.py` so that:
     - All 7 options share homogeneous length, vocabulary, LaTeX structure, and token overlap.
     - The correct answer is NOT the centroid (e.g. distractors are generated with balanced pairwise distances and mutual overlaps so the correct answer doesn't sit conspicuously in the center or on the periphery of the token distribution).
     - Distractors strictly represent real misconceptions / variation parameters.
  4. Run `python tests/test_blind_guess_empirical.py` to confirm the empirical blind-guess rate drops to <= 30.0% (chance is ~14.3%).
  5. Run unit & pipeline tests: `pytest tests/test_skill.py tests/test_validator.py`.

### Step 2: Regenerate & Strictly Validate `courses/pde_course.json`
- Regenerate the official 500-question PDE course using the calibrated skill generator:
  `python .agents/skills/content-to-course/run.py --pdf sample_content/I__Ecuaciones_en_derivadas_parciales_2026.pdf --output-dir courses --course-id pde_course`
- Run strict validation:
  `python -m validator.cli courses/pde_course.json --strict`
- Confirm all 500 questions, 21 competencies pass all 16 validator rules (including length anti-giveaway rules and options counts).

### Step 3: Empirical Blind-Guess Verification
- Run `python tests/test_blind_guess_empirical.py` directly against the newly generated `courses/pde_course.json`.
- Confirm accuracy on >=40 sampled bare MC items is strictly <= 30.0%.

### Step 4: Full Consolidated Test Suite & Playwright E2E Verification
- Run consolidated test suite:
  `python -m pytest tests/test_validator.py tests/test_skill.py tests/test_platform.py -v`
- Run Playwright headless E2E browser suite:
  `python -m pytest tests/e2e/ -v`
- Confirm all tests pass with 0 failures and 0 console errors.

### Step 5: Acceptance Criteria Verification & Sentinel Reporting
- Check off all Acceptance Criteria in `ORIGINAL_REQUEST.md` and `PROJECT.md`.
- Formulate comprehensive final delivery report and communicate to Sentinel (`7e638524-1a06-4e86-8bac-6392dd5a5ea4`).
