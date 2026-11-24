"""Reproducible C2C canonical course builder for Milestone 20.

Compiles the 4 canonical San Marcos / Eloy Ávalos Microeconomics cases from
FUTURE_MILESTONES.md + concept_matching + FIB ds + invariant_canvas (cartesian & tree)
through the real Content-to-Course pipeline under the strict v2 contract
(K=2 per active modality, >= 80% active, 0 MC7 in Skills, <= 1 MC7 in Concepts,
4 anti-clone gates, >= 3 steps and >= 1 edge in ProofDAG/find_fallacy):
  compile_cta -> compile_shard(strict=True, templates_per_modality=2)
  -> check_templates_file_or_dir(strict=True)
  -> instantiate_competency -> validate_course_content(strict=True) -> run_full_audit

Writes output strictly inside tests/fixtures/m20_canonical_cases/ (NEVER into courses/).
"""

from __future__ import annotations

import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

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
        ["open_symbolic", "fill_in_the_blank", "adversarial_break"],
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
            ("Omision Gasto Bloque Previo", r"Evaluar el gasto total del Tramo B como $p_1(1-r)x_1$ omitiendo el pago completo $p_1\bar{x}_1$ del primer bloque.", r"Para $x_1 > \bar{x}_1$ el gasto es $p_1\bar{x}_1 + p_1(1-r)(x_1 - \bar{x}_1)$.", r"$p_1 x_1$", "Suma siempre el costo exacto de las primeras $\bar{x}_1$ unidades antes de agregar el costo del exceso.", "Omitir el pago íntegro p1 * x_bar del primer tramo al expresar el gasto del segundo segmento."),
            ("Lagrangiano Global Unico", "Aplicar condiciones KKT o Lagrangiano clásico asumiendo unicidad de tangencia en un conjunto no convexo.", "Con un quiebre no convexo pueden existir dos tangencias locales y un candidato de vértice que deben compararse.", r"$\text{Óptimo único}$", r"Compara explícitamente las utilidades en $u(x^A)$, el vértice $u(x^{\text{kink}})$ y el segundo tramo $u(x^B)$.", "Omitir la comparación global entre tangencias locales y la condición de esquina en conjuntos no convexos."),
            ("Condicion Esquina Quiebre", r"Ignorar el rango de pendientes $p_1(1-r) \le TMS(x^{\text{kink}}) \le p_1$ o ubicar el óptimo fuera del vértice.", r"En el punto de quiebre $\bar{x}_1$ el vértice no diferenciable es óptimo si la $TMS$ yace entre ambas pendientes.", r"$TMS \neq p_1$", "Verifica la inclusión de la $TMS$ dentro del cono normal delimitado por las pendientes derecha e izquierda."),
            ("Inversion Rol Presupuesto", "Confundir el parámetro exógeno de descuento o renta con la variable de elección endógena.", "Solo las cantidades de consumo $(x_1, x_2)$ son variables de decisión endógenas del hogar.", r"$r = \text{endógena}$", "Diferencia con precisión las variables de elección del consumidor frente a los precios e ingreso exógenos."),
            ("Continuidad Demanda No Convexa", "Suponer que la demanda marshalliana $x_1(p,m)$ es continua al cruzar el umbral crítico de renta.", "Un aumento marginal del ingreso $m$ provoca un salto discreto del óptimo desde el Tramo A al Tramo B.", r"$x_1(m) \text{ continua}$", "Observa cómo ocurre el salto discontinuo entre dos tangencias locales al incrementar gradualmente el presupuesto."),
        ],
        [
            ("Descuento marginal por bloque", r"El descuento $r \in (0,1)$ aplica solo a las unidades $x_1 > \bar{x}_1$.", r"Genera un ángulo entrante no convexo en $(\bar{x}_1, m - p_1\bar{x}_1)$.", r"Si aplicara a todas las unidades habría salto vertical."),
            ("Preferencias estrictamente convexas", r"Curvas de indiferencia suaves y estrictamente convexas.", "Garantiza comparación finita entre dos tangencias locales y el vértice.", r"Sin convexidad de preferencias habría soluciones de esquina triviales."),
        ],
        ["invariant_canvas", "open_symbolic", "unstructured_model"],
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
        ["adversarial_break", "invariant_canvas", "fill_in_the_blank"],
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


SHARD_01_DATA_PY = r'''# Shard 01 Data — 4 Casos Canónicos de Milestone 20 (25 plantillas bajo K=2, >=80% activo, 4 candados anti-clon)
import math


def _ok_sep(vals):
    return len(set(vals)) == len(vals) and all(
        b - a >= 0.02 * max(abs(a), abs(b), 1.0)
        for a, b in zip(sorted(vals), sorted(vals)[1:])
    )


# ==============================================================================
# COMPETENCIA Hab-01 (Skill — 0 MC7, M=3, K=2 => 6 plantillas, 100% activo)
# ==============================================================================

def gen_hab01_os1(rng):
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


def ver_hab01_os1(c, v):
    k = v.get("k")
    a = v.get("a")
    s = str(c).replace(" ", "")
    return bool(k) and s in (f"{k}/sqrt(x)", f"{k}*x^(-1/2)", f"{a}/(2*sqrt(x))")


def gen_hab01_os2(rng):
    a = 2 * rng.randint(2, 24)
    F = rng.randint(12, 80)
    ans = f"{a}/sqrt(x) + {F}/x"
    return {
        "vars": {"a": a, "F": F},
        "correct": ans,
        "accepted_equivalents": [ans, f"({a}*sqrt(x) + {F})/x", f"{a}*x^(-1/2) + {F}*x^(-1)"],
        "variables": ["x"],
        "symbolic_config": {
            "variables": ["x"],
            "palette": ["sqrt()", "^", "/", "+", "-"],
            "placeholder": "Ej: 6/sqrt(x) + 20/x",
        },
        "ds": [
            ("D-Hab01-04", f"{a}*sqrt(x) + {F}", r"Reportaste el costo total $c(x) = @a@\sqrt{x} + @F@$ sin dividir entre la producción $x$ para hallar el costo medio."),
            ("D-Hab01-06", f"{a}/sqrt(x)", r"Omitiste prorratear el costo fijo medio $@F@/x$ al dividir $@a@\sqrt{x} + @F@$ entre la cantidad $x$."),
        ],
    }


def ver_hab01_os2(c, v):
    import sympy
    x = sympy.Symbol("x")
    try:
        target = v["a"] / sympy.sqrt(x) + v["F"] / x
        return sympy.simplify(sympy.sympify(str(c)) - target) == 0
    except Exception:
        return False


def gen_hab01_fib1(rng):
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


def ver_hab01_fib1(c, v):
    try:
        expected = int(v["p"] * v["x_hi"] - v["a"] * v["m_hi"] - v["F"])
        return abs(float(c) - expected) < 1e-6
    except Exception:
        return False


def gen_hab01_fib2(rng):
    for _ in range(40):
        m = rng.randint(3, 18)
        p = rng.randint(2, 9)
        k = m * p
        a = 2 * k
        ans = m * m
        d_nosq = m
        d_inv = k * p
        if _ok_sep([ans, d_nosq, d_inv]):
            break
    return {
        "vars": {"a": a, "k": k, "p": p, "m": m, "ans": ans, "d_nosq": d_nosq, "d_inv": d_inv},
        "correct": str(ans),
        "ds": [
            ("D-Hab01-02", str(d_nosq), r"Reportaste $\sqrt{x} = @k@/@p@ = @d_nosq@$ sin elevar al cuadrado para despejar el punto crítico $x_{\text{stat}}$."),
            ("D-Hab01-01", str(d_inv), r"Multiplicaste $@k@$ por $@p@$ dando $@d_inv@$ en vez de despejar $(@k@/@p@)^2$ desde $p = CMg(x)$ con $a=@a@$."),
        ],
    }


def ver_hab01_fib2(c, v):
    try:
        expected = int((v["k"] // v["p"]) ** 2)
        return abs(float(c) - expected) < 1e-6
    except Exception:
        return False


def gen_hab01_adv_ff(rng):
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


def ver_hab01_adv_ff(res):
    adv = res.get("adversarial_break") if isinstance(res, dict) else None
    if not isinstance(adv, dict):
        return False
    steps = adv.get("steps", [])
    f_steps = [s["id"] for s in steps if s.get("is_fallacy")]
    r_corr = [r["id"] for r in adv.get("reason_options", []) if r.get("is_correct")]
    return len(steps) >= 3 and f_steps == ["A3"] and r_corr == ["R_cs"]


def gen_hab01_adv_ce(rng):
    k = rng.randint(2, 8)
    a = 2 * k
    p = rng.randint(2, 6)
    F = rng.randint(10, 40)
    m_stat = k // p + 1
    k = m_stat * p
    a = 2 * k
    x_stat = m_stat * m_stat
    pi_stat = int(p * x_stat - a * m_stat - F)
    m_w = m_stat + 6
    x_w = m_w * m_w
    adv = {
        "mode": "counterexample",
        "prompt": r"Un analista afirma que $x_{\text{stat}} = @x_stat@$ maximiza $\pi(x) = @p@x - @a@\sqrt{x} - @F@$ (donde $\pi_{\text{stat}} = @pi_stat@$). Exhibe un nivel $x > 0$ con mayor beneficio:",
        "inputs": [
            {"id": "x", "label": "x", "type": "number", "min": 0.5, "max": 900, "step": 1, "placeholder": f"Ej: {x_w}"},
        ],
        "predicates": [
            {
                "id": "P_DOM",
                "expr": "x > 0",
                "distractor_id": "D-Hab01-01",
                "failure_rationale": r"En competencia con tecnología $c(x)=@a@\sqrt{x}+@F@$, el nivel productivo $x$ debe ser estrictamente positivo.",
            },
            {
                "id": "P_SUP",
                "expr": f"{p}*x - {a}*sqrt(x) - {F} > {pi_stat}",
                "distractor_id": "D-Hab01-05",
                "failure_rationale": r"El volumen $x$ propuesto no supera el beneficio estacionario $\pi_{\text{stat}} = @pi_stat@$ bajo $p=@p@$ y $F=@F@$.",
            },
        ],
        "trap_predicates": [
            {
                "expr": f"abs(x - {x_stat}) < 0.05",
                "distractor_id": "D-Hab01-02",
                "error_rationale": r"Evaluaste el propio mínimo local $x_{\text{stat}} = @x_stat@$ donde $\pi''(x) > 0$ minimiza beneficios.",
            },
        ],
        "computed_readouts": [
            {"label": r"$\pi(x)$", "expr": f"{p}*x - {a}*sqrt(x) - {F}"},
            {"label": r"$\pi(x) - \pi_{\text{stat}}$", "expr": f"{p}*x - {a}*sqrt(x) - {F} - ({pi_stat})"},
        ],
        "sample_witness": {"x": float(x_w)},
    }
    return {"vars": {"a": a, "p": p, "F": F, "x_stat": x_stat, "pi_stat": pi_stat}, "adversarial_break": adv}


def ver_hab01_adv_ce(res):
    adv = res.get("adversarial_break") if isinstance(res, dict) else None
    v = res.get("vars", {}) if isinstance(res, dict) else {}
    if not isinstance(adv, dict) or adv.get("mode") != "counterexample":
        return False
    x = (adv.get("sample_witness") or {}).get("x", 0)
    pi_x = v["p"] * x - v["a"] * math.sqrt(x) - v["F"]
    return x > 0 and pi_x > v["pi_stat"]


# ==============================================================================
# COMPETENCIA Hab-02 (Skill — 0 MC7, M=3, K=2 => 6 plantillas, 100% activo)
# ==============================================================================

def gen_hab02_ic1(rng):
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
            {"id": "pt_kink", "label": "Vértice no convexo", "x": 1, "y": 1, "color": "#dc2626"}
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
        "target_state": {"points": {"pt_kink": {"x": x_bar, "y": x2_kink}}},
    }
    return {"vars": {"p1": p1, "r_pct": r_pct, "x_bar": x_bar, "m": m}, "invariant_canvas": ic}


def ver_hab02_ic1(res):
    ic = res.get("invariant_canvas") if isinstance(res, dict) else None
    v = res.get("vars", {}) if isinstance(res, dict) else {}
    if not isinstance(ic, dict) or ic.get("mode") != "cartesian":
        return False
    invs = ic.get("invariants", [])
    kpos = next((i for i in invs if i.get("kind") == "point_coords"), None)
    expected_y = v.get("m", 0) - v.get("p1", 0) * v.get("x_bar", 0)
    pt_ts = ((ic.get("target_state") or {}).get("points") or {}).get("pt_kink") or {}
    return (
        kpos is not None
        and kpos.get("target_x") == v.get("x_bar")
        and kpos.get("target_y") == expected_y
        and pt_ts.get("x") == v.get("x_bar")
        and pt_ts.get("y") == expected_y
    )


def gen_hab02_ic2(rng):
    p1 = rng.choice([4, 6, 8])
    r_pct = rng.choice([25, 50])
    p1_disc = round(p1 * (100 - r_pct) / 100.0, 2)
    x_bar = rng.randint(2, 6)
    x2_kink = rng.randint(10, 22)
    m = p1 * x_bar + x2_kink
    ic = {
        "mode": "cartesian",
        "x_range": [0, 14],
        "y_range": [0, 36],
        "step": 0.5,
        "x_label": "x_1",
        "y_label": "x_2",
        "sliders": [
            {"id": "s_p1p", "label": "Precio marginal p_1'", "min": 1, "max": 8, "step": 0.5, "initial": 1}
        ],
        "fixed_curves": [
            {
                "id": "seg_b",
                "label": r"Frontera Tramo B ($x_1 \ge @x_bar@$)",
                "color": "#16a34a",
                "expression": f"{x2_kink} - s_p1p * max(0, x - {x_bar})",
                "domain": [x_bar, 14],
                "style": "solid",
            }
        ],
        "inequality": {"curve_id": "seg_b", "initial_style": "dashed", "initial_shade": "above"},
        "invariants": [
            {
                "id": "INV_INEQ",
                "kind": "inequality_state",
                "expected_style": "solid",
                "expected_shade": "below",
                "distractor_id": "D-Hab02-01",
                "error_rationale": r"La restricción presupuestaria débil $\le$ con descuento $@r_pct@\%$ exige borde sólido y sombreado inferior.",
            },
            {
                "id": "INV_SL_P",
                "kind": "slider_eq",
                "slider_id": "s_p1p",
                "target": p1_disc,
                "tolerance": 0.25,
                "distractor_id": "D-Hab02-02",
                "error_rationale": r"Ajusta el deslizador al precio efectivo $p_1(1-r)$ tras descontar $@r_pct@\%$ sobre $p_1=@p1@$ (con $m=@m@$).",
            },
        ],
        "target_state": {"inequalityStyle": "solid", "inequalityShade": "below", "sliders": {"s_p1p": p1_disc}},
    }
    return {"vars": {"p1": p1, "r_pct": r_pct, "x_bar": x_bar, "m": m, "p1_disc": p1_disc}, "invariant_canvas": ic}


def ver_hab02_ic2(res):
    ic = res.get("invariant_canvas") if isinstance(res, dict) else None
    v = res.get("vars", {}) if isinstance(res, dict) else {}
    if not isinstance(ic, dict) or ic.get("mode") != "cartesian":
        return False
    ts = ic.get("target_state") or {}
    return (
        ts.get("inequalityStyle") == "solid"
        and ts.get("inequalityShade") == "below"
        and abs(float((ts.get("sliders") or {}).get("s_p1p", -1)) - v.get("p1_disc", -2)) < 1e-6
    )


def gen_hab02_os1(rng):
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


def ver_hab02_os1(c, v):
    p1 = v.get("p1")
    return bool(p1) and str(c).replace(" ", "") in (f"{p1}*(1-r)", f"{p1}-{p1}*r")


def gen_hab02_os2(rng):
    p1 = rng.randint(3, 15)
    x_bar = rng.randint(2, 12)
    m = p1 * x_bar + rng.randint(8, 30)
    ans = f"{m} - {p1}*{x_bar} - {p1}*(1 - r)*(x1 - {x_bar})"
    return {
        "vars": {"p1": p1, "x_bar": x_bar, "m": m},
        "correct": ans,
        "accepted_equivalents": [ans, f"({m} - {p1}*{x_bar}) - {p1}*(1-r)*(x1 - {x_bar})"],
        "variables": ["x1", "r"],
        "symbolic_config": {
            "variables": ["x1", "r"],
            "palette": ["(", ")", "*", "-", "+"],
            "placeholder": "Ej: 24 - 4*3 - 4*(1-r)*(x1-3)",
        },
        "ds": [
            ("D-Hab02-02", f"{m} - {p1}*(1 - r)*x1", r"Omitiste el gasto pleno $@p1@ \cdot @x_bar@$ del primer tramo sobre la renta $m = @m@$ al formular el Tramo B."),
            ("D-Hab02-01", f"{m} - {p1}*{x_bar} - {p1}*r*(x1 - {x_bar})", r"Empleaste $r$ en lugar de $(1-r)$ para el precio efectivo tras superar $\bar{x}_1 = @x_bar@$ con $m=@m@$."),
        ],
    }


def ver_hab02_os2(c, v):
    import sympy
    x1, r = sympy.symbols("x1 r")
    try:
        target = v["m"] - v["p1"] * v["x_bar"] - v["p1"] * (1 - r) * (x1 - v["x_bar"])
        return sympy.simplify(sympy.sympify(str(c)) - target) == 0
    except Exception:
        return False


def gen_hab02_um_select(rng):
    p1 = rng.randint(3, 14)
    x_bar = rng.randint(4, 20)
    m = p1 * x_bar + rng.randint(10, 40)
    um = {
        "phase1_variables": {
            "prompt": r"Identifica los roles en el problema del consumidor con umbral $\bar{x}_1 = @x_bar@$ y renta $m = @m@$:",
            "roles": ["Variable endógena", "Parámetro exógeno"],
            "items": [
                {
                    "id": "S_x1",
                    "label": r"Demanda del bien 1 ($x_1$)",
                    "correct_role": "Variable endógena",
                    "distractor_id": "D-Hab02-05",
                    "error_rationale": r"La cantidad $x_1$ frente al umbral $@x_bar@$ es elegida óptimamente por el hogar dado $m=@m@$.",
                },
                {
                    "id": "S_m",
                    "label": r"Ingreso monetario $m = @m@$",
                    "correct_role": "Parámetro exógeno",
                    "error_rationale": r"La renta $m = @m@$ es un dato presupuestario fijo para $p_1 = @p1@$.",
                },
                {
                    "id": "S_xbar",
                    "label": r"Umbral tarifario $\bar{x}_1 = @x_bar@$",
                    "correct_role": "Parámetro exógeno",
                    "error_rationale": r"El quiebre $\bar{x}_1 = @x_bar@$ es impuesto exógenamente por la estructura tarifaria.",
                },
            ],
        },
        "phase2_assumptions": {
            "prompt": r"Selecciona las implicancias estructurales del quiebre en $\bar{x}_1 = @x_bar@$:",
            "options": [
                {
                    "id": "P2_NONCONV",
                    "content": r"El conjunto presupuestario pierde convexidad en $(\bar{x}_1, @m@ - @p1@ \cdot @x_bar@)$.",
                    "is_required": True,
                },
                {
                    "id": "P2_CAND",
                    "content": r"Deben compararse tangencias del Tramo A, Tramo B y el vértice $\bar{x}_1 = @x_bar@$.",
                    "is_required": True,
                },
                {
                    "id": "P2_UNIQ",
                    "content": r"La condición $TMS = p_1$ garantiza un óptimo interior único y continuo.",
                    "is_required": False,
                    "distractor_id": "D-Hab02-06",
                    "error_rationale": r"Con descuento tras $\bar{x}_1 = @x_bar@$, el conjunto es no convexo y la demanda salta discontinuamente.",
                },
            ],
        },
        "phase3_formulation": {
            "prompt": r"Elige el criterio válido de optimalidad global bajo ingreso $m = @m@$:",
            "input_mode": "select",
            "options": [
                {
                    "id": "OPT_GLOB",
                    "content": r"Evaluar $x^* = \arg\max \{u(x^A), u(x^{\text{kink}}), u(x^B)\}$ con $\bar{x}_1 = @x_bar@$.",
                    "is_correct": True,
                },
                {
                    "id": "OPT_KKT",
                    "content": r"Resolver un Lagrangiano único imponiendo $TMS = @p1@$ en todo el dominio.",
                    "is_correct": False,
                    "distractor_id": "D-Hab02-03",
                    "error_rationale": r"Un Lagrangiano único falla ante la no convexidad generada en $\bar{x}_1 = @x_bar@$ con $p_1 = @p1@$.",
                },
                {
                    "id": "OPT_NO_KINK",
                    "content": r"Descartar el vértice $\bar{x}_1 = @x_bar@$ por carecer de derivada en el quiebre.",
                    "is_correct": False,
                    "distractor_id": "D-Hab02-04",
                    "error_rationale": r"El vértice en $\bar{x}_1 = @x_bar@$ es óptimo cuando la $TMS$ yace entre $p_1(1-r)$ y $@p1@$.",
                },
            ],
        },
    }
    return {"vars": {"p1": p1, "x_bar": x_bar, "m": m}, "unstructured_model": um}


def ver_hab02_um_select(res):
    um = res.get("unstructured_model") if isinstance(res, dict) else None
    v = res.get("vars", {}) if isinstance(res, dict) else {}
    if not isinstance(um, dict) or not v.get("m"):
        return False
    p3 = um.get("phase3_formulation", {})
    req = [o["id"] for o in um["phase2_assumptions"]["options"] if o.get("is_required")]
    corr_p3 = [o["id"] for o in p3.get("options", []) if o.get("is_correct")]
    return p3.get("input_mode") == "select" and req == ["P2_NONCONV", "P2_CAND"] and corr_p3 == ["OPT_GLOB"]


def gen_hab02_um_sym(rng):
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


def ver_hab02_um_sym(res):
    um = res.get("unstructured_model") if isinstance(res, dict) else None
    v = res.get("vars", {}) if isinstance(res, dict) else {}
    if not isinstance(um, dict) or not v.get("p1"):
        return False
    p3 = um.get("phase3_formulation", {})
    ce = (p3.get("correct_expression") or {}).get("expression", "")
    expected = f"{v['p1']}*{v['x_bar']} + {v['p1']}*(1-r)*(x1 - {v['x_bar']})"
    return p3.get("input_mode") == "symbolic" and ce == expected


# ==============================================================================
# COMPETENCIA C-01 (Concept — 0 MC7, M=3, K=2 => 6 plantillas, 100% activo)
# ==============================================================================

def gen_c01_adv_ce(rng):
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
        "trap_predicates": [
            {
                "expr": f"(a1 + a2 >= {k_lvl} and floor(a1) + floor(a2) < {k_lvl}) or (b1 + b2 >= {k_lvl} and floor(b1) + floor(b2) < {k_lvl})",
                "distractor_id": "D-C01-05",
                "error_rationale": r"Evaluaste una canasta como suma continua $x_1 + x_2 \ge @k_lvl@$ ignorando el truncamiento entero $\lfloor x_i \rfloor$.",
            },
        ],
        "computed_readouts": [
            {"label": r"$M_1 = 0.5(a_1 + b_1)$", "expr": "0.5*(a1 + b1)"},
            {"label": r"$M_2 = 0.5(a_2 + b_2)$", "expr": "0.5*(a2 + b2)"},
            {"label": r"$u(M)$", "expr": "floor(0.5*(a1 + b1)) + floor(0.5*(a2 + b2))"},
        ],
        "sample_witness": {"a1": 1.0, "a2": float(k_lvl - 1), "b1": 2.0, "b2": float(k_lvl - 2)},
    }
    return {"vars": {"k_lvl": k_lvl}, "adversarial_break": adv}


def ver_c01_adv_ce(res):
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


def gen_c01_adv_ff(rng):
    k_lvl = rng.randint(4, 24)
    adv = {
        "mode": "find_fallacy",
        "prompt": r"Audita el intento de demostrar cuasiconcavidad para $u(x_1, x_2) = \lfloor x_1 \rfloor + \lfloor x_2 \rfloor$ en el nivel $k = @k_lvl@$:",
        "steps": [
            {
                "id": "H1",
                "label": "Paso 1",
                "content": r"Se plantea el conjunto contorno superior $U(@k_lvl@) = \{(x_1, x_2) \in \mathbb{R}_+^2 : \lfloor x_1 \rfloor + \lfloor x_2 \rfloor \ge @k_lvl@\}$.",
                "is_fallacy": False,
                "valid_explanation": "La definición del conjunto contorno superior es formalmente exacta.",
            },
            {
                "id": "H2",
                "label": "Paso 2",
                "content": r"Se toman derivadas parciales $u_1 = 1$, $u_2 = 1$ y hessiano orlado constante para evaluar curvatura alrededor de $@k_lvl@$.",
                "is_fallacy": True,
                "distractor_id": "D-C01-05",
                "error_rationale": r"La función $\lfloor x_1 \rfloor + \lfloor x_2 \rfloor$ en cota $@k_lvl@$ es discontinua en enteros y carece de derivadas diferenciales.",
            },
            {
                "id": "H3",
                "label": "Paso 3",
                "content": r"Al resultar el determinante orlado no negativo en el interior de los cuadros, se concluye cuasiconcavidad global.",
                "is_fallacy": False,
                "valid_explanation": "El criterio diferencial solo aplica bajo clase $C^2$; el quiebre ocurrió en el Paso 2 al diferenciar.",
            },
        ],
        "reason_options": [
            {
                "id": "R_DISC",
                "content": r"El operador piso introduce discontinuidades de salto en los enteros e invalida el cálculo diferencial.",
                "is_correct": True,
            },
            {
                "id": "R_CEIL",
                "content": r"Se debía redondear hacia arriba con función techo $\lceil x_i \rceil$ antes de calcular el determinante.",
                "is_correct": False,
                "distractor_id": "D-C01-06",
                "error_rationale": r"Sustituir $\lfloor x_i \rfloor$ por techo $\lceil x_i \rceil$ cambia la función y tampoco la hace diferenciable en cota $@k_lvl@$.",
            },
        ],
    }
    return {"vars": {"k_lvl": k_lvl}, "adversarial_break": adv}


def ver_c01_adv_ff(res):
    adv = res.get("adversarial_break") if isinstance(res, dict) else None
    if not isinstance(adv, dict) or adv.get("mode") != "find_fallacy":
        return False
    steps = adv.get("steps", [])
    return len(steps) >= 3 and [s["id"] for s in steps if s.get("is_fallacy")] == ["H2"]


def gen_c01_tree(rng):
    w1 = rng.randint(8, 32)
    w2 = rng.randint(1, 5)
    branch_map = [
        ("t1", ["e_top", "e1"], "T1"),
        ("t2", ["e_top", "e2"], "T2"),
        ("t3", ["e_bot", "e3"], "T3"),
        ("t4", ["e_bot", "e4"], "T4"),
    ]
    win_tid, req_edges, win_label = rng.choice(branch_map)
    nodes = [
        {"id": "n0", "label": "J1", "x": 80, "y": 150, "player": "J1"},
        {"id": "n1", "label": "J2a", "x": 240, "y": 80, "player": "J2"},
        {"id": "n2", "label": "J2b", "x": 240, "y": 220, "player": "J2"},
    ]
    ys = {"t1": 45, "t2": 115, "t3": 185, "t4": 255}
    for tid, _, lbl in branch_map:
        pay = f"({w1}, {w1})" if tid == win_tid else f"({w2}, 0)"
        nodes.append({"id": tid, "label": lbl, "x": 420, "y": ys[tid], "terminal": True, "payoff": pay})

    ic = {
        "mode": "tree",
        "width": 520,
        "height": 300,
        "interaction_mode": "both",
        "nodes": nodes,
        "edges": [
            {"id": "e_top", "from": "n0", "to": "n1", "label": "Cooperar"},
            {"id": "e_bot", "from": "n0", "to": "n2", "label": "Desviar"},
            {"id": "e1", "from": "n1", "to": "t1", "label": "C_2"},
            {"id": "e2", "from": "n1", "to": "t2", "label": "D_2"},
            {"id": "e3", "from": "n2", "to": "t3", "label": "C_2"},
            {"id": "e4", "from": "n2", "to": "t4", "label": "D_2"},
        ],
        "tree_invariants": {
            "required_edges": req_edges,
            "required_info_sets": [["n1", "n2"]],
            "distractor_id": "D-C01-03",
            "distractor_ids": ["D-C01-03", "D-C01-04"],
            "edge_error_rationale": "La senda óptima con pago dominante (@w1@, @w1@) exige activar exactamente las dos ramas hacia @win_label@.",
            "info_set_error_rationale": "El Jugador 2 no observa la acción previa de J1; debes agrupar sus dos nodos de decisión J2a y J2b en un conjunto de información.",
        },
    }
    return {"vars": {"w1": w1, "w2": w2, "win_label": win_label, "req_edges": req_edges}, "invariant_canvas": ic}


def ver_c01_tree(res):
    ic = res.get("invariant_canvas") if isinstance(res, dict) else None
    v = res.get("vars", {}) if isinstance(res, dict) else {}
    if not isinstance(ic, dict) or ic.get("mode") != "tree":
        return False
    ti = ic.get("tree_invariants", {})
    return sorted(ti.get("required_edges", [])) == sorted(v.get("req_edges", [])) and ti.get("required_info_sets") == [["n1", "n2"]]


def gen_c01_cart(rng):
    k_lvl = rng.randint(4, 12)
    a1, a2 = 1, k_lvl - 1
    b1, b2 = 2, k_lvl - 2
    mx, my = 1.5, k_lvl - 1.5
    ic = {
        "mode": "cartesian",
        "x_range": [0, 6],
        "y_range": [0, 14],
        "step": 0.5,
        "x_label": "x_1",
        "y_label": "x_2",
        "fixed_points": [
            {"id": "fp_A", "x": a1, "y": a2, "label": f"A({a1},{a2})", "color": "#16a34a"},
            {"id": "fp_B", "x": b1, "y": b2, "label": f"B({b1},{b2})", "color": "#16a34a"},
        ],
        "interactive_points": [
            {"id": "pt_mid", "label": "M", "x": 4, "y": 1, "color": "#dc2626"}
        ],
        "invariants": [
            {
                "id": "INV_MID_POS",
                "kind": "point_coords",
                "point_id": "pt_mid",
                "target_x": mx,
                "target_y": my,
                "tolerance": 0.35,
                "distractor_id": "D-C01-02",
                "error_rationale": r"Calcula el punto medio convexo $M = 0.5A + 0.5B$ promediando $A=(@a1@,@a2@)$ y $B=(@b1@,@b2@)$ para cota $k=@k_lvl@$.",
            },
            {
                "id": "INV_DROP",
                "kind": "point_in_region",
                "point_id": "pt_mid",
                "expr": f"floor(x) + floor(y) < {k_lvl}",
                "distractor_id": "D-C01-01",
                "error_rationale": r"En el punto medio debe caer la utilidad escalonada $\lfloor x_1 \rfloor + \lfloor x_2 \rfloor < @k_lvl@$.",
            },
        ],
        "target_state": {"points": {"pt_mid": {"x": mx, "y": my}}},
    }
    return {"vars": {"k_lvl": k_lvl, "a1": a1, "a2": a2, "b1": b1, "b2": b2}, "invariant_canvas": ic}


def ver_c01_cart(res):
    ic = res.get("invariant_canvas") if isinstance(res, dict) else None
    v = res.get("vars", {}) if isinstance(res, dict) else {}
    if not isinstance(ic, dict) or ic.get("mode") != "cartesian":
        return False
    pt = ((ic.get("target_state") or {}).get("points") or {}).get("pt_mid") or {}
    return abs(pt.get("x", 0) - 1.5) < 1e-6 and abs(pt.get("y", 0) - (v.get("k_lvl", 0) - 1.5)) < 1e-6


def gen_c01_fib1(rng):
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


def ver_c01_fib1(c, v):
    try:
        expected = math.floor(v["x1"]) + math.floor(v["x2"])
        return abs(float(c) - expected) < 1e-6
    except Exception:
        return False


def gen_c01_fib2(rng):
    for _ in range(40):
        p1 = rng.randint(1, 8)
        p2 = rng.randint(1, 8)
        gap = rng.randint(2, 16)
        k_lvl = p1 + p2 + gap
        x1 = round(p1 + rng.choice([0.3, 0.4, 0.6]), 1)
        x2 = round(p2 + rng.choice([0.2, 0.5, 0.7]), 1)
        u_m = p1 + p2
        ans = k_lvl - u_m
        d_ceil = k_lvl - (p1 + p2 + 2)
        d_cont = round(k_lvl - (x1 + x2), 1)
        if d_ceil != ans and d_cont != ans:
            break
    return {
        "vars": {"x1": x1, "x2": x2, "k_lvl": k_lvl, "u_m": u_m, "ans": ans},
        "correct": str(ans),
        "ds": [
            ("D-C01-06", str(d_ceil), r"Restaste la suma techo $\lceil @x1@ \rceil + \lceil @x2@ \rceil$ a $@k_lvl@$ en vez del operador piso truncado."),
            ("D-C01-05", str(d_cont), r"Calculaste el déficit con suma continua $@x1@ + @x2@$ frente a $@k_lvl@$ omitiendo truncar cada coordenada."),
        ],
    }


def ver_c01_fib2(c, v):
    try:
        expected = v["k_lvl"] - (math.floor(v["x1"]) + math.floor(v["x2"]))
        return abs(float(c) - expected) < 1e-6
    except Exception:
        return False


# ==============================================================================
# COMPETENCIA C-02 (Concept — 1 MC7, M=4 => 1 MC7 + 3*2 = 7 plantillas, 85.7% activo)
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


def gen_c02_dag_shephard(rng):
    j_idx = rng.randint(1, 25)
    u_bar = rng.randint(2, 18)
    dag = {
        "goal": r"Demostrar el Lema de Shephard para la demanda compensada $x_{@j_idx@}^h(p, @u_bar@)$ vía Teorema de la Envolvente:",
        "steps": [
            {
                "id": "E1",
                "content": r"Plantear el Lagrangiano del gasto mínimo: $\mathcal{L}(x,\mu) = p \cdot x + \mu(@u_bar@ - U(x))$.",
                "justification": "Lagrangiano de minimización",
                "is_fallacy": False,
            },
            {
                "id": "E2",
                "content": r"Evaluar la función valor en el óptimo compensado: $e(p, @u_bar@) = \mathcal{L}(x^h(p,@u_bar@), \mu^*)$.",
                "justification": "Función valor óptima",
                "is_fallacy": False,
            },
            {
                "id": "E3",
                "content": r"Aplicar Teorema de la Envolvente diferenciando $e(p,@u_bar@)$ respecto a $p_{@j_idx@}$ (términos indirectos se anulan).",
                "justification": "Teorema de la Envolvente",
                "is_fallacy": False,
            },
            {
                "id": "E4",
                "content": r"Concluir $\frac{\partial e(p,@u_bar@)}{\partial p_{@j_idx@}} = x_{@j_idx@}^h(p, @u_bar@)$ con signo positivo.",
                "justification": "Lema de Shephard",
                "is_fallacy": False,
            },
            {
                "id": "E_BAD",
                "content": r"Concluir que $x_{@j_idx@}^h(p, @u_bar@) = -\frac{\partial e/\partial p_{@j_idx@}}{\partial e/\partial u}$ dividiendo por $\partial e/\partial u$.",
                "justification": "Teorema de la Envolvente",
                "is_fallacy": True,
                "distractor_id": "D-C02-04",
                "error_rationale": r"Confunde Shephard con Roy en el bien $@j_idx@$ bajo nivel $@u_bar@$: la derivada directa de $e(p,u)$ ya entrega $x^h$.",
            },
        ],
        "edges": [["E1", "E2"], ["E2", "E3"], ["E3", "E4"]],
        "require_justification": True,
        "justification_bank": [
            "Lagrangiano de minimización",
            "Función valor óptima",
            "Teorema de la Envolvente",
            "Lema de Shephard",
        ],
    }
    return {"vars": {"j_idx": j_idx, "u_bar": u_bar}, "proof_dag": dag}


def ver_c02_dag_shephard(res):
    dag = res.get("proof_dag") if isinstance(res, dict) else None
    if not isinstance(dag, dict):
        return False
    valid_ids = [s["id"] for s in dag.get("steps", []) if not s.get("is_fallacy")]
    fallacy_ids = [s["id"] for s in dag.get("steps", []) if s.get("is_fallacy")]
    return len(valid_ids) == 4 and fallacy_ids == ["E_BAD"]


def gen_c02_os1(rng):
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


def ver_c02_os1(c, v):
    k = v.get("k")
    return bool(k) and str(c).replace(" ", "") in (f"{k}*m/p", f"({k}*m)/p", f"{k}*(m/p)")


def gen_c02_os2(rng):
    k = rng.randint(2, 16)
    F = rng.randint(3, 25)
    ans = f"{2 * k}*p*u"
    return {
        "vars": {"k": k, "F": F},
        "correct": ans,
        "accepted_equivalents": [ans, f"2*{k}*p*u", f"{2 * k}*u*p"],
        "variables": ["p", "u"],
        "symbolic_config": {
            "variables": ["p", "u"],
            "palette": ["*", "+", "-", "^"],
            "placeholder": "Ej: 6*p*u",
        },
        "ds": [
            ("D-C02-05", f"-{2 * k}*p*u", r"Introdujiste un signo negativo espurio al aplicar Shephard sobre $e(p,u)=@F@+@k@p^2 u$; la demanda compensada crece positivamente en $p$."),
            ("D-C02-04", f"{k}*p^2", r"Derivaste respecto a $u$ en lugar de aplicar Shephard diferenciando $e(p,u)=@F@+@k@p^2 u$ respecto al precio $p$."),
        ],
    }


def ver_c02_os2(c, v):
    import sympy
    p, u = sympy.symbols("p u")
    try:
        return sympy.simplify(sympy.sympify(str(c)) - 2 * v["k"] * p * u) == 0
    except Exception:
        return False


def gen_c02_cm1(rng):
    idx_b = rng.randint(1, 30)
    cm = {
        "left_title": "Teorema / Identidad Dual",
        "right_title": "Expresión Analítica Exacta",
        "premises": [
            {"id": "M_roy", "content": r"Identidad de Roy para demanda ordinaria $x_{@idx_b@}^d(p,m)$"},
            {"id": "M_shep", "content": r"Lema de Shephard para demanda compensada $x_{@idx_b@}^h(p,u)$"},
            {"id": "M_dual", "content": r"Relación inversa entre gasto mínimo y utilidad indirecta"},
            {"id": "M_hom", "content": r"Homogeneidad de grado cero de $v(p,m)$ para el bien $x_{@idx_b@}$"},
        ],
        "targets": [
            {"id": "R_roy", "content": r"$-\frac{\partial v/\partial p_{@idx_b@}}{\partial v/\partial m}$"},
            {"id": "R_shep", "content": r"$\frac{\partial e(p,u)}{\partial p_{@idx_b@}}$"},
            {"id": "R_dual", "content": r"$e(p, v(p,m)) \equiv m$"},
            {"id": "R_hom", "content": r"$v(\lambda p, \lambda m) \equiv v(p,m)$ para $\lambda > 0$"},
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
        "correct_pairs": {"M_roy": "R_roy", "M_shep": "R_shep", "M_dual": "R_dual", "M_hom": "R_hom"},
    }
    return {"vars": {"idx_b": idx_b}, "concept_matching": cm}


def ver_c02_cm1(res):
    cm = res.get("concept_matching") if isinstance(res, dict) else None
    return isinstance(cm, dict) and cm.get("correct_pairs") == {"M_roy": "R_roy", "M_shep": "R_shep", "M_dual": "R_dual", "M_hom": "R_hom"}


def gen_c02_cm2(rng):
    idx_d = rng.randint(1, 25)
    cm = {
        "left_title": "Error en la Derivación Dual",
        "right_title": "Consecuencia Analítica",
        "premises": [
            {"id": "E_umu", "content": r"Suponer $\partial e/\partial u = 1$ sin diferenciar $m \equiv e(p,v(p,m))$ respecto a $m$"},
            {"id": "E_shep", "content": r"Sustituir $\partial e/\partial p_{@idx_d@}$ sin invocar el Lema de Shephard"},
            {"id": "E_hom", "content": r"Afirmar que $e(p, v(p,m)) = u$ para el bien $x_{@idx_d@}$"},
            {"id": "E_conc", "content": r"Suponer convexidad de $e(p,u)$ en precios para el bien $x_{@idx_d@}$"},
        ],
        "targets": [
            {"id": "C_umu", "content": r"Omite el factor $(\partial v/\partial m)^{-1}$ en la regla de la cadena"},
            {"id": "C_shep", "content": r"Rompe el puente $\partial e/\partial p_{@idx_d@} = x_{@idx_d@}^h(p,u)$"},
            {"id": "C_hom", "content": r"Confunde la identidad de gasto mínimo $m$ con nivel ordinal $u$"},
            {"id": "C_conc", "content": r"Viola la matriz de Slutsky negativa semidefinida en $x_{@idx_d@}^h$"},
            {
                "id": "C_dist1",
                "content": r"Garantiza que $v(p,m)$ es homogénea de grado uno en precios",
                "is_distractor": True,
                "distractor_id": "D-C02-06",
                "error_rationale": r"Para el bien $x_{@idx_d@}$, $v(p,m)$ es homogénea de grado cero en $(p,m)$, nunca de grado uno.",
            },
            {
                "id": "C_dist2",
                "content": r"Invierte el cociente $-\frac{\partial v/\partial m}{\partial v/\partial p_{@idx_d@}}$",
                "is_distractor": True,
                "distractor_id": "D-C02-03",
                "error_rationale": r"Invertir derivadas en $x_{@idx_d@}$ altera las unidades monetarias de la demanda marshalliana.",
            },
        ],
        "correct_pairs": {"E_umu": "C_umu", "E_shep": "C_shep", "E_hom": "C_hom", "E_conc": "C_conc"},
    }
    return {"vars": {"idx_d": idx_d}, "concept_matching": cm}


def ver_c02_cm2(res):
    cm = res.get("concept_matching") if isinstance(res, dict) else None
    return isinstance(cm, dict) and cm.get("correct_pairs") == {"E_umu": "C_umu", "E_shep": "C_shep", "E_hom": "C_hom", "E_conc": "C_conc"}


def gen_c02_mc7(rng):
    for _ in range(40):
        p0 = rng.choice([2, 3, 4, 5, 6])
        q_base = rng.randint(2, 14)
        k = rng.randint(2, 7)
        c_val = rng.randint(3, 18)
        m0 = p0 * q_base
        ans = k * q_base
        d1 = -ans
        d2 = k + q_base
        d3 = m0 + k
        d4 = c_val + k + p0
        d5 = abs(m0 - k * p0) if m0 != k * p0 else m0 + p0 + k
        d6 = k * m0 + c_val
        ds_vals = [d1, d2, d3, d4, d5, d6]
        if _ok_sep([ans, *ds_vals]):
            break
    dids = ["D-C02-01", "D-C02-02", "D-C02-03", "D-C02-04", "D-C02-05", "D-C02-06"]
    rats = {
        "D-C02-01": r"Error de signo en la Identidad de Roy con $p=@p0@$ y $m=@m0@$: el cociente $-(-@k@/@p0@)/(1/@m0@)$ cancela ambos signos negativos.",
        "D-C02-02": r"Sumaste $@k@ + @m0@/@p0@$ asumiendo $\partial e/\partial u = 1$ en lugar de multiplicar por $m = @m0@$ al despejar.",
        "D-C02-03": r"Alteraste el cociente entre $\partial v/\partial p$ y $\partial v/\partial m$ evaluado en $p=@p0@$ y renta $m=@m0@$.",
        "D-C02-04": r"Confundiste la utilidad indirecta evaluada con constante $@c_val@$ y precio $@p0@$ con la demanda ordinaria.",
        "D-C02-05": r"Omitiste el paso por el Lema de Shephard combinando erróneamente $m=@m0@$ y $@k@ \cdot @p0@$ sin dividir.",
        "D-C02-06": r"Confundiste la inversión dual en $m=@m0@$ sin dividir entre el precio $p=@p0@$ y sumando $@c_val@$.",
    }
    return {
        "vars": {"p0": p0, "m0": m0, "k": k, "c_val": c_val, "ans": ans},
        "correct": str(ans),
        "ds": [(did, str(val), rats[did]) for did, val in zip(dids, ds_vals)],
    }


def ver_c02_mc7(c, v):
    try:
        expected = v["k"] * (v["m0"] / v["p0"])
        val = float(str(c).strip().strip("$").strip())
        return abs(val - expected) < 1e-6
    except Exception:
        return False


# ==============================================================================
# STEMS & HINTS (disjuntos por Jaccard < 0.70 y con >= 4 variantes cada uno)
# ==============================================================================

stems_hab01_os1 = [
    r"Para la función de costo total $c(x) = @a@\sqrt{x} + @F@$ ($k = @k@ = @a@/2$), obtenga la expresión simbólica exacta del costo marginal $CMg(x)$ en función de `x`:",
    r"Dada la tecnología $c(x) = @a@\sqrt{x} + @F@$ ($k = @k@$), derive algebraicamente $CMg(x) = c'(x)$ en términos de `x`:",
    r"Calcule la fórmula simbólica de $CMg(x)$ correspondiente al costo $c(x) = @a@\sqrt{x} + @F@$ (con parámetro $k = @k@$):",
    r"Determine simbólicamente el costo marginal $CMg(x)$ para $c(x) = @a@\sqrt{x} + @F@$ donde el coeficiente reducido es $k = @k@$:",
]

stems_hab01_os2 = [
    r"Calcule el costo medio total $CMe(x) = c(x)/x$ para la planta con tecnología $c(x) = @a@\sqrt{x} + @F@$ en términos de `x`:",
    r"Exprese simbólicamente el costo promedio por unidad producida cuando $c(x) = @a@\sqrt{x} + @F@$ en función de `x`:",
    r"Divida el costo total $c(x) = @a@\sqrt{x} + @F@$ por la cantidad $x > 0$ para formular $CMe(x)$ en `x`:",
    r"Escriba la regla algebraica del costo unitario medio para tecnología $c(x) = @a@\sqrt{x} + @F@$ usando `x`:",
]

stems_hab01_fib1 = [
    r"Con $c(x) = @a@\sqrt{x} + @F@$ ($k = @k@$) y precio $p = @p@$, la CPO anula $\pi'(x)$ en $x_{\text{stat}} = @x_stat@$ ($\pi_{\text{stat}} = @pi_stat@$). Calcule $\pi(x)$ al expandir a $x = @x_hi@$ ($\sqrt{@x_hi@} = @m_hi@$):",
    r"Evalúe el beneficio competitivo $\pi(@x_hi@)$ cuando $p = @p@$, $c(x) = @a@\sqrt{x} + @F@$ ($k = @k@$), frente al mínimo en $x_{\text{stat}} = @x_stat@$ ($\pi_{\text{stat}} = @pi_stat@$, $\sqrt{@x_hi@} = @m_hi@$):",
    r"Si $p = @p@$ y $c(x) = @a@\sqrt{x} + @F@$ ($k = @k@$), determine el beneficio exacto en $x = @x_hi@$ ($\sqrt{@x_hi@} = @m_hi@$) evitando el mínimo $x_{\text{stat}} = @x_stat@$ ($\pi_{\text{stat}} = @pi_stat@$):",
    r"Una firma con $c(x) = @a@\sqrt{x} + @F@$ ($k = @k@$) y $p = @p@$ descarta $x_{\text{stat}} = @x_stat@$ ($\pi_{\text{stat}} = @pi_stat@$) y produce $x = @x_hi@$ ($\sqrt{@x_hi@} = @m_hi@$). Halle $\pi(@x_hi@)$:",
]

stems_hab01_fib2 = [
    r"Para la empresa competitiva con $p = @p@$ y costo $c(x) = @a@\sqrt{x} + 10$ ($k = @k@$), despeje numéricamente la escala estacionaria $x_{\text{stat}}$ donde $\pi'(x) = 0$:",
    r"Iguale el precio $p = @p@$ al costo marginal de $c(x) = @a@\sqrt{x} + 10$ ($k = @k@$) y halle el punto crítico $x_{\text{stat}}$:",
    r"¿En qué nivel productivo $x_{\text{stat}}$ se anula la derivada del beneficio si $p = @p@$ y $c(x) = @a@\sqrt{x} + 10$ ($k = @k@$) con costo marginal $c'(x)$?",
    r"Dada la función $c(x) = @a@\sqrt{x} + 10$ ($k = @k@$), resuelva la ecuación $p = @k@/\sqrt{x}$ para $p = @p@$ reportando el valor entero exacto de $x_{\text{stat}}$:",
]

stems_hab01_adv_ff = [
    r"Un alumno afirma maximizar beneficios con $c(x) = @b_dbl@\sqrt{x} + @F@$ ($b=@b@$) y $p = @p_val@$ igualando $p = CMg(x)$. Detecte el paso falaz y su justificación:",
    r"Audite esta deducción competitiva para $c(x) = @b_dbl@\sqrt{x} + @F@$ ($b=@b@$) a precio $p = @p_val@$ y señale el quiebre de segundo orden:",
    r"Examine el procedimiento propuesto bajo $c(x) = @b_dbl@\sqrt{x} + @F@$ ($b=@b@$, $p=@p_val@$). Identifique la afirmación errónea y el motivo correcto:",
    r"Caza de falacias para $c(x) = @b_dbl@\sqrt{x} + @F@$ con $b = @b@$ y precio $p = @p_val@$: marque el paso inválido y seleccione la explicación analítica:",
]

stems_hab01_adv_ce = [
    r"Refute en la Arena Adversarial que $x_{\text{stat}} = @x_stat@$ ($\pi_{\text{stat}} = @pi_stat@$) maximiza $\pi(x) = @p@x - @a@\sqrt{x} - @F@$ ingresando un nivel $x > 0$ con mayor beneficio:",
    r"Proponga un contraejemplo productivo $x > 0$ que demuestre que $\pi(x) = @p@x - @a@\sqrt{x} - @F@$ supera el valor crítico $@pi_stat@$ alcanzado en $x_{\text{stat}} = @x_stat@$:",
    r"Construya un testigo numérico $x > 0$ para refutar la optimalidad de $x_{\text{stat}} = @x_stat@$ bajo $p = @p@$, $a = @a@$ y costo fijo $F = @F@$ ($\pi_{\text{stat}} = @pi_stat@$):",
    r"Encuentre una escala $x > 0$ donde la firma con $c(x) = @a@\sqrt{x} + @F@$ y $p = @p@$ obtenga utilidad estrictamente mayor a $\pi(@x_stat@) = @pi_stat@$:",
]

stems_hab02_ic1 = [
    r"Con ingreso $m = @m@$, precio $p_1 = @p1@$, $p_2 = 1$ y descuento $r = @r_pct@\%$ tras superar $\bar{x}_1 = @x_bar@$, deduce el excedente $x_2^*$ y ubica el vértice no convexo:",
    r"Dada la restricción por tramos con renta $m = @m@$, tarifa $p_1 = @p1@$, $p_2 = 1$ y descuento marginal $r = @r_pct@\%$ desde $\bar{x}_1 = @x_bar@$, sitúa el punto de quiebre:",
    r"Analiza en el lienzo el quiebre presupuestario con $m = @m@$, $p_1 = @p1@$, $p_2 = 1$ y descuento $r = @r_pct@\%$ a partir de $\bar{x}_1 = @x_bar@$, marcando el vértice:",
    r"Localiza geométricamente el ángulo entrante no convexo bajo $m = @m@$, $p_1 = @p1@$, $p_2 = 1$, umbral $\bar{x}_1 = @x_bar@$ y descuento $r = @r_pct@\%$:",
]

stems_hab02_ic2 = [
    r"En el Tramo B ($x_1 \ge @x_bar@$) con tarifa inicial $p_1 = @p1@$, renta $m = @m@$ y descuento $@r_pct@\%$, configure estilo de frontera factible $\le$, región inferior y deslizador:",
    r"Ajuste el deslizador del precio descontado para $p_1 = @p1@$ con rebaja $@r_pct@\%$ tras $\bar{x}_1 = @x_bar@$ ($m = @m@$) y trace borde sólido con sombreado debajo:",
    r"Modele en el plano la desigualdad presupuestaria del segundo tramo ($m = @m@$, $p_1 = @p1@$, descuento $@r_pct@\%$ desde $\bar{x}_1 = @x_bar@$) fijando el deslizador:",
    r"Determine borde, semiplano factible y parámetro marginal en el deslizador si el precio $@p1@$ recibe descuento $@r_pct@\%$ después de $@x_bar@$ ($m = @m@$):",
]

stems_hab02_os1 = [
    r"Con precio inicial $p_1 = @p1@$, umbral $\bar{x}_1 = @x_bar@$ y descuento `r` en el tramo $x_1 > @x_bar@$, escriba simbólicamente el precio efectivo unitario:",
    r"Exprese en función de `r` el costo marginal por unidad adicional cuando $x_1 > @x_bar@$ dado $\bar{x}_1 = @x_bar@$ y $p_1 = @p1@$:",
    r"Para el Tramo B ($x_1 > @x_bar@$) tras $\bar{x}_1 = @x_bar@$ con precio base $p_1 = @p1@$ y descuento `r`, ingrese la fórmula simbólica neta:",
    r"Determine simbólicamente (en `r`) la pendiente absoluta del segundo tramo $x_1 > @x_bar@$ tras $\bar{x}_1 = @x_bar@$ con $p_1 = @p1@$:",
]

stems_hab02_os2 = [
    r"Despeje $x_2$ en función de `x1` y `r` para el segundo tramo ($x_1 > @x_bar@$) cuando la renta es $m = @m@$, $p_1 = @p1@$ y $p_2 = 1$:",
    r"Formule la frontera presupuestaria $x_2(x_1, r)$ válida tras superar $\bar{x}_1 = @x_bar@$ con ingreso $m = @m@$, $p_1 = @p1@$ y $p_2 = 1$:",
    r"Escriba simbólicamente en `x1` y `r` el consumo máximo $x_2$ ($p_2 = 1$) tras superar $\bar{x}_1 = @x_bar@$ ($x_1 > @x_bar@$) con presupuesto $m = @m@$ y tarifa inicial $p_1 = @p1@$:",
    r"Obtenga $x_2$ expresada en `x1` y `r` sobre el segmento con descuento por volumen ($\bar{x}_1 = @x_bar@$, $m = @m@$, $p_1 = @p1@$, $p_2 = 1$):",
]

stems_hab02_um1 = [
    r"Un consumidor enfrenta ingreso $m = @m@$, precio $p_1 = @p1@$ hasta $\bar{x}_1 = @x_bar@$ y rebaja posterior. Ejecute el diagnóstico Stage 0 para elegir el criterio de optimalidad:",
    r"Audite las tres fases Stage 0 para el problema con descuento tras $\bar{x}_1 = @x_bar@$ ($m = @m@$, $p_1 = @p1@$) seleccionando la regla global correcta:",
    r"Clasifique variables, no convexidad y criterio global en Stage 0 antes de optimizar la cesta cuando $m = @m@$, $p_1 = @p1@$ y umbral $\bar{x}_1 = @x_bar@$:",
    r"Complete el modelado guiado Stage 0 de selección para la restricción por bloques con renta $m = @m@$, precio $@p1@$ y corte en $\bar{x}_1 = @x_bar@$:",
]

stems_hab02_um2 = [
    r"Un consumidor paga $p_1 = @p1@$ hasta $\bar{x}_1 = @x_bar@$ y recibe descuento `r` por cada unidad adicional ($x_1 > @x_bar@$). Modele variables, supuestos y ecuación de gasto total en Stage 0:",
    r"Complete las tres fases Stage 0 para formular algebraicamente en `x1` y `r` el gasto del bien 1 en el Tramo B ($x_1 > @x_bar@$, $\bar{x}_1 = @x_bar@$) con tarifa base $p_1 = @p1@$:",
    r"Formalice en Stage 0 el presupuesto por bloques ($p_1 = @p1@$, umbral $\bar{x}_1 = @x_bar@$, tramo $x_1 > @x_bar@$, descuento `r`) culminando con el gasto en `x1` y `r`:",
    r"Resuelva el modelado progresivo Stage 0 hasta escribir simbólicamente el gasto en bien 1 para $x_1 > @x_bar@$ con $\bar{x}_1 = @x_bar@$, $p_1 = @p1@$ y descuento `r`:",
]

stems_c01_adv_ce = [
    r"Dada $u(x_1, x_2) = \lfloor x_1 \rfloor + \lfloor x_2 \rfloor$, refuta la convexidad del contorno superior en $k = @k_lvl@$ ingresando canastas $A=(a_1,a_2)$ y $B=(b_1,b_2)$ cuyo punto medio caiga debajo:",
    r"Encuentra un contraejemplo numérico $A=(a_1, a_2)$ y $B=(b_1, b_2)$ para $u(x_1,x_2) = \lfloor x_1 \rfloor + \lfloor x_2 \rfloor$ con cota $k = @k_lvl@$ donde $u(0.5A+0.5B) < @k_lvl@$:",
    r"Demuestra en la Arena Adversarial que $u(x_1, x_2) = \lfloor x_1 \rfloor + \lfloor x_2 \rfloor$ no es cuasicóncava exhibiendo un testigo $A=(a_1, a_2)$, $B=(b_1, b_2)$ para $k = @k_lvl@$:",
    r"Propón coordenadas válidas $A=(a_1,a_2)$ y $B=(b_1,b_2)$ dentro del contorno de $u(x_1, x_2) = \lfloor x_1 \rfloor + \lfloor x_2 \rfloor$ en cota $k = @k_lvl@$ cuya combinación media viole la convexidad:",
]

stems_c01_adv_ff = [
    r"Un estudiante intenta probar con cálculo diferencial que $u(x_1, x_2) = \lfloor x_1 \rfloor + \lfloor x_2 \rfloor$ es cuasicóncava en $k = @k_lvl@$. Detecte el paso inválido y su motivo:",
    r"Audite esta supuesta demostración por hessiano orlado sobre la utilidad parte entera en cota $@k_lvl@$ señalando la falacia:",
    r"Identifique en qué paso quiebra el argumento diferencial aplicado a $u(x_1, x_2) = \lfloor x_1 \rfloor + \lfloor x_2 \rfloor$ en nivel $@k_lvl@$:",
    r"Localice la ruptura axiomática al aplicar derivadas parciales sobre contornos escalonados en $k = @k_lvl@$ y elija su razón formal:",
]

stems_c01_tree = [
    r"En el árbol extensivo de información imperfecta con pago óptimo $(@w1@, @w1@)$ en `@win_label@` (y pagos $(@w2@, 0)$ en desvíos), seleccione las ramas hacia `@win_label@` y agrupe los nodos indistinguibles de J2:",
    r"Trace en el árbol de juego la trayectoria hacia `@win_label@` con pago $(@w1@, @w1@)$ frente a $(@w2@, 0)$ y forme el conjunto de información correcto para `J2`:",
    r"Marque las aristas que conducen al nodo terminal `@win_label@` ($(@w1@, @w1@)$ vs $(@w2@, 0)$) e indique la partición informacional entre `J2a` y `J2b`:",
    r"Configure en el árbol interactivo las acciones hacia `@win_label@` con utilidad $(@w1@, @w1@)$ (alternativa $(@w2@, 0)$) junto al conjunto de información de `J2`:",
]

stems_c01_cart = [
    r"Dados los extremos $A=(@a1@,@a2@)$ y $B=(@b1@,@b2@)$ en el contorno $\lfloor x_1 \rfloor + \lfloor x_2 \rfloor \ge @k_lvl@$, mueve el punto `M` a la semisuma $0.5A + 0.5B$ verificando la caída debajo de $@k_lvl@$:",
    r"Ubica sobre el plano el punto medio convexo `M` entre $A=(@a1@,@a2@)$ y $B=(@b1@,@b2@)$ donde se rompe el contorno superior de cota $k = @k_lvl@$:",
    r"En el lienzo cartesiano de la utilidad piso con cota $@k_lvl@$, sitúa el marcador `M` exactamente en el promedio aritmético de $A=(@a1@,@a2@)$ y $B=(@b1@,@b2@)$:",
    r"Localiza el testigo convexo `M` generado por la combinación equitativa de $A=(@a1@,@a2@)$ y $B=(@b1@,@b2@)$ bajo umbral $k = @k_lvl@$:",
]

stems_c01_fib1 = [
    r"Calcule el valor entero exacto de $u(x_1, x_2) = \lfloor x_1 \rfloor + \lfloor x_2 \rfloor$ evaluado en la canasta fraccionaria $(x_1, x_2) = (@x1@, @x2@)$:",
    r"Determine numéricamente $u(x_1, x_2) = \lfloor x_1 \rfloor + \lfloor x_2 \rfloor$ evaluada en $(x_1, x_2) = (@x1@, @x2@)$:",
    r"Para $(x_1, x_2) = (@x1@, @x2@)$, evalúe $u(x_1, x_2) = \lfloor x_1 \rfloor + \lfloor x_2 \rfloor$ e ingrese el resultado numérico exacto:",
    r"Evalúe sin aproximaciones continuas la utilidad $u(x_1, x_2) = \lfloor x_1 \rfloor + \lfloor x_2 \rfloor$ en la canasta $(x_1, x_2) = (@x1@, @x2@)$:",
]

stems_c01_fib2 = [
    r"Para el umbral $k = @k_lvl@$ y el punto medio $M = (@x1@, @x2@)$, calcule el déficit entero $k - u(M)$ donde $u(x_1, x_2) = \lfloor x_1 \rfloor + \lfloor x_2 \rfloor$:",
    r"¿Cuántas unidades por debajo de la cota $k = @k_lvl@$ cae la utilidad parte entera en $M = (@x1@, @x2@)$?",
    r"Calcule la brecha $k - (\lfloor @x1@ \rfloor + \lfloor @x2@ \rfloor)$ cuando el contorno superior exige al menos $k = @k_lvl@$:",
    r"Determine exactamente cuánto falta al valor escalonado $u(@x1@, @x2@)$ para alcanzar el nivel de utilidad $k = @k_lvl@$:",
]

stems_c02_dag1 = [
    r"A partir de la identidad $m \equiv e(p, v(p,m))$, encadene los pasos y justificaciones para derivar la Identidad de Roy de $x_{@g_idx@}$ descartando la falacia:",
    r"Construya en ProofDAG la demostración de la Identidad de Roy para $x_{@g_idx@}$ a partir de $m \equiv e(p, v(p,m))$:",
    r"Ordene la deducción analítica formal de la Identidad de Roy de $x_{@g_idx@}$ desde $m \equiv e(p, v(p,m))$, asociando cada lema:",
    r"Ensamble los 5 eslabones lógicos desde $m \equiv e(p, v(p,m))$ para deducir la Identidad de Roy en $x_{@g_idx@}$, excluyendo el paso con signo errado:",
]

stems_c02_dag2 = [
    r"Ordene la prueba formal del Lema de Shephard para la demanda compensada $x_{@j_idx@}^h(p, @u_bar@)$ vía Teorema de la Envolvente excluyendo la falacia de Roy:",
    r"Construya en ProofDAG la derivación de $x_{@j_idx@}^h(p, @u_bar@) = \partial e/\partial p_{@j_idx@}$ desde el Lagrangiano del gasto descartando el paso erróneo:",
    r"Encadene los pasos y justificaciones desde el problema mínimo del gasto en nivel $@u_bar@$ hasta obtener $x_{@j_idx@}^h$ para el bien $@j_idx@$:",
    r"Ensamble topológicamente la demostración del Lema de Shephard en $x_{@j_idx@}^h(p, @u_bar@)$ mediante la función valor del gasto mínimo:",
]

stems_c02_os1 = [
    r"Dada $v(p, m) = @c_val@ + \ln(m) - @k@\ln(p)$, aplique la Identidad de Roy para hallar simbólicamente $x^d(p,m)$ en `m` y `p`:",
    r"Calcule algebraicamente $x^d(p,m)$ mediante Identidad de Roy si $v(p,m) = @c_val@ + \ln(m) - @k@\ln(p)$ en función de `m` y `p`:",
    r"Obtenga en términos simbólicos de `m` y `p` la demanda marshalliana $x^d(p,m)$ derivada de $v(p,m) = @c_val@ + \ln(m) - @k@\ln(p)$:",
    r"Determine en el editor simbólico la expresión reducida de $x^d(p,m)$ en `m` y `p` para $v(p,m) = @c_val@ + \ln(m) - @k@\ln(p)$:",
]

stems_c02_os2 = [
    r"Dada la función de gasto $e(p, u) = @F@ + @k@p^2 u$, aplique el Lema de Shephard para obtener simbólicamente la demanda hicksiana $x^h(p,u)$ en `p` y `u`:",
    r"Calcule por Lema de Shephard la demanda compensada $x^h(p,u) = \partial e/\partial p$ si $e(p,u) = @F@ + @k@p^2 u$ en términos de `p` y `u`:",
    r"Derive simbólicamente en `p` y `u` la demanda hicksiana asociada al gasto mínimo $e(p,u) = @F@ + @k@p^2 u$:",
    r"Exprese $x^h(p,u)$ en función de `p` y `u` diferenciando la función de gasto $e(p,u) = @F@ + @k@p^2 u$:",
]

stems_c02_cm1 = [
    r"Asocie cada identidad de dualidad del consumidor para el bien $x_{@idx_b@}$ con su fórmula analítica correcta:",
    r"Empareje los teoremas duales aplicados sobre el bien $x_{@idx_b@}$ con sus expresiones formales correspondientes:",
    r"Relacione correctamente la Identidad de Roy, el Lema de Shephard y la inversión gasto-utilidad para el bien $x_{@idx_b@}$:",
    r"Vincule cada principio de dualidad del consumidor del bien $x_{@idx_b@}$ con su expresión formal descartando distractores cruzados:",
]

stems_c02_cm2 = [
    r"Empareje cada ruptura lógica en la deducción dual del bien $x_{@idx_d@}$ con su consecuencia analítica exacta:",
    r"Asocie los errores frecuentes al derivar desde $m \equiv e(p,v(p,m))$ para el bien $@idx_d@$ con el fallo que producen:",
    r"Relacione cada hipótesis omitida o inversión en la prueba de dualidad de $x_{@idx_d@}$ con su impacto deductivo:",
    r"Vincule las fallas de derivación dual sobre el bien $x_{@idx_d@}$ con sus respectivos diagnósticos formales:",
]

stems_c02_mc7 = [
    r"Con utilidad indirecta $v(p, m) = @c_val@ + \ln(m) - @k@\ln(p)$, evalúe la demanda ordinaria $x^d(p, m)$ cuando $p = @p0@$ y la renta es $m = @m0@$:",
    r"Aplique numéricamente la Identidad de Roy sobre $v(p,m) = @c_val@ + \ln(m) - @k@\ln(p)$ para precio $p = @p0@$ e ingreso $m = @m0@$:",
    r"Si $v(p, m) = @c_val@ + \ln(m) - @k@\ln(p)$, ¿cuántas unidades demanda el consumidor en $(p, m) = (@p0@, @m0@)$?",
    r"Calcule la cantidad marshalliana $x^d(@p0@, @m0@)$ correspondiente a $v(p, m) = @c_val@ + \ln(m) - @k@\ln(p)$:",
]

TEMPLATES = [
    # Hab-01 (6 templates: 0 MC7, 100% active)
    {"id": "T-Hab-01-01", "cid": "Hab-01", "qtype": "open_symbolic", "archetype": "direct", "band": ("easy", "Apply"), "gen": gen_hab01_os1, "ver": ver_hab01_os1, "stem_variants": stems_hab01_os1, "hints": [r"Expresa $\sqrt{x}$ como $x^{1/2}$ antes de derivar.", r"Multiplica por el coeficiente $@a@ = 2 \cdot @k@$ y reduce la potencia a $x^{-1/2}$.", r"El costo fijo $@F@$ desaparece al derivar respecto a $x$."], "sol": r"Derivando $c(x) = @a@\sqrt{x} + @F@$ se obtiene $CMg(x) = @k@/\sqrt{x}$."},
    {"id": "T-Hab-01-02", "cid": "Hab-01", "qtype": "open_symbolic", "archetype": "perturbation", "band": ("medium", "Analyze"), "gen": gen_hab01_os2, "ver": ver_hab01_os2, "stem_variants": stems_hab01_os2, "hints": [r"Divide cada sumando de $c(x) = @a@\sqrt{x} + @F@$ entre la producción $x$.", r"Simplifica $\sqrt{x}/x$ como $1/\sqrt{x}$.", r"Conserva el término fijo medio $@F@/x$ junto al costo variable medio."], "sol": r"El costo medio total resulta $CMe(x) = (@a@\sqrt{x} + @F@)/x = @a@/\sqrt{x} + @F@/x$."},
    {"id": "T-Hab-01-03", "cid": "Hab-01", "qtype": "fill_in_the_blank", "archetype": "direct", "band": ("medium", "Apply"), "gen": gen_hab01_fib1, "ver": ver_hab01_fib1, "stem_variants": stems_hab01_fib1, "hints": [r"Calcula primero el ingreso total multiplicando $p = @p@$ por $x = @x_hi@$.", r"Evalúa el costo variable $@a@\sqrt{@x_hi@} = @a@ \cdot @m_hi@$ y añade $F = @F@$.", r"Comprueba que $\pi(@x_hi@)$ supera el mínimo local $\pi_{\text{stat}} = @pi_stat@$."], "sol": r"En $x = @x_hi@$, $\pi = (@p@)(@x_hi@) - (@a@)(@m_hi@) - @F@ = @pi_hi@ > @pi_stat@$."},
    {"id": "T-Hab-01-04", "cid": "Hab-01", "qtype": "fill_in_the_blank", "archetype": "inverse", "band": ("hard", "Analyze"), "gen": gen_hab01_fib2, "ver": ver_hab01_fib2, "stem_variants": stems_hab01_fib2, "hints": [r"Iguale el precio exógeno $@p@$ a $@k@/\sqrt{x}$.", r"Despeje $\sqrt{x} = @k@/@p@ = @m@$ antes de elevar.", r"Eleve al cuadrado para obtener $x_{\text{stat}} = @m@^2$."], "sol": r"De $@p@ = @k@/\sqrt{x}$ resulta $\sqrt{x} = @m@$ y por tanto $x_{\text{stat}} = @ans@$."},
    {"id": "T-Hab-01-05", "cid": "Hab-01", "qtype": "adversarial_break", "archetype": "perturbation", "band": ("hard", "Evaluate"), "gen": gen_hab01_adv_ff, "ver": ver_hab01_adv_ff, "stem_variants": stems_hab01_adv_ff, "hints": [r"Revisa si la derivada primera en $x_{\text{stat}}$ basta para afirmar un máximo.", r"Deriva una segunda vez la expresión $\pi'(x) = @p_val@ - @b@/\sqrt{x}$.", r"Observa por qué un beneficio estrictamente convexo convierte la CPO en mínimo."], "sol": r"El Paso 3 ignora $\pi''(x) > 0$ bajo $c(x) = @b_dbl@\sqrt{x} + @F@$ y $p = @p_val@$."},
    {"id": "T-Hab-01-06", "cid": "Hab-01", "qtype": "adversarial_break", "archetype": "boundary_or_edge_case", "assumption_id": "A-Hab01-01", "band": ("hard", "Evaluate"), "gen": gen_hab01_adv_ce, "ver": ver_hab01_adv_ce, "stem_variants": stems_hab01_adv_ce, "hints": [r"Elige un valor positivo de $x$ bastante mayor que $x_{\text{stat}} = @x_stat@$.", r"Verifica que con $\pi''(x) > 0$, la función crece al alejarte del mínimo.", r"Prueba un cuadrado perfecto superior a $@x_stat@$ para comprobar $\pi(x) > @pi_stat@$."], "sol": r"Al expandir por encima de $x_{\text{stat}} = @x_stat@$, $\pi(x) = @p@x - @a@\sqrt{x} - @F@$ supera $@pi_stat@$."},
    # Hab-02 (6 templates: 0 MC7, 100% active)
    {"id": "T-Hab-02-01", "cid": "Hab-02", "qtype": "invariant_canvas", "archetype": "direct", "band": ("easy", "Analyze"), "gen": gen_hab02_ic1, "ver": ver_hab02_ic1, "stem_variants": stems_hab02_ic1, "hints": [r"El tramo inicial rige exactamente hasta $x_1 = \bar{x}_1 = @x_bar@$.", r"Resta el gasto inicial $p_1 \cdot \bar{x}_1$ de la renta total $m = @m@$.", r"Coloca el punto sobre el vértice no diferenciable de la frontera presupuestaria."], "sol": r"El quiebre no convexo ocurre en $\bar{x}_1 = @x_bar@$, donde $x_2^* = m - p_1\bar{x}_1 = @m@ - (@p1@)(@x_bar@)$ con descuento $r = @r_pct@\%$."},
    {"id": "T-Hab-02-02", "cid": "Hab-02", "qtype": "invariant_canvas", "archetype": "perturbation", "band": ("hard", "Evaluate"), "gen": gen_hab02_ic2, "ver": ver_hab02_ic2, "stem_variants": stems_hab02_ic2, "hints": [r"Una desigualdad $\le$ incluye el borde con trazo sólido y región inferior.", r"El descuento $@r_pct@\%$ sobre $p_1 = @p1@$ fija el precio marginal $@p1_disc@$.", r"Mueve el deslizador de $p'_1$ exactamente a $p_1(1 - @r_pct@/100)$."], "sol": r"Para $x_1 \ge @x_bar@$ ($m = @m@$), la restricción $\le$ es sólida con sombra inferior y pendiente $@p1_disc@$."},
    {"id": "T-Hab-02-03", "cid": "Hab-02", "qtype": "open_symbolic", "archetype": "direct", "band": ("medium", "Apply"), "gen": gen_hab02_os1, "ver": ver_hab02_os1, "stem_variants": stems_hab02_os1, "hints": [r"Identifica el precio de lista $@p1@$ antes del descuento proporcional.", r"Restar una proporción `r` equivale a multiplicar el precio base por $(1 - r)$.", r"Verifica que si $r = 0$, el precio marginal en $x_1 > @x_bar@$ se reduce a $@p1@$."], "sol": r"Para $x_1 > @x_bar@$, cada unidad cuesta $p_1(1-r) = @p1@(1-r)$."},
    {"id": "T-Hab-02-04", "cid": "Hab-02", "qtype": "open_symbolic", "archetype": "inverse", "band": ("hard", "Analyze"), "gen": gen_hab02_os2, "ver": ver_hab02_os2, "stem_variants": stems_hab02_os2, "hints": [r"Reste primero el gasto completo $@p1@ \cdot @x_bar@$ de la renta $@m@$.", r"Las unidades adicionales $(x_1 - @x_bar@)$ pagan la tarifa reducida $@p1@(1-r)$.", r"Con $p_2 = 1$, $x_2$ iguala directamente el ingreso remanente."], "sol": r"En el Tramo B, $x_2 = @m@ - @p1@ \cdot @x_bar@ - @p1@(1-r)(x_1 - @x_bar@)$."},
    {"id": "T-Hab-02-05", "cid": "Hab-02", "qtype": "unstructured_model", "archetype": "inverse", "band": ("easy", "Analyze"), "gen": gen_hab02_um_select, "ver": ver_hab02_um_select, "stem_variants": stems_hab02_um1, "hints": [r"Distingue la decisión $x_1$ de los datos exógenos $m = @m@$ y $\bar{x}_1 = @x_bar@$.", r"El descuento por volumen quiebra la convexidad del presupuesto.", r"Debes comparar las tangencias de cada tramo frente al punto de quiebre."], "sol": r"Con $m = @m@$ y quiebre en $\bar{x}_1 = @x_bar@$, el óptimo global compara $\max\{u(x^A), u(x^{\text{kink}}), u(x^B)\}$."},
    {"id": "T-Hab-02-06", "cid": "Hab-02", "qtype": "unstructured_model", "archetype": "boundary_or_edge_case", "assumption_id": "A-Hab02-01", "band": ("hard", "Create"), "gen": gen_hab02_um_sym, "ver": ver_hab02_um_sym, "stem_variants": stems_hab02_um2, "hints": [r"Separa el gasto fijo de las primeras $\bar{x}_1 = @x_bar@$ unidades a tarifa $@p1@$.", r"Suma únicamente las unidades excedentes $(x_1 - @x_bar@)$ al precio descontado.", r"Formula el gasto total como suma lineal por tramos en función de `x1` y `r`."], "sol": r"El gasto total en el Tramo B ($x_1 > @x_bar@$) es $@p1@\cdot @x_bar@ + @p1@(1-r)(x_1 - @x_bar@)$."},
    # C-01 (6 templates: 0 MC7, 100% active)
    {"id": "T-C-01-01", "cid": "C-01", "qtype": "adversarial_break", "archetype": "direct", "band": ("medium", "Evaluate"), "gen": gen_c01_adv_ce, "ver": ver_c01_adv_ce, "stem_variants": stems_c01_adv_ce, "hints": [r"Elige primero canastas enteras $A$ y $B$ tales que ambas alcancen exactamente $@k_lvl@$.", r"Procura que al menos una coordenada de $A$ y $B$ difiera en una unidad impar.", r"Calcula la semisuma $0.5A + 0.5B$ para observar cómo $\lfloor \cdot \rfloor$ trunca abajo."], "sol": r"Un testigo como $A=(1, @k_lvl@-1)$ y $B=(2, @k_lvl@-2)$ da punto medio con suma $< @k_lvl@$."},
    {"id": "T-C-01-02", "cid": "C-01", "qtype": "adversarial_break", "archetype": "perturbation", "band": ("hard", "Evaluate"), "gen": gen_c01_adv_ff, "ver": ver_c01_adv_ff, "stem_variants": stems_c01_adv_ff, "hints": [r"Verifica si $u(x_1, x_2) = \lfloor x_1 \rfloor + \lfloor x_2 \rfloor$ es diferenciable.", r"Las funciones escalonadas saltan en cada valor entero.", r"Un criterio basado en derivadas segundas es inválido sin continuidad ni diferenciabilidad."], "sol": r"El Paso 2 falla porque la función parte entera no es diferenciable en contorno $@k_lvl@$."},
    {"id": "T-C-01-03", "cid": "C-01", "qtype": "invariant_canvas", "archetype": "inverse", "band": ("hard", "Analyze"), "gen": gen_c01_tree, "ver": ver_c01_tree, "stem_variants": stems_c01_tree, "hints": [r"Compara los perfiles de pago terminales hasta identificar $(@w1@, @w1@)$.", r"Activa únicamente las dos aristas que llevan al nodo terminal `@win_label@`.", r"Cuando J2 desconoce qué eligió J1, sus dos nodos pertenecen al mismo conjunto informacional."], "sol": r"Activa las aristas hacia `@win_label@` ($(@w1@, @w1@)$ frente a $(@w2@, 0)$) y une J2a con J2b."},
    {"id": "T-C-01-04", "cid": "C-01", "qtype": "invariant_canvas", "archetype": "boundary_or_edge_case", "assumption_id": "A-C01-01", "band": ("hard", "Evaluate"), "gen": gen_c01_cart, "ver": ver_c01_cart, "stem_variants": stems_c01_cart, "hints": [r"Promedia las abscisas de $A=(@a1@,@a2@)$ y $B=(@b1@,@b2@)$ para obtener $x_1$.", r"Promedia las ordenadas de ambas canastas para obtener $x_2$.", r"Verifica que en ese punto medio $u(M) < @k_lvl@$."], "sol": r"El punto medio de $A=(@a1@,@a2@)$ y $B=(@b1@,@b2@)$ cae por debajo del nivel $@k_lvl@$ tras aplicar piso."},
    {"id": "T-C-01-05", "cid": "C-01", "qtype": "fill_in_the_blank", "archetype": "direct", "band": ("easy", "Understand"), "gen": gen_c01_fib1, "ver": ver_c01_fib1, "stem_variants": stems_c01_fib1, "hints": [r"Trunca separadamente la parte decimal de $x_1 = @x1@$ al entero menor o igual.", r"Trunca separadamente $x_2 = @x2@$ hacia abajo, nunca redondees hacia arriba.", r"Suma únicamente ambos resultados enteros tras aplicar el operador piso."], "sol": r"$\lfloor @x1@ \rfloor + \lfloor @x2@ \rfloor = @ans@$ (no $@cont_sum@$ ni $@ceil_sum@$)."},
    {"id": "T-C-01-06", "cid": "C-01", "qtype": "fill_in_the_blank", "archetype": "inverse", "band": ("medium", "Analyze"), "gen": gen_c01_fib2, "ver": ver_c01_fib2, "stem_variants": stems_c01_fib2, "hints": [r"Aplica primero el operador piso a cada coordenada de $(@x1@, @x2@)$.", r"Suma ambas partes enteras obteniendo $@u_m@$.", r"Reste dicho valor al umbral requerido $@k_lvl@$."], "sol": r"El déficit resulta $@k_lvl@ - (\lfloor @x1@ \rfloor + \lfloor @x2@ \rfloor) = @k_lvl@ - @u_m@ = @ans@$."},
    # C-02 (7 templates: 1 MC7 + 6 active = 85.7% >= 80% active)
    {"id": "T-C-02-01", "cid": "C-02", "qtype": "proof_dag", "archetype": "perturbation", "band": ("hard", "Evaluate"), "gen": gen_c02_dag_roy, "ver": ver_c02_dag_roy, "stem_variants": stems_c02_dag1, "hints": [r"Inicia diferenciando $m \equiv e(p, v(p,m))$ respecto a $p_{@g_idx@}$ por regla de la cadena.", r"Necesitas derivar además la identidad respecto a $m$ para despejar $\partial e/\partial u$.", r"Despeja la demanda ordinaria cuidando el signo negativo del término en precio."], "sol": r"La deducción para el bien $@g_idx@$ aplica regla de la cadena, Shephard y derivada respecto a $m$."},
    {"id": "T-C-02-02", "cid": "C-02", "qtype": "proof_dag", "archetype": "boundary_or_edge_case", "assumption_id": "A-C02-01", "band": ("hard", "Evaluate"), "gen": gen_c02_dag_shephard, "ver": ver_c02_dag_shephard, "stem_variants": stems_c02_dag2, "hints": [r"Formula primero el Lagrangiano del problema de minimización del gasto en $@u_bar@$.", r"Evalúa la función valor óptima antes de derivar respecto a $p_{@j_idx@}$.", r"Aplica el Teorema de la Envolvente anulando derivadas indirectas para concluir con signo positivo."], "sol": r"Por Envolvente sobre $e(p,@u_bar@)$, la derivada respecto a $p_{@j_idx@}$ iguala $x_{@j_idx@}^h(p,@u_bar@)$."},
    {"id": "T-C-02-03", "cid": "C-02", "qtype": "open_symbolic", "archetype": "direct", "band": ("medium", "Analyze"), "gen": gen_c02_os1, "ver": ver_c02_os1, "stem_variants": stems_c02_os1, "hints": [r"Deriva $v = @c_val@ + \ln(m) - @k@\ln(p)$ respecto a $p$ obteniendo $-@k@/p$.", r"Deriva la misma función respecto a $m$ obteniendo el inverso multiplicativo $1/m$.", r"Divide $-(\partial v/\partial p)$ entre $(\partial v/\partial m)$ simplificando signos."], "sol": r"Con $v = @c_val@ + \ln(m) - @k@\ln(p)$, $-\frac{-@k@/p}{1/m} = @k@m/p$."},
    {"id": "T-C-02-04", "cid": "C-02", "qtype": "open_symbolic", "archetype": "inverse", "band": ("hard", "Analyze"), "gen": gen_c02_os2, "ver": ver_c02_os2, "stem_variants": stems_c02_os2, "hints": [r"Identifica la relación del Lema de Shephard: $x^h(p,u) = \partial e(p,u)/\partial p$.", r"La constante fija $@F@$ se anula al diferenciar respecto al precio $p$.", r"Deriva $@k@p^2 u$ respecto a `p` manteniendo fija la utilidad `u`."], "sol": r"Derivando $e(p,u)=@F@+@k@p^2 u$ respecto a $p$ resulta $x^h(p,u)=2 \cdot @k@pu$."},
    {"id": "T-C-02-05", "cid": "C-02", "qtype": "concept_matching", "archetype": "direct", "band": ("easy", "Understand"), "gen": gen_c02_cm1, "ver": ver_c02_cm1, "stem_variants": stems_c02_cm1, "hints": [r"Identifica cuál teorema diferencia la utilidad indirecta $v(p,m)$ respecto a $p_{@idx_b@}$.", r"Recuerda el signo negativo que acompaña al cociente de derivadas en Roy.", r"Asocia la derivada de la función de gasto $e(p,u)$ con la demanda compensada."], "sol": r"Roy arroja demanda ordinaria con signo negativo y Shephard deriva $e(p,u)$ para el bien $@idx_b@$."},
    {"id": "T-C-02-06", "cid": "C-02", "qtype": "concept_matching", "archetype": "inverse", "band": ("medium", "Analyze"), "gen": gen_c02_cm2, "ver": ver_c02_cm2, "stem_variants": stems_c02_cm2, "hints": [r"Revisa cómo despejar $\partial e/\partial u$ diferenciando la identidad en $m$.", r"Recuerda que el vínculo entre $\partial e/\partial p_{@idx_d@}$ y $x^h$ proviene de Shephard.", r"La identidad del gasto iguala la renta $m$, nunca la utilidad $u$."], "sol": r"Cada ruptura en la derivación dual de $x_{@idx_d@}$ destruye el despeje correcto de la Identidad de Roy."},
    {"id": "T-C-02-07", "cid": "C-02", "qtype": "multiple_choice", "archetype": "perturbation", "band": ("medium", "Apply"), "gen": gen_c02_mc7, "ver": ver_c02_mc7, "stem_variants": stems_c02_mc7, "hints": [r"Calcula $\partial v/\partial p = -@k@/p$ y $\partial v/\partial m = 1/m$.", r"Aplica la fórmula $x^d = -(\partial v/\partial p)/(\partial v/\partial m) = @k@m/p$.", r"Sustituye $p = @p0@$ y $m = @m0@$ en $@k@m/p$."], "sol": r"Por Identidad de Roy, $x^d(@p0@, @m0@) = @k@ \cdot @m0@ / @p0@ = @ans@$ unidades.", "fmt": r"$@X@$"},
]
'''


def main(out_json: Optional[Path] = None) -> int:
    out_dir = Path(__file__).resolve().parent
    target_json = Path(out_json) if out_json is not None else (out_dir / "m20_canonical_course.json")

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

        # 3. Stage 3: compile_shard(strict=True, templates_per_modality=2)
        cs_ok, cs_errs = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_01",
            strict=True,
            min_archetypes=4,
            templates_per_modality=2,
            seeds=20,
        )
        assert cs_ok and not cs_errs, f"compile_shard failed:\n" + "\n".join(cs_errs)
        print("[2/6] compile_shard(strict=True, min_archetypes=4, templates_per_modality=2) OK")

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
                "recommended_modalities": c.get("recommended_modalities", []),
                "bloom_level": c.get("bloom", "Analyze"),
                "mastery_target": 0.9,
            })

        course_obj: Dict[str, Any] = {
            "schema_version": "1.0.0",
            "version": "1.0.0",
            "contract_version": 2,
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
        assert rm_summary.get("skill_mc7_violations_count", 0) == 0, f"Skill MC7 violations: {rm_summary}"
        assert rm_summary.get("low_active_quota_competencies_count", 0) == 0, f"Low active quota: {rm_summary}"
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

        target_json.parent.mkdir(parents=True, exist_ok=True)
        target_json.write_text(json.dumps(course_obj, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[6/6] Wrote canonical fixture to {target_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
