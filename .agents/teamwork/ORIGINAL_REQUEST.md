# Original User Request

## Initial Request — 2026-10-12T06:10:03Z

Refactor and optimize the `content-to-course` educational generation pipeline and Top's Academy practice platform to eliminate multi-agent authoring bottlenecks (Variability Fixers, subagent file over-reading, patch fragmentation), enforce pedagogical content sequencing and question diversity (>=0.5), and implement a 3-strikes solution reveal safeguard in the practice UI.

Working directory: g:\Mi unidad\Competence_analyser
Integrity mode: development

## Requirements

### R1. Pipeline Ingestion & Consolidation
- Consolidate Vision Patcher markdown transcriptions so that all pages originating from the same source document are merged into a single structured patch file (`work/patches/<doc_stem>.md`). Different documents must remain in separate files.
- Ensure the Cognitive Task Analysis (CTA) synthesizes competencies respecting the chronological/pedagogical order of source documents and lecture sessions (e.g., `LEC01 -> LEC02 -> LEC03`), including optional session/unit metadata, without sorting by knowledge type (`H/C/Hab`).

### R2. Self-Contained Shards & Variability Validation (Zero Fixers)
- Generate self-contained shard payloads in `work/shards/shard_XX.json` that include the complete DSL reference, template schemas, sandbox helpers, and competency distractors. Shard author subagents must not need to inspect internal engine code.
- Increase the dynamic shard cap up to $K=8$ for large courses (~2-3 competencies per shard).
- Enforce the `TPL-VAR` rule in `check_templates.py`: verify non-empty `vars`, stem placeholders, and simulate multi-seed uniqueness up to the required quota before passing. Plantillas with insufficient parameter combinations must fail early in the author's local loop.

### R3. Question Diversity & `stem_variants`
- Add support for `stem_variants` in `template.schema.json`, `engine/assemble.py`, and `engine/instantiate.py`.
- Turn the stem diversity ratio ($\ge 0.5$) into a hard gate in `check_templates.py` and `run.py --stage build`.

### R4. Stratified Blind Judge & Key Normalization
- Refactor `judge.py` to extract a stratified sample of exactly 2 items per competency for blind evaluation.
- Canonically normalize keys and choices (`A/B/C`, numeric tolerance in fill-in-the-blank) to prevent artificial 0% agreement failures.
- Enforce blind evaluation rules so judges cannot access answer keys or ground truth.

### R5. Platform Educational Guardrail (3-Strikes Reveal)
- In `platform/src/components/PracticeSession.tsx` and `FeedbackToast.tsx`, track consecutive incorrect attempts per question.
- After 3 failed attempts, lock the question inputs, reveal the correct answer(s), automatically expand the step-by-step solution and misconception warning, award 0 mastery points, and guide the user to the next question.

### R6. Independent Offline Test Suite & Performance
- Provide an automated test suite (`tests/test_pipeline_optimizations.py`) validating all pipeline improvements against existing course artifacts (`Solow_model` and `estadistica3_regresion`) without external LLM API dependencies.
- Enable parallel multi-core template validation using `ProcessPoolExecutor` in `check_templates.py`.

## Acceptance Criteria

### Ingestion & CTA Sequencing
- [ ] Patch files for pages of the same original document are unified in `work/patches/<doc_stem>.md` with clear page separators.
- [ ] `cta.json` competency list preserves the order of source sessions, and `course.json` retains this pedagogical progression.
- [ ] CTA schema supports `session` and `unit_index` optional fields.

### Template Validation & Authoring
- [ ] `check_templates.py` fails on templates with empty `vars` or lack of dynamic stem variables.
- [ ] `check_templates.py` run on unpatched Solow templates flags the 51 defective templates with `FAIL (TPL-VAR)`.
- [ ] Templates declaring `stem_variants` pass validation and produce diversity ratios $\ge 0.5$ in test instantiations.
- [ ] Parallel multi-core validation runs across templates utilizing available CPU cores.

### Blind Judges
- [ ] `judge.py` generates stratified batches (~2 items/competency) and matches ground truth with normalized options without `OPT_` prefix mismatches.

### Practice Platform UI
- [ ] In `PracticeSession`, submitting 3 incorrect answers locks inputs and displays "Maximum attempts reached (3/3)".
- [ ] The feedback toast reveals the correct answer, step-by-step solution, and misconception warning on the 3rd failure.
- [ ] The session advances to the next question with 0 credit for the exhausted item.
- [ ] Existing automated tests (`tests/test_platform.py`, Playwright tests) pass or are updated to reflect the new 3-attempt lifecycle.
