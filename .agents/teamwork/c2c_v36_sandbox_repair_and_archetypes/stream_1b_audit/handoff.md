# Handoff de Auditoría Forense — Stream 1B (Fase 3: `audit_1b`)

## 1. Dictamen de Auditoría
- **Estado:** **PASS** (Stream 1B Aprobado)
- **Componentes Auditados:**
  - `.agents/skills/content-to-course/engine/sandbox.py` (líneas 400–705)
  - `.agents/skills/content-to-course/check_templates.py` (líneas 2936–3280)
  - `tests/test_sandbox_gil_and_circuit_breaker.py` (10 tests unitarios y adversarios)

## 2. Hallazgos Forenses y Verificación de Criterios

### A. Pre-compilación AST y Bytecode en Lotes (`execute_sandbox_batch`)
- **Implementación verificada:** `validate_code_ast` y `compile(..., "<sandbox>", "exec")` se invocan exactamente una sola vez antes de iterar sobre el conjunto de semillas (`generate_py` y `cross_check_py`).
- **Aislamiento de mutabilidad:** `copy.deepcopy(gen_res)` previene que mutaciones adversarias o involuntarias en la función `verify` del cross-check contaminen el diccionario `result["vars"]` o las salidas de semillas subsiguientes (verificado por `test_cross_check_mutation_isolation`).
- **Preservación de excepciones y orden:** Sintaxis inválida y violaciones de seguridad (`SandboxSecurityError` / `SecurityViolationError`) son detectadas y reportadas conforme al contrato de API sin enmascaramientos.

### B. Resiliencia ante Contención del GIL (`call_with_timeout`)
- **Mecanismo híbrido verificado:**
  - Cuando `threading.active_count() > 1` y existe `time.thread_time()`, el tracer mide el tiempo real de CPU consumido por el hilo específico, complementado con un techo de tiempo de pared generoso (`wall_limit = max(timeout * 4.0, 2.5)`).
  - En entornos monohilo (`threading.active_count() <= 1`), mantiene el reloj estricto de pared (`time.perf_counter()`).
- **Resistencia y precisión:** 16 hilos simultáneos procesan 15 semillas cada uno con `timeout_sec=0.8` sin ningún falso timeout por contención del GIL. Al mismo tiempo, bucles infinitos reales (`while True: pass`) dentro de pools multihilo son interceptados y terminados limpiamente con `SandboxTimeoutError` en tiempo < 3.0s (verificado por `test_16_concurrent_threads_no_false_timeouts` y `test_real_infinite_loop_under_thread_pool_executor_raises_timeout`).
- **Restauración del trace:** Bloque `finally` con manejo seguro anidado garantiza que `sys.settrace(prev_trace)` o `sys.settrace(None)` se restaure bajo cualquier circunstancia.

### C. Aislamiento del Circuit Breaker y Budget Halt por Competencia (`check_templates.py`)
- **Segregación de errores:** `errors_by_comp` registra errores vinculados de forma quirúrgica a cada `cid`.
- **Prevención de colisión de identificadores con prefijo compartido:** Se implementó coincidencia exacta por regex con delimitadores de palabra (`\b{re.escape(cid)}\b`), evitando que errores en competencias como `C-010` o `C-10` contaminen a `C-01` o `C-1` (verificado por `test_shared_prefix_id_non_collision`).
- **Evaluación independiente de estado:** Cada competencia evalúa su propio `cid_is_clean = (len(cid_errs) == 0)` y su huella SHA-256 (`cid_err_hash`).
- **Recuperación y limpieza atómica:** Cuando una competencia en halt se corrige y pasa limpiamente, su archivo de registro (`.check_attempts/<cid>.json` y variantes de shard) es eliminado atómicamente sin importar que competencias vecinas en el mismo lote fallen (verificado por `test_competency_recovery_clears_attempt_file_while_neighbor_fails`).

### D. Inspección de Tests (Ausencia de Falsos Positivos)
- Todos los tests en `tests/test_sandbox_gil_and_circuit_breaker.py` ejecutan código real contra el sandbox y el validador, comprobando estructuras de datos internas, excepciones lanzadas, contenido de archivos `.check_attempts` y mensajes de error formateados. No se detectaron aserciones vacías ni falsos positivos.

## 3. Evidencia de Ejecución Independiente
- `.venv\Scripts\python.exe -m pytest tests/test_sandbox_gil_and_circuit_breaker.py -v`:
  - **10 passed in 3.44s (100% green)**
- `.venv\Scripts\python.exe -m pytest tests/test_sandbox_gil_and_circuit_breaker.py tests/test_sandbox_adversarial.py tests/test_template_variability.py -q`:
  - **64 passed in 12.71s (100% green)**

## 4. Veredicto Final
**PASS:: Stream 1B Auditor aprobado**
