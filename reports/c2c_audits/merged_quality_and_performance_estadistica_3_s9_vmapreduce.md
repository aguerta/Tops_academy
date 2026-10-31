# Reporte Unificado de Auditoría Determinista: Calidad Estática y Telemetría Multi-Agente
## Curso: Estadística III — Semana 9: Propiedades en Muestras Finitas y Teoría Asintótica (vMapReduce) (`estadistica_3_s9_vmapreduce`)
### Plataforma Top's Academy — Pipeline Content-to-Course (C2C) v3.2

---

**Fecha de Consolidación:** 31 de Octubre de 2026  
**Identificador del Curso:** `estadistica_3_s9_vmapreduce`  
**Conversación Orquestadora Auditada:** [`068a3181-c378-4025-96b3-6f68ba04dfc5`](conversation://068a3181-c378-4025-96b3-6f68ba04dfc5)  
**Calificación QM-OSCQR / Risk Score:** **5.5 / 20.0 (RECHAZADO (Crítico))**  
**Mastery Path Readiness Index (`MPRI`):** **`39.45 / 100.0` (MASTERY-HOSTILE (0-39): Sabotaje Cognitivo / Colapso de Andamiaje Adaptativo)**  
**Tiempo de Pared Global:** **22.3 minutos** | **Cómputo Total de Agentes:** **162.37 minutos** | **Speedup:** **7.28x**  

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
  - [10. Paquete Forense Agéntico Completo (Argon QA + Clúster Flash)](#10-paquete-forense-agéntico-completo-argon-qa--clúster-flash)

---

# PARTE I: TELEMETRÍA ESTÁTICA Y LINTERS DE CALIDAD (`StandardizedAuditEngine`)

## 1. Resumen Consolidado de Linters Deterministas

| Métrica Determinista | Valor Medido | Detalle Técnico |
| :--- | :--- | :--- |
| **Total de Competencias** | **39** | Distribución: Fact: 5, Concept: 20, Skill: 14 |
| **Banco Total de Reactivos** | **920 preguntas** | Rango por comp.: 20..30 |
| **Competencias Subpobladas (< 3 preg.)** | **0** | Nodos raíz sin prerrequisitos: 4 |
| **Preguntas Huérfanas** | **0** | Reactivos sin `competency_id` válido |
| **Cobertura de Rationales de Error** | **100.0%** | 5520 / 5520 distractores con `error_rationale` |
| **Distractores Delatores (Telltale)** | **0 items** | Confesiones de error en texto visible |
| **Andamiaje Socrático (Hints)** | **0 sin pistas** | 0 reactivos con `< 3` pistas; 0 sin solución |
| **Incidencias de Sintaxis KaTeX** | **0 incidencias** | Llaves sin cerrar: 0, `$` impares: 0, `$$$`: 0 |
| **Residuos de Código / F-strings** | **0 incidencias** | F-strings: 0, Vars plantilla: 0, `{{}}`: 0 |
| **Sustituciones Ciegas bajo Operador** | **0 incidencias** | Patrón `\dot{num}` / `\ddot{num}` |
| **Penalizaciones Duras Precalculadas** | **-2.0 puntos** | 2 reglas de deducción activadas |
| **Risk Score Global (0.0 - 100.0)** | **100.0** | 2053 issues totales detectados por linters |
| **Mastery Path Readiness (`MPRI`)** | **`39.45 / 100.0`** | MASTERY-HOSTILE (0-39): Sabotaje Cognitivo / Colapso de Andamiaje Adaptativo |

---

## 1B. Auditoría de Camino al Dominio (`Path-to-Mastery v2.0` — 6 Pilares Cognitivos)

| Pilar de Dominio del Estudiante | Puntaje MPRI | Máximo | Diagnóstico Empírico Determinista |
| :--- | :---: | :---: | :--- |
| **1. Progresión Adaptativa ZPD y Bloom** | **0.0** | 20.0 | Competencias con ZPD colapsado (1 sola banda): `39/39`; Habilidades en Bloom `Apply+`: `0.0%` |
| **2. Modalidad de Evocación y Anti-Gaming** | **0.0** | 20.0 | `MC7=100.0%`, `FIB=0.0%`, `MS=0.0%`; Comps memorizables: `2`; Cuantif. vacuos: `20`; Relleno `[R-15]`: `55` |
| **3. Integridad del Salvavidas Socrático (3-Strikes)** | **13.65** | 25.0 | Pistas genuinas: `8.15%`; Boilerplate Mad-Libs: `91.85%`; Pistas envenenadas: `20` (`2.17%`) |
| **4. Alineación Diagnóstica en `FeedbackToast`** | **10.89** | 15.0 | Unicidad global de `error_rationale`: `7.93%` (`438/5520`); Distractores `1.333x` arbitrarios: `9` |
| **5. Topología DAG e Interleaving (Quiz/Test)** | **8.5** | 10.0 | Ciclos: `False`, Profundidad DAG: `8`, Aristas invertidas: `0`, Islas: `1` |
| **6. Ergonomía Cognitiva y Pureza de Encuadre** | **6.41** | 10.0 | Prosa en `\text{...}`: `160`, Vars crudas `$theta_hat$`: `0`, Prefijos Solow/EDP ajenos: `92` |

---

## 2. Resultados por Linter y Dimensión

| Dimensión de la Rúbrica | Puntaje Obtenido | Máximo Posible | Observación Registrada |
| :--- | :---: | :---: | :--- |
| **Dimensión 1: Arquitectura y Granularidad** | **2.0** | 4.0 | Tope normativo aplicado por colapso 100% 'medium' en 39/39 competencias (calibrateByMasteryDifficulty inoperante), nodo isla C-01 (in=0, out=0) y fractura MapReduce no fusionada en 3 subgrafos disjuntos (1 + 14 + 24 nodos) con 9 competencias duplicadas y reinicio de Unidad 25 a Unidad 3. |
| **Dimensión 2: Calidad de Evaluación y Reactivos** | **1.5** | 5.0 | Rango Crítico (<=2.4) activado por corrupción matemática de cuantificador universal y falacia existencial->universal en C-02 (Q-C02-131..150) y C-10 (Q-C10-561..565), exploit de memorización en C-05 (1 clave única en 20 ítems) y H-01 (4 claves únicas), monocultivo 100% MC7 (0% FIB/MS), distractores por multiplicador arbitrario (9 ítems) y firma delatora de cláusula simple vs doble para evadir [R-15] en Q-H05-670..680. |
| **Dimensión 3: Andamiaje y Feedback Progresivo** | **1.1** | 5.0 | Tope estricto (0.8 - 1.5) activado por 89.67% de boilerplate Mad-Libs, stubs de etiquetas crudas ['C20', 'Teorema-slutsky', 'Asintotica'] en Q-C20-871..875, envenenamiento anti-socrático en Pista 2 ('asegurando considerar adecuadamente: [fórmula falsa CTA]') y desconexión/eco de fórmulas falsas crudas en FeedbackToast.tsx. Se reconoce el 7.61% (70 ítems en Hab-08, C-12, C-13) con pistas socráticas legítimas. |
| **Dimensión 4: Alineación Instruccional** | **1.5** | 4.0 | Cobertura temática rigurosa del sílabo de Semana 9, pero degradada por 100% Bloom 'Understand' (0% Apply/Analyze en 420 ítems [Hab]), 92 reactivos con prefijos robóticos contaminados de Solow/EDP ('condiciones de frontera', 'fundamentos del equilibrio') y discordancia matemática irreparada en Stage 5 (T-C-02-02_judge_1) que enseña una implicación lógica falsa. |
| **Dimensión 5: Accesibilidad y Ergonomía Técnica / KaTeX** | **1.4** | 2.0 | Cero errores de compilación KaTeX, llaves, signos '$' o variables crudas (las 174 alertas en \bar{Y}_n son falsos positivos del linter). Deducción de -0.6 pts por 160 ítems (250 instancias) con oraciones completas de prosa envueltas en $\text{...}$ que impiden el salto de línea (white-space: nowrap) en tarjetas móviles. |
| **Total Consolidado** | **5.5** | **20.0** | **RECHAZADO (Crítico)** |

---

## 3. Clusters de Riesgo e Incidencias Detectadas

| Cluster de Riesgo | Ítems Afectados | Muestra de IDs |
| :--- | :---: | :--- |
| **`katex_issues`** | **279** | `Q-Hab02-071`, `Q-Hab02-072`, `Q-Hab02-073`, `Q-Hab02-074`, `Q-Hab02-075`, `Q-Hab02-076`, `Q-Hab02-077`, `Q-Hab02-078` |
| **`telltale_distractors`** | **0** | — |
| **`fstring_residues`** | **0** | — |
| **`scaffolding_flaws`** | **850** | `Q-C20-871`, `Q-C20-872`, `Q-C20-873`, `Q-C20-874`, `Q-C20-875`, `Q-C01-001`, `Q-C01-002`, `Q-C01-003` |
| **`template_residues`** | **0** | — |
| **`blind_replacements`** | **0** | — |
| **`cloned_distractors`** | **0** | — |
| **`archetype_monotony`** | **0** | — |
| **`poisoned_hints`** | **20** | `Q-H01-021`, `Q-H01-022`, `Q-H01-023`, `Q-H01-024`, `Q-H01-025`, `Q-H01-026`, `Q-H01-027`, `Q-H01-028` |
| **`boilerplate_hints`** | **825** | `Q-C01-001`, `Q-C01-002`, `Q-C01-003`, `Q-C01-004`, `Q-C01-005`, `Q-C01-006`, `Q-C01-007`, `Q-C01-008` |
| **`magic_multiplier_distractors`** | **10** | `Q-Hab08-299`, `Q-Hab08-300`, `Q-Hab08-303`, `Q-Hab08-304`, `Q-Hab08-306`, `Q-H03-513`, `Q-H05-677`, `Q-H05-678` |
| **`memorizable_answers`** | **2** | `Q-H01-021`, `Q-C05-341` |
| **`length_padded_options`** | **55** | `Q-Hab07-283`, `Q-Hab08-292`, `Q-Hab08-303`, `Q-Hab08-318`, `Q-Hab09-380`, `Q-Hab09-388`, `Q-H02-396`, `Q-H02-404` |
| **`cross_domain_prefixes`** | **92** | `Q-C01-005`, `Q-C01-012`, `Q-H01-031`, `Q-H01-033`, `Q-Hab01-042`, `Q-Hab01-064`, `Q-Hab01-067`, `Q-Hab01-069` |
| **`vacuous_quantifiers`** | **20** | `Q-C02-131`, `Q-C02-132`, `Q-C02-133`, `Q-C02-134`, `Q-C02-135`, `Q-C02-136`, `Q-C02-137`, `Q-C02-138` |
| **`katex_ergonomics`** | **160** | `Q-C01-001`, `Q-C01-002`, `Q-C01-003`, `Q-C01-004`, `Q-C01-005`, `Q-C01-006`, `Q-C01-007`, `Q-C01-008` |

---

## 4. Muestra de Control Estratificada

Ítems extraídos determinísticamente por competencia (`prepare_course_payload.py`):

1. **`Q-C01-001` (Fragilidad de la Normalidad Exacta y Criterio del Tamaño Muestral Eficaz | `multiple_choice_7_options` | `hints=3`):** `Verifique la consistencia del modelo y obtenga: En un modelo econométrico con asimetría poblacional $\gamma_1 = 1.6$ y c...`
2. **`Q-C01-002` (Fragilidad de la Normalidad Exacta y Criterio del Tamaño Muestral Eficaz | `multiple_choice_7_options` | `hints=3`):** `Procediendo conforme al marco teórico correspondiente, deduzca: En un modelo econométrico con asimetría poblacional $\ga...`
3. **`Q-H01-021` (Definición de Sesgo y Eficiencia Relativa en Muestras Finitas | `multiple_choice_7_options` | `hints=3`):** `Analice la formulación operativa y deduzca: Para un estimador puntual $\hat{\theta}_n$ de un parámetro poblacional $\the...`
4. **`Q-H01-022` (Definición de Sesgo y Eficiencia Relativa en Muestras Finitas | `multiple_choice_7_options` | `hints=3`):** `Verifique la consistencia del modelo y obtenga: Para un estimador puntual $\hat{\theta}_n$ de un parámetro poblacional $...`
5. **`Q-Hab01-041` (Demostración de la Descomposición del Error Cuadrático Medio | `multiple_choice_7_options` | `hints=3`):** `Aplicando las identidades teóricas pertinentes, evalúe: Sea $\hat{\theta}_n$ un estimador puntual del parámetro $\theta$...`
6. **`Q-Hab01-042` (Demostración de la Descomposición del Error Cuadrático Medio | `multiple_choice_7_options` | `hints=3`):** `Al examinar detenidamente las condiciones de frontera, resuelva: Sea $\hat{\theta}_n$ un estimador puntual del parámetro...`
7. **`Q-Hab02-071` (Deducción de los Momentos Exactos de la Media Muestral | `multiple_choice_7_options` | `hints=3`):** `Considere el siguiente planteamiento formal: Considere una muestra aleatoria simple $Y_1, \dots, Y_{60}$ de variables al...`
8. **`Q-Hab02-072` (Deducción de los Momentos Exactos de la Media Muestral | `multiple_choice_7_options` | `hints=3`):** `A partir de las condiciones analíticas dadas, determine: Considere una muestra aleatoria simple $Y_1, \dots, Y_{46}$ de ...`
9. **`Q-Hab03-101` (Demostración del Sesgo de la Varianza Muestral y Corrección por Grados de Libertad | `multiple_choice_7_options` | `hints=3`):** `Desde la perspectiva analítica correspondiente, compute: Considere una muestra aleatoria simple de tamaño $n = 27$ prove...`
10. **`Q-Hab03-102` (Demostración del Sesgo de la Varianza Muestral y Corrección por Grados de Libertad | `multiple_choice_7_options` | `hints=3`):** `Atendiendo a la relación funcional planteada, halle: Considere una muestra aleatoria simple de tamaño $n = 17$ provenien...`

---

## 5. Reglas de Linting Registradas (`discovered_lint_rules`)

* **ID de Regla:** `dag_disconnected_subgraphs_linter`
* **Severidad:** critical
* **Patrón Regex:** `GRAPH_TOPOLOGY: weakly_connected_components(competencies_dag) > 1`
* **Descripción:** Detecta cuando el grafo curricular completo se fractura en múltiples componentes conexas disjuntas (incluso si cada subgrafo tiene nodos con aristas y evade isolated_competencies). Captura concatenaciones MapReduce sin etapa Reduce de fusión semántica.
* **Ítems Evidencia:** C-01, H-01, H-02, C-06, C-20

* **ID de Regla:** `bound_constant_in_universal_quantifier_linter`
* **Severidad:** critical
* **Patrón Regex:** `(?:para\s+todo|todo\s+margen|\\forall)\s+\$?\\eps(?:ilon)?\s*=\s*\d+(?:\.\d+)?`
* **Descripción:** Detecta cuantificadores universales ligados directamente por igualdad a un flotante numérico fijo (ej. 'para todo \epsilon = 0.04 > 0'), corrompiendo la definición analítica de límite en probabilidad en enunciados y soluciones.
* **Ítems Evidencia:** Q-C10-561, Q-C10-562, Q-C10-563, Q-C10-564, Q-C10-565

* **ID de Regla:** `single_vs_double_filler_clause_r15_gaming_linter`
* **Severidad:** critical
* **Patrón Regex:** `(?:,\s*(?:bajo las hip[oó]tesis del modelo|seg[uú]n los supuestos cl[aá]sicos del modelo|para los par[aá]metros bajo an[aá]lisis|en el contexto del contraste analizado|en el marco de la especificaci[oó]n|de acuerdo con la teor[ií]a econom[eé]trica|para la muestra de datos observada|en la formulaci[oó]n matricial considerada)){2}`
* **Descripción:** Detecta la evasión perversa de [R-15] donde opt_a concatena 2 cláusulas de relleno para superar en longitud a la clave correcta, dejando a la respuesta correcta 100% delatada como la única opción con exactamente 1 cláusula de relleno frente a 5 distractores cortos.
* **Ítems Evidencia:** Q-H05-670, Q-H05-671, Q-H05-672, Q-H05-676, Q-H05-677, Q-H05-678, Q-H05-680

* **ID de Regla:** `latex_misconception_injected_in_madlibs_hint_linter`
* **Severidad:** critical
* **Patrón Regex:** `asegurando considerar adecuadamente:\s*\$[^$]+\$`
* **Descripción:** Extiende socratic_scaffolding_integrity_linter para capturar pistas Mad-Libs que inyectan una fórmula LaTeX falsa de la columna CTA Misconception tras 'asegurando considerar adecuadamente:', saboteando al alumno en Strike 1/2 aunque la cadena no coincida literalmente en texto plano con una opción.
* **Ítems Evidencia:** Q-C01-001, Q-C02-131, Q-C04-339, Q-C05-341, Q-H05-670

* **ID de Regla:** `unrefuted_latex_misconception_as_rationale_linter`
* **Severidad:** warning
* **Patrón Regex:** `^\$(?:\\text\{[^}]+\}|[^$])+\$$`
* **Descripción:** Detecta cuando error_rationale consiste únicamente en una ecuación o proposición falsa envuelta en '$...$' sin ningún verbo ni explicación refutativa en español, haciendo que FeedbackToast muestre una afirmación matemáticamente falsa como si fuera retroalimentación válida.
* **Ítems Evidencia:** Q-C02-131, Q-C02-132, Q-Hab03-130, Q-C05-341, Q-C05-342

---

# PARTE II: AUDITORÍA FORENSE DE RENDIMIENTO Y TELEMETRÍA (RUN AUDITOR)

## 6. Consolidación de Métricas de Rendimiento y Ratios Unitarios

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada (`pre_cta_manifest.json`)** | `2 archivos` (80 págs / 0.93 MB) | Ingesta directa PDF Zero-Waste (v3.2) |
| **Competencias Extraídas (`cta.json`)** | **`39 competencias`** | Compiladas desde tuplas posicionales (`compile_cta.py`) |
| **Shards Particionados (`pre_shard_manifest.json`)** | **`27 shards`** | Compilados vía `compile_shard.py` |
| **Subagentes Desplegados ($M$ CTA, $N$ Shards, $K$ Judges)** | **`36 subagentes`** | Fan-out dinámico coordinado por orquestador |
| **Reactivos Finales Validados** | **`920 preguntas`** | Evaluadas en sandbox in-process |
| **Tokens Entrada (Subagentes)** | **`3,286,902 tokens`** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`1,215,982 tokens`** | Código de tuplas Python y JSON generado |
| **Tokens Caché (Leídos)** | **`11,533,780 tokens`** | Caché de contexto reutilizado por la API |
| **Trazas de Pensamiento (`thinking_traces`)** | **`223 turnos` (881,400 chars)** | Razonamiento interno extraído de `transcript.jsonl` / `transcript_full.jsonl` |
| **Gran Total Tokens Activos** | **`4,502,884 tokens`** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`16,036,664 tokens`** | Consumo total de cuota facturable |
| **Tiempo de Pared Total** | **`1338.0 s` (22.3 min)** | Tiempo transcurrido de principio a fin |
| **Tiempo Cómputo Acumulado** | **`9742.0 s` (162.37 min)** | Suma escalar de tiempos de todos los agentes |
| **Factor de Aceleración Paralela** | **`7.28x`** | Relación tiempo cómputo vs tiempo de pared |
| **Tokens Totales por Pregunta** | **`17,431.2 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`4,894.4 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`411,196.5 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`89,531.4 tokens/comp`** | Costo puro de la etapa de autoría |
| **Segundos de Pared por Pregunta** | **`1.45 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`41.26 preg/min`** | Velocidad de producción del pipeline |

---

## 7. Distribución Empírica del Tiempo: Inferencia LLM vs. Ejecución de Herramientas

- **Porcentaje Promedio en Inferencia LLM:** `95.8%`
- **Porcentaje Promedio en Ejecución Local de Herramientas:** `4.2%`

```
========================================================================================
DISTRIBUCIÓN DEL TIEMPO DE PARED POR SUBAGENTE (INFERENCIA LLM vs TOOLS)
========================================================================================
Direct CTA Architect   : [░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 0s (0.0%) LLM | 0s Tools
Author Shard 01        : [███████████████████████████████████████░] 227s (98.7%) LLM | 3s Tools
Author Shard 02        : [███████████████████████████████████████░] 301s (98.7%) LLM | 4s Tools
Author Shard 03        : [███████████████████████████████████████░] 258s (98.1%) LLM | 5s Tools
Author Shard 04        : [███████████████████████████████████████░] 240s (99.2%) LLM | 2s Tools
Author Shard 05        : [███████████████████████████████████████░] 240s (98.8%) LLM | 3s Tools
Author Shard 06        : [███████████████████████████████████████░] 267s (98.5%) LLM | 4s Tools
Author Shard 07        : [███████████████████████████████████████░] 292s (98.6%) LLM | 4s Tools
Author Shard 08        : [██████████████████████████████████████░░] 240s (97.2%) LLM | 7s Tools
Author Shard 09        : [███████████████████████████████████████░] 258s (98.1%) LLM | 5s Tools
Author Shard 10        : [███████████████████████████████████████░] 204s (99.0%) LLM | 2s Tools
Author Shard 11        : [███████████████████████████████████████░] 208s (98.6%) LLM | 3s Tools
Author Shard 12        : [███████████████████████████████████████░] 295s (98.7%) LLM | 4s Tools
Author Shard 13        : [██████████████████████████████████████░░] 227s (97.4%) LLM | 6s Tools
Author Shard 14        : [███████████████████████████████████████░] 251s (98.4%) LLM | 4s Tools
Author Shard 15        : [███████████████████████████████████████░] 228s (98.3%) LLM | 4s Tools
Author Shard 16        : [███████████████████████████████████████░] 322s (98.2%) LLM | 6s Tools
Author Shard 17        : [███████████████████████████████████████░] 262s (98.5%) LLM | 4s Tools
Author Shard 18        : [██████████████████████████████████████░░] 326s (97.3%) LLM | 9s Tools
Author Shard 19        : [███████████████████████████████████████░] 192s (97.5%) LLM | 5s Tools
Author Shard 20        : [███████████████████████████████████████░] 318s (97.8%) LLM | 7s Tools
Author Shard 21        : [███████████████████████████████████████░] 237s (97.5%) LLM | 6s Tools
Author Shard 22        : [██████████████████████████████████████░░] 244s (95.3%) LLM | 12s Tools
Author Shard 23        : [███████████████████████████████████████░] 295s (98.7%) LLM | 4s Tools
Author Shard 24        : [███████████████████████████████████████░] 317s (97.8%) LLM | 7s Tools
Author Shard 25        : [███████████████████████████████████████░] 247s (98.0%) LLM | 5s Tools
Author Shard 26        : [███████████████████████████████████████░] 289s (98.3%) LLM | 5s Tools
Author Shard 27        : [███████████████████████████████████████░] 224s (98.7%) LLM | 3s Tools
Judge 01               : [████████████████████████████████████████] 58s (100.0%) LLM | 0s Tools
Judge 02               : [███████████████████████████████████████░] 56s (98.2%) LLM | 1s Tools
Judge 03               : [███████████████████████████████████████░] 56s (98.2%) LLM | 1s Tools
Judge 04               : [████████████████████████████████████████] 65s (100.0%) LLM | 0s Tools
Judge 05               : [████████████████████████████████████████] 72s (100.0%) LLM | 0s Tools
Judge 06               : [███████████████████████████████████████░] 53s (98.1%) LLM | 1s Tools
Judge 07               : [████████████████████████████████████████] 76s (100.0%) LLM | 0s Tools
========================================================================================
```

---

## 8. Métricas Deterministas de Latencia por Etapa

| Etapa del Pipeline | Agentes / Shards | Tiempo de Pared (s) | Detalle Determinista |
| :--- | :---: | :---: | :--- |
| **Stage 1B: CTA Architects** | `2` | `434.0s` | Mappers max: `434.0s`, Harmonizer: `0.0s` |
| **Stage 3: Shard Authors** | `27` | `335.0s` | Min: `197.0s`, Mediana: `256.0s`, Straggler: `Shard Author shard_18` (`+79.0s`) |
| **Stage 5: Blind Judges** | `7` | `76.0s` | Lote: `78` ítems, 1er intento: `True`, Auto-repair: `2` |
| **Orquestador Principal** | `1` | `1338.0s` | CLI: `77.0s`, Barrera: `44.0s`, Intervenciones: `0` (`0.0s`) |

---

## 9. Taxonomía Consolidada de Errores y Retrabajo

| Categoría de Error | Ocurrencias | Agentes Afectados | Causa Raíz Técnica y Ejemplo |
| :--- | :---: | :--- | :--- |
| **Missing File / Relative Path / Directory Error (FileNotFoundError)** | **64** | Author Shard 01, Author Shard 02, Author Shard 03 | Encountered error in step execution: declaring permissions: cortex tool view_file: convert |
| **Shard Compilation & Template Validator Failure (compile_shard / check_templates)** | **2** | Author Shard 18, Author Shard 20 | Command exited with code 1. / Command output: / [-] FAIL: 4 errores detectados (4 errores  |
| **Non-Zero CLI Exit / Subprocess Probe (Exit Code 1)** | **1** | Orchestrator | Encountered error in step execution: declaring permissions: failed to parse path: courses/ |
| **Stage Contract / Pipeline Loader Mismatch (run.py / judge.py)** | **1** | Orchestrator | Command exited with code 1. / Command output: / ========================================== |

---

## 10. Paquete Forense Agéntico Completo (Argon QA + Clúster Flash)

Todos los artefactos originales individuales generados por los auditores especializados se preservan íntegros en [`reports/audits_archive/estadistica_3_s9_vmapreduce/`](file:///D:/Augusto/personal_portfolio/Tops_academy/reports/audits_archive/estadistica_3_s9_vmapreduce/):

- **Auditoría Cualitativa Profunda de Calidad (Gemini 4 Argon):** [`qa_report.md`](file:///D:/Augusto/personal_portfolio/Tops_academy/reports/audits_archive/estadistica_3_s9_vmapreduce/qa_report.md) | [`qa_report.json`](file:///D:/Augusto/personal_portfolio/Tops_academy/reports/audits_archive/estadistica_3_s9_vmapreduce/qa_report.json)
- **Informe Maestro Agéntico del Pipeline (Gemini Flash Lead + 3 Subagentes):** [`agentic_pipeline_audit.md`](file:///D:/Augusto/personal_portfolio/Tops_academy/reports/audits_archive/estadistica_3_s9_vmapreduce/agentic_pipeline_audit.md)
- **Sub-Auditorías del Clúster Agéntico (`agentic_batches/`):** [`agentic_batches/`](file:///D:/Augusto/personal_portfolio/Tops_academy/reports/audits_archive/estadistica_3_s9_vmapreduce/agentic_batches/)
- **Dashboard Visual Interactivo:** [`dashboard.html`](file:///D:/Augusto/personal_portfolio/Tops_academy/reports/audits_archive/estadistica_3_s9_vmapreduce/dashboard.html)
- **Índice Completo del Archivo Persistente:** [`README.md`](file:///D:/Augusto/personal_portfolio/Tops_academy/reports/audits_archive/estadistica_3_s9_vmapreduce/README.md)
