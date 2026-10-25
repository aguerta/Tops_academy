# Step 0 Pre-Flight Verification & Briefing — Stream 1A

- **Subagent:** `stream_1a_impl`
- **Orchestrator Conversation ID:** `d0ce22db-904e-4856-b353-59975bfb5874`
- **Teamwork Directory:** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1a_impl`
- **Target Files (Strict Write Boundaries):**
  - `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/engine/assemble.py`
  - `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/engine/instantiate.py`
  - `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/engine/invariants.py`
  - `d:/Augusto/personal_portfolio/Tops_academy/tests/test_katex_prairielearn_tokens.py` *(new)*
  - `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1a_impl/{BRIEFING.md, progress.md, handoff.md}`

---

## 1. Pre-Flight Inspection Findings

### A. `engine/assemble.py`
- **Current Signature of `format_template_string`:** `format_template_string(template_str: str, variables: Dict[str, Any]) -> str`.
  - Currently handles `{var}` and `{var:fmt}` using regex `r"\{([^{}]+)\}"`.
  - Lacks orthogonal PrairieLearn `@var@` / `@var:fmt@` interpolation pass.
  - Does not alias/export `render_template`.
- **Current `assemble_question`:**
  - Formats `stem`, `hints`, `detailed_solution`, and MC7 `correct` / `distractors`.
  - **Omission:** `fill_in_the_blank` does not run `format_template_string` or `sanitize_katex_syntax` on `correct_answer.value`, `canonical_algebraic`, or `accepted_equivalents`.
  - **Omission:** `multiple_select` only reads `opt.get("text", opt.get("content", ""))`, missing `opt.get("value")`, and needs consistent formatting for options and rationales.
- **Current `calibrate_option_lengths`:**
  - Already free of fake filler padding (returns unchanged if within or outside bounds).
  - Lacks the deterministic diagnostic helper `compute_option_length_metrics(correct_text, distractors, min_ratio=0.65, max_ratio=1.35)`.

### B. `engine/instantiate.py`
- **Current Signature of `instantiate_template`:** sweeps seeds, executes sandbox, calls `assemble_question`, and invokes `check_instance_invariants(candidate_q, interaction_type)`.
  - Currently does not pass `variables=variables` to `check_instance_invariants`.
  - Can cleanly pass `variables=variables` without breaking any contracts.

### C. `engine/invariants.py`
- **Current Signature of `validate_katex_syntax`:** `validate_katex_syntax(text: str, context: str, allow_template_vars: bool = False) -> List[str]`.
  - Checks balanced delimiters, triple dollar `$$$`, residual double braces `{{...}}`, macro arity, and unsubstituted `{var}`.
  - Currently permits any macro matching `\\[a-zA-Z]+` to precede `{var}` without checking if the macro actually takes arguments (e.g. 0-arg Greek macros like `\delta` would falsely suppress placeholder detection).
  - Does not check for unresolved PrairieLearn tokens `@ident@` / `@ident:fmt@`.
  - Lacks `variables: Optional[Dict[str, Any]] = None` support.
- **Current Signature of `check_instance_invariants`:** `check_instance_invariants(instance: Dict[str, Any], interaction_type: str, strict_length_bounds: bool = True) -> Tuple[bool, List[str]]`.
  - Currently does not validate `correct_answer` fields in `fill_in_the_blank` with `validate_katex_syntax`.
  - Can take optional `variables: Optional[Dict[str, Any]] = None` after `strict_length_bounds`.

### D. Existing Test Suite Baseline
- Ran pytest on `tests/test_latex_engine.py` and `tests/test_engine_invariants_adversarial.py`: **61 passed in 0.85s**.
- Ran pytest on `tests/test_c2c_validator_prescriptive.py`: **12 passed in 1.27s**.
- All existing tests pass cleanly on current codebase.

### E. Blocker Evaluation
- **Verdict:** NO BLOCKERS. All specifications fit cleanly within the designated Write Boundaries and preserve full backwards compatibility.

---

## 2. Implementation Plan

1. **PrairieLearn Token Interpolation & Helpers in `engine/assemble.py`:**
   - Define `render_template(template_str: str, variables: Dict[str, Any]) -> str` and alias `format_template_string = render_template`.
   - Add **Phase 0 priority pass** in `format_template_string` matching `r"@([A-Za-z_][A-Za-z0-9_]*)(?::([^@\s{}]+))?@"`.
     - When `key in variables`, format using `format(val, fmt_spec)` (with float fallback) if `fmt_spec` provided, else `str(val)`.
     - Leaves LaTeX curly braces `{...}` completely untouched.
   - Retain existing Phase 1 for backward compatibility with `{var}` / `{var:fmt}`.
   - Add `compute_option_length_metrics(correct_text: str, distractors: Sequence[Union[str, Dict[str, Any]]], min_ratio: float = 0.65, max_ratio: float = 1.35) -> Dict[str, Any]`.
   - Extend `assemble_question` for `fill_in_the_blank` (`correct_answer.value`, `canonical_algebraic`, `accepted_equivalents`) and `multiple_select` (`content`/`value`/`text` and `error_rationale`).

2. **Hard Anti-Unrendered-Placeholder Invariant in `engine/invariants.py`:**
   - Define `_LATEX_ARG_MACROS` restricting argument-taking macros to valid LaTeX commands (`text`, `textbf`, `mathbf`, `sqrt`, `frac`, `begin`, `operatorname`, accents, etc.).
   - Define and export `check_unrendered_placeholders(text: str, context: str = "text", variables: Optional[Dict[str, Any]] = None) -> List[str]`:
     - Catch any unresolved `@ident@` or `@ident:fmt@` matching `r"@([A-Za-z_][A-Za-z0-9_]*(?::[^@\s{}]+)?)@"`.
     - Catch any uninterpolated `{key}` or `{key:fmt}` where `key in variables` (or standalone `{ident}` outside LaTeX macro arguments / sub-superscripts).
     - Protect legitimate LaTeX `\frac{delta}{2}`, `\frac{delta}{n}`, `\text{delta}`, `x_{delta}`, `x^{delta}`, `\begin{matrix}`, `\operatorname{plim}`.
   - Wire `check_unrendered_placeholders` into `validate_katex_syntax(text, context, allow_template_vars=False, variables=None)`.
   - Update `check_instance_invariants(instance, interaction_type, strict_length_bounds=True, variables=None)`:
     - Automatically extract `variables = variables or instance.get("vars") or instance.get("variables")`.
     - Validate `correct_answer.value`, `canonical_algebraic`, and `accepted_equivalents` for `fill_in_the_blank`.

3. **Wiring in `engine/instantiate.py`:**
   - In `instantiate_template`: pass `variables=variables` to `check_instance_invariants(candidate_q, interaction_type, variables=variables)`.

4. **Dedicated Test Suite `tests/test_katex_prairielearn_tokens.py`:**
   - Test PrairieLearn `@var@` and `@var:fmt@` inside nested KaTeX fractions and matrices.
   - Test single-letter variables `@n@`, `@k@` alongside `\sum_{i=1}^{n}` and `\mathbb{R}^{k}`.
   - Test `fill_in_the_blank` and `multiple_select` token interpolation and KaTeX sanitization.
   - Test detection of unresolved `@delta@` and uninterpolated `{delta}` (when `delta` is in `vars` or standalone in prose like `"tol <= {delta}"`), while ensuring valid LaTeX `\frac{delta}{n}`, `x_{delta}`, `\text{delta}` passes.
   - Test backward compatibility with legacy `{var}` and `compute_option_length_metrics()`.

5. **Validation & Completion:**
   - Run full pytest suite.
   - Write `progress.md` and `handoff.md`.
