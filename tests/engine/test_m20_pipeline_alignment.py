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
from engine.assemble import _coerce_num_if_numeric
from engine.invariants import check_instance_invariants
from validator.core import validate_course_content
from validator.rules import check_extended_quality_rules


CANONICAL_8_MODALITIES = {
    "multiple_choice_7_options",
    "multiple_select",
    "fill_in_the_blank",
    "open_symbolic",
    "proof_dag",
    "adversarial_break",
    "unstructured_model",
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
    def test_canonical_modality_sets_match_8_modalities(self):
        assert compile_cta._CANONICAL_MODALITIES == CANONICAL_8_MODALITIES
        assert check_cta._VALID_RECOMMENDED_MODALITIES == CANONICAL_8_MODALITIES

    def test_normalize_recommended_modalities_aliases_and_dedup(self):
        raw = ["MC7", "ms", "fib", "sym", "proof", "fallacy", "stage0", "matching", "mc", "open_symbolic"]
        normalized = compile_cta._normalize_recommended_modalities(raw, cid="Hab-01")
        assert normalized == [
            "multiple_choice_7_options",
            "multiple_select",
            "fill_in_the_blank",
            "open_symbolic",
            "proof_dag",
            "adversarial_break",
            "unstructured_model",
            "concept_matching",
        ]
        assert compile_cta._normalize_recommended_modalities("proof, sym, proof", cid="C-01") == [
            "proof_dag",
            "open_symbolic",
        ]
        assert compile_cta._normalize_recommended_modalities(None, cid="C-01") == []

    def test_normalize_recommended_modalities_rejects_invalid_with_error_code(self):
        for bad in ("bogus_modality", "invariant_canvas", "canvas"):
            with pytest.raises(ValueError) as excinfo:
                compile_cta._normalize_recommended_modalities(["open_symbolic", bad], cid="Hab-09")
            msg = str(excinfo.value)
            assert "[CTA-MODALITY-INVALID]" in msg
            assert "Hab-09" in msg

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

        good_tuples = [(*bad_tuples[0][:10], ["sym", "ms", "proof"])]
        compiled = compile_cta.compile_cta_module(good_tuples, require_assumptions=True, contract_version=2)
        assert compiled["competencies"][0]["recommended_modalities"] == [
            "open_symbolic",
            "multiple_select",
            "proof_dag",
        ]

    def test_check_cta_accepts_8_canonical_and_rejects_invalid_or_canvas(self):
        manifest = _make_manifest()
        all_canonical = sorted(CANONICAL_8_MODALITIES)
        for chunk in (all_canonical[0:3], all_canonical[3:6], all_canonical[5:8]):
            valid_cta = _make_valid_cta_dict(rec_mods=chunk)
            res_ok = check_cta.validate_cta_rules(valid_cta, manifest_data=manifest, require_assumptions=True)
            assert res_ok.valid, f"Expected valid CTA with modalities {chunk}, got: {res_ok.errors}"

            res_part_ok = check_cta.check_cta_part(valid_cta, manifest_data=manifest, require_assumptions=True)
            assert res_part_ok.valid, f"Expected valid cta_part for {chunk}, got: {res_part_ok.errors}"

        for bad_val in (["open_symbolic", "bogus_modality"], ["open_symbolic", "invariant_canvas"], ["FIB"], [123], "open_symbolic"):
            bad_cta = _make_valid_cta_dict(rec_mods=bad_val, cid="Hab-07")
            res_bad = check_cta.validate_cta_rules(bad_cta, manifest_data=manifest, require_assumptions=True)
            assert not res_bad.valid
            assert any("[CTA-MODALITY-INVALID]" in e and "Hab-07" in e for e in res_bad.errors), (
                f"Expected [CTA-MODALITY-INVALID] for {bad_val!r}, got {res_bad.errors}"
            )
            res_part_bad = check_cta.check_cta_part(bad_cta, manifest_data=manifest, require_assumptions=True)
            assert any("[CTA-MODALITY-INVALID]" in e and "Hab-07" in e for e in res_part_bad.errors)


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

        # 5. concept_matching
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
