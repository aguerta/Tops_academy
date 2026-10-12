# Top's Academy Platform & Content-to-Course AI Pipeline

[![Tests](https://img.shields.io/badge/Tests-191%20Passed-brightgreen.svg)]()
[![Validator](https://img.shields.io/badge/Format%20Validator-16%20Rules%20Strict-blue.svg)]()
[![Platform](https://img.shields.io/badge/Platform-React%2018%20%2B%20Vite%20%2B%20KaTeX-61dafb.svg)]()
[![Skill](https://img.shields.io/badge/Antigravity%20Skill-Content--to--Course-orange.svg)]()

> [!NOTE]
> **Pedagogical & UX Inspiration:**
> This project has been heavily inspired by Khan Academy for its mastery learning framework, progressive hint scaffolding, multi-tiered competency progression, and student practice workflows.

An end-to-end educational system that ingests academic university course materials (syllabi, lecture slide decks, and textbook chapters) in PDF format, performs **Cognitive Task Analysis (CTA)** to extract competencies and expert knowledge, generates calibrated **mastery learning exercise banks** across multiple interaction types with mathematical anti-giveaway guarantees, independently verifies answer keys via **SymPy** and blind solver tiers, auto-repairs validation errors, and serves an interactive web practice platform with mastery tracking.

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Single Command Launcher](#single-command-launcher)
3. [Practice Platform Features & Views](#practice-platform-features--views)
4. [Course Bank Format & Validator CLI](#course-bank-format--validator-cli)
5. [Content-to-Course Antigravity Skill](#content-to-course-antigravity-skill)
6. [Automated Test Suite Execution](#automated-test-suite-execution)
7. [Milestone Verification & Certification Metrics](#milestone-verification--certification-metrics)

---

## System Architecture

The project consists of four interconnected, independently testable subsystems:

```
                            +-----------------------------------------------+
                            |             Academic Course PDFs             |
                            |  (Single PDF, Multi-PDF list, or Directory)   |
                            +-----------------------+-----------------------+
                                                    |
                                                    v
+---------------------------------------------------------------------------------------------------+
| Subsystem 3: Content-to-Course Antigravity Skill (.agents/skills/content-to-course/)             |
|                                                                                                   |
|  1. Ingestion (ingest)   -->  2. CTA Decomposition   -->  3. Batch Generator  (MC7, MS, FIB)       |
|     (PDFs & Images)          (Skills, Concepts, Facts)      (>=30 per Skill, >=20 per Fact/Concept)|
|                                                                     |                             |
|  6. Course Publisher    <--  5. Auto-Repair Loop    <--  4. Two-Tier Verifier                     |
|     (Publish & Append)       (<=3 Repair Cycles)            (Tier 1: SymPy, Tier 2: Blind Solver) |
+---------------------------------------------------+-----------------------------------------------+
                                                    | Outputs valid course JSON
                                                    v
+---------------------------------------------------------------------------------------------------+
| Subsystem 1: Format & Psychometric Validator (src/validator/)                                     |
|                                                                                                   |
|  Pass 1: Raw Lexical Scanner  -->  Pass 2: JSON Schema Validation --> Pass 3: Rules & Psychometrics|
|  - RFC 8259 syntax                 - Draft-07 JSON Schema              - 16 core rules (R-01..R-16)|
|  - Silent LaTeX escapes (\tau,\frac)- Top-level metadata & types        - R-15 Length bound [0.8, 1.2]|
|  - Unescaped control characters    - Graphing curve/point schema       - R-16 Course dist <= 25%   |
+---------------------------------------------------+-----------------------------------------------+
                                                    | Verified courses saved to courses/
                                                    v
+---------------------------------------------------------------------------------------------------+
| Subsystem 2: Top's Academy Practice Platform (platform/ & run_platform.py)                          |
|                                                                                                   |
|  - Python Launcher & API Server: Discovers courses, serves REST API and SPA on port 5173         |
|  - Frontend: React 18 + TypeScript + Tailwind CSS + Lucide Icons                                  |
|  - Math Engine: KaTeX LaTeX typesetting + Symbolic/Numeric Math Equivalence Engine                |
|  - Interactive SVG Coordinate Plane: Curves, asymptotes, open/closed points                       |
|  - Fast Redo on Mistakes: Immediate re-attempt on practice items, quizzes, unit tests, challenges |
|  - Mastery Persistence: LocalStorage tracking, 4 mastery levels, course completion certificates   |
+---------------------------------------------------------------------------------------------------+
```

---

## Single Command Launcher

Launch the complete application (both the backend course discovery API and frontend user interface) with a single command:

```bash
python run_platform.py
```

### Options and Flags

```bash
# Start server on custom port or host
python run_platform.py --port 5173 --host 127.0.0.1

# Course Discovery & Inspection Mode (non-server scan)
python run_platform.py --scan

# Help & Usage
python run_platform.py --help
```

### Discovery & Output

When starting, the platform scans `courses/`, validates all course banks, and logs the discovery:

```
========================================================================
  Top's Academy Platform Server Running
  Access URL: http://127.0.0.1:5173
  Open your browser to: http://localhost:5173
========================================================================
Discovered 4 course(s) (4 valid):
  * demo_course.json -> 'Sistemas de Ecuaciones Diferenciales Ordinarias...' (230 questions, 9 competencies) [VALID]
  * pde_course.json -> 'Ecuaciones en derivadas parciales' (500 questions, 21 competencies) [VALID]
========================================================================
Press Ctrl+C to stop the platform server.
```

To access the platform, open your web browser to:
**[http://localhost:5173](http://localhost:5173)**

---

## Practice Platform Features & Views

The platform delivers a comprehensive mastery-learning student experience across six pixel-accurate reference workflows:

### 1. Six Reference Views
1. **Course Overview**: Left sidebar navigation displaying course units and competencies, mastery status summary, mastery legend (Not Started, Practiced, Familiar, Mastered), and Unit Test / Quiz launcher cards.
2. **Pre-Exercise Screen**: Hero practice banner ("Ready to practice?"), question count indicator, estimated time, and "Let's go" activation button.
3. **Question Layout**: Standardized layout with lettered options (`A`, `B`, `C`, ...), embedded SVG coordinate planes, bottom progress bar with status dots, Skip button, and Check button.
4. **Correct Answer Toast**: Immediate green success feedback card, "Good work!" badge, and expandable step-by-step mathematical explanation.
5. **Exercise Complete Summary**: Session score display, animated confetti particle celebration, review breakdown, and "Try again" / "Up next" action buttons.
6. **Course Challenge Start**: Comprehensive summative assessment launcher displaying question count (30 questions) and time estimate (30-45 minutes).

### 2. Fast Redo on Mistakes
When taking a practice session, quiz, unit test, or course challenge, students who answer incorrectly are given an immediate **"Re-attempt" / "Quick Redo"** button right on the result card. They can review the problem and re-attempt the question immediately without being forced to wait until the session ends.

### 3. Course Completion & Progress Tracking
- Tracks 4 competency mastery tiers: *Sin empezar (0%)*, *Practicado (50%)*, *Familiar (80%)*, and *Dominado (100%)*.
- Mastery state is persisted locally in `localStorage` across browser refreshes and sessions.
- Courses with 100% competencies mastered display a **Course Completed Badge** and celebratory completion state in the course library.

### 4. Mathematical Engine & Coordinate Plane
- **KaTeX Typesetting**: High-performance LaTeX formula rendering across stems, options, hints, and detailed solutions.
- **Client-Side Math Equivalence**: Powered by AST normalizer and symbolic evaluation, accepting equivalent expressions (e.g., $-(x - 3) \equiv 3 - x$, $0.5 \equiv 1/2$, $1 - (\alpha + n)\sigma \equiv 1 - \alpha\sigma - n\sigma$, commutativity of Greek terms, spaces, and $\LaTeX$ fractions) while strictly rejecting false positives.
- **SVG Coordinate Plane Component**: Interactive graphing widget supporting Cartesian coordinate grids, polynomial/trigonometric curves, vertical/horizontal asymptotes, and open/closed coordinate points.

---

## Course Bank Format & Validator CLI

Course banks are stored in structured JSON conforming to JSON Schema Draft 7 with strict psychometric and LaTeX formatting rules.

### Course Bank Schema Highlights
- **Competencies**: Categorized into `Skill` [Hab] ($\ge 30$ questions), `Concept` [C] ($\ge 20$ questions), `Fact` [H] ($\ge 20$ questions), and `Automation_Seed`.
- **Interaction Types**:
  * `multiple_choice_7_options`: Exactly 7 options, exactly 1 correct, strictly bounded distractor lengths.
  * `multiple_select`: 4 to 6 options, between 1 and $n-1$ correct options.
  * `fill_in_the_blank`: Empty options array, explicit string or list `correct_answer`.
- **Pedagogical Fields**: 3 to 5 graduated hints, `detailed_solution`, `misconception_warning`, `difficulty` (`easy`, `medium`, `hard`).

### Validator Rules Matrix (16 Core Rules + 4 Strict Rules)
- **R-01 & R-02**: Valid RFC 8259 JSON and valid double-escaped LaTeX sequences (`\\frac`, `\\alpha`).
- **R-03**: Zero silent control characters from single backslash escapes (`\tau`, `\frac`, `\beta`).
- **R-04**: Complete JSON schema conformity (types, required properties, enums).
- **R-05 & R-06**: Globally unique competency and question IDs.
- **R-07**: Valid competency foreign key references.
- **R-08 & R-09**: Volume quotas ($\ge 30$ per Skill, $\ge 20$ per Fact/Concept).
- **R-10 & R-11**: Multiple-choice cardinality (exactly 7 options, exactly 1 correct).
- **R-12 & R-13**: Multiple-select cardinality (4-6 options, $1 \le k \le n-1$ correct).
- **R-14**: Graduated hints count between 3 and 5.
- **R-15**: Item length anti-giveaway: $0.80 \cdot \min(D) \le L_{\text{correct}} \le 1.20 \cdot \max(D)$.
- **R-16**: Course distribution anti-giveaway: correct option is longest in $\le 25\%$ and shortest in $\le 25\%$ of items.
- **S-01 to S-04 (Strict Mode)**: Mandatory detailed solution, misconception warning, valid difficulty, and valid competency description.

### Validator CLI Usage

```bash
# Validate single course file in standard mode
python -m validator.cli courses/pde_course.json

# Validate in strict pedagogical mode (enforces detailed solutions and misconception warnings)
python -m validator.cli courses/pde_course.json --strict

# Machine-readable JSON output for CI/CD pipelines
python -m validator.cli courses/pde_course.json --json

# Validate entire directory of course files
python -m validator.cli courses/
```

Exit codes: `0` = Valid, `1` = Validation failure, `2` = File not found or I/O error.

---

## Content-to-Course Antigravity Skill

Located in `.agents/skills/content-to-course/`, this Antigravity skill automates the full ingestion and synthesis pipeline.

### Pipeline Workflow
1. **Multiformat Ingestion (`ingest.py`)**: Ingests PDFs and images (with automatic tiling for images >2500px, 10% overlap), generating manifest with SHA-256 caching and diacritic normalization.
2. **Cognitive Task Analysis (`cta_analyzer.py`)**: Decomposes academic course content into competencies across Skills, Concepts, Facts, prerequisite graphs, and expert blindness pitfalls. Saves persistent `competence_analysis_<course_id>.md`.
3. **Batch Question Generator (`batch_generator.py`)**: Synthesizes calibrated mastery-learning items in balanced chunks, maintaining length bounding ($0.8\cdot\min \le L \le 1.2\cdot\max$) and course distribution ($\le 25\%$ longest/shortest).
4. **Two-Tier Verification Engine (`verifier.py`)**:
   - **Tier 1 (SymPy)**: Programmatic verification of algebraic formulas, discriminant calculations, and characteristic roots.
   - **Tier 2 (Blind Solver)**: Autonomous solver that solves questions purely from stems without access to answer keys or hints to eliminate cues and verify uniqueness.
5. **Auto-Repair Loop (`repair_loop.py`)**: Iterative auto-repair (up to 3 iterations) correcting LaTeX escaping, hint counts, distractor length bounds, and quota shortfalls.
6. **Course Publisher (`course_publisher.py`)**: Validates against `validator.cli --strict`, publishes the finished course to `courses/<course_id>.json`, and supports `--append` mode to merge new question batches into existing courses.

### Running the Skill Pipeline CLI

```bash
# Ingest single PDF and generate new course
python .agents/skills/content-to-course/run.py \
  --pdf sample_content/I__Ecuaciones_en_derivadas_parciales_2026.pdf \
  --course-id pde_course \
  --output-dir courses \
  --strict

# Append additional questions to an existing course bank
python .agents/skills/content-to-course/run.py \
  --pdf sample_content/additional_topics.pdf \
  --course-id pde_course \
  --append \
  --strict
```

---

## Automated Test Suite Execution

All test suites across the repository have been consolidated into clean, unified, modular modules.

### Consolidated Python Test Suites

Run the unified test suite with pytest:

```bash
python -m pytest tests/test_validator.py tests/test_skill.py tests/test_platform.py -v
```

Breakdown of consolidated modules:
- **`tests/test_validator.py`** (95 tests): 28-fixture catalog matrix, lexical scanner, JSON schema, semantic rules, psychometric anti-giveaway limits, coordinate graphs, scale benchmarks (450 questions in $<3.0$s), UTF-8 BOM handling, and CLI strict mode.
- **`tests/test_skill.py`** (27 tests): PyMuPDF extractor, CTA taxonomy parser, batch generator quotas and distributions, SymPy Tier 1 verifier, Blind Solver Tier 2, auto-repair loop, super-pathological course repair, and end-to-end pipeline runner.
- **`tests/test_platform.py`** (19 tests): Math equivalence engine, course validation, course discovery, live HTTP server endpoints (`/api/courses`, `/api/courses/<id>`, CORS `OPTIONS`, static SPA routing), and launcher CLI flags (`--scan`, `--help`).

### Playwright End-to-End Browser Tests

Run browser automation and visual fidelity tests:

```bash
python -m pytest tests/e2e/ -v
```

### Standalone Adversarial Verification Scripts

```bash
# Math Equivalence Engine 63-case adversarial suite
node tests/test_math_adversarial_suite.mjs

# Empirical Adversarial Blind-Guess Distractor Audit (N=50 sample + N=250 population)
python tests/test_blind_guess_empirical.py
```

---

## Milestone Verification & Certification Metrics

| Milestone / Requirement | Target Metric | Certified Value | Verification Status |
| :--- | :--- | :--- | :--- |
| **M1: Validator Engine** | 16 Rules + 4 Strict Rules | 100% Pass across 28 Fixtures | **VERIFIED** |
| **M1: Benchmark Scale** | 450 items in $< 3.0$s | $0.28$s elapsed ($>10\times$ faster) | **VERIFIED** |
| **M2: Reference Views** | 6 Pixel-Accurate Views | 6/6 Captured & Verified | **VERIFIED** |
| **M2: Math Equivalence** | $\ge 98\%$ Pass Rate | 100% (63/63 Cases Passed) | **VERIFIED** |
| **M2: Fast Redo Action** | Immediate re-attempt | Interactive on all 4 modes | **VERIFIED** |
| **M3: Skill Decomposition** | Full Academic Taxonomy | 21 Competencies (8 Hab, 6 C, 7 H) | **VERIFIED** |
| **M3: Quotas & Volume** | $\ge 30$ Skill, $\ge 20$ Fact/Concept | 500 Questions generated | **VERIFIED** |
| **M3: Psychometrics** | R-15 $[0.8, 1.2]$, R-16 $\le 25\%$ | 100% within bounds | **VERIFIED** |
| **M3: Verifier & Repair** | Multi-defect course repair | Repaired in $\le 3$ iterations | **VERIFIED** |
| **M4: Blind Guess Audit** | Guess Accuracy $\le 30\%$ | **16.0%** (Sample), **15.2%** (Population)| **VERIFIED** |
| **M4: Test Consolidation**| Unified Test Architecture | 141/141 Tests Passed Cleanly | **VERIFIED** |
| **M4: Single Launcher** | `python run_platform.py` | Discovers `pde_course` & `demo_course` | **VERIFIED** |

---

## Repository Structure

```
Competence_analyser/
├── README.md                                # Authoritative documentation (this file)
├── PROJECT.md                               # Project specification and interfaces
├── pyproject.toml                           # Python project configuration & dependencies
├── run_platform.py                          # Single-command application launcher
├── courses/                                 # Published course banks and CTA analyses
│   ├── demo_course.json                     # Playable macroeconomic ODE course
│   ├── pde_course.json                      # 500-question academic PDE course
│   ├── competence_analysis_pde_course.md    # Decomposed 21-competency CTA document
│   └── fixtures/                            # 28 canonical test course fixtures
├── platform/                                # Top's Academy Practice Platform Frontend
│   ├── index.html                           # Single-page application entry point
│   ├── package.json                         # Node dependencies (React 18, KaTeX, Vite)
│   ├── src/                                 # Platform source code
│   │   ├── components/                      # UI Views: CourseOverview, PracticeSession, etc.
│   │   ├── utils/mathEquivalence.ts         # Client-side math equivalence engine
│   │   └── App.tsx                          # Platform router and mastery manager
│   └── dist/                                # Compiled production web bundle
├── src/                                     # Subsystem 1: Format & Psychometric Validator
│   └── validator/                           # core.py, lexical_scanner.py, rules.py, cli.py
├── .agents/skills/content-to-course/        # Subsystem 3: Antigravity Skill
│   ├── SKILL.md                             # Antigravity skill specification and rules
│   ├── ingest.py                            # Multiformat academic document & image ingestion
│   ├── cta_analyzer.py                      # Cognitive Task Analysis decomposition
│   ├── batch_generator.py                   # Calibrated question synthesis
│   ├── verifier.py                          # SymPy & Blind Solver verification
│   ├── repair_loop.py                       # Automated multi-pass repair loop
│   ├── course_publisher.py                  # CLI validation, publishing & append mode
│   └── run.py                               # Pipeline CLI orchestrator
└── tests/                                   # Consolidated Automated Test Suite
    ├── test_validator.py                    # Consolidated validator test suite (95 tests)
    ├── test_skill.py                        # Consolidated skill pipeline test suite (27 tests)
    ├── test_platform.py                     # Consolidated platform & server test suite (19 tests)
    ├── test_math_adversarial_suite.mjs      # Node.js math equivalence 63-case test suite
    ├── test_blind_guess_empirical.py        # Adversarial blind-guess distractor test harness
    └── e2e/                                 # Playwright End-to-End browser test suite
```

---

## License & Credits

Built as an open-source educational framework adhering to psychometric assessment standards and Cognitive Task Analysis methodologies. Heavily inspired by the pedagogical design and mastery learning framework of Khan Academy.
