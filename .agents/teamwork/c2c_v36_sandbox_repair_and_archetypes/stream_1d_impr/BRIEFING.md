# BRIEFING — Stream 1D (Fase 2: Mejorador `impr_1d`)

## 1. Identificación y Objetivos
- **Stream:** 1D (Milestone 3 Semantic Archetype Gate Hardening & Modular Fix Merging)
- **Fase:** 2 (Mejorador `impr_1d`)
- **Agente:** Mejorador `/flash-triad-orchestrator`
- **Frontera Exclusiva de Escritura:**
  - `.agents/skills/content-to-course/compile_shard.py`
  - `.agents/skills/content-to-course/system_prompts/prompt_shard_author.md`
  - `.agents/skills/content-to-course/system_prompts/lean/prompt_shard_author.md`
  - `tests/test_m3_archetypes_semantic_gate.py`
  - `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1d_impr/BRIEFING.md`
  - `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1d_impr/handoff.md`

---

## 2. Diagnóstico de Casos Borde y Hardening Requerido

### Caso Borde 1: Modular Merging (`shard_fixes/<CID>.py`)
- **Problema:** En la implementación inicial de Fase 1, la compuerta `[M3-ARCHETYPES]` acumulaba todas las funciones encontradas en `shard_XX_data.py` y en todos los `shard_fixes/*.py` en un único diccionario global `shard_ast_funcs`. Si un shard base contenía una función generadora antigua/rota para una competencia (ej. `def _gen_h01(rng, arch=1): pass`), y dicha competencia era sustituida mediante `shard_fixes/H-01.py` con un generador corregido (posiblemente con otro nombre o sobrescrito), la compuerta AST continuaba inspeccionando la función obsoleta del shard base, generando un **falso positivo** que bloqueaba la compilación válida.
- **Solución:** Aislar el análisis AST por competencia (`cid`):
  - Si `cid` cuenta con un archivo modular en `fix_files_by_cid[cid]`, la fuente efectiva para `cid` es dicho archivo modular más los `generator_code` compilados de sus tuplas en `tpls`. Las funciones declaradas en el archivo base para `cid` son omitidas para evitar falsos positivos por código muerto.
  - Si `cid` no tiene fix modular, la fuente efectiva es `shard_data_path` / `healed_source` más los `generator_code` compilados de `tpls`.

### Caso Borde 2: Evasión Trivial del AST (`_ = arch` o `arch == arch` o generadores clonados)
- **Problema:** Un autor o agente podría intentar burlar el análisis AST de `arch` insertando una asignación vacía (`_ = arch` o `arch == arch`) sin ramificar realmente el comportamiento matemático, o escribiendo 4 generadores distintos pero matemáticamente idénticos. Ambas trampas producirían exactamente el mismo `(correct, vars)` para cualquier semilla pseudo-aleatoria, violando el propósito pedagógico de los 4 arquetipos disjuntos (Directo, Inverso, Perturbación, Frontera).
- **Solución:**
  - En `compile_shard.py` dentro de `[M3-ARCHETYPES]` (cuando `strict` y `eff_min_arch >= 4` y `len(tpls) >= 4`): evaluar dinámicamente las tuplas en `seed=100` (y comprobar `seed=101` para certificar determinismo).
  - Comparar los resultados `(correct, vars)` generados entre las tuplas. Si todas las tuplas devuelven exactamente la misma tupla `(correct, vars)` (menos de 2 salidas distintas), rechazar con un error explícito `[M3-ARCHETYPES]` indicando que las tuplas son clones matemáticos que no varían el problema entre arquetipos.

---

## 3. Plan de Acción
1. **Refactorizar `compile_shard.py`:**
   - Asociar `gen_raw` y `generator_code` a las estructuras de verificación de `templates_by_cid`.
   - Implementar resolución de AST por competencia según su fuente efectiva (`fix_files_by_cid` vs `shard_data_path` vs `generator_code`).
   - Implementar la verificación de diferenciación matemática con `seed=100` y `seed=101`.
2. **Actualizar Prompts Canónicos:**
   - En `prompt_shard_author.md` y `lean/prompt_shard_author.md`, detallar que además de enunciados distintos y uso de `arch`, los 4 arquetipos deben producir cálculos matemáticos distintos (rechazo automático de clones).
3. **Ampliar Tests Unitarios (`test_m3_archetypes_semantic_gate.py`):**
   - Test adversario 1: `_gen_h01(rng, arch=1)` con dummy `_ = arch` devolviendo clones matemáticos -> Rechazado por `[M3-ARCHETYPES]`.
   - Test adversario 2: Shard base con código roto de `H-01` reparado limpiamente mediante `shard_fixes/H-01.py` con 4 arquetipos válidos -> Compila `PASS` 100%.
4. **Verificación Formal:**
   - Ejecutar la suite completa mediante `.venv\Scripts\python.exe -m pytest ... -q` sin `--help` ni `python -c`.
   - Redactar `handoff.md` y notificar al Orquestador con `DONE:: Stream 1D Improver completado`.
