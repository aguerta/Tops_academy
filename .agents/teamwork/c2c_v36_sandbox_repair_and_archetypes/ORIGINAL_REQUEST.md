# ORIGINAL REQUEST — `c2c_v36_sandbox_repair_and_archetypes`

El usuario solicitó aplicar mediante `/flash-triad-orchestrator` todos los parches para resolver de raíz los hallazgos detectados en la auditoría de `asyntotic_estatistics_v6` (`bb374ed7`), incluyendo explícitamente la corrección de los **prerrequisitos hacia adelante (`Forward Prerequisites`)**:

1. **Stream 1A — `cta_merge.py` (Corrección de Prerrequisitos hacia Adelante y Colisión de `comp_id_map` por Parte):**
   - Aislar el mapeo de IDs de competencias por subparte (`part_key`) en `merge_cta_parts` (`cta_merge.py:857-902`) para que los IDs locales `C-01`, `H-01`, `Hab-01` de `part_02` jamás sobrescriban los de `part_01` al reescribir `prerequisites`.
   - Aplicar ordenamiento topológico estable intra-parte antes de la renumeración secuencial (`H-01..`, `C-01..`, `Hab-01..`) y garantizar el invariante estricto `pos[prereq] < pos[comp]` (cero prerrequisitos hacia adelante en `cta_draft.json`, `cta_outline.json` y `cta.json`).

2. **Stream 1B — `engine/sandbox.py` y `check_templates.py` (Pre-compilación AST/Bytecode, Reloj de CPU por Hilo y `BUDGET HALT` por Competencia):**
   - Pre-validar AST (`validate_code_ast`) y pre-compilar bytecode (`compile()`) **una sola vez por plantilla** fuera del bucle de 50 semillas en `execute_sandbox_batch` (`engine/sandbox.py:535-589`).
   - Medir el timeout de `call_with_timeout` (`engine/sandbox.py:406-445`) con tiempo de CPU del hilo (`time.thread_time()`) más techo de seguridad de reloj de pared (`max(timeout * 4.0, 3.0)`), eliminando los falsos `SandboxTimeoutError (0.8s)` por inanición del GIL en `ThreadPoolExecutor`.
   - Limitar `max_workers` en `check_templates_file_or_dir` (`check_templates.py:2941`) a `min(4, os.cpu_count() or 4, len(template_files))` y corregir el bug del booleano global `is_clean` en el circuit-breaker `BUDGET HALT` (`check_templates.py:3153-3221`), evaluando `cid_is_clean` individualmente por cada competencia `cid`.

3. **Stream 1C — `run.py` y `dispatch.py` (Compilación Incremental en `--stage templates`, Persistencia de `templates_report.json` y 3 Fixes en `dispatch-repair`):**
   - En `run_stage_templates` (`run.py:738-765`), omitir la recompilación secuencial de `shard_*_data.py` cuyos `work/templates/<cid>.json` ya estén al día (`mtime`), y persistir siempre `work/reports/templates_report.json` con `errors`, `errors_by_cid` y `failed_competencies`.
   - En `dispatch_repair` (`dispatch.py:1555-1840, 2071`), soportar `--ids` separados por comas (`.split(",")`), extraer los errores por competencia desde `templates_report.json` y corregir la colisión del puntero `repair_01.json` apuntando `make_pointer_prompt` a `cid_item_file.name` (`repair_<cid>.json`).

4. **Stream 1D — `compile_shard.py` y `prompt_shard_author.md` (Compuerta Semántica `[M3-ARCHETYPES]` y Ejemplo Canónico con 4 Arquetipos Reales):**
   - En `compile_shard.py:1653-1675`, exigir que las tuplas de una competencia en modo `--strict` tengan enunciados `stem_es` distintos (`len(distinct_stems) >= min(eff_min_arch, len(tpls))`) y que sus generadores no devuelvan salidas idénticas para todas las tuplas (bloqueando listas `stems` clonadas y funciones `_gen_*(rng, arch=1)` que ignoran `arch`).
   - En `system_prompts/prompt_shard_author.md` y `system_prompts/lean/prompt_shard_author.md`, actualizar el Ejemplo Canónico 1 (`H-01` Carnot) para que `_gen_h01(rng, arch=1)` ramifique explícitamente en `arch == 1, 2, 3, 4` con 4 enunciados distintos.
