# Handoff — Stream 1B (Fase 2: Mejorador `impr_1b`)

## 1. Endurecimientos y Mitigaciones Implementadas

Todas las modificaciones se mantuvieron estrictamente dentro de la **Frontera Exclusiva de Escritura** (`Exclusive Write Boundaries`):

1. **`engine/sandbox.py`**:
   - **Restauración a prueba de fallos de `sys.settrace`:** En el bloque `finally` de `call_with_timeout`, se añadió captura de excepciones anidada (`try: sys.settrace(prev_trace) except Exception: try: sys.settrace(None)`), garantizando que el trace siempre se restaura limpiamente sin importar el estado de `prev_trace`.
   - **Aislamiento de mutabilidad entre etapas y semillas:** En `execute_template_code`, `execute_verifier_code` y `execute_sandbox_batch`, se aplica `copy.deepcopy(gen_res)` antes de pasar los resultados a la función `verify` de `cross_check_py`. Esto impide que cualquier mutación maliciosa o accidental en `verify` contamine el diccionario `result["vars"]` o las salidas de semillas subsiguientes.
   - **Detección robusta de `SandboxTimeoutError` en hilos de `ThreadPoolExecutor`:** Concurrencia evaluada con reloj por hilo `time.thread_time()` y techo `wall_limit` cuando `threading.active_count() > 1`. Los bucles infinitos en worker threads son cancelados limpiamente en `~timeout` segundos de CPU del hilo.

2. **`check_templates.py`**:
   - **Eliminación de colisión de prefijos compartidos (`C-01` vs `C-010`, `C-1` vs `C-10`):** Se reemplazó la búsqueda abierta de subcadenas (`f"Competency {cid}" in err`) por coincidencia exacta basada en fronteras de palabra regex (`\b{re.escape(cid)}\b`) y delimitadores estrictos (`'{cid}'`, `"{cid}"`, `[{cid}]`, `/{cid}.json`). Ningún error de `C-010` o `C-10` se atribuye a `C-01` o `C-1`.
   - **Limpieza atómica en recuperación de `BUDGET HALT`:** Cuando una competencia previamente en halt (`halted: True`, 3 intentos) pasa limpiamente (`cid_is_clean == True`), su archivo `.check_attempts/<cid>.json` (y cualquier variante con prefijo shard) se elimina por completo de forma aislada, incluso cuando competencias vecinas en el mismo directorio fallan en esa misma corrida.

3. **`tests/test_sandbox_gil_and_circuit_breaker.py`**:
   - Se amplió la suite con 4 nuevos tests adversarios de alta exigencia:
     1. `test_cross_check_mutation_isolation`: Verifica que mutaciones agresivas en `verify` sobre `res["vars"]` no contaminen la salida serializada del sandbox.
     2. `test_real_infinite_loop_under_thread_pool_executor_raises_timeout`: Verifica la interrupción precisa con `SandboxTimeoutError` de un bucle `while True: pass` dentro de un pool multihilo con hilos activos concurrentes.
     3. `test_competency_recovery_clears_attempt_file_while_neighbor_fails`: Simula 3 fallos de `C-03` hasta `BUDGET HALT`, y en el intento 4 corrige `C-03` mientras `C-02` falla. Comprueba la eliminación total de `C-03.json` y la correcta asignación del primer intento a `C-02`.
     4. `test_shared_prefix_id_non_collision`: Evalúa `C-01` (sana) y `C-010` (con fallo) durante 3 ciclos de halt; garantiza que `C-01` nunca genere archivo de intento ni reciba falsos halts.

## 2. Resultados de Verificación Automatizada

- **`tests/test_sandbox_gil_and_circuit_breaker.py`**: 10 tests pasados (**100% green** en 3.47s).
- **Suite combinada (`test_sandbox_gil_and_circuit_breaker.py` + `test_sandbox_adversarial.py` + `test_template_variability.py`)**:
  - **64 passed in 12.17s** (0 fallos, 0 warnings).
- **Pruebas de regresión adicionales:**
  - `tests/test_engine_invariants_adversarial.py`: 53 passed in 1.06s.
  - `tests/test_shard06_and_dry_archetypes.py`: 21 passed in 7.36s.

## 3. Estado de Entrega
Fase 2 (Mejorador Stream 1B) completada exitosamente sin bloqueos ni transgresión de fronteras. Listo para auditoría de Fase 3 (Auditor Stream 1B).
