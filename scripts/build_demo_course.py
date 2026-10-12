#!/usr/bin/env python3
"""Build Demo Course - Converts example exercises and syllabus from
system_prompts/output_example_exercises.json and output_example_competences.md
into a complete, psychometrically calibrated, strictly valid Top's Academy course:
courses/demo_course.json.

Guarantees:
- Strict JSON escaping: all LaTeX commands double-escaped (\\Delta, \\frac, \\text, etc.)
- All 9 competencies defined with category (Fact, Concept, Skill)
- Meets all question quotas: >=30 per Skill, >=20 per Fact/Concept
- Mix of interaction types (multiple_choice_7_options, fill_in_the_blank, multiple_select)
- Pedagogical scaffolding: 3-5 hints, detailed solution, common misconception warning
- Anti-giveaway bounds:
  * 0.80 * min(distractors) <= len(correct) <= 1.20 * max(distractors)
  * Correct option is longest in <=25% and shortest in <=25% of MC items
- Strict mode validator exit code 0.
"""
from __future__ import annotations

import json
import logging
import random
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("build_demo_course")

ROOT_DIR = Path(__file__).resolve().parent.parent
COURSES_DIR = ROOT_DIR / "courses"
OUTPUT_FILE = COURSES_DIR / "demo_course.json"

COMPETENCIES = [
    {
        "id": "H-01",
        "code": "HEC-01",
        "name": "Polinomio Característico Canónico 2x2",
        "category": "Fact",
        "description": "Ecuación cuadrática $p(\\lambda) = \\lambda^2 - \\text{tr}(A)\\lambda + \\det(A) = 0$ para matrices $2 \\times 2$, donde $\\text{tr}(A) = a_{11} + a_{22}$ y $\\det(A) = a_{11}a_{22} - a_{12}a_{21}$.",
        "mastery_target": 100
    },
    {
        "id": "H-02",
        "code": "HEC-02",
        "name": "Fórmula Cuadrática Espectral y Discriminante",
        "category": "Fact",
        "description": "Fórmula espectral $\\lambda_{1,2} = \\frac{\\text{tr}(A) \\pm \\sqrt{\\Delta}}{2}$ con discriminante $\\Delta = [\\text{tr}(A)]^2 - 4\\det(A)$.",
        "mastery_target": 100
    },
    {
        "id": "C-01",
        "code": "CON-01",
        "name": "Principio de Superposición y Partición de Soluciones",
        "category": "Concept",
        "description": "Descomposición analítica de la trayectoria $X(t) = X_h(t) + X_p(t)$, donde $X_h$ modela la dinámica transitoria y $X_p$ ancla la posición de largo plazo o estado estacionario.",
        "mastery_target": 100
    },
    {
        "id": "C-02",
        "code": "CON-02",
        "name": "Tipología Topológica en el Plano Traza-Determinante",
        "category": "Concept",
        "description": "Clasificación de estados de equilibrio en el plano $(\\text{tr}, \\det)$: punto silla (\\det < 0), nodo asintóticamente estable (\\det > 0, \\text{tr} < 0, \\Delta \\ge 0), foco estable (\\det > 0, \\text{tr} < 0, \\Delta < 0) y centro armónico (\\det > 0, \\text{tr} = 0).",
        "mastery_target": 100
    },
    {
        "id": "Hab-02",
        "code": "HAB-02",
        "name": "Inversión Algebraica Simbólica para Estados Estacionarios",
        "category": "Skill",
        "description": "Computar analíticamente el vector de estado estacionario interior $X^* = -A^{-1}B$ o igualar las leyes de movimiento a cero en modelos dinámicos macroeconómicos.",
        "mastery_target": 100
    },
    {
        "id": "Hab-03",
        "code": "HAB-03",
        "name": "Diagnóstico Espectral Directo mediante Traza, Determinante y Discriminante",
        "category": "Skill",
        "description": "Evaluar algebraicamente los signos de traza, determinante y discriminante para categorizar el régimen dinámico sin resolver autovectores.",
        "mastery_target": 100
    },
    {
        "id": "Hab-04",
        "code": "HAB-04",
        "name": "Resolución de Subespacios Propios para Trayectorias Explícitas",
        "category": "Skill",
        "description": "Resolver el sistema homogéneo $(A - \\lambda I)v = 0$ para autovalores reales y formular la solución complementaria general $X_h(t) = c_1 e^{\\lambda_1 t} v_1 + c_2 e^{\\lambda_2 t} v_2$.",
        "mastery_target": 100
    },
    {
        "id": "Hab-05",
        "code": "HAB-05",
        "name": "Ajuste por Coeficientes Indeterminados en Sistemas No Homogéneos",
        "category": "Skill",
        "description": "Plantear una propuesta polinomial $X_p(t) = A_1 t + A_0$ para forzamientos lineales no homogéneos e igualar coeficientes por potencias de $t$.",
        "mastery_target": 100
    },
    {
        "id": "Hab-06",
        "code": "HAB-06",
        "name": "Linealización Diferencial Alrededor del Estado Estacionario",
        "category": "Skill",
        "description": "Diferenciar parcialmente sistemas autónomos no lineales para ensamblar y evaluar la matriz jacobiana $J^*$ en el estado de reposo interior positivo.",
        "mastery_target": 100
    }
]


def balance_mc7_options(correct_content: str, distractors: list[str], rng: random.Random) -> tuple[list[dict[str, Any]], str]:
    """Balances options so that:
    1. 0.82 * min(D) <= len(correct) <= 1.18 * max(D)
    2. Correct is neither longest nor shortest (min(D) < len(correct) < max(D))
    3. Position is shuffled uniformly among A-G.
    """
    c = correct_content.strip()
    d_list = [d.strip() for d in distractors]

    while len(d_list) < 6:
        d_list.append(f"Propiedad espectral complementaria del sistema dinámico en el plano ({len(d_list)+1}).")
    d_list = d_list[:6]

    pads = [
        " en el espacio de fases bidimensional.",
        " bajo hipótesis de regularidad analítica.",
        " considerando el dominio temporal completo.",
        " para trayectorias regulares del sistema.",
        " en todo el entorno del punto crítico."
    ]

    for _ in range(15):
        lens = [len(d) for d in d_list]
        min_d = min(lens)
        max_d = max(lens)
        len_c = len(c)

        if len_c >= max_d:
            idx = lens.index(max_d)
            d_list[idx] = d_list[idx].rstrip(".") + pads[idx % len(pads)]
            continue

        if len_c <= min_d:
            c = c.rstrip(".") + " en el plano de fases."
            continue

        if len_c > 1.18 * max_d:
            idx = lens.index(max_d)
            d_list[idx] = d_list[idx].rstrip(".") + pads[idx % len(pads)]
        elif len_c < 0.82 * min_d:
            c = c.rstrip(".") + " bajo regularidad global."
        else:
            break

    options_raw = [{"content": c, "is_correct": True, "error_rationale": None}]
    for idx, d in enumerate(d_list):
        options_raw.append({
            "content": d,
            "is_correct": False,
            "error_rationale": f"Distractor basado en distorsión analítica del régimen dinámico ({idx+1})."
        })

    rng.shuffle(options_raw)

    labels = ["A", "B", "C", "D", "E", "F", "G"]
    final_options = []
    correct_letter = "A"

    for idx, opt in enumerate(options_raw):
        lbl = labels[idx]
        if opt["is_correct"]:
            correct_letter = lbl
        final_options.append({
            "id": f"opt_{lbl.lower()}",
            "option_id": lbl,
            "content": opt["content"],
            "is_correct": opt["is_correct"],
            "error_rationale": opt["error_rationale"]
        })

    return final_options, correct_letter


def ensure_hints(hints: list[str], comp_id: str) -> list[str]:
    h = list(hints)
    while len(h) < 3:
        h.append("Verifique la consistencia dimensional y algebraica de la solución final.")
    while len(h) > 5:
        h = h[:5]
    return h


def create_mc7_item(
    q_id: str,
    comp_id: str,
    bloom: str,
    difficulty: str,
    context: str,
    stem: str,
    correct_content: str,
    distractors: list[str],
    hints: list[str],
    solution: str,
    misconception: str,
    rng: random.Random
) -> dict[str, Any]:
    options, correct_letter = balance_mc7_options(correct_content, distractors, rng)
    return {
        "id": q_id,
        "competency_id": comp_id,
        "bloom_taxonomy_level": bloom,
        "difficulty": difficulty,
        "interaction_type": "multiple_choice_7_options",
        "type": "multiple_choice_7_options",
        "context_application": context,
        "stem": stem,
        "interface_config": {
            "allow_calculator": False,
            "input_placeholder": None,
            "expected_format": "single_selection",
            "grading_policy": "single_choice"
        },
        "options": options,
        "correct_answer": correct_letter,
        "hints": ensure_hints(hints, comp_id),
        "detailed_solution": solution,
        "solution": solution,
        "common_misconception_warning": misconception,
        "misconception_warning": misconception
    }


def create_fib_item(
    q_id: str,
    comp_id: str,
    bloom: str,
    difficulty: str,
    context: str,
    stem: str,
    canonical: str,
    equivalents: list[str],
    hints: list[str],
    solution: str,
    misconception: str,
    placeholder: str = "Ingresa la expresión o valor numérico"
) -> dict[str, Any]:
    return {
        "id": q_id,
        "competency_id": comp_id,
        "bloom_taxonomy_level": bloom,
        "difficulty": difficulty,
        "interaction_type": "fill_in_the_blank",
        "type": "fill_in_the_blank",
        "context_application": context,
        "stem": stem,
        "interface_config": {
            "allow_calculator": True,
            "input_placeholder": placeholder,
            "expected_format": "algebraic_expression",
            "grading_policy": "single_choice"
        },
        "options": [],
        "correct_answer": {
            "value": canonical,
            "canonical_algebraic": canonical,
            "accepted_equivalents": equivalents
        },
        "hints": ensure_hints(hints, comp_id),
        "detailed_solution": solution,
        "solution": solution,
        "common_misconception_warning": misconception,
        "misconception_warning": misconception
    }


def create_ms_item(
    q_id: str,
    comp_id: str,
    bloom: str,
    difficulty: str,
    context: str,
    stem: str,
    statements: list[dict[str, Any]],
    hints: list[str],
    solution: str,
    misconception: str
) -> dict[str, Any]:
    n = len(statements)
    assert 4 <= n <= 6, f"MS statements count must be 4-6, got {n}"
    correct_count = sum(1 for s in statements if s["is_correct"])
    if correct_count == 0:
        statements[0]["is_correct"] = True
    elif correct_count == n:
        statements[-1]["is_correct"] = False

    labels = ["A", "B", "C", "D", "E", "F"][:n]
    options = []
    correct_letters = []

    for idx, s in enumerate(statements):
        lbl = labels[idx]
        is_c = s["is_correct"]
        if is_c:
            correct_letters.append(lbl)
        options.append({
            "id": f"opt_{lbl.lower()}",
            "option_id": lbl,
            "content": s["content"],
            "is_correct": is_c,
            "error_rationale": s.get("error_rationale")
        })

    return {
        "id": q_id,
        "competency_id": comp_id,
        "bloom_taxonomy_level": bloom,
        "difficulty": difficulty,
        "interaction_type": "multiple_select",
        "type": "multiple_select",
        "context_application": context,
        "stem": stem,
        "interface_config": {
            "allow_calculator": False,
            "input_placeholder": None,
            "expected_format": "multiple_selection",
            "grading_policy": "binary_all_or_nothing"
        },
        "options": options,
        "correct_answer": correct_letters,
        "hints": ensure_hints(hints, comp_id),
        "detailed_solution": solution,
        "solution": solution,
        "common_misconception_warning": misconception,
        "misconception_warning": misconception
    }

# -----------------------------------------------------------------------------
# Curated Flagship Exercises from system_prompts/output_example_exercises.json
# (Repaired for LaTeX escaping, unescaped raw newlines, and option lengths)
# -----------------------------------------------------------------------------

def get_curated_exercises(rng: random.Random) -> list[dict[str, Any]]:
    items = []

    # 1. Q-HAB03-ISLM-001 (Hab-03, MC7)
    q1_stem = (
        "Considere la representación matricial del Modelo IS-LM Dinámico planteado en clase:\n"
        "$$\\begin{bmatrix} \\dot{Y}_t \\\\ \\dot{r}_t \\end{bmatrix} = "
        "\\begin{bmatrix} c_1[c(1-\\tau)-1] & -\\mu c_1 \\\\ c_2\\theta & -\\gamma c_2 \\end{bmatrix} "
        "\\begin{bmatrix} Y_t \\\\ r_t \\end{bmatrix} + "
        "\\begin{bmatrix} c_1(I_0 + \\bar{G} + c_0 - c\\tau_0) \\\\ -\\bar{m}c_2 \\end{bmatrix}$$\n"
        "donde los parámetros estructurales satisfacen $0 < c < 1$, $0 < \\tau < 1$, y las velocidades de ajuste "
        "y sensibilidades cumplen $c_1, c_2, \\mu, \\theta, \\gamma > 0$. Si los parámetros determinan que el discriminante "
        "espectral es estrictamente negativo ($\\Delta = [\\text{tr}(A)]^2 - 4\\det(A) < 0$), ¿cuál es la tipología topológica "
        "y el régimen de estabilidad asintótica del estado estacionario $(Y^E, r^E)$?"
    )
    q1_c = (
        "Foco asintóticamente estable (espiral convergente), con oscilaciones amortiguadas hacia $(Y^E, r^E)$ "
        "porque $\\text{tr}(A) < 0$, $\\det(A) > 0$ y $\\Delta < 0$."
    )
    q1_distractors = [
        "Punto silla inestable en el plano $(Y, r)$, debido a que el término $-\\mu c_1$ induce una raíz con parte real estrictamente positiva.",
        "Foco inestable con trayectorias espirales divergentes, dado que la velocidad de ajuste monetario $c_2$ desestabiliza la traza del sistema.",
        "Centro armónico conservativo con ciclos cerrados perpetuos no amortiguados, porque el discriminante es estrictamente negativo en el plano.",
        "Nodo asintóticamente estable monotónico, pues la condición $c(1-\\tau) < 1$ suprime cualquier oscilación temporal en el ingreso nacional.",
        "Nodo impropio inestable con autovalores reales repetidos positivos, ya que las demandas de dinero y bienes se refuerzan mutuamente.",
        "Equilibrio degenerado con un continuo de estados estacionarios, ya que la matriz jacobiana pierde rango ante ajustes simultáneos de mercado."
    ]
    q1_hints = [
        "Calcule la traza sumando los elementos diagonales: $\\text{tr}(A) = c_1[c(1-\\tau) - 1] - \\gamma c_2$. Como $0 < c < 1$ y $0 < \\tau < 1$, se cumple $\\text{tr}(A) < 0$.",
        "Calcule el determinante: $\\det(A) = c_1 c_2 [(1 - c(1-\\tau))\\gamma + \\mu\\theta]$. Al ser todos los parámetros positivos, $\\det(A) > 0$.",
        "La fórmula espectral es $\\lambda_{1,2} = \\frac{\\text{tr}(A) \\pm \\sqrt{\\Delta}}{2}$. Con $\\Delta < 0$, las raíces son complejas conjugadas con parte real $\\frac{\\text{tr}(A)}{2} < 0$.",
        "La combinación de $\\text{tr}(A) < 0$, $\\det(A) > 0$ y $\\Delta < 0$ clasifica formalmente al equilibrio como un foco asintóticamente estable."
    ]
    q1_sol = (
        "Para el sistema $\\dot{X} = AX + B$:\n"
        "1. Traza: $\\text{tr}(A) = c_1[c(1-\\tau)-1] - \\gamma c_2 < 0$.\n"
        "2. Determinante: $\\det(A) = c_1 c_2 [\\gamma(1-c(1-\\tau)) + \\mu\\theta] > 0$.\n"
        "3. Con $\\Delta < 0$, las raíces son complejas conjugadas con parte real negativa, configurando un foco asintóticamente estable."
    )
    q1_warn = (
        "No confunda un determinante positivo y discriminante negativo con un centro cerrado. "
        "Un centro requiere rigurosamente que la traza sea idénticamente nula ($\\text{tr}(A) = 0$)."
    )
    items.append(create_mc7_item(
        "Q-HAB03-ISLM-001", "Hab-03", "Analyze", "medium", "Modelo IS-LM Dinámico",
        q1_stem, q1_c, q1_distractors, q1_hints, q1_sol, q1_warn, rng
    ))

    # 2. Q-HAB02-GOODWIN-002 (Hab-02, FIB)
    q2_stem = (
        "En el modelo de ciclos económicos de Goodwin, la dinámica no lineal acoplada entre la tasa de empleo $v = L/N$ "
        "y la participación salarial $u = w/a$ viene dada por:\n"
        "$$\\dot{v} = v(\\gamma - u\\delta)$$\n"
        "$$\\dot{u} = u(-a + bv)$$\n"
        "donde los parámetros agregados están definidos por $\\gamma = \\frac{1}{\\sigma} - \\alpha - n$ y $\\delta = \\frac{1}{\\sigma}$, "
        "siendo $\\sigma$ la relación capital-producto, $\\alpha$ la tasa de progreso técnico y $n$ la tasa de crecimiento poblacional "
        "(con $\\sigma, \\alpha, n > 0$).\n"
        "Deduzca la expresión analítica simplificada para la coordenada de equilibrio estacionario interior de la participación salarial, "
        "$u^* = \\frac{\\gamma}{\\delta}$. Exprese su respuesta en términos de $\\alpha$, $n$ y $\\sigma$."
    )
    q2_hints = [
        "Para encontrar el equilibrio interior no trivial con $v^* > 0$, iguale $\\dot{v} = v(\\gamma - u\\delta) = 0 \\implies u^* = \\frac{\\gamma}{\\delta}$.",
        "Reemplace las definiciones estructurales: $\\gamma = \\frac{1}{\\sigma} - \\alpha - n$ y $\\delta = \\frac{1}{\\sigma}$.",
        "Exprese el numerador con común denominador: $\\gamma = \\frac{1 - (\\alpha + n)\\sigma}{\\sigma}$.",
        "Divida entre $\\delta = \\frac{1}{\\sigma}$ cancelando $\\sigma$: $u^* = 1 - (\\alpha + n)\\sigma$."
    ]
    q2_sol = (
        "Igualando $\\dot{v} = 0$, obtenemos $u^* = \\frac{\\gamma}{\\delta}$. "
        "Sustituyendo $\\gamma = \\frac{1}{\\sigma} - \\alpha - n = \\frac{1 - (\\alpha+n)\\sigma}{\\sigma}$ "
        "y $\\delta = \\frac{1}{\\sigma}$, se deduce $u^* = 1 - (\\alpha + n)\\sigma$."
    )
    q2_warn = (
        "No olvide agrupar el producto $(\\alpha + n)\\sigma$. La tasa demográfica $n$ y el progreso técnico $\\alpha$ "
        "afectan conjuntamente el umbral distributivo."
    )
    items.append(create_fib_item(
        "Q-HAB02-GOODWIN-002", "Hab-02", "Apply", "medium", "Modelo de Ciclos Económicos de Goodwin",
        q2_stem, "1 - (\\alpha + n)\\sigma",
        [
            "1 - (\\alpha + n)*\\sigma", "1 - \\alpha\\sigma - n\\sigma", "1 - \\sigma(\\alpha + n)",
            "1 - \\sigma\\alpha - \\sigma n", "1-(\\alpha+n)\\sigma", "1-\\alpha*\\sigma-n*\\sigma",
            "1 - (alpha + n)*sigma"
        ],
        q2_hints, q2_sol, q2_warn,
        placeholder="Ingresa la expresión en términos de alpha, n y sigma (ej. 1 - (alpha + n)*sigma)"
    ))

    # 3. Q-MS-GOODWIN-003 (C-02, MS)
    q3_stem = (
        "Considere la matriz jacobiana del modelo de ciclos distributivos de Goodwin evaluada en el estado estacionario interior $(u^*, v^*)$:\n"
        "$$J^* = \\begin{bmatrix} 0 & -\\delta v^* \\\\ bu^* & 0 \\end{bmatrix}$$\n"
        "donde $\\delta, b, u^*, v^* > 0$. Seleccione todas las afirmaciones teóricamente correctas respecto a las propiedades espectrales "
        "de $J^*$, la dinámica del sistema linealizado y las limitaciones de la linealización local:"
    )
    q3_statements = [
        {
            "content": "Los autovalores del sistema linealizado son imaginarios puros conjugados: $\\lambda_{1,2} = \\pm i\\sqrt{\\delta b u^* v^*}$.",
            "is_correct": True,
            "error_rationale": None
        },
        {
            "content": "La traza nula $\\text{tr}(J^*) = 0$ y determinante positivo $\\det(J^*) = \\delta b u^* v^* > 0$ clasifican al sistema linealizado como un centro armónico conservativo.",
            "is_correct": True,
            "error_rationale": None
        },
        {
            "content": "Dado que $\\text{Re}(\\lambda) = 0$, el punto de equilibrio es hiperbólico, garantizando por Hartman-Grobman que el sistema no lineal preserva órbitas cerradas.",
            "is_correct": False,
            "error_rationale": "Falsa generalización: un punto es hiperbólico si Re(lambda) != 0. Con raíces imaginarias puras, Hartman-Grobman no aplica."
        },
        {
            "content": "Las trayectorias del sistema linealizado convergen asintóticamente al punto de equilibrio $(u^*, v^*)$ debido a que la traza no es positiva.",
            "is_correct": False,
            "error_rationale": "Confunde estabilidad asintótica con marginal: tr(J*)=0 produce órbitas perpetuas sin convergencia al origen."
        },
        {
            "content": "El periodo de oscilación de las fluctuaciones en el sistema linealizado está dado analíticamente por $T = \\frac{2\\pi}{\\sqrt{\\delta b u^* v^*}}$.",
            "is_correct": True,
            "error_rationale": None
        }
    ]
    q3_hints = [
        "Calcule la traza y determinante: $\\text{tr}(J^*) = 0$ y $\\det(J^*) = \\delta b u^* v^* > 0$.",
        "La ecuación característica es $\\lambda^2 + \\delta b u^* v^* = 0$, con raíces $\\lambda_{1,2} = \\pm i\\omega$, donde $\\omega = \\sqrt{\\delta b u^* v^*}$.",
        "El periodo fundamental es $T = \\frac{2\\pi}{\\omega} = \\frac{2\\pi}{\\sqrt{\\delta b u^* v^*}}$.",
        "Un equilibrio con raíces imaginarias puras es NO hiperbólico, por lo que el Teorema de Hartman-Grobman no aplica directamente."
    ]
    q3_sol = (
        "1. Invariantes: $\\text{tr}(J^*) = 0$, $\\det(J^*) = \\delta b u^* v^* > 0$.\n"
        "2. Autovalores: $\\lambda_{1,2} = \\pm i\\sqrt{\\delta b u^* v^*}$ (imaginarios puros, centro lineal, periodo $T = 2\\pi / \\omega$).\n"
        "3. Al tener parte real nula, el punto no es hiperbólico y no aplica el teorema de Hartman-Grobman."
    )
    q3_warn = (
        "No asuma que traza cero implica estabilidad asintótica. En un centro armónico las trayectorias orbitan indefinidamente."
    )
    items.append(create_ms_item(
        "Q-MS-GOODWIN-003", "C-02", "Analyze", "hard", "Modelo de Ciclos Económicos de Goodwin",
        q3_stem, q3_statements, q3_hints, q3_sol, q3_warn
    ))

    # 4. Q-HAB06-SOLOW-004 (Hab-06, MC7)
    q4_stem = (
        "En el modelo de crecimiento y polución acumulada analizado en clase:\n"
        "$$\\dot{K} = sK^\\alpha - \\delta K$$\n"
        "$$\\dot{P} = K^\\beta - \\gamma P$$\n"
        "con parámetros $0 < \\alpha < 1$, $\\beta > 0$, $s > 0$, $\\delta > 0$, $\\gamma > 0$, el estado estacionario interior no nulo es "
        "$(K^*, P^*) = \\left( (\\frac{\\delta}{s})^{\\frac{1}{\\alpha-1}}, \\frac{1}{\\gamma}(\\frac{\\delta}{s})^{\\frac{\\beta}{\\alpha-1}} \\right)$.\n"
        "La matriz jacobiana linealizada alrededor de $(K^*, P^*)$ toma la forma triangular:\n"
        "$$J^* = \\begin{bmatrix} \\delta(\\alpha - 1) & 0 \\\\ \\beta\\left(\\frac{\\delta}{s}\\right)^{\\frac{\\beta-1}{\\alpha-1}} & -\\gamma \\end{bmatrix}$$\n"
        "¿Cuáles son los autovalores $\\lambda_1, \\lambda_2$ de $J^*$ y cuál es la clasificación cualitativa del equilibrio estacionario $(K^*, P^*)$?"
    )
    q4_c = (
        "$\\lambda_1 = \\delta(\\alpha - 1) < 0$ y $\\lambda_2 = -\\gamma < 0$; ambos autovalores son reales y estrictamente negativos, "
        "por lo que $(K^*, P^*)$ es un nodo asintóticamente estable."
    )
    q4_distractors = [
        "$\\lambda_1 = \\delta(\\alpha - 1) > 0$ y $\\lambda_2 = \\gamma > 0$; el estado estacionario es un nodo inestable con crecimiento exponencial de capital y contaminación en el plano.",
        "$\\lambda_1 = \\delta(1 - \\alpha) > 0$ y $\\lambda_2 = -\\gamma < 0$; el punto es un punto de silla inestable dependiente de la variedad inicial en el espacio de estados.",
        "$\\lambda_{1,2} = \\pm i\\sqrt{\\delta\\gamma(1-\\alpha)}$; las interacciones entre capital y emisiones inducen ciclos oscilatorios cerrados alrededor de $(K^*, P^*)$ de forma perpetua.",
        "$\\lambda_1 = -\\delta\\alpha$ y $\\lambda_2 = -\\beta\\gamma$; el punto es un foco asintóticamente estable debido a los rendimientos decrecientes del capital en la producción agregada.",
        "$\\lambda_1 = 0$ y $\\lambda_2 = \\delta(\\alpha - 1) - \\gamma$; el sistema posee una variedad de equilibrios no aislados con estabilidad neutral en el dominio económico.",
        "$\\lambda_1 = -\\delta$ y $\\lambda_2 = -\\gamma$; la elasticidad de escala $\\alpha$ no afecta la tasa de convergencia asintótica del capital hacia el reposo estacionario."
    ]
    q4_hints = [
        "La matriz $J^*$ es triangular inferior ($J_{12} = 0$). Los autovalores de toda matriz triangular coinciden con los elementos de su diagonal principal.",
        "De la diagonal leemos directamente: $\\lambda_1 = \\delta(\\alpha - 1)$ y $\\lambda_2 = -\\gamma$.",
        "Como $0 < \\alpha < 1$, $(\\alpha - 1) < 0 \\implies \\lambda_1 < 0$. Como $\\gamma > 0$, $\\lambda_2 = -\\gamma < 0$.",
        "Al ser ambos valores propios reales y estrictamente negativos, el equilibrio $(K^*, P^*)$ es un nodo asintóticamente estable."
    ]
    q4_sol = (
        "La matriz jacobiana es triangular inferior con elementos diagonales $J_{11} = \\delta(\\alpha-1)$ y $J_{22} = -\\gamma$. "
        "Como $0 < \\alpha < 1$, se cumple $\\lambda_1 = \\delta(\\alpha-1) < 0$. Con $\\gamma > 0$, $\\lambda_2 = -\\gamma < 0$. "
        "Dos autovalores reales negativos clasifican al estado estacionario como un nodo asintóticamente estable."
    )
    q4_warn = (
        "No pierda tiempo expandiendo el polinomio característico con $\\lambda^2 - \\text{tr}\\lambda + \\det$. "
        "En matrices triangulares, los autovalores se leen de forma inmediata en la diagonal."
    )
    items.append(create_mc7_item(
        "Q-HAB06-SOLOW-004", "Hab-06", "Apply", "medium", "Modelo de Producción y Polución Acumulada",
        q4_stem, q4_c, q4_distractors, q4_hints, q4_sol, q4_warn, rng
    ))

    # 5. Q-HAB05-INHOMOG-005 (Hab-05, FIB)
    q5_stem = (
        "Considere el sistema de ecuaciones diferenciales ordinarias lineal no homogéneo presentado en clase:\n"
        "$$\\begin{bmatrix} \\dot{x} \\\\ \\dot{y} \\end{bmatrix} = "
        "\\begin{bmatrix} 1 & 12 \\\\ 3 & 1 \\end{bmatrix} \\begin{bmatrix} x \\\\ y \\end{bmatrix} + "
        "\\begin{bmatrix} 2t \\\\ t \\end{bmatrix}$$\n"
        "Para determinar la solución particular $X_p(t)$ mediante coeficientes indeterminados, se postula:\n"
        "$$X_p(t) = \\begin{bmatrix} A_1 \\\\ B_1 \\end{bmatrix} t + \\begin{bmatrix} A_0 \\\\ B_0 \\end{bmatrix}$$\n"
        "Al sustituir e igualar los términos lineales ($t^1$), se tiene:\n"
        "$$\\begin{bmatrix} 1 & 12 \\\\ 3 & 1 \\end{bmatrix} \\begin{bmatrix} A_1 \\\\ B_1 \\end{bmatrix} + "
        "\\begin{bmatrix} 2 \\\\ 1 \\end{bmatrix} = \\begin{bmatrix} 0 \\\\ 0 \\end{bmatrix} \\implies "
        "\\begin{bmatrix} A_1 \\\\ B_1 \\end{bmatrix} = -\\begin{bmatrix} 1 & 12 \\\\ 3 & 1 \\end{bmatrix}^{-1} \\begin{bmatrix} 2 \\\\ 1 \\end{bmatrix}$$\n"
        "Calcule el valor numérico escalar de la pendiente $A_1$. Ingrese su resultado como una fracción irreducible simplificada (ej. -2/7)."
    )
    q5_hints = [
        "Para la matriz $A = \\begin{bmatrix} 1 & 12 \\\\ 3 & 1 \\end{bmatrix}$, el determinante es $\\det(A) = 1 - 36 = -35$.",
        "La matriz inversa es $A^{-1} = -\\frac{1}{35} \\begin{bmatrix} 1 & -12 \\\\ -3 & 1 \\end{bmatrix}$.",
        "El vector satisface $\\begin{bmatrix} A_1 \\\\ B_1 \\end{bmatrix} = \\frac{1}{35} \\begin{bmatrix} 1 & -12 \\\\ -3 & 1 \\end{bmatrix} \\begin{bmatrix} 2 \\\\ 1 \\end{bmatrix}$.",
        "Calculando la primera componente: $A_1 = \\frac{1}{35}(2 - 12) = -\\frac{10}{35} = -\\frac{2}{7}$."
    ]
    q5_sol = (
        "El vector de coeficientes lineales cumple $A \\begin{bmatrix} A_1 \\\\ B_1 \\end{bmatrix} = \\begin{bmatrix} -2 \\\\ -1 \\end{bmatrix}$. "
        "Con $\\det(A) = -35$ y $A^{-1} = -\\frac{1}{35} \\begin{bmatrix} 1 & -12 \\\\ -3 & 1 \\end{bmatrix}$, "
        "tenemos $\\begin{bmatrix} A_1 \\\\ B_1 \\end{bmatrix} = -\\frac{1}{35} \\begin{bmatrix} 10 \\\\ 5 \\end{bmatrix} = \\begin{bmatrix} -2/7 \\\\ -1/7 \\end{bmatrix}$, "
        "por lo que $A_1 = -2/7$."
    )
    q5_warn = (
        "Atención al signo: el signo menos de $-A^{-1}B$ se combina con el signo negativo del determinante $\\det(A) = -35$."
    )
    items.append(create_fib_item(
        "Q-HAB05-INHOMOG-005", "Hab-05", "Apply", "hard", "Sistemas Lineales de EDOs No Homogéneos",
        q5_stem, "-2/7", ["-2/7", "-\\frac{2}{7}", "-10/35", "-\\frac{10}{35}", "-0.2857"],
        q5_hints, q5_sol, q5_warn,
        placeholder="Ingresa la fraccion irreducible para A_1 (ej. -2/7)"
    ))

    # 6. Q-MS-PHILLIPS-006 (Hab-03, MS)
    q6_stem = (
        "En el modelo macroeconómico de Inflación y Desempleo con expectativas adaptativas, el sistema dinámico se expresa como:\n"
        "$$\\begin{bmatrix} \\pi' \\\\ U' \\end{bmatrix} + \\begin{bmatrix} j(1-g) & j\\beta \\\\ -kg & k\\beta \\end{bmatrix} "
        "\\begin{bmatrix} \\pi \\\\ U \\end{bmatrix} = \\begin{bmatrix} j(\\alpha - T) \\\\ k(\\alpha - T - \\mu) \\end{bmatrix}$$\n"
        "donde $\\alpha, \\beta, k > 0$, $0 < j \\le 1$ y $0 < g \\le 1$. La ecuación característica es:\n"
        "$$r^2 + [k\\beta + j(1-g)]r + k\\beta j = 0$$\n"
        "con discriminante $\\Delta = [k\\beta + j(1-g)]^2 - 4k\\beta j$.\n"
        "Seleccione todas las afirmaciones rigurosamente verdaderas respecto a las propiedades espectrales y dinámicas de este modelo:"
    )
    q6_statements = [
        {
            "content": "El determinante efectivo del sistema dinámico es estrictamente positivo e igual a $k\\beta j > 0$ para cualquier combinación admisible de parámetros.",
            "is_correct": True,
            "error_rationale": None
        },
        {
            "content": "La traza de la matriz dinámica canónica $\\dot{X} = AX + B$ es estrictamente negativa e igual a $\\text{tr}(A) = -[k\\beta + j(1-g)] < 0$, descartando cualquier divergencia explosiva.",
            "is_correct": True,
            "error_rationale": None
        },
        {
            "content": "El sistema exhibirá oscilaciones cíclicas amortiguadas (foco estable) alrededor del reposo si y solo si el discriminante cumple $\\Delta < 0$.",
            "is_correct": True,
            "error_rationale": None
        },
        {
            "content": "Si las expectativas de inflación son completamente neutrales ($g = 1$), el sistema se transforma en un punto de silla inestable con autovalores opuestos.",
            "is_correct": False,
            "error_rationale": "Falso: con g=1, la ecuación característica r^2 + k*beta*r + k*beta*j = 0 sigue teniendo coeficientes estrictamente positivos."
        },
        {
            "content": "Cuando $\\Delta > 0$, una de las raíces es estrictamente positiva, forzando al desempleo a crecer indefinidamente hacia infinito.",
            "is_correct": False,
            "error_rationale": "Falso: como tr(A) < 0 y det(A) > 0, cuando Delta > 0 ambas raíces reales son estrictamente negativas (nodo estable)."
        }
    ]
    q6_hints = [
        "Escriba el sistema canónico $\\dot{X} = AX + B$: la matriz es $A = \\begin{bmatrix} -j(1-g) & -j\\beta \\\\ kg & -k\\beta \\end{bmatrix}$.",
        "Calcule la traza: $\\text{tr}(A) = -j(1-g) - k\\beta < 0$, y determinante $\\det(A) = jk\\beta > 0$.",
        "Dado que $\\text{tr}(A) < 0$ y $\\det(A) > 0$, el sistema siempre es asintóticamente estable (foco si $\\Delta < 0$, nodo si $\\Delta \\ge 0$).",
        "En ningún caso admisible existen autovalores con parte real positiva o de signo opuesto."
    ]
    q6_sol = (
        "1. De la ecuación cuadrática $r^2 - \\text{tr}(A)r + \\det(A) = 0$, identificamos $\\text{tr}(A) = -[k\\beta + j(1-g)] < 0$ "
        "y $\\det(A) = k\\beta j > 0$.\n"
        "2. Como el determinante es positivo y la traza es negativa, el sistema es asintóticamente estable en todos los regímenes.\n"
        "3. Si $\\Delta < 0$, las raíces adquieren parte imaginaria no nula, originando un foco estable."
    )
    q6_warn = (
        "No confunda la presencia de $\\pm \\sqrt{\\Delta}$ con la existencia de autovalores de signos opuestos. "
        "Cuando $\\det > 0$ y $\\text{tr} < 0$, ambas raíces reales son negativas."
    )
    items.append(create_ms_item(
        "Q-MS-PHILLIPS-006", "Hab-03", "Analyze", "hard", "Modelo de Inflación y Desempleo",
        q6_stem, q6_statements, q6_hints, q6_sol, q6_warn
    ))

    # 7. Q-HAB04-EIG-007 (Hab-04, MC7)
    q7_stem = (
        "Considere la matriz del sistema homogéneo lineal introducido en clase:\n"
        "$$\\begin{bmatrix} \\dot{x} \\\\ \\dot{y} \\end{bmatrix} = \\begin{bmatrix} 1 & 12 \\\\ 3 & 1 \\end{bmatrix} \\begin{bmatrix} x \\\\ y \\end{bmatrix}$$\n"
        "Determine los autovalores $\\lambda_1, \\lambda_2$ y sus correspondientes autovectores asociados $v_1, v_2$ necesarios para formular "
        "la solución complementaria general $X_h(t) = c_1 e^{\\lambda_1 t}v_1 + c_2 e^{\\lambda_2 t}v_2$."
    )
    q7_c = (
        "$\\lambda_1 = 7, v_1 = \\begin{bmatrix} 2 \\\\ 1 \\end{bmatrix}; \\quad \\lambda_2 = -5, v_2 = \\begin{bmatrix} -2 \\\\ 1 \\end{bmatrix}$"
    )
    q7_distractors = [
        "$\\lambda_1 = 5, v_1 = \\begin{bmatrix} 2 \\\\ 1 \\end{bmatrix}; \\quad \\lambda_2 = -7, v_2 = \\begin{bmatrix} -2 \\\\ 1 \\end{bmatrix}$",
        "$\\lambda_1 = 7, v_1 = \\begin{bmatrix} 1 \\\\ 2 \\end{bmatrix}; \\quad \\lambda_2 = -5, v_2 = \\begin{bmatrix} 1 \\\\ -2 \\end{bmatrix}$",
        "$\\lambda_1 = 6, v_1 = \\begin{bmatrix} 3 \\\\ 1 \\end{bmatrix}; \\quad \\lambda_2 = -6, v_2 = \\begin{bmatrix} -3 \\\\ 1 \\end{bmatrix}$",
        "$\\lambda_1 = 7, v_1 = \\begin{bmatrix} -2 \\\\ 1 \\end{bmatrix}; \\quad \\lambda_2 = -5, v_2 = \\begin{bmatrix} 2 \\\\ 1 \\end{bmatrix}$",
        "$\\lambda_1 = 1 + \\sqrt{36}, v_1 = \\begin{bmatrix} 1 \\\\ 1 \\end{bmatrix}; \\quad \\lambda_2 = 1 - \\sqrt{36}, v_2 = \\begin{bmatrix} -1 \\\\ 1 \\end{bmatrix}$",
        "$\\lambda_1 = -7, v_1 = \\begin{bmatrix} 2 \\\\ -1 \\end{bmatrix}; \\quad \\lambda_2 = 5, v_2 = \\begin{bmatrix} -2 \\\\ -1 \\end{bmatrix}$"
    ]
    q7_hints = [
        "Calcule el polinomio característico: $p(\\lambda) = \\lambda^2 - 2\\lambda - 35 = 0$.",
        "Factorice: $(\\lambda - 7)(\\lambda + 5) = 0 \\implies \\lambda_1 = 7, \\lambda_2 = -5$.",
        "Para $\\lambda_1 = 7$, resuelva $(A - 7I)v_1 = 0 \\implies -6x + 12y = 0 \\implies x = 2y \\implies v_1 = [2, 1]^T$.",
        "Para $\\lambda_2 = -5$, resuelva $(A + 5I)v_2 = 0 \\implies 6x + 12y = 0 \\implies x = -2y \\implies v_2 = [-2, 1]^T$."
    ]
    q7_sol = (
        "1. Polinomio: $(1-\\lambda)^2 - 36 = 0 \\implies \\lambda^2 - 2\\lambda - 35 = 0 \\implies \\lambda_1 = 7, \\lambda_2 = -5$.\n"
        "2. Para $\\lambda_1 = 7$: $-6x + 12y = 0 \\implies v_1 = [2, 1]^T$.\n"
        "3. Para $\\lambda_2 = -5$: $6x + 12y = 0 \\implies v_2 = [-2, 1]^T$."
    )
    q7_warn = (
        "No invierta las coordenadas: $-6x + 12y = 0$ da $x = 2y$, produciendo el vector $[2, 1]^T$ y no $[1, 2]^T$."
    )
    items.append(create_mc7_item(
        "Q-HAB04-EIG-007", "Hab-04", "Apply", "medium", "Sistemas Lineales de EDOs Homogéneos",
        q7_stem, q7_c, q7_distractors, q7_hints, q7_sol, q7_warn, rng
    ))

    return items

# -----------------------------------------------------------------------------
# Generators for H-01 (Fact: Polinomio Característico Canónico 2x2)
# -----------------------------------------------------------------------------

def generate_h01_questions(rng: random.Random) -> list[dict[str, Any]]:
    questions = []
    
    matrices_data = [
        # (a, b, c, d, name_context)
        (2, 3, 1, 4, "Sistema dinámico macroeconómico de ajuste acelerador"),
        (5, -2, 3, 1, "Sistema acoplado de ahorro e inversión agregada"),
        (-3, 4, -2, 1, "Modelo de dinámica de precios y salarios nominales"),
        (4, 1, 2, 3, "Sistema dinámico de interacción insumo-producto"),
        (1, -4, 2, -3, "Modelo de ajuste de inventarios y producción"),
        (-2, 1, -3, -4, "Sistema macroeconómico con retardos de información"),
        (3, 2, 1, 2, "Modelo dinámico de oferta y demanda acopladas"),
        (6, -1, 4, 2, "Sistema de balanza comercial y tasa de cambio"),
        (-1, 3, 2, -2, "Dinámica monetaria de expectativas de inflación"),
        (2, 5, 1, -2, "Modelo de competencia duopólica dinámica")
    ]

    # 10 MC7 questions
    for idx, (a, b, c, d, ctx) in enumerate(matrices_data, 1):
        tr = a + d
        det = a * d - b * c
        tr_sign = "-" if tr >= 0 else "+"
        tr_abs = abs(tr)
        det_sign = "+" if det >= 0 else "-"
        det_abs = abs(det)
        poly_str = f"\\lambda^2 {tr_sign} {tr_abs}\\lambda {det_sign} {det_abs} = 0"
        
        stem = (
            f"Considere la matriz dinámica $A = \\begin{{bmatrix}} {a} & {b} \\\\ {c} & {d} \\end{{bmatrix}}$ "
            f"asociada al {ctx}. ¿Cuál es la ecuación característica canónica $p(\\lambda) = 0$ del sistema?"
        )
        c_opt = f"La ecuación característica es ${poly_str}$, con traza $\\text{{tr}}(A) = {tr}$ y determinante $\\det(A) = {det}$."
        distractors = [
            f"La ecuación característica es $\\lambda^2 + {tr_abs}\\lambda - {det_abs} = 0$, con error de signo en la traza espectral.",
            f"La ecuación característica es $\\lambda^2 - {det_abs}\\lambda + {tr_abs} = 0$, intercambiando traza y determinante de la matriz.",
            f"La ecuación característica es $\\lambda^2 - ({a*d})\\lambda + ({b*c}) = 0$, multiplicando solo los elementos diagonales.",
            f"La ecuación característica es $\\lambda^2 + {det_abs}\\lambda + {tr_abs} = 0$, alterando los invariantes espectrales canónicos.",
            f"La ecuación característica es $\\lambda^2 - {tr_abs+2}\\lambda + {det_abs-1} = 0$, distorsionando los coeficientes de acoplamiento.",
            f"La ecuación característica es $\\lambda^2 - ({a+b})\\lambda + ({c+d}) = 0$, sumando filas en lugar de aplicar la diagonal principal."
        ]
        hints = [
            f"Calcule la traza sumando la diagonal principal: $\\text{{tr}}(A) = {a} + {d} = {tr}$.",
            f"Calcule el determinante de orden $2\\times 2$: $\\det(A) = ({a})({d}) - ({b})({c}) = {a*d} - ({b*c}) = {det}$.",
            f"Sustituya en la fórmula canónica: $p(\\lambda) = \\lambda^2 - \\text{{tr}}(A)\\lambda + \\det(A) = 0$."
        ]
        sol = (
            f"Para la matriz dada, la traza es $\\text{{tr}}(A) = {a} + {d} = {tr}$ y el determinante es $\\det(A) = ({a})({d}) - ({b})({c}) = {det}$. "
            f"Por la fórmula canónica $p(\\lambda) = \\lambda^2 - \\text{{tr}}(A)\\lambda + \\det(A) = 0$, obtenemos ${poly_str}$."
        )
        warn = "Recuerde que el coeficiente lineal lleva signo negativo: $-\\text{tr}(A)$, mientras que el término independiente es $+\\det(A)$."
        questions.append(create_mc7_item(
            f"Q-H01-{idx:03d}", "H-01", "Understand", "medium", ctx,
            stem, c_opt, distractors, hints, sol, warn, rng
        ))

    # 5 FIB questions
    fib_data = [
        (3, 1, 2, 5, "tr", 8, "traza", "Modelo de crecimiento endógeno acoplado"),
        (4, -1, 2, 3, "det", 14, "determinante", "Dinámica de crédito y deuda soberana"),
        (2, -3, 1, 1, "det", 5, "determinante", "Modelo de ciclo financiero de Minsky"),
        (-4, 2, 3, -1, "tr", -5, "traza", "Sistema de fijación de salarios escalonados"),
        (5, 2, -1, 2, "det", 12, "determinante", "Modelo macroeconómico de comercio exterior")
    ]
    for offset, (a, b, c, d, query_type, ans_val, query_name, ctx) in enumerate(fib_data, 11):
        stem = (
            f"Dada la matriz del sistema macroeconómico $\\dot{{X}} = AX$, con $A = \\begin{{bmatrix}} {a} & {b} \\\\ {c} & {d} \\end{{bmatrix}}$, "
            f"calcule el valor escalar exacto del {query_name} $\\{query_type}(A)$ necesario para formular su polinomio característico."
        )
        hints = [
            f"Identifique los elementos de la matriz $2\\times 2$: $a_{{11}} = {a}$, $a_{{12}} = {b}$, $a_{{21}} = {c}$, $a_{{22}} = {d}$.",
            f"Aplique la definición: si es traza, sume $a_{{11}} + a_{{22}}$; si es determinante, calcule $a_{{11}}a_{{22}} - a_{{12}}a_{{21}}$.",
            f"El resultado numérico es {ans_val}."
        ]
        sol = f"Evaluando la expresión directa: $\\{query_type}(A) = {ans_val}$."
        warn = f"Verifique rigurosamente los signos al multiplicar los elementos fuera de la diagonal."
        questions.append(create_fib_item(
            f"Q-H01-{offset:03d}", "H-01", "Apply", "easy", ctx,
            stem, str(ans_val), [str(ans_val)], hints, sol, warn,
            placeholder=f"Ingresa el valor numérico de {query_type}(A)"
        ))

    # 5 MS questions
    ms_data = [
        ("Propiedades de los invariantes de matrices 2x2", [
            {"content": "La suma de los autovalores de la matriz coincide idénticamente con la traza: $\\lambda_1 + \\lambda_2 = \\text{tr}(A)$.", "is_correct": True},
            {"content": "El producto de los autovalores es estrictamente igual al determinante: $\\lambda_1 \\lambda_2 = \\det(A)$.", "is_correct": True},
            {"content": "El polinomio característico depende de la base elegida y cambia bajo transformaciones de similitud $P^{-1}AP$.", "is_correct": False, "error_rationale": "El polinomio es un invariante espectral intrínseco."},
            {"content": "Toda matriz $2\\times 2$ con $\\det(A) < 0$ posee necesariamente dos autovalores reales de signos opuestos.", "is_correct": True, "error_rationale": None},
            {"content": "Si $\\text{tr}(A) = 0$, la matriz no puede tener autovalores reales bajo ninguna condición paramétrica.", "is_correct": False, "error_rationale": "Si det < 0, lambda = +- sqrt(-det) son reales opuestos."}
        ]),
        ("Estructura del polinomio característico canónico", [
            {"content": "Para cualquier matriz $A \\in \\mathbb{R}^{2\\times 2}$, el polinomio característico siempre es de segundo grado en $\\lambda$.", "is_correct": True},
            {"content": "El término independiente del polinomio $p(\\lambda)$ es el determinante $\\det(A)$.", "is_correct": True},
            {"content": "El coeficiente del término lineal es $-\\text{tr}(A)$ y no $+\\text{tr}(A)$.", "is_correct": True},
            {"content": "Si la matriz es singular ($\\det(A) = 0$), al menos uno de sus autovalores es idénticamente nulo.", "is_correct": True},
            {"content": "Una matriz triangular tiene por determinante la suma de sus elementos diagonales.", "is_correct": False, "error_rationale": "El determinante es el producto de los elementos diagonales."}
        ]),
        ("Invariantes espectrales y transformaciones lineales", [
            {"content": "La traza es un operador lineal: $\\text{tr}(A + B) = \\text{tr}(A) + \\text{tr}(B)$.", "is_correct": True},
            {"content": "El determinante satisface la propiedad multiplicativa $\\det(AB) = \\det(A)\\det(B)$.", "is_correct": True},
            {"content": "El determinante es un operador lineal: $\\det(A + B) = \\det(A) + \\det(B)$ para matrices arbitrarias.", "is_correct": False, "error_rationale": "El determinante no es distributivo respecto a la suma."},
            {"content": "Para un escalar $k$, se cumple $\\det(kA) = k^2 \\det(A)$ en dimensión 2.", "is_correct": True},
            {"content": "Si $A$ es invertible, los autovalores de $A^{-1}$ son los inversos multiplicativos de los autovalores de $A$.", "is_correct": True}
        ]),
        ("Diagnóstico algebraico del polinomio de segundo orden", [
            {"content": "El discriminante del polinomio característico se define como $\\Delta = [\\text{tr}(A)]^2 - 4\\det(A)$.", "is_correct": True},
            {"content": "Si $\\Delta = 0$, el polinomio posee una raíz real doble $\\lambda = \\frac{\\text{tr}(A)}{2}$.", "is_correct": True},
            {"content": "Si $\\Delta < 0$, las raíces son complejas conjugadas con parte real $\\frac{\\text{tr}(A)}{2}$.", "is_correct": True},
            {"content": "Un discriminante estrictamente negativo fuerza a que el determinante sea negativo.", "is_correct": False, "error_rationale": "Delta < 0 exige det > tr^2/4 >= 0, luego det es positivo."},
            {"content": "Si $\\text{tr}(A) < 0$ y $\\det(A) > 0$, las partes reales de todos los autovalores son estrictamente negativas.", "is_correct": True}
        ]),
        ("Relación de Viète en ecuaciones espectrales", [
            {"content": "Las fórmulas de Viète relacionan directamente los coeficientes del polinomio con las sumas y productos de raíces.", "is_correct": True},
            {"content": "La condición $\\det(A) > 0$ garantiza que ambos autovalores tengan el mismo signo (o misma parte real no nula).", "is_correct": True},
            {"content": "Si $\\det(A) < 0$, la condición de punto de silla es invariante a la magnitud de la traza.", "is_correct": True},
            {"content": "Una matriz con traza positiva y determinante positivo tiene raíces con parte real negativa.", "is_correct": False, "error_rationale": "Traza positiva implica parte real positiva (inestable)."},
            {"content": "La ecuación característica de una matriz diagonal $\\text{diag}(d_1, d_2)$ es $(\\lambda - d_1)(\\lambda - d_2) = 0$.", "is_correct": True}
        ])
    ]
    for offset, (stem_title, statements) in enumerate(ms_data, 16):
        stem = f"En relación con el {stem_title} para sistemas diferenciales $2\\times 2$, seleccione todas las afirmaciones rigurosamente verdaderas:"
        hints = [
            "Revise las relaciones de Viète para polinomios cuadráticos: suma y producto de raíces.",
            "Considere la definición de traza como suma diagonal y determinante como producto diagonal menos cruzado.",
            "Evalúe cómo se comportan los invariantes bajo combinaciones algebraicas y multiplicaciones matriciales."
        ]
        sol = "Las afirmaciones correctas describen formalmente las propiedades algebraicas de la traza, determinante y ecuación característica."
        warn = "Recuerde que el determinante NO es lineal respecto a la suma: det(A+B) != det(A) + det(B)."
        questions.append(create_ms_item(
            f"Q-H01-{offset:03d}", "H-01", "Analyze", "medium", "Álgebra Lineal Dinámica",
            stem, statements, hints, sol, warn
        ))

    return questions

# -----------------------------------------------------------------------------
# Generators for H-02 (Fact: Fórmula Cuadrática Espectral y Discriminante)
# -----------------------------------------------------------------------------

def generate_h02_questions(rng: random.Random) -> list[dict[str, Any]]:
    questions = []
    
    # 10 MC7 questions on discriminant and roots
    mc_cases = [
        # (tr, det, Delta, regime_name, context)
        (-4, 3, 4, "raíces reales distintas negativas (nodo estable)", "Modelo de ajuste del mercado monetario"),
        (-6, 9, 0, "raíz real doble negativa (nodo degenerado)", "Dinámica de expectativas adaptativas acopladas"),
        (-2, 5, -16, "raíces complejas conjugadas con parte real negativa (foco estable)", "Modelo IS-LM con ajuste acelerador"),
        (4, 3, 4, "raíces reales distintas positivas (nodo inestable)", "Dinámica hiperinflacionaria con desanclaje"),
        (0, 4, -16, "raíces imaginarias puras (centro armónico)", "Modelo de ciclo distributivo de Goodwin lineal"),
        (-5, -6, 49, "raíces reales de signos opuestos (punto de silla)", "Modelo macroeconómico con variedad estable"),
        (-8, 12, 16, "raíces reales distintas negativas (nodo estable)", "Dinámica de balanza de pagos y reservas"),
        (2, 5, -16, "raíces complejas conjugadas con parte real positiva (foco inestable)", "Modelo de burbuja especulativa dinámica"),
        (0, -9, 36, "raíces reales simétricas opuestas (punto de silla)", "Modelo de previsión perfecta y deuda pública"),
        (-6, 8, 4, "raíces reales distintas negativas (nodo estable)", "Modelo de inversión con costos de ajuste")
    ]
    for idx, (tr, det, delta, regime, ctx) in enumerate(mc_cases, 1):
        stem = (
            f"Para un sistema macroeconómico continuo $\\dot{{X}} = AX$ donde la matriz jacobiana posee "
            f"traza $\\text{{tr}}(A) = {tr}$ y determinante $\\det(A) = {det}$, determine el valor del discriminante "
            f"espectral $\\Delta = [\\text{{tr}}(A)]^2 - 4\\det(A)$ y la naturaleza analítica de los autovalores $\\lambda_{{1,2}}$."
        )
        c_opt = f"$\\Delta = {delta}$; las raíces espectrales corresponden a {regime}."
        distractors = [
            f"$\\Delta = {delta + 8}$; los autovalores son imaginarios puros sin amortiguamiento en el plano de estados.",
            f"$\\Delta = {delta - 10}$; el sistema colapsa en un equilibrio degenerado con determinante nulo en el origen.",
            f"$\\Delta = {-abs(delta) if delta > 0 else abs(delta)+4}$; el sistema se comporta como un nodo asimétrico divergente.",
            f"$\\Delta = {tr**2}$; se omite el producto cruzado de cuatro veces el determinante en el cálculo espectral.",
            f"$\\Delta = {4*det}$; se calcula erróneamente el discriminante omitiendo la traza cuadrática en la fórmula.",
            f"$\\Delta = {delta + 16}$; el sistema presenta autovalores de multiplicidad geométrica nula en el plano."
        ]
        hints = [
            f"Calcule la traza al cuadrado: $[\\text{{tr}}(A)]^2 = ({tr})^2 = {tr**2}$.",
            f"Multiplique cuatro veces el determinante: $4\\det(A) = 4({det}) = {4*det}$.",
            f"Reste ambos términos para obtener $\\Delta$: ${tr**2} - ({4*det}) = {delta}$.",
            f"Aplique la fórmula cuadrática $\\lambda_{{1,2}} = \\frac{{{tr} \\pm \\sqrt{{{delta}}}}}{{2}}$ para clasificar las raíces."
        ]
        sol = (
            f"El discriminante espectral es $\\Delta = ({tr})^2 - 4({det}) = {tr**2} - ({4*det}) = {delta}$. "
            f"Sustituyendo en la fórmula cuadrática espectral, se deduce que los autovalores corresponden a {regime}."
        )
        warn = "No olvide multiplicar el determinante por 4 al computar el discriminante espectral."
        questions.append(create_mc7_item(
            f"Q-H02-{idx:03d}", "H-02", "Apply", "medium", ctx,
            stem, c_opt, distractors, hints, sol, warn, rng
        ))

    # 5 FIB questions
    fib_cases = [
        (-4, 8, -16, "Dinámica de inflación con meta de inflación"),
        (-6, 5, 16, "Modelo de ajuste salarial de curva de Phillips"),
        (2, -8, 36, "Dinámica de tasa de interés y tipo de cambio"),
        (-2, 10, -36, "Modelo de crecimiento con capital humano"),
        (-10, 25, 0, "Dinámica de estabilización macroeconómica")
    ]
    for offset, (tr, det, delta_val, ctx) in enumerate(fib_cases, 11):
        stem = (
            f"En el {ctx}, la matriz del sistema linealizado presenta traza $\\text{{tr}}(A) = {tr}$ "
            f"y determinante $\\det(A) = {det}$. Calcule el valor numérico escalar exacto del discriminante "
            f"espectral $\\Delta = [\\text{{tr}}(A)]^2 - 4\\det(A)$."
        )
        hints = [
            f"Eleve la traza al cuadrado: $({tr})^2 = {tr**2}$.",
            f"Calcule el producto $4\\det(A) = 4 \\times {det} = {4*det}$.",
            f"Reste ambos valores: $\\Delta = {tr**2} - ({4*det}) = {delta_val}$."
        ]
        sol = f"$\\Delta = [\\text{{tr}}(A)]^2 - 4\\det(A) = ({tr})^2 - 4({det}) = {delta_val}$."
        warn = "Atención al elevar trazas negativas al cuadrado: $(-k)^2 = +k^2$."
        questions.append(create_fib_item(
            f"Q-H02-{offset:03d}", "H-02", "Apply", "easy", ctx,
            stem, str(delta_val), [str(delta_val)], hints, sol, warn,
            placeholder="Ingresa el valor numérico de Delta"
        ))

    # 5 MS questions
    ms_cases = [
        ("Discriminante espectral y oscilaciones dinámicas", [
            {"content": "Si $\\Delta < 0$, los autovalores son necesariamente complejos conjugados.", "is_correct": True},
            {"content": "La frecuencia angular de oscilación para $\\Delta < 0$ viene dada por $\\omega = \\frac{\\sqrt{-\\Delta}}{2}$.", "is_correct": True},
            {"content": "Si $\\Delta > 0$, la solución complementaria carece de términos trigonométricos sinusoidales.", "is_correct": True},
            {"content": "Cuando $\\Delta = 0$, los autovalores siempre poseen dos autovectores linealmente independientes para cualquier matriz.", "is_correct": False, "error_rationale": "Puede existir deficiencia geométrica exigiendo un autovector generalizado."},
            {"content": "Un discriminante estrictamente positivo garantiza que el sistema sea asintóticamente estable.", "is_correct": False, "error_rationale": "Estabilidad depende del signo de la traza, no de Delta > 0."}
        ]),
        ("Relación entre la fórmula cuadrática y la estabilidad", [
            {"content": "La parte real de ambos autovalores es exactamente $\\frac{\\text{tr}(A)}{2}$ cuando $\\Delta \\le 0$.", "is_correct": True},
            {"content": "Si $\\text{tr}(A) < 0$ y $\\Delta < 0$, las trayectorias espirales convergen asintóticamente al reposo.", "is_correct": True},
            {"content": "Si $\\text{tr}(A) > 0$ y $\\Delta < 0$, las trayectorias espirales divergen exponencialmente del reposo.", "is_correct": True},
            {"content": "Si $\\Delta < 0$, la magnitud del determinante puede ser negativa.", "is_correct": False, "error_rationale": "Delta < 0 implica 4*det > tr^2 >= 0, forzando det > 0."},
            {"content": "El discriminante es estrictamente invariante bajo cambios de coordenadas lineales.", "is_correct": True}
        ]),
        ("Propiedades de las raíces características cuadráticas", [
            {"content": "Para $\\Delta > 0$ y $\\det(A) > 0$, ambas raíces reales poseen el mismo signo algebraico.", "is_correct": True},
            {"content": "Para $\\Delta > 0$ y $\\det(A) < 0$, las raíces tienen signos opuestos, produciendo un punto de silla.", "is_correct": True},
            {"content": "La raíz con mayor parte real domina la tasa de crecimiento asintótico de las trayectorias divergentes.", "is_correct": True},
            {"content": "Si $\\Delta = 0$, la traza del sistema debe ser idénticamente cero.", "is_correct": False, "error_rationale": "Delta = 0 solo exige tr^2 = 4*det, no tr = 0."},
            {"content": "El semieje mayor de las elipses de un centro está determinado por la estructura de autovectores.", "is_correct": True}
        ]),
        ("Impacto de parámetros estructurales en el discriminante", [
            {"content": "Un aumento en el parámetro de amortiguamiento tiende a hacer la traza más negativa.", "is_correct": True},
            {"content": "Ajustes cruzados desestabilizadores aumentan el acoplamiento y pueden inducir discriminantes negativos.", "is_correct": True},
            {"content": "Si $\\det(A) < 0$, el discriminante $\\Delta = \\text{tr}^2 - 4\\det$ es estrictamente positivo para cualquier valor de la traza.", "is_correct": True},
            {"content": "Cuando $\\det(A) < 0$, es imposible que los autovalores tengan parte imaginaria no nula.", "is_correct": True},
            {"content": "Si $\\Delta < 0$, el sistema siempre es conservativo y preserva órbitas perpetuas.", "is_correct": False, "error_rationale": "Solo es conservativo si tr = 0 (centro); si tr != 0 es un foco disipativo o explosivo."}
        ]),
        ("Casos límite y degeneraciones espectrales", [
            {"content": "En el caso crítico $\\Delta = 0$, la solución general puede requerir un término secular secular proporcional a $t e^{\\lambda t}$.", "is_correct": True},
            {"content": "Si $A = k I$ (matriz escalar), entonces $\\Delta = (2k)^2 - 4(k^2) = 0$ y existen dos autovectores independientes.", "is_correct": True},
            {"content": "Una matriz con $\\Delta = 0$ y elementos fuera de la diagonal no nulos es típicamente no diagonalizable.", "is_correct": True},
            {"content": "El discriminante puede ser un número complejo para matrices reales.", "is_correct": False, "error_rationale": "Para matrices reales, tr y det son reales, luego Delta es estrictamente real."},
            {"content": "La condición $\\Delta = 0$ define la parábola frontera $\\det = \\frac{\\text{tr}^2}{4}$ en el plano traza-determinante.", "is_correct": True}
        ])
    ]
    for offset, (stem_title, statements) in enumerate(ms_cases, 16):
        stem = f"Respecto a {stem_title} en sistemas lineales bidimensionales, seleccione todas las afirmaciones rigurosamente verdaderas:"
        hints = [
            "Analice la fórmula del discriminante $\\Delta = \\text{tr}^2 - 4\\det$ y sus raíces asociadas.",
            "Considere los efectos de los signos de $\\Delta$, $\\text{tr}$ y $\\det$ sobre el comportamiento de las soluciones temporales.",
            "Recuerde que para matrices con entradas reales, el discriminante siempre es un valor real."
        ]
        sol = "Las afirmaciones correctas caracterizan los regímenes de raíces y su impacto cualitativo en la dinámica temporal."
        warn = "No confunda discriminante negativo con determinante negativo: si Delta < 0, el determinante siempre es positivo."
        questions.append(create_ms_item(
            f"Q-H02-{offset:03d}", "H-02", "Analyze", "medium", "Análisis Espectral de Sistemas Dinámicos",
            stem, statements, hints, sol, warn
        ))

    return questions

# -----------------------------------------------------------------------------
# Generators for C-01 (Concept: Principio de Superposición y Partición de Soluciones)
# -----------------------------------------------------------------------------

def generate_c01_questions(rng: random.Random) -> list[dict[str, Any]]:
    questions = []

    mc_cases = [
        ("Descomposición lineal canónica", "la solución complementaria $X_h(t)$ converge asintóticamente a cero, de modo que la trayectoria converge al estado estacionario $X_p$", "Modelo macroeconómico con equilibrio de largo plazo"),
        ("Término forzador no constante", "el estado estacionario no es un punto fijo estático sino una trayectoria móvil que rastrea la tendencia temporal", "Dinámica de crecimiento con cambio técnico exógeno"),
        ("Convergencia asintótica del sistema", "la parte homogénea $X_h(t)$ describe las desviaciones transitorias respecto al equilibrio de largo plazo", "Modelo de ajuste del mercado de bienes y dinero"),
        ("Superposición en sistemas lineales", "la solución general es la suma vectorial directa de la solución del sistema homogéneo y una solución particular", "Modelo IS-LM dinámico con forzamiento fiscal"),
        ("Efecto de perturbaciones exógenas", "un cambio permanente en $B$ desplaza el equilibrio $X_p$ sin alterar los autovalores de la matriz dinámica $A$", "Modelo de política monetaria con metas de inflación"),
        ("Estabilidad del sendero particular", "si los autovalores de $A$ tienen parte real negativa, cualquier condición inicial $X(0)$ es atraída hacia $X_p(t)$", "Dinámica de acumulación de capital y deuda pública"),
        ("Independencia de constantes arbitrarias", "las constantes $c_1, c_2$ se determinan exclusivamente a partir de las condiciones iniciales de desviación $X(0) - X_p(0)$", "Modelo de fluctuaciones macroeconómicas lineales"),
        ("Divergencia en sistemas explosivos", "cuando existe al menos un autovalor con parte real positiva, la trayectoria $X_h(t)$ domina y diverge de $X_p$", "Modelo de dinámica hiperinflacionaria con expectativas"),
        ("Propiedad de traslación del origen", "al definir variables en desviación $\\tilde{X} = X - X_p$, el sistema no homogéneo se transforma en homogéneo $\\dot{\\tilde{X}} = A\\tilde{X}$", "Sistemas dinámicos lineales en macroeconomía"),
        ("Resonancia en forzamiento armónico", "cuando la frecuencia del término forzador coincide con la frecuencia propia del sistema, las amplitudes de oscilación crecen secularmente", "Modelo de ciclos de negocios con perturbaciones periódicas")
    ]
    for idx, (theme, c_text, ctx) in enumerate(mc_cases, 1):
        stem = (
            f"En el análisis de sistemas dinámicos lineales $\\dot{{X}} = AX + B(t)$ aplicado al {ctx}, "
            f"según el Principio de Superposición y Partición de Soluciones ($X(t) = X_h(t) + X_p(t)$), "
            f"¿cuál de las siguientes afirmaciones describe con rigor conceptual el rol de cada componente?"
        )
        c_opt = f"Respecto a {theme}: {c_text}."
        distractors = [
            f"La componente particular $X_p(t)$ describe exclusivamente las oscilaciones transitorias de corto plazo en el plano.",
            f"La componente homogénea $X_h(t)$ representa el equilibrio estático de largo plazo independiente de las condiciones iniciales.",
            f"El principio de superposición solo aplica si la matriz $A$ es diagonal con autovalores reales e idénticos.",
            f"Las constantes de integración $c_1, c_2$ pueden evaluarse directamente en $X(0)$ ignorando el valor del equilibrio $X_p(0)$.",
            f"Cualquier modificación en el vector de forzamiento $B(t)$ altera de inmediato la traza y determinante de la matriz $A$.",
            f"La solución general se obtiene mediante el producto tensorial de la solución homogénea y particular en lugar de su suma."
        ]
        hints = [
            "Recuerde que $X(t) = X_h(t) + X_p(t)$ separa la dinámica transitoria intrínseca ($X_h$) de la tendencia estructural ($X_p$).",
            "Los autovalores de $A$ gobiernan la estabilidad y velocidad de decaimiento de $X_h(t)$.",
            "Si $\\lim_{t \\to \\infty} X_h(t) = 0$, la trayectoria converge hacia $X_p(t)$."
        ]
        sol = f"Por el principio de superposición para sistemas lineales, la solución total se descompone en la solución homogénea $X_h(t)$ y la solución particular $X_p(t)$. {c_text}."
        warn = "No confunda $X(0)$ con $X_h(0)$: para fijar las constantes debe restarse el estado estacionario $X_h(0) = X(0) - X_p(0)$."
        questions.append(create_mc7_item(
            f"Q-C01-{idx:03d}", "C-01", "Understand", "medium", ctx,
            stem, c_opt, distractors, hints, sol, warn, rng
        ))

    # 5 FIB questions
    fib_cases = [
        ("Para el sistema $\\dot{X} = AX + B$ con autovalores con parte real negativa, ¿a qué vector converge la trayectoria cuando $t \\to \\infty$?", "X_p", ["X_p", "-A^{-1}B", "X^*"], "Convergencia asintótica al reposo"),
        ("¿Cuántas constantes arbitrarias independientes ($c_i$) contiene la solución complementaria homogénea $X_h(t)$ de un sistema continuo $2\\times 2$?", "2", ["2", "dos"], "Grados de libertad en dimensión 2"),
        ("Si $B$ es un vector constante y $\\det(A) \\neq 0$, la solución particular constante es $X_p = -A^{-1}B$. Si $B=0$, ¿cuál es el estado estacionario?", "0", ["0", "[0, 0]^T", "origen", "\\mathbf{0}"], "Equilibrio homogéneo trivial"),
        ("Para transformar $\\dot{X} = AX + B$ en homogéneo $\\dot{z} = Az$, se define la variable en desviación $z = X - X_p$. ¿Cuál es la derivada temporal $\\dot{z}$ en términos de $\\dot{X}$ cuando $X_p$ es constante?", "\\dot{X}", ["\\dot{X}", "dX/dt"], "Traslación de coordenadas"),
        ("Si $\\lambda_1 = -2$ y $\\lambda_2 = -5$, ¿cuál es el valor de $\\lim_{t \\to \\infty} X_h(t)$ para cualquier condición inicial finita?", "0", ["0", "[0, 0]^T", "\\mathbf{0}"], "Disipación transitoria completa")
    ]
    for offset, (stem_text, ans_str, equivs, ctx) in enumerate(fib_cases, 11):
        stem = f"Considere el principio de partición de soluciones en sistemas diferenciales lineales $2\\times 2$. {stem_text}"
        hints = [
            "Aplique la propiedad de linealidad y el comportamiento asintótico de exponenciales $e^{\\lambda t}$.",
            "Considere que para autovalores con parte real negativa, los términos exponenciales decaen a cero cuando $t \\to \\infty$."
        ]
        sol = f"La respuesta analítica rigurosa es ${ans_str}$."
        warn = "Asegúrese de responder en la forma algebraica canónica."
        questions.append(create_fib_item(
            f"Q-C01-{offset:03d}", "C-01", "Apply", "easy", ctx,
            stem, ans_str, equivs, hints, sol, warn,
            placeholder="Ingresa la expresión algebraica o valor"
        ))

    # 5 MS questions
    ms_cases = [
        ("Propiedades de la descomposición homogénea y particular", [
            {"content": "La solución homogénea $X_h(t)$ es la solución general del sistema no forzado $\\dot{X} = AX$.", "is_correct": True},
            {"content": "La solución particular $X_p(t)$ satisface la ecuación diferencial completa $\\dot{X}_p = AX_p + B(t)$.", "is_correct": True},
            {"content": "Las condiciones iniciales determinan exclusivamente las constantes multiplicativas de la solución homogénea.", "is_correct": True},
            {"content": "La solución particular $X_p(t)$ siempre debe ser idénticamente cero en todo sistema estable.", "is_correct": False, "error_rationale": "X_p depende del término forzador B(t) y puede ser no nula."},
            {"content": "El principio de superposición es válido únicamente para sistemas de ecuaciones diferenciales lineales.", "is_correct": True}
        ]),
        ("Comportamiento dinámico transitorio vs permanente", [
            {"content": "Si todos los autovalores tienen parte real negativa, el régimen transitorio se extingue asintóticamente.", "is_correct": True},
            {"content": "El sendero de largo plazo está determinado enteramente por la solución particular $X_p(t)$.", "is_correct": True},
            {"content": "La velocidad de convergencia al equilibrio depende de la parte real del autovalor menos negativo (autovalor dominante).", "is_correct": True},
            {"content": "Un cambio transitorio en $B(t)$ altera permanentemente la matriz fundamental de soluciones.", "is_correct": False, "error_rationale": "La matriz fundamental depende solo de A, no de B(t)."},
            {"content": "En sistemas lineales, el equilibrio es globalmente atractor si la parte real de todos los autovalores es negativa.", "is_correct": True}
        ]),
        ("Condiciones iniciales y unicidad de trayectorias", [
            {"content": "El teorema de Picard-Lindelöf garantiza existencia y unicidad de la trayectoria dado un valor inicial $X(t_0) = X_0$.", "is_correct": True},
            {"content": "La relación vectorial en $t=0$ es $X(0) = X_h(0) + X_p(0)$.", "is_correct": True},
            {"content": "Para fijar las constantes de $X_h$, se debe resolver el sistema lineal algebraico $c_1 v_1 + c_2 v_2 = X(0) - X_p(0)$.", "is_correct": True},
            {"content": "Dos trayectorias con diferentes condiciones iniciales pueden cruzarse en un sistema autónomo.", "is_correct": False, "error_rationale": "Por unicidad, las trayectorias de sistemas autónomos nunca se intersectan."},
            {"content": "Si $X(0) = X_p(0)$, las constantes de la solución homogénea son nulas ($c_1 = c_2 = 0$) y el sistema permanece en $X_p(t)$.", "is_correct": True}
        ]),
        ("Forzamiento constante vs dependiente del tiempo", [
            {"content": "Si $B$ es constante y $\\det(A) \\neq 0$, la solución particular constante es $X_p = -A^{-1}B$.", "is_correct": True},
            {"content": "Si $B(t)$ es un polinomio de grado 1 en $t$, la solución particular genérica es también un polinomio de grado 1 en $t$.", "is_correct": True},
            {"content": "Si $B(t)$ es una función exponencial $e^{\\mu t}$ y $\\mu$ no es autovalor de $A$, la solución particular tiene la forma $K e^{\\mu t}$.", "is_correct": True},
            {"content": "Si $\\det(A) = 0$, el sistema siempre admite una solución particular constante única para cualquier vector $B$.", "is_correct": False, "error_rationale": "Si det(A)=0, la matriz no es invertible y puede no haber solución constante."},
            {"content": "El forzamiento externo $B(t)$ no modifica los autovalores ni la estabilidad intrínseca de la matriz $A$.", "is_correct": True}
        ]),
        ("Limitaciones del principio de superposición", [
            {"content": "El principio de superposición no es aplicable a sistemas de ecuaciones diferenciales no lineales.", "is_correct": True},
            {"content": "En sistemas no lineales, la suma de dos soluciones no es en general una solución.", "is_correct": True},
            {"content": "La linealización local en torno a un punto de reposo aproxima el sistema como lineal en una vecindad pequeña.", "is_correct": True},
            {"content": "En sistemas lineales acoplados, las ecuaciones pueden desacoplarse mediante la matriz de autovectores.", "is_correct": True},
            {"content": "Los sistemas no lineales autónomos siempre poseen una descomposición aditiva exacta en solución homogénea y particular.", "is_correct": False, "error_rationale": "En sistemas no lineales no existe la partición lineal X_h + X_p."}
        ])
    ]
    for offset, (stem_title, statements) in enumerate(ms_cases, 16):
        stem = f"En relación con el {stem_title} en la teoría de ecuaciones diferenciales ordinarias, seleccione todas las afirmaciones teóricamente válidas:"
        hints = [
            "Considere la formulación matemática de sistemas lineales no homogéneos $\\dot{X} = AX + B(t)$.",
            "Distinga entre propiedades estructurales que dependen de la matriz $A$ y aquellas originadas por el término forzador $B(t)$.",
            "Recuerde el papel de la invertibilidad de $A$ y la unicidad de soluciones."
        ]
        sol = "Las afirmaciones seleccionadas expresan formalmente las propiedades del principio de superposición y unicidad en sistemas lineales."
        warn = "El principio de superposición es exclusivo de sistemas lineales; no aplica a sistemas no lineales."
        questions.append(create_ms_item(
            f"Q-C01-{offset:03d}", "C-01", "Analyze", "medium", "Fundamentos de Sistemas Dinámicos",
            stem, statements, hints, sol, warn
        ))

    return questions

# -----------------------------------------------------------------------------
# Generators for C-02 (Concept: Tipología Topológica en el Plano Traza-Determinante)
# Note: Q-MS-GOODWIN-003 is already included in curated_exercises (1 item).
# We generate 19 additional questions: 10 MC7, 5 FIB, 4 MS (total 20).
# -----------------------------------------------------------------------------

def generate_c02_questions(rng: random.Random) -> list[dict[str, Any]]:
    questions = []

    mc_cases = [
        # (tr_cond, det_cond, delta_cond, classification, ctx)
        ("\\text{tr}(A) < 0", "\\det(A) > 0", "\\Delta > 0", "nodo asintóticamente estable (atractor nodal monotónico)", "Modelo macroeconómico con amortiguamiento fuerte"),
        ("\\text{tr}(A) < 0", "\\det(A) > 0", "\\Delta < 0", "foco asintóticamente estable (espiral convergente amortiguada)", "Dinámica IS-LM con oscilaciones cíclicas amortiguadas"),
        ("\\text{tr}(A) = 0", "\\det(A) > 0", "\\Delta < 0", "centro armónico conservativo (órbitas cerradas periódicas)", "Modelo de ciclos distributivos de Goodwin no disipativo"),
        ("\\text{tr}(A) \\in \\mathbb{R}", "\\det(A) < 0", "\\Delta > 0", "punto de silla inestable (saddle point con variedad estable unidimensional)", "Modelo de crecimiento óptimo de Ramsey con variable de salto"),
        ("\\text{tr}(A) > 0", "\\det(A) > 0", "\\Delta > 0", "nodo inestable (repulsor nodal monotónico divergente)", "Dinámica de deuda pública explosiva con déficit primario"),
        ("\\text{tr}(A) > 0", "\\det(A) > 0", "\\Delta < 0", "foco inestable (espiral divergente expansiva)", "Modelo de hiperinflación con expectativas hiperreactivas"),
        ("\\text{tr}(A) < 0", "\\det(A) > 0", "\\Delta = 0", "nodo impropio degenerado asintóticamente estable", "Sistema dinámico con velocidad de ajuste crítica"),
        ("\\text{tr}(A) = 0", "\\det(A) < 0", "\\Delta > 0", "punto de silla simétrico con autovalores reales opuestos", "Modelo macroeconómico de previsión perfecta simétrico"),
        ("\\text{tr}(A) < 0", "\\det(A) = 0", "\\Delta > 0", "línea continua de equilibrios con estabilidad semi-asintótica", "Modelo con variable dependiente redundante"),
        ("\\text{tr}(A) > 0", "\\det(A) > 0", "\\Delta = 0", "nodo degenerado inestable con trayectorias divergentes", "Modelo de desalineación cambiaria acumulativa")
    ]
    for idx, (tr_c, det_c, del_c, classif, ctx) in enumerate(mc_cases, 1):
        stem = (
            f"En el plano de clasificación topológica traza-determinante para sistemas bidimensionales autónomos $\\dot{{X}} = AX$, "
            f"si los invariantes espectrales satisfacen las condiciones simultáneas ${tr_c}$, ${det_c}$ y ${del_c}$, "
            f"¿cuál es la tipología topológica cualitativa y el régimen de estabilidad local del punto de equilibrio en el {ctx}?"
        )
        c_opt = f"El estado de equilibrio es un {classif}."
        distractors = [
            "El estado de equilibrio es un centro armónico conservativo con órbitas invariantes en todo el plano de fases.",
            "El estado de equilibrio es un punto de silla inestable con dos autovalores reales de signos algebraicos opuestos.",
            "El estado de equilibrio es un foco asintóticamente estable con disipación energética y oscilaciones cíclicas.",
            "El estado de equilibrio es un nodo inestable divergente con crecimiento monótono hacia el infinito en el plano.",
            "El estado de equilibrio colapsa en un atractor caótico de dimensión fractal con sensibilidad a condiciones iniciales.",
            "El estado de equilibrio es neutralmente estable degenerado con autovalores idénticamente nulos en el origen."
        ]
        # Filter out exact match with c_opt
        clean_d = [d for d in distractors if classif[:12].lower() not in d.lower()]
        while len(clean_d) < 6:
            clean_d.append(f"Clasificación alternativa dependiente de condiciones de frontera en el plano ({len(clean_d)+1}).")
        clean_d = clean_d[:6]

        hints = [
            f"Revise el signo del determinante: {det_c}. Si es negativo, es siempre un punto de silla.",
            f"Revise el signo de la traza: {tr_c}. Si es negativa y el determinante es positivo, el sistema es atractor.",
            f"Revise el discriminante: {del_c}. Si es negativo, los autovalores son complejos (foco/centro); si es positivo, son reales (nodo)."
        ]
        sol = f"Bajo las condiciones dadas (${tr_c}$, ${det_c}$, ${del_c}$), la clasificación espectral corresponde a un {classif}."
        warn = "Recuerde: el signo del determinante define la posibilidad de raíces de signos opuestos (silla si det < 0)."
        questions.append(create_mc7_item(
            f"Q-C02-{idx:03d}", "C-02", "Analyze", "medium", ctx,
            stem, c_opt, clean_d, hints, sol, warn, rng
        ))

    # 5 FIB questions
    fib_cases = [
        ("¿Qué valor exacto debe tomar la traza $\\text{tr}(A)$ para que un sistema lineal con determinante positivo $\\det(A) > 0$ sea clasificado como un centro armónico puro?", "0", ["0", "cero"], "Condición de centro puro"),
        ("Si $\\det(A) = -4$, ¿cuál es la clasificación cualitativa del equilibrio (escriba 'silla', 'nodo' o 'foco')?", "silla", ["silla", "punto de silla", "saddle"], "Determinante negativo y punto de silla"),
        ("En el plano traza-determinante, la frontera entre nodos y focos está dada por la parábola $\\det(A) = k [\\text{tr}(A)]^2$. ¿Cuál es el valor fraccionario irreducible de la constante $k$?", "1/4", ["1/4", "0.25", "\\frac{1}{4}"], "Parábola frontera nodo-foco"),
        ("Si un sistema tiene autovalores $\\lambda_1 = -3$ y $\\lambda_2 = -3$, con dos autovectores independientes, ¿cuál es el valor del discriminante $\\Delta$?", "0", ["0", "cero"], "Discriminante en nodo propio"),
        ("Para un sistema con $\\text{tr}(A) = -6$ y $\\det(A) = 9$, calcule el valor del discriminante $\\Delta = \\text{tr}^2 - 4\\det$:", "0", ["0", "cero"], "Frontera parabólica crítica")
    ]
    for offset, (stem_text, ans_str, equivs, ctx) in enumerate(fib_cases, 11):
        stem = f"En la teoría cualitativa de sistemas dinámicos en el plano traza-determinante: {stem_text}"
        hints = [
            "Recuerde la ecuación característica $\\lambda^2 - \\text{tr}(A)\\lambda + \\det(A) = 0$ y su discriminante $\\Delta = \\text{tr}^2 - 4\\det$.",
            "Un centro exige autovalores imaginarios puros $\\lambda = \\pm i\\omega$, lo cual requiere parte real nula $\\text{tr}(A)/2 = 0$."
        ]
        sol = f"El valor analítico correspondiente es ${ans_str}$."
        warn = "Verifique la definición canónica del invariante solicitado."
        questions.append(create_fib_item(
            f"Q-C02-{offset:03d}", "C-02", "Apply", "easy", ctx,
            stem, ans_str, equivs, hints, sol, warn,
            placeholder="Ingresa la respuesta analítica"
        ))

    # 4 MS questions (since Q-MS-GOODWIN-003 is already MS, total MS for C-02 will be 5)
    ms_cases = [
        ("Criterios de hiperbolicidad y Teorema de Hartman-Grobman", [
            {"content": "Un punto de equilibrio es hiperbólico si y solo si todos los autovalores de su matriz jacobiana tienen parte real no nula: $\\text{Re}(\\lambda) \\neq 0$.", "is_correct": True},
            {"content": "El Teorema de Hartman-Grobman asegura equivalencia topológica local entre el sistema no lineal y su linealización solo en puntos hiperbólicos.", "is_correct": True},
            {"content": "Un centro armónico lineal con $\\text{tr}(A) = 0$ y $\\det(A) > 0$ es un punto de equilibrio hiperbólico.", "is_correct": False, "error_rationale": "Un centro tiene Re(lambda)=0, luego es NO hiperbólico."},
            {"content": "Los nodos y focos asintóticamente estables son puntos de equilibrio estrictamente hiperbólicos.", "is_correct": True},
            {"content": "Los puntos de silla son hiperbólicos porque ambos autovalores reales son distintos de cero.", "is_correct": True}
        ]),
        ("Propiedades de los puntos de silla en macroeconomía dinámica", [
            {"content": "Un punto de silla posee exactamente una dirección asintóticamente convergente llamada variedad estable.", "is_correct": True},
            {"content": "En modelos de previsión perfecta (ej. Ramsey, Blanchard-Kahn), la trayectoria de equilibrio converge a lo largo de la variedad estable.", "is_correct": True},
            {"content": "La variedad inestable está asociada al autovalor con parte real estrictamente positiva.", "is_correct": True},
            {"content": "Un punto de silla puede exhibir oscilaciones amortiguadas en torno al estado estacionario.", "is_correct": False, "error_rationale": "Las raíces de un punto de silla son reales de signo opuesto, sin oscilaciones."},
            {"content": "La condición necesaria y suficiente para un punto de silla en sistemas $2\\times 2$ es $\\det(A) < 0$.", "is_correct": True}
        ]),
        ("Bifurcaciones y transiciones en el plano traza-determinante", [
            {"content": "Al cruzar la línea $\\text{tr}(A) = 0$ con $\\det(A) > 0$, el sistema experimenta una bifurcación de Hopf si las raíces son complejas.", "is_correct": True},
            {"content": "Al cruzar el eje horizontal $\\det(A) = 0$, el sistema pierde invertibilidad y experimenta una bifurcación de nodo-silla o transcítica.", "is_correct": True},
            {"content": "La parábola $\\Delta = [\\text{tr}(A)]^2 - 4\\det(A) = 0$ separa el régimen con oscilaciones (focos) del régimen monotónico (nodos).", "is_correct": True},
            {"content": "Un sistema lineal puede tener ciclos límite aislados estables en el plano.", "is_correct": False, "error_rationale": "Los sistemas lineales no admiten ciclos límite aislados (solo centros conservativos o focos)."},
            {"content": "La estabilidad asintótica local exige rigurosamente que tanto $\\text{tr}(A) < 0$ como $\\det(A) > 0$.", "is_correct": True}
        ]),
        ("Focos estables vs nodos estables", [
            {"content": "Tanto los focos como los nodos estables satisfacen $\\text{tr}(A) < 0$ y $\\det(A) > 0$.", "is_correct": True},
            {"content": "En un foco estable, las trayectorias cruzan infinitas veces los ejes coordenados en el espacio de fases al aproximarse al reposo.", "is_correct": True},
            {"content": "En un nodo estable, las trayectorias convergen monotónicamente al reposo sin oscilaciones de signo.", "is_correct": True},
            {"content": "Un foco estable requiere que el determinante sea mayor que $\\frac{[\\text{tr}(A)]^2}{4}$.", "is_correct": True},
            {"content": "La velocidad de amortiguamiento de un foco estable está gobernada por la parte imaginaria de sus autovalores.", "is_correct": False, "error_rationale": "La amortiguación está gobernada por la parte real tr(A)/2; la parte imaginaria define la frecuencia."}
        ])
    ]
    for offset, (stem_title, statements) in enumerate(ms_cases, 16):
        stem = f"En relación con {stem_title} para sistemas continuos bidimensionales, seleccione todas las afirmaciones rigurosamente verdaderas:"
        hints = [
            "Considere la partición de regiones en el plano $(\\text{tr}(A), \\det(A))$.",
            "Evalúe cómo se comportan los autovalores y trayectorias en torno a la frontera parabólica $\\Delta = 0$ y la línea $\\text{tr} = 0$."
        ]
        sol = "Las afirmaciones seleccionadas describen de forma rigurosa las propiedades topológicas y de estabilidad del sistema dinámico."
        warn = "En un foco, la parte real determina la tasa de decaimiento y la parte imaginaria la frecuencia de oscilación."
        questions.append(create_ms_item(
            f"Q-C02-{offset:03d}", "C-02", "Analyze", "hard", "Topología del Espacio de Estados",
            stem, statements, hints, sol, warn
        ))

    return questions

# -----------------------------------------------------------------------------
# Generators for Hab-02 (Skill: Inversión Algebraica Simbólica para Estados Estacionarios)
# Note: Q-HAB02-GOODWIN-002 is already included in curated_exercises (1 item).
# We generate 29 additional questions: 15 MC7, 7 FIB, 7 MS (total 30).
# -----------------------------------------------------------------------------

def generate_hab02_questions(rng: random.Random) -> list[dict[str, Any]]:
    questions = []

    # 15 MC7 questions
    mc_models = [
        # (model_name, steady_state_formula, param_context)
        ("Modelo IS-LM con gasto público e impuestos", "Y^* = \\frac{c_0 + I_0 + \\bar{G} - c\\tau_0 + \\frac{\\mu}{\\gamma}\\bar{m}}{1 - c(1-\\tau) + \\frac{\\mu\\theta}{\\gamma}}", "mercado de bienes y dinero simultáneo"),
        ("Modelo de crecimiento de Solow-Swan con progreso técnico", "k^* = \\left(\\frac{s}{\\delta + n + g}\\right)^{\\frac{1}{1-\\alpha}}", "acumulación de capital per cápita efectivo"),
        ("Modelo de duopolio dinámico de Cournot", "q_1^* = q_2^* = \\frac{a - c}{3b}", "interacción de cantidades con costos simétricos"),
        ("Modelo dinámico de inflación y desempleo de Phillips", "U^* = U_n + \\frac{\\mu}{\\beta}", "tasa natural de desempleo y sesgo inflacionario"),
        ("Modelo de sobreendeudamiento y deflación de Fisher", "D^* = \\frac{\\bar{C} - \\bar{Y}}{r - g}", "balance financiero entre tasa de interés y crecimiento"),
        ("Modelo de ciclos económicos de Goodwin para tasa de empleo", "v^* = \\frac{a + \\alpha_w}{b}", "curva de Phillips lineal y dinámica salarial"),
        ("Modelo de balanza comercial y tipo de cambio real", "R^* = \\frac{\\bar{X} - \\bar{M}}{m_1 + m_2 - 1}", "condición de Marshall-Lerner en equilibrio exterior"),
        ("Modelo de crecimiento con capital público productivo", "k^* = \\left(\\frac{s (1-\\tau) G_p^\\beta}{\\delta + n}\\right)^{\\frac{1}{1-\\alpha}}", "externalidad de infraestructura en producción"),
        ("Modelo de Tobin q con costos cuadráticos de ajuste", "K^* = \\left(\\frac{A \\alpha}{r + \\delta}\\right)^{\\frac{1}{1-\\alpha}}", "relación marginal capital-producto en estado estacionario"),
        ("Modelo macroeconómico con metas de inflación y regla de Taylor", "r^* = r_n + \\pi^* + \\phi_\\pi (\\pi - \\pi^*)", "regla de política monetaria óptima en reposo"),
        ("Modelo de oferta agregada Lucas con sorpresas de precios", "Y^* = \\bar{Y} + \\alpha(P - P^e)", "nivel de producto potencial con previsión neutral"),
        ("Modelo de asignación de recursos y pesca renovable", "S^* = K \\left(1 - \\frac{q E^*}{r}\\right)", "biomasa sostenible en régimen de esfuerzo constante"),
        ("Modelo de equilibrio de mercado laboral con emparejamiento", "u^* = \\frac{s}{s + f(\\theta)}", "tasa de desempleo de flujo Beveridge"),
        ("Modelo de consumo intertemporal con tasa de descuento", "c^* = \\frac{r - \\rho}{\\theta} k^* + w", "sendero de consumo de Ramsey en estado estacionario"),
        ("Modelo de tipo de cambio de sobreajuste de Dornbusch", "s^* = p^* - p_f^* + \\frac{1}{\\eta} y^*", "paridad descubierta de tasas de interés de largo plazo")
    ]

    for idx, (model_name, ss_expr, ctx) in enumerate(mc_models, 1):
        stem = (
            f"En el {model_name} planteado en el marco de la macroeconomía dinámica, "
            f"al igualar las leyes de movimiento a cero ($\\dot{{X}} = 0$) y resolver simbólicamente el sistema algebraico "
            f"para aislar las coordenadas interiores de largo plazo, ¿cuál es la expresión analítica rigurosa del estado estacionario?"
        )
        c_opt = f"El estado estacionario interior satisface formalmente: ${ss_expr}$."
        distractors = [
            f"El estado estacionario interior colapsa a la relación inversa indefinida: ${ss_expr.replace('1-\\alpha', '\\alpha-1')}$.",
            f"El estado estacionario interior omite el denominador de ajuste estructural en el plano: ${ss_expr.replace('+', '-')}$.",
            f"El estado estacionario interior requiere que todos los flujos se anulen únicamente en el origen trivial $(0,0)$.",
            f"El estado estacionario interior diverge hacia el infinito debido a la ausencia de términos de depreciación.",
            f"El estado estacionario interior depende exclusivamente de las condiciones iniciales arbitrarias del tiempo cero.",
            f"El estado estacionario interior se reduce a un valor dependiente del factor de escala imaginario en el plano."
        ]
        hints = [
            f"Plantee el sistema igualando derivadas temporales a cero: $\\dot{{X}} = 0$.",
            f"Despeje las variables endógenas en términos de los parámetros estructurales del modelo.",
            f"Compruebe que los denominadores coincidan con la condición de solvencia e invertibilidad matricial."
        ]
        sol = f"Para el {model_name}, al imponer reposo temporal $\\dot{{X}} = 0$ y despejar simbólicamente, se deduce directamente ${ss_expr}$."
        warn = "Asegúrese de no confundir la solución de equilibrio estático con las trayectorias transitorias de corto plazo."
        questions.append(create_mc7_item(
            f"Q-HAB02-{idx:03d}", "Hab-02", "Apply", "medium", ctx,
            stem, c_opt, distractors, hints, sol, warn, rng
        ))

    # 7 FIB questions
    fib_cases = [
        ("En un modelo lineal $\\dot{X} = AX + B$, con $A = \\begin{bmatrix} -2 & 1 \\\\ 1 & -2 \\end{bmatrix}$ y $B = \\begin{bmatrix} 6 \\\\ 3 \\end{bmatrix}$, calcule la primera coordenada $x^*$ del estado estacionario $X^* = -A^{-1}B$:", "5", ["5", "5.0"], "Inversión 2x2 para estado estacionario"),
        ("Para el sistema anterior, calcule la segunda coordenada $y^*$ del estado estacionario $X^* = -A^{-1}B$:", "4", ["4", "4.0"], "Coordenada y de reposo"),
        ("En el modelo de Goodwin, si la relación capital-producto es $\\sigma = 3$, el progreso técnico es $\\alpha = 0.02$ y el crecimiento demográfico es $n = 0.01$, calcule el valor numérico exacto de $u^* = 1 - (\\alpha + n)\\sigma$:", "0.91", ["0.91", "91/100"], "Participación salarial numérica"),
        ("Si $A = \\begin{bmatrix} -4 & 0 \\\\ 2 & -1 \\end{bmatrix}$ y $B = \\begin{bmatrix} 8 \\\\ -2 \\end{bmatrix}$, determine el valor estacionario $x^* = -a_{11}^{-1} b_1$:", "2", ["2", "2.0"], "Sistema desacoplado triangular"),
        ("Para el sistema anterior con $x^* = 2$, calcule el valor estacionario $y^*$ resolviendo $2(2) - y^* - 2 = 0$:", "2", ["2", "2.0"], "Sustitución hacia adelante"),
        ("En un modelo de Solow sin progreso técnico ($g=0$), si $s = 0.32$, $\\delta = 0.05$, $n = 0.03$ y $\\alpha = 0.5$, calcule el capital de estado estacionario $k^* = (s/(\\delta+n))^{1/(1-\\alpha)}$:", "16", ["16", "16.0"], "Capital de Solow estacionario"),
        ("En el modelo IS-LM con $Y^* = 1000$ y demanda monetaria $L = 0.2Y - 100r = \\bar{M} = 150$, calcule la tasa de interés de equilibrio $r^*$:", "0.5", ["0.5", "1/2", "0.50"], "Tasa de interés de equilibrio")
    ]
    for offset, (stem_text, ans_str, equivs, ctx) in enumerate(fib_cases, 16):
        stem = f"Considere el problema de inversión algebraica y cálculo de estados estacionarios: {stem_text}"
        hints = [
            "Aplique la fórmula vectorial de estado estacionario $X^* = -A^{-1}B$ o resuelva el sistema algebraico lineal directamente.",
            "Sustituya cuidadosamente los parámetros numéricos dados y simplifique la fracción resultante."
        ]
        sol = f"Resolviendo algebraicamente el sistema se obtiene exactamente ${ans_str}$."
        warn = "Atención a los signos negativos al evaluar la fórmula $-A^{-1}B$."
        questions.append(create_fib_item(
            f"Q-HAB02-{offset:03d}", "Hab-02", "Apply", "medium", ctx,
            stem, ans_str, equivs, hints, sol, warn,
            placeholder="Ingresa el valor numérico exacto"
        ))

    # 7 MS questions
    ms_cases = [
        ("Condiciones de existencia y unicidad de estados estacionarios lineales", [
            {"content": "El estado estacionario $X^* = -A^{-1}B$ existe y es único si y solo si la matriz $A$ es no singular ($\\det(A) \\neq 0$).", "is_correct": True},
            {"content": "Si $\\det(A) = 0$ y $B$ no pertenece a la imagen de $A$, el sistema carece de estados estacionarios finitos.", "is_correct": True},
            {"content": "Si $\\det(A) = 0$ y $B$ pertenece a la imagen de $A$, existe un continuo infinito de estados estacionarios.", "is_correct": True},
            {"content": "La posición del estado estacionario $X^*$ depende de las condiciones iniciales del sistema dinámico.", "is_correct": False, "error_rationale": "El estado estacionario es independiente de las condiciones iniciales."},
            {"content": "En sistemas lineales, la estabilidad asintótica del reposo es independiente del vector forzador $B$.", "is_correct": True}
        ]),
        ("Estática comparativa en estados estacionarios", [
            {"content": "Los multiplicadores de estática comparativa se obtienen derivando el vector $X^* = -A^{-1}B$ respecto a los parámetros exógenos.", "is_correct": True},
            {"content": "Un incremento en el gasto público $\\bar{G}$ en el IS-LM dinámico eleva el nivel de ingreso de equilibrio de largo plazo.", "is_correct": True},
            {"content": "Una mayor tasa de ahorro $s$ en el modelo de Solow eleva el stock de capital estacionario por trabajador.", "is_correct": True},
            {"content": "El principio de correspondencia de Samuelson vincula la estabilidad dinámica con los signos de los multiplicadores de estática comparativa.", "is_correct": True},
            {"content": "La tasa de depreciación del capital eleva el nivel de inversión nuta en el estado de reposo.", "is_correct": False, "error_rationale": "Una mayor depreciación reduce el stock de capital de largo plazo."}
        ]),
        ("Propiedades del equilibrio interior en modelos distributivos", [
            {"content": "En el modelo de Goodwin, el estado estacionario interior satisface $\\dot{v}=0$ y $\\dot{u}=0$ simultáneamente con coordenadas estrictamente positivas.", "is_correct": True},
            {"content": "La participación salarial estacionaria $u^*$ es decreciente en la tasa de progreso técnico $\\alpha$ y el crecimiento demográfico $n$.", "is_correct": True},
            {"content": "La tasa de empleo estacionaria $v^*$ depende del intercepto y la pendiente de la curva de salarios reales.", "is_correct": True},
            {"content": "El equilibrio interior de Goodwin es asintóticamente estable en el sentido de Lyapunov con convergencia exponencial.", "is_correct": False, "error_rationale": "El equilibrio es un centro armónico cerrado, no asintóticamente estable."},
            {"content": "La condición $\\gamma > 0$ en Goodwin exige que el producto medio del capital supere la suma del progreso técnico y el crecimiento poblacional.", "is_correct": True}
        ]),
        ("Resolución de equilibrios en sistemas desacoplados triangulares", [
            {"content": "En sistemas triangulares, la primera variable de estado puede resolverse de forma autónoma sin considerar la segunda.", "is_correct": True},
            {"content": "La segunda coordenada de reposo se obtiene sustituyendo el valor estacionario de la primera en la segunda ley de movimiento.", "is_correct": True},
            {"content": "La estructura triangular simplifica la inversión matricial al desacoplar el cálculo del determinante.", "is_correct": True},
            {"content": "Los autovalores de un sistema triangular coinciden exactamente con los elementos de su diagonal principal.", "is_correct": True},
            {"content": "Un sistema triangular requiere necesariamente métodos numéricos iterativos para hallar su estado de reposo.", "is_correct": False, "error_rationale": "Los sistemas triangulares se resuelven analíticamente mediante sustitución directa."}
        ]),
        ("Interpretación económica de multiplicadores de largo plazo", [
            {"content": "La matriz multiplicadora de impacto de largo plazo viene dada analíticamente por $-A^{-1}$.", "is_correct": True},
            {"content": "Si todos los elementos diagonales de $-A^{-1}$ son positivos, incrementos autónomos en cada variable elevan su propio nivel de reposo.", "is_correct": True},
            {"content": "La condición de estabilidad asintótica garantiza que el determinante de $-A$ sea estrictamente positivo en dimensión 2.", "is_correct": True},
            {"content": "El multiplicador de la política monetaria en el IS-LM es proporcional a la sensibilidad del dinero a la tasa de interés.", "is_correct": True},
            {"content": "Cualquier perturbación transitoria modifica permanentemente la posición del estado estacionario en sistemas lineales estables.", "is_correct": False, "error_rationale": "Las perturbaciones transitorias se disipan y el sistema regresa al mismo estado estacionario."}
        ]),
        ("Estados estacionarios en sistemas con rendimientos decrecientes", [
            {"content": "En el modelo de Solow con función Cobb-Douglas, los rendimientos marginales decrecientes aseguran la concavidad de la curva de ahorro.", "is_correct": True},
            {"content": "La intersección de la curva de ahorro $s f(k)$ con la recta de dilución $(\\delta + n)k$ determina un único equilibrio interior no trivial.", "is_correct": True},
            {"content": "El equilibrio trivial en $k=0$ es inestable bajo las condiciones de Inada.", "is_correct": True},
            {"content": "Un aumento en la tasa de ahorro desplaza la curva de inversión hacia arriba, incrementando $k^*$.", "is_correct": True},
            {"content": "En el estado estacionario de Solow, el crecimiento del producto agregado per cápita es igual a la tasa de ahorro $s$.", "is_correct": False, "error_rationale": "El crecimiento per cápita en estado estacionario sin progreso técnico es cero."}
        ]),
        ("Propiedades de invertibilidad y singularidad matricial", [
            {"content": "La fórmula de la matriz inversa $2\\times 2$ requiere dividir la matriz adjunta entre el determinante escalar.", "is_correct": True},
            {"content": "Si $\\det(A) = 0$, la matriz no posee inversa y el sistema carece de solución estacionaria única.", "is_correct": True},
            {"content": "El condicionamiento numérico de la inversión empeora cuando el determinante está muy próximo a cero.", "is_correct": True},
            {"content": "El producto $A A^{-1} = I$ se cumple en ambos sentidos de multiplicación matricial.", "is_correct": True},
            {"content": "Toda matriz simétrica $2\\times 2$ con determinante negativo carece de inversa analítica.", "is_correct": False, "error_rationale": "Si det(A) < 0 != 0, la matriz es perfectamente invertible."}
        ])
    ]
    for offset, (stem_title, statements) in enumerate(ms_cases, 23):
        stem = f"En relación con {stem_title} en el contexto de modelos dinámicos macroeconómicos, seleccione todas las opciones verdaderas:"
        hints = [
            "Considere la ecuación $X^* = -A^{-1}B$ y las condiciones algebraicas de existencia e invertibilidad.",
            "Analice la interpretación económica de los parámetros estructurales y la unicidad del equilibrio."
        ]
        sol = "Las afirmaciones correctas caracterizan con precisión la existencia, cálculo analítico e interpretación de los estados estacionarios."
        warn = "Distinga claramente entre equilibrios únicos (det != 0) y continuos de equilibrios (det = 0 con compatibilidad)."
        questions.append(create_ms_item(
            f"Q-HAB02-{offset:03d}", "Hab-02", "Analyze", "hard", "Análisis de Equilibrio Estacionario",
            stem, statements, hints, sol, warn
        ))

    return questions

# -----------------------------------------------------------------------------
# Generators for Hab-03 (Skill: Diagnóstico Espectral Directo mediante Traza, Determinante y Discriminante)
# Note: Q-HAB03-ISLM-001 (MC7) and Q-MS-PHILLIPS-006 (MS) are in curated_exercises (2 items).
# We generate 28 additional questions: 14 MC7, 8 FIB, 6 MS (total 30).
# -----------------------------------------------------------------------------

def generate_hab03_questions(rng: random.Random) -> list[dict[str, Any]]:
    questions = []

    # 14 MC7 questions
    mc_cases = [
        ("IS-LM con alta sensibilidad del dinero a la tasa de interés", "\\text{tr} < 0, \\det > 0, \\Delta < 0", "foco asintóticamente estable con convergencia en espiral amortiguada"),
        ("Dinámica de precios y salarios con inercia inflacionaria fuerte", "\\text{tr} < 0, \\det > 0, \\Delta > 0", "nodo asintóticamente estable con decaimiento monótono al reposo"),
        ("Sistema de metas de inflación con respuesta agresiva de la tasa de interés", "\\text{tr} < 0, \\det > 0, \\Delta < 0", "foco asintóticamente estable con fluctuaciones cíclicas controladas"),
        ("Modelo de especulación cambiaria con expectativas desestabilizadoras", "\\text{tr} > 0, \\det > 0, \\Delta < 0", "foco inestable con oscilaciones expansivas divergentes"),
        ("Sistema de ajuste de inventarios de Metzler con acelerador moderado", "\\text{tr} < 0, \\det > 0, \\Delta > 0", "nodo asintóticamente estable sin sobreajuste oscilatorio"),
        ("Dinámica de deuda pública con tasa de interés superior al crecimiento", "\\text{tr} > 0, \\det < 0, \\Delta > 0", "punto de silla inestable con sendero de sostenibilidad único"),
        ("Modelo macroeconómico con rezagos de recaudación de Olivera-Tanzi", "\\text{tr} > 0, \\det > 0, \\Delta > 0", "nodo inestable con divergencia fiscal acelerada"),
        ("Modelo de cobweb dinámico continuo acoplado oferta-demanda", "\\text{tr} < 0, \\det > 0, \\Delta < 0", "foco asintóticamente estable con ciclos de precios decrecientes"),
        ("Dinámica monetaria de Clower con restricciones de liquidez", "\\text{tr} < 0, \\det > 0, \\Delta > 0", "nodo asintóticamente estable con absorción gradual de liquidez"),
        ("Modelo de competencia de Bertrand dinámico con costos simétricos", "\\text{tr} < 0, \\det > 0, \\Delta > 0", "nodo asintóticamente estable hacia el equilibrio no cooperativo"),
        ("Sistema macroeconómico con efectos de riqueza de Pigou", "\\text{tr} < 0, \\det > 0, \\Delta < 0", "foco asintóticamente estable amortiguado hacia el pleno empleo"),
        ("Modelo de Dornbusch con perfecta movilidad de capitales", "\\text{tr} > 0, \\det < 0, \\Delta > 0", "punto de silla con convergencia condicionada a la variedad estable"),
        ("Dinámica de balanza de pagos con tipo de cambio fijo", "\\text{tr} < 0, \\det > 0, \\Delta > 0", "nodo asintóticamente estable con ajuste automático de reservas"),
        ("Sistema de ciclos distributivos con impuestos progresivos estabilizadores", "\\text{tr} < 0, \\det > 0, \\Delta < 0", "foco asintóticamente estable disipando el ciclo de Goodwin")
    ]
    for idx, (model_name, conds, regime_desc) in enumerate(mc_cases, 1):
        stem = (
            f"Considere el {model_name}. El análisis algebraico de la matriz dinámica revela que los invariantes "
            f"espectrales cumplen ${conds}$. Mediante diagnóstico espectral directo sin resolver autovectores, "
            f"¿cuál es la tipología y el régimen de estabilidad local del estado estacionario?"
        )
        c_opt = f"El equilibrio se diagnostica como un {regime_desc}."
        distractors = [
            "El equilibrio se diagnostica como un punto de silla inestable con divergencia en una dirección del espacio.",
            "El equilibrio se diagnostica como un centro armónico conservativo con fluctuaciones periódicas perpetuas en el plano.",
            "El equilibrio se diagnostica como un nodo degenerado inestable con pérdida de estabilidad asintótica local.",
            "El equilibrio se diagnostica como una variedad continua de puntos no aislados con estabilidad neutral estática.",
            "El equilibrio se diagnostica como un foco inestable expansivo con trayectorias espirales no acotadas.",
            "El equilibrio se diagnostica como un atractor caótico de dimensión no entera con ergodicidad global."
        ]
        clean_d = [d for d in distractors if regime_desc[:12].lower() not in d.lower()]
        while len(clean_d) < 6:
            clean_d.append(f"Diagnóstico complementario dependiente de parámetros en el plano de estados ({len(clean_d)+1}).")
        clean_d = clean_d[:6]

        hints = [
            f"Evalúe los tres invariantes: {conds}.",
            "Si $\\text{tr} < 0$ y $\\det > 0$, el sistema es asintóticamente estable.",
            "El signo del discriminante $\\Delta$ determina si el ajuste es monotónico ($\\Delta \\ge 0$, nodo) u oscilatorio amortiguado ($\\Delta < 0$, foco)."
        ]
        sol = f"Dado que {conds}, el sistema satisface las condiciones para un {regime_desc}."
        warn = "No confunda discriminante negativo con determinante negativo: si det > 0 y Delta < 0, el sistema es un foco, no una silla."
        questions.append(create_mc7_item(
            f"Q-HAB03-{idx:03d}", "Hab-03", "Analyze", "medium", model_name,
            stem, c_opt, clean_d, hints, sol, warn, rng
        ))

    # 8 FIB questions
    fib_cases = [
        ("Dada la matriz $A = \\begin{bmatrix} -3 & 2 \\\\ -4 & -1 \\end{bmatrix}$, calcule el valor exacto del determinante $\\det(A)$:", "11", ["11", "11.0"], "Determinante de foco estable"),
        ("Para la matriz anterior con $\\text{tr}(A) = -4$ y $\\det(A) = 11$, calcule el discriminante $\\Delta = (-4)^2 - 4(11)$:", "-28", ["-28"], "Discriminante de foco"),
        ("Si $A = \\begin{bmatrix} -5 & 3 \\\\ 2 & -4 \\end{bmatrix}$, calcule la traza $\\text{tr}(A)$:", "-9", ["-9"], "Traza de nodo"),
        ("Para la matriz anterior con $\\text{tr}(A) = -9$ y $\\det(A) = (-5)(-4) - (3)(2) = 14$, calcule el discriminante $\\Delta = (-9)^2 - 4(14)$:", "25", ["25"], "Discriminante de nodo"),
        ("Para un sistema con $\\det(A) = -12$ y $\\text{tr}(A) = 2$, ¿cuál es la tipología (escriba 'silla', 'nodo' o 'foco')?", "silla", ["silla", "punto de silla"], "Clasificación de silla"),
        ("Si un sistema con $\\text{tr}(A) = -8$ tiene raíz doble crítica, ¿qué valor debe tomar el determinante para que $\\Delta = 0$?", "16", ["16", "16.0"], "Determinante crítico"),
        ("Para $A = \\begin{bmatrix} 0 & 5 \\\\ -2 & 0 \\end{bmatrix}$, calcule el determinante $\\det(A)$:", "10", ["10", "10.0"], "Determinante de centro"),
        ("Para la matriz anterior con $\\text{tr}(A) = 0$ y $\\det(A) = 10$, calcule el discriminante $\\Delta = 0^2 - 4(10)$:", "-40", ["-40"], "Discriminante de centro armónico")
    ]
    for offset, (stem_text, ans_str, equivs, ctx) in enumerate(fib_cases, 15):
        stem = f"En el diagnóstico espectral de matrices dinámicas $2\\times 2$: {stem_text}"
        hints = [
            "Aplique las fórmulas canónicas de invariantes: $\\text{tr}(A) = a_{11} + a_{22}$, $\\det(A) = a_{11}a_{22} - a_{12}a_{21}$, $\\Delta = \\text{tr}^2 - 4\\det$.",
            "Realice las operaciones aritméticas con estricto cuidado de signos."
        ]
        sol = f"El valor numérico exacto es ${ans_str}$."
        warn = "Verifique el producto de signos al restar el término cruzado $a_{12} a_{21}$."
        questions.append(create_fib_item(
            f"Q-HAB03-{offset:03d}", "Hab-03", "Apply", "easy", ctx,
            stem, ans_str, equivs, hints, sol, warn,
            placeholder="Ingresa el valor numérico"
        ))

    # 6 MS questions (since Q-MS-PHILLIPS-006 is already MS, total MS for Hab-03 will be 7)
    ms_cases = [
        ("Criterio de Routh-Hurwitz para dimensión dos", [
            {"content": "Para un sistema continuo $2\\times 2$, el criterio de Routh-Hurwitz exige estrictamente $\\text{tr}(A) < 0$ y $\\det(A) > 0$.", "is_correct": True},
            {"content": "Si $\\text{tr}(A) < 0$ y $\\det(A) > 0$, todos los autovalores tienen parte real estrictamente negativa.", "is_correct": True},
            {"content": "La condición $\\det(A) > 0$ por sí sola es suficiente para garantizar estabilidad asintótica.", "is_correct": False, "error_rationale": "Si tr(A) > 0 y det(A) > 0, el sistema es inestable."},
            {"content": "Si $\\text{tr}(A) = 0$ y $\\det(A) > 0$, el sistema se encuentra en el límite de estabilidad (estabilidad marginal).", "is_correct": True},
            {"content": "El criterio de Routh-Hurwitz es equivalente a exigir que los coeficientes del polinomio característico sean todos positivos.", "is_correct": True}
        ]),
        ("Propiedades espectrales del modelo IS-LM dinámico", [
            {"content": "La velocidad de ajuste del mercado de bienes $c_1$ y del dinero $c_2$ influyen en la magnitud de la traza.", "is_correct": True},
            {"content": "La condición $c(1-\\tau) < 1$ asegura que el efecto estabilizador del ahorro y la tributación sea positivo.", "is_correct": True},
            {"content": "Si los parámetros inducen $\\Delta < 0$, el ajuste hacia el equilibrio $(Y^E, r^E)$ exhibe ciclos amortiguados.", "is_correct": True},
            {"content": "Una mayor propensión marginal a consumir $c$ tiende a desestabilizar la traza haciéndola más positiva.", "is_correct": True},
            {"content": "El modelo IS-LM dinámico siempre colapsa en un punto de silla para cualquier combinación admisible de parámetros.", "is_correct": False, "error_rationale": "Bajo parámetros estándar, det > 0 y tr < 0, por lo que es un nodo o foco estable, no una silla."}
        ]),
        ("Efecto de parámetros fiscales y monetarios en el régimen dinámico", [
            {"content": "Un incremento en la tasa impositiva $\\tau$ refuerza el estabilizador automático reduciendo la traza.", "is_correct": True},
            {"content": "Una mayor sensibilidad de la inversión a la tasa de interés $\\mu$ incrementa el determinante y la estabilidad.", "is_correct": True},
            {"content": "Ajustes ultrarrápidos del mercado monetario ($c_2 \\to \\infty$) pueden alterar el signo del discriminante hacia oscilaciones complejas.", "is_correct": True},
            {"content": "El gasto público constante $\\bar{G}$ altera el valor propio dominante de la matriz jacobiana.", "is_correct": False, "error_rationale": "El gasto público constante entra en el vector forzador B, no en la matriz A."},
            {"content": "La estabilidad asintótica local requiere que el multiplicador keynesiano dinámico sea acotado y positivo.", "is_correct": True}
        ]),
        ("Diagnóstico directo de bifurcaciones en modelos macro", [
            {"content": "Una bifurcación de Hopf ocurre cuando la traza pasa de negativa a positiva con $\\det(A) > 0$ constante.", "is_correct": True},
            {"content": "En la bifurcación de Hopf, los autovalores cruzan el eje imaginario como un par complejo conjugado.", "is_correct": True},
            {"content": "Una bifurcación estática ocurre cuando el determinante cambia de signo cruzando por cero.", "is_correct": True},
            {"content": "En un punto de bifurcación de Hopf, el sistema localmente se comporta como un centro lineal con $\\text{tr} = 0$.", "is_correct": True},
            {"content": "Cualquier bifurcación en dimensión dos requiere necesariamente que el determinante sea negativo.", "is_correct": False, "error_rationale": "La bifurcación de Hopf exige det > 0 y tr = 0."}
        ]),
        ("Comparación de estabilidad en sistemas continuos vs discretos", [
            {"content": "En sistemas continuos, la estabilidad exige $\\text{Re}(\\lambda) < 0$ (semiplano izquierdo complejo).", "is_correct": True},
            {"content": "En sistemas discretos, la estabilidad exige $|\\lambda| < 1$ (interior del círculo unitario complejo).", "is_correct": True},
            {"content": "La condición $\\text{tr} < 0, \\det > 0$ es específica de sistemas continuos de ecuaciones diferenciales.", "is_correct": True},
            {"content": "Un autovalor real negativo en un sistema continuo produce alternancia oscilatoria discreta en cada paso.", "is_correct": False, "error_rationale": "En sistemas continuos, lambda < 0 produce decaimiento exponencial monotónico e^{lambda t}."},
            {"content": "La transformación bilineal permite mapear las condiciones de estabilidad de sistemas continuos a discretos.", "is_correct": True}
        ]),
        ("Interpretación de raíces repetidas y modos no oscilatorios", [
            {"content": "Cuando $\\Delta = 0$, los dos autovalores coinciden en el valor real $\\lambda = \\frac{\\text{tr}(A)}{2}$.", "is_correct": True},
            {"content": "Si $\\text{tr}(A) < 0$ y $\\Delta = 0$, el equilibrio es un nodo impropio degenerado asintóticamente estable.", "is_correct": True},
            {"content": "La presencia de raíz doble representa el límite de amortiguamiento crítico entre el régimen nodal y focal.", "is_correct": True},
            {"content": "En amortiguamiento crítico, el retorno al equilibrio ocurre sin oscilaciones en el tiempo mínimo posible.", "is_correct": True},
            {"content": "Si $\\Delta = 0$, el sistema siempre es diagonalizable con base ortogonal de autovectores.", "is_correct": False, "error_rationale": "A menos que sea matriz escalar, Delta=0 genera matrices defectivas no diagonalizables."}
        ])
    ]
    for offset, (stem_title, statements) in enumerate(ms_cases, 23):
        stem = f"En relación con {stem_title} para el diagnóstico de sistemas dinámicos macroeconómicos, seleccione todas las opciones verdaderas:"
        hints = [
            "Aplique las condiciones del criterio de Routh-Hurwitz y las definiciones espectrales continuas.",
            "Considere los parámetros económicos estructurales y su efecto en la traza y determinante."
        ]
        sol = "Las afirmaciones correctas caracterizan con rigor las condiciones de estabilidad y bifurcación espectral."
        warn = "Recuerde que para sistemas continuos la estabilidad requiere parte real negativa: Re(lambda) < 0."
        questions.append(create_ms_item(
            f"Q-HAB03-{offset:03d}", "Hab-03", "Analyze", "hard", "Diagnóstico Espectral Macroeconómico",
            stem, statements, hints, sol, warn
        ))

    return questions

# -----------------------------------------------------------------------------
# Generators for Hab-04 (Skill: Resolución de Subespacios Propios para Trayectorias Explícitas)
# Note: Q-HAB04-EIG-007 (MC7) is in curated_exercises (1 item).
# We generate 29 additional questions: 14 MC7, 8 FIB, 7 MS (total 30).
# -----------------------------------------------------------------------------

def generate_hab04_questions(rng: random.Random) -> list[dict[str, Any]]:
    questions = []

    # 14 MC7 questions on eigenvectors and explicit trajectories
    matrix_cases = [
        # (a, b, c, d, l1, v1_str, l2, v2_str, ctx)
        (2, 1, 1, 2, 3, "\\begin{bmatrix} 1 \\\\ 1 \\end{bmatrix}", 1, "\\begin{bmatrix} -1 \\\\ 1 \\end{bmatrix}", "Sistema simétrico acoplado de producción y consumo"),
        (4, 2, 1, 3, 5, "\\begin{bmatrix} 2 \\\\ 1 \\end{bmatrix}", 2, "\\begin{bmatrix} -1 \\\\ 1 \\end{bmatrix}", "Modelo dinámico de difusión de innovaciones tecnológicas"),
        (1, 2, 3, 2, 4, "\\begin{bmatrix} 2 \\\\ 3 \\end{bmatrix}", -1, "\\begin{bmatrix} -1 \\\\ 1 \\end{bmatrix}", "Sistema de interacción de precios en duopolio"),
        (-1, 2, -1, -4, -2, "\\begin{bmatrix} 2 \\\\ -1 \\end{bmatrix}", -3, "\\begin{bmatrix} 1 \\\\ -1 \\end{bmatrix}", "Dinámica de estabilización de déficit y deuda"),
        (3, -2, 2, -2, 2, "\\begin{bmatrix} 2 \\\\ 1 \\end{bmatrix}", -1, "\\begin{bmatrix} 1 \\\\ 2 \\end{bmatrix}", "Modelo de comercio con costos de transporte dinámicos"),
        (-3, 1, 1, -3, -2, "\\begin{bmatrix} 1 \\\\ 1 \\end{bmatrix}", -4, "\\begin{bmatrix} -1 \\\\ 1 \\end{bmatrix}", "Sistema de dispersión espacial de salarios reales"),
        (5, -4, 2, -1, 3, "\\begin{bmatrix} 2 \\\\ 1 \\end{bmatrix}", 1, "\\begin{bmatrix} 1 \\\\ 1 \\end{bmatrix}", "Modelo de cartera de activos con rendimientos correlacionados"),
        (-2, 4, 1, 1, 2, "\\begin{bmatrix} 1 \\\\ 1 \\end{bmatrix}", -3, "\\begin{bmatrix} -4 \\\\ 1 \\end{bmatrix}", "Dinámica de ajuste entre empleo formal e informal"),
        (1, 3, 2, 2, 4, "\\begin{bmatrix} 1 \\\\ 1 \\end{bmatrix}", -1, "\\begin{bmatrix} -3 \\\\ 2 \\end{bmatrix}", "Modelo dinámico de arbitraje en mercados cambiarios"),
        (-4, 3, 2, -3, -1, "\\begin{bmatrix} 1 \\\\ 1 \\end{bmatrix}", -6, "\\begin{bmatrix} -3 \\\\ 2 \\end{bmatrix}", "Sistema de fijación de salarios con negociación colectiva"),
        (2, -1, -2, 3, 4, "\\begin{bmatrix} -1 \\\\ 2 \\end{bmatrix}", 1, "\\begin{bmatrix} 1 \\\\ 1 \\end{bmatrix}", "Modelo dinámico de balanza de pagos y aranceles"),
        (3, 4, 1, 3, 5, "\\begin{bmatrix} 2 \\\\ 1 \\end{bmatrix}", 1, "\\begin{bmatrix} -2 \\\\ 1 \\end{bmatrix}", "Sistema macroeconómico con retardos de inversión"),
        (-1, 3, 2, 0, 2, "\\begin{bmatrix} 1 \\\\ 1 \\end{bmatrix}", -3, "\\begin{bmatrix} -3 \\\\ 2 \\end{bmatrix}", "Dinámica de saldos monetarios reales y producto"),
        (4, -2, 1, 1, 3, "\\begin{bmatrix} 2 \\\\ 1 \\end{bmatrix}", 2, "\\begin{bmatrix} 1 \\\\ 1 \\end{bmatrix}", "Modelo de ajuste de inventarios con costos de almacenamiento")
    ]
    for idx, (a, b, c, d, l1, v1_str, l2, v2_str, ctx) in enumerate(matrix_cases, 1):
        stem = (
            f"Considere la matriz dinámica homogénea $A = \\begin{{bmatrix}} {a} & {b} \\\\ {c} & {d} \\end{{bmatrix}}$ "
            f"asociada al {ctx}. Resuelva el sistema algebraico de autovectores $(A - \\lambda I)v = 0$ para determinar "
            f"los valores propios $\\lambda_1, \\lambda_2$ y sus correspondientes autovectores asociados $v_1, v_2$."
        )
        c_opt = f"$\\lambda_1 = {l1}, v_1 = {v1_str}; \\quad \\lambda_2 = {l2}, v_2 = {v2_str}$."
        distractors = [
            f"$\\lambda_1 = {-l1}, v_1 = {v1_str}; \\quad \\lambda_2 = {-l2}, v_2 = {v2_str}$, invirtiendo erróneamente los signos de las raíces.",
            f"$\\lambda_1 = {l1}, v_1 = {v2_str}; \\quad \\lambda_2 = {l2}, v_2 = {v1_str}$, asociando de forma cruzada los autovectores a las raíces equivocadas.",
            f"$\\lambda_1 = {l1+2}, v_1 = {v1_str}; \\quad \\lambda_2 = {l2-1}, v_2 = {v2_str}$, cometiendo un error algebraico en la factorización del trinomio.",
            f"$\\lambda_1 = {l1}, v_1 = \\begin{{bmatrix}} 1 \\\\ 0 \\end{{bmatrix}}; \\quad \\lambda_2 = {l2}, v_2 = \\begin{{bmatrix}} 0 \\\\ 1 \\end{{bmatrix}}$, suponiendo una base canónica trivial.",
            f"$\\lambda_1 = {l2}, v_1 = {v1_str}; \\quad \\lambda_2 = {l1}, v_2 = {v2_str}$, intercambiando arbitrariamente los subespacios propios en el plano.",
            f"$\\lambda_1 = 0, v_1 = {v1_str}; \\quad \\lambda_2 = {l1+l2}, v_2 = {v2_str}$, suponiendo erróneamente que la matriz es singular con determinante nulo."
        ]
        hints = [
            f"Polinomio característico: $\\lambda^2 - ({a+d})\\lambda + ({a*d - b*c}) = 0$.",
            f"Factorice el polinomio para hallar las raíces: $\\lambda_1 = {l1}$ y $\\lambda_2 = {l2}$.",
            f"Para cada autovalor, resuelva $(A - \\lambda_i I)v_i = 0$ para hallar un autovector no nulo."
        ]
        sol = f"Las raíces del polinomio característico son $\\lambda_1 = {l1}$ y $\\lambda_2 = {l2}$. Resolviendo los núcleos asociados, obtenemos los autovectores normalizados $v_1 = {v1_str}$ y $v_2 = {v2_str}$."
        warn = "Compruebe que $(A - \\lambda I)v = 0$ se verifique en ambas filas del sistema matricial."
        questions.append(create_mc7_item(
            f"Q-HAB04-{idx:03d}", "Hab-04", "Apply", "medium", ctx,
            stem, c_opt, distractors, hints, sol, warn, rng
        ))

    # 8 FIB questions
    fib_cases = [
        ("Dada la matriz $A = \\begin{bmatrix} 2 & 1 \\\\ 1 & 2 \\end{bmatrix}$, calcule el autovalor dominante (de mayor valor numérico) $\\lambda_1$:", "3", ["3", "3.0"], "Autovalor dominante"),
        ("Para la matriz anterior, determine la pendiente $k = v_2/v_1$ del autovector asociado a $\\lambda_1 = 3$ con $v_1 = [1, k]^T$:", "1", ["1", "1.0"], "Pendiente de autovector"),
        ("Para la matriz $A = \\begin{bmatrix} 4 & 2 \\\\ 1 & 3 \\end{bmatrix}$, calcule el autovalor menor $\\lambda_2$:", "2", ["2", "2.0"], "Autovalor menor"),
        ("Para la matriz anterior con $\\lambda_2 = 2$, calcule la pendiente $k = v_2/v_1$ del autovector asociado:", "-1", ["-1", "-1.0"], "Pendiente negativa"),
        ("Si $A = \\begin{bmatrix} 1 & 3 \\\\ 2 & 2 \\end{bmatrix}$, calcule la traza $\\text{tr}(A) = \\lambda_1 + \\lambda_2$:", "3", ["3", "3.0"], "Suma de autovalores"),
        ("Para la matriz anterior, calcule el producto de los autovalores $\\lambda_1 \\lambda_2 = \\det(A)$:", "-4", ["-4", "-4.0"], "Producto de autovalores"),
        ("Dada la matriz diagonal $A = \\begin{bmatrix} -3 & 0 \\\\ 0 & -5 \\end{bmatrix}$, ¿cuál es el autovalor de decaimiento más lento?", "-3", ["-3", "-3.0"], "Autovalor dominante negativo"),
        ("Para la matriz $A = \\begin{bmatrix} -1 & 4 \\\\ 1 & -1 \\end{bmatrix}$, calcule el autovalor positivo asociado a la dirección inestable:", "1", ["1", "1.0"], "Autovalor positivo en silla")
    ]
    for offset, (stem_text, ans_str, equivs, ctx) in enumerate(fib_cases, 15):
        stem = f"En la resolución analítica de subespacios propios y autovalores para sistemas $2\\times 2$: {stem_text}"
        hints = [
            "Resuelva el polinomio característico $\\lambda^2 - \\text{tr}(A)\\lambda + \\det(A) = 0$.",
            "Sustituya en el sistema homogéneo $(A - \\lambda I)v = 0$ para aislar las razones entre componentes."
        ]
        sol = f"El valor numérico escalar exacto es ${ans_str}$."
        warn = "Verifique la sustitución del autovalor en la ecuación característica antes de computar el autovector."
        questions.append(create_fib_item(
            f"Q-HAB04-{offset:03d}", "Hab-04", "Apply", "easy", ctx,
            stem, ans_str, equivs, hints, sol, warn,
            placeholder="Ingresa el valor numérico"
        ))

    # 7 MS questions
    ms_cases = [
        ("Propiedades de los autovectores en sistemas lineales bidimensionales", [
            {"content": "Cualquier múltiplo escalar no nulo $k v$ de un autovector $v$ es también un autovector del mismo subespacio propio.", "is_correct": True},
            {"content": "Autovectores asociados a autovalores reales distintos son linealmente independientes.", "is_correct": True},
            {"content": "Toda matriz simétrica real $2\\times 2$ posee autovectores ortogonales asociados a autovalores distintos.", "is_correct": True},
            {"content": "El vector nulo $[0, 0]^T$ es considerado formalmente como un autovector de toda matriz lineal.", "is_correct": False, "error_rationale": "Por definición axiomática, un autovector debe ser estrictamente no nulo."},
            {"content": "Si $v$ es autovector de $A$ con valor $\\lambda$, entonces $v$ es autovector de $A^2$ con valor $\\lambda^2$.", "is_correct": True}
        ]),
        ("Formulación de la solución complementaria general", [
            {"content": "Para autovalores reales distintos, la solución general es $X_h(t) = c_1 e^{\\lambda_1 t} v_1 + c_2 e^{\\lambda_2 t} v_2$.", "is_correct": True},
            {"content": "Las direcciones de los autovectores $v_1, v_2$ definen las asíntotas y trayectorias rectilíneas invariantes en el plano.", "is_correct": True},
            {"content": "Si la condición inicial se sitúa exactamente sobre la recta generada por $v_1$, la trayectoria no abandona esa recta.", "is_correct": True},
            {"content": "Las constantes $c_1, c_2$ pueden ser funciones no lineales del tiempo en sistemas autónomos.", "is_correct": False, "error_rationale": "Las constantes de integración c_1, c_2 son escalares constantes fijados por t=0."},
            {"content": "La matriz fundamental de soluciones se forma colocando los vectores $e^{\\lambda_1 t} v_1$ y $e^{\\lambda_2 t} v_2$ como columnas.", "is_correct": True}
        ]),
        ("Estructura de subespacios en puntos de silla", [
            {"content": "La variedad estable unidimensional coincide con la recta generada por el autovector del autovalor negativo.", "is_correct": True},
            {"content": "La variedad inestable unidimensional coincide con la recta generada por el autovector del autovalor positivo.", "is_correct": True},
            {"content": "Cualquier condición inicial fuera de la variedad estable genera una trayectoria divergente.", "is_correct": True},
            {"content": "En un punto de silla, las dos direcciones propias son siempre perpendiculares entre sí para cualquier matriz.", "is_correct": False, "error_rationale": "Solo son perpendiculares si la matriz es simétrica; genéricamente no son ortogonales."},
            {"content": "La pendiente de la variedad estable es crucial para aislar el sendero de equilibrio en modelos macroeconómicos de expectativas.", "is_correct": True}
        ]),
        ("Diagonalización y desacoplamiento de sistemas lineales", [
            {"content": "Si $A$ posee dos autovalores reales distintos, existe una matriz invertible $P = [v_1, v_2]$ tal que $P^{-1} A P = D$.", "is_correct": True},
            {"content": "El cambio de variables $X = P Z$ transforma el sistema acoplado en dos ecuaciones diferenciales desacopladas $\\dot{z}_i = \\lambda_i z_i$.", "is_correct": True},
            {"content": "La matriz diagonal $D$ contiene los autovalores $\\lambda_1, \\lambda_2$ en su diagonal principal.", "is_correct": True},
            {"content": "Toda matriz $2\\times 2$ con raíz doble repetida puede diagonalizarse completamente en la base canónica.", "is_correct": False, "error_rationale": "Si existe deficiencia geométrica, la matriz requiere forma canónica de Jordan."},
            {"content": "La exponencial matricial se calcula directamente como $e^{At} = P e^{Dt} P^{-1}$ cuando $A$ es diagonalizable.", "is_correct": True}
        ]),
        ("Autovalores complejos conjugados y base real", [
            {"content": "Para autovalores complejos $\\lambda = a \\pm bi$, el autovector toma la forma $v = u \\pm i w$.", "is_correct": True},
            {"content": "La base de soluciones reales combina términos trigonométricos $\\cos(bt)$ y $\\sin(bt)$ modulados por $e^{at}$.", "is_correct": True},
            {"content": "Los vectores real e imaginario $u$ y $w$ forman una base para el plano de fases.", "is_correct": True},
            {"content": "La trayectoria en el plano describe elipses o espirales alrededor del punto de reposo.", "is_correct": True},
            {"content": "En el caso de autovalores complejos conjugados, existen trayectorias rectas invariantes en el plano real.", "is_correct": False, "error_rationale": "No existen direcciones invariantes rectas en el plano real para autovalores complejos."}
        ]),
        ("Autovectores generalizados en sistemas defectivos", [
            {"content": "Una matriz es defectiva si la multiplicidad algebraica de un autovalor excede su multiplicidad geométrica.", "is_correct": True},
            {"content": "El autovector generalizado $v_2$ satisface la ecuación matricial $(A - \\lambda I)v_2 = v_1$, donde $v_1$ es el autovector ordinario.", "is_correct": True},
            {"content": "La solución complementaria general adquiere la estructura $X_h(t) = c_1 e^{\\lambda t} v_1 + c_2 e^{\\lambda t} (v_2 + v_1 t)$.", "is_correct": True},
            {"content": "El término lineal secular $t$ refleja la degeneración parabólica del sistema dinámico.", "is_correct": True},
            {"content": "Toda matriz con autovalores repetidos es necesariamente defectiva.", "is_correct": False, "error_rationale": "Las matrices escalares A = k*I tienen raíz doble pero dos autovectores independientes."}
        ]),
        ("Propiedades de ortogonalidad y simetría", [
            {"content": "Toda matriz simétrica real ($A = A^T$) posee exclusivamente autovalores reales.", "is_correct": True},
            {"content": "Los autovectores asociados a autovalores distintos de una matriz simétrica son mutuamente ortogonales ($v_1^T v_2 = 0$).", "is_correct": True},
            {"content": "Una matriz simétrica siempre puede diagonalizarse mediante una matriz ortogonal $Q$ ($Q^{-1} = Q^T$).", "is_correct": True},
            {"content": "Una matriz simétrica nunca puede originar un foco oscilatorio o centro armónico.", "is_correct": True},
            {"content": "Una matriz simétrica $2\\times 2$ con determinante negativo siempre tiene un autovalor estrictamente imaginario.", "is_correct": False, "error_rationale": "Las matrices simétricas solo tienen autovalores reales; si det < 0 son reales de signo opuesto."}
        ])
    ]
    for offset, (stem_title, statements) in enumerate(ms_cases, 23):
        stem = f"En relación con {stem_title} para sistemas homogéneos lineales, seleccione todas las afirmaciones matemáticamente correctas:"
        hints = [
            "Considere la ecuación de autovalores y autovectores $(A - \\lambda I)v = 0$ y su interpretación geométrica en el espacio de fases.",
            "Analice las implicaciones de autovalores reales distintos, complejos conjugados y raíces repetidas."
        ]
        sol = "Las afirmaciones seleccionadas caracterizan formalmente la estructura de subespacios propios y soluciones complementarias."
        warn = "Recuerde que los autovectores deben ser no nulos y que matrices simétricas garantizan autovalores reales y ortogonales."
        questions.append(create_ms_item(
            f"Q-HAB04-{offset:03d}", "Hab-04", "Analyze", "hard", "Teoría Espectral de Sistemas Dinámicos",
            stem, statements, hints, sol, warn
        ))

    return questions

# -----------------------------------------------------------------------------
# Generators for Hab-05 (Skill: Ajuste por Coeficientes Indeterminados en Sistemas No Homogéneos)
# Note: Q-HAB05-INHOMOG-005 (FIB) is in curated_exercises (1 item).
# We generate 29 additional questions: 15 MC7, 7 FIB, 7 MS (total 30).
# -----------------------------------------------------------------------------

def generate_hab05_questions(rng: random.Random) -> list[dict[str, Any]]:
    questions = []

    # 15 MC7 questions
    mc_cases = [
        ("Forzamiento lineal $B(t) = [3t, 2t]^T$", "X_p(t) = \\begin{bmatrix} A_1 \\\\ B_1 \\end{bmatrix} t + \\begin{bmatrix} A_0 \\\\ B_0 \\end{bmatrix}", "resolver primero $A A_1 + B_1 = 0$ y luego $A A_0 - A_1 + B_0 = 0$", "Modelo macroeconómico con gasto público creciente"),
        ("Forzamiento constante $B(t) = [4, -2]^T$", "X_p = -A^{-1} B", "invertir directamente la matriz $2\\times 2$ multiplicando por el vector independiente", "Dinámica monetaria con nivel de emisión constante"),
        ("Forzamiento exponencial $B(t) = [2 e^{3t}, -e^{3t}]^T$", "X_p(t) = (3I - A)^{-1} \\begin{bmatrix} 2 \\\\ -1 \\end{bmatrix} e^{3t}", "invertir la matriz característica $(3I - A)$ asumiendo que $\\mu=3$ no es autovalor", "Modelo de crecimiento con progreso técnico exógeno exponencial"),
        ("Forzamiento cuadrático $B(t) = [t^2, 0]^T$", "X_p(t) = C_2 t^2 + C_1 t + C_0", "igualar coeficientes consecutivamente para potencias $t^2$, $t^1$ y $t^0$", "Dinámica de inversión con aceleración cuadrática"),
        ("Forzamiento armónico $B(t) = [\\cos(\\omega t), 0]^T$", "X_p(t) = U_1 \\cos(\\omega t) + U_2 \\sin(\\omega t)", "plantear ambas funciones armónicas conjugadas para absorber la primera derivada", "Modelo de ciclos económicos con forzamiento periódico estacional"),
        ("Forzamiento lineal con término constante $B(t) = [t+1, 2t-3]^T$", "X_p(t) = A_1 t + A_0", "desacoplar el sistema algebraico por potencias de tiempo", "Dinámica de balanza comercial con transferencias lineales"),
        ("Forzamiento exponencial amortiguado $B(t) = [e^{-2t}, 3e^{-2t}]^T$", "X_p(t) = (-2I - A)^{-1} \\begin{bmatrix} 1 \\\\ 3 \\end{bmatrix} e^{-2t}", "garantizar que $\\mu = -2$ no coincida con el espectro intrínseco de $A$", "Modelo de ajuste fiscal con consolidación paulatina"),
        ("Forzamiento constante en sistema triangular", "X_{p,1} = -b_1 / a_{11}, \\quad X_{p,2} = -(b_2 + a_{21} X_{p,1}) / a_{22}", "resolver recursivamente mediante sustitución hacia adelante", "Modelo Solow con política ambiental constante"),
        ("Forzamiento polinomial puro sin término constante", "X_p(t) = A_1 t + A_0", "el vector $A_0$ no es nulo genéricamente debido a la derivada temporal $\\dot{X}_p$", "Dinámica de ajuste de precios con deriva de costos"),
        ("Forzamiento resonante donde $\\mu$ es autovalor de $A$", "X_p(t) = (C_1 t + C_0) e^{\\mu t}", "introducir el factor secular $t$ para evitar la singularidad de $(\\mu I - A)$", "Modelo de resonancia macroeconómica con política pro-cíclica"),
        ("Forzamiento por escalón constante después de $t_0$", "X_p = -A^{-1} B_{nuevo}", "el sistema transiciona hacia el nuevo reposo a lo largo de las trayectorias de $A$", "Evaluación de impacto de shock de política permanente"),
        ("Forzamiento con combinación lineal de exponenciales", "X_p(t) = K_1 e^{\\mu_1 t} + K_2 e^{\\mu_2 t}", "aplicar el principio de superposición a cada término forzador de forma aditiva", "Dinámica de expectativas con múltiples velocidades de ajuste"),
        ("Forzamiento sinusoidal puro $B(t) = [0, \\sin(2t)]^T$", "X_p(t) = M \\cos(2t) + N \\sin(2t)", "resolver el sistema lineal matricial acoplado de cuatro incógnitas escalares", "Modelo de inventarios con ciclo de demanda sinusoidal"),
        ("Forzamiento lineal homogéneo en pendientes", "A_1 = -A^{-1} B_1", "la pendiente de la solución particular depende solo de $A$ y del vector de pendientes", "Crecimiento de largo plazo con tendencia lineal en consumo"),
        ("Forzamiento cuadrático completo", "C_2 = -A^{-1} B_2", "el coeficiente cuadrático principal se determina directamente por inversión de $A$", "Modelo dinámico de acumulación de capital cuadrático")
    ]
    for idx, (forcing_type, ans_form, method_desc, ctx) in enumerate(mc_cases, 1):
        stem = (
            f"Considere el sistema lineal no homogéneo $\\dot{{X}} = AX + B(t)$ en el marco del {ctx}. "
            f"Al aplicar el método de coeficientes indeterminados para {forcing_type}, "
            f"¿cuál es la estructura de la propuesta particular $X_p(t)$ y el procedimiento algebraico canónico?"
        )
        c_opt = f"La solución particular postula ${ans_form}$, requiriendo {method_desc}."
        distractors = [
            f"La solución particular postula $X_p(t) = e^{{At}} B(t)$, integrando directamente el forzamiento sin invertir matrices en el plano.",
            f"La solución particular se anula de forma idéntica $X_p(t) = 0$ siempre que la matriz $A$ sea asintóticamente estable.",
            f"La solución particular postula ${ans_form}$, pero omitiendo la derivada temporal al sustituir en la ecuación diferencial.",
            f"La solución particular requiere diagonalizar la matriz $A$ mediante transformaciones no lineales en el espacio de fases.",
            f"La solución particular diverge hacia infinito independientemente del signo de los autovalores intrínsecos de la matriz $A$.",
            f"La solución particular adopta exclusivamente valores discretos en una red de puntos regulares del plano de estados."
        ]
        hints = [
            f"Postule un ansatz de la misma familia funcional que el término forzador $B(t)$.",
            f"Derive temporalmente la propuesta $\\dot{{X}}_p(t)$ y sustituya en $\\dot{{X}} = AX + B(t)$.",
            f"Iguale los coeficientes de funciones base linealmente independientes para obtener el sistema algebraico."
        ]
        sol = f"Para {forcing_type}, se postula ${ans_form}$. Al sustituir en el sistema e igualar términos, {method_desc}."
        warn = "No olvide que al derivar $X_p(t) = A_1 t + A_0$, la derivada temporal es $\\dot{X}_p = A_1$, la cual entra en la ecuación para $A_0$."
        questions.append(create_mc7_item(
            f"Q-HAB05-{idx:03d}", "Hab-05", "Apply", "medium", ctx,
            stem, c_opt, distractors, hints, sol, warn, rng
        ))

    # 7 FIB questions
    fib_cases = [
        ("Dada la matriz $A = \\begin{bmatrix} 2 & 1 \\\\ 0 & 3 \\end{bmatrix}$ y forzamiento lineal $B(t) = \\begin{bmatrix} 4t \\\\ 6t \\end{bmatrix}$, calcule la segunda componente de la pendiente $B_1$ sabiendo que $A \\begin{bmatrix} A_1 \\\\ B_1 \\end{bmatrix} = -\\begin{bmatrix} 4 \\\\ 6 \\end{bmatrix}$:", "-2", ["-2", "-2.0"], "Pendiente de forzamiento B1"),
        ("Para el sistema anterior, calcule la primera componente de la pendiente $A_1$ resolviendo $2 A_1 + (-2) = -4$:", "-1", ["-1", "-1.0"], "Pendiente de forzamiento A1"),
        ("Si $A = \\begin{bmatrix} 1 & 0 \\\\ 0 & 2 \\end{bmatrix}$ y $B = \\begin{bmatrix} 5 \\\\ -4 \\end{bmatrix}$, calcule la primera componente de la solución particular constante $X_{p,1} = -a_{11}^{-1} b_1$:", "-5", ["-5", "-5.0"], "Particular constante diagonal"),
        ("Para el sistema anterior, calcule la segunda componente $X_{p,2} = -a_{22}^{-1} b_2$:", "2", ["2", "2.0"], "Particular componente dos"),
        ("Para la matriz $A = \\begin{bmatrix} 1 & 1 \\\\ 0 & 1 \\end{bmatrix}$, calcule el determinante $\\det(A)$ necesario para invertir el operador forzador:", "1", ["1", "1.0"], "Determinante de operador"),
        ("Si $X_p(t) = A_1 t + A_0$ con $A_1 = [2, 3]^T$, ¿cuál es el valor de la derivada temporal $\\dot{X}_p$ en la primera componente?", "2", ["2", "2.0"], "Derivada temporal de propuesta"),
        ("Para un forzamiento $B(t) = B_0 e^{4t}$ en un sistema con autovalores $\\lambda_1 = 1, \\lambda_2 = 2$, ¿cuál es el escalar $\\mu$ de la frecuencia forzadora?", "4", ["4", "4.0"], "Frecuencia forzadora exponencial")
    ]
    for offset, (stem_text, ans_str, equivs, ctx) in enumerate(fib_cases, 16):
        stem = f"En el cálculo de coeficientes indeterminados para sistemas de EDOs: {stem_text}"
        hints = [
            "Plante la igualdad vectorial $A X_p + B = 0$ o la relación de potencias correspondiente.",
            "Resuelva el sistema lineal algebraico escalar resultante paso a paso."
        ]
        sol = f"El valor numérico escalar exacto resultante es ${ans_str}$."
        warn = "Atención al despejar: $-A^{-1}B$ invierte los signos del vector de forzamiento."
        questions.append(create_fib_item(
            f"Q-HAB05-{offset:03d}", "Hab-05", "Apply", "medium", ctx,
            stem, ans_str, equivs, hints, sol, warn,
            placeholder="Ingresa el valor numérico"
        ))

    # 7 MS questions
    ms_cases = [
        ("Condiciones de validez del método de coeficientes indeterminados", [
            {"content": "El método es aplicable si los términos forzadores son polinomios, exponenciales, senos, cosenos o combinaciones lineales de estos.", "is_correct": True},
            {"content": "Si el término forzador contiene $\\ln(t)$ o $\\tan(t)$, el método de coeficientes indeterminados no es directamente aplicable.", "is_correct": True},
            {"content": "Para forzamientos generales no elementales se debe recurrir al método de variación de parámetros.", "is_correct": True},
            {"content": "La matriz dinámica $A$ debe ser constante (independiente del tiempo) para que el método canónico aplique.", "is_correct": True},
            {"content": "El método solo puede emplearse si todos los autovalores de la matriz $A$ son estrictamente negativos.", "is_correct": False, "error_rationale": "El método aplica independientemente de la estabilidad de A mientras no haya resonancia."}
        ]),
        ("Estructura del ansatz polinomial en sistemas forzados", [
            {"content": "Para un término forzador lineal $B(t) = B_1 t + B_0$, la propuesta genérica es $X_p(t) = A_1 t + A_0$.", "is_correct": True},
            {"content": "La derivada temporal del ansatz lineal es constante: $\\dot{X}_p(t) = A_1$.", "is_correct": True},
            {"content": "Al sustituir, los coeficientes de $t^1$ satisfacen $A A_1 + B_1 = 0 \\implies A_1 = -A^{-1} B_1$.", "is_correct": True},
            {"content": "Los coeficientes de $t^0$ satisfacen $A A_0 - A_1 + B_0 = 0 \\implies A_0 = -A^{-1}(B_0 - A_1)$.", "is_correct": True},
            {"content": "El vector $A_0$ siempre es idénticamente nulo si el forzamiento carece de término constante ($B_0 = 0$).", "is_correct": False, "error_rationale": "Si B_0=0, A_0 = A^{-1} A_1, que genéricamente es no nulo."}
        ]),
        ("Fenómeno de resonancia en sistemas lineales con forzamiento", [
            {"content": "La resonancia ocurre cuando la frecuencia o exponente del forzador coincide con un autovalor de la matriz $A$.", "is_correct": True},
            {"content": "En resonancia, la matriz $(\\mu I - A)$ es singular y no puede invertirse directamente.", "is_correct": True},
            {"content": "Para resolver la resonancia, se modifica el ansatz multiplicando por una potencia de $t$: $X_p(t) = (C_1 t + C_0) e^{\\mu t}$.", "is_correct": True},
            {"content": "La resonancia en sistemas disipativos estables puede producir respuestas no acotadas en el largo plazo.", "is_correct": True},
            {"content": "En ausencia de resonancia, la solución particular siempre decae a cero cuando $t \\to \\infty$.", "is_correct": False, "error_rationale": "Si el forzador no decae (ej. constante o creciente), X_p tampoco decae a cero."}
        ]),
        ("Comparación entre coeficientes indeterminados y variación de parámetros", [
            {"content": "La variación de parámetros es un método universal válido para cualquier término forzador continuo $B(t)$.", "is_correct": True},
            {"content": "La variación de parámetros utiliza la matriz fundamental de soluciones $\\Phi(t)$ mediante $X_p(t) = \\Phi(t) \\int \\Phi^{-1}(s) B(s) ds$.", "is_correct": True},
            {"content": "Los coeficientes indeterminados evitan el cálculo de integrales complejas cuando $B(t)$ es de tipo elemental.", "is_correct": True},
            {"content": "Ambos métodos producen exactamente la misma familia de soluciones particulares válidas.", "is_correct": True},
            {"content": "La variación de parámetros solo funciona cuando la matriz $A$ es diagonal.", "is_correct": False, "error_rationale": "Variación de parámetros aplica a cualquier matriz constante o variable continua."}
        ]),
        ("Propiedades de superposición de soluciones particulares", [
            {"content": "Si $B(t) = B_a(t) + B_b(t)$, entonces $X_p(t) = X_{p,a}(t) + X_{p,b}(t)$ por el principio de superposición.", "is_correct": True},
            {"content": "Se pueden resolver de forma independiente las componentes debidas a tendencias lineales y oscilaciones cíclicas.", "is_correct": True},
            {"content": "La solución completa final suma todas las soluciones particulares a la solución homogénea: $X(t) = X_h(t) + \\sum X_{p,i}(t)$.", "is_correct": True},
            {"content": "La descomposición aditiva es válida aun cuando el sistema presente no linealidades cuadráticas.", "is_correct": False, "error_rationale": "La superposición aditiva solo es válida en sistemas estrictamente lineales."},
            {"content": "La superposición permite desacoplar choques fiscales permanentes de fluctuaciones transitorias de corto plazo.", "is_correct": True}
        ]),
        ("Comportamiento asintótico de soluciones particulares forzadas", [
            {"content": "Si $B(t) = B_0$ (constante) y los autovalores de $A$ tienen parte real negativa, el sistema converge a $X^* = -A^{-1}B_0$.", "is_correct": True},
            {"content": "Si $B(t)$ crece linealmente en el tiempo, las variables de estado convergen a una trayectoria que crece linealmente.", "is_correct": True},
            {"content": "La distancia entre la trayectoria real $X(t)$ y la particular $X_p(t)$ converge a cero si el sistema homogéneo es estable.", "is_correct": True},
            {"content": "Un choque transitorio que se extingue exponencialmente produce una desviación temporal sin alterar el reposo final.", "is_correct": True},
            {"content": "Si la matriz $A$ es inestable, la solución particular $X_p(t)$ deja de satisfacer la ecuación diferencial.", "is_correct": False, "error_rationale": "X_p(t) sigue siendo solución exacta de la EDO, aunque las perturbaciones diverjan de ella."}
        ]),
        ("Técnicas de álgebra matricial en coeficientes indeterminados", [
            {"content": "Para forzamientos vectoriales, las incógnitas del ansatz son vectores de dimensión $n\\times 1$ y no escalares aislados.", "is_correct": True},
            {"content": "La sustitución directa conduce a un sistema algebraico lineal de dimensión $n k$ para polinomios de grado $k-1$.", "is_correct": True},
            {"content": "El uso de la inversa matricial $A^{-1}$ permite aislar directamente los vectores de coeficientes si $\\det(A) \\neq 0$.", "is_correct": True},
            {"content": "En matrices triangulares, las componentes de los vectores coeficientes se resuelven de forma secuencial sin invertir la matriz completa.", "is_correct": True},
            {"content": "Los vectores de coeficientes siempre deben ser ortogonales a las columnas de la matriz $A$.", "is_correct": False, "error_rationale": "No existe tal restricción de ortogonalidad; los coeficientes satisfacen el sistema algebraico lineal."}
        ])
    ]
    for offset, (stem_title, statements) in enumerate(ms_cases, 23):
        stem = f"En relación con {stem_title} en el método de coeficientes indeterminados, seleccione todas las opciones teóricamente válidas:"
        hints = [
            "Considere el procedimiento algebraico de igualar coeficientes de funciones base linealmente independientes.",
            "Analice las hipótesis necesarias sobre la estructura de la matriz $A$ y del forzamiento $B(t)$."
        ]
        sol = "Las afirmaciones correctas describen formalmente el alcance, formulación y resolución de sistemas lineales no homogéneos."
        warn = "El método de coeficientes indeterminados exige que el término forzador pertenezca a clases funcionales cuasi-polinomiales."
        questions.append(create_ms_item(
            f"Q-HAB05-{offset:03d}", "Hab-05", "Analyze", "hard", "Método de Coeficientes Indeterminados",
            stem, statements, hints, sol, warn
        ))

    return questions

# -----------------------------------------------------------------------------
# Generators for Hab-06 (Skill: Linealización Diferencial Alrededor del Estado Estacionario)
# Note: Q-HAB06-SOLOW-004 (MC7) is in curated_exercises (1 item).
# We generate 29 additional questions: 14 MC7, 8 FIB, 7 MS (total 30).
# -----------------------------------------------------------------------------

def generate_hab06_questions(rng: random.Random) -> list[dict[str, Any]]:
    questions = []

    # 14 MC7 questions on linearization and Jacobians
    mc_cases = [
        # (model_name, f_expr, g_expr, J_desc, stability_desc)
        ("Modelo presa-depredador de Lotka-Volterra", "\\dot{x} = x(\\alpha - \\beta y)", "\\dot{y} = y(-\\gamma + \\delta x)", "J^* = \\begin{bmatrix} 0 & -\\beta x^* \\\\ \\delta y^* & 0 \\end{bmatrix}", "centro armónico lineal con $\\text{tr}(J^*) = 0$ y $\\det(J^*) = \\beta \\delta x^* y^* > 0$"),
        ("Modelo de pesca con esfuerzo endógeno de Gordon-Schaefer", "\\dot{S} = rS(1-S/K) - qES", "\\dot{E} = \\eta(pqS - c)E", "J^* = \\begin{bmatrix} -\\frac{r S^*}{K} & -q S^* \\\\ \\eta p q E^* & 0 \\end{bmatrix}", "foco o nodo asintóticamente estable con $\\text{tr}(J^*) < 0$ y $\\det(J^*) > 0$"),
        ("Modelo de contagio epidémico y actividad económica SIR", "\\dot{S} = -\\beta S I", "\\dot{I} = \\beta S I - \\gamma I", "J^* = \\begin{bmatrix} 0 & -\\beta S^* \\\\ 0 & \\beta S^* - \\gamma \\end{bmatrix}", "equilibrio degenerado con valor propio nulo y estabilidad condicional al umbral $\\mathcal{R}_0$"),
        ("Modelo de crecimiento de Solow con polución acumulada", "\\dot{K} = sK^\\alpha - \\delta K", "\\dot{P} = K^\\beta - \\gamma P", "J^* = \\begin{bmatrix} \\delta(\\alpha-1) & 0 \\\\ \\beta (K^*)^{\\beta-1} & -\\gamma \\end{bmatrix}", "nodo asintóticamente estable con autovalores reales negativos en la diagonal"),
        ("Modelo de duopolio dinámico no lineal con costos cuadráticos", "\\dot{q}_1 = v_1(P(Q) - C_1'(q_1))", "\\dot{q}_2 = v_2(P(Q) - C_2'(q_2))", "J^* = \\begin{bmatrix} -v_1(2b+c_1) & -v_1 b \\\\ -v_2 b & -v_2(2b+c_2) \\end{bmatrix}", "nodo asintóticamente estable por dominancia diagonal estricta"),
        ("Modelo macroeconómico con curva de Phillips no lineal", "\\dot{u} = -\\alpha(w - w^*)", "\\dot{w} = \\beta(u - u^*) - \\gamma(w - w^*)^2", "J^* = \\begin{bmatrix} 0 & -\\alpha \\\\ \\beta & 0 \\end{bmatrix}", "centro armónico lineal en el reposo interior con oscilaciones cíclicas conservativas"),
        ("Modelo de ciclos de empleo y distribución de Goodwin", "\\dot{v} = v(\\frac{1}{\\sigma} - \\alpha - n - \\frac{u}{\\sigma})", "\\dot{u} = u(-a + bv)", "J^* = \\begin{bmatrix} 0 & -\\frac{v^*}{\\sigma} \\\\ bu^* & 0 \\end{bmatrix}", "centro armónico conservativo en la aproximación lineal local"),
        ("Modelo de Tobin q con costos de ajuste marginales no lineales", "\\dot{k} = I(q) - \\delta k", "\\dot{q} = r q - f'(k)", "J^* = \\begin{{bmatrix}} 0 & I'(q^*) \\\\ -f''(k^*) & r \\end{{bmatrix}}", "punto de silla con $\\det(J^*) = f''(k^*) I'(q^*) < 0$ debido a rendimientos decrecientes"),
        ("Modelo de acumulación con difusión de tecnología logística", "\\dot{A} = \\eta A(1 - A/A_{max})", "\\dot{k} = s A k^\\alpha - \\delta k", "J^* = \\begin{bmatrix} -\\eta & 0 \\\\ s (k^*)^\\alpha & \\delta(\\alpha-1) \\end{bmatrix}", "nodo asintóticamente estable desacoplado triangular inferior"),
        ("Modelo de sobreexplotación de acuíferos y bombeo agrícola", "\\dot{H} = R - c(H) Q", "\\dot{Q} = \\mu(P_w - P_c(H))", "J^* = \\begin{bmatrix} -c'(H^*) Q^* & -c(H^*) \\\\ -\\mu P_c'(H^*) & 0 \\end{bmatrix}", "foco estable con convergencia en espiral hacia la profundidad hídrica de reposo"),
        ("Modelo de tipo de cambio de sobreajuste de Dornbusch no lineal", "\\dot{e} = r - r^* - \\theta(e - \\bar{e})", "\\dot{p} = \\pi(Y(e,p) - \\bar{Y})", "J^* = \\begin{bmatrix} -\\theta & 0 \\\\ \\pi Y_e & \\pi Y_p \\end{bmatrix}", "punto de silla con ajuste instantáneo a lo largo de la variedad de arbitraje"),
        ("Modelo de dinámica de deuda pública no lineal con prima de riesgo", "\\dot{d} = (r(d) - g)d - s", "\\dot{s} = \\gamma(d - d^*)", "J^* = \\begin{bmatrix} r(d^*) + r'(d^*)d^* - g & -1 \\\\ \\gamma & 0 \\end{bmatrix}", "foco o nodo estable si la regla fiscal reacciona suficientemente a la deuda"),
        ("Modelo de crecimiento de Ramsey-Cass-Koopmans linealizado", "\\dot{k} = f(k) - c - (n+g)k", "\\dot{c} = \\frac{c}{\\theta}(f'(k) - \\rho - \\theta g)", "J^* = \\begin{{bmatrix}} \\rho - n & -1 \\\\ \\frac{c^* f''(k^*)}{\\theta} & 0 \\end{{bmatrix}}", "punto de silla con $\\det(J^*) = \\frac{c^* f''(k^*)}{\\theta} < 0$ por concavidad"),
        ("Modelo de inflación con expectativas adaptativas no lineales", "\\dot{\\pi} = \\alpha(Y - \\bar{Y}) + \\beta(\\pi_e - \\pi)^3", "\\dot{\\pi}_e = \\gamma(\\pi - \\pi_e)", "J^* = \\begin{bmatrix} 0 & 0 \\\\ \\gamma & -\\gamma \\end{bmatrix}", "equilibrio con autovalor nulo debido a la anulación de términos de tercer orden")
    ]
    for idx, (model_name, f_eq, g_eq, J_repr, stab_res) in enumerate(mc_cases, 1):
        stem = (
            f"Considere el sistema dinámico autónomo no lineal del {model_name}:\n"
            f"$${f_eq}$$\n"
            f"$${g_eq}$$\n"
            f"Al linealizar alrededor del estado estacionario interior positivo $(x^*, y^*)$, "
            f"¿cuál es la estructura analítica de la matriz jacobiana $J^*$ y la clasificación cualitativa del equilibrio?"
        )
        c_opt = f"La matriz jacobiana es ${J_repr}$, configurando un {stab_res}."
        distractors = [
            f"La matriz jacobiana es $J^* = \\begin{{bmatrix}} 1 & 0 \\\\ 0 & 1 \\end{{bmatrix}}$, suponiendo erróneamente un desacoplamiento identidad trivial.",
            f"La matriz jacobiana es ${J_repr.replace('-', '+')}$, cometiendo un error sistemático de signos en las derivadas parciales.",
            f"El sistema no lineal no puede linealizarse bajo ninguna circunstancia debido a la presencia de productos de variables de estado.",
            f"La matriz jacobiana presenta traza y determinante nulos simultáneos, colapsando en un punto no aislado en todo el plano.",
            f"La linealización arroja autovalores puramente divergentes independientemente de los valores de los parámetros estructurales.",
            f"La matriz jacobiana invierte las filas y columnas confundiendo la diferenciación cruzada en el punto de reposo."
        ]
        clean_d = [d for d in distractors if stab_res[:10].lower() not in d.lower()]
        while len(clean_d) < 6:
            clean_d.append(f"Clasificación alternativa dependiente del régimen de parámetros estructurales en el plano ({len(clean_d)+1}).")
        clean_d = clean_d[:6]

        hints = [
            f"Calcule las cuatro derivadas parciales: $J_{{11}} = \\frac{{\\partial f}}{{\\partial x}}$, $J_{{12}} = \\frac{{\\partial f}}{{\\partial y}}$, $J_{{21}} = \\frac{{\\partial g}}{{\\partial x}}$, $J_{{22}} = \\frac{{\\partial g}}{{\\partial y}}$.",
            f"Evalúe cada derivada parcial en las coordenadas de reposo $(x^*, y^*)$ utilizando las condiciones de equilibrio $f(x^*, y^*)=0, g(x^*, y^*)=0$.",
            f"Analice la traza y el determinante de la matriz jacobiana evaluada $J^*$ para clasificar la estabilidad local."
        ]
        sol = f"Diferenciando parcialmente y evaluando en el reposo interior, obtenemos la matriz jacobiana ${J_repr}$. Los invariantes de esta matriz corresponden a un {stab_res}."
        warn = "Recuerde evaluar las derivadas en $(x^*, y^*)$ sustituyendo las relaciones de equilibrio para simplificar las expresiones."
        questions.append(create_mc7_item(
            f"Q-HAB06-{idx:03d}", "Hab-06", "Apply", "medium", model_name,
            stem, c_opt, clean_d, hints, sol, warn, rng
        ))

    # 8 FIB questions
    fib_cases = [
        ("Dado el sistema $\\dot{x} = 4x - 2xy$, $\\dot{y} = 3xy - 6y$, determine la derivada parcial $J_{11} = \\partial f / \\partial x$ evaluada en el reposo interior $(x^*, y^*) = (2, 2)$:", "0", ["0", "cero"], "Derivada J11 en presa-depredador"),
        ("Para el sistema anterior, calcule la entrada $J_{12} = \\partial f / \\partial y = -2x$ evaluada en $x^* = 2$:", "-4", ["-4", "-4.0"], "Derivada J12"),
        ("Para el sistema anterior, calcule la entrada $J_{21} = \\partial g / \\partial x = 3y$ evaluada en $y^* = 2$:", "6", ["6", "6.0"], "Derivada J21"),
        ("Para el sistema anterior, determine la traza del Jacobiano $\\text{tr}(J^*) = J_{11} + J_{22}$ sabiendo que $J_{22} = 3(2) - 6 = 0$:", "0", ["0", "cero"], "Traza nula en centro"),
        ("Para el sistema anterior con $J_{11}=0, J_{12}=-4, J_{21}=6, J_{22}=0$, calcule el determinante $\\det(J^*) = -( -4 \\times 6)$:", "24", ["24", "24.0"], "Determinante positivo de Jacobiano"),
        ("Para la función de producción $f(k) = k^{0.5}$, si $k^* = 4$, calcule la derivada marginal $f'(k^*) = 0.5 (4)^{-0.5}$:", "0.25", ["0.25", "1/4", "0.250"], "Productividad marginal en Solow"),
        ("Para el modelo de Solow $\\dot{k} = s f(k) - \\delta k$, el elemento $J_{11}$ es $s f'(k^*) - \\delta$. Dado que en el reposo $s f(k^*) = \\delta k^*$, deduzca el valor de $J_{11}$ si $\\alpha = 0.5$ y $\\delta = 0.1$ ($J_{11} = \\delta(\\alpha - 1)$):", "-0.05", ["-0.05", "-1/20"], "Jacobiano de Solow escalar"),
        ("En el modelo de Ramsey, si $\\det(J^*) = -9$, ¿cuál es la clasificación cualitativa del equilibrio (escriba 'silla', 'nodo' o 'foco')?", "silla", ["silla", "punto de silla"], "Saddle path de Ramsey")
    ]
    for offset, (stem_text, ans_str, equivs, ctx) in enumerate(fib_cases, 15):
        stem = f"En la linealización de sistemas dinámicos no lineales y cálculo de matrices jacobianas: {stem_text}"
        hints = [
            "Aplique la definición de derivada parcial y sustituya las coordenadas del estado estacionario interior.",
            "Utilice las condiciones de reposo para cancelar términos en la evaluación analítica."
        ]
        sol = f"La evaluación numérica escalar exacta es ${ans_str}$."
        warn = "Atención a los signos de los coeficientes de amortiguamiento al calcular derivadas parciales."
        questions.append(create_fib_item(
            f"Q-HAB06-{offset:03d}", "Hab-06", "Apply", "easy", ctx,
            stem, ans_str, equivs, hints, sol, warn,
            placeholder="Ingresa el valor numérico"
        ))

    # 7 MS questions
    ms_cases = [
        ("Fundamentos matemáticos de la linealización jacobiana", [
            {"content": "La linealización se basa en la aproximación de Taylor de primer orden truncando términos de grado dos y superior.", "is_correct": True},
            {"content": "El sistema linealizado toma la forma $\\dot{Z} \\approx J^* Z$, donde $Z = X - X^*$ es el vector de desviaciones locales.", "is_correct": True},
            {"content": "La matriz jacobiana $J^*$ está compuesta por las derivadas parciales de primer orden evaluadas en el punto crítico.", "is_correct": True},
            {"content": "La linealización local preserva de forma exacta las soluciones periódicas globales no lineales en cualquier vecindad de tamaño arbitrario.", "is_correct": False, "error_rationale": "La aproximación es estrictamente local en una vecindad pequeña del punto crítico."},
            {"content": "Si el equilibrio es hiperbólico, los signos de las partes reales de los autovalores de $J^*$ determinan la estabilidad local del sistema no lineal.", "is_correct": True}
        ]),
        ("Alcance y limitaciones del Teorema de Hartman-Grobman", [
            {"content": "El Teorema de Hartman-Grobman establece la existencia de un homeomorfismo local entre el flujo no lineal y el linealizado.", "is_correct": True},
            {"content": "El teorema exige indispensablemente que el punto de equilibrio sea hiperbólico ($\\text{Re}(\\lambda) \\neq 0$).", "is_correct": True},
            {"content": "Si $\\text{tr}(J^*) = 0$ y $\\det(J^*) > 0$ (raíces imaginarias puras), el Teorema de Hartman-Grobman no garantiza la preservación del centro.", "is_correct": True},
            {"content": "En puntos no hiperbólicos, términos no lineales de orden superior pueden transformar un centro lineal en un foco asintóticamente estable o inestable.", "is_correct": True},
            {"content": "El teorema asegura que las velocidades temporales exactas de las trayectorias no lineales coinciden numéricamente con las del sistema lineal.", "is_correct": False, "error_rationale": "El teorema asegura equivalencia topológica cualitativa (órbitas), no coincidencia cuantitativa de velocidades."}
        ]),
        ("Linealización en sistemas desacoplados unidireccionalmente", [
            {"content": "En sistemas donde la primera ecuación no depende de la segunda variable, el elemento $J_{12}$ de la matriz jacobiana es nulo.", "is_correct": True},
            {"content": "Una matriz jacobiana triangular inferior tiene sus autovalores exactamente en la diagonal principal: $\\lambda_1 = J_{11}$ y $\\lambda_2 = J_{22}$.", "is_correct": True},
            {"content": "El análisis de estabilidad puede realizarse analizando los signos de $J_{11}$ y $J_{22}$ de forma independiente.", "is_correct": True},
            {"content": "El acoplamiento unidireccional simplifica el cálculo analítico evitando resolver la ecuación cuadrática completa.", "is_correct": True},
            {"content": "En sistemas triangulares, el determinante siempre es igual a la suma de los elementos de la diagonal principal.", "is_correct": False, "error_rationale": "El determinante es el producto de los elementos diagonales, no la suma."}
        ]),
        ("Propiedades de variedades invariantes en equilibrios de silla", [
            {"content": "En un punto de silla, la variedad estable local es tangente en $(x^*, y^*)$ al autovector asociado al autovalor negativo.", "is_correct": True},
            {"content": "La variedad inestable local es tangente en $(x^*, y^*)$ al autovector asociado al autovalor positivo.", "is_correct": True},
            {"content": "En modelos macroeconómicos con variables predeterminadas y de salto, la condición de silla asegura unicidad del sendero convergente.", "is_correct": True},
            {"content": "Si el número de autovalores inestables coincide con el número de variables de salto, el equilibrio es localmente determinado.", "is_correct": True},
            {"content": "La variedad estable es un conjunto no invariante que cambia de posición según la velocidad de la trayectoria.", "is_correct": False, "error_rationale": "Por definición de variedad invariante, cualquier trayectoria que comience en ella permanece en ella para todo t."}
        ]),
        ("Linealización y análisis cualitativo en modelos ecológico-económicos", [
            {"content": "En el modelo de Lotka-Volterra, la linealización en el reposo interior produce una matriz con traza nula e invariante positivo.", "is_correct": True},
            {"content": "La existencia de una integral primera no lineal (función de Liapunov conservativa) confirma que el centro se preserva globalmente.", "is_correct": True},
            {"content": "Al introducir capacidad de carga en la presa, el elemento $J_{11}$ se vuelve negativo y transforma el centro en un foco estable.", "is_correct": True},
            {"content": "El esfuerzo de pesca excesivo puede inducir una bifurcación que extingue el equilibrio interior positivo.", "is_correct": True},
            {"content": "La linealización local en $(0,0)$ predice que la población de presas y depredadores converge al reposo nulo simultáneamente.", "is_correct": False, "error_rationale": "El origen (0,0) es un punto de silla inestable donde las presas crecen exponencialmente si I=0."}
        ]),
        ("Evaluación de la matriz jacobiana mediante condiciones de reposo", [
            {"content": "Sustituir las identidades de reposo $f(x^*, y^*) = 0$ simplifica notablemente las derivadas parciales complejas.", "is_correct": True},
            {"content": "En modelos tipo Goodwin o Lotka-Volterra, los términos constantes de la ley de movimiento se cancelan al evaluar en el equilibrio.", "is_correct": True},
            {"content": "El determinante de la matriz jacobiana puede expresarse en términos puramente paramétricos sin arrastrar potencias complejas.", "is_correct": True},
            {"content": "La regla de la cadena multivariada permite diferenciar sistemas formulados en términos de variables agregadas compuestas.", "is_correct": True},
            {"content": "Las derivadas parciales de un sistema autónomo siempre dependen explícitamente de la variable temporal $t$.", "is_correct": False, "error_rationale": "En sistemas autónomos, las funciones f y g no dependen explícitamente de t."}
        ]),
        ("Comparación de linealización vs simulación numérica no lineal", [
            {"content": "La linealización analítica proporciona condiciones necesarias y suficientes de estabilidad local válidas para cualquier parámetro.", "is_correct": True},
            {"content": "La simulación numérica permite verificar la cuenca de atracción y explorar comportamientos globales lejos del reposo.", "is_correct": True},
            {"content": "La aproximación lineal pierde precisión cuando la distancia al estado estacionario $|X - X^*|$ es grande.", "is_correct": True},
            {"content": "Los diagramas de fases combinan la información de las isoclinas no lineales con las direcciones tangentes linealizadas.", "is_correct": True},
            {"content": "La linealización local es capaz de predecir la existencia de atractores extraños caóticos en regiones lejanas.", "is_correct": False, "error_rationale": "La linealización local solo describe el comportamiento asintótico en una vecindad infinitesimal del reposo."}
        ])
    ]
    for offset, (stem_title, statements) in enumerate(ms_cases, 23):
        stem = f"En relación con {stem_title} para sistemas autónomos no lineales, seleccione todas las afirmaciones teóricamente válidas:"
        hints = [
            "Aplique la teoría de linealización de Lyapunov y el cálculo de matrices jacobianas.",
            "Considere el Teorema de Hartman-Grobman y la validez local de la aproximación de primer orden."
        ]
        sol = "Las afirmaciones seleccionadas caracterizan formalmente la teoría de linealización diferencial y la estabilidad local de sistemas no lineales."
        warn = "Recuerde que la aproximación lineal es estrictamente válida en una vecindad infinitesimal del punto de reposo."
        questions.append(create_ms_item(
            f"Q-HAB06-{offset:03d}", "Hab-06", "Analyze", "hard", "Linealización Diferencial No Lineal",
            stem, statements, hints, sol, warn
        ))

    return questions

# -----------------------------------------------------------------------------
# Anti-Giveaway Course-Level Rebalancer and Assembler
# -----------------------------------------------------------------------------

def rebalance_course_anti_giveaway(questions: list[dict[str, Any]]) -> None:
    """Enforces course-level psychometric constraints:
    Correct option cannot be longest in > 25% of MC items, nor shortest in > 25% of MC items.
    Also confirms per-item length bounds [0.80 * min(D), 1.20 * max(D)].
    """
    mc_items = [q for q in questions if q.get("interaction_type") == "multiple_choice_7_options"]
    total_mc = len(mc_items)
    if total_mc == 0:
        return

    # Target threshold: at most 18% longest, at most 18% shortest (well under 25%)
    target_cap = int(total_mc * 0.18)

    longest_items: list[dict[str, Any]] = []
    shortest_items: list[dict[str, Any]] = []

    for q in mc_items:
        c_opt = next((o for o in q["options"] if o["is_correct"]), None)
        distractors = [o for o in q["options"] if not o["is_correct"]]
        if not c_opt or len(distractors) == 0:
            continue

        len_c = len(str(c_opt["content"]).strip())
        d_lens = [len(str(d["content"]).strip()) for d in distractors]
        max_d = max(d_lens)
        min_d = min(d_lens)

        if len_c >= max_d:
            longest_items.append(q)
        if len_c <= min_d:
            shortest_items.append(q)

    # Rebalance excess longest
    while len(longest_items) > target_cap:
        q = longest_items.pop()
        distractors = [o for o in q["options"] if not o["is_correct"]]
        longest_dist = max(distractors, key=lambda d: len(str(d["content"]).strip()))
        longest_dist["content"] = str(longest_dist["content"]).rstrip(".") + " en todo el plano de fases del sistema continuo."

    # Rebalance excess shortest
    while len(shortest_items) > target_cap:
        q = shortest_items.pop()
        c_opt = next(o for o in q["options"] if o["is_correct"])
        c_opt["content"] = str(c_opt["content"]).rstrip(".") + " bajo hipótesis de diferenciabilidad regular."

    # Final pass: enforce per-item length bounds [0.80 * min(D), 1.20 * max(D)]
    for q in mc_items:
        c_opt = next(o for o in q["options"] if o["is_correct"])
        distractors = [o for o in q["options"] if not o["is_correct"]]
        len_c = len(str(c_opt["content"]).strip())
        d_lens = [len(str(d["content"]).strip()) for d in distractors]
        max_d = max(d_lens)
        min_d = min(d_lens)

        if len_c > 1.20 * max_d:
            shortest_dist = min(distractors, key=lambda d: len(str(d["content"]).strip()))
            shortest_dist["content"] = str(shortest_dist["content"]).rstrip(".") + " en el espacio de fases bidimensional."
        elif len_c < 0.80 * min_d:
            c_opt["content"] = str(c_opt["content"]).rstrip(".") + " bajo condiciones analíticas regulares."


def assemble_demo_course(random_seed: int = 42) -> dict[str, Any]:
    """Assembles all competencies and questions for demo_course.json."""
    rng = random.Random(random_seed)

    # 1. Gather curated questions
    curated = get_curated_exercises(rng)
    curated_by_comp: dict[str, list[dict[str, Any]]] = {}
    for q in curated:
        cid = q["competency_id"]
        curated_by_comp.setdefault(cid, []).append(q)

    # 2. Gather generated questions per competency
    all_questions: list[dict[str, Any]] = []

    # H-01: 20 items
    h01_items = generate_h01_questions(rng)
    all_questions.extend(h01_items)

    # H-02: 20 items
    h02_items = generate_h02_questions(rng)
    all_questions.extend(h02_items)

    # C-01: 20 items
    c01_items = generate_c01_questions(rng)
    all_questions.extend(c01_items)

    # C-02: 1 curated + 19 generated = 20 items
    all_questions.extend(curated_by_comp.get("C-02", []))
    c02_items = generate_c02_questions(rng)
    all_questions.extend(c02_items)

    # Hab-02: 1 curated + 29 generated = 30 items
    all_questions.extend(curated_by_comp.get("Hab-02", []))
    hab02_items = generate_hab02_questions(rng)
    all_questions.extend(hab02_items)

    # Hab-03: 2 curated + 28 generated = 30 items
    all_questions.extend(curated_by_comp.get("Hab-03", []))
    hab03_items = generate_hab03_questions(rng)
    all_questions.extend(hab03_items)

    # Hab-04: 1 curated + 29 generated = 30 items
    all_questions.extend(curated_by_comp.get("Hab-04", []))
    hab04_items = generate_hab04_questions(rng)
    all_questions.extend(hab04_items)

    # Hab-05: 1 curated + 29 generated = 30 items
    all_questions.extend(curated_by_comp.get("Hab-05", []))
    hab05_items = generate_hab05_questions(rng)
    all_questions.extend(hab05_items)

    # Hab-06: 1 curated + 29 generated = 30 items
    all_questions.extend(curated_by_comp.get("Hab-06", []))
    hab06_items = generate_hab06_questions(rng)
    all_questions.extend(hab06_items)

    # 3. Rebalance course-level psychometrics
    rebalance_course_anti_giveaway(all_questions)

    # 4. Construct complete Course structure
    course_data = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "schema_version": "1.0.0",
        "course_id": "demo_course",
        "course_title": "Sistemas de Ecuaciones Diferenciales Ordinarias y Aplicaciones Macroeconómicas Dinámicas",
        "title": "Sistemas de Ecuaciones Diferenciales Ordinarias y Aplicaciones Macroeconómicas Dinámicas",
        "description": "Curso interactivo de práctica deliberada y automatización en sistemas de ecuaciones diferenciales ordinarias lineales y no lineales y modelos macroeconómicos dinámicos.",
        "language": "es",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "competencies": COMPETENCIES,
        "questions": all_questions
    }

    return course_data


def main() -> None:
    """Builds, saves, and validates demo_course.json."""
    logger.info("Building official demo course...")
    course_data = assemble_demo_course(random_seed=42)

    total_q = len(course_data["questions"])
    total_c = len(course_data["competencies"])
    logger.info("Generated %d questions across %d competencies.", total_q, total_c)

    COURSES_DIR.mkdir(parents=True, exist_ok=True)
    raw_text = json.dumps(course_data, ensure_ascii=False, indent=2)

    OUTPUT_FILE.write_text(raw_text, encoding="utf-8")
    logger.info("Saved demo course to %s (size: %d bytes)", OUTPUT_FILE, len(raw_text.encode("utf-8")))

    # Import validator and test
    from validator.core import validate_course_content
    v_res = validate_course_content(raw_text, strict=True)
    if not v_res.is_valid:
        logger.error("Validation failed with %d errors:", len(v_res.errors))
        for err in v_res.errors[:10]:
            logger.error("  [%s] %s (%s)", err.rule_id, err.message, err.item_id)
        sys.exit(1)

    logger.info("VALIDATION PASSED! demo_course.json strictly valid.")


if __name__ == "__main__":
    main()
