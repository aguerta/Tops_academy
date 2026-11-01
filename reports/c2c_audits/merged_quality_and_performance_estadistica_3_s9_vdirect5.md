# Reporte Unificado de Auditoría Determinista: Calidad Estática y Telemetría Multi-Agente
## Curso: Estadistica 3 S9 Vdirect5 (`estadistica_3_s9_vdirect5`)
### Plataforma Top's Academy — Pipeline Content-to-Course (C2C) v3.2

---

**Fecha de Consolidación:** 1 de Noviembre de 2026  
**Identificador del Curso:** `estadistica_3_s9_vdirect5`  
**Conversación Orquestadora Auditada:** [`597bb79e`](conversation://597bb79e)  
**Calificación QM-OSCQR / Risk Score:** **18.9 / 20.0 (EXCELENTE (17-20))**  
**Mastery Path Readiness Index (`MPRI`):** **`96.95 / 100.0` (GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo)**  
**Tiempo de Pared Global:** **136.28 minutos** | **Cómputo Total de Agentes:** **299.07 minutos** | **Speedup:** **2.19x**  

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
| **Total de Competencias** | **24** | Distribución: Fact: 7, Concept: 10, Skill: 7 |
| **Banco Total de Reactivos** | **550 preguntas** | Rango por comp.: 20..30 |
| **Competencias Subpobladas (< 3 preg.)** | **0** | Nodos raíz sin prerrequisitos: 2 |
| **Preguntas Huérfanas** | **0** | Reactivos sin `competency_id` válido |
| **Cobertura de Rationales de Error** | **100.0%** | 1794 / 1794 distractores con `error_rationale` |
| **Distractores Delatores (Telltale)** | **0 items** | Confesiones de error en texto visible |
| **Andamiaje Socrático (Hints)** | **0 sin pistas** | 0 reactivos con `< 3` pistas; 0 sin solución |
| **Incidencias de Sintaxis KaTeX** | **0 incidencias** | Llaves sin cerrar: 0, `$` impares: 0, `$$$`: 0 |
| **Residuos de Código / F-strings** | **0 incidencias** | F-strings: 0, Vars plantilla: 0, `{{}}`: 0 |
| **Sustituciones Ciegas bajo Operador** | **0 incidencias** | Patrón `\dot{num}` / `\ddot{num}` |
| **Penalizaciones Duras Precalculadas** | **-0.0 puntos** | 0 reglas de deducción activadas |
| **Risk Score Global (0.0 - 100.0)** | **24.64** | 271 issues totales detectados por linters |
| **Mastery Path Readiness (`MPRI`)** | **`96.95 / 100.0`** | GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo |

---

## 1B. Auditoría de Camino al Dominio (`Path-to-Mastery v2.0` — 6 Pilares Cognitivos)

| Pilar de Dominio del Estudiante | Puntaje MPRI | Máximo | Diagnóstico Empírico Determinista |
| :--- | :---: | :---: | :--- |
| **1. Progresión Adaptativa ZPD y Bloom** | **16.95** | 20.0 | Competencias con ZPD colapsado (1 sola banda): `0/24`; Habilidades en Bloom `Apply+`: `61.9%` |
| **2. Modalidad de Evocación y Anti-Gaming** | **20.0** | 20.0 | `MC7=54.36%`, `FIB=45.64%`, `MS=0.0%`; Comps memorizables: `0`; Cuantif. vacuos: `0`; Relleno `[R-15]`: `0` |
| **3. Integridad del Salvavidas Socrático (3-Strikes)** | **25.0** | 25.0 | Pistas genuinas: `100.0%`; Boilerplate Mad-Libs: `0.0%`; Pistas envenenadas: `0` (`0.0%`) |
| **4. Alineación Diagnóstica en `FeedbackToast`** | **15.0** | 15.0 | Unicidad global de `error_rationale`: `91.25%` (`1637/1794`); Distractores `1.333x` arbitrarios: `0` |
| **5. Topología DAG e Interleaving (Quiz/Test)** | **10.0** | 10.0 | Ciclos: `False`, Profundidad DAG: `7`, Aristas invertidas: `0`, Islas: `0` |
| **6. Ergonomía Cognitiva y Pureza de Encuadre** | **10.0** | 10.0 | Prosa en `\text{...}`: `0`, Vars crudas `$theta_hat$`: `0`, Prefijos Solow/EDP ajenos: `0` |

---

## 2. Resultados por Linter y Dimensión

| Dimensión de la Rúbrica | Puntaje Obtenido | Máximo Posible | Observación Registrada |
| :--- | :---: | :---: | :--- |
| **Dimensión 1: Arquitectura y Granularidad** | **4.0** | 4.0 | Topología DAG impecable de 24 micro-competencias atómicas balanceadas (7 Hechos, 10 Conceptos, 7 Habilidades). Grafo acíclico y estrictamente conexo con profundidad máxima de 7 niveles, orden topológico riguroso (idx(prereq) < idx(comp)), sin dependencias invertidas ni competencias huérfanas. Calibración ZPD perfecta: el 100% (24/24) de las competencias disponen de las tres bandas de dificultad requeridas (189 easy, 189 medium, 172 hard), permitiendo la activación plena de calibrateByMasteryDifficulty en todo el ciclo de transiciones hacia Mastered. Granularidad óptima con 20 a 30 reactivos por competencia. |
| **Dimensión 2: Calidad de Evaluación y Reactivos** | **4.8** | 5.0 | Excelente diversidad psicométrica con un balance robusto entre reconocimiento pasivo (299 reactivos MC7, 54.36%) y evocación activa generativa (251 reactivos FIB, 45.64%), superando ampliamente el umbral normativo del 40% de generación activa. 100% de cobertura de rationales diagnósticos (1794/1794 distractores) con alta tasa de unicidad (91.25%, 1637 explicaciones únicas). Cero multiplicadores mágicos sintéticos (1.333x), cero distractores delatores por longitud o pistas directas, cero distractores clonados y cero vulnerabilidad de memorización visual. Validación ciega de Stage 5 con 100% de acuerdo (216/216 reactivos sin desacuerdos). Deducción menor (-0.2 pts) por ausencia de reactivos multiple_select (MS) para discriminación multivariada condicional. |
| **Dimensión 3: Andamiaje y Feedback Progresivo** | **4.7** | 5.0 | Andamiaje socrático sobresaliente: cero reactivos sin pistas, 100% del banco dotado de 3 a 4 pistas socráticas escalonadas (Conceptual -> Procedimental -> Operativa sin regalar clave), cero boilerplate sintético Mad-Libs, cero fugas de respuestas y cero pistas envenenadas (0% poisoned). Soluciones analíticas paso a paso exhaustivas en el 100% de los reactivos. Deducción leve (-0.3 pts) debido a que los 251 reactivos FIB mantienen advertencias de error conceptual genéricas en contraste con las advertencias hiper-específicas de los reactivos MC7. |
| **Dimensión 4: Alineación Instruccional** | **3.8** | 4.0 | Rigor disciplinar impecable y pureza absoluta de dominio en estadística matemática e inferencia asintótica (consistencia débil, convergencia casi segura, Slutsky, TCL Lindeberg-Lévy, Teorema de Mann-Wald y Método Delta). Cero contaminación léxica inter-dominio (0% cross-domain). Cero cuantificadores universales vacuos. Las competencias de Habilidad alcanzan un 61.9% de niveles cognitivos superiores (Apply y Analyze). Deducción de -0.2 pts por sub-etiquetado Bloom en un 38.1% de ítems de Habilidad clasificados como 'Understand' a pesar de involucrar deducciones analíticas avanzadas. |
| **Dimensión 5: Accesibilidad y Ergonomía Técnica / KaTeX** | **1.6** | 2.0 | Sintaxis KaTeX mayoritariamente limpia: cero llaves rotas, cero dólares impares, cero triples dólares, cero residuos de f-strings y cero bloques de prosa en \text{...} que rompan el diseño responsivo móvil. No obstante, se detectó un defecto ergonómico puntual en 13 reactivos de la competencia H-06 (Q-H06-431 a Q-H06-437 y Q-H06-445 a Q-H06-450), donde los distractores exponen comandos LaTeX en texto plano sin delimitar entre signos de dólar '$' (ej. '\operatorname{Var}(\bar{Y}_n) = 25'), ocasionando que la interfaz del estudiante renderice código LaTeX crudo en lugar de fórmulas matemáticas (-0.4 pts). |
| **Total Consolidado** | **18.9** | **20.0** | **EXCELENTE (17-20)** |

---

## 3. Clusters de Riesgo e Incidencias Detectadas

| Cluster de Riesgo | Ítems Afectados | Muestra de IDs |
| :--- | :---: | :--- |
| **`katex_issues`** | **147** | `Q-H01-001`, `Q-H01-002`, `Q-H01-003`, `Q-H01-004`, `Q-H01-005`, `Q-H01-006`, `Q-H01-007`, `Q-H01-015` |
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

1. **`Q-H01-001` (Definición de Muestra Aleatoria Simple y Estimador Puntual | `multiple_choice_7_options` | `hints=4`):** `Dada una colección de $n=36$ variables aleatorias $Y_1, \dots, Y_{36}$ i.i.d., determine cuál de las opciones representa...`
2. **`Q-H01-002` (Definición de Muestra Aleatoria Simple y Estimador Puntual | `multiple_choice_7_options` | `hints=4`):** `Al extraer una muestra aleatoria simple de $n=72$ elementos con distribución $F_Y$, ¿qué expresión matemática define rig...`
3. **`Q-H02-021` (Axiomas de Probabilidad y Espacio Muestral de Kolmogorov | `multiple_choice_7_options` | `hints=3`):** `Dos sucesos no excluyentes presentan probabilidades marginales $P(A) = 0.463$, $P(B) = 0.312$, mientras que su intersecc...`
4. **`Q-H02-022` (Axiomas de Probabilidad y Espacio Muestral de Kolmogorov | `multiple_choice_7_options` | `hints=3`):** `A partir de las asignaciones de probabilidad $P(A) = 0.634$, $P(B) = 0.255$ y $P(A \cap B) = 0.129$ compatibles con los ...`
5. **`Q-C01-041` (Sesgo e Insesgadez en Muestras Finitas | `multiple_choice_7_options` | `hints=3`):** `En un estudio de inferencia paramétrica con $n = 20$ datos, un investigador evalúa $\hat{\theta}$ para el parámetro $\th...`
6. **`Q-C01-042` (Sesgo e Insesgadez en Muestras Finitas | `multiple_choice_7_options` | `hints=3`):** `Un proceso de calibración reporta que el parámetro objetivo vale $\theta = 284$. Al aplicar el estimador puntual con $n ...`
7. **`Q-C02-061` (Varianza y Eficiencia Relativa de Estimadores | `multiple_choice_7_options` | `hints=3`):** `Evalúe la varianza teórica $Var(\bar{Y}_n)$ que exhibe la media aritmética de $n = 6$ variables aleatorias independiente...`
8. **`Q-C02-062` (Varianza y Eficiencia Relativa de Estimadores | `multiple_choice_7_options` | `hints=3`):** `Para una muestra aleatoria simple de tamaño $n = 16$ tomada de una población con varianza $\sigma^2 = 608$, calcule la v...`
9. **`Q-C03-081` (Descomposición y Trade-off del Error Cuadrático Medio | `multiple_choice_7_options` | `hints=3`):** `Calcule la magnitud del error cuadrático medio $ECM(\hat{\theta})$ para un modelo cuyo estimador presenta dispersión int...`
10. **`Q-C03-082` (Descomposición y Trade-off del Error Cuadrático Medio | `multiple_choice_7_options` | `hints=3`):** `Bajo la descomposición aditiva clásica del riesgo cuadrático, halle $ECM(\hat{\theta})$ sabiendo que $Var(\hat{\theta}) ...`

---

## 5. Reglas de Linting Registradas (`discovered_lint_rules`)

* **ID de Regla:** `orphan_latex_command_in_option_text`
* **Severidad:** warning
* **Patrón Regex:** `^(?:\\operatorname|\\bar|\\sum|\\frac|\\lim|\\sqrt)[^$]*$`
* **Descripción:** Detecta opciones que inician con un comando LaTeX pero omiten los delimitadores '$...$', provocando que KaTeX muestre texto crudo en lugar de símbolos matemáticos formateados.
* **Ítems Evidencia:** Q-H06-431, Q-H06-432, Q-H06-433, Q-H06-434, Q-H06-435, Q-H06-436, Q-H06-437, Q-H06-445, Q-H06-446, Q-H06-447, Q-H06-448, Q-H06-449, Q-H06-450

* **ID de Regla:** `latex_braced_symbol_false_positive_filter`
* **Severidad:** info
* **Patrón Regex:** `(?<!\\bar|\\operatorname|\\text|\^|_)\{[a-zA-Z_][a-zA-Z0-9_]*\}`
* **Descripción:** Filtro de contexto negativo para 'uninterpolated_math_variable_linter'. Evita falsos positivos en agrupadores sintácticos legítimos de LaTeX como \bar{Y}, \bar{X}, F_{Y_j}, \operatorname{plim} y \text{MSE}.
* **Ítems Evidencia:** Q-H01-001, Q-C01-055, Q-C02-061, Q-Hab02-151, Q-C05-303, Q-C06-321, Q-C07-343, Q-C09-411, Q-C10-481

---

# PARTE II: AUDITORÍA FORENSE DE RENDIMIENTO Y TELEMETRÍA (RUN AUDITOR)

## 6. Consolidación de Métricas de Rendimiento y Ratios Unitarios

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada (`pre_cta_manifest.json`)** | `2 archivos` (80 págs / 0.93 MB) | Ingesta directa PDF Zero-Waste (v3.2) |
| **Competencias Extraídas (`cta.json`)** | **`24 competencias`** | Compiladas desde tuplas posicionales (`compile_cta.py`) |
| **Shards Particionados (`pre_shard_manifest.json`)** | **`16 shards`** | Compilados vía `compile_shard.py` |
| **Subagentes Desplegados ($M$ CTA, $N$ Shards, $R$ Repairs, $K$ Judges)** | **`62 subagentes`** | Fan-out dinámico coordinado por orquestador (CTA: 1, Shards: 16, Repairs: 26, Judges: 18) |
| **Reactivos Finales Validados** | **`550 preguntas`** | Evaluadas en sandbox in-process |
| **Tokens Entrada (Subagentes)** | **`5,148,780 tokens`** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`1,381,348 tokens`** | Código de tuplas Python y JSON generado |
| **Tokens Caché (Leídos)** | **`31,668,442 tokens`** | Caché de contexto reutilizado por la API |
| **Trazas de Pensamiento (`thinking_traces`)** | **`374 turnos` (926,150 chars)** | Razonamiento interno extraído de `transcript.jsonl` / `transcript_full.jsonl` |
| **Gran Total Tokens Activos** | **`6,530,128 tokens`** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`38,198,570 tokens`** | Consumo total de cuota facturable |
| **Tiempo de Pared Total** | **`8177.0 s` (136.28 min)** | Tiempo transcurrido de principio a fin |
| **Tiempo Cómputo Acumulado** | **`17944.0 s` (299.07 min)** | Suma escalar de tiempos de todos los agentes |
| **Factor de Aceleración Paralela** | **`2.19x`** | Relación tiempo cómputo vs tiempo de pared |
| **Tokens Totales por Pregunta** | **`69,451.9 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`11,873.0 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`1,591,607.1 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`88,670.0 tokens/comp`** | Costo puro de la etapa de autoría |
| **Segundos de Pared por Pregunta** | **`14.87 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`4.04 preg/min`** | Velocidad de producción del pipeline |

---

## 7. Distribución Empírica del Tiempo: Inferencia LLM vs. Ejecución de Herramientas

- **Porcentaje Promedio en Inferencia LLM:** `95.8%`
- **Porcentaje Promedio en Ejecución Local de Herramientas:** `4.2%`

```
========================================================================================
DISTRIBUCIÓN DEL TIEMPO DE PARED POR SUBAGENTE (INFERENCIA LLM vs TOOLS)
========================================================================================
Direct CTA Architect   : [███████████████████████████████████████░] 613s (99.7%) LLM | 2s Tools
Author Shard 01        : [███████████████████████████████████████░] 193s (97.5%) LLM | 5s Tools
Author Shard 02        : [███████████████████████████████████████░] 265s (98.9%) LLM | 3s Tools
Author Shard 03        : [███████████████████████████████████████░] 251s (98.4%) LLM | 4s Tools
Author Shard 04        : [███████████████████████████████████████░] 233s (98.7%) LLM | 3s Tools
Author Shard 05        : [███████████████████████████████████████░] 226s (97.8%) LLM | 5s Tools
Author Shard 06        : [███████████████████████████████████████░] 258s (97.7%) LLM | 6s Tools
Author Shard 07        : [███████████████████████████████████████░] 260s (98.5%) LLM | 4s Tools
Author Shard 08        : [███████████████████████████████████████░] 371s (97.6%) LLM | 9s Tools
Author Shard 09        : [██████████████████████████████████████░░] 321s (97.0%) LLM | 10s Tools
Author Shard 10        : [███████████████████████████████████████░] 340s (98.6%) LLM | 5s Tools
Author Shard 11        : [███████████████████████████████████████░] 326s (97.9%) LLM | 7s Tools
Author Shard 12        : [██████████████████████████████████████░░] 328s (97.3%) LLM | 8s Tools
Author Shard 13        : [███████████████████████████████████████░] 327s (97.9%) LLM | 7s Tools
Author Shard 14        : [███████████████████████████████████████░] 503s (98.6%) LLM | 7s Tools
Author Shard 15        : [███████████████████████████████████████░] 248s (98.4%) LLM | 4s Tools
Author Shard 16        : [███████████████████████████████████████░] 304s (97.7%) LLM | 7s Tools
Repair Engineer C-01 (ca5d59): [█████████████████████████████████░░░░░░░] 75s (83.3%) LLM | 15s Tools
Repair Engineer C-02 (4bcfce): [█████████████████████████████████░░░░░░░] 72s (83.7%) LLM | 14s Tools
Repair Engineer C-03 (2b56ee): [████████████████████████████████░░░░░░░░] 52s (80.0%) LLM | 13s Tools
Repair Engineer C-04 (df49dc): [██████████████████████████████████░░░░░░] 91s (85.8%) LLM | 15s Tools
Repair Engineer C-05 (da59bb): [████████████████████████████████████░░░░] 114s (91.2%) LLM | 11s Tools
Repair Engineer C-06 (6a1d02): [██████████████████████████████████░░░░░░] 81s (87.1%) LLM | 12s Tools
Repair Engineer C-07 (9ed32f): [████████████████████████████████░░░░░░░░] 70s (81.4%) LLM | 16s Tools
Repair Engineer C-08 (30365d): [████████████████████████████████░░░░░░░░] 66s (81.5%) LLM | 15s Tools
Repair Engineer C-09 (27ea8c): [█████████████████████████████████░░░░░░░] 83s (83.0%) LLM | 17s Tools
Repair Engineer C-10 (a5aadc): [██████████████████████████████████░░░░░░] 87s (87.0%) LLM | 12s Tools
Repair Engineer H-01 (d5b9e3): [██████████████████████████████████████░░] 71s (97.3%) LLM | 2s Tools
Repair Engineer H-02 (f10e64): [██████████████████████████████████████░░] 342s (95.5%) LLM | 16s Tools
Repair Engineer H-03 (a4312f): [███████████████████████████████░░░░░░░░░] 49s (79.0%) LLM | 13s Tools
Repair Engineer H-04 (11c749): [██████████████████████████████████░░░░░░] 92s (86.0%) LLM | 15s Tools
Repair Engineer H-04 (ed8f06): [█████████████████████████████████████░░░] 228s (93.4%) LLM | 8s Tools
Repair Engineer H-05 (8c0043): [█████████████████████████████████░░░░░░░] 76s (82.6%) LLM | 16s Tools
Repair Engineer H-06 (77f7fa): [███████████████████████████████████░░░░░] 116s (89.9%) LLM | 13s Tools
Repair Engineer H-07 (d226ef): [█████████████████████████████████░░░░░░░] 67s (83.8%) LLM | 12s Tools
Repair Engineer Hab-01 (80ba0a): [██████████████████████████████████░░░░░░] 61s (85.9%) LLM | 10s Tools
Repair Engineer Hab-02 (f50ae4): [████████████████████████████████████░░░░] 98s (90.7%) LLM | 10s Tools
Repair Engineer Hab-03 (724f8a): [██████████████████████████████████░░░░░░] 69s (85.2%) LLM | 12s Tools
Repair Engineer Hab-04 (acd36b): [████████████████████████████████████░░░░] 118s (91.5%) LLM | 11s Tools
Repair Engineer Hab-05 (3d1a58): [█████████████████████████████████░░░░░░░] 71s (84.5%) LLM | 13s Tools
Repair Engineer Hab-06 (3ea821): [███████████████████████████████████████░] 341s (98.6%) LLM | 5s Tools
Repair Engineer Hab-06 (dc55f6): [████████████████████████████████████░░░░] 90s (90.0%) LLM | 10s Tools
Repair Engineer Hab-07 (05671d): [████████████████████████████████████░░░░] 103s (90.4%) LLM | 11s Tools
Judge 01               : [███████████████████████████████████████░] 48s (98.0%) LLM | 1s Tools
Judge 02               : [███████████████████████████████████████░] 45s (97.8%) LLM | 1s Tools
Judge 03               : [████████████████████████████████████████] 49s (100.0%) LLM | 0s Tools
Judge 04               : [███████████████████████████████████████░] 50s (98.0%) LLM | 1s Tools
Judge 05               : [███████████████████████████████████████░] 57s (98.3%) LLM | 1s Tools
Judge 06               : [████████████████████████████████████████] 49s (100.0%) LLM | 0s Tools
Judge 07               : [████████████████████████████████████████] 47s (100.0%) LLM | 0s Tools
Judge 08               : [███████████████████████████████████████░] 48s (98.0%) LLM | 1s Tools
Judge 09               : [███████████████████████████████████████░] 54s (98.2%) LLM | 1s Tools
Judge 10               : [████████████████████████████████████████] 45s (100.0%) LLM | 0s Tools
Judge 11               : [████████████████████████████████████████] 43s (100.0%) LLM | 0s Tools
Judge 12               : [████████████████████████████████████████] 46s (100.0%) LLM | 0s Tools
Judge 13               : [███████████████████████████████████████░] 43s (97.7%) LLM | 1s Tools
Judge 14               : [███████████████████████████████████████░] 57s (98.3%) LLM | 1s Tools
Judge 15               : [██████████████████████████████████████░░] 40s (95.2%) LLM | 2s Tools
Judge 16               : [███████████████████████████████████████░] 48s (98.0%) LLM | 1s Tools
Judge 17               : [████████████████████████████████████████] 45s (100.0%) LLM | 0s Tools
Judge 18               : [███████████████████████████████████████░] 58s (98.3%) LLM | 1s Tools
========================================================================================
```

---

## 8. Métricas Deterministas de Latencia por Etapa

| Etapa del Pipeline | Agentes / Shards | Tiempo de Pared (s) | Detalle Determinista |
| :--- | :---: | :---: | :--- |
| **Stage 1B: CTA Architects** | `1` | `615.0s` | Mappers max: `0.0s`, Harmonizer: `615.0s` |
| **Stage 3: Shard Authors** | `16` | `510.0s` | Min: `198.0s`, Mediana: `311.0s`, Straggler: `Shard Author shard_14` (`+199.0s`) |
| **Stage 3B: Repair Engineers** | `26` | `358.0s` | Min: `62.0s`, Mediana: `100.0s`, Straggler / Slowest: `Repair Engineer (H02)` |
| **Stage 5: Blind Judges** | `18` | `59.0s` | Lote: `216` ítems, 1er intento: `False`, Auto-repair: `0` |
| **Orquestador Principal** | `1` | `8177.0s` | CLI: `318.0s`, Barrera: `58.0s`, Intervenciones: `7` (`65.0s`) |

---

## 9. Taxonomía Consolidada de Errores y Retrabajo

| Categoría de Error | Ocurrencias | Agentes Afectados | Causa Raíz Técnica y Ejemplo |
| :--- | :---: | :--- | :--- |
| **Missing File / Relative Path / Directory Error (FileNotFoundError)** | **33** | Author Shard 01, Author Shard 02, Author Shard 03 | Encountered error in step execution: declaring permissions: cortex tool view_file: convert |
| **Shard Compilation & Template Validator Failure (compile_shard / check_templates)** | **10** | Author Shard 02, Author Shard 03, Author Shard 04 | Command exited with code 1. / Command output: / [-] FAIL: 6 errores detectados (6 errores  |
| **Anti-Giveaway & Psychometric Parity Violations (R-14..R-19)** | **9** | Author Shard 01, Author Shard 08, Author Shard 09 | Command exited with code 1. / Command output: / ERROR: Publish Quality Gate Rejected Publi |
| **Parameter Diversity & Option Collapse (TPL-VAR / TPL-COLLAPSE)** | **4** | Author Shard 05, Author Shard 11, Author Shard 14 | Command exited with code 1. / Command output: / [-] [TPL-DRY: FALLO EN EJECUCI�N DRY-RUN]  |
| **Non-Zero CLI Exit / Subprocess Probe (Exit Code 1)** | **2** | Orchestrator | Encountered error in step execution: declaring permissions: failed to parse path: courses/ |
| **File Edit / Write Tool Target Mismatch (replace_file_content / Overwrite)** | **2** | Author Shard 08, Orchestrator | Encountered error in step execution: target content not found in the file; the Target must |
| **LaTeX Control Character / Raw-String Corruption (R-03 / SyntaxWarning)** | **2** | Author Shard 10, Author Shard 16 | Command exited with code 1. / Command output: / D:\Augusto\personal_portfolio\Tops_academy |
| **Stage Contract / Pipeline Loader Mismatch (run.py / judge.py)** | **1** | Orchestrator | Command exited with code 1. / Command output: / ========================================== |
| **Python Environment / Virtualenv / Encoding Discrepancy** | **1** | Orchestrator | Command exited with code 1. / Command output: / Traceback (most recent call last): / File  |
| **Token Limit Cutoff (Model Truncation)** | **1** | Repair Engineer H-04 (ed8f06) | — |

---

## 10. Paquete Forense Agéntico Completo (Argon QA + Clúster Flash)

Todos los artefactos originales individuales generados por los auditores especializados se preservan íntegros en [`reports/audits_archive/estadistica_3_s9_vdirect5/`](file:///D:/Augusto/personal_portfolio/Tops_academy/reports/audits_archive/estadistica_3_s9_vdirect5/):

- **Auditoría Cualitativa Profunda de Calidad (Gemini 4 Argon):** [`qa_report.md`](file:///D:/Augusto/personal_portfolio/Tops_academy/reports/audits_archive/estadistica_3_s9_vdirect5/qa_report.md) | [`qa_report.json`](file:///D:/Augusto/personal_portfolio/Tops_academy/reports/audits_archive/estadistica_3_s9_vdirect5/qa_report.json)
- **Informe Maestro Agéntico del Pipeline (Gemini Flash Lead + 3 Subagentes):** [`agentic_pipeline_audit.md`](file:///D:/Augusto/personal_portfolio/Tops_academy/reports/audits_archive/estadistica_3_s9_vdirect5/agentic_pipeline_audit.md)
- **Sub-Auditorías del Clúster Agéntico (`agentic_batches/`):** [`agentic_batches/`](file:///D:/Augusto/personal_portfolio/Tops_academy/reports/audits_archive/estadistica_3_s9_vdirect5/agentic_batches/)
- **Dashboard Visual Interactivo:** [`dashboard.html`](file:///D:/Augusto/personal_portfolio/Tops_academy/reports/audits_archive/estadistica_3_s9_vdirect5/dashboard.html)
- **Índice Completo del Archivo Persistente:** [`README.md`](file:///D:/Augusto/personal_portfolio/Tops_academy/reports/audits_archive/estadistica_3_s9_vdirect5/README.md)
