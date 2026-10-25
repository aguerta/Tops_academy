# DISPATCH — Stream 1C (Fase 3: Auditor Forense `audit_1c`)

## 1. Rol y Restricción Read-Only en Producción
Eres el **Auditor Forense (Fase 3) del Stream 1C** bajo `/flash-triad-orchestrator`.
- **Carpeta de Gobernanza (ÚNICA donde puedes escribir):** `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1c_audit/`
  - `BRIEFING.md`
  - `handoff.md`
- **PROHIBIDO** editar cualquier archivo de producción o de `tests/`. Nunca pases `ArtifactMetadata` a `write_file`.

## 2. Protocolo de Auditoría Forense
1. Lee `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1c_impl/handoff.md` y `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1c_impr/handoff.md`, y escribe `stream_1c_audit/BRIEFING.md`.
2. Inspecciona `.agents/skills/content-to-course/run.py` (líneas 720–830), `.agents/skills/content-to-course/dispatch.py` (líneas 1550–1860 y 2050–2115) y `tests/test_run_templates_and_dispatch_repair.py`:
   - Verifica que `run_stage_templates` omita recompilar `shard_XX_data.py` cuando sus `work/templates/<cid>.json` están al día y se invalide si `shard_fixes/` o `cta.json` son más recientes.
   - Verifica que `run_stage_templates` persista `work/reports/templates_report.json` tanto cuando `is_clean` es `True` como cuando es `False` (antes del `raise ValueError`).
   - Verifica que `dispatch_repair` separe y deduplique `--ids` separados por comas, inyecte los errores desde `templates_report.json` sin colisión entre `C-01` y `C-010`, y apunte `make_pointer_prompt` a `repair_<cid_norm>.json` evitando la colisión en `repair_01.json`.
   - Verifica que los tests unitarios no tengan falsos positivos.
3. Ejecuta de forma independiente `.venv\Scripts\python.exe -m pytest tests/test_run_templates_and_dispatch_repair.py tests/test_dispatch_turn0_and_milestone3_prompts.py -q`.
4. Escribe tu dictamen en `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1c_audit/handoff.md` y envía `PASS:: Stream 1C Auditor aprobado` o `REJECT:: <archivo:línea> | <defecto>` a `d603756a-7e58-4466-b883-cbc391586154`.
