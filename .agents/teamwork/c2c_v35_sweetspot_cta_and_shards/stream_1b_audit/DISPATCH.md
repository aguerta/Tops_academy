# DISPATCH — Stream 1B (Phase 3: Forensic Auditor `audit_1b`)

## 1. Rol y Misión
Eres el **Auditor Forense (Phase 3 Auditor)** del **Stream 1B (`compile_shard.py`, `check_templates.py`, `tests/test_shard06_and_dry_archetypes.py`)** dentro de `/flash-triad-orchestrator`.
Debes leer primero:
1. `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1b_impl/BRIEFING.md`
2. `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1b_impl/handoff.md`
3. `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1b_impr/handoff.md`

## 2. Frontera Exclusiva de Escritura (SOLO Gobernanza)
- **ÚNICO ARCHIVO PERMITIDO:**
  - `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1b_audit/handoff.md`
- **PROHIBIDO TOCAR:** Cualquier archivo de código de producción o tests.

## 3. Checklist de Auditoría Forense Obligatoria
1. **Inspección de Código Real (`read_file`):**
   - Verifica en `compile_shard.py` y `check_templates.py`:
     - Persistencia de `error_count` y `has_syntax_error` en `.check_attempts/compile_<shard_id>.json` y receipts `--output`.
     - Directiva dinámica `[UMBRAL < 6 ...]` vs `[UMBRAL >= 6 ...]` en `render_compact_aggregated_errors` con garantía `<= 28` líneas.
     - Gate determinista `[M3-ARCHETYPES]` (`--min-archetypes` / `min_archetypes` en `pre_shard_manifest.json`) que rechaza competencias con `< min_arch` tuplas o tuplas clonadas idénticas en `TEMPLATES`.
     - Ordenamiento ascendente de `helper_functions` en `ShardDataLineLocator.get_preamble_code()` para soportar `_gen_<cid>(rng, arch)`.
2. **Inspección de Tests Reales (`read_file`):**
   - Verifica en `tests/test_shard06_and_dry_archetypes.py` que los nuevos tests de umbral `< 6` y de `[M3-ARCHETYPES]` prueben el comportamiento real sin mocks triviales.
3. **Ejecución Independiente de Pruebas (`run_command`):**
   - Ejecuta `.venv\Scripts\python.exe -m pytest tests/test_shard06_and_dry_archetypes.py tests/test_compile_shard.py tests/test_shard_compiler_hardening.py tests/test_c2c_error_aggregation.py -q` y verifica `100% PASS`.
4. **Handoff y Señal Final:**
   - Escribe `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1b_audit/handoff.md` y envía `PASS::` (o `FAIL::`) al Orquestador (`7d2e6386-9933-4c70-9e50-a3cf214925f6`).
