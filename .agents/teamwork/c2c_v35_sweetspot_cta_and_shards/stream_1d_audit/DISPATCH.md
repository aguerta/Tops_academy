# DISPATCH — Stream 1D (Phase 3: Forensic Auditor `audit_1d`)

## 1. Rol y Misión
Eres el **Auditor Forense (Phase 3 Auditor)** del **Stream 1D (`dispatch.py`, `system_prompts/**`, `tests/test_dispatch_turn0_and_milestone3_prompts.py`)** dentro de `/flash-triad-orchestrator`.
Debes leer primero:
1. `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1d_impl/BRIEFING.md`
2. `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1d_impl/handoff.md`
3. `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1d_impr/handoff.md`

## 2. Frontera Exclusiva de Escritura (SOLO Gobernanza)
- **ÚNICO ARCHIVO PERMITIDO:**
  - `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1d_audit/handoff.md`
- **PROHIBIDO TOCAR:** Cualquier archivo de código de producción o tests.

## 3. Checklist de Auditoría Forense Obligatoria
1. **Inspección de Código y Prompts (`read_file`):**
   - Verifica en `dispatch.py` y los 6 prompts (`prompt_cta_architect.md`, `prompt_shard_author.md`, `prompt_repair.md` Full y Lean):
     - Umbral oficial `< 6` errores (`edit_file` obligatorio en `1..5` errores vs `cta_fixes`/`shard_fixes`/`write_file` en `>= 6` errores).
     - Eliminación del escape hatch `"o 1 tupla por competencia"` en `prompt_shard_author.md`, presencia de `[M3-ARCHETYPES]`, patrón compacto `_gen_h01(rng, arch)` + `gen_h01_1..4` + 4 tuplas en `TEMPLATES`.
     - Inclusión de `--min-archetypes 4` en `compile_cmd` y estampado de `"min_archetypes": 4` en `pre_shard_manifest.json` dentro de `dispatch_authors`.
     - Tamaño en bytes: `lean/prompt_shard_author.md <= 4,750` bytes y todos los `lean/*.md <= 5,000` bytes.
     - Que `subagent_types.json` NO haya sido modificado por Stream 1D.
2. **Ejecución Independiente de Pruebas (`run_command`):**
   - Ejecuta `.venv\Scripts\python.exe -m pytest tests/test_dispatch_turn0_and_milestone3_prompts.py tests/test_dispatch_scope.py tests/test_prompts_contract_alignment.py tests/test_c2c_v321_comp4_prompts.py -q` y verifica `100% PASS`.
3. **Handoff y Señal Final:**
   - Escribe `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1d_audit/handoff.md` y envía `PASS::` (o `FAIL::`) al Orquestador (`7d2e6386-9933-4c70-9e50-a3cf214925f6`).
