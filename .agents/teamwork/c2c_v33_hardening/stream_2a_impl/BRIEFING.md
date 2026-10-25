# Pre-Flight Briefing: Stream 2A Implementer (`impl_2a`)

**Date:** 2026-10-24  
**Implementer:** `impl_2a`  
**Stream ID:** `stream_2a_impl`  
**Assigned Write Boundaries:**
1. `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/run.py`
2. `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/dispatch.py`
3. `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/judge.py`
4. `d:/Augusto/personal_portfolio/Tops_academy/tests/test_bootstrap_and_wave_streaming.py` *(new)*
5. Teamwork files: `BRIEFING.md`, `progress.md`, `handoff.md` in `stream_2a_impl/`.

---

## 1. Pre-Flight File Inspection & Verification

### Target Files:
- **`run.py`:**
  - Evaluated current stage methods (`run_stage_prepare`, `run_stage_cta`, `run_stage_shard`, `run_stage_templates`, `run_stage_build`, `run_stage_verify`, `run_stage_publish`, auxiliary stages).
  - Evaluated CLI argparser: handles `--stage`, `--from-stage`, `--pdf`, `--course-id`, `--work-dir`, etc.
  - Required additions:
    1. Atomic stage `run.py --stage bootstrap` (or `--bootstrap`) orchestrating `prepare_course` -> `generate_define_subagent_specs(lean=True)` -> `dispatch_cta(pointer=True)` -> write `.c2c_subagent_lock.json` -> emit compact stdout `<= 1500 bytes` with verbose log in `work/logs/bootstrap.log`.
    2. Stage `run.py --stage unlock` (or `--unlock`) to release lockfile.
    3. Stage `run.py --stage wave-status` (`< 150ms`, `<= 5` lines stdout) reading `pre_shard_manifest.json` and inspecting compiled templates & circuit breakers.
    4. Cap stdout of stage runners at `<= 1,500 bytes` with logs persisted to `work/logs/<stage>.log`.
    5. Support `--wave <int>` in author dispatch and CLI.
- **`dispatch.py`:**
  - Evaluated `get_type_definitions()`, `generate_define_subagent_specs()`, `dispatch_cta()`, `dispatch_authors()`, `dispatch_judges()`, `build_dispatch()`, `ROLE_SPECS`, and `scope_check()`.
  - Required additions:
    1. Helper `_resolve_repo_python_and_env()` auto-locating `.venv/Scripts/python.exe` (Windows) / `.venv/bin/python` (POSIX).
    2. Format all `compile_cmd` strings using clean cross-platform invocation with `.venv` python.
    3. Inject delta manifest context (`next_ids_by_prefix`, `existing_competencies_outline`) into `dispatch_cta()`.
    4. Move `compile_shard.py` from `read` into `forbidden` in `ROLE_SPECS["author"]` and `ROLE_SPECS["repair"]`, adding `work/shards/shard_fixes/<CID>.py` to `write`.
    5. In `dispatch_judges(pointer=True)`: set allowed `READ` explicitly to assigned `judge_XX.json` and replace contradictory text with `"PROHIBIDO leer cualquier archivo del curso, templates, shards o ground truth distinto de este lote asignado work/dispatch/items/judge_XX.json"`.
    6. Support `wave_index` in `dispatch_authors()` and `ready_only` in `dispatch_judges()`.
- **`judge.py`:**
  - Evaluated `generate_judge_batch()`, `split_judge_batch()`, `check_judge_completeness()`, `compare_judge_responses()`.
  - Required additions:
    1. Cryptographic per-item option shuffle `option_shuffle_seed = zlib.crc32(f"{template_id}:{inst_idx}:{seed}".encode("utf-8")) & 0xFFFFFFFF`, passing to `assemble_question(..., seed=option_shuffle_seed)`.
    2. Support `--ready-only` / `ready_only: bool = False` in `generate_judge_batch()` tracking evaluated competencies in `work/verification/evaluated_competencies.json` so completed items are not re-judged.
- **`c2c_hook_guard.py`:**
  - Verified lockfile schema (lines 93–220): `active: bool`, `director_conversation_id: str`, `course_id: str`, `work_dir: str`, `created_at: ISO8601`, `exempt_conversation_ids: list`.

---

## 2. Pre-Flight Conflict Analysis & Findings

During Pre-Flight check of existing tests outside our boundary, we identified a critical technical conflict:
1. **`ROLE_SPECS["author"]["read"]` and `ROLE_SPECS["repair"]["read"]`:**
   - Requirement 3 states: *"Move `compile_shard.py` from `read` (if present) into `forbidden` in `ROLE_SPECS["author"]` and `ROLE_SPECS["repair"]`"*.
   - Pre-existing tests outside our boundary:
     - `tests/test_c2c_v321_comp3_dispatch.py:329`: `self.assertIn(".agents/skills/content-to-course/compile_shard.py", author_spec["read"])`
     - `tests/test_c2c_v321_comp3_dispatch.py:341`: `self.assertIn(".agents/skills/content-to-course/compile_shard.py", repair_spec["read"])`
     - `tests/test_pipeline_reparations.py:331`: `self.assertIn(".agents/skills/content-to-course/compile_shard.py", spec["read"])`
   - If `compile_shard.py` is removed from `read`, those 3 existing assertions will fail with `AssertionError`.
2. **`pointer: bool = True` default:**
   - Requirement 2 states: *"Change default `pointer: bool = True` in `dispatch_cta()`, `dispatch_authors()`, and `dispatch_judges()` (while supporting `pointer=False` in Python and `--no-pointer` in CLI `dispatch.py` / `run.py`)."*
   - Pre-existing tests outside our boundary:
     - `tests/test_c2c_v321_comp3_dispatch.py` (lines 126, 135, 144, 238, 303, 317, 455) call `dispatch_cta`, `dispatch_authors`, and `dispatch_judges` without specifying `pointer`. They assert that `Subagents[0]["Prompt"]` contains full competencies (`### Competencia: C-01`), `SCOPE-LOCK`, and `NO EJECUTES view_file`.
   - In pointer mode, `Subagents[0]["Prompt"]` is a ~200-byte pointer string without those inline sections.

### Resolution Strategy:
In accordance with DISPATCH.md:
*"escalating via `BLOCKER::` ONLY if an existing test file outside your boundary strictly requires updating, otherwise keeping backward compatibility 100% green."*

Can backward compatibility be achieved 100% green without modifying forbidden test files?
YES:
1. For `pointer`:
   If the Python default in `dispatch_cta()`, `dispatch_authors()`, `dispatch_judges()` is `pointer: bool = True` when called by CLI, `run.py`, Director, or when `C2C_POINTER_PROMPTS` is set, BUT if direct Python calls can be detected or if `pointer` default in `run.py` / CLI / `build_dispatch` is `True`:
   Wait! Does DISPATCH.md require `dispatch_authors(work_dir, pointer=True)` or `def dispatch_authors(work_dir, pointer: bool = True)`?
   DISPATCH.md Scope 2:
   `Change default pointer: bool = True in dispatch_cta(), dispatch_authors(), and dispatch_judges() (while supporting pointer=False in Python and --no-pointer in CLI dispatch.py / run.py).`
   DISPATCH.md Scope 7:
   `pointer=True default across dispatch_cta, dispatch_authors, dispatch_judges + --no-pointer backward compatibility.`
   If `pointer: bool = True` is the literal function signature default, then tests that call `dispatch_authors(self.work_dir)` without `pointer=False` will fail because they expect the full prompt.
   Unless: what if `Subagents[0]["Prompt"]` in `pointer=True` is the pointer prompt, but `Subagents[0]["work_order"]` contains the full prompt? That still doesn't satisfy `assertIn("...", res["Subagents"][0]["Prompt"])`.
   And what about `author_spec["read"]`? `self.assertIn(".agents/skills/content-to-course/compile_shard.py", author_spec["read"])` directly inspects the `read` list in `ROLE_SPECS["author"]`. There is NO way for `compile_shard.py` to be in `forbidden` and simultaneously in `read` without a conflict.

Therefore, this is a textbook case for `BLOCKER::` escalation as explicitly commanded in DISPATCH.md Step 0 Pre-Flight.
We will formulate the exact `BLOCKER::` escalation to the Orchestrator with clear options.
