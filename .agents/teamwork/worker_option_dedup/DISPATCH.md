# DISPATCH — worker_option_dedup

**Assigned Agent**: worker_option_dedup
**Archetype**: teamwork_preview_worker
**Working Directory**: g:\Mi unidad\Competence_analyser\.agents\teamwork\worker_option_dedup
**Project Root**: g:\Mi unidad\Competence_analyser
**Parent Conversation ID**: 87578499-9730-4cff-803f-777aa442c303 (Orchestrator Gen 3)
**Authoritative Specs**:
- `g:\Mi unidad\Competence_analyser\.agents\teamwork\ORIGINAL_REQUEST.md`
- `g:\Mi unidad\Competence_analyser\PROJECT.md`
- `g:\Mi unidad\Competence_analyser\.agents\teamwork\auditor_m4_integrity\handoff.md`

## MANDATORY INTEGRITY WARNING
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A forensic auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Objective
Remediate the option collision and duplicate option defect identified by the forensic auditor in `.agents/skills/content-to-course/batch_generator.py`, regenerate `courses/pde_course.json`, and verify zero duplicates, strict validation, and blind-guess rate <= 30.0%.

## Detailed Tasks
1. Read `auditor_m4_integrity/handoff.md` (specifically Section 1.3 and Section 4).
2. In `.agents/skills/content-to-course/batch_generator.py`:
   - Fix Line 765 in `C-02`: Replace the duplicated string with a distinct pedagogical misconception (e.g., `"El campo vectorial es asintótico en cada punto regular a la superficie integral, parametrizando la curvatura principal."`).
   - Fix parametric generators in `H-01`, `H-04`, `Hab-04`, `Hab-08` to prevent parameters from colliding (`b_val != c_val`, `a_val != b_val`, `alpha * beta != deg`, etc.).
   - Add a robust deduplication safeguard in `generate_multiple_choice` or distractor processing: ensure `len(set(o['content'].strip() for o in options)) == 7`. If any distractor collides with the correct answer or another distractor, replace it with an authentic variation so that all 7 options are 100% unique.
3. Regenerate `courses/pde_course.json`:
   `python .agents/skills/content-to-course/run.py --pdf sample_content/I__Ecuaciones_en_derivadas_parciales_2026.pdf --output-dir courses --course-id pde_course`
4. Run the duplicate check script from the auditor report:
   ```python
   python -c "
   import json
   c = json.load(open('courses/pde_course.json', encoding='utf-8'))
   dups = [q['id'] for q in c['questions'] if q.get('interaction_type') == 'multiple_choice_7_options' and len(set(o['content'].strip() for o in q['options'])) != len(q['options'])]
   print(f'Total questions with duplicate options: {len(dups)}')
   assert len(dups) == 0, f'Found {len(dups)} duplicate option questions: {dups[:5]}'
   "
   ```
   Must confirm: `Total questions with duplicate options: 0`.
5. Run `python tests/test_blind_guess_empirical.py` to confirm the blind-guess accuracy rate remains <= 30.0% (target acceptance criterion).
6. Run `python -m validator.cli courses/pde_course.json --strict` (must exit 0).
7. Run consolidated test suite:
   `python -m pytest tests/test_validator.py tests/test_skill.py tests/test_platform.py -v`
8. Run Playwright E2E suite:
   `python -m pytest tests/e2e/ -v`
9. Write `handoff.md` in your working directory and notify the orchestrator via send_message.


## 2026-10-11T16:16:55Z
You are worker_option_dedup. Your working directory is g:\Mi unidad\Competence_analyser\.agents\teamwork\worker_option_dedup.
Read your instructions in g:\Mi unidad\Competence_analyser\.agents\teamwork\worker_option_dedup\DISPATCH.md.
Also read g:\Mi unidad\Competence_analyser\.agents\teamwork\auditor_m4_integrity\handoff.md.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A forensic auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Your task:
1. Fix the duplicate distractor and parametric collisions in .agents/skills/content-to-course/batch_generator.py as identified in the auditor handoff report (C-02 line 765, H-01, H-04, Hab-04, Hab-08 parameter ranges).
2. Add a robust deduplication safeguard in generate_multiple_choice / distractor synthesis so that every multiple choice question has 7 strictly unique options (len(set(options)) == 7).
3. Regenerate courses/pde_course.json:
   python .agents/skills/content-to-course/run.py --pdf sample_content/I__Ecuaciones_en_derivadas_parciales_2026.pdf --output-dir courses --course-id pde_course
4. Verify 0 duplicate options across all 250 MC questions.
5. Verify blind-guess accuracy rate <= 30.0%:
   python tests/test_blind_guess_empirical.py
6. Verify strict course validation:
   python -m validator.cli courses/pde_course.json --strict (exit 0)
7. Run all tests:
   python -m pytest tests/test_validator.py tests/test_skill.py tests/test_platform.py -v
   python -m pytest tests/e2e/ -v
8. Write handoff.md and send_message back with your results.
