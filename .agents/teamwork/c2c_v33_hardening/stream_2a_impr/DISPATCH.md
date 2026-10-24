# DISPATCH: Stream 2A — Improver (`impr_2a`)

- **Orchestrator Conversation ID (`Recipient` for `send_message`):** `d0ce22db-904e-4856-b353-59975bfb5874`
- **Teamwork Directory (Governance Docs):** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_2a_impr`
- **Implementer Handoff to Review:** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_2a_impl/handoff.md`
- **Exclusive Production/Test Write Boundaries:**
  1. `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/run.py`
  2. `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/dispatch.py`
  3. `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/judge.py`
  4. `d:/Augusto/personal_portfolio/Tops_academy/tests/test_bootstrap_and_wave_streaming.py`
  5. `d:/Augusto/personal_portfolio/Tops_academy/tests/test_c2c_v321_comp3_dispatch.py`
  6. `d:/Augusto/personal_portfolio/Tops_academy/tests/test_pipeline_reparations.py` *(`TestAuthorDispatchAndProtocol` only)*
  7. `d:/Augusto/personal_portfolio/Tops_academy/tests/test_dispatch_scope.py`
  8. `d:/Augusto/personal_portfolio/Tops_academy/tests/test_c2c_v31_adversarial_plan.py`

> **CRITICAL RULES:**
> - **DO NOT** modify any file outside the 8 files above + `stream_2a_impr/*.md`.
> - **NEVER** pass `ArtifactMetadata` when calling `write_file` or `edit_file`.
> - **NEVER** leave temporary `.py` scripts in repo root or leave `.c2c_subagent_lock.json` inside `REPO_ROOT/courses/*` (always use `tmp_path`!).

## High-Value Adversarial Hardening Checklist

1. **CRITICAL Cross-Stream Contract — `compile_cmd` vs `c2c_hook_guard.py` (`PYTHON_EXEC_PATTERN`):**
   - Inspect `_resolve_repo_python_and_env()` in `dispatch.py` and `PYTHON_EXEC_PATTERN` in `c2c_hook_guard.py` (lines 83–90, 320–332, READ-ONLY on `c2c_hook_guard.py`!).
   - Notice: in `c2c_hook_guard.py`, `PYTHON_EXEC_PATTERN` expects commands starting with `(?:&|call)?\s*["']...python.exe["']` (`^\s*(?:&|call)?...`)! If `compile_cmd` starts with `$env:PYTHONPATH="..."; & "...python.exe"`, `PYTHON_EXEC_PATTERN.match(cmd)` returns `False`, which will cause `c2c_hook_guard.py` to FALSELY DENY `compile_shard.py` or `compile_cta.py` whenever a course path/slug contains words like `type`, `cat`, `more`, `head`, or `copy`!
   - Furthermore, both `compile_shard.py` and `compile_cta.py` ALREADY add `.agents/skills/content-to-course` and `REPO_ROOT` to `sys.path` internally, and `.venv/Scripts/python.exe` already has `site-packages` (`pymupdf`, etc.)!
   - **Fix:** Format `compile_cmd` cleanly as `& "<venv_python_posix>" "<script_posix>" ...` on Windows (and `"<venv_python_posix>" "<script_posix>" ...` on POSIX) WITHOUT `$env:PYTHONPATH=...;` prefix so `PYTHON_EXEC_PATTERN` matches 100% natively! Add an explicit test in `test_bootstrap_and_wave_streaming.py` passing the generated `compile_cmd` (including a work_dir containing `/course_type_cat_test/`) into `c2c_hook_guard.process_hook(...)` with an active worker lockfile and asserting `{"decision": "allow"}`!

2. **Valid Parseable JSON Under `1,500` Bytes in `bootstrap` & `dispatch-*` (`run.py`):**
   - Inspect how `cap_stdout_to_log` interacts with JSON-emitting stages (`bootstrap`, `dispatch-cta`, `dispatch-authors`, `dispatch-judges`).
   - If `bootstrap` has e.g. 6 map-reduce CTA parts or `dispatch-authors --wave 1` has 10 shards, raw `json.dumps(..., indent=2)` might be `1,800–2,800` bytes; if `cap_stdout_to_log` slices mid-string (`head + ... + tail`), `json.loads(stdout)` breaks!
   - **Fix:** Ensure `bootstrap` and `dispatch-*` serialize their stdout JSON compactly (`separators=(",", ":")` when `indent=2` would exceed `1,450` bytes, and if still `> 1,450` bytes, emit a valid compact JSON summary pointing to `work/dispatch/<role>_work_orders.json` + `work/logs/<stage>.log`) so `stdout` is **BOTH `<= 1,500` bytes AND 100% valid JSON (`json.loads(stdout)` succeeds)** even for 6 CTA parts or 10 wave shards! Keep `cap_stdout_to_log` as the outer safety net for verbose text stages. Add a test with 10 shards / 6 CTA parts proving `len(stdout.encode("utf-8")) <= 1500` AND `json.loads(stdout)` succeeds!

3. **`bootstrap --append` End-to-End Forwarding (`run.py`):**
   - Verify `run.py --stage bootstrap --append` (or `--base-course`) forwards delta flags cleanly to `prepare_course` and `dispatch_cta`, injecting `next_ids_by_prefix` & `existing_competencies_outline` into the bootstrap CTA work order in a single command! Add a test verifying `bootstrap --append`.

4. **`judge.py` Incremental Streaming Edge Cases (`--ready-only`) & `repair` Dispatch:**
   - Check what happens when `generate_judge_batch(..., ready_only=True)` is called when:
     (a) Wave 1 (`10` competencies) is compiled in `work/templates/`, while Wave 2 (`12` competencies) is not yet compiled -> must generate judge batch ONLY for the 10 compiled competencies without crashing on missing Wave 2 templates!
     (b) A competency fails Blind Judge and is repaired (`templates/<CID>.json` has a newer `mtime` or SHA-256 hash than when `evaluated_competencies.json` recorded it!) -> `evaluated_competencies.json` should store `{cid: template_sha256}` so unchanged passed templates are skipped in Wave 2 `--ready-only`, while **newly repaired/updated templates ARE automatically re-evaluated**!
   - Check `dispatch.py --role repair` (`dispatch_repair` / `build_dispatch(role="repair")`) to verify repair work orders ALSO use `.venv` `compile_cmd`, forbid reading `compile_shard.py`, and instruct writing modular fixes to `work/shards/shard_fixes/<CID>.py`!

Run `& "d:\Augusto\personal_portfolio\Tops_academy\.venv\Scripts\python.exe" -m pytest tests/test_bootstrap_and_wave_streaming.py tests/test_c2c_v321_comp3_dispatch.py tests/test_pipeline_reparations.py tests/test_orchestration_resilience.py tests/test_dispatch_scope.py tests/test_c2c_v31_adversarial_plan.py tests/test_skill.py -q`, write `BRIEFING.md`, `progress.md`, and `handoff.md` in `stream_2a_impr/`, and `send_message` `DONE:: stream_2a_impr | ...` to `d0ce22db-904e-4856-b353-59975bfb5874`.
