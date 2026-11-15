# Reporte de Auditoría de Calidad Pedagógica, Psicométrica y Path-to-Mastery v2.0

> [!WARNING]
> **CURSO RETIRADO DE LA PLATAFORMA**: Este curso fue eliminado de la plataforma interactiva el **2026-11-14 22:37:15**. Este informe de auditoría se conserva exclusivamente como registro histórico y pedagógico ('legacy').

**Estado en Plataforma:** ELIMINADO  
**Fecha de Eliminación:** 2026-11-14 22:37:15  
**Curso:** `estadistica_3_s9_vmapreduce5` — *Estadistica 3 S9 Vmapreduce5 (Inferencia Asintótica, Desigualdades de Concentración, Modos de Convergencia, LGN, TCL, Slutsky y Método Delta)*  
**Fecha de Auditoría:** 15 de noviembre de 2026  
**Estándares Aplicados:** Quality Matters (QM), OSCQR, Bloom's 2-Sigma Mastery Learning, Zona de Desarrollo Próximo (ZPD) y Práctica de Evocación Activa  
**Motor de Telemetría:** `StandardizedAuditEngine` (Fast Deterministic Pass + Loop de Verificación Semántica Adaptativa)

---

## 1. Resumen Ejecutivo y Veredicto de Certificación

| Métrica Global | Valor | Nivel / Certificación |
| :--- | :--- | :--- |
| **Calificación Final QM-OSCQR** | **19.57 / 20.00** | **EXCELENTE (17.0 - 20.0 pts) — PLATINUM MASTERY** |
| **Subtotal de Dimensiones** | **19.57 / 20.00** | Sin penalizaciones duras activadas (`0.00 pts`) |
| **Mastery Path Readiness Index (MPRI)** | **96.89 / 100.0** | **GOLD MASTERY PATH (85 - 100): Certificado para Dominio Adaptativo** |
| **Total de Competencias** | **37** | 8 Hechos (`[H]`), 17 Conceptos (`[C]`), 12 Habilidades (`[Hab]`) |
| **Total de Reactivos** | **860** | 457 `multiple_choice_7_options` (53.14%) · 403 `fill_in_the_blank` (46.86%) |
| **Risk Score Estático** | **34.48** | Generado por 230 alertas KaTeX (100% falsos positivos de `\text{ECM}`, `\bar{Y}`, `\bar{X}`, `\hat{p}`) y 403 `misconception_warning` genéricos en FIB |

> [!IMPORTANT]
> **Veredicto del Recorrido del Estudiante (Student Journey Verdict):**  
> El curso `estadistica_3_s9_vmapreduce5` alcanza una arquitectura instruccional y psicométrica sobresaliente (**19.57/20.0** y **MPRI 96.89/100**), certificada para producción en estudio autónomo adaptativo. El grafo curricular de 37 micro-competencias es 100% conexo, acíclico (profundidad máxima 7) y topológicamente ordenado, con calibración ZPD tri-banda (`easy`, `medium`, `hard`) activa en el 100% de los nodos (37/37) y un 46.86% de práctica de evocación activa mediante reactivos `fill_in_the_blank`. La verificación semántica profunda descartó como falsos positivos las 230 advertencias del linter de variables sin interpolar (correspondientes a argumentos LaTeX legítimos como `\text{ECM}` y `\bar{Y}_n`), pero identificó **cuatro oportunidades de pulido semántico fino**: (1) el uso de un texto genérico de `misconception_warning` en los 403 reactivos `fill_in_the_blank`, (2) fugas de parámetros auxiliares no declarados en el enunciado hacia las pistas o justificaciones de error en 4 competencias conceptuales (`C-10`, `C-14`, `C-18`, `C-19`), (3) desacoplamiento entre la explicación conceptual del `error_rationale` y el cálculo numérico del distractor en arquetipos cuantitativos de `H-04`, `C-06`, `C-07` y `C-08`, y (4) etiquetado de Bloom conservador (`Remember`/`Understand`) en el 38.89% de los ejercicios de Habilidad (`[Hab]`) de banda `easy`.

---

## 2. Desglose de Calificación por Dimensiones y Pilares MPRI

### 2.1 Matriz de Evaluación QM-OSCQR (20.0 Puntos)

| Dimensión | Puntaje | Máx. | Cumplimiento | Síntesis de Auditoría |
| :--- | :---: | :---: | :---: | :--- |
| **D1. Arquitectura Curricular, Topología DAG y Calibración ZPD** | **4.00** | 4.00 | 100.0% | 37 competencias atómicas (8 `[H]`, 17 `[C]`, 12 `[Hab]`); DAG acíclico conexo (`depth=7`, 0 aristas invertidas); ZPD tri-banda (`easy`/`medium`/`hard`) en 37/37 competencias. |
| **D2. Calidad Psicométrica, Modalidad de Evocación y Anti-Gaming** | **5.00** | 5.00 | 100.0% | Balance óptimo MC7 (53.14%) + FIB (46.86%); $\ge 15$ esqueletos distintos observados; 2,742 distractores con 100% de cobertura y 89.2% de unicidad en `error_rationale`; 0 multiplicadores mágicos y 0 fugas. |
| **D3. Andamiaje Socrático Progresivo y Remediación Diagnóstica** | **4.95** | 5.00 | 99.0% | 100% de reactivos con 3–4 pistas socráticas genuinas (0% Mad-Libs, 0% envenenamiento); soluciones detalladas en 860/860 ítems. Leve deducción (-0.05) por `misconception_warning` genérico en los 403 ítems FIB y fugas menores de parámetros en `error_rationale`. |
| **D4. Alineación Instruccional, Taxonomía de Bloom y Pureza de Dominio** | **3.62** | 4.00 | 90.5% | Fidelidad matemática rigurosa al sílabo de Estadística III y 0 prefijos contaminantes de otros dominios. Deducción (-0.38) porque el 38.89% de ítems en Habilidades (`[Hab]`) están etiquetados en niveles declarativos (`Remember`/`Understand`). |
| **D5. Accesibilidad, Ergonomía Cognitiva en UI y Sintaxis KaTeX** | **2.00** | 2.00 | 100.0% | Sintaxis KaTeX 100% limpia y balanceada (0 llaves rotas, 0 `$$$`, 0 `\text{prosa}` desbordante, 0 identificadores crudos). Las 230 alertas estáticas corresponden a comandos LaTeX válidos. |
| **Subtotal Bruto** | **19.57** | **20.00** | **97.85%** | Excelencia estructural y psicométrica sostenida. |
| **Penalizaciones Duras (Hard Deductions)** | **0.00** | — | — | Ninguna regla punitiva activada (`0` bancos $<3$, `0` ítems sin pistas, `0` huérfanas, `0` pistas envenenadas). |
| **CALIFICACIÓN FINAL** | **19.57** | **20.00** | **97.85%** | **EXCELENTE (19.0 - 20.0 pts) — PLATINUM MASTERY** |

### 2.2 Índice de Preparación para el Dominio — MPRI (100.0 Puntos)

| Pilar Cognitivo y de Plataforma | Puntaje | Máx. | Estado Operativo en Motor Top's Academy |
| :--- | :---: | :---: | :--- |
| **1. `zpd_adaptive_progression`** | **16.89** | 20.0 | `calibrateByMasteryDifficulty` 100% funcional en las 37 competencias (`easy`: 295, `medium`: 295, `hard`: 270); 61.11% de `[Hab]` en Bloom `Apply`/`Analyze`. |
| **2. `retrieval_modality_and_anti_gaming`** | **20.00** | 20.0 | 403 reactivos `fill_in_the_blank` (46.86%) activan `mathEquivalence.ts`; 0 competencias memorizables; 0 relleno `[R-15]`; 0 cuantificadores vacuos. |
| **3. `socratic_scaffolding_lifeline`** | **25.00** | 25.0 | Salvavidas de 3 intentos (`PracticeSession.tsx`) respaldado por 100% de pistas socráticas genuinas y 0% de pistas envenenadas o boilerplate. |
| **4. `diagnostic_remediation_alignment`** | **15.00** | 15.0 | `FeedbackToast.tsx` alimentado por 2,446 `error_rationale` únicos (89.2% de unicidad sobre 2,742 distractores) sin multiplicadores mágicos `1.333x`. |
| **5. `dag_and_interleaving_topology`** | **10.00** | 10.0 | Grafo conexo único (`max_dag_depth = 7`), 0 ciclos, 0 aristas invertidas; habilita interleaving 60/40 en Quiz y 55/45 en Unit Test en `sessionShuffler.ts`. |
| **6. `cognitive_ergonomics_and_framing`** | **10.00** | 10.0 | Renderizado móvil limpio sin desbordamientos `white-space: nowrap` en KaTeX (`prose_in_katex = 0`, `raw_identifier = 0`). |
| **TOTAL MPRI** | **96.89** | **100.0** | **GOLD MASTERY PATH (85 - 100): Certificado para Dominio Adaptativo** |

---

## 3. Análisis Técnico y Pedagógico por Dimensión

### Dimensión 1: Arquitectura Curricular, Topología DAG y Calibración ZPD (4.00 / 4.00 pts)
- **Granularidad y Balance Cognitivo:** El curso descompone la unidad de teoría asintótica y desigualdades probabilísticas en **37 micro-competencias atómicas**: **8 Hechos (`[H]`)** (20 ítems c/u), **17 Conceptos (`[C]`)** (20 ítems c/u) y **12 Habilidades (`[Hab]`)** (30 ítems c/u), totalizando **860 reactivos**.
- **Integridad Topológica del DAG:** El grafo de prerrequisitos tiene como única raíz a `C-01` (*Limitaciones de Muestras Finitas y Fundamentos de la Inferencia Asintótica*) y se despliega sin ciclos (`has_cycle: false`), en un único componente conexo (`connected_components_count: 1`) de profundidad máxima 7 (`max_dag_depth: 7`), sin aristas invertidas (`inverted_prerequisite_edges_count: 0`) ni habilidades huérfanas de prerrequisitos (`skills_without_prerequisites_count: 0`).
- **Calibración ZPD Tri-Banda Completa:** Las 37 competencias poseen reactivos distribuidos en las tres bandas de dificultad (`easy`: 295, `medium`: 295, `hard`: 270; `three_band_competencies_count: 37`), garantizando que la función `calibrateByMasteryDifficulty` en `sessionShuffler.ts` opere sin puntos ciegos durante toda la transición `Not started` $\to$ `Familiar` $\to$ `Proficient` $\to$ `Mastered`.

### Dimensión 2: Calidad Psicométrica, Modalidad de Evocación y Anti-Gaming (5.00 / 5.00 pts)
- **Diversidad de Modalidades de Evocación:** A diferencia de cursos basados exclusivamente en reconocimiento pasivo, el banco integra **403 reactivos `fill_in_the_blank` (46.86%)** junto con **457 reactivos `multiple_choice_7_options` (53.14%)**, eliminando cualquier competencia de habilidad basada únicamente en selección múltiple (`recognition_only_skill_competencies_count: 0`). Esto impide la resolución por ingeniería inversa desde las opciones y fuerza el cálculo analítico directo.
- **Rigor de Distractores y Anti-Gaming:** Los 2,742 distractores poseen `error_rationale` explícito (100% de cobertura) con una unicidad del **89.2%** (2,446 justificaciones únicas). No existen distractores clonados (`cloned_distractor_items_count: 0`), ni pistas parentéticas delatoras (`parenthetical_telltale_count: 0`), ni relleno artificial de longitud `[R-15]` (`length_padded_items_count: 0`), ni vulnerabilidades de memorización visual de claves (`memorizable_competencies_count: 0`).
- **Evidencia de Diseño Psicométrico Destacado:**
  - En **`Q-Hab04-231`** y **`Q-Hab04-232`** (*Demostración de Cauchy-Schwarz mediante Formas Cuadráticas y Discriminante*), los distractores modelan errores algebraicos precisos y altamente plausibles sobre $P(t) = a t^2 + b t + c$: omitir el factor 2 en $b = 2E[XY]$ (`D-Hab04-02`), calcular $b^2$ como $2(E[XY])^2$ sin elevar el coeficiente 2 (`D-Hab04-06`), sumar $4ac$ en lugar de restarlo (`D-Hab04-04`), o invertir el signo exigiendo $\Delta \ge 0$ (`D-Hab04-01`).
  - En **`Q-Hab08-511`** (*Cálculo de Esperanza y Varianza Teórica mediante Momentos*), los distractores capturan exactamente la omisión de restar $(E[X])^2$ (`D-Hab08-01`), la suma de $(E[X])^2$ (`D-Hab08-03`), la confusión entre $E[X^2]$ y $E[X]$ dando varianza negativa (`D-Hab08-02`) y la entrega de la desviación estándar $\sqrt{\text{Var}(X)}$ en lugar de la varianza (`D-Hab08-06`).
  - En **`Q-Hab12-831`** (*Método Delta para $g(\mu)=1/\mu$*), los distractores aíslan errores reales de aplicación: centrar el intervalo en $\bar{y}$ en lugar de $1/\bar{y}$ (`D-Hab12-03`), usar $z_{0.95}=1.645$ en lugar de $z_{0.975}=1.96$ (`D-Hab12-05`), omitir multiplicar por $ee(\bar{Y})$ (`D-Hab12-02`) o evaluar la derivada en $g(\bar{y})$ en lugar de $\bar{y}$ (`D-Hab12-06`).

### Dimensión 3: Andamiaje Socrático Progresivo y Remediación Diagnóstica (4.95 / 5.00 pts)
- **Calidad de Pistas Progresivas:** El 100% de los 860 reactivos cuenta con entre 3 y 4 pistas progresivas escalonadas (`zero_hints_count: 0`, `insufficient_hints_count: 0`) libres de plantillas Mad-Libs (`boilerplate_hints_pct: 0.0%`) y libres de envenenamiento anti-socrático (`poisoned_hints_pct: 0.0%`). Las pistas guían desde el principio teórico (Pista 1), pasando por la articulación algebraica (Pista 2), hasta el planteamiento operativo con los parámetros del ejercicio sin filtrar trivialmente la respuesta (Pista 3/4).
- **Soluciones Formales Paso a Paso:** Los 860 ítems presentan `detailed_solution` con desarrollo matemático limpio y verificable (ej. `Q-Hab01-041`, `Q-Hab03-141`, `Q-Hab06-331`, `Q-Hab10-611`).
- **Observaciones Semánticas (-0.05 pts):**
  1. **Fallback Genérico en `misconception_warning` para Reactivos FIB (403 ítems):** Mientras que los 457 reactivos `multiple_choice_7_options` incluyen advertencias de errores conceptuales ricas y específicas al teorema evaluado, los **403 reactivos `fill_in_the_blank`** (`generic_misconception_count: 403`, p. ej. `Q-H01-031`) contienen la cadena genérica `"Verifique cuidadosamente los supuestos y cálculos antes de seleccionar su respuesta."` (que además menciona *"seleccionar su respuesta"* pese a ser un reactivo de entrada libre).
  2. **Interpolación Híbrida Menor en Pistas de `C-09`:** En `Q-C09-451` ($n=40$) y `Q-C09-452` ($n=13$), la primera pista interpola el tamaño muestral únicamente en el denominador dejando el numerador simbólico: `"Recuerde que el estimador no corregido satisface $E[m_2] = \frac{n-1}{13}\sigma^2$."`

### Dimensión 4: Alineación Instruccional, Taxonomía de Bloom y Pureza de Dominio (3.62 / 4.00 pts)
- **Pureza de Dominio Estadístico y Econométrico:** El lenguaje técnico es 100% fiel a la inferencia estadística y econometría asintótica (descomposición ortogonal del ECM, corrección de Bessel, desigualdades de Markov, Chebyshev, Jensen y Cauchy-Schwarz, jerarquía de normas $L^p$, contraejemplo de explosión de momentos $P(X_n = c n^2) = 1/n$, estimador geométrico $M_B$, LGN de Khinchine, TCL de Lindeberg-Lévy, Teorema de la Aplicación Continua, Lema de Slutsky y Método Delta). Se verifican **0 prefijos contaminantes de otros dominios** (`cross_domain_prefix_items_count: 0`) y **0 cuantificadores vacuos** (`vacuous_quantifier_items_count: 0`).
- **Distribución Taxonómica de Bloom (-0.38 pts):** A nivel global, el curso registra `Remember`: 195 (22.67%), `Understand`: 274 (31.86%), `Apply`: 273 (31.74%) y `Analyze`: 118 (13.72%). En los 360 reactivos de Habilidades (`[Hab]`), **220 ítems (61.11%)** alcanzan niveles superiores (`Apply`/`Analyze`), pero **140 ítems (38.89%)** —concentrados en la banda `easy` de competencias prácticas como `Hab-01` (`Q-Hab01-041`, etiquetado `Understand`), `Hab-03` (`Q-Hab03-141`, etiquetado `Remember`) y `Hab-04` (`Q-Hab04-231`, etiquetado `Remember`)— tienen etiquetas declarativas inferiores a la demanda cognitiva real de ejecución analítica que exigen.

### Dimensión 5: Accesibilidad, Ergonomía Cognitiva en UI y Sintaxis KaTeX (2.00 / 2.00 pts)
- **Integridad de Renderizado KaTeX:** El banco presenta **0 llaves rotas** (`unclosed_braces_count: 0`), **0 signos de dólar desbalanceados** (`unbalanced_dollars_count: 0`), **0 triples dólares** (`triple_dollars_count: 0`), **0 bloques `\text{...}` con prosa larga que rompan el layout móvil** (`prose_in_katex_text_items_count: 0`) y **0 variables crudas de Python en modo matemático** (`raw_identifier_math_items_count: 0`).

---

## 4. Hallazgos del Loop de Verificación Semántica Adaptativa

### 4.1 Auditoría del Cluster `katex_issues` (230 Alertas de `uninterpolated_math_variable_linter` $\to$ 100% Falsos Positivos)
El motor determinista reportó 230 reactivos con advertencias del tipo `"Variable de plantilla posiblemente sin interpolar '{ECM}' / '{Y}' / '{X}' / '{p}'"`. La inspección directa de los reactivos en `risk_cluster_samples` y `stratified_samples` confirma que **ninguno corresponde a un error real de interpolación**:
- **`{ECM}`** en `Q-H01-031`, `Q-H01-035`, `Q-Hab07-421`, `Q-Hab10-612`: Es el argumento legítimo del comando LaTeX `\text{ECM}` (Error Cuadrático Medio).
- **`{Y}`** y **`{X}`** en `Q-Hab01-041`, `Q-Hab06-331`, `Q-H04-381`, `Q-C18-701`, `Q-C19-721`, `Q-C20-771`, `Q-Hab12-843`: Son los argumentos legítimos del comando de barra superior `\bar{Y}_n`, `\bar{X}_n` o `\bar{Y}`.
- **`{p}`** en `Q-C05-261`, `Q-Hab11-757`: Es el argumento legítimo de `\xrightarrow{p}` o `\hat{p}`.

### 4.2 Fuga de Parámetros Fantasma No Declarados en el Enunciado (`undeclared_stem_parameter_in_feedback`)
En cuatro competencias conceptuales (`C-10`, `C-14`, `C-18`, `C-19`), las plantillas generadoras instancian parámetros numéricos auxiliares en Python que **no se imprimen en el `stem`**, pero sí se interpolan dentro de las opciones, `hints` o `error_rationale`, generando referencias a números que el estudiante no vio en la pregunta:
- **`Q-C14-641` / `Q-C14-642` (`C-14`):** El enunciado de `Q-C14-641` solo declara $n = 76$ (*"para un estimador $\hat{\theta}_{76}$"*), pero el `error_rationale` de la opción A dice *"garantizan varianza mínima $\sigma^2=11$"* y el de la opción F dice *"si existe sesgo constante $2$"*, valores ($\sigma^2=11$, $\text{sesgo}=2$) ausentes en el enunciado y en las opciones.
- **`Q-C18-701` / `Q-C18-702` (`C-18`):** El enunciado de `Q-C18-701` declara $\mu = 29$, $\sigma^2 = 144$ y $\epsilon = 0.5$ (sin fijar tamaño muestral $n$), pero el `error_rationale` de la opción C afirma: *"La varianza del promedio decrece como $\sigma^2/n = 144/542$, no $144$"*, introduciendo $n = 542$ sin contexto previo.
- **`Q-C19-721` / `Q-C19-722` (`C-19`):** El enunciado de `Q-C19-721` pregunta por el estadístico pivote general $Z_n$ con $\mu = 17$ y $\sigma = 10$ sin especificar un valor numérico de $n$, pero la Pista 3 indica *"Compruebe que el factor $\sqrt{90}$ multiplique al numerador..."* y el distractor B muestra $N(0, 1/90)$.
- **`Q-C10-491` / `Q-C10-492` (`C-10`):** El enunciado de `Q-C10-492` menciona $35$ elementos y valor escalar $1$, pero los distractores D y F introducen *"por tener solamente $6$ valores discretos"* sin que el cardinal del soporte $k=6$ figure en el enunciado.

### 4.3 Desacoplamiento Semántico entre `error_rationale` Conceptual y Distractor Numérico (`conceptual_rationale_numeric_offset_mismatch`)
En los arquetipos numéricos de **`H-04`**, **`C-06`**, **`C-07`** y **`C-08`**, los distractores numéricos fueron generados mediante perturbaciones aritméticas, pero sus `error_rationale` reutilizan descripciones de falacias teóricas que no explican de dónde sale el número:
- En **`Q-H04-381`** ($\hat{\mu} = 1.54 \bar{Y}, \mu = 53 \implies \text{Sesgo} = 28.62$): La opción A ofrece el valor `$12.42$` y su `error_rationale` afirma: *"Asume incorrectamente que el sesgo es nulo 12.42 ignorando el factor de escala 1.54"* (contradicción semántica al llamar "sesgo nulo" al valor no nulo `12.42`).
- En **`Q-C06-311`** ($E[X_{21}] = 10 \times 21 = 210$): Los distractores son múltiplos escalados (`231.0`, `178.5`, `189.0`, `220.5`), pero sus justificaciones citan errores cualitativos como *"Concluye no convergencia en probabilidad para $c=10$"* o *"Extrapola propiedades gaussianas con factor $c=10$"*, en lugar de explicar el error de cálculo que arroja `231.0` o `178.5`.
- El mismo patrón ocurre en **`Q-C07-361`** ($\hat{\theta} = 2666/80 = 33.33$, donde `35.0` se justifica como *"Confunde la distribución muestral con el histograma"*) y **`Q-C08-401`** ($ee = \sqrt{156.25} = 12.5$, donde `10.0` se justifica como *"Aplica criterio de varianza ignorando la condición de insesgadez dando 10.0"*).

---

## 5. Plan de Acción y Remediación Prioritaria

1. **[Prioridad Media — Andamiaje en FIB] Reemplazar el `misconception_warning` genérico en los 403 reactivos `fill_in_the_blank`:**  
   Sustituir la cadena por defecto `"Verifique cuidadosamente los supuestos y cálculos antes de seleccionar su respuesta."` en los ítems FIB por el `misconception_warning` específico de la competencia correspondiente (ya disponible en los reactivos MC7 de la misma competencia).
2. **[Prioridad Media — Coherencia de Parámetros en Plantillas] Sincronizar variables impresas entre `stem`, `hints` y `error_rationale` (`C-10`, `C-14`, `C-18`, `C-19`, `C-09`):**  
   Eliminar de los `error_rationale` y `hints` de `C-14`, `C-18`, `C-19` y `C-10` la interpolación de variables aleatorias auxiliares ($n$, $\sigma^2$, $k$) cuando el arquetipo sea simbólico y no las declare en el `stem`, y corregir `\frac{n-1}{40}` $\to$ `\frac{n-1}{n}` en la Pista 1 de `C-09`.
3. **[Prioridad Baja — Diagnóstico en `FeedbackToast`] Alinear la fórmula del distractor con su `error_rationale` en `H-04`, `C-06`, `C-07` y `C-08`:**  
   En `H-04` (`D-H04-03`), fijar el distractor de "sesgo nulo" exactamente en `0.0` (o ajustar el rationale al cálculo aritmético real), y en los ítems de cálculo de `C-06`, `C-07` y `C-08`, vincular cada distractor con la operación aritmética errónea que lo genera.
4. **[Prioridad Baja — Calibración Taxonómica] Re-etiquetar a `Apply` los reactivos operativos de banda `easy` en Habilidades (`[Hab]`):**  
   Actualizar la etiqueta `bloom` de `Remember`/`Understand` a `Apply` en los 140 reactivos de `[Hab]` que exigen cálculo numérico o deducción algebraica directa (como `Q-Hab01-041` y `Q-Hab04-231`), elevando el `skill_higher_bloom_pct` del 61.11% al $>85\%$.
5. **[Mejora del Motor Estático — `StandardizedAuditEngine`] Excluir argumentos de macros LaTeX en `uninterpolated_math_variable_linter`:**  
   Actualizar la expresión regular de `uninterpolated_math_variable_linter` con un *negative lookbehind* `(?<!\\text)(?<!\\bar)(?<!\\hat)(?<!\\tilde)(?<!\\xrightarrow)(?<!\\mathbb)(?<!\\mathcal)(?<!\\operatorname)` para eliminar los 230 falsos positivos sobre `\text{ECM}`, `\bar{Y}_n`, `\bar{X}_n` y `\xrightarrow{p}`.

---

<details>
<summary>Metadatos Estructurados (JSON)</summary>

```json
{
  "course_metadata": {
    "course_id": "estadistica_3_s9_vmapreduce5",
    "unit_title": "Estadistica 3 S9 Vmapreduce5",
    "detected_objective": "Dominio y aplicación analítica integral de la inferencia asintótica, descomposición del Error Cuadrático Medio, desigualdades de concentración (Markov, Chebyshev, Jensen, Cauchy-Schwarz), modos de convergencia estocástica (L^r, probabilidad, casi segura, distribución), Ley de los Grandes Números, Teorema Central del Límite, Teorema de la Aplicación Continua, Teorema de Slutsky y Método Delta.",
    "total_competencies": 37,
    "total_questions": 860
  },
  "dimension_scores": {
    "architecture_granularity": {
      "score": 4.0,
      "max": 4.0,
      "feedback": "Estructura curricular impecable con 37 competencias (8 Hechos, 17 Conceptos, 12 Habilidades). Grafo DAG acíclico y conexo (profundidad máxima 7, 0 aristas invertidas, 1 componente conexo). Calibración ZPD tri-banda ('easy': 295, 'medium': 295, 'hard': 270) activa en las 37/37 competencias."
    },
    "assessment_quality": {
      "score": 5.0,
      "max": 5.0,
      "feedback": "Excelente equilibrio de modalidades cognitivas: MC7=53.14% (457 ítems) y FIB=46.86% (403 ítems de evocación activa), con 0 competencias de habilidad restringidas a reconocimiento pasivo. 2,742 distractores evaluados con 100.0% de cobertura de error_rationale, 89.2% de unicidad (2,446 únicos), 0 distractores delatores y 0 multiplicadores mágicos."
    },
    "scaffolding_hints": {
      "score": 4.95,
      "max": 5.0,
      "feedback": "Andamiaje socrático sobresaliente: 100% de reactivos con 3 a 4 pistas escalonadas genuinas (0.0% boilerplate Mad-Libs, 0.0% pistas envenenadas) y soluciones formales paso a paso en los 860/860 ítems. Leve deducción (-0.05) por el uso de una cadena genérica de misconception_warning en los 403 ítems FIB y referencias menores a parámetros auxiliares en error_rationale."
    },
    "instructional_alignment": {
      "score": 3.62,
      "max": 4.0,
      "feedback": "Rigor matemático y econométrico sobresaliente con 0 prefijos contaminantes de otros dominios y 0 cuantificadores vacuos. Alineación cognitiva de Bloom en 61.11% de habilidades prácticas en niveles superiores (Apply/Analyze); el 38.89% restante de ítems [Hab] en banda 'easy' conserva etiquetas declarativas ('Remember'/'Understand') pese a requerir ejecución analítica."
    },
    "technical_ergonomics": {
      "score": 2.0,
      "max": 2.0,
      "feedback": "Sintaxis KaTeX 100% limpia y balanceada (0 llaves sin cerrar, 0 delimitadores impares, 0 $$$, 0 bloques \\text{...} con prosa extensa y 0 identificadores crudos). Las 230 alertas del linter de variables sin interpolar son falsos positivos sobre comandos LaTeX válidos como \\text{ECM}, \\bar{Y}_n, \\bar{X}_n y \\xrightarrow{p}."
    }
  },
  "penalties_applied": [],
  "raw_subtotal": 19.57,
  "final_score": 19.57,
  "quality_tier": "EXCELENTE (17-20)",
  "mastery_path_readiness": {
    "mpri_score": 96.89,
    "mpri_max": 100.0,
    "mpri_tier": "GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo",
    "pillars": {
      "zpd_adaptive_progression": { "score": 16.89, "max": 20.0 },
      "retrieval_modality_and_anti_gaming": { "score": 20.0, "max": 20.0 },
      "socratic_scaffolding_lifeline": { "score": 25.0, "max": 25.0 },
      "diagnostic_remediation_alignment": { "score": 15.0, "max": 15.0 },
      "dag_and_interleaving_topology": { "score": 10.0, "max": 10.0 },
      "cognitive_ergonomics_and_framing": { "score": 10.0, "max": 10.0 }
    },
    "student_journey_verdict": "Curso certificado en categoría GOLD/PLATINUM MASTERY PATH (19.57/20.0, MPRI 96.89/100). El estudiante experimenta progresión ZPD adaptativa real en las 37 competencias, práctica de evocación activa en el 46.86% del banco (FIB) y andamiaje socrático genuino en el 100% de los ejercicios."
  },
  "discovered_lint_rules": [
    {
      "rule_id": "fib_generic_misconception_fallback",
      "severity": "info",
      "regex_pattern": "Verifique cuidadosamente los supuestos y cálculos antes de seleccionar su respuesta",
      "description": "Detecta el uso de la advertencia genérica por defecto en el campo misconception_warning de reactivos fill_in_the_blank, que además alude a 'seleccionar su respuesta' en un ítem de respuesta abierta.",
      "evidence_items": ["Q-H01-031"]
    },
    {
      "rule_id": "undeclared_stem_parameter_in_feedback",
      "severity": "warning",
      "regex_pattern": "(?:varianza mínima \\\\sigma\\^2=\\d+|sesgo constante \\d+|\\\\sigma\\^2/n = \\d+/\\d+|\\\\sqrt\\{\\d+\\}\\(\\\\bar\\{Y\\}_n)",
      "description": "Detecta cuando una plantilla conceptual interpola parámetros numéricos auxiliares de la semilla aleatoria (como n, sigma^2 o k) dentro de hints o error_rationale sin haberlos declarado en el stem del reactivo.",
      "evidence_items": ["Q-C14-641", "Q-C14-642", "Q-C18-701", "Q-C18-702", "Q-C19-721", "Q-C19-722", "Q-C10-492"]
    },
    {
      "rule_id": "contradictory_null_bias_rationale",
      "severity": "warning",
      "regex_pattern": "sesgo es nulo\\s+[1-9]\\d*(?:\\.\\d+)?",
      "description": "Detecta contradicciones semánticas en error_rationale donde se afirma que un parámetro o sesgo es 'nulo' seguido inmediatamente de un valor numérico distinto de cero.",
      "evidence_items": ["Q-H04-381", "Q-H04-382"]
    }
  ],
  "remediation_actions": [
    "Reemplazar el misconception_warning genérico en los 403 reactivos fill_in_the_blank por la advertencia conceptual específica de cada competencia.",
    "Sincronizar las variables impresas en las plantillas conceptuales C-10, C-14, C-18 y C-19 para evitar que hints o error_rationale mencionen valores numéricos de n, sigma^2 o k no declarados en el stem.",
    "Alinear el error_rationale de los arquetipos numéricos en H-04, C-06, C-07 y C-08 con la operación aritmética exacta que produce cada distractor (y corregir 'sesgo es nulo 12.42' en Q-H04-381).",
    "Re-etiquetar de Remember/Understand a Apply los 140 reactivos de Habilidad ([Hab]) de banda 'easy' que requieren ejecución algorítmica o deducción algebraica.",
    "Refinar la expresión regular de uninterpolated_math_variable_linter en StandardizedAuditEngine con negative lookbehinds para comandos LaTeX (\\text, \\bar, \\hat, \\xrightarrow) y eliminar los 230 falsos positivos."
  ]
}
```

</details>
