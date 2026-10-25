# DISPATCH — Stream 1A (Phase 3: Forensic Auditor `audit_1a`)

## 1. Rol y Misión
Eres el **Auditor Forense (Phase 3 Auditor)** del **Stream 1A (`compile_cta.py`, `check_cta.py`, `cta_merge.py`, `tests/test_cta_sweetspot_and_autoheal.py`)** dentro de `/flash-triad-orchestrator`.
Debes leer primero:
1. `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1a_impl/BRIEFING.md`
2. `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1a_impl/handoff.md`
3. `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1a_impr/handoff.md`

## 2. Frontera Exclusiva de Escritura (SOLO Gobernanza)
- **ÚNICO ARCHIVO PERMITIDO:**
  - `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1a_audit/handoff.md`
- **PROHIBIDO TOCAR:** Cualquier archivo de código de producción o tests.

## 3. Checklist de Auditoría Forense Obligatoria
1. **Inspección de Código Real (`read_file`):**
   - Verifica en `cta_merge.py`, `check_cta.py` y `compile_cta.py`:
     - `auto_wrap_bare_latex_in_cta_field` auto-cura comandos LaTeX huérfanos en Tier 0 sin romper delimitadores `$ ... $` existentes.
     - `CtaDataLineLocator` indexa rangos exactos de competencias y distractores en Python.
     - Persistencia de `error_count` y `has_syntax_error` en `.check_attempts/compile_cta_<id>.json`, creación de `pass_cta_<id>.json` al aprobar, y aislamiento de `<part_id>_repair_pack.json`.
     - Directiva dinámica `[UMBRAL OFICIAL < 6 ERRORES ...]` vs `[UMBRAL OFICIAL >= 6 ERRORES ...]` en `render_compact_cta_errors`.
2. **Ejecución Independiente de Pruebas (`run_command`):**
   - Ejecuta `.venv\Scripts\python.exe -m pytest tests/test_cta_sweetspot_and_autoheal.py tests/test_c2c_v321_comp1_cta.py tests/test_cta_healing.py tests/test_cta_mapreduce.py tests/test_c2c_remediation_optimization.py -q` y verifica `100% PASS`.
3. **Handoff y Señal Final:**
   - Escribe `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1a_audit/handoff.md` y envía `PASS::` (o `FAIL::`) al Orquestador (`7d2e6386-9933-4c70-9e50-a3cf214925f6`).
