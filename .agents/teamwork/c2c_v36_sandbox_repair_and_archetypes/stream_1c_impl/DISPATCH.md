# DISPATCH — Stream 1C (Fase 1: Implementador `impl_1c`)

## 1. Rol y Frontera Exclusiva de Escritura (`Exclusive Write Boundaries`)
Eres el **Implementador del Stream 1C** bajo `/flash-triad-orchestrator`.
- **Carpeta de Gobernanza:** `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1c_impl/`
- **Archivos de Producción Permitidos (ÚNICOS que puedes modificar):**
  1. `.agents/skills/content-to-course/run.py`
  2. `.agents/skills/content-to-course/dispatch.py`
  3. `tests/test_run_templates_and_dispatch_repair.py`
- **Artefactos de Gobernanza Permitidos:**
  - `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1c_impl/BRIEFING.md`
  - `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1c_impl/handoff.md`
- **PROHIBIDO** editar cualquier otro archivo del repositorio. Nunca pases `ArtifactMetadata` a `write_file` o `edit_file`.

## 2. Paso 0 Obligatorio (*Pre-Flight Sanity Check*)
Antes de realizar cualquier edición:
1. Lee `.agents/skills/content-to-course/run.py` (líneas 720–785) y `.agents/skills/content-to-course/dispatch.py` (líneas 1550–1855 y 2050–2115).
2. Escribe `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1c_impl/BRIEFING.md` confirmando líneas y firmas reales. Si detectas un bloqueo fuera de tu frontera, detén ediciones y envía `BLOCKER:: <archivo:línea> | <causa> | <opciones>` al Orquestador (`d603756a-7e58-4466-b883-cbc391586154`).

## 3. Especificación Técnica de Implementación

### A. Compilación Incremental de Shards y Persistencia de `work/reports/templates_report.json` en `run_stage_templates` (`run.py:728-775`)
1. **Problema Raíz #1 (Recompilación secuencial redundante, `run.py:738-748`):**
   - Cada vez que el Director ejecuta `run.py --stage templates`, `run_stage_templates` recompila secuencialmente todos los `shard_*_data.py` llamando a `compile_shard_file` (lo que re-ejecuta `check_templates` shard por shard durante ~3.5 minutos) incluso cuando los Shard Authors ya habían compilado sus `work/templates/<cid>.json`!
   - **Solución:**
     - Antes de llamar a `compile_shard_file(shard_path=shard_f, ...)` en `run_stage_templates`, verifica si `pre_shard_manifest.json` existe y cuáles `competency_ids` corresponden a `shard_f.stem.replace("_data", "")` (ej. `shard_01`).
     - Si todos los archivos `templates_dir / f"{cid}.json"` de ese shard ya existen, no están vacíos y tienen `cid_json.stat().st_mtime >= shard_f.stat().st_mtime` (y también `>= cualquier shard_fixes/<cid>.py` si existe), **omite** `compile_shard_file` para ese shard e imprime `  [i] Skipping compilation for {shard_f.name} (templates up-to-date).`. Si falta algún `.json` o el `.py` es más reciente, compílalo normalmente.
2. **Problema Raíz #2 (Falta de `work/reports/templates_report.json`, `run.py:756-765`):**
   - `run_stage_templates` llama a `check_templates_file_or_dir(templates_dir)` en memoria y, si falla, lanza `ValueError` sin escribir `work/reports/templates_report.json`. Cuando el Director ejecuta después `dispatch.py dispatch-repair`, este busca `work/reports/templates_report.json` (`dispatch.py:1557`), no lo encuentra y deja a los subagentes reparadores a ciegas (`manual_request: True`)!
   - **Solución en `run_stage_templates` (`run.py`):**
     - Tanto cuando `is_clean` es `False` como cuando es `True`, construye un diccionario `errors_by_cid: Dict[str, List[str]] = {}` asociando cada mensaje de `errors` a la competencia `cid` correspondiente (buscando referencias a `cid` conocidas de `cta.json` / `templates/*.json` en el texto del error, p. ej. `f"/{cid}.json"`, `f"\\{cid}.json"`, `f"'{cid}'"`, `f"[{cid}]"`, `f"Competency {cid}"`, `f"competency '{cid}'"`).
     - Escribe `self.work_dir / "reports" / "templates_report.json"` (creando `reports/` si no existe) con:
       ```json
       {
         "status": "PASS" if is_clean else "FAIL",
         "total_templates": total_t,
         "total_seeds_run": total_s,
         "errors": errors,
         "warnings": warnings,
         "errors_by_cid": errors_by_cid,
         "failed_competencies": sorted(errors_by_cid.keys())
       }
       ```
     - Haz esto **antes** de hacer `raise ValueError(...)` cuando `not is_clean`.

### B. Tres Correcciones en `dispatch_repair` (`dispatch.py:1550-1850, 2070`)
1. **Soporte para `--ids` separados por comas (`dispatch.py:1674, 2071`):**
   - En `dispatch_repair`: si `ids` contiene strings con comas (ej. `["C-05,C-11,H-02,H-05"]` o `"C-05, C-11"`), aplánalos separando por `,` (`[part.strip() for raw in ids for part in str(raw).split(",") if part.strip()]`) antes de iterar sobre `req_ids`.
2. **Extracción de errores por competencia desde `templates_report.json` (`dispatch.py:1620-1690`):**
   - En `dispatch_repair`, cuando lee `templates_report_p` (`work/reports/templates_report.json`), además de soportar los formatos legacy (`"competencies"` / `"results"`), soporta el formato `errors_by_cid` y la lista plana `"errors"` de `templates_report.json`:
     - Si `templates_report` tiene `"errors_by_cid"` (un dict `cid -> list[str]`), para cada `cid, err_list` con errores no vacíos, registra `failed_competencies.setdefault(cid, {"cid": cid, "errors": [], "failed_seeds": []})["errors"].extend(err_list)`.
     - Si `templates_report` tiene `"errors"` (lista de strings), asocia cada string de error a cualquier `cid` conocido (de `cid_to_shard` o regex `\b(?:C|H|Hab)-\d+\b`) que aparezca en el string del error.
3. **Corrección de colisión del archivo puntero `repair_01.json` (`dispatch.py:1813-1836`):**
   - Actualmente, `dispatch_repair` escribe `item_file = items_dir / f"repair_{idx:02d}.json"` y `cid_item_file = items_dir / f"repair_{cid_norm}.json"`, pero construye el `pointer_prompt` con `make_pointer_prompt(work_rel, f"prompts/repair/{item_file.name}")` (`repair_01.json`). Cuando el Director despacha `--ids C-05` y luego `--ids C-08`, la segunda llamada sobrescribe `repair_01.json` y ambos subagentes leen el mismo archivo!
   - Cambia `make_pointer_prompt` en `dispatch_repair` para que apunte a `f"prompts/repair/{cid_item_file.name}"` (`repair_{cid_norm}.json`) y pon `f"prompts/repair/{cid_item_file.name}"` como archivo primario en `item_files`, manteniendo la escritura de `repair_{idx:02d}.json` y `repair_{cid_norm}.json` en `prompts/repair/` y `dispatch/items/` para 100% compatibilidad hacia atrás con los tests existentes!

## 4. Verificación y Entrega
1. Crea `tests/test_run_templates_and_dispatch_repair.py` con tests unitarios que verifiquen:
   - Que `dispatch_repair` con `--ids "C-05,C-11,H-02"` separa correctamente las 3 competencias y genera 3 subagentes cuyos `Prompt` apuntan a `prompts/repair/repair_c05.json`, `prompts/repair/repair_c11.json` y `prompts/repair/repair_h02.json` (sin colisionar en `repair_01.json`).
   - Que cuando `work/reports/templates_report.json` contiene `errors` y `errors_by_cid`, `dispatch_repair` inyecta los mensajes de error exactos dentro de `work/prompts/repair/repair_<cid>.json` en lugar de caer en `manual_request` vacío.
   - Que `run_stage_templates` escribe `work/reports/templates_report.json` tanto en caso de éxito como de fallo, y omite recompilar `shard_01_data.py` cuando sus `work/templates/<cid>.json` ya son más recientes que `shard_01_data.py`.
2. Ejecuta `.venv\Scripts\python.exe -m pytest tests/test_run_templates_and_dispatch_repair.py tests/test_dispatch_turn0_and_milestone3_prompts.py -q`.
3. Escribe `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1c_impl/handoff.md` y envía `DONE:: Stream 1C Implementer completado` a `d603756a-7e58-4466-b883-cbc391586154`.
