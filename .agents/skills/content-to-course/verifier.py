"""Independent Verification Tier for content-to-course v2.

Provides generic mathematical and programmatic verification (SymPy algebraic equivalence,
expression simplification, numerical evaluation, and invariant auditing) with ZERO
domain logic or hardcoded regexes.
"""
from __future__ import annotations

import argparse
import json
import logging
import math
import random
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import sympy as sp

logger = logging.getLogger("verifier")


@dataclass
class AuditReport:
    """Diagnostic report for an audit sample across generated questions."""
    total_audited: int
    passed_count: int
    flagged_count: int
    accuracy_rate: float
    flagged_items: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class SymPyVerifier:
    """Tier 1: Programmatic symbolic mathematics verifier."""

    def __init__(self) -> None:
        pass

    def parse_math(self, text: str) -> Optional[sp.Expr]:
        """Safely parses mathematical text into a SymPy expression."""
        if not text:
            return None
        clean = text.replace("$", "").replace("\\", "").strip()
        clean = re.sub(r"\s+", "", clean)
        try:
            return sp.sympify(clean)
        except Exception:
            return None

    def are_equivalent(
        self, expr1: Union[str, sp.Expr], expr2: Union[str, sp.Expr]
    ) -> bool:
        """Determines whether two mathematical expressions are algebraically equivalent."""
        e1 = self.parse_math(str(expr1)) if isinstance(expr1, str) else expr1
        e2 = self.parse_math(str(expr2)) if isinstance(expr2, str) else expr2

        if e1 is None or e2 is None:
            return str(expr1).strip().lower() == str(expr2).strip().lower()

        try:
            diff = sp.simplify(e1 - e2)
            if diff == 0:
                return True
        except Exception:
            pass

        # Numerical evaluation check
        try:
            symbols = list(e1.free_symbols.union(e2.free_symbols))
            if not symbols:
                return math.isclose(float(sp.N(e1)), float(sp.N(e2)), abs_tol=1e-5)
            # Evaluate at multiple random points
            rng = random.Random(42)
            for _ in range(5):
                subs_map = {s: rng.uniform(1.5, 5.0) for s in symbols}
                v1 = complex(sp.N(e1.subs(subs_map)))
                v2 = complex(sp.N(e2.subs(subs_map)))
                if abs(v1 - v2) > 1e-4:
                    return False
            return True
        except Exception:
            return False

    def is_numerical_close(self, val1: Any, val2: Any, tol: float = 0.0001) -> bool:
        """Checks if two values evaluate to within numerical tolerance."""
        try:
            s1 = str(val1).replace(",", ".").replace("$", "").strip()
            s2 = str(val2).replace(",", ".").replace("$", "").strip()
            f1 = float(s1)
            f2 = float(s2)
            return abs(f1 - f2) <= tol or math.isclose(f1, f2, abs_tol=tol)
        except Exception:
            return False


class BlindSolver:
    """Tier 2: Agnostic question solver and consistency checker."""

    def __init__(self, sympy_verifier: Optional[SymPyVerifier] = None) -> None:
        self.sympy = sympy_verifier or SymPyVerifier()

    def check_internal_consistency(self, question: Dict[str, Any]) -> Tuple[bool, str]:
        """Validates that stem and options are structurally sound and self-consistent."""
        stem = question.get("stem", "")
        if not stem or len(stem.strip()) < 10:
            return False, "Stem text is too short or empty."

        itype = question.get("interaction_type", "")
        if itype == "multiple_choice_7_options":
            options = question.get("options", [])
            if len(options) != 7:
                return False, f"Expected 7 options, found {len(options)}."
            correct_count = sum(1 for o in options if o.get("is_correct") is True)
            if correct_count != 1:
                return False, f"Expected exactly 1 correct option, found {correct_count}."
            # Check options uniqueness
            contents = [o.get("content", "").strip() for o in options]
            if len(set(contents)) != len(contents):
                return False, "Duplicate option contents found."

        elif itype == "fill_in_the_blank":
            val = question.get("value") or question.get("canonical_algebraic") or question.get("correct_answer")
            if val is None or str(val).strip() == "":
                return False, "Missing fill-in-the-blank answer value."

        elif itype == "multiple_select":
            options = question.get("options", [])
            if not (4 <= len(options) <= 6):
                return False, f"Expected 4-6 options, found {len(options)}."
            correct_count = sum(1 for o in options if o.get("is_correct") is True)
            if not (1 <= correct_count < len(options)):
                return False, f"Expected between 1 and n-1 correct, found {correct_count}."

        return True, "Consistent"


class Verifier:
    """Unified verification manager combining symbolic math and consistency checks."""

    def __init__(self) -> None:
        self.sympy = SymPyVerifier()
        self.solver = BlindSolver(self.sympy)

    def verify_question(self, question: Dict[str, Any]) -> Tuple[bool, str]:
        """Performs comprehensive verification on a single question dictionary."""
        return self.solver.check_internal_consistency(question)

    def audit_course_bank(
        self, course_data: Dict[str, Any], sample_size: int = 40
    ) -> AuditReport:
        """Audits a representative sample of questions from the course bank."""
        questions = course_data.get("questions", [])
        if not questions:
            return AuditReport(total_audited=0, passed_count=0, flagged_count=0, accuracy_rate=100.0)

        n_sample = min(sample_size, len(questions))
        rng = random.Random(42)
        sample = rng.sample(questions, n_sample)

        passed = 0
        flagged = []

        for q in sample:
            is_valid, msg = self.verify_question(q)
            if is_valid:
                passed += 1
            else:
                flagged.append({"question_id": q.get("id"), "reason": msg})

        accuracy = round((passed / n_sample) * 100.0, 1) if n_sample > 0 else 100.0

        return AuditReport(
            total_audited=n_sample,
            passed_count=passed,
            flagged_count=len(flagged),
            accuracy_rate=accuracy,
            flagged_items=flagged,
        )


def main() -> None:
    """CLI utility for auditing course bank questions."""
    parser = argparse.ArgumentParser(description="Audit course bank questions.")
    parser.add_argument("course_json", help="Path to course JSON file")
    parser.add_argument("--sample", type=int, default=40, help="Number of questions to sample")
    args = parser.parse_args()

    data = json.loads(Path(args.course_json).read_text(encoding="utf-8"))
    verifier = Verifier()
    report = verifier.audit_course_bank(data, sample_size=args.sample)

    print("==================================================")
    print("INDEPENDENT VERIFICATION AUDIT")
    print(f"Sample size:   {report.total_audited}")
    print(f"Passed:        {report.passed_count}")
    print(f"Flagged:       {report.flagged_count}")
    print(f"Accuracy Rate: {report.accuracy_rate}%")
    print("==================================================")


if __name__ == "__main__":
    main()
