# Informe de Auditoría Forense Agéntica ("No Headless"): Ejecución Content-to-Course `solow_m20_v11`

**Fecha de Auditoría:** `2026-11-22 21:00:00 UTC`  
**Curso Auditado:** `solow_m20_v11` (*Solow M20 V11* — 36 páginas fuente / 1.49 MB, 20 competencias, 20 shards, 621 reactivos)  
**Conversación Orquestadora:** [`dc8545ff-fd7d-4e36-8545-6411880c0eb2`](conversation://dc8545ff-fd7d-4e36-8545-6411880c0eb2) ([transcript.jsonl](file:///C:/Users/augus/.gemini/antigravity/brain/dc8545ff-fd7d-4e36-8545-6411880c0eb2/.system_generated/logs/transcript.jsonl))  
**Directorio de Trabajo Auditado:** [`courses/solow_m20_v11/work`](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/solow_m20_v11/work)  
**Artefactos Base Contrastados:** [report.md](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/c2c_audits/20261122_160000_solow_m20_v11_dc8545ff/report.md), [telemetry.json](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/c2c_audits/20261122_160000_solow_m20_v11_dc8545ff/telemetry.json), [traceback_deepdive_dc8545ff.md](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/c2c_audits/20261122_160000_solow_m20_v11_dc8545ff/traceback_deepdive_dc8545ff.md), [shard_timing_decomposition.md](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/c2c_audits/20261122_160000_solow_m20_v11_dc8545ff/shard_timing_decomposition.md)

---

## 1. Resumen Ejecutivo Forense y Unit Economics

> [!IMPORTANT]
> **Veredicto Global de Auditoría Forense:** **CERTIFICADO CON AISLAMIENTO 100.00% ZERO-COLLISION Y ADOPCIÓN TOTAL DE MEJORAS POST-v7/v8**.  
> El curso `solow_m20_v11` completó el pipeline extremo a extremo en **`23.78 min`** (`1,427.00 s`) con **`50 subagentes`** desplegados (`4` CTA, `20` Autores, `7` Repair Engineers, `19` Blind Judges), **`0` intervenciones manuales del supervisor**, **`100.00%` de adopción de verificadores algebraicos/numéricos `c2c_ver.*`** (`183` plantillas en `20/20` shards), **`0` reescrituras destructivas post-compilación (`write_file`)**, y calificación final de calidad **`19.80 / 20.00 pts` (PLATINUM MASTERY, MPRI `99.18 / 100.00`)**.

| Métrica Forense / Unit Economics | Valor Verificado | Benchmark Óptimo | Diagnóstico Forense |
| :--- | :---: | :---: | :--- |
| **Tiempo Total de Pared / Cómputo** | `23.78 min` (`1,427.00 s`) / `94.87 min` | `< 25.00 min` | Factor de aceleración paralela **`3.99x`** |
| **Volumen Total de Tokens (con Caché)** | `10,942,792` (`3,195,061` activos) | — | In: `2,445,355` \| Out: `749,706` \| Cache: `7,747,731` \| Think: `103,181` |
| **Costo Total Estimado (Gemini 4 Hydrogen)** | **`$9.87 USD`** | `< $12.00 USD` | In: `$3.67` \| Out+Think: `$5.62` \| Cache: `$0.58` |
| **Tokens Totales / Activos por Pregunta** | `17,621.20` / `5,145.00 tok/preg` | `15,000 – 35,000` | Alta eficiencia de contexto gracias a Turn-0 data slices |
| **Segundos de Pared por Pregunta / QPM** | `2.30 s/preg` / `26.11 preg/min` | `2.00 – 5.00 s/preg` | Throughput óptimo (`621` reactivos finales validados) |
| **Costo por Pregunta / por Competencia** | `$0.02 USD/preg` / `$0.49 USD/comp` | `< $0.03 USD/preg` | Autoría pura: `80,310.70 tok/comp` (`$5.33 USD` en Stage 3) |
| **First-Time-Pass (FTP) en Stage 3** | **`15.00%`** (`3/20` shards) | `> 40.00%` | `17/20` shards resolvieron en 2da compilación (`1` solo turno de `edit_file`); `shard_02` requirió 3 compilaciones |
| **Adopción de `c2c_ver.*` en Stage 3** | **`100.00%`** (`20/20` shards, `183` usos) | `100.00%` | `m20_guard`: `141` \| `equiv`: `24` \| `numeric`: `18` |
| **Disciplina Quirúrgica (`edit_file` vs `write_file`)** | `20` writes iniciales / `66` edits (Stage 3) | `0` re-writes | `100.00%` cumplimiento de edición quirúrgica post-compilación (`+19` edits en Stage 3B) |

---

## 2. Verificación de Aislamiento Estricto por `conversation_id` (Zero-Collision Gate)

Se auditó física y criptográficamente la cadena de custodia de telemetría para la conversación orquestadora [`dc8545ff-fd7d-4e36-8545-6411880c0eb2`](conversation://dc8545ff-fd7d-4e36-8545-6411880c0eb2):

1. **Estado Maestro ([work/state.json](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/solow_m20_v11/work/state.json#L1-L8)):**
   - Estampado con `"course_id": "solow_m20_v11"`, `"conversation_id": "dc8545ff-fd7d-4e36-8545-6411880c0eb2"`, `"status": "completed"` y `"last_stage": "06_publish"`.
2. **Snapshots Incrementales ([work/telemetry/*.json](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/solow_m20_v11/work/telemetry/00_prepare.json)):**
   - Los **9 snapshots de etapa** (`00_prepare.json`, `00b_bootstrap.json`, `01_cta.json`, `02_shard.json`, `03_templates.json`, `04_build.json`, `05_verify.json`, `05b_judge_compare.json`, `06_publish.json`) contienen `"conversation_id": "dc8545ff-fd7d-4e36-8545-6411880c0eb2"`.
   - Los 4 logs auxiliares del sanitizador KaTeX ([cta_sanitizer_log.json](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/solow_m20_v11/work/telemetry/cta_sanitizer_log.json), `cta_sanitizer_part_01..03.json`) registran `"course_id": "solow_m20_v11"` con timestamps dentro de la ventana de Stage 1B (`20:36:59Z` – `20:37:06Z`).
3. **Espejo por Conversación ([work/telemetry/by_conversation/dc8545ff-fd7d-4e36-8545-6411880c0eb2/](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/solow_m20_v11/work/telemetry/by_conversation/dc8545ff-fd7d-4e36-8545-6411880c0eb2/state.json)):**
   - Existe un único directorio bajo `by_conversation/`, correspondiente exactamente a `dc8545ff-fd7d-4e36-8545-6411880c0eb2`, con copia espejo íntegra de los `10` artefactos JSON (`9` snapshots + `state.json`). Cero contaminación cruzada con corridas previas (`v7`, `v8`, `v10`).
4. **Telemetría Consolidada del Run ([telemetry.json](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/c2c_audits/20261122_160000_solow_m20_v11_dc8545ff/telemetry.json#L2-L8)):**
   - `meta.orchestrator_conversation_id == "dc8545ff-fd7d-4e36-8545-6411880c0eb2"`, `workload.work_dir_conversation_match == true` y `meta.telemetry_v3_snapshots_used == 9`.

---

## 3. Evaluación Forense de Mejoras Post-v7/v8 en `Stage 3` (Shard Authors)

### 3.1. `first_compile_pass_rate` (FTP) y Desempaquetado de Reglas Bloqueantes Reales en 1ra Compilación

- **Tasa de Aprobación en 1ra Compilación (`first_compile_pass_rate`):** **`15.00%`** (`3/20` shards aprobaron al primer intento sin ediciones: `shard_01` en `107.00 s`, `shard_03` en `111.00 s` y `shard_04` en `125.00 s`).
- **Convergencia en 2da Compilación:** **`80.00%`** (`16/20` shards aprobaron en su 2do intento tras un único turno de `edit_file`), elevando la tasa acumulada al 2do intento a **`95.00%`** (`19/20` shards). Solo `shard_02` requirió un 3er intento (`319.00 s`).
- **Exclusión Confirmada de `[EPISTEMIC-CLOSURE-WARNING]`:** Aunque el validador emitió `82` líneas informativas `[EPISTEMIC-CLOSURE-WARNING]` a lo largo de las compilaciones de Stage 3 (recordando que variables libres como `T1, g, n, r, s` en `open_symbolic` / `invariant_canvas` requieren cierre epistémico), **`0` de ellas contaminaron `first_compile_top_rules` ni bloquearon compilaciones**.

#### Contraste Forense: `first_compile_top_rules` (Telemetry) vs. Reglas Bloqueantes Reales en 1ra Compilación
En [telemetry.json](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/c2c_audits/20261122_160000_solow_m20_v11_dc8545ff/telemetry.json), el extractor captura tanto la categoría envolvente `[GENERAL]` como la regla interna en la línea `Causa: FAIL: [<REGLA>]`, además de advertencias estáticas de `[PRECHECK]`:

| Regla / Código en 1ra Compilación | Conteo en `telemetry.json` | Shards Afectados (IDs) | Naturaleza Forense Real |
| :--- | :---: | :--- | :--- |
| **`[TPL-VAR]`** | **8 shards** | `shard_02, 06, 07, 09, 13, 17, 18, 20` | **Bloqueante real:** Cuota de diversidad (< 4 instancias únicas en 300 intentos RNG o < 30 ítems). |
| **`[GENERAL]`** *(contenedor de reglas `TPL-*`)* | **6 shards** | `shard_10, 11, 12, 14, 15, 19` | **Contenedor sintético:** En `shard_11, 12, 14, 15, 19` envuelve `[TPL-CONST-DISTRACTOR]`; en `shard_10` envuelve `[TPL-STEM-DERIV-GIVEAWAY]`. |
| **`[R-19]`** *(Minimum Distractor Epsilon)* | **5 shards** | `shard_07, 09, 10, 13, 20` | **Bloqueante real:** Distancia relativa entre distractor numérico y clave $< 1.50\%$ o colisión numérica. |
| **`[TPL-CONST-DISTRACTOR]`** | **5 shards** | `shard_11, 12, 14, 15, 19` | **Bloqueante real** (reportado dentro de `[GENERAL]`): Distractor estático o expresión idéntica entre semillas. |
| **`[TPL-STATIC-OPT]`** | **4 shards** | `shard_05, 07, 08, 20` | **Bloqueante real:** Menos de 10 respuestas correctas únicas en dry-run de 50 semillas. |
| **`[TPL-DIGIT-PLACEHOLDER-CONCAT]`** | **2 shards** | `shard_06, 18` | **Bloqueante real:** Concatenación literal de dígito con token `@var@` sin operador explícito. |
| **`[VERIFIER-TAUTOLOGY-DETECTED]`** | **2 shards** | `shard_07, 20` | **Bloqueante real:** Expresión en verificador evaluada como constante/tautológica. |
| **`[TPL-DYNAMIC-RATIONALE]`** | **2 shards** | `shard_09, 20` | **Advertencia `[PRECHECK]` no bloqueante:** Explicación de distractor sin token `@var@` (en `shard_09` persistió en el intento 2 con `exit code 0`). |
| **`[INVARIANT]`** | **1 shard** | `shard_06` | **Bloqueante real:** Violación estructural en dry-run de 50 semillas (también ocurrió en intento #2 de `shard_02`). |
| **`[OPEN-SYM-DISJOINT]`** | **1 shard** | `shard_02` | **Bloqueante real:** Fuga de decimales numéricos fantasma (`0.6`, `0.48`) en `error_rationale` de ítem `open_symbolic`. |
| **`[R-15-MS]`** | **1 shard** | `shard_17` | **Bloqueante real:** Asimetría de longitud en opciones de `multiple_select`. |
| **`[TPL-ASM]` / `[ADV-WITNESS-INVALID]`** | **1 shard** | `shard_16` | **Bloqueante real:** Contraejemplo testigo inválido en `adversarial_break`. |
| **`[TPL-KATEX-SYMPY-LEAK]`** | **1 shard** | `shard_06` | **Bloqueante real:** Sintaxis cruda de SymPy (`*`, `**`) filtrada en cadena LaTeX. |
| **`[TPL-STEM-DERIV-GIVEAWAY]`** | **1 shard** | `shard_10` | **Bloqueante real** (dentro de `[GENERAL]`): El enunciado regala la derivada o paso algebraico pedido. |
| **`[TPL-STEM-VARIANT-PARITY]`** | **1 shard** | `shard_17` | **Bloqueante real:** Desbalance de símbolos/tokens entre variantes de stem `S1..S9`. |
| **`[LATEX-RAW-STRING]`** | **1 shard** | `shard_02` | **Advertencia `[PRECHECK]`:** Uso de `\alpha` en string sin prefijo raw `r"..."` en L508. |

---

### 3.2. Adopción de `c2c_ver.*` (`numeric`, `equiv`, `m20_guard`) en `work/shards/shard_XX_data.py`

La inspección estática de los 20 archivos [`work/shards/shard_01_data.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/solow_m20_v11/work/shards/shard_01_data.py) a [`shard_20_data.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/solow_m20_v11/work/shards/shard_20_data.py) confirma una **adopción del `100.00%`** (`20/20` shards, **`183` invocaciones totales**, equivalentes a 1 verificador por cada una de las 183 plantillas del curso):

- **`c2c_ver.m20_guard`:** **`141` plantillas** (`77.05%`) — empleado universalmente en modalidades interactivas M20 (`unstructured_model`, `invariant_canvas`, `proof_dag`, `adversarial_break`, `concept_matching`, `multiple_select`).
- **`c2c_ver.equiv`:** **`24` plantillas** (`13.11%`) — empleado en las 3 plantillas `open_symbolic` de las 8 competencias de habilidad (`shard_01` a `shard_08`, `8 × 3 = 24`).
- **`c2c_ver.numeric`:** **`18` plantillas** (`9.84%`) — empleado en las 3 plantillas `fill_in_the_blank` de `shard_02, 04, 05, 07, 08` y `shard_20` (`6 × 3 = 18`).

| Shard | Competencia (Tipo) | `c2c_ver.numeric` | `c2c_ver.equiv` | `c2c_ver.m20_guard` | Total `c2c_ver.*` | Archivo Fuente |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **`shard_01`** | `Hab-01` (Skill) | 0 | 3 | 6 | **9** | [shard_01_data.py](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/solow_m20_v11/work/shards/shard_01_data.py) |
| **`shard_02`** | `Hab-02` (Skill) | 3 | 3 | 3 | **9** | [shard_02_data.py](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/solow_m20_v11/work/shards/shard_02_data.py) |
| **`shard_03`** | `Hab-03` (Skill) | 0 | 3 | 6 | **9** | [shard_03_data.py](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/solow_m20_v11/work/shards/shard_03_data.py) |
| **`shard_04`** | `Hab-04` (Skill) | 3 | 3 | 3 | **9** | [shard_04_data.py](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/solow_m20_v11/work/shards/shard_04_data.py) |
| **`shard_05`** | `Hab-05` (Skill) | 3 | 3 | 3 | **9** | [shard_05_data.py](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/solow_m20_v11/work/shards/shard_05_data.py) |
| **`shard_06`** | `Hab-06` (Skill) | 0 | 3 | 6 | **9** | [shard_06_data.py](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/solow_m20_v11/work/shards/shard_06_data.py) |
| **`shard_07`** | `Hab-07` (Skill) | 3 | 3 | 3 | **9** | [shard_07_data.py](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/solow_m20_v11/work/shards/shard_07_data.py) |
| **`shard_08`** | `Hab-08` (Skill) | 3 | 3 | 3 | **9** | [shard_08_data.py](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/solow_m20_v11/work/shards/shard_08_data.py) |
| **`shard_09`** | `C-07` (Concept) | 0 | 0 | 12 | **12** | [shard_09_data.py](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/solow_m20_v11/work/shards/shard_09_data.py) |
| **`shard_10..19`** | `C-01..06, C-09..12` | 0 (c/u) | 0 (c/u) | 9 (c/u) | **90** (`9×10`) | [shard_10_data.py](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/solow_m20_v11/work/shards/shard_10_data.py)..[shard_19_data.py](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/solow_m20_v11/work/shards/shard_19_data.py) |
| **`shard_20`** | `H-01` (Fact) | 3 | 0 | 6 | **9** | [shard_20_data.py](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/solow_m20_v11/work/shards/shard_20_data.py) |
| **TOTAL** | **20 Competencias** | **18** | **24** | **141** | **183** | **100.00% cobertura** |

---

### 3.3. Conteo Exacto de `INFO: [AUTO-FIXED]`, `WARNING:` No Bloqueantes y Uso de `edit_file` vs `write_file`

#### A. Poda Automática `INFO: [AUTO-FIXED]` y `WARNING:` No Bloqueantes (Deduplicados por Ejecución de `compile_shard.py`)
1. **`INFO: [AUTO-FIXED] [TPL-ORPHAN-VARS]`:**
   - **Stage 3 (Autores — 38 ejecuciones de `compile_shard.py`):** **`15` auto-fixes en 1ra compilación** (`26` acumulados en las 38 compilaciones; `34` ocurrencias crudas en `transcript.jsonl` incluyendo re-lecturas de log), podando automáticamente claves auxiliares de `vars` no interpoladas en texto (`shard_01, 02, 07, 11, 12, 14, 15, 18, 19`).
   - **Stage 3B (Repairs — 8 ejecuciones de `compile_shard.py`):** **`10` auto-fixes** (`shard_12` / `C-03`: 5; `shard_14` / `C-05`: 3 en 3 rondas; `shard_07` / `Hab-07`: 2).
   - **Impacto:** Evitó que **9 shards en Stage 3** (`45.00%` de los autores, incluyendo el clean-room `shard_01`) fallaran por variables auxiliares huérfanas (`sl`, `inv_al`, `r1`, `r3`, `y2`, `g_kl`).
2. **`WARNING:` No Bloqueantes:**
   - **Stage 3 (38 compilaciones):** **`70` warnings en 1ra compilación** (`118` acumulados en las 38 compilaciones):
     - `[EPISTEMIC-CLOSURE-WARNING]`: **`82` ocurrencias** (100% no bloqueantes).
     - `WARNING: [BLOOM-SUPERIOR-TARGET]`: **`27` ocurrencias** (aviso no bloqueante cuando la cuota Analyze+Evaluate de un shard es `66.70%` frente al `70.00%` recomendado).
     - `WARNING: [TPL-STEM-SYMBOL-PARITY]`: **`9` ocurrencias** (aviso no bloqueante de paridad de símbolos entre variantes de enunciado en `shard_03, 10, 12, 15, 17`).
   - **Stage 3B (8 compilaciones):** **`23` warnings no bloqueantes** (`14` `[EPISTEMIC-CLOSURE-WARNING]`, `7` `[BLOOM-SUPERIOR-TARGET]`, `2` `[TPL-STEM-SYMBOL-PARITY]`, más `4` avisos `[!] Warning: Se detectó rf"..."` en `Hab-07`).

#### B. Disciplina de Herramientas: `edit_file` vs `write_file`
- **Stage 3 (20 Shard Authors):**
  - **`write_file`:** Exactamente **`20` llamadas** (`1.00` por shard, únicamente para la creación inicial de `shard_XX_data.py` en el Turno 2). **Cero (`0`) llamadas a `write_file(Overwrite=True)` tras la 1ra compilación**.
  - **`edit_file`:** **`66` llamadas quirúrgicas** distribuidas entre los 17 shards que requirieron remediación (`min=1`, `med=4`, `max=8` en `shard_10` y `shard_18`).
- **Stage 3B (7 Repair Engineers):**
  - **`write_file`:** **`0` llamadas**.
  - **`edit_file`:** **`19` llamadas quirúrgicas** (`1` a `3` edits en los 6 ingenieros que aprobaron al 1er intento; `9` edits en `Repair Engineer Hab-07`).

---

### 3.4. Descomposición Paso a Paso del Straggler Crítico: `Shard Author shard_02` (`319.00 s`)

- **Identificación:** [`Shard Author shard_02`](conversation://9331d87b-f93d-4791-9024-dae2a8bd8292) ([transcript.jsonl](file:///C:/Users/augus/.gemini/antigravity/brain/9331d87b-f93d-4791-9024-dae2a8bd8292/.system_generated/logs/transcript.jsonl)), encargado de la competencia `Hab-02` (*Sustitución de Bernoulli y solución explícita Cobb-Douglas*).
- **Métricas vs. Baseline Clean-Room (`shard_01`):** Duración total **`319.00 s`** (`+212.00 s` vs `shard_01` con `107.00 s`; **`+186.00 s` de retraso en barrera vs. la mediana de `133.00 s`**). Consumió `14` turnos, `109,969` tokens activos (`$0.39 USD`), **`99.00 s` en Pre-1st-Compile** y **`220.00 s` en Post-1st-Compile** (`68.97%` del tiempo total).

| Fase / Pasos (`transcript.jsonl`) | Ventana UTC | Duración | Acción / Herramienta | Diagnóstico Forense de Causa Raíz |
| :--- | :---: | :---: | :--- | :--- |
| **1. Ingesta Turn-0 (Steps 0–2)** | `20:38:01Z – 20:38:04Z` | `3.00 s` | `read_file` ([author_02_data.md](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/solow_m20_v11/work/dispatch/items/author_02_data.md)) | Lectura limpia de la orden de trabajo autosuficiente (129 líneas). |
| **2. Autoría Inicial (Steps 3–4)** | `20:38:04Z – 20:39:40Z` | `96.00 s` | Thinking (`4,121` chars) + `write_file` ([shard_02_data.py](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/solow_m20_v11/work/shards/shard_02_data.py), 786 líneas, `22,403` out tok) | Generación inicial de las 9 plantillas de `Hab-02`. Finaliza `Pre-1st-Compile` en **`99.00 s`** (alineado con `shard_04` que tardó `96.00 s`). |
| **3. Compile #1 Asíncrono (Steps 5–8)** | `20:39:40Z – 20:40:50Z` | **`70.00 s`** | `run_command` (`compile_shard.py`) -> bg [`task-6.log`](file:///C:/Users/augus/.gemini/antigravity/brain/9331d87b-f93d-4791-9024-dae2a8bd8292/.system_generated/tasks/task-6.log) -> `SYSTEM_MESSAGE` (`exit 1`) | **Fallo #1:** (a) `[PRECHECK] L508 [LATEX-RAW-STRING]` (faltó prefijo `r"..."` en cadena con `\alpha`); (b) `[OPEN-SYM-DISJOINT]` en `T-Hab02-01`: `vars` incluía variables numéricas que filtraban decimales fantasma (`0.6`, `0.48`) en `error_rationale` de un ítem `open_symbolic`; (c) `[TPL-VAR]` en `T-Hab02-02` (`1/4` instancias únicas tras 300 intentos RNG; la ejecución de 300 semillas SymPy demoró `67.00 s`). Además, `[AUTO-FIXED]` podó `['inv_al']` en `T-Hab02-03`. |
| **4. Remediación #1 (Steps 9–14)** | `20:40:50Z – 20:41:19Z` | **`29.00 s`** | `read_file` (L480–540) + `3 × edit_file` (L72, L124, L514) | **Error Humano/Agéntico Inducido en el Parche:** Al limpiar `vars` en `gen_2` (`T-Hab02-02`, L72) para corregir `[OPEN-SYM-DISJOINT]` y ampliar rangos para `[TPL-VAR]`, **el autor eliminó accidentalmente la clave `"oma": oma` del diccionario `vars` de `gen_2`**, sin notar que `H2` (L622) y `SOL2` (L664) seguían interpolando el token `@oma@`. |
| **5. Compile #2 Asíncrono (Steps 15–18)** | `20:41:19Z – 20:42:21Z` | **`62.00 s`** | `run_command` (`compile_shard.py`) -> bg [`task-16.log`](file:///C:/Users/augus/.gemini/antigravity/brain/9331d87b-f93d-4791-9024-dae2a8bd8292/.system_generated/tasks/task-16.log) -> `SYSTEM_MESSAGE` (`exit 1`) | **Fallo #2 (Regresión auto-inducida):** `3 × [INVARIANT]` (`Unresolved PrairieLearn template token '@oma@' detected in solution, hint 2, detailed_solution` en las 50 semillas `seed=100..149`), lo que provocó colapso total de `[TPL-VAR]` (`0/4` instancias válidas tras 300 intentos = `59.00 s` de CPU). |
| **6. Remediación #2 (Steps 19–25)** | `20:42:21Z – 20:42:33Z` | **`12.00 s`** | `2 × read_file` (L600–680) + `2 × edit_file` (L622 `H2`, L664 `SOL2`) | Reemplaza `@oma@` por `1-@al@` en `H2` y `SOL2`, eliminando el token huérfano. |
| **7. Compile #3 Asíncrono y Cierre (Steps 26–31)** | `20:42:33Z – 20:43:20Z` | **`47.00 s`** | `run_command` -> bg [`task-27.log`](file:///C:/Users/augus/.gemini/antigravity/brain/9331d87b-f93d-4791-9024-dae2a8bd8292/.system_generated/tasks/task-27.log) (`34.00 s`, `exit 0`) + `finish` | **`[+] PASS`** en `compile_shard.py` (9 plantillas, 50 semillas validadas) y emisión de señal `DONE`. |

> [!TIP]
> **Conclusión de Causa Raíz de `shard_02`:** De los `220.00 s` de Post-1st-Compile, **`113.00 s` (`51.36%`) se perdieron directamente por la regresión auto-inducida en el Paso 11** (borrar `"oma"` de `vars` en `gen_2` mientras seguía referenciado como `@oma@` en `H2` y `SOL2`), forzando una segunda corrida fallida de 300 semillas de SymPy (`62.00 s`) y un tercer ciclo de compilación (`47.00 s`).

---

## 4. Auditoría del Orquestador (`frictions`), `Stage 3B` (Repairs), `Stage 5` (Blind Judges & LQAS), Barreras N/N y Cobertura de `traceback_deepdive`

### 4.1. `orchestrator_audit.frictions` y Eliminación del Doble `dispatch-repair`

1. **Métricas de Fricción en [`telemetry.json`](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/c2c_audits/20261122_160000_solow_m20_v11_dc8545ff/telemetry.json):**
   - `hook_denials_count`: **`0`**
   - `malformed_tool_calls_count`: **`0`**
   - `run_workflow_count`: **`4`** (`task-19`, `task-23`, `task-27`, `task-33`)
   - `legacy_invoke_subagent_count`: **`0`** | `legacy_manage_kill_count`: **`0`** | `is_hybrid_workflow_fallback`: **`false`**
   - `interventions_count` (Supervisor Manual Edits): **`0`**
2. **Confirmación de Eliminación del Doble `dispatch-repair`:**
   - En corridas anteriores, el Director ejecutaba manualmente `dispatch.py dispatch-repair` por CLI antes de invocar el workflow `repair_and_rejudge`, provocando un doble despacho redundante.
   - En `solow_m20_v11`, la inspección de los `17` turnos del Director ([transcript.jsonl](file:///C:/Users/augus/.gemini/antigravity/brain/dc8545ff-fd7d-4e36-8545-6411880c0eb2/.system_generated/logs/transcript.jsonl)) y de [`tasks/task-23.log`](file:///C:/Users/augus/.gemini/antigravity/brain/dc8545ff-fd7d-4e36-8545-6411880c0eb2/.system_generated/tasks/task-23.log), [`task-27.log`](file:///C:/Users/augus/.gemini/antigravity/brain/dc8545ff-fd7d-4e36-8545-6411880c0eb2/.system_generated/tasks/task-27.log) y [`task-33.log`](file:///C:/Users/augus/.gemini/antigravity/brain/dc8545ff-fd7d-4e36-8545-6411880c0eb2/.system_generated/tasks/task-33.log) demuestra que **el Director NUNCA invocó `dispatch-repair` manualmente**. Sus únicas 4 llamadas a `run_command` fueron: (1) `prepare`, (2) `bootstrap`, (3) `certify` y (4) limpieza final. Cada ciclo `repair_and_rejudge` de `c2c_wave_workflow.py` ejecutó exactamente **1 vez** `repair-matrix` seguido de **1 vez** `dispatch-repair`. **El antipatrón de doble `dispatch-repair` ha desaparecido al 100.00%**.

---

### 4.2. Arbitraje de Blind Judges (`Stage 5`), Confirmación LQAS (`Stage 5B`) y Bucle de Reparación (`Stage 3B`)

La reconstrucción forense cruzando [`judge_report_baseline.json`](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/solow_m20_v11/work/judge_report_baseline.json), [`judge_report_lqas.json`](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/solow_m20_v11/work/judge_report_lqas.json), [`judge_report_rejudge.json`](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/solow_m20_v11/work/judge_report_rejudge.json) y los logs de workflow revela la trazabilidad exacta de extremo a extremo:

#### A. Ronda 1 de Blind Judges (`Stage 5` en `task-19.log` — 9 Jueces, 155 Reactivos)
- **Discrepancias Epistémicas Directas (`round_1_flaw_detected_count` / `round_1_discrepancies_count`):** **`5` discrepancias** (`status: "flaw_detected"` emitidas por los jueces ciegos) distribuidas en **4 competencias** (`failed_shards`: `["C-01", "C-03", "C-05", "Hab-07"]`):
  1. `C-01` (`T-C01-05_judge_1`, `shard_10`): Enunciado revelaba literalmente el contraejemplo testigo (`L=9, K=54`) en un ítem `adversarial_break`.
  2. `C-03` (`T-C03-01_judge_1` y `T-C03-03_judge_1`, `shard_12` — **2 ítems**): El punto de equilibrio resultante `(100, 10)` / `(100, 20)` excedía el dominio `x_range: [0, 90]` de `invariant_canvas`.
  3. `C-05` (`T-C05-04_judge_1`, `shard_14`): Redondeo de `s = round(n * k / a_coef, 2)` (`0.04` en vez de `0.045`) hacía que `r*` fuera `64/9` en lugar de `9`.
  4. `Hab-07` (`T-Hab07-08_judge_1`, `shard_07`): Error matemático en la tasa asintótica de $Y$ y $K/Y$ bajo progreso técnico neutral Cobb-Douglas.
- **Overrides de Prueba Constructiva (`round_1_kernel_override_count`):** **`6` ítems** (`single_seed_override_templates`: `["T-C03-02", "T-C10-06", "T-C11-02", "T-Hab02-07", "T-Hab07-05", "T-Hab07-06"]`), donde el juez no reportó `flaw_detected` pero su respuesta numérica/estructural difirió de la clave verificada por el kernel en una semilla única.

#### B. Confirmación Adaptativa LQAS de Dos Etapas (`Stage 5B` en `task-19.log` — 1 Juez, 12 Reactivos)
- Para evitar falsos positivos de override del kernel, `stage lqas-rejudge` instanció **2 nuevas semillas independientes por cada una de las 6 plantillas con override** (`6 × 2 = 12` reactivos) y despachó a [`Blind Judge 01 (32d0c320)`](conversation://32d0c320-1542-4a76-afb0-a946c747f82d).
- **Resultado en [`judge_report_lqas.json`](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/solow_m20_v11/work/judge_report_lqas.json):** `agreement_rate: 0.50` (`6/12` acordados):
  - **Confirmadas por LQAS (`lqas_confirmed_templates`, 2 plantillas):** `["T-C11-02", "T-Hab02-07"]` (error aritmético aislado del juez en Ronda 1; plantillas sanas, se descarta reparación de `C-11` y `Hab-02`).
  - **Rechazadas por LQAS (`lqas_rejected_templates`, 4 plantillas en 3 competencias):** `["T-C03-02", "T-C10-06", "T-Hab07-05", "T-Hab07-06"]` (desacuerdo sistemático en `C-03`, `C-10` y `Hab-07`).
- **Unión en `repair-matrix`:** Las 4 competencias con `flaw_detected` (`C-01, C-03, C-05, Hab-07`) $\cup$ las 3 competencias rechazadas por LQAS (`C-03, C-10, Hab-07`) produjeron las **5 competencias de la Ronda 1 de Reparación:** `C-01, C-03, C-05, C-10, Hab-07`.

#### C. Desglose Cronológico de `Stage 3B` (3 Rondas, 7 Repair Engineers) y Re-arbitraje Quirúrgico

| Ronda Repair | Task Workflow | Competencias Reparadas | Subagentes Repair Engineers (`Stage 3B`) | Subagentes Surgical Rejudge (`Stage 5`) | Resultado de la Ronda |
| :---: | :---: | :---: | :--- | :--- | :--- |
| **Ronda 1** | [`task-23.log`](file:///C:/Users/augus/.gemini/antigravity/brain/dc8545ff-fd7d-4e36-8545-6411880c0eb2/.system_generated/tasks/task-23.log) (`20:46:31Z – 20:50:42Z`) | `C-01, C-03, C-05, C-10, Hab-07` (`5` shards) | • [`Repair C-01 (6f7c1ed7)`](conversation://6f7c1ed7-2ba1-4118-a41b-14f2c3a609fd) (`35.00 s`, 1 comp)<br>• [`Repair C-03 (266952a8)`](conversation://266952a8-ddad-4b10-b3c6-25559cb1ccad) (`49.00 s`, 1 comp)<br>• [`Repair C-05 (42107d15)`](conversation://42107d15-8a9b-4477-b6c7-e230ac3ddb82) (`40.00 s`, 1 comp)<br>• [`Repair C-10 (f3a7e154)`](conversation://f3a7e154-ee0f-40fd-a02e-0ac60d397019) (`34.00 s`, 1 comp)<br>• [`Repair Hab-07 (3ed271f7)`](conversation://3ed271f7-d598-444e-89e4-638b525b3ce8) (`156.00 s`, 2 comps: falló intento #1 por `[TPL-DYNAMIC-RATIONALE]`, `[TPL-STATIC-OPT]` y `[TPL-D3]`, aprobó en intento #2) | 5 Jueces (`4bda281b`, `f19dcbd0`, `5c1a0d87`, `f7b2b56d`, `1533d9d8`) | **`4/5` competencias aprobadas (`C-01, C-03, C-10, Hab-07`)**. En `C-05`, el juez detectó un nuevo flaw en `T-C05-02_judge_2` (*no se especificaba la forma funcional $F(r,1)=\sqrt{r}$ para hallar $s$*). |
| **Ronda 2** | [`task-27.log`](file:///C:/Users/augus/.gemini/antigravity/brain/dc8545ff-fd7d-4e36-8545-6411880c0eb2/.system_generated/tasks/task-27.log) (`20:50:46Z – 20:52:27Z`) | `C-05` (`shard_14`) | • [`Repair C-05 (d0656984)`](conversation://d0656984-1d0f-4e11-b9d2-706769fce0bc) (`36.00 s`, 1 comp: agregó $F(r,1)=\sqrt{r}$ al stem `S2` de `T-C05-02`) | 3 intentos de `Blind Judge 01` (`d7b16ccc`, `9260bccf`, `dda2d082`) | **Abortado por Cuota API (`HTTP 429 RESOURCE_EXHAUSTED`)** en la fase `Atomic Surgical Rejudge Wave` tras 3 intentos de `Blind Judge 01`. |
| **Ronda 3** | [`task-33.log`](file:///C:/Users/augus/.gemini/antigravity/brain/dc8545ff-fd7d-4e36-8545-6411880c0eb2/.system_generated/tasks/task-33.log) (`20:54:17Z – 20:56:17Z`) | `C-05` (`shard_14`) | • [`Repair C-05 (55816fa1)`](conversation://55816fa1-79e4-4fa2-9baf-50d42ebb169b) (`50.00 s`, 1 comp: explicitó la etiqueta `$s\sqrt{r}$` también en `interactive_curves` de `T-C05-02`) | 1 Juez: [`Blind Judge 01 (05d59915)`](conversation://05d59915-7c05-4f1c-8f6f-1d83bc6bf7a9) (`31.00 s`, 15 ítems) | **`100.00%` APROBADO (`15/15` en `judge_report_rejudge.json`, `155/155` global en `judge_report.json`, `repair_matrix.json` = `CLEAN`)**. |

---

### 4.3. Auditoría de Barreras Deterministas N/N en `tasks/task-*.log`

Se verificaron todas las olas `parallel(...)` ejecutadas por `c2c_wave_workflow.py` en los logs de tareas del Director:

| Task Log del Orquestador | Fase / Wave (`[phase]`) | Workers Lanzados (`Launching N`) | Barrera Completada (`Completed N/N`) | Estado de Barrera |
| :--- | :--- | :---: | :---: | :--- |
| [`tasks/task-19.log`](file:///C:/Users/augus/.gemini/antigravity/brain/dc8545ff-fd7d-4e36-8545-6411880c0eb2/.system_generated/tasks/task-19.log#L3-L5) | `Stage 1B: CTA Architects Wave` | `3` | `Completed 3/3 workers` | ✅ Barrera 3/3 limpia |
| [`tasks/task-19.log`](file:///C:/Users/augus/.gemini/antigravity/brain/dc8545ff-fd7d-4e36-8545-6411880c0eb2/.system_generated/tasks/task-19.log#L10-L12) | `Stage 1B: CTA Harmonizer` | `1` | `Completed 1/1 workers` | ✅ Barrera 1/1 limpia |
| [`tasks/task-19.log`](file:///C:/Users/augus/.gemini/antigravity/brain/dc8545ff-fd7d-4e36-8545-6411880c0eb2/.system_generated/tasks/task-19.log#L19-L21) | `Stage 3: Shard Authors Wave` | `20` | `Completed 20/20 workers` | ✅ Barrera 20/20 limpia |
| [`tasks/task-19.log`](file:///C:/Users/augus/.gemini/antigravity/brain/dc8545ff-fd7d-4e36-8545-6411880c0eb2/.system_generated/tasks/task-19.log#L47-L49) | `Stage 5: Blind Judges Wave` | `9` | `Completed 9/9 workers` | ✅ Barrera 9/9 limpia |
| [`tasks/task-19.log`](file:///C:/Users/augus/.gemini/antigravity/brain/dc8545ff-fd7d-4e36-8545-6411880c0eb2/.system_generated/tasks/task-19.log#L62-L64) | `Stage 5B: Adaptive LQAS Confirmation Wave` | `1` | `Completed 1/1 workers` | ✅ Barrera 1/1 limpia |
| [`tasks/task-23.log`](file:///C:/Users/augus/.gemini/antigravity/brain/dc8545ff-fd7d-4e36-8545-6411880c0eb2/.system_generated/tasks/task-23.log#L5-L7) | `Atomic Repair Wave` (Ronda 1) | `5` | `Completed 5/5 workers` | ✅ Barrera 5/5 limpia |
| [`tasks/task-23.log`](file:///C:/Users/augus/.gemini/antigravity/brain/dc8545ff-fd7d-4e36-8545-6411880c0eb2/.system_generated/tasks/task-23.log#L16-L18) | `Atomic Surgical Rejudge Wave` (Ronda 1) | `5` | `Completed 5/5 workers` | ✅ Barrera 5/5 limpia |
| [`tasks/task-27.log`](file:///C:/Users/augus/.gemini/antigravity/brain/dc8545ff-fd7d-4e36-8545-6411880c0eb2/.system_generated/tasks/task-27.log#L5-L7) | `Atomic Repair Wave` (Ronda 2) | `1` | `Completed 1/1 workers` | ✅ Barrera 1/1 limpia |
| [`tasks/task-27.log`](file:///C:/Users/augus/.gemini/antigravity/brain/dc8545ff-fd7d-4e36-8545-6411880c0eb2/.system_generated/tasks/task-27.log#L12-L19) | `Atomic Surgical Rejudge Wave` (Ronda 2) | `1` | `0/1` (`[WORKER-EXHAUSTED]` tras 3 intentos `HTTP 429`) | ⚠️ Interrupción por cuota API (`code 429`) |
| [`tasks/task-33.log`](file:///C:/Users/augus/.gemini/antigravity/brain/dc8545ff-fd7d-4e36-8545-6411880c0eb2/.system_generated/tasks/task-33.log#L5-L7) | `Atomic Repair Wave` (Ronda 3) | `1` | `Completed 1/1 workers` | ✅ Barrera 1/1 limpia |
| [`tasks/task-33.log`](file:///C:/Users/augus/.gemini/antigravity/brain/dc8545ff-fd7d-4e36-8545-6411880c0eb2/.system_generated/tasks/task-33.log#L12-L14) | `Atomic Surgical Rejudge Wave` (Ronda 3) | `1` | `Completed 1/1 workers` | ✅ Barrera 1/1 limpia |

> [!NOTE]
> **Observación sobre `Judge 01 (05d59915)` en `task-33.log`:** En total se registraron `19` subagentes `c2c_judge` en los logs de workflow (`9` en Stage 5 + `1` en Stage 5B LQAS + `5` en Rejudge Ronda 1 + `3` intentos fallidos por 429 en Rejudge Ronda 2 + `1` en Rejudge Ronda 3). Como `task-33` finalizó con éxito (`finished with result`), su `SYSTEM_MESSAGE` en el Paso 35 del Director truncó la última línea del log en el preview y `discover_all_subagents` (que además leyó el snapshot pre-certify) listó 19 entradas de jueces donde la primera entrada (`Judge 01` sin sufijo en la tabla de `traceback_deepdive_dc8545ff.md`) corresponde a `05d59915-7c05-4f1c-8f6f-1d83bc6bf7a9` (`31.00 s`, 3 turnos).

---

### 4.4. Validación de Cobertura 100% de Fallos Reales en `traceback_deepdive_dc8545ff`

Se contrastaron las **`20` incidencias** catalogadas en [`traceback_deepdive_dc8545ff.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/c2c_audits/20261122_160000_solow_m20_v11_dc8545ff/traceback_deepdive_dc8545ff.md#L171-L184) y [`traceback_deepdive_dc8545ff.json`](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/c2c_audits/20261122_160000_solow_m20_v11_dc8545ff/traceback_deepdive_dc8545ff.json) contra la totalidad de eventos en los `50` transcripts de subagentes:

1. **Captura del 100.00% de Fallos de Herramientas y Compilación de Subagentes (`20/20`):**
   - **1 fallo de `read_file` (`FileNotFoundError`) en Stage 1B:** [`CTA Architect part_01 (6a162dc1)`](conversation://6a162dc1-4b20-416c-a423-efe83bb031c2) en el Paso 1 intentó adivinar el nombre del PDF como `05_15_07_El_modelo_de_Solow.pdf` (omitiendo `_crecimiento_`), a pesar de que su prompt `[SCOPE-LOCK]` especificaba explícitamente `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf`. Se recuperó inmediatamente en el Paso 3 (`+3.00 s`).
   - **18 fallos de compilación en Stage 3 (17 shards × 1 fallo + `shard_02` × 2 fallos = 18):**
     - **12 fallos asíncronos vía `SYSTEM_MESSAGE`** (cuando `compile_shard.py` superó los `10.00 s` de `WaitMsBeforeAsync` y pasó a background task: `shard_02` [pasos 8 y 18], `shard_05` [paso 8], `shard_06` [paso 8], `shard_07` [paso 8], `shard_08` [paso 8], `shard_13` [paso 11], `shard_14` [paso 8], `shard_15` [paso 8], `shard_16` [paso 8], `shard_17` [paso 8], `shard_18` [paso 8]). **Todos (`12/12`, `100.00%`) fueron capturados y clasificados por `traceback_analyzer.py`**.
     - **6 fallos síncronos vía `GENERIC`** (cuando `compile_shard.py` falló en `< 10.00 s`: `shard_09, 10, 11, 12, 19, 20` [paso 6]). **Todos (`6/6`, `100.00%`) fueron capturados**.
   - **1 fallo de compilación en Stage 3B:** [`Repair Engineer Hab-07 (3ed271f7)`](conversation://3ed271f7-d598-444e-89e4-638b525b3ce8) en el Paso 15 (síncrono, capturado con su traza de `thinking` previa).
2. **Sanitización Automática `[CTA-KATEX]` (`0` fallos bloqueantes):**
   - Gracias al sanitizador determinista en `compile_cta.py` ([cta_sanitizer_log.json](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/solow_m20_v11/work/telemetry/cta_sanitizer_log.json)), se evaluaron `1,177` campos en las `21` competencias preliminares y se aplicaron **`4` parches automáticos** (`2` en `part_02` y `2` en `part_03`), logrando **`0` errores `[CTA-KATEX]`** en Stage 1B.
3. **Hallazgo Forense Adicional en Nivel Orquestador (`SYSTEM_MESSAGE` de `run_workflow`):**
   - Mientras que los `20` errores a nivel de subagentes fueron capturados al `100.00%`, a nivel del **Orquestador** (`orchestrator_audit.metrics.tool_errors_count = 0`) hubo **3 tareas de `run_workflow` que finalizaron con excepción asíncrona vía `SYSTEM_MESSAGE`** en el transcript del Director ([Steps 21, 25 y 29](file:///C:/Users/augus/.gemini/antigravity/brain/dc8545ff-fd7d-4e36-8545-6411880c0eb2/.system_generated/logs/transcript.jsonl)):
     - **Step 21 (`task-19`) y Step 25 (`task-23`):** Excepción esperada de parada de compuerta (`RuntimeError: CLI command failed (C2C stage gates) with exit code 1`) cuando `gates` puebla `repair_matrix.json` para activar `repair_and_rejudge`.
     - **Step 29 (`task-27`):** Fallo transitorio de cuota de infraestructura (`WorkflowError: RESOURCE_EXHAUSTED (code 429): Individual quota reached`) durante la ola `Atomic Surgical Rejudge Wave`, en la cual [`Blind Judge 01 (d7b16ccc)`](conversation://d7b16ccc-8da9-438c-a144-c98586d764ee) colapsó en su Turno 2 tras `26.00 s` y sus 2 reintentos automáticos ([`9260bccf`](conversation://9260bccf-176b-4f6a-80a6-838ba3d9b92e) y [`dda2d082`](conversation://dda2d082-882a-4052-962c-58aa1a186903)) abortaron en Turno 0 (`0.00 s`). Tras reanudación con `max_concurrency=4` en `task-33`, la corrida concluyó exitosamente.

---

## 5. Recomendaciones Accionables de Ingeniería (Post-v11)

1. **Pre-Check Estático de Paridad `vars` $\leftrightarrow$ Tokens `@var@` antes del Dry-Run de 50/300 Semillas (`compile_shard.py`):**
   - **Problema:** Cuando un autor o repair engineer olvida u omite una clave en el diccionario `vars` retornado por `gen_k(rng)` (como ocurrió en el intento #2 de `shard_02` al borrar `"oma": oma` mientras `H2` y `SOL2` usaban `@oma@`), el validador ejecuta igualmente las 50 semillas de `[INVARIANT]` y los 300 intentos de `[TPL-VAR]` con SymPy, desperdiciando `~60.00 s` de CPU para reportar un error que es detectable en `< 5.00 ms` en la primera semilla (`seed=100`).
   - **Acción:** Cortocircuitar (`fail-fast`) el dry-run de `[TPL-VAR]` si la semilla `seed=100` lanza `Unresolved PrairieLearn template token '@...@'`. Esto habría reducido el tiempo de `shard_02` en `~55.00 s`.
2. **Desempaquetar `[GENERAL: VALIDATION_ERROR]` en `audit_engine.py` (`_extract_compile_rules`):**
   - **Problema:** Cuando `compile_shard.py` formatea errores de `check_templates.py` bajo el encabezado `[-] [GENERAL: VALIDATION_ERROR]` con `• [GENERAL] ... -> Causa: FAIL: [TPL-CONST-DISTRACTOR]`, `first_compile_top_rules` contabiliza tanto `GENERAL (6)` como la sub-regla `TPL-CONST-DISTRACTOR (5)`.
   - **Acción:** En `_extract_compile_rules`, excluir el tag genérico `GENERAL` cuando la misma línea `Causa:` contenga un tag específico `[TPL-*]` o `[R-*]`, y filtrar los tags de la sección `[PRECHECK]` que son sólo advertencias cuando la compilación sea `PASS`.
3. **Captura de `RESOURCE_EXHAUSTED (code 429)` desde `task-*.log` del Orquestador en `traceback_analyzer.py`:**
   - **Problema:** Cuando un subagente lanzado dentro de `c2c_wave_workflow.py` falla por `HTTP 429 RESOURCE_EXHAUSTED` durante la generación del stream LLM, la excepción queda registrada en `tasks/task-N.log` (`[AUTO-RETRY]` / `[WORKER-EXHAUSTED]`) y en el `SYSTEM_MESSAGE` del Orquestador, pero no escribe un evento de error dentro del `transcript.jsonl` del subagente colapsado (`d7b16ccc`, `9260bccf`, `dda2d082`).
   - **Acción:** Hacer que `traceback_analyzer.py` inspeccione también los bloques `failed with result: ... RESOURCE_EXHAUSTED (code 429)` en los `SYSTEM_MESSAGE` del Orquestador para clasificarlos automáticamente bajo la categoría `Transient Stream / API Quota Interruption (HTTP 429)`.
