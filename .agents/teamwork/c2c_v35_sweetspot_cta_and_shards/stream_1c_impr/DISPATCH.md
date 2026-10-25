# DISPATCH — Stream 1C (Phase 2: Improver `impr_1c`)

## 1. Rol y Misión
Eres el **Mejorador (Phase 2 Improver)** del **Stream 1C (`c2c_hook_guard.py` + `tests/test_hook_post_pass_and_write_isolation.py`)** dentro de `/flash-triad-orchestrator`.
Debes leer primero:
1. `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1c_impl/BRIEFING.md`
2. `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1c_impl/handoff.md`

Tu misión es auditar y endurecer el código y las pruebas de `impl_1c` buscando edge cases sutiles en `c2c_hook_guard.py`.

## 2. Frontera Exclusiva de Escritura (100% Disjunta)
- **ARCHIVO DE PRODUCCIÓN PERMITIDO:**
  - `.agents/skills/content-to-course/c2c_hook_guard.py`
- **ARCHIVO DE TEST PERMITIDO:**
  - `tests/test_hook_post_pass_and_write_isolation.py`
- **ARCHIVO DE GOBERNANZA PERMITIDO:**
  - `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1c_impr/handoff.md`
- **PROHIBIDO TOCAR:** Cualquier otro archivo fuera de esta lista.

## 3. Requerimientos Técnicos de Endurecimiento (`impr_1c`)
1. **Revisión de Edge Cases en Regla C (`error_count` y `[M3-ARCHETYPES]`):**
   - ¿Qué ocurre si `compile_shard_XX.json` o `compile_cta_XX.json` tiene `error_count == 0` (por ejemplo, un estado residual o inicializado antes de fallar)? Verifica que si `error_count == 0` o `error_count is None`, caiga de forma segura al fallback legacy (`> 250` líneas deny, `<= 250` líneas allow) y no bloquee indebidamente la creación/escritura cuando no hay errores registrados.
   - ¿Qué ocurre cuando un shard de 1 o 2 competencias que emitió solo 1 arquetipo por competencia (~75–120 líneas) recibe `[M3-ARCHETYPES]` (`error_count` = 1 o 2 errores, es decir `< 6`)? Con `1 <= error_count < 6` y `>= 40` líneas, `c2c_hook_guard.py` bloquea `write_file` sobre `shard_XX_data.py` e instruye usar `edit_file` (`replace_file_content`) quirúrgico para insertar las tuplas faltantes en `TEMPLATES` o usar `shard_fixes/<CID>.py`. Verifica que el mensaje de denegación de Regla C sea ultra claro al respecto.
   - Verifica que en Windows las rutas con backslashes (`courses\c1\work\cta_fixes\H-01.py`, `courses\c1\work\cta_parts\part_01_data.py`) o relativas (`work/cta_fixes/H-01.py`) se normalicen a `/` antes de evaluar `Regla A`, `Regla B` y `Regla C`.
2. **Pruebas Adicionales en `tests/test_hook_post_pass_and_write_isolation.py`:**
   - Agrega tests para:
     - Rutas con backslashes de Windows (`courses\c1\work\cta_fixes\C-01.py`, `courses\c1\work\cta_parts\part_01_data.py`, `courses\c1\work\shards\shard_01_data.py`).
     - `error_count == 0` o JSON corrupto en `.check_attempts/compile_shard_01.json` (fallback seguro sin excepción no manejada).
     - Benchmark de latencia promedio `< 10 ms` sobre 50 invocaciones consecutivas de `evaluate_hook_payload`.

## 4. Verificación y Handoff
1. Ejecuta:
   `.venv\Scripts\python.exe -m pytest tests/test_hook_post_pass_and_write_isolation.py tests/test_watchdog_and_hooks.py -q`
2. Normaliza CRLF a LF en los archivos de tu frontera.
3. Escribe `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1c_impr/handoff.md` y envía `DONE::` al Orquestador (`7d2e6386-9933-4c70-9e50-a3cf214925f6`).
