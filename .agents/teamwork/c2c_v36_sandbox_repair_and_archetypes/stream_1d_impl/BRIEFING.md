# Pre-Flight Sanity Check — Stream 1D

**Fecha:** 2026-10-25
**Agente:** Implementador Stream 1D (`impl_1d`)
**Objetivo:** Blindaje de compuerta semántica `[M3-ARCHETYPES]` en `compile_shard.py` y corrección del Ejemplo Canónico 1 en prompts de autor.

---

## 1. Inspección de Archivos Reales y Líneas

### A. `.agents/skills/content-to-course/compile_shard.py`
- **Líneas 1643–1664:** Bloque de compuerta Milestone 3 `[M3-ARCHETYPES]`.
  - Evalúa `len(tpls) < eff_min_arch`.
  - En la rama `else:`, únicamente evalúa:
    `distinct_tuples = {(t.get("stem_es", "").strip(), t.get("generator_code", "").strip()) for t in tpls}`
    con `len(distinct_tuples) < min(eff_min_arch, 2)`.
  - **Fallo confirmado:** Como los wrappers `gen_<cid>_<idx>` tienen nombres distintos generados sintéticamente en tiempo de carga (`gen_h01_1`, `gen_h01_2`, etc.), `generator_code` resulta ser una cadena distinta incluso si el autor usó un generador idéntico o pasó la misma lista de `stem_es` a las 4 tuplas.
- **Acceso al código fuente de los shards:**
  - `healed_source` o `raw_source` está disponible en `compile_shard_file` (líneas 1172–1179).
  - Adicionalmente, `tuple_records` preserva `rec["file_path"]` por tupla, permitiendo analizar tanto el AST global del shard como el AST de los generadores asociados a cada tupla.

### B. `.agents/skills/content-to-course/system_prompts/prompt_shard_author.md`
- **Líneas 245–302:** Ejemplo 1 (Carnot, H-01).
  - `def _gen_h01(rng, arch=1):` recibe `arch=1` pero jamás lee `arch` en el cuerpo.
  - Se define una única lista `stems_h01` reutilizada en las 4 tuplas de `TEMPLATES`.
  - Esto propaga la mala práctica a los autores LLM.

### C. `.agents/skills/content-to-course/system_prompts/lean/prompt_shard_author.md`
- **Líneas 26–55:** Ejemplo canónico H-01 en versión lean.
  - `def _gen_h01(rng, arch=1):` define `arch=1` pero jamás lo lee en su cuerpo.
  - Reutiliza la misma variable `stems` para las 4 tuplas de `TEMPLATES`.

### D. `tests/test_shard06_and_dry_archetypes.py`
- **Líneas 1051–1218:** `test_milestone3_min_archetypes_passes_with_compact_shared_helper_pattern`.
  - Implementa `_gen_c01(rng, arch)` donde `arch` sí se evalúa (`if arch == 1: ... elif arch == 2: ...`).
  - Las 4 tuplas usan 4 `stem` diferentes.
  - La suite actual pasa 55/55 pruebas exitosamente.

---

## 2. Plan de Implementación Quirúrgica

1. **Blindaje en `compile_shard.py`:**
   - **Verificación 1 (Stems distintos por arquetipo):**
     - Extraer `distinct_stems = {t.get("stem_es", "").strip() for t in tpls if t.get("stem_es", "").strip()}`.
     - Si `len(tpls) >= 2` y `len(distinct_stems) < min(eff_min_arch, len(tpls))`, emitir error `[M3-ARCHETYPES]`.
   - **Verificación 2 (Wrapper normalizado & AST de generadores con `arch` sin usar):**
     - Normalizar wrappers en `generator_code` (`norm_gen_codes`) quitando el sufijo numérico del wrapper `def gen_<cid>_<idx>(` -> `def _gen_wrapper_(`. Si `len(norm_gen_codes) < min(eff_min_arch, 2)`, emitir error.
     - Usar `ast.parse` sobre la fuente del archivo donde reside la tupla (o `healed_source` / `raw_source` / `shard_data_path`). Identificar funciones `FunctionDef` en el shard.
     - Para funciones con parámetro `arch`, inspeccionar si `arch` es leído (`ast.Name(id='arch', ctx=ast.Load())`) en cualquier nodo del cuerpo de la función.
     - Determinar si alguna tupla de la competencia `cid` invoca directa o indirectamente esa función (o si la función generadora `_gen_*` declarada para `cid` la referencia).
     - Si la función recibe `arch` pero no lo usa en el cuerpo, emitir el error descriptivo indicado en la especificación.

2. **Actualización de Prompts de Autor:**
   - En `prompt_shard_author.md`:
     - Ramificar en `_gen_h01(rng, arch=1)` por `arch == 1, 2, 3, 4`.
     - Definir 4 listas de stems (`stems_h01_1`, `stems_h01_2`, `stems_h01_3`, `stems_h01_4`) y asignarlas a cada tupla en `TEMPLATES`.
     - Agregar nota explícita sobre `[M3-ARCHETYPES]`.
   - En `lean/prompt_shard_author.md`:
     - Actualizar el snippet conciso de forma equivalente.

3. **Creación de Tests:**
   - `tests/test_m3_archetypes_semantic_gate.py` probando los 3 escenarios clave requeridos.
   - Ejecución completa de pytest para certificar regresiones cero.

## 3. Estado de Impedimentos
- Ningún bloqueo fuera de la frontera exclusiva de escritura. No se requiere `BLOCKER`.
