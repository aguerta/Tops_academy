"""Stage 0 Prepare: Lossless Multiformat Source Ingestion & Delta Generation Engine.

Features:
- Encapsulates Stage 0 preparation, multiformat partitioning, and manifest generation.
- Incremental Append Mode (--append): reads existing courses/<id>.json, extracts existing
  competency IDs and names, and calculates continuous next_ids per category/prefix
  to guarantee non-overlapping, continuous sequences (e.g. Solow model 21 -> 45).
- Windows PowerShell Resilience: sanitizes quoting anomalies and gracefully falls back
  to clean titles when CLI --title contains corrupted replacement characters (\\ufffd).
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Union

# Ensure skill directory and project root are importable
skill_dir = Path(__file__).resolve().parent
if str(skill_dir) not in sys.path:
    sys.path.insert(0, str(skill_dir))

from ingest import ingest_course

logger = logging.getLogger("c2c.prepare")
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def sanitize_cli_arg(arg: Any) -> Any:
    """Sanitize CLI argument by stripping outer and escaped quotes from Windows shells."""
    if not isinstance(arg, str):
        return arg
    cleaned = arg.strip()
    for _ in range(3):
        if (cleaned.startswith('"') and cleaned.endswith('"')) or (
            cleaned.startswith("'") and cleaned.endswith("'")
        ):
            if len(cleaned) <= 1:
                break
            cleaned = cleaned[1:-1].strip()
        if cleaned.startswith(r'\"') and cleaned.endswith(r'\"'):
            cleaned = cleaned[2:-2].strip()

    # Remove escaped quotes embedded at boundaries
    cleaned = cleaned.replace(r'\"', '"')
    if (cleaned.startswith('"') and cleaned.endswith('"')) or (
        cleaned.startswith("'") and cleaned.endswith("'")
    ):
        cleaned = cleaned[1:-1].strip()

    # Normalize trailing backslash if it wasn't a Windows drive root
    if len(cleaned) > 3 and cleaned.endswith("\\"):
        cleaned = cleaned.rstrip("\\")
    return cleaned


def sanitize_path(path_val: Union[str, Path, None]) -> Optional[Path]:
    """Clean and resolve path argument removing literal quotes or backslash-quote anomalies."""
    if path_val is None:
        return None
    cleaned_str = sanitize_cli_arg(str(path_val))
    return Path(cleaned_str)


def is_corrupted_unicode(text: Optional[str]) -> bool:
    """Detect if string contains corrupted Unicode replacement character (\ufffd)."""
    if not text:
        return False
    return "\ufffd" in text or "\uFFFD" in text


def compute_next_ids(competencies: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculates continuous, non-overlapping next_ids per category and prefix.
    
    Extracts numerical suffixes from existing IDs (e.g. C-01..C-10 -> next C-11,
    Hab-01..Hab-06 -> next Hab-07, H-01..H-05 -> next H-06) preserving padding width.
    """
    max_num_by_prefix: Dict[str, int] = {}
    width_by_prefix: Dict[str, int] = {}

    for comp in competencies:
        if not isinstance(comp, dict):
            continue
        cid = str(comp.get("id") or comp.get("competency_id") or "")
        if not cid:
            continue
        m = re.match(r"^([A-Za-z]+[-_]?)(\d+)$", cid)
        if m:
            prefix, num_str = m.group(1), m.group(2)
            num_val = int(num_str)
            max_num_by_prefix[prefix] = max(max_num_by_prefix.get(prefix, 0), num_val)
            width_by_prefix[prefix] = max(width_by_prefix.get(prefix, 2), len(num_str))

    # Ensure baseline standard prefixes exist
    standard_prefixes = ["C-", "Hab-", "H-"]
    for pref in standard_prefixes:
        if pref not in max_num_by_prefix:
            # Check without hyphen if present
            alt_pref = pref.rstrip("-")
            if alt_pref in max_num_by_prefix:
                max_num_by_prefix[pref] = max_num_by_prefix[alt_pref]
                width_by_prefix[pref] = width_by_prefix[alt_pref]
            else:
                max_num_by_prefix[pref] = 0
                width_by_prefix[pref] = 2

    next_ids_by_prefix: Dict[str, str] = {}
    next_numbers_by_prefix: Dict[str, int] = {}
    for pref, max_num in max_num_by_prefix.items():
        nxt = max_num + 1
        width = width_by_prefix.get(pref, 2)
        next_numbers_by_prefix[pref] = nxt
        next_ids_by_prefix[pref] = f"{pref}{nxt:0{width}d}"

    # Map categories to expected prefixes
    category_to_prefix = {
        "Concept": "C-",
        "Skill": "Hab-",
        "Fact": "H-",
    }
    next_ids_by_category: Dict[str, str] = {}
    for cat, pref in category_to_prefix.items():
        next_ids_by_category[cat] = next_ids_by_prefix.get(pref, f"{pref}01")

    return {
        "max_numbers_by_prefix": max_num_by_prefix,
        "width_by_prefix": width_by_prefix,
        "next_numbers_by_prefix": next_numbers_by_prefix,
        "next_ids_by_prefix": next_ids_by_prefix,
        "next_ids_by_category": next_ids_by_category,
        "next_competency_index": len(competencies) + 1,
    }


def prepare_course(
    input_path: Union[str, Path, Sequence[Union[str, Path]]],
    work_dir: Union[str, Path],
    course_id: Optional[str] = None,
    courses_dir: Union[str, Path] = "courses",
    append: bool = False,
    cta_mode: str = "direct",
    granularity: str = "standard",
    dpi: int = 150,
    order_override: Optional[Sequence[str]] = None,
    title: Optional[str] = None,
    render_pages: bool = False,
) -> Dict[str, Any]:
    """Executes Stage 0 preparation: partitioning, manifest generation, and append delta injection."""
    clean_work_dir = Path(sanitize_cli_arg(str(work_dir)))
    clean_courses_dir = Path(sanitize_cli_arg(str(courses_dir)))
    clean_course_id = sanitize_cli_arg(course_id) if course_id else None
    clean_title = sanitize_cli_arg(title) if title else None

    clean_work_dir.mkdir(parents=True, exist_ok=True)

    # 1. Stale artifact purge for append mode isolated in work_append/
    if append and clean_work_dir.name == "work_append" and clean_work_dir.is_dir():
        for stale_item in (
            "cta.json", "cta.md", "cta_data.py", "course.json", "course_verified.json",
            "judge_report.json", "templates", "shards", "verification", "cta_parts", "cta",
            "delta_manifest.json"
        ):
            stale_p = clean_work_dir / stale_item
            if stale_p.is_dir():
                shutil.rmtree(stale_p, ignore_errors=True)
            elif stale_p.is_file():
                stale_p.unlink(missing_ok=True)

    # 2. Normalize input sources
    raw_items = input_path if isinstance(input_path, (list, tuple)) else [input_path]
    sources: List[Path] = []
    for item in raw_items:
        clean_item = sanitize_path(item)
        if clean_item:
            if not clean_item.exists():
                raise FileNotFoundError(f"Input source path does not exist: {clean_item.resolve()}")
            sources.append(clean_item)

    if not sources:
        raise FileNotFoundError("Cannot execute prepare: No valid input source paths provided.")

    # 3. Execute core ingestion & partitioning with explicit input_files and zero-raster default
    manifest_payload = ingest_course(
        input_path=sources[0],
        output_dir=clean_work_dir,
        course_id=clean_course_id,
        cta_mode=cta_mode,
        dpi=dpi,
        order_override=order_override,
        render_pages=render_pages,
        input_files=sources,
    )

    # Pre-seed compile_cta.py compiler in canonical work directory if present
    compile_src = skill_dir / "compile_cta.py"
    if compile_src.is_file():
        shutil.copy2(compile_src, clean_work_dir / "compile_cta.py")

    # 4. Handle Incremental Append Mode (--append) with Delta Generation
    if append and clean_course_id:
        existing_course_path = clean_courses_dir / f"{clean_course_id}.json"
        if not existing_course_path.is_file():
            # Check default "courses" dir fallback
            alt_path = Path("courses") / f"{clean_course_id}.json"
            if alt_path.is_file():
                existing_course_path = alt_path

        if existing_course_path.is_file():
            try:
                existing_data = json.loads(existing_course_path.read_text(encoding="utf-8"))
                existing_comps = existing_data.get("competencies", [])
                existing_questions = existing_data.get("questions", [])

                # Handle title fallback if CLI title is mangled with \ufffd
                base_title = existing_data.get("course_title") or existing_data.get("title", "")
                if clean_title and is_corrupted_unicode(clean_title):
                    logger.warning(
                        "CLI --title contains corrupted Unicode ('\\ufffd'): %r. "
                        "Falling back to existing course title: %r.",
                        clean_title, base_title
                    )
                    clean_title = base_title
                elif not clean_title and base_title:
                    clean_title = base_title

                # Calculate non-overlapping next continuous IDs
                next_ids_info = compute_next_ids(existing_comps)

                delta_info = {
                    "append_mode": True,
                    "course_id": clean_course_id,
                    "base_course_file": str(existing_course_path.resolve()),
                    "base_course_title": base_title,
                    "total_existing_competencies": len(existing_comps),
                    "total_existing_questions": len(existing_questions),
                    "existing_competency_ids": [
                        str(c.get("id") or c.get("competency_id")) for c in existing_comps
                    ],
                    "existing_competency_names": [
                        str(c.get("name") or c.get("title") or "").strip() for c in existing_comps
                    ],
                    "existing_competencies_summary": [
                        {
                            "id": c.get("id") or c.get("competency_id"),
                            "name": c.get("name") or c.get("title"),
                            "category": c.get("category", "Concept"),
                        }
                        for c in existing_comps
                    ],
                    "existing_competencies_outline": [
                        {
                            "id": c.get("id") or c.get("competency_id"),
                            "type": c.get("type") or c.get("category", "concept").lower(),
                            "name": c.get("name") or c.get("title"),
                        }
                        for c in existing_comps
                    ],
                    "max_numbers_by_prefix": next_ids_info["max_numbers_by_prefix"],
                    "next_ids_by_prefix": next_ids_info["next_ids_by_prefix"],
                    "next_ids_by_category": next_ids_info["next_ids_by_category"],
                    "next_competency_index": next_ids_info["next_competency_index"],
                    "instructions": (
                        f"APPEND DELTA MODE: Existing course '{clean_course_id}' has {len(existing_comps)} competencies "
                        f"and {len(existing_questions)} questions in base course bank. "
                        f"The CTA architect and authors must produce ONLY new delta competencies "
                        f"starting with IDs: {next_ids_info['next_ids_by_prefix']}. Do NOT duplicate existing competency names or restart from 01."
                    ),
                }

                # Inject delta information into central manifest
                manifest_payload["append_mode"] = True
                manifest_payload["delta"] = delta_info
                manifest_payload["existing_course"] = delta_info

                manifest_file = clean_work_dir / "pre_cta_manifest.json"
                manifest_file.write_text(
                    json.dumps(manifest_payload, indent=2, ensure_ascii=False),
                    encoding="utf-8",
                )

                # Persist dedicated delta manifest for downstream consumers
                delta_manifest_file = clean_work_dir / "delta_manifest.json"
                delta_manifest_file.write_text(
                    json.dumps(delta_info, indent=2, ensure_ascii=False),
                    encoding="utf-8",
                )

                logger.info(
                    "[+] Append delta mode configured: %d existing competencies found in %s.",
                    len(existing_comps),
                    existing_course_path.name,
                )
                logger.info("    Next IDs sequence starts at: %s", next_ids_info["next_ids_by_prefix"])
            except Exception as ex:
                logger.warning("Could not parse existing course JSON for delta append (%s): %s", existing_course_path, ex)
        else:
            logger.info("Append flag specified but existing course '%s.json' not found. Starting initial sequence.", clean_course_id)

    # 5. Persist title and granularity metadata in manifest
    if clean_title:
        manifest_payload["course_title"] = clean_title
    manifest_payload["granularity"] = granularity
    manifest_file = clean_work_dir / "pre_cta_manifest.json"
    manifest_file.write_text(
        json.dumps(manifest_payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return manifest_payload


def main() -> None:
    """CLI utility for Stage 0 Prepare."""
    parser = argparse.ArgumentParser(
        description="Stage 0 Prepare: Lossless Multiformat Source Ingestion & Delta Generation Engine."
    )
    parser.add_argument("--input", "--pdf", dest="input", required=True, nargs="+", help="Input PDF(s) or directory")
    parser.add_argument("--work-dir", "--output-dir", "--work", dest="work_dir", required=True, help="Work directory")
    parser.add_argument("--course-id", help="Course slug identifier")
    parser.add_argument("--courses-dir", default="courses", help="Courses destination folder (defaults to courses/)")
    parser.add_argument("--title", help="Human-readable title for the course")
    parser.add_argument("--append", action="store_true", default=False, help="Enable incremental append delta generation")
    parser.add_argument("--cta-mode", choices=["direct", "mapreduce", "auto"], default="auto", help="CTA execution mode")
    parser.add_argument("--granularity", choices=["fine", "standard", "coarse"], default="standard", help="Competency granularity")
    parser.add_argument("--dpi", type=int, default=150, help="DPI for page rendering")
    parser.add_argument("--order", nargs="*", help="Optional document processing order")
    parser.add_argument("--render-pages", dest="render_pages", action="store_true", default=False, help="Render PDF pages to PNG (default False)")
    parser.add_argument("--no-render-pages", dest="render_pages", action="store_false", help="Do not render PDF pages to PNG")

    # Sanitize sys.argv arguments
    sanitized_argv = [sys.argv[0]] + [sanitize_cli_arg(a) for a in sys.argv[1:]]
    args = parser.parse_args(sanitized_argv[1:])

    pdf_arg = args.input[0] if (args.input and len(args.input) == 1) else args.input

    try:
        manifest = prepare_course(
            input_path=pdf_arg,
            work_dir=args.work_dir,
            course_id=args.course_id,
            courses_dir=args.courses_dir,
            append=args.append,
            cta_mode=args.cta_mode,
            granularity=args.granularity,
            dpi=args.dpi,
            order_override=args.order,
            title=args.title,
            render_pages=args.render_pages,
        )
        print(f"[+] Prepare complete: {manifest.get('total_files', 0)} files, {manifest.get('total_pages', 0)} pages processed.")
        print(f"[+] Manifest written to: {Path(args.work_dir) / 'pre_cta_manifest.json'}")
        if manifest.get("append_mode"):
            print(f"[+] Append delta active. Next IDs: {manifest.get('delta', {}).get('next_ids_by_prefix')}")
    except Exception as ex:
        print(f"[FATAL ERROR in prepare.py]: {ex}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
