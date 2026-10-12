## 2026-10-11T00:59:48Z
You are the Competence Analysis & Skill Pipeline Spec Miner for the "Top's Academy" project.
Your working directory is: g:\Mi unidad\Competence_analyser\.agents\teamwork\spec_miner_skill
Read g:\Mi unidad\Competence_analyser\.agents\teamwork\ORIGINAL_REQUEST.md immediately.

Your task:
1. Examine R3 and R4 requirements and Skill Acceptance Criteria in ORIGINAL_REQUEST.md.
2. Inspect g:\Mi unidad\Competence_analyser\system_prompts\prompt_competence_analyser.md, g:\Mi unidad\Competence_analyser\system_prompts\output_example_competences.md, and g:\Mi unidad\Competence_analyser\sample_content\I__Ecuaciones_en_derivadas_parciales_2026.pdf.
3. Analyze the PDE PDF: topics, sections, language (Spanish), mathematical depth, page count, and competence extraction feasibility.
4. Formulate the architecture for the Antigravity skill in .agents/skills/:
   - SKILL.md definition and invocation protocol
   - Extraction pipeline (PDF text & formulas)
   - Cognitive Task Analysis step (Facts, Concepts, Skills, blind spots, automation seeds)
   - Exercise generation strategy (>=30 per Skill, >=20 per Fact/Concept, all 3 types, graphs, plausible distractors, no giveaway cues, batching to handle large courses reliably)
   - Independent verification step for answer keys
   - Automated R2 validator check & iterative repair loop
   - Course publication to platform's courses directory
5. Design the methodology for:
   - Question audit (sample >=40 questions, >=95% accuracy)
   - Blind-guess test (sample >=40 MC items with stem/hints removed, <=30% guess rate)
   - Converting output_example_exercises.json into a valid demo course
6. Document your findings in g:\Mi unidad\Competence_analyser\.agents\teamwork\spec_miner_skill\skill_spec.md and handoff.md in your working directory.
7. Send a message to your parent with the path to your completed report.
