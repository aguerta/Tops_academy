# Informe de Auditoría Arquitectónica Forense: Rendimiento, Shards y Telemetría Multi-Agente
## Curso: Mateco 4 Optimizacion Plus (`mateco_4_optimizacion_plus`)

**Fecha de Auditoría:** `2026-11-21 21:19:09 UTC`  
**Conversación Orquestadora:** [`619cb6cf-7cb2-4dfe-a559-5b7064a904e8`](conversation://619cb6cf-7cb2-4dfe-a559-5b7064a904e8)  
**Directorio de Trabajo Validado (Zero-Collision):** `D:\Augusto\personal_portfolio\Tops_academy\courses\mateco_4_optimizacion_plus\work` (`match=True`)  
**Enfoque:** Telemetría Determinista de API, Subagentes, Shards, Latencias, Costos USD (Gemini 4 Hydrogen) y Operaciones del Orquestador.

---

## 1. Consolidación de Métricas y Caracterización de Carga

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada** | `5 archivos` (65 págs / 3.47 MB) | Control Optimo Apuntes.pdf, opt_din_3.pdf, optimizacion_dinamica.pdf, Problemas_teoria_de_control.pdf, Teoria_de_control_optimo___teoria (1).pdf |
| **Requerimiento de Visión** | `0 páginas` (0 handouts) | Cuadrículas generadas para diagramas/fórmulas |
| **Corpus Sintetizado** | `0 caracteres` (0 palabras) | Texto consolidado tras ingesta y visión |
| **Competencias Extraídas** | **`30 competencias`** | Desglose pedagógico (Hechos, Conceptos, Habilidades) |
| **Shards Particionados** | **`13 shards`** | Unidades de trabajo concurrentes |
| **Subagentes Desplegados** | **`44 subagentes`** | Visión (0), CTA (7), Autores (13), Repairs (10), Jueces (14) |
| **Reactivos Finales Validados** | **`730 preguntas`** | Evaluadas en sandbox |
| **Tokens Entrada (Subagentes)** | **`2,202,826` tokens** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`914,241` tokens** | Código de plantillas y JSON generado |
| **Tokens Caché (Leídos)** | **`11,038,683` tokens** | Caché de contexto reutilizado por la API |
| **Gran Total Tokens Activos** | **`3,467,268` tokens** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`14,505,951` tokens** | Consumo total de cuota facturable |
| **Costo Estimado Total (Gemini 4 Hydrogen)** | **`$11.6942 USD`** | In: `$3.7846` (`$1.50/1M`), Out+Think: `$7.0817` (`$7.50/1M`), Cache: `$0.8279` (`$0.075/1M`) |

---

## 2. Ratios Unitarios Normalizados (Unit Economics)

Métricas normalizadas para comparación *apples-to-apples* frente a cursos de diferente volumen de contenido:

| Métrica Unitaria | Valor Obtenido | Interpretación de Eficiencia |
| :--- | :--- | :--- |
| **Tokens Totales por Pregunta** | **`19,871.2 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`4,749.7 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`483,531.7 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`49,937.1 tokens/comp`** | Costo puro de la etapa de autoría por competencia |
| **Tokens Totales por Página / Slide** | **`223,168.5 tokens/pág`** | Esfuerzo cognitivo por diapositiva original |
| **Costo Estimado por Pregunta (Hydrogen)** | **`$0.0160 USD/preg`** | Costo monetario valorizado por reactivo |
| **Costo Estimado por Competencia (Hydrogen)** | **`$0.3898 USD/comp`** | Costo monetario valorizado por competencia |
| **Segundos de Pared por Pregunta** | **`2.1 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`28.63 preg/min`** | Velocidad de producción del pipeline |
| **Factor de Aceleración Paralela** | **`4.43x`** | Relación tiempo cómputo vs tiempo de pared |

---

## 3. Desglose Forense por Etapas Críticas

### 3.0a. Valorización Monetaria por Etapa (Tarifas Gemini 4 Hydrogen)
> Tarifas oficiales aplicables: Entrada `$1.50/1M`, Caché leído `$0.075/1M`, Salida (incl. thinking) `$7.50/1M`.

| Etapa / Rol | Agentes | Tokens Entrada | Tokens Salida | Caché Leído | Costo Estimado (USD) | % del Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Stage 1A: Visión** | 0 | 0 | 0 | 0 | **`$0.0000`** | 0.0% |
| **Stage 1B: CTA Architects** | 7 | 309,458 | 119,929 | 935,694 | **`$1.4338`** | 12.3% |
| **Stage 3: Shard Authors** | 13 | 956,386 | 541,726 | 4,559,405 | **`$5.8395`** | 49.9% |
| **Stage 3B: Repair Engineers** | 10 | 561,494 | 103,397 | 2,025,216 | **`$1.7696`** | 15.1% |
| **Stage 5: Blind Judges** | 14 | 375,488 | 149,189 | 361,493 | **`$1.7093`** | 14.6% |
| **Orquestador Principal (Director)** | 1 | 320,215 | 29,986 | 3,156,875 | **`$0.9420`** | 8.1% |
| **TOTAL CORRIDA (Gemini 4 Hydrogen)** | **45** | **2,523,041** | **944,227** | **11,038,683** | **`$11.6942 USD`** | **100.0%** |

### 3.0. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json` & `state.json`)
- **Snapshots de Etapa Verificados (`conversation_id` = `619cb6cf`):** `8 etapas`
- **Estado Maestro (`work/state.json`):** `completed` (Etapa actual/final: `publish`)

| Etapa (Snapshot) | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes Capturados | Artefactos / Metadatos de Etapa |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`00_prepare`** | `2026-11-19 01:24:11` | `0.14s` | `0` (`0` act) | 0 | `—` |
| **`00b_bootstrap`** | `2026-11-19 01:24:11` | `0.25s` | `0` (`0` act) | 0 | `lock_file=D:\Augusto\personal_portfolio\Tops_academy\courses\mateco_4_optimizacion_plus\work\.c2c_subagent_lock.json` |
| **`01_cta`** | `2026-11-19 01:27:38` | `0.29s` | `0` (`0` act) | 0 | `needs_harmonize=True` |
| **`02_shard`** | `2026-11-19 01:29:45` | `0.03s` | `0` (`0` act) | 0 | `shards=13` |
| **`03_templates`** | `2026-11-19 01:49:11` | `0.5s` | `0` (`0` act) | 0 | `count=30` |
| **`04_build`** | `2026-11-19 01:49:18` | `6.37s` | `0` (`0` act) | 0 | `total_questions=730` |
| **`05_verify`** | `2026-11-19 01:49:19` | `1.56s` | `0` (`0` act) | 0 | `verified_course_path=D:\Augusto\personal_portfolio\Tops_academy\courses\mateco_4_optimizacion_plus\work\course_verified.json` |
| **`06_publish`** | `2026-11-19 01:49:23` | `3.2s` | `0` (`0` act) | 0 | `published_json=D:\Augusto\personal_portfolio\Tops_academy\courses\mateco_4_optimizacion_plus.json` |

---

### 3.1. Stage 1A: Preprocesamiento de Visión
- **Subagentes de Visión Desplegados:** `0 agentes en paralelo`
- **Tiempo de Pared de la Etapa (Máximo / Critical Path):** **`0.0s`** (`0.0 min`)
- **Costo Estimado Etapa 1A (Gemini 4 Hydrogen):** **`$0.0000 USD`**
- **Agente Determinante del Camino Crítico:** `N/A`

| Subagente de Visión | Turnos | Tokens In | Tokens Out | Cache Leído | Total Activo | Costo (USD) | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- |

---

### 3.2. Stage 1B: Análisis Cognitivo de Competencias (CTA)
- **Arquitectura:** `MAPREDUCE (6 Mappers + 1 Harmonizer)`
- **Tiempo de Pared Fase Mappers (Máximo):** **`171.0s`** (determinado por `Cognitive Task Analysis Architect part_03`)
- **Tiempo Fase Harmonizer (Barrera Síncrona):** **`98.0s`**
- **Tiempo de Pared Total de Etapa 1B:** **`269.0s`** (`4.5 min`)
- **Costo Estimado Etapa 1B (Gemini 4 Hydrogen):** **`$1.4338 USD`**

| Subagente CTA | Rol / Sección | Turnos | Tokens In | Tokens Out | Cache Leído | Costo (USD) | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| **Cognitive Task Analysis Architect part_02** | Mapper | 5 | 41,175 | 16,157 | 100,390 | `$0.1905` | 1 | **114.0s** |
| **Cognitive Task Analysis Architect part_03** | Mapper | 7 | 53,122 | 24,635 | 194,178 | `$0.2790` | 2 | **171.0s** |
| **Cognitive Task Analysis Architect part_04** | Mapper | 7 | 54,183 | 25,886 | 198,591 | `$0.2903` | 2 | **142.0s** |
| **Cognitive Task Analysis Architect part_01** | Mapper | 5 | 32,375 | 12,697 | 78,972 | `$0.1497` | 1 | **77.0s** |
| **Cognitive Task Analysis Architect part_06** | Mapper | 5 | 31,906 | 12,954 | 76,947 | `$0.1508` | 1 | **77.0s** |
| **Cognitive Task Analysis Architect part_05** | Mapper | 5 | 26,238 | 13,228 | 60,004 | `$0.1431` | 1 | **71.0s** |
| **CTA Harmonizer** | Harmonizer | 6 | 70,459 | 14,372 | 226,612 | `$0.2305` | 0 | **98.0s** |

---

### 3.3. Stage 3: Autoría de Reactivos por Shard y Análisis por Competencia
- **Total de Shards Auditados:** `13 shards concurrentes`
- **Tasa de Aprobación en 1ra Compilación:** **`0/13 (0.0%)`** (Reglas en 1er fallo: `[GENERAL]` (12), `[TPL-CONST-DISTRACTOR]` (9), `[TPL-DYNAMIC-RATIONALE]` (7), `[TPL-DRY]` (6), `[TPL-VAR]` (5), `[TPL-VERIFIER-UNSOUND]` (4))
- **Duración Mínima de Shard:** `130.0s` | **Mediana:** `231.0s`
- **Tiempo de Pared Máximo (Straggler Crítico):** **`330.0s`** (`5.5 min`) por `Shard Author shard_02`
- **Retraso de Sincronización Impuesto por el Straggler:** **`+99.0s`** frente a la mediana
- **Tokens Promedio por Competencia en Autores:** **`49,937.1 tokens/competencia`**
- **Costo Estimado Etapa 3 (Gemini 4 Hydrogen):** **`$5.8395 USD`**

| Shard ID | Competencias Asignadas | Comps | Tokens In | Tokens Out | Cache Leído | Total Activo | Costo (USD) | Tokens / Comp | Turnos | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :--- | :--- | :--- |
| **Shard Author shard_01** | `Hab-03, Hab-05` | 2 | 75,365 | 44,695 | 457,939 | 120,060 | `$0.4826` | **60,030.0** | 11 | 3 | **260.0s** |
| **Shard Author shard_02 🛑** | `Hab-01, Hab-02` | 2 | 93,380 | 56,305 | 738,015 | 149,685 | `$0.6177` | **74,842.5** | 16 | 3 | **330.0s** |
| **Shard Author shard_03** | `Hab-07, Hab-08` | 2 | 83,954 | 50,128 | 433,049 | 134,082 | `$0.5344` | **67,041.0** | 10 | 2 | **262.0s** |
| **Shard Author shard_04** | `Hab-14, Hab-16` | 2 | 61,200 | 39,751 | 198,865 | 100,951 | `$0.4048` | **50,475.5** | 7 | 1 | **188.0s** |
| **Shard Author shard_05** | `Hab-10, Hab-11` | 2 | 48,889 | 30,851 | 137,830 | 79,740 | `$0.3151` | **39,870.0** | 6 | 1 | **165.0s** |
| **Shard Author shard_06** | `Hab-12, Hab-13` | 2 | 58,516 | 37,500 | 194,254 | 96,016 | `$0.3836` | **48,008.0** | 7 | 1 | **190.0s** |
| **Shard Author shard_08** | `C-01, C-02, C-04` | 3 | 71,137 | 45,124 | 288,627 | 116,261 | `$0.4668` | **38,753.7** | 8 | 1 | **231.0s** |
| **Shard Author shard_09** | `C-05, C-06, C-07` | 3 | 94,970 | 43,838 | 696,219 | 138,808 | `$0.5235` | **46,269.3** | 13 | 2 | **264.0s** |
| **Shard Author shard_10** | `C-10, C-11, C-12` | 3 | 62,241 | 40,406 | 199,903 | 102,647 | `$0.4114` | **34,215.7** | 7 | 1 | **215.0s** |
| **Shard Author shard_11** | `C-13, C-14, C-15` | 3 | 86,526 | 50,826 | 386,526 | 137,352 | `$0.5400` | **45,784.0** | 9 | 1 | **259.0s** |
| **Shard Author shard_12** | `H-01, C-08, C-09` | 3 | 82,477 | 44,165 | 531,210 | 126,642 | `$0.4948` | **42,214.0** | 12 | 3 | **264.0s** |
| **Shard Author shard_13** | `C-16, C-17` | 2 | 94,613 | 36,028 | 148,692 | 130,641 | `$0.4233` | **65,320.5** | 7 | 1 | **188.0s** |
| **Shard Author shard_07** | `Hab-19` | 1 | 43,118 | 22,109 | 148,276 | 65,227 | `$0.2416` | **65,227.0** | 7 | 1 | **130.0s** |

---

### 3.3b. Stage 3B: Remediación y Repair Engineers (Ingenieros de Reparación)
- **Total de Repair Engineers Desplegados:** `10 subagentes` en **`3 ronda(s)`** (`DONE`: `10`, `BLOCKED`: **`0`**)
- **Duración Mínima:** `37.0s` | **Mediana:** `61.0s` | **Máxima:** `283.0s` (`4.7 min`)
- **Tokens Activos Totales en Reparación:** `664,891 tokens`
- **Costo Estimado Etapa 3B (Gemini 4 Hydrogen):** **`$1.7696 USD`**
- **Agente Determinante del Retraso:** `Repair Engineer shard_11 (C-14, C-15)`

| Repair Engineer | Estado | Turnos | Tokens In | Tokens Out | Cache Leído | Total Activo | Costo (USD) | Errores | Duración |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Repair Engineer C-04** | `DONE` | 6 | 57,622 | 6,432 | 153,234 | 64,054 | `$0.1462` | 1 | **58.0s** |
| **Repair Engineer shard_11 (C-14, C-15)** | `DONE` | 16 | 94,148 | 42,873 | 792,502 | 137,021 | `$0.5222` | 2 | **283.0s** |
| **Repair Engineer C-17** | `DONE` | 5 | 30,447 | 3,843 | 65,629 | 34,290 | `$0.0794` | 1 | **37.0s** |
| **Repair Engineer Hab-03** | `DONE` | 7 | 62,370 | 13,988 | 187,157 | 76,358 | `$0.2125` | 0 | **102.0s** |
| **Repair Engineer Hab-07** | `DONE` | 7 | 96,899 | 7,380 | 137,006 | 104,279 | `$0.2110` | 0 | **61.0s** |
| **Repair Engineer Hab-13** | `DONE` | 7 | 36,560 | 4,195 | 105,559 | 40,755 | `$0.0942` | 0 | **45.0s** |
| **Repair Engineer Hab-19** | `DONE` | 6 | 48,341 | 4,899 | 110,161 | 53,240 | `$0.1175` | 0 | **42.0s** |
| **Repair Engineer C-04** | `DONE` | 7 | 43,131 | 7,764 | 134,810 | 50,895 | `$0.1330` | 0 | **70.0s** |
| **Repair Engineer Hab-03** | `DONE` | 8 | 52,683 | 5,515 | 190,883 | 58,198 | `$0.1347` | 1 | **58.0s** |
| **Repair Engineer Hab-03** | `DONE` | 9 | 39,293 | 6,508 | 148,275 | 45,801 | `$0.1189` | 0 | **63.0s** |

---

### 3.4. Evaluación y Arbitraje de Blind Judges (Verificación Psicométrica Ciega)

> [!NOTE]
> **Dictamen de Blind Judges:** ⚠️ NO PASÓ AL PRIMER INTENTO — APROBADO POST-REJUDGE (120/120 REACTIVOS)  
> La Ronda 1 de Blind Judges registró 12 discrepancia(s), por lo que no hubo acuerdo limpio al primer intento. Tras correcciones y Rejudge, el resultado final alcanzó 100.0% de acuerdo (0 discrepancias).

| Dimensión de Arbitraje Ciego | Valor Registrado | Observación Técnica |
| :--- | :--- | :--- |
| **Lote Estratificado Ciego** | `120 reactivos` (30 comps × 2) | Lote de evaluación sin soluciones (`judge_batch.json`) |
| **Subagentes Jueces Ciegos** | `14 jueces` | Aislamiento epistémico en Stage 5 |
| **Costo Etapa 5 (Gemini 4 Hydrogen)** | **`$1.7093 USD`** | Evaluado sobre los 14 Blind Judges (In: `375,488`, Out: `149,189`, Cache: `361,493`) |
| **Resultado al Primer Intento** | **`❌ Falló al primer intento`** | Ronda 1: 12 discrepancia(s) (`flaw_detected`: 10, `kernel_override`: 0); 0 violaciones iniciales |
| **Resultado Final Post-Rejudge** | **`✅ Aprobado`** | `100.0%` acuerdo, `0` discrepancia(s) |
| **Iteraciones de Auto-Reparación** | `0 iteraciones` en sandbox | 0 iteraciones ejecutadas |
| **Intervenciones del Supervisor** | 🛠️ `0 operaciones directas` | Ninguna (ejecución autónoma) |

#### Detalle de Acciones Registradas:
- 1. **Ronda 1 (`judge_report_round_1.json` / `rounds_history`)**: 12 discrepancia(s) detectada(s).
- 2. **Bucle de Auto-Reparación / Rejudge**: 4 ola(s) de jueces ejecutada(s) (0 intervenciones de supervisor).
- 3. **Resultado Final Post-Rejudge (`judge_report.json`)**: ✅ Aprobado (`100.0% agreement rate`, `0 discrepancias` sobre 120 reactivos).

---

## 4. Auditoría Forense del Orquestador y Catálogo de Intervenciones Manuales

### 4.1. Descomposición del Tiempo y Costo del Orquestador
- 💵 **Costo Estimado del Orquestador Principal (Gemini 4 Hydrogen):** **`$0.9420 USD`** (In: `320,215`, Out: `29,986`, Cache: `3,156,875`)
- ⏱️ **Tiempo Total de Pared del Orquestador:** `25.5 min` (`1530.0s`)
- 💻 **Tiempo Activo Ejecutando Comandos CLI (`run.py`):** `1.1 min` (`67.0s`)
- 🛠️ **Tiempo Gastado en Intervenciones Manuales (Supervisor Repair):** **`0.0 min`** (`0.0s`)
- ⏳ **Tiempo Ocioso en Barreras de Sincronización (Esperando Subagentes):** `0.1 min` (`4.0s`)
- 🧠 **Tiempo de Inferencia y Razonamiento del Modelo:** `2.1 min` (`126.0s`)

### 4.2. Catálogo Cronológico de Reparaciones Manuales del Orquestador
Operaciones directas de edición de código ejecutadas por el orquestador: **`0`**

| Paso | Archivo Afectado | Tipo de Acción | Causa Raíz / Justificación Técnica | Herramienta | Tokens Paso |
| :---: | :--- | :--- | :--- | :--- | :--- |
| — | *Ninguna intervención registrada* | — | — | — | 0 |

### 4.3. Fricciones de Orquestación, Hooks y Gobernanza Híbrida
- **Denegaciones de Pre-Tool Hooks:** `0` (Pasos: N/A)
- **Llamadas Malformadas (`Malformed function call`):** `2` (Pasos: 52, 89)
- **Gobernanza Híbrida (`run_workflow` + `invoke_subagent` legado):** `Sí` (`run_workflow`: 9, `invoke_subagent`: 1, `manage_subagents(kill*)`: 0)

---

## 5. Diagnóstico de Cuellos de Botella y Antipatrones Detectados

### ⚠️ [MEDIUM] Fricción de Herramientas en 3 subagentes
- **Ámbito:** `Multiple Subagents`
- **Diagnóstico:** Subagentes como Shard Author shard_01 acumularon fallos en consola (3 errores), provocando reintentos e invalidación de caché.

---

## 6. Telemetría de Razonamiento Cognitivo (Thinking Traces)

- **Total de Turnos con Razonamiento:** `131 turnos`
- **Volumen Total de Razonamiento:** `517,538 caracteres`
- **Razonamiento del Orquestador:** `9 turnos` (2,419 chars)
- **Razonamiento de Subagentes:** `122 turnos` (515,119 chars)

| Agente / Subagente | Turnos de Thinking | Caracteres de Thinking | Trazas de Error Capturadas |
| :--- | :---: | :---: | :---: |
| **Cognitive Task Analysis Architect part_02** | 2 | 3,256 | ⚠️ 1 |
| **Cognitive Task Analysis Architect part_03** | 4 | 3,351 | ⚠️ 2 |
| **Cognitive Task Analysis Architect part_04** | 3 | 5,553 | ⚠️ 2 |
| **Cognitive Task Analysis Architect part_01** | 3 | 4,413 | ⚠️ 1 |
| **Cognitive Task Analysis Architect part_06** | 2 | 2,629 | ⚠️ 1 |
| **Cognitive Task Analysis Architect part_05** | 1 | 5,003 | ⚠️ 1 |
| **CTA Harmonizer** | 3 | 15,385 | 0 |
| **Repair Engineer C-04** | 5 | 4,972 | ⚠️ 1 |
| **Repair Engineer shard_11 (C-14, C-15)** | 7 | 35,866 | ⚠️ 2 |
| **Repair Engineer C-17** | 3 | 2,182 | ⚠️ 1 |
| **Repair Engineer Hab-03** | 6 | 11,096 | 0 |
| **Repair Engineer Hab-07** | 4 | 3,920 | 0 |
| **Repair Engineer Hab-13** | 4 | 3,083 | 0 |
| **Repair Engineer Hab-19** | 3 | 3,403 | 0 |
| **Blind Judge 01** | 1 | 9,411 | 0 |
| **Blind Judge 02** | 2 | 13,163 | 0 |
| **Repair Engineer C-04** | 3 | 4,676 | 0 |
| **Repair Engineer Hab-03** | 5 | 4,081 | ⚠️ 1 |
| **Blind Judge 01** | 1 | 6,866 | 0 |
| **Repair Engineer Hab-03** | 4 | 5,388 | 0 |
| **Blind Judge 01** | 1 | 3,597 | 0 |
| **Shard Author shard_01** | 4 | 23,594 | ⚠️ 3 |
| **Shard Author shard_02** | 5 | 33,338 | ⚠️ 3 |
| **Shard Author shard_03** | 4 | 17,343 | ⚠️ 2 |
| **Shard Author shard_04** | 3 | 21,703 | ⚠️ 1 |
| **Shard Author shard_05** | 3 | 13,981 | ⚠️ 1 |
| **Shard Author shard_06** | 4 | 18,533 | ⚠️ 1 |
| **Shard Author shard_08** | 3 | 20,355 | ⚠️ 1 |
| **Shard Author shard_09** | 6 | 21,998 | ⚠️ 2 |
| **Shard Author shard_10** | 2 | 16,739 | ⚠️ 1 |
| **Shard Author shard_11** | 2 | 22,405 | ⚠️ 1 |
| **Shard Author shard_12** | 3 | 18,357 | ⚠️ 3 |
| **Shard Author shard_13** | 2 | 22,309 | ⚠️ 1 |
| **Shard Author shard_07** | 2 | 14,404 | ⚠️ 1 |
| **Blind Judge 01** | 1 | 9,977 | 0 |
| **Blind Judge 02** | 2 | 7,919 | 0 |
| **Blind Judge 03** | 1 | 15,930 | 0 |
| **Blind Judge 04** | 1 | 7,634 | 0 |
| **Blind Judge 05** | 2 | 7,321 | 0 |
| **Blind Judge 06** | 1 | 5,795 | 0 |
| **Blind Judge 07** | 1 | 6,608 | 0 |
| **Blind Judge 08** | 1 | 13,946 | 0 |
| **Blind Judge 09** | 1 | 13,603 | 0 |
| **Blind Judge 10** | 1 | 10,033 | 0 |

---
*Reporte forense determinista emitido por `c2c-run-auditor`.*