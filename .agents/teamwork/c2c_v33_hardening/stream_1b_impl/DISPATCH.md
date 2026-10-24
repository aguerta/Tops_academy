# DISPATCH: Stream 1B — Implementer (`impl_1b`)

- **Orchestrator Conversation ID (`Recipient` for `send_message`):** `d0ce22db-904e-4856-b353-59975bfb5874`
- **Teamwork Directory:** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1b_impl`
- **Role:** `Phase 1 Implementador — Stream 1B (Hardening de compile_shard.py y check_templates.py)`

## 1. Strict Write Boundaries (ONLY touch these files + your Teamwork Directory)
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/compile_shard.py`
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/check_templates.py`
- `d:/Augusto/personal_portfolio/Tops_academy/tests/test_shard_compiler_hardening.py` *(new)*
- `d:/Augusto/personal_portfolio/Tops_academy/tests/test_compile_shard.py` *(authorized Tier A update ONLY for `TestBoundedCompilation` lines 102–124 to reflect the v3.3 unified SHA-256 circuit breaker contract; preserve `TestStatefulSHA256CircuitBreaker` [standalone `check_templates_file_or_dir`] and `TestAdaptiveShardSizing` untouched!)*
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1b_impl/{BRIEFING.md,progress.md,handoff.md}`

*(Note: `compile_shard.py` already has pre-existing Case 2B edits in the working tree—preserve all Case 2B mastery rules! Do NOT touch `engine/*`, `plan_shards.py`, `run.py`, or `dispatch.py`.)*

## 2. Technical Specifications
1. **Step 0 Pre-Flight Sanity Check:**
   - Read `compile_shard.py`, `check_templates.py` (around circuit breaker `.check_attempts`, `TPL-VAR`/`TPL-COLLAPSE`, `R-16`, `TPL-DRY`), `tests/test_compile_shard.py`, and `tests/test_c2c_case_2b_mastery.py`. Document findings in `BRIEFING.md`. Escalate via `BLOCKER::` if any hard conflict blocks your order.
2. **Unified SHA-256 Intelligent Circuit Breaker (`compile_shard.py` + `check_templates.py`):**
   - Replace the blind monotonic `[COMPILE n/6]` counter in `compile_shard.py` with a unified state file in `.check_attempts/compile_{norm_shard_id}.json` tracking:
     `{"distinct_compiles": int, "same_error_streak": int, "last_source_sha256": str, "last_err_hash": str, "last_errors": list}`
     where `source_sha256` hashes `shard_XX_data.py` PLUS any existing modular override files in `<work_dir>/shards/shard_fixes/*.py` relevant to that shard.
   - **Idempotent `[NO-CHANGE]` Re-Run:** If `source_sha256 == last_source_sha256` and the previous attempt failed, do NOT increment `distinct_compiles` or `same_error_streak`—return the cached errors prefixed with `[NO-CHANGE: código idéntico al intento previo; edita el archivo antes de recompilar]`.
   - **Dual Calibrated Halt Thresholds:** Trigger `CIRCUIT BREAKER HALT` (`STOP, send_message the Director`) ONLY when `same_error_streak >= 3` (3 consecutive distinct compiles producing the exact same `err_hash`) **OR** `distinct_compiles > 10`. Ensure `check_templates.py`'s internal `.check_attempts` logic does not prematurely halt at 3 attempts when errors are evolving productively during a `compile_shard.py` run! Reset state cleanly on `PASS`.
3. **Zero-Disk-Mutation on Failed Compiles (`compile_shard.py`):**
   - Currently `heal_shard_source_file()` overwrites `shard_XX_data.py` on disk BEFORE compilation/validation finishes—so when validation fails, the author's next `edit_file` fails with `Target Mismatch`!
   - Refactor `heal_shard_source_file` / module loading in `compile_shard.py` so healing happens **in-memory** (or in an internal staging file `.check_attempts/_staged/<shard_id>_data.py`), NEVER modifying `shard_XX_data.py` on disk when compilation or validation fails! (Even on `PASS`, prefer leaving `shard_XX_data.py` untouched on disk while emitting the healed code into the compiled JSON templates so `shard_XX_data.py` always matches what the author wrote!).
4. **Modular Competency Splicing (`<work_dir>/shards/shard_fixes/<CID>.py`):**
   - Allow an author or `c2c_repair` subagent to write `<work_dir>/shards/shard_fixes/<CID>.py` (e.g. `Hab-03.py` or `C-08.py`) containing `TEMPLATES = [...]` (plus helper `gen_*` / `ver_*` functions) for a single competency `<CID>`.
   - When `compile_shard.py` compiles a shard, discover any matching `<CID>.py` files in `<work_dir>/shards/shard_fixes/` (matching `CID` or normalized `CID.replace('-', '_')`), load them with the same in-memory healing, and **replace all tuples for `<CID>` from `shard_XX_data.py` with the tuples from `shard_fixes/<CID>.py`** (or allow compiling a shard solely from `shard_fixes/<CID>.py` if `shard_XX_data.py` lacks `<CID>`).
   - Ensure error line numbers for `<CID>` point accurately to `shard_fixes/<CID>.py:L<n>`!
5. **Surgical Diagnostics (`TPL-VAR / TPL-COLLAPSE`, `R-16`, `[TPL-DRY]`, Unrendered Placeholders, `rf"{{{` Warning):**
   - **AST Warning on `rf"..."` + `{{{`:** If source contains `rf"..."` / `fr"..."` with `{{{`, include a clear hint recommending raw strings `r"..."` with `@var@` tokens.
   - **Unrendered Placeholders Check:** During dry-run in `check_templates.py`, reject any rendered stem/option/answer/hint/solution that still contains `@[A-Za-z_][A-Za-z0-9_]*(?::[^@\s{}]+)?@` OR an uninterpolated `{key}` where `key` is a variable name in `gen_res["vars"]` (or bare `{ident}` placeholder in prose, without false-flagging valid LaTeX like `\frac{a}{b}`, `x_{i}`, `\text{...}`).
   - **`TPL-VAR / TPL-COLLAPSE`:** Include the exact failing `seed`, the colliding option values (`opt_X == opt_Y == '...'`), which `vars` keys stayed constant across seeds, and remind the author to provide 3–5 `stem_variants` with `@var@`.
   - **`R-16` Option Length Parity:** Report exact character counts and ratio: `len(correct)=<L_c> vs avg(distractors)=<L_d> (ratio=<r:.2f>x, rango permitido=[0.65x, 1.35x])` plus individual distractor lengths.
   - **`[TPL-DRY]` Traceback:** Map runtime sandbox errors back to the exact generator/verifier function name, `seed`, and line number in `shard_XX_data.py` (or `shard_fixes/<CID>.py`), stripping internal `compile_shard.py` / `engine/` stack frames.

## 3. Required Tests & Verification
- Create `tests/test_shard_compiler_hardening.py` testing all 5 features above thoroughly.
- Run `& "d:\Augusto\personal_portfolio\Tops_academy\.venv\Scripts\python.exe" -m pytest tests/test_shard_compiler_hardening.py tests/test_compile_shard.py tests/test_c2c_case_2b_mastery.py -q` and ensure 100% pass rate!
