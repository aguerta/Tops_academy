# Empirical Challenge Report: Milestone 1 Exercise Bank Format & Validator

**Challenger**: Challenger 2 (`challenger_m1_2`)  
**Date**: 2026-10-11T01:30:00Z  
**Verdict**: **REQUEST_CHANGES**  
**Assigned Directory**: `g:\Mi unidad\Competence_analyser\.agents\teamwork\challenger_m1_2`  

---

## 1. Observation

1. **Baseline Test Execution**:
   - Running `python -m pytest tests/validator -v` succeeded with 67 passed tests in 13.30s.
   - Fixture verification on `system_prompts/output_example_exercises.json` exited with code 1, and `courses/fixtures/28_valid_complete_course.json` exited with code 0.

2. **Empirical Stress Test Execution**:
   - An adversarial empirical test battery was written and executed at `tests/validator/test_empirical_stress.py`.
   - Running `python -m pytest tests/validator/test_empirical_stress.py -v` produced 6 test failures exposing concrete false negatives:
     ```
     FAILED tests/validator/test_empirical_stress.py::test_fn_multiselect_missing_options
     FAILED tests/validator/test_empirical_stress.py::test_fn_fill_in_the_blank_missing_correct_answer
     FAILED tests/validator/test_empirical_stress.py::test_fn_fill_in_the_blank_empty_dict_correct_answer
     FAILED tests/validator/test_empirical_stress.py::test_fn_fill_in_the_blank_empty_list_correct_answer
     FAILED tests/validator/test_empirical_stress.py::test_fn_latex_newline_command_escape
     FAILED tests/validator/test_empirical_stress.py::test_fn_latex_not_command_escape
     ```

3. **False Negative FN-1: `multiple_select` missing `options` property slips through unflagged**:
   - Tested in `test_fn_multiselect_missing_options`:
     ```python
     base['questions'][0]['interaction_type'] = 'multiple_select'
     del base['questions'][0]['options']
     res = validate_course_content(json.dumps(base))
     # Output: is_valid: True, errors: []
     ```
   - In `src/validator/schema_validator.py` lines 97-103:
     ```python
     "Question": {
         "type": "object",
         "required": [
             "id",
             "competency_id",
             "interaction_type",
             "stem",
             "hints"
         ],
     ```
     `options` is NOT in the `required` list of `Question`.
   - In `src/validator/rules.py` lines 167-183:
     ```python
     elif itype == "multiple_select":
         if isinstance(options, list):
             n_opts = len(options)
             ...
     ```
     Unlike `multiple_choice_7_options` (which includes an `else` branch appending `ERR_MC_COUNT`), `multiple_select` has NO `else` branch. When `options` is omitted or `None`, `isinstance(options, list)` is `False`, bypassing all checks.

4. **False Negative FN-2 & FN-3: `fill_in_the_blank` without `correct_answer` (or with `{}` or `[]`) slips through unflagged**:
   - Tested in `test_fn_fill_in_the_blank_missing_correct_answer`:
     ```python
     base['questions'][0]['interaction_type'] = 'fill_in_the_blank'
     del base['questions'][0]['options']
     del base['questions'][0]['correct_answer']
     res = validate_course_content(json.dumps(base))
     # Output: is_valid: True, errors: []
     ```
   - In `src/validator/schema_validator.py`, `correct_answer` is not in `required`.
   - Furthermore, in lines 162-180 of `COURSE_SCHEMA`:
     ```python
     {
         "type": "object",
         "properties": {
             "value": { ... },
             "expression": { "type": "string" },
             "tolerance": { "type": "number" },
             "canonical_algebraic": { "type": "string" },
             "accepted_equivalents": { "type": "array", "items": { "type": "string" } }
         }
     }
     ```
     No properties are required inside the object, and `additionalProperties` is not set to `false`. Therefore `{}` or `{"bogus": 123}` passes Draft-07 schema validation.
   - In `src/validator/rules.py`, there is zero logic verifying `fill_in_the_blank` items.

5. **False Negative FN-4 & FN-5: Raw single-backslash LaTeX keywords `\newline` and `\not` unintercepted in Pass 1**:
   - In `src/validator/lexical_scanner.py` lines 26-30:
     ```python
     "n": {
         "nu", "nabla", "neq", "neg", "notin", "nsubseteq", "nexists",
         "natural", "nearrow", "nwarrow", "normalsize", "nparallel",
         "noindent", "nonumber"
     }
     ```
     Neither `"newline"` nor `"not"` is present in `LATEX_CONTROL_PREFIXES["n"]`.
   - When raw JSON contains `\newline` or `\not=`, `scan_lexical` treats `\n` as an escaped newline (lines 210-213) and the remaining letters as plain text. The standard JSON parser decodes this to ASCII `\n` (0x0A) followed by `"ewline"` or `"ot="`, silently corrupting mathematical formulas without throwing an error.

6. **Psychometric Distractor Length Symmetry & Uniformity (R-15 & R-16)**:
   - Evaluated in `test_psychometric_r15_exact_upper_boundary` (len_c = 1.20 * max_d) and `test_psychometric_r15_exact_lower_boundary` (len_c = 0.80 * min_d): Both boundaries pass as valid (exit code 0).
   - Evaluated in `test_psychometric_r16_exact_25_percent_longest` (5 of 20 items = 25.0%): Passes exit code 0.
   - In `test_psychometric_r16_boundary_exceeded_26_percent` (6 of 20 items = 30.0%): Fails with `[ERR_GIVEAWAY_COURSE]`.
   - However, when all options in every MCQ have identical character length (e.g. 50 characters):
     ```python
     is_longest = (len_c >= max_d)  # True (50 >= 50)
     is_shortest = (len_c <= min_d) # True (50 <= 50)
     ```
     Because of the tie condition `(strictly or tied)` mandated in R2, uniform-length options count as both longest AND shortest in 100% of items, triggering R-16 errors on both directions. This is compliant with R2, but represents a critical constraint that Milestone 3 exercise generation must account for (options cannot be padded to identical lengths).

7. **Graphing Object & Scale Robustness**:
   - Declarative graphs with vector properties (`x_range`, `y_range`, `curves`, `points` with `style: "closed"`/`"open"`) validate cleanly (`test_graph_vector_complete_specification`).
   - High-load test with 500 questions across 5 competencies executes and passes validation in under 0.15s (`test_large_course_500_questions`).

---

## 2. Logic Chain

1. **Premise 1 (Platform Compatibility & Grading Contract)**:
   - Acceptance Criteria R1 and R2 require the platform to grade all three interaction types (`multiple_choice_7_options`, `multiple_select`, and `fill_in_the_blank`) and isolate invalid courses.
   - If a course containing `multiple_select` questions without options or `fill_in_the_blank` questions without answer keys is admitted by the validator as valid (Observation 3, Observation 4), the platform runner will encounter `undefined` properties or be completely unable to evaluate correctness.
   - Therefore, the validator suffers from under-validation (False Negatives).

2. **Premise 2 (Silent Control Character Interception Contract)**:
   - Requirement R2 explicitly states: "The validator must reject: ... LaTeX backslash corruption (including silently-valid escapes that produce control characters)".
   - Standard LaTeX syntax contains `\newline` and `\not` (e.g. `\not=`). In raw JSON, `\newline` and `\not` start with `\n` (valid escape for linefeed).
   - Because `lexical_scanner.py` did not include `"newline"` and `"not"` in `LATEX_CONTROL_PREFIXES["n"]` (Observation 5), raw unescaped LaTeX commands silently bypass Pass 1 and mutate into control characters in Pass 2.
   - Therefore, the lexical scanner fails to satisfy the complete R2 specification for silent control character interception.

3. **Premise 3 (Actionable Remediation Scoping)**:
   - These vulnerabilities do not require structural rewrites. They are scoped and actionable:
     * In `src/validator/schema_validator.py`: Add conditional validation or require `options` for choice questions, require `correct_answer` for `fill_in_the_blank`, and require `{"anyOf": [{"required": ["value"]}, {"required": ["expression"]}]}` on the `correct_answer` object definition.
     * In `src/validator/rules.py`: Add an `else` branch for `multiple_select` when `options` is missing or not a list (matching line 158 for MCQ), and add a check verifying `correct_answer` presence and non-emptiness for `fill_in_the_blank`.
     * In `src/validator/lexical_scanner.py`: Add `"newline"`, `"not"`, `"bigcup"`, `"bigcap"`, `"therefore"` to `LATEX_CONTROL_PREFIXES`.

---

## 3. Caveats

- **Frontend Browser Execution**: This empirical challenge evaluated the Python validator package, lexical scanner, schema rules, psychometric distributions, and synthetic fixtures. Headless browser rendering of SVGs and KaTeX math in the React platform belongs to Milestone 2 (E2E Playwright track).
- **Option ID Uniqueness**: Schema currently does not enforce global uniqueness of option IDs within a question (`opt_a`, `opt_b`). While not fatal if UI maps indices, declaring unique option IDs per item is recommended.

---

## 4. Conclusion

**Verdict: REQUEST_CHANGES**

Milestone 1 is well-architected and handles the 28 baseline fixtures correctly. However, empirical stress testing has revealed 5 critical False Negative vulnerabilities where malformed and ungradable courses slip through unflagged:
1. `multiple_select` questions missing `options` are accepted as valid (`is_valid = True`).
2. `fill_in_the_blank` questions missing `correct_answer` are accepted as valid (`is_valid = True`).
3. `fill_in_the_blank` questions with empty `{}` or `[]` answers are accepted as valid (`is_valid = True`).
4. Single-backslash LaTeX `\newline` escapes are not intercepted and silently corrupt.
5. Single-backslash LaTeX `\not` escapes are not intercepted and silently corrupt.

The worker (`worker_m1_validator`) must implement these remediations and verify that `tests/validator/test_empirical_stress.py` passes 100%.

---

## 5. Verification Method

To independently reproduce all empirical findings:

1. **Run the empirical stress test battery**:
   ```bash
   python -m pytest tests/validator/test_empirical_stress.py -v
   ```
   *Expected reproduction result*: 6 tests fail with assertion errors demonstrating the false negatives described in Observation 2.

2. **Run programmatic reproduction for missing options in multi-select**:
   ```bash
   python -c "import json; from pathlib import Path; from src.validator.core import validate_course_content; base = json.loads(Path('courses/fixtures/28_valid_complete_course.json').read_text(encoding='utf-8')); base['questions'][0]['interaction_type'] = 'multiple_select'; del base['questions'][0]['options']; res = validate_course_content(json.dumps(base)); print('is_valid:', res.is_valid)"
   ```
   *Expected reproduction result*: Prints `is_valid: True` (demonstrating false negative).

3. **Run programmatic reproduction for missing answer in fill-in-the-blank**:
   ```bash
   python -c "import json; from pathlib import Path; from src.validator.core import validate_course_content; base = json.loads(Path('courses/fixtures/28_valid_complete_course.json').read_text(encoding='utf-8')); base['questions'][0]['interaction_type'] = 'fill_in_the_blank'; del base['questions'][0]['options']; del base['questions'][0]['correct_answer']; res = validate_course_content(json.dumps(base)); print('is_valid:', res.is_valid)"
   ```
   *Expected reproduction result*: Prints `is_valid: True` (demonstrating false negative).
