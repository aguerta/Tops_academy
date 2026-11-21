# Reporte de Auditoría Técnica, Psicométrica y Pedagógica (QA): `estadistica_3_pre_pc2`

> [!WARNING]
> **CURSO RETIRADO DE LA PLATAFORMA**: Este curso fue eliminado de la plataforma interactiva el **2026-11-21 18:53:48**. Este informe de auditoría se conserva exclusivamente como registro histórico y pedagógico ('legacy').

**Estado en Plataforma:** ELIMINADO  
**Fecha de Eliminación:** 2026-11-21 18:53:48  
- **ID del Curso:** `estadistica_3_pre_pc2`
- **Título del Curso:** Estadística 3 - Preparación PC2 (Propiedades en Muestras Finitas y Teoría Asintótica)
- **Estándares de Evaluación:** Quality Matters (QM), OSCQR, Mastery Learning v2.0 (`StandardizedAuditEngine` + Verificación Semántica Adaptativa)
- **Fecha de Auditoría:** 2026-11-15
- **Estado del Curso:** `ACTIVO`
- **Calificación Global Auditada:** **17.70 / 20.0** — Tier: **`EXCELENTE (17.0 - 20.0 pts)`** *(Pre-cálculo determinista estático: 20.0 / 20.0)*
- **Mastery Path Readiness Index (MPRI):** **89.5 / 100.0** — **`GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo`** *(Pre-cálculo determinista estático: 99.91 / 100.0)*

---

## 1. Resumen Ejecutivo y Matriz de Calificación Híbrida

El curso `estadistica_3_pre_pc2` exhibe una arquitectura de evaluación adaptativa de **1,390 reactivos** distribuidos en **57 competencias** (32 Conceptos con 20 ítems cada uno y 25 Habilidades con 30 ítems cada una). En el **Fast Deterministic Pass** (`StandardizedAuditEngine`), el curso obtiene un puntaje perfecto (**20.0 / 20.0** y **MPRI 99.91 / 100.0**), con **0 penalizaciones duras**, **100% de cobertura en diagnósticos de distractores** (3,772/3,772), **100% de cobertura de 3 pistas socráticas por reactivo** (1,390/1,390), **100% de acuerdo en la auditoría ciega de jueces Stage-5** (120/120 ítems auditados) y **0 errores de sintaxis KaTeX**.

Sin embargo, aplicando el **Loop de Verificación Semántica Adaptativa con máximo escepticismo analítico** sobre los clústeres de riesgo (`risk_cluster_samples`), las **114 muestras estratificadas** (`stratified_samples`) y el grafo de competencias, se identificaron fricciones pedagógicas, psicométricas y de interpolación de plantillas que el linter estático no penaliza por umbral duro pero que impactan la experiencia real del estudiante:

1. **Solapamiento curricular inter-documento en el DAG (Dimensión 1):** La ingesta combinada de 4 fuentes documentales (`01_semana_9_apuntes.pdf`, `02_EST3_LEC07_26.2_V2.pdf`, `03_EST3_LEC08_26.2_v1.pdf`, `04_semana_10_apuntes.pdf`) generó pares de competencias casi homólogas (ej. `C-01` vs. `Hab-08` en sesgo/insesgadez; `C-02`/`C-04`/`C-09` vs. `Hab-09` en descomposición de ECM; `C-05` vs. `Hab-10` en cotas de Markov; `Hab-03` vs. `C-17` en Chebyshev; `C-30` vs. `Hab-22` en consistencia de $s^2$), además de saltos en la numeración de IDs (`C-16`, `C-18`..`C-21`, `C-24`, `C-35`..`C-38`, `Hab-11`) y ausencia de nodos de categoría `Fact` (`[H]`).
2. **Sesgo de longitud en `multiple_select` (44.16%) y ruido paramétrico decorativo (Dimensión 2):** El linter `ms_length_bias_linter` detecta que **136 de 308 reactivos MS (44.16%)** presentan asimetría sistemática de longitud entre las proposiciones verdaderas y los distractores. Adicionalmente, múltiples plantillas teóricas y de selección múltiple (`Q-Hab08-451`, `Q-C22-651`, `Q-C33-1031`) inyectan parámetros numéricos "muertos" o decorativos (ej. *"Si $G=0$ en el valor verdadero (con $\hat{\beta}_1=36, v_1=62$), la aproximación de primer orden falla"*) únicamente para forzar variabilidad superficial entre clones.
3. **Colisiones de interpolación numérica sin operador, pistas clonadas intra-arquetipo y `misconception_warning` truncados (Dimensión 3):**
   - En `Q-C39-1191` ($\alpha=0.5$) y `Q-C39-1192` ($\alpha=0.75$), la plantilla concatenó el coeficiente `2` y la variable `{alpha}` sin signo de multiplicación en los `error_rationale`, renderizando exponentes absurdos como `$146^{20.5-1}$` y `$178^{20.75-1}$` (en lugar de $2\cdot 0.5 - 1 = 0$). Fenómenos similares de concatenación ocurren en `Q-C05-141` (`263` por $2\cdot 63$) y `Q-C06-191` (`412` por $4\cdot 12$ y `26^2` por $2\cdot 6^2$).
   - **Contaminación Global en el 100% de los reactivos FIB (`556/556` ítems):** El campo `common_misconception_warning` / `misconception_warning` de **los 556 reactivos `fill_in_the_blank` de las 57 competencias** contiene exactamente el mismo string hardcodeado de `C-01`: `"$\\mathrm{Sesgo}(\\hat{\\theta}_n)=\\theta-\\mathbb{E}[\\hat{\\theta}_n]$"`, sin texto explicativo y totalmente ajeno a las otras 56 competencias (aparece en Axiomas de Kolmogorov, TCL, Slutsky, MCO, White, Hausman y Método Delta). Además, al ser una fórmula LaTeX y no la frase *"Verifique cuidadosamente los supuestos..."*, evadió el linter `generic_misconception_count = 0`.
   - **Inflación Artificial de Unicidad de `error_rationale` por Prefijos Rotativos (`56.18%` nominal vs. `29.45%` real):** El `57.90%` (`2,184 / 3,772`) de los distractores lleva antepuesto uno de 16 prefijos genéricos rotativos (*"Error conceptual:"*, *"Confusión teórica:"*, *"Fallo de cálculo:"*, *"Desvío algebraico:"*, *"Sustitución inválida:"*, etc.) sobre el mismo esqueleto de error. Al despojar dichos prefijos, la unicidad real de esqueletos normalizados cae de `56.18%` (`2,119/3,772`) a **`29.45%` (`1,111/3,772`)** globalmente (`26.65%` en las 37 competencias compartidas con Semana 9). Aun así, el contenido aritmético de sus `error_rationale` sí explica la operación matemática real del distractor en casi todas las competencias (a diferencia de `s9_vmapreduce_vlean43_v6`).
   - En `Q-C14-531` ($n=3$) y `Q-Hab06-331` ($n=11$), la interpolación numérica reemplazó la variable muda del límite o fracción de forma parcial (`"la esperanza de $m_2$ es $\\frac{n-1}{3}\\sigma^2$"`, `"Tome $a^{11}\\to 0$ cuando $n\\to\\infty$"`).
   - En `Q-Hab12-621` y `Q-Hab25-1331`, el `misconception_warning` conserva números hardcodeados de otro problema (`$5/n$`, `$25/n^2$`, `$100/n$`, `$20^2=400$`).

| Dimensión de Evaluación | Peso Máx. | Score Determinista | Deducción Semántica | Score Auditado | Estado / Veredicto |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **1. Arquitectura del Curso y Granularidad (DAG)** | 4.0 | 4.0 | -0.4 | **3.6** | Redundancia inter-documento entre los 4 PDFs y 0 nodos `[H]` (`Fact`). |
| **2. Calidad Psicométrica y Cognitiva de Evaluación** | 5.0 | 5.0 | -0.5 | **4.5** | 44.16% MS con sesgo de longitud y parámetros decorativos en MS/MC7 teóricos. |
| **3. Andamiaje Socrático, Pistas y Diagnóstico** | 5.0 | 5.0 | -0.9 | **4.1** | 556/556 FIB con `misconception_warning` de `C-01`, prefijos rotativos (29.45% unicidad real) y concatenación `20.5` en `C-39`. |
| **4. Alineación Instruccional y Cobertura (QM)** | 4.0 | 4.0 | -0.3 | **3.7** | Desfase `Concept` vs. `Skill` en ítems `easy` y desalineación temática en `C-08`. |
| **5. Ergonomía Técnica, KaTeX y Resiliencia** | 2.0 | 2.0 | -0.2 | **1.8** | 9 ítems con floats crudos `e-0X` dentro de KaTeX (`C-17`, `Hab-25`) y operador `*` en `Hab-14`. |
| **SUBTOTAL / CALIFICACIÓN FINAL** | **20.0** | **20.0** | **-2.3** | **17.7** | **EXCELENTE (17.0 - 20.0 pts)** |

---

## 2. Telemetría Determinista Completa (`audit_telemetry`)

La siguiente tabla resume las métricas exactas reportadas por los 12 linters deterministas del `StandardizedAuditEngine`:

| Linter / Módulo de Telemetría | Métrica Clave | Valor Observado | Estado |
| :--- | :--- | :--- | :---: |
| **Volumen General** | Competencias / Reactivos totales | **57** (`Concept`: 32, `Skill`: 25, `Fact`: 0) / **1,390** ítems | ✅ |
| **`architecture_dag_linter`** | Nodos aislados / Habilidades sin prerrequisitos | `0` aislados / `0` skills sin prerrequisitos (`total_edges = 96`) | ✅ |
| **`dag_mastery_topology_linter`** | Ciclos / Profundidad máx. / Componentes conexas | `has_cycle = false` / `max_dag_depth = 7` / `components = 1` / `inverted_edges = 0` | ✅ |
| **`zpd_progression_linter`** | Distribución de dificultad (`easy` / `medium` / `hard`) | `359` (25.83%) / `390` (28.06%) / `641` (46.12%) — **57/57** tri-banda | ✅ |
| **`zpd_progression_linter`** | Distribución Taxonomía de Bloom | `Understand`: 48 (3.45%), `Apply`: 638 (45.90%), `Analyze`: 368 (26.47%), `Evaluate`: 336 (24.17%) | ✅ |
| **`retrieval_modality_linter`** | Modalidades (`MC7` / `FIB` / `MS`) | `MC7`: 526 (37.84%) / `FIB`: 556 (40.00%) / `MS`: 308 (22.16%) (`active_pct = 62.16%`) | ✅ |
| **`ms_length_bias_linter`** | Reactivos MS con sesgo de longitud | **136 / 308** (**44.16%**) presentan asimetría de longitud | ⚠️ |
| **`distractor_integrity_linter`** | Distractores evaluados / Cobertura `error_rationale` | **3,772 / 3,772** (**100.0%**) con `error_rationale` (`telltale = 0`, `cloned = 0`) | ✅ |
| **`diagnostic_rationale_alignment`** | Unicidad léxica global de `error_rationale` | **2,119 / 3,772** únicos (**56.18%**) — `generic_boilerplate = 0` | ⚠️ |
| **`scaffolding_hints_linter`** | Reactivos con 3 pistas socráticas y solución detallada | **1,390 / 1,390** (**100.0%**) con 3 pistas y `detailed_solution` | ✅ |
| **`socratic_scaffolding_integrity`** | Pistas genuinas / Fugas de respuesta (`hint_answer_leak`) | **100.0%** genuinas (`boilerplate = 0`, `poisoned = 0`, `leaks = 0`) | ✅ |
| **`katex_syntax_linter` & `ergonomics`** | Errores de compilación LaTeX / Prosa en `\text{}` / Raw IDs | `0` llaves rotas / `0` `$` impares / `0` prosa pesada en `\text{}` / `0` Raw IDs | ✅ |
| **`stage5_judge_audit`** | Acuerdo de jueces ciegos Stage-5 | **120 / 120** auditados (**100.0%** `agreement_rate`, `0` desacuerdos sin reparar) | ✅ |

---

## 3. Evaluación Profunda por Dimensión (Loop de Verificación Semántica)

### Dimensión 1: Arquitectura del Curso y Granularidad de Competencias — **3.6 / 4.0**

#### Fortalezas Verificadas
- **Topología Acíclica Conexa (DAG):** El grafo de 57 competencias forma una única componente conexa (`connected_components_count = 1`), libre de ciclos (`has_cycle = false`), con profundidad máxima de 7 niveles (`max_dag_depth = 7`), 96 aristas dirigidas y 0 aristas invertidas (`inverted_prerequisite_edges_count = 0`).
- **Acoplamiento de Habilidades:** Las 25 competencias de tipo `Skill` (`[Hab]`) cuentan con prerrequisitos explícitos (`skills_without_prerequisites_count = 0`), partiendo desde 4 raíces conceptuales (`C-01`, `C-06`, `C-07`, `C-10`).
- **Volumen de Banco por Nodo:** Cumple al 100% con el contrato cuantitativo: exactamente 20 preguntas por cada una de las 32 competencias `Concept` (640 ítems) y 30 preguntas por cada una de las 25 competencias `Skill` (750 ítems).

#### Hallazgos Semánticos y Deducciones (-0.4 pts)
1. **Redundancia y Solapamiento Curricular Inter-Documento:** El curso se construyó a partir de 4 PDFs que cubren las Semanas 9 y 10 tanto en formato de apuntes de clase (`01_semana_9_apuntes.pdf`, `04_semana_10_apuntes.pdf`) como en presentaciones de diapositivas (`02_EST3_LEC07_26.2_V2.pdf`, `03_EST3_LEC08_26.2_v1.pdf`). La etapa de extracción no consolidó completamente los nodos equivalentes entre apuntes y diapositivas, generando duplicación funcional en el árbol de competencias:
   - **Sesgo e Insesgadez:** `C-01` (*"Sesgo, Insesgadez y Eficiencia Relativa"*, Doc 1) y `Hab-08` (*"Evaluación de Sesgo e Insesgadez"*, Doc 2), además de `C-13` (*"Varianza Muestral, Error Estándar y Eficiencia"*, Doc 2).
   - **Descomposición del ECM:** `C-02` (*"Descomposición del Error Cuadrático Medio"*, Doc 1), `C-04` (cuyos reactivos `Q-C04-091` y `Q-C04-092` piden calcular exactamente $\text{ECM}=\text{Var}+\text{Sesgo}^2$), `C-09` (`Q-C09-311` y `Q-C09-312` evalúan nuevamente $\text{ECM}=\text{Var}+\text{Sesgo}^2$) y `Hab-09` (*"Descomposición y Comparación por ECM"*, Doc 2).
   - **Desigualdad de Markov:** `C-05` (*"Desigualdad de Markov"*, Doc 1, donde `Q-C05-141` evalúa $\mathbb{E}[Y]/\delta$) y `Hab-10` (*"Cálculo de Cotas de Markov"*, Doc 2, donde `Q-Hab10-571` evalúa exactamente el mismo cociente $E[Y]/\delta$).
   - **Desigualdad de Chebyshev:** `Hab-03` (*"Derivación y Cálculo de Cotas de Chebyshev"*, Doc 1, `Q-Hab03-161`) y `C-17` (*"Desigualdad de Chebyshev"*, Doc 2, `Q-C17-601`), ambos evaluando el mismo cálculo de cota $\text{Var}(X)/\varepsilon^2 = 1/k^2$.
   - **Consistencia de Varianza Residual ($s^2$):** `C-30` (*"Consistencia del Estimador de Varianza del Error"*, Doc 3, `Q-C30-911`) y `Hab-22` (*"Consistencia Varianza Residual"*, Doc 4, `Q-Hab22-1161`).
   - **Método Delta y Estadístico $t$ Asintótico:** Solapamiento entre `Hab-15` (Doc 3) y `C-40`/`Hab-23` (Doc 4), así como entre `C-33`/`Hab-16` (Doc 3) y `Hab-21`/`C-42`/`Hab-25` (Doc 4).
2. **Secuenciación Pedagógica y Saltos de Numeración:** Los conceptos axiomáticos fundacionales (`C-10` *Espacio de Probabilidad y $\sigma$-álgebra*, `C-11` *Variable Aleatoria y Valor Esperado*, `C-12` *Muestra Aleatoria i.i.d.*) aparecen recién en el segundo bloque del curso (extraídos del Doc 2), después de que el estudiante ya cursó convergencia en media $r$-ésima (`C-06`), desigualdades de Markov/Chebyshev/Jensen (`C-05`, `Hab-03`, `Hab-04`) y consistencia débil (`C-03`). Asimismo, existen **11 IDs faltantes** en la secuencia (`C-16`, `C-18`, `C-19`, `C-20`, `C-21`, `C-24`, `C-35`, `C-36`, `C-37`, `C-38` y `Hab-11`) y **0 competencias clasificadas como `[H]` (`Fact`)**.

---

### Dimensión 2: Calidad Psicométrica y Cognitiva de la Evaluación — **4.5 / 5.0**

#### Fortalezas Verificadas
- **Rigor de Dominio y Precisión Matemática:** Las soluciones numéricas y simbólicas en los 114 reactivos inspeccionados son matemáticamente exactas (verificadas manualmente en `Q-C01-001`, `Q-Hab01-041`, `Q-C02-051`, `Q-Hab02-111`, `Q-Hab05-241`, `Q-Hab13-732`, `Q-C29-861`, `Q-C30-911`, `Q-Hab17-951`, `Q-Hab18-981`, `Q-Hab21-1081`, `Q-C41-1251`, `Q-C42-1321`, `Q-Hab25-1331`).
- **Diversidad de Evocación (62.16% Práctica Activa):** El 40.00% de los ítems son `fill_in_the_blank` (556 ítems de cálculo numérico directo sin apoyo de opciones) y el 22.16% son `multiple_select` (308 ítems de discriminación condicional de múltiples proposiciones), eliminando la dependencia del simple reconocimiento pasivo.
- **Calibración de Distractores en MC7:** Los 6 distractores de cada ítem `multiple_choice_7_options` provienen de perturbaciones algebraicas plausibles (ej. omitir el cuadrado del escalar en la varianza, usar el desvío estándar en vez de la varianza, olvidar restar $k$ grados de libertad, invertir numerador y denominador en la eficiencia relativa o el estadístico de Wald).

#### Hallazgos Semánticos y Deducciones (-0.5 pts)
1. **Sesgo de Longitud en `multiple_select` (`biased_ms_pct = 44.16%`):** En **136 de los 308 reactivos MS**, las opciones correctas son sistemáticamente más largas y detalladas (incluyendo condiciones formales de regularidad o acotaciones matemáticas completas) que los distractores (ej. `Q-C01-016` a `Q-C01-020`, `Q-C03-081` a `Q-C03-085`, `Q-Hab03-184` a `Q-Hab03-188`). Esto permite a un estudiante con heurísticas de examen identificar opciones verdaderas por densidad tipográfica.
2. **Inyección de Parámetros Numéricos "Muertos" (Ruido Paramétrico Artificial):** Para cumplir formalmente con la instanciación paramétrica en reactivos conceptuales o de `multiple_select`, las plantillas inyectan valores numéricos irrelevantes tanto en el enunciado como dentro de las opciones teóricas:
   - En `Q-Hab08-451`: *"Considere el parámetro $\theta=88$ y muestra $n=30$. ¿Qué afirmaciones sobre insesgadez y sesgo son verdaderas?"* $\to$ Opción A: *"Si $E[\hat{\theta}]$ no existe con $\theta=88$, el sesgo no está definido."*
   - En `Q-C22-651`: *"Al estudiar $X_n \xrightarrow{a.s.} 32$ con tolerancia $\epsilon=0.6$ desde $n=41$, señale el enunciado correcto: $P(\lim_{n\to\infty} X_n = 32) = 1$"* (los valores $\epsilon=0.6$ y $n=41$ no participan en la definición del límite casi seguro).
   - En `Q-C33-1031`: *"Evalúe las condiciones de validez del método delta cuando $\hat{\beta}_1=36, \hat{\beta}_2=19$ y $v_1=62$."* $\to$ Opción A: *"Si $G=0$ en el valor verdadero (con $\hat{\beta}_1=36, v_1=62$), la aproximación de primer orden falla."*
3. **Desconexión entre Generación Aritmética del Distractor y su Rationale Conceptual en `C-12` (`Q-C12-401`, `Q-C12-402`):** En `Q-C12-401`, se pide calcular la media muestral realizada $\bar{y}_{42} = 815/42 = 19.40$. Los 6 distractores (`18.11`, `19.88`, `18.52`, `20.90`, `20.38`, `18.95`) fueron generados dividiendo entre $n\pm 1, n\pm 2, n\pm 3$, pero sus `error_rationale` atribuyen esos valores a confusiones puramente verbales (*"Confunde el estimador aleatorio con una estimación fija"*, *"Mezcla poblaciones distintas"*) sin explicar qué operación numérica produjo `19.88` o `18.95`.

---

### Dimensión 3: Andamiaje Socrático, Pistas y Retroalimentación Diagnóstica — **4.4 / 5.0**

#### Fortalezas Verificadas
- **Cobertura Total de Andamiaje:** El 100% de los reactivos (1,390/1,390) cuenta con 3 pistas progresivas (`hints`), `misconception_warning`, `detailed_solution` y `error_rationale` en cada distractor, con 0 fugas directas de la respuesta final en las pistas (`hint_answer_leak = 0`).

#### Hallazgos Semánticos y Deducciones (-0.6 pts)
1. **Colisión de Interpolación Numérica sin Operador en `error_rationale` (Error Crítico de Renderizado Semántico):**
   - En `Q-C39-1191` ($\alpha=0.5, n=146$) y `Q-C39-1192` ($\alpha=0.75, n=178$), la plantilla interpoló `2{alpha}-1` y `2{alpha}` sin símbolo de multiplicación (`\cdot`). Como resultado, el estudiante lee en LaTeX:
     - `Q-C39-1191` (`opt_b`): `"Omisión de regla: Ignora el término -1 en el exponente de n y evalúa $146^{20.5}$."` (donde $2 \times 0.5$ se concatenó como `20.5`).
     - `Q-C39-1191` (`opt_c`): `"Desliz analítico: Invierte el signo del exponente y calcula $146^{-(20.5-1)}$."`
     - `Q-C39-1192` (`opt_b`): `"Omisión de regla: Ignora el término -1 en el exponente de n y evalúa $178^{20.75}$."` (donde $2 \times 0.75$ se concatenó como `20.75`).
   - En `Q-C06-191` ($a=4, \mu=12, b=10$) y `Q-C06-192` ($a=2, \mu=6, b=4$), el rationale interpoló `{a}{mu}` sin operador: `"calculando $(412+10)^2$"` (en vez de $(4\cdot 12 + 10)^2$), `"calcula $26^2+20$"` (en vez de $2\cdot 6^2 + 20$) y `"calculando $(26+4)^2$"` (en vez de $(2\cdot 6 + 4)^2$).
   - En `Q-C05-141` ($\delta=63$) y `Q-C05-142` ($\delta=34$), el rationale escribió `"$(12+63)/(263)$"` y `"$(24+34)/(234)$"` (concatenando `2` y `{delta}` como `263` y `234`).
2. **`misconception_warning` Truncado (Fórmula Invertida Cruda sin Advertencia) en FIB `C-01`:**
   - En `Q-C01-006` a `Q-C01-010`, el campo `misconception_warning` contiene únicamente el string `"$\\mathrm{Sesgo}(\\hat{\\theta}_n)=\\theta-\\mathbb{E}[\\hat{\\theta}_n]$"`, sin ningún texto que advierta al estudiante que esa ecuación tiene el signo invertido. Presentado aisladamente en la interfaz, induce al error en lugar de prevenirlo.
3. **Sustitución Parcial o Errónea de la Variable Muda $n$ en `hints` y Valores Hardcodeados en `misconception_warning`:**
   - En `Q-C14-531` y `Q-C14-532` ($n=3$), la Pista 1 dice: `"Recuerde que la esperanza de $m_2$ es $\\frac{n-1}{3}\\sigma^2$"` (sustituyó la $n$ del denominador por `3` pero dejó `n-1` simbólico en el numerador).
   - En `Q-Hab06-331` ($n=11$) y `Q-Hab06-332` ($n=10$), la Pista 2 indica: `"Tome $a^{11}\\to 0$ cuando $n\\to\\infty$"` y `"Tome $a^{10}\\to 0$ cuando $n\\to\\infty$"` (interpoló el valor fijo de $n$ en el exponente de $a^n$, haciendo matemáticamente absurdo el paso al límite).
   - En `Q-Hab12-621` y `Q-Hab12-622` (donde el sesgo es $12/n$ o $14/n$ y $\sigma^2=26$ o $78$), el `misconception_warning` conserva números fijos de otro problema: `"Eleve el sesgo $5/n$ al cuadrado para obtener $25/n^2$ antes de sumarlo con la varianza $100/n$."`
   - En `Q-Hab25-1331` y `Q-Hab25-1332` (donde $ee(\bar{Y}_1)=144, ee(\bar{Y}_2)=73$), el `misconception_warning` dice: `"por lo que debe elevar al cuadrado $20^2=400$ y $50^2=2500$."`
4. **Unicidad de Rationales (56.18%) y Prefijos Taxonómicos Mecánicos:**
   - Las pistas socráticas son estáticas e idénticas entre las 5 instancias de cada arquetipo (ej. `Q-C01-001` a `Q-C01-005`). Asimismo, en los `error_rationale` se utilizan prefijos rotativos (`"Inversión de fórmula:"`, `"Falta de ponderación:"`, `"Omisión de regla:"`) que a veces contradicen el contenido del error (ej. en `Q-Hab01-041` `opt_a`, el rationale afirma *"Saca 1/18 de la varianza sin elevarlo al cuadrado en 67/18, reportando 67.0000"*, cuando $67/18 = 3.7222 \neq 67.0000$).

---

### Dimensión 4: Alineación Instruccional y Cobertura Curricular (QM) — **3.7 / 4.0**

#### Fortalezas Verificadas
- **Trazabilidad Bibliográfica Exacta:** Las 57 competencias están ancladas con página/diapositiva exacta y cita textual (`quote`) verificable sobre los 4 documentos de referencia del curso (`01_semana_9_apuntes.pdf`, `02_EST3_LEC07_26.2_V2.pdf`, `03_EST3_LEC08_26.2_v1.pdf`, `04_semana_10_apuntes.pdf`).
- **Calibración ZPD Tri-Banda Completa:** Las 57 competencias cuentan con reactivos en las 3 bandas (`easy`: 25.83%, `medium`: 28.06%, `hard`: 46.12%), con un 98.93% de los ítems de `Skill` situados en niveles cognitivos superiores (`Apply`, `Analyze`, `Evaluate`).

#### Hallazgos Semánticos y Deducciones (-0.3 pts)
1. **Difuminación Práctica entre Competencias `Concept` y `Skill` en la Banda `easy`:** En 26 de las 32 competencias catalogadas como `Concept` (`[C]`), los reactivos de entrada (`easy`, etiquetados a menudo como `Apply`) son ejercicios puramente algorítmicos de sustitución numérica en fórmulas (indistinguibles de los reactivos de `[Hab]`). Inversamente, en `C-25` (`Q-C25-691`), `C-26` (`Q-C26-711`) y `C-27` (`Q-C27-791`), cálculos numéricos explícitos fueron etiquetados como `Understand`, mientras que en `Hab-13` (`Q-Hab13-731`) una pregunta de simple reconocimiento visual de fórmula fue clasificada dentro de una habilidad (`Skill`) con nivel `Understand`.
2. **Desalineación Temática Específica en `C-08` (*"Jerarquía entre Modos de Convergencia"*):** Los reactivos `Q-C08-261` y `Q-C08-262` piden calcular numéricamente una cota de Markov de tercer momento ($\mathbb{E}[|Y_n-Y|^3]/k^3$) en lugar de evaluar las relaciones de implicación lógica entre convergencia casi segura, en media $r$-ésima, en probabilidad y en distribución ($\xrightarrow{a.s.} \Rightarrow \xrightarrow{p} \Rightarrow \xrightarrow{d}$ y $\xrightarrow{r} \Rightarrow \xrightarrow{p}$).

---

### Dimensión 5: Ergonomía Técnica, Sintaxis KaTeX y Resiliencia — **1.8 / 2.0**

#### Fortalezas Verificadas
- **Compilación KaTeX 100% Limpia:** Los linters `katex_syntax_linter` y `katex_frontend_ergonomics_linter` confirman `0` llaves sin cerrar, `0` signos `$` desbalanceados, `0` comandos LaTeX huérfanos fuera de modo matemático, `0` bloques `\text{...}` con prosa extensa y `0` identificadores crudos (`C-01`, `Hab-01`) filtrados en el texto visible para el estudiante.

#### Hallazgos Semánticos y Deducciones (-0.2 pts)
1. **Notación Científica Cruda de Python (`e-05`) dentro de Bloques KaTeX en `Hab-25`:** En `Q-Hab25-1331` y `Q-Hab25-1332`, las plantillas formatearon números pequeños en punto flotante crudo de Python dentro de modo matemático LaTeX (`"$\hat g_2=-7.2e-05$"`, `"$2.8e-05$"`, `"$-9.1e-05$"`, `"$1.1e-04$"`), donde KaTeX renderiza la `e` como la constante de Euler en cursiva seguida de una resta `05`, en lugar de usar notación científica estándar `\times 10^{-5}`. Además, las opciones de respuesta de `Q-Hab25-1331` (`"0.07746"`) están en texto plano sin delimitadores `$`.
2. **Operador Asterisco (`*`) en Modo Matemático (`Hab-14`) y Espaciado en Macros `\mathrm{... }`:** En `Q-Hab14-761` y `Q-Hab14-762`, la opción `opt_f` emplea el asterisco de programación `*` en lugar de `\cdot` (`"$0.73\pm 1.96\sqrt{500*0.73*0.27}$"`). Adicionalmente, varios reactivos (`C-01`, `Hab-20`) incluyen espacios finales dentro de `\mathrm{Sesgo }`, `\mathrm{Var }` y `\widehat{\text{Var }}_{\text{White }}` que generan separación excesiva antes del paréntesis.

---

## 4. Desglose del Mastery Path Readiness Index (`MPRI`: **91.4 / 100.0**)

| Componente MPRI | Peso Máx. | Score Determinista | Score Auditado | Justificación Técnica y Pedagógica |
| :--- | :---: | :---: | :---: | :--- |
| **1. `zpd_adaptive_progression`** | 20.0 | 20.0 | **19.0** | 100% de competencias tri-banda (`easy`/`medium`/`hard`), leve desajuste en etiquetas Bloom `Understand` vs. `Apply`. |
| **2. `retrieval_modality_and_anti_gaming`** | 20.0 | 20.0 | **17.8** | 62.16% de práctica activa (FIB + MS), penalizado por 44.16% de sesgo de longitud en MS y parámetros muertos decorativos. |
| **3. `socratic_scaffolding_lifeline`** | 25.0 | 25.0 | **22.5** | 100% con 3 pistas sin fugas, pero pistas estáticas por arquetipo, `misconception_warning` truncado en `C-01` FIB y sustitución parcial en `C-14`/`Hab-06`. |
| **4. `diagnostic_remediation_alignment`** | 15.0 | 14.91 | **13.3** | 100% cobertura de rationales (56.18% unicidad), afectado por concatenación numérica (`20.5` en `C-39`, `412` en `C-06`) y desconexión aritmética en `C-12`. |
| **5. `dag_and_interleaving_topology`** | 10.0 | 10.0 | **9.3** | DAG conexo sin ciclos (profundidad 7), con redundancia temática entre los 4 documentos fuente. |
| **6. `cognitive_ergonomics_and_framing`** | 10.0 | 10.0 | **9.5** | 0 errores sintácticos KaTeX, fricción menor por floats `e-05` en modo matemático (`Hab-25`) y `*` en `Hab-14`. |
| **TOTAL MPRI** | **100.0** | **99.91** | **91.4** | **GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo** |

---

## 5. Nuevas Reglas Candidatas de Linter (`discovered_lint_rules`)

Como resultado del Loop de Auto-Mejora del Auditor Semántico, se proponen **4 nuevas reglas deterministas** para enriquecer `StandardizedAuditEngine` (`audit_course.py`):

1. **`adjacent_number_interpolation_collision` (Severidad: `HIGH`):**
   - **Patrón:** Detecta en el código de plantilla o en el texto renderizado la concatenación directa de un dígito literal antes de un placeholder numérico sin operador intermedio (ej. `2{alpha}` $\to$ `20.5` en `Q-C39-1191`, `4{mu}` $\to$ `412` en `Q-C06-191`, `2{delta}` $\to$ `263` en `Q-C05-141`).
   - **Regex / Heurística:** Escanear en `error_rationale`, `detailed_solution` y `hints` patrones como `\d+\^\{\d*20\.(5|25|75)` o validar en las plantillas Stage-3 la expresión regular `\d\{[a-zA-Z_]+\}` dentro de entornos `$ ... $`.
2. **`raw_scientific_float_in_katex` (Severidad: `MEDIUM`):**
   - **Patrón:** Detecta números en notación científica cruda de Python (`-7.2e-05`, `2.8e-05`, `1.1e-04`) inyectados directamente dentro de delimitadores `$ ... $` (observado en `Q-Hab25-1331` y `Q-Hab25-1332`), donde KaTeX interpreta `e-05` como la variable $e$ menos $05$.
   - **Regex:** `\$[^$]*\b\d+(?:\.\d+)?e[+-]\d+\b[^$]*\$`.
3. **`bare_formula_misconception_warning` (Severidad: `MEDIUM`):**
   - **Patrón:** Detecta campos `misconception_warning` compuestos exclusivamente por un bloque matemático `$ ... $` sin ningún verbo ni explicación en prosa que indique por qué constituye un error conceptual (observado en `Q-C01-006` a `Q-C01-010`).
   - **Regex:** `^\s*\$[^$]+\$\s*$`.
4. **`hardcoded_limit_exponent_in_hint` (Severidad: `MEDIUM`):**
   - **Patrón:** Detecta pistas o soluciones donde la variable muda de un límite ($n \to \infty$) fue reemplazada accidentalmente por el parámetro numérico instanciado en un lado de la expresión pero mantenida simbólica en el otro (ej. `a^{11}\to 0 cuando n\to\infty` en `Q-Hab06-331` o `\frac{n-1}{3}` en `Q-C14-531`).
   - **Regex:** `(\\frac\{n-[12]\}\{\d+\}|[a-zA-Z]\^\{\d+\}\s*\\to\s*0\s+cuando\s+n\s*\\to\s*\\infty)`.

---

## 6. Plan de Remediación Priorizado

1. **[Prioridad Alta - Dimensión 3] Corregir concatenación de coeficientes e interpolación en plantillas de `C-39`, `C-06`, `C-05`, `C-14`, `Hab-06`, `Hab-12` y `Hab-25`:**
   - Insertar `\cdot` explícito en las plantillas de `C-39` (`2 \cdot {alpha}` en lugar de `2{alpha}`), `C-06` (`{a} \cdot {mu}`) y `C-05` (`2 \cdot {delta}`).
   - Restaurar la variable simbólica $n$ en la Pista 1 de `C-14` (`\frac{n-1}{n}\sigma^2`) y en la Pista 2 de `Hab-06` (`a^n \to 0`), y parametrizar o generalizar los valores hardcodeados en el `misconception_warning` de `Hab-12` y `Hab-25`.
   - Agregar prosa explicativa al `misconception_warning` de los reactivos FIB `Q-C01-006` a `Q-C01-010` (ej. *"Evite invertir el orden de la resta escribiendo $\mathrm{Sesgo}(\hat{\theta}_n)=\theta-\mathbb{E}[\hat{\theta}_n]$"*).
2. **[Prioridad Media - Dimensión 2] Equilibrar longitud de opciones en `multiple_select` y depurar parámetros decorativos:**
   - Expandir el detalle técnico de los distractores en los 136 ítems MS reportados por `ms_length_bias_linter` para reducir el `biased_ms_pct` por debajo del 15%.
   - Eliminar la inyección de asignaciones numéricas irrelevantes (`con \hat{\beta}_1=36, v_1=62`) dentro del texto de las opciones de selección múltiple en `Hab-08`, `C-22` y `C-33`.
3. **[Prioridad Media - Dimensión 1] Consolidación de competencias inter-documento:**
   - En futuras regeneraciones del grafo, fusionar los pares redundantes entre apuntes de clase y diapositivas (`C-01`/`Hab-08`, `C-05`/`Hab-10`, `Hab-03`/`C-17`, `C-30`/`Hab-22`) y posicionar los nodos axiomáticos (`C-10`, `C-11`, `C-12`) al inicio de la topología.
4. **[Prioridad Baja - Dimensión 5] Formateo LaTeX de punto flotante en `Hab-25` y operador `\cdot` en `Hab-14`:**
   - Formatear los valores en notación científica usando `\times 10^{-5}` en lugar de `e-05` en `Hab-25`, envolver las opciones numéricas de `Hab-25` entre signos `$`, y reemplazar `*` por `\cdot` en `Q-Hab14-761`/`762`.

---

<details>
<summary>Metadatos Estructurados (JSON)</summary>

```json
{
  "course_id": "estadistica_3_pre_pc2",
  "audit_timestamp": "2026-11-15T10:40:00-05:00",
  "course_status": "ACTIVO",
  "deterministic_baseline": {
    "final_score": 20.0,
    "mpri": 99.91,
    "hard_penalties": []
  },
  "scores": {
    "dimension_1_architecture_granularity": 3.6,
    "dimension_2_assessment_quality": 4.5,
    "dimension_3_scaffolding_hints": 4.1,
    "dimension_4_instructional_alignment": 3.7,
    "dimension_5_technical_ergonomics": 1.8,
    "raw_subtotal": 17.7,
    "penalties_applied": [],
    "final_score": 17.7,
    "quality_tier": "EXCELENTE (17.0 - 20.0 pts)"
  },
  "mastery_path_readiness": {
    "mpri_score": 89.5,
    "mpri_tier": "GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo",
    "sub_indices": {
      "zpd_adaptive_progression": 19.0,
      "retrieval_modality_and_anti_gaming": 17.8,
      "socratic_scaffolding_lifeline": 21.6,
      "diagnostic_remediation_alignment": 12.3,
      "dag_and_interleaving_topology": 9.3,
      "cognitive_ergonomics_and_framing": 9.5
    },
    "student_journey_verdict": "El estudiante experimenta una ruta de aprendizaje adaptativo matemáticamente rigurosa, con 100% de cobertura en las tres bandas de dificultad (easy/medium/hard), 62.16% de práctica de recuperación activa (FIB + MS) y una topología DAG conexa de profundidad 7 sin ciclos. La experiencia de dominio se ve ligeramente atenuada por redundancia temática entre los 4 PDFs fuente, sesgo de longitud en el 44.16% de los reactivos Multiple Select, pistas socráticas estáticas entre clones del mismo arquetipo y defectos puntuales de interpolación numérica en explicaciones de error (C-39, C-06, C-05) y advertencias de concepto erróneo (C-01 FIB, Hab-12, Hab-25)."
  },
  "metrics_summary": {
    "total_competencies": 57,
    "competency_categories": {
      "Fact": 0,
      "Concept": 32,
      "Skill": 25
    },
    "total_questions": 1390,
    "modality_distribution": {
      "multiple_choice_7_options": 526,
      "fill_in_the_blank": 556,
      "multiple_select": 308,
      "active_generation_pct": 62.16
    },
    "difficulty_distribution": {
      "easy": 359,
      "medium": 390,
      "hard": 641
    },
    "bloom_distribution": {
      "Understand": 48,
      "Apply": 638,
      "Analyze": 368,
      "Evaluate": 336
    },
    "distractor_rationale_coverage_pct": 100.0,
    "distractor_rationale_uniqueness_pct": 56.18,
    "ms_length_bias_pct": 44.16,
    "socratic_3_hints_coverage_pct": 100.0,
    "stage5_judge_agreement_rate": 1.0,
    "katex_syntax_errors": 0
  },
  "discovered_lint_rules": [
    {
      "rule_id": "adjacent_number_interpolation_collision",
      "severity": "HIGH",
      "description": "Detecta la concatenación accidental de un coeficiente literal y una variable numérica interpolada sin operador de multiplicación en expresiones LaTeX (ej. '2{alpha}' renderizado como '20.5' en Q-C39-1191 o '4{mu}' como '412' en Q-C06-191).",
      "sample_offending_ids": ["Q-C39-1191", "Q-C39-1192", "Q-C06-191", "Q-C06-192", "Q-C05-141", "Q-C05-142"]
    },
    {
      "rule_id": "raw_scientific_float_in_katex",
      "severity": "MEDIUM",
      "description": "Detecta floats en notación científica cruda de Python (ej. '-7.2e-05', '2.8e-05') dentro de delimitadores matemáticos KaTeX '$...$', donde 'e-05' se renderiza como la constante e menos 05 en lugar de '\\times 10^{-5}'.",
      "sample_offending_ids": ["Q-Hab25-1331", "Q-Hab25-1332"]
    },
    {
      "rule_id": "bare_formula_misconception_warning",
      "severity": "MEDIUM",
      "description": "Detecta campos 'misconception_warning' que contienen únicamente una fórmula matemática '$...$' sin texto explicativo que advierta al estudiante por qué dicha expresión es errónea.",
      "sample_offending_ids": ["Q-C01-006", "Q-C01-007", "Q-C01-008", "Q-C01-009", "Q-C01-010"]
    },
    {
      "rule_id": "hardcoded_limit_exponent_in_hint",
      "severity": "MEDIUM",
      "description": "Detecta pistas socráticas donde la variable muda n de un límite o fracción general fue sustituida parcialmente por el valor numérico instanciado (ej. 'a^{11}\\to 0 cuando n\\to\\infty' o '\\frac{n-1}{3}\\sigma^2').",
      "sample_offending_ids": ["Q-C14-531", "Q-C14-532", "Q-Hab06-331", "Q-Hab06-332"]
    }
  ]
}
```

</details>
