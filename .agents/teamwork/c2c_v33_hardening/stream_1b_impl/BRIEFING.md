# STEP 0 PRE-FLIGHT BRIEFING: Stream 1B — Implementer

- **Agent:** Phase 1 Implementador — Stream 1B (`impl_1b`)
- **Date:** 2026-10-24
- **Working Tree:** Windows (`d:\Augusto\personal_portfolio\Tops_academy`)
- **Assigned Boundaries:**
  - `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/compile_shard.py`
  - `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/check_templates.py`
  - `d:/Augusto/personal_portfolio/Tops_academy/tests/test_shard_compiler_hardening.py`
  - `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1b_impl/{BRIEFING.md,progress.md,handoff.md}`

---

## 1. Pre-Flight Verification of Existing Codebase

### A. `compile_shard.py` (1122 lines)
- **Pre-existing Case 2B logic:** Lines 810-1035 group templates by competency `templates_by_cid: Dict[str, List[Dict[str, Any]]]`, disambiguate template IDs (`T-{cid}-01..04`), handle multi-template container JSON structures (`{"competency_id": cid, "templates": tpls}`), and preserve all Case 2B mastery rules.
- **Disk mutation:** Line 740 calls `heal_shard_source_file(shard_data_path)` before parsing. Lines 60-106 in `heal_shard_source_file()` write healed tokens back to `py_path` on disk. When validation subsequently fails, the disk file has changed, causing author `edit_file` target mismatches.
- **Compilation counter:** Lines 661-694 implement the blind monotonic counter tracking `count` in `.check_attempts/compile_{norm_shard_id}.json` up to 6 (`[COMPILE {count}/6]`), halting when `compile_count > 6`.
- **Module loading:** Lines 749-756 dynamically load `shard_data_path` using `importlib.util.spec_from_file_location`.

### B. `check_templates.py` (2815 lines)
- **Circuit breaker logic:** Lines 2536-2708 track attempts in `.check_attempts/circuit_breaker_{scope_key}.json` (consecutive error hashes) and `.check_attempts/{shard_id}_{cid}.json` (per-competency SHA-256 source hash).
- **Diagnostics:** Lines 749-890 implement `_format_dry_failure()`. Lines 1274-1320 and 1530-1580 implement `format_invariant_error_diagnostic()` and `format_parity_error()`.
- **TPL-VAR & Diversity:** Lines 1999-2070 enforce early variability checks (empty `vars`, missing placeholders/`stem_variants`, < 4 unique instances). Lines 2074-2225 simulate competency diversity (`check_competency_diversity`).

### C. Existing Test Suites
- Executed: `& "d:\Augusto\personal_portfolio\Tops_academy\.venv\Scripts\python.exe" -m pytest tests/test_compile_shard.py tests/test_c2c_case_2b_mastery.py -q`
- Result: **17 passed in 3.34s** (100% clean baseline).

---

## 2. Technical Conflict Analysis & Escalation Point (`tests/test_compile_shard.py`)

A direct technical conflict exists between `DISPATCH.md` Specification 2 and existing test assertions in `tests/test_compile_shard.py:102-124`:

1. **`tests/test_compile_shard.py:102-124` (`test_compile_counter_increments_and_halts_at_limit`):**
   ```python
   for attempt in range(1, 7):
       success, errors = compile_shard(work_dir, shard_id="shard_01", strict=False)
       assert not success
       captured = capsys.readouterr()
       assert f"[COMPILE {attempt}/6]" in captured.out or f"[COMPILE {attempt}/6]" in captured.err
       if attempt == 6:
           assert "STOP, send_message the Director" in captured.err or any("STOP, send_message the Director" in e for e in errors)
   ```
2. **`DISPATCH.md` Specification 2 Requirements:**
   - Unified state file tracking `{"distinct_compiles": int, "same_error_streak": int, "last_source_sha256": str, "last_err_hash": str, "last_errors": list}`.
   - **Idempotent `[NO-CHANGE]` Re-Run:** If `source_sha256 == last_source_sha256` and the previous attempt failed, do NOT increment `distinct_compiles` or `same_error_streak`—return cached errors prefixed with `[NO-CHANGE: ...]`.
   - **Dual Calibrated Halt Thresholds:** Halt ONLY when `same_error_streak >= 3` OR `distinct_compiles > 10`.
3. **The Conflict:**
   - In `test_compile_shard.py`, the loop runs 6 times on unchanged code `TEMPLATES = 'broken'\n`.
   - If `[NO-CHANGE]` idempotency is active, attempt 2 will NOT increment or print `[COMPILE 2/6]`, causing `assert f"[COMPILE {attempt}/6]"` to fail immediately on attempt 2.
   - If the counter limit is 10 (`[COMPILE n/10]`), the format assertion `f"[COMPILE {attempt}/6]"` fails.
   - If halt is at 10 or `same_error_streak >= 3`, the halt at attempt 6 assertion fails.
   - `DISPATCH.md` prohibits modifying `tests/test_compile_shard.py` ("Do NOT touch `engine/*`, `plan_shards.py`, `run.py`, `dispatch.py`, or `tests/test_compile_shard.py`").

---

## 3. Implementation Plan (Pending Orchestrator Resolution)

1. **Intelligent Circuit Breaker (`compile_shard.py` + `check_templates.py`):**
   - Store state in `.check_attempts/compile_{norm_shard_id}.json`.
   - Hash `shard_XX_data.py` plus all relevant `shards/shard_fixes/*.py`.
   - Maintain backward compatibility with legacy `{"count": int}` format while supporting `distinct_compiles`, `same_error_streak`, `last_source_sha256`, `last_err_hash`.
2. **Zero-Disk-Mutation (`compile_shard.py`):**
   - Refactor `heal_shard_source_file` to perform in-memory healing or write to staged files under `.check_attempts/_staged/`.
   - Never overwrite `shard_XX_data.py` on disk during compilation.
3. **Modular Competency Splicing (`shards/shard_fixes/<CID>.py`):**
   - Discover matching fix files in `<work_dir>/shards/shard_fixes/` for expected competencies.
   - Replace or inject competency tuples into `raw_templates`.
   - Map diagnostic line numbers directly to `shard_fixes/<CID>.py:L<n>`.
4. **Surgical Diagnostics:**
   - Warning on `rf"..."` / `fr"..."` with `{{{`.
   - Dry-run validation rejecting unrendered `@...tokens...@` and un-interpolated `{vars}` without false-flagging valid LaTeX (`\frac{a}{b}`, `x_{i}`).
   - Enhanced `TPL-VAR / TPL-COLLAPSE` reporting failing seeds, colliding options, invariant variables.
   - Enhanced `R-16` reporting length ratios `len(correct)` vs `avg(distractors)` and distractor lengths.
   - Mapped `[TPL-DRY]` traceback frames.
5. **New Test Suite (`tests/test_shard_compiler_hardening.py`):**
   - Rigorous unit tests covering all 5 features.
