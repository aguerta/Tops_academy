# BRIEFING — 2026-10-11T21:10:00Z

## Mission
Implement Content-to-Course v2 infrastructure: JSON schemas, validators, multiformat ingestion, generic parametric engine, and system prompts.

## 🔒 My Identity
- Archetype: worker
- Roles: implementer, qa, specialist
- Working directory: g:\Mi unidad\Competence_analyser\.agents\teamwork\worker_m1b_engine
- Original parent: 8c6e51b9-04fd-4a8c-a9ab-21b3a1985725
- Milestone: M1b

## 🔒 Key Constraints
- Exclusively own and modify:
  .agents/skills/content-to-course/schemas/pages.schema.json
  .agents/skills/content-to-course/schemas/cta.schema.json
  .agents/skills/content-to-course/schemas/template.schema.json
  .agents/skills/content-to-course/check_pages.py
  .agents/skills/content-to-course/check_cta.py
  .agents/skills/content-to-course/check_templates.py
  .agents/skills/content-to-course/ingest.py
  .agents/skills/content-to-course/system_prompts/prompt_page_transcriber.md
  .agents/skills/content-to-course/system_prompts/prompt_competence_analyser.md
  .agents/skills/content-to-course/system_prompts/prompt_creator_exercises.md
  .agents/skills/content-to-course/engine/ (__init__.py, sandbox.py, instantiate.py, assemble.py, render.py, invariants.py, diversity.py)
- MUST NOT edit files in platform/ or courses/.
- Genuine implementation: no hardcoding, no cheats, zero domain keywords in generic parametric engine.

## Current Parent
- Conversation ID: 8c6e51b9-04fd-4a8c-a9ab-21b3a1985725
- Updated: 2026-10-11T20:55:07Z

## Task Summary
- **What to build**: Content-to-course v2 components: JSON schemas (pages, cta, template), validators (check_pages, check_cta, check_templates), multiformat ingest (ingest.py), generic parametric engine (sandbox, instantiate, assemble, render, invariants, diversity), and system prompts (transcriber, competence analyser, exercise creator).
- **Success criteria**: All schemas, validators, ingestion pipeline, parametric engine modules, and system prompts implemented genuinely and passing validation checks.
- **Interface contracts**: content_to_course_v2_design.md and explorer survey reports.
- **Code layout**: .agents/skills/content-to-course/

## Key Decisions Made
- Implemented AST sandbox with strict whitelist (math, fractions, statistics, sympy, numpy, scipy, random, decimal) and banned dunders/I/O.
- Built isolated worker subprocess execution for hard timeout handling and batch acceleration.
- Built 3x2 image tiling with 10% overlap + overview thumbnail in ingest.py for images >2500px.
- Built diacritic normalizer in ingest.py for corrupt Beamer characters (`´`+vowel).
- Zero domain keywords confirmed in all engine/ modules.

## Artifact Index
- .agents/skills/content-to-course/schemas/pages.schema.json
- .agents/skills/content-to-course/schemas/cta.schema.json
- .agents/skills/content-to-course/schemas/template.schema.json
- .agents/skills/content-to-course/check_pages.py
- .agents/skills/content-to-course/check_cta.py
- .agents/skills/content-to-course/check_templates.py
- .agents/skills/content-to-course/ingest.py
- .agents/skills/content-to-course/system_prompts/prompt_page_transcriber.md
- .agents/skills/content-to-course/system_prompts/prompt_competence_analyser.md
- .agents/skills/content-to-course/system_prompts/prompt_creator_exercises.md
- .agents/skills/content-to-course/engine/__init__.py
- .agents/skills/content-to-course/engine/sandbox.py
- .agents/skills/content-to-course/engine/render.py
- .agents/skills/content-to-course/engine/invariants.py
- .agents/skills/content-to-course/engine/diversity.py
- .agents/skills/content-to-course/engine/assemble.py
- .agents/skills/content-to-course/engine/instantiate.py

## Change Tracker
- **Files modified**: All 17 assigned files created and tested.
- **Build status**: PASS (100% test pass on test_engine_full.py, test_engine_smoke.py, test_validator.py, test_platform.py)
- **Pending issues**: None

## Quality Status
- **Build/test result**: 8/8 full engine verification tests passed, 114/114 regression tests passed.
- **Lint status**: Clean
- **Tests added/modified**: test_engine_full.py, test_engine_smoke.py

## Loaded Skills
- **Source**: g:\Mi unidad\Competence_analyser\.agents\skills\content-to-course\SKILL.md
- **Local copy**: g:\Mi unidad\Competence_analyser\.agents\teamwork\worker_m1b_engine\SKILL.md
- **Core methodology**: End-to-end course generation from academic PDFs via Cognitive Task Analysis, fused distractors, parametric exercise templates, AST sandboxing, invariant checks, and automated validation.
