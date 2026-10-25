# DISPATCH — Stream 1D (Fase 1: Implementador `impl_1d`)

## 1. Rol y Frontera Exclusiva de Escritura (`Exclusive Write Boundaries`)
Eres el **Implementador del Stream 1D** bajo `/flash-triad-orchestrator`.
- **Carpeta de Gobernanza:** `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1d_impl/`
- **Archivos de Producción Permitidos (ÚNICOS que puedes modificar):**
  1. `.agents/skills/content-to-course/c2c_hook_guard.py`
  2. `tests/test_hook_post_pass_and_write_isolation.py` *(nuevo archivo de tests unitarios)*
- **Artefactos de Gobernanza Permitidos:**
  - `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1d_impl/BRIEFING.md`
  - `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1d_impl/handoff.md`
- **PROHIBIDO** editar cualquier otro archivo del repositorio.

## 2. Paso 0 Obligatorio (*Pre-Flight Sanity Check*)
Antes de realizar cualquier edición:
1. Lee `.agents/skills/content-to-course/c2c_hook_guard.py` completo y `tests/test_watchdog_and_hooks.py` (solo lectura) para entender exactamente cómo se evalúan las reglas del Director y de los Workers cuando existe un lockfile activo `.c2c_subagent_lock.json`.
2. Escribe `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1d_impl/BRIEFING.md`. Si detectas cualquier bloqueo fuera de tu frontera, detén ediciones y envía `BLOCKER:: <archivo:línea> | <causa> | <opciones>` al Orquestador (`526cfac0-d37b-49c9-bf09-00b5c520add2`).

## 3. Especificación Técnica de Implementación (100% Agnóstica al Dominio)

En `.agents/skills/content-to-course/c2c_hook_guard.py`, para los **Subagentes Workers** (`conversationId != director_conversation_id` y no exentos en `exempt_conversation_ids` ni auditores QA) cuando hay una corrida C2C activa:

### A. Aislamiento de Rutas de Escritura para Workers (Bloqueo de Scripts de Debug Ad-Hoc como `test_debug.py`)
- Cuando la herramienta sea de escritura (`write_file`, `edit_file`, `replace_file_content`, `multi_replace_file_content` o equivalente en `_WRITE_TOOLS`):
  - Si el archivo destino termina en `.py` y **NO** está dentro de una ruta de trabajo C2C autorizada (`work/shards/<shard_id>_data.py`, `work/shards/shard_fixes/<CID>.py`, `work/shards/build_<shard_id>.py`, `work/cta/part_*.py`, `work_append/...` o carpeta `scratch/`), **DENEGAR** la operación con mensaje prescriptivo:
    `"BLOCKER:: Prohibido crear o editar scripts Python arbitrarios fuera de tu shard asignado (ej. scripts de debug sueltos). Escribe únicamente en work/shards/<shard_id>_data.py o work/shards/shard_fixes/<CID>.py."`

### B. Guarda de Corte Temprano Post-PASS (`.check_attempts/pass_<shard_id>.json`)
- Cuando un subagente worker invoque una herramienta de escritura (`_WRITE_TOOLS`) sobre `.../shards/<shard_id>_data.py` (ej. `shard_07_data.py`):
  - Determinar el directorio `work` padre (`target_path.parent.parent`) y verificar si existe `work / ".check_attempts" / f"pass_{shard_id}.json"`.
  - Si `pass_<shard_id>.json` existe en disco (y su `"status"` es `"PASS"`), **DENEGAR** la escritura con:
    `"BLOCKER:: El shard {shard_id} ya aprobó todas las validaciones estrictas ([+] PASS). Detén llamadas a herramientas de edición y emite DONE inmediatamente."`

### C. Protección Anti-Reescritura Monolítica Tras Fallo de Compilación (`write_file` vs `edit_file`)
- Cuando un subagente worker invoque `write_file` (sobreescritura completa, no `edit_file`) sobre un archivo `.../shards/<shard_id>_data.py` que **ya existe en disco**:
  - Verificar si ya existe un registro de intento de compilación previo en `work / ".check_attempts" / f"compile_{shard_id}.json"` (con `distinct_compiles >= 1` o `last_err_hash` no vacío) y el archivo existente en disco ya tiene `> 250` líneas (o el nuevo `Content` tiene `> 250` líneas).
  - Si es así, **DENEGAR** `write_file` con mensaje prescriptivo:
    `"BLOCKER:: El archivo {shard_id}_data.py ya fue compilado y supera las 250 líneas. Para corregir errores de validación usa edit_file quirúrgico sobre las líneas indicadas por el compilador o escribe un override modular en work/shards/shard_fixes/<CID>.py en lugar de reescribir todo el archivo con write_file."`
  - Nota: Si el archivo aún no existe en disco (Turno 1 de creación inicial) o tiene `<= 250` líneas, `write_file` se permite normalmente.

## 4. Verificación y Entrega
1. Crea `tests/test_hook_post_pass_and_write_isolation.py` verificando:
   - Que un worker con lock C2C activo sea bloqueado al intentar crear `test_debug.py` o `debug_shard.py` en la raíz del proyecto, pero pueda escribir normalmente en `courses/demo/work/shards/shard_01_data.py` y `courses/demo/work/shards/shard_fixes/Hab-01.py`.
   - Que si existe `courses/demo/work/.check_attempts/pass_shard_01.json` con `"status": "PASS"`, cualquier intento de `write_file` o `edit_file` sobre `shard_01_data.py` sea bloqueado con el mensaje Post-PASS.
   - Que si `shard_01_data.py` ya existe con `> 250` líneas y existe `.check_attempts/compile_shard_01.json` con un intento fallido previo, `write_file` sea denegado exigiendo `edit_file` o `shard_fixes/<CID>.py`, mientras que `edit_file` sí sea permitido.
   - Que todos los tests existentes en `tests/test_watchdog_and_hooks.py` sigan pasando al 100%.
2. Ejecuta `.venv\Scripts\python.exe -m pytest tests/test_hook_post_pass_and_write_isolation.py tests/test_watchdog_and_hooks.py`.
3. Escribe `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1d_impl/handoff.md` y envía `DONE:: Stream 1D Implementer completado` a `526cfac0-d37b-49c9-bf09-00b5c520add2`.
