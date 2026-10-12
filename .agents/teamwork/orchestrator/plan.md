# Execution Plan: Top's Academy

## Phase 0: Survey & Groundwork
1. Dispatch 3 Explorer / Spec Miner subagents:
   - Explorer 1 (UI & Experience Analyst): Examine `Khan_academy_images_references/` screenshots, breakdown UI components, mastery states, layout, and visual fidelity criteria.
   - Explorer 2 (Format, Schema & Validator Analyst): Examine `system_prompts/`, `output_example_exercises.json`, LaTeX escape issues, giveaway rules, and validation criteria.
   - Explorer 3 (Competence Extraction & Skill Pipeline Analyst): Examine `prompt_competence_analyser.md`, `sample_content/I__Ecuaciones_en_derivadas_parciales_2026.pdf`, Antigravity skill structure, and question generation pipeline.
2. Merge findings into `PROJECT.md` (Architecture, Feature Inventory, Code Layout, Interface Contracts, Milestones).

## Phase 1: Dual Track Execution
- **Track A: E2E Testing Track**
  - Design test infrastructure (`TEST_INFRA.md`).
  - Implement automated headless browser test suite (Playwright / Puppeteer in Node or Python) covering all platform requirements: library discovery, invalid course isolation, course overview, practice session, hints, feedback, LaTeX rendering, graph rendering, math equivalence grading, shuffling & grading stability, mastery persistence, quizzes, tests, challenge, console error checks.
  - Implement automated validator test suite covering all positive and negative fixture rules.
  - Publish `TEST_READY.md`.

- **Track B: Core Implementation Milestones**
  - **Milestone 1 (R2)**: Exercise Bank Specification & Validator CLI + automated tests and fixtures.
  - **Milestone 2 (R1)**: Top's Academy-style Practice Platform web app (backend/static server, frontend UI, LaTeX via KaTeX/MathJax, graph rendering via FunctionPlot/JSXGraph/Canvas, math equivalence grading via mathjs/SymPy, persistent mastery storage, session randomized shuffling).
  - **Milestone 3 (R3)**: Content-to-Course Antigravity Skill (`.agents/skills/`) with PDF extraction, Cognitive Task Analysis, prompt engineering, anti-giveaway generation, automated validation & auto-repair loop, and course publishing.
  - **Milestone 4 (R4)**: End-to-End Demo & Verification:
    - Run skill on `sample_content/I__Ecuaciones_en_derivadas_parciales_2026.pdf` to produce valid course.
    - Convert `output_example_exercises.json` into valid playable course.
    - Independent Reviewer visual fidelity audit vs 6 reference screenshots.
    - Independent Question Auditor sample audit (>=40 questions, >=95% accuracy).
    - Blind-guess distractor test (<=30% correct guess rate on shuffled options without stem).
    - Full E2E automated test run pass.

## Phase 2: Synthesis, Gate Audits & Reporting
1. Verify all acceptance criteria are met with zero skipped checks.
2. Write comprehensive README.md and documentation.
3. Report completion to Sentinel with full evidence and verification instructions.
