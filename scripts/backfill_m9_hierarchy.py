"""Deterministic M9 hierarchy backfill script (zero-LLM, < 2 s).

Reads ``courses/*.json``, parses matching ``courses/competence_analysis_<course_id>.md``
(and optionally ``work/<course_id>*/cta.json``), and injects ``session``, ``evidence``,
and ``assumptions`` into each matching competency. Validates every modified course
with ``validate_course_content(..., strict=True)`` before overwriting.
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.validator.core import validate_course_content  # noqa: E402

_SECTION_RE = re.compile(r"^###\s+\[([^\]]+)\]", re.MULTILINE)
_SESSION_RE = re.compile(r"^-\s+\*\*Session:\*\*\s*(.+)$", re.MULTILINE)
_EVIDENCE_LINE_RE = re.compile(r"^-\s+\*\*Evidence Citations:\*\*\s*(.+)$", re.MULTILINE)
_EVIDENCE_ITEM_RE = re.compile(
    r"`([^`]+)`\s*(?:\((?:page|pág\.?|slide)\s*([^)]+)\))?",
    re.IGNORECASE,
)
_ASSUMPTIONS_HEADING_RE = re.compile(
    r"^####\s+Formal Mathematical Assumptions\b", re.MULTILINE
)


def _parse_page_value(raw_page: str | None) -> int | str | None:
    if raw_page is None:
        return None
    cleaned = raw_page.strip()
    if not cleaned:
        return None
    if cleaned.isdigit():
        return int(cleaned)
    return cleaned


def _parse_evidence_citations(line_value: str) -> list[dict[str, Any]]:
    evidence: list[dict[str, Any]] = []
    for match in _EVIDENCE_ITEM_RE.finditer(line_value):
        doc_name = match.group(1).strip()
        page_val = _parse_page_value(match.group(2))
        if not doc_name:
            continue
        item: dict[str, Any] = {"doc": doc_name}
        if page_val is not None:
            item["page"] = page_val
        evidence.append(item)
    return evidence


def _split_markdown_row(row: str) -> list[str]:
    """Split a Markdown table row into stripped cell values, preserving escaped pipes."""
    stripped = row.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    cells = re.split(r"(?<!\\)\|", stripped)
    return [cell.replace("\\|", "|").strip() for cell in cells]


def _parse_assumptions_table(section_text: str) -> list[dict[str, str]]:
    heading_match = _ASSUMPTIONS_HEADING_RE.search(section_text)
    if not heading_match:
        return []

    assumptions: list[dict[str, str]] = []
    lines = section_text[heading_match.end() :].splitlines()
    in_table = False
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            if in_table:
                break
            continue
        if line.startswith("#") or line.startswith("---"):
            break
        if not line.startswith("|"):
            if in_table:
                break
            continue

        in_table = True
        cells = _split_markdown_row(line)
        if len(cells) < 4:
            continue
        # Skip header and alignment separator rows
        first_cell = cells[0].strip("`").strip()
        if not first_cell or first_cell.lower() == "assumption id" or set(first_cell) <= {"-", ":"}:
            continue

        assumption: dict[str, str] = {"id": first_cell}
        name_val = cells[1].strip() if len(cells) > 1 else ""
        stmt_val = cells[2].strip() if len(cells) > 2 else ""
        viol_val = cells[3].strip() if len(cells) > 3 else ""
        role_val = cells[4].strip() if len(cells) > 4 else ""

        if name_val and name_val != "-":
            assumption["name"] = name_val
        if stmt_val and stmt_val != "-":
            assumption["statement_latex"] = stmt_val
        if viol_val and viol_val != "-":
            assumption["violation_consequence"] = viol_val
        if role_val and role_val != "-":
            assumption["role_in_proof"] = role_val

        assumptions.append(assumption)

    return assumptions


def parse_competence_analysis_md(md_text: str) -> dict[str, dict[str, Any]]:
    """Parse ``competence_analysis_<course_id>.md`` into a map keyed by competency ID."""
    matches = list(_SECTION_RE.finditer(md_text))
    parsed: dict[str, dict[str, Any]] = {}

    for idx, match in enumerate(matches):
        comp_id = match.group(1).strip()
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(md_text)
        section_text = md_text[start:end]

        entry: dict[str, Any] = {}
        sess_match = _SESSION_RE.search(section_text)
        if sess_match:
            session_val = sess_match.group(1).strip()
            if session_val and session_val != "-":
                entry["session"] = session_val

        evid_match = _EVIDENCE_LINE_RE.search(section_text)
        if evid_match:
            evidence_list = _parse_evidence_citations(evid_match.group(1))
            if evidence_list:
                entry["evidence"] = evidence_list

        assumptions_list = _parse_assumptions_table(section_text)
        if assumptions_list:
            entry["assumptions"] = assumptions_list

        if entry:
            parsed[comp_id] = entry

    return parsed


def _load_cta_fallback(course_id: str, work_dir: Path | None) -> dict[str, dict[str, Any]]:
    """Optionally load competency metadata from ``work/<course_id>*/cta.json``."""
    if work_dir is None or not work_dir.is_dir():
        return {}
    fallback: dict[str, dict[str, Any]] = {}
    for candidate_dir in sorted(work_dir.glob(f"{course_id}*")):
        cta_path = candidate_dir / "cta.json"
        if not cta_path.is_file():
            continue
        try:
            cta_data = json.loads(cta_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for comp in cta_data.get("competencies", []):
            if not isinstance(comp, dict) or not comp.get("id"):
                continue
            cid = str(comp["id"])
            meta: dict[str, Any] = {}
            for key in ("session", "evidence", "assumptions"):
                val = comp.get(key)
                if val:
                    meta[key] = val
            if meta:
                fallback[cid] = meta
        break
    return fallback


def backfill_courses(
    courses_dir: Path,
    work_dir: Path | None = None,
    write: bool = True,
) -> dict[str, Any]:
    """Hydrate ``courses/*.json`` with M9 hierarchy fields and validate strictly."""
    t0 = time.perf_counter()
    summary: dict[str, Any] = {
        "courses_scanned": 0,
        "courses_updated": 0,
        "courses_skipped_no_source": 0,
        "courses_skipped_invalid": 0,
        "competencies_hydrated": 0,
        "invalid_courses": [],
        "elapsed_ms": 0.0,
    }

    for json_path in sorted(courses_dir.glob("*.json")):
        try:
            raw_original = json_path.read_text(encoding="utf-8")
            course_data = json.loads(raw_original)
        except (OSError, json.JSONDecodeError):
            continue

        if not isinstance(course_data, dict) or not isinstance(course_data.get("competencies"), list):
            continue
        course_id = course_data.get("course_id") or json_path.stem
        if not isinstance(course_id, str) or not course_id:
            continue

        summary["courses_scanned"] += 1

        md_path = courses_dir / f"competence_analysis_{course_id}.md"
        if not md_path.is_file() and json_path.stem != course_id:
            md_path = courses_dir / f"competence_analysis_{json_path.stem}.md"

        md_meta: dict[str, dict[str, Any]] = {}
        if md_path.is_file():
            md_meta = parse_competence_analysis_md(md_path.read_text(encoding="utf-8"))

        cta_meta = _load_cta_fallback(course_id, work_dir)
        if not md_meta and not cta_meta:
            summary["courses_skipped_no_source"] += 1
            continue

        # Build case-insensitive lookup fallback
        md_lower = {k.lower(): v for k, v in md_meta.items()}
        cta_lower = {k.lower(): v for k, v in cta_meta.items()}

        course_changed = False
        hydrated_in_course = 0

        for comp in course_data["competencies"]:
            if not isinstance(comp, dict):
                continue
            cid = str(comp.get("id", ""))
            if not cid:
                continue

            source_meta = (
                md_meta.get(cid)
                or md_lower.get(cid.lower())
                or cta_meta.get(cid)
                or cta_lower.get(cid.lower())
            )
            if not source_meta:
                continue

            comp_updated = False
            for field in ("session", "evidence", "assumptions"):
                val = source_meta.get(field)
                if val and comp.get(field) != val:
                    comp[field] = val
                    comp_updated = True

            if comp_updated:
                course_changed = True
                hydrated_in_course += 1

        if not course_changed:
            continue

        new_raw = json.dumps(course_data, ensure_ascii=False, indent=2) + "\n"
        val_result = validate_course_content(new_raw, file_path=str(json_path), strict=True)
        if not val_result.is_valid:
            summary["courses_skipped_invalid"] += 1
            summary["invalid_courses"].append(
                {
                    "file": json_path.name,
                    "errors": len(val_result.errors),
                    "first_error": val_result.errors[0].message if val_result.errors else "",
                }
            )
            continue

        if write:
            json_path.write_text(new_raw, encoding="utf-8")

        summary["courses_updated"] += 1
        summary["competencies_hydrated"] += hydrated_in_course

    summary["elapsed_ms"] = round((time.perf_counter() - t0) * 1000.0, 2)
    return summary


def main() -> int:
    courses_dir = REPO_ROOT / "courses"
    work_dir = REPO_ROOT / "work"
    result = backfill_courses(courses_dir=courses_dir, work_dir=work_dir, write=True)
    elapsed_s = result["elapsed_ms"] / 1000.0
    print(
        f"[backfill_m9_hierarchy] scanned={result['courses_scanned']} "
        f"updated={result['courses_updated']} "
        f"competencies_hydrated={result['competencies_hydrated']} "
        f"skipped_no_source={result['courses_skipped_no_source']} "
        f"skipped_invalid={result['courses_skipped_invalid']} "
        f"elapsed={result['elapsed_ms']:.2f}ms ({elapsed_s:.3f}s)"
    )
    for inv in result["invalid_courses"]:
        print(
            f"  [WARN] skipped invalid course {inv['file']} "
            f"({inv['errors']} errors): {inv['first_error'][:120]}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
