# Informe Forense Enriquecido ("No Headless" / Modo Agéntico)
## Ejecución Content-to-Course: `solow_m20_v6` (`bc7bba12-4176-4fc1-8f6e-1efba7e87b48`)

**Fecha de Auditoría Forense:** `2026-11-22 18:48 UTC`  
**Conversación Orquestadora:** `bc7bba12-4176-4fc1-8f6e-1efba7e87b48`  
**Directorio de Trabajo (`work/`):** `D:\Augusto\personal_portfolio\Tops_academy\courses\solow_m20_v6\work`  
**Artefactos Base Preservados:** `report.md`, `telemetry.json`, `traceback_deepdive_bc7bba12.md`, `traceback_deepdive_bc7bba12.json`, `shard_timing_profile.json`, `shard_timing_decomposition.md`

---

## 1. Verificación de Aislamiento Estricto (`conversation_id`)

Se verificó el aislamiento determinista **Zero-Collision** en los artefactos de estado y telemetría:

| Artefacto / Directorio | `conversation_id` Registrado | Estado de Aislamiento |
| :--- | :--- | :--- |
| `work/state.json` | `bc7bba12-4176-4fc1-8f6e-1efba7e87b48` | ✅ Coincidencia estricta (`match=True`) |
| `work/telemetry/*.json` (9 snapshots v3.2: `00_prepare` .. `06_publish`) | `bc7bba12-4176-4fc1-8f6e-1efba7e87b48` | ✅ 9/9 snapshots aislados |
| `work/telemetry/by_conversation/bc7bba12-4176-4fc1-8f6e-1efba7e87b48/` | `bc7bba12-4176-4fc1-8f6e-1efba7e87b48` | ✅ 10 archivos particionados (`00_prepare`..`06_publish` + `state.json`) |
| `work/telemetry/cta_sanitizer_*.json` (4 archivos) | `course_id: solow_m20_v6` (sin `conversation_id`) | ✅ Específico del curso |

---

## 2. Resumen Ejecutivo de Métricas y Unit Economics

- **Carga de Entrada:** 2 PDFs (36 páginas, `1.49 MB`: `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` y `solow1956.pdf`), `0` páginas de visión.
- **Producción Curricular:** `19` competencias (`1` Fact, `12` Concept, `6` Skill), `10` shards, `440` preguntas validadas (`20`–`30` por competencia).
- **Calidad Pedagógica Certificada (`certify` / `task-32.log`):** `20.00 / 20.00` pts QM-OSCQR (PLATINUM MASTERY), `100.00 / 100.00` pts MPRI, `0.00` penalizaciones.
- **Tiempo y Aceleración:** `16.33 min` (`980.00 s`) de pared (`16.45 min` / `987.00 s` extremo a extremo en `traceback_deepdive`), `67.47 min` (`4048.00 s`) de cómputo de subagentes, **Speedup paralelo `4.13x`**.
- **Consumo y Costo (Gemini 4 Hydrogen):** `8,269,086` tokens totales (`2,101,780` activos: `1,504,980` In + `596,800` Out; `6,167,306` Cache Read; `66,089` Thinking en `62` turnos / `264,441` chars), costo total **`$7.20 USD`** (`$0.02 USD/preg`, `$0.38 USD/comp`, `$0.20 USD/pág`).
- **Subagentes Desplegados:** `29` subagentes (`0` Visión, `4` CTA, `10` Shard Authors, `2` Repair Engineers, `13` Blind Judges).

---

## 3. Auditoría de Orquestación, `c2c_wave_workflow.py` y Fricciones

### 3.1. Validación de `orchestrator_audit.frictions` e Intervenciones
- **Intervenciones manuales del supervisor:** `0` (`supervisor_repair_seconds = 0.00 s`, `interventions_count = 0`).
- **Fricciones registradas en `telemetry.json`:**
  - `hook_denials_count = 0`
  - `malformed_tool_calls_count = 0`
  - `legacy_invoke_subagent_count = 0`
  - `legacy_manage_kill_count = 0`
  - `is_hybrid_workflow_fallback = false`
  - `run_workflow_count = 3` (1 ejecución de `full_pipeline`, 1 de `post_cta_pipeline`, 1 de `repair_and_rejudge`).
- **Descomposición de tiempo del Orquestador:** `31.00 s` (`0.52 min`) en CLI, `759.00 s` (`12.65 min`) esperando barreras de subagentes, `63.00 s` (`1.05 min`) en inferencia/thinking.

### 3.2. Comportamiento de `c2c_wave_workflow.py` y Hallazgo de Reintento CLI
La inspección directa del transcript crudo (`bc7bba12-4176-4fc1-8f6e-1efba7e87b48/transcript_full.jsonl`) y `tasks/*.log` revela **dos fallos de `run_workflow` durante la ejecución**:
1. **`task-18` (`mode="full_pipeline"`, paso 17, `18:28:18Z` -> `18:30:25Z`):**
   - Completó las barreras N/N de Stage 1B (`3/3` CTA Architects, `1/1` CTA Harmonizer) y Stage 2 (`sharding`).
   - **Fallo CLI/Argumento:** Falló al invocar `dispatch.py dispatch-authors --work-dir ... --templates-per-modality 3` porque `dispatch.py` no soporta `--templates-per-modality`.
   - **Recuperación:** El orquestador detectó el error en el paso 21 y relanzó `task-22` (`mode="post_cta_pipeline"`, `comps_per_shard=2`, sin `templates_per_modality`).
2. **`task-22` (`mode="post_cta_pipeline"`, paso 21, `18:30:30Z` -> `18:36:43Z`):**
   - Completó las barreras N/N de Stage 3 (`10/10` Shard Authors), Stage 4 (`templates`, `build`), Stage 5 (`10/10` Blind Judges), Stage 5B (`1/1` LQAS Confirmation Judge) y Stage 6 (`gates`).
   - **Salida no-cero esperada por Gate:** `gates` devolvió código de salida distinto de cero tras detectar 2 competencias fallidas (`C-06`, `Hab-05`).
3. **`task-28` (`mode="repair_and_rejudge"`, paso 27, `18:36:57Z` -> `18:41:12Z`):**
   - Precedido por `dispatch.py dispatch-repair --ids C-06 Hab-05` (exit 0). Completó `2/2` Repair Engineers, `templates`, `build`, `2/2` Surgical Rejudges y `gates` post-reparación.
4. **`task-32` (`run.py --stage certify`, paso 31):** Completó `templates -> build -> verify -> publish` y emitió el certificado QA/Auditor.

**Conclusión sobre Barreras N/N:** Todas las barreras de sincronización (`3/3`, `1/1`, `10/10`, `10/10`, `1/1`, `2/2`, `2/2`) cerraron al 100% sin timeouts ni *straggler drops*.

---

## 4. Discrepancia Forense: 5 Errores Catalogados vs 14 `tool_errors_total`

La auditoría cruzada entre `traceback_deepdive_bc7bba12.json` (`5` errores) y `telemetry.json` (`tool_errors_total = 14`) explica exactamente la diferencia:
- **14 comandos fallidos reales (`exit code 1`) en subagentes:**
  - `CTA Harmonizer` (`aa163390`): **1** (`apply_harmonize` por solapamiento curricular entre `Hab-01` y `Hab-03`).
  - `Shard Author shard_01` (`cc2421bd`): **1** (Compilación #1: 6 errores).
  - `Shard Author shard_02` (`75af681b`): **1** (Compilación #1: 1 error `VERIFIER-TAUTOLOGY-DETECTED`).
  - `Shard Author shard_03` (`77a4a5f8`): **1** (Compilación #1: 7 errores).
  - `Shard Author shard_04` (`4498e1bf`): **1** (Compilación #1: 8 errores).
  - `Shard Author shard_05` (`0c98b05d`): **2** (Compilación #1: 10 errores; Compilación #2: 2 errores).
  - `Shard Author shard_06` (`0ea4a426`): **1** (Compilación #1: 11 errores).
  - `Shard Author shard_07` (`3306244c`): **2** (Compilación #1: 5 errores; Compilación #2: 3 errores).
  - `Shard Author shard_08` (`5d80ecc4`): **1** (Compilación #1: 3 errores).
  - `Shard Author shard_09` (`d2b29172`): **2** (Compilación #1: 18 errores; Compilación #2: 1 error `TPL-STATIC-OPT`).
  - `Repair Engineer Hab-05` (`c8dcf6d7`): **1** (Compilación #1: 5 errores).
- **Causa raíz de la sub-contabilidad en `traceback_deepdive`:** `traceback_analyzer.py` solo capturó los **5** fallos devueltos síncronamente en registros `GENERIC` (`CTA Harmonizer` cmd#1, `Shard 05` cmd#1, `Shard 08` cmd#1, `Shard 09` cmd#1 y cmd#2), omitiendo los **9** fallos de `run_command` que excedieron `WaitMsBeforeAsync` y regresaron asíncronamente como `SYSTEM_MESSAGE` (`Shard 01`, `02`, `03`, `04`, `05` cmd#2, `06`, `07` cmd#1 y cmd#2, y `Repair Hab-05` cmd#1).

---

## 5. Análisis de `first_compile_pass_rate`, Straggler (`shard_05`), `Judges: 13` y `Repairs: 2`

### 5.1. Stage 3 (`first_compile_pass_rate = 10.00%`) y Straggler `shard_05` (`258.00 s`)
- **Tasa de aprobación en 1ra compilación:** **`1/10 (10.00%)`**. Solo `Shard Author shard_10` (`C-12`, 1 competencia) pasó al primer intento en `81.00 s` (`4` turnos, `0` errores, `0` warns).
- **Straggler crítico `Shard Author shard_05` (`C-04, C-05`):** **`258.00 s`** (`+20.00 s` sobre la mediana de `238.00 s`; `107.00 s` Pre-1st-Compile + `151.00 s` Post-1st-Compile, `11` turnos, `89,786` In / `48,008` Out / `601,049` Cache).
  - **Causa raíz:** Requirió **3 compilaciones** (2 fallos bloqueantes):
    - *Compilación #1 (`exit=1`):* 10 errores consolidados (`[TPL-STEM-GRAMMAR]` en `C-04`, 3x `[VERIFIER-TAUTOLOGY-DETECTED]` en `C-04`, 4x `[TPL-DRY]` en `C-04`/`C-05`, 2x `[TPL-VAR]` en `C-04`/`C-05`).
    - *Compilación #2 (`exit=1`):* 2 errores residuales en `C-05` (`[R-15-MS]` y `[TPL-VAR]`).
    - *Compilación #3 (`exit=0`):* Aprobada tras edición en `shard_05_data.py`.

### 5.2. Stage 5 (`Judges: 13`), `round_1_flaw_detected_count` vs `round_1_kernel_override_count` y Stage 3B (`Repairs: 2`)
Se validó la consistencia exacta entre `telemetry.json`, `judge_report_baseline.json`, `judge_report_lqas.json`, `judge_report_rejudge.json` y las órdenes de reparación (`repair_c06_data.md`, `repair_hab05_data.md`):

- **Ola 1 — Baseline (`10` jueces, `124` ítems):**
  - `round_1_flaw_detected_count = 3`: Los jueces detectaron **3 fallos epistémicos explícitos**:
    1. `T-C06-02_judge_1` (`C-06`): *"El enunciado revela literalmente el valor del contraejemplo (r = 8) para refutar el pleno empleo de capital."*
    2. `T-Hab-05-06_judge_1` (`Hab-05`): *"En la fase 3 se pide formular ln((K/Y)(t)/(K/Y)(0))... pero fuera del estado estacionario se requieren la tasa de ahorro s y (K/Y)(0) (no provistos)..."*
    3. `T-Hab-05-05_judge_1` (`Hab-05`): *"En phase1_variables, ninguno de los roles provistos describe el comportamiento asintótico correcto del coeficiente capital-producto K/Y..."*
  - `round_1_kernel_override_count = 2`: Adicionalmente, en `Hab-05` hubo **2 discrepancias de cálculo** (`T-Hab-05-02_judge_1` y `T-Hab-05-04_judge_1`) anuladas temporalmente por prueba constructiva del kernel (`single_seed_override_templates: ["T-Hab-05-02", "T-Hab-05-04"]`).
- **Ola 2 — Stage 5B LQAS Confirmation (`1` juez: `Blind Judge 01` `94aa05dd`, `19.00 s`):**
  - Re-evaluó `4` ítems de los 2 templates con *kernel override*; **`3/4` fallaron** (`agreement_rate = 0.25`, `passed = false`), confirmando que el *kernel override* había ocultado defectos reales en `Hab-05` (p. ej., en `T-Hab-05-02`, el literal `@g@` mal interpolado causó que el juez omitiera `/0.5`).
- **Stage 3B — Atomic Repair (`2` Repair Engineers, `1` ronda):**
  - `Repair Engineer C-06` (`50d9bed4`, `38.00 s`, `7` turnos, `1` edit, `$0.10 USD`): Reparó `T-C06-02` en `shard_06_data.py` y compiló limpio en el intento #1 (`exit=0`).
  - `Repair Engineer Hab-05` (`c8dcf6d7`, `151.00 s`, `9` turnos, `11` edits, `$0.28 USD`): Aplicó barrido epistémico sobre `Hab-05` en `shard_02_data.py`; falló Compilación #1 (`5` errores: `3x INVARIANT`, `TPL-D4`, `TPL-VAR`) y aprobó en Compilación #2 (`exit=0`).
- **Ola 3 — Surgical Rejudge (`2` jueces: `0df167c7` y `f860f0d4`, `22` ítems):**
  - `passed = true`, `agreement_rate = 1.00`, `0` discrepancias, `kernel_override_count = 0`. Total acumulado: `10 + 1 + 2 = 13` jueces.

---

## 6. Informe Detallado de Todos los WARNs No Bloqueantes (Stage 3 Authors & Stage 3B Repairs)

Se extrajeron **todos** los `WARN`s no bloqueantes de los transcripts crudos de los **10 Shard Authors** y **2 Repair Engineers**.

### 6.1. Taxonomía y Causa Raíz Técnica de Por Qué Pasaron

| Regla / Código de WARN | Módulo Validador | Por Qué Pasó (Causa Raíz Técnica) |
| :--- | :--- | :--- |
| `[EPISTEMIC-CLOSURE-WARNING]` | `engine/epistemic_closure.py:346-349` | Verificación heurística de cierre simbólico ($S_{\text{sol}} \subseteq S_{\text{stem}} \cup S_{\text{std}}$). Emite el mensaje como advertencia informativa sin agregarlo a la lista bloqueante `errors`. Ocurre cuando la solución/explicación paso a paso introduce notación estándar implícita del modelo de Solow (`s`, `r`, `K`, `w`, `G`, `Q`, `Y`, `q`, `f`, `f_K`) o yuxtaposiciones como `an_3` (leído como símbolo único en lugar de $a \cdot n_3$) que no aparecen literalmente en el `stem`. |
| `WARNING: [BLOOM-SUPERIOR-TARGET]` | `check_templates.py:2090-2098` | Recomendación pedagógica no bloqueante cuando la cuota de plantillas `Analyze + Evaluate` es `< 70.0%` en un shard (`is_clean = (len(errors) == 0)`). Imprime a `stderr` y permite `exit=0`. |
| `WARNING: [TPL-ORPHAN-VARS]` | `check_templates.py:1204-1214` / `engine/shard_compiler_steps.py:969` | Regla configurada explícitamente como *warn-only* (`# warn-only to accommodate auxiliary vars`) para detectar claves en `vars` no referenciadas en placeholders, stems, hints, solución o `cross_check_py`. |
| `WARNING: [TPL-UNBOUNDED-LOOP]` | `engine/shard_compiler_steps.py:615-620` | Un bucle `while` con condición no-constante (distinto de `while True`) sin contador explícito verificado estáticamente emite `WARNING` a `stderr` en lugar de `FAIL`, asumiendo convergencia rápida. |

### 6.2. Inventario Exhaustivo por Agente, Compilación y Estado Final

| Agente | Compilación / Turno | Código y Mensaje Exacto del WARN | Estado al Pasar (`exit=0`) |
| :--- | :--- | :--- | :--- |
| **Shard Author `shard_01`** | Compile #1 (L9, `exit=1`) & Compile #2 (L15, `exit=0`) | `WARNING: [BLOOM-SUPERIOR-TARGET] Cuota Analyze+Evaluate = 66.7% (8/12 plantillas, < 70.0% recomendado).` | **Persistió** en Compile #2 (`exit=0`). No bloqueante (`8/12` en `Analyze+Evaluate`). |
| **Shard Author `shard_02`** | Compile #1 (L9, `exit=1`) | `Hab-04 (T-Hab-04-04, seed=100): [EPISTEMIC-CLOSURE-WARNING] 'Q-Hab04-001': Símbolos en solución/respuesta (A) no aparecen definidos en stem (S_sol <= S_stem U S_std).` | **Corregido** antes de Compile #2 (`exit=0`, 0 warns). |
| **Shard Author `shard_03`** | Compile #2 (L17, `exit=0`) | `Hab-07 (T-Hab-07-01, seed=100): [EPISTEMIC-CLOSURE-WARNING] 'Q-Hab07-001': Símbolos (K) no aparecen definidos en stem.`<br>`Hab-07 (T-Hab-07-05, seed=100): [EPISTEMIC-CLOSURE-WARNING] 'Q-Hab07-001': Símbolos (w) no aparecen definidos en stem.`<br>`Hab-07 (T-Hab-07-06, seed=100): [EPISTEMIC-CLOSURE-WARNING] 'Q-Hab07-001': Símbolos (w) no aparecen definidos en stem.` | **Persistieron (3 WARNs)** en Compile #2 (`exit=0`). Símbolos `K`, `w` usados en explicación/respuesta sin declararse en stem. |
| **Shard Author `shard_04`** | Compile #1 (L9, `exit=1`) | `C-03 (T-C03-06, seed=100): [EPISTEMIC-CLOSURE-WARNING] 'Q-C03-001': Símbolos (\phi, k, s) no aparecen definidos en stem.` | **Corregido** en Compile #2 (`T-C03-06` limpio). |
| **Shard Author `shard_04`** | Compile #2 (L15, `exit=0`) | `C-03 (T-C03-01, seed=100): [EPISTEMIC-CLOSURE-WARNING] 'Q-C03-001': Símbolos (K, L, Q) no aparecen definidos en stem.` | **Persistió** en Compile #2 (`exit=0`). Nuevo warn introducido tras edición en `C-03`. |
| **Shard Author `shard_05`** | Compile #1 (L7, `exit=1`) | `WARNING: [TPL-ORPHAN-VARS] En 'T-C04-01': claves retornadas en 'vars' no usadas: ['k']`<br>`C-04 (T-C04-04, seed=100): [EPISTEMIC-CLOSURE-WARNING] 'Q-C04-001': Símbolos (K) no aparecen definidos en stem.` | **Ambos corregidos** en ediciones posteriores (`T-C04-01` y `T-C04-04` limpios en Compile #2). |
| **Shard Author `shard_05`** | Compile #2 (L13, `exit=1`) | `C-04 (T-C04-05, seed=100): [EPISTEMIC-CLOSURE-WARNING] 'Q-C04-001': Símbolos (K) no aparecen definidos en stem.` | **Corregido** antes de Compile #3. |
| **Shard Author `shard_05`** | Compile #3 (L21, `exit=0`) | `C-05 (T-C05-06, seed=100): [EPISTEMIC-CLOSURE-WARNING] 'Q-C05-001': Símbolos (Y) no aparecen definidos en stem.` | **Persistió** en Compile #3 (`exit=0`). |
| **Shard Author `shard_06`** | Compile #1 (L9, `exit=1`) | `WARNING: [TPL-UNBOUNDED-LOOP] En 'T-C06-04': Bucle while en 'gen_c06_4' sin contador explícito verificado.`<br>`C-06 (T-C06-06, seed=100): [EPISTEMIC-CLOSURE-WARNING] 'Q-C06-001': Símbolos (b, r) no aparecen definidos en stem.` | **Ambos corregidos** antes de Compile #2. |
| **Shard Author `shard_06`** | Compile #2 (L17, `exit=0`) | `C-07 (T-C07-03, seed=100): [EPISTEMIC-CLOSURE-WARNING] 'Q-C07-001': Símbolos (q, w) no aparecen definidos en stem.`<br>`C-06 (T-C06-04, seed=100): [EPISTEMIC-CLOSURE-WARNING] 'Q-C06-001': Símbolos (an_3, r) no aparecen definidos en stem.` | **Persistieron (2 WARNs)** en Compile #2 (`exit=0`). En `T-C06-04`, `an_3` y `\dot{r}` aparecen en la derivación de solución. |
| **Shard Author `shard_07`** | Compile #1 (L9, `exit=1`) | `WARNING: [TPL-ORPHAN-VARS] En 'T-C08-04': claves no usadas: ['min_dp']`<br>`C-09 (T-C09-06, seed=100): [EPISTEMIC-CLOSURE-WARNING] (q, w)`<br>`C-08 (T-C08-06, seed=100): [EPISTEMIC-CLOSURE-WARNING] (q)`<br>`WARNING: [BLOOM-SUPERIOR-TARGET] Cuota Analyze+Evaluate = 66.7% (8/12)` | `[TPL-ORPHAN-VARS]` **corregido** en Compile #2; los otros **3 persistieron**. |
| **Shard Author `shard_07`** | Compile #2 (L24, `exit=1`) | `C-09 (T-C09-05, seed=103): [EPISTEMIC-CLOSURE-WARNING] 'Q-C09-004': Símbolos (r)`<br>`C-09 (T-C09-06, seed=100): [EPISTEMIC-CLOSURE-WARNING] (q, w)`<br>`C-08 (T-C08-06, seed=100): [EPISTEMIC-CLOSURE-WARNING] (q)`<br>`WARNING: [BLOOM-SUPERIOR-TARGET] Cuota Analyze+Evaluate = 66.7% (8/12)` | Todos **persistieron** hacia Compile #3 (en `T-C09-05` pasó a `seed=100`). |
| **Shard Author `shard_07`** | Compile #3 (L29, `exit=0`) | `C-09 (T-C09-05, seed=100): [EPISTEMIC-CLOSURE-WARNING] (r)`<br>`C-09 (T-C09-06, seed=100): [EPISTEMIC-CLOSURE-WARNING] (q, w)`<br>`C-08 (T-C08-06, seed=100): [EPISTEMIC-CLOSURE-WARNING] (q)`<br>`WARNING: [BLOOM-SUPERIOR-TARGET] Cuota Analyze+Evaluate = 66.7% (8/12)` | **Persistieron (4 WARNs)** en Compile #3 (`exit=0`). |
| **Shard Author `shard_08`** | Compile #1 (L7, `exit=1`) & Compile #2 (L14, `exit=0`) | `C-11 (T-C11-04, seed=100): [EPISTEMIC-CLOSURE-WARNING] (s)`<br>`C-10 (T-C10-04, seed=100): [EPISTEMIC-CLOSURE-WARNING] (G, r, s)`<br>`C-10 (T-C10-05, seed=100): [EPISTEMIC-CLOSURE-WARNING] (r, s)`<br>`C-11 (T-C11-06, seed=100): [EPISTEMIC-CLOSURE-WARNING] (s)`<br>`C-10 (T-C10-06, seed=100): [EPISTEMIC-CLOSURE-WARNING] (r, s)`<br>`WARNING: [BLOOM-SUPERIOR-TARGET] Cuota Analyze+Evaluate = 66.7% (8/12)` | **Persistieron los 6 WARNs** en Compile #2 (`exit=0`). En `T-C10-04`, el stem usa `@r_eq@` numérico mientras la solución cita la EDP simbólica con `G, r, s`. |
| **Shard Author `shard_09`** | Compile #1 (L7, `exit=1`) | `PRE-01 (T-PRE-01-06, seed=100): [EPISTEMIC-CLOSURE-WARNING] (f, f_K)`<br>`WARNING: [BLOOM-SUPERIOR-TARGET] Cuota Analyze+Evaluate = 41.7% (5/12)` | **Persistieron** en Compile #2 y #3. |
| **Shard Author `shard_09`** | Compile #2 (L13, `exit=1`) | `C-01 (T-C01-06, seed=100): [EPISTEMIC-CLOSURE-WARNING] (Q)`<br>`PRE-01 (T-PRE-01-06, seed=100): [EPISTEMIC-CLOSURE-WARNING] (f, f_K)`<br>`WARNING: [BLOOM-SUPERIOR-TARGET] Cuota Analyze+Evaluate = 41.7% (5/12)` | `C-01 (T-C01-06)` **corregido** en Compile #3; los otros 2 **persistieron**. |
| **Shard Author `shard_09`** | Compile #3 (L17, `exit=0`) | `PRE-01 (T-PRE-01-06, seed=100): [EPISTEMIC-CLOSURE-WARNING] (f, f_K)`<br>`WARNING: [BLOOM-SUPERIOR-TARGET] Cuota Analyze+Evaluate = 41.7% (5/12)` | **Persistieron (2 WARNs)** en Compile #3 (`exit=0`). `T-PRE-01-06` usa `F(K,L)` en stem y `f_K` en solución. |
| **Shard Author `shard_10`** | Compile #1 (L7, `exit=0`) | *Ninguno (0 WARNs)* | ✅ Pase limpio (`0` warns, `0` errores). |
| **Repair Engineer `C-06`** | Compile #1 (L15, `exit=0`) | `C-06 (T-C06-04, seed=100): [EPISTEMIC-CLOSURE-WARNING] 'Q-C06-001': Símbolos (an_3, r) no aparecen definidos en stem.` | **Persistió** en Compile #1 (`exit=0`). Heredado de `shard_06` (no tocó `T-C06-04`, solo reparó `T-C06-02`). |
| **Repair Engineer `Hab-05`** | Compile #1 (L21, `exit=1`) | `Hab-05 (T-Hab-05-05, seed=100): [EPISTEMIC-CLOSURE-WARNING] (s)`<br>`Hab-04 (T-Hab-04-04, seed=100): [EPISTEMIC-CLOSURE-WARNING] (A)` | `Hab-04` **corregido/desapareció** en Compile #2; `Hab-05 (T-Hab-05-05)` **persistió**. |
| **Repair Engineer `Hab-05`** | Compile #2 (L27, `exit=0`) | `Hab-05 (T-Hab-05-05, seed=100): [EPISTEMIC-CLOSURE-WARNING] 'Q-Hab05-001': Símbolos en solución/respuesta (s) no aparecen definidos en stem.` | **Persistió** en Compile #2 (`exit=0`). La solución cita $s/(n+g/b)$ sin que `s` aparezca en el stem. |

---

## 7. Recomendaciones Accionables

1. **Corregir desajuste de CLI entre `c2c_wave_workflow.py` y `dispatch.py`:** Eliminar el reenvío de `--templates-per-modality` en `c2c_wave_workflow.py` cuando invoca `dispatch.py dispatch-authors` (o añadir soporte explícito del flag en `dispatch.py`), evitando el fallo de `full_pipeline` (`task-18`) y la necesidad de relanzar `post_cta_pipeline`.
2. **Corregir captura de errores asíncronos en `traceback_analyzer.py`:** Incluir los mensajes `SYSTEM_MESSAGE` de finalización de tareas (`Command exited with code 1`) al catalogar errores, eliminando la brecha entre `5` errores catalogados y `14` `tool_errors_total`.
3. **Reducir tasa de fallo en 1ra compilación (`10.00%`):** Reforzar en el prompt de `c2c_shard_author` la paridad de símbolos entre `stem_variants` (`[TPL-STEM-GRAMMAR]`, `[TPL-STEM-VARIANT-PARITY]`), la prohibición de tautologías en verificadores (`[VERIFIER-TAUTOLOGY-DETECTED]`) y el cumplimiento de `[TPL-DRY]` antes del primer `compile_shard.py`.
4. **Afinar `epistemic_closure.py`:** Soportar yuxtaposiciones implícitas como `an_3` (cuando `a` y `n_3` están en `allowed`) y distinguir símbolos introducidos únicamente en la explicación pedagógica (`explanation_es`) vs símbolos requeridos en la respuesta final (`expected_answer`).
