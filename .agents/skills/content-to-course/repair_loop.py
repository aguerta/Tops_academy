"""Automated Validator Execution and Sanitization Loop.

Orchestrates validation against platform validator rules and applies
Module A: Regex LaTeX escape sanitizer and silent control character restorer.
Purged of all synthetic mutators and padding injections.
"""
from __future__ import annotations

import argparse
import copy
import json
import logging
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Optional

from validator.core import validate_course_content
from validator.models import ValidationError, ValidationResult

logger = logging.getLogger(__name__)


@dataclass
class RepairIterationReport:
    """Diagnostic report for a single repair pass."""
    iteration: int
    error_count_before: int
    error_codes_fixed: list[str]
    applied_repairs: list[str]
    is_valid_after: bool


@dataclass
class RepairResult:
    """Final result of the auto-repair process."""
    success: bool
    iterations_run: int
    repaired_course_data: dict[str, Any]
    repaired_raw_json: str
    remaining_errors: list[ValidationError] = field(default_factory=list)
    iteration_history: list[RepairIterationReport] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "iterations_run": self.iterations_run,
            "remaining_errors": [asdict(e) for e in self.remaining_errors],
            "iteration_history": [asdict(h) for h in self.iteration_history]
        }


class RepairLoop:
    """Automated validator runner and deterministic LaTeX escape sanitizer."""

    def __init__(self, max_iterations: int = 3, strict: bool = True) -> None:
        self.max_iterations = max_iterations
        self.strict = strict

    def run(
        self,
        course_input: str | dict[str, Any],
        source_cta: Optional[Any] = None
    ) -> RepairResult:
        """Alias for repair_course to support alternate invocation patterns."""
        return self.repair_course(course_input, source_cta)

    def repair_course(
        self,
        course_input: str | dict[str, Any],
        source_cta: Optional[Any] = None
    ) -> RepairResult:
        """Executes validator and applies deterministic Module A LaTeX sanitization."""
        # 1. Normalize input to raw_json and parsed dict
        if isinstance(course_input, dict):
            raw_json = json.dumps(course_input, ensure_ascii=False, indent=2)
            course_data = copy.deepcopy(course_input)
        else:
            raw_json = course_input
            try:
                course_data = json.loads(self.sanitize_latex_escapes(raw_json))
            except Exception:
                raw_json = self.sanitize_latex_escapes(raw_json)
                try:
                    course_data = json.loads(raw_json)
                except Exception:
                    course_data = {}

        history: list[RepairIterationReport] = []

        # Initial validation
        v_res = validate_course_content(raw_json, strict=self.strict)
        if v_res.is_valid:
            return RepairResult(
                success=True,
                iterations_run=0,
                repaired_course_data=course_data,
                repaired_raw_json=raw_json,
                remaining_errors=[]
            )

        current_errors = v_res.errors

        for it in range(1, self.max_iterations + 1):
            logger.info("Starting repair iteration %d with %d errors", it, len(current_errors))
            repairs_applied: list[str] = []
            error_codes = [e.code for e in current_errors]

            # -------------------------------------------------------------
            # Module A: Lexical LaTeX & Silent Control Character Sanitizer
            # -------------------------------------------------------------
            sanitized = self.sanitize_latex_escapes(raw_json)
            if sanitized != raw_json:
                raw_json = sanitized
                repairs_applied.append("Module A: Sanitized LaTeX backslashes & restored control characters")
                try:
                    course_data = json.loads(raw_json)
                except Exception as ex:
                    logger.warning("JSON decode after regex sanitizer failed: %s", ex)

            # Re-validate after sanitization
            v_after = validate_course_content(raw_json, strict=self.strict)
            history.append(RepairIterationReport(
                iteration=it,
                error_count_before=len(current_errors),
                error_codes_fixed=list(set(error_codes) - {e.code for e in v_after.errors}),
                applied_repairs=repairs_applied,
                is_valid_after=v_after.is_valid
            ))

            if v_after.is_valid:
                return RepairResult(
                    success=True,
                    iterations_run=it,
                    repaired_course_data=course_data,
                    repaired_raw_json=raw_json,
                    remaining_errors=[],
                    iteration_history=history
                )

            current_errors = v_after.errors

            # If no repairs were applied or could change the output, break early
            if not repairs_applied:
                break

        return RepairResult(
            success=False,
            iterations_run=len(history),
            repaired_course_data=course_data,
            repaired_raw_json=raw_json,
            remaining_errors=current_errors,
            iteration_history=history
        )

    # -------------------------------------------------------------------------
    # Module A: Regex LaTeX Sanitizer & Control Character Recovery
    # -------------------------------------------------------------------------

    @staticmethod
    def sanitize_latex_escapes(raw_text: str) -> str:
        """Sanitizes raw JSON string: fixes unescaped LaTeX backslashes,
        restores corrupted ASCII control characters, and cleans raw newlines.
        """
        s = raw_text

        # 1. Restore silent control character mutations caused by single backslash
        # \t from \text, \tau, \theta, \times, \tr
        s = re.sub(r"\t(ext|au|heta|imes|r)", r"\\t\1", s)
        # \f from \frac
        s = re.sub(r"\f(rac)", r"\\f\1", s)
        # \b from \begin, \beta, \bar
        s = re.sub(r"\x08(egin|eta|ar)", r"\\b\1", s)
        # \r from \right
        s = re.sub(r"\r(ight)", r"\\r\1", s)
        # \n from \nu, \nabla
        s = re.sub(r"(?<!\\)\n(u|abla)\b", r"\\n\1", s)

        # 2. Convert unescaped single backslash before known LaTeX tokens to double backslash
        latex_commands = [
            "alpha", "beta", "gamma", "delta", "epsilon", "varepsilon", "zeta",
            "eta", "theta", "iota", "kappa", "lambda", "mu", "nu", "xi", "pi",
            "rho", "sigma", "tau", "upsilon", "phi", "chi", "psi", "omega",
            "Gamma", "Delta", "Theta", "Lambda", "Xi", "Pi", "Sigma", "Phi", "Psi", "Omega",
            "frac", "sqrt", "text", "partial", "sum", "int", "prod", "infty",
            "pm", "mp", "cdot", "times", "div", "approx", "equiv", "neq", "le", "ge",
            "leq", "geq", "subset", "subseteq", "in", "notin", "forall", "exists",
            "implies", "iff", "to", "rightarrow", "leftarrow", "vec", "hat", "bar",
            "dot", "ddot", "begin", "end", "det", "dim", "ker", "exp", "ln", "log",
            "sin", "cos", "tan", "quad", "qquad", "left", "right", "matrix", "pmatrix",
            "bmatrix", "vmatrix"
        ]

        pattern = r"(?<!\\)\\(" + "|".join(latex_commands) + r")\b"
        s = re.sub(pattern, r"\\\\\1", s)

        # 3. Clean unescaped raw newlines inside JSON string literals
        s = s.replace("\r\n", "\n").replace("\r", "\n")

        return s


def main() -> None:
    """CLI utility for running the repair loop on a course JSON file."""
    parser = argparse.ArgumentParser(description="Auto-repair malformed course JSON files.")
    parser.add_argument("course_json", help="Path to course JSON file")
    parser.add_argument("--output", "-o", help="Optional output path for repaired JSON")
    parser.add_argument("--max-iterations", type=int, default=3, help="Max repair iterations")
    parser.add_argument("--strict", action="store_true", default=True, help="Enforce strict mode")
    args = parser.parse_args()

    course_p = Path(args.course_json)
    raw_text = course_p.read_text(encoding="utf-8")

    repairer = RepairLoop(max_iterations=args.max_iterations, strict=args.strict)
    result = repairer.repair_course(raw_text)

    print(f"Repair Result: {'SUCCESS' if result.success else 'FAILED'}")
    print(f"Iterations run: {result.iterations_run}")
    print(f"Remaining errors: {len(result.remaining_errors)}")

    for h in result.iteration_history:
        print(f"Pass {h.iteration}: errors before={h.error_count_before}, fixed={h.error_codes_fixed}")
        for rep in h.applied_repairs:
            print(f"  - {rep}")

    if args.output and result.success:
        out_p = Path(args.output)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(result.repaired_raw_json, encoding="utf-8")
        print(f"Saved repaired course to {out_p}")


if __name__ == "__main__":
    main()
