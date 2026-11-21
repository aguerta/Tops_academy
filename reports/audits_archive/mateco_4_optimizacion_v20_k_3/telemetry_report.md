# Informe de Auditoría Arquitectónica Forense: Rendimiento, Shards y Telemetría Multi-Agente
## Curso: Mateco 4 Optimizacion V20 K 3 (`mateco_4_optimizacion_v20_k_3`)

**Fecha de Auditoría:** `2026-11-21 21:47:12 UTC`  
**Conversación Orquestadora:** [`d65b2d48-4e52-480c-83a0-78d3055cc411`](conversation://d65b2d48-4e52-480c-83a0-78d3055cc411)  
**Directorio de Trabajo Validado (Zero-Collision):** `D:\Augusto\personal_portfolio\Tops_academy\courses\mateco_4_optimizacion_v20_k_3\work` (`match=True`)  
**Enfoque:** Telemetría Determinista de API, Subagentes, Shards, Latencias, Costos USD (Gemini 4 Hydrogen) y Operaciones del Orquestador.

---

## 1. Consolidación de Métricas y Caracterización de Carga

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada** | `6 archivos` (71 págs / 3.61 MB) | 01_optimizacion_dinamica.pdf, 02_Set_Problem_Calculo_de_variaciones.pdf, 03_Teoria_de_control_optimo___teoria (1).pdf, 04_opt_din_3.pdf, 05_Control Optimo Apuntes.pdf, 06_Problemas_teoria_de_control.pdf |
| **Requerimiento de Visión** | `0 páginas` (0 handouts) | Cuadrículas generadas para diagramas/fórmulas |
| **Corpus Sintetizado** | `0 caracteres` (0 palabras) | Texto consolidado tras ingesta y visión |
| **Competencias Extraídas** | **`27 competencias`** | Desglose pedagógico (Hechos, Conceptos, Habilidades) |
| **Shards Particionados** | **`21 shards`** | Unidades de trabajo concurrentes |
| **Subagentes Desplegados** | **`55 subagentes`** | Visión (0), CTA (8), Autores (21), Repairs (7), Jueces (19) |
| **Reactivos Finales Validados** | **`963 preguntas`** | Evaluadas en sandbox |
| **Tokens Entrada (Subagentes)** | **`3,073,251` tokens** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`1,158,316` tokens** | Código de plantillas y JSON generado |
| **Tokens Caché (Leídos)** | **`15,403,257` tokens** | Caché de contexto reutilizado por la API |
| **Gran Total Tokens Activos** | **`5,217,750` tokens** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`20,621,007` tokens** | Consumo total de cuota facturable |
| **Costo Estimado Total (Gemini 4 Hydrogen)** | **`$16.2156 USD`** | In: `$6.0182` (`$1.50/1M`), Out+Think: `$9.0421` (`$7.50/1M`), Cache: `$1.1552` (`$0.075/1M`) |

---

## 2. Ratios Unitarios Normalizados (Unit Economics)

Métricas normalizadas para comparación *apples-to-apples* frente a cursos de diferente volumen de contenido:

| Métrica Unitaria | Valor Obtenido | Interpretación de Eficiencia |
| :--- | :--- | :--- |
| **Tokens Totales por Pregunta** | **`21,413.3 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`5,418.2 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`763,741.0 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`99,523.4 tokens/comp`** | Costo puro de la etapa de autoría por competencia |
| **Tokens Totales por Página / Slide** | **`290,436.7 tokens/pág`** | Esfuerzo cognitivo por diapositiva original |
| **Costo Estimado por Pregunta (Hydrogen)** | **`$0.0168 USD/preg`** | Costo monetario valorizado por reactivo |
| **Costo Estimado por Competencia (Hydrogen)** | **`$0.6006 USD/comp`** | Costo monetario valorizado por competencia |
| **Segundos de Pared por Pregunta** | **`1.46 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`41.07 preg/min`** | Velocidad de producción del pipeline |
| **Factor de Aceleración Paralela** | **`5.32x`** | Relación tiempo cómputo vs tiempo de pared |

---

## 3. Desglose Forense por Etapas Críticas

### 3.0a. Valorización Monetaria por Etapa (Tarifas Gemini 4 Hydrogen)
> Tarifas oficiales aplicables: Entrada `$1.50/1M`, Caché leído `$0.075/1M`, Salida (incl. thinking) `$7.50/1M`.

| Etapa / Rol | Agentes | Tokens Entrada | Tokens Salida | Caché Leído | Costo Estimado (USD) | % del Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Stage 1A: Visión** | 0 | 0 | 0 | 0 | **`$0.0000`** | 0.0% |
| **Stage 1B: CTA Architects** | 8 | 310,974 | 80,137 | 691,324 | **`$1.1193`** | 6.9% |
| **Stage 3: Shard Authors** | 21 | 1,814,986 | 872,147 | 10,694,300 | **`$10.0657`** | 62.1% |
| **Stage 3B: Repair Engineers** | 7 | 404,071 | 35,747 | 1,001,482 | **`$0.9493`** | 5.9% |
| **Stage 5: Blind Judges** | 19 | 543,220 | 170,285 | 525,857 | **`$2.1314`** | 13.1% |
| **Orquestador Principal (Director)** | 1 | 938,879 | 47,304 | 2,490,294 | **`$1.9499`** | 12.0% |
| **TOTAL CORRIDA (Gemini 4 Hydrogen)** | **56** | **4,012,130** | **1,205,620** | **15,403,257** | **`$16.2156 USD`** | **100.0%** |

### 3.0. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json` & `state.json`)
- **Snapshots de Etapa Verificados (`conversation_id` = `d65b2d48`):** `9 etapas`
- **Estado Maestro (`work/state.json`):** `completed` (Etapa actual/final: `publish`)

| Etapa (Snapshot) | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes Capturados | Artefactos / Metadatos de Etapa |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`00_prepare`** | `2026-11-21 21:23:39` | `0.1s` | `0` (`0` act) | 0 | `—` |
| **`00b_bootstrap`** | `2026-11-21 21:23:39` | `0.2s` | `0` (`0` act) | 0 | `lock_file=D:\Augusto\personal_portfolio\Tops_academy\courses\mateco_4_optimizacion_v20_k_3\work\.c2c_subagent_lock.json` |
| **`01_cta`** | `2026-11-21 21:26:26` | `0.33s` | `0` (`0` act) | 0 | `needs_harmonize=True` |
| **`02_shard`** | `2026-11-21 21:28:07` | `0.03s` | `0` (`0` act) | 0 | `shards=21` |
| **`03_templates`** | `2026-11-21 21:46:44` | `0.3s` | `0` (`0` act) | 0 | `count=27` |
| **`04_build`** | `2026-11-21 21:47:07` | `22.92s` | `0` (`0` act) | 0 | `total_questions=963` |
| **`05_verify`** | `2026-11-21 21:47:08` | `1.52s` | `0` (`0` act) | 0 | `verified_course_path=D:\Augusto\personal_portfolio\Tops_academy\courses\mateco_4_optimizacion_v20_k_3\work\course_verified.json` |
| **`05b_judge_compare`** | `2026-11-21 21:36:12` | `0.12s` | `0` (`0` act) | 0 | `passed=False` |
| **`06_publish`** | `2026-11-21 21:47:11` | `3.29s` | `0` (`0` act) | 0 | `published_json=D:\Augusto\personal_portfolio\Tops_academy\courses\mateco_4_optimizacion_v20_k_3.json` |

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
- **Arquitectura:** `MAPREDUCE (7 Mappers + 1 Harmonizer)`
- **Tiempo de Pared Fase Mappers (Máximo):** **`80.0s`** (determinado por `Cognitive Task Analysis Architect part_05`)
- **Tiempo Fase Harmonizer (Barrera Síncrona):** **`72.0s`**
- **Tiempo de Pared Total de Etapa 1B:** **`152.0s`** (`2.5 min`)
- **Costo Estimado Etapa 1B (Gemini 4 Hydrogen):** **`$1.1193 USD`**

| Subagente CTA | Rol / Sección | Turnos | Tokens In | Tokens Out | Cache Leído | Costo (USD) | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| **Cognitive Task Analysis Architect part_01** | Mapper | 4 | 35,704 | 8,470 | 67,629 | `$0.1222` | 0 | **72.0s** |
| **Cognitive Task Analysis Architect part_05** | Mapper | 4 | 38,564 | 10,904 | 70,799 | `$0.1449` | 0 | **80.0s** |
| **Cognitive Task Analysis Architect part_02** | Mapper | 4 | 39,554 | 12,442 | 71,709 | `$0.1580` | 0 | **70.0s** |
| **Cognitive Task Analysis Architect part_04** | Mapper | 4 | 29,928 | 8,333 | 56,514 | `$0.1116` | 0 | **55.0s** |
| **Cognitive Task Analysis Architect part_06** | Mapper | 4 | 29,808 | 7,522 | 56,757 | `$0.1054` | 0 | **46.0s** |
| **Cognitive Task Analysis Architect part_03** | Mapper | 4 | 28,044 | 8,829 | 51,997 | `$0.1122` | 0 | **54.0s** |
| **Cognitive Task Analysis Architect part_07** | Mapper | 4 | 24,228 | 8,618 | 44,712 | `$0.1043` | 0 | **49.0s** |
| **CTA Harmonizer** | Harmonizer | 6 | 85,144 | 15,019 | 271,207 | `$0.2607` | 0 | **72.0s** |

---

### 3.3. Stage 3: Autoría de Reactivos por Shard y Análisis por Competencia
- **Total de Shards Auditados:** `21 shards concurrentes`
- **Tasa de Aprobación en 1ra Compilación:** **`2/21 (9.5%)`** (Reglas en 1er fallo: `[TPL-ORPHAN-VARS]` (15), `[GENERAL]` (14), `[TPL-STEM-VARIANT-PARITY]` (13), `[TPL-VAR]` (8), `[TPL-STATIC-OPT]` (8), `[TPL-DRY]` (7))
- **Duración Mínima de Shard:** `85.0s` | **Mediana:** `194.0s`
- **Tiempo de Pared Máximo (Straggler Crítico):** **`368.0s`** (`6.1 min`) por `Shard Author shard_05`
- **Retraso de Sincronización Impuesto por el Straggler:** **`+174.0s`** frente a la mediana
- **Tokens Promedio por Competencia en Autores:** **`99,523.4 tokens/competencia`**
- **Costo Estimado Etapa 3 (Gemini 4 Hydrogen):** **`$10.0657 USD`**

| Shard ID | Competencias Asignadas | Comps | Tokens In | Tokens Out | Cache Leído | Total Activo | Costo (USD) | Tokens / Comp | Turnos | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :--- | :--- | :--- |
| **Shard Author shard_15** | `C-12, C-10` | 2 | 97,904 | 52,300 | 647,042 | 150,204 | `$0.5876` | **75,102.0** | 11 | 2 | **276.0s** |
| **Shard Author shard_16** | `C-05, C-04` | 2 | 122,631 | 64,576 | 1,117,997 | 187,207 | `$0.7521` | **93,603.5** | 15 | 4 | **327.0s** |
| **Shard Author shard_17** | `C-14, C-15` | 2 | 109,619 | 56,227 | 506,517 | 165,846 | `$0.6241` | **82,923.0** | 9 | 1 | **246.0s** |
| **Shard Author shard_18** | `C-01, H-01` | 2 | 142,193 | 65,170 | 1,263,575 | 207,363 | `$0.7968` | **103,681.5** | 15 | 2 | **312.0s** |
| **Shard Author shard_19** | `C-07, C-11` | 2 | 114,489 | 59,203 | 768,863 | 173,692 | `$0.6734` | **86,846.0** | 12 | 2 | **286.0s** |
| **Shard Author shard_20** | `C-02, C-03` | 2 | 74,112 | 37,970 | 347,071 | 112,082 | `$0.4220` | **56,041.0** | 8 | 1 | **190.0s** |
| **Shard Author shard_01** | `Hab-06` | 1 | 101,837 | 44,226 | 550,351 | 146,063 | `$0.5257` | **146,063.0** | 11 | 1 | **214.0s** |
| **Shard Author shard_02** | `Hab-07` | 1 | 107,684 | 39,690 | 498,454 | 147,374 | `$0.4966` | **147,374.0** | 11 | 2 | **278.0s** |
| **Shard Author shard_03** | `Hab-09` | 1 | 57,678 | 26,915 | 148,859 | 84,593 | `$0.2995` | **84,593.0** | 5 | 0 | **127.0s** |
| **Shard Author shard_04** | `Hab-16` | 1 | 83,269 | 47,903 | 357,852 | 131,172 | `$0.5110` | **131,172.0** | 8 | 1 | **209.0s** |
| **Shard Author shard_05 🛑** | `Hab-17` | 1 | 99,869 | 50,030 | 890,012 | 149,899 | `$0.5918` | **149,899.0** | 15 | 3 | **368.0s** |
| **Shard Author shard_06** | `Hab-20` | 1 | 76,257 | 28,621 | 511,854 | 104,878 | `$0.3674` | **104,878.0** | 11 | 2 | **194.0s** |
| **Shard Author shard_07** | `Hab-01` | 1 | 66,045 | 26,542 | 404,696 | 92,587 | `$0.3285` | **92,587.0** | 10 | 2 | **172.0s** |
| **Shard Author shard_08** | `Hab-10` | 1 | 75,593 | 35,489 | 516,534 | 111,082 | `$0.4183` | **111,082.0** | 11 | 2 | **183.0s** |
| **Shard Author shard_09** | `Hab-03` | 1 | 45,862 | 16,768 | 84,760 | 62,630 | `$0.2009` | **62,630.0** | 4 | 0 | **85.0s** |
| **Shard Author shard_10** | `Hab-04` | 1 | 88,956 | 43,668 | 633,910 | 132,624 | `$0.5085` | **132,624.0** | 12 | 5 | **229.0s** |
| **Shard Author shard_11** | `Hab-05` | 1 | 65,867 | 33,134 | 255,565 | 99,001 | `$0.3665` | **99,001.0** | 7 | 1 | **158.0s** |
| **Shard Author shard_12** | `Hab-11` | 1 | 71,383 | 37,091 | 315,015 | 108,474 | `$0.4089` | **108,474.0** | 8 | 1 | **181.0s** |
| **Shard Author shard_13** | `Hab-14` | 1 | 74,559 | 37,320 | 315,103 | 111,879 | `$0.4154` | **111,879.0** | 8 | 1 | **178.0s** |
| **Shard Author shard_14** | `Hab-15` | 1 | 71,499 | 36,469 | 315,348 | 107,968 | `$0.4044` | **107,968.0** | 8 | 1 | **186.0s** |
| **Shard Author shard_21** | `C-16` | 1 | 67,680 | 32,835 | 244,922 | 100,515 | `$0.3662` | **100,515.0** | 7 | 1 | **149.0s** |

---

### 3.3b. Stage 3B: Remediación y Repair Engineers (Ingenieros de Reparación)
- **Total de Repair Engineers Desplegados:** `7 subagentes` en **`3 ronda(s)`** (`DONE`: `7`, `BLOCKED`: **`0`**)
- **Duración Mínima:** `36.0s` | **Mediana:** `41.0s` | **Máxima:** `78.0s` (`1.3 min`)
- **Tokens Activos Totales en Reparación:** `439,818 tokens`
- **Costo Estimado Etapa 3B (Gemini 4 Hydrogen):** **`$0.9493 USD`**
- **Agente Determinante del Retraso:** `Repair Engineer C-15`

| Repair Engineer | Estado | Turnos | Tokens In | Tokens Out | Cache Leído | Total Activo | Costo (USD) | Errores | Duración |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Repair Engineer C-02** | `DONE` | 6 | 50,441 | 3,963 | 169,347 | 54,404 | `$0.1181` | 0 | **39.0s** |
| **Repair Engineer C-15** | `DONE` | 7 | 59,220 | 8,863 | 231,992 | 68,083 | `$0.1727` | 1 | **78.0s** |
| **Repair Engineer Hab-06** | `DONE` | 6 | 41,686 | 4,316 | 143,568 | 46,002 | `$0.1057` | 0 | **40.0s** |
| **Repair Engineer Hab-10** | `DONE` | 5 | 70,680 | 5,250 | 73,904 | 75,930 | `$0.1509` | 0 | **41.0s** |
| **Repair Engineer Hab-20** | `DONE` | 5 | 40,258 | 4,635 | 108,231 | 44,893 | `$0.1033` | 1 | **42.0s** |
| **Repair Engineer C-02** | `DONE` | 6 | 94,636 | 5,415 | 115,317 | 100,051 | `$0.1912` | 0 | **47.0s** |
| **Repair Engineer C-02** | `DONE` | 6 | 47,150 | 3,305 | 159,123 | 50,455 | `$0.1074` | 0 | **36.0s** |

---

### 3.4. Evaluación y Arbitraje de Blind Judges (Verificación Psicométrica Ciega)

> [!NOTE]
> **Dictamen de Blind Judges:** ⚠️ NO PASÓ AL PRIMER INTENTO — APROBADO POST-REJUDGE (120/120 REACTIVOS)  
> La Ronda 1 de Blind Judges registró 5 discrepancia(s), por lo que no hubo acuerdo limpio al primer intento. Tras correcciones y Rejudge, el resultado final alcanzó 100.0% de acuerdo (0 discrepancias).

| Dimensión de Arbitraje Ciego | Valor Registrado | Observación Técnica |
| :--- | :--- | :--- |
| **Lote Estratificado Ciego** | `120 reactivos` (27 comps × 2) | Lote de evaluación sin soluciones (`judge_batch.json`) |
| **Subagentes Jueces Ciegos** | `19 jueces` | Aislamiento epistémico en Stage 5 |
| **Costo Etapa 5 (Gemini 4 Hydrogen)** | **`$2.1314 USD`** | Evaluado sobre los 19 Blind Judges (In: `543,220`, Out: `170,285`, Cache: `525,857`) |
| **Resultado al Primer Intento** | **`❌ Falló al primer intento`** | Ronda 1: 5 discrepancia(s) (`flaw_detected`: 2, `kernel_override`: 0); 0 violaciones iniciales |
| **Resultado Final Post-Rejudge** | **`✅ Aprobado`** | `100.0%` acuerdo, `0` discrepancia(s) |
| **Iteraciones de Auto-Reparación** | `0 iteraciones` en sandbox | 0 iteraciones ejecutadas |
| **Intervenciones del Supervisor** | 🛠️ `0 operaciones directas` | Ninguna (ejecución autónoma) |

#### Detalle de Acciones Registradas:
- 1. **Ronda 1 (`judge_report_round_1.json` / `rounds_history`)**: 5 discrepancia(s) detectada(s).
- 2. **Bucle de Auto-Reparación / Rejudge**: 5 ola(s) de jueces ejecutada(s) (0 intervenciones de supervisor).
- 3. **Resultado Final Post-Rejudge (`judge_report.json`)**: ✅ Aprobado (`100.0% agreement rate`, `0 discrepancias` sobre 120 reactivos).

---

## 4. Auditoría Forense del Orquestador y Catálogo de Intervenciones Manuales

### 4.1. Descomposición del Tiempo y Costo del Orquestador
- 💵 **Costo Estimado del Orquestador Principal (Gemini 4 Hydrogen):** **`$1.9499 USD`** (In: `938,879`, Out: `47,304`, Cache: `2,490,294`)
- ⏱️ **Tiempo Total de Pared del Orquestador:** `23.45 min` (`1407.0s`)
- 💻 **Tiempo Activo Ejecutando Comandos CLI (`run.py`):** `1.0 min` (`62.0s`)
- 🛠️ **Tiempo Gastado en Intervenciones Manuales (Supervisor Repair):** **`0.0 min`** (`0.0s`)
- ⏳ **Tiempo Ocioso en Barreras de Sincronización (Esperando Subagentes):** `0.1 min` (`4.0s`)
- 🧠 **Tiempo de Inferencia y Razonamiento del Modelo:** `1.1 min` (`66.0s`)

### 4.2. Catálogo Cronológico de Reparaciones Manuales del Orquestador
Operaciones directas de edición de código ejecutadas por el orquestador: **`0`**

| Paso | Archivo Afectado | Tipo de Acción | Causa Raíz / Justificación Técnica | Herramienta | Tokens Paso |
| :---: | :--- | :--- | :--- | :--- | :--- |
| — | *Ninguna intervención registrada* | — | — | — | 0 |

### 4.3. Fricciones de Orquestación, Hooks y Gobernanza Híbrida
- **Denegaciones de Pre-Tool Hooks:** `1` (Pasos: 68)
- **Llamadas Malformadas (`Malformed function call`):** `0` (Pasos: N/A)
- **Gobernanza Híbrida (`run_workflow` + `invoke_subagent` legado):** `Sí` (`run_workflow`: 6, `invoke_subagent`: 1, `manage_subagents(kill*)`: 0)

---

## 5. Diagnóstico de Cuellos de Botella y Antipatrones Detectados

### 🛑 [HIGH] Straggler Crítico en Shards: Shard Author shard_05
- **Ámbito:** `Stage 3: Question Authoring`
- **Diagnóstico:** Shard Author shard_05 tardó 368.0s frente a la mediana de 194.0s (+174.0s de retraso en la barrera). Determinó el tiempo total de pared de la etapa de autoría.

### ⚠️ [MEDIUM] Fricción de Herramientas en 3 subagentes
- **Ámbito:** `Multiple Subagents`
- **Diagnóstico:** Subagentes como Shard Author shard_16 acumularon fallos en consola (4 errores), provocando reintentos e invalidación de caché.

---

## 5b. Investigación Forense Agéntica Profunda (Contraste con Transcripts Crudos y `work/`)

### 5b.1. Tasa de 1ra Compilación en Stage 3 (Authors) y Reglas Dominantes
- **Tasa de Aprobación en 1ra Compilación (`compile_first_passed`):** **`2 / 21 shards (9.52%)`**
  - **Shards Clean-Room (1 compilación, 0 fallos, 0 ediciones post-escritura):**
    1. **`shard_09` (`Hab-03`, `eee8078f`)** — **Gold Standard Clean-Room:** `85.0s` total (`70.0s` Pre-1st-Compile, `15.0s` Post-1st-Compile), `4` turnos, `62,630` tokens activos (`$0.2009 USD`).
    2. **`shard_03` (`Hab-09`, `f0c72520`)**: `127.0s` total (`105.0s` Pre-1st-Compile, `22.0s` Post-1st-Compile), `5` turnos, `84,593` tokens activos (`$0.2995 USD`).
- **Distribución de Compilaciones en los 19 Shards con Reintento:**
  - **2 compilaciones (1 fallo):** 10 shards (`shard_01`, `shard_04`, `shard_11`, `shard_12`, `shard_13`, `shard_14`, `shard_17`, `shard_20`, `shard_21`).
  - **3 compilaciones (2-3 fallos):** 7 shards (`shard_02`, `shard_06`, `shard_07`, `shard_08`, `shard_10`, `shard_15`, `shard_18`, `shard_19`).
  - **4 compilaciones (3-4 fallos):** 2 shards (`shard_05`, `shard_16`).
- **Reglas Dominantes en el 1er Fallo de Compilación:**
  1. **`[TPL-ORPHAN-VARS]`** (`15 shards`): Claves retornadas en `vars` que no se inyectan en `@...@` ni se leen en `ver_fn`.
  2. **`[GENERAL]` / `[TPL-VERIFIER-UNSOUND]`** (`14 shards`): El verificador `ver_fn` retornó `False` en `seed=42` por buscar valores numéricos interpolados (`f'{v.get("t1")}'`) sobre strings que en pre-validación aún conservan placeholders `@t1@`, o por comparar `sympy.Rational` contra floats en `sympy.simplify(expr - target) == 0`.
  3. **`[TPL-STEM-VARIANT-PARITY]`** (`13 shards`): Asimetría de placeholders `@var@` entre `stem_variants[i]` de una misma plantilla.
  4. **`[TPL-VAR]`** (`8 shards`) y **`[TPL-STATIC-OPT]`** (`8 shards`): Cuota de diversidad no alcanzada en 50 semillas o menos de 10 respuestas correctas únicas.
  5. **`[TPL-DRY]`** (`7 shards`): Fallos de ejecución en sandbox (50 semillas) derivados de `AssertionError: cross_check verification returned False`.
  6. **Otras reglas recurrentes:** `[R-19]` (fuga de respuesta cuando un parámetro entero pequeño del stem coincide textualmente con `ans`), `[TPL-DYNAMIC-RATIONALE]` (rationales en `RATS` sin `@var@`), `[TPL-CONST-DISTRACTOR]`, `[VERIFIER-TAUTOLOGY-DETECTED]` / `[TPL-CROSS]`.
- **Impacto del Particionamiento (1 vs 2 Competencias por Shard):**
  - Los `15` shards con **1 competencia** promediaron **`187.3s`** (mediana `181.0s`).
  - Los `6` shards con **2 competencias** (`shard_15` a `shard_20`) promediaron **`272.8s`** (`shard_16`: `327.0s`, `shard_18`: `312.0s`, `shard_19`: `286.0s`, `shard_15`: `276.0s`, `shard_17`: `246.0s`, `shard_20`: `190.0s`).

### 5b.2. Análisis Forense de Stragglers en Stage 3 y Stage 3B (Repairs)
- **Straggler Crítico de Stage 3 (`Shard Author shard_05`, `Hab-17`, `70cbd63e`):**
  - **Métricas:** `368.0s` (`6.13 min`, `+174.0s` sobre la mediana de `194.0s`), `15` turnos, `2` writes, `3` edits, `4` compilaciones (`3` fallidas, `1` exitosa), `149,899` tokens activos (`$0.5918 USD`).
  - **Descomposición Bimodal:** `Pre-1st-Compile = 105.0s` | **`Post-1st-Compile = 263.0s (71.5% del tiempo)`**.
  - **Cronología Exacta en Transcript (`70cbd63e`):**
    - *Compile 1 (Paso 8):* `13` errores (`[TPL-VERIFIER-UNSOUND]` en `ver_6` de `T-Hab17-06`, `[TPL-STEM-VARIANT-PARITY]` en `T-Hab17-02`, KaTeX `\cdot@c@u`, `[TPL-DRY]`, `[TPL-VAR]`). Reescribe con `write_file(Overwrite=True)` en Paso 9 (`17,916` tokens de salida).
    - *Compile 2 (Paso 14):* `3` errores; persiste `[TPL-VERIFIER-UNSOUND]` en `ver_6`.
    - *Sondeo por Shell (Paso 15):* Ejecuta `python.exe -c "import sympy..."` para depurar `ver_6`, descubriendo que `sympy.nsimplify(sympy.sympify('5*(1 - exp(-0.5*(3 - t)))'), rational=True)` evalúa numéricamente $e^{-1.5}$ y no cancela contra `sympy.Rational('0.5')`. En Paso 17 parchea `ver_6` con evaluación numérica en 3 puntos (`tv in (0.1, 0.7, 1.3)`).
    - *Compile 3 (Paso 22):* `1` error (`[R-19: FUGA DE RESPUESTA]` en `gen_1`/`gen_2` porque `ans` tomaba valores pequeños que coincidían con parámetros del stem). En Paso 23 restringe `k >= 13` y `ans >= 12` disjunto de `(p, c, T, a0, lam)`.
    - *Compile 4 (Paso 29):* `PASS` limpio (12 plantillas, 50 semillas).
- **Segundo Straggler de Stage 3 (`Shard Author shard_16`, `C-05, C-04`, `0e732ee6`):**
  - `327.0s` (`120.0s` Pre / `207.0s` Post), `15` turnos, `4` compilaciones (`3` fallos: 44 errores en Compile 1 por `[TPL-DYNAMIC-RATIONALE]` y `ver_fn` sin soporte pre-interpolación; 6 errores en Compile 2 por `y_label` sin `$...$` en `invariant_canvas`; 6 errores en Compile 3 por `[VERIFIER-TAUTOLOGY-DETECTED]` / `[TPL-CROSS]` y `[R-15-MS]`; `PASS` en Compile 4 tras `7` llamadas a `edit_file`).
- **Stage 3B (Repair Engineers — 7 subagentes en 3 olas, 100% `DONE`, `0` `BLOCKED`):**
  - Todos los `7` ingenieros de reparación finalizaron con estado **`DONE`** (`0 BLOCKED`).
  - Seis de siete (`6/7`, `85.7%`) compilaron en **1 solo intento (`0` fallos)** entre `36.0s` y `47.0s` (mediana `41.0s`).
  - **Straggler de Stage 3B (`Repair Engineer C-15`, `ef0d1140`, Ola 1):** `78.0s` (`42.0s` Pre / `36.0s` Post), `7` turnos, `4` edits, `2` compilaciones (`1` fallo). En Paso 13 falló Compile 1 con `[TPL-CONST-DISTRACTOR]` porque al corregir la ambigüedad del coestado corriente $m(t)$ vs $\lambda(t)$ en `T-C15-08` dejó las opciones falsas `D-C15-01` y `D-C15-03` sin placeholders dinámicos `@rho1@`; en Paso 14 inyectó `$@rho1@$` con `edit_file` y aprobó Compile 2 en Paso 17.
  - **Por qué hubo 3 instancias de `Repair Engineer C-02` (`shard_20`):**
    1. **Ola 1 (`c55ae3f4`, `39.0s`, 6 turnos, `$0.1181`):** Reparó `T-C02-09` (`multiple_select`), cuyos distractores estaban redactados como condicionales contrafactuales verdaderos (*"Si se omite..., la ecuación queda..."*), haciendo que el juez seleccionara `['A','B','C','D']`. Sin embargo, **no** aplicó el barrido epistémico a `T-C02-07` ni `T-C02-08` que tenían el mismo patrón.
    2. **Ola 2 (`3a171e59`, `47.0s`, 6 turnos, `$0.1912`):** Tras el Rejudge de Ola 1, `T-C02-07` y `T-C02-08` fallaron por la misma redacción condicional contrafactual (*"Sin derivar respecto a t, resulta..."*). El ingeniero reescribió las opciones falsas en `gen_c02_ms1` y `gen_c02_ms2` como afirmaciones incondicionalmente falsas.
    3. **Ola 3 (`e02e3fbe`, `36.0s`, 6 turnos, `$0.1074`):** En el Rejudge de Ola 2 se muestreó una nueva instancia de `T-C02-06` (`adversarial_break`, `gen_c02_adv3`) donde el juez detectó un `flaw_detected` legítimo: un bug de f-string en Python (`rf'... dando -2{b} - {2*a}\ddot{{x}} = 0'`) que concatenaba el literal `-2` con `b` (ej. para $b=3$ imprimía `-23` en vez de `-6`, y para $b=7$ imprimía `-27` en vez de `-14`). El ingeniero reemplazó `-2{b}` por `-{2*b}` en la línea 281 y compiló a la primera.

### 5b.3. Denegaciones de Hooks, Mutaciones Inline vía Shell y Fricciones del Orquestador
- **Denegaciones de Pre-Tool Hooks:**
  - **Orquestador (`1` denegación en Paso 68):** En el Paso 65 lanzó `run.py --stage gates` (`task-66`, que pasó a background tras 10s). En el Paso 67, antes de que `task-66` terminara, el Orquestador intentó adelantar `run.py --stage certify`. El pre-tool hook lo bloqueó en el Paso 68: `Barrera de Consolidación: Prohibido ejecutar '... --stage cer' mientras sigan en ejecución tareas de validación/gates en segundo plano (d65b2d48.../task-66)`.
  - **Subagentes (`0` denegaciones):** Ningún subagente sufrió bloqueos de hook; todos respetaron la directiva `⚠️ USA edit_file (NO uses write_file con Overwrite=True)` cuando el conteo de errores cayó a `< 6`.
- **Mutaciones Inline vía Shell e Inspecciones `python -c`:**
  - **`0` mutaciones inline vía shell** en toda la corrida (ningún agente modificó archivos mediante `python -c`, `sed`, `awk` o PowerShell).
  - **`1` llamada de lectura/cálculo `python -c` en `Shard Author shard_05` (Paso 15):** Ejecutó `python.exe -c "import sympy; ..."` exclusivamente para inspeccionar por qué `sympy.simplify(expr - target) == 0` daba `False` en `ver_6`.
- **Intervenciones Manuales y Fricciones de Gobernanza del Orquestador:**
  - **Ediciones manuales del Director sobre archivos del curso (*Supervisor Fix*):** **`0`** (autonomía del 100% en código y JSON del curso).
  - **Fricción 1 — Gobernanza Híbrida en CTA Harmonizer (Pasos 24–29):** Mientras que los 7 CTA Mappers, 21 Autores, 7 Repairs y 19 Jueces se despacharon vía `run_workflow` (`c2c_wave_workflow.py`), el `CTA Harmonizer` (`fc334b4e`) fue despachado manualmente con `invoke_subagent` (Paso 24) y cerrado con `manage_subagents(Action="kill_all")` (Paso 28).
  - **Fricción 2 — Fallo de Infraestructura de Modelo en Ola 3 de Rejudge (Paso 57 / `task-54`):** Tras completar `Repair Engineer C-02` (`e02e3fbe`), el workflow lanzó `Blind Judge 01` (`6ddd456d`), el cual abortó al segundo `1.0s` tras su primer `read_file` con el error de plataforma: `WorkflowError: failed to run agent "6ddd456d-7e59-42db-b833-bcf2e6637535": generating and executing: unknown model key MODEL_PLACEHOLDER_M526: model not found`.
  - **Fricción 3 — Prompts de Usuario (`USER_INPUT`) y Cambio de Modelo en Caliente:**
    - En **Paso 58** (`21:44:53Z`), tras el fallo de `MODEL_PLACEHOLDER_M526`, el usuario intervino con `"continue, tell the blid judge to continue"`, tras lo cual el Director invocó `run_workflow(mode="judges")` (`task-60`) que completó exitosamente con `Blind Judge 01` (`1f235516`).
    - En **Paso 72** (`21:46:29Z`), tras finalizar `task-66` (`gates`), el usuario envió `"finish"` y cambió el selector de modelo de **Gemini 4 Hydrogen (Medium)** a **Gemini 4 Argon (Low)** para los últimos 3 turnos del Director (Pasos 73, 75, 77 y 79: ejecución de `--stage certify` y renderizado del resumen final).
  - **Anomalía de Transporte en Inicio de Stage 3 (`RESOURCE_EXHAUSTED 429`):** Al despachar los 21 autores simultáneamente a las `21:28:10Z`, varios subagentes (`shard_09`, `shard_10`, `shard_19`, etc.) registraron en `step_index: 1` un `ERROR_MESSAGE` transitorio `RESOURCE_EXHAUSTED (code 429): You have exhausted your capacity on this model. Resets in 0s.`, que el SDK reintentó automáticamente en `< 5s` sin pérdida de estado (pero que `traceback_analyzer.py` contabilizó bajo la etiqueta `Token Limit Cutoff (Model Truncation)`).

### 5b.4. Desglose Exacto de Blind Judges (Stage 5): Olas, Discrepancias, LQAS y Rejudge
- **Total de Subagentes Jueces en Telemetría:** `19` instancias de `c2c_judge` distribuidas en **4 ejecuciones de workflow** (3 rondas efectivas de arbitraje + 1 intento abortado por `MODEL_PLACEHOLDER_M526`):
  1. **Ola 1 — Ronda 1 Baseline (`task-33`, `21:35:00Z` – `21:36:12Z`, `54.0s` pared):**
     - **Jueces:** `10` jueces (`Judge 01` a `Judge 10`, `12` reactivos c/u = **`120 reactivos`** totales, `27 comps × ~4.4 ítems`).
     - **Resultado (`05b_judge_compare.json`):** `passed = False`, **`115/120` acuerdos (`95.83%`)**, **`5` competencias con discrepancias** (`0` `kernel_override`):
       | Competencia (Shard) | Ítem / Plantilla | Modalidad | Clasificación Forense | Detalle Exacto de la Discordancia en Ronda 1 |
       | :--- | :--- | :--- | :--- | :--- |
       | **`Hab-06`** (`shard_01`) | `T-Hab-06-05_judge_1` | `open_symbolic` | **`flaw_detected` (1/2)** | *La ecuación de Euler determina únicamente los cocientes $b/c = 1$ y $a/c = 31/6$, dejando indeterminado el factor de escala $c$ en la expresión simbólica de $(K, v)$.* |
       | **`Hab-10`** (`shard_08`) | `T-Hab-10-02_judge_1` | `open_symbolic` | **`flaw_detected` (2/2)** | *La expresión solicitada $H(t) + dS/dt$ es ambigua porque $S = 4x(t_1) + 16t_1$ depende tanto de $x(t_1)$ como de $t_1$.* |
       | **`C-02`** (`shard_20`) | `T-C02-09_judge_1` | `multiple_select` | **Desacuerdo de opción (1/3)** | Juez seleccionó `['A', 'B', 'C', 'D']` vs esperado `['B', 'D']` (opciones falsas redactadas como condicionales contrafactuales verdaderos). |
       | **`C-15`** (`shard_17`) | `T-C15-08_judge_1` | `multiple_select` | **Desacuerdo de opción (2/3)** | Juez seleccionó `['A', 'D', 'E']` vs esperado `['A', 'E']` (mezcla de coestado presente $\lambda(t)$ y corriente $m(t)$ en transversalidad). |
       | **`Hab-20`** (`shard_06`) | `T-Hab-20-10_judge_1` | `multiple_select` | **Desacuerdo de opción (3/3)** | Juez seleccionó `['B', 'D']` vs esperado `['A', 'C']` (stem de minimización no especificaba convención de Hamiltoniano de máximo $H = -L + \lambda\dot{x}$). |
  2. **Ola 2 — Rejudge Quirúrgico 1 (`task-39`, `21:38:55Z` – `21:39:52Z`, `57.0s` pared):**
     - **Jueces:** `6` jueces (`Judge 01 (318bdb)` a `Judge 06 (51514b)`) evaluando las 5 competencias reparadas (`C-02`, `C-15`, `Hab-06`, `Hab-10`, `Hab-20`) con réplicas duales (`judge_archive/20261121_164152`).
     - **Resultado:** **`C-15`, `Hab-06`, `Hab-10` y `Hab-20` aprobaron al 100%**. Solo **`C-02`** falló en 2 plantillas (`T-C02-08_judge_1`: ambos jueces eligieron `['A','B','C','D']` vs `['A','D']`; `T-C02-07_judge_1`: réplicas discreparon `[['C','D'], ['B','C','D']]` vs `['C','D']`).
  3. **Ola 3 — Rejudge Quirúrgico 2 (`task-45`, `21:41:53Z` – `21:42:31Z`, `38.0s` pared):**
     - **Juez:** `1` juez (`Judge 01 (05321a)`) evaluando `15` ítems de `C-02` (`judge_archive/20261121_164424`).
     - **Resultado:** `T-C02-07`, `T-C02-08` y `T-C02-09` aprobaron, pero en **`T-C02-06` (`adversarial_break`)** el juez emitió **`flaw_detected` (`BLOCKED`)** en las 2 semillas (`T-C02-06_judge_1` y `T-C02-06_judge_2`) al detectar el error aritmético `-2{b}` en `R1` (`-23` en vez de `-6`, `-27` en vez de `-14`).
  4. **Ola 4a (Abortada) y Ola 4b — Rejudge Quirúrgico 3 Final (`task-54` + `task-60`, `21:44:25Z` – `21:45:38Z`, `30.0s` pared efectivo):**
     - **Jueces:** `Judge 01 (6ddd45)` abortó en `1.0s` por `MODEL_PLACEHOLDER_M526`. Relanzado en `task-60` como **`Judge 01 (1f235516)`** (`29.0s`, `3` turnos), evaluó los `15` reactivos de `C-02` (`9` plantillas únicas).
     - **Resultado Final (`judge_report_rejudge.json` & `judge_report.json`):** **`15/15` acuerdos (`100.0%`)** en `C-02`, fusionado en **`120/120` acuerdos (`100.0% agreement_rate`)**, `0` discrepancias, `0` `kernel_override`, `lqas_followup_required = False`, cota superior de defecto al 95% ajustada = `0.0294` (`2.94%`).

### 5b.5. Síntesis Consolidada de Costos USD, Tokens, Tiempos de Pared y Speedup por Etapa

| Etapa / Cohorte | Agentes | Tiempo Cómputo (s) | Tiempo Pared (s) | Speedup Paralelo | Tokens Entrada | Tokens Salida (+Think) | Tokens Activos | Caché Leído | Costo In (USD) | Costo Out (USD) | Costo Caché (USD) | Costo Total (USD) | % Costo |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Stage 0: Bootstrap & Prepare** | CLI | 0.3s | 0.3s | 1.00x | 0 | 0 | 0 | 0 | `$0.0000` | `$0.0000` | `$0.0000` | **`$0.0000`** | 0.0% |
| **Stage 1A: Visión** | 0 | 0.0s | 0.0s | — | 0 | 0 | 0 | 0 | `$0.0000` | `$0.0000` | `$0.0000` | **`$0.0000`** | 0.0% |
| **Stage 1B: CTA (7 Mappers + 1 Harm.)** | 8 | 498.0s | 152.0s | **3.28x** | 310,974 | 80,137 *(9,496 th)* | 391,111 | 691,324 | `$0.4665` | `$0.6010` | `$0.0518` | **`$1.1193`** | 6.9% |
| **Stage 2: Sharding** | CLI | 0.03s | 0.03s | 1.00x | 0 | 0 | 0 | 0 | `$0.0000` | `$0.0000` | `$0.0000` | **`$0.0000`** | 0.0% |
| **Stage 3: Shard Authors** | 21 | 4,547.0s | 368.0s | **12.36x** | 1,814,986 | 872,147 *(64,175 th)* | 2,687,133 | 10,694,300 | `$2.7225` | `$6.5411` | `$0.8021` | **`$10.0657`** | 62.1% |
| **Stage 3B: Repair Engineers (3 olas)** | 7 | 323.0s | 161.0s* | **2.01x** | 404,071 | 35,747 *(6,203 th)* | 439,818 | 1,001,482 | `$0.6061` | `$0.2681` | `$0.0751` | **`$0.9493`** | 5.9% |
| **Stage 4: Templates & Build** | CLI | 23.22s | 23.22s | 1.00x | 0 | 0 | 0 | 0 | `$0.0000` | `$0.0000` | `$0.0000` | **`$0.0000`** | 0.0% |
| **Stage 5: Blind Judges (4 olas)** | 19 | 715.0s | 180.0s* | **3.97x** | 543,220 | 170,285 *(34,183 th)* | 713,505 | 525,857 | `$0.8148` | `$1.2771` | `$0.0394` | **`$2.1314`** | 13.1% |
| **Stage 6: Verify & Publish** | CLI | 4.81s | 4.81s | 1.00x | 0 | 0 | 0 | 0 | `$0.0000` | `$0.0000` | `$0.0000` | **`$0.0000`** | 0.0% |
| **Orquestador Principal (Director)** | 1 | 1,407.0s | 1,407.0s | 1.00x | 938,879 | 47,304 *(529 th)* | 986,183 | 2,490,294 | `$1.4083` | `$0.3548` | `$0.1868` | **`$1.9499`** | 12.0% |
| **TOTAL CORRIDA (Gemini 4 Hydrogen)** | **56** | **7,490.0s** | **1,407.0s** | **5.32x** | **4,012,130** | **1,205,620** *(114,586 th)* | **5,217,750** | **15,403,257** | **`$6.0182`** | **`$9.0421`** | **`$1.1552`** | **`$16.2156`** | **100.0%** |

> *\*Nota sobre Tiempo de Pared Acumulado en Olas Secuenciales:* En Stage 3B, el máximo individual es `78.0s` (Ola 1: `78.0s` + Ola 2: `47.0s` + Ola 3: `36.0s` = `161.0s` de pared acumulado en las 3 olas). En Stage 5, el máximo individual de una ola es `57.0s` (Ola 1: `54.0s` [10 jueces, speedup **7.52x**] + Ola 2: `57.0s` [6 jueces, speedup **4.72x**] + Ola 3: `38.0s` [1 juez] + Ola 4a/4b: `30.0s` [1+1 jueces] = `179.0s–180.0s` de pared acumulado en arbitraje).

---

## 6. Telemetría de Razonamiento Cognitivo (Thinking Traces)

- **Total de Turnos con Razonamiento:** `129 turnos`
- **Volumen Total de Razonamiento:** `458,542 caracteres`
- **Razonamiento del Orquestador:** `11 turnos` (2,133 chars)
- **Razonamiento de Subagentes:** `118 turnos` (456,409 chars)

| Agente / Subagente | Turnos de Thinking | Caracteres de Thinking | Trazas de Error Capturadas |
| :--- | :---: | :---: | :---: |
| **Cognitive Task Analysis Architect part_01** | 2 | 3,695 | 0 |
| **Cognitive Task Analysis Architect part_05** | 2 | 3,809 | 0 |
| **Cognitive Task Analysis Architect part_02** | 4 | 6,393 | 0 |
| **Cognitive Task Analysis Architect part_04** | 3 | 2,630 | 0 |
| **Cognitive Task Analysis Architect part_06** | 2 | 2,311 | 0 |
| **Cognitive Task Analysis Architect part_03** | 2 | 4,096 | 0 |
| **Cognitive Task Analysis Architect part_07** | 4 | 3,622 | 0 |
| **CTA Harmonizer** | 2 | 11,467 | 0 |
| **Blind Judge 01** | 1 | 3,552 | 0 |
| **Shard Author shard_15** | 3 | 16,897 | ⚠️ 2 |
| **Shard Author shard_16** | 4 | 18,906 | ⚠️ 4 |
| **Shard Author shard_17** | 3 | 12,170 | ⚠️ 1 |
| **Shard Author shard_18** | 3 | 12,644 | ⚠️ 2 |
| **Shard Author shard_19** | 3 | 12,921 | ⚠️ 2 |
| **Shard Author shard_20** | 3 | 10,361 | ⚠️ 1 |
| **Shard Author shard_01** | 4 | 12,572 | ⚠️ 1 |
| **Shard Author shard_02** | 3 | 12,766 | ⚠️ 2 |
| **Shard Author shard_03** | 1 | 13,610 | 0 |
| **Shard Author shard_04** | 2 | 11,746 | ⚠️ 1 |
| **Shard Author shard_05** | 5 | 17,040 | ⚠️ 3 |
| **Shard Author shard_06** | 4 | 10,468 | ⚠️ 2 |
| **Shard Author shard_07** | 4 | 11,285 | ⚠️ 2 |
| **Shard Author shard_08** | 4 | 11,779 | ⚠️ 2 |
| **Shard Author shard_09** | 1 | 6,362 | 0 |
| **Shard Author shard_10** | 4 | 15,150 | ⚠️ 5 |
| **Shard Author shard_11** | 2 | 8,545 | ⚠️ 1 |
| **Shard Author shard_12** | 2 | 12,476 | ⚠️ 1 |
| **Shard Author shard_13** | 2 | 12,556 | ⚠️ 1 |
| **Shard Author shard_14** | 2 | 11,589 | ⚠️ 1 |
| **Shard Author shard_21** | 2 | 9,946 | ⚠️ 1 |
| **Blind Judge 01** | 1 | 4,099 | 0 |
| **Blind Judge 02** | 1 | 7,066 | 0 |
| **Blind Judge 03** | 1 | 7,247 | 0 |
| **Blind Judge 04** | 1 | 7,416 | 0 |
| **Blind Judge 05** | 1 | 5,104 | 0 |
| **Blind Judge 06** | 1 | 6,276 | 0 |
| **Blind Judge 07** | 1 | 13,603 | 0 |
| **Blind Judge 08** | 1 | 10,385 | 0 |
| **Blind Judge 09** | 1 | 6,862 | 0 |
| **Blind Judge 10** | 1 | 4,827 | 0 |
| **Repair Engineer C-02** | 1 | 2,496 | 0 |
| **Repair Engineer C-15** | 4 | 6,380 | ⚠️ 1 |
| **Repair Engineer Hab-06** | 4 | 2,808 | 0 |
| **Repair Engineer Hab-10** | 1 | 3,105 | 0 |
| **Repair Engineer Hab-20** | 1 | 4,496 | 0 |
| **Blind Judge 01** | 1 | 7,489 | 0 |
| **Blind Judge 02** | 1 | 8,877 | 0 |
| **Blind Judge 03** | 1 | 13,220 | 0 |
| **Blind Judge 04** | 1 | 6,183 | 0 |
| **Blind Judge 05** | 1 | 6,400 | 0 |
| **Blind Judge 06** | 1 | 7,045 | 0 |
| **Repair Engineer C-02** | 2 | 3,494 | 0 |
| **Blind Judge 01** | 1 | 6,106 | 0 |
| **Repair Engineer C-02** | 5 | 2,061 | 0 |
| **Blind Judge 01** | 0 | 0 | 0 |

---
*Reporte forense determinista emitido por `c2c-run-auditor`.*