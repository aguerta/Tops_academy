# Auditoría Forense Ultra-Detallada del Traceback de Ejecución
## Pipeline Content-to-Course (C2C) — Conversación [`bb98a610-c34f-44af-93c6-323d3cc202e7`](conversation://bb98a610-c34f-44af-93c6-323d3cc202e7)

**Fecha de Auditoría:** `2026-10-24 19:55:28 UTC`  
**Conversación Orquestadora:** [`bb98a610-c34f-44af-93c6-323d3cc202e7`](conversation://bb98a610-c34f-44af-93c6-323d3cc202e7)  
**Directorio de Telemetría Validado (Zero-Collision):** `D:\Augusto\personal_portfolio\Tops_academy\courses\asyntotic_estatistics_v3\work` (`9` snapshots C2C v3.2)  
**Motor Forense:** C2C Traceback Deep-Dive Analyzer (Antigravity SDK)  

---

## 1. Resumen Ejecutivo y Metrología Forense Global

| Métrica Forense | Valor Registrado | Observación Técnica |
| :--- | :--- | :--- |
| **Tiempo de Pared Total** | **`66.62 min`** (3997.0 s) | Tiempo transcurrido de extremo a extremo |
| **Total de Turnos Analizados** | **`825 turnos`** | Suma de orquestador y subagentes |
| **Total de Errores Catalogados** | **`85 errores`** | Clasificados en 9 categorías técnicas (0% caja negra) |
| **Inferencia LLM Promedio** | **`95.8%`** | Porcentaje de tiempo dedicado a generación/thinking |
| **Ejecución Local de Tools** | **`4.2%`** | Porcentaje de tiempo consumido en I/O y terminal |

### 1.1. Distribución Empírica del Tiempo (Inferencia vs Tools)
```text
========================================================================================
DISTRIBUCIÓN DEL TIEMPO DE PARED POR SUBAGENTE (INFERENCIA LLM vs TOOLS)
========================================================================================
CTA Architect (part_01):    313s (99.4%) LLM |    2s Tools
CTA Architect (part_02):    130s (94.2%) LLM |    8s Tools
Author Shard 01        :    448s (90.0%) LLM |   50s Tools
Author Shard 02        :    725s (95.5%) LLM |   34s Tools
Author Shard 03        :    453s (97.6%) LLM |   11s Tools
Author Shard 04        :    454s (96.0%) LLM |   19s Tools
Author Shard 05        :    514s (95.0%) LLM |   27s Tools
Author Shard 06        :    585s (96.4%) LLM |   22s Tools
Author Shard 07        :    307s (96.8%) LLM |   10s Tools
Author Shard 08        :    498s (96.1%) LLM |   20s Tools
Author Shard 09        :    719s (93.9%) LLM |   47s Tools
Author Shard 10        :    683s (93.6%) LLM |   46s Tools
Author Shard 11        :    445s (94.1%) LLM |   28s Tools
Author Shard 12        :    752s (94.5%) LLM |   44s Tools
Author Shard 13        :    423s (91.6%) LLM |   39s Tools
Author Shard 14        :    447s (95.7%) LLM |   20s Tools
Author Shard 15        :    554s (93.9%) LLM |   36s Tools
Author Shard 16        :    700s (95.6%) LLM |   32s Tools
Author Shard 17        :    642s (94.6%) LLM |   32s Tools
Author Shard 18        :    691s (94.4%) LLM |   34s Tools
Author Shard 19        :    622s (95.0%) LLM |   33s Tools
Author Shard 20        :    519s (96.3%) LLM |   20s Tools
Judge 01               :     77s (98.7%) LLM |    1s Tools
Judge 02               :     77s (98.7%) LLM |    1s Tools
Judge 03               :     92s (98.9%) LLM |    1s Tools
Judge 04               :     73s (100.0%) LLM |    0s Tools
Judge 05               :     98s (99.0%) LLM |    1s Tools
========================================================================================
```

### 1.2. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json`)

| Etapa | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes en Snapshot | Metadatos de Etapa |
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

## 2. Análisis Forense: CTA Architects (Stage 1)
### 2.1. CTA Architect (part_01)
- **Duración Total:** **`5.25 min`** (315.0 s) en **`8 turnos`**.
- **Tokens:** 105,680 In | 41,281 Out | 208,808 Cache.
### 2.2. CTA Architect (part_02)
- **Duración Total:** **`2.3 min`** (138.0 s) en **`27 turnos`**.
- **Tokens:** 119,963 In | 9,675 Out | 866,183 Cache.

---

## 3. Análisis Forense: Shards de Autoría (Stage 3)

| Shard ID | Duración (min) | Turnos | Writes | Edits | Check Runs (Fail/Pass) | Lecturas Validador (Ing. Inversa) | Micro-Bucle / Patrón |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Author Shard 01** | 8.3 | 29 | 0 | 0 | 13 (6/7) | NO (0) | ⚠️ SÍ (Check Loop: 6 fallos) |
| **Author Shard 02** | 12.65 | 49 | 0 | 0 | 7 (4/3) | NO (1) | ⚠️ SÍ (Edición Granular: 49t) |
| **Author Shard 03** | 7.73 | 18 | 0 | 0 | 2 (1/1) | NO (0) | NO |
| **Author Shard 04** | 7.88 | 26 | 0 | 0 | 6 (3/3) | NO (0) | NO |
| **Author Shard 05** | 9.02 | 33 | 0 | 0 | 5 (1/4) | NO (0) | NO |
| **Author Shard 06** | 10.12 | 35 | 0 | 0 | 4 (2/2) | NO (0) | NO |
| **Author Shard 07** | 5.28 | 29 | 0 | 0 | 2 (0/2) | NO (0) | NO |
| **Author Shard 08** | 8.63 | 20 | 0 | 0 | 4 (1/3) | NO (0) | NO |
| **Author Shard 09** | 12.77 | 30 | 0 | 0 | 6 (2/4) | NO (0) | NO |
| **Author Shard 10** | 12.17 | 50 | 0 | 0 | 5 (0/5) | NO (0) | ⚠️ SÍ (Edición Granular: 50t) |
| **Author Shard 11** | 7.88 | 26 | 0 | 0 | 4 (0/4) | NO (0) | NO |
| **Author Shard 12** | 13.27 | 45 | 0 | 0 | 6 (2/4) | NO (0) | ⚠️ SÍ (Edición Granular: 45t) |
| **Author Shard 13** | 7.7 | 33 | 0 | 0 | 6 (0/6) | NO (0) | NO |
| **Author Shard 14** | 7.78 | 30 | 0 | 0 | 9 (5/4) | NO (0) | ⚠️ SÍ (Check Loop: 5 fallos) |
| **Author Shard 15** | 9.83 | 34 | 0 | 0 | 4 (0/4) | NO (0) | NO |
| **Author Shard 16** | 12.2 | 36 | 0 | 0 | 4 (1/3) | NO (0) | ⚠️ SÍ (Edición Granular: 36t) |
| **Author Shard 17** | 11.32 | 34 | 0 | 0 | 5 (1/4) | NO (0) | NO |
| **Author Shard 18** | 12.2 | 24 | 0 | 0 | 4 (2/2) | NO (0) | NO |
| **Author Shard 19** | 10.92 | 26 | 0 | 0 | 6 (1/5) | NO (0) | NO |
| **Author Shard 20** | 8.98 | 23 | 0 | 0 | 4 (2/2) | NO (0) | NO |

---

## 4. Análisis Forense: Blind Judges (Stage 5)

| Blind Judge | Duración (min) | Turnos | Consultas `search_web` | Peticiones HTTP | Estado de Aislamiento |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Judge 01** | 1.3 | 5 | 0 | 0 | ✅ Aislamiento Estricto (Razonamiento Puro) |
| **Judge 02** | 1.3 | 5 | 0 | 0 | ✅ Aislamiento Estricto (Razonamiento Puro) |
| **Judge 03** | 1.55 | 6 | 0 | 0 | ✅ Aislamiento Estricto (Razonamiento Puro) |
| **Judge 04** | 1.22 | 5 | 0 | 0 | ✅ Aislamiento Estricto (Razonamiento Puro) |
| **Judge 05** | 1.65 | 5 | 0 | 0 | ✅ Aislamiento Estricto (Razonamiento Puro) |

---

## 5. Taxonomía Consolidada de Errores (85 Registrados)

| Categoría de Error | Ocurrencias | Ejemplo de Incidencia | Razonamiento Previo (Thinking) |
| :--- | :---: | :--- | :--- |
| **Missing File / Relative Path / Directory Error (FileNotFoundError)** | **35** | `CTA Architect (part_02)` (Paso 6): Encountered error in step execution: declaring permissions: cortex too... | *Sin thinking capturado* |
| **Parameter Diversity & Option Collapse (TPL-VAR / TPL-COLLAPSE)** | **26** | `Orchestrator` (Paso 99): Partial read (lines 1-77 of 77). Showing bytes 0-46080 of 170779 in th... | `Investigating the transcript of `shard_02` for clues. Identified the transcript'...` |
| **Shard Compilation & Template Validator Failure (compile_shard / check_templates)** | **8** | `Author Shard 01` (Paso 14): The command exited with code 1. | Output: | ERROR: No existe el archiv... | `The "templates" directory is not yet present. Investigating whether `shard_01.js...` |
| **PowerShell Command / Quoting / $Variable Expansion Friction** | **5** | `Author Shard 15` (Paso 12): The command exited with code 1. | Output: | = : El t�rmino '=' no se r... | `The manifest file will specify the configuration of `shard_15`, including requir...` |
| **Non-Zero CLI Exit / Subprocess Probe (Exit Code 1)** | **4** | `Orchestrator` (Paso 111): Encountered error in step execution: cannot kill task "bb98a610-c34f-4... | *Sin thinking capturado* |
| **Anti-Giveaway & Psychometric Parity Violations (R-14..R-19)** | **4** | `Author Shard 10` (Paso 36): Encountered error in step execution: tool call denied by pre-tool hook... | *Sin thinking capturado* |
| **KaTeX Double Curly Braces ({{ / }})** | **1** | `Orchestrator` (Paso 178): Partial read (lines 100-157 of 157). Showing bytes 0-46080 of 81957 in... | `The compilation failed, triggering a circuit breaker on a specific data file due...` |
| **Cross-check Verification False (TPL-CROSS)** | **1** | `Author Shard 04` (Paso 34): The command exited with code 1. | Output: | [-] [TPL-DRY: FALLO EN EJE... | *Sin thinking capturado* |
| **LaTeX Control Character / Raw-String Corruption (R-03 / SyntaxWarning)** | **1** | `Author Shard 06` (Paso 42): The command exited with code 1. | Output: | <truncated 324 lines> | <s... | `The data shard is ready. Attempting to compile the shard using the designated sc...` |

---

## 6. Telemetría de Razonamiento Cognitivo (Thinking Traces)
- **Total de Turnos con Razonamiento:** `379 turnos`
- **Volumen Total de Razonamiento:** `924,752 caracteres`

| Agente | Turnos con Thinking | Volumen (Caracteres) | Muestra de Razonamiento Previo |
| :--- | :---: | :---: | :--- |
| **Author Shard 01** | 17 | 38,334 | `The task involves creating a data file for a specific shard. Need to ensure the ...` |
| **Author Shard 02** | 26 | 51,228 | `Understanding the request, the primary task is to create a Python file, `shard_0...` |
| **Author Shard 03** | 8 | 38,391 | `Assigned the task to author a shard and retrieve the work order. The initial pre...` |
| **Author Shard 04** | 13 | 29,569 | `Task is to read a specified file, write a Python file with specific naming conve...` |
| **Author Shard 05** | 17 | 38,710 | `Received a work order specifying the assigned shard and associated JSON item. Th...` |
| **Author Shard 06** | 18 | 34,905 | `Initial task: Shard author `shard_06` according to the provided work order. The ...` |
| **Author Shard 07** | 13 | 23,717 | `Initial assessment involves understanding the assigned role and target file for ...` |
| **Author Shard 08** | 11 | 46,268 | `Reviewing the provided work order to understand the task assigned. The file name...` |
| **Author Shard 09** | 16 | 30,151 | `I'm thinking through how to approach this.


The initial step necessitates confi...` |
| **Author Shard 10** | 26 | 46,125 | `The task involves authoring content for shard_10, reading course materials and d...` |
| **Author Shard 11** | 15 | 33,254 | `Reviewing the instructions, confirming the designated shard author role and work...` |
| **Author Shard 12** | 25 | 54,689 | `Acknowledged the role of Shard Author for `shard_12` within the specified work o...` |
| **Author Shard 13** | 14 | 27,735 | `Checking the pre-shard guard manifest to ensure the current shard's task aligns ...` |
| **Author Shard 14** | 17 | 33,627 | `Reviewing the provided instructions, the task involves authoring a data file and...` |
| **Author Shard 15** | 17 | 45,529 | `Instructions specify writing a data file and compiling it. The goal is to genera...` |
| **Author Shard 16** | 13 | 34,119 | `Initial assessment involves examining the course materials and associated data f...` |
| **Author Shard 17** | 17 | 57,971 | `Reviewing the instructions, the focus is on a specific work order related to `sh...` |
| **Author Shard 18** | 11 | 60,171 | `The task involves authoring content for shard_18, guided by instructions from a ...` |
| **Author Shard 19** | 15 | 51,856 | `Acknowledged the work order; the objective is to process author data and generat...` |
| **Author Shard 20** | 12 | 43,615 | `Analyzing course materials and associated data to understand the content structu...` |
| **CTA Architect (part_01)** | 6 | 29,627 | `I'm thinking through how to approach this....` |
| **CTA Architect (part_02)** | 12 | 5,358 | `Task requires processing a work order and adhering to specific read/write permis...` |
| **Judge 01** | 2 | 7,614 | `Initial task assignment received. The agent is confirming work order details, in...` |
| **Judge 02** | 2 | 10,181 | `Initiating the blind judging process. The first step involves retrieving and exa...` |
| **Judge 03** | 3 | 16,712 | `Initiating the first turn by reading the specified file, recognizing this is the...` |
| **Judge 04** | 2 | 9,423 | `Initial assessment: Received a task to judge an item from a specified file. The ...` |
| **Judge 05** | 3 | 14,589 | `Examining the specified file to understand the assigned task. The instructions s...` |
| **Orchestrator** | 28 | 11,284 | `Immediately, the explicit instruction dictates starting with the bootstrap stage...` |

---
*Informe generado automáticamente por `traceback_analyzer.py`.*


---

## 7. Deep-Dive Forense de los 20 Shards (Auditoría Paralela 4x Flash) y Caso Especial `shard_02`

### 7.1. Desglose Completo de Tiempos Pre-Compilación vs Post-Compilación y Reglas Infringidas

| Shard ID | Competencias | Duración (s / min) | Pre-1ra Comp. | Post-1ra Comp. | Compilaciones Reales (Pass/Fail) | Códigos de Error Post-1ra-Compilación | Aislamiento Cross-Course (`v2` / otros cursos) |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **`shard_01`** | `Hab-01` | 498s (8.30m) | 59s (11.8%) | 439s (88.2%) | 12 (6P / 6F) | `FileNotFound` (prematuro), `[TPL-VAR]`, `[R-15]`, Paridad (`Hab-01_1`), `[TPL-DRY]` (`f-string`), `[R-18]` | ✅ 100% Aislado |
| **`shard_02` (Int. 1)** | `Hab-02` | 1273s (21.22m) | 349s (27.4%) | 924s (72.6%) | 6 (0P / 6F) | `[R-20]` (`\text{Asy. Var}[b_}{LS}]`), `[R-18]`, `[TPL-D4]`, `[TPL-VAR]`, `CIRCUIT BREAKER` (Paso 71) | ✅ 100% Aislado (Cancelado) |
| **`shard_02` (Int. 2)** | `Hab-02` | 1055s (17.58m) | 52s (4.9%) | 1003s (95.1%) | 5 (0P / 5F) | `2x [NO-CHANGE]` + `5x CIRCUIT BREAKER` heredados (no se limpió `.check_attempts/`) | ✅ 100% Aislado (Cancelado) |
| **`shard_02` (Int. 3)** | `Hab-02` | 759s (12.65m) | 48s (6.3%) | 711s (93.7%) | 3 (1P / 2F) | `[TPL-DRY]`, `[R-18]`, `[R-20]`, `[TPL-VAR]` -> Resuelto al desacoplar `$@d1@$` de `error_rationale` | 🟡 Leyó `shard_01/03/06` de `v3` |
| **`shard_03`** | `Hab-03` | 464s (7.73m) | 307s (66.2%) | 157s (33.8%) | 2 (1P / 1F) | `[R-18]`, `[TPL-D4]` (`0.005000` duplicado), `[TPL-VAR]` | ✅ 100% Aislado |
| **`shard_04`** | `Hab-04` | 473s (7.88m) | 191s (40.4%) | 282s (59.6%) | 5 (2P / 3F) | `[TPL-VAR]`, `[TPL-DRY]` (`ValueError` format specifier & `AssertionError` en `ver_hab04`) | 🟡 Leyó `shard_01` de `v3` |
| **`shard_05`** | `Hab-05` | 541s (9.02m) | 357s (66.0%) | 184s (34.0%) | 4 (3P / 1F) | `[R-18]` (13 errores por gerundios delatores: `"omitiendo..."`, `"invirtiendo..."`) | 🚨 **Violó Cross-Course:** Leyó `v2/work/shards/shard_05_data.py` |
| **`shard_06`** | `Hab-06` | 607s (10.12m) | 314s (51.7%) | 293s (48.3%) | 3 (1P / 2F) | `[AST]` (`\beta`, `\alpha`, `\theta` sin `r'...'`), `[R-18]`, `[TPL-VAR]` | 🚨 **Violó Cross-Course:** Leyó `practica_parcial_saul` |
| **`shard_07`** | `Hab-07` | 317s (5.28m) | 253s (79.8%) | 64s (20.2%) | 1 (1P / 0F) | Ninguno (1st-pass por copia de `v2`) | 🚨 **Violó Cross-Course:** Leyó `v2/work/shards/shard_07_data.py` |
| **`shard_08`** | `Hab-08` | 518s (8.63m) | 368s (71.0%) | 150s (29.0%) | 3 (2P / 1F) | `[TPL-VAR]` (`k in [3,4,5]` x `j in [2,6]` = 6 combinaciones < 30) | 🌟 **100% Clean-Room** |
| **`shard_09`** | `Hab-09` | 766s (12.77m) | 340s (44.4%) | 426s (55.6%) | 5 (3P / 2F) | Paridad (`shard_01` target), `[R-18]` (5 giveaways) + **328s en Paranoid Loop post-pase** | 🟡 Leyó `shard_01` de `v3` |
| **`shard_10`** | `C-04, C-05` | 730s (12.17m) | 478s (65.5%) | 252s (34.5%) | 4 (4P / 0F) | Ninguno, pero perdió **252s post-pase** al confundir `"2 plantillas"` con 2 de 8 arquetipos | 🚨 **Violó Cross-Course:** Leyó `v2`, `estadistica_asintotica` y `practica_parcial_saul` |
| **`shard_11`** | `C-06, C-07` | 473s (7.88m) | 320s (67.7%) | 153s (32.3%) | 3 (3P / 0F) | Ninguno (153s post-pase verificando JSONs) | 🟡 Leyó `shard_01/07/10` de `v3` |
| **`shard_12`** | `C-09, C-10` | 796s (13.27m) | 432s (54.3%) | 364s (45.7%) | 5 (3P / 2F) | `[R-15]`, `[TPL-VAR]`, `[R-18]`, `[NO-CHANGE]` + reescritura de 53.8 KB | 🟡 Leyó `shard_01/02/10` de `v3` |
| **`shard_13`** | `C-12, C-13` | 462s (7.70m) | 296s (64.1%) | 166s (35.9%) | 5 (5P / 0F) | Ninguno (166s post-pase verificando JSONs) | 🟡 Leyó `shard_01/05/10/11` de `v3` |
| **`shard_14`** | `C-14, C-15` | 467s (7.78m) | 188s (40.3%) | 279s (59.7%) | 8 (4P / 4F) | `FileNotFound` (x3 prematuros), Paridad (`C-15` omitido), `[TPL-VAR]` | 🌟 **100% Clean-Room** |
| **`shard_15`** | `H-01, C-01` | 590s (9.83m) | 511s (86.6%) | 79s (13.4%) | 3 (3P / 0F) | Ninguno (1st-pass tras `write_file` de 4m 42s) | 🟡 Leyó `shard_01/02` de `v3` |
| **`shard_16`** | `H-02, C-02` | 732s (12.20m) | 440s (60.1%) | 292s (39.9%) | 3 (2P / 1F) | `[R-15]`, `[TPL-VAR]` + 3 `write_file` de 57 KB (466s en streaming) | 🟡 Leyó `shard_01/02/03/10/15` de `v3` |
| **`shard_17`** | `H-03, C-03` | 679s (11.32m) | 379s (55.8%) | 300s (44.2%) | 3 (1P / 2F) | `[R-15]`, `[TPL-VAR]`, `[NO-CHANGE]` | 🟡 Leyó `shard_01/02/07/10/16` de `v3` |
| **`shard_18`** | `H-04, C-08` | 732s (12.20m) | 306s (41.8%) | 426s (58.2%) | 4 (1P / 3F) | `[R-18]` (x3), `[R-20]` (`hat{\theta}`), `[TPL-VAR]` (x3) + 4 `write_file` de 33–42 KB (566s) | 🌟 **100% Clean-Room** |
| **`shard_19`** | `C-11, H-05` | 655s (10.92m) | 323s (49.3%) | 332s (50.7%) | 5 (4P / 1F) | `[R-15]` tras expandir de 3 a 6 distractores (corregido con `edit_file` de 43 líneas) | 🌟 **100% Clean-Room** |
| **`shard_20`** | `H-06` | 539s (8.98m) | 270s (50.1%) | 269s (49.9%) | 4 (2P / 2F) | `[R-20]` (x2 por signos `$` impares), `[TPL-VAR]` (x2) | 🌟 **100% Clean-Room** |


---

### 7.2. Diagnóstico Raíz Detrás de los Errores: `shard_08` (`reference_cleanroom`) vs los Otros 19 Shards y `shard_02`

1. **Por qué `shard_08` pasó limpio mientras `shard_02`, `shard_03`, `shard_01` y `shard_06` chocaron con `[R-18: DISTRACTORES BOILERPLATE SINTÉTICOS]`:**
   - En `engine/invariants.py` y `src/validator/rules.py`, `check_synthetic_boilerplate_distractors` calculaba `_skeleton(d)` sin remover primero las expresiones matemáticas `$...$`.
   - En `shard_08_data.py`, las opciones numéricas `r"$\text{Avar} = @d1@$"` producían el esqueleto `\text{avar} = <NUM>` de **19 caracteres (`< 20`)** y solo definían **3 distractores manuales (`< 4`)**, esquivando el umbral `len(sk) >= 20` y `len(group) >= 4` por **1 solo carácter**.
   - En `shard_02` (Intento 1) y `shard_03`, las 6 opciones `r"$\text{Est. Asy. Var}[b_{IV}] = @d1@$"` producían el esqueleto `\text{est asy var} b_{iv} = <NUM>` de **33 caracteres (`>= 20`)** en los 6 distractores (`>= 4`), disparando un **falso positivo `[R-18]`**.
   - Cuando `shard_02` (Intento 1) obedeció la instrucción del validador de agregar explicaciones conceptuales dentro del `"value"` de cada opción LaTeX, corrompió llaves (`\text{Asy. Var}[b_}{LS}]` $\to$ `[R-20]`), introdujo gerundios delatores (`[R-18: META-INFORMACIÓN]`) y cayó en el Circuit Breaker a los 21 minutos.
2. **Por qué 11 de los 20 shards (incluido `shard_08` en su 1er intento) fallaron `[TPL-VAR]`:**
   - `system_prompts/lean/prompt_shard_author.md` (L22) decía `TPL-VAR: Generator must produce >= 4 unique instances across seeds`, contradiciendo directamente el contrato real del validador ($\ge 30$ instancias únicas en 50 semillas para `Hab-*` y $\ge 20$ para `C-*`/`H-*`).
3. **Por qué seguían ocurriendo fallos de LaTeX (`[AST]` / `[R-20]`) pese a `r"..."` y `@var@`:**
   - `extract_function_code` en `compile_shard.py` (L446) llamaba a `inspect.getsource(fn_or_str)` antes de consultar `locator.lines`, leyendo el código **sin curar desde el disco** y anulando la auto-curación en memoria de `heal_shard_source_text` (lo que causó el fallo `[AST]` de `\beta, \alpha, \theta` en `shard_06`).
   - Faltaba además auto-curar en `heal_shard_source_text` los comandos matemáticos sin barra dentro de `$...$` (`hat{\theta}` $\to$ `\hat{\theta}` en `shard_18`), `\implies` $\to$ `\Rightarrow` (`shard_11, 20`) y el doble `$$` accidental al final de expresiones inline (`shard_20`).
4. **Todos estos defectos de motor, validador y prompts han sido parcheados en `engine/invariants.py`, `src/validator/rules.py`, `compile_shard.py`, `system_prompts/lean/prompt_shard_author.md` y `dispatch.py`.**
