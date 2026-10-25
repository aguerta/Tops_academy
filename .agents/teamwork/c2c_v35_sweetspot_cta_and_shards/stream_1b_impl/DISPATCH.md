# DISPATCH — Stream 1B (Fase 1: Implementador `impl_1b`)

## 1. Rol y Frontera Exclusiva de Escritura (`Exclusive Write Boundaries`)
Eres el **Implementador del Stream 1B** bajo `/flash-triad-orchestrator`.
- **Carpeta de Gobernanza:** `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1b_impl/`
- **Archivos de Producción Permitidos (ÚNICOS que puedes modificar):**
  1. `.agents/skills/content-to-course/compile_shard.py`
  2. `.agents/skills/content-to-course/check_templates.py`
  3. `tests/test_shard06_and_dry_archetypes.py`
- **Artefactos de Gobernanza Permitidos:**
  - `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1b_impl/BRIEFING.md`
  - `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1b_impl/handoff.md`
- **PROHIBIDO** editar cualquier otro archivo del repositorio. Nunca pases `ArtifactMetadata` a `write_file` o `edit_file`.

## 2. Paso 0 Obligatorio (*Pre-Flight Sanity Check*)
Antes de realizar cualquier edición:
1. Lee `.agents/skills/content-to-course/compile_shard.py` (especialmente L1040–L1690) y `.agents/skills/content-to-course/check_templates.py` (`render_compact_aggregated_errors` L1207–L1415) y `tests/test_shard06_and_dry_archetypes.py`.
2. Escribe `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1b_impl/BRIEFING.md` confirmando líneas y firmas reales. Si detectas un bloqueo fuera de tu frontera, detén ediciones y envía `BLOCKER:: <archivo:línea> | <causa> | <opciones>` al Orquestador (`7d2e6386-9933-4c70-9e50-a3cf214925f6`).

## 3. Especificación Técnica de Implementación

### A. Conteo Estructurado `error_count` y `has_syntax_error` en `.check_attempts/compile_<shard_id>.json` (`compile_shard.py`)
1. **Problema:** `c2c_hook_guard.py` necesita conocer con exactitud cuántos errores/bloques fallaron en la última compilación del shard (`error_count`) y si hubo un `SyntaxError` (`has_syntax_error`) para aplicar el umbral oficial `< 6` (`1..5` errores = `edit_file` obligatorio vs `>= 6` errores = `shard_fixes/<CID>.py` o `write_file`).
2. **Solución en `compile_shard.py`:**
   - Añadir un helper `count_distinct_shard_error_hunks(raw_errors: List[Any]) -> int` (o exportarlo desde `check_templates.py` y llamarlo en `compile_shard.py`) que cuente cuántos ítems/diagnósticos deduplicados produce `render_compact_aggregated_errors` (es decir, `total_items = sum(len(err_map) for file_map in grouped.values() for err_map in file_map.values())`, garantizando `>= 1` cuando `raw_errors` no está vacío). De este modo, si una plantilla falla en 50 semillas por la misma regla `(cid, rule_tag, cause)`, cuenta como **1 error lógico/hunk** que el autor repara con 1 `edit_file`, y no como 50 errores!
   - En `_fail(msg: str, has_syntax_error: bool = False, error_count: int = 1)` (L1087):
     - Guardar en `state["error_count"] = error_count` y `state["has_syntax_error"] = bool(has_syntax_error)` dentro de `.check_attempts/compile_{norm_shard_id}.json` (y también en `r_data["error_count"]` y `r_data["has_syntax_error"]` si se escribe `receipt_p`).
     - Cuando `_fail` se invoca por `locator.syntax_error` (L1173 o L1225) o por un `SyntaxError` durante `compile(...)`, pasar `has_syntax_error=True, error_count=1`.
   - En el bloque `if not is_clean:` (L1604–L1650):
     - Calcular `error_count = count_distinct_shard_error_hunks(raw_errors)`.
     - Guardar `state["error_count"] = error_count` y `state["has_syntax_error"] = False` en `.check_attempts/compile_{norm_shard_id}.json` y en `receipt_p`.

### B. Directiva Dinámica del Umbral Oficial `< 6` en `render_compact_aggregated_errors` (`check_templates.py` y `compile_shard.py`)
1. En `render_compact_aggregated_errors` (`check_templates.py` L1370–L1414):
   - Sea `hunk_count = total_items` (el número de diagnósticos consolidados únicos).
   - Construir una línea de directiva de acción al final del reporte (respetando estrictamente el tope `max_output_lines`, reservando la última línea para que `len(res_str.splitlines()) <= max_output_lines` siga cumpliéndose al 100% en todos los tests existentes):
     - Si `1 <= hunk_count < 6`:
       `[UMBRAL < 6 ({hunk_count}/5 errores)]: Usa edit_file (replace_file_content) quirúrgico en las líneas indicadas; PROHIBIDO write_file completo.`
     - Si `hunk_count >= 6`:
       `[UMBRAL >= 6 ({hunk_count} errores)]: Usa write_file modular en shard_fixes/<CID>.py (1-2 comps) o write_file(Overwrite=True) completo.`
2. En `compile_shard.py` (L1647), incluir en el mensaje de fallo impreso en `stderr` el conteo deduplicado `error_count` además de `len(raw_errors)` para que el subagente vea inmediatamente si está en `< 6` (`edit_file`) o `>= 6` (`shard_fixes` / `write_file`).

## 4. Verificación y Entrega
1. Amplía `tests/test_shard06_and_dry_archetypes.py` con tests unitarios que comprueben:
   - Que ante 1 a 5 errores consolidados (incluso si un mismo error se repite en múltiples semillas), `compile_shard.py` persiste `"error_count"` entre `1` y `5` y `"has_syntax_error": False` en `.check_attempts/compile_<shard_id>.json`, y el reporte incluye `[UMBRAL < 6 ...]`.
   - Que ante `>= 6` errores consolidados distintos, `compile_shard.py` persiste `"error_count" >= 6` y el reporte incluye `[UMBRAL >= 6 ...]`.
   - Que ante un `SyntaxError` en `shard_XX_data.py`, `compile_shard.py` persiste `"has_syntax_error": True` y `"error_count": 1`.
   - Que `render_compact_aggregated_errors` nunca excede `max_output_lines` (`<= 28` líneas por defecto).
2. Ejecuta `.venv\Scripts\python.exe -m pytest tests/test_shard06_and_dry_archetypes.py tests/test_compile_shard.py tests/test_shard_compiler_hardening.py tests/test_check_templates.py -q`.
3. Escribe `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1b_impl/handoff.md` y envía `DONE:: Stream 1B Implementer completado` a `7d2e6386-9933-4c70-9e50-a3cf214925f6`.
