# Informe de Auditoría de Calidad Pedagógica y Psicométrica (QM-OSCQR)
## Curso: Economía Abierta y Balanza de Pagos (`eco_101`)

- **Fecha de Evaluación:** 2026-11-18
- **Evaluador:** Course QA Evaluator — Top's Academy (Modo Determinista)
- **Estado en Plataforma:** OBSERVADO
- **Calificación Final Certificada:** **13.6 / 20.0 pts**
- **Quality Tier:** **DEFICIENTE (11.0 - 13.9 pts)**
- **Mastery Path Readiness Index (MPRI):** **75.05 / 100.0** (PARTIAL MASTERY PATH (65-84): Funcional con Brechas ZPD/Modalidad)

---

### 1. Resumen Ejecutivo de Dimensiones

| Dimensión | Puntuación | Máximo | Calificación | Estado |
| :--- | :---: | :---: | :---: | :---: |
| **D1: Arquitectura Curricular y Granularidad** | **0.0** | 4.0 | 0% | ❌ Deficiente |
| **D2: Calidad Psicométrica y Reactivos** | **3.8** | 5.0 | 76% | ⚠️ Observación menor |
| **D3: Andamiaje y Pistas Socráticas** | **3.8** | 5.0 | 76% | ⚠️ Observación menor |
| **D4: Alineación Instruccional y ZPD** | **4.0** | 4.0 | 100% | ✅ Impecable |
| **D5: Ergonomía Técnica y KaTeX** | **2.0** | 2.0 | 100% | ✅ Impecable |
| **Penalizaciones Duras** | **-0.0** | - | - | ✅ Sin penalizaciones |
| **TOTAL** | **13.6** | **20.0** | **68.1%** | 🏆 **DEFICIENTE (11.0 - 13.9 pts)** |

---

### 2. Desglose Detallado por Dimensión

#### D1. Arquitectura Curricular y Granularidad (0.0 / 4.0 pts)
- Estructura curricular con 21 competencias (5 Hechos, 10 Conceptos, 6 Habilidades). DAG acíclico y conexo (ciclos=False, comp. conexos=21, pares solapados=0). ZPD: 0/21 competencias con calibración tri-banda ('easy', 'medium', 'hard').

#### D2. Calidad Psicométrica y Reactivos (3.8 / 5.0 pts)
- Modalidad: MC7=100.0%, FIB=0.0%, MS=0.0% (0.0% evocación activa/discriminación). Distractores: 189 evaluados con 100.0% cobertura de error_rationale (imposibles por dominio=0, claves corruptas=0, sesgo MS=0.0%).

#### D3. Andamiaje y Pistas Socráticas (3.8 / 5.0 pts)
- Andamiaje formativo: 100.0% de reactivos con 3 a 5 pistas socráticas escalonadas (100.0% pistas genuinas, 0.0% boilerplate Mad-Libs, 0.0% envenenadas). Unicidad diagnóstica real de rationales: 1.59% (rationales numéricos desconectados=0, advertencias clonadas/mudas=0).

#### D4. Alineación Instruccional y ZPD (4.0 / 4.0 pts)
- Alineación cognitiva de Bloom: 100.0% de habilidades prácticas en niveles superiores (Apply+). Registro disciplinar auténtico y alta fidelidad con los contenidos fuente.

#### D5. Ergonomía Técnica y KaTeX (2.0 / 2.0 pts)
- Sintaxis KaTeX: 0 errores críticos (delimitadores balanceados, llaves cerradas, cero $$$). Ergonomía: 0 observaciones de prosa en \text{...}, 0 identificadores crudos, 0 colisiones por concatenación y 0 formatos flotantes/asteriscos crudos.

---

### 3. Índice de Preparación para el Dominio (MPRI: 100.0 pts)

| Pilar Cognitivo | Puntaje | Máximo | Calificación |
| :--- | :---: | :---: | :---: |
| **1. Progresión Adaptativa ZPD y Bloom** | **20.00** | 20.0 | 100.0% |
| **2. Modalidad de Evocación y Anti-Gaming** | **10.00** | 20.0 | 50.0% |
| **3. Integridad Salvavidas Socrático (3-Strikes)** | **25.00** | 25.0 | 100.0% |
| **4. Alineación Diagnóstica en FeedbackToast** | **10.05** | 15.0 | 67.0% |
| **5. Topología DAG e Interleaving** | **0.00** | 10.0 | 0.0% |
| **6. Ergonomía Cognitiva y Sintaxis KaTeX** | **10.00** | 10.0 | 100.0% |
| **TOTAL MPRI** | **75.05** | **100.0** | **75.0% (PARTIAL MASTERY PATH (65-84): Funcional con Brechas ZPD/Modalidad)** |

---

### 4. Veredicto y Certificación

El curso **Economía Abierta y Balanza de Pagos** queda en estado **OBSERVADO** (requiere correcciones antes de despliegue pleno) con calificación de **13.6 / 20.0** y MPRI de **75.05 / 100.0**.

---

<details>
<summary>Metadatos Estructurados (JSON)</summary>

```json
{
  "course_metadata": {
    "course_id": "eco_101",
    "unit_title": "Economía Abierta y Balanza de Pagos",
    "detected_objective": "Curso completo de Economía Abierta y Balanza de Pagos con validación psicométrica estricta.",
    "total_competencies": 21,
    "total_questions": 63,
    "question_types_distribution": {
      "multiple_choice_7_options": 63
    },
    "platform_status": "OBSERVADO",
    "evaluator": "Course QA Evaluator — Standardized Deterministic Engine",
    "evaluation_date": "2026-11-18"
  },
  "dimension_scores": {
    "architecture_granularity": {
      "score": 0.0,
      "max": 4.0,
      "feedback": "Estructura curricular con 21 competencias (5 Hechos, 10 Conceptos, 6 Habilidades). DAG acíclico y conexo (ciclos=False, comp. conexos=21, pares solapados=0). ZPD: 0/21 competencias con calibración tri-banda ('easy', 'medium', 'hard')."
    },
    "assessment_quality": {
      "score": 3.8,
      "max": 5.0,
      "feedback": "Modalidad: MC7=100.0%, FIB=0.0%, MS=0.0% (0.0% evocación activa/discriminación). Distractores: 189 evaluados con 100.0% cobertura de error_rationale (imposibles por dominio=0, claves corruptas=0, sesgo MS=0.0%)."
    },
    "scaffolding_hints": {
      "score": 3.82,
      "max": 5.0,
      "feedback": "Andamiaje formativo: 100.0% de reactivos con 3 a 5 pistas socráticas escalonadas (100.0% pistas genuinas, 0.0% boilerplate Mad-Libs, 0.0% envenenadas). Unicidad diagnóstica real de rationales: 1.59% (rationales numéricos desconectados=0, advertencias clonadas/mudas=0)."
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
  "raw_subtotal": 13.62,
  "final_score": 13.62,
  "quality_tier": "DEFICIENTE (11.0 - 13.9 pts)",
  "mastery_path_readiness": {
    "mpri_score": 75.05,
    "mpri_max": 100.0,
    "mpri_tier": "PARTIAL MASTERY PATH (65-84): Funcional con Brechas ZPD/Modalidad",
    "pillars": {
      "zpd_adaptive_progression": {
        "score": 20.0,
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
        "score": 10.05,
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
    "Elevar calificación global (13.6/20.0 < 14.0 mínimo requerido) atendiendo dimensiones deficitarias."
  ],
  "discovered_lint_rules": [],
  "platform_status": "OBSERVADO"
}
```

</details>