# DISPATCH — Stream 1A (Phase 2: Improver `impr_1a`)

## 1. Rol y Misión
Eres el **Mejorador (Phase 2 Improver)** del **Stream 1A (`compile_cta.py`, `check_cta.py`, `cta_merge.py`, `tests/test_cta_sweetspot_and_autoheal.py`)** dentro de `/flash-triad-orchestrator`.
Debes leer primero:
1. `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1a_impl/BRIEFING.md`
2. `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1a_impl/handoff.md`

## 2. Frontera Exclusiva de Escritura (100% Disjunta)
- **ARCHIVOS DE PRODUCCIÓN PERMITIDOS:**
  - `.agents/skills/content-to-course/compile_cta.py`
  - `.agents/skills/content-to-course/check_cta.py`
  - `.agents/skills/content-to-course/cta_merge.py`
- **ARCHIVO DE TEST PERMITIDO:**
  - `tests/test_cta_sweetspot_and_autoheal.py`
- **ARCHIVO DE GOBERNANZA PERMITIDO:**
  - `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1a_impr/handoff.md`
- **PROHIBIDO TOCAR:** Cualquier otro archivo fuera de esta lista.

## 3. Requerimientos de Endurecimiento (`impr_1a`)
1. **Revisión de Edge Cases en Tier-0 Auto-Heal (`cta_merge.py`) y `CtaDataLineLocator` (`compile_cta.py`):**
   - Verifica que `auto_wrap_bare_latex_in_cta_field` envuelva limpiamente los 5 patrones reales de `asyntotic_estatistics_v5` (`\lim_{n\to\infty} \frac{\sigma^2}{n} = 0`, `\frac{1}{n}\sum_{i=1}^n X_i`, `\sqrt{n}(\hat{\theta}_n - \theta_0) \xrightarrow{d} \mathcal{N}(0, V)`, `\sigma` suelto en prosa, y ecuaciones con `=`) sin alterar cadenas que ya tienen `$ ... $` bien balanceados ni romper los tests legacy de `tests/test_cta_healing.py` y `tests/test_c2c_v321_comp1_cta.py`.
   - Verifica que `compile_cta.py` persista `error_count` y `has_syntax_error` en `.check_attempts/compile_cta_<target_id>.json` (y `compile_<target_id>.json`), que escriba `pass_cta_<target_id>.json` al aprobar, y que aísle `part_XX_repair_pack.json` en ejecuciones paralelas Map-Reduce.
2. **Pruebas Adicionales en `tests/test_cta_sweetspot_and_autoheal.py`:**
   - Agrega un test con las 5 expresiones exactas de `asyntotic_estatistics_v5` (`D-H03-03`, `D-C03-04`, `D-Hab01-05`, `D-Hab03-02`, `D-Hab04-05`) verificando que `compile_cta` las auto-cura en Tier 0 (`0` errores) y `check_cta_katex` reporta `0` violaciones.
   - Agrega un test para `has_syntax_error: True` cuando `part_01_data.py` tiene un `SyntaxError` de Python.

## 4. Verificación y Handoff
1. Ejecuta:
   `.venv\Scripts\python.exe -m pytest tests/test_cta_sweetspot_and_autoheal.py tests/test_c2c_v321_comp1_cta.py tests/test_cta_healing.py tests/test_cta_mapreduce.py -q`
2. Normaliza CRLF a LF en los 4 archivos de tu frontera.
3. Escribe `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1a_impr/handoff.md` y envía `DONE::` al Orquestador (`7d2e6386-9933-4c70-9e50-a3cf214925f6`).
