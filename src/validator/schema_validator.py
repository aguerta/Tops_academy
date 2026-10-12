"""JSON Schema validator for course exercise banks (Draft-07)."""
from __future__ import annotations

import re
from typing import Any
import jsonschema
from jsonschema import Draft7Validator

from .models import ValidationError

COURSE_SCHEMA: dict[str, Any] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://tops-academy.local/schemas/course-v1.json",
    "title": "TopsAcademyCourse",
    "description": "Standardized, versioned JSON format for Top's Academy courses, competencies, and practice banks.",
    "type": "object",
    "required": [
        "schema_version",
        "course_id",
        "course_title",
        "description",
        "language",
        "created_at",
        "competencies",
        "questions"
    ],
    "properties": {
        "schema_version": {
            "type": "string",
            "pattern": "^1\\.[0-9]+\\.[0-9]+$"
        },
        "course_id": {
            "type": "string",
            "pattern": "^[a-z0-9_-]+$"
        },
        "course_title": {
            "type": "string",
            "minLength": 3
        },
        "description": {
            "type": "string",
            "minLength": 10
        },
        "language": {
            "type": "string",
            "pattern": "^[a-z]{2}(-[A-Z]{2})?$"
        },
        "created_at": {
            "type": "string"
        },
        "competencies": {
            "type": "array",
            "minItems": 1,
            "items": {
                "$ref": "#/definitions/Competency"
            }
        },
        "questions": {
            "type": "array",
            "minItems": 1,
            "items": {
                "$ref": "#/definitions/Question"
            }
        }
    },
    "definitions": {
        "Competency": {
            "type": "object",
            "required": ["id", "name", "category", "description"],
            "properties": {
                "id": {
                    "type": "string",
                    "pattern": "^(Hab|C|H|Aut|COMP)-[0-9A-Za-z_-]+$"
                },
                "code": {
                    "type": "string"
                },
                "name": {
                    "type": "string",
                    "minLength": 3
                },
                "category": {
                    "type": "string",
                    "enum": ["Skill", "Concept", "Fact", "Automation_Seed"]
                },
                "description": {
                    "type": "string",
                    "minLength": 5
                },
                "mastery_target": {
                    "type": "number"
                }
            }
        },
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
                "id": {
                    "type": "string",
                    "pattern": "^Q-[A-Za-z0-9_-]+$"
                },
                "competency_id": {
                    "type": "string"
                },
                "competency_ref": {
                    "type": "object",
                    "properties": {
                        "id": { "type": "string" },
                        "name": { "type": "string" },
                        "category": { "type": "string" }
                    }
                },
                "bloom_taxonomy_level": {
                    "type": "string",
                    "enum": ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]
                },
                "difficulty": {
                    "type": "string",
                    "enum": ["easy", "medium", "hard"]
                },
                "interaction_type": {
                    "type": "string",
                    "enum": [
                        "multiple_choice_7_options",
                        "multiple_select",
                        "fill_in_the_blank"
                    ]
                },
                "context_application": {
                    "type": "string"
                },
                "stem": {
                    "type": "string",
                    "minLength": 5
                },
                "graph": {
                    "$ref": "#/definitions/Graph"
                },
                "interface_config": {
                    "type": "object"
                },
                "options": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/Option"
                    }
                },
                "correct_answer": {
                    "oneOf": [
                        { "type": "string", "minLength": 1 },
                        { "type": "number" },
                        {
                            "type": "array",
                            "minItems": 1,
                            "items": { "type": "string", "minLength": 1 }
                        },
                        {
                            "type": "object",
                            "minProperties": 1,
                            "anyOf": [
                                { "required": ["value"] },
                                { "required": ["expression"] }
                            ],
                            "properties": {
                                "value": {
                                    "oneOf": [
                                        { "type": "string", "minLength": 1 },
                                        { "type": "number" },
                                        {
                                            "type": "array",
                                            "minItems": 1,
                                            "items": { "type": "string", "minLength": 1 }
                                        }
                                    ]
                                },
                                "expression": { "type": "string", "minLength": 1 },
                                "tolerance": { "type": "number" },
                                "canonical_algebraic": { "type": "string", "minLength": 1 },
                                "accepted_equivalents": {
                                    "type": "array",
                                    "items": { "type": "string", "minLength": 1 }
                                }
                            }
                        }
                    ]
                },
                "hints": {
                    "type": "array"
                },
                "detailed_solution": {
                    "type": "string"
                },
                "solution": {
                    "type": "string"
                },
                "common_misconception_warning": {
                    "type": "string"
                },
                "misconception_warning": {
                    "type": "string"
                }
            }
        },
        "Option": {
            "type": "object",
            "required": ["content", "is_correct"],
            "properties": {
                "id": {
                    "type": "string"
                },
                "option_id": {
                    "type": "string"
                },
                "content": {
                    "type": "string"
                },
                "is_correct": {
                    "type": "boolean"
                },
                "error_rationale": {
                    "type": ["string", "null"]
                }
            }
        },
        "Graph": {
            "type": "object",
            "properties": {
                "title": { "type": "string" },
                "x_range": {
                    "type": "array",
                    "items": { "type": "number" }
                },
                "y_range": {
                    "type": "array",
                    "items": { "type": "number" }
                },
                "x_axis": { "type": "object" },
                "y_axis": { "type": "object" },
                "curves": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": { "type": "string" },
                            "fn": { "type": "string" },
                            "label": { "type": "string" },
                            "color": { "type": "string" },
                            "style": { "type": "string" }
                        }
                    }
                },
                "points": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "x": { "type": "number" },
                            "y": { "type": "number" },
                            "style": { "type": "string", "enum": ["closed", "open"] },
                            "type": { "type": "string", "enum": ["closed", "open"] },
                            "label": { "type": "string" },
                            "color": { "type": "string" }
                        }
                    }
                },
                "annotations": { "type": "array" }
            }
        }
    }
}


def validate_schema(data: dict[str, Any]) -> list[ValidationError]:
    """Validates course dict against JSON Schema Draft-07 (Rule R-04)."""
    errors: list[ValidationError] = []
    validator = Draft7Validator(COURSE_SCHEMA)

    for err in sorted(validator.iter_errors(data), key=lambda e: str(e.path)):
        path = list(err.path)
        item_id: str | None = None
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

    return errors
