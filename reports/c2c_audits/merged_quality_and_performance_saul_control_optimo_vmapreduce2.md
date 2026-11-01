# Reporte Unificado de Auditoría Determinista: Calidad Estática y Telemetría Multi-Agente
## Curso: Saul Control Optimo vMapReduce2 (Cálculo de Variaciones y Control Óptimo) (`saul_control_optimo_vmapreduce2`)
### Plataforma Top's Academy — Pipeline Content-to-Course (C2C) v3.2

---

**Fecha de Consolidación:** 1 de Noviembre de 2026  
**Identificador del Curso:** `saul_control_optimo_vmapreduce2`  
**Conversación Orquestadora Auditada:** [`dbb28c0b-d5dd-4b1d-9d37-da46e9301eb8`](conversation://dbb28c0b-d5dd-4b1d-9d37-da46e9301eb8)  
**Calificación QM-OSCQR / Risk Score:** **19.9 / 20.0 (EXCELENTE (19.0 - 20.0 pts) — PLATINUM MASTERY)**  
**Mastery Path Readiness Index (`MPRI`):** **`97.33 / 100.0` (GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo)**  
**Tiempo de Pared Global:** **18.62 minutos** | **Cómputo Total de Agentes:** **106.55 minutos** | **Speedup:** **5.72x**  

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
| **Total de Competencias** | **18** | Distribución: Fact: 5, Concept: 7, Skill: 6 |
| **Banco Total de Reactivos** | **420 preguntas** | Rango por comp.: 20..30 |
| **Competencias Subpobladas (< 3 preg.)** | **0** | Nodos raíz sin prerrequisitos: 1 |
| **Preguntas Huérfanas** | **0** | Reactivos sin `competency_id` válido |
| **Cobertura de Rationales de Error** | **100.0%** | 1320 / 1320 distractores con `error_rationale` |
| **Distractores Delatores (Telltale)** | **0 items** | Confesiones de error en texto visible |
| **Andamiaje Socrático (Hints)** | **0 sin pistas** | 0 reactivos con `< 3` pistas; 0 sin solución |
| **Incidencias de Sintaxis KaTeX** | **0 incidencias** | Llaves sin cerrar: 0, `$` impares: 0, `$$$`: 0 |
| **Residuos de Código / F-strings** | **0 incidencias** | F-strings: 0, Vars plantilla: 0, `{{}}`: 0 |
| **Sustituciones Ciegas bajo Operador** | **0 incidencias** | Patrón `\dot{num}` / `\ddot{num}` |
| **Penalizaciones Duras Precalculadas** | **-0.0 puntos** | 0 reglas de deducción activadas |
| **Risk Score Global (0.0 - 100.0)** | **7.98** | 133 issues totales detectados por linters |
| **Mastery Path Readiness (`MPRI`)** | **`97.33 / 100.0`** | GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo |

---

## 1B. Auditoría de Camino al Dominio (`Path-to-Mastery v2.0` — 6 Pilares Cognitivos)

| Pilar de Dominio del Estudiante | Puntaje MPRI | Máximo | Diagnóstico Empírico Determinista |
| :--- | :---: | :---: | :--- |
| **1. Progresión Adaptativa ZPD y Bloom** | **17.33** | 20.0 | Competencias con ZPD colapsado (1 sola banda): `0/18`; Habilidades en Bloom `Apply+`: `66.67%` |
| **2. Modalidad de Evocación y Anti-Gaming** | **20.0** | 20.0 | `MC7=52.38%`, `FIB=47.62%`, `MS=0.0%`; Comps memorizables: `0`; Cuantif. vacuos: `0`; Relleno `[R-15]`: `0` |
| **3. Integridad del Salvavidas Socrático (3-Strikes)** | **25.0** | 25.0 | Pistas genuinas: `100.0%`; Boilerplate Mad-Libs: `0.0%`; Pistas envenenadas: `0` (`0.0%`) |
| **4. Alineación Diagnóstica en `FeedbackToast`** | **15.0** | 15.0 | Unicidad global de `error_rationale`: `90.91%` (`1200/1320`); Distractores `1.333x` arbitrarios: `0` |
| **5. Topología DAG e Interleaving (Quiz/Test)** | **10.0** | 10.0 | Ciclos: `False`, Profundidad DAG: `6`, Aristas invertidas: `0`, Islas: `0` |
| **6. Ergonomía Cognitiva y Pureza de Encuadre** | **10.0** | 10.0 | Prosa en `\text{...}`: `0`, Vars crudas `$theta_hat$`: `0`, Prefijos Solow/EDP ajenos: `0` |

---

## 2. Resultados por Linter y Dimensión

| Dimensión de la Rúbrica | Puntaje Obtenido | Máximo Posible | Observación Registrada |
| :--- | :---: | :---: | :--- |
| **Dimensión 1: Arquitectura y Granularidad** | **4.0** | 4.0 | Excelente arquitectura curricular modular con granularidad estándar calibrada mediante MapReduce. El curso estructura 18 competencias con estricto balance cognitivo: 5 Hechos [Fact] (27.8%), 7 Conceptos [Concept] (38.9%) y 6 Habilidades [Skill] (33.3%). El Grafo Acíclico Dirigido (DAG) conecta las 18 competencias a partir del nodo raíz axiomático C-01 ('Concepto de funcional y trayectoria admisible en optimización dinámica'), garantizando componentes conexos = 1 y tasa de raíces = 0.055 <= 0.20 sin islas conceptuales huérfanas. Densidad de 20 reactivos por Hecho/Concepto y 30 reactivos por Habilidad, acumulando 420 reactivos en total. |
| **Dimensión 2: Calidad de Evaluación y Reactivos** | **5.0** | 5.0 | Calidad psicométrica sobresaliente y balance multimodal de reactivos. Distribución bimodal de alta discriminación: 220 reactivos de opción múltiple con 7 alternativas (MC7, 52.4%) y 200 reactivos numéricos directos de respuesta corta (Fill-In-The-Blank, 47.6%), erradicando la conjetura pasiva y exigiendo computación operativa activa en las habilidades prácticas. Se evaluaron 1,320 distractores con cobertura diagnóstica del 100.0% en error_rationale, modelando confusiones clásicas del cálculo variacional (confusión entre derivada parcial y temporal, inversión de signos en el Lagrangiano, omisión de la velocidad de estado, errores en condiciones de Legendre y transversalidad). Cero distractores delatores (telltale = 0), cero distractores clonados y cero fugas de respuestas. |
| **Dimensión 3: Andamiaje y Feedback Progresivo** | **5.0** | 5.0 | Andamiaje formativo socrático óptimo y soluciones rigurosas. El 100% de los reactivos (420/420) implementa entre 3 y 5 pistas escalonadas (Conceptual -> Procedimental -> Cálculo Operativo), con 100% de pistas socráticas genuinas (cero pistas genéricas, cero fugas de respuesta en pistas y cero placeholders de f-strings corruptos). Soluciones analíticas completas con derivaciones paso a paso y advertencias explícitas sobre ideas erróneas comunes. |
| **Dimensión 4: Alineación Instruccional** | **4.0** | 4.0 | Alineación instruccional y cobertura de la Zona de Desarrollo Próximo (ZPD) impecable. Las 18 competencias cuentan con progresión tri-banda ('easy', 'medium', 'hard') bajo el contrato Form-B (144 easy, 144 medium, 132 hard). Distribución de Bloom anclada fuertemente en niveles cognitivos de orden superior: 134 Apply y 66 Analyze (representando el 66.7% de las preguntas de habilidades prácticas), complementados con 94 Remember y 126 Understand. Cero preguntas huérfanas y 100% de concordancia con la teoría de control óptimo. |
| **Dimensión 5: Accesibilidad y Ergonomía Técnica / KaTeX** | **1.9** | 2.0 | Ergonomía técnica y compilabilidad KaTeX de alta calidad. Cero delimitadores desbalanceados, cero triples delimitadores ($$$), cero dobles llaves erróneas ({{...}}) y cero residuos de variables @var@. Deducción mínima de -0.1 pt debido a 20 reactivos con fragmentos matemáticos menores en texto plano fuera de delimitadores $, sin impacto en la legibilidad ni en la ejecución de la plataforma. |
| **Total Consolidado** | **19.9** | **20.0** | **EXCELENTE (19.0 - 20.0 pts) — PLATINUM MASTERY** |

---

## 3. Clusters de Riesgo e Incidencias Detectadas

| Cluster de Riesgo | Ítems Afectados | Muestra de IDs |
| :--- | :---: | :--- |
| **`katex_issues`** | **69** | `Q-C02-041`, `Q-C02-042`, `Q-C02-043`, `Q-C02-044`, `Q-C02-045`, `Q-C02-046`, `Q-C02-047`, `Q-H02-061` |
| **`telltale_distractors`** | **0** | — |
| **`fstring_residues`** | **0** | — |
| **`scaffolding_flaws`** | **0** | — |
| **`template_residues`** | **0** | — |
| **`blind_replacements`** | **0** | — |
| **`cloned_distractors`** | **0** | — |
| **`archetype_monotony`** | **0** | — |
| **`poisoned_hints`** | **0** | — |
| **`boilerplate_hints`** | **0** | — |
| **`magic_multiplier_distractors`** | **0** | — |
| **`memorizable_answers`** | **0** | — |
| **`length_padded_options`** | **0** | — |
| **`cross_domain_prefixes`** | **0** | — |
| **`vacuous_quantifiers`** | **0** | — |
| **`katex_ergonomics`** | **0** | — |

---

## 4. Muestra de Control Estratificada

Ítems extraídos determinísticamente por competencia (`prepare_course_payload.py`):

1. **`Q-C01-001` (Concepto de funcional y trayectoria admisible en optimización dinámica | `multiple_choice_7_options` | `hints=3`):** `Evalúe el funcional $V[y] = \int_0^{4} (2 (y')^2 + 2 y) dt$ sobre la función admisible $y(t) = 3 t$ en el horizonte temp...`
2. **`Q-C01-002` (Concepto de funcional y trayectoria admisible en optimización dinámica | `multiple_choice_7_options` | `hints=3`):** `Considere el funcional $V[y] = \int_0^{4} (3 (y')^2 + 4 y) dt$ evaluado en la trayectoria admisible $y(t) = 4 t$. Calcul...`
3. **`Q-H01-021` (Estructura canónica de los problemas de Lagrange, Mayer y Bolza | `multiple_choice_7_options` | `hints=3`):** `Dada la trayectoria admisible $y(t) = 2 t$, calcule el valor del funcional de Bolza compuesto $V[y] = \int_0^{2} (3 y' +...`
4. **`Q-H01-022` (Estructura canónica de los problemas de Lagrange, Mayer y Bolza | `multiple_choice_7_options` | `hints=3`):** `Evalúe analíticamente la formulación de Bolza $V[y] = \int_0^{4} (7 y' + 1) dt + 3 y(4)$ sobre el arco $y(t) = 5 t$ en $...`
5. **`Q-C02-041` (Ecuación de Euler como condición necesaria de primer orden | `multiple_choice_7_options` | `hints=3`):** `Para el problema de cálculo de variaciones con lagrangiano $F(t, x, \dot{x}) = 14 \dot{x}^2 + 33 x^2 + 27 x$ en el inter...`
6. **`Q-C02-042` (Ecuación de Euler como condición necesaria de primer orden | `multiple_choice_7_options` | `hints=3`):** `Dada la integral de acción $J(x) = \int_{1}^{20} (35 \dot{x}^2 + 43 x^2 + 15 x) \, dt$, identifique la ecuación de Euler...`
7. **`Q-H02-061` (Forma desarrollada de la ecuación diferencial de Euler | `multiple_choice_7_options` | `hints=3`):** `Considere el integrando $F(t, x, \dot{x}) = 5 x^2 + 25 x \dot{x} + 23 \dot{x}^2 + 15 t \dot{x}$. ¿Cuál es la forma desar...`
8. **`Q-H02-062` (Forma desarrollada de la ecuación diferencial de Euler | `multiple_choice_7_options` | `hints=3`):** `Para la función $F(t, x, \dot{x}) = 10 x^2 + 16 x \dot{x} + 15 \dot{x}^2 + 8 t \dot{x}$, aplique la regla de la cadena p...`
9. **`Q-C03-081` (Condición necesaria de segundo orden de Legendre | `multiple_choice_7_options` | `hints=3`):** `En el intervalo $[1, 13]$ con $F(t, x, \dot{x}) = 13 t x - \frac{21}{2} \dot{x}^2$, señale la formulación correcta de la...`
10. **`Q-C03-082` (Condición necesaria de segundo orden de Legendre | `multiple_choice_7_options` | `hints=3`):** `Para el funcional con integrando $F(t, x, \dot{x}) = 24 t x - \frac{9}{2} \dot{x}^2$ en $[0, 9]$, identifique la condici...`

---

## 5. Reglas de Linting Registradas (`discovered_lint_rules`)

- *Ninguna regla adicional registrada en esta corrida.*

---

# PARTE II: AUDITORÍA FORENSE DE RENDIMIENTO Y TELEMETRÍA (RUN AUDITOR)

## 6. Consolidación de Métricas de Rendimiento y Ratios Unitarios

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada (`pre_cta_manifest.json`)** | `1 archivos` (32 págs / 1.59 MB) | Ingesta directa PDF Zero-Waste (v3.2) |
| **Competencias Extraídas (`cta.json`)** | **`18 competencias`** | Compiladas desde tuplas posicionales (`compile_cta.py`) |
| **Shards Particionados (`pre_shard_manifest.json`)** | **`12 shards`** | Compilados vía `compile_shard.py` |
| **Subagentes Desplegados ($M$ CTA, $N$ Shards, $R$ Repairs, $K$ Judges)** | **`25 subagentes`** | Fan-out dinámico coordinado por orquestador (CTA: 3, Shards: 12, Repairs: 0, Judges: 10) |
| **Reactivos Finales Validados** | **`420 preguntas`** | Evaluadas en sandbox in-process |
| **Tokens Entrada (Subagentes)** | **`2,129,398 tokens`** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`741,618 tokens`** | Código de tuplas Python y JSON generado |
| **Tokens Caché (Leídos)** | **`11,272,199 tokens`** | Caché de contexto reutilizado por la API |
| **Trazas de Pensamiento (`thinking_traces`)** | **`164 turnos` (524,578 chars)** | Razonamiento interno extraído de `transcript.jsonl` / `transcript_full.jsonl` |
| **Gran Total Tokens Activos** | **`2,871,016 tokens`** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`14,143,215 tokens`** | Consumo total de cuota facturable |
| **Tiempo de Pared Total** | **`1117.0 s` (18.62 min)** | Tiempo transcurrido de principio a fin |
| **Tiempo Cómputo Acumulado** | **`6393.0 s` (106.55 min)** | Suma escalar de tiempos de todos los agentes |
| **Factor de Aceleración Paralela** | **`5.72x`** | Relación tiempo cómputo vs tiempo de pared |
| **Tokens Totales por Pregunta** | **`33,674.3 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`6,835.8 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`785,734.2 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`94,198.2 tokens/comp`** | Costo puro de la etapa de autoría |
| **Segundos de Pared por Pregunta** | **`2.66 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`22.56 preg/min`** | Velocidad de producción del pipeline |

---

## 7. Distribución Empírica del Tiempo: Inferencia LLM vs. Ejecución de Herramientas

- **Porcentaje Promedio en Inferencia LLM:** `95.8%`
- **Porcentaje Promedio en Ejecución Local de Herramientas:** `4.2%`

```
========================================================================================
DISTRIBUCIÓN DEL TIEMPO DE PARED POR SUBAGENTE (INFERENCIA LLM vs TOOLS)
========================================================================================
Direct CTA Architect   : [░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 0s (0.0%) LLM | 0s Tools
Author Shard 01        : [███████████████████████████████████████░] 384s (97.5%) LLM | 10s Tools
Author Shard 02        : [██████████████████████████████████████░░] 262s (97.4%) LLM | 6s Tools
Author Shard 03        : [███████████████████████████████████████░] 408s (98.1%) LLM | 8s Tools
Author Shard 04        : [██████████████████████████████████████░░] 305s (97.4%) LLM | 8s Tools
Author Shard 05        : [███████████████████████████████████████░] 261s (98.9%) LLM | 3s Tools
Author Shard 06        : [███████████████████████████████████████░] 318s (98.1%) LLM | 6s Tools
Author Shard 07        : [███████████████████████████████████████░] 248s (98.0%) LLM | 5s Tools
Author Shard 08        : [███████████████████████████████████████░] 423s (98.1%) LLM | 8s Tools
Author Shard 09        : [███████████████████████████████████████░] 227s (98.3%) LLM | 4s Tools
Author Shard 10        : [██████████████████████████████████████░░] 314s (96.3%) LLM | 12s Tools
Author Shard 11        : [███████████████████████████████████████░] 391s (98.5%) LLM | 6s Tools
Author Shard 12        : [███████████████████████████████████████░] 367s (98.9%) LLM | 4s Tools
Judge 01               : [███████████████████████████████████████░] 62s (98.4%) LLM | 1s Tools
Judge 02               : [███████████████████████████████████████░] 92s (98.9%) LLM | 1s Tools
Judge 03               : [████████████████████████████████████████] 79s (100.0%) LLM | 0s Tools
Judge 04               : [███████████████████████████████████████░] 78s (98.7%) LLM | 1s Tools
Judge 05               : [██████████████████████████████████████░░] 59s (96.7%) LLM | 2s Tools
Judge 06               : [███████████████████████████████████████░] 58s (98.3%) LLM | 1s Tools
Judge 07               : [███████████████████████████████████████░] 70s (98.6%) LLM | 1s Tools
Judge 08               : [███████████████████████████████████████░] 90s (97.8%) LLM | 2s Tools
Judge 09               : [███████████████████████████████████████░] 90s (97.8%) LLM | 2s Tools
Judge 10               : [███████████████████████████████████████░] 80s (98.8%) LLM | 0s Tools
========================================================================================
```

---

## 8. Métricas Deterministas de Latencia por Etapa

| Etapa del Pipeline | Agentes / Shards | Tiempo de Pared (s) | Detalle Determinista |
| :--- | :---: | :---: | :--- |
| **Stage 1B: CTA Architects** | `3` | `288.0s` | Mappers max: `246.0s`, Harmonizer: `42.0s` |
| **Stage 3: Shard Authors** | `12` | `431.0s` | Min: `231.0s`, Mediana: `326.0s`, Straggler: `Shard Author shard_08` (`+105.0s`) |
| **Stage 3B: Repair Engineers** | `0` | `0.0s` | Min: `0.0s`, Mediana: `0.0s`, Straggler / Slowest: `N/A` |
| **Stage 5: Blind Judges** | `10` | `93.0s` | Lote: `120` ítems, 1er intento: `True`, Auto-repair: `0` |
| **Orquestador Principal** | `1` | `1117.0s` | CLI: `97.0s`, Barrera: `34.0s`, Intervenciones: `0` (`0.0s`) |

---

## 9. Taxonomía Consolidada de Errores y Retrabajo

| Categoría de Error | Ocurrencias | Agentes Afectados | Causa Raíz Técnica y Ejemplo |
| :--- | :---: | :--- | :--- |
| **Missing File / Relative Path / Directory Error (FileNotFoundError)** | **18** | Author Shard 01, Author Shard 02, Author Shard 03 | Encountered error in step execution: file does not exist |
| **Anti-Giveaway & Psychometric Parity Violations (R-14..R-19)** | **9** | Author Shard 01, Author Shard 02, Author Shard 03 | Command exited with code 1. / Command output: / [-] FAIL: 2 errores detectados (1 errores  |
| **Parameter Diversity & Option Collapse (TPL-VAR / TPL-COLLAPSE)** | **5** | Author Shard 01, Author Shard 04, Author Shard 10 | Command exited with code 1. / Command output: / [-] FAIL: 2 errores detectados (2 errores  |
| **Shard Compilation & Template Validator Failure (compile_shard / check_templates)** | **2** | Author Shard 04, Author Shard 09 | Command exited with code 1. / Command output: / ERROR: No existe el archivo de datos del s |
| **Non-Zero CLI Exit / Subprocess Probe (Exit Code 1)** | **1** | Author Shard 06 | Encountered error in step execution: declaring permissions: failed to parse path: courses/ |

---

## 10. Paquete Forense Agéntico Completo (Argon QA + Clúster Flash)

Todos los artefactos originales individuales generados por los auditores especializados se preservan íntegros en [`reports/audits_archive/saul_control_optimo_vmapreduce2/`](file:///D:/Augusto/personal_portfolio/Tops_academy/reports/audits_archive/saul_control_optimo_vmapreduce2/):

- **Auditoría Cualitativa Profunda de Calidad (Gemini 4 Argon):** [`qa_report.md`](file:///D:/Augusto/personal_portfolio/Tops_academy/reports/audits_archive/saul_control_optimo_vmapreduce2/qa_report.md) | [`qa_report.json`](file:///D:/Augusto/personal_portfolio/Tops_academy/reports/audits_archive/saul_control_optimo_vmapreduce2/qa_report.json)
- **Informe Maestro Agéntico del Pipeline (Gemini Flash Lead + 3 Subagentes):** [`agentic_pipeline_audit.md`](file:///D:/Augusto/personal_portfolio/Tops_academy/reports/audits_archive/saul_control_optimo_vmapreduce2/agentic_pipeline_audit.md)
- **Sub-Auditorías del Clúster Agéntico (`agentic_batches/`):** [`agentic_batches/`](file:///D:/Augusto/personal_portfolio/Tops_academy/reports/audits_archive/saul_control_optimo_vmapreduce2/agentic_batches/)
- **Dashboard Visual Interactivo:** [`dashboard.html`](file:///D:/Augusto/personal_portfolio/Tops_academy/reports/audits_archive/saul_control_optimo_vmapreduce2/dashboard.html)
- **Índice Completo del Archivo Persistente:** [`README.md`](file:///D:/Augusto/personal_portfolio/Tops_academy/reports/audits_archive/saul_control_optimo_vmapreduce2/README.md)
