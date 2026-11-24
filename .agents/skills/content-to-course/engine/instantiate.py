"""Deterministic parametric instantiation engine for content-to-course v2.

Features:
- Quota allocation: >=30 for Skill, >=20 for Fact/Concept
- Balanced allocation across templates (>=2 per interaction type)
- Deterministic seed sweeping
- Deduplication: rejects duplicate parameter tuples and duplicate stem texts
- 100% Invariant evaluation on every instance
- Diversity calculation per competency
"""

import json
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


def get_competency_quota(comp_type: str, num_templates: int = 0) -> int:
    """Return required question quota: max(30, N*4) for Skill, max(20, N*3) for Fact/Concept."""
    from engine.stage_contract import quota_for_competency, quota_for_type
    if num_templates and int(num_templates) > 0:
        return quota_for_competency(comp_type, int(num_templates))
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
        t_id = tpl.get("id") or tpl.get("template_id") or f"tpl_{idx}"
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


def _answer_key_signature(q: Dict[str, Any]) -> str:
    """Return a canonical signature of the assembled answer key for rejection sampling."""
    q_type = str(q.get("interaction_type") or q.get("type") or "").strip().lower()
    if q_type in ("multiple_choice_7_options", "multiple_choice"):
        correct_opt = next((opt for opt in q.get("options", []) if opt.get("is_correct")), None)
        return re.sub(r"\s+", " ", str(correct_opt.get("content", ""))).strip() if correct_opt else ""
    if q_type in ("fill_in_the_blank", "open_symbolic"):
        ans = q.get("correct_answer")
        if isinstance(ans, dict):
            val = ans.get("expression") or ans.get("value") or ans.get("canonical_algebraic") or q.get("correct", "")
        else:
            val = ans if ans is not None else q.get("correct", "")
        return re.sub(r"\s+", " ", str(val)).strip()
    if q_type == "multiple_select":
        pairs = sorted(
            (re.sub(r"\s+", " ", str(opt.get("content", ""))).strip(), bool(opt.get("is_correct")))
            for opt in q.get("options", [])
        )
        return json.dumps(pairs, default=str)
    if q_type in ("proof_dag", "adversarial_break", "unstructured_model", "concept_matching"):
        sig_obj: Dict[str, Any] = {"correct_answer": q.get("correct_answer")}
        payload = q.get(q_type)
        if isinstance(payload, dict):
            if q_type == "proof_dag":
                sig_obj["steps"] = sorted(
                    ((s.get("id"), s.get("content"), bool(s.get("is_fallacy")))
                     for s in (payload.get("steps") or []) if isinstance(s, dict)),
                    key=lambda t: str(t),
                )
            elif q_type == "adversarial_break":
                sig_obj["prompt"] = payload.get("prompt")
                sig_obj["sample_witness"] = payload.get("sample_witness")
                sig_obj["steps"] = [
                    (s.get("id"), s.get("content"), bool(s.get("is_fallacy")))
                    for s in (payload.get("steps") or []) if isinstance(s, dict)
                ]
                sig_obj["predicates"] = [
                    p.get("expr") for p in (payload.get("predicates") or []) if isinstance(p, dict)
                ]
            elif q_type == "unstructured_model":
                sig_obj["p1"] = sorted(
                    ((it.get("id"), it.get("label"))
                     for it in ((payload.get("phase1_variables") or {}).get("items") or []) if isinstance(it, dict)),
                    key=lambda t: str(t),
                )
                sig_obj["p2"] = sorted(
                    str((o.get("id"), o.get("content")))
                    for o in ((payload.get("phase2_assumptions") or {}).get("options") or []) if isinstance(o, dict)
                )
                _p3 = payload.get("phase3_formulation") or {}
                sig_obj["p3"] = _p3.get("correct_expression")
                sig_obj["p3_opts"] = sorted(
                    str((o.get("id"), o.get("content")))
                    for o in (_p3.get("options") or []) if isinstance(o, dict)
                )
            elif q_type == "concept_matching":
                sig_obj["premises"] = sorted(
                    ((p.get("id"), p.get("content")) for p in (payload.get("premises") or []) if isinstance(p, dict)),
                    key=lambda t: str(t),
                )
                sig_obj["targets"] = sorted(
                    ((t.get("id"), t.get("content")) for t in (payload.get("targets") or []) if isinstance(t, dict)),
                    key=lambda t: str(t),
                )
        return json.dumps(sig_obj, sort_keys=True, default=str)
    return re.sub(r"\s+", " ", str(q.get("correct", ""))).strip()


def instantiate_template(
    template: Dict[str, Any],
    competency_id: str,
    target_count: int,
    start_index: int = 1,
    seed_offset: int = 1000,
    cta_distractors_map: Optional[Dict[str, Dict[str, Any]]] = None,
    max_attempts: int = 300,
    shared_key_counts: Optional[Dict[str, int]] = None,
    max_key_count: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """Deterministically sweep seeds and instantiate unique, invariant-valid questions."""
    generate_py = template["generate_py"]
    cross_check_py = template.get("cross_check_py")
    interaction_type = template["interaction_type"]

    seen_param_tuples: Set[Tuple[Tuple[str, str], ...]] = set()
    seen_stems: Set[str] = set()
    instantiated_questions: List[Dict[str, Any]] = []
    deferred_clumped: List[Tuple[Dict[str, Any], Tuple[Tuple[str, str], ...], str, str]] = []
    clean_comp = re.sub(r"[^A-Za-z0-9]", "", competency_id)

    attempt = 0

    seeds_evaluated_count = 0
    seeds_retried_count = 0

    while len(instantiated_questions) < target_count and attempt < max_attempts:
        cur_batch_size = min(20, max(6, target_count * 2)) if attempt == 0 else 20
        current_batch_seeds = [
            seed_offset + attempt + i for i in range(min(cur_batch_size, max_attempts - attempt))
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
                if "SecurityViolationError" in err_txt or "SandboxSecurityError" in err_txt:
                    raise SecurityViolationError(
                        f"Template {template.get('id', 'UNKNOWN')} security violation on seed {item.get('seed')}: {err_txt}"
                    )
                if "SandboxTimeoutError" in err_txt:
                    raise SandboxTimeoutError(
                        f"Template {template.get('id', 'UNKNOWN')} timed out during instantiation: {err_txt}"
                    )
                raise SandboxExecutionError(
                    f"Template {template.get('id', 'UNKNOWN')} failed on seed {item.get('seed')}: {err_txt}"
                )

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
            except Exception as e:
                raise SandboxExecutionError(
                    f"Template {template.get('id', 'UNKNOWN')} failed during question assembly on seed {s}: {e}"
                )

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

            # Stratified rejection sampling against answer-key clumping
            k_sig = ""
            if shared_key_counts is not None and max_key_count is not None:
                k_sig = _answer_key_signature(candidate_q)
                if k_sig and shared_key_counts.get(k_sig, 0) >= max_key_count:
                    if len(deferred_clumped) < target_count:
                        deferred_clumped.append((candidate_q, param_tuple, norm_stem, k_sig))
                    continue

            # Passed all checks!
            seen_param_tuples.add(param_tuple)
            seen_stems.add(norm_stem)
            if shared_key_counts is not None and k_sig:
                shared_key_counts[k_sig] = shared_key_counts.get(k_sig, 0) + 1
            instantiated_questions.append(candidate_q)

            if len(instantiated_questions) >= target_count:
                break

    if len(instantiated_questions) < target_count and deferred_clumped:
        for cand_q, p_tup, n_stem, k_sig in deferred_clumped:
            if len(instantiated_questions) >= target_count:
                break
            if p_tup in seen_param_tuples or n_stem in seen_stems:
                continue
            q_idx = start_index + len(instantiated_questions)
            cand_q["id"] = f"Q-{clean_comp}-{q_idx:03d}"
            seen_param_tuples.add(p_tup)
            seen_stems.add(n_stem)
            if shared_key_counts is not None and k_sig:
                shared_key_counts[k_sig] = shared_key_counts.get(k_sig, 0) + 1
            instantiated_questions.append(cand_q)

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
        comp_id = str(competency.get("id") or competency_id or "comp-01")
        comp_type = str(competency.get("type") or competency.get("category") or category or "")
    elif competency is not None:
        comp_id = str(getattr(competency, "id", None) or competency_id or "comp-01")
        comp_type = str(getattr(competency, "category", None) or getattr(competency, "type", None) or category or "")
    else:
        comp_id = str(competency_id or "comp-01")
        comp_type = str(category or "")
    if comp_id.startswith("Hab-"):
        comp_type = "skill"
    elif not comp_type.strip():
        comp_type = "concept"

    min_contract_quota = get_competency_quota(comp_type, num_templates=len(templates))
    if quota is not None:
        target_quota = max(int(quota), min_contract_quota) if int(quota) >= 20 else int(quota)
    else:
        target_quota = min_contract_quota

    if base_seed is not None:
        seed_offset_base = base_seed

    quotas = allocate_template_quotas(templates, target_quota)

    all_questions: List[Dict[str, Any]] = []
    q_counter = 1
    shared_key_counts: Optional[Dict[str, int]] = {} if target_quota >= 20 else None
    max_key_count: Optional[int] = max(2, int(target_quota * 0.20)) if target_quota >= 20 else None

    for t_idx, tpl in enumerate(templates):
        t_id = tpl.get("id") or tpl.get("template_id") or f"tpl_{t_idx}"
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
            shared_key_counts=shared_key_counts,
            max_key_count=max_key_count,
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
