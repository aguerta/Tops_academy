# Informe de Auditoría de Calidad Pedagógica y Psicométrica (QM-OSCQR)
## Curso: Modelo de Solow (`solow_model`)

- **Fecha de Evaluación:** 2026-11-21
- **Evaluador:** Course QA Evaluator — Top's Academy (Modo Determinista)
- **Estado en Plataforma:** RECHAZADO
- **Calificación Final Certificada:** **10.8 / 20.0 pts**
- **Quality Tier:** **CRÍTICO (0.0 - 10.9 pts)**
- **Mastery Path Readiness Index (MPRI):** **71.10 / 100.0** (PARTIAL MASTERY PATH (65-84): Funcional con Brechas ZPD/Modalidad)
- **Índice Bloom Ponderado (1–5):** **2.07 / 5.0** (piso adaptativo 3.70 | Analyze+Evaluate: 3.6% | Tier: **BAJO**)

---

### 1. Resumen Ejecutivo de Dimensiones

| Dimensión | Puntuación | Máximo | Calificación | Estado |
| :--- | :---: | :---: | :---: | :---: |
| **D1: Arquitectura Curricular y Granularidad** | **0.0** | 4.0 | 0% | ❌ Deficiente |
| **D2: Calidad Psicométrica y Reactivos** | **3.8** | 5.0 | 76% | ⚠️ Observación menor |
| **D3: Andamiaje y Pistas Socráticas** | **3.9** | 5.0 | 77% | ⚠️ Observación menor |
| **D4: Alineación Instruccional y ZPD** | **3.2** | 4.0 | 80% | ⚠️ Observación menor |
| **D5: Ergonomía Técnica y KaTeX** | **2.0** | 2.0 | 100% | ✅ Impecable |
| **Penalizaciones Duras** | **-2.0** | - | - | ⚠️ Penalizaciones aplicadas |
| **TOTAL** | **10.8** | **20.0** | **54.2%** | 🏆 **CRÍTICO (0.0 - 10.9 pts)** |

---

### 2. Desglose Detallado por Dimensión

#### D1. Arquitectura Curricular y Granularidad (0.0 / 4.0 pts)
- Estructura curricular con 10 competencias (2 Hechos, 6 Conceptos, 2 Habilidades). DAG acíclico y conexo (ciclos=False, comp. conexos=10, pares solapados=0). ZPD: 0/10 competencias con calibración tri-banda ('easy', 'medium', 'hard').

#### D2. Calidad Psicométrica y Reactivos (3.8 / 5.0 pts)
- Modalidad: MC7=100.0%, FIB=0.0%, MS=0.0% (0.0% evocación activa/discriminación). Distractores: 84 evaluados con 100.0% cobertura de error_rationale (imposibles por dominio=0, claves corruptas=0, sesgo MS=0.0%).

#### D3. Andamiaje y Pistas Socráticas (3.9 / 5.0 pts)
- Andamiaje formativo: 100.0% de reactivos con 3 a 5 pistas socráticas escalonadas (100.0% pistas genuinas, 0.0% boilerplate Mad-Libs, 0.0% envenenadas). Unicidad diagnóstica real de rationales: 3.33% (rationales numéricos desconectados=0, advertencias clonadas/mudas=0).

#### D4. Alineación Instruccional y ZPD (3.2 / 4.0 pts)
- Alineación cognitiva de Bloom: 100.0% de habilidades prácticas en Apply+; Índice Bloom ponderado: 2.07/5.0 (piso adaptativo 3.70, 3.6% Analyze+Evaluate, tier: BAJO, incoherencias=0).

#### D5. Ergonomía Técnica y KaTeX (2.0 / 2.0 pts)
- Sintaxis KaTeX: 0 errores críticos (delimitadores balanceados, llaves cerradas, cero $$$). Ergonomía: 0 observaciones de prosa en \text{...}, 0 identificadores crudos, 0 colisiones por concatenación, 0 identidades tautológicas y 0 formatos flotantes/asteriscos crudos.

---

### 3. Índice de Preparación para el Dominio (MPRI: 100.0 pts)

| Pilar Cognitivo | Puntaje | Máximo | Calificación |
| :--- | :---: | :---: | :---: |
| **1. Progresión Adaptativa ZPD y Bloom** | **16.00** | 20.0 | 80.0% |
| **2. Modalidad de Evocación y Anti-Gaming** | **10.00** | 20.0 | 50.0% |
| **3. Integridad Salvavidas Socrático (3-Strikes)** | **25.00** | 25.0 | 100.0% |
| **4. Alineación Diagnóstica en FeedbackToast** | **10.10** | 15.0 | 67.3% |
| **5. Topología DAG e Interleaving** | **0.00** | 10.0 | 0.0% |
| **6. Ergonomía Cognitiva y Sintaxis KaTeX** | **10.00** | 10.0 | 100.0% |
| **TOTAL MPRI** | **71.10** | **100.0** | **71.1% (PARTIAL MASTERY PATH (65-84): Funcional con Brechas ZPD/Modalidad)** |

---

### 4. Veredicto y Certificación

El curso **Modelo de Solow** ha sido **RECHAZADO** para despliegue en plataforma con calificación de **10.8 / 20.0** y MPRI de **71.10 / 100.0**. Debe corregir las brechas críticas y penalizaciones bloqueantes antes de reevaluar.

---

<details>
<summary>Metadatos Estructurados (JSON)</summary>

```json
{
  "course_metadata": {
    "course_id": "solow_model",
    "unit_title": "Modelo de Solow",
    "detected_objective": "Curso completo de Modelo de Solow con validación psicométrica estricta.",
    "total_competencies": 10,
    "total_questions": 28,
    "question_types_distribution": {
      "multiple_choice_7_options": 28
    },
    "bloom_index": {
      "weighted_index": 2.071,
      "adaptive_floor": 3.696,
      "gap": 1.625,
      "apply_plus_pct": 25.0,
      "superior_pct": 3.57,
      "tier": "BAJO",
      "coherence_violations_count": 0
    },
    "platform_status": "RECHAZADO",
    "evaluator": "Course QA Evaluator — Standardized Deterministic Engine",
    "evaluation_date": "2026-11-21"
  },
  "dimension_scores": {
    "architecture_granularity": {
      "score": 0.0,
      "max": 4.0,
      "feedback": "Estructura curricular con 10 competencias (2 Hechos, 6 Conceptos, 2 Habilidades). DAG acíclico y conexo (ciclos=False, comp. conexos=10, pares solapados=0). ZPD: 0/10 competencias con calibración tri-banda ('easy', 'medium', 'hard')."
    },
    "assessment_quality": {
      "score": 3.8,
      "max": 5.0,
      "feedback": "Modalidad: MC7=100.0%, FIB=0.0%, MS=0.0% (0.0% evocación activa/discriminación). Distractores: 84 evaluados con 100.0% cobertura de error_rationale (imposibles por dominio=0, claves corruptas=0, sesgo MS=0.0%)."
    },
    "scaffolding_hints": {
      "score": 3.85,
      "max": 5.0,
      "feedback": "Andamiaje formativo: 100.0% de reactivos con 3 a 5 pistas socráticas escalonadas (100.0% pistas genuinas, 0.0% boilerplate Mad-Libs, 0.0% envenenadas). Unicidad diagnóstica real de rationales: 3.33% (rationales numéricos desconectados=0, advertencias clonadas/mudas=0)."
    },
    "instructional_alignment": {
      "score": 3.2,
      "max": 4.0,
      "feedback": "Alineación cognitiva de Bloom: 100.0% de habilidades prácticas en Apply+; Índice Bloom ponderado: 2.07/5.0 (piso adaptativo 3.70, 3.6% Analyze+Evaluate, tier: BAJO, incoherencias=0)."
    },
    "technical_ergonomics": {
      "score": 2.0,
      "max": 2.0,
      "feedback": "Sintaxis KaTeX: 0 errores críticos (delimitadores balanceados, llaves cerradas, cero $$$). Ergonomía: 0 observaciones de prosa en \\text{...}, 0 identificadores crudos, 0 colisiones por concatenación, 0 identidades tautológicas y 0 formatos flotantes/asteriscos crudos."
    }
  },
  "penalties_applied": [
    {
      "rule": "bank_lt_3_exercises",
      "deduction": 2.0,
      "reason": "1 competencia(s) tienen menos de 3 ejercicios prácticos."
    }
  ],
  "raw_subtotal": 12.85,
  "final_score": 10.85,
  "quality_tier": "CRÍTICO (0.0 - 10.9 pts)",
  "mastery_path_readiness": {
    "mpri_score": 71.1,
    "mpri_max": 100.0,
    "mpri_tier": "PARTIAL MASTERY PATH (65-84): Funcional con Brechas ZPD/Modalidad",
    "pillars": {
      "zpd_adaptive_progression": {
        "score": 16.0,
        "max": 20.0
      },
      "retrieval_modality_and_anti_gaming": {
        "score": 10.0,
        "max": 20.0
      },
      "socratic_scaffolding_lifeline": {
        "score": 25.0,
        "max": 25.0
      },
      "diagnostic_remediation_alignment": {
        "score": 10.1,
        "max": 15.0
      },
      "dag_and_interleaving_topology": {
        "score": 0.0,
        "max": 10.0
      },
      "cognitive_ergonomics_and_framing": {
        "score": 10.0,
        "max": 10.0
      }
    }
  },
  "remediation_actions": [
    "Resolver penalización dura [bank_lt_3_exercises]: 1 competencia(s) tienen menos de 3 ejercicios prácticos.",
    "Elevar calificación global (10.8/20.0 < 14.0 mínimo requerido) atendiendo dimensiones deficitarias."
  ],
  "discovered_lint_rules": [],
  "platform_status": "RECHAZADO"
}
```

</details>