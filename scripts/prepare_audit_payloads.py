#!/usr/bin/env python3
"""Prepare course payloads for QA auditor subagents.

Extracts published courses from courses/ directory and formats them into
structured audit payloads with detailed statistics and representative question samples.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
COURSES_DIR = ROOT_DIR / "courses"
REPORTS_DIR = ROOT_DIR / "reports" / "qa_audits"


def get_published_courses() -> list[dict]:
    """Return all valid published course JSON payloads."""
    results = []
    for f in sorted(COURSES_DIR.glob("*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            if isinstance(data, dict) and data.get("course_id") and data.get("competencies"):
                results.append({"path": str(f), "filename": f.name, "data": data})
        except Exception as e:
            print(f"Error loading {f.name}: {e}")
    return results


def summarize_course_for_qa(course: dict) -> dict:
    """Prepare a structured audit package for a course."""
    data = course["data"]
    competencies = data.get("competencies", [])
    questions = data.get("questions", [])

    # Metrics
    comp_map = {c.get("id"): c for c in competencies}
    q_by_comp: dict[str, list[dict]] = {c.get("id"): [] for c in competencies}

    hint_counts: list[int] = []
    missing_hints: list[str] = []
    latex_in_stem: int = 0
    types_count: dict[str, int] = {}

    for q in questions:
        cid = q.get("competency_id", "unassigned")
        if cid not in q_by_comp:
            q_by_comp[cid] = []
        q_by_comp[cid].append(q)

        hints = q.get("hints", [])
        hint_counts.append(len(hints))
        if len(hints) == 0:
            missing_hints.append(q.get("id", "unknown"))

        qtype = q.get("interaction_type") or q.get("type", "unknown")
        types_count[qtype] = types_count.get(qtype, 0) + 1

        stem = q.get("stem", "")
        if "$" in stem:
            latex_in_stem += 1

    # Select representative sample (first 2-3 questions per competency)
    sample_questions = []
    for cid, qlist in q_by_comp.items():
        comp_info = comp_map.get(cid, {})
        for q in qlist[:3]:  # sample up to 3 per competency
            sample_questions.append({
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

    summary = {
        "course_id": data.get("course_id"),
        "title": data.get("title") or data.get("course_title"),
        "description": data.get("description"),
        "total_competencies": len(competencies),
        "total_questions": len(questions),
        "question_types_distribution": types_count,
        "questions_per_competency": {cid: len(ql) for cid, ql in q_by_comp.items()},
        "questions_with_zero_hints_count": len(missing_hints),
        "sample_questions_count": len(sample_questions),
        "competencies": [
            {
                "id": c.get("id"),
                "name": c.get("name"),
                "category": c.get("category"),
                "description": c.get("description"),
                "question_count": len(q_by_comp.get(c.get("id"), [])),
            }
            for c in competencies
        ],
        "sample_questions": sample_questions,
    }
    return summary


def main():
    courses = get_published_courses()
    print(f"Found {len(courses)} published courses.")
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    for c in courses:
        file_stem = Path(c["filename"]).stem
        pkg = summarize_course_for_qa(c)
        pkg["filename"] = c["filename"]
        out_file = REPORTS_DIR / f"{file_stem}_payload.json"
        out_file.write_text(json.dumps(pkg, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Prepared QA payload for '{file_stem}' ({c['filename']}) -> {out_file.name} ({pkg['total_questions']} questions, {pkg['total_competencies']} comps)")


if __name__ == "__main__":
    main()
