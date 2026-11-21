# Informe de Auditoría de Calidad Pedagógica, Psicométrica y Path-to-Mastery v2.0
## Curso: Solow M20 V1 (`solow_m20_v1`)

- **Fecha de Evaluación:** 2026-11-21
- **Evaluador:** Course QA Auditor — Top's Academy (Loop Semántico Adaptativo + Inspección Directa)
- **Estado en Plataforma:** ACTIVO (`courses/solow_m20_v1.json`)
- **Calificación Final Certificada:** **19.67 / 20.0 pts** (**19.7 / 20.0**)
- **Quality Tier:** **EXCELENTE (17.0 - 20.0 pts) — PLATINUM MASTERY**
- **Mastery Path Readiness Index (MPRI):** **98.2 / 100.0** (**GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo**)

> [!NOTE]
> **Nota metodológica sobre el payload transitorio:** El archivo `%TEMP%/tops_academy_qa/solow_m20_v1_payload.json` reportó `0` competencias y `0` reactivos debido a una colisión de lectura con la carpeta intermedia `courses/solow_m20_v1/` (aunque sí conservó `stage5_judge_audit`: 120/120 ítems juzgados con 100% de acuerdo). Por ello, esta auditoría se ejecutó mediante inspección directa de `courses/solow_m20_v1.json` (540 reactivos, 22 competencias), `courses/competence_analysis_solow_m20_v1.md` y contraste con `reports/audits_archive/solow_m20_v1/qa_report.md`.

---

### 1. Resumen Ejecutivo de Dimensiones

| Dimensión | Puntuación | Máximo | Calificación | Estado |
| :--- | :---: | :---: | :---: | :--- |
| **D1: Arquitectura Curricular, Topología DAG y ZPD** | **3.92** | 4.0 | 98.0% | ✨ Excelente |
| **D2: Calidad Psicométrica, Modalidad y Anti-Gaming** | **5.00** | 5.0 | 100.0% | ✅ Impecable |
| **D3: Andamiaje Socrático y Remediación Diagnóstica** | **5.00** | 5.0 | 100.0% | ✅ Impecable |
| **D4: Alineación Instruccional, Bloom y Pureza de Dominio** | **4.00** | 4.0 | 100.0% | ✅ Impecable |
| **D5: Accesibilidad, Ergonomía UI y Sintaxis KaTeX** | **1.75** | 2.0 | 87.5% | ✨ Excelente (con hallazgo menor en `open_symbolic`) |
| **Penalizaciones Duras** | **-0.00** | - | - | ✅ Sin penalizaciones |
| **TOTAL** | **19.67** | **20.0** | **98.4%** | 🏆 **EXCELENTE — PLATINUM MASTERY** |

---

### 2. Desglose Detallado y Verificación Semántica Adaptativa

#### D1. Arquitectura Curricular, Topología DAG y Calibración ZPD (`3.92 / 4.0 pts`)
- **Granularidad y Balance:** 22 micro-competencias atómicas (**1 Hechos `[H]`**, **11 Conceptos `[C]`**, **10 Habilidades `[Hab]`**) alineadas con el Cognitive Task Analysis (`competence_analysis_solow_m20_v1.md`), con **20 a 30 reactivos por competencia** (total: **540 reactivos**).
- **Topología DAG:** Grafo acíclico y conexo (1 componente conexo, **0 prerrequisitos invertidos** en orden topológico `idx(prereq) < idx(comp)`). Se mantiene una deducción mínima (`-0.08 pts`) por 1 par de competencias con solapamiento conceptual leve reportado en el motor determinista histórico.
- **Calibración ZPD Tri-Banda:** **22 / 22 competencias (100%)** cuentan con reactivos en las tres bandas de dificultad: `easy` (115), `medium` (206) y `hard` (219), habilitando plenamente `calibrateByMasteryDifficulty`.

#### D2. Calidad Psicométrica, Modalidad de Evocación y Anti-Gaming (`5.00 / 5.0 pts`)
- **Diversidad de Modalidades (0% reconocimiento pasivo `MC7`):**
  - `open_symbolic`: 100 (18.5%)
  - `adversarial_break`: 98 (18.1%)
  - `fill_in_the_blank`: 92 (17.0%)
  - `concept_matching`: 90 (16.7%)
  - `unstructured_model`: 60 (11.1%)
  - `proof_dag`: 46 (8.5%)
  - `invariant_canvas`: 40 (7.4%)
  - `multiple_select`: 14 (2.6%)
- **Calidad de Distractores y Anti-Gaming:** En los ítems de `multiple_select` (ej. `Q-C03-071`), cada distractor está vinculado explícitamente a un `distractor_id` del CTA (`D-C03-03`, `D-C03-01`) con `error_rationale` diagnóstico específico. En la verificación directa sobre los 14 ítems `multiple_select`, ninguno presentó sesgo de longitud >1.25x entre opciones correctas e incorrectas; no hay prefijos sintéticos, relleno `[R-15]` ni cuantificadores vacuos.

#### D3. Andamiaje Socrático Progresivo y Remediación Diagnóstica (`5.00 / 5.0 pts`)
- **Cobertura y Escalonamiento (3-Strikes Safeguard):** **540 / 540 reactivos (100%)** disponen de exactamente **3 pistas socráticas** progresivas instanciadas con los parámetros concretos del problema (conceptual $\to$ procedimental $\to$ operativa, sin regalar la clave).
- **Cero Boilerplate / Cero Envenenamiento:** 0% de pistas Mad-Libs genéricas y 0% de envenenamiento anti-socrático.
- **Remediación y Advertencias:** Tanto `detailed_solution` como `common_misconception_warning` están anclados en los modelos de error reales del CTA (ej. `Q-C01-001` refuerza el factor de escala $L$ en $Q=L\phi(k)$; `Q-Hab01-021` refuerza el signo negativo de la dilución laboral $-\lambda k$).

#### D4. Alineación Instruccional, Taxonomía de Bloom y Pureza de Dominio (`4.00 / 4.0 pts`)
- **Distribución Bloom Global:** `Remember` (26), `Understand` (45), `Apply` (154), `Analyze` (190), `Evaluate` (125).
- **Alineación en Habilidades `[Hab-01..10]`:** **300 / 300 reactivos (100%)** pertenecen a niveles superiores de Bloom (`Apply`: 110, `Analyze`: 115, `Evaluate`: 75), sin colapso declarativo en `Understand`.
- **Fidelidad Disciplinar y Arbitraje Ciego:** Registro económico-matemático auténtico del modelo de Solow-Swan, Harrod-Domar, Cobb-Douglas (linealización de Bernoulli), CES y trampa de liquidez. El arbitraje ciego de Stage 5 (`stage5_judge_audit`) reporta **120 / 120 ítems con acuerdo del 100%** (0 desacuerdos no reparados).

#### D5. Accesibilidad, Ergonomía Cognitiva en UI y Sintaxis KaTeX (`1.75 / 2.0 pts`)
- **Integridad KaTeX Estructural:** **0** delimitadores `$` desbalanceados, **0** bloques `$$$`, **0** residuos `{{...}}`, **0** flotantes con precisión excesiva (`\d+\.\d{5,}`) ni notación científica cruda en texto renderizado.
- **Hallazgo Ergonómico en `open_symbolic` (60 reactivos):** En reactivos como `Q-Hab01-031` (`Q-Hab01-031` a `Q-Hab01-040`, etc.), el campo `detailed_solution` interpola directamente la cadena SymPy destinada al evaluador dentro de delimitadores KaTeX: `$2.8*sqrt(k)-0.08*k$` en lugar de `$2.8\sqrt{k}-0.08k$`. Aunque no rompe el parser de KaTeX ni invalida la respuesta matemática, degrada la tipografía matemática en la tarjeta de solución paso a paso en 60/540 ítems (11.1%), motivando una deducción de **-0.25 pts** en D5 y una nueva regla candidata en `discovered_lint_rules`.

---

### 3. Muestras Estratificadas Verificadas

| ID | Competencia | Modalidad | Dificultad | Bloom | Hallazgo de Verificación Semántica |
| :--- | :--- | :--- | :---: | :---: | :--- |
| `Q-C01-001` | `C-01` | `concept_matching` | `easy` | `Remember` | Pistas y solución paso a paso exactas para $\phi(4)=5\sqrt{4}$ y $Q=L\phi(k)=30$; advertencia vinculada a `D-C01-03`. |
| `Q-C01-013` | `C-01` | `adversarial_break` | `medium` | `Analyze` | Falacia bien aislada en paso `S3` (omisión del denominador $L=15$ al despejar $Q$); pistas guían al paso sin revelar la letra. |
| `Q-Hab01-021` | `Hab-01` | `fill_in_the_blank` | `easy` | `Apply` | Contrato de redondeo explícito (`redondee a 4 decimales`), solución exacta ($\dot{k}=14.9$) y pistas escalonadas con los valores del ítem. |
| `Q-Hab01-031` | `Hab-01` | `open_symbolic` | `medium` | `Apply` | Stem y pistas limpios (`$s\cdot 7\sqrt{k}-\lambda k$`), pero `detailed_solution` renderiza sintaxis cruda SymPy `$2.8*sqrt(k)-0.08*k$`. |
| `Q-Hab01-041` | `Hab-01` | `proof_dag` | `medium` | `Analyze` | Secuencia causal `S1 -> S2 -> S3 -> S4` rigurosa (regla del producto en $K=kL$ $\to$ sustitución $\to$ división por $L>0$). |
| `Q-C02-051` | `C-02` | `invariant_canvas` | `easy` | `Analyze` | Geometría cartesiana consistente (`4*sqrt(x)` vs `2*x`, punto de equilibrio `E1=(4, 8)`). |
| `Q-C03-071` | `C-03` | `multiple_select` | `easy` | `Understand` | Distractores (`opt_a`, `opt_c`) con `error_rationale` específico a `D-C03-03` (filo de la navaja) y `D-C03-01` (estado estacionario). |
| `Q-Hab02-111` | `Hab-02` | `unstructured_model` | `medium` | `Analyze` | Clasificación de variables en linealización de Bernoulli ($\alpha=0.25\in(0,1)$, $z=k^{1-\alpha}$) y pistas socráticas precisas. |
| `Q-Hab10-530` | `Hab-10` | `proof_dag` | `hard` | `Evaluate` | Derivación rigurosa de subutilización por rigidez de tasa de interés sobre $r^*$ en trampa de liquidez. |

---

### 4. Índice de Preparación para el Dominio (`MPRI`: 98.2 / 100.0)

| Pilar Cognitivo | Puntaje | Máximo | Calificación |
| :--- | :---: | :---: | :--- |
| **1. Progresión Adaptativa ZPD y Bloom** | **20.00** | 20.0 | 100.0% |
| **2. Modalidad de Evocación y Anti-Gaming** | **20.00** | 20.0 | 100.0% |
| **3. Integridad Salvavidas Socrático (3-Strikes)** | **25.00** | 25.0 | 100.0% |
| **4. Alineación Diagnóstica en FeedbackToast** | **15.00** | 15.0 | 100.0% |
| **5. Topología DAG e Interleaving** | **9.65** | 10.0 | 96.5% |
| **6. Ergonomía Cognitiva y Sintaxis KaTeX** | **8.55** | 10.0 | 85.5% |
| **TOTAL MPRI** | **98.20** | **100.0** | **98.2% (GOLD MASTERY PATH)** |

---

### 5. Veredicto y Acciones de Mejora

El curso **`solow_m20_v1`** queda **CERTIFICADO** en nivel **EXCELENTE — PLATINUM MASTERY (`19.67 / 20.0`)** para estudio autónomo y dominio adaptativo en Top's Academy.

1. **Mejora menor recomendada (D5):** Formatear a LaTeX canónico (`\sqrt{k}`, multiplicación implícita o `\cdot`) la expresión simbólica dentro de `detailed_solution` en los 60 reactivos `open_symbolic` que actualmente muestran sintaxis SymPy (`*` y `sqrt(`) dentro de `$...$`.
2. **Corrección de infraestructura QA:** Revisar `prepare_course_payload.py` para evitar la colisión de lectura cuando existe una carpeta `courses/<course_id>/` junto al archivo `courses/<course_id>.json`.

---

<details>
<summary>Metadatos Estructurados (JSON)</summary>

```json
{
  "course_metadata": {
    "course_id": "solow_m20_v1",
    "unit_title": "Solow M20 V1",
    "detected_objective": "Dominio y aplicación analítica integral de Solow M20 V1",
    "total_competencies": 22,
    "total_questions": 540
  },
  "dimension_scores": {
    "architecture_granularity": {
      "score": 3.92,
      "max": 4.0,
      "feedback": "22 micro-competencias (1 Fact, 11 Concept, 10 Skill), DAG acíclico y conexo (0 prerrequisitos invertidos, 1 par solapado leve) y calibración ZPD tri-banda en 22/22 competencias."
    },
    "assessment_quality": {
      "score": 5.0,
      "max": 5.0,
      "feedback": "0% MC7; 100% evocación activa, discriminación condicional o modelado (open_symbolic=100, adversarial_break=98, fill_in_the_blank=92, concept_matching=90, unstructured_model=60, proof_dag=46, invariant_canvas=40, multiple_select=14). 0% sesgo de longitud en MS."
    },
    "scaffolding_hints": {
      "score": 5.0,
      "max": 5.0,
      "feedback": "540/540 reactivos con 3 pistas socráticas progresivas específicas al ítem; 0% Mad-Libs, 0% envenenamiento anti-socrático y error_rationale alineados al CTA."
    },
    "instructional_alignment": {
      "score": 4.0,
      "max": 4.0,
      "feedback": "300/300 reactivos en Skill en niveles superiores de Bloom (Apply=110, Analyze=115, Evaluate=75). Stage-5 Blind Judges con 120/120 acuerdos (100%)."
    },
    "technical_ergonomics": {
      "score": 1.75,
      "max": 2.0,
      "feedback": "0 errores críticos de delimitadores KaTeX ($ balanceados, cero $$$, cero {{...}}). Se detectan 60 reactivos open_symbolic con sintaxis cruda SymPy (*, sqrt()) en detailed_solution dentro de $...$."
    }
  },
  "penalties_applied": [],
  "raw_subtotal": 19.67,
  "final_score": 19.67,
  "quality_tier": "EXCELENTE (17-20)",
  "mastery_path_readiness": {
    "mpri_score": 98.2,
    "mpri_max": 100.0,
    "mpri_tier": "GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo",
    "pillars": {
      "zpd_adaptive_progression": { "score": 20.0, "max": 20.0 },
      "retrieval_modality_and_anti_gaming": { "score": 20.0, "max": 20.0 },
      "socratic_scaffolding_lifeline": { "score": 25.0, "max": 25.0 },
      "diagnostic_remediation_alignment": { "score": 15.0, "max": 15.0 },
      "dag_and_interleaving_topology": { "score": 9.65, "max": 10.0 },
      "cognitive_ergonomics_and_framing": { "score": 8.55, "max": 10.0 }
    },
    "student_journey_verdict": "Ruta óptima hacia el dominio: progresión ZPD tri-banda completa, 100% evocación activa/discriminación y salvavidas socrático de 3 pistas sin fugas."
  },
  "discovered_lint_rules": [
    {
      "rule_id": "sympy_syntax_leaked_in_katex_solution",
      "severity": "warning",
      "regex_pattern": "\\$[^$]*(?:\\d\\s*\\*\\s*[a-zA-Z(]|\\bsqrt\\()[^$]*\\$",
      "description": "Expresión SymPy/Python cruda (* o sqrt() sin backslash) interpolada dentro de delimitadores KaTeX en detailed_solution (afecta a ítems open_symbolic).",
      "evidence_items": ["Q-Hab01-031", "Q-Hab01-032", "Q-Hab01-033"]
    }
  ],
  "remediation_actions": [
    "Convertir a LaTeX canónico (\\sqrt{...}, multiplicación implícita o \\cdot) las expresiones en detailed_solution de los 60 reactivos open_symbolic afectados.",
    "Corregir la resolución de rutas en prepare_course_payload.py cuando coexisten courses/<course_id>/ y courses/<course_id>.json."
  ]
}
```

</details>
