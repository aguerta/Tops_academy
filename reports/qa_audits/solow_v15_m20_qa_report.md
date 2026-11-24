# Auditoría de Calidad Pedagógica, Psicométrica y Path-to-Mastery v2.0: `solow_v15_m20`

> [!WARNING]
> **CURSO RETIRADO DE LA PLATAFORMA**: Este curso fue eliminado de la plataforma interactiva el **2026-11-24 04:14:51**. Este informe de auditoría se conserva exclusivamente como registro histórico y pedagógico ('legacy').

**Estado en Plataforma:** ELIMINADO  
**Fecha de Eliminación:** 2026-11-24 04:14:51  
**Curso:** Solow V15 M20 (`solow_v15_m20.json`)  
**Calificación Normativa QM-OSCQR:** **20.00 / 20.00** — *EXCELENTE (19.0 - 20.0 pts) — PLATINUM MASTERY*  
**Mastery Path Readiness Index (MPRI):** **100.00 / 100.00** — *GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo*  
**Arbitraje Ciego (Stage 5 Judge Audit):** `149 / 149` ítems concordantes (`100.00%` acuerdo, `0` desacuerdos sin reparar)  
**Validación de Plataforma:** `platform_validation_error = null` (`18` competencias, `579` reactivos)

---

## 1. Resumen Ejecutivo y Perfil del Banco

El curso **`solow_v15_m20`** cubre de manera integral el modelo neoclásico de crecimiento de Solow (1956), su formulación intensiva y en niveles, la dinámica cuantitativa Cobb-Douglas, el caso Harrod-Domar de proporciones fijas, la producción sin capital esencial, precios competitivos de factores, arbitraje intertemporal, participación factorial, cambio tecnológico neutral, oferta laboral elástica / ahorro variable, tributación proporcional con población endógena y rigidez salarial con preferencia por la liquidez.

- **Competencias:** `18` (`1` Hecho `[H]`, `9` Conceptos `[C]`, `8` Habilidades `[Hab]`), con entre `27` y `48` reactivos por competencia.
- **Distribución de Modalidades (`579` reactivos):**
  - `adversarial_break`: `132` (`22.80%`)
  - `open_symbolic`: `96` (`16.58%`)
  - `multiple_select`: `90` (`15.54%`)
  - `unstructured_model`: `87` (`15.03%`)
  - `fill_in_the_blank`: `69` (`11.92%`)
  - `proof_dag`: `51` (`8.81%`)
  - `invariant_canvas`: `45` (`7.77%`)
  - `concept_matching`: `9` (`1.55%`)
  - `multiple_choice_7_options`: `0` (`0.00%`)
- **Evocación Activa y Discriminación:** `100.00%` (`72.54%` modalidades Bloom Superior + `15.54%` `multiple_select` + `11.92%` `fill_in_the_blank`).

---

## 2. Evaluación por Dimensiones QM-OSCQR (20.00 Puntos)

| Dimensión | Puntaje | Máximo | Estado | Hallazgos Deterministas y Semánticos |
| :--- | :---: | :---: | :---: | :--- |
| **D1. Arquitectura Curricular, Topología DAG y ZPD** | **4.00** | 4.00 | EXCELENTE | `18` competencias (`1` Fact, `9` Concept, `8` Skill). DAG acíclico (`has_cycle=false`), `1` componente conexo, `max_dag_depth=5`, `0` pares solapados, `0` huérfanas. ZPD tri-banda (`193` easy / `193` medium / `193` hard) en `18/18` competencias. |
| **D2. Calidad Psicométrica, Modalidad y Anti-Gaming** | **5.00** | 5.00 | EXCELENTE | `MC7=0.00%`, `FIB=11.92%`, `MS=15.54%`, `BloomSup=72.54%`. `282` distractores con `100.00%` cobertura de `error_rationale`, `0` imposibles por dominio, `0` multiplicadores mágicos, `0` relleno de longitud. Sesgo de longitud en MS: `2.22%` (`2/90`: `Q-C02-128`, `Q-C02-129`, diferencia marginal de 2 caracteres). |
| **D3. Andamiaje Socrático y Remediación Diagnóstica** | **5.00** | 5.00 | EXCELENTE | `100.00%` de reactivos con `3` a `5` pistas socráticas genuinas (`0.00%` boilerplate Mad-Libs, `0.00%` envenenadas, `0` fugas de clave). Unicidad de slots de rationale: `100.00%` (`33/33` slots únicos), `0` rationales numéricos desconectados, `0` advertencias clonadas. |
| **D4. Alineación Instruccional, Bloom y Pureza** | **4.00** | 4.00 | EXCELENTE | `100.00%` de habilidades (`300/300`) en `Apply+`. **Índice Bloom Real Generado (`bloom_weighted_index`): `3.96 / 5.00`** vs **Piso Bloom Expected (`adaptive_bloom_floor`): `3.86 / 5.00`** (brecha `0.00`). `90.67%` en `Apply+`, `68.91%` en `Analyze + Evaluate` (tier `ÉLITE`), `0` violaciones de coherencia `modalidad × bloom`. |
| **D5. Accesibilidad, Ergonomía UI y Sintaxis KaTeX** | **2.00** | 2.00 | EXCELENTE | `0` errores KaTeX (`unclosed_braces=0`, `triple_dollars=0`, `unbalanced_dollars=0`, `sympy_in_katex=0`). `0` observaciones de prosa en `\text{...}`, `0` identificadores crudos, `0` colisiones por concatenación, `0` residuos de plantilla (`template_vars=0`, `blind_repl=0`). |

- **Subtotal Bruto:** `20.00 / 20.00`
- **Penalizaciones Duras Aplicadas:** Ninguna (`0.00`)
- **Puntaje Final:** **`20.00 / 20.00`**

---

## 3. Mastery Path Readiness Index (`MPRI`: 100.00 / 100.00)

| Pilar Cognitivo y de Plataforma | Puntaje | Máximo | Detalle de Cumplimiento |
| :--- | :---: | :---: | :--- |
| **1. `zpd_adaptive_progression`** | **20.00** | 20.00 | Calibración tri-banda (`easy`/`medium`/`hard`) en `18/18` competencias; `100.00%` de Habilidades en `Apply+`; **`bloom_weighted_index = 3.96` vs `adaptive_bloom_floor = 3.86`** (banda `ÉLITE`). |
| **2. `retrieval_modality_and_anti_gaming`** | **20.00** | 20.00 | `100.00%` evocación activa/discriminación; `>= 25` esqueletos distintos; `0` competencias memorizables; `0` cuantificadores vacuos; `0` relleno `[R-15]`. |
| **3. `socratic_scaffolding_lifeline`** | **25.00** | 25.00 | `100.00%` pistas socráticas genuinas (`3–5` niveles progresivos específicos a los parámetros del reactivo); `0` pistas envenenadas o Mad-Libs. |
| **4. `diagnostic_remediation_alignment`** | **15.00** | 15.00 | `100.00%` cobertura y unicidad de `error_rationale` (`282/282`), `0` rationales numéricos desconectados, `0` `phantom_numeric_rationale` en `96` `open_symbolic`. |
| **5. `dag_and_interleaving_topology`** | **10.00** | 10.00 | Grafo DAG acíclico (`has_cycle=false`), `1` componente conexo, `0` aristas invertidas, `0` habilidades sin prerrequisitos. |
| **6. `cognitive_ergonomics_and_framing`** | **10.00** | 10.00 | KaTeX 100% limpio, `0` prosa desbordante, `0` prefijos inter-dominio, notación consistente ($k=r=K/L$, $\lambda=n$). |

**Veredicto del Recorrido Estudiantil:** Certificado en nivel **GOLD MASTERY PATH** para estudio autónomo y dominio adaptativo sin fricción cognitiva ni atajos de *gaming*.

---

## 4. Auditoría Explícita de Regresión Histórica (`content-to-course`)

Se verificó directamente sobre `courses/solow_v15_m20.json` que no reaparezcan los defectos históricos documentados en versiones previas:

1. **`multiple_select` (90 reactivos):**
   - **Cantidad de opciones:** `78 / 90` (`86.67%`) tienen **5 opciones** y `12 / 90` (`13.33%`) tienen **6 opciones**. **`0 / 90` (`0.00%`)** quedaron atascados en 4 opciones.
   - **Variación de respuestas correctas:** Distribución perfectamente balanceada entre **1 correcta** (`30 / 90`, `33.33%`), **2 correctas** (`30 / 90`, `33.33%`) y **3 correctas** (`30 / 90`, `33.33%`). Se elimina por completo el sesgo histórico $\binom{4}{2}=6$.
2. **`invariant_canvas` (45 reactivos):**
   - **Curvas interactivas vs fijas:** `24 / 45` (`53.33%`) usan `1` curva interactiva y `3 / 45` (`6.67%`) usan `2` curvas interactivas. Los `18 / 45` (`40.00%`) restantes (`C-02`, ej. `Q-C02-106` a `Q-C02-108`) combinan `1` recta fija (`lamk`) con **`1` deslizador paramétrico (`c_sl`)** y `1` punto móvil (`P1`); es decir, no existe ningún caso trivial donde `fixed_curves` ya dibuje la solución sin interacción paramétrica.
   - **`step_mismatch`:** **`0 / 45` (`0.00%`)** — todas las coordenadas objetivo (`target_state.points`) son múltiplos exactos de `step`.
3. **`adversarial_break` (132 reactivos):**
   - De los `88` ítems en modo `find_fallacy` (los otros `44` corresponden a modos alternos sin `fallacy_step_id`/`correct_reason_id`), la posición de la razón correcta está distribuida equilibradamente: **`R1` = `26 / 88` (`29.55%`)**, **`R2` = `28 / 88` (`31.82%`)**, **`R3` = `34 / 88` (`38.64%`)**.
   - La posición del paso falaz está balanceada exactamente: **`S2` = `44 / 88` (`50.00%`)** y **`S3` = `44 / 88` (`50.00%`)**. Sin concentración patológica.
4. **`proof_dag` (51 reactivos):**
   - **`39 / 51` (`76.47%`)** presentan **ramificación real** en el DAG (`in-degree > 1` o `out-degree > 1`) con pools de `5` a `7` pasos y `require_justification`.
   - Solo `12 / 51` (`23.53%`) tienen cadena lineal de 4 pasos requeridos, pero igualmente embebidos en pools con pasos distractores (`pool_len` 5–7).
5. **`concept_matching` (9 reactivos):**
   - **`0 / 9` (`0.00%`)** tienen 2–3 pares: `6 / 9` (`66.67%`) tienen **4 pares** y `3 / 9` (`33.33%`) tienen **5 pares**.
   - **`9 / 9` (`100.00%`)** incluyen **distractores** en `targets` (`6` o `7` targets para `4` o `5` premisas).
   - **`0 / 9` (`0.00%`)** presentan mapeo trivial `P_i -> T_i`.
6. **Interpolación literal, inconsistencias conceptuales y palabras absolutas:**
   - **Bugs de interpolación literal (`Si $2=0$`, `($6>0$)`):** **`0`** ocurrencias en todo el banco (`579` reactivos).
   - **Inconsistencias conceptuales entre competencias:** **`0`** detectadas; la transición de notación entre Solow 1956 ($Q=L\phi(k), \lambda$) y la formulación moderna ($Y=F(K,L), r=K/L, n$) está explícitamente unificada en `Hab-01` y mantenida de forma coherente en las `18` competencias.
   - **Palabras absolutas en distractores (`nunca`, `siempre`, `todo`, `únicamente`, `ignora`, etc.):** Presentes en apenas `15 / 282` (`5.32%`) distractores frente a `3 / 180` (`1.67%`) en opciones correctas (dentro de rango sano, sin constituir patrón *test-wise* explotable; en los ítems revisados, como `Q-C02-128`, corresponden a cuantificadores matemáticos legítimos como *"Para todo $k>12$"*).

---

## 5. Acciones de Seguimiento Opcionales (No Bloqueantes)

1. **Micro-ajuste cosmético en `Q-C02-128` y `Q-C02-129` (`multiple_select`):** En ambos reactivos la opción correcta mide `92` caracteres frente a un máximo de `90` caracteres en distractores (`2.22%` del subtipo MS). Aunque es imperceptible para un estudiante y no activa penalización, se puede recortar 3–4 caracteres en la opción correcta en futuras regeneraciones para llevar `ms_length_bias` a `0.00%`.

---

<details>
<summary>Metadatos Estructurados (JSON)</summary>

```json
{
  "course_metadata": {
    "course_id": "solow_v15_m20",
    "unit_title": "Solow V15 M20",
    "detected_objective": "Dominio y aplicación analítica integral del modelo de crecimiento neoclásico de Solow y sus extensiones",
    "total_competencies": 18,
    "total_questions": 579,
    "bloom_index": {
      "weighted_index": 3.96,
      "adaptive_floor": 3.86,
      "gap": 0.0,
      "apply_plus_pct": 90.67,
      "superior_pct": 68.91,
      "tier": "ÉLITE",
      "coherence_violations_count": 0
    }
  },
  "dimension_scores": {
    "architecture_granularity": {
      "score": 4.0,
      "max": 4.0,
      "feedback": "Estructura curricular con 18 competencias (1 Hechos, 9 Conceptos, 8 Habilidades). DAG acíclico y conexo (ciclos=False, comp. conexos=1, pares solapados=0). ZPD: 18/18 competencias con calibración tri-banda ('easy', 'medium', 'hard')."
    },
    "assessment_quality": {
      "score": 5.0,
      "max": 5.0,
      "feedback": "Modalidad: MC7=0.0%, FIB=11.92%, MS=15.54%, BloomSup=72.54% (100.0% evocación activa/discriminación). Distractores: 282 evaluados con 100.0% cobertura de error_rationale (imposibles por dominio=0, claves corruptas=0, sesgo MS=2.22%)."
    },
    "scaffolding_hints": {
      "score": 5.0,
      "max": 5.0,
      "feedback": "Andamiaje formativo: 100.0% de reactivos con 3 a 5 pistas socráticas escalonadas (100.0% pistas genuinas, 0.0% boilerplate Mad-Libs, 0.0% envenenadas). Unicidad diagnóstica real de rationales: 100.0%."
    },
    "instructional_alignment": {
      "score": 4.0,
      "max": 4.0,
      "feedback": "Alineación cognitiva de Bloom: 100.0% de habilidades prácticas en Apply+; Índice Bloom Real Generado: 3.96/5.0 vs Piso Bloom Expected (Adaptativo): 3.86/5.0 (68.91% Analyze+Evaluate, tier: ÉLITE, incoherencias=0)."
    },
    "technical_ergonomics": {
      "score": 2.0,
      "max": 2.0,
      "feedback": "Sintaxis KaTeX: 0 errores críticos. Ergonomía: 0 observaciones de prosa en \\text{...}, 0 identificadores crudos, 0 colisiones por concatenación, 0 residuos de plantilla/reemplazo."
    }
  },
  "penalties_applied": [],
  "raw_subtotal": 20.0,
  "final_score": 20.0,
  "quality_tier": "EXCELENTE (17-20)",
  "mastery_path_readiness": {
    "mpri_score": 100.0,
    "mpri_max": 100.0,
    "mpri_tier": "GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo",
    "pillars": {
      "zpd_adaptive_progression": { "score": 20.0, "max": 20.0 },
      "retrieval_modality_and_anti_gaming": { "score": 20.0, "max": 20.0 },
      "socratic_scaffolding_lifeline": { "score": 25.0, "max": 25.0 },
      "diagnostic_remediation_alignment": { "score": 15.0, "max": 15.0 },
      "dag_and_interleaving_topology": { "score": 10.0, "max": 10.0 },
      "cognitive_ergonomics_and_framing": { "score": 10.0, "max": 10.0 }
    },
    "student_journey_verdict": "Certificado GOLD MASTERY PATH para dominio adaptativo autónomo."
  },
  "discovered_lint_rules": [
    {
      "rule_id": "LR-ABS-QUANT-MONITOR",
      "severity": "info",
      "regex_pattern": "\\b(nunca|siempre|todo|todos|todas|únicamente|ignora|jamás|ninguno|ninguna)\\b",
      "description": "Monitoreo preventivo de palabras absolutas en distractores frente a opciones correctas (5.32% vs 1.67% en solow_v15_m20, dentro de rango sano).",
      "evidence_items": ["Q-C02-128", "Q-C02-129"]
    }
  ],
  "remediation_actions": [
    "Opcional: acortar ligeramente la opción correcta en Q-C02-128 y Q-C02-129 (92 vs 90 chars) para eliminar el 2.22% de sesgo de longitud residual en multiple_select."
  ]
}
```

</details>
