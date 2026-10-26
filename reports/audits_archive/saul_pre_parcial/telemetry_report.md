# Informe de Auditoría Arquitectónica Forense: Rendimiento, Shards y Telemetría Multi-Agente
## Curso: Saul Pre Parcial (`saul_pre_parcial`)

**Fecha de Auditoría:** `2026-10-26 04:21:49 UTC`  
**Conversación Orquestadora:** [`201fa8ef-682b-4a7e-bdbd-88394a8ac506`](conversation://201fa8ef-682b-4a7e-bdbd-88394a8ac506)  
**Directorio de Trabajo Validado (Zero-Collision):** `D:\Augusto\personal_portfolio\Tops_academy\courses\saul_pre_parcial\work` (`match=True`)  
**Enfoque:** Telemetría Determinista de API, Subagentes, Shards, Latencias y Operaciones del Orquestador.

---

## 1. Consolidación de Métricas y Caracterización de Carga

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada** | `7 archivos` (103 págs / 10.39 MB) | MATH_IV_Problem_Set_I.pdf, MATH_IV_Problem_Set_II_2026_II.pdf, MATH_IV_Problem_Set_III_2026_II.pdf, TEMA 1 (EDP SAÚL) 2.pdf, TEMA 2 (APLICACIONES ECONOMICAS).pdf, TEMA 2 (S'EDOS I ).pdf, TEMA 2 (S'EDOS II).pdf |
| **Requerimiento de Visión** | `0 páginas` (0 handouts) | Cuadrículas generadas para diagramas/fórmulas |
| **Corpus Sintetizado** | `0 caracteres` (0 palabras) | Texto consolidado tras ingesta y visión |
| **Competencias Extraídas** | **`63 competencias`** | Desglose pedagógico (Hechos, Conceptos, Habilidades) |
| **Shards Particionados** | **`45 shards`** | Unidades de trabajo concurrentes |
| **Subagentes Desplegados** | **`63 subagentes`** | Visión (0), CTA (7), Autores (45), Jueces (11) |
| **Reactivos Finales Validados** | **`1520 preguntas`** | Evaluadas en sandbox |
| **Tokens Entrada (Subagentes)** | **`6,256,381` tokens** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`2,314,740` tokens** | Código de plantillas y JSON generado |
| **Tokens Caché (Leídos)** | **`34,570,011` tokens** | Caché de contexto reutilizado por la API |
| **Gran Total Tokens Activos** | **`9,139,649` tokens** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`43,709,660` tokens** | Consumo total de cuota facturable |

---

## 2. Ratios Unitarios Normalizados (Unit Economics)

Métricas normalizadas para comparación *apples-to-apples* frente a cursos de diferente volumen de contenido:

| Métrica Unitaria | Valor Obtenido | Interpretación de Eficiencia |
| :--- | :--- | :--- |
| **Tokens Totales por Pregunta** | **`28,756.4 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`6,012.9 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`693,804.1 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`106,629.5 tokens/comp`** | Costo puro de la etapa de autoría por competencia |
| **Tokens Totales por Página / Slide** | **`424,365.6 tokens/pág`** | Esfuerzo cognitivo por diapositiva original |
| **Segundos de Pared por Pregunta** | **`1.03 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`58.13 preg/min`** | Velocidad de producción del pipeline |
| **Factor de Aceleración Paralela** | **`12.77x`** | Relación tiempo cómputo vs tiempo de pared |

---

## 3. Desglose Forense por Etapas Críticas

### 3.0. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json` & `state.json`)
- **Snapshots de Etapa Verificados (`conversation_id` = `201fa8ef`):** `9 etapas`
- **Estado Maestro (`work/state.json`):** `completed` (Etapa actual/final: `publish`)

| Etapa (Snapshot) | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes Capturados | Artefactos / Metadatos de Etapa |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`00_prepare`** | `2026-10-26 03:52:31` | `0.13s` | `0` (`0` act) | 0 | `—` |
| **`00b_bootstrap`** | `2026-10-26 03:52:31` | `0.18s` | `0` (`0` act) | 0 | `lock_file=D:\Augusto\personal_portfolio\Tops_academy\courses\saul_pre_parcial\work\.c2c_subagent_lock.json` |
| **`01_cta`** | `2026-10-26 04:00:22` | `0.61s` | `3,259,039` (`1,022,521` act) | 7 | `competencies=63` |
| **`02_shard`** | `2026-10-26 04:00:27` | `0.07s` | `0` (`0` act) | 0 | `shards=45` |
| **`03_templates`** | `2026-10-26 04:13:10` | `86.17s` | `32,466,282` (`6,717,659` act) | 45 | `count=63` |
| **`04_build`** | `2026-10-26 04:13:33` | `14.95s` | `0` (`0` act) | 0 | `total_questions=1520` |
| **`05_verify`** | `2026-10-26 04:14:08` | `15.34s` | `0` (`0` act) | 0 | `verified_course_path=D:\Augusto\personal_portfolio\Tops_academy\courses\saul_pre_parcial\work\course_verified.json` |
| **`05b_judge_compare`** | `2026-10-26 04:17:05` | `0.11s` | `1,680,314` (`830,941` act) | 11 | `passed=True` |
| **`06_publish`** | `2026-10-26 04:17:17` | `6.64s` | `0` (`0` act) | 0 | `published_json=D:\Augusto\personal_portfolio\Tops_academy\courses\saul_pre_parcial.json` |

---

### 3.1. Stage 1A: Preprocesamiento de Visión
- **Subagentes de Visión Desplegados:** `0 agentes en paralelo`
- **Tiempo de Pared de la Etapa (Máximo / Critical Path):** **`0.0s`** (`0.0 min`)
- **Agente Determinante del Camino Crítico:** `N/A`

| Subagente de Visión | Turnos | Tokens In | Tokens Out | Cache Leído | Total Activo | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |

---

### 3.2. Stage 1B: Análisis Cognitivo de Competencias (CTA)
- **Arquitectura:** `MAPREDUCE (7 Mappers)`
- **Tiempo de Pared Fase Mappers (Máximo):** **`407.0s`** (determinado por `Cognitive Task Analysis Architect part_03`)
- **Tiempo Fase Harmonizer (Barrera Síncrona):** **`0.0s`**
- **Tiempo de Pared Total de Etapa 1B:** **`407.0s`** (`6.8 min`)

| Subagente CTA | Rol / Sección | Turnos | Tokens In | Tokens Out | Cache Leído | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Cognitive Task Analysis Architect part_04** | Mapper | 9 | 107,602 | 38,244 | 234,028 | 1 | **353.0s** |
| **Cognitive Task Analysis Architect part_07** | Mapper | 11 | 109,483 | 38,430 | 291,064 | 2 | **283.0s** |
| **Cognitive Task Analysis Architect part_05** | Mapper | 16 | 107,836 | 32,205 | 419,662 | 2 | **272.0s** |
| **Cognitive Task Analysis Architect part_06** | Mapper | 10 | 117,603 | 39,257 | 230,556 | 1 | **297.0s** |
| **Cognitive Task Analysis Architect part_03** | Mapper | 17 | 112,364 | 38,815 | 612,955 | 4 | **407.0s** |
| **Cognitive Task Analysis Architect part_02** | Mapper | 10 | 96,055 | 39,572 | 218,568 | 2 | **286.0s** |
| **Cognitive Task Analysis Architect part_01** | Mapper | 10 | 106,597 | 38,458 | 229,685 | 2 | **298.0s** |

---

### 3.3. Stage 3: Autoría de Reactivos por Shard y Análisis por Competencia
- **Total de Shards Auditados:** `45 shards concurrentes`
- **Duración Mínima de Shard:** `230.0s` | **Mediana:** `337.0s`
- **Tiempo de Pared Máximo (Straggler Crítico):** **`628.0s`** (`10.5 min`) por `Shard Author shard_14`
- **Retraso de Sincronización Impuesto por el Straggler:** **`+291.0s`** frente a la mediana
- **Tokens Promedio por Competencia en Autores:** **`106,629.5 tokens/competencia`**

| Shard ID | Competencias Asignadas | Comps | Tokens In | Tokens Out | Cache Leído | Total Activo | Tokens / Comp | Turnos | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Shard Author shard_27** | `C-07, C-08` | 2 | 103,272 | 38,081 | 482,292 | 141,353 | **70,676.5** | 17 | 3 | **314.0s** |
| **Shard Author shard_28** | `C-18, C-19` | 2 | 164,952 | 36,135 | 161,061 | 201,087 | **100,543.5** | 10 | 3 | **285.0s** |
| **Shard Author shard_29** | `C-01, H-01` | 2 | 110,716 | 37,643 | 602,786 | 148,359 | **74,179.5** | 17 | 3 | **322.0s** |
| **Shard Author shard_30** | `C-02, H-02` | 2 | 121,183 | 45,953 | 609,732 | 167,136 | **83,568.0** | 17 | 4 | **360.0s** |
| **Shard Author shard_31** | `C-03, H-03` | 2 | 114,668 | 47,357 | 671,884 | 162,025 | **81,012.5** | 20 | 3 | **386.0s** |
| **Shard Author shard_32** | `C-04, H-04` | 2 | 86,458 | 42,855 | 206,598 | 129,313 | **64,656.5** | 8 | 2 | **333.0s** |
| **Shard Author shard_33** | `C-05, H-05` | 2 | 116,439 | 49,425 | 469,584 | 165,864 | **82,932.0** | 14 | 4 | **390.0s** |
| **Shard Author shard_34** | `H-06, C-06` | 2 | 128,395 | 42,435 | 1,040,521 | 170,830 | **85,415.0** | 24 | 6 | **381.0s** |
| **Shard Author shard_35** | `H-07, C-09` | 2 | 98,196 | 39,747 | 430,918 | 137,943 | **68,971.5** | 12 | 2 | **275.0s** |
| **Shard Author shard_36** | `H-08, C-10` | 2 | 111,040 | 42,403 | 203,579 | 153,443 | **76,721.5** | 9 | 2 | **306.0s** |
| **Shard Author shard_37** | `C-11, H-09` | 2 | 121,544 | 45,448 | 1,072,024 | 166,992 | **83,496.0** | 23 | 6 | **353.0s** |
| **Shard Author shard_38** | `H-10, C-12` | 2 | 131,302 | 44,740 | 845,488 | 176,042 | **88,021.0** | 23 | 6 | **337.0s** |
| **Shard Author shard_39** | `H-11, C-13` | 2 | 136,406 | 48,380 | 950,704 | 184,786 | **92,393.0** | 21 | 4 | **350.0s** |
| **Shard Author shard_40** | `H-12, C-14` | 2 | 103,712 | 44,825 | 574,781 | 148,537 | **74,268.5** | 15 | 3 | **358.0s** |
| **Shard Author shard_41** | `C-15, H-15` | 2 | 111,523 | 52,973 | 419,226 | 164,496 | **82,248.0** | 14 | 4 | **442.0s** |
| **Shard Author shard_42** | `C-16, H-16` | 2 | 81,551 | 37,498 | 231,902 | 119,049 | **59,524.5** | 9 | 2 | **289.0s** |
| **Shard Author shard_43** | `C-17, H-17` | 2 | 97,751 | 46,443 | 369,842 | 144,194 | **72,097.0** | 12 | 4 | **346.0s** |
| **Shard Author shard_44** | `H-13, H-14` | 2 | 90,338 | 47,013 | 260,011 | 137,351 | **68,675.5** | 9 | 3 | **376.0s** |
| **Shard Author shard_01** | `Hab-01` | 1 | 77,993 | 36,420 | 179,380 | 114,413 | **114,413.0** | 8 | 2 | **289.0s** |
| **Shard Author shard_02** | `Hab-02` | 1 | 94,178 | 39,687 | 376,964 | 133,865 | **133,865.0** | 14 | 3 | **336.0s** |
| **Shard Author shard_03** | `Hab-03` | 1 | 89,051 | 32,754 | 472,462 | 121,805 | **121,805.0** | 16 | 4 | **230.0s** |
| **Shard Author shard_04** | `Hab-04` | 1 | 95,910 | 38,127 | 300,001 | 134,037 | **134,037.0** | 9 | 3 | **281.0s** |
| **Shard Author shard_05** | `Hab-05` | 1 | 71,414 | 31,925 | 176,581 | 103,339 | **103,339.0** | 8 | 2 | **254.0s** |
| **Shard Author shard_06** | `Hab-06` | 1 | 98,976 | 34,217 | 540,235 | 133,193 | **133,193.0** | 18 | 3 | **294.0s** |
| **Shard Author shard_07** | `Hab-07` | 1 | 76,461 | 34,784 | 221,735 | 111,245 | **111,245.0** | 9 | 2 | **239.0s** |
| **Shard Author shard_08** | `Hab-08` | 1 | 112,179 | 45,319 | 442,960 | 157,498 | **157,498.0** | 11 | 4 | **354.0s** |
| **Shard Author shard_09** | `Hab-09` | 1 | 98,004 | 37,038 | 429,070 | 135,042 | **135,042.0** | 16 | 4 | **364.0s** |
| **Shard Author shard_10** | `Hab-10` | 1 | 78,452 | 36,582 | 209,630 | 115,034 | **115,034.0** | 9 | 3 | **264.0s** |
| **Shard Author shard_11** | `Hab-11` | 1 | 135,592 | 53,400 | 1,377,015 | 188,992 | **188,992.0** | 27 | 7 | **450.0s** |
| **Shard Author shard_12** | `Hab-12` | 1 | 104,631 | 35,505 | 441,513 | 140,136 | **140,136.0** | 12 | 4 | **300.0s** |
| **Shard Author shard_13** | `Hab-13` | 1 | 92,727 | 38,256 | 444,107 | 130,983 | **130,983.0** | 14 | 3 | **301.0s** |
| **Shard Author shard_14 🛑** | `Hab-14` | 1 | 176,348 | 82,659 | 1,383,337 | 259,007 | **259,007.0** | 18 | 3 | **628.0s** |
| **Shard Author shard_15** | `Hab-15` | 1 | 141,248 | 49,384 | 1,332,509 | 190,632 | **190,632.0** | 28 | 3 | **480.0s** |
| **Shard Author shard_16** | `Hab-16` | 1 | 110,554 | 41,140 | 796,628 | 151,694 | **151,694.0** | 21 | 5 | **338.0s** |
| **Shard Author shard_17** | `Hab-17` | 1 | 88,569 | 34,838 | 402,108 | 123,407 | **123,407.0** | 15 | 6 | **297.0s** |
| **Shard Author shard_18** | `Hab-18` | 1 | 90,158 | 40,011 | 462,217 | 130,169 | **130,169.0** | 14 | 4 | **340.0s** |
| **Shard Author shard_19** | `Hab-19` | 1 | 74,365 | 32,178 | 173,379 | 106,543 | **106,543.0** | 8 | 2 | **231.0s** |
| **Shard Author shard_20** | `Hab-20` | 1 | 87,874 | 47,570 | 209,363 | 135,444 | **135,444.0** | 8 | 2 | **337.0s** |
| **Shard Author shard_21** | `Hab-21` | 1 | 135,817 | 43,602 | 825,271 | 179,419 | **179,419.0** | 18 | 6 | **348.0s** |
| **Shard Author shard_22** | `Hab-22` | 1 | 101,387 | 46,027 | 593,610 | 147,414 | **147,414.0** | 15 | 2 | **371.0s** |
| **Shard Author shard_23** | `Hab-23` | 1 | 111,222 | 46,670 | 863,330 | 157,892 | **157,892.0** | 23 | 6 | **397.0s** |
| **Shard Author shard_24** | `Hab-24` | 1 | 173,682 | 48,848 | 2,361,310 | 222,530 | **222,530.0** | 36 | 7 | **478.0s** |
| **Shard Author shard_25** | `Hab-25` | 1 | 95,629 | 38,505 | 408,663 | 134,134 | **134,134.0** | 16 | 5 | **308.0s** |
| **Shard Author shard_26** | `Hab-26` | 1 | 100,030 | 37,536 | 532,148 | 137,566 | **137,566.0** | 17 | 3 | **296.0s** |
| **Shard Author shard_45** | `C-20` | 1 | 72,408 | 31,018 | 190,164 | 103,426 | **103,426.0** | 9 | 3 | **251.0s** |

---

### 3.4. Evaluación y Arbitraje de Blind Judges (Verificación Psicométrica Ciega)

> [!NOTE]
> **Dictamen de Blind Judges:** ✅ 100% ACUERDO AL PRIMER INTENTO (126/126 REACTIVOS)  
> Los 11 Blind Judges evaluaron el lote estratificado de 126 reactivos en 1 turno de razonamiento puro cada uno (0 búsquedas web, 100% aislamiento epistémico), logrando un acuerdo psicométrico del 100.0% (126/126) con 0 discrepancias frente al ground truth.

| Dimensión de Arbitraje Ciego | Valor Registrado | Observación Técnica |
| :--- | :--- | :--- |
| **Lote Estratificado Ciego** | `126 reactivos` (63 comps × 2) | Lote de evaluación sin soluciones (`judge_batch.json`) |
| **Subagentes Jueces Ciegos** | `11 jueces` | Aislamiento epistémico en Stage 5 |
| **Resultado al Primer Intento** | **`✅ 100% Limpio (Sin Discrepancias)`** | Sin discrepancias ni arbitraje necesario |
| **Iteraciones de Auto-Reparación** | `2 iteraciones` en sandbox | 0 requeridas |
| **Intervenciones del Supervisor** | 🛠️ `0 operaciones directas` | Ninguna (ejecución autónoma) |

#### Detalle de Acciones Registradas:
- 1. **Arbitraje Ciego (`05b_judge_compare.json`)**: 126/126 acuerdos (`100.0% agreement rate`, `0 discrepancias`).
- 2. **Verificación Determinista Previa (`--stage verify`)**: Detectó 1 error(es) léxico/estructural(es) corregido(s) antes del arbitraje ciego.

---

## 4. Auditoría Forense del Orquestador y Catálogo de Intervenciones Manuales

### 4.1. Descomposición del Tiempo Total del Orquestador
- ⏱️ **Tiempo Total de Pared del Orquestador:** `26.15 min` (`1569.0s`)
- 💻 **Tiempo Activo Ejecutando Comandos CLI (`run.py`):** `1.2 min` (`70.0s`)
- 🛠️ **Tiempo Gastado en Intervenciones Manuales (Supervisor Repair):** **`0.0 min`** (`0.0s`)
- ⏳ **Tiempo Ocioso en Barreras de Sincronización (Esperando Subagentes):** `0.8 min` (`48.0s`)
- 🧠 **Tiempo de Inferencia y Razonamiento del Modelo:** `0.9 min` (`56.0s`)

### 4.2. Catálogo Cronológico de Reparaciones Manuales del Orquestador
Operaciones directas de edición de código ejecutadas por el orquestador: **`0`**

| Paso | Archivo Afectado | Tipo de Acción | Causa Raíz / Justificación Técnica | Herramienta | Tokens Paso |
| :---: | :--- | :--- | :--- | :--- | :--- |
| — | *Ninguna intervención registrada* | — | — | — | 0 |

---

## 5. Diagnóstico de Cuellos de Botella y Antipatrones Detectados

### 🛑 [HIGH] Straggler Crítico en Shards: Shard Author shard_14
- **Ámbito:** `Stage 3: Question Authoring`
- **Diagnóstico:** Shard Author shard_14 tardó 628.0s frente a la mediana de 337.0s (+291.0s de retraso en la barrera). Determinó el tiempo total de pared de la etapa de autoría.

### 🛑 [HIGH] Antipatrón de Micro-Bucle Interactivo (36 turnos en Shard Author shard_24)
- **Ámbito:** `Shard Author shard_24`
- **Diagnóstico:** 1 subagentes realizaron > 30 turnos individuales (ej. Shard Author shard_24 con 36 turnos). Ocurre por bucles de depuración o escritura incremental en lugar de redactar por lotes atómicos.

### ⚠️ [MEDIUM] Fricción de Herramientas en 36 subagentes
- **Ámbito:** `Multiple Subagents`
- **Diagnóstico:** Subagentes como Cognitive Task Analysis Architect part_03 acumularon fallos en consola (4 errores), provocando reintentos e invalidación de caché.

---

## 6. Telemetría de Razonamiento Cognitivo (Thinking Traces)

- **Total de Turnos con Razonamiento:** `443 turnos`
- **Volumen Total de Razonamiento:** `1,656,578 caracteres`
- **Razonamiento del Orquestador:** `14 turnos` (4,753 chars)
- **Razonamiento de Subagentes:** `429 turnos` (1,651,825 chars)

| Agente / Subagente | Turnos de Thinking | Caracteres de Thinking | Trazas de Error Capturadas |
| :--- | :---: | :---: | :---: |
| **Cognitive Task Analysis Architect part_04** | 5 | 33,789 | ⚠️ 1 |
| **Cognitive Task Analysis Architect part_07** | 7 | 23,701 | ⚠️ 2 |
| **Cognitive Task Analysis Architect part_05** | 10 | 23,309 | ⚠️ 2 |
| **Cognitive Task Analysis Architect part_06** | 8 | 33,292 | ⚠️ 1 |
| **Cognitive Task Analysis Architect part_03** | 10 | 32,447 | ⚠️ 4 |
| **Cognitive Task Analysis Architect part_02** | 6 | 32,767 | ⚠️ 2 |
| **Cognitive Task Analysis Architect part_01** | 6 | 19,542 | ⚠️ 2 |
| **Shard Author shard_27** | 5 | 24,882 | ⚠️ 3 |
| **Shard Author shard_28** | 7 | 23,557 | ⚠️ 3 |
| **Shard Author shard_29** | 8 | 23,106 | ⚠️ 3 |
| **Shard Author shard_30** | 8 | 38,284 | ⚠️ 4 |
| **Shard Author shard_31** | 8 | 38,245 | ⚠️ 3 |
| **Shard Author shard_32** | 6 | 23,686 | ⚠️ 2 |
| **Shard Author shard_33** | 5 | 30,274 | ⚠️ 4 |
| **Shard Author shard_34** | 11 | 29,662 | ⚠️ 6 |
| **Shard Author shard_35** | 7 | 27,245 | ⚠️ 2 |
| **Shard Author shard_36** | 6 | 27,804 | ⚠️ 2 |
| **Shard Author shard_37** | 8 | 35,213 | ⚠️ 6 |
| **Shard Author shard_38** | 10 | 28,914 | ⚠️ 6 |
| **Shard Author shard_39** | 8 | 43,309 | ⚠️ 4 |
| **Shard Author shard_40** | 9 | 35,311 | ⚠️ 3 |
| **Shard Author shard_41** | 8 | 35,695 | ⚠️ 4 |
| **Shard Author shard_42** | 6 | 30,772 | ⚠️ 2 |
| **Shard Author shard_43** | 6 | 32,522 | ⚠️ 4 |
| **Shard Author shard_44** | 6 | 30,942 | ⚠️ 3 |
| **Shard Author shard_01** | 6 | 26,711 | ⚠️ 2 |
| **Shard Author shard_02** | 5 | 25,980 | ⚠️ 3 |
| **Shard Author shard_03** | 10 | 19,927 | ⚠️ 4 |
| **Shard Author shard_04** | 5 | 25,320 | ⚠️ 3 |
| **Shard Author shard_05** | 6 | 23,789 | ⚠️ 2 |
| **Shard Author shard_06** | 9 | 21,261 | ⚠️ 3 |
| **Shard Author shard_07** | 7 | 21,811 | ⚠️ 2 |
| **Shard Author shard_08** | 7 | 36,314 | ⚠️ 4 |
| **Shard Author shard_09** | 8 | 30,951 | ⚠️ 4 |
| **Shard Author shard_10** | 6 | 28,323 | ⚠️ 3 |
| **Shard Author shard_11** | 8 | 27,287 | ⚠️ 7 |
| **Shard Author shard_12** | 7 | 28,348 | ⚠️ 4 |
| **Shard Author shard_13** | 8 | 23,731 | ⚠️ 3 |
| **Shard Author shard_14** | 15 | 57,791 | ⚠️ 3 |
| **Shard Author shard_15** | 16 | 34,841 | ⚠️ 3 |
| **Shard Author shard_16** | 12 | 27,765 | ⚠️ 5 |
| **Shard Author shard_17** | 8 | 22,808 | ⚠️ 6 |
| **Shard Author shard_18** | 7 | 29,977 | ⚠️ 4 |
| **Shard Author shard_19** | 4 | 28,449 | ⚠️ 2 |
| **Shard Author shard_20** | 6 | 31,241 | ⚠️ 2 |
| **Shard Author shard_21** | 7 | 29,217 | ⚠️ 6 |
| **Shard Author shard_22** | 8 | 33,245 | ⚠️ 2 |
| **Shard Author shard_23** | 11 | 36,467 | ⚠️ 6 |
| **Shard Author shard_24** | 14 | 37,188 | ⚠️ 7 |
| **Shard Author shard_25** | 7 | 26,087 | ⚠️ 5 |
| **Shard Author shard_26** | 9 | 27,233 | ⚠️ 3 |
| **Shard Author shard_45** | 6 | 25,426 | ⚠️ 3 |
| **Blind Judge 01** | 2 | 8,156 | 0 |
| **Blind Judge 02** | 2 | 15,875 | 0 |
| **Blind Judge 03** | 2 | 10,437 | 0 |
| **Blind Judge 04** | 2 | 9,937 | 0 |
| **Blind Judge 05** | 2 | 19,848 | 0 |
| **Blind Judge 06** | 2 | 5,181 | 0 |
| **Blind Judge 07** | 3 | 13,200 | 0 |
| **Blind Judge 08** | 2 | 5,940 | 0 |
| **Blind Judge 09** | 2 | 4,994 | 0 |
| **Blind Judge 10** | 2 | 4,777 | 0 |
| **Blind Judge 11** | 2 | 7,722 | 0 |

---
*Reporte forense determinista emitido por `c2c-run-auditor`.*