# DISPATCH: Stream 2A — Implementer (`impl_2a`)

- **Orchestrator Conversation ID (`Recipient` for `send_message`):** `d0ce22db-904e-4856-b353-59975bfb5874`
- **Teamwork Directory (Governance Docs):** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_2a_impl`
- **Exclusive Production/Test Write Boundaries:**
  1. `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/run.py`
  2. `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/dispatch.py`
  3. `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/judge.py`
  4. `d:/Augusto/personal_portfolio/Tops_academy/tests/test_bootstrap_and_wave_streaming.py` *(new)*
  5. `d:/Augusto/personal_portfolio/Tops_academy/tests/test_c2c_v321_comp3_dispatch.py` *(authorized in Tier A Escalation #4: modernize `compile_shard.py` -> `forbidden`, coherent judge pointer, and explicit `pointer=False` where testing legacy inline prompt rendering)*
  6. `d:/Augusto/personal_portfolio/Tops_academy/tests/test_pipeline_reparations.py` *(authorized in Tier A Escalation #4: line 331 `compile_shard.py` -> `forbidden` & `pointer` alignment in `TestAuthorDispatchAndProtocol` only)*
  7. `d:/Augusto/personal_portfolio/Tops_academy/tests/test_dispatch_scope.py` *(authorized in Tier A Escalation #4b: line 181 `pointer=False` for explicit inline prompt assertion, or check `item_file` in default `pointer=True`)*
  8. `d:/Augusto/personal_portfolio/Tops_academy/tests/test_c2c_v31_adversarial_plan.py` *(authorized in Tier A Escalation #4b: line 856 `pointer=False` in `build_dispatch(role="judge", ..., pointer=False)` for legacy Zero-Warmup inline test)*

> **CRITICAL RULES:**
> - **DO NOT** modify ANY file outside the 4 files above + `stream_2a_impl/*.md` (Stream 2B is editing `system_prompts/**` and `SKILL.md` in parallel!).
> - **NEVER** pass `ArtifactMetadata` when calling `write_file` or `edit_file`.
> - **NEVER** leave temporary helper `.py` scripts in the workspace root or leave an active `.c2c_subagent_lock.json` inside `REPO_ROOT/courses/*` during tests (always use `tmp_path` in tests!).

## Step 0: Mandatory Pre-Flight Sanity Check
Read `run.py`, `dispatch.py`, `judge.py`, `c2c_hook_guard.py` (lines 93–220 for `.c2c_subagent_lock.json` schema), `plan_shards.py` (lines 708–775 for `wave_index` / `waves`), and existing tests (`tests/test_c2c_v321_comp2_shard.py`, `tests/test_c2c_case_2b_mastery.py`, `tests/test_cta_mapreduce.py`, or any `test_*dispatch*` / `test_*judge*` / `test_*run*`) BEFORE editing!
Pay special attention to whether any existing unit test calls `dispatch_cta(work_dir)`, `dispatch_authors(work_dir)`, or `dispatch_judges(work_dir)` directly in Python and inspects fields inside `Subagents[i]["Prompt"]`! Make sure `work/dispatch/items/*.json` preserves 100% of full metadata/payloads, support `--no-pointer` / `pointer=False` cleanly, and check existing tests in Pre-Flight (escalating via `BLOCKER::` ONLY if an existing test file outside your boundary strictly requires updating, otherwise keeping backward compatibility 100% green).
Write `stream_2a_impl/BRIEFING.md` confirming Pre-Flight before touching code.

## Scope of Implementation (Bottlenecks #1, #5, #6, #9, #11, #13 + Milestones 4 & 7)

### 1. New Atomic Stage `run.py --stage bootstrap` (`< 5s` local compute, total startup SLA `<= 60–90s`) & `wave-status`
- Support `run.py --stage bootstrap` accepting `--sources` / `--source-dir`, `--course-id`, `--work-dir` (optional, auto-resolved as in `prepare`), `--append`, `--granularity`, and `--director-id <CONVERSATION_ID>` (optional, defaults to `""` or `os.environ.get("C2C_DIRECTOR_ID", "")`).
- Execute atomically in one CLI call:
  1. `prepare_course(...)` (Zero-Raster PDF ingest already hardened in Stream 1E).
  2. `generate_define_subagent_specs(work_dir, lean=True)` — writes `work/dispatch/types/*.json` to disk **WITHOUT** dumping the 87 KB `subagent_types.json` content to `stdout`!
  3. `dispatch_cta(work_dir, pointer=True)` — writes `work/dispatch/cta_work_orders.json` and `work/dispatch/items/*.json`.
  4. Write `work/.c2c_subagent_lock.json` conforming to `c2c_hook_guard.py`'s exact schema:
     ```json
     {
       "active": true,
       "director_conversation_id": "<director_id>",
       "course_id": "<course_id>",
       "work_dir": "<posix_abs_work_dir>",
       "created_at": "<ISO8601_UTC>",
       "exempt_conversation_ids": []
     }
     ```
  5. Emit a compact JSON summary (`<= 1.5 KB` on `stdout`, full verbose log written to `work/logs/bootstrap.log`) containing `status`, `course_id`, `work_dir`, `lock_file`, `type_spec_files` (list of the 4 `work/dispatch/types/*.json` POSIX paths), `cta_unit_count`, and the compact pointer `Subagents` array ready for `invoke_subagent`.
- **Lockfile Lifecycle Release:** Automatically remove (or set `"active": false` and unlink) `work/.c2c_subagent_lock.json` when `run.py --stage publish` succeeds OR when `run.py --stage unlock --work-dir <dir>` (or `--unlock`) is invoked.
- **New `run.py --stage wave-status --work-dir <dir>` (`< 150ms`, `<= 5` lines stdout):** Reads `pre_shard_manifest.json` (`shards` + `waves`) and checks compiled `work/templates/<CID>.json` + `.check_attempts/compile_shard_*.json` to print a crystal-clear `<= 5`-line summary of `completed / pending / circuit-broken` shards per wave.

### 2. Universal Director Context Diet (`pointer: bool = True` Default + `stdout <= 1.5 KB` Cap)
- In `dispatch.py`:
  - Change default `pointer: bool = True` in `dispatch_cta()`, `dispatch_authors()`, and `dispatch_judges()` (while supporting `pointer=False` in Python and `--no-pointer` in CLI `dispatch.py` / `run.py`).
  - Ensure `work/dispatch/items/<unit>.json` ALWAYS stores the full rich work-order context (competencies, DSL reference, compile command, source files, etc.) so workers have 100% of required info in 1 `view_file` call, while the `Prompt` string in `Subagents` (returned to the Director) is a ultra-compact pointer (`~350–600 bytes`).
- In `run.py`:
  - Cap `stdout` of stage runners (`prepare`, `bootstrap`, `define-types`, `dispatch-cta`, `cta`, `plan-shards`, `dispatch-authors`, `templates`, `judge-generate`, `dispatch-judges`, `judge-compare`, `publish`) at `<= 1,500 bytes` (`1.5 KB`), persisting full verbose output/tables to `work/logs/<stage>.log` and referencing the log path if truncated.

### 3. Auto-Resolution of `.venv/Scripts/python.exe` + `PYTHONPATH`, `--append` CTA Injection & `ROLE_SPECS` Hardening (`dispatch.py`)
- Add helper `_resolve_repo_python_and_env()` in `dispatch.py`:
  - Automatically locate `<repo_root>/.venv/Scripts/python.exe` (Windows) or `<repo_root>/.venv/bin/python` (POSIX), falling back to `Path(sys.executable).as_posix()` if `.venv` doesn't exist.
  - Format all generated `compile_cmd` strings (`cta`, `author`, `repair`) using explicit POSIX-slashed `.venv` python executable + clean PowerShell/cross-platform invocation (no `ModuleNotFoundError` on `pymupdf` or `src.validator`), e.g. setting `$env:PYTHONPATH="<repo_root>"; & "<venv_python>" "<script_posix>" ...` on Windows (or clean `python` invocation that works reliably in PowerShell without nested quote traps) AND ensuring `compile_shard.py` / `compile_cta.py` themselves also ensure `REPO_ROOT` is on `sys.path`.
- **`--append` Delta Context in `dispatch_cta()`:**
  - When `work/delta_manifest.json` (or `pre_cta_manifest.json["delta"]`) exists, inject `next_ids_by_prefix` (`H`, `C`, `Hab`) AND `existing_competencies_outline` (`[{id, type, name}]`) directly into the CTA work order (`work/dispatch/items/part_XX.json` / single CTA order) with explicit instructions to start numbering at `next_ids_by_prefix` and NEVER duplicate existing base competencies.
- **`ROLE_SPECS` Isolation:**
  - Move `compile_shard.py` from `read` (if present) into `forbidden` in `ROLE_SPECS["author"]` and `ROLE_SPECS["repair"]`, and explicitly list `work/shards/shard_fixes/<CID>.py` in allowed `write` paths for `author` and `repair`.

### 4. Coherent Blind Judges, Cryptographic Option Shuffle (`crc32`), Wave Filtering & Judge Streaming (`dispatch.py` + `judge.py`)
- **Coherent Blind Judge Pointer (`dispatch.py`):**
  - In `dispatch_judges(pointer=True)`, set allowed `READ` explicitly to `[work/dispatch/items/judge_XX.json]` (POSIX path) and **REMOVE** any contradictory `"NO EJECUTES view_file"` text inside `judge_XX.json` (replace with `"PROHIBIDO leer cualquier archivo del curso, templates, shards o ground truth distinto de este lote asignado work/dispatch/items/judge_XX.json"`).
- **Cryptographic Per-Item Option Shuffle (`judge.py`):**
  - In `generate_judge_batch()`, keep `seed` for `execute_sandbox_instance(...)`, and compute deterministic per-item shuffle seed:
    `option_shuffle_seed = zlib.crc32(f"{template_id}:{inst_idx}:{seed}".encode("utf-8")) & 0xFFFFFFFF`
    passing `seed=option_shuffle_seed` to `assemble_question(..., seed=option_shuffle_seed)` so correct letters `A..G` distribute uniformly across every judge batch instead of clustering on `B` or `C`!
- **Wave Dispatch & Incremental Judge Streaming (`dispatch.py` + `judge.py` + `run.py`):**
  - Support `--wave <int>` (`wave_index: Optional[int] = None`) in `dispatch_authors()` and `run.py --stage dispatch-authors --wave <k>` so the Director dispatches at most `<= 10` authors per wave (`Wave 1` = isolated `Hab-*` skills first!).
  - Support `--ready-only` / `ready_only: bool = False` (or `--partial`) in `generate_judge_batch()` and `dispatch_judges()` so already-validated shards/competencies can stream to Blind Judges incrementally without failing on not-yet-compiled shards from a later wave, recording evaluated competency IDs cleanly so subsequent batches don't re-judge already-passed items unless requested.

## Verification Suite (`tests/test_bootstrap_and_wave_streaming.py`)
Write comprehensive unit/integration tests (all using `tmp_path`!) covering:
1. `run.py --stage bootstrap` end-to-end on synthetic multi-PDF input (`< 3s`, zero PNGs, writes `types/*.json` lean specs, pointer `cta_work_orders.json`, active `.c2c_subagent_lock.json` matching `c2c_hook_guard.py`, `stdout <= 1500` bytes, and `unlock` cleans lockfile).
2. `pointer=True` default across `dispatch_cta`, `dispatch_authors`, `dispatch_judges` + `--no-pointer` backward compatibility.
3. `.venv` Python auto-resolution + `delta_manifest.json` (`next_ids_by_prefix` & `existing_competencies_outline`) injection in `dispatch_cta` + `compile_shard.py` in `ROLE_SPECS` `forbidden`.
4. `dispatch_authors --wave 1` vs `--wave 2` filtering + `run.py --stage wave-status`.
5. `judge.py` `crc32` per-item option shuffle producing uniform distribution across `A..G` (no single letter `> 35%` across 35+ MC7 items) + coherent `judge_XX.json` pointer instructions + `--ready-only` incremental judge batching.

Run `.venv\Scripts\python.exe -m pytest` on your new suite AND existing `dispatch`/`judge`/`run` tests, write `progress.md` and `handoff.md` in `stream_2a_impl/`, and `send_message` `DONE:: stream_2a_impl | ...` to `d0ce22db-904e-4856-b353-59975bfb5874`.
