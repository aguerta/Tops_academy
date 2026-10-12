# Master Execution Plan: content-to-course v2 & Estadistica III

## Project Objectives
Deliver v2 of `content-to-course` skill and generate the Estadistica III course adhering strictly to the 2-phase protocol:
- **Fase 1 (Infraestructura de Código)**: Implementar y verificar al 100% todos los cambios a la skill (R1 a R6) y a la plataforma (R7). Ejecutar pruebas de regresión y congelar el código.
- **Fase 2 (Generación del Curso Nuevo)**: Ingestar y generar el curso de Estadística III (R8) sin modificar una sola línea de código Python o TypeScript.

---

## Phase 1 Milestones (Code Infrastructure & Platform Refactor)

### M1.1: Contracts & JSON Schemas
- Artifacts:
  - `.agents/skills/content-to-course/schemas/pages.schema.json`
  - `.agents/skills/content-to-course/schemas/cta.schema.json`
  - `.agents/skills/content-to-course/schemas/template.schema.json`
  - `.agents/skills/content-to-course/check_pages.py`
  - `.agents/skills/content-to-course/check_cta.py`
  - `.agents/skills/content-to-course/check_templates.py`
- Rules: JSON Schema Draft-07, CTA-D1/D2, TPL-D1..D4, zero domain dependencies.

### M1.2: Multiformat Vision Ingestion & Image Fallback Plan
- Artifacts:
  - `.agents/skills/content-to-course/ingest.py`
  - `.agents/skills/content-to-course/system_prompts/prompt_page_transcriber.md`
- Features: Directory scanning, PDF Beamer vs ink/scanned detection, image fallback (>2500px tiled with 10% overlap + overview thumbnail), PyMuPDF rendering, text layer extraction & diacritics normalization, SHA-256 caching manifest, batch distribution for vision subagents.

### M1.3: Generic Parametric Engine & AST Sandbox
- Artifacts:
  - `.agents/skills/content-to-course/engine/sandbox.py` (AST whitelist: `math`, `fractions`, `statistics`, `sympy`, `numpy`, `scipy.stats`, `rng`; banned: `open`, `eval`, `exec`, `compile`, `__import__`, dunder attributes, `os`, `sys`, subprocess, network; 2s timeout)
  - `.agents/skills/content-to-course/engine/instantiate.py` (duplicate rejection, quota distribution 30/20, seed determinism)
  - `.agents/skills/content-to-course/engine/assemble.py` (MC7 shuffle, distractor_id mapping, FIB tolerance, MS all-or-nothing, length anti-giveaway balance, LaTeX escaping)
  - `.agents/skills/content-to-course/engine/render.py` (`bmatrix`, `table_array`, `fmt`, `latex_frac`)
  - `.agents/skills/content-to-course/engine/invariants.py` & `diversity.py` (invariants on 100% instances, stem diversity >=0.5)

### M1.4: Platform FIB Decimal & Fraction Refactor
- Artifacts:
  - `platform/src/types.ts`
  - `platform/src/utils/mathEquivalence.ts`
  - `tests/test_math_adversarial_suite.ts`
- Features: `canonical_algebraic` / `value` / `expression` compatibility, comma decimal normalization (`0,8333` -> `0.8333`), 4 decimals tolerance (`0.00005`), fractions (`5/6` vs `0.8333`), tests passing.

### M1.5: Verification, Blind Judge & Modular Pipeline CLI
- Artifacts:
  - `.agents/skills/content-to-course/judge.py` (blind judge batch generator & evaluator)
  - `.agents/skills/content-to-course/run.py` (explicit stages: `--stage`, `--from-stage`, `--review-cta`, strict fail-fast without silent fallback)
  - `.agents/skills/content-to-course/course_publisher.py`
  - `.agents/skills/content-to-course/repair_loop.py`
  - `.agents/skills/content-to-course/SKILL.md`

### M1.6: Domain Cleanup, Migration & Skill Tests
- Actions:
  - Delete `edos_synthesizer.py`, remove domain keywords (`edo`, `pde`, etc.) from core engine.
  - Move 2 competencies per legacy topic to `.agents/skills/content-to-course/examples/edp/` and `examples/edo/`.
  - Rewrite `tests/test_skill.py` to test engine, sandbox, schemas, and legacy examples.
  - Verify `courses/pde_course.json` and `courses/sistemas_edos.json` continue to pass `--strict` unmodified.
  - Verify `tests/test_validator.py` and `tests/test_platform.py` pass without modifications.

### M1.7: Phase 1 Regression & Code Freeze
- Full regression verification: `pytest tests/test_skill.py tests/test_validator.py tests/test_platform.py`.
- Forensic integrity audit of Phase 1 codebase.
- Code Freeze milestone declaration. Record SHA/commit baseline.

---

## Phase 2 Milestones (Statistics III Course Generation - Zero Code Changes)

### M2.1: Ingestion & Vision Transcription
- Ingest `content/estadistica3_Cano` (3 Beamer PDFs, 1 ink PDF, 1 tiled PNG 5941x3327).
- Subagents transcribe all ~84 pages/tiles to `courses/estadistica3_regresion/work/pages/`.
- Validate with `check_pages.py`.

### M2.2: Cognitive Task Analysis (CTA)
- Subagent generates `cta.json` with >=20 competencies, fused distractors, and evidence citations from `Stats3 10-10.pdf` and `stats 3 3-10.png`.
- Validate with `check_cta.py`.

### M2.3: Parametric Templates Generation
- Specialist subagents write `templates/<id>.json` (>=6 per competency, >=2 per MC7/FIB/MS) with `generate_py` and `cross_check_py`.
- Validate with `check_templates.py`.

### M2.4: Engine Instantiation & Quality Verification
- Generic engine instantiates quotas (Skill >=30, Fact/Concept >=20).
- Check invariants (100%), diversity (>=0.5), blind judge concordance (>=95%).
- Assemble `courses/estadistica3_regresion.json`.

### M2.5: Course Validation, Platform Smoke & Final Victory Audit
- Run `python -m validator.cli courses/estadistica3_regresion.json --strict`.
- Verify platform renders `bmatrix` and `array` without KaTeX errors.
- Verify interactive FIB decimal/fraction grading.
- Verify `git diff` of `.py` and `.ts` files between Phase 1 freeze and final state is strictly empty.
- Independent victory audit confirmation.
