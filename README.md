# Top's Academy Platform & Content-to-Course AI Pipeline

[![Tests](https://img.shields.io/badge/Tests-363%20Passed-brightgreen.svg)]()
[![Validator](https://img.shields.io/badge/Format%20Validator-21%20Rules%20%2B%203%20Strict-blue.svg)]()
[![Platform](https://img.shields.io/badge/Platform-React%2018%20%2B%20Vite%20%2B%20KaTeX-61dafb.svg)]()
[![Math Equivalence](https://img.shields.io/badge/Math%20Equivalence-81%20Adversarial%20Cases%20100%25-success.svg)]()
[![Skills Suite](https://img.shields.io/badge/Antigravity%20Skills-5%20Specialized-orange.svg)]()

> [!NOTE]
> **Pedagogical & UX Inspiration:**
> This project has been heavily inspired by Khan Academy for its mastery learning framework, progressive hint scaffolding, multi-tiered competency progression, and student practice workflows.

An end-to-end educational system that ingests academic university course materials (syllabi, lecture slide decks, handwritten notes, and textbook chapters) in PDF format, performs **Cognitive Task Analysis (CTA)** via a parallelized Map-Reduce architecture to extract competencies and prerequisite graphs, generates calibrated **mastery learning exercise banks** with sandboxed Python parametric templates, enforces mathematical anti-giveaway and KaTeX syntax guarantees, independently arbitrates answer keys via **Stratified Blind Judges** under epistemic closure, auto-repairs validation errors, and serves an interactive web practice platform with real-time mastery tracking, an AST-based mathematical equivalence engine, and educational safeguards.

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Single Command Launcher](#single-command-launcher)
3. [Practice Platform Features & Safeguards](#practice-platform-features--safeguards)
4. [Course Bank Format & Validator CLI (21 Rules + 3 Strict)](#course-bank-format--validator-cli-21-rules--3-strict)
5. [Content-to-Course Antigravity Skill Ecosystem](#content-to-course-antigravity-skill-ecosystem)
6. [Automated Test Suite Execution](#automated-test-suite-execution)
7. [Active Production Courses & Audit Registry](#active-production-courses--audit-registry)
8. [Milestone Verification & Certification Metrics](#milestone-verification--certification-metrics)
9. [Repository Structure](#repository-structure)

---

## System Architecture

The project consists of interconnected, independently testable subsystems coordinated by specialized multi-agent skills:

```
                            +-----------------------------------------------+
                            |            Academic Course Materials          |
                            |  (PDFs, Beamer Decks, Handwritten Notes, Ink) |
                            +-----------------------+-----------------------+
                                                    |
                                                    v
+---------------------------------------------------------------------------------------------------+
| Subsystem 3: Content-to-Course Pipeline v3 (.agents/skills/content-to-course/)                     |
|                                                                                                   |
|  Stage 0: Ingestion & Slicing  -->  Stage 1: CTA Map-Reduce      -->  Stage 2: Shard Planning     |
|  (PyMuPDF corpus extraction,         (Sectional Analyzers +           (Self-contained payloads,   |
|   direct PDF reading, session slices) Harmonizer & DAG Integrator)     embedded DSL, K <= 8)      |
|                                                                                |                  |
|  Stage 6: Publishing & Append  <--  Stage 5: Stratified Judges   <--  Stage 3 & 4: Authors & Sandbox|
|  (Strict validation, metadata,       (Stratified 2 items/comp,         (Shift-Left TPL-VAR >=0.50,|
|   atomic sync to courses/)            epistemic closure, key norm.)     in-process assembly <6.5s)|
+---------------------------------------------------+-----------------------------------------------+
                                                    | Outputs validated course JSON
                                                    v
+---------------------------------------------------------------------------------------------------+
| Subsystem 1: Format & Psychometric Validator (src/validator/)                                     |
|                                                                                                   |
|  Pass 1: Lexical Scanner   -->  Pass 2: JSON Schema & Semantics  -->  Pass 3: Quality & KaTeX Mode|
|  - RFC 8259 raw syntax          - Draft-07 Schema conformity          - 21 Formal Rules (R-01..22)|
|  - Silent LaTeX escapes         - Referential integrity (R-05..R-07)  - 3 Strict Rules (S-01..S-03)|
|    (\tau, \rho, \frac, \nu)     - Volume quotas: >=30 Skill,          - Anti-giveaway bounds      |
|  - Raw newline detection          >=20 Fact/Concept (R-08..R-09)        [0.8 min, 1.2 max], <=25% |
|                                                                       - KaTeX macro arity, nested |
|                                                                         macros, environment lint  |
+---------------------------------------------------+-----------------------------------------------+
                                                    | Verified courses saved to courses/
                                                    v
+---------------------------------------------------------------------------------------------------+
| Subsystem 2: Top's Academy Practice Platform (platform/ & run_platform.py)                          |
|                                                                                                   |
|  - Backend Discovery Server: Auto-scans courses/, exposes REST API, isolates invalid files        |
|  - Modern Web Frontend: React 18 + Vite + TypeScript + Tailwind CSS + Lucide Icons               |
|  - Mathematical Equivalence Engine: Client-side AST normalizer + Monte Carlo sampler supporting   |
|    Spanish decimal commas (0,8333 == 0.8333), fractions (5/6 == 0,8333), Greek symbols, tolerances |
|  - Educational Safeguard (3-Strikes Reveal): Locks inputs after 3 failed attempts, expands         |
|    step-by-step solution and misconception warning, awards 0 credit, and guides user to next item |
|  - Fast Redo on Mistakes: Immediate re-attempt across Practice, Quizzes, Unit Tests, Challenge    |
|  - Vector Coordinate Plane: SVG widget for curves, asymptotes, open/closed points                |
|  - Static Bundle Pipeline: Compiles to platform/dist/ with static courses bundle for GitHub Pages|
+---------------------------------------------------------------------------------------------------+
                                                    | Telemetry & QA Evaluation
                                                    v
+---------------------------------------------------------------------------------------------------+
| Subsystem 4: Forensic Telemetry & Quality Evaluation Skills Suite (.agents/skills/)               |
|                                                                                                   |
|  - course-qa-evaluator: QM & OSCQR audit across 5 dimensions (Architecture, Items, Hints, Align, KaTeX)|
|  - c2c-run-auditor: Token decomposition (input, output, cache, thinking), throughput & benchmarks |
|  - c2c-unified-auditor: Concurrent orchestration merging pedagogical QA with execution telemetry |
|  - delete-course: Fast safe course deletion (<300ms) with historical audit report preservation    |
+---------------------------------------------------------------------------------------------------+
```

---

## Single Command Launcher

Launch the complete application (both the backend course discovery server and the web interface) with a single command:

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

When starting, the platform scans `courses/`, validates all course banks with the format validator, and reports discovered courses:

```text
========================================================================
Scanning courses in 'D:\Augusto\personal_portfolio\Tops_academy\courses'...
Found 1 course file(s):
------------------------------------------------------------------------
File:         estadistica3_regresion_v3.json
ID:           estadistica3_regresion_v3
Title:        Estadística III: Econometría y Modelo de Regresión Lineal
Status:       VALID
Competencies: 16
Questions:    390
------------------------------------------------------------------------
Scan complete.
========================================================================
```

Open your web browser to: **[http://localhost:5173](http://localhost:5173)**

---

## Practice Platform Features & Safeguards

The platform delivers a comprehensive mastery-learning student experience across six pixel-accurate reference workflows:

### 1. Six Reference Views
1. **Course Overview**: Left sidebar navigation displaying course units and competencies, mastery status summary, mastery legend (*Sin empezar*, *Practicado*, *Familiar*, *Dominado*), and Unit Test / Quiz launcher cards.
2. **Pre-Exercise Screen**: Hero practice banner ("Ready to practice?"), question count indicator, estimated time, and "Let's go" activation button.
3. **Question Layout**: Standardized layout with lettered options (`A`, `B`, `C`, ...), embedded SVG coordinate planes, bottom progress bar with status dots, Skip button, and Check button.
4. **Feedback Card & Toast**: Immediate feedback card with downward pointer, contextual success/error messages, and expandable step-by-step mathematical explanation.
5. **Exercise Complete Summary**: Session score display, animated confetti particle celebration, review breakdown, and "Try again" / "Up next" action buttons.
6. **Course Challenge Start**: Comprehensive summative assessment launcher displaying question count (30 questions) and time estimate (30-45 minutes).

### 2. Educational Safeguard: 3-Strikes Solution Reveal
In `PracticeSession.tsx` and `FeedbackToast.tsx`, the platform tracks consecutive incorrect attempts per item:
- **Attempts 1 & 2**: Displays diagnostic feedback, highlights misconception warnings, and offers immediate re-attempt via the **"Re-intentar" / "Quick Redo"** action.
- **Attempt 3 (Final Strike)**: Locks the question inputs, displays `"Máximo de intentos alcanzado (3/3)"`, automatically reveals the correct answer, expands the full step-by-step mathematical solution and misconception warning, awards **0 mastery points**, and transforms the action into "Siguiente pregunta".

### 3. Mathematical Engine & Coordinate Plane
- **KaTeX Typesetting**: High-performance LaTeX formula rendering across stems, options, hints, and detailed solutions.
- **Client-Side Math Equivalence Engine**: AST normalizer and Monte Carlo sampler accepting mathematically equivalent expressions:
  - Spanish decimal comma notation: `0,8333` $\equiv$ `0.8333`
  - Decimal-to-fraction equivalence: `5/6` $\equiv$ `0,8333`
  - Factored vs. expanded algebra: $-(x - 3) \equiv 3 - x$, $(x+2)(x-2) \equiv x^2 - 4$
  - Commutativity of Greek terms and products: $1 - (\alpha + n)\sigma \equiv 1 - \alpha\sigma - n\sigma$
  - Negative powers and LaTeX fractions: $\frac{1}{x} \equiv x^{-1}$, $\frac{a+b}{c} \equiv (a+b)/c$
  - Strict rejection of false positives (sign differences, power mismatches, alien variables). Verified by **81 adversarial test cases (100% pass rate)**.
- **SVG Coordinate Plane Component**: Interactive graphing widget supporting Cartesian coordinate grids, polynomial/trigonometric curves, vertical/horizontal asymptotes, and open/closed coordinate points.

---

## Course Bank Format & Validator CLI (21 Rules + 3 Strict)

Course banks are stored in structured JSON conforming to JSON Schema Draft-07 with strict psychometric and LaTeX formatting rules.

### Validator Rules Matrix

| Rule ID | Code | Category | Specification / Invariant Enforced |
| :--- | :--- | :--- | :--- |
| **R-01** | `ERR_RAW_NEWLINE` | Lexical | RFC 8259 conformity; zero raw unescaped newlines/tabs inside string literals |
| **R-02** | `ERR_INVALID_ESCAPE` | Lexical | Double-escaped LaTeX sequences (`\\frac`, `\\alpha`, `\\sigma`) |
| **R-03** | `ERR_SILENT_ESCAPE` | Lexical | Zero silent control characters from single backslash escapes (`\tau`, `\frac`, `\beta`, `\nu`, `\text`) |
| **R-04** | `ERR_SCHEMA_VALIDATION` | Schema | Draft-07 JSON Schema validation and fill-in-the-blank answer key presence |
| **R-05** | `ERR_DUP_COMPETENCY` | Integrity | Globally unique competency IDs across the course |
| **R-06** | `ERR_DUP_QUESTION` | Integrity | Globally unique question IDs across the course |
| **R-07** | `ERR_MISSING_COMPETENCY` | Referential | Valid competency foreign key references |
| **R-08** | `ERR_COUNT_SKILL` | Quota | Volume quota: $\ge 30$ questions per Skill (`Hab`) competency |
| **R-09** | `ERR_COUNT_CONCEPT` | Quota | Volume quota: $\ge 20$ questions per Fact (`H`) or Concept (`C`) competency |
| **R-10** | `ERR_MC_COUNT` | Cardinality | Multiple-choice 7 options cardinality (exactly 7 options) |
| **R-11** | `ERR_MC_CORRECT` | Cardinality | Multiple-choice correct answer cardinality (exactly 1 correct option) |
| **R-12** | `ERR_MS_COUNT` | Cardinality | Multiple-select option count between 4 and 6 options |
| **R-13** | `ERR_MS_CORRECT` | Cardinality | Multiple-select correct answers between 1 and $n-1$ |
| **R-14** | `ERR_HINT_COUNT` | Scaffolding | Graduated hints count between 3 and 5 |
| **R-15** | `ERR_ITEM_LENGTH_RATIO` | Psychometrics | Distractor length anti-giveaway: $0.80 \cdot \min(D) \le L_{\text{correct}} \le 1.20 \cdot \max(D)$ |
| **R-16** | `ERR_COURSE_LENGTH_DIST`| Psychometrics | Course anti-giveaway: correct option is longest in $\le 25\%$ and shortest in $\le 25\%$ of items |
| **R-17** | `ERR_PLACEHOLDER_RATIONALE`| Quality | Formative error rationales without placeholders ("placeholder", "n/a", "none", "error") |
| **R-18** | `ERR_META_GIVEAWAY` | Psychometrics | Confinement of meta-information: forbids giveaway terms (*"erróneamente"*, *"omitiendo"*) in visible option content |
| **R-19** | `ERR_ANSWER_LEAK` | Quality | Answer leak prevention: forbids embedding exact `correct_answer` value in fill-in-the-blank stems |
| **R-20** | `ERR_LATEX_SYNTAX` | KaTeX Mode | Strict KaTeX mode: delimiter parity (`$`, `$$`), no triple dollars (`$$$`), no residual `{{...}}`, no `{var}`, macro arity checks (`\frac{}{}`), nested macro validations, environment closures |
| **R-22** | `ERR_MS_MISSING_RATIONALE`| Quality | Mandatory diagnostic error rationale in all multiple-select distractors (`is_correct: false`) |
| **S-01** | `ERR_STRICT_MISSING_SOLUTION` | Strict Mode | Mandatory step-by-step mathematical explanation |
| **S-02** | `ERR_STRICT_MISSING_MISCONCEPTION` | Strict Mode | Mandatory misconception warning |
| **S-03** | `ERR_STRICT_MISSING_DIFFICULTY` | Strict Mode | Explicit difficulty rating (`easy`, `medium`, `hard`) |

### Validator CLI Usage

```bash
# Validate single course file in standard mode
python -m src.validator.cli courses/estadistica3_regresion_v3.json

# Validate in strict pedagogical mode (enforces detailed solutions, misconceptions, difficulties)
python -m src.validator.cli courses/estadistica3_regresion_v3.json --strict

# Machine-readable JSON output for CI/CD pipelines
python -m src.validator.cli courses/estadistica3_regresion_v3.json --json

# Validate entire directory of course files
python -m src.validator.cli courses/
```

Exit codes: `0` = Valid, `1` = Validation failure, `2` = File not found or I/O error.

---

## Content-to-Course Antigravity Skill Ecosystem

Located under `.agents/skills/`, five specialized skills automate authoring, quality evaluation, telemetry, and lifecycle management:

### 1. `content-to-course` (v3 High-Throughput Pipeline)
- **Multiformat Ingestion (`ingest.py`)**: PyMuPDF extraction, session slicing (`generate_session_slices`), and direct PDF reading (`work/pre_cta_manifest.json`).
- **CTA Map-Reduce (`run.py --stage cta-map` & `--stage cta-reduce`)**:
  - *Phase Map*: Concurrent *Sectional CTA Analyzers* processing individual session slices.
  - *Phase Reduce*: *CTA Harmonizer & DAG Integrator* (`cta_merge.py`) assembling `work/cta.json` with canonical IDs and inter-session prerequisite DAGs.
- **Shard Planning (`plan_shards.py`)**: Decomposes competencies into self-contained shard payloads (`work/shards/shard_XX.json`) with embedded DSL references and dynamic shard caps ($K \le 8$).
- **Shift-Left Shard Authoring (`check_templates.py`)**: Subagents author parametric templates with mandatory `stem_variants >= 3` and simulated diversity $\ge 0.50$ (Rule `TPL-VAR`). Defective templates fail locally before orchestrator handoff.
- **Sandboxed Assembly & Instantiation (`engine/assemble.py`, `engine/instantiate.py`)**: In-process execution generating 500+ items in $<6.5$ seconds with invariant checking (`engine/invariants.py`).
- **Stratified Blind Judges (`judge.py`)**: Stratified sampling of 2 items per competency evaluated under epistemic closure with normalized keys.
- **Course Publisher (`course_publisher.py`)**: Validates strictly and publishes atomically to `courses/<course_id>.json`.

### 2. `course-qa-evaluator`
Evaluates courses against Quality Matters (QM), OSCQR Higher Ed, and Mastery Learning standards across 5 dimensions: Architecture (4 pts), Items & Distractors (5 pts), Scaffolding (5 pts), Cognitive Alignment (4 pts), and KaTeX/Ergonomics (2 pts).

### 3. `c2c-run-auditor`
Audits execution runs extracting token telemetry (input, output, cache read, thinking), latencies, stage bottlenecks, unit economics (tokens/question, sec/question), and maintains `reports/c2c_audits/historical_benchmark.md` and `audit_registry.json`.

### 4. `c2c-unified-auditor`
Unified orchestration skill that dispatches the Run Auditor and Course QA Evaluator concurrently, generating consolidated reports with interactive navigation.

### 5. `delete-course`
Safely deletes courses in $<300$ms, removing course JSON and competence markdown files while preserving historical audit reports with `ELIMINADO` status and strictly enforcing the immutability of `content/`.

---

## Automated Test Suite Execution

The repository maintains an automated test matrix with 100% pass rates across unit, integration, adversarial, and browser suites:

### 1. Python Consolidated Test Suites (367 items / 363 passed, 4 skipped in 18.05s)

```powershell
# Run consolidated pytest suite (367 items / 363 passed, 4 skipped in ~18s)
.venv\Scripts\python.exe -m pytest -v
```

Breakdown of test suites:
- **`tests/test_validator.py`** (144 tests): Lexical scanner, schema, core rules R-01..R-16, extended rules R-17..R-20, R-22, strict rules S-01..S-03, KaTeX macro arity, nested macros, and environments.
- **`tests/test_engine_invariants_adversarial.py`** (51 tests): Invariant validation, sandboxed assembly, length bounding, option deduplication.
- **`tests/test_sandbox_adversarial.py`** (49 tests): AST sandbox isolation, blocked syscalls, forbidden imports, memory safety.
- **`tests/test_skill.py`** (33 tests): Document ingestion, CTA taxonomy, batch generation, SymPy Tier 1 verifier, blind solver, publisher.
- **`tests/test_platform.py`** (19 tests): HTTP server endpoints, static routing, course discovery, launcher CLI flags.
- **`tests/test_cta_mapreduce.py`** (16 tests): Sectional corpus slicing, `cta_merge.py`, DAG prerequisite validation, distractor deduplication.
- **`tests/test_c2c_validator_prescriptive.py`** (12 tests): Prescriptive repair suggestions and schema conformity.
- **`tests/test_dispatch_scope.py`** (10 tests): Role isolation and subagent prompt contracts.
- **`tests/test_delete_course.py`** (8 tests): Safe deletion lifecycle, report stamping, content immutability.
- **`tests/test_handouts.py`** (8 tests): Vision handout fallback processing.
- **`tests/test_pipeline_optimizations.py`** (6 tests): Performance optimizations and multi-core `ProcessPoolExecutor` validation.
- **`tests/test_skill_v3.py`** (6 tests): v3 high-throughput pipeline runner integration.
- **`tests/test_template_variability.py`** (5 tests): Rule `TPL-VAR`, `stem_variants >= 3`, and diversity ratio $\ge 0.50$.

### 2. Node.js Client-Side & Standalone Verification Suites

```powershell
# Math Equivalence Engine 81-case adversarial suite (100% pass)
node tests/test_math_adversarial_suite.mjs

# Question evaluation & normalization test suite (1048 MC & MS items verified across courses, 100% pass)
node tests/test_question_grading.mjs

# Keyboard navigation & auto-advance logic suite
node tests/test_keyboard_navigation.mjs

# Unit isolation and shuffle boundaries suite
node tests/test_unit_isolation.mjs

# Empirical adversarial blind-guess distractor test harness (4% guess rate, <= 30% target)
.venv\Scripts\python.exe tests/test_blind_guess_empirical.py
```

### 3. Playwright End-to-End Browser Tests

```powershell
python -m pytest tests/e2e/ -v
```

Verifies the 10 acceptance criteria (AC-01 through AC-10), the 3-strikes safeguard (AC-11), Spanish comma notation (AC-12), and captures the 6 visual fidelity screenshots (VF-01).

---

## Active Production Courses & Audit Registry

| Course Identifier | Title | Questions | Competencies | Validation Status | Quality Score | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **`estadistica3_regresion_v3`** | Estadística III: Econometría y Modelo de Regresión Lineal | 390 | 16 | **VALID (Strict)** | **19.4 / 20.0** | **Activo / Producción** |

- **Archived Courses**: Previous generation courses (`pde_course`, `sistemas_edos`, `solow_model_old`) are preserved in `archive_rejected_courses/` for regression testing and forensic audit comparisons.
- **Historical Telemetry Registry**: Tracked in `reports/c2c_audits/historical_benchmark.md` and `reports/c2c_audits/audit_registry.json`, recording up to **6.69x parallel speedup** and **1.96 s/question** throughput.

---

## Milestone Verification & Certification Metrics

| Milestone / Requirement | Target Metric | Certified Value | Verification Status |
| :--- | :--- | :--- | :--- |
| **M1: Validator Engine** | 21 Rules + 3 Strict Rules | 100% Pass across 28 Fixtures | **VERIFIED** |
| **M1: Benchmark Scale** | 450 items in $< 3.0$s | $0.28$s elapsed ($>10\times$ faster) | **VERIFIED** |
| **M2: Reference Views** | 6 Pixel-Accurate Views | 6/6 Captured & Verified | **VERIFIED** |
| **M2: Math Equivalence** | $\ge 98\%$ Pass Rate | 100% (81/81 Cases Passed) | **VERIFIED** |
| **M2: Fast Redo Action** | Immediate re-attempt | Interactive on all 4 modes | **VERIFIED** |
| **M2: 3-Strikes Safeguard**| Reveal after 3 attempts | Locked inputs, auto-solution | **VERIFIED** |
| **M3: Skill Pipeline v3** | High-Throughput & Map-Reduce | 16/16 CTA Map-Reduce Tests | **VERIFIED** |
| **M3: Stem Diversity Gate** | Diversity ratio $\ge 0.50$ | 5/5 Template Variability Tests | **VERIFIED** |
| **M4: Automated Test Matrix**| Unified Test Architecture | 363 Pytest + 81 Node Math + 1048 Item Grading Passed | **VERIFIED** |
| **M4: Single Launcher** | `python run_platform.py` | Discovers `estadistica3_regresion_v3` | **VERIFIED** |
| **M5: Forensic Telemetry** | Granular multi-agent audit | `c2c-run-auditor` & Registry | **VERIFIED** |
| **M6: QA Audit Standards** | QM & OSCQR Accreditation | `course-qa-evaluator` & Reports | **VERIFIED** |
| **M7: KaTeX Saneamiento** | Macro arity & environment lint | Rule R-20 & Clean Kurs | **VERIFIED** |

---

## Repository Structure

```
Tops_academy/
├── README.md                                # Authoritative documentation (this file)
├── PROJECT.md                               # Project specification, inventory, and interfaces
├── FUTURE_MILESTONES.md                     # Roadmap for Mobile PWA and Local Daemon
├── TEST_INFRA.md                            # Comprehensive test infrastructure specification
├── TEST_READY.md                            # Test suite verification checklist
├── pyproject.toml                           # Python project configuration & dependencies
├── run_platform.py                          # Unified single-command platform launcher
├── courses/                                 # Active published course banks and CTA analyses
│   ├── estadistica3_regresion_v3.json       # Active certified course bank (390 questions, 16 comps)
│   ├── competence_analysis_estadistica3_regresion_v3.md # 16-competency CTA document
│   └── fixtures/                            # 28 canonical test course fixtures
├── archive_rejected_courses/                # Historical archived course banks
├── content/                                 # Academic source documents (zero-bloat gitignored)
│   ├── README.md                            # Ingestion guidelines & catalog
│   └── Solow_model/                         # Source academic PDFs
├── docs/                                    # Architectural research and proposals
│   └── proposals_cta_mapreduce_and_shard_autocheck.md # CTA Map-Reduce & Shard Auto-Check
├── reports/                                 # Forensic telemetry and QA audit reports
│   ├── qa_audits/                           # Quality Matters / OSCQR audit reports
│   │   ├── SUITE_QA_AUDIT_REPORT.md         # Master suite QA audit report
│   │   ├── COURSE_CREATION_IMPROVEMENTS.md  # Architectural recommendations
│   │   └── estadistica3_regresion_v3_qa_report.md # Course QA report
│   └── c2c_audits/                          # Execution telemetry & unit economics
│       ├── historical_benchmark.md          # Multi-run benchmark evolution
│       └── audit_registry.json              # Machine-readable telemetry registry
├── platform/                                # Top's Academy Practice Platform Frontend
│   ├── index.html                           # Single-page application entry point
│   ├── package.json                         # Node dependencies (React 18, KaTeX, Vite, mathjs)
│   ├── vite.config.ts                       # Vite bundler configuration
│   ├── src/                                 # Frontend source code
│   │   ├── components/                      # UI Views: PracticeSession, FeedbackToast, etc.
│   │   ├── utils/                           # mathEquivalence.ts, sessionShuffler.ts, etc.
│   │   └── App.tsx                          # Platform router and mastery manager
│   └── dist/                                # Compiled production web bundle & static courses
├── src/validator/                           # Subsystem 1: Format & Psychometric Validator
│   ├── cli.py                               # CLI entrypoint
│   ├── lexical_scanner.py                   # Pass 1: raw syntax & control character scanner
│   ├── schema_validator.py                  # Pass 2: Draft-07 schema validator
│   ├── rules.py                             # Pass 2 & 3: Structural, pedagogical, and KaTeX rules
│   └── psychometric_checker.py              # Pass 3: Anti-giveaway ratio checkers
├── .agents/skills/                          # Specialized Multi-Agent Skills Suite
│   ├── content-to-course/                   # Universal v3 course creation pipeline
│   ├── course-qa-evaluator/                 # Quality Matters & OSCQR QA evaluator
│   ├── c2c-run-auditor/                     # Multi-agent telemetry & performance auditor
│   ├── c2c-unified-auditor/                 # Unified orchestration auditor
│   └── delete-course/                       # Fast safe course deletion tool (<300ms)
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

---

## License & Credits

Built as an open-source educational framework adhering to psychometric assessment standards and Cognitive Task Analysis methodologies. Heavily inspired by the pedagogical design and mastery learning framework of Khan Academy.
