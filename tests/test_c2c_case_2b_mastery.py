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
_skill_root = Path(__file__).resolve().parents[1] / ".agents" / "skills" / "content-to-course"
if str(_skill_root) not in sys.path:
    sys.path.insert(0, str(_skill_root))

_src_root = Path(__file__).resolve().parents[1] / "src"
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
        """Default comps per shard constant must be 2 for Case 2B."""
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
        """Under Case 2B default invocations (no max_comps passed), no shard exceeds 2 competencies."""
        for n in [1, 2, 3, 5, 8, 16, 21, 24, 43]:
            comps = [{"id": f"C-{i:02d}", "name": f"Comp {i}", "type": "concept"} for i in range(1, n + 1)]
            k = determine_shard_count(comps)
            shards = partition_competencies_into_shards(comps, k)
            assert len(shards) == k
            for s in shards:
                assert len(s["competency_ids"]) <= 2, f"Shard {s['shard_id']} exceeded 2 competencies with default args for N={n}"

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
        "Desvío superior en el cálculo de la tasa requerida @s@ para producto @y@",
        "Desvío inferior por aproximación truncada en tasa @s@ y producto @y@",
        "Uso erróneo de la inversión bruta @inv@ en el numerador",
        "Cociente invertido entre inversión @inv@ y producto @y@",
        "Sesgo aditivo constante en la tasa de ahorro @s@",
        "Sesgo sustractivo constante en la tasa de ahorro @s@",
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

# Archetype 3: Comparative Statics / Perturbation
def gen_c01_perturbation(rng):
    s1 = round(rng.uniform(0.16, 0.34), 2)
    delta_s = round(rng.uniform(0.02, 0.14), 2)
    s2 = round(s1 + delta_s, 2)
    shift_dir = "hacia arriba"
    distractors = [
        {"value": "La curva de inversión rota en sentido horario hacia el origen geométrico del plano cartesiano", "distractor_id": "D-C01-01", "error_rationale": "Confusión entre desplazamiento y rotación para tasa @s1@"},
        {"value": "La recta de reposición de capital incrementa su pendiente verticalmente sin desplazar el intercepto", "distractor_id": "D-C01-02", "error_rationale": "Atribución errónea del efecto a la reposición con @delta_s@"},
        {"value": "El nivel de producto per cápita permanece inmutable sin experimentar traslación ni rotación alguna", "distractor_id": "D-C01-04", "error_rationale": "Falsa neutralidad del parámetro de ahorro @s1@ a @s2@"},
        {"value": "La tasa de ahorro marginal colapsa produciendo rendimientos decrecientes", "distractor_id": "D-C01-03", "error_rationale": "Confusión entre ahorro @s2@ y productividad marginal"},
        {"value": "La acumulación neta de capital se anula instantáneamente en este régimen", "distractor_id": "D-C01-05", "error_rationale": "Confusión entre régimen transitorio y estado estacionario con @s2@"},
        {"value": "El consumo por trabajador iguala a la inversión bruta en todo momento", "distractor_id": "D-C01-06", "error_rationale": "Supuesto arbitrario de igualdad ahorro-consumo para @delta_s@"},
    ]
    correct_str = f"La curva de inversión se desplaza {shift_dir} con nueva tasa de ahorro s = {s2}"
    return {"vars": {"s1": s1, "s2": s2, "delta_s": delta_s}, "correct": correct_str, "distractors": distractors}

def ver_c01_perturbation(res):
    c = str(res.get("correct", "")) if isinstance(res, dict) else str(res)
    v = res.get("vars", {}) if isinstance(res, dict) else {}
    return "se desplaza" in c and str(v.get("s2")) in c

# Archetype 4: Boundary Testing / Axiomatic Violations
def gen_c01_boundary(rng):
    s_lim = round(rng.uniform(0.001, 0.050), 4)
    cond = "mínimo"
    correct_str = rf"La inversión bruta converge al anularse el ahorro con tasa s = {s_lim}"

    distractors = [
        {"value": "La economía agregada alcanza de forma inmediata el óptimo dinámico prescrito por la regla de oro intertemporal", "distractor_id": "D-C01-01", "error_rationale": "Confusión con el óptimo intertemporal en régimen para tasa @s_lim@"},
        {"value": "El stock de capital per cápita diverge exponencialmente hacia infinito sin cota superior alguna en el largo plazo", "distractor_id": "D-C01-03", "error_rationale": "Falsa analogía con modelos endógenos en límite @s_lim@"},
        {"value": "La tasa efectiva de depreciación combinada colapsa a valores estrictamente negativos en todo el dominio analítico", "distractor_id": "D-C01-04", "error_rationale": "Violación axiomática de no-negatividad bajo régimen con @s_lim@"},
        {"value": "La función de producción global pierde los rendimientos constantes de escala", "distractor_id": "D-C01-02", "error_rationale": "Atribución de cambios tecnológicos a parámetro @s_lim@"},
        {"value": "El estado estacionario resultante colapsa a cero", "distractor_id": "D-C01-05", "error_rationale": "Atribución espuria de ciclos límite para tasa @s_lim@"},
        {"value": "La elasticidad del producto se descontinúa", "distractor_id": "D-C01-06", "error_rationale": "Atribución espuria de singularidad en régimen con @s_lim@"},
    ]
    return {"vars": {"s_lim": s_lim, "cond": cond}, "correct": correct_str, "distractors": distractors}

def ver_c01_boundary(res):
    c = str(res.get("correct", "")) if isinstance(res, dict) else str(res)
    v = res.get("vars", {}) if isinstance(res, dict) else {}
    return "anularse el ahorro" in c and str(v.get("s_lim")) in c


# --- Competency C-02 (Skill) Archetypes ---
def gen_c02_direct(rng):
    s = round(rng.uniform(0.15, 0.45), 2)
    denom = round(rng.uniform(0.04, 0.10), 3)
    ratio = s / denom
    k_star = round(ratio ** 2, 2)
    d_ids = ["D-C02-01", "D-C02-02", "D-C02-03", "D-C02-04", "D-C02-05", "D-C02-06"]
    rats = [
        "Sobreestimación por omisión del exponente cuadrático en capital @k_star@",
        "Subestimación por truncamiento de decimales para tasa @s@",
        "Inversión de los términos en el cociente de reposición @denom@",
        "Atribución de factor de depreciación duplicado en factor @denom@",
        "Sesgo aditivo espurio en la ecuación de equilibrio para @k_star@",
        "Sesgo sustractivo espurio en el despeje analítico con tasa @s@",
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
        "Desvío superior en el cálculo de la tasa requerida @s@",
        "Desvío inferior por aproximación truncada en tasa @s@",
        "Uso de k en lugar de la raíz cuadrada de capital @k_star@",
        "Cociente invertido entre tasa @denom@ y capital @k_star@",
        "Sesgo aditivo constante en la tasa de ahorro @s@",
        "Sesgo sustractivo constante en la tasa de ahorro @s@",
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
    distractors = [
        {"value": "La tasa de ahorro exógena se ajusta automáticamente para contrarrestar la dilución poblacional inducida", "distractor_id": "D-C02-04", "error_rationale": "Atribución errónea de endogeneidad ante tasa @n_new@"},
        {"value": "La productividad marginal del capital disminuye de forma discontinua a lo largo de toda la trayectoria", "distractor_id": "D-C02-05", "error_rationale": "Violación axiomática de continuidad para tasa @n_old@"},
        {"value": "El consumo por unidad de trabajo eficiente converge a una senda de crecimiento no balanceado y volátil", "distractor_id": "D-C02-06", "error_rationale": "Confusión de régimen transitorio con optimización para @delta_n@"},
        {"value": "El capital estacionario se incrementa por efecto escala", "distractor_id": "D-C02-01", "error_rationale": "Confusión entre dilución de capital y producto absoluto con @delta_n@"},
        {"value": "El capital estacionario permanece totalmente inalterado", "distractor_id": "D-C02-02", "error_rationale": "Falsa neutralidad demográfica ante cambio de @n_old@ a @n_new@"},
        {"value": "El sistema diverge hacia una trayectoria inestable", "distractor_id": "D-C02-03", "error_rationale": "Atribución espuria de dinámica caótica ante variación @delta_n@"},
    ]
    correct_str = rf"El capital $k^*$ disminuye al incrementarse la reposición con tasa n = {n_new}"
    return {"vars": {"n_old": n_old, "n_new": n_new, "delta_n": delta_n}, "correct": correct_str, "distractors": distractors}

def ver_c02_perturbation(res):
    c = str(res.get("correct", "")) if isinstance(res, dict) else str(res)
    v = res.get("vars", {}) if isinstance(res, dict) else {}
    return "disminuye al incrementarse la reposición" in c and str(v.get("n_new")) in c

def gen_c02_boundary(rng):
    sample_rate = round(rng.uniform(0.001, 0.050), 4)
    correct_str = rf"Bajo {sample_rate}, $k^*$ tiende a infinito al anularse la reposición"
    distractors = [
        {"value": "La economía deja de producir bienes al alcanzarse la frontera analítica del espacio de estados posibles", "distractor_id": "D-C02-02", "error_rationale": "Confusión entre dinámica de capital y nivel de producto con @sample_rate@"},
        {"value": "El estado estacionario resultante genera fluctuaciones y oscilaciones cíclicas explosivas no lineales", "distractor_id": "D-C02-04", "error_rationale": "Atribución errónea de inestabilidad ante valor @sample_rate@"},
        {"value": "El stock de capital por trabajador efectivo se desploma súbitamente a cero en toda la trayectoria temporal", "distractor_id": "D-C02-01", "error_rationale": "Inversión errónea de la cota de reposición para @sample_rate@"},
        {"value": "La función de ahorro converge a una cota fija", "distractor_id": "D-C02-03", "error_rationale": "Confusión analítica de singularidad asintótica con @sample_rate@"},
        {"value": "El producto per cápita alcanza un valor simétrico interior", "distractor_id": "D-C02-05", "error_rationale": "Atribución de óptimo local en lugar de divergencia asintótica"},
        {"value": "La velocidad transitoria se anula", "distractor_id": "D-C02-06", "error_rationale": "Confusión entre cota de nivel y velocidad de transición"},
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
    r"Analice el impacto cualitativo de un aumento en la tasa de ahorro de $s_1 = {s1}$ a $s_2 = {s2}$ sobre la curva de inversión:",
    r"Examine la traslación de la función de ahorro e inversión ante una variación de $s_1 = {s1}$ a $s_2 = {s2}$:",
    r"Determine la respuesta gráfica del flujo de inversión cuando la tasa de ahorro cambia de $s_1 = {s1}$ a $s_2 = {s2}$:",
    r"Evalúe el desplazamiento de la curva de inversión si el ahorro pasa de $s_1 = {s1}$ a $s_2 = {s2}$:",
    r"Indique el cambio geométrico en la inversión bruta tras subir la tasa de $s_1 = {s1}$ a $s_2 = {s2}$:",
    r"Describa la traslación vertical de la función de inversión ante el salto de $s_1 = {s1}$ a $s_2 = {s2}$:",
    r"Verifique la nueva posición de la curva de ahorro tras variar de $s_1 = {s1}$ a $s_2 = {s2}$:",
]
stems_c01_4 = [
    r"Examine las implicaciones teóricas en el caso límite de régimen de ahorro {cond} con $s = {s_lim}$:",
    r"Analice el comportamiento asintótico del sistema económico en la frontera {cond} fijando $s = {s_lim}$:",
    r"Evalúe la dinámica de acumulación en el escenario extremo {cond} bajo el valor de parámetro $s = {s_lim}$:",
    r"Determine el balance asintótico en la cota {cond} con parámetro $s = {s_lim}$:",
    r"Identifique la conducta límite del modelo en el régimen {cond} con tasa $s = {s_lim}$:",
    r"Halle las consecuencias analíticas para la condición {cond} al fijar $s = {s_lim}$:",
    r"Compruebe la estabilidad de frontera del sistema en el entorno {cond} con $s = {s_lim}$:",
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
    r"Considere un incremento en la tasa de crecimiento poblacional de $n = {n_old}$ a $n = {n_new}$. ¿Cómo responde el capital $k^*$?",
    r"Analice el efecto sobre el capital de equilibrio $k^*$ ante un shock demográfico de $n = {n_old}$ a $n = {n_new}$:",
    r"Examine la sensibilidad del estado estacionario $k^*$ cuando la tasa demográfica varía de $n = {n_old}$ a $n = {n_new}$:",
    r"Determine el cambio en el capital $k^*$ si el crecimiento laboral pasa de $n = {n_old}$ a $n = {n_new}$:",
    r"Evalúe la contracción de $k^*$ causada por una expansión poblacional de $n = {n_old}$ a $n = {n_new}$:",
    r"Halle el impacto sobre la dotación de equilibrio $k^*$ al subir la natalidad de $n = {n_old}$ a $n = {n_new}$:",
    r"Compruebe la variación de $k^*$ provocada por el incremento en $n$ desde {n_old} hasta {n_new}:",
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

hints_c01 = [
    "Identifique la tasa de ahorro y el producto per cápita.",
    "Aplique la relación fundamental de inversión bruta.",
    "Verifique la escala del valor numérico obtenido.",
]
hints_c02 = [
    "Iguale la inversión bruta a la depreciación de reposición.",
    "Divida ambos lados por la función de producción per cápita.",
    "Eleve al exponente adecuado para despejar el capital estacionario.",
]

TEMPLATES = [
    # Competency C-01: 4 Archetypes
    ("T-C-01-01", "C-01", "multiple_choice", gen_c01_direct, ver_c01_direct, ("easy", "Remember"), stems_c01_1, hints_c01, r"La inversión es $i = s y = ({s})({y}) = {inv}$."),
    ("T-C-01-02", "C-01", "fill_in_the_blank", gen_c01_inverse, ver_c01_inverse, ("medium", "Understand"), stems_c01_2, hints_c01, r"Despejando, $s = i / y = {inv} / {y} = {s}$."),
    ("T-C-01-03", "C-01", "multiple_choice", gen_c01_perturbation, ver_c01_perturbation, ("hard", "Apply"), stems_c01_3, hints_c01, r"Un incremento en $s$ desplaza la curva de inversión verticalmente hacia arriba."),
    ("T-C-01-04", "C-01", "multiple_choice", gen_c01_boundary, ver_c01_boundary, ("hard", "Analyze"), stems_c01_4, hints_c01, r"En el caso límite analizado, el comportamiento del sistema refleja la condición de frontera."),

    # Competency C-02: 4 Archetypes
    ("T-C-02-01", "C-02", "fill_in_the_blank", gen_c02_direct, ver_c02_direct, ("easy", "Remember"), stems_c02_1, hints_c02, r"En estado estacionario, $s \sqrt{k} = ({denom})k \implies k^* = (s/{denom})^2 = {k_star}$."),
    ("T-C-02-02", "C-02", "fill_in_the_blank", gen_c02_inverse, ver_c02_inverse, ("medium", "Understand"), stems_c02_2, hints_c02, r"Despejando, $s = \sqrt{k^*} ({denom}) = {s}$."),
    ("T-C-02-03", "C-02", "multiple_choice", gen_c02_perturbation, ver_c02_perturbation, ("hard", "Apply"), stems_c02_3, hints_c02, r"Un aumento en $n$ incrementa la pendiente de la recta de reposición reduciendo $k^*$."),
    ("T-C-02-04", "C-02", "multiple_choice", gen_c02_boundary, ver_c02_boundary, ("hard", "Analyze"), stems_c02_4, hints_c02, r"Al anularse el denominador de la relación de equilibrio, $k^*$ diverge hacia infinito."),
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
        "Suma espuria de tres unidades para @k@",
        "Sustracción de cinco unidades con respecto al balance para @k@",
        "Adición de siete unidades en la estimación de @k@",
        "Sustracción de nueve unidades en la resolución analítica con @k@",
        "Desvío de once unidades sobre el producto de @k@",
        "Desvío sustractivo de trece unidades para @k@",
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
        "Desvío de cuatro unidades en la tasa analítica con @k@",
        "Sustracción de cuatro unidades sobre el cálculo de @k@",
        "Desvío aditivo de ocho unidades para el nivel @k@",
        "Sustracción de ocho unidades en el despeje para @k@",
        "Desvío de catorce unidades sobre la función con @k@",
        "Sustracción de catorce unidades en el balance con @k@",
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
        {"content": f"El valor límite es menor a {k - 5}", "is_correct": False, "distractor_id": "D-C01-01", "error_rationale": "Subestimación del umbral con parámetro @k@"},
        {"content": f"La relación se anula para {k}", "is_correct": False, "distractor_id": "D-C01-02", "error_rationale": "Atribución espuria de anulación para parámetro @k@"},
        {"content": f"La tasa diverge sin cota para {k}", "is_correct": False, "distractor_id": "D-C01-03", "error_rationale": "Falsa divergencia en régimen con parámetro @k@"},
    ]
    return {"vars": {"k": k}, "options": options, "correct": "A"}

def ver_ms(res):
    opts = res.get("options", [])
    return len(opts) == 4 and all(o.get("is_correct") == (o.get("distractor_id") is None) for o in opts)

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

hints_common = [
    "Identifique las variables relevantes del enunciado.",
    "Aplique la relación analítica fundamental entre factores.",
    "Verifique la coherencia y magnitud del cálculo obtenido.",
]

TEMPLATES = [
    ("T-C-01-01", "C-01", "multiple_choice", gen_mc, ver_mc, ("easy", "Remember"), stems_mc, hints_common, "Solución formal."),
    ("T-C-01-02", "C-01", "fill_in_the_blank", gen_fib, ver_fib, ("medium", "Apply"), stems_fib, hints_common, "Solución FIB."),
    ("T-C-01-03", "C-01", "multiple_select", gen_ms, ver_ms, ("hard", "Analyze"), stems_ms, hints_common, "Solución MS."),
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
                        "remediation_hint": f"Pista formativa {i}",
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
                        "remediation_hint": f"Pista cálculo {i}",
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

