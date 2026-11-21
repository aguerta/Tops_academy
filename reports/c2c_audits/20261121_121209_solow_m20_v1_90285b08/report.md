# Informe de Auditoría Arquitectónica Forense: Rendimiento, Shards y Telemetría Multi-Agente
## Curso: Solow M20 V1 (`solow_m20_v1`)

**Fecha de Auditoría:** `2026-11-21 17:12:09 UTC`  
**Conversación Orquestadora:** [`90285b08-71a7-43ca-bbe7-285cd65efaab`](conversation://90285b08-71a7-43ca-bbe7-285cd65efaab)  
**Directorio de Trabajo Validado (Zero-Collision):** `D:\Augusto\personal_portfolio\Tops_academy\courses\solow_m20_v1\work` (`match=True`)  
**Enfoque:** Telemetría Determinista de API, Subagentes, Shards, Latencias y Operaciones del Orquestador.

---

## 1. Consolidación de Métricas y Caracterización de Carga

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada** | `2 archivos` (36 págs / 1.49 MB) | 05_15_07_El_modelo_de_crecimiento_de_Solow.pdf, solow1956.pdf |
| **Requerimiento de Visión** | `0 páginas` (0 handouts) | Cuadrículas generadas para diagramas/fórmulas |
| **Corpus Sintetizado** | `0 caracteres` (0 palabras) | Texto consolidado tras ingesta y visión |
| **Competencias Extraídas** | **`22 competencias`** | Desglose pedagógico (Hechos, Conceptos, Habilidades) |
| **Shards Particionados** | **`9 shards`** | Unidades de trabajo concurrentes |
| **Subagentes Desplegados** | **`39 subagentes`** | Visión (0), CTA (4), Autores (9), Repairs (15), Jueces (11) |
| **Reactivos Finales Validados** | **`540 preguntas`** | Evaluadas en sandbox |
| **Tokens Entrada (Subagentes)** | **`2,147,516` tokens** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`666,167` tokens** | Código de plantillas y JSON generado |
| **Tokens Caché (Leídos)** | **`13,380,433` tokens** | Caché de contexto reutilizado por la API |
| **Gran Total Tokens Activos** | **`3,376,491` tokens** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`16,756,924` tokens** | Consumo total de cuota facturable |

---

## 2. Ratios Unitarios Normalizados (Unit Economics)

Métricas normalizadas para comparación *apples-to-apples* frente a cursos de diferente volumen de contenido:

| Métrica Unitaria | Valor Obtenido | Interpretación de Eficiencia |
| :--- | :--- | :--- |
| **Tokens Totales por Pregunta** | **`31,031.3 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`6,252.8 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`761,678.4 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`56,152.5 tokens/comp`** | Costo puro de la etapa de autoría por competencia |
| **Tokens Totales por Página / Slide** | **`465,470.1 tokens/pág`** | Esfuerzo cognitivo por diapositiva original |
| **Segundos de Pared por Pregunta** | **`2.85 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`21.08 preg/min`** | Velocidad de producción del pipeline |
| **Factor de Aceleración Paralela** | **`3.5x`** | Relación tiempo cómputo vs tiempo de pared |

---

## 3. Desglose Forense por Etapas Críticas

### 3.0. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json` & `state.json`)
- **Snapshots de Etapa Verificados (`conversation_id` = `90285b08`):** `9 etapas`
- **Estado Maestro (`work/state.json`):** `completed` (Etapa actual/final: `publish`)

| Etapa (Snapshot) | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes Capturados | Artefactos / Metadatos de Etapa |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`00_prepare`** | `2026-11-19 20:02:06` | `0.06s` | `0` (`0` act) | 0 | `—` |
| **`00b_bootstrap`** | `2026-11-19 20:02:06` | `0.11s` | `0` (`0` act) | 0 | `lock_file=D:\Augusto\personal_portfolio\Tops_academy\courses\solow_m20_v1\work\.c2c_subagent_lock.json` |
| **`01_cta`** | `2026-11-19 20:04:55` | `0.18s` | `0` (`0` act) | 0 | `needs_harmonize=True` |
| **`02_shard`** | `2026-11-19 20:05:58` | `0.02s` | `0` (`0` act) | 0 | `shards=9` |
| **`03_templates`** | `2026-11-19 20:27:01` | `0.19s` | `1,015,081` (`223,453` act) | 3 | `count=22` |
| **`04_build`** | `2026-11-19 20:27:14` | `13.44s` | `1,015,081` (`223,453` act) | 3 | `total_questions=540` |
| **`05_verify`** | `2026-11-19 20:27:15` | `0.85s` | `1,015,081` (`223,453` act) | 3 | `verified_course_path=D:\Augusto\personal_portfolio\Tops_academy\courses\solow_m20_v1\work\course_verified.json` |
| **`05b_judge_compare`** | `2026-11-19 20:24:07` | `0.24s` | `0` (`0` act) | 0 | `passed=False` |
| **`06_publish`** | `2026-11-19 20:27:21` | `1.88s` | `0` (`0` act) | 0 | `published_json=D:\Augusto\personal_portfolio\Tops_academy\courses\solow_m20_v1.json` |

---

### 3.1. Stage 1A: Preprocesamiento de Visión
- **Subagentes de Visión Desplegados:** `0 agentes en paralelo`
- **Tiempo de Pared de la Etapa (Máximo / Critical Path):** **`0.0s`** (`0.0 min`)
- **Agente Determinante del Camino Crítico:** `N/A`

| Subagente de Visión | Turnos | Tokens In | Tokens Out | Cache Leído | Total Activo | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |

---

### 3.2. Stage 1B: Análisis Cognitivo de Competencias (CTA)
- **Arquitectura:** `MAPREDUCE (3 Mappers + 1 Harmonizer)`
- **Tiempo de Pared Fase Mappers (Máximo):** **`78.0s`** (determinado por `Cognitive Task Analysis Architect part_03`)
- **Tiempo Fase Harmonizer (Barrera Síncrona):** **`34.0s`**
- **Tiempo de Pared Total de Etapa 1B:** **`112.0s`** (`1.9 min`)

| Subagente CTA | Rol / Sección | Turnos | Tokens In | Tokens Out | Cache Leído | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Cognitive Task Analysis Architect part_02** | Mapper | 4 | 43,813 | 13,095 | 79,245 | 0 | **74.0s** |
| **Cognitive Task Analysis Architect part_03** | Mapper | 4 | 43,583 | 12,246 | 79,698 | 0 | **78.0s** |
| **Cognitive Task Analysis Architect part_01** | Mapper | 4 | 27,866 | 8,201 | 52,015 | 0 | **67.0s** |
| **CTA Harmonizer** | Harmonizer | 5 | 35,026 | 5,193 | 92,627 | 0 | **34.0s** |

---

### 3.3. Stage 3: Autoría de Reactivos por Shard y Análisis por Competencia
- **Total de Shards Auditados:** `9 shards concurrentes`
- **Tasa de Aprobación en 1ra Compilación:** **`0/9 (0.0%)`** (Reglas en 1er fallo: `[GENERAL]` (6), `[TPL-ORPHAN-VARS]` (5), `[TPL-DRY]` (5), `[TPL-VERIFIER-UNSOUND]` (5), `[TPL-STATIC-OPT]` (5), `[TPL-VAR]` (5))
- **Duración Mínima de Shard:** `154.0s` | **Mediana:** `218.0s`
- **Tiempo de Pared Máximo (Straggler Crítico):** **`319.0s`** (`5.3 min`) por `Shard Author shard_02`
- **Retraso de Sincronización Impuesto por el Straggler:** **`+101.0s`** frente a la mediana
- **Tokens Promedio por Competencia en Autores:** **`56,152.5 tokens/competencia`**

| Shard ID | Competencias Asignadas | Comps | Tokens In | Tokens Out | Cache Leído | Total Activo | Tokens / Comp | Turnos | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Shard Author shard_01** | `Hab-01, Hab-02` | 2 | 89,120 | 37,450 | 414,230 | 126,570 | **63,285.0** | 9 | 1 | **215.0s** |
| **Shard Author shard_02 🛑** | `Hab-03, Hab-04` | 2 | 99,664 | 47,406 | 680,763 | 147,070 | **73,535.0** | 12 | 2 | **319.0s** |
| **Shard Author shard_03** | `Hab-05, Hab-06` | 2 | 150,878 | 44,877 | 275,448 | 195,755 | **97,877.5** | 8 | 1 | **218.0s** |
| **Shard Author shard_04** | `Hab-07, Hab-08` | 2 | 82,120 | 42,977 | 336,722 | 125,097 | **62,548.5** | 8 | 1 | **223.0s** |
| **Shard Author shard_05** | `Hab-09, Hab-10` | 2 | 65,766 | 24,737 | 398,799 | 90,503 | **45,251.5** | 10 | 1 | **154.0s** |
| **Shard Author shard_06** | `C-01, C-02, C-03` | 3 | 113,324 | 53,965 | 471,910 | 167,289 | **55,763.0** | 9 | 2 | **245.0s** |
| **Shard Author shard_07** | `C-06, C-07, C-08` | 3 | 75,483 | 40,576 | 351,994 | 116,059 | **38,686.3** | 8 | 2 | **212.0s** |
| **Shard Author shard_08** | `C-09, C-10, C-11` | 3 | 87,124 | 54,231 | 298,539 | 141,355 | **47,118.3** | 7 | 1 | **236.0s** |
| **Shard Author shard_09** | `C-04, C-05, H-01` | 3 | 79,092 | 46,564 | 273,491 | 125,656 | **41,885.3** | 7 | 2 | **201.0s** |

---

### 3.3b. Stage 3B: Remediación y Repair Engineers (Ingenieros de Reparación)
- **Total de Repair Engineers Desplegados:** `15 subagentes` en **`7 ronda(s)`** (`DONE`: `6`, `BLOCKED`: **`9`**)
- **Duración Mínima:** `34.0s` | **Mediana:** `78.0s` | **Máxima:** `134.0s` (`2.2 min`)
- **Tokens Activos Totales en Reparación:** `1,005,553 tokens`
- **Agente Determinante del Retraso:** `Repair Engineer C-01`

| Repair Engineer | Estado | Turnos | Tokens In | Tokens Out | Cache Leído | Total Activo | Errores | Duración |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Repair Engineer shard_06 (C-01, C-02, C-03)** | `BLOCKED` | 7 | 52,110 | 9,761 | 193,584 | 61,871 | 2 | **78.0s** |
| **Repair Engineer shard_09 (C-04, C-05, H-01)** | `BLOCKED` | 8 | 122,792 | 12,168 | 213,054 | 134,960 | 2 | **92.0s** |
| **Repair Engineer shard_07 (C-06, C-07, C-08)** | `BLOCKED` | 7 | 54,969 | 10,172 | 215,229 | 65,141 | 2 | **84.0s** |
| **Repair Engineer C-01** | `BLOCKED` | 8 | 63,695 | 17,171 | 298,830 | 80,866 | 2 | **110.0s** |
| **Repair Engineer shard_09 (C-04, H-01)** | `BLOCKED` | 9 | 65,237 | 14,480 | 326,903 | 79,717 | 2 | **105.0s** |
| **Repair Engineer C-06** | `BLOCKED` | 6 | 52,148 | 10,722 | 165,895 | 62,870 | 1 | **71.0s** |
| **Repair Engineer C-01** | `BLOCKED` | 11 | 71,247 | 18,146 | 427,198 | 89,393 | 4 | **134.0s** |
| **Repair Engineer shard_09 (C-04, H-01)** | `BLOCKED` | 7 | 53,442 | 9,898 | 214,092 | 63,340 | 2 | **90.0s** |
| **Repair Engineer C-06** | `BLOCKED` | 7 | 45,278 | 7,101 | 186,961 | 52,379 | 2 | **69.0s** |
| **Repair Engineer C-01** | `DONE` | 8 | 54,773 | 4,378 | 242,971 | 59,151 | 0 | **45.0s** |
| **Repair Engineer shard_09 (C-04, H-01)** | `DONE` | 7 | 64,166 | 10,828 | 252,657 | 74,994 | 1 | **90.0s** |
| **Repair Engineer C-06** | `DONE` | 6 | 42,604 | 4,560 | 142,065 | 47,164 | 0 | **38.0s** |
| **Repair Engineer C-03** | `DONE` | 5 | 43,537 | 4,491 | 114,913 | 48,028 | 0 | **41.0s** |
| **Repair Engineer C-09** | `DONE` | 5 | 37,890 | 3,429 | 104,673 | 41,319 | 0 | **34.0s** |
| **Repair Engineer Hab-04** | `DONE` | 6 | 40,394 | 3,966 | 132,962 | 44,360 | 0 | **56.0s** |

---

### 3.4. Evaluación y Arbitraje de Blind Judges (Verificación Psicométrica Ciega)

> [!NOTE]
> **Dictamen de Blind Judges:** ⚠️ NO PASÓ AL PRIMER INTENTO — APROBADO POST-REJUDGE (120/120 REACTIVOS)  
> La Ronda 1 de Blind Judges registró 3 discrepancia(s), por lo que no hubo acuerdo limpio al primer intento. Tras correcciones y Rejudge, el resultado final alcanzó 100.0% de acuerdo (0 discrepancias).

| Dimensión de Arbitraje Ciego | Valor Registrado | Observación Técnica |
| :--- | :--- | :--- |
| **Lote Estratificado Ciego** | `120 reactivos` (22 comps × 2) | Lote de evaluación sin soluciones (`judge_batch.json`) |
| **Subagentes Jueces Ciegos** | `11 jueces` | Aislamiento epistémico en Stage 5 |
| **Resultado al Primer Intento** | **`❌ Falló al primer intento`** | Ronda 1: 3 discrepancia(s) (`flaw_detected`: 3, `kernel_override`: 5); 0 violaciones iniciales |
| **Resultado Final Post-Rejudge** | **`✅ Aprobado`** | `100.0%` acuerdo, `0` discrepancia(s) |
| **Iteraciones de Auto-Reparación** | `0 iteraciones` en sandbox | 0 iteraciones ejecutadas |
| **Intervenciones del Supervisor** | 🛠️ `2 operaciones directas` | 2 ediciones registradas |

#### Detalle de Acciones Registradas:
- 1. **Ronda 1 (`judge_report_round_1.json` / `rounds_history`)**: 3 discrepancia(s) detectada(s).
- 2. **Bucle de Auto-Reparación / Rejudge**: 1 iteración(es) ejecutada(s) (2 intervenciones de supervisor).
- 3. **Resultado Final Post-Rejudge (`judge_report.json`)**: ✅ Aprobado (`100.0% agreement rate`, `0 discrepancias` sobre 120 reactivos).

---

## 4. Auditoría Forense del Orquestador y Catálogo de Intervenciones Manuales

### 4.1. Descomposición del Tiempo Total del Orquestador
- ⏱️ **Tiempo Total de Pared del Orquestador:** `25.62 min` (`1537.0s`)
- 💻 **Tiempo Activo Ejecutando Comandos CLI (`run.py`):** `1.7 min` (`103.0s`)
- 🛠️ **Tiempo Gastado en Intervenciones Manuales (Supervisor Repair):** **`0.2 min`** (`11.0s`)
- ⏳ **Tiempo Ocioso en Barreras de Sincronización (Esperando Subagentes):** `0.2 min` (`10.0s`)
- 🧠 **Tiempo de Inferencia y Razonamiento del Modelo:** `2.1 min` (`127.0s`)

### 4.2. Catálogo Cronológico de Reparaciones Manuales del Orquestador
Operaciones directas de edición de código ejecutadas por el orquestador: **`2`**

| Paso | Archivo Afectado | Tipo de Acción | Causa Raíz / Justificación Técnica | Herramienta | Tokens Paso |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **71** | `cta.json` | Mutación Inline vía Shell (Supervisor Fix) | Mutación directa vía python -c / shell sobre cta.json ("& \".venv\\Scripts\\python.exe\" -c \"import json; p='courses/solow_m20_v1/work) | `run_command` | 3,193 |
| **85** | `pre_shard_manifest.json` | Mutación Inline vía Shell (Supervisor Fix) | Mutación directa vía python -c / shell sobre pre_shard_manifest.json ("& \".venv\\Scripts\\python.exe\" -c \"import json; p='courses/solow_m20_v1/work) | `run_command` | 3,218 |

### 4.3. Fricciones de Orquestación, Hooks y Gobernanza Híbrida
- **Denegaciones de Pre-Tool Hooks:** `2` (Pasos: 50, 63)
- **Llamadas Malformadas (`Malformed function call`):** `1` (Pasos: 64)
- **Gobernanza Híbrida (`run_workflow` + `invoke_subagent` legado):** `Sí` (`run_workflow`: 7, `invoke_subagent`: 4, `manage_subagents(kill*)`: 0)

---

## 5. Diagnóstico de Cuellos de Botella y Antipatrones Detectados

### ⚠️ [MEDIUM] Fricción de Herramientas en 1 subagentes
- **Ámbito:** `Multiple Subagents`
- **Diagnóstico:** Subagentes como Repair Engineer C-01 acumularon fallos en consola (4 errores), provocando reintentos e invalidación de caché.

---

## 6. Telemetría de Razonamiento Cognitivo (Thinking Traces)

- **Total de Turnos con Razonamiento:** `125 turnos`
- **Volumen Total de Razonamiento:** `302,867 caracteres`
- **Razonamiento del Orquestador:** `26 turnos` (9,091 chars)
- **Razonamiento de Subagentes:** `99 turnos` (293,776 chars)

| Agente / Subagente | Turnos de Thinking | Caracteres de Thinking | Trazas de Error Capturadas |
| :--- | :---: | :---: | :---: |
| **Cognitive Task Analysis Architect part_02** | 2 | 7,954 | 0 |
| **Cognitive Task Analysis Architect part_03** | 2 | 4,076 | 0 |
| **Cognitive Task Analysis Architect part_01** | 3 | 3,867 | 0 |
| **CTA Harmonizer** | 1 | 3,160 | 0 |
| **Repair Engineer shard_06 (C-01, C-02, C-03)** | 5 | 6,685 | ⚠️ 2 |
| **Repair Engineer shard_09 (C-04, C-05, H-01)** | 4 | 6,875 | ⚠️ 2 |
| **Repair Engineer shard_07 (C-06, C-07, C-08)** | 4 | 5,474 | ⚠️ 2 |
| **Repair Engineer C-01** | 5 | 8,092 | ⚠️ 2 |
| **Repair Engineer shard_09 (C-04, H-01)** | 5 | 9,171 | ⚠️ 2 |
| **Repair Engineer C-06** | 3 | 7,345 | ⚠️ 1 |
| **Repair Engineer C-01** | 6 | 5,615 | ⚠️ 4 |
| **Repair Engineer shard_09 (C-04, H-01)** | 3 | 5,681 | ⚠️ 2 |
| **Repair Engineer C-06** | 5 | 4,038 | ⚠️ 2 |
| **Repair Engineer C-01** | 3 | 1,540 | 0 |
| **Repair Engineer shard_09 (C-04, H-01)** | 3 | 5,790 | ⚠️ 1 |
| **Repair Engineer C-06** | 3 | 2,629 | 0 |
| **Blind Judge 01** | 1 | 4,785 | 0 |
| **Blind Judge 02** | 1 | 4,587 | 0 |
| **Blind Judge 03** | 2 | 7,008 | 0 |
| **Blind Judge 04** | 1 | 5,237 | 0 |
| **Blind Judge 05** | 1 | 6,788 | 0 |
| **Blind Judge 06** | 1 | 7,301 | 0 |
| **Blind Judge 07** | 2 | 10,818 | 0 |
| **Blind Judge 08** | 1 | 7,436 | 0 |
| **Blind Judge 09** | 1 | 9,613 | 0 |
| **Blind Judge 10** | 1 | 4,744 | 0 |
| **Repair Engineer C-03** | 1 | 3,881 | 0 |
| **Repair Engineer C-09** | 1 | 2,287 | 0 |
| **Repair Engineer Hab-04** | 2 | 2,852 | 0 |
| **Blind Judge 01** | 1 | 6,615 | 0 |
| **Shard Author shard_01** | 2 | 9,139 | ⚠️ 1 |
| **Shard Author shard_02** | 3 | 16,428 | ⚠️ 2 |
| **Shard Author shard_03** | 3 | 11,450 | ⚠️ 1 |
| **Shard Author shard_04** | 2 | 15,018 | ⚠️ 1 |
| **Shard Author shard_05** | 3 | 10,253 | ⚠️ 1 |
| **Shard Author shard_06** | 3 | 13,737 | ⚠️ 2 |
| **Shard Author shard_07** | 3 | 18,070 | ⚠️ 2 |
| **Shard Author shard_08** | 3 | 16,394 | ⚠️ 1 |
| **Shard Author shard_09** | 3 | 11,343 | ⚠️ 2 |

---
*Reporte forense determinista emitido por `c2c-run-auditor`.*