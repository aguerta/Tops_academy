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


@dataclass
class CompetenceSlice:
    """Compact context slice (< 2 KB) for a single competence."""
    competence_id: str
    name: str = ""
    definition: str = ""
    assumptions: list[str] = field(default_factory=list)
    distractor_guidelines: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "competence_id": self.competence_id,
            "name": self.name,
            "definition": self.definition,
            "assumptions": self.assumptions,
            "distractor_guidelines": self.distractor_guidelines,
        }


def slice_competence_context(comp_data: dict[str, Any], max_bytes: int = 2000) -> dict[str, Any]:
    """Extracts a compact competence slice strictly under max_bytes (< 2 KB).
    Selects only core definition, assumptions, and distractor hints without dumping full curriculum data.
    """
    cid = str(comp_data.get("id") or comp_data.get("competence_id") or comp_data.get("cid") or "UNKNOWN")
    name = str(comp_data.get("name") or comp_data.get("title") or "")
    definition = str(
        comp_data.get("definition")
        or comp_data.get("description")
        or comp_data.get("summary")
        or ""
    )
    assumptions = comp_data.get("assumptions") or comp_data.get("assumptions_and_constraints") or []
    if not isinstance(assumptions, list):
        assumptions = [str(assumptions)]
    assumptions = [str(a) for a in assumptions]

    distractors = (
        comp_data.get("distractors")
        or comp_data.get("distractor_archetypes")
        or comp_data.get("distractor_guidelines")
        or comp_data.get("distractor_rules")
        or []
    )
    if not isinstance(distractors, list):
        distractors = [str(distractors)]
    distractors = [str(d) for d in distractors]

    raw_slice = {
        "competence_id": cid,
        "name": name,
        "definition": definition,
        "assumptions": assumptions,
        "distractor_guidelines": distractors,
    }

    # Ensure byte size strictly adheres to limit (< 2 KB)
    serialized = json.dumps(raw_slice, ensure_ascii=False)
    if len(serialized.encode("utf-8")) > max_bytes:
        trimmed_def = definition[:500] + "..." if len(definition) > 500 else definition
        trimmed_assump = assumptions[:4]
        trimmed_dist = distractors[:6]
        raw_slice["definition"] = trimmed_def
        raw_slice["assumptions"] = trimmed_assump
        raw_slice["distractor_guidelines"] = trimmed_dist
        serialized = json.dumps(raw_slice, ensure_ascii=False)
        while len(serialized.encode("utf-8")) > max_bytes and len(raw_slice["definition"]) > 100:
            raw_slice["definition"] = raw_slice["definition"][: len(raw_slice["definition"]) - 100] + "..."
            serialized = json.dumps(raw_slice, ensure_ascii=False)

    return raw_slice


def evaluate_2d_matrix_recommendation(
    error_count: int,
    affected_line_count: int,
    shard_id: str = "shard_1",
    competence_id: str = "CID_01",
) -> dict[str, Any]:
    """Calculates 2D matrix remediation recommendation:
    - If 1 <= error_count < 6 and affected_line_count <= 5:
        strategy: 'edit_file', command: 'edit_file'
    - If error_count >= 6 or affected_line_count > 5:
        strategy: 'ModularSplicing', command: 'ModularSplicing shard_fixes/<shard>/<CID>.py'
    """
    clean_shard = shard_id or "shard_1"
    clean_cid = competence_id or "CID_01"

    if 1 <= error_count < 6 and affected_line_count <= 5:
        strategy = "edit_file"
        action = "edit_file"
        path = ""
    else:
        strategy = "ModularSplicing"
        action = f"ModularSplicing shard_fixes/{clean_shard}/{clean_cid}.py"
        path = f"shard_fixes/{clean_shard}/{clean_cid}.py"

    return {
        "strategy": strategy,
        "recommendation": action,
        "action": action,
        "shard_id": clean_shard,
        "competence_id": clean_cid,
        "error_count": error_count,
        "affected_line_count": affected_line_count,
        "splicing_target": path,
    }


def parse_dual_audit_report(report_data: dict[str, Any]) -> dict[str, Any]:
    """Parses audit reports supporting dual schema conventions:
    - Rule groupings: 'grouped_by_rule' or 'groups'
    - Shards: 'failing_shards' or 'affected_shards'
    - Status: case-insensitive ('REJECTED', 'FAIL', 'FAILED')
    """
    raw_status = str(report_data.get("status", "")).strip().upper()
    is_failing = raw_status in ("REJECTED", "FAIL", "FAILED")

    # Dual schema rule groups
    groups = report_data.get("grouped_by_rule") or report_data.get("groups") or {}

    # Dual schema shards
    shards = report_data.get("failing_shards") or report_data.get("affected_shards") or []
    if not isinstance(shards, list):
        shards = [str(shards)]
    shards = [str(s) for s in shards]

    # Failing competencies
    comps = report_data.get("failing_competencies") or report_data.get("affected_competencies") or []
    if not isinstance(comps, list):
        comps = [str(comps)]
    comps = [str(c) for c in comps]

    return {
        "status": raw_status,
        "is_failing": is_failing,
        "groups": groups,
        "shards": shards,
        "competencies": comps,
    }


def build_remediation_order(
    audit_report: dict[str, Any],
    cta_data: Optional[dict[str, Any]] = None,
    default_shard: str = "shard_1",
    affected_lines_by_comp: Optional[dict[str, int]] = None,
) -> dict[str, Any]:
    """Constructs a structured remediation order from audit reports with:
    - Dual schema parsing ('grouped_by_rule'/'groups', 'failing_shards'/'affected_shards', case-insensitive status)
    - Compact competence slicing (< 2 KB per competence slice)
    - 2D matrix recommendation ('edit_file' vs 'ModularSplicing shard_fixes/<shard>/<CID>.py')
    """
    parsed = parse_dual_audit_report(audit_report)
    shards = parsed["shards"]
    groups = parsed["groups"]
    is_failing = parsed["is_failing"]
    affected_lines_map = affected_lines_by_comp or {}

    # Map competencies from cta_data if supplied
    cta_comp_map: dict[str, dict[str, Any]] = {}
    if isinstance(cta_data, dict):
        raw_comps = cta_data.get("competencies", [])
        if isinstance(raw_comps, list):
            for c in raw_comps:
                if isinstance(c, dict) and "id" in c:
                    cta_comp_map[c["id"]] = c

    # Determine failing competencies from report or groups
    failing_cids = list(parsed["competencies"])
    if not failing_cids and isinstance(groups, dict):
        for rule_key, items in groups.items():
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict) and "competency_id" in item:
                        cid = item["competency_id"]
                        if cid not in failing_cids:
                            failing_cids.append(cid)

    # Count errors per competence
    error_counts_by_comp: dict[str, int] = {}
    if isinstance(groups, dict):
        for rule_key, items in groups.items():
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict):
                        cid = item.get("competency_id") or item.get("cid") or "UNKNOWN"
                        error_counts_by_comp[cid] = error_counts_by_comp.get(cid, 0) + 1

    # Build competence slices and 2D matrix recommendations
    competence_orders: list[dict[str, Any]] = []
    primary_shard = shards[0] if shards else default_shard

    for cid in failing_cids:
        raw_comp = cta_comp_map.get(cid, {"id": cid})
        c_slice = slice_competence_context(raw_comp)

        err_count = error_counts_by_comp.get(cid, len(audit_report.get("errors", [])) or 1)
        line_count = affected_lines_map.get(cid, 1)

        matrix_rec = evaluate_2d_matrix_recommendation(
            error_count=err_count,
            affected_line_count=line_count,
            shard_id=primary_shard,
            competence_id=cid,
        )

        competence_orders.append({
            "competence_id": cid,
            "competence_slice": c_slice,
            "matrix_recommendation": matrix_rec,
            "error_count": err_count,
            "affected_line_count": line_count,
        })

    return {
        "status": parsed["status"],
        "is_remediation_required": is_failing,
        "shards": shards,
        "failing_competencies": failing_cids,
        "competence_orders": competence_orders,
        "rule_groups": groups,
    }


class RepairLoop:
    """Automated validator runner and deterministic LaTeX escape sanitizer."""

    def __init__(self, max_iterations: int = 3, strict: bool = True) -> None:
        self.max_iterations = max_iterations
        self.strict = strict

    def build_remediation_order(
        self,
        audit_report: dict[str, Any],
        cta_data: Optional[dict[str, Any]] = None,
        default_shard: str = "shard_1",
        affected_lines_by_comp: Optional[dict[str, int]] = None,
    ) -> dict[str, Any]:
        """Convenience method delegating to build_remediation_order."""
        return build_remediation_order(
            audit_report=audit_report,
            cta_data=cta_data,
            default_shard=default_shard,
            affected_lines_by_comp=affected_lines_by_comp,
        )

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
