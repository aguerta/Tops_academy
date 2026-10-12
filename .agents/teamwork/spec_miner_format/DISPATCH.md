## 2026-10-11T00:59:48Z
You are the Format & Validator Spec Miner for the "Top's Academy" project.
Your working directory is: g:\Mi unidad\Competence_analyser\.agents\teamwork\spec_miner_format
Read g:\Mi unidad\Competence_analyser\.agents\teamwork\ORIGINAL_REQUEST.md immediately.

Your task:
1. Examine R2 and Validator Acceptance Criteria in ORIGINAL_REQUEST.md.
2. Inspect g:\Mi unidad\Competence_analyser\system_prompts\prompt_creator_exercises.md and g:\Mi unidad\Competence_analyser\system_prompts\output_example_exercises.json.
3. Identify every flaw in output_example_exercises.json, especially LaTeX backslash escaping (including silently-valid escapes producing control characters like \t, \f, \n, \b, \v, \0), unescaped quotes, giveaway patterns (correct option length vs distractors, justification on correct answer).
4. Formulate the exact JSON schema and validator specification for courses, units/competencies, questions, graphs, hints, solutions, and anti-giveaway rules:
   - Invalid JSON detection
   - LaTeX backslash corruption detection
   - Multiple-choice items: exactly 7 options, exactly 1 correct
   - Multiple-select items: correct count between 1 and n-1
   - Fill-in-the-blank items: expected answer / equivalence criteria
   - Hints: between 3 and 5 hints per question
   - Duplicate IDs check
   - Questions referencing missing competencies
   - Minimum question counts: Skill [Hab] >= 30, Fact/Concept >= 20
   - Giveaway rules: per-item length difference <= 20%, per-course correct option longest in <= 25% and shortest in <= 25% of MC items
5. Design the test matrix and fixture files needed to verify the validator.
6. Document your findings in g:\Mi unidad\Competence_analyser\.agents\teamwork\spec_miner_format\format_spec.md and provide a structured handoff.md in your working directory.
7. Send a message to your parent with the path to your completed report.
