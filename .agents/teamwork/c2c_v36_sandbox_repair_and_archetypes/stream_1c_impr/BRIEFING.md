# BRIEFING — Stream 1C (Fase 2: Mejorador `impr_1c`)

**Fecha:** 2026-10-25  
**Agente:** `impr_1c` (Mejorador Stream 1C)  
**Objetivo:** Endurecimiento, cobertura de casos borde y tests adversarios para la compilación incremental de shards, persistencia y reporte de templates, y despacho de reparación con diagnóstico transparente.

---

## 1. Análisis de Estado Actual (Post-Implementación Stream 1C)
El implementador `impl_1c` sentó las bases de:
- Detección de timestamps `mtime` en `run_stage_templates` para shards vs `templates/<cid>.json`.
- Estructuración de `work/reports/templates_report.json` con `errors_by_cid` y `failed_competencies`.
- Normalización inicial de `--ids` por comas y eliminación de colisión de punteros (`prompts/repair/repair_<cid_norm>.json`).

## 2. Puntos Críticos y Casos Borde Identificados para Endurecimiento

### 2.1 En `run.py` (`run_stage_templates`):
1. **Invalidación de caché incremental por `shard_fixes/` y `cta.json`:**
   - La comprobación actual revisa `shards_dir / "shard_fixes" / f"{cid}.py"`, pero no revisa `self.work_dir / "shard_fixes" / f"{cid}.py"`, ni tampoco si `cta.json` es más reciente que `cid_json.stat().st_mtime`.
   - Se debe verificar que si existe un fix modular en `work/shards/shard_fixes/{cid}.py` O `work/shard_fixes/{cid}.py` con `mtime > cid_json.stat().st_mtime`, o si `cta_file.stat().st_mtime > cid_json.stat().st_mtime`, se invalide la caché y se recompile el shard.
2. **No-colisión de prefijos en `errors_by_cid`:**
   - En `run.py` (líneas 840–855):
     Se revisaban substrings como `f"'{cid}'"`, `f"[{cid}]"`, `f"competency '{cid}'"`, o regex `\b{re.escape(cid)}\b`. Pero luego `re.finditer(r"\b(?:C|H|Hab)-\d+\b", err_str)` capturaba cualquier ID en el error.
     Si el error contiene `"Error in C-10"`, una iteración sobre `known_cids` donde `cid = "C-1"` podría emparejar si no se tiene cuidado (o si un mensaje contiene `C-10.json`, un chequeo ingenuo de `C-1` podría colisionar si los delimitadores son ambiguos).
     Con regex estricto con word boundaries `\b{re.escape(cid)}\b` y delimitadores canónicos `(?:^|[^\w-]){re.escape(cid)}(?:[^\w-]|$)`, nos aseguramos de que `"C-1"` nunca coincida con `"C-10"` o `"C-010"`.
     Asimismo, en la recolección de `re.finditer`, sólo se deben asociar competencias exactas que pertenezcan a `known_cids`.

### 2.2 En `dispatch.py` (`dispatch_repair`):
1. **Deduplicación de `--ids` preservando orden:**
   - Si el llamador pasa `--ids "C-05, C-11, C-05"` o arrays combinados `["C-05, C-11", "C-05"]`, se debe deduplicar manteniendo el primer orden de aparición.
2. **Inyección explícita de errores reales en `repair_<cid>.json` y `prompt_text`:**
   - Cuando `failed_competencies` o `failing_targets[cid]` tiene errores registrados, la sección `## 2. DIAGNÓSTICO DEL FALLO` en `prompt_text` y el campo `"diagnostics"` en el JSON de la orden de trabajo deben reflejar de forma exhaustiva los mensajes de error extraídos de `templates_report.json`. Si `diagnostics` tiene `template_errors` o `errors`, se garantiza que no se enmascaren y que `manual_request` no se marque si hay diagnósticos reales.

### 2.3 Ampliación de tests en `tests/test_run_templates_and_dispatch_repair.py`:
1. `test_run_stage_templates_invalidates_cache_on_shard_fix_or_cta_update`:
   - Modificar `work/shards/shard_fixes/C-01.py` con `mtime > work/templates/C-01.json`, verificando que `run_stage_templates` no salta la compilación y re-ejecuta `compile_shard`.
   - Modificar `work/cta.json` con `mtime > work/templates/C-01.json`, verificando la misma invalidación.
2. `test_errors_by_cid_no_prefix_collision`:
   - Probar que un error en `C-010` o `C-10` no se asigna indebidamente a `C-01` o `C-1`.
3. `test_dispatch_repair_deduplicates_ids_preserving_order`:
   - Probar `--ids "C-05, C-08, C-05"` o `["C-05,C-08", "C-05", "C-08"]`, verificando que se generan exactamente 2 subagentes en el orden `[C-05, C-08]`.

---

## 3. Plan de Ejecución
1. Escribir este `BRIEFING.md`.
2. Actualizar `run.py` con las validaciones de `shard_fixes/`, `work/shard_fixes/`, `cta.json` y coincidencia exacta no colisionante en `errors_by_cid`.
3. Actualizar `dispatch.py` con deduplicación de `--ids` preservando orden e inyección precisa de diagnósticos en el prompt de reparación.
4. Agregar tests unitarios adversarios en `tests/test_run_templates_and_dispatch_repair.py`.
5. Ejecutar la suite de tests unitarios `.venv\Scripts\python.exe -m pytest tests/test_run_templates_and_dispatch_repair.py tests/test_dispatch_turn0_and_milestone3_prompts.py -q`.
6. Documentar en `handoff.md` y enviar señal `DONE` al Orquestador.
