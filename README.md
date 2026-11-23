# Top's Academy Platform & Content-to-Course Neuro-Symbolic AI Pipeline (v4.0)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-1%2C526%2B%20Passed%20(4%20Domains)-brightgreen.svg)]()
[![Pipeline](https://img.shields.io/badge/C2C%20Pipeline-v4.0%20Form--C%20%2B%20Lean%204%20%2B%20Z3-purple.svg)]()
[![Validator](https://img.shields.io/badge/Format%20Validator-23%20Rules%20%2B%203%20Strict%20%2B%20MPRI-blue.svg)]()
[![Platform](https://img.shields.io/badge/Platform-React%2018%20%2B%20Vite%20%2B%20PWA%20%2B%20FSRS--6-61dafb.svg)]()
[![Math Equivalence](https://img.shields.io/badge/Math%20Equivalence-81%20Adversarial%20Cases%20100%25-success.svg)]()
[![Skills Suite](https://img.shields.io/badge/Antigravity%20Skills-7%20Specialized-orange.svg)]()

> [!NOTE]
> **Language & Localization Note:**
> While this repository's technical specification and open-source documentation are written in **English**, the **Top's Academy web platform UI, generated university courses, mathematical scaffolding, Socratic hints, and internal engineering roadmaps run natively in Spanish** (designed for university-level STEM, economics, statistics, and mathematical optimization courses, including native support for Spanish decimal comma notation `0,8333 == 0.8333`).
>
> **Pedagogical & Cognitive Foundation:**
> Built upon **Mastery Learning** (inspired by Khan Academy), **Cognitive Task Analysis (CTA)**, **Spaced Repetition (`FSRS-5/6`)**, and deliberate practice principles (*The Expert Myth*), emphasizing **Active Free Recall** and **Higher-Order Bloom Modalities** over passive multiple-choice elimination.

An end-to-end neuro-symbolic educational platform and multi-agent pipeline that ingests academic university materials (syllabi, Beamer slide decks, handwritten notes, and textbook chapters in PDF), performs **Cognitive Task Analysis (CTA)** via a parallelized Map-Reduce architecture to extract prerequisite DAGs, explicit assumptions (`assumptions` + `violation_consequence`), and foundation units (`PRE-XX`), compiles **4-Axis parametric exercise templates** (`Form-C` DSL with PrairieLearn `@var@` interpolation, `KaTeXAST` grammar verification, and `c2c_ver` symbolic/numeric verification), arbitrates answer keys under **Epistemic Closure** ($\alpha_{\text{Kernel}} = 0$), and serves an offline-ready **React 18 + PWA Study Harness** featuring **6 Higher-Order Bloom Modalities**, **FSRS-5/6 spaced repetition**, **Bidirectional Mastery 2.0 (80/20 hybrid bar)**, **Smart Blank-First free recall**, and an **Iron Mode (SAT Bluebook 2-Module Adaptive Exam Simulator)** with mandatory metacognitive calibration.

---

## Table of Contents

1. [Documentation Ecosystem (`docs/`)](#documentation-ecosystem-docs)
2. [System Architecture (v4.0 Neuro-Symbolic & Study Harness)](#system-architecture-v40-neuro-symbolic--study-harness)
3. [Single Command Launcher](#single-command-launcher)
4. [Practice Platform & Antigravity Study Harness Features](#practice-platform--antigravity-study-harness-features)
5. [4-Axis Authoring Architecture & 6 Higher-Order Bloom Modalities (M20)](#4-axis-authoring-architecture--6-higher-order-bloom-modalities-m20)
6. [Course Bank Format, KaTeXAST & Validator CLI (23 Rules + 3 Strict + MPRI)](#course-bank-format-katexast--validator-cli-23-rules--3-strict--mpri)
7. [Content-to-Course Antigravity Skill Ecosystem (7 Skills)](#content-to-course-antigravity-skill-ecosystem-7-skills)
8. [Automated Test Matrix (4 Isolated Domains + E2E)](#automated-test-matrix-4-isolated-domains--e2e)
9. [Active Production Courses & Benchmark Telemetry](#active-production-courses--benchmark-telemetry)
10. [Certified Milestones Registry (M1 – M20-B)](#certified-milestones-registry-m1--m20-b)
11. [Active Engineering Roadmap (`FUTURE_MILESTONES.md`)](#active-engineering-roadmap-future_milestonesmd)
12. [Repository Structure](#repository-structure)
13. [License](#license)

---

## Documentation Ecosystem (`docs/`)

All architectural specifications, historical certifications, and active roadmaps live inside [`docs/`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/):

| Document | Purpose & Scope |
| :--- | :--- |
| 🗺️ [`docs/future_milestones/FUTURE_MILESTONES.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/future_milestones/FUTURE_MILESTONES.md) | **Active Strategic Roadmap:** High-level priorities, cognitive rationale, acceptance criteria (AC), and unit economics for active milestones (**M19** $k=4$ First-Pass scaling, **M16 F2** `z3-solver`, **M9+M21** ContentCore hierarchy, **M18** Prompt-Compiler CI, **M15 F2** Lean 4). |
| 📗 [`docs/future_milestones/MILESTONES_COMPLETED.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/future_milestones/MILESTONES_COMPLETED.md) | **Certified Historical Ledger:** Forensic delivery record of all completed milestones (**M1, M1-T, M2, M2a, M3, M4, M6, M7, M8, M9 [Quick Wins + Phase A], M10, M11, M12, M13, M14, M14-B, M15 [F1 + DRT], M16 [F1], M17, M20 Core & M20-B Iron Mode**). |
| 📘 [`docs/future_milestones/CONOCIMIENTO_TRIBAL.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/future_milestones/CONOCIMIENTO_TRIBAL.md) | **Tribal Knowledge & Inference Physics:** Causal architecture, LLM streaming physics, 2D Governance FSM matrix, hardware viewport ergonomics (14" 150% zoom & Split 50%), KaTeX lessons, and 4-Archetype invariants. |
| 🏁 [`docs/future_milestones/HANDOFF_M20_CLOSURE.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/future_milestones/HANDOFF_M20_CLOSURE.md) | **Milestone 20 Closure Report:** Certification handoff for the 6 Higher-Order Bloom Modalities, Iron Mode, and $k=2$ production standard. |
| 📋 [`docs/PROJECT.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/PROJECT.md) | **Core Project Specification:** Foundation contracts, schema interfaces, and baseline subsystem definitions. |
| 🧪 [`docs/TEST_INFRA.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/TEST_INFRA.md) & [`docs/TEST_READY.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/TEST_READY.md) | **Test Infrastructure & Readiness Specs:** E2E Playwright harness design and verification checklists. |
| 📐 [`docs/specs/`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/) | **Deep Technical Specifications:** Detailed specs for Study Harness ([`m06_study_harness.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/m06_study_harness.md)), FSRS-5/6 SRS ([`m08_srs_fsrs_fluency.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/m08_srs_fsrs_fluency.md)), Hierarchical ContentCore ([`m09_hierarchical_content_khanmigo.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/m09_hierarchical_content_khanmigo.md)), Mastery 2.0 ([`m14_khan_mastery_engine.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/m14_khan_mastery_engine.md)), Formal Kernel ([`m15_m18_formal_lean4.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/m15_m18_formal_lean4.md)), and 4-Axis Archetypes ([`sintesis_plantillas_arquetipos.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/sintesis_plantillas_arquetipos.md)). |

---

## System Architecture (v4.0 Neuro-Symbolic & Study Harness)

```
                            +-----------------------------------------------+
                            |            Academic Course Materials          |
                            |  (PDFs, Beamer Decks, Handwritten Notes, Ink) |
                            +-----------------------+-----------------------+
                                                    |
                                                    v
+---------------------------------------------------------------------------------------------------+
| Subsystem 1: Content-to-Course Pipeline v4.0 (.agents/skills/content-to-course/)                  |
|                                                                                                   |
|  Stage 0: Multimodal Ingest    -->  Stage 1: CTA Map-Reduce      -->  Stage 2: Weighted Sharding  |
|  (PyMuPDF session slicing,          (Sectional Analyzers +            (1:1 heavy / 2:1 light,     |
|   direct PDF reading, evidence)      DAG Harmonizer, PRE-XX,           Typed Contract Skeletons,  |
|                                      explicit assumptions)             k=2 stable default)        |
|                                                                                |                  |
|  Stage 6: Quality Gate Publish <--  Stage 5: Bicameral Judges    <--  Stage 3 & 4: Form-C & Build |
|  (MPRI /100 pts, 7 Path-to-         (Alpha_Kernel = 0 dominance,      (4 Orthogonal Archetypes,   |
|   Mastery linters, atomic sync)      LQAS fast-path, .rejudge ckpt)    KaTeXAST, c2c_ver, SymPy/Z3|
|                                                                        SHA-256 certs, Pool <8.5s) |
+---------------------------------------------------+-----------------------------------------------+
                                                    | Outputs certified course JSON
                                                    v
+---------------------------------------------------------------------------------------------------+
| Subsystem 2: Format, Psychometric & Epistemic Validator (src/validator/ & engine/)                |
|                                                                                                   |
|  Pass 1: Lexical & Overescape  -->  Pass 2: Schema & Epistemic   -->  Pass 3: Psychometric & MPRI |
|  - RFC 8259 raw syntax              - Draft-07 Schema & Pydantic      - 23 Rules + 3 Strict Rules |
|  - Silent LaTeX escapes             - Epistemic Closure gate          - Anti-giveaway [0.8, 1.2]  |
|  - Anti-Overescape Guard (R-23)       [TPL-EPISTEMIC-CLOSURE]         - Active Recall Quota >=80% |
|    auto-repair in run_platform      - 0 MC7 in Skill, <=1 in Concept  - KaTeXAST & PyKaTeX column |
+---------------------------------------------------+-----------------------------------------------+
                                                    | Verified courses served from courses/
                                                    v
+---------------------------------------------------------------------------------------------------+
| Subsystem 3: Top's Academy Study Harness & PWA Platform (platform/ & run_platform.py)             |
|                                                                                                   |
|  - Slim Manifest & ETag Server: 2.52 KB manifest, mtime+size cache, ETag/304/gzip, /healthz       |
|  - Offline-First PWA & Resilience: Workbox Service Worker, IndexedDB course cache, sessionStore   |
|    auto-rehydration on laptop sleep/wake, and native mobile popstate navigation                   |
|  - Ergonomic Viewport Engine: 12-viewport E2E matrix (14" 150% zoom, Split-View 50%, mobile)      |
|  - Antigravity Study Harness 2.0: Smart Blank-First curtain (free recall), 100% mouseless hotkeys,|
|    4-Strikes adaptive Socratic gate, and 1-click $0 API Socratic prompt transfer                  |
|  - 6 Higher-Order Bloom Modalities: open_symbolic (mathjs AST), proof_dag, adversarial_break,     |
|    unstructured_model, invariant_canvas (Cartesian & Tree SVG), and concept_matching              |
|  - Mastery 2.0 & FSRS-5/6 Engine: Bidirectional calibration, 80/20 hybrid bar, ts-fsrs scheduler, |
|    12h Mastery Challenge cooldown, Misconception Ledger ("Practicar mis Trampas"), ProgressLogView|
|  - Iron Mode (20-B) & SAT Bluebook Simulator (14-B): Closed-book timed exam, 2-module adaptive    |
|    routing (Module 1 diagnostic -> Module 2 Standard/Advanced), mandatory MetacognitiveModal      |
|    (confidence + Brier Score / Log-Loss calibration), and 0-20 university grade projection        |
+---------------------------------------------------+-----------------------------------------------+
                                                    | Telemetry & QA Evaluation
                                                    v
+---------------------------------------------------------------------------------------------------+
| Subsystem 4: Multi-Agent Governance, Telemetry & QA Skills (.agents/skills/)                      |
|                                                                                                   |
|  - c2c_hook_guard.py (2D FSM): Blocks global rewrites on <6 errors, enforces surgical edits       |
|  - course-qa-evaluator: QM, OSCQR & Mastery Learning audit + 7 Path-to-Mastery v2.0 linters       |
|  - c2c-run-auditor & c2c-unified-auditor: Per-turn token telemetry, cache multiplier & QA fusion  |
|  - flash-duet-orchestrator, prompt-architect & delete-course (<300ms safe lifecycle management)   |
+---------------------------------------------------------------------------------------------------+
```

---

## Single Command Launcher

Launch the complete application (both the backend course discovery server with anti-overescape KaTeX guards and the web interface) with a single command:

```bash
python run_platform.py
```

### Options and Flags

```bash
# Start server on custom port or host
python run_platform.py --port 5173 --host 127.0.0.1

# Course Discovery & Inspection Mode (non-server scan with validation summary)
python run_platform.py --scan

# Help & Usage
python run_platform.py --help
```

Open your web browser to: **[http://localhost:5173](http://localhost:5173)**

---

## Practice Platform & Antigravity Study Harness Features

### 1. Ergonomics Across 12 Viewports, Split-View 50% & Installable Offline PWA (M1, M1-T, M2, M2a, M11, M12)
- **Container-Query 2-Column Grid (`@container qc (min-width: 480px)`)**: Eliminates vertical overflow on compact 14" laptops at 150% OS scaling and **50% Split-View** windows alongside PDF readers or notes.
- **Prose-Outside-KaTeX Splitting (`splitMathAndProse`)**: Keeps mathematical formulas crisp (`white-space: nowrap`) while wrapping surrounding Spanish prose cleanly.
- **Installable Offline PWA**: Workbox Service Worker precaching the App Shell and KaTeX `.woff2` fonts (~1.5 MB), storing large course banks in IndexedDB (`tops_academy_cache`), with native mobile back-gesture support (`navigationHistory.ts`) and an `✓ Offline` status badge.
- **Laptop Sleep/Wake Resilience (`sessionStore.ts`)**: Persists active practice state in `sessionStorage` (`tops_active_session_v1`) and silently reconciles server `ETag` headers on `visibilitychange` without losing student progress.
- **Slim Manifest Architecture**: Compresses initial catalog discovery from `59.8 MB` down to a `2.52 KB` slim manifest (`0.76 KB` gzip) backed by `.cache/course_index.json`.

### 2. Antigravity Study Harness 2.0 & $0 API Socratic Transfer (M6)
- **Smart Blank-First Curtain**: Hides options on question load to enforce pure **Free Recall** before recognition (`Enter` to reveal options; automatically bypassed for direct active-input items).
- **100% Mouseless Navigation**: Full keyboard control via `A`–`G` / `1`–`7` option toggles, auto-focused inputs, and `Enter` submission.
- **4-Strikes Adaptive Socratic Gate**: Allows up to 4 attempts (`4/4`), triggering a Socratic intervention gate on repeated failures and providing a **1-click anti-giveaway prompt generator** (`$0 API cost`) to paste into any external LLM tutor without leaking the answer key.

### 3. Khan-Style Mastery 2.0, FSRS-5/6 Spaced Repetition & Misconception Ledger (M8, M9, M14)
- **Bidirectional Mastery Calibration**: Dynamic transitions across *Sin empezar* $\leftrightarrow$ *Practicado* $\leftrightarrow$ *Familiar* $\leftrightarrow$ *Dominado* (`100 pts`), with **80/20 Hybrid Course Progress** (80% mastery points + 20% competency coverage), *Hint-Cap* penalties, and a 5-tier **"Up Next for You"** recommendation engine.
- **Client-Side `FSRS-5/6` (`ts-fsrs`) Scheduler**: Maps objective telemetry (`wrong_attempts`, `hints_used`, partial credit, `lucky_guess`) to FSRS ratings without penalizing deep-thinking latency. Includes a **12-hour per-competency cooldown** in *Mastery Challenge* (6 items) and separates `review_reason: 'error' | 'decay'`.
- **Misconception Ledger (`D-XX-YY`)**: Tracks specific structural distractors and error families across all modalities, enabling targeted **"Practicar mis Trampas"** remediation sessions and an SVG **ProgressLogView** tracking Brier Score and Log-Loss calibration.
- **Hierarchical `ContentCoreDrawer` & Unit 0 (`PRE-XX`)**: Organizes competencies by source lecture decks/modules in pedagogical order, displaying 5-block Khanmigo study guides, explicit mathematical assumptions (`assumptions` + `violation_consequence`), and prerequisite foundation units (`PRE-XX`).

### 4. Iron Mode (M20-B) & SAT Bluebook 2-Module Adaptive Exam Simulator (M14-B)
- **Closed-Book Timed Examination (`IronExamSession.tsx`)**: Simulates high-stakes university exams with countdown timers (visual alerts at $\le 5\text{ min}$ and $\le 1\text{ min}$), zero hint access, and deferred feedback until final submission.
- **SAT Bluebook 2-Module Adaptive Routing**: Module 1 serves a 12-question diagnostic baseline; achieving $\ge 70\%$ routes the student to **Module 2 Advanced**, while $< 70\%$ routes to **Module 2 Standard** without item repetition.
- **Mandatory Metacognitive Calibration (`MetacognitiveModal.tsx`)**: Before revealing grades, students rate their confidence ($0$–$100\%$) to compute real-time **Brier Scores** and **0–20 Peruvian University Grade Projections** broken down by unit.

---

## 4-Axis Authoring Architecture & 6 Higher-Order Bloom Modalities (M20)

To eradicate syntactic overfitting and passive option elimination, Milestone 20 enforces a **4-Axis Competency Contract** across every shard:
1. **Axis 1 — 4 Orthogonal Archetypes**: `direct` (frontal calculation), `inverse` (parameter recovery/diagnosis), `perturbation` (comparative statics/shock analysis), and `boundary_or_edge_case` (asymptotics/degenerate limits).
2. **Axis 2 — Anti-Elimination Quota (`[M20-MC7-CAP]` & `[M20-ACTIVE-QUOTA]`)**: **`0 MC7` (7-option multiple choice) is strictly forbidden in `Skill` (`Hab-*`) competencies** and capped at $\le 1$ in `Concept`/`Fact`, enforcing **$\ge 80\%$ active production/discrimination modalities**.
3. **Axis 3 — ZPD Difficulty Tri-Band**: Balanced distribution across `easy`, `medium`, and `hard` templates with mandatory diagnostic rationales (`ds` / `D-XX-YY`) even on free-input items (`TPL-D3`).
4. **Axis 4 — Higher-Order Bloom Taxonomy ($\ge \text{L3–L6}$)**: Powered by 6 specialized interactive modalities evaluated client-side with zero `eval()`:

| Modality | Cognitive Task (Bloom Level) | Engine & Verification Mechanism |
| :--- | :--- | :--- |
| **`open_symbolic`** | **L3–L5 Symbolic Derivation:** Free-form algebraic/calculus formula entry | Client-side `mathjs` AST equivalence + 81-case adversarial normalizer + server `[TPL-EPISTEMIC-CLOSURE]` hard gate |
| **`proof_dag`** | **L4–L5 Deductive Proof Assembly:** Reconstruct multi-step mathematical proofs (`steps >= 3`) | Compiled via `engine/proof_compiler.py` with topological dependency validation and trap step rationales |
| **`adversarial_break`** | **L5–L6 Counterexample & Assumption Auditing:** Identify the violated theorem hypothesis or breaking witness | Compiled via `engine/adversarial_generator.py` with `[ADV-WITNESS-LEAK]` Shift-Left guard |
| **`unstructured_model`** | **L4–L6 Stage-0 Formalization:** Translate a raw word problem into formal variables, objective functions, and constraints | Multi-part structured schema validated via `c2c_ver.m20_guard` |
| **`invariant_canvas`** | **L4–L5 Visual/Topological Reasoning:** Interactive Cartesian curves/equilibria or decision/game trees | Dual `cartesian` & `tree` SVG renderer with `[CANVAS-OUT-OF-BOUNDS]` viewport clipping linter |
| **`concept_matching`** | **L3–L4 Structural Isomorphism:** Map formal properties/theorems to their mathematical consequences | Bijective/surjective pairing matrix with specific misconception rationales (`D-XX-YY`) |

*Note: Standard `fill_in_the_blank` (`FIB` with diagnostic `ds` rationales) and `multiple_select` (`MS` 4–6 options) complement the 6 higher-order modalities.*

---

## Course Bank Format, KaTeXAST & Validator CLI (23 Rules + 3 Strict + MPRI)

Course banks are validated through a 3-pass deterministic validator (`src/validator/`) and a 7-linter **Mastery Pedagogical Rigor Index (MPRI / 100 pts)** pre-publish quality gate:

### Validator Rules Matrix

| Rule ID | Code | Category | Specification / Invariant Enforced |
| :--- | :--- | :--- | :--- |
| **R-01..R-03** | `ERR_RAW_NEWLINE` / `ESCAPE` | Lexical | RFC 8259 conformity; zero raw newlines or silent control characters (`\tau`, `\frac`, `\beta`, `\nu`, `\text`) |
| **R-04..R-07** | `ERR_SCHEMA` / `INTEGRITY` | Schema & DAG | Draft-07 JSON Schema, Pydantic `ShardCompetenceContract`, unique IDs, valid foreign keys, acyclic `PRE-XX` / `C-XX` DAG |
| **R-08..R-09** | `ERR_COUNT_SKILL` / `CONCEPT`| Volume Quota | Volume quotas per competency scaled by `k` (`DEFAULT_TEMPLATES_PER_MODALITY = 2` stable standard) |
| **R-10..R-13** | `ERR_MC` / `ERR_MS_COUNT` | Cardinality | Cardinality invariants + `[M20-MC7-CAP]` (`0 MC7` in `Skill`, $\le 1$ in `Concept`/`Fact`) & `[M20-ACTIVE-QUOTA]` ($\ge 80\%$) |
| **R-14** | `ERR_HINT_COUNT` | Scaffolding | Graduated Socratic hints count between 3 and 5 |
| **R-15..R-16** | `ERR_LENGTH_RATIO` / `DIST` | Psychometrics | Anti-giveaway bounds: $0.80 \cdot \min(D) \le L_{\text{correct}} \le 1.20 \cdot \max(D)$; longest/shortest $\le 25\%$ |
| **R-17..R-19** | `ERR_RATIONALE` / `LEAK` | Quality | Zero placeholder rationales, zero meta-giveaway words in options, zero answer leaks in stems |
| **R-20** | `ERR_LATEX_SYNTAX` | `KaTeXAST` | Recursive `KaTeXAST` parser + `pykatex_validate_with_column`, PrairieLearn `@var@` raw strings, `[SYMPY-LATEX-MATRIX]` |
| **R-22** | `ERR_MS_MISSING_RATIONALE` | Diagnostics | Mandatory diagnostic error rationale (`D-XX-YY`) in all distractors and `TPL-D3` free-input `ds` maps |
| **R-23** | `ERR_KATEX_OVERESCAPE` | Admission Guard| Platform anti-overescape guard (`\\frac`, `\\alpha` in JSON) with idempotent auto-repair in `run_platform.py` |
| **S-01..S-03** | `ERR_STRICT_*` | Strict Mode | Mandatory step-by-step `detailed_solution`, `misconception_warning`, and explicit `difficulty` (`easy`, `medium`, `hard`) |

### Validator CLI Usage

```bash
# Validate a single course file in strict pedagogical mode
python -m src.validator.cli courses/estadistica_3_pre_pc2_m20.json --strict

# Machine-readable JSON output for CI/CD pipelines
python -m src.validator.cli courses/mateco_4_optimizacion_v20_k_3.json --strict --json

# Validate entire directory of course files
python -m src.validator.cli courses/
```

---

## Content-to-Course Antigravity Skill Ecosystem (7 Skills)

Located under `.agents/skills/`, seven specialized skills power the autonomous authoring, formal verification, and auditing lifecycle:

1. **`content-to-course` (v4.0 "More with Less" Neuro-Symbolic Pipeline)**:
   - **Stage 0 & 1 (`ingest.py`, `cta_merge.py`)**: Multimodal PDF slicing + CTA Map-Reduce extracting acyclic prerequisite DAGs, `PRE-XX` foundation units, explicit `assumptions`, and ordered `evidence` blocks.
   - **Stage 2 (`plan_shards.py`)**: Weighted competency sharding (`is_heavy_competency` `1:1` for heavy `Skill` shards, `2:1` for `Concept`/`Fact`, `max_concurrency=12`) with zero prompt duplication (`-2.0M` tokens saved).
   - **Stage 3 (`compile_shard.py`, `check_templates.py`, `engine/c2c_ver.py`)**: Shift-Left compilation in `<50 ms` precheck using the `Form-C` DSL (55–70 lines), **6 First-Time Pass (FTP) Levers** (pre-wired Typed Contract Skeletons in `author_XX_data.md`, `c2c_ver.numeric/equiv/m20_guard` proxy, `[AUTO-FIXED] [TPL-ORPHAN-VARS]`, `normalize_prose_outside_math`, `[Z3-RULE-WARNING]` shadow solver, and `[TPL-EPISTEMIC-CLOSURE]` gate), emitting SHA-256 cryptographic receipts (`shard_XX.cert.json`).
   - **Stage 4 (`engine/instantiate.py`, `build_worker.py`)**: Parallel `ProcessPoolExecutor` + `orjson` instantiation with stratified **Rejection Sampling** ($\le 20\%$ key concentration), assembling full courses in **$< 8.5\text{ seconds}$**.
   - **Stage 5 (`judge.py`)**: Bicameral Blind Judges with absolute formal kernel dominance ($\alpha_{\text{Kernel}} = 0$), **LQAS statistical fast-path** (skipping LLM re-judging on clean deterministic passes), and `.rejudge_pending.json` crash-recovery checkpoints.
   - **Stage 6 (`course_publisher.py`)**: Enforces the blocking `PublishQualityGateError` (MPRI + 7 Path-to-Mastery v2.0 linters) before atomic publication to `courses/`.
   - **2D FSM Hook Guard (`c2c_hook_guard.py`)**: Intercepts subagent tool calls (`read_file`/`write_file`/`edit_file`), blocking full-file rewrites when errors $< 6$ to enforce surgical edits and cap subagents at 40 turns / 5M tokens.
2. **`course-qa-evaluator`**: Hybrid deterministic (`<300 ms`) + adaptive semantic QA auditor scoring courses `/20.0 pts` (QM/OSCQR) and `/100 pts` (MPRI across 6 pillars).
3. **`c2c-run-auditor`**: Forensic multi-agent telemetry extractor measuring input, output, cache-read multipliers (`1.0x` vs `7.6x` on retries), thinking tokens, critical path stragglers, and USD unit economics.
4. **`c2c-unified-auditor`**: Dispatches `c2c-run-auditor` and `course-qa-evaluator` concurrently to produce unified benchmark reports in `docs/unified_reports/` and `reports/`.
5. **`delete-course`**: Safely purges courses and working artifacts in `<300 ms` while stamping historical QA audit reports as `ELIMINADO` and preserving `content/` immutability.
6. **`flash-duet-orchestrator`**: Sequential gate orchestrator (`Implementer -> Auditor` in Duet mode, or `Implementer -> Editor -> Auditor` in Triad mode) with strictly disjoint write boundaries and pre-flight verification.
7. **`prompt-architect`**: Frontier prompt engineering and blind auditing skill built on modular XML contracts and official DeepMind / AI Studio guidelines.

---

## Automated Test Matrix (4 Isolated Domains + E2E)

Consolidated under Milestone 13 into **4 isolated domain directories** (`tests/{quality,engine,platform,pipeline}/` + `tests/e2e/`) running via `pytest-xdist` (`-n auto --dist worksteal`):

```powershell
# Run the full parallelized Python test suite (1,526+ tests across 4 domains)
pytest tests/ -q

# Run specific domain suites
pytest tests/engine/ tests/quality/ -q
pytest tests/platform/ tests/pipeline/ -q

# Run Node.js 81-case Math Equivalence & M20 Validators suites
node tests/platform/test_math_adversarial_suite.mjs
node tests/test_m20_validators.mjs

# Run 12-Viewport Ergonomics Matrix & Playwright E2E Browser Suites
node tests/e2e_m1_viewport_matrix.mjs
pytest tests/e2e/ -v
```

- **`tests/engine/`**: `KaTeXAST` parser, `Form-C` compiler, `c2c_ver` symbolic/numeric verification, `[TPL-EPISTEMIC-CLOSURE]` gate, AST sandbox security, and `z3-solver` shadow checks.
- **`tests/quality/`**: 23 format rules + 3 strict rules, 7 Path-to-Mastery v2.0 linters, MPRI scoring, 4-Archetype semantic gates, and anti-giveaway psychometrics.
- **`tests/platform/`**: Slim manifest & ETag server, KaTeX anti-overescape admission guard (`R-23`), FSRS-5/6 scheduler & 12h cooldown, Misconception Ledger, Bidirectional Mastery 80/20, SAT Bluebook 2-Module adaptive exam (`M14-B`), laptop sleep resilience (`M12`), and PWA offline caching.
- **`tests/pipeline/`**: 2D FSM `c2c_hook_guard.py` + Hypothesis DRT property tests (`M15`), Prompt-Compiler CI gate (`test_system_prompts_compile_clean.py`), CTA Map-Reduce & `PRE-XX` hierarchy (`M9`), weighted sharding, and safe course deletion.
- **`tests/e2e/`**: Headless Playwright browser verification for the 6 Higher-Order Bloom Modalities (`test_m20_bloom_modalities.py`), Iron Mode & Metacognitive Modal (`test_platform_assessments.py`), and 12-viewport container-query ergonomics.

---

## Active Production Courses & Benchmark Telemetry

Currently discovered and validated in `courses/` (`python run_platform.py --scan`):

| Course Identifier | Title | Questions | Competencies | Milestone Standard | Status |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`estadistica_3_pre_pc2_m20`** | Estadística III: Pre-PC2 (Inferencia, Asintótica y Regresión) | **1,396** | **58** | **M20 Bloom Superior (`k=2`)** | **VALID / Active** |
| **`mateco_4_optimizacion_v20_k_3`** | Matemática para Economistas IV: Optimización Dinámica y Estática | **963** | **27** | **M20 Platinum Pilot (`k=3`, 19.92/20, MPRI 99.65)** | **VALID / Active** |
| **`solow_m20_v11`** | Modelo de Crecimiento de Solow-Swan (Serie Experimental FTP) | **621** | **20** | **M19/M20 FTP Benchmark (`k=3`)** | **VALID / Active** |
| **`solow_m20_v5` .. `solow_m20_v10`** | Serie Experimental Solow M20 (Calibración de Palancas FTP `v5`–`v10`) | **402 – 597** | **17 – 20** | **M19/M20 Telemetry Series (`k=2..3`)** | **VALID / Active** |

- **Benchmark Highlights (`docs/future_milestones/FUTURE_MILESTONES.md`)**:
  - **Quality Peak (`mateco_4_optimizacion_v20_k_3`)**: **19.92 / 20.0 QM/OSCQR (`PLATINUM MASTERY`)**, **MPRI 99.65 / 100**, `risk_score = 0.05`, average Bloom level **3.931 (`Tier ÉLITE`)** across 963 items.
  - **Throughput & First-Time Pass Record (`solow_m20_v13` / `v12` with M19 6 FTP Levers)**: Stage 3 First-Time Pass elevated from `0–9.5%` to **`30.0–38.5%`**, generating **621 higher-order items in `12.85 min` (`1.24 s/question`, `5.46x` parallel speedup)** using **`8.61M` gross tokens (`USD 8.13`, `-48.1%` token reduction)**.

---

## Certified Milestones Registry (M1 – M20-B)

Full forensic logs and commit hashes are documented in [`docs/future_milestones/MILESTONES_COMPLETED.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/future_milestones/MILESTONES_COMPLETED.md):

| Milestone | Delivered Scope | Certification & Verification Evidence |
| :--- | :--- | :--- |
| **M1 & M1-T** | **Web Ergonomics (14" 150% Zoom, Split-View 50%, 12-Viewport Matrix)** | Container queries, off-canvas drawer, `splitMathAndProse`, `tests/e2e_m1_viewport_matrix.mjs` (12/12 PASS) & 97 static contracts |
| **M2 & M2a** | **Installable Offline PWA & Mobile Usability** | Workbox SW, IndexedDB course cache, adaptive icons, native mobile `popstate` (`navigationHistory.ts`), `test_pwa_offline.py` (12/12 PASS) |
| **M3** | **Anti-Overfitting & Tri-Band Archetype Variety (v3.8)** | `--min-archetypes 3`, 3 ZPD bands, $\ge 2$ Bloom levels, `[STEM-DIVERSITY-GATE]`, `ArchetypeEntropyLinter` |
| **M4** | **Form-C DSL, KaTeXAST Grammar & Pydantic Contracts (100%)** | `KaTeXAST` recursive compiler, `sympy_to_katex`, 55–70 line `Form-C` DSL with AST auto-export, PrairieLearn `@var@`, `test_milestone4_formc_katex_ast.py` (23/23 PASS) |
| **M6** | **Antigravity Study Harness 2.0 (Blank-First & $0 API Socratic)** | Smart Blank-First free-recall curtain, 100% mouseless hotkeys (`A`–`G`/`1`–`7`), 4-strikes adaptive Socratic gate & 1-click prompt generator |
| **M7** | **Pipeline v4.0 "More with Less" (`< 15 min` & `-65%` Tokens)** | `-2.0M` token deduplication in `dispatch.py`, SHA-256 `shard_XX.cert.json` receipts, `--lean` subagents, `<50 ms` AST precheck |
| **M8** | **FSRS-5/6 Spaced Repetition, 12h Cooldown & Misconception Ledger** | `ts-fsrs` (`^6.0.0`) client scheduler, 12h per-skill cooldown, `D-XX-YY` Misconception Ledger ("Practicar mis Trampas"), SVG `ProgressLogView` (Brier Score) |
| **M9 (Quick Wins + Phase A)** | **PPT Hierarchy, Unit 0 `PRE-XX`, `ContentCoreDrawer` & Ordered Modules** | `PRE-XX` prerequisite extraction, 5-block Khanmigo `ContentCoreDrawer.tsx`, contiguous source-order `hierarchyAdapter.ts` (`modulesPreserveOrder`) |
| **M10** | **QA Rubric v2.0 Deep Mastery (MPRI & 7 Linters)** | 7 Path-to-Mastery v2.0 linters, MPRI (/100 pts), blocking pre-publish `PublishQualityGateError` with AST line mapping |
| **M11** | **Fast Course Loading Core (Slim Manifest, ETag & Prefetch)** | `59.8 MB` $\to$ `2.52 KB` slim manifest (`0.76 KB` gzip), `.cache/course_index.json`, `ETag` / `304 Not Modified` |
| **M12** | **Laptop Sleep/Wake Session Resilience (`sessionStore.ts`)** | `sessionStorage` active hydration, silent `ETag` reconciliation on `visibilitychange`, `GET /healthz`, `test_m12_session_resilience.py` (14/14 PASS) |
| **M13** | **Repository Consolidation & 4 Isolated Test Domains** | `tests/{quality,engine,platform,pipeline}/`, clean artifact policies, hardened `.gitignore`, 1,526+ tests passing |
| **M14 & M14-B** | **Khan Mastery 2.0 (80/20 Hybrid) & SAT Bluebook 2-Module Simulator** | Bidirectional calibration, 80/20 bar, Hint-Cap, 5-tier "Up Next", and 2-module adaptive exam (M1 diagnostic $\to$ M2 Advanced/Standard + 0–20 grade projection) |
| **M15 (F1 + DRT)** | **Formal Multi-Agent Governance FSM & Hypothesis DRT** | 2D `decidirEstrategiaEdicion` in `c2c_hook_guard.py` (blocks global rewrites on $<6$ errors), 40-turn/5M-token hard cap, Hypothesis DRT property suite |
| **M16 (F1)** | **Shift-Left Mathematical Certification & 4 Orthogonal Archetypes** | `Stage Contract v4.0`, 4 mandatory archetypes (`direct`, `inverse`, `perturbation`, `boundary_or_edge_case`), explicit `assumptions`, `[DIAG-MAGIC-MULT]` |
| **M17** | **Curricular DAG, Epistemic Closure & Bicameral Arbitration ($\alpha_{\text{Kernel}}=0$)** | Acyclic connected DAG & epistemic monotonicity ($K_t \subseteq K_{t+1}$), $\alpha_{\text{Kernel}}=0$ judge dominance, `[TPL-EPISTEMIC-CLOSURE]` hard gate on `open_symbolic` (`0/497` false positives) |
| **M20 (Core + 20-B Iron Mode)** | **6 Higher-Order Bloom Modalities, `TPL-D3`, `0 MC7` in Skill & Iron Mode** | `open_symbolic`, `proof_dag`, `adversarial_break`, `unstructured_model`, `invariant_canvas`, `concept_matching`; `[M20-MC7-CAP]`, `[M20-ACTIVE-QUOTA]` ($\ge 80\%$); `IronExamSession.tsx` + `MetacognitiveModal.tsx`; `k=2` stable production standard |

---

## Active Engineering Roadmap (`FUTURE_MILESTONES.md`)

Current engineering priorities tracked in [`docs/future_milestones/FUTURE_MILESTONES.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/future_milestones/FUTURE_MILESTONES.md):

| Priority | Milestone | Target Objective & Current Status | Spec Reference |
| :---: | :--- | :--- | :--- |
| 🧬 **P0** | **Milestone 19: Sustainable Scaling to $k=4$ (`1,284+` Items), *First-Pass* Architecture ($\ge 75\%$ FTP) & Google AI Pro Quota Protection** | **6 FTP Levers ✅ Implemented in code (2026-11-22)** (`c2c_ver`, Typed Contract Skeletons, Rejection Sampling, `[TPL-ORPHAN-VARS]`/`[PROSE-NORM]` auto-healing, `1:1`/`2:1` weighted sharding, `.rejudge_pending.json`), raising Stage 3 FTP to `30.0–38.5%`. Remaining: converge `Skill` FTP to $\ge 75\%$ and certify full $k=4$ run (`<= 11.55M` gross tokens, `< 10 min`). | [`sintesis_plantillas_arquetipos.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/sintesis_plantillas_arquetipos.md) |
| 📐 **P1** | **Milestone 16 (Phase 2): Automated Algebraic Deduction with `z3-solver` (Python)** | **Phase 1 ✅ active in shadow mode (`[Z3-RULE-WARNING]` in `shard_ast_transforms.py`, `150 ms` timeout, `0` false positives across `805` templates)**. Remaining (~1 d): Phase 2 bounded AST verification in `check_templates.py` for `TPL-D4`. | [`m15_m18_formal_lean4.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/m15_m18_formal_lean4.md) |
| 🏛️ **P1** | **Milestone 9 (Merged with M21): Native LLM Ordered `modules[]`, Subtopic Quizzes & PPT Challenge** | Quick Wins + Phase A (`modulesPreserveOrder`) ✅ closed. Remaining (~0.5–1 d): Phase B native LLM emission of ordered `modules[]` validated at publish, slide/note deduplication, Subtopic Quizzes (3–5 items), and PPT Challenge (8–12 items). | [`m09_hierarchical_content_khanmigo.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/m09_hierarchical_content_khanmigo.md) |
| 🔒 **P1** | **Milestone 18: Continuous Certification Harness (Prompt-Compiler CI + SLA)** | CI gate `test_system_prompts_compile_clean.py` ✅ active (verifying M20 micro-examples + `ast.parse` on `lean/` prompts). Remaining (~0.5 d): automated SLA regression benchmark gate. | [`m15_m18_formal_lean4.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/m15_m18_formal_lean4.md) |
| 🛡️ **P3** | **Milestone 15 (Phase 2): Native Perceus C Lean 4 FFI Kernel** | Python Hypothesis DRT (`test_c2c_hook_guard_drt.py`) ✅ closed. Native Lean 4 FFI binary (`<0.5 ms`) deferred to P3 research. | [`m15_m18_formal_lean4.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/m15_m18_formal_lean4.md) |

---

## Repository Structure

```text
Tops_academy/
├── README.md                                # Authoritative project documentation (this file)
├── LICENSE                                  # MIT License (Copyright (c) 2026 Augusto Huerta)
├── pyproject.toml                           # Python packaging, dependencies & pytest-xdist config
├── run_platform.py                          # Single-command launcher & R-23 KaTeX admission guard
├── docs/                                    # Centralized documentation ecosystem
│   ├── PROJECT.md                           # Foundational project & interface specification
│   ├── TEST_INFRA.md                        # E2E & validator test infrastructure architecture
│   ├── TEST_READY.md                        # Verification readiness checklist
│   ├── future_milestones/                   # Active roadmap, historical ledger & tribal knowledge
│   │   ├── FUTURE_MILESTONES.md             # Master strategic roadmap (M19, M16 F2, M9+M21, M18)
│   │   ├── MILESTONES_COMPLETED.md          # Forensic ledger of certified milestones (M1..M20-B)
│   │   ├── CONOCIMIENTO_TRIBAL.md           # Inference physics, causal architecture & governance
│   │   └── HANDOFF_M20_CLOSURE.md           # Milestone 20 & Iron Mode certification handoff
│   ├── specs/                               # Deep technical specifications (M6, M8, M9, M14, M15-20)
│   ├── investigaciones/                     # Foundational studies (KaTeX decoupling, cognitive limits)
│   ├── qa_reports/ & run_reports/           # Standardized QA and execution telemetry summaries
│   └── unified_reports/                     # Consolidated pedagogical + telemetry audit reports
├── courses/                                 # Active published course banks (.json) & CTA analyses (.md)
│   ├── estadistica_3_pre_pc2_m20.json       # 1,396 questions, 58 competencies (M20 Bloom Superior)
│   ├── mateco_4_optimizacion_v20_k_3.json   # 963 questions, 27 competencies (19.92/20 Platinum)
│   ├── solow_m20_v5.json .. v11.json        # Solow-Swan M19/M20 FTP experimental benchmark series
│   └── fixtures/                            # Canonical test course fixtures
├── content/                                 # Immutable academic source PDFs (gitignored zero-bloat)
├── platform/                                # Subsystem 3: React 18 + Vite + TypeScript + PWA Platform
│   ├── server/                              # Slim manifest indexer (courseIndex.cjs) & REST server
│   ├── src/
│   │   ├── components/                      # QuestionCard, PracticeSession, IronExamSession,
│   │   │                                    # MetacognitiveModal, ContentCoreDrawer, ProgressLogView
│   │   ├── utils/                           # mathEquivalence.ts, masteryStorage.ts (FSRS-5/6),
│   │   │                                    # hierarchyAdapter.ts, ironExamGrading.ts, sessionStore.ts
│   │   └── App.tsx                          # Platform router, Blank-First & Mastery 2.0 controller
│   └── dist/                                # Compiled production PWA bundle
├── src/validator/                           # Subsystem 2: Format, Lexical, KaTeXAST & Psychometric CLI
├── .agents/skills/                          # Subsystem 1 & 4: 7 Specialized Antigravity Skills
│   ├── content-to-course/                   # v4.0 C2C pipeline (engine/, compile_shard.py, judge.py,
│   │                                        # c2c_hook_guard.py, proof_compiler.py, c2c_ver.py)
│   ├── course-qa-evaluator/                 # QM, OSCQR & MPRI (7 Path-to-Mastery v2.0 linters)
│   ├── c2c-run-auditor/                     # Forensic token, cache & latency telemetry auditor
│   ├── c2c-unified-auditor/                 # Concurrent QA + Run telemetry orchestrator
│   ├── delete-course/                       # Fast (<300ms) safe course lifecycle deletion
│   ├── flash-duet-orchestrator/             # Multi-agent gated Duet/Triad implementation orchestrator
│   └── prompt-architect/                    # Frontier XML prompt architect & blind semantic auditor
├── reports/                                 # Historical telemetry ledger (audit_registry.json) & audits
└── tests/                                   # 4 Isolated Test Domains + E2E Playwright Suite
    ├── engine/                              # KaTeXAST, Form-C, c2c_ver, epistemic closure, sandbox
    ├── quality/                             # 23+3 validator rules, MPRI linters, 4-archetype gates
    ├── platform/                            # Server, R-23 guard, FSRS-5/6, Mastery 2.0, M14-B, PWA
    ├── pipeline/                            # 2D FSM hook guard + DRT, Prompt-Compiler CI, CTA, delete
    └── e2e/                                 # Playwright browser tests (6 Bloom modalities & Iron Mode)
```

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](file:///d:/Augusto/personal_portfolio/Tops_academy/LICENSE) file for details.  
Copyright (c) 2026 **Augusto Huerta**.
