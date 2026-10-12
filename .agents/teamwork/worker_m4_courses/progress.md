# Progress — worker_m4_courses

Last visited: 2026-10-11T11:58:00Z

## Status
Tasks completed. Both official course deliverables (`courses/pde_course.json` and `courses/demo_course.json`) generated, strictly validated, and verified on platform discovery.

## Checklist
- [x] 1. Generate and validate official PDE course (`courses/pde_course.json`)
  - Skill pipeline executed on `sample_content/I__Ecuaciones_en_derivadas_parciales_2026.pdf`
  - 500 questions across 21 competencies (8 Skills >=30, 6 Concepts >=20, 7 Facts >=20)
  - `python -m validator.cli courses/pde_course.json --strict` -> VALID (exit code 0)
- [x] 2. Author, generate, and validate official Demo course (`courses/demo_course.json`)
  - Authored `scripts/build_demo_course.py`
  - Converted and repaired all 7 exercises from `system_prompts/output_example_exercises.json`
  - 230 questions across 9 competencies (5 Skills >=30, 2 Concepts >=20, 2 Facts >=20)
  - Anti-giveaway calibrated (0 item violations, 0% longest/shortest violations)
  - `python -m validator.cli courses/demo_course.json --strict` -> VALID (exit code 0)
- [x] 3. Verify platform course discovery
  - Platform scanner `run_platform.scan_courses()` detects both courses with status `valid`
- [x] 4. Document findings and write handoff report (`handoff.md`)
- [ ] 5. Report completion to orchestrator
