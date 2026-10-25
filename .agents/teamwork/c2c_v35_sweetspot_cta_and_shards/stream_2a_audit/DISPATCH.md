# DISPATCH — Stream 2A (Gate 2, Phase 3: Final Integrator Forensic Auditor `audit_2a`)

## 1. Rol y Frontera Exclusiva de Escritura (SOLO Gobernanza)
Eres el **Auditor Forense Final del Stream 2A (Gate 2)** bajo `/flash-triad-orchestrator`.
- **ÚNICO ARCHIVO PERMITIDO:**
  - `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_2a_audit/handoff.md`
- **PROHIBIDO TOCAR:** Cualquier archivo de código de producción o tests.

## 2. Checklist de Auditoría Forense Integral
1. Lee `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_2a_impl/BRIEFING.md`, `stream_2a_impl/handoff.md` y `stream_2a_impr/handoff.md`.
2. Inspecciona `subagent_types.json` y `tests/test_sweetspot_v35_cta_and_shards.py`.
3. Verifica con `git status --short` que todos los archivos modificados pertenezcan únicamente a las fronteras autorizadas de los Streams 1A, 1B, 1C, 1D, 2A y `FUTURE_MILESTONES.md`, sin archivos basura ni scripts temporales.
4. Ejecuta la suite integral de regresión:
   `.venv\Scripts\python.exe -m pytest tests/test_sweetspot_v35_cta_and_shards.py tests/test_cta_sweetspot_and_autoheal.py tests/test_shard06_and_dry_archetypes.py tests/test_hook_post_pass_and_write_isolation.py tests/test_dispatch_turn0_and_milestone3_prompts.py tests/test_prompts_contract_alignment.py tests/test_c2c_v321_comp4_prompts.py tests/test_cta_healing.py tests/test_cta_mapreduce.py tests/test_compile_shard.py -q`
5. Escribe `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_2a_audit/handoff.md` y envía `PASS::` (o `FAIL::`) al Orquestador (`7d2e6386-9933-4c70-9e50-a3cf214925f6`).
