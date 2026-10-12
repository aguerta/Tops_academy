"""Core validation orchestrator combining lexical, schema, and semantic passes."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Union

from .models import ValidationError, ValidationResult
from .lexical_scanner import scan_lexical
from .schema_validator import validate_schema
from .rules import check_semantic_rules, check_strict_rules, check_extended_quality_rules
from .psychometric_checker import check_psychometrics


def validate_course_content(
    raw_text: str,
    file_path: str | None = None,
    strict: bool = False
) -> ValidationResult:
    """Validates raw course JSON text across all passes (Pass 1 and Pass 2, plus strict mode)."""
    # Pass 1: Raw text lexical scanning
    lex_errors = scan_lexical(raw_text)

    # Attempt JSON parsing
    parsed_data: dict[str, Any] | None = None
    try:
        parsed_data = json.loads(raw_text)
    except json.JSONDecodeError as e:
        # If lexical scanner didn't already capture R-01/R-02/R-03 errors, or to complement it:
        json_err = ValidationError(
            rule_id="R-01",
            code="ERR_INVALID_JSON",
            message=f"File is not valid JSON at line {e.lineno}, col {e.colno}: {e.msg}",
            line=e.lineno,
            col=e.colno
        )
        # Avoid duplicate error if already reported
        if not any(err.code == "ERR_INVALID_JSON" and err.line == e.lineno for err in lex_errors):
            lex_errors.append(json_err)

    if lex_errors or parsed_data is None:
        return ValidationResult(
            file_path=file_path,
            is_valid=False,
            errors=lex_errors
        )

    if not isinstance(parsed_data, dict):
        return ValidationResult(
            file_path=file_path,
            is_valid=False,
            errors=[ValidationError(
                rule_id="R-04",
                code="ERR_SCHEMA",
                message="Root course element must be a JSON object"
            )]
        )

    # Pass 2: Schema, Structural, Pedagogical, Psychometric, and Quality validation
    schema_errors = validate_schema(parsed_data)
    semantic_errors = check_semantic_rules(parsed_data)
    psychometric_errors = check_psychometrics(parsed_data)
    quality_errors = check_extended_quality_rules(parsed_data)

    all_errors = schema_errors + semantic_errors + psychometric_errors + quality_errors

    # Strict mode validation (Pass 3)
    if strict:
        strict_errors = check_strict_rules(parsed_data)
        all_errors.extend(strict_errors)

    course_id = parsed_data.get("course_id")
    course_title = parsed_data.get("course_title")
    questions = parsed_data.get("questions", [])
    competencies = parsed_data.get("competencies", [])

    return ValidationResult(
        file_path=file_path,
        is_valid=(len(all_errors) == 0),
        errors=all_errors,
        course_id=course_id if isinstance(course_id, str) else None,
        course_title=course_title if isinstance(course_title, str) else None,
        total_questions=len(questions) if isinstance(questions, list) else 0,
        total_competencies=len(competencies) if isinstance(competencies, list) else 0
    )


def validate_course(
    path_or_text: Union[str, Path],
    is_raw_text: bool = False,
    strict: bool = False
) -> ValidationResult:
    """Validates a course by file path or directly from raw text string.

    Raises FileNotFoundError or OSError if a file path cannot be accessed.
    """
    if is_raw_text:
        return validate_course_content(str(path_or_text), file_path=None, strict=strict)

    file_path = Path(path_or_text)
    if not file_path.exists():
        raise FileNotFoundError(f"Course file not found: {file_path}")
    if not file_path.is_file():
        raise IsADirectoryError(f"Specified path is not a file: {file_path}")

    raw_text = file_path.read_text(encoding="utf-8")
    return validate_course_content(raw_text, file_path=str(file_path), strict=strict)
