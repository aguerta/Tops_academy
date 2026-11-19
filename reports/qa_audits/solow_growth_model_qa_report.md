# Informe de Auditoría de Calidad Pedagógica y Psicométrica (QM-OSCQR)
## Curso: El Modelo de Crecimiento Económico de Solow (1956) (`solow_growth_model`)

- **Fecha de Evaluación:** 2026-11-18
- **Evaluador:** Course QA Evaluator — Top's Academy (Modo Determinista)
- **Estado en Plataforma:** ACTIVO
- **Calificación Final Certificada:** **17.9 / 20.0 pts**
- **Quality Tier:** **EXCELENTE (17.0 - 18.9 pts) — GOLD MASTERY**
- **Mastery Path Readiness Index (MPRI):** **91.53 / 100.0** (GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo)

---

### 1. Resumen Ejecutivo de Dimensiones

| Dimensión | Puntuación | Máximo | Calificación | Estado |
| :--- | :---: | :---: | :---: | :---: |
| **D1: Arquitectura Curricular y Granularidad** | **3.2** | 4.0 | 80% | ⚠️ Observación menor |
| **D2: Calidad Psicométrica y Reactivos** | **3.8** | 5.0 | 75% | ⚠️ Observación menor |
| **D3: Andamiaje y Pistas Socráticas** | **5.0** | 5.0 | 100% | ✅ Impecable |
| **D4: Alineación Instruccional y ZPD** | **4.0** | 4.0 | 100% | ✅ Impecable |
| **D5: Ergonomía Técnica y KaTeX** | **2.0** | 2.0 | 100% | ✅ Impecable |
| **Penalizaciones Duras** | **-0.0** | - | - | ✅ Sin penalizaciones |
| **TOTAL** | **17.9** | **20.0** | **89.7%** | 🏆 **GOLD MASTERY** |

---

### 2. Desglose Detallado por Dimensión

#### D1. Arquitectura Curricular y Granularidad (3.2 / 4.0 pts)
- Estructura curricular con 25 competencias (5 Hechos, 12 Conceptos, 8 Habilidades). DAG acíclico y conexo (ciclos=False, comp. conexos=1, pares solapados=1). ZPD: 1/25 competencias con calibración tri-banda ('easy', 'medium', 'hard').

#### D2. Calidad Psicométrica y Reactivos (3.8 / 5.0 pts)
- Modalidad: MC7=13.79%, FIB=43.28%, MS=42.93% (86.21% evocación activa/discriminación). Distractores: 1227 evaluados con 100.0% cobertura de error_rationale (imposibles por dominio=0, claves corruptas=0, sesgo MS=83.94%).

#### D3. Andamiaje y Pistas Socráticas (5.0 / 5.0 pts)
- Andamiaje formativo: 100.0% de reactivos con 3 a 5 pistas socráticas escalonadas (100.0% pistas genuinas, 0.0% boilerplate Mad-Libs, 0.0% envenenadas). Unicidad diagnóstica real de rationales: 100.0% (rationales numéricos desconectados=0, advertencias clonadas/mudas=0).

#### D4. Alineación Instruccional y ZPD (4.0 / 4.0 pts)
- Alineación cognitiva de Bloom: 100.0% de habilidades prácticas en niveles superiores (Apply+). Registro disciplinar auténtico y alta fidelidad con los contenidos fuente.

#### D5. Ergonomía Técnica y KaTeX (2.0 / 2.0 pts)
- Sintaxis KaTeX: 0 errores críticos (delimitadores balanceados, llaves cerradas, cero $$$). Ergonomía: 0 observaciones de prosa en \text{...}, 0 identificadores crudos, 0 colisiones por concatenación y 0 formatos flotantes/asteriscos crudos.

---

### 3. Índice de Preparación para el Dominio (MPRI: 100.0 pts)

| Pilar Cognitivo | Puntaje | Máximo | Calificación |
| :--- | :---: | :---: | :---: |
| **1. Progresión Adaptativa ZPD y Bloom** | **13.38** | 20.0 | 66.9% |
| **2. Modalidad de Evocación y Anti-Gaming** | **18.50** | 20.0 | 92.5% |
| **3. Integridad Salvavidas Socrático (3-Strikes)** | **25.00** | 25.0 | 100.0% |
| **4. Alineación Diagnóstica en FeedbackToast** | **15.00** | 15.0 | 100.0% |
| **5. Topología DAG e Interleaving** | **9.65** | 10.0 | 96.5% |
| **6. Ergonomía Cognitiva y Sintaxis KaTeX** | **10.00** | 10.0 | 100.0% |
| **TOTAL MPRI** | **91.53** | **100.0** | **91.5% (GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo)** |

---

### 4. Veredicto y Certificación

El curso **El Modelo de Crecimiento Económico de Solow (1956)** ha sido **certificado y aprobado** con calificación de **17.9 / 20.0** y MPRI de **91.53 / 100.0**, acreditando el cumplimiento de los estándares Quality Matters, OSCQR y Mastery Learning.

---

<details>
<summary>Metadatos Estructurados (JSON)</summary>

```json
{
  "course_metadata": {
    "course_id": "solow_growth_model",
    "unit_title": "El Modelo de Crecimiento Económico de Solow (1956)",
    "detected_objective": "Comprender, formular y resolver dinámicamente el modelo neoclásico de crecimiento económico de Solow (1956), analizando sus propiedades de estabilidad, implicaciones de precios factoriales, dinámicas de transición y extensiones analíticas.",
    "total_competencies": 25,
    "total_questions": 580,
    "question_types_distribution": {
      "fill_in_the_blank": 251,
      "multiple_select": 249,
      "multiple_choice_7_options": 80
    },
    "platform_status": "ACTIVO",
    "evaluator": "Course QA Evaluator — Standardized Deterministic Engine",
    "evaluation_date": "2026-11-18"
  },
  "dimension_scores": {
    "architecture_granularity": {
      "score": 3.19,
      "max": 4.0,
      "feedback": "Estructura curricular con 25 competencias (5 Hechos, 12 Conceptos, 8 Habilidades). DAG acíclico y conexo (ciclos=False, comp. conexos=1, pares solapados=1). ZPD: 1/25 competencias con calibración tri-banda ('easy', 'medium', 'hard')."
    },
    "assessment_quality": {
      "score": 3.75,
      "max": 5.0,
      "feedback": "Modalidad: MC7=13.79%, FIB=43.28%, MS=42.93% (86.21% evocación activa/discriminación). Distractores: 1227 evaluados con 100.0% cobertura de error_rationale (imposibles por dominio=0, claves corruptas=0, sesgo MS=83.94%)."
    },
    "scaffolding_hints": {
      "score": 5.0,
      "max": 5.0,
      "feedback": "Andamiaje formativo: 100.0% de reactivos con 3 a 5 pistas socráticas escalonadas (100.0% pistas genuinas, 0.0% boilerplate Mad-Libs, 0.0% envenenadas). Unicidad diagnóstica real de rationales: 100.0% (rationales numéricos desconectados=0, advertencias clonadas/mudas=0)."
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
  "penalties_applied": [],
  "raw_subtotal": 17.94,
  "final_score": 17.94,
  "quality_tier": "EXCELENTE (17.0 - 18.9 pts) — GOLD MASTERY",
  "mastery_path_readiness": {
    "mpri_score": 91.53,
    "mpri_max": 100.0,
    "mpri_tier": "GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo",
    "pillars": {
      "zpd_adaptive_progression": {
        "score": 13.38,
        "max": 20.0
      },
      "retrieval_modality_and_anti_gaming": {
        "score": 18.5,
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
    }
  },
  "remediation_actions": [
    "Certificación plena para despliegue en plataforma Top's Academy con Nivel EXCELENTE (17.0 - 18.9 pts) — GOLD MASTERY.",
    "El banco de 580 reactivos y 25 competencias cumple con los estándares Quality Matters, OSCQR y Mastery Learning."
  ],
  "discovered_lint_rules": [],
  "platform_status": "ACTIVO"
}
```

</details>