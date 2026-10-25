# DISPATCH — Stream 2A (Gate 2, Phase 1: Integrator Implementer `impl_2a`)

## 1. Rol y Frontera Exclusiva de Escritura (`Exclusive Write Boundaries`)
Eres el **Implementador de Integración del Stream 2A (Gate 2)** bajo `/flash-triad-orchestrator`.
- **Carpeta de Gobernanza:** `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_2a_impl/`
- **Archivos de Producción y Test Permitidos (ÚNICOS que puedes modificar):**
  1. `.agents/skills/content-to-course/subagent_types.json`
  2. `tests/test_sweetspot_v35_cta_and_shards.py` *(nueva suite integral End-to-End de contrato cruzado v3.5)*
- **Artefactos de Gobernanza Permitidos:**
  - `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_2a_impl/BRIEFING.md`
  - `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_2a_impl/handoff.md`
- **PROHIBIDO** editar cualquier archivo de los Streams 1A, 1B, 1C o 1D. Nunca pases `ArtifactMetadata` a `write_file` o `edit_file`.

## 2. Paso 0 Obligatorio (*Pre-Flight Sanity Check*)
1. Lee los handoffs de los 4 streams de Gate 1 (`stream_1{a,b,c,d}_audit/handoff.md`) y verifica cómo quedó `.agents/skills/content-to-course/system_prompts/lean/*.md` frente a `.agents/skills/content-to-course/subagent_types.json`.
2. Escribe `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_2a_impl/BRIEFING.md`.

## 3. Requerimientos Técnicos Exactos

### A. Sincronización de `.agents/skills/content-to-course/subagent_types.json`
- Sincroniza `subagent_types.json` con los archivos actualizados en `.agents/skills/content-to-course/system_prompts/lean/` (puedes ejecutar o verificar la lógica de sincronización de `subagent_types.json` con `lean/prompt_cta_architect.md`, `lean/prompt_shard_author.md`, `lean/prompt_repair.md`, o revisar cómo `test_prompts_contract_alignment.py` valida `subagent_types.json`).
- Asegúrate de que todos los tests de alineación de `subagent_types.json` (`tests/test_prompts_contract_alignment.py`, `tests/test_c2c_v321_comp4_prompts.py`, `tests/test_dispatch_turn0_and_milestone3_prompts.py`) pasen al 100%.

### B. Nueva Suite Integral End-to-End `tests/test_sweetspot_v35_cta_and_shards.py`
Crea `tests/test_sweetspot_v35_cta_and_shards.py` validando la integración cruzada de los 4 componentes (Streams 1A + 1B + 1C + 1D):
1. **Integración CTA (`compile_cta.py` + `c2c_hook_guard.py`):**
   - Tier-0 Auto-Heal de las expresiones LaTeX huérfanas de `v5` (`\lim_{n\to\infty}`, `\frac{\sigma^2}{n}`, `\sigma`) pasa con `0` errores y genera `pass_cta_<id>.json`, tras lo cual `c2c_hook_guard.py` (Regla B) bloquea cualquier `write_file` o `edit_file` posterior sobre `part_01_data.py`.
   - Cuando `compile_cta.py` falla con `1 <= error_count < 6` (ej. 3 errores estructurales), graba `error_count: 3` en `.check_attempts/compile_cta_part_01.json`, emite `[UMBRAL OFICIAL < 6 ERRORES (3/5)]`, y `c2c_hook_guard.py` (Regla C) bloquea `write_file` sobre `part_01_data.py` mientras permite `edit_file` o `write_file` en `cta_fixes/<CID>.py`.
   - Cuando `compile_cta.py` falla con `error_count >= 6`, `c2c_hook_guard.py` permite `write_file` sobre `part_01_data.py`.
2. **Integración Shards (`compile_shard.py` + `c2c_hook_guard.py` + `dispatch.py`):**
   - `dispatch_authors` estampa `"min_archetypes": 4` en `pre_shard_manifest.json` e incluye `--min-archetypes 4` en `compile_cmd`.
   - Cuando un shard emite solo 1 tupla por competencia (como `shard_09_data.py` en `v5`), `compile_shard.py` falla con `[M3-ARCHETYPES]`, graba `error_count` (`< 6`) en `.check_attempts/compile_shard_09.json`, y `c2c_hook_guard.py` bloquea `write_file` completo e instruye usar `edit_file` para insertar las tuplas faltantes o `shard_fixes/<CID>.py`.
   - Cuando el shard usa el patrón compacto (`def _gen_c06(rng, arch):` + `gen_c06_1..4` + 4 tuplas de 9 elementos), `compile_shard.py` aprueba con `[+] PASS`, escribe `pass_shard_09.json`, y `c2c_hook_guard.py` bloquea ediciones posteriores (Regla B).

## 4. Verificación y Entrega
1. Ejecuta:
   `.venv\Scripts\python.exe -m pytest tests/test_sweetspot_v35_cta_and_shards.py tests/test_cta_sweetspot_and_autoheal.py tests/test_shard06_and_dry_archetypes.py tests/test_hook_post_pass_and_write_isolation.py tests/test_dispatch_turn0_and_milestone3_prompts.py tests/test_prompts_contract_alignment.py -q`
2. Normaliza CRLF a LF en `subagent_types.json` y `tests/test_sweetspot_v35_cta_and_shards.py`.
3. Escribe `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_2a_impl/handoff.md` y envía `DONE::` al Orquestador (`7d2e6386-9933-4c70-9e50-a3cf214925f6`).
