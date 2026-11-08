"""Single source of truth for the Stage 4 (build) acceptance contract.

Stage 2 (plan_shards -> pre_shard_manifest.json), the local author self-test
(compile_shard.py) and Stage 4 (run.py --stage build / engine.instantiate) MUST
all read these values from here. Never hardcode quotas/ratios elsewhere.
"""

import math
from typing import Any, Dict, Optional

CONTRACT_VERSION = 2
QUOTA_SKILL = 30
QUOTA_OTHER = 20
MIN_DIVERSITY_RATIO = 0.5
MIN_ARCHETYPES = 4
ARCHETYPE_KINDS = ("direct", "inverse", "perturbation", "boundary_or_edge_case")
SKILL_TYPES = ("skill", "hab", "habilidad")


def is_skill_type(comp_type: str) -> bool:
    return str(comp_type or "").lower().strip() in SKILL_TYPES


def quota_for_type(comp_type: str) -> int:
    return QUOTA_SKILL if is_skill_type(comp_type) else QUOTA_OTHER


def required_unique_stems(quota: int) -> int:
    """Minimum unique masked stems so that unique/quota >= MIN_DIVERSITY_RATIO."""
    return int(math.ceil(quota * MIN_DIVERSITY_RATIO))


def competency_contract(comp_type: str) -> Dict[str, Any]:
    quota = quota_for_type(comp_type)
    return {
        "type": str(comp_type or "concept").lower().strip(),
        "quota": quota,
        "required_unique_stems": required_unique_stems(quota),
        "min_diversity_ratio": MIN_DIVERSITY_RATIO,
        "min_archetypes": MIN_ARCHETYPES,
    }


def global_contract() -> Dict[str, Any]:
    return {
        "version": CONTRACT_VERSION,
        "quota_skill": QUOTA_SKILL,
        "quota_other": QUOTA_OTHER,
        "min_diversity_ratio": MIN_DIVERSITY_RATIO,
        "min_archetypes": MIN_ARCHETYPES,
    }


def stems_advice(comp_type: str, min_archetypes: Optional[int] = None) -> Dict[str, str]:
    """Author-facing ranges (20% headroom over the Stage 4 minimum for dedup after masking)."""
    m_arch = min_archetypes or MIN_ARCHETYPES
    uniq = required_unique_stems(quota_for_type(comp_type))
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
    diffs = [
        f"{k}: manifest={manifest_contract.get(k)!r} vs stage4={v!r}"
        for k, v in expected.items()
        if manifest_contract.get(k) != v
    ]
    return "; ".join(diffs)
