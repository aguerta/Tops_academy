# Reporte de Re-Auditoría Exhaustiva (Agéntica + Determinista) — `solow_test_k4`

> [!WARNING]
> **CURSO RETIRADO DE LA PLATAFORMA**: Este curso fue eliminado de la plataforma interactiva el **2026-11-28 05:27:43**. Este informe de auditoría se conserva exclusivamente como registro histórico y pedagógico ('legacy').

**Estado en Plataforma:** ELIMINADO  
**Fecha de Eliminación:** 2026-11-28 05:27:43  
**Curso:** Solow Test K4 (`courses/solow_test_k4.json`)  
**Objetivo detectado:** Dominio y aplicación analítica integral del modelo neoclásico de crecimiento de Solow (forma per cápita, estabilidad de fase, linealización de Bernoulli, proporciones fijas Harrod-Domar, precios factoriales, cambio tecnológico neutral y extensiones endógenas).  
**Competencias:** 19 (1 Hechos `[H]`, 11 Conceptos `[C]`, 7 Habilidades `[Hab]`)  
**Reactivos totales:** 768 (36 por Hecho/Concepto; 48 por Habilidad)  
**Calificación Final QM-OSCQR:** **16.50 / 20.00** — **ACEPTABLE (14.0 - 16.9 pts)** *(recalibrada desde 20.00/20.00 tras auditoría semántica directa sobre el JSON del curso)*  
**Mastery Path Readiness Index (MPRI):** **87.00 / 100.00** — **GOLD MASTERY PATH (85-100): Aprobado con Reservas (requiere corrección de defectos puntuales)**

---

## 1. Resumen Ejecutivo de la Re-Auditoría

Aunque `solow_test_k4` obtuvo `risk_score = 0.00` en los 7 linters deterministas *Path-to-Mastery v2.0* y un DAG/ZPD estructuralmente limpios, la **inspección agéntica directa sobre `courses/solow_test_k4.json`** reveló **5 familias de defectos semánticos, matemáticos, psicométricos y ergonómicos reales** que el linter estático no detecta:

1. **Error matemático e inversión conceptual grave en `C-04` (`Q-C04-256`, `Q-C04-257`, `Q-C04-258`):** Los 3 ítems `Create`/`hard` usan parámetros concretos donde $s \cdot a > n$ (imposibilitando cualquier equilibrio positivo), pero sus opciones requeridas (`A1`) y `detailed_solution` afirman que debe cumplirse $s \cdot a < n$ para que exista un único equilibrio positivo estable, además de referirse al rayo $(3/100)r$ como `"rayo $3 r$"` e invertir el nombre de $r=K/L$ a `"Razón trabajo-capital $r$"`.
2. **Barrera ergonómica en 83 reactivos (`allow_calculator: false` con 4 decimales):** Los 768 reactivos tienen `"allow_calculator": false`, pero **83 ítems `fill_in_the_blank`** exigen calcular exponenciales ($120 e^{0.45}$) o potencias/raíces irracionales ($(10/3)^{5/3}$, $1 - 0.5\sqrt{2.5}$) redondeadas a 4 decimales con tolerancias de `0.001`–`0.005`.
3. **Fugas de respuesta (`answer leaks`) en `stem` y `hints`:** Varios ítems `multiple_select`, `adversarial_break` y `unstructured_model` (`Q-H01-013`, `Q-H01-016`, `Q-C12-759`, `Q-C12-760`, `Q-Hab04-421`, `Q-Hab01-177`) regalan explícitamente los cálculos o el umbral exacto dentro del enunciado o pistas.
4. **Goodharting de Taxonomía de Bloom:** El linter reporta `bloom_weighted_index = 3.94` vs `adaptive_bloom_floor = 3.84` (Tier `ÉLITE`), pero existen reactivos de sustitución mecánica directa o verificación literal etiquetados como `Analyze` (`Q-H01-007..008`), `Evaluate` (`Q-H01-016..017`, `Q-C12-759`) o `Create` (`Q-C04-256..258`, `Q-Hab01-177`).
5. **Inconsistencias menores de terminología y formato:** `Q-C02-074` denomina `"depreciación efectiva"` a $\lambda=0.05$ (definido como crecimiento laboral en `C-01`/`C-03`), y las opciones `is_required: true` de `phase2_assumptions` en `unstructured_model` cierran su `error_rationale` con doble punto (`..`).

---

## 2. Evaluación por Dimensiones (Rúbrica QM-OSCQR v2.0 — 20.00 pts)

| Dimensión | Puntaje | Máximo | Ajuste | Evidencia Determinista y Hallazgos Semánticos Directos |
| :--- | :---: | :---: | :---: | :--- |
| **D1: Arquitectura Curricular, Topología DAG y Calibración ZPD** | 4.00 | 4.00 | 0.00 | 19 competencias (1 `[H]`, 11 `[C]`, 7 `[Hab]`), 768 ítems (36–48/comp). DAG acíclico y conexo (`has_cycle=false`, `connected_components=1`, `max_dag_depth=5`, `inverted_edges=0`). Calibración tri-banda activa en 19/19 competencias (`easy`: 256, `medium`: 256, `hard`: 256). |
| **D2: Calidad Psicométrica, Modalidad de Evocación y Anti-Gaming** | 3.90 | 5.00 | -1.10 | Base sólida (`MC7=0.00%`, `FIB=11.98%`, `MS=18.75%`, BloomSup=`69.27%`, 504 distractores con 100.00% cobertura). **Deducciones:** `-0.60` por fugas de respuesta en `stem` (`Q-H01-013`, `Q-H01-016`, `Q-C12-759`, `Q-C12-760`, `Q-Hab04-421`); `-0.50` por contradicción paramétrica en `Q-C04-256..258`. |
| **D3: Andamiaje Socrático Progresivo y Remediación Diagnóstica** | 4.40 | 5.00 | -0.60 | 100.00% de ítems con 3–5 pistas sin boilerplate Mad-Libs ni envenenamiento. **Deducción:** `-0.60` por pistas que filtran directamente la respuesta (`Q-Hab01-177`, `Q-Hab04-421`) y `error_rationale` con doble punto (`..`) en `phase2_assumptions` de `unstructured_model`. |
| **D4: Alineación Instruccional, Taxonomía de Bloom y Pureza de Dominio** | 2.90 | 4.00 | -1.10 | 100.00% de `[Hab]` en `Apply+`. **`bloom_weighted_index` = 3.94** vs **`adaptive_bloom_floor` = 3.84** (`gap = 0.00`, `superior_pct = 67.97%`, Tier `ÉLITE`). **Deducciones:** `-0.70` por errores matemáticos/conceptuales reales en `Q-C04-256..258` (`(38/100)6 < (3/100)` falso, `"rayo $3r$"`, `"Razón trabajo-capital"`) y `Q-C02-074` (`depreciación efectiva`); `-0.40` por Goodharting de Bloom en `H-01`, `C-04`, `Hab-01` y `C-12`. |
| **D5: Accesibilidad, Ergonomía Cognitiva en UI y Sintaxis KaTeX** | 1.30 | 2.00 | -0.70 | Sintaxis KaTeX 100.00% válida (0 llaves rotas, 0 `$$$`, 0 prosa en `\text{...}`). **Deducción:** `-0.70` por **83 ítems `fill_in_the_blank`** que exigen redondeo a 4 decimales de exponenciales/raíces irracionales con `"allow_calculator": false`. |

---

## 3. Mastery Path Readiness Index (`MPRI`: 87.00 / 100.00)

| Pilar Cognitivo y de Plataforma | Puntaje | Máximo | Métricas y Ajustes de Rigurosidad |
| :--- | :---: | :---: | :--- |
| **1. Progresión Adaptativa ZPD y Bloom (`zpd_adaptive_progression`)** | 17.50 | 20.00 | 19/19 competencias tri-banda (`256/256/256`); **`bloom_weighted_index` = 3.94** vs **`adaptive_bloom_floor` = 3.84** (`gap = 0.00`). Ajuste `-2.50` por Goodharting de Bloom (`Analyze`/`Evaluate`/`Create` en tareas mecánicas). |
| **2. Modalidad de Evocación y Anti-Gaming (`retrieval_modality_and_anti_gaming`)** | 16.00 | 20.00 | 100.00% evocación activa/discriminación (`MC7=0.00%`). Ajuste `-4.00` por *answer leaks* en `stem` (`H-01`, `C-12`, `Hab-04`) y contradicción paramétrica en `C-04`. |
| **3. Salvavidas de Andamiaje Socrático (`socratic_scaffolding_lifeline`)** | 22.50 | 25.00 | 0.00% Mad-Libs y 0.00% envenenamiento. Ajuste `-2.50` por pistas con *answer-leak* en `Q-Hab01-177` y `Q-Hab04-421`. |
| **4. Alineación Diagnóstica de Remediación (`diagnostic_remediation_alignment`)** | 13.50 | 15.00 | 504/504 distractores cubiertos. Ajuste `-1.50` por `A1` matemáticamente falso en `Q-C04-256..258` y doble punto en `phase2`. |
| **5. Topología DAG e Interleaving (`dag_and_interleaving_topology`)** | 10.00 | 10.00 | Grafo acíclico conexo (`has_cycle=false`, 1 componente conexo, 0 aristas invertidas). |
| **6. Ergonomía Cognitiva y Framing (`cognitive_ergonomics_and_framing`)** | 7.50 | 10.00 | KaTeX limpio, pero ajuste `-2.50` por 83 ítems a 4 decimales con `allow_calculator: false` y etiqueta invertida `"Razón trabajo-capital"`. |

---

## 4. Penalizaciones Duras Aplicadas

Ninguna penalización dura automática activada (`hard_penalties = []`, deducción total = **0.00 pts**).

---

## 5. Evidencia Verbatim de Hallazgos en `courses/solow_test_k4.json`

### 5.1 Errores Matemáticos y Conceptuales (`C-04` y `C-02`)
1. **`Q-C04-256` (`Create`, `hard`, `unstructured_model`):**
   - *Enunciado:* `"Formule el modelo dinámico $\dot{r}=(38/100)F(r,1)-(3/100)r$ para la función lineal $F(r,1)=6 r+2$:"`
   - *Error conceptual (`phase1_variables`, `V1`):* `"label": "Razón trabajo-capital $r$"` (invertido; $r=K/L$ es la razón **capital-trabajo**, presente 3 veces en `Q-C04-256`, `Q-C04-257` y `Q-C04-258`).
   - *Error matemático (`phase2_assumptions`, `A1`, `is_required: true`):* `"Debe cumplirse $(38/100)6 < (3/100)$ para que el rayo $3 r$ cruce desde abajo a la recta de ahorro."` — Con los parámetros del enunciado, $(38/100)\cdot 6 = 2.28 > 0.03$, por lo que **no existe equilibrio positivo** $r^*>0$ (contradicción directa). Además, llama `"rayo $3 r$"` al rayo $(3/100)r$.
   - *Mismo fallo exacto:* **`Q-C04-257`** ($(30/100)\cdot 6 = 1.80 \not< 0.07$, `"rayo $7 r$"`) y **`Q-C04-258`** ($(15/100)\cdot 6 = 0.90 \not< 0.04$, `"rayo $4 r$"`).
2. **`Q-C02-074` (`Understand`, `easy`, `open_symbolic`):**
   - *Cita:* `"depreciación efectiva $\lambda=0.05$"` — En `C-01` y `C-03`, $\lambda$ es la tasa de crecimiento laboral $\dot{L}/L$; mezclar la nomenclatura con depreciación introduce ambigüedad conceptual.

### 5.2 Imposibilidad Operativa por `allow_calculator: false` (83 ítems `fill_in_the_blank`)
- **`Q-H01-007` (`allow_calculator: false`, `tolerance: 0.001`):** `"Determine el tamaño de la fuerza de trabajo $L(t)$ tras $t=9$ períodos partiendo de $L_0=120$ a una tasa exponencial $5\%$ (redondee a 4 decimales):"` $\to$ `188.1975` ($120 e^{0.45}$).
- **`Q-H01-008` (`allow_calculator: false`, `tolerance: 0.001`):** $130 e^{0.50} \approx 214.3338$.
- **`Q-Hab01-161` (`allow_calculator: false`, `tolerance: 0.005`):** $k^* = (0.08/0.04)^{1/(1-0.6)} = 2^{2.5} \approx 5.6569$.
- **`Q-Hab01-162` (`allow_calculator: false`, `tolerance: 0.005`):** $k^* = (0.1/0.03)^{1/(1-0.4)} = (10/3)^{5/3} \approx 7.4381$.
- **`Q-Hab05-497` (`allow_calculator: false`, `tolerance: 0.005`):** $1 - 0.4\sqrt{0.12/0.06} \approx 0.4343$.
- **`Q-Hab05-498` (`allow_calculator: false`, `tolerance: 0.005`):** $1 - 0.5\sqrt{0.2/0.08} \approx 0.2094$.

### 5.3 Fugas de Respuesta (`Answer Leaks`) y Goodharting de Bloom
- **`Q-H01-013` (`multiple_select`, `Apply`):** El `stem` dice `($\dot{K}=75.0$)`, regalando el valor de la opción correcta `D` (`...satisface $\dot{K}=0.25 \cdot 300=75.0$`).
- **`Q-H01-016` (`multiple_select`, `Evaluate`):** El `stem` dice `$\lambda=4$ ($560$)`, regalando la opción correcta `F` (`...eleva el producto total de $140$ a $560$ unidades`). Además, evaluar $F(4K,4L)=4Y_0$ y $\dot{K}=sY$ no corresponde al nivel `Evaluate`.
- **`Q-C12-759` (`multiple_select`, `Evaluate`):** El `stem` entrega ya calculados $\dot{L}/L=33\%$, $n=43\%$ y `diferencial $10\%$`, regalando las opciones `A` y `E`.
- **`Q-C12-760` (`multiple_select`, `Understand`):** El `stem` entrega `su tasa de ahorro crítica $s^*=14\%$` y `n=42%`, regalando la opción `D`.
- **`Q-Hab04-421` (`adversarial_break`, `Analyze`):** El `stem` dice `(umbral $sa^2=1.7778$)` y la pista 2 indica literalmente `"Elija un valor positivo $n>0$ estrictamente menor que $1.7778$"`.
- **`Q-Hab01-177` (`unstructured_model`, `Create`):** La pista 1 revela `V1` (`$z=k^{1-0.4}$`) y la pista 3 revela la estructura de `phase3`, mientras `phase3` es solo aplicar regla de la cadena.
- **`Q-H01-007`, `Q-H01-008` (`Analyze`):** Sustitución directa de dos números en $L_0 e^{nt}$ (nivel real `Apply`).

---

## 6. Acciones Prioritarias de Remediación

1. **[CRÍTICO] Corregir `Q-C04-256`, `Q-C04-257` y `Q-C04-258`:** Cambiar `"Razón trabajo-capital $r$"` por `"Razón capital-trabajo $r$"`, corregir el rayo `"$3r$"` / `"$7r$"` / `"$4r$"` a `$(3/100)r$` / `$(7/100)r$` / `$(4/100)r$`, y ajustar los parámetros $(s, a, n)$ para que $s \cdot a < n$ realmente se cumpla cuando se pide equilibrio positivo estable.
2. **[ALTO] Habilitar `"allow_calculator": true` en los 83 ítems de cálculo irracional/exponencial a 4 decimales** (o usar parámetros con raíces/potencias exactas).
3. **[ALTO] Eliminar *answer leaks* en `stem` y `hints`** de `Q-H01-013`, `Q-H01-016`, `Q-C12-759`, `Q-C12-760`, `Q-Hab04-421` y `Q-Hab01-177`.
4. **[MEDIO] Recalibrar etiquetas de Bloom (`Goodharting`)** en `H-01`, `C-04`, `Hab-01` y `C-12`, unificar el término de $\lambda$ en `Q-C02-074`, y limpiar el doble punto (`..`) en `error_rationale` de `phase2_assumptions`.

---

<details>
<summary>Metadatos Estructurados (JSON)</summary>

```json
{
  "course_metadata": {
    "course_id": "solow_test_k4",
    "unit_title": "Solow Test K4",
    "detected_objective": "Dominio y aplicación analítica integral de Solow Test K4",
    "total_competencies": 19,
    "total_questions": 768,
    "bloom_index": {
      "weighted_index": 3.94,
      "adaptive_floor": 3.84,
      "gap": 0.0,
      "apply_plus_pct": 92.58,
      "superior_pct": 67.97,
      "tier": "ÉLITE",
      "coherence_violations_count": 0
    }
  },
  "dimension_scores": {
    "architecture_granularity": {
      "score": 4.0,
      "max": 4.0,
      "feedback": "Estructura curricular con 19 competencias (1 Hechos, 11 Conceptos, 7 Habilidades). DAG acíclico y conexo (ciclos=False, comp. conexos=1, pares solapados=0). ZPD: 19/19 competencias con calibración tri-banda ('easy', 'medium', 'hard')."
    },
    "assessment_quality": {
      "score": 3.9,
      "max": 5.0,
      "feedback": "Modalidad: MC7=0.00%, FIB=11.98%, MS=18.75%, BloomSup=69.27% (100.00% evocación activa/discriminación). Deducción de -1.10 pts por fugas de respuesta en stem (Q-H01-013, Q-H01-016, Q-C12-759, Q-C12-760, Q-Hab04-421) y contradicción paramétrica en Q-C04-256..258."
    },
    "scaffolding_hints": {
      "score": 4.4,
      "max": 5.0,
      "feedback": "100.00% con 3-5 pistas sin boilerplate Mad-Libs ni envenenamiento. Deducción de -0.60 pts por pistas con answer-leak directo (Q-Hab01-177, Q-Hab04-421) y doble punto ('..') en error_rationale de phase2_assumptions."
    },
    "instructional_alignment": {
      "score": 2.9,
      "max": 4.0,
      "feedback": "100.00% de habilidades en Apply+; bloom_weighted_index=3.94 vs adaptive_bloom_floor=3.84 (67.97% Analyze+Evaluate, Tier ÉLITE). Deducción de -1.10 pts por errores matemáticos/conceptuales en Q-C04-256..258 y Q-C02-074 (-0.70) y Goodharting de Bloom en H-01, C-04, Hab-01 y C-12 (-0.40)."
    },
    "technical_ergonomics": {
      "score": 1.3,
      "max": 2.0,
      "feedback": "KaTeX 100.00% limpio. Deducción de -0.70 pts porque 83 reactivos fill_in_the_blank exigen redondeo a 4 decimales de exponenciales/raíces irracionales con allow_calculator=false."
    }
  },
  "penalties_applied": [],
  "raw_subtotal": 16.5,
  "final_score": 16.5,
  "quality_tier": "ACEPTABLE (14.0 - 16.9 pts)",
  "mastery_path_readiness": {
    "mpri_score": 87.0,
    "mpri_max": 100.0,
    "mpri_tier": "GOLD MASTERY PATH (85-100): Aprobado con Reservas",
    "pillars": {
      "zpd_adaptive_progression": {
        "score": 17.5,
        "max": 20.0
      },
      "retrieval_modality_and_anti_gaming": {
        "score": 16.0,
        "max": 20.0
      },
      "socratic_scaffolding_lifeline": {
        "score": 22.5,
        "max": 25.0
      },
      "diagnostic_remediation_alignment": {
        "score": 13.5,
        "max": 15.0
      },
      "dag_and_interleaving_topology": {
        "score": 10.0,
        "max": 10.0
      },
      "cognitive_ergonomics_and_framing": {
        "score": 7.5,
        "max": 10.0
      }
    },
    "student_journey_verdict": "Base estructural y ZPD sólidas, pero requiere corregir errores matemáticos en C-04, habilitar calculadora en 83 ítems de 4 decimales y eliminar answer leaks antes de certificación Platinum."
  },
  "discovered_lint_rules": [
    {
      "rule_id": "QA-SEM-CALC-01",
      "severity": "warning",
      "regex_pattern": "redondee a 4 decimales",
      "description": "Detecta reactivos numéricos que exigen precisión a 4 decimales (exponenciales/raíces irracionales) manteniendo allow_calculator=false.",
      "evidence_items": ["Q-H01-007", "Q-H01-008", "Q-Hab01-161", "Q-Hab01-162", "Q-Hab05-497", "Q-Hab05-498"]
    },
    {
      "rule_id": "QA-SEM-LEAK-01",
      "severity": "warning",
      "regex_pattern": "\\(\\\\dot\\{K\\}=|\\(umbral sa\\^2=|tasa de ahorro cr[ií]tica s\\*=",
      "description": "Detecta fugas de resultados intermedios o umbrales exactos dentro del enunciado (stem) en ítems multiple_select y adversarial_break.",
      "evidence_items": ["Q-H01-013", "Q-H01-016", "Q-C12-759", "Q-C12-760", "Q-Hab04-421"]
    }
  ],
  "remediation_actions": [
    "Corregir en Q-C04-256, Q-C04-257 y Q-C04-258 la etiqueta 'Razón trabajo-capital r', el rayo '3r'/'7r'/'4r' y los parámetros s*a < n.",
    "Habilitar allow_calculator=true en los 83 reactivos fill_in_the_blank que exigen 4 decimales sobre exponenciales o raíces irracionales.",
    "Eliminar answer leaks en stem y hints (Q-H01-013, Q-H01-016, Q-C12-759, Q-C12-760, Q-Hab04-421, Q-Hab01-177).",
    "Recalibrar etiquetas de Bloom (Goodharting) y unificar nomenclatura de lambda en Q-C02-074."
  ]
}
```

</details>
