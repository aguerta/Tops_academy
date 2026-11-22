# Reporte de Auditoría Técnica, Psicométrica y Pedagógica — `solow_m20_v11`

> [!IMPORTANT]
> **Veredicto Ejecutivo**: El curso **`solow_m20_v11` ("Solow M20 V11")** alcanza una calificación global de **19.30 / 20.00 puntos** (**Tier: EXCELENTE (17.0 - 20.0)**) y un **Mastery Path Readiness Index (`MPRI`) de 96.68 / 100.00** (**GOLD MASTERY PATH**). El banco de **621 reactivos** distribuidos en **20 micro-competencias** demuestra una ejecución sobresaliente del contrato M20 (`0.00%` MC7, `100.00%` evocación activa/discriminación condicional, `100.00%` calibración tri-banda ZPD y `100.00%` acuerdo en arbitraje ciego Stage-5 sobre 155 ítems auditados). No obstante, el **Loop de Verificación Semántica Adaptativa** identificó **tres hallazgos de rigor matemático y psicométrico** que impiden la perfección absoluta y se registran como nuevas reglas candidatas (`discovered_lint_rules`):
> 1. **Error algebraico de especificación en `Q-Hab07-473` (Hab-07)**: En el modelo Cobb-Douglas con progreso tecnológico neutral de Hicks ($Y = e^{gt}K^a L^{1-a}$, con $a = 0.3, b = 1 - a = 0.7$), la tasa asintótica de crecimiento del producto es $g_Y = n + \frac{g}{b}$ (igual a la del capital $g_K$), o bajo otra convención $g_Y = n + \frac{a g}{b}$ si el cambio técnico no se reescala. El enunciado escribe $g_Y = n + \frac{g}{0.7}$, mientras que el `misconception_warning` contradice directamente la fórmula del enunciado afirmando que la tasa de $Y$ es $n + \frac{a g}{b}$ (que supera a $n + g$ si $a > 1/2$).
> 2. **Fuga directa de respuesta en el enunciado (*Stem Answer Leak*) en `Q-C01-001` y `Q-C01-002` (C-01)**: El enunciado entrega explícitamente entre paréntesis el resultado que las opciones correctas piden validar (ej. en `Q-C01-001`: *"Con $K = 12$, $L = 4$ y $\phi(3) = 11$ (para $Q = 44$ y $\rho = 4$, $\rho K = 48$)..."*, mientras que la opción correcta D afirma *"La razón capital-trabajo es $k = 3$ y el producto total es $Q = 44$"*).
> 3. **Colisión de unidades porcentaje vs. proporción decimal en ecuaciones diferenciales de `Q-C10-505` y `Q-C10-506` (C-10)**: Se escribe $L = L_0 e^{4t}(w/p)^5$ y $\dot{r} = (sF(r,1) - 4r)(1 + 5 \cdot 5/r)^{-1}$ usando $n = 4$ en la ecuación diferencial mientras el paso S3 lo interpreta simultáneamente como *"tasa $4\%$ exógena"* y *"ahorro $s = 22\%$"*, mezclando escalas `[0, 1]` y `[0, 100]` además de instanciar $a = 5$ para una participación factorial que teóricamente pertenece a $(0, 1)$.

---

## 1. Resumen de Telemetría y Veredicto Global

| Métrica / Indicador | Valor Observado | Referencia / Umbral Normativo | Estado |
| :--- | :---: | :---: | :---: |
| **ID del Curso** | `solow_m20_v11` | Contrato JSON v11 | Validado (`error = null`) |
| **Total de Competencias** | `20` | $1$ Hecho (`[H]`), $11$ Conceptos (`[C]`), $8$ Habilidades (`[Hab]`) | Balanceado |
| **Total de Reactivos** | `621` | Mín: `27` / Máx: `36` por competencia ($\ge 3$ req.) | Cumple (`0` subpobladas) |
| **Acuerdo Arbitraje Ciego (Stage-5)** | `100.00%` | `155 / 155` ítems auditados sin desacuerdos latentes | Óptimo |
| **Índice Bloom Ponderado** | `3.80 / 5.00` | Piso adaptativo: `3.84` (Brecha: `-0.04` \| Tier: `SÓLIDO`) | Brecha menor (`-0.05` pts) |
| **Proporción `Apply+` / `Analyze+Evaluate`** | `93.24%` / `68.76%` | `100.00%` de Habilidades `[Hab]` en `Apply+` ($\ge 65\%$ Sup.) | Cumple |
| **Calificación Final QM-OSCQR** | **19.30 / 20.00** | Tier: **EXCELENTE (17.0 - 20.0)** | Certificado con observaciones |
| **Mastery Path Readiness (`MPRI`)** | **96.68 / 100.00** | Tier: **GOLD MASTERY PATH (85.0 - 100.0)** | Certificado para Dominio |

---

## 2. Evaluación Detallada por Dimensión (Rúbrica de 20 Puntos)

| Dimensión | Puntaje Determinista | Ajuste Semántico | Puntaje Final | Máximo | Estado |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **D1. Arquitectura Curricular, Topología DAG y ZPD** | `3.84` | `0.00` | **3.84** | `4.00` | Sólido |
| **D2. Calidad Psicométrica, Evocación y Anti-Gaming** | `5.00` | `-0.19` | **4.81** | `5.00` | Muy Bueno |
| **D3. Andamiaje Socrático Progresivo y Remediación** | `5.00` | `-0.10` | **4.90** | `5.00` | Excelente |
| **D4. Alineación Instruccional, Bloom y Pureza de Dominio** | `3.95` | `-0.20` | **3.75** | `4.00` | Sólido |
| **D5. Accesibilidad, Ergonomía Cognitiva en UI y KaTeX** | `2.00` | `0.00` | **2.00** | `2.00` | Impecable |
| **Subtotal Bruto** | `19.79` | `-0.49` | **19.30** | `20.00` | — |
| **Penalizaciones Duras Automáticas** | `0.00` | `0.00` | **0.00** | — | Sin penalizaciones duras |
| **CALIFICACIÓN FINAL** | **19.79** | **-0.49** | **19.30** | **20.00** | **EXCELENTE (17.0 - 20.0)** |

---

### 2.1. Dimensión 1: Arquitectura Curricular, Topología DAG y Calibración ZPD (`3.84 / 4.00 pts`)
- **Topología DAG y Navegación Adaptativa**: El grafo consta de **20 micro-competencias** en un único componente conexo (`connected_components_count = 1`), libre de ciclos (`has_cycle = false`), con profundidad máxima `4`, `0` aristas invertidas (`idx(prereq) < idx(comp)` cumplido al 100%) y `0` habilidades sin prerrequisitos.
- **Calibración ZPD Tri-Banda**: Las **20 de 20 competencias (`100.00%`)** implementan las 3 bandas de dificultad (`easy = 165`, `medium = 207`, `hard = 249`), habilitando el motor `calibrateByMasteryDifficulty` en todas las transiciones hacia *Mastered*.
- **Hallazgo Estructural (`-0.16 pts`)**: El linter arquitectónico y la inspección semántica confirman **2 pares de competencias con solapamiento curricular directo** debido a la fusión de dos notaciones del modelo de Solow (notación $(Q, k, \phi(k), \lambda)$ en `C-01..Hab-02` vs. notación del artículo original de Solow 1956 $(Y, r, F(r,1), n)$ en `H-01..C-12`):
  1. `Hab-01` (*"Derivación de la Ecuación Fundamental de Solow"*: $\dot{k} = s\phi(k) - \lambda k$) $\leftrightarrow$ `C-04` (*"Ecuación Fundamental de Solow"*: $\dot{r} = sF(r,1) - nr$).
  2. `Hab-02` (*"Solución Cuantitativa Cobb-Douglas y Trayectoria Temporal"*: $\bar{k} = (s/\lambda)^{1/(1-\alpha)}$) $\leftrightarrow$ `Hab-04` (*"Solución Explícita Cobb-Douglas"*: $r^* = (s/n)^{1/(1-a)}$).

### 2.2. Dimensión 2: Calidad Psicométrica, Modalidad de Evocación y Anti-Gaming (`4.81 / 5.00 pts`)
- **Erradicación del Reconocimiento Pasivo (Contrato M20)**: `0.00%` de opción múltiple convencional (`mc7_count = 0`). El `100.00%` de los 621 reactivos exige generación activa o discriminación estructural:
  - `adversarial_break`: `135` (`21.74%`)
  - `multiple_select`: `108` (`17.39%`)
  - `open_symbolic`: `96` (`15.46%`)
  - `unstructured_model`: `81` (`13.04%`)
  - `fill_in_the_blank`: `69` (`11.11%`)
  - `invariant_canvas`: `54` (`8.70%`)
  - `proof_dag`: `51` (`8.21%`)
  - `concept_matching`: `27` (`4.35%`)
- **Integridad de Distractores**: `240 / 240` distractores evaluados poseen `error_rationale` específico (`100.00%` cobertura), `0` multiplicadores mágicos (`1.333x`), `0` sesgos de longitud en `multiple_select` (`biased_ms_pct = 0.00%`) y un mínimo de `25` esqueletos distintos por competencia.
- **Hallazgo Semántico Anti-Gaming (`-0.19 pts`)**: En los reactivos `Q-C01-001` y `Q-C01-002` (`multiple_select`), el enunciado incluye un bloque parentético que **regala literalmente el valor numérico de $Q$ evaluado en las opciones**:
  - En `Q-C01-001`: El stem declara *"Con $K = 12$, $L = 4$ y $\phi(3) = 11$ **(para $Q = 44$ y $\rho = 4$, $\rho K = 48$)**, marque las afirmaciones correctas..."*, y la opción correcta `D` dice *"La razón capital-trabajo es $k = 3$ y el producto total es $Q = 44$"*, mientras los distractores `B` y `C` proponen $Q = 48$ y $Q = 11$.
  - En `Q-C01-002`: El stem declara *"Dada una economía con $K = 98$, $L = 7$, $\phi(14) = 9$ **(producto total $Q = 63$; referencia Domar $\rho = 4$, $\rho K = 392$)**..."*, y la opción correcta `B` dice *"La razón capital-trabajo es $k = 14$ y el producto total es $Q = 63$"*.
  - Esto reduce un ejercicio de discriminación conceptual a simple lectura literal del paréntesis del enunciado.

### 2.3. Dimensión 3: Andamiaje Socrático Progresivo y Remediación Diagnóstica (`4.90 / 5.00 pts`)
- **Cobertura y Pureza Socrática**: El `100.00%` de los 621 reactivos cuenta con 3 pistas progresivas genuinas (`0.00%` boilerplate Mad-Libs, `0.00%` envenenamiento anti-socrático, `0` fugas de respuesta en pistas) y solución detallada paso a paso.
- **Unicidad Diagnóstica**: `100.00%` de unicidad de slots de `error_rationale` (`41 / 41` slots únicos, `93` instancias únicas, `0` rationales numéricos desconectados en `open_symbolic`).
- **Hallazgo en `misconception_warning` (`-0.10 pts`)**: En `Q-Hab07-473` (y 11 reactivos hermanos de `Hab-07`), el linter detectó `[static_misconception_warning_uninstantiated_params]` por la condición estática `a>1/2`. Al inspeccionar semánticamente el ítem, se observa que además de no instanciar $a = 0.3$, la advertencia cita la fórmula $g_Y = n + a g / b$, la cual **contradice** la fórmula $g_Y = n + g / b$ usada en el enunciado, las pistas y la solución detallada del propio reactivo.

### 2.4. Dimensión 4: Alineación Instruccional, Taxonomía de Bloom y Pureza de Dominio (`3.75 / 4.00 pts`)
- **Taxonomía de Bloom e Índice Ponderado**:
  - Distribución: `Remember = 3` (`0.48%`), `Understand = 39` (`6.28%`), `Apply = 152` (`24.48%`), `Analyze = 310` (`49.92%`), `Evaluate = 117` (`18.84%`).
  - El `100.00%` de los reactivos de Habilidades (`288 / 288`) están en `Apply+`, y el `68.76%` del curso completo se ubica en niveles superiores (`Analyze + Evaluate`).
  - El **Índice Bloom Ponderado es `3.80 / 5.00`** frente a un piso adaptativo de `3.84` (brecha de `-0.04`, Tier `SÓLIDO`, deducción determinista de `-0.05 pts`), con `0` violaciones de coherencia `modalidad × bloom`.
- **Hallazgos Semánticos de Rigor Económico y Matemático (`-0.20 pts`)**:
  1. **Inconsistencia en la Tasa Asintótica del Producto con Progreso Neutral de Hicks (`Q-Hab07-473`, Hab-07)**:
     - En Solow (1956, Sección VI, ec. 13), con $Y = e^{gt} K^a L^{1-a}$ y $b = 1 - a$, la integración de $\dot{K} = s e^{gt} K^a (L_0 e^{nt})^b$ arroja que el stock de capital $K(t)$ crece asintóticamente a la tasa $g_K = n + \frac{g}{b}$ (tal como se evalúa correctamente en `Q-Hab07-469` y `Q-Hab07-470`).
     - Sin embargo, dado que $Y(t) = e^{gt} K(t)^a L(t)^b$, la tasa asintótica del producto total $Y(t)$ es:
       $$g_Y = g + a\left(n + \frac{g}{b}\right) + b n = n + g\left(1 + \frac{a}{b}\right) = n + \frac{g}{b}$$
       (porque $1 + \frac{a}{1-a} = \frac{1}{1-a} = \frac{1}{b}$), **mientras que** la fórmula citada en el `misconception_warning` de `Q-Hab07-473` dice: *"Calcule la tasa de $Y=e^{gt}K^a L^{1-a}$ usando la tasa asintótica de $K$: $g + a(n+g/b) + (1-a)n = n + ag/b$, que supera a $n+g$ si $a>1/2$"*.
     - Esa igualdad en `misconception_warning` contiene un **error algebraico elemental**: suma $g + a(n + g/b) + (1-a)n$ y olvida el primer sumando $g$ al simplificar a $n + ag/b$ (el resultado real de $g + a(n+g/b) + (1-a)n$ es $n + g + ag/b = n + g/b$). Este error confunde al estudiante que lee la advertencia tras resolver $g_Y = n + g/0.7$.
  2. **Mezcla de Porcentajes y Tasas Decimales + Parámetro $a > 1$ en Oferta Laboral Elástica (`Q-C10-505` y `Q-C10-506`, C-10)**:
     - En `Q-C10-505`, se escribe $L = L_0 e^{4t}(w/p)^5$ y $\dot{r} = (sF(r,1) - 4r)(1 + 5 \cdot 5/r)^{-1}$, y luego en `S3` se afirma *"idéntica a la condición de equilibrio con tasa $4\%$ exógena"*. Escribir $e^{4t}$ y $-4r$ representa una tasa del $400\%$ por periodo, no del $4\%$ ($0.04$). Además, en la ecuación (6a) de Solow, el factor es $(1 + a h / r)^{-1}$ o $(1 + \frac{w}{p}\frac{h}{\dots})$, donde $a \in (0, 1)$ es la elasticidad del producto respecto al capital; instanciar $a = 5$ y $h = 5$ viola el dominio económico estándar $a \in (0, 1)$.

### 2.5. Dimensión 5: Accesibilidad, Ergonomía Cognitiva en UI y Sintaxis KaTeX (`2.00 / 2.00 pts`)
- **Pureza Sintáctica y Visual**: `0` delimitadores `$` desbalanceados, `0` llaves sin cerrar, `0` triples dólares `$$$`, `0` residuos de variables de plantilla o `SymPy`, `0` bloques `\text{...}` con prosa extensa y `0` identificadores crudos de código. Todas las expresiones en `invariant_canvas`, `proof_dag`, `open_symbolic` y `adversarial_break` renderizan limpiamente en el frontend.

---

## 3. Desglose del Mastery Path Readiness Index (`MPRI`: `96.68 / 100.00`)

| Pilar Cognitivo / Plataforma | Puntaje Determinista | Puntaje Ajustado | Máximo | Observación de Camino al Dominio |
| :--- | :---: | :---: | :---: | :--- |
| **1. `zpd_adaptive_progression`** | `19.88` | **19.88** | `20.00` | `20/20` competencias tri-banda (`easy`/`medium`/`hard`); `100%` skills en `Apply+`; Bloom `3.80` vs `3.84`. |
| **2. `retrieval_modality_and_anti_gaming`** | `20.00` | **19.00** | `20.00` | `100%` evocación activa/discriminación (`0%` MC7); `-1.00 pt` por fuga de respuesta en stems de `C-01`. |
| **3. `socratic_scaffolding_lifeline`** | `25.00` | **24.50** | `25.00` | `100%` pistas socráticas genuinas en 3 niveles; `-0.50 pts` por contradicción algebraica en `misconception_warning` de `Hab-07`. |
| **4. `diagnostic_remediation_alignment`** | `15.00` | **15.00** | `15.00` | `240/240` distractores con `error_rationale` fiel al error operacional exacto. |
| **5. `dag_and_interleaving_topology`** | `9.30` | **9.30** | `10.00` | DAG conexo, acíclico y en orden topológico; `-0.70 pts` por 2 pares de competencias duplicadas (`Hab-01/C-04`, `Hab-02/Hab-04`). |
| **6. `cognitive_ergonomics_and_framing`** | `10.00` | **9.00** | `10.00` | KaTeX impecable; `-1.00 pt` por inconsistencia de escala `%` vs decimal ($4\%$ escrito como $e^{4t}$ y $-4r$) en `C-10`. |
| **TOTAL MPRI** | **99.18** | **96.68** | **100.00** | **GOLD MASTERY PATH (85.0 - 100.0): Certificado para Dominio Adaptativo** |

---

## 4. Nuevas Reglas de Linter Descubiertas (`/learn` — Loop de Auto-Mejora)

Para evitar que futuros cursos incurran en los tres patrones semánticos detectados, se reportan tres reglas candidatas para `scripts/standardized_audit_engine.py`:

1. **`stem_parenthetical_answer_leak_linter` (`warning` / Dimensión 2)**:
   - **Patrón**: El enunciado (`stem`) contiene entre paréntesis una igualdad explícita variable-valor, ej. `\(.*?\b([QYrkwp])\s*=\s*(-?\d+(?:\.\d+)?).*?\)`, que coincide textualmente con la igualdad declarada como verdadera en una opción correcta (`is_correct: true`) de `multiple_select` o `multiple_choice`.
   - **Evidencia**: `Q-C01-001` (`(para $Q = 44$...)` en el stem y `el producto total es $Q = 44$` en `opt_d`), `Q-C01-002` (`(producto total $Q = 63$...)` en el stem y `el producto total es $Q = 63$` en `opt_b`).
2. **`misconception_warning_formula_contradiction_linter` (`warning` / Dimensión 3 y 4)**:
   - **Patrón**: El campo `misconception_warning` afirma como verdadera una identidad algebraica que contradice la expresión canónica del `stem` o `detailed_solution` (en `Hab-07`: $g + a(n+g/b) + (1-a)n = n + ag/b$ omite el término $+g$, contradiciendo $g_Y = n + g/b$).
   - **Evidencia**: `Q-Hab07-473` (y los 11 reactivos adicionales de `Hab-07` afectados por el mismo template de `misconception_warning`).
3. **`percent_integer_exponent_mismatch_linter` (`warning` / Dimensión 4 y 5)**:
   - **Patrón**: Un reactivo utiliza un entero $n \in [1, 50]$ directamente en un exponente temporal $e^{nt}$ o término de dilución $-nr$ (ej. $e^{4t}$, $-4r$) mientras el texto de los pasos o del `error_rationale` se refiere a dicho parámetro con el símbolo de porcentaje `$4\%$` sin dividir por $100$.
   - **Evidencia**: `Q-C10-505`, `Q-C10-506`.

---

## 5. Plan de Remediación Prioritario

1. **Corregir el `misconception_warning` en `Hab-07` (`Q-Hab07-473` y reactivos hermanos)**:
   - Reemplazar la derivación errónea `$g + a(n+g/b) + (1-a)n = n + ag/b$, que supera a $n+g$ si $a>1/2$` por la identidad algebraica correcta: `$g + a(n+g/b) + (1-a)n = n + g(1 + a/b) = n + g/b$, que supera a $n+g$ porque $b = 1 - a < 1$`, instanciando además los parámetros $a$ y $b$ de cada reactivo.
2. **Eliminar la fuga de respuesta entre paréntesis en los stems de `C-01` (`Q-C01-001`, `Q-C01-002`, etc.)**:
   - Retirar `(para $Q = 44$ y $\rho = 4$, $\rho K = 48$)` del enunciado y conservar únicamente el parámetro de referencia de Domar `($\rho = 4$)`, obligando al estudiante a calcular genuinamente $k = K/L$ y $Q = L\phi(k)$.
3. **Unificar la escala decimal de tasas en `C-10` (`Q-C10-505`, `Q-C10-506`)**:
   - Expresar la tasa demográfica en forma decimal consistente ($e^{0.04t}$ y $-0.04r$ cuando se habla de $4\%$) y restringir el parámetro de participación del capital a $a \in (0, 1)$ en el factor $(1 + a h / r)^{-1}$.
4. **Consolidar o diferenciar explícitamente los pares de competencias solapadas (`Hab-01` vs. `C-04` y `Hab-02` vs. `Hab-04`)**:
   - Diferenciar los títulos y alcances (por ejemplo, dedicando `Hab-01`/`Hab-02` al contraste introductorio Domar vs. Solow por sustitución de Bernoulli y `C-04`/`Hab-04` a la integración directa sobre niveles agregados $K(t)$ del artículo de Solow de 1956) para eliminar la alerta de duplicación curricular en `architecture_dag_linter`.
5. **Elevar marginalmente el Índice Bloom Ponderado (`+0.04`)**:
   - Promover 10–12 reactivos de nivel `Understand` en `C-01` (una vez eliminado el leak parentético) a nivel `Apply` o `Analyze` para superar el piso adaptativo de `3.84` y alcanzar el tier `ÉLITE` de Bloom.

---

<details>
<summary>Metadatos Estructurados (JSON)</summary>

```json
{
  "course_metadata": {
    "course_id": "solow_m20_v11",
    "unit_title": "Solow M20 V11",
    "detected_objective": "Dominio y aplicación analítica integral de Solow M20 V11",
    "total_competencies": 20,
    "total_questions": 621,
    "bloom_index": {
      "weighted_index": 3.8,
      "adaptive_floor": 3.84,
      "gap": 0.04,
      "apply_plus_pct": 93.24,
      "superior_pct": 68.76,
      "tier": "SÓLIDO",
      "coherence_violations_count": 0
    }
  },
  "dimension_scores": {
    "architecture_granularity": {
      "score": 3.84,
      "max": 4.0,
      "feedback": "Estructura curricular con 20 competencias (1 Hechos, 11 Conceptos, 8 Habilidades). DAG acíclico y conexo (ciclos=False, comp. conexos=1, pares solapados=2: Hab-01<->C-04 y Hab-02<->Hab-04). ZPD: 20/20 competencias con calibración tri-banda ('easy', 'medium', 'hard')."
    },
    "assessment_quality": {
      "score": 4.81,
      "max": 5.0,
      "feedback": "Modalidad M20 ejemplar: MC7=0.0%, FIB=11.11%, MS=17.39%, BloomSup=71.5% (100.0% evocación activa/discriminación). Distractores: 240/240 con error_rationale. Deducción semántica (-0.19 pts) por fuga directa de respuesta (Q=44, Q=63) en el paréntesis del enunciado en Q-C01-001 y Q-C01-002."
    },
    "scaffolding_hints": {
      "score": 4.9,
      "max": 5.0,
      "feedback": "100.0% de reactivos con 3 pistas socráticas genuinas (0.0% boilerplate Mad-Libs, 0.0% envenenadas) y 100.0% unicidad de slots diagnósticos. Deducción menor (-0.10 pts) en Hab-07 (12 ítems, ej. Q-Hab07-473) por misconception_warning estático ('a>1/2') cuya identidad algebraica contradice la fórmula del propio reactivo."
    },
    "instructional_alignment": {
      "score": 3.75,
      "max": 4.0,
      "feedback": "100.0% de habilidades en Apply+; Índice Bloom ponderado: 3.80/5.0 (piso adaptativo 3.84, brecha -0.04, 68.76% Analyze+Evaluate, tier: SÓLIDO). Deducción semántica (-0.20 pts) por error algebraico en misconception_warning de Hab-07 (g + a(n+g/b) + (1-a)n simplificado erróneamente a n + ag/b en vez de n + g/b) y mezcla de tasas porcentuales (4%) con enteros (e^{4t}, -4r) y parámetro a=5>1 en Q-C10-505/506."
    },
    "technical_ergonomics": {
      "score": 2.0,
      "max": 2.0,
      "feedback": "Sintaxis KaTeX 100% limpia: 0 errores críticos (delimitadores balanceados, llaves cerradas, cero $$$), 0 observaciones de prosa en \\text{...}, 0 identificadores crudos y 0 residuos de plantilla."
    }
  },
  "penalties_applied": [],
  "raw_subtotal": 19.3,
  "final_score": 19.3,
  "quality_tier": "EXCELENTE (17-20)",
  "mastery_path_readiness": {
    "mpri_score": 96.68,
    "mpri_max": 100.0,
    "mpri_tier": "GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo",
    "pillars": {
      "zpd_adaptive_progression": { "score": 19.88, "max": 20.0 },
      "retrieval_modality_and_anti_gaming": { "score": 19.0, "max": 20.0 },
      "socratic_scaffolding_lifeline": { "score": 24.5, "max": 25.0 },
      "diagnostic_remediation_alignment": { "score": 15.0, "max": 15.0 },
      "dag_and_interleaving_topology": { "score": 9.3, "max": 10.0 },
      "cognitive_ergonomics_and_framing": { "score": 9.0, "max": 10.0 }
    },
    "student_journey_verdict": "El estudiante experimenta una ruta de aprendizaje adaptativa de altísimo nivel cognitivo (100% libre de opción múltiple pasiva MC7, con 8 modalidades interactivas ricas, calibración ZPD tri-banda completa y pistas socráticas bien articuladas). Corregir el leak parentético en C-01, la identidad algebraica en el misconception_warning de Hab-07 y la escala porcentual en C-10 elevará el curso a perfección técnica absoluta (20/20)."
  },
  "discovered_lint_rules": [
    {
      "rule_id": "stem_parenthetical_answer_leak",
      "severity": "warning",
      "regex_pattern": "\\([^)]*\\b([QYrkwp]\\s*=\\s*-?\\d+(?:\\.\\d+)?)[^)]*\\)",
      "description": "Detecta enunciados que declaran explícitamente entre paréntesis el valor numérico de la variable objetivo (ej. 'para Q = 44', 'producto total Q = 63') que luego se evalúa literalmente como proposición verdadera en las opciones correctas.",
      "evidence_items": ["Q-C01-001", "Q-C01-002"]
    },
    {
      "rule_id": "misconception_warning_formula_contradiction",
      "severity": "warning",
      "regex_pattern": "g\\s*\\+\\s*a\\(n\\+g/b\\)\\s*\\+\\s*\\(1-a\\)n\\s*=\\s*n\\s*\\+\\s*ag/b",
      "description": "Detecta contradicciones algebraicas entre la fórmula enseñada en el reactivo (g_Y = n + g/b) y la identidad en misconception_warning que omite el sumando g al simplificar g + a(n+g/b) + (1-a)n como n + ag/b.",
      "evidence_items": ["Q-Hab07-473"]
    },
    {
      "rule_id": "percent_integer_exponent_mismatch",
      "severity": "warning",
      "regex_pattern": "e\\^\\{([1-9]\\d*)t\\}[\\s\\S]*?\\1\\\\%",
      "description": "Detecta reactivos donde una tasa porcentual n% (ej. 4%) se inserta como entero n=4 sin dividir entre 100 en exponentes temporales e^{4t} o términos diferenciales -4r.",
      "evidence_items": ["Q-C10-505", "Q-C10-506"]
    }
  ],
  "remediation_actions": [
    "Corregir la identidad algebraica en el misconception_warning de Hab-07 (Q-Hab07-473 y 11 reactivos hermanos): reemplazar 'g + a(n+g/b) + (1-a)n = n + ag/b, que supera a n+g si a>1/2' por 'g + a(n+g/b) + (1-a)n = n + g/b, que supera a n+g porque b = 1-a < 1', instanciando los parámetros del enunciado.",
    "Eliminar la fuga directa de respuesta entre paréntesis en los enunciados de C-01 (ej. retirar 'para Q = 44' en Q-C01-001 y 'producto total Q = 63' en Q-C01-002).",
    "Homogeneizar la escala decimal en C-10 (Q-C10-505 y Q-C10-506): usar n = 0.04 en e^{0.04t} y -0.04r cuando el texto refiera a una tasa del 4%, y restringir la participación factorial a in (0, 1).",
    "Diferenciar explícitamente el alcance curricular entre los dos pares de competencias solapadas (Hab-01 <-> C-04 y Hab-02 <-> Hab-04) para eliminar la redundancia entre las dos notaciones del modelo de Solow.",
    "Promover ~10 reactivos de C-01 del nivel Bloom 'Understand' a 'Apply' tras eliminar la fuga parentética para cerrar la brecha de -0.04 respecto al piso adaptativo de Bloom (3.80 vs 3.84)."
  ]
}
```

</details>
