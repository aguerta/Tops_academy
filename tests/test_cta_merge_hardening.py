"""Hardening tests for cta_merge: proportional outline budget, distractor semantic dedup + round-robin cap, and cross-PDF formula boost."""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

SKILL_DIR = Path(__file__).resolve().parents[1] / ".agents" / "skills" / "content-to-course"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from cta_merge import (  # noqa: E402
    MAX_DISTRACTORS_PER_COMPETENCY,
    _build_outline_payload,
    _token_jaccard,
    apply_harmonize,
    find_duplicate_candidates,
)


def _make_distractor(
    did: str,
    name: str,
    wrong_belief: str = None,
    omitted_step: str = None,
    doc: str = "a.pdf",
    page: int = 1,
) -> Dict[str, Any]:
    return {
        "id": did,
        "name": name,
        "wrong_belief": wrong_belief,
        "correct_belief": "Razonamiento matemático correcto",
        "omitted_step": omitted_step,
        "trigger": "Durante la resolución",
        "manifestation": "Resultado incorrecto",
        "error_type": "conceptual_swap",
        "severity": "medium",
        "origin": "source",
        "evidence": {"doc": doc, "page": page},
        "remediation_hint": "Verifica cuidadosamente cada hipótesis y paso algebraico antes de concluir.",
    }


def _make_comp(
    cid: str,
    ctype: str = "concept",
    name: str = "Concepto",
    desc: str = "Explicación matemática detallada.",
    doc: str = "doc1.pdf",
    page: int = 1,
    distractors: List[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    return {
        "id": cid,
        "type": ctype,
        "name": name,
        "description_latex": desc,
        "bloom": "Apply" if ctype == "skill" else "Understand",
        "session": "Sesión 1",
        "unit_index": 1,
        "evidence": [{"doc": doc, "page": page}],
        "prerequisites": [],
        "distractors": distractors or [],
        "assumptions": [],
    }


def test_outline_budget_proportional_scaling():
    """_build_outline_payload computes recommended_min and recommended_max proportionally with floors/caps."""
    small = _build_outline_payload(
        "c_small",
        "Small",
        "Macro",
        [_make_comp(f"C-{i:02d}", name=f"Comp {i}") for i in range(1, 11)],
    )
    b_small = small["target_competency_budget"]
    assert b_small["draft_count"] == 10
    assert b_small["recommended_min"] == 14
    assert b_small["recommended_max"] == 24
    assert b_small["consolidation_needed"] is False

    medium = _build_outline_payload(
        "c_med",
        "Medium",
        "Macro",
        [_make_comp(f"C-{i:02d}", name=f"Comp {i}") for i in range(1, 41)],
    )
    b_med = medium["target_competency_budget"]
    assert b_med["draft_count"] == 40
    assert b_med["recommended_min"] == 20
    assert b_med["recommended_max"] == 27
    assert b_med["consolidation_needed"] is True

    large = _build_outline_payload(
        "c_large",
        "Large",
        "Macro",
        [_make_comp(f"C-{i:02d}", name=f"Comp {i}") for i in range(1, 61)],
    )
    b_large = large["target_competency_budget"]
    assert b_large["draft_count"] == 60
    assert b_large["recommended_min"] == 30
    assert b_large["recommended_max"] == 32
    assert b_large["consolidation_needed"] is True


def test_apply_harmonize_semantic_dedup_round_robin_and_cap(tmp_path: Path):
    """apply_harmonize deduplicates semantically similar distractors, preserves round-robin diversity, and caps at 10."""
    # Direct _token_jaccard check
    sim_high = _token_jaccard(
        "Confundir la varianza muestral con la varianza poblacional",
        "Confunde varianza muestral con varianza poblacional",
    )
    sim_low = _token_jaccard(
        "Olvidar dividir por n menos uno en la varianza muestral",
        "Aplicar teorema de Bayes sin verificar independencia",
    )
    assert sim_high >= 0.55
    assert sim_low < 0.55

    work_dir = tmp_path / "work_dedup"
    work_dir.mkdir(parents=True)

    c1_distractors = [
        _make_distractor("D-C01-01", "C1-1", wrong_belief="Confundir la varianza muestral con la varianza poblacional"),
        _make_distractor("D-C01-02", "C1-2", wrong_belief="Asumir normalidad cuando el tamaño muestral es pequeño"),
        _make_distractor("D-C01-03", "C1-3", wrong_belief="Ignorar la dependencia temporal entre observaciones consecutivas"),
        _make_distractor("D-C01-04", "C1-4", wrong_belief="Usar covarianza nula como sinónimo de independencia"),
        _make_distractor("D-C01-05", "C1-5", wrong_belief="Aplicar límite central sin varianza finita"),
        _make_distractor("D-C01-06", "C1-6", wrong_belief="Confundir probabilidad condicional con probabilidad conjunta"),
    ]
    c2_distractors = [
        # Semantic duplicate of C1-1
        _make_distractor("D-C02-01", "C2-dup", wrong_belief="Confunde varianza muestral con varianza poblacional"),
        _make_distractor("D-C02-02", "C2-2", wrong_belief="Dividir por n en lugar de n menos uno al estimar sigma cuadrado"),
        _make_distractor("D-C02-03", "C2-3", wrong_belief="Omitir el jacobiano al transformar variables aleatorias continuas"),
        _make_distractor("D-C02-04", "C2-4", wrong_belief="Intercambiar hipótesis nula y alternativa en el contraste"),
        _make_distractor("D-C02-05", "C2-5", wrong_belief="Interpretar el p valor como probabilidad de hipótesis nula"),
    ]
    c3_distractors = [
        _make_distractor("D-C03-01", "C3-1", wrong_belief="Evaluar verosimilitud sin tomar logaritmo antes de derivar"),
        _make_distractor("D-C03-02", "C3-2", wrong_belief="Descartar puntos frontera del espacio paramétrico al maximizar"),
        _make_distractor("D-C03-03", "C3-3", wrong_belief="Confundir intervalo de confianza con intervalo de predicción"),
        _make_distractor("D-C03-04", "C3-4", wrong_belief="Aplicar desigualdad de Markov a variables con valores negativos"),
    ]

    c1 = _make_comp("C-01", "concept", "Inferencia I", doc="a.pdf", page=1, distractors=c1_distractors)
    c2 = _make_comp("C-02", "concept", "Inferencia II", doc="b.pdf", page=2, distractors=c2_distractors)
    c3 = _make_comp("C-03", "concept", "Inferencia III", doc="c.pdf", page=3, distractors=c3_distractors)

    draft = {
        "course_id": "dedup_course",
        "title": "Dedup Course",
        "macro_competency": "Mastery",
        "competencies": [c1, c2, c3],
    }
    (work_dir / "cta_draft.json").write_text(json.dumps(draft), encoding="utf-8")
    (work_dir / "cta_order.json").write_text(json.dumps({"order": ["C-01", "C-02", "C-03"]}), encoding="utf-8")
    (work_dir / "duplicate_candidates.json").write_text(json.dumps([]), encoding="utf-8")
    (work_dir / "pre_cta_manifest.json").write_text(
        json.dumps({
            "course_id": "dedup_course",
            "files": [
                {"doc": "a.pdf", "total_pages": 10, "valid_page_range": [1, 10]},
                {"doc": "b.pdf", "total_pages": 10, "valid_page_range": [1, 10]},
                {"doc": "c.pdf", "total_pages": 10, "valid_page_range": [1, 10]},
            ],
        }),
        encoding="utf-8",
    )
    harmonize = {
        "merges": [
            {"keep_id": "C-01", "drop_id": "C-02", "decision": "merge", "reason": "Overlap"},
            {"keep_id": "C-01", "drop_id": "C-03", "decision": "merge", "reason": "Overlap"},
        ]
    }
    (work_dir / "cta_harmonize.json").write_text(json.dumps(harmonize), encoding="utf-8")

    final_cta = apply_harmonize(work_dir)
    assert len(final_cta["competencies"]) == 1
    survivor = final_cta["competencies"][0]
    kept = survivor["distractors"]

    assert MAX_DISTRACTORS_PER_COMPETENCY == 10
    assert len(kept) == 10

    kept_names = [d["name"] for d in kept]
    # Semantic duplicate from C-02 must be dropped
    assert "C2-dup" not in kept_names
    # Round-robin diversity: distractors from all 3 competencies must be present
    assert any(n.startswith("C1-") for n in kept_names)
    assert any(n.startswith("C2-") for n in kept_names)
    assert any(n.startswith("C3-") for n in kept_names)
    # Unique IDs
    kept_ids = [d["id"] for d in kept]
    assert len(kept_ids) == len(set(kept_ids))


def test_cross_pdf_formula_terms_boost_and_cap():
    """Cross-PDF pairs sharing formula key terms in key_concepts/distractors get +0.20 boost (capped at 1.0)."""
    base_c1 = {
        "id": "C-01",
        "type": "concept",
        "name": "Cota de probabilidad para variables aleatorias",
        "description_latex": r"Acota la cola de una distribución usando $E[X]$.",
        "source_ref": "teoria_tema2.pdf#page=4",
    }
    base_c2 = {
        "id": "C-02",
        "type": "concept",
        "name": "Cota de probabilidad de variables aleatorias",
        "description_latex": r"Acota la cola de una distribución usando $E[X]$.",
        "source_ref": "ejercicios_tema2.pdf#page=7",
    }

    cands_without = find_duplicate_candidates([base_c1, base_c2])
    assert len(cands_without) == 1
    score_without = cands_without[0]["score"]
    assert "shared_formula_terms" not in cands_without[0]["signals"]

    boosted_c1 = {
        **base_c1,
        "key_concepts": ["Desigualdad de Chebyshev", "Error estándar"],
        "distractors": [{"name": "Confundir Markov con Chebyshev", "wrong_belief": "Aplicar Markov a variables negativas"}],
    }
    boosted_c2 = {
        **base_c2,
        "key_concepts": ["Desigualdad de Markov", "Error estandar"],
        "distractors": [{"name": "Olvidar no negatividad en Chebyshev", "wrong_belief": "Usar cota sin varianza finita"}],
    }

    cands_with = find_duplicate_candidates([boosted_c1, boosted_c2])
    assert len(cands_with) == 1
    cand = cands_with[0]
    assert "shared_formula_terms" in cand["signals"]
    assert cand["score"] == round(min(1.0, score_without + 0.20), 4)
    assert cand["score"] <= 1.0

    # Same source_ref PDF must NOT receive the cross-PDF formula boost
    same_pdf_c2 = {**boosted_c2, "source_ref": "teoria_tema2.pdf#page=9"}
    cands_same_pdf = find_duplicate_candidates([boosted_c1, same_pdf_c2])
    assert len(cands_same_pdf) == 1
    assert "shared_formula_terms" not in cands_same_pdf[0]["signals"]


def test_outline_budget_never_inverts_for_large_drafts():
    """For large drafts (e.g. draft=66), recommended_min must never exceed recommended_max."""
    huge = _build_outline_payload(
        "c_huge",
        "Huge",
        "Macro",
        [_make_comp(f"C-{i:02d}", name=f"Comp {i}") for i in range(1, 67)],
    )
    b = huge["target_competency_budget"]
    assert b["draft_count"] == 66
    assert b["recommended_max"] == 32
    assert b["recommended_min"] <= b["recommended_max"]
    assert b["recommended_min"] == 32


def test_duplicate_candidates_capped_keeps_mandatory_and_strong():
    from cta_merge import _cap_duplicate_candidates_for_harmonizer

    cands = (
        [{"pair": ["A", "B"], "mandatory": True, "strength": "weak", "score": 0.9}]
        + [{"pair": [f"S{i}", f"T{i}"], "mandatory": False, "strength": "strong", "score": 0.8} for i in range(10)]
        + [{"pair": [f"W{i}", f"Z{i}"], "mandatory": False, "strength": "weak", "score": 0.4} for i in range(120)]
    )
    capped = _cap_duplicate_candidates_for_harmonizer(cands, max_candidates=80)
    assert len(capped) == 80
    assert any(c.get("mandatory") for c in capped)
    assert sum(1 for c in capped if c.get("strength") == "strong") == 10


def test_apply_harmonize_enforces_cta_budget_exceeded(tmp_path: Path):
    """apply_harmonize raises [CTA-BUDGET-EXCEEDED] when draft > recommended_max, candidates exist, and final > ceil(max*1.15)."""
    import pytest

    work_dir = tmp_path / "work_budget"
    work_dir.mkdir(parents=True)
    comps = [
        _make_comp(
            f"C-{i:02d}",
            name=f"Tema Distinto {i}",
            distractors=[_make_distractor(f"D-C{i:02d}-{j}", f"Dist {i}-{j}") for j in range(1, 4)],
        )
        for i in range(1, 46)
    ]
    draft = {"course_id": "budget_test", "title": "Budget", "macro_competency": "M", "competencies": comps}
    (work_dir / "cta_draft.json").write_text(json.dumps(draft), encoding="utf-8")
    (work_dir / "cta_order.json").write_text(
        json.dumps({"order": [c["id"] for c in comps], "order_hash": "h"}), encoding="utf-8"
    )
    (work_dir / "duplicate_candidates.json").write_text(
        json.dumps([{"pair": ["C-01", "C-02"], "score": 0.7, "strength": "strong"}]), encoding="utf-8"
    )
    (work_dir / "cta_harmonize.json").write_text(
        json.dumps({"duplicate_decisions": [], "add_prerequisites": [], "rename": [], "drop_duplicate_distractors": []}),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match=r"CTA-BUDGET-EXCEEDED"):
        apply_harmonize(work_dir)
