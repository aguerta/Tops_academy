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
        "Sobreestimación de propensión marginal al ahorro",
        "Subestimación de propensión marginal al ahorro",
        "Atribución de factor de escala tecnológico espurio",
        "Deducción contractiva no justificada",
        "Confusión entre ahorro voluntario y ahorro forzoso",
        "Omisión de depreciación en la inversión bruta",
    ]
    distractors = [
        {"value": rf"${round(inv + (i + 1) * 3.5, 2)}$", "distractor_id": did, "error_rationale": rat}
        for i, (did, rat) in enumerate(zip(d_ids, rats))
    ]
    return {"vars": {"s": s, "y": y, "inv": inv}, "correct": rf"${inv}$", "distractors": distractors}

def ver_c01_direct(res):
    v = res["vars"]
    return abs(round(v["s"] * v["y"], 2) - v["inv"]) < 1e-4

# Archetype 2: Inverse / Diagnostic
def gen_c01_inverse(rng):
    y = rng.randint(40, 100)
    s_pct = rng.randint(15, 45)
    s = round(s_pct / 100.0, 2)
    inv = round(s * y, 2)
    d_ids = ["D-C01-01", "D-C01-02", "D-C01-03", "D-C01-04", "D-C01-05", "D-C01-06"]
    rats = [
        "Desvío positivo en el despeje algebraico del ahorro",
        "Desvío negativo en el cálculo del coeficiente",
        "Multiplicación de inversión por producto",
        "Inversión del cociente analítico de solvencia",
        "Suma directa de constante no normalizada",
        "Resta arbitraria en el cálculo del ratio",
    ]
    distractors = [
        {"value": rf"$s = {round(s + (i + 1) * 0.05, 2)}$", "distractor_id": did, "error_rationale": rat}
        for i, (did, rat) in enumerate(zip(d_ids, rats))
    ]
    return {"vars": {"inv": inv, "y": y, "s": s}, "correct": rf"$s = {s}$", "distractors": distractors}

def ver_c01_inverse(res):
    v = res["vars"]
    return abs(v["inv"] - round(v["s"] * v["y"], 2)) < 1e-4

# Archetype 3: Comparative Statics / Perturbation
def gen_c01_perturbation(rng):
    s1 = rng.choice([0.18, 0.22, 0.26, 0.30, 0.34, 0.38, 0.42])
    delta_s = rng.choice([0.04, 0.06, 0.08, 0.10, 0.12])
    s2 = round(s1 + delta_s, 2)
    shift_dir = "hacia arriba" if delta_s > 0 else "hacia abajo"
    distractors = [
        {"value": "La curva de inversión rota en sentido horario convergiendo a cero", "distractor_id": "D-C01-01", "error_rationale": "Confusión entre desplazamiento y rotación"},
        {"value": "La recta de depreciación incrementa su pendiente de forma automática", "distractor_id": "D-C01-02", "error_rationale": "Atribución errónea del efecto a la depreciación"},
        {"value": "La tasa de ahorro marginal colapsa produciendo rendimientos decrecientes", "distractor_id": "D-C01-03", "error_rationale": "Confusión entre ahorro y productividad marginal"},
        {"value": "El nivel de producto per cápita permanece estrictamente inmutable", "distractor_id": "D-C01-04", "error_rationale": "Falsa neutralidad del parámetro de ahorro"},
        {"value": "La acumulación neta de capital se anula instantáneamente en el plano", "distractor_id": "D-C01-05", "error_rationale": "Confusión entre régimen transitorio y estado estacionario"},
        {"value": "El consumo por trabajador iguala a la inversión bruta en todo momento", "distractor_id": "D-C01-06", "error_rationale": "Supuesto arbitrario de igualdad ahorro-consumo"},
    ]
    correct_str = rf"La curva de inversión se desplaza {shift_dir} en el diagrama fundamental de Solow"
    return {"vars": {"s1": s1, "s2": s2, "delta_s": delta_s}, "correct": correct_str, "distractors": distractors}

def ver_c01_perturbation(res):
    return "diagrama fundamental" in res["correct"]

# Archetype 4: Boundary Testing / Axiomatic Violations
def gen_c01_boundary(rng):
    s_lim = rng.choice([0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.992, 0.994])
    if s_lim < 0.5:
        cond = "mínimo"
        correct_str = "La inversión bruta per cápita converge a cero asintóticamente al anularse el ahorro"
    else:
        cond = "máximo"
        correct_str = "El consumo agregado por trabajador converge a cero asintóticamente en dicho límite"

    distractors = [
        {"value": "La economía alcanza el óptimo dinámico de la regla de oro de Phelps en equilibrio", "distractor_id": "D-C01-01", "error_rationale": "Confusión con el óptimo de consumo intertemporal"},
        {"value": "La función de producción global pierde los rendimientos constantes a escala agregados", "distractor_id": "D-C01-02", "error_rationale": "Atribución de cambios tecnológicos a parámetros de ahorro"},
        {"value": "El capital per cápita diverge exponencialmente sin cota analítica alguna en el tiempo", "distractor_id": "D-C01-03", "error_rationale": "Falsa analogía con modelos de crecimiento endógeno"},
        {"value": "La tasa efectiva de depreciación del capital colapsa a valores negativos no admisibles", "distractor_id": "D-C01-04", "error_rationale": "Violación axiomática de no-negatividad en parámetros físicos"},
        {"value": "El estado estacionario se convierte en una órbita periódica cerrada y estable en Solow", "distractor_id": "D-C01-05", "error_rationale": "Atribución espuria de ciclos límite en sistemas unidimensionales"},
        {"value": "La elasticidad del producto respecto al capital se vuelve discontinua en la frontera", "distractor_id": "D-C01-06", "error_rationale": "Atribución espuria de singularidad en la función de producción"},
    ]
    return {"vars": {"s_lim": s_lim, "cond": cond}, "correct": correct_str, "distractors": distractors}

def ver_c01_boundary(res):
    return "asintóticamente" in res["correct"]


# --- Competency C-02 (Skill) Archetypes ---
def gen_c02_direct(rng):
    s = rng.choice([0.16, 0.20, 0.24, 0.28, 0.32, 0.36, 0.40, 0.44])
    denom = rng.choice([0.05, 0.06, 0.07, 0.08, 0.09, 0.10])
    ratio = s / denom
    k_star = round(ratio ** 2, 2)
    d_ids = ["D-C02-01", "D-C02-02", "D-C02-03", "D-C02-04", "D-C02-05", "D-C02-06"]
    rats = [
        "Sobreestimación por omisión del exponente cuadrático",
        "Subestimación por truncamiento de decimales",
        "Inversión de los términos en el cociente de reposición",
        "Atribución de factor de depreciación duplicado",
        "Sesgo aditivo espurio en la ecuación de equilibrio",
        "Sesgo sustractivo espurio en el despeje analítico",
    ]
    distractors = [
        {"value": rf"$k^* = {round(k_star + (i + 1) * 4.5, 2)}$", "distractor_id": did, "error_rationale": rat}
        for i, (did, rat) in enumerate(zip(d_ids, rats))
    ]
    return {"vars": {"s": s, "denom": denom, "k_star": k_star}, "correct": rf"$k^* = {k_star}$", "distractors": distractors}

def ver_c02_direct(res):
    v = res["vars"]
    return abs(round((v["s"] / v["denom"]) ** 2, 2) - v["k_star"]) < 1e-4

def gen_c02_inverse(rng):
    k_root = rng.randint(4, 15)
    k_star = round(float(k_root ** 2), 2)
    denom = rng.choice([0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10])
    s = round(k_root * denom, 3)
    d_ids = ["D-C02-01", "D-C02-02", "D-C02-03", "D-C02-04", "D-C02-05", "D-C02-06"]
    rats = [
        "Desvío superior en el cálculo de la tasa requerida",
        "Desvío inferior por aproximación truncada",
        "Uso de k en lugar de la raíz cuadrada de k",
        "Cociente invertido entre depreciación y capital",
        "Sesgo aditivo constante en la tasa de ahorro",
        "Sesgo sustractivo constante en la tasa de ahorro",
    ]
    distractors = [
        {"value": rf"$s = {round(s + (i + 1) * 0.04, 3)}$", "distractor_id": did, "error_rationale": rat}
        for i, (did, rat) in enumerate(zip(d_ids, rats))
    ]
    return {"vars": {"k_star": k_star, "denom": denom, "s": s}, "correct": rf"$s = {s}$", "distractors": distractors}

def ver_c02_inverse(res):
    v = res["vars"]
    return abs(round(math.sqrt(v["k_star"]) * v["denom"], 3) - v["s"]) < 1e-4

def gen_c02_perturbation(rng):
    n_old = rng.choice([0.01, 0.02, 0.03])
    delta_n = rng.choice([0.01, 0.02, 0.03, 0.04, 0.05, 0.06])
    n_new = round(n_old + delta_n, 3)
    distractors = [
        {"value": "El capital estacionario se incrementa debido al mayor tamaño de la fuerza laboral agregada", "distractor_id": "D-C02-01", "error_rationale": "Confusión entre dilución de capital y producto absoluto"},
        {"value": "El capital estacionario permanece inalterado por neutralidad demográfica de largo plazo", "distractor_id": "D-C02-02", "error_rationale": "Falsa neutralidad demográfica en el modelo neoclásico"},
        {"value": "El sistema diverge hacia una trayectoria caótica no convergente de acumulación", "distractor_id": "D-C02-03", "error_rationale": "Atribución espuria de dinámica caótica en ecuaciones cóncavas"},
        {"value": "La tasa de ahorro se ajusta endógenamente para compensar la dilución de trabajadores", "distractor_id": "D-C02-04", "error_rationale": "Atribución errónea de endogeneidad en parámetros de conducta"},
        {"value": "La productividad marginal del capital disminuye discontinuamente a un valor nulo", "distractor_id": "D-C02-05", "error_rationale": "Violación axiomática de continuidad en la función de producción"},
        {"value": "El consumo per cápita converge instantáneamente a la regla de oro modificada", "distractor_id": "D-C02-06", "error_rationale": "Confusión de régimen transitorio con optimización de Ramsey"},
    ]
    correct_str = rf"El capital estacionario $k^*$ disminuye al incrementarse la pendiente de reposición efectiva"
    return {"vars": {"n_old": n_old, "n_new": n_new, "delta_n": delta_n}, "correct": correct_str, "distractors": distractors}

def ver_c02_perturbation(res):
    return "disminuye al incrementarse la pendiente" in res["correct"]

def gen_c02_boundary(rng):
    sample_rate = rng.choice([0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008])
    correct_str = r"Cuando $(n + g + \delta) \to 0^+$, la tasa de reposición se anula y el capital $k^*$ tiende a infinito"
    distractors = [
        {"value": "El capital estacionario colapsa asintóticamente a cero por falta de renovación tecnológica", "distractor_id": "D-C02-01", "error_rationale": "Inversión del comportamiento límite en el cociente"},
        {"value": "La economía deja de producir bienes y el consumo por trabajador se extingue", "distractor_id": "D-C02-02", "error_rationale": "Confusión entre dinámica de capital y nivel de producto"},
        {"value": "La función de producción global pierde su propiedad de homogeneidad de grado uno", "distractor_id": "D-C02-03", "error_rationale": "Atribución errónea de cambio tecnológico a tasas demográficas"},
        {"value": "El estado estacionario resultante es dinámicamente inestable y genera oscilaciones", "distractor_id": "D-C02-04", "error_rationale": "Atribución errónea de inestabilidad en modelo de Solow"},
        {"value": "La tasa de ahorro voluntario se transforma en una variable residual compensatoria", "distractor_id": "D-C02-05", "error_rationale": "Violación de supuestos de comportamiento exógeno"},
        {"value": "El producto marginal del capital se fija de manera inelástica en la unidad global", "distractor_id": "D-C02-06", "error_rationale": "Atribución de valor arbitrario a la derivada de producción"},
    ]
    return {"vars": {"sample_rate": sample_rate}, "correct": correct_str, "distractors": distractors}

def ver_c02_boundary(res):
    return "tiende a infinito" in res["correct"]


TEMPLATES = [
    # Competency C-01: 4 Archetypes
    ("C-01", "multiple_choice", r"Considere una tasa de ahorro $s = {s}$ y un producto $y = {y}$. Calcule la inversión bruta per cápita:", gen_c01_direct, ver_c01_direct, r"La inversión es $i = s y = ({s})({y}) = {inv}$.", "Inversión Bruta", ["D-C01-01", "D-C01-02", "D-C01-03", "D-C01-04", "D-C01-05", "D-C01-06"], ("solow.pdf", 5, "Inversión"), ["Identifique la tasa de ahorro y el producto.", "Multiplique ambos términos.", "Verifique el valor resultante."]),
    ("C-01", "multiple_choice", r"Si la inversión es $i = {inv}$ y el producto es $y = {y}$, determine la tasa de ahorro implícita $s$:", gen_c01_inverse, ver_c01_inverse, r"Despejando, $s = i / y = {inv} / {y} = {s}$.", "Despeje de Tasa de Ahorro", ["D-C01-01", "D-C01-02", "D-C01-03", "D-C01-04", "D-C01-05", "D-C01-06"], ("solow.pdf", 6, "Inversión inversa"), ["Plantee la relación i = s y.", "Despeje la tasa s como cociente.", "Calcule el valor escalar."]),
    ("C-01", "multiple_choice", r"Analice el impacto cualitativo de un aumento exógeno en la tasa de ahorro de $s_1 = {s1}$ a $s_2 = {s2}$ sobre la curva de inversión:", gen_c01_perturbation, ver_c01_perturbation, r"Un incremento en $s$ desplaza la curva de inversión verticalmente hacia arriba.", "Estática Comparativa de Ahorro", ["D-C01-01", "D-C01-02", "D-C01-03", "D-C01-04", "D-C01-05", "D-C01-06"], ("solow.pdf", 7, "Perturbación"), ["Examine el signo de Delta s.", "Analice el desplazamiento gráfico de la función s f(k).", "Identifique la conclusión correcta."]),
    ("C-01", "multiple_choice", r"Examine las implicaciones teóricas en el caso límite de régimen de ahorro ${cond}$ con $s = {s_lim}$:", gen_c01_boundary, ver_c01_boundary, r"En el caso límite analizado, el comportamiento del sistema refleja la condición de frontera.", "Casos Límite de Ahorro", ["D-C01-01", "D-C01-02", "D-C01-03", "D-C01-04", "D-C01-05", "D-C01-06"], ("solow.pdf", 8, "Límites"), ["Considere el valor extremo del parámetro.", "Evalúe las ecuaciones dinámicas en dicha frontera.", "Determine la implicación formal."]),

    # Competency C-02: 4 Archetypes
    ("C-02", "multiple_choice", r"Bajo $s = {s}$ y tasa de depreciación efectiva combinada $(n + g + \delta) = {denom}$, halle $k^*$ con $f(k) = \sqrt{{k}}$:", gen_c02_direct, ver_c02_direct, r"En estado estacionario, $s \sqrt{{k}} = ({denom})k \implies k^* = (s/{denom})^2 = {k_star}$.", "Estado Estacionario Frontal", ["D-C02-01", "D-C02-02", "D-C02-03", "D-C02-04", "D-C02-05", "D-C02-06"], ("solow.pdf", 10, "Cálculo k*"), ["Iguale inversión a depreciación de reposición.", "Divida por la raíz de k.", "Eleve al cuadrado para despejar k*."]),
    ("C-02", "multiple_choice", r"Si se desea sostener un capital de estado estacionario $k^* = {k_star}$ con $(n+g+\delta) = {denom}$, determine la tasa de ahorro requerida $s$:", gen_c02_inverse, ver_c02_inverse, r"Despejando, $s = \sqrt{{k^*}} ({denom}) = {s}$.", "Despeje Inverso de k*", ["D-C02-01", "D-C02-02", "D-C02-03", "D-C02-04", "D-C02-05", "D-C02-06"], ("solow.pdf", 11, "Despeje s"), ["Plantee la condición de equilibrio.", "Sustituya k* y el denominador.", "Calcule la tasa s necesaria."]),
    ("C-02", "multiple_choice", r"Considere un incremento en la tasa de crecimiento poblacional de $n = {n_old}$ a $n = {n_new}$. ¿Cómo responde el capital $k^*$?", gen_c02_perturbation, ver_c02_perturbation, r"Un aumento en $n$ incrementa la pendiente de la recta de reposición reduciendo $k^*$.", "Perturbación Demográfica", ["D-C02-01", "D-C02-02", "D-C02-03", "D-C02-04", "D-C02-05", "D-C02-06"], ("solow.pdf", 12, "Shock poblacional"), ["Analice el efecto de n sobre la recta de depreciación.", "Observe la nueva intersección con la curva de ahorro.", "Deduzca la dirección del cambio en k*."]),
    ("C-02", "multiple_choice", r"Considere el caso límite donde la tasa combinada $(n + g + \delta) \to 0$. Analice la trayectoria asintótica de $k^*$:", gen_c02_boundary, ver_c02_boundary, r"Al anularse el denominador de la relación de equilibrio, $k^*$ diverge hacia infinito.", "Frontera Asintótica k*", ["D-C02-01", "D-C02-02", "D-C02-03", "D-C02-04", "D-C02-05", "D-C02-06"], ("solow.pdf", 13, "Límites k*"), ["Examine el comportamiento del cociente cuando el divisor tiende a cero.", "Analice la ausencia de depreciación en la acumulación.", "Concluya sobre la divergencia asintótica."]),
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
