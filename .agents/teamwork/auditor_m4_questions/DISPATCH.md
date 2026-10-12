## 2026-10-11T11:59:54Z
[Message] timestamp=2026-10-11T11:59:54Z sender=7609f41d-901b-455e-a8d4-9ddd5b18b728 priority=MESSAGE_PRIORITY_HIGH content=You are an independent Forensic Integrity and Quality Auditor (auditor_m4_questions) auditing the question bank of the official PDE course deliverable (`courses/pde_course.json`).

Your Working Directory: g:\Mi unidad\Competence_analyser\.agents\teamwork\auditor_m4_questions
Project Root: g:\Mi unidad\Competence_analyser
Authoritative Specifications:
- g:\Mi unidad\Competence_analyser\.agents\teamwork\ORIGINAL_REQUEST.md
- g:\Mi unidad\Competence_analyser\PROJECT.md
- Official Course File: `courses/pde_course.json`
- Source Academic Content: `sample_content/I__Ecuaciones_en_derivadas_parciales_2026.pdf`
- Competence Analysis Document: `courses/competence_analysis_pde_course.md`

Your Tasks:
1. Load `courses/pde_course.json`.
2. Extract a stratified random sample of at least 40 questions covering all 3 competency categories (Skills, Concepts, Facts) and all 3 interaction types (MC7, FIB, MS).
3. Cross-reference each sampled question against `sample_content/I__Ecuaciones_en_derivadas_parciales_2026.pdf` and `courses/competence_analysis_pde_course.md`:
   - Verification Dimension 1: Answer Key Correctness — Is the designated answer mathematically true and verifiable?
   - Verification Dimension 2: Distractor Coherence — Are distractors plausible mathematical misconceptions rather than nonsensical strings?
   - Verification Dimension 3: Scaffolding Quality — Do the 3-5 progressive hints genuinely guide the student toward the solution without circular jumps?
   - Verification Dimension 4: Competency Alignment — Does the item genuinely evaluate the assigned competency?
4. Calculate the empirical accuracy rate (target: >=95.0%).
5. Document all 40+ evaluated questions in a comprehensive markdown table in your handoff report (`g:\Mi unidad\Competence_analyser\.agents\teamwork\auditor_m4_questions\handoff.md`) with ID, Competency, Question Type, Evaluation, and Pass/Fail status.
6. Provide an explicit verdict in `handoff.md`:
   - Conclude with `Verdict: APPROVE (accuracy = X%)` or `Verdict: REQUEST_CHANGES`.
7. Send a completion message back to the orchestrator (conversation ID: 7609f41d-901b-455e-a8d4-9ddd5b18b728).
