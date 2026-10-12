# DISPATCH — auditor_m4_integrity

**Assigned Agent**: auditor_m4_integrity
**Archetype**: teamwork_preview_auditor
**Working Directory**: g:\Mi unidad\Competence_analyser\.agents\teamwork\auditor_m4_integrity
**Project Root**: g:\Mi unidad\Competence_analyser
**Parent Conversation ID**: 87578499-9730-4cff-803f-777aa442c303 (Orchestrator Gen 3)
**Authoritative Specs**:
- `g:\Mi unidad\Competence_analyser\.agents\teamwork\ORIGINAL_REQUEST.md`
- `g:\Mi unidad\Competence_analyser\PROJECT.md`
- `g:\Mi unidad\Competence_analyser\.agents\teamwork\worker_distractor_calibration\handoff.md`

## Objective
Perform forensic integrity auditing on the changes made to `.agents/skills/content-to-course/batch_generator.py` and the generated courses (`courses/pde_course.json`, `courses/demo_course.json`):
1. **Integrity Forensics**:
   - Verify that there are NO hardcoded test results, test-specific bypasses, dummy or facade implementations.
   - Verify that the distractor calibration does NOT contain fake options, nonsense text, or artificial tricks that bypass the solver while producing unpedagogical questions.
   - Verify that questions and distractors in `courses/pde_course.json` derive authentically from the PDE curriculum and authentic misconceptions.
   - Verify that the blind guess test script `tests/test_blind_guess_empirical.py` is genuine and not compromised or modified to artificially report low scores.
2. Determine verdict: **CLEAN** or **INTEGRITY VIOLATION**.
3. Document evidence and deliver verdict in `handoff.md` in your working directory, and notify the orchestrator via send_message.

## 2026-10-11T16:01:05Z
You are auditor_m4_integrity. Your working directory is g:\Mi unidad\Competence_analyser\.agents\teamwork\auditor_m4_integrity.
Read your instructions in g:\Mi unidad\Competence_analyser\.agents\teamwork\auditor_m4_integrity\DISPATCH.md.
Also read g:\Mi unidad\Competence_analyser\.agents\teamwork\ORIGINAL_REQUEST.md and g:\Mi unidad\Competence_analyser\.agents\teamwork\worker_distractor_calibration\handoff.md.

Perform forensic audit on .agents/skills/content-to-course/batch_generator.py and courses/pde_course.json:
- Check git diff or inspect batch_generator.py and tests/test_blind_guess_empirical.py.
- Ensure no test bypasses, no hardcoded answers, no dummy facades, no corrupted distractor texts.
- Verify that questions and distractors represent authentic PDE mathematical content and misconceptions.
- Write your handoff.md with verdict (CLEAN or INTEGRITY VIOLATION) and send_message back to parent.
