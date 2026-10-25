# BRIEFING — Stream 1B (Fase 2: Mejorador `impr_1b`)

## 1. Diagnóstico del Estado Inicial (Post-Fase 1 Implementador)
- **Implementación base:** El Implementador (`impl_1b`) completó la AST pre-compilación en `execute_sandbox_batch`, la reducción de concurrencia a `min(4, os.cpu_count() or 4, len(template_files))` en `check_templates.py`, y la inicialización de `errors_by_comp` y `cid_is_clean` para aislar el Circuit Breaker / Budget Halt.
- **Suite de pruebas actual:** `tests/test_sandbox_gil_and_circuit_breaker.py` cuenta con 6 tests unitarios pasando en verde (60 tests pasando en total junto a `test_sandbox_adversarial.py` y `test_template_variability.py`).

## 2. Puntos Críticos y Casos Borde Identificados para Endurecimiento
1. **Seguridad y robustez en restauración de trace (`call_with_timeout`):**
   - El bloque `finally` de `call_with_timeout` debe restaurar `sys.settrace(prev_trace)` de manera infalible mediante bloque `try ... except ...`, cayendo a `sys.settrace(None)` si ocurriera cualquier excepción inesperada.
2. **Inmutabilidad y aislamiento de estado en `execute_sandbox_batch` y `execute_template_code`:**
   - Si `cross_check_py` (`verify(gen_res)`) muta su argumento de entrada (por ejemplo modificando `gen_res["vars"]` o limpiando listas), la contaminación se propaga al resultado final devuelto en el lote. Se debe introducir copia profunda (`copy.deepcopy(gen_res)`) antes de invocar la verificación, garantizando que `result["vars"]` de cada semilla sea 100% fiel e inmutable.
   - Cada semilla debe mantener su entorno fresco (`build_sandbox_globals()`).
3. **Detección de `SandboxTimeoutError` bajo concurrencia de hilos (`ThreadPoolExecutor`):**
   - Cuando un bucle infinito real (`while True: pass`) se ejecuta en un worker thread dentro de un pool concurrente (`threading.active_count() > 1`), el reloj de tiempo de CPU por hilo (`time.thread_time()`) y el techo de pared (`wall_limit`) deben asegurar la interrupción precisa con `SandboxTimeoutError` sin depender de timers globales que pudieran ser afectados por hilos durmientes o contención.
4. **Desconexión e independencia de IDs con prefijos compartidos (`check_templates.py`):**
   - En la asociación de errores globales a competencias (`errors_by_comp`), las comprobaciones simples como `f"Competency {cid}" in err` causan falsos positivos cuando un ID es subcadena de otro (ej. `C-01` coincide erróneamente en `Competency C-010 failed` o `C-1` en `C-10`).
   - Se reemplazará la búsqueda laxa por coincidencia exacta con fronteras de palabra regex (`\b{re.escape(cid)}\b`) y delimitadores estrictos (`'{cid}'`, `"{cid}"`, `[{cid}]`, `/{cid}.json`).
5. **Limpieza completa y recuperación tras `BUDGET HALT`:**
   - Cuando una competencia `cid` previamente en `halted: True` es corregida y pasa limpiamente (`cid_is_clean == True`), su archivo `.check_attempts/<cid>.json` debe ser completamente eliminado incluso cuando competencias vecinas en el mismo directorio continúen fallando en esa misma corrida.

## 3. Plan de Acción y Frontera Exclusiva de Escritura
- Modificar exclusivamente:
  1. `.agents/skills/content-to-course/engine/sandbox.py`
  2. `.agents/skills/content-to-course/check_templates.py`
  3. `tests/test_sandbox_gil_and_circuit_breaker.py`
- Agregar tests unitarios adversarios para:
  - Bucle infinito en `ThreadPoolExecutor` con hilos activos concurrentes.
  - Recuperación de competencia corregida tras `BUDGET HALT` con fallo simultáneo de competencia vecina.
  - No colisión de IDs con prefijos comunes (`C-01` vs `C-010`, `C-1` vs `C-10`).
  - Inmutabilidad de `gen_res` frente a mutaciones en `verify`.
- Ejecutar verificación mediante `.venv\Scripts\python.exe -m pytest tests/test_sandbox_gil_and_circuit_breaker.py tests/test_sandbox_adversarial.py tests/test_template_variability.py -q`.
- Generar `handoff.md` y notificar al orquestador.
