# Informe de Auditoría de Calidad Pedagógica y Psicométrica (QM-OSCQR)
## Curso: Base Course (`math_base`)

- **Fecha de Evaluación:** 2026-11-14
- **Evaluador:** Course QA Evaluator — Top's Academy (Modo Determinista)
- **Estado en Plataforma:** ACTIVO
- **Calificación Final Certificada:** **13.2 / 20.0 pts**
- **Quality Tier:** **DEFICIENTE (11.0 - 13.9 pts)**
- **Mastery Path Readiness Index (MPRI):** **75.00 / 100.0** (PARTIAL MASTERY PATH (65-84): Funcional con Brechas ZPD/Modalidad)

---

### 1. Resumen Ejecutivo de Dimensiones

| Dimensión | Puntuación | Máximo | Calificación | Estado |
| :--- | :---: | :---: | :---: | :---: |
| **D1: Arquitectura Curricular y Granularidad** | **3.2** | 4.0 | 80% | ⚠️ Observación menor |
| **D2: Calidad Psicométrica y Reactivos** | **5.0** | 5.0 | 100% | ✅ Impecable |
| **D3: Andamiaje y Pistas Socráticas** | **4.0** | 5.0 | 80% | ⚠️ Observación menor |
| **D4: Alineación Instruccional y ZPD** | **4.0** | 4.0 | 100% | ✅ Impecable |
| **D5: Ergonomía Técnica y KaTeX** | **2.0** | 2.0 | 100% | ✅ Impecable |
| **Penalizaciones Duras** | **-5.0** | - | - | ⚠️ Penalizaciones aplicadas |
| **TOTAL** | **13.2** | **20.0** | **66.0%** | 🏆 **DEFICIENTE (11.0 - 13.9 pts)** |

---

### 2. Desglose Detallado por Dimensión

#### D1. Arquitectura Curricular y Granularidad (3.2 / 4.0 pts)
- Estructura curricular con 3 competencias (0 Hechos, 0 Conceptos, 0 Habilidades). DAG acíclico y conexo (ciclos=False, comp. conexos=1). ZPD: 0/3 competencias con calibración tri-banda ('easy', 'medium', 'hard').

#### D2. Calidad Psicométrica y Reactivos (5.0 / 5.0 pts)
- Modalidad: MC7=0.0%, FIB=0.0%, MS=0.0% (0.0% evocación activa/discriminación). Distractores: 0 evaluados con 100.0% cobertura de error_rationale. Cero distractores delatores (telltale=0) y 0 multiplicadores sintéticos.

#### D3. Andamiaje y Pistas Socráticas (4.0 / 5.0 pts)
- Andamiaje formativo: 100% de reactivos con 3 a 5 pistas socráticas escalonadas (100.0% pistas genuinas, 0.0% boilerplate Mad-Libs, 0.0% envenenadas). Soluciones formales paso a paso presentes en 0/3 ítems. Unicidad diagnóstica de rationales: 100.0%.

#### D4. Alineación Instruccional y ZPD (4.0 / 4.0 pts)
- Alineación cognitiva de Bloom: 100.0% de habilidades prácticas en niveles superiores (Apply+). Registro disciplinar auténtico y alta fidelidad con los contenidos fuente.

#### D5. Ergonomía Técnica y KaTeX (2.0 / 2.0 pts)
- Sintaxis KaTeX: 0 errores críticos (delimitadores balanceados, llaves cerradas, cero $$$). Ergonomía: 0 observaciones de prosa en \text{...} y 0 identificadores crudos.

---

### 3. Índice de Preparación para el Dominio (MPRI: 100.0 pts)

| Pilar Cognitivo | Puntaje | Máximo | Calificación |
| :--- | :---: | :---: | :---: |
| **1. Progresión Adaptativa ZPD y Bloom** | **20.00** | 20.0 | 100.0% |
| **2. Modalidad de Evocación y Anti-Gaming** | **20.00** | 20.0 | 100.0% |
| **3. Integridad Salvavidas Socrático (3-Strikes)** | **0.00** | 25.0 | 0.0% |
| **4. Alineación Diagnóstica en FeedbackToast** | **15.00** | 15.0 | 100.0% |
| **5. Topología DAG e Interleaving** | **10.00** | 10.0 | 100.0% |
| **6. Ergonomía Cognitiva y Sintaxis KaTeX** | **10.00** | 10.0 | 100.0% |
| **TOTAL MPRI** | **75.00** | **100.0** | **75.0% (PARTIAL MASTERY PATH (65-84): Funcional con Brechas ZPD/Modalidad)** |

---

### 4. Veredicto y Certificación

El curso **Base Course** ha sido **certificado y aprobado** con calificación sobresaliente de **13.2 / 20.0** y MPRI de **75.00 / 100.0**, acreditando el cumplimiento exhaustivo de los estándares Quality Matters, OSCQR y Mastery Learning.

---

<details>
<summary>Metadatos Estructurados (JSON)</summary>

```json
{
  "course_metadata": {
    "course_id": "math_base",
    "unit_title": "Base Course",
    "detected_objective": "",
    "total_competencies": 3,
    "total_questions": 3,
    "question_types_distribution": {
      "unknown": 3
    },
    "platform_status": "ACTIVO",
    "evaluator": "Course QA Evaluator — Standardized Deterministic Engine",
    "evaluation_date": "2026-11-14"
  },
  "dimension_scores": {
    "architecture_granularity": {
      "score": 3.2,
      "max": 4.0,
      "feedback": "Estructura curricular con 3 competencias (0 Hechos, 0 Conceptos, 0 Habilidades). DAG acíclico y conexo (ciclos=False, comp. conexos=1). ZPD: 0/3 competencias con calibración tri-banda ('easy', 'medium', 'hard')."
    },
    "assessment_quality": {
      "score": 5.0,
      "max": 5.0,
      "feedback": "Modalidad: MC7=0.0%, FIB=0.0%, MS=0.0% (0.0% evocación activa/discriminación). Distractores: 0 evaluados con 100.0% cobertura de error_rationale. Cero distractores delatores (telltale=0) y 0 multiplicadores sintéticos."
    },
    "scaffolding_hints": {
      "score": 4.0,
      "max": 5.0,
      "feedback": "Andamiaje formativo: 100% de reactivos con 3 a 5 pistas socráticas escalonadas (100.0% pistas genuinas, 0.0% boilerplate Mad-Libs, 0.0% envenenadas). Soluciones formales paso a paso presentes en 0/3 ítems. Unicidad diagnóstica de rationales: 100.0%."
    },
    "instructional_alignment": {
      "score": 4.0,
      "max": 4.0,
      "feedback": "Alineación cognitiva de Bloom: 100.0% de habilidades prácticas en niveles superiores (Apply+). Registro disciplinar auténtico y alta fidelidad con los contenidos fuente."
    },
    "technical_ergonomics": {
      "score": 2.0,
      "max": 2.0,
      "feedback": "Sintaxis KaTeX: 0 errores críticos (delimitadores balanceados, llaves cerradas, cero $$$). Ergonomía: 0 observaciones de prosa en \\text{...} y 0 identificadores crudos."
    }
  },
  "penalties_applied": [
    {
      "rule": "bank_lt_3_exercises",
      "deduction": 2.0,
      "reason": "3 competencia(s) tienen menos de 3 ejercicios prácticos."
    },
    {
      "rule": "hints_zero",
      "deduction": 3.0,
      "reason": "3 reactivo(s) carecen por completo de pistas progresivas (hints = 0)."
    }
  ],
  "raw_subtotal": 18.2,
  "final_score": 13.2,
  "quality_tier": "DEFICIENTE (11.0 - 13.9 pts)",
  "mastery_path_readiness": {
    "mpri_score": 75.0,
    "mpri_max": 100.0,
    "mpri_tier": "PARTIAL MASTERY PATH (65-84): Funcional con Brechas ZPD/Modalidad",
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
        "score": 0.0,
        "max": 25.0
      },
      "diagnostic_remediation_alignment": {
        "score": 15.0,
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
    "Certificación plena para despliegue en plataforma Top's Academy con Nivel DEFICIENTE (11.0 - 13.9 pts).",
    "El banco de 3 reactivos y 3 competencias cumple con los estándares Quality Matters, OSCQR y Mastery Learning."
  ],
  "discovered_lint_rules": [],
  "platform_status": "ACTIVO"
}
```

</details>