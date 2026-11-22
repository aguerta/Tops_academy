"""Tests for M16 Phase 1 shadow-mode [Z3-RULE-WARNING] anti-clone fallback."""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import List

import sympy

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOT = REPO_ROOT / ".agents" / "skills" / "content-to-course"
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

from engine.shard_ast_transforms import (
    _check_intra_competency_anti_clone,
    _z3_check_sympy_equiv,
)


def test_z3_helper_positive_domain_and_fallbacks():
    """Z3 proves equivalence under positive domain and safely skips transcendentals."""
    x0 = sympy.Symbol("x0", real=True)
    x1 = sympy.Symbol("x1", real=True)

    # Under real=True without positive=True, Abs(x0) - x0 does not reduce to 0 in SymPy,
    # whereas under Z3's positive domain (x0 > 0) they are provably equal (unsat).
    assert _z3_check_sympy_equiv(sympy.Abs(x0) + x0 * x1, x0 + x0 * x1) is True
    assert _z3_check_sympy_equiv(sympy.sqrt(x0**2 * x1), x0 * sympy.sqrt(x1)) is True

    # Genuinely distinct expressions must return False (sat counterexample).
    assert _z3_check_sympy_equiv(x0 + x1, x0 * x1) is False

    # Transcendental functions must fall back silently to None without raising.
    assert _z3_check_sympy_equiv(sympy.exp(x0), sympy.exp(x0 + 0)) is None
    assert _z3_check_sympy_equiv(sympy.log(x0 * x1), sympy.log(x0) + sympy.log(x1)) is None


def test_anti_clone_emits_non_blocking_z3_warning_on_sympy_miss(caplog):
    """Equivalent positive-domain formulas missed by SymPy emit [Z3-RULE-WARNING] with zero blocking errors."""
    gen_a = (
        "def generate(rng):\n"
        "    a = rng.randint(2, 10)\n"
        "    b = rng.randint(2, 10)\n"
        "    ans = sqrt(a * a * b)\n"
        "    return {'vars': {'a': a, 'b': b, 'ans': ans}, 'correct': str(ans)}\n"
    )
    gen_b = (
        "def generate(rng):\n"
        "    a = rng.randint(2, 10)\n"
        "    b = rng.randint(2, 10)\n"
        "    ans = a * sqrt(b)\n"
        "    return {'vars': {'a': a, 'b': b, 'ans': ans}, 'correct': str(ans)}\n"
    )
    tpls = [
        {
            "id": "T-C01-01",
            "interaction_type": "fill_in_the_blank",
            "archetype": "direct",
            "difficulty": "easy",
            "bloom": "apply",
            "stem_variants": ["Calcula la norma reducida dado lado @a@ y factor @b@."],
            "generator_code": gen_a,
        },
        {
            "id": "T-C01-02",
            "interaction_type": "fill_in_the_blank",
            "archetype": "direct",
            "difficulty": "medium",
            "bloom": "analyze",
            "stem_variants": ["Determina la magnitud escalada correspondiente a @a@ y parámetro @b@."],
            "generator_code": gen_b,
        },
    ]

    warnings_out: List[str] = []
    with caplog.at_level(logging.WARNING):
        errors = _check_intra_competency_anti_clone(
            cid="C-01",
            source_name="C-01.json",
            tpls=tpls,
            gen_callables=[None, None],
            cid_ast_funcs={},
            eff_k=2,
            norm_shard_id="shard_01",
            warnings_out=warnings_out,
        )

    assert errors == [], f"Shadow mode must never block pipeline; got errors={errors}"
    assert len(warnings_out) == 1
    assert "[Z3-RULE-WARNING]" in warnings_out[0]
    assert "T-C01-01" in warnings_out[0] and "T-C01-02" in warnings_out[0]
    assert any("[Z3-RULE-WARNING]" in rec.message for rec in caplog.records)


def test_z3_helper_rejects_unsat_domain_and_scopes_piecewise_constraints():
    """Unsatisfiable domains must yield None (never vacuous True), and Piecewise branch constraints stay scoped."""
    x0 = sympy.Symbol("x0", real=True)

    # Under x0 > 0, sqrt(-x0) makes domain (-x0 >= 0) unsatisfiable -> must return None, not True.
    assert _z3_check_sympy_equiv(sympy.sqrt(-x0), x0 + 1) is None

    # Branch-scoped sqrt(x0 - 5) must not force x0 >= 5 globally across the fallback branch.
    pw1 = sympy.Piecewise((sympy.sqrt(x0 - 5), x0 >= 5), (0, True))
    pw2 = sympy.Piecewise((sympy.sqrt(x0 - 5), x0 >= 5), (999, True))
    assert _z3_check_sympy_equiv(pw1, pw2) is False

    # Last-branch condition x0 < 0 must stay guarded by Not(x0 > 5), not asserted globally with x0 > 0.
    pw3 = sympy.Piecewise((x0, x0 > 5), (0, x0 < 0))
    assert _z3_check_sympy_equiv(pw3, 123 * x0 + 9) is False

    # Genuinely equivalent Piecewise expressions still resolve to True.
    pw_eq1 = sympy.Piecewise((x0 + 1, x0 >= 2), (2 * x0, True))
    pw_eq2 = sympy.Piecewise((1 + x0, x0 >= 2), (x0 + x0, True))
    assert _z3_check_sympy_equiv(pw_eq1, pw_eq2) is True
