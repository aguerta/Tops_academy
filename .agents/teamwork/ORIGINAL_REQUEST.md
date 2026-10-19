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


## 2026-10-19T03:49:57Z

Harden the Top's Academy Content-to-Course (C2C) multi-agent pipeline to achieve reliable, unattended course generation in ≤ 20 minutes per run by eliminating CTA micro-edit loops, reducing Director emission latency, preventing straggler token burn, and enforcing strict workspace data safety. Execution leverages parallel streams with independent adversarial auditors and an automated review-fix repair loop.

Working directory: d:/Augusto/personal_portfolio/Tops_academy
Integrity mode: demo

Reference: d:/Augusto/Downloads/c2c_hardening_plan.md and d:/Augusto/personal_portfolio/Tops_academy/reports/c2c_audits/master_forensic_synthesis_7_runs.md

## Execution Architecture: Parallel Streams & Safety Sequencing

1. **Gate 0 (Sequential Foundation — Safety Lock)**:
   - R1 (P0 Data Safety & Legacy Artifact Purge) must be fully implemented, verified, and audited with a formal `PASS` before any other parallel changes or broad test runs execute, preventing accidental deletion of active workspaces.
2. **Gate 1 (Concurrent Parallel Implementation Streams)**:
   - **Stream A (CTA Architecture & Ingest)**: R3 (P2 CTA Zero-Micro-Edit & Patch Ledger) and R4 (P3 Lossless MapReduce Partitioning & Slicing).
   - **Stream B (Template Engine & Author Pipeline)**: R2 (P1 Stage 3 Diagnostics & Circuit Breakers) and R6.1 (P5 Author Adaptive Sizing & Syntax Normalization).
   - **Stream C (Orchestration, Watchdog & Evaluation)**: R5 (P4 Director Pointer Prompts & Budget Watchdog) and R6.2 (P6 Judge Native Batching & Blind Re-dispatch).
   - **Stream D (Environment, Append & Documentation)**: R7 (P7 Append Workflow, Unicode Resilience & P8 Documentation v3.22).
3. **Gate 2 (Integration & End-to-End Benchmark)**:
   - Merging streams, full regression suite execution, and the MapReduce P3.0 spike against `solow_model`.

## Requirements

### R1. Workspace Data Safety & Legacy Artifact Elimination (P0 — Sequential Prerequisite)
- Guard `clean_orphan_course_dirs` in `delete_course.py` from deleting any workspace containing active state files (`work/state.json`, `work/pre_cta_manifest.json`, `work/cta_data.py`) or any file modified within the last 24 hours. Support overriding `COURSES_DIR` via environment variable.
- Completely purge all residual references, stdout print statements, and fallback paths for legacy `corpus.md` and `section_*.md` across `dispatch.py`, `run.py`, `SKILL.md`, and subagent system prompts, enforcing direct lossless PDF/image access.
- Commit the 2-line LaTeX regex fix in `assemble.py` (`frac_simple_fix`).

### R2. Stage 3 Diagnostics, Tool Isolation & Circuit Breakers (P1 — Stream B)
- Prohibit author subagents from reading `compile_shard.py` in `dispatch.py`.
- Enhance `check_templates.py` (`TPL-DRY`) to provide detailed failure diagnostics (first failing seed, parameters, exception name and message, and the last 3 call frames mapped to shard source lines).
- Implement a stateful SHA-256 circuit breaker in `check_templates.py` that halts repeated identical template failures while immediately clearing on code changes.
- Add bounded compilation counters (`[COMPILE n/6]`) and graceful missing-file error handling in `compile_shard.py`.
- Standardize author prompt with a canonical 15-line template pattern and enforce parameter space ≥ 500 combinations.

### R3. CTA Zero-Micro-Edit Architecture & Patch Ledger (P2 — Stream A)
- Re-architect Competence Taxonomy Architect (CTA) generation to enforce single atomic creation (`write_to_file`), allowing ≤ 1 repair turn, ≤ 3 total file edits, and ≤ 2 compile cycles per architect.
- Implement layered automated healing prior to subagent intervention: L1 pre-import LaTeX tokenization and raw-string conversion; L2 deterministic KaTeX syntax repair; L3 evidence page normalization and heading snapping (`pages_index.md`); L4 unthrottled consolidated repair pack (`cta_repair_pack.json`); and L5 terminal degrade-and-flag (wrapping unresolvable math in `\text{}`).
- Establish an append-only, cross-run `patch_ledger.py` recording every automatic repair (`healed`, `snapped`, `degraded`) with human-readable reporting in `work/cta_review.md` and automated alerts if degraded fields exceed 3%.

### R4. Lossless CTA MapReduce Partitioning (P3 — Stream A)
- Implement weight-balanced sequential partitioning in `partition_corpus.py` based strictly on PDF structural weights (stream size, vector strokes, ink/image density) without text extraction.
- Slice source documents physically using `pymupdf` `select()` + `save()` into lossless sub-PDFs (`work/parts/part_NN/`), preserving vector ink and original typography.
- Support localized slice page indexing (pages 1..n) remapped to global document coordinates upon deterministic merge in `cta_merge.py`.
- Validate the MapReduce pipeline via a dedicated verification spike against the `solow_model` corpus prior to defaulting.

### R5. Director Emission Reduction & Runtime Resilience (P4 — Stream C)
- Migrate subagent dispatch to a pointer-prompt protocol: lean system prompts (≤ 5 KB) containing static roles and rules, paired with ultra-compact (~300 B) dynamic work orders referencing disk JSON payloads (`work/dispatch/items/`).
- Enforce the Swift-Dispatch SLA (≤ 20 seconds from dispatch command completion to `invoke_subagent` dispatch).
- Purge stale errored subagents via `manage_subagents(kill_all)` prior to Stage 5.
- Deploy an automated watchdog (`budget_guard.py`) on timer interrupts to abort and replace runaway subagents exceeding 40 turns, 5M tokens, or looping on tool scripts.
- Introduce stateful resumption checkpoints in `work/state.json` to handle 429/404 API rate limits seamlessly.

### R6. Author Scaling & Native Judge Batching (P5, P6 — Streams B & C)
- Dynamically size author shards (`clamp(ceil(N / 8), 2, 6)` competencies per shard) with up to 8 concurrent authors.
- Enforce native batch slicing for blind judges at ≤ 12 items per batch (`judge_batch_NN.json`), with automated detection and re-dispatch of incomplete evaluations.
- Normalize non-variable double curly braces (`{{token}}` → `{token}`) in template compilers.

### R7. Append Workflow & Environment Resilience (P7, P8 — Stream D)
- Enable seamless delta generation in `prepare --append` by preserving existing competency IDs and injecting continuous ID sequences.
- Sanitize CLI argument parsing to handle Unicode titles gracefully on Windows PowerShell and eliminate path quoting anomalies.
- Bump skill documentation to v3.22 with updated architectural diagrams, failure taxonomies, and watchdog procedures.

### R8. Independent Adversarial Audit & Iterative Repair Loop
- **Independent Scrutiny**: For each stream and requirement (R1 through R7), an independent adversarial auditor conducts an audit completely separate from the implementing agent.
- **Anti-Cheating Verification**: Scrutinize code, tests, and git diffs to verify zero artificial mocks, zero hardcoded bypasses, and zero weakened assertions.
- **Worst-Case Pipeline Analysis**: Stress-test edge cases (e.g. malformed PDFs, intense vector ink density, token ceilings, zero-length files, Windows path escaping) and identify whether any change introduces worst-case regressions or pipeline bottlenecks.
- **Limitation Documentation**: Explicitly detail implementation boundaries and operating assumptions.
- **Iterative Review-Fix Loop**: If the auditor emits a critique or `FAIL`, a subagent is immediately dispatched to fix the findings. The fix is re-submitted to the auditor. This cycle repeats iteratively until the auditor verifies the remediation and issues a formal `PASS` certification.

## Acceptance Criteria

### Programmatic Regression & Unit Testing
- [ ] `python -m pytest tests/test_delete_course.py tests/test_cta_healing.py tests/test_latex_engine.py tests/test_compile_shard.py -q` passes 100% clean.
- [ ] Full repository test suite `python -m pytest tests -q` passes without regressions (executed strictly after Gate 0 / P0 isolation is certified).
- [ ] `clean_orphan_course_dirs` verified not to delete directories with recent modifications (< 24h) or active state files (`state.json`, `pre_cta_manifest.json`, `cta_data.py`).
- [ ] Automated check confirms zero stdout occurrences of `corpus.md` or `section_*.md` during `run.py --stage prepare` or inside `work/dispatch/**`.

### Independent Adversarial Audit Certification
- [ ] Every individual requirement (R1 through R7) achieves an explicit, signed-off auditor `PASS` certification.
- [ ] Zero unmitigated cheat patterns, dummy mocks, or weakened checks across all modified modules.
- [ ] Worst-case analysis documented for each stream, proving no catastrophic edge-case bottlenecks.
- [ ] Any initial auditor rejection triggers the review-fix loop and resolves successfully to a verified `PASS`.

### Performance & Quality Benchmark Gates (20-Competency Course)
- [ ] Total wall-clock runtime ≤ 20 minutes from stage 0 start to course publication.
- [ ] CTA execution stage completes in ≤ 6 minutes.
- [ ] Zero construction micro-edits in CTA; total architect file edits ≤ 3; compile cycles ≤ 2.
- [ ] Single-shard maximum author token consumption ≤ 4M tokens.
- [ ] Director dispatch emission latency ≤ 30 seconds total across all stages.
- [ ] Zero manual human interventions required during the complete run.
- [ ] Degraded fields in `patch_ledger.json` do not exceed 3% of total competencies.
