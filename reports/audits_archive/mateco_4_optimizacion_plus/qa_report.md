# Reporte de Auditoría QA: `mateco_4_optimizacion_plus`

**Título del curso:** Mateco 4 Optimizacion Plus  
**Objetivo detectado:** Dominio y aplicación analítica integral de Mateco 4 Optimizacion Plus (Cálculo de Variaciones y Control Óptimo)  
**Calificación Final QM-OSCQR:** **19.06 / 20.0** — **EXCELENTE (19.0 - 20.0 pts) — PLATINUM MASTERY**  
**Índice de Preparación para el Dominio (MPRI):** **95.91 / 100.0** — **GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo**  
**Validación Stage-5 Blind Judges:** `120 / 120` reactivos arbitrados (`agreement_rate = 1.0`, `0` desacuerdos sin reparar)  
**Nivel de Riesgo Estático (`risk_score`):** `5.27`

---

## 1. Resumen Ejecutivo

El curso **`mateco_4_optimizacion_plus`** (30 competencias, 730 reactivos) alcanza la certificación **PLATINUM MASTERY (19.06 / 20.0)** y **GOLD MASTERY PATH (95.91 / 100.0 MPRI)**. La estructura curricular cubre Cálculo de Variaciones (funcionales, Euler, Legendre, Beltrami, transversalidad) y Control Óptimo (Principio del Máximo de Pontryagin, Hamiltoniano en valor presente y corriente, modelo Ramsey-Cass-Koopmans, contaminación y permisos de emisión) con 100% de calibración tri-banda ZPD (`easy`: 189, `medium`: 218, `hard`: 323), 0 errores de sintaxis KaTeX y 100% de cobertura de `error_rationale` sobre 2,232 distractores.

No obstante, el **Loop de Verificación Semántica** sobre `risk_cluster_samples` y `stratified_samples` identificó hallazgos relevantes que deben atenderse para llevar el banco a perfección operativa:
1. **Colisiones por concatenación de dígitos en `hints`, `detailed_solution` y `error_rationale` (no detectadas por el linter de `stem`/`options`):** Multiplicaciones implícitas sin `\cdot` ni paréntesis fusionan coeficientes y constantes en cifras falsas (ej. `-22u` y `/22` en lugar de `-4u` y `/4` en `Q-C01-011`; `-24u` en `Q-Hab14-621`; `-21u` en `Q-Hab14-622`; `(53+4)t+(52+33)` en `Q-C07-251`; `22\dot{x}` en `Q-C14-471`/`Q-C14-472`; `4+62t` y `623` en `Q-C17-681`; `2+81t` y `814` en `Q-C17-682`), aunque la clave numérica final en todos los casos verificados es matemáticamente exacta.
2. **Reciclaje de `misconception_warning` y desfase paramétrico:** 243 reactivos reciclan la fórmula muda `$\frac{\partial\mathcal{H}}{\partial x}=\dot{\lambda}$` sin prosa diagnóstica (`Q-C01-011`), y en competencias específicas la advertencia conserva valores fijos que no coinciden con la instancia (`t=2` en `Q-Hab11-492` cuando pide `x(5)`; `$50\%$` / `0.5x` en `Q-Hab14-621` y `Q-Hab14-622` cuando usan `0.2x` y `0.8x`; `x(3)=0` en `Q-Hab16-651` y `Q-Hab16-652` cuando sus horizontes son $T=2$ y $T=4$).
3. **Incumplimiento del contrato M20 en competencias Skill y sesgo de longitud en MS:** Las 13 competencias `Skill` (`Hab-01`..`Hab-19`) aún incluyen reactivos `MC7` (`[M20-MC7-CAP]`), las 30 competencias quedan por debajo del 80% de modalidades activas (`[M20-ACTIVE-QUOTA]`, entre 46.7% y 73.3%), y 50/176 reactivos `multiple_select` (28.41%) presentan sesgo de longitud en opciones correctas.
4. **Solapamiento curricular en el DAG y brecha leve de Bloom:** 5 pares de competencias se solapan temáticamente (`C-01<->C-16`, `C-05<->C-14`, `C-05<->C-15`, `C-14<->C-15`, `Hab-11<->Hab-12`) y el Índice Bloom Ponderado (`3.753`) queda `-0.117` por debajo del piso adaptativo (`3.87`).

---

## 2. Desglose de Evaluación por Dimensiones (Rúbrica QM-OSCQR /20.0)

| Dimensión | Puntaje | Máximo | Estado |
|---|---:|---:|---|
| **D1. Arquitectura Curricular, Topología DAG y Calibración ZPD** | **3.60** | 4.00 | Sólido con solapamientos |
| **D2. Calidad Psicométrica, Modalidad de Evocación y Anti-Gaming** | **5.00** | 5.00 | Excelente (con alertas M20/MS) |
| **D3. Andamiaje Socrático Progresivo y Remediación Diagnóstica** | **4.60** | 5.00 | Sólido con colisiones en soluciones |
| **D4. Alineación Instruccional, Taxonomía de Bloom y Pureza de Dominio** | **3.86** | 4.00 | Sólido (brecha Bloom -0.12) |
| **D5. Accesibilidad, Ergonomía Cognitiva en UI y Sintaxis KaTeX** | **2.00** | 2.00 | Excelente |
| **Penalizaciones Duras Automáticas** | **0.00** | — | Sin deducciones duras |
| **CALIFICACIÓN FINAL** | **19.06** | **20.00** | **EXCELENTE — PLATINUM MASTERY** |

---

## 3. Análisis Detallado y Verificación Semántica por Dimensión

### Dimensión 1: Arquitectura Curricular, Topología DAG y Calibración ZPD (3.60 / 4.00)
- **Topología y Granularidad:** El grafo curricular contiene **30 competencias** (1 Hecho `H-01`, 16 Conceptos `C-01`..`C-17`, 13 Habilidades `Hab-01`..`Hab-19`), con 20 a 30 reactivos por competencia (`min=20`, `max=30`), 0 competencias subpobladas y 0 preguntas huérfanas. El DAG es acíclico (`has_cycle = false`), conexo en un solo componente (`connected_components_count = 1`, `max_dag_depth = 6`), con 0 prerrequisitos colgantes ni habilidades sin prerrequisitos.
- **Calibración ZPD:** 30/30 competencias poseen calibración tri-banda real (`easy`: 189 [25.89%], `medium`: 218 [29.86%], `hard`: 323 [44.25%]), habilitando `calibrateByMasteryDifficulty` en todas las transiciones.
- **Hallazgos:**
  - **5 pares con solapamiento curricular:** `C-01<->C-16` (*Principio del Máximo y Hamiltoniano* vs. *Principio del Máximo de Pontryagin*), `C-05<->C-14`, `C-05<->C-15`, `C-14<->C-15` (condiciones de transversalidad de estado/tiempo libre) y `Hab-11<->Hab-12` (*Extremales con Estado Final Libre* vs. *Extremales con Horizonte Libre*).
  - **2 competencias raíz sin prerrequisitos:** `C-01` y `C-07` (raíces paralelas de Control Óptimo y Cálculo de Variaciones).

### Dimensión 2: Calidad Psicométrica, Modalidad de Evocación y Anti-Gaming (5.00 / 5.00)
- **Distribución de Modalidades:** `multiple_choice_7_options` = 311 (42.60%), `fill_in_the_blank` = 243 (33.29%), `multiple_select` = 176 (24.11%), logrando **57.40%** de evocación activa/discriminación.
- **Entropía y Distractores:** Mínimo 16 esqueletos distintos observados por competencia; 2,232 distractores evaluados con **100.0%** de cobertura de `error_rationale`, 0 distractores imposibles por dominio, 0 claves corruptas, 0 multiplicadores mágicos, 0 respuestas memorizables y 0 relleno de longitud `[R-15]`.
- **Alertas de Contrato M20 y Sesgo MS (para remediación):**
  - **`[M20-MC7-CAP]` (13 críticas):** Todas las competencias `Skill` (`Hab-01`, `Hab-02`, `Hab-03`, `Hab-05`, `Hab-07`, `Hab-08`, `Hab-10`, `Hab-11`, `Hab-12`, `Hab-13`, `Hab-14`, `Hab-16`, `Hab-19`) conservan entre 8 y 16 reactivos `MC7` sobre 30, cuando M20 exige 0 `MC7` en competencias `Skill`.
  - **`[M20-ACTIVE-QUOTA]` (30 advertencias):** Las 30 competencias tienen entre 46.7% y 73.3% de modalidades activas, por debajo del umbral $\ge 80\%$ de M20.
  - **Sesgo de longitud en `multiple_select`:** 50/176 ítems MS (28.41%) presentan opciones correctas sistemáticamente más largas (ej. `Q-Hab03-124`..`130`, `Q-C04-146`..`150`, `Q-C05-166`, `Q-C05-168`, `Q-Hab05-194`).

### Dimensión 3: Andamiaje Socrático Progresivo y Remediación Diagnóstica (4.60 / 5.00)
- **Cobertura y Calidad Socrática:** 100.0% de los 730 reactivos cuentan con 3 a 5 pistas socráticas genuinas (0% Mad-Libs, 0% envenenamiento, 0% fuga de clave) y `100.0%` de unicidad de `error_rationale` por slot (`208/208` slots únicos).
- **Hallazgos Semánticos Concretos:**
  1. **Reciclaje de `misconception_warning` mudo (243 reactivos):** La cadena `$\frac{\partial\mathcal{H}}{\partial x}=\dot{\lambda}$` se repite sin explicación diagnóstica en prosa en 243 ítems a lo largo de las 30 competencias (ej. `Q-C01-011`).
  2. **Desfase paramétrico en `misconception_warning`:**
     - `Q-Hab11-492`: instruye *"evalúe en $t=2$"* cuando el reactivo pide $x(5)$ en $[0,10]$.
     - `Q-Hab14-621` y `Q-Hab14-622`: advierten sobre *"depreciación natural del $50\%$ anual... $\dot{x}=u-0.5x$"* cuando los reactivos usan $\dot{x}=u-0.2x$ y $\dot{x}=u-0.8x$.
     - `Q-Hab16-651` y `Q-Hab16-652`: mencionan *"$x(3)=0$ fijo, por lo que $\lambda(3)$ es libre"* cuando sus horizontes son $T=2$ y $T=4$.
  3. **Colisiones de concatenación en `hints`, `detailed_solution` y `error_rationale`:**
     - `Q-C01-011`: `hints[2]` y `detailed_solution` derivan $-2u^2$ como `-22u` y despejan `u^*=\frac{\lambda(16)}{22}` en vez de `-4u` y `/4` (aunque la respuesta `36` sí usa `/4`).
     - `Q-C07-251` y `Q-C07-252`: `detailed_solution` muestra `F=(53+4)t+(52+33)` y `F=(64+4)t+(62+44)` en lugar de `(5\cdot 3+4)t+(5\cdot 2+3\cdot 3)` y `(6\cdot 4+4)t+(6\cdot 2+4\cdot 4)`.
     - `Q-C14-471` y `Q-C14-472`: `detailed_solution` escribe `22\dot{x}` en lugar de `4\dot{x}` al derivar $2\dot{x}^2$.
     - `Q-Hab14-621` y `Q-Hab14-622`: `hints[2]` y `detailed_solution` muestran `-24u+\lambda=0` y `-21u+\lambda=0` en vez de `-8u+\lambda=0` y `-2u+\lambda=0`.
     - `Q-Hab16-651` y `Q-Hab16-652`: `detailed_solution` muestra `147-23u^*-\lambda^*=0` y `106-21u^*-\lambda^*=0` en vez de `2(3)u^*` y `2(1)u^*`.
     - `Q-C17-681` y `Q-C17-682`: `detailed_solution` y `error_rationale` fusionan productos en `62t`, `623`, `3623^2`, `343+34`, `81t`, `814`, `224+32`.

### Dimensión 4: Alineación Instruccional, Taxonomía de Bloom y Pureza de Dominio (3.86 / 4.00)
- **Alineación Cognitiva:** 100.0% de los reactivos `Skill` (390/390) están en `Apply+`, y 97.95% del banco total está en `Apply+` (`Apply`: 326, `Analyze`: 213, `Evaluate`: 176, `Understand`: 15), con 0 violaciones de coherencia `modalidad × bloom`.
- **Índice Bloom Ponderado:** `3.753 / 5.0` (piso adaptativo `3.87`, brecha `-0.117`, `53.29%` en `Analyze + Evaluate`, tier `SÓLIDO`).
- **Rigor Matemático:** Verificación simbólica y numérica positiva en las muestras auditadas (`Q-Hab01-041` $c_2=514$, `Q-Hab02-071` $\dot{C}/C=1.2180$, `Q-Hab03-101` $C^*=200$, `Q-Hab07-221` $C^*(1)=0.3736$, `Q-Hab10-441` $x(2)=15$, `Q-C15-521` $t_1=89.4$, `Q-Hab14-621` $u^*(4)=3.1019$, `Q-Hab16-651` $\lambda^*=111$, `Q-C17-681` $J=330$, `Q-Hab19-701` formulación en valor corriente).

### Dimensión 5: Accesibilidad, Ergonomía Cognitiva en UI y Sintaxis KaTeX (2.00 / 2.00)
- **Integridad KaTeX:** 0 delimitadores `$` desbalanceados, 0 llaves sin cerrar, 0 `$$$`, 0 `sympy` crudo en KaTeX, 0 residuos f-string/plantilla, 0 prosa desbordante en `\text{...}` y 0 identificadores Python crudos.

---

## 4. Índice de Preparación para el Dominio (`MPRI = 95.91 / 100.0`)

| Pilar Cognitivo / Plataforma | Puntaje | Máximo |
|---|---:|---:|
| `zpd_adaptive_progression` | 19.66 | 20.0 |
| `retrieval_modality_and_anti_gaming` | 20.00 | 20.0 |
| `socratic_scaffolding_lifeline` | 23.00 | 25.0 |
| `diagnostic_remediation_alignment` | 15.00 | 15.0 |
| `dag_and_interleaving_topology` | 8.25 | 10.0 |
| `cognitive_ergonomics_and_framing` | 10.00 | 10.0 |
| **Total MPRI** | **95.91** | **100.0** |

**Veredicto del recorrido del estudiante:** Certificado para dominio adaptativo (`GOLD MASTERY PATH`). Un estudiante recorre el DAG de 30 competencias con progresión ZPD tri-banda y andamiaje socrático sólido de 3 intentos, aunque al revisar soluciones detalladas o pistas en ítems puntuales encontrará colisiones tipográficas de multiplicación implícita (`-22u`, `623`, `23u^*`) y advertencias de error genéricas o con parámetros fijos.

---

## 5. Acciones de Remediación Recomendadas

1. **Corregir interpolación de productos en `hints`, `detailed_solution` y `error_rationale`:** Insertar `\cdot` o paréntesis explícitos en todas las plantillas que multiplican `2 * coef` o `a * b * t` (ej. `2({coef})u`, `{a}\cdot{b}t`) para eliminar colisiones como `-22u`, `-24u`, `22\dot{x}`, `23u^*`, `623` y `814`.
2. **Parametrizar o reescribir `misconception_warning`:** Reemplazar la cadena muda reciclada en 243 reactivos por explicaciones diagnósticas en prosa adaptadas al contexto de cada competencia, y parametrizar los valores fijos en `Hab-11` (`t=2`), `Hab-14` (`0.5x`) y `Hab-16` (`T=3`).
3. **Alinear modalidades al contrato M20 y equilibrar longitudes MS:** Migrar los reactivos `MC7` de las 13 competencias `Skill` hacia `FIB`/`MS`/`open_symbolic`, elevar la cuota activa $\ge 80\%$ y nivelar la longitud de distractores en los 50 ítems `MS` sesgados.
4. **Consolidar pares curriculares solapados y elevar Bloom:** Revisar si `C-14`/`C-15` vs. `C-05` y `C-16` vs. `C-01` pueden fusionarse o diferenciarse explícitamente en el DAG, e incrementar ligeramente la proporción de ítems `Analyze`/`Evaluate` para cerrar la brecha de `-0.12` respecto al piso `3.87`.

---

<details>
<summary>Metadatos Estructurados (JSON)</summary>

```json
{
  "course_metadata": {
    "course_id": "mateco_4_optimizacion_plus",
    "unit_title": "Mateco 4 Optimizacion Plus",
    "detected_objective": "Dominio y aplicación analítica integral de Mateco 4 Optimizacion Plus",
    "total_competencies": 30,
    "total_questions": 730,
    "bloom_index": {
      "weighted_index": 3.753,
      "adaptive_floor": 3.87,
      "gap": 0.117,
      "apply_plus_pct": 97.95,
      "superior_pct": 53.29,
      "tier": "SÓLIDO",
      "coherence_violations_count": 0
    }
  },
  "dimension_scores": {
    "architecture_granularity": {
      "score": 3.6,
      "max": 4.0,
      "feedback": "Estructura curricular con 30 competencias (1 Hechos, 16 Conceptos, 13 Habilidades). DAG acíclico y conexo (ciclos=False, comp. conexos=1, pares solapados=5). ZPD: 30/30 competencias con calibración tri-banda ('easy', 'medium', 'hard')."
    },
    "assessment_quality": {
      "score": 5.0,
      "max": 5.0,
      "feedback": "Modalidad: MC7=42.6%, FIB=33.29%, MS=24.11% (57.4% evocación activa/discriminación). Distractores: 2232 evaluados con 100.0% cobertura de error_rationale (imposibles por dominio=0, claves corruptas=0, sesgo MS=28.41%). Incumplimiento M20 en 13 Skill con MC7 y 30 competencias <80% activo."
    },
    "scaffolding_hints": {
      "score": 4.6,
      "max": 5.0,
      "feedback": "Andamiaje formativo: 100.0% de reactivos con 3 a 5 pistas socráticas escalonadas (100.0% pistas genuinas, 0.0% boilerplate Mad-Libs, 0.0% envenenadas). Unicidad diagnóstica real de rationales: 100.0% (243 advertencias clonadas/mudas y colisiones de concatenación numérica en detailed_solution/hints/error_rationale)."
    },
    "instructional_alignment": {
      "score": 3.86,
      "max": 4.0,
      "feedback": "Alineación cognitiva de Bloom: 100.0% de habilidades prácticas en Apply+; Índice Bloom ponderado: 3.75/5.0 (piso adaptativo 3.87, 53.3% Analyze+Evaluate, tier: SÓLIDO, incoherencias=0)."
    },
    "technical_ergonomics": {
      "score": 2.0,
      "max": 2.0,
      "feedback": "Sintaxis KaTeX: 0 errores críticos (delimitadores balanceados, llaves cerradas, cero $$$). Ergonomía: 0 observaciones de prosa en \\text{...}, 0 identificadores crudos, 0 colisiones en stem/options, 0 identidades tautológicas y 0 formatos flotantes/asteriscos crudos."
    }
  },
  "penalties_applied": [],
  "raw_subtotal": 19.06,
  "final_score": 19.06,
  "quality_tier": "EXCELENTE (17-20)",
  "mastery_path_readiness": {
    "mpri_score": 95.91,
    "mpri_max": 100.0,
    "mpri_tier": "GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo",
    "pillars": {
      "zpd_adaptive_progression": { "score": 19.66, "max": 20.0 },
      "retrieval_modality_and_anti_gaming": { "score": 20.0, "max": 20.0 },
      "socratic_scaffolding_lifeline": { "score": 23.0, "max": 25.0 },
      "diagnostic_remediation_alignment": { "score": 15.0, "max": 15.0 },
      "dag_and_interleaving_topology": { "score": 8.25, "max": 10.0 },
      "cognitive_ergonomics_and_framing": { "score": 10.0, "max": 10.0 }
    },
    "student_journey_verdict": "Certificado para dominio adaptativo (GOLD MASTERY PATH), con deuda menor en colisiones tipográficas de multiplicación implícita en soluciones/pistas, reciclaje de misconception_warning y contrato de modalidades M20 en Skill."
  },
  "discovered_lint_rules": [
    {
      "rule_id": "R-IMPLICIT-MULT-CONCAT-SCAFFOLDING",
      "severity": "warning",
      "regex_pattern": "(?:-?\\d{2,}[uUxXt]|\\(\\d{2,}\\+\\d+\\)|/2\\d\\b)",
      "description": "Detecta colisiones de concatenación de dígitos por multiplicación implícita sin \\cdot o paréntesis dentro de hints, detailed_solution y error_rationale (ej. -22u, -24u, 22\\dot{x}, 62t, 623, 23u^*).",
      "evidence_items": [
        "Q-C01-011",
        "Q-C07-251",
        "Q-C07-252",
        "Q-C14-471",
        "Q-C14-472",
        "Q-Hab14-621",
        "Q-Hab14-622",
        "Q-Hab16-651",
        "Q-Hab16-652",
        "Q-C17-681",
        "Q-C17-682"
      ]
    }
  ],
  "remediation_actions": [
    "Insertar \\cdot o paréntesis explícitos en multiplicaciones de parámetros dentro de hints, detailed_solution y error_rationale (ej. -2({b})u, {a}\\cdot{b}t).",
    "Reemplazar las 243 cadenas mudas recicladas de misconception_warning y parametrizar los valores fijos en Hab-11 (t=2), Hab-14 (0.5x) y Hab-16 (T=3).",
    "Eliminar reactivos MC7 de las 13 competencias Skill y elevar modalidades activas >=80% conforme al contrato M20.",
    "Balancear longitud de opciones correctas en los 50 reactivos multiple_select con sesgo (28.41%).",
    "Consolidar o desambiguar los 5 pares de competencias solapadas en el DAG (C-01<->C-16, C-05<->C-14, C-05<->C-15, C-14<->C-15, Hab-11<->Hab-12) y elevar el Índice Bloom Ponderado >= 3.87."
  ]
}
```

</details>
