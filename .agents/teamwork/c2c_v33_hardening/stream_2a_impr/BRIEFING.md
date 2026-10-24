# Stream 2A Improver Briefing (`impr_2a`)

- **Role:** Principal Engineering Improver (`Phase 2 of 3: Mejorador`)
- **Stream:** 2A (Pipeline Orchestration, Subagent Dispatch, Blind Judge Streaming & Hook Guard Compatibility)
- **Orchestrator Conversation ID:** `d0ce22db-904e-4856-b353-59975bfb5874`
- **Date:** 2026-10-24
- **Implementer Review Status:** COMPLETE with Critical Hardening Areas Identified

---

## 1. Implementer Review & Architectural Scrutiny

The Implementer (`stream_2a_impl`) successfully landed the core architecture:
- `PipelineRunner` with atomic `run_stage_bootstrap`, `run_stage_unlock`, and `run_stage_wave_status`.
- Universal Context Diet with `pointer=True` default across `dispatch_cta`, `dispatch_authors`, `dispatch_judges`.
- Cryptographic `crc32` option shuffle and baseline incremental judge streaming.
- All 70 existing tests passing.

However, four critical edge cases and cross-stream contracts were identified for Phase 2 hardening:

1. **`compile_cmd` vs `c2c_hook_guard.py` (`PYTHON_EXEC_PATTERN`):**
   - Implementer prefixed Windows commands with `$env:PYTHONPATH="..."; & "..."`.
   - `c2c_hook_guard.py`'s `PYTHON_EXEC_PATTERN` expects commands to start with `(?:&|call)?\s*["']...python.exe["']`.
   - The `$env:PYTHONPATH=...` prefix caused `PYTHON_EXEC_PATTERN.match` to return `False`.
   - When a course slug or path contains shell inspection tokens (e.g. `type`, `cat`, `more`, `head`, `copy`), `c2c_hook_guard.py` would falsely deny legitimate `compile_shard.py` or `compile_cta.py` executions.
   - **Resolution:** Format `compile_cmd` cleanly as `& "<venv_python_posix>" ...` on Windows and `"<venv_python_posix>" ...` on POSIX without `$env:PYTHONPATH=...;` prefix.

2. **Valid Parseable JSON Under 1,500 Bytes in `bootstrap` & `dispatch-*` (`run.py`):**
   - With 6 CTA mapreduce parts or 10 wave shards, raw indented JSON exceeds `1,450` bytes.
   - Slicing stdout mid-string via `cap_stdout_to_log` broke `json.loads(stdout)`.
   - **Resolution:** Implement `format_compact_json_stdout` in `run.py` which cascades: `indent=2` -> `compact separators=(',', ':')` -> structured compact summary referencing disk work orders and logs. Console stdout is strictly `<= 1,500` bytes AND 100% valid JSON parseable via `json.loads(stdout)`.

3. **`bootstrap --append` End-to-End Forwarding (`run.py`):**
   - Support `--append` and `--base-course` flags in `PipelineRunner` and CLI args, ensuring `delta_manifest.json` and `pre_cta_manifest.json["delta"]` forward `next_ids_by_prefix` and `existing_competencies_outline` directly into the bootstrap CTA work order.

4. **`judge.py` Incremental Streaming & Repair Dispatch:**
   - In `judge.py`: when `ready_only=True`, track SHA-256 hashes in `evaluated_competencies.json` (`competency_hashes: {cid: sha256}`). If a template is modified/repaired, it is automatically re-evaluated while unchanged templates remain skipped.
   - In `dispatch.py` for `role="repair"`: use `.venv` `compile_cmd`, forbid reading `compile_shard.py`, include `work/shards/shard_fixes/<CID>.py` in allowed write paths and prompt instructions.

---

## 2. Hardening Plan

1. Edit [dispatch.py](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/dispatch.py):
   - Update `_resolve_repo_python_and_env()`: return clean `& "<venv_python_posix>"` on Windows, `"<venv_python_posix>"` on POSIX.
   - In `role == "repair"`: use `cmd_prefix`, forbid `compile_shard.py`, add `shard_fixes/<CID>.py` to write paths and instructions.
2. Edit [run.py](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/run.py):
   - Implement `format_compact_json_stdout(...)`.
   - Update `run_stage_bootstrap`, `run_stage_dispatch_cta`, `run_stage_dispatch_authors`, `run_stage_dispatch_judges` to emit compact parseable JSON.
   - Add `--base-course` CLI argument and end-to-end forwarding.
3. Edit [judge.py](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/judge.py):
   - Add template SHA-256 hashing in `_load_templates` and `generate_judge_batch`.
   - Track `competency_hashes` in `evaluated_competencies.json`.
   - Allow automatic re-evaluation of modified templates under `--ready-only`.
   - Prevent stale split batch reuse.
4. Expand [tests/test_bootstrap_and_wave_streaming.py](file:///d:/Augusto/personal_portfolio/Tops_academy/tests/test_bootstrap_and_wave_streaming.py):
   - Test `c2c_hook_guard` compatibility with course paths containing `cat`, `type`, etc.
   - Test JSON parseability <= 1500 B under 10 shards and 6 CTA parts.
   - Test `bootstrap --append` end-to-end.
   - Test SHA-256-aware incremental judge re-evaluation on template repair.
5. Execute regression test sweep across all test files in scope.
