# DISPATCH — Stream 1B (Fase 1: Implementador)

- **Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1b_impl`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\compile_shard.py`
2. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\c2c_hook_guard.py`
3. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_m3_archetypes_semantic_gate.py`
4. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_compile_shard.py`
5. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_shard_compiler_hardening.py`
6. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_shard06_and_dry_archetypes.py`
7. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_invariants_and_shard_overescape_r23.py`
8. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_latex_engine.py`
9. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_hook_post_pass_and_write_isolation.py`
10. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_watchdog_and_hooks.py`
11. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1b_impl\BRIEFING.md` `[NEW]`
12. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1b_impl\handoff.md` `[NEW]`

PROHIBIDO modificar cualquier otro archivo.

## Reglas Pre-Flight y Guardias de Entorno
- **Hooks:** Prohibido ejecutar `run.py --help` / `dispatch.py --help` o `python -c` mencionando `"content-to-course/"` junto con `open(`, `read_text`, `run.py`, `prepare.py`, `ingest.py`, `dispatch.py`. Usa `read_file` para leer código y `& ".venv\Scripts\python.exe" -m pytest <archivos_test> -q`.
- **Seguridad `c2c_hook_guard.py`:** Mantén únicamente imports de Python stdlib, bloque `try ... except BaseException:` de alto nivel y `sys.exit(0)` siempre. Prohibido dejar `.c2c_subagent_lock.json` activo fuera de `tmp_path`.
- **Zero-Domain (`test_skill.py`):** En NINGÚN `.py` de `content-to-course/` pueden aparecer (ni siquiera en comentarios) las subcadenas en minúsculas: `edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`. ¡Cuidado en español con `puedo`, `quedo`, `heredo` (`edo`) o `regresión` (`regresi`)! Usa inglés en comentarios de `.py`.

## Especificación Técnica

### 1. `compile_shard.py` (`P0.2` + `Brecha 1`)
1. **Contrato único `Form-B` (Retiro total de `Form-A`):**
   - Rechazar cualquier definición legacy `Form-A`; exigir en `TEMPLATES` exclusivamente la 9-tupla `Form-B`:
     `(tpl_id, cid, qtype, gen_fn, ver_fn, (difficulty, bloom), stems, hints, solution)`
   - Exigir que el elemento `[5]` sea explícitamente una 2-tupla/lista `(difficulty, bloom)` (rechazando strings sueltos que antes inyectaban `bloom="Understand"` silenciosamente), con `difficulty in {"easy", "medium", "hard"}` y `bloom in {"Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"}`.
2. **Eliminación de inyección anti-socrática en `hints`:**
   - Eliminar `_format_socratic_step` y todo fallback que sintetice pistas copiando `wrong_belief` desde `cta.json`.
   - Exigir `3 <= len(hints) <= 5` pistas explícitas del autor, cada una con `len(h.strip()) >= 25` caracteres, rechazando copias literales de `wrong_belief` o muletillas anti-socráticas (`"Evita el error común"`, `"Recuerda no confundir"`, etc.).
3. **Eliminación de `1.333x` / `"Opción alterna N"` / fallback posicional `0..5` y compuerta `[TPL-DYNAMIC-RATIONALE]` (`Brecha 1`):**
   - Eliminar por completo multiplicadores mágicos (`1.333`, `"Opción alterna N"`, etc.) y asignación posicional ciega `0..5` de IDs de distractores. Todo `distractor_id` debe existir explícitamente en los distractores de esa competencia en `cta.json`.
   - **En `--strict` (`strict=True`), eliminar la 2-tupla opcional `(distractor_id, value)`:**
     - En `MC7`, cada distractor debe ser una 3-tupla `(distractor_id, value, error_rationale)` (o dict `{"distractor_id": ..., "value": ..., "error_rationale": ...}`) con `len(error_rationale.strip()) >= 20`.
     - En `MS` (`multiple_select`), toda opción falsa (`is_correct=False`) debe incluir `"distractor_id"` válido de `cta.json` y `"error_rationale"` explícito con `len(error_rationale.strip()) >= 20`.
     - **Anclaje determinista `@var@` (`[TPL-DYNAMIC-RATIONALE]`):** cuando `vars` no esté vacío y el `value`/`content` del distractor contenga tokens `@var@` (o la plantilla tenga variables numéricas/simbólicas e interpole `@var@` en `correct`/`stem` con distractores calculados desde `vars`), exigir que `error_rationale` contenga al menos un token `@var@` cuyo nombre exista en `vars`. Si se omite o es 100% estático, abortar compilación con `[TPL-DYNAMIC-RATIONALE]`.
   - **Guardia KaTeX para `FIB` (`fill_blank`):** rechazar delimitadores `$` externos en `correct`, `value` o `canonical_algebraic` de `FIB` (ya que `FeedbackToast.tsx` envuelve respuestas `FIB` en `$...$`).
   - **Extracción `distractor_ids` en `MS`:** poblar `tpl["distractor_ids"]` extrayendo en dry-run los `"distractor_id"` de las opciones con `is_correct=False` en `MS` (además de `MC7`) para que `check_templates.py` valide `TPL-D3` en competencias multimodales.
4. **Eliminación de `generate_rich_stem_variants`:**
   - Borrar `generate_rich_stem_variants` y conservar los `stems` genuinos escritos por el autor, exigiendo `len(stems) >= 3` enunciados distintos por plantilla.
5. **Verificadores `ver_fn` no triviales y Gate `[M3-ARCHETYPES]` Tri-Banda Multimodal (`min_archetypes = 3`):**
   - Cambiar default de `--min-archetypes` a `3`.
   - Rechazar por inspección AST cualquier `ver_fn` trivial que haga `return True` directo o constante sin inspeccionar su argumento/resultado ni evaluar una condición matemática/lógica real.
   - En `--strict` (cuando `min_archetypes >= 3`), exigir por competencia:
     - `>= min_archetypes` (`>= 3`) plantillas;
     - cobertura completa de las 3 bandas `{"easy", "medium", "hard"}`;
     - `>= 2` niveles `bloom` distintos;
     - práctica activa: `>= 2` plantillas `qtype in {"FIB", "MS"}` cuando la competencia sea `Hab-*` (o `type == "Skill"` en `cta.json`), y `>= 1` plantilla `qtype in {"FIB", "MS"}` cuando sea `C-*` / `H-*` (`Concept` / `Misconception`).
   - En `_eval_tuple_output` (huella de equivalencia semántica entre arquetipos): incluir la huella de `"options"` para `MS` (donde `correct` es `None`), evitando falsas colisiones entre dos plantillas `MS` distintas.

### 2. `c2c_hook_guard.py`
- Actualizar el mensaje guía de `[M3-ARCHETYPES]` (`~L825-840`) al nuevo contrato `Form-B` Tri-Banda Multimodal (`--min-archetypes 3`, bandas `easy/medium/hard`, `>= 2` Bloom, `FIB`/`MS` obligatorio y 3-tupla `(did, val, error_rationale_@var@)`), preservando intactos todos los guards existentes, stdlib pura, `try ... except BaseException:` y `sys.exit(0)`.

### 3. Actualización y Ampliación de las 8 Suites de Tests Exclusivas
Migra todos los fixtures de las 8 suites al contrato `Form-B` Tri-Banda con 3-tuplas `(did, val, rationale_@var@)`, `ver_fn` reales y `hints >= 25` chars, y añade tests específicos para:
- Rechazo de `Form-A`, rechazo de `(difficulty)` sin `bloom`, rechazo de 2-tupla `(did, val)` y rechazo `[TPL-DYNAMIC-RATIONALE]` cuando un distractor paramétrico carece de `@var@` en `error_rationale`.
- Rechazo de `ver_fn` trivial (`return True`), rechazo de `$` externos en `FIB`, extracción de `distractor_ids` en `MS`, y validación Tri-Banda (`easy/medium/hard` + `FIB`/`MS` por `Hab-*` vs `C-*`).

## Verificación
Ejecuta:
```powershell
& ".venv\Scripts\python.exe" -m pytest tests/test_m3_archetypes_semantic_gate.py tests/test_compile_shard.py tests/test_shard_compiler_hardening.py tests/test_shard06_and_dry_archetypes.py tests/test_invariants_and_shard_overescape_r23.py tests/test_latex_engine.py tests/test_hook_post_pass_and_write_isolation.py tests/test_watchdog_and_hooks.py -q
```
Escribe `BRIEFING.md` antes de editar, `handoff.md` al terminar y notifica a `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589` con `DONE:: Stream 1B Impl completado (<N> passed)`.
