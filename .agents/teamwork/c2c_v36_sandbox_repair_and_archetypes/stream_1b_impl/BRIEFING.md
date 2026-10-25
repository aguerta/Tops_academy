# Pre-Flight Sanity Check (Paso 0) — Stream 1B Implementer

## 1. Confirmación de Entorno y Fronteras de Escritura
- **Rol:** Implementador de Stream 1B (`impl_1b`)
- **Fronteras Exclusivas de Escritura (Archivos de producción):**
  1. `.agents/skills/content-to-course/engine/sandbox.py`
  2. `.agents/skills/content-to-course/check_templates.py`
  3. `tests/test_sandbox_gil_and_circuit_breaker.py`
- **Artefactos de Gobernanza:**
  - `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1b_impl/BRIEFING.md`
  - `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1b_impl/handoff.md`

## 2. Inspección de Código Fuente Real

### A. `.agents/skills/content-to-course/engine/sandbox.py`
- **`call_with_timeout` (líneas 398–446):**
  - Firma: `def call_with_timeout(func: Callable, args: tuple = (), kwargs: Optional[dict] = None, timeout: Optional[float] = 0.5, seed: Optional[int] = None, max_user_steps: int = 250_000) -> Any:`
  - Actualmente calcula `deadline = time.perf_counter() + float(timeout) if (timeout is not None and timeout > 0) else None` y en `_timeout_tracer` compara `time.perf_counter() > deadline`.
  - Confirmado: Se implementará reloj por hilo con `time.thread_time()` cuando `threading.active_count() > 1`, y `wall_limit = max(timeout * 4.0, 2.5)` para evitar timeouts espurios por contención de GIL, manteniendo semántica estricta en single-thread.
- **`execute_sandbox_batch` (líneas 535–589):**
  - Firma: `def execute_sandbox_batch(generate_py: str, seeds: List[int], cross_check_py: Optional[str] = None, timeout_per_item: float = 2.0, isolated: bool = False, use_subprocess: bool = False) -> List[Dict[str, Any]]:`
  - Actualmente valida AST y compila dentro de `run_code_in_env` para cada semilla (50 semillas x 2 códigos = 100 parses/compiles redundantes).
  - Confirmado: Se pre-compilarán `generate_py` y `cross_check_py` una sola vez antes del bucle de semillas, preservando el orden de evaluación, tipos de excepciones (`SandboxSecurityError`, `SyntaxError`, etc.) y formato de retorno.

### B. `.agents/skills/content-to-course/check_templates.py`
- **Dimensionamiento de hilos (línea 2941):**
  - Actual: `max_workers = min(16, (os.cpu_count() or 4) * 2, len(template_files))`
  - Confirmado: Reducir a `max_workers = min(4, os.cpu_count() or 4, len(template_files))` para reducir contención de GIL.
- **Seguimiento de errores por competencia y Circuit Breaker (líneas 2954–3226):**
  - Actual: `is_clean = (len(errors) == 0)` es global. En línea 3153, `for cid in processed_comp_ids:` evalúa `if is_clean:`, lo cual provoca que un fallo en una sola competencia incremente contadores de intentos en todas las competencias del curso, culminando en falsos `BUDGET HALT`.
  - Confirmado:
    1. Acumular `errors_by_comp: Dict[str, List[str]] = {}` por archivo y en validaciones posteriores (TPL-D3, TPL-VAR, etc.).
    2. Determinar `cid_is_clean = (len(cid_errs) == 0)` y calcular `cid_err_hash` por competencia.
    3. Condicionar el reseteo o incremento de intentos a nivel de cada competencia (`if cid_is_clean:`).

## 3. Estado del Pre-Flight
- Todos los archivos y firmas coinciden exactamente con la especificación de `DISPATCH.md`.
- No se detectan impedimentos ni dependencias fuera de la frontera exclusiva de escritura.
- Estado: **PRE-FLIGHT SANITY CHECK EXITOSO (SIN BLOQUEOS)**. Procediendo con Fase 1.
