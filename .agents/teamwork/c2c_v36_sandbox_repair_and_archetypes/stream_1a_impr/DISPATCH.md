# DISPATCH — Stream 1A (Fase 2: Mejorador `impr_1a`)

## 1. Rol y Frontera Exclusiva de Escritura (`Exclusive Write Boundaries`)
Eres el **Mejorador (Fase 2) del Stream 1A** bajo `/flash-triad-orchestrator`.
- **Carpeta de Gobernanza:** `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1a_impr/`
- **Archivos de Producción Permitidos (ÚNICOS que puedes modificar):**
  1. `.agents/skills/content-to-course/cta_merge.py`
  2. `tests/test_cta_merge_prereq_scoping.py`
- **Artefactos de Gobernanza Permitidos:**
  - `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1a_impr/BRIEFING.md`
  - `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1a_impr/handoff.md`
- **PROHIBIDO** editar cualquier otro archivo del repositorio. Nunca pases `ArtifactMetadata` a `write_file` o `edit_file`.

## 2. Paso 0 Obligatorio (*Pre-Flight*)
1. Lee `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1a_impl/handoff.md`, `.agents/skills/content-to-course/cta_merge.py` (líneas 668–995) y `tests/test_cta_merge_prereq_scoping.py`.
2. Escribe `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1a_impr/BRIEFING.md`.

## 3. Tareas de Endurecimiento (Hardening & Edge Cases)
1. Verifica y endurece en `merge_cta_parts` (`cta_merge.py`):
   - **Ciclos intra-parte accidentales:** Si un autor de `part_XX.json` introduce por error un ciclo de prerrequisitos entre dos competencias de la misma subparte (`A <-> B`), el ordenamiento topológico intra-parte debe degradar limpiamente (rompiendo el ciclo determinísticamente según `_sort_key` sin quedar en loop infinito ni perder competencias) y luego el filtro `pos[prereq] < pos[comp]` debe eliminar la arista hacia adelante residual para que `check_prerequisites_dag` pase al 100%.
   - **Modo Incremental (`--append` / `delta_manifest.json`):** Si una competencia de `part_01` o `part_02` referencia un ID de competencia del curso base existente (`existing_competency_ids` en `delta_info`), ese prerrequisito externo (que no está en `comp_pos` pero sí en `existing_competency_ids`) debe **conservarse** intacto y no ser filtrado por `comp_pos[mapped] < idx`.
   - **Limpieza de llaves temporales:** Garantiza que ni `_part_key` ni `_sort_key` queden jamás en los objetos de `cta_draft.json` o `cta.json`.
2. Amplía `tests/test_cta_merge_prereq_scoping.py` con tests adversarios para:
   - Ciclo intra-parte `A <-> B` en `part_01.json` (resuelto determinísticamente sin ciclo ni forward prereq en `cta.json`).
   - Modo `--append` (`delta` en `pre_cta_manifest.json` con `existing_competency_ids: ["C-01", "H-01"]` y `next_numbers_by_prefix: {"C": 2, "H": 2, "Hab": 1}`), verificando que los prerrequisitos hacia el curso base existente se preserven mientras los intra-parte nuevos se mapeen sin colisión.
   - Simulación a escala real del caso `asyntotic_estatistics_v6` (2 partes con 12 y 13 competencias respectivamente donde `part_01` y `part_02` numeran ambas desde `C-01, H-01, Hab-01`), verificando `0` forward prerequisites y `validate_cta_rules` = `True`.
3. Ejecuta `.venv\Scripts\python.exe -m pytest tests/test_cta_merge_prereq_scoping.py tests/test_cta_sweetspot_and_autoheal.py tests/test_cta_mapreduce.py -q`.
4. Escribe `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1a_impr/handoff.md` y envía `DONE:: Stream 1A Improver completado` a `d603756a-7e58-4466-b883-cbc391586154`.
