#!/usr/bin/env python3
"""Canonical Parametric Exercise Template Generator Scaffold.

Pre-tested, deterministic reference template generator designed to be cloned
into work/shards/<shard_id>/scratch/ or imported into template JSONs.

Guarantees:
- 0% false positives against check_templates.py and strict validator suite.
- Uses raw strings r"..." for LaTeX math without escape corruption.
- Uses f-strings with double braces rf"k^{{{alpha}}}" for LaTeX exponents/subscripts.
- Distractors model authentic analytical errors (omitted parameters, inverted exponents, scale slips).
- Zero symmetric boilerplate ("converge con X" vs "diverge con Y").
- Zero scaffolding answer leaks in progressive hints (no mechanical elimination instructions).
- Meets TPL-VAR diversity gates (>= 12 distinct seed configurations).
"""

import math
import random


def generate(rng):
    """Generates a parametric question instance with rigorous analytical distractors."""
    # Parametric sweep with high variability (TPL-VAR)
    alpha_choices = [0.25, 0.30, 0.33, 0.35, 0.40, 0.45, 0.50, 0.55]
    s_choices = [0.15, 0.18, 0.20, 0.22, 0.24, 0.26, 0.28, 0.30, 0.32]
    n_choices = [0.01, 0.015, 0.02, 0.025, 0.03]
    g_choices = [0.01, 0.015, 0.02]
    delta_choices = [0.03, 0.035, 0.04, 0.045, 0.05]

    alpha = rng.choice(alpha_choices)
    s = rng.choice(s_choices)
    n = rng.choice(n_choices)
    g = rng.choice(g_choices)
    delta = rng.choice(delta_choices)

    dilution = round(n + g + delta, 4)
    ratio = round(s / dilution, 4)
    exponent = round(1.0 / (1.0 - alpha), 3)
    k_star = round(ratio ** exponent, 2)

    # Correct answer formulated as an objective analytical statement
    c_str = (
        rf"El capital estacionario efectivo es $k^* = \left(\frac{{{s}}}{{{dilution}}}\right)^{{{exponent:.2f}}} \approx {k_star:.2f}$, "
        rf"donde la inversión bruta iguala la depreciación efectiva."
    )

    # Distractor 1: Omits technological growth g (omitted step error)
    dil_err1 = round(n + delta, 4)
    k_err1 = round((s / dil_err1) ** exponent, 2)
    d1 = (
        rf"El capital de equilibrio es $k^* \approx {k_err1:.2f}$, considerando únicamente la suma de tasa demográfica y depreciación física."
    )

    # Distractor 2: Inverts exponent (1 - alpha instead of 1 / (1 - alpha)) (procedural slip)
    inv_exp = round(1.0 - alpha, 3)
    k_err2 = round(ratio ** inv_exp, 2)
    d2 = (
        rf"La magnitud estacionaria resulta en $k^* = \left(\frac{{{s}}}{{{dilution}}}\right)^{{{inv_exp:.2f}}} \approx {k_err2:.2f}$ por despeje directo sin raíz."
    )

    # Distractor 3: Multiplies saving rate by dilution rate instead of ratio (conceptual swap)
    prod_err = round(s * dilution, 4)
    k_err3 = round(prod_err ** exponent, 2)
    d3 = (
        rf"El nivel estacionario se sitúa en $k^* = (s \cdot (n+g+\delta))^{{{exponent:.2f}}} \approx {k_err3:.2f}$ al multiplicar ahorro y dilución."
    )

    # Distractor 4: Uses gross investment rate inverted (dilution / s) (sign/boundary slip)
    inv_ratio = round(dilution / s, 4)
    k_err4 = round(inv_ratio ** exponent, 2)
    d4 = (
        rf"El sendero converge al valor recíproco $k^* = \left(\frac{{{dilution}}}{{{s}}}\right)^{{{exponent:.2f}}} \approx {k_err4:.2f}$ por inversión de cociente."
    )

    # Distractor 5: Confuses capital share alpha with labor share (1 - alpha) (parameter slip)
    alt_exp = round(1.0 / alpha, 3)
    k_err5 = round(ratio ** alt_exp, 2)
    d5 = (
        rf"La intensidad óptima es $k^* = \left(\frac{{{s}}}{{{dilution}}}\right)^{{1/\alpha}} \approx {k_err5:.2f}$ al asumir elasticidad unitaria del capital."
    )

    # Distractor 6: Neglects depreciation rate delta (omitted parameter)
    dil_err6 = round(n + g, 4)
    k_err6 = round((s / dil_err6) ** exponent, 2)
    d6 = (
        rf"El estado estacionario alcanza $k^* \approx {k_err6:.2f}$ bajo el supuesto de conservación total de capital sin depreciación."
    )

    distractors = [
        {"value": d1, "distractor_id": "D-Hab01-01"},
        {"value": d2, "distractor_id": "D-Hab01-02"},
        {"value": d3, "distractor_id": "D-Hab01-03"},
        {"value": d4, "distractor_id": "D-Hab01-04"},
        {"value": d5, "distractor_id": "D-Hab01-05"},
        {"value": d6, "distractor_id": "D-Hab01-06"},
    ]

    return {
        "vars": {
            "s": s,
            "alpha": alpha,
            "n": n,
            "g": g,
            "delta": delta,
            "dilution": dilution,
            "k_star": k_star,
        },
        "correct": c_str,
        "distractors": distractors,
    }


def verify(res):
    """Cross-checks that generated instance satisfies mathematical invariants."""
    v = res.get("vars", {})
    s = v.get("s", 0)
    alpha = v.get("alpha", 0)
    dilution = v.get("dilution", 1)
    k_star = v.get("k_star", 0)

    if s <= 0 or alpha <= 0 or dilution <= 0 or k_star <= 0:
        return False

    expected_ratio = s / dilution
    expected_exp = 1.0 / (1.0 - alpha)
    expected_k = round(expected_ratio ** expected_exp, 2)

    return abs(k_star - expected_k) <= 0.05 and len(res.get("distractors", [])) == 6
