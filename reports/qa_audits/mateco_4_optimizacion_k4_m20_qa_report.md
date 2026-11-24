# Reporte de Auditoría QA — `mateco_4_optimizacion_k4_m20`

> [!WARNING]
> **CURSO RETIRADO DE LA PLATAFORMA**: Este curso fue eliminado de la plataforma interactiva el **2026-11-24 15:02:49**. Este informe de auditoría se conserva exclusivamente como registro histórico y pedagógico ('legacy').

**Estado en Plataforma:** ELIMINADO  
**Fecha de Eliminación:** 2026-11-24 15:02:49  
**Curso:** Mateco 4 Optimizacion K4 M20 (`mateco_4_optimizacion_k4_m20`)  
**Fecha de Auditoría:** 2026-11-24  
**Calificación Final QM-OSCQR:** **19.58 / 20.00** — **EXCELENTE (19.0 - 20.0 pts) — PLATINUM MASTERY**  
**Mastery Path Readiness Index (MPRI):** **98.17 / 100.00** — **GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo**  
**Risk Score:** `0.76` | **Penalizaciones Duras:** `0.00` (0 activadas) | **Stage-5 Blind Judges:** `143/143` (`100.00%` acuerdo, `0` desacuerdos sin reparar)

---

## 1. Resumen Ejecutivo y Cobertura del Banco

El curso `mateco_4_optimizacion_k4_m20` comprende **31 competencias** (`2` Hechos, `11` Conceptos, `18` Habilidades) y **1,452 reactivos** (`36` a `64` por competencia, `0` competencias subpobladas y `0` preguntas huérfanas). La distribución de modalidades cognitivas elimina por completo el monocultivo de opción múltiple pasiva (`MC7 = 0.00%`), operando al `100.00%` con modalidades de evocación activa, discriminación condicional y evaluación de orden superior:

| Modalidad de Interacción | Cantidad | Porcentaje | Rol Cognitivo |
| :--- | :---: | :---: | :--- |
| `adversarial_break` | 324 | 22.31% | Refutación y contraejemplos (Bloom Superior) |
| `open_symbolic` | 300 | 20.66% | Evocación simbólica abierta (Bloom Superior) |
| `unstructured_model` | 220 | 15.15% | Modelado estructurado multifase (Bloom Superior) |
| `fill_in_the_blank` | 200 | 13.77% | Evocación activa numérica/algebraica (`FIB`) |
| `multiple_select` | 160 | 11.02% | Discriminación condicional múltiple (`MS`) |
| `proof_dag` | 136 | 9.37% | Construcción lógica de demostraciones (Bloom Superior) |
| `invariant_canvas` | 76 | 5.23% | Manipulación gráfica e invariantes (Bloom Superior) |
| `concept_matching` | 36 | 2.48% | Emparejamiento conceptual (Bloom Superior) |
| `multiple_choice_7_options` | 0 | 0.00% | Reconocimiento pasivo (`MC7`) |

---

## 2. Evaluación Determinista por Dimensiones (Rúbrica QM-OSCQR / 20.00)

| Dimensión | Puntaje | Máximo | Estado | Hallazgos Clave |
| :--- | :---: | :---: | :---: | :--- |
| **D1. Arquitectura Curricular, Topología DAG y Calibración ZPD** | **3.60** | 4.00 | Sólido | 31 competencias (`2` Hechos, `11` Conceptos, `18` Habilidades). DAG acíclico y conexo (`ciclos=False`, `comp_conexos=1`, profundidad máxima `7`, `0` aristas invertidas). Calibración ZPD tri-banda (`easy`: 504, `medium`: 474, `hard`: 474) en `31/31` competencias. Deducción de `-0.40` por `5` pares de solapamiento curricular (`C-02<->C-08`, `Hab-06<->Hab-18`, `Hab-07<->Hab-21`, `C-12<->C-13`, `C-08<->Hab-04`). |
| **D2. Calidad Psicométrica, Modalidad de Evocación y Anti-Gaming** | **4.99** | 5.00 | Élite | `100.00%` evocación activa/discriminación (`MC7=0.00%`, `FIB=13.77%`, `MS=11.02%`, `BloomSup=75.21%`). `452` distractores con `100.00%` cobertura de `error_rationale`, `0` imposibles por dominio, `0` claves corruptas, `0` multiplicadores mágicos y `0` competencias memorizables. Leve sesgo de longitud en `8/160` ítems `MS` (`5.00%`) y `1` parámetro decorativo inerte (`Q-C02-083`: `"(no $y=19$)"`). |
| **D3. Andamiaje Socrático Progresivo y Remediación Diagnóstica** | **5.00** | 5.00 | Élite | `100.00%` de reactivos con `3` a `5` pistas socráticas genuinas (`0.00%` boilerplate Mad-Libs, `0.00%` envenenamiento anti-socrático, `0.00%` fuga de respuesta). `100.00%` de unicidad de `error_rationale` por slot (`54/54`). Se observan `58` advertencias menores de constantes no instanciadas en `misconception_warning`. |
| **D4. Alineación Instruccional, Taxonomía de Bloom y Pureza de Dominio** | **3.99** | 4.00 | Élite | `100.00%` de habilidades prácticas (`960/960`) en `Apply+`. **Piso Bloom Expected (`adaptive_bloom_floor`):** `3.89 / 5.00` vs **Índice Bloom Real Generado (`bloom_weighted_index`):** `3.90 / 5.00` (brecha `0.00`, `Apply+`: `92.98%`, `Analyze+Evaluate`: `64.26%`, Tier: `ÉLITE`, `0` incoherencias `modalidad × bloom`). |
| **D5. Accesibilidad, Ergonomía Cognitiva en UI y Sintaxis KaTeX** | **2.00** | 2.00 | Élite | `0` errores críticos de sintaxis KaTeX (`$` balanceados, llaves cerradas, `0` `$$$`, `0` `{{...}}`, `0` `SymPy` en KaTeX, `0` residuos de plantilla). Se detectaron `6` colisiones de signos sin simplificar (`+-k`) en `C-09` y `2` comandos LaTeX fusionados en `misconception_warning` (`\betaj`, `\rhot`). |
| **Subtotal Bruto** | **19.58** | **20.00** | — | — |
| **Penalizaciones Duras** | **0.00** | — | Limpio | Ninguna penalización dura activada. |
| **Calificación Final** | **19.58** | **20.00** | **PLATINUM** | **EXCELENTE (19.0 - 20.0 pts) — PLATINUM MASTERY** |

---

## 3. Mastery Path Readiness Index (`MPRI`: 98.17 / 100.00)

| Pilar Cognitivo y de Plataforma | Puntaje | Máximo | Cumplimiento | Notas de Verificación |
| :--- | :---: | :---: | :---: | :--- |
| **1. `zpd_adaptive_progression`** | **20.00** | 20.00 | 100.00% | `31/31` competencias con bandas `easy`/`medium`/`hard`; `100.00%` de Habilidades en `Apply+`; **Piso Bloom Expected (`adaptive_bloom_floor`): `3.89`** vs **Índice Bloom Real Generado (`bloom_weighted_index`): `3.90`** (brecha `0.00`, Tier `ÉLITE`). |
| **2. `retrieval_modality_and_anti_gaming`** | **19.92** | 20.00 | 99.60% | `100.00%` evocación activa/discriminación; alta entropía de arquetipos (`>= 33` esqueletos distintos); `5.00%` (`8/160`) de sesgo leve de longitud en `MS`. |
| **3. `socratic_scaffolding_lifeline`** | **25.00** | 25.00 | 100.00% | `100.00%` pistas socráticas genuinas (`3–5` por reactivo), `0` pistas envenenadas y `0` boilerplate. |
| **4. `diagnostic_remediation_alignment`** | **15.00** | 15.00 | 100.00% | `452/452` distractores con `error_rationale` diagnóstico único por slot (`100.00%`), `0` multiplicadores mágicos y `0` rationales numéricos fantasma. |
| **5. `dag_and_interleaving_topology`** | **8.25** | 10.00 | 82.50% | DAG acíclico y conexo en orden topológico válido; penalización menor por `5` pares con solapamiento léxico/temático entre Cálculo de Variaciones y Control Óptimo. |
| **6. `cognitive_ergonomics_and_framing`** | **10.00** | 10.00 | 100.00% | Sin `\text{prosa}` desbordante, sin identificadores Python crudos en LaTeX y sin contaminación de dominios ajenos. |
| **Total MPRI** | **98.17** | **100.00** | **98.17%** | **GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo** |

---

## 4. Verificación Semántica Adaptativa sobre Risk Clusters

1. **Colisión de signos algebraicos en `C-09` (`katex_issues`: 6 ítems):**
   - Ítems `Q-C09-439`, `Q-C09-440`, `Q-C09-441`, `Q-C09-463`, `Q-C09-464`, `Q-C09-465` presentan expresiones como `q=23-8p+-5\dot{p}`, `q=40-4p+-6\dot{p}` y `q=32-6p+-2\dot{p}` tanto en el `stem` como en `detailed_solution` y opciones. Aunque no rompen el parser KaTeX ni alteran la validez matemática, degradan la limpieza tipográfica. Además, en `Q-C09-439/440/441` (`phase2_assumptions`), el `error_rationale` de opciones requeridas termina en doble punto (`".."`).
2. **Constantes estáticas no instanciadas en `misconception_warning` (`scaffolding_flaws`: 58 ítems en 10 competencias):**
   - Verificado en `Q-Hab01-277` (el enunciado usa $x(2)=37$ pero `misconception_warning` cita `t=4`), `Q-Hab02-329` (`|H_F|=4>0` fijo frente a `2x^2+qx\dot{x}+2\dot{x}^2`), `Q-Hab04-870` (`F_{\dot{x}}=6\dot{x}` fijo frente a `8\dot{x}^2+3x+4\dot{x}`), `Q-Hab05-493`, `Q-Hab06-521`, `Q-Hab09-933`, `Q-Hab18-1245`, `Q-Hab19-1294`, `Q-Hab20-1361` y `Q-Hab21-1405`. No sabotean el intento del estudiante, pero restan coherencia paramétrica a la advertencia final.
   - **Hallazgo adicional de renderizado LaTeX:** En `Q-Hab05-493` (`misconception_warning`) aparece `\frac{4\alpha}{(\betaj)^2}` (`\betaj` sin espacio) y en `Q-Hab09-933` aparece `e^{-\rhot}` (`\rhot` sin espacio), lo que provoca secuencias de control indefinidas en KaTeX.
3. **Solapamiento curricular en el DAG (`duplicate_competencies`: 5 pares):**
   - `C-02` vs `C-08`, `C-08` vs `Hab-04`, `C-12` vs `C-13`, `Hab-06` vs `Hab-18`, `Hab-07` vs `Hab-21`. Al inspeccionar las descripciones, `C-02` cubre condiciones de punto final generales mientras `C-08` y `Hab-04` cubren transversalidad en estado final libre e instante final libre; `Hab-06` trata inversión con costos de ajuste y `Hab-18` publicidad, por lo que son diferenciables pedagógicamente aunque comparten estructura léxica.
4. **Anti-Gaming y Sesgo MS (`Q-C02-083` y 8 ítems `MS`):**
   - `Q-C02-083` incluye el parámetro decorativo `"(no $y=19$)"` y `8/160` ítems `MS` (`5.00%`, ej. `Q-C04-199`, `Q-C09-460`, `Q-C13-766`, `Q-C08-803`) muestran ligero sesgo de longitud entre opciones correctas e incorrectas.

---

## 5. Acciones de Remediación Prioritarias y Reglas Aprendidas

1. **Normalizar signos `+-` en `C-09`** (`Q-C09-439` a `441`, `463` a `465`) reemplazando `+-k` por `-k` mediante formateador algebraico de coeficientes.
2. **Corregir secuencias LaTeX fusionadas** (`\betaj` $\to$ `\beta j`, `\rhot` $\to$ `\rho t`) en `misconception_warning` de `Hab-05` y `Hab-09`, e instanciar dinámicamente los parámetros de `misconception_warning` en las `10` habilidades afectadas (`58` reactivos).
3. **Pulir detalles menores de D2/D1**: eliminar el parámetro decorativo en `Q-C02-083`, equilibrar la longitud de opciones en los `8` ítems `MS` marcados y precisar los títulos/descripciones de los `5` pares con solapamiento léxico si se realiza una revisión curricular futura.
4. **Nueva regla candidata (`LATEX_MERGED_CONTROL_SEQUENCE`)**: Detectar comandos griegos concatenados sin espacio con otra letra (ej. `\betaj`, `\rhot`) que rompen KaTeX aun con delimitadores `$` balanceados.

---

<details>
<summary>Metadatos Estructurados (JSON)</summary>

```json
{
  "course_metadata": {
    "course_id": "mateco_4_optimizacion_k4_m20",
    "unit_title": "Mateco 4 Optimizacion K4 M20",
    "detected_objective": "Dominio y aplicación analítica integral de Cálculo de Variaciones y Control Óptimo en economía y optimización dinámica",
    "total_competencies": 31,
    "total_questions": 1452,
    "bloom_index": {
      "weighted_index": 3.9,
      "adaptive_floor": 3.89,
      "gap": 0.0,
      "apply_plus_pct": 92.98,
      "superior_pct": 64.26,
      "tier": "ÉLITE",
      "coherence_violations_count": 0
    }
  },
  "dimension_scores": {
    "architecture_granularity": {
      "score": 3.6,
      "max": 4.0,
      "feedback": "Estructura curricular con 31 competencias (2 Hechos, 11 Conceptos, 18 Habilidades). DAG acíclico y conexo (ciclos=False, comp. conexos=1, pares solapados=5). ZPD: 31/31 competencias con calibración tri-banda ('easy', 'medium', 'hard')."
    },
    "assessment_quality": {
      "score": 4.99,
      "max": 5.0,
      "feedback": "Modalidad: MC7=0.0%, FIB=13.77%, MS=11.02%, BloomSup=75.21% (100.0% evocación activa/discriminación). Distractores: 452 evaluados con 100.0% cobertura de error_rationale (imposibles por dominio=0, claves corruptas=0, sesgo MS=5.0%)."
    },
    "scaffolding_hints": {
      "score": 5.0,
      "max": 5.0,
      "feedback": "Andamiaje formativo: 100.0% de reactivos con 3 a 5 pistas socráticas escalonadas (100.0% pistas genuinas, 0.0% boilerplate Mad-Libs, 0.0% envenenadas). Unicidad diagnóstica real de rationales: 100.0% (rationales numéricos desconectados=0, advertencias clonadas/mudas=0)."
    },
    "instructional_alignment": {
      "score": 3.99,
      "max": 4.0,
      "feedback": "Alineación cognitiva de Bloom: 100.0% de habilidades prácticas en Apply+; Índice Bloom Real Generado: 3.90/5.0 vs Piso Bloom Expected (Adaptativo): 3.89/5.0 (64.26% Analyze+Evaluate, tier: ÉLITE, incoherencias=0)."
    },
    "technical_ergonomics": {
      "score": 2.0,
      "max": 2.0,
      "feedback": "Sintaxis KaTeX: 0 errores críticos (delimitadores balanceados, llaves cerradas, cero $$$). Ergonomía: 0 observaciones de prosa en \\text{...}, 0 identificadores crudos, 0 colisiones por concatenación, 0 identidades tautológicas, 0 formatos flotantes/asteriscos crudos y 0 residuos de plantilla/reemplazo."
    }
  },
  "penalties_applied": [],
  "raw_subtotal": 19.58,
  "final_score": 19.58,
  "quality_tier": "EXCELENTE (17-20)",
  "mastery_path_readiness": {
    "mpri_score": 98.17,
    "mpri_max": 100.0,
    "mpri_tier": "GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo",
    "pillars": {
      "zpd_adaptive_progression": { "score": 20.0, "max": 20.0 },
      "retrieval_modality_and_anti_gaming": { "score": 19.92, "max": 20.0 },
      "socratic_scaffolding_lifeline": { "score": 25.0, "max": 25.0 },
      "diagnostic_remediation_alignment": { "score": 15.0, "max": 15.0 },
      "dag_and_interleaving_topology": { "score": 8.25, "max": 10.0 },
      "cognitive_ergonomics_and_framing": { "score": 10.0, "max": 10.0 }
    },
    "student_journey_verdict": "Curso certificado en banda Platinum Mastery (19.58/20.00) y Gold Mastery Path (98.17/100.00), apto para estudio autónomo adaptativo con pulido menor recomendado en signos +- de C-09, secuencias LaTeX fusionadas (\\betaj, \\rhot) e instanciación de misconception_warning."
  },
  "discovered_lint_rules": [
    {
      "rule_id": "LATEX_MERGED_CONTROL_SEQUENCE",
      "severity": "warning",
      "regex_pattern": "\\\\(alpha|beta|gamma|delta|theta|lambda|mu|rho|sigma|pi|phi|psi|omega)[a-zA-Z]+",
      "description": "Detecta comandos de letras griegas en LaTeX fusionados sin espacio con la variable siguiente (ej. \\betaj, \\rhot), lo que causa errores de secuencia indefinida al renderizar en KaTeX.",
      "evidence_items": ["Q-Hab05-493", "Q-Hab09-933"]
    }
  ],
  "remediation_actions": [
    "Simplificar colisiones de signos algebraicos '+-k' a '-k' en 6 reactivos de C-09 (Q-C09-439, Q-C09-440, Q-C09-441, Q-C09-463, Q-C09-464, Q-C09-465).",
    "Separar comandos LaTeX fusionados (\\betaj -> \\beta j y \\rhot -> \\rho t) en misconception_warning de Hab-05 y Hab-09.",
    "Instanciar dinámicamente los parámetros de misconception_warning en 58 reactivos de 10 habilidades (Hab-01, Hab-02, Hab-04, Hab-05, Hab-06, Hab-09, Hab-18, Hab-19, Hab-20, Hab-21).",
    "Eliminar el parámetro decorativo '(no $y=19$)' en Q-C02-083 y balancear longitudes en los 8 ítems MS con sesgo menor."
  ]
}
```

</details>
