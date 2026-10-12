#!/usr/bin/env python3
"""delete_course.py

Fast, deterministic course deletion and audit stamping engine for the
Top's Academy platform.

Guarantees:
1. Complete removal of course files from courses/ so the platform (run_platform.py)
   and web UI cannot discover or serve them.
2. Preservation of historical QA audit reports in reports/qa_audits/, updating them
   with 'ELIMINADO' status and the exact deletion timestamp ('Fecha Eliminación' column).
3. Absolute immutability of the content/ (and contents/) directory.
4. Protection of courses/fixtures/ test assets.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# Resolve repository root
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
COURSES_DIR = REPO_ROOT / "courses"
REPORTS_DIR = REPO_ROOT / "reports" / "qa_audits"
ARCHIVE_DIR = REPO_ROOT / "archive_rejected_courses"
WORK_DIR = REPO_ROOT / "work"

IMMUTABLE_ROOT_NAMES: Set[str] = {"content", "contents"}
PROTECTED_RELATIVE_DIRS: Set[str] = {
    "courses/fixtures",
    "platform",
    "src",
    "tests",
    ".agents",
    "system_prompts",
    "scripts",
}


class SecurityError(Exception):
    """Raised when an operation attempts to violate safety or immutability guardrails."""
    pass


def assert_path_safe(target_path: Path) -> Path:
    """Validate that the target path does not violate safety invariants.
    
    Raises:
        SecurityError: If the target path points inside content/, courses/fixtures/,
                       or any protected system directory.
    """
    resolved = target_path.resolve()
    repo_resolved = REPO_ROOT.resolve()

    # 1. Check directory containment inside content/ or contents/
    for imm_name in IMMUTABLE_ROOT_NAMES:
        imm_path = (repo_resolved / imm_name).resolve()
        if resolved == imm_path or imm_path in resolved.parents:
            raise SecurityError(
                f"VIOLACIÓN CRÍTICA DE SEGURIDAD: '{target_path}' está dentro del directorio "
                f"inmutable de fuentes originales ('{imm_name}/'). Operación abortada."
            )

    # 2. Check courses/fixtures protection
    fixtures_path = (repo_resolved / "courses" / "fixtures").resolve()
    if resolved == fixtures_path or fixtures_path in resolved.parents:
        raise SecurityError(
            f"PROTECTED ASSET: '{target_path}' es parte de la suite de pruebas (fixtures). Operación abortada."
        )

    # 3. Check protected system directories
    for prot_rel in PROTECTED_RELATIVE_DIRS:
        prot_path = (repo_resolved / prot_rel).resolve()
        if resolved == prot_path:
            raise SecurityError(
                f"PROTECTED DIRECTORY: '{target_path}' es un directorio protegido del sistema. Operación abortada."
            )

    # 4. Must be inside repository
    try:
        resolved.relative_to(repo_resolved)
    except ValueError:
        raise SecurityError(
            f"PATH ESCAPE: '{target_path}' está fuera del repositorio. Operación abortada."
        )

    return resolved


def get_current_timestamp_str() -> str:
    """Return local formatted timestamp string."""
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def get_current_iso_str() -> str:
    """Return ISO 8601 timestamp string."""
    now = datetime.datetime.now()
    return now.isoformat()


def stamp_individual_audit_json(json_path: Path, timestamp_str: str, dry_run: bool = False) -> bool:
    """Update individual audit JSON with ELIMINADO status and deletion timestamp."""
    if not json_path.is_file():
        return False
    try:
        assert_path_safe(json_path)
        data = json.loads(json_path.read_text(encoding="utf-8"))
        data["platform_status"] = "ELIMINADO"
        data["deleted_at"] = timestamp_str
        if "course_metadata" in data and isinstance(data["course_metadata"], dict):
            data["course_metadata"]["platform_status"] = "ELIMINADO"
            data["course_metadata"]["deleted_at"] = timestamp_str
        data["deletion_note"] = (
            "Curso retirado de la plataforma interactiva Top's Academy; "
            "conservado como registro histórico de auditoría pedagógica."
        )
        if not dry_run:
            json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return True
    except Exception as ex:
        print(f"  [WARN] No se pudo actualizar {json_path.name}: {ex}")
        return False


def stamp_individual_audit_md(md_path: Path, timestamp_str: str, dry_run: bool = False) -> bool:
    """Update individual audit Markdown report with ELIMINADO banner and deletion timestamp."""
    if not md_path.is_file():
        return False
    try:
        assert_path_safe(md_path)
        content = md_path.read_text(encoding="utf-8")
        
        # Check if already stamped
        if "**Estado en Plataforma:** ELIMINADO" in content and timestamp_str in content:
            return True

        # Build stamp note
        stamp_banner = (
            f"> [!WARNING]\n"
            f"> **CURSO RETIRADO DE LA PLATAFORMA**: Este curso fue eliminado de la plataforma interactiva "
            f"el **{timestamp_str}**. Este informe de auditoría se conserva exclusivamente como registro "
            f"histórico y pedagógico ('legacy').\n\n"
        )

        metadata_lines = (
            f"**Estado en Plataforma:** ELIMINADO  \n"
            f"**Fecha de Eliminación:** {timestamp_str}  \n"
        )

        # Replace or insert metadata
        if "**Estado en Plataforma:**" in content:
            content = re.sub(r"\*\*Estado en Plataforma:\*\*.*?\n", metadata_lines, content)
        else:
            # Insert after the title header block (after level 1 heading)
            h1_match = re.search(r"^#\s+.*?\n+", content, re.MULTILINE)
            if h1_match:
                end_pos = h1_match.end()
                content = content[:end_pos] + stamp_banner + metadata_lines + content[end_pos:]
            else:
                content = stamp_banner + metadata_lines + content

        if not dry_run:
            md_path.write_text(content, encoding="utf-8")
        return True
    except Exception as ex:
        print(f"  [WARN] No se pudo actualizar {md_path.name}: {ex}")
        return False


def stamp_suite_audit_table(course_id: str, timestamp_str: str, dry_run: bool = False) -> bool:
    """Ensure SUITE_QA_AUDIT_REPORT.md has 'Fecha Eliminación' column and marks this course."""
    suite_file = REPORTS_DIR / "SUITE_QA_AUDIT_REPORT.md"
    if not suite_file.is_file():
        return False

    try:
        assert_path_safe(suite_file)
        lines = suite_file.read_text(encoding="utf-8").splitlines()
        new_lines: List[str] = []
        in_table = False
        header_has_col = False
        date_col_index = -1

        for line in lines:
            stripped = line.strip()
            # Detect table header
            if stripped.startswith("|") and "Curso" in stripped and "Estado" in stripped:
                in_table = True
                cols = [c.strip() for c in stripped.split("|")[1:-1]]
                if "Fecha Eliminación" in cols:
                    header_has_col = True
                    date_col_index = cols.index("Fecha Eliminación")
                    new_lines.append(line)
                else:
                    # Append new column to header
                    header_has_col = False
                    new_header = stripped[:-1] + " Fecha Eliminación |"
                    date_col_index = len(cols)
                    new_lines.append(new_header)
                continue

            # Detect separator row
            if in_table and stripped.startswith("|") and ":---" in stripped:
                if not header_has_col:
                    new_sep = stripped[:-1] + " :---: |"
                    new_lines.append(new_sep)
                else:
                    new_lines.append(line)
                continue

            # Detect table rows
            if in_table and stripped.startswith("|"):
                if stripped.startswith("| **Promedio") or stripped.startswith("| Promedio") or not stripped.startswith("|"):
                    in_table = False
                    new_lines.append(line)
                    continue

                cells = [c.strip() for c in stripped.split("|")[1:-1]]
                
                # Check if this row corresponds to the deleted course
                is_target_course = (course_id in stripped) or (f"`{course_id}`" in stripped)
                
                if not header_has_col:
                    # We added the column, pad row
                    if is_target_course:
                        # Set Estado to Eliminado and add timestamp
                        if len(cells) >= 12:
                            cells[11] = "Eliminado de la Plataforma"
                        cells.append(timestamp_str)
                    else:
                        cells.append("Nulo")
                else:
                    # Column already existed
                    if is_target_course:
                        if len(cells) > date_col_index:
                            cells[date_col_index] = timestamp_str
                        if len(cells) >= 12:
                            cells[11] = "Eliminado de la Plataforma"

                # Reassemble row
                formatted_row = "| " + " | ".join(cells) + " |"
                new_lines.append(formatted_row)
                continue

            # End of table
            if in_table and not stripped.startswith("|"):
                in_table = False

            new_lines.append(line)

        if not dry_run:
            suite_file.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        return True
    except Exception as ex:
        print(f"  [WARN] No se pudo actualizar SUITE_QA_AUDIT_REPORT.md: {ex}")
        return False


def stamp_all_active_reports_as_nulo(dry_run: bool = False) -> None:
    """Ensure all active audit reports have 'Fecha de Eliminación: Nulo' if not deleted."""
    if not REPORTS_DIR.exists():
        return
    for md_file in REPORTS_DIR.glob("*_qa_report.md"):
        if md_file.name == "SUITE_QA_AUDIT_REPORT.md":
            continue
        try:
            assert_path_safe(md_file)
            content = md_file.read_text(encoding="utf-8")
            if "Fecha de Eliminación:" not in content and "CURSO RETIRADO" not in content:
                # Add status line for active course
                h1_match = re.search(r"^#\s+.*?\n+", content, re.MULTILINE)
                if h1_match:
                    end_pos = h1_match.end()
                    active_stamp = (
                        "**Estado en Plataforma:** Activo (Vigente)  \n"
                        "**Fecha de Eliminación:** Nulo  \n"
                    )
                    content = content[:end_pos] + active_stamp + content[end_pos:]
                    if not dry_run:
                        md_file.write_text(content, encoding="utf-8")
        except Exception:
            pass


def find_course_artifacts(course_id: str) -> Dict[str, List[Path]]:
    """Discover all files and directories linked to a course across the platform."""
    artifacts: Dict[str, List[Path]] = {
        "platform_json": [],
        "platform_cta": [],
        "course_dirs": [],
        "qa_reports": [],
        "work_dirs": [],
    }

    if not COURSES_DIR.exists():
        return artifacts

    # 1. Main JSON file: courses/<course_id>.json
    target_json = COURSES_DIR / f"{course_id}.json"
    if target_json.is_file():
        artifacts["platform_json"].append(target_json)

    # Scan for JSONs whose internal course_id matches
    for jf in COURSES_DIR.glob("*.json"):
        if jf == target_json:
            continue
        try:
            data = json.loads(jf.read_text(encoding="utf-8"))
            if isinstance(data, dict) and data.get("course_id") == course_id:
                artifacts["platform_json"].append(jf)
        except Exception:
            pass

    # 2. CTA analysis markdown: courses/competence_analysis_<course_id>.md
    cta_patterns = [
        COURSES_DIR / f"competence_analysis_{course_id}.md",
        COURSES_DIR / f"competence_analysis_{course_id}_v3.md",
    ]
    for cta_p in cta_patterns:
        if cta_p.is_file():
            artifacts["platform_cta"].append(cta_p)

    # 3. Intermediate course directory: courses/<course_id>/
    for cand in COURSES_DIR.iterdir():
        if cand.is_dir() and cand.name != "fixtures":
            if cand.name == course_id or cand.name.startswith(f"{course_id}_"):
                artifacts["course_dirs"].append(cand)

    # 4. QA Audit reports (to be stamped, not deleted)
    if REPORTS_DIR.exists():
        for r in REPORTS_DIR.glob(f"*{course_id}*"):
            if r.is_file():
                artifacts["qa_reports"].append(r)

    # 5. Active work directory if it references this course
    if WORK_DIR.exists() and WORK_DIR.is_dir():
        order_file = WORK_DIR / "order.json"
        manifest_file = WORK_DIR / "manifest.json"
        is_current_work = False
        for chk in [order_file, manifest_file]:
            if chk.is_file():
                try:
                    txt = chk.read_text(encoding="utf-8")
                    if course_id in txt:
                        is_current_work = True
                        break
                except Exception:
                    pass
        if is_current_work:
            artifacts["work_dirs"].append(WORK_DIR)

    return artifacts


def delete_course(
    course_id: str,
    dry_run: bool = False,
    archive: bool = False,
    clear_work: bool = False
) -> Dict[str, Any]:
    """Execute complete removal of a course from the platform and stamp QA records.
    
    Returns:
        Summary dict containing operation metrics, deleted files, and stamped reports.
    """
    start_time = time.perf_counter()
    timestamp_str = get_current_timestamp_str()

    artifacts = find_course_artifacts(course_id)
    platform_files_to_remove: List[Path] = artifacts["platform_json"] + artifacts["platform_cta"]
    dirs_to_remove: List[Path] = artifacts["course_dirs"]
    qa_reports: List[Path] = artifacts["qa_reports"]

    # Verify safety of every candidate path before executing
    for p in platform_files_to_remove:
        assert_path_safe(p)
    for d in dirs_to_remove:
        assert_path_safe(d)
    for q in qa_reports:
        assert_path_safe(q)

    deleted_files: List[str] = []
    deleted_dirs: List[str] = []
    archived_files: List[str] = []
    stamped_reports: List[str] = []

    if archive:
        target_archive = ARCHIVE_DIR / f"{course_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        if not dry_run:
            target_archive.mkdir(parents=True, exist_ok=True)

        for f in platform_files_to_remove:
            if not dry_run:
                dest = target_archive / f.name
                shutil.move(str(f), str(dest))
            archived_files.append(str(f))

        for d in dirs_to_remove:
            if not dry_run:
                dest = target_archive / d.name
                shutil.move(str(d), str(dest))
            archived_files.append(str(d))
    else:
        # Standard fast deletion (purge from platform)
        for f in platform_files_to_remove:
            if not dry_run:
                f.unlink(missing_ok=True)
            deleted_files.append(str(f))

        for d in dirs_to_remove:
            if not dry_run:
                shutil.rmtree(d, ignore_errors=True)
            deleted_dirs.append(str(d))

    if clear_work and artifacts["work_dirs"]:
        for wd in artifacts["work_dirs"]:
            assert_path_safe(wd)
            if not dry_run:
                # Clear contents of work/ without deleting the directory itself
                for item in wd.iterdir():
                    assert_path_safe(item)
                    if item.is_file():
                        item.unlink(missing_ok=True)
                    elif item.is_dir():
                        shutil.rmtree(item, ignore_errors=True)
            deleted_dirs.append(str(wd))

    # Stamp QA audit reports
    for q_file in qa_reports:
        if q_file.suffix == ".json" and "qa_report" in q_file.name:
            if stamp_individual_audit_json(q_file, timestamp_str, dry_run=dry_run):
                stamped_reports.append(str(q_file))
        elif q_file.suffix == ".md" and "qa_report" in q_file.name:
            if stamp_individual_audit_md(q_file, timestamp_str, dry_run=dry_run):
                stamped_reports.append(str(q_file))

    # Update consolidated suite audit report
    if stamp_suite_audit_table(course_id, timestamp_str, dry_run=dry_run):
        stamped_reports.append(str(REPORTS_DIR / "SUITE_QA_AUDIT_REPORT.md"))

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0

    return {
        "course_id": course_id,
        "success": True,
        "dry_run": dry_run,
        "archive_mode": archive,
        "timestamp": timestamp_str,
        "deleted_files": deleted_files,
        "deleted_dirs": deleted_dirs,
        "archived_items": archived_files,
        "stamped_reports": stamped_reports,
        "elapsed_ms": round(elapsed_ms, 2),
    }


def clean_orphan_course_dirs(dry_run: bool = False) -> List[str]:
    """Clean intermediate directories in courses/ that have no corresponding JSON."""
    if not COURSES_DIR.exists():
        return []

    active_json_stems = {f.stem for f in COURSES_DIR.glob("*.json")}
    cleaned: List[str] = []

    for d in COURSES_DIR.iterdir():
        if not d.is_dir() or d.name == "fixtures":
            continue
        assert_path_safe(d)
        # If directory stem does not match any active course JSON
        if d.name not in active_json_stems:
            if not dry_run:
                shutil.rmtree(d, ignore_errors=True)
            cleaned.append(str(d))

    return cleaned


def list_courses_status() -> None:
    """Print an exhaustive status table of all courses across platform and audits."""
    print("=" * 80)
    print("  ESTADO DE CURSOS EN LA PLATAFORMA Y AUDITORÍAS HISTÓRICAS")
    print("=" * 80)

    # 1. Platform published courses
    platform_courses: Dict[str, Dict[str, Any]] = {}
    if COURSES_DIR.exists():
        for jf in sorted(COURSES_DIR.glob("*.json")):
            try:
                data = json.loads(jf.read_text(encoding="utf-8"))
                cid = data.get("course_id", jf.stem)
                title = data.get("title") or data.get("course_title", jf.stem)
                q_count = len(data.get("questions", []))
                c_count = len(data.get("competencies", []))
                platform_courses[cid] = {
                    "file": jf.name,
                    "title": title,
                    "questions": q_count,
                    "competencies": c_count,
                    "active": True,
                }
            except Exception:
                platform_courses[jf.stem] = {
                    "file": jf.name,
                    "title": jf.stem,
                    "questions": 0,
                    "competencies": 0,
                    "active": False,
                }

    # 2. Audits in reports/qa_audits
    audited_courses: Dict[str, Dict[str, Any]] = {}
    if REPORTS_DIR.exists():
        for rep in REPORTS_DIR.glob("*_qa_report.json"):
            cid = rep.stem.replace("_qa_report", "")
            try:
                data = json.loads(rep.read_text(encoding="utf-8"))
                status = data.get("platform_status") or (
                    "Activo" if cid in platform_courses else "ELIMINADO"
                )
                deleted_at = data.get("deleted_at", "Nulo")
                audited_courses[cid] = {
                    "status": status,
                    "deleted_at": deleted_at,
                    "score": data.get("final_score", "-"),
                    "tier": data.get("quality_tier", "-"),
                }
            except Exception:
                audited_courses[cid] = {
                    "status": "Desconocido",
                    "deleted_at": "Nulo",
                    "score": "-",
                    "tier": "-",
                }

    all_ids = sorted(set(list(platform_courses.keys()) + list(audited_courses.keys())))
    if not all_ids:
        print("  No se detectaron cursos registrados ni en courses/ ni en reports/qa_audits/.")
        print("=" * 80)
        return

    print(f"{'ID del Curso':<32} | {'Estado Plataforma':<16} | {'Fecha Eliminación':<20} | {'Auditoría'}")
    print("-" * 80)
    for cid in all_ids:
        is_in_platform = cid in platform_courses
        audit_info = audited_courses.get(cid, {})
        del_date = audit_info.get("deleted_at", "Nulo") if not is_in_platform else "Nulo"
        if not is_in_platform and del_date == "Nulo":
            del_date = audit_info.get("deleted_at", "Nulo")

        plat_status = "ACTIVO" if is_in_platform else "ELIMINADO (Legacy)"
        audit_tag = f"Tier: {audit_info.get('tier', 'N/A')} ({audit_info.get('score', '-')}/20)" if audit_info else "Sin Auditoría"
        print(f"{cid:<32} | {plat_status:<16} | {del_date:<20} | {audit_tag}")

    print("=" * 80)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fast course deletion and QA audit stamping engine for Top's Academy platform"
    )
    parser.add_argument("--course-id", "-c", type=str, help="ID of the course to delete/purge")
    parser.add_argument("--all", "-a", action="store_true", help="Purge all active courses from platform")
    parser.add_argument("--list", "-l", action="store_true", help="List all courses with platform status and deletion dates")
    parser.add_argument("--clean-orphans", action="store_true", help="Clean orphan subdirectories in courses/")
    parser.add_argument("--dry-run", action="store_true", help="Simulate deletion without modifying disk")
    parser.add_argument("--archive", action="store_true", help="Move course to archive_rejected_courses/ instead of permanent deletion")
    parser.add_argument("--clear-work", action="store_true", help="Also clear active working directory work/ if related")
    parser.add_argument("--yes", "-y", action="store_true", help="Bypass interactive confirmation prompt")
    parser.add_argument("--init-nulo", action="store_true", help="Initialize 'Fecha de Eliminación: Nulo' on all active reports")

    args = parser.parse_args()

    if args.init_nulo:
        stamp_all_active_reports_as_nulo(dry_run=args.dry_run)
        print("[OK] Reportes de auditoría inicializados con 'Fecha de Eliminación: Nulo'.")
        return

    if args.list:
        list_courses_status()
        return

    if args.clean_orphans:
        print("[*] Buscando directorios huérfanos en courses/...")
        cleaned = clean_orphan_course_dirs(dry_run=args.dry_run)
        prefix = "[DRY-RUN] " if args.dry_run else ""
        if cleaned:
            print(f"{prefix}Directorios eliminados ({len(cleaned)}):")
            for c in cleaned:
                print(f"  - {c}")
        else:
            print("No se encontraron directorios huérfanos.")
        return

    if not args.course_id and not args.all:
        parser.print_help()
        sys.exit(1)

    target_ids: List[str] = []
    if args.all:
        if COURSES_DIR.exists():
            for f in COURSES_DIR.glob("*.json"):
                try:
                    data = json.loads(f.read_text(encoding="utf-8"))
                    cid = data.get("course_id", f.stem)
                    target_ids.append(cid)
                except Exception:
                    target_ids.append(f.stem)
    elif args.course_id:
        target_ids.append(args.course_id)

    if not target_ids:
        print("[!] No se encontraron cursos para eliminar.")
        return

    mode_label = "ARCHIVADO" if args.archive else "PURGA PERMANENTE"
    dry_label = " [MODO SIMULACIÓN --dry-run]" if args.dry_run else ""
    print(f"\n=======================================================")
    print(f"  OPERACIÓN: {mode_label}{dry_label}")
    print(f"  Cursos objetivo ({len(target_ids)}): {', '.join(target_ids)}")
    print(f"=======================================================")

    if not args.yes and not args.dry_run:
        prompt_msg = f"¿Está seguro de eliminar {len(target_ids)} curso(s) de la plataforma? [s/N]: "
        try:
            confirm = input(prompt_msg).strip().lower()
            if confirm not in ("s", "si", "y", "yes"):
                print("Operación cancelada por el usuario.")
                sys.exit(0)
        except EOFError:
            print("Operación cancelada (entrada no interactiva sin --yes).")
            sys.exit(1)

    for cid in target_ids:
        res = delete_course(
            course_id=cid,
            dry_run=args.dry_run,
            archive=args.archive,
            clear_work=args.clear_work,
        )
        tag = "[DRY-RUN]" if args.dry_run else "[OK]"
        print(f"\n{tag} Curso: '{cid}' procesado en {res['elapsed_ms']} ms")
        if res["deleted_files"]:
            print(f"  Archivos eliminados de la plataforma ({len(res['deleted_files'])}):")
            for df in res["deleted_files"]:
                print(f"    - {Path(df).name}")
        if res["deleted_dirs"]:
            print(f"  Directorios eliminados ({len(res['deleted_dirs'])}):")
            for dd in res["deleted_dirs"]:
                print(f"    - {Path(dd).name}")
        if res["archived_items"]:
            print(f"  Ítems archivados ({len(res['archived_items'])}):")
            for ai in res["archived_items"]:
                print(f"    - {Path(ai).name}")
        if res["stamped_reports"]:
            print(f"  Reportes de auditoría preservados y sellados ({len(res['stamped_reports'])}):")
            for sr in res["stamped_reports"]:
                print(f"    - {Path(sr).name} (Fecha: {res['timestamp']})")

    print("\nOperación completada exitosamente.")


if __name__ == "__main__":
    main()
