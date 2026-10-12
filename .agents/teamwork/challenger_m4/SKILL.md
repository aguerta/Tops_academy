---
name: content-to-course
description: End-to-end Antigravity skill that ingests academic course PDFs, performs Cognitive Task Analysis (CTA) to extract competencies (Facts [H], Concepts [C], Skills [Hab], expert blindness, automation seeds), generates Top's Academy-style exercise banks (>=30 per Skill, >=20 per Fact/Concept) across all 3 interaction types with psychometric anti-giveaway guarantees and escaped LaTeX, independently verifies answer keys via SymPy and blind solver tiers, auto-repairs validation errors, and publishes valid courses to the practice platform.
triggers:
  - "create course from pdf"
  - "generate Top's Academy course"
  - "analyze competencies"
  - "convert pdf to course"
  - "publish course"
inputs:
  pdf_path:
    type: string
    description: Path to the academic course material PDF (e.g. sample_content/I__Ecuaciones_en_derivadas_parciales_2026.pdf)
    required: true
  output_dir:
    type: string
    description: Directory where the published course JSON and CTA Markdown are stored (defaults to courses/)
    required: false
  course_id:
    type: string
    description: Alphanumeric slug identifier for the course (defaults to sanitized PDF filename)
    required: false
  strict:
    type: boolean
    description: Whether to enforce strict mode validation (solutions, misconception warnings, difficulty levels)
    default: true
outputs:
  course_file:
    type: string
    description: Absolute path to the validated course JSON (courses/<course_id>.json)
  cta_file:
    type: string
    description: Absolute path to the Cognitive Task Analysis document (courses/competence_analysis_<course_id>.md)
---

# Content-to-Course Antigravity Skill

An automated, psychometrically grounded educational engineering pipeline that converts raw academic PDFs into fully playable, interactive Top's Academy courses.

## Pipeline Architecture

```
[ Academic PDF Input ]
         │
         ▼
[ Phase 1: PDF Extractor ]
   - Multi-engine extraction (fitz / PyMuPDF, pdfplumber, pypdf)
   - Multi-line formula stitching & LaTeX normalization
   - Slide & section outline chunking
         │
         ▼
[ Phase 2: CTA Cognitive Task Analysis Engine ]
   - Knowledge Triad decomposition: Facts [H], Concepts [C], Skills [Hab]
   - Expert Blindness identification & common student pitfalls
   - Top's Academy-style Automation Seeds (parametric micro-drills)
   - Outputs: courses/competence_analysis_<course_id>.md
         │
         ▼
[ Phase 3: Batch Exercise Generator ]
   - Chunked batch generation (5-8 items/batch) to avoid token limits
   - Volume quotas: >=30 per Skill [Hab], >=20 per Fact/Concept [H/C]
   - 3 Interaction Types:
       * multiple_choice_7_options (exactly 7 options, 1 correct, randomized A-G)
       * fill_in_the_blank (canonical LaTeX + accepted_equivalents array)
       * multiple_select (4-6 options, 1 to n-1 correct, binary scoring)
   - Psychometric Anti-Giveaway Engine:
       * Per-item length bounding: 0.80 * min(D) <= L_correct <= 1.20 * max(D)
       * Course distribution: L_correct longest in <= 25%, shortest in <= 25%
       * Symmetrical distractor rationales & grammatical parallelism
   - Declarative Coordinate Plane vector graphs (axes, curves, points)
   - Double-backslash escaped LaTeX: valid JSON without control character corruptions
         │
         ▼
[ Phase 4: Independent Verification Tier ]
   - Tier 1: SymPy Programmatic Solver (symbolic math, roots, derivatives, equivalence)
   - Tier 2: Blind Solver (solves stems without answer key or hints)
   - Discordance arbitration and validation
         │
         ▼
[ Phase 5: Automated R2 Validator & Iterative Repair Loop ]
   - Executes Python validator (validate-course --strict)
   - Automated repair modules (max 3 iterations):
       * Regex LaTeX escape & control character sanitizer
       * Option length rebalancer
       * Quota shortfall generator
       * Scaffolding hints normalizer
         │
         ▼
[ Phase 6: Course Publication & Registration ]
   - Saves final JSON to courses/<course_id>.json
   - Practice platform auto-discovers and registers course dynamically
   - Reports summary metrics and launch command
```

## Multi-Agent Workflow Architecture

The skill implements a decoupled dual-agent architecture separating cognitive curriculum decomposition from psychometric question engineering:

```
┌────────────────────────────────────────────────────────┐
│                   ACADEMIC RAW PDFS                    │
│   (Single PDF, Multi-PDF List, or Content Directory)   │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
 ┌─────────────────────────────────────────────────────┐
 │       AGENT 1: CTA Architect (Cognitive Task)       │
 │   System Prompt: prompt_competence_analyser.md      │
 ├─────────────────────────────────────────────────────┤
 │ • Decomposes theory into Knowledge Triad:           │
 │     - Facts [H] (identities, formulas)              │
 │     - Concepts [C] (models, boundary conditions)    │
 │     - Skills [Hab] (observable procedures)          │
 │ • Uncovers Expert Blindness & implicit steps        │
 │ • Generates Top's Academy-style Automation Seeds     │
 │ • Produces structured competence_analysis.md        │
 └──────────────────────────┬──────────────────────────┘
                            │ CTA Taxonomy + Slides
                            ▼
 ┌─────────────────────────────────────────────────────┐
 │      AGENT 2: Exercise Generator (Psychometrics)    │
 │   System Prompt: prompt_creator_exercises.md        │
 ├─────────────────────────────────────────────────────┤
 │ • Synthesizes chunked exercise banks (5-8 / batch)  │
 │ • Strictly balances 3 interaction types:            │
 │     - multiple_choice_7_options (7 options, A-G)    │
 │     - fill_in_the_blank (canonical + equivalents)   │
 │     - multiple_select (4-6 stmts, binary scoring)   │
 │ • Calibrates psychometric anti-giveaway lengths     │
 │ • Generates 3-5 progressive hints & warnings        │
 │ • Escapes LaTeX (\\) cleanly for JSON compliance    │
 └──────────────────────────┬──────────────────────────┘
                            │ Course Bank JSON
                            ▼
 ┌─────────────────────────────────────────────────────┐
 │        INDEPENDENT VERIFICATION & REPAIR TIER       │
 ├─────────────────────────────────────────────────────┤
 │ • Tier 1: SymPy Programmatic Solver                 │
 │ • Tier 2: Decoupled Blind Solver (Zero Key Access)  │
 │ • Iterative Auto-Repair Loop (Max 3 passes)         │
 └──────────────────────────┬──────────────────────────┘
                            │ Validated Course
                            ▼
 ┌─────────────────────────────────────────────────────┐
 │         COURSE PUBLISHER & PLATFORM LAUNCH          │
 │   (--append merges into existing course banks)      │
 └─────────────────────────────────────────────────────┘
```

### Agent Roles & Specifications

#### 1. CTA Architect Subagent
- **Prompt Reference**: `system_prompts/prompt_competence_analyser.md`
- **Objective**: Ingest theoretical lecture slides and reconstruct the latent cognitive curriculum that university examiners require.
- **Decomposition Schema**:
  - **Facts [H]**: Invariant definitions, algebraic identities, fixed formulas that must reside in long-term memory (e.g., `[H-01]` Characteristic equation formula).
  - **Concepts [C]**: Mental models, qualitative classifications, domain boundaries, and conceptual traps (e.g., `[C-01]` Technology-scale vs. marginal returns in Euler's Theorem).
  - **Skills [Hab]**: Observable procedures, analytic decision rules, and calculations (e.g., `[Hab-01]` Computing homogeneity degrees and validating Euler identities).
  - **Expert Blindness**: Matrix of operations professors skip, assumptions left implicit, and student error vectors.
  - **Automation Seeds**: Parametric micro-drills for rapid mental fluency prior to complex problem solving.

#### 2. Exercise Generation Subagent
- **Prompt Reference**: `system_prompts/prompt_creator_exercises.md`
- **Objective**: Transform extracted slides and CTA competence matrices into high-volume, interactive Top's Academy-style exercise batteries.
- **Strict Psychometric Contracts**:
  - **MC7**: Exactly 7 options ($A-G$), exactly 1 correct, 6 homogeneous distractors derived from expert blindness traps. Length calibration bounds correct option length: $0.80 \cdot \min(D) \le L_{\text{correct}} \le 1.20 \cdot \max(D)$.
  - **FIB**: Direct numeric or canonical LaTeX string entry with extensive `accepted_equivalents` array for symbolic representations.
  - **MS**: 4 to 6 independent statements; correct cardinality strictly constrained between $1$ and $n-1$; evaluates domain edge cases and disproves overgeneralizations.
  - **Hints & Scaffolding**: 3 to 5 progressive hints moving from principle $\rightarrow$ setup $\rightarrow$ algebraic crux $\rightarrow$ solution.

## CLI Usage

### Basic Usage (Single PDF)
```bash
python .agents/skills/content-to-course/run.py --pdf sample_content/I__Ecuaciones_en_derivadas_parciales_2026.pdf
```

### Multi-PDF and Directory Ingestion
Ingest multiple PDFs or an entire folder of slides, aggregating sections and competencies:
```bash
# Multiple explicit PDFs
python .agents/skills/content-to-course/run.py \
  --pdf lecture_part1.pdf lecture_part2.pdf \
  --output-dir courses/ \
  --course-id advanced_pde

# Whole directory of PDFs
python .agents/skills/content-to-course/run.py \
  --pdf sample_content/ \
  --output-dir courses/ \
  --course-id compiled_course
```

### Incremental Append Mode
Append freshly generated questions to an existing course bank without overwriting previous work:
```bash
python .agents/skills/content-to-course/run.py \
  --pdf supplemental_module.pdf \
  --output-dir courses/ \
  --course-id test_run_pde \
  --append
```

### Advanced Options
```bash
python .agents/skills/content-to-course/run.py \
  --pdf sample_content/I__Ecuaciones_en_derivadas_parciales_2026.pdf \
  --output-dir courses/ \
  --course-id ecuaciones_derivadas_parciales \
  --title "Ecuaciones en Derivadas Parciales" \
  --strict \
  --append \
  --max-repair-iterations 3 \
  --audit-sample 40
```

## Running the Practice Platform
Once published, start the platform to practice immediately:
```bash
python run_platform.py
```
Open `http://localhost:3000/#/course/<course_id>` in any browser.
