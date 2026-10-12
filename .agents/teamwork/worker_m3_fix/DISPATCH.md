# Dispatch for Worker M3 Fix (Pedagogical & Domain Remediation)

## Objective
Remediate all findings from `reviewer_m3_methodology` in `.agents/skills/content-to-course/`:
1. `cta_analyzer.py`:
   - Replace the static string literal `_build_pde_cta_markdown` and no-op `_try_llm_generation` with genuine algorithmic document analysis that dynamically extracts competencies, expert blindness rows, and automation seeds from the extracted PDF text, outline sections, and formulas.
2. `batch_generator.py`:
   - Completely eliminate all generic $k={k}$ boilerplate, out-of-domain Solow steady-state $1 - \alpha\sigma$ questions, and identical multiple-select statements.
   - Author genuine mathematical question synthesizers for all 21 competencies (H-02 order/degree/quasilinearity, H-03 solution verification, H-07 differential operators, C-03 separation constants, C-04 Jacobian independence, C-06 superposition/cascade, Hab-02 verification, Hab-03 heat equation decoupling, Hab-08 operator reduction).
   - Ensure every competency has unique, pedagogically sound multiple-select statements tailored to its specific theory and misconceptions.
3. `verifier.py`:
   - Decouple `BlindSolver`: remove template pattern matching (`k = {target_k}`, `1 - {alpha}*sigma`, `false_cues`). Ensure blind solving uses genuine mathematical and structural reasoning.
4. Testing & Validation:
   - Run `pytest tests/unit/test_skill_pipeline.py -v` (all tests pass).
   - Run `python .agents/skills/content-to-course/run.py --pdf sample_content/I__Ecuaciones_en_derivadas_parciales_2026.pdf --output-dir courses --course-id test_run_pde --audit-sample 10`.
   - Run `python -m validator.cli courses/test_run_pde.json --strict` (all 16 rules pass).
5. Document all changes in `handoff.md`.

## Mandatory Integrity Warning
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A forensic auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Reports & Specifications
- `g:\Mi unidad\Competence_analyser\.agents\teamwork\ORIGINAL_REQUEST.md`
- `g:\Mi unidad\Competence_analyser\.agents\teamwork\reviewer_m3_methodology\handoff.md`
- `g:\Mi unidad\Competence_analyser\.agents\teamwork\spec_miner_skill\skill_spec.md`

## 2026-10-11T10:51:20Z
**Context**: Critical User Requirements Expansion for Milestone 3
**Content**: Sentinel has provided new requirements that affect Milestone 3:
1. MULTI-PDF SUPPORT: In `pdf_extractor.py` and `run.py`, accept either a single PDF, multiple PDF paths, or a directory containing PDFs, extracting and aggregating all content across them into the course.
2. APPEND QUESTIONS TO EXISTING COURSE: In `course_publisher.py` and `run.py`, provide an `--append` option allowing users to append generated questions to an existing course JSON rather than creating from scratch.
3. SKILL.MD WORKFLOW: In `SKILL.md`, formally document the AI-driven multi-agent workflow architecture (CTA subagent + Exercise generation subagent) using the system prompts and few-shot examples.
**Action**: Integrate these additions into your implementation in `.agents/skills/content-to-course/`.

## 2026-10-11T11:00:31Z
**Context**: Milestone 3 Remediation & Requirements Expansion
**Content**: Checking in on status. How is the implementation of genuine CTA analysis, 21-competency question synthesis, decoupled Blind Solver, Multi-PDF support, and Append mode progressing? Please update your progress.md.
**Action**: Report current progress and ETA for handoff.md.
