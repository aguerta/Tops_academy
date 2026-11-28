# Informe de Auditoría de Calidad Pedagógica, Psicométrica y Rigor Disciplinar (QM-OSCQR)
## Curso: Mateco 4 Test K4 (`mateco_4_test_k4`)

- **Fecha de Evaluación:** 2026-11-27
- **Evaluador:** Course QA Auditor — Top's Academy (Auditoría Agéntica Híbrida: Telemetría Determinista + Verificación Semántica Directa)
- **Estado en Plataforma:** ELIMINADO  
**Fecha de Eliminación:** 2026-11-28 05:27:42  
- **Calificación Final Certificada:** **18.39 / 20.0 pts** *(ajustada desde `19.59` determinista tras inspección semántica directa)*
- **Quality Tier:** **EXCELENTE (17.0 - 20.0 pts)**
- **Mastery Path Readiness Index (MPRI):** **93.52 / 100.0** (`GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo`, ajustado desde `98.22`)
- **Índice Bloom Ponderado (1–5):** **3.84 / 5.0** (Piso Bloom Expected: **3.85** | Brecha: **-0.01** | `Apply+`: **91.31%** | `Analyze+Evaluate`: **62.72%** | Tier: **SÓLIDO**)

---

### 1. Resumen Ejecutivo de Dimensiones

| Dimensión | Puntuación | Máximo | Calificación | Estado |
| :--- | :---: | :---: | :---: | :--- |
| **D1: Arquitectura Curricular, Topología DAG y ZPD** | **3.60** | 4.00 | 90.00% | ✨ Excelente |
| **D2: Calidad Psicométrica, Modalidad y Anti-Gaming** | **4.85** | 5.00 | 97.00% | ✅ Sólido |
| **D3: Andamiaje Socrático y Remediación Diagnóstica** | **4.55** | 5.00 | 91.00% | ⚠️ Con observaciones semánticas |
| **D4: Alineación Instruccional, Bloom y Rigor (Piso Bloom Expected: `3.85` \| Real Generado: `3.84` / 5.0)** | **3.74** | 4.00 | 93.50% | ⚠️ Rigor 100%, leve Bloom Goodharting |
| **D5: Ergonomía Técnica, UI y Sintaxis KaTeX** | **1.65** | 2.00 | 82.50% | ⚠️ Fricción por `allow_calculator: false` |
| **Penalizaciones Duras** | **-0.00** | - | - | ✅ Sin penalizaciones duras |
| **TOTAL** | **18.39** | **20.00** | **91.95%** | 🏆 **EXCELENTE** |

---

### 2. Desglose Detallado por Dimensión y Hallazgos Semánticos

#### D1. Arquitectura Curricular, Topología DAG y Calibración ZPD (3.60 / 4.00 pts)
- **Telemetría:** 57 competencias (6 Hechos, 22 Conceptos, 29 Habilidades) y 2,452 reactivos (36 a 64 por competencia). DAG acíclico (`has_cycle = false`), conexo (`connected_components_count = 1`), profundidad máxima 9 y calibración tri-banda ZPD (`easy`: 826, `medium`: 813, `hard`: 813) en el 57/57 de competencias.
- **Análisis Semántico de Solapamientos:** El linter reportó 5 pares solapados (`PRE-01<->PRE-02`, `Hab-03<->C-06`, `C-09<->C-22`, `Hab-07<->Hab-20`, `Hab-19<->Hab-20`). Al revisar las descripciones, `PRE-01` vs `PRE-02`, `C-09` vs `C-22` y `Hab-07` vs `Hab-20` corresponden a la transición legítima entre **Cálculo de Variaciones** y **Control Óptimo (Pontryagin)**, mientras que `Hab-03` (*Verificación de Optimalidad con Hessiano*) y `C-06` (*Condición de Legendre y Suficiencia Hessiana*) sí presentan superposición conceptual real. Se mantiene el puntaje determinista `3.60 / 4.00`.

#### D2. Calidad Psicométrica, Modalidad y Anti-Gaming (4.85 / 5.00 pts)
- **Modalidad:** 100.00% evocación activa / discriminación superior (`MC7`: 0.00%, `fill_in_the_blank`: 16.48% [404], `multiple_select`: 15.01% [368], `BloomSup`: 68.52% [1,680: `open_symbolic`=500, `adversarial_break`=476, `unstructured_model`=416, `proof_dag`=192, `concept_matching`=96]).
- **Integridad de Distractores y Jueces:** 1,288 distractores planos con 100.00% de `error_rationale`, 0 sesgo de longitud en `MS` (`0.00%`), 0 distractores mágicos y 143/143 acuerdos en `stage5_judge_audit`.
- **Ajuste por Hallazgo Invisible (-0.15 pts):** Aunque los 1,288 distractores planos están limpios, la inspección directa de `unstructured_model` reveló plantillas mecánicas en los `error_rationale` de las fases 1 y 2 (ver D3), afectando la calidad diagnóstica de 416 reactivos.

#### D3. Andamiaje Socrático y Remediación Diagnóstica (4.55 / 5.00 pts)
- **Fortalezas:** 100.00% de los 2,452 reactivos cuentan con 3 a 5 pistas socráticas genuinas y específicas (0.00% boilerplate Mad-Libs en `hints`, 0.00% envenenamiento).
- **Defecto Invisible #1 — Rationales Boilerplate en `unstructured_model` (-0.35 pts):** El linter `diagnostic_rationale_alignment_linter` solo audita distractores planos y omitió las fases internas de los 416 `unstructured_model`, donde se detectaron **1,004** `error_rationale` de plantilla:
  - **633 ocurrencias** en `phase2_assumptions` con el patrón `"Verifica la validez analítica del supuesto <content>."` (generando doble punto `..`), p. ej.:
    - `Q-C01-109` (`A1`): `"Verifica la validez analítica del supuesto La trayectoria $y(t)$ es diferenciable a trozos en $[0,4]$.."`
    - `Q-C01-115` (`A1`): `"Verifica la validez analítica del supuesto La forma $V[y]=\\int_0^{7} F[t,y(t),y'(t)]\\,dt$ conserva las tres entradas $t, y(t), y'(t)$.."`
    - `Q-Hab09-914` (`A1`): `"Verifica la validez analítica del supuesto Condición de Legendre estricta $F_{\\dot{\\pi}\\dot{\\pi}} > 0$ para $\\beta=5, j=3, \\alpha=7$."`
  - **371 ocurrencias** en `phase1_variables` con el patrón `"Revisa el rol estructural de <label> dentro del modelo."`, p. ej.:
    - `Q-Hab09-914` (`V3`): `"Revisa el rol estructural de $F_{\\pi\\dot{\\pi}} = \\frac{2 \\cdot 7}{3}$ dentro del modelo."`
- **Defecto #2 — Advertencias con Parámetros Estáticos No Instanciados (-0.10 pts):** Confirmado en 19 reactivos (`Q-Hab07-725` + 11 de `Hab-07`, `Q-Hab09-914` + 2 de `Hab-09`, `Q-Hab28-2337` + 3 de `Hab-28`). Ejemplo verbatim en `Q-Hab07-725` (cuyo integrando es $35\dot{x}^2+5x+50$):
  - `misconception_warning`: `"Agrupe correctamente los términos cuadráticos en $\\dot{x}$: $F - \\dot{x}F_{\\dot{x}}$ reduce el coeficiente cuadrático a $3\\dot{x}^2 - 6\\dot{x}^2 = -3\\dot{x}^2$."` (ejemplo estático no instanciado).

#### D4. Alineación Instruccional, Bloom y Rigor Disciplinar (3.74 / 4.00 pts)
- **Métricas Bloom Deterministas:** Piso Bloom Expected (`adaptive_bloom_floor`): **`3.85`** | Índice Bloom Real Generado (`bloom_weighted_index`): **`3.84 / 5.0`** (brecha `-0.01`, `Apply+`: `91.31%`, `Analyze+Evaluate`: `62.72%`, `Skill Apply+`: `100.00%`).
- **Rigor Matemático (Sobresaliente):** El muestreo directo de `Hab-02`, `Hab-03`, `Hab-07`, `Hab-09`, `Hab-11`, `Hab-15`, `Hab-16`, `Hab-18`, `Hab-21`, `Hab-22`, `Hab-25`, `Hab-26`, `Hab-28`, `Hab-29` y `Hab-30` confirma rigor algebraico y variacional impecable:
  - `Q-Hab16-1429` (Hamiltoniano corriente): $\mathcal{H}=8x^2+6u+m(5u-4x)$, $\rho=7 \implies \dot{m}=(7+4)m-16x$ (exacto).
  - `Q-Hab18-1561` (Utilidad logarítmica descontada): $c^*(t)=e^{10t}/5$ (exacto).
  - `Q-Hab21-1813` (Regla de Keynes-Ramsey RCK): $\dot{c}=(c/4)(16/(2\sqrt{k})-0.09)$ (exacto).
  - `Q-Hab22-1897` (Precio sombra negativo de contaminación): $\lambda^*(t)=7e^{-0.05t}(e^{-0.06(6-t)}-1)$ (exacto).
  - `Q-Hab25-2113` (Euler con daño ambiental): $\dot{C}/C = f'(K)-0.05-9KC-0.09$ (exacto).
  - `Q-Hab29-2357` (Permisos de emisión) y `Q-Hab30-2405` (Control del delito): signos y condiciones de transversalidad exactos.
- **Defecto Invisible #3 — Bloom Goodharting en `Fact` y `Concept` (-0.25 pts):** Se detectó inflación de etiquetas Bloom en reactivos iniciales de hechos y conceptos:
  - `Q-PRE01-016` (`PRE-01`, categoría `Fact`, `multiple_select`): etiquetado como **`Evaluate`**, aunque solo pide identificar propiedades declarativas elementales (`x(0)=6` y criterio de minimización en daño social).
  - `Q-C01-115` (`C-01`, categoría `Concept`, `unstructured_model`): etiquetado como **`Create`**, aunque solo perturba un coeficiente de $6$ a $12$ en una plantilla fija de clasificación de dominio/codominio.

#### D5. Ergonomía Técnica, UI y Sintaxis KaTeX (1.65 / 2.00 pts)
- **Sintaxis KaTeX:** 0 errores críticos, 0 `\text{prosa}`, 0 identificadores crudos, 0 residuos de plantilla.
- **Defecto Invisible #4 — `allow_calculator: false` en el 100% del curso (2,452/2,452) con cálculo trascendente a 4 decimales (-0.35 pts):** Existen reactivos `fill_in_the_blank` (`tolerance: 0.005`) que exigen evaluar exponenciales o raíces irracionales a 4 decimales sin calculadora habilitada:
  - `Q-Hab02-353`: `"Determine $x(1)$ en la trayectoria $x(t)=c_1 e^{-t}+c_2 e^t$ con $c_1=4$ y $c_2=7$ (redondee a 4 decimales)."` -> `20.4995` (`allow_calculator: false`).
  - `Q-Hab09-923`: `"Calcule la raíz característica positiva $r_1 = \\frac{\\beta j \\sqrt{\\alpha}}{\\sqrt{1+\\beta^2\\alpha}}$ para $\\beta=3$, $j=2$ y $\\alpha=6$ (redondee a 4 decimales)"` -> `1.9817` (`allow_calculator: false`).
  - `Q-Hab11-1013`: `"Con condiciones no negativas ($P_0=22$, $a=8$, $b=2$), calcule el nivel de contaminación $P(2.0)$ de $P(t)=22 e^{-\\sqrt{8/2}\\,t}$ (redondee a 4 decimales):"` -> `0.4029` (`allow_calculator: false`, y sin aproximación de $e^{-4}$ en las pistas).

---

### 3. Índice de Preparación para el Dominio (MPRI: 93.52 / 100.0 pts)

| Pilar Cognitivo | Puntaje | Máximo | Calificación |
| :--- | :---: | :---: | :---: |
| **1. Progresión Adaptativa ZPD y Bloom** *(Piso Bloom Expected: `3.85` \| Real Generado: `3.84` / 5.0)* | **19.47** | 20.00 | 97.35% |
| **2. Modalidad de Evocación y Anti-Gaming** | **19.60** | 20.00 | 98.00% |
| **3. Andamiaje Socrático (3-Strikes Lifeline)** | **24.20** | 25.00 | 96.80% |
| **4. Alineación Diagnóstica y Remediación** | **13.50** | 15.00 | 90.00% |
| **5. Topología DAG e Interleaving** | **8.25** | 10.00 | 82.50% |
| **6. Ergonomía Cognitiva y Pureza de Dominio** | **8.50** | 10.00 | 85.00% |
| **TOTAL MPRI** | **93.52** | **100.00** | **93.52%** |

> **Veredicto del Viaje del Estudiante:** El curso posee un rigor matemático sobresaliente en cálculo de variaciones y control óptimo, 100% de evocación activa/discriminación y calibración ZPD tri-banda completa; sin embargo, antes del despliegue masivo debe habilitarse `allow_calculator: true` en ítems `FIB` con exponenciales/raíces irracionales y reemplazarse los 1,004 rationales boilerplate en `unstructured_model`.

---

### 4. Acciones de Remediación Prioritarias

1. **[ALTA — Ergonomía UI]** Activar `"allow_calculator": true` en todos los reactivos `fill_in_the_blank` que requieran evaluación numérica de exponenciales, logaritmos o raíces irracionales a 4 decimales (`Q-Hab02-353`, `Q-Hab09-923`, `Q-Hab11-1013` y equivalentes).
2. **[ALTA — Andamiaje `unstructured_model`]** Reescribir los 1,004 `error_rationale` de plantilla en `phase1_variables` (`"Revisa el rol estructural de..."`, 371 casos) y `phase2_assumptions` (`"Verifica la validez analítica del supuesto..."`, 633 casos) para ofrecer retroalimentación diagnóstica específica (p. ej. `Q-C01-109`, `Q-C01-115`, `Q-Hab09-914`).
3. **[MEDIA — Taxonomía Bloom]** Recalibrar las etiquetas `Evaluate` y `Create` en competencias `Fact` y `Concept` iniciales (`Q-PRE01-016`, `Q-C01-115`) a `Understand`/`Apply`/`Analyze` según la demanda cognitiva real.
4. **[BAJA — Instanciación de Advertencias]** Parametrizar `misconception_warning` en los 19 reactivos de `Hab-07` (`Q-Hab07-725`), `Hab-09` (`Q-Hab09-914`) y `Hab-28` (`Q-Hab28-2337`).

---

<details>
<summary>Metadatos Estructurados (JSON)</summary>

```json
{
  "course_metadata": {
    "course_id": "mateco_4_test_k4",
    "unit_title": "Mateco 4 Test K4",
    "detected_objective": "Dominio y aplicación analítica integral de Cálculo de Variaciones y Control Óptimo en Economía",
    "total_competencies": 57,
    "total_questions": 2452,
    "bloom_index": {
      "weighted_index": 3.84,
      "adaptive_floor": 3.85,
      "gap": -0.01,
      "apply_plus_pct": 91.31,
      "superior_pct": 62.72,
      "tier": "SÓLIDO",
      "coherence_violations_count": 0
    }
  },
  "dimension_scores": {
    "architecture_granularity": {
      "score": 3.6,
      "max": 4.0,
      "feedback": "57 competencias (6 Hechos, 22 Conceptos, 29 Habilidades), DAG acíclico y conexo, calibración ZPD tri-banda en 57/57 competencias; solapamiento real focalizado en Hab-03<->C-06."
    },
    "assessment_quality": {
      "score": 4.85,
      "max": 5.0,
      "feedback": "100.0% evocación activa/discriminación (MC7=0%, FIB=16.48%, MS=15.01%, BloomSup=68.52%), 143/143 acuerdos Stage-5; deducción -0.15 por rationales boilerplate en fases internas de unstructured_model."
    },
    "scaffolding_hints": {
      "score": 4.55,
      "max": 5.0,
      "feedback": "100.0% pistas socráticas genuinas; deducción -0.45 por 1,004 error_rationale boilerplate en unstructured_model (633 en phase2, 371 en phase1) y 19 misconception_warning con parámetros estáticos no instanciados."
    },
    "instructional_alignment": {
      "score": 3.74,
      "max": 4.0,
      "feedback": "Rigor matemático 100% exacto en muestreo de optimización dinámica y control óptimo; Bloom Real Generado 3.84 vs Piso Bloom Expected 3.85; deducción -0.25 por Bloom Goodharting en Fact/Concept (Q-PRE01-016, Q-C01-115)."
    },
    "technical_ergonomics": {
      "score": 1.65,
      "max": 2.0,
      "feedback": "KaTeX 100% limpio; deducción -0.35 por allow_calculator: false global (2,452/2,452) en reactivos FIB que exigen 4 decimales con exponenciales y raíces irracionales (Q-Hab02-353, Q-Hab09-923, Q-Hab11-1013)."
    }
  },
  "penalties_applied": [],
  "raw_subtotal": 18.39,
  "final_score": 18.39,
  "quality_tier": "EXCELENTE (17-20)",
  "mastery_path_readiness": {
    "mpri_score": 93.52,
    "mpri_max": 100.0,
    "mpri_tier": "GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo",
    "pillars": {
      "zpd_adaptive_progression": {
        "score": 19.47,
        "max": 20.0
      },
      "retrieval_modality_and_anti_gaming": {
        "score": 19.6,
        "max": 20.0
      },
      "socratic_scaffolding_lifeline": {
        "score": 24.2,
        "max": 25.0
      },
      "diagnostic_remediation_alignment": {
        "score": 13.5,
        "max": 15.0
      },
      "dag_and_interleaving_topology": {
        "score": 8.25,
        "max": 10.0
      },
      "cognitive_ergonomics_and_framing": {
        "score": 8.5,
        "max": 10.0
      }
    },
    "student_journey_verdict": "Curso riguroso y certificado (18.39/20.0, MPRI 93.52), con remediación prioritaria en allow_calculator para FIB trascendentes y rationales internos de unstructured_model."
  },
  "discovered_lint_rules": [
    {
      "rule_id": "UNSTRUCTURED_MODEL_BOILERPLATE_RATIONALE",
      "severity": "warning",
      "regex_pattern": "\"error_rationale\":\\s*\"(Verifica la validez analítica del supuesto |Revisa el rol estructural de )",
      "description": "Detecta error_rationale de plantilla mecánica en phase1_variables y phase2_assumptions de unstructured_model (1,004 ocurrencias totales).",
      "evidence_items": [
        "Q-C01-109",
        "Q-C01-110",
        "Q-C01-115",
        "Q-Hab09-914"
      ]
    },
    {
      "rule_id": "FIB_TRANSCENDENTAL_NO_CALCULATOR",
      "severity": "warning",
      "regex_pattern": "\"allow_calculator\":\\s*false[\\s\\S]*?redondee a 4 decimales",
      "description": "Reactivos fill_in_the_blank con redondeo a 4 decimales que involucran exp/sqrt/ln y tienen allow_calculator: false.",
      "evidence_items": [
        "Q-Hab02-353",
        "Q-Hab09-923",
        "Q-Hab11-1013"
      ]
    },
    {
      "rule_id": "BLOOM_GOODHARTING_FACT_CONCEPT",
      "severity": "warning",
      "regex_pattern": "\"bloom_taxonomy_level\":\\s*\"(Evaluate|Create)\"",
      "description": "Etiquetado inflado (Evaluate/Create) en competencias Fact o Concept que evalúan reconocimiento estructural o perturbación paramétrica trivial.",
      "evidence_items": [
        "Q-PRE01-016",
        "Q-C01-115"
      ]
    }
  ],
  "remediation_actions": [
    "Habilitar allow_calculator: true en reactivos fill_in_the_blank con cálculos trascendentes/irracionales a 4 decimales (Q-Hab02-353, Q-Hab09-923, Q-Hab11-1013).",
    "Reemplazar los 1,004 error_rationale boilerplate en phase1_variables y phase2_assumptions de unstructured_model por diagnósticos específicos.",
    "Recalibrar etiquetas Bloom infladas en competencias Fact y Concept iniciales (Q-PRE01-016, Q-C01-115).",
    "Instanciar parámetros dinámicos en misconception_warning de los 19 reactivos afectados en Hab-07, Hab-09 y Hab-28."
  ]
}
```

</details>
