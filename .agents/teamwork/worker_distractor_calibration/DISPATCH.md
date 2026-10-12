# DISPATCH — worker_distractor_calibration

**Assigned Agent**: worker_distractor_calibration
**Archetype**: teamwork_preview_worker
**Working Directory**: g:\Mi unidad\Competence_analyser\.agents\teamwork\worker_distractor_calibration
**Project Root**: g:\Mi unidad\Competence_analyser
**Parent Conversation ID**: 87578499-9730-4cff-803f-777aa442c303 (Orchestrator Gen 3)
**Authoritative Specs**:
- `g:\Mi unidad\Competence_analyser\.agents\teamwork\ORIGINAL_REQUEST.md`
- `g:\Mi unidad\Competence_analyser\PROJECT.md`

## MANDATORY INTEGRITY WARNING
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A forensic auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Objective
Calibrate distractor generation in `.agents/skills/content-to-course/batch_generator.py` so that distractor options for multiple-choice questions have homogeneous token overlap, structure, and length, ensuring that `python tests/test_blind_guess_empirical.py` achieves <= 30.0% accuracy across >=40 randomly sampled multiple-choice questions (chance is ~14.3% with 7 options).

## Tasks & Instructions
1. Inspect `tests/test_blind_guess_empirical.py` and understand how the empirical blind guess solver guesses options (e.g., token overlap / centroid heuristic, length scoring, etc.).
2. Inspect `.agents/skills/content-to-course/batch_generator.py` (specifically how distractors are constructed, formatted, and padded for multiple choice items).
3. Calibrate the distractor generation logic so that:
   - All 7 options share homogeneous token overlap, vocabulary, LaTeX formatting, and lengths.
   - Distractors represent genuine pedagogical misconceptions or systematic mathematical parameter variations.
   - The correct answer is NOT the centroid of token overlap (or an outlier in token distribution). Ensure distractors have pairwise mutual overlap and balanced variation so heuristic centroid / intersection scoring cannot single out the correct option.
4. Run `python tests/test_blind_guess_empirical.py` to confirm empirical blind guess accuracy is strictly <= 30.0%.
5. Regenerate `courses/pde_course.json`:
   `python .agents/skills/content-to-course/run.py --pdf sample_content/I__Ecuaciones_en_derivadas_parciales_2026.pdf --output-dir courses --course-id pde_course`
6. Verify strict validation on the regenerated course:
   `python -m validator.cli courses/pde_course.json --strict`
7. Re-run `python tests/test_blind_guess_empirical.py` on the regenerated `courses/pde_course.json` to confirm accuracy <= 30.0%.
8. Run the consolidated test suite and Playwright headless E2E suite:
   `python -m pytest tests/test_validator.py tests/test_skill.py tests/test_platform.py -v`
   `python -m pytest tests/e2e/ -v`
9. Document your changes, commands run, test outputs, and final empirical guess rate in `handoff.md` in your working directory, and message back your completion report.

## 2026-10-11T15:40:10Z
Received dispatch from 87578499-9730-4cff-803f-777aa442c303:
- Calibrate distractor generation in .agents/skills/content-to-course/batch_generator.py so distractors have homogeneous token overlap, vocabulary, and length distributions, preventing heuristic solvers (such as centroid/intersection scoring in tests/test_blind_guess_empirical.py) from guessing the answer.
- Confirm blind guess rate <= 30.0%.
- Regenerate courses/pde_course.json: python .agents/skills/content-to-course/run.py --pdf sample_content/I__Ecuaciones_en_derivadas_parciales_2026.pdf --output-dir courses --course-id pde_course
- Verify strict validation: python -m validator.cli courses/pde_course.json --strict
- Re-run blind guess test on pde_course.json (<= 30.0%).
- Run consolidated test suite and Playwright E2E suite.
- Write handoff.md and send_message back.
