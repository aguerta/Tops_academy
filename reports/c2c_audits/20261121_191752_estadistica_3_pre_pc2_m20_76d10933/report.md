# Informe de Auditoría Arquitectónica Forense: Rendimiento, Shards y Telemetría Multi-Agente
## Curso: Estadistica 3 Pre Pc2 M20 (`estadistica_3_pre_pc2_m20`)

**Fecha de Auditoría:** `2026-11-22 00:17:52 UTC`  
**Conversación Orquestadora:** [`76d10933-dd9f-42b3-bdf8-c3caaeb435b1`](conversation://76d10933-dd9f-42b3-bdf8-c3caaeb435b1)  
**Directorio de Trabajo Validado (Zero-Collision):** `D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_pre_pc2_m20\work` (`match=True`)  
**Enfoque:** Telemetría Determinista de API, Subagentes, Shards, Latencias, Costos USD (Gemini 4 Hydrogen) y Operaciones del Orquestador.

---

## 1. Consolidación de Métricas y Caracterización de Carga

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada** | `4 archivos` (129 págs / 1.88 MB) | 01_semana_9_apuntes.pdf, 02_EST3_LEC07_26.2_V2.pdf, 03_EST3_LEC08_26.2_v1.pdf, 04_semana_10_apuntes.pdf |
| **Requerimiento de Visión** | `0 páginas` (0 handouts) | Cuadrículas generadas para diagramas/fórmulas |
| **Corpus Sintetizado** | `0 caracteres` (0 palabras) | Texto consolidado tras ingesta y visión |
| **Competencias Extraídas** | **`58 competencias`** | Desglose pedagógico (Hechos, Conceptos, Habilidades) |
| **Shards Particionados** | **`23 shards`** | Unidades de trabajo concurrentes |
| **Subagentes Desplegados** | **`55 subagentes`** | Visión (0), CTA (9), Autores (23), Repairs (6), Jueces (17) |
| **Reactivos Finales Validados** | **`1396 preguntas`** | Evaluadas en sandbox |
| **Tokens Entrada (Subagentes)** | **`3,262,703` tokens** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`1,332,687` tokens** | Código de plantillas y JSON generado |
| **Tokens Caché (Leídos)** | **`19,219,260` tokens** | Caché de contexto reutilizado por la API |
| **Gran Total Tokens Activos** | **`4,883,378` tokens** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`24,102,638` tokens** | Consumo total de cuota facturable |
| **Costo Estimado Total (Gemini 4 Hydrogen)** | **`$17.0826 USD`** | In: `$5.2460` (`$1.50/1M`), Out+Think: `$10.3951` (`$7.50/1M`), Cache: `$1.4414` (`$0.075/1M`) |

---

## 2. Ratios Unitarios Normalizados (Unit Economics)

Métricas normalizadas para comparación *apples-to-apples* frente a cursos de diferente volumen de contenido:

| Métrica Unitaria | Valor Obtenido | Interpretación de Eficiencia |
| :--- | :--- | :--- |
| **Tokens Totales por Pregunta** | **`17,265.5 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`3,498.1 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`415,562.7 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`54,806.4 tokens/comp`** | Costo puro de la etapa de autoría por competencia |
| **Tokens Totales por Página / Slide** | **`186,842.2 tokens/pág`** | Esfuerzo cognitivo por diapositiva original |
| **Costo Estimado por Pregunta (Hydrogen)** | **`$0.0122 USD/preg`** | Costo monetario valorizado por reactivo |
| **Costo Estimado por Competencia (Hydrogen)** | **`$0.2945 USD/comp`** | Costo monetario valorizado por competencia |
| **Segundos de Pared por Pregunta** | **`1.03 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`58.33 preg/min`** | Velocidad de producción del pipeline |
| **Factor de Aceleración Paralela** | **`6.27x`** | Relación tiempo cómputo vs tiempo de pared |

---

## 3. Desglose Forense por Etapas Críticas

### 3.0a. Valorización Monetaria por Etapa (Tarifas Gemini 4 Hydrogen)
> Tarifas oficiales aplicables: Entrada `$1.50/1M`, Caché leído `$0.075/1M`, Salida (incl. thinking) `$7.50/1M`.

| Etapa / Rol | Agentes | Tokens Entrada | Tokens Salida | Caché Leído | Costo Estimado (USD) | % del Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Stage 1A: Visión** | 0 | 0 | 0 | 0 | **`$0.0000`** | 0.0% |
| **Stage 1B: CTA Architects** | 9 | 446,412 | 111,043 | 1,087,299 | **`$1.5840`** | 9.3% |
| **Stage 3: Shard Authors** | 23 | 2,109,308 | 1,069,462 | 12,060,811 | **`$12.0895`** | 70.8% |
| **Stage 3B: Repair Engineers** | 6 | 279,766 | 29,786 | 837,347 | **`$0.7058`** | 4.1% |
| **Stage 5: Blind Judges** | 17 | 427,217 | 122,396 | 491,949 | **`$1.5957`** | 9.3% |
| **Orquestador Principal (Director)** | 1 | 234,658 | 53,330 | 4,741,854 | **`$1.1076`** | 6.5% |
| **TOTAL CORRIDA (Gemini 4 Hydrogen)** | **56** | **3,497,361** | **1,386,017** | **19,219,260** | **`$17.0826 USD`** | **100.0%** |

### 3.0. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json` & `state.json`)
- **Snapshots de Etapa Verificados (`conversation_id` = `76d10933`):** `9 etapas`
- **Estado Maestro (`work/state.json`):** `completed` (Etapa actual/final: `publish`)

| Etapa (Snapshot) | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes Capturados | Artefactos / Metadatos de Etapa |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`00_prepare`** | `2026-11-21 23:54:02` | `0.33s` | `0` (`0` act) | 0 | `—` |
| **`00b_bootstrap`** | `2026-11-21 23:54:02` | `0.38s` | `0` (`0` act) | 0 | `lock_file=D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_pre_pc2_m20\work\.c2c_subagent_lock.json` |
| **`01_cta`** | `2026-11-21 23:56:37` | `0.41s` | `0` (`0` act) | 0 | `needs_harmonize=True` |
| **`02_shard`** | `2026-11-21 23:58:26` | `0.05s` | `0` (`0` act) | 0 | `shards=23` |
| **`03_templates`** | `2026-11-22 00:13:18` | `0.42s` | `0` (`0` act) | 0 | `count=58` |
| **`04_build`** | `2026-11-22 00:13:42` | `23.32s` | `0` (`0` act) | 0 | `total_questions=1396` |
| **`05_verify`** | `2026-11-22 00:13:44` | `2.38s` | `0` (`0` act) | 0 | `verified_course_path=D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_pre_pc2_m20\work\course_verified.json` |
| **`05b_judge_compare`** | `2026-11-22 00:06:38` | `0.13s` | `0` (`0` act) | 0 | `passed=False` |
| **`06_publish`** | `2026-11-22 00:13:50` | `5.23s` | `0` (`0` act) | 0 | `published_json=D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_pre_pc2_m20.json` |

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
- **Arquitectura:** `MAPREDUCE (8 Mappers + 1 Harmonizer)`
- **Tiempo de Pared Fase Mappers (Máximo):** **`96.0s`** (determinado por `Cognitive Task Analysis Architect part_07`)
- **Tiempo Fase Harmonizer (Barrera Síncrona):** **`75.0s`**
- **Tiempo de Pared Total de Etapa 1B:** **`171.0s`** (`2.9 min`)
- **Costo Estimado Etapa 1B (Gemini 4 Hydrogen):** **`$1.5840 USD`**

| Subagente CTA | Rol / Sección | Turnos | Tokens In | Tokens Out | Cache Leído | Costo (USD) | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| **Cognitive Task Analysis Architect part_06** | Mapper | 4 | 47,237 | 13,808 | 85,339 | `$0.1808` | 0 | **73.0s** |
| **Cognitive Task Analysis Architect part_03** | Mapper | 4 | 40,669 | 10,957 | 74,991 | `$0.1488` | 0 | **73.0s** |
| **Cognitive Task Analysis Architect part_04** | Mapper | 4 | 42,491 | 12,584 | 77,184 | `$0.1639` | 0 | **68.0s** |
| **Cognitive Task Analysis Architect part_01** | Mapper | 4 | 48,403 | 11,363 | 90,181 | `$0.1646` | 0 | **74.0s** |
| **Cognitive Task Analysis Architect part_05** | Mapper | 4 | 37,108 | 11,118 | 67,867 | `$0.1441` | 0 | **63.0s** |
| **Cognitive Task Analysis Architect part_08** | Mapper | 6 | 51,503 | 12,869 | 173,593 | `$0.1868` | 1 | **95.0s** |
| **Cognitive Task Analysis Architect part_07** | Mapper | 6 | 50,982 | 13,275 | 165,959 | `$0.1885` | 3 | **96.0s** |
| **Cognitive Task Analysis Architect part_02** | Mapper | 4 | 44,178 | 12,276 | 80,996 | `$0.1644` | 0 | **74.0s** |
| **CTA Harmonizer** | Harmonizer | 6 | 83,841 | 12,793 | 271,189 | `$0.2420` | 0 | **75.0s** |

---

### 3.3. Stage 3: Autoría de Reactivos por Shard y Análisis por Competencia
- **Total de Shards Auditados:** `23 shards concurrentes`
- **Tasa de Aprobación en 1ra Compilación:** **`0/23 (0.0%)`** (Reglas en 1er fallo: `[TPL-STEM-VARIANT-PARITY]` (15), `[GENERAL]` (14), `[TPL-VAR]` (12), `[PRECHECK]` (10), `[TPL-ORPHAN-VARS]` (9), `[TPL-STEM-GRAMMAR]` (9))
- **Duración Mínima de Shard:** `183.0s` | **Mediana:** `268.0s`
- **Tiempo de Pared Máximo (Straggler Crítico):** **`415.0s`** (`6.9 min`) por `Shard Author shard_16`
- **Retraso de Sincronización Impuesto por el Straggler:** **`+147.0s`** frente a la mediana
- **Tokens Promedio por Competencia en Autores:** **`54,806.4 tokens/competencia`**
- **Costo Estimado Etapa 3 (Gemini 4 Hydrogen):** **`$12.0895 USD`**

| Shard ID | Competencias Asignadas | Comps | Tokens In | Tokens Out | Cache Leído | Total Activo | Costo (USD) | Tokens / Comp | Turnos | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :--- | :--- | :--- |
| **Shard Author shard_12** | `C-10, C-11, C-01` | 3 | 91,104 | 53,666 | 382,367 | 144,770 | `$0.5678` | **48,256.7** | 8 | 1 | **281.0s** |
| **Shard Author shard_13** | `C-04, C-05, C-06` | 3 | 94,378 | 55,309 | 402,896 | 149,687 | `$0.5866` | **49,895.7** | 8 | 1 | **299.0s** |
| **Shard Author shard_14** | `H-02, C-22, C-23` | 3 | 107,763 | 53,918 | 744,971 | 161,681 | `$0.6219` | **53,893.7** | 12 | 2 | **316.0s** |
| **Shard Author shard_01** | `Hab-03, Hab-04` | 2 | 83,649 | 46,415 | 362,938 | 130,064 | `$0.5008` | **65,032.0** | 8 | 1 | **259.0s** |
| **Shard Author shard_02** | `Hab-23, Hab-24` | 2 | 106,228 | 56,296 | 497,500 | 162,524 | `$0.6189` | **81,262.0** | 9 | 1 | **305.0s** |
| **Shard Author shard_03** | `Hab-01, Hab-02` | 2 | 72,954 | 37,455 | 283,736 | 110,409 | `$0.4116` | **55,204.5** | 7 | 1 | **200.0s** |
| **Shard Author shard_04** | `Hab-05, Hab-06` | 2 | 70,397 | 31,178 | 383,505 | 101,575 | `$0.3682` | **50,787.5** | 9 | 1 | **201.0s** |
| **Shard Author shard_05** | `Hab-07, Hab-10` | 2 | 61,952 | 24,915 | 303,026 | 86,867 | `$0.3025` | **43,433.5** | 8 | 1 | **183.0s** |
| **Shard Author shard_06** | `Hab-11, Hab-12` | 2 | 70,090 | 27,556 | 459,369 | 97,646 | `$0.3463` | **48,823.0** | 11 | 2 | **233.0s** |
| **Shard Author shard_07** | `Hab-13, Hab-14` | 2 | 70,268 | 27,773 | 416,344 | 98,041 | `$0.3449` | **49,020.5** | 10 | 2 | **210.0s** |
| **Shard Author shard_08** | `Hab-15, Hab-16` | 2 | 79,097 | 43,207 | 344,885 | 122,304 | `$0.4686` | **61,152.0** | 8 | 1 | **216.0s** |
| **Shard Author shard_09** | `Hab-17, Hab-18` | 2 | 87,064 | 44,522 | 424,262 | 131,586 | `$0.4963` | **65,793.0** | 9 | 1 | **223.0s** |
| **Shard Author shard_10** | `Hab-19, Hab-20` | 2 | 69,410 | 29,265 | 324,292 | 98,675 | `$0.3479` | **49,337.5** | 8 | 1 | **194.0s** |
| **Shard Author shard_11** | `Hab-21, Hab-22` | 2 | 85,658 | 43,152 | 421,412 | 128,810 | `$0.4837` | **64,405.0** | 9 | 2 | **250.0s** |
| **Shard Author shard_15** | `C-24, C-32, C-25` | 3 | 112,408 | 49,124 | 848,944 | 161,532 | `$0.6007` | **53,844.0** | 13 | 2 | **268.0s** |
| **Shard Author shard_16 🛑** | `C-33, C-35, C-36` | 3 | 135,206 | 78,746 | 1,050,161 | 213,952 | `$0.8722` | **71,317.3** | 14 | 3 | **415.0s** |
| **Shard Author shard_17** | `C-07, C-08, C-09` | 3 | 101,160 | 58,720 | 612,210 | 159,880 | `$0.6381` | **53,293.3** | 10 | 3 | **322.0s** |
| **Shard Author shard_18** | `C-03, C-14, C-17` | 3 | 68,097 | 30,721 | 315,506 | 98,818 | `$0.3562` | **32,939.3** | 8 | 1 | **200.0s** |
| **Shard Author shard_19** | `C-18, C-19, C-20` | 3 | 129,266 | 67,377 | 922,228 | 196,643 | `$0.7684` | **65,547.7** | 13 | 2 | **359.0s** |
| **Shard Author shard_20** | `C-26, C-27, C-28` | 3 | 117,916 | 51,513 | 870,150 | 169,429 | `$0.6285` | **56,476.3** | 13 | 2 | **285.0s** |
| **Shard Author shard_21** | `C-29, C-30, C-31` | 3 | 95,419 | 58,160 | 398,388 | 153,579 | `$0.6092` | **51,193.0** | 8 | 1 | **288.0s** |
| **Shard Author shard_22** | `C-37, C-38, H-03` | 3 | 111,367 | 49,174 | 922,414 | 160,541 | `$0.6050` | **53,513.7** | 14 | 2 | **289.0s** |
| **Shard Author shard_23** | `PRE-01, H-01, C-02` | 3 | 88,457 | 51,300 | 369,307 | 139,757 | `$0.5451` | **46,585.7** | 8 | 1 | **275.0s** |

---

### 3.3b. Stage 3B: Remediación y Repair Engineers (Ingenieros de Reparación)
- **Total de Repair Engineers Desplegados:** `6 subagentes` en **`2 ronda(s)`** (`DONE`: `6`, `BLOCKED`: **`0`**)
- **Duración Mínima:** `31.0s` | **Mediana:** `45.0s` | **Máxima:** `57.0s` (`0.9 min`)
- **Tokens Activos Totales en Reparación:** `309,552 tokens`
- **Costo Estimado Etapa 3B (Gemini 4 Hydrogen):** **`$0.7058 USD`**
- **Agente Determinante del Retraso:** `Repair Engineer C-04`

| Repair Engineer | Estado | Turnos | Tokens In | Tokens Out | Cache Leído | Total Activo | Costo (USD) | Errores | Duración |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Repair Engineer C-07** | `DONE` | 5 | 42,699 | 3,007 | 116,335 | 45,706 | `$0.0953` | 0 | **31.0s** |
| **Repair Engineer C-33** | `DONE` | 5 | 44,609 | 6,091 | 118,508 | 50,700 | `$0.1215` | 0 | **45.0s** |
| **Repair Engineer C-04** | `DONE` | 7 | 48,973 | 5,702 | 190,014 | 54,675 | `$0.1305` | 0 | **57.0s** |
| **Repair Engineer shard_17 (C-07, C-09)** | `DONE` | 6 | 56,778 | 5,789 | 187,728 | 62,567 | `$0.1427` | 0 | **56.0s** |
| **Repair Engineer C-33** | `DONE` | 5 | 44,292 | 5,595 | 115,571 | 49,887 | `$0.1171` | 0 | **44.0s** |
| **Repair Engineer Hab-24** | `DONE` | 5 | 42,415 | 3,602 | 109,191 | 46,017 | `$0.0988` | 0 | **35.0s** |

---

### 3.4. Evaluación y Arbitraje de Blind Judges (Verificación Psicométrica Ciega)

> [!NOTE]
> **Dictamen de Blind Judges:** ⚠️ NO PASÓ AL PRIMER INTENTO — APROBADO POST-REJUDGE (122/122 REACTIVOS)  
> La Ronda 1 de Blind Judges registró 5 discrepancia(s), por lo que no hubo acuerdo limpio al primer intento. Tras correcciones y Rejudge, el resultado final alcanzó 100.0% de acuerdo (0 discrepancias).

| Dimensión de Arbitraje Ciego | Valor Registrado | Observación Técnica |
| :--- | :--- | :--- |
| **Lote Estratificado Ciego** | `122 reactivos` (58 comps × 2) | Lote de evaluación sin soluciones (`judge_batch.json`) |
| **Subagentes Jueces Ciegos** | `17 jueces` | Aislamiento epistémico en Stage 5 |
| **Costo Etapa 5 (Gemini 4 Hydrogen)** | **`$1.5957 USD`** | Evaluado sobre los 17 Blind Judges (In: `427,217`, Out: `122,396`, Cache: `491,949`) |
| **Resultado al Primer Intento** | **`❌ Falló al primer intento`** | Ronda 1: 5 discrepancia(s) (`flaw_detected`: 3, `kernel_override`: 1); 0 violaciones iniciales |
| **Resultado Final Post-Rejudge** | **`✅ Aprobado`** | `100.0%` acuerdo, `0` discrepancia(s) |
| **Iteraciones de Auto-Reparación** | `0 iteraciones` en sandbox | 0 iteraciones ejecutadas |
| **Intervenciones del Supervisor** | 🛠️ `2 operaciones directas` | 2 ediciones registradas |

#### Detalle de Acciones Registradas:
- 1. **Ronda 1 (`judge_report_round_1.json` / `rounds_history`)**: 5 discrepancia(s) detectada(s).
- 2. **Bucle de Auto-Reparación / Rejudge**: 4 ola(s) de jueces ejecutada(s) (2 intervenciones de supervisor).
- 3. **Resultado Final Post-Rejudge (`judge_report.json`)**: ✅ Aprobado (`100.0% agreement rate`, `0 discrepancias` sobre 122 reactivos).

---

## 4. Auditoría Forense del Orquestador y Catálogo de Intervenciones Manuales

### 4.1. Descomposición del Tiempo y Costo del Orquestador
- 💵 **Costo Estimado del Orquestador Principal (Gemini 4 Hydrogen):** **`$1.1076 USD`** (In: `234,658`, Out: `53,330`, Cache: `4,741,854`)
- ⏱️ **Tiempo Total de Pared del Orquestador:** `23.93 min` (`1436.0s`)
- 💻 **Tiempo Activo Ejecutando Comandos CLI (`run.py`):** `1.4 min` (`84.0s`)
- 🛠️ **Tiempo Gastado en Intervenciones Manuales (Supervisor Repair):** **`0.1 min`** (`6.0s`)
- ⏳ **Tiempo Ocioso en Barreras de Sincronización (Esperando Subagentes):** `0.1 min` (`5.0s`)
- 🧠 **Tiempo de Inferencia y Razonamiento del Modelo:** `1.6 min` (`98.0s`)

### 4.2. Catálogo Cronológico de Reparaciones Manuales del Orquestador
Operaciones directas de edición de código ejecutadas por el orquestador: **`2`**

| Paso | Archivo Afectado | Tipo de Acción | Causa Raíz / Justificación Técnica | Herramienta | Tokens Paso |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **89** | `audit_engine.py` | Modificación / Script Auxiliar | Created At: 2026-11-21T19:16:37-05:00
Completed At: 2026-11-21T19:16:40-05:00
Created At:  | `edit_file` | 3,274 |
| **89** | `audit_engine.py` | Modificación / Script Auxiliar | Created At: 2026-11-21T19:16:37-05:00
Completed At: 2026-11-21T19:16:40-05:00
Created At:  | `edit_file` | 3,274 |

### 4.3. Fricciones de Orquestación, Hooks y Gobernanza Híbrida
- **Denegaciones de Pre-Tool Hooks:** `0` (Pasos: N/A)
- **Llamadas Malformadas (`Malformed function call`):** `0` (Pasos: N/A)
- **Gobernanza Híbrida (`run_workflow` + `invoke_subagent` legado):** `Sí` (`run_workflow`: 4, `invoke_subagent`: 1, `manage_subagents(kill*)`: 0)

---

## 5. Diagnóstico de Cuellos de Botella y Antipatrones Detectados

### 🛑 [HIGH] Straggler Crítico en Shards: Shard Author shard_16
- **Ámbito:** `Stage 3: Question Authoring`
- **Diagnóstico:** Shard Author shard_16 tardó 415.0s frente a la mediana de 268.0s (+147.0s de retraso en la barrera). Determinó el tiempo total de pared de la etapa de autoría.

### ⚠️ [MEDIUM] Fricción de Herramientas en 3 subagentes
- **Ámbito:** `Multiple Subagents`
- **Diagnóstico:** Subagentes como Cognitive Task Analysis Architect part_07 acumularon fallos en consola (3 errores), provocando reintentos e invalidación de caché.

---

## 6. Telemetría de Razonamiento Cognitivo (Thinking Traces)

- **Total de Turnos con Razonamiento:** `136 turnos`
- **Volumen Total de Razonamiento:** `469,923 caracteres`
- **Razonamiento del Orquestador:** `16 turnos` (5,579 chars)
- **Razonamiento de Subagentes:** `120 turnos` (464,344 chars)

| Agente / Subagente | Turnos de Thinking | Caracteres de Thinking | Trazas de Error Capturadas |
| :--- | :---: | :---: | :---: |
| **Cognitive Task Analysis Architect part_06** | 1 | 5,881 | 0 |
| **Cognitive Task Analysis Architect part_03** | 4 | 3,832 | 0 |
| **Cognitive Task Analysis Architect part_04** | 2 | 5,339 | 0 |
| **Cognitive Task Analysis Architect part_01** | 3 | 4,289 | 0 |
| **Cognitive Task Analysis Architect part_05** | 4 | 4,835 | 0 |
| **Cognitive Task Analysis Architect part_08** | 3 | 4,991 | ⚠️ 1 |
| **Cognitive Task Analysis Architect part_07** | 3 | 5,824 | ⚠️ 3 |
| **Cognitive Task Analysis Architect part_02** | 4 | 6,954 | 0 |
| **CTA Harmonizer** | 3 | 13,244 | 0 |
| **Repair Engineer C-07** | 3 | 1,613 | 0 |
| **Repair Engineer C-33** | 2 | 3,264 | 0 |
| **Blind Judge 01** | 1 | 6,203 | 0 |
| **Blind Judge 02** | 1 | 3,747 | 0 |
| **Shard Author shard_12** | 3 | 7,144 | ⚠️ 1 |
| **Shard Author shard_13** | 2 | 12,717 | ⚠️ 1 |
| **Shard Author shard_14** | 3 | 10,489 | ⚠️ 2 |
| **Shard Author shard_01** | 2 | 12,945 | ⚠️ 1 |
| **Shard Author shard_02** | 2 | 14,141 | ⚠️ 1 |
| **Shard Author shard_03** | 2 | 8,746 | ⚠️ 1 |
| **Shard Author shard_04** | 4 | 13,931 | ⚠️ 1 |
| **Shard Author shard_05** | 2 | 9,417 | ⚠️ 1 |
| **Shard Author shard_06** | 3 | 10,788 | ⚠️ 2 |
| **Shard Author shard_07** | 3 | 10,975 | ⚠️ 2 |
| **Shard Author shard_08** | 2 | 12,981 | ⚠️ 1 |
| **Shard Author shard_09** | 3 | 13,867 | ⚠️ 1 |
| **Shard Author shard_10** | 2 | 12,716 | ⚠️ 1 |
| **Shard Author shard_11** | 2 | 15,691 | ⚠️ 2 |
| **Shard Author shard_15** | 4 | 13,605 | ⚠️ 2 |
| **Shard Author shard_16** | 4 | 15,963 | ⚠️ 3 |
| **Shard Author shard_17** | 4 | 15,099 | ⚠️ 3 |
| **Shard Author shard_18** | 2 | 7,719 | ⚠️ 1 |
| **Shard Author shard_19** | 5 | 22,426 | ⚠️ 2 |
| **Shard Author shard_20** | 4 | 7,397 | ⚠️ 2 |
| **Shard Author shard_21** | 2 | 17,353 | ⚠️ 1 |
| **Shard Author shard_22** | 3 | 14,212 | ⚠️ 2 |
| **Shard Author shard_23** | 2 | 15,961 | ⚠️ 1 |
| **Blind Judge 01** | 1 | 4,405 | 0 |
| **Blind Judge 02** | 1 | 7,350 | 0 |
| **Blind Judge 03** | 1 | 8,138 | 0 |
| **Blind Judge 04** | 1 | 3,609 | 0 |
| **Blind Judge 05** | 1 | 5,322 | 0 |
| **Blind Judge 06** | 1 | 6,247 | 0 |
| **Blind Judge 07** | 1 | 5,302 | 0 |
| **Blind Judge 08** | 1 | 4,282 | 0 |
| **Blind Judge 09** | 1 | 6,100 | 0 |
| **Blind Judge 10** | 1 | 4,695 | 0 |
| **Blind Judge 01** | 1 | 1,601 | 0 |
| **Repair Engineer C-04** | 2 | 3,826 | 0 |
| **Repair Engineer shard_17 (C-07, C-09)** | 1 | 2,737 | 0 |
| **Repair Engineer C-33** | 1 | 4,406 | 0 |
| **Repair Engineer Hab-24** | 2 | 1,320 | 0 |
| **Blind Judge 01** | 1 | 6,298 | 0 |
| **Blind Judge 02** | 1 | 6,411 | 0 |
| **Blind Judge 03** | 1 | 7,848 | 0 |
| **Blind Judge 04** | 1 | 8,148 | 0 |

---
*Reporte forense determinista emitido por `c2c-run-auditor`.*