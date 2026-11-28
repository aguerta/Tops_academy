# Informe de Auditoría Arquitectónica Forense: Rendimiento, Shards y Telemetría Multi-Agente
## Curso: Estadistica 3 Test K4 (`est3_exp_arm_a`)

**Fecha de Auditoría:** `2026-11-27 18:47:10 UTC`  
**Conversación Orquestadora:** [`08e90bb9-fbc8-4fbc-924f-9d1ae8002060`](conversation://08e90bb9-fbc8-4fbc-924f-9d1ae8002060)  
**Directorio de Trabajo Validado (Zero-Collision):** `D:\Augusto\personal_portfolio\Tops_academy\courses\est3_exp_arm_a\work` (`match=True`)  
**Enfoque:** Telemetría Determinista de API, Subagentes, Shards, Latencias, Costos USD (Gemini 4 Hydrogen) y Operaciones del Orquestador.

---

## 1. Consolidación de Métricas y Caracterización de Carga

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada** | `3 archivos` (43 págs / 1.56 MB) | 01_measure_theory_bridge.pdf, 02_stat110_lec27_conditional_expectation.pdf, 03_rincon_cl_caps1_2.pdf |
| **Requerimiento de Visión** | `0 páginas` (0 handouts) | Cuadrículas generadas para diagramas/fórmulas |
| **Corpus Sintetizado** | `0 caracteres` (0 palabras) | Texto consolidado tras ingesta y visión |
| **Competencias Extraídas** | **`23 competencias`** | Desglose pedagógico (Hechos, Conceptos, Habilidades) |
| **Shards Particionados** | **`25 shards`** | Unidades de trabajo concurrentes |
| **Subagentes Desplegados** | **`42 subagentes`** | Visión (0), CTA (0), Autores (25), Repairs (4), Jueces (12) |
| **Reactivos Finales Validados** | **`0 preguntas`** | Evaluadas en sandbox |
| **Tokens Entrada (Subagentes)** | **`2,541,507` tokens** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`998,709` tokens** | Código de plantillas y JSON generado |
| **Tokens Caché (Leídos)** | **`35,406,627` tokens** | Caché de contexto reutilizado por la API |
| **Gran Total Tokens Activos** | **`6,532,949` tokens** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`41,939,576` tokens** | Consumo total de cuota facturable |
| **Costo Estimado Total (Gemini 4 Hydrogen)** | **`$19.40 USD`** | In: `$8.06` (`$1.50/1M`), Out+Think: `$8.68` (`$7.50/1M`), Cache: `$2.66` (`$0.08/1M`) |

---

## 2. Ratios Unitarios Normalizados (Unit Economics)

Métricas normalizadas para comparación *apples-to-apples* frente a cursos de diferente volumen de contenido:

| Métrica Unitaria | Valor Obtenido | Interpretación de Eficiencia |
| :--- | :--- | :--- |
| **Tokens Totales por Pregunta** | **`0.0 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`0.0 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`1,823,459.8 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`107,799.9 tokens/comp`** | Costo puro de la etapa de autoría por competencia |
| **Tokens Totales por Página / Slide** | **`975,339.0 tokens/pág`** | Esfuerzo cognitivo por diapositiva original |
| **Costo Estimado por Pregunta (Hydrogen)** | **`$0.00 USD/preg`** | Costo monetario valorizado por reactivo |
| **Costo Estimado por Competencia (Hydrogen)** | **`$0.84 USD/comp`** | Costo monetario valorizado por competencia |
| **Segundos de Pared por Pregunta** | **`0.0 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`0.0 preg/min`** | Velocidad de producción del pipeline |
| **Factor de Aceleración Paralela** | **`2.05x`** | Relación tiempo cómputo vs tiempo de pared |

---

## 3. Desglose Forense por Etapas Críticas

### 3.0a. Valorización Monetaria por Etapa (Tarifas Gemini 4 Hydrogen)
> Tarifas oficiales aplicables: Entrada `$1.50/1M`, Caché leído `$0.08/1M`, Salida (incl. thinking) `$7.50/1M`.

| Etapa / Rol | Agentes | Tokens Entrada | Tokens Salida | Caché Leído | Costo Estimado (USD) | % del Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Stage 1A: Visión** | 0 | 0 | 0 | 0 | **`$0.00`** | 0.0% |
| **Stage 1B: CTA Architects** | 0 | 0 | 0 | 0 | **`$0.00`** | 0.0% |
| **Stage 3: Shard Authors** | 25 | 1,704,447 | 774,950 | 5,468,866 | **`$8.78`** | 45.3% |
| **Stage 3B: Repair Engineers** | 4 | 239,677 | 21,743 | 762,164 | **`$0.58`** | 3.0% |
| **Stage 5: Blind Judges** | 12 | 380,440 | 135,757 | 366,522 | **`$1.62`** | 8.4% |
| **Otros Subagentes** | 1 | 216,943 | 66,259 | 1,564,102 | **`$0.94`** | 4.8% |
| **Orquestador Principal (Director)** | 1 | 2,833,750 | 158,983 | 27,244,973 | **`$7.49`** | 38.6% |
| **TOTAL CORRIDA (Gemini 4 Hydrogen)** | **43** | **5,375,257** | **1,157,692** | **35,406,627** | **`$19.40 USD`** | **100.0%** |

### 3.0. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json` & `state.json`)
- **Snapshots de Etapa Verificados (`conversation_id` = `08e90bb9`):** `4 etapas`
- **Estado Maestro (`work/state.json`):** `completed` (Etapa actual/final: `publish`)

| Etapa (Snapshot) | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes Capturados | Artefactos / Metadatos de Etapa |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`03_templates`** | `2026-11-27 18:46:47` | `0.54s` | `1,847,304` (`283,202` act) | 1 | `count=23` |
| **`04_build`** | `2026-11-27 18:46:57` | `9.49s` | `1,847,304` (`283,202` act) | 1 | `total_questions=948` |
| **`05_verify`** | `2026-11-27 18:46:59` | `2.29s` | `1,847,304` (`283,202` act) | 1 | `verified_course_path=D:\Augusto\personal_portfolio\Tops_academy\courses\est3_exp_arm_a\work\course_verified.json` |
| **`06_publish`** | `2026-11-27 18:47:10` | `3.85s` | `0` (`0` act) | 0 | `published_json=D:\Augusto\personal_portfolio\Tops_academy\courses\est3_exp_arm_a.json` |

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
- **Arquitectura:** `DIRECT (0 Direct CTA Architect)`
- **Tiempo de Pared Fase Mappers (Máximo):** **`0.0s`** (determinado por `N/A`)
- **Tiempo Fase Harmonizer (Barrera Síncrona):** **`0.0s`**
- **Tiempo de Pared Total de Etapa 1B:** **`0.0s`** (`0.0 min`)
- **Costo Estimado Etapa 1B (Gemini 4 Hydrogen):** **`$0.00 USD`**

| Subagente CTA | Rol / Sección | Turnos | Tokens In | Tokens Out | Cache Leído | Costo (USD) | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :--- |

---

### 3.3. Stage 3: Autoría de Reactivos por Shard y Análisis por Competencia
- **Total de Shards Auditados:** `25 shards concurrentes`
- **Tasa de Aprobación en 1ra Compilación:** **`4/21 (19.05%)`** (Reglas en 1er fallo: `[TPL-STATIC-OPT]` (5), `[TPL-DYNAMIC-RATIONALE]` (4), `[R-15-MS]` (3), `[TPL-D4]` (3), `[INVARIANT]` (3), `[TPL-STEM-EQUATION-PARITY]` (2))
- **Duración Mínima de Shard:** `109.0s` | **Mediana:** `155.0s`
- **Tiempo de Pared Máximo (Straggler Crítico):** **`219.0s`** (`3.6 min`) por `Shard Author shard_16`
- **Retraso de Sincronización Impuesto por el Straggler:** **`+64.0s`** frente a la mediana
- **Tokens Promedio por Competencia en Autores:** **`68,872.1 tokens/competencia`**
- **Costo Estimado Etapa 3 (Gemini 4 Hydrogen):** **`$8.78 USD`**

| Shard ID | Competencias Asignadas | Comps | Tokens In | Tokens Out | Cache Leído | Total Activo | Costo (USD) | Tokens / Comp | Turnos | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :--- | :--- | :--- |
| **Shard Author shard_11** | `C-05, C-06` | 2 | 34,110 | 37,565 | 24,736 | 71,675 | `$0.33` | **35,837.5** | 2 | 0 | **150.0s** |
| **Shard Author shard_04** | `Hab-04` | 1 | 56,724 | 24,242 | 107,143 | 80,966 | `$0.27` | **80,966.0** | 4 | 0 | **116.0s** |
| **Shard Author shard_05** | `Hab-05` | 1 | 55,574 | 23,147 | 106,143 | 78,721 | `$0.26` | **78,721.0** | 4 | 0 | **111.0s** |
| **Shard Author shard_12** | `C-03, C-04` | 2 | 67,629 | 31,522 | 121,775 | 99,151 | `$0.35` | **49,575.5** | 4 | 1 | **156.0s** |
| **Shard Author shard_06** | `Hab-06` | 1 | 63,216 | 33,007 | 55,183 | 96,223 | `$0.35` | **96,223.0** | 3 | 0 | **143.0s** |
| **Shard Author shard_13** | `C-01, C-02` | 2 | 64,014 | 28,271 | 117,788 | 92,285 | `$0.32` | **46,142.5** | 4 | 1 | **153.0s** |
| **Shard Author shard_07** | `Hab-07` | 1 | 62,122 | 27,910 | 168,823 | 90,032 | `$0.32` | **90,032.0** | 5 | 1 | **140.0s** |
| **Shard Author shard_14** | `C-07, C-08` | 2 | 66,042 | 30,267 | 119,864 | 96,309 | `$0.34` | **48,154.5** | 4 | 1 | **156.0s** |
| **Shard Author shard_08** | `Hab-08` | 1 | 73,100 | 42,603 | 227,893 | 115,703 | `$0.45` | **115,703.0** | 6 | 1 | **189.0s** |
| **Shard Author shard_15** | `C-09, C-10` | 2 | 33,535 | 30,902 | 24,740 | 64,437 | `$0.28` | **32,218.5** | 2 | 0 | **126.0s** |
| **Shard Author shard_09** | `Hab-09` | 1 | 30,610 | 26,262 | 24,736 | 56,872 | `$0.24` | **56,872.0** | 2 | 0 | **109.0s** |
| **Shard Author shard_11** | `C-05, C-06` | 2 | 85,798 | 32,668 | 597,924 | 118,466 | `$0.42` | **59,233.0** | 11 | 1 | **196.0s** |
| **Shard Author shard_06** | `Hab-06` | 1 | 68,751 | 28,332 | 288,439 | 97,083 | `$0.34` | **97,083.0** | 7 | 1 | **153.0s** |
| **Shard Author shard_12** | `C-03, C-04` | 2 | 150,984 | 37,033 | 336,110 | 188,017 | `$0.53` | **94,008.5** | 8 | 1 | **203.0s** |
| **Shard Author shard_08** | `Hab-08` | 1 | 65,379 | 23,768 | 315,682 | 89,147 | `$0.30` | **89,147.0** | 8 | 1 | **164.0s** |
| **Shard Author shard_13** | `C-01, C-02` | 2 | 66,300 | 28,044 | 176,880 | 94,344 | `$0.32` | **47,172.0** | 5 | 0 | **155.0s** |
| **Shard Author shard_09** | `Hab-09` | 1 | 68,826 | 31,396 | 225,773 | 100,222 | `$0.36` | **100,222.0** | 6 | 1 | **176.0s** |
| **Shard Author shard_14** | `C-07, C-08` | 2 | 79,867 | 34,541 | 390,071 | 114,408 | `$0.41` | **57,204.0** | 8 | 1 | **210.0s** |
| **Shard Author shard_10** | `Hab-10` | 1 | 88,238 | 44,871 | 322,344 | 133,109 | `$0.49` | **133,109.0** | 7 | 1 | **202.0s** |
| **Shard Author shard_15** | `C-09, C-10` | 2 | 66,914 | 28,410 | 177,466 | 95,324 | `$0.33` | **47,662.0** | 5 | 0 | **141.0s** |
| **Shard Author shard_17** | `C-13` | 1 | 59,818 | 23,225 | 204,299 | 83,043 | `$0.28` | **83,043.0** | 6 | 1 | **127.0s** |
| **Shard Author shard_16 🛑** | `C-11, C-12` | 2 | 96,404 | 37,538 | 659,191 | 133,942 | `$0.48` | **66,971.0** | 11 | 2 | **219.0s** |
| **Shard Author shard_01** | `Hab-01` | 1 | 64,372 | 25,551 | 222,592 | 89,923 | `$0.30` | **89,923.0** | 6 | 1 | **147.0s** |
| **Shard Author shard_02** | `Hab-02` | 1 | 68,229 | 32,465 | 220,601 | 100,694 | `$0.36` | **100,694.0** | 6 | 1 | **168.0s** |
| **Shard Author shard_03** | `Hab-03` | 1 | 67,891 | 31,410 | 232,670 | 99,301 | `$0.35` | **99,301.0** | 6 | 1 | **168.0s** |

---

### 3.3b. Stage 3B: Remediación y Repair Engineers (Ingenieros de Reparación)
- **Total de Repair Engineers Desplegados:** `4 subagentes` en **`1 ronda(s)`** (`DONE`: `4`, `BLOCKED`: **`0`**)
- **Duración Mínima:** `46.0s` | **Mediana:** `58.0s` | **Máxima:** `68.0s` (`1.1 min`)
- **Tokens Activos Totales en Reparación:** `261,420 tokens`
- **Costo Estimado Etapa 3B (Gemini 4 Hydrogen):** **`$0.58 USD`**
- **Agente Determinante del Retraso:** `Repair Engineer Hab-01`

| Repair Engineer | Estado | Turnos | Tokens In | Tokens Out | Cache Leído | Total Activo | Costo (USD) | Errores | Duración |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Repair Engineer C-01** | `DONE` | 8 | 82,321 | 4,178 | 212,430 | 86,499 | `$0.17` | 0 | **58.0s** |
| **Repair Engineer C-07** | `DONE` | 7 | 60,568 | 5,103 | 234,956 | 65,671 | `$0.15` | 0 | **52.0s** |
| **Repair Engineer Hab-01** | `DONE` | 6 | 51,224 | 6,608 | 167,058 | 57,832 | `$0.14` | 0 | **68.0s** |
| **Repair Engineer Hab-02** | `DONE` | 6 | 45,564 | 5,854 | 147,720 | 51,418 | `$0.12` | 0 | **46.0s** |

---

### 3.4. Evaluación y Arbitraje de Blind Judges (Verificación Psicométrica Ciega)

> [!NOTE]
> **Dictamen de Blind Judges:** ⚠️ NO PASÓ AL PRIMER INTENTO — APROBADO POST-REJUDGE (143/143 REACTIVOS)  
> La Ronda 1 de Blind Judges registró 5 discrepancia(s), por lo que no hubo acuerdo limpio al primer intento. Tras correcciones y Rejudge, el resultado final alcanzó 100.0% de acuerdo (0 discrepancias).

| Dimensión de Arbitraje Ciego | Valor Registrado | Observación Técnica |
| :--- | :--- | :--- |
| **Lote Estratificado Ciego** | `143 reactivos` (23 comps × 2) | Lote de evaluación sin soluciones (`judge_batch.json`) |
| **Subagentes Jueces Ciegos** | `12 jueces` | Aislamiento epistémico en Stage 5 |
| **Costo Etapa 5 (Gemini 4 Hydrogen)** | **`$1.62 USD`** | Evaluado sobre los 12 Blind Judges (In: `380,440`, Out: `135,757`, Cache: `366,522`) |
| **Resultado al Primer Intento** | **`❌ Falló al primer intento`** | Ronda 1: 5 discrepancia(s) (`flaw_detected`: 3, `kernel_override`: 0); 0 violaciones iniciales |
| **Resultado Final Post-Rejudge** | **`✅ Aprobado`** | `100.0%` acuerdo, `0` discrepancia(s) |
| **Iteraciones de Auto-Reparación** | `0 iteraciones` en sandbox | 0 iteraciones ejecutadas |
| **Intervenciones del Supervisor** | 🛠️ `64 operaciones directas` | 64 ediciones registradas |

#### Detalle de Acciones Registradas:
- 1. **Ronda 1 (`judge_report_round_1.json` / `rounds_history`)**: 5 discrepancia(s) detectada(s).
- 2. **Bucle de Auto-Reparación / Rejudge**: 3 ola(s) de jueces ejecutada(s) (71 intervenciones de supervisor).
- 3. **Resultado Final Post-Rejudge (`judge_report.json`)**: ✅ Aprobado (`100.0% agreement rate`, `0 discrepancias` sobre 143 reactivos).

---

## 4. Auditoría Forense del Orquestador y Catálogo de Intervenciones Manuales

### 4.1. Descomposición del Tiempo y Costo del Orquestador
- 💵 **Costo Estimado del Orquestador Principal (Gemini 4 Hydrogen):** **`$7.49 USD`** (In: `2,833,750`, Out: `158,983`, Cache: `27,244,973`)
- ⏱️ **Tiempo Total de Pared del Orquestador:** `85.97 min` (`5158.0s`)
- 💻 **Tiempo Activo Ejecutando Comandos CLI (`run.py`):** `1.97 min` (`118.0s`)
- 🛠️ **Tiempo Gastado en Intervenciones Manuales (Supervisor Repair):** **`11.95 min`** (`717.0s`)
- ⏳ **Tiempo Ocioso en Barreras de Sincronización (Esperando Subagentes):** `28.65 min` (`1719.0s`)
- 🧠 **Tiempo de Inferencia y Razonamiento del Modelo:** `10.07 min` (`604.0s`)

### 4.2. Catálogo Cronológico de Reparaciones Manuales del Orquestador
Operaciones directas de edición de código ejecutadas por el orquestador: **`71`**

| Paso | Archivo Afectado | Tipo de Acción | Causa Raíz / Justificación Técnica | Herramienta | Tokens Paso |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **32** | `analyze_k3_vs_k4.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T12:22:20-05:00
Completed At: 2026-11-27T12:22:23-05:00
Created At:  | `write_file` | 9,042 |
| **47** | `analyze_k3_vs_k4_deep.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T12:23:08-05:00
Completed At: 2026-11-27T12:23:11-05:00
Created At:  | `write_file` | 73,315 |
| **55** | `analyze_k3_vs_k4_deep.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T12:24:06-05:00
Completed At: 2026-11-27T12:24:11-05:00
Created At:  | `write_file` | 10,478 |
| **66** | `analyze_k3_vs_k4_deep.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T12:25:13-05:00
Completed At: 2026-11-27T12:25:16-05:00
Created At:  | `edit_file` | 6,999 |
| **75** | `analyze_k3_vs_k4_deep.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T12:25:36-05:00
Completed At: 2026-11-27T12:25:38-05:00
Created At:  | `edit_file` | 15,243 |
| **79** | `analyze_cta_and_spans.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T12:25:52-05:00
Completed At: 2026-11-27T12:25:54-05:00
Created At:  | `write_file` | 9,747 |
| **88** | `meta_analysis_k3_vs_k4.md` | Modificación / Script Auxiliar | Created At: 2026-11-27T12:26:47-05:00
Completed At: 2026-11-27T12:26:49-05:00
Created At:  | `write_file` | 24,026 |
| **101** | `meta_analysis_k3_vs_k4.md` | Modificación / Script Auxiliar | Created At: 2026-11-27T12:26:47-05:00
Completed At: 2026-11-27T12:26:49-05:00
Created At:  | `write_file` | 23,001 |
| **150** | `cta_merge.py` | Parche de Infraestructura Core | Ajuste en cta_merge.py | `edit_file` | 6,875 |
| **150** | `cta_merge.py` | Parche de Infraestructura Core | Ajuste en cta_merge.py | `edit_file` | 6,875 |
| **150** | `cta_merge.py` | Parche de Infraestructura Core | Ajuste en cta_merge.py | `edit_file` | 6,875 |
| **150** | `cta_merge.py` | Parche de Infraestructura Core | Ajuste en cta_merge.py | `edit_file` | 6,875 |
| **150** | `cta_merge.py` | Parche de Infraestructura Core | Ajuste en cta_merge.py | `edit_file` | 6,875 |
| **150** | `cta_merge.py` | Parche de Infraestructura Core | Ajuste en cta_merge.py | `edit_file` | 6,875 |
| **150** | `dispatch.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T12:51:34-05:00
Completed At: 2026-11-27T12:51:35-05:00
Created At:  | `edit_file` | 6,875 |
| **150** | `judge.py` | Parche de Infraestructura (Stage 5) | Resolución de ruta en subdirectorio verification/ () | `edit_file` | 6,875 |
| **150** | `template_diagnostics.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T12:51:34-05:00
Completed At: 2026-11-27T12:51:35-05:00
Created At:  | `edit_file` | 6,875 |
| **150** | `template_diagnostics.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T12:51:34-05:00
Completed At: 2026-11-27T12:51:35-05:00
Created At:  | `edit_file` | 6,875 |
| **161** | `c2c_wave_workflow.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T12:51:34-05:00
Completed At: 2026-11-27T12:51:35-05:00
Created At:  | `edit_file` | 13,360 |
| **161** | `c2c_wave_workflow.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T12:51:34-05:00
Completed At: 2026-11-27T12:51:35-05:00
Created At:  | `edit_file` | 13,360 |
| **161** | `c2c_wave_workflow.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T12:51:34-05:00
Completed At: 2026-11-27T12:51:35-05:00
Created At:  | `edit_file` | 13,360 |
| **161** | `c2c_wave_workflow.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T12:51:34-05:00
Completed At: 2026-11-27T12:51:35-05:00
Created At:  | `edit_file` | 13,360 |
| **161** | `c2c_wave_workflow.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T12:51:34-05:00
Completed At: 2026-11-27T12:51:35-05:00
Created At:  | `edit_file` | 13,360 |
| **161** | `c2c_wave_workflow.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T12:51:34-05:00
Completed At: 2026-11-27T12:51:35-05:00
Created At:  | `edit_file` | 13,360 |
| **161** | `test_c2c_first_pass_and_zero_repair.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T12:51:34-05:00
Completed At: 2026-11-27T12:51:35-05:00
Created At:  | `edit_file` | 13,360 |
| **161** | `test_cta_merge_hardening.py` | Parche de Infraestructura Core | Ajuste en test_cta_merge_hardening.py | `edit_file` | 13,360 |
| **161** | `test_judge_hardening.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T12:51:34-05:00
Completed At: 2026-11-27T12:51:35-05:00
Created At:  | `edit_file` | 13,360 |
| **161** | `test_c2c_hardening_workflow.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T12:51:34-05:00
Completed At: 2026-11-27T12:51:35-05:00
Created At:  | `edit_file` | 13,360 |
| **161** | `test_c2c_validator_prescriptive.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T12:51:34-05:00
Completed At: 2026-11-27T12:51:35-05:00
Created At:  | `edit_file` | 13,360 |
| **175** | `test_c2c_validator_prescriptive.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T12:53:24-05:00
Completed At: 2026-11-27T12:53:46-05:00
Encountered  | `edit_file` | 9,766 |
| **181** | `test_c2c_validator_prescriptive.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T12:53:24-05:00
Completed At: 2026-11-27T12:53:46-05:00
Encountered  | `edit_file` | 439,894 |
| **187** | `c2c_wave_workflow.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T12:54:42-05:00
Completed At: 2026-11-27T12:54:43-05:00
Created At:  | `edit_file` | 4,378 |
| **192** | `test_c2c_validator_prescriptive.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T12:54:42-05:00
Completed At: 2026-11-27T12:54:43-05:00
Created At:  | `edit_file` | 3,873 |
| **229** | `template_healing.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T13:06:24-05:00
Completed At: 2026-11-27T13:06:25-05:00
Created At:  | `edit_file` | 9,392 |
| **229** | `assemble.py` | Parche de Infraestructura Core | Ajuste en assemble.py | `edit_file` | 9,392 |
| **229** | `check_templates.py` | Parche de Plantilla |  | `edit_file` | 9,392 |
| **229** | `check_templates.py` | Parche de Plantilla |  | `edit_file` | 9,392 |
| **229** | `c2c_wave_workflow.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T13:06:24-05:00
Completed At: 2026-11-27T13:06:25-05:00
Created At:  | `edit_file` | 9,392 |
| **229** | `c2c_wave_workflow.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T13:06:24-05:00
Completed At: 2026-11-27T13:06:25-05:00
Created At:  | `edit_file` | 9,392 |
| **229** | `budget_guard.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T13:06:24-05:00
Completed At: 2026-11-27T13:06:25-05:00
Created At:  | `edit_file` | 9,392 |
| **229** | `dispatch.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T13:06:24-05:00
Completed At: 2026-11-27T13:06:25-05:00
Created At:  | `edit_file` | 9,392 |
| **229** | `experiment_p1_4_k4_hab_structure.md` | Modificación / Script Auxiliar | Created At: 2026-11-27T13:06:24-05:00
Completed At: 2026-11-27T13:06:25-05:00
Created At:  | `write_file` | 9,392 |
| **239** | `test_c2c_validator_prescriptive.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T13:06:24-05:00
Completed At: 2026-11-27T13:06:25-05:00
Created At:  | `edit_file` | 9,685 |
| **239** | `test_c2c_hardening_workflow.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T13:06:24-05:00
Completed At: 2026-11-27T13:06:25-05:00
Created At:  | `edit_file` | 9,685 |
| **248** | `test_c2c_hardening_workflow.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T13:06:24-05:00
Completed At: 2026-11-27T13:06:25-05:00
Created At:  | `edit_file` | 34,510 |
| **252** | `test_c2c_validator_prescriptive.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T13:09:18-05:00
Completed At: 2026-11-27T13:09:19-05:00
Created At:  | `edit_file` | 2,795 |
| **257** | `check_templates.py` | Parche de Plantilla |  | `edit_file` | 4,181 |
| **315** | `plan_shards.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T13:19:07-05:00
Completed At: 2026-11-27T13:19:08-05:00
Created At:  | `edit_file` | 8,848 |
| **315** | `plan_shards.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T13:19:07-05:00
Completed At: 2026-11-27T13:19:08-05:00
Created At:  | `edit_file` | 8,848 |
| **315** | `plan_shards.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T13:19:07-05:00
Completed At: 2026-11-27T13:19:08-05:00
Created At:  | `edit_file` | 8,848 |
| **315** | `plan_shards.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T13:19:07-05:00
Completed At: 2026-11-27T13:19:08-05:00
Created At:  | `edit_file` | 8,848 |
| **315** | `plan_shards.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T13:19:07-05:00
Completed At: 2026-11-27T13:19:08-05:00
Created At:  | `edit_file` | 8,848 |
| **322** | `compile_shard.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T13:19:07-05:00
Completed At: 2026-11-27T13:19:08-05:00
Created At:  | `edit_file` | 10,179 |
| **322** | `compile_shard.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T13:19:07-05:00
Completed At: 2026-11-27T13:19:08-05:00
Created At:  | `edit_file` | 10,179 |
| **322** | `run.py` | Parche de Infraestructura Core | Ajuste en run.py | `edit_file` | 10,179 |
| **322** | `run.py` | Parche de Infraestructura Core | Ajuste en run.py | `edit_file` | 10,179 |
| **322** | `run.py` | Parche de Infraestructura Core | Ajuste en run.py | `edit_file` | 10,179 |
| **322** | `run.py` | Parche de Infraestructura Core | Ajuste en run.py | `edit_file` | 10,179 |
| **332** | `dispatch.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T13:19:07-05:00
Completed At: 2026-11-27T13:19:08-05:00
Created At:  | `edit_file` | 3,766 |
| **332** | `dispatch.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T13:19:07-05:00
Completed At: 2026-11-27T13:19:08-05:00
Created At:  | `edit_file` | 3,766 |
| **337** | `run.py` | Parche de Infraestructura Core | Ajuste en run.py | `edit_file` | 5,407 |
| **337** | `dispatch.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T13:20:39-05:00
Completed At: 2026-11-27T13:20:44-05:00
Created At:  | `edit_file` | 5,407 |
| **341** | `test_p1_4_shard_arms.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T13:20:39-05:00
Completed At: 2026-11-27T13:20:44-05:00
Created At:  | `write_file` | 3,838 |
| **346** | `test_p1_4_shard_arms.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T13:20:39-05:00
Completed At: 2026-11-27T13:20:44-05:00
Created At:  | `edit_file` | 4,508 |
| **356** | `test_p1_4_shard_arms.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T13:21:59-05:00
Completed At: 2026-11-27T13:22:01-05:00
Created At:  | `edit_file` | 3,826 |
| **361** | `test_p1_4_shard_arms.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T13:21:59-05:00
Completed At: 2026-11-27T13:22:01-05:00
Created At:  | `edit_file` | 3,726 |
| **366** | `test_p1_4_shard_arms.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T13:21:59-05:00
Completed At: 2026-11-27T13:22:01-05:00
Created At:  | `edit_file` | 4,595 |
| **375** | `nsrc` | Mutación Inline vía Shell (Supervisor Fix) | Mutación directa vía python -c / shell sobre nsrc ("python -c \"\nimport json, shutil, pathlib, sys\nsys.path.insert(0, '.agents/sk) | `run_command` | 4,161 |
| **377** | `nsrc` | Mutación Inline vía Shell (Supervisor Fix) | Mutación directa vía python -c / shell sobre nsrc ("python -c \"\nimport json, shutil, pathlib, sys\nsys.path.insert(0, '.agents/sk) | `run_command` | 3,711 |
| **390** | `c2c_wave_workflow.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T13:23:35-05:00
Completed At: 2026-11-27T13:23:37-05:00
Created At:  | `edit_file` | 3,630 |
| **395** | `c2c_wave_workflow.py` | Modificación / Script Auxiliar | Created At: 2026-11-27T13:23:35-05:00
Completed At: 2026-11-27T13:23:37-05:00
Created At:  | `edit_file` | 4,821 |

### 4.3. Fricciones de Orquestación, Hooks y Gobernanza Híbrida
- **Denegaciones de Pre-Tool Hooks:** `0` (Pasos: N/A)
- **Llamadas Malformadas (`Malformed function call`):** `1` (Pasos: 11)
- **Gobernanza Híbrida (`run_workflow` + `invoke_subagent` legado):** `Sí` (`run_workflow`: 5, `invoke_subagent`: 1, `manage_subagents(kill*)`: 0)

---

## 5. Diagnóstico de Cuellos de Botella y Antipatrones Detectados

### 🛑 [HIGH] Síndrome del Orquestador Reparador (71 intervenciones manuales)
- **Ámbito:** `Director (Orchestrator)`
- **Diagnóstico:** El orquestador principal ejecutó 71 operaciones directas de edición de código y plantillas. Consumió más de 1,151,332 tokens en turnos de mantenimiento/recuperación manual.

### ⚠️ [MEDIUM] Fricción de Herramientas en 1 subagentes
- **Ámbito:** `Multiple Subagents`
- **Diagnóstico:** Subagentes como Skeptical Meta-Analysis Auditor acumularon fallos en consola (8 errores), provocando reintentos e invalidación de caché.

---

## 6. Telemetría de Razonamiento Cognitivo (Thinking Traces)

- **Total de Turnos con Razonamiento:** `129 turnos`
- **Volumen Total de Razonamiento:** `226,945 caracteres`
- **Razonamiento del Orquestador:** `53 turnos` (28,473 chars)
- **Razonamiento de Subagentes:** `76 turnos` (198,472 chars)

| Agente / Subagente | Turnos de Thinking | Caracteres de Thinking | Trazas de Error Capturadas |
| :--- | :---: | :---: | :---: |
| **Skeptical Meta-Analysis Auditor** | 15 | 15,149 | ⚠️ 8 |
| **Blind Judge 01** | 1 | 2,184 | 0 |
| **Shard Author shard_11** | 1 | 4,428 | 0 |
| **Shard Author shard_04** | 1 | 5,041 | 0 |
| **Shard Author shard_05** | 1 | 4,472 | 0 |
| **Shard Author shard_12** | 1 | 2,234 | ⚠️ 1 |
| **Shard Author shard_06** | 1 | 8,623 | 0 |
| **Shard Author shard_13** | 1 | 2,628 | ⚠️ 1 |
| **Shard Author shard_07** | 2 | 5,264 | ⚠️ 1 |
| **Shard Author shard_14** | 1 | 2,759 | ⚠️ 1 |
| **Shard Author shard_08** | 2 | 6,299 | ⚠️ 1 |
| **Shard Author shard_15** | 1 | 2,442 | 0 |
| **Shard Author shard_09** | 1 | 5,568 | 0 |
| **Shard Author shard_11** | 3 | 2,650 | ⚠️ 1 |
| **Shard Author shard_06** | 2 | 5,591 | ⚠️ 1 |
| **Shard Author shard_12** | 2 | 4,382 | ⚠️ 1 |
| **Shard Author shard_08** | 2 | 4,110 | ⚠️ 1 |
| **Shard Author shard_13** | 1 | 2,073 | 0 |
| **Shard Author shard_09** | 3 | 5,682 | ⚠️ 1 |
| **Shard Author shard_14** | 2 | 3,185 | ⚠️ 1 |
| **Shard Author shard_10** | 3 | 5,986 | ⚠️ 1 |
| **Shard Author shard_15** | 1 | 2,425 | 0 |
| **Shard Author shard_17** | 2 | 2,981 | ⚠️ 1 |
| **Shard Author shard_16** | 2 | 3,115 | ⚠️ 2 |
| **Shard Author shard_01** | 1 | 4,862 | ⚠️ 1 |
| **Shard Author shard_02** | 2 | 3,727 | ⚠️ 1 |
| **Shard Author shard_03** | 2 | 6,366 | ⚠️ 1 |
| **Blind Judge 01** | 1 | 6,096 | 0 |
| **Blind Judge 02** | 1 | 6,394 | 0 |
| **Blind Judge 03** | 1 | 7,363 | 0 |
| **Blind Judge 04** | 1 | 5,838 | 0 |
| **Blind Judge 05** | 1 | 4,938 | 0 |
| **Blind Judge 06** | 1 | 7,037 | 0 |
| **Blind Judge 07** | 1 | 5,217 | 0 |
| **Blind Judge 08** | 1 | 7,482 | 0 |
| **Blind Judge 09** | 1 | 7,245 | 0 |
| **Repair Engineer C-01** | 2 | 2,048 | 0 |
| **Repair Engineer C-07** | 3 | 2,575 | 0 |
| **Repair Engineer Hab-01** | 2 | 1,860 | 0 |
| **Repair Engineer Hab-02** | 1 | 2,487 | 0 |
| **Blind Judge 01** | 1 | 4,037 | 0 |
| **Blind Judge 02** | 1 | 3,629 | 0 |

---
*Reporte forense determinista emitido por `c2c-run-auditor`.*