---
name: content-to-course
description: End-to-end Antigravity skill that converts any academic course materials (PDFs, handwritten ink, large images) into interactive Top's Academy courses using strict JSON stage contracts, parametric templates in a sandboxed Python engine, blind LLM arbitration, and automated validation without domain-specific code.
triggers:
  - "create course from pdf"
  - "generate Top's Academy course"
  - "analyze competencies"
  - "convert pdf to course"
  - "publish course"
inputs:
  pdf:
    type: string
    description: Path to input course document, directory, or multiple files
    required: true
  output_dir:
    type: string
    description: Directory where the published course JSON is stored (defaults to courses/)
    default: courses
  course_id:
    type: string
    description: Alphanumeric slug identifier for the course
    required: false
  title:
    type: string
    description: Human-readable title for the course
    required: false
  work_dir:
    type: string
    description: Working directory for intermediate stage JSON artifacts
    required: false
  stage:
    type: string
    description: Run a single stage (ingest, cta, templates, build, verify, publish)
    required: false
  from_stage:
    type: string
    description: Resume pipeline execution from a given stage to completion
    required: false
  review_cta:
    type: boolean
    description: Pause execution after stage 1 (CTA) for inspection before template generation
    default: false
  strict:
    type: boolean
    description: Whether to enforce strict mode validation (16 psychometric rules)
    default: true
  append:
    type: boolean
    description: Whether to append questions into an existing course bank instead of replacing it
    default: false
outputs:
  course_file:
    type: string
    description: Absolute path to the validated course JSON (courses/<course_id>.json)
  cta_file:
    type: string
    description: Absolute path to the Cognitive Task Analysis document
---

# Content-to-Course Antigravity Skill (v2 Architecture)

A universal, subject-agnostic educational engineering pipeline that converts raw academic materials (Beamer presentations, handwritten OneNote notes, statistical software exports, and high-resolution chalkboard images) into fully playable, interactive Top's Academy courses.

## Pipeline Architecture & JSON Stage Contracts

The v2 pipeline operates via sequential, resumable stages communicating exclusively through validated JSON artifacts on disk. If any required artifact is missing, the pipeline fails fast immediately with a non-zero exit code: **zero silent fallback to hardcoded templates and zero external LLM API calls** (the Antigravity agents act as the LLMs).

```
[ Academic Input: PDFs, Handwritten Ink, Large Images (>2500px) ]
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 0: Ingest & Vision (ingest.py)                           │
│ - PyMuPDF rendering (130-150 DPI) + Diacritic normalization     │
│ - High-res image tiling (>2500px: 3x2 grid, 10% overlap, thumb) │
│ - Manifest caching with SHA-256 (work/pages/manifest.json)      │
│ - Vision transcription subagents: pages/<doc>/<n>.md            │
└────────────────────────────────┬────────────────────────────────┘
                                 │ pages.schema.json
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 1: Cognitive Task Analysis (check_cta.py)                 │
│ - Knowledge Triad: Facts [H], Concepts [C], Skills [Hab]       │
│ - Fused Distractors: Expert Blindness + Misconceptions          │
│ - CTA-D1: >=3 distractors/comp, >=6/Skill (>=2 with omitted_step)│
│ - CTA-D2: Unique distractor IDs, non-null wrong_belief/omitted  │
│ - Optional pause checkpoint: --review-cta                       │
└────────────────────────────────┬────────────────────────────────┘
                                 │ cta.schema.json (work/cta.json)
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 2: Parametric Templates Authoring (check_templates.py)   │
│ - Authoring subagents generate templates/<comp_id>.json        │
│ - >=6 templates per competency (>=2 MC7, >=2 FIB, >=2 MS)       │
│ - AST Whitelist Sandbox: math, fractions, numpy, scipy, sympy   │
│ - Prohibits: os, sys, subprocess, open, eval, exec, dunder, net │
│ - 50-seed dry run, invariants, TPL-D1..D4 (distractor coverage) │
└────────────────────────────────┬────────────────────────────────┘
                                 │ template.schema.json
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 3: Generic Engine Instantiation (engine/instantiate.py)  │
│ - Deterministic seed sweeps fulfilling strict quotas:           │
│     * >=30 questions per Skill [Hab]                            │
│     * >=20 questions per Fact [H] or Concept [C]               │
│ - Parameter tuple & stem text deduplication                     │
│ - Masked stem diversity ratio: unique / total >= 0.5            │
│ - KaTeX rendering helpers: bmatrix, table_array, fmt, latex_frac│
│ - Outputs: work/course.json                                     │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 4: Independent Verification & Blind Judge (judge.py)      │
│ - Invariants evaluated on 100% of instances                     │
│ - Anti-giveaway option bounds [0.8*min, 1.2*max] & distribution │
│ - Blind Judge Batch: 2 instances/template WITHOUT answer keys   │
│ - Judge response comparison & discordance cycles (max 3 cycles) │
│ - Strict course validation & auto-repair loop (repair_loop.py)  │
│ - Outputs: work/course_verified.json                            │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 5: Course Publication & Registration (course_publisher.py)│
│ - Saves validated course JSON to courses/<course_id>.json       │
│ - Append mode (--append): merges questions preserving unique IDs│
│ - Practice platform automatically discovers and registers course│
└─────────────────────────────────────────────────────────────────┘
```

---

## Subagent Roles & System Prompts

The workflow decouples cognitive curriculum extraction from psychometric question generation across specialized subagents:

### 1. Vision Transcription Subagents
- **Prompt Reference**: `system_prompts/prompt_page_transcriber.md`
- **Role**: Transcribes individual pages and image tiles into structured Markdown with KaTeX formulas, tabular arrays, and figure descriptions.
- **Rules**: Zero extrapolation; marks `[ILEGIBLE]` if unclear; formats matrices and EViews regression tables as KaTeX `\\begin{array}`.

### 2. CTA Architect Subagent
- **Prompt Reference**: `system_prompts/prompt_competence_analyser.md`
- **Role**: Reads transcribed pages and synthesizes `work/cta.json` complying with `cta.schema.json`.
- **Rules**: Decomposes competencies into Knowledge Triad, links evidence (doc and page), and crafts fused distractors (expert blindness + misconceptions).

### 3. Exercise Template Creator Subagents
- **Prompt Reference**: `system_prompts/prompt_creator_exercises.md`
- **Role**: Authors parametric template files `work/templates/<comp_id>.json`.
- **Rules**: Provides a sandboxed Python `generate(rng)` function returning variables, correct answer, and distractors mapped to `distractor_ids` from the CTA.

### 4. Independent Blind Judge Subagent
- **Role**: Solves 2 sample instances per template presented in `work/judge_batch.json` with zero access to answer keys, hints, or solutions.
- **Rules**: `judge.py` compares judge solutions against ground truth. If agreement is < 95%, discordance reports guide template repair across up to 3 correction cycles.

---

## CLI Execution Guide

### 1. Run Complete Pipeline
```bash
python .agents/skills/content-to-course/run.py \
  --pdf content/estadistica3_Cano \
  --course-id estadistica3_regresion \
  --title "Estadística III: Modelo de Regresión Lineal"
```

### 2. Inspection Checkpoint (`--review-cta`)
Pause execution immediately after Stage 1 (CTA) to inspect competencies and fused distractors before generating templates:
```bash
python .agents/skills/content-to-course/run.py \
  --pdf content/estadistica3_Cano \
  --course-id estadistica3_regresion \
  --review-cta
```

### 3. Resuming from a Stage (`--from-stage`)
Resume execution after template authoring:
```bash
python .agents/skills/content-to-course/run.py \
  --work-dir courses/estadistica3_regresion/work \
  --from-stage templates \
  --course-id estadistica3_regresion
```

### 4. Running a Single Stage (`--stage`)
```bash
# Ingest documents and prepare manifest/tiling only
python .agents/skills/content-to-course/run.py --stage ingest --pdf content/estadistica3_Cano --work-dir work

# Validate CTA rules only
python .agents/skills/content-to-course/run.py --stage cta --work-dir work

# Instantiate question bank only
python .agents/skills/content-to-course/run.py --stage build --work-dir work

# Verify course bank and generate blind judge batch
python .agents/skills/content-to-course/run.py --stage verify --work-dir work

# Publish course to platform
python .agents/skills/content-to-course/run.py --stage publish --work-dir work --output-dir courses
```

### 5. Append Questions to Existing Course (`--append`)
```bash
python .agents/skills/content-to-course/run.py \
  --work-dir courses/estadistica3_regresion/work \
  --from-stage build \
  --course-id estadistica3_regresion \
  --append
```

---

## How to Process Any New Academic Topic (Zero Code Changes)

1. **Place content** in any folder (PDFs, handwritten notes, PNG/JPG images).
2. **Run stage 0 (ingest)**:
   ```bash
   python .agents/skills/content-to-course/run.py --stage ingest --pdf path/to/content --work-dir work
   ```
3. **Transcribe pages**: Vision subagents transcribe pages from `work/vision_batches.json` to `work/pages/`.
4. **Generate CTA**: CTA subagent creates `work/cta.json` using `prompt_competence_analyser.md`. Verify with `check_cta.py`.
5. **Author templates**: Template subagents author `work/templates/*.json` using `prompt_creator_exercises.md`. Verify with `check_templates.py`.
6. **Instantiate and verify**:
   ```bash
   python .agents/skills/content-to-course/run.py --from-stage build --work-dir work --course-id my_course
   ```
7. **Start practice**:
   ```bash
   python run_platform.py
   ```
   Open `http://localhost:3000/#/course/my_course`.
