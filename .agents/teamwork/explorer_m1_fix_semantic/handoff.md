# Milestone 1 Remediation Investigation Report: Semantic & Schema Validation

**Agent**: Explorer 2 (`explorer_m1_fix_semantic`)  
**Date**: 2026-10-11T01:40:00Z  
**Target Milestone**: Milestone 1 (Exercise Bank Format & Reference Validator, R2)  
**Report Type**: Hard Handoff  
**Plan Reference**: `g:\Mi unidad\Competence_analyser\.agents\teamwork\explorer_m1_fix_semantic\semantic_fix_plan.md`  

---

## 1. Observation

1. **Current Test Failures in Baseline Test Suites**:
   - Running `python -m pytest tests/validator/test_empirical_stress.py -v`:
     ```
     FAILED tests/validator/test_empirical_stress.py::test_fn_multiselect_missing_options - AssertionError: FALSE NEGATIVE: multiple_select question without 'options' was accepted as valid!
     FAILED tests/validator/test_empirical_stress.py::test_fn_fill_in_the_blank_missing_correct_answer - AssertionError: FALSE NEGATIVE: fill_in_the_blank question without 'correct_answer' was accepted as valid!
     FAILED tests/validator/test_empirical_stress.py::test_fn_fill_in_the_blank_empty_dict_correct_answer - AssertionError: FALSE NEGATIVE: fill_in_the_blank question with empty correct_answer {} was accepted as valid!
     FAILED tests/validator/test_empirical_stress.py::test_fn_fill_in_the_blank_empty_list_correct_answer - AssertionError: FALSE NEGATIVE: fill_in_the_blank question with empty list correct_answer [] was accepted as valid!
     ```
   - Running `python -m pytest tests/test_adversarial_validator.py -v`:
     ```
     FAILED tests/test_adversarial_validator.py::TestMixedQuestionsAndGraphs::test_multiple_select_missing_options_blind_spot - AssertionError: BLIND SPOT: multiple_select question Q-030 completely omitted 'options', but validator generated NO error for it!
     FAILED tests/test_adversarial_validator.py::TestMixedQuestionsAndGraphs::test_multiple_select_null_options_blind_spot - AssertionError: multiple_select with null options must produce an error
     FAILED tests/test_adversarial_validator.py::TestMixedQuestionsAndGraphs::test_fill_in_the_blank_missing_correct_answer_blind_spot - AssertionError: BLIND SPOT: fill_in_the_blank question Q-030 completely omitted 'correct_answer', but validator generated NO error for it!
     ```

2. **Source Inspection of `src/validator/schema_validator.py`**:
   - Lines 95-103:
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
     Neither `"options"` nor `"correct_answer"` is listed in the `required` properties of `Question`. No conditional schemas (`allOf`, `if`/`then`) exist to enforce presence according to `interaction_type`.
   - Lines 155-182:
     ```python
     "correct_answer": {
         "oneOf": [
             { "type": "string" },
             {
                 "type": "array",
                 "items": { "type": "string" }
             },
             {
                 "type": "object",
                 "properties": {
                     "value": { ... },
                     "expression": { "type": "string" },
                     ...
                 }
             }
         ]
     }
     ```
     There are no minimum length (`minLength: 1`) or item (`minItems: 1`) constraints. In the object schema, there are no required properties, meaning `{}` or `{"irrelevant": 123}` passes Draft-07 validation.
   - Lines 274-297: `validate_schema` creates `ValidationError` with `item_id=None` and generic message `Field 'questions.29.options': None is not of type 'array'`. The specific question ID `"Q-030"` is not included in the error model or diagnostic string.

3. **Source Inspection of `src/validator/rules.py`**:
   - Lines 166-184:
     ```python
     # R-12 & R-13: Multiple Select (4 to 6 options, 1 to n-1 correct)
     elif itype == "multiple_select":
         if isinstance(options, list):
             n_opts = len(options)
             ...
     ```
     Unlike `multiple_choice_7_options` (lines 157-163), which includes an `else` branch appending `ERR_MC_COUNT`, `multiple_select` has NO `else` branch. When `options` is missing or null, `isinstance(options, list)` evaluates to `False`, completely skipping R-12 and R-13.
   - Lines 138-184: There is no branch for `elif itype == "fill_in_the_blank":`. Fill-in-the-blank items are never inspected for answer key existence or non-emptiness.

4. **Empirical Verification of Proposed Remediation**:
   - A scratch test harness `verify_proposed_logic.py` was executed against all test scenarios:
     `$env:PYTHONPATH="."; python .agents/teamwork/explorer_m1_fix_semantic/verify_proposed_logic.py`
     Result: All 9 invalid edge cases (None, {}, [], "", "   ", {"expression": ""}, {"value": ""}, {"tolerance": 0.001}, {"random": 1}) were rejected with targeted error codes and question IDs, while all 10 valid answer structures and baseline course 28 passed with 0 errors.

---

## 2. Logic Chain

1. **Premise 1 (Grading & Platform Integrity)**:
   - Acceptance Criteria R1 and R2 mandate that courses must be gradable across all three interaction types (`multiple_choice_7_options`, `multiple_select`, `fill_in_the_blank`).
   - If a course containing `multiple_select` items without options or `fill_in_the_blank` items without answer keys passes validation with exit code 0 (Observation 1), the practice platform (Milestone 2) will fail at runtime when rendering options or grading student submissions.

2. **Premise 2 (Schema Specification Enforcement)**:
   - Observation 2 demonstrates that Draft-07 JSON schema validation in `schema_validator.py` allows questions of type `multiple_select` to omit `options` and questions of type `fill_in_the_blank` to omit `correct_answer` or provide empty placeholders (`{}`, `[]`, `""`).
   - Using Draft-07 `allOf` with `if`/`then` conditional schemas allows declarative enforcement of required fields per `interaction_type`.
   - Adding `minLength: 1`, `minItems: 1`, and `anyOf: [{"required": ["value"]}, {"required": ["expression"]}]` cleanly rejects empty objects and collections while preserving all valid mathematical representations (strings, numbers, arrays, and expression dicts).

3. **Premise 3 (Domain Rules & Diagnostic Symmetry)**:
   - Observation 3 shows an asymmetry between `multiple_choice_7_options` and `multiple_select`: MCQ explicitly emits `R-10: ERR_MC_COUNT` when `options` is not a list, whereas `multiple_select` silently ignores missing/null options.
   - Adding an `else:` branch to `multiple_select` emitting `R-12: ERR_MS_COUNT` (with 0 options) restores symmetric rule enforcement.
   - Adding a dedicated `elif itype == "fill_in_the_blank":` block in `check_semantic_rules()` guarantees that empty or missing answer keys emit explicit errors with `rule_id="R-04"` and `code="ERR_MISSING_ANSWER"`.

4. **Premise 4 (Item Context Extraction)**:
   - Tests assert `item_id == "Q-030"` or `"Q-030" in str(e)`.
   - By querying `data["questions"][path[1]]["id"]` inside `validate_schema()`, the validator can populate `item_id` and include `(question 'Q-030')` in the diagnostic message, satisfying automated tests and providing immediate human debugging context.

5. **Conclusion**:
   - Implementing this two-layer strategy eliminates all 7 semantic/schema test failures across `test_empirical_stress.py` and `test_adversarial_validator.py` without causing any regressions in the 28 baseline fixtures.

---

## 3. Caveats

1. **Lexical Scanner Escapes**: This report and plan focus strictly on Pass 2 (Schema and Semantic Rules). LaTeX silent escape issues (`\norm`, `\ne`, `\not`, `\newline`, etc.) belong to Pass 1 (`lexical_scanner.py`) and are addressed in Explorer 1's scope.
2. **CLI Entry Point Packaging**: The `ModuleNotFoundError: No module named 'src'` issue when invoking `validate-course` requires relative imports inside `src/validator/` (e.g. `from .models import ValidationError`) and package definition in `pyproject.toml`.
3. **No Code Modification Undertaken**: In accordance with the Explorer archetype constraints, no production files in `src/` were modified. The proposed logic was verified exclusively via a standalone scratch test in this agent's directory.

---

## 4. Conclusion

The semantic and schema blind spots causing the Milestone 1 Gate failure are clearly identified and straightforward to remediate:
1. In `src/validator/schema_validator.py`:
   - Add Draft-07 `allOf` conditional requirements for `options` (MCQ and MS) and `correct_answer` (FIB).
   - Constrain `correct_answer` properties with `minLength: 1`, `minItems: 1`, and object `anyOf: [{"required": ["value"]}, {"required": ["expression"]}]`.
   - Populate `item_id` and item context in `validate_schema()`.
2. In `src/validator/rules.py`:
   - Add `else:` branch on `multiple_select` emitting `R-12: ERR_MS_COUNT`.
   - Add `elif itype == "fill_in_the_blank":` branch emitting `R-04: ERR_MISSING_ANSWER` when answer key is missing or empty.
   - Guard R-13 to evaluate only when `n_opts > 0`.
3. Switch internal imports in `src/validator/` to relative imports (`from .models import ValidationError`).

Full replacement code and line-by-line diffs are documented in `semantic_fix_plan.md`.

---

## 5. Verification Method

1. **Dry-Run Proposed Logic**:
   ```powershell
   $env:PYTHONPATH="."; python .agents/teamwork/explorer_m1_fix_semantic/verify_proposed_logic.py
   ```
   *Expected output*: `ALL INVALID AND VALID FIB CASES VERIFIED SUCCESSFULLY!`

2. **Independent Verification of Fixes (After Implementation by Worker)**:
   - Run empirical stress test suite:
     ```powershell
     python -m pytest tests/validator/test_empirical_stress.py -k "multiselect or fill_in_the_blank" -v
     ```
     *Must pass 100% of tests (4 previously failing tests now pass).*
   - Run adversarial mixed questions suite:
     ```powershell
     python -m pytest tests/test_adversarial_validator.py -k "TestMixedQuestionsAndGraphs" -v
     ```
     *Must pass 100% of tests (3 previously failing tests now pass).*
   - Run baseline fixture suite:
     ```powershell
     python -m pytest tests/validator/test_validator.py -v
     ```
     *Must pass 100% of all 28 fixtures (0 regressions).*
