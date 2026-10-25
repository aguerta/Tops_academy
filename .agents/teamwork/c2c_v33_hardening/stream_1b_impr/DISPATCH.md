# DISPATCH: Stream 1B — Improver (`impr_1b`)

- **Orchestrator Conversation ID (`Recipient` for `send_message`):** `d0ce22db-904e-4856-b353-59975bfb5874`
- **Teamwork Directory:** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1b_impr`
- **Implementer Handoff to Audit & Improve:** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1b_impl/handoff.md`
- **Role:** `Phase 2 Mejorador — Stream 1B (Hardening de compile_shard.py y check_templates.py)`

## 1. Strict Write Boundaries (ONLY touch these files + your Teamwork Directory)
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/compile_shard.py`
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/check_templates.py`
- `d:/Augusto/personal_portfolio/Tops_academy/tests/test_shard_compiler_hardening.py`
- `d:/Augusto/personal_portfolio/Tops_academy/tests/test_compile_shard.py` *(ONLY `TestBoundedCompilation` if needed; keep `TestStatefulSHA256CircuitBreaker` and `TestAdaptiveShardSizing` untouched!)*
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1b_impr/{BRIEFING.md,progress.md,handoff.md}`

*(Put any helper scripts inside `stream_1b_impr/` if needed—NEVER leave temporary `.py` scripts in repository root!)*

## 2. Hardening & Scrutiny Objectives
1. Read `stream_1b_impl/handoff.md`, `stream_1b_impl/BRIEFING.md`, and inspect the diffs in `compile_shard.py`, `check_templates.py`, `tests/test_shard_compiler_hardening.py`, and `tests/test_compile_shard.py`.
2. Scrutinize & harden critical edge cases:
   - **Zero-Disk-Mutation Guarantee Under ALL Failure Paths:**
     - Verify byte-for-byte SHA-256 identity of `shard_XX_data.py` before and after `compile_shard()` on: (a) Python `SyntaxError`, (b) runtime `ZeroDivisionError` in generator, (c) `R-20` KaTeX failure, (d) `R-16` parity failure, and (e) `TPL-VAR / TPL-COLLAPSE` failure, including CRLF (`\r\n`) files on Windows!
   - **Modular Competency Splicing (`shard_fixes/<CID>.py`) Edge Cases:**
     - What if `shard_06_data.py` has a **Python `SyntaxError`** on line 600 (inside `Hab-04`), or doesn't even exist yet because `c2c_repair` is writing `shard_fixes/Hab-03.py` and `shard_fixes/Hab-04.py` cleanly? Verify `compile_shard.py` handles:
       1. `shard_06_data.py` valid + `shard_fixes/Hab-04.py` overriding `Hab-04`.
       2. `shard_fixes/Hab-03.py` + `shard_fixes/Hab-04.py` covering 100% of shard competencies even when `shard_06_data.py` is missing or broken! (That makes `c2c_repair` rescue bulletproof even if the aborted author left a half-written `SyntaxError` in `shard_06_data.py`!).
       3. Filename normalization: both `Hab-03.py` and `Hab_03.py` (or lowercase `hab-03.py`) matched unambiguously to competency `Hab-03`.
       4. `sys.modules` cache safety: ensure repeated `compile_shard()` calls in the same Python process (such as `run.py` or `pytest`) don't serve stale cached `shard_fixes` modules!
   - **Circuit Breaker Edge Cases:**
     - Ensure volatile fields (like timestamps or temp paths) are stripped before computing `err_hash`, so two compiles with the exact same semantic error actually produce the **exact same `err_hash`** and trip at `same_error_streak == 3`!
     - Ensure atomic writes (`temp -> os.replace`) on `.check_attempts/compile_{norm_shard_id}.json`.
   - **PrairieLearn `@var@` Compatibility in `check_templates.py` Early Variability Check:**
     - Check lines ~1999–2070 of `check_templates.py`! Does `check_templates.py` have an early static regex check requiring `{var}` braces in `stem` to verify placeholder presence (`has_placeholders`)?!
     - **CRITICAL CHECK:** If an author writes a pure `@var@` template (`r"Calcule $\frac{@a@}{@b@}$"` with ZERO `{...}` braces!), make sure `check_templates.py`'s static placeholder detector recognizes `@var@` / `@var:fmt@` tokens as valid variable placeholders and does NOT falsely reject pure `@var@` templates for "missing `{var}` placeholders"!! Test this explicitly in `tests/test_shard_compiler_hardening.py`!
   - **Single-Letter `vars` vs LaTeX Braces in Placeholder Leak Detector:**
     - Ensure `vars = {"n": 100, "d": 4, "a": 2, "b": 5}` alongside `\xrightarrow{d}`, `\frac{a}{b}`, `x_{n}` does NOT false-positive in `check_templates.py`, while genuine leaked `"tol <= {delta}"` or `"@delta@"` IS caught!
3. Run `& "d:\Augusto\personal_portfolio\Tops_academy\.venv\Scripts\python.exe" -m pytest tests/test_shard_compiler_hardening.py tests/test_compile_shard.py tests/test_c2c_case_2b_mastery.py -q`.
4. Write `BRIEFING.md`, `progress.md`, and `handoff.md`, then `send_message` starting with `DONE:: stream_1b_impr`.
