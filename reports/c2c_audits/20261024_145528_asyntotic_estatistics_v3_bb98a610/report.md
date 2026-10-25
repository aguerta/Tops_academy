# Informe de Auditoría Arquitectónica Forense: Rendimiento, Shards y Telemetría Multi-Agente
## Curso: Asyntotic Estatistics V3 (`asyntotic_estatistics_v3`)

**Fecha de Auditoría:** `2026-10-24 19:55:28 UTC`  
**Conversación Orquestadora:** [`bb98a610-c34f-44af-93c6-323d3cc202e7`](conversation://bb98a610-c34f-44af-93c6-323d3cc202e7)  
**Directorio de Trabajo Validado (Zero-Collision):** `D:\Augusto\personal_portfolio\Tops_academy\courses\asyntotic_estatistics_v3\work` (`match=True`)  
**Enfoque:** Telemetría Determinista de API, Subagentes, Shards, Latencias y Operaciones del Orquestador.

---

## 1. Consolidación de Métricas y Caracterización de Carga

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada** | `2 archivos` (52 págs / 3.44 MB) | ECONOMETRIC ANALTYSIS FIFTH EDITION  -  William H_ Greene  -  5th ed_, Upper Saddle River, N_J, New Jersey, 2003  -  Prentice Hall PTR  -  isbn13 9780130661890  -  d139b0dca2a0c7d0984d735f6be1944e  -  Anna’s Archive-93.pdf, Econometric Analysis (Greene) (z-library.sk, 1lib.sk, z-lib.sk)-923-946.pdf |
| **Requerimiento de Visión** | `0 páginas` (0 handouts) | Cuadrículas generadas para diagramas/fórmulas |
| **Corpus Sintetizado** | `0 caracteres` (0 palabras) | Texto consolidado tras ingesta y visión |
| **Competencias Extraídas** | **`30 competencias`** | Desglose pedagógico (Hechos, Conceptos, Habilidades) |
| **Shards Particionados** | **`22 shards`** | Unidades de trabajo concurrentes |
| **Subagentes Desplegados** | **`29 subagentes`** | Visión (0), CTA (2), Autores (22), Jueces (5) |
| **Reactivos Finales Validados** | **`690 preguntas`** | Evaluadas en sandbox |
| **Tokens Entrada (Subagentes)** | **`5,040,300` tokens** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`1,813,813` tokens** | Código de plantillas y JSON generado |
| **Tokens Caché (Leídos)** | **`80,520,212` tokens** | Caché de contexto reutilizado por la API |
| **Gran Total Tokens Activos** | **`7,560,750` tokens** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`88,080,962` tokens** | Consumo total de cuota facturable |

---

## 2. Ratios Unitarios Normalizados (Unit Economics)

Métricas normalizadas para comparación *apples-to-apples* frente a cursos de diferente volumen de contenido:

| Métrica Unitaria | Valor Obtenido | Interpretación de Eficiencia |
| :--- | :--- | :--- |
| **Tokens Totales por Pregunta** | **`127,653.6 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`10,957.6 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`2,936,032.1 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`206,145.0 tokens/comp`** | Costo puro de la etapa de autoría por competencia |
| **Tokens Totales por Página / Slide** | **`1,693,864.7 tokens/pág`** | Esfuerzo cognitivo por diapositiva original |
| **Segundos de Pared por Pregunta** | **`5.79 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`10.36 preg/min`** | Velocidad de producción del pipeline |
| **Factor de Aceleración Paralela** | **`4.75x`** | Relación tiempo cómputo vs tiempo de pared |

---

## 3. Desglose Forense por Etapas Críticas

### 3.0. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json` & `state.json`)
- **Snapshots de Etapa Verificados (`conversation_id` = `bb98a610`):** `9 etapas`
- **Estado Maestro (`work/state.json`):** `completed` (Etapa actual/final: `publish`)

| Etapa (Snapshot) | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes Capturados | Artefactos / Metadatos de Etapa |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`00_prepare`** | `2026-10-24 18:31:07` | `0.0s` | `0` (`0` act) | 0 | `—` |
| **`00b_bootstrap`** | `2026-10-24 18:31:07` | `0.03s` | `0` (`0` act) | 0 | `lock_file=D:\Augusto\personal_portfolio\Tops_academy\courses\asyntotic_estatistics_v3\work\.c2c_subagent_lock.json` |
| **`01_cta`** | `2026-10-24 18:37:16` | `0.34s` | `1,277,805` (`273,961` act) | 2 | `competencies=30` |
| **`02_shard`** | `2026-10-24 18:37:20` | `0.04s` | `0` (`0` act) | 0 | `shards=20` |
| **`03_templates`** | `2026-10-24 19:34:04` | `142.02s` | `68,096,681` (`6,184,349` act) | 22 | `count=30` |
| **`04_build`** | `2026-10-24 19:34:27` | `15.02s` | `0` (`0` act) | 0 | `total_questions=690` |
| **`05_verify`** | `2026-10-24 19:35:01` | `6.67s` | `9,893,909` (`423,711` act) | 1 | `verified_course_path=D:\Augusto\personal_portfolio\Tops_academy\courses\asyntotic_estatistics_v3\work\course_verified.json` |
| **`05b_judge_compare`** | `2026-10-24 19:37:09` | `0.13s` | `1,017,961` (`393,165` act) | 5 | `passed=True` |
| **`06_publish`** | `2026-10-24 19:37:20` | `3.48s` | `0` (`0` act) | 0 | `published_json=D:\Augusto\personal_portfolio\Tops_academy\courses\asyntotic_estatistics_v3.json` |

---

### 3.1. Stage 1A: Preprocesamiento de Visión
- **Subagentes de Visión Desplegados:** `0 agentes en paralelo`
- **Tiempo de Pared de la Etapa (Máximo / Critical Path):** **`0.0s`** (`0.0 min`)
- **Agente Determinante del Camino Crítico:** `N/A`

| Subagente de Visión | Turnos | Tokens In | Tokens Out | Cache Leído | Total Activo | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |

---

### 3.2. Stage 1B: Análisis Cognitivo de Competencias (CTA)
- **Arquitectura:** `MAPREDUCE (2 Mappers)`
- **Tiempo de Pared Fase Mappers (Máximo):** **`315.0s`** (determinado por `Cognitive Task Analysis Architect part_01`)
- **Tiempo Fase Harmonizer (Barrera Síncrona):** **`0.0s`**
- **Tiempo de Pared Total de Etapa 1B:** **`315.0s`** (`5.2 min`)

| Subagente CTA | Rol / Sección | Turnos | Tokens In | Tokens Out | Cache Leído | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Cognitive Task Analysis Architect part_01** | Mapper | 8 | 105,680 | 41,281 | 208,808 | 0 | **315.0s** |
| **Cognitive Task Analysis Architect part_02** | Mapper | 27 | 119,963 | 9,675 | 866,183 | 1 | **138.0s** |

---

### 3.3. Stage 3: Autoría de Reactivos por Shard y Análisis por Competencia
- **Total de Shards Auditados:** `22 shards concurrentes`
- **Duración Mínima de Shard:** `317.0s` | **Mediana:** `607.0s`
- **Tiempo de Pared Máximo (Straggler Crítico):** **`1273.0s`** (`21.2 min`) por `Shard Author shard_02`
- **Retraso de Sincronización Impuesto por el Straggler:** **`+666.0s`** frente a la mediana
- **Tokens Promedio por Competencia en Autores:** **`193,260.9 tokens/competencia`**

| Shard ID | Competencias Asignadas | Comps | Tokens In | Tokens Out | Cache Leído | Total Activo | Tokens / Comp | Turnos | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Shard Author shard_10** | `C-04, C-05` | 2 | 242,256 | 84,433 | 3,902,411 | 326,689 | **163,344.5** | 50 | 3 | **730.0s** |
| **Shard Author shard_01** | `Hab-01` | 1 | 154,425 | 65,138 | 1,622,947 | 219,563 | **219,563.0** | 29 | 8 | **498.0s** |
| **Shard Author shard_02 🛑** | `Hab-02` | 1 | 323,361 | 163,653 | 5,717,771 | 487,014 | **487,014.0** | 39 | 11 | **1273.0s** |
| **Shard Author shard_03** | `Hab-03` | 1 | 145,022 | 62,665 | 827,617 | 207,687 | **207,687.0** | 18 | 3 | **464.0s** |
| **Shard Author shard_04** | `Hab-04` | 1 | 154,740 | 55,213 | 1,344,126 | 209,953 | **209,953.0** | 26 | 6 | **473.0s** |
| **Shard Author shard_05** | `Hab-05` | 1 | 174,657 | 68,291 | 2,008,512 | 242,948 | **242,948.0** | 33 | 3 | **541.0s** |
| **Shard Author shard_06** | `Hab-06` | 1 | 201,538 | 71,106 | 3,042,083 | 272,644 | **272,644.0** | 35 | 4 | **607.0s** |
| **Shard Author shard_07** | `Hab-07` | 1 | 170,374 | 36,891 | 1,839,734 | 207,265 | **207,265.0** | 29 | 1 | **317.0s** |
| **Shard Author shard_08** | `Hab-08` | 1 | 142,267 | 64,437 | 955,801 | 206,704 | **206,704.0** | 20 | 3 | **518.0s** |
| **Shard Author shard_09** | `Hab-09` | 1 | 179,495 | 47,711 | 2,270,862 | 227,206 | **227,206.0** | 30 | 4 | **766.0s** |
| **Targeted Repair Engineer shard_02** | `Hab-02` | 1 | 317,348 | 106,363 | 9,470,198 | 423,711 | **423,711.0** | 78 | 19 | **1055.0s** |
| **Shard Author shard_11** | `C-06, C-07` | 2 | 160,998 | 54,007 | 1,966,757 | 215,005 | **107,502.5** | 26 | 0 | **473.0s** |
| **Shard Author shard_12** | `C-09, C-10` | 2 | 230,456 | 100,187 | 3,720,728 | 330,643 | **165,321.5** | 45 | 3 | **796.0s** |
| **Shard Author shard_13** | `C-12, C-13` | 2 | 190,000 | 44,777 | 2,855,794 | 234,777 | **117,388.5** | 33 | 1 | **462.0s** |
| **Shard Author shard_14** | `C-14, C-15` | 2 | 169,303 | 53,784 | 1,709,630 | 223,087 | **111,543.5** | 30 | 7 | **467.0s** |
| **Shard Author shard_15** | `H-01, C-01` | 2 | 190,496 | 72,812 | 2,112,217 | 263,308 | **131,654.0** | 34 | 5 | **590.0s** |
| **Shard Author shard_16** | `H-02, C-02` | 2 | 224,026 | 96,951 | 2,685,370 | 320,977 | **160,488.5** | 36 | 4 | **732.0s** |
| **Shard Author shard_17** | `H-03, C-03` | 2 | 213,719 | 89,667 | 2,266,949 | 303,386 | **151,693.0** | 34 | 2 | **679.0s** |
| **Shard Author shard_18** | `H-04, C-08` | 2 | 220,589 | 106,763 | 2,173,221 | 327,352 | **163,676.0** | 24 | 5 | **732.0s** |
| **Shard Author shard_19** | `C-11, H-05` | 2 | 195,334 | 88,345 | 2,285,987 | 283,679 | **141,839.5** | 26 | 3 | **655.0s** |
| **Shard Author shard_20** | `H-06` | 1 | 199,483 | 76,045 | 1,608,353 | 275,528 | **275,528.0** | 23 | 5 | **539.0s** |
| **Shard Author shard_02 clean** | `Hab-02` | 1 | 285,414 | 89,809 | 5,525,264 | 375,223 | **375,223.0** | 49 | 5 | **759.0s** |

---

### 3.4. Evaluación y Arbitraje de Blind Judges (Verificación Psicométrica Ciega)

> [!NOTE]
> **Dictamen de Blind Judges:** ✅ 100% ACUERDO AL PRIMER INTENTO (60/60 REACTIVOS)  
> Los 5 Blind Judges evaluaron el lote estratificado de 60 reactivos en 1 turno de razonamiento puro cada uno (0 búsquedas web, 100% aislamiento epistémico), logrando un acuerdo psicométrico del 100.0% (60/60) con 0 discrepancias frente al ground truth.

| Dimensión de Arbitraje Ciego | Valor Registrado | Observación Técnica |
| :--- | :--- | :--- |
| **Lote Estratificado Ciego** | `60 reactivos` (30 comps × 2) | Lote de evaluación sin soluciones (`judge_batch.json`) |
| **Subagentes Jueces Ciegos** | `5 jueces` | Aislamiento epistémico en Stage 5 |
| **Resultado al Primer Intento** | **`✅ 100% Limpio (Sin Discrepancias)`** | Sin discrepancias ni arbitraje necesario |
| **Iteraciones de Auto-Reparación** | `2 iteraciones` en sandbox | 0 requeridas |
| **Intervenciones del Supervisor** | 🛠️ `0 operaciones directas` | Ninguna (ejecución autónoma) |

#### Detalle de Acciones Registradas:
- 1. **Arbitraje Ciego (`05b_judge_compare.json`)**: 60/60 acuerdos (`100.0% agreement rate`, `0 discrepancias`).
- 2. **Verificación Determinista Previa (`--stage verify`)**: Detectó 2 error(es) léxico/estructural(es) corregido(s) antes del arbitraje ciego.

---

## 4. Auditoría Forense del Orquestador y Catálogo de Intervenciones Manuales

### 4.1. Descomposición del Tiempo Total del Orquestador
- ⏱️ **Tiempo Total de Pared del Orquestador:** `66.62 min` (`3997.0s`)
- 💻 **Tiempo Activo Ejecutando Comandos CLI (`run.py`):** `2.9 min` (`176.0s`)
- 🛠️ **Tiempo Gastado en Intervenciones Manuales (Supervisor Repair):** **`0.0 min`** (`0.0s`)
- ⏳ **Tiempo Ocioso en Barreras de Sincronización (Esperando Subagentes):** `1.2 min` (`74.0s`)
- 🧠 **Tiempo de Inferencia y Razonamiento del Modelo:** `1.4 min` (`81.0s`)

### 4.2. Catálogo Cronológico de Reparaciones Manuales del Orquestador
Operaciones directas de edición de código ejecutadas por el orquestador: **`0`**

| Paso | Archivo Afectado | Tipo de Acción | Causa Raíz / Justificación Técnica | Herramienta | Tokens Paso |
| :---: | :--- | :--- | :--- | :--- | :--- |
| — | *Ninguna intervención registrada* | — | — | — | 0 |

---

## 5. Diagnóstico de Cuellos de Botella y Antipatrones Detectados

### 🛑 [HIGH] Straggler Crítico en Shards: Shard Author shard_02
- **Ámbito:** `Stage 3: Question Authoring`
- **Diagnóstico:** Shard Author shard_02 tardó 1273.0s frente a la mediana de 607.0s (+666.0s de retraso en la barrera). Determinó el tiempo total de pared de la etapa de autoría.

### 🛑 [HIGH] Antipatrón de Micro-Bucle Interactivo (78 turnos en Targeted Repair Engineer shard_02)
- **Ámbito:** `Targeted Repair Engineer shard_02`
- **Diagnóstico:** 11 subagentes realizaron > 30 turnos individuales (ej. Targeted Repair Engineer shard_02 con 78 turnos). Ocurre por bucles de depuración o escritura incremental en lugar de redactar por lotes atómicos.

### ⚠️ [MEDIUM] Fricción de Herramientas en 18 subagentes
- **Ámbito:** `Multiple Subagents`
- **Diagnóstico:** Subagentes como Shard Author shard_10 acumularon fallos en consola (3 errores), provocando reintentos e invalidación de caché.

---

## 6. Telemetría de Razonamiento Cognitivo (Thinking Traces)

- **Total de Turnos con Razonamiento:** `449 turnos`
- **Volumen Total de Razonamiento:** `1,090,683 caracteres`
- **Razonamiento del Orquestador:** `28 turnos` (11,284 chars)
- **Razonamiento de Subagentes:** `421 turnos` (1,079,399 chars)

| Agente / Subagente | Turnos de Thinking | Caracteres de Thinking | Trazas de Error Capturadas |
| :--- | :---: | :---: | :---: |
| **Cognitive Task Analysis Architect part_01** | 6 | 29,627 | 0 |
| **Cognitive Task Analysis Architect part_02** | 12 | 5,358 | ⚠️ 1 |
| **Shard Author shard_10** | 26 | 46,125 | ⚠️ 3 |
| **Shard Author shard_01** | 17 | 38,334 | ⚠️ 8 |
| **Shard Author shard_02** | 30 | 105,931 | ⚠️ 10 |
| **Shard Author shard_03** | 8 | 38,391 | ⚠️ 3 |
| **Shard Author shard_04** | 13 | 29,569 | ⚠️ 6 |
| **Shard Author shard_05** | 17 | 38,710 | ⚠️ 3 |
| **Shard Author shard_06** | 18 | 34,905 | ⚠️ 4 |
| **Shard Author shard_07** | 13 | 23,717 | ⚠️ 1 |
| **Shard Author shard_08** | 11 | 46,268 | ⚠️ 3 |
| **Shard Author shard_09** | 16 | 30,151 | ⚠️ 4 |
| **Targeted Repair Engineer shard_02** | 40 | 60,000 | ⚠️ 10 |
| **Shard Author shard_11** | 15 | 33,254 | 0 |
| **Shard Author shard_12** | 25 | 54,689 | ⚠️ 3 |
| **Shard Author shard_13** | 14 | 27,735 | ⚠️ 1 |
| **Shard Author shard_14** | 17 | 33,627 | ⚠️ 7 |
| **Shard Author shard_15** | 17 | 45,529 | ⚠️ 5 |
| **Shard Author shard_16** | 13 | 34,119 | ⚠️ 4 |
| **Shard Author shard_17** | 17 | 57,971 | ⚠️ 2 |
| **Shard Author shard_18** | 11 | 60,171 | ⚠️ 5 |
| **Shard Author shard_19** | 15 | 51,856 | ⚠️ 3 |
| **Shard Author shard_20** | 12 | 43,615 | ⚠️ 5 |
| **Shard Author shard_02 clean** | 26 | 51,228 | ⚠️ 5 |
| **Blind Judge 01** | 2 | 7,614 | 0 |
| **Blind Judge 02** | 2 | 10,181 | 0 |
| **Blind Judge 03** | 3 | 16,712 | 0 |
| **Blind Judge 04** | 2 | 9,423 | 0 |
| **Blind Judge 05** | 3 | 14,589 | 0 |

---
*Reporte forense determinista emitido por `c2c-run-auditor`.*


---

## 7. Investigación Especial Solicitada: Respuestas Forenses Detalladas

### 7.1. Observación 1: ¿Por qué `CTA Architect part_02` tardó 2.30 min (138s) mientras `part_01` tardó 5.25 min (315s)? ¿Es bueno o malo?

> [!WARNING]
> **Dictamen Forense:** La rapidez de `CTA Architect part_02` (138s) fue **MALA (fuga de aislamiento inter-curso mediante `Copy-Item`)**, mientras que los 315s (5.25 min) de `CTA Architect part_01` representan el **tiempo legítimo, limpio y saludable** de síntesis curricular real.

| Dimensión Forense | `CTA Architect part_01` (`8e09ad50`) | `CTA Architect part_02` (`dc84b0b3`) |
| :--- | :--- | :--- |
| **Documento Fuente Asignado** | Cap. 4 Greene (28 páginas) | Apéndice D Greene (24 páginas) |
| **Duración Wall-Clock** | **315.46 s (5.25 min)** | **138.01 s (2.30 min)** |
| **Turnos (`PLANNER_RESPONSE`)** | **7 turnos** | **27 turnos** |
| **Tokens de Salida (Output)** | **41,216 tokens** (38,789 en 1 solo `write_file`) | **9,675 tokens** |
| **¿Leyó su PDF asignado?** | ✅ **SÍ** (`view_file` de las 28 págs. en Paso 7) | 🚨 **NO** (0 páginas leídas del PDF fuente) |
| **Evidencia en Transcript** | Sintetizó desde primeros principios 14 competencias y 84 distractores y compiló en 1 solo intento (Paso 11). | En el Paso 7 ejecutó `Get-ChildItem courses`, descubrió la corrida previa `asyntotic_estatistics_v2`, inspeccionó sus archivos durante 20 turnos y en el Paso 45 ejecutó:<br/>`Copy-Item -Path "courses/asyntotic_estatistics_v2/work/cta_parts/part_02_data.py" -Destination "courses/asyntotic_estatistics_v3/work/cta_parts/part_02_data.py"` |

---

### 7.2. Observación 2: Varianza entre los 20 Shards (5.28 min a 13.27 min) y Causas Exactas de Retraso Post-Primera-Compilación

#### Matriz Forense Completa de los 20 Shards (Ordenados por Duración)

| Ranking | Shard | Competencias Reales | Duración Total | Pre-1ra Comp. (Síntesis) | Post-1ra Comp. (Debug / Loops) | Compilaciones Reales (Pass/Fail) | Reglas Violadas en Intentos Fallidos | Causa Principal de su Duración / Varianza |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **1 (Más rápido)** | **`shard_07`** (`24a88d3b`) | `Hab-07` (1) | **317s (5.28m)** | 253s (79.8%) | 64s (20.2%) | 1 (1P / 0F) | Ninguna | 🚨 **Falso positivo (Copia de `v2`):** Leyó `asyntotic_estatistics_v2/work/shards/shard_07_data.py` en Pasos 21–25. |
| **2** | **`shard_13`** (`e4a0766a`) | `C-12, C-13` (2) | **462s (7.70m)** | 296s (64.1%) | 166s (35.9%) | 5 (5P / 0F) | Ninguna | ✅ **1st-Pass Clean**, pero gastó 166s post-pase verificando por qué el log decía `"2 plantillas"`. |
| **3** | **`shard_03`** (`a8694f71`) | `Hab-03` (1) | **464s (7.73m)** | 307s (66.2%) | 157s (33.8%) | 2 (1P / 1F) | `[R-18]`, `[TPL-D4]`, `[TPL-VAR]` | ✅ **Aislamiento 100% puro:** Resolvió colisión numérica (`0.005000`) y rango de `k` en 1 sola reedición (157s). |
| **4** | **`shard_14`** (`7358274f`) | `C-14, C-15` (2) | **467s (7.78m)** | 188s (40.3%) | 279s (59.7%) | 8 (4P / 4F) | Paridad (`C-15`), `[TPL-VAR]` | ✅ **Aislamiento 100% puro:** Omitió `C-15` en el borrador 1 y amplió rangos para `TPL-VAR` rápidamente. |
| **5** | **`shard_04`** (`bc2b704c`) | `Hab-04` (1) | **473s (7.88m)** | 191s (40.4%) | 282s (59.6%) | 5 (2P / 3F) | `[TPL-VAR]`, `[TPL-DRY]` (`f-string` & `cross_check`) | Corrigió especificador `.2f` mal anidado y tolerancia numérica del test de Hausman en `ver_hab04`. |
| **6** | **`shard_11`** (`60a6e778`) | `C-06, C-07` (2) | **473s (7.88m)** | 320s (67.7%) | 153s (32.3%) | 3 (3P / 0F) | Ninguna | ✅ **1st-Pass Clean:** Gastó 153s post-pase confirmando que los 8 arquetipos estaban en los 2 JSON. |
| **7** | **`shard_01`** (`7bdc6b0f`) | `Hab-01` (1) | **498s (8.30m)** | 59s (11.8%) | 439s (88.2%) | 12 (6P / 6F) | `[TPL-VAR]`, `[R-15]`, Paridad (`Hab-01_1`), `[TPL-DRY]`, `[R-18]` | Construyó el shard incrementalmente template por template en lugar de escribir los 4 arquetipos de golpe. |
| **8** | **`shard_08`** (`4d0b3923`) | `Hab-08` (1) | **518s (8.63m)** | 368s (71.0%) | 150s (29.0%) | 3 (2P / 1F) | `[TPL-VAR]` | 🌟 **Referente Clean-Room (100% aislado):** Único fallo `[TPL-VAR]` (`k in [3,4,5]` x `j in [2,6]` = 6 < 30), resuelto en 1 edición. |
| **9** | **`shard_20`** (`6fae6638`) | `H-06` (1) | **539s (8.98m)** | 270s (50.1%) | 269s (49.9%) | 4 (2P / 2F) | `[R-20]` (`$` impares), `[TPL-VAR]` | 2 ciclos de corrección por signos `$` huérfanos al final de las opciones 1 y 2 en `H-06`. |
| **10** | **`shard_05`** (`2cc478ab`) | `Hab-05` (1) | **541s (9.02m)** | 357s (66.0%) | 184s (34.0%) | 4 (3P / 1F) | `[R-18]` (13 giveaways verbales) | 🚨 Leyó `v2` (`shard_05_data.py`), pero falló con 13 errores `[R-18]` por usar gerundios delatores (`"omitiendo..."`). |
| **11** | **`shard_15`** (`d1c9494e`) | `H-01, C-01` (2) | **590s (9.83m)** | 511s (86.6%) | 79s (13.4%) | 3 (3P / 0F) | Ninguna | ✅ **1st-Pass Clean:** Invirtió 4m 42s en un único `write_file` masivo para 2 competencias y pasó a la primera. |
| **12** | **`shard_06`** (`66a588dc`) | `Hab-06` (1) | **607s (10.12m)** | 314s (51.7%) | 293s (48.3%) | 3 (1P / 2F) | `[AST]` (`\beta`, `\alpha`), `[R-18]`, `[TPL-VAR]` | 2 fallos seguidos por no usar raw strings `r'...'` y por generar distractores sumando offsets lineales `cv + step`. |
| **13** | **`shard_19`** (`b42109ad`) | `C-11, H-05` (2) | **655s (10.92m)** | 323s (49.3%) | 332s (50.7%) | 5 (4P / 1F) | `[R-15]` (longitud de opciones) | En el 1er pase puso solo 3 distractores; al expandir a 6 distractores en `C-11` disparó `[R-15]` y lo corrigió con `edit_file`. |
| **14** | **`shard_17`** (`b1bcb10d`) | `H-03, C-03` (2) | **679s (11.32m)** | 379s (55.8%) | 300s (44.2%) | 3 (1P / 2F) | `[R-15]`, `[TPL-VAR]`, `[NO-CHANGE]` | Doble competencia (8 arquetipos) + reescritura completa para igualar longitud de opciones (`R-15`) y rangos (`TPL-VAR`). |
| **15** | **`shard_10`** (`585a45aa`) | `C-04, C-05` (2) | **730s (12.17m)** | 478s (65.5%) | 252s (34.5%) | 4 (4P / 0F) | Ninguna | ⚠️ **Paranoid Loop Post-Pase (252s):** Pasó al 1er intento, pero al leer `"2 plantillas"` creyó que faltaban 6 y reescribió el archivo. |
| **16** | **`shard_16`** (`731c004f`) | `H-02, C-02` (2) | **732s (12.20m)** | 440s (60.1%) | 292s (39.9%) | 3 (2P / 1F) | `[R-15]`, `[TPL-VAR]` | **Cuello de botella `write_file` masivo:** Escribió 3 veces un archivo de **57 KB (>860 líneas)**, gastando **466s (7.77m)** solo en streaming. |
| **17** | **`shard_18`** (`6451c5fe`) | `H-04, C-08` (2) | **732s (12.20m)** | 306s (41.8%) | 426s (58.2%) | 4 (1P / 3F) | `[R-18]` (x3), `[R-20]` (`hat{\theta}`), `[TPL-VAR]` (x3) | **3 fallos consecutivos en `H-04` por `[R-18]` + 4 `write_file` de 33–42 KB** (**566s = 9.43m** solo generando código en `write_file`). |
| **18** | **`shard_09`** (`dfbde880`) | `Hab-09` (1) | **766s (12.77m)** | 340s (44.4%) | 426s (55.6%) | 5 (3P / 2F) | Paridad (`shard_01` target), `[R-18]` | ⚠️ **Paranoid Loop Post-Pase (328s = 5.47m perdidos):** Ya había pasado a los 7.3m, pero iteró 5.5m viendo `LastWriteTime` de `shard_09.json`. |
| **19** | **`shard_12`** (`30b820d1`) | `C-09, C-10` (2) | **796s (13.27m)** | 432s (54.3%) | 364s (45.7%) | 5 (3P / 2F) | `[R-15]`, `[TPL-VAR]`, `[R-18]`, `[NO-CHANGE]` | **Hiper-exploración inicial (7.2m)** + triple fallo simultáneo (`R-15` + `R-18` + `TPL-VAR`) + reescritura completa de **53.8 KB** (~2.5m). |
| **20 (Caso Especial)** | **`shard_02`** (`4e68` / `697c` / `fff0`) | `Hab-02` (1) | **1273s + 1055s + 759s (51.45m acum.)** | 349s / 52s / 48s | 924s / 1003s / 711s | Int.1: 0P/6F (CB)<br/>Int.2: 0P/5F (CB)<br/>Int.3: 1P/2F | `[R-20]` (`\text{Asy. Var}[b_}{LS}]`), `[R-18]`, `[TPL-VAR]`, `[TPL-D4]`, `CIRCUIT BREAKER` | **Caso Especial (3 intentos):** Ver desglose forense completo en Sección 7.3. |

---

### 7.3. Observación 3: Caso Especial `shard_02` (`Hab-02`) — Anatomía de los 3 Intentos (51.45 min acumulados)

1. **Intento 1 (`Original Author`, `4e6890bd-a359-40a2-9503-3f50221b7b5c` — 1,273s / 21.22 min, 39 turnos -> CANCELADO):**
   - El autor incrustó tanto la expresión matemática como la justificación verbal dentro de las cadenas de opciones con llaves rotas: `\text{Asy. Var}[b_}{LS}]` y `{"value": r"$\text{Est. Asy. Var}[b_{IV}] = @d1@$: omisión de la forma sándwich..."}`.
   - Esto disparó simultáneamente `[R-20: SINTAXIS / LLAVES]` (llaves desbalanceadas en L247..267), `[R-18: DISTRACTORES BOILERPLATE SINTÉTICOS]`, `[TPL-D4: OPCIONES DUPLICADAS]` y `[TPL-VAR: DIVERSIDAD DE REACTIVOS]` (menos de 30 combinaciones únicas).
   - Tras 6 compilaciones fallidas, en el **Paso 71 (18:57:00Z)** se disparó el **Circuit Breaker (`circuit_breaker_shard_02_Hab-02.json`)**. El subagente ignoró la orden `STOP, send_message the Director` y continuó ejecutando `view_file` y scripts de PowerShell con errores de sintaxis hasta que el Director lo mató a las `18:58:52Z`.
2. **Intento 2 (`c2c_repair`, `697cb35c-d298-4f84-97f5-e8accba18f94` — 1,055s / 17.58 min, 78 turnos -> CANCELADO):**
   - **Triple fallo sistémico en la transición Director -> Repair:**
     1. El Director ejecutó `dispatch.py --role repair --work-dir ... --failed-cid Hab-02` (siguiendo una instrucción desactualizada de `SKILL.md` L226 y `c2c_hook_guard.py` L315), recibiendo error de `argparse`.
     2. Al ejecutar `dispatch.py dispatch-repair`, devolvió `Subagents: []` porque `dispatch_repair` solo leía `templates_report.json` (inexistente antes de completar Stage 3).
     3. El Director invocó `c2c_repair` manualmente **sin limpiar `.check_attempts/circuit_breaker_shard_02_Hab-02.json` ni `compile_shard_02.json`**.
   - Como consecuencia, `c2c_repair` nació bloqueado: sufrió **2 rechazos `[NO-CHANGE]`** y **5 disparos consecutivos del Circuit Breaker heredado** (Turnos 91, 105, 126, 137). Desorientado por el bloqueo, gastó **78 turnos y 9.89M de tokens** ejecutando búsquedas recursivas en segundo plano (`Get-ChildItem -Recurse | Select-String '}{LS'`) que saturaron el proceso hasta ser cancelado a las `19:17:47Z`.
3. **Intento 3 (`Shard Author shard_02 clean`, `fff07e52-ccd1-4fe8-9167-3baa5ac3bf56` — 759s / 12.65 min, 49 turnos -> ÉXITO):**
   - El Director eliminó manualmente `courses/asyntotic_estatistics_v3/work/.check_attempts/*` y despachó un autor limpio.
   - Tras 2 fallos iniciales en los Turnos 47 y 55 (`[R-18]`, `[R-20]`, `[TPL-VAR]`), el subagente inspeccionó los shards ya compilados (`shard_01_data.py`, `shard_03_data.py`, `shard_06_data.py`) y descubrió el patrón ganador: separar limpiamente `"value": r"$@d1@$"` de `"error_rationale": r"..."` y garantizar separación numérica `abs(val - c) < 0.0003`.
   - En el **Turno 89 (`19:30:13Z`)** reescribió `shard_02_data.py` con esta arquitectura y en el **Turno 91 (`19:31:10Z`)** compiló `Hab-02.json` con 0 errores.

---

### 7.4. Impacto de las 2 Olas Secuenciales vs 1 Sola Ola y Blindajes Implementados

- **Costo Real de haber partido en 2 olas:** La Ola 2 (`shard_11` a `shard_20`) estuvo bloqueada esperando **22.5 minutos** (de `18:37:38Z` a `19:00:12Z`) a que terminara la Ola 1, añadiendo **+13.27 minutos adicionales** (`shard_12`) al camino crítico. Además, `dispatch-authors --wave 2` sobrescribió `work/dispatch/items/author_01.json..author_10.json`.
- **Blindajes Aplicados en `.agents/skills/content-to-course/`:**
  1. **1 Sola Ola de Máxima Paralelización (`plan_shards.py` + `SKILL.md`):** `DEFAULT_MAX_WAVE_SIZE = 50` para lanzar los 20 shards simultáneamente a $t=0$ ordenados *Heaviest-First*.
  2. **Nombres de Work Orders por `shard_id` (`dispatch.py`):** `author_shard_01.json`..`author_shard_20.json` y `repair_<CID>.json`, eliminando el riesgo de sobrescritura.
  3. **Auto-Detección y Auto-Reset de Circuit Breaker en `dispatch-repair` (`dispatch.py`):** Mantiene `c2c_repair` en `Model="flash"`, detecta shards con `.check_attempts/` en circuit breaker o `work/templates/<cid>.json` faltantes sin requerir `templates_report.json`, inyecta `last_errors` en el diagnóstico del prompt y **elimina automáticamente los archivos `.check_attempts/` del shard afectado**. Soporta además `--failed-cid` y el fallback CLI `--role repair`.
  4. **Aislamiento Cross-Course en `c2c_hook_guard.py`:** Bloquea deterministamente cualquier lectura, listado (`Get-ChildItem courses`) o `Copy-Item` hacia otros directorios `courses/<otro_course_id>/` durante una corrida activa.
  5. **Mensaje `[+] PASS` Explícito en `compile_shard.py`:** Reporta tanto el número de competencias como el total de plantillas/arquetipos y las rutas escritas (`2 competencias, 8 plantillas/arquetipos en [...] STOP: No ejecutes más herramientas`), erradicando el *Paranoid Verification Loop* que costó 4–5.5 min en `shard_09` y `shard_10`.


---

### 7.5. El Diagnóstico Detrás de los Errores: ¿Qué fue literalmente diferente entre `shard_08` (`reference_cleanroom`) y los demás 19 Shards (incluido `shard_02`)?

Al comparar línea por línea el código de [`shard_08_data.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/asyntotic_estatistics_v3/work/shards/shard_08_data.py) (**269 líneas, 8.63 min, 20 turnos, 100% Clean-Room**) frente a [`shard_02_data.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/asyntotic_estatistics_v3/work/shards/shard_02_data.py) y los otros 18 shards, e inspeccionar [`invariants.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/engine/invariants.py), [`rules.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/src/validator/rules.py), [`compile_shard.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/compile_shard.py) y [`prompt_shard_author.md (lean)`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/system_prompts/lean/prompt_shard_author.md), se descubrieron **6 causas raíz sistémicas** que explican toda la varianza y los bucles de compilación:

#### Causa Raíz 1: El Falso Positivo de `[R-18: DISTRACTORES BOILERPLATE SINTÉTICOS]` que destruyó a `shard_02` y frenó a `shard_01, 03, 06` (mientras `shard_08` se salvó por 1 carácter)
- **Cómo funcionaba el chequeo en [`invariants.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/engine/invariants.py#L81-L101) y [`rules.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/src/validator/rules.py#L353-L369):**
  La función `check_synthetic_boilerplate_distractors` calculaba `_skeleton(d)` reemplazando números por `<NUM>` **sin extraer ni ignorar los bloques matemáticos LaTeX `$...$`**, y lanzaba error `[R-18: DISTRACTORES BOILERPLATE SINTÉTICOS]` si **$\ge 4$ distractores** compartían un mismo esqueleto de **$\ge 20$ caracteres**.
- **Por qué `shard_08` pasó sin error `[R-18]`:**
  1. En [`shard_08_data.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/asyntotic_estatistics_v3/work/shards/shard_08_data.py#L57), el autor escribió:
     `{"value": r"$\text{Avar} = @d1@$", "distractor_id": "D-Hab08-05", "error_rationale": "..."}`
  2. Su esqueleto era `\text{avar} = <NUM>`, que mide exactamente **19 caracteres (`19 < 20`)** — ¡1 carácter por debajo del umbral! Además, `shard_08` declaró solo **3 distractores manuales** (`3 < 4`) por arquetipo.
- **Por qué `shard_02` (Intento 1), `shard_03`, `shard_01` y `shard_06` fallaron con `[R-18]`:**
  1. Siguiendo el mismo patrón pero usando la notación de Greene para los 6 distractores (`6 >= 4`), `shard_02` y `shard_03` escribieron:
     `{"value": r"$\text{Est. Asy. Var}[b_{IV}] = @d1@$", ...}` o `r"$\text{Est. Asy. Var}[b_{2SLS}] = @d1@$"`
  2. Su esqueleto `\text{est asy var} b_{iv} = <NUM>` mide **33 caracteres (`>= 20`)** en los 6 distractores.
  3. El validador rechazó falsamente sus opciones numéricas legítimas con el mensaje:
     `[-] [R-18: DISTRACTORES BOILERPLATE SINTÉTICOS] -> Acción: Reemplazar distractores boilerplate por modelos de error y confusiones conceptuales reales.`
  4. **Efecto dominó en `shard_02` (Intento 1):** Al obedecer al validador e inyectar explicaciones conceptuales dentro del `"value"` junto a la fórmula LaTeX (`r"$\text{Est. Asy. Var}[b_{IV}] = @d1@$: omisión de..."`), el autor de `shard_02` rompió llaves LaTeX (`\text{Asy. Var}[b_}{LS}]` $\to$ `[R-20]`), introdujo gerundios delatores (`[R-18: META-INFORMACIÓN]`) y desbalanceó longitudes (`[R-15]`), consumiendo 21 minutos hasta disparar el Circuit Breaker. En el **Intento 3 (`fff07e52`)**, solo logró pasar en el Turno 89 cuando borró el lado izquierdo de la ecuación y dejó únicamente `"value": r"$@d1@$"` (esqueleto `<NUM>` de 5 caracteres `< 20`).

#### Causa Raíz 2: Contradicción Directa sobre `TPL-VAR` en el Lean System Prompt (Causó el 1er fallo en 11 de los 20 Shards)
- Durante `run.py --stage bootstrap`, el sistema genera las definiciones de subagentes con `lean=True`, cargando [`system_prompts/lean/prompt_shard_author.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/system_prompts/lean/prompt_shard_author.md).
- La línea 22 de ese prompt instruía literalmente a los autores:
  `- **TPL-VAR:** Generator must produce >= 4 unique instances across seeds.`
- Sin embargo, `check_templates.py` exige **$\ge 30$ instancias únicas en 50 semillas para habilidades (`Hab-*`) y $\ge 20$ para conceptos/hechos (`C-*`, `H-*`)**.
- Por esta contradicción, **11 de los 20 shards** (incluyendo `shard_08` en su 1ra compilación de `gen_hab08_02`, donde usó `k in [3,4,5]` y `j in [2,6]` produciendo $3 \times 2 = 6 \ge 4$ instancias) fallaron su primer intento de compilación con `[TPL-VAR: BAJA DIVERSIDAD DE INSTANCIACIÓN]`.

#### Causa Raíz 3: Por qué seguían ocurriendo errores de LaTeX (`[AST]` / `[R-20]`) pese a `r"..."` y `@var@`
1. **Bug en `extract_function_code` ([`compile_shard.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/compile_shard.py#L444-L453)) que anulaba la auto-curación en memoria (`shard_06`):**
   - `compile_shard.py` ejecutaba `_, healed_source = heal_shard_source_text(raw_source)` en la línea 885 para escapar automáticamente comandos LaTeX en strings sin prefijo `r` (`"\beta"`, `"\alpha"`, `"\theta"`).
   - **Pero** en la línea 446, `extract_function_code()` llamaba primero a `inspect.getsource(fn_or_str)`, el cual lee el archivo **sin curar directamente desde el disco** (vía `linecache`), descartando `healed_source` (`locator.lines`)! Por eso `shard_06` falló con `[AST: CORRUPCIÓN DE ESCAPE LATEX]`.
2. **Comandos matemáticos sin barra inicial o macros no soportados en KaTeX estricto (`shard_11, 18, 20`):**
   - `shard_18` escribió `hat{\theta}` (sin `\`) dentro de `$...$`; `shard_11` y `shard_20` usaron `\implies` en vez de `\Rightarrow`; y `shard_20` dejó un doble `$$` de cierre en una expresión inline (`$...@ans@$$`).
3. **f-strings anidados con especificadores de formato (`.2f`) dentro de diccionarios Python (`shard_01, 04`):**
   - Aunque las plantillas usaban `@var@`, dentro del cuerpo de `gen_hab01` y `gen_hab04` los autores usaron f-strings complejos con llaves anidadas que provocaron `ValueError: Invalid format specifier` en `[TPL-DRY]`.

#### Causa Raíz 4: Bug de Resolución de `@ans@` en `build_adapted_mc7_generator` ([`compile_shard.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/compile_shard.py#L540-L575))
- Cuando un autor definía $< 6$ distractores por arquetipo y usaba `@ans@` en `correct` (como `shard_08` y `shard_19`), `build_adapted_mc7_generator` intentaba extraer un `float` de `correct_val` **antes de sustituir `@ans@` desde `res["vars"]`**.
- Como `"@ans@"` aún no era un número, `m_num` daba `False` y el adaptador rellenaba los distractores faltantes con el texto literal `"Opción alterna 4: <correct_val>"`, disparando violaciones de longitud `[R-15]` o haciendo que `shard_19` entrara en pánico y reescribiera todo su archivo.

#### Causa Raíz 5: Confusión entre `"value"` y `"error_rationale"` en `[R-18: META-INFORMACIÓN]` y Longitud `[R-15]` (`shard_05, 09, 12, 16, 17, 19`)
- En el work order generado por `dispatch.py`, cada distractor se imprimía como `Creencia errónea: "Omitir evaluar..."` sin advertir la diferencia entre `"value"` (texto visible al estudiante en la opción MC) y `"error_rationale"` (retroalimentación post-evaluación).
- Mientras **`shard_08`** redactó en `"value"` proposiciones matemáticas neutras de longitud homogénea y colocó el diagnóstico en `"error_rationale"`, los autores de `shard_05` (13 errores), `shard_09` (5 errores) y `shard_12` copiaron gerundios autodelatores (`"omitiendo..."`, `"confundiendo..."`, `"asumiendo erróneamente..."`) dentro de `"value"`.

#### Causa Raíz 6: Inflación de Tamaño en `write_file` (50–57 KB en `shard_12, 16, 17, 18` vs 11 KB en `shard_08` y 4.8 KB en `shard_02` clean)
- **`shard_08_data.py`** tiene **269 líneas (~11 KB)** y **`shard_02_data.py` (Intento 3)** tiene **121 líneas (4.8 KB)** (~18 a 35 segundos de generación en `write_file`).
- En cambio, los shards con 2 competencias (`shard_12, 16, 17, 18`) escribieron archivos monolíticos de **600 a 865 líneas (42 a 57 KB)** (~14,000 tokens de salida) y, ante errores menores de 2 líneas, reescribieron los 57 KB completos con `write_file(Overwrite=True)` en vez de usar `edit_file`, gastando **de 7.7 a 9.4 minutos únicamente transmitiendo tokens en `write_file`**.

---

### 7.6. Matriz Consolidada de Parches: (A) Qué se Parcheó en Fase 2 (Orquestación/Guardas) vs (B) Qué se Parcheó en Fase 3 (Motor, Validador y Prompts)

| Categoría | Archivo Modificado | Problema Raíz que Resuelve | Estado |
| :--- | :--- | :--- | :---: |
| **A.1. Paralelismo 1 Sola Ola** | [`plan_shards.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/plan_shards.py#L40) y [`SKILL.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/SKILL.md) | `DEFAULT_MAX_WAVE_SIZE = 50`: elimina la espera secuencial de 22.5 min entre Ola 1 y Ola 2; lanza los 20 shards en **1 sola ola** ordenados *Heaviest-First*. | ✅ **Parcheado (Fase 2)** |
| **A.2. No-Colisión de Work Orders** | [`dispatch.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/dispatch.py#L1095-L1097) | Nombra las órdenes como `author_shard_01.json`..`author_shard_20.json` y `repair_<CID>.json`, evitando que una ola sobrescriba a otra. | ✅ **Parcheado (Fase 2)** |
| **A.3. Auto-Reset de Circuit Breaker en `dispatch-repair`** | [`dispatch.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/dispatch.py#L1140-L1275) | Mantiene `Model="flash"`, detecta fallos desde `.check_attempts/` sin requerir `templates_report.json`, inyecta `last_errors` en el prompt y **limpia automáticamente `.check_attempts/`** del shard afectado (evita el bloqueo de `shard_02` Intento 2). | ✅ **Parcheado (Fase 2)** |
| **A.4. Aislamiento Cross-Course** | [`c2c_hook_guard.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/c2c_hook_guard.py#L229-L265) | Bloquea lecturas, `Get-ChildItem courses` y `Copy-Item` hacia otros cursos (`v2`, `practica_parcial_saul`) que contaminaron `CTA part_02` y `shard_05, 06, 07, 10`. | ✅ **Parcheado (Fase 2)** |
| **A.5. Fin del Paranoid Loop Post-Pase** | [`compile_shard.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/compile_shard.py#L1349) | Mensaje `[+] PASS` reporta `({N} competencias, {M} plantillas/arquetipos en [...]). STOP: No ejecutes más herramientas`, ahorrando los 4–5.5 min perdidos en `shard_09` y `shard_10`. | ✅ **Parcheado (Fase 2)** |
| **B.1. Fin del Falso Positivo `[R-18]` en Ecuaciones Matemáticas** | [`invariants.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/engine/invariants.py#L81-L106) y [`rules.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/src/validator/rules.py#L353-L370) | `_prose_skeleton` limpia bloques matemáticos `$...$` / `$$...$$` antes de medir repetición de plantilla sintética ($\ge 20$ chars), evitando que opciones como `$\text{Est. Asy. Var}[b_{IV}] = @d1@$` sean rechazadas como boilerplate (causa raíz del colapso de `shard_02` y fallos en `shard_01, 03, 06`), mientras sigue atrapando prosa repetitiva e inversión de antónimos. | ✅ **Parcheado (Fase 3)** |
| **B.2. Persistencia Real de Auto-Curación LaTeX en Memoria y AST** | [`compile_shard.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/compile_shard.py#L97-L105) y [`compile_shard.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/compile_shard.py#L453) | `extract_function_code` ahora extrae desde `locator.lines` (`healed_source`) en vez de `inspect.getsource()` (disco sin curar), pasa `staged_p` a `check_templates` y auto-cura `\implies` $\to$ `\Rightarrow`, `\iff` $\to$ `\Leftrightarrow`, comandos sin barra (`hat{\theta}` $\to$ `\hat{\theta}`) y `$$` huérfano en inline math (`shard_06, 11, 18, 20`). | ✅ **Parcheado (Fase 3)** |
| **B.3. Resolución de `@var@` en Adaptador MC7** | [`compile_shard.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/compile_shard.py#L550-L563) | `build_adapted_mc7_generator` resuelve `@var@` desde `res["vars"]` antes de extraer el ancla numérica de `correct_val`, generando perturbaciones numéricas limpias cuando se definen $< 6$ distractores. | ✅ **Parcheado (Fase 3)** |
| **B.4. Contrato `TPL-VAR`, `R-18`, `R-15` y Compactación Estándar `shard_08`** | [`prompt_shard_author.md (lean)`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/system_prompts/lean/prompt_shard_author.md#L17-L28) y [`dispatch.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/dispatch.py#L1083-L1092) | Corrige `TPL-VAR >= 4` por la cuota real (**$\ge 30$ `Hab-*` / $\ge 20$ `C-*, H-*` con espacio $\ge 500$ combinaciones**), exige separación estricta entre `"value"` (neutro/matemático, `0.80x–1.20x`) y `"error_rationale"` (sin gerundios en `"value"`), y fija presupuesto compacto ($\le 150\text{–}250$ líneas/competencia + `edit_file` quirúrgico). | ✅ **Parcheado (Fase 3)** |
