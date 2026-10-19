# Dispatch: Gate 0 Safety Foundation & Legacy Purge Worker

## Identity
- Role: Gate 0 Safety Implementation Worker
- Type: teamwork_preview_worker
- Working Directory: d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/worker_gate0/
- Parent Conversation ID: e831bfe5-b034-48b8-9c7e-f1ebfdfd3200

## Assigned Scope (Requirement 1 / P0)
1. **Workspace Data Safety in delete_course.py**:
   - Location: `.agents/skills/delete-course/scripts/delete_course.py` (around lines 465-484).
   - In `clean_orphan_course_dirs`: NEVER delete any directory under `COURSES_DIR` if it contains active workspace state files (`work/state.json`, `work/pre_cta_manifest.json`, `work/cta_data.py`) OR any file modified within the last 24 hours.
   - Support overriding `COURSES_DIR` via environment variable (e.g. `COURSES_DIR = Path(os.environ.get("COURSES_DIR", ...))`).
2. **Test Isolation in tests/test_delete_course.py**:
   - Location: `tests/test_delete_course.py` (around line 164).
   - Isolate `test_clean_orphan_dirs` using pytest's `tmp_path` fixture and `monkeypatch.setattr(delete_course, "COURSES_DIR", tmp_path)` (or env var).
   - Add tests verifying:
     - A live workspace containing active state files (`work/state.json`, etc.) or recent files (<24h) is NOT deleted.
     - An old orphan directory without active files is cleaned.
     - The real `courses/` directory is never touched.
3. **Commit 2-line LaTeX regex fix in assemble.py**:
   - Location: `.agents/skills/content-to-course/engine/assemble.py`.
   - In `frac_simple_fix`: change regex `[^{}\\]+` to `[^{}\\^_]+` so that subscript `_` and superscript `^` (e.g. `_{xy}`, `_{xx}`, `K^{0.5}`) inside fractions are not broken.
4. **Complete Purge of legacy corpus.md and section_*.md**:
   - `.agents/skills/content-to-course/dispatch.py`:
     - L240: replace legacy `"work/sections/section_*.md"` with `"work/parts/part_*/**"` and `"work/parts/part_manifest_*.json"`.
     - L463, L543, L546, L556: remove `sp.get("text_ref") ... or f"{work_rel}/corpus.md"` and `doc_rows` fallback to `corpus.md`. Point directly to original file path or slice path from `pre_cta_manifest.json`. Fail fast if missing.
     - L579: remove `corpus.md` from `read_paths`.
   - `.agents/skills/content-to-course/run.py`:
     - L222: update banner to `"Stage 0: Lossless source partitioning & pre_cta_manifest generation"`.
     - L271: delete `print(f"  [+] Corpus file: ...")`.
   - `.agents/skills/content-to-course/SKILL.md`:
     - Clean legacy mentions of `work/corpus.md` extraction; document that subagents read original PDFs or lossless slices directly via `view_file`.
   - `.agents/skills/content-to-course/system_prompts/prompt_competence_analyser.md` & `prompt_cta_sectional.md`: clean any legacy references.
   - `README.md` & `PROJECT.md`: clean references to `corpus.md`.
   - Add automated assertion test in `tests/test_delete_course.py` (or new test in `tests/`) asserting zero stdout occurrences of `corpus.md` and `section_` during prepare / dispatch.
5. **Verification**:
   - Run: `python -m pytest tests/test_delete_course.py -q`
   - Ensure 100% clean passing tests.
   - NOTE: DO NOT run the full test suite `python -m pytest tests -q` yet! Only run the targeted test suite for `test_delete_course.py`.


## 2026-10-19T03:55:27Z
You are the Gate 0 Safety Foundation & Legacy Purge Worker.
Your working directory is: d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/worker_gate0/

You MUST read and follow:
1. d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/ORIGINAL_REQUEST.md (under header ## 2026-10-19T03:49:57Z)
2. d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/worker_gate0/DISPATCH.md
3. d:/Augusto/Downloads/c2c_hardening_plan.md (§5 P0 Data safety)
4. d:/Augusto/personal_portfolio/Tops_academy/reports/c2c_audits/master_forensic_synthesis_7_runs.md (§3.1)

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Your task:
1. Modify `.agents/skills/delete-course/scripts/delete_course.py`:
   - In `clean_orphan_course_dirs`, ensure that a directory under `COURSES_DIR` is NEVER deleted if it contains active workspace state files (`work/state.json`, `work/pre_cta_manifest.json`, `work/cta_data.py`) OR any file modified within the last 24 hours.
   - Allow overriding `COURSES_DIR` via an environment variable `COURSES_DIR` if set.
2. Modify `tests/test_delete_course.py`:
   - In `test_clean_orphan_dirs`, isolate the test using `tmp_path` and `monkeypatch.setattr(delete_course, "COURSES_DIR", tmp_path)` (or via the env var) so it NEVER operates on the real `courses/` directory.
   - Add comprehensive tests:
     - Verify active workspaces (containing state files or recent files <24h old) are preserved.
     - Verify orphan directories older than 24h with no state files are cleaned.
     - Verify the real courses directory is never touched.
3. Modify `.agents/skills/content-to-course/engine/assemble.py`:
   - In `frac_simple_fix`, replace `[^{}\\]+` with `[^{}\\^_]+` so subscripts `_` and superscripts `^` inside fractions (e.g., `_{xy}`, `_{xx}`, `K^{0.5}`) are preserved.
4. Completely purge legacy `corpus.md` and `section_*.md` fallbacks, prompts, and stdout lines:
   - In `.agents/skills/content-to-course/dispatch.py`:
     - L240: replace `"work/sections/section_*.md"` with `"work/parts/part_*/**"` and `"work/parts/part_manifest_*.json"`.
     - L463, L543, L546, L556: remove `corpus.md` fallbacks; point to original file or slice path from `pre_cta_manifest.json`.
     - L579: remove `corpus.md` from `read_paths`.
   - In `.agents/skills/content-to-course/run.py`:
     - L222: update banner to `"Stage 0: Lossless source partitioning & pre_cta_manifest generation"`.
     - L271: delete print statement `print(f"  [+] Corpus file: ...")`.
   - In `.agents/skills/content-to-course/SKILL.md`:
     - Clean legacy mentions of `work/corpus.md`.
   - In system prompts (`prompt_competence_analyser.md`, `prompt_cta_sectional.md`): clean legacy references to `corpus.md` / `section_*.md`.
   - In `README.md` and `PROJECT.md`: clean references to `corpus.md`.
   - Add a test in `tests/test_delete_course.py` (or a dedicated test) ensuring that `corpus.md` and `section_` never appear in `run.py --stage prepare` stdout or inside `work/dispatch/**`.
5. Run verification:
   - Execute: `python -m pytest tests/test_delete_course.py -q`
   - Ensure all tests pass.
   - NOTE: DO NOT run the full pytest test suite yet (`python -m pytest tests -q` is strictly locked until Gate 0 passes independent audit).

Write your progress in `progress.md` and upon completion write a complete `handoff.md` in your working directory and notify the parent orchestrator via `send_message`.
