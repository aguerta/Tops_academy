# Handoff — Stream 1B (Fase 1: Implementador `impl_1b`)

## 1. Archivos Modificados y Creados
Todos los cambios están estrictamente dentro de las fronteras exclusivas de escritura (`Exclusive Write Boundaries`):

1. **`.agents/skills/content-to-course/engine/sandbox.py`**:
   - **`call_with_timeout`**: Incorporación de reloj de tiempo de CPU por hilo (`time.thread_time()`) y techo de pared generoso (`wall_limit = max(timeout * 4.0, 2.5)`) cuando hay múltiples hilos activos (`threading.active_count() > 1`). En ejecución monohilo (`threading.active_count() <= 1`), mantiene el comportamiento idéntico al milisegundo.
   - **`execute_sandbox_batch`**: Pre-compilación única de AST y bytecode (`validate_code_ast` + `compile`) tanto para `generate_py` como para `cross_check_py` una sola vez antes del bucle de 50 semillas, reduciendo de 100 compilaciones redundantes por plantilla a exactamente 1. Manejo diferido de errores de sintaxis y seguridad para preservar el orden y contratos de excepciones. Soporta alias `timeout_sec` y `timeout_per_item`.
   - **Alias de seguridad**: Definición de `SandboxSecurityError = SecurityViolationError`.

2. **`.agents/skills/content-to-course/check_templates.py`**:
   - **Dimensionamiento de hilos**: Reducción de `max_workers` de 16 a `min(4, os.cpu_count() or 4, len(template_files))` para mitigar contención del GIL en `sys.settrace`.
   - **Seguimiento de errores por competencia**: Introducción de `errors_by_comp: Dict[str, List[str]] = {}` para registrar fallos asociados quirúrgicamente a cada competencia (`cid`) en la validación de archivos, distractores TPL-D3, diversidad TPL-VAR y paridad de producción.
   - **Aislamiento en Circuit Breaker**: Evaluación de `cid_is_clean = (len(cid_errs) == 0)` y cálculo de huella `cid_err_hash` por competencia, sustituyendo la evaluación del booleano global `is_clean`. Las competencias sanas limpian su estado (`attempts = 0`) y jamás entran en `BUDGET HALT` por errores en competencias vecinas.

3. **`tests/test_sandbox_gil_and_circuit_breaker.py`**:
   - Suite completa con 6 tests unitarios verificando:
     - Pre-compilación AST en lote de 50 semillas.
     - Detección precisa de `SyntaxError`, `SandboxSecurityError` y `SandboxTimeoutError` (con bucle infinito real `while True: pass`).
     - Resiliencia ante contención de GIL en 16 hilos concurrentes con `timeout_sec=0.8` sin falsos timeouts.
     - Aislamiento del Circuit Breaker / Budget Halt en directorio multi-competencia (`C-01` y `C-02` sanas, `C-03` con error), confirmando que solo `C-03` sufre halt.

## 2. Resultados de Pruebas Automatizadas
Ejecución con `.venv\Scripts\python.exe -m pytest`:
- `tests/test_sandbox_gil_and_circuit_breaker.py`: **6 passed**
- `tests/test_sandbox_adversarial.py`: **49 passed**
- `tests/test_template_variability.py`: **5 passed**
- **Total:** **60 passed in 10.69s (100% green)**.

## 3. Estado de Entrega
Fase 1 (Implementador Stream 1B) finalizada con éxito sin bloqueos ni transgresión de fronteras.
Listo para revisión y mejoras de Fase 2 (Mejorador Stream 1B).
