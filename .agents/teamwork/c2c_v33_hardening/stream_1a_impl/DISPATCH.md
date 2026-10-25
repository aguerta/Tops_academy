# DISPATCH: Stream 1A — Implementer (`impl_1a`)

- **Orchestrator Conversation ID (`Recipient` for `send_message`):** `d0ce22db-904e-4856-b353-59975bfb5874`
- **Teamwork Directory:** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1a_impl`
- **Role:** `Phase 1 Implementador — Stream 1A (Motor PrairieLearn @var@, Invariantes Anti-Placeholder y Métricas R-16)`

## 1. Strict Write Boundaries (ONLY touch these files + your Teamwork Directory)
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/engine/assemble.py`
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/engine/instantiate.py`
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/engine/invariants.py`
- `d:/Augusto/personal_portfolio/Tops_academy/tests/test_katex_prairielearn_tokens.py` *(new)*
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1a_impl/{BRIEFING.md,progress.md,handoff.md}`

*(Forbidden: Do NOT edit `compile_shard.py`, `check_templates.py`, `run.py`, `dispatch.py`, or any other file outside the list above!)*

## 2. Technical Specifications
1. **Step 0 Pre-Flight Sanity Check:**
   - Read `engine/assemble.py`, `engine/instantiate.py`, `engine/invariants.py`, and existing engine tests (`tests/test_engine*.py` / `tests/test_assemble*.py` if present) to verify all existing function signatures and invariants. Record findings in `BRIEFING.md`. If a hard code conflict blocks this order, escalate via `BLOCKER::` to `d0ce22db-904e-4856-b353-59975bfb5874`.
2. **Orthogonal PrairieLearn `@var@` / `@var:fmt@` Token Interpolation (`engine/assemble.py`):**
   - In `render_template(template_str, variables)` (and `format_template_string`), add a **Phase 0 priority pass** matching `@([A-Za-z_][A-Za-z0-9_]*)(?::([^@\s{}]+))?@`.
   - When the identifier exists in `variables`, format it using `format(val, fmt_spec)` if `fmt_spec` is provided (supporting e.g. `.2f`, `+.3f`, `.4g`, `d`), or `str(val)` otherwise—**without touching any `{...}` braces of KaTeX**!
   - Support 1-character variable names cleanly via `@k@`, `@n@`, `@r@`, `@x@` without colliding with LaTeX `\frac{1}{n}` or `\mathbf{I}_{k}`!
   - Preserve 100% backward compatibility with existing `{var}` / `{var:fmt}` interpolation for templates that still use `{var}`.
3. **Full Question-Type Coverage (`engine/assemble.py` -> `assemble_question`):**
   - Today `multiple_choice_7_options` formats `correct` and `distractors`, plus `stem`, `hints`, and `explanation`/`detailed_solution`, **but `fill_in_the_blank` and `multiple_select` miss variable interpolation & KaTeX sanitization**.
   - Extend `format_template_string(..., variables)` + `sanitize_katex_syntax()` to:
     - `fill_in_the_blank`: `correct_answer.value` / `ans_val` (`str_val`), `canonical_algebraic` (if string), and each string element in `accepted_equivalents` / `equivalents`.
     - `multiple_select`: `content`/`value` and `error_rationale` of every option in `raw_options` / `options`.
4. **Zero-Fake-Padding `R-16` Helper (`engine/assemble.py`):**
   - Keep `calibrate_option_lengths()` free of artificial text padding (do NOT append generic filler words that corrupt psychometric validity), and add a clean deterministic helper `compute_option_length_metrics(correct_text: str, distractors: Sequence[str], min_ratio: float = 0.65, max_ratio: float = 1.35) -> Dict[str, Any]` returning `correct_len`, `distractor_lens`, `avg_distractor_len`, `ratio`, `is_within_bounds`, and `summary_str` so validators/compilers can report exact character diagnostics.
5. **Hard Anti-Unrendered-Placeholder Invariant (`engine/invariants.py` & `engine/instantiate.py`):**
   - In `ab30cf91` (`Judge 04`), an unrendered `{delta}` placeholder leaked all the way into Stage 5 blind judging!
   - In `engine/invariants.py` (`check_instance_invariants` / helper exported for template dry-runs), deterministically detect and reject:
     a) Any unresolved `@ident@` or `@ident:fmt@` placeholder (`@[A-Za-z_][A-Za-z0-9_]*(?::[^@\s{}]+)?@`) in `stem`, `options[*].content`, `options[*].error_rationale`, `correct_answer.value`, `hints[*]`, or `detailed_solution`.
     b) Any uninterpolated `{key}` (or `{key:fmt}`) where `key` matches an actual key in `gen_result.get("vars", {})` (when `vars` is passed/available on the instance or checked in `instantiate.py`), OR a standalone `{ident}` placeholder outside LaTeX macro arguments (carefully avoiding false positives on legitimate LaTeX like `\frac{delta}{2}`, `\text{delta}`, `x_{delta}`, `x^{delta}`, `\begin{matrix}`, `\operatorname{plim}`).
   - Wire `vars` awareness cleanly in `instantiate.py` / `check_instance_invariants` without breaking existing function signatures (use optional `variables: Optional[Dict[str, Any]] = None` parameter).

## 3. Required Tests & Verification
- Create `tests/test_katex_prairielearn_tokens.py` covering:
  - `@var@` and `@var:fmt@` inside complex nested KaTeX (`r"$\operatorname{Est.Asy.Var}[b_{IV}] = \frac{@s2:.2f@ \cdot @szz@}{@szx@^2} \mathbf{I}_{@k_dim@}$"`).
  - Single-letter variables `@n@`, `@k@` alongside `\sum_{i=1}^{n}` and `\mathbb{R}^{k}`.
  - `fill_in_the_blank` and `multiple_select` variable interpolation.
  - Rejection of unresolved `@delta@` and uninterpolated `{delta}` (when `delta` is in `vars` or bare `{delta}` in prose like `"tol <= {delta}"`), while allowing valid LaTeX `\frac{delta}{n}`, `x_{delta}`, `\text{delta}`.
  - Backward compatibility with legacy `{var}` templates and `compute_option_length_metrics()`.
- Run `& "d:\Augusto\personal_portfolio\Tops_academy\.venv\Scripts\python.exe" -m pytest tests/test_katex_prairielearn_tokens.py -q` plus existing engine tests.
