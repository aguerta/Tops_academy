"""Tests for cross-PDF duplicate detection, canonical parts_order, outline budget, and Union-Find merges."""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

SKILL_DIR = Path(__file__).resolve().parents[1] / ".agents" / "skills" / "content-to-course"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from cta_merge import (  # noqa: E402
    _extract_math_tokens,
    apply_harmonize,
    find_duplicate_candidates,
    merge_cta_parts,
    prepare_harmonize_from_single_draft,
)


def _make_distractor(did: str, omitted_step: str = None, doc: str = "a.pdf", page: int = 1) -> Dict[str, Any]:
    return {
        "id": did,
        "name": f"Trap {did}",
        "wrong_belief": None if omitted_step else f"Wrong belief for {did}",
        "correct_belief": "Correct mathematical reasoning",
        "omitted_step": omitted_step,
        "trigger": "During problem solving",
        "manifestation": "Incorrect result",
        "error_type": "conceptual_swap",
        "severity": "medium",
        "origin": "source",
        "evidence": {"doc": doc, "page": page},
        "remediation_hint": "Verify every hypothesis and algebraic step carefully before proceeding with the final conclusion.",
    }


def _make_comp(
    cid: str,
    ctype: str = "concept",
    name: str = "Concept",
    desc: str = "Detailed mathematical explanation",
    doc: str = "doc1.pdf",
    page: int = 1,
    prerequisites: List[str] = None,
    assumptions: List[Dict[str, Any]] = None,
    is_prerequisite: bool = False,
) -> Dict[str, Any]:
    clean = cid.replace("-", "")
    if ctype == "skill":
        distractors = [
            _make_distractor(f"D-{clean}-01", doc=doc, page=page),
            _make_distractor(f"D-{clean}-02", doc=doc, page=page),
            _make_distractor(f"D-{clean}-03", doc=doc, page=page),
            _make_distractor(f"D-{clean}-04", doc=doc, page=page),
            _make_distractor(f"D-{clean}-05", omitted_step="Omitted step A", doc=doc, page=page),
            _make_distractor(f"D-{clean}-06", omitted_step="Omitted step B", doc=doc, page=page),
        ]
    else:
        distractors = [
            _make_distractor(f"D-{clean}-01", doc=doc, page=page),
            _make_distractor(f"D-{clean}-02", doc=doc, page=page),
            _make_distractor(f"D-{clean}-03", doc=doc, page=page),
        ]
    comp: Dict[str, Any] = {
        "id": cid,
        "type": ctype,
        "name": name,
        "description_latex": desc,
        "bloom": "Apply" if ctype == "skill" else "Understand",
        "session": "Sesión 1",
        "unit_index": 1,
        "evidence": [{"doc": doc, "page": page}],
        "prerequisites": prerequisites or [],
        "distractors": distractors,
        "assumptions": assumptions or [],
    }
    if is_prerequisite:
        comp["is_prerequisite"] = True
    return comp


def test_cross_pdf_math_tokens_and_fact_vs_concept_strong():
    """Cross-PDF pairs avoid -0.20 penalty, get cross_pdf_match, and fact vs concept can reach strong."""
    tokens = _extract_math_tokens(r"El estimador $\bar{X}_n \xrightarrow{p} \mu$ tiene $s_n^2$ y $ECM(\hat{\theta})$")
    assert r"\bar" in tokens
    assert r"\xrightarrow" in tokens
    assert "s_n^2" in tokens
    assert "ecm" in tokens

    comps = [
        {
            "id": "H-01",
            "type": "fact",
            "name": "Error cuadrático medio del estimador",
            "description_latex": r"Definido como $ECM(\hat{\theta}) = \text{Var}(\hat{\theta}) + B^2$ con $s_n^2$ y $\bar{X}_n$.",
            "evidence": [{"doc": "pdf_01.pdf", "page": 4}],
            "distractor_names": ["Confundir sesgo con varianza"],
        },
        {
            "id": "C-01",
            "type": "concept",
            "name": "Error cuadrático medio de un estimador",
            "description_latex": r"Descomposición $ECM(\hat{\theta}) = \text{Var}(\hat{\theta}) + B^2$ usando $s_n^2$ y $\bar{X}_n$.",
            "evidence": [{"doc": "pdf_02.pdf", "page": 11}],
            "distractor_names": ["Confundir sesgo con varianza"],
        },
    ]
    cands = find_duplicate_candidates(comps)
    assert len(cands) == 1
    cand = cands[0]
    assert cand["type"] == "fact_vs_concept"
    assert "cross_pdf_match" in cand["signals"]
    assert cand["score"] >= 0.60
    assert cand["strength"] == "strong"


def test_parts_order_preserved_when_part04_has_pre01(tmp_path: Path):
    """Canonical subpart order part_01..part_04 is preserved even if part_04 contains PRE-01."""
    work_dir = tmp_path / "work"
    parts_dir = work_dir / "cta_parts"
    parts_dir.mkdir(parents=True)

    manifest = {
        "course_id": "stats_test",
        "files": [{"file_index": 0, "doc": "notes.pdf", "doc_slug": "notes"}],
        "subparts": [
            {"subpart_index": 0, "subpart_id": "part_01", "file_index": 0},
            {"subpart_index": 1, "subpart_id": "part_02", "file_index": 0},
            {"subpart_index": 2, "subpart_id": "part_03", "file_index": 0},
            {"subpart_index": 3, "subpart_id": "part_04", "file_index": 0},
        ],
    }
    (work_dir / "pre_cta_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    (parts_dir / "part_01.json").write_text(
        json.dumps({"competencies": [_make_comp("C-01", "concept", "Alpha Part 1", page=1)]}),
        encoding="utf-8",
    )
    (parts_dir / "part_02.json").write_text(
        json.dumps({"competencies": [_make_comp("C-01", "concept", "Beta Part 2", page=5)]}),
        encoding="utf-8",
    )
    (parts_dir / "part_03.json").write_text(
        json.dumps({"competencies": [_make_comp("C-01", "concept", "Gamma Part 3", page=9)]}),
        encoding="utf-8",
    )
    (parts_dir / "part_04.json").write_text(
        json.dumps({
            "competencies": [
                _make_comp("PRE-01", "fact", "Prereq From Part 4", page=12, is_prerequisite=True),
                _make_comp("C-01", "concept", "Delta Part 4", page=13),
            ]
        }),
        encoding="utf-8",
    )

    result = merge_cta_parts(work_dir)
    names = [c["name"] for c in result["competencies"]]
    assert names[0] == "Prereq From Part 4"
    assert names[1:] == ["Alpha Part 1", "Beta Part 2", "Gamma Part 3", "Delta Part 4"]


def test_outline_contains_description_latex_assumptions_and_budget(tmp_path: Path):
    """cta_outline.json includes full description_latex, assumptions_count, and target_competency_budget."""
    work_dir = tmp_path / "work_outline"
    work_dir.mkdir(parents=True)

    draft = {
        "course_id": "econ_101",
        "title": "Econometrics",
        "macro_competency": "Mastery",
        "competencies": [
            _make_comp(
                "C-01",
                "concept",
                "Gauss-Markov",
                desc=r"Teorema completo con $\hat{\beta}_{MCO}$ y varianza mínima.",
                assumptions=[{"id": "A-C01-01", "statement_latex": "$E[u|X]=0$"}],
            )
        ],
    }
    (work_dir / "cta_draft.json").write_text(json.dumps(draft), encoding="utf-8")

    prepare_harmonize_from_single_draft(work_dir)
    outline = json.loads((work_dir / "cta_outline.json").read_text(encoding="utf-8"))

    assert "target_competency_budget" in outline
    budget = outline["target_competency_budget"]
    assert set(budget.keys()) >= {"recommended_min", "recommended_max", "draft_count", "consolidation_needed"}
    assert budget["draft_count"] == 1
    assert budget["consolidation_needed"] is False

    comp_out = outline["competencies"][0]
    assert comp_out["description_latex"] == r"Teorema completo con $\hat{\beta}_{MCO}$ y varianza mínima."
    assert comp_out["assumptions_count"] == 1


def test_union_find_transitive_merge_and_merged_type(tmp_path: Path):
    """Union-Find resolves A <- B and B <- C transitively, honors merged_type, and clears omitted_step."""
    work_dir = tmp_path / "work_uf"
    work_dir.mkdir(parents=True)

    c_a = _make_comp("H-01", "fact", "Estimador A", desc="Desc A", doc="a.pdf", page=1)
    c_b = _make_comp(
        "C-01",
        "concept",
        "Estimador B",
        desc="Desc B",
        doc="b.pdf",
        page=2,
        assumptions=[{
            "id": "A-C01-01",
            "statement_latex": "$n > 30$",
            "violation_consequence": "Asymptotic normality approximation fails.",
        }],
    )
    c_c = _make_comp("Hab-01", "skill", "Calcular Estimador C", desc="Desc C", doc="c.pdf", page=3, prerequisites=["C-01"])

    draft = {
        "course_id": "uf_course",
        "title": "UF Course",
        "macro_competency": "Mastery",
        "competencies": [c_a, c_b, c_c],
    }
    (work_dir / "cta_draft.json").write_text(json.dumps(draft), encoding="utf-8")
    (work_dir / "cta_order.json").write_text(
        json.dumps({"order": ["H-01", "C-01", "Hab-01"]}), encoding="utf-8"
    )
    (work_dir / "duplicate_candidates.json").write_text(json.dumps([]), encoding="utf-8")
    (work_dir / "pre_cta_manifest.json").write_text(
        json.dumps({
            "course_id": "uf_course",
            "files": [
                {"doc": "a.pdf", "total_pages": 10, "valid_page_range": [1, 10]},
                {"doc": "b.pdf", "total_pages": 10, "valid_page_range": [1, 10]},
                {"doc": "c.pdf", "total_pages": 10, "valid_page_range": [1, 10]},
            ],
        }),
        encoding="utf-8",
    )

    # Deliberately order H-01 <- C-01 before C-01 <- Hab-01 to verify Union-Find transitivity
    harmonize = {
        "merges": [
            {
                "keep_id": "H-01",
                "drop_id": "C-01",
                "decision": "merge",
                "reason": "Same estimator definition",
            },
            {
                "keep_id": "C-01",
                "drop_id": "Hab-01",
                "decision": "merge",
                "merged_type": "concept",
                "merged_name": "Estimador Unificado",
                "merged_description_latex": r"Descripción unificada con $\hat{\theta}$.",
                "reason": "Unified into concept",
            },
        ]
    }
    (work_dir / "cta_harmonize.json").write_text(json.dumps(harmonize), encoding="utf-8")

    final_cta = apply_harmonize(work_dir)
    comps = final_cta["competencies"]
    assert len(comps) == 1
    survivor = comps[0]
    assert survivor["id"] == "H-01"
    assert survivor["type"] == "concept"
    assert survivor["name"] == "Estimador Unificado"
    assert survivor["description_latex"] == r"Descripción unificada con $\hat{\theta}$."
    assert all(d.get("omitted_step") is None for d in survivor["distractors"])
