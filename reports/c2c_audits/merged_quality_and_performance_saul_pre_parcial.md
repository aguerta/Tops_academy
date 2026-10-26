# Reporte Unificado de Auditoría Determinista: Calidad Estática y Telemetría Multi-Agente
## Curso: Saul Pre Parcial (`saul_pre_parcial`)
### Plataforma Top's Academy — Pipeline Content-to-Course (C2C) v3.2

---

**Fecha de Consolidación:** 25 de Octubre de 2026  
**Identificador del Curso:** `saul_pre_parcial`  
**Conversación Orquestadora Auditada:** [`201fa8ef-682b-4a7e-bdbd-88394a8ac506`](conversation://201fa8ef-682b-4a7e-bdbd-88394a8ac506)  
**Calificación / Risk Score:** **18.0 / 20.0 (EXCELENTE (17.0 - 20.0 pts))**  
**Tiempo de Pared Global:** **26.15 minutos** | **Cómputo Total de Agentes:** **333.88 minutos** | **Speedup:** **12.77x**  

---

## Tabla de Contenidos

- [PARTE I: TELEMETRÍA ESTÁTICA Y LINTERS DE CALIDAD (`StandardizedAuditEngine`)](#parte-i-telemetría-estática-y-linters-de-calidad-standardizedauditengine)
  - [1. Resumen Consolidado de Linters Deterministas](#1-resumen-consolidado-de-linters-deterministas)
  - [2. Resultados por Linter y Dimensión](#2-resultados-por-linter-y-dimensión)
  - [3. Clusters de Riesgo e Incidencias Detectadas](#3-clusters-de-riesgo-e-incidencias-detectadas)
  - [4. Muestra de Control Estratificada](#4-muestra-de-control-estratificada)
  - [5. Reglas de Linting Registradas (`discovered_lint_rules`)](#5-reglas-de-linting-registradas-discovered_lint_rules)
- [PARTE II: AUDITORÍA FORENSE DE RENDIMIENTO Y TELEMETRÍA (RUN AUDITOR)](#parte-ii-auditoría-forense-de-rendimiento-y-telemetría-run-auditor)
  - [6. Consolidación de Métricas de Rendimiento y Ratios Unitarios](#6-consolidación-de-métricas-de-rendimiento-y-ratios-unitarios)
  - [7. Distribución Empírica del Tiempo: Inferencia LLM vs. Ejecución de Herramientas](#7-distribución-empírica-del-tiempo-inferencia-llm-vs-ejecución-de-herramientas)
  - [8. Métricas Deterministas de Latencia por Etapa](#8-métricas-deterministas-de-latencia-por-etapa)
  - [9. Taxonomía Consolidada de Errores y Retrabajo](#9-taxonomía-consolidada-de-errores-y-retrabajo)

---

# PARTE I: TELEMETRÍA ESTÁTICA Y LINTERS DE CALIDAD (`StandardizedAuditEngine`)

## 1. Resumen Consolidado de Linters Deterministas

| Métrica Determinista | Valor Medido | Detalle Técnico |
| :--- | :--- | :--- |
| **Total de Competencias** | **63** | Distribución: Fact: 17, Concept: 20, Skill: 26 |
| **Banco Total de Reactivos** | **1520 preguntas** | Rango por comp.: 20..30 |
| **Competencias Subpobladas (< 3 preg.)** | **0** | Nodos raíz sin prerrequisitos: 13 |
| **Preguntas Huérfanas** | **0** | Reactivos sin `competency_id` válido |
| **Cobertura de Rationales de Error** | **100.0%** | 9120 / 9120 distractores con `error_rationale` |
| **Distractores Delatores (Telltale)** | **0 items** | Confesiones de error en texto visible |
| **Andamiaje Socrático (Hints)** | **0 sin pistas** | 0 reactivos con `< 3` pistas; 0 sin solución |
| **Incidencias de Sintaxis KaTeX** | **0 incidencias** | Llaves sin cerrar: 0, `$` impares: 0, `$$$`: 0 |
| **Residuos de Código / F-strings** | **0 incidencias** | F-strings: 0, Vars plantilla: 0, `{{}}`: 0 |
| **Sustituciones Ciegas bajo Operador** | **0 incidencias** | Patrón `\dot{num}` / `\ddot{num}` |
| **Penalizaciones Duras Precalculadas** | **-0.0 puntos** | 0 reglas de deducción activadas |
| **Risk Score Global (0.0 - 100.0)** | **22.2** | 675 issues totales detectados por linters |

---

## 2. Resultados por Linter y Dimensión

| Dimensión de la Rúbrica | Puntaje Obtenido | Máximo Posible | Observación Registrada |
| :--- | :---: | :---: | :--- |
| **Dimensión 1: Arquitectura y Granularidad** | **3.8** | 4.0 | Excelente arquitectura curricular con 63 micro-competencias atómicas perfectamente delimitadas y balance cognitivo homogéneo entre Hechos (17, 27%), Conceptos (20, 32%) y Habilidades (26, 41%). El modelado de prerrequisitos en grafo acíclico dirigido (DAG) estructura rutas de aprendizaje progresivas desde principios teóricos elementales hasta linealización avanzada de Lotka-Volterra e IS-LM. Deducción menor (-0.2 pts) por 13 hechos basales con dependencias vacías que podrían beneficiarse de encadenamiento secuencial explícito. |
| **Dimensión 2: Calidad de Evaluación y Reactivos** | **4.5** | 5.0 | Excepcional cobertura diagnóstica con 100% de rationales pedagógicos en los 9,120 distractores evaluados (6 distractores por ítem en formato MC7). Ausencia absoluta de fugas de respuesta (Answer Leaks), distractores delatores o clonaciones espurias. Los distractores modelan errores conceptuales auténticos de la literatura matemática (inversión de derivadas, confusión de signos, omisión de términos autónomos). Deducción menor (-0.5 pts) debido a la concentración exclusiva en opción múltiple de 7 alternativas (MC7), sin inclusión complementaria de ítems de selección múltiple (MS) o fill-in-the-blank (FIB). |
| **Dimensión 3: Andamiaje y Feedback Progresivo** | **4.0** | 5.0 | El 98.3% del banco (1,494 reactivos) cuenta con andamiaje socrático de 3 niveles en prosa fluida (Conceptual -> Procedimental -> Consistencia dimensional). Sin embargo, se identificó un cluster aislado de 26 reactivos (1.7%) en las competencias Hab-05, C-04, H-04 y Hab-18 con pistas deficientes tipo stub keywords o etiquetas snake_case (e.g. ['Microeconomia', 'Hotelling', 'Dualidad'] o ['Sistemas_lineales', 'Autovalores_reales', 'Trayectorias']). Se aplica la deducción estipulada en la rúbrica de -1.0 pt por pistas deficientes aisladas. |
| **Dimensión 4: Alineación Instruccional** | **4.0** | 4.0 | Alineación instruccional impecable (4.0/4.0). Congruencia semántica absoluta entre el título, descripción formal de cada competencia y el conjunto de 20 a 30 reactivos asociados. Cero preguntas huérfanas, sin contaminación cruzada inter-dominio y con riguroso énfasis en niveles taxonómicos superiores de Bloom (Aplicación y Análisis cualitativo). |
| **Dimensión 5: Accesibilidad y Ergonomía Técnica / KaTeX** | **1.7** | 2.0 | Sintaxis KaTeX limpia y compilable al 100%: cero delimitadores desbalanceados, cero triples delimitadores y notación matemática formal preservada. El análisis semántico confirma que las advertencias del linter sobre '{pmatrix}', '{bmatrix}' y '{p}' corresponden a macros y entornos estándar válidos de LaTeX (falsos positivos del detector determinista). Se aplica una deducción menor (-0.3 pts) por colisiones tipográficas de dobles signos menos ('--56', '--126', '--25') detectadas en las soluciones de 16 reactivos de la competencia Hab-21. |
| **Total Consolidado** | **18.0** | **20.0** | **EXCELENTE (17.0 - 20.0 pts)** |

---

## 3. Clusters de Riesgo e Incidencias Detectadas

| Cluster de Riesgo | Ítems Afectados | Muestra de IDs |
| :--- | :---: | :--- |
| **`katex_issues`** | **506** | `Q-H05-391`, `Q-H05-392`, `Q-H05-393`, `Q-H05-394`, `Q-H05-395`, `Q-H05-396`, `Q-H05-397`, `Q-H05-398` |
| **`telltale_distractors`** | **0** | — |
| **`fstring_residues`** | **0** | — |
| **`scaffolding_flaws`** | **26** | `Q-Hab05-221`, `Q-Hab05-222`, `Q-Hab05-223`, `Q-Hab05-224`, `Q-Hab05-225`, `Q-Hab05-226`, `Q-Hab05-227`, `Q-Hab05-228` |
| **`template_residues`** | **0** | — |
| **`blind_replacements`** | **0** | — |
| **`cloned_distractors`** | **0** | — |
| **`archetype_monotony`** | **0** | — |

---

## 4. Muestra de Control Estratificada

Ítems extraídos determinísticamente por competencia (`prepare_course_payload.py`):

1. **`Q-C01-001` (Sistema de Ecuaciones Auxiliares de Lagrange para EDPs Cuasilineales de Primer Orden | `multiple_choice_7_options` | `hints=3`):** `Verifique la consistencia del modelo y obtenga: Dada la ecuación en derivadas parciales cuasilineal $2 x U_x - 2 y U_y =...`
2. **`Q-C01-002` (Sistema de Ecuaciones Auxiliares de Lagrange para EDPs Cuasilineales de Primer Orden | `multiple_choice_7_options` | `hints=3`):** `Procediendo conforme al marco teórico correspondiente, deduzca: Dada la ecuación en derivadas parciales cuasilineal $5 x...`
3. **`Q-Hab01-021` (Resolución de EDPs Cuasilineales mediante Integrales Primeras y el Método de Lagrange | `multiple_choice_7_options` | `hints=3`):** `Aplicando las identidades teóricas pertinentes, evalúe: Para la EDP cuasilineal $(y+U)U_x + (x+U)U_y = x+y$, con valores...`
4. **`Q-Hab01-022` (Resolución de EDPs Cuasilineales mediante Integrales Primeras y el Método de Lagrange | `multiple_choice_7_options` | `hints=3`):** `Al examinar detenidamente las condiciones de frontera, resuelva: Para la EDP cuasilineal $(y+U)U_x + (x+U)U_y = x+y$, co...`
5. **`Q-Hab02-051` (Resolución del Problema de Cauchy para EDPs Cuasilineales mediante Curvas Características | `multiple_choice_7_options` | `hints=3`):** `Considere el siguiente planteamiento formal: Considere el problema de Cauchy cuasilineal $x \frac{\partial U}{\partial x...`
6. **`Q-Hab02-052` (Resolución del Problema de Cauchy para EDPs Cuasilineales mediante Curvas Características | `multiple_choice_7_options` | `hints=3`):** `A partir de las condiciones analíticas dadas, determine: Considere el problema de Cauchy cuasilineal $x \frac{\partial U...`
7. **`Q-H01-081` (Teorema de Euler y Grado de Homogeneidad en Funciones de Producción | `multiple_choice_7_options` | `hints=3`):** `Analice la formulación operativa y deduzca: Para la función de producción $F(K, L) = 2 K^{3} L^{6}$, determine el grado ...`
8. **`Q-H01-082` (Teorema de Euler y Grado de Homogeneidad en Funciones de Producción | `multiple_choice_7_options` | `hints=3`):** `Verifique la consistencia del modelo y obtenga: Para la función de producción $F(K, L) = 6 K^{6} L^{2}$, determine el gr...`
9. **`Q-Hab03-101` (Modelado de Funciones de Utilidad y Cálculo de la Relación Marginal de Sustitución vía EDPs | `multiple_choice_7_options` | `hints=3`):** `Desde la perspectiva analítica correspondiente, compute: Considere las preferencias gobernadas por $\gamma U_\gamma + 2 ...`
10. **`Q-Hab03-102` (Modelado de Funciones de Utilidad y Cálculo de la Relación Marginal de Sustitución vía EDPs | `multiple_choice_7_options` | `hints=3`):** `Atendiendo a la relación funcional planteada, halle: Considere las preferencias gobernadas por $\gamma U_\gamma + 2 U_\t...`

---

## 5. Reglas de Linting Registradas (`discovered_lint_rules`)

* **ID de Regla:** `exclude_latex_matrix_environments_from_template_linter`
* **Severidad:** info
* **Patrón Regex:** `N/A`
* **Descripción:** 
* **ID de Regla:** `exclude_latex_accents_from_template_linter`
* **Severidad:** info
* **Patrón Regex:** `N/A`
* **Descripción:** 
* **ID de Regla:** `auto_simplify_algebraic_double_negatives`
* **Severidad:** info
* **Patrón Regex:** `N/A`
* **Descripción:** 
---

# PARTE II: AUDITORÍA FORENSE DE RENDIMIENTO Y TELEMETRÍA (RUN AUDITOR)

## 6. Consolidación de Métricas de Rendimiento y Ratios Unitarios

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada (`pre_cta_manifest.json`)** | `7 archivos` (103 págs / 10.39 MB) | Ingesta directa PDF Zero-Waste (v3.2) |
| **Competencias Extraídas (`cta.json`)** | **`63 competencias`** | Compiladas desde tuplas posicionales (`compile_cta.py`) |
| **Shards Particionados (`pre_shard_manifest.json`)** | **`45 shards`** | Compilados vía `compile_shard.py` |
| **Subagentes Desplegados ($M$ CTA, $N$ Shards, $K$ Judges)** | **`63 subagentes`** | Fan-out dinámico coordinado por orquestador |
| **Reactivos Finales Validados** | **`1520 preguntas`** | Evaluadas en sandbox in-process |
| **Tokens Entrada (Subagentes)** | **`6,796,153 tokens`** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`2,343,496 tokens`** | Código de tuplas Python y JSON generado |
| **Tokens Caché (Leídos)** | **`34,570,011 tokens`** | Caché de contexto reutilizado por la API |
| **Trazas de Pensamiento (`thinking_traces`)** | **`443 turnos` (1,656,578 chars)** | Razonamiento interno extraído de `transcript.jsonl` / `transcript_full.jsonl` |
| **Gran Total Tokens Activos** | **`9,139,649 tokens`** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`43,709,660 tokens`** | Consumo total de cuota facturable |
| **Tiempo de Pared Total** | **`1569.0 s` (26.15 min)** | Tiempo transcurrido de principio a fin |
| **Tiempo Cómputo Acumulado** | **`20033.0 s` (333.88 min)** | Suma escalar de tiempos de todos los agentes |
| **Factor de Aceleración Paralela** | **`12.77x`** | Relación tiempo cómputo vs tiempo de pared |
| **Tokens Totales por Pregunta** | **`28,756.4 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`6,012.9 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`693,804.1 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`106,629.5 tokens/comp`** | Costo puro de la etapa de autoría |
| **Segundos de Pared por Pregunta** | **`1.03 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`58.13 preg/min`** | Velocidad de producción del pipeline |

---

## 7. Distribución Empírica del Tiempo: Inferencia LLM vs. Ejecución de Herramientas

- **Porcentaje Promedio en Inferencia LLM:** `95.8%`
- **Porcentaje Promedio en Ejecución Local de Herramientas:** `4.2%`

```
========================================================================================
DISTRIBUCIÓN DEL TIEMPO DE PARED POR SUBAGENTE (INFERENCIA LLM vs TOOLS)
========================================================================================
Direct CTA Architect   : [░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 0s (0.0%) LLM | 0s Tools
Author Shard 01        : [████████████████████████████████████░░░░] 265s (91.7%) LLM | 18s Tools
Author Shard 02        : [████████████████████████████████████░░░░] 305s (90.8%) LLM | 19s Tools
Author Shard 03        : [██████████████████████████████████████░░] 221s (96.1%) LLM | 9s Tools
Author Shard 04        : [███████████████████████████████████████░] 278s (98.9%) LLM | 3s Tools
Author Shard 05        : [████████████████████████████████████░░░░] 230s (90.6%) LLM | 18s Tools
Author Shard 06        : [█████████████████████████████████████░░░] 275s (93.5%) LLM | 17s Tools
Author Shard 07        : [██████████████████████████████████████░░] 227s (95.0%) LLM | 12s Tools
Author Shard 08        : [█████████████████████████████████████░░░] 331s (93.5%) LLM | 18s Tools
Author Shard 09        : [██████████████████████████████████████░░] 346s (95.1%) LLM | 16s Tools
Author Shard 10        : [██████████████████████████████████████░░] 256s (97.0%) LLM | 7s Tools
Author Shard 11        : [████████████████████████████████████░░░░] 411s (91.3%) LLM | 27s Tools
Author Shard 12        : [████████████████████████████████████░░░░] 272s (90.7%) LLM | 18s Tools
Author Shard 13        : [████████████████████████████████████░░░░] 278s (92.4%) LLM | 21s Tools
Author Shard 14        : [██████████████████████████████████████░░] 610s (97.1%) LLM | 13s Tools
Author Shard 15        : [██████████████████████████████████░░░░░░] 415s (86.5%) LLM | 41s Tools
Author Shard 16        : [██████████████████████████████████████░░] 326s (96.4%) LLM | 12s Tools
Author Shard 17        : [███████████████████████████████████░░░░░] 263s (88.6%) LLM | 23s Tools
Author Shard 18        : [████████████████████████████████████░░░░] 311s (91.5%) LLM | 18s Tools
Author Shard 19        : [██████████████████████████████████████░░] 225s (97.4%) LLM | 6s Tools
Author Shard 20        : [████████████████████████████████████░░░░] 304s (90.2%) LLM | 21s Tools
Author Shard 21        : [██████████████████████████████████████░░] 332s (95.4%) LLM | 10s Tools
Author Shard 22        : [██████████████████████████████████████░░] 355s (95.7%) LLM | 11s Tools
Author Shard 23        : [████████████████████████████████████░░░░] 366s (92.2%) LLM | 24s Tools
Author Shard 24        : [█████████████████████████████████████░░░] 449s (93.9%) LLM | 23s Tools
Author Shard 25        : [██████████████████████████████████████░░] 297s (96.4%) LLM | 11s Tools
Author Shard 26        : [████████████████████████████████████░░░░] 271s (91.6%) LLM | 23s Tools
Author Shard 27        : [██████████████████████████████████████░░] 299s (95.2%) LLM | 15s Tools
Author Shard 28        : [██████████████████████████████████████░░] 273s (95.8%) LLM | 12s Tools
Author Shard 29        : [███████████████████████████████████████░] 314s (97.5%) LLM | 8s Tools
Author Shard 30        : [█████████████████████████████████████░░░] 338s (93.9%) LLM | 16s Tools
Author Shard 31        : [██████████████████████████████████████░░] 370s (95.9%) LLM | 15s Tools
Author Shard 32        : [████████████████████████████████░░░░░░░░] 271s (81.4%) LLM | 34s Tools
Author Shard 33        : [████████████████████████████████████░░░░] 355s (91.0%) LLM | 21s Tools
Author Shard 34        : [█████████████████████████████████████░░░] 359s (94.2%) LLM | 17s Tools
Author Shard 35        : [██████████████████████████████████████░░] 265s (96.4%) LLM | 9s Tools
Author Shard 36        : [██████████████████████████████████████░░] 296s (96.7%) LLM | 10s Tools
Author Shard 37        : [████████████████████████████████████░░░░] 326s (92.4%) LLM | 25s Tools
Author Shard 38        : [█████████████████████████████████████░░░] 318s (94.4%) LLM | 19s Tools
Author Shard 39        : [█████████████████████████████████████░░░] 328s (93.7%) LLM | 16s Tools
Author Shard 40        : [█████████████████████████████████████░░░] 331s (92.5%) LLM | 22s Tools
Author Shard 41        : [██████████████████████████████████████░░] 426s (96.4%) LLM | 16s Tools
Author Shard 42        : [██████████████████████████████████████░░] 275s (95.2%) LLM | 14s Tools
Author Shard 43        : [██████████████████████████████████████░░] 332s (96.0%) LLM | 13s Tools
Author Shard 44        : [█████████████████████████████████████░░░] 355s (94.4%) LLM | 15s Tools
Author Shard 45        : [█████████████████████████████████████░░░] 234s (93.2%) LLM | 16s Tools
Judge 01               : [███████████████████████████████████████░] 66s (98.5%) LLM | 1s Tools
Judge 02               : [████████████████████████████████████████] 131s (100.0%) LLM | 0s Tools
Judge 03               : [████████████████████████████████████████] 92s (100.0%) LLM | 0s Tools
Judge 04               : [████████████████████████████████████████] 94s (100.0%) LLM | 0s Tools
Judge 05               : [████████████████████████████████████████] 152s (100.0%) LLM | 0s Tools
Judge 06               : [███████████████████████████████████████░] 66s (98.5%) LLM | 1s Tools
Judge 07               : [███████████████████████████████████████░] 134s (99.3%) LLM | 1s Tools
Judge 08               : [████████████████████████████████████████] 67s (100.0%) LLM | 0s Tools
Judge 09               : [████████████████████████████████████████] 55s (100.0%) LLM | 0s Tools
Judge 10               : [████████████████████████████████████████] 67s (100.0%) LLM | 0s Tools
Judge 11               : [█████████████████████████████████████░░░] 77s (93.9%) LLM | 5s Tools
========================================================================================
```

---

## 8. Métricas Deterministas de Latencia por Etapa

| Etapa del Pipeline | Agentes / Shards | Tiempo de Pared (s) | Detalle Determinista |
| :--- | :---: | :---: | :--- |
| **Stage 1B: CTA Architects** | `7` | `407.0s` | Mappers max: `407.0s`, Harmonizer: `0.0s` |
| **Stage 3: Shard Authors** | `45` | `628.0s` | Min: `230.0s`, Mediana: `337.0s`, Straggler: `Shard Author shard_14` (`+291.0s`) |
| **Stage 5: Blind Judges** | `11` | `152.0s` | Lote: `126` ítems, 1er intento: `True`, Auto-repair: `2` |
| **Orquestador Principal** | `1` | `1569.0s` | CLI: `70.0s`, Barrera: `48.0s`, Intervenciones: `0` (`0.0s`) |

---

## 9. Taxonomía Consolidada de Errores y Retrabajo

| Categoría de Error | Ocurrencias | Agentes Afectados | Causa Raíz Técnica y Ejemplo |
| :--- | :---: | :--- | :--- |
| **Missing File / Relative Path / Directory Error (FileNotFoundError)** | **138** | Author Shard 01, Author Shard 02, Author Shard 03 | Encountered error in step execution: declaring permissions: cortex tool view_file: convert |
| **Token Limit Cutoff (Model Truncation)** | **114** | Author Shard 01, Author Shard 02, Author Shard 03 | — |
| **Anti-Giveaway & Psychometric Parity Violations (R-14..R-19)** | **21** | Author Shard 03, Author Shard 06, Author Shard 09 | Encountered error in step execution: tool call denied by pre-tool hook: C2C Cross-Course I |
| **PowerShell Command / Quoting / $Variable Expansion Friction** | **7** | Author Shard 23, Author Shard 24, Author Shard 31 | The command exited with code 1. / Output: / Select-String : La cadena " shard_31\ no es un |
| **Parameter Diversity & Option Collapse (TPL-VAR / TPL-COLLAPSE)** | **4** | Author Shard 11, Author Shard 13, Author Shard 14 | The command exited with code 1. / Output: / [-] FAIL: 3 errores detectados (3 errores cons |
| **CTA Compilation & Schema Errors (CTA-SCHEMA / CTA-EV / DAG Cycle)** | **3** | CTA Architect (part_01), CTA Architect (part_03), CTA Architect (part_05) | Encountered error in step execution: tool call denied by pre-tool hook: C2C Worker Boundar |
| **File Edit / Write Tool Target Mismatch (replace_file_content / Overwrite)** | **2** | Author Shard 11, CTA Architect (part_03) | Encountered error in step execution: target content not found in the file; the Target must |
| **Non-Zero CLI Exit / Subprocess Probe (Exit Code 1)** | **2** | Author Shard 17, CTA Architect (part_01) | Encountered error in step execution: declaring permissions: failed to parse path: courses/ |
| **Stage Contract / Pipeline Loader Mismatch (run.py / judge.py)** | **1** | Orchestrator | Command exited with code 1. / Command output: / ========================================== |
| **Shard Compilation & Template Validator Failure (compile_shard / check_templates)** | **1** | Author Shard 34 | The command exited with code 1. / Output: / [-] FAIL: 2 errores detectados (2 errores cons |
| **Cross-check Verification False (TPL-CROSS)** | **1** | Author Shard 40 | The command exited with code 1. / Output: / [-] [TPL-DRY: FALLO EN EJECUCI�N DRY-RUN] / Co |
