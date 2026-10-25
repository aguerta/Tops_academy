# Pre-Flight Sanity Check — Stream 1C (`impl_1c`)

**Fecha/Hora:** 2026-10-24T20:38:00-05:00  
**Agente:** `impl_1c` (Implementador Stream 1C — `/flash-triad-orchestrator`)  
**Frontera de Producción Exclusiva:**
1. `.agents/skills/content-to-course/c2c_hook_guard.py`
2. `tests/test_hook_post_pass_and_write_isolation.py`

---

## 1. Verificación de Código Fuente y Firmas Reales

### A. `.agents/skills/content-to-course/c2c_hook_guard.py`
- **Total de líneas inspeccionadas:** 744 líneas.
- **Constantes y colecciones clave:**
  - `WORKER_DENIED_READ_SUBSTRINGS` (L37–L51): 13 strings protegidos (`compile_shard.py`, `check_templates.py`, `engine/`, `validator/`, `.check_attempts`, `judge_ground_truth.json`, etc.). Falta `"tests/"`.
  - `WORKER_DENIED_WRITE_SUBSTRINGS` (L54–L71): Targets protegidos contra escritura/edición.
  - `_WRITE_TOOLS` (L73–L80): `("write_file", "write_to_file", "edit_file", "replace_file_content", "multi_replace_file_content", "notebook_edit")`.
  - `WORKER_AUTHORIZED_PYTHON_PATTERNS` (L82–L89): 6 expresiones regulares autorizadas para shards y cta básico. Faltan `cta_fixes/*.py`, `cta_parts/cta_fixes/*.py`, `cta_parts/*.py`.
  - `SHARD_DATA_PATTERN` (L91–L94): Identificador regex de archivos de shards.
- **Funciones y lógica operativa:**
  - `_extract_target_file_path(args)` (L97–L112)
  - `_is_authorized_worker_python_write(p)` (L115–L128)
  - `_extract_paths_from_args(args)` (L225–L248)
  - `process_hook(payload, custom_lock_file)` (L308–L708)
    - `Case B: Caller IS C2C Worker Subagent` (L405–L708):
      - 0. Cross-Course Isolation (L410–L456): Prohibición de acceder o listar `courses/`. Requiere endurecer `Get-ChildItem -Path courses/ -Recurse`.
      - 1. Deny reading forbidden compiler/validator (L457–L468): Requiere incorporar `"tests/"` y herramientas como `grep_search` / `find_by_name`.
      - 2. Deny writing protected targets (L469–L480).
      - Rule A: Worker Python write isolation (L486–L496).
      - Rule B: Post-PASS early cut guard (L536–L556): Actualmente solo aplica a shards (`pass_<shard_id>.json`). Requiere extensión a CTA (`pass_cta_{target_id}.json`).
      - Rule C: Anti-monolithic rewrite guard (L558–L643): Requiere soporte unificado del umbral oficial `< 6` errores (`has_syntax_error`, `error_count < 6` vs `>= 6`), tanto para Shards como para CTA.
      - 3. Deny shell command circumvention (L645–L707): Requiere bloqueo de `git log/diff/show/status/branch/grep` y lecturas de `tests/` vía shell.

### B. `tests/test_hook_post_pass_and_write_isolation.py`
- **Total de líneas inspeccionadas:** 658 líneas.
- **Suite existente:** `TestHookPostPassAndWriteIsolation` (12 métodos de prueba).
- **Estado de ejecución actual:** 100% pasando (12/12 en 0.28s).

---

## 2. Evaluación de Conflictos y Bloqueos (Tier A / Tier B)
- **Archivos fuera de frontera:** Ninguno entra en conflicto o bloquea las tareas de Stream 1C.
- **Bloqueos detectados:** **0 bloqueos**. No se requiere escalamiento `BLOCKER::` al Orquestador.

---

## 3. Plan de Acción Inmediato
1. Extender `WORKER_AUTHORIZED_PYTHON_PATTERNS` y `_is_authorized_worker_python_write` para incluir `cta_fixes/*.py`, `cta_parts/cta_fixes/*.py`, y `cta_parts/*.py`.
2. Actualizar mensaje de denegación de Regla A para citar `work/cta_fixes/<CID>.py`.
3. Agregar `"tests/"` a `WORKER_DENIED_READ_SUBSTRINGS` y asegurar bloqueo en herramientas de lectura/búsqueda (`view_file`, `read_file`, `grep_search`, `find_by_name`).
4. Bloquear comandos `git` exploratorios (`log`, `diff`, `show`, `status`, `branch`, `grep`) y lecturas shell sobre `tests/`. Endurecer regex de listado sobre `courses/`.
5. Implementar Regla B para CTA (`pass_cta_{cta_target_id}.json` / `pass_{cta_target_id}.json`).
6. Implementar Regla C con umbral `< 6` errores para Shards y CTA (`has_syntax_error`, `error_count < 6` deny, `error_count >= 6` allow, y retrocompatibilidad con `error_count is None`).
7. Expandir `tests/test_hook_post_pass_and_write_isolation.py` con cobertura completa de todos los nuevos casos.
8. Ejecutar pytest y validar verde al 100%.
