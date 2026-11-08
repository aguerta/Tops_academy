"""Deterministic parametric instantiation engine for content-to-course v2.

Features:
- Quota allocation: >=30 for Skill, >=20 for Fact/Concept
- Balanced allocation across templates (>=2 per interaction type)
- Deterministic seed sweeping
- Deduplication: rejects duplicate parameter tuples and duplicate stem texts
- 100% Invariant evaluation on every instance
- Diversity calculation per competency
"""

import re
import zlib
from typing import Any, Dict, List, Optional, Set, Tuple

from engine.assemble import assemble_question, format_template_string, sanitize_katex_syntax
from engine.diversity import evaluate_competency_diversity
from engine.invariants import InvariantViolationError, check_instance_invariants
from engine.sandbox import (
    execute_sandbox_batch,
    execute_sandbox_instance,
    SandboxExecutionError,
    SandboxTimeoutError,
    SecurityViolationError,
)


def competency_seed_base(cid: str, base_seed: int = 42) -> int:
    """Returns deterministic base seed for a competency, strictly shared between local check and build."""
    return base_seed + (zlib.crc32(cid.encode("utf-8")) % 10000)


def get_competency_quota(comp_type: str) -> int:
    """Return required question quota: >=30 for Skill, >=20 for Fact/Concept."""
    from engine.stage_contract import quota_for_type
    return quota_for_type(comp_type)


def allocate_template_quotas(
    templates: List[Dict[str, Any]],
    target_quota: int,
) -> Dict[str, int]:
    """Distribute quota evenly across templates while enforcing >=2 per interaction type."""
    if not templates:
        return {}

    num_templates = len(templates)
    base_quota = target_quota // num_templates
    remainder = target_quota % num_templates

    quotas = {}
    for idx, tpl in enumerate(templates):
        t_id = tpl["id"]
        extra = 1 if idx < remainder else 0
        quotas[t_id] = base_quota + extra

    return quotas


MAX_SUBSEED_ATTEMPTS = 8


def compute_subseed(seed: int, k: int) -> int:
    """Deterministic sub-seed derivation for rejection sampling."""
    if k == 0:
        return seed
    return (seed * 1009 + k) & 0x7FFFFFFF


def instantiate_verified_seed(
    template: Dict[str, Any],
    seed: int,
    competency_id: str = "comp-01",
    question_index: int = 1,
    cta_distractors_map: Optional[Dict[str, Dict[str, Any]]] = None,
    max_subseeds: int = MAX_SUBSEED_ATTEMPTS,
    timeout: float = 5.0,
) -> Tuple[Dict[str, Any], Dict[str, Any], int]:
    """Deterministically instantiate a verified question instance using sub-seed rejection sampling on collision.

    Returns:
        (candidate_q, gen_res, subseed_index_used)
    """
    generate_py = template["generate_py"]
    cross_check_py = template.get("cross_check_py")
    interaction_type = template["interaction_type"]

    last_errors: List[str] = []
    collision_seen = False

    for k in range(max_subseeds):
        s_k = compute_subseed(seed, k)
        try:
            gen_res = execute_sandbox_instance(
                generate_py,
                seed=s_k,
                cross_check_py=cross_check_py,
                timeout=timeout,
            )
        except Exception as e:
            last_errors = [str(e)]
            continue

        variables = gen_res.get("vars", {})
        try:
            candidate_q = assemble_question(
                template=template,
                gen_result=gen_res,
                competency_id=competency_id,
                question_index=question_index,
                cta_distractors_map=cta_distractors_map,
                seed=s_k,
            )
        except Exception as e:
            last_errors = [f"Assembly error: {e}"]
            continue

        is_valid, errors = check_instance_invariants(candidate_q, interaction_type, variables=variables)
        if is_valid:
            return candidate_q, gen_res, k

        has_collision = any(
            "Distractor identical to correct answer" in e or "Duplicate option content" in e
            for e in errors
        )
        if has_collision:
            collision_seen = True
        last_errors = errors

    tpl_id = template.get("id", "UNKNOWN")
    if collision_seen:
        err_msg = (
            f"[-] [TPL-D4] Collision violation in template '{tpl_id}' on seed {seed}: "
            f"Exhausted all {max_subseeds} sub-seeds without resolving distractor collision. "
            f"Last errors: {last_errors}"
        )
        raise InvariantViolationError(err_msg)
    else:
        err_msg = (
            f"Template '{tpl_id}' failed invariants on seed {seed} after {max_subseeds} sub-seeds. "
            f"Last errors: {last_errors}"
        )
        raise InvariantViolationError(err_msg)


def instantiate_template(
    template: Dict[str, Any],
    competency_id: str,
    target_count: int,
    start_index: int = 1,
    seed_offset: int = 1000,
    cta_distractors_map: Optional[Dict[str, Dict[str, Any]]] = None,
    max_attempts: int = 300,
) -> List[Dict[str, Any]]:
    """Deterministically sweep seeds and instantiate unique, invariant-valid questions."""
    generate_py = template["generate_py"]
    cross_check_py = template.get("cross_check_py")
    interaction_type = template["interaction_type"]

    seen_param_tuples: Set[Tuple[Tuple[str, str], ...]] = set()
    seen_stems: Set[str] = set()
    instantiated_questions: List[Dict[str, Any]] = []

    attempt = 0
    batch_size = 20

    seeds_evaluated_count = 0
    seeds_retried_count = 0

    while len(instantiated_questions) < target_count and attempt < max_attempts:
        current_batch_seeds = [
            seed_offset + attempt + i for i in range(min(batch_size, max_attempts - attempt))
        ]
        attempt += len(current_batch_seeds)

        try:
            batch_results = execute_sandbox_batch(
                generate_py=generate_py,
                seeds=current_batch_seeds,
                cross_check_py=cross_check_py,
            )
        except Exception:
            batch_results = []
            for s in current_batch_seeds:
                try:
                    res = execute_sandbox_instance(generate_py, seed=s, cross_check_py=cross_check_py)
                    batch_results.append({"seed": s, "success": True, "result": res})
                except Exception as e:
                    batch_results.append({"seed": s, "success": False, "error": str(e)})

        for item in batch_results:
            if not item.get("success"):
                err_txt = str(item.get("error", ""))
                if "SandboxTimeoutError" in err_txt:
                    raise SandboxTimeoutError(
                        f"Template {template.get('id', 'UNKNOWN')} timed out during instantiation: {err_txt}"
                    )
                continue

            s = item["seed"]
            gen_res = item["result"]
            variables = gen_res.get("vars", {})

            # 1. Parameter tuple deduplication
            param_tuple = tuple(sorted((str(k), str(v)) for k, v in variables.items()))
            if param_tuple in seen_param_tuples:
                continue

            # 2. Rendered stem text deduplication
            raw_stem = template["stem"]
            stem_variants = template.get("stem_variants")
            if stem_variants and len(stem_variants) > 0:
                var_idx = (s % len(stem_variants))
                raw_stem = stem_variants[var_idx]
            rendered_stem = sanitize_katex_syntax(format_template_string(raw_stem, variables))
            norm_stem = re.sub(r"\s+", " ", rendered_stem.strip())
            if norm_stem in seen_stems:
                continue

            # 3. Assemble candidate question
            q_num = start_index + len(instantiated_questions)
            try:
                candidate_q = assemble_question(
                    template=template,
                    gen_result=gen_res,
                    competency_id=competency_id,
                    question_index=q_num,
                    cta_distractors_map=cta_distractors_map,
                    seed=s,
                )
            except Exception:
                continue

            # 4. Invariant validation on candidate
            is_valid, errors = check_instance_invariants(candidate_q, interaction_type, variables=variables)
            k_used = 0

            # If invalid due to collision, attempt sub-seed rejection sampling
            if not is_valid:
                has_collision = any(
                    "Distractor identical to correct answer" in e or "Duplicate option content" in e
                    for e in errors
                )
                if has_collision:
                    try:
                        candidate_q, gen_res, k_used = instantiate_verified_seed(
                            template=template,
                            seed=s,
                            competency_id=competency_id,
                            question_index=q_num,
                            cta_distractors_map=cta_distractors_map,
                            max_subseeds=MAX_SUBSEED_ATTEMPTS,
                        )
                        variables = gen_res.get("vars", {})
                        param_tuple = tuple(sorted((str(k), str(v)) for k, v in variables.items()))
                        if param_tuple in seen_param_tuples:
                            continue
                        rendered_stem = candidate_q["stem"]
                        norm_stem = re.sub(r"\s+", " ", rendered_stem.strip())
                        if norm_stem in seen_stems:
                            continue
                        is_valid = True
                    except InvariantViolationError:
                        raise
                    except Exception:
                        continue
                else:
                    continue

            if not is_valid:
                continue

            seeds_evaluated_count += 1
            if k_used > 0:
                seeds_retried_count += 1
                # Anti-cloning safeguard: > 20% retry rate indicates structurally identical distractors
                if seeds_evaluated_count >= 5 and (seeds_retried_count / seeds_evaluated_count) > 0.20:
                    tpl_id = template.get("id", "UNKNOWN")
                    raise InvariantViolationError(
                        f"[-] [TPL-D4] Anti-cloning safeguard violation in template '{tpl_id}': "
                        f"Sub-seed retry rate {seeds_retried_count}/{seeds_evaluated_count} "
                        f"({(seeds_retried_count/seeds_evaluated_count):.1%}) exceeds 20% limit. "
                        f"Distractors are structurally identical or systematically colliding."
                    )

            # Passed all checks!
            seen_param_tuples.add(param_tuple)
            seen_stems.add(norm_stem)
            instantiated_questions.append(candidate_q)

            if len(instantiated_questions) >= target_count:
                break

    if len(instantiated_questions) < target_count:
        raise ValueError(
            f"Template {template['id']} could only generate {len(instantiated_questions)}/{target_count} "
            f"unique invariant instances after {attempt} attempts."
        )

    return instantiated_questions


def instantiate_competency(
    competency: Optional[Any] = None,
    templates: Optional[List[Dict[str, Any]]] = None,
    cta_distractors_map: Optional[Dict[str, Dict[str, Any]]] = None,
    seed_offset_base: int = 10000,
    *,
    competency_id: Optional[str] = None,
    category: Optional[str] = None,
    quota: Optional[int] = None,
    base_seed: Optional[int] = None,
) -> Dict[str, Any]:
    """Instantiate complete question bank for a competency fulfilling quotas and diversity.
    
    Supports both (competency=dict/obj, templates=list, ...) and
    (competency_id=..., category=..., templates=..., quota=..., base_seed=...).
    """
    templates = templates or []

    # Extract ID
    if isinstance(competency, dict):
        comp_id = competency.get("id", competency_id or "comp-01")
        comp_type = competency.get("type", category or "concept")
    elif competency is not None:
        comp_id = getattr(competency, "id", competency_id or "comp-01")
        comp_type = getattr(competency, "category", getattr(competency, "type", category or "concept"))
    else:
        comp_id = competency_id or "comp-01"
        comp_type = category or "concept"

    if quota is not None:
        target_quota = quota
    else:
        target_quota = get_competency_quota(comp_type)

    if base_seed is not None:
        seed_offset_base = base_seed

    quotas = allocate_template_quotas(templates, target_quota)

    all_questions: List[Dict[str, Any]] = []
    q_counter = 1

    for t_idx, tpl in enumerate(templates):
        t_id = tpl["id"]
        t_quota = quotas.get(t_id, 0)
        if t_quota <= 0:
            continue

        tpl_seed_offset = seed_offset_base + (t_idx * 500)
        tpl_questions = instantiate_template(
            template=tpl,
            competency_id=comp_id,
            target_count=t_quota,
            start_index=q_counter,
            seed_offset=tpl_seed_offset,
            cta_distractors_map=cta_distractors_map,
        )
        all_questions.extend(tpl_questions)
        q_counter += len(tpl_questions)

    # Calculate diversity
    stems = [q["stem"] for q in all_questions]
    div_stats = evaluate_competency_diversity(stems)

    counts_by_type: Dict[str, int] = {}
    for q in all_questions:
        itype = q["interaction_type"]
        counts_by_type[itype] = counts_by_type.get(itype, 0) + 1

    return {
        "competency_id": comp_id,
        "quota_target": target_quota,
        "total_generated": len(all_questions),
        "questions": all_questions,
        "diversity_stats": div_stats,
        "counts_by_type": counts_by_type,
    }
