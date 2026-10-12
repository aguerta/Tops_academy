# DISPATCH — worker_m4_courses

## Mission
Author and validate the official Milestone 4 course files:
1. `courses/pde_course.json` (500 questions generated from `sample_content/I__Ecuaciones_en_derivadas_parciales_2026.pdf` using `.agents/skills/content-to-course/run.py`).
2. `courses/demo_course.json` (complete, valid demo course derived from `system_prompts/output_example_exercises.json`, satisfying all quotas and anti-giveaway rules).
Both courses must strictly pass `python -m validator.cli <file> --strict`.
## 2026-10-11T11:28:05Z
You are a Worker (worker_m4_courses) responsible for authoring and validating both official course deliverables for Milestone 4:
1. `courses/pde_course.json`
2. `courses/demo_course.json`

Your Working Directory: g:\Mi unidad\Competence_analyser\.agents\teamwork\worker_m4_courses
Project Root: g:\Mi unidad\Competence_analyser
Authoritative Specifications:
- g:\Mi unidad\Competence_analyser\.agents\teamwork\ORIGINAL_REQUEST.md
- g:\Mi unidad\Competence_analyser\PROJECT.md
- Validator CLI: `python -m validator.cli <file> --strict`
- Skill CLI: `python .agents/skills/content-to-course/run.py`
- Source PDF: `sample_content/I__Ecuaciones_en_derivadas_parciales_2026.pdf`
- Guide Example Exercises: `system_prompts/output_example_exercises.json`

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A forensic auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Your Tasks:
1. Generate Official PDE Course:
   Execute the skill pipeline:
   ```bash
   python .agents/skills/content-to-course/run.py --pdf sample_content/I__Ecuaciones_en_derivadas_parciales_2026.pdf --output-dir courses --course-id pde_course --audit-sample 10
   ```
   Verify that `courses/pde_course.json` is generated, contains all 21 competencies with >=30 questions per Skill [Hab] and >=20 questions per Fact [H] / Concept [C] (500 questions total), with zero unescaped LaTeX errors, valid anti-giveaway metrics, and clean answer keys.
   Validate with:
   ```bash
   python -m validator.cli courses/pde_course.json --strict
   ```
   Exit code must be 0 (`VALID`).

2. Convert and Author Official Demo Course (`courses/demo_course.json`):
   Inspect `system_prompts/output_example_exercises.json`.
   Note: The guide file has raw LaTeX backslash corruptions (`\Delta`, `\text`, `\frac`, etc.), insufficient question counts, and giveaway option lengths.
   Author a clean script or builder (e.g. `scripts/build_demo_course.py`) that converts the concepts and exercises from `output_example_exercises.json` into a complete, valid Top's Academy course `courses/demo_course.json`:
   - Proper JSON escaping: all LaTeX commands must be properly escaped (`\\Delta`, `\\frac`, `\\text`, etc.).
   - Competencies defined with proper metadata (`category`: Skill, Concept, Fact).
   - Meet all minimum question quotas: at least 30 questions per Skill competency, at least 20 per Fact/Concept competency.
   - Mix of interaction types: `multiple_choice_7_options`, `fill_in_the_blank`, `multiple_select`.
   - Pedagogical scaffolding: 3-5 hints per item, step-by-step solution, misconception warning.
   - Anti-giveaway guarantees:
     * Item-level length bounds: `0.80 * min(distractors) <= len(correct) <= 1.20 * max(distractors)`.
     * Course-level distribution: correct option is longest in <=25% and shortest in <=25% of MC items across the course.
   - Validate with:
   ```bash
   python -m validator.cli courses/demo_course.json --strict
   ```
   Exit code must be 0 (`VALID`).

3. Verify Platform Course Discovery:
   Check that both `courses/pde_course.json` and `courses/demo_course.json` are properly discoverable in `courses/`.

4. Document all commands, line counts, question counts, and verbatim validation outputs in `g:\Mi unidad\Competence_analyser\.agents\teamwork\worker_m4_courses\handoff.md`.
   Provide verdict: `Verdict: DONE (both courses valid)` or `FAILED`.
5. Send completion message back to the orchestrator (conversation ID: 7609f41d-901b-455e-a8d4-9ddd5b18b728).
