"""Phase 2 Milestone 20 + CTA-Autonomy pipeline alignment unit tests.

Covers:
1. compile_cta & check_cta canonical recommended_modalities validation ([CTA-MODALITY-INVALID])
2. engine/assemble._assemble_invariant_canvas validation, @var@ interpolation & numeric coercion
3. engine/invariants.check_instance_invariants M20 KaTeX, inequality, kind, and stem leak guards
4. check_templates._canonical_answer_signature diversity for invariant_canvas geometry/inequality/target_state
5. src/validator/rules.py R-20 & R-19 parity for unstructured_model and invariant_canvas + canonical course
6. judge.py M20 sanitization & answer matching across all 6 M20 modalities
7. Updated M20 + CTA-Autonomy wording in pipeline utilities
"""

from __future__ import annotations

import copy
import json
import random
import sys
from pathlib import Path
from typing import Any, Dict, List

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
C2C_DIR = REPO_ROOT / ".agents" / "skills" / "content-to-course"
SRC_DIR = REPO_ROOT / "src"

for _p in (C2C_DIR, SRC_DIR, REPO_ROOT):
    _p_str = str(_p)
    if _p_str not in sys.path:
        sys.path.insert(0, _p_str)

import check_cta
import check_templates
import compile_cta
import course_publisher
import judge
import plan_shards
import shard_precheck
from engine.assemble import (
    VALID_CANVAS_INVARIANT_KINDS as ASSEMBLE_VALID_KINDS,
    _assemble_invariant_canvas,
    _coerce_num_if_numeric,
)
from engine.invariants import (
    VALID_CANVAS_INVARIANT_KINDS as INV_VALID_KINDS,
    check_instance_invariants,
)
from validator.core import validate_course_content
from validator.rules import check_extended_quality_rules


CANONICAL_9_MODALITIES = {
    "multiple_choice_7_options",
    "multiple_select",
    "fill_in_the_blank",
    "open_symbolic",
    "proof_dag",
    "adversarial_break",
    "unstructured_model",
    "invariant_canvas",
    "concept_matching",
}


def _make_valid_cta_dict(rec_mods: Any = None, cid: str = "C-01", ctype: str = "concept") -> Dict[str, Any]:
    comp: Dict[str, Any] = {
        "id": cid,
        "type": ctype,
        "name": "Análisis paramétrico de equilibrio",
        "description_latex": "Determina puntos de equilibrio y restricciones analíticas sobre parámetros reales.",
        "bloom": "Analyze",
        "session": "Unidad 1: Equilibrio",
        "unit_index": 1,
        "prerequisites": [],
        "evidence": [{"doc": "manual.pdf", "page": 1}],
        "distractors": [
            {
                "id": f"D-{cid.replace('-', '')}-0{i}",
                "name": f"Trampa conceptual #{i}",
                "wrong_belief": f"Creencia errónea #{i}",
                "correct_belief": f"Principio válido #{i}",
                "trigger": f"Al evaluar el parámetro #{i}",
                "manifestation": f"$x_{i}$",
                "error_type": "conceptual_swap",
                "severity": "high",
                "origin": "inferred",
                "remediation_hint": (
                    f"Revisar paso a paso la condición #{i} y comprobar la formulación matemática completa."
                ),
                "omitted_step": f"Paso omitido #{i}",
                "evidence": {"doc": "manual.pdf", "page": 1},
            }
            for i in range(1, 7)
        ],
        "assumptions": [
            {
                "id": f"A-{cid.replace('-', '')}-01",
                "statement_latex": r"Continuidad en todo el intervalo real $[a, b]$.",
                "violation_consequence": "Sin continuidad no se garantiza la existencia de raíz interior.",
            }
        ],
    }
    if rec_mods is not None:
        comp["recommended_modalities"] = rec_mods
    return {
        "contract_version": 2,
        "course_id": "test_m20_cta",
        "title": "Curso CTA M20",
        "macro_competency": "Dominio analítico integral",
        "competencies": [comp],
    }


def _make_manifest() -> Dict[str, Any]:
    return {
        "course_id": "test_m20_cta",
        "files": [{"doc": "manual.pdf", "total_pages": 10, "valid_page_range": [1, 10]}],
    }


def _make_valid_unstructured_model() -> Dict[str, Any]:
    return {
        "interaction_type": "unstructured_model",
        "stem": r"Formula el modelo térmico para constante $k = 3$ y temperatura inicial $T_0 = 20$:",
        "hints": [
            "Identifica primero la incógnita principal del problema.",
            "Selecciona las hipótesis físicas compatibles con el régimen estacionario.",
            "Escribe la ecuación diferencial o algebraica resultante.",
        ],
        "unstructured_model": {
            "phase1_variables": {
                "prompt": r"Clasifica las variables del modelo con $k = 3$:",
                "roles": ["parametro", "incognita", "distractor"],
                "items": [
                    {"id": "V1", "label": r"Temperatura $T_0$", "correct_role": "parametro"},
                    {
                        "id": "V2",
                        "label": r"Razón $r$",
                        "correct_role": "incognita",
                        "error_rationale": r"Confunde la razón $r$ con parámetro fijo.",
                    },
                ],
            },
            "phase2_assumptions": {
                "prompt": r"Selecciona supuestos válidos para $T(t)$:",
                "options": [
                    {"id": "A1", "content": r"Ambiente constante $T_a$", "is_required": True},
                    {
                        "id": "A2",
                        "content": r"Transferencia infinita",
                        "is_required": False,
                        "error_rationale": r"La hipótesis viola la ley exponencial $e^{-kt}$.",
                    },
                ],
            },
            "phase3_formulation": {
                "prompt": r"Elige la ecuación para $\frac{dT}{dt}$:",
                "input_mode": "select",
                "options": [
                    {"id": "F1", "content": r"$\frac{dT}{dt} = -k(T - T_a)$", "is_correct": True},
                    {
                        "id": "F2",
                        "content": r"$\frac{dT}{dt} = +k(T - T_a)$",
                        "is_correct": False,
                        "error_rationale": r"El signo positivo produce divergencia en $T(t)$.",
                    },
                ],
            },
        },
    }


def _make_valid_cartesian_canvas(stem: str | None = None) -> Dict[str, Any]:
    return {
        "interaction_type": "invariant_canvas",
        "stem": stem or r"Ubica el vértice y configura la desigualdad para pendiente $m = 2$:",
        "hints": [
            "Determina primero la frontera lineal en el primer cuadrante.",
            "Evalúa la continuidad de la frontera según si la desigualdad es estricta.",
            "Comprueba un punto de prueba en el semiplano sombreado.",
        ],
        "invariant_canvas": {
            "mode": "cartesian",
            "x_range": [0, 10],
            "y_range": [0, 20],
            "step": 1,
            "x_label": r"$x_1$",
            "y_label": r"$x_2$",
            "sliders": [{"id": "s", "label": r"Pendiente $m$", "min": 0, "max": 5, "initial": 1}],
            "fixed_curves": [
                {"id": "b", "label": r"Recta $x_2 = 10 - 2x_1$", "expression": "10 - 2*x", "domain": [0, 5]}
            ],
            "interactive_curves": [
                {"id": "c_int", "label": r"Curva $s \cdot x$", "expression": "s*x", "domain": [0, 5]}
            ],
            "interactive_points": [{"id": "pt_v", "label": r"Vértice $V$", "x": 1, "y": 1}],
            "fixed_points": [{"id": "fp0", "label": r"Origen $O$", "x": 0, "y": 10}],
            "inequality": {
                "curve_id": "b",
                "initial_style": "solid",
                "initial_shade": "above",
            },
            "invariants": [
                {
                    "id": "INV1",
                    "kind": "point_coords",
                    "point_id": "pt_v",
                    "target_x": 3,
                    "target_y": 4,
                    "error_rationale": r"El vértice debe ubicarse sobre $x_2 = 10 - 2x_1$.",
                },
                {
                    "id": "INV2",
                    "kind": "inequality_state",
                    "expected_style": "dashed",
                    "expected_shade": "below",
                    "error_rationale": r"Desigualdad estricta $<$ exige trazo discontinuo y región inferior.",
                },
            ],
        },
    }


def _make_valid_tree_canvas() -> Dict[str, Any]:
    return {
        "interaction_type": "invariant_canvas",
        "stem": r"Selecciona las ramas de equilibrio perfecto en el juego secuencial:",
        "hints": [
            "Aplica inducción hacia atrás desde los nodos terminales.",
            "Agrupa en un conjunto de información los nodos indistinguibles.",
            "Verifica que la estrategia del jugador 2 sea óptima.",
        ],
        "invariant_canvas": {
            "mode": "tree",
            "interaction_mode": "both",
            "nodes": [
                {"id": "N0", "label": r"$J_1$", "x": 100, "y": 40, "player": "1"},
                {"id": "N1", "label": r"$J_2$", "x": 60, "y": 140, "player": "2"},
                {"id": "N2", "label": r"$J_2$", "x": 140, "y": 140, "player": "2"},
            ],
            "edges": [
                {"id": "E1", "from": "N0", "to": "N1", "label": r"$a_1$"},
                {"id": "E2", "from": "N0", "to": "N2", "label": r"$a_2$"},
            ],
            "tree_invariants": {
                "required_edges": ["E1"],
                "required_info_sets": [["N1", "N2"]],
                "edge_error_rationale": r"La rama seleccionada no maximiza el pago $u_1$.",
                "info_set_error_rationale": r"El conjunto $\{N_1, N_2\}$ no agrupa las historias simultáneas.",
            },
        },
    }


class TestCtaRecommendedModalitiesCanonical:
    def test_canonical_modality_sets_match_9_modalities(self):
        assert compile_cta._CANONICAL_MODALITIES == CANONICAL_9_MODALITIES
        assert check_cta._VALID_RECOMMENDED_MODALITIES == CANONICAL_9_MODALITIES

    def test_normalize_recommended_modalities_aliases_and_dedup(self):
        raw = ["MC7", "ms", "fib", "sym", "proof", "fallacy", "stage0", "canvas", "matching", "mc", "open_symbolic"]
        normalized = compile_cta._normalize_recommended_modalities(raw, cid="Hab-01")
        assert normalized == [
            "multiple_choice_7_options",
            "multiple_select",
            "fill_in_the_blank",
            "open_symbolic",
            "proof_dag",
            "adversarial_break",
            "unstructured_model",
            "invariant_canvas",
            "concept_matching",
        ]
        assert compile_cta._normalize_recommended_modalities("canvas, sym, canvas", cid="C-01") == [
            "invariant_canvas",
            "open_symbolic",
        ]
        assert compile_cta._normalize_recommended_modalities(None, cid="C-01") == []

    def test_normalize_recommended_modalities_rejects_invalid_with_error_code(self):
        with pytest.raises(ValueError) as excinfo:
            compile_cta._normalize_recommended_modalities(["open_symbolic", "bogus_modality"], cid="Hab-09")
        msg = str(excinfo.value)
        assert "[CTA-MODALITY-INVALID]" in msg
        assert "Hab-09" in msg
        assert "bogus_modality" in msg

    def test_compile_cta_module_rejects_invalid_11th_tuple_modality(self):
        distractors = [
            (
                f"Trampa {i}",
                f"Creencia falsa {i}",
                f"Creencia correcta {i}",
                f"$x_{i}$",
                f"Revisar detenidamente la propiedad matemática #{i} antes de enviar tu respuesta.",
                f"Paso {i}",
            )
            for i in range(1, 7)
        ]
        assumptions = [("A-Hab01-01", r"Hipótesis de suavidad $C^1$ en el dominio.", "Sin suavidad falla el gradiente.")]
        bad_tuples = [
            (
                "skill",
                "Hab-01",
                "Derivación paramétrica",
                r"Analiza la función $f(x) = x^2$ sobre todo el dominio real de estudio.",
                "Analyze",
                "manual.pdf",
                1,
                [],
                distractors,
                assumptions,
                ["open_symbolic", "unknown_mode"],
            )
        ]
        with pytest.raises(ValueError, match=r"\[CTA-MODALITY-INVALID\].*Hab-01"):
            compile_cta.compile_cta_module(bad_tuples, require_assumptions=True, contract_version=2)

        good_tuples = [(*bad_tuples[0][:10], ["sym", "canvas", "proof"])]
        compiled = compile_cta.compile_cta_module(good_tuples, require_assumptions=True, contract_version=2)
        assert compiled["competencies"][0]["recommended_modalities"] == [
            "open_symbolic",
            "invariant_canvas",
            "proof_dag",
        ]

    def test_check_cta_accepts_9_canonical_and_rejects_invalid_or_unnormalized(self):
        manifest = _make_manifest()
        all_canonical = sorted(CANONICAL_9_MODALITIES)
        for chunk in (all_canonical[0:3], all_canonical[3:6], all_canonical[6:9]):
            valid_cta = _make_valid_cta_dict(rec_mods=chunk)
            res_ok = check_cta.validate_cta_rules(valid_cta, manifest_data=manifest, require_assumptions=True)
            assert res_ok.valid, f"Expected valid CTA with modalities {chunk}, got: {res_ok.errors}"

            res_part_ok = check_cta.check_cta_part(valid_cta, manifest_data=manifest, require_assumptions=True)
            assert res_part_ok.valid, f"Expected valid cta_part for {chunk}, got: {res_part_ok.errors}"

        for bad_val in (["open_symbolic", "bogus_modality"], ["FIB"], [123], "open_symbolic"):
            bad_cta = _make_valid_cta_dict(rec_mods=bad_val, cid="Hab-07")
            res_bad = check_cta.validate_cta_rules(bad_cta, manifest_data=manifest, require_assumptions=True)
            assert not res_bad.valid
            assert any("[CTA-MODALITY-INVALID]" in e and "Hab-07" in e for e in res_bad.errors), (
                f"Expected [CTA-MODALITY-INVALID] for {bad_val!r}, got {res_bad.errors}"
            )
            res_part_bad = check_cta.check_cta_part(bad_cta, manifest_data=manifest, require_assumptions=True)
            assert any("[CTA-MODALITY-INVALID]" in e and "Hab-07" in e for e in res_part_bad.errors)


class TestAssembleInvariantCanvasM20:
    def test_valid_kinds_constant_shared(self):
        expected = {
            "point_on_curve",
            "point_coords",
            "kink_at",
            "slope_at",
            "slider_eq",
            "slider_range",
            "curves_intersect_at",
            "point_in_region",
            "inequality_state",
            "expr_true",
        }
        assert ASSEMBLE_VALID_KINDS == expected
        assert INV_VALID_KINDS == expected

    def test_coerce_num_if_numeric(self):
        assert _coerce_num_if_numeric("42") == 42 and isinstance(_coerce_num_if_numeric("42"), int)
        assert _coerce_num_if_numeric("-7") == -7 and isinstance(_coerce_num_if_numeric("-7"), int)
        assert _coerce_num_if_numeric("3.25") == 3.25 and isinstance(_coerce_num_if_numeric("3.25"), float)
        assert _coerce_num_if_numeric("  -0.5 ") == -0.5 and isinstance(_coerce_num_if_numeric("  -0.5 "), float)
        assert _coerce_num_if_numeric("2*x + 1") == "2*x + 1"
        assert _coerce_num_if_numeric("dashed") == "dashed"
        assert _coerce_num_if_numeric("") == ""
        assert _coerce_num_if_numeric(True) is True
        assert _coerce_num_if_numeric(None) is None

    def test_invalid_invariant_kind_rejected(self):
        raw_ic = {
            "mode": "cartesian",
            "invariants": [{"id": "INV1", "kind": "unknown_kind"}],
        }
        with pytest.raises(ValueError, match=r"\[CANVAS-INVARIANT-KIND\]"):
            _assemble_invariant_canvas(raw_ic, {}, None, {})

        with pytest.raises(ValueError, match=r"\[CANVAS-INVARIANT-KIND\]"):
            _assemble_invariant_canvas({"mode": "cartesian", "invariants": ["not_a_dict"]}, {}, None, {})

    def test_numeric_interpolation_all_kinds_inequality_and_target_state(self):
        variables = {
            "tx": 5,
            "ty": 14,
            "slope": 2.5,
            "lo": 1,
            "hi": 9,
            "cid": "b",
            "init_st": "solid",
            "init_sh": "above",
            "exp_st": "dashed",
            "exp_sh": "below",
        }
        raw_ic = {
            "mode": "cartesian",
            "fixed_curves": [{"id": "b", "label": r"Borde $y = 24 - 2x$", "expression": "24 - 2*x", "domain": [0, 12]}],
            "interactive_curves": [{"id": "c2", "label": r"Recta", "expression": "s*x", "domain": [0, 12]}],
            "fixed_points": [{"id": "fp1", "x": "@lo@", "y": "@ty@", "label": r"$P_0$"}],
            "inequality": {
                "curve_id": "@cid@",
                "initial_style": "@init_st@",
                "initial_shade": "@init_sh@",
            },
            "invariants": [
                {"id": "I1", "kind": "point_on_curve", "point_id": "p", "curve_id": "b"},
                {"id": "I2", "kind": "point_coords", "point_id": "p", "target_x": "@tx@", "target_y": "@ty@"},
                {"id": "I3", "kind": "kink_at", "curve_id": "b", "x": "@tx@", "target": "0.5"},
                {"id": "I4", "kind": "slope_at", "curve_id": "b", "x": "@lo@", "target_slope": "@slope@", "expected": "-2"},
                {"id": "I5", "kind": "slider_eq", "slider_id": "s", "expected": "@slope@"},
                {"id": "I6", "kind": "slider_range", "slider_id": "s", "min": "@lo@", "max": "@hi@"},
                {"id": "I7", "kind": "curves_intersect_at", "curve_a": "b", "curve_b": "c2", "x": "@tx@"},
                {"id": "I8", "kind": "point_in_region", "point_id": "p", "expr": "y <= 24 - 2*x + @lo@"},
                {"id": "I9", "kind": "inequality_state", "expected_style": "@exp_st@", "expected_shade": "@exp_sh@"},
                {"id": "I10", "kind": "expr_true", "expr": "s >= @lo@"},
            ],
            "target_state": {
                "points": {"pt_v": {"x": "@tx@", "y": "@ty@"}},
                "sliders": {"s": "@slope@"},
                "inequalityStyle": "@exp_st@",
                "inequalityShade": "@exp_sh@",
                "coords_list": ["@lo@", "@hi@"],
            },
        }
        compiled_ic, ans = _assemble_invariant_canvas(raw_ic, variables, None, {})
        invs = {inv["id"]: inv for inv in compiled_ic["invariants"]}
        assert invs["I2"]["target_x"] == 5 and isinstance(invs["I2"]["target_x"], int)
        assert invs["I2"]["target_y"] == 14 and isinstance(invs["I2"]["target_y"], int)
        assert invs["I3"]["x"] == 5 and invs["I3"]["target"] == 0.5
        assert invs["I4"]["target_slope"] == 2.5 and invs["I4"]["expected"] == -2
        assert invs["I6"]["min"] == 1 and invs["I6"]["max"] == 9
        assert invs["I8"]["expr"] == "y <= 24 - 2*x + 1"
        assert invs["I10"]["expr"] == "s >= 1"
        assert compiled_ic["fixed_points"][0]["x"] == 1
        assert compiled_ic["inequality"] == {
            "curve_id": "b",
            "initial_style": "solid",
            "initial_shade": "above",
        }
        expected_ts = {
            "points": {"pt_v": {"x": 5, "y": 14}},
            "sliders": {"s": 2.5},
            "inequalityStyle": "dashed",
            "inequalityShade": "below",
            "coords_list": [1, 9],
        }
        assert compiled_ic["target_state"] == expected_ts
        assert ans == {"mode": "cartesian", "target_state": expected_ts}

    def test_inequality_validation_failures(self):
        base_curves = [{"id": "b", "expression": "10 - x", "domain": [0, 10]}]

        # Missing curve_id in fixed_curves/interactive_curves
        with pytest.raises(ValueError, match=r"\[CANVAS-INEQUALITY\]"):
            _assemble_invariant_canvas(
                {
                    "mode": "cartesian",
                    "fixed_curves": base_curves,
                    "inequality": {"curve_id": "missing_curve", "initial_style": "solid"},
                    "invariants": [{"kind": "inequality_state", "expected_style": "dashed", "expected_shade": "below"}],
                },
                {},
                None,
                {},
            )

        # Invalid initial_style
        with pytest.raises(ValueError, match=r"\[CANVAS-INEQUALITY\]"):
            _assemble_invariant_canvas(
                {
                    "mode": "cartesian",
                    "fixed_curves": base_curves,
                    "inequality": {"curve_id": "b", "initial_style": "dotted"},
                    "invariants": [{"kind": "inequality_state", "expected_style": "dashed", "expected_shade": "below"}],
                },
                {},
                None,
                {},
            )

        # Invalid initial_shade
        with pytest.raises(ValueError, match=r"\[CANVAS-INEQUALITY\]"):
            _assemble_invariant_canvas(
                {
                    "mode": "cartesian",
                    "fixed_curves": base_curves,
                    "inequality": {"curve_id": "b", "initial_shade": "left"},
                    "invariants": [{"kind": "inequality_state", "expected_style": "dashed", "expected_shade": "below"}],
                },
                {},
                None,
                {},
            )

        # Invalid expected_style / expected_shade on inequality_state invariant
        for bad_inv in (
            {"kind": "inequality_state", "expected_style": "dotted", "expected_shade": "below"},
            {"kind": "inequality_state", "expected_style": "dashed", "expected_shade": "none"},
        ):
            with pytest.raises(ValueError, match=r"\[CANVAS-INEQUALITY\]"):
                _assemble_invariant_canvas(
                    {"mode": "cartesian", "fixed_curves": base_curves, "invariants": [bad_inv]},
                    {},
                    None,
                    {},
                )


class TestInvariantsM20Parity:
    def test_unstructured_model_katex_checks(self):
        base = _make_valid_unstructured_model()
        ok, errs = check_instance_invariants(base, "unstructured_model")
        assert ok, f"Valid unstructured_model failed: {errs}"

        bad_latex = r"$\frac{1}{2$"

        # phase1_variables.items[*].label
        q1 = copy.deepcopy(base)
        q1["unstructured_model"]["phase1_variables"]["items"][0]["label"] = bad_latex
        ok1, errs1 = check_instance_invariants(q1, "unstructured_model")
        assert not ok1 and any("phase1_variables.items[0].label" in e for e in errs1)

        # phase2_assumptions.options[*].{content, error_rationale}
        for fld in ("content", "error_rationale"):
            q2 = copy.deepcopy(base)
            q2["unstructured_model"]["phase2_assumptions"]["options"][1][fld] = bad_latex
            ok2, errs2 = check_instance_invariants(q2, "unstructured_model")
            assert not ok2 and any(f"phase2_assumptions.options[1].{fld}" in e for e in errs2)

        # phase3_formulation.options[*].{content, error_rationale}
        for fld in ("content", "error_rationale"):
            q3 = copy.deepcopy(base)
            q3["unstructured_model"]["phase3_formulation"]["options"][1][fld] = bad_latex
            ok3, errs3 = check_instance_invariants(q3, "unstructured_model")
            assert not ok3 and any(f"phase3_formulation.options[1].{fld}" in e for e in errs3)

        # phase3_formulation.{distractors, diagnostic_distractors}[*].error_rationale
        for dkey in ("distractors", "diagnostic_distractors"):
            qd = copy.deepcopy(base)
            qd["unstructured_model"]["phase3_formulation"][dkey] = [
                {"expression": "k*T", "error_rationale": bad_latex}
            ]
            okd, errsd = check_instance_invariants(qd, "unstructured_model")
            assert not okd and any(f"phase3_formulation.{dkey}[0].error_rationale" in e for e in errsd)

    def test_invariant_canvas_cartesian_katex_inequality_kind_and_leaks(self):
        base = _make_valid_cartesian_canvas()
        ok, errs = check_instance_invariants(base, "invariant_canvas")
        assert ok, f"Valid cartesian invariant_canvas failed: {errs}"

        # Invalid kind
        qk = copy.deepcopy(base)
        qk["invariant_canvas"]["invariants"][0]["kind"] = "bad_kind"
        okk, errsk = check_instance_invariants(qk, "invariant_canvas")
        assert not okk and any("[CANVAS-INVARIANT-KIND]" in e for e in errsk)

        # Undeclared inequality.curve_id and bad initial_style/initial_shade
        qi = copy.deepcopy(base)
        qi["invariant_canvas"]["inequality"] = {
            "curve_id": "undeclared",
            "initial_style": "dotted",
            "initial_shade": "sideways",
        }
        oki, errsi = check_instance_invariants(qi, "invariant_canvas")
        assert not oki
        err_joined = "\n".join(errsi)
        assert err_joined.count("[CANVAS-INEQUALITY]") >= 3

        # Bad inequality_state invariant
        qis = copy.deepcopy(base)
        qis["invariant_canvas"]["invariants"][1]["expected_style"] = "thick"
        qis["invariant_canvas"]["invariants"][1]["expected_shade"] = "none"
        okis, errsis = check_instance_invariants(qis, "invariant_canvas")
        assert not okis and sum("[CANVAS-INEQUALITY]" in e for e in errsis) == 2

        # KaTeX errors across cartesian labels & rationales
        bad_latex = r"$\frac{1}{2$"
        targets = [
            ("x_label", lambda ic: ic.__setitem__("x_label", bad_latex)),
            ("y_label", lambda ic: ic.__setitem__("y_label", bad_latex)),
            ("fixed_curves[0].label", lambda ic: ic["fixed_curves"][0].__setitem__("label", bad_latex)),
            ("interactive_curves[0].label", lambda ic: ic["interactive_curves"][0].__setitem__("label", bad_latex)),
            ("interactive_points[0].label", lambda ic: ic["interactive_points"][0].__setitem__("label", bad_latex)),
            ("fixed_points[0].label", lambda ic: ic["fixed_points"][0].__setitem__("label", bad_latex)),
            ("sliders[0].label", lambda ic: ic["sliders"][0].__setitem__("label", bad_latex)),
            ("invariants[0].error_rationale", lambda ic: ic["invariants"][0].__setitem__("error_rationale", bad_latex)),
        ]
        for label_desc, mutator in targets:
            qm = copy.deepcopy(base)
            mutator(qm["invariant_canvas"])
            okm, errsm = check_instance_invariants(qm, "invariant_canvas")
            assert not okm and any(label_desc in e for e in errsm), (
                f"Expected KaTeX error for {label_desc}, got {errsm}"
            )

        # Stem coordinate leak on point_coords and kink_at, excluding fixed_points
        q_pc_leak = _make_valid_cartesian_canvas(stem=r"Ubica el punto objetivo exactamente en $(3, 4)$:")
        ok_pc, errs_pc = check_instance_invariants(q_pc_leak, "invariant_canvas")
        assert not ok_pc and any("leaked verbatim in stem text" in e for e in errs_pc)

        q_kink_leak = copy.deepcopy(base)
        q_kink_leak["stem"] = r"Identifica el quiebre en $(6, 8)$ de la restricción:"
        q_kink_leak["invariant_canvas"]["invariants"] = [
            {"id": "K1", "kind": "kink_at", "curve_id": "b", "x": 6, "target_y": 8, "target": 0.5}
        ]
        ok_kl, errs_kl = check_instance_invariants(q_kink_leak, "invariant_canvas")
        assert not ok_kl and any("leaked verbatim in stem text" in e for e in errs_kl)

        # Excluded when declared in fixed_points (including int vs numeric string)
        q_fp_ok = copy.deepcopy(q_kink_leak)
        q_fp_ok["invariant_canvas"]["fixed_points"] = [{"id": "fp_ref", "x": "6", "y": 8, "label": r"$A$"}]
        ok_fp, errs_fp = check_instance_invariants(q_fp_ok, "invariant_canvas")
        assert ok_fp, f"fixed_points coordinates should be excluded from leak check: {errs_fp}"

    def test_invariant_canvas_tree_katex_checks(self):
        base = _make_valid_tree_canvas()
        ok, errs = check_instance_invariants(base, "invariant_canvas")
        assert ok, f"Valid tree invariant_canvas failed: {errs}"

        bad_latex = r"$\frac{1}{2$"
        for desc, mutator in (
            ("nodes[0].label", lambda ic: ic["nodes"][0].__setitem__("label", bad_latex)),
            ("edges[0].label", lambda ic: ic["edges"][0].__setitem__("label", bad_latex)),
            ("tree_invariants.edge_error_rationale", lambda ic: ic["tree_invariants"].__setitem__("edge_error_rationale", bad_latex)),
            ("tree_invariants.info_set_error_rationale", lambda ic: ic["tree_invariants"].__setitem__("info_set_error_rationale", bad_latex)),
        ):
            qt = copy.deepcopy(base)
            mutator(qt["invariant_canvas"])
            okt, errst = check_instance_invariants(qt, "invariant_canvas")
            assert not okt and any(desc in e for e in errst), f"Expected error for {desc}, got {errst}"


class TestCheckTemplatesCanvasSignature:
    def test_canonical_answer_signature_tracks_all_canvas_geometry_fields(self):
        base_q = {
            "correct_answer": {"mode": "cartesian", "target_state": {"invariants_count": 1}},
            "invariant_canvas": {
                "mode": "cartesian",
                "fixed_curves": [{"id": "b", "expression": "10 - x"}],
                "interactive_curves": [],
                "invariants": [{"kind": "inequality_state", "expected_style": "dashed", "expected_shade": "below"}],
                "inequality": {"curve_id": "b", "initial_style": "solid", "initial_shade": "above"},
                "fixed_points": [{"id": "fp1", "x": 0, "y": 10}],
                "interactive_points": [{"id": "pt1", "x": 2, "y": 8}],
                "segments": [{"id": "s1", "from": [0, 0], "to": [2, 8]}],
                "polygons": [{"id": "pg1", "vertices": [[0, 0], [2, 0], [2, 8]]}],
                "shaded_regions": [{"id": "sr1", "curve_top": "b", "domain": [0, 2]}],
                "sliders": [{"id": "sl1", "min": 0, "max": 5, "initial": 2}],
                "target_state": {"inequalityStyle": "dashed", "inequalityShade": "below"},
            },
        }
        sig_base = check_templates._canonical_answer_signature(base_q, "invariant_canvas")
        assert sig_base == check_templates._canonical_answer_signature(copy.deepcopy(base_q), "invariant_canvas")

        variants = [
            ("inequality", lambda ic: ic["inequality"].__setitem__("initial_shade", "below")),
            ("fixed_points", lambda ic: ic["fixed_points"][0].__setitem__("y", 12)),
            ("interactive_points", lambda ic: ic["interactive_points"][0].__setitem__("x", 4)),
            ("segments", lambda ic: ic["segments"][0].__setitem__("to", [4, 6])),
            ("polygons", lambda ic: ic["polygons"][0].__setitem__("vertices", [[0, 0], [4, 0], [4, 6]])),
            ("shaded_regions", lambda ic: ic["shaded_regions"][0].__setitem__("domain", [0, 4])),
            ("sliders", lambda ic: ic["sliders"][0].__setitem__("initial", 3)),
            ("target_state", lambda ic: ic["target_state"].__setitem__("inequalityShade", "above")),
        ]
        sigs = {sig_base}
        for name, mutator in variants:
            q_var = copy.deepcopy(base_q)
            mutator(q_var["invariant_canvas"])
            s = check_templates._canonical_answer_signature(q_var, "invariant_canvas")
            assert s != sig_base, f"Signature failed to reflect change in {name}"
            sigs.add(s)
        assert len(sigs) == 1 + len(variants)


class TestValidatorRulesM20Parity:
    def test_r20_unstructured_model_and_invariant_canvas(self):
        bad_latex = r"$\frac{1}{2$"
        um_ok = {**_make_valid_unstructured_model(), "id": "Q-UM-1", "competency_id": "Hab-01"}
        ic_cart_ok = {**_make_valid_cartesian_canvas(), "id": "Q-IC-1", "competency_id": "Hab-01"}
        ic_tree_ok = {**_make_valid_tree_canvas(), "id": "Q-TR-1", "competency_id": "Hab-01"}

        assert check_extended_quality_rules({"questions": [um_ok, ic_cart_ok, ic_tree_ok]}) == []

        # Break unstructured_model fields
        um_bad = copy.deepcopy(um_ok)
        um_bad["unstructured_model"]["phase1_variables"]["items"][0]["label"] = bad_latex
        um_bad["unstructured_model"]["phase2_assumptions"]["options"][1]["error_rationale"] = bad_latex
        um_bad["unstructured_model"]["phase3_formulation"]["diagnostic_distractors"] = [
            {"expression": "x", "error_rationale": bad_latex}
        ]
        um_errs = check_extended_quality_rules({"questions": [um_bad]})
        um_fields = " ".join(e.message for e in um_errs)
        assert all(e.rule_id == "R-20" for e in um_errs)
        assert "phase1_variables.items[0].label" in um_fields
        assert "phase2_assumptions.options[1].error_rationale" in um_fields
        assert "phase3_formulation.diagnostic_distractors[0].error_rationale" in um_fields

        # Break cartesian & tree invariant_canvas fields
        ic_cart_bad = copy.deepcopy(ic_cart_ok)
        ic_cart_bad["invariant_canvas"]["x_label"] = bad_latex
        ic_cart_bad["invariant_canvas"]["sliders"][0]["label"] = bad_latex
        ic_cart_bad["invariant_canvas"]["invariants"][0]["error_rationale"] = bad_latex
        cart_errs = check_extended_quality_rules({"questions": [ic_cart_bad]})
        cart_msg = " ".join(e.message for e in cart_errs)
        assert any(e.rule_id == "R-20" for e in cart_errs)
        assert "invariant_canvas.x_label" in cart_msg
        assert "invariant_canvas.sliders[0].label" in cart_msg
        assert "invariant_canvas.invariants[0].error_rationale" in cart_msg

        ic_tree_bad = copy.deepcopy(ic_tree_ok)
        ic_tree_bad["invariant_canvas"]["nodes"][0]["label"] = bad_latex
        ic_tree_bad["invariant_canvas"]["edges"][0]["label"] = bad_latex
        ic_tree_bad["invariant_canvas"]["tree_invariants"]["edge_error_rationale"] = bad_latex
        tree_errs = check_extended_quality_rules({"questions": [ic_tree_bad]})
        tree_msg = " ".join(e.message for e in tree_errs)
        assert any(e.rule_id == "R-20" for e in tree_errs)
        assert "invariant_canvas.nodes[0].label" in tree_msg
        assert "invariant_canvas.edges[0].label" in tree_msg
        assert "invariant_canvas.tree_invariants.edge_error_rationale" in tree_msg

    def test_r19_invariant_canvas_stem_coordinate_leak(self):
        q_pc = {
            **_make_valid_cartesian_canvas(stem=r"Ubica el punto óptimo en $(3, 4)$:"),
            "id": "Q-LEAK-1",
            "competency_id": "Hab-01",
        }
        errs_pc = [e for e in check_extended_quality_rules({"questions": [q_pc]}) if e.rule_id == "R-19"]
        assert len(errs_pc) == 1 and errs_pc[0].code == "ERR_ANSWER_LEAK"

        q_kink = copy.deepcopy(q_pc)
        q_kink["stem"] = r"Marca el quiebre exacto en $(7, 11)$:"
        q_kink["invariant_canvas"]["invariants"] = [
            {"id": "K1", "kind": "kink_at", "curve_id": "b", "x": 7, "target_y": 11, "target": 0.5}
        ]
        errs_kink = [e for e in check_extended_quality_rules({"questions": [q_kink]}) if e.rule_id == "R-19"]
        assert len(errs_kink) == 1 and errs_kink[0].code == "ERR_ANSWER_LEAK"

        # Fixed point exclusion
        q_kink["invariant_canvas"]["fixed_points"] = [{"id": "fp", "x": 7, "y": "11", "label": "$P$"}]
        assert [e for e in check_extended_quality_rules({"questions": [q_kink]}) if e.rule_id == "R-19"] == []

    def test_canonical_m20_course_still_validates_strict(self):
        canonical_path = REPO_ROOT / "tests" / "fixtures" / "m20_canonical_cases" / "m20_canonical_course.json"
        res = validate_course_content(canonical_path.read_text(encoding="utf-8"), strict=True)
        assert res.is_valid, f"Canonical M20 course failed strict validation: {[e.message for e in res.errors]}"


class TestJudgeM20SanitizationAndMatching:
    def test_all_6_m20_modalities_sanitized_and_matched(self):
        # 1. open_symbolic (SymPy equivalence)
        q_sym = {
            "correct_answer": {"expression": "m*g*sin(theta)", "accepted_equivalents": ["g*m*sin(theta)"], "tolerance": 0.001},
            "symbolic_config": {"variables": ["m", "g", "theta"]},
        }
        ji_sym, gt_sym = {}, {}
        judge._sanitize_m20_judge_item("open_symbolic", q_sym, ji_sym, gt_sym)
        assert "correct_answer" not in ji_sym and ji_sym["answer_contract"]["expected_format"] == "open_symbolic"
        assert judge._check_m20_answer_match({"expression": "g*sin(theta)*m"}, gt_sym, "open_symbolic") == (True, "")
        assert not judge._check_m20_answer_match("m*g*cos(theta)", gt_sym, "open_symbolic")[0]

        # 2. proof_dag
        q_dag = {
            "proof_dag": {
                "goal": "Probar P",
                "require_justification": True,
                "justification_bank": ["Axioma", "Sustitución"],
                "steps": [
                    {"id": "S1", "content": "Paso 1", "justification": "Axioma"},
                    {"id": "S2", "content": "Paso 2", "justification": "Sustitución"},
                    {"id": "F1", "content": "Falacia", "is_fallacy": True, "error_rationale": "Falso"},
                ],
                "edges": [["S1", "S2"]],
            },
            "correct_answer": {
                "canonical_order": ["S1", "S2"],
                "required_step_ids": ["S1", "S2"],
                "edges": [["S1", "S2"]],
                "justifications": {"S1": "Axioma", "S2": "Sustitución"},
            },
        }
        ji_dag, gt_dag = {}, {}
        judge._sanitize_m20_judge_item("proof_dag", q_dag, ji_dag, gt_dag)
        assert all("is_fallacy" not in s and "error_rationale" not in s for s in ji_dag["proof_dag"]["steps"])
        assert "edges" not in ji_dag["proof_dag"]
        assert judge._check_m20_answer_match(
            {"canonical_order": ["S1", "S2"], "edges": [["S1", "S2"]], "justifications": {"S1": "Axioma", "S2": "Sustitución"}},
            gt_dag,
            "proof_dag",
        ) == (True, "")
        assert not judge._check_m20_answer_match({"canonical_order": ["S2", "S1"]}, gt_dag, "proof_dag")[0]

        # 3a. adversarial_break (find_fallacy)
        q_adv_f = {
            "adversarial_break": {
                "mode": "find_fallacy",
                "steps": [
                    {"id": "A1", "content": "Paso válido"},
                    {"id": "A2", "content": "Salto falso", "is_fallacy": True, "error_rationale": "Inválido"},
                ],
                "reason_options": [
                    {"id": "R1", "content": "Razón correcta", "is_correct": True},
                    {"id": "R2", "content": "Razón falsa", "is_correct": False},
                ],
            },
            "correct_answer": {"mode": "find_fallacy", "fallacy_step_id": "A2", "correct_reason_id": "R1"},
        }
        ji_af, gt_af = {}, {}
        judge._sanitize_m20_judge_item("adversarial_break", q_adv_f, ji_af, gt_af)
        assert all("is_fallacy" not in s and "error_rationale" not in s for s in ji_af["adversarial_break"]["steps"])
        assert all("is_correct" not in r for r in ji_af["adversarial_break"]["reason_options"])
        assert judge._check_m20_answer_match({"fallacy_step_id": "A2", "correct_reason_id": "R1"}, gt_af, "adversarial_break") == (True, "")
        assert not judge._check_m20_answer_match({"fallacy_step_id": "A1", "correct_reason_id": "R1"}, gt_af, "adversarial_break")[0]

        # 3b. adversarial_break (counterexample)
        q_adv_c = {
            "adversarial_break": {
                "mode": "counterexample",
                "inputs": [{"name": "n", "type": "integer", "min": 1, "max": 20}],
                "predicates": [{"expr": "n**2 > 9"}],
                "sample_witness": {"n": 4},
            },
            "correct_answer": {"mode": "counterexample", "sample_witness": {"n": 4}},
        }
        ji_ac, gt_ac = {}, {}
        judge._sanitize_m20_judge_item("adversarial_break", q_adv_c, ji_ac, gt_ac)
        assert "sample_witness" not in ji_ac["adversarial_break"]
        assert judge._check_m20_answer_match({"sample_witness": {"n": 4}}, gt_ac, "adversarial_break") == (True, "")
        assert not judge._check_m20_answer_match({"sample_witness": {"n": 2}}, gt_ac, "adversarial_break")[0]

        # 4. unstructured_model (symbolic phase3)
        q_um = {
            "unstructured_model": {
                "phase1_variables": {
                    "prompt": "Clasifica:",
                    "roles": ["param", "var"],
                    "items": [{"id": "V1", "label": "k", "correct_role": "param", "error_rationale": "x"}],
                },
                "phase2_assumptions": {
                    "prompt": "Supuestos:",
                    "options": [{"id": "A1", "content": "Lineal", "is_required": True}],
                },
                "phase3_formulation": {
                    "prompt": "Formula:",
                    "input_mode": "symbolic",
                    "correct_expression": {"expression": "a*x + b", "accepted_equivalents": ["b + a*x"]},
                },
            },
            "correct_answer": {
                "phase1": {"V1": "param"},
                "phase2": ["A1"],
                "phase3": {"expression": "a*x + b", "accepted_equivalents": ["b + a*x"]},
            },
        }
        ji_um, gt_um = {}, {}
        judge._sanitize_m20_judge_item("unstructured_model", q_um, ji_um, gt_um)
        assert "correct_role" not in ji_um["unstructured_model"]["phase1_variables"]["items"][0]
        assert "is_required" not in ji_um["unstructured_model"]["phase2_assumptions"]["options"][0]
        assert "correct_expression" not in ji_um["unstructured_model"]["phase3_formulation"]
        assert judge._check_m20_answer_match(
            {"phase1": {"V1": "param"}, "phase2": ["A1"], "phase3": "b + x*a"},
            gt_um,
            "unstructured_model",
        ) == (True, "")
        assert not judge._check_m20_answer_match(
            {"phase1": {"V1": "var"}, "phase2": ["A1"], "phase3": "a*x + b"},
            gt_um,
            "unstructured_model",
        )[0]

        # 5a. invariant_canvas (cartesian + alias + invariants fallback)
        q_ic_cart = {
            "invariant_canvas": {
                **_make_valid_cartesian_canvas()["invariant_canvas"],
                "target_state": {"points": {"pt_v": {"x": 3, "y": 4}}, "inequalityStyle": "dashed", "inequalityShade": "below"},
            },
            "correct_answer": {
                "mode": "cartesian",
                "target_state": {"points": {"pt_v": {"x": 3, "y": 4}}, "inequalityStyle": "dashed", "inequalityShade": "below"},
            },
        }
        ji_ic, gt_ic = {}, {}
        judge._sanitize_m20_judge_item("invariant_canvas", q_ic_cart, ji_ic, gt_ic)
        assert "invariants" not in ji_ic["invariant_canvas"]
        assert "target_state" not in ji_ic["invariant_canvas"]
        assert judge._check_m20_answer_match(
            {"points": {"pt_v": {"x": 3.01, "y": 4.0}}, "style": "dashed", "shade": "below"},
            gt_ic,
            "invariant_canvas",
        ) == (True, "")
        assert not judge._check_m20_answer_match(
            {"points": {"pt_v": {"x": 1, "y": 1}}, "style": "solid", "shade": "above"},
            gt_ic,
            "invariant_canvas",
        )[0]

        # 5b. invariant_canvas (tree)
        q_ic_tree = {
            "invariant_canvas": _make_valid_tree_canvas()["invariant_canvas"],
            "correct_answer": {"mode": "tree", "required_edges": ["E1"], "required_info_sets": [["N1", "N2"]]},
        }
        ji_tr, gt_tr = {}, {}
        judge._sanitize_m20_judge_item("invariant_canvas", q_ic_tree, ji_tr, gt_tr)
        assert "tree_invariants" not in ji_tr["invariant_canvas"]
        assert judge._check_m20_answer_match(
            {"required_edges": ["E1"], "required_info_sets": [["N2", "N1"]]},
            gt_tr,
            "invariant_canvas",
        ) == (True, "")
        assert not judge._check_m20_answer_match(
            {"required_edges": ["E2"], "required_info_sets": [["N1", "N2"]]},
            gt_tr,
            "invariant_canvas",
        )[0]

        # 6. concept_matching
        q_cm = {
            "concept_matching": {
                "premises": [{"id": "P1", "content": "$f'' > 0$"}],
                "targets": [
                    {"id": "T1", "content": "Convexa"},
                    {"id": "T2", "content": "Cóncava", "is_distractor": True, "error_rationale": "Signo"},
                ],
                "correct_pairs": {"P1": "T1"},
            },
            "correct_answer": {"pairs": {"P1": "T1"}},
        }
        ji_cm, gt_cm = {}, {}
        judge._sanitize_m20_judge_item("concept_matching", q_cm, ji_cm, gt_cm)
        assert "correct_pairs" not in ji_cm["concept_matching"]
        assert all("is_distractor" not in t and "error_rationale" not in t for t in ji_cm["concept_matching"]["targets"])
        assert judge._check_m20_answer_match({"pairs": {"P1": "T1"}}, gt_cm, "concept_matching") == (True, "")
        assert not judge._check_m20_answer_match({"pairs": {"P1": "T2"}}, gt_cm, "concept_matching")[0]


class TestStaleWordingAligned:
    def test_pipeline_utilities_reflect_m20_cta_autonomy_wording(self):
        # 1. shard_precheck.py VER-SIGNATURE
        bad_ver_src = "def ver_1(res, v=None):\n    return True\n"
        precheck_errs = shard_precheck.precheck_source(bad_ver_src)
        assert any(
            "[VER-SIGNATURE]" in e and "(MC/FIB/open_symbolic)" in e and "(MS/M20 estructurado)" in e
            for e in precheck_errs
        ), f"Unexpected shard_precheck message: {precheck_errs}"

        # 2. course_publisher.py prescriptive ZPD/modality guidance
        _, _, fix_msg = course_publisher._resolve_linter_remediation(
            "retrieval_modality_linter", "Insufficient diversity", "Hab-01", "shard_01_data.py", "gen_1", "L10-L20"
        )
        assert "al menos 4 tuplas ortogonales" in fix_msg
        assert "las modalidades recomendadas por el CTA (M20 / FIB / MS / MC7)" in fix_msg
        assert "cuota de `fill_in_the_blank`" not in fix_msg

        # 3. run.py telemetry line includes M20 share
        run_text = (C2C_DIR / "run.py").read_text(encoding="utf-8")
        assert "M20={mod_l.get('bloom_superior_share_pct', 0.0)}%" in run_text

        # 4. c2c_hook_guard.py edit_file guidance
        guard_text = (C2C_DIR / "c2c_hook_guard.py").read_text(encoding="utf-8")
        assert "modalidades alineadas al plan del CTA (M20 / FIB / MS / MC7)" in guard_text
        assert "FIB/MS obligatorio" not in guard_text

        # 5. plan_shards.py FIB tag
        rules = plan_shards.DSL_REFERENCE["rules"]
        assert "[TPL-FIB-KATEX]" in rules["fib_naked_contract"]
        assert "[FIB-NAKED]" not in rules["fib_naked_contract"]
