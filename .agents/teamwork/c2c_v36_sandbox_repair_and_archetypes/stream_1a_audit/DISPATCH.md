# DISPATCH — Stream 1A (Fase 3: Auditor Forense `audit_1a`)

## 1. Rol y Restricción Read-Only en Producción
Eres el **Auditor Forense (Fase 3) del Stream 1A** bajo `/flash-triad-orchestrator`.
- **Carpeta de Gobernanza (ÚNICA donde puedes escribir):** `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1a_audit/`
  - `BRIEFING.md`
  - `handoff.md`
- **PROHIBIDO** editar cualquier archivo de producción o de `tests/`. Nunca pases `ArtifactMetadata` a `write_file`.

## 2. Protocolo de Auditoría Forense
1. Lee `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1a_impl/handoff.md` y `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1a_impr/handoff.md`, y escribe `stream_1a_audit/BRIEFING.md`.
2. Inspecciona `.agents/skills/content-to-course/cta_merge.py` (líneas 668–995) y `tests/test_cta_merge_prereq_scoping.py`:
   - Verifica que `comp_id_map_by_part` aísle los IDs por subparte (`_part_key`), impidiendo que `part_02` sobrescriba los prerrequisitos locales de `part_01`.
   - Verifica que el ordenamiento topológico intra-parte degrade limpiamente ante ciclos accidentales y que el filtro final garantice `0` prerrequisitos hacia adelante (`comp_pos[prereq] < comp_pos[comp]`), preservando `existing_competency_ids` en modo `--append`.
   - Verifica que los tests en `tests/test_cta_merge_prereq_scoping.py` contengan aserciones reales y estrictas (sin falsos positivos).
3. Ejecuta de forma independiente `.venv\Scripts\python.exe -m pytest tests/test_cta_merge_prereq_scoping.py tests/test_cta_sweetspot_and_autoheal.py tests/test_cta_mapreduce.py -q`.
4. Escribe tu dictamen en `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1a_audit/handoff.md` y envía `PASS:: Stream 1A Auditor aprobado` o `REJECT:: <archivo:línea> | <defecto>` a `d603756a-7e58-4466-b883-cbc391586154`.
