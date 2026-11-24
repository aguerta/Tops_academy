# Informe de Auditoría Arquitectónica Forense: Rendimiento, Shards y Telemetría Multi-Agente
## Curso: Estadistica 3 Pre Cl K3 (`estadistica_3_pre_cl_k3`)

**Fecha de Auditoría:** `2026-11-24 21:49:24 UTC`  
**Conversación Orquestadora:** [`e7d34485-9871-4c16-b1fb-921e7e56482b`](conversation://e7d34485-9871-4c16-b1fb-921e7e56482b)  
**Directorio de Trabajo Validado (Zero-Collision):** `D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_pre_cl_k3\work` (`match=True`)  
**Enfoque:** Telemetría Determinista de API, Subagentes, Shards, Latencias, Costos USD (Gemini 4 Hydrogen) y Operaciones del Orquestador.

---

## 1. Consolidación de Métricas y Caracterización de Carga

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada** | `3 archivos` (43 págs / 1.56 MB) | 01_measure_theory_bridge.pdf, 02_stat110_lec27_conditional_expectation.pdf, 03_rincon_cl_caps1_2.pdf |
| **Requerimiento de Visión** | `0 páginas` (0 handouts) | Cuadrículas generadas para diagramas/fórmulas |
| **Corpus Sintetizado** | `0 caracteres` (0 palabras) | Texto consolidado tras ingesta y visión |
| **Competencias Extraídas** | **`18 competencias`** | Desglose pedagógico (Hechos, Conceptos, Habilidades) |
| **Shards Particionados** | **`18 shards`** | Unidades de trabajo concurrentes |
| **Subagentes Desplegados** | **`34 subagentes`** | Visión (0), CTA (4), Autores (18), Repairs (1), Jueces (11) |
| **Reactivos Finales Validados** | **`558 preguntas`** | Evaluadas en sandbox |
| **Tokens Entrada (Subagentes)** | **`1,532,351` tokens** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`522,984` tokens** | Código de plantillas y JSON generado |
| **Tokens Caché (Leídos)** | **`4,146,103` tokens** | Caché de contexto reutilizado por la API |
| **Gran Total Tokens Activos** | **`2,129,339` tokens** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`6,275,442` tokens** | Consumo total de cuota facturable |
| **Costo Estimado Total (Gemini 4 Hydrogen)** | **`$6.67 USD`** | In: `$2.40` (`$1.50/1M`), Out+Think: `$3.95` (`$7.50/1M`), Cache: `$0.31` (`$0.08/1M`) |

---

## 2. Ratios Unitarios Normalizados (Unit Economics)

Métricas normalizadas para comparación *apples-to-apples* frente a cursos de diferente volumen de contenido:

| Métrica Unitaria | Valor Obtenido | Interpretación de Eficiencia |
| :--- | :--- | :--- |
| **Tokens Totales por Pregunta** | **`11,246.3 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`3,816.0 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`348,635.7 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`76,580.5 tokens/comp`** | Costo puro de la etapa de autoría por competencia |
| **Tokens Totales por Página / Slide** | **`145,940.5 tokens/pág`** | Esfuerzo cognitivo por diapositiva original |
| **Costo Estimado por Pregunta (Hydrogen)** | **`$0.01 USD/preg`** | Costo monetario valorizado por reactivo |
| **Costo Estimado por Competencia (Hydrogen)** | **`$0.37 USD/comp`** | Costo monetario valorizado por competencia |
| **Segundos de Pared por Pregunta** | **`7.63 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`7.86 preg/min`** | Velocidad de producción del pipeline |
| **Factor de Aceleración Paralela** | **`1.65x`** | Relación tiempo cómputo vs tiempo de pared |

---

## 3. Desglose Forense por Etapas Críticas

### 3.0a. Valorización Monetaria por Etapa (Tarifas Gemini 4 Hydrogen)
> Tarifas oficiales aplicables: Entrada `$1.50/1M`, Caché leído `$0.08/1M`, Salida (incl. thinking) `$7.50/1M`.

| Etapa / Rol | Agentes | Tokens Entrada | Tokens Salida | Caché Leído | Costo Estimado (USD) | % del Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Stage 1A: Visión** | 0 | 0 | 0 | 0 | **`$0.00`** | 0.0% |
| **Stage 1B: CTA Architects** | 4 | 155,322 | 31,229 | 298,876 | **`$0.49`** | 7.3% |
| **Stage 3: Shard Authors** | 18 | 996,321 | 382,128 | 3,138,738 | **`$4.60`** | 69.0% |
| **Stage 3B: Repair Engineers** | 1 | 43,436 | 6,002 | 114,340 | **`$0.12`** | 1.8% |
| **Stage 5: Blind Judges** | 11 | 337,272 | 103,625 | 358,826 | **`$1.31`** | 19.6% |
| **Orquestador Principal (Director)** | 1 | 69,912 | 4,092 | 235,323 | **`$0.15`** | 2.2% |
| **TOTAL CORRIDA (Gemini 4 Hydrogen)** | **35** | **1,602,263** | **527,076** | **4,146,103** | **`$6.67 USD`** | **100.0%** |

### 3.0. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json` & `state.json`)
- **Snapshots de Etapa Verificados (`conversation_id` = `e7d34485`):** `9 etapas`
- **Estado Maestro (`work/state.json`):** `completed` (Etapa actual/final: `publish`)

| Etapa (Snapshot) | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes Capturados | Artefactos / Metadatos de Etapa |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`00_prepare`** | `2026-11-24 21:38:38` | `0.0s` | `0` (`0` act) | 0 | `—` |
| **`00b_bootstrap`** | `2026-11-24 21:38:38` | `0.11s` | `0` (`0` act) | 0 | `lock_file=D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_pre_cl_k3\work\.c2c_subagent_lock.json` |
| **`01_cta`** | `2026-11-24 21:40:26` | `0.85s` | `0` (`0` act) | 0 | `competencies=18` |
| **`02_shard`** | `2026-11-24 21:40:28` | `0.03s` | `0` (`0` act) | 0 | `shards=18` |
| **`03_templates`** | `2026-11-24 21:49:09` | `0.3s` | `0` (`0` act) | 0 | `count=18` |
| **`04_build`** | `2026-11-24 21:49:15` | `6.93s` | `0` (`0` act) | 0 | `total_questions=558` |
| **`05_verify`** | `2026-11-24 21:49:17` | `1.1s` | `0` (`0` act) | 0 | `verified_course_path=D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_pre_cl_k3\work\course_verified.json` |
| **`05b_judge_compare`** | `2026-11-24 21:46:36` | `0.19s` | `0` (`0` act) | 0 | `passed=False` |
| **`06_publish`** | `2026-11-24 21:49:23` | `2.58s` | `0` (`0` act) | 0 | `published_json=D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_pre_cl_k3.json` |

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
- **Tiempo de Pared Fase Mappers (Máximo):** **`69.0s`** (determinado por `Cognitive Task Analysis Architect part_03`)
- **Tiempo Fase Harmonizer (Barrera Síncrona):** **`27.0s`**
- **Tiempo de Pared Total de Etapa 1B:** **`96.0s`** (`1.6 min`)
- **Costo Estimado Etapa 1B (Gemini 4 Hydrogen):** **`$0.49 USD`**

| Subagente CTA | Rol / Sección | Turnos | Tokens In | Tokens Out | Cache Leído | Costo (USD) | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| **Cognitive Task Analysis Architect part_03** | Mapper | 4 | 48,232 | 10,363 | 91,640 | `$0.16` | 0 | **69.0s** |
| **Cognitive Task Analysis Architect part_01** | Mapper | 4 | 40,401 | 9,407 | 76,675 | `$0.14` | 0 | **63.0s** |
| **Cognitive Task Analysis Architect part_02** | Mapper | 4 | 38,512 | 8,536 | 73,814 | `$0.13` | 0 | **58.0s** |
| **CTA Harmonizer** | Harmonizer | 4 | 28,177 | 2,923 | 56,747 | `$0.07` | 0 | **27.0s** |

---

### 3.3. Stage 3: Autoría de Reactivos por Shard y Análisis por Competencia
- **Total de Shards Auditados:** `18 shards concurrentes`
- **Tasa de Aprobación en 1ra Compilación:** **`7/18 (38.89%)`** (Reglas en 1er fallo: `[TPL-STATIC-OPT]` (5), `[TPL-D4]` (2), `[R-15-MS]` (2), `[TPL-STEM-EQUATION-PARITY]` (1), `[TPL-DRY]` (1), `[TPL-VAR]` (1))
- **Duración Mínima de Shard:** `83.0s` | **Mediana:** `113.0s`
- **Tiempo de Pared Máximo (Straggler Crítico):** **`151.0s`** (`2.5 min`) por `Shard Author shard_01`
- **Retraso de Sincronización Impuesto por el Straggler:** **`+38.0s`** frente a la mediana
- **Tokens Promedio por Competencia en Autores:** **`76,580.5 tokens/competencia`**
- **Costo Estimado Etapa 3 (Gemini 4 Hydrogen):** **`$4.60 USD`**

| Shard ID | Competencias Asignadas | Comps | Tokens In | Tokens Out | Cache Leído | Total Activo | Costo (USD) | Tokens / Comp | Turnos | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :--- | :--- | :--- |
| **Shard Author shard_01 🛑** | `Hab-01` | 1 | 59,041 | 23,939 | 210,123 | 82,980 | `$0.28` | **82,980.0** | 6 | 1 | **151.0s** |
| **Shard Author shard_02** | `Hab-02` | 1 | 56,910 | 22,481 | 198,280 | 79,391 | `$0.27` | **79,391.0** | 6 | 1 | **117.0s** |
| **Shard Author shard_03** | `Hab-03` | 1 | 52,301 | 20,768 | 101,037 | 73,069 | `$0.24` | **73,069.0** | 4 | 0 | **104.0s** |
| **Shard Author shard_04** | `Hab-04` | 1 | 61,902 | 26,143 | 211,890 | 88,045 | `$0.30` | **88,045.0** | 6 | 1 | **135.0s** |
| **Shard Author shard_05** | `Hab-05` | 1 | 63,879 | 28,274 | 225,977 | 92,153 | `$0.32` | **92,153.0** | 6 | 1 | **149.0s** |
| **Shard Author shard_06** | `Hab-06` | 1 | 57,195 | 25,505 | 105,949 | 82,700 | `$0.29` | **82,700.0** | 4 | 0 | **113.0s** |
| **Shard Author shard_07** | `Hab-07` | 1 | 54,701 | 22,787 | 103,291 | 77,488 | `$0.26` | **77,488.0** | 4 | 0 | **110.0s** |
| **Shard Author shard_08** | `Hab-08` | 1 | 58,133 | 23,170 | 204,198 | 81,303 | `$0.28` | **81,303.0** | 6 | 1 | **121.0s** |
| **Shard Author shard_09** | `C-01` | 1 | 49,619 | 15,863 | 177,713 | 65,482 | `$0.21` | **65,482.0** | 6 | 1 | **95.0s** |
| **Shard Author shard_13** | `C-05` | 1 | 54,028 | 18,737 | 186,587 | 72,765 | `$0.24` | **72,765.0** | 6 | 1 | **103.0s** |
| **Shard Author shard_14** | `C-06` | 1 | 52,325 | 19,014 | 141,878 | 71,339 | `$0.23` | **71,339.0** | 5 | 0 | **111.0s** |
| **Shard Author shard_15** | `C-07` | 1 | 51,659 | 20,994 | 99,341 | 72,653 | `$0.24` | **72,653.0** | 4 | 0 | **103.0s** |
| **Shard Author shard_16** | `C-08` | 1 | 63,384 | 19,143 | 362,147 | 82,527 | `$0.27` | **82,527.0** | 10 | 2 | **129.0s** |
| **Shard Author shard_17** | `C-09` | 1 | 46,692 | 15,770 | 94,456 | 62,462 | `$0.20` | **62,462.0** | 4 | 0 | **83.0s** |
| **Shard Author shard_18** | `C-10` | 1 | 55,451 | 21,737 | 194,736 | 77,188 | `$0.26` | **77,188.0** | 6 | 1 | **117.0s** |
| **Shard Author shard_10** | `C-02` | 1 | 51,785 | 17,433 | 181,713 | 69,218 | `$0.22` | **69,218.0** | 6 | 1 | **109.0s** |
| **Shard Author shard_11** | `C-03` | 1 | 57,467 | 21,356 | 242,184 | 78,823 | `$0.26` | **78,823.0** | 7 | 1 | **116.0s** |
| **Shard Author shard_12** | `C-04` | 1 | 49,849 | 19,014 | 97,238 | 68,863 | `$0.22` | **68,863.0** | 4 | 0 | **92.0s** |

---

### 3.3b. Stage 3B: Remediación y Repair Engineers (Ingenieros de Reparación)
- **Total de Repair Engineers Desplegados:** `1 subagentes` en **`1 ronda(s)`** (`DONE`: `1`, `BLOCKED`: **`0`**)
- **Duración Mínima:** `46.0s` | **Mediana:** `46.0s` | **Máxima:** `46.0s` (`0.8 min`)
- **Tokens Activos Totales en Reparación:** `49,438 tokens`
- **Costo Estimado Etapa 3B (Gemini 4 Hydrogen):** **`$0.12 USD`**
- **Agente Determinante del Retraso:** `Repair Engineer Hab-06`

| Repair Engineer | Estado | Turnos | Tokens In | Tokens Out | Cache Leído | Total Activo | Costo (USD) | Errores | Duración |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Repair Engineer Hab-06** | `DONE` | 5 | 43,436 | 6,002 | 114,340 | 49,438 | `$0.12` | 0 | **46.0s** |

---

### 3.4. Evaluación y Arbitraje de Blind Judges (Verificación Psicométrica Ciega)

> [!NOTE]
> **Dictamen de Blind Judges:** ⚠️ NO PASÓ AL PRIMER INTENTO — APROBADO POST-REJUDGE (145/145 REACTIVOS)  
> La Ronda 1 de Blind Judges registró 1 discrepancia(s), por lo que no hubo acuerdo limpio al primer intento. Tras correcciones y Rejudge, el resultado final alcanzó 100.0% de acuerdo (0 discrepancias).

| Dimensión de Arbitraje Ciego | Valor Registrado | Observación Técnica |
| :--- | :--- | :--- |
| **Lote Estratificado Ciego** | `145 reactivos` (18 comps × 2) | Lote de evaluación sin soluciones (`judge_batch.json`) |
| **Subagentes Jueces Ciegos** | `11 jueces` | Aislamiento epistémico en Stage 5 |
| **Costo Etapa 5 (Gemini 4 Hydrogen)** | **`$1.31 USD`** | Evaluado sobre los 11 Blind Judges (In: `337,272`, Out: `103,625`, Cache: `358,826`) |
| **Resultado al Primer Intento** | **`❌ Falló al primer intento`** | Ronda 1: 1 discrepancia(s) (`flaw_detected`: 1, `kernel_override`: 1); 0 violaciones iniciales |
| **Resultado Final Post-Rejudge** | **`✅ Aprobado`** | `100.0%` acuerdo, `0` discrepancia(s) |
| **Iteraciones de Auto-Reparación** | `0 iteraciones` en sandbox | 0 iteraciones ejecutadas |
| **Intervenciones del Supervisor** | 🛠️ `0 operaciones directas` | Ninguna (ejecución autónoma) |

#### Detalle de Acciones Registradas:
- 1. **Ronda 1 (`judge_report_round_1.json` / `rounds_history`)**: 1 discrepancia(s) detectada(s).
- 2. **Bucle de Auto-Reparación / Rejudge**: 3 ola(s) de jueces ejecutada(s) (0 intervenciones de supervisor).
- 3. **Resultado Final Post-Rejudge (`judge_report.json`)**: ✅ Aprobado (`100.0% agreement rate`, `0 discrepancias` sobre 145 reactivos).

---

## 4. Auditoría Forense del Orquestador y Catálogo de Intervenciones Manuales

### 4.1. Descomposición del Tiempo y Costo del Orquestador
- 💵 **Costo Estimado del Orquestador Principal (Gemini 4 Hydrogen):** **`$0.15 USD`** (In: `69,912`, Out: `4,092`, Cache: `235,323`)
- ⏱️ **Tiempo Total de Pared del Orquestador:** `71.0 min` (`4260.0s`)
- 💻 **Tiempo Activo Ejecutando Comandos CLI (`run.py`):** `0.32 min` (`19.0s`)
- 🛠️ **Tiempo Gastado en Intervenciones Manuales (Supervisor Repair):** **`0.0 min`** (`0.0s`)
- ⏳ **Tiempo Ocioso en Barreras de Sincronización (Esperando Subagentes):** `70.05 min` (`4203.0s`)
- 🧠 **Tiempo de Inferencia y Razonamiento del Modelo:** `0.58 min` (`35.0s`)

### 4.2. Catálogo Cronológico de Reparaciones Manuales del Orquestador
Operaciones directas de edición de código ejecutadas por el orquestador: **`0`**

| Paso | Archivo Afectado | Tipo de Acción | Causa Raíz / Justificación Técnica | Herramienta | Tokens Paso |
| :---: | :--- | :--- | :--- | :--- | :--- |
| — | *Ninguna intervención registrada* | — | — | — | 0 |

---

## 5. Diagnóstico de Cuellos de Botella y Antipatrones Detectados

> ✅ **0 cuellos de botella detectados según los umbrales deterministas.**
---

## 6. Telemetría de Razonamiento Cognitivo (Thinking Traces)

- **Total de Turnos con Razonamiento:** `54 turnos`
- **Volumen Total de Razonamiento:** `244,860 caracteres`
- **Razonamiento del Orquestador:** `4 turnos` (915 chars)
- **Razonamiento de Subagentes:** `50 turnos` (243,945 chars)

| Agente / Subagente | Turnos de Thinking | Caracteres de Thinking | Trazas de Error Capturadas |
| :--- | :---: | :---: | :---: |
| **Repair Engineer Hab-06** | 1 | 2,404 | 0 |
| **Blind Judge 01** | 1 | 1,953 | 0 |
| **Cognitive Task Analysis Architect part_03** | 2 | 2,761 | 0 |
| **Cognitive Task Analysis Architect part_01** | 1 | 6,208 | 0 |
| **Cognitive Task Analysis Architect part_02** | 2 | 2,670 | 0 |
| **CTA Harmonizer** | 1 | 1,583 | 0 |
| **Shard Author shard_01** | 2 | 10,703 | ⚠️ 1 |
| **Shard Author shard_02** | 2 | 6,327 | ⚠️ 1 |
| **Shard Author shard_03** | 1 | 10,018 | 0 |
| **Shard Author shard_04** | 2 | 10,210 | ⚠️ 1 |
| **Shard Author shard_05** | 2 | 12,299 | ⚠️ 1 |
| **Shard Author shard_06** | 1 | 11,163 | 0 |
| **Shard Author shard_07** | 1 | 11,812 | 0 |
| **Shard Author shard_08** | 2 | 9,887 | ⚠️ 1 |
| **Shard Author shard_09** | 2 | 4,382 | ⚠️ 1 |
| **Shard Author shard_13** | 2 | 7,741 | ⚠️ 1 |
| **Shard Author shard_14** | 2 | 5,133 | 0 |
| **Shard Author shard_15** | 1 | 10,080 | 0 |
| **Shard Author shard_16** | 3 | 5,384 | ⚠️ 2 |
| **Shard Author shard_17** | 1 | 3,757 | 0 |
| **Shard Author shard_18** | 3 | 9,906 | ⚠️ 1 |
| **Shard Author shard_10** | 2 | 5,757 | ⚠️ 1 |
| **Shard Author shard_11** | 2 | 9,056 | ⚠️ 1 |
| **Shard Author shard_12** | 1 | 7,156 | 0 |
| **Blind Judge 01** | 1 | 7,034 | 0 |
| **Blind Judge 02** | 1 | 10,971 | 0 |
| **Blind Judge 03** | 1 | 6,920 | 0 |
| **Blind Judge 04** | 1 | 9,093 | 0 |
| **Blind Judge 05** | 1 | 8,553 | 0 |
| **Blind Judge 06** | 1 | 8,651 | 0 |
| **Blind Judge 07** | 1 | 10,047 | 0 |
| **Blind Judge 08** | 1 | 7,588 | 0 |
| **Blind Judge 09** | 1 | 5,766 | 0 |
| **Blind Judge 01** | 1 | 972 | 0 |

---
*Reporte forense determinista emitido por `c2c-run-auditor`.*