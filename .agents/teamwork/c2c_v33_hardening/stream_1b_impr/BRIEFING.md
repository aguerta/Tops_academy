# STEP 0 PRE-FLIGHT BRIEFING: Stream 1B — Improver (`impr_1b`)

- **Agent:** Phase 2 Mejorador — Stream 1B (`impr_1b`)
- **Recipient:** Orchestrator (`d0ce22db-904e-4856-b353-59975bfb5874`) & Phase 3 Auditor
- **Date:** 2026-10-24
- **Working Tree:** Windows (`d:\Augusto\personal_portfolio\Tops_academy`)
- **Assigned Boundaries:**
  - `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/compile_shard.py`
  - `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/check_templates.py`
  - `d:/Augusto/personal_portfolio/Tops_academy/tests/test_shard_compiler_hardening.py`
  - `d:/Augusto/personal_portfolio/Tops_academy/tests/test_compile_shard.py` (Tier A authorized update ONLY for `TestBoundedCompilation:102-124`)
  - Teamwork directory: `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1b_impr/{BRIEFING.md,progress.md,handoff.md}`

---

## 1. Architectural Scrutiny & Pre-Flight Audit of Implementer Deliverables

### A. Zero-Disk-Mutation Guarantee
- **Inspection:** In `compile_shard.py`, `heal_shard_source_text` is executed in-memory. Source text is staged under `.check_attempts/_staged/` and compiled dynamically via `types.ModuleType` and `compile(..., "exec")`.
- **Gap Identified:** Hardening requires adversarial unit tests verifying byte-for-byte SHA-256 identity across all 5 C2C failure modes (`SyntaxError`, runtime `ZeroDivisionError`, `R-20` KaTeX failure, `R-16` parity failure, and `TPL-VAR / TPL-COLLAPSE` failure) under Windows CRLF line endings (`\r\n`).

### B. Modular Competency Splicing & Broken Shard Recovery (`shard_fixes/<CID>.py`)
- **Inspection:** Currently, `compile_shard()` checks `locator.syntax_error` and executes `compile(healed_source, ...)` BEFORE loading `shard_fixes/`.
- **Critical Flaw:** If `shard_06_data.py` contains a Python `SyntaxError` (e.g., from an aborted author leaving half-written code on line 600) or runtime error on load, `compile_shard` immediately fails, even if `c2c_repair` has created 100% complete fix files in `shards/shard_fixes/` (`Hab-03.py` and `Hab-04.py`)!
- **Improver Hardening:**
  1. Discover fix files ahead of time with case-insensitive and delimiter-agnostic normalization (`Hab-03.py`, `Hab_03.py`, `hab-03.py`, `hab_03.py`, `T-Hab-03.py` -> `Hab-03`).
  2. If 100% of expected competencies are covered by `shard_fixes/`, bypass/tolerate syntax and runtime errors in `shard_XX_data.py` and compile cleanly from the fix files alone.
  3. Guarantee `sys.modules` and `linecache` cache safety: clear `linecache` and evict old `c2c_fix_mod_*` / `c2c_shard_mod_*` before every compilation.

### C. PrairieLearn `@var@` Static Placeholder Detection in `check_templates.py`
- **Inspection:** In `check_templates.py:2106`, `has_placeholder` only checked `r"\{[A-Za-z0-9_]+(?::[^{}]+)?\}"`.
- **Critical Flaw:** Pure `@var@` templates (e.g., `stem = r"Calcule $\frac{@a@}{@b@}$"` with zero `{...}` braces) were falsely rejected by `TPL-VAR: DIVERSIDAD DE REACTIVOS` for missing `{var}` placeholders!
- **Improver Hardening:**
  1. Update `check_templates.py:2106` to recognize `@var@` and `@var:fmt@` tokens: `re.search(r"@[A-Za-z_][A-Za-z0-9_]*(?::[^@\s{}]+)?@", stem)`.
  2. Update `_extract_template_placeholders()` to extract PrairieLearn `@var@` / `@var:fmt@` tokens for auto-exporting variables in `auto_heal_template_data()`.

### D. Volatile Fields Stripping in Circuit Breaker Error Hashing
- **Inspection:** Currently, `err_hash` only stripped `at 0x[0-9a-fA-F]+`. Volatile module names (`c2c_shard_mod_<id>_<uuid>`), timestamps, temp paths, and Windows backslashes (`\`) could cause identical semantic errors to yield different hashes.
- **Improver Hardening:** Create `normalize_error_string_for_hash(text: str)` stripping UUIDs, timestamps, temp paths, and normalizing path separators to forward slashes.

### E. Single-Letter `vars` vs LaTeX Macros
- **Inspection:** Verified `engine/invariants.py` does not flag `\frac{a}{b}`, `\xrightarrow{d}`, or `x_{n}` when `vars = {"n": 100, "d": 4, "a": 2, "b": 5}`.
- **Improver Hardening:** Add explicit adversarial tests ensuring zero false positives on LaTeX macros while catching real leaked tokens like `{delta}` and `@delta@`.

---

## 2. Hardening Execution Plan

1. **`compile_shard.py`:**
   - Implement `discover_fix_files()` with full normalization.
   - Guard against `shard_XX_data.py` `SyntaxError` / runtime errors when 100% covered by `shard_fixes/`.
   - Invalidate `linecache` and prune `sys.modules` for cache safety.
   - Use `normalize_error_string_for_hash()` for error hashes.
   - Persist circuit breaker state atomically.
2. **`check_templates.py`:**
   - Expand `_extract_template_placeholders` to support `@var@` and `@var:fmt@`.
   - Update line 2106 to detect `@var@` / `@var:fmt@` tokens in `stem`.
   - Use `normalize_error_string_for_hash()` in circuit breaker tracking.
3. **`tests/test_shard_compiler_hardening.py`:**
   - Test 100% fix recovery when `shard_06_data.py` has a `SyntaxError` on line 600.
   - Test filename normalization across variants (`Hab-03.py`, `hab_03.py`).
   - Test `sys.modules` and `linecache` cache safety across multiple compiles.
   - Test pure `@var@` template acceptance without `{var}` braces.
   - Test all 5 C2C failure modes with CRLF verifying zero-disk-mutation.
   - Test single-letter `vars` alongside LaTeX macros vs true placeholder leaks.
4. **Validation:**
   - Run complete test suite via pytest.
