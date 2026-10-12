## 2026-10-11T21:09:38Z
You are a Worker agent (worker_m1c_pipeline_and_tests).
Your working directory is: g:\Mi unidad\Competence_analyser\.agents\teamwork\worker_m1c_pipeline_and_tests
Your parent orchestrator conversation ID is: 8c6e51b9-04fd-4a8c-a9ab-21b3a1985725

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Authoritative Request:
g:\Mi unidad\Competence_analyser\.agents\teamwork\ORIGINAL_REQUEST.md (specifically ## 2026-10-11T20:38:27Z and R1, R4, R6).
Read reference materials and explorer handoffs:
- C:\Users\augus\.gemini\antigravity\brain\d9fbac3b-e132-4b61-89ba-dc5d00df791f\content_to_course_v2_design.md
- C:\Users\augus\.gemini\antigravity\brain\d9fbac3b-e132-4b61-89ba-dc5d00df791f\implementation_plan.md
- g:\Mi unidad\Competence_analyser\.agents\teamwork\explorer_survey_skill\handoff.md
- g:\Mi unidad\Competence_analyser\.agents\teamwork\explorer_survey_tests\handoff.md
- g:\Mi unidad\Competence_analyser\.agents\teamwork\worker_m1b_engine\handoff.md

Exclusive Write Ownership:
You EXCLUSIVELY own and may create/edit/delete:
- `.agents/skills/content-to-course/judge.py`
- `.agents/skills/content-to-course/run.py`
- `.agents/skills/content-to-course/course_publisher.py`
- `.agents/skills/content-to-course/repair_loop.py`
- `.agents/skills/content-to-course/SKILL.md`
- `.agents/skills/content-to-course/examples/` (`examples/edp/`, `examples/edo/`)
- Delete `.agents/skills/content-to-course/edos_synthesizer.py`
- Clean domain logic from `.agents/skills/content-to-course/batch_generator.py`, `cta_analyzer.py`, `verifier.py`
- `pyproject.toml`
- `tests/test_skill.py`
You MUST NOT edit files in `platform/` or `courses/`.

Tasks:
1. Implement `judge.py`:
   - Generate `work/judge_batch.json` with 2 instances per template WITHOUT the answer key.
   - Compare judge responses against answer keys and emit discordances with a max of 3 correction cycles.
2. Implement Modular `run.py` CLI:
   - CLI flags: `--stage ingest|cta|templates|build|verify|publish`, `--from-stage N`, `--review-cta`, `--course-id`, `--title`, `--work-dir`, `--pdf` (accepting directory or file list), `--append`.
   - Strict fail-fast: if an artifact is missing, terminate with exit code != 0 and clear error message. NO silent fallback to templates, NO external LLM API calls.
3. Update `course_publisher.py` and `repair_loop.py`:
   - Compatible with v2 stages and schema. Retain length balance repair and JSON sanitization without any domain logic.
4. Update `SKILL.md`:
   - Document the v2 pipeline, JSON stage contracts, subagent roles, and execution guide.
5. Domain Cleanup & Few-Shot Migration:
   - DELETE `edos_synthesizer.py`.
   - In `batch_generator.py`, `cta_analyzer.py`, and `verifier.py`, remove domain keywords, regexes, and legacy branches. If these files are superseded by `engine/` modules, make them thin wrappers or clean them so that `grep -ri` of domain terms (`edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `regresi`) in `.agents/skills/content-to-course/**/*.py` finds ZERO domain logic (only examples in `examples/`).
   - Create few-shot examples in `examples/edp/` (`cta.json`, `templates/`) and `examples/edo/` (`cta.json`, `templates/`) with 2 full competencies per topic.
   - Update `pyproject.toml` to declare dependencies (`numpy`, `scipy`, `PyMuPDF`, `Pillow`).
6. Rewrite `tests/test_skill.py`:
   - Rewrite with 6 modular test classes (32 test cases) as specified by `explorer_survey_tests`:
     1. `TestSandboxSecurity`: AST rejection of `import os`, `open`, `__import__`, dunder attributes (`__`), subprocess, network, and timeout 2.0s.
     2. `TestGenericEngine`: deterministic seed sweeps, parameter & stem deduplication, quota distribution (30/20), length balance.
     3. `TestStageContracts`: CTA-D1/D2, TPL-D1..D4, manifest coverage.
     4. `TestMultiformatIngest`: image tiling > 2500 px with 10% overlap, Beamer diacritic normalization, SHA-256 caching.
     5. `TestPipelineFailFast`: `run.py` fails without `cta.json`, zero silent fallback.
     6. `TestFewShotRegression`: legacy EDP and EDO few-shot templates generate valid questions through the generic engine.
7. Verification & Regression Tests:
   - Run `python -m pytest tests/test_skill.py -v` (must pass 100%).
   - Run `python -m pytest tests/test_validator.py tests/test_platform.py -v` (must continue passing 100%).
   - Run `python -m validator.cli courses/pde_course.json --strict` and `python -m validator.cli courses/sistemas_edos.json --strict` (must exit 0 and course hashes must match).
   - Run `grep` to verify zero domain logic in skill `.py` files.
8. Document all commands, outputs, and diffs in `handoff.md` in your working directory.
When complete, notify parent orchestrator (8c6e51b9-04fd-4a8c-a9ab-21b3a1985725) using send_message.
