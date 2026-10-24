# DISPATCH — Stream 1D (Fase 2: Mejorador `impr_1d`)

## 1. Rol y Frontera Exclusiva de Escritura (`Exclusive Write Boundaries`)
Eres el **Mejorador (Improver) del Stream 1D** bajo `/flash-triad-orchestrator`.
- **Carpeta de Gobernanza:** `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1d_impr/`
- **Archivos de Producción Permitidos (ÚNICOS que puedes modificar):**
  1. `.agents/skills/content-to-course/c2c_hook_guard.py`
  2. `tests/test_hook_post_pass_and_write_isolation.py`
- **Artefactos de Gobernanza Permitidos:**
  - `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1d_impr/BRIEFING.md`
  - `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1d_impr/handoff.md`

## 2. Instrucciones de Endurecimiento
1. Lee `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1d_impl/handoff.md`, `.agents/skills/content-to-course/c2c_hook_guard.py` y `tests/test_hook_post_pass_and_write_isolation.py`. Escribe `BRIEFING.md`.
2. Revisa y endurece casos borde en `c2c_hook_guard.py`:
   - Rutas Windows con backslashes `\` vs POSIX `/` y mayúsculas/minúsculas en `D:\...` vs `d:/...`.
   - Que `shard_fixes/<CID>.py` siempre esté permitido aun cuando exista `compile_<shard_id>.json` con intentos fallidos, y que editar `shard_fixes/<CID>.py` no sea bloqueado por la regla de `> 250` líneas de `<shard_id>_data.py`.
   - Que cuando `pass_<shard_id>.json` esté corrupto (JSON inválido) o tenga `"status": "FAIL"`, no bloquee la escritura (fail-open seguro ante archivo corrupto).
   - Latencia de ejecución `< 25 ms`.
3. Amplía `tests/test_hook_post_pass_and_write_isolation.py` con estos casos borde y ejecuta `.venv\Scripts\python.exe -m pytest tests/test_hook_post_pass_and_write_isolation.py tests/test_watchdog_and_hooks.py`.
4. Escribe `handoff.md` y envía `DONE:: Stream 1D Improver completado` a `526cfac0-d37b-49c9-bf09-00b5c520add2`.
