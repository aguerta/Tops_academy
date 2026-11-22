# Informe Forense Enriquecido ("No Headless" / Modo Agéntico)
## Ejecución Content-to-Course: `solow_m20_v8` (`15fa3433-bf3b-4618-a7e2-9edc177912c5`)

**Fecha de Auditoría Forense:** `2026-11-22 20:03:45 UTC`  
**Conversación Orquestadora:** [`15fa3433-bf3b-4618-a7e2-9edc177912c5`](conversation://15fa3433-bf3b-4618-a7e2-9edc177912c5)  
**Curso / Work Dir:** `solow_m20_v8` (`D:\Augusto\personal_portfolio\Tops_academy\courses\solow_m20_v8\work`)  
**Estado Final del Pipeline:** `completed` (`549` preguntas publicadas en `courses/solow_m20_v8.json`, `1.87 MB`, `19.90/20.00` QA Score, `MPRI = 99.65/100.00`, `100.00%` acuerdo post-rejudge)  
**Costo Total / Tiempo de Pared:** **`$8.77 USD`** (Gemini 4 Hydrogen) | **`18.47 min`** (`1,108.00 s`) | `41` subagentes (`4.42x` aceleración paralela)

---

## 1. Verificación de Aislamiento Estricto de `conversation_id`

Se auditó la integridad y el aislamiento zero-collision en `work/state.json`, `work/telemetry/*.json` y `work/telemetry/by_conversation/`:

| Artefacto / Ruta | `conversation_id` Registrado | Estado de Aislamiento | Evidencia |
| :--- | :--- | :---: | :--- |
| `work/state.json` | `15fa3433-bf3b-4618-a7e2-9edc177912c5` | ✅ **Válido** | `status="completed"`, `last_stage="06_publish"`, `artifact_counts.questions_built=549` |
| `work/telemetry/00_prepare.json` .. `06_publish.json` (`9` snapshots) | `15fa3433-bf3b-4618-a7e2-9edc177912c5` | ✅ **9/9 Válidos** | Todos los snapshots de etapa coinciden 100.00% con el director |
| `work/telemetry/by_conversation/15fa3433-bf3b-4618-a7e2-9edc177912c5/` | `15fa3433-bf3b-4618-a7e2-9edc177912c5` | ✅ **10/10 Válidos** | Incluye `state.json` y los `9` snapshots de etapa particionados |
| `work/telemetry/cta_sanitizer_*.json` (`4` logs) | `N/A` (`course_id="solow_m20_v8"`) | ✅ **Limpio** | Logs del sanitizador de CTA sin colisión de otro `conversation_id` |
| `telemetry.json -> workload.work_dir_conversation_match` | `true` | ✅ **Zero-Collision** | Verificado contra el directorio resuelto |

> [!NOTE]
> **Observación de Telemetría v3.2:** Aunque los `9` snapshots de etapa en `work/telemetry/` registran correctamente `conversation_id`, duración y `metadata`, los campos `stage_tokens` y `subagents_count` en `state.json` y en los snapshots aparecen en `0` porque el conteo real de tokens y subagentes proviene del parser de `transcript.jsonl` / `transcript_full.jsonl` ejecutado por `audit_engine.py`.

---

## 2. Evaluación de Impacto Real de las 6 Mejoras FTP (First-Time Pass)

### 2.1. Resumen Cuantitativo de Adopción y Compilación

| Dimensión FTP | Métrica Observada | Diagnóstico Forense |
| :--- | :--- | :--- |
| **`first_compile_pass_rate`** | **`2/18 (11.11%)`** | `shard_11` (`105.00s`) y `shard_15` (`91.00s`) compilaron limpio en el intento 1. `15/18` (`83.33%`) pasaron en el intento 2; `1/18` (`shard_13`, `5.56%`) requirió 3 intentos. |
| **Adopción de `c2c_ver.*`** | **`18/18 (100.00%)`** | `c2c_ver.m20_guard`: `18/18` (`100.00%`); `c2c_ver.equiv`: `9/18` (`50.00%`); `c2c_ver.numeric`: `6/18` (`33.33%`). Cero funciones de verificación ad-hoc inseguras. |
| **Esqueleto en `author_XX_data.md`** | **`18/18 (100.00%)`** | Todos los briefs (`work/dispatch/items/author_01_data.md`..`author_18_data.md`) inyectaron el esqueleto Python (`RATS`, `gen_k`, `ver_k`, firmas `c2c_ver.*`), eliminando errores estructurales de contrato Form-C. |
| **`INFO: [AUTO-FIXED]` (No bloqueante)** | **`23` ocurrencias** | 100.00% correspondieron a `[TPL-ORPHAN-VARS]` (poda automática de variables auxiliares no referenciadas en `vars`, ej. `q_sn`, `v0`, `y_rate`, `phi0`, `rho`, `sK`). |
| **`WARNING:` (No bloqueante)** | **`34` ocurrencias** | `[BLOOM-SUPERIOR-TARGET]`: `24`; `[TPL-STEM-SYMBOL-PARITY]`: `5`; `[TPL-UNBOUNDED-LOOP]`: `4`; `[TPL-STEM-VARIANT-PARITY]`: `1`. No abortaron compilación. |
| **Straggler Crítico (`shard_01`)** | **`226.00s` (`+84.00s` vs mediana `142.00s`)** | `112.00s` pre-1er-compile (`109.00s` en `write_file` con `25,124` tokens de salida) + `114.00s` post-1er-compile (`9` llamadas `edit_file` + 2da compilación). |

### 2.2. Análisis Profundo: ¿Por qué `first_compile_pass_rate` fue `11.11%` pese a `100.00%` de adopción?

La inspección directa de los transcripts crudos de los `18` `Shard Author` revela que **los errores sintácticos y estructurales desaparecieron**, pero el cuello de botella en 1ra compilación se desplazó hacia **reglas semánticas y psicométricas estrictas**:

1. **`[EPISTEMIC-CLOSURE-WARNING]` (presente en `14/18` shards, `77.78%`):** Símbolos en la solución o `error_rationale` no declarados explícitamente en el `stem` (ej. `a`, `r`, `L`, `L_0` en `shard_01`).
2. **`[TPL-VAR]` (`9/18` shards, `50.00%`) y `[TPL-STATIC-OPT]` (`6/18` shards, `33.33%`):** Varianza insuficiente de parámetros o distractores con opciones colapsadas/estáticas.
3. **`[TPL-STEM-VARIANT-PARITY]` (`6/18` shards, `33.33%`):** Omisión de placeholders `@var@` en alguna variante de `stem_variants`.
4. **`[R-19]` (`5/18` shards, `27.78%`):** Paridad psicométrica anti-giveaway en distractores.

> [!IMPORTANT]
> El impacto positivo de `c2c_ver.*`, del esqueleto en `author_XX_data.md` y del auto-fix de `[TPL-ORPHAN-VARS]` se refleja en que **ningún shard necesitó reescritura completa (`0` fallos de contrato Form-C)** y **17/18 (`94.44%`) cerraron en <= 2 compilaciones** con `0` intervenciones manuales del orquestador.

### 2.3. Descomposición Forense de `shard_01` (`226.00s` — `Hab-02`)

La traza exacta de `Shard Author shard_01` (`862fbb16-6fcf-4e88-b76e-a37244f6cf18`) explica el `100.00%` de su latencia:
- **Fase Pre-Compilación (`112.00s`):**
  - `19:45:49Z` (`Step 1`): `read_file` de `author_01_data.md` (`23,034` tokens entrada).
  - `19:45:52Z -> 19:47:41Z` (`Step 3`): `write_file` de `shard_01_data.py` consumió **`109.00s`** generando **`25,124` tokens de salida** (la competencia `Hab-02` es de tipo `Skill` con `4` arquetipos y `3` bandas de dificultad).
- **1ra Compilación (`19:47:41Z -> 19:48:15Z`, `34.00s`):**
  - `compile_shard.py` pasó a tarea en segundo plano (`task-6`). Auto-corrigió `[TPL-ORPHAN-VARS]` en `T-Hab02-03` (`INFO: [AUTO-FIXED]`), pero falló (`exit code 1`) por `4/5` errores en `T-Hab02-05` (`[TPL-STEM-VARIANT-PARITY]`, `[TPL-DYNAMIC-RATIONALE]` en `D-Hab02-10`) y `T-Hab02-07` (`[INVARIANT]` error KaTeX de doble subíndice: `1-\alpha=@one_m_^al@`).
- **Fase Post-Compilación (`114.00s`):**
  - `19:48:15Z -> 19:49:03Z` (`Step 9`): El agente ejecutó **`9` llamadas `edit_file`** (`7,788` tokens salida, `48.00s`).
  - `19:49:03Z -> 19:49:30Z` (`Step 19..23`): 2da compilación (`task-20`) exitosa y `finish`.

---

## 3. Validación de Fricciones del Orquestador, Reparaciones, Blind Judges y `c2c_wave_workflow.py`

### 3.1. `orchestrator_audit.frictions` y Desempeño del Director

Los contadores deterministas en `telemetry.json -> orchestrator_audit.frictions` fueron verificados contra `15fa3433.../.system_generated/logs/transcript_full.jsonl`:
- **`hook_denials_count`:** `0`
- **`malformed_tool_calls_count`:** `0`
- **`run_workflow_count`:** `3` (`Step 18`: `full_pipeline`; `Step 24`: `repair_and_rejudge` Ronda 1; `Step 30`: `repair_and_rejudge` Ronda 2)
- **`legacy_invoke_subagent_count` / `legacy_manage_kill_count`:** `0` (`is_hybrid_workflow_fallback = false`)
- **`interventions_count` (Supervisor Repair):** `0` (`0.00s` de edición manual)
- **Descomposición de pared (`1,108.00s` / `18.47 min`):** `881.00s` (`79.51%`) en espera de barreras de subagentes, `60.00s` (`5.42%`) en inferencia/thinking del director, `49.00s` (`4.42%`) en comandos CLI locales.

### 3.2. Blind Judges, `round_1_flaw_detected_count` vs `round_1_kernel_override_count` y `repair_rounds`

La reconciliación entre `judge-compare.log`, `judge_report_baseline.json`, `judge_report_lqas.json`, `lqas-compare.log` y `rejudge-compare.log` aclara exactamente la mecánica de arbitraje y las `2` rondas de reparación:

1. **Ronda 1 de Blind Judges (`9` jueces, `151` reactivos evaluados):**
   - `judge-compare.log` reportó **`97.90%` de acuerdo (`140/143`)** con **`3` discrepancias (`round_1_flaw_detected_count = 3`)**: `T-C03-08_judge_1` (`C-03`), `T-Hab08-09_judge_1` (`Hab-08`) y `T-H01-07_judge_1` (`H-01`).
   - Simultáneamente, `judge_report_baseline.json` registró **`round_1_kernel_override_count = 4`**, todos en **`Hab-08`**: `T-Hab08-02_judge_1`, `T-Hab08-03_judge_1`, `T-Hab08-07_judge_1` y `T-Hab08-08_judge_1`.
   - Esos `4` overrides dispararon la ola adaptativa **Stage 5B LQAS** (`1` juez, `8` reactivos), donde `lqas-compare.log` registró **`0.00%` de acuerdo (`0/8`)** y rechazó las `4` plantillas (`rejected=['T-Hab08-02', 'T-Hab08-03', 'T-Hab08-07', 'T-Hab08-08']`).
2. **Repair Ronda 1 (`spawn_step = 25`, `3` workers):**
   - `Repair Engineer C-03` (`f75bb1`, `36.00s`), `Repair Engineer H-01` (`1c1d5c`, `34.00s`) y `Repair Engineer Hab-08` (`d42a2f`, `103.00s`, `7` edits).
   - Tras el rejudge quirúrgico (`3` jueces), `C-03` y `H-01` aprobaron limpio, pero `Hab-08` presentó una discrepancia residual en `T-Hab08-05` (`S5`), haciendo fallar `gates` en `task-25`.
3. **Repair Ronda 2 (`spawn_step = 33`, `1` worker):**
   - `Repair Engineer Hab-08` (`15a4b5`, `39.00s`, `1` edit sobre `S5` de `T-Hab08-05`).
   - El rejudge quirúrgico final (`2` jueces, `18` ítems evaluados, `kappa = 1.00`) aprobó `Hab-08` (`100.00%` acuerdo, `0` discrepancias), cerrando `repair_matrix.json` en `CLEAN`.

### 3.3. Comportamiento de `c2c_wave_workflow.py` (Barreras N/N, Fallos CLI/Infra, Stragglers)

La auditoría de `task-19.log`, `task-25.log` y `task-31.log` confirma **estabilidad total de infraestructura** (`0` fallos de red/CLI/timeout, `0` reintentos consumidos de `max_retries=2`, `max_concurrency=12`):
- **Barreras N/N en `task-19.log` (`full_pipeline`):** CTA Architects `3/3` -> CTA Harmonizer `1/1` -> Shard Authors `18/18` -> Blind Judges `9/9` -> LQAS `1/1`. Salida controlada en `gates` (`exit code 1`) al poblar `repair_matrix.json`.
- **Barreras N/N en `task-25.log` (`repair_and_rejudge` R1):** Atomic Repair `3/3` -> Surgical Rejudge `3/3`. Salida controlada en `gates` (`exit code 1`) para `Hab-08`.
- **Barreras N/N en `task-31.log` (`repair_and_rejudge` R2):** Atomic Repair `1/1` -> Surgical Rejudge `2/2` -> `gates` aprobado.
- **Stragglers por etapa:** Stage 1B Mappers: `part_01` (`84.00s` vs `65.00s` min); Stage 3 Authors: `shard_01` (`226.00s` vs `142.00s` mediana); Stage 3B Repairs: `Hab-08` R1 (`103.00s` vs `39.00s` mediana); Stage 5 Judges: `Judge 03` / `Judge 08` (`62.00s`).

### 3.4. Causa Raíz: Errores Reales (`18` + `1`) vs Catalogados (`13`) en `traceback_deepdive_15fa3433`

Se detectó una **discrepancia de cobertura** en el analizador automático `traceback_analyzer.py` (`traceback_deepdive_15fa3433.md` / `.json`):
- **Errores reales en ejecución (`19` incidentes):**
  - **`18` errores de herramienta (`tool_errors_total = 18` en `telemetry.json`):** `1` fallo en `CTA Architect part_01` (Step 6, `[CTA-KATEX]`) + `17` fallos de `compile_shard.py` (`15` shards con `1` fallo + `shard_13` con `2` fallos).
  - **`1` truncamiento de stream del modelo:** `CTA Harmonizer` (Step 7, `Error: The stream was interrupted`), recuperado autónomamente en Step 8 generando `compile_cta.py`.
- **Por qué `traceback_deepdive_15fa3433` solo catalogó `13` errores:**
  - `traceback_analyzer.py` solo inspecciona respuestas síncronas de `run_command`. En **`6` shards (`shard_01`, `shard_03`, `shard_04`, `shard_05`, `shard_06`, `shard_07`)**, `compile_shard.py` excedió el umbral síncrono y corrió como **tarea en segundo plano (`task-*.log`)**, devolviendo el resultado vía `<SYSTEM_MESSAGE>` en el turno posterior. Esos `6` fallos reales fueron omitidos por el deep-dive (`18 - 6 + 1 truncamiento = 13`), lo que también explica que la tabla de `traceback_deepdive_15fa3433.md` muestre erróneamente `2 (0/2)` para los shards `01..07` mientras `shard_timing_decomposition.md` y `telemetry.json` reportan correctamente `2 (1)`.
  - Adicionalmente, `traceback_analyzer.py` clasificó el `[CTA-KATEX]` de `CTA part_01` bajo la categoría `Anti-Giveaway & Psychometric Parity Violations (R-14..R-19)` por coincidencia de patrón genérico.

---

## 4. Recomendaciones Accionables

1. **Reducir fallos de 1ra compilación por `[EPISTEMIC-CLOSURE-WARNING]` (`14/18` shards):** Inyectar en el esqueleto de `author_XX_data.md` una lista explícita de `stem_symbols` requeridos por cada plantilla para que el autor declare todas las variables (`a`, `r`, `L`, `L_0`) en el `stem` antes de escribir el `error_rationale`, elevando `first_compile_pass_rate` de `11.11%` hacia `> 60.00%`.
2. **Prevenir errores KaTeX de doble subíndice (`[INVARIANT]` en `shard_01`):** Agregar una regla de pre-chequeo o ejemplo negativo en `c2c_shard_author` prohibiendo `@var@` inmediatamente precedido por `^` o `_` sin llaves (`^{@var@}` / `_{@var@}`), evitando ediciones iterativas en `Skill` shards pesados (`shard_01` consumió `9` edits y `114.00s` post-compile).
3. **Corregir `traceback_analyzer.py` para capturar errores en `background tasks`:** Parsear los `<SYSTEM_MESSAGE>` de `task-*.log` con `Command exited with code 1` para eliminar el subregistro de `6` fallos en `traceback_deepdive_*.md` y corregir la taxonomía de `[CTA-KATEX]`.
4. **Endurecer verificación de `open_symbolic` y `unstructured_model` en `Hab-08`:** Las `4` discrepancias de `kernel_override` rechazadas por LQAS ocurrieron en `Hab-08` (`T-Hab08-02`, `03`, `07`, `08`). Reforzar la validación de equivalencia simbólica y orden de fases en `c2c_ver.equiv` evitará la necesidad de `2` rondas de reparación.
