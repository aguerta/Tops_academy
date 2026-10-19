# BRIEFING — 2026-10-19T03:55:27Z

## Mission
Implement Gate 0 Safety Foundation & Legacy Purge (R1 / P0): protect active workspaces from orphan deletion in delete_course.py, isolate test_clean_orphan_dirs, fix frac_simple_fix in assemble.py, and fully purge legacy corpus.md / section_*.md references across the repository.

## 🔒 My Identity
- Archetype: teamwork_preview_worker
- Roles: implementer, qa, specialist
- Working directory: d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/worker_gate0
- Original parent: e831bfe5-b034-48b8-9c7e-f1ebfdfd3200
- Milestone: Gate 0 (Sequential Foundation — Safety Lock)

## 🔒 Key Constraints
- DO NOT CHEAT: all implementations genuine, no hardcoded results or dummy facades.
- DO NOT run full test suite `python -m pytest tests -q` (strictly locked until Gate 0 passes independent audit).
- Only targeted verification via `python -m pytest tests/test_delete_course.py -q`.
- Follow minimal change principle and preserve comments/docstrings.
- Write handoff.md and notify parent with send_message upon completion.

## Current Parent
- Conversation ID: e831bfe5-b034-48b8-9c7e-f1ebfdfd3200
- Updated: 2026-10-19T04:13:00Z

## Task Summary
- **What to build**:
  1. `delete_course.py`: Protect active workspaces in `clean_orphan_course_dirs` (presence of `work/state.json`, `work/pre_cta_manifest.json`, `work/cta_data.py` OR any file modified within 24h); support `COURSES_DIR` env override.
  2. `tests/test_delete_course.py`: Isolate `test_clean_orphan_dirs` with `tmp_path` and `monkeypatch`; test active workspace preservation, orphan deletion, and real `courses/` safety.
  3. `assemble.py`: In `frac_simple_fix`, replace `[^{}\\]+` with `[^{}\\^_]+` to preserve subscripts `_` and superscripts `^` inside fractions.
  4. Purge legacy `corpus.md` and `section_*.md` from `dispatch.py`, `run.py`, `SKILL.md`, system prompts, `README.md`, `PROJECT.md`, and add regression tests.
- **Success criteria**:
  - `python -m pytest tests/test_delete_course.py -q` passes 100% (24/24 passing).
  - Zero stdout/dispatch mentions of `corpus.md` or `section_*.md`.
- **Interface contracts**: `.agents/skills/delete-course/`, `.agents/skills/content-to-course/`
- **Code layout**: Root repo layout

## Key Decisions Made
- `COURSES_DIR` default initialized from `os.environ.get("COURSES_DIR", REPO_ROOT / "courses")` and resolved dynamically via `get_effective_courses_dir()` across all operations in `delete_course.py`.
- `assert_path_safe` adapted to permit paths inside the effective `COURSES_DIR` override (such as `tmp_path` in test runners) while strictly maintaining content/ and fixture immutability.
- In `dispatch.py`, replaced `corpus.md` fallbacks with fail-fast `BLOCKER::` assertions pointing to original document path or slice path from `pre_cta_manifest.json`.

## Artifact Index
- `.agents/teamwork/worker_gate0/DISPATCH.md` — Assignment instructions
- `.agents/teamwork/worker_gate0/BRIEFING.md` — Working memory and status
- `.agents/teamwork/worker_gate0/progress.md` — Heartbeat log
- `.agents/teamwork/worker_gate0/handoff.md` — Final handoff report

## Change Tracker
- **Files modified**:
  - `.agents/skills/delete-course/scripts/delete_course.py`: Added active workspace protection and `COURSES_DIR` env override.
  - `tests/test_delete_course.py`: Isolated `test_clean_orphan_dirs` using `tmp_path`, added active workspace, LaTeX frac fix, and purge tests (24/24 pass).
  - `.agents/skills/content-to-course/engine/assemble.py`: Verified `frac_simple_fix` preserves subscripts and superscripts inside fractions.
  - `.agents/skills/content-to-course/dispatch.py`: Replaced `work/sections/section_*.md` with parts slices and removed all `corpus.md` fallbacks/reads.
  - `.agents/skills/content-to-course/run.py`: Updated Stage 0 banner and removed `corpus file:` stdout print.
  - `.agents/skills/content-to-course/SKILL.md`: Purged `work/corpus.md` references in favor of direct PDF / slice reads.
  - `prompt_competence_analyser.md` & `prompt_cta_sectional.md`: Removed `corpus.md` and `section_XX.md`.
  - `README.md` & `PROJECT.md`: Cleaned `corpus.md` and `Corpus Slicing` references.
- **Build status**: 24/24 tests pass in 0.27s.
- **Pending issues**: None. Gate 0 implementation 100% complete.

## Quality Status
- **Build/test result**: PASS (24 passed in 0.27s)
- **Lint status**: Clean (py_compile passed on all changed Python files)
- **Tests added/modified**: `test_clean_orphan_dirs` isolated; added `TestActiveWorkspaceSafeguards`, `TestLatexRegexFracFix`, and `TestPurgeLegacyCorpusAndSections`.

## Loaded Skills
- Source: None loaded directly
- Local copy: None
- Core methodology: Minimal edits, safety-first, test isolation
