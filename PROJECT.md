# Project: Top's Academy

## Architecture
The system delivers a complete, local, self-contained educational ecosystem composed of four primary interconnected subsystems:
1. **Core Data Specification & Validator (`src/validator/`)**:
   - Python-based reference validator and CLI (`validate-course`).
   - Two-pass validation: (Pass 1) Lexical scanner detecting raw LaTeX syntax corruptions and silent control escapes (`\b`, `\t`, `\f`, `\n`, `\r`, `\0`, `\v`) before JSON decoding; (Pass 2) Schema validation (Draft-07), structural rules, referential integrity, minimum counts, and psychometric anti-giveaway length distributions.
2. **Interactive Practice Platform (`platform/`)**:
   - Modern, lightweight web platform built with React, Vite, TypeScript, and Tailwind CSS.
   - Runs with a single documented command (`npm.cmd run dev` or `python run_platform.py`).
   - Backend discovery endpoint dynamically serves valid courses from `courses/` and isolates invalid course files with explicit error diagnostics.
   - Frontend features:
     - Sidebar navigation and Course Overview with mastery grid, badges, quiz/test markers, and overall course mastery percentage.
     - "Ready to practice?" launcher modal with question count and mascot artwork.
     - Practice session runner with real-time progress indicator, randomized question ordering, and independent option shuffling.
     - KaTeX LaTeX renderer ($...$ and $$...$$).
     - Native SVG `<CoordinatePlane />` vector graphing component rendering axes, grids, curves, and open/closed points.
     - Math equivalence engine (`mathjs` AST normalizer + Monte Carlo sampler) accepting equivalent expressions (e.g., `1-(alpha+n)*sigma` for `1 - \alpha\sigma - n\sigma`, `0.5` for `1/2`).
     - Progressive hint reveal (3 to 5 hints), instant green/red feedback toast with downward speech bubble, step-by-step solution expansion.
     - "Exercise complete!" celebration screen with `canvas-confetti` particles and mastery score update.
     - Quiz, Unit Test, and Course Challenge (~30 questions across units).
     - LocalStorage persistence for unit and course mastery levels.
3. **Content-to-Course Antigravity Skill (`.agents/skills/content-to-course/`)**:
   - Workspace skill discoverable under `.agents/skills/content-to-course/SKILL.md`.
   - Pipeline stages:
     1. Text and formula extraction from PDF using `fitz` (PyMuPDF).
     2. Cognitive Task Analysis (CTA) extracting Facts [H], Concepts [C], Skills [Hab], expert blind spots, and automation seeds.
     3. Chunked batch question generator (6-8 questions per prompt) producing >=30 questions per Skill and >=20 per Fact/Concept across all 3 interaction types with graphs and zero giveaways.
     4. Two-tier independent verification: SymPy programmatic checking and blind LLM solver.
     5. Automated R2 validation and 3-step auto-repair loop.
     6. Publication to `courses/` directory.
4. **End-to-End Verification & Audit Subsystems**:
   - Automated Headless Browser test suite (Playwright) running all platform acceptance tests.
   - Automated Validator test suite with 28 positive/negative fixtures.
   - Visual Fidelity Reviewer agent comparing platform screenshots against 6 reference screenshots.
   - Question Sample Auditor verifying >=40 questions against PDF with >=95% accuracy.
   - Blind-Guess Distractor Tester verifying <=30% accuracy on bare options without stem.

---

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| F01 | Lexical Scanner for LaTeX Escapes | Pre-parse scanner detecting invalid JSON escapes and silent control character escapes (`\b`, `\t`, `\n`, etc.) | M1 | Survey / R2 |
| F02 | Course Schema Validation | JSON Schema (Draft-07) for course metadata, units, question types, hints, solutions | M1 | Survey / R2 |
| F03 | Question Type Constraints | Enforce exactly 7 options & 1 correct for MCQ; 1 to n-1 correct for Multi-Select; expression/value for Fill-in-Blank | M1 | Survey / R2 |
| F04 | Pedagogical Scaffolding Rules | Enforce 3 to 5 hints per question, step-by-step solution, misconception warning | M1 | Survey / R2 |
| F05 | Unit Count Minimums | Enforce >=30 questions per Skill [Hab] competency, >=20 questions per Fact [H] / Concept [C] | M1 | Survey / R2 |
| F06 | Anti-Giveaway Item Rule | Enforce correct option length within [0.8*min, 1.2*max] of distractor lengths | M1 | Survey / R2 |
| F07 | Anti-Giveaway Course Rule | Enforce correct option is longest in <=25% and shortest in <=25% of MCQs across course | M1 | Survey / R2 |
| F08 | Validator CLI & Exit Codes | CLI tool `validate-course` with standard 0/1/2 exit codes and diagnostic reporting | M1 | Survey / R2 |
| F09 | Validator Automated Test Suite | Automated test suite and 28 positive/negative fixtures covering all validator rules | E2E-Track / M1 | Survey / AC |
| F10 | Course Dynamic Discovery & Error Isolation | Auto-discover courses in `courses/` folder; display clear errors on invalid courses without crashing app | M2 | Survey / R1, R2 |
| F11 | Single-Command Execution | Platform runs with one documented command (`npm.cmd run dev` or python launcher) | M2 | Survey / R1 |
| F12 | Course Overview & Navigation | Left sidebar with course + unit list; course mastery %; unit cards with mastery grid | M2 | Survey / R1 |
| F13 | Mastery Level System | 5 tiers (Mastered, Proficient, Familiar, Attempted, Not started) with mastery color palette & local persistence | M2 | Survey / R1 |
| F14 | "Ready to Practice?" Screen | Blue hero modal with question count, mascot graphics, and "Let's go" button | M2 | Survey / R1 |
| F15 | Practice Session Runner | Question presentation, progress indicator dots, Skip and Check buttons | M2 | Survey / R1 |
| F16 | Session Shuffling & Non-Mirroring | Randomize question order and shuffle options independently; assert orders differ and grading stays robust | M2 | Survey / R1, AC |
| F17 | LaTeX Math Rendering | KaTeX rendering for math in stems, options, hints, and solutions | M2 | Survey / R1 |
| F18 | Coordinate Plane Graphing | Vector SVG `<CoordinatePlane />` rendering axes, grid, curves, labels, open/closed points | M2 | Survey / R1 |
| F19 | Math Equivalence Grading | Grade fill-in-the-blank answers by algebraic equivalence (mathjs AST + Monte Carlo sampling) | M2 | Survey / R1, AC |
| F20 | Progressive Hint Reveal | Reveal 3-5 hints sequentially upon user request | M2 | Survey / R1 |
| F21 | Interactive Feedback & Explanations | Green "Good work!" speech bubble popover, step-by-step solution expansion, red try-again state | M2 | Survey / R1 |
| F22 | Completion Celebration | Exercise complete screen with score, canvas-confetti animation, "Try again" and "Up next" buttons | M2 | Survey / R1 |
| F23 | Quizzes, Unit Tests & Course Challenge | Support unit quizzes, unit tests, and comprehensive ~30-question Course Challenge | M2 | Survey / R1 |
| F24 | Automated Headless Browser Tests | Playwright automated tests verifying library, invalid isolation, practice, shuffling, math equivalence, graphs, mastery persistence, no console errors | E2E-Track | Survey / AC |
| F25 | Visual Fidelity Parity | UI faithfully matches all 6 reference screenshots per visual fidelity checklist | M2 / M4 | Survey / AC |
| F26 | Antigravity Skill Definition (`SKILL.md`) | Skill manifest in `.agents/skills/content-to-course/SKILL.md` documenting end-to-end pipeline | M3 | Survey / R3, AC |
| F27 | PDF Text & Math Extraction | Extract digital text and formulas from PDF using PyMuPDF / pdfplumber | M3 | Survey / R3 |
| F28 | Cognitive Task Analysis (CTA) Generator | Generate CTA output (Facts, Concepts, Skills, blind spots, automation seeds) grounded in source PDF | M3 | Survey / R3 |
| F29 | Chunked Batch Question Generation | Generate >=30 questions per Skill, >=20 per Fact/Concept in 6-8 item chunks avoiding token truncation | M3 | Survey / R3 |
| F30 | Symmetrical Distractor & Anti-Giveaway Synthesis | Generate plausible distractors based on misconceptions with homogeneous length and symmetric justification | M3 | Survey / R3 |
| F31 | Independent Answer Verification | Verify answer keys independently via SymPy programmatic checking and blind LLM solving | M3 | Survey / R3 |
| F32 | Automated Validation & Auto-Repair Loop | Auto-validate via R2 CLI and apply repair passes (escape normalization, option rebalancing, shortfall filling) | M3 | Survey / R3 |
| F33 | Automatic Course Publishing | Save validated JSON course to platform's `courses/` directory and notify user | M3 | Survey / R3 |
| F34 | Sample PDE Course Generation | Run skill on `sample_content/I__Ecuaciones_en_derivadas_parciales_2026.pdf` to produce valid course | M4 | Survey / R4 |
| F35 | Demo Course Conversion | Convert `system_prompts/output_example_exercises.json` into valid, playable demo course | M4 | Survey / R4 |
| F36 | Visual Fidelity Reviewer Audit | Independent reviewer agent checks platform screenshots vs 6 reference images item-by-item | M4 | Survey / AC |
| F37 | Question Accuracy Sample Audit | Independent reviewer agent audits >=40 questions against PDF with >=95% accuracy | M4 | Survey / AC |
| F38 | Blind-Guess Distractor Test | Independent agent guesses correct option on >=40 bare MC items with <=30% accuracy | M4 | Survey / AC |
| F39 | Comprehensive Documentation & README | Root README.md documenting platform startup, test execution, validator CLI, and skill usage | M4 | Survey / R4 |

---

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| E2E | E2E Testing Track | Design `TEST_INFRA.md`, build automated headless browser test suite (Playwright) and validator test runner; publish `TEST_READY.md` | None | DONE |
| M1 | Exercise Bank Format & Validator (R2) | Implement Python validator (`src/validator/`), CLI `validate-course`, 28 test fixtures, unit tests, 249 passing tests (F01–F08) | None | DONE |
| M2 | Practice Platform Web App (R1) | Implement React+Vite+Tailwind platform, course loader, mathjs grader, SVG graphs, KaTeX, mastery persistence (F10–F23) | M1 (Schema) | DONE |
| M3 | Content-to-Course Antigravity Skill (R3) | Implement `.agents/skills/content-to-course/`, PDF extractor, CTA generator, batch generator, SymPy verifier, auto-repair loop (F26–F33) | M1 (Validator) | DONE |
| M4 | End-to-End Demo, Audits & Handoff (R4) | Convert demo course (F35), generate PDE course (F34), run visual fidelity audit (F36), run question audit (F37), run blind-guess test (F38), run 100% E2E tests, README (F39) | M2, M3, E2E | DONE |

---

## Interface Contracts

### 1. Course Bank JSON Format (M1 ↔ M2, M3, M4)
Standard Course Schema:
```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "course_id": "string (slug)",
  "title": "string",
  "description": "string",
  "version": "1.0.0",
  "language": "es" | "en",
  "competencies": [
    {
      "id": "COMP-001",
      "code": "HAB-01" | "CON-01" | "HEC-01",
      "name": "string",
      "category": "Skill" | "Concept" | "Fact",
      "description": "string",
      "mastery_target": 100
    }
  ],
  "questions": [
    {
      "id": "Q-001",
      "competency_id": "COMP-001",
      "type": "multiple_choice_7_options" | "multiple_select" | "fill_in_the_blank",
      "difficulty": "easy" | "medium" | "hard",
      "stem": "string (with $LaTeX$)",
      "graph": {
        "x_range": [-7, 7],
        "y_range": [-7, 7],
        "curves": [{ "fn": "string", "label": "string", "color": "string" }],
        "points": [{ "x": 3, "y": -4, "type": "open" | "closed", "label": "string" }]
      },
      "options": [
        { "id": "opt_a", "content": "string (with $LaTeX$)" }
      ],
      "correct_answer": "opt_a" | ["opt_a", "opt_c"] | { "expression": "string", "tolerance": 0.001 },
      "hints": [
        "string (hint 1)",
        "string (hint 2)",
        "string (hint 3)"
      ],
      "solution": "string (step-by-step)",
      "misconception_warning": "string"
    }
  ]
}
```

### 2. Validator CLI (M1 ↔ M3, E2E-Track)
Command:
```bash
python -m src.validator.cli <path_to_course_json> [--strict]
```
Exit Codes:
- `0`: Valid course (meets all schema, LaTeX escape, question count, and anti-giveaway rules).
- `1`: Validation error (specific violation printed with code and file location).
- `2`: Internal CLI or I/O error.

### 3. Platform Dynamic Course API (M1, M3 ↔ M2)
- Courses directory: `courses/*.json` relative to project root.
- Server endpoint: `GET /api/courses` returns:
  `{ "courses": [ { "id": "...", "title": "...", "status": "valid" | "error", "error_message": "..." } ] }`
- Course detail endpoint: `GET /api/courses/:id` returns course JSON payload.

### 4. Skill Invocation Protocol (M3 ↔ M4, Antigravity)
- Skill entrypoint: `.agents/skills/content-to-course/run_pipeline.py`
- Command:
  ```bash
  python .agents/skills/content-to-course/run_pipeline.py --pdf <path_to_pdf> --out-dir courses/
  ```
- Deliverables produced:
  - Competence analysis markdown: `courses/<course_id>_competences.md`
  - Validated course JSON: `courses/<course_id>.json`

---

## Code Layout
```
g:\Mi unidad\Competence_analyser\
├── .agents/
│   ├── skills/
│   │   └── content-to-course/
│   │       ├── SKILL.md
│   │       ├── run_pipeline.py
│   │       ├── extractor.py
│   │       ├── cta_engine.py
│   │       ├── batch_generator.py
│   │       ├── verifier.py
│   │       └── repair_loop.py
│   └── teamwork/
├── courses/
│   ├── pde_course.json
│   ├── demo_course.json
│   └── fixtures/
├── platform/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── Sidebar.tsx
│   │   │   ├── CourseOverview.tsx
│   │   │   ├── MasteryGrid.tsx
│   │   │   ├── PreExerciseModal.tsx
│   │   │   ├── PracticeSession.tsx
│   │   │   ├── QuestionCard.tsx
│   │   │   ├── CoordinatePlane.tsx
│   │   │   ├── MathText.tsx
│   │   │   ├── FeedbackToast.tsx
│   │   │   ├── CompletionScreen.tsx
│   │   │   └── CourseChallenge.tsx
│   │   ├── utils/
│   │   │   ├── mathEquivalence.ts
│   │   │   ├── masteryStorage.ts
│   │   │   └── sessionShuffler.ts
│   │   └── server/
│   │       └── courseServer.js
├── src/
│   └── validator/
│       ├── __init__.py
│       ├── cli.py
│       ├── lexical_scanner.py
│       ├── schema_validator.py
│       ├── psychometric_checker.py
│       └── rules.py
├── tests/
│   ├── validator/
│   │   ├── test_validator.py
│   │   └── fixtures/
│   └── e2e/
│       ├── playwright.config.ts
│       ├── platform.spec.ts
│       └── visual_fidelity.spec.ts
├── run_platform.py
└── README.md
```
