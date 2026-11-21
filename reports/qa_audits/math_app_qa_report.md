# Informe de Auditoría de Calidad Pedagógica y Psicométrica (QM-OSCQR)
## Curso: Math Course (`math_app`)

- **Fecha de Evaluación:** 2026-11-21
- **Evaluador:** Course QA Evaluator — Top's Academy (Modo Determinista)
- **Estado en Plataforma:** OBSERVADO
- **Calificación Final Certificada:** **15.7 / 20.0 pts**
- **Quality Tier:** **ACEPTABLE (14.0 - 16.9 pts) — SILVER MASTERY**
- **Mastery Path Readiness Index (MPRI):** **68.65 / 100.0** (PARTIAL MASTERY PATH (65-84): Funcional con Brechas ZPD/Modalidad)

---

### 1. Resumen Ejecutivo de Dimensiones

| Dimensión | Puntuación | Máximo | Calificación | Estado |
| :--- | :---: | :---: | :---: | :---: |
| **D1: Arquitectura Curricular y Granularidad** | **2.5** | 4.0 | 62% | ❌ Deficiente |
| **D2: Calidad Psicométrica y Reactivos** | **3.8** | 5.0 | 76% | ⚠️ Observación menor |
| **D3: Andamiaje y Pistas Socráticas** | **3.9** | 5.0 | 77% | ⚠️ Observación menor |
| **D4: Alineación Instruccional y ZPD** | **4.0** | 4.0 | 100% | ✅ Impecable |
| **D5: Ergonomía Técnica y KaTeX** | **2.0** | 2.0 | 100% | ✅ Impecable |
| **Penalizaciones Duras** | **-0.5** | - | - | ⚠️ Penalizaciones aplicadas |
| **TOTAL** | **15.7** | **20.0** | **78.3%** | 🏆 **SILVER MASTERY** |

---

### 2. Desglose Detallado por Dimensión

#### D1. Arquitectura Curricular y Granularidad (2.5 / 4.0 pts)
- Estructura curricular con 1 competencias (0 Hechos, 1 Conceptos, 0 Habilidades). DAG acíclico y conexo (ciclos=False, comp. conexos=1, pares solapados=0). ZPD: 0/1 competencias con calibración tri-banda ('easy', 'medium', 'hard').

#### D2. Calidad Psicométrica y Reactivos (3.8 / 5.0 pts)
- Modalidad: MC7=100.0%, FIB=0.0%, MS=0.0% (0.0% evocación activa/discriminación). Distractores: 126 evaluados con 100.0% cobertura de error_rationale (imposibles por dominio=0, claves corruptas=0, sesgo MS=0.0%).

#### D3. Andamiaje y Pistas Socráticas (3.9 / 5.0 pts)
- Andamiaje formativo: 100.0% de reactivos con 3 a 5 pistas socráticas escalonadas (100.0% pistas genuinas, 0.0% boilerplate Mad-Libs, 0.0% envenenadas). Unicidad diagnóstica real de rationales: 4.76% (rationales numéricos desconectados=0, advertencias clonadas/mudas=0).

#### D4. Alineación Instruccional y ZPD (4.0 / 4.0 pts)
- Alineación cognitiva de Bloom: 100.0% de habilidades prácticas en niveles superiores (Apply+). Registro disciplinar auténtico y alta fidelidad con los contenidos fuente.

#### D5. Ergonomía Técnica y KaTeX (2.0 / 2.0 pts)
- Sintaxis KaTeX: 0 errores críticos (delimitadores balanceados, llaves cerradas, cero $$$). Ergonomía: 0 observaciones de prosa en \text{...}, 0 identificadores crudos, 0 colisiones por concatenación y 0 formatos flotantes/asteriscos crudos.

---

### 3. Índice de Preparación para el Dominio (MPRI: 100.0 pts)

| Pilar Cognitivo | Puntaje | Máximo | Calificación |
| :--- | :---: | :---: | :---: |
| **1. Progresión Adaptativa ZPD y Bloom** | **8.00** | 20.0 | 40.0% |
| **2. Modalidad de Evocación y Anti-Gaming** | **5.50** | 20.0 | 27.5% |
| **3. Integridad Salvavidas Socrático (3-Strikes)** | **25.00** | 25.0 | 100.0% |
| **4. Alineación Diagnóstica en FeedbackToast** | **10.15** | 15.0 | 67.7% |
| **5. Topología DAG e Interleaving** | **10.00** | 10.0 | 100.0% |
| **6. Ergonomía Cognitiva y Sintaxis KaTeX** | **10.00** | 10.0 | 100.0% |
| **TOTAL MPRI** | **68.65** | **100.0** | **68.7% (PARTIAL MASTERY PATH (65-84): Funcional con Brechas ZPD/Modalidad)** |

---

### 4. Veredicto y Certificación

El curso **Math Course** queda en estado **OBSERVADO** (requiere correcciones antes de despliegue pleno) con calificación de **15.7 / 20.0** y MPRI de **68.65 / 100.0**.

---

<details>
<summary>Metadatos Estructurados (JSON)</summary>

```json
{
  "course_metadata": {
    "course_id": "math_app",
    "unit_title": "Math Course",
    "detected_objective": "Curso formativo con ejercicios interactivos.",
    "total_competencies": 1,
    "total_questions": 21,
    "question_types_distribution": {
      "multiple_choice_7_options": 21
    },
    "platform_status": "OBSERVADO",
    "evaluator": "Course QA Evaluator — Standardized Deterministic Engine",
    "evaluation_date": "2026-11-21"
  },
  "dimension_scores": {
    "architecture_granularity": {
      "score": 2.5,
      "max": 4.0,
      "feedback": "Estructura curricular con 1 competencias (0 Hechos, 1 Conceptos, 0 Habilidades). DAG acíclico y conexo (ciclos=False, comp. conexos=1, pares solapados=0). ZPD: 0/1 competencias con calibración tri-banda ('easy', 'medium', 'hard')."
    },
    "assessment_quality": {
      "score": 3.8,
      "max": 5.0,
      "feedback": "Modalidad: MC7=100.0%, FIB=0.0%, MS=0.0% (0.0% evocación activa/discriminación). Distractores: 126 evaluados con 100.0% cobertura de error_rationale (imposibles por dominio=0, claves corruptas=0, sesgo MS=0.0%)."
    },
    "scaffolding_hints": {
      "score": 3.87,
      "max": 5.0,
      "feedback": "Andamiaje formativo: 100.0% de reactivos con 3 a 5 pistas socráticas escalonadas (100.0% pistas genuinas, 0.0% boilerplate Mad-Libs, 0.0% envenenadas). Unicidad diagnóstica real de rationales: 4.76% (rationales numéricos desconectados=0, advertencias clonadas/mudas=0)."
    },
    "instructional_alignment": {
      "score": 4.0,
      "max": 4.0,
      "feedback": "Alineación cognitiva de Bloom: 100.0% de habilidades prácticas en niveles superiores (Apply+). Registro disciplinar auténtico y alta fidelidad con los contenidos fuente."
    },
    "technical_ergonomics": {
      "score": 2.0,
      "max": 2.0,
      "feedback": "Sintaxis KaTeX: 0 errores críticos (delimitadores balanceados, llaves cerradas, cero $$$). Ergonomía: 0 observaciones de prosa en \\text{...}, 0 identificadores crudos, 0 colisiones por concatenación y 0 formatos flotantes/asteriscos crudos."
    }
  },
  "penalties_applied": [
    {
      "rule": "answer_memorization_exploit",
      "deduction": 0.5,
      "reason": "1 competencia(s) permiten alcanzar 'Mastered' por memorización visual (<= 4 respuestas correctas únicas en >= 15 reactivos)."
    }
  ],
  "raw_subtotal": 16.17,
  "final_score": 15.67,
  "quality_tier": "ACEPTABLE (14.0 - 16.9 pts) — SILVER MASTERY",
  "mastery_path_readiness": {
    "mpri_score": 68.65,
    "mpri_max": 100.0,
    "mpri_tier": "PARTIAL MASTERY PATH (65-84): Funcional con Brechas ZPD/Modalidad",
    "pillars": {
      "zpd_adaptive_progression": {
        "score": 8.0,
        "max": 20.0
      },
      "retrieval_modality_and_anti_gaming": {
        "score": 5.5,
        "max": 20.0
      },
      "socratic_scaffolding_lifeline": {
        "score": 25.0,
        "max": 25.0
      },
      "diagnostic_remediation_alignment": {
        "score": 10.15,
        "max": 15.0
      },
      "dag_and_interleaving_topology": {
        "score": 10.0,
        "max": 10.0
      },
      "cognitive_ergonomics_and_framing": {
        "score": 10.0,
        "max": 10.0
      }
    }
  },
  "remediation_actions": [
    "Resolver penalización dura [answer_memorization_exploit]: 1 competencia(s) permiten alcanzar 'Mastered' por memorización visual (<= 4 respuestas correctas únicas en >= 15 reactivos).",
    "Elevar Índice MPRI (68.65/100.0 < 70.0 mínimo requerido) fortaleciendo ZPD, modalidad activa y andamiaje."
  ],
  "discovered_lint_rules": [],
  "platform_status": "OBSERVADO"
}
```

</details>