"""End-to-end regression test for the M20 canonical course builder (P0-2)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
SKILL_DIR = ROOT_DIR / ".agents" / "skills" / "content-to-course"
QA_DIR = ROOT_DIR / ".agents" / "skills" / "course-qa-evaluator" / "scripts"
FIXTURE_DIR = ROOT_DIR / "tests" / "fixtures" / "m20_canonical_cases"

for p in (str(SKILL_DIR), str(QA_DIR), str(FIXTURE_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

CANONICAL_8_MODALITIES = {
    "multiple_choice_7_options",
    "fill_in_the_blank",
    "open_symbolic",
    "proof_dag",
    "adversarial_break",
    "unstructured_model",
    "invariant_canvas",
    "concept_matching",
}


def test_build_canonical_course_v2_contract_and_qa_audit(tmp_path: Path):
    import build_canonical_course
    import standardized_audit_engine

    out_json = tmp_path / "m20_canonical_course.json"
    rc = build_canonical_course.main(out_json=out_json)
    assert rc == 0
    assert out_json.is_file()

    course = json.loads(out_json.read_text(encoding="utf-8"))
    assert str(course.get("contract_version")) in ("2", "2.0")

    comps = course.get("competencies") or []
    assert [c["id"] for c in comps] == ["Hab-01", "Hab-02", "C-01", "C-02"]

    questions = course.get("questions") or []
    assert len(questions) == 101

    qtypes_present = {q.get("type") for q in questions}
    assert CANONICAL_8_MODALITIES <= qtypes_present, (
        f"Missing canonical modalities: {CANONICAL_8_MODALITIES - qtypes_present}"
    )

    # Verify 0 MC7 in Skills (Hab-01, Hab-02) and <= 1 MC7 template share in Concepts
    by_cid = {}
    for q in questions:
        by_cid.setdefault(q["competency_id"], []).append(q)

    for skill_cid in ("Hab-01", "Hab-02"):
        mc7_count = sum(1 for q in by_cid[skill_cid] if q.get("type") == "multiple_choice_7_options")
        assert mc7_count == 0, f"Skill {skill_cid} must have 0 MC7 items, found {mc7_count}"

    # Run deterministic QA audit and assert zero M20 modality/quota issues
    audit = standardized_audit_engine.run_full_audit(course)
    issues = audit.get("issues") or []
    m20_issues = [
        i for i in issues
        if "[M20-MC7-CAP]" in str(i.get("message", "")) or "[M20-ACTIVE-QUOTA]" in str(i.get("message", ""))
    ]
    assert not m20_issues, f"Unexpected M20 quota/cap issues: {m20_issues}"
