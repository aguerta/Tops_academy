"""Reproducible C2C canonical course builder for Milestone 20 Core.

Compiles the 4 canonical San Marcos / Eloy Ávalos Microeconomics cases from
FUTURE_MILESTONES.md + concept_matching + FIB ds + invariant_canvas (cartesian & tree)
through the real Content-to-Course pipeline:
  compile_cta -> compile_shard(strict=True) -> check_templates_file_or_dir(strict=True)
  -> instantiate_competency -> validate_course_content(strict=True) -> run_full_audit

Writes output strictly inside tests/fixtures/m20_canonical_cases/ (NEVER into courses/).
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
C2C_DIR = ROOT_DIR / ".agents" / "skills" / "content-to-course"
QA_DIR = ROOT_DIR / ".agents" / "skills" / "course-qa-evaluator" / "scripts"
SRC_DIR = ROOT_DIR / "src"

for p in (str(ROOT_DIR), str(C2C_DIR), str(QA_DIR), str(SRC_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

from compile_cta import compile_cta
from compile_shard import compile_shard
from check_templates import check_templates_file_or_dir
from engine.instantiate import instantiate_competency
from validator.core import validate_course_content
from standardized_audit_engine import run_full_audit


CTA_DATA_PY = r'''COURSE_ID = "m20_canonical_course"
COURSE_TITLE = "Microeconomía Avanzada M20 (Casos Canónicos)"
MACRO_COMPETENCY = "Modelado formal, demostraciones paso a paso, análisis de no convexidad y refutación adversarial sin descarte."
CONTRACT_VERSION = 2

COMPETENCIES = [
    (
        "skill",
        "Hab-01",
        "Trampas de Segundo Orden y Rendimientos Crecientes",
        r"Auditoría de concavidad y extremos locales para firmas competitivas con costo $c(x) = a\sqrt{x} + F$ y $\pi''(x) > 0$.",
        "Analyze",
        "microeconomia_casos_canonicos.pdf",
        12,
        [],
        [
            ("Confusion Variable Exogena", r"Asumir que el precio competitivo $p$ es controlado por la firma o que el producto $x$ es fijo.", r"Distinguir la variable de decisión endógena $x$ de los parámetros exógenos $(p, F)$.", r"$x = \text{cte}$", "Identifica qué elige la firma frente a los parámetros fijos que toma pasivamente del mercado.", "Omitir la clasificación previa entre variables de decisión endógenas y parámetros exógenos dados."),
            ("Inversion Segundo Orden", r"Suponer que la condición de primer orden $p = CMg(x)$ garantiza un máximo de beneficios sin evaluar $\pi''(x)$.", r"Con $c''(x) < 0$ se tiene $\pi''(x) = -c''(x) > 0$, por lo que la tangencia corresponde a un mínimo local.", r"$\pi''(x) < 0$", "Evalúa explícitamente el signo de la segunda derivada de la función de beneficios antes de concluir.", "Omitir la verificación de la condición de segundo orden pi''(x) < 0 tras anular la primera derivada."),
            ("Signo Derivada Marginal", r"Derivar $\sqrt{x}$ introduciendo un signo negativo o aplicando incorrectamente la regla del exponente.", r"La derivada de $a\sqrt{x}$ es positiva e igual a $\frac{a}{2\sqrt{x}}$.", r"$-\frac{k}{\sqrt{x}}$", r"Revisa paso a paso la regla de derivación de potencias fraccionarias para el exponente $x^{1/2}$."),
            ("Confusion Costo Total Marginal", r"Reportar el costo variable total $a\sqrt{x}$ en lugar del costo marginal derivado $c'(x)$.", r"El costo marginal es la primera derivada $c'(x) = \frac{a}{2\sqrt{x}}$.", r"$a\sqrt{x}$", "Deriva completamente la función de costo total respecto a la cantidad $x$ antes de sustituir valores."),
            ("Minimo Como Maximo", "Reportar el beneficio negativo del punto crítico estacionario pensando que maximiza las utilidades.", "Has maximizado las pérdidas en el mínimo local; con costo marginal decreciente, expandir la escala eleva el beneficio.", r"$\pi(x_{\text{stat}})$", r"Compara el beneficio en $\pi(x_{\text{stat}})$ frente a un nivel de producción suficientemente expandido."),
            ("Omision Costo Fijo", r"Omitir el costo fijo $F$ al computar el beneficio total $\pi(x) = px - c(x)$.", r"El beneficio total siempre deduce tanto el costo variable $a\sqrt{x}$ como el costo fijo $F$.", r"$px - a\sqrt{x}$", "Recuerda restar el término constante del costo fijo $F$ al computar el beneficio neto total.", "Omitir la deducción del costo fijo F al evaluar el beneficio neto total de la firma."),
        ],
        [
            ("No negatividad productiva", r"$x > 0$ para que $c'(x)$ esté bien definido.", "Exige dominio abierto positivo en el cálculo marginal.", r"División por cero o indeterminación en $x = 0$."),
            ("Precio competitivo dado", r"$p > 0$ exógeno para la empresa precio-aceptante.", "Fija ingreso marginal constante igual a $p$.", r"Si $p$ dependiera de $x$ cambiaría la CPO."),
        ],
        ["unstructured_model", "open_symbolic", "fill_in_the_blank", "adversarial_break"],
    ),
    (
        "skill",
        "Hab-02",
        "Restricción Presupuestaria No Convexa con Descuento por Volumen",
        r"Análisis geométrico y de optimalidad global bajo quiebre no convexo en $\bar{x}_1$ con precio efectivo $p_1(1-r)$.",
        "Evaluate",
        "microeconomia_casos_canonicos.pdf",
        24,
        ["Hab-01"],
        [
            ("Descuento En Tramo Inicial", "Aplicar el descuento porcentual directamente sobre el precio del tramo inicial o confundir $r$ con $(1-r)$.", r"El precio efectivo tras superar $\bar{x}_1$ es $p_1(1-r)$ exclusivamente sobre unidades marginales.", r"$p_1 \cdot r$", "Distingue cuidadosamente la fracción descontada $r$ frente al factor de precio efectivamente pagado $(1-r)$."),
            ("Omision Gasto Bloque Previo", r"Evaluar el gasto total del Tramo B como $p_1(1-r)x_1$ omitiendo el pago completo $p_1\bar{x}_1$ del primer bloque.", r"Para $x_1 > \bar{x}_1$ el gasto es $p_1\bar{x}_1 + p_1(1-r)(x_1 - \bar{x}_1)$.", r"$p_1 x_1$", r"Suma siempre el costo exacto de las primeras $\bar{x}_1$ unidades antes de agregar el costo del exceso.", "Omitir el pago íntegro p1 * x_bar del primer tramo al expresar el gasto del segundo segmento."),
            ("Lagrangiano Global Unico", "Aplicar condiciones KKT o Lagrangiano clásico asumiendo unicidad de tangencia en un conjunto no convexo.", "Con un quiebre no convexo pueden existir dos tangencias locales y un candidato de vértice que deben compararse.", r"$\text{Óptimo único}$", r"Compara explícitamente las utilidades en $u(x^A)$, el vértice $u(x^{\text{kink}})$ y el segundo tramo $u(x^B)$.", "Omitir la comparación global entre tangencias locales y la condición de esquina en conjuntos no convexos."),
            ("Condicion Esquina Quiebre", r"Ignorar el rango de pendientes $p_1(1-r) \le TMS(x^{\text{kink}}) \le p_1$ o ubicar el óptimo fuera del vértice.", r"En el punto de quiebre $\bar{x}_1$ el vértice no diferenciable es óptimo si la $TMS$ yace entre ambas pendientes.", r"$TMS \neq p_1$", "Verifica la inclusión de la $TMS$ dentro del cono normal delimitado por las pendientes derecha e izquierda."),
            ("Inversion Rol Presupuesto", "Confundir el parámetro exógeno de descuento o renta con la variable de elección endógena.", "Solo las cantidades de consumo $(x_1, x_2)$ son variables de decisión endógenas del hogar.", r"$r = \text{endógena}$", "Diferencia con precisión las variables de elección del consumidor frente a los precios e ingreso exógenos."),
            ("Continuidad Demanda No Convexa", "Suponer que la demanda marshalliana $x_1(p,m)$ es continua al cruzar el umbral crítico de renta.", "Un aumento marginal del ingreso $m$ provoca un salto discreto del óptimo desde el Tramo A al Tramo B.", r"$x_1(m) \text{ continua}$", "Observa cómo ocurre el salto discontinuo entre dos tangencias locales al incrementar gradualmente el presupuesto."),
        ],
        [
            ("Descuento marginal por bloque", r"El descuento $r \in (0,1)$ aplica solo a las unidades $x_1 > \bar{x}_1$.", r"Genera un ángulo entrante no convexo en $(\bar{x}_1, m - p_1\bar{x}_1)$.", r"Si aplicara a todas las unidades habría salto vertical."),
            ("Preferencias estrictamente convexas", r"Curvas de indiferencia suaves y estrictamente convexas.", "Garantiza comparación finita entre dos tangencias locales y el vértice.", r"Sin convexidad de preferencias habría soluciones de esquina triviales."),
        ],
        ["invariant_canvas", "open_symbolic", "proof_dag", "unstructured_model"],
    ),
    (
        "concept",
        "C-01",
        "Ruptura Axiomática en Contorno Superior y Árboles Extensivos",
        r"Refutación por contraejemplo de la cuasiconcavidad en $u(x_1, x_2) = \lfloor x_1 \rfloor + \lfloor x_2 \rfloor$ y particiones de información imperfecta.",
        "Evaluate",
        "microeconomia_casos_canonicos.pdf",
        38,
        ["Hab-01"],
        [
            ("Canasta Fuera Contorno", r"Proponer canastas base $A$ o $B$ que no satisfacen la cota requerida $u(\cdot) \ge k$ del contorno superior.", "Ambos puntos extremos $A$ y $B$ deben pertenecer primero al conjunto contorno superior $MI$.", r"$u(A) < k$", r"Comprueba primero que $\lfloor a_1 \rfloor + \lfloor a_2 \rfloor \ge k$ y que ocurra lo mismo con la canasta $B$."),
            ("Combinacion Convexa Interior", r"Elegir dos canastas cuyo punto medio $0.5A + 0.5B$ aún cumple $u(M) \ge k$, fallando en refutar convexidad.", r"Un contraejemplo válido exhibe $u(A) \ge k$ y $u(B) \ge k$ mientras la media cae a $u(M) < k$.", r"$u(M) \ge k$", "Busca coordenadas enteras escalonadas cuya semisuma exactamente trunque por debajo de la cota requerida."),
            ("Subhistoria Arbol Extensivo", "Seleccionar una trayectoria estratégica inconsistente con las ramas de equilibrio o el nodo inicial.", "Las ramas seleccionadas en el árbol extensivo deben formar una trayectoria válida de equilibrio.", r"$\text{Rama inválida}$", "Verifica qué nodo de decisión inicial conduce a la trayectoria terminal óptima especificada en el enunciado."),
            ("Omision Conjunto Informacion", "Tratar los nodos del segundo jugador como observables entre sí omitiendo el conjunto de información.", "La información imperfecta requiere agrupar los nodos indistinguibles en un único conjunto de información.", r"$\text{Info perfecta}$", "Agrupa los dos nodos de decisión indistinguibles del Jugador 2 dentro de un mismo conjunto de información."),
            ("Tratamiento Continuo Piso", r"Evaluar $u(x_1, x_2)$ como la suma lineal continua $x_1 + x_2$ ignorando el truncamiento del operador piso.", r"El operador $\lfloor x_i \rfloor$ retorna el mayor entero menor o igual a $x_i$, descartando decimales.", r"$x_1 + x_2$", "Aplica el truncamiento entero inferior a cada coordenada fraccionaria por separado antes de efectuar la suma."),
            ("Redondeo Techo Erroneo", r"Redondear hacia arriba mediante función techo $\lceil x_i \rceil$ en lugar de truncar hacia abajo con $\lfloor x_i \rfloor$.", "Para fraccionarios no enteros positivos, la función piso queda una unidad por debajo de la función techo.", r"$\lceil x_1 \rceil + \lceil x_2 \rceil$", r"Recuerda que el operador parte entera trunca hacia abajo (por ejemplo $\lfloor 2.7 \rfloor = 2$, nunca $3$)."),
        ],
        [
            ("Discontinuidad de escalera", r"$u(x_1,x_2)=\lfloor x_1\rfloor+\lfloor x_2\rfloor$ es discontinua en enteros.", "Invalida criterios diferenciales basados en hessiano orlado.", r"El análisis debe operar directo sobre conjuntos de contorno superior."),
        ],
        ["adversarial_break", "invariant_canvas", "concept_matching", "fill_in_the_blank"],
    ),
    (
        "concept",
        "C-02",
        "Deducción Analítica de la Identidad de Roy vía Dualidad",
        r"Derivación formal de la demanda marshalliana desde $m \equiv e(p, v(p,m))$ combinando regla de la cadena y Lema de Shephard.",
        "Evaluate",
        "microeconomia_casos_canonicos.pdf",
        51,
        ["Hab-02", "C-01"],
        [
            ("Error Signo Positivo Roy", r"Despejar la demanda marshalliana con signo positivo $+\frac{\partial v/\partial p_i}{\partial v/\partial m}$ omitiendo el signo negativo.", r"Al despejar desde $0 = \partial e/\partial p_i + (\partial e/\partial u)(\partial v/\partial p_i)$, surge necesariamente el signo negativo.", r"$+\frac{v_p}{v_m}$", "Vigila cuidadosamente el cambio de signo al pasar el término derivado respecto al precio al lado opuesto."),
            ("Supuesto Utilidad Marginal Unitaria", r"Asumir implícitamente $\partial e/\partial u = 1$ sin derivar la identidad respecto a la renta $m$.", r"Diferenciar $m \equiv e(p, v(p,m))$ respecto a $m$ demuestra que $\partial e/\partial u = (\partial v/\partial m)^{-1}$.", r"$\partial e/\partial u = 1$", "Deriva explícitamente ambos miembros de la identidad de gasto $e(p, v(p,m)) = m$ respecto a la renta $m$."),
            ("Inversion Cociente Roy", r"Invertir numerador y denominador escribiendo $-\frac{\partial v/\partial m}{\partial v/\partial p_i}$ al despejar de la identidad.", "La demanda marshalliana coloca la derivada respecto al precio en el numerador y respecto a la renta en el denominador.", r"$-\frac{v_m}{v_p}$", "Verifica el análisis dimensional: derivada respecto al precio dividida entre utilidad marginal del ingreso."),
            ("Confusion Shephard Roy", r"Identificar erróneamente el cociente $-\frac{\partial v/\partial p_i}{\partial v/\partial m}$ como demanda hicksiana en vez de marshalliana.", r"El Lema de Shephard $\partial e/\partial p_i$ da $x_i^h(p,u)$, mientras la Identidad de Roy entrega $x_i^d(p,m)$.", r"$x_i^h = -\frac{v_p}{v_m}$", "Distingue con claridad la función de gasto $e(p,u)$ de la función de utilidad indirecta $v(p,m)$."),
            ("Omision Lema Shephard", r"Sustituir $\partial e/\partial p_i$ sin invocar formalmente el Lema de Shephard $\partial e/\partial p_i = x_i^h(p, u)$.", "El paso puente indispensable iguala la derivada parcial del gasto mínimo respecto al precio con la demanda compensada.", r"$\partial e/\partial p_i \neq x_i^h$", "Aplica el teorema de la envolvente al problema de minimización del gasto para invocar el Lema de Shephard."),
            ("Confusion Homogeneidad Dual", r"Confundir la identidad $e(p, v(p,m)) \equiv m$ con homogeneidad de grado uno de $v$ en la renta.", "La función $v(p,m)$ es homogénea de grado cero en $(p,m)$, mientras $e(p,u)$ recupera exactamente $m$.", r"$e(p,v)=u$", "Recuerda la relación inversa directa entre el gasto mínimo $e(p,u)$ y la función de utilidad indirecta $v(p,m)$."),
        ],
        [
            ("No saciacion local y diferenciabilidad", r"$e(p,u)$ y $v(p,m)$ diferenciables con $\partial v/\partial m > 0$.", r"Asegura divisor estrictamente positivo $\partial v/\partial m \neq 0$ al despejar.", r"Si $\partial v/\partial m = 0$ no puede aplicarse la Identidad de Roy."),
        ],
        ["proof_dag", "open_symbolic", "concept_matching", "multiple_choice_7_options"],
    ),
]
'''


SHARD_01_DATA_PY = r'''# Shard 01 Data — 4 Casos Canónicos de Milestone 20 Core (16 plantillas, 4 arquetipos c/u)
import math


# ==============================================================================
# COMPETENCIA Hab-01 (Skill — Caso 1: Rendimientos Crecientes c(x) = a*sqrt(x) + F)
# ==============================================================================

def gen_hab01_stage0(rng):
    k = rng.randint(2, 10)
    a = 2 * k
    F = rng.randint(15, 75)
    p = rng.randint(2, 12)
    um = {
        "phase1_variables": {
            "prompt": "Clasifica cada símbolo de la firma competitiva con tecnología $c(x) = @a@\\sqrt{x} + @F@$ antes de derivar:",
            "roles": ["Variable de decisión endógena", "Parámetro exógeno de mercado", "Costo fijo exógeno"],
            "items": [
                {
                    "id": "V_x",
                    "label": "Cantidad producida $x$",
                    "correct_role": "Variable de decisión endógena",
                    "distractor_id": "D-Hab01-01",
                    "error_rationale": "Confusión estructural: la firma elige libremente el nivel productivo $x$ con parámetro de costo @a@ y fijo @F@.",
                },
                {
                    "id": "V_p",
                    "label": "Precio competitivo $p = @p@$",
                    "correct_role": "Parámetro exógeno de mercado",
                    "error_rationale": "Una empresa precio-aceptante toma el precio de mercado $p = @p@$ como dato exógeno independiente de $x$.",
                },
                {
                    "id": "V_F",
                    "label": "Costo fijo $F = @F@$",
                    "correct_role": "Costo fijo exógeno",
                    "error_rationale": "El monto constante $F = @F@$ representa un costo fijo invariante frente al volumen producido $x$.",
                },
            ],
        },
        "phase2_assumptions": {
            "prompt": "Audita la tecnología $c(x) = @a@\\sqrt{x} + @F@$ y marca los supuestos activos:",
            "options": [
                {
                    "id": "A_ir",
                    "content": "Rendimientos crecientes: costo marginal decreciente $c''(x) < 0$ para todo $x > 0$.",
                    "is_required": True,
                },
                {
                    "id": "A_conv",
                    "content": r"La segunda derivada del beneficio satisface $\pi''(x) = -c''(x) > 0$ (convexidad).",
                    "is_required": True,
                },
                {
                    "id": "A_conc",
                    "content": r"Concavidad estándar garantizada: $\pi''(x) < 0$ en todo el dominio productivo.",
                    "is_required": False,
                    "distractor_id": "D-Hab01-02",
                    "error_rationale": "Suponer $\\pi''(x) < 0$ cuando $c(x) = @a@\\sqrt{x} + @F@$ invierte el signo de curvatura de segundo orden.",
                },
            ],
        },
        "phase3_formulation": {
            "prompt": "Dictamina la naturaleza del punto estacionario $p = CMg(x)$ antes de despejar:",
            "input_mode": "select",
            "options": [
                {
                    "id": "F_min",
                    "content": r"El punto crítico $p = CMg(x)$ constituye un mínimo local de beneficios ($\pi''(x) > 0$).",
                    "is_correct": True,
                },
                {
                    "id": "F_max",
                    "content": r"El punto crítico $p = CMg(x)$ determina el óptimo competitivo máximo con beneficio positivo.",
                    "is_correct": False,
                    "distractor_id": "D-Hab01-02",
                    "error_rationale": "Aplicar el criterio de primer orden con $c(x) = @a@\\sqrt{x} + @F@$ sin chequear $\\pi''(x) > 0$ maximiza las pérdidas.",
                },
            ],
        },
    }
    return {"vars": {"a": a, "F": F, "p": p}, "unstructured_model": um}


def ver_hab01_stage0(res):
    um = res.get("unstructured_model") if isinstance(res, dict) else None
    v = res.get("vars", {}) if isinstance(res, dict) else {}
    if not isinstance(um, dict) or not v.get("a"):
        return False
    req = [o["id"] for o in um["phase2_assumptions"]["options"] if o.get("is_required")]
    corr_p3 = [o["id"] for o in um["phase3_formulation"]["options"] if o.get("is_correct")]
    return req == ["A_ir", "A_conv"] and corr_p3 == ["F_min"]


def gen_hab01_open_sym(rng):
    k = rng.randint(2, 26)
    a = 2 * k
    F = rng.randint(10, 65)
    ans = f"{k}/sqrt(x)"
    return {
        "vars": {"k": k, "a": a, "F": F},
        "correct": ans,
        "accepted_equivalents": [ans, f"{k}*x^(-1/2)", f"{a}/(2*sqrt(x))"],
        "variables": ["x"],
        "symbolic_config": {
            "variables": ["x"],
            "palette": ["sqrt()", "^", "/", "+", "-"],
            "placeholder": "Ej: 5/sqrt(x)",
        },
        "ds": [
            ("D-Hab01-03", f"-{k}/sqrt(x)", r"Error de signo al derivar $c(x) = @a@\sqrt{x} + @F@$: el costo marginal $\frac{@k@}{\sqrt{x}}$ es estrictamente positivo."),
            ("D-Hab01-04", f"{a}*sqrt(x)", r"Reportaste el componente de costo variable $@a@\sqrt{x}$ sin diferenciar respecto al nivel productivo $x$ con $F=@F@$."),
        ],
    }


def ver_hab01_open_sym(res):
    c = str(res.get("correct", "")) if isinstance(res, dict) else str(res)
    v = res.get("vars", {}) if isinstance(res, dict) else {}
    k = v.get("k")
    return bool(k) and c.strip() == f"{k}/sqrt(x)"


def gen_hab01_fib_profit(rng):
    k = rng.randint(1, 6)
    a = 2 * k
    p = rng.randint(2, 5)
    F = rng.randint(8, 45)
    min_m = (k // p) + 4
    m_hi = rng.randint(min_m, min_m + 18)
    x_hi = m_hi * m_hi
    pi_hi = int(p * x_hi - a * m_hi - F)
    x_stat = round((k / p) ** 2, 2)
    pi_stat = round(-(k * k) / p - F, 2)
    pi_no_f = int(p * x_hi - a * m_hi)
    return {
        "vars": {"a": a, "k": k, "p": p, "F": F, "x_hi": x_hi, "m_hi": m_hi, "x_stat": x_stat, "pi_hi": pi_hi, "pi_stat": pi_stat, "pi_no_f": pi_no_f},
        "correct": str(pi_hi),
        "ds": [
            ("D-Hab01-05", str(pi_stat), r"Has maximizado las pérdidas en el mínimo local $x_{\text{stat}} = @x_stat@$. Con CMg decreciente, expandir a $x = @x_hi@$ supera $@pi_stat@$."),
            ("D-Hab01-06", str(pi_no_f), r"Omitiste restar el costo fijo $F = @F@$ al reportar $@pi_no_f@$ en escala $x = @x_hi@$ bajo $p = @p@$."),
        ],
    }


def ver_hab01_fib_profit(res):
    c = str(res.get("correct", "")) if isinstance(res, dict) else str(res)
    v = res.get("vars", {}) if isinstance(res, dict) else {}
    try:
        expected = int(v["p"] * v["x_hi"] - v["a"] * v["m_hi"] - v["F"])
        return abs(float(c) - expected) < 1e-6
    except Exception:
        return False


def gen_hab01_adv(rng):
    b = rng.randint(2, 12)
    b_dbl = 2 * b
    F = rng.randint(10, 50)
    p_val = rng.randint(2, 8)
    adv = {
        "mode": "find_fallacy",
        "prompt": "Audita la siguiente resolución competitiva e identifica el paso donde quiebra la deducción:",
        "steps": [
            {
                "id": "A1",
                "label": "Paso 1",
                "content": r"Definición del beneficio competitivo: $\pi(x) = @p_val@x - (@b_dbl@\sqrt{x} + @F@)$.",
                "is_fallacy": False,
                "valid_explanation": "La función objetivo resta correctamente el costo total $c(x)$ al ingreso competitivo.",
            },
            {
                "id": "A2",
                "label": "Paso 2",
                "content": r"Igualdad de primer orden: $\frac{d\pi}{dx} = @p_val@ - \frac{@b@}{\sqrt{x}} = 0 \implies x_{\text{stat}} = \left(\frac{@b@}{@p_val@}\right)^2$.",
                "is_fallacy": False,
                "valid_explanation": "La derivación algebraica de la condición de primer orden es aritméticamente correcta.",
            },
            {
                "id": "A3",
                "label": "Paso 3",
                "content": r"Por anularse el beneficio marginal, $x_{\text{stat}}$ maximiza globalmente las utilidades competitivas de la empresa.",
                "is_fallacy": True,
                "distractor_id": "D-Hab01-02",
                "error_rationale": "Falla crítica de segundo orden en $c(x)=@b_dbl@\\sqrt{x}+@F@$: como $\\pi''(x) = \\frac{@b@}{2x^{3/2}} > 0$, la tangencia es un mínimo local.",
            },
            {
                "id": "A4",
                "label": "Paso 4",
                "content": r"Evaluación en la escala crítica sustituyendo $p = @p_val@$ y costo fijo $F = @F@$.",
                "is_fallacy": False,
            },
        ],
        "reason_options": [
            {
                "id": "R_cs",
                "content": r"La condición de segundo orden verifica $\pi''(x) > 0$, invirtiendo el extremo en mínimo local de beneficios.",
                "is_correct": True,
            },
            {
                "id": "R_sig",
                "content": r"La derivada de $\sqrt{x}$ debía llevar coeficiente negativo duplicado en la CPO para $b = @b@$.",
                "is_correct": False,
                "distractor_id": "D-Hab01-03",
                "error_rationale": "El cálculo de $d/dx(@b_dbl@\\sqrt{x}) = @b@/\\sqrt{x}$ es exacto; el error reside en omitir $\\pi''(x) > 0$.",
            },
            {
                "id": "R_cf",
                "content": r"Se omitió derivar la constante del costo fijo $F = @F@$ dentro de la expresión de costo marginal.",
                "is_correct": False,
                "distractor_id": "D-Hab01-06",
                "error_rationale": "La derivada de la constante fija $@F@$ respecto a $x$ es cero; el fallo real es de concavidad en el Paso 3.",
            },
        ],
    }
    return {"vars": {"b": b, "b_dbl": b_dbl, "F": F, "p_val": p_val}, "adversarial_break": adv}


def ver_hab01_adv(res):
    adv = res.get("adversarial_break") if isinstance(res, dict) else None
    if not isinstance(adv, dict):
        return False
    f_steps = [s["id"] for s in adv.get("steps", []) if s.get("is_fallacy")]
    r_corr = [r["id"] for r in adv.get("reason_options", []) if r.get("is_correct")]
    return f_steps == ["A3"] and r_corr == ["R_cs"]


# ==============================================================================
# COMPETENCIA Hab-02 (Skill — Caso 2: Restricción Presupuestaria No Convexa)
# ==============================================================================

def gen_hab02_canvas_cart(rng):
    p1 = rng.choice([2, 4])
    r_pct = 50 if p1 == 2 else rng.choice([25, 50])
    p1_disc = int(p1 * (100 - r_pct) // 100)
    x_bar = rng.randint(3, 8)
    x2_kink = rng.randint(4, 15)
    m = p1 * x_bar + x2_kink
    ic = {
        "mode": "cartesian",
        "x_range": [0, 20],
        "y_range": [0, 48],
        "step": 0.5,
        "x_label": "x_1",
        "y_label": "x_2",
        "fixed_curves": [
            {
                "id": "budget",
                "label": r"Restricción con descuento tras $\bar{x}_1 = @x_bar@$",
                "color": "#2563eb",
                "expression": f"x <= {x_bar} ? {m} - {p1}*x : ({m} - {p1}*{x_bar}) - {p1_disc}*(x - {x_bar})",
                "domain": [0, 20],
                "style": "solid",
            }
        ],
        "interactive_points": [
            {
                "id": "pt_kink",
                "label": "Vértice no convexo",
                "x": 1,
                "y": 1,
                "color": "#dc2626",
            }
        ],
        "invariants": [
            {
                "id": "INV_ON",
                "kind": "point_on_curve",
                "point_id": "pt_kink",
                "curve_id": "budget",
                "tolerance": 0.5,
                "distractor_id": "D-Hab02-04",
                "error_rationale": "El punto marcado no yace sobre la restricción presupuestaria no convexa para ingreso $m = @m@$ y umbral $@x_bar@$.",
            },
            {
                "id": "INV_KINK_POS",
                "kind": "point_coords",
                "point_id": "pt_kink",
                "target_x": x_bar,
                "target_y": x2_kink,
                "tolerance": 0.5,
                "distractor_id": "D-Hab02-04",
                "error_rationale": "Ubica exactamente el ángulo entrante no convexo evaluando $(\\bar{x}_1, m - p_1\\bar{x}_1)$ en $\\bar{x}_1 = @x_bar@$ (con $m = @m@$, $p_1 = @p1@$).",
            },
            {
                "id": "INV_KINK_SHAPE",
                "kind": "kink_at",
                "curve_id": "budget",
                "x": x_bar,
                "target": 0.5,
                "distractor_id": "D-Hab02-03",
                "error_rationale": "La restricción debe exhibir cambio estricto de pendiente en $\\bar{x}_1 = @x_bar@$ quebrando la convexidad clásica.",
            },
        ],
        "target_state": {"pt_kink": {"x": x_bar, "y": x2_kink}},
    }
    return {"vars": {"p1": p1, "r_pct": r_pct, "x_bar": x_bar, "m": m}, "invariant_canvas": ic}


def ver_hab02_canvas_cart(res):
    ic = res.get("invariant_canvas") if isinstance(res, dict) else None
    v = res.get("vars", {}) if isinstance(res, dict) else {}
    if not isinstance(ic, dict) or ic.get("mode") != "cartesian":
        return False
    invs = ic.get("invariants", [])
    kpos = next((i for i in invs if i.get("kind") == "point_coords"), None)
    expected_y = v.get("m", 0) - v.get("p1", 0) * v.get("x_bar", 0)
    return kpos is not None and kpos.get("target_x") == v.get("x_bar") and kpos.get("target_y") == expected_y


def gen_hab02_open_sym(rng):
    p1 = rng.randint(2, 42)
    x_bar = rng.randint(3, 18)
    ans = f"{p1}*(1 - r)"
    return {
        "vars": {"p1": p1, "x_bar": x_bar},
        "correct": ans,
        "accepted_equivalents": [ans, f"{p1} - {p1}*r", f"{p1}*(1-r)"],
        "variables": ["r"],
        "symbolic_config": {
            "variables": ["r"],
            "palette": ["(", ")", "*", "-", "+"],
            "placeholder": "Ej: 6*(1 - r)",
        },
        "ds": [
            ("D-Hab02-01", f"{p1}*r", r"Confundiste la fracción descontada $r$ con el precio marginal efectivamente pagado $p_1(1-r)$ tras superar $@x_bar@$ con $p_1 = @p1@$."),
            ("D-Hab02-02", f"{p1}", r"Omitiste aplicar el factor de descuento por volumen $(1-r)$ sobre el precio base $p_1 = @p1@$ para el tramo superior a $@x_bar@$."),
        ],
    }


def ver_hab02_open_sym(res):
    c = str(res.get("correct", "")) if isinstance(res, dict) else str(res)
    v = res.get("vars", {}) if isinstance(res, dict) else {}
    p1 = v.get("p1")
    return bool(p1) and c.replace(" ", "") == f"{p1}*(1-r)"


def gen_hab02_dag(rng):
    x_bar = rng.randint(4, 28)
    p1 = rng.randint(3, 12)
    r_dec = round(rng.choice([0.15, 0.2, 0.25, 0.3, 0.4, 0.5]), 2)
    dag = {
        "goal": "Establecer el óptimo global bajo restricción presupuestaria no convexa:",
        "steps": [
            {
                "id": "K1",
                "content": r"Evaluar el óptimo interior del Tramo A ($x_1 < @x_bar@$) imponiendo $TMS(x^A) = @p1@$.",
                "is_fallacy": False,
            },
            {
                "id": "K2",
                "content": r"Evaluar el óptimo interior del Tramo B ($x_1 > @x_bar@$) imponiendo $TMS(x^B) = @p1@(1 - @r_dec@)$.",
                "is_fallacy": False,
            },
            {
                "id": "K3",
                "content": r"Verificar el candidato de quiebre en $(\bar{x}_1, m - @p1@\cdot @x_bar@)$ vía $@p1@(1-@r_dec@) \le TMS \le @p1@$.",
                "is_fallacy": False,
            },
            {
                "id": "K4",
                "content": r"Elegir globalmente $x^* = \arg\max \{u(x^A), u(x^{\text{kink}}), u(x^B)\}$.",
                "is_fallacy": False,
            },
            {
                "id": "K_BAD",
                "content": r"Plantear un Lagrangiano clásico único asumiendo tangencia interior única en todo el dominio.",
                "is_fallacy": True,
                "distractor_id": "D-Hab02-03",
                "error_rationale": "Falla crítica: ante el ángulo entrante en $\\bar{x}_1 = @x_bar@$ pueden coexistir dos tangencias locales no globales.",
            },
        ],
        "edges": [["K1", "K4"], ["K2", "K4"], ["K3", "K4"]],
        "require_justification": False,
    }
    return {"vars": {"x_bar": x_bar, "p1": p1, "r_dec": r_dec}, "proof_dag": dag}


def ver_hab02_dag(res):
    dag = res.get("proof_dag") if isinstance(res, dict) else None
    if not isinstance(dag, dict):
        return False
    valid_ids = {s["id"] for s in dag.get("steps", []) if not s.get("is_fallacy")}
    fallacy_ids = {s["id"] for s in dag.get("steps", []) if s.get("is_fallacy")}
    return valid_ids == {"K1", "K2", "K3", "K4"} and fallacy_ids == {"K_BAD"}


def gen_hab02_stage0_sym(rng):
    p1 = rng.randint(2, 16)
    x_bar = rng.randint(4, 24)
    expr = f"{p1}*{x_bar} + {p1}*(1-r)*(x1 - {x_bar})"
    um = {
        "phase1_variables": {
            "prompt": "Clasifica las cantidades y parámetros del modelo con descuento tras $\\bar{x}_1 = @x_bar@$:",
            "roles": ["Variable de elección endógena", "Parámetro exógeno"],
            "items": [
                {
                    "id": "U_x1",
                    "label": "Cantidad consumida $x_1$",
                    "correct_role": "Variable de elección endógena",
                    "distractor_id": "D-Hab02-05",
                    "error_rationale": "La cesta de consumo $x_1$ respecto al umbral $@x_bar@$ es decidida por el hogar, no fijada exógenamente.",
                },
                {
                    "id": "U_r",
                    "label": "Tasa de descuento $r$ sobre exceso",
                    "correct_role": "Parámetro exógeno",
                    "error_rationale": "El porcentaje de descuento tarifario $r$ constituye un dato exógeno paramétrico del mercado.",
                },
            ],
        },
        "phase2_assumptions": {
            "prompt": "Marca los supuestos estructurales activos para $x_1 > @x_bar@$:",
            "options": [
                {
                    "id": "S2_blk",
                    "content": r"Las primeras $\bar{x}_1 = @x_bar@$ unidades siempre se pagan a tarifa completa $p_1 = @p1@$.",
                    "is_required": True,
                },
                {
                    "id": "S2_salto",
                    "content": r"Variaciones pequeñas de renta $m$ pueden inducir saltos discontinuos entre tramos.",
                    "is_required": True,
                },
                {
                    "id": "S2_cont",
                    "content": r"La demanda ordinaria resulta estrictamente continua en $m$ pese al quiebre de tarifa.",
                    "is_required": False,
                    "distractor_id": "D-Hab02-06",
                    "error_rationale": "La no convexidad del quiebre en $\\bar{x}_1 = @x_bar@$ provoca discontinuidades de salto al variar la renta $m$.",
                },
            ],
        },
        "phase3_formulation": {
            "prompt": r"Escribe el gasto total en bien 1 para el Tramo B ($x_1 > @x_bar@$) en función de `x1` y `r`:",
            "input_mode": "symbolic",
            "correct_expression": {
                "expression": expr,
                "accepted_equivalents": [expr, f"{p1}*{x_bar} + {p1}*(1 - r)*(x1 - {x_bar})"],
                "tolerance": 0.001,
            },
            "diagnostic_distractors": [
                {
                    "distractor_id": "D-Hab02-01",
                    "expression": f"{p1}*(1-r)*x1",
                    "error_rationale": "Aplicaste el descuento $(1-r)$ retroactivamente a las primeras $@x_bar@$ unidades en lugar de solo al exceso $(x_1 - @x_bar@)$.",
                },
                {
                    "distractor_id": "D-Hab02-02",
                    "expression": f"{p1}*x1",
                    "error_rationale": "Omitiste el descuento marginal $(1-r)$ en las unidades que exceden el umbral de volumen $\\bar{x}_1 = @x_bar@$.",
                },
            ],
        },
    }
    return {"vars": {"p1": p1, "x_bar": x_bar}, "unstructured_model": um}


def ver_hab02_stage0_sym(res):
    um = res.get("unstructured_model") if isinstance(res, dict) else None
    v = res.get("vars", {}) if isinstance(res, dict) else {}
    if not isinstance(um, dict) or not v.get("p1"):
        return False
    p3 = um.get("phase3_formulation", {})
    ce = (p3.get("correct_expression") or {}).get("expression", "")
    expected = f"{v['p1']}*{v['x_bar']} + {v['p1']}*(1-r)*(x1 - {v['x_bar']})"
    return p3.get("input_mode") == "symbolic" and ce == expected


# ==============================================================================
# COMPETENCIA C-01 (Concept — Caso 3: Ruptura Axiomática Contorno Superior y Árbol)
# ==============================================================================

def gen_c01_counterexample(rng):
    k_lvl = rng.randint(3, 35)
    adv = {
        "mode": "counterexample",
        "prompt": r"Para $u(x_1, x_2) = \lfloor x_1 \rfloor + \lfloor x_2 \rfloor$, exhibe un par de canastas $A=(a_1,a_2)$ y $B=(b_1,b_2)$ en el contorno $u \ge @k_lvl@$ cuyo punto medio viole la convexidad del conjunto:",
        "inputs": [
            {"id": "a1", "label": "a_1", "type": "number", "min": 0, "max": 60, "step": 0.1, "placeholder": "Ej: 1.0"},
            {"id": "a2", "label": "a_2", "type": "number", "min": 0, "max": 60, "step": 0.1, "placeholder": f"Ej: {k_lvl - 1}.0"},
            {"id": "b1", "label": "b_1", "type": "number", "min": 0, "max": 60, "step": 0.1, "placeholder": "Ej: 2.0"},
            {"id": "b2", "label": "b_2", "type": "number", "min": 0, "max": 60, "step": 0.1, "placeholder": f"Ej: {k_lvl - 2}.0"},
        ],
        "predicates": [
            {
                "id": "P_A",
                "expr": f"floor(a1) + floor(a2) >= {k_lvl}",
                "distractor_id": "D-C01-01",
                "failure_rationale": "La canasta $A = (a_1, a_2)$ debe pertenecer primero al contorno superior cumpliendo $\\lfloor a_1 \\rfloor + \\lfloor a_2 \\rfloor \\ge @k_lvl@$.",
            },
            {
                "id": "P_B",
                "expr": f"floor(b1) + floor(b2) >= {k_lvl}",
                "distractor_id": "D-C01-01",
                "failure_rationale": "La canasta $B = (b_1, b_2)$ también debe satisfacer la cota del contorno superior $\\lfloor b_1 \\rfloor + \\lfloor b_2 \\rfloor \\ge @k_lvl@$.",
            },
            {
                "id": "P_MID",
                "expr": f"floor(0.5*(a1 + b1)) + floor(0.5*(a2 + b2)) < {k_lvl}",
                "distractor_id": "D-C01-02",
                "failure_rationale": "El punto medio $M = 0.5A + 0.5B$ quedó dentro del contorno $\\ge @k_lvl@$ y por ello no refuta la convexidad.",
            },
        ],
        "sample_witness": {
            "a1": 1.0,
            "a2": float(k_lvl - 1),
            "b1": 2.0,
            "b2": float(k_lvl - 2),
        },
    }
    return {"vars": {"k_lvl": k_lvl}, "adversarial_break": adv}


def ver_c01_counterexample(res):
    adv = res.get("adversarial_break") if isinstance(res, dict) else None
    v = res.get("vars", {}) if isinstance(res, dict) else {}
    if not isinstance(adv, dict) or adv.get("mode") != "counterexample":
        return False
    w = adv.get("sample_witness", {})
    k_lvl = v.get("k_lvl")
    if not isinstance(w, dict) or k_lvl is None:
        return False
    ua = math.floor(w["a1"]) + math.floor(w["a2"])
    ub = math.floor(w["b1"]) + math.floor(w["b2"])
    um = math.floor(0.5 * (w["a1"] + w["b1"])) + math.floor(0.5 * (w["a2"] + w["b2"]))
    return ua >= k_lvl and ub >= k_lvl and um < k_lvl


def gen_c01_tree(rng):
    w1 = rng.randint(5, 30)
    w2 = rng.randint(1, 4)
    ic = {
        "mode": "tree",
        "width": 520,
        "height": 300,
        "interaction_mode": "both",
        "nodes": [
            {"id": "n0", "label": "J1", "x": 80, "y": 150, "player": "J1"},
            {"id": "n1", "label": "J2a", "x": 240, "y": 80, "player": "J2"},
            {"id": "n2", "label": "J2b", "x": 240, "y": 220, "player": "J2"},
            {"id": "t1", "label": "T1", "x": 420, "y": 45, "terminal": True, "payoff": f"({w1}, {w1})"},
            {"id": "t2", "label": "T2", "x": 420, "y": 115, "terminal": True, "payoff": f"({w2}, 0)"},
            {"id": "t3", "label": "T3", "x": 420, "y": 185, "terminal": True, "payoff": f"(0, {w2})"},
            {"id": "t4", "label": "T4", "x": 420, "y": 255, "terminal": True, "payoff": "(1, 1)"},
        ],
        "edges": [
            {"id": "e_top", "from": "n0", "to": "n1", "label": "Cooperar"},
            {"id": "e_bot", "from": "n0", "to": "n2", "label": "Desviar"},
            {"id": "e1", "from": "n1", "to": "t1", "label": "C_2"},
            {"id": "e2", "from": "n1", "to": "t2", "label": "D_2"},
            {"id": "e3", "from": "n2", "to": "t3", "label": "C_2"},
            {"id": "e4", "from": "n2", "to": "t4", "label": "D_2"},
        ],
        "tree_invariants": {
            "required_edges": ["e_top", "e1"],
            "required_info_sets": [["n1", "n2"]],
            "distractor_id": "D-C01-03",
            "distractor_ids": ["D-C01-03", "D-C01-04"],
            "edge_error_rationale": "La senda óptima con pago dominante (@w1@, @w1@) exige activar exactamente las ramas 'Cooperar' y 'C_2' hacia T1.",
            "info_set_error_rationale": "El Jugador 2 no observa la acción previa de J1; debes agrupar sus dos nodos de decisión J2a y J2b en un conjunto de información.",
        },
    }
    return {"vars": {"w1": w1, "w2": w2}, "invariant_canvas": ic}


def ver_c01_tree(res):
    ic = res.get("invariant_canvas") if isinstance(res, dict) else None
    if not isinstance(ic, dict) or ic.get("mode") != "tree":
        return False
    ti = ic.get("tree_invariants", {})
    return sorted(ti.get("required_edges", [])) == ["e1", "e_top"] and ti.get("required_info_sets") == [["n1", "n2"]]


def gen_c01_matching(rng):
    c_lvl = round(rng.uniform(2.0, 9.5), 1)
    cm = {
        "left_title": "Propiedad / Escenario",
        "right_title": "Consecuencia Formal",
        "premises": [
            {"id": "P_cut", "content": r"Corte discontinuo en $u(x_1, x_2) = \lfloor x_1 \rfloor + \lfloor x_2 \rfloor$ con cota @c_lvl@"},
            {"id": "P_hess", "content": r"Intento de aplicar matriz hessiana orlada sobre la utilidad piso"},
            {"id": "P_mid", "content": r"Punto medio $M = 0.5(1, 2) + 0.5(2, 1)$ evaluado bajo escalonamiento"},
        ],
        "targets": [
            {"id": "T_cut", "content": r"Contorno superior formado por unión no convexa de bloques enteros"},
            {"id": "T_hess", "content": r"Método inaplicable por no existir derivadas en discontinuidades enteras"},
            {"id": "T_mid", "content": r"Utilidad caída $u(1.5, 1.5) = 2 < 3$ refutando cuasiconcavidad"},
            {
                "id": "T_dist1",
                "content": r"Cuasiconcavidad estricta preservada alrededor de cota @c_lvl@",
                "is_distractor": True,
                "distractor_id": "D-C01-01",
                "error_rationale": "La función piso quiebra la convexidad de los contornos superiores en cada valor entero independientemente de @c_lvl@.",
            },
            {
                "id": "T_dist2",
                "content": r"Observabilidad perfecta equivalente a juego sin conjuntos de información",
                "is_distractor": True,
                "distractor_id": "D-C01-04",
                "error_rationale": "Un conjunto de información no trivial representa exactamente nodos donde el jugador desconoce la historia previa.",
            },
        ],
        "correct_pairs": {"P_cut": "T_cut", "P_hess": "T_hess", "P_mid": "T_mid"},
    }
    return {"vars": {"c_lvl": c_lvl}, "concept_matching": cm}


def ver_c01_matching(res):
    cm = res.get("concept_matching") if isinstance(res, dict) else None
    if not isinstance(cm, dict):
        return False
    return cm.get("correct_pairs") == {"P_cut": "T_cut", "P_hess": "T_hess", "P_mid": "T_mid"}


def gen_c01_fib(rng):
    i1 = rng.randint(1, 10)
    i2 = rng.randint(1, 10)
    f1 = rng.choice([0.3, 0.4, 0.6, 0.7, 0.8])
    f2 = rng.choice([0.2, 0.4, 0.5, 0.7, 0.9])
    x1 = round(i1 + f1, 1)
    x2 = round(i2 + f2, 1)
    ans = i1 + i2
    cont_sum = round(x1 + x2, 1)
    ceil_sum = i1 + i2 + 2
    return {
        "vars": {"x1": x1, "x2": x2, "ans": ans, "cont_sum": cont_sum, "ceil_sum": ceil_sum},
        "correct": str(ans),
        "ds": [
            ("D-C01-05", str(cont_sum), r"Evaluaste $u(@x1@, @x2@)$ como suma continua lineal (@cont_sum@) omitiendo el operador parte entera $\lfloor x_i \rfloor$."),
            ("D-C01-06", str(ceil_sum), r"Redondeaste hacia arriba con techo $\lceil x_i \rceil$ dando @ceil_sum@; la parte entera trunca hacia abajo a @ans@."),
        ],
    }


def ver_c01_fib(res):
    c = str(res.get("correct", "")) if isinstance(res, dict) else str(res)
    v = res.get("vars", {}) if isinstance(res, dict) else {}
    try:
        expected = math.floor(v["x1"]) + math.floor(v["x2"])
        return abs(float(c) - expected) < 1e-6
    except Exception:
        return False


# ==============================================================================
# COMPETENCIA C-02 (Concept — Caso 4: Deducción Identidad de Roy vía Dualidad)
# ==============================================================================

def gen_c02_dag_roy(rng):
    g_idx = rng.randint(1, 30)
    dag = {
        "goal": r"Derivar analíticamente la Identidad de Roy para el bien $x_{@g_idx@}$ desde $m \equiv e(p, v(p,m))$:",
        "steps": [
            {
                "id": "S1",
                "content": r"Diferenciación respecto a $p_{@g_idx@}$: $0 = \frac{\partial e}{\partial p_{@g_idx@}} + \frac{\partial e}{\partial u}\frac{\partial v}{\partial p_{@g_idx@}}$.",
                "justification": "Regla de la Cadena respecto a p",
                "is_fallacy": False,
            },
            {
                "id": "S2",
                "content": r"Por Lema de Shephard y dualidad: $\frac{\partial e}{\partial p_{@g_idx@}} = x_{@g_idx@}^h(p,u) = x_{@g_idx@}^d(p,m)$.",
                "justification": "Lema de Shephard y dualidad",
                "is_fallacy": False,
            },
            {
                "id": "S3",
                "content": r"Diferenciando respecto a renta $m$: $1 = \frac{\partial e}{\partial u}\frac{\partial v}{\partial m} \implies \frac{\partial e}{\partial u} = \frac{1}{\partial v/\partial m}$.",
                "justification": "Derivación de identidad respecto a m",
                "is_fallacy": False,
            },
            {
                "id": "S4",
                "content": r"Sustitución en la ecuación inicial: $0 = x_{@g_idx@}^d(p,m) + \frac{\partial v/\partial p_{@g_idx@}}{\partial v/\partial m}$.",
                "justification": "Sustitución algebraica dual",
                "is_fallacy": False,
            },
            {
                "id": "S5",
                "content": r"Despeje final (Identidad de Roy): $x_{@g_idx@}^d(p,m) = -\frac{\partial v/\partial p_{@g_idx@}}{\partial v/\partial m}$.",
                "justification": "Despeje de la Identidad de Roy",
                "is_fallacy": False,
            },
            {
                "id": "S_BAD",
                "content": r"Despeje erróneo con signo positivo: $x_{@g_idx@}^d(p,m) = +\frac{\partial v/\partial p_{@g_idx@}}{\partial v/\partial m}$.",
                "justification": "Despeje de la Identidad de Roy",
                "is_fallacy": True,
                "distractor_id": "D-C02-01",
                "error_rationale": "Falta crítica de signo negativo en el bien $x_{@g_idx@}$: pasar el segundo sumando al otro lado invierte el signo a menos.",
            },
        ],
        "edges": [["S1", "S2"], ["S1", "S3"], ["S2", "S4"], ["S3", "S4"], ["S4", "S5"]],
        "require_justification": True,
        "justification_bank": [
            "Regla de la Cadena respecto a p",
            "Lema de Shephard y dualidad",
            "Derivación de identidad respecto a m",
            "Sustitución algebraica dual",
            "Despeje de la Identidad de Roy",
        ],
    }
    return {"vars": {"g_idx": g_idx}, "proof_dag": dag}


def ver_c02_dag_roy(res):
    dag = res.get("proof_dag") if isinstance(res, dict) else None
    if not isinstance(dag, dict):
        return False
    valid_ids = [s["id"] for s in dag.get("steps", []) if not s.get("is_fallacy")]
    fallacy_ids = [s["id"] for s in dag.get("steps", []) if s.get("is_fallacy")]
    return valid_ids == ["S1", "S2", "S3", "S4", "S5"] and fallacy_ids == ["S_BAD"]


def gen_c02_open_sym(rng):
    k = rng.randint(2, 24)
    c_val = rng.randint(1, 15)
    ans = f"{k}*m/p"
    return {
        "vars": {"k": k, "c_val": c_val},
        "correct": ans,
        "accepted_equivalents": [ans, f"({k}*m)/p", f"{k}*(m/p)"],
        "variables": ["m", "p"],
        "symbolic_config": {
            "variables": ["m", "p"],
            "palette": ["*", "/", "+", "-", "^"],
            "placeholder": "Ej: 3*m/p",
        },
        "ds": [
            ("D-C02-01", f"-{k}*m/p", r"Error de signo al aplicar Roy sobre $v(p,m) = @c_val@ + \ln(m) - @k@\ln(p)$: los dos signos negativos se cancelan dando $@k@m/p > 0$."),
            ("D-C02-03", f"{k}*p/m", r"Invertiste el cociente de derivadas en $v(p,m) = @c_val@ + \ln(m) - @k@\ln(p)$ calculando $(\partial v/\partial m)/(\partial v/\partial p)$ en vez de $-(\partial v/\partial p)/(\partial v/\partial m)$."),
        ],
    }


def ver_c02_open_sym(res):
    c = str(res.get("correct", "")) if isinstance(res, dict) else str(res)
    v = res.get("vars", {}) if isinstance(res, dict) else {}
    k = v.get("k")
    return bool(k) and c.replace(" ", "") == f"{k}*m/p"


def gen_c02_matching(rng):
    idx_b = rng.randint(1, 30)
    cm = {
        "left_title": "Teorema / Identidad Dual",
        "right_title": "Expresión Analítica Exacta",
        "premises": [
            {"id": "M_roy", "content": r"Identidad de Roy para demanda ordinaria $x_{@idx_b@}^d(p,m)$"},
            {"id": "M_shep", "content": r"Lema de Shephard para demanda compensada $x_{@idx_b@}^h(p,u)$"},
            {"id": "M_dual", "content": r"Relación inversa entre gasto mínimo y utilidad indirecta"},
        ],
        "targets": [
            {"id": "R_roy", "content": r"$-\frac{\partial v/\partial p_{@idx_b@}}{\partial v/\partial m}$"},
            {"id": "R_shep", "content": r"$\frac{\partial e(p,u)}{\partial p_{@idx_b@}}$"},
            {"id": "R_dual", "content": r"$e(p, v(p,m)) \equiv m$"},
            {
                "id": "R_dist_roy",
                "content": r"$+\frac{\partial v/\partial p_{@idx_b@}}{\partial v/\partial m}$ sin signo negativo",
                "is_distractor": True,
                "distractor_id": "D-C02-01",
                "error_rationale": "Como $\\partial v/\\partial p_{@idx_b@} < 0$ y $\\partial v/\\partial m > 0$, sin el signo negativo la demanda resultaría negativa.",
            },
            {
                "id": "R_dist_shep",
                "content": r"$\frac{\partial v(p,m)}{\partial m}$ como demanda compensada",
                "is_distractor": True,
                "distractor_id": "D-C02-04",
                "error_rationale": "La demanda hicksiana deriva de la función de gasto $e(p,u)$ por Lema de Shephard, no de $\\partial v/\\partial m$.",
            },
        ],
        "correct_pairs": {"M_roy": "R_roy", "M_shep": "R_shep", "M_dual": "R_dual"},
    }
    return {"vars": {"idx_b": idx_b}, "concept_matching": cm}


def ver_c02_matching(res):
    cm = res.get("concept_matching") if isinstance(res, dict) else None
    if not isinstance(cm, dict):
        return False
    return cm.get("correct_pairs") == {"M_roy": "R_roy", "M_shep": "R_shep", "M_dual": "R_dual"}


def gen_c02_mc7(rng):
    idx_g = rng.randint(1, 35)
    correct = r"Se requiere $\partial v/\partial m > 0$ y usar el Lema de Shephard en $p_{" + str(idx_g) + r"}$ con signo negativo"
    distractors = [
        {"value": r"El signo resultante en la Identidad de Roy es positivo por la regla de la cadena para el bien " + str(idx_g), "distractor_id": "D-C02-01", "error_rationale": "Al despejar de la identidad derivada respecto a precio $p_{@idx_g@}$, el término pasa con signo negativo."},
        {"value": r"Se asume automáticamente $\partial e/\partial u = 1$ simplificando la deducción en el bien " + str(idx_g), "distractor_id": "D-C02-02", "error_rationale": "El factor $\\partial e/\\partial u = (\\partial v/\\partial m)^{-1}$ debe despejarse derivando respecto a $m$ para bien @idx_g@."},
        {"value": r"El cociente correcto coloca $\partial v/\partial m$ arriba y $\partial v/\partial p$ abajo en el bien " + str(idx_g), "distractor_id": "D-C02-03", "error_rationale": "Invertir el cociente destruye la dimensión económica correcta al despejar la demanda del bien @idx_g@."},
        {"value": r"La identidad produce directamente la demanda hicksiana compensada en el bien " + str(idx_g), "distractor_id": "D-C02-04", "error_rationale": "La Identidad de Roy recupera la demanda ordinaria $x_{@idx_g@}^d(p,m)$, mientras Shephard entrega la hicksiana."},
        {"value": r"Puede prescindirse de aplicar relaciones duales del gasto al derivar para el bien " + str(idx_g), "distractor_id": "D-C02-05", "error_rationale": "Sustituir $\\partial e/\\partial p_{@idx_g@} = x^h$ mediante Shephard es el eslabón formal obligatorio en el paso 2."},
        {"value": r"La identidad dual $e(p,v(p,m)) \equiv m$ refleja homogeneidad lineal en precios para el bien " + str(idx_g), "distractor_id": "D-C02-06", "error_rationale": "La identidad del gasto recupera $m$ por inversión dual, no por homogeneidad de grado uno en $v$ para @idx_g@."},
    ]
    return {"vars": {"idx_g": idx_g}, "correct": correct, "distractors": distractors}


def ver_c02_mc7(res):
    c = str(res.get("correct", "")) if isinstance(res, dict) else str(res)
    v = res.get("vars", {}) if isinstance(res, dict) else {}
    return "Lema de Shephard" in c and str(v.get("idx_g")) in c


# ==============================================================================
# STEMS & HINTS
# ==============================================================================

stems_hab01_1 = [
    r"Una firma precio-aceptante enfrenta el precio $p = @p@$ con función de costos $c(x) = @a@\sqrt{x} + @F@$. Ejecute la modelización Stage 0 antes de optimizar:",
    r"Considere una empresa competitiva con tecnología $c(x) = @a@\sqrt{x} + @F@$ y precio exógeno $p = @p@$. Complete la auditoría estructural Stage 0:",
    r"Evalúe la firma con costo total $c(x) = @a@\sqrt{x} + @F@$ operando bajo precio dado $p = @p@$. Formalice variables y curvatura en Stage 0:",
    r"Antes de calcular extremos para $c(x) = @a@\sqrt{x} + @F@$ y precio $p = @p@$, estructure las fases del problema competitivo en Stage 0:",
    r"Una planta tomadora de precios opera con $c(x) = @a@\sqrt{x} + @F@$ a precio $p = @p@$. Clasifique variables, supuestos y diagnóstico en Stage 0:",
    r"Audite el modelo de la firma competitiva con costo $c(x) = @a@\sqrt{x} + @F@$ y precio $p = @p@$ siguiendo el flujo guiado de Stage 0:",
]

stems_hab01_2 = [
    r"Para la función de costo total $c(x) = @a@\sqrt{x} + @F@$ ($k = @k@ = @a@/2$), obtenga la expresión simbólica exacta del costo marginal $CMg(x)$ en función de `x`:",
    r"Dada la tecnología $c(x) = @a@\sqrt{x} + @F@$ ($k = @k@$), derive algebraicamente $CMg(x) = c'(x)$ en términos de `x`:",
    r"Calcule la fórmula simbólica de $CMg(x)$ correspondiente al costo $c(x) = @a@\sqrt{x} + @F@$ (con parámetro $k = @k@$):",
    r"Escriba la expresión simbólica equivalente a $c'(x)$ cuando el costo total es $c(x) = @a@\sqrt{x} + @F@$ ($k = @k@$):",
    r"Determine simbólicamente el costo marginal $CMg(x)$ para $c(x) = @a@\sqrt{x} + @F@$ donde el coeficiente reducido es $k = @k@$:",
    r"Obtenga $CMg(x)$ en el editor simbólico respecto a `x` a partir de $c(x) = @a@\sqrt{x} + @F@$ ($k = @k@$):",
]

stems_hab01_3 = [
    r"Con $c(x) = @a@\sqrt{x} + @F@$ ($k = @k@$) y precio $p = @p@$, la CPO anula $\pi'(x)$ en $x_{\text{stat}} = @x_stat@$ ($\pi_{\text{stat}} = @pi_stat@$). Calcule $\pi(x)$ al expandir a $x = @x_hi@$ ($\sqrt{@x_hi@} = @m_hi@$):",
    r"Evalúe el beneficio competitivo $\pi(@x_hi@)$ cuando $p = @p@$, $c(x) = @a@\sqrt{x} + @F@$ ($k = @k@$), frente al mínimo en $x_{\text{stat}} = @x_stat@$ ($\pi_{\text{stat}} = @pi_stat@$, $\sqrt{@x_hi@} = @m_hi@$):",
    r"Si $p = @p@$ y $c(x) = @a@\sqrt{x} + @F@$ ($k = @k@$), determine el beneficio exacto en $x = @x_hi@$ ($\sqrt{@x_hi@} = @m_hi@$) evitando el mínimo $x_{\text{stat}} = @x_stat@$ ($\pi_{\text{stat}} = @pi_stat@$):",
    r"Una firma con $c(x) = @a@\sqrt{x} + @F@$ ($k = @k@$) y $p = @p@$ descarta $x_{\text{stat}} = @x_stat@$ ($\pi_{\text{stat}} = @pi_stat@$) y produce $x = @x_hi@$ ($\sqrt{@x_hi@} = @m_hi@$). Halle $\pi(@x_hi@)$:",
    r"Calcule el valor de $\pi(x) = px - c(x)$ en $x = @x_hi@$ ($\sqrt{@x_hi@} = @m_hi@$) dados $p = @p@$, $c(x) = @a@\sqrt{x} + @F@$ ($k = @k@$) y $\pi(x_{\text{stat}} = @x_stat@) = @pi_stat@$:",
    r"Compare el óptimo respecto al mínimo $x_{\text{stat}} = @x_stat@$ ($\pi_{\text{stat}} = @pi_stat@$) calculando $\pi(@x_hi@)$ para $p = @p@$, $c(x) = @a@\sqrt{x} + @F@$ ($\sqrt{@x_hi@} = @m_hi@$, $k=@k@$):",
]

stems_hab01_4 = [
    r"Un alumno afirma maximizar beneficios con $c(x) = @b_dbl@\sqrt{x} + @F@$ ($b=@b@$) y $p = @p_val@$ igualando $p = CMg(x)$. Detecte el paso falaz y su justificación:",
    r"Audite esta deducción competitiva para $c(x) = @b_dbl@\sqrt{x} + @F@$ ($b=@b@$) a precio $p = @p_val@$ y señale el quiebre de segundo orden:",
    r"Examine el procedimiento propuesto bajo $c(x) = @b_dbl@\sqrt{x} + @F@$ ($b=@b@$, $p=@p_val@$). Identifique la afirmación errónea y el motivo correcto:",
    r"Caza de falacias para $c(x) = @b_dbl@\sqrt{x} + @F@$ con $b = @b@$ y precio $p = @p_val@$: marque el paso inválido y seleccione la explicación analítica:",
    r"Revise los pasos para optimizar $c(x) = @b_dbl@\sqrt{x} + @F@$ ($b=@b@$, $p=@p_val@$) e indique dónde falla la condición de optimalidad:",
    r"Identifique la falacia analítica al optimizar la tecnología $c(x) = @b_dbl@\sqrt{x} + @F@$ ($b=@b@, p=@p_val@$) de rendimientos crecientes:",
]

stems_hab02_1 = [
    r"Con ingreso $m = @m@$, precio $p_1 = @p1@$, $p_2 = 1$ y descuento $r = @r_pct@\%$ tras superar $\bar{x}_1 = @x_bar@$, deduce el excedente $x_2^*$ y ubica el vértice no convexo:",
    r"Dada la restricción por tramos con renta $m = @m@$, tarifa $p_1 = @p1@$, $p_2 = 1$ y descuento marginal $r = @r_pct@\%$ desde $\bar{x}_1 = @x_bar@$, sitúa el punto de quiebre:",
    r"Analiza en el lienzo el quiebre presupuestario con $m = @m@$, $p_1 = @p1@$, $p_2 = 1$ y descuento $r = @r_pct@\%$ a partir de $\bar{x}_1 = @x_bar@$, marcando el vértice:",
    r"Localiza geométricamente el ángulo entrante no convexo bajo $m = @m@$, $p_1 = @p1@$, $p_2 = 1$, umbral $\bar{x}_1 = @x_bar@$ y descuento $r = @r_pct@\%$:",
    r"Calcula $(x_1^*, x_2^*)$ en el cambio de tramo para $m = @m@$, $p_1 = @p1@$, $p_2 = 1$, $\bar{x}_1 = @x_bar@$ y descuento $r = @r_pct@\%$, y mueve el punto al vértice:",
    r"Identifica sobre el plano el punto de quiebre presupuestario generado por $m = @m@$, $p_1 = @p1@$, $p_2 = 1$, umbral $\bar{x}_1 = @x_bar@$ y descuento $r = @r_pct@\%$:",
]

stems_hab02_2 = [
    r"Con precio inicial $p_1 = @p1@$, umbral $\bar{x}_1 = @x_bar@$ y descuento `r` en el tramo $x_1 > @x_bar@$, escriba simbólicamente el precio efectivo unitario:",
    r"Exprese en función de `r` el costo marginal por unidad adicional cuando $x_1 > @x_bar@$ dado $\bar{x}_1 = @x_bar@$ y $p_1 = @p1@$:",
    r"Para el Tramo B ($x_1 > @x_bar@$) tras $\bar{x}_1 = @x_bar@$ con precio base $p_1 = @p1@$ y descuento `r`, ingrese la fórmula simbólica neta:",
    r"Determine simbólicamente (en `r`) la pendiente absoluta del segundo tramo $x_1 > @x_bar@$ tras $\bar{x}_1 = @x_bar@$ con $p_1 = @p1@$:",
    r"Escriba la fórmula en `r` del precio descontado para $x_1 > @x_bar@$ con umbral $\bar{x}_1 = @x_bar@$ partiendo de $p_1 = @p1@$:",
    r"Formule el precio efectivo unitario del tramo $x_1 > @x_bar@$ superando $\bar{x}_1 = @x_bar@$ con precio inicial $p_1 = @p1@$ y tasa `r`:",
]

stems_hab02_3 = [
    r"Ordene el protocolo deductivo en ProofDAG para hallar el óptimo global con restricción no convexa en $\bar{x}_1 = @x_bar@$, $p_1 = @p1@$ y descuento $r = @r_dec@$, descartando el paso falaz:",
    r"Construya la cadena lógica de optimización bajo descuento por volumen ($\bar{x}_1 = @x_bar@$, $p_1 = @p1@$, $r = @r_dec@$) evitando el Lagrangiano único inválido:",
    r"Encadene los pasos válidos para comparar tangencias locales y vértice en ($\bar{x}_1 = @x_bar@$, $p_1 = @p1@$, $r = @r_dec@$) y excluya el paso falaz:",
    r"Establezca el orden topológico de optimalidad global cuando la restricción quiebra en $\bar{x}_1 = @x_bar@$ con $p_1 = @p1@$ y $r = @r_dec@$:",
    r"Ordene la prueba formal del óptimo global por tramos ($\bar{x}_1 = @x_bar@$, tarifa $p_1 = @p1@$, descuento $r = @r_dec@$) omitiendo la falacia de convexidad:",
    r"Ensamble en ProofDAG las condiciones necesarias de comparación global para $\bar{x}_1 = @x_bar@$, $p_1 = @p1@$ y descuento $r = @r_dec@$:",
]

stems_hab02_4 = [
    r"Un consumidor paga $p_1 = @p1@$ hasta $\bar{x}_1 = @x_bar@$ y recibe descuento `r` por cada unidad adicional ($x_1 > @x_bar@$). Modele variables, supuestos y ecuación de gasto total en Stage 0:",
    r"Complete las tres fases Stage 0 para formular algebraicamente en `x1` y `r` el gasto del bien 1 en el Tramo B ($x_1 > @x_bar@$, $\bar{x}_1 = @x_bar@$) con tarifa base $p_1 = @p1@$:",
    r"Formalice en Stage 0 el presupuesto por bloques ($p_1 = @p1@$, umbral $\bar{x}_1 = @x_bar@$, tramo $x_1 > @x_bar@$, descuento `r`) culminando con el gasto en `x1` y `r`:",
    r"Audite variables endógenas, quiebres de demanda y formule el gasto total para $x_1 > @x_bar@$ ($\bar{x}_1 = @x_bar@$) en `x1` y `r` dado $p_1 = @p1@$:",
    r"Resuelva el modelado progresivo Stage 0 hasta escribir simbólicamente el gasto en bien 1 para $x_1 > @x_bar@$ con $\bar{x}_1 = @x_bar@$, $p_1 = @p1@$ y descuento `r`:",
    r"Desarrolle el stepper Stage 0 para tarifa por bloques ($p_1 = @p1@$, umbral $\bar{x}_1 = @x_bar@$, $x_1 > @x_bar@$, descuento `r`) y formule el gasto total:",
]

stems_c01_1 = [
    r"Dada $u(x_1, x_2) = \lfloor x_1 \rfloor + \lfloor x_2 \rfloor$, refuta la convexidad del contorno superior en $k = @k_lvl@$ ingresando canastas $A=(a_1,a_2)$ y $B=(b_1,b_2)$ cuyo punto medio caiga debajo:",
    r"Encuentra un contraejemplo numérico $A=(a_1, a_2)$ y $B=(b_1, b_2)$ para $u(x_1,x_2) = \lfloor x_1 \rfloor + \lfloor x_2 \rfloor$ con cota $k = @k_lvl@$ donde $u(0.5A+0.5B) < @k_lvl@$:",
    r"Demuestra en la Arena Adversarial que $u(x_1, x_2) = \lfloor x_1 \rfloor + \lfloor x_2 \rfloor$ no es cuasicóncava exhibiendo un testigo $A=(a_1, a_2)$, $B=(b_1, b_2)$ para $k = @k_lvl@$:",
    r"Propón coordenadas válidas $A=(a_1,a_2)$ y $B=(b_1,b_2)$ dentro del contorno de $u(x_1, x_2) = \lfloor x_1 \rfloor + \lfloor x_2 \rfloor$ en cota $k = @k_lvl@$ cuya combinación media viole la convexidad:",
    r"Refuta analíticamente mediante contraejemplo $A=(a_1, a_2)$ y $B=(b_1, b_2)$ la cuasiconcavidad de $u(x_1, x_2) = \lfloor x_1 \rfloor + \lfloor x_2 \rfloor$ en el nivel $k = @k_lvl@$:",
    r"Construye un testigo numérico $A=(a_1,a_2)$ y $B=(b_1,b_2)$ para $u(x_1, x_2) = \lfloor x_1 \rfloor + \lfloor x_2 \rfloor$ respecto al umbral $k = @k_lvl@$ violando convexidad:",
]

stems_c01_2 = [
    r"En el árbol extensivo de información imperfecta con pago cooperativo $(@w1@, @w1@)$ (y desvío $(@w2@, 0)$), seleccione las ramas correspondientes al equilibrio cooperativo y agrupe los nodos indistinguibles del Jugador 2:",
    r"Trace en el árbol de juego extensivo la senda de equilibrio hacia el nodo terminal con pagos $(@w1@, @w1@)$ (alternativa $(@w2@, 0)$) y forme el conjunto de información correcto para `J2`:",
    r"Marque en el lienzo las aristas hacia `T1` con utilidad conjunta $(@w1@, @w1@)$ frente a $(@w2@, 0)$ e indique la partición de información entre `J2a` y `J2b`:",
    r"Configure la estrategia cooperativa $(@w1@, @w1@)$ (versus $(@w2@, 0)$) seleccionando sus ramas en el árbol e instanciando el conjunto de información de `J2`:",
    r"Determine sobre el árbol extensivo las ramas que conducen al perfil $(@w1@, @w1@)$ frente al pago $(@w2@, 0)$ junto con el conjunto de información imperfecta:",
    r"Construya en el árbol interactivo la trayectoria óptima hacia $(@w1@, @w1@)$ (con pago asimétrico $(@w2@, 0)$) y trace la equivalencia informacional de `J2`:",
]

stems_c01_3 = [
    r"Empareje cada propiedad analítica sobre preferencias discontinuas en torno al nivel $k = @c_lvl@$ con su consecuencia formal correspondiente:",
    r"Asocie causalmente los escenarios de ruptura axiomática alrededor del nivel de contorno $k = @c_lvl@$ con sus resultados deductivos:",
    r"Relacione en la matriz causal cada enunciado de contorno superior (nivel $k = @c_lvl@$) y teoría de juegos con su implicación exacta:",
    r"Vincule cada concepto analítico evaluado alrededor de $k = @c_lvl@$ con la propiedad formal correcta evitando distractores cruzados:",
    r"Empareje los fenómenos de no diferenciabilidad en el umbral $k = @c_lvl@$ con el diagnóstico matemático adecuado:",
    r"Seleccione la asociación correcta entre cada propiedad microeconómica en cota $k = @c_lvl@$ y su consecuencia formal:",
]

stems_c01_4 = [
    r"Calcule el valor entero exacto de $u(x_1, x_2) = \lfloor x_1 \rfloor + \lfloor x_2 \rfloor$ evaluado en la canasta fraccionaria $(x_1, x_2) = (@x1@, @x2@)$:",
    r"Determine numéricamente $u(x_1, x_2) = \lfloor x_1 \rfloor + \lfloor x_2 \rfloor$ evaluada en $(x_1, x_2) = (@x1@, @x2@)$:",
    r"Para $(x_1, x_2) = (@x1@, @x2@)$, evalúe $u(x_1, x_2) = \lfloor x_1 \rfloor + \lfloor x_2 \rfloor$ e ingrese el resultado numérico exacto:",
    r"Halle el nivel de utilidad de $u(x_1,x_2) = \lfloor x_1 \rfloor + \lfloor x_2 \rfloor$ para $(x_1, x_2) = (@x1@, @x2@)$:",
    r"Evalúe sin aproximaciones continuas la utilidad $u(x_1, x_2) = \lfloor x_1 \rfloor + \lfloor x_2 \rfloor$ en la canasta $(x_1, x_2) = (@x1@, @x2@)$:",
    r"Calcule el entero resultante de evaluar $u(x_1,x_2) = \lfloor x_1 \rfloor + \lfloor x_2 \rfloor$ en el punto $(x_1, x_2) = (@x1@, @x2@)$:",
]

stems_c02_1 = [
    r"A partir de la identidad $m \equiv e(p, v(p,m))$, encadene los pasos y justificaciones para derivar la Identidad de Roy de $x_{@g_idx@}$ descartando la falacia:",
    r"Construya en ProofDAG la demostración de la Identidad de Roy para $x_{@g_idx@}$ a partir de $m \equiv e(p, v(p,m))$:",
    r"Ordene la deducción analítica formal de la Identidad de Roy de $x_{@g_idx@}$ desde $m \equiv e(p, v(p,m))$, asociando cada lema:",
    r"Ensamble los 5 eslabones lógicos desde $m \equiv e(p, v(p,m))$ para deducir la Identidad de Roy en $x_{@g_idx@}$, excluyendo el paso con signo errado:",
    r"Desarrolle la prueba paso a paso de la Identidad de Roy para $x_{@g_idx@}$ partiendo de $m \equiv e(p, v(p,m))$ mediante regla de la cadena y Shephard:",
    r"Verifique en ProofDAG el encadenamiento dual correcto desde $m \equiv e(p,v(p,m))$ hacia la Identidad de Roy del bien $x_{@g_idx@}$:",
]

stems_c02_2 = [
    r"Dada $v(p, m) = @c_val@ + \ln(m) - @k@\ln(p)$, aplique la Identidad de Roy para hallar simbólicamente $x^d(p,m)$ en `m` y `p`:",
    r"Calcule algebraicamente $x^d(p,m)$ mediante Identidad de Roy si $v(p,m) = @c_val@ + \ln(m) - @k@\ln(p)$ en función de `m` y `p`:",
    r"Obtenga en términos simbólicos de `m` y `p` la demanda marshalliana $x^d(p,m)$ derivada de $v(p,m) = @c_val@ + \ln(m) - @k@\ln(p)$:",
    r"Aplique la Identidad de Roy para $x^d(p,m)$ dada la utilidad indirecta $v(p,m) = @c_val@ + \ln(m) - @k@\ln(p)$ usando `m` y `p`:",
    r"Determine en el editor simbólico la expresión reducida de $x^d(p,m)$ en `m` y `p` para $v(p,m) = @c_val@ + \ln(m) - @k@\ln(p)$:",
    r"Deduzca simbólicamente la función de demanda ordinaria $x^d(p,m)$ en `m` y `p` correspondiente a $v(p,m) = @c_val@ + \ln(m) - @k@\ln(p)$:",
]

stems_c02_3 = [
    r"Asocie cada identidad de dualidad del consumidor para el bien $x_{@idx_b@}$ con su fórmula analítica correcta:",
    r"Empareje los teoremas duales aplicados sobre el bien $x_{@idx_b@}$ con sus expresiones formales correspondientes:",
    r"Relacione correctamente la Identidad de Roy, el Lema de Shephard y la inversión gasto-utilidad para el bien $x_{@idx_b@}$:",
    r"Vincule cada principio de dualidad del consumidor del bien $x_{@idx_b@}$ con su expresión formal descartando distractores cruzados:",
    r"Determine la correspondencia causal correcta entre los teoremas de dualidad del bien $x_{@idx_b@}$ y sus ecuaciones:",
    r"Asocie cada identidad fundamental en teoría de la dualidad para el bien $x_{@idx_b@}$ con su expresión exacta:",
]

stems_c02_4 = [
    r"En la derivación de la Identidad de Roy para $x_{@idx_g@}$ a partir de $m \equiv e(p, v(p,m))$, indique el requisito analítico indispensable:",
    r"Señale la condición formal correcta sobre la obtención analítica de la Identidad de Roy en $x_{@idx_g@}$ desde $m \equiv e(p, v(p,m))$:",
    r"Identifique cuál afirmación describe rigurosamente el paso dual entre $m \equiv e(p, v(p,m))$ y la Identidad de Roy para $x_{@idx_g@}$:",
    r"Determine el supuesto y mecanismo correcto al derivar la Identidad de Roy del bien $x_{@idx_g@}$ desde $m \equiv e(p,v(p,m))$:",
    r"Seleccione la propiedad verdadera sobre la derivación general de la Identidad de Roy en $x_{@idx_g@}$ partiendo de $m \equiv e(p, v(p,m))$:",
    r"Evalúe la validez deductiva de la Identidad de Roy para $x_{@idx_g@}$ desde $m \equiv e(p, v(p,m))$ y elija la proposición exacta:",
]

def _mk_hints(topic, a, b, c):
    return [a, b, c]

TEMPLATES = [
    # Hab-01 (0 MC7, 100% active)
    ("T-Hab-01-01", "Hab-01", "unstructured_model", gen_hab01_stage0, ver_hab01_stage0, ("easy", "Apply"), stems_hab01_1, [r"Distingue la decisión endógena $x$ de los datos exógenos $p$ y $F$.", r"Evalúa el signo de $c''(x)$ cuando el costo crece como raíz cuadrada.", r"Un $\pi''(x) > 0$ invierte el punto crítico de primer orden en mínimo local."], r"Con $c(x) = @a@\sqrt{x} + @F@$ y $p = @p@$, $\pi''(x) > 0$, por lo que $p = CMg(x)$ es mínimo local."),
    ("T-Hab-01-02", "Hab-01", "open_symbolic", gen_hab01_open_sym, ver_hab01_open_sym, ("medium", "Analyze"), stems_hab01_2, [r"Expresa $\sqrt{x}$ como $x^{1/2}$ antes de derivar.", r"Multiplica por el coeficiente $@a@ = 2 \cdot @k@$ y reduce la potencia a $x^{-1/2}$.", r"El costo fijo $@F@$ desaparece al derivar respecto a $x$."], r"Derivando $c(x) = @a@\sqrt{x} + @F@$ se obtiene $CMg(x) = @k@/\sqrt{x}$."),
    ("T-Hab-01-03", "Hab-01", "fill_in_the_blank", gen_hab01_fib_profit, ver_hab01_fib_profit, ("hard", "Analyze"), stems_hab01_3, [r"Calcula primero el ingreso total multiplicando $p = @p@$ por $x = @x_hi@$.", r"Evalúa el costo variable $@a@\sqrt{@x_hi@} = @a@ \cdot @m_hi@$ y añade $F = @F@$.", r"Comprueba que $\pi(@x_hi@)$ supera el mínimo local $\pi_{\text{stat}} = @pi_stat@$."], r"En $x = @x_hi@$, $\pi = (@p@)(@x_hi@) - (@a@)(@m_hi@) - @F@ = @pi_hi@ > @pi_stat@$."),
    ("T-Hab-01-04", "Hab-01", "adversarial_break", gen_hab01_adv, ver_hab01_adv, ("hard", "Evaluate"), stems_hab01_4, [r"Revisa si la derivada primera en $x_{\text{stat}}$ basta para afirmar un máximo.", r"Deriva una segunda vez la expresión $\pi'(x) = @p_val@ - @b@/\sqrt{x}$.", r"Observa por qué un beneficio estrictamente convexo convierte la CPO en mínimo."], r"El Paso 3 ignora $\pi''(x) > 0$ bajo $c(x) = @b_dbl@\sqrt{x} + @F@$ y $p = @p_val@$."),
    # Hab-02 (0 MC7, 100% active)
    ("T-Hab-02-01", "Hab-02", "invariant_canvas", gen_hab02_canvas_cart, ver_hab02_canvas_cart, ("easy", "Analyze"), stems_hab02_1, [r"El tramo inicial rige exactamente hasta $x_1 = \bar{x}_1 = @x_bar@$.", r"Resta el gasto inicial $p_1 \cdot \bar{x}_1$ de la renta total $m = @m@$.", r"Coloca el punto sobre el vértice no diferenciable de la frontera presupuestaria."], r"El quiebre no convexo ocurre en $\bar{x}_1 = @x_bar@$, donde $x_2^* = m - p_1\bar{x}_1 = @m@ - (@p1@)(@x_bar@)$ con descuento $r = @r_pct@\%$."),
    ("T-Hab-02-02", "Hab-02", "open_symbolic", gen_hab02_open_sym, ver_hab02_open_sym, ("medium", "Apply"), stems_hab02_2, [r"Identifica el precio de lista $@p1@$ antes del descuento proporcional.", r"Restar una proporción `r` equivale a multiplicar el precio base por $(1 - r)$.", r"Verifica que si $r = 0$, el precio marginal en $x_1 > @x_bar@$ se reduce a $@p1@$."], r"Para $x_1 > @x_bar@$, cada unidad cuesta $p_1(1-r) = @p1@(1-r)$."),
    ("T-Hab-02-03", "Hab-02", "proof_dag", gen_hab02_dag, ver_hab02_dag, ("hard", "Evaluate"), stems_hab02_3, [r"La restricción presupuestaria no es un conjunto convexo alrededor de $@x_bar@$.", r"Cada tramo suave y el propio vértice deben evaluarse como candidatos independientes.", r"Un Lagrangiano global único no detecta tangencias locales múltiples ni esquinas."], r"Con $\bar{x}_1 = @x_bar@$, $p_1 = @p1@$ y $r = @r_dec@$, compara tangencias locales y vértice en $\arg\max$."),
    ("T-Hab-02-04", "Hab-02", "unstructured_model", gen_hab02_stage0_sym, ver_hab02_stage0_sym, ("hard", "Create"), stems_hab02_4, [r"Separa el gasto fijo de las primeras $\bar{x}_1 = @x_bar@$ unidades a tarifa $@p1@$.", r"Suma únicamente las unidades excedentes $(x_1 - @x_bar@)$ al precio descontado.", r"Formula el gasto total como suma lineal por tramos en función de `x1` y `r`."], r"El gasto total en el Tramo B ($x_1 > @x_bar@$) es $@p1@\cdot @x_bar@ + @p1@(1-r)(x_1 - @x_bar@)$."),
    # C-01 (0 MC7, 100% active)
    ("T-C-01-01", "C-01", "adversarial_break", gen_c01_counterexample, ver_c01_counterexample, ("medium", "Evaluate"), stems_c01_1, [r"Elige primero canastas enteras $A$ y $B$ tales que ambas alcancen exactamente $@k_lvl@$.", r"Procura que al menos una coordenada de $A$ y $B$ difiera en una unidad impar.", r"Calcula la semisuma $0.5A + 0.5B$ para observar cómo $\lfloor \cdot \rfloor$ trunca abajo."], r"Un testigo como $A=(1, @k_lvl@-1)$ y $B=(2, @k_lvl@-2)$ da punto medio con suma $< @k_lvl@$."),
    ("T-C-01-02", "C-01", "invariant_canvas", gen_c01_tree, ver_c01_tree, ("hard", "Analyze"), stems_c01_2, [r"Compara los perfiles de pago terminales hasta identificar $(@w1@, @w1@)$.", r"Activa de manera secuencial únicamente las dos aristas que llevan al nodo `T1`.", r"Cuando J2 desconoce qué eligió J1, sus dos nodos pertenecen al mismo conjunto informacional."], r"Activa las aristas hacia el pago $(@w1@, @w1@)$ (frente a $(@w2@, 0)$) y une J2a con J2b."),
    ("T-C-01-03", "C-01", "concept_matching", gen_c01_matching, ver_c01_matching, ("easy", "Understand"), stems_c01_3, [r"Analiza si la función escalonada $\lfloor x_i \rfloor$ admite derivadas parciales continuas.", r"Contrasta la convexidad geométrica del contorno en cota $@c_lvl@$ frente a bloques.", r"Descarta asociaciones que atribuyan suavidad o información perfecta falsa."], r"La función piso alrededor de $@c_lvl@$ produce contornos en escalera no convexos e inaplicabilidad del hessiano."),
    ("T-C-01-04", "C-01", "fill_in_the_blank", gen_c01_fib, ver_c01_fib, ("hard", "Analyze"), stems_c01_4, [r"Trunca separadamente la parte decimal de $x_1 = @x1@$ al entero menor o igual.", r"Trunca separadamente $x_2 = @x2@$ hacia abajo, nunca redondees hacia arriba.", r"Suma únicamente ambos resultados enteros tras aplicar el operador piso."], r"$\lfloor @x1@ \rfloor + \lfloor @x2@ \rfloor = @ans@$ (no $@cont_sum@$ ni $@ceil_sum@$)."),
    # C-02 (1 MC7 + 3 active = 75% active)
    ("T-C-02-01", "C-02", "proof_dag", gen_c02_dag_roy, ver_c02_dag_roy, ("hard", "Evaluate"), stems_c02_1, [r"Inicia diferenciando $m \equiv e(p, v(p,m))$ respecto a $p_{@g_idx@}$ por regla de la cadena.", r"Necesitas derivar además la identidad respecto a $m$ para despejar $\partial e/\partial u$.", r"Despeja la demanda ordinaria cuidando el signo negativo del término en precio."], r"La deducción para el bien $@g_idx@$ aplica regla de la cadena, Shephard y derivada respecto a $m$."),
    ("T-C-02-02", "C-02", "open_symbolic", gen_c02_open_sym, ver_c02_open_sym, ("medium", "Analyze"), stems_c02_2, [r"Deriva $v = @c_val@ + \ln(m) - @k@\ln(p)$ respecto a $p$ obteniendo $-@k@/p$.", r"Deriva la misma función respecto a $m$ obteniendo el inverso multiplicativo $1/m$.", r"Divide $-(\partial v/\partial p)$ entre $(\partial v/\partial m)$ simplificando signos."], r"Con $v = @c_val@ + \ln(m) - @k@\ln(p)$, $-\frac{-@k@/p}{1/m} = @k@m/p$."),
    ("T-C-02-03", "C-02", "concept_matching", gen_c02_matching, ver_c02_matching, ("easy", "Analyze"), stems_c02_3, [r"Identifica cuál teorema diferencia la utilidad indirecta $v(p,m)$ respecto a $p_{@idx_b@}$.", r"Recuerda el signo negativo que acompaña al cociente de derivadas en Roy.", r"Asocia la derivada de la función de gasto $e(p,u)$ con la demanda compensada."], r"Roy arroja demanda ordinaria con signo negativo y Shephard deriva $e(p,u)$ para el bien $@idx_b@$."),
    ("T-C-02-04", "C-02", "multiple_choice", gen_c02_mc7, ver_c02_mc7, ("hard", "Evaluate"), stems_c02_4, [r"Verifica la condición de diferenciabilidad y no saciación $\partial v/\partial m > 0$ en $p_{@idx_g@}$.", r"El puente entre la derivada del gasto mínimo y la demanda usa el Lema de Shephard.", r"Examina el signo y la posición del numerador y denominador tras el despeje final."], r"La Identidad de Roy en el bien $p_{@idx_g@}$ requiere $\partial v/\partial m > 0$, Shephard y signo negativo."),
]
'''


def main() -> int:
    out_dir = Path(__file__).resolve().parent
    out_json = out_dir / "m20_canonical_course.json"

    with tempfile.TemporaryDirectory(prefix="m20_c2c_") as tmp_str:
        work_dir = Path(tmp_str)
        shards_dir = work_dir / "shards"
        templates_dir = work_dir / "templates"
        shards_dir.mkdir(parents=True, exist_ok=True)
        templates_dir.mkdir(parents=True, exist_ok=True)

        # 1. Stage 2: compile_cta
        cta_py = work_dir / "cta_data.py"
        cta_py.write_text(CTA_DATA_PY, encoding="utf-8")
        (work_dir / "pre_cta_manifest.json").write_text(
            json.dumps(
                {
                    "course_id": "m20_canonical_course",
                    "source_files": ["microeconomia_casos_canonicos.pdf"],
                    "files": [
                        {
                            "doc": "microeconomia_casos_canonicos.pdf",
                            "total_pages": 80,
                            "valid_page_range": [1, 80],
                        }
                    ],
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        cta_ok, cta_dict, cta_errs, cta_ms = compile_cta(
            cta_py,
            output_dir=work_dir,
            require_assumptions=True,
        )
        assert cta_ok and not cta_errs, f"compile_cta failed: {cta_errs}"
        print(f"[1/6] compile_cta OK ({len(cta_dict['competencies'])} comps, {cta_ms:.1f} ms)")

        # 2. Pre-shard manifest + shard_01_data.py
        (shards_dir / "pre_shard_manifest.json").write_text(
            json.dumps(
                {
                    "total_competencies": len(cta_dict["competencies"]),
                    "total_shards": 1,
                    "shards": [
                        {
                            "shard_id": "shard_01",
                            "shard_index": 0,
                            "competency_ids": [c["id"] for c in cta_dict["competencies"]],
                            "competencies": cta_dict["competencies"],
                            "shard_data_path": str((shards_dir / "shard_01_data.py").as_posix()),
                            "templates_dir": str(templates_dir.as_posix()),
                        }
                    ],
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        (shards_dir / "shard_01_data.py").write_text(SHARD_01_DATA_PY, encoding="utf-8")

        # 3. Stage 3: compile_shard(strict=True)
        cs_ok, cs_errs = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_01",
            strict=True,
            min_archetypes=4,
            seeds=15,
        )
        assert cs_ok and not cs_errs, f"compile_shard failed:\n" + "\n".join(cs_errs)
        print("[2/6] compile_shard(strict=True, min_archetypes=4) OK")

        # 4. Stage 3B: check_templates_file_or_dir(strict=True)
        ct_ok, ct_errs = check_templates_file_or_dir(
            templates_dir,
            cta_path=work_dir / "cta.json",
            num_dry_run_seeds=10,
            strict=True,
        )
        assert ct_ok and not ct_errs, f"check_templates_file_or_dir failed:\n" + "\n".join(ct_errs)
        print("[3/6] check_templates_file_or_dir(strict=True) OK")

        # 5. Stage 4: instantiate_competency per competency
        all_questions: List[Dict[str, Any]] = []
        for idx, comp in enumerate(cta_dict["competencies"]):
            cid = comp["id"]
            tpl_file = templates_dir / f"{cid}.json"
            tpl_container = json.loads(tpl_file.read_text(encoding="utf-8"))
            templates_list = tpl_container.get("templates", [])
            d_map = {d["id"]: d for d in comp.get("distractors", [])}
            inst_res = instantiate_competency(
                competency=comp,
                templates=templates_list,
                cta_distractors_map=d_map,
                seed_offset_base=10000 + idx * 1000,
            )
            all_questions.extend(inst_res["questions"])
            print(f"      instantiated {cid} ({comp['type']}): {len(inst_res['questions'])} questions")

        course_comps: List[Dict[str, Any]] = []
        cat_map = {"skill": "Skill", "concept": "Concept", "fact": "Fact"}
        for c in cta_dict["competencies"]:
            course_comps.append({
                "id": c["id"],
                "code": c["id"],
                "name": c["name"],
                "category": cat_map.get(str(c.get("type", "concept")).lower(), "Concept"),
                "description": c.get("description_latex") or c.get("description") or c["name"],
                "prerequisites": c.get("prerequisites", []),
                "evidence": c.get("evidence", []),
                "assumptions": c.get("assumptions", []),
                "bloom_level": c.get("bloom", "Analyze"),
                "mastery_target": 0.9,
            })

        course_obj: Dict[str, Any] = {
            "schema_version": "1.0.0",
            "version": "1.0.0",
            "course_id": "m20_canonical_course",
            "course_title": cta_dict["title"],
            "title": cta_dict["title"],
            "description": (
                "Curso canónico compilado vía Content-to-Course para validar las 6 modalidades "
                "de Bloom Superior, distractores diagnósticos (ds) y Smart Blank-First del Milestone 20."
            ),
            "language": "es",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "competencies": course_comps,
            "questions": all_questions,
        }

        # 6. Strict Schema Validation + QA Audit
        val_res = validate_course_content(json.dumps(course_obj, ensure_ascii=False), strict=True)
        assert val_res.is_valid, f"validate_course_content(strict=True) failed: {[str(e) for e in val_res.errors]}"
        print(f"[4/6] validate_course_content(strict=True) OK ({len(all_questions)} questions)")

        audit = run_full_audit(course_obj)
        rm_summary = audit["dimension_summaries"]["retrieval_modality_linter"]
        active_pct = rm_summary.get("active_generation_or_discrimination_pct", 0.0)
        bs_count = rm_summary.get("bloom_superior_count", 0)
        bs_breakdown = rm_summary.get("bloom_superior_breakdown", {})
        assert active_pct >= 80.0, f"Expected active_generation_or_discrimination_pct >= 80.0, got {active_pct} ({rm_summary})"
        expected_types = {
            "open_symbolic",
            "proof_dag",
            "adversarial_break",
            "unstructured_model",
            "invariant_canvas",
            "concept_matching",
        }
        missing_types = [t for t in expected_types if bs_breakdown.get(t, 0) <= 0]
        assert not missing_types, f"Missing Bloom Superior types in breakdown: {missing_types}"
        print(
            f"[5/6] run_full_audit OK (active={active_pct:.2f}%, bloom_superior={bs_count}, "
            f"breakdown={bs_breakdown})"
        )

        out_json.write_text(json.dumps(course_obj, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[6/6] Wrote canonical fixture to {out_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
