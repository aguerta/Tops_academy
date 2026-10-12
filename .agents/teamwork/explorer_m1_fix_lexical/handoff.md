# Explorer 1 Handoff Report: Lexical Corruption Remediation Plan (Milestone 1)

**Agent**: Explorer 1 (`explorer_m1_fix_lexical`)  
**Target**: Milestone 1 Remediation (Lexical Scanner Rules R-03 and R-02)  
**Date**: 2026-10-11T01:41:00Z  
**Recipient**: Parent (`84948f37-b77a-4675-a1cb-6a3b8a288462`)  
**Status**: INVESTIGATION & REMEDIATION DESIGN COMPLETE (HARD HANDOFF)  

---

## 1. Observation

1. **Adversarial Test Suite Execution**:
   - Tool Command: `python -m pytest tests/test_adversarial_validator.py -v`
   - Result: 14 failed, 21 passed in 0.76s.
   - Verbatim Failures:
     * `FAILED tests/test_adversarial_validator.py::TestAdversarialLatex::test_unescaped_latex_command_starting_with_control_prefix[\\norm]`
     * `FAILED tests/test_adversarial_validator.py::TestAdversarialLatex::test_unescaped_latex_command_starting_with_control_prefix[\\ne]`
     * `FAILED tests/test_adversarial_validator.py::TestAdversarialLatex::test_unescaped_latex_command_starting_with_control_prefix[\\boxed]`
     * `FAILED tests/test_adversarial_validator.py::TestAdversarialLatex::test_unescaped_latex_command_starting_with_control_prefix[\\therefore]`
     * `FAILED tests/test_adversarial_validator.py::TestAdversarialLatex::test_unescaped_latex_command_starting_with_control_prefix[\\thickspace]`
     * `FAILED tests/test_adversarial_validator.py::TestAdversarialLatex::test_unescaped_latex_command_starting_with_control_prefix[\\textcolor]`
     * `FAILED tests/test_adversarial_validator.py::TestAdversarialLatex::test_unescaped_latex_command_starting_with_control_prefix[\\bigcap]`
     * `FAILED tests/test_adversarial_validator.py::TestAdversarialLatex::test_unescaped_latex_command_starting_with_control_prefix[\\bigcup]`
     * `FAILED tests/test_adversarial_validator.py::TestAdversarialLatex::test_unescaped_latex_command_starting_with_control_prefix[\\bigoplus]`
     * `FAILED tests/test_adversarial_validator.py::TestAdversarialLatex::test_unescaped_latex_command_starting_with_control_prefix[\\bigotimes]`
     * `FAILED tests/test_adversarial_validator.py::TestAdversarialLatex::test_unescaped_latex_command_starting_with_control_prefix[\\rank]`
   - Verbatim Assertion: `BLIND SPOT: Single-backslash LaTeX command '{cmd}' was NOT detected by lexical scanner! It will silently decode to an ASCII control character in standard JSON parsers.`

2. **Challenger 2 Empirical Stress Test Execution**:
   - Tool Command: `python -m pytest tests/validator/test_empirical_stress.py -v`
   - Result: 6 failed, 79 passed in 12.70s.
   - Verbatim Failures in Lexical Scanner:
     * `FAILED tests/validator/test_empirical_stress.py::test_fn_latex_newline_command_escape`
       `AssertionError: FALSE NEGATIVE: LaTeX '\newline' was not caught by Pass 1 lexical scanner!`
     * `FAILED tests/validator/test_empirical_stress.py::test_fn_latex_not_command_escape`
       `AssertionError: FALSE NEGATIVE: LaTeX '\not' was not caught by Pass 1 lexical scanner!`

3. **Inspection of `src/validator/lexical_scanner.py`**:
   - Lines 17–46: `LATEX_CONTROL_PREFIXES` defines a hardcoded dictionary:
     * `"b"` contains only 18 entries: `{"begin", "beta", "bar", "bmatrix", "bmod", "boldsymbol", "binom", "breve", "bullet", "bot", "big", "Big", "bigg", "Bigg", "bold", "backslash", "bigskip", "bordermatrix", "box"}`. Omitted: `boxed`, `bm`, `bigcap`, `bigcup`, `bigoplus`, `bigotimes`, `mathbf`, `mathbb`, etc.
     * `"n"` contains only 14 entries: `{"nu", "nabla", "neq", "neg", "notin", "nsubseteq", "nexists", "natural", "nearrow", "nwarrow", "normalsize", "nparallel", "noindent", "nonumber"}`. Omitted: `ne`, `not`, `norm`, `newline`, `ni`.
     * `"r"` contains only 9 entries: `{"right", "rho", "rangle", "rceil", "rfloor", "rightarrow", "Rightarrow", "Re", "root"}`. Omitted: `rank`, `ref`, `real`.
     * `"t"` contains only 18 entries: `{"tau", "theta", "text", "times", "tilde", "to", "top", "tan", "tanh", "triangle", "tfrac", "textbf", "textit", "texttt", "textsf", "tag", "tiny", "thinspace"}`. Omitted: `tr`, `therefore`, `thickspace`, `textcolor`.
   - Lines 210–213: Fallthrough bug:
     ```python
     if next_ch in ("b", "f", "n", "r", "t"):
         pos += 1
         continue
     ```
     When an unlisted command is scanned, this block assumes `next_ch` is a standard JSON control escape and advances `pos += 1`, allowing the corrupted string to pass without error.
   - Lines 95–131: Dead code bug:
     `ch in ("\n", "\r")` is intercepted at lines 95–106 and calls `continue`. As a result, lines 113–131 (`CONTROL_CHAR_TO_LATEX`) can never be reached for `0x0A` and `0x0D`.
   - Lines 215–226: Prefix `v` and `0` bug:
     For unlisted `v` escapes, `seq` is set to `f"\\{next_ch}"` (`\v`) instead of the full word token (e.g. `\varpi`), and `pos` is only incremented by 1, leaving trailing letters in the parse stream.

---

## 2. Logic Chain

1. **Premise 1 (R2 Specification Mandate)**:
   - Acceptance Criteria R2 and F01 require the validator to reject: *"LaTeX backslash corruption (including silently-valid escapes that produce control characters)"*.
   - In standard JSON (RFC 8259), `\b`, `\f`, `\n`, `\r`, and `\t` are valid single-character control escapes.

2. **Premise 2 (Empirically Confirmed Leakage)**:
   - In Observation 1 and Observation 2, common mathematical commands (`\ne`, `\not`, `\norm`, `\boxed`, `\therefore`, `\thickspace`, `\textcolor`, `\bigcap`, `\bigcup`, `\bigoplus`, `\bigotimes`, `\rank`, `\newline`) were tested against `src/validator/lexical_scanner.py`.
   - Because `LATEX_CONTROL_PREFIXES` omitted them (Observation 3), lines 210–213 treated them as valid JSON escapes, allowing single-backslash commands to bypass Pass 1 validation.
   - In standard Python `json.loads`, `\ne 0` decodes to `<newline>e 0`, `\norm{x}` decodes to `<newline>orm{x}`, and `\boxed{x}` decodes to `<backspace>oxed{x}`.

3. **Premise 3 (Downstream Architectural Impact)**:
   - The practice platform (Milestone 2) uses KaTeX to render mathematical expressions.
   - Decoded control characters destroy the LaTeX syntax, causing KaTeX rendering errors that break the user interface.
   - The content-to-course Antigravity skill (Milestone 3) generates course material from PDFs (e.g. PDEs in `sample_content/I__Ecuaciones_en_derivadas_parciales_2026.pdf`). If the validator fails to catch unescaped `\ne`, `\not`, and `\norm`, corrupted questions will be published to `courses/`.

4. **Conclusion**:
   - A multi-layered remediation strategy combining an expanded dictionary (~250 commands), math-mode context awareness (`in_math`), and non-text control heuristics (`\b`, `\f`, `\r`) is necessary and sufficient to eliminate all false negatives while preserving 100% compatibility with valid formatted JSON text.

---

## 3. Caveats

- **Scope Constraint**: As Explorer 1, this task is strictly an investigation and remediation plan. Source code modifications to `src/validator/` must be implemented by the assigned worker agent (`worker_m1_validator`).
- **Non-Lexical Reviewer Findings**: Reviewer 2, Challenger 1, and Challenger 2 also identified non-lexical defects (CLI entry point packaging `validate-course`, missing `options` on `multiple_select`, and missing `correct_answer` on `fill_in_the_blank`). Those are tracked separately for Explorer 2 and Worker 1.

---

## 4. Conclusion

1. **Root Cause**: The lexical scanner's reliance on a narrow whitelist in `LATEX_CONTROL_PREFIXES` combined with an unconditional fallthrough for `b`, `f`, `n`, `r`, `t` created a critical blind spot where common LaTeX commands silently mutated into ASCII control characters.
2. **Remediation Strategy**:
   - Expand `LATEX_CONTROL_PREFIXES` to include all ~250 AMS-LaTeX, KaTeX, and physics macros starting with `b`, `f`, `n`, `r`, `t`, `v`, `0`.
   - Implement Math Mode Context Tracking (`in_math` toggled by `$` and `$$`): Inside math mode, any single backslash before `[bfnrt]` followed by letters is flagged as R-03.
   - Implement Inherent Control Byte Heuristics: Outside math mode, `\b`, `\f`, and lone `\r` followed by letters are flagged as R-03.
   - Implement Syntax Signature Detection: Outside math mode, commands followed by `{`, `[`, `_`, `^`, `=`, `<`, `>` are flagged as R-03.
   - Safe Fallthrough: Legitimate JSON formatting escapes (`\n` and `\t`) in natural language text are preserved.
   - Fix R-02 tokenization for `v` and `0` to capture full command tokens.
   - Clean up dead code in `CONTROL_CHAR_TO_LATEX`.
3. **Artifact**: The comprehensive fix plan and complete reference code have been documented in:
   `g:\Mi unidad\Competence_analyser\.agents\teamwork\explorer_m1_fix_lexical\lexical_fix_plan.md`

---

## 5. Verification Method

To verify the implementation once applied by Worker 1:

1. **Adversarial LaTeX Test Verification**:
   ```powershell
   python -m pytest tests/test_adversarial_validator.py -k "TestAdversarialLatex" -v
   ```
   *Must pass 12 of 12 tests with 0 failures.*

2. **Empirical Challenger Test Verification**:
   ```powershell
   python -m pytest tests/validator/test_empirical_stress.py -k "test_fn_latex" -v
   ```
   *Must pass both `test_fn_latex_newline_command_escape` and `test_fn_latex_not_command_escape`.*

3. **Programmatic Verification of Reviewer 2 Commands**:
   ```bash
   python -c "from src.validator.lexical_scanner import scan_lexical; errs = scan_lexical('{\"stem\": \"x \\not= y and a \\ne b and \\bm{v} and \\tr(A) and \\ref{eq1}\"}'); print([e.rule_id for e in errs])"
   ```
   *Must output exactly `['R-03', 'R-03', 'R-03', 'R-03', 'R-03']`.*

4. **Regression Verification of Baseline Suite**:
   ```powershell
   python -m pytest tests/validator/test_validator.py -v
   ```
   *Must pass 67 of 67 tests.*
