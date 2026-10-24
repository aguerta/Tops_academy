# Step 0 Pre-Flight & Architectural Scrutiny — Stream 1A Improver (`impr_1a`)

- **Subagent:** `stream_1a_impr`
- **Orchestrator Conversation ID:** `d0ce22db-904e-4856-b353-59975bfb5874`
- **Role:** `Phase 2 Mejorador — Stream 1A (Motor PrairieLearn @var@, Invariantes Anti-Placeholder y Métricas R-16)`
- **Teamwork Directory:** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1a_impr`
- **Target Files (Strict Write Boundaries):**
  - `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/engine/assemble.py`
  - `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/engine/instantiate.py`
  - `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/engine/invariants.py`
  - `d:/Augusto/personal_portfolio/Tops_academy/tests/test_katex_prairielearn_tokens.py`
  - `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1a_impr/{BRIEFING.md,progress.md,handoff.md}`

---

## 1. Implementer Work Verification

Implementer `stream_1a_impl` successfully laid down the core foundations:
- Phase 0 PrairieLearn `@var@` and `@var:fmt@` interpolation pass in `assemble.py`.
- Deterministic R-16 option length helper `compute_option_length_metrics()` in `assemble.py`.
- Unrendered placeholder detection `check_unrendered_placeholders()` and delegation from `validate_katex_syntax()` in `invariants.py`.
- Wiring of `variables=variables` into `check_instance_invariants()` in `instantiate.py`.
- Baseline test suite with 9 tests in `test_katex_prairielearn_tokens.py`.

All 82 existing and new tests pass on the current implementation.

---

## 2. Critical Edge Cases & Hardening Plan

Under rigorous adversarial scrutiny, several high-impact edge cases must be hardened:

### A. Econometrics LaTeX Macros & Single-Letter Variable Collisions (`\xrightarrow{d}`, `x_{n}`, `\mathbb{R}^{k}`)
- **Vulnerability:** In `invariants.py`, `_LATEX_ARG_MACROS` does not include extensible arrows (`\xrightarrow`, `\xleftarrow`, `\xmapsto`, etc.). If `vars` contains single-letter keys common in econometrics (e.g. `vars = {"d": 4, "n": 100, "k": 3, "a": 2, "b": 5}`), expressions like `\xrightarrow{d}` are falsely flagged as uninterpolated `{d}`!
- **Vulnerability:** In `invariants.py`, if there is whitespace before a subscript/superscript (`x_ {n}` or `\sum_ {i=1}`), or multi-argument spacing (`\frac{a} {b}`), the current character check `start > 0 and text[start - 1] in ("_", "^")` and `s.endswith("}")` fails to recognize legitimate LaTeX arguments.
- **Fix:**
  1. Add extensible arrow macros (`xrightarrow`, `xleftarrow`, `xleftrightarrow`, `xRightarrow`, `xLeftarrow`, `xLeftrightarrow`, `xmapsto`, `xhookleftarrow`, `xhookrightarrow`, `xtwoheadleftarrow`, `xtwoheadrightarrow`, `xrightharpoondown`, `xrightharpoonup`, `xleftharpoondown`, `xleftharpoonup`, `substack`, `prescript`, `pmod`, `pod`) to `_LATEX_ARG_MACROS`.
  2. Support optional macro asterisk like `\operatorname*{plim}` and optional bracket arguments `\xrightarrow[n \to \infty]{d}`.
  3. Support whitespace-tolerant subscript/superscript detection `prefix.endswith(("_", "^"))` and `s = prefix.rstrip()` in multi-arg LaTeX command backtracking.

### B. Safe Numeric Formatting Coercion in `@var:fmt@` and `{var:fmt}`
- **Vulnerability:** When a format spec like `@val:.2f@` is used on numeric strings (e.g. `"2.50"`) or integer specs like `03d` on float values/strings, direct `format(val, fmt_spec)` raises `ValueError`.
- **Fix:** Implement robust `_safe_format_value(val, fmt_spec)` across both PrairieLearn Phase 0 pass and legacy Phase 1 pass in `assemble.py`:
  - Gracefully handles `int`, `float`, numeric `str`, and integer-convertible values.
  - Safe fallback to `str(val)` without runtime crashes.

### C. Email & Multiple `@` Non-Token Safety
- **Verification:** Confirm that lines with legitimate `@` characters like `"contact user@domain.com and admin@domain.com"` are never matched by `_PL_TOKEN_PATTERN` and never false-flagged by `check_unrendered_placeholders()`.
- Add adversarial unit tests verifying this invariant.

### D. Full FIB & MS Question-Type Robustness
- **`fill_in_the_blank`:** Normalize `accepted_equivalents` containing mixed types (`[2.5, "5/2", "@frac_str@"]`) to ensure numeric scalars are stringified without duplicates, and run anti-placeholder validation on all equivalents.
- **`multiple_select`:** Fall back cleanly across `content`, `value`, and `text` (preventing dict `.get("content", default)` trap when content is `""`), and handle dict-formatted `hints`.
- **`stem_variants`:** Validate that 3–5 stem variants containing `@var@` tokens interpolate correctly with random seed selection and deduplicate cleanly in `instantiate_template`.

---

## 3. Blocker Evaluation
- **Verdict:** ZERO BLOCKERS. All improvements are strictly confined to the 4 files within our Write Boundaries. No changes required outside allowed files.
