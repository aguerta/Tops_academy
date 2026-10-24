# Handoff — Stream 1D (Fase 1: Implementador `impl_1d`)

**Fecha:** 2026-10-24  
**Implementador:** `impl_1d` (Fase 1 Stream 1D)  
**Receptor:** Stream 1D Mejorador (`impr_1d`) / Orquestador (`526cfac0-d37b-49c9-bf09-00b5c520add2`)  
**Estado:** COMPLETADO CON ÉXITO (0 errores, 37/37 tests unitarios pasando)

---

## 1. Frontera Exclusiva de Escritura (`Exclusive Write Boundaries`)
Se respetó estrictamente la frontera asignada en `DISPATCH.md`:
- Modificado: `.agents/skills/content-to-course/c2c_hook_guard.py`
- Creado: `tests/test_hook_post_pass_and_write_isolation.py`
- Artefactos de gobernanza:
  - `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1d_impl/BRIEFING.md`
  - `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1d_impl/handoff.md`
- Cero modificaciones a archivos fuera de esta frontera.

---

## 2. Resumen de Implementación Técnica (100% Agnóstica al Dominio)

En `.agents/skills/content-to-course/c2c_hook_guard.py`, dentro del flujo de verificación para **Subagentes Workers** (`conversationId != director_conversation_id` y no exentos en `exempt_conversation_ids`), se implementaron tres nuevas defensas críticas:

### A. Aislamiento de Rutas de Escritura de Python para Workers (Regla A)
- **Objetivo:** Evitar que los subagentes autores creen scripts de debug ad-hoc o pruebas sueltas (`test_debug.py`, `debug_shard.py`, etc.) en la raíz del proyecto o en directorios no autorizados, previniendo polución del repositorio y desvíos de tokens.
- **Mecanismo:** Al invocar cualquier herramienta de escritura (`_WRITE_TOOLS = ("write_file", "write_to_file", "edit_file", "replace_file_content", "multi_replace_file_content", "notebook_edit")`), si el archivo termina en `.py` y no coincide con las rutas de trabajo C2C autorizadas:
  - `work/shards/<shard_id>_data.py`
  - `work/shards/shard_fixes/<CID>.py`
  - `work/shards/build_<shard_id>.py`
  - `work/cta/part_*.py`
  - `work/cta_data.py`
  - `work_append/...`
  - `scratch/...` (incluyendo scratch de sesión AGY)
- **Respuesta Prescriptiva:**
  ```text
  BLOCKER:: Prohibido crear o editar scripts Python arbitrarios fuera de tu shard asignado (ej. scripts de debug sueltos). Escribe únicamente en work/shards/<shard_id>_data.py o work/shards/shard_fixes/<CID>.py.
  ```

### B. Guarda de Corte Temprano Post-PASS (Regla B)
- **Objetivo:** Prevenir que un subagente continúe editando innecesariamente un shard tras haber obtenido ya una validación exitosa (`[+] PASS`), protegiendo el trabajo ya completado y forzando el corte inmediato del bucle del agente.
- **Mecanismo:** Cuando un subagente invoca una herramienta de escritura sobre `.../shards/<shard_id>_data.py`, el hook inspecciona el directorio `work` correspondiente y verifica si existe `.check_attempts/pass_<shard_id>.json` (o `.check_attempts/pass_<norm_s_id>.json`). Si existe y su `"status"` es `"PASS"`, la llamada se bloquea inmediatamente.
- **Respuesta Prescriptiva:**
  ```text
  BLOCKER:: El shard {shard_id} ya aprobó todas las validaciones estrictas ([+] PASS). Detén llamadas a herramientas de edición y emite DONE inmediatamente.
  ```

### C. Protección Anti-Reescritura Monolítica Tras Fallo de Compilación (Regla C)
- **Objetivo:** Erradicar el patrón de sobreescritura total (`write_file`) destructiva o redundante en archivos grandes (`> 250` líneas) tras un fallo de compilación, guiando al worker a usar `edit_file` quirúrgico o crear overrides modulares en `shard_fixes/<CID>.py`.
- **Mecanismo:** Si el subagente invoca `write_file` o `write_to_file` (sobreescritura completa) sobre `.../shards/<shard_id>_data.py`, y:
  1. El archivo ya existe en disco.
  2. Existe un registro previo de compilación en `.check_attempts/compile_<shard_id>.json` (con `distinct_compiles >= 1` o `last_err_hash` no vacío).
  3. El archivo existente supera 250 líneas (o el nuevo contenido supera 250 líneas).
  Entonces la operación se deniega.
  *Excepciones permitidas:* Creación inicial (Turno 1, archivo aún no existe en disco), shards pequeños (`<= 250` líneas), o si aún no se ha ejecutado ninguna compilación. Adicionalmente, `edit_file` y `replace_file_content` están explícitamente permitidos para ediciones quirúrgicas.
- **Respuesta Prescriptiva:**
  ```text
  BLOCKER:: El archivo {shard_id}_data.py ya fue compilado y supera las 250 líneas. Para corregir errores de validación usa edit_file quirúrgico sobre las líneas indicadas por el compilador o escribe un override modular en work/shards/shard_fixes/<CID>.py en lugar de reescribir todo el archivo con write_file.
  ```

---

## 3. Cobertura de Tests Unitarios (`tests/test_hook_post_pass_and_write_isolation.py`)

Se implementaron 12 tests específicos que validan minuciosamente cada regla y caso límite:
1. `test_rule_a_blocks_root_debug_scripts`: Bloqueo de `test_debug.py`, `debug_shard.py`, `scratch_debug.py`, etc., en la raíz del proyecto con el mensaje prescriptivo exacto.
2. `test_rule_a_allows_authorized_c2c_worker_python_paths`: Permiso explícito para rutas C2C legítimas (`shards/*_data.py`, `shard_fixes/*.py`, `build_*.py`, `cta/part_*.py`, `cta_data.py`, `work_append/...`, `scratch/...`).
3. `test_rule_a_allows_non_python_worker_files`: Archivos no-Python (JSON, TXT) no se ven afectados por la Regla A.
4. `test_rule_b_blocks_write_and_edit_when_shard_passed`: Bloqueo de `write_file`, `edit_file` y `replace_file_content` sobre `shard_01_data.py` cuando `pass_shard_01.json` tiene `"status": "PASS"`.
5. `test_rule_b_allows_writing_to_other_shards_without_pass_file`: Shards en progreso sin archivo pass no son bloqueados.
6. `test_rule_b_allows_when_pass_file_is_not_status_pass`: Si el status es `FAIL` o en progreso, no se bloquea.
7. `test_rule_c_blocks_monolithic_write_file_on_compiled_shard_over_250_lines`: Bloqueo de `write_file` en archivo de 260 líneas con fallo de compilación previo; y permiso para `edit_file` y escritura en `shard_fixes/Hab-01.py`.
8. `test_rule_c_allows_turn1_creation_when_file_not_on_disk`: Permiso de `write_file` en Turno 1 con > 250 líneas cuando el archivo no existe aún en disco.
9. `test_rule_c_allows_write_file_when_under_250_lines`: Permiso de `write_file` en archivos de `<= 250` líneas.
10. `test_rule_c_allows_write_file_when_no_prior_compile_attempt`: Permiso si aún no existe `compile_<shard_id>.json`.
11. `test_auditor_exemption_bypasses_all_worker_rules`: Exención total de auditores listados en `exempt_conversation_ids`.
12. `test_director_diet_remains_active_for_director`: El Director sigue operando bajo Director Diet (Case A).

---

## 4. Resultados de Ejecución de Pytest

Comando ejecutado:
```bash
.venv\Scripts\python.exe -m pytest tests/test_hook_post_pass_and_write_isolation.py tests/test_watchdog_and_hooks.py -v
```

Resultado:
```text
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\Augusto\personal_portfolio\Tops_academy
configfile: pyproject.toml
collected 37 items

tests/test_hook_post_pass_and_write_isolation.py::TestHookPostPassAndWriteIsolation::test_auditor_exemption_bypasses_all_worker_rules PASSED [  2%]
tests/test_hook_post_pass_and_write_isolation.py::TestHookPostPassAndWriteIsolation::test_director_diet_remains_active_for_director PASSED [  5%]
tests/test_hook_post_pass_and_write_isolation.py::TestHookPostPassAndWriteIsolation::test_rule_a_allows_authorized_c2c_worker_python_paths PASSED [  8%]
tests/test_hook_post_pass_and_write_isolation.py::TestHookPostPassAndWriteIsolation::test_rule_a_allows_non_python_worker_files PASSED [ 10%]
tests/test_hook_post_pass_and_write_isolation.py::TestHookPostPassAndWriteIsolation::test_rule_a_blocks_root_debug_scripts PASSED [ 13%]
tests/test_hook_post_pass_and_write_isolation.py::TestHookPostPassAndWriteIsolation::test_rule_b_allows_when_pass_file_is_not_status_pass PASSED [ 16%]
tests/test_hook_post_pass_and_write_isolation.py::TestHookPostPassAndWriteIsolation::test_rule_b_allows_writing_to_other_shards_without_pass_file PASSED [ 18%]
tests/test_hook_post_pass_and_write_isolation.py::TestHookPostPassAndWriteIsolation::test_rule_b_blocks_write_and_edit_when_shard_passed PASSED [ 21%]
tests/test_hook_post_pass_and_write_isolation.py::TestHookPostPassAndWriteIsolation::test_rule_c_allows_turn1_creation_when_file_not_on_disk PASSED [ 24%]
tests/test_hook_post_pass_and_write_isolation.py::TestHookPostPassAndWriteIsolation::test_rule_c_allows_write_file_when_no_prior_compile_attempt PASSED [ 27%]
tests/test_hook_post_pass_and_write_isolation.py::TestHookPostPassAndWriteIsolation::test_rule_c_allows_write_file_when_under_250_lines PASSED [ 29%]
tests/test_hook_post_pass_and_write_isolation.py::TestHookPostPassAndWriteIsolation::test_rule_c_blocks_monolithic_write_file_on_compiled_shard_over_250_lines PASSED [ 32%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_auditor_exemption_in_lockfile PASSED [ 35%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_cli_subprocess_stdin_stdout_robustness PASSED [ 37%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_director_allowed_logs_and_dispatch_types PASSED [ 40%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_director_context_diet_enforcement PASSED [ 43%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_docs_hooks_contract_schema_and_variations PASSED [ 45%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_fast_passthrough_when_no_active_lock PASSED [ 48%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_hook_guard_performance_benchmark PASSED [ 51%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_hooks_template_json_structure_and_cwd_execution PASSED [ 54%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_passthrough_when_lock_is_stale_or_inactive PASSED [ 56%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_pre_bootstrap_fast_start_guard PASSED [ 59%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_windows_path_normalization_and_traversal_safety PASSED [ 62%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_worker_allowed_compiler_execution_commands PASSED [ 64%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_worker_allowed_safe_operations PASSED [ 67%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_worker_denied_deleting_check_attempts_and_nested_quote_python_c PASSED [ 70%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_worker_denied_modifying_compiler_and_engine PASSED [ 72%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_worker_denied_modifying_skills_and_check_attempts PASSED [ 75%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_worker_denied_powershell_and_shell_read_commands PASSED [ 78%]
tests/test_watchdog_and_hooks.py::TestLifecycleHookGuard::test_worker_denied_reading_compiler_engine_and_truth PASSED [ 81%]
tests/test_watchdog_and_hooks.py::TestBudgetWatchdogBrainAndRedispatch::test_cumulative_context_token_estimator_on_compact_transcript PASSED [ 83%]
tests/test_watchdog_and_hooks.py::TestBudgetWatchdogBrainAndRedispatch::test_generate_repair_redispatch_with_modular_shard_fixes_and_schedule PASSED [ 86%]
tests/test_watchdog_and_hooks.py::TestBudgetWatchdogBrainAndRedispatch::test_parse_real_antigravity_brain_transcript_108_turns PASSED [ 89%]
tests/test_watchdog_and_hooks.py::TestBudgetWatchdogBrainAndRedispatch::test_parse_transcript_empty_file PASSED [ 91%]
tests/test_watchdog_and_hooks.py::TestBudgetWatchdogBrainAndRedispatch::test_parse_transcript_with_truncated_live_line PASSED [ 94%]
tests/test_watchdog_and_hooks.py::TestBudgetWatchdogBrainAndRedispatch::test_resolve_brain_transcript_with_app_data_dir PASSED [ 97%]
tests/test_watchdog_and_hooks.py::TestBudgetWatchdogBrainAndRedispatch::test_resolve_brain_transcript_with_transcript_full_fallback PASSED [100%]

============================= 37 passed in 0.96s ==============================
```

La suite pasa al 100% en menos de 1 segundo sin regresiones.
