"""Canonical, sandbox-safe verification helpers (`c2c_ver`) for Form-C shard templates.

Injected automatically into shard execution globals and sandbox verification
environments so shard authors only supply domain math/logic while structural
safety, mutation refutation, KaTeX number parsing, and transcendental equivalence
checks are enforced deterministically.
"""

from __future__ import annotations

import functools
import math
import re
from typing import Any, Dict, Iterable, Optional, Tuple

_SYMPY_BUILTINS = frozenset({
    "ln", "log", "sin", "cos", "tan", "cot", "sec", "csc",
    "asin", "acos", "atan", "sinh", "cosh", "tanh",
    "exp", "sqrt", "abs", "pi", "e",
})
_SYMPY_BUILTIN_RE = "|".join(sorted(_SYMPY_BUILTINS - {"e", "pi"}, key=len, reverse=True))


def _normalize_sympy_expr(expr: str, var_names: Tuple[str, ...]) -> str:
    """Split adjacent variable+builtin (e.g. xln(x)) and adjacent declared vars (e.g. 12tv)."""
    out = expr
    if var_names:
        # Split <var><builtin>( -> <var>*<builtin>(
        for v in sorted(var_names, key=len, reverse=True):
            if v in _SYMPY_BUILTINS or not v.isalpha():
                continue
            out = re.sub(
                rf"(?<![a-zA-Z_])({re.escape(v)})({_SYMPY_BUILTIN_RE})(?=\s*\()",
                r"\1*\2",
                out,
            )
            # Also split <var>e^ -> <var>*e^
            if v != "e":
                out = re.sub(
                    rf"(?<![a-zA-Z_])({re.escape(v)})(e)(?=\s*[\^*])",
                    r"\1*\2",
                    out,
                )
        # Split adjacent single-char declared vars inside unknown identifiers (e.g., tv -> t*v, xy -> x*y)
        single_vars = {v for v in var_names if len(v) == 1 and v.isalpha()}
        multi_vars = set(var_names) - single_vars
        if len(single_vars) >= 2:
            def _split_tok(m: re.Match[str]) -> str:
                tok = m.group(0)
                if tok in var_names or tok in _SYMPY_BUILTINS or tok in multi_vars:
                    return tok
                if all(ch in single_vars for ch in tok):
                    return "*".join(tok)
                return tok
            out = re.sub(r"(?<![a-zA-Z_])[a-zA-Z_][a-zA-Z0-9_]*\b", _split_tok, out)
    return out

from engine.template_healing import parse_katex_number

_BAD_SENTINELS = frozenset({
    "__MUTATED__",
    "$0 = 1$",
    "$1 = 2$",
    "0 = 1",
    "1 = 2",
})

_MULTI_POINT_GRID = (0.3713, 1.1927, 2.4183)


def _to_finite_float(val: Any) -> Optional[float]:
    if val is None or isinstance(val, (bool, dict, list, tuple, set)):
        return None
    try:
        num = float(val)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(num):
        return None
    return num


def _ver_numeric(candidate: Any, exact: Any, tol: float = 0.005) -> bool:
    """Verify numeric equivalence between a candidate answer (number or KaTeX string) and exact value."""
    if candidate is None or isinstance(candidate, (bool, dict, list, tuple, set)):
        return False
    if isinstance(candidate, str) and not candidate.strip():
        return False
    if isinstance(exact, bool):
        return False

    exact_f = _to_finite_float(exact)
    if exact_f is None:
        return False

    try:
        cand_f = float(parse_katex_number(candidate))
    except Exception:
        return False

    if not math.isfinite(cand_f):
        return False
    return abs(cand_f - exact_f) <= float(tol)


_SYMPY_PARSER_CTX: Optional[Tuple[Any, Any, Any, Dict[str, Any]]] = None


def _get_sympy_parser_ctx() -> Tuple[Any, Any, Any, Dict[str, Any]]:
    """Lazily initialize sympy, parse_expr, transforms, and a reusable global_dict once.

    Avoids sympy.parsing.sympy_parser.parse_expr executing `from sympy import *` on every call.
    """
    global _SYMPY_PARSER_CTX
    if _SYMPY_PARSER_CTX is None:
        import sympy
        from sympy.parsing.sympy_parser import (
            convert_xor,
            implicit_multiplication_application,
            parse_expr,
            standard_transformations,
        )

        global_dict: Dict[str, Any] = {}
        exec("from sympy import *", global_dict)
        transforms = standard_transformations + (implicit_multiplication_application, convert_xor)
        _SYMPY_PARSER_CTX = (sympy, parse_expr, transforms, global_dict)
    return _SYMPY_PARSER_CTX


@functools.lru_cache(maxsize=4096)
def _ver_equiv_cached(
    cand_s: str,
    exp_s: str,
    var_names: Tuple[str, ...],
    tol_f: float,
) -> bool:
    sympy, parse_expr, transforms, base_globals = _get_sympy_parser_ctx()

    sym_locals: Dict[str, Any] = {vn: sympy.Symbol(vn) for vn in var_names}
    sym_locals.setdefault("ln", sympy.log)
    sym_locals.setdefault("e", sympy.E)
    sym_locals.setdefault("pi", sympy.pi)

    norm_cand = _normalize_sympy_expr(cand_s, var_names)
    norm_exp = _normalize_sympy_expr(exp_s, var_names)
    try:
        c_expr = parse_expr(
            norm_cand,
            local_dict=sym_locals,
            global_dict=base_globals.copy(),
            transformations=transforms,
        )
        e_expr = parse_expr(
            norm_exp,
            local_dict=sym_locals,
            global_dict=base_globals.copy(),
            transformations=transforms,
        )
    except Exception:
        return False

    if c_expr is None or e_expr is None:
        return False

    allowed_syms = set(sym_locals.values()) | e_expr.free_symbols
    if var_names and (c_expr.free_symbols - allowed_syms):
        return False

    if c_expr == e_expr:
        return True

    eval_syms = (
        [sym_locals[vn] for vn in var_names]
        if var_names
        else sorted(c_expr.free_symbols | e_expr.free_symbols, key=lambda s: s.name)
    )

    if not eval_syms:
        try:
            cv = complex(c_expr.evalf())
            ev = complex(e_expr.evalf())
        except Exception:
            cv = ev = None
        if (
            cv is not None
            and ev is not None
            and abs(cv.imag) <= 1e-9
            and abs(ev.imag) <= 1e-9
            and math.isfinite(cv.real)
            and math.isfinite(ev.real)
        ):
            if abs(cv.real - ev.real) <= tol_f * max(1.0, abs(ev.real)):
                return True
            if abs(cv.real - ev.real) > max(1e-3, 10.0 * tol_f) * max(1.0, abs(ev.real), abs(cv.real)):
                return False
        try:
            return sympy.simplify(c_expr - e_expr) == 0
        except Exception:
            return False

    valid_points = 0
    near_miss = False
    for pt_idx, base_val in enumerate(_MULTI_POINT_GRID):
        subs = {
            sym: base_val + (0.07 * s_idx) + (0.03 * pt_idx if s_idx > 0 else 0.0)
            for s_idx, sym in enumerate(eval_syms)
        }
        try:
            cv = complex(c_expr.evalf(subs=subs))
            ev = complex(e_expr.evalf(subs=subs))
        except Exception:
            continue
        if abs(cv.imag) > 1e-9 or abs(ev.imag) > 1e-9:
            continue
        if not (math.isfinite(cv.real) and math.isfinite(ev.real)):
            continue
        diff_abs = abs(cv.real - ev.real)
        if diff_abs > max(1e-3, 10.0 * tol_f) * max(1.0, abs(ev.real), abs(cv.real)):
            return False
        if diff_abs > tol_f * max(1.0, abs(ev.real)):
            near_miss = True
            break
        valid_points += 1

    if not near_miss and valid_points >= 2:
        return True

    try:
        if sympy.simplify(c_expr - e_expr) == 0:
            return True
    except Exception:
        pass
    return False


def _ver_equiv(
    candidate: Any,
    expected: Any,
    variables: Optional[Iterable[str]] = None,
    tol: float = 1e-4,
) -> bool:
    """Verify symbolic/algebraic equivalence using SymPy plus transcendental multi-point fallback."""
    if candidate is None or isinstance(candidate, (bool, dict, list, tuple, set)):
        return False
    if expected is None or isinstance(expected, (bool, dict, list, tuple, set)):
        return False

    cand_s = str(candidate).strip()
    exp_s = str(expected).strip()
    if not cand_s or not exp_s or cand_s == "__MUTATED__":
        return False
    if "=" in cand_s or "=" in exp_s:
        return False

    var_names = tuple(str(v).strip() for v in (variables or []) if str(v).strip())
    return _ver_equiv_cached(cand_s, exp_s, var_names, float(tol))


def _has_bad_sentinel(val: Any) -> bool:
    return isinstance(val, str) and val.strip() in _BAD_SENTINELS


def _check_distractor_entry(
    entry: Any,
    rats: Optional[Dict[str, str]] = None,
    *,
    require_inline_rationale: bool = False,
) -> bool:
    if not isinstance(entry, dict):
        return False
    did_raw = entry.get("distractor_id") or entry.get("id") or entry.get("did")
    if not isinstance(did_raw, str):
        return False
    did = did_raw.strip()
    if not did or did == "__INVALID_DID__":
        return False
    norm_did = did.replace("_", "-")
    if isinstance(rats, dict) and len(rats) > 0:
        if did not in rats and norm_did not in rats:
            return False

    has_rat_key = ("error_rationale" in entry) or ("rationale" in entry)
    rat_raw = entry.get("error_rationale")
    if rat_raw is None:
        rat_raw = entry.get("rationale")

    if require_inline_rationale or has_rat_key:
        if not isinstance(rat_raw, str):
            return False
        rat_s = rat_raw.strip()
        if len(rat_s) < 20 or rat_s in _BAD_SENTINELS:
            return False
    elif isinstance(rats, dict):
        fallback_rat = rats.get(did) or rats.get(norm_did) or ""
        if not isinstance(fallback_rat, str) or len(fallback_rat.strip()) < 20:
            return False
    else:
        return False

    return True


def _ver_m20_guard(
    r: Any,
    rats: Optional[Dict[str, str]] = None,
    qtype: Optional[str] = None,
    expected_correct_count: Optional[int] = None,
) -> bool:
    """Validate structural integrity and adversarial mutation rejection for MS and M20 payloads."""
    if not isinstance(r, dict):
        return False
    vars_dict = r.get("vars")
    if not isinstance(vars_dict, dict) or len(vars_dict) == 0:
        return False

    norm_qt = str(qtype or "").strip().lower()
    if not norm_qt:
        if isinstance(r.get("options"), list):
            norm_qt = "multiple_select"
        else:
            for key in (
                "proof_dag",
                "adversarial_break",
                "unstructured_model",
                "concept_matching",
            ):
                if isinstance(r.get(key), dict):
                    norm_qt = key
                    break

    if norm_qt in ("ms", "multiple_select"):
        opts = r.get("options")
        if not isinstance(opts, list) or len(opts) != 7:
            return False
        true_opts = []
        false_opts = []
        for opt in opts:
            if not isinstance(opt, dict):
                return False
            is_corr = opt.get("is_correct")
            if not isinstance(is_corr, bool):
                return False
            txt = opt.get("value") if "value" in opt else opt.get("content")
            if not isinstance(txt, str) or not txt.strip() or _has_bad_sentinel(txt):
                return False
            if is_corr:
                if opt.get("distractor_id") or opt.get("did"):
                    return False
                true_opts.append(opt)
            else:
                if not _check_distractor_entry(opt, rats, require_inline_rationale=True):
                    return False
                false_opts.append(opt)
        if not (2 <= len(true_opts) <= 5) or not false_opts:
            return False
        if expected_correct_count is not None and len(true_opts) != int(expected_correct_count):
            return False
        return True

    if norm_qt == "proof_dag":
        pd = r.get("proof_dag") or r.get("dag")
        if not isinstance(pd, dict):
            return False
        steps = pd.get("steps")
        edges = pd.get("edges")
        if not isinstance(steps, list) or not isinstance(edges, list) or len(edges) < 1:
            return False
        valid_steps = 0
        for step in steps:
            if not isinstance(step, dict):
                return False
            sid = step.get("id")
            content = step.get("content")
            if not isinstance(sid, str) or not sid.strip():
                return False
            if not isinstance(content, str) or not content.strip() or _has_bad_sentinel(content):
                return False
            if step.get("is_fallacy") is True:
                if not _check_distractor_entry(step, rats):
                    return False
            else:
                valid_steps += 1
        return valid_steps >= 3

    if norm_qt == "adversarial_break":
        adv = r.get("adversarial_break") or r.get("adversarial")
        if not isinstance(adv, dict):
            return False
        mode = str(adv.get("mode") or "").strip().lower()
        if mode == "find_fallacy":
            steps = adv.get("steps")
            if not isinstance(steps, list) or len(steps) < 3:
                return False
            fallacy_count = 0
            for step in steps:
                if not isinstance(step, dict):
                    return False
                content = step.get("content")
                if not isinstance(content, str) or not content.strip() or _has_bad_sentinel(content):
                    return False
                if step.get("is_fallacy") is True:
                    fallacy_count += 1
                    if not _check_distractor_entry(step, rats):
                        return False
            if fallacy_count < 1:
                return False
            reason_opts = adv.get("reason_options")
            if isinstance(reason_opts, list) and reason_opts:
                has_true = False
                for ro in reason_opts:
                    if not isinstance(ro, dict):
                        return False
                    r_txt = ro.get("content") or ro.get("value")
                    if not isinstance(r_txt, str) or not r_txt.strip() or _has_bad_sentinel(r_txt):
                        return False
                    if ro.get("is_correct") is True:
                        has_true = True
                    elif ro.get("is_correct") is False:
                        if not _check_distractor_entry(ro, rats):
                            return False
                if not has_true:
                    return False
            return True

        if mode == "counterexample":
            inputs = adv.get("inputs")
            predicates = adv.get("predicates")
            witness = adv.get("sample_witness")
            if (
                not isinstance(inputs, list) or not inputs
                or not isinstance(predicates, list) or not predicates
                or not isinstance(witness, dict) or not witness
            ):
                return False
            for pred in predicates:
                if not isinstance(pred, dict):
                    return False
                expr = pred.get("expr")
                if not isinstance(expr, str) or not expr.strip() or _has_bad_sentinel(expr):
                    return False
            for trap in (adv.get("trap_predicates") or []):
                if not isinstance(trap, dict):
                    return False
                expr = trap.get("expr")
                if not isinstance(expr, str) or not expr.strip() or _has_bad_sentinel(expr):
                    return False
                if not _check_distractor_entry(trap, rats):
                    return False
            return True

        return False

    if norm_qt == "unstructured_model":
        um = r.get("unstructured_model") or r.get("stage0")
        if not isinstance(um, dict):
            return False
        p1 = um.get("phase1_variables")
        p2 = um.get("phase2_assumptions")
        p3 = um.get("phase3_formulation")
        if not (isinstance(p1, dict) and isinstance(p2, dict) and isinstance(p3, dict)):
            return False
        p1_items = p1.get("items")
        p2_opts = p2.get("options")
        if not isinstance(p1_items, list) or not p1_items or not isinstance(p2_opts, list) or not p2_opts:
            return False
        for item in p1_items:
            if not isinstance(item, dict):
                return False
            lbl = item.get("label")
            if not isinstance(lbl, str) or not lbl.strip() or _has_bad_sentinel(lbl):
                return False
            if item.get("distractor_id") or item.get("did"):
                if not _check_distractor_entry(item, rats):
                    return False
        for opt in p2_opts:
            if not isinstance(opt, dict):
                return False
            content = opt.get("content") or opt.get("value")
            if not isinstance(content, str) or not content.strip() or _has_bad_sentinel(content):
                return False
            if opt.get("is_required") is False:
                if not _check_distractor_entry(opt, rats):
                    return False
        input_mode = str(p3.get("input_mode") or "").strip().lower()
        if input_mode == "symbolic":
            ce = p3.get("correct_expression")
            expr = ce.get("expression") if isinstance(ce, dict) else None
            if not isinstance(expr, str) or not expr.strip() or _has_bad_sentinel(expr):
                return False
        elif input_mode == "select":
            p3_opts = p3.get("options")
            if not isinstance(p3_opts, list) or not p3_opts:
                return False
            has_true = False
            for opt in p3_opts:
                if not isinstance(opt, dict):
                    return False
                content = opt.get("content") or opt.get("value")
                if not isinstance(content, str) or not content.strip() or _has_bad_sentinel(content):
                    return False
                if opt.get("is_correct") is True:
                    has_true = True
                elif opt.get("is_correct") is False:
                    if not _check_distractor_entry(opt, rats):
                        return False
            if not has_true:
                return False
        else:
            return False
        return True

    if norm_qt == "concept_matching":
        cm = r.get("concept_matching") or r.get("matching")
        if not isinstance(cm, dict):
            return False
        premises = cm.get("premises")
        targets = cm.get("targets")
        correct_pairs = cm.get("correct_pairs")
        if (
            not isinstance(premises, list) or not premises
            or not isinstance(targets, list) or not targets
            or not isinstance(correct_pairs, dict) or not correct_pairs
        ):
            return False
        for p in premises:
            if not isinstance(p, dict):
                return False
            content = p.get("content")
            if not isinstance(content, str) or not content.strip() or _has_bad_sentinel(content):
                return False
        matched_tids = set(correct_pairs.values())
        for tg in targets:
            if not isinstance(tg, dict):
                return False
            tid = tg.get("id")
            content = tg.get("content")
            if not isinstance(content, str) or not content.strip() or _has_bad_sentinel(content):
                return False
            is_dist = (tg.get("is_distractor") is True) or (tid not in matched_tids)
            if is_dist:
                if not _check_distractor_entry(tg, rats):
                    return False
        return True

    return False


class _ReadOnlyC2CVer:
    """Read-only proxy exposing canonical c2c_ver verifier helpers safely in sandbox."""

    __slots__ = ()

    _ALLOWED = frozenset({"numeric", "equiv", "m20_guard"})

    def __getattribute__(self, name: str) -> Any:
        if name == "numeric":
            return _ver_numeric
        if name == "equiv":
            return _ver_equiv
        if name == "m20_guard":
            return _ver_m20_guard
        raise AttributeError(f"c2c_ver has no accessible attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError("c2c_ver is read-only")

    def __delattr__(self, name: str) -> None:
        raise AttributeError("c2c_ver is read-only")

    def __repr__(self) -> str:
        return "<c2c_ver read-only helpers: numeric, equiv, m20_guard>"


c2c_ver = _ReadOnlyC2CVer()
numeric = _ver_numeric
equiv = _ver_equiv
m20_guard = _ver_m20_guard
