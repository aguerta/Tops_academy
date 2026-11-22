# Informe de Auditoría de Calidad Pedagógica y Psicométrica (QM-OSCQR)
## Curso: Mathematical Statistics (`stats_math`)

- **Fecha de Evaluación:** 2026-11-21
- **Evaluador:** Course QA Evaluator — Top's Academy (Modo Determinista)
- **Estado en Plataforma:** RECHAZADO
- **Calificación Final Certificada:** **11.4 / 20.0 pts**
- **Quality Tier:** **DEFICIENTE (11.0 - 13.9 pts)**
- **Mastery Path Readiness Index (MPRI):** **70.40 / 100.0** (PARTIAL MASTERY PATH (65-84): Funcional con Brechas ZPD/Modalidad)
- **Índice Bloom Ponderado (1–5):** **0.00 / 5.0** (piso adaptativo 3.85 | Analyze+Evaluate: 100.0% | Tier: **N/A**)

---

### 1. Resumen Ejecutivo de Dimensiones

| Dimensión | Puntuación | Máximo | Calificación | Estado |
| :--- | :---: | :---: | :---: | :---: |
| **D1: Arquitectura Curricular y Granularidad** | **3.0** | 4.0 | 75% | ⚠️ Observación menor |
| **D2: Calidad Psicométrica y Reactivos** | **5.0** | 5.0 | 100% | ✅ Impecable |
| **D3: Andamiaje y Pistas Socráticas** | **4.0** | 5.0 | 80% | ⚠️ Observación menor |
| **D4: Alineación Instruccional y ZPD** | **2.4** | 4.0 | 60% | ❌ Deficiente |
| **D5: Ergonomía Técnica y KaTeX** | **2.0** | 2.0 | 100% | ✅ Impecable |
| **Penalizaciones Duras** | **-5.0** | - | - | ⚠️ Penalizaciones aplicadas |
| **TOTAL** | **11.4** | **20.0** | **57.0%** | 🏆 **DEFICIENTE (11.0 - 13.9 pts)** |

---

### 2. Desglose Detallado por Dimensión

#### D1. Arquitectura Curricular y Granularidad (3.0 / 4.0 pts)
- Estructura curricular con 2 competencias (0 Hechos, 1 Conceptos, 1 Habilidades). DAG acíclico y conexo (ciclos=False, comp. conexos=1, pares solapados=0). ZPD: 0/2 competencias con calibración tri-banda ('easy', 'medium', 'hard').

#### D2. Calidad Psicométrica y Reactivos (5.0 / 5.0 pts)
- Modalidad: MC7=0.0%, FIB=0.0%, MS=0.0% (0.0% evocación activa/discriminación). Distractores: 0 evaluados con 100.0% cobertura de error_rationale (imposibles por dominio=0, claves corruptas=0, sesgo MS=0.0%).

#### D3. Andamiaje y Pistas Socráticas (4.0 / 5.0 pts)
- Andamiaje formativo: 0.0% de reactivos con 3 a 5 pistas socráticas escalonadas (100.0% pistas genuinas, 0.0% boilerplate Mad-Libs, 0.0% envenenadas). Unicidad diagnóstica real de rationales: 100.0% (rationales numéricos desconectados=0, advertencias clonadas/mudas=0).

#### D4. Alineación Instruccional y ZPD (2.4 / 4.0 pts)
- Alineación cognitiva de Bloom: 0.0% de habilidades prácticas en Apply+; Índice Bloom ponderado: 0.00/5.0 (piso adaptativo 3.85, 100.0% Analyze+Evaluate, tier: N/A, incoherencias=0).

#### D5. Ergonomía Técnica y KaTeX (2.0 / 2.0 pts)
- Sintaxis KaTeX: 0 errores críticos (delimitadores balanceados, llaves cerradas, cero $$$). Ergonomía: 0 observaciones de prosa en \text{...}, 0 identificadores crudos, 0 colisiones por concatenación, 0 identidades tautológicas, 0 formatos flotantes/asteriscos crudos y 0 residuos de plantilla/reemplazo (template_vars=0, blind_repl=0).

---

### 3. Índice de Preparación para el Dominio (MPRI: 100.0 pts)

| Pilar Cognitivo | Puntaje | Máximo | Calificación |
| :--- | :---: | :---: | :---: |
| **1. Progresión Adaptativa ZPD y Bloom** | **16.00** | 20.0 | 80.0% |
| **2. Modalidad de Evocación y Anti-Gaming** | **20.00** | 20.0 | 100.0% |
| **3. Integridad Salvavidas Socrático (3-Strikes)** | **0.00** | 25.0 | 0.0% |
| **4. Alineación Diagnóstica en FeedbackToast** | **15.00** | 15.0 | 100.0% |
| **5. Topología DAG e Interleaving** | **9.40** | 10.0 | 94.0% |
| **6. Ergonomía Cognitiva y Sintaxis KaTeX** | **10.00** | 10.0 | 100.0% |
| **TOTAL MPRI** | **70.40** | **100.0** | **70.4% (PARTIAL MASTERY PATH (65-84): Funcional con Brechas ZPD/Modalidad)** |

---

### 4. Veredicto y Certificación

El curso **Mathematical Statistics** ha sido **RECHAZADO** para despliegue en plataforma con calificación de **11.4 / 20.0** y MPRI de **70.40 / 100.0**. Debe corregir las brechas críticas y penalizaciones bloqueantes antes de reevaluar.

---

<details>
<summary>Metadatos Estructurados (JSON)</summary>

```json
{
  "course_metadata": {
    "course_id": "stats_math",
    "unit_title": "Mathematical Statistics",
    "detected_objective": "",
    "total_competencies": 2,
    "total_questions": 3,
    "question_types_distribution": {
      "unknown": 3
    },
    "bloom_index": {
      "weighted_index": 0.0,
      "adaptive_floor": 3.85,
      "gap": 0.0,
      "apply_plus_pct": 100.0,
      "superior_pct": 100.0,
      "tier": "N/A",
      "coherence_violations_count": 0
    },
    "platform_status": "RECHAZADO",
    "evaluator": "Course QA Evaluator — Standardized Deterministic Engine",
    "evaluation_date": "2026-11-21"
  },
  "dimension_scores": {
    "architecture_granularity": {
      "score": 3.0,
      "max": 4.0,
      "feedback": "Estructura curricular con 2 competencias (0 Hechos, 1 Conceptos, 1 Habilidades). DAG acíclico y conexo (ciclos=False, comp. conexos=1, pares solapados=0). ZPD: 0/2 competencias con calibración tri-banda ('easy', 'medium', 'hard')."
    },
    "assessment_quality": {
      "score": 5.0,
      "max": 5.0,
      "feedback": "Modalidad: MC7=0.0%, FIB=0.0%, MS=0.0% (0.0% evocación activa/discriminación). Distractores: 0 evaluados con 100.0% cobertura de error_rationale (imposibles por dominio=0, claves corruptas=0, sesgo MS=0.0%)."
    },
    "scaffolding_hints": {
      "score": 4.0,
      "max": 5.0,
      "feedback": "Andamiaje formativo: 0.0% de reactivos con 3 a 5 pistas socráticas escalonadas (100.0% pistas genuinas, 0.0% boilerplate Mad-Libs, 0.0% envenenadas). Unicidad diagnóstica real de rationales: 100.0% (rationales numéricos desconectados=0, advertencias clonadas/mudas=0)."
    },
    "instructional_alignment": {
      "score": 2.4,
      "max": 4.0,
      "feedback": "Alineación cognitiva de Bloom: 0.0% de habilidades prácticas en Apply+; Índice Bloom ponderado: 0.00/5.0 (piso adaptativo 3.85, 100.0% Analyze+Evaluate, tier: N/A, incoherencias=0)."
    },
    "technical_ergonomics": {
      "score": 2.0,
      "max": 2.0,
      "feedback": "Sintaxis KaTeX: 0 errores críticos (delimitadores balanceados, llaves cerradas, cero $$$). Ergonomía: 0 observaciones de prosa en \\text{...}, 0 identificadores crudos, 0 colisiones por concatenación, 0 identidades tautológicas, 0 formatos flotantes/asteriscos crudos y 0 residuos de plantilla/reemplazo (template_vars=0, blind_repl=0)."
    }
  },
  "penalties_applied": [
    {
      "rule": "bank_lt_3_exercises",
      "deduction": 2.0,
      "reason": "2 competencia(s) tienen menos de 3 ejercicios prácticos."
    },
    {
      "rule": "hints_zero",
      "deduction": 3.0,
      "reason": "3 reactivo(s) carecen por completo de pistas progresivas (hints = 0)."
    }
  ],
  "raw_subtotal": 16.4,
  "final_score": 11.4,
  "quality_tier": "DEFICIENTE (11.0 - 13.9 pts)",
  "mastery_path_readiness": {
    "mpri_score": 70.4,
    "mpri_max": 100.0,
    "mpri_tier": "PARTIAL MASTERY PATH (65-84): Funcional con Brechas ZPD/Modalidad",
    "pillars": {
      "zpd_adaptive_progression": {
        "score": 16.0,
        "max": 20.0
      },
      "retrieval_modality_and_anti_gaming": {
        "score": 20.0,
        "max": 20.0
      },
      "socratic_scaffolding_lifeline": {
        "score": 0.0,
        "max": 25.0
      },
      "diagnostic_remediation_alignment": {
        "score": 15.0,
        "max": 15.0
      },
      "dag_and_interleaving_topology": {
        "score": 9.4,
        "max": 10.0
      },
      "cognitive_ergonomics_and_framing": {
        "score": 10.0,
        "max": 10.0
      }
    }
  },
  "remediation_actions": [
    "Resolver penalización dura [bank_lt_3_exercises]: 2 competencia(s) tienen menos de 3 ejercicios prácticos.",
    "Resolver penalización dura [hints_zero]: 3 reactivo(s) carecen por completo de pistas progresivas (hints = 0).",
    "Elevar calificación global (11.4/20.0 < 14.0 mínimo requerido) atendiendo dimensiones deficitarias."
  ],
  "discovered_lint_rules": [],
  "platform_status": "RECHAZADO"
}
```

</details>