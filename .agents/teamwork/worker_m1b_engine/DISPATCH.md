## 2026-10-11T20:55:07Z
You are a Worker agent (worker_m1b_engine).
Your working directory is: g:\Mi unidad\Competence_analyser\.agents\teamwork\worker_m1b_engine
Your parent orchestrator conversation ID is: 8c6e51b9-04fd-4a8c-a9ab-21b3a1985725

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Authoritative Request:
g:\Mi unidad\Competence_analyser\.agents\teamwork\ORIGINAL_REQUEST.md (specifically ## 2026-10-11T20:38:27Z and R1, R2, R3, R5).
Read reference design and explorer report:
- C:\Users\augus\.gemini\antigravity\brain\d9fbac3b-e132-4b61-89ba-dc5d00df791f\content_to_course_v2_design.md
- g:\Mi unidad\Competence_analyser\.agents\teamwork\explorer_survey_skill\handoff.md
- g:\Mi unidad\Competence_analyser\.agents\teamwork\explorer_survey_skill\analysis.md

Exclusive Write Ownership:
You EXCLUSIVELY own and may create/edit:
- `.agents/skills/content-to-course/schemas/pages.schema.json`
- `.agents/skills/content-to-course/schemas/cta.schema.json`
- `.agents/skills/content-to-course/schemas/template.schema.json`
- `.agents/skills/content-to-course/check_pages.py`
- `.agents/skills/content-to-course/check_cta.py`
- `.agents/skills/content-to-course/check_templates.py`
- `.agents/skills/content-to-course/ingest.py`
- `.agents/skills/content-to-course/system_prompts/prompt_page_transcriber.md`
- `.agents/skills/content-to-course/system_prompts/prompt_competence_analyser.md`
- `.agents/skills/content-to-course/system_prompts/prompt_creator_exercises.md`
- `.agents/skills/content-to-course/engine/` (`__init__.py`, `sandbox.py`, `instantiate.py`, `assemble.py`, `render.py`, `invariants.py`, `diversity.py`)
You MUST NOT edit files in `platform/` or `courses/`.

Tasks:
1. Create JSON Schemas in `.agents/skills/content-to-course/schemas/`:
   - `pages.schema.json`: manifest and page headers (doc, page, kind, sha256, render_dpi, tile, has_text_layer).
   - `cta.schema.json`: CTA schema with fused distractors (id, name, wrong_belief, correct_belief, omitted_step, trigger, manifestation, error_type, severity, origin, evidence, remediation_hint), Bloom, prerequisites, source_examples.
   - `template.schema.json`: competency_id, templates list (interaction_type, difficulty, bloom, stem, generate_py, cross_check_py, hints, solution, distractor_ids).
2. Create Validation Scripts:
   - `check_pages.py`: checks 100% manifest pages transcribed, cross-checks text layer numbers/symbols.
   - `check_cta.py`: validates cta.json against schema, enforces CTA-D1 (>=3 distractors per comp, >=6 per Skill with >=2 omitted_step), CTA-D2 (unique IDs, non-null wrong_belief or omitted_step), verifies evidence pages exist in manifest.
   - `check_templates.py`: schema, AST sandbox check, dry-run 50 seeds, invariants check, TPL-D1 (valid distractor_id references), TPL-D2 (MC7 uses 6 distinct distractor_ids), TPL-D3 (100% distractor coverage across templates), TPL-D4 (distractors != correct answer).
3. Create Multiformat Ingestion in `ingest.py`:
   - Analyzes directory: detects Beamer PDFs, OneNote ink PDFs (0 text layer), images (.png, .jpg).
   - If image > 2500 px (e.g. `stats 3 3-10.png` 5941x3327 px): tile into 3x2 grid with 10% overlap + overview thumbnail.
   - Render PDF pages via PyMuPDF (fitz) at 130-150 dpi.
   - Extract and normalize text layer with corrupt diacritics (`´`+vocal).
   - Generate SHA-256 caching manifest `manifest.json`.
   - Partition into balanced vision batches (~10 items per batch) in `vision_batches.json`.
4. Create Generic Parametric Engine in `engine/`:
   - `sandbox.py`: AST whitelist (`math`, `fractions`, `statistics`, `sympy`, `numpy`, `scipy.stats`, `random` via `rng`), bans `os`, `sys`, `subprocess`, `open`, `eval`, `exec`, `compile`, `__import__`, dunder attributes (`__`), network. Executes in isolated worker with 2.0s timeout per instance.
   - `instantiate.py`: sweeps seeds deterministically, rejects duplicate parameter tuples and duplicate stem texts, allocates quotas (>=30 Skill, >=20 Fact/Concept) evenly across templates with >=2 per interaction type.
   - `assemble.py`: builds course question JSON conforming to platform format (shuffled MC7 with distinct distractor_ids, FIB with tolerance/equivalents, MS 4-6, hints 3-5, detailed_solution, common_misconception_warning from distractor remediation_hint, length anti-giveaway balance, LaTeX escaping via json.dumps). ZERO domain keywords in engine!
   - `render.py`: KaTeX helper functions (`bmatrix`, `table_array`, `fmt`, `latex_frac`).
   - `invariants.py`: evaluates 100% of instances (1 correct, distractors distinct from correct and each other, cross_check True, no leaks in stem/hints).
   - `diversity.py`: calculates `unique(masked_stems)/total >= 0.5` per competency.
5. Create System Prompts:
   - `prompt_page_transcriber.md`: vision transcription rules (KaTeX math, arrays for tables, describe graphs, [ILEGIBLE]).
   - `prompt_competence_analyser.md`: CTA generation rules producing `cta.json`.
   - `prompt_creator_exercises.md`: parametric template authoring rules.
6. Verify your implementation by running dry-run tests and unit checks. Document commands and results in `handoff.md`.
When complete, notify parent orchestrator (8c6e51b9-04fd-4a8c-a9ab-21b3a1985725) using send_message.
