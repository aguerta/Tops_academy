"""Command-line interface for the Course Format Validator.

Usage:
    python -m validator.cli <path_to_course_json_or_dir> [--strict] [--json]
    validate-course <path_to_course_json_or_dir> [--strict] [--json]

Exit codes:
    0: Course is valid.
    1: Validation failed (one or more rules violated).
    2: File not found or I/O error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Sequence

from .core import validate_course
from .models import ValidationError, ValidationResult


def consolidate_validation_errors(errors: list[ValidationError]) -> list[ValidationError]:
    """Consolidates identical or repeated errors sharing (rule_id, code, canonical_message) into single errors with lines."""
    if not errors:
        return []

    grouped: dict[tuple[str, str, str], list[ValidationError]] = {}
    for err in errors:
        canonical_msg = re.sub(r"\s+at line \d+(?:, col \d+)?", "", err.message)
        canonical_msg = re.sub(r"\s*\(line \d+(?:, col \d+)?\)", "", canonical_msg)
        canonical_msg = re.sub(r"\s*:\s*$", "", canonical_msg.strip())
        key = (err.rule_id, err.code, canonical_msg)
        grouped.setdefault(key, []).append(err)

    consolidated: list[ValidationError] = []
    for (rule_id, code, canonical_msg), err_list in grouped.items():
        if len(err_list) == 1:
            consolidated.append(err_list[0])
        else:
            collected_lines: list[int] = []
            for e in err_list:
                if e.lines:
                    collected_lines.extend(e.lines)
                elif e.line is not None:
                    collected_lines.append(e.line)
                else:
                    m_l = re.search(r"\bline\s+(\d+)\b", e.message)
                    if m_l:
                        collected_lines.append(int(m_l.group(1)))
            rep_msg = canonical_msg if canonical_msg else err_list[0].message
            consolidated.append(ValidationError(
                rule_id=rule_id,
                code=code,
                message=rep_msg,
                line=collected_lines[0] if collected_lines else None,
                lines=sorted(set(collected_lines)),
                item_id=err_list[0].item_id,
                details={"consolidated_count": len(err_list)},
            ))

    return consolidated


def format_cli_output(result: ValidationResult, strict: bool = False) -> str:
    """Formats human-readable diagnostic messages for CLI output."""
    lines: list[str] = []
    file_name = result.file_path or "course.json"

    if result.is_valid:
        course_name = result.course_id or "course"
        mode_suffix = " (strict mode)" if strict else ""
        lines.append(f"VALID: Course '{course_name}' passed all 16 validation rules{mode_suffix}.")
    else:
        lines.append(f"[VALIDATION FAILURE] {file_name}")
        consolidated = consolidate_validation_errors(result.errors)
        for err in consolidated:
            lines.append(f"  {err.formatted()}")
        err_count = len(result.errors)
        lines.append(f"FAILED: {err_count} {'error' if err_count == 1 else 'errors'} detected.")

    return "\n".join(lines)


def run_validation(target_path: Path, strict: bool = False) -> list[ValidationResult]:
    """Runs validation on a single file or recursively on a directory."""
    results: list[ValidationResult] = []

    if target_path.is_file():
        results.append(validate_course(target_path, strict=strict))
    elif target_path.is_dir():
        json_files = sorted(list(target_path.glob("*.json")))
        if not json_files:
            raise FileNotFoundError(f"No JSON course files found in directory: {target_path}")
        for jf in json_files:
            results.append(validate_course(jf, strict=strict))
    else:
        raise FileNotFoundError(f"Path does not exist: {target_path}")

    return results


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="validate-course",
        description="Top's Academy Course Exercise Bank Validator"
    )
    parser.add_argument(
        "path",
        help="Path to course JSON file or directory containing course JSON files"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Enable strict checking mode"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output diagnostics in JSON format"
    )

    args = parser.parse_args(argv)

    target_path = Path(args.path)

    try:
        results = run_validation(target_path, strict=args.strict)
    except (FileNotFoundError, PermissionError, IsADirectoryError, OSError) as e:
        if args.json_output:
            print(json.dumps({"status": "error", "message": str(e), "exit_code": 2}, indent=2))
        else:
            print(f"[IO ERROR] {e}", file=sys.stderr)
        return 2

    all_valid = all(r.is_valid for r in results)

    if args.json_output:
        payload = {
            "all_valid": all_valid,
            "exit_code": 0 if all_valid else 1,
            "results": [r.to_dict() for r in results]
        }
        print(json.dumps(payload, indent=2))
    else:
        for r in results:
            print(format_cli_output(r, strict=args.strict))

    return 0 if all_valid else 1


if __name__ == "__main__":
    sys.exit(main())
