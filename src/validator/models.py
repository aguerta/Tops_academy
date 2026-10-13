"""Data models for validator errors and results."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class ValidationError:
    """Represents a single validation error with rule ID, diagnostic code, and context."""
    rule_id: str
    code: str
    message: str
    line: Optional[int] = None
    col: Optional[int] = None
    item_id: Optional[str] = None
    lines: list[int] = field(default_factory=list)
    details: dict[str, Any] = field(default_factory=dict)

    @property
    def diagnostic(self) -> str:
        """Returns the canonical diagnostic string '[CODE] message'."""
        return f"[{self.code}] {self.message}"

    def formatted(self) -> str:
        """Formatted string for CLI output."""
        location = ""
        if self.lines:
            lines_str = ", ".join(str(l) for l in sorted(set(self.lines)))
            location = f" (líneas: {lines_str} - {len(self.lines)} ocurrencias)"
        elif self.line is not None and self.col is not None:
            location = f" (line {self.line}, col {self.col})"
        elif self.line is not None:
            location = f" (line {self.line})"
        return f"Rule {self.rule_id}: [{self.code}] {self.message}{location}"

    def to_dict(self) -> dict[str, Any]:
        """Convert error to JSON-serializable dictionary."""
        return {
            "rule_id": self.rule_id,
            "code": self.code,
            "message": self.message,
            "line": self.line,
            "col": self.col,
            "lines": self.lines,
            "item_id": self.item_id,
            "details": self.details,
            "diagnostic": self.diagnostic,
        }

    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"


@dataclass
class ValidationResult:
    """Represents the outcome of validating a course file or document."""
    file_path: Optional[str]
    is_valid: bool
    errors: list[ValidationError] = field(default_factory=list)
    course_id: Optional[str] = None
    course_title: Optional[str] = None
    total_questions: int = 0
    total_competencies: int = 0

    @property
    def exit_code(self) -> int:
        """Standard exit code: 0 if valid, 1 if invalid."""
        return 0 if self.is_valid else 1

    def to_dict(self) -> dict[str, Any]:
        """Convert result to JSON-serializable dictionary."""
        return {
            "file_path": self.file_path,
            "is_valid": self.is_valid,
            "exit_code": self.exit_code,
            "course_id": self.course_id,
            "course_title": self.course_title,
            "total_questions": self.total_questions,
            "total_competencies": self.total_competencies,
            "errors": [err.to_dict() for err in self.errors],
        }
