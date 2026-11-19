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
        "modules": {
            "type": "array"
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
                    "pattern": "^(PRE|Hab|C|H|Aut|COMP)-[0-9A-Za-z_-]+$"
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
                },
                "session": {
                    "type": "string"
                },
                "unit_index": {
                    "type": "integer"
                },
                "is_prerequisite": {
                    "type": "boolean"
                },
                "evidence": {
                    "type": "array"
                },
                "assumptions": {
                    "type": "array"
                },
                "source_examples": {
                    "type": "array"
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
                },
                {
                    "if": {
                        "properties": {
                            "interaction_type": {"const": "open_symbolic"}
                        }
                    },
                    "then": {
                        "required": ["correct_answer"]
                    }
                },
                {
                    "if": {
                        "properties": {
                            "interaction_type": {"const": "proof_dag"}
                        }
                    },
                    "then": {
                        "required": ["proof_dag"]
                    }
                },
                {
                    "if": {
                        "properties": {
                            "interaction_type": {"const": "adversarial_break"}
                        }
                    },
                    "then": {
                        "required": ["adversarial_break"]
                    }
                },
                {
                    "if": {
                        "properties": {
                            "interaction_type": {"const": "unstructured_model"}
                        }
                    },
                    "then": {
                        "required": ["unstructured_model"]
                    }
                },
                {
                    "if": {
                        "properties": {
                            "interaction_type": {"const": "invariant_canvas"}
                        }
                    },
                    "then": {
                        "required": ["invariant_canvas"]
                    }
                },
                {
                    "if": {
                        "properties": {
                            "interaction_type": {"const": "concept_matching"}
                        }
                    },
                    "then": {
                        "required": ["concept_matching"]
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
                        "fill_in_the_blank",
                        "open_symbolic",
                        "proof_dag",
                        "adversarial_break",
                        "unstructured_model",
                        "invariant_canvas",
                        "concept_matching"
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
                "diagnostic_distractors": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "distractor_id": { "type": "string" },
                            "expression": { "type": "string" },
                            "value": { "type": ["string", "number"] },
                            "accepted_equivalents": {
                                "type": "array",
                                "items": { "type": "string" }
                            },
                            "tolerance": { "type": "number" },
                            "error_rationale": { "type": "string" }
                        }
                    }
                },
                "symbolic_config": {
                    "type": "object"
                },
                "proof_dag": {
                    "type": "object"
                },
                "adversarial_break": {
                    "type": "object"
                },
                "unstructured_model": {
                    "type": "object"
                },
                "invariant_canvas": {
                    "type": "object"
                },
                "concept_matching": {
                    "type": "object"
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
                            "minProperties": 1
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
