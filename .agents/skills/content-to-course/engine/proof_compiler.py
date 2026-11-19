"""Shift-Left ProofDAG compiler and verifier for Bloom Superior (`proof_dag`) items.

Pre-compiles step-by-step derivations into topologically verified DAGs with
valid deductive steps, optional justification requirements, and fallacy trap steps,
optionally verifying algebraic steps via SymPy during course build time ($0 server runtime).
"""

from __future__ import annotations

import random
from collections import deque
from typing import Any, Dict, List, Optional, Set, Tuple


def _get_format_helpers():
    try:
        from engine.assemble import (
            _is_generic_placeholder,
            _resolve_distractor_rationale,
            format_template_string,
            sanitize_katex_syntax,
        )
    except ImportError:
        from .assemble import (
            _is_generic_placeholder,
            _resolve_distractor_rationale,
            format_template_string,
            sanitize_katex_syntax,
        )
    return format_template_string, sanitize_katex_syntax, _resolve_distractor_rationale, _is_generic_placeholder


def _format_text(text: Any, variables: Dict[str, Any], format_fn, sanitize_fn) -> str:
    if text is None:
        return ""
    s = str(text).strip()
    if not s:
        return ""
    if variables:
        s = format_fn(s, variables)
    return sanitize_fn(s)


def _verify_sympy_step(step: Dict[str, Any], step_id: str, variables: Dict[str, Any], format_fn) -> None:
    """Optionally verify algebraic equivalence for a step carrying sympy_expr / expected_sympy_expr."""
    lhs_raw = step.get("sympy_expr")
    rhs_raw = step.get("expected_sympy_expr") if "expected_sympy_expr" in step else step.get("sympy_equiv_to")
    if not lhs_raw or not rhs_raw:
        return
    try:
        import sympy as sp  # type: ignore
    except ImportError:
        return

    safe_vars = {
        k: (f"({v})" if isinstance(v, (int, float)) and not isinstance(v, bool) and v < 0 else v)
        for k, v in (variables or {}).items()
    }
    lhs_str = format_fn(str(lhs_raw), safe_vars) if safe_vars else str(lhs_raw)
    rhs_str = format_fn(str(rhs_raw), safe_vars) if safe_vars else str(rhs_raw)
    try:
        lhs = sp.sympify(lhs_str)
        rhs = sp.sympify(rhs_str)
        diff = sp.simplify(lhs - rhs)
        if diff != 0 and getattr(diff, "free_symbols", None):
            num_subs = {
                sp.Symbol(str(k)): v
                for k, v in (variables or {}).items()
                if isinstance(v, (int, float)) and not isinstance(v, bool)
            }
            if num_subs and {sy for sy in diff.free_symbols} <= set(num_subs):
                diff = sp.simplify(diff.subs(num_subs))
        if diff != 0:
            raise ValueError(
                f"[PROOF-DAG-SYMPY] Step '{step_id}' failed SymPy equivalence check: "
                f"simplify(({lhs_str}) - ({rhs_str})) = {diff} != 0."
            )
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError(
            f"[PROOF-DAG-SYMPY] Step '{step_id}' SymPy expression parse/check error: {exc}"
        ) from exc


def extract_proof_dag_distractor_ids(raw_dag: Any) -> List[str]:
    """Extract all distractor_id references from a raw or compiled proof_dag payload."""
    if not isinstance(raw_dag, dict):
        return []
    dids: List[str] = []
    seen: Set[str] = set()
    for step in raw_dag.get("steps") or []:
        if not isinstance(step, dict):
            continue
        did = step.get("distractor_id") or step.get("did")
        if isinstance(did, str) and did.strip():
            norm = did.strip().replace("_", "-")
            if norm not in seen:
                seen.add(norm)
                dids.append(norm)
    return dids


def compile_and_verify_proof_dag(
    raw_dag: Dict[str, Any],
    variables: Optional[Dict[str, Any]] = None,
    cta_distractors_map: Optional[Dict[str, Any]] = None,
    rng: Optional[random.Random] = None,
    rats_map: Optional[Dict[str, str]] = None,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Validate, verify (DAG acyclicity + optional SymPy), format, and shuffle a proof_dag item.

    Returns:
        (compiled_proof_dag, correct_answer)
    """
    if not isinstance(raw_dag, dict):
        raise ValueError("[PROOF-DAG-INVALID] proof_dag payload must be a dictionary.")

    format_fn, sanitize_fn, resolve_rat_fn, is_generic_fn = _get_format_helpers()
    vars_dict = variables if isinstance(variables, dict) else {}
    rats_dict = rats_map if isinstance(rats_map, dict) else {}

    raw_steps = raw_dag.get("steps")
    if not isinstance(raw_steps, list) or not raw_steps:
        raise ValueError("[PROOF-DAG-EMPTY] proof_dag must declare a non-empty 'steps' list.")

    seen_ids: Set[str] = set()
    valid_steps: List[Dict[str, Any]] = []
    fallacy_steps: List[Dict[str, Any]] = []
    compiled_steps: List[Dict[str, Any]] = []

    for idx, step in enumerate(raw_steps):
        if not isinstance(step, dict):
            raise ValueError(f"[PROOF-DAG-STEP] Step at index {idx} must be a dict.")
        sid = str(step.get("id") or f"S{idx + 1}").strip()
        if not sid:
            raise ValueError(f"[PROOF-DAG-STEP] Step at index {idx} has empty id.")
        if sid in seen_ids:
            raise ValueError(f"[PROOF-DAG-DUP-ID] Duplicate step id '{sid}' in proof_dag.")
        seen_ids.add(sid)

        content = _format_text(step.get("content"), vars_dict, format_fn, sanitize_fn)
        if not content:
            raise ValueError(f"[PROOF-DAG-EMPTY-CONTENT] Step '{sid}' has empty content.")

        is_fallacy = bool(step.get("is_fallacy", False))
        justification = _format_text(step.get("justification"), vars_dict, format_fn, sanitize_fn)

        if not is_fallacy:
            _verify_sympy_step(step, sid, vars_dict, format_fn)
            entry: Dict[str, Any] = {
                "id": sid,
                "content": content,
                "is_fallacy": False,
            }
            if justification:
                entry["justification"] = justification
            valid_steps.append(entry)
            compiled_steps.append(entry)
        else:
            did = step.get("distractor_id") or step.get("did")
            did_str = str(did).strip().replace("_", "-") if did else None
            # Inject rats_map fallback before CTA lookup
            step_copy = dict(step)
            if not step_copy.get("error_rationale") and not step_copy.get("rationale"):
                if did_str and did_str in rats_dict:
                    step_copy["error_rationale"] = rats_dict[did_str]
            rat_text = resolve_rat_fn(
                step_copy,
                did_str,
                cta_distractors_map,
                "",
                variables=vars_dict,
            )
            if not rat_text or is_generic_fn(rat_text):
                raise ValueError(
                    f"[PROOF-DAG-RATIONALE] Fallacy step '{sid}' must provide a non-empty diagnostic 'error_rationale'."
                )
            entry = {
                "id": sid,
                "content": content,
                "is_fallacy": True,
                "error_rationale": rat_text,
            }
            if did_str:
                entry["distractor_id"] = did_str
            if justification:
                entry["justification"] = justification
            fallacy_steps.append(entry)
            compiled_steps.append(entry)

    if not (2 <= len(valid_steps) <= 10):
        raise ValueError(
            f"[PROOF-DAG-SIZE] proof_dag must contain between 2 and 10 valid steps (found {len(valid_steps)})."
        )

    valid_id_set = {s["id"] for s in valid_steps}

    # Validate DAG edges and compute topological canonical order via Kahn's algorithm
    raw_edges = raw_dag.get("edges") or []
    if not isinstance(raw_edges, list):
        raise ValueError("[PROOF-DAG-EDGES] 'edges' must be a list of [u, v] pairs.")

    adj: Dict[str, List[str]] = {sid: [] for sid in valid_id_set}
    indegree: Dict[str, int] = {sid: 0 for sid in valid_id_set}
    unique_edges: List[List[str]] = []
    seen_edges: Set[Tuple[str, str]] = set()

    for e_idx, edge in enumerate(raw_edges):
        if not isinstance(edge, (list, tuple)) or len(edge) != 2:
            raise ValueError(f"[PROOF-DAG-EDGE] Edge at index {e_idx} must be a 2-element pair [from, to].")
        u, v = str(edge[0]).strip(), str(edge[1]).strip()
        if u not in valid_id_set or v not in valid_id_set:
            raise ValueError(
                f"[PROOF-DAG-EDGE-REF] Edge [{u}, {v}] must reference valid non-fallacy step IDs."
            )
        if u == v:
            raise ValueError(f"[PROOF-DAG-CYCLE] Self-loop detected on step '{u}'.")
        if (u, v) not in seen_edges:
            seen_edges.add((u, v))
            unique_edges.append([u, v])
            adj[u].append(v)
            indegree[v] += 1

    # Preserve declaration order for tie-breaking in Kahn's algorithm
    valid_order_pos = {s["id"]: i for i, s in enumerate(valid_steps)}
    queue = deque(sorted([sid for sid, deg in indegree.items() if deg == 0], key=lambda x: valid_order_pos[x]))
    canonical_order: List[str] = []

    while queue:
        curr = queue.popleft()
        canonical_order.append(curr)
        next_ready: List[str] = []
        for nxt in adj[curr]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                next_ready.append(nxt)
        if next_ready:
            # Re-sort queue deterministically to preserve declaration order tie-breaking
            combined = list(queue) + next_ready
            combined.sort(key=lambda x: valid_order_pos[x])
            queue = deque(combined)

    if len(canonical_order) != len(valid_steps):
        raise ValueError(
            "[PROOF-DAG-CYCLE] Cycle detected in proof_dag edges; proof prerequisites must form a DAG."
        )

    require_justification = bool(raw_dag.get("require_justification", False))
    raw_bank = raw_dag.get("justification_bank")
    formatted_bank: List[str] = []
    if isinstance(raw_bank, list) and raw_bank:
        seen_j: Set[str] = set()
        for j_item in raw_bank:
            j_fmt = _format_text(j_item, vars_dict, format_fn, sanitize_fn)
            if j_fmt and j_fmt not in seen_j:
                seen_j.add(j_fmt)
                formatted_bank.append(j_fmt)

    if require_justification:
        for s in valid_steps:
            if not s.get("justification"):
                raise ValueError(
                    f"[PROOF-DAG-JUSTIFICATION] Valid step '{s['id']}' missing required 'justification'."
                )
        if not formatted_bank:
            seen_j = set()
            for s in compiled_steps:
                j_val = s.get("justification", "")
                if j_val and j_val not in seen_j:
                    seen_j.add(j_val)
                    formatted_bank.append(j_val)
        else:
            bank_set = set(formatted_bank)
            for s in valid_steps:
                if s["justification"] not in bank_set:
                    formatted_bank.append(s["justification"])
                    bank_set.add(s["justification"])

    goal_text = _format_text(raw_dag.get("goal"), vars_dict, format_fn, sanitize_fn)

    shuffled_steps = list(compiled_steps)
    shuffled_bank = list(formatted_bank)
    if rng is not None:
        rng.shuffle(shuffled_steps)
        if shuffled_bank:
            rng.shuffle(shuffled_bank)

    compiled_dag: Dict[str, Any] = {
        "steps": shuffled_steps,
        "edges": unique_edges,
        "require_justification": require_justification,
    }
    if goal_text:
        compiled_dag["goal"] = goal_text
    if shuffled_bank:
        compiled_dag["justification_bank"] = shuffled_bank

    correct_answer: Dict[str, Any] = {
        "required_step_ids": [s["id"] for s in valid_steps],
        "edges": unique_edges,
        "canonical_order": canonical_order,
    }
    if require_justification:
        correct_answer["justifications"] = {s["id"]: s["justification"] for s in valid_steps}

    return compiled_dag, correct_answer
