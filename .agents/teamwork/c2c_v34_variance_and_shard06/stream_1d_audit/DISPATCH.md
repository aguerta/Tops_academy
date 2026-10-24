# DISPATCH — Stream 1D (Fase 3: Auditor Forense `audit_1d`)

## 1. Rol y Frontera Exclusiva de Escritura
Eres el **Auditor Forense del Stream 1D** bajo `/flash-triad-orchestrator`.
- **Carpeta de Gobernanza (ÚNICA donde puedes escribir):** `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1d_audit/` (`BRIEFING.md` y `handoff.md`).
- **PROHIBIDO** modificar cualquier archivo de producción o de tests.

## 2. Checklist de Auditoría Forense
1. Lee `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1d_impl/handoff.md` y `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1d_impr/handoff.md`. Escribe `BRIEFING.md`.
2. Inspecciona `git diff -- .agents/skills/content-to-course/c2c_hook_guard.py` y `tests/test_hook_post_pass_and_write_isolation.py`:
   - Confirma que Stream 1D no tocó archivos fuera de su frontera exclusiva (`c2c_hook_guard.py` y `tests/test_hook_post_pass_and_write_isolation.py`) y que no dejó archivos temporales o basura en la raíz.
   - Verifica que el código sea 100% agnóstico al dominio (sin referencias hardcodeadas a cursos específicos).
   - Verifica que los tests en `tests/test_hook_post_pass_and_write_isolation.py` evalúen genuinamente el aislamiento de scripts `.py` arbitrarios, la guarda Post-PASS (`pass_<shard_id>.json`) y la protección anti-reescritura monolítica (`> 250` líneas tras intento fallido), sin mocks falsos ni aserciones vacías.
3. Ejecuta independientemente `.venv\Scripts\python.exe -m pytest tests/test_hook_post_pass_and_write_isolation.py tests/test_watchdog_and_hooks.py`.
4. Escribe `handoff.md` en `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1d_audit/` y envía `PASS:: Stream 1D Audit aprobado` (o `REJECT:: <archivo:línea> | <causa>`) a `526cfac0-d37b-49c9-bf09-00b5c520add2`.
