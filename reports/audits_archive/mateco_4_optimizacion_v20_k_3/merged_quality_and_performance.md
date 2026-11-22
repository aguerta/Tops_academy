# Reporte Unificado de Auditoría Determinista: Calidad Estática y Telemetría Multi-Agente
## Curso: Mateco 4 Optimizacion V20 K 3 (`mateco_4_optimizacion_v20_k_3`)
### Plataforma Top's Academy — Pipeline Content-to-Course (C2C) v3.2

---

**Fecha de Consolidación:** 21 de Noviembre de 2026  
**Identificador del Curso:** `mateco_4_optimizacion_v20_k_3`  
**Conversación Orquestadora Auditada:** [`d65b2d48-4e52-480c-83a0-78d3055cc411`](conversation://d65b2d48-4e52-480c-83a0-78d3055cc411)  
**Calificación QM-OSCQR / Risk Score:** **19.92 / 20.0 (EXCELENTE (19.0 - 20.0 pts) — PLATINUM MASTERY)**  
**Mastery Path Readiness Index (`MPRI`):** **`99.65 / 100.0` (GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo)**  
**Índice Bloom Ponderado (1–5):** **3.93 / 5.0** (piso `3.89` | `Analyze+Evaluate`: `73.5%` | Tier: **ÉLITE**)  
**Tiempo de Pared Global:** **23.45 minutos** | **Cómputo Total de Agentes:** **124.83 minutos** | **Speedup:** **5.32x**  
**Costo Estimado Total (Gemini 4 Hydrogen):** **`$16.2156 USD`** (`$0.0168 USD/preg` | In: `$6.0182`, Out+Think: `$9.0421`, Cache: `$1.1552`)  

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
| **Total de Competencias** | **27** | Distribución: Fact: 1, Concept: 12, Skill: 14 |
| **Banco Total de Reactivos** | **963 preguntas** | Rango por comp.: 27..48 |
| **Competencias Subpobladas (< 3 preg.)** | **0** | Nodos raíz sin prerrequisitos: 1 |
| **Preguntas Huérfanas** | **0** | Reactivos sin `competency_id` válido |
| **Cobertura de Rationales de Error** | **100.0%** | 264 / 264 distractores con `error_rationale` |
| **Distractores Delatores (Telltale)** | **0 items** | Confesiones de error en texto visible |
| **Andamiaje Socrático (Hints)** | **0 sin pistas** | 0 reactivos con `< 3` pistas; 0 sin solución |
| **Incidencias de Sintaxis KaTeX** | **0 incidencias** | Llaves sin cerrar: 0, `$` impares: 0, `$$$`: 0 |
| **Residuos de Código / F-strings** | **0 incidencias** | F-strings: 0, Vars plantilla: 0, `{{}}`: 0 |
| **Sustituciones Ciegas bajo Operador** | **0 incidencias** | Patrón `\dot{num}` / `\ddot{num}` |
| **Penalizaciones Duras Precalculadas** | **-0.0 puntos** | 0 reglas de deducción activadas |
| **Risk Score Global (0.0 - 100.0)** | **0.05** | 1 issues totales detectados por linters |
| **Mastery Path Readiness (`MPRI`)** | **`99.65 / 100.0`** | GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo |
| **Índice Bloom Ponderado (1–5)** | **3.93 / 5.0** | Piso adaptativo `3.89`, `Analyze+Evaluate`: `73.5%`, incoherencias: `0`, Tier: **ÉLITE** |

---

## 1B. Auditoría de Camino al Dominio (`Path-to-Mastery v2.0` — 6 Pilares Cognitivos)

| Pilar de Dominio del Estudiante | Puntaje MPRI | Máximo | Diagnóstico Empírico Determinista |
| :--- | :---: | :---: | :--- |
| **1. Progresión Adaptativa ZPD y Bloom** | **20.0** | 20.0 | Competencias con ZPD colapsado (1 sola banda): `0/27`; Habilidades en Bloom `Apply+`: `100.0%`; Índice Bloom: `3.93/5.0` (piso `3.89`, Tier `ÉLITE`) |
| **2. Modalidad de Evocación y Anti-Gaming** | **20.0** | 20.0 | `MC7=0.0%`, `FIB=13.4%`, `MS=13.4%`; Comps memorizables: `0`; Cuantif. vacuos: `0`; Relleno `[R-15]`: `0` |
| **3. Integridad del Salvavidas Socrático (3-Strikes)** | **25.0** | 25.0 | Pistas genuinas: `100.0%`; Boilerplate Mad-Libs: `0.0%`; Pistas envenenadas: `0` (`0.0%`) |
| **4. Alineación Diagnóstica en `FeedbackToast`** | **15.0** | 15.0 | Unicidad global de `error_rationale`: `100.0%` (`62/264`); Distractores `1.333x` arbitrarios: `0` |
| **5. Topología DAG e Interleaving (Quiz/Test)** | **9.65** | 10.0 | Ciclos: `False`, Profundidad DAG: `6`, Aristas invertidas: `0`, Islas: `0` |
| **6. Ergonomía Cognitiva y Pureza de Encuadre** | **10.0** | 10.0 | Prosa en `\text{...}`: `0`, Vars crudas `$theta_hat$`: `0`, Prefijos Solow/EDP ajenos: `0` |

---

## 2. Resultados por Linter y Dimensión

| Dimensión de la Rúbrica | Puntaje Obtenido | Máximo Posible | Observación Registrada |
| :--- | :---: | :---: | :--- |
| **Dimensión 1: Arquitectura y Granularidad** | **3.92** | 4.0 | Estructura curricular depurada con 27 competencias (1 Hechos, 12 Conceptos, 14 Habilidades) y densidad k=3 exacta (27, 36 o 48 ítems/comp). DAG acíclico y conexo con raíz única C-01 (ciclos=False, comp. conexos=1, alerta léxica benigna C-07<->C-14 entre Cálculo de Variaciones y Control Óptimo). ZPD: 27/27 competencias con calibración tri-banda ('easy': 230, 'medium': 321, 'hard': 412). |
| **Dimensión 2: Calidad de Evaluación y Reactivos** | **5.0** | 5.0 | Modalidad: MC7=0.0%, FIB=13.4%, MS=13.4%, BloomSup=73.21% (100.0% evocación activa/discriminación bajo contrato M20). Distractores: 264 evaluados con 100.0% cobertura de error_rationale (imposibles por dominio=0, claves corruptas=0, sesgo MS=0.0%). Rigor matemático verificado en las 54 muestras estratificadas y 120/120 acuerdos Stage-5. |
| **Dimensión 3: Andamiaje y Feedback Progresivo** | **5.0** | 5.0 | Andamiaje formativo: 100.0% de reactivos con 3 pistas socráticas escalonadas y parametrizadas (100.0% pistas genuinas, 0.0% boilerplate Mad-Libs, 0.0% envenenadas, 0 colisiones tipográficas). Unicidad diagnóstica real de rationales: 100.0% (62/62 slots). Observación menor: residuo estático t_1=sqrt(60) en misconception_warning de Hab-04 e interpolación $a=a$ en rationale de C-02/C-03. |
| **Dimensión 4: Alineación Instruccional** | **4.0** | 4.0 | Alineación cognitiva de Bloom: 100.0% de habilidades prácticas (576/576) en Apply+; Índice Bloom ponderado: 3.931/5.0 superando el piso adaptativo 3.886 (superávit +0.045, 73.52% Analyze+Evaluate, tier: ÉLITE, incoherencias=0). Contaminación léxica previa de Hab-07/Hab-05 corregida. |
| **Dimensión 5: Accesibilidad y Ergonomía Técnica / KaTeX** | **2.0** | 2.0 | Sintaxis KaTeX: 0 errores críticos (delimitadores balanceados, llaves cerradas, cero $$$, cero SymPy crudo). Ergonomía: 0 observaciones de prosa en \text{...}, 0 identificadores crudos, 0 colisiones por concatenación, 0 identidades tautológicas detectadas por linter y 0 formatos flotantes/asteriscos crudos. |
| **Total Consolidado** | **19.92** | **20.0** | **EXCELENTE (19.0 - 20.0 pts) — PLATINUM MASTERY** |

---

## 3. Clusters de Riesgo e Incidencias Detectadas

| Cluster de Riesgo | Ítems Afectados | Muestra de IDs |
| :--- | :---: | :--- |
| **`katex_issues`** | **0** | — |
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
| **`domain_impossible_options`** | **0** | — |
| **`string_concat_collisions`** | **0** | — |
| **`disconnected_numeric_rationales`** | **0** | — |
| **`duplicate_competencies`** | **1** | `comp_C-14` |
| **`sympy_in_katex`** | **0** | — |
| **`phantom_numeric_rationale`** | **0** | — |
| **`bloom_alignment`** | **0** | — |
| **`ms_length_bias`** | **0** | — |

---

## 4. Muestra de Control Estratificada

Ítems extraídos determinísticamente por competencia (`prepare_course_payload.py`):

1. **`Q-C01-001` (Forma Funcional, Trayectorias Admisibles y Formulación Variacional | `invariant_canvas` | `hints=3`):** `En el plano $(t,y)$ sobre $[0,4]$, trace el extremo final $P_1$ de la trayectoria admisible $y(t)=2+2t$:...`
2. **`Q-C01-002` (Forma Funcional, Trayectorias Admisibles y Formulación Variacional | `invariant_canvas` | `hints=3`):** `Sea la trayectoria admisible $y(t)=4+3t$ en $[0,7]$ con $y(0)=4$. Ubique el punto terminal $P_1=(T,y(T))$:...`
3. **`Q-H01-037` (Tipos de Funcionales: Lagrange, Mayer y Bolza | `fill_in_the_blank` | `hints=3`):** `Para el problema de Mayer $V[y]=G(5,y(5))=6(5)+9y(5)$, sabiendo que $y(0)=8$ y $y(5)=12$, determine $V[y]$:...`
4. **`Q-H01-038` (Tipos de Funcionales: Lagrange, Mayer y Bolza | `fill_in_the_blank` | `hints=3`):** `Evalúe el funcional de Mayer $V[y]=2T+4y(T)$ en $T=12$ cuando la trayectoria satisface $y(0)=8$ y $y(12)=18$. Ingrese $V...`
5. **`Q-C02-064` (Ecuación de Euler (Primer Orden) | `proof_dag` | `hints=3`):** `Ordene la derivación de la ecuación de Euler para $J[x] = \int_{t_0}^{t_1} (3\dot{x}^2 + 8x^2)\,dt$ con extremos fijos:...`
6. **`Q-C02-065` (Ecuación de Euler (Primer Orden) | `proof_dag` | `hints=3`):** `Construya el grafo deductivo de la condición de primer orden de Euler sobre $F(x,\dot{x},t) = 8\dot{x}^2 + 11x^2$:...`
7. **`Q-C03-091` (Condición de Legendre (Segundo Orden) | `open_symbolic` | `hints=3`):** `Determine la expresión de $F_{\dot{x}\dot{x}}$ respecto a $t$ en el integrando $F(x,\dot{x},t) = (4t + 6)\dot{x}^2 - 4x^...`
8. **`Q-C03-092` (Condición de Legendre (Segundo Orden) | `open_symbolic` | `hints=3`):** `Para $F(x,\dot{x},t) = (3t + 5)\dot{x}^2 - 7x^2$, exprese simbólicamente $F_{\dot{x}\dot{x}}$ en función de $t$:...`
9. **`Q-C05-118` (Casos Particulares de la Ecuación de Euler | `proof_dag` | `hints=3`):** `Seleccione los pasos válidos que simplifican Euler dado que $F(\dot{x},t)=3\dot{x}^2+10t\dot{x}$ omite $x$:...`
10. **`Q-C05-119` (Casos Particulares de la Ecuación de Euler | `proof_dag` | `hints=3`):** `Construya el grafo deductivo para reducir la ecuación de Euler cuando $F(\dot{x},t)=6\dot{x}^2+2t\dot{x}$:...`

---

## 5. Reglas de Linting Registradas (`discovered_lint_rules`)

* **ID de Regla:** `R-TAUTOLOGICAL-PARAM-EQUALITY-IN-RATIONALE`
* **Severidad:** info
* **Patrón Regex:** `\$\b([0-9]+)\s*=\s*\1\b\$`
* **Descripción:** Detecta igualdades numéricas tautológicas del tipo '$3=3$' o '$4=4$' dentro de error_rationale producidas cuando tanto el nombre simbólico del parámetro como su valor fueron interpolados con el mismo número.
* **Ítems Evidencia:** Q-C02-064, Q-C02-065, Q-C03-091, Q-C03-092

---

# PARTE II: AUDITORÍA FORENSE DE RENDIMIENTO Y TELEMETRÍA (RUN AUDITOR)

## 6. Consolidación de Métricas de Rendimiento y Ratios Unitarios

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada (`pre_cta_manifest.json`)** | `6 archivos` (71 págs / 3.61 MB) | Ingesta directa PDF Zero-Waste (v3.2) |
| **Competencias Extraídas (`cta.json`)** | **`27 competencias`** | Compiladas desde tuplas posicionales (`compile_cta.py`) |
| **Shards Particionados (`pre_shard_manifest.json`)** | **`21 shards`** | Compilados vía `compile_shard.py` |
| **Subagentes Desplegados ($M$ CTA, $N$ Shards, $R$ Repairs, $K$ Judges)** | **`55 subagentes`** | Fan-out dinámico coordinado por orquestador (CTA: 8, Shards: 21, Repairs: 7, Judges: 19) |
| **Reactivos Finales Validados** | **`963 preguntas`** | Evaluadas en sandbox in-process |
| **Tokens Entrada (Subagentes)** | **`4,012,130 tokens`** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`1,205,620 tokens`** | Código de tuplas Python y JSON generado |
| **Tokens Caché (Leídos)** | **`15,403,257 tokens`** | Caché de contexto reutilizado por la API |
| **Trazas de Pensamiento (`thinking_traces`)** | **`129 turnos` (458,542 chars)** | Razonamiento interno extraído de `transcript.jsonl` / `transcript_full.jsonl` |
| **Gran Total Tokens Activos** | **`5,217,750 tokens`** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`20,621,007 tokens`** | Consumo total de cuota facturable |
| **Costo Estimado Total (Gemini 4 Hydrogen)** | **`$16.2156 USD`** | In: `$6.0182` (`$1.50/1M`), Out+Think: `$9.0421` (`$7.50/1M`), Cache: `$1.1552` (`$0.075/1M`) |
| **Tiempo de Pared Total** | **`1407.0 s` (23.45 min)** | Tiempo transcurrido de principio a fin |
| **Tiempo Cómputo Acumulado** | **`7490.0 s` (124.83 min)** | Suma escalar de tiempos de todos los agentes |
| **Factor de Aceleración Paralela** | **`5.32x`** | Relación tiempo cómputo vs tiempo de pared |
| **Tokens Totales por Pregunta** | **`21,413.3 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`5,418.2 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Costo Estimado por Pregunta (Hydrogen)** | **`$0.0168 USD/preg`** | Costo monetario por reactivo validado (`$0.6006 USD/comp`) |
| **Tokens por Competencia (Global)** | **`763,741.0 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`99,523.4 tokens/comp`** | Costo puro de la etapa de autoría |
| **Segundos de Pared por Pregunta** | **`1.46 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`41.07 preg/min`** | Velocidad de producción del pipeline |

---

## 7. Distribución Empírica del Tiempo: Inferencia LLM vs. Ejecución de Herramientas

- **Porcentaje Promedio en Inferencia LLM:** `95.8%`
- **Porcentaje Promedio en Ejecución Local de Herramientas:** `4.2%`

```
========================================================================================
DISTRIBUCIÓN DEL TIEMPO DE PARED POR SUBAGENTE (INFERENCIA LLM vs TOOLS)
========================================================================================
Direct CTA Architect   : [░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 0s (0.0%) LLM | 0s Tools
Author Shard 01        : [███████████████████████████████░░░░░░░░░] 168s (78.5%) LLM | 33s Tools
Author Shard 02        : [██████████████████████░░░░░░░░░░░░░░░░░░] 159s (57.2%) LLM | 45s Tools
Author Shard 03        : [████████████████████████████████░░░░░░░░] 103s (81.1%) LLM | 18s Tools
Author Shard 04        : [████████████████████████████████░░░░░░░░] 169s (80.9%) LLM | 27s Tools
Author Shard 05        : [███████████████████████░░░░░░░░░░░░░░░░░] 214s (58.2%) LLM | 63s Tools
Author Shard 06        : [████████████████████████░░░░░░░░░░░░░░░░] 121s (62.4%) LLM | 59s Tools
Author Shard 07        : [██████████████████████████░░░░░░░░░░░░░░] 113s (65.7%) LLM | 47s Tools
Author Shard 08        : [█████████████████████████████░░░░░░░░░░░] 134s (73.2%) LLM | 41s Tools
Author Shard 09        : [████████████████████████████████░░░░░░░░] 69s (81.2%) LLM | 15s Tools
Author Shard 10        : [█████████████████████████████░░░░░░░░░░░] 167s (72.9%) LLM | 56s Tools
Author Shard 11        : [██████████████████████████████░░░░░░░░░░] 120s (75.9%) LLM | 28s Tools
Author Shard 12        : [███████████████████████████████░░░░░░░░░] 141s (77.9%) LLM | 33s Tools
Author Shard 13        : [███████████████████████████████░░░░░░░░░] 139s (78.1%) LLM | 27s Tools
Author Shard 14        : [███████████████████████████░░░░░░░░░░░░░] 128s (68.8%) LLM | 31s Tools
Author Shard 15        : [████████████████████████░░░░░░░░░░░░░░░░] 168s (60.9%) LLM | 58s Tools
Author Shard 16        : [████████████████████████████░░░░░░░░░░░░] 229s (70.0%) LLM | 66s Tools
Author Shard 17        : [████████████████████████████████░░░░░░░░] 200s (81.3%) LLM | 28s Tools
Author Shard 18        : [██████████████████████████████░░░░░░░░░░] 238s (76.3%) LLM | 49s Tools
Author Shard 19        : [██████████████████████████████░░░░░░░░░░] 220s (76.9%) LLM | 49s Tools
Author Shard 20        : [███████████████████████████░░░░░░░░░░░░░] 131s (68.9%) LLM | 33s Tools
Author Shard 21        : [████████████████████████████████░░░░░░░░] 120s (80.5%) LLM | 25s Tools
Repair Engineer C-02 (3a171e): [███████████████████████░░░░░░░░░░░░░░░░░] 28s (59.6%) LLM | 17s Tools
Repair Engineer C-02 (c55ae3): [█████████████████████████░░░░░░░░░░░░░░░] 25s (64.1%) LLM | 12s Tools
Repair Engineer C-02 (e02e3f): [████████████████████████░░░░░░░░░░░░░░░░] 22s (61.1%) LLM | 13s Tools
Repair Engineer C-15 (ef0d11): [████████████████████████░░░░░░░░░░░░░░░░] 47s (60.3%) LLM | 29s Tools
Repair Engineer Hab-06 (920f85): [███████████████████████░░░░░░░░░░░░░░░░░] 23s (57.5%) LLM | 13s Tools
Repair Engineer Hab-10 (29fa5b): [█████████████████████████░░░░░░░░░░░░░░░] 26s (63.4%) LLM | 13s Tools
Repair Engineer Hab-20 (9f7374): [████████████████████████░░░░░░░░░░░░░░░░] 26s (61.9%) LLM | 14s Tools
Judge 01               : [█████████████████████████████████████░░░] 27s (93.1%) LLM | 2s Tools
Judge 01 (631e84)      : [██████████████████████████████████████░░] 26s (96.3%) LLM | 1s Tools
Judge 02               : [██████████████████████████████████████░░] 33s (97.1%) LLM | 1s Tools
Judge 03               : [██████████████████████████████████████░░] 38s (95.0%) LLM | 2s Tools
Judge 04               : [█████████████████████████████████████░░░] 38s (92.7%) LLM | 2s Tools
Judge 05               : [███████████████████████████████████░░░░░] 25s (89.3%) LLM | 2s Tools
Judge 06               : [████████████████████████████████████░░░░] 30s (90.9%) LLM | 2s Tools
Judge 07               : [█████████████████████████████████████░░░] 51s (94.4%) LLM | 2s Tools
Judge 08               : [██████████████████████████████████████░░] 45s (95.7%) LLM | 1s Tools
Judge 09               : [████████████████████████████████████░░░░] 36s (90.0%) LLM | 3s Tools
Judge 10               : [███████████████████████████████████░░░░░] 29s (87.9%) LLM | 3s Tools
Judge 01 (318bdb)      : [██████████████████████████████████████░░] 41s (95.3%) LLM | 2s Tools
Judge 02 (f6bae3)      : [██████████████████████████████████████░░] 49s (96.1%) LLM | 2s Tools
Judge 03 (89f6b6)      : [█████████████████████████████████████░░░] 54s (94.7%) LLM | 2s Tools
Judge 04 (abb5ae)      : [█████████████████████████████████████░░░] 37s (94.9%) LLM | 1s Tools
Judge 05 (bbe74f)      : [████████████████████████████████████░░░░] 36s (92.3%) LLM | 3s Tools
Judge 06 (51514b)      : [████████████████████████████████████░░░░] 36s (90.0%) LLM | 3s Tools
Judge 01 (05321a)      : [█████████████████████████████████████░░░] 36s (94.7%) LLM | 2s Tools
Judge 01 (6ddd45)      : [████████████████████████████████████████] 1s (100.0%) LLM | 0s Tools
========================================================================================
```

---

## 8. Métricas Deterministas de Latencia y Costo por Etapa (Gemini 4 Hydrogen)

| Etapa del Pipeline | Agentes / Shards | Tiempo de Pared (s) | Costo (USD) | Detalle Determinista |
| :--- | :---: | :---: | :---: | :--- |
| **Stage 1B: CTA Architects** | `8` | `152.0s` | **`$1.1193`** | Mappers max: `80.0s`, Harmonizer: `72.0s` |
| **Stage 3: Shard Authors** | `21` | `368.0s` | **`$10.0657`** | Min: `85.0s`, Mediana: `194.0s`, Straggler: `Shard Author shard_05` (`+174.0s`) |
| **Stage 3B: Repair Engineers** | `7` | `78.0s` | **`$0.9493`** | Min: `36.0s`, Mediana: `41.0s`, Straggler / Slowest: `Repair Engineer C-15` |
| **Stage 5: Blind Judges** | `19` | `57.0s` | **`$2.1314`** | Lote: `120` ítems, 1er intento: `False`, Auto-repair: `0` |
| **Orquestador Principal** | `1` | `1407.0s` | **`$1.9499`** | CLI: `62.0s`, Barrera: `4.0s`, Intervenciones: `0` (`0.0s`) |
| **TOTAL CORRIDA (Gemini 4 Hydrogen)** | **`56`** | **`1407.0s`** | **`$16.2156 USD`** | `$0.0168 USD/preg` (`$0.6006 USD/comp`) |

---

## 9. Taxonomía Consolidada de Errores y Retrabajo

| Categoría de Error | Ocurrencias | Agentes Afectados | Causa Raíz Técnica y Ejemplo |
| :--- | :---: | :--- | :--- |
| **Token Limit Cutoff (Model Truncation)** | **10** | Author Shard 01, Author Shard 02, Author Shard 03 | — |
| **Parameter Diversity & Option Collapse (TPL-VAR / TPL-COLLAPSE)** | **3** | Author Shard 08, Author Shard 10, Author Shard 11 | Command exited with code 1. / Command output: / [COMPILE 1/10] Compilando shard 'shard_08' |
| **Cross-check Verification False (TPL-CROSS)** | **2** | Author Shard 16, Author Shard 21 | Showing lines 1-181 of 181 / 1: Command exited with code 1. / 2: / 3: Command output: / 4: |
| **Anti-Giveaway & Psychometric Parity Violations (R-14..R-19)** | **2** | Author Shard 10, Repair Engineer C-15 (ef0d11) | Command exited with code 1. / Command output: / [COMPILE 2/10] Compilando shard 'shard_10' |
| **File Edit / Write Tool Target Mismatch (replace_file_content / Overwrite)** | **2** | Author Shard 10 | Encountered error in step execution: target content not found in the file; the Target must |
| **Non-Zero CLI Exit / Subprocess Probe (Exit Code 1)** | **1** | Orchestrator | Encountered error in step execution: tool call denied by pre-tool hook: Barrera de Consoli |
| **Shard Compilation & Template Validator Failure (compile_shard / check_templates)** | **1** | Author Shard 07 | Command exited with code 1. / Command output: / [COMPILE 1/10] Compilando shard 'shard_07' |
| **Missing File / Relative Path / Directory Error (FileNotFoundError)** | **1** | Repair Engineer Hab-20 (9f7374) | Encountered error in step execution: file does not exist |

---

## 10. Paquete Forense Agéntico Completo (Argon QA + Clúster Flash)

Todos los artefactos originales individuales generados por los auditores especializados se preservan íntegros en [`reports/audits_archive/mateco_4_optimizacion_v20_k_3/`](file:///D:/Augusto/personal_portfolio/Tops_academy/reports/audits_archive/mateco_4_optimizacion_v20_k_3/):

- **Auditoría Cualitativa Profunda de Calidad (Gemini 4 Argon):** [`qa_report.md`](file:///D:/Augusto/personal_portfolio/Tops_academy/reports/audits_archive/mateco_4_optimizacion_v20_k_3/qa_report.md) *(autocontenido con metadatos JSON embebidos)*
- **Informe Maestro Agéntico del Pipeline (Gemini Flash Lead + 3 Subagentes):** [`agentic_pipeline_audit.md`](file:///D:/Augusto/personal_portfolio/Tops_academy/reports/audits_archive/mateco_4_optimizacion_v20_k_3/agentic_pipeline_audit.md)
- **Sub-Auditorías del Clúster Agéntico (`agentic_batches/`):** [`agentic_batches/`](file:///D:/Augusto/personal_portfolio/Tops_academy/reports/audits_archive/mateco_4_optimizacion_v20_k_3/agentic_batches/)
- **Índice Completo del Archivo Persistente:** [`README.md`](file:///D:/Augusto/personal_portfolio/Tops_academy/reports/audits_archive/mateco_4_optimizacion_v20_k_3/README.md)
