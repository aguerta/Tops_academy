# Remediation Plan: Semantic & Schema Validation Hardening

**Author**: Explorer 2 (`explorer_m1_fix_semantic`)  
**Target Subsystem**: `src/validator/schema_validator.py` and `src/validator/rules.py`  
**Milestone**: Milestone 1 (Exercise Bank Format & Reference Validator, R2)  
**Date**: 2026-10-11T01:40:00Z  

---

## 1. Problem Statement & Root Cause Analysis

During the Milestone 1 Gate evaluation, Reviewer 2, Challenger 1, and Challenger 2 identified critical false-negative vulnerabilities where ungradable and malformed question items pass validation with exit code 0 (`is_valid == True`).

### Vulnerability 1: `multiple_select` items omitting or nullifying `options` pass unflagged
- **Observed Behavior**:
  - In `test_empirical_stress.py::test_fn_multiselect_missing_options`, deleting `options` on a `multiple_select` item produces 0 validation errors.
  - In `test_adversarial_validator.py::test_multiple_select_missing_options_blind_spot`, omitting `options` produces 0 validation errors.
  - In `test_adversarial_validator.py::test_multiple_select_null_options_blind_spot`, setting `options: None` emits a schema error (`Field 'questions.29.options': None is not of type 'array'`), but `item_id` is `None` and the error message does not contain `"Q-030"`, failing item-level diagnostics.
- **Root Cause**:
  1. **Schema level** (`src/validator/schema_validator.py:97-103`): `COURSE_SCHEMA["definitions"]["Question"]` defines `required: ["id", "competency_id", "interaction_type", "stem", "hints"]`. The `"options"` field is NOT in the `required` list, and no conditional schema (`allOf` with `if`/`then`) enforces that `multiple_select` or `multiple_choice_7_options` must have `options`.
  2. **Semantic rules level** (`src/validator/rules.py:166-184`):
     ```python
     elif itype == "multiple_select":
         if isinstance(options, list):
             n_opts = len(options)
             ...
     ```
     Unlike `multiple_choice_7_options` (lines 157-163, which has an `else` branch appending `ValidationError(rule_id="R-10", code="ERR_MC_COUNT", ...)`), `multiple_select` has NO `else` branch. When `options` is missing or `None`, `isinstance(options, list)` evaluates to `False`, silently bypassing Rule R-12 (`ERR_MS_COUNT`) and Rule R-13 (`ERR_MS_CORRECT`).

---

### Vulnerability 2: `fill_in_the_blank` items missing or having empty `correct_answer` pass unflagged
- **Observed Behavior**:
  - In `test_empirical_stress.py::test_fn_fill_in_the_blank_missing_correct_answer`, omitting `correct_answer` produces 0 validation errors.
  - In `test_empirical_stress.py::test_fn_fill_in_the_blank_empty_dict_correct_answer`, setting `correct_answer: {}` produces 0 validation errors.
  - In `test_empirical_stress.py::test_fn_fill_in_the_blank_empty_list_correct_answer`, setting `correct_answer: []` produces 0 validation errors.
  - In `test_adversarial_validator.py::test_fill_in_the_blank_missing_correct_answer_blind_spot`, completely omitting `correct_answer` produces 0 validation errors.
- **Root Cause**:
  1. **Schema level** (`src/validator/schema_validator.py:97-103, 155-182`):
     - `Question` does not require `correct_answer`.
     - `correct_answer` schema allows `{ "type": "string" }` without `minLength: 1` (accepting `""`).
     - `correct_answer` schema allows `{ "type": "array" }` without `minItems: 1` (accepting `[]`).
     - `correct_answer` schema allows `{ "type": "object" }` without requiring either `value` or `expression` (accepting `{}` or objects with arbitrary non-standard keys).
  2. **Semantic rules level** (`src/validator/rules.py`):
     - There is zero validation logic for `itype == "fill_in_the_blank"`. The parser iterates over questions and evaluates `multiple_choice_7_options` and `multiple_select`, but completely ignores `fill_in_the_blank`.

---

### Vulnerability 3: Missing `item_id` and Question Context in Schema Error Diagnostics
- **Observed Behavior**:
  - Schema errors report: `Field 'questions.29.options': None is not of type 'array'` with `item_id=None`.
  - Downstream diagnostic consumers and test suites (e.g. `test_adversarial_validator.py`) inspect `item_id == "Q-030"` or `"Q-030" in str(e)`. Because the error only contains the zero-based array index, locating the faulted question in large files (500+ items) requires manual index mapping.
- **Root Cause**:
  - In `schema_validator.py:274-297`, `validate_schema` creates `ValidationError` with `rule_id="R-04"`, `code="ERR_SCHEMA"`, but leaves `item_id=None` and does not query the question object to obtain its `"id"`.

---

## 2. Comprehensive Fix Strategy

A two-layer defense-in-depth architecture is required:
1. **Layer 1: Schema Validation (`src/validator/schema_validator.py`)**: Draft-07 structural constraints enforcing presence of required fields per question type and enforcing non-emptiness of answer models.
2. **Layer 2: Semantic Rules Validation (`src/validator/rules.py`)**: Domain-specific pedagogical rules with explicit error emission for missing options (`R-12: ERR_MS_COUNT`) and missing/unusable answer keys (`R-04: ERR_MISSING_ANSWER`).

---

### Layer 1: Schema Hardening (`src/validator/schema_validator.py`)

#### 1.1 Type-Conditional Field Requirements via Draft-07 `allOf`
In `COURSE_SCHEMA["definitions"]["Question"]`, add `allOf` to conditionally require:
- If `interaction_type == "multiple_choice_7_options"` -> require `["options"]`
- If `interaction_type == "multiple_select"` -> require `["options"]`
- If `interaction_type == "fill_in_the_blank"` -> require `["correct_answer"]`

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
            "allOf": [
                {
                    "if": {
                        "properties": {
                            "interaction_type": {"const": "multiple_choice_7_options"}
                        }
                    },
                    "then": {
                        "required": ["options"]
                    }
                },
                {
                    "if": {
                        "properties": {
                            "interaction_type": {"const": "multiple_select"}
                        }
                    },
                    "then": {
                        "required": ["options"]
                    }
                },
                {
                    "if": {
                        "properties": {
                            "interaction_type": {"const": "fill_in_the_blank"}
                        }
                    },
                    "then": {
                        "required": ["correct_answer"]
                    }
                }
            ],
            "properties": {
                ...
            }
        }
```

#### 1.2 Non-Empty `correct_answer` Schema Definition
Update `COURSE_SCHEMA["definitions"]["Question"]["properties"]["correct_answer"]`:
1. **String answer**: Add `"minLength": 1` to reject empty strings `""`.
2. **Numeric answer**: Add `{ "type": "number" }` at top-level `oneOf` to accept numeric values directly (e.g. `42`, `0.5`).
3. **Array answer**: Add `"minItems": 1` and items `"minLength": 1` to reject empty lists `[]` or lists of empty strings.
4. **Object answer**:
   - Add `"minProperties": 1`.
   - Add `"anyOf": [{"required": ["value"]}, {"required": ["expression"]}]` to ensure at least one actionable answer attribute is defined.
   - For `"expression"`: `"type": "string", "minLength": 1`.
   - For `"value"`:
     ```python
     "value": {
         "oneOf": [
             {"type": "string", "minLength": 1},
             {"type": "number"},
             {
                 "type": "array",
                 "minItems": 1,
                 "items": {"type": "string", "minLength": 1}
             }
         ]
     }
     ```
   - For `"canonical_algebraic"`: `"type": "string", "minLength": 1`.
   - For `"accepted_equivalents"`: `"type": "array", "items": {"type": "string", "minLength": 1}`.

#### 1.3 Pinpointed Diagnostic Reporting in `validate_schema()`
Update `validate_schema(data: dict[str, Any]) -> list[ValidationError]` to extract `item_id` when `err.path` originates inside `questions` or `competencies`:
```python
        path = list(err.path)
        item_id = None
        item_context = ""

        if len(path) >= 2 and path[0] == "questions" and isinstance(path[1], int):
            questions = data.get("questions")
            if isinstance(questions, list) and 0 <= path[1] < len(questions):
                q = questions[path[1]]
                if isinstance(q, dict) and "id" in q:
                    item_id = str(q["id"])
                    item_context = f" (question '{item_id}')"
        elif len(path) >= 2 and path[0] == "competencies" and isinstance(path[1], int):
            competencies = data.get("competencies")
            if isinstance(competencies, list) and 0 <= path[1] < len(competencies):
                comp = competencies[path[1]]
                if isinstance(comp, dict) and "id" in comp:
                    item_id = str(comp["id"])
                    item_context = f" (competency '{item_id}')"

        if err.validator == "required":
            match = re.search(r"'([^']+)' is a required property", err.message)
            missing_field = match.group(1) if match else "unknown"
            if len(path) == 0:
                msg = f"Missing required top-level field '{missing_field}'"
            else:
                path_str = ".".join(str(p) for p in path)
                msg = f"Missing required field '{missing_field}' at '{path_str}'{item_context}"
        else:
            if len(path) == 0:
                msg = f"Root schema violation: {err.message}"
            else:
                path_str = ".".join(str(p) for p in path)
                msg = f"Field '{path_str}'{item_context}: {err.message}"

        errors.append(ValidationError(
            rule_id="R-04",
            code="ERR_SCHEMA",
            message=msg,
            item_id=item_id,
            details={"validator": err.validator, "path": [str(p) for p in path]}
        ))
```

---

### Layer 2: Semantic Rules Hardening (`src/validator/rules.py`)

#### 2.1 Explicit Error Emission for Missing/Empty Options on `multiple_select` (Rule R-12)
In `check_semantic_rules()`:
Add an `else` branch for `itype == "multiple_select"` when `options` is not a list.
Also guard the R-13 calculation so it only runs when `n_opts > 0`.

```python
        # R-12 & R-13: Multiple Select (4 to 6 options, 1 to n-1 correct)
        elif itype == "multiple_select":
            if isinstance(options, list):
                n_opts = len(options)
                if n_opts < 4 or n_opts > 6:
                    errors.append(ValidationError(
                        rule_id="R-12",
                        code="ERR_MS_COUNT",
                        message=f"Question '{q_id}' has {n_opts} options; multiple-select items must have between 4 and 6 options",
                        item_id=q_id
                    ))
                if n_opts > 0:
                    k_correct = sum(1 for opt in options if isinstance(opt, dict) and opt.get("is_correct") is True)
                    if k_correct < 1 or k_correct >= n_opts:
                        errors.append(ValidationError(
                            rule_id="R-13",
                            code="ERR_MS_CORRECT",
                            message=f"Question '{q_id}' has {k_correct} correct options out of {n_opts}; multiple-select items must have between 1 and n-1 correct options",
                            item_id=q_id
                        ))
            else:
                errors.append(ValidationError(
                    rule_id="R-12",
                    code="ERR_MS_COUNT",
                    message=f"Question '{q_id}' has 0 options; multiple-select items must have between 4 and 6 options",
                    item_id=q_id
                ))
```

#### 2.2 Explicit Validation for `fill_in_the_blank` (Rule R-04 / `ERR_MISSING_ANSWER`)
In `check_semantic_rules()`, add an `elif itype == "fill_in_the_blank":` block that validates:
- `correct_answer` must exist and not be `None`.
- If string: `ans.strip()` must be non-empty.
- If number: `isinstance(ans, (int, float)) and not isinstance(ans, bool)` is valid.
- If list: must have `len(ans) > 0` and at least one non-empty string.
- If dict: must have `len(ans) > 0` and either a valid non-empty `value` or a valid non-empty `expression`.
- Otherwise: emit `ValidationError(rule_id="R-04", code="ERR_MISSING_ANSWER", message=f"Question '{q_id}' of type 'fill_in_the_blank' must specify a valid non-empty 'correct_answer' with expression or value", item_id=q_id)`.

```python
        # Fill-in-the-Blank Answer Key Validation
        elif itype == "fill_in_the_blank":
            ans = q.get("correct_answer")
            is_valid_ans = False

            if isinstance(ans, str) and ans.strip():
                is_valid_ans = True
            elif isinstance(ans, (int, float)) and not isinstance(ans, bool):
                is_valid_ans = True
            elif isinstance(ans, list) and len(ans) > 0 and any(isinstance(x, str) and bool(x.strip()) for x in ans):
                is_valid_ans = True
            elif isinstance(ans, dict) and len(ans) > 0:
                val = ans.get("value")
                expr = ans.get("expression")
                has_valid_val = (
                    (isinstance(val, str) and bool(val.strip()))
                    or (isinstance(val, (int, float)) and not isinstance(val, bool))
                    or (isinstance(val, list) and len(val) > 0 and any(isinstance(x, str) and bool(x.strip()) for x in val))
                )
                has_valid_expr = isinstance(expr, str) and bool(expr.strip())
                if has_valid_val or has_valid_expr:
                    is_valid_ans = True

            if not is_valid_ans:
                errors.append(ValidationError(
                    rule_id="R-04",
                    code="ERR_MISSING_ANSWER",
                    message=f"Question '{q_id}' of type 'fill_in_the_blank' must specify a valid non-empty 'correct_answer' with expression or value",
                    item_id=q_id
                ))
```

#### 2.3 Packaging & Import Portability Fixes
In both `src/validator/schema_validator.py` and `src/validator/rules.py`:
Change:
```python
from src.validator.models import ValidationError
```
to:
```python
from .models import ValidationError
```
This resolves the `ModuleNotFoundError: No module named 'src'` issue when installed via `pip install -e .` and imported outside the repository root.

---

## 3. Targeted Test Cases & Expected Outcomes

| Test Case | Prior Result | Proposed Result | Validating Mechanism |
|---|---|---|---|
| `test_fn_multiselect_missing_options` | FAIL (accepted exit 0) | **PASS** (rejected exit 1) | Schema: missing required field `options`; Rules: `R-12: ERR_MS_COUNT` (0 options) |
| `test_fn_multiselect_options_null` | FAIL (accepted exit 0) | **PASS** (rejected exit 1) | Schema: `options` is not of type array; Rules: `R-12: ERR_MS_COUNT` (0 options) |
| `test_fn_fill_in_the_blank_missing_correct_answer` | FAIL (accepted exit 0) | **PASS** (rejected exit 1) | Schema: missing required field `correct_answer`; Rules: `R-04: ERR_MISSING_ANSWER` |
| `test_fn_fill_in_the_blank_empty_dict_correct_answer` | FAIL (accepted exit 0) | **PASS** (rejected exit 1) | Schema: `{}` fails `anyOf` value/expression; Rules: `R-04: ERR_MISSING_ANSWER` |
| `test_fn_fill_in_the_blank_empty_list_correct_answer` | FAIL (accepted exit 0) | **PASS** (rejected exit 1) | Schema: `[]` fails `minItems: 1`; Rules: `R-04: ERR_MISSING_ANSWER` |
| `test_multiple_select_missing_options_blind_spot` | FAIL (no error on Q-030) | **PASS** (error on Q-030) | Item ID populated in `ValidationError.item_id="Q-030"` and message |
| `test_multiple_select_null_options_blind_spot` | FAIL (no error on Q-030) | **PASS** (error on Q-030) | Item ID populated in `ValidationError.item_id="Q-030"` and message |
| `test_fill_in_the_blank_missing_correct_answer_blind_spot` | FAIL (no error on Q-030) | **PASS** (error on Q-030) | Item ID populated in `ValidationError.item_id="Q-030"` and message |
| `test_all_fixtures_programmatic` (all 28 fixtures) | PASS | **PASS** (no regressions) | All 28 fixtures continue to match expected exit codes and diagnostics |
| Valid course with mixed interaction types | PASS | **PASS** | Valid courses with expressions/values/options pass with 0 errors |

---

## 4. Empirical Validation Script

To verify this logic independently prior to source modification, run:
```powershell
$env:PYTHONPATH="."; python .agents/teamwork/explorer_m1_fix_semantic/verify_proposed_logic.py
```
**Empirical output**:
```
Test 1 (MS missing options): ["[ERR_SCHEMA] Missing required field 'options' at 'questions.0' (question 'Q-001')", "[ERR_MS_COUNT] Question 'Q-001' has 0 options; multiple-select items must have between 4 and 6 options"]
Test 2 (MS null options): ["[ERR_SCHEMA] Field 'questions.0.options' (question 'Q-001'): None is not of type 'array'", "[ERR_MS_COUNT] Question 'Q-001' has 0 options; multiple-select items must have between 4 and 6 options"]
Test 3 (FIB missing answer): ["[ERR_SCHEMA] Missing required field 'correct_answer' at 'questions.0' (question 'Q-001')", "[ERR_MISSING_ANSWER] Question 'Q-001' of type 'fill_in_the_blank' must specify a valid non-empty 'correct_answer' with expression or value"]
Test 4 (FIB empty dict): ["[ERR_SCHEMA] Field 'questions.0.correct_answer' (question 'Q-001'): {} is not valid under any of the given schemas", "[ERR_MISSING_ANSWER] Question 'Q-001' of type 'fill_in_the_blank' must specify a valid non-empty 'correct_answer' with expression or value"]
Test 5 (FIB empty list): ["[ERR_SCHEMA] Field 'questions.0.correct_answer' (question 'Q-001'): [] is not valid under any of the given schemas", "[ERR_MISSING_ANSWER] Question 'Q-001' of type 'fill_in_the_blank' must specify a valid non-empty 'correct_answer' with expression or value"]
Test 6 (Valid base course 28 errors): 0
ALL INVALID AND VALID FIB CASES VERIFIED SUCCESSFULLY!
```
