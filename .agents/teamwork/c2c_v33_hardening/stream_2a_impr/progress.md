# Stream 2A Improver Progress (`impr_2a`)

- **Role:** Principal Engineering Improver (`Phase 2 of 3: Mejorador`)
- **Stream:** 2A (Pipeline Orchestration, Subagent Dispatch, Blind Judge Streaming & Hook Guard Compatibility)
- **Orchestrator Conversation ID:** `d0ce22db-904e-4856-b353-59975bfb5874`
- **Date:** 2026-10-24
- **Status:** COMPLETED — 100% Tests GREEN (107/107 passed)

---

## Completed Improvements & Hardening Tasks

### 1. Cross-Stream `compile_cmd` vs `c2c_hook_guard.py` (`PYTHON_EXEC_PATTERN`)
- **Identified Blocker:** Implementer prefixed Windows commands with `$env:PYTHONPATH="..."; & "..."`. `PYTHON_EXEC_PATTERN` in `c2c_hook_guard.py` expects commands starting with `(?:&|call)?\s*["']...python.exe["']`. The prefix caused `PYTHON_EXEC_PATTERN.match(cmd)` to fail. When course directory paths contained shell inspection tokens (e.g. `type`, `cat`, `more`, `head`, `copy`), `c2c_hook_guard.py` falsely denied valid compiler executions.
- **Resolution:**
  - In `dispatch.py`: updated `_resolve_repo_python_and_env()` to return `& "<py_exe>"` on Windows and `"<py_exe>"` on POSIX without `$env:PYTHONPATH=...;` prefix.
  - Updated all compiler command builders in `dispatch_cta`, `dispatch_authors`, `cta-reduce`, and `role="repair"` to use `.venv` `cmd_prefix`.
  - Added adversarial test `test_compile_cmd_hook_guard_cross_stream_compatibility` in `test_bootstrap_and_wave_streaming.py` asserting `process_hook` returns `{"decision": "allow"}` under an active worker lockfile with course slug containing `course_type_cat_test`.

### 2. Valid Parseable JSON Under 1,500 Bytes in `bootstrap` & `dispatch-*` (`run.py`)
- **Identified Failure Mode:** With 6 CTA mapreduce parts or 10 author shards, indented JSON exceeded `1,450` bytes. Slicing stdout mid-string via `cap_stdout_to_log` broke `json.loads(stdout)`.
- **Resolution:**
  - Implemented `format_compact_json_stdout(payload, work_dir, stage_name, work_orders_file, max_bytes=1450)` in `run.py`.
  - Cascades gracefully: `indent=2` -> compact separators `(',', ':')` -> structured compact summary referencing disk work orders and stage logs.
  - Updated `run_stage_bootstrap`, `run_stage_dispatch_cta`, `run_stage_dispatch_authors`, and `run_stage_dispatch_judges` to emit their payload via `format_compact_json_stdout`.
  - Added adversarial test `test_valid_parseable_json_under_1500_bytes_under_heavy_load` verifying that console stdout is BOTH `<= 1,500` bytes AND 100% valid JSON (`json.loads(stdout)` succeeds) for 6 CTA parts, 10 wave shards, and 10 judge batches.

### 3. `bootstrap --append` and `--base-course` End-to-End Forwarding (`run.py`)
- **Identified Gap:** CLI and runner lacked clean `--base-course` support to forward existing course outlines to `prepare_course` and `dispatch_cta` in a single bootstrap command.
- **Resolution:**
  - Added `base_course` parameter to `PipelineRunner.__init__` and `--base-course` to CLI parser in `run.py`.
  - When `--base-course` or `--append` is supplied, `run_stage_prepare` cleanly forwards delta flags to `prepare_course`, injecting `next_ids_by_prefix` and `existing_competencies_outline` into `delta_manifest.json` and `pre_cta_manifest.json["delta"]`.
  - `dispatch_cta` automatically consumes the delta manifest, injecting non-overlapping start IDs into work order JSON and anti-duplication warnings into prompts.
  - Added adversarial test `test_bootstrap_append_end_to_end_forwarding`.

### 4. `judge.py` SHA-256 Incremental Streaming & Repair Dispatch Isolation
- **Identified Failure Mode:** `evaluated_competencies.json` only recorded competency IDs. If a template failed blind judge and was repaired, `--ready-only` would skip it because the ID was already marked as evaluated.
- **Resolution:**
  - In `judge.py`: added SHA-256 calculation for templates in `_load_templates`.
  - In `generate_judge_batch`: recorded `competency_hashes: {cid: template_sha256}` alongside `evaluated_competency_ids`.
  - When `--ready-only` runs, it checks whether `saved_hashes[cid] == current_hash`. Unchanged templates are skipped, but **modified/repaired templates are automatically re-evaluated**.
  - In `dispatch.py` for `role="repair"`: updated `compile_cmd` to `.venv`, added `compile_shard.py` to `forbidden_paths`, excluded it from `read_paths`, and added `work/shards/shard_fixes/<CID>.py` to allowed write paths and prompt instructions.
  - Cleaned up stale split batches in `work/verification/` to ensure fresh slicing on new batch generations.
  - Added adversarial test `test_judge_streaming_sha256_re_evaluation_on_repair_and_wave_isolation`.
