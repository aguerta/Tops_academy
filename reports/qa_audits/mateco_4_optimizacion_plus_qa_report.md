# Informe de Auditoría de Calidad Pedagógica y Psicométrica (QM-OSCQR)
## Curso: Mateco 4 Optimizacion Plus (`mateco_4_optimizacion_plus`)

- **Fecha de Evaluación:** 2026-11-18
- **Evaluador:** Course QA Evaluator — Top's Academy (Modo Determinista)
- **Estado en Plataforma:** ACTIVO
- **Calificación Final Certificada:** **19.0 / 20.0 pts**
- **Quality Tier:** **EXCELENTE (19.0 - 20.0 pts) — PLATINUM MASTERY**
- **Mastery Path Readiness Index (MPRI):** **95.50 / 100.0** (GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo)

---

### 1. Resumen Ejecutivo de Dimensiones

| Dimensión | Puntuación | Máximo | Calificación | Estado |
| :--- | :---: | :---: | :---: | :---: |
| **D1: Arquitectura Curricular y Granularidad** | **3.4** | 4.0 | 85% | ⚠️ Observación menor |
| **D2: Calidad Psicométrica y Reactivos** | **5.0** | 5.0 | 100% | ✅ Impecable |
| **D3: Andamiaje y Pistas Socráticas** | **4.6** | 5.0 | 92% | ✨ Excelente |
| **D4: Alineación Instruccional y ZPD** | **4.0** | 4.0 | 100% | ✅ Impecable |
| **D5: Ergonomía Técnica y KaTeX** | **2.0** | 2.0 | 100% | ✅ Impecable |
| **Penalizaciones Duras** | **-0.0** | - | - | ✅ Sin penalizaciones |
| **TOTAL** | **19.0** | **20.0** | **95.0%** | 🏆 **PLATINUM MASTERY** |

---

### 2. Desglose Detallado por Dimensión

#### D1. Arquitectura Curricular y Granularidad (3.4 / 4.0 pts)
- Estructura curricular con 30 competencias (1 Hechos, 16 Conceptos, 13 Habilidades). DAG acíclico y conexo (ciclos=False, comp. conexos=1, pares solapados=12). ZPD: 30/30 competencias con calibración tri-banda ('easy', 'medium', 'hard').

#### D2. Calidad Psicométrica y Reactivos (5.0 / 5.0 pts)
- Modalidad: MC7=42.6%, FIB=33.29%, MS=24.11% (57.4% evocación activa/discriminación). Distractores: 2232 evaluados con 100.0% cobertura de error_rationale (imposibles por dominio=0, claves corruptas=0, sesgo MS=46.59%).

#### D3. Andamiaje y Pistas Socráticas (4.6 / 5.0 pts)
- Andamiaje formativo: 100.0% de reactivos con 3 a 5 pistas socráticas escalonadas (100.0% pistas genuinas, 0.0% boilerplate Mad-Libs, 0.0% envenenadas). Unicidad diagnóstica real de rationales: 100.0% (rationales numéricos desconectados=0, advertencias clonadas/mudas=243).

#### D4. Alineación Instruccional y ZPD (4.0 / 4.0 pts)
- Alineación cognitiva de Bloom: 100.0% de habilidades prácticas en niveles superiores (Apply+). Registro disciplinar auténtico y alta fidelidad con los contenidos fuente.

#### D5. Ergonomía Técnica y KaTeX (2.0 / 2.0 pts)
- Sintaxis KaTeX: 0 errores críticos (delimitadores balanceados, llaves cerradas, cero $$$). Ergonomía: 0 observaciones de prosa en \text{...}, 0 identificadores crudos, 0 colisiones por concatenación y 0 formatos flotantes/asteriscos crudos.

---

### 3. Índice de Preparación para el Dominio (MPRI: 100.0 pts)

| Pilar Cognitivo | Puntaje | Máximo | Calificación |
| :--- | :---: | :---: | :---: |
| **1. Progresión Adaptativa ZPD y Bloom** | **20.00** | 20.0 | 100.0% |
| **2. Modalidad de Evocación y Anti-Gaming** | **20.00** | 20.0 | 100.0% |
| **3. Integridad Salvavidas Socrático (3-Strikes)** | **23.00** | 25.0 | 92.0% |
| **4. Alineación Diagnóstica en FeedbackToast** | **15.00** | 15.0 | 100.0% |
| **5. Topología DAG e Interleaving** | **7.50** | 10.0 | 75.0% |
| **6. Ergonomía Cognitiva y Sintaxis KaTeX** | **10.00** | 10.0 | 100.0% |
| **TOTAL MPRI** | **95.50** | **100.0** | **95.5% (GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo)** |

---

### 4. Veredicto y Certificación

El curso **Mateco 4 Optimizacion Plus** ha sido **certificado y aprobado** con calificación de **19.0 / 20.0** y MPRI de **95.50 / 100.0**, acreditando el cumplimiento de los estándares Quality Matters, OSCQR y Mastery Learning.

---

<details>
<summary>Metadatos Estructurados (JSON)</summary>

```json
{
  "course_metadata": {
    "course_id": "mateco_4_optimizacion_plus",
    "unit_title": "Mateco 4 Optimizacion Plus",
    "detected_objective": "Dominio y aplicación analítica integral de Mateco 4 Optimizacion Plus",
    "total_competencies": 30,
    "total_questions": 730,
    "question_types_distribution": {
      "multiple_choice_7_options": 311,
      "fill_in_the_blank": 243,
      "multiple_select": 176
    },
    "platform_status": "ACTIVO",
    "evaluator": "Course QA Evaluator — Standardized Deterministic Engine",
    "evaluation_date": "2026-11-18"
  },
  "dimension_scores": {
    "architecture_granularity": {
      "score": 3.4,
      "max": 4.0,
      "feedback": "Estructura curricular con 30 competencias (1 Hechos, 16 Conceptos, 13 Habilidades). DAG acíclico y conexo (ciclos=False, comp. conexos=1, pares solapados=12). ZPD: 30/30 competencias con calibración tri-banda ('easy', 'medium', 'hard')."
    },
    "assessment_quality": {
      "score": 5.0,
      "max": 5.0,
      "feedback": "Modalidad: MC7=42.6%, FIB=33.29%, MS=24.11% (57.4% evocación activa/discriminación). Distractores: 2232 evaluados con 100.0% cobertura de error_rationale (imposibles por dominio=0, claves corruptas=0, sesgo MS=46.59%)."
    },
    "scaffolding_hints": {
      "score": 4.6,
      "max": 5.0,
      "feedback": "Andamiaje formativo: 100.0% de reactivos con 3 a 5 pistas socráticas escalonadas (100.0% pistas genuinas, 0.0% boilerplate Mad-Libs, 0.0% envenenadas). Unicidad diagnóstica real de rationales: 100.0% (rationales numéricos desconectados=0, advertencias clonadas/mudas=243)."
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
  "raw_subtotal": 19.0,
  "final_score": 19.0,
  "quality_tier": "EXCELENTE (19.0 - 20.0 pts) — PLATINUM MASTERY",
  "mastery_path_readiness": {
    "mpri_score": 95.5,
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
        "score": 23.0,
        "max": 25.0
      },
      "diagnostic_remediation_alignment": {
        "score": 15.0,
        "max": 15.0
      },
      "dag_and_interleaving_topology": {
        "score": 7.5,
        "max": 10.0
      },
      "cognitive_ergonomics_and_framing": {
        "score": 10.0,
        "max": 10.0
      }
    }
  },
  "remediation_actions": [
    "Certificación plena para despliegue en plataforma Top's Academy con Nivel EXCELENTE (19.0 - 20.0 pts) — PLATINUM MASTERY.",
    "El banco de 730 reactivos y 30 competencias cumple con los estándares Quality Matters, OSCQR y Mastery Learning."
  ],
  "discovered_lint_rules": [],
  "platform_status": "ACTIVO"
}
```

</details>