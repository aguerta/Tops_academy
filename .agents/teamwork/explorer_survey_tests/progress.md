# Progress — explorer_survey_tests

Last visited: 2026-10-11T20:48:30Z

- [x] Initialized DISPATCH.md, BRIEFING.md, and progress.md
- [x] Read reference materials and ORIGINAL_REQUEST.md
- [x] Inspected existing test files: `tests/test_skill.py`, `tests/test_validator.py`, `tests/test_platform.py`
  - `test_validator.py` + `test_platform.py`: 114 tests passing in 18.14s. Completely decoupled from skill.
  - `test_skill.py`: 27 tests passing in 20.20s against legacy domain-specific code. Ready for modular generic rewrite.
- [x] Inspected existing courses and verified with validator:
  - `courses/pde_course.json`: Valid in `--strict` mode (21 competencies, 500 questions). SHA256: 3A8D4C0D23CA9FCFA8A2B7E05765725E1C3B71391DDB74011667850256694192.
  - `courses/sistemas_edos.json`: Valid in `--strict` mode (20 competencies, 470 questions). SHA256: 6AFAFB088AEABF0729A4223DE8F28BEC80D958395C5157C56D592F4B9D3FCB06.
- [x] Analyzed sandbox security requirements and implementation strategy:
  - Static AST whitelist: allow math, fractions, statistics, sympy, numpy, scipy, scipy.stats.
  - AST rejections: os, sys, subprocess, socket, urllib, open, __import__, dunder attributes (`__`), eval, exec, compile.
  - Execution runtime: deterministic seed via RNG, isolated subprocess execution with 2.0s per-instance timeout (cross-platform, safe on Windows).
- [x] Inspected `content/estadistica3_Cano/` files:
  - `EST3_LEC01_26_2.pdf`: 297,245 B, 13 pages, text layer: 5,243 chars, corrupted accents.
  - `EST3_LEC02_26_2.pdf`: 311,530 B, 26 pages, text layer: 12,749 chars, sum derivations.
  - `EST3_LEC03_26_2.pdf`: 305,378 B, 29 pages, text layer: 19,406 chars, matrix regression, P/M/M0, t/F tests.
  - `Stats3 10-10.pdf`: 3,560,906 B, 9 pages, text layer: only 381 chars (vector ink from OneNote, invisible to text extractor, requires vision).
  - `stats 3 3-10.png`: 697,520 B, RGBA 5941x3327 px (>2500 px threshold, requires tiling with 10% overlap + overview = 7 images).
  - Total vision workload: 13 + 26 + 29 + 9 + 7 = 84 image units.
- [x] Defined exact test cases for rewriting `tests/test_skill.py` without breaking other tests (6 modular test classes, 30+ test cases).
- [x] Formulated comprehensive 6-gate test plan for Phase 1 code freeze.
- [ ] Generate `analysis.md` and `handoff.md`
- [ ] Notify parent orchestrator
