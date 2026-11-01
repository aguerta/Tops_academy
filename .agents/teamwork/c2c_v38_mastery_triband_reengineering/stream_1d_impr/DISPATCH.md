# DISPATCH — Stream 1D (Fase 2: Mejorador)

- **Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1d_impr`
- **Impl Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1d_impl\handoff.md`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\check_templates.py`
2. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\engine\invariants.py`
3. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\engine\assemble.py`
4. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\examples\edo\templates\*.json`
5. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\examples\edp\templates\*.json`
6. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_engine_invariants_adversarial.py`
7. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_assemble_katex_and_rationale.py`
8. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_assemble_sanitize_katex_r23.py`
9. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_katex_prairielearn_tokens.py`
10. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_c2c_error_aggregation.py`
11. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_sandbox_adversarial.py`
12. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_sandbox_gil_and_circuit_breaker.py`
13. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_template_variability.py`
14. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1d_impr\handoff.md` `[NEW]`

PROHIBIDO tocar cualquier otro archivo.

## Objetivos de Endurecimiento (Fase 2 — Mejorador)
1. Lee `stream_1d_impl/handoff.md` y revisa con `read_file` los cambios en `check_templates.py`, `engine/invariants.py`, `engine/assemble.py`, `examples/{edo,edp}/templates/*.json` y las 8 suites asignadas.
2. **Endurecimiento de `[TPL-STATIC-OPT]` (`Matiz 4b`) y `[TPL-DYNAMIC-RATIONALE]` (`Brecha 1`):**
   - Verifica explícitamente el caso adversario donde `vars == {}` / `domain == {}` está completamente vacío y `N >= 2` semillas producen `len(unique_correct) == 1`: debe fallar SIEMPRE con `[TPL-STATIC-OPT]` bajo `strict=True` (tanto en `MC7`, como en `fill_blank`, como en `multiple_select`).
   - Verifica que en `multiple_select` (`MS`), donde `tpl["distractor_ids"]` viene poblado por `compile_shard.py` (`Stream 1B`) desde opciones falsas `is_correct=False`, `TPL-D3` valide limpiamente competencias multimodales (`100% FIB + MS` con `>= 2` IDs válidos de `cta.json`, `100% FIB` sin falsos bloqueos, y `6/6` cuando existe `>= 1` plantilla `MC7`).
   - Verifica en `[TPL-DYNAMIC-RATIONALE]` (`strict=True`, `num_dry_run_seeds >= 15`) que: (a) un distractor `MC7` o `MS` cuyo `content` varía entre semillas pero cuyo `error_rationale` es estático sea bloqueado por slot individual; (b) `rationale_uniqueness_pct < 35.0%` en `>= 30` distractores de la competencia sea bloqueado; y (c) un distractor puramente conceptual invariante en una plantilla conceptual de rotación no genere falsos positivos si su propio `content` no varía en esas semillas específicas mientras la competencia cumple `>= 35%`.
3. **Endurecimiento de `[KATEX-PROSE-OVERFLOW]`, `[R-18]` y `assemble.py`:**
   - En `engine/invariants.py`, verifica llaves anidadas dentro de `\text{...}`, `\textrm{...}`, `\mathrm{...}` (ej. `\text{valor de $x_{i}$ ...}`), frontera exacta `45` (pasa) vs `46` (falla con `[KATEX-PROSE-OVERFLOW]`, nunca `R-23`), y desenvoltura en `[R-18]`.
   - En `engine/assemble.py`, verifica interpolación simultánea de `@n@`, `@k@`, `@c@` junto con preservación intacta de `${k}^*$` y `$\mathbb{R}^{n}$` cuando `is_cta=True` y `is_cta=False`.
   - Confirma **0 subcadenas Zero-Domain prohibidas** (`edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`) en todos los `.py` fuera de `examples/`.
   - Ejecuta `check_templates.py` (en tests) contra `examples/edo/templates/*.json` y `examples/edp/templates/*.json` en modo `strict=True` confirmando `0` errores.

## Verificación
Ejecuta (sin usar `--help` sobre scripts de `content-to-course/` ni `python -c` leyendo `"content-to-course/"`):
```powershell
& ".venv\Scripts\python.exe" -m pytest tests/test_engine_invariants_adversarial.py tests/test_assemble_katex_and_rationale.py tests/test_assemble_sanitize_katex_r23.py tests/test_katex_prairielearn_tokens.py tests/test_c2c_error_aggregation.py tests/test_sandbox_adversarial.py tests/test_sandbox_gil_and_circuit_breaker.py tests/test_template_variability.py -q
```
Escribe `handoff.md` en `stream_1d_impr/` y envía `DONE:: Stream 1D Impr completado (<N> passed)` a `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`.
