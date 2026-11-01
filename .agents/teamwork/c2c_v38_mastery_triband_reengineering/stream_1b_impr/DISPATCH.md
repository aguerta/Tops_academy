# DISPATCH — Stream 1B (Fase 2: Mejorador)

- **Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1b_impr`
- **Impl Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1b_impl\handoff.md`

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
11. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1b_impr\handoff.md` `[NEW]`

PROHIBIDO tocar cualquier otro archivo.

## Objetivos de Endurecimiento (Fase 2 — Mejorador)
*(Nota de eficiencia: usa `read_file` con rangos de `400-800` líneas por llamada).*

1. Lee `stream_1b_impl/handoff.md` y revisa con `read_file` los cambios en `compile_shard.py`, `c2c_hook_guard.py` y las 8 suites asignadas.
2. **Contratos Críticos Inter-Stream con `Stream 1C` (`dispatch.py`/`prompts`) y `Stream 1D` (`check_templates.py`):**
   - **Default `min_archetypes`:** verifica que cuando `min_archetypes` no se pase explícitamente por CLI ni en el manifest (`None`), bajo `strict=True` el default efectivo sea `3` (mientras si un test pasa explícitamente `min_archetypes=1` o `min_archetypes=4` o el manifest declara `"min_archetypes"`, se respete ese valor explícito).
   - **Compuerta `[TPL-DYNAMIC-RATIONALE]` (`Brecha 1`):**
     - Verifica que en `--strict` tanto `MC7` (2-tupla `(did, val)`) como `MS` (opción falsa sin `"error_rationale"` o `< 20` chars) sean rechazados determinísticamente con diagnóstico de línea exacto.
     - Verifica que cuando un distractor paramétrico (`@var@` en `val`, o plantilla cuantitativa/simbólica con `@var@` en `correct`/`stem`) trae un `error_rationale` 100% estático sin ningún token `@var@` válido de `vars`, falle explícitamente con el tag `[TPL-DYNAMIC-RATIONALE]`.
   - **Extracción `distractor_ids` en `MS` y guardia `$` en `FIB`:**
     - Confirma que una competencia `Hab-*` compuesta por `2 FIB + 1 MS` (cero `MC7`) compile limpiamente con `strict=True` poblando `tpl["distractor_ids"]` en la plantilla `MS` y pasando `check_templates.py` (`TPL-D3`).
     - Confirma que respuestas `FIB` con delimitadores `$` externos (`"$42$"`, `"$x + 1$"`) fallen de inmediato en `compile_shard.py`.
   - **Eliminación total de código muerto anti-socrático / sintético:**
     - Confirma que NO queden residuos de `Form-A`, `_format_socratic_step`, `generate_rich_stem_variants`, `1.333`, `"Opción alterna"` ni asignación posicional `0..5`.
   - **Seguridad `c2c_hook_guard.py` y Regla Zero-Domain:**
     - Verifica stdlib pura, `try ... except BaseException:` y `sys.exit(0)` en `c2c_hook_guard.py`.
     - Escanea `compile_shard.py` y `c2c_hook_guard.py` confirmando **0 subcadenas Zero-Domain prohibidas** (`edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi` — atención a `puedo`/`quedo`/`heredo`/`regresión`).

## Verificación
Ejecuta (sin usar `--help` sobre scripts de `content-to-course/` ni `python -c` leyendo `"content-to-course/"`):
```powershell
& ".venv\Scripts\python.exe" -m pytest tests/test_m3_archetypes_semantic_gate.py tests/test_compile_shard.py tests/test_shard_compiler_hardening.py tests/test_shard06_and_dry_archetypes.py tests/test_invariants_and_shard_overescape_r23.py tests/test_latex_engine.py tests/test_hook_post_pass_and_write_isolation.py tests/test_watchdog_and_hooks.py -q
```
Escribe `handoff.md` en `stream_1b_impr/` y envía `DONE:: Stream 1B Impr completado (<N> passed)` a `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`.
