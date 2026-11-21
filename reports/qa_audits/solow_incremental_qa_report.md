# Informe de Auditoría de Calidad Pedagógica y Psicométrica (QM-OSCQR)
## Curso: Modelo de Crecimiento de Solow (`solow_incremental`)

- **Fecha de Evaluación:** 2026-11-21
- **Evaluador:** Course QA Evaluator — Top's Academy (Modo Determinista)
- **Estado en Plataforma:** ACTIVO
- **Calificación Final Certificada:** **17.3 / 20.0 pts**
- **Quality Tier:** **EXCELENTE (17.0 - 18.9 pts) — GOLD MASTERY**
- **Mastery Path Readiness Index (MPRI):** **82.01 / 100.0** (PARTIAL MASTERY PATH (65-84): Funcional con Brechas ZPD/Modalidad)

---

### 1. Resumen Ejecutivo de Dimensiones

| Dimensión | Puntuación | Máximo | Calificación | Estado |
| :--- | :---: | :---: | :---: | :---: |
| **D1: Arquitectura Curricular y Granularidad** | **3.2** | 4.0 | 81% | ⚠️ Observación menor |
| **D2: Calidad Psicométrica y Reactivos** | **4.2** | 5.0 | 84% | ⚠️ Observación menor |
| **D3: Andamiaje y Pistas Socráticas** | **3.8** | 5.0 | 77% | ⚠️ Observación menor |
| **D4: Alineación Instruccional y ZPD** | **4.0** | 4.0 | 100% | ✅ Impecable |
| **D5: Ergonomía Técnica y KaTeX** | **2.0** | 2.0 | 100% | ✅ Impecable |
| **Penalizaciones Duras** | **-0.0** | - | - | ✅ Sin penalizaciones |
| **TOTAL** | **17.3** | **20.0** | **86.3%** | 🏆 **GOLD MASTERY** |

---

### 2. Desglose Detallado por Dimensión

#### D1. Arquitectura Curricular y Granularidad (3.2 / 4.0 pts)
- Estructura curricular con 2 competencias (0 Hechos, 0 Conceptos, 2 Habilidades). DAG acíclico y conexo (ciclos=False, comp. conexos=2, pares solapados=0). ZPD: 0/2 competencias con calibración tri-banda ('easy', 'medium', 'hard').

#### D2. Calidad Psicométrica y Reactivos (4.2 / 5.0 pts)
- Modalidad: MC7=86.89%, FIB=6.56%, MS=6.56% (13.11% evocación activa/discriminación). Distractores: 330 evaluados con 100.0% cobertura de error_rationale (imposibles por dominio=0, claves corruptas=0, sesgo MS=100.0%).

#### D3. Andamiaje y Pistas Socráticas (3.8 / 5.0 pts)
- Andamiaje formativo: 100.0% de reactivos con 3 a 5 pistas socráticas escalonadas (100.0% pistas genuinas, 0.0% boilerplate Mad-Libs, 0.0% envenenadas). Unicidad diagnóstica real de rationales: 2.73% (rationales numéricos desconectados=0, advertencias clonadas/mudas=0).

#### D4. Alineación Instruccional y ZPD (4.0 / 4.0 pts)
- Alineación cognitiva de Bloom: 93.44% de habilidades prácticas en niveles superiores (Apply+). Registro disciplinar auténtico y alta fidelidad con los contenidos fuente.

#### D5. Ergonomía Técnica y KaTeX (2.0 / 2.0 pts)
- Sintaxis KaTeX: 0 errores críticos (delimitadores balanceados, llaves cerradas, cero $$$). Ergonomía: 0 observaciones de prosa en \text{...}, 0 identificadores crudos, 0 colisiones por concatenación y 0 formatos flotantes/asteriscos crudos.

---

### 3. Índice de Preparación para el Dominio (MPRI: 100.0 pts)

| Pilar Cognitivo | Puntaje | Máximo | Calificación |
| :--- | :---: | :---: | :---: |
| **1. Progresión Adaptativa ZPD y Bloom** | **14.68** | 20.0 | 73.4% |
| **2. Modalidad de Evocación y Anti-Gaming** | **12.24** | 20.0 | 61.2% |
| **3. Integridad Salvavidas Socrático (3-Strikes)** | **25.00** | 25.0 | 100.0% |
| **4. Alineación Diagnóstica en FeedbackToast** | **10.09** | 15.0 | 67.3% |
| **5. Topología DAG e Interleaving** | **10.00** | 10.0 | 100.0% |
| **6. Ergonomía Cognitiva y Sintaxis KaTeX** | **10.00** | 10.0 | 100.0% |
| **TOTAL MPRI** | **82.01** | **100.0** | **82.0% (PARTIAL MASTERY PATH (65-84): Funcional con Brechas ZPD/Modalidad)** |

---

### 4. Veredicto y Certificación

El curso **Modelo de Crecimiento de Solow** ha sido **certificado y aprobado** con calificación de **17.3 / 20.0** y MPRI de **82.01 / 100.0**, acreditando el cumplimiento de los estándares Quality Matters, OSCQR y Mastery Learning.

---

<details>
<summary>Metadatos Estructurados (JSON)</summary>

```json
{
  "course_metadata": {
    "course_id": "solow_incremental",
    "unit_title": "Modelo de Crecimiento de Solow",
    "detected_objective": "Banco de ejercicios canonico y completo para validacion del sistema Top's Academy.",
    "total_competencies": 2,
    "total_questions": 61,
    "question_types_distribution": {
      "multiple_choice_7_options": 53,
      "multiple_select": 4,
      "fill_in_the_blank": 4
    },
    "platform_status": "ACTIVO",
    "evaluator": "Course QA Evaluator — Standardized Deterministic Engine",
    "evaluation_date": "2026-11-21"
  },
  "dimension_scores": {
    "architecture_granularity": {
      "score": 3.25,
      "max": 4.0,
      "feedback": "Estructura curricular con 2 competencias (0 Hechos, 0 Conceptos, 2 Habilidades). DAG acíclico y conexo (ciclos=False, comp. conexos=2, pares solapados=0). ZPD: 0/2 competencias con calibración tri-banda ('easy', 'medium', 'hard')."
    },
    "assessment_quality": {
      "score": 4.18,
      "max": 5.0,
      "feedback": "Modalidad: MC7=86.89%, FIB=6.56%, MS=6.56% (13.11% evocación activa/discriminación). Distractores: 330 evaluados con 100.0% cobertura de error_rationale (imposibles por dominio=0, claves corruptas=0, sesgo MS=100.0%)."
    },
    "scaffolding_hints": {
      "score": 3.84,
      "max": 5.0,
      "feedback": "Andamiaje formativo: 100.0% de reactivos con 3 a 5 pistas socráticas escalonadas (100.0% pistas genuinas, 0.0% boilerplate Mad-Libs, 0.0% envenenadas). Unicidad diagnóstica real de rationales: 2.73% (rationales numéricos desconectados=0, advertencias clonadas/mudas=0)."
    },
    "instructional_alignment": {
      "score": 4.0,
      "max": 4.0,
      "feedback": "Alineación cognitiva de Bloom: 93.44% de habilidades prácticas en niveles superiores (Apply+). Registro disciplinar auténtico y alta fidelidad con los contenidos fuente."
    },
    "technical_ergonomics": {
      "score": 2.0,
      "max": 2.0,
      "feedback": "Sintaxis KaTeX: 0 errores críticos (delimitadores balanceados, llaves cerradas, cero $$$). Ergonomía: 0 observaciones de prosa en \\text{...}, 0 identificadores crudos, 0 colisiones por concatenación y 0 formatos flotantes/asteriscos crudos."
    }
  },
  "penalties_applied": [],
  "raw_subtotal": 17.27,
  "final_score": 17.27,
  "quality_tier": "EXCELENTE (17.0 - 18.9 pts) — GOLD MASTERY",
  "mastery_path_readiness": {
    "mpri_score": 82.01,
    "mpri_max": 100.0,
    "mpri_tier": "PARTIAL MASTERY PATH (65-84): Funcional con Brechas ZPD/Modalidad",
    "pillars": {
      "zpd_adaptive_progression": {
        "score": 14.68,
        "max": 20.0
      },
      "retrieval_modality_and_anti_gaming": {
        "score": 12.24,
        "max": 20.0
      },
      "socratic_scaffolding_lifeline": {
        "score": 25.0,
        "max": 25.0
      },
      "diagnostic_remediation_alignment": {
        "score": 10.09,
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
    "Certificación plena para despliegue en plataforma Top's Academy con Nivel EXCELENTE (17.0 - 18.9 pts) — GOLD MASTERY.",
    "El banco de 61 reactivos y 2 competencias cumple con los estándares Quality Matters, OSCQR y Mastery Learning."
  ],
  "discovered_lint_rules": [],
  "platform_status": "ACTIVO"
}
```

</details>