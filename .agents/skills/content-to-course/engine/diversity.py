"""Stem diversity evaluation for content-to-course v2.

Calculates unique(masked_stems) / total >= 0.5 per competency to prevent
repetitive stems that only differ by numerical substitution.
"""

import re
from collections import Counter, defaultdict
from typing import Any, Dict, List, Tuple


NUM_LITERAL_RE = re.compile(r"\b\d+(?:\.\d+)?\b")

# Rotating generic taxonomic prefixes used to mask static rationale recycling
SYNTHETIC_RATIONALE_PREFIX_PAT = re.compile(
    r"^\s*(?:Error\s+(?:conceptual|de\s+c[aá]lculo|algebraico|metodol[oó]gico|operativo)|"
    r"Confusi[oó]n\s+(?:te[oó]rica|metodol[oó]gica|conceptual|de\s+conceptos?)|"
    r"Fallo\s+(?:de\s+c[aá]lculo|conceptual|anal[ií]tico|algebraico)|"
    r"Desv[ií]o\s+(?:algebraico|de\s+operador|anal[ií]tico|num[eé]rico)|"
    r"Aplicaci[oó]n\s+incorrecta|Sustituci[oó]n\s+inv[aá]lida|"
    r"Desliz\s+anal[ií]tico|Descuido\s+algebraico|Falta\s+de\s+ponderaci[oó]n|"
    r"Interpretaci[oó]n\s+err[oó]nea|Omisi[oó]n\s+de\s+regla|Inversi[oó]n\s+de\s+f[oó]rmula)\s*:\s*",
    re.IGNORECASE,
)



def mask_stem_numbers(stem: str) -> str:
    """Mask numeric quantities, fractions, and matrices to isolate structural syntax."""
    # 1. Normalize whitespace
    text = re.sub(r"\s+", " ", stem.strip())

    # 2. Mask bmatrix and table arrays
    text = re.sub(r"\\begin\{bmatrix\}.*?\\end\{bmatrix\}", "[BMATRIX]", text)
    text = re.sub(r"\\begin\{array\}\{.*?\}.*?\\end\{array\}", "[ARRAY]", text)

    # 3. Mask LaTeX fractions (supporting 1-level nested braces such as \frac{x^{2}}{3})
    text = re.sub(
        r"\\frac\{(?:[^{}]|\{[^{}]*\})+\}\{(?:[^{}]|\{[^{}]*\})+\}",
        "[FRAC]",
        text,
    )

    # 4. Mask numeric literals (integers, floats, scientific notation) including variable coefficients (e.g. 2x, 3.5y)
    text = re.sub(r"(?<![A-Za-z_])\d+(?:\.\d+)?(?:[eE][+-]?\d+)?(?=[A-Za-z\\]|\b)", "[NUM]", text)

    # 5. Mask numbers adjacent to LaTeX math symbols
    text = re.sub(r"(?<=[=\+\-\*\/\^])\s*\d+", " [NUM]", text)

    return text


def evaluate_competency_diversity(
    stems: List[str],
    min_diversity_ratio: float = 0.5,
) -> Dict[str, Any]:
    """Calculate stem structural diversity ratio for a competency.
    
    Returns:
        {
            "total": int,
            "unique_masked": int,
            "diversity_ratio": float,
            "passes": bool,
            "sample_masked": list of strings
        }
    """
    if not stems:
        return {
            "total": 0,
            "unique_masked": 0,
            "diversity_ratio": 0.0,
            "passes": False,
            "sample_masked": [],
        }

    masked_stems = [mask_stem_numbers(s) for s in stems]
    unique_masked = len(set(masked_stems))
    total = len(stems)
    ratio = unique_masked / total if total > 0 else 0.0
    passes = ratio >= min_diversity_ratio

    return {
        "total": total,
        "unique_masked": unique_masked,
        "diversity_ratio": round(ratio, 4),
        "passes": bool(passes),
        "sample_masked": list(set(masked_stems))[:5],
    }


def evaluate_slot_rationale_diversity(questions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Evaluate slot-based distractor error_rationale diversity across questions.

    Groups normalized rationales (after stripping rotating synthetic prefixes and
    masking numeric literals) by `(competency_id, slot_id)` where `slot_id` is
    `distractor_id` when present, or a template/question+option fallback key.
    """
    slot_texts: Dict[Tuple[str, str], List[str]] = defaultdict(list)
    raw_slot_texts: Dict[Tuple[str, str], List[str]] = defaultdict(list)
    all_norm_rats: List[str] = []
    all_raw_masked_rats: List[str] = []
    synthetic_prefix_cnt = 0

    for q in questions or []:
        if not isinstance(q, dict):
            continue
        cid = str(q.get("competency_id") or "unassigned").strip() or "unassigned"
        options = q.get("options", []) or []
        if not isinstance(options, list):
            continue
        for idx, o in enumerate(options):
            if not isinstance(o, dict) or o.get("is_correct"):
                continue
            rat = str(o.get("error_rationale") or "").strip()
            if not rat:
                continue
            if SYNTHETIC_RATIONALE_PREFIX_PAT.match(rat):
                synthetic_prefix_cnt += 1
            stripped_rat = SYNTHETIC_RATIONALE_PREFIX_PAT.sub("", rat).strip()
            norm_rat = NUM_LITERAL_RE.sub("<NUM>", stripped_rat).lower()
            raw_masked = NUM_LITERAL_RE.sub("<NUM>", rat)

            all_norm_rats.append(norm_rat)
            all_raw_masked_rats.append(raw_masked)

            did = str(o.get("distractor_id") or "").strip()
            if did:
                slot_id = did
            else:
                slot_id = f"{q.get('template_id') or q.get('id', 'q')}::{o.get('id') or o.get('option_id') or idx}"

            slot_texts[(cid, slot_id)].append(norm_rat)
            raw_slot_texts[(cid, slot_id)].append(raw_masked.lower())

    by_cid: Dict[str, List[Tuple[str, str]]] = defaultdict(list)
    raw_by_cid: Dict[str, List[Tuple[str, str]]] = defaultdict(list)
    for (cid, slot_id), txts in slot_texts.items():
        cnt = Counter(txts)
        canonical = min(cnt.items(), key=lambda kv: (-kv[1], kv[0]))[0]
        by_cid[cid].append((slot_id, canonical))
    for (cid, slot_id), r_txts in raw_slot_texts.items():
        r_cnt = Counter(r_txts)
        raw_canonical = min(r_cnt.items(), key=lambda kv: (-kv[1], kv[0]))[0]
        raw_by_cid[cid].append((slot_id, raw_canonical))

    total_slots = sum(len(s) for s in by_cid.values())
    all_slot_canonicals = [ct for s in by_cid.values() for _, ct in s]
    all_raw_slot_canonicals = [ct for s in raw_by_cid.values() for _, ct in s]
    global_cnt = Counter(all_slot_canonicals)

    unique_slots_per_cid = sum(len(set(ct for _, ct in s)) for s in by_cid.values())
    global_unique_slots = len(global_cnt)
    unique_slots = min(unique_slots_per_cid, global_unique_slots)
    raw_unique_slots = len(set(all_raw_slot_canonicals))

    total_colliding_slots = 0
    duplicated_slots_by_competency: Dict[str, List[Tuple[str, str]]] = {}

    for cid, slots_in_cid in by_cid.items():
        canonical_texts_in_cid = [ct for _, ct in slots_in_cid]
        cnt = Counter(canonical_texts_in_cid)
        colliding_in_cid = [
            (sid, ct)
            for sid, ct in slots_in_cid
            if cnt[ct] > 1 or global_cnt[ct] > 1
        ]
        total_colliding_slots += len(colliding_in_cid)
        if colliding_in_cid:
            duplicated_slots_by_competency[cid] = colliding_in_cid

    slot_uniqueness_pct = round(100.0 * unique_slots / total_slots, 2) if total_slots else 100.0
    raw_slot_uniqueness_pct = round(100.0 * raw_unique_slots / total_slots, 2) if total_slots else 100.0
    non_colliding_slot_pct = (
        round(100.0 * (total_slots - total_colliding_slots) / total_slots, 2)
        if total_slots
        else 100.0
    )
    instance_uniqueness_pct = (
        round(100.0 * len(set(all_norm_rats)) / len(all_norm_rats), 2)
        if all_norm_rats
        else 100.0
    )
    raw_uniqueness_pct = (
        round(100.0 * len(set(all_raw_masked_rats)) / len(all_raw_masked_rats), 2)
        if all_raw_masked_rats
        else 100.0
    )
    synthetic_prefix_pct = (
        round(100.0 * synthetic_prefix_cnt / len(all_norm_rats), 2)
        if all_norm_rats
        else 0.0
    )

    return {
        "total_rationales": len(all_norm_rats),
        "unique_instance_rationales": len(set(all_norm_rats)),
        "raw_unique_instance_rationales": len(set(all_raw_masked_rats)),
        "total_slots": total_slots,
        "unique_slots": unique_slots,
        "raw_unique_slots": raw_unique_slots,
        "colliding_slots": total_colliding_slots,
        "slot_uniqueness_pct": slot_uniqueness_pct,
        "raw_slot_uniqueness_pct": raw_slot_uniqueness_pct,
        "non_colliding_slot_pct": non_colliding_slot_pct,
        "instance_uniqueness_pct": instance_uniqueness_pct,
        "raw_uniqueness_pct": raw_uniqueness_pct,
        "synthetic_prefix_count": synthetic_prefix_cnt,
        "synthetic_prefix_pct": synthetic_prefix_pct,
        "duplicated_slots_by_competency": duplicated_slots_by_competency,
    }

