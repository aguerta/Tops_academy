# DISPATCH — Stream 1C (Fase 2: Mejorador `impr_1c`)

## 1. Rol y Frontera Exclusiva de Escritura (`Exclusive Write Boundaries`)
Eres el **Mejorador (Fase 2) del Stream 1C** bajo `/flash-triad-orchestrator`.
- **Carpeta de Gobernanza:** `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1c_impr/`
- **Archivos de Producción Permitidos (ÚNICOS que puedes modificar):**
  1. `.agents/skills/content-to-course/run.py`
  2. `.agents/skills/content-to-course/dispatch.py`
  3. `tests/test_run_templates_and_dispatch_repair.py`
- **Artefactos de Gobernanza Permitidos:**
  - `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1c_impr/BRIEFING.md`
  - `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1c_impr/handoff.md`
- **PROHIBIDO** editar cualquier otro archivo del repositorio. Nunca pases `ArtifactMetadata` a `write_file` o `edit_file`.

## 2. Paso 0 Obligatorio (*Pre-Flight*)
1. Lee `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1c_impl/handoff.md`, `.agents/skills/content-to-course/run.py` (líneas 720–810), `.agents/skills/content-to-course/dispatch.py` (líneas 1550–1860 y 2050–2115) y `tests/test_run_templates_and_dispatch_repair.py`.
2. Escribe `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1c_impr/BRIEFING.md`.

## 3. Tareas de Endurecimiento (Hardening & Edge Cases)
1. En `run.py` (`run_stage_templates`, líneas 725–805):
   - **Invalidez por `shard_fixes/<CID>.py` o `cta.json` más reciente:** Al decidir si omitir (`skip`) la recompilación de `shard_XX_data.py`, verifica también que ningún archivo en `work/shards/shard_fixes/` (o `work/shard_fixes/`) correspondiente a las competencias de ese shard tenga `mtime > cid_json.stat().st_mtime`. Si existe un fix modular más reciente que el `.json`, **no** omitas la compilación de ese shard.
   - **No-colisión de prefijos al construir `errors_by_cid`:** Asegúrate de que un error que menciona `"C-10"` no se asocie falsamente a `"C-1"` (usa regex con frontera `\b` o coincidencia exacta de delimitadores).
2. En `dispatch.py` (`dispatch_repair`, líneas 1550–1860):
   - **Deduplicación de `--ids` y preservación de orden:** Si el llamador pasa `--ids "C-05, C-11, C-05"` o combina múltiples flags/comas, deduplica preservando el orden.
   - **Inyección de los errores reales en el prompt de reparación (`repair_<cid>.json`):** Verifica que cuando `failed_competencies[cid]["errors"]` contiene los mensajes de error extraídos de `templates_report.json`, esos mensajes se incluyan claramente en la sección de errores diagnosticados del prompt escrito en `prompts/repair/repair_<cid_norm>.json` (y en `dispatch/items/repair_<cid_norm>.json`) para que el `Repair Engineer` vea exactamente qué falló desde su Turno 1!
3. Amplía `tests/test_run_templates_and_dispatch_repair.py` con tests adversarios para:
   - Invalidación de caché incremental cuando se modifica `work/shards/shard_fixes/C-01.py` (`mtime` más reciente que `work/templates/C-01.json`), verificando que `run_stage_templates` sí recompile `shard_01_data.py`.
   - No-colisión entre `C-01` y `C-010` en `errors_by_cid` y `dispatch_repair`.
   - Deduplicación de `--ids "C-05,C-08,C-05"`.
4. Ejecuta `.venv\Scripts\python.exe -m pytest tests/test_run_templates_and_dispatch_repair.py tests/test_dispatch_turn0_and_milestone3_prompts.py -q`.
5. Escribe `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1c_impr/handoff.md` y envía `DONE:: Stream 1C Improver completado` a `d603756a-7e58-4466-b883-cbc391586154`.
