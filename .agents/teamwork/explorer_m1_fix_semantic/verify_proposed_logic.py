"""Verification script for Explorer 2 proposed semantic and schema remediation."""
import copy
import json
import re
import sys
from pathlib import Path
from typing import Any
import jsonschema
from jsonschema import Draft7Validator

from src.validator.models import ValidationError, ValidationResult
from src.validator.schema_validator import COURSE_SCHEMA

PROPOSED_COURSE_SCHEMA = copy.deepcopy(COURSE_SCHEMA)

PROPOSED_COURSE_SCHEMA["definitions"]["Question"]["properties"]["correct_answer"] = {
    "oneOf": [
        {
            "type": "string",
            "minLength": 1
        },
        {
            "type": "number"
        },
        {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "string",
                "minLength": 1
            }
        },
        {
            "type": "object",
            "minProperties": 1,
            "anyOf": [
                {"required": ["value"]},
                {"required": ["expression"]}
            ],
            "properties": {
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
                },
                "expression": {
                    "type": "string",
                    "minLength": 1
                },
                "tolerance": {
                    "type": "number"
                },
                "canonical_algebraic": {
                    "type": "string",
                    "minLength": 1
                },
                "accepted_equivalents": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "minLength": 1
                    }
                }
            }
        }
    ]
}

PROPOSED_COURSE_SCHEMA["definitions"]["Question"]["allOf"] = [
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
]


def proposed_validate_schema(data: dict[str, Any]) -> list[ValidationError]:
    errors: list[ValidationError] = []
    validator = Draft7Validator(PROPOSED_COURSE_SCHEMA)

    for err in sorted(validator.iter_errors(data), key=lambda e: str(e.path)):
        path = list(err.path)
        item_id = None
        item_context = ""

        if len(path) >= 2 and path[0] == "questions" and isinstance(path[1], int):
            questions = data.get("questions")
            if isinstance(questions, list) and 0 <= path[1] < len(questions):
                q = questions[path[1]]
                if isinstance(q, dict) and "id" in q:
                    item_id = q["id"]
                    item_context = f" (question '{item_id}')"
        elif len(path) >= 2 and path[0] == "competencies" and isinstance(path[1], int):
            competencies = data.get("competencies")
            if isinstance(competencies, list) and 0 <= path[1] < len(competencies):
                comp = competencies[path[1]]
                if isinstance(comp, dict) and "id" in comp:
                    item_id = comp["id"]
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

    return errors


def proposed_check_semantic_rules(data: dict[str, Any]) -> list[ValidationError]:
    from src.validator.rules import check_semantic_rules
    errors = check_semantic_rules(data)

    questions = data.get("questions")
    if not isinstance(questions, list):
        return errors

    for q in questions:
        if not isinstance(q, dict):
            continue
        q_id = q.get("id", "UNKNOWN")
        itype = q.get("interaction_type")
        options = q.get("options")

        if itype == "multiple_select":
            if not isinstance(options, list):
                errors.append(ValidationError(
                    rule_id="R-12",
                    code="ERR_MS_COUNT",
                    message=f"Question '{q_id}' has 0 options; multiple-select items must have between 4 and 6 options",
                    item_id=q_id
                ))

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

    return errors


if __name__ == "__main__":
    base_course = json.loads(Path("courses/fixtures/28_valid_complete_course.json").read_text(encoding="utf-8"))

    # Comprehensive matrix test
    # 1. Invalid cases that MUST fail
    invalid_answers = [
        None,
        {},
        [],
        "",
        "   ",
        {"expression": ""},
        {"value": ""},
        {"tolerance": 0.001},
        {"random_key": "abc"},
    ]
    for idx, inv in enumerate(invalid_answers):
        c = copy.deepcopy(base_course)
        c["questions"][0]["interaction_type"] = "fill_in_the_blank"
        del c["questions"][0]["options"]
        if inv is None:
            c["questions"][0].pop("correct_answer", None)
        else:
            c["questions"][0]["correct_answer"] = inv

        errs = proposed_validate_schema(c) + proposed_check_semantic_rules(c)
        assert len(errs) > 0, f"Failed to reject invalid FIB correct_answer case {idx}: {inv}"
        assert any(e.code in ("ERR_SCHEMA", "ERR_MISSING_ANSWER") for e in errs)
        assert any("Q-001" in str(e) for e in errs)

    # 2. Valid cases that MUST pass
    valid_answers = [
        "42",
        "x^2 + 1",
        42,
        3.14159,
        ["42", "42.0", "forty-two"],
        {"value": "x_i", "canonical_algebraic": "x_i", "accepted_equivalents": ["x_i"]},
        {"value": 42, "tolerance": 0.01},
        {"value": ["a", "b"]},
        {"expression": "sin(x)*exp(-t)", "tolerance": 0.001},
        {"value": "x", "expression": "x"},
    ]
    for idx, v in enumerate(valid_answers):
        c = copy.deepcopy(base_course)
        c["questions"][0]["interaction_type"] = "fill_in_the_blank"
        del c["questions"][0]["options"]
        c["questions"][0]["correct_answer"] = v

        errs = proposed_validate_schema(c) + proposed_check_semantic_rules(c)
        assert len(errs) == 0, f"False positive: rejected valid FIB correct_answer case {idx}: {v}. Errors: {[str(e) for e in errs]}"

    print("ALL INVALID AND VALID FIB CASES VERIFIED SUCCESSFULLY!")
