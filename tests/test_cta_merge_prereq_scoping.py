"""Unit tests for CTA merge prerequisite scoping and strict backward-only topological sorting.

Validates:
1. Multi-part local ID isolation (part_01 and part_02 using identical C-01, H-01, Hab-01).
   Prerequisites of part_01 stay bound to part_01 and are never overwritten by part_02 IDs.
2. 100% backward-only guarantee (comp_pos[prereq] < comp_pos[comp]) across all merged competencies.
3. Stable intra-part topological sorting when a competency at an earlier position depends on
   a competency declared at a later position within the same subpart.
4. Explicit cross-part prerequisite prefixes (e.g. 'part_01:C-01').
5. id_map.json payload schema containing 'competencies', 'distractors', and 'by_part'.
6. Full prerequisite DAG conformance through check_prerequisites_dag.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

import pytest

# Ensure skill directory is in sys.path
_SKILL_DIR = Path(__file__).resolve().parent.parent / ".agents" / "skills" / "content-to-course"
if str(_SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(_SKILL_DIR))

from check_cta import check_prerequisites_dag, validate_cta_rules
from cta_merge import merge_cta_parts


def _make_distractors(cid: str, ctype: str, page: int = 1, doc: str = "lecture.pdf") -> List[Dict[str, Any]]:
    clean_prefix = cid.replace("-", "")
    ctype_lower = ctype.lower()
    distractors: List[Dict[str, Any]] = []

    if ctype_lower in ("fact", "concept"):
        for k in range(1, 4):
            distractors.append({
                "id": f"D-{clean_prefix}-{k:02d}",
                "name": f"Distractor {k} for {cid}",
                "wrong_belief": f"Wrong belief {k}",
                "correct_belief": f"Correct belief {k}",
                "trigger": "When calculating",
                "manifestation": "$0$",
                "error_type": "conceptual_swap",
                "severity": "medium",
                "origin": "source",
                "evidence": {"doc": doc, "page": page},
                "remediation_hint": "Check fundamentals",
            })
    elif ctype_lower == "skill":
        for k in range(1, 5):
            distractors.append({
                "id": f"D-{clean_prefix}-{k:02d}",
                "name": f"Distractor {k} for {cid}",
                "wrong_belief": f"Wrong belief {k}",
                "correct_belief": f"Correct belief {k}",
                "omitted_step": None,
                "trigger": "When solving equation",
                "manifestation": "$0$",
                "error_type": "sign_error",
                "severity": "medium",
                "origin": "source",
                "evidence": {"doc": doc, "page": page},
                "remediation_hint": "Check signs",
            })
        for k in range(5, 7):
            distractors.append({
                "id": f"D-{clean_prefix}-{k:02d}",
                "name": f"Omitted Step {k} for {cid}",
                "wrong_belief": None,
                "correct_belief": f"Correct belief {k}",
                "omitted_step": f"Omitted step {k}",
                "trigger": "When solving equation",
                "manifestation": "$0$",
                "error_type": "skipped_step",
                "severity": "medium",
                "origin": "source",
                "evidence": {"doc": doc, "page": page},
                "remediation_hint": "Do not skip step",
            })
    return distractors


def _make_comp(
    cid: str,
    ctype: str,
    name: str,
    unit_index: int = 1,
    prerequisites: List[str] = None,
    doc: str = "lecture.pdf",
    page: int = 1,
    bloom: str = None,
) -> Dict[str, Any]:
    if not bloom:
        bloom_map = {"fact": "Remember", "concept": "Understand", "skill": "Apply"}
        bloom = bloom_map.get(ctype.lower(), "Understand")
    return {
        "id": cid,
        "type": ctype,
        "name": name,
        "description_latex": f"Description for ${cid}$",
        "bloom": bloom,
        "session": f"Unidad {unit_index}: Tema",
        "unit_index": unit_index,
        "evidence": [{"doc": doc, "page": page}],
        "prerequisites": prerequisites or [],
        "distractors": _make_distractors(cid, ctype, page=page, doc=doc),
    }


def _setup_work_env(tmp_path: Path, subparts: List[Dict[str, Any]]) -> Path:
    work_dir = tmp_path / "work"
    work_dir.mkdir(parents=True, exist_ok=True)
    parts_dir = work_dir / "cta_parts"
    parts_dir.mkdir(parents=True, exist_ok=True)

    manifest_data = {
        "course_id": "test_prereq_scoping",
        "cta_mode": "mapreduce",
        "total_files": 1,
        "total_pages": 10,
        "files": [{"file_index": 0, "doc": "lecture.pdf", "doc_slug": "lecture", "total_pages": 10, "valid_page_range": [1, 10]}],
        "subparts": subparts,
    }
    (work_dir / "pre_cta_manifest.json").write_text(json.dumps(manifest_data, indent=2), encoding="utf-8")
    return work_dir


class TestCtaMergePrereqScoping:
    """Test suite for prerequisite scoping across parts and DAG guarantees."""

    def test_two_parts_identical_local_ids_scoping(self, tmp_path: Path):
        """Part 1 and Part 2 both use local C-01, H-01, Hab-01.

        Verifies that:
        - part_01 prerequisites point to part_01 renumbered IDs (e.g. H-01, C-01).
        - part_01 prerequisites are NEVER overwritten by part_02 renumbered IDs (e.g. H-02, C-02).
        - part_02 prerequisites point to part_02 renumbered IDs.
        """
        subparts = [
            {"subpart_id": "part_01", "subpart_index": 0, "doc": "lecture.pdf", "file_index": 0},
            {"subpart_id": "part_02", "subpart_index": 1, "doc": "lecture.pdf", "file_index": 0},
        ]
        work_dir = _setup_work_env(tmp_path, subparts)
        parts_dir = work_dir / "cta_parts"

        # Part 1 uses C-01, H-01, Hab-01
        part_01 = {
            "course_id": "test_prereq_scoping",
            "competencies": [
                _make_comp("H-01", "fact", "Fact P1", unit_index=1, page=1),
                _make_comp("C-01", "concept", "Concept P1", unit_index=1, prerequisites=["H-01"], page=1),
                _make_comp("Hab-01", "skill", "Skill P1", unit_index=1, prerequisites=["C-01", "H-01"], page=1),
            ],
        }
        (parts_dir / "part_01.json").write_text(json.dumps(part_01, indent=2), encoding="utf-8")

        # Part 2 ALSO uses identical local IDs C-01, H-01, Hab-01
        part_02 = {
            "course_id": "test_prereq_scoping",
            "competencies": [
                _make_comp("H-01", "fact", "Fact P2", unit_index=2, page=2),
                _make_comp("C-01", "concept", "Concept P2", unit_index=2, prerequisites=["H-01"], page=2),
                _make_comp("Hab-01", "skill", "Skill P2", unit_index=2, prerequisites=["C-01", "H-01"], page=2),
            ],
        }
        (parts_dir / "part_02.json").write_text(json.dumps(part_02, indent=2), encoding="utf-8")

        res = merge_cta_parts(work_dir)
        comps = res["competencies"]
        assert len(comps) == 6

        # IDs in Part 1 should be H-01, C-01, Hab-01
        # IDs in Part 2 should be H-02, C-02, Hab-02
        c_p1_fact = next(c for c in comps if c["name"] == "Fact P1")
        c_p1_concept = next(c for c in comps if c["name"] == "Concept P1")
        c_p1_skill = next(c for c in comps if c["name"] == "Skill P1")

        c_p2_fact = next(c for c in comps if c["name"] == "Fact P2")
        c_p2_concept = next(c for c in comps if c["name"] == "Concept P2")
        c_p2_skill = next(c for c in comps if c["name"] == "Skill P2")

        assert c_p1_fact["id"] == "H-01"
        assert c_p1_concept["id"] == "C-01"
        assert c_p1_skill["id"] == "Hab-01"

        assert c_p2_fact["id"] == "H-02"
        assert c_p2_concept["id"] == "C-02"
        assert c_p2_skill["id"] == "Hab-02"

        # Check part 1 prerequisites: must resolve within part 1!
        assert c_p1_concept["prerequisites"] == ["H-01"]
        assert set(c_p1_skill["prerequisites"]) == {"C-01", "H-01"}
        # Must NEVER reference H-02 or C-02 from part 2!
        assert "H-02" not in c_p1_concept["prerequisites"]
        assert "H-02" not in c_p1_skill["prerequisites"]
        assert "C-02" not in c_p1_skill["prerequisites"]

        # Check part 2 prerequisites: must resolve within part 2!
        assert c_p2_concept["prerequisites"] == ["H-02"]
        assert set(c_p2_skill["prerequisites"]) == {"C-02", "H-02"}

        # Validate backward-only invariant for 100% of competencies
        comp_pos = {c["id"]: idx for idx, c in enumerate(comps)}
        for idx, c in enumerate(comps):
            for prereq in c["prerequisites"]:
                assert comp_pos[prereq] < idx, f"Forward prereq violation: {prereq} -> {c['id']}"

        # Verify id_map.json structure
        id_map_file = work_dir / "id_map.json"
        assert id_map_file.is_file()
        id_map = json.loads(id_map_file.read_text(encoding="utf-8"))
        assert "competencies" in id_map
        assert "distractors" in id_map
        assert "by_part" in id_map
        assert id_map["by_part"]["part_01"]["C-01"] == "C-01"
        assert id_map["by_part"]["part_02"]["C-01"] == "C-02"

    def test_explicit_cross_part_prerequisite_prefix(self, tmp_path: Path):
        """Cross-part prerequisite using explicit prefix (e.g. 'part_01:C-01') resolves cleanly."""
        subparts = [
            {"subpart_id": "part_01", "subpart_index": 0, "doc": "lecture.pdf", "file_index": 0},
            {"subpart_id": "part_02", "subpart_index": 1, "doc": "lecture.pdf", "file_index": 0},
        ]
        work_dir = _setup_work_env(tmp_path, subparts)
        parts_dir = work_dir / "cta_parts"

        part_01 = {
            "course_id": "test_prereq_scoping",
            "competencies": [
                _make_comp("C-01", "concept", "Base Concept P1", unit_index=1, page=1),
            ],
        }
        (parts_dir / "part_01.json").write_text(json.dumps(part_01, indent=2), encoding="utf-8")

        # Part 2 explicitly references part_01:C-01
        part_02 = {
            "course_id": "test_prereq_scoping",
            "competencies": [
                _make_comp("C-01", "concept", "Advanced Concept P2", unit_index=2, prerequisites=["part_01:C-01"], page=2),
            ],
        }
        (parts_dir / "part_02.json").write_text(json.dumps(part_02, indent=2), encoding="utf-8")

        res = merge_cta_parts(work_dir)
        comps = res["competencies"]
        assert len(comps) == 2

        c_p1 = comps[0]
        c_p2 = comps[1]

        assert c_p1["id"] == "C-01"
        assert c_p2["id"] == "C-02"
        # part_01:C-01 should resolve to C-01
        assert c_p2["prerequisites"] == ["C-01"]

    def test_intra_part_topological_sort_inverts_order(self, tmp_path: Path):
        """If competency on page 2 depends on competency on page 3 within the same part,

        intra-part topological sort stably places the prerequisite first before assigning IDs.
        """
        subparts = [
            {"subpart_id": "part_01", "subpart_index": 0, "doc": "lecture.pdf", "file_index": 0},
        ]
        work_dir = _setup_work_env(tmp_path, subparts)
        parts_dir = work_dir / "cta_parts"

        # C-01 is at page 2, but depends on C-02 which is at page 3
        part_01 = {
            "course_id": "test_prereq_scoping",
            "competencies": [
                _make_comp("C-01", "concept", "Derivative Concept", unit_index=2, prerequisites=["C-02"], page=2),
                _make_comp("C-02", "concept", "Fundamental Concept", unit_index=3, prerequisites=[], page=3),
            ],
        }
        (parts_dir / "part_01.json").write_text(json.dumps(part_01, indent=2), encoding="utf-8")

        res = merge_cta_parts(work_dir)
        comps = res["competencies"]
        assert len(comps) == 2

        # Fundamental Concept must now be first (C-01) and Derivative Concept second (C-02)
        assert comps[0]["name"] == "Fundamental Concept"
        assert comps[0]["id"] == "C-01"
        assert comps[0]["prerequisites"] == []

        assert comps[1]["name"] == "Derivative Concept"
        assert comps[1]["id"] == "C-02"
        assert comps[1]["prerequisites"] == ["C-01"]

        # Ensure DAG check passes with 0 errors
        dag_errors = check_prerequisites_dag(comps)
        assert len(dag_errors) == 0

    def test_strict_backward_only_guarantee_drops_unresolvable_forward_prereqs(self, tmp_path: Path):
        """Unresolvable forward prerequisites or cycles are safely dropped, guaranteeing zero forward references."""
        subparts = [
            {"subpart_id": "part_01", "subpart_index": 0, "doc": "lecture.pdf", "file_index": 0},
            {"subpart_id": "part_02", "subpart_index": 1, "doc": "lecture.pdf", "file_index": 0},
        ]
        work_dir = _setup_work_env(tmp_path, subparts)
        parts_dir = work_dir / "cta_parts"

        # Mutual cycle across parts: P1 depends forward on P2
        part_01 = {
            "course_id": "test_prereq_scoping",
            "competencies": [
                _make_comp("C-01", "concept", "Concept P1", unit_index=1, prerequisites=["part_02:C-01"], page=1),
            ],
        }
        (parts_dir / "part_01.json").write_text(json.dumps(part_01, indent=2), encoding="utf-8")

        part_02 = {
            "course_id": "test_prereq_scoping",
            "competencies": [
                _make_comp("C-01", "concept", "Concept P2", unit_index=2, prerequisites=["part_01:C-01"], page=2),
            ],
        }
        (parts_dir / "part_02.json").write_text(json.dumps(part_02, indent=2), encoding="utf-8")

        res = merge_cta_parts(work_dir)
        comps = res["competencies"]
        assert len(comps) == 2

        comp_pos = {c["id"]: idx for idx, c in enumerate(comps)}
        # C-01 (Part 1, index 0) cannot depend forward on C-02 (Part 2, index 1)
        assert "C-02" not in comps[0]["prerequisites"]
        assert comps[0]["prerequisites"] == []

        # C-02 (Part 2, index 1) can depend backward on C-01 (Part 1, index 0)
        assert comps[1]["prerequisites"] == ["C-01"]

        # 0 forward prerequisites across the entire course
        for idx, c in enumerate(comps):
            for p in c["prerequisites"]:
                assert comp_pos[p] < idx

    def test_full_dag_validation_with_check_prerequisites_dag(self, tmp_path: Path):
        """End-to-end multi-part scenario satisfies check_prerequisites_dag with 0 errors."""
        subparts = [
            {"subpart_id": "part_01", "subpart_index": 0, "doc": "lecture.pdf", "file_index": 0},
            {"subpart_id": "part_02", "subpart_index": 1, "doc": "lecture.pdf", "file_index": 0},
            {"subpart_id": "part_03", "subpart_index": 2, "doc": "lecture.pdf", "file_index": 0},
        ]
        work_dir = _setup_work_env(tmp_path, subparts)
        parts_dir = work_dir / "cta_parts"

        part_01 = {
            "course_id": "test_prereq_scoping",
            "competencies": [
                _make_comp("H-01", "fact", "Fact A", unit_index=1, page=1),
                _make_comp("C-01", "concept", "Concept A", unit_index=1, prerequisites=["H-01"], page=1),
            ],
        }
        part_02 = {
            "course_id": "test_prereq_scoping",
            "competencies": [
                _make_comp("H-01", "fact", "Fact B", unit_index=2, page=2),
                _make_comp("C-01", "concept", "Concept B", unit_index=2, prerequisites=["H-01", "part_01:C-01"], page=2),
            ],
        }
        part_03 = {
            "course_id": "test_prereq_scoping",
            "competencies": [
                _make_comp("Hab-01", "skill", "Skill C", unit_index=3, prerequisites=["part_01:C-01", "part_02:C-01"], page=3),
            ],
        }

        (parts_dir / "part_01.json").write_text(json.dumps(part_01, indent=2), encoding="utf-8")
        (parts_dir / "part_02.json").write_text(json.dumps(part_02, indent=2), encoding="utf-8")
        (parts_dir / "part_03.json").write_text(json.dumps(part_03, indent=2), encoding="utf-8")

        res = merge_cta_parts(work_dir)
        comps = res["competencies"]
        assert len(comps) == 5

        dag_errors = check_prerequisites_dag(comps)
        assert len(dag_errors) == 0, f"DAG errors encountered: {dag_errors}"

    def test_intra_part_cycle_fallback_deterministic_dag(self, tmp_path: Path):
        """Author mistakenly introduces an accidental cycle A <-> B within the same part.

        Verifies that:
        - Intra-part topological sort degrades cleanly using deterministic sort key fallback.
        - No infinite loop occurs and zero competencies are lost.
        - Strict backward-only filter removes the forward edge, leaving 0 DAG errors.
        - Neither '_part_key' nor '_sort_key' remain in cta_draft.json or cta.json.
        """
        subparts = [
            {"subpart_id": "part_01", "subpart_index": 0, "doc": "lecture.pdf", "file_index": 0},
        ]
        work_dir = _setup_work_env(tmp_path, subparts)
        parts_dir = work_dir / "cta_parts"

        part_01 = {
            "course_id": "test_prereq_scoping",
            "competencies": [
                _make_comp("H-01", "fact", "Fact Root", unit_index=1, page=1),
                _make_comp("C-01", "concept", "Concept Alpha", unit_index=1, prerequisites=["C-02"], page=1),
                _make_comp("C-02", "concept", "Concept Beta", unit_index=1, prerequisites=["C-01"], page=2),
            ],
        }
        (parts_dir / "part_01.json").write_text(json.dumps(part_01, indent=2), encoding="utf-8")

        res = merge_cta_parts(work_dir)
        comps = res["competencies"]
        assert len(comps) == 3

        comp_by_name = {c["name"]: c for c in comps}
        c_root = comp_by_name["Fact Root"]
        c_alpha = comp_by_name["Concept Alpha"]
        c_beta = comp_by_name["Concept Beta"]

        assert c_root["id"] == "H-01"
        assert c_alpha["id"] == "C-01"
        assert c_beta["id"] == "C-02"

        # Alpha appeared before Beta in sort order, so Alpha's forward edge to Beta is dropped,
        # while Beta's backward edge to Alpha is kept.
        assert c_alpha["prerequisites"] == []
        assert c_beta["prerequisites"] == ["C-01"]

        # Strict backward-only invariant
        comp_pos = {c["id"]: idx for idx, c in enumerate(comps)}
        for idx, c in enumerate(comps):
            for p in c["prerequisites"]:
                assert comp_pos[p] < idx

        # Full DAG validation must pass with 0 errors
        dag_errors = check_prerequisites_dag(comps)
        assert len(dag_errors) == 0, f"DAG errors: {dag_errors}"

        # Guarantee no temporary internal keys leak to disk
        draft_json = json.loads((work_dir / "cta_draft.json").read_text(encoding="utf-8"))
        final_json = json.loads((work_dir / "cta.json").read_text(encoding="utf-8"))
        for item in draft_json["competencies"] + final_json["competencies"]:
            assert "_part_key" not in item, f"Leaked _part_key in {item.get('id')}"
            assert "_sort_key" not in item, f"Leaked _sort_key in {item.get('id')}"

    def test_incremental_append_preserves_base_course_prereqs(self, tmp_path: Path):
        """Incremental mode (--append) with base course competencies.

        Verifies that:
        - External prerequisites to existing base course competencies are preserved intact.
        - Intra-part local IDs are renumbered without collision or unintended cross-part remapping.
        - validate_cta_rules passes with 0 errors.
        """
        subparts = [
            {"subpart_id": "part_01", "subpart_index": 0, "doc": "lecture.pdf", "file_index": 0},
            {"subpart_id": "part_02", "subpart_index": 1, "doc": "lecture.pdf", "file_index": 0},
        ]
        work_dir = tmp_path / "work"
        work_dir.mkdir(parents=True, exist_ok=True)
        parts_dir = work_dir / "cta_parts"
        parts_dir.mkdir(parents=True, exist_ok=True)

        manifest_data = {
            "course_id": "test_append_course",
            "cta_mode": "mapreduce",
            "total_files": 1,
            "total_pages": 10,
            "files": [{"file_index": 0, "doc": "lecture.pdf", "doc_slug": "lecture", "total_pages": 10, "valid_page_range": [1, 10]}],
            "subparts": subparts,
            "delta": {
                "existing_competency_ids": ["C-01", "H-01"],
                "next_numbers_by_prefix": {"C": 2, "H": 2, "Hab": 1},
            },
        }
        (work_dir / "pre_cta_manifest.json").write_text(json.dumps(manifest_data, indent=2), encoding="utf-8")

        # Part 1 uses local C-01, Hab-01. C-01 depends on base course H-01.
        part_01 = {
            "course_id": "test_append_course",
            "competencies": [
                _make_comp("C-01", "concept", "Concept New P1", unit_index=1, prerequisites=["H-01"], page=1),
                _make_comp("Hab-01", "skill", "Skill New P1", unit_index=1, prerequisites=["C-01", "H-01"], page=1),
            ],
        }
        (parts_dir / "part_01.json").write_text(json.dumps(part_01, indent=2), encoding="utf-8")

        # Part 2 defines new fact H-01 and concept C-01.
        # Concept C-01 depends on local H-01, cross-part part_01:C-01, and base course C-01 via 'base:C-01'.
        part_02 = {
            "course_id": "test_append_course",
            "competencies": [
                _make_comp("H-01", "fact", "Fact New P2", unit_index=2, page=2),
                _make_comp("C-01", "concept", "Concept New P2", unit_index=2, prerequisites=["H-01", "part_01:C-01", "base:C-01"], page=2),
            ],
        }
        (parts_dir / "part_02.json").write_text(json.dumps(part_02, indent=2), encoding="utf-8")

        res = merge_cta_parts(work_dir)
        comps = res["competencies"]
        assert len(comps) == 4

        # Part 1: C-01 -> C-02, Hab-01 -> Hab-01
        # Part 2: H-01 -> H-02, C-01 -> C-03
        c_p1_concept = next(c for c in comps if c["name"] == "Concept New P1")
        c_p1_skill = next(c for c in comps if c["name"] == "Skill New P1")
        c_p2_fact = next(c for c in comps if c["name"] == "Fact New P2")
        c_p2_concept = next(c for c in comps if c["name"] == "Concept New P2")

        assert c_p1_concept["id"] == "C-02"
        assert c_p1_skill["id"] == "Hab-01"
        assert c_p2_fact["id"] == "H-02"
        assert c_p2_concept["id"] == "C-03"

        # Check that base course H-01 was preserved and NOT mapped to part_02's H-02
        assert c_p1_concept["prerequisites"] == ["H-01"]
        assert set(c_p1_skill["prerequisites"]) == {"C-02", "H-01"}

        # Check part 2 resolution:
        # local H-01 -> H-02
        # part_01:C-01 -> C-02
        # base:C-01 -> C-01
        assert set(c_p2_concept["prerequisites"]) == {"H-02", "C-02", "C-01"}

        # Validate with check_prerequisites_dag allowing base course IDs
        dag_errors = check_prerequisites_dag(comps, allowed_prereq_ids={"C-01", "H-01"})
        assert len(dag_errors) == 0, f"DAG errors: {dag_errors}"

        # Validate with validate_cta_rules
        valid, rules_errors = validate_cta_rules(res, manifest_data)
        assert valid is True, f"validate_cta_rules failed: {rules_errors}"
        assert len(rules_errors) == 0

    def test_asymptotic_statistics_v6_scale_simulation(self, tmp_path: Path):
        """Full-scale simulation of asymptotic_statistics_v6 (2 parts, 12 + 13 = 25 competencies).

        Both part_01 and part_02 number their competencies starting locally from C-01, H-01, Hab-01.
        Verifies:
        - Correct sequential renumbering across parts (8 facts, 9 concepts, 8 skills).
        - 0 forward prerequisites across all 25 competencies.
        - check_prerequisites_dag passes with 0 errors.
        - validate_cta_rules passes with True and 0 errors.
        - Cleanliness of temporary keys (_part_key, _sort_key).
        """
        doc_name = "asymptotic_statistics.pdf"
        subparts = [
            {"subpart_id": "part_01", "subpart_index": 0, "doc": doc_name, "file_index": 0},
            {"subpart_id": "part_02", "subpart_index": 1, "doc": doc_name, "file_index": 0},
        ]
        work_dir = tmp_path / "work"
        work_dir.mkdir(parents=True, exist_ok=True)
        parts_dir = work_dir / "cta_parts"
        parts_dir.mkdir(parents=True, exist_ok=True)

        manifest_data = {
            "course_id": "asymptotic_statistics_v6",
            "cta_mode": "mapreduce",
            "total_files": 1,
            "total_pages": 30,
            "files": [{"file_index": 0, "doc": doc_name, "doc_slug": "asymptotic_statistics", "total_pages": 30, "valid_page_range": [1, 30]}],
            "subparts": subparts,
        }
        (work_dir / "pre_cta_manifest.json").write_text(json.dumps(manifest_data, indent=2), encoding="utf-8")

        # Part 1: 12 competencies (4 facts, 4 concepts, 4 skills) on pages 1..6
        p1_comps = [
            # 4 Facts
            _make_comp("H-01", "fact", "Propiedad Asintótica Básica", unit_index=1, page=1, doc=doc_name),
            _make_comp("H-02", "fact", "Lema de Slutsky Condición", unit_index=1, page=2, doc=doc_name),
            _make_comp("H-03", "fact", "Teorema del Mapeo Continuo", unit_index=2, page=3, doc=doc_name),
            _make_comp("H-04", "fact", "Convergencia en Probabilidad", unit_index=2, page=4, doc=doc_name),
            # 4 Concepts (with intra-part dependencies)
            _make_comp("C-01", "concept", "Concepto Consistencia Débil", unit_index=1, prerequisites=["H-01"], page=2, doc=doc_name),
            _make_comp("C-02", "concept", "Concepto Normalidad Asintótica", unit_index=2, prerequisites=["H-02"], page=3, doc=doc_name),
            _make_comp("C-03", "concept", "Distribución Límite", unit_index=2, prerequisites=["C-01", "H-03"], page=4, doc=doc_name),
            _make_comp("C-04", "concept", "Eficiencia Asintótica", unit_index=3, prerequisites=["C-02", "H-04"], page=5, doc=doc_name),
            # 4 Skills (with intra-part dependencies)
            _make_comp("Hab-01", "skill", "Calcular Límite en Probabilidad", unit_index=2, prerequisites=["C-01", "H-01"], page=3, doc=doc_name),
            _make_comp("Hab-02", "skill", "Aplicar Expansión Delta", unit_index=3, prerequisites=["C-02", "H-02"], page=4, doc=doc_name),
            _make_comp("Hab-03", "skill", "Derivar Varianza Asintótica", unit_index=3, prerequisites=["Hab-01", "C-03"], page=5, doc=doc_name),
            _make_comp("Hab-04", "skill", "Comprobar Eficiencia relativa", unit_index=3, prerequisites=["Hab-02", "C-04"], page=6, doc=doc_name),
        ]
        part_01 = {"course_id": "asymptotic_statistics_v6", "competencies": p1_comps}
        (parts_dir / "part_01.json").write_text(json.dumps(part_01, indent=2), encoding="utf-8")

        # Part 2: 13 competencies (4 facts, 5 concepts, 4 skills) on pages 11..17
        # Also numbering from H-01, C-01, Hab-01 locally!
        p2_comps = [
            # 4 Facts
            _make_comp("H-01", "fact", "Estimador M-Estimador Hipótesis", unit_index=4, prerequisites=["part_01:H-01"], page=11, doc=doc_name),
            _make_comp("H-02", "fact", "Condición de Rango e Identificación", unit_index=4, page=12, doc=doc_name),
            _make_comp("H-03", "fact", "Matriz de Información de Fisher", unit_index=5, page=13, doc=doc_name),
            _make_comp("H-04", "fact", "Test de Razón de Verosimilitud", unit_index=5, page=14, doc=doc_name),
            # 5 Concepts
            _make_comp("C-01", "concept", "Concepto M-Estimadores", unit_index=4, prerequisites=["H-01", "part_01:C-01"], page=12, doc=doc_name),
            _make_comp("C-02", "concept", "Concepto Identificabilidad Local", unit_index=4, prerequisites=["H-02", "C-01"], page=13, doc=doc_name),
            _make_comp("C-03", "concept", "Cota de Cramér-Rao", unit_index=5, prerequisites=["H-03"], page=14, doc=doc_name),
            _make_comp("C-04", "concept", "Distribución del Test LRT", unit_index=5, prerequisites=["H-04", "C-03"], page=15, doc=doc_name),
            _make_comp("C-05", "concept", "Wald y Multiplicadores de Lagrange", unit_index=6, prerequisites=["C-04", "part_01:C-02"], page=16, doc=doc_name),
            # 4 Skills
            _make_comp("Hab-01", "skill", "Construir Estimador GMM", unit_index=5, prerequisites=["C-01", "H-01"], page=14, doc=doc_name),
            _make_comp("Hab-02", "skill", "Contrastar Hipótesis con Wald", unit_index=5, prerequisites=["C-03", "part_01:Hab-01"], page=15, doc=doc_name),
            _make_comp("Hab-03", "skill", "Calcular Estadístico LRT", unit_index=6, prerequisites=["Hab-01", "C-04"], page=16, doc=doc_name),
            _make_comp("Hab-04", "skill", "Evaluar Robustez Asintótica", unit_index=6, prerequisites=["Hab-02", "C-05"], page=17, doc=doc_name),
        ]
        part_02 = {"course_id": "asymptotic_statistics_v6", "competencies": p2_comps}
        (parts_dir / "part_02.json").write_text(json.dumps(part_02, indent=2), encoding="utf-8")

        res = merge_cta_parts(work_dir)
        comps = res["competencies"]

        # Validate total counts
        assert len(comps) == 25
        fact_ids = [c["id"] for c in comps if c["type"] == "fact"]
        concept_ids = [c["id"] for c in comps if c["type"] == "concept"]
        skill_ids = [c["id"] for c in comps if c["type"] == "skill"]

        assert len(fact_ids) == 8
        assert fact_ids == [f"H-{i:02d}" for i in range(1, 9)]
        assert len(concept_ids) == 9
        assert concept_ids == [f"C-{i:02d}" for i in range(1, 10)]
        assert len(skill_ids) == 8
        assert skill_ids == [f"Hab-{i:02d}" for i in range(1, 9)]

        # Validate 0 forward prerequisites across the entire course
        comp_pos = {c["id"]: idx for idx, c in enumerate(comps)}
        for idx, comp in enumerate(comps):
            for prereq in comp["prerequisites"]:
                assert comp_pos[prereq] < idx, f"Forward prereq violation: {prereq} -> {comp['id']}"

        # Validate check_prerequisites_dag
        dag_errors = check_prerequisites_dag(comps)
        assert len(dag_errors) == 0, f"check_prerequisites_dag reported errors: {dag_errors}"

        # Validate full validate_cta_rules
        valid, rules_errors = validate_cta_rules(res, manifest_data)
        assert valid is True, f"validate_cta_rules returned False: {rules_errors}"
        assert len(rules_errors) == 0

        # Guarantee no temporary internal keys leak to disk
        draft_json = json.loads((work_dir / "cta_draft.json").read_text(encoding="utf-8"))
        final_json = json.loads((work_dir / "cta.json").read_text(encoding="utf-8"))
        for item in draft_json["competencies"] + final_json["competencies"]:
            assert "_part_key" not in item, f"Leaked _part_key in {item.get('id')}"
            assert "_sort_key" not in item, f"Leaked _sort_key in {item.get('id')}"
