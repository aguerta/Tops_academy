# Project: Top's Academy

## Architecture
The system delivers a complete, local, self-contained educational ecosystem composed of five primary interconnected subsystems and a specialized multi-agent skill suite:

1. **Core Data Specification & Validator (`src/validator/`)**:
   - Python-based reference validator and CLI (`validate-course` / `python -m src.validator.cli`).
   - Multi-pass validation:
     - **Pass 1 (Lexical Scanner)**: Detects raw LaTeX syntax corruptions, unescaped control escapes (`\b`, `\t`, `\f`, `\n`, `\r`, `\0`, `\v`), and silent control character collisions (`\text`, `\frac`, `\nu`, `\tau`, `\rho`, `\beta`, `\theta`) before JSON decoding.
     - **Pass 2 (Schema & Semantic Rules)**: JSON Schema Draft-07 conformity, structural referential integrity, duplicate ID detection, and volume quotas ($\ge 30$ per Skill, $\ge 20$ per Fact/Concept).
     - **Pass 3 (Extended Quality & Psychometrics)**: 21 formal rules (R-01..R-16, R-17..R-20, R-22) plus 3 Strict Pedagogical Rules (S-01..S-03), enforcing item-level distractor length ratios ($[0.8\cdot\min(D), 1.2\cdot\max(D)]$), course-level distribution limits ($\le 25\%$ longest/shortest), formative diagnostic error rationales without placeholders (R-17), meta-giveaway confinement (R-18), fill-in-the-blank answer leak prevention (R-19), strict KaTeX syntax with macro arity, nested macros, and environment checks (R-20), and mandatory error rationales in multiple-select options (R-22).

2. **Interactive Practice Platform (`platform/`)**:
   - Modern web platform built with React 18, Vite, TypeScript, and Tailwind CSS.
   - Runs with a single command (`python run_platform.py` or `npm.cmd run dev` inside `platform/`).
   - Dynamic course discovery endpoint serves valid courses from `courses/` and isolates invalid files with explicit diagnostics.
   - **Static Bundle Generation**: Built to `platform/dist/` with static JSON course bundles (`dist/api/courses.json`, `dist/courses/*.json`) ready for offline serving or GitHub Pages deployment.
   - Frontend features:
     - Sidebar navigation and Course Overview with mastery grid, badges, quiz/test markers, and overall mastery percentage.
     - "Ready to practice?" launcher modal with question count and estimated time.
     - Practice session runner with real-time progress indicator, randomized question presentation, and independent option shuffling.
     - KaTeX LaTeX typesetting with inline ($...$) and display ($$...$$) math.
     - Native SVG `<CoordinatePlane />` vector graphing component rendering axes, grids, curves, and open/closed points.
     - Client-side Math Equivalence Engine (`mathjs` AST normalizer + Monte Carlo sampler) supporting Spanish decimal comma (`0,8333` $\equiv$ `0.8333`), fraction/decimal equivalence (`5/6` $\equiv$ `0,8333`), algebraic expansion/factoring, negative powers, Greek letters, and tolerance bounds (81 verified adversarial cases).
     - Progressive hint reveal (3 to 5 hints), instant feedback toast with downward speech bubble pointer, and step-by-step solution expansion.
     - **3-Strikes Solution Reveal Safeguard**: Tracks consecutive incorrect attempts per item; on the 3rd failed attempt, locks inputs ("Maximum attempts reached 3/3"), auto-expands the step-by-step solution and misconception warning, awards 0 credit, and enables advancing.
     - Fast Redo on mistakes across Practice, Quiz, Unit Test, and Course Challenge modes.
     - "Exercise complete!" celebration screen with `canvas-confetti` particles and LocalStorage mastery persistence.

3. **Content-to-Course Antigravity Skill (`.agents/skills/content-to-course/`)**:
   - High-throughput v3 educational authoring pipeline:
     1. **Stage 0 (Ingestion & Corpus Slicing)**: PyMuPDF extraction, vision tiling fallback, direct PDF viewing, and curricular session partitioning.
     2. **Stage 1 (CTA Map-Reduce)**: Concurrent *Sectional CTA Analyzers* generating partial JSONs in parallel, unified by the *CTA Harmonizer & DAG Integrator* with inter-session prerequisite DAGs.
     3. **Stage 2 (Shard Planning)**: Partitioning into self-contained shard payloads (`work/shards/shard_XX.json`) with embedded DSL references and dynamic shard caps up to $K=8$.
     4. **Stage 3 (Shard Authoring with Shift-Left Self-Audit)**: Subagents authoring parametric templates in sandboxed Python, strictly gating on `check_templates.py` with mandatory `stem_variants >= 3` and simulated diversity ratio $\ge 0.50$ (Rule `TPL-VAR`).
     5. **Stage 4 (Sandboxed Assembly & Instantiation)**: In-process multi-seed generation executing 500+ items in $<6.5$ seconds with invariant checking (`engine/invariants.py`).
     6. **Stage 5 (Stratified Blind Judges)**: Stratified 2-item/competency sampling evaluated under epistemic closure with normalized keys to verify accuracy.
     7. **Stage 6 (Validation & Publishing)**: Strict verification via `validator.cli --strict` and atomic publication to `courses/`.

4. **Multi-Agent Evaluation & Auditing Ecosystem**:
   - **`course-qa-evaluator`**: Fast deterministic pass (<300ms) + adaptive semantic check evaluating courses under Quality Matters, OSCQR, and Mastery Learning standards across 5 dimensions (Architecture, Items, Hints, Alignment, KaTeX/Ergonomics).
   - **`c2c-run-auditor`**: Granular telemetry auditing extracting token decomposition (input, output, cache read, thinking), latencies, wall-time speedups (achieving up to 6.69x speedup, 1.96s/question), and historical benchmark registry (`reports/c2c_audits/`).
   - **`c2c-unified-auditor`**: Consolidated multi-agent orchestrator dispatching Run Auditor and Course QA Evaluator concurrently, generating merged reports.
   - **`delete-course`**: Safe course deletion tool (<300ms) removing JSON and markdown files while stamping audit reports and preserving immutable content.

5. **Consolidated Test & Verification Matrix**:
   - 367 Python test items (363 passed, 4 skipped in 18.05s) across 13 dedicated test suites.
   - 81-case Node.js Math Adversarial Suite (100% pass rate).
   - Node.js keyboard navigation and unit isolation test suites (100% pass rate).
   - Headless browser E2E test suite (Playwright) covering AC-01 through AC-12 and VF-01 visual fidelity captures.

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
| F40 | Extended Quality Rules (R-17..R-22) | Implement R-17 (error rationales without placeholders), R-18 (meta-giveaway ban), R-19 (FIB leak prevention), R-22 (mandatory MS error rationale) | M5 | QA / Audit |
| F41 | KaTeX Macro Arity & Environment Linters (R-20) | Pre-publication linter detecting unclosed delimiters, triple dollars, residual double braces, macro arities (`\frac{}{}`), nested macros, unclosed environments | M5 | QA / Audit |
| F42 | CTA Map-Reduce Architecture | Slicing corpus into session partitions (`cta-map`), parallel sectional analysis, and DAG integration with inter-session prerequisites (`cta-reduce`) | M5 | Pipeline v3 |
| F43 | Shift-Left Shard Author Self-Audit | Enforce `TPL-VAR` gate in `check_templates.py` with $\ge 3$ `stem_variants` and diversity ratio $\ge 0.50$ | M5 | Pipeline v3 |
| F44 | Stratified Blind Judge Arbitration | Sampling exactly 2 items/competency for blind evaluation under epistemic closure with normalized keys | M5 | Pipeline v3 |
| F45 | 3-Strikes Solution Reveal Safeguard | Enforce 3-attempts limit in `PracticeSession.tsx` and `FeedbackToast.tsx`, locking inputs and revealing step-by-step solution with 0 credit | M5 | Platform UI |
| F46 | C2C Run Telemetry Auditor | Granular token extraction (input, output, cache, thinking), latencies, bottlenecks, throughput, and historical registry | M6 | Skills Suite |
| F47 | Course QA Evaluator under QM/OSCQR | Hybrid deterministic pass (<300ms) + adaptive semantic check under Quality Matters, OSCQR, and Mastery Learning | M6 | Skills Suite |
| F48 | Unified Auditor & Safe Course Deletion | Merged reporting orchestrator and fast safe course deletion tool (<300ms) preserving audit reports | M6 | Skills Suite |
| F49 | Spanish Decimal Comma & Advanced Math Equivalence | Math equivalence engine supporting Spanish decimal comma (`0,8333`), fraction-to-decimal, tolerances, Greek letters (81 cases) | M5 | Platform Math |
| F50 | Static Course Bundling & Web Deployment | Vite base path configuration, static JSON course generation, and GitHub Pages deploy workflow | M5 | Platform Build |

---

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| E2E | E2E Testing Track | Design `TEST_INFRA.md`, build automated headless browser test suite (Playwright) and validator test runner; publish `TEST_READY.md` | None | DONE |
| M1 | Exercise Bank Format & Validator (R2) | Implement Python validator (`src/validator/`), CLI `validate-course`, 28 test fixtures, unit tests (F01–F08) | None | DONE |
| M2 | Practice Platform Web App (R1) | Implement React+Vite+Tailwind platform, course loader, mathjs grader, SVG graphs, KaTeX, mastery persistence (F10–F23) | M1 (Schema) | DONE |
| M3 | Content-to-Course Antigravity Skill (R3) | Implement `.agents/skills/content-to-course/`, PDF extractor, CTA generator, batch generator, SymPy verifier, auto-repair loop (F26–F33) | M1 (Validator) | DONE |
| M4 | End-to-End Demo, Audits & Handoff (R4) | Convert demo course (F35), generate PDE course (F34), run visual fidelity audit (F36), run question audit (F37), run blind-guess test (F38), run E2E tests, README (F39) | M2, M3, E2E | DONE |
| M5 | Pipeline v3 High-Throughput & Platform Safeguards | CTA Map-Reduce, Shift-Left Shard Authoring, stem variants $\ge 0.50$, 3-strikes UI safeguard, 81-case math equivalence, static bundling (F40–F45, F49, F50) | M1, M2, M3 | DONE |
| M6 | Forensic Telemetry & Multi-Agent Auditing | Implement `c2c-run-auditor`, `course-qa-evaluator`, `c2c-unified-auditor`, `delete-course`, and historical registry (F46–F48) | M4, M5 | DONE |
| M7 | KaTeX Saneamiento & Validator Hardening | Implement strict KaTeX macro arity, nested macro linters, environment checks (R-20), and repair courses (`bf7e634`, `75ba68d`) | M1, M5 | DONE |

---

## Active & Certified Production Courses
- **Active Production Course**: `courses/estadistica3_regresion_v3.json`
  - Title: *Estadística III: Econometría y Modelo de Regresión Lineal*
  - Competencies: 16 (8 Habilidades, 4 Conceptos, 4 Hechos)
  - Questions: 390
  - Validation Status: **100% VALID** in strict pedagogical mode (`python -m src.validator.cli courses/estadistica3_regresion_v3.json --strict` -> EXIT 0).
  - QA Score: **19.4 / 20.0 (EXCELENTE)**.
- **Archived Courses**: `archive_rejected_courses/` preserves previous generation courses (`pde_course.json`, `sistemas_edos.json`, `estadistica3_regresion_legacy.json`, `solow_model_old.json`) for historical auditing purposes.
- **Canonical Test Fixtures**: `courses/fixtures/` contains 28 positive and negative test fixtures covering all validator invariants.

---

## Interface Contracts

### 1. Course Bank JSON Format
Standard Course Schema conforming to JSON Schema Draft-07:
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
      "mastery_target": 100,
      "prerequisites": ["COMP-000"]
    }
  ],
  "questions": [
    {
      "id": "Q-001",
      "competency_id": "COMP-001",
      "type": "multiple_choice_7_options" | "multiple_select" | "fill_in_the_blank",
      "difficulty": "easy" | "medium" | "hard",
      "stem": "string (with $LaTeX$)",
      "stem_variants": ["string variant 1", "string variant 2", "string variant 3"],
      "graph": {
        "x_range": [-7, 7],
        "y_range": [-7, 7],
        "curves": [{ "fn": "string", "label": "string", "color": "string" }],
        "points": [{ "x": 3, "y": -4, "type": "open" | "closed", "label": "string" }]
      },
      "options": [
        { "id": "opt_a", "content": "string", "is_correct": true },
        { "id": "opt_b", "content": "string", "is_correct": false, "error_rationale": "Diagnóstico de error pedagógico" }
      ],
      "correct_answer": "opt_a" | ["opt_a", "opt_c"] | { "expression": "string", "canonical_algebraic": "0.8333", "tolerance": 0.001 },
      "hints": [
        "string (hint 1: conceptual)",
        "string (hint 2: procedural)",
        "string (hint 3: operational)"
      ],
      "solution": "string (step-by-step)",
      "misconception_warning": "string"
    }
  ]
}
```

### 2. Validator CLI
Command:
```bash
python -m src.validator.cli <path_to_course_json> [--strict] [--json]
```
Exit Codes:
- `0`: Valid course (satisfies all 21 rules, plus 3 strict rules if `--strict`).
- `1`: Validation error (explicit violation code and diagnostic location).
- `2`: Internal CLI or I/O error.

### 3. Platform Dynamic & Static Course API
- Courses directory: `courses/*.json` relative to project root.
- Server endpoint: `GET /api/courses` returns:
  `{ "courses": [ { "id": "...", "title": "...", "status": "valid" | "error", "competency_count": 16, "question_count": 390 } ] }`
- Course detail endpoint: `GET /api/courses/:id` returns complete course JSON.
- Static bundle output: `platform/dist/api/courses.json` and `platform/dist/courses/<id>.json`.

### 4. Skill Invocation Protocol
- Pipeline entrypoint: `.agents/skills/content-to-course/run.py`
- Command:
  ```bash
  python .agents/skills/content-to-course/run.py \
    --course-id <course_id> \
    --title "<Human Title>" \
    --pdf <path_to_document> \
    --output-dir courses \
    --strict
  ```

---

## Code Layout
```
Tops_academy/
├── README.md                                # Authoritative documentation
├── PROJECT.md                               # Project architecture, inventory, and interfaces
├── FUTURE_MILESTONES.md                     # Roadmap for Mobile PWA and High-Speed Daemon
├── TEST_INFRA.md                            # Comprehensive test infrastructure specification
├── TEST_READY.md                            # Test suite verification checklist
├── pyproject.toml                           # Python project configuration
├── run_platform.py                          # Unified launcher and API server
├── courses/                                 # Published courses & fixtures
│   ├── estadistica3_regresion_v3.json       # Active certified course (390 items, 16 comps)
│   ├── competence_analysis_estadistica3_regresion_v3.md # CTA analysis document
│   └── fixtures/                            # 28 canonical test course fixtures
├── archive_rejected_courses/                # Historical legacy courses archive
├── content/                                 # Academic source documents (zero-bloat gitignored)
│   ├── README.md                            # Ingestion guidelines
│   └── Solow_model/                         # Source PDFs
├── docs/                                    # Research and architecture proposals
│   └── proposals_cta_mapreduce_and_shard_autocheck.md # CTA Map-Reduce & Shard Auto-Check
├── reports/                                 # Forensic telemetry & QA audit reports
│   ├── qa_audits/                           # Quality Matters / OSCQR audit reports
│   │   ├── SUITE_QA_AUDIT_REPORT.md         # Master suite QA audit report
│   │   ├── COURSE_CREATION_IMPROVEMENTS.md  # Architectural recommendations
│   │   └── estadistica3_regresion_v3_qa_report.md # Individual course report
│   └── c2c_audits/                          # Execution telemetry & unit economics
│       ├── historical_benchmark.md          # Multi-run benchmark evolution
│       └── audit_registry.json              # Machine-readable telemetry registry
├── platform/                                # Top's Academy Practice Platform Frontend
│   ├── package.json                         # Node dependencies (React 18, Vite, KaTeX)
│   ├── vite.config.ts                       # Vite bundler configuration
│   ├── src/                                 # Application source code
│   │   ├── components/                      # UI Views: PracticeSession, FeedbackToast, etc.
│   │   ├── utils/                           # mathEquivalence.ts, sessionShuffler.ts, etc.
│   │   └── App.tsx                          # Mastery state router and course loader
│   └── dist/                                # Compiled production web bundle
├── src/validator/                           # Subsystem 1: Format & Psychometric Validator
│   ├── cli.py                               # CLI entrypoint
│   ├── lexical_scanner.py                   # Pass 1: raw syntax & control character scanner
│   ├── schema_validator.py                  # Pass 2: Draft-07 schema validator
│   ├── rules.py                             # Pass 2 & 3: Structural, pedagogical, and KaTeX rules
│   └── psychometric_checker.py              # Pass 3: Anti-giveaway ratio checkers
├── .agents/skills/                          # Specialized Multi-Agent Skills Ecosystem
│   ├── content-to-course/                   # v3 universal course creation pipeline
│   ├── course-qa-evaluator/                 # Automated pedagogical quality evaluator
│   ├── c2c-run-auditor/                     # Granular multi-agent execution telemetry auditor
│   ├── c2c-unified-auditor/                 # Unified orchestration auditor
│   └── delete-course/                       # Fast safe course deletion tool
├── system_prompts/                          # Formal prompts for specialized subagents
└── tests/                                   # Consolidated Automated Test Suites
    ├── test_validator.py                    # Consolidated validator test suite (144 tests)
    ├── test_engine_invariants_adversarial.py# Invariants & sandboxed assembly (51 tests)
    ├── test_sandbox_adversarial.py          # AST sandbox security (49 tests)
    ├── test_skill.py                        # Pipeline ingestion & publishing (33 tests)
    ├── test_platform.py                     # Platform server & API (19 tests)
    ├── test_cta_mapreduce.py                # CTA Map-Reduce & DAG merging (16 tests)
    ├── test_c2c_validator_prescriptive.py   # Prescriptive validator rules (12 tests)
    ├── test_dispatch_scope.py               # Subagent role isolation (10 tests)
    ├── test_delete_course.py                # Safe course deletion (8 tests)
    ├── test_handouts.py                     # Vision handout fallback (8 tests)
    ├── test_pipeline_optimizations.py       # Pipeline optimizations (6 tests)
    ├── test_skill_v3.py                     # v3 pipeline execution (6 tests)
    ├── test_template_variability.py         # Stem variants & diversity (5 tests)
    ├── test_math_adversarial_suite.mjs      # Math equivalence 81-case suite (100% pass)
    ├── test_question_grading.mjs            # Question evaluation & normalization suite (1048 items, 100% pass)
    ├── test_keyboard_navigation.mjs         # Keyboard accessibility suite
    ├── test_unit_isolation.mjs              # Unit isolation & shuffle suite
    ├── test_blind_guess_empirical.py        # Adversarial blind-guess distractor test harness
    └── e2e/                                 # Playwright headless browser E2E test suite
```
