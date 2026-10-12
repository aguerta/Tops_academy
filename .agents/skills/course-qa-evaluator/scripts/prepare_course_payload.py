#!/usr/bin/env python3
"""prepare_course_payload.py

Helper script for the course-qa-evaluator skill.
Discovers published courses and prepares enriched audit payloads powered by
the StandardizedAuditEngine (Google Antigravity SDK Hybrid Multi-Agent pattern).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
COURSES_DIR = ROOT_DIR / "courses"
REPORTS_DIR = ROOT_DIR / "reports" / "qa_audits"

# Add current scripts directory to path for local imports
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

try:
    from standardized_audit_engine import run_full_audit
except ImportError:
    run_full_audit = None


def get_available_courses() -> list[dict]:
    """Scan and return published courses with validation metadata."""
    if str(ROOT_DIR) not in sys.path:
        sys.path.insert(0, str(ROOT_DIR))

    try:
        import run_platform
        return run_platform.scan_courses()
    except Exception:
        # Fallback direct scan
        results = []
        for f in sorted(COURSES_DIR.glob("*.json")):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                results.append({
                    "id": data.get("course_id", f.stem),
                    "filename": f.name,
                    "title": data.get("title") or data.get("course_title", f.stem),
                    "status": "valid",
                    "total_competencies": len(data.get("competencies", [])),
                    "total_questions": len(data.get("questions", [])),
                    "data": data,
                })
            except Exception as err:
                results.append({
                    "id": f.stem,
                    "filename": f.name,
                    "title": f.stem,
                    "status": "error",
                    "error_message": str(err),
                })
        return results


def summarize_course(course_entry: dict) -> dict:
    """Build an enriched, standardized audit package for a course."""
    data = course_entry.get("data", {})
    competencies = data.get("competencies", [])
    questions = data.get("questions", [])

    # 1. Run deterministic static audit engine (< 300 ms)
    telemetry = {}
    if run_full_audit:
        telemetry = run_full_audit(data)

    comp_map = {c.get("id"): c for c in competencies}
    q_by_comp: dict[str, list[dict]] = {c.get("id"): [] for c in competencies}
    q_by_id = {q.get("id"): q for q in questions}

    types_count: dict[str, int] = {}
    for q in questions:
        cid = q.get("competency_id", "unassigned")
        if cid not in q_by_comp:
            q_by_comp[cid] = []
        q_by_comp[cid].append(q)

        qtype = q.get("interaction_type") or q.get("type", "unknown")
        types_count[qtype] = types_count.get(qtype, 0) + 1

    # 2. Select stratified normal sample (up to 2 items per competency)
    stratified_samples = []
    for cid, qlist in q_by_comp.items():
        comp_info = comp_map.get(cid, {})
        for q in qlist[:2]:
            stratified_samples.append({
                "id": q.get("id"),
                "competency_id": cid,
                "competency_name": comp_info.get("name", ""),
                "type": q.get("interaction_type") or q.get("type"),
                "difficulty": q.get("difficulty"),
                "stem": q.get("stem"),
                "options": q.get("options"),
                "correct_answer": q.get("correct_answer"),
                "hints_count": len(q.get("hints", [])),
                "hints": q.get("hints"),
                "detailed_solution": q.get("detailed_solution"),
            })

    # 3. Select targeted anomaly samples from Risk Clusters for direct quotation
    risk_cluster_samples: dict[str, list[dict]] = {}
    risk_clusters = telemetry.get("risk_clusters", {})
    for cluster_name, item_ids in risk_clusters.items():
        risk_cluster_samples[cluster_name] = []
        for qid in item_ids[:5]:
            q_item = q_by_id.get(qid)
            if q_item:
                risk_cluster_samples[cluster_name].append({
                    "id": qid,
                    "competency_id": q_item.get("competency_id"),
                    "stem": q_item.get("stem"),
                    "options": q_item.get("options"),
                    "hints": q_item.get("hints"),
                    "detailed_solution": q_item.get("detailed_solution"),
                    "detected_issues": telemetry.get("issues_by_item", {}).get(qid, []),
                })

    return {
        "course_id": course_entry.get("id"),
        "filename": course_entry.get("filename"),
        "title": course_entry.get("title"),
        "description": data.get("description", ""),
        "total_competencies": len(competencies),
        "total_questions": len(questions),
        "question_types_distribution": types_count,
        "questions_per_competency": {cid: len(ql) for cid, ql in q_by_comp.items()},
        "evaluator_guidance": {
            "instruction": "Toda la telemetría métrica estática (conteo de KaTeX roto, distractores delatores, pistas faltantes, placeholders f-string y distribución de Bloom) ha sido calculada de manera estandarizada y determinista en 'audit_telemetry'. NO escribas ni ejecutes scripts de prueba exploratorios en Python. Aplica el Adaptive Semantic Loop y redacta directamente los reportes JSON y Markdown.",
            "risk_score": telemetry.get("risk_score", 0.0),
            "hard_penalties_precalculated": telemetry.get("hard_penalties", []),
        },
        "audit_telemetry": telemetry,
        "competencies": [
            {
                "id": c.get("id"),
                "name": c.get("name"),
                "category": c.get("category"),
                "description": c.get("description"),
                "prerequisites": c.get("prerequisites", []),
                "question_count": len(q_by_comp.get(c.get("id"), [])),
            }
            for c in competencies
        ],
        "stratified_samples": stratified_samples,
        "risk_cluster_samples": risk_cluster_samples,
    }


def main():
    parser = argparse.ArgumentParser(description="Course audit payload preparer")
    parser.add_argument("--list", action="store_true", help="List discovered courses in JSON")
    parser.add_argument("--course-id", type=str, help="Specific course ID or filename to prepare")
    parser.add_argument("--all", action="store_true", help="Prepare payloads for all courses")
    args = parser.parse_args()

    courses = get_available_courses()

    if args.list:
        summary_list = [
            {
                "id": c.get("id"),
                "filename": c.get("filename"),
                "title": c.get("title"),
                "status": c.get("status"),
                "competencies": c.get("total_competencies", 0),
                "questions": c.get("total_questions", 0),
            }
            for c in courses
        ]
        print(json.dumps(summary_list, indent=2, ensure_ascii=False))
        return

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    target_courses = []
    if args.all:
        target_courses = [c for c in courses if c.get("status") == "valid"]
    elif args.course_id:
        req = args.course_id.strip().lower()
        matched = [
            c for c in courses
            if c.get("id", "").lower() == req
            or c.get("filename", "").lower() == req
            or c.get("filename", "").lower() == f"{req}.json"
            or req in c.get("title", "").lower()
        ]
        if not matched:
            print(f"Error: Course '{args.course_id}' not found.", file=sys.stderr)
            sys.exit(1)
        target_courses = matched
    else:
        # Default behavior: list and exit
        print(f"Discovered {len(courses)} course(s). Use --course-id <id> or --all.")
        return

    for c in target_courses:
        pkg = summarize_course(c)
        cid = c.get("id")
        out_file = REPORTS_DIR / f"{cid}_payload.json"
        out_file.write_text(json.dumps(pkg, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Prepared enriched payload: {out_file.name} ({pkg['total_questions']} questions, {pkg['total_competencies']} comps, risk_score={pkg['evaluator_guidance']['risk_score']})")


if __name__ == "__main__":
    main()
