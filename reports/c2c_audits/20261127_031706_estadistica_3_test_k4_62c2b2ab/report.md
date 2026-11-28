# Informe de Auditoría Arquitectónica Forense: Rendimiento, Shards y Telemetría Multi-Agente
## Curso: Estadistica 3 Test K4 (`estadistica_3_test_k4`)

**Fecha de Auditoría:** `2026-11-27 08:17:06 UTC`  
**Conversación Orquestadora:** [`62c2b2ab-4c50-41eb-a0fd-530f02aa3ab6`](conversation://62c2b2ab-4c50-41eb-a0fd-530f02aa3ab6)  
**Directorio de Trabajo Validado (Zero-Collision):** `D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_test_k4\work` (`match=True`)  
**Enfoque:** Telemetría Determinista de API, Subagentes, Shards, Latencias, Costos USD (Gemini 4 Hydrogen) y Operaciones del Orquestador.

---

## 1. Consolidación de Métricas y Caracterización de Carga

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada** | `3 archivos` (43 págs / 1.56 MB) | 01_measure_theory_bridge.pdf, 02_stat110_lec27_conditional_expectation.pdf, 03_rincon_cl_caps1_2.pdf |
| **Requerimiento de Visión** | `0 páginas` (0 handouts) | Cuadrículas generadas para diagramas/fórmulas |
| **Corpus Sintetizado** | `0 caracteres` (0 palabras) | Texto consolidado tras ingesta y visión |
| **Competencias Extraídas** | **`23 competencias`** | Desglose pedagógico (Hechos, Conceptos, Habilidades) |
| **Shards Particionados** | **`23 shards`** | Unidades de trabajo concurrentes |
| **Subagentes Desplegados** | **`48 subagentes`** | Visión (0), CTA (4), Autores (23), Repairs (7), Jueces (14) |
| **Reactivos Finales Validados** | **`948 preguntas`** | Evaluadas en sandbox |
| **Tokens Entrada (Subagentes)** | **`2,425,903` tokens** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`809,259` tokens** | Código de plantillas y JSON generado |
| **Tokens Caché (Leídos)** | **`8,201,692` tokens** | Caché de contexto reutilizado por la API |
| **Gran Total Tokens Activos** | **`3,412,928` tokens** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`11,614,620` tokens** | Consumo total de cuota facturable |
| **Costo Estimado Total (Gemini 4 Hydrogen)** | **`$10.67 USD`** | In: `$3.89` (`$1.50/1M`), Out+Think: `$6.16` (`$7.50/1M`), Cache: `$0.62` (`$0.08/1M`) |

---

## 2. Ratios Unitarios Normalizados (Unit Economics)

Métricas normalizadas para comparación *apples-to-apples* frente a cursos de diferente volumen de contenido:

| Métrica Unitaria | Valor Obtenido | Interpretación de Eficiencia |
| :--- | :--- | :--- |
| **Tokens Totales por Pregunta** | **`12,251.7 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`3,600.1 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`504,983.5 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`91,998.0 tokens/comp`** | Costo puro de la etapa de autoría por competencia |
| **Tokens Totales por Página / Slide** | **`270,107.4 tokens/pág`** | Esfuerzo cognitivo por diapositiva original |
| **Costo Estimado por Pregunta (Hydrogen)** | **`$0.01 USD/preg`** | Costo monetario valorizado por reactivo |
| **Costo Estimado por Competencia (Hydrogen)** | **`$0.46 USD/comp`** | Costo monetario valorizado por competencia |
| **Segundos de Pared por Pregunta** | **`1.75 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`34.29 preg/min`** | Velocidad de producción del pipeline |
| **Factor de Aceleración Paralela** | **`3.74x`** | Relación tiempo cómputo vs tiempo de pared |

---

## 3. Desglose Forense por Etapas Críticas

### 3.0a. Valorización Monetaria por Etapa (Tarifas Gemini 4 Hydrogen)
> Tarifas oficiales aplicables: Entrada `$1.50/1M`, Caché leído `$0.08/1M`, Salida (incl. thinking) `$7.50/1M`.

| Etapa / Rol | Agentes | Tokens Entrada | Tokens Salida | Caché Leído | Costo Estimado (USD) | % del Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Stage 1A: Visión** | 0 | 0 | 0 | 0 | **`$0.00`** | 0.0% |
| **Stage 1B: CTA Architects** | 4 | 168,604 | 36,850 | 429,958 | **`$0.56`** | 5.2% |
| **Stage 3: Shard Authors** | 23 | 1,512,394 | 603,561 | 5,743,558 | **`$7.23`** | 67.8% |
| **Stage 3B: Repair Engineers** | 7 | 344,634 | 38,997 | 860,167 | **`$0.87`** | 8.2% |
| **Stage 5: Blind Judges** | 14 | 400,271 | 129,851 | 408,249 | **`$1.60`** | 15.0% |
| **Orquestador Principal (Director)** | 1 | 165,224 | 12,542 | 759,760 | **`$0.40`** | 3.7% |
| **TOTAL CORRIDA (Gemini 4 Hydrogen)** | **49** | **2,591,127** | **821,801** | **8,201,692** | **`$10.67 USD`** | **100.0%** |

### 3.0. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json` & `state.json`)
- **Snapshots de Etapa Verificados (`conversation_id` = `62c2b2ab`):** `9 etapas`
- **Estado Maestro (`work/state.json`):** `completed` (Etapa actual/final: `publish`)

| Etapa (Snapshot) | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes Capturados | Artefactos / Metadatos de Etapa |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`00_prepare`** | `2026-11-27 07:45:44` | `0.03s` | `0` (`0` act) | 0 | `—` |
| **`00b_bootstrap`** | `2026-11-27 07:45:44` | `0.08s` | `0` (`0` act) | 0 | `lock_file=D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_test_k4\work\.c2c_subagent_lock.json` |
| **`01_cta`** | `2026-11-27 07:48:29` | `1.05s` | `0` (`0` act) | 0 | `competencies=23` |
| **`02_shard`** | `2026-11-27 07:48:30` | `0.04s` | `0` (`0` act) | 0 | `shards=23` |
| **`03_templates`** | `2026-11-27 08:12:20` | `0.58s` | `0` (`0` act) | 0 | `count=23` |
| **`04_build`** | `2026-11-27 08:12:28` | `7.39s` | `0` (`0` act) | 0 | `total_questions=948` |
| **`05_verify`** | `2026-11-27 08:12:30` | `1.93s` | `0` (`0` act) | 0 | `verified_course_path=D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_test_k4\work\course_verified.json` |
| **`05b_judge_compare`** | `2026-11-27 08:02:06` | `0.12s` | `0` (`0` act) | 0 | `passed=False` |
| **`06_publish`** | `2026-11-27 08:12:39` | `4.01s` | `0` (`0` act) | 0 | `published_json=D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_test_k4.json` |

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
- **Tiempo de Pared Fase Mappers (Máximo):** **`121.0s`** (determinado por `Cognitive Task Analysis Architect part_03`)
- **Tiempo Fase Harmonizer (Barrera Síncrona):** **`34.0s`**
- **Tiempo de Pared Total de Etapa 1B:** **`155.0s`** (`2.6 min`)
- **Costo Estimado Etapa 1B (Gemini 4 Hydrogen):** **`$0.56 USD`**

| Subagente CTA | Rol / Sección | Turnos | Tokens In | Tokens Out | Cache Leído | Costo (USD) | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| **Cognitive Task Analysis Architect part_03** | Mapper | 6 | 57,213 | 14,234 | 191,029 | `$0.21` | 1 | **121.0s** |
| **Cognitive Task Analysis Architect part_01** | Mapper | 4 | 39,176 | 8,179 | 75,590 | `$0.13` | 0 | **65.0s** |
| **Cognitive Task Analysis Architect part_02** | Mapper | 4 | 40,986 | 11,014 | 76,268 | `$0.15` | 0 | **71.0s** |
| **CTA Harmonizer** | Harmonizer | 5 | 31,229 | 3,423 | 87,071 | `$0.08` | 0 | **34.0s** |

---

### 3.3. Stage 3: Autoría de Reactivos por Shard y Análisis por Competencia
- **Total de Shards Auditados:** `23 shards concurrentes`
- **Tasa de Aprobación en 1ra Compilación:** **`10/23 (43.48%)`** (Reglas en 1er fallo: `[INVARIANT]` (3), `[TPL-STEM-EQUATION-PARITY]` (3), `[R-15-MS]` (3), `[TPL-DEGENERATE-LITERAL-COND]` (2), `[TPL-DYNAMIC-RATIONALE]` (2), `[TPL-D4]` (2))
- **Duración Mínima de Shard:** `83.0s` | **Mediana:** `120.0s`
- **Tiempo de Pared Máximo (Straggler Crítico):** **`317.0s`** (`5.3 min`) por `Shard Author shard_13`
- **Retraso de Sincronización Impuesto por el Straggler:** **`+197.0s`** frente a la mediana
- **Tokens Promedio por Competencia en Autores:** **`91,998.0 tokens/competencia`**
- **Costo Estimado Etapa 3 (Gemini 4 Hydrogen):** **`$7.23 USD`**

| Shard ID | Competencias Asignadas | Comps | Tokens In | Tokens Out | Cache Leído | Total Activo | Costo (USD) | Tokens / Comp | Turnos | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :--- | :--- | :--- |
| **Shard Author shard_01** | `Hab-01` | 1 | 56,252 | 22,968 | 105,190 | 79,220 | `$0.26` | **79,220.0** | 4 | 0 | **120.0s** |
| **Shard Author shard_02** | `Hab-02` | 1 | 84,735 | 44,473 | 400,132 | 129,208 | `$0.49` | **129,208.0** | 8 | 2 | **221.0s** |
| **Shard Author shard_03** | `Hab-03` | 1 | 75,041 | 30,601 | 370,082 | 105,642 | `$0.37` | **105,642.0** | 8 | 1 | **163.0s** |
| **Shard Author shard_04** | `Hab-04` | 1 | 55,971 | 23,482 | 106,004 | 79,453 | `$0.27` | **79,453.0** | 4 | 0 | **108.0s** |
| **Shard Author shard_05** | `Hab-05` | 1 | 56,753 | 24,391 | 107,056 | 81,144 | `$0.28` | **81,144.0** | 4 | 0 | **115.0s** |
| **Shard Author shard_06** | `Hab-06` | 1 | 72,367 | 34,927 | 244,045 | 107,294 | `$0.39` | **107,294.0** | 6 | 1 | **184.0s** |
| **Shard Author shard_07** | `Hab-07` | 1 | 69,682 | 32,506 | 243,886 | 102,188 | `$0.37` | **102,188.0** | 6 | 1 | **155.0s** |
| **Shard Author shard_08** | `Hab-08` | 1 | 74,450 | 30,536 | 301,402 | 104,986 | `$0.36` | **104,986.0** | 7 | 1 | **158.0s** |
| **Shard Author shard_09** | `Hab-09` | 1 | 83,471 | 39,349 | 497,074 | 122,820 | `$0.46` | **122,820.0** | 10 | 3 | **218.0s** |
| **Shard Author shard_13 🛑** | `C-06` | 1 | 102,171 | 51,121 | 957,804 | 153,292 | `$0.61` | **153,292.0** | 16 | 6 | **317.0s** |
| **Shard Author shard_14** | `C-01` | 1 | 48,676 | 17,058 | 97,924 | 65,734 | `$0.21` | **65,734.0** | 4 | 0 | **84.0s** |
| **Shard Author shard_15** | `C-02` | 1 | 47,803 | 16,027 | 96,906 | 63,830 | `$0.20` | **63,830.0** | 4 | 0 | **83.0s** |
| **Shard Author shard_16** | `C-03` | 1 | 69,258 | 22,576 | 537,637 | 91,834 | `$0.31` | **91,834.0** | 12 | 3 | **157.0s** |
| **Shard Author shard_17** | `C-07` | 1 | 51,225 | 19,115 | 99,890 | 70,340 | `$0.23` | **70,340.0** | 4 | 0 | **94.0s** |
| **Shard Author shard_18** | `C-08` | 1 | 48,431 | 16,692 | 97,646 | 65,123 | `$0.21` | **65,123.0** | 4 | 0 | **87.0s** |
| **Shard Author shard_10** | `Hab-10` | 1 | 70,332 | 32,894 | 225,317 | 103,226 | `$0.37` | **103,226.0** | 6 | 1 | **174.0s** |
| **Shard Author shard_11** | `C-04` | 1 | 51,555 | 19,360 | 100,757 | 70,915 | `$0.23` | **70,915.0** | 4 | 0 | **95.0s** |
| **Shard Author shard_12** | `C-05` | 1 | 55,845 | 20,783 | 196,420 | 76,628 | `$0.25` | **76,628.0** | 6 | 1 | **119.0s** |
| **Shard Author shard_19** | `C-09` | 1 | 51,051 | 19,525 | 100,375 | 70,576 | `$0.23` | **70,576.0** | 4 | 0 | **107.0s** |
| **Shard Author shard_20** | `C-10` | 1 | 48,533 | 16,839 | 97,627 | 65,372 | `$0.21` | **65,372.0** | 4 | 0 | **96.0s** |
| **Shard Author shard_21** | `C-11` | 1 | 119,061 | 26,239 | 272,454 | 145,300 | `$0.40` | **145,300.0** | 8 | 2 | **167.0s** |
| **Shard Author shard_22** | `C-12` | 1 | 59,888 | 18,871 | 281,767 | 78,759 | `$0.25` | **78,759.0** | 8 | 2 | **123.0s** |
| **Shard Author shard_23** | `C-13` | 1 | 59,843 | 23,228 | 206,163 | 83,071 | `$0.28` | **83,071.0** | 6 | 1 | **118.0s** |

---

### 3.3b. Stage 3B: Remediación y Repair Engineers (Ingenieros de Reparación)
- **Total de Repair Engineers Desplegados:** `7 subagentes` en **`4 ronda(s)`** (`DONE`: `7`, `BLOCKED`: **`0`**)
- **Duración Mínima:** `41.0s` | **Mediana:** `55.0s` | **Máxima:** `61.0s` (`1.0 min`)
- **Tokens Activos Totales en Reparación:** `383,631 tokens`
- **Costo Estimado Etapa 3B (Gemini 4 Hydrogen):** **`$0.87 USD`**
- **Agente Determinante del Retraso:** `Repair Engineer C-09`

| Repair Engineer | Estado | Turnos | Tokens In | Tokens Out | Cache Leído | Total Activo | Costo (USD) | Errores | Duración |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Repair Engineer C-09** | `DONE` | 5 | 42,689 | 5,627 | 114,763 | 48,316 | `$0.11` | 0 | **43.0s** |
| **Repair Engineer C-05** | `DONE` | 7 | 81,086 | 5,396 | 148,893 | 86,482 | `$0.17` | 1 | **56.0s** |
| **Repair Engineer C-09** | `DONE` | 5 | 45,269 | 6,208 | 105,915 | 51,477 | `$0.12` | 0 | **61.0s** |
| **Repair Engineer C-10** | `DONE` | 5 | 41,909 | 4,672 | 100,160 | 46,581 | `$0.11` | 0 | **41.0s** |
| **Repair Engineer C-13** | `DONE` | 6 | 48,068 | 5,466 | 159,722 | 53,534 | `$0.13` | 0 | **45.0s** |
| **Repair Engineer C-09** | `DONE` | 5 | 45,260 | 8,123 | 117,506 | 53,383 | `$0.14` | 0 | **55.0s** |
| **Repair Engineer C-09** | `DONE` | 5 | 40,353 | 3,505 | 113,208 | 43,858 | `$0.10` | 0 | **55.0s** |

---

### 3.4. Evaluación y Arbitraje de Blind Judges (Verificación Psicométrica Ciega)

> [!NOTE]
> **Dictamen de Blind Judges:** ⚠️ NO PASÓ AL PRIMER INTENTO — APROBADO POST-REJUDGE (145/145 REACTIVOS)  
> La Ronda 1 de Blind Judges registró 3 discrepancia(s), por lo que no hubo acuerdo limpio al primer intento. Tras correcciones y Rejudge, el resultado final alcanzó 100.0% de acuerdo (0 discrepancias).

| Dimensión de Arbitraje Ciego | Valor Registrado | Observación Técnica |
| :--- | :--- | :--- |
| **Lote Estratificado Ciego** | `145 reactivos` (23 comps × 2) | Lote de evaluación sin soluciones (`judge_batch.json`) |
| **Subagentes Jueces Ciegos** | `14 jueces` | Aislamiento epistémico en Stage 5 |
| **Costo Etapa 5 (Gemini 4 Hydrogen)** | **`$1.60 USD`** | Evaluado sobre los 14 Blind Judges (In: `400,271`, Out: `129,851`, Cache: `408,249`) |
| **Resultado al Primer Intento** | **`❌ Falló al primer intento`** | Ronda 1: 3 discrepancia(s) (`flaw_detected`: 0, `kernel_override`: 1); 0 violaciones iniciales |
| **Resultado Final Post-Rejudge** | **`✅ Aprobado`** | `100.0%` acuerdo, `0` discrepancia(s) |
| **Iteraciones de Auto-Reparación** | `0 iteraciones` en sandbox | 0 iteraciones ejecutadas |
| **Intervenciones del Supervisor** | 🛠️ `0 operaciones directas` | Ninguna (ejecución autónoma) |

#### Detalle de Acciones Registradas:
- 1. **Ronda 1 (`judge_report_round_1.json` / `rounds_history`)**: 3 discrepancia(s) detectada(s).
- 2. **Bucle de Auto-Reparación / Rejudge**: 6 ola(s) de jueces ejecutada(s) (0 intervenciones de supervisor).
- 3. **Resultado Final Post-Rejudge (`judge_report.json`)**: ✅ Aprobado (`100.0% agreement rate`, `0 discrepancias` sobre 145 reactivos).

---

## 4. Auditoría Forense del Orquestador y Catálogo de Intervenciones Manuales

### 4.1. Descomposición del Tiempo y Costo del Orquestador
- 💵 **Costo Estimado del Orquestador Principal (Gemini 4 Hydrogen):** **`$0.40 USD`** (In: `165,224`, Out: `12,542`, Cache: `759,760`)
- ⏱️ **Tiempo Total de Pared del Orquestador:** `27.65 min` (`1659.0s`)
- 💻 **Tiempo Activo Ejecutando Comandos CLI (`run.py`):** `0.13 min` (`8.0s`)
- 🛠️ **Tiempo Gastado en Intervenciones Manuales (Supervisor Repair):** **`0.0 min`** (`0.0s`)
- ⏳ **Tiempo Ocioso en Barreras de Sincronización (Esperando Subagentes):** `24.52 min` (`1471.0s`)
- 🧠 **Tiempo de Inferencia y Razonamiento del Modelo:** `0.9 min` (`54.0s`)

### 4.2. Catálogo Cronológico de Reparaciones Manuales del Orquestador
Operaciones directas de edición de código ejecutadas por el orquestador: **`0`**

| Paso | Archivo Afectado | Tipo de Acción | Causa Raíz / Justificación Técnica | Herramienta | Tokens Paso |
| :---: | :--- | :--- | :--- | :--- | :--- |
| — | *Ninguna intervención registrada* | — | — | — | 0 |

### 4.3. Fricciones de Orquestación, Hooks y Gobernanza Híbrida
- **Denegaciones de Pre-Tool Hooks:** `1` (Pasos: 40)
- **Llamadas Malformadas (`Malformed function call`):** `1` (Pasos: 57)
- **Gobernanza Híbrida (`run_workflow` + `invoke_subagent` legado):** `No` (`run_workflow`: 5, `invoke_subagent`: 0, `manage_subagents(kill*)`: 0)

---

## 5. Diagnóstico de Cuellos de Botella y Antipatrones Detectados

### 🛑 [HIGH] Straggler Crítico en Shards: Shard Author shard_13
- **Ámbito:** `Stage 3: Question Authoring`
- **Diagnóstico:** Shard Author shard_13 tardó 317.0s frente a la mediana de 120.0s (+197.0s de retraso en la barrera). Determinó el tiempo total de pared de la etapa de autoría.

### ⚠️ [MEDIUM] Fricción de Herramientas en 3 subagentes
- **Ámbito:** `Multiple Subagents`
- **Diagnóstico:** Subagentes como Shard Author shard_09 acumularon fallos en consola (3 errores), provocando reintentos e invalidación de caché.

---

## 6. Telemetría de Razonamiento Cognitivo (Thinking Traces)

- **Total de Turnos con Razonamiento:** `92 turnos`
- **Volumen Total de Razonamiento:** `189,009 caracteres`
- **Razonamiento del Orquestador:** `12 turnos` (3,672 chars)
- **Razonamiento de Subagentes:** `80 turnos` (185,337 chars)

| Agente / Subagente | Turnos de Thinking | Caracteres de Thinking | Trazas de Error Capturadas |
| :--- | :---: | :---: | :---: |
| **Repair Engineer C-09** | 1 | 2,066 | 0 |
| **Blind Judge 01** | 1 | 1,291 | 0 |
| **Cognitive Task Analysis Architect part_03** | 3 | 2,568 | ⚠️ 1 |
| **Cognitive Task Analysis Architect part_01** | 2 | 1,199 | 0 |
| **Cognitive Task Analysis Architect part_02** | 2 | 2,296 | 0 |
| **CTA Harmonizer** | 1 | 1,499 | 0 |
| **Shard Author shard_01** | 1 | 5,310 | 0 |
| **Shard Author shard_02** | 3 | 8,933 | ⚠️ 2 |
| **Shard Author shard_03** | 3 | 6,783 | ⚠️ 1 |
| **Shard Author shard_04** | 1 | 5,019 | 0 |
| **Shard Author shard_05** | 1 | 5,332 | 0 |
| **Shard Author shard_06** | 2 | 8,135 | ⚠️ 1 |
| **Shard Author shard_07** | 2 | 6,292 | ⚠️ 1 |
| **Shard Author shard_08** | 2 | 6,442 | ⚠️ 1 |
| **Shard Author shard_09** | 4 | 8,223 | ⚠️ 3 |
| **Shard Author shard_13** | 7 | 5,446 | ⚠️ 6 |
| **Shard Author shard_14** | 1 | 1,726 | 0 |
| **Shard Author shard_15** | 1 | 1,662 | 0 |
| **Shard Author shard_16** | 2 | 2,411 | ⚠️ 3 |
| **Shard Author shard_17** | 1 | 2,482 | 0 |
| **Shard Author shard_18** | 1 | 2,024 | 0 |
| **Shard Author shard_10** | 2 | 5,840 | ⚠️ 1 |
| **Shard Author shard_11** | 1 | 1,813 | 0 |
| **Shard Author shard_12** | 2 | 2,851 | ⚠️ 1 |
| **Shard Author shard_19** | 1 | 2,570 | 0 |
| **Shard Author shard_20** | 1 | 2,478 | 0 |
| **Shard Author shard_21** | 3 | 3,356 | ⚠️ 2 |
| **Shard Author shard_22** | 3 | 2,069 | ⚠️ 2 |
| **Shard Author shard_23** | 2 | 2,609 | ⚠️ 1 |
| **Blind Judge 01** | 1 | 5,023 | 0 |
| **Blind Judge 02** | 1 | 4,449 | 0 |
| **Blind Judge 03** | 1 | 4,319 | 0 |
| **Blind Judge 04** | 1 | 5,006 | 0 |
| **Blind Judge 05** | 1 | 4,626 | 0 |
| **Blind Judge 06** | 1 | 5,197 | 0 |
| **Blind Judge 07** | 1 | 6,551 | 0 |
| **Blind Judge 08** | 1 | 7,167 | 0 |
| **Blind Judge 09** | 1 | 7,935 | 0 |
| **Blind Judge 01** | 1 | 902 | 0 |
| **Repair Engineer C-05** | 2 | 1,727 | ⚠️ 1 |
| **Repair Engineer C-09** | 2 | 2,634 | 0 |
| **Repair Engineer C-10** | 1 | 1,884 | 0 |
| **Repair Engineer C-13** | 2 | 2,114 | 0 |
| **Blind Judge 01** | 1 | 6,413 | 0 |
| **Repair Engineer C-09** | 1 | 2,339 | 0 |
| **Blind Judge 01** | 1 | 2,637 | 0 |
| **Repair Engineer C-09** | 2 | 1,528 | 0 |
| **Blind Judge 01** | 1 | 2,161 | 0 |

---
*Reporte forense determinista emitido por `c2c-run-auditor`.*

---

## 7. Anexo Forense de Causa Raíz (Auditoría Agéntica Profunda — Modo 2)

### 7.1. Causa Raíz del Straggler Crítico `Author Shard 13` (`317.0s`): Ceguera de `template_id` en `[R-15-MS]`
El análisis verbatim de `transcript.jsonl` de `shard_13` (`606370ac-59bb-477d-a6ae-ec8415a6bb87`) revela que los **4 fallos consecutivos de `[R-15-MS]`** (pasos 18, 22, 27 y 32; `238.0s` de post-compilación) fueron provocados por un **defecto de observabilidad en el validador**:
- **Evidencia verbatim del error (Pasos 18, 22, 27, 32):**
  > `• [R-15-MS] courses/estadistica_3_test_k4/work/.check_attempts/_staged_templates/shard_13/templates/C-06.json:L1 [Tupla en shard_13_data.py: Líneas 600..605] -> Causa: ... (avg_true=111.5 vs avg_false=139.7, ratio=0.80x < 0.80x)`
  El mensaje apunta a `C-06.json:L1` y a la tupla global `600..605`, **omitiendo el `template_id` (`T-C06-11`)**.
- **Bucle ciego resultante en `shard_13`:**
  - **Paso 19:** El agente atribuyó erróneamente `111.5 vs 139.7` a `gen_10` (`T-C06-10`) y lo editó, desbalanceando `gen_10` a `1.42x > 1.20x` (Paso 22).
  - **Paso 23 y Paso 28:** Editó `gen_10` y `gen_12` simultáneamente sin tocar `gen_11`, manteniendo vivo el fallo original `111.5 vs 139.7` en los Pasos 27 y 32.
  - **Paso 33:** Recién al analizar el denominador de `.5` (*"Tracing `gen_11` reveals four true options averaging precisely 111.5 characters"*), identificó que el culpable era **`T-C06-11` (`gen_11`)** y lo corrigió en un solo intento.

### 7.2. Cadena Forense Completa de `C-09` (`T-C09-02`), Reinicio del Servidor y Desperdicio Real
La reconstrucción cronológica cruzando el transcript del orquestador (`62c2b2ab`), los 4 `Repair Engineer C-09` y los 4 `Blind Judge 01` explica por qué hubo 4 rondas:

1. **`task-10` (`full_pipeline`, `07:45:44–08:02:45Z`):** Completó 23/23 autores, 948 preguntas, 9/9 jueces de Ronda 1 y LQAS. `gates` falló (`exit code 1`) con `4` competencias: `C-05`, `C-09`, `C-10`, `C-13`.
2. **`task-15` (`repair_and_rejudge`, `08:02:45–08:05:15Z`):** `Repair C-09 (d09a638b)` editó `T-C09-02` porque el juez había omitido la opción `'A'`. `C-05`, `C-10` y `C-13` pasaron `gates`, pero `Blind Judge 01 (8a12fc4a)` volvió a discrepar en `C-09` por ambigüedad de estacionariedad en el stem (`gates` exit code 1).
3. **`task-21` (`repair_and_rejudge` C-09, `08:05:15–08:07:09Z`) — Interrumpida por Reinicio:** `Repair C-09 (29abb86d)` (`08:05:23–08:06:18`, `$0.14`) y `Blind Judge 01 (befbb56d)` (`08:06:32–08:06:54`, `$0.06`) **sí terminaron**, pero a las `08:07:08Z` ocurrió un **reinicio del servidor** (*`[Notice] All your background tasks have been stopped due to server restart`*) antes de que `task-21` cerrara `gates`, dejando un lock huérfano de tarea activa.
4. **`task-26` (`repair_and_rejudge` C-09 sin `force_repair`, `08:07:09–08:09:01Z`):** El orquestador relanzó el workflow inmediatamente tras el reinicio sin leer `repair_matrix.json` ni activar `force_repair`. Como resultado, `Repair C-09 (fdebc54a)` (`$0.10`) observó en su thinking un estado inconsistente residual (*"missing responses from the blind judge... suspecting an intermittent API timeout"*), aplicó solo 2 ediciones menores y `Blind Judge 01 (d3f19e84)` (`$0.05`) volvió a fallar `gates`.
5. **`task-33` (`repair_and_rejudge` con `force_repair=true`, `08:09:05–08:10:40Z`):** El orquestador leyó `repair_matrix.json`, diagnosticó el estado stale (*"repair_and_rejudge omitted a forced update, leaving stale state cached"*) y activó `"force_repair": true`. `Repair C-09 (c5425c97)` (`$0.11`) corrigió las definiciones faltantes del proceso de Lévy en `S2`/`S4` de `T-C09-02`, y `Blind Judge 01 (ec09ce6e)` (`$0.05`) aprobó `100%` en `18.0s`.
6. **Secuela en Paso 40 (`08:10:45Z`):** El Pre-Tool Hook (*Barrera de Consolidación*) denegó `--stage certify` por la tarea huérfana `task-21` del reinicio; el orquestador verificó `manage_task(list)` y certificó/publicó a las `08:12:39Z`.

- **Impacto Real Desperdiciado (`task-21` + `task-26` + `task-33` extra):** **`323s` (`5.38 min`, `19.5%` del tiempo de pared total)** y **`$0.51 USD`** directos en subagentes redundantes (sin contar tokens del orquestador en los 3 relanzamientos).

### 7.3. Anatomía de `T-C05-03`: `kernel_override` Enmascarado vs LQAS `0/2`
- **Ronda 1 (`judge_report_baseline.json`):** `round_1_flaw_detected_count = 0`, `round_1_kernel_override_count = 1` (`T-C05-03_judge_1`, `proof_dag`: *"Kernel verified constructive proof overrides LLM calculation disagreement"*).
- **Stage 5B LQAS (`judge_report_lqas.json`):** Al escalar `T-C05-03` a confirmación LQAS (`Blind Judge 01 e1437ac9`), **2 de 2 ítems fallaron** (`agreement_rate = 0.0`) por `"proof_dag justifications mismatch"`. El `kernel_override` había enmascarado un banco de justificaciones incompleto/ambiguo, resuelto posteriormente por `Repair Engineer C-05 (fe3b26ed)` en `shard_12_data.py` (con 1 fallo previo `[TPL-M20-PROOF-DAG], [TPL-ASM]` antes de expandir las claves de justificación).

### 7.4. Anomalías de Telemetría en el Reporte Determinista (`audit_engine.py`)
1. **Snapshots `work/telemetry/*.json` en `0` tokens:** Los 9 snapshots reportan `0` tokens y `0` subagentes porque `run_workflow` ejecuta las olas fuera de `run.py`; `audit_engine.py` compensa reconstruyendo los `11,614,620` tokens directamente desde los transcripts.
2. **Corpus Sintetizado `0 caracteres`:** Esperado al haber `0` páginas de Visión (los CTA Mappers leyeron los 3 PDFs directamente sin `01_ingest`).
3. **Desglose real de "6 olas de jueces" (14 jueces):** `9` jueces en Ronda 1 + `1` juez LQAS (`C-05`) + `4` rejudges quirúrgicos secuenciales de `C-09`.