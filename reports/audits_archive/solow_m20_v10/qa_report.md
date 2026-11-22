# Reporte de Auditoría de Calidad Pedagógica, Psicométrica y Técnica (`solow_m20_v10`)

> [!IMPORTANT]
> **Veredicto Ejecutivo:** **18.79 / 20.00 pts** — **EXCELENTE (17.00 - 20.00 pts)**  
> **Mastery Path Readiness Index (MPRI):** **95.47 / 100.00** — **GOLD MASTERY PATH (85.00 - 100.00): Certificado para Dominio Adaptativo**  
> **Puntaje Base Determinista (`StandardizedAuditEngine`):** 19.99 / 20.00 pts (MPRI Determinista: 99.97 / 100.00)  
> **Ajuste por Loop de Verificación Semántica Adaptativa:** -1.20 pts (-0.40 pts en Dimensión 2, -0.45 pts en Dimensión 3, -0.35 pts en Dimensión 4) tras detectar una inconsistencia algebraica en la competencia `Hab-07` entre la descripción/advertencia (`n + ag/b`, omitiendo el término directo `+g`) y la derivación de las soluciones/claves (`n + g/b`), además de rationales tautológicos por omisión en sub-ítems verdaderos de las Fases 1 y 2 de `unstructured_model`.

---

## 1. Resumen de Telemetría y Perfil Curricular

| Métrica / Indicador | Valor Observado | Estándar / Umbral Normativo | Estado |
| :--- | :--- | :--- | :--- |
| **ID del Curso** | `solow_m20_v10` | Contrato JSON Schema v1.0.0 | ✅ Válido (`platform_validation_error: null`) |
| **Total de Competencias** | 17 (`1` Hecho, `10` Conceptos, `6` Habilidades) | Granularidad atómica y balance cognitivo | ✅ Balanceado |
| **Total de Reactivos** | 402 (20 a 32 por competencia) | $\ge 3$ reactivos por competencia | ✅ 100.00% poblado |
| **Topología DAG** | 0 ciclos, 1 componente conexo, prof. máx. 4 | Acíclico, conexo, orden topológico válido | ✅ 100.00% íntegro |
| **Calibración ZPD** | 17/17 competencias tri-banda (`100` easy, `150` medium, `152` hard) | 3 bandas (`easy`, `medium`, `hard`) por competencia | ✅ 100.00% tri-banda |
| **Modalidades de Evocación** | `MC7`: 0.00%, `FIB`: 8.96%, `MS`: 15.42%, `BloomSup`: 75.62% | 100% generación activa o discriminación compleja | ✅ Contrato M20 activo |
| **Índice Bloom Ponderado** | **3.83 / 5.00** (Piso adaptativo: **3.84**, brecha: `-0.01`) | Banda Sólida/Élite ($\ge 65\%$ `Analyze + Evaluate`) | ⚠️ **68.91%** en `Analyze + Evaluate` (Tier: `SÓLIDO`) |
| **Arbitraje Ciego (Stage-5)** | 145/145 ítems auditados con acuerdo (`100.00%`) | 0 desacuerdos sin reparar | ✅ 100.00% acuerdo |
| **Sintaxis y Ergonomía KaTeX** | 0 errores de sintaxis, 0 errores de ergonomía UI | 0 delimitadores rotos, 0 `\text{prosa}` larga | ✅ 100.00% limpio |

### Distribución de Modalidades Interactivas (`402` reactivos)
- **`adversarial_break`**: 92 reactivos (22.89%)
- **`multiple_select`**: 62 reactivos (15.42%)
- **`unstructured_model`**: 62 reactivos (15.42%)
- **`open_symbolic`**: 58 reactivos (14.43%)
- **`invariant_canvas`**: 48 reactivos (11.94%)
- **`fill_in_the_blank`**: 36 reactivos (8.96%)
- **`proof_dag`**: 32 reactivos (7.96%)
- **`concept_matching`**: 12 reactivos (2.99%)

---

## 2. Evaluación por Dimensiones (Rúbrica QM-OSCQR / Path-to-Mastery v2.0 — 20.00 Puntos)

| Dimensión | Puntaje Determinista | Ajuste Semántico | Puntaje Final | Máximo | Nivel |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **D1. Arquitectura Curricular, Topología DAG y Calibración ZPD** | 4.00 | 0.00 | **4.00** | 4.00 | Excelente |
| **D2. Calidad Psicométrica, Modalidad de Evocación y Anti-Gaming** | 5.00 | -0.40 | **4.60** | 5.00 | Excelente |
| **D3. Andamiaje Socrático Progresivo y Remediación Diagnóstica** | 5.00 | -0.45 | **4.55** | 5.00 | Excelente |
| **D4. Alineación Instruccional, Taxonomía de Bloom y Pureza de Dominio** | 3.99 | -0.35 | **3.64** | 4.00 | Excelente |
| **D5. Accesibilidad, Ergonomía Cognitiva en UI y Sintaxis KaTeX** | 2.00 | 0.00 | **2.00** | 2.00 | Excelente |
| **Subtotal / Nota Final (0 Penalizaciones Duras)** | **19.99** | **-1.20** | **18.79** | **20.00** | **EXCELENTE** |

---

### Dimensión 1: Arquitectura Curricular, Topología DAG y Calibración ZPD — **4.00 / 4.00 pts**
- **Granularidad y Secuenciación:** El curso desglosa exhaustivamente el artículo seminal de Robert M. Solow (1956), *"A Contribution to the Theory of Economic Growth"*, y las notas de análisis dinámico en 17 competencias atómicas: 1 Hecho (`H-01`), 10 Conceptos (`C-01` a `C-06`, `C-08` a `C-11`) y 6 Habilidades (`Hab-01`, `Hab-02`, `Hab-05`, `Hab-06`, `Hab-07`, `Hab-08`).
- **Topología del Grafo (DAG):** El grafo es conexo (`1` solo componente conexo, `0` nodos isla), acíclico (`has_cycle: false`), con profundidad máxima de `4` niveles y `0` aristas invertidas (`inverted_prerequisite_edges_count: 0`). Las dos competencias raíz (`H-01` y `C-03`) alimentan la derivación de la Ecuación Fundamental de Solow (`Hab-01`), desde donde se ramifican el análisis cualitativo, las tecnologías específicas (Cobb-Douglas, Leontief/Harrod-Domar, CES cuadrática), la determinación competitiva de precios factoriales y las extensiones macroeconómicas (oferta laboral elástica, impuestos, trampas demográficas y rigideces keynesianas).
- **Calibración ZPD Tri-Banda:** Las 17 competencias presentan cobertura completa en las tres bandas de dificultad (`100` `easy`, `150` `medium`, `152` `hard`), habilitando las transiciones adaptativas de `calibrateByMasteryDifficulty` sin puntos muertos.

---

### Dimensión 2: Calidad Psicométrica, Modalidad de Evocación y Anti-Gaming — **4.60 / 5.00 pts**
- **Fortalezas Deterministas:** El curso opera bajo el contrato M20 (`mc7_count: 0`), con un **100.00%** de reactivos de generación activa o discriminación estructural compleja y un **75.62%** (`304/402`) en modalidades interactivas de orden superior (`adversarial_break`, `unstructured_model`, `open_symbolic`, `invariant_canvas`, `proof_dag`, `concept_matching`). Se observa alta variedad de esqueletos ($\ge 16$ esqueletos distintos), `0` distractores por multiplicador mágico, `0` opciones con sesgo de longitud en `multiple_select` y `0` competencias vulnerables a memorización visual.
- **Hallazgo del Loop de Verificación Semántica (-0.40 pts):**
  - En los reactivos de `unstructured_model` (como se evidencia en `Q-Hab07-303` a `Q-Hab07-311`), mientras que las opciones falsas o distractores poseen `error_rationale` diagnósticos precisos (`"Con 0.04>0 y 0.5>0, K/L crece sin límite a tasa 0.04/0.5 y nunca converge a un r* finito"`), los sub-ítems verdaderos/requeridos de `phase1_variables` y `phase2_assumptions` utilizan plantillas tautológicas de fallback del generador:
    - `"Revisa el rol estructural de Crecimiento poblacional n=0.02 dentro del modelo."` (`Q-Hab07-303`, `phase1_variables.items[0]`)
    - `"Verifica la validez analítica del supuesto Fuerza laboral exponencial a tasa constante n=0.02."` (`Q-Hab07-303`, `phase2_assumptions.options[0]`)
  - Cuando un estudiante clasifica erróneamente una variable exógena como endógena o omite un supuesto requerido en `PracticeSession.tsx`, el `FeedbackToast` muestra este mensaje genérico sin explicar *por qué* la variable es exógena ni qué condición del modelo se rompe al omitir el supuesto.

---

### Dimensión 3: Andamiaje Socrático Progresivo y Remediación Diagnóstica — **4.55 / 5.00 pts**
- **Fortalezas Deterministas:** El **100.00%** de los 402 reactivos cuenta con 3 pistas progresivas genuinas (`0.00%` boilerplate Mad-Libs, `0.00%` pistas envenenadas, `0` fugas de respuesta). Las pistas guían paso a paso desde el planteamiento estructural (ej. regla del producto en `K = kL` o sustitución de Bernoulli $z = k^{1-\alpha}$) hasta el despeje algebraico.
- **Hallazgos del Loop de Verificación Semántica (-0.45 pts):**
  1. **Clúster de Riesgo `Q-Hab07-289` (`static_misconception_warning_uninstantiated_params` — 10 reactivos en `Hab-07`):** El linter determinista señaló 7 instancias (`Q-Hab07-288` a `Q-Hab07-292`, `Q-Hab07-303` a `Q-Hab07-307`), y la inspección semántica reveló dos defectos acoplados en la misma advertencia:
     > `"Calcule \dot{Y}/Y=g+a(\dot{K}/K)+(1-a)n=n+ag/b; note que si a>1/2 el producto crece incluso más rápido que n+g."`
     - **Contradicción algebraica con la solución detallada:** En el paso previo de la misma advertencia se escribe $\dot{Y}/Y = g + a(\dot{K}/K) + (1-a)n$. Como $\dot{K}/K = n + g/b$ con $b = 1-a$, al sustituir se obtiene:
       $$\frac{\dot{Y}}{Y} = g + a\left(n + \frac{g}{1-a}\right) + (1-a)n = n + g\left(1 + \frac{a}{1-a}\right) = n + \frac{g}{1-a} = n + \frac{g}{b}$$
       Sin embargo, la advertencia afirma que la suma es $n + ag/b$ (omitiendo sumar el término directo $+g$, que es precisamente el error de Solow 1956 p. 85 al escribir la tasa de $Y$, mientras que el propio `detailed_solution` del ítem `Q-Hab07-289` calcula correctamente $y = g + 0.4(0.02 + g/0.6) + 0.6(0.02) = 0.02 + g/0.6$ y el distractor `D-Hab07-01` penaliza exactamente usar $n + (a/b)g$ por *"omitir el término directo $+g$ en $\dot{Y}/Y$"*). Es decir, la advertencia `misconception_warning` contradice frontalmente la solución detallada y enseña como identidad la misma expresión que el reactivo penaliza como distractor `D-Hab07-01`.
     - **Falta de instanciación paramétrica:** Repite la cota estática `a>1/2` incluso en reactivos donde el enunciado fija $a=0.4 < 1/2$ (`Q-Hab07-289`), $a=0.25$ (`Q-Hab07-290`) o $a=0.2$ (`Q-Hab07-307`).

---

### Dimensión 4: Alineación Instruccional, Taxonomía de Bloom y Pureza de Dominio — **3.64 / 4.00 pts**
- **Alineación Taxonómica y Piso Adaptativo (-0.01 pt determinista):** El **100.00%** de los 182 reactivos de Habilidades (`Skill`) están evaluados en `Apply+`, y el **68.91%** del curso completo se ubica en niveles superiores (`188` en `Analyze` y `89` en `Evaluate`), con `0` violaciones de coherencia `modalidad × bloom`. El Índice Bloom Ponderado es **3.83 / 5.00** frente al piso adaptativo de **3.84** (brecha marginal de `-0.01`, cluster `Q-H01-001`), ubicándose en el límite superior del tier `SÓLIDO`.
- **Hallazgo Semántico de Consistencia Teórico-Matemática en `Hab-07` (-0.35 pts):**
  - En la definición curricular de la competencia `Hab-07` (*"Cambio Tecnológico Neutral"*):
    > `"Análisis asintótico del modelo Cobb-Douglas con progreso técnico neutral Y=e^{gt}K^a L^{1-a} (b=1-a): tasas de crecimiento de K (n+g/b), Y (n+ag/b), K/L (g/b) y K/Y (g)."`
  - Esta descripción reproduce sin corregir un conocido desliz tipográfico del texto original de Solow (1956, Sección IV, p. 85), donde tras integrar $K(t) \sim e^{(n+g/b)t}$ se sustituyó en $K^a L^{1-a}$ olvidando multiplicar por el factor externo $e^{gt}$. Si $\dot{K}/K = n + g/b$ y $\dot{Y}/Y = n + ag/b$, entonces $\dot{K}/K - \dot{Y}/Y = (1-a)g/b = g$ (razón $K/Y$ creciendo a tasa $g$). **Pero** en todos los reactivos del banco de `Hab-07` (`Q-Hab07-288` a `Q-Hab07-311`), el motor matemático deriva correctamente $\dot{Y}/Y = g + a(n + g/b) + bn = n + g/b = \dot{K}/K$, concluyendo que $K/Y$ converge a una **constante** ($\dot{K}/K - \dot{Y}/Y = 0$) y marcando $n + (a/b)g$ como el distractor `D-Hab07-01`.
  - Esta dualidad entre el enunciado de la competencia/advertencia (`n + ag/b` y `K/Y` creciendo a `g`) y la evaluación real de los reactivos (`n + g/b` y `K/Y` constante) genera disonancia cognitiva directa para el estudiante que consulta la ficha teórica de la competencia antes de resolver la práctica.
- **Verificación de las Otras 16 Competencias:** El resto del curso (`H-01`, `C-01` a `C-11`, `Hab-01` a `Hab-06`, `Hab-08`) presenta rigor económico y matemático impecable:
  - Derivación exacta de $\dot{k} = s\phi(k) - \lambda k$ mediante regla del producto (`Hab-01`).
  - Integración exacta de la EDO de Bernoulli para Cobb-Douglas con cambio de variable $z = k^{1-\alpha}$ y tasa de convergencia $(1-\alpha)\lambda$ (`Hab-02`).
  - Análisis de la función Leontief $Y = \min(K/a, L/b)$ comparando la tasa garantizada $s/a$ con la tasa natural $n$ (`C-05`).
  - Resolución del modelo CES cuadrático $Y = (a\sqrt{K} + \sqrt{L})^2$, umbral de existencia de estado estacionario $sa^2 < n$, equilibrio $r^* = (\sqrt{n/s} - a)^{-2}$ y participación laboral $\theta_L = 1 - a\sqrt{s/n}$ (`Hab-05` y `Hab-06`).
  - Invariancia de $r^*$ bajo oferta laboral elástica $L = L_0 e^{nt}(w/p)^h$ gracias a la positividad estricta del factor amortiguador $(1 + ah/r)^{-1} > 0$ (`C-09`).
  - Tasa de ahorro efectiva $s_{\text{eff}} = s + (v-s)t$ bajo tributación proporcional y fracción de inversión pública $v$ (`C-10`).
  - Trampa demográfica malthusiana vs. umbral inestable $r_2$ con crecimiento poblacional endógeno $n(r)$ (`C-11`).
  - Desempleo bajo salario real rígido $\bar{w}/p$ con brecha $\dot{L}/L - n = (s/\bar{r})F(\bar{r},1) - n$ (`Hab-08`).

---

### Dimensión 5: Accesibilidad, Ergonomía Cognitiva en UI y Sintaxis KaTeX — **2.00 / 2.00 pts**
- **Pureza Sintáctica y Visual:** `0` llaves sin cerrar, `0` signos de dólar desbalanceados, `0` triples dólares `$$$`, `0` residuos de plantilla o variables de SymPy expuestas, `0` bloques `\text{...}` con prosa larga que rompan el diseño responsivo en dispositivos móviles, y `0` identificadores crudos sin formatear. Todas las curvas interactivas de `invariant_canvas` especifican dominios, rangos y pasos (`step`) limpios y bien escalados.

---

## 3. Mastery Path Readiness Index (MPRI: **95.47 / 100.00**)

| Pilar de Preparación para el Dominio (MPRI) | Puntaje Determinista | Puntaje Ajustado | Máximo | Observación Técnica y Pedagógica |
| :--- | :---: | :---: | :---: | :--- |
| **1. Progresión Adaptativa ZPD (`zpd_adaptive_progression`)** | 19.97 | **19.97** | 20.00 | 17/17 competencias tri-banda; 100% `Skill` en `Apply+`; Bloom 3.83 vs piso 3.84. |
| **2. Modalidad de Evocación y Anti-Gaming (`retrieval_modality_and_anti_gaming`)** | 20.00 | **20.00** | 20.00 | 0% MC7, 100% generación activa/discriminación, 75.62% modalidades Bloom Superior. |
| **3. Salvavidas de Andamiaje Socrático (`socratic_scaffolding_lifeline`)** | 25.00 | **23.50** | 25.00 | 100% pistas socráticas genuinas; -1.50 pts por contradicción algebraica en `misconception_warning` de `Hab-07`. |
| **4. Alineación de Remediación Diagnóstica (`diagnostic_remediation_alignment`)** | 15.00 | **12.00** | 15.00 | 100% cobertura en distractores; -3.00 pts por rationales tautológicos en ítems verdaderos de `unstructured_model` y contradicción con `D-Hab07-01`. |
| **5. Topología DAG e Interleaving (`dag_and_interleaving_topology`)** | 10.00 | **10.00** | 10.00 | DAG conexo, acíclico, profundidad 4, listo para interleaving 60/40 en Quiz y 55/45 en Unit Test. |
| **6. Ergonomía Cognitiva y Framing (`cognitive_ergonomics_and_framing`)** | 10.00 | **10.00** | 10.00 | Sintaxis KaTeX impecable y registro disciplinar macroeconómico riguroso. |
| **Total MPRI** | **99.97** | **95.47** | **100.00** | **GOLD MASTERY PATH (85.00 - 100.00)** |

---

## 4. Loop de Auto-Mejora de Reglas (`discovered_lint_rules`)

Durante la inspección semántica de los reactivos de `unstructured_model` y `Hab-07`, se identificaron **2 nuevos patrones sistemáticos** que los 21 linters actuales de `StandardizedAuditEngine` no interceptan:

1. **`unstructured_model_tautological_rationale` (Severity: `warning`)**
   - **Patrón Regex:** `^(?:Revisa el rol estructural de|Verifica la validez anal[íi]tica del supuesto)\s+.+$`
   - **Evidencia:** `Q-Hab07-303`, `Q-Hab07-304`, `Q-Hab07-305`, `Q-Hab07-306`, `Q-Hab07-307`, `Q-Hab07-308`, `Q-Hab07-309`, `Q-Hab07-310`, `Q-Hab07-311`.
   - **Descripción:** Los ítems de `phase1_variables` y las opciones verdaderas (`is_required: true`) de `phase2_assumptions` en `unstructured_model` utilizan una cadena genérica prefabricada que repite el nombre de la variable o supuesto sin ofrecer explicación diagnóstica cuando el estudiante falla al clasificarlos.
2. **`warning_solution_formula_contradiction` (Severity: `critical`)**
   - **Patrón Regex:** `\\dot\{Y\}/Y\s*=\s*g\s*\+\s*a\(\\dot\{K\}/K\)\s*\+\s*\(1-a\)n\s*=\s*n\s*\+\s*ag/b`
   - **Evidencia:** `Q-Hab07-288`, `Q-Hab07-289`, `Q-Hab07-290`, `Q-Hab07-291`, `Q-Hab07-292`, `Q-Hab07-303`, `Q-Hab07-304`, `Q-Hab07-305`, `Q-Hab07-306`, `Q-Hab07-307`.
   - **Descripción:** La identidad algebraica en `misconception_warning` omite sumar el término $+g$ al simplificar $g + a(n + g/b) + (1-a)n$, afirmando que equivale a $n + ag/b$ mientras que `detailed_solution` deriva $n + g/b$ y `diagnostic_distractors` penaliza $n + (a/b)g$ como el error `D-Hab07-01`.

---

## 5. Plan de Remediación Prioritario

1. **[Prioridad Alta — Rigor Matemático en `Hab-07`]:** Actualizar `competencies[12].description` (`Hab-07`) y el `misconception_warning` de los reactivos `Q-Hab07-288` a `Q-Hab07-292` y `Q-Hab07-303` a `Q-Hab07-307` para reflejar la identidad consistente con el resto del banco: $\dot{Y}/Y = g + a(n + g/b) + (1-a)n = n + g/b$ (con razón $K/Y$ asintóticamente constante), e instanciar dinámicamente los parámetros $a, b, n$ del enunciado en lugar de la desigualdad estática `a>1/2`.
2. **[Prioridad Media — Diagnóstico en `unstructured_model`]:** Reemplazar las plantillas `"Revisa el rol estructural de {label} dentro del modelo."` y `"Verifica la validez analítica del supuesto {content}."` en `phase1_variables` y `phase2_assumptions` por explicaciones causales específicas (ej. explicar por qué $g$ y $n$ vienen dados fuera del sistema de acumulación y por qué $a \in (0,1)$ evita la divergencia de $g/(1-a)$).
3. **[Prioridad Baja — Piso Adaptativo de Bloom]:** Elevar 2 reactivos de nivel `Understand` en `H-01` o `C-03` a `Apply` para subir el Índice Bloom Ponderado de `3.83` a `3.85`, superando holgadamente el piso adaptativo de `3.84` y alcanzando el tier `ÉLITE`.

---

<details>
<summary>Metadatos Estructurados (JSON)</summary>

```json
{
  "course_metadata": {
    "course_id": "solow_m20_v10",
    "unit_title": "Solow M20 V10",
    "detected_objective": "Dominio y aplicación analítica integral del modelo neoclásico de crecimiento económico de Solow (1956), su ecuación diferencial fundamental, trayectorias explícitas (Cobb-Douglas, Leontief, CES cuadrática), precios factoriales competitivos y extensiones macroeconómicas.",
    "total_competencies": 17,
    "total_questions": 402,
    "bloom_index": {
      "weighted_index": 3.83,
      "adaptive_floor": 3.84,
      "gap": -0.01,
      "apply_plus_pct": 92.04,
      "superior_pct": 68.91,
      "tier": "SÓLIDO",
      "coherence_violations_count": 0
    }
  },
  "dimension_scores": {
    "architecture_granularity": {
      "score": 4.0,
      "max": 4.0,
      "feedback": "Estructura curricular impecable con 17 competencias atómicas (1 Hecho, 10 Conceptos, 6 Habilidades). DAG acíclico y conexo (profundidad máxima 4, 0 pares solapados, 0 aristas invertidas). Calibración ZPD tri-banda ('easy', 'medium', 'hard') activa en 17/17 competencias."
    },
    "assessment_quality": {
      "score": 4.6,
      "max": 5.0,
      "feedback": "100.00% de evocación activa o discriminación compleja bajo contrato M20 (MC7=0.00%, FIB=8.96%, MS=15.42%, BloomSup=75.62%) y 100.00% de acuerdo en arbitraje ciego Stage-5 (145/145). Se deduce -0.40 pts porque los sub-ítems verdaderos/requeridos de phase1_variables y phase2_assumptions en unstructured_model emplean rationales tautológicos de plantilla ('Revisa el rol estructural de...', 'Verifica la validez analítica del supuesto...')."
    },
    "scaffolding_hints": {
      "score": 4.55,
      "max": 5.0,
      "feedback": "100.00% de reactivos con 3 pistas socráticas escalonadas genuinas (0.00% boilerplate, 0.00% envenenamiento). Se deduce -0.45 pts por el clúster Q-Hab07-289 (10 reactivos en Hab-07) donde misconception_warning repite la condición estática 'a>1/2' sin instanciar parámetros y afirma que g+a(n+g/b)+(1-a)n = n+ag/b, contradiciendo la solución detallada (n+g/b) y el distractor D-Hab07-01."
    },
    "instructional_alignment": {
      "score": 3.64,
      "max": 4.0,
      "feedback": "100.00% de habilidades prácticas en Apply+ y 68.91% del banco en Analyze+Evaluate. Índice Bloom Ponderado en 3.83/5.00 frente al piso adaptativo de 3.84 (-0.01 pt determinista). Se deduce -0.35 pts por la inconsistencia algebraica en la ficha descriptiva de Hab-07, que lista las tasas de Y como n+ag/b y K/Y como g, mientras que todos los reactivos de Hab-07 evalúan y demuestran que Y crece a n+g/b y K/Y permanece constante."
    },
    "technical_ergonomics": {
      "score": 2.0,
      "max": 2.0,
      "feedback": "Sintaxis KaTeX y ergonomía visual 100.00% libres de defectos: 0 llaves rotas, 0 delimitadores desbalanceados, 0 bloques \\text{...} desbordantes, 0 identificadores crudos y 0 residuos de plantilla."
    }
  },
  "penalties_applied": [],
  "raw_subtotal": 18.79,
  "final_score": 18.79,
  "quality_tier": "EXCELENTE (17-20)",
  "mastery_path_readiness": {
    "mpri_score": 95.47,
    "mpri_max": 100.0,
    "mpri_tier": "GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo",
    "pillars": {
      "zpd_adaptive_progression": {
        "score": 19.97,
        "max": 20.0
      },
      "retrieval_modality_and_anti_gaming": {
        "score": 20.0,
        "max": 20.0
      },
      "socratic_scaffolding_lifeline": {
        "score": 23.5,
        "max": 25.0
      },
      "diagnostic_remediation_alignment": {
        "score": 12.0,
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
    },
    "student_journey_verdict": "El curso ofrece una experiencia de aprendizaje adaptativo de altísimo rigor analítico, con un 75.62% de interacciones de orden superior (proof_dag, adversarial_break, invariant_canvas, open_symbolic, unstructured_model). Corrigiendo la identidad algebraica en la descripción/advertencia de Hab-07 y los rationales de fallback en unstructured_model, alcanzará la perfección teórica y diagnóstica."
  },
  "discovered_lint_rules": [
    {
      "rule_id": "unstructured_model_tautological_rationale",
      "severity": "warning",
      "regex_pattern": "^(?:Revisa el rol estructural de|Verifica la validez anal[íi]tica del supuesto)\\s+.+$",
      "description": "Detecta error_rationale tautológicos generados por plantilla en ítems de phase1_variables y opciones requeridas de phase2_assumptions dentro de reactivos unstructured_model.",
      "evidence_items": [
        "Q-Hab07-303",
        "Q-Hab07-304",
        "Q-Hab07-305",
        "Q-Hab07-306",
        "Q-Hab07-307",
        "Q-Hab07-308",
        "Q-Hab07-309",
        "Q-Hab07-310",
        "Q-Hab07-311"
      ]
    },
    {
      "rule_id": "warning_solution_formula_contradiction",
      "severity": "critical",
      "regex_pattern": "\\\\dot\\{Y\\}/Y\\s*=\\s*g\\s*\\+\\s*a\\(\\\\dot\\{K\\}/K\\)\\s*\\+\\s*\\(1-a\\)n\\s*=\\s*n\\s*\\+\\s*ag/b",
      "description": "Detecta contradicción algebraica en misconception_warning donde la simplificación de la tasa asintótica del producto omite el término directo +g (escribiendo n+ag/b en lugar de n+g/b) en conflicto directo con detailed_solution y con el distractor D-Hab07-01.",
      "evidence_items": [
        "Q-Hab07-288",
        "Q-Hab07-289",
        "Q-Hab07-290",
        "Q-Hab07-291",
        "Q-Hab07-292",
        "Q-Hab07-303",
        "Q-Hab07-304",
        "Q-Hab07-305",
        "Q-Hab07-306",
        "Q-Hab07-307"
      ]
    }
  ],
  "remediation_actions": [
    "Corregir en competencies[12].description (Hab-07) y en el misconception_warning de Q-Hab07-288..292 y Q-Hab07-303..307 la tasa asintótica de Y a n+g/b (con K/Y constante) para eliminar la contradicción con detailed_solution y el distractor D-Hab07-01, instanciando además el valor de 'a' del enunciado en vez de la cadena fija 'a>1/2'.",
    "Reemplazar los error_rationale tautológicos ('Revisa el rol estructural de...', 'Verifica la validez analítica del supuesto...') en phase1_variables y phase2_assumptions de los reactivos unstructured_model por explicaciones diagnósticas sustantivas.",
    "Promover 2 reactivos de nivel Understand en H-01 o C-03 a nivel Apply para elevar el Índice Bloom Ponderado de 3.83 a >= 3.85 (superando el piso adaptativo de 3.84)."
  ]
}
```

</details>
