# DISPATCH — Tier A Hotfix (`tier_a_2b_fix` — Resolución de `BLOCKER:: Stream 2B`)

- **Parent Conversation ID:** `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\tier_a_2b_fix`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\compile_shard.py`
2. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\system_prompts\lean\prompt_shard_author.md`
3. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\system_prompts\prompt_shard_author.md`
4. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\subagent_types.json`
5. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\tier_a_2b_fix\handoff.md` `[NEW]`

PROHIBIDO tocar cualquier otro archivo (`Stream 2A` y `Stream 2C` están ejecutándose en paralelo sobre `run.py` y sus suites).

## Especificación Quirúrgica (Resolución 100% Verificada de `BLOCKER:: Stream 2B`)

1. **`compile_shard.py` (`extract_function_code`, `ShardDataLineLocator`, `prune_ast_dependencies`, `~L820-L965`):**
   - Añade soporte completo para funciones asignadas como `lambda` (`gen_x = lambda rng: ...` o `ver_x = lambda c, v: ...`):
     * En `ShardDataLineLocator` y `prune_ast_dependencies`, registra asignaciones de nivel superior `ast.Assign` cuyo `value` sea `ast.Lambda` (con `len(targets) == 1` y `isinstance(targets[0], ast.Name)`), extrayendo el segmento exacto de ese nodo AST (`ast.get_source_segment` o líneas/columnas `lineno..end_lineno`, `col_offset..end_col_offset`) para que dos declaraciones separadas por `;` en la misma línea NO se mezclen.
     * En `extract_function_code`, si `fn_or_str` tiene `__name__ == "<lambda>"` usa `fn_name_hint` como `orig_name`; y si `raw_src` es una asignación lambda `name = lambda <args>: <expr>` (o expresión `lambda <args>: <expr>`), transfórmala limpiamente con `ast` en:
       ```python
       def {target_name}(<args>):
           return <expr>
       ```
     * Mantén comentarios en inglés (Zero-Domain invariant) y re-compactación JSON intacta.

2. **`system_prompts/lean/prompt_shard_author.md` (`<= 4,750` bytes, LF puro `\n`) y `system_prompts/prompt_shard_author.md` (LF puro `\n`):**
   - Asegúrate de que el ejemplo canónico `Form-C` (`Hab-01 Carnot Cycle`) en AMBOS archivos compile y apruebe **100% limpio y sin warnings** en `compile_shard.py --strict --min-archetypes 4` (50 semillas), `instantiate_competency`, `validate_course_content(..., strict=True)` y `standardized_audit_engine.run_full_audit`:
     * **PROHIBIDO `import re`** en el snippet del ejemplo (recuerda que `engine/sandbox.py` prohíbe `re` en `ALLOWED_ROOT_MODULES`, permitiendo `math`, `fractions`, `statistics`, `sympy`, `numpy`, `scipy`, `random`, `decimal`). Parsea el número en `_pv(c)` con Python puro sin imports:
       `def _pv(c): return float(str(c).split("=")[-1].replace("$", "").strip())`
     * **Usa `def` explícitos** (`def gen_h01_1(r): return _gen_h01(r, 1)` ... `def ver_h01_1(c, v): ...`) en lugar de `lambda`s.
     * **Garantía Algebraica Universal Anti-Colisión y Cero Multiplicador Mágico en los 6 distractores de `arch == 1`:**
       Usa `tc = rng.randint(200, 280); th = tc + rng.randint(460, 650); eta = round(1.0 - tc/th, 3)` ($r = T_C/T_H \in [0.215, 0.378]$) y los 6 distractores disjuntos sin ningún múltiplo constante de `eta`:
       `v1 = (th/tc, tc/th, 1-(tc/th)**2, 1-0.6*tc/th, (th-tc)/(th+tc), (tc/th)**2)`
       (donde $d_6 < d_2 < d_5 < \eta < d_4 < d_3 < d_1$ con brecha mínima $\ge 0.047$ en las 15,471 combinaciones y 0 multiplicadores mágicos!). Actualiza `RATS` correspondientemente (con `@tc@`/`@th@`, `>= 20` chars y longitudes balanceadas).
     * En `arch == 4` (`MS`), verifica que las 4 opciones tengan longitudes balanceadas (`R-16`), sintaxis KaTeX limpia sin meta-pistas (`R-18`), `distractor_id` + `error_rationale` dinámico en las falsas, y que `ver_h01_4(res)` verifique la verdad matemática de las opciones seleccionadas (no tautológico).
     * Verifica también que los `stems` `(CTX, Qk)` generen `>= 15` stems únicos entre los 4 arquetipos (ej. `len(CTX) == 2` y `len(Qk) == 2` dan `4 * 4 = 16 >= 15` stems únicos cuando cada enunciado es distinto y tiene `@tc@`/`@th@`/`@eta@`), `hints` `>= 25` chars sin filtrar la respuesta, y que `lean/prompt_shard_author.md` conserve todas las cadenas obligatorias de `test_c2c_v321_comp4_prompts.py` (`## 0. SCOPE-LOCK`, `DONE:`, `compile_shard.py`, `Física`, `Sistemas Distribuidos`, `línea`, `stem_variants`, `ArtifactMetadata`, `MC7`, `FIB`, `MS`, `RATS`, `assumption_id`) pesando **`<= 4,750` bytes** y `0` bytes `\r`!

3. **Regenera `subagent_types.json` con LF puro (`\n`, `0` bytes `\r`)** usando `dispatch.get_type_definitions(lean=True)`.

4. **Prueba Empírica End-to-End antes de reportar `DONE::`:**
   - Ejecuta un test rápido en `pytest` sobre:
     `& ".venv\Scripts\python.exe" -m pytest -o addopts="" tests/test_compile_shard.py tests/test_c2c_v321_comp4_prompts.py tests/test_dispatch_turn0_and_milestone3_prompts.py tests/test_skill.py -k "not dummy_nonexistent" -q`
   - Y comprueba en Python sobre un `tmp` temporal (que luego se limpia automáticamente) que extraer el bloque ```` ```python ... ``` ```` de `lean/prompt_shard_author.md` y correr `compile_shard(tmp_work, "shard_01", strict=True, min_archetypes=4)` devuelve `(True, [])` a la primera!
   - Escribe `tier_a_2b_fix/handoff.md` y envía `DONE:: Tier A 2B Fix` a `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`.
