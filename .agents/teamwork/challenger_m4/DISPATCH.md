# DISPATCH — challenger_m4

**Assigned Agent**: challenger_m4
**Archetype**: teamwork_preview_challenger
**Working Directory**: g:\Mi unidad\Competence_analyser\.agents\teamwork\challenger_m4
**Project Root**: g:\Mi unidad\Competence_analyser
**Parent Conversation ID**: 87578499-9730-4cff-803f-777aa442c303 (Orchestrator Gen 3)
**Authoritative Specs**:
- `g:\Mi unidad\Competence_analyser\.agents\teamwork\ORIGINAL_REQUEST.md`
- `g:\Mi unidad\Competence_analyser\PROJECT.md`
- `g:\Mi unidad\Competence_analyser\.agents\teamwork\worker_distractor_calibration\handoff.md`

## Objective
Independently and empirically challenge and verify Milestone 4 deliverables:
1. Run `python tests/test_blind_guess_empirical.py` on `courses/pde_course.json`.
   - Verify sample ($N=50$) and full population ($N=250$) accuracy rates.
   - Confirm empirical adversarial blind guess rate is strictly <= 30.0% (target acceptance criterion).
2. Verify strict validator execution on both course banks:
   - `python -m validator.cli courses/pde_course.json --strict` (exit code 0)
   - `python -m validator.cli courses/demo_course.json --strict` (exit code 0)
3. Run the consolidated test suite:
   - `python -m pytest tests/test_validator.py tests/test_skill.py tests/test_platform.py -v`
4. Run the Playwright headless E2E browser test suite:
   - `python -m pytest tests/e2e/ -v`
5. Verify `python run_platform.py` / root launcher availability and documentation.
6. Provide an empirical challenge verdict (APPROVE or CHALLENGE_FAILED) in your `handoff.md` and send_message back with your findings.


## 2026-10-11T16:01:05Z
You are challenger_m4. Your working directory is g:\Mi unidad\Competence_analyser\.agents\teamwork\challenger_m4.
Read your instructions in g:\Mi unidad\Competence_analyser\.agents\teamwork\challenger_m4\DISPATCH.md.
Also read g:\Mi unidad\Competence_analyser\.agents\teamwork\ORIGINAL_REQUEST.md and g:\Mi unidad\Competence_analyser\.agents\teamwork\worker_distractor_calibration\handoff.md.

Run all empirical tests:
1. python tests/test_blind_guess_empirical.py
   Confirm sample (N=50) and full population (N=250) adversarial guess rate <= 30.0%.
2. python -m validator.cli courses/pde_course.json --strict
   python -m validator.cli courses/demo_course.json --strict
   Confirm both exit 0.
3. python -m pytest tests/test_validator.py tests/test_skill.py tests/test_platform.py -v
   Confirm all tests pass.
4. python -m pytest tests/e2e/ -v
   Confirm all Playwright browser tests pass.

Write your handoff.md with your empirical findings and verdict (APPROVE or CHALLENGE_FAILED) and send_message back to parent.
