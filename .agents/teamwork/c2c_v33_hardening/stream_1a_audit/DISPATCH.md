# DISPATCH: Stream 1A — Forensic Auditor (`audit_1a`)

- **Orchestrator Conversation ID (`Recipient` for `send_message`):** `d0ce22db-904e-4856-b353-59975bfb5874`
- **Teamwork Directory (ONLY allowed write target):** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1a_audit`
- **Artifacts to Audit:**
  - Original Stream Spec: `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1a_impl/DISPATCH.md`
  - Implementer Handoff: `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1a_impl/handoff.md`
  - Improver Spec & Handoff: `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1a_impr/{DISPATCH.md,handoff.md}`
  - Audited Code & Tests (READ-ONLY):
    - `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/engine/assemble.py`
    - `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/engine/instantiate.py`
    - `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/engine/invariants.py`
    - `d:/Augusto/personal_portfolio/Tops_academy/tests/test_katex_prairielearn_tokens.py`

## Audit Checklist
1. **Boundary Integrity:** Inspect `git status --short` and `git diff -- .agents/skills/content-to-course/engine/ tests/test_katex_prairielearn_tokens.py`. Confirm Stream 1A modified ONLY its 4 assigned files and left zero stray temporary `.py` files in the repo root (note: Streams `1B..1E` have their own disjoint modified/untracked files and `ORIGINAL_REQUEST.md` lists baseline pre-existing files—do NOT false-flag those).
2. **Requirement Verification (Milestone 3.1/3.2 + Bottleneck #2 + Judge 04 `{delta}` Guard + `R-16` Metrics):**
   - `assemble.py`: Phase 0 resolves `@var@` and `@var:fmt@` across `multiple_choice` (`MC7`), `fill_in_the_blank` (`FIB`, including `correct_answer` & `accepted_equivalents`), `multiple_select` (`MS`, including `options` & `correct_answers`), `hints` (strings and dicts), `solution`, and `stem_variants`. Phase 1 preserves backward-compatible `{var}` / `{var:fmt}` without corrupting LaTeX braces (`\frac{a}{b}`, `\begin{bmatrix} ... \\ ... \end{bmatrix}` row breaks, `\mathbb{R}^{k}`, `\xrightarrow{d}`).
   - `assemble.py`: `calibrate_option_lengths` / `compute_option_length_metrics` performs **ZERO fake text padding** on option strings and exposes pure diagnostic length metrics (`correct_len`, `median_distractor_len`, `ratio`, `is_flagged`).
   - `invariants.py` & `instantiate.py`: `check_all_invariants(question, variables=...)` hard-blocks any unrendered `@ident@` / `@ident:fmt@` token AND any uninterpolated `{key}` / `{key:fmt}` matching `variables` (such as `{delta}` leak in prose/math), while producing **zero false positives** when single-letter variables (`d`, `n`, `k`, `a`, `b`, `p`) coexist with real KaTeX (`\xrightarrow{d}`, `x_{n}`, `\mathbb{R}^{k}`, `\frac{a}{b}`, `\mathcal{N}(0, \sigma^2)`, `S_{zz}`).
   - Zero fake mocks, zero weakened assertions, zero `pytest.skip` workarounds in `tests/test_katex_prairielearn_tokens.py`.
3. **Independent Test Execution:**
   - Run `& "d:\Augusto\personal_portfolio\Tops_academy\.venv\Scripts\python.exe" -m pytest tests/test_katex_prairielearn_tokens.py tests/test_latex_engine.py tests/test_engine_invariants_adversarial.py tests/test_c2c_validator_prescriptive.py -q`.
4. Write `BRIEFING.md`, `progress.md`, and `handoff.md` inside `stream_1a_audit/`, then `send_message` starting with `PASS:: stream_1a_audit | ...` or `REJECT:: stream_1a_audit | ...`.
