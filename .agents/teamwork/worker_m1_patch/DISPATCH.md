## 2026-10-11T01:41:22Z
You are the Milestone 1 Patch Worker for the "Top's Academy" project.
Your working directory is: g:\Mi unidad\Competence_analyser\.agents\teamwork\worker_m1_patch
Read g:\Mi unidad\Competence_analyser\.agents\teamwork\ORIGINAL_REQUEST.md immediately.
Read g:\Mi unidad\Competence_analyser\PROJECT.md.

Read the 3 remediation blueprints prepared by the Explorers:
- Lexical plan: `g:\Mi unidad\Competence_analyser\.agents\teamwork\explorer_m1_fix_lexical\lexical_fix_plan.md`
- Semantic plan: `g:\Mi unidad\Competence_analyser\.agents\teamwork\explorer_m1_fix_semantic\semantic_fix_plan.md`
- Packaging plan: `g:\Mi unidad\Competence_analyser\.agents\teamwork\explorer_m1_fix_packaging\packaging_fix_plan.md`

Write ownership: You exclusively own `src/validator/`, `pyproject.toml`, and `tests/validator/`.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Your task:
1. Implement the Lexical Scanner remediations in `src/validator/lexical_scanner.py` per `lexical_fix_plan.md`:
   - Expand `LATEX_CONTROL_PREFIXES` to cover the full ~250 AMS-LaTeX, KaTeX, and physics macros starting with b, f, n, r, t, v, 0.
   - Implement Math Mode context tracking (`in_math` toggled by `$` and `$$`) to catch any single-backslash before control letters in math formulas.
   - Implement non-text control heuristics (`\b`, `\f`, `\r` followed by letters) and syntax signatures (`{`, `[`, `_`, `^`, `=`, `<`, `>`).
   - Fix full token parsing for `v` and `0` prefixes.
   - Clean up dead code.
2. Implement Semantic & Schema remediations in `src/validator/schema_validator.py` and `src/validator/rules.py` per `semantic_fix_plan.md`:
   - Add Draft-07 `allOf` conditional schemas in `schema_validator.py` requiring `options` on MCQ/MS and `correct_answer` on FIB.
   - Constrain `correct_answer` with non-empty checks (`minLength: 1`, `minItems: 1`, and object `anyOf: [{"required": ["value"]}, {"required": ["expression"]}]`).
   - Add `else:` branch on `multiple_select` in `rules.py` emitting `R-12: ERR_MS_COUNT`.
   - Add `elif itype == "fill_in_the_blank":` block in `rules.py` emitting `R-04: ERR_MISSING_ANSWER`.
   - Enrich `validate_schema()` to populate `item_id` and item context.
3. Implement Packaging & CLI remediations in `pyproject.toml` and `src/validator/` per `packaging_fix_plan.md`:
   - Update `pyproject.toml`: `[tool.setuptools.packages.find] where = ["src"]`, script `validate-course = "validator.cli:main"`, pytest pythonpath `[".", "src"]`.
   - Convert all internal imports across `src/validator/*.py` to relative imports (`from .models import ...`, `from .core import ...`).
   - Thread `--strict` parameter through `cli.py`, `core.py`, and implement strict validation rules.
4. Run all test suites and verify:
   - `python -m pytest tests/validator/test_validator.py -v` (must pass 67/67).
   - `python -m pytest tests/test_adversarial_validator.py -v` (all 35 must pass 100%).
   - `python -m pytest tests/validator/test_empirical_stress.py -v` (all 85 must pass 100%).
   - Re-install editable package: `pip install -e .` and verify `validate-course` CLI entrypoint.
5. Write your handoff report in `g:\Mi unidad\Competence_analyser\.agents\teamwork\worker_m1_patch\handoff.md` detailing all files modified and test execution logs.
6. Send a message to parent when complete.
