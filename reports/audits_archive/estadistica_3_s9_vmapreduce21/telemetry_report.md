# Informe de Auditoría Arquitectónica Forense: Rendimiento, Shards y Telemetría Multi-Agente
## Curso: Estadistica 3 S9 Vmapreduce21 (`estadistica_3_s9_vmapreduce21`)

**Fecha de Auditoría:** `2026-11-08 19:17:05 UTC`  
**Conversación Orquestadora:** [`119c07de-4eb7-4ecb-8bb9-3cd20b223e33`](conversation://119c07de-4eb7-4ecb-8bb9-3cd20b223e33)  
**Directorio de Trabajo Validado (Zero-Collision):** `D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_s9_vmapreduce21\work` (`match=True`)  
**Enfoque:** Telemetría Determinista de API, Subagentes, Shards, Latencias y Operaciones del Orquestador.

**Artefactos Forenses Complementarios:**
- 📊 Dashboard Interactivo: [`dashboard.html`](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/c2c_audits/20261108_141705_estadistica_3_s9_vmapreduce21_119c07de/dashboard.html)
- ⏱️ Descomposición Temporal Pre vs Post Compilación: [`shard_timing_decomposition.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/c2c_audits/20261108_141705_estadistica_3_s9_vmapreduce21_119c07de/shard_timing_decomposition.md) & [`shard_timing_profile.json`](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/c2c_audits/20261108_141705_estadistica_3_s9_vmapreduce21_119c07de/shard_timing_profile.json)
- 🔍 Taxonomía Forense de Tracebacks (65 errores catalogados): [`traceback_deepdive_119c07de.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/c2c_audits/20261108_141705_estadistica_3_s9_vmapreduce21_119c07de/traceback_deepdive_119c07de.md) & [`traceback_deepdive_119c07de.json`](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/c2c_audits/20261108_141705_estadistica_3_s9_vmapreduce21_119c07de/traceback_deepdive_119c07de.json)
- 📦 Telemetría Bruta y Snapshots de Estado: [`telemetry.json`](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/c2c_audits/20261108_141705_estadistica_3_s9_vmapreduce21_119c07de/telemetry.json)

---

## 1. Consolidación de Métricas y Caracterización de Carga

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada** | `2 archivos` (80 págs / 0.93 MB) | Clases_sintetizadas_semana_9.pdf, EST3_LEC07_26.2_V2.pdf |
| **Requerimiento de Visión** | `0 páginas` (0 handouts) | Cuadrículas generadas para diagramas/fórmulas |
| **Corpus Sintetizado** | `0 caracteres` (0 palabras) | Texto consolidado tras ingesta y visión |
| **Competencias Extraídas** | **`47 competencias`** | Desglose pedagógico (Hechos, Conceptos, Habilidades) |
| **Shards Particionados** | **`31 shards`** | Unidades de trabajo concurrentes |
| **Subagentes Desplegados** | **`47 subagentes`** | Visión (0), CTA (6), Autores (31), Repairs (0), Jueces (10) |
| **Reactivos Finales Validados** | **`1080 preguntas`** | Evaluadas en sandbox |
| **Tokens Entrada (Subagentes)** | **`4,392,778` tokens** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`2,154,680` tokens** | Código de plantillas y JSON generado |
| **Tokens Caché (Leídos)** | **`25,077,041` tokens** | Caché de contexto reutilizado por la API |
| **Gran Total Tokens Activos** | **`6,878,259` tokens** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`31,955,300` tokens** | Consumo total de cuota facturable |

---

## 2. Ratios Unitarios Normalizados (Unit Economics)

Métricas normalizadas para comparación *apples-to-apples* frente a cursos de diferente volumen de contenido:

| Métrica Unitaria | Valor Obtenido | Interpretación de Eficiencia |
| :--- | :--- | :--- |
| **Tokens Totales por Pregunta** | **`29,588.2 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`6,368.8 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`679,900.0 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`113,717.5 tokens/comp`** | Costo puro de la etapa de autoría por competencia |
| **Tokens Totales por Página / Slide** | **`399,441.2 tokens/pág`** | Esfuerzo cognitivo por diapositiva original |
| **Segundos de Pared por Pregunta** | **`1.37 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`43.93 preg/min`** | Velocidad de producción del pipeline |
| **Factor de Aceleración Paralela** | **`10.73x`** | Relación tiempo cómputo vs tiempo de pared |

---

## 3. Desglose Forense por Etapas Críticas

### 3.0. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json` & `state.json`)
- **Snapshots de Etapa Verificados (`conversation_id` = `119c07de`):** `9 etapas`
- **Estado Maestro (`work/state.json`):** `completed` (Etapa actual/final: `publish`)

| Etapa (Snapshot) | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes Capturados | Artefactos / Metadatos de Etapa |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`00_prepare`** | `2026-11-08 18:51:29` | `0.2s` | `0` (`0` act) | 0 | `—` |
| **`00b_bootstrap`** | `2026-11-08 18:51:29` | `0.23s` | `0` (`0` act) | 0 | `lock_file=D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_s9_vmapreduce21\work\.c2c_subagent_lock.json` |
| **`01_cta`** | `2026-11-08 18:56:21` | `0.19s` | `1,561,873` (`566,474` act) | 5 | `needs_harmonize=True` |
| **`02_shard`** | `2026-11-08 18:58:48` | `0.06s` | `0` (`0` act) | 0 | `shards=31` |
| **`03_templates`** | `2026-11-08 19:15:11` | `0.1s` | `21,216,291` (`5,344,723` act) | 31 | `count=47` |
| **`04_build`** | `2026-11-08 19:15:18` | `7.07s` | `0` (`0` act) | 0 | `total_questions=1080` |
| **`05_verify`** | `2026-11-08 19:15:21` | `2.43s` | `1,027,342` (`553,582` act) | 10 | `verified_course_path=D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_s9_vmapreduce21\work\course_verified.json` |
| **`05b_judge_compare`** | `2026-11-08 19:14:46` | `0.06s` | `1,027,342` (`553,582` act) | 10 | `passed=True` |
| **`06_publish`** | `2026-11-08 19:15:24` | `3.02s` | `0` (`0` act) | 0 | `published_json=D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_s9_vmapreduce21.json` |

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
- **Tiempo de Pared Fase Mappers (Máximo):** **`252.0s`** (determinado por `CTA Architect part_05`)
- **Tiempo Fase Harmonizer (Barrera Síncrona):** **`128.0s`**
- **Tiempo de Pared Total de Etapa 1B:** **`380.0s`** (`6.3 min`)

| Subagente CTA | Rol / Sección | Turnos | Tokens In | Tokens Out | Cache Leído | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CTA Architect part_03** | Mapper | 8 | 83,694 | 27,354 | 185,620 | 0 | **219.0s** |
| **CTA Architect part_04** | Mapper | 7 | 88,192 | 32,007 | 178,483 | 0 | **223.0s** |
| **CTA Architect part_01** | Mapper | 6 | 76,643 | 35,920 | 126,275 | 0 | **246.0s** |
| **CTA Architect part_05** | Mapper | 12 | 94,163 | 30,826 | 311,026 | 1 | **252.0s** |
| **CTA Architect part_02** | Mapper | 8 | 70,334 | 27,341 | 193,995 | 1 | **194.0s** |
| **CTA Harmonizer** | Harmonizer | 6 | 64,636 | 18,043 | 159,464 | 0 | **128.0s** |

---

### 3.3. Stage 3: Autoría de Reactivos por Shard y Análisis por Competencia
- **Total de Shards Auditados:** `31 shards concurrentes`
- **Duración Mínima de Shard:** `201.0s` | **Mediana:** `368.0s`
- **Tiempo de Pared Máximo (Straggler Crítico):** **`650.0s`** (`10.8 min`) por `Shard Author shard_27`
- **Retraso de Sincronización Impuesto por el Straggler:** **`+282.0s`** frente a la mediana
- **Tokens Promedio por Competencia en Autores:** **`113,717.5 tokens/competencia`**

| Shard ID | Competencias Asignadas | Comps | Tokens In | Tokens Out | Cache Leído | Total Activo | Tokens / Comp | Turnos | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Shard Author shard_15** | `C-03, C-04` | 2 | 131,828 | 83,775 | 423,942 | 215,603 | **107,801.5** | 8 | 1 | **548.0s** |
| **Shard Author shard_16** | `C-05, C-06` | 2 | 84,329 | 39,578 | 104,997 | 123,907 | **61,953.5** | 5 | 0 | **245.0s** |
| **Shard Author shard_17** | `C-07, C-08` | 2 | 144,904 | 89,114 | 876,543 | 234,018 | **117,009.0** | 14 | 5 | **616.0s** |
| **Shard Author shard_18** | `C-10, C-11` | 2 | 101,964 | 54,506 | 257,737 | 156,470 | **78,235.0** | 7 | 1 | **325.0s** |
| **Shard Author shard_19** | `C-13, C-14` | 2 | 131,667 | 65,689 | 962,647 | 197,356 | **98,678.0** | 15 | 2 | **459.0s** |
| **Shard Author shard_20** | `C-17, C-18` | 2 | 110,286 | 56,297 | 462,798 | 166,583 | **83,291.5** | 10 | 1 | **358.0s** |
| **Shard Author shard_21** | `C-21, C-22` | 2 | 108,938 | 55,605 | 495,024 | 164,543 | **82,271.5** | 11 | 2 | **368.0s** |
| **Shard Author shard_22** | `C-23, C-24` | 2 | 128,680 | 73,951 | 560,656 | 202,631 | **101,315.5** | 11 | 3 | **486.0s** |
| **Shard Author shard_23** | `C-01, H-01` | 2 | 136,055 | 66,901 | 1,040,953 | 202,956 | **101,478.0** | 17 | 3 | **475.0s** |
| **Shard Author shard_24** | `H-02, C-02` | 2 | 149,657 | 85,671 | 1,104,291 | 235,328 | **117,664.0** | 17 | 4 | **593.0s** |
| **Shard Author shard_25** | `H-03, C-09` | 2 | 120,401 | 59,537 | 587,532 | 179,938 | **89,969.0** | 11 | 1 | **407.0s** |
| **Shard Author shard_26** | `C-12, H-04` | 2 | 140,881 | 84,509 | 886,544 | 225,390 | **112,695.0** | 14 | 4 | **530.0s** |
| **Shard Author shard_27 🛑** | `H-05, C-15` | 2 | 156,911 | 94,370 | 1,380,424 | 251,281 | **125,640.5** | 20 | 6 | **650.0s** |
| **Shard Author shard_28** | `C-16, H-06` | 2 | 167,774 | 91,822 | 1,823,291 | 259,596 | **129,798.0** | 21 | 3 | **647.0s** |
| **Shard Author shard_29** | `C-19, H-07` | 2 | 110,427 | 60,942 | 335,827 | 171,369 | **85,684.5** | 8 | 1 | **395.0s** |
| **Shard Author shard_30** | `C-20, H-08` | 2 | 86,027 | 41,322 | 108,352 | 127,349 | **63,674.5** | 5 | 0 | **276.0s** |
| **Shard Author shard_01** | `Hab-01` | 1 | 75,718 | 32,835 | 89,311 | 108,553 | **108,553.0** | 5 | 0 | **201.0s** |
| **Shard Author shard_02** | `Hab-02` | 1 | 80,516 | 37,679 | 98,819 | 118,195 | **118,195.0** | 5 | 0 | **237.0s** |
| **Shard Author shard_03** | `Hab-03` | 1 | 141,323 | 40,847 | 198,114 | 182,170 | **182,170.0** | 8 | 1 | **258.0s** |
| **Shard Author shard_04** | `Hab-04` | 1 | 90,419 | 45,392 | 206,078 | 135,811 | **135,811.0** | 7 | 1 | **291.0s** |
| **Shard Author shard_05** | `Hab-05` | 1 | 89,091 | 41,429 | 267,200 | 130,520 | **130,520.0** | 8 | 1 | **272.0s** |
| **Shard Author shard_06** | `Hab-06` | 1 | 77,243 | 37,111 | 48,540 | 114,354 | **114,354.0** | 4 | 0 | **220.0s** |
| **Shard Author shard_07** | `Hab-07` | 1 | 167,113 | 94,329 | 1,560,665 | 261,442 | **261,442.0** | 20 | 4 | **636.0s** |
| **Shard Author shard_08** | `Hab-08` | 1 | 104,160 | 58,796 | 238,320 | 162,956 | **162,956.0** | 7 | 1 | **381.0s** |
| **Shard Author shard_09** | `Hab-09` | 1 | 93,185 | 45,440 | 282,800 | 138,625 | **138,625.0** | 8 | 1 | **293.0s** |
| **Shard Author shard_10** | `Hab-10` | 1 | 82,137 | 39,436 | 102,196 | 121,573 | **121,573.0** | 5 | 0 | **235.0s** |
| **Shard Author shard_11** | `Hab-11` | 1 | 81,596 | 39,451 | 102,089 | 121,047 | **121,047.0** | 5 | 0 | **264.0s** |
| **Shard Author shard_12** | `Hab-12` | 1 | 122,253 | 76,602 | 393,508 | 198,855 | **198,855.0** | 10 | 1 | **502.0s** |
| **Shard Author shard_13** | `Hab-13` | 1 | 104,497 | 56,654 | 454,684 | 161,151 | **161,151.0** | 10 | 1 | **376.0s** |
| **Shard Author shard_14** | `Hab-14` | 1 | 83,208 | 40,347 | 104,391 | 123,555 | **123,555.0** | 5 | 0 | **259.0s** |
| **Shard Author shard_31** | `C-25` | 1 | 99,345 | 52,253 | 313,295 | 151,598 | **151,598.0** | 8 | 1 | **343.0s** |

---

### 3.4. Evaluación y Arbitraje de Blind Judges (Verificación Psicométrica Ciega)

> [!NOTE]
> **Dictamen de Blind Judges:** ✅ 100% ACUERDO AL PRIMER INTENTO (120/120 REACTIVOS)  
> Los 10 Blind Judges evaluaron el lote estratificado de 120 reactivos en 1 turno de razonamiento puro cada uno (0 búsquedas web, 100% aislamiento epistémico), logrando un acuerdo psicométrico del 100.0% (120/120) con 0 discrepancias frente al ground truth.

| Dimensión de Arbitraje Ciego | Valor Registrado | Observación Técnica |
| :--- | :--- | :--- |
| **Lote Estratificado Ciego** | `120 reactivos` (47 comps × 2) | Lote de evaluación sin soluciones (`judge_batch.json`) |
| **Subagentes Jueces Ciegos** | `10 jueces` | Aislamiento epistémico en Stage 5 |
| **Resultado al Primer Intento** | **`✅ 100% Limpio (Sin Discrepancias)`** | Sin discrepancias ni arbitraje necesario |
| **Iteraciones de Auto-Reparación** | `0 iteraciones` en sandbox | 0 requeridas |
| **Intervenciones del Supervisor** | 🛠️ `0 operaciones directas` | Ninguna (ejecución autónoma) |

#### Detalle de Acciones Registradas:
- 1. **Arbitraje Ciego (`05b_judge_compare.json`)**: 120/120 acuerdos (`100.0% agreement rate`, `0 discrepancias`).

---

## 4. Auditoría Forense del Orquestador y Catálogo de Intervenciones Manuales

### 4.1. Descomposición del Tiempo Total del Orquestador
- ⏱️ **Tiempo Total de Pared del Orquestador:** `24.58 min` (`1475.0s`)
- 💻 **Tiempo Activo Ejecutando Comandos CLI (`run.py`):** `1.0 min` (`60.0s`)
- 🛠️ **Tiempo Gastado en Intervenciones Manuales (Supervisor Repair):** **`0.0 min`** (`0.0s`)
- ⏳ **Tiempo Ocioso en Barreras de Sincronización (Esperando Subagentes):** `0.6 min` (`38.0s`)
- 🧠 **Tiempo de Inferencia y Razonamiento del Modelo:** `0.7 min` (`41.0s`)

### 4.2. Catálogo Cronológico de Reparaciones Manuales del Orquestador
Operaciones directas de edición de código ejecutadas por el orquestador: **`0`**

| Paso | Archivo Afectado | Tipo de Acción | Causa Raíz / Justificación Técnica | Herramienta | Tokens Paso |
| :---: | :--- | :--- | :--- | :--- | :--- |
| — | *Ninguna intervención registrada* | — | — | — | 0 |

---

## 5. Diagnóstico de Cuellos de Botella y Antipatrones Detectados

### 🛑 [HIGH] Straggler Crítico en Shards: Shard Author shard_27 (650.0s vs 368.0s Mediana)
- **Ámbito:** `Stage 3: Question Authoring`
- **Diagnóstico:** Shard Author shard_27 tardó 650.0s frente a la mediana de 368.0s (+282.0s de retraso en la barrera). Determinó el tiempo total de pared de la etapa de autoría.
- **Descomposición Pre-Compilación vs Post-Compilación:**
  - **Fase Pre-1er-Compile:** `239.0s` (vs `202.0s` del Gold Standard `shard_01`, delta de apenas `+37.0s` / `+18.3%`).
  - **Fase Post-1er-Compile:** `428.0s` (vs `13.0s` del Gold Standard `shard_01`, delta masivo de `+415.0s` / `+3,192%`).
  - **Conclusión de Causa Raíz:** El **91.8%** del retraso excedente del straggler fue estrictamente **POST-compilación**, originado por un fallo de sintaxis en `shard_27_data.py` (Línea 49, Columna 52: `SyntaxError: f-string expecting a valid expression after '{'`), seguido por discordancias de validación cruzada `[TPL-CROSS]`. Esto indujo un bucle de remediación iterativa de 7 ejecuciones de compilación (6 fallidas) y 8 ediciones de código en 20 turnos.

#### Comparativa: Straggler Crítico vs Shard Gold Standard Clean-Room
| Dimensión / Métrica | Shard Gold Standard (`shard_01`) | Shard Straggler (`shard_27`) | Delta / Factor | Diagnóstico Técnico |
| :--- | :---: | :---: | :---: | :--- |
| **Tiempo de Pared Total** | **`201.0s`** (3.35 min) | **`650.0s`** (10.83 min) | **+449.0s (3.23x)** | Cuello de botella crítico de Stage 3 |
| **Tiempo Pre-1st-Compile** | `202.0s` | `239.0s` | `+37.0s (+18.3%)` | Exploración cognitiva inicial equilibrada |
| **Tiempo Post-1st-Compile** | `13.0s` | `428.0s` | **+415.0s (+3,192%)** | **91.8% del sobrecosto en remediación** |
| **Compilaciones (Fallidas)** | `1 (0 fallos)` | `7 (6 fallos)` | `+6 fallos` | Errores iterativos de sintaxis y plantilla |
| **Ediciones de Código (Edits)** | `0 ediciones` | `8 ediciones` | `+8 parches` | Modificaciones sucesivas a `shard_27_data.py` |
| **Turnos de Conversación** | `5 turnos` | `20 turnos` | `4.0x turnos` | Saturación de contexto e I/O de consola |
| **Tokens Activos (In+Out)** | `108,553 tokens` | `251,281 tokens` | `2.31x tokens` | Disipación innecesaria de cuota de API |
| **Tokens de Razonamiento (Thinking)**| `6,129 tokens` | `15,813 tokens` | `2.58x tokens` | Esfuerzo de recuperación ante tracebacks |
| **Causa Raíz Principal** | *Ninguna (Pase limpio)* | `SyntaxError f-string, [TPL-CROSS]` | Bucle de autocorrección | Fallo de templating en f-strings de Python |

---

### ⚠️ [MEDIUM] Fricción de Herramientas y Taxonomía de Errores (65 Registrados en 495 Turnos)
- **Ámbito:** `Multiple Subagents (Stage 1B CTA, Stage 3 Authors)`
- **Diagnóstico:** Se registraron 65 errores técnicos clasificados deterministamente en 7 categorías. El 100% de ellos fue resuelto autónomamente por los subagentes dentro del sandbox sin requerir ninguna intervención del supervisor humano (0 fixes directos del orquestador).

| Categoría Técnica de Error | Ocurrencias | % del Total | Severidad | Impacto y Mecanismo de Resolución |
| :--- | :---: | :---: | :---: | :--- |
| **Anti-Giveaway & Psychometric Parity Violations (R-14..R-19)** | **36** | 55.4% | `Media` | Fallos de longitud de distractores o pistas obvias; corregidos por autores tras la salida del linter. |
| **Token Limit Cutoff (Model Truncation)** | **14** | 21.5% | `Media` | Truncamiento por límites de salida; solventado mediante paginación automática de turnos. |
| **Shard Compilation & Template Validator Failure (compile_shard / check_templates)** | **8** | 12.3% | `Alta` | Excepciones de compilación de sintaxis o esquemas paramétricos; resueltos mediante parches con `edit_file`. |
| **Parameter Diversity & Option Collapse (TPL-VAR / TPL-COLLAPSE)** | **3** | 4.6% | `Media` | Espacio paramétrico insuficiente o colapso de opciones; ajustado expandiendo rangos en los shards. |
| **Missing File / Relative Path / Directory Error (FileNotFoundError)** | **2** | 3.1% | `Baja` | Rutas relativas en llamadas iniciales; corregidas a absolutas en turnos inmediatos. |
| **Cross-check Verification False (TPL-CROSS)** | **1** | 1.5% | `Alta` | Invariante matemática discordante entre enunciado y solución; armonizada en distractor logic. |
| **LaTeX Control Character / Raw-String Corruption (R-03 / SyntaxWarning)** | **1** | 1.5% | `Baja` | Caracteres de escape en expresiones LaTeX; resuelto migrando a raw-strings (`r"..."`). |
| **TOTAL** | **65** | **100.0%** | — | **Tasa de Auto-Recuperación: 100.0% (0 fallos residuales)** |

---

## 6. Telemetría de Razonamiento Cognitivo (Thinking Traces)

- **Total de Turnos con Razonamiento:** `274 turnos`
- **Volumen Total de Razonamiento:** `1,640,388 caracteres`
- **Razonamiento del Orquestador:** `16 turnos` (4,301 chars)
- **Razonamiento de Subagentes:** `258 turnos` (1,636,087 chars)

| Agente / Subagente | Turnos de Thinking | Caracteres de Thinking | Trazas de Error Capturadas |
| :--- | :---: | :---: | :---: |
| **CTA Architect part_03** | 7 | 18,348 | 0 |
| **CTA Architect part_04** | 6 | 18,693 | 0 |
| **CTA Architect part_01** | 5 | 21,652 | 0 |
| **CTA Architect part_05** | 9 | 18,608 | ⚠️ 1 |
| **CTA Architect part_02** | 7 | 17,854 | ⚠️ 1 |
| **CTA Harmonizer** | 3 | 17,717 | 0 |
| **Shard Author shard_15** | 7 | 69,219 | ⚠️ 1 |
| **Shard Author shard_16** | 4 | 26,503 | 0 |
| **Shard Author shard_17** | 9 | 66,685 | ⚠️ 5 |
| **Shard Author shard_18** | 5 | 37,433 | ⚠️ 1 |
| **Shard Author shard_19** | 7 | 49,827 | ⚠️ 2 |
| **Shard Author shard_20** | 6 | 43,324 | ⚠️ 1 |
| **Shard Author shard_21** | 6 | 40,566 | ⚠️ 2 |
| **Shard Author shard_22** | 7 | 50,429 | ⚠️ 3 |
| **Shard Author shard_23** | 9 | 46,845 | ⚠️ 3 |
| **Shard Author shard_24** | 8 | 60,396 | ⚠️ 4 |
| **Shard Author shard_25** | 6 | 48,930 | ⚠️ 1 |
| **Shard Author shard_26** | 9 | 52,856 | ⚠️ 4 |
| **Shard Author shard_27** | 10 | 63,257 | ⚠️ 6 |
| **Shard Author shard_28** | 9 | 75,991 | ⚠️ 3 |
| **Shard Author shard_29** | 5 | 48,229 | ⚠️ 1 |
| **Shard Author shard_30** | 4 | 33,932 | 0 |
| **Shard Author shard_01** | 4 | 24,522 | 0 |
| **Shard Author shard_02** | 4 | 28,137 | 0 |
| **Shard Author shard_03** | 7 | 29,888 | ⚠️ 1 |
| **Shard Author shard_04** | 6 | 34,835 | ⚠️ 1 |
| **Shard Author shard_05** | 6 | 33,528 | ⚠️ 1 |
| **Shard Author shard_06** | 4 | 29,942 | 0 |
| **Shard Author shard_07** | 15 | 68,837 | ⚠️ 4 |
| **Shard Author shard_08** | 6 | 45,561 | ⚠️ 1 |
| **Shard Author shard_09** | 6 | 38,162 | ⚠️ 1 |
| **Shard Author shard_10** | 4 | 34,235 | 0 |
| **Shard Author shard_11** | 4 | 33,943 | 0 |
| **Shard Author shard_12** | 7 | 64,197 | ⚠️ 1 |
| **Shard Author shard_13** | 8 | 46,695 | ⚠️ 1 |
| **Shard Author shard_14** | 4 | 31,580 | 0 |
| **Shard Author shard_31** | 5 | 48,390 | ⚠️ 1 |
| **Blind Judge 01** | 2 | 13,035 | 0 |
| **Blind Judge 02** | 2 | 5,234 | 0 |
| **Blind Judge 03** | 2 | 6,968 | 0 |
| **Blind Judge 04** | 2 | 8,936 | 0 |
| **Blind Judge 05** | 2 | 6,089 | 0 |
| **Blind Judge 06** | 2 | 8,499 | 0 |
| **Blind Judge 07** | 2 | 4,101 | 0 |
| **Blind Judge 08** | 2 | 30,994 | 0 |
| **Blind Judge 09** | 2 | 24,874 | 0 |
| **Blind Judge 10** | 2 | 7,611 | 0 |

---
*Reporte forense determinista emitido por `c2c-run-auditor`.*