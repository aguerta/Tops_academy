#!/usr/bin/env python3
"""
calibrate_auditor.py - Script de calibración objetiva del auditor estático.

Ejecuta el auditor contra el suite sintético `tests/calibration_cases.json`
para medir empíricamente Precisión, Recall y Tasa de Falsos Descubrimientos,
garantizando cero overfitting sobre los prompts de producción del proyecto.
"""

import sys
import os
import json
from audit_prompt import PromptAuditor


def run_calibration():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

    cases_path = os.path.join(os.path.dirname(__file__), "..", "tests", "calibration_cases.json")
    with open(cases_path, "r", encoding="utf-8") as f:
        cases = json.load(f)

    print(f"=== CALIBRACIÓN OBJETIVA DEL AUDITOR ({len(cases)} Casos Sintéticos) ===")
    print("Objetivo: Evaluar detección fáctica de defectos conocidos y ausencia de falsos positivos.\n")

    tp, fp, fn, tn = 0, 0, 0, 0
    results_detail = []

    flaw_map = {
        "few_shot_negative_pattern": "R_ANTI_PATTERN",
        "deprecated_sampling_parameters": "R_DEPRECATED_SAMPLING",
        "context_inversion": "R_CONTEXT_ORDER",
        "emotional_shouting": "R_SHOUTING",
        "unisolated_input": "R_INPUT_ISOLATION",
        "missing_delimiters": "R_STRUCTURE_DELIMITERS",
        "missing_examples": "R_FEW_SHOT_MISSING",
        "agentic_missing_risk_matrix": "R_AGENTIC_RISK",
        "missing_few_shot_examples": "R_FEW_SHOT_MISSING"
    }

    for case in cases:
        auditor = PromptAuditor(case["prompt"], case["id"])
        res = auditor.audit()

        detected_rules = set(f["rule_id"] for f in res["flaws"])
        expected_rules = set(flaw_map.get(e, e) for e in case["expected_flaws"])

        # Compare
        matched = detected_rules.intersection(expected_rules)
        unmatched_expected = expected_rules - detected_rules
        unexpected_detected = detected_rules - expected_rules

        # Filter low severity stylistic recommendations from pure false positives if clean
        clean_case = len(case["expected_flaws"]) == 0
        if clean_case:
            # Clean cases should trigger 0 High and 0 Medium flaws
            severe_detected = [f for f in res["flaws"] if f["severity"] in ["Alta", "Media"]]
            if len(severe_detected) == 0:
                tn += 1
                status = "PASSED (Clean verified)"
            else:
                fp += len(severe_detected)
                status = f"FAILED (False Positives: {[f['rule_id'] for f in severe_detected]})"
        else:
            tp += len(matched)
            fn += len(unmatched_expected)
            fp += len(unexpected_detected)
            if len(unmatched_expected) == 0 and len(unexpected_detected) == 0:
                status = "PASSED (Exact match)"
            elif len(unmatched_expected) == 0:
                status = f"PASSED WITH EXTRA ({unexpected_detected})"
            else:
                status = f"FAILED (Missed: {unmatched_expected})"

        results_detail.append((case["id"], status, res["verdict"]))
        print(f"[{status[:6]}] {case['id']:<35} -> Veredicto: {res['verdict']}")
        if len(unmatched_expected) > 0 or len(unexpected_detected) > 0:
            print(f"       [DEBUG] expected={expected_rules} | detected={detected_rules}")
            print(f"       [DEBUG] unmatched={unmatched_expected} | unexpected={unexpected_detected}")

    print("\n=== RESUMEN ESTADÍSTICO DE BENCHMARK SINTÉTICO ===")
    precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 1.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    print(f"Verdaderos Positivos (TP): {tp}")
    print(f"Falsos Positivos       (FP): {fp}")
    print(f"Falsos Negativos       (FN): {fn}")
    print(f"Verdaderos Negativos   (TN): {tn}")
    print(f"Precisión:             {precision:.2%}")
    print(f"Recall:                {recall:.2%}")
    print(f"F1-Score:              {f1:.2%}")

    if fn == 0 and fp == 0:
        print("\n CALIBRACIÓN EXITOSA: 100% Recall de defectos inyectados y 0 Falsos Positivos.")
        sys.exit(0)
    else:
        print(f"\n CALIBRACIÓN CON DESVIACIÓN: FP={fp}, FN={fn}")
        sys.exit(1)


if __name__ == "__main__":
    run_calibration()
