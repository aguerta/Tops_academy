# Auditoría Agéntica Exhaustiva de Calidad Pedagógica, Psicométrica y Path-to-Mastery v2.0

**Curso:** `estadistica_3_test_k3` — *Estadistica 3 Test K3*  
**Fecha de Auditoría:** 2026-11-27 (Re-auditoría agéntica profunda sobre `courses/estadistica_3_test_k3.json`)  
**Calificación Final QM-OSCQR:** **17.70 / 20.00**  
**Tier de Calidad:** **EXCELENTE (17.0 - 20.0 pts)**  
**Mastery Path Readiness Index (MPRI):** **90.80 / 100.00** — *GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo*

---

## 1. Resumen Ejecutivo y Hallazgos de Inspección Directa

El curso **`estadistica_3_test_k3`** (**22 competencias**: 1 Hecho `[H]`, 13 Conceptos `[C]`, 8 Habilidades `[Hab]`; **666 reactivos**) posee una arquitectura sólida sin monocultivo de opción múltiple (`MC7 = 0.00%`), calibración ZPD tri-banda completa (`222` ítems por banda `easy`/`medium`/`hard`) y `100.00%` de acuerdo en Stage-5 Blind Judges (`145/145`).

Sin embargo, la **inspección agéntica directa** de muestras amplias en `courses/estadistica_3_test_k3.json` (incluyendo ítems `medium`, `hard`, `multiple_select`, `fill_in_the_blank`, `concept_matching`, `unstructured_model` y `adversarial_break`) reveló **defectos reales no capturados por los linters deterministas**, que obligan a recalibrar la calificación desde `19.84` a **`17.70 / 20.00`** y el MPRI desde `99.30` a **`90.80 / 100.00`**:

1. **Corrupción aritmética por truncamiento en `Hab-04` (`Q-Hab04-350`, `Q-Hab04-351`):** El promedio simple $(23+16)/2 = 19.5$ y $(18+13)/2 = 15.5$ fue truncado a entero (`19` y `15`), generando igualdades aritméticamente falsas en distractores (`=19`) y contradicciones explícitas en enunciados y soluciones (`"resultado 19, contraste 19"`, `"=15 ... (no 15)"`, `"se obtiene 19, distinto del promedio simple 19"`).
2. **Spoilers numéricos en enunciados (`stem`):** Múltiples ítems anticipan el valor final o el contraste entre paréntesis (`"=15 ... (no 15)"`, `"y regreso 0.75"`, `"(término 16, total 24)"`, `"(donde 490 es el numerador combinado)"`), reduciendo el esfuerzo de evocación.
3. **Clonación paramétrica en bloques hermanos:** Tripletas de ítems (`Q-C01-019..021`, `Q-C04-175..177`, `Q-C05-199..201`, `Q-Hab08-660..662`) repiten exactamente las mismas opciones, pistas y soluciones cambiando solo constantes numéricas.
4. **Goodharting moderado de Bloom (`Evaluate`):** Ítems `multiple_select` de propiedades definitorias (`Q-C01-025`, `Q-C01-026`, `Q-C13-590..592`) y detección de inversión de fronteras en un solo paso (`Q-Hab07-625`, `Q-Hab07-626`) están etiquetados como `Evaluate` cuando corresponden a `Understand`/`Analyze`.

---

## 2. Evaluación Detallada por Dimensiones (Rúbrica QM-OSCQR / 20.0)

| Dimensión | Puntaje | Máximo | Estado / Ajuste Agéntico |
| :--- | :---: | :---: | :--- |
| **D1. Arquitectura Curricular, Topología DAG y Calibración ZPD** | **3.75** | 4.00 | DAG limpio y ZPD 3-bandas; `-0.25` por solapamiento léxico y clonación intra-bloque |
| **D2. Calidad Psicométrica, Modalidad de Evocación y Anti-Gaming** | **4.10** | 5.00 | `MC7=0.00%`; **`-0.90`** por truncamiento `19.5->19` en `Hab-04`, spoilers en `stem` y clones |
| **D3. Andamiaje Socrático Progresivo y Remediación Diagnóstica** | **4.40** | 5.00 | Pistas genuinas sin Mad-Libs; **`-0.60`** por pistas clonadas/reveladoras y contradicción en `Hab-04` |
| **D4. Alineación Instruccional, Taxonomía de Bloom y Pureza de Dominio** | **3.55** | 4.00 | Dominio puro; **`-0.45`** por Goodharting de etiquetas `Evaluate` en `MS`/`adversarial_break` |
| **D5. Accesibilidad, Ergonomía Cognitiva en UI y Sintaxis KaTeX** | **1.90** | 2.00 | KaTeX limpio; **`-0.10`** por micro-defectos (`..`, `N0.65`, `7-(4)`) |
| **Subtotal Bruto** | **17.70** | **20.00** | — |
| **Penalizaciones Duras Automáticas** | **0.00** | — | Sin infracciones duras (`bank < 3`, `hints=0`, `poisoning`, `vacuous_quantifier`, `memorizable`) |
| **Calificación Final** | **17.70** | **20.00** | **EXCELENTE (17.0 - 20.0 pts)** |

### D1. Arquitectura Curricular, Topología DAG y Calibración ZPD (3.75 / 4.00)
- **Topología DAG:** Acíclico y conexo (`has_cycle = false`, `connected_components_count = 1`, `max_dag_depth = 7`, `inverted_prerequisite_edges = 0`, `isolated_competencies = 0`).
- **Calibración ZPD:** `22/22` competencias con 3 bandas (`easy = 222`, `medium = 222`, `hard = 222`).
- **Observación (`-0.25 pts`):** 2 pares marcados por solapamiento léxico (`C-06 <-> C-08` y `Hab-07 <-> Hab-08`, aunque matemáticamente distintos y bien ordenados) y redundancia estructural entre ítems hermanos dentro de la misma competencia.

### D2. Calidad Psicométrica, Modalidad de Evocación y Anti-Gaming (4.10 / 5.00)
- **Fortalezas:** `MC7 = 0.00%`, `FIB = 10.36%`, `MS = 17.57%`, modalidades Bloom Superior = `72.07%`; `100.00%` cobertura de `error_rationale` en `468` distractores; `0` multiplicadores mágicos `1.333x`.
- **Defectos reales detectados (`-0.90 pts`):**
  - **Truncamiento aritmético en `Hab-04` (`-0.35`):** En `Q-Hab04-350`, $\frac{1}{2}((18+5)+(11+5)) = 19.5$, pero la opción `O2` afirma `$\mathbb{E}[Y'\mid A_1]=\frac{(18+5)+(11+5)}{2}=19$`. En `Q-Hab04-351`, $\frac{1}{2}((13+5)+(8+5)) = 15.5$ fue truncado a `15`.
  - **Spoilers en `stem` (`-0.30`):** Ej. `Q-Hab04-351` (`"esperanza condicional perturbada \mathbb{E}[Y+5\mid A_1]=15 ... (no 15)"`), `Q-C13-592` (`"y regreso 0.75"`), `Q-C08-262` (`"(término 16, total 24)"`), `Q-C01-020` (`"(2^4=16, frente a 9)"`).
  - **Clonación paramétrica y sesgo MS (`-0.25`):** `Q-C01-019..021`, `Q-C04-175..177` (con sesgo de longitud MS `2.56%`), `Q-C05-199..201`, `Q-Hab08-660..662`.

### D3. Andamiaje Socrático Progresivo y Remediación Diagnóstica (4.40 / 5.00)
- **Fortalezas:** `100.00%` de reactivos con 3–5 pistas genuinas (`0.00%` Mad-Libs, `0.00%` envenenadas).
- **Defectos reales detectados (`-0.60 pts`):**
  - Pistas clonadas entre tripletas de ítems y pistas que regalan el atajo completo (ej. `Q-Hab03-305`, pista 3: `"Verifique que el resultado coincide con la varianza de Bin(40, 0.5*0.65)"`).
  - Solución contradictoria en `Q-Hab04-350/351` (`"se obtiene 19, distinto del promedio simple 19"`).
  - `33` `misconception_warning` estáticos sin instanciar parámetros (`Hab-05`, `Hab-06`, `C-13`, `Hab-08`), incluyendo advertencias del caso simétrico `(N/2)^2` en ítems asimétricos (`Q-Hab08-643` con $p=3/7, q=4/7$).

### D4. Alineación Instruccional, Taxonomía de Bloom y Pureza de Dominio (3.55 / 4.00)

| Métrica Determinista D4 (Bloom & ZPD) | Valor Observado | Referencia / Umbral | Estado |
| :--- | :---: | :---: | :--- |
| **Piso Bloom Expected (`adaptive_bloom_floor`)** | **3.84** | Mezcla curricular `Fact/Concept/Skill` | Cumplido |
| **Índice Bloom Real Generado (`bloom_weighted_index`)** | **4.03** | $\ge 3.84$ (`gap = 0.00`) | **ÉLITE (con inflación parcial)** |
| **Habilidades en `Apply+`** | **100.00%** (`288/288`) | $\ge 90.00\%$ | Excelente |
| **Reactivos en `Apply+`** | **91.44%** | — | Excelente |
| **Reactivos en `Analyze + Evaluate` (`bloom_superior_pct`)** | **73.57%** | $\ge 65.00\%$ | Élite (sobre-etiquetado en MS) |
| **Violaciones de Coherencia `modalidad × bloom`** | **0** (linter) | Revisión agéntica: `MS`/`AB` sobre-etiquetados | **-0.45 pts (Goodharting)** |

### D5. Accesibilidad, Ergonomía Cognitiva en UI y Sintaxis KaTeX (1.90 / 2.00)
- `0` errores críticos de KaTeX, `0` prosa en `\text{...}`, `0` identificadores crudos de Python.
- **Observación (`-0.10 pts`):** Doble punto final `..` en `error_rationale` de `phase2_assumptions` (`is_required: true`) en todos los `unstructured_model`, falta de `\cdot` en `N0.65` (`Q-Hab03-305`, `Q-Hab03-306`, `Q-Hab03-315`) y expresión sin simplificar `7-(4)` (`Q-Hab06-532`).

---

## 3. Evidencia Verbatim de Hallazgos Críticos

```json
// Q-Hab04-350 (líneas 32677, 32683, 32763-32765) — Truncamiento 19.5 -> 19
"stem": "Formule el modelo completo de $\\mathbb{E}[Y'\\mid A_1]$ para la variable desplazada $Y'=Y+5$ cuando $Y(\\omega_1)=18$, $Y(\\omega_2)=11$, $\\mathbb{P}(\\{\\omega_1\\})=3/11$, $\\mathbb{P}(\\{\\omega_2\\})=4/11$, $\\mathbb{P}(A_1)=7/11$ (resultado $19$, contraste $19$):"
"detailed_solution": "Paso 1: ... Paso 2: Evaluando $\\frac{3(18+5)+4(11+5)}{7}$ se obtiene $19$, distinto del promedio simple $19$."
"O2": "$\\mathbb{E}[Y'\\mid A_1]=\\frac{(18+5)+(11+5)}{2}=19$"

// Q-Hab04-351 (líneas 32797, 32803) — Spoiler + Truncamiento 15.5 -> 15
"stem": "Construya el modelo estructurado de la esperanza condicional perturbada $\\mathbb{E}[Y+5\\mid A_1]=15$ sobre el átomo $A_1$ de probabilidad $5/7$ con realizaciones $13$, $8$ y pesos $2/7$, $3/7$ (no $15$):"

// Q-Hab03-305 (línea 28501, 28532) — Pista reveladora + tipografía N0.65
"hints[2]": "Verifique que el resultado coincide con la varianza de $\\operatorname{Bin}(40,0.5\\cdot 0.65)$."
"error_rationale": "Omite $\\mathbb{E}[N0.65(1-0.65)]$ conservando únicamente $0.65^2\\operatorname{Var}(N)$ para $m=40$."
```

---

## 4. Mastery Path Readiness Index (`MPRI`: 90.80 / 100.00)

| Pilar MPRI | Puntaje | Máximo | Detalle Métrico Clave |
| :--- | :---: | :---: | :--- |
| **1. `zpd_adaptive_progression`** | **19.00** | 20.00 | 22/22 competencias tri-banda; Habilidades `Apply+` = `100.00%`; **`bloom_weighted_index` = 4.03** vs **`adaptive_bloom_floor` = 3.84** (`gap = 0.00`, `-1.0` por Goodharting `Evaluate` en MS). |
| **2. `retrieval_modality_and_anti_gaming`** | **17.00** | 20.00 | `MC7 = 0.00%`, `FIB = 10.36%`, `MS = 17.57%`, `BloomSup = 72.07%`; `-3.0` por truncamiento `Hab-04`, spoilers en `stem` y clonación en tripletas. |
| **3. `socratic_scaffolding_lifeline`** | **22.50** | 25.00 | Pistas genuinas sin Mad-Libs; `-2.5` por pistas clonadas/reveladoras y 33 `misconception_warning` estáticos. |
| **4. `diagnostic_remediation_alignment`** | **13.50** | 15.00 | `100.00%` cobertura; `-1.5` por igualdad falsa `=19`/`=15` en `O2` de `Q-Hab04-350/351` y doble punto `..`. |
| **5. `dag_and_interleaving_topology`** | **9.30** | 10.00 | DAG acíclico y conexo (`max_depth = 7`, `0` aristas invertidas); `-0.70` por 2 pares con solapamiento léxico. |
| **6. `cognitive_ergonomics_and_framing`** | **9.50** | 10.00 | KaTeX limpio; `-0.50` por micro-defectos tipográficos (`..`, `N0.65`, `7-(4)`). |
| **Total MPRI** | **90.80** | **100.00** | **GOLD MASTERY PATH (85-100)** |

---

## 5. Acciones de Remediación Prioritarias

1. **[CRÍTICO / Aritmética `Hab-04`]**: Corregir el truncamiento a entero del promedio simple en `Q-Hab04-350` (`19.5`, no `19`) y `Q-Hab04-351` (`15.5`, no `15`), y eliminar el spoiler `=15 ... (no 15)` del `stem` de `Q-Hab04-351`.
2. **[ALTO / Anti-Gaming]**: Remover paréntesis spoiler en `stem` (`(resultado X, contraste Y)`, `(término 16, total 24)`, `y regreso 0.75`) y diversificar las tripletas clonadas (`Q-C01-019..021`, `Q-C04-175..177`, `Q-C05-199..201`, `Q-Hab08-660..662`).
3. **[MEDIO / Taxonomía Bloom]**: Recalibrar `bloom_taxonomy_level` de `Evaluate` a `Understand`/`Analyze` en `Q-C01-025/026`, `Q-C13-590..592` y `Q-Hab07-625/626` para evitar Goodharting.
4. **[BAJO / Pulido Tipográfico]**: Eliminar el doble punto `..` en `phase2_assumptions`, insertar `\cdot` en `N\cdot 0.65` (`Hab-03`) y contextualizar `misconception_warning` en ítems asimétricos (`Q-Hab08-643`).

---

<details>
<summary>Metadatos Estructurados (JSON)</summary>

```json
{
  "course_metadata": {
    "course_id": "estadistica_3_test_k3",
    "unit_title": "Estadistica 3 Test K3",
    "detected_objective": "Dominio y aplicación analítica integral de Estadistica 3 Test K3",
    "total_competencies": 22,
    "total_questions": 666,
    "bloom_index": {
      "weighted_index": 4.03,
      "adaptive_floor": 3.84,
      "gap": 0.0,
      "apply_plus_pct": 91.44,
      "superior_pct": 73.57,
      "tier": "ÉLITE",
      "coherence_violations_count": 0
    }
  },
  "dimension_scores": {
    "architecture_granularity": {
      "score": 3.75,
      "max": 4.0,
      "feedback": "22 competencias (1 Hechos, 13 Conceptos, 8 Habilidades), DAG acíclico conexo, 22/22 ZPD tri-banda. Deducción de -0.25 por 2 pares con solapamiento léxico y clonación estructural intra-bloque."
    },
    "assessment_quality": {
      "score": 4.1,
      "max": 5.0,
      "feedback": "MC7=0.0%, 100% evocación activa/discriminación. Deducción de -0.90 por truncamiento aritmético 19.5->19 y 15.5->15 en Q-Hab04-350/351, spoilers numéricos en stem, clonación paramétrica en tripletas y sesgo MS 2.56%."
    },
    "scaffolding_hints": {
      "score": 4.4,
      "max": 5.0,
      "feedback": "100% con 3-5 pistas reales sin Mad-Libs ni envenenamiento. Deducción de -0.60 por pistas clonadas/reveladoras (Q-Hab03-305), contradicción en solución de Q-Hab04-350/351 y 33 misconception_warning estáticos."
    },
    "instructional_alignment": {
      "score": 3.55,
      "max": 4.0,
      "feedback": "Índice Bloom Real 4.03 vs Piso Adaptativo 3.84 (100% habilidades en Apply+). Deducción de -0.45 por Goodharting moderado de etiquetas Evaluate en MS de C-01/C-13 y AB de Hab-07."
    },
    "technical_ergonomics": {
      "score": 1.9,
      "max": 2.0,
      "feedback": "KaTeX limpio sin errores críticos. Deducción de -0.10 por doble punto '..' en unstructured_model, 'N0.65' sin \\cdot en Hab-03 y '7-(4)' sin simplificar en Hab-06."
    }
  },
  "penalties_applied": [],
  "raw_subtotal": 17.7,
  "final_score": 17.7,
  "quality_tier": "EXCELENTE (17.0 - 20.0 pts)",
  "mastery_path_readiness": {
    "mpri_score": 90.8,
    "mpri_max": 100.0,
    "mpri_tier": "GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo",
    "pillars": {
      "zpd_adaptive_progression": { "score": 19.0, "max": 20.0 },
      "retrieval_modality_and_anti_gaming": { "score": 17.0, "max": 20.0 },
      "socratic_scaffolding_lifeline": { "score": 22.5, "max": 25.0 },
      "diagnostic_remediation_alignment": { "score": 13.5, "max": 15.0 },
      "dag_and_interleaving_topology": { "score": 9.3, "max": 10.0 },
      "cognitive_ergonomics_and_framing": { "score": 9.5, "max": 10.0 }
    },
    "student_journey_verdict": "Certificado para dominio adaptativo con corrección prioritaria de truncamiento en Q-Hab04-350/351 y limpieza de spoilers numéricos en enunciados."
  },
  "discovered_lint_rules": [
    {
      "rule_id": "R-TRUNCATED-DISTRACTOR-EQ",
      "severity": "critical",
      "regex_pattern": "distinto del promedio simple (\\d+)",
      "description": "Truncamiento a entero del promedio simple en Hab-04 generando igualdades falsas en distractores y contradicción en stem/detailed_solution.",
      "evidence_items": ["Q-Hab04-350", "Q-Hab04-351"]
    },
    {
      "rule_id": "R-STEM-NUMERIC-SPOILER",
      "severity": "warning",
      "regex_pattern": "\\((?:resultado|contraste|término|total|numerador|no)\\s+\\d+",
      "description": "Paréntesis en stem que filtran el resultado esperado o el contraste numérico.",
      "evidence_items": ["Q-Hab04-350", "Q-Hab04-351", "Q-C08-262", "Q-Hab04-325"]
    },
    {
      "rule_id": "R-DOUBLE-PERIOD-RATIONALE",
      "severity": "info",
      "regex_pattern": "\\.\\.$",
      "description": "Doble punto final en error_rationale autogenerado de phase2_assumptions (is_required=true) dentro de ítems unstructured_model.",
      "evidence_items": ["Q-C04-154", "Q-Hab01-055", "Q-Hab03-315", "Q-Hab04-350"]
    }
  ],
  "remediation_actions": [
    "Corregir truncamiento a entero del promedio simple en Q-Hab04-350 (19.5) y Q-Hab04-351 (15.5) y quitar spoiler '=15 ... (no 15)'.",
    "Remover paréntesis spoiler en stem y diversificar tripletas clonadas (Q-C01-019..021, Q-C04-175..177, Q-C05-199..201, Q-Hab08-660..662).",
    "Recalibrar etiquetas Bloom infladas en Evaluate (Q-C01-025/026, Q-C13-590..592, Q-Hab07-625/626).",
    "Eliminar '..' en phase2_assumptions, agregar \\cdot en N*0.65 (Hab-03) y contextualizar misconception_warning en Q-Hab08-643."
  ]
}
```

</details>
