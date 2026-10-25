"""End-to-End Forensic Verification Suite: Shard 06 & Variance v3.4 (Gate 2 / Stream 2A).

Comprehensive verification of all 6 forensic findings (F-01 through F-06):
1. F-01 & F-02:
   - KaTeX fraction shielding in `sanitize_katex_syntax`: leaves Hausman variance expressions
     \\frac{(b_{IV} - b_{LS})^2}{\\text{Var}[b_{IV}] + \\text{Var}[b_{LS}]} completely intact,
     shielded against false closures (`b_}{LS}`), while repairing genuine dropped braces.
   - `assemble_question` preserves explicit author `error_rationale` in MC7 and MS over CTA map,
     with safe fallback to CTA when author rationale is generic/placeholder, discarding broken LaTeX.
   - Full instantiation of real production `Hab-06.json` with 0 invariant violations.
2. F-03:
   - 4 Disjoint Archetypes under Milestone 3 (Directo, Inverso, Perturbación, Frontera)
     compiled with DRY compact distractor format (2-tuples, compact dicts, bare values)
     without 24x redundant error_rationale definitions.
3. F-04:
   - Surgical R-20 LaTeX error diagnostics identifying exact field, distractor ID, and open/close brace counts.
   - Target path parity in `render_compact_aggregated_errors` prioritizing real relative paths.
   - Receipt JSON (`--output`) and Post-PASS marker (`.check_attempts/pass_shard_06.json`) lifecycle.
4. F-05:
   - `dispatch_authors` Turn-0 rich context injection (`correct_belief`, 6 structured distractors,
     anti-PDF-reading autosufficiency directive, domain-agnostic).
   - `dispatch_repair` cleanup of `pass_<shard_id>.json` and sticky compile attempts.
5. F-06:
   - `c2c_hook_guard.py` enforcing Rule A (worker python path isolation against ad-hoc debug scripts),
     Rule B (early cut post-PASS), and Rule C (anti-monolithic rewrite guard for > 250 lines).
   - Absolute immunity for `shard_fixes/` and auditor exemptions.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import sys
import tempfile
import time
import unittest
from pathlib import Path
from typing import Any, Dict

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / ".agents" / "skills" / "content-to-course"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from c2c_hook_guard import process_hook
from check_templates import (
    check_single_template,
    format_invariant_error_diagnostic,
    render_compact_aggregated_errors,
)
from compile_shard import compile_shard
from dispatch import dispatch_authors, dispatch_repair, get_type_definitions
from engine.assemble import (
    _is_generic_placeholder,
    _resolve_distractor_rationale,
    assemble_question,
    sanitize_katex_syntax,
)
from engine.instantiate import instantiate_template
from engine.invariants import check_instance_invariants, validate_katex_syntax


# ==============================================================================
# 0. SUBAGENT CATALOG SYNCHRONIZATION CHECK
# ==============================================================================

class TestCatalogSynchronization:
    """Verifies subagent_types.json is in complete parity with dispatch.get_type_definitions(lean=False)."""

    def test_subagent_types_json_matches_get_type_definitions(self):
        types_file = SKILL_DIR / "subagent_types.json"
        assert types_file.is_file(), f"subagent_types.json missing from {SKILL_DIR}"

        disk_content = json.loads(types_file.read_text(encoding="utf-8"))
        mem_types = get_type_definitions(lean=False)

        assert disk_content == mem_types, (
            "subagent_types.json on disk is out of sync with dispatch.get_type_definitions(lean=False)"
        )
        assert len(disk_content) >= 4
        names = {t["name"] for t in disk_content}
        assert {"c2c_cta_architect", "c2c_shard_author", "c2c_judge", "c2c_repair"}.issubset(names)


# ==============================================================================
# 1. F-01 & F-02: KATEX SANITIZATION & AUTHOR ERROR_RATIONALE PRESERVATION
# ==============================================================================

class TestF01AndF02KaTeXAndRationale:
    """Verifies KaTeX formula shielding and priority preservation of author error_rationale."""

    def test_sanitize_katex_hausman_variance_formula_unmodified(self):
        """b_{IV} - b_{LS} and denominator subscripts/brackets must remain completely intact."""
        hausman_expr = r"$H = \frac{(b_{IV} - b_{LS})^2}{\text{Var}[b_{IV}] + \text{Var}[b_{LS}]}$"
        sanitized = sanitize_katex_syntax(hausman_expr)
        assert sanitized == hausman_expr
        assert "_}{LS}" not in sanitized
        assert "_}{" not in sanitized
        assert "^}{" not in sanitized

    def test_sanitize_katex_shielded_even_with_unclosed_brace_elsewhere(self):
        """Unclosed braces elsewhere in the string must not cause fraction corruption."""
        target_frac = r"\frac{(b_{IV} - b_{LS})^2}{\text{Var}(b_{IV}) - \text{Var}(b_{LS})}"
        complex_text = f"Considere el estimador ${target_frac}$ con {{parametro_sin_cerrar"
        sanitized = sanitize_katex_syntax(complex_text)
        assert target_frac in sanitized
        assert "_}{LS}" not in sanitized

    def test_sanitize_katex_repairs_genuine_missing_numerator_brace(self):
        """Legitimate broken numerators such as \\frac{a_{1}{b} must be safely repaired."""
        broken = r"\frac{a_{1}{b}"
        repaired = sanitize_katex_syntax(broken)
        assert repaired == r"\frac{a_{1}}{b}"

    def test_sanitize_katex_nested_complex_subscripts_and_superscripts(self):
        """Adversarial KaTeX formulas with deep nested subscripts/superscripts must remain intact."""
        adversarial_formulas = [
            r"$\hat{\beta}_{IV}^{(k)} = \frac{\sum_{i=1}^n (z_i - \bar{z})(y_i - \bar{y})}{\sum_{i=1}^n (z_i - \bar{z})(x_i - \bar{x})}$",
            r"$H = \frac{(\hat{\beta}_{IV, \text{2SLS}} - \hat{\beta}_{LS, \text{OLS}})^2}{\widehat{\text{Var}}[\hat{\beta}_{IV}] - \widehat{\text{Var}}[\hat{\beta}_{LS}]}$",
            r"$\sigma^2_{\hat{\beta}_{IV}} = \sigma^2 (X' P_Z X)^{-1} X' P_Z X (X' P_Z X)^{-1}$",
            r"$\Delta y_{i, t} = \beta_{\Delta} \Delta S_{i, t} + \Delta \varepsilon_{i, t}$",
        ]
        for formula in adversarial_formulas:
            sanitized = sanitize_katex_syntax(formula)
            assert sanitized == formula
            assert "_}{" not in sanitized
            assert "^}{" not in sanitized
            errs = validate_katex_syntax(sanitized, "formula")
            assert len(errs) == 0, f"KaTeX validation error on {sanitized}: {errs}"

    def test_assemble_question_preserves_author_explicit_rationale_mc7(self):
        """Author's explicit error_rationale must NOT be overwritten by CTA distractors map in MC7."""
        author_rationale = "Razonamiento analítico específico del autor sobre varianza de Hausman."
        cta_map = {
            "D-Hab06-01": {
                "manifestation": r"$b_{IV} - b_{LS} = 0$",
                "wrong_belief": "Creencia errónea del CTA",
                "remediation_hint": "Pista del CTA",
            }
        }
        d_dict = {
            "distractor_id": "D-Hab06-01",
            "value": "$b_{IV} - b_{LS}$",
            "error_rationale": author_rationale,
        }
        res = _resolve_distractor_rationale(
            d_dict=d_dict,
            d_id="D-Hab06-01",
            cta_distractors_map=cta_map,
            default_fallback="Fallback por defecto",
        )
        assert res == author_rationale

    def test_assemble_question_safe_cta_fallback_when_author_rationale_placeholder(self):
        """Generic placeholders ('placeholder', 'None', '', etc.) must safely inherit from CTA map."""
        cta_map = {
            "D-Hab06-02": {
                "manifestation": r"$\text{Var}[b_{IV}] < 0$",
                "wrong_belief": "Varianza estimada no puede ser negativa.",
                "remediation_hint": "Verifique los supuestos asintóticos.",
            }
        }
        for placeholder in ["placeholder", "Dummy rationale", "Static", "None", "", "   ", "Distractor."]:
            d_dict = {
                "distractor_id": "D-Hab06-02",
                "value": "$V_{IV}$",
                "error_rationale": placeholder,
            }
            res = _resolve_distractor_rationale(
                d_dict=d_dict,
                d_id="D-Hab06-02",
                cta_distractors_map=cta_map,
                default_fallback="Fallback por defecto",
            )
            assert res == r"$\text{Var}[b_{IV}] < 0$"

    def test_assemble_question_skips_broken_latex_in_cta_manifestation(self):
        """If CTA manifestation contains broken LaTeX, fallback cascades to wrong_belief."""
        cta_map = {
            "D-Hab06-03": {
                "manifestation": r"$\frac{broken{expression$",  # Missing closing brace
                "wrong_belief": "El sesgo de atenuación es severo.",
                "remediation_hint": "Considere la varianza del instrumento.",
            }
        }
        d_dict = {
            "distractor_id": "D-Hab06-03",
            "value": "$V_{LS}$",
            "error_rationale": "",
        }
        res = _resolve_distractor_rationale(
            d_dict=d_dict,
            d_id="D-Hab06-03",
            cta_distractors_map=cta_map,
            default_fallback="Fallback por defecto",
        )
        assert res == "El sesgo de atenuación es severo."

    def test_legacy_shard06_exact_code_compiles_cleanly(self, tmp_path: Path):
        """Preserves regression test for the original 1-tuple shard_06_data.py code that experienced 10 failures in 0b8b5084.

        Validates that it compiles with success=True, 0 errors, preserving explicit author error_rationale
        and without b_{LS} corruption to b_}{LS}.
        """
        work_dir = tmp_path / "work"
        shards_dir = work_dir / "shards"
        templates_dir = work_dir / "templates"
        shards_dir.mkdir(parents=True, exist_ok=True)
        templates_dir.mkdir(parents=True, exist_ok=True)

        # Extract Hab-06 competency definition from real cta.json
        real_cta_path = REPO_ROOT / "courses" / "asyntotic_estatistics_v4" / "work" / "cta.json"
        assert real_cta_path.is_file(), f"Real cta.json missing at {real_cta_path}"
        real_cta_data = json.loads(real_cta_path.read_text(encoding="utf-8"))
        hab06_comp = [c for c in real_cta_data.get("competencies", []) if c.get("id") == "Hab-06"]
        assert len(hab06_comp) == 1, "Hab-06 missing from real cta.json"

        isolated_cta = {"competencies": hab06_comp}
        cta_file = work_dir / "cta.json"
        cta_file.write_text(json.dumps(isolated_cta, indent=2, ensure_ascii=False), encoding="utf-8")

        shard_py = shards_dir / "shard_06_data.py"
        manifest_file = shards_dir / "pre_shard_manifest.json"
        manifest_payload = {
            "course_id": "asyntotic_estatistics_v4",
            "shards": [
                {
                    "shard_id": "shard_06",
                    "competency_ids": ["Hab-06"],
                    "shard_data_path": str(shard_py.resolve().as_posix()),
                    "templates_dir": str(templates_dir.resolve().as_posix()),
                    "competencies": hab06_comp,
                }
            ],
        }
        manifest_file.write_text(json.dumps(manifest_payload, indent=2, ensure_ascii=False), encoding="utf-8")

        # The exact 1-tuple code that failed 10 times in 0b8b5084
        legacy_code = '''"""
Parametric Exercise Templates for Shard 06
Competency: Hab-06 (Estimación con Datos de Gemelos, Ratio de Fiabilidad y Corrección de Endogeneidad)
Clean-Room Standard v3.21
"""

def gen_hab06(rng):
    b_iv = round(rng.randint(150, 450) * 0.001, 3)
    b_ls = round(rng.randint(20, 120) * 0.001, 3)
    q = round(rng.randint(60, 95) * 0.01, 2)
    rho = round(rng.randint(40, 85) * 0.01, 2)

    v_iv = round(rng.randint(80, 250) * 0.0001, 4)
    v_ls = round(rng.randint(10, 50) * 0.0001, 4)

    denom = round(v_iv - v_ls, 4)
    diff = round(b_iv - b_ls, 3)

    ans = round((diff ** 2) / denom, 3)

    d1 = round(((b_iv - b_ls * q) ** 2) / denom, 3)
    d2 = round(((b_iv - b_ls * round(1.0 - q, 2)) ** 2) / denom, 3)
    d3 = round(((2.0 * b_ls - b_iv) ** 2) / denom, 3)
    d4 = round((diff ** 2) / round(v_iv + v_ls, 4), 3)
    d5 = round((diff ** 2) / v_iv, 3)
    d6 = round(((diff / q) ** 2) / denom, 3)

    vals = [ans]
    dists_raw = [d1, d2, d3, d4, d5, d6]
    adjusted = []
    for d in dists_raw:
        cur = d
        step = 0.015
        while any(abs(cur - v_other) < 1e-3 for v_other in vals + adjusted):
            cur = round(cur + step, 3)
        adjusted.append(round(cur, 3))

    d1, d2, d3, d4, d5, d6 = adjusted

    v = {
        "b_ls": b_ls,
        "b_iv": b_iv,
        "v_ls": v_ls,
        "v_iv": v_iv,
        "q": q,
        "rho": rho,
        "diff": diff,
        "denom": denom,
        "ans": ans,
        "d1": d1,
        "d2": d2,
        "d3": d3,
        "d4": d4,
        "d5": d5,
        "d6": d6,
    }

    dists = [
        {"value": r"H = @d1@", "distractor_id": "D-Hab06-01", "error_rationale": "Omite el agravamiento del sesgo de atenuacion tras primeras diferencias."},
        {"value": r"H = @d2@", "distractor_id": "D-Hab06-02", "error_rationale": "Confunde el ratio de fiabilidad con la proporcion de varianza de ruido."},
        {"value": r"H = @d3@", "distractor_id": "D-Hab06-03", "error_rationale": "Asume que MCO supera a VI debido al sesgo de habilidad."},
        {"value": r"H = @d4@", "distractor_id": "D-Hab06-04", "error_rationale": "Suma las varianzas en el denominador del estadistico de Hausman."},
        {"value": r"H = @d5@", "distractor_id": "D-Hab06-05", "error_rationale": "Omite la varianza de MCO en el denominador del estadistico."},
        {"value": r"H = @d6@", "distractor_id": "D-Hab06-06", "error_rationale": "Aplica incorrectamente el factor de atenuacion dividiendo por el ratio de fiabilidad."},
    ]

    return {"vars": v, "correct": r"H = @ans@", "distractors": dists}


def ver_hab06(res):
    if not isinstance(res, dict):
        return False
    v = res.get("vars", {})
    b_iv = v.get("b_iv")
    b_ls = v.get("b_ls")
    v_iv = v.get("v_iv")
    v_ls = v.get("v_ls")
    ans = v.get("ans")
    if any(x is None for x in [b_iv, b_ls, v_iv, v_ls, ans]):
        return False
    denom = round(v_iv - v_ls, 4)
    if abs(denom) < 1e-6:
        return False
    diff = round(b_iv - b_ls, 3)
    expected = round((diff ** 2) / denom, 3)
    return abs(ans - expected) < 1e-3


TEMPLATES = [
    (
        "Hab-06",
        "multiple_choice",
        [
            r"En un modelo salarial con datos de gemelos donde b_LS = @b_ls@, b_IV = @b_iv@, V_LS = @v_ls@, V_IV = @v_iv@, y ratio de fiabilidad q = @q@, calcule el estadistico de Hausman H:",
            r"A partir de estimaciones con datos de gemelos donde b_LS = @b_ls@, b_IV = @b_iv@, varianzas V_LS = @v_ls@, V_IV = @v_iv@, y q = @q@, halle el valor de H:",
            r"Para contrastar la presencia de endogeneidad en las diferencias entre gemelos con b_LS = @b_ls@, b_IV = @b_iv@, V_LS = @v_ls@ y V_IV = @v_iv@, determine el estadistico H:",
            r"Bajo la hipotesis nula de exogeneidad en el modelo de gemelos con estimadores b_LS = @b_ls@, b_IV = @b_iv@, V_LS = @v_ls@ y V_IV = @v_iv@, compute el estadistico H:",
        ],
        gen_hab06,
        ver_hab06,
        r"El estadistico de Hausman univariado es H = @ans@.",
        r"En el contraste de Hausman univariado para evaluar endogeneidad en datos de gemelos el estadistico escalar se define como H = (b_IV - b_LS)^2 / (V_IV - V_LS).",
        [
            "D-Hab06-01",
            "D-Hab06-02",
            "D-Hab06-03",
            "D-Hab06-04",
            "D-Hab06-05",
            "D-Hab06-06",
        ],
        (
            "ECONOMETRIC ANALTYSIS FIFTH EDITION  -  William H_ Greene  -  5th ed_, Upper Saddle River, N_J, New Jersey, 2003  -  Prentice Hall PTR  -  isbn13 9780130661890  -  d139b0dca2a0c7d0984d735f6be1944e  -  Anna’s Archive-93.pdf",
            25,
            "Estimación con Datos de Gemelos, Ratio de Fiabilidad y Corrección de Endogeneidad",
        ),
        [
            r"El numerador del estadistico de Hausman es la diferencia al cuadrado entre los estimadores.",
            r"El denominador del estadistico de Hausman es la resta de varianzas, nunca su suma.",
            r"Sustituyendo los valores del modelo se obtiene H = @ans@.",
        ],
    ),
]
'''
        shard_py.write_text(legacy_code, encoding="utf-8")

        success, errors = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_06",
            strict=True,
            seeds=50,
            cta_path=cta_file,
            manifest_path=manifest_file,
        )
        assert success, f"Expected successful compile of legacy shard_06, got errors: {errors}"
        assert len(errors) == 0

        compiled_json_path = templates_dir / "Hab-06.json"
        assert compiled_json_path.is_file(), f"Compiled template JSON not found at {compiled_json_path}"

        raw_compiled_text = compiled_json_path.read_text(encoding="utf-8")
        assert "b_}{LS}" not in raw_compiled_text, "False closure b_}{LS} detected in compiled template"
        assert "b_{LS}" in raw_compiled_text or "b_LS" in raw_compiled_text

        tpl_data = json.loads(raw_compiled_text)
        assert tpl_data.get("competency_id") == "Hab-06"
        ca_instances = instantiate_template(tpl_data, "Hab-06", target_count=3, seed_offset=42)
        assert len(ca_instances) == 3

        # Verify author error_rationale was strictly preserved for D-Hab06-04
        d4_rationales = [
            opt["error_rationale"]
            for q in ca_instances
            for opt in q["options"]
            if opt.get("distractor_id") == "D-Hab06-04"
        ]
        assert len(d4_rationales) >= 1
        for rat in d4_rationales:
            assert "Suma las varianzas en el denominador del estadistico de Hausman." in rat

    def test_real_hab06_template_instantiation_and_invariants(self):
        """Real Hab-06.json from courses/asyntotic_estatistics_v4 must contain 4 archetypes and instantiate with 0 errors."""
        real_hab06_path = REPO_ROOT / "courses" / "asyntotic_estatistics_v4" / "work" / "templates" / "Hab-06.json"
        assert real_hab06_path.is_file(), f"Real Hab-06.json missing at {real_hab06_path}"

        tpl_data = json.loads(real_hab06_path.read_text(encoding="utf-8"))
        assert tpl_data["competency_id"] == "Hab-06"
        assert "templates" in tpl_data
        templates_list = tpl_data["templates"]
        assert len(templates_list) == 4, f"Expected 4 archetypes in Hab-06.json, found {len(templates_list)}"

        for idx, sub_tpl in enumerate(templates_list):
            assert sub_tpl["interaction_type"] == "multiple_choice_7_options"
            assert sub_tpl["competency_id"] == "Hab-06"
            instantiated = instantiate_template(sub_tpl, "Hab-06", target_count=3, seed_offset=100 + idx * 50)
            assert len(instantiated) == 3
            for q in instantiated:
                is_valid, errs = check_instance_invariants(q, "multiple_choice_7_options")
                assert is_valid, f"Instance invariant failure on Hab-06 template {sub_tpl.get('id')}: {errs}"
                assert len(q["options"]) == 7
                assert "@" not in q["stem"]
                for opt in q["options"]:
                    assert "@" not in opt["content"]


# ==============================================================================
# 2. F-03: MILESTONE 3 4 DISJOINT ARCHETYPES & DRY COMPACT DISTRACTORS
# ==============================================================================

class TestF03Milestone3DisjointArchetypes:
    """Verifies compilation of the 4 disjoint archetypes with DRY distractor auto-inheritance."""

    def test_compile_four_disjoint_milestone3_archetypes_dry_distractors(self, tmp_path: Path):
        work_dir = tmp_path / "work"
        shards_dir = work_dir / "shards"
        templates_dir = work_dir / "templates"
        shards_dir.mkdir(parents=True, exist_ok=True)
        templates_dir.mkdir(parents=True, exist_ok=True)

        cta_payload = {
            "competencies": [
                {
                    "id": "Hab-M3",
                    "name": "Estimación de Parámetros y Diagnóstico de Robustez",
                    "distractors": [
                        {"id": "D-HabM3-01", "name": "Error de Signo", "remediation_hint": "Inversión de signo en el estimador."},
                        {"id": "D-HabM3-02", "name": "Omisión de Covarianza", "remediation_hint": "Omitir la covarianza entre regresores."},
                        {"id": "D-HabM3-03", "name": "Varianza No Consistente", "remediation_hint": "Uso de varianzas homocedásticas."},
                        {"id": "D-HabM3-04", "name": "Instrumento Débil", "remediation_hint": "Correlación insuficiente entre instrumento y endógena."},
                        {"id": "D-HabM3-05", "name": "Sesgo de Selección", "remediation_hint": "No corregir por truncamiento de la muestra."},
                        {"id": "D-HabM3-06", "name": "Identificación Exacta", "remediation_hint": "Asumir sobreidentificación cuando el rango es deficiente."},
                    ],
                }
            ]
        }
        (work_dir / "cta.json").write_text(json.dumps(cta_payload, indent=2), encoding="utf-8")

        # Native shard script defining 4 disjoint archetypes using compact DRY distractor formats:
        # Archetype 1 (Directo): 2-tuple ("D-HabM3-01", r"$@d1@$")
        # Archetype 2 (Inverso): Compact dict {"distractor_id": "D-HabM3-02", "value": r"$@d2@$"}
        # Archetype 3 (Perturbación): Inverted 2-tuple (r"$@d1@$", "D-HabM3-01")
        # Archetype 4 (Frontera): Bare numeric/string formats
        shard_source = '''
import random

def gen_directo(rng):
    base = rng.randint(20, 60)
    step = rng.randint(2, 8)
    ans = base * step
    v = {"base": base, "step": step, "ans": ans}
    for i in range(1, 7):
        v[f"d{i}"] = ans + i * 5
    dists = [(f"D-HabM3-0{i}", f"$@d{i}@$") for i in range(1, 7)]
    return {"vars": v, "correct": "$@ans@$", "distractors": dists}

def ver_directo(res):
    v = res["vars"]
    return v["ans"] == v["base"] * v["step"]

def gen_inverso(rng):
    ans = rng.randint(10, 50)
    div = rng.choice([2, 4, 5, 10])
    total = ans * div
    v = {"total": total, "div": div, "ans": ans}
    for i in range(1, 7):
        v[f"d{i}"] = ans + (i * 3)
    dists = [{"distractor_id": f"D-HabM3-0{i}", "value": f"$@d{i}@$"} for i in range(1, 7)]
    return {"vars": v, "correct": "$@ans@$", "distractors": dists}

def ver_inverso(res):
    v = res["vars"]
    return v["ans"] * v["div"] == v["total"]

def gen_perturbacion(rng):
    x = rng.randint(10, 40)
    delta = rng.choice([1, 2, 3])
    ans = (x + delta) ** 2
    v = {"x": x, "delta": delta, "ans": ans}
    for i in range(1, 7):
        v[f"d{i}"] = ans - (i * 7)
    dists = [(f"$@d{i}@$", f"D-HabM3-0{i}") for i in range(1, 7)]
    return {"vars": v, "correct": "$@ans@$", "distractors": dists}

def ver_perturbacion(res):
    v = res["vars"]
    return v["ans"] == (v["x"] + v["delta"]) ** 2

def gen_frontera(rng):
    k = rng.randint(5, 25)
    ans = round(1.0 / k, 4)
    v = {"k": k, "ans": ans}
    for i in range(1, 7):
        v[f"d{i}"] = round((1.0 + i * 0.1) / k, 4)
    dists = [f"$@d{i}@$" for i in range(1, 7)]
    return {"vars": v, "correct": "$@ans@$", "distractors": dists}

def ver_frontera(res):
    v = res["vars"]
    return abs(v["ans"] * v["k"] - 1.0) < 1e-3

TEMPLATES = [
    (
        "Hab-M3",
        "multiple_choice",
        [
            r"Enfoque Directo: Dados $@base@$ y $@step@$, halle el producto:",
            r"Cálculo frontal estándar de $@base@$ multiplicado por $@step@$:",
            r"Multiplique directamente $@base@$ y $@step@$:"
        ],
        gen_directo,
        ver_directo,
        r"El resultado directo es $@ans@$.",
        "Directo",
        ["D-HabM3-01", "D-HabM3-02", "D-HabM3-03", "D-HabM3-04", "D-HabM3-05", "D-HabM3-06"],
        ("doc.pdf", 1, "Directo"),
        ["Pista 1", "Pista 2", "Pista 3"]
    ),
    (
        "Hab-M3",
        "multiple_choice",
        [
            r"Enfoque Inverso: Dado el total $@total@$ y divisor $@div@$, determine el cociente:",
            r"Resolución inversa para recuperar la cantidad base de $@total@$ dividido $@div@$:",
            r"Halle la inversa de $@total@$ sobre $@div@$:"
        ],
        gen_inverso,
        ver_inverso,
        r"El resultado inverso es $@ans@$.",
        "Inverso",
        ["D-HabM3-01", "D-HabM3-02", "D-HabM3-03", "D-HabM3-04", "D-HabM3-05", "D-HabM3-06"],
        ("doc.pdf", 2, "Inverso"),
        ["Pista 1", "Pista 2", "Pista 3"]
    ),
    (
        "Hab-M3",
        "multiple_choice",
        [
            r"Enfoque Perturbación: Considere $@x@$ perturbado por $@delta@$:",
            r"Análisis de estática comparativa tras sumar $@delta@$ a $@x@$:",
            r"Evalúe la perturbación sobre $@x@$ con incremento $@delta@$:"
        ],
        gen_perturbacion,
        ver_perturbacion,
        r"La perturbación evaluada es $@ans@$.",
        "Perturbación",
        ["D-HabM3-01", "D-HabM3-02", "D-HabM3-03", "D-HabM3-04", "D-HabM3-05", "D-HabM3-06"],
        ("doc.pdf", 3, "Perturbación"),
        ["Pista 1", "Pista 2", "Pista 3"]
    ),
    (
        "Hab-M3",
        "multiple_choice",
        [
            r"Enfoque Frontera: Con parámetro límite $@k@$, determine el recíproco:",
            r"Evaluación en régimen asintótico o de frontera para $@k@$:",
            r"Halle el caso límite de $1/@k@$:"
        ],
        gen_frontera,
        ver_frontera,
        r"El valor de frontera es $@ans@$.",
        "Frontera",
        ["D-HabM3-01", "D-HabM3-02", "D-HabM3-03", "D-HabM3-04", "D-HabM3-05", "D-HabM3-06"],
        ("doc.pdf", 4, "Frontera"),
        ["Pista 1", "Pista 2", "Pista 3"]
    ),
]
'''
        shard_py = shards_dir / "shard_m3_data.py"
        shard_py.write_text(shard_source, encoding="utf-8")

        manifest_data = {
            "shards": [
                {
                    "shard_id": "shard_m3",
                    "competency_ids": ["Hab-M3"],
                    "shard_data_path": str(shard_py.resolve().as_posix()),
                    "templates_dir": str(templates_dir.resolve().as_posix()),
                }
            ]
        }
        (shards_dir / "pre_shard_manifest.json").write_text(json.dumps(manifest_data, indent=2), encoding="utf-8")

        # Compile in strict mode with 50 dry-run seeds
        success, errors = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_m3",
            strict=True,
            seeds=50,
            cta_path=work_dir / "cta.json",
        )
        assert success, f"Milestone 3 compilation failed: {errors}"
        assert len(errors) == 0

        # Check output template
        out_tpl = templates_dir / "Hab-M3.json"
        assert out_tpl.is_file()
        tpl_data = json.loads(out_tpl.read_text(encoding="utf-8"))
        assert tpl_data["competency_id"] == "Hab-M3"
        assert len(tpl_data["templates"]) == 4

        # Verify DRY distractor rationales were inherited from CTA into archetypes
        gen_code = tpl_data["templates"][0]["generator_code"]
        assert "Inversión de signo en el estimador." in gen_code
        assert "Omitir la covarianza entre regresores." in gen_code


# ==============================================================================
# 3. F-04: SURGICAL R-20 DIAGNOSTICS, PATH PARITY & RECEIPT LIFECYCLE
# ==============================================================================

class TestF04SurgicalDiagnosticsAndReceipts:
    """Verifies R-20 surgical error reporting, relative paths in aggregated errors, and receipt lifecycle."""

    def test_surgical_r20_diagnostic_pinpoints_field_and_counts(self):
        inv_err = r"LaTeX math expression in option 2 error_rationale has unbalanced braces: '\frac{b_{IV} - b_{LS}{V_{IV}}'"
        q_obj = {
            "options": [
                {"content": "$A$", "is_correct": True},
                {
                    "content": "$B$",
                    "is_correct": False,
                    "distractor_id": "D-Hab06-02",
                    "error_rationale": r"\frac{b_{IV} - b_{LS}{V_{IV}}",
                },
            ]
        }
        diag = format_invariant_error_diagnostic(
            cid="Hab-06",
            tpl_id="T-Hab06-01",
            q_id="Q-001",
            inv_err=inv_err,
            q_obj=q_obj,
        )
        assert diag.field_name == "options[1].error_rationale (distractor D-Hab06-02)"
        assert "options[1].error_rationale (distractor D-Hab06-02)" in diag.cause
        assert "open=" in diag.cause and "close=" in diag.cause
        assert any("Balancear" in a for a in diag.actions)

    def test_surgical_r20_detects_inverted_subscript_pattern(self):
        inv_err = "LaTeX math expression in option 2 content has unbalanced braces: $H = \\hat{\\beta}_}{1}$"
        q_obj = {
            "options": [
                {"content": "$A$", "is_correct": True},
                {"content": r"$H = \hat{\beta}_}{1}$", "is_correct": False, "distractor_id": "D-Hab06-02"},
            ]
        }
        diag = format_invariant_error_diagnostic(
            cid="Hab-06",
            tpl_id="T-Hab06-01",
            q_id="Q-001",
            inv_err=inv_err,
            q_obj=q_obj,
        )
        assert "patrón invertido" in diag.cause and "open=" in diag.cause and "_}{" in diag.cause

    def test_render_compact_aggregated_errors_uses_real_relative_path(self):
        from check_templates import format_diagnostic_error
        real_target = REPO_ROOT / "courses" / "asyntotic_estatistics_v4" / "work" / "templates" / "Hab-06.json"
        diag_err = format_diagnostic_error(
            rule_tag="R-20: SINTAXIS / LLAVES",
            competency="Hab-06",
            template="T-Hab-06",
            item_id="N/A",
            field_name="options[1].error_rationale",
            snippet=r"\frac{a}{b}",
            cause="Unbalanced braces in LaTeX expression",
            actions=["Balance braces"],
        )
        rendered = render_compact_aggregated_errors([diag_err], targets=[real_target])
        assert "courses/asyntotic_estatistics_v4/work/templates/Hab-06.json" in rendered
        assert not any(line.strip().startswith("[FILE work/templates/Hab-06.json") for line in rendered.splitlines())
        assert not any("work/templates/Hab-06.json" in line and "courses/" not in line for line in rendered.splitlines())
        assert any("courses/asyntotic_estatistics_v4/work/templates/Hab-06.json" in line for line in rendered.splitlines())

    def test_real_shard06_receipt_and_pass_marker_verified(self):
        """Verifies courses/asyntotic_estatistics_v4 real shard_06 receipt and pass marker."""
        shard_receipt = REPO_ROOT / "courses" / "asyntotic_estatistics_v4" / "work" / "shards" / "shard_06.json"
        assert shard_receipt.is_file(), f"Receipt file missing at {shard_receipt}"
        receipt_data = json.loads(shard_receipt.read_text(encoding="utf-8"))
        assert receipt_data.get("compiled_status") == "PASS"
        assert len(receipt_data.get("compiled_templates", [])) >= 1

        pass_file = REPO_ROOT / "courses" / "asyntotic_estatistics_v4" / "work" / ".check_attempts" / "pass_shard_06.json"
        assert pass_file.is_file(), f"Pass marker missing at {pass_file}"
        pass_data = json.loads(pass_file.read_text(encoding="utf-8"))
        assert pass_data.get("status") == "PASS"
        assert pass_data.get("shard_id") == "shard_06"
        assert pass_data.get("template_counts", {}).get("Hab-06") == 4

    def test_pass_marker_unlinked_on_compile_failure(self, tmp_path: Path):
        """If compilation fails, existing pass marker must be unlinked."""
        work_dir = tmp_path / "work"
        shards_dir = work_dir / "shards"
        check_dir = work_dir / ".check_attempts"
        shards_dir.mkdir(parents=True, exist_ok=True)
        check_dir.mkdir(parents=True, exist_ok=True)

        stale_pass = check_dir / "pass_shard_fail.json"
        stale_pass.write_text(json.dumps({"status": "PASS", "shard_id": "shard_fail"}), encoding="utf-8")

        bad_shard = shards_dir / "shard_fail_data.py"
        bad_shard.write_text("INVALID PYTHON SYNTAX :::", encoding="utf-8")

        (shards_dir / "pre_shard_manifest.json").write_text(json.dumps({
            "shards": [{"shard_id": "shard_fail", "competency_ids": ["Hab-99"]}]
        }), encoding="utf-8")

        success, errors = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_fail",
            strict=True,
        )
        assert success is False
        assert not stale_pass.is_file(), "Stale pass marker must be unlinked on compilation failure"

    def test_windows_posix_path_normalization_adversarial(self, tmp_path: Path):
        """Path locators and receipt paths must tolerate mixed Windows backslashes and POSIX slashes."""
        from check_templates import normalize_error_string_for_hash
        win_path = r"D:\Augusto\personal_portfolio\Tops_academy\courses\course_01\work\templates\Hab-06.json"
        posix_path = "D:/Augusto/personal_portfolio/Tops_academy/courses/course_01/work/templates/Hab-06.json"
        norm_win = normalize_error_string_for_hash(win_path)
        norm_posix = normalize_error_string_for_hash(posix_path)
        assert "\\" not in norm_win
        assert "\\" not in norm_posix
        assert norm_win == norm_posix

    def test_cli_backward_compatibility_dual_invocation_and_error_handling(self, tmp_path: Path):
        """compile_shard must support both directory-based and file-based invocations, failing cleanly on missing inputs."""
        # Missing file error
        non_existent = tmp_path / "non_existent_shard_data.py"
        success, errors = compile_shard(str(non_existent))
        assert not success
        assert any("No existe" in e for e in errors)

        # Missing shard_id in directory
        empty_dir = tmp_path / "empty_dir"
        empty_dir.mkdir(parents=True, exist_ok=True)
        success2, errors2 = compile_shard(empty_dir, shard_id=None)
        assert not success2
        assert any("shard_id no especificado" in e for e in errors2)


# ==============================================================================
# 4. F-05: TURN-0 CONTEXT & REPAIR PASS-MARKER CLEANUP
# ==============================================================================

class TestF05Turn0ContextAndRepairCleanup:
    """Verifies Turn-0 context injection, anti-PDF-reading directive, and dispatch_repair cleanup."""

    def test_dispatch_authors_turn0_rich_context_and_anti_pdf_reading(self, tmp_path: Path):
        work_dir = tmp_path / "work"
        work_dir.mkdir(parents=True, exist_ok=True)

        (work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "course_id": "test_course_turn0",
            "documents": [{"name": "lecture.pdf", "path": "content/lecture.pdf", "total_pages": 10, "valid_page_range": [1, 10]}],
        }), encoding="utf-8")

        (work_dir / "cta.json").write_text(json.dumps({
            "competencies": [
                {
                    "id": "Hab-55",
                    "type": "skill",
                    "name": "Cálculo de Invariantes Cuantitativos",
                    "description_latex": r"$\int_a^b f(x) dx$",
                    "bloom": "Apply",
                    "distractors": [
                        {
                            "id": "D-Hab55-01",
                            "name": "Error de Límites",
                            "wrong_belief": r"$F(a) - F(b)$",
                            "correct_belief": r"$F(b) - F(a)$",
                            "manifestation": r"$-10$",
                            "remediation_hint": "Invierta el orden de evaluación.",
                            "omitted_step": "Omitir verificar el signo del integrando.",
                        }
                    ],
                }
            ]
        }), encoding="utf-8")

        shards_dir = work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)
        (shards_dir / "pre_shard_manifest.json").write_text(json.dumps({
            "course_id": "test_course_turn0",
            "shards": [{"shard_id": "shard_55", "competency_ids": ["Hab-55"]}],
        }), encoding="utf-8")

        res = dispatch_authors(work_dir, pointer=False)
        subagents = res.get("Subagents") or res.get("subagents", [])
        assert len(subagents) == 1

        prompt = subagents[0]["Prompt"]
        assert "AUTOSUFICIENCIA TURN-0 (CERO LECTURA INNECESARIA DE PDFs)" in prompt
        assert ("Creencia Correcta" in prompt or "correct_belief" in prompt) and r"$F(b) - F(a)$" in prompt
        assert ("Remediation Hint" in prompt or "remediation_hint" in prompt) and "Invierta el orden de evaluación." in prompt
        assert "Corte Inmediato Post-PASS" in prompt
        assert "DONE: work/shards/shard_55.json" in prompt

    def test_dispatch_repair_clears_pass_and_sticky_attempt_files(self, tmp_path: Path):
        work_dir = tmp_path / "work"
        work_dir.mkdir(parents=True, exist_ok=True)
        (work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "course_id": "test_repair_cleanup",
            "documents": [{"name": "book.pdf", "path": "content/book.pdf"}],
        }), encoding="utf-8")
        (work_dir / "cta.json").write_text(json.dumps({"course_id": "test_repair_cleanup"}), encoding="utf-8")

        shards_dir = work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)
        (shards_dir / "pre_shard_manifest.json").write_text(json.dumps({
            "shards": [{"shard_id": "shard_06", "competency_ids": ["Hab-06"]}],
        }), encoding="utf-8")

        check_dir = work_dir / ".check_attempts"
        check_dir.mkdir(parents=True, exist_ok=True)

        pass_file = check_dir / "pass_shard_06.json"
        pass_file.write_text(json.dumps({"status": "PASS", "shard_id": "shard_06"}), encoding="utf-8")

        compile_file = check_dir / "compile_shard_06.json"
        compile_file.write_text(json.dumps({"same_error_streak": 3, "last_errors": ["Error syntax"]}), encoding="utf-8")

        (work_dir / "reports").mkdir(parents=True, exist_ok=True)
        (work_dir / "reports" / "templates_report.json").write_text(json.dumps({
            "results": [{"cid": "Hab-06", "status": "fail", "errors": ["LaTeX math expression has unbalanced braces"]}],
        }), encoding="utf-8")

        res = dispatch_repair(work_dir)
        assert res is not None

        assert not pass_file.is_file(), "dispatch_repair must delete pass_shard_06.json to prevent post-PASS block"
        assert not compile_file.is_file(), "dispatch_repair must clear sticky compile attempt file"


# ==============================================================================
# 5. F-06: C2C_HOOK_GUARD RULES A, B, AND C
# ==============================================================================

class TestF06HookGuardRulesABC(unittest.TestCase):
    """Verifies c2c_hook_guard Rules A (Write Path Isolation), B (Post-PASS Early Cut), and C (Anti-Monolithic Rewrite)."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="c2c_hook_test_f06_")
        self.work_dir = Path(self.test_dir) / "courses" / "demo_f06" / "work"
        self.shards_dir = self.work_dir / "shards"
        self.shard_fixes_dir = self.shards_dir / "shard_fixes"
        self.check_dir = self.work_dir / ".check_attempts"

        self.shards_dir.mkdir(parents=True, exist_ok=True)
        self.shard_fixes_dir.mkdir(parents=True, exist_ok=True)
        self.check_dir.mkdir(parents=True, exist_ok=True)

        self.lock_file = Path(self.test_dir) / ".c2c_subagent_lock.json"
        self.lock_data = {
            "active": True,
            "director_conversation_id": "director-123",
            "course_id": "demo_f06",
            "work_dir": str(self.work_dir),
            "exempt_conversation_ids": ["auditor-999"],
        }
        self.lock_file.write_text(json.dumps(self.lock_data), encoding="utf-8")
        self.worker_conv = "worker-subagent-01"

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_rule_a_blocks_root_debug_scripts(self):
        # Attempt to write ad-hoc debug script in root
        resp = process_hook(
            {
                "conversationId": self.worker_conv,
                "toolCall": {
                    "name": "write_file",
                    "args": {"Path": "test_debug.py", "Content": "print('debug')"},
                },
            },
            custom_lock_file=str(self.lock_file),
        )
        self.assertEqual(resp["decision"], "deny")
        self.assertIn("BLOCKER", resp["reason"])
        self.assertIn("debug", resp["reason"])

        # Authorized worker path must be allowed
        resp_ok = process_hook(
            {
                "conversationId": self.worker_conv,
                "toolCall": {
                    "name": "write_file",
                    "args": {
                        "Path": str(self.shards_dir / "shard_01_data.py"),
                        "Content": "TEMPLATES = []",
                    },
                },
            },
            custom_lock_file=str(self.lock_file),
        )
        self.assertEqual(resp_ok["decision"], "allow")

    def test_rule_b_early_cut_blocks_post_pass(self):
        pass_marker = self.check_dir / "pass_shard_01.json"
        pass_marker.write_text(json.dumps({"status": "PASS", "shard_id": "shard_01"}), encoding="utf-8")

        # Worker trying to edit shard_01_data.py after PASS must be denied immediately
        resp = process_hook(
            {
                "conversationId": self.worker_conv,
                "toolCall": {
                    "name": "edit_file",
                    "args": {
                        "Path": str(self.shards_dir / "shard_01_data.py"),
                        "Target": "x",
                        "Replacement": "y",
                    },
                },
            },
            custom_lock_file=str(self.lock_file),
        )
        self.assertEqual(resp["decision"], "deny")
        self.assertIn("BLOCKER", resp["reason"])
        self.assertTrue("STOP" in resp["reason"] or "ya aprobó" in resp["reason"])

    def test_rule_c_anti_monolithic_rewrite_guard(self):
        shard_file = self.shards_dir / "shard_02_data.py"
        # Create a large file (> 250 lines)
        shard_file.write_text("\n".join([f"# line {i}" for i in range(300)]), encoding="utf-8")

        # Record a prior compile failure in .check_attempts with distinct_compiles >= 1
        (self.check_dir / "compile_shard_02.json").write_text(
            json.dumps({
                "distinct_compiles": 1,
                "same_error_streak": 1,
                "last_err_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                "last_errors": ["Error syntax"],
            }),
            encoding="utf-8",
        )

        # Monolithic write_file on existing large file must be blocked
        resp_block = process_hook(
            {
                "conversationId": self.worker_conv,
                "toolCall": {
                    "name": "write_file",
                    "args": {
                        "Path": str(shard_file),
                        "Content": "# complete rewrite",
                    },
                },
            },
            custom_lock_file=str(self.lock_file),
        )
        self.assertEqual(resp_block["decision"], "deny")
        self.assertIn("BLOCKER", resp_block["reason"])
        self.assertTrue("edit_file" in resp_block["reason"] or "shard_fixes" in resp_block["reason"])

        # Surgical edit_file must be allowed
        resp_edit = process_hook(
            {
                "conversationId": self.worker_conv,
                "toolCall": {
                    "name": "edit_file",
                    "args": {
                        "Path": str(shard_file),
                        "Target": "# line 10",
                        "Replacement": "# line 10 fixed",
                    },
                },
            },
            custom_lock_file=str(self.lock_file),
        )
        self.assertEqual(resp_edit["decision"], "allow")

        # Modular override in shard_fixes/ must be allowed unconditionally
        resp_fix = process_hook(
            {
                "conversationId": self.worker_conv,
                "toolCall": {
                    "name": "write_file",
                    "args": {
                        "Path": str(self.shard_fixes_dir / "Hab-02.py"),
                        "Content": "# modular fix",
                    },
                },
            },
            custom_lock_file=str(self.lock_file),
        )
        self.assertEqual(resp_fix["decision"], "allow")
