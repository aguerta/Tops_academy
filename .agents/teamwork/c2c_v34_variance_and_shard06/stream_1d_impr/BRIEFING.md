# BRIEFING — Stream 1D (Fase 2: Mejorador `impr_1d`)

**Fecha:** 2026-10-24  
**Agente:** `impr_1d` (Mejorador Stream 1D)  
**Supervisor / Orquestador:** `526cfac0-d37b-49c9-bf09-00b5c520add2`  

---

## 1. Inspección de Cambios del Implementador (`impl_1d`)

El Implementador `impl_1d` incorporó en `.agents/skills/content-to-course/c2c_hook_guard.py` tres reglas de defensa en el ciclo de vida del subagente worker:
1. **Regla A (Worker Python write path isolation):** Bloquea la creación/edición de scripts `.py` no autorizados (ej. `test_debug.py`, scripts sueltos en el root o en `shards/`) fuera de los contratos autorizados (`work/shards/<shard_id>_data.py`, `work/shards/shard_fixes/<CID>.py`, `build_<shard_id>.py`, `cta/part_*.py`, `cta_data.py`, `work_append/`, `scratch/`).
2. **Regla B (Early cut post-PASS):** Bloquea escrituras/ediciones sobre `<shard_id>_data.py` una vez que `.check_attempts/pass_<shard_id>.json` registra `"status": "PASS"`.
3. **Regla C (Anti-monolithic rewrite guard):** Bloquea sobreescritura completa (`write_file`) cuando `<shard_id>_data.py` ya existe con `> 250` líneas y hay registro de fallos en `.check_attempts/compile_<shard_id>.json`, orientando a `edit_file` o overrides en `shard_fixes/<CID>.py`.

Estado de la suite de tests (`tests/test_hook_post_pass_and_write_isolation.py` + `tests/test_watchdog_and_hooks.py`):
- 37 tests ejecutados y pasando (0 fallos) en 0.93 segundos.

---

## 2. Puntos Críticos a Endurecer (Gap Analysis & Hardening Plan)

En base al análisis del código y los requisitos de `DISPATCH.md`:

1. **Rutas Windows con backslashes `\` vs POSIX `/` y casing (`D:\...` vs `d:/...` vs `./...`):**
   - En `_normalize_path(p)`: se reemplazan `\` por `/` y se elimina `./`, pero no normaliza mayúsculas/minúsculas ni resuelve paths absolutos que incluyan drive letters en mayúsculas (`D:` vs `d:`) cuando se usan expresiones regulares sensibles a mayúsculas/minúsculas o rutas relativas frente a absolutas.
   - En `WORKER_AUTHORIZED_PYTHON_PATTERNS` y `SHARD_DATA_PATTERN`:
     `SHARD_DATA_PATTERN = re.compile(r"(?:^|/)(?:.*/)?shards/([a-zA-Z0-9_-]+)_data\.py$", re.IGNORECASE)`
     Si la ruta es `D:\path\to\shards\shard_fixes\Hab-01.py`, `SHARD_DATA_PATTERN` no hace match, pero debemos asegurar que nunca colisione con subcarpetas bajo `shards/` como `shards/shard_fixes/shard_01_data.py` o similares.
   - En la resolución de `target_file_on_disk` y `candidate_dirs`:
     Actualmente se usan:
     `p_parent_2 = Path(norm_target).parent.parent`
     Si `norm_target` es una ruta relativa como `courses/demo/work/shards/shard_01_data.py`, `Path(norm_target).parent.parent` es `courses/demo/work`. Pero si `norm_target` es absoluta de Windows (`D:/Augusto/...`), `Path(norm_target)` puede comportarse de manera diferente si tiene drive letter o no. Se debe garantizar que la inspección de archivos no lance excepciones y resuelva de forma canónica tanto rutas absolutas Windows (`D:\...`, `d:\...`), rutas POSIX (`/d/...`), como rutas relativas (`courses/...`, `work/...`).

2. **Garantía estricta para `shard_fixes/<CID>.py`:**
   - La escritura y edición en `shard_fixes/<CID>.py` debe ser permitida incondicionalmente, incluso cuando exista `compile_<shard_id>.json` con intentos fallidos y múltiples errores acumulados.
   - La regla C de `> 250` líneas sólo aplica a `<shard_id>_data.py` y JAMÁS debe bloquear la creación o sobreescritura de `shard_fixes/<CID>.py`, ni siquiera si el fix supera 250 líneas (por ejemplo un test case extenso o diccionario grande).
   - Verificaremos que ningún regex ni condición en Regla C intercepte archivos en `shard_fixes/`.

3. **Manejo de archivos `pass_<shard_id>.json` corruptos o con `status != "PASS"`:**
   - Fail-open seguro: si `pass_<shard_id>.json` tiene JSON sintácticamente inválido, byte order marks corruptos, archivo truncado a 0 bytes, o permisos restringidos, el hook debe ignorar el error silenciosamente (fail-open) y permitir la edición, para no trabar al subagente.
   - Si `"status"` es `"FAIL"`, `"IN_PROGRESS"` o cualquier otro valor, debe permitir inmediatamente la escritura.

4. **Presupuesto de latencia (< 25 ms):**
   - Asegurar que no se hagan lecturas repetidas o redundantes en disco, y que el benchmarking de `process_hook` mantenga latencias medias < 5 ms por llamada (máx < 25 ms).
   - Minimizar chequeos `Path.is_file()` redundantes agrupándolos o podando paths inexistentes tempranamente.

5. **Ampliación de Tests Unitarios:**
   - Crear tests de adversarial testing en `tests/test_hook_post_pass_and_write_isolation.py` para:
     a) Rutas Windows con `D:\`, `d:\`, `\\`, dobles slashes, y espacios.
     b) `shard_fixes/<CID>.py` con > 250 líneas cuando `compile_<shard_id>.json` tiene 10 fallos previos (debe permitir).
     c) `pass_<shard_id>.json` corrupto (0 bytes, json corrupto `{"status": `, caracteres binarios).
     d) Rendimiento/latencia (< 25 ms bajo 100 llamadas consecutivas).
