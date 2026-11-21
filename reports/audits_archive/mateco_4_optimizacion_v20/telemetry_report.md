# Informe de Auditoría Arquitectónica Forense: Rendimiento, Shards y Telemetría Multi-Agente
## Curso: Mateco 4 Optimizacion V20 (`mateco_4_optimizacion_v20`)

**Fecha de Auditoría:** `2026-11-21 21:19:09 UTC`  
**Conversación Orquestadora:** [`30d67613-8520-43c2-9044-d7de43975036`](conversation://30d67613-8520-43c2-9044-d7de43975036)  
**Directorio de Trabajo Validado (Zero-Collision):** `D:\Augusto\personal_portfolio\Tops_academy\courses\mateco_4_optimizacion_v20\work` (`match=True`)  
**Enfoque:** Telemetría Determinista de API, Subagentes, Shards, Latencias, Costos USD (Gemini 4 Hydrogen) y Operaciones del Orquestador.

---

## 1. Consolidación de Métricas y Caracterización de Carga

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada** | `6 archivos` (71 págs / 3.61 MB) | 01_optimizacion_dinamica.pdf, 02_Set_Problem_Calculo_de_variaciones.pdf, 03_Teoria_de_control_optimo___teoria (1).pdf, 04_opt_din_3.pdf, 05_Control Optimo Apuntes.pdf, 06_Problemas_teoria_de_control.pdf |
| **Requerimiento de Visión** | `0 páginas` (0 handouts) | Cuadrículas generadas para diagramas/fórmulas |
| **Corpus Sintetizado** | `0 caracteres` (0 palabras) | Texto consolidado tras ingesta y visión |
| **Competencias Extraídas** | **`30 competencias`** | Desglose pedagógico (Hechos, Conceptos, Habilidades) |
| **Shards Particionados** | **`13 shards`** | Unidades de trabajo concurrentes |
| **Subagentes Desplegados** | **`42 subagentes`** | Visión (0), CTA (16), Autores (13), Repairs (1), Jueces (12) |
| **Reactivos Finales Validados** | **`786 preguntas`** | Evaluadas en sandbox |
| **Tokens Entrada (Subagentes)** | **`2,389,722` tokens** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`967,515` tokens** | Código de plantillas y JSON generado |
| **Tokens Caché (Leídos)** | **`12,755,073` tokens** | Caché de contexto reutilizado por la API |
| **Gran Total Tokens Activos** | **`3,581,299` tokens** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`16,336,372` tokens** | Consumo total de cuota facturable |
| **Costo Estimado Total (Gemini 4 Hydrogen)** | **`$12.4267 USD`** | In: `$3.8474` (`$1.50/1M`), Out+Think: `$7.6227` (`$7.50/1M`), Cache: `$0.9566` (`$0.075/1M`) |

---

## 2. Ratios Unitarios Normalizados (Unit Economics)

Métricas normalizadas para comparación *apples-to-apples* frente a cursos de diferente volumen de contenido:

| Métrica Unitaria | Valor Obtenido | Interpretación de Eficiencia |
| :--- | :--- | :--- |
| **Tokens Totales por Pregunta** | **`20,784.2 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`4,556.4 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`544,545.7 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`72,338.8 tokens/comp`** | Costo puro de la etapa de autoría por competencia |
| **Tokens Totales por Página / Slide** | **`230,089.7 tokens/pág`** | Esfuerzo cognitivo por diapositiva original |
| **Costo Estimado por Pregunta (Hydrogen)** | **`$0.0158 USD/preg`** | Costo monetario valorizado por reactivo |
| **Costo Estimado por Competencia (Hydrogen)** | **`$0.4142 USD/comp`** | Costo monetario valorizado por competencia |
| **Segundos de Pared por Pregunta** | **`1.33 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`45.0 preg/min`** | Velocidad de producción del pipeline |
| **Factor de Aceleración Paralela** | **`5.83x`** | Relación tiempo cómputo vs tiempo de pared |

---

## 3. Desglose Forense por Etapas Críticas

### 3.0a. Valorización Monetaria por Etapa (Tarifas Gemini 4 Hydrogen)
> Tarifas oficiales aplicables: Entrada `$1.50/1M`, Caché leído `$0.075/1M`, Salida (incl. thinking) `$7.50/1M`.

| Etapa / Rol | Agentes | Tokens Entrada | Tokens Salida | Caché Leído | Costo Estimado (USD) | % del Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Stage 1A: Visión** | 0 | 0 | 0 | 0 | **`$0.0000`** | 0.0% |
| **Stage 1B: CTA Architects** | 16 | 606,944 | 149,137 | 1,290,783 | **`$2.1258`** | 17.1% |
| **Stage 3: Shard Authors** | 13 | 1,441,914 | 728,250 | 8,205,563 | **`$8.2402`** | 66.3% |
| **Stage 3B: Repair Engineers** | 1 | 43,413 | 3,267 | 116,733 | **`$0.0984`** | 0.8% |
| **Stage 5: Blind Judges** | 12 | 297,451 | 86,861 | 342,739 | **`$1.1233`** | 9.0% |
| **Orquestador Principal (Director)** | 1 | 175,222 | 48,840 | 2,799,255 | **`$0.8391`** | 6.8% |
| **TOTAL CORRIDA (Gemini 4 Hydrogen)** | **43** | **2,564,944** | **1,016,355** | **12,755,073** | **`$12.4267 USD`** | **100.0%** |

### 3.0. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json` & `state.json`)
- **Snapshots de Etapa Verificados (`conversation_id` = `30d67613`):** `9 etapas`
- **Estado Maestro (`work/state.json`):** `completed` (Etapa actual/final: `publish`)

| Etapa (Snapshot) | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes Capturados | Artefactos / Metadatos de Etapa |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`00_prepare`** | `2026-11-21 20:51:50` | `0.13s` | `0` (`0` act) | 0 | `—` |
| **`00b_bootstrap`** | `2026-11-21 20:51:50` | `0.2s` | `0` (`0` act) | 0 | `lock_file=D:\Augusto\personal_portfolio\Tops_academy\courses\mateco_4_optimizacion_v20\work\.c2c_subagent_lock.json` |
| **`01_cta`** | `2026-11-21 20:53:25` | `0.37s` | `46,485` (`19,372` act) | 1 | `needs_harmonize=True` |
| **`02_shard`** | `2026-11-21 20:55:10` | `0.03s` | `0` (`0` act) | 0 | `shards=13` |
| **`03_templates`** | `2026-11-21 21:05:25` | `0.27s` | `0` (`0` act) | 0 | `count=30` |
| **`04_build`** | `2026-11-21 21:05:41` | `16.34s` | `0` (`0` act) | 0 | `total_questions=786` |
| **`05_verify`** | `2026-11-21 21:05:43` | `1.33s` | `0` (`0` act) | 0 | `verified_course_path=D:\Augusto\personal_portfolio\Tops_academy\courses\mateco_4_optimizacion_v20\work\course_verified.json` |
| **`05b_judge_compare`** | `2026-11-21 21:02:42` | `0.07s` | `0` (`0` act) | 0 | `passed=False` |
| **`06_publish`** | `2026-11-21 21:05:46` | `2.79s` | `0` (`0` act) | 0 | `published_json=D:\Augusto\personal_portfolio\Tops_academy\courses\mateco_4_optimizacion_v20.json` |

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
- **Arquitectura:** `MAPREDUCE (14 Mappers + 1 Harmonizer)`
- **Tiempo de Pared Fase Mappers (Máximo):** **`81.0s`** (determinado por `Cognitive Task Analysis Architect part_03`)
- **Tiempo Fase Harmonizer (Barrera Síncrona):** **`73.0s`**
- **Tiempo de Pared Total de Etapa 1B:** **`154.0s`** (`2.6 min`)
- **Costo Estimado Etapa 1B (Gemini 4 Hydrogen):** **`$2.1258 USD`**

| Subagente CTA | Rol / Sección | Turnos | Tokens In | Tokens Out | Cache Leído | Costo (USD) | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| **Cognitive Task Analysis Architect part_01** | Mapper | 4 | 36,510 | 9,322 | 68,378 | `$0.1298` | 0 | **74.0s** |
| **Cognitive Task Analysis Architect part_05** | Mapper | 4 | 38,423 | 10,789 | 70,592 | `$0.1438` | 0 | **71.0s** |
| **Cognitive Task Analysis Architect part_02** | Mapper | 4 | 37,244 | 10,023 | 69,204 | `$0.1362` | 0 | **62.0s** |
| **Cognitive Task Analysis Architect part_04** | Mapper | 4 | 29,279 | 7,738 | 55,551 | `$0.1061` | 0 | **53.0s** |
| **Cognitive Task Analysis Architect part_06** | Mapper | 6 | 35,312 | 8,179 | 110,246 | `$0.1226` | 1 | **62.0s** |
| **Cognitive Task Analysis Architect part_03** | Mapper | 6 | 33,137 | 9,126 | 100,403 | `$0.1257` | 1 | **62.0s** |
| **Cognitive Task Analysis Architect part_07** | Mapper | 4 | 24,542 | 8,990 | 45,118 | `$0.1076` | 0 | **48.0s** |
| **Cognitive Task Analysis Architect part_01** | Mapper | 4 | 37,367 | 10,173 | 69,262 | `$0.1375` | 0 | **75.0s** |
| **Cognitive Task Analysis Architect part_05** | Mapper | 4 | 38,729 | 11,116 | 70,951 | `$0.1468` | 0 | **71.0s** |
| **Cognitive Task Analysis Architect part_02** | Mapper | 4 | 38,855 | 11,601 | 70,779 | `$0.1506` | 0 | **62.0s** |
| **Cognitive Task Analysis Architect part_04** | Mapper | 4 | 30,238 | 8,663 | 56,467 | `$0.1146` | 0 | **50.0s** |
| **Cognitive Task Analysis Architect part_06** | Mapper | 4 | 30,784 | 8,506 | 57,803 | `$0.1143` | 0 | **49.0s** |
| **Cognitive Task Analysis Architect part_03** | Mapper | 6 | 61,369 | 10,724 | 78,682 | `$0.1784` | 1 | **81.0s** |
| **Cognitive Task Analysis Architect part_07** | Mapper | 4 | 23,185 | 7,624 | 43,468 | `$0.0952` | 0 | **41.0s** |
| **CTA Harmonizer** | Harmonizer | 4 | 18,287 | 1,085 | 27,113 | `$0.0376` | 4 | **12.0s** |
| **CTA Harmonizer** | Harmonizer | 6 | 93,683 | 15,478 | 296,766 | `$0.2789` | 0 | **73.0s** |

---

### 3.3. Stage 3: Autoría de Reactivos por Shard y Análisis por Competencia
- **Total de Shards Auditados:** `13 shards concurrentes`
- **Tasa de Aprobación en 1ra Compilación:** **`0/13 (0.0%)`** (Reglas en 1er fallo: `[TPL-ORPHAN-VARS]` (9), `[TPL-STEM-VARIANT-PARITY]` (7), `[GENERAL]` (6), `[TPL-DRY]` (6), `[TPL-VAR]` (6), `[TPL-DYNAMIC-RATIONALE]` (5))
- **Duración Mínima de Shard:** `197.0s` | **Mediana:** `286.0s`
- **Tiempo de Pared Máximo (Straggler Crítico):** **`390.0s`** (`6.5 min`) por `Shard Author shard_12`
- **Retraso de Sincronización Impuesto por el Straggler:** **`+104.0s`** frente a la mediana
- **Tokens Promedio por Competencia en Autores:** **`72,338.8 tokens/competencia`**
- **Costo Estimado Etapa 3 (Gemini 4 Hydrogen):** **`$8.2402 USD`**

| Shard ID | Competencias Asignadas | Comps | Tokens In | Tokens Out | Cache Leído | Total Activo | Costo (USD) | Tokens / Comp | Turnos | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :--- | :--- | :--- |
| **Shard Author shard_01** | `Hab-10, Hab-15` | 2 | 108,303 | 60,249 | 798,950 | 168,552 | `$0.6742` | **84,276.0** | 13 | 3 | **312.0s** |
| **Shard Author shard_09** | `C-03, C-04, C-06` | 3 | 126,285 | 81,693 | 726,860 | 207,978 | `$0.8566` | **69,326.0** | 11 | 2 | **345.0s** |
| **Shard Author shard_10** | `C-14, C-12, C-13` | 3 | 117,060 | 61,762 | 825,387 | 178,822 | `$0.7007` | **59,607.3** | 12 | 2 | **321.0s** |
| **Shard Author shard_11** | `C-01, H-01, C-02` | 3 | 117,041 | 59,702 | 614,628 | 176,743 | `$0.6694` | **58,914.3** | 10 | 1 | **283.0s** |
| **Shard Author shard_02** | `Hab-01, Hab-02` | 2 | 88,973 | 51,578 | 381,105 | 140,551 | `$0.5489` | **70,275.5** | 8 | 1 | **286.0s** |
| **Shard Author shard_03** | `Hab-13, Hab-14` | 2 | 110,338 | 52,503 | 847,212 | 162,841 | `$0.6228` | **81,420.5** | 13 | 3 | **298.0s** |
| **Shard Author shard_04** | `Hab-16, Hab-19` | 2 | 190,028 | 50,689 | 701,486 | 240,717 | `$0.7178` | **120,358.5** | 12 | 2 | **314.0s** |
| **Shard Author shard_05** | `Hab-04, Hab-05` | 2 | 99,026 | 49,861 | 464,116 | 148,887 | `$0.5573` | **74,443.5** | 9 | 1 | **252.0s** |
| **Shard Author shard_06** | `Hab-06, Hab-07` | 2 | 100,058 | 53,814 | 702,787 | 153,872 | `$0.6064` | **76,936.0** | 12 | 3 | **281.0s** |
| **Shard Author shard_07** | `Hab-08, Hab-09` | 2 | 78,631 | 35,285 | 568,761 | 113,916 | `$0.4252` | **56,958.0** | 12 | 2 | **222.0s** |
| **Shard Author shard_08** | `Hab-11, Hab-12` | 2 | 95,109 | 46,871 | 446,724 | 141,980 | `$0.5277` | **70,990.0** | 9 | 1 | **249.0s** |
| **Shard Author shard_12 🛑** | `C-07, C-08, C-11` | 3 | 137,409 | 82,797 | 908,674 | 220,206 | `$0.8952` | **73,402.0** | 12 | 2 | **390.0s** |
| **Shard Author shard_13** | `C-16, C-17` | 2 | 73,653 | 41,446 | 218,873 | 115,099 | `$0.4377` | **57,549.5** | 6 | 1 | **197.0s** |

---

### 3.3b. Stage 3B: Remediación y Repair Engineers (Ingenieros de Reparación)
- **Total de Repair Engineers Desplegados:** `1 subagentes` en **`1 ronda(s)`** (`DONE`: `1`, `BLOCKED`: **`0`**)
- **Duración Mínima:** `32.0s` | **Mediana:** `32.0s` | **Máxima:** `32.0s` (`0.5 min`)
- **Tokens Activos Totales en Reparación:** `46,680 tokens`
- **Costo Estimado Etapa 3B (Gemini 4 Hydrogen):** **`$0.0984 USD`**
- **Agente Determinante del Retraso:** `Repair Engineer C-01`

| Repair Engineer | Estado | Turnos | Tokens In | Tokens Out | Cache Leído | Total Activo | Costo (USD) | Errores | Duración |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Repair Engineer C-01** | `DONE` | 5 | 43,413 | 3,267 | 116,733 | 46,680 | `$0.0984` | 0 | **32.0s** |

---

### 3.4. Evaluación y Arbitraje de Blind Judges (Verificación Psicométrica Ciega)

> [!NOTE]
> **Dictamen de Blind Judges:** ⚠️ NO PASÓ AL PRIMER INTENTO — APROBADO POST-REJUDGE (122/122 REACTIVOS)  
> La Ronda 1 de Blind Judges registró 1 discrepancia(s), por lo que no hubo acuerdo limpio al primer intento. Tras correcciones y Rejudge, el resultado final alcanzó 100.0% de acuerdo (0 discrepancias).

| Dimensión de Arbitraje Ciego | Valor Registrado | Observación Técnica |
| :--- | :--- | :--- |
| **Lote Estratificado Ciego** | `122 reactivos` (30 comps × 2) | Lote de evaluación sin soluciones (`judge_batch.json`) |
| **Subagentes Jueces Ciegos** | `12 jueces` | Aislamiento epistémico en Stage 5 |
| **Costo Etapa 5 (Gemini 4 Hydrogen)** | **`$1.1233 USD`** | Evaluado sobre los 12 Blind Judges (In: `297,451`, Out: `86,861`, Cache: `342,739`) |
| **Resultado al Primer Intento** | **`❌ Falló al primer intento`** | Ronda 1: 1 discrepancia(s) (`flaw_detected`: 0, `kernel_override`: 1); 0 violaciones iniciales |
| **Resultado Final Post-Rejudge** | **`✅ Aprobado`** | `100.0%` acuerdo, `0` discrepancia(s) |
| **Iteraciones de Auto-Reparación** | `0 iteraciones` en sandbox | 0 iteraciones ejecutadas |
| **Intervenciones del Supervisor** | 🛠️ `0 operaciones directas` | Ninguna (ejecución autónoma) |

#### Detalle de Acciones Registradas:
- 1. **Ronda 1 (`judge_report_round_1.json` / `rounds_history`)**: 1 discrepancia(s) detectada(s).
- 2. **Bucle de Auto-Reparación / Rejudge**: 3 ola(s) de jueces ejecutada(s) (0 intervenciones de supervisor).
- 3. **Resultado Final Post-Rejudge (`judge_report.json`)**: ✅ Aprobado (`100.0% agreement rate`, `0 discrepancias` sobre 122 reactivos).

---

## 4. Auditoría Forense del Orquestador y Catálogo de Intervenciones Manuales

### 4.1. Descomposición del Tiempo y Costo del Orquestador
- 💵 **Costo Estimado del Orquestador Principal (Gemini 4 Hydrogen):** **`$0.8391 USD`** (In: `175,222`, Out: `48,840`, Cache: `2,799,255`)
- ⏱️ **Tiempo Total de Pared del Orquestador:** `17.47 min` (`1048.0s`)
- 💻 **Tiempo Activo Ejecutando Comandos CLI (`run.py`):** `0.7 min` (`42.0s`)
- 🛠️ **Tiempo Gastado en Intervenciones Manuales (Supervisor Repair):** **`0.0 min`** (`0.0s`)
- ⏳ **Tiempo Ocioso en Barreras de Sincronización (Esperando Subagentes):** `0.1 min` (`9.0s`)
- 🧠 **Tiempo de Inferencia y Razonamiento del Modelo:** `1.1 min` (`69.0s`)

### 4.2. Catálogo Cronológico de Reparaciones Manuales del Orquestador
Operaciones directas de edición de código ejecutadas por el orquestador: **`0`**

| Paso | Archivo Afectado | Tipo de Acción | Causa Raíz / Justificación Técnica | Herramienta | Tokens Paso |
| :---: | :--- | :--- | :--- | :--- | :--- |
| — | *Ninguna intervención registrada* | — | — | — | 0 |

### 4.3. Fricciones de Orquestación, Hooks y Gobernanza Híbrida
- **Denegaciones de Pre-Tool Hooks:** `3` (Pasos: 28, 42, 43)
- **Llamadas Malformadas (`Malformed function call`):** `0` (Pasos: N/A)
- **Gobernanza Híbrida (`run_workflow` + `invoke_subagent` legado):** `Sí` (`run_workflow`: 4, `invoke_subagent`: 2, `manage_subagents(kill*)`: 0)

---

## 5. Diagnóstico de Cuellos de Botella y Antipatrones Detectados

### ⚠️ [MEDIUM] Fricción de Herramientas en 4 subagentes
- **Ámbito:** `Multiple Subagents`
- **Diagnóstico:** Subagentes como CTA Harmonizer acumularon fallos en consola (4 errores), provocando reintentos e invalidación de caché.

---

## 6. Telemetría de Razonamiento Cognitivo (Thinking Traces)

- **Total de Turnos con Razonamiento:** `99 turnos`
- **Volumen Total de Razonamiento:** `349,926 caracteres`
- **Razonamiento del Orquestador:** `12 turnos` (3,213 chars)
- **Razonamiento de Subagentes:** `87 turnos` (346,713 chars)

| Agente / Subagente | Turnos de Thinking | Caracteres de Thinking | Trazas de Error Capturadas |
| :--- | :---: | :---: | :---: |
| **Cognitive Task Analysis Architect part_01** | 1 | 3,919 | 0 |
| **Cognitive Task Analysis Architect part_05** | 2 | 4,571 | 0 |
| **Cognitive Task Analysis Architect part_02** | 2 | 4,005 | 0 |
| **Cognitive Task Analysis Architect part_04** | 2 | 3,897 | 0 |
| **Cognitive Task Analysis Architect part_06** | 2 | 3,385 | ⚠️ 1 |
| **Cognitive Task Analysis Architect part_03** | 1 | 3,180 | ⚠️ 1 |
| **Cognitive Task Analysis Architect part_07** | 2 | 3,517 | 0 |
| **CTA Harmonizer** | 1 | 285 | 0 |
| **Cognitive Task Analysis Architect part_01** | 1 | 3,799 | 0 |
| **Cognitive Task Analysis Architect part_05** | 3 | 4,517 | 0 |
| **Cognitive Task Analysis Architect part_02** | 1 | 4,754 | 0 |
| **Cognitive Task Analysis Architect part_04** | 2 | 4,900 | 0 |
| **Cognitive Task Analysis Architect part_06** | 2 | 4,524 | 0 |
| **Cognitive Task Analysis Architect part_03** | 3 | 4,553 | ⚠️ 1 |
| **Cognitive Task Analysis Architect part_07** | 2 | 3,248 | 0 |
| **CTA Harmonizer** | 4 | 14,835 | 0 |
| **Repair Engineer C-01** | 2 | 2,127 | 0 |
| **Blind Judge 01** | 1 | 4,272 | 0 |
| **Shard Author shard_01** | 4 | 18,632 | ⚠️ 3 |
| **Shard Author shard_09** | 3 | 15,697 | ⚠️ 2 |
| **Shard Author shard_10** | 3 | 16,345 | ⚠️ 2 |
| **Shard Author shard_11** | 3 | 13,923 | ⚠️ 1 |
| **Shard Author shard_02** | 2 | 14,416 | ⚠️ 1 |
| **Shard Author shard_03** | 4 | 15,947 | ⚠️ 3 |
| **Shard Author shard_04** | 3 | 11,901 | ⚠️ 2 |
| **Shard Author shard_05** | 3 | 23,347 | ⚠️ 1 |
| **Shard Author shard_06** | 3 | 17,521 | ⚠️ 3 |
| **Shard Author shard_07** | 5 | 15,173 | ⚠️ 2 |
| **Shard Author shard_08** | 2 | 14,215 | ⚠️ 1 |
| **Shard Author shard_12** | 5 | 19,257 | ⚠️ 2 |
| **Shard Author shard_13** | 2 | 9,282 | ⚠️ 1 |
| **Blind Judge 01** | 1 | 6,377 | 0 |
| **Blind Judge 02** | 1 | 6,530 | 0 |
| **Blind Judge 03** | 1 | 5,735 | 0 |
| **Blind Judge 04** | 1 | 5,357 | 0 |
| **Blind Judge 05** | 1 | 6,234 | 0 |
| **Blind Judge 06** | 1 | 5,110 | 0 |
| **Blind Judge 07** | 1 | 6,560 | 0 |
| **Blind Judge 08** | 1 | 4,965 | 0 |
| **Blind Judge 09** | 1 | 5,434 | 0 |
| **Blind Judge 10** | 1 | 7,676 | 0 |
| **Blind Judge 01** | 1 | 2,791 | 0 |

---
*Reporte forense determinista emitido por `c2c-run-auditor`.*