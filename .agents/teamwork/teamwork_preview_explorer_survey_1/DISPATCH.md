# Dispatch Assignment — Survey Agent 1 (Explorer)

You are teamwork_preview_explorer_survey_1.
Working directory: g:\Mi unidad\Competence_analyser\.agents\teamwork\teamwork_preview_explorer_survey_1\
Authoritative User Request: g:\Mi unidad\Competence_analyser\.agents\teamwork\ORIGINAL_REQUEST.md
Skill Directory: g:\Mi unidad\Competence_analyser\.agents\skills\content-to-course\

Scope: Survey requirements R1 & R2.
Investigate existing code, schemas, and pipelines in `.agents/skills/content-to-course/` (especially `ingest.py`, `check_pages.py`, `cta_analyzer.py`, `check_cta.py`, `plan_shards.py`, `check_templates.py`, `repair_loop.py`, `schemas/`).
Analyze:
1. R1: Vision Patcher consolidation: current page patch storage vs consolidated `work/patches/<doc_stem>.md` with clear page separators. CTA sequencing: current ordering vs preserving chronological/pedagogical order (`LEC01 -> LEC02`), `session` and `unit_index` schema fields.
2. R2: Shard payloads: current `plan_shards.py` and `work/shards/shard_XX.json` vs self-contained payload (DSL reference, template schemas, sandbox helpers, competency distractors), dynamic shard cap up to K=8 (~2-3 competencies per shard). `TPL-VAR` rule in `check_templates.py`: non-empty `vars`, stem placeholders, multi-seed uniqueness simulation up to required quota, flagging defective Solow templates with `FAIL (TPL-VAR)`.

Deliverable: Write comprehensive report to `survey_report.md` in your working directory and send completion message back.
