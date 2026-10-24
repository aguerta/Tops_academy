# DISPATCH — Stream 2A (Fase 3: Auditor Forense `audit_2a` — Victory Gate)

- **Rol:** Auditor Forense Independiente (Fase 3 de la Tríada Secuencial — Etapa 2 Post-Gate 1 / Victory Gate)
- **Orquestador Conversation ID:** `526cfac0-d37b-49c9-bf09-00b5c520add2`
- **Handoffs Previos (Lectura Obligatoria):**
  - `.agents/teamwork/c2c_v34_variance_and_shard06/stream_2a_impl/handoff.md`
  - `.agents/teamwork/c2c_v34_variance_and_shard06/stream_2a_impr/handoff.md`
  - `.agents/teamwork/c2c_v34_variance_and_shard06/ORIGINAL_REQUEST.md`
- **Directorio de Gobernanza:** `.agents/teamwork/c2c_v34_variance_and_shard06/stream_2a_audit/`

## 1. Frontera de Escritura Exclusiva (`Exclusive Write Boundary`)
Como Auditor Forense de cierre, tienes permiso de escritura **ÚNICAMENTE** sobre:
1. `.agents/teamwork/c2c_v34_variance_and_shard06/stream_2a_audit/BRIEFING.md`
2. `.agents/teamwork/c2c_v34_variance_and_shard06/stream_2a_audit/handoff.md`

**PROHIBIDO** editar cualquier archivo de código de producción o tests.

## 2. Checklist de Auditoría Forense del Victory Gate (`Gate 2`)

Debes ejecutar y verificar de forma independiente con `run_command` y `read_file`:

1. **Verificación de `git status --short` y Fronteras:**
   - Confirma que todos los archivos modificados/creados en el repositorio correspondan exclusivamente a los Streams 1A, 1B, 1C, 1D y 2A y al directorio de gobernanza `.agents/teamwork/c2c_v34_variance_and_shard06/`.
   - Confirma que no existan archivos temporales sueltos (`scratch/`, `out_*.txt`, `test_debug*.py`) en la raíz del proyecto.
2. **Verificación de los 3 Requisitos Inviolables en `ORIGINAL_REQUEST.md`:**
   - **Milestone 3 (Diversidad de 4 Arquetipos por Competencia):** Verifica que `courses/asyntotic_estatistics_v4/work/shards/shard_06_data.py` y `Hab-06.json` tengan los 4 arquetipos disjuntos (*Directo, Inverso, Perturbación, Frontera*) y que `system_prompts/` + `dispatch.py` exijan los 4 arquetipos con formato DRY de distractores.
   - **Agnosticismo de Dominio 100%:** Ejecuta una búsqueda/inspección en `.agents/skills/content-to-course/` (`engine/assemble.py`, `compile_shard.py`, `check_templates.py`, `dispatch.py`, `c2c_hook_guard.py`, `system_prompts/lean/*.md`, `system_prompts/*.md`, `subagent_types.json`) para confirmar que **no** se haya introducido ninguna referencia hardcodeada a `Greene` ni a `asyntotic_estatistics` en el motor ni en los prompts del pipeline.
   - **Certificación de `shard_06` (`Hab-06.json`) y Test de Regresión del `shard_06_data.py` Original:**
     - Ejecuta independientemente:
       `.venv\Scripts\python.exe .agents/skills/content-to-course/check_templates.py courses/asyntotic_estatistics_v4/work/templates/Hab-06.json --cta courses/asyntotic_estatistics_v4/work/cta.json --strict`
     - Verifica que `courses/asyntotic_estatistics_v4/work/shards/shard_06.json` tenga `"compiled_status": "PASS"` y `courses/asyntotic_estatistics_v4/work/.check_attempts/pass_shard_06.json` tenga `"status": "PASS"` con `"template_counts": {"Hab-06": 4}`.
     - Verifica en `tests/test_forensic_shard06_and_variance_v34.py` que no queden aserciones flojas con `or` en las líneas auditadas (`L436`, `L455`, `L468`, `L563-564`) y que exista y pase `test_legacy_shard06_exact_code_compiles_cleanly`.
3. **Ejecución Independiente de la Batería Completa de `pytest`:**
   - Ejecuta:
     `.venv\Scripts\python.exe -m pytest tests/test_forensic_shard06_and_variance_v34.py tests/test_assemble_katex_and_rationale.py tests/test_shard06_and_dry_archetypes.py tests/test_dispatch_turn0_and_milestone3_prompts.py tests/test_hook_post_pass_and_write_isolation.py tests/test_prompts_contract_alignment.py`
   - Verifica `0` fallos y `0` errores.

## 3. Protocolo de Ejecución y Cierre
1. Escribe primero `.agents/teamwork/c2c_v34_variance_and_shard06/stream_2a_audit/BRIEFING.md`.
2. Ejecuta todas las verificaciones independientes.
3. Escribe `.agents/teamwork/c2c_v34_variance_and_shard06/stream_2a_audit/handoff.md` con la evidencia completa y tu veredicto (`PASS` o `FAIL`).
4. Envía un mensaje con `send_message` a `526cfac0-d37b-49c9-bf09-00b5c520add2` con prefijo `PASS::` (o `FAIL::` si encuentras cualquier incumplimiento).
