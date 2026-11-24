# Reporte de Auditoría QA: `solow_v13_m20` (Solow V13 M20)

> [!WARNING]
> **CURSO RETIRADO DE LA PLATAFORMA**: Este curso fue eliminado de la plataforma interactiva el **2026-11-24 04:14:51**. Este informe de auditoría se conserva exclusivamente como registro histórico y pedagógico ('legacy').

**Estado en Plataforma:** ELIMINADO  
**Fecha de Eliminación:** 2026-11-24 04:14:51  
**Calificación Final QM-OSCQR**: **19.92 / 20.00** — **EXCELENTE (19.0 - 20.0 pts) — PLATINUM MASTERY**  
**Índice de Preparación para el Dominio (MPRI)**: **99.65 / 100.00** — **GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo**  
**Fecha de Auditoría**: 2026-11-24  
**Conversación de Origen**: `Solow Model Course Generation` (`181a95d7-eb3c-43b1-9b0b-bb3d344940e0`)

---

## 1. Resumen Ejecutivo y Perfil del Curso

El curso **`solow_v13_m20`** (*Solow V13 M20*) consta de **20 competencias** (1 Hecho, 11 Conceptos, 8 Habilidades) y **480 reactivos** (20 por Hecho/Concepto, 30 por Habilidad), con validación de plataforma limpia (`platform_validation_error = null`) y **100.00%** de acuerdo en la auditoría ciega de Stage 5 (`145/145` ítems juzgados, `0` desacuerdos sin reparar).

| Métrica Global | Valor | Estado |
| :--- | :---: | :--- |
| Competencias Totales | 20 | 1 Fact, 11 Concept, 8 Skill |
| Reactivos Totales | 480 | 20–30 reactivos/competencia |
| Calificación QM-OSCQR | **19.92 / 20.00** | PLATINUM MASTERY |
| Índice MPRI | **99.65 / 100.00** | GOLD MASTERY PATH |
| Penalizaciones Duras | 0 (0.00 pts) | Sin bloqueos críticos |
| Riesgo Residual (`risk_score`) | 0.10 | Mínimo |
| Acuerdo Jueces Ciegos (Stage 5) | 100.00% (145/145) | Sin desacuerdos latentes |

---

## 2. Evaluación Normativa QM-OSCQR (20.00 Puntos)

| Dimensión | Puntaje | Máximo | Hallazgos Clave |
| :--- | :---: | :---: | :--- |
| **D1. Arquitectura Curricular, Topología DAG y ZPD** | **3.92** | 4.00 | DAG acíclico y conexo (`has_cycle = false`, `connected_components = 1`, `max_dag_depth = 4`). **20/20** competencias con calibración tri-banda (`easy`: 164, `medium`: 164, `hard`: 152). Deducción menor (`-0.08`) por solapamiento curricular entre `Hab-02` (*Solución Cuantitativa con Función Cobb-Douglas*) y `Hab-04` (*Solución y Equilibrio Cobb-Douglas*). |
| **D2. Calidad Psicométrica, Modalidad y Anti-Gaming** | **5.00** | 5.00 | `MC7 = 0.00%`, `FIB = 14.17%` (68), `MS = 15.42%` (74), `BloomSup = 70.42%` (338); **100.00%** evocación activa/discriminación. `207/207` distractores con `error_rationale` (`100.00%`), `0` imposibles por dominio, `0` claves corruptas. Sesgo de longitud en MS: `4.05%` (`3/74`: `Q-C10-405`, `Q-C10-406`, `Q-C10-407`), dentro de tolerancia. |
| **D3. Andamiaje Socrático y Remediación Diagnóstica** | **5.00** | 5.00 | **100.00%** de reactivos con 3–5 pistas socráticas escalonadas (`100.00%` genuinas, `0.00%` Mad-Libs, `0.00%` envenenadas, `0` fugas de respuesta). Unicidad diagnóstica de rationales por slot: **100.00%** (`39/39`), unicidad por instancia: `40.58%` (`84/207`), `0` rationales numéricos desconectados, `0` advertencias clonadas. |
| **D4. Alineación Instruccional, Bloom y Pureza de Dominio** | **4.00** | 4.00 | **100.00%** (`240/240`) de reactivos de Habilidad en `Apply+`. **Índice Bloom Real Generado (`bloom_weighted_index`): 3.98 / 5.00** vs **Piso Bloom Expected (`adaptive_bloom_floor`): 3.85 / 5.00** (`gap = 0.00`, `Apply+ = 92.29%`, `Analyze+Evaluate = 65.42%`, tier: **ÉLITE**, `0` violaciones de coherencia `modalidad × bloom`). |
| **D5. Accesibilidad, Ergonomía UI y Sintaxis KaTeX** | **2.00** | 2.00 | **0** errores KaTeX (llaves cerradas, delimitadores balanceados, cero `$$$`, cero `sympy_in_katex`). **0** observaciones de prosa en `\text{...}`, `0` identificadores crudos, `0` colisiones por concatenación, `0` identidades tautológicas, `0` residuos de plantilla o reemplazo ciego. |
| **Penalizaciones Duras** | **0.00** | — | Ninguna penalización aplicada. |
| **TOTAL FINAL** | **19.92** | **20.00** | **EXCELENTE — PLATINUM MASTERY** |

---

## 3. Mastery Path Readiness Index (MPRI: 99.65 / 100.00)

| Pilar MPRI | Puntaje | Máximo | Detalle Técnico |
| :--- | :---: | :---: | :--- |
| **Pilar 1. Progresión Adaptativa ZPD** | **20.00** | 20.00 | 20/20 competencias tri-banda (`easy`/`medium`/`hard`), 100.00% Habilidades en `Apply+`, **`bloom_weighted_index = 3.98`** frente a **`adaptive_bloom_floor = 3.85`** (`gap = 0.00`). |
| **Pilar 2. Modalidad de Evocación y Anti-Gaming** | **20.00** | 20.00 | 100.00% evocación activa/discriminación (`MC7 = 0.00%`), `>= 16` esqueletos distintos por competencia, `0` ítems memorizables, `0` cuantificadores vacuos. |
| **Pilar 3. Andamiaje Socrático (3-Strikes)** | **25.00** | 25.00 | 100.00% pistas socráticas genuinas, 0.00% boilerplate, 0.00% envenenamiento. |
| **Pilar 4. Alineación Diagnóstica de Remediación** | **15.00** | 15.00 | 100.00% cobertura de `error_rationale` y unicidad por slot (`39/39`), `0` multiplicadores mágicos. |
| **Pilar 5. Topología DAG e Interleaving** | **9.65** | 10.00 | Grafo conexo acíclico de profundidad 4; deducción menor (`-0.35`) por par solapado `Hab-02 <-> Hab-04`. |
| **Pilar 6. Ergonomía Cognitiva y Encuadre** | **10.00** | 10.00 | KaTeX 100.00% limpio, sin prefijos inter-dominio ni prosa desbordante en `\text{...}`. |

---

## 4. Auditoría Explícita de Regresión Histórica (`courses/solow_v13_m20.json`)

Se verificaron directamente los 6 patrones históricos documentados en auditorías previas de `content-to-course`:

| Patrón Histórico Auditado | Resultado en `solow_v13_m20` | Veredicto |
| :--- | :--- | :---: |
| **`multiple_select`** (4 opciones / siempre 2 correctas) | **0/74 (0.00%)** con 4 opciones: `52/74` (**70.27%**) tienen **5 opciones** y `22/74` (**29.73%**) tienen **6 opciones**. En claves correctas: `37/74` (**50.00%**) tienen **2 correctas** y `37/74` (**50.00%**) tienen **3 correctas** (rompe el patrón rígido $\binom{4}{2}=6$, aunque sin casos de 1 o 4 correctas). | **SUPERADO** |
| **`invariant_canvas`** (`fixed_curves` + solo `P1` sin `interactive_curves`, `step_mismatch`) | **0/40 (0.00%)** con `fixed_curves` que dibujen la solución pidiendo solo mover `P1` sin interacción de curva: `20/40` (**50.00%**) usan `interactive_curves` y `20/40` (**50.00%**) usan `sliders` activos. **`step_mismatch`: 0/40 (0.00%)** (todas las coordenadas objetivo son múltiplos exactos de `step`). | **SUPERADO** |
| **`adversarial_break`** (sesgo posicional `R1` / `S3`) | De 100 ítems (`50` modo `counterexample`, `50` modo `fallacy`): en `fallacy`, `correct_reason_id` se distribuye en **`R1`: 22/50 (44.00%)**, **`R2`: 14/50 (28.00%)**, **`R3`: 14/50 (28.00%)** (superado el sesgo de 100% en `R1`). Sin embargo, `fallacy_step_id` aún muestra concentración moderada en **`S3`: 33/50 (66.00%)** vs **`S2`: 17/50 (34.00%)** (`0` en `S1`/`S4`). | **PARCIAL (Alerta menor en `S3`)** |
| **`proof_dag`** (cadenas lineales triviales de 3–4 pasos) | **30/34 (88.24%)** son DAGs ramificados reales de 5 a 7 nodos (incluyendo nodos distractores y bifurcaciones/convergencias, ej. `S1->S3, S2->S3, S3->S4`). Solo **4/34 (11.76%)** (`Q-C04-145` a `Q-C04-148`) presentan secuencia lineal de 4 pasos requeridos dentro de 5 nodos totales. | **SUPERADO** |
| **`concept_matching`** (2–3 pares, sin distractores, mapeo `P_i -> T_i`) | **12/12 (100.00%)** tienen **4 pares** (`0` con 2–3 pares), **12/12 (100.00%)** incluyen **distractores** (6 objetivos para 4 premisas) y **0/12 (0.00%)** tienen mapeo trivial `P_i -> T_i`. | **SUPERADO** |
| **Interpolación literal, inconsistencias y palabras absolutas** | **0/480 (0.00%)** bugs de interpolación literal (`Si $N=0$`, `($N>0$)`, `{{...}}`). **0** inconsistencias conceptuales entre competencias. Palabras absolutas en `multiple_select`: **`9/207` (4.35%)** en distractores vs **`12/185` (6.49%)** en opciones correctas (**sin sesgo** hacia distractores). | **SUPERADO** |

---

## 5. Acciones de Mejora Recomendadas (No Bloqueantes)

1. **Diferenciar o fusionar `Hab-02` y `Hab-04` (`architecture_dag_linter`)**: Aunque `Hab-02` usa la notación $\dot{k} + \lambda k = s k^\alpha$ (linealización Bernoulli) y `Hab-04` usa $\dot{K} = s K^a (L_0 e^{nt})^{1-a}$ (integración directa), unificar o explicitar la distinción metodológica en sus nombres evitaría el warning de solapamiento (`-0.08` pts en D1).
2. **Diversificar `fallacy_step_id` en `adversarial_break` (`S1`/`S2`/`S4`)**: Reducir la frecuencia de `S3` (`66.00%`) introduciendo falacias en `S1` y `S4` para eliminar cualquier heurística posicional en modo `fallacy`.
3. **Incluir 1 o 4 correctas en `multiple_select` y eliminar sesgo de longitud en `Q-C10-405..407`**: Ampliar la cardinalidad de `multiple_select` más allá de `{2, 3}` y nivelar la longitud de distractores en `C-10` (70–75 chars vs 83–85 chars).

---

<details>
<summary>Metadatos Estructurados (JSON)</summary>

```json
{
  "course_metadata": {
    "course_id": "solow_v13_m20",
    "unit_title": "Solow V13 M20",
    "detected_objective": "Dominio y aplicación analítica integral del modelo de crecimiento neoclásico de Solow (ecuación fundamental, estabilidad, Cobb-Douglas, proporciones fijas, sustituibilidad parcial, precios factoriales, progreso técnico, ahorro variable, población endógena y rigideces).",
    "total_competencies": 20,
    "total_questions": 480,
    "bloom_index": {
      "weighted_index": 3.98,
      "adaptive_floor": 3.85,
      "gap": 0.0,
      "apply_plus_pct": 92.29,
      "superior_pct": 65.42,
      "tier": "ÉLITE",
      "coherence_violations_count": 0
    }
  },
  "dimension_scores": {
    "architecture_granularity": {
      "score": 3.92,
      "max": 4.0,
      "feedback": "Estructura curricular con 20 competencias (1 Hechos, 11 Conceptos, 8 Habilidades). DAG acíclico y conexo (ciclos=False, comp. conexos=1, pares solapados=1: Hab-02<->Hab-04). ZPD: 20/20 competencias con calibración tri-banda ('easy', 'medium', 'hard')."
    },
    "assessment_quality": {
      "score": 5.0,
      "max": 5.0,
      "feedback": "Modalidad: MC7=0.0%, FIB=14.17%, MS=15.42%, BloomSup=70.42% (100.0% evocación activa/discriminación). Distractores: 207 evaluados con 100.0% cobertura de error_rationale (imposibles por dominio=0, claves corruptas=0, sesgo MS=4.05%)."
    },
    "scaffolding_hints": {
      "score": 5.0,
      "max": 5.0,
      "feedback": "Andamiaje formativo: 100.0% de reactivos con 3 a 5 pistas socráticas escalonadas (100.0% pistas genuinas, 0.0% boilerplate Mad-Libs, 0.0% envenenadas). Unicidad diagnóstica real de rationales: 100.0% por slot (rationales numéricos desconectados=0, advertencias clonadas/mudas=0)."
    },
    "instructional_alignment": {
      "score": 4.0,
      "max": 4.0,
      "feedback": "Alineación cognitiva de Bloom: 100.0% de habilidades prácticas en Apply+; Índice Bloom Real Generado: 3.98/5.0 vs Piso Bloom Expected (Adaptativo): 3.85/5.0 (65.42% Analyze+Evaluate, tier: ÉLITE, incoherencias=0)."
    },
    "technical_ergonomics": {
      "score": 2.0,
      "max": 2.0,
      "feedback": "Sintaxis KaTeX: 0 errores críticos. Ergonomía: 0 observaciones de prosa en \\text{...}, 0 identificadores crudos, 0 colisiones por concatenación, 0 identidades tautológicas, 0 formatos flotantes/asteriscos crudos y 0 residuos de plantilla/reemplazo."
    }
  },
  "penalties_applied": [],
  "raw_subtotal": 19.92,
  "final_score": 19.92,
  "quality_tier": "EXCELENTE (19.0 - 20.0 pts) — PLATINUM MASTERY",
  "mastery_path_readiness": {
    "mpri_score": 99.65,
    "mpri_max": 100.0,
    "mpri_tier": "GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo",
    "pillars": {
      "zpd_adaptive_progression": { "score": 20.0, "max": 20.0 },
      "retrieval_modality_and_anti_gaming": { "score": 20.0, "max": 20.0 },
      "socratic_scaffolding_lifeline": { "score": 25.0, "max": 25.0 },
      "diagnostic_remediation_alignment": { "score": 15.0, "max": 15.0 },
      "dag_and_interleaving_topology": { "score": 9.65, "max": 10.0 },
      "cognitive_ergonomics_and_framing": { "score": 10.0, "max": 10.0 }
    },
    "student_journey_verdict": "Certificado para producción inmediata en Mastery Path adaptativo: progresión ZPD tri-banda completa, 100% evocación activa/discriminación y andamiaje socrático genuino sin sesgos críticos."
  },
  "discovered_lint_rules": [
    {
      "rule_id": "adversarial_break_fallacy_step_skew",
      "severity": "info",
      "regex_pattern": "\"fallacy_step_id\":\\s*\"S3\"",
      "description": "Concentración moderada (66.00%, 33/50) del paso falaz en S3 dentro de reactivos adversarial_break en modo fallacy; conviene equilibrar entre S1, S2, S3 y S4.",
      "evidence_items": ["Q-C01-027", "Q-Hab01-045", "Q-C02-075"]
    }
  ],
  "remediation_actions": [
    "Clarificar o fusionar el solapamiento curricular entre Hab-02 y Hab-04 para alcanzar 4.00/4.00 en D1 y 100.00/100.00 en MPRI.",
    "Distribuir fallacy_step_id en adversarial_break (modo fallacy) más allá de S2 y S3 (incluir S1 y S4).",
    "Balancear longitud de opciones en Q-C10-405, Q-C10-406 y Q-C10-407 y añadir ítems multiple_select con 1 o 4 opciones correctas."
  ]
}
```

</details>
