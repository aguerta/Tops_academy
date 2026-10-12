# Dispatch for Challenger M3 Generator (Batch & Psychometrics Stress Test)

## Objective
Adversarially challenge and stress-test `batch_generator.py`:
1. Generate courses with varied seeds and volume demands.
2. Verify strict mathematical adherence to:
   - Volume quotas: >=30 per Skill, >=20 per Fact/Concept.
   - Item-level anti-giveaway length bounding: `0.80 * min(D) <= L_correct <= 1.20 * max(D)`.
   - Course-level length distribution: `longest <= 25%` and `shortest <= 25%`.
   - Option counts: MC7 has exactly 7 options; MS has 4-6 options with 1 to n-1 correct; FIB has empty options array.
   - LaTeX escapes: strict double backslashes in all JSON string outputs.
3. Validate output against `python -m validator.cli <file> --strict`.
4. Issue verdict in `handoff.md`: APPROVE or REQUEST_CHANGES.

## Specifications
- `g:\Mi unidad\Competence_analyser\.agents\teamwork\ORIGINAL_REQUEST.md`
- `g:\Mi unidad\Competence_analyser\PROJECT.md`
- `g:\Mi unidad\Competence_analyser\.agents\skills\content-to-course\batch_generator.py`

## 2026-10-11T06:59:11Z
You are an adversarial Challenger (challenger_m3_generator) stress-testing the batch generator and psychometric anti-giveaway engine.

Your Working Directory: g:\Mi unidad\Competence_analyser\.agents\teamwork\challenger_m3_generator
Project Root: g:\Mi unidad\Competence_analyser
Authoritative Specifications:
- g:\Mi unidad\Competence_analyser\.agents\teamwork\ORIGINAL_REQUEST.md
- g:\Mi unidad\Competence_analyser\PROJECT.md
- Implementation in `.agents/skills/content-to-course/batch_generator.py`

Your Tasks:
1. Empirically challenge `batch_generator.py` with multiple runs and varied parameters.
2. Verify:
   - Quota enforcement: >=30 per Skill, >=20 per Fact/Concept.
   - Item-level length bounding: `0.80 * min(D) <= L_correct <= 1.20 * max(D)`.
   - Course-level distribution: longest <= 25% and shortest <= 25%.
   - Option cardinality: MC7 exactly 7 options; MS 4-6 options with 1 to n-1 correct; FIB empty options.
   - Double-escaped LaTeX JSON in all strings.
3. Validate output against `python -m validator.cli <file> --strict`.
4. Provide a clear verdict in `g:\Mi unidad\Competence_analyser\.agents\teamwork\challenger_m3_generator\handoff.md`:
   - Must conclude with either `Verdict: APPROVE` or `Verdict: REQUEST_CHANGES`.
5. Send a completion message back to the orchestrator (conversation ID: 7609f41d-901b-455e-a8d4-9ddd5b18b728).
