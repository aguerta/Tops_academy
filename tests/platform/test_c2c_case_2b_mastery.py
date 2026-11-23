"""Test Suite for Case 2B (Variedad Máxima / Deep Mastery: C=2, T=4) & Case 2A Reversibility.

Tests:
1. Shard Partitioning under Case 2B (C=2 max competencies per shard) and Case 2A (C=3).
2. Multi-Template Compilation (compile_shard.py) with C=2 and T=4 archetypes (8 tuples total):
   - Direct / Forward Computation
   - Inverse / Parameter Recovery
   - Comparative Statics / Perturbation
   - Boundary Testing / Counterexample
3. Automatic Template ID Disambiguation (T-<cid>-01 .. 04).
4. Template Quota Allocation (allocate_template_quotas) for T=4 and T=3 with full sum integrity (20 and 30).
5. Invariant & Diversity Validation with check_templates on multi-template containers.
"""

from __future__ import annotations

import json
import random
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List

import pytest

# Add skill root and project src to sys.path
_skill_root = Path(__file__).resolve().parents[2] / ".agents" / "skills" / "content-to-course"
if str(_skill_root) not in sys.path:
    sys.path.insert(0, str(_skill_root))

_src_root = Path(__file__).resolve().parents[2] / "src"
if str(_src_root) not in sys.path:
    sys.path.insert(0, str(_src_root))

from check_templates import check_templates_file_or_dir
from compile_shard import compile_shard
from cta_merge import apply_harmonize, merge_cta_parts
from engine.instantiate import allocate_template_quotas, instantiate_competency
from plan_shards import (
    DEFAULT_COMPS_PER_SHARD,
    determine_shard_count,
    partition_competencies_into_shards,
    plan_shards,
)


class TestCase2BShardPartitioning:
    """Verifies that Case 2B enforces max 2 competencies per shard across diverse curriculum sizes."""

    def test_default_comps_per_shard_is_two(self):
        """Default comps per shard constant must be 2 (non-skill)."""
        assert DEFAULT_COMPS_PER_SHARD == 2

    def test_partitioning_case_2b_various_sizes(self):
        """Under Case 2B (max_comps=2), no shard ever contains more than 2 competencies."""
        for n in [1, 2, 3, 5, 8, 16, 21, 24, 43]:
            comps = [{"id": f"C-{i:02d}", "name": f"Comp {i}", "type": "concept"} for i in range(1, n + 1)]
            k = determine_shard_count(comps, max_comps_per_shard=2)
            shards = partition_competencies_into_shards(comps, k)
            assert len(shards) == k
            for s in shards:
                assert len(s["competency_ids"]) <= 2, f"Shard {s['shard_id']} exceeded 2 competencies for N={n}"

    def test_partitioning_case_2b_default_args(self):
        """Under default invocations (no max_comps passed), no shard exceeds 3 non-skill competencies."""
        for n in [1, 2, 3, 5, 8, 16, 21, 24, 43]:
            comps = [{"id": f"C-{i:02d}", "name": f"Comp {i}", "type": "concept"} for i in range(1, n + 1)]
            k = determine_shard_count(comps)
            shards = partition_competencies_into_shards(comps, k)
            assert len(shards) == k
            for s in shards:
                assert len(s["competency_ids"]) <= 3, f"Shard {s['shard_id']} exceeded 3 competencies with default args for N={n}"

    def test_partitioning_case_2a_various_sizes(self):
        """Under Case 2A (max_comps=3), no shard ever contains more than 3 competencies."""
        for n in [1, 2, 3, 5, 8, 16, 21, 24, 43]:
            comps = [{"id": f"C-{i:02d}", "name": f"Comp {i}", "type": "concept"} for i in range(1, n + 1)]
            k = determine_shard_count(comps, max_comps_per_shard=3)
            shards = partition_competencies_into_shards(comps, k)
            assert len(shards) == k
            for s in shards:
                assert len(s["competency_ids"]) <= 3, f"Shard {s['shard_id']} exceeded 3 competencies for N={n}"

    def test_revert_to_case_2a_constant_switch(self, monkeypatch):
        """Switching DEFAULT_COMPS_PER_SHARD to 3 cleanly sets Case 2A behavior across determine_shard_count."""
        import plan_shards
        monkeypatch.setattr(plan_shards, "DEFAULT_COMPS_PER_SHARD", 3)
        # determine_shard_count with max_comps_per_shard=None falls back to adaptive clamp(ceil(N/8), 2, 3)
        assert plan_shards.determine_shard_count(24, max_comps_per_shard=None) == 8
        assert plan_shards.determine_shard_count(43, max_comps_per_shard=None) == 15
        assert plan_shards.determine_shard_count(16, max_comps_per_shard=None) == 8


class TestCase2BQuotaAllocation:
    """Verifies quota distribution across T=4 templates (Case 2B) and T=3 templates (Case 2A)."""

    def test_quota_allocation_case_2b_t4(self):
        """4 templates must sum exactly to 20 (Concept/Fact) and 30 (Skill)."""
        tpls = [{"id": f"T-C01-{i:02d}"} for i in range(1, 5)]

        # Concept/Fact (quota = 20) -> 5, 5, 5, 5
        q20 = allocate_template_quotas(tpls, 20)
        assert len(q20) == 4
        assert sum(q20.values()) == 20
        assert all(v == 5 for v in q20.values())

        # Skill (quota = 30) -> 8, 8, 7, 7
        q30 = allocate_template_quotas(tpls, 30)
        assert len(q30) == 4
        assert sum(q30.values()) == 30
        assert sorted(q30.values(), reverse=True) == [8, 8, 7, 7]

    def test_quota_allocation_case_2a_t3(self):
        """3 templates (Case 2A) must sum exactly to 20 and 30."""
        tpls = [{"id": f"T-C01-{i:02d}"} for i in range(1, 4)]

        # Concept/Fact (quota = 20) -> 7, 7, 6
        q20 = allocate_template_quotas(tpls, 20)
        assert len(q20) == 3
        assert sum(q20.values()) == 20
        assert sorted(q20.values(), reverse=True) == [7, 7, 6]

        # Skill (quota = 30) -> 10, 10, 10
        q30 = allocate_template_quotas(tpls, 30)
        assert len(q30) == 3
        assert sum(q30.values()) == 30
        assert all(v == 10 for v in q30.values())


class TestCase2BMultiTemplateCompilation:
    """End-to-end integration test compiling a shard with C=2 and T=4 archetypes (8 total tuples)."""

    def test_compile_shard_c2_t4_archetypes(self, tmp_path: Path):
        """Compiles a shard with 2 competencies, each having 4 templates covering the 4 archetypes."""
        work_dir = tmp_path / "work"
        shards_dir = work_dir / "shards"
        templates_dir = work_dir / "templates"
        shards_dir.mkdir(parents=True, exist_ok=True)
        templates_dir.mkdir(parents=True, exist_ok=True)

        # 1. cta.json with 2 competencies and 6 distractors each
        distractors_c01 = [
            {"id": f"D-C01-{i:02d}", "name": f"Distractor C01 {i}", "wrong_belief": f"Error C01 {i}", "omitted_step": "N/A"}
            for i in range(1, 7)
        ]
        distractors_c02 = [
            {"id": f"D-C02-{i:02d}", "name": f"Distractor C02 {i}", "wrong_belief": f"Error C02 {i}", "omitted_step": "N/A"}
            for i in range(1, 7)
        ]

        cta_data = {
            "course_id": "test_course_2b",
            "title": "Test Course 2B",
            "competencies": [
                {
                    "id": "C-01",
                    "type": "concept",
                    "name": "Dinámica de Capital Solow",
                    "description_latex": r"Ecuación $\dot{k} = s f(k) - (n + g + \delta)k$",
                    "distractors": distractors_c01,
                },
                {
                    "id": "C-02",
                    "type": "skill",
                    "name": "Cálculo de Capital de Estado Estacionario",
                    "description_latex": r"Resolución de $k^*$ tal que $\dot{k} = 0$",
                    "distractors": distractors_c02,
                },
            ],
        }
        (work_dir / "cta.json").write_text(json.dumps(cta_data), encoding="utf-8")

        # 2. pre_cta_manifest.json and pre_shard_manifest.json
        (work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "course_id": "test_course_2b",
            "source_files": ["solow.pdf"],
        }), encoding="utf-8")

        (shards_dir / "pre_shard_manifest.json").write_text(json.dumps({
            "total_competencies": 2,
            "total_shards": 1,
            "shards": [
                {
                    "shard_id": "shard_01",
                    "shard_index": 0,
                    "competency_ids": ["C-01", "C-02"],
                    "competencies": cta_data["competencies"],
                    "shard_data_path": str((shards_dir / "shard_01_data.py").as_posix()),
                    "templates_dir": str(templates_dir.as_posix()),
                }
            ],
        }), encoding="utf-8")

        # 3. Write shard_01_data.py containing 8 tuples (4 archetypes for C-01, 4 archetypes for C-02)
        shard_source = r'''# Shard 01 Data - Case 2B Implementation
import math

# --- Competency C-01 (Concept) Archetypes ---
# Archetype 1: Direct / Forward Computation
def gen_c01_direct(rng):
    s_idx = rng.randint(15, 45)
    s = round(s_idx / 100.0, 2)
    y = rng.randint(20, 90)
    inv = round(s * y, 2)
    d_ids = ["D-C01-01", "D-C01-02", "D-C01-03", "D-C01-04", "D-C01-05", "D-C01-06"]
    rats = [
        "Sobreestimación de propensión marginal al ahorro con tasa @s@ y producto @y@",
        "Subestimación de propensión marginal al ahorro con tasa @s@ y producto @y@",
        "Atribución de factor de escala espurio sobre el producto @y@",
        "Deducción contractiva no justificada para la inversión @inv@",
        "Confusión entre ahorro voluntario y forzoso con tasa @s@",
        "Omisión de depreciación en la inversión bruta per cápita @inv@",
    ]
    inv_offsets = [1.2, -1.2, 2.7, -2.7, 4.1, -4.1]
    distractors = [
        {"value": rf"$i = {round(inv + off, 2)}$", "distractor_id": did, "error_rationale": rat}
        for off, did, rat in zip(inv_offsets, d_ids, rats)
    ]
    return {"vars": {"s": s, "y": y, "inv": inv}, "correct": rf"$i = {inv}$", "distractors": distractors}

def ver_c01_direct(res):
    c = res.get("correct", "") if isinstance(res, dict) else str(res)
    v = res.get("vars", {}) if isinstance(res, dict) else {}
    raw = "".join(ch for ch in str(c) if ch.isdigit() or ch in ".-")
    val = float(raw) if raw else -999.0
    return abs(val - round(v["s"] * v["y"], 2)) < 1e-3

# Archetype 2: Inverse / Diagnostic
def gen_c01_inverse(rng):
    y = rng.randint(40, 100)
    s_pct = rng.randint(15, 45)
    s = round(s_pct / 100.0, 2)
    inv = round(s * y, 2)
    d_ids = ["D-C01-01", "D-C01-02", "D-C01-03", "D-C01-04", "D-C01-05", "D-C01-06"]
    rats = [
        "Desvío superior significativo en el cálculo de la tasa requerida @s@ para producto @y@",
        "Desvío inferior por aproximación truncada en tasa @s@ sobre el producto observado @y@",
        "Uso erróneo de la inversión bruta @inv@ en el numerador de la fracción de equilibrio",
        "Cociente invertido entre inversión bruta @inv@ y el producto por trabajador observado @y@",
        "Sesgo aditivo constante injustificado sobre la tasa de ahorro estacionaria @s@",
        "Sesgo sustractivo constante injustificado sobre la tasa de ahorro estacionaria @s@",
    ]
    s_offsets = [0.03, -0.03, 0.07, -0.07, 0.11, -0.11]
    distractors = [
        {"value": rf"$s = {round(s + off, 2)}$", "distractor_id": did, "error_rationale": rat}
        for off, did, rat in zip(s_offsets, d_ids, rats)
    ]
    return {"vars": {"inv": inv, "y": y, "s": s}, "correct": str(s), "distractors": distractors}


def ver_c01_inverse(res):
    c = res.get("correct", "") if isinstance(res, dict) else str(res)
    v = res.get("vars", {}) if isinstance(res, dict) else {}
    raw = "".join(ch for ch in str(c) if ch.isdigit() or ch in ".-")
    val = float(raw) if raw else -999.0
    return abs(val - v["s"]) < 1e-3

# Archetype 3: Comparative Statics / Perturbation (multiple_select)
def gen_c01_perturbation(rng):
    s1 = round(rng.uniform(0.16, 0.34), 2)
    delta_s = round(rng.uniform(0.02, 0.14), 2)
    s2 = round(s1 + delta_s, 2)
    shift_dir = "hacia arriba"
    options = [
        {"content": f"La curva de inversión bruta se desplaza {shift_dir} alcanzando una nueva tasa de ahorro s = {s2}", "is_correct": True},
        {"content": f"La variación paramétrica acumulada en la tasa de ahorro asciende exactamente a {delta_s} unidades reales", "is_correct": True},
        {"content": "La curva de inversión rota en sentido horario hacia el origen geométrico del plano cartesiano", "is_correct": False, "distractor_id": "D-C01-01", "error_rationale": "Confusión entre desplazamiento paralelo vertical y rotación de pendiente para la tasa @s1@ en el plano"},
        {"content": "La recta de reposición de capital incrementa su pendiente verticalmente sin desplazar el intercepto", "is_correct": False, "distractor_id": "D-C01-02", "error_rationale": "Atribución errónea del efecto de acumulación a la recta de reposición ante la variación @delta_s@"},
        {"content": "El nivel de producto per cápita permanece inmutable sin experimentar traslación ni rotación alguna", "is_correct": False, "distractor_id": "D-C01-04", "error_rationale": "Falsa neutralidad dinámica del parámetro de ahorro al variar desde @s1@ hasta el valor @s2@"},
    ]
    return {"vars": {"s1": s1, "s2": s2, "delta_s": delta_s}, "options": options}

def ver_c01_perturbation(res):
    opts = res.get("options", []) if isinstance(res, dict) else []
    v = res.get("vars", {}) if isinstance(res, dict) else {}
    corrects = [o for o in opts if isinstance(o, dict) and o.get("is_correct") is True]
    falses = [o for o in opts if isinstance(o, dict) and o.get("is_correct") is False]
    if len(opts) != 5 or len(corrects) != 2 or len(falses) != 3:
        return False
    has_shift = any("se desplaza" in str(o.get("content", "")) and str(v.get("s2")) in str(o.get("content", "")) for o in corrects)
    has_delta = any("variación paramétrica" in str(o.get("content", "")) and str(v.get("delta_s")) in str(o.get("content", "")) for o in corrects)
    valid_falses = all(
        o.get("distractor_id") in {"D-C01-01", "D-C01-02", "D-C01-04"}
        and bool(str(o.get("error_rationale") or "").strip())
        for o in falses
    )
    return has_shift and has_delta and valid_falses

# Archetype 4: Boundary Testing / Axiomatic Violations (fill_in_the_blank)
def gen_c01_boundary(rng):
    s_lim = round(rng.uniform(0.001, 0.050), 4)
    y_lim = rng.randint(50, 200)
    inv_lim = round(s_lim * y_lim, 4)
    cond = "mínimo"
    d_ids = ["D-C01-01", "D-C01-02", "D-C01-03", "D-C01-04", "D-C01-05", "D-C01-06"]
    rats = [
        "Sobreestimación analítica del flujo límite de inversión con tasa de ahorro @s_lim@ y producto @y_lim@",
        "Subestimación numérica sistemática del flujo límite para tasa de ahorro @s_lim@ y nivel productivo @y_lim@",
        "Error de escala porcentual aplicado incorrectamente sobre el caudal de inversión bruta @inv_lim@ en frontera",
        "Deducción espuria de depreciación física aplicada indebidamente sobre el flujo de inversión límite @inv_lim@",
        "Inversión aritmética directa errónea entre la tasa límite de ahorro @s_lim@ y el producto estacionario @y_lim@",
        "Truncamiento decimal prematuro de la cota límite convergente para el flujo resultante @inv_lim@ en frontera",
    ]
    offsets = [0.5, -0.5, 1.2, -1.2, 2.1, -2.1]
    distractors = [
        {"value": str(round(inv_lim + off, 4)), "distractor_id": did, "error_rationale": rat}
        for off, did, rat in zip(offsets, d_ids, rats)
    ]
    return {"vars": {"s_lim": s_lim, "y_lim": y_lim, "inv_lim": inv_lim, "cond": cond}, "correct": str(inv_lim), "distractors": distractors}

def ver_c01_boundary(res):
    c = res.get("correct", "") if isinstance(res, dict) else str(res)
    v = res.get("vars", {}) if isinstance(res, dict) else {}
    raw = "".join(ch for ch in str(c) if ch.isdigit() or ch in ".-")
    val = float(raw) if raw else -999.0
    return abs(val - round(v["s_lim"] * v["y_lim"], 4)) < 1e-3


# --- Competency C-02 (Skill) Archetypes ---
def gen_c02_direct(rng):
    s = round(rng.uniform(0.15, 0.45), 2)
    denom = round(rng.uniform(0.04, 0.10), 3)
    ratio = s / denom
    k_star = round(ratio ** 2, 2)
    d_ids = ["D-C02-01", "D-C02-02", "D-C02-03", "D-C02-04", "D-C02-05", "D-C02-06"]
    rats = [
        "Sobreestimación analítica por omisión del exponente cuadrático en el capital @k_star@",
        "Subestimación numérica por truncamiento de decimales intermedios para tasa @s@",
        "Inversión algebraica de los términos en el cociente de tasa de reposición @denom@",
        "Atribución errónea de factor de depreciación duplicado en el denominador @denom@",
        "Sesgo aditivo espurio en la resolución de la ecuación de equilibrio para @k_star@",
        "Sesgo sustractivo espurio en el despeje analítico estacionario con tasa de ahorro @s@",
    ]
    k_offsets = [1.8, -1.8, 3.7, -3.7, 5.6, -5.6]
    distractors = [
        {"value": rf"$k^* = {round(k_star + off, 2)}$", "distractor_id": did, "error_rationale": rat}
        for off, did, rat in zip(k_offsets, d_ids, rats)
    ]
    return {"vars": {"s": s, "denom": denom, "k_star": k_star}, "correct": str(k_star), "distractors": distractors}

def ver_c02_direct(res):
    c = res.get("correct", "") if isinstance(res, dict) else str(res)
    v = res.get("vars", {}) if isinstance(res, dict) else {}
    raw = "".join(ch for ch in str(c) if ch.isdigit() or ch in ".-")
    val = float(raw) if raw else -999.0
    return abs(val - round((v["s"] / v["denom"]) ** 2, 2)) < 1e-2

def gen_c02_inverse(rng):
    k_root = rng.randint(4, 25)
    k_star = round(float(k_root ** 2), 2)
    denom = round(rng.uniform(0.04, 0.10), 3)
    s = round(k_root * denom, 3)
    d_ids = ["D-C02-01", "D-C02-02", "D-C02-03", "D-C02-04", "D-C02-05", "D-C02-06"]
    rats = [
        "Desvío superior sistemático en el cálculo analítico de la tasa requerida @s@",
        "Desvío inferior causado por aproximación truncada de raíz sobre la tasa @s@",
        "Uso directo del nivel k en lugar de extraer la raíz cuadrada de capital @k_star@",
        "Cociente invertido entre la tasa de reposición @denom@ y la raíz de capital @k_star@",
        "Sesgo aditivo constante introducido en el despeje de la tasa de ahorro @s@",
        "Sesgo sustractivo constante introducido en el despeje de la tasa de ahorro @s@",
    ]
    s_offsets = [0.03, -0.03, 0.07, -0.07, 0.11, -0.11]
    distractors = [
        {"value": rf"$s = {round(s + off, 3)}$", "distractor_id": did, "error_rationale": rat}
        for off, did, rat in zip(s_offsets, d_ids, rats)
    ]
    return {"vars": {"k_star": k_star, "denom": denom, "s": s}, "correct": str(s), "distractors": distractors}

def ver_c02_inverse(res):
    c = res.get("correct", "") if isinstance(res, dict) else str(res)
    v = res.get("vars", {}) if isinstance(res, dict) else {}
    raw = "".join(ch for ch in str(c) if ch.isdigit() or ch in ".-")
    val = float(raw) if raw else -999.0
    return abs(val - v["s"]) < 1e-3

def gen_c02_perturbation(rng):
    n_old = round(rng.uniform(0.01, 0.03), 3)
    delta_n = round(rng.uniform(0.01, 0.05), 3)
    n_new = round(n_old + delta_n, 3)
    options = [
        {"content": rf"El capital estacionario $k^*$ disminuye tras elevarse la reposición poblacional a tasa n = {n_new}", "is_correct": True},
        {"content": rf"La pendiente de la recta de reposición efectiva aumenta exactamente en {delta_n} puntos porcentuales", "is_correct": True},
        {"content": "La tasa de ahorro exógena se ajusta automáticamente para contrarrestar la dilución poblacional inducida", "is_correct": False, "distractor_id": "D-C02-04", "error_rationale": "Atribución errónea de endogeneidad del ahorro ante nueva tasa demográfica @n_new@"},
        {"content": "La productividad marginal del capital disminuye de forma discontinua a lo largo de toda la trayectoria", "is_correct": False, "distractor_id": "D-C02-05", "error_rationale": "Violación axiomática de continuidad productiva para tasa poblacional @n_old@"},
        {"content": "El consumo por unidad de trabajo eficiente converge a una senda de crecimiento no balanceado y volátil", "is_correct": False, "distractor_id": "D-C02-06", "error_rationale": "Confusión de régimen transitorio con senda balanceada de largo plazo para @delta_n@"},
    ]
    return {"vars": {"n_old": n_old, "n_new": n_new, "delta_n": delta_n}, "options": options}

def ver_c02_perturbation(res):
    opts = res.get("options", []) if isinstance(res, dict) else []
    v = res.get("vars", {}) if isinstance(res, dict) else {}
    corrects = [o for o in opts if isinstance(o, dict) and o.get("is_correct") is True]
    falses = [o for o in opts if isinstance(o, dict) and o.get("is_correct") is False]
    if len(opts) != 5 or len(corrects) != 2 or len(falses) != 3:
        return False
    has_k = any("disminuye tras elevarse" in str(o.get("content", "")) and str(v.get("n_new")) in str(o.get("content", "")) for o in corrects)
    has_slope = any("pendiente de la recta" in str(o.get("content", "")) and str(v.get("delta_n")) in str(o.get("content", "")) for o in corrects)
    valid_falses = all(
        o.get("distractor_id") in {"D-C02-04", "D-C02-05", "D-C02-06"}
        and bool(str(o.get("error_rationale") or "").strip())
        for o in falses
    )
    return has_k and has_slope and valid_falses

def gen_c02_boundary(rng):
    sample_rate = round(rng.uniform(0.001, 0.050), 4)
    correct_str = rf"Bajo {sample_rate}, k* tiende a infinito al anularse la reposición"
    distractors = [
        {"value": "La economía deja de producir bienes al alcanzarse la frontera analítica del espacio de estados posibles", "distractor_id": "D-C02-02", "error_rationale": "Confusión entre dinámica de acumulación de capital y nivel de producto con @sample_rate@"},
        {"value": "El estado estacionario resultante genera fluctuaciones y oscilaciones cíclicas explosivas no lineales", "distractor_id": "D-C02-04", "error_rationale": "Atribución errónea de inestabilidad oscilatoria no lineal ante valor límite @sample_rate@"},
        {"value": "El stock de capital por trabajador efectivo se desploma súbitamente a cero en toda la trayectoria temporal", "distractor_id": "D-C02-01", "error_rationale": "Inversión errónea del comportamiento en la cota de reposición límite para @sample_rate@"},
        {"value": "La función de ahorro converge a una cota fija", "distractor_id": "D-C02-03", "error_rationale": "Confusión analítica de singularidad asintótica del equilibrio con tasa @sample_rate@"},
        {"value": "El producto per cápita alcanza un valor simétrico interior", "distractor_id": "D-C02-05", "error_rationale": "Atribución de óptimo interior acotado en lugar de divergencia asintótica real"},
        {"value": "La velocidad transitoria se anula", "distractor_id": "D-C02-06", "error_rationale": "Confusión entre cota asintótica de nivel estacionario y velocidad de transición"},
    ]
    return {"vars": {"sample_rate": sample_rate}, "correct": correct_str, "distractors": distractors}

def ver_c02_boundary(res):
    c = str(res.get("correct", "")) if isinstance(res, dict) else str(res)
    v = res.get("vars", {}) if isinstance(res, dict) else {}
    return "tiende a infinito al anularse la reposición" in c and str(v.get("sample_rate")) in c

stems_c01_1 = [
    r"Considere una tasa de ahorro $s = {s}$ y un producto $y = {y}$. Calcule la inversión bruta per cápita:",
    r"Determine la inversión bruta per cápita asociada a una tasa de ahorro $s = {s}$ y un producto $y = {y}$:",
    r"Evalúe el flujo de inversión bruta por trabajador dados $s = {s}$ e ingreso $y = {y}$:",
    r"Halle el nivel de inversión bruta si el ahorro es $s = {s}$ y la producción es $y = {y}$:",
    r"Calcule el monto invertido por empleado con tasa $s = {s}$ y producto $y = {y}$:",
    r"Obtenga la inversión correspondiente a una propensión $s = {s}$ y valor $y = {y}$:",
    r"Determine la acumulación bruta a partir de ahorro $s = {s}$ e ingreso $y = {y}$:",
]
stems_c01_2 = [
    r"Si la inversión es $i = {inv}$ y el producto es $y = {y}$, determine la tasa de ahorro implícita $s$:",
    r"A partir de una inversión $i = {inv}$ y un nivel de producto $y = {y}$, halle la tasa $s$ requerida:",
    r"Calcule la propensión marginal al ahorro $s$ cuando la inversión per cápita es $i = {inv}$ y el producto es $y = {y}$:",
    r"Despeje la fracción de ahorro $s$ dados el flujo $i = {inv}$ y el nivel $y = {y}$:",
    r"Determine la tasa $s$ coherente con una inversión $i = {inv}$ e ingreso $y = {y}$:",
    r"Halle la tasa media de ahorro $s$ asociada a $i = {inv}$ y producto $y = {y}$:",
    r"Calcule la relación de ahorro $s$ sabiendo que $i = {inv}$ y el ingreso es $y = {y}$:",
]
stems_c01_3 = [
    r"Seleccione todas las afirmaciones verdaderas sobre el impacto de un aumento en la tasa de ahorro de $s_1 = {s1}$ a $s_2 = {s2}$ en la curva de inversión:",
    r"Marque todas las proposiciones correctas acerca de la traslación de la función de inversión ante una variación de $s_1 = {s1}$ a $s_2 = {s2}$:",
    r"Indique todas las respuestas válidas sobre la respuesta gráfica del flujo de inversión cuando el ahorro cambia de $s_1 = {s1}$ a $s_2 = {s2}$:",
    r"Elija todas las consecuencias ciertas del desplazamiento de la curva de inversión si el ahorro pasa de $s_1 = {s1}$ a $s_2 = {s2}$:",
    r"Señale todas las afirmaciones correctas sobre el cambio geométrico en la inversión bruta tras subir la tasa de $s_1 = {s1}$ a $s_2 = {s2}$:",
    r"Identifique todas las propiedades válidas de la traslación vertical de la función de inversión ante el salto de $s_1 = {s1}$ a $s_2 = {s2}$:",
    r"Verifique cuáles conclusiones sobre la nueva posición de la curva de ahorro tras variar de $s_1 = {s1}$ a $s_2 = {s2}$ son verdaderas:",
]
stems_c01_4 = [
    r"Examine el caso límite de régimen de ahorro {cond} con $s = {s_lim}$ y producto $y = {y_lim}$. Calcule la inversión bruta límite $i$:",
    r"En el escenario extremo {cond} fijando $s = {s_lim}$ e ingreso $y = {y_lim}$, halle el flujo límite de inversión $i$:",
    r"Determine la inversión bruta $i$ en la frontera {cond} bajo $s = {s_lim}$ y nivel de producción $y = {y_lim}$:",
    r"Calcule el flujo de inversión de frontera $i$ en la cota {cond} con parámetro $s = {s_lim}$ y producto $y = {y_lim}$:",
    r"Evalúe la inversión bruta límite $i$ del modelo en el régimen {cond} con tasa $s = {s_lim}$ e ingreso $y = {y_lim}$:",
    r"Obtenga la inversión límite $i$ para la condición {cond} al fijar $s = {s_lim}$ y producción $y = {y_lim}$:",
    r"Halle el monto numérico de inversión bruta $i$ en el entorno límite {cond} con $s = {s_lim}$ y $y = {y_lim}$:",
]

stems_c02_1 = [
    r"Bajo una tasa de ahorro $s = {s}$ y depreciación combinada $(n + g + \delta) = {denom}$, halle $k^*$:",
    r"Calcule el capital de estado estacionario $k^*$ dado el parámetro $s = {s}$ y el factor $(n + g + \delta) = {denom}$:",
    r"Determine el nivel estacionario $k^*$ resolviendo el balance con $s = {s}$ y tasa de reposición ${denom}$:",
    r"Halle el valor de equilibrio $k^*$ dados el ahorro $s = {s}$ y la reposición total ${denom}$:",
    r"Calcule el stock por trabajador $k^*$ que equilibra inversión $s = {s}$ con tasa ${denom}$:",
    r"Obtenga la dotación $k^*$ de largo plazo cuando $s = {s}$ y la suma de tasas es ${denom}$:",
    r"Resuelva para el capital estacionario $k^*$ asumiendo propensión $s = {s}$ y factor ${denom}$:",
]
stems_c02_2 = [
    r"Si se desea sostener un capital de estado estacionario $k^* = {k_star}$ con $(n+g+\delta) = {denom}$, determine la tasa de ahorro $s$:",
    r"Halle la tasa de ahorro requerida $s$ para alcanzar el nivel de capital $k^* = {k_star}$ con factor $(n+g+\delta) = {denom}$:",
    r"Calcule el valor de la propensión al ahorro $s$ necesario para preservar el equilibrio $k^* = {k_star}$ con tasa ${denom}$:",
    r"Determine la tasa $s$ que hace sostenible un capital $k^* = {k_star}$ con depreciación ${denom}$:",
    r"Despeje el ahorro $s$ imprescindible para mantener $k^* = {k_star}$ frente a la reposición ${denom}$:",
    r"Obtenga la tasa de inversión $s$ que balancea el nivel $k^* = {k_star}$ con la suma ${denom}$:",
    r"Calcule la propensión requerida $s$ para fijar el equilibrio en $k^* = {k_star}$ con factor ${denom}$:",
]
stems_c02_3 = [
    r"Seleccione todas las afirmaciones verdaderas sobre un incremento poblacional de $n = {n_old}$ a $n = {n_new}$ y su efecto en $k^*$:",
    r"Marque todas las proposiciones correctas acerca del capital de equilibrio $k^*$ ante un shock demográfico de $n = {n_old}$ a $n = {n_new}$:",
    r"Indique todas las respuestas válidas sobre la sensibilidad del estado estacionario $k^*$ cuando la tasa demográfica varía de $n = {n_old}$ a $n = {n_new}$:",
    r"Elija todas las conclusiones correctas sobre el cambio en $k^*$ si el crecimiento laboral pasa de $n = {n_old}$ a $n = {n_new}$:",
    r"Señale todas las proposiciones ciertas sobre la contracción de $k^*$ causada por una expansión poblacional de $n = {n_old}$ a $n = {n_new}$:",
    r"Identifique todas las consecuencias verdaderas sobre la dotación de equilibrio $k^*$ al subir la tasa de $n = {n_old}$ a $n = {n_new}$:",
    r"Verifique cuáles efectos sobre $k^*$ provocados por el incremento en $n$ desde {n_old} hasta {n_new} son correctos:",
]
stems_c02_4 = [
    r"Considere el caso límite donde la tasa combinada toma el valor ${sample_rate}$. Analice la trayectoria asintótica de $k^*$:",
    r"Examine el comportamiento de frontera con tasa combinada de reposición ${sample_rate}$ para el capital $k^*$:",
    r"Determine la trayectoria asintótica del capital $k^*$ evaluando la tasa combinada ${sample_rate}$:",
    r"Evalúe la divergencia de $k^*$ cuando la depreciación combinada se aproxima a ${sample_rate}$:",
    r"Halle el límite del stock de capital $k^*$ si la reposición total desciende a ${sample_rate}$:",
    r"Identifique el curso asintótico de $k^*$ ante una tasa casi nula de ${sample_rate}$:",
    r"Compruebe el crecimiento sin cota de $k^*$ en la frontera analítica con ${sample_rate}$:",
]

hints_c01_1 = [
    "Identifique la tasa de ahorro y el producto per cápita.",
    "Aplique la relación fundamental de inversión bruta directa.",
    "Verifique la escala del valor numérico obtenido.",
]
hints_c01_2 = [
    "Despeje la tasa de ahorro como cociente entre inversión y producto.",
    "Sustituya los valores de flujo de inversión e ingreso per cápita.",
    "Compruebe que la propensión resultante permanezca entre cero y uno.",
]
hints_c01_3 = [
    "Analice cómo cambia la pendiente de la recta de inversión bruta.",
    "Compare las posiciones de la curva antes y después del salto en s.",
    "Verifique si el desplazamiento es vertical hacia arriba o rotación.",
]
hints_c01_4 = [
    "Evalúe el comportamiento límite cuando la tasa de ahorro tiende a cero.",
    "Observe hacia qué cota converge el flujo de inversión bruta.",
    "Contraste la frontera de ahorro mínimo con el estado estacionario interior.",
]
hints_c02_1 = [
    "Iguale la inversión bruta a la depreciación de reposición.",
    "Divida ambos lados por la función de producción per cápita.",
    "Eleve al exponente adecuado para despejar el capital estacionario.",
]
hints_c02_2 = [
    "Calcule primero la raíz cuadrada del capital de estado estacionario.",
    "Multiplique dicho término por la tasa combinada de reposición.",
    "Valide que la tasa de ahorro despejada sea consistente con el equilibrio.",
]
hints_c02_3 = [
    "Identifique cómo afecta el crecimiento poblacional a la recta de reposición.",
    "Determine el desplazamiento del punto de intersección en el equilibrio.",
    "Concluya si el capital por trabajador efectivo aumenta o disminuye.",
]
hints_c02_4 = [
    "Examine el denominador de la fracción de capital estacionario en el límite.",
    "Evalúe qué sucede cuando la tasa de reposición combinada se aproxima a cero.",
    "Determine el comportamiento asintótico del nivel de capital de largo plazo.",
]

TEMPLATES = [
    # Competency C-01: 4 Archetypes (max 1 MC7, 75% active)
    ("T-C-01-01", "C-01", "multiple_choice", gen_c01_direct, ver_c01_direct, ("easy", "Remember"), stems_c01_1, hints_c01_1, r"La inversión bruta per cápita directa es $i = s y = ({s})({y}) = {inv}$."),
    ("T-C-01-02", "C-01", "fill_in_the_blank", gen_c01_inverse, ver_c01_inverse, ("medium", "Understand"), stems_c01_2, hints_c01_2, r"Despejando la propensión media, obtenemos $s = i / y = {inv} / {y} = {s}$."),
    ("T-C-01-03", "C-01", "multiple_select", gen_c01_perturbation, ver_c01_perturbation, ("hard", "Apply"), stems_c01_3, hints_c01_3, r"Un incremento en $s$ desplaza la curva de inversión verticalmente hacia arriba."),
    ("T-C-01-04", "C-01", "fill_in_the_blank", gen_c01_boundary, ver_c01_boundary, ("hard", "Analyze"), stems_c01_4, hints_c01_4, r"En el caso límite {cond}, la inversión bruta resultante es $i = ({s_lim})({y_lim}) = {inv_lim}$."),

    # Competency C-02: 4 Archetypes (Skill Bloom Apply..Evaluate, max 1 MC7, 75% active)
    ("T-C-02-01", "C-02", "fill_in_the_blank", gen_c02_direct, ver_c02_direct, ("easy", "Apply"), stems_c02_1, hints_c02_1, r"En estado estacionario, $s \sqrt{k} = ({denom})k \implies k^* = (s/{denom})^2 = {k_star}$."),
    ("T-C-02-02", "C-02", "fill_in_the_blank", gen_c02_inverse, ver_c02_inverse, ("medium", "Apply"), stems_c02_2, hints_c02_2, r"Despejando la tasa de equilibrio, $s = \sqrt{k^*} ({denom}) = {s}$."),
    ("T-C-02-03", "C-02", "multiple_select", gen_c02_perturbation, ver_c02_perturbation, ("hard", "Analyze"), stems_c02_3, hints_c02_3, r"Un aumento en $n$ incrementa la pendiente de la recta de reposición reduciendo $k^*$."),
    ("T-C-02-04", "C-02", "fill_in_the_blank", gen_c02_boundary, ver_c02_boundary, ("hard", "Evaluate"), stems_c02_4, hints_c02_4, r"Al anularse el denominador de la relación de equilibrio, $k^*$ diverge hacia infinito."),
]
'''
        (shards_dir / "shard_01_data.py").write_text(shard_source, encoding="utf-8")

        # 4. Run compile_shard
        success, errors = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_01",
            strict=True,
            seeds=50,
        )
        assert success, f"compile_shard failed with errors: {errors}"

        # 5. Verify output files
        c01_json = templates_dir / "C-01.json"
        c02_json = templates_dir / "C-02.json"
        assert c01_json.is_file(), "Missing C-01.json"
        assert c02_json.is_file(), "Missing C-02.json"

        # Check multi-template container structure and unique IDs
        c01_data = json.loads(c01_json.read_text(encoding="utf-8"))
        assert "templates" in c01_data
        assert len(c01_data["templates"]) == 4, f"Expected 4 templates for C-01, got {len(c01_data['templates'])}"
        c01_tids = [t["id"] for t in c01_data["templates"]]
        assert len(set(c01_tids)) == 4, f"Expected 4 unique template IDs, got {c01_tids}"
        assert all(tid.startswith("T-C-01") for tid in c01_tids)

        c02_data = json.loads(c02_json.read_text(encoding="utf-8"))
        assert "templates" in c02_data
        assert len(c02_data["templates"]) == 4, f"Expected 4 templates for C-02, got {len(c02_data['templates'])}"
        c02_tids = [t["id"] for t in c02_data["templates"]]
        assert len(set(c02_tids)) == 4, f"Expected 4 unique template IDs, got {c02_tids}"
        assert all(tid.startswith("T-C-02") for tid in c02_tids)


class TestCase2BTribandMultimodalAndHarmonization:
    """End-to-end integration tests for Tri-Banda Multimodal coverage and CTA Harmonization."""

    def test_triband_multimodal_coverage_and_fib_non_dollar(self, tmp_path: Path):
        """Verifies Tri-Banda coverage (easy/medium/hard), >=2 Bloom, FIB without external $, and MS distractor IDs."""
        work_dir = tmp_path / "work_triband"
        shards_dir = work_dir / "shards"
        templates_dir = work_dir / "templates"
        shards_dir.mkdir(parents=True, exist_ok=True)
        templates_dir.mkdir(parents=True, exist_ok=True)

        cta_data = {
            "course_id": "course_triband",
            "title": "Curso Tri-Banda Multimodal",
            "competencies": [
                {
                    "id": "C-01",
                    "type": "concept",
                    "name": "Concepto Fundamental de Balances",
                    "description_latex": r"Ecuación $y = f(k)$",
                    "distractors": [
                        {
                            "id": f"D-C01-0{i}",
                            "name": f"Distractor {i}",
                            "wrong_belief": f"Error {i}",
                            "remediation_hint": f"Pista {i}",
                        }
                        for i in range(1, 7)
                    ],
                }
            ],
        }
        (work_dir / "cta.json").write_text(json.dumps(cta_data), encoding="utf-8")
        (shards_dir / "pre_shard_manifest.json").write_text(json.dumps({
            "shards": [
                {
                    "shard_id": "shard_01",
                    "competency_ids": ["C-01"],
                    "competencies": cta_data["competencies"],
                }
            ]
        }), encoding="utf-8")

        shard_code = r'''
def gen_mc(rng):
    k = rng.randint(10, 50)
    ans = f"${k * 2}$"
    d_offsets = [3, -5, 7, -9, 11, -13]
    d_ids = ["D-C01-01", "D-C01-02", "D-C01-03", "D-C01-04", "D-C01-05", "D-C01-06"]
    rats = [
        "Suma espuria sistemática de tres unidades adicionales sobre el parámetro @k@",
        "Sustracción arbitraria de cinco unidades con respecto al balance para @k@",
        "Adición injustificada de siete unidades en la estimación analítica de @k@",
        "Sustracción errónea de nueve unidades en la resolución analítica con @k@",
        "Desvío positivo de once unidades sobre el producto calculado de @k@",
        "Desvío sustractivo de trece unidades en el cálculo estacionario para @k@",
    ]
    distractors = [
        {"value": f"${k * 2 + off}$", "distractor_id": did, "error_rationale": rat}
        for off, did, rat in zip(d_offsets, d_ids, rats)
    ]
    return {"vars": {"k": k}, "correct": ans, "distractors": distractors}

def ver_mc(res):
    c = res.get("correct", "") if isinstance(res, dict) else str(res)
    v = res.get("vars", {}) if isinstance(res, dict) else {}
    raw = "".join(ch for ch in str(c) if ch.isdigit() or ch in ".-")
    val = int(raw) if raw else -999
    return val == v.get("k", -1) * 2

def gen_fib(rng):
    k = rng.randint(10, 50)
    # FIB answer must be a clean numeric string without wrapping dollar signs
    ans_num = str(k * 3)
    d_offsets = [4, -4, 8, -8, 14, -14]
    d_ids = ["D-C01-01", "D-C01-02", "D-C01-03", "D-C01-04", "D-C01-05", "D-C01-06"]
    rats = [
        "Desvío positivo de cuatro unidades en la tasa analítica evaluada con @k@",
        "Sustracción errónea de cuatro unidades sobre el cálculo directo de @k@",
        "Desvío aditivo de ocho unidades injustificado para el nivel estacionario @k@",
        "Sustracción de ocho unidades en el despeje algebraico directo para @k@",
        "Desvío de catorce unidades acumulado sobre la función analítica con @k@",
        "Sustracción de catorce unidades en el balance paramétrico resuelto con @k@",
    ]
    distractors = [
        {"value": str(k * 3 + off), "distractor_id": did, "error_rationale": rat}
        for off, did, rat in zip(d_offsets, d_ids, rats)
    ]
    return {"vars": {"k": k}, "correct": ans_num, "distractors": distractors}

def ver_fib(res):
    v = res.get("vars", {}).get("k")
    return v is not None and str(res.get("correct")) == str(v * 3)

def gen_ms(rng):
    k = rng.randint(10, 50)
    # Multiple select options with explicit correctness and declared distractor_ids
    options = [
        {"content": f"El valor límite supera {k}", "is_correct": True, "distractor_id": None, "error_rationale": None},
        {"content": f"El valor límite es menor a {k - 5}", "is_correct": False, "distractor_id": "D-C01-01", "error_rationale": "Subestimación sistemática del umbral crítico respecto al parámetro @k@"},
        {"content": f"La relación se anula para {k}", "is_correct": False, "distractor_id": "D-C01-02", "error_rationale": "Atribución espuria de anulación analítica en el dominio para parámetro @k@"},
        {"content": f"La tasa diverge sin cota para {k}", "is_correct": False, "distractor_id": "D-C01-03", "error_rationale": "Falsa divergencia asintótica sin cota en régimen estable con parámetro @k@"},
    ]
    return {"vars": {"k": k}, "options": options, "correct": "A"}

def ver_ms(res):
    opts = res.get("options", [])
    valid_dids = {"D-C01-01", "D-C01-02", "D-C01-03"}
    t = [o for o in opts if o.get("is_correct") is True]
    f = [o for o in opts if o.get("is_correct") is False]
    return (
        len(opts) == 4
        and len(t) == 1
        and len(f) == 3
        and "supera" in (t[0].get("content") or t[0].get("value") or "")
        and all(o.get("distractor_id") in valid_dids and len(o.get("error_rationale") or "") >= 20 for o in f)
    )

stems_mc = [
    r"Considere el parámetro {k}. Calcule el balance directo:",
    r"A partir de la tasa {k}, halle la magnitud resultante:",
    r"Determine el balance correspondiente al valor {k}:",
    r"Calcule el valor del balance para el parámetro {k}:",
    r"Halle la magnitud calculada con el nivel {k}:",
    r"Obtenga el resultado numérico para la variable {k}:",
    r"Evalúe la función analítica con el dato {k}:",
    r"Determine la solución directa para el factor {k}:",
    r"Calcule el importe final considerando {k}:",
    r"Estime el balance exacto con la tasa {k}:",
]
stems_fib = [
    r"Dado el nivel de capital $k = {k}$, calcule el producto implícito:",
    r"Para una economía con parámetro $k = {k}$, complete el valor analítico:",
    r"Evalúe la función estructural fijando $k = {k}$ e indique el resultado:",
    r"Determine la producción per cápita con capital $k = {k}$:",
    r"Halle el nivel de producto asociado al parámetro $k = {k}$:",
    r"Calcule el valor numérico del producto si $k = {k}$:",
    r"Indique el valor entero o decimal con capital $k = {k}$:",
    r"Complete la cifra resultante para el capital $k = {k}$:",
    r"Obtenga el producto resultante fijando la dotación $k = {k}$:",
    r"Escriba la magnitud analítica calculada para $k = {k}$:",
]
stems_ms = [
    r"Considere el sistema con parámetro $k = {k}$. Seleccione todas las afirmaciones válidas:",
    r"Para el marco paramétrico con nivel $k = {k}$, determine las opciones correctas:",
    r"Evalúe las propiedades analíticas del sistema con $k = {k}$ y elija las verdaderas:",
    r"Identifique las proposiciones correctas para el modelo con $k = {k}$:",
    r"Señale las alternativas verdaderas relativas al parámetro $k = {k}$:",
    r"Marque todas las opciones acertadas para el nivel $k = {k}$:",
    r"Seleccione los enunciados verdaderos bajo el valor $k = {k}$:",
    r"Determine las afirmaciones ciertas en el contexto de $k = {k}$:",
    r"Escoja las afirmaciones consistentes con la tasa $k = {k}$:",
    r"Indique cuáles de las siguientes proposiciones con $k = {k}$ son válidas:",
]

hints_mc = [
    "Identifique las variables relevantes del enunciado de opción múltiple.",
    "Aplique la relación analítica multiplicativa por dos sobre el parámetro.",
    "Verifique la coherencia y magnitud del cálculo entero obtenido.",
]
hints_fib = [
    "Extraiga el parámetro entero de capital desde la consigna del modelo.",
    "Multiplique dicho parámetro por el coeficiente tres en respuesta abierta.",
    "Compruebe que el formato numérico final carezca de signos de moneda.",
]
hints_ms = [
    "Evalúe el umbral mínimo estricto establecido por el parámetro del modelo.",
    "Contraste cada afirmación alternativa frente a la desigualdad fundamental.",
    "Seleccione únicamente el enunciado consistente con la cota superior analítica.",
]

TEMPLATES = [
    ("T-C-01-01", "C-01", "multiple_choice", gen_mc, ver_mc, ("easy", "Remember"), stems_mc, hints_mc, "Solución formal directa multiplicando el parámetro por dos para obtener la respuesta."),
    ("T-C-01-02", "C-01", "fill_in_the_blank", gen_fib, ver_fib, ("medium", "Apply"), stems_fib, hints_fib, "Solución FIB numérica multiplicando el nivel de capital por tres sin delimitadores."),
    ("T-C-01-03", "C-01", "multiple_select", gen_ms, ver_ms, ("hard", "Analyze"), stems_ms, hints_ms, "Solución MS analítica verificando la desigualdad estricta por encima del umbral."),
]
'''
        (shards_dir / "shard_01_data.py").write_text(shard_code, encoding="utf-8")

        success, errors = compile_shard(work_dir, "shard_01", strict=True, seeds=50, min_archetypes=1)
        assert success, f"Shard compilation failed: {errors}"

        c01_path = templates_dir / "C-01.json"
        assert c01_path.is_file()
        c01_data = json.loads(c01_path.read_text(encoding="utf-8"))

        templates = c01_data["templates"]
        assert len(templates) == 3

        # 1. Tri-Banda difficulties: easy, medium, hard
        diffs = {t["difficulty"] for t in templates}
        assert diffs == {"easy", "medium", "hard"}, f"Expected tri-band difficulties, got {diffs}"

        # 2. Bloom diversity >= 2
        blooms = {t["bloom"] for t in templates}
        assert len(blooms) >= 2, f"Expected >= 2 Bloom levels, got {blooms}"
        assert blooms == {"Remember", "Apply", "Analyze"}

        # 3. Multimodal interaction types
        itypes = {t["interaction_type"] for t in templates}
        assert itypes == {"multiple_choice_7_options", "fill_in_the_blank", "multiple_select"}

        # 4. FIB validation: answer must NOT be wrapped in external dollar signs
        fib_tpl = next(t for t in templates if t["interaction_type"] == "fill_in_the_blank")
        from engine.sandbox import execute_sandbox_batch
        fib_batch = execute_sandbox_batch(fib_tpl["generate_py"], [101, 102, 103])
        for item in fib_batch:
            assert item["success"]
            c_val = str(item["result"]["correct"]).strip()
            assert not (c_val.startswith("$") and c_val.endswith("$")), (
                f"FIB answer key must NOT be wrapped in external dollar signs: '{c_val}'"
            )

        # 5. MS validation: options must have distractor_ids and error_rationale
        ms_tpl = next(t for t in templates if t["interaction_type"] == "multiple_select")
        assert ms_tpl["distractor_ids"] == ["D-C01-01", "D-C01-02", "D-C01-03"]
        ms_batch = execute_sandbox_batch(ms_tpl["generate_py"], [101, 102])
        for item in ms_batch:
            assert item["success"]
            for opt in item["result"]["options"]:
                if not opt["is_correct"]:
                    assert opt.get("distractor_id") in ms_tpl["distractor_ids"]
                    rat = opt.get("error_rationale")
                    assert rat and len(rat) >= 20

    def test_cta_mapreduce_full_flow_merge_to_harmonize(self, tmp_path: Path):
        """Verifies complete Map-Reduce flow: merge_cta_parts -> cta_draft.json -> apply_harmonize -> cta.json."""
        work_dir = tmp_path / "work_cta_flow"
        work_dir.mkdir(parents=True, exist_ok=True)
        parts_dir = work_dir / "cta_parts"
        parts_dir.mkdir(parents=True, exist_ok=True)

        # Pre-CTA manifest
        manifest = {
            "course_id": "solow_growth_mapreduce",
            "title": "Crecimiento Económico Avanzado",
            "files": [
                {"doc": "solow_part1.pdf", "file_index": 0, "total_pages": 50, "valid_page_range": [1, 50]},
                {"doc": "solow_part2.pdf", "file_index": 1, "total_pages": 50, "valid_page_range": [1, 50]},
            ],
            "subparts": [
                {"subpart_id": "part_01", "subpart_index": 0, "file_index": 0},
                {"subpart_id": "part_02", "subpart_index": 1, "file_index": 1},
            ],
        }
        (work_dir / "pre_cta_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

        # Two sectional CTA parts
        part_01 = [
            {
                "id": "C-01",
                "name": "Ecuación de Dinámica de Capital",
                "type": "concept",
                "bloom": "Understand",
                "session": "Sesión 1",
                "unit_index": 1,
                "description_latex": r"Dinámica $\dot{k} = s f(k) - (n + g + \delta)k$",
                "prerequisites": [],
                "evidence": [{"doc": "solow_part1.pdf", "page": 10}],
                "distractors": [
                    {
                        "id": f"D-C01-0{i}",
                        "name": f"Error de Dinámica {i}",
                        "wrong_belief": f"Belief erróneo {i}",
                        "correct_belief": f"Belief correcto {i}",
                        "trigger": f"Condición de balance {i}",
                        "manifestation": f"Manifestación analítica {i}",
                        "error_type": "sign_error",
                        "severity": "medium",
                        "origin": "inferred",
                        "evidence": {"doc": "solow_part1.pdf", "page": 10},
                        "remediation_hint": f"Revise minuciosamente la definicion formal y los pasos de derivacion algebraica {i} del modelo.",
                    }
                    for i in range(1, 7)
                ],
            }
        ]
        part_02 = [
            {
                "id": "C-01",  # Local duplicate ID across parts, to be sequentially renumbered to Hab-01
                "name": "Cálculo de Capital Estacionario",
                "type": "skill",
                "bloom": "Apply",
                "session": "Sesión 2",
                "unit_index": 2,
                "description_latex": r"Resolución de $k^*$ tal que $\dot{k} = 0$",
                "prerequisites": [],
                "evidence": [{"doc": "solow_part2.pdf", "page": 25}],
                "distractors": [
                    {
                        "id": f"D-C02-0{i}",
                        "name": f"Error de Cálculo {i}",
                        "wrong_belief": f"Belief cálculo erróneo {i}",
                        "correct_belief": f"Belief cálculo correcto {i}",
                        "trigger": f"Despeje analítico {i}",
                        "manifestation": f"Manifestación cálculo {i}",
                        "error_type": "skipped_step" if i <= 2 else "boundary_case",
                        "severity": "high",
                        "origin": "inferred",
                        "evidence": {"doc": "solow_part2.pdf", "page": 25},
                        "remediation_hint": f"Revise minuciosamente la definicion formal y los pasos de derivacion algebraica {i} del modelo.",
                        "omitted_step": f"Paso omitido {i}" if i <= 2 else None,
                    }
                    for i in range(1, 7)
                ],
            }
        ]
        (parts_dir / "part_01.json").write_text(json.dumps(part_01), encoding="utf-8")
        (parts_dir / "part_02.json").write_text(json.dumps(part_02), encoding="utf-8")

        # Step 1: Execute merge_cta_parts
        res_merge = merge_cta_parts(work_dir)
        assert res_merge["status"] == "success"
        assert res_merge["total_competencies"] == 2

        # Verify Stage 1 artifacts
        draft_file = work_dir / "cta_draft.json"
        order_file = work_dir / "cta_order.json"
        candidates_file = work_dir / "duplicate_candidates.json"
        outline_file = work_dir / "cta_outline.json"
        assert draft_file.is_file(), "Missing cta_draft.json"
        assert order_file.is_file(), "Missing cta_order.json"
        assert candidates_file.is_file(), "Missing duplicate_candidates.json"
        assert outline_file.is_file(), "Missing cta_outline.json"

        # Verify draft IDs are cleanly renumbered
        draft_data = json.loads(draft_file.read_text(encoding="utf-8"))
        draft_cids = [c["id"] for c in draft_data["competencies"]]
        assert draft_cids == ["C-01", "Hab-01"]

        # Step 2: Write cta_harmonize.json with valid Harmonizer directives
        harmonize_payload = {
            "rename": [
                {"competency": "C-01", "name": "Dinámica Fundamental del Capital de Solow"}
            ],
            "add_prerequisites": [
                {"competency": "Hab-01", "prerequisites": ["C-01"]}
            ],
            "drop_duplicate_distractors": [],
            "merge": [],
        }
        (work_dir / "cta_harmonize.json").write_text(json.dumps(harmonize_payload), encoding="utf-8")

        # Step 3: Execute apply_harmonize
        apply_harmonize(work_dir)

        # Verify Stage 2 final artifacts
        cta_file = work_dir / "cta.json"
        cta_md = work_dir / "cta.md"
        report_file = work_dir / "merge_report.json"
        assert cta_file.is_file(), "Missing final cta.json"
        assert cta_md.is_file(), "Missing final cta.md"
        assert report_file.is_file(), "Missing merge_report.json"

        # Verify applied changes in cta.json
        cta_final = json.loads(cta_file.read_text(encoding="utf-8"))
        comps_final = cta_final["competencies"]
        assert len(comps_final) == 2
        assert comps_final[0]["id"] == "C-01"
        assert comps_final[0]["name"] == "Dinámica Fundamental del Capital de Solow"
        assert comps_final[1]["id"] == "Hab-01"
        assert comps_final[1]["prerequisites"] == ["C-01"]

