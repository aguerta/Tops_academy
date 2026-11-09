# BRIEFING: Stream 1A Pre-Flight Sanity Check

**Milestone:** M4 (KaTeXAST + Algebraic Canonicalizer + Pydantic ShardCompetenceContract)
**Stream:** 1A
**Author:** m4_implementer

---

## 1. Baseline Findings

### A. `validate_katex_syntax` in `engine/invariants.py`
- **Location:** Lines 550-840 in `engine/invariants.py`.
- **Current Behavior:**
  1. Checks for triple dollar delimiters (`$$$`).
  2. Checks for residual double curly braces (`{{}}` or `{{var}}` when `allow_template_vars=False`).
  3. Checks balanced math delimiters (`$$` and `$`).
  4. Checks balanced curly braces and runs `_render_katex_safe(block.strip(), is_disp)`.
  5. Checks unclosed nested accent/style macros.
  6. Checks arity of 2-arg macros (`\frac`, `\binom`, `\overset`, etc.).
  7. Checks matched and closed LaTeX environments (`\begin{...}` ... `\end{...}`).
  8. Checks scalable delimiters (`\left` / `\right`).
  9. Checks unescaped LaTeX math commands (`dot{w}`, `frac{a}{b}`).
  10. Checks unrendered placeholders (`@var@`, `{var}`).
  11. Detects overescaped LaTeX commands (`\\frac`, `\\text`, etc. via R-23).
  12. Rejects forbidden linebreaks `\\` inside inline math outside matrix/cases.
  13. Rejects unsupported `\centernot` and unescaped underscores in `\text{...}`.
  14. Rejects prose overflow (`> 45` chars) in `\text{...}`, `\textrm{...}`, `\mathrm{...}` via `[KATEX-PROSE-OVERFLOW]`.
- **Target Changes:**
  - Export `KaTeXAST`, `validate_katex_ast`, and `pykatex_validate_with_column` from `engine/katex_ast.py`.
  - In `_render_katex_raw`, integrate exact column detection `(col X)` from `pykatex` errors while maintaining backwards compatibility with all existing invariant checks and test expectations.

### B. `sanitize_katex_syntax` in `engine/assemble.py`
- **Location:** Lines 233-432 in `engine/assemble.py`.
- **Current Behavior:**
  1. Collapses overescaped LaTeX commands (`\\frac` -> `\frac`, preserving matrix `\\\frac` as `\\ \frac`).
  2. Maps unsupported external macros (`\centernot` -> `\nRightarrow`, `\not`).
  3. Repairs `\text{..._...}` and unescaped underscores in `\text{...}`.
  4. Collapses basic double signs (`+ -5` -> `- 5`, etc.) in math blocks.
  5. Replaces `$$$` with `$$`.
  6. Normalizes double curly braces `{{var}}` -> `{var}` without corrupting nested LaTeX.
  7. Auto-repairs unclosed nested accent/style/sqrt macros, dropped numerator/denominator braces in `\frac`, and unbraced numeric denominators (`\frac{s}3` -> `\frac{s}{3}`).
- **Target Changes:**
  - Import `canonicalize_algebraic_katex` from `engine.katex_ast` (with fallback `.katex_ast`).
  - Integrate `canonicalize_algebraic_katex` so both double signs and unitary coefficients (`$1 x$` -> `$x$`, `$-1 x$` -> `$-x$`, etc.) are canonically collapsed inside math blocks.

### C. Test Suite Baseline
- Ran: `pytest -o addopts="" tests/test_pykatex_warn.py tests/test_assemble_sanitize_katex_r23.py tests/test_invariants_and_shard_overescape_r23.py -q`
- Result: 73 passed in 2.59s with zero failures.
