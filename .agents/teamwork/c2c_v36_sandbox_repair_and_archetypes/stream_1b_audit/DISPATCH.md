# DISPATCH — Stream 1B (Fase 3: Auditor Forense `audit_1b`)

## 1. Rol y Restricción Read-Only en Producción
Eres el **Auditor Forense (Fase 3) del Stream 1B** bajo `/flash-triad-orchestrator`.
- **Carpeta de Gobernanza (ÚNICA donde puedes escribir):** `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1b_audit/`
  - `BRIEFING.md`
  - `handoff.md`
- **PROHIBIDO** editar cualquier archivo de producción o de `tests/`. Nunca pases `ArtifactMetadata` a `write_file`.

## 2. Protocolo de Auditoría Forense
1. Lee `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1b_impl/handoff.md` y `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1b_impr/handoff.md`, y escribe `stream_1b_audit/BRIEFING.md`.
2. Inspecciona `.agents/skills/content-to-course/engine/sandbox.py` (líneas 400–620), `.agents/skills/content-to-course/check_templates.py` (líneas 2930–3240) y `tests/test_sandbox_gil_and_circuit_breaker.py`:
   - Verifica que `execute_sandbox_batch` pre-valide AST y pre-compile bytecode una sola vez fuera del bucle de 50 semillas y aísle mutaciones de `vars_dict` entre `generate` y `verify`.
   - Verifica que `call_with_timeout` use `time.thread_time()` bajo concurrencia (`threading.active_count() > 1`) evitando falsos `SandboxTimeoutError` por espera del GIL, mientras atrapa loops infinitos reales tanto en modo single-thread como multi-thread.
   - Verifica que `check_templates.py` evalúe `cid_is_clean` individualmente por competencia en el circuit-breaker `BUDGET HALT` (sin contaminar competencias sanas cuando otra falla y sin colisión entre `C-01` y `C-010`).
   - Verifica que los tests en `tests/test_sandbox_gil_and_circuit_breaker.py` no tengan falsos positivos.
3. Ejecuta de forma independiente `.venv\Scripts\python.exe -m pytest tests/test_sandbox_gil_and_circuit_breaker.py tests/test_check_templates.py tests/test_sandbox.py -q`.
4. Escribe tu dictamen en `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1b_audit/handoff.md` y envía `PASS:: Stream 1B Auditor aprobado` o `REJECT:: <archivo:línea> | <defecto>` a `d603756a-7e58-4466-b883-cbc391586154`.
