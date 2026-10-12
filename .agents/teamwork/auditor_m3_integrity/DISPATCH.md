# Dispatch for Auditor M3 Integrity (Forensic Audit)

## Objective
Forensic integrity audit of Milestone 3 (Content-to-Course Antigravity Skill):
1. Static analysis of `.agents/skills/content-to-course/`:
   - Verify authentic implementation: genuine PDF parsing (`fitz` / `pdfplumber`), genuine Cognitive Task Analysis, genuine SymPy mathematical verification, genuine auto-repair logic.
   - Verify NO mock facades, no hardcoded answer dictionaries, no bypasses of validator rules.
2. Verify that generated courses contain genuine mathematical questions, authentic distractors, and properly escaped LaTeX.
3. Verify test runs: `pytest tests/unit/test_skill_pipeline.py -v`.
4. Issue binary verdict in `handoff.md`: CLEAN or INTEGRITY VIOLATION.

## Specifications
- `g:\Mi unidad\Competence_analyser\.agents\teamwork\ORIGINAL_REQUEST.md`
- `g:\Mi unidad\Competence_analyser\PROJECT.md`
- `g:\Mi unidad\Competence_analyser\.agents\skills\content-to-course/`


## 2026-10-11T06:59:11Z
You are a Forensic Integrity Auditor (auditor_m3_integrity) conducting an integrity audit of Milestone 3: Content-to-Course Antigravity Skill.

Your Working Directory: g:\Mi unidad\Competence_analyser\.agents\teamwork\auditor_m3_integrity
Project Root: g:\Mi unidad\Competence_analyser
Authoritative Specifications:
- g:\Mi unidad\Competence_analyser\.agents\teamwork\ORIGINAL_REQUEST.md
- g:\Mi unidad\Competence_analyser\PROJECT.md
- Implementation in `.agents/skills/content-to-course/`
- Test suite in `tests/unit/test_skill_pipeline.py`

Your Tasks:
1. Conduct forensic static analysis across `.agents/skills/content-to-course/`:
   - Verify authentic implementation: genuine PDF text extraction, genuine Cognitive Task Analysis, genuine SymPy mathematical verification, genuine auto-repair logic.
   - Verify that there are NO dummy facades, no hardcoded answer dictionaries, and no validator circumventions.
2. Verify that generated course files contain authentic mathematical questions, real distractors, and properly escaped LaTeX.
3. Verify test runs: `python -m pytest tests/unit/test_skill_pipeline.py -v`.
4. Provide a binary verdict in `g:\Mi unidad\Competence_analyser\.agents\teamwork\auditor_m3_integrity\handoff.md`:
   - `Verdict: CLEAN`
   - `Verdict: INTEGRITY VIOLATION`
5. Send a completion message back to the orchestrator (conversation ID: 7609f41d-901b-455e-a8d4-9ddd5b18b728).
