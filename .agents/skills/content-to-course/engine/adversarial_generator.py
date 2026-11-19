"""Shift-Left Adversarial Break compiler and witness verifier (`adversarial_break`).

Supports two domain-agnostic submodes:
1. `find_fallacy`: Multi-step derivation containing a deliberate mathematical or logical fallacy
   (e.g., 2nd-order extremum inversion, hidden division by zero, invalid Hessian on discontinuous fn).
2. `counterexample`: Bounded numeric witness discovery where a student submits values satisfying
   all formal predicates (certified at build time via Shift-Left AST predicate evaluation on `sample_witness`).
"""

from __future__ import annotations

import ast
import math
import random
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


_SAFE_FUNCS: Dict[str, Any] = {
    "floor": math.floor,
    "ceil": math.ceil,
    "abs": abs,
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "exp": math.exp,
    "log": math.log,
    "ln": math.log,
    "min": min,
    "max": max,
    "round": round,
    "pow": pow,
}

_SAFE_CONSTS: Dict[str, Any] = {
    "pi": math.pi,
    "e": math.e,
    "True": True,
    "False": False,
    "true": True,
    "false": False,
}


def _eval_ast_node(node: ast.AST, scope: Dict[str, Any]) -> Any:
    if isinstance(node, ast.Expression):
        return _eval_ast_node(node.body, scope)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float, bool)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
    if isinstance(node, ast.Name):
        if node.id in scope:
            return scope[node.id]
        if node.id in _SAFE_CONSTS:
            return _SAFE_CONSTS[node.id]
        raise ValueError(f"Unknown variable '{node.id}' in expression.")
    if isinstance(node, ast.UnaryOp):
        val = _eval_ast_node(node.operand, scope)
        if isinstance(node.op, ast.UAdd):
            return +val
        if isinstance(node.op, ast.USub):
            return -val
        if isinstance(node.op, ast.Not):
            return not bool(val)
        raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
    if isinstance(node, ast.BinOp):
        left = _eval_ast_node(node.left, scope)
        right = _eval_ast_node(node.right, scope)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right
        if isinstance(node.op, ast.FloorDiv):
            return left // right
        if isinstance(node.op, ast.Mod):
            return left % right
        if isinstance(node.op, ast.Pow):
            return left ** right
        raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
    if isinstance(node, ast.BoolOp):
        if isinstance(node.op, ast.And):
            for v in node.values:
                if not bool(_eval_ast_node(v, scope)):
                    return False
            return True
        if isinstance(node.op, ast.Or):
            for v in node.values:
                if bool(_eval_ast_node(v, scope)):
                    return True
            return False
        raise ValueError(f"Unsupported bool operator: {type(node.op).__name__}")
    if isinstance(node, ast.Compare):
        left = _eval_ast_node(node.left, scope)
        for op, comp in zip(node.ops, node.comparators):
            right = _eval_ast_node(comp, scope)
            if isinstance(op, ast.Eq):
                ok = left == right
            elif isinstance(op, ast.NotEq):
                ok = left != right
            elif isinstance(op, ast.Lt):
                ok = left < right
            elif isinstance(op, ast.LtE):
                ok = left <= right
            elif isinstance(op, ast.Gt):
                ok = left > right
            elif isinstance(op, ast.GtE):
                ok = left >= right
            else:
                raise ValueError(f"Unsupported comparison: {type(op).__name__}")
            if not ok:
                return False
            left = right
        return True
    if isinstance(node, ast.IfExp):
        cond = _eval_ast_node(node.test, scope)
        return _eval_ast_node(node.body if cond else node.orelse, scope)
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name) or node.func.id not in _SAFE_FUNCS:
            fn_name = getattr(node.func, "id", type(node.func).__name__)
            raise ValueError(f"Unsupported function call '{fn_name}' in expression.")
        args = [_eval_ast_node(a, scope) for a in node.args]
        return _SAFE_FUNCS[node.func.id](*args)
    raise ValueError(f"Unsupported AST construct: {type(node).__name__}")


def eval_safe_predicate(expr: str, scope: Dict[str, Any]) -> Any:
    """Safely evaluate a mathematical predicate/expression using an AST whitelist."""
    norm = str(expr or "").strip()
    if not norm:
        raise ValueError("Empty expression.")
    # Normalize common JS boolean operators if authored
    norm = norm.replace("&&", " and ").replace("||", " or ")
    tree = ast.parse(norm, mode="eval")
    return _eval_ast_node(tree, scope)


def extract_adversarial_distractor_ids(raw_adv: Any) -> List[str]:
    """Extract all distractor_id references from an adversarial_break payload."""
    if not isinstance(raw_adv, dict):
        return []
    dids: List[str] = []
    seen: Set[str] = set()

    def _add(raw_did: Any) -> None:
        if isinstance(raw_did, str) and raw_did.strip():
            norm = raw_did.strip().replace("_", "-")
            if norm not in seen:
                seen.add(norm)
                dids.append(norm)

    for step in raw_adv.get("steps") or []:
        if isinstance(step, dict):
            _add(step.get("distractor_id") or step.get("did"))
    for opt in raw_adv.get("reason_options") or []:
        if isinstance(opt, dict):
            _add(opt.get("distractor_id") or opt.get("did"))
    for tp in raw_adv.get("trap_predicates") or []:
        if isinstance(tp, dict):
            _add(tp.get("distractor_id") or tp.get("did"))
    for p in raw_adv.get("predicates") or []:
        if isinstance(p, dict):
            _add(p.get("distractor_id") or p.get("did"))

    return dids


def compile_and_verify_adversarial(
    raw_adv: Dict[str, Any],
    variables: Optional[Dict[str, Any]] = None,
    cta_distractors_map: Optional[Dict[str, Any]] = None,
    rng: Optional[random.Random] = None,
    rats_map: Optional[Dict[str, str]] = None,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Validate, verify, format, and assemble an adversarial_break payload.

    Returns:
        (compiled_adversarial_break, correct_answer)
    """
    if not isinstance(raw_adv, dict):
        raise ValueError("[ADV-INVALID] adversarial_break payload must be a dictionary.")

    format_fn, sanitize_fn, resolve_rat_fn, is_generic_fn = _get_format_helpers()
    vars_dict = variables if isinstance(variables, dict) else {}
    rats_dict = rats_map if isinstance(rats_map, dict) else {}

    mode = str(raw_adv.get("mode") or "find_fallacy").strip().lower()
    if mode not in ("find_fallacy", "counterexample"):
        raise ValueError(f"[ADV-MODE] Invalid adversarial_break mode '{mode}'; expected 'find_fallacy' or 'counterexample'.")

    if mode == "find_fallacy":
        raw_steps = raw_adv.get("steps")
        if not isinstance(raw_steps, list) or len(raw_steps) < 2:
            raise ValueError("[ADV-STEPS] find_fallacy mode requires at least 2 derivation steps.")

        compiled_steps: List[Dict[str, Any]] = []
        fallacy_ids: List[str] = []
        seen_sids: Set[str] = set()

        for idx, step in enumerate(raw_steps):
            if not isinstance(step, dict):
                raise ValueError(f"[ADV-STEP] Step at index {idx} must be a dict.")
            sid = str(step.get("id") or f"A{idx + 1}").strip()
            if not sid or sid in seen_sids:
                raise ValueError(f"[ADV-STEP-ID] Missing or duplicate step id '{sid}'.")
            seen_sids.add(sid)

            label = _format_text(step.get("label") or f"Paso {idx + 1}", vars_dict, format_fn, sanitize_fn)
            content = _format_text(step.get("content"), vars_dict, format_fn, sanitize_fn)
            if not content:
                raise ValueError(f"[ADV-STEP-EMPTY] Step '{sid}' has empty content.")

            is_fallacy = bool(step.get("is_fallacy", False))
            did = step.get("distractor_id") or step.get("did")
            did_str = str(did).strip().replace("_", "-") if did else None

            if is_fallacy:
                fallacy_ids.append(sid)
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
                        f"[ADV-FALLACY-RATIONALE] Fallacy step '{sid}' must provide a non-empty diagnostic 'error_rationale'."
                    )
                entry: Dict[str, Any] = {
                    "id": sid,
                    "label": label,
                    "content": content,
                    "is_fallacy": True,
                    "error_rationale": rat_text,
                }
                if did_str:
                    entry["distractor_id"] = did_str
            else:
                entry = {
                    "id": sid,
                    "label": label,
                    "content": content,
                    "is_fallacy": False,
                }
                valid_exp = _format_text(step.get("valid_explanation"), vars_dict, format_fn, sanitize_fn)
                if valid_exp:
                    entry["valid_explanation"] = valid_exp
            compiled_steps.append(entry)

        if len(fallacy_ids) != 1:
            raise ValueError(
                f"[ADV-FALLACY-COUNT] find_fallacy requires exactly 1 step with is_fallacy=True (found {len(fallacy_ids)})."
            )

        compiled_reasons: List[Dict[str, Any]] = []
        correct_reason_id: Optional[str] = None
        raw_reasons = raw_adv.get("reason_options")
        if isinstance(raw_reasons, list) and len(raw_reasons) > 0:
            correct_reasons = 0
            false_reasons = 0
            seen_rids: Set[str] = set()
            for r_idx, opt in enumerate(raw_reasons):
                if not isinstance(opt, dict):
                    raise ValueError(f"[ADV-REASON] reason_options[{r_idx}] must be a dict.")
                rid = str(opt.get("id") or f"R{r_idx + 1}").strip()
                if not rid or rid in seen_rids:
                    raise ValueError(f"[ADV-REASON-ID] Missing or duplicate reason id '{rid}'.")
                seen_rids.add(rid)
                r_content = _format_text(opt.get("content") or opt.get("value"), vars_dict, format_fn, sanitize_fn)
                if not r_content:
                    raise ValueError(f"[ADV-REASON-EMPTY] Reason '{rid}' has empty content.")
                is_corr = bool(opt.get("is_correct", False))
                r_entry: Dict[str, Any] = {
                    "id": rid,
                    "content": r_content,
                    "is_correct": is_corr,
                }
                if is_corr:
                    correct_reasons += 1
                    correct_reason_id = rid
                else:
                    false_reasons += 1
                    did = opt.get("distractor_id") or opt.get("did")
                    did_str = str(did).strip().replace("_", "-") if did else None
                    opt_copy = dict(opt)
                    if not opt_copy.get("error_rationale") and not opt_copy.get("rationale"):
                        if did_str and did_str in rats_dict:
                            opt_copy["error_rationale"] = rats_dict[did_str]
                    rat_text = resolve_rat_fn(
                        opt_copy,
                        did_str,
                        cta_distractors_map,
                        "",
                        variables=vars_dict,
                    )
                    if not rat_text or is_generic_fn(rat_text):
                        raise ValueError(
                            f"[ADV-REASON-RATIONALE] Incorrect reason option '{rid}' requires a non-empty 'error_rationale'."
                        )
                    r_entry["error_rationale"] = rat_text
                    if did_str:
                        r_entry["distractor_id"] = did_str
                compiled_reasons.append(r_entry)

            if correct_reasons != 1 or false_reasons < 1:
                raise ValueError(
                    f"[ADV-REASON-COUNT] reason_options requires 1 correct and >= 1 false options (got {correct_reasons} true, {false_reasons} false)."
                )
            if rng is not None:
                rng.shuffle(compiled_reasons)

        compiled_adv: Dict[str, Any] = {
            "mode": "find_fallacy",
            "steps": compiled_steps,
        }
        if compiled_reasons:
            compiled_adv["reason_options"] = compiled_reasons

        correct_answer: Dict[str, Any] = {
            "mode": "find_fallacy",
            "fallacy_step_id": fallacy_ids[0],
        }
        if correct_reason_id:
            correct_answer["correct_reason_id"] = correct_reason_id

        return compiled_adv, correct_answer

    # mode == "counterexample"
    raw_inputs = raw_adv.get("inputs")
    raw_preds = raw_adv.get("predicates")
    sample_witness = raw_adv.get("sample_witness")
    if not isinstance(raw_inputs, list) or not raw_inputs:
        raise ValueError("[ADV-CE-INPUTS] counterexample mode requires non-empty 'inputs'.")
    if not isinstance(raw_preds, list) or not raw_preds:
        raise ValueError("[ADV-CE-PREDS] counterexample mode requires non-empty 'predicates'.")
    if not isinstance(sample_witness, dict) or not sample_witness:
        raise ValueError("[ADV-CE-WITNESS] counterexample mode requires 'sample_witness' dictionary.")

    compiled_inputs: List[Dict[str, Any]] = []
    witness_scope: Dict[str, float] = {}
    for k, v in vars_dict.items():
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            witness_scope[str(k)] = float(v)

    for idx, inp in enumerate(raw_inputs):
        if not isinstance(inp, dict):
            raise ValueError(f"[ADV-CE-INPUT] input[{idx}] must be a dict.")
        iid = str(inp.get("id") or inp.get("name") or f"x{idx + 1}").strip()
        if not iid:
            raise ValueError(f"[ADV-CE-INPUT] input[{idx}] has empty id.")
        if iid not in sample_witness:
            raise ValueError(f"[ADV-WITNESS-MISSING] sample_witness missing value for input '{iid}'.")
        try:
            w_val = float(sample_witness[iid])
        except (TypeError, ValueError) as exc:
            raise ValueError(f"[ADV-WITNESS-TYPE] sample_witness['{iid}'] must be numeric.") from exc
        if not math.isfinite(w_val):
            raise ValueError(f"[ADV-WITNESS-FINITE] sample_witness['{iid}'] must be finite.")

        inp_min = inp.get("min")
        inp_max = inp.get("max")
        if inp_min is not None and w_val < float(inp_min):
            raise ValueError(f"[ADV-WITNESS-BOUNDS] sample_witness['{iid}']={w_val} < min {inp_min}.")
        if inp_max is not None and w_val > float(inp_max):
            raise ValueError(f"[ADV-WITNESS-BOUNDS] sample_witness['{iid}']={w_val} > max {inp_max}.")

        witness_scope[iid] = w_val
        c_inp: Dict[str, Any] = {
            "id": iid,
            "label": _format_text(inp.get("label") or iid, vars_dict, format_fn, sanitize_fn),
        }
        if inp.get("placeholder") is not None:
            c_inp["placeholder"] = _format_text(inp.get("placeholder"), vars_dict, format_fn, sanitize_fn)
        if inp_min is not None:
            c_inp["min"] = float(inp_min)
        if inp_max is not None:
            c_inp["max"] = float(inp_max)
        if inp.get("step") is not None:
            c_inp["step"] = float(inp["step"])
        compiled_inputs.append(c_inp)

    compiled_preds: List[Dict[str, Any]] = []
    for p_idx, pred in enumerate(raw_preds):
        if not isinstance(pred, dict):
            raise ValueError(f"[ADV-CE-PRED] predicates[{p_idx}] must be a dict.")
        pid = str(pred.get("id") or f"P{p_idx + 1}").strip()
        expr_raw = format_fn(str(pred.get("expr") or ""), vars_dict) if vars_dict else str(pred.get("expr") or "")
        expr_str = expr_raw.strip()
        if not expr_str:
            raise ValueError(f"[ADV-CE-PRED] Predicate '{pid}' has empty 'expr'.")

        # Certify Shift-Left on sample_witness
        try:
            ok = bool(eval_safe_predicate(expr_str, witness_scope))
        except Exception as exc:
            raise ValueError(f"[ADV-WITNESS-EVAL] Predicate '{pid}' ({expr_str}) failed evaluation: {exc}") from exc
        if not ok:
            raise ValueError(
                f"[ADV-WITNESS-INVALID] sample_witness {sample_witness} failed predicate '{pid}' ({expr_str})."
            )

        desc = _format_text(pred.get("description") or expr_str, vars_dict, format_fn, sanitize_fn)
        did = pred.get("distractor_id") or pred.get("did")
        did_str = str(did).strip().replace("_", "-") if did else None
        pred_copy = dict(pred)
        if not pred_copy.get("error_rationale") and not pred_copy.get("failure_rationale"):
            if did_str and did_str in rats_dict:
                pred_copy["error_rationale"] = rats_dict[did_str]
        elif pred_copy.get("failure_rationale") and not pred_copy.get("error_rationale"):
            pred_copy["error_rationale"] = pred_copy["failure_rationale"]

        fail_rat = resolve_rat_fn(
            pred_copy,
            did_str,
            cta_distractors_map,
            f"El contraejemplo ingresado no satisface la condición {desc}.",
            variables=vars_dict,
        )
        c_pred: Dict[str, Any] = {
            "id": pid,
            "expr": expr_str,
            "description": desc,
            "failure_rationale": fail_rat,
        }
        if did_str:
            c_pred["distractor_id"] = did_str
        compiled_preds.append(c_pred)

    compiled_traps: List[Dict[str, Any]] = []
    for t_idx, tp in enumerate(raw_adv.get("trap_predicates") or []):
        if not isinstance(tp, dict):
            continue
        t_expr = format_fn(str(tp.get("expr") or ""), vars_dict) if vars_dict else str(tp.get("expr") or "")
        t_expr = t_expr.strip()
        if not t_expr:
            continue
        try:
            hit_trap = bool(eval_safe_predicate(t_expr, witness_scope))
        except Exception as exc:
            raise ValueError(f"[ADV-TRAP-EVAL] trap_predicates[{t_idx}] ({t_expr}) failed evaluation: {exc}") from exc
        if hit_trap:
            raise ValueError(
                f"[ADV-WITNESS-TRAP] sample_witness {sample_witness} triggered trap_predicate '{t_expr}'."
            )
        did = tp.get("distractor_id") or tp.get("did")
        did_str = str(did).strip().replace("_", "-") if did else None
        tp_copy = dict(tp)
        if not tp_copy.get("error_rationale") and did_str and did_str in rats_dict:
            tp_copy["error_rationale"] = rats_dict[did_str]
        t_rat = resolve_rat_fn(tp_copy, did_str, cta_distractors_map, "", variables=vars_dict)
        if not t_rat:
            raise ValueError(f"[ADV-TRAP-RATIONALE] trap_predicates[{t_idx}] missing 'error_rationale'.")
        c_tp: Dict[str, Any] = {"expr": t_expr, "error_rationale": t_rat}
        if did_str:
            c_tp["distractor_id"] = did_str
        compiled_traps.append(c_tp)

    # Optional non_witness sanity check (must fail at least one predicate)
    non_witness = raw_adv.get("non_witness")
    if isinstance(non_witness, dict) and non_witness:
        nw_scope = dict(witness_scope)
        for k, v in non_witness.items():
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                nw_scope[str(k)] = float(v)
        all_ok = all(bool(eval_safe_predicate(p["expr"], nw_scope)) for p in compiled_preds)
        if all_ok:
            raise ValueError(
                f"[ADV-NON-WITNESS-PASSED] Declared non_witness {non_witness} unexpectedly satisfied all predicates."
            )

    compiled_readouts: List[Dict[str, Any]] = []
    for r_idx, ro in enumerate(raw_adv.get("computed_readouts") or []):
        if not isinstance(ro, dict):
            continue
        r_expr = format_fn(str(ro.get("expr") or ""), vars_dict) if vars_dict else str(ro.get("expr") or "")
        r_expr = r_expr.strip()
        if not r_expr:
            continue
        try:
            _ = eval_safe_predicate(r_expr, witness_scope)
        except Exception as exc:
            raise ValueError(f"[ADV-READOUT-EVAL] computed_readouts[{r_idx}] ({r_expr}) failed: {exc}") from exc
        compiled_readouts.append({
            "label": _format_text(ro.get("label") or r_expr, vars_dict, format_fn, sanitize_fn),
            "expr": r_expr,
        })

    clean_witness = {k: sample_witness[k] for k in [i["id"] for i in compiled_inputs]}
    compiled_adv = {
        "mode": "counterexample",
        "inputs": compiled_inputs,
        "predicates": compiled_preds,
        "sample_witness": clean_witness,
    }
    if compiled_traps:
        compiled_adv["trap_predicates"] = compiled_traps
    if compiled_readouts:
        compiled_adv["computed_readouts"] = compiled_readouts

    correct_answer = {
        "mode": "counterexample",
        "sample_witness": clean_witness,
    }
    return compiled_adv, correct_answer
