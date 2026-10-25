# Pre-Flight Sanity Check & Briefing — Stream 1D (impl_1d)

**Fecha:** 2026-10-24  
**Agente:** Implementador Stream 1D (`impl_1d`)  
**Orquestador ID:** `526cfac0-d37b-49c9-bf09-00b5c520add2`  
**Frontera de Escritura Exclusiva:**
- `.agents/skills/content-to-course/c2c_hook_guard.py`
- `tests/test_hook_post_pass_and_write_isolation.py`
- `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1d_impl/BRIEFING.md`
- `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1d_impl/handoff.md`

---

## 1. Análisis de Estado Base y Hallazgos Pre-Flight

1. **Lectura Completa de `c2c_hook_guard.py`:**
   - La arquitectura actual de `c2c_hook_guard.py` evalúa:
     - Pre-Bootstrap Fast-Start Guard (sin necesidad de lockfile activo).
     - Detección de lockfile activo (`.c2c_subagent_lock.json`).
     - Auditor Exemption (`exempt_conversation_ids`).
     - Independent Conversation Exemption (verificando `transcript.jsonl` del Director).
     - Case A: Caller IS Director (`DIRECTOR_DENIED_PATTERNS`).
     - Case B: Caller IS C2C Worker Subagent.
       - Sub-regla 0: Cross-Course Isolation Guard.
       - Sub-regla 1: Deny reading forbidden internal compiler / validator / ground truth targets.
       - Sub-regla 2: Deny writing / modifying skills, compiler source, or check attempts.
       - Sub-regla 3: Deny circumventing via shell commands.
   - Invariante de Salida: Retorno código 0 en stdout en formato JSON `{"decision": "allow" | "deny", "reason": ...}`.

2. **Lectura de Tests Existentes (`tests/test_watchdog_and_hooks.py`):**
   - 25 tests unitarios pasan exitosamente en 0.58s con `.venv\Scripts\python.exe -m pytest tests/test_watchdog_and_hooks.py`.
   - Se validan tiempos (< 50ms passthrough, benchmark 1000 iteraciones < 250ms), aislamiento Director/Worker, y comandos permitidos/denegados.

3. **Verificación de Bloqueos:**
   - No se detecta ningún conflicto ni bloqueo exterior a la frontera asignada.
   - Las tres nuevas protecciones para Workers en `c2c_hook_guard.py` se integran en el bloque Case B (Caller IS C2C Worker Subagent) de forma limpia y ortogonal:
     1. **Regla A (Aislamiento de Rutas de Escritura de Python):** Bloqueo a workers que escriban `.py` fuera de las rutas de trabajo asignadas (`work/shards/<shard_id>_data.py`, `work/shards/shard_fixes/<CID>.py`, `work/shards/build_<shard_id>.py`, `work/cta/part_*.py`, `work/cta_data.py`, `work_append/...`, `scratch/...`).
     2. **Regla B (Guarda de Corte Temprano Post-PASS):** Bloqueo de escrituras (`write_tools`) sobre `.../shards/<shard_id>_data.py` si existe `pass_<shard_id>.json` con `"status": "PASS"`.
     3. **Regla C (Anti-Reescritura Monolítica Tras Fallo de Compilación):** Bloqueo de `write_file` / `write_to_file` sobre `.../shards/<shard_id>_data.py` existente con `> 250` líneas cuando existe `compile_<shard_id>.json` con al menos un intento de compilación registrado, forzando `edit_file` o `shard_fixes/<CID>.py`.

---

## 2. Plan de Implementación Quirúrgica

1. **En `.agents/skills/content-to-course/c2c_hook_guard.py`:**
   - Definir `_WRITE_TOOLS = ("write_file", "write_to_file", "edit_file", "replace_file_content", "multi_replace_file_content", "notebook_edit")`.
   - Implementar helper `_is_authorized_worker_python_path(path: str) -> bool` para filtrar rutas `.py`.
   - Implementar helper `_extract_shard_id_and_work_dir(path: str, active_lock: Dict[str, Any]) -> Tuple[Optional[str], Optional[Path]]`.
   - Añadir validación Post-PASS temprana antes de permitir cualquier herramienta de escritura sobre `shard_*_data.py`.
   - Añadir validación Anti-Reescritura Monolítica (`write_file` vs `edit_file`) cuando el archivo supera 250 líneas y ya cuenta con un registro en `.check_attempts/compile_<shard_id>.json`.
   - Asegurar que todas las rutas mantengan el benchmark de performance (< 250ms para 1000 llamadas).

2. **En `tests/test_hook_post_pass_and_write_isolation.py`:**
   - Crear suite completa de tests cubriendo las tres reglas (A, B y C).
   - Testear escenarios positivos (permitidos) y negativos (bloqueados con mensajes prescriptivos exactos).

3. **Verificación:**
   - Ejecutar suite combinada `pytest tests/test_hook_post_pass_and_write_isolation.py tests/test_watchdog_and_hooks.py`.
   - Generar `handoff.md` y enviar `DONE:: ...` al Orquestador.
