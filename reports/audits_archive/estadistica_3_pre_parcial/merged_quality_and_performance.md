# Reporte Unificado de Auditoría Determinista: Calidad Estática y Telemetría Multi-Agente
## Curso: Estadistica 3 Pre Parcial (`estadistica_3_pre_parcial`)
### Plataforma Top's Academy — Pipeline Content-to-Course (C2C) v3.2

---

**Fecha de Consolidación:** 26 de Octubre de 2026  
**Identificador del Curso:** `estadistica_3_pre_parcial`  
**Conversación Orquestadora Auditada:** [`821334d0-216d-40c5-8920-dca90c0f0b26`](conversation://821334d0-216d-40c5-8920-dca90c0f0b26)  
**Calificación / Risk Score:** **16.8 / 20.0 (ACEPTABLE (14.0 - 16.9 pts))**  
**Tiempo de Pared Global:** **26.92 minutos** | **Cómputo Total de Agentes:** **440.72 minutos** | **Speedup:** **16.37x**  

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
| **Total de Competencias** | **93** | Distribución: Fact: 24, Concept: 36, Skill: 33 |
| **Banco Total de Reactivos** | **2190 preguntas** | Rango por comp.: 20..30 |
| **Competencias Subpobladas (< 3 preg.)** | **0** | Nodos raíz sin prerrequisitos: 13 |
| **Preguntas Huérfanas** | **0** | Reactivos sin `competency_id` válido |
| **Cobertura de Rationales de Error** | **100.0%** | 13140 / 13140 distractores con `error_rationale` |
| **Distractores Delatores (Telltale)** | **0 items** | Confesiones de error en texto visible |
| **Andamiaje Socrático (Hints)** | **0 sin pistas** | 0 reactivos con `< 3` pistas; 0 sin solución |
| **Incidencias de Sintaxis KaTeX** | **0 incidencias** | Llaves sin cerrar: 0, `$` impares: 0, `$$$`: 0 |
| **Residuos de Código / F-strings** | **0 incidencias** | F-strings: 0, Vars plantilla: 0, `{{}}`: 0 |
| **Sustituciones Ciegas bajo Operador** | **0 incidencias** | Patrón `\dot{num}` / `\ddot{num}` |
| **Penalizaciones Duras Precalculadas** | **-0.0 puntos** | 0 reglas de deducción activadas |
| **Risk Score Global (0.0 - 100.0)** | **15.48** | 678 issues totales detectados por linters |

---

## 2. Resultados por Linter y Dimensión

| Dimensión de la Rúbrica | Puntaje Obtenido | Máximo Posible | Observación Registrada |
| :--- | :---: | :---: | :--- |
| **Dimensión 1: Arquitectura y Granularidad** | **4.0** | 4.0 | Sobresaliente arquitectura curricular con 93 micro-competencias atómicas perfectamente delimitadas y balance cognitivo homogéneo entre Hechos (24, 25.8%), Conceptos (36, 38.7%) y Habilidades (33, 35.5%). Cada competencia cuenta con exactamente entre 20 (Hechos y Conceptos) y 30 reactivos (Habilidades), totalizando 2,190 preguntas sin ninguna competencia subpoblada. El análisis semántico del grafo DAG confirmó que las 13 competencias basales con dependencias vacías corresponden a los puntos de entrada legítimos (nodos raíz) de los módulos temáticos de econometría, articulando rutas de aprendizaje sólidas y coherentes. |
| **Dimensión 2: Calidad de Evaluación y Reactivos** | **3.2** | 5.0 | Excepcional cobertura diagnóstica con 100.0% de error_rationales pedagógicos en los 13,140 distractores evaluados (6 distractores por ítem en 2,190 reactivos MC7), capturando errores teóricos auténticos (desigualdad de Jensen en errores estándar, confusión de grados de libertad, inversión de matrices no conmutativas, etc.). Cero fugas de respuesta (Answer Leaks) y cero distractores delatores. Sin embargo, se aplica una deducción de -1.5 pts por presencia de Phantom Keying en la competencia Hab-11 (reactivos Q-Hab11-721 y Q-Hab11-722), donde distractores clonan la respuesta correcta anteponiendo prefijos sintéticos ('Opción alterna 5:', 'Opción alterna 6:'), y una deducción menor de -0.3 pts por monocultivo del formato de opción múltiple de 7 alternativas sin inclusión de ítems multimodales (MS o FIB). |
| **Dimensión 3: Andamiaje y Feedback Progresivo** | **3.8** | 5.0 | El 98.54% del curso (2,158 reactivos) cuenta con andamiaje socrático progresivo de 3 niveles en prosa fluida y rigurosa (Conceptual -> Procedimental -> Consistencia dimensional), y el 100% de los reactivos posee soluciones detalladas completas. No obstante, se detectó un cluster aislado de 32 reactivos (1.46%) en las competencias Hab-06, Hab-08, Hab-19 y Hab-20 con pistas deficientes tipo palabras clave aisladas o stub keywords (e.g. ['Mco', 'Insesgadez', 'Gauss-markov'], ['Arch', 'Heterocedasticidad']). Conforme a la rúbrica normativa, se aplica una deducción estipulada de -1.2 pts por pistas deficientes aisladas. |
| **Dimensión 4: Alineación Instruccional** | **4.0** | 4.0 | Alineación instruccional impecable (4.0/4.0). Congruencia semántica absoluta entre el título del curso, las descripciones de las 93 micro-competencias y los reactivos asociados. Cero preguntas huérfanas, sin contaminación cruzada inter-dominio y con riguroso énfasis en niveles taxonómicos superiores de Bloom (Aplicación empírica en Habilidades y Análisis deductivo en Conceptos). |
| **Dimensión 5: Accesibilidad y Ergonomía Técnica / KaTeX** | **1.8** | 2.0 | Sintaxis KaTeX completamente limpia y compilable al 100%: cero delimitadores desbalanceados, cero triples delimitadores y notación matemática formal preservada. El Loop de Verificación Semántica demostró que el 100% de las 464 advertencias de variables no interpoladas fueron falsos positivos del linter estático sobre entornos canónicos de matrices KaTeX (\begin{pmatrix}), subíndices econométricos estándar (_{BP}, _{LB}, _{MCO}, _{White}), macros de texto (\text{Tol}, \text{FIV}) y acentos matemáticos (\hat{u}, \bar{X}, \bar{Y}). Deducción menor (-0.2 pts) por ligera redundancia tipográfica en cláusulas de cierre de ciertos distractores numéricos. |
| **Total Consolidado** | **16.8** | **20.0** | **ACEPTABLE (14.0 - 16.9 pts)** |

---

## 3. Clusters de Riesgo e Incidencias Detectadas

| Cluster de Riesgo | Ítems Afectados | Muestra de IDs |
| :--- | :---: | :--- |
| **`katex_issues`** | **464** | `Q-C05-276`, `Q-C05-277`, `Q-C05-278`, `Q-C05-279`, `Q-C05-280`, `Q-H04-301`, `Q-H04-302`, `Q-H04-303` |
| **`telltale_distractors`** | **0** | — |
| **`fstring_residues`** | **0** | — |
| **`scaffolding_flaws`** | **32** | `Q-Hab06-371`, `Q-Hab06-372`, `Q-Hab06-373`, `Q-Hab06-374`, `Q-Hab06-375`, `Q-Hab06-376`, `Q-Hab06-377`, `Q-Hab06-378` |
| **`template_residues`** | **0** | — |
| **`blind_replacements`** | **0** | — |
| **`cloned_distractors`** | **0** | — |
| **`archetype_monotony`** | **0** | — |

---

## 4. Muestra de Control Estratificada

Ítems extraídos determinísticamente por competencia (`prepare_course_payload.py`):

1. **`Q-H01-001` (Especificación Estándar del Modelo de Regresión Lineal Simple | `multiple_choice_7_options` | `hints=3`):** `Analice la formulación operativa y deduzca: En una investigación con $n = 241$ observaciones, se plantea la regresión li...`
2. **`Q-H01-002` (Especificación Estándar del Modelo de Regresión Lineal Simple | `multiple_choice_7_options` | `hints=3`):** `Verifique la consistencia del modelo y obtenga: En una investigación con $n = 660$ observaciones, se plantea la regresió...`
3. **`Q-C01-021` (Formulación Matricial y Conformabilidad Dimensional del Modelo Lineal | `multiple_choice_7_options` | `hints=3`):** `Verifique la consistencia del modelo y obtenga: En una regresión lineal múltiple con $n = 64$ observaciones y $k = 2$ re...`
4. **`Q-C01-022` (Formulación Matricial y Conformabilidad Dimensional del Modelo Lineal | `multiple_choice_7_options` | `hints=3`):** `Procediendo conforme al marco teórico correspondiente, deduzca: En una regresión lineal múltiple con $n = 291$ observaci...`
5. **`Q-Hab01-041` (Derivación Escalar de los Estimadores MCO | `multiple_choice_7_options` | `hints=3`):** `Aplicando las identidades teóricas pertinentes, evalúe: A partir de una muestra de $n = 34$ observaciones con $\bar{x} =...`
6. **`Q-Hab01-042` (Derivación Escalar de los Estimadores MCO | `multiple_choice_7_options` | `hints=3`):** `Al examinar detenidamente las condiciones de frontera, resuelva: A partir de una muestra de $n = 31$ observaciones con $...`
7. **`Q-Hab02-071` (Derivación Matricial de Estimadores MCO y Ecuaciones Normales | `multiple_choice_7_options` | `hints=3`):** `Considere el siguiente planteamiento formal: En el modelo lineal general $y = X\beta + u$ con matriz $X$ ($161 \times 3$...`
8. **`Q-Hab02-072` (Derivación Matricial de Estimadores MCO y Ecuaciones Normales | `multiple_choice_7_options` | `hints=3`):** `A partir de las condiciones analíticas dadas, determine: En el modelo lineal general $y = X\beta + u$ con matriz $X$ ($2...`
9. **`Q-H02-101` (Varianza de Estimadores MCO y Estimación de la Varianza del Error | `multiple_choice_7_options` | `hints=3`):** `Al examinar detenidamente las condiciones de frontera, resuelva: En un modelo de regresión lineal múltiple con $n = 56$ ...`
10. **`Q-H02-102` (Varianza de Estimadores MCO y Estimación de la Varianza del Error | `multiple_choice_7_options` | `hints=3`):** `Con arreglo a las definiciones operativas del sistema, verifique: En un modelo de regresión lineal múltiple con $n = 142...`

---

## 5. Reglas de Linting Registradas (`discovered_lint_rules`)

* **ID de Regla:** `exclude_latex_matrix_and_text_from_template_linter`
* **Severidad:** info
* **Patrón Regex:** `N/A`
* **Descripción:** 
* **ID de Regla:** `exclude_econometric_subscripts_from_template_linter`
* **Severidad:** info
* **Patrón Regex:** `N/A`
* **Descripción:** 
* **ID de Regla:** `strip_synthetic_prefixes_before_cloned_distractor_check`
* **Severidad:** info
* **Patrón Regex:** `N/A`
* **Descripción:** 
---

# PARTE II: AUDITORÍA FORENSE DE RENDIMIENTO Y TELEMETRÍA (RUN AUDITOR)

## 6. Consolidación de Métricas de Rendimiento y Ratios Unitarios

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada (`pre_cta_manifest.json`)** | `8 archivos` (141 págs / 6.19 MB) | Ingesta directa PDF Zero-Waste (v3.2) |
| **Competencias Extraídas (`cta.json`)** | **`93 competencias`** | Compiladas desde tuplas posicionales (`compile_cta.py`) |
| **Shards Particionados (`pre_shard_manifest.json`)** | **`63 shards`** | Compilados vía `compile_shard.py` |
| **Subagentes Desplegados ($M$ CTA, $N$ Shards, $K$ Judges)** | **`87 subagentes`** | Fan-out dinámico coordinado por orquestador |
| **Reactivos Finales Validados** | **`2190 preguntas`** | Evaluadas en sandbox in-process |
| **Tokens Entrada (Subagentes)** | **`8,884,815 tokens`** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`3,176,541 tokens`** | Código de tuplas Python y JSON generado |
| **Tokens Caché (Leídos)** | **`38,536,687 tokens`** | Caché de contexto reutilizado por la API |
| **Trazas de Pensamiento (`thinking_traces`)** | **`584 turnos` (2,322,607 chars)** | Razonamiento interno extraído de `transcript.jsonl` / `transcript_full.jsonl` |
| **Gran Total Tokens Activos** | **`12,061,356 tokens`** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`50,598,043 tokens`** | Consumo total de cuota facturable |
| **Tiempo de Pared Total** | **`1615.0 s` (26.92 min)** | Tiempo transcurrido de principio a fin |
| **Tiempo Cómputo Acumulado** | **`26443.0 s` (440.72 min)** | Suma escalar de tiempos de todos los agentes |
| **Factor de Aceleración Paralela** | **`16.37x`** | Relación tiempo cómputo vs tiempo de pared |
| **Tokens Totales por Pregunta** | **`23,104.1 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`5,507.5 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`544,065.0 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`100,067.3 tokens/comp`** | Costo puro de la etapa de autoría |
| **Segundos de Pared por Pregunta** | **`0.74 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`81.36 preg/min`** | Velocidad de producción del pipeline |

---

## 7. Distribución Empírica del Tiempo: Inferencia LLM vs. Ejecución de Herramientas

- **Porcentaje Promedio en Inferencia LLM:** `95.8%`
- **Porcentaje Promedio en Ejecución Local de Herramientas:** `4.2%`

```
========================================================================================
DISTRIBUCIÓN DEL TIEMPO DE PARED POR SUBAGENTE (INFERENCIA LLM vs TOOLS)
========================================================================================
Direct CTA Architect   : [░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 0s (0.0%) LLM | 0s Tools
Author Shard 01        : [██████████████████████████████████░░░░░░] 234s (87.0%) LLM | 23s Tools
Author Shard 02        : [██████████████████████████████████████░░] 296s (95.5%) LLM | 8s Tools
Author Shard 03        : [███████████████████████████████████░░░░░] 222s (88.1%) LLM | 23s Tools
Author Shard 04        : [████████████████████████████████████░░░░] 229s (90.9%) LLM | 16s Tools
Author Shard 05        : [████████████████████████████████████░░░░] 316s (91.6%) LLM | 19s Tools
Author Shard 06        : [██████████████████████████████████████░░] 334s (96.0%) LLM | 12s Tools
Author Shard 07        : [████████████████████████████████████░░░░] 252s (92.3%) LLM | 16s Tools
Author Shard 08        : [█████████████████████████████████░░░░░░░] 290s (83.6%) LLM | 36s Tools
Author Shard 09        : [███████████████████████████████████████░] 281s (97.6%) LLM | 7s Tools
Author Shard 10        : [██████████████████████████████████████░░] 255s (95.5%) LLM | 12s Tools
Author Shard 11        : [███████████████████████████████░░░░░░░░░] 206s (78.3%) LLM | 28s Tools
Author Shard 12        : [██████████████████████████████████░░░░░░] 259s (87.2%) LLM | 19s Tools
Author Shard 13        : [███████████████████████████████████░░░░░] 218s (88.6%) LLM | 22s Tools
Author Shard 14        : [████████████████████████████████████░░░░] 325s (91.5%) LLM | 16s Tools
Author Shard 15        : [████████████████████████████████████░░░░] 234s (91.4%) LLM | 16s Tools
Author Shard 16        : [██████████████████████████████████████░░] 278s (96.9%) LLM | 9s Tools
Author Shard 17        : [██████████████████████████████████████░░] 331s (96.2%) LLM | 13s Tools
Author Shard 18        : [████████████████████████████████████░░░░] 423s (91.0%) LLM | 31s Tools
Author Shard 19        : [█████████████████████████████████░░░░░░░] 298s (83.7%) LLM | 36s Tools
Author Shard 20        : [█████████████████████████████████████░░░] 209s (94.6%) LLM | 11s Tools
Author Shard 21        : [█████████████████████████████████████░░░] 272s (93.2%) LLM | 14s Tools
Author Shard 22        : [█████████████████████████████████████░░░] 276s (93.2%) LLM | 15s Tools
Author Shard 23        : [███████████████████████████████░░░░░░░░░] 225s (78.4%) LLM | 35s Tools
Author Shard 24        : [████████████████████████████████████░░░░] 209s (92.1%) LLM | 17s Tools
Author Shard 25        : [████████████████████████████████░░░░░░░░] 212s (80.0%) LLM | 28s Tools
Author Shard 26        : [███████████████████████████████░░░░░░░░░] 222s (78.7%) LLM | 28s Tools
Author Shard 27        : [█████████████████████████████████████░░░] 237s (93.3%) LLM | 16s Tools
Author Shard 28        : [█████████████████████████████████░░░░░░░] 296s (82.7%) LLM | 37s Tools
Author Shard 29        : [████████████████████████████████████░░░░] 239s (92.3%) LLM | 14s Tools
Author Shard 30        : [██████████████████████████████████████░░] 348s (96.1%) LLM | 9s Tools
Author Shard 31        : [█████████████████████████████████████░░░] 541s (94.3%) LLM | 20s Tools
Author Shard 32        : [█████████████████████████████████░░░░░░░] 315s (84.5%) LLM | 37s Tools
Author Shard 33        : [████████████████████████████████████░░░░] 222s (91.7%) LLM | 14s Tools
Author Shard 34        : [████████████████████████████████████░░░░] 262s (90.0%) LLM | 19s Tools
Author Shard 35        : [█████████████████████████████████░░░░░░░] 295s (84.0%) LLM | 33s Tools
Author Shard 36        : [█████████████████████████████████░░░░░░░] 325s (84.4%) LLM | 30s Tools
Author Shard 37        : [██████████████████████████████████████░░] 244s (96.1%) LLM | 9s Tools
Author Shard 38        : [████████████████████████████████████░░░░] 323s (92.0%) LLM | 21s Tools
Author Shard 39        : [█████████████████████████████████████░░░] 259s (94.5%) LLM | 15s Tools
Author Shard 40        : [█████████████████████████████████████░░░] 330s (94.8%) LLM | 16s Tools
Author Shard 41        : [██████████████████████████████████████░░] 256s (95.2%) LLM | 12s Tools
Author Shard 42        : [█████████████████████████████████████░░░] 430s (92.7%) LLM | 22s Tools
Author Shard 43        : [██████████████████████████████████████░░] 270s (95.1%) LLM | 14s Tools
Author Shard 44        : [████████████████████████████████████░░░░] 263s (92.3%) LLM | 16s Tools
Author Shard 45        : [█████████████████████████████████████░░░] 303s (92.9%) LLM | 23s Tools
Author Shard 46        : [█████████████████████████████████████░░░] 395s (94.7%) LLM | 20s Tools
Author Shard 47        : [██████████████████████████████████░░░░░░] 223s (85.8%) LLM | 24s Tools
Author Shard 48        : [██████████████████████████████████████░░] 347s (95.9%) LLM | 15s Tools
Author Shard 49        : [█████████████████████████████████████░░░] 290s (93.5%) LLM | 17s Tools
Author Shard 50        : [█████████████████████████████████░░░░░░░] 311s (84.3%) LLM | 33s Tools
Author Shard 51        : [█████████████████████████████████████░░░] 299s (93.7%) LLM | 18s Tools
Author Shard 52        : [█████████████████████████████████████░░░] 342s (93.4%) LLM | 18s Tools
Author Shard 53        : [███████████████████████████████████░░░░░] 347s (88.7%) LLM | 31s Tools
Author Shard 54        : [█████████████████████████████████████░░░] 565s (94.3%) LLM | 27s Tools
Author Shard 55        : [████████████████████████████████████░░░░] 336s (90.1%) LLM | 26s Tools
Author Shard 56        : [█████████████████████████████████████░░░] 408s (94.2%) LLM | 23s Tools
Author Shard 57        : [████████████████████████████████████░░░░] 332s (91.2%) LLM | 19s Tools
Author Shard 58        : [████████████████████████████████████░░░░] 224s (90.3%) LLM | 19s Tools
Author Shard 59        : [████████████████████████████████████░░░░] 293s (91.3%) LLM | 16s Tools
Author Shard 60        : [███████████████████████████████████████░] 363s (97.8%) LLM | 8s Tools
Author Shard 61        : [██████████████████████████████████████░░] 462s (96.9%) LLM | 15s Tools
Author Shard 62        : [████████████████████████████████████░░░░] 263s (90.1%) LLM | 18s Tools
Author Shard 63        : [██████████████████████████████████░░░░░░] 247s (86.4%) LLM | 29s Tools
Judge 01               : [███████████████████████████████████████░] 73s (98.6%) LLM | 1s Tools
Judge 02               : [████████████████████████████████████████] 82s (100.0%) LLM | 0s Tools
Judge 03               : [████████████████████████████████████████] 161s (100.0%) LLM | 0s Tools
Judge 04               : [███████████████████████████████████████░] 94s (98.9%) LLM | 1s Tools
Judge 05               : [███████████████████████████████████████░] 92s (98.9%) LLM | 1s Tools
Judge 06               : [████████████████████████████████████████] 84s (100.0%) LLM | 0s Tools
Judge 07               : [███████████████████████████████████████░] 83s (97.6%) LLM | 2s Tools
Judge 08               : [████████████████████████████████████████] 60s (100.0%) LLM | 0s Tools
Judge 09               : [███████████████████████████████████████░] 70s (98.6%) LLM | 1s Tools
Judge 10               : [████████████████████████████████████████] 133s (100.0%) LLM | 0s Tools
Judge 11               : [████████████████████████████████████████] 94s (100.0%) LLM | 0s Tools
Judge 12               : [████████████████████████████████████████] 92s (100.0%) LLM | 0s Tools
Judge 13               : [███████████████████████████████████████░] 169s (99.4%) LLM | 1s Tools
Judge 14               : [████████████████████████████████████████] 141s (100.0%) LLM | 0s Tools
Judge 15               : [████████████████████████████████████████] 78s (100.0%) LLM | 0s Tools
Judge 16               : [████████████████████████████████████████] 61s (100.0%) LLM | 0s Tools
========================================================================================
```

---

## 8. Métricas Deterministas de Latencia por Etapa

| Etapa del Pipeline | Agentes / Shards | Tiempo de Pared (s) | Detalle Determinista |
| :--- | :---: | :---: | :--- |
| **Stage 1B: CTA Architects** | `8` | `445.0s` | Mappers max: `445.0s`, Harmonizer: `0.0s` |
| **Stage 3: Shard Authors** | `63` | `599.0s` | Min: `221.0s`, Mediana: `310.0s`, Straggler: `Shard Author shard_54` (`+289.0s`) |
| **Stage 5: Blind Judges** | `16` | `170.0s` | Lote: `186` ítems, 1er intento: `True`, Auto-repair: `2` |
| **Orquestador Principal** | `1` | `1615.0s` | CLI: `66.0s`, Barrera: `44.0s`, Intervenciones: `0` (`0.0s`) |

---

## 9. Taxonomía Consolidada de Errores y Retrabajo

| Categoría de Error | Ocurrencias | Agentes Afectados | Causa Raíz Técnica y Ejemplo |
| :--- | :---: | :--- | :--- |
| **Token Limit Cutoff (Model Truncation)** | **202** | Author Shard 01, Author Shard 02, Author Shard 03 | — |
| **Missing File / Relative Path / Directory Error (FileNotFoundError)** | **173** | Author Shard 01, Author Shard 02, Author Shard 03 | Encountered error in step execution: declaring permissions: cortex tool view_file: convert |
| **Anti-Giveaway & Psychometric Parity Violations (R-14..R-19)** | **20** | Author Shard 01, Author Shard 06, Author Shard 09 | Encountered error in step execution: tool call denied by pre-tool hook: C2C Cross-Course I |
| **Parameter Diversity & Option Collapse (TPL-VAR / TPL-COLLAPSE)** | **7** | Author Shard 10, Author Shard 18, Author Shard 42 | The command exited with code 1. / Output: / [-] FAIL: 2 errores detectados (2 errores cons |
| **Shard Compilation & Template Validator Failure (compile_shard / check_templates)** | **3** | Author Shard 18, Author Shard 52, Author Shard 53 | The command exited with code 1. / Output: / [-] FAIL: 4 errores detectados (4 errores cons |
| **PowerShell Command / Quoting / $Variable Expansion Friction** | **2** | Author Shard 38, Author Shard 48 | The command exited with code 1. / Output: / Select-String : La cadena " shard_id\: \shard_ |
| **CTA Compilation & Schema Errors (CTA-SCHEMA / CTA-EV / DAG Cycle)** | **1** | CTA Architect (part_07) | Encountered error in step execution: tool call denied by pre-tool hook: C2C Worker Boundar |
| **File Edit / Write Tool Target Mismatch (replace_file_content / Overwrite)** | **1** | Author Shard 54 | Encountered error in step execution: target content not found in the file; the Target must |
| **Non-Zero CLI Exit / Subprocess Probe (Exit Code 1)** | **1** | Author Shard 54 | Encountered error in step execution: tool call denied by pre-tool hook: BLOCKER:: El shard |
| **Cross-check Verification False (TPL-CROSS)** | **1** | Author Shard 56 | The command exited with code 1. / Output: / [-] [TPL-DRY: FALLO EN EJECUCI�N DRY-RUN] / Co |
