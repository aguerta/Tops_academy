# Informe de Auditoría Arquitectónica Forense: Rendimiento, Shards y Telemetría Multi-Agente
## Curso: Solow M20 V11 (`solow_m20_v11`)

**Fecha de Auditoría:** `2026-11-22 21:00:00 UTC`  
**Conversación Orquestadora:** [`dc8545ff-fd7d-4e36-8545-6411880c0eb2`](conversation://dc8545ff-fd7d-4e36-8545-6411880c0eb2)  
**Directorio de Trabajo Validado (Zero-Collision):** `D:\Augusto\personal_portfolio\Tops_academy\courses\solow_m20_v11\work` (`match=True`)  
**Enfoque:** Telemetría Determinista de API, Subagentes, Shards, Latencias, Costos USD (Gemini 4 Hydrogen) y Operaciones del Orquestador.

---

## 1. Consolidación de Métricas y Caracterización de Carga

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada** | `2 archivos` (36 págs / 1.49 MB) | 05_15_07_El_modelo_de_crecimiento_de_Solow.pdf, solow1956.pdf |
| **Requerimiento de Visión** | `0 páginas` (0 handouts) | Cuadrículas generadas para diagramas/fórmulas |
| **Corpus Sintetizado** | `0 caracteres` (0 palabras) | Texto consolidado tras ingesta y visión |
| **Competencias Extraídas** | **`20 competencias`** | Desglose pedagógico (Hechos, Conceptos, Habilidades) |
| **Shards Particionados** | **`20 shards`** | Unidades de trabajo concurrentes |
| **Subagentes Desplegados** | **`50 subagentes`** | Visión (0), CTA (4), Autores (20), Repairs (7), Jueces (19) |
| **Reactivos Finales Validados** | **`621 preguntas`** | Evaluadas en sandbox |
| **Tokens Entrada (Subagentes)** | **`2,187,306` tokens** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`704,099` tokens** | Código de plantillas y JSON generado |
| **Tokens Caché (Leídos)** | **`7,747,731` tokens** | Caché de contexto reutilizado por la API |
| **Gran Total Tokens Activos** | **`3,195,061` tokens** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`10,942,792` tokens** | Consumo total de cuota facturable |
| **Costo Estimado Total (Gemini 4 Hydrogen)** | **`$9.87 USD`** | In: `$3.67` (`$1.50/1M`), Out+Think: `$5.62` (`$7.50/1M`), Cache: `$0.58` (`$0.08/1M`) |

---

## 2. Ratios Unitarios Normalizados (Unit Economics)

Métricas normalizadas para comparación *apples-to-apples* frente a cursos de diferente volumen de contenido:

| Métrica Unitaria | Valor Obtenido | Interpretación de Eficiencia |
| :--- | :--- | :--- |
| **Tokens Totales por Pregunta** | **`17,621.2 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`5,145.0 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`547,139.6 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`80,310.7 tokens/comp`** | Costo puro de la etapa de autoría por competencia |
| **Tokens Totales por Página / Slide** | **`303,966.4 tokens/pág`** | Esfuerzo cognitivo por diapositiva original |
| **Costo Estimado por Pregunta (Hydrogen)** | **`$0.02 USD/preg`** | Costo monetario valorizado por reactivo |
| **Costo Estimado por Competencia (Hydrogen)** | **`$0.49 USD/comp`** | Costo monetario valorizado por competencia |
| **Segundos de Pared por Pregunta** | **`2.3 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`26.11 preg/min`** | Velocidad de producción del pipeline |
| **Factor de Aceleración Paralela** | **`3.99x`** | Relación tiempo cómputo vs tiempo de pared |

---

## 3. Desglose Forense por Etapas Críticas

### 3.0a. Valorización Monetaria por Etapa (Tarifas Gemini 4 Hydrogen)
> Tarifas oficiales aplicables: Entrada `$1.50/1M`, Caché leído `$0.08/1M`, Salida (incl. thinking) `$7.50/1M`.

| Etapa / Rol | Agentes | Tokens Entrada | Tokens Salida | Caché Leído | Costo Estimado (USD) | % del Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Stage 1A: Visión** | 0 | 0 | 0 | 0 | **`$0.00`** | 0.0% |
| **Stage 1B: CTA Architects** | 4 | 152,062 | 35,692 | 313,802 | **`$0.52`** | 5.3% |
| **Stage 3: Shard Authors** | 20 | 1,176,700 | 429,514 | 4,562,657 | **`$5.33`** | 54.0% |
| **Stage 3B: Repair Engineers** | 7 | 319,579 | 53,469 | 931,201 | **`$0.95`** | 9.6% |
| **Stage 5: Blind Judges** | 19 | 538,965 | 185,424 | 531,544 | **`$2.24`** | 22.7% |
| **Orquestador Principal (Director)** | 1 | 258,049 | 45,607 | 1,408,527 | **`$0.83`** | 8.4% |
| **TOTAL CORRIDA (Gemini 4 Hydrogen)** | **51** | **2,445,355** | **749,706** | **7,747,731** | **`$9.87 USD`** | **100.0%** |

### 3.0. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json` & `state.json`)
- **Snapshots de Etapa Verificados (`conversation_id` = `dc8545ff`):** `9 etapas`
- **Estado Maestro (`work/state.json`):** `completed` (Etapa actual/final: `publish`)

| Etapa (Snapshot) | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes Capturados | Artefactos / Metadatos de Etapa |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`00_prepare`** | `2026-11-22 20:33:20` | `0.05s` | `0` (`0` act) | 0 | `—` |
| **`00b_bootstrap`** | `2026-11-22 20:33:20` | `0.1s` | `0` (`0` act) | 0 | `lock_file=D:\Augusto\personal_portfolio\Tops_academy\courses\solow_m20_v11\work\.c2c_subagent_lock.json` |
| **`01_cta`** | `2026-11-22 20:37:57` | `0.96s` | `0` (`0` act) | 0 | `competencies=20` |
| **`02_shard`** | `2026-11-22 20:37:59` | `0.05s` | `0` (`0` act) | 0 | `shards=20` |
| **`03_templates`** | `2026-11-22 20:56:25` | `0.38s` | `0` (`0` act) | 0 | `count=20` |
| **`04_build`** | `2026-11-22 20:56:33` | `8.24s` | `0` (`0` act) | 0 | `total_questions=621` |
| **`05_verify`** | `2026-11-22 20:56:34` | `1.31s` | `0` (`0` act) | 0 | `verified_course_path=D:\Augusto\personal_portfolio\Tops_academy\courses\solow_m20_v11\work\course_verified.json` |
| **`05b_judge_compare`** | `2026-11-22 20:45:29` | `0.11s` | `0` (`0` act) | 0 | `passed=False` |
| **`06_publish`** | `2026-11-22 20:56:37` | `2.7s` | `0` (`0` act) | 0 | `published_json=D:\Augusto\personal_portfolio\Tops_academy\courses\solow_m20_v11.json` |

---

### 3.1. Stage 1A: Preprocesamiento de Visión
- **Subagentes de Visión Desplegados:** `0 agentes en paralelo`
- **Tiempo de Pared de la Etapa (Máximo / Critical Path):** **`0.0s`** (`0.0 min`)
- **Costo Estimado Etapa 1A (Gemini 4 Hydrogen):** **`$0.00 USD`**
- **Agente Determinante del Camino Crítico:** `N/A`

| Subagente de Visión | Turnos | Tokens In | Tokens Out | Cache Leído | Total Activo | Costo (USD) | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- |

---

### 3.2. Stage 1B: Análisis Cognitivo de Competencias (CTA)
- **Arquitectura:** `MAPREDUCE (3 Mappers + 1 Harmonizer)`
- **Tiempo de Pared Fase Mappers (Máximo):** **`70.0s`** (determinado por `Cognitive Task Analysis Architect part_03`)
- **Tiempo Fase Harmonizer (Barrera Síncrona):** **`41.0s`**
- **Tiempo de Pared Total de Etapa 1B:** **`111.0s`** (`1.9 min`)
- **Costo Estimado Etapa 1B (Gemini 4 Hydrogen):** **`$0.52 USD`**

| Subagente CTA | Rol / Sección | Turnos | Tokens In | Tokens Out | Cache Leído | Costo (USD) | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| **Cognitive Task Analysis Architect part_02** | Mapper | 4 | 40,191 | 9,283 | 75,699 | `$0.14` | 0 | **66.0s** |
| **Cognitive Task Analysis Architect part_03** | Mapper | 4 | 43,330 | 11,801 | 79,631 | `$0.16` | 0 | **70.0s** |
| **Cognitive Task Analysis Architect part_01** | Mapper | 5 | 30,677 | 8,701 | 63,761 | `$0.12` | 1 | **68.0s** |
| **CTA Harmonizer** | Harmonizer | 5 | 37,864 | 5,907 | 94,711 | `$0.11` | 0 | **41.0s** |

---

### 3.3. Stage 3: Autoría de Reactivos por Shard y Análisis por Competencia
- **Total de Shards Auditados:** `20 shards concurrentes`
- **Tasa de Aprobación en 1ra Compilación:** **`3/20 (15.0%)`** (Reglas en 1er fallo: `[TPL-VAR]` (8), `[GENERAL]` (6), `[R-19]` (5), `[TPL-CONST-DISTRACTOR]` (5), `[TPL-STATIC-OPT]` (4), `[TPL-DIGIT-PLACEHOLDER-CONCAT]` (2))
- **Duración Mínima de Shard:** `107.0s` | **Mediana:** `133.0s`
- **Tiempo de Pared Máximo (Straggler Crítico):** **`319.0s`** (`5.3 min`) por `Shard Author shard_02`
- **Retraso de Sincronización Impuesto por el Straggler:** **`+186.0s`** frente a la mediana
- **Tokens Promedio por Competencia en Autores:** **`80,310.7 tokens/competencia`**
- **Costo Estimado Etapa 3 (Gemini 4 Hydrogen):** **`$5.33 USD`**

| Shard ID | Competencias Asignadas | Comps | Tokens In | Tokens Out | Cache Leído | Total Activo | Costo (USD) | Tokens / Comp | Turnos | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :--- | :--- | :--- |
| **Shard Author shard_01** | `Hab-01` | 1 | 49,059 | 17,694 | 133,102 | 66,753 | `$0.22` | **66,753.0** | 5 | 0 | **107.0s** |
| **Shard Author shard_13** | `C-04` | 1 | 57,041 | 20,420 | 264,867 | 77,461 | `$0.26` | **77,461.0** | 8 | 1 | **133.0s** |
| **Shard Author shard_14** | `C-05` | 1 | 56,389 | 21,061 | 227,550 | 77,450 | `$0.26` | **77,450.0** | 7 | 1 | **132.0s** |
| **Shard Author shard_02 🛑** | `Hab-02` | 1 | 81,063 | 28,906 | 662,453 | 109,969 | `$0.39` | **109,969.0** | 14 | 2 | **319.0s** |
| **Shard Author shard_15** | `C-06` | 1 | 56,509 | 22,121 | 226,750 | 78,630 | `$0.27` | **78,630.0** | 7 | 1 | **138.0s** |
| **Shard Author shard_03** | `Hab-03` | 1 | 50,888 | 19,655 | 136,351 | 70,543 | `$0.23` | **70,543.0** | 5 | 0 | **111.0s** |
| **Shard Author shard_04** | `Hab-04` | 1 | 54,038 | 22,635 | 142,296 | 76,673 | `$0.26` | **76,673.0** | 5 | 0 | **125.0s** |
| **Shard Author shard_16** | `C-09` | 1 | 96,043 | 18,332 | 177,695 | 114,375 | `$0.29` | **114,375.0** | 7 | 1 | **117.0s** |
| **Shard Author shard_05** | `Hab-05` | 1 | 60,152 | 21,687 | 278,662 | 81,839 | `$0.27` | **81,839.0** | 8 | 1 | **167.0s** |
| **Shard Author shard_17** | `C-10` | 1 | 56,231 | 21,221 | 217,605 | 77,452 | `$0.26` | **77,452.0** | 7 | 1 | **142.0s** |
| **Shard Author shard_18** | `C-11` | 1 | 57,451 | 22,102 | 224,809 | 79,553 | `$0.27` | **79,553.0** | 7 | 1 | **144.0s** |
| **Shard Author shard_06** | `Hab-06` | 1 | 56,622 | 18,997 | 263,331 | 75,619 | `$0.25` | **75,619.0** | 8 | 1 | **143.0s** |
| **Shard Author shard_19** | `C-12` | 1 | 51,061 | 18,701 | 174,719 | 69,762 | `$0.23` | **69,762.0** | 6 | 1 | **110.0s** |
| **Shard Author shard_07** | `Hab-07` | 1 | 63,217 | 27,980 | 244,081 | 91,197 | `$0.32` | **91,197.0** | 7 | 1 | **165.0s** |
| **Shard Author shard_20** | `H-01` | 1 | 52,425 | 20,851 | 175,079 | 73,276 | `$0.25` | **73,276.0** | 6 | 1 | **122.0s** |
| **Shard Author shard_08** | `Hab-08` | 1 | 60,663 | 20,765 | 277,235 | 81,428 | `$0.27` | **81,428.0** | 8 | 1 | **133.0s** |
| **Shard Author shard_09** | `C-07` | 1 | 57,488 | 24,277 | 195,208 | 81,765 | `$0.28` | **81,765.0** | 6 | 1 | **142.0s** |
| **Shard Author shard_10** | `C-01` | 1 | 53,463 | 20,140 | 176,984 | 73,603 | `$0.24` | **73,603.0** | 6 | 1 | **123.0s** |
| **Shard Author shard_11** | `C-02` | 1 | 54,490 | 22,208 | 186,611 | 76,698 | `$0.26` | **76,698.0** | 6 | 1 | **124.0s** |
| **Shard Author shard_12** | `C-03` | 1 | 52,407 | 19,761 | 177,269 | 72,168 | `$0.24` | **72,168.0** | 6 | 1 | **114.0s** |

---

### 3.3b. Stage 3B: Remediación y Repair Engineers (Ingenieros de Reparación)
- **Total de Repair Engineers Desplegados:** `7 subagentes` en **`3 ronda(s)`** (`DONE`: `7`, `BLOCKED`: **`0`**)
- **Duración Mínima:** `34.0s` | **Mediana:** `40.0s` | **Máxima:** `156.0s` (`2.6 min`)
- **Tokens Activos Totales en Reparación:** `373,048 tokens`
- **Costo Estimado Etapa 3B (Gemini 4 Hydrogen):** **`$0.95 USD`**
- **Agente Determinante del Retraso:** `Repair Engineer Hab-07`

| Repair Engineer | Estado | Turnos | Tokens In | Tokens Out | Cache Leído | Total Activo | Costo (USD) | Errores | Duración |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Repair Engineer C-05** | `DONE` | 6 | 57,400 | 6,403 | 173,481 | 63,803 | `$0.15` | 0 | **50.0s** |
| **Repair Engineer C-01** | `DONE` | 5 | 39,375 | 3,504 | 95,767 | 42,879 | `$0.09` | 0 | **35.0s** |
| **Repair Engineer C-03** | `DONE` | 5 | 40,495 | 6,104 | 107,980 | 46,599 | `$0.11` | 0 | **49.0s** |
| **Repair Engineer C-05** | `DONE` | 5 | 38,078 | 4,176 | 103,756 | 42,254 | `$0.10` | 0 | **40.0s** |
| **Repair Engineer C-10** | `DONE` | 5 | 36,070 | 3,338 | 103,982 | 39,408 | `$0.09` | 0 | **34.0s** |
| **Repair Engineer Hab-07** | `DONE` | 7 | 69,529 | 27,221 | 250,973 | 96,750 | `$0.33` | 1 | **156.0s** |
| **Repair Engineer C-05** | `DONE` | 5 | 38,632 | 2,723 | 95,262 | 41,355 | `$0.09` | 0 | **36.0s** |

---

### 3.4. Evaluación y Arbitraje de Blind Judges (Verificación Psicométrica Ciega)

> [!NOTE]
> **Dictamen de Blind Judges:** ⚠️ NO PASÓ AL PRIMER INTENTO — APROBADO POST-REJUDGE (155/155 REACTIVOS)  
> La Ronda 1 de Blind Judges registró 5 discrepancia(s), por lo que no hubo acuerdo limpio al primer intento. Tras correcciones y Rejudge, el resultado final alcanzó 100.0% de acuerdo (0 discrepancias).

| Dimensión de Arbitraje Ciego | Valor Registrado | Observación Técnica |
| :--- | :--- | :--- |
| **Lote Estratificado Ciego** | `155 reactivos` (20 comps × 2) | Lote de evaluación sin soluciones (`judge_batch.json`) |
| **Subagentes Jueces Ciegos** | `19 jueces` | Aislamiento epistémico en Stage 5 |
| **Costo Etapa 5 (Gemini 4 Hydrogen)** | **`$2.24 USD`** | Evaluado sobre los 19 Blind Judges (In: `538,965`, Out: `185,424`, Cache: `531,544`) |
| **Resultado al Primer Intento** | **`❌ Falló al primer intento`** | Ronda 1: 5 discrepancia(s) (`flaw_detected`: 5, `kernel_override`: 6); 0 violaciones iniciales |
| **Resultado Final Post-Rejudge** | **`✅ Aprobado`** | `100.0%` acuerdo, `0` discrepancia(s) |
| **Iteraciones de Auto-Reparación** | `0 iteraciones` en sandbox | 0 iteraciones ejecutadas |
| **Intervenciones del Supervisor** | 🛠️ `0 operaciones directas` | Ninguna (ejecución autónoma) |

#### Detalle de Acciones Registradas:
- 1. **Ronda 1 (`judge_report_round_1.json` / `rounds_history`)**: 5 discrepancia(s) detectada(s).
- 2. **Bucle de Auto-Reparación / Rejudge**: 5 ola(s) de jueces ejecutada(s) (0 intervenciones de supervisor).
- 3. **Resultado Final Post-Rejudge (`judge_report.json`)**: ✅ Aprobado (`100.0% agreement rate`, `0 discrepancias` sobre 155 reactivos).

---

## 4. Auditoría Forense del Orquestador y Catálogo de Intervenciones Manuales

### 4.1. Descomposición del Tiempo y Costo del Orquestador
- 💵 **Costo Estimado del Orquestador Principal (Gemini 4 Hydrogen):** **`$0.83 USD`** (In: `258,049`, Out: `45,607`, Cache: `1,408,527`)
- ⏱️ **Tiempo Total de Pared del Orquestador:** `23.78 min` (`1427.0s`)
- 💻 **Tiempo Activo Ejecutando Comandos CLI (`run.py`):** `0.6 min` (`36.0s`)
- 🛠️ **Tiempo Gastado en Intervenciones Manuales (Supervisor Repair):** **`0.0 min`** (`0.0s`)
- ⏳ **Tiempo Ocioso en Barreras de Sincronización (Esperando Subagentes):** `18.45 min` (`1107.0s`)
- 🧠 **Tiempo de Inferencia y Razonamiento del Modelo:** `1.07 min` (`64.0s`)

### 4.2. Catálogo Cronológico de Reparaciones Manuales del Orquestador
Operaciones directas de edición de código ejecutadas por el orquestador: **`0`**

| Paso | Archivo Afectado | Tipo de Acción | Causa Raíz / Justificación Técnica | Herramienta | Tokens Paso |
| :---: | :--- | :--- | :--- | :--- | :--- |
| — | *Ninguna intervención registrada* | — | — | — | 0 |

---

## 5. Diagnóstico de Cuellos de Botella y Antipatrones Detectados

### 🛑 [HIGH] Straggler Crítico en Shards: Shard Author shard_02
- **Ámbito:** `Stage 3: Question Authoring`
- **Diagnóstico:** Shard Author shard_02 tardó 319.0s frente a la mediana de 133.0s (+186.0s de retraso en la barrera). Determinó el tiempo total de pared de la etapa de autoría.

---

## 6. Telemetría de Razonamiento Cognitivo (Thinking Traces)

- **Total de Turnos con Razonamiento:** `103 turnos`
- **Volumen Total de Razonamiento:** `412,889 caracteres`
- **Razonamiento del Orquestador:** `8 turnos` (2,658 chars)
- **Razonamiento de Subagentes:** `95 turnos` (410,231 chars)

| Agente / Subagente | Turnos de Thinking | Caracteres de Thinking | Trazas de Error Capturadas |
| :--- | :---: | :---: | :---: |
| **Repair Engineer C-05** | 4 | 5,589 | 0 |
| **Blind Judge 01** | 1 | 4,835 | 0 |
| **Cognitive Task Analysis Architect part_02** | 3 | 3,486 | 0 |
| **Cognitive Task Analysis Architect part_03** | 3 | 5,893 | 0 |
| **Cognitive Task Analysis Architect part_01** | 4 | 3,555 | ⚠️ 1 |
| **CTA Harmonizer** | 1 | 4,670 | 0 |
| **Shard Author shard_01** | 2 | 8,946 | 0 |
| **Shard Author shard_13** | 3 | 9,285 | ⚠️ 1 |
| **Shard Author shard_14** | 2 | 10,412 | ⚠️ 1 |
| **Shard Author shard_02** | 3 | 17,837 | ⚠️ 2 |
| **Shard Author shard_15** | 2 | 8,963 | ⚠️ 1 |
| **Shard Author shard_03** | 2 | 10,685 | 0 |
| **Shard Author shard_04** | 2 | 10,495 | 0 |
| **Shard Author shard_16** | 3 | 8,043 | ⚠️ 1 |
| **Shard Author shard_05** | 2 | 12,472 | ⚠️ 1 |
| **Shard Author shard_17** | 2 | 8,218 | ⚠️ 1 |
| **Shard Author shard_18** | 2 | 9,344 | ⚠️ 1 |
| **Shard Author shard_06** | 2 | 6,723 | ⚠️ 1 |
| **Shard Author shard_19** | 2 | 8,125 | ⚠️ 1 |
| **Shard Author shard_07** | 2 | 17,565 | ⚠️ 1 |
| **Shard Author shard_20** | 3 | 10,225 | ⚠️ 1 |
| **Shard Author shard_08** | 3 | 10,500 | ⚠️ 1 |
| **Shard Author shard_09** | 2 | 11,208 | ⚠️ 1 |
| **Shard Author shard_10** | 2 | 7,299 | ⚠️ 1 |
| **Shard Author shard_11** | 2 | 9,451 | ⚠️ 1 |
| **Shard Author shard_12** | 2 | 8,286 | ⚠️ 1 |
| **Blind Judge 01** | 1 | 8,846 | 0 |
| **Blind Judge 03** | 1 | 12,268 | 0 |
| **Blind Judge 02** | 1 | 14,956 | 0 |
| **Blind Judge 04** | 1 | 11,038 | 0 |
| **Blind Judge 05** | 1 | 10,715 | 0 |
| **Blind Judge 06** | 1 | 7,972 | 0 |
| **Blind Judge 07** | 1 | 15,922 | 0 |
| **Blind Judge 08** | 1 | 8,684 | 0 |
| **Blind Judge 09** | 1 | 10,728 | 0 |
| **Blind Judge 01** | 1 | 8,809 | 0 |
| **Repair Engineer C-01** | 3 | 2,738 | 0 |
| **Repair Engineer C-03** | 3 | 4,088 | 0 |
| **Repair Engineer C-05** | 3 | 2,315 | 0 |
| **Repair Engineer C-10** | 2 | 2,275 | 0 |
| **Repair Engineer Hab-07** | 4 | 11,760 | ⚠️ 1 |
| **Blind Judge 02** | 1 | 7,041 | 0 |
| **Blind Judge 01** | 1 | 7,211 | 0 |
| **Blind Judge 03** | 1 | 7,377 | 0 |
| **Blind Judge 04** | 2 | 8,364 | 0 |
| **Blind Judge 05** | 1 | 7,540 | 0 |
| **Repair Engineer C-05** | 2 | 1,899 | 0 |
| **Blind Judge 01** | 1 | 5,575 | 0 |
| **Blind Judge 01** | 0 | 0 | 0 |
| **Blind Judge 01** | 0 | 0 | 0 |

---
*Reporte forense determinista emitido por `c2c-run-auditor`.*