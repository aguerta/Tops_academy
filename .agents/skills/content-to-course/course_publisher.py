"""Course Publisher for Top's Academy Platform.

Validates course banks via the strict validator CLI (`validate-course --strict`),
persists the course JSON to `courses/<course_id>.json`, publishes the CTA markdown,
and outputs platform integration launch instructions.
"""
from __future__ import annotations

import argparse
import json
import logging
import os
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

    def __init__(
        self,
        courses_dir: str | Path = "courses",
        project_root: Optional[str | Path] = None,
    ) -> None:
        self.courses_dir = Path(courses_dir)
        if project_root:
            self.project_root = Path(project_root).resolve()
        else:
            # Hermetic resolution: find project root containing .venv or src
            curr = Path(__file__).resolve().parent
            root = curr
            for parent in [curr] + list(curr.parents):
                if (parent / ".venv").is_dir() or (parent / "src").is_dir():
                    root = parent
                    break
            self.project_root = root

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

        # 1b. If append mode is active and existing file exists, merge content with ID collision remapping
        comp_id_remap: dict[str, str] = {}
        distractor_id_remap: dict[str, str] = {}
        if append and json_path.is_file():
            import re
            try:
                existing_data = json.loads(json_path.read_text(encoding="utf-8"))
                existing_comp_by_id: dict[str, dict[str, Any]] = {}
                max_num_by_prefix: dict[str, int] = {}
                width_by_prefix: dict[str, int] = {}

                for ec in existing_data.get("competencies", []):
                    if not isinstance(ec, dict):
                        continue
                    ec_id = str(ec.get("id") or ec.get("competency_id") or "")
                    if ec_id:
                        existing_comp_by_id[ec_id] = ec
                        m_pre = re.match(r"^([A-Za-z]+-?)(\d+)$", ec_id)
                        if m_pre:
                            pref, num_s = m_pre.group(1), m_pre.group(2)
                            max_num_by_prefix[pref] = max(max_num_by_prefix.get(pref, 0), int(num_s))
                            width_by_prefix[pref] = max(width_by_prefix.get(pref, 2), len(num_s))

                def _remap_dist_id(d_id: str, old_c: str, new_c: str) -> str:
                    m_old = re.match(r"^([A-Za-z]+)-?(\d+)$", old_c)
                    m_new = re.match(r"^([A-Za-z]+)-?(\d+)$", new_c)
                    if not m_old or not m_new:
                        return d_id.replace(old_c, new_c)
                    old_num, new_num = m_old.group(2), m_new.group(2)
                    old_tag = f"{m_old.group(1)}{old_num}"
                    new_tag = f"{m_new.group(1)}{new_num}"
                    if old_tag in d_id:
                        return d_id.replace(old_tag, new_tag, 1)
                    return re.sub(rf"^([Dd]-?){re.escape(old_num)}(-)", rf"\g<1>{new_num}\2", d_id)

                for c in parsed.get("competencies", []):
                    if not isinstance(c, dict):
                        continue
                    orig_cid = str(c.get("id") or c.get("competency_id") or "")
                    if not orig_cid:
                        continue
                    inc_name = str(c.get("name") or c.get("title") or "").strip().lower()

                    if orig_cid not in existing_comp_by_id:
                        new_cid = orig_cid
                        comp_id_remap[orig_cid] = new_cid
                        existing_comp_by_id[new_cid] = c
                        m_pre = re.match(r"^([A-Za-z]+-?)(\d+)$", new_cid)
                        if m_pre:
                            pref, num_s = m_pre.group(1), m_pre.group(2)
                            max_num_by_prefix[pref] = max(max_num_by_prefix.get(pref, 0), int(num_s))
                        existing_data.setdefault("competencies", []).append(c)
                    else:
                        ex_c = existing_comp_by_id[orig_cid]
                        ex_name = str(ex_c.get("name") or ex_c.get("title") or "").strip().lower()
                        if inc_name and ex_name and inc_name == ex_name:
                            # Same competency: append questions into existing competency ID
                            comp_id_remap[orig_cid] = orig_cid
                        else:
                            # Distinct competency with colliding ID: assign next sequential ID for prefix
                            m_pre = re.match(r"^([A-Za-z]+-?)(\d+)$", orig_cid)
                            if m_pre:
                                pref, num_s = m_pre.group(1), m_pre.group(2)
                                width = max(width_by_prefix.get(pref, 2), len(num_s))
                                next_n = max_num_by_prefix.get(pref, int(num_s)) + 1
                                while f"{pref}{next_n:0{width}d}" in existing_comp_by_id:
                                    next_n += 1
                                max_num_by_prefix[pref] = next_n
                                new_cid = f"{pref}{next_n:0{width}d}"
                            else:
                                idx_s = len(existing_comp_by_id) + 1
                                new_cid = f"{orig_cid}_{idx_s:02d}"

                            comp_id_remap[orig_cid] = new_cid
                            c["id"] = new_cid
                            if "competency_id" in c:
                                c["competency_id"] = new_cid
                            for d in c.get("distractors", []):
                                if isinstance(d, dict) and d.get("id"):
                                    old_did = str(d["id"])
                                    new_did = _remap_dist_id(old_did, orig_cid, new_cid)
                                    distractor_id_remap[old_did] = new_did
                                    d["id"] = new_did
                            existing_comp_by_id[new_cid] = c
                            existing_data.setdefault("competencies", []).append(c)

                # Merge optional units/modules if present
                if isinstance(parsed.get("units"), list):
                    ex_units = existing_data.setdefault("units", [])
                    ex_unit_names = {str(u.get("name") or u.get("title") or u).strip().lower() for u in ex_units if isinstance(u, (dict, str))}
                    for u in parsed["units"]:
                        u_key = str(u.get("name") or u.get("title") or u).strip().lower() if isinstance(u, (dict, str)) else ""
                        if u_key and u_key not in ex_unit_names:
                            ex_units.append(u)
                            ex_unit_names.add(u_key)

                existing_q_ids = {
                    q.get("id") or q.get("question_id") for q in existing_data.get("questions", [])
                }
                existing_signatures = {
                    (q.get("stem", "").strip(), str(q.get("correct_answer", "")).strip())
                    for q in existing_data.get("questions", [])
                }

                for q in parsed.get("questions", []):
                    old_q_cid = str(q.get("competency_id") or "")
                    eff_cid = comp_id_remap.get(old_q_cid, old_q_cid)
                    if eff_cid:
                        q["competency_id"] = eff_cid
                    if q.get("subcompetency_id") in comp_id_remap:
                        q["subcompetency_id"] = comp_id_remap[str(q["subcompetency_id"])]

                    if distractor_id_remap:
                        for arch in q.get("distractor_archetypes", []):
                            if isinstance(arch, dict) and arch.get("id") in distractor_id_remap:
                                arch["id"] = distractor_id_remap[str(arch["id"])]
                        for opt in q.get("options", []):
                            if isinstance(opt, dict) and opt.get("distractor_id") in distractor_id_remap:
                                opt["distractor_id"] = distractor_id_remap[str(opt["distractor_id"])]

                    item_sig = (q.get("stem", "").strip(), str(q.get("correct_answer", "")).strip())
                    if item_sig in existing_signatures:
                        continue  # Avoid exact duplicate items

                    orig_id = q.get("id") or q.get("question_id")
                    if orig_id in existing_q_ids or (old_q_cid and eff_cid != old_q_cid):
                        comp_tag = (eff_cid or "Q").replace("-", "")
                        next_idx = len(existing_data.get("questions", [])) + 1
                        new_id = f"Q-{comp_tag}-app-{next_idx:03d}"
                        while new_id in existing_q_ids:
                            next_idx += 1
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
                    "Appended questions into existing course %s. New total: %d questions across %d competencies.",
                    json_path.name,
                    len(parsed.get("questions", [])),
                    len(parsed.get("competencies", [])),
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

        # 4. Write or append CTA markdown if provided
        cta_path_str: Optional[str] = None
        if cta_markdown:
            import re
            cta_path = out_dir / f"competence_analysis_{course_id}.md"
            eff_cta_md = cta_markdown
            full_token_map = {k: v for k, v in {**comp_id_remap, **distractor_id_remap}.items() if k != v}
            if full_token_map:
                pattern = re.compile(
                    r"\b(" + "|".join(re.escape(k) for k in sorted(full_token_map.keys(), key=len, reverse=True)) + r")\b"
                )
                eff_cta_md = pattern.sub(lambda m: full_token_map[m.group(1)], eff_cta_md)

            if append and cta_path.is_file():
                existing_md = cta_path.read_text(encoding="utf-8")
                if eff_cta_md.strip() not in existing_md:
                    merged_md = existing_md.rstrip() + "\n\n---\n\n## Actualización Incremental (Append)\n\n" + eff_cta_md.lstrip() + "\n"
                    cta_path.write_text(merged_md, encoding="utf-8")
            else:
                cta_path.write_text(eff_cta_md, encoding="utf-8")
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

    def _resolve_python_executable(self) -> str:
        """Resolves hermetic Python interpreter path in .venv or falls back to sys.executable."""
        venv_python_win = self.project_root / ".venv" / "Scripts" / "python.exe"
        venv_python_posix = self.project_root / ".venv" / "bin" / "python"

        if sys.platform == "win32" and venv_python_win.is_file():
            return str(venv_python_win.resolve())
        elif venv_python_posix.is_file():
            return str(venv_python_posix.resolve())
        elif venv_python_win.is_file():
            return str(venv_python_win.resolve())
        return sys.executable

    def _run_cli_validator(self, file_path: Path, strict: bool = True) -> bool:
        """Invokes Python validator CLI on published course file with hermetic resolution and fallback."""
        python_bin = self._resolve_python_executable()

        # Inject absolute path of src into PYTHONPATH for hermetic execution
        env = dict(os.environ)
        src_dir = (self.project_root / "src").resolve()
        if src_dir.is_dir():
            existing_pp = env.get("PYTHONPATH", "")
            if existing_pp:
                env["PYTHONPATH"] = f"{src_dir}{os.pathsep}{existing_pp}"
            else:
                env["PYTHONPATH"] = str(src_dir)

        cmd = [python_bin, "-m", "validator.cli", str(file_path)]
        if strict:
            cmd.append("--strict")

        try:
            res = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,
                env=env,
                cwd=str(self.project_root),
            )
            if res.returncode == 0:
                return True

            output_str = (res.stdout or "") + (res.stderr or "")
            # Detect environment / module resolution issues to trigger in-memory fallback
            is_env_error = (
                res.returncode in (9009, 127, 2)
                or any(
                    err_term in output_str
                    for err_term in (
                        "ModuleNotFoundError",
                        "ImportError",
                        "No module named",
                        "not recognized as an internal or external command",
                        "No such file or directory",
                    )
                )
            )

            if is_env_error:
                logger.warning(
                    "CLI validator failed due to environment/module issue (code %d): %s. "
                    "Falling back immediately to in-memory validator.",
                    res.returncode,
                    output_str.strip(),
                )
                v = validate_course_content(file_path.read_text(encoding="utf-8"), strict=strict)
                return v.is_valid

            logger.warning("CLI validator returned %d: %s", res.returncode, output_str.strip())
            return False
        except Exception as ex:
            logger.warning("Failed executing CLI validator (%s). Falling back immediately to in-memory validator.", ex)
            try:
                v = validate_course_content(file_path.read_text(encoding="utf-8"), strict=strict)
                return v.is_valid
            except Exception as in_mem_ex:
                logger.error("In-memory validation fallback failed: %s", in_mem_ex)
                return False


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
