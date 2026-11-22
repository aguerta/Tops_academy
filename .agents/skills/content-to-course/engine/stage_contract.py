"""Single source of truth for the Stage 4 (build) acceptance contract.

Stage 2 (plan_shards -> pre_shard_manifest.json), the local author self-test
(compile_shard.py) and Stage 4 (run.py --stage build / engine.instantiate) MUST
all read these values from here. Never hardcode quotas/ratios elsewhere.
"""

import math
import os
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

CONTRACT_VERSION = 2
QUOTA_SKILL = 30
QUOTA_OTHER = 20
MIN_DIVERSITY_RATIO = 0.5
MIN_ARCHETYPES = 4
MIN_MODALITIES_PER_COMPETENCY = 2
MAX_MODALITIES_PER_COMPETENCY = 4
MIN_SEEDS_PER_TEMPLATE_SKILL = 4
MIN_SEEDS_PER_TEMPLATE_OTHER = 3


def _parse_default_templates_per_modality() -> int:
    raw = os.getenv("C2C_TEMPLATES_PER_MODALITY", "2")
    try:
        val = int(str(raw).strip())
    except (TypeError, ValueError):
        val = 2
    return max(1, val)


DEFAULT_TEMPLATES_PER_MODALITY = _parse_default_templates_per_modality()
ARCHETYPE_KINDS = ("direct", "inverse", "perturbation", "boundary_or_edge_case")
SKILL_TYPES = ("skill", "hab", "habilidad")


def is_skill_type(comp_type: str) -> bool:
    return str(comp_type or "").lower().strip() in SKILL_TYPES


def quota_for_type(comp_type: str) -> int:
    return QUOTA_SKILL if is_skill_type(comp_type) else QUOTA_OTHER


def required_templates_for_competency(
    num_modalities: int,
    templates_per_modality: int = DEFAULT_TEMPLATES_PER_MODALITY,
    min_archetypes: int = MIN_ARCHETYPES,
    has_mc7: bool = False,
) -> int:
    """Minimum distinct templates required for a competency given M modalities and K per modality.

    Under [M20-MC7-CAP] and [M20-ACTIVE-QUOTA]:
    - Skill competencies prohibit MC7 (0 MC7).
    - Non-Skill competencies allow at most 1 MC7 template (count(MC7) == 1 when recommended),
      while every active modality requires >= K templates and total active share must be >= 80%
      when K >= 2 (requiring >= 4 active templates alongside 1 MC7 => total >= 5).
    """
    eff_min_arch = max(1, int(min_archetypes))
    eff_k = max(1, int(templates_per_modality))
    eff_m = int(num_modalities) if num_modalities else 0
    if eff_m > 0:
        if has_mc7:
            if eff_k >= 2:
                return max(eff_min_arch, 5, 1 + max(0, eff_m - 1) * eff_k)
            return max(eff_min_arch, eff_m)
        return max(eff_min_arch, eff_m * eff_k)
    return eff_min_arch


def quota_for_competency(comp_type: str, num_templates: int) -> int:
    """Dynamic Stage 4 question quota scaled so each template receives adequate seed coverage."""
    n_tpls = max(0, int(num_templates))
    if is_skill_type(comp_type):
        return max(QUOTA_SKILL, n_tpls * MIN_SEEDS_PER_TEMPLATE_SKILL)
    return max(QUOTA_OTHER, n_tpls * MIN_SEEDS_PER_TEMPLATE_OTHER)


def required_unique_stems(quota: int) -> int:
    """Minimum unique masked stems so that unique/quota >= MIN_DIVERSITY_RATIO."""
    return int(math.ceil(quota * MIN_DIVERSITY_RATIO))


def competency_contract(
    comp_type: str,
    num_modalities: int = 0,
    templates_per_modality: Optional[int] = None,
    has_mc7: bool = False,
    target_bloom: Optional[str] = None,
) -> Dict[str, Any]:
    eff_k = (
        DEFAULT_TEMPLATES_PER_MODALITY
        if templates_per_modality is None
        else max(1, int(templates_per_modality))
    )
    eff_has_mc7 = bool(has_mc7) and not is_skill_type(comp_type)
    min_tpls = required_templates_for_competency(
        num_modalities=num_modalities,
        templates_per_modality=eff_k,
        min_archetypes=MIN_ARCHETYPES,
        has_mc7=eff_has_mc7,
    )
    quota = quota_for_competency(comp_type, min_tpls)
    res: Dict[str, Any] = {
        "type": str(comp_type or "concept").lower().strip(),
        "quota": quota,
        "required_unique_stems": required_unique_stems(quota),
        "min_diversity_ratio": MIN_DIVERSITY_RATIO,
        "min_archetypes": MIN_ARCHETYPES,
        "templates_per_modality": eff_k,
        "min_templates_required": min_tpls,
        "min_modalities": MIN_MODALITIES_PER_COMPETENCY,
        "max_modalities": MAX_MODALITIES_PER_COMPETENCY,
        "max_mc7_templates": 0 if is_skill_type(comp_type) else 1,
        "min_active_ratio": 0.75 if (min_tpls <= 4 and eff_k == 1) else 0.80,
    }
    if target_bloom:
        res["target_bloom"] = str(target_bloom).strip()
    return res


def global_contract(templates_per_modality: Optional[int] = None) -> Dict[str, Any]:
    eff_k = (
        DEFAULT_TEMPLATES_PER_MODALITY
        if templates_per_modality is None
        else max(1, int(templates_per_modality))
    )
    return {
        "version": CONTRACT_VERSION,
        "quota_skill": QUOTA_SKILL,
        "quota_other": QUOTA_OTHER,
        "min_diversity_ratio": MIN_DIVERSITY_RATIO,
        "min_archetypes": MIN_ARCHETYPES,
        "templates_per_modality": eff_k,
        "min_modalities": MIN_MODALITIES_PER_COMPETENCY,
        "max_modalities": MAX_MODALITIES_PER_COMPETENCY,
    }


def stems_advice(
    comp_type: str,
    min_archetypes: Optional[int] = None,
    quota: Optional[int] = None,
) -> Dict[str, str]:
    """Author-facing ranges (20% headroom over the Stage 4 minimum for dedup after masking)."""
    m_arch = max(1, int(min_archetypes)) if min_archetypes else MIN_ARCHETYPES
    eff_quota = int(quota) if quota is not None else quota_for_competency(comp_type, m_arch)
    uniq = required_unique_stems(eff_quota)
    lo = int(math.ceil(uniq * 1.2 / m_arch))
    hi = lo + 1
    return {
        "per_tpl": f"{lo}-{hi}",
        "total": f"{lo * m_arch}-{hi * m_arch}",
        "required": str(uniq),
    }


def stems_advice_text(min_archetypes: Optional[int] = None) -> str:
    s, c = stems_advice("skill", min_archetypes), stems_advice("concept", min_archetypes)
    return (
        f">= {s['per_tpl']} enunciados sintácticamente distintos por plantilla para Skills (total >= {s['total']}) "
        f"o >= {c['per_tpl']} para Concepts/Facts (total >= {c['total']})."
    )


def contract_tokens() -> Dict[str, str]:
    return {
        "<<S4_QUOTA_SKILL>>": str(QUOTA_SKILL),
        "<<S4_QUOTA_OTHER>>": str(QUOTA_OTHER),
        "<<S4_UNIQ_SKILL>>": str(required_unique_stems(QUOTA_SKILL)),
        "<<S4_UNIQ_OTHER>>": str(required_unique_stems(QUOTA_OTHER)),
        "<<S4_RATIO>>": f"{MIN_DIVERSITY_RATIO:.2f}",
        "<<S4_MIN_ARCH>>": str(MIN_ARCHETYPES),
        "<<S4_VARIANTS_SKILL>>": str(math.ceil(required_unique_stems(QUOTA_SKILL) / MIN_ARCHETYPES)),
        "<<S4_VARIANTS_OTHER>>": str(math.ceil(required_unique_stems(QUOTA_OTHER) / MIN_ARCHETYPES)),
        "<<S4_TPL_PER_MOD>>": str(DEFAULT_TEMPLATES_PER_MODALITY),
        "<<S4_MIN_MODS>>": str(MIN_MODALITIES_PER_COMPETENCY),
        "<<S4_MAX_MODS>>": str(MAX_MODALITIES_PER_COMPETENCY),
    }


_SHORT_TOKENS = {"%VO%": "<<S4_VARIANTS_OTHER>>", "%VS%": "<<S4_VARIANTS_SKILL>>"}


def render_contract_tokens(text: str) -> str:
    """Replace <<S4_*>> placeholders in prompts with the live Stage 4 contract values."""
    for short, long_tok in _SHORT_TOKENS.items():
        text = text.replace(short, long_tok)
    for tok, val in contract_tokens().items():
        text = text.replace(tok, val)
    return text


def contract_drift(manifest_contract: Any) -> str:
    """Return '' if manifest contract equals the code contract, else a description."""
    if manifest_contract is None:
        return ""  # legacy manifest: code constants (same source of truth) apply
    if not isinstance(manifest_contract, dict):
        return "'stage4_contract' del manifiesto es inválido (regenerar con run.py --stage shard)"
    expected = global_contract()
    base_keys = ("version", "quota_skill", "quota_other", "min_diversity_ratio", "min_archetypes")
    diffs = [
        f"{k}: manifest={manifest_contract.get(k)!r} vs stage4={expected[k]!r}"
        for k in base_keys
        if manifest_contract.get(k) != expected[k]
    ]
    for opt_k in ("min_modalities", "max_modalities"):
        if opt_k in manifest_contract and manifest_contract.get(opt_k) != expected[opt_k]:
            diffs.append(
                f"{opt_k}: manifest={manifest_contract.get(opt_k)!r} vs stage4={expected[opt_k]!r}"
            )
    if "templates_per_modality" in manifest_contract:
        tpm = manifest_contract.get("templates_per_modality")
        if isinstance(tpm, bool) or not isinstance(tpm, int) or tpm < 1:
            diffs.append(f"templates_per_modality: manifest={tpm!r} must be an int >= 1")
    return "; ".join(diffs)


# =============================================================================
# Bloom Quality Gate Constants & Helpers (M20 Calibrated Single Source of Truth)
# =============================================================================

BLOOM_LEVELS: Tuple[str, ...] = ("Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create")
BLOOM_RANK: Dict[str, int] = {lvl: idx for idx, lvl in enumerate(BLOOM_LEVELS, start=1)}

MODALITY_BLOOM_WEIGHTS: Dict[str, float] = {
    "multiple_choice_7_options": 2.20,
    "concept_matching": 2.80,
    "fill_in_the_blank": 3.25,
    "invariant_canvas": 3.45,
    "open_symbolic": 3.65,
    "multiple_select": 3.70,
    "proof_dag": 4.25,
    "unstructured_model": 4.40,
    "adversarial_break": 4.50,
}

EVALUATE_CAPABLE_MODALITIES: frozenset = frozenset({
    "adversarial_break",
    "unstructured_model",
    "proof_dag",
    "multiple_select",
})
LOW_COGNITIVE_MODALITIES: frozenset = frozenset({
    "multiple_choice_7_options",
    "concept_matching",
})
ASSUMPTION_REQUIRED_MODALITIES: frozenset = frozenset({"unstructured_model"})

MIN_COMPS_FOR_CTA_BLOOM_GATE: int = 5
BLOOM_FLOOR_BY_TYPE: Dict[str, float] = {"skill": 4.00, "concept": 3.75, "fact": 3.25}
EVAL_CAP_FLOOR_BY_TYPE: Dict[str, float] = {"skill": 0.50, "concept": 0.42, "fact": 0.20}
LOW_MOD_CAP_BY_TYPE: Dict[str, float] = {"skill": 0.08, "concept": 0.20, "fact": 0.45}

MODALITY_BLOOM_BOUNDS: Dict[str, Tuple[int, int]] = {
    "multiple_choice_7_options": (1, 3),  # Remember..Apply
    "concept_matching": (1, 4),           # Remember..Analyze
    "fill_in_the_blank": (2, 4),          # Understand..Analyze (direct capped a Apply)
    "open_symbolic": (2, 5),              # Understand..Evaluate
    "invariant_canvas": (2, 5),           # Understand..Evaluate
    "multiple_select": (2, 5),            # Understand..Evaluate
    "proof_dag": (3, 5),                  # Apply..Evaluate
    "adversarial_break": (4, 5),          # Analyze..Evaluate
    "unstructured_model": (4, 6),         # Analyze..Create
}
MODALITY_ARCHETYPE_BLOOM_OVERRIDES: Dict[Tuple[str, str], Tuple[int, int]] = {
    ("fill_in_the_blank", "direct"): (2, 3),
}

_MODALITY_ALIAS_MAP: Dict[str, str] = {
    "mc7": "multiple_choice_7_options",
    "mc_7": "multiple_choice_7_options",
    "mc": "multiple_choice_7_options",
    "multiple_choice": "multiple_choice_7_options",
    "multiple-choice": "multiple_choice_7_options",
    "multiple_choice_7_options": "multiple_choice_7_options",
    "single_choice": "multiple_choice_7_options",
    "ms": "multiple_select",
    "multiple_select": "multiple_select",
    "fib": "fill_in_the_blank",
    "fill_in_the_blank": "fill_in_the_blank",
}


def normalize_modality_name(raw: Any) -> str:
    """Normalize shorthand modality aliases (MC7/MS/FIB) to canonical M20 names."""
    key = str(raw or "").strip().lower()
    return _MODALITY_ALIAS_MAP.get(key, key)


def _normalize_bloom_label(bloom: Any) -> str:
    raw = str(bloom or "").strip().capitalize()
    return raw if raw in BLOOM_RANK else ""


def _canonical_comp_bucket(comp: Dict[str, Any]) -> str:
    cid = str(comp.get("id") or "").strip()
    ctype = str(comp.get("type") or comp.get("category") or "concept").lower().strip()
    if is_skill_type(ctype) or cid.startswith("Hab-"):
        return "skill"
    if ctype == "fact" or cid.startswith("H-") or cid.startswith("PRE-"):
        return "fact"
    return "concept"


def compute_cta_bloom_portfolio_metrics(
    competencies: Iterable[Dict[str, Any]],
    templates_per_modality: int = DEFAULT_TEMPLATES_PER_MODALITY,
    exclude_ids: Optional[Set[str]] = None,
) -> Dict[str, Any]:
    """Compute quota-weighted expected Bloom index and adaptive portfolio floors for CTA competencies."""
    eff_k = max(1, int(templates_per_modality or DEFAULT_TEMPLATES_PER_MODALITY))
    excluded = set(exclude_ids or set())

    total_quota = 0.0
    weighted_bloom_sum = 0.0
    weighted_eval_sum = 0.0
    weighted_low_sum = 0.0
    floor_sum = 0.0
    eval_floor_sum = 0.0
    low_cap_sum = 0.0
    eligible_count = 0
    comp_profiles: List[Dict[str, Any]] = []

    for comp in competencies or []:
        if not isinstance(comp, dict):
            continue
        cid = str(comp.get("id") or "").strip()
        if not cid or cid in excluded or comp.get("read_only_base") is True:
            continue
        raw_mods = comp.get("recommended_modalities") or []
        if not isinstance(raw_mods, list) or not raw_mods:
            continue
        norm_mods = list(dict.fromkeys(normalize_modality_name(m) for m in raw_mods if str(m).strip()))
        if not norm_mods:
            continue

        bucket = _canonical_comp_bucket(comp)
        is_sk = bucket == "skill"
        has_mc7 = ("multiple_choice_7_options" in norm_mods) and not is_sk
        tpl_weights = {
            m: (1.0 if (m == "multiple_choice_7_options" and has_mc7) else float(eff_k))
            for m in norm_mods
        }
        sum_tw = sum(tpl_weights.values()) or 1.0
        n_tpls = required_templates_for_competency(
            num_modalities=len(norm_mods),
            templates_per_modality=eff_k,
            has_mc7=has_mc7,
        )
        quota = float(quota_for_competency("skill" if is_sk else "concept", n_tpls))

        c_bloom = sum(MODALITY_BLOOM_WEIGHTS.get(m, 3.0) * tpl_weights[m] for m in norm_mods) / sum_tw
        c_eval = sum(tpl_weights[m] for m in norm_mods if m in EVALUATE_CAPABLE_MODALITIES) / sum_tw
        c_low = sum(tpl_weights[m] for m in norm_mods if m in LOW_COGNITIVE_MODALITIES) / sum_tw

        eligible_count += 1
        total_quota += quota
        weighted_bloom_sum += quota * c_bloom
        weighted_eval_sum += quota * c_eval
        weighted_low_sum += quota * c_low
        floor_sum += quota * BLOOM_FLOOR_BY_TYPE.get(bucket, 3.75)
        eval_floor_sum += quota * EVAL_CAP_FLOOR_BY_TYPE.get(bucket, 0.42)
        low_cap_sum += quota * LOW_MOD_CAP_BY_TYPE.get(bucket, 0.20)

        comp_profiles.append({
            "id": cid,
            "type": bucket,
            "bloom": str(comp.get("bloom") or ""),
            "expected_bloom": round(c_bloom, 3),
            "recommended_modalities": norm_mods,
            "assumptions_count": len(comp.get("assumptions") or []) if isinstance(comp.get("assumptions"), list) else int(comp.get("assumptions_count") or 0),
            "distractor_count": len(comp.get("distractors") or []) if isinstance(comp.get("distractors"), list) else int(comp.get("distractor_count") or 0),
        })

    active_gate = eligible_count >= MIN_COMPS_FOR_CTA_BLOOM_GATE
    if total_quota <= 0:
        return {
            "eligible_competencies": 0,
            "active_gate": False,
            "expected_bloom_index": 0.0,
            "adaptive_bloom_floor": 0.0,
            "evaluate_capable_ratio": 0.0,
            "adaptive_eval_floor": 0.0,
            "low_modality_ratio": 0.0,
            "adaptive_low_cap": 1.0,
            "passes": True,
            "violations": [],
            "weak_competencies": [],
        }

    expected_bloom_index = round(weighted_bloom_sum / total_quota, 3)
    adaptive_bloom_floor = round(floor_sum / total_quota, 3)
    evaluate_capable_ratio = round(weighted_eval_sum / total_quota, 3)
    adaptive_eval_floor = round(eval_floor_sum / total_quota, 3)
    low_modality_ratio = round(weighted_low_sum / total_quota, 3)
    adaptive_low_cap = round(low_cap_sum / total_quota, 3)

    violations: List[str] = []
    if active_gate:
        if expected_bloom_index + 1e-9 < adaptive_bloom_floor:
            violations.append(
                f"expected_bloom_index={expected_bloom_index:.3f} < adaptive_bloom_floor={adaptive_bloom_floor:.3f}"
            )
        if evaluate_capable_ratio + 1e-9 < adaptive_eval_floor:
            violations.append(
                f"evaluate_capable_ratio={evaluate_capable_ratio * 100:.1f}% < adaptive_eval_floor={adaptive_eval_floor * 100:.1f}%"
            )
        if low_modality_ratio - 1e-9 > adaptive_low_cap:
            violations.append(
                f"low_modality_ratio={low_modality_ratio * 100:.1f}% > adaptive_low_cap={adaptive_low_cap * 100:.1f}%"
            )

    weak_competencies = sorted(
        comp_profiles,
        key=lambda item: (item["expected_bloom"], 0 if item["type"] == "skill" else (1 if item["type"] == "concept" else 2), item["id"]),
    )[:5]

    return {
        "eligible_competencies": eligible_count,
        "active_gate": active_gate,
        "expected_bloom_index": expected_bloom_index,
        "adaptive_bloom_floor": adaptive_bloom_floor,
        "evaluate_capable_ratio": evaluate_capable_ratio,
        "adaptive_eval_floor": adaptive_eval_floor,
        "low_modality_ratio": low_modality_ratio,
        "adaptive_low_cap": adaptive_low_cap,
        "passes": (len(violations) == 0) if active_gate else True,
        "violations": violations,
        "weak_competencies": weak_competencies,
    }


def template_bloom_bounds(interaction_type: Any, archetype: Any = None) -> Optional[Tuple[int, int]]:
    """Return allowed (min_rank, max_rank) Bloom bounds for a modality and optional archetype."""
    norm_mod = normalize_modality_name(interaction_type)
    norm_arch = str(archetype or "").strip().lower()
    if norm_arch and (norm_mod, norm_arch) in MODALITY_ARCHETYPE_BLOOM_OVERRIDES:
        return MODALITY_ARCHETYPE_BLOOM_OVERRIDES[(norm_mod, norm_arch)]
    return MODALITY_BLOOM_BOUNDS.get(norm_mod)


def check_template_bloom_coherence(interaction_type: Any, archetype: Any, bloom: Any) -> Optional[str]:
    """Validate modality x archetype x bloom coherence against anti-Goodhart bounds."""
    norm_bloom = _normalize_bloom_label(bloom)
    if not norm_bloom:
        return None
    bounds = template_bloom_bounds(interaction_type, archetype=archetype)
    if not bounds:
        return None
    rank = BLOOM_RANK[norm_bloom]
    min_r, max_r = bounds
    if rank < min_r or rank > max_r:
        norm_mod = normalize_modality_name(interaction_type)
        norm_arch = str(archetype or "unknown").strip().lower()
        min_lbl = BLOOM_LEVELS[min_r - 1]
        max_lbl = BLOOM_LEVELS[max_r - 1]
        return (
            f"Modalidad '{norm_mod}' (arquetipo='{norm_arch}') con Bloom='{norm_bloom}' está fuera del rango coherente "
            f"[{min_lbl}..{max_lbl}]."
        )
    return None


def max_achievable_bloom_rank(modalities: Iterable[Any]) -> int:
    """Return the maximum Bloom rank achievable across the given modalities."""
    best = 0
    for m in modalities or []:
        bounds = template_bloom_bounds(m)
        if bounds:
            best = max(best, bounds[1])
    return best

