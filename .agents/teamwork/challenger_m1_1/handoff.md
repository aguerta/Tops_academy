# Milestone 1 Adversarial Challenge Report: Exercise Bank Format & Validator

**Challenger**: Challenger 1 (`challenger_m1_1`)  
**Target Milestone**: Milestone 1 (Exercise Bank Format & Validator, R2)  
**Date**: 2026-10-11T01:30:00Z  
**Verdict**: **REQUEST_CHANGES**  
**Overall Risk Assessment**: **HIGH**  

---

## 1. Observation

1. **Baseline Verification**:
   - Baseline validator test suite in `tests/validator/test_validator.py` was executed:
     ```
     $ python -m pytest tests/validator -v
     ============================= 67 passed in 11.77s =============================
     ```
   - Standard 28 fixtures and basic edge cases all pass cleanly as reported by the worker.

2. **Empirical Adversarial Test Execution**:
   - Adversarial stress harness `tests/test_adversarial_validator.py` was created and executed:
     ```
     $ python -m pytest tests/test_adversarial_validator.py -v
     ======================== 14 failed, 21 passed in 0.83s ========================
     ```
   - 21 stress tests passed (boundary anti-giveaway values, deep JSON nesting, 50k character stems, extreme floats, valid mixed question types, valid graphs).
   - 14 stress tests failed, isolating 3 distinct blind spots in `src/validator/`.

3. **Observation 1: Silent Control Character Escapes for Standard LaTeX Commands (`src/validator/lexical_scanner.py:17-46, 186-213`)**:
   - `LATEX_CONTROL_PREFIXES` maintains a hardcoded whitelist of LaTeX commands starting with letters `b`, `f`, `n`, `r`, `t`.
   - In lines 210-213:
     ```python
     # If not a recognized LaTeX command, next_ch in (b, f, n, r, t) is a valid JSON escape
     if next_ch in ("b", "f", "n", "r", "t"):
         pos += 1
         continue
     ```
   - When a LaTeX command starts with `b`, `f`, `n`, `r`, or `t` but is NOT in the whitelist, the scanner skips it without flagging an error.
   - Standard `json.loads` then parses `\n` as newline (0x0A), `\b` as backspace (0x08), `\t` as tab (0x09), `\r` as carriage return (0x0D), destroying the LaTeX command name.
   - Tested empirically:
     * `\norm{x}`: `\n` becomes newline + `orm{x}` -> 0 errors detected.
     * `\ne 0`: `\n` becomes newline + `e 0` -> 0 errors detected (`\neq` is present, but `\ne` is missing).
     * `\boxed{x}`: `\b` becomes backspace + `oxed{x}` -> 0 errors detected (`box` is in whitelist, but exact token `boxed` is not).
     * `\therefore`: `\t` becomes tab + `herefore` -> 0 errors detected.
     * `\thickspace`: `\t` becomes tab + `hickspace` -> 0 errors detected.
     * `\textcolor`: `\t` becomes tab + `extcolor` -> 0 errors detected.
     * `\bigcap`: `\b` becomes backspace + `igcap` -> 0 errors detected.
     * `\bigcup`: `\b` becomes backspace + `igcup` -> 0 errors detected.
     * `\bigoplus`: `\b` becomes backspace + `igoplus` -> 0 errors detected.
     * `\bigotimes`: `\b` becomes backspace + `igotimes` -> 0 errors detected.
     * `\rank`: `\r` becomes carriage return + `ank` -> 0 errors detected.

4. **Observation 2: Missing / Null `options` Allowed on `multiple_select` (`src/validator/schema_validator.py:98`, `src/validator/rules.py:166-184`)**:
   - In `COURSE_SCHEMA`, `Question` specifies `required: ["id", "competency_id", "interaction_type", "stem", "hints"]`. `"options"` is NOT required.
   - In `src/validator/rules.py`:
     ```python
     elif itype == "multiple_select":
         if isinstance(options, list):
             n_opts = len(options)
             ...
     ```
   - If `options` is omitted or `None`, `isinstance(options, list)` evaluates to `False`. Unlike `multiple_choice_7_options` (which has an `else` branch raising `R-10: ERR_MC_COUNT`), `multiple_select` has NO `else` branch.
   - Tested empirically:
     ```python
     # Question with interaction_type: 'multiple_select' and NO options
     res = validate_course_content(json.dumps(course))
     # Result: Course passes validation with 0 errors!
     ```

5. **Observation 3: Missing / Empty `correct_answer` Allowed on `fill_in_the_blank` (`src/validator/schema_validator.py:98`, `src/validator/rules.py:123-185`)**:
   - In `COURSE_SCHEMA`, `correct_answer` is not in `Question`'s `required` list.
   - In `src/validator/rules.py`, there is no validation block for `interaction_type == "fill_in_the_blank"`.
   - Tested empirically:
     ```python
     # Question with interaction_type: 'fill_in_the_blank' and NO correct_answer (or correct_answer: {})
     res = validate_course_content(json.dumps(course))
     # Result: Course passes validation with 0 errors!
     ```

6. **Observation 4: Anti-Giveaway Rule R-16 Behavior on Identical Option Lengths (`src/validator/psychometric_checker.py:55-61`)**:
   - `is_longest = (len_c >= max_d)` and `is_shortest = (len_c <= min_d)`.
   - If an exercise bank author creates options with perfectly identical lengths across all 7 options for every question (e.g. 50 characters each), `len_c >= max_d` and `len_c <= min_d` evaluate to `True` for 100% of items.
   - Tested empirically:
     * `test_course_distribution_all_identical_lengths_triggers_giveaway` triggered both `ERR_GIVEAWAY_COURSE` (longest in 100%) and `ERR_GIVEAWAY_COURSE` (shortest in 100%).

---

## 2. Logic Chain

1. **Premise 1 (R2 Contract for LaTeX Escapes)**:
   - R2 explicitly specifies that the validator must reject: *"LaTeX backslash corruption (including silently-valid escapes that produce control characters)"*.
   - In Observation 3, 11 common math LaTeX commands starting with `b`, `f`, `n`, `r`, `t` (`\norm`, `\ne`, `\boxed`, `\therefore`, `\thickspace`, `\textcolor`, `\bigcap`, `\bigcup`, `\bigoplus`, `\bigotimes`, `\rank`) bypass the lexical scanner because the whitelist is incomplete.
   - During downstream JSON parsing, these commands silently mutate into ASCII control characters.
   - Because these commands are standard in PDE (`sample_content/I__Ecuaciones_en_derivadas_parciales_2026.pdf`), when Milestone 3 generates course content, single-backslash occurrences of these commands will bypass the validator and crash KaTeX rendering on the practice platform (Milestone 2/4).

2. **Premise 2 (R2 Contract for Interaction Types & Scaffolding)**:
   - R2 specifies that multiple-select items must have *"correct count between 1 and n-1"* and schema violations must be rejected.
   - In Observation 4, a `multiple_select` item with 0 options (or `options: null`) bypasses both schema validation and semantic rules, passing with 0 errors.
   - In Observation 5, a `fill_in_the_blank` item without `correct_answer` bypasses all validation passes.
   - When loaded into the practice platform (Milestone 2), a multiple-select item with no options or a fill-in-the-blank item with no answer key cannot be rendered or graded, breaking the student experience.

3. **Premise 3 (Anti-Giveaway Boundaries)**:
   - Psychometric checks in `psychometric_checker.py` were rigorously tested at numerical boundaries:
     * Exact 20.0% longer (`len_c = 120`, `max_d = 100`) passes; exact 21.0% longer (`len_c = 121`) fails.
     * Exact 20.0% shorter (`len_c = 80`, `min_d = 100`) passes; exact 21.0% shorter (`len_c = 79`) fails.
     * Exact 25.0% course longest (`10 / 40 = 25.0%`) passes; 27.5% (`11 / 40 = 27.5%`) fails.
   - These boundaries are strictly correct per the specification.
   - However, Observation 6 reveals that tied lengths count as both longest and shortest, meaning an automated generator cannot make all options equal length without failing R-16.

4. **Conclusion**:
   - Because Observations 3, 4, and 5 allow corrupted or unrenderable/ungradable courses to pass validation with exit code 0, Milestone 1 cannot be approved in its current state. The validator must be hardened before downstream milestones (M2 platform, M3 generator) rely on it.

---

## 3. Caveats

- **Multi-gigabyte stress testing**: We did not test files exceeding 50 MB, as course banks are expected to be between 100 KB and 5 MB.
- ** KaTeX semantic validation**: The validator checks lexical escapes and JSON syntax, but does not execute a full LaTeX macro compiler (e.g. KaTeX AST parse). This is consistent with R2's lexical scope.

---

## 4. Conclusion & Verdict

**Verdict**: **REQUEST_CHANGES**

### Required Changes for Worker M1:

1. **Fix `src/validator/lexical_scanner.py` (Rule R-03)**:
   Expand `LATEX_CONTROL_PREFIXES` to include missing standard math commands, or preferably, in math contexts / string values, treat ANY sequence of `\b`, `\f`, `\n`, `\r`, `\t` immediately followed by ASCII alphabetic characters (e.g. `re.match(r"^[a-zA-Z]{2,}", raw_text[pos:])`) as an unescaped LaTeX command if it's not a recognized JSON escape pattern. At minimum, add to whitelist:
   - `b`: `boxed`, `bigcap`, `bigcup`, `bigoplus`, `bigotimes`, `bigsqcup`, `biguplus`, `bowtie`, `bra`
   - `n`: `norm`, `ne`, `newline`, `not`, `ni`, `null`
   - `r`: `rank`, `real`, `restriction`, `ring`, `rightleftharpoons`, `rightharpoonup`
   - `t`: `therefore`, `thickspace`, `textcolor`, `textnormal`, `textup`, `textsl`, `tensor`
   - `f`: `footnote`

2. **Fix `src/validator/rules.py` (Rule R-12)**:
   Add an `else` branch for `interaction_type == "multiple_select"` when `options` is not a list:
   ```python
   elif itype == "multiple_select":
       if isinstance(options, list):
           ...
       else:
           errors.append(ValidationError(
               rule_id="R-12",
               code="ERR_MS_COUNT",
               message=f"Question '{q_id}' has 0 options; multiple-select items must have between 4 and 6 options",
               item_id=q_id
           ))
   ```

3. **Fix `src/validator/rules.py` & `src/validator/schema_validator.py` (Fill-in-the-Blank Answer Key)**:
   Enforce that questions with `interaction_type == "fill_in_the_blank"` MUST have a non-empty `correct_answer`:
   ```python
   elif itype == "fill_in_the_blank":
       ca = q.get("correct_answer")
       if ca is None or (isinstance(ca, dict) and not ca):
           errors.append(ValidationError(
               rule_id="R-04",
               code="ERR_SCHEMA",
               message=f"Question '{q_id}' of type 'fill_in_the_blank' must specify a valid non-empty 'correct_answer'",
               item_id=q_id
           ))
   ```

---

## 5. Verification Method

To independently reproduce all 14 failure findings:

1. **Run adversarial test suite**:
   ```bash
   python -m pytest tests/test_adversarial_validator.py -v
   ```
   *Observed result*: 14 failed, 21 passed.

2. **Inspect the failing test logs**:
   - `TestAdversarialLatex::test_unescaped_latex_command_starting_with_control_prefix` (11 failures for unescaped LaTeX commands).
   - `TestMixedQuestionsAndGraphs::test_multiple_select_missing_options_blind_spot` (failure confirming multiple-select missing options passes).
   - `TestMixedQuestionsAndGraphs::test_multiple_select_null_options_blind_spot` (failure confirming multiple-select null options passes).
   - `TestMixedQuestionsAndGraphs::test_fill_in_the_blank_missing_correct_answer_blind_spot` (failure confirming fill-in-the-blank missing answer passes).

3. **Invalidation condition**:
   Worker fixes items 1, 2, and 3 above in `src/validator/`, re-runs:
   ```bash
   python -m pytest tests/validator -v
   python -m pytest tests/test_adversarial_validator.py -v
   ```
   When all 67 baseline tests AND all 35 adversarial tests pass (102 passed, 0 failed), the challenge is resolved and Milestone 1 can be APPROVED.
