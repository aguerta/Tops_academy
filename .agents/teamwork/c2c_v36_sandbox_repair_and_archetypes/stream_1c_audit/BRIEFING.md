# BRIEFING — Stream 1C (Fase 3: Auditor Forense `audit_1c`)

**Fecha:** 2026-10-25  
**Auditor:** `audit_1c` (Auditor Forense Stream 1C)  
**Objetivo:** Auditar la implementación y hardening de la compilación incremental de shards, persistencia obligatoria de `templates_report.json`, aislamiento estricto de errores por CID y despacho de reparación en `run.py` y `dispatch.py`.

---

## 1. Alcance de la Auditoría
1. **Compilación incremental en `run_stage_templates` (`run.py`):**
   - Comprobación de que `shard_XX_data.py` se omite si `work/templates/<cid>.json` está al día.
   - Verificación de que la caché se invalida correctamente si `shard_XX_data.py`, `cta.json`, o parches quirúrgicos en `work/shards/shard_fixes/<cid>.py` / `work/shard_fixes/<cid>.py` tienen `mtime` mayor al template generado.
2. **Persistencia de reporte de templates (`run.py`):**
   - Comprobación de que `work/reports/templates_report.json` se persiste incondicionalmente, tanto en ejecuciones exitosas (`is_clean == True`) como en fallidas (`is_clean == False`), antes de lanzar cualquier excepción (`raise ValueError`).
   - Verificación de estructura del reporte: `status`, `total_templates`, `total_seeds_run`, `errors`, `warnings`, `errors_by_cid`, `failed_competencies`.
3. **Mapeo de errores y prevención de colisión de prefijos (`run.py` y `dispatch.py`):**
   - Verificación de que el mapeo por CID utiliza regex estrictas (evitando falsos positivos como asociar errores de `C-010` o `C-10` a `C-01` o `C-1`).
4. **Despacho de reparación (`dispatch.py`):**
   - Soporte para argumentos `--ids` con cadenas separadas por comas (`"C-05, C-11"` o listas anidadas/aplanadas), deduplicando preservando orden.
   - Inyección de diagnósticos reales desde `templates_report.json` al prompt de reparación.
   - Punteros y archivos `work/prompts/repair/repair_<cid_norm>.json` y `repair_{idx:02d}.json` sin sobrescritura o colisión destructiva.
5. **Calidad de Pruebas Unitarias:**
   - Auditoría estricta de `tests/test_run_templates_and_dispatch_repair.py`: sin aserciones vacías ni falsos positivos.
   - Ejecución independiente con pytest.
