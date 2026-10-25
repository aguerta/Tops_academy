# DISPATCH — Stream 1B (Fase 2: Mejorador `impr_1b`)

## 1. Rol y Frontera Exclusiva de Escritura (`Exclusive Write Boundaries`)
Eres el **Mejorador (Fase 2) del Stream 1B** bajo `/flash-triad-orchestrator`.
- **Carpeta de Gobernanza:** `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1b_impr/`
- **Archivos de Producción Permitidos (ÚNICOS que puedes modificar):**
  1. `.agents/skills/content-to-course/engine/sandbox.py`
  2. `.agents/skills/content-to-course/check_templates.py`
  3. `tests/test_sandbox_gil_and_circuit_breaker.py`
- **Artefactos de Gobernanza Permitidos:**
  - `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1b_impr/BRIEFING.md`
  - `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1b_impr/handoff.md`
- **PROHIBIDO** editar cualquier otro archivo del repositorio. Nunca pases `ArtifactMetadata` a `write_file` o `edit_file`.

## 2. Paso 0 Obligatorio (*Pre-Flight*)
1. Lee `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1b_impl/handoff.md`, `.agents/skills/content-to-course/engine/sandbox.py` (líneas 400–620), `.agents/skills/content-to-course/check_templates.py` (líneas 2930–3230) y `tests/test_sandbox_gil_and_circuit_breaker.py`.
2. Escribe `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1b_impr/BRIEFING.md`.

## 3. Tareas de Endurecimiento (Hardening & Edge Cases)
1. En `engine/sandbox.py` (`execute_sandbox_batch` y `call_with_timeout`):
   - **Restauración segura de `sys.settrace`:** Asegúrate de que `sys.settrace(old_trace)` en el bloque `finally` de `call_with_timeout` jamás falle aunque `old_trace` sea `None`.
   - **Aislamiento de estado mutable entre semillas en `execute_sandbox_batch`:** Verifica que cuando el código pre-compilado (`gen_compiled`, `ver_compiled`) se ejecuta en cada semilla `s`, cada semilla reciba su propio `gen_env = build_sandbox_globals()` y `ver_env = build_sandbox_globals()` completamente fresco y que `copy.deepcopy(vars_dict)` (o paso de argumentos a `verify(vars_dict, ans_val)`) no permita que una mutación en `verify` contamine `result["vars"]` de esa semilla.
   - **Detección de `SandboxTimeoutError` dentro de un worker thread de `ThreadPoolExecutor`:** Asegúrate de que si una plantilla contiene un loop infinito real (`while True: pass`) y se ejecuta **dentro de un hilo de `ThreadPoolExecutor` mientras hay otros hilos vivos (`threading.active_count() > 1`)**, `call_with_timeout` dispare igualmente `SandboxTimeoutError` en `~timeout` segundos de CPU del hilo!
2. En `check_templates.py` (circuit breaker `BUDGET HALT` por competencia, líneas 3150–3230):
   - Verifica que cuando una competencia `cid` que estaba previamente en `halted: True` (después de 3 intentos fallidos) es corregida y pasa limpiamente (`cid_is_clean == True`), su archivo `.check_attempts/<cid>.json` se elimine por completo incluso si otra competencia vecina en el mismo directorio falló en esa misma corrida!
   - Verifica que los prefijos de IDs con números que son subcadenas de otros (ej. `C-1` vs `C-10`, o `C-01` vs `C-010`) no se confundan al asociar errores globales a `errors_by_comp[cid]` (usa regex con frontera `\b` o coincidencia exacta de delimitadores `'{cid}'`, `[{cid}]`, `/{cid}.json`).
3. Amplía `tests/test_sandbox_gil_and_circuit_breaker.py` con tests adversarios para:
   - Un loop infinito real (`while True: pass`) ejecutándose dentro de un `ThreadPoolExecutor` con otros hilos activos (`threading.active_count() > 1`), comprobando que sí lanza `SandboxTimeoutError`.
   - Recuperación individual de una competencia que estaba en `BUDGET HALT` (`C-03` corregida en el intento 4 mientras `C-02` falla por primera vez), verificando que `C-03` salga de `BUDGET HALT` y elimine su `.check_attempts/C-03.json`.
   - No-colisión de IDs con prefijo compartido (`C-01` sana vs `C-010` con error).
4. Ejecuta `.venv\Scripts\python.exe -m pytest tests/test_sandbox_gil_and_circuit_breaker.py tests/test_check_templates.py tests/test_sandbox.py -q`.
5. Escribe `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1b_impr/handoff.md` y envía `DONE:: Stream 1B Improver completado` a `d603756a-7e58-4466-b883-cbc391586154`.
