"""Single source of truth for the Stage 4 (build) acceptance contract.

Stage 2 (plan_shards -> pre_shard_manifest.json), the local author self-test
(compile_shard.py) and Stage 4 (run.py --stage build / engine.instantiate) MUST
all read these values from here. Never hardcode quotas/ratios elsewhere.
"""

import math
import os
from typing import Any, Dict, Optional

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
) -> int:
    """Minimum distinct templates required for a competency given M modalities and K per modality."""
    eff_min_arch = max(1, int(min_archetypes))
    eff_k = max(1, int(templates_per_modality))
    eff_m = int(num_modalities) if num_modalities else 0
    if eff_m > 0:
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
) -> Dict[str, Any]:
    eff_k = (
        DEFAULT_TEMPLATES_PER_MODALITY
        if templates_per_modality is None
        else max(1, int(templates_per_modality))
    )
    min_tpls = required_templates_for_competency(
        num_modalities=num_modalities,
        templates_per_modality=eff_k,
        min_archetypes=MIN_ARCHETYPES,
    )
    quota = quota_for_competency(comp_type, min_tpls)
    return {
        "type": str(comp_type or "concept").lower().strip(),
        "quota": quota,
        "required_unique_stems": required_unique_stems(quota),
        "min_diversity_ratio": MIN_DIVERSITY_RATIO,
        "min_archetypes": MIN_ARCHETYPES,
        "templates_per_modality": eff_k,
        "min_templates_required": min_tpls,
        "min_modalities": MIN_MODALITIES_PER_COMPETENCY,
        "max_modalities": MAX_MODALITIES_PER_COMPETENCY,
    }


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
