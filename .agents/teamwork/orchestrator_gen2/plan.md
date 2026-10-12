# Orchestration Plan — Generation 2

## Phase 1: Milestone 2 Platform Certification & Visual Fidelity Gate
- [ ] 1.1 Run and document all E2E platform tests (`pytest tests/e2e`), verify build (`platform/dist`), and confirm launcher (`run_platform.py`).
- [ ] 1.2 Reviewer visual fidelity evaluation comparing `tests/e2e/screenshots/` vs `Khan_academy_images_references/` and feature checklist against `ui_spec.md`.
- [ ] 1.3 Challenger empirical evaluation of grading equivalence, session shuffling, and error isolation.
- [ ] 1.4 Forensic Auditor integrity audit of platform implementation.
- [ ] 1.5 Gate evaluation in `GATE_STATUS.md` -> Certify Milestone 2 as DONE.

## Phase 2: Milestone 3 Content-to-Course Antigravity Skill
- [ ] 2.1 Remediate findings via worker_m3_fix:
  - Genuine dynamic CTA analysis from PDF
  - Dedicated mathematical question generators for all 21 competencies
  - Decoupled Blind Solver verifier
  - Multi-PDF ingestion support (file, list, directory)
  - Append option (`--append`) to existing courses
  - Multi-agent AI workflow specification in `SKILL.md`
- [ ] 2.2 M3 Gate verification & certification.

## Phase 3: Platform UX Enhancements (New User Requirements)
- [ ] 3.1 Implement Fast Redo / Re-attempt on wrong answers in `platform/src/components/PracticeSession.tsx` and `FeedbackToast.tsx`.
- [ ] 3.2 Display completed vs not-completed blocks in Course Overview and visual completed course tracking in Course Library.
- [ ] 3.3 Verify root launcher `python run_platform.py` and test consolidation.

## Phase 4: Milestone 4 End-to-End Demo, Course Generation & Audits
- [ ] 4.1 Convert `output_example_exercises.json` into valid `demo_course.json` passing `validate-course --strict`.
- [ ] 4.2 Run content-to-course skill on `sample_content/I__Ecuaciones_en_derivadas_parciales_2026.pdf` to generate `pde_course.json` (>=30 per Skill, >=20 per Fact/Concept, 500 questions).
- [ ] 4.3 Independent Question Audit on >=40 sampled questions (>=95% accuracy).
- [ ] 4.4 Independent Blind-Guess Test on >=40 bare MC items (<=30% guess rate).
- [ ] 4.5 Consolidate test suite across repository into unified, clean test files.
- [ ] 4.6 Complete root `README.md` with full usage instructions and single command launcher.
- [ ] 4.7 Run full E2E Playwright test suite and certify all Acceptance Criteria.
- [ ] 4.8 Final Sentinel handoff report.
