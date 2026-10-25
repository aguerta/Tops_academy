# HANDOFF — Stream 1C (Fase 2: Mejorador `impr_1c`)

**Fecha:** 2026-10-25  
**Agente:** `impr_1c` (Mejorador Stream 1C)  
**Destino:** `audit_1c` (Auditor Stream 1C) / Orquestador (`d603756a-7e58-4466-b883-cbc391586154`)

---

## 1. Resumen Ejecutivo de Endurecimiento (Hardening)
Se completó con éxito el endurecimiento de la compilación incremental de shards, el aislamiento de errores de templates sin colisiones de prefijo y el despacho de subagentes de reparación con diagnósticos exhaustivos en Turno 1.

### Mejoras Realizadas:
1. **Invalidación de Caché Incremental Robusta (`run.py` - `run_stage_templates`):**
   - Incorpora comprobación de timestamp `mtime` respecto a `work/templates/<cid>.json` considerando:
     - `shard_XX_data.py` (código fuente del shard).
     - `cta.json` (diseño curricular y distractores actualizados).
     - Parches modulares quirúrgicos en `work/shards/shard_fixes/<cid>.py`, `work/shard_fixes/<cid>.py`, y sus variantes en minúsculas.
   - Si cualquiera de estos archivos es más reciente que el template compilado (`mtime > cid_json.stat().st_mtime`), se invalida la caché de compilación de ese shard y se ejecuta `compile_shard`.

2. **Eliminación Total de Colisiones de Prefijo en `errors_by_cid` (`run.py` y `dispatch.py`):**
   - Reemplazó los chequeos parciales basados en `in` (e.g. `f"Competency {cid}" in err_str` o `f"competency '{cid}'" in err_str`), los cuales provocaban que un error en `C-010` o `C-10` se atribuyera falsamente a `C-01` o `C-1`.
   - Implementó delimitación estricta con regex negative lookbehind y lookahead:
     `rf"(?<![A-Za-z0-9_-]){re.escape(cid)}(?![A-Za-z0-9_-])"`.
   - Adicionalmente, `re.finditer` para patrones `(?:C|H|Hab)-\d+` valida membresía en los IDs conocidos antes de registrar la coincidencia.

3. **Deduplicación de `--ids` Preservando Orden (`dispatch.py` - `dispatch_repair`):**
   - Soporta argumentos `--ids "C-05, C-11, C-05"` o arrays combinados `["C-11, C-05", "C-11"]`, aplanando y deduplicando estrictamente con preservación del orden de aparición.
   - Limpia la bandera `manual_request` cuando existen errores diagnosticados válidos para la competencia solicitada.

4. **Inyección Explícita de Errores Diagnosticados en Turno 1 (`dispatch.py`):**
   - Soporta múltiples formatos de `templates_report.json`, incluyendo `"failed_competencies"` como lista o como diccionario de objetos (`{"C-05": {"errors": [...]}}`).
   - Construye una sección `### Errores Diagnosticados en Templates:` con viñetas legibles dentro del prompt Markdown de la orden de trabajo (`Prompt` y `work_order`) en `work/prompts/repair/repair_<cid_norm>.json` y `work/dispatch/items/repair_<cid_norm>.json`, permitiendo al `Repair Engineer` identificar la falla de forma instantánea desde su Turno 1.

---

## 2. Archivos Modificados (Strict Exclusive Write Boundaries)
1. `.agents/skills/content-to-course/run.py`
2. `.agents/skills/content-to-course/dispatch.py`
3. `tests/test_run_templates_and_dispatch_repair.py`
4. Artefactos de gobernanza:
   - `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1c_impr/BRIEFING.md`
   - `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1c_impr/handoff.md`

*(Ningún otro archivo del repositorio fue modificado).*

---

## 3. Cobertura de Pruebas Unitarias y Resultados
Se añadieron 4 nuevos tests unitarios adversarios en `tests/test_run_templates_and_dispatch_repair.py`:
- `test_dispatch_repair_deduplicates_ids_preserving_order`: Deduplicación de `--ids` preservando orden.
- `test_dispatch_repair_supports_dict_failed_competencies_and_diagnostics`: Soporte para estructura dict en `failed_competencies`.
- `test_errors_by_cid_no_prefix_collision`: Prueba adversaria que confirma que un error en `C-010` jamás se asigna a `C-01` en `run_stage_templates` ni en `dispatch_repair`.
- `test_run_stage_templates_invalidates_cache_on_newer_shard_fix_or_cta`: Prueba exhaustiva de invalidación incremental por timestamp en `shard_fixes/` y `cta.json`.

### Ejecución de Pruebas:
- `.venv\Scripts\python.exe -m pytest tests/test_run_templates_and_dispatch_repair.py -v`:
  **8/8 PASSED** (100% verde).
- `.venv\Scripts\python.exe -m pytest tests/test_dispatch_turn0_and_milestone3_prompts.py -k repair -v`:
  **3/3 PASSED** (100% verde).
- Total de pruebas directas del Stream 1C: **11/11 PASSED**.
*(Nota: En la suite combinada `test_dispatch_turn0_and_milestone3_prompts.py`, 18 tests pasan y 3 fallos corresponden a `lean/prompt_shard_author.md` (5328B > 4750B), bajo el Stream 1B/1D).*

---

## 4. Estado de Entrega
Fase 2 (Mejorador Stream 1C) completada al 100%. Código endurecido y listo para la Fase 3 (Auditor Stream 1C).
