import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".agents" / "skills" / "content-to-course"))

from cta_merge import (  # noqa: E402
    find_duplicate_candidates,
    normalized_stems,
    trigram_dice,
)


def _c(cid, name, desc="", ev=None, dis=None, typ="concept"):
    return {
        "id": cid, "type": typ, "name": name, "description_latex": desc,
        "evidence": ev or [], "distractor_names": dis or [],
    }


def _pairs(cands):
    return {tuple(sorted(c["pair"])) for c in cands}


def test_normalization_accents_plurals_stopwords():
    assert normalized_stems("Cálculo de las derivadas") & normalized_stems("Calcular la derivada")
    assert trigram_dice("Regla de la cadena", "Regla de cadena") > 0.7


def test_reformulated_names_become_candidates():
    comps = [
        _c("C-01", "Interpretación geométrica de la derivada", "Pendiente de la recta tangente"),
        _c("C-02", "Interpretar geométricamente derivadas", "Tangente y su pendiente en un punto"),
        _c("C-03", "Teorema fundamental del cálculo", "Relaciona integral y derivada"),
    ]
    pairs = _pairs(find_duplicate_candidates(comps))
    assert ("C-01", "C-02") in pairs
    assert ("C-01", "C-03") not in pairs


def test_strong_shared_evidence_without_name_overlap():
    ev = [{"doc": "a.pdf", "page": 3}, {"doc": "a.pdf", "page": 4}]
    comps = [_c("C-01", "Alfa beta", ev=ev), _c("C-02", "Gamma delta", ev=ev)]
    cands = find_duplicate_candidates(comps)
    assert cands and "strong_shared_evidence" in cands[0]["signals"]


def test_shared_distractors_signal():
    dis = ["Confundir pendiente con ordenada", "Usar el signo opuesto"]
    comps = [_c("C-01", "Alfa", dis=dis), _c("C-02", "Omega", dis=dis)]
    cands = find_duplicate_candidates(comps)
    assert cands and "shared_distractors" in cands[0]["signals"]


def test_candidates_have_score_strength_and_truncated_descriptions_sorted_strong_first():
    long_desc = "palabra " * 100
    comps = [
        _c("C-01", "Regla de la cadena", long_desc),
        _c("C-02", "Regla de la cadena", long_desc),
        _c("C-03", "Regla del producto cadena"),
    ]
    cands = find_duplicate_candidates(comps)
    assert cands[0]["strength"] == "strong"
    assert len(cands[0]["c1_description"]) <= 120
    assert all({"score", "strength"} <= set(c) for c in cands)
    scores = [c["score"] for c in cands if c["strength"] == "strong"]
    assert scores == sorted(scores, reverse=True)


def test_unrelated_competencies_not_flagged():
    comps = [_c("C-01", "Límites laterales", "Definición epsilon-delta"),
             _c("C-02", "Distribución normal", "Media y desviación estándar")]
    assert find_duplicate_candidates(comps) == []


def test_delta_vs_base_keeps_base_fields():
    base = [{"id": "C-01", "name": "Regla de la cadena", "type": "concept"}]
    new = [_c("C-09", "Regla de cadena", typ="concept")]
    cands = find_duplicate_candidates(new, existing_competencies=base)
    assert cands and cands[0]["against_base"] and cands[0]["base_id"] == "C-01" and cands[0]["delta_id"] == "C-09"
