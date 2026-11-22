# Informe de Auditoría de Calidad Pedagógica y Psicométrica (QM-OSCQR)
## Curso: Solow M20 V5 (`solow_m20_v5`)

- **Fecha de Evaluación:** 2026-11-21
- **Evaluador:** Course QA Evaluator — Top's Academy (Modo Híbrido: Motor Determinista + Loop de Verificación Semántica Adaptativa)
- **Estado en Plataforma:** ACTIVO
- **Calificación Final Certificada:** **19.92 / 20.0 pts**
- **Quality Tier:** **EXCELENTE (19.0 - 20.0 pts) — PLATINUM MASTERY**
- **Mastery Path Readiness Index (MPRI):** **99.65 / 100.0** (`GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo`)
- **Índice Bloom Ponderado (1–5):** **3.881 / 5.0** (piso adaptativo **3.83** | `Apply+`: **94.47%** | `Analyze+Evaluate`: **69.35%** | Tier: **ÉLITE** | incoherencias: **0**)
- **Arbitraje Ciego Stage-5:** **120 / 120** reactivos auditados con **100.0% de acuerdo** (`0` desacuerdos sin reparar)

---

### 1. Resumen Ejecutivo de Dimensiones

| Dimensión | Puntuación | Máximo | Calificación | Estado |
| :--- | :---: | :---: | :---: | :---: |
| **D1: Arquitectura Curricular, DAG y Calibración ZPD** | **3.92** | 4.00 | 98.0% | ✨ Excelente |
| **D2: Calidad Psicométrica, Evocación y Anti-Gaming** | **5.00** | 5.00 | 100.0% | ✅ Impecable |
| **D3: Andamiaje Socrático y Remediación Diagnóstica** | **5.00** | 5.00 | 100.0% | ✅ Impecable |
| **D4: Alineación Instruccional, Bloom y Pureza de Dominio** | **4.00** | 4.00 | 100.0% | ✅ Impecable |
| **D5: Ergonomía Técnica y Sintaxis KaTeX** | **2.00** | 2.00 | 100.0% | ✅ Impecable |
| **Penalizaciones Duras** | **-0.00** | - | - | ✅ Sin penalizaciones |
| **TOTAL** | **19.92** | **20.00** | **99.6%** | 🏆 **PLATINUM MASTERY** |

---

### 2. Desglose Detallado por Dimensión

#### D1. Arquitectura Curricular, Topología DAG y Calibración ZPD (3.92 / 4.00 pts)
- **Estructura Curricular:** 19 competencias balanceadas (`2` Hechos `[H-01, H-02]`, `9` Conceptos `[C-01..C-09]`, `8` Habilidades `[Hab-01, Hab-02, Hab-04..Hab-09]`) con `597` reactivos (`27` a `48` por competencia; `0` competencias subpobladas y `0` preguntas huérfanas).
- **Topología DAG:** Grafo acíclico (`has_cycle=False`), conexo (`connected_components_count=1`, profundidad máxima `4`), sin aristas invertidas ni prerrequisitos colgantes.
- **Calibración ZPD:** `19/19` competencias cuentan con calibración tri-banda (`easy: 151`, `medium: 199`, `hard: 247`), activando `calibrateByMasteryDifficulty` en todo el trayecto hacia *Mastered*.
- **Observación única (`-0.08` pts):** `architecture_dag_linter` reportó 1 par con solapamiento curricular (`Hab-02` *"Solución Cuantitativa Cobb-Douglas"* vs. `Hab-05` *"Solución Explícita Cobb-Douglas"*). La verificación semántica confirma que abordan derivaciones distintas de la literatura fuente (cambio de variable de Bernoulli $z=k^{1-\alpha}$ en forma intensiva vs. integración directa de $\dot{K}=sK^a(L_0 e^{nt})^{1-a}$ en Solow 1956), aunque convergen a fórmulas de estado estacionario isomorfas ($\bar{k}=(s/\lambda)^{1/(1-\alpha)}$ y $r^*=(s/n)^{1/(1-a)}$).

#### D2. Calidad Psicométrica, Evocación y Anti-Gaming (5.00 / 5.00 pts)
- **Diversidad de Modalidades (100% evocación activa o discriminación):**
  - `MC7`: **0.0%** (`0` reactivos de reconocimiento pasivo).
  - `fill_in_the_blank`: **15.08%** (`90`), `multiple_select`: **17.09%** (`102`), y modalidades de Bloom Superior (`67.84%`, `405` reactivos): `adversarial_break` (`129`), `open_symbolic` (`96`), `unstructured_model` (`87`), `invariant_canvas` (`45`), `proof_dag` (`30`), `concept_matching` (`18`).
- **Integridad de Distractores y Anti-Gaming:** `210` distractores evaluados con **100.0%** de cobertura de `error_rationale`, `0` distractores imposibles por dominio, `0` multiplicadores mágicos, `0` claves memorizables, `0` sesgos de longitud en `MS` y `>= 26` esqueletos distintos por competencia.

#### D3. Andamiaje Socrático y Remediación Diagnóstica (5.00 / 5.00 pts)
- **Pistas Socráticas (3-Strikes Safeguard):** El **100.0%** de los `597` reactivos dispone de 3 a 5 pistas escalonadas específicas a los parámetros del ítem (`0.0%` boilerplate Mad-Libs, `0.0%` envenenamiento anti-socrático, `0` fugas de clave).
- **Remediación Diagnóstica (`FeedbackToast`):** `100.0%` de unicidad de `error_rationale` por slot (`0` rationales numéricos desconectados, `0` advertencias clonadas o mudas y `0` soluciones faltantes).

#### D4. Alineación Instruccional, Bloom y Pureza de Dominio (4.00 / 4.00 pts)
- **Rigor de Bloom:** `100.0%` de las habilidades prácticas (`300/300`) están en `Apply+`. Distribución global: `Understand` (`33`), `Apply` (`150`), `Analyze` (`269`), `Evaluate` (`145`).
- **Índice Bloom Ponderado:** **3.881 / 5.0**, superando el piso adaptativo (**3.83**, brecha `0.0`), con **69.35%** en `Analyze + Evaluate` (Tier **ÉLITE**) y `0` violaciones de coherencia `modalidad × bloom`.
- **Pureza de Dominio:** `0` prefijos de dominios ajenos y `0` cuantificadores vacuos.

#### D5. Ergonomía Técnica y Sintaxis KaTeX (2.00 / 2.00 pts)
- **Sintaxis KaTeX:** `0` delimitadores `$` desbalanceados, `0` llaves sin cerrar, `0` triples `$$$`, `0` residuos de SymPy/f-strings.
- **Ergonomía UI:** `0` bloques de prosa en `\text{...}`, `0` identificadores crudos de Python, `0` colisiones por concatenación y `0` identidades tautológicas.

---

### 3. Loop de Verificación Semántica Adaptativa

Dado que `risk_clusters` presentó `0` alertas en reactivos individuales y únicamente 1 advertencia estructural (`comp_Hab-05`), se ejecutó la verificación semántica sobre muestras estratificadas de las 19 competencias y todas las modalidades activas:

1. **Verificación Matemática y Económica (Solow 1956 & Ecuación de Bernoulli):**
   - **`fill_in_the_blank` (`Q-H01-001/002`, `Q-Hab01-055/056`, `Q-Hab02-157/158`, `Q-Hab05-256/257`, `Q-Hab07-409/410`, `Q-Hab08-472/473`, `Q-Hab09-535/536`):** Cálculos exactos (p. ej. $\dot{k}=0.29(14)-0.09(9)=3.25$; $r_K = 0.01 + 0.016/0.65 = 0.0346$; $s_{\text{eff}} = 0.16+(0.61-0.16)(0.3)=0.2950$; $\dot{L}/L = 0.12(3.53)/3 = 0.1412$). Cada distractor numérico corresponde exactamente al error algebraico descrito en su `error_rationale` (omisión de dilución $-\lambda k$, inversión de razón $\lambda/s$, omisión de inversión pública $vt$, etc.).
   - **`open_symbolic` (`Q-Hab04-220/221`, `Q-Hab06-292/293`):** Expresiones simbólicas canónicas y equivalentes aceptados verificados (`0.042*r`, `0.11*(5*sqrt(r)+1)**2-0.16*r`), con `symbolic_config` coherente.
   - **`invariant_canvas` (`Q-C01-103/104`, `Q-C02-130/131`, `Q-C04-193/194`, `Q-C06-382/383`, `Q-C08-508/509`):** Coordenadas objetivo exactas sobre las curvas cartesianas (p. ej. $(81, 3.24)$ en $\dot{k}=0.36\sqrt{k}-0.04k$; trampa de pobreza estable $r_1=4, y=1.0$ en $0.5\sqrt{r}-n(r)r=0.005(r-4)(r-16)$).
   - **`adversarial_break` y `proof_dag` (`Q-C03-028/029`, `Q-C07-445/446`, `Q-C09-571/572`):** Falacias rigurosas sin ambigüedad (p. ej., distinción entre capital en uso $K(t)$ fijado por preferencia por la liquidez $\bar{M}=Q(Y,q/p)$ frente al stock físico acumulado $K_s$, e invarianza de la raíz $r^*$ ante el factor positivo $(1+ah/r)^{-1}$ bajo oferta laboral elástica).
2. **Validación de Solapamiento `Hab-02` ↔ `Hab-05`:**
   - Diferenciación pedagógica real en las derivaciones (ecuación intensiva de Bernoulli vs. integración de $K(t)$), aunque con convergencia en el cálculo de estado uniforme. Se mantiene la deducción menor de `-0.08` pts en D1.
3. **Nuevos Patrones de Error (`discovered_lint_rules`):**
   - Ninguno detectado (`[]`).

---

### 4. Índice de Preparación para el Dominio (MPRI: 99.65 / 100.0)

| Pilar Cognitivo | Puntaje | Máximo | Calificación |
| :--- | :---: | :---: | :---: |
| **1. Progresión Adaptativa ZPD y Bloom** | **20.00** | 20.0 | 100.0% |
| **2. Modalidad de Evocación y Anti-Gaming** | **20.00** | 20.0 | 100.0% |
| **3. Integridad Salvavidas Socrático (3-Strikes)** | **25.00** | 25.0 | 100.0% |
| **4. Alineación Diagnóstica en FeedbackToast** | **15.00** | 15.0 | 100.0% |
| **5. Topología DAG e Interleaving** | **9.65** | 10.0 | 96.5% |
| **6. Ergonomía Cognitiva y Sintaxis KaTeX** | **10.00** | 10.0 | 100.0% |
| **TOTAL MPRI** | **99.65** | **100.0** | **99.7% (`GOLD MASTERY PATH`)** |

---

### 5. Veredicto y Certificación

El curso **Solow M20 V5** (`solow_m20_v5`) queda **certificado para producción inmediata** con calificación de **19.92 / 20.0 pts** (`PLATINUM MASTERY`) y **MPRI de 99.65 / 100.0** (`GOLD MASTERY PATH`), cumpliendo íntegramente los estándares Quality Matters, OSCQR y Mastery Learning v2.0.

---

<details>
<summary>Metadatos Estructurados (JSON)</summary>

```json
{
  "course_metadata": {
    "course_id": "solow_m20_v5",
    "unit_title": "Solow M20 V5",
    "detected_objective": "Dominio y aplicación analítica integral de Solow M20 V5",
    "total_competencies": 19,
    "total_questions": 597,
    "question_types_distribution": {
      "fill_in_the_blank": 90,
      "multiple_select": 102,
      "concept_matching": 18,
      "adversarial_break": 129,
      "unstructured_model": 87,
      "open_symbolic": 96,
      "proof_dag": 30,
      "invariant_canvas": 45
    },
    "bloom_index": {
      "weighted_index": 3.881,
      "adaptive_floor": 3.83,
      "gap": 0.0,
      "apply_plus_pct": 94.47,
      "superior_pct": 69.35,
      "tier": "ÉLITE",
      "coherence_violations_count": 0
    },
    "stage5_judge_audit": {
      "total_items_judged": 120,
      "agreed_items": 120,
      "agreement_rate": 1.0,
      "unrepaired_disagreements_count": 0
    },
    "platform_status": "ACTIVO",
    "evaluator": "Course QA Evaluator — Hybrid (Deterministic Engine + Adaptive Semantic Loop)",
    "evaluation_date": "2026-11-21"
  },
  "dimension_scores": {
    "architecture_granularity": {
      "score": 3.92,
      "max": 4.0,
      "feedback": "Estructura curricular con 19 competencias (2 Hechos, 9 Conceptos, 8 Habilidades). DAG acíclico y conexo (ciclos=False, comp. conexos=1, pares solapados=1: Hab-02<->Hab-05 con derivaciones distintas pero estado estacionario isomorfo). ZPD: 19/19 competencias con calibración tri-banda ('easy', 'medium', 'hard')."
    },
    "assessment_quality": {
      "score": 5.0,
      "max": 5.0,
      "feedback": "Modalidad: MC7=0.0%, FIB=15.08%, MS=17.09%, BloomSup=67.84% (100.0% evocación activa/discriminación). Distractores: 210 evaluados con 100.0% cobertura de error_rationale (imposibles por dominio=0, claves corruptas=0, sesgo MS=0.0%). Verificación semántica confirma exactitud matemática."
    },
    "scaffolding_hints": {
      "score": 5.0,
      "max": 5.0,
      "feedback": "Andamiaje formativo: 100.0% de reactivos con 3 a 5 pistas socráticas escalonadas (100.0% pistas genuinas, 0.0% boilerplate Mad-Libs, 0.0% envenenadas). Unicidad diagnóstica real de rationales: 100.0% (rationales numéricos desconectados=0, advertencias clonadas/mudas=0)."
    },
    "instructional_alignment": {
      "score": 4.0,
      "max": 4.0,
      "feedback": "Alineación cognitiva de Bloom: 100.0% de habilidades prácticas en Apply+; Índice Bloom ponderado: 3.881/5.0 (piso adaptativo 3.83, 69.35% Analyze+Evaluate, tier: ÉLITE, incoherencias=0). Stage-5 Blind Judges: 120/120 acuerdo."
    },
    "technical_ergonomics": {
      "score": 2.0,
      "max": 2.0,
      "feedback": "Sintaxis KaTeX: 0 errores críticos (delimitadores balanceados, llaves cerradas, cero $$$). Ergonomía: 0 observaciones de prosa en \\text{...}, 0 identificadores crudos, 0 colisiones por concatenación, 0 identidades tautológicas y 0 formatos flotantes/asteriscos crudos."
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
      "zpd_adaptive_progression": {
        "score": 20.0,
        "max": 20.0
      },
      "retrieval_modality_and_anti_gaming": {
        "score": 20.0,
        "max": 20.0
      },
      "socratic_scaffolding_lifeline": {
        "score": 25.0,
        "max": 25.0
      },
      "diagnostic_remediation_alignment": {
        "score": 15.0,
        "max": 15.0
      },
      "dag_and_interleaving_topology": {
        "score": 9.65,
        "max": 10.0
      },
      "cognitive_ergonomics_and_framing": {
        "score": 10.0,
        "max": 10.0
      }
    },
    "student_journey_verdict": "Trayectoria de dominio lista para despliegue autónomo: 100% evocación activa, calibración tri-banda en 19/19 competencias y andamiaje socrático íntegro en el sistema de 3 intentos."
  },
  "discovered_lint_rules": [],
  "remediation_actions": [
    "Certificación plena para despliegue en plataforma Top's Academy con Nivel EXCELENTE (19.0 - 20.0 pts) — PLATINUM MASTERY.",
    "Opcional (mejora cosmética): distinguir explícitamente en los enunciados de estado uniforme de Hab-02 vs Hab-05 el método de derivación (Bernoulli en forma intensiva vs integración directa de K(t)) para reducir el solapamiento léxico."
  ],
  "platform_status": "ACTIVO"
}
```

</details>
