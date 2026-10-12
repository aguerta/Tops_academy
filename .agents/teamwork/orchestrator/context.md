# Context: Top's Academy

## Objectives
Build:
1. **R1 Practice Platform**: A local web app recreating Top's Academy course & practice experience (overview, mastery grid, question screens, progressive hints, LaTeX rendering, math equivalence grading, interactive graphs, session shuffling, persistent mastery, course challenge).
2. **R2 Exercise Bank Format & Validator**: Standardized JSON schema for courses/competencies/questions and a CLI validator enforcing all structural, mathematical, LaTeX, count (Skill >= 30, Fact/Concept >= 20), and anti-giveaway rules (no length giveaways).
3. **R3 Content-to-Course Antigravity Skill**: Complete pipeline skill in `.agents/skills/` that ingests PDF -> extracts text/math -> Cognitive Task Analysis -> generates valid exercise bank with zero giveaways -> validates & repairs -> publishes to platform.
4. **R4 End-to-End Demo & Verification**: Process `sample_content/I__Ecuaciones_en_derivadas_parciales_2026.pdf` into published course, convert `output_example_exercises.json` into valid playable course, automated headless browser tests, visual fidelity review vs 6 reference screenshots, question audit (>=40 questions, >=95% accuracy), blind-guess test (<=30% accuracy).

## Reference Materials
- `Khan_academy_images_references/` — 6 screenshots
- `system_prompts/prompt_competence_analyser.md` & `output_example_competences.md`
- `system_prompts/prompt_creator_exercises.md` & `output_example_exercises.json`
- `sample_content/I__Ecuaciones_en_derivadas_parciales_2026.pdf`

## Technical Environment
- OS: Windows
- Node.js: v24 (run npm.cmd / npx.cmd)
- Python: 3.12
- Git available
- Google Drive sync active
