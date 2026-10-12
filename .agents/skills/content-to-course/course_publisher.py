"""Course Publisher for Top's Academy Platform.

Validates course banks via the strict validator CLI (`validate-course --strict`),
persists the course JSON to `courses/<course_id>.json`, publishes the CTA markdown,
and outputs platform integration launch instructions.
"""
from __future__ import annotations

import argparse
import json
import logging
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Optional

from validator.core import validate_course_content
from validator.models import ValidationResult

logger = logging.getLogger(__name__)


@dataclass
class PublicationResult:
    """Outcome of publishing a course to the platform."""
    success: bool
    course_id: str
    course_title: str
    published_json_path: str
    published_cta_path: Optional[str]
    total_competencies: int
    total_questions: int
    competency_breakdown: dict[str, int]
    interaction_type_breakdown: dict[str, int]
    validation_passed: bool
    launch_command: str
    launch_url: str
    error_message: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class CoursePublisher:
    """Manages validation, disk persistence, and platform registration."""

    def __init__(self, courses_dir: str | Path = "courses") -> None:
        self.courses_dir = Path(courses_dir)

    def publish(
        self,
        course_data: dict[str, Any] | str,
        output_dir: Optional[str | Path] = None,
        strict: bool = True,
        cta_markdown: Optional[str] = None,
        append: bool = False
    ) -> PublicationResult:
        """Validates strictly, writes course files to disk, and prints launch instructions.
        
        If append=True and the target course JSON already exists, merges new competencies
        and questions with existing data while preserving unique question IDs.
        """
        out_dir = Path(output_dir) if output_dir else self.courses_dir
        out_dir.mkdir(parents=True, exist_ok=True)

        # 1. Parse incoming course data
        if isinstance(course_data, str):
            parsed = json.loads(course_data)
        else:
            parsed = json.loads(json.dumps(course_data))

        course_id = parsed.get("course_id", "course_demo")
        course_title = parsed.get("course_title", "Curso Top's Academy")
        json_path = out_dir / f"{course_id}.json"

        # 1b. If append mode is active and existing file exists, merge content
        if append and json_path.is_file():
            try:
                existing_data = json.loads(json_path.read_text(encoding="utf-8"))
                existing_comp_ids = {
                    c.get("id") or c.get("competency_id") for c in existing_data.get("competencies", [])
                }
                for c in parsed.get("competencies", []):
                    c_id = c.get("id") or c.get("competency_id")
                    if c_id not in existing_comp_ids:
                        existing_data.setdefault("competencies", []).append(c)
                        existing_comp_ids.add(c_id)

                existing_q_ids = {
                    q.get("id") or q.get("question_id") for q in existing_data.get("questions", [])
                }
                existing_signatures = {
                    (q.get("stem", "").strip(), str(q.get("correct_answer", "")).strip())
                    for q in existing_data.get("questions", [])
                }

                for q in parsed.get("questions", []):
                    item_sig = (q.get("stem", "").strip(), str(q.get("correct_answer", "")).strip())
                    if item_sig in existing_signatures:
                        continue  # Avoid exact duplicate items

                    orig_id = q.get("id") or q.get("question_id")
                    if orig_id in existing_q_ids:
                        comp_tag = q.get("competency_id", "Q").replace("-", "")
                        next_idx = len(existing_data.get("questions", [])) + 1
                        new_id = f"Q-{comp_tag}-app-{next_idx:03d}"
                        q["id"] = new_id
                        if "question_id" in q:
                            q["question_id"] = new_id
                        existing_q_ids.add(new_id)
                    else:
                        existing_q_ids.add(orig_id)

                    existing_signatures.add(item_sig)
                    existing_data.setdefault("questions", []).append(q)

                parsed = existing_data
                course_title = parsed.get("course_title", course_title)
                logger.info(
                    "Appended questions into existing course %s. New total: %d questions.",
                    json_path.name,
                    len(parsed.get("questions", []))
                )
            except Exception as ex:
                logger.warning("Failed to load existing course JSON for append: %s", ex)

        raw_text = json.dumps(parsed, ensure_ascii=False, indent=2)

        # 2. Programmatic validation
        v_res = validate_course_content(raw_text, strict=strict)
        if not v_res.is_valid:
            # Attempt auto-repair (e.g. for length rebalancing after merges)
            try:
                from repair_loop import RepairLoop
                repairer = RepairLoop(max_iterations=2, strict=strict)
                rep_res = repairer.repair_course(parsed)
                if rep_res.success:
                    parsed = rep_res.repaired_course_data
                    raw_text = json.dumps(parsed, ensure_ascii=False, indent=2)
                    v_res = validate_course_content(raw_text, strict=strict)
            except Exception as rx:
                logger.debug("Auto-repair during publish failed: %s", rx)

        if not v_res.is_valid:
            err_summary = "; ".join(f"[{e.rule_id}] {e.message}" for e in v_res.errors[:3])
            return PublicationResult(
                success=False,
                course_id=course_id,
                course_title=course_title,
                published_json_path="",
                published_cta_path=None,
                total_competencies=len(parsed.get("competencies", [])),
                total_questions=len(parsed.get("questions", [])),
                competency_breakdown={},
                interaction_type_breakdown={},
                validation_passed=False,
                launch_command="",
                launch_url="",
                error_message=f"Course failed validation before publishing: {err_summary}"
            )

        # 3. Write course JSON to disk
        json_path.write_text(raw_text, encoding="utf-8")
        logger.info("Published course JSON to %s", json_path.resolve())

        # 4. Write CTA markdown if provided
        cta_path_str: Optional[str] = None
        if cta_markdown:
            cta_path = out_dir / f"competence_analysis_{course_id}.md"
            cta_path.write_text(cta_markdown, encoding="utf-8")
            cta_path_str = str(cta_path.resolve())
            logger.info("Published CTA analysis to %s", cta_path_str)

        # 5. Execute external CLI validator to confirm strict compliance on disk
        cli_success = self._run_cli_validator(json_path, strict=strict)
        if not cli_success:
            return PublicationResult(
                success=False,
                course_id=course_id,
                course_title=course_title,
                published_json_path=str(json_path.resolve()),
                published_cta_path=cta_path_str,
                total_competencies=len(parsed.get("competencies", [])),
                total_questions=len(parsed.get("questions", [])),
                competency_breakdown={},
                interaction_type_breakdown={},
                validation_passed=False,
                launch_command="",
                launch_url="",
                error_message="External CLI validator check failed."
            )

        # 6. Compute metric breakdowns
        comp_breakdown: dict[str, int] = {}
        for c in parsed.get("competencies", []):
            cat = c.get("category", "Other")
            comp_breakdown[cat] = comp_breakdown.get(cat, 0) + 1

        itype_breakdown: dict[str, int] = {}
        for q in parsed.get("questions", []):
            it = q.get("interaction_type", "Other")
            itype_breakdown[it] = itype_breakdown.get(it, 0) + 1

        launch_cmd = "python run_platform.py"
        launch_url = f"http://localhost:3000/#/course/{course_id}"

        return PublicationResult(
            success=True,
            course_id=course_id,
            course_title=course_title,
            published_json_path=str(json_path.resolve()),
            published_cta_path=cta_path_str,
            total_competencies=len(parsed.get("competencies", [])),
            total_questions=len(parsed.get("questions", [])),
            competency_breakdown=comp_breakdown,
            interaction_type_breakdown=itype_breakdown,
            validation_passed=True,
            launch_command=launch_cmd,
            launch_url=launch_url
        )

    def _run_cli_validator(self, file_path: Path, strict: bool = True) -> bool:
        """Invokes Python validator CLI on published course file."""
        cmd = [sys.executable, "-m", "validator.cli", str(file_path)]
        if strict:
            cmd.append("--strict")

        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if res.returncode == 0:
                return True
            logger.warning("CLI validator returned %d: %s", res.returncode, res.stdout + res.stderr)
            return False
        except Exception as ex:
            logger.warning("Failed executing CLI validator: %s", ex)
            # Fall back to programmatic verification
            v = validate_course_content(file_path.read_text(encoding="utf-8"), strict=strict)
            return v.is_valid


def main() -> None:
    """CLI utility for publishing course banks."""
    parser = argparse.ArgumentParser(description="Publish validated course bank to courses/ folder.")
    parser.add_argument("course_json", help="Path to input course JSON file")
    parser.add_argument("--output-dir", "-o", default="courses", help="Courses destination directory")
    parser.add_argument("--strict", action="store_true", default=True, help="Enforce strict mode")
    parser.add_argument("--append", action="store_true", default=False, help="Append questions to existing course JSON")
    args = parser.parse_args()

    input_p = Path(args.course_json)
    data = json.loads(input_p.read_text(encoding="utf-8"))

    publisher = CoursePublisher(courses_dir=args.output_dir)
    result = publisher.publish(data, strict=args.strict, append=args.append)

    if result.success:
        print("=================================================================")
        print(f"COURSE PUBLISHED SUCCESSFULLY: {result.course_title} ({result.course_id})")
        print("=================================================================")
        print(f"File Path: {result.published_json_path}")
        print(f"Competencies ({result.total_competencies}): {result.competency_breakdown}")
        print(f"Questions ({result.total_questions}): {result.interaction_type_breakdown}")
        print(f"Validation: 100% Passed (strict mode)")
        print("\nTo start practicing immediately:")
        print(f"  Command: {result.launch_command}")
        print(f"  URL:     {result.launch_url}")
        print("=================================================================")
    else:
        print(f"PUBLICATION FAILED: {result.error_message}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
