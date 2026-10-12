# Dispatch Assignment — Survey Agent 2 (Explorer)

You are teamwork_preview_explorer_survey_2.
Working directory: g:\Mi unidad\Competence_analyser\.agents\teamwork\teamwork_preview_explorer_survey_2\
Authoritative User Request: g:\Mi unidad\Competence_analyser\.agents\teamwork\ORIGINAL_REQUEST.md
Skill Directory: g:\Mi unidad\Competence_analyser\.agents\skills\content-to-course\

Scope: Survey requirements R3 & R4.
Investigate existing code, schemas, and engines in `.agents/skills/content-to-course/` (especially `schemas/template.schema.json`, `engine/assemble.py`, `engine/instantiate.py`, `check_templates.py`, `run.py`, `judge.py`).
Analyze:
1. R3: `stem_variants` support in `template.schema.json`, `engine/assemble.py`, and `engine/instantiate.py`. How stems are stored and formatted. How stem diversity ratio is currently computed or needs to be computed, and how to make diversity ratio >= 0.5 a hard gate in `check_templates.py` and `run.py --stage build`.
2. R4: Stratified Blind Judge in `judge.py`. Current sampling and evaluation logic. How to implement stratified sample of exactly 2 items per competency. Canonical normalization of keys/choices (A/B/C, option prefix mismatch fix like `OPT_` prefix vs `opt_a`, numeric tolerance for fill-in-the-blank). Blind evaluation enforcement (ensuring judge LLM cannot access ground truth / answer keys).

Deliverable: Write comprehensive report to `survey_report.md` in your working directory and send completion message back.


## 2026-10-12T06:13:37Z
[Message] timestamp=2026-10-12T06:13:37Z sender=16a74650-bfa4-4250-90d1-044a303b90f3 priority=MESSAGE_PRIORITY_HIGH content=You are teamwork_preview_explorer_survey_2.
Your working directory is: g:\Mi unidad\Competence_analyser\.agents\teamwork\teamwork_preview_explorer_survey_2\
The Authoritative User Request is located at: g:\Mi unidad\Competence_analyser\.agents\teamwork\ORIGINAL_REQUEST.md
Your dispatch instructions are at: g:\Mi unidad\Competence_analyser\.agents\teamwork\teamwork_preview_explorer_survey_2\DISPATCH.md

You MUST read ORIGINAL_REQUEST.md first.
Survey existing code, schemas, and engines in g:\Mi unidad\Competence_analyser\.agents\skills\content-to-course\ specifically for requirements R3 and R4:
- R3: Question Diversity & stem_variants (schemas/template.schema.json, engine/assemble.py, engine/instantiate.py, check_templates.py, run.py --stage build, diversity ratio >= 0.5 hard gate).
- R4: Stratified Blind Judge & Key Normalization (judge.py, stratified sample of exactly 2 items/competency, canonical normalization of keys and choices, preventing OPT_ prefix mismatches and numeric tolerance issues, blind evaluation rules preventing access to answer keys).

Produce a comprehensive, rigorous technical survey report with code locations, existing mechanisms, required modifications, and potential risks.
Write your complete report to: g:\Mi unidad\Competence_analyser\.agents\teamwork\teamwork_preview_explorer_survey_2\survey_report.md
Also maintain your progress.md and handoff.md in your working directory.
When finished, send a message to the caller with the path to your survey report.
