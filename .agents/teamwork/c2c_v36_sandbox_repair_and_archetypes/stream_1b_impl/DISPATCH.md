# DISPATCH — Stream 1B (Fase 1: Implementador `impl_1b`)

## 1. Rol y Frontera Exclusiva de Escritura (`Exclusive Write Boundaries`)
Eres el **Implementador del Stream 1B** bajo `/flash-triad-orchestrator`.
- **Carpeta de Gobernanza:** `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1b_impl/`
- **Archivos de Producción Permitidos (ÚNICOS que puedes modificar):**
  1. `.agents/skills/content-to-course/engine/sandbox.py`
  2. `.agents/skills/content-to-course/check_templates.py`
  3. `tests/test_sandbox_gil_and_circuit_breaker.py`
- **Artefactos de Gobernanza Permitidos:**
  - `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1b_impl/BRIEFING.md`
  - `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1b_impl/handoff.md`
- **PROHIBIDO** editar cualquier otro archivo del repositorio. Nunca pases `ArtifactMetadata` a `write_file` o `edit_file`.

## 2. Paso 0 Obligatorio (*Pre-Flight Sanity Check*)
Antes de realizar cualquier edición:
1. Lee `.agents/skills/content-to-course/engine/sandbox.py` (líneas 400–600) y `.agents/skills/content-to-course/check_templates.py` (líneas 2930–3230).
2. Escribe `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1b_impl/BRIEFING.md` confirmando líneas y firmas reales. Si detectas un bloqueo fuera de tu frontera, detén ediciones y envía `BLOCKER:: <archivo:línea> | <causa> | <opciones>` al Orquestador (`d603756a-7e58-4466-b883-cbc391586154`).

## 3. Especificación Técnica de Implementación

### A. Pre-compilación AST/Bytecode en `execute_sandbox_batch` y Reloj de CPU por Hilo en `call_with_timeout` (`engine/sandbox.py`)
1. **Problema Raíz #1 (`execute_sandbox_batch`, líneas 535–589):**
   - Actualmente `execute_sandbox_batch` llama a `run_code_in_env` dos veces por cada semilla (`50 semillas × 2 = 100 veces por plantilla`), ejecutando `validate_code_ast(code_str)` (`ast.parse` + recorrido completo del AST) y `compile(code_str, "<sandbox>", "exec")` **100 veces sobre exactamente el mismo código fuente**, saturando el GIL cuando se validan 25 competencias.
   - **Solución en `execute_sandbox_batch`:**
     - Mantén `run_code_in_env` intacto para sus llamadores directos.
     - En `execute_sandbox_batch(generate_code, verify_code, seeds, timeout_sec=0.8)`:
       1. Si `not seeds`: retorna `[]`.
       2. Valida y compila `generate_code` **una sola vez antes del bucle**:
          - Ejecuta `validate_code_ast(generate_code)` (que lanza `SandboxSecurityError` si hay violaciones de seguridad AST, exactamente igual que antes; si ocurre `SyntaxError`, retorna `[{"seed": seeds[0], "ok": False, "error": f"SyntaxError: {e}", "stage": "generate"}]`).
          - Ejecuta `gen_compiled = compile(generate_code, "<sandbox>", "exec")` (capturando `SyntaxError` igual).
       3. Valida y compila `verify_code` **una sola vez antes del bucle**:
          - Si `validate_code_ast(verify_code)` lanza `SyntaxError` o `compile(verify_code, ...)` lanza `SyntaxError`, no falles antes de correr `generate` en la primera semilla (o guárdalo como `ver_syntax_err` para reportarlo en `"stage": "verify"` después de que `generate` corra en `seeds[0]`, preservando al 100% el orden de evaluación y el formato de error de `run_code_in_env`!). Nota: si `validate_code_ast(verify_code)` lanza `SandboxSecurityError`, ejecútalo cuando llegue al paso `verify` de la primera semilla (o antes si no rompe ningún test).
       4. Dentro del bucle `for s in seeds:`, crea un entorno limpio `gen_env = build_sandbox_globals()`, ejecuta `exec(gen_compiled, gen_env)` y `gen_fn(s)` usando `call_with_timeout(..., timeout=timeout_sec)`, y haz lo mismo para `ver_compiled` / `ver_fn(vars_dict, ans_val)`, manteniendo idénticos todos los mensajes de error (`SandboxError`, `SandboxTimeoutError`, `SandboxSecurityError`, etc.).
2. **Problema Raíz #2 (`call_with_timeout`, líneas 406–445):**
   - `deadline = time.perf_counter() + timeout` mide tiempo de pared (wall-clock). Cuando `ThreadPoolExecutor` corre múltiples hilos con `sys.settrace` activo, un hilo que cede el GIL mientras otros hilos compilan o recolectan basura acumula `> 0.8s` de reloj de pared habiendo consumido apenas `~15 ms` de CPU real, disparando falsos `SandboxTimeoutError`.
   - **Solución en `call_with_timeout`:**
     - Usa `has_thread_time = hasattr(time, "thread_time")`.
     - Calcula `cpu_start = time.thread_time()` (si está disponible) y `wall_start = time.perf_counter()`.
     - Define un techo de pared generoso contra bloqueos no-CPU: `wall_limit = max(timeout * 4.0, 2.5)` si hay múltiples hilos activos (`threading.active_count() > 1`), o `timeout` cuando corre en un solo hilo (`threading.active_count() <= 1`).
     - En `_timeout_tracer(frame, event, arg)`:
       - Si `threading.active_count() > 1` y `has_thread_time`: dispara `SandboxTimeoutError(f"Template execution timed out after {timeout}s")` solo si `(time.thread_time() - cpu_start) > timeout` o `(time.perf_counter() - wall_start) > wall_limit`.
       - Si `threading.active_count() <= 1`: dispara `SandboxTimeoutError(f"Template execution timed out after {timeout}s")` si `(time.perf_counter() - wall_start) > timeout`.
     - De esta forma, en ejecución single-thread (y en todos los tests unitarios existentes) el comportamiento de `timeout` es 100% idéntico al milisegundo, mientras que bajo `ThreadPoolExecutor` (`threading.active_count() > 1`) la espera del GIL jamás cuenta como tiempo de CPU consumido por la plantilla!

### B. Dimensionamiento del Pool de Hilos y Corrección del Bug `is_clean` en `BUDGET HALT` (`check_templates.py`)
1. **Dimensionamiento de `ThreadPoolExecutor` (`check_templates.py:2940-2942`):**
   - Cambia `max_workers = min(16, (os.cpu_count() or 4) * 2, len(template_files))` a `max_workers = min(4, os.cpu_count() or 4, len(template_files))` para evitar contención extrema de `sys.settrace` en el GIL al validar directorios de 25+ archivos.
2. **Bug del Booleano Global `is_clean` en el Circuit-Breaker por Competencia (`check_templates.py:2940-2980, 3153-3221`):**
   - **Problema:** En la línea 3153, `for cid in processed_comp_ids:` evalúa `if is_clean:`, donde `is_clean = (len(errors) == 0)` es el booleano **global de todo el directorio**. Cuando una sola competencia (`C-11`) fallaba al validar `work/templates/`, `check_templates.py` incrementaba `attempts` en `.check_attempts/<cid>.json` para **las 25 competencias del curso**, causando falsos `[!] BUDGET HALT` en competencias 100% sanas a la 3ra corrida!
   - **Solución:**
     - Lleva un diccionario `errors_by_comp: Dict[str, List[str]] = {}` durante la validación de archivos (líneas 2954–2978): cuando `_validate_single_template_file` retorna `(file_errs, comp_id, ref_dids, tpls)`, si `comp_id` existe y `file_errs` no está vacío, registra `errors_by_comp.setdefault(comp_id, []).extend(file_errs)`.
     - Adicionalmente, para cualquier error global agregado después (entre líneas 2980 y 3120, ej. distractores huérfanos o `[M3-ARCHETYPES]`), si el texto del error menciona a `cid` (ej. `f"'{cid}'" in err` o `f" {cid} " in err` o `f"[{cid}]" in err` o `f"/{cid}.json" in err.replace("\\", "/")` o `f"Competency {cid}" in err`), asócialo también a `errors_by_comp.setdefault(cid, []).append(err)`. (Si `len(processed_comp_ids) == 1` y `errors` no está vacío, asocia `errors` a ese único `cid`).
     - En el bucle `for cid in processed_comp_ids:` (línea 3153):
       - Define `cid_errs = errors_by_comp.get(cid, [])` y `cid_is_clean = (len(cid_errs) == 0)`.
       - Calcula `cid_err_hash` a partir de `cid_errs` (en lugar del `err_hash` global, o usa `err_hash` cuando `len(processed_comp_ids) == 1`).
       - Reemplaza `if is_clean:` (línea 3195) por `if cid_is_clean:`! Así, toda competencia `cid` sin errores propios limpia su archivo `f_att` (`attempts = 0`) y jamás sufre `BUDGET HALT` por culpa de otra competencia vecina!

## 4. Verificación y Entrega
1. Crea `tests/test_sandbox_gil_and_circuit_breaker.py` con tests unitarios que verifiquen:
   - Que `execute_sandbox_batch` pre-compila el código y ejecuta 50 semillas limpiamente, manteniendo detección exacta de `SyntaxError`, `SandboxSecurityError` y `SandboxTimeoutError` (con un loop infinito real `while True: pass`).
   - Que al ejecutar 16 hilos concurrentes en `ThreadPoolExecutor` invocando `execute_sandbox_batch` sobre plantillas válidas con `timeout_sec=0.8`, **ninguna** lanza falso `SandboxTimeoutError`.
   - Que al validar un directorio con 3 competencias (`C-01` sana, `C-02` sana, `C-03` con error) 3 veces seguidas mediante `check_templates_file_or_dir`, **únicamente `C-03`** incrementa `.check_attempts/C-03.json` y entra en `BUDGET HALT`, mientras que `C-01` y `C-02` permanecen limpias (`0` errores de `BUDGET HALT` para `C-01` y `C-02`).
2. Ejecuta `.venv\Scripts\python.exe -m pytest tests/test_sandbox_gil_and_circuit_breaker.py tests/test_check_templates.py tests/test_sandbox.py -q`.
3. Escribe `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1b_impl/handoff.md` y envía `DONE:: Stream 1B Implementer completado` a `d603756a-7e58-4466-b883-cbc391586154`.
