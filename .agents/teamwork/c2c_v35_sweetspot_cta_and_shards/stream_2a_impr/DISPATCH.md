# DISPATCH — Stream 2A (Gate 2, Phase 2: Integrator Improver `impr_2a`)

## 1. Rol y Frontera Exclusiva de Escritura
Eres el **Mejorador de Integración del Stream 2A (Gate 2)** bajo `/flash-triad-orchestrator`.
- **Archivos de Producción y Test Permitidos:**
  1. `.agents/skills/content-to-course/subagent_types.json`
  2. `tests/test_sweetspot_v35_cta_and_shards.py`
- **Artefacto de Gobernanza Permitido:**
  - `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_2a_impr/handoff.md`

## 2. Requerimientos Técnicos
1. Lee `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_2a_impl/BRIEFING.md` y `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_2a_impl/handoff.md`.
2. Audita y endurece `tests/test_sweetspot_v35_cta_and_shards.py` agregando pruebas de casos borde cruzados (por ejemplo, recuperación con `has_syntax_error=True` tanto en `compile_cta.py` como en `compile_shard.py` frente a `c2c_hook_guard.py`, y verificación de que `subagent_types.json` esté 100% sincronizado byte a byte con `system_prompts/lean/`).
3. Ejecuta:
   `.venv\Scripts\python.exe -m pytest tests/test_sweetspot_v35_cta_and_shards.py tests/test_cta_sweetspot_and_autoheal.py tests/test_shard06_and_dry_archetypes.py tests/test_hook_post_pass_and_write_isolation.py tests/test_dispatch_turn0_and_milestone3_prompts.py tests/test_prompts_contract_alignment.py -q`
4. Escribe `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_2a_impr/handoff.md` y envía `DONE::` al Orquestador (`7d2e6386-9933-4c70-9e50-a3cf214925f6`).
