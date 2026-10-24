# DISPATCH: Stream 1A — Improver (`impr_1a`)

- **Orchestrator Conversation ID (`Recipient` for `send_message`):** `d0ce22db-904e-4856-b353-59975bfb5874`
- **Teamwork Directory:** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1a_impr`
- **Implementer Handoff to Audit & Improve:** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1a_impl/handoff.md`
- **Role:** `Phase 2 Mejorador — Stream 1A (Motor PrairieLearn @var@, Invariantes Anti-Placeholder y Métricas R-16)`

## 1. Strict Write Boundaries (ONLY touch these files + your Teamwork Directory)
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/engine/assemble.py`
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/engine/instantiate.py`
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/engine/invariants.py`
- `d:/Augusto/personal_portfolio/Tops_academy/tests/test_katex_prairielearn_tokens.py`
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1a_impr/{BRIEFING.md,progress.md,handoff.md}`

## 2. Hardening & Scrutiny Objectives
1. Read `stream_1a_impl/handoff.md`, `stream_1a_impl/BRIEFING.md`, `engine/assemble.py`, `engine/instantiate.py`, `engine/invariants.py`, and `tests/test_katex_prairielearn_tokens.py`.
2. Scrutinize & harden edge cases:
   - **`@var@` / `@var:fmt@` Edge Cases:**
     - What happens if a format spec fails `format(val, fmt_spec)` (e.g. `val` is a `str` like `"2.50"` while template has `@val:.2f@`, or `val` is `int` with `@val:.2f@`)? Coercing numeric strings / `int` safely for float format specs `.2f`/`.3f` when appropriate (or clear `ValueError` with exact `@var:fmt@` context) prevents cryptic runtime crashes!
     - What if a stem contains TWO `@` signs on the same line that are NOT placeholders (e.g. `"contact a@b.com or c@d.com"` where there is space/dot between `@...` and `@`)? Verify the regex `@([A-Za-z_][A-Za-z0-9_]*)(?::([^@\s{}]+))?@` does NOT accidentally match across `"@b.com or c@"` (which it won't if identifier chars are restricted, AND verify `invariants.py` doesn't false-flag `"user@domain.com and admin@domain.com"` while reliably catching any genuine `@missing_var@`!).
     - Verify `stem_variants` (list of 3–5 stems) works seamlessly with `@var@` in `assemble_question` and `instantiate_competency`.
   - **Anti-Unrendered-Placeholder Precision (`{delta}` vs Valid KaTeX):**
     - Test real econometrics LaTeX expressions from Greene (`ab30cf91` `shard_06`, `part_01`, `part_02`): `\operatorname{plim}_{n \to \infty}`, `\xrightarrow{d}`, `\stackrel{a}{\sim}`, `\begin{pmatrix} a & b \\ c & d \end{pmatrix}`, `\mathbb{R}^{k}`, `\mathcal{N}(0, \sigma^2)`, `S_{zz}`, `X'Z(Z'Z)^{-1}Z'X`, `{k}^*` — ensure ZERO false positives when e.g. `vars = {"n": 100, "k": 3, "a": 2, "d": 4}` (CRITICAL: if `vars` contains `"d": 4` or `"n": 100`, ensure `\xrightarrow{d}` or `x_{n}` or `\mathbb{R}^{k}` is NOT false-flagged as an uninterpolated `{d}`, `{n}`, or `{k}`, while prose `"con dimensión {d} y muestra {n}"` or `"tolerancia <= {delta}"` IS caught!!). Check this specific edge case carefully—if `vars` has single-letter keys `n`, `k`, `d`, `a`, `b`, LaTeX `x_{n}` / `\frac{a}{b}` / `\xrightarrow{d}` has `{n}`, `{a}`, `{b}`, `{d}` preceded by `\cmd`, `_`, `^`, or `}`! That's a classic bug if not guarded!
   - **`FIB` & `MS` Edge Cases:** Verify `accepted_equivalents` containing non-string numbers (`[2.5, "5/2", "@frac_str@"]`), `multiple_select` options with both `"content"` and `"value"` keys, and `hints` list interpolation.
   - Expand `tests/test_katex_prairielearn_tokens.py` with adversarial tests for all of the above (especially `vars = {"d": 4, "n": 100, "a": 2, "b": 5}` alongside `\xrightarrow{d}`, `\frac{a}{b}`, `x_{n}` vs genuine leaked `<= {delta}`!).
3. Run `& "d:\Augusto\personal_portfolio\Tops_academy\.venv\Scripts\python.exe" -m pytest tests/test_katex_prairielearn_tokens.py tests/test_latex_engine.py tests/test_engine_invariants_adversarial.py tests/test_c2c_validator_prescriptive.py -q`.
4. Write `BRIEFING.md`, `progress.md`, and `handoff.md`, then `send_message` starting with `DONE:: stream_1a_impr`.
