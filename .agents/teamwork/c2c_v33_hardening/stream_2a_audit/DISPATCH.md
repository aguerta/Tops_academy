# DISPATCH: Stream 2A — Forensic Auditor (`audit_2a`)

- **Orchestrator Conversation ID (`Recipient` for `send_message`):** `d0ce22db-904e-4856-b353-59975bfb5874`
- **Teamwork Directory (ONLY allowed write target):** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_2a_audit`
- **Artifacts to Audit:**
  - Original Stream Spec: `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_2a_impl/DISPATCH.md`
  - Implementer Handoff: `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_2a_impl/handoff.md`
  - Improver Spec & Handoff: `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_2a_impr/{DISPATCH.md,handoff.md}`
  - Audited Code & Tests (READ-ONLY):
    - `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/run.py`
    - `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/dispatch.py`
    - `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/judge.py`
    - `d:/Augusto/personal_portfolio/Tops_academy/tests/test_bootstrap_and_wave_streaming.py`
    - `d:/Augusto/personal_portfolio/Tops_academy/tests/test_c2c_v321_comp3_dispatch.py`
    - `d:/Augusto/personal_portfolio/Tops_academy/tests/test_pipeline_reparations.py`
    - `d:/Augusto/personal_portfolio/Tops_academy/tests/test_dispatch_scope.py`
    - `d:/Augusto/personal_portfolio/Tops_academy/tests/test_c2c_v31_adversarial_plan.py`

## Audit Checklist
1. **Boundary, Cleanliness & Lockfile Hygiene:**
   - Run `git status --short` and confirm Stream 2A modified ONLY its 8 authorized files above (ignoring Stage 1 files, Stream 2B files, and baseline pre-existing files in `ORIGINAL_REQUEST.md`).
   - Confirm **ZERO temporary `.py` scripts** in repo root AND **ZERO lingering `.c2c_subagent_lock.json` files** anywhere inside `REPO_ROOT` (`courses/*` or `work*/`).
2. **Requirement Verification (Bottlenecks #1, #5, #6, #9, #11, #13 + Cross-Stream Contracts):**
   - `run.py`:
     - `--stage bootstrap` atomically runs `prepare` (Zero-Raster) -> `generate_define_subagent_specs(..., lean=True)` (without dumping 87 KB `subagent_types.json` to stdout) -> `dispatch_cta(..., pointer=True)` -> creates `work/.c2c_subagent_lock.json` matching `c2c_hook_guard.py`'s schema (`active: True`, `director_conversation_id`, etc.) -> emits valid parseable JSON `<= 1,500` bytes on `stdout` (`format_compact_json_stdout`).
     - Supports `--append` / `--base-course` in `bootstrap`.
     - Automatically releases `.c2c_subagent_lock.json` on `publish` success and `--stage unlock` / `--unlock`.
     - `--stage wave-status` prints `<= 5` lines in `< 150ms`.
     - `cap_stdout_to_log` caps verbose text stages at `<= 1,500` bytes and writes full logs to `work/logs/<stage>.log`.
   - `dispatch.py`:
     - `pointer: bool = True` is universal default across `dispatch_cta`, `dispatch_authors`, `dispatch_judges`, and `build_dispatch` (with `--no-pointer` / `pointer=False` preserved).
     - `_resolve_repo_python_and_env()` generates `compile_cmd` matching `c2c_hook_guard.py`'s `PYTHON_EXEC_PATTERN` directly (`& "<venv_python>" "<script>"` without `$env:PYTHONPATH=...;`) for `cta`, `author`, and `repair`.
     - `dispatch_cta` injects `next_ids_by_prefix` and `existing_competencies_outline` from `delta_manifest.json` under `--append`.
     - `ROLE_SPECS["author"]` and `ROLE_SPECS["repair"]` place `compile_shard.py` in `forbidden` (NOT `read`) and `work/shards/shard_fixes/<CID>.py` in `write`.
     - `dispatch_authors` supports `--wave` / `wave_index`.
     - `dispatch_judges(pointer=True)` sets `READ permitido: [work/dispatch/items/judge_XX.json]` with ZERO contradictory `"NO EJECUTES view_file"` text.
   - `judge.py`:
     - `generate_judge_batch` uses `zlib.crc32(f"{template_id}:{inst_idx}:{seed}".encode("utf-8")) & 0xFFFFFFFF` for `assemble_question(..., seed=option_shuffle_seed)` producing uniform `A..G` letter distribution.
     - `--ready-only` incremental streaming skips unchanged evaluated templates via SHA-256 hashes while automatically re-evaluating repaired templates.
   - Zero fake mocks, zero masked/weakened assertions in `tests/test_bootstrap_and_wave_streaming.py` and the 4 modernized legacy test slices.
3. **Independent Test Execution:**
   - Run `& "d:\Augusto\personal_portfolio\Tops_academy\.venv\Scripts\python.exe" -m pytest tests/test_bootstrap_and_wave_streaming.py tests/test_c2c_v321_comp3_dispatch.py tests/test_pipeline_reparations.py tests/test_orchestration_resilience.py tests/test_dispatch_scope.py tests/test_c2c_v31_adversarial_plan.py tests/test_skill.py -q`.
4. Write `BRIEFING.md`, `progress.md`, and `handoff.md` inside `stream_2a_audit/`, then `send_message` starting with `PASS:: stream_2a_audit | ...` or `REJECT:: stream_2a_audit | ...`.
