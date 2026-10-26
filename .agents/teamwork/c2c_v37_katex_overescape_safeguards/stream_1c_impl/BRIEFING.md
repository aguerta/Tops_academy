# BRIEFING — Stream 1C (Fase 1: Implementador)

- **Parent Conversation ID:** `da4d9acf-34da-4bc8-930b-6fb3d28b5744`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1c_impl`
- **Timestamp:** 2026-10-25T18:42:00-05:00

## 1. Confirmación de Lectura y Pre-Flight Sanity Check
Se han leído y verificado completamente:
1. `DISPATCH.md`: Especificaciones precisas para `invariants.py`, `compile_shard.py`, y suite de tests R-23.
2. `engine/invariants.py`: `validate_katex_syntax` (líneas 268-452) actualmente concluye en la Regla 10 (`check_unrendered_placeholders`). Se integrarán de forma modular las Reglas 11 (R-23 overescaped commands), 12 (KaTeX inline linebreak `\\` fuera de entornos matriciales/casos), y 13 (prohibición de `\centernot` y `_` sin escapar en `\text{...}`).
3. `compile_shard.py`: `heal_shard_source_text` (líneas 84-132) procesa tokens mediante `tokenize`. Se identificó la causa raíz de la corrupción: `_bs = "\\"` en sustituciones `re.sub` fallaba con `re.error: bad escape \R` cayendo al bloque `except Exception:`, el cual sobre-escapaba strings raw. Se aplicará el colapso de doble barra en `is_raw`, lookbehind `(?<!\\)` en reemplazos de flechas y macros KaTeX, y protección del fallback ante strings raw.
4. `tests/test_engine_invariants_adversarial.py`: 53 tests ejecutados y pasando al 100% como baseline.

## 2. Frontera Exclusiva de Escritura
Se respetará estrictamente el límite de escritura disjunto:
1. `.agents/skills/content-to-course/engine/invariants.py`
2. `.agents/skills/content-to-course/compile_shard.py`
3. `tests/test_invariants_and_shard_overescape_r23.py` `[NEW]`
4. `.agents/teamwork/c2c_v37_katex_overescape_safeguards/stream_1c_impl/BRIEFING.md` `[NEW]`
5. `.agents/teamwork/c2c_v37_katex_overescape_safeguards/stream_1c_impl/handoff.md` `[NEW]`

No se tocarán archivos fuera de esta frontera ni se dejarán archivos temporales en el repositorio.

## 3. Plan de Implementación Quirúrgica
1. **Paso 1:** Editar `invariants.py` para agregar las Reglas 11, 12 y 13 en `validate_katex_syntax`.
2. **Paso 2:** Editar `compile_shard.py` para corregir `heal_shard_source_text` en strings raw, deduplicación de barras y fallback protegido.
3. **Paso 3:** Crear `tests/test_invariants_and_shard_overescape_r23.py` con cobertura completa para todos los casos solicitados.
4. **Paso 4:** Ejecutar `.venv\Scripts\pytest.exe tests/test_invariants_and_shard_overescape_r23.py tests/test_engine_invariants_adversarial.py -q`.
5. **Paso 5:** Redactar `handoff.md` y emitir reporte de conclusión `DONE:: Stream 1C Impl completado`.
