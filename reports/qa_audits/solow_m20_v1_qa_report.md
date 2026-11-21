# Reporte de Auditoría Técnica y Pedagógica — `solow_m20_v1`

**Curso:** Solow M20 V1 (`solow_m20_v1`)  
**Archivo fuente:** `solow_m20_v1.json`  
**Estándares aplicados:** Quality Matters (QM), OSCQR, Mastery Learning (Bloom 2-Sigma), ZPD (Vygotsky) & Path-to-Mastery v2.0  
**Fecha de auditoría:** 2026-11-21  

---

## 1. Resumen Ejecutivo

| Métrica | Resultado | Estado |
| :--- | :--- | :--- |
| **Calificación Final QM-OSCQR** | **19.72 / 20.0** | **EXCELENTE (19.0 - 20.0 pts) — PLATINUM MASTERY** |
| **Mastery Path Readiness Index (MPRI)** | **98.45 / 100.0** | **GOLD MASTERY PATH (85-100)** |
| **Penalizaciones Duras Automáticas** | **0.0 pts** (0 reglas activadas) | Limpio |
| **Competencias / Reactivos** | **22** competencias / **540** reactivos | 20–30 ítems por competencia |
| **Auditoría de Jueces Ciegos (Stage 5)** | **120 / 120** acuerdos (`100.0%`) | 0 desacuerdos sin reparar |
| **Risk Score** | **6.57** | Riesgo bajo (ergonomía KaTeX en soluciones) |

> [!WARNING]
> **Bloqueador de Validación de Plataforma Detectado (`platform_validation_error`):** El validador de la plataforma reportó `"Invalid question type 'concept_matching'"` (90 reactivos). Aunque el diseño psicométrico y pedagógico de los 540 ítems M20 alcanza nivel *Platinum Mastery* (`19.72/20.0`), se requiere habilitar/registrar el tipo `concept_matching` (y verificar soporte para el resto de modalidades M20) en el validador del backend antes de publicar el curso en producción.

---

## 2. Desglose por Dimensiones (Rúbrica Normativa 20.0 pts)

| Dimensión | Puntaje | Máximo | Diagnóstico |
| :--- | :---: | :---: | :--- |
| **D1. Arquitectura Curricular, Topología DAG y Calibración ZPD** | **3.92** | 4.00 | 22 competencias (`1` Hecho, `11` Conceptos, `10` Habilidades). DAG acíclico (`has_cycle=false`), conexo (`1` componente, profundidad máx. `6`), sin aristas invertidas ni nodos isla. **22/22 competencias con calibración tri-banda (`easy`/`medium`/`hard`)**. Deducción menor (`-0.08`) por 1 par con solapamiento temático (`Hab-02` ↔ `Hab-05`). |
| **D2. Calidad Psicométrica, Modalidad de Evocación y Anti-Gaming** | **5.00** | 5.00 | `100.0%` de evocación activa y discriminación (`MC7=0.0%`, `FIB=17.04%`, `MS=2.59%`, `BloomSup=80.37%` repartido en `open_symbolic`, `adversarial_break`, `concept_matching`, `unstructured_model`, `proof_dag`, `invariant_canvas`). Cobertura `100.0%` de `error_rationale`, `0` distractores imposibles o multiplicadores mágicos, `0` relleno `[R-15]` y `0` competencias memorizables. |
| **D3. Andamiaje Socrático Progresivo y Remediación Diagnóstica** | **5.00** | 5.00 | `100.0%` de reactivos con 3 pistas socráticas genuinas y escalonadas (`0.0%` boilerplate Mad-Libs, `0.0%` pistas envenenadas, `0` fugas). `100.0%` de unicidad diagnóstica en slots de `error_rationale`, `0` advertencias clonadas o desconectadas. |
| **D4. Alineación Instruccional, Taxonomía de Bloom y Pureza de Dominio** | **4.00** | 4.00 | `100.0%` de habilidades prácticas (`300/300`) en niveles superiores de Bloom (`Apply: 154`, `Analyze: 190`, `Evaluate: 125`; `Remember: 26`, `Understand: 45`). Registro disciplinar auténtico en teoría del crecimiento de Solow (1956), sin contaminación inter-dominio. |
| **D5. Accesibilidad, Ergonomía Cognitiva en UI y Sintaxis KaTeX** | **1.80** | 2.00 | `0` errores críticos de delimitadores o llaves en KaTeX, `0` prosa larga en `\text{...}`, `0` identificadores crudos. Deducción de `-0.20` por **60 reactivos** con sintaxis cruda de SymPy dentro de `$...$` en `detailed_solution` (`*`, `sqrt()`, `exp()`) y **10 reactivos** en `Hab-03` con asteriscos crudos `*` en KaTeX. |

### Índice de Preparación para el Dominio (`MPRI`: 98.45 / 100.0)

| Pilar Cognitivo y de Plataforma | Puntaje | Máximo |
| :--- | :---: | :---: |
| `zpd_adaptive_progression` | 20.00 | 20.0 |
| `retrieval_modality_and_anti_gaming` | 20.00 | 20.0 |
| `socratic_scaffolding_lifeline` | 25.00 | 25.0 |
| `diagnostic_remediation_alignment` | 15.00 | 15.0 |
| `dag_and_interleaving_topology` | 9.65 | 10.0 |
| `cognitive_ergonomics_and_framing` | 8.80 | 10.0 |

---

## 3. Verificación Semántica sobre Muestras Estratificadas y Clústeres de Riesgo

La inspección semántica de las muestras estratificadas (`Q-C01-001`..`Q-Hab10-512`) y de los clústeres de riesgo (`katex_issues`, `katex_ergonomics`, `sympy_in_katex`) confirma:

1. **Rigor Matemático y Económico (Solow 1956):**
   - Derivación correcta de la función intensiva $Q = L\phi(k)$, homogeneidad lineal y ecuación fundamental $\dot{k} = s\phi(k) - \lambda k$ (`C-01`, `Hab-01`).
   - Análisis cualitativo de fase en `invariant_canvas` (`C-02`, `C-05`, `C-08`, `C-11`) con curvas y puntos objetivo exactos (ej. $4\sqrt{k}=2k \Rightarrow (4,8)$, trampa de población endógena en $r_1=3$ vs umbral inestable $r_2=10$).
   - Resolución simbólica y numérica exacta para Bernoulli Cobb-Douglas (`Hab-02`, `Hab-05`), tramos Leontief/Harrod-Domar (`H-01`, `Hab-04`, `Hab-07`), familia CES $Y=(a\sqrt{K}+\sqrt{L})^2$ (`Hab-06`, `Hab-08`), cambio tecnológico neutral de Hicks (`Hab-09`), arbitraje perfecto $i = q/p + \dot{p}/p$ (`C-07`), oferta laboral elástica (`C-09`), impuesto a la renta $s+(v-s)t$ (`C-10`) y salario rígido (`Hab-10`).
2. **Clúster de Riesgo D5 — Sintaxis SymPy filtrada en KaTeX (`60` ítems) y asteriscos `*` (`10` ítems):**
   - En `Q-Hab01-031`..`040`, `Q-Hab02-101`..`105`, `Q-Hab03-151`..`160`, `Q-Hab04-221`..`230`, `Q-Hab05-256`..`260`, `Q-Hab07-376`..`380`, `Q-Hab08-401`..`405` y `Q-Hab10-511`..`520`, el campo `detailed_solution` renderiza expresiones en formato SymPy dentro de `$...$` (ej. `$2.8*sqrt(k)-0.08*k$`, `$k^{1/2}(t)=(4)*exp(-4*t)+9$`, `$0.17/sqrt(r)$`, `$\dot{r}=0.3 \cdot 3\sqrt{r}-0.03 r=0.3*3*sqrt(r)-0.03*r$`). Esto no invalida la clave matemática, pero degrada la tipografía LaTeX/KaTeX en la retroalimentación paso a paso.
3. **Observaciones Menores Adicionales:**
   - **Solapamiento curricular `Hab-02` ↔ `Hab-05`:** Ambas competencias abordan la integración de Cobb-Douglas (*Solución Cobb-Douglas Bernoulli* vs. *Solución Explícita Cobb-Douglas*). Conviene diferenciar explícitamente en el sílabo o fusionar si se busca mayor concisión.
   - **Sesgo de longitud en `multiple_select` (`4/14` ítems, `28.57%`):** Detectado en `Q-C03-075`..`078`; revisar simetría de longitud entre opciones correctas y distractores.
   - **Escala porcentual en `error_rationale` (`Q-Hab01-031`..`035`):** Los valores de los distractores son matemáticamente exactos (ej. `0.4*k-0.08*k`), pero el texto de `error_rationale` interpola el numerador sin `%` o `/100` (ej. `con $\lambda=8$` o `en $s=40$`).

---

## 4. Acciones de Remediación Priorizadas

1. **[CRÍTICO / Plataforma]** Registrar y habilitar el tipo de pregunta `concept_matching` (y validar soporte completo M20) en el validador de ingesta de la plataforma para eliminar el error `"Invalid question type 'concept_matching'"`.
2. **[PRIORIDAD MEDIA / D5 KaTeX]** Convertir a LaTeX canónico (`\sqrt{...}`, `\exp(...)` o `e^{...}`, `\cdot` o yuxtaposición) las 60 expresiones SymPy filtradas dentro de `$...$` en `detailed_solution`, eliminando los 10 asteriscos crudos `*` en `Q-Hab03-151`..`160`.
3. **[PRIORIDAD BAJA / D1 & D2]** Revisar el solapamiento entre `Hab-02` y `Hab-05`, equilibrar la longitud de opciones en `Q-C03-075`..`078` (`multiple_select`) y formatear con `%` o `/100` la interpolación de tasas en `error_rationale` de `Q-Hab01-031`..`035`.

---

<details>
<summary>Metadatos Estructurados (JSON)</summary>

```json
{
  "course_metadata": {
    "course_id": "solow_m20_v1",
    "unit_title": "Solow M20 V1",
    "detected_objective": "Dominio y aplicación analítica integral del modelo de crecimiento económico de Solow (1956), estabilidad, proporciones fijas, familia CES, precios factoriales, cambio tecnológico y extensiones.",
    "total_competencies": 22,
    "total_questions": 540
  },
  "dimension_scores": {
    "architecture_granularity": {
      "score": 3.92,
      "max": 4.0,
      "feedback": "Estructura curricular con 22 competencias (1 Hechos, 11 Conceptos, 10 Habilidades). DAG acíclico y conexo (ciclos=False, comp. conexos=1, pares solapados=1: Hab-02<->Hab-05). ZPD: 22/22 competencias con calibración tri-banda ('easy', 'medium', 'hard')."
    },
    "assessment_quality": {
      "score": 5.0,
      "max": 5.0,
      "feedback": "Modalidad: MC7=0.0%, FIB=17.04%, MS=2.59%, BloomSup=80.37% (100.0% evocación activa/discriminación). Distractores: 28 evaluados con 100.0% cobertura de error_rationale (imposibles por dominio=0, claves corruptas=0, sesgo MS=28.57% en 4/14 ítems)."
    },
    "scaffolding_hints": {
      "score": 5.0,
      "max": 5.0,
      "feedback": "Andamiaje formativo: 100.0% de reactivos con 3 pistas socráticas escalonadas (100.0% pistas genuinas, 0.0% boilerplate Mad-Libs, 0.0% envenenadas). Unicidad diagnóstica real de rationales: 100.0% (rationales numéricos desconectados=0, advertencias clonadas/mudas=0)."
    },
    "instructional_alignment": {
      "score": 4.0,
      "max": 4.0,
      "feedback": "Alineación cognitiva de Bloom: 100.0% de habilidades prácticas (300/300) en niveles superiores (Apply+). Registro disciplinar auténtico y alta fidelidad con los contenidos fuente."
    },
    "technical_ergonomics": {
      "score": 1.8,
      "max": 2.0,
      "feedback": "Sintaxis KaTeX: 0 errores críticos (delimitadores balanceados, llaves cerradas, cero $$$). Ergonomía: 0 observaciones de prosa en \\text{...}, 0 identificadores crudos, pero 60 ítems con sintaxis SymPy filtrada en KaTeX y 10 asteriscos crudos '*' en detailed_solution."
    }
  },
  "penalties_applied": [],
  "raw_subtotal": 19.72,
  "final_score": 19.72,
  "quality_tier": "EXCELENTE (19.0 - 20.0 pts) — PLATINUM MASTERY",
  "mastery_path_readiness": {
    "mpri_score": 98.45,
    "mpri_max": 100.0,
    "mpri_tier": "GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo",
    "pillars": {
      "zpd_adaptive_progression": { "score": 20.0, "max": 20.0 },
      "retrieval_modality_and_anti_gaming": { "score": 20.0, "max": 20.0 },
      "socratic_scaffolding_lifeline": { "score": 25.0, "max": 25.0 },
      "diagnostic_remediation_alignment": { "score": 15.0, "max": 15.0 },
      "dag_and_interleaving_topology": { "score": 9.65, "max": 10.0 },
      "cognitive_ergonomics_and_framing": { "score": 8.8, "max": 10.0 }
    },
    "student_journey_verdict": "Trayectoria óptima de dominio adaptativo tri-banda con 100% de evocación activa y andamiaje socrático genuino; requiere únicamente habilitar 'concept_matching' en el validador de plataforma y limpiar la sintaxis SymPy en detailed_solution."
  },
  "discovered_lint_rules": [
    {
      "rule_id": "PLATFORM_UNSUPPORTED_M20_QUESTION_TYPE",
      "severity": "critical",
      "regex_pattern": "\"type\"\\s*:\\s*\"concept_matching\"",
      "description": "El validador de la plataforma rechaza el tipo de pregunta 'concept_matching' ('Invalid question type concept_matching'), bloqueando la ingesta de 90 reactivos M20.",
      "evidence_items": ["Q-C01-001", "Q-C01-002", "Q-C04-121", "Q-C06-301"]
    },
    {
      "rule_id": "SYMPY_PERCENTAGE_SCALE_MISMATCH_IN_RATIONALE",
      "severity": "info",
      "regex_pattern": "(?:\\\\lambda|s)=[1-9][0-9]?(?!%|/100)",
      "description": "El texto de error_rationale interpola el numerador entero de una tasa expresada en porcentaje/fracción (ej. s=40, \\lambda=8) sin el símbolo '%' ni '/100', aunque la expresión matemática del distractor sí usa el decimal correcto.",
      "evidence_items": ["Q-Hab01-031", "Q-Hab01-032", "Q-Hab01-033", "Q-Hab01-034", "Q-Hab01-035"]
    }
  ],
  "remediation_actions": [
    "Habilitar el tipo 'concept_matching' (y verificar el resto de modalidades M20) en el validador del backend de la plataforma.",
    "Formatear a LaTeX canónico las 60 expresiones SymPy filtradas dentro de $...$ en detailed_solution y reemplazar los 10 asteriscos crudos '*' en Q-Hab03-151..160.",
    "Evaluar la diferenciación o consolidación entre Hab-02 y Hab-05 para eliminar el solapamiento curricular.",
    "Equilibrar la longitud de opciones en Q-C03-075..078 (multiple_select) y normalizar el formato '%' en error_rationale de Q-Hab01-031..035."
  ]
}
```

</details>
