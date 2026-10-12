"""Unit tests for Component 2: CTA Map-Reduce, Harmonizer, and Sectional Validation."""

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

import pytest

# Ensure skill directory is in sys.path
SKILL_DIR = Path(__file__).parent.parent / ".agents" / "skills" / "content-to-course"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from check_cta import check_cta_part, validate_cta_rules
from cta_merge import (
    apply_harmonize,
    find_duplicate_candidates,
    merge_cta_parts,
    render_cta_md,
)


def make_mock_distractor(
    did: str,
    name: str = "Common Mistake",
    wrong_belief: str = "Sign is positive instead of negative",
    omitted_step: str = None,
    doc: str = "lec01.pdf",
    page: int = 1,
) -> Dict[str, Any]:
    """Helper to create a schema-valid distractor."""
    return {
        "id": did,
        "name": name,
        "wrong_belief": wrong_belief,
        "correct_belief": "Sign must be negative following the chain rule",
        "omitted_step": omitted_step,
        "trigger": "When multiplying two negative factors",
        "manifestation": "Produces +14 instead of -14",
        "error_type": "sign_error",
        "severity": "medium",
        "origin": "source",
        "evidence": {"doc": doc, "page": page},
        "remediation_hint": "Check the signs of the coefficients carefully.",
    }


def make_mock_competency(
    cid: str,
    ctype: str = "concept",
    name: str = "Canonical Concept",
    desc: str = "Mathematical explanation of the theorem",
    session: str = "Sesión 1",
    unit_index: int = 1,
    prerequisites: List[str] = None,
    doc: str = "lec01.pdf",
    page: int = 1,
) -> Dict[str, Any]:
    """Helper to create a schema-valid competency."""
    clean_prefix = cid.replace("-", "")
    ctype_lower = ctype.lower()
    distractors = []

    if ctype_lower in ("fact", "concept"):
        # Minimum 3 distractors required
        for k in range(1, 4):
            distractors.append(
                make_mock_distractor(
                    did=f"D-{clean_prefix}-{k:02d}",
                    name=f"Trap {k} for {cid}",
                    doc=doc,
                    page=page,
                )
            )
    elif ctype_lower == "skill":
        # Minimum 6 distractors required, >=2 with omitted_step
        for k in range(1, 5):
            distractors.append(
                make_mock_distractor(
                    did=f"D-{clean_prefix}-{k:02d}",
                    name=f"Trap {k} for {cid}",
                    wrong_belief=f"Flawed rule {k}",
                    omitted_step=None,
                    doc=doc,
                    page=page,
                )
            )
        for k in range(5, 7):
            distractors.append(
                make_mock_distractor(
                    did=f"D-{clean_prefix}-{k:02d}",
                    name=f"Skipped Step {k} for {cid}",
                    wrong_belief=None,
                    omitted_step=f"Omitted intermediate calculation step {k}",
                    doc=doc,
                    page=page,
                )
            )

    bloom_map = {"fact": "Remember", "concept": "Understand", "skill": "Apply"}

    return {
        "id": cid,
        "type": ctype_lower,
        "name": name,
        "description_latex": desc,
        "bloom": bloom_map.get(ctype_lower, "Apply"),
        "session": session,
        "unit_index": unit_index,
        "prerequisites": prerequisites or [],
        "evidence": [{"doc": doc, "page": page}],
        "distractors": distractors,
    }


class TestCTAMergeMapReduce:
    """Test suite for sectional CTA merge and canonical ID renumbering."""

    def test_merge_cta_parts_generates_draft_outline_candidates_and_renumbers(self, tmp_path: Path):
        work_dir = tmp_path / "work"
        parts_dir = work_dir / "cta_parts"
        parts_dir.mkdir(parents=True)

        # Section 1: H-01, C-01, Hab-01
        part1 = {
            "course_id": "stats_101",
            "title": "Introduction to Probability",
            "section_index": 1,
            "competencies": [
                make_mock_competency("H-01", "fact", "Axiomas de Kolmogorov", session="Sesión 1", page=1),
                make_mock_competency("C-01", "concept", "Probabilidad Condicional", session="Sesión 1", page=2),
                make_mock_competency("Hab-01", "skill", "Cálculo de Bayes", session="Sesión 1", page=3),
            ],
        }
        (parts_dir / "cta_part_01.json").write_text(json.dumps(part1, indent=2), encoding="utf-8")

        # Section 2: temporary local IDs H-01, C-01, Hab-01
        part2 = {
            "section_index": 2,
            "competencies": [
                make_mock_competency("H-01", "fact", "Definición de Variable Aleatoria", session="Sesión 2", page=10),
                make_mock_competency("C-01", "concept", "Función de Distribución Acumulada", session="Sesión 2", page=11),
                make_mock_competency("Hab-01", "skill", "Cálculo de Esperanza Matemática", session="Sesión 2", page=12),
            ],
        }
        (parts_dir / "cta_part_02.json").write_text(json.dumps(part2, indent=2), encoding="utf-8")

        # Run merge
        draft = merge_cta_parts(work_dir)

        # Verify artifacts exist
        assert (work_dir / "cta_draft.json").exists()
        assert (work_dir / "cta_outline.json").exists()
        assert (work_dir / "cta_order.json").exists()
        assert (work_dir / "id_map.json").exists()
        assert (work_dir / "duplicate_candidates.json").exists()

        # Verify canonical renumbering
        comps = draft["competencies"]
        assert len(comps) == 6
        expected_ids = ["H-01", "C-01", "Hab-01", "H-02", "C-02", "Hab-02"]
        assert [c["id"] for c in comps] == expected_ids

        # Verify distractor IDs are renumbered to match new canonical prefixes
        for c in comps:
            prefix = c["id"].replace("-", "")
            for d in c["distractors"]:
                assert d["id"].startswith(f"D-{prefix}-")

        # Verify compact outline structure
        outline = json.loads((work_dir / "cta_outline.json").read_text(encoding="utf-8"))
        assert len(outline["competencies"]) == 6
        for oc in outline["competencies"]:
            assert "description_latex" not in oc  # Compact: no long text
            assert "distractor_names" in oc
            assert "distractor_ids" in oc

        # Verify cta_order.json
        order_data = json.loads((work_dir / "cta_order.json").read_text(encoding="utf-8"))
        assert order_data["order"] == expected_ids
        assert len(order_data["order_hash"]) == 64

    def test_find_duplicate_candidates_lexical_and_shared_evidence(self):
        c1 = make_mock_competency(
            "C-01", "concept", "Propiedad de Insesgadez del Estimador OLS",
            desc="Demostrar que el valor esperado del estimador coincide con el parámetro poblacional",
            doc="lec01.pdf", page=5
        )
        # c2 has high lexical Jaccard overlap (> 0.6) with c1
        c2 = make_mock_competency(
            "C-02", "concept", "Insesgadez del Estimador OLS en Muestras Grandes",
            desc="Demostrar que el valor esperado del estimador coincide con el verdadero parámetro poblacional",
            doc="lec02.pdf", page=8
        )
        # c3 has shared evidence with c1 (same doc and page) and name overlap
        c3 = make_mock_competency(
            "C-03", "concept", "Estimador OLS Insesgado",
            desc="Resumen breve",
            doc="lec01.pdf", page=5
        )
        # c4 is completely different
        c4 = make_mock_competency(
            "C-04", "concept", "Heterocedasticidad y Test de Breusch-Pagan",
            desc="Varianza de los errores no constante",
            doc="lec03.pdf", page=20
        )

        candidates = find_duplicate_candidates([c1, c2, c3, c4])

        candidate_pairs = [tuple(sorted(cand["pair"])) for cand in candidates]
        assert tuple(sorted(["C-01", "C-02"])) in candidate_pairs
        assert tuple(sorted(["C-01", "C-03"])) in candidate_pairs
        assert tuple(sorted(["C-01", "C-04"])) not in candidate_pairs


class TestCTAHarmonizer:
    """Test suite for apply_harmonize operations, validations, and rejection gates."""

    @pytest.fixture
    def setup_work_env(self, tmp_path: Path):
        work_dir = tmp_path / "work"
        work_dir.mkdir(parents=True)

        c1 = make_mock_competency("H-01", "fact", "Hecho 1", session="Sesión 1", page=1)
        c2 = make_mock_competency("C-01", "concept", "Concepto 1", session="Sesión 1", page=2)
        c3 = make_mock_competency("C-02", "concept", "Concepto 1 Duplicado", session="Sesión 2", page=2)
        c4 = make_mock_competency("Hab-01", "skill", "Habilidad 1", session="Sesión 2", page=4)

        competencies = [c1, c2, c3, c4]
        order_list = [c["id"] for c in competencies]

        draft_data = {
            "course_id": "test_course",
            "title": "Harmonizer Test Course",
            "macro_competency": "Test Macro",
            "competencies": competencies,
        }
        order_data = {"order": order_list, "order_hash": "hash123"}
        candidates_data = [
            {
                "pair": ["C-01", "C-02"],
                "type": "concept",
                "signals": ["shared_evidence"],
            }
        ]

        (work_dir / "cta_draft.json").write_text(json.dumps(draft_data, indent=2), encoding="utf-8")
        (work_dir / "cta_order.json").write_text(json.dumps(order_data, indent=2), encoding="utf-8")
        (work_dir / "duplicate_candidates.json").write_text(json.dumps(candidates_data, indent=2), encoding="utf-8")

        return work_dir

    def test_apply_harmonize_valid_add_prerequisites_backward_only(self, setup_work_env: Path):
        work_dir = setup_work_env
        harmonize_data = {
            "add_prerequisites": [
                {"competency": "Hab-01", "requires": ["C-01", "H-01"]}
            ]
        }
        (work_dir / "cta_harmonize.json").write_text(json.dumps(harmonize_data, indent=2), encoding="utf-8")

        result = apply_harmonize(work_dir)
        hab01 = next(c for c in result["competencies"] if c["id"] == "Hab-01")
        assert "C-01" in hab01["prerequisites"]
        assert "H-01" in hab01["prerequisites"]
        assert (work_dir / "cta.json").exists()
        assert (work_dir / "cta.md").exists()
        assert (work_dir / "merge_report.json").exists()

    def test_apply_harmonize_rejects_forward_prerequisites(self, setup_work_env: Path):
        work_dir = setup_work_env
        # H-01 (index 0) cannot depend forward on Hab-01 (index 3)
        harmonize_data = {
            "add_prerequisites": [
                {"competency": "H-01", "requires": ["Hab-01"]}
            ]
        }
        (work_dir / "cta_harmonize.json").write_text(json.dumps(harmonize_data, indent=2), encoding="utf-8")

        with pytest.raises(ValueError, match="Backward-only violation"):
            apply_harmonize(work_dir)

    def test_apply_harmonize_rejects_cycles(self, setup_work_env: Path):
        work_dir = setup_work_env
        # If C-01 already required Hab-01 (or vice versa), self or circular dependency
        harmonize_data = {
            "add_prerequisites": [
                {"competency": "C-01", "requires": ["C-01"]}
            ]
        }
        (work_dir / "cta_harmonize.json").write_text(json.dumps(harmonize_data, indent=2), encoding="utf-8")

        with pytest.raises(ValueError, match="Backward-only violation"):
            apply_harmonize(work_dir)

    def test_apply_harmonize_merge_valid_candidate(self, setup_work_env: Path):
        work_dir = setup_work_env
        harmonize_data = {
            "merges": [
                {
                    "pair": ["C-01", "C-02"],
                    "decision": "merge",
                    "reason": "Duplicate concept across sessions",
                }
            ]
        }
        (work_dir / "cta_harmonize.json").write_text(json.dumps(harmonize_data, indent=2), encoding="utf-8")

        result = apply_harmonize(work_dir)
        remaining_ids = [c["id"] for c in result["competencies"]]
        assert "C-01" in remaining_ids
        assert "C-02" not in remaining_ids  # C-02 was absorbed

        # C-01 survived and unifies distractors
        c01 = next(c for c in result["competencies"] if c["id"] == "C-01")
        assert len(c01["distractors"]) >= 3

        report = json.loads((work_dir / "merge_report.json").read_text(encoding="utf-8"))
        merge_decisions = [d for d in report["decisions"] if d.get("operation") == "merge"]
        assert len(merge_decisions) == 1
        assert merge_decisions[0]["survivor"] == "C-01"
        assert merge_decisions[0]["absorbed"] == "C-02"

    def test_apply_harmonize_rejects_merge_on_non_candidate(self, setup_work_env: Path):
        work_dir = setup_work_env
        # Pair ["H-01", "Hab-01"] is NOT in duplicate_candidates.json
        harmonize_data = {
            "merges": [
                {
                    "pair": ["H-01", "Hab-01"],
                    "decision": "merge",
                    "reason": "Invalid merge attempt",
                }
            ]
        }
        (work_dir / "cta_harmonize.json").write_text(json.dumps(harmonize_data, indent=2), encoding="utf-8")

        with pytest.raises(ValueError, match="REJECTED: Merge attempted on pair"):
            apply_harmonize(work_dir)

    def test_apply_harmonize_no_merge_flag_bypasses_merge(self, setup_work_env: Path):
        work_dir = setup_work_env
        harmonize_data = {
            "merges": [
                {
                    "pair": ["C-01", "C-02"],
                    "decision": "merge",
                    "reason": "Should be ignored when no_merge=True",
                }
            ]
        }
        (work_dir / "cta_harmonize.json").write_text(json.dumps(harmonize_data, indent=2), encoding="utf-8")

        result = apply_harmonize(work_dir, no_merge=True)
        remaining_ids = [c["id"] for c in result["competencies"]]
        assert "C-01" in remaining_ids
        assert "C-02" in remaining_ids  # Both kept

    def test_apply_harmonize_rejects_dropping_distractors_below_quota(self, setup_work_env: Path):
        work_dir = setup_work_env
        # C-01 has 3 distractors. Dropping 1 leaves 2, which violates minimum quota 3.
        harmonize_data = {
            "drop_duplicate_distractors": [
                {"competency": "C-01", "distractor_ids": ["D-C01-01"]}
            ]
        }
        (work_dir / "cta_harmonize.json").write_text(json.dumps(harmonize_data, indent=2), encoding="utf-8")

        with pytest.raises(ValueError, match="Quota violation"):
            apply_harmonize(work_dir)

    def test_apply_harmonize_rename_success(self, setup_work_env: Path):
        work_dir = setup_work_env
        harmonize_data = {
            "rename": [
                {"competency": "C-01", "name": "Refined Concept Name"}
            ]
        }
        (work_dir / "cta_harmonize.json").write_text(json.dumps(harmonize_data, indent=2), encoding="utf-8")

        result = apply_harmonize(work_dir)
        c01 = next(c for c in result["competencies"] if c["id"] == "C-01")
        assert c01["name"] == "Refined Concept Name"


class TestMarkdownRenderingAndSectionalCheck:
    """Test suite for deterministic markdown generation and check_cta_part CLI."""

    def test_render_cta_md_deterministic_and_complete(self):
        comp = make_mock_competency("Hab-01", "skill", "Estimador MCO", session="Sesión 1", page=3)
        cta_data = {
            "course_id": "stats_adv",
            "title": "Advanced Econometrics",
            "macro_competency": "Econometric Modeling",
            "competencies": [comp],
        }

        md_output = render_cta_md(cta_data)
        assert "# Cognitive Task Analysis (CTA): Advanced Econometrics" in md_output
        assert "`Hab-01`" in md_output
        assert "Estimador MCO" in md_output
        assert "Fused Distractor Models (6)" in md_output
        assert "D-Hab01-01" in md_output

    def test_check_cta_part_validation_and_cli(self, tmp_path: Path):
        # 1. Valid sectional part
        valid_comp = make_mock_competency("Hab-01", "skill", "Cálculo Integral", session="Sesión 1", page=1)
        part_data = {"section_index": 1, "competencies": [valid_comp]}
        is_valid, errors = check_cta_part(part_data)
        assert is_valid
        assert errors == []

        # 2. Invalid sectional part: Skill with only 2 distractors (minimum 6 required)
        invalid_comp = dict(valid_comp)
        invalid_comp["distractors"] = valid_comp["distractors"][:2]
        is_valid_bad, errors_bad = check_cta_part({"competencies": [invalid_comp]})
        assert not is_valid_bad
        assert any("CTA-D1 violation" in e for e in errors_bad)

        # 3. CLI execution via python subprocess
        part_file = tmp_path / "cta_part_01.json"
        part_file.write_text(json.dumps(part_data, indent=2), encoding="utf-8")

        check_script = Path(__file__).parent.parent / ".agents" / "skills" / "content-to-course" / "check_cta.py"
        res = subprocess.run(
            [sys.executable, str(check_script), str(part_file), "--part"],
            capture_output=True,
            text=True,
        )
        assert res.returncode == 0
        assert "PASS: cta_part satisfies local schema" in res.stdout

    def test_apply_harmonize_rejects_altered_pedagogical_order(self, tmp_path: Path):
        work_dir = tmp_path / "work"
        work_dir.mkdir(parents=True)

        c1 = make_mock_competency("H-01", "fact", "Fact 1", session="Sesión 1", page=1)
        c2 = make_mock_competency("C-01", "concept", "Concept 1", session="Sesión 1", page=2)

        # Original order was H-01 then C-01
        order_data = {"order": ["H-01", "C-01"], "order_hash": "hash"}
        # But draft was tampered/reversed to C-01 then H-01
        draft_data = {
            "course_id": "test",
            "title": "Test",
            "macro_competency": "Test",
            "competencies": [c2, c1],
        }

        (work_dir / "cta_draft.json").write_text(json.dumps(draft_data, indent=2), encoding="utf-8")
        (work_dir / "cta_order.json").write_text(json.dumps(order_data, indent=2), encoding="utf-8")
        (work_dir / "duplicate_candidates.json").write_text("[]", encoding="utf-8")
        (work_dir / "cta_harmonize.json").write_text("{}", encoding="utf-8")

        with pytest.raises(ValueError, match="Pedagogical order violation"):
            apply_harmonize(work_dir)

    def test_apply_harmonize_skill_omitted_step_quota(self, tmp_path: Path):
        work_dir = tmp_path / "work"
        work_dir.mkdir(parents=True)

        c_skill = make_mock_competency("Hab-01", "skill", "Skill 1", session="Sesión 1", page=1)
        # c_skill has 6 distractors: D-Hab01-01 to 04 (wrong_belief), D-Hab01-05 and 06 (omitted_step)
        order_data = {"order": ["Hab-01"], "order_hash": "hash"}
        draft_data = {
            "course_id": "test",
            "title": "Test",
            "macro_competency": "Test",
            "competencies": [c_skill],
        }

        (work_dir / "cta_draft.json").write_text(json.dumps(draft_data, indent=2), encoding="utf-8")
        (work_dir / "cta_order.json").write_text(json.dumps(order_data, indent=2), encoding="utf-8")
        (work_dir / "duplicate_candidates.json").write_text("[]", encoding="utf-8")

        # Attempt to drop D-Hab01-05 (leaving only 1 omitted_step distractor)
        harmonize_data = {
            "drop_duplicate_distractors": [
                {"competency": "Hab-01", "distractor_ids": ["D-Hab01-05"]}
            ]
        }
        (work_dir / "cta_harmonize.json").write_text(json.dumps(harmonize_data, indent=2), encoding="utf-8")

        with pytest.raises(ValueError, match="Quota violation"):
            apply_harmonize(work_dir)

    def test_cta_merge_and_apply_cli(self, tmp_path: Path):
        work_dir = tmp_path / "work"
        parts_dir = work_dir / "cta_parts"
        parts_dir.mkdir(parents=True)

        part = {
            "course_id": "cli_course",
            "title": "CLI Test Course",
            "section_index": 1,
            "competencies": [
                make_mock_competency("H-01", "fact", "CLI Fact", session="Sesión 1", page=1),
                make_mock_competency("C-01", "concept", "CLI Concept", session="Sesión 1", page=2),
            ],
        }
        (parts_dir / "cta_part_01.json").write_text(json.dumps(part, indent=2), encoding="utf-8")

        merge_script = Path(__file__).parent.parent / ".agents" / "skills" / "content-to-course" / "cta_merge.py"

        # 1. Run merge CLI
        res_merge = subprocess.run(
            [sys.executable, str(merge_script), "merge", "--work-dir", str(work_dir)],
            capture_output=True,
            text=True,
        )
        assert res_merge.returncode == 0
        assert "SUCCESS: Sectional parts merged" in res_merge.stdout
        assert (work_dir / "cta_draft.json").exists()

        # Write empty harmonization
        (work_dir / "cta_harmonize.json").write_text("{}", encoding="utf-8")

        # 2. Run apply CLI
        res_apply = subprocess.run(
            [sys.executable, str(merge_script), "apply", "--work-dir", str(work_dir)],
            capture_output=True,
            text=True,
        )
        assert res_apply.returncode == 0
        assert "SUCCESS: Harmonization applied" in res_apply.stdout
        assert (work_dir / "cta.json").exists()
        assert (work_dir / "cta.md").exists()
