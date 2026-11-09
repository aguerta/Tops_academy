# Informe de Auditoría Arquitectónica Forense: Rendimiento, Shards y Telemetría Multi-Agente
## Curso: Saul Pc Sistemas De Ecuaciones Vmapreduce6 (`saul_pc_sistemas_de_ecuaciones_vmapreduce6`)

**Fecha de Auditoría:** `2026-11-09 07:10:01 UTC`  
**Conversación Orquestadora:** [`12fe6d7c-1c14-4288-912b-6d276c02d194`](conversation://12fe6d7c-1c14-4288-912b-6d276c02d194)  
**Directorio de Trabajo Validado (Zero-Collision):** `D:\Augusto\personal_portfolio\Tops_academy\courses\saul_pc_sistemas_de_ecuaciones_vmapreduce6\work` (`match=True`)  
**Enfoque:** Telemetría Determinista de API, Subagentes, Shards, Latencias y Operaciones del Orquestador.

---

## 1. Consolidación de Métricas y Caracterización de Carga

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada** | `6 archivos` (93 págs / 4.23 MB) | TEMA 2.1 (S'EDOS I ).pdf, TEMA 2.2 (APLICACIONES ECONOMICAS).pdf, TEMA 2.3 (S'EDOS II).pdf, Tema 2.4 MATH_IV_Problem_Set_III_2026_II.pdf, TEMA 3.1 APUNTES GRABACION TEMA 3 (S'EED).pdf, TEMA 3.2 (S'EED).pdf |
| **Requerimiento de Visión** | `0 páginas` (0 handouts) | Cuadrículas generadas para diagramas/fórmulas |
| **Corpus Sintetizado** | `0 caracteres` (0 palabras) | Texto consolidado tras ingesta y visión |
| **Competencias Extraídas** | **`60 competencias`** | Desglose pedagógico (Hechos, Conceptos, Habilidades) |
| **Shards Particionados** | **`41 shards`** | Unidades de trabajo concurrentes |
| **Subagentes Desplegados** | **`59 subagentes`** | Visión (0), CTA (8), Autores (41), Repairs (0), Jueces (10) |
| **Reactivos Finales Validados** | **`1410 preguntas`** | Evaluadas en sandbox |
| **Tokens Entrada (Subagentes)** | **`5,830,667` tokens** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`2,749,852` tokens** | Código de plantillas y JSON generado |
| **Tokens Caché (Leídos)** | **`35,373,575` tokens** | Caché de contexto reutilizado por la API |
| **Gran Total Tokens Activos** | **`9,067,394` tokens** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`44,440,969` tokens** | Consumo total de cuota facturable |

---

## 2. Ratios Unitarios Normalizados (Unit Economics)

Métricas normalizadas para comparación *apples-to-apples* frente a cursos de diferente volumen de contenido:

| Métrica Unitaria | Valor Obtenido | Interpretación de Eficiencia |
| :--- | :--- | :--- |
| **Tokens Totales por Pregunta** | **`31,518.4 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`6,430.8 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`740,682.8 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`117,163.3 tokens/comp`** | Costo puro de la etapa de autoría por competencia |
| **Tokens Totales por Página / Slide** | **`477,859.9 tokens/pág`** | Esfuerzo cognitivo por diapositiva original |
| **Segundos de Pared por Pregunta** | **`1.62 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`36.96 preg/min`** | Velocidad de producción del pipeline |
| **Factor de Aceleración Paralela** | **`12.55x`** | Relación tiempo cómputo vs tiempo de pared |

---

## 3. Desglose Forense por Etapas Críticas

### 3.0. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json` & `state.json`)
- **Snapshots de Etapa Verificados (`conversation_id` = `12fe6d7c`):** `9 etapas`
- **Estado Maestro (`work/state.json`):** `completed` (Etapa actual/final: `publish`)

| Etapa (Snapshot) | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes Capturados | Artefactos / Metadatos de Etapa |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`00_prepare`** | `2026-11-09 06:22:20` | `0.11s` | `0` (`0` act) | 0 | `—` |
| **`00b_bootstrap`** | `2026-11-09 06:22:20` | `0.14s` | `0` (`0` act) | 0 | `lock_file=D:\Augusto\personal_portfolio\Tops_academy\courses\saul_pc_sistemas_de_ecuaciones_vmapreduce6\work\.c2c_subagent_lock.json` |
| **`01_cta`** | `2026-11-09 06:27:34` | `0.28s` | `1,977,565` (`789,875` act) | 7 | `needs_harmonize=True` |
| **`02_shard`** | `2026-11-09 06:30:46` | `0.07s` | `0` (`0` act) | 0 | `shards=41` |
| **`03_templates`** | `2026-11-09 06:59:47` | `0.13s` | `29,911,271` (`7,029,799` act) | 41 | `count=60` |
| **`04_build`** | `2026-11-09 06:59:56` | `8.63s` | `0` (`0` act) | 0 | `total_questions=1410` |
| **`05_verify`** | `2026-11-09 06:59:58` | `1.86s` | `1,185,345` (`662,449` act) | 10 | `verified_course_path=D:\Augusto\personal_portfolio\Tops_academy\courses\saul_pc_sistemas_de_ecuaciones_vmapreduce6\work\course_verified.json` |
| **`05b_judge_compare`** | `2026-11-09 06:59:21` | `0.06s` | `1,185,345` (`662,449` act) | 10 | `passed=True` |
| **`06_publish`** | `2026-11-09 07:00:02` | `4.05s` | `0` (`0` act) | 0 | `published_json=D:\Augusto\personal_portfolio\Tops_academy\courses\saul_pc_sistemas_de_ecuaciones_vmapreduce6.json` |

---

### 3.1. Stage 1A: Preprocesamiento de Visión
- **Subagentes de Visión Desplegados:** `0 agentes en paralelo`
- **Tiempo de Pared de la Etapa (Máximo / Critical Path):** **`0.0s`** (`0.0 min`)
- **Agente Determinante del Camino Crítico:** `N/A`

| Subagente de Visión | Turnos | Tokens In | Tokens Out | Cache Leído | Total Activo | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |

---

### 3.2. Stage 1B: Análisis Cognitivo de Competencias (CTA)
- **Arquitectura:** `MAPREDUCE (7 Mappers + 1 Harmonizer)`
- **Tiempo de Pared Fase Mappers (Máximo):** **`267.0s`** (determinado por `Cognitive Task Analysis Architect part_07`)
- **Tiempo Fase Harmonizer (Barrera Síncrona):** **`167.0s`**
- **Tiempo de Pared Total de Etapa 1B:** **`434.0s`** (`7.2 min`)

| Subagente CTA | Rol / Sección | Turnos | Tokens In | Tokens Out | Cache Leído | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Cognitive Task Analysis Architect part_04** | Mapper | 7 | 79,811 | 25,241 | 148,220 | 1 | **206.0s** |
| **Cognitive Task Analysis Architect part_01** | Mapper | 7 | 78,004 | 25,402 | 167,551 | 0 | **193.0s** |
| **Cognitive Task Analysis Architect part_02** | Mapper | 7 | 83,142 | 30,513 | 177,882 | 0 | **219.0s** |
| **Cognitive Task Analysis Architect part_03** | Mapper | 7 | 74,891 | 22,241 | 152,901 | 0 | **184.0s** |
| **Cognitive Task Analysis Architect part_06** | Mapper | 6 | 116,851 | 35,940 | 86,061 | 0 | **266.0s** |
| **Cognitive Task Analysis Architect part_07** | Mapper | 10 | 85,017 | 27,397 | 303,747 | 2 | **267.0s** |
| **Cognitive Task Analysis Architect part_05** | Mapper | 7 | 76,392 | 29,033 | 151,328 | 0 | **221.0s** |
| **CTA Harmonizer** | Harmonizer | 6 | 79,263 | 19,133 | 196,890 | 0 | **167.0s** |

---

### 3.3. Stage 3: Autoría de Reactivos por Shard y Análisis por Competencia
- **Total de Shards Auditados:** `41 shards concurrentes`
- **Duración Mínima de Shard:** `253.0s` | **Mediana:** `495.0s`
- **Tiempo de Pared Máximo (Straggler Crítico):** **`1289.0s`** (`21.5 min`) por `Shard Author shard_12`
- **Retraso de Sincronización Impuesto por el Straggler:** **`+794.0s`** frente a la mediana
- **Tokens Promedio por Competencia en Autores:** **`117,163.3 tokens/competencia`**

| Shard ID | Competencias Asignadas | Comps | Tokens In | Tokens Out | Cache Leído | Total Activo | Tokens / Comp | Turnos | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Shard Author shard_22** | `C-02, C-03` | 2 | 174,706 | 87,000 | 2,268,125 | 261,706 | **130,853.0** | 27 | 5 | **1157.0s** |
| **Shard Author shard_23** | `C-04, C-05` | 2 | 102,032 | 53,624 | 517,128 | 155,656 | **77,828.0** | 11 | 3 | **765.0s** |
| **Shard Author shard_24** | `C-07, C-08` | 2 | 96,309 | 62,663 | 347,903 | 158,972 | **79,486.0** | 8 | 2 | **637.0s** |
| **Shard Author shard_25** | `C-09, C-10` | 2 | 76,853 | 40,654 | 327,402 | 117,507 | **58,753.5** | 9 | 2 | **344.0s** |
| **Shard Author shard_26** | `C-12, C-13` | 2 | 193,958 | 66,009 | 957,449 | 259,967 | **129,983.5** | 16 | 3 | **846.0s** |
| **Shard Author shard_27** | `C-15, C-16` | 2 | 78,311 | 51,825 | 80,919 | 130,136 | **65,068.0** | 4 | 0 | **416.0s** |
| **Shard Author shard_28** | `C-18, C-19` | 2 | 97,155 | 51,137 | 128,961 | 148,292 | **74,146.0** | 5 | 0 | **342.0s** |
| **Shard Author shard_29** | `C-20, C-21` | 2 | 128,746 | 79,543 | 980,119 | 208,289 | **104,144.5** | 14 | 3 | **801.0s** |
| **Shard Author shard_30** | `C-23, C-24` | 2 | 189,273 | 57,087 | 603,853 | 246,360 | **123,180.0** | 13 | 3 | **769.0s** |
| **Shard Author shard_31** | `C-26, C-27` | 2 | 66,431 | 36,009 | 116,652 | 102,440 | **51,220.0** | 5 | 0 | **253.0s** |
| **Shard Author shard_32** | `C-01, H-03` | 2 | 141,025 | 90,087 | 978,146 | 231,112 | **115,556.0** | 15 | 4 | **916.0s** |
| **Shard Author shard_33** | `H-04, C-06` | 2 | 138,581 | 89,477 | 1,267,193 | 228,058 | **114,029.0** | 16 | 4 | **862.0s** |
| **Shard Author shard_34** | `C-11, H-05` | 2 | 73,069 | 42,089 | 180,255 | 115,158 | **57,579.0** | 6 | 1 | **388.0s** |
| **Shard Author shard_35** | `C-14, H-07` | 2 | 96,507 | 46,861 | 238,203 | 143,368 | **71,684.0** | 7 | 1 | **342.0s** |
| **Shard Author shard_36** | `C-17, H-08` | 2 | 127,325 | 67,406 | 709,295 | 194,731 | **97,365.5** | 12 | 2 | **697.0s** |
| **Shard Author shard_37** | `C-22, H-11` | 2 | 96,698 | 44,407 | 286,050 | 141,105 | **70,552.5** | 8 | 1 | **378.0s** |
| **Shard Author shard_38** | `C-25, H-12` | 2 | 80,678 | 51,260 | 145,532 | 131,938 | **65,969.0** | 5 | 0 | **353.0s** |
| **Shard Author shard_39** | `H-01, H-02` | 2 | 93,534 | 42,122 | 330,727 | 135,656 | **67,828.0** | 9 | 1 | **349.0s** |
| **Shard Author shard_40** | `H-09, H-10` | 2 | 156,958 | 81,170 | 1,750,624 | 238,128 | **119,064.0** | 22 | 5 | **846.0s** |
| **Shard Author shard_01** | `Hab-01` | 1 | 78,416 | 34,871 | 93,559 | 113,287 | **113,287.0** | 5 | 0 | **254.0s** |
| **Shard Author shard_02** | `Hab-02` | 1 | 130,907 | 73,479 | 779,653 | 204,386 | **204,386.0** | 13 | 3 | **833.0s** |
| **Shard Author shard_03** | `Hab-03` | 1 | 86,913 | 46,147 | 57,812 | 133,060 | **133,060.0** | 4 | 0 | **346.0s** |
| **Shard Author shard_04** | `Hab-04` | 1 | 90,747 | 51,479 | 447,720 | 142,226 | **142,226.0** | 10 | 2 | **782.0s** |
| **Shard Author shard_05** | `Hab-05` | 1 | 102,543 | 53,772 | 304,561 | 156,315 | **156,315.0** | 8 | 2 | **495.0s** |
| **Shard Author shard_06** | `Hab-06` | 1 | 118,836 | 62,076 | 725,329 | 180,912 | **180,912.0** | 13 | 2 | **737.0s** |
| **Shard Author shard_07** | `Hab-07` | 1 | 183,538 | 58,445 | 532,570 | 241,983 | **241,983.0** | 12 | 3 | **587.0s** |
| **Shard Author shard_08** | `Hab-08` | 1 | 133,768 | 58,050 | 442,800 | 191,818 | **191,818.0** | 11 | 3 | **724.0s** |
| **Shard Author shard_09** | `Hab-09` | 1 | 88,615 | 45,013 | 114,153 | 133,628 | **133,628.0** | 5 | 0 | **341.0s** |
| **Shard Author shard_10** | `Hab-10` | 1 | 69,379 | 28,822 | 40,630 | 98,201 | **98,201.0** | 4 | 0 | **255.0s** |
| **Shard Author shard_11** | `Hab-11` | 1 | 156,850 | 48,788 | 290,967 | 205,638 | **205,638.0** | 9 | 2 | **493.0s** |
| **Shard Author shard_12 🛑** | `Hab-12` | 1 | 230,682 | 149,684 | 3,469,095 | 380,366 | **380,366.0** | 32 | 8 | **1289.0s** |
| **Shard Author shard_13** | `Hab-13` | 1 | 81,844 | 37,764 | 99,832 | 119,608 | **119,608.0** | 5 | 0 | **389.0s** |
| **Shard Author shard_14** | `Hab-14` | 1 | 106,363 | 56,261 | 387,063 | 162,624 | **162,624.0** | 9 | 2 | **507.0s** |
| **Shard Author shard_15** | `Hab-15` | 1 | 83,319 | 39,373 | 103,398 | 122,692 | **122,692.0** | 5 | 0 | **273.0s** |
| **Shard Author shard_16** | `Hab-16` | 1 | 122,182 | 66,496 | 667,086 | 188,678 | **188,678.0** | 12 | 3 | **745.0s** |
| **Shard Author shard_17** | `Hab-17` | 1 | 163,466 | 57,253 | 782,130 | 220,719 | **220,719.0** | 15 | 2 | **873.0s** |
| **Shard Author shard_18** | `Hab-18` | 1 | 84,327 | 42,521 | 108,301 | 126,848 | **126,848.0** | 5 | 1 | **340.0s** |
| **Shard Author shard_19** | `Hab-19` | 1 | 88,865 | 44,810 | 114,427 | 133,675 | **133,675.0** | 5 | 0 | **308.0s** |
| **Shard Author shard_20** | `Hab-20` | 1 | 127,810 | 66,610 | 1,002,280 | 194,420 | **194,420.0** | 17 | 4 | **806.0s** |
| **Shard Author shard_21** | `Hab-21` | 1 | 75,122 | 38,007 | 53,878 | 113,129 | **113,129.0** | 4 | 0 | **304.0s** |
| **Shard Author shard_41** | `C-28` | 1 | 79,182 | 37,825 | 49,692 | 117,007 | **117,007.0** | 4 | 0 | **273.0s** |

---

### 3.4. Evaluación y Arbitraje de Blind Judges (Verificación Psicométrica Ciega)

> [!NOTE]
> **Dictamen de Blind Judges:** ✅ 100% ACUERDO AL PRIMER INTENTO (120/120 REACTIVOS)  
> Los 10 Blind Judges evaluaron el lote estratificado de 120 reactivos en 1 turno de razonamiento puro cada uno (0 búsquedas web, 100% aislamiento epistémico), logrando un acuerdo psicométrico del 100.0% (120/120) con 0 discrepancias frente al ground truth.

| Dimensión de Arbitraje Ciego | Valor Registrado | Observación Técnica |
| :--- | :--- | :--- |
| **Lote Estratificado Ciego** | `120 reactivos` (60 comps × 2) | Lote de evaluación sin soluciones (`judge_batch.json`) |
| **Subagentes Jueces Ciegos** | `10 jueces` | Aislamiento epistémico en Stage 5 |
| **Resultado al Primer Intento** | **`✅ 100% Limpio (Sin Discrepancias)`** | Sin discrepancias ni arbitraje necesario |
| **Iteraciones de Auto-Reparación** | `0 iteraciones` en sandbox | 0 requeridas |
| **Intervenciones del Supervisor** | 🛠️ `0 operaciones directas` | Ninguna (ejecución autónoma) |

#### Detalle de Acciones Registradas:
- 1. **Arbitraje Ciego (`05b_judge_compare.json`)**: 120/120 acuerdos (`100.0% agreement rate`, `0 discrepancias`).

---

## 4. Auditoría Forense del Orquestador y Catálogo de Intervenciones Manuales

### 4.1. Descomposición del Tiempo Total del Orquestador
- ⏱️ **Tiempo Total de Pared del Orquestador:** `38.15 min` (`2289.0s`)
- 💻 **Tiempo Activo Ejecutando Comandos CLI (`run.py`):** `1.4 min` (`82.0s`)
- 🛠️ **Tiempo Gastado en Intervenciones Manuales (Supervisor Repair):** **`0.0 min`** (`0.0s`)
- ⏳ **Tiempo Ocioso en Barreras de Sincronización (Esperando Subagentes):** `0.5 min` (`32.0s`)
- 🧠 **Tiempo de Inferencia y Razonamiento del Modelo:** `0.8 min` (`46.0s`)

### 4.2. Catálogo Cronológico de Reparaciones Manuales del Orquestador
Operaciones directas de edición de código ejecutadas por el orquestador: **`0`**

| Paso | Archivo Afectado | Tipo de Acción | Causa Raíz / Justificación Técnica | Herramienta | Tokens Paso |
| :---: | :--- | :--- | :--- | :--- | :--- |
| — | *Ninguna intervención registrada* | — | — | — | 0 |

---

## 5. Diagnóstico de Cuellos de Botella y Antipatrones Detectados

### 🛑 [HIGH] Straggler Crítico en Shards: Shard Author shard_12
- **Ámbito:** `Stage 3: Question Authoring`
- **Diagnóstico:** Shard Author shard_12 tardó 1289.0s frente a la mediana de 495.0s (+794.0s de retraso en la barrera). Determinó el tiempo total de pared de la etapa de autoría.

### 🛑 [HIGH] Antipatrón de Micro-Bucle Interactivo (32 turnos en Shard Author shard_12)
- **Ámbito:** `Shard Author shard_12`
- **Diagnóstico:** 1 subagentes realizaron > 30 turnos individuales (ej. Shard Author shard_12 con 32 turnos). Ocurre por bucles de depuración o escritura incremental en lugar de redactar por lotes atómicos.

### ⚠️ [MEDIUM] Fricción de Herramientas en 14 subagentes
- **Ámbito:** `Multiple Subagents`
- **Diagnóstico:** Subagentes como Shard Author shard_22 acumularon fallos en consola (5 errores), provocando reintentos e invalidación de caché.

---

## 6. Telemetría de Razonamiento Cognitivo (Thinking Traces)

- **Total de Turnos con Razonamiento:** `380 turnos`
- **Volumen Total de Razonamiento:** `2,012,216 caracteres`
- **Razonamiento del Orquestador:** `19 turnos` (5,564 chars)
- **Razonamiento de Subagentes:** `361 turnos` (2,006,652 chars)

| Agente / Subagente | Turnos de Thinking | Caracteres de Thinking | Trazas de Error Capturadas |
| :--- | :---: | :---: | :---: |
| **Cognitive Task Analysis Architect part_04** | 7 | 18,065 | ⚠️ 1 |
| **Cognitive Task Analysis Architect part_01** | 5 | 11,907 | 0 |
| **Cognitive Task Analysis Architect part_02** | 5 | 17,167 | 0 |
| **Cognitive Task Analysis Architect part_03** | 6 | 14,258 | 0 |
| **Cognitive Task Analysis Architect part_06** | 5 | 25,012 | 0 |
| **Cognitive Task Analysis Architect part_07** | 8 | 16,805 | ⚠️ 2 |
| **Cognitive Task Analysis Architect part_05** | 5 | 14,198 | 0 |
| **CTA Harmonizer** | 3 | 12,936 | 0 |
| **Shard Author shard_22** | 16 | 52,550 | ⚠️ 5 |
| **Shard Author shard_23** | 7 | 37,260 | ⚠️ 3 |
| **Shard Author shard_24** | 6 | 48,043 | ⚠️ 2 |
| **Shard Author shard_25** | 6 | 25,129 | ⚠️ 2 |
| **Shard Author shard_26** | 8 | 44,804 | ⚠️ 3 |
| **Shard Author shard_27** | 4 | 39,690 | 0 |
| **Shard Author shard_28** | 4 | 40,310 | 0 |
| **Shard Author shard_29** | 10 | 45,939 | ⚠️ 3 |
| **Shard Author shard_30** | 9 | 36,004 | ⚠️ 3 |
| **Shard Author shard_31** | 4 | 25,861 | 0 |
| **Shard Author shard_32** | 11 | 54,871 | ⚠️ 4 |
| **Shard Author shard_33** | 11 | 57,297 | ⚠️ 4 |
| **Shard Author shard_34** | 5 | 27,753 | ⚠️ 1 |
| **Shard Author shard_35** | 5 | 31,617 | ⚠️ 1 |
| **Shard Author shard_36** | 9 | 47,649 | ⚠️ 2 |
| **Shard Author shard_37** | 5 | 28,311 | ⚠️ 1 |
| **Shard Author shard_38** | 4 | 40,078 | 0 |
| **Shard Author shard_39** | 6 | 29,825 | ⚠️ 1 |
| **Shard Author shard_40** | 11 | 61,588 | ⚠️ 5 |
| **Shard Author shard_01** | 4 | 30,050 | 0 |
| **Shard Author shard_02** | 10 | 55,822 | ⚠️ 3 |
| **Shard Author shard_03** | 4 | 37,364 | 0 |
| **Shard Author shard_04** | 7 | 39,075 | ⚠️ 2 |
| **Shard Author shard_05** | 6 | 41,725 | ⚠️ 2 |
| **Shard Author shard_06** | 9 | 46,970 | ⚠️ 2 |
| **Shard Author shard_07** | 7 | 39,628 | ⚠️ 3 |
| **Shard Author shard_08** | 7 | 37,408 | ⚠️ 3 |
| **Shard Author shard_09** | 4 | 38,748 | 0 |
| **Shard Author shard_10** | 4 | 22,457 | 0 |
| **Shard Author shard_11** | 7 | 31,673 | ⚠️ 2 |
| **Shard Author shard_12** | 24 | 105,032 | ⚠️ 8 |
| **Shard Author shard_13** | 4 | 29,333 | 0 |
| **Shard Author shard_14** | 7 | 45,121 | ⚠️ 2 |
| **Shard Author shard_15** | 4 | 32,217 | 0 |
| **Shard Author shard_16** | 10 | 61,550 | ⚠️ 3 |
| **Shard Author shard_17** | 12 | 39,184 | ⚠️ 2 |
| **Shard Author shard_18** | 4 | 34,364 | ⚠️ 1 |
| **Shard Author shard_19** | 4 | 38,416 | 0 |
| **Shard Author shard_20** | 10 | 40,018 | ⚠️ 4 |
| **Shard Author shard_21** | 4 | 28,841 | 0 |
| **Shard Author shard_41** | 4 | 32,601 | 0 |
| **Blind Judge 01** | 2 | 5,709 | 0 |
| **Blind Judge 02** | 2 | 16,941 | 0 |
| **Blind Judge 03** | 2 | 33,713 | 0 |
| **Blind Judge 04** | 2 | 9,375 | 0 |
| **Blind Judge 05** | 2 | 23,548 | 0 |
| **Blind Judge 06** | 2 | 11,028 | 0 |
| **Blind Judge 07** | 2 | 44,142 | 0 |
| **Blind Judge 08** | 2 | 21,717 | 0 |
| **Blind Judge 09** | 2 | 8,957 | 0 |
| **Blind Judge 10** | 2 | 18,998 | 0 |

---
*Reporte forense determinista emitido por `c2c-run-auditor`.*