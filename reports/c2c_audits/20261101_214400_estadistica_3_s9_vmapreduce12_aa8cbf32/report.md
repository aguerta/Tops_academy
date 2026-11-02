# Informe de Auditoría Arquitectónica Forense: Rendimiento, Shards y Telemetría Multi-Agente
## Curso: Estadistica 3 S9 Vmapreduce12 (`estadistica_3_s9_vmapreduce12`)

**Fecha de Auditoría:** `2026-11-02 02:44:00 UTC`  
**Conversación Orquestadora:** [`aa8cbf32-3892-4628-a164-7a6cfa8f3c70`](conversation://aa8cbf32-3892-4628-a164-7a6cfa8f3c70)  
**Directorio de Trabajo Validado (Zero-Collision):** `D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_s9_vmapreduce12\work` (`match=True`)  
**Enfoque:** Telemetría Determinista de API, Subagentes, Shards, Latencias y Operaciones del Orquestador.

---

## 1. Consolidación de Métricas y Caracterización de Carga

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada** | `2 archivos` (80 págs / 0.93 MB) | Clases_sintetizadas_semana_9.pdf, EST3_LEC07_26.2_V2.pdf |
| **Requerimiento de Visión** | `0 páginas` (0 handouts) | Cuadrículas generadas para diagramas/fórmulas |
| **Corpus Sintetizado** | `0 caracteres` (0 palabras) | Texto consolidado tras ingesta y visión |
| **Competencias Extraídas** | **`45 competencias`** | Desglose pedagógico (Hechos, Conceptos, Habilidades) |
| **Shards Particionados** | **`29 shards`** | Unidades de trabajo concurrentes |
| **Subagentes Desplegados** | **`71 subagentes`** | Visión (0), CTA (6), Autores (29), Repairs (16), Jueces (20) |
| **Reactivos Finales Validados** | **`1030 preguntas`** | Evaluadas en sandbox |
| **Tokens Entrada (Subagentes)** | **`5,165,112` tokens** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`1,971,439` tokens** | Código de plantillas y JSON generado |
| **Tokens Caché (Leídos)** | **`31,844,687` tokens** | Caché de contexto reutilizado por la API |
| **Gran Total Tokens Activos** | **`7,675,235` tokens** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`39,519,922` tokens** | Consumo total de cuota facturable |

---

## 2. Ratios Unitarios Normalizados (Unit Economics)

Métricas normalizadas para comparación *apples-to-apples* frente a cursos de diferente volumen de contenido:

| Métrica Unitaria | Valor Obtenido | Interpretación de Eficiencia |
| :--- | :--- | :--- |
| **Tokens Totales por Pregunta** | **`38,368.9 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`7,451.7 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`878,220.5 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`87,980.5 tokens/comp`** | Costo puro de la etapa de autoría por competencia |
| **Tokens Totales por Página / Slide** | **`493,999.0 tokens/pág`** | Esfuerzo cognitivo por diapositiva original |
| **Segundos de Pared por Pregunta** | **`2.49 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`24.13 preg/min`** | Velocidad de producción del pipeline |
| **Factor de Aceleración Paralela** | **`6.29x`** | Relación tiempo cómputo vs tiempo de pared |

---

## 3. Desglose Forense por Etapas Críticas

### 3.0. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json` & `state.json`)
- **Snapshots de Etapa Verificados (`conversation_id` = `aa8cbf32`):** `8 etapas`
- **Estado Maestro (`work/state.json`):** `completed` (Etapa actual/final: `judge_compare`)

| Etapa (Snapshot) | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes Capturados | Artefactos / Metadatos de Etapa |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`00_prepare`** | `2026-11-02 02:01:18` | `0.3s` | `0` (`0` act) | 0 | `—` |
| **`00b_bootstrap`** | `2026-11-02 02:01:18` | `0.32s` | `0` (`0` act) | 0 | `lock_file=D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_s9_vmapreduce12\work\.c2c_subagent_lock.json` |
| **`01_cta`** | `2026-11-02 02:06:37` | `0.2s` | `1,267,954` (`558,135` act) | 5 | `needs_harmonize=True` |
| **`02_shard`** | `2026-11-02 02:08:30` | `0.04s` | `0` (`0` act) | 0 | `shards=29` |
| **`03_templates`** | `2026-11-02 02:40:48` | `29.85s` | `18,859,285` (`5,235,147` act) | 40 | `count=45` |
| **`04_build`** | `2026-11-02 02:41:00` | `5.25s` | `5,154,362` (`1,276,024` act) | 11 | `total_questions=1030` |
| **`05_verify`** | `2026-11-02 02:24:38` | `2.89s` | `1,504,792` (`614,068` act) | 11 | `verified_course_path=D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_s9_vmapreduce12\work\course_verified.json` |
| **`05b_judge_compare`** | `2026-11-02 02:26:29` | `0.11s` | `1,976,275` (`996,427` act) | 20 | `passed=True` |

---

### 3.1. Stage 1A: Preprocesamiento de Visión
- **Subagentes de Visión Desplegados:** `0 agentes en paralelo`
- **Tiempo de Pared de la Etapa (Máximo / Critical Path):** **`0.0s`** (`0.0 min`)
- **Agente Determinante del Camino Crítico:** `N/A`

| Subagente de Visión | Turnos | Tokens In | Tokens Out | Cache Leído | Total Activo | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |

---

### 3.2. Stage 1B: Análisis Cognitivo de Competencias (CTA)
- **Arquitectura:** `MAPREDUCE (5 Mappers + 1 Harmonizer)`
- **Tiempo de Pared Fase Mappers (Máximo):** **`275.0s`** (determinado por `Cognitive Task Analysis Architect part_03`)
- **Tiempo Fase Harmonizer (Barrera Síncrona):** **`75.0s`**
- **Tiempo de Pared Total de Etapa 1B:** **`350.0s`** (`5.8 min`)

| Subagente CTA | Rol / Sección | Turnos | Tokens In | Tokens Out | Cache Leído | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Cognitive Task Analysis Architect part_03** | Mapper | 6 | 84,328 | 41,099 | 165,836 | 1 | **275.0s** |
| **Cognitive Task Analysis Architect part_04** | Mapper | 5 | 75,222 | 31,499 | 118,213 | 0 | **219.0s** |
| **Cognitive Task Analysis Architect part_01** | Mapper | 7 | 84,987 | 31,609 | 175,112 | 2 | **230.0s** |
| **Cognitive Task Analysis Architect part_05** | Mapper | 6 | 82,589 | 29,022 | 110,603 | 0 | **201.0s** |
| **Cognitive Task Analysis Architect part_02** | Mapper | 6 | 68,995 | 28,785 | 140,055 | 1 | **216.0s** |
| **CTA Harmonizer** | Harmonizer | 7 | 54,678 | 9,609 | 158,829 | 1 | **75.0s** |

---

### 3.3. Stage 3: Autoría de Reactivos por Shard y Análisis por Competencia
- **Total de Shards Auditados:** `29 shards concurrentes`
- **Duración Mínima de Shard:** `190.0s` | **Mediana:** `311.0s`
- **Tiempo de Pared Máximo (Straggler Crítico):** **`454.0s`** (`7.6 min`) por `Shard Author shard_25`
- **Retraso de Sincronización Impuesto por el Straggler:** **`+143.0s`** frente a la mediana
- **Tokens Promedio por Competencia en Autores:** **`87,980.5 tokens/competencia`**

| Shard ID | Competencias Asignadas | Comps | Tokens In | Tokens Out | Cache Leído | Total Activo | Tokens / Comp | Turnos | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Shard Author shard_14** | `H-04, H-05, H-06` | 3 | 96,386 | 53,482 | 532,285 | 149,868 | **49,956.0** | 10 | 2 | **361.0s** |
| **Shard Author shard_15** | `C-04, C-05` | 2 | 107,440 | 64,539 | 634,146 | 171,979 | **85,989.5** | 12 | 2 | **445.0s** |
| **Shard Author shard_16** | `C-06, C-07` | 2 | 66,780 | 34,271 | 121,526 | 101,051 | **50,525.5** | 5 | 0 | **221.0s** |
| **Shard Author shard_17** | `C-08, C-09` | 2 | 95,572 | 52,785 | 442,308 | 148,357 | **74,178.5** | 9 | 1 | **365.0s** |
| **Shard Author shard_18** | `C-11, C-12` | 2 | 90,759 | 53,899 | 434,067 | 144,658 | **72,329.0** | 9 | 2 | **367.0s** |
| **Shard Author shard_19** | `C-14, C-15` | 2 | 80,639 | 48,444 | 148,905 | 129,083 | **64,541.5** | 5 | 0 | **322.0s** |
| **Shard Author shard_20** | `C-16, C-17` | 2 | 99,697 | 52,867 | 586,339 | 152,564 | **76,282.0** | 11 | 1 | **385.0s** |
| **Shard Author shard_21** | `C-01, H-01` | 2 | 83,633 | 40,469 | 472,317 | 124,102 | **62,051.0** | 11 | 2 | **316.0s** |
| **Shard Author shard_22** | `H-02, C-02` | 2 | 166,197 | 49,227 | 570,734 | 215,424 | **107,712.0** | 12 | 1 | **348.0s** |
| **Shard Author shard_23** | `C-03, H-03` | 2 | 78,909 | 42,250 | 506,134 | 121,159 | **60,579.5** | 11 | 2 | **310.0s** |
| **Shard Author shard_24** | `C-10, H-07` | 2 | 90,719 | 51,817 | 418,469 | 142,536 | **71,268.0** | 9 | 1 | **354.0s** |
| **Shard Author shard_25 🛑** | `C-13, H-08` | 2 | 184,411 | 68,150 | 490,483 | 252,561 | **126,280.5** | 10 | 2 | **454.0s** |
| **Shard Author shard_26** | `C-18, H-11` | 2 | 113,498 | 60,983 | 878,985 | 174,481 | **87,240.5** | 14 | 2 | **423.0s** |
| **Shard Author shard_27** | `C-19, H-12` | 2 | 70,542 | 38,424 | 129,009 | 108,966 | **54,483.0** | 5 | 0 | **244.0s** |
| **Shard Author shard_28** | `H-09, H-10` | 2 | 68,374 | 36,099 | 124,166 | 104,473 | **52,236.5** | 5 | 0 | **235.0s** |
| **Shard Author shard_01** | `Hab-01` | 1 | 59,233 | 28,529 | 104,727 | 87,762 | **87,762.0** | 5 | 0 | **193.0s** |
| **Shard Author shard_02** | `Hab-02` | 1 | 78,238 | 40,769 | 73,053 | 119,007 | **119,007.0** | 5 | 1 | **285.0s** |
| **Shard Author shard_03** | `Hab-03` | 1 | 58,754 | 28,384 | 103,433 | 87,138 | **87,138.0** | 5 | 0 | **190.0s** |
| **Shard Author shard_04** | `Hab-04` | 1 | 60,727 | 30,476 | 107,211 | 91,203 | **91,203.0** | 5 | 0 | **200.0s** |
| **Shard Author shard_05** | `Hab-05` | 1 | 60,946 | 30,692 | 107,928 | 91,638 | **91,638.0** | 5 | 0 | **210.0s** |
| **Shard Author shard_06** | `Hab-06` | 1 | 186,222 | 53,555 | 871,107 | 239,777 | **239,777.0** | 17 | 3 | **382.0s** |
| **Shard Author shard_07** | `Hab-07` | 1 | 60,346 | 29,793 | 107,678 | 90,139 | **90,139.0** | 5 | 0 | **199.0s** |
| **Shard Author shard_08** | `Hab-08` | 1 | 74,456 | 44,132 | 135,157 | 118,588 | **118,588.0** | 5 | 0 | **277.0s** |
| **Shard Author shard_09** | `Hab-09` | 1 | 75,657 | 41,762 | 288,323 | 117,419 | **117,419.0** | 8 | 1 | **311.0s** |
| **Shard Author shard_10** | `Hab-10` | 1 | 93,894 | 47,093 | 622,988 | 140,987 | **140,987.0** | 13 | 2 | **344.0s** |
| **Shard Author shard_11** | `Hab-11` | 1 | 152,983 | 54,909 | 394,810 | 207,892 | **207,892.0** | 10 | 2 | **377.0s** |
| **Shard Author shard_12** | `Hab-12` | 1 | 64,284 | 34,094 | 114,752 | 98,378 | **98,378.0** | 5 | 0 | **231.0s** |
| **Shard Author shard_13** | `Hab-13` | 1 | 83,448 | 35,818 | 100,242 | 119,266 | **119,266.0** | 5 | 0 | **239.0s** |
| **Shard Author shard_29** | `C-20` | 1 | 69,364 | 39,303 | 124,518 | 108,667 | **108,667.0** | 5 | 0 | **258.0s** |

---

### 3.3b. Stage 3B: Remediación y Repair Engineers (Ingenieros de Reparación)
- **Total de Repair Engineers Desplegados:** `16 subagentes`
- **Duración Mínima:** `7.0s` | **Mediana:** `187.0s` | **Máxima:** `304.0s` (`5.1 min`)
- **Tokens Activos Totales en Reparación:** `1,558,579 tokens`
- **Agente Determinante del Retraso:** `Repair Engineer (HAB09)`

| Repair Engineer | Turnos | Tokens In | Tokens Out | Cache Leído | Total Activo | Errores | Duración |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Repair Engineer (C16)** | 11 | 96,103 | 23,201 | 366,708 | 119,304 | 0 | **170.0s** |
| **Repair Engineer (C16)** | 8 | 68,079 | 27,185 | 198,520 | 95,264 | 1 | **187.0s** |
| **Repair Engineer (H03)** | 8 | 53,067 | 14,208 | 189,252 | 67,275 | 1 | **114.0s** |
| **Repair Engineer (HAB04)** | 11 | 101,882 | 41,730 | 425,248 | 143,612 | 1 | **262.0s** |
| **Repair Engineer (HAB05)** | 17 | 147,832 | 37,192 | 1,083,574 | 185,024 | 1 | **302.0s** |
| **Repair Engineer (HAB09)** | 9 | 101,501 | 43,577 | 342,293 | 145,078 | 1 | **304.0s** |
| **Repair Engineer (C16)** | 8 | 69,565 | 28,505 | 196,479 | 98,070 | 1 | **189.0s** |
| **Repair Engineer (H03)** | 7 | 51,448 | 13,354 | 148,512 | 64,802 | 1 | **93.0s** |
| **Repair Engineer (HAB04)** | 11 | 84,304 | 40,251 | 378,865 | 124,555 | 1 | **284.0s** |
| **Repair Engineer (HAB05)** | 12 | 95,420 | 42,679 | 440,186 | 138,099 | 1 | **247.0s** |
| **Repair Engineer (HAB09)** | 6 | 64,708 | 30,233 | 108,701 | 94,941 | 1 | **200.0s** |
| **Repair Engineer (C16)** | 6 | 41,565 | 2,003 | 99,053 | 43,568 | 0 | **22.0s** |
| **Repair Engineer (H03)** | 3 | 50,923 | 2,532 | 0 | 53,455 | 0 | **7.0s** |
| **Repair Engineer (HAB04)** | 3 | 55,860 | 2,861 | 0 | 58,721 | 0 | **8.0s** |
| **Repair Engineer (HAB05)** | 4 | 61,567 | 1,934 | 20,379 | 63,501 | 0 | **12.0s** |
| **Repair Engineer (HAB09)** | 4 | 60,982 | 2,328 | 20,456 | 63,310 | 0 | **12.0s** |

---

### 3.4. Evaluación y Arbitraje de Blind Judges (Verificación Psicométrica Ciega)

> [!NOTE]
> **Dictamen de Blind Judges:** ✅ 100% ACUERDO AL PRIMER INTENTO (120/120 REACTIVOS)  
> Los 20 Blind Judges evaluaron el lote estratificado de 120 reactivos en 1 turno de razonamiento puro cada uno (0 búsquedas web, 100% aislamiento epistémico), logrando un acuerdo psicométrico del 100.0% (120/120) con 0 discrepancias frente al ground truth.

| Dimensión de Arbitraje Ciego | Valor Registrado | Observación Técnica |
| :--- | :--- | :--- |
| **Lote Estratificado Ciego** | `120 reactivos` (45 comps × 2) | Lote de evaluación sin soluciones (`judge_batch.json`) |
| **Subagentes Jueces Ciegos** | `20 jueces` | Aislamiento epistémico en Stage 5 |
| **Resultado al Primer Intento** | **`✅ 100% Limpio (Sin Discrepancias)`** | Sin discrepancias ni arbitraje necesario |
| **Iteraciones de Auto-Reparación** | `0 iteraciones` en sandbox | 0 requeridas |
| **Intervenciones del Supervisor** | 🛠️ `0 operaciones directas` | Ninguna (ejecución autónoma) |

#### Detalle de Acciones Registradas:
- 1. **Arbitraje Ciego (`05b_judge_compare.json`)**: 120/120 acuerdos (`100.0% agreement rate`, `0 discrepancias`).

---

## 4. Auditoría Forense del Orquestador y Catálogo de Intervenciones Manuales

### 4.1. Descomposición del Tiempo Total del Orquestador
- ⏱️ **Tiempo Total de Pared del Orquestador:** `42.68 min` (`2561.0s`)
- 💻 **Tiempo Activo Ejecutando Comandos CLI (`run.py`):** `4.7 min` (`282.0s`)
- 🛠️ **Tiempo Gastado en Intervenciones Manuales (Supervisor Repair):** **`0.0 min`** (`0.0s`)
- ⏳ **Tiempo Ocioso en Barreras de Sincronización (Esperando Subagentes):** `1.3 min` (`79.0s`)
- 🧠 **Tiempo de Inferencia y Razonamiento del Modelo:** `2.0 min` (`121.0s`)

### 4.2. Catálogo Cronológico de Reparaciones Manuales del Orquestador
Operaciones directas de edición de código ejecutadas por el orquestador: **`0`**

| Paso | Archivo Afectado | Tipo de Acción | Causa Raíz / Justificación Técnica | Herramienta | Tokens Paso |
| :---: | :--- | :--- | :--- | :--- | :--- |
| — | *Ninguna intervención registrada* | — | — | — | 0 |

---

## 5. Diagnóstico de Cuellos de Botella y Antipatrones Detectados

### 🛑 [HIGH] Straggler Crítico en Shards: Shard Author shard_25
- **Ámbito:** `Stage 3: Question Authoring`
- **Diagnóstico:** Shard Author shard_25 tardó 454.0s frente a la mediana de 311.0s (+143.0s de retraso en la barrera). Determinó el tiempo total de pared de la etapa de autoría.

### ⚠️ [MEDIUM] Fricción de Herramientas en 1 subagentes
- **Ámbito:** `Multiple Subagents`
- **Diagnóstico:** Subagentes como Shard Author shard_06 acumularon fallos en consola (3 errores), provocando reintentos e invalidación de caché.

---

## 6. Telemetría de Razonamiento Cognitivo (Thinking Traces)

- **Total de Turnos con Razonamiento:** `351 turnos`
- **Volumen Total de Razonamiento:** `1,589,743 caracteres`
- **Razonamiento del Orquestador:** `35 turnos` (10,042 chars)
- **Razonamiento de Subagentes:** `316 turnos` (1,579,701 chars)

| Agente / Subagente | Turnos de Thinking | Caracteres de Thinking | Trazas de Error Capturadas |
| :--- | :---: | :---: | :---: |
| **Cognitive Task Analysis Architect part_03** | 6 | 26,928 | ⚠️ 1 |
| **Cognitive Task Analysis Architect part_04** | 5 | 25,327 | 0 |
| **Cognitive Task Analysis Architect part_01** | 4 | 18,472 | ⚠️ 2 |
| **Cognitive Task Analysis Architect part_05** | 5 | 16,002 | 0 |
| **Cognitive Task Analysis Architect part_02** | 6 | 15,556 | ⚠️ 1 |
| **CTA Harmonizer** | 3 | 7,187 | ⚠️ 1 |
| **Shard Author shard_14** | 8 | 41,139 | ⚠️ 2 |
| **Shard Author shard_15** | 8 | 43,867 | ⚠️ 2 |
| **Shard Author shard_16** | 4 | 25,560 | 0 |
| **Shard Author shard_17** | 7 | 52,649 | ⚠️ 1 |
| **Shard Author shard_18** | 7 | 46,025 | ⚠️ 2 |
| **Shard Author shard_19** | 4 | 47,734 | 0 |
| **Shard Author shard_20** | 7 | 47,860 | ⚠️ 1 |
| **Shard Author shard_21** | 8 | 29,884 | ⚠️ 2 |
| **Shard Author shard_22** | 7 | 44,409 | ⚠️ 1 |
| **Shard Author shard_23** | 8 | 33,605 | ⚠️ 2 |
| **Shard Author shard_24** | 5 | 44,232 | ⚠️ 1 |
| **Shard Author shard_25** | 8 | 55,281 | ⚠️ 2 |
| **Shard Author shard_26** | 8 | 56,088 | ⚠️ 2 |
| **Shard Author shard_27** | 4 | 32,936 | 0 |
| **Shard Author shard_28** | 4 | 27,690 | 0 |
| **Shard Author shard_01** | 4 | 21,193 | 0 |
| **Shard Author shard_02** | 4 | 39,345 | ⚠️ 1 |
| **Shard Author shard_03** | 4 | 23,222 | 0 |
| **Shard Author shard_04** | 4 | 31,342 | 0 |
| **Shard Author shard_05** | 4 | 27,123 | 0 |
| **Shard Author shard_06** | 10 | 35,915 | ⚠️ 3 |
| **Shard Author shard_07** | 4 | 27,549 | 0 |
| **Shard Author shard_08** | 4 | 42,602 | 0 |
| **Shard Author shard_09** | 6 | 35,478 | ⚠️ 1 |
| **Shard Author shard_10** | 6 | 39,944 | ⚠️ 2 |
| **Shard Author shard_11** | 6 | 52,344 | ⚠️ 2 |
| **Shard Author shard_12** | 4 | 29,483 | 0 |
| **Shard Author shard_13** | 4 | 30,655 | 0 |
| **Shard Author shard_29** | 4 | 32,868 | 0 |
| **Blind Judge 01** | 3 | 4,605 | 0 |
| **Blind Judge 02** | 2 | 5,527 | 0 |
| **Blind Judge 03** | 2 | 5,405 | 0 |
| **Blind Judge 04** | 2 | 6,083 | 0 |
| **Blind Judge 05** | 2 | 8,281 | 0 |
| **Blind Judge 06** | 2 | 3,018 | 0 |
| **Blind Judge 07** | 2 | 5,145 | 0 |
| **Blind Judge 08** | 2 | 4,017 | 0 |
| **Blind Judge 09** | 2 | 11,137 | 0 |
| **Blind Judge 10** | 2 | 4,106 | 0 |
| **Repair Engineer (C16)** | 7 | 15,188 | 0 |
| **Blind Judge 01** | 2 | 3,899 | 0 |
| **Blind Judge 02** | 2 | 3,921 | 0 |
| **Blind Judge 03** | 2 | 3,455 | 0 |
| **Blind Judge 04** | 2 | 3,749 | 0 |
| **Blind Judge 05** | 2 | 3,990 | 0 |
| **Blind Judge 06** | 2 | 2,701 | 0 |
| **Blind Judge 07** | 2 | 3,952 | 0 |
| **Blind Judge 08** | 2 | 5,027 | 0 |
| **Blind Judge 09** | 2 | 4,560 | 0 |
| **Blind Judge 10** | 2 | 5,236 | 0 |
| **Repair Engineer (C16)** | 5 | 17,887 | ⚠️ 1 |
| **Repair Engineer (H03)** | 7 | 10,377 | ⚠️ 1 |
| **Repair Engineer (HAB04)** | 7 | 31,378 | ⚠️ 1 |
| **Repair Engineer (HAB05)** | 8 | 31,587 | ⚠️ 1 |
| **Repair Engineer (HAB09)** | 7 | 37,314 | ⚠️ 1 |
| **Repair Engineer (C16)** | 5 | 21,017 | ⚠️ 1 |
| **Repair Engineer (H03)** | 6 | 9,416 | ⚠️ 1 |
| **Repair Engineer (HAB04)** | 7 | 35,008 | ⚠️ 1 |
| **Repair Engineer (HAB05)** | 7 | 33,899 | ⚠️ 1 |
| **Repair Engineer (HAB09)** | 5 | 24,378 | ⚠️ 1 |
| **Repair Engineer (C16)** | 2 | 574 | 0 |
| **Repair Engineer (H03)** | 2 | 1,859 | 0 |
| **Repair Engineer (HAB04)** | 2 | 1,867 | 0 |
| **Repair Engineer (HAB05)** | 2 | 1,049 | 0 |
| **Repair Engineer (HAB09)** | 2 | 1,595 | 0 |

---
*Reporte forense determinista emitido por `c2c-run-auditor`.*