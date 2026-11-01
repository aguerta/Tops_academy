# DISPATCH — Stream 1D (Fase 1: Implementador)

- **Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1d_impl`

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
14. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1d_impl\BRIEFING.md` `[NEW]`
15. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1d_impl\handoff.md` `[NEW]`

PROHIBIDO modificar cualquier otro archivo.

## Reglas Pre-Flight y Guardias de Entorno
- **Hooks:** Prohibido ejecutar `run.py --help` / `dispatch.py --help` o `python -c` mencionando `"content-to-course/"` junto con `open(`, `read_text`, `run.py`, `prepare.py`, `ingest.py`, `dispatch.py`. Usa `read_file` y `& ".venv\Scripts\python.exe" -m pytest <archivos_test> -q`.
- **Zero-Domain (`test_skill.py`):** En `check_templates.py`, `engine/invariants.py` y `engine/assemble.py` (cualquier `.py` fuera de `examples/`), PROHIBIDO incluir (ni en comentarios ni en strings) las subcadenas en minúsculas: `edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`. ¡Cuidado en español con `puedo`, `quedo`, `heredo` (`edo`) o `regresión` (`regresi`)!
- **Tag KaTeX:** Usa `[KATEX-PROSE-OVERFLOW]`, NUNCA `"R-23"`.
- **Compatibilidad `strict=False`:** Aplica las nuevas compuertas estrictas bajo `strict=True` (default en producción/CLI) para no romper micro-fixtures unitarios legacy que invocan `strict=False`.

## Especificación Técnica

### 1. `check_templates.py` (`P0.4` + `Brecha 1` + `Matiz 4b`)
1. **Compuerta `[TPL-STATIC-OPT]` Incondicional (`Matiz 4b`):**
   - Bajo `strict=True`, recolectar las respuestas correctas normalizadas a lo largo de las instancias renderizadas en dry-run (`N = min(20, num_dry_run_seeds)`):
     - Para `MC7` / `fill_blank`: contenido/valor normalizado de la respuesta correcta; para `multiple_select`: frozenset de opciones correctas `(content, is_correct)`.
     - **Bloqueo incondicional de mono-clave:** si `N >= 2` y `len(unique_correct) == 1`, rechazar **SIEMPRE** con `[TPL-STATIC-OPT]`, **incluso cuando el autor dejó `vars == {}` / `domain == {}` vacío** para intentar fingir que la plantilla no es paramétrica.
     - Cuando `num_dry_run_seeds >= 15`: exigir `len(unique_correct) >= min(10, max(4, N // 2))` en plantillas cuantitativas/simbólicas o de competencias `Skill`/`Hab-*`, y `len(unique_correct) >= 4` en rotación conceptual; en `multiple_select`, exigir `len(unique_option_sets) > 1`.
     - En `check_competency_diversity` (`strict=True`): cuando el pool renderizado de la competencia tenga `>= 20` ítems, exigir que ninguna clave correcta individual concentre `> 20%` (`0.20`) de las instancias (`[TPL-STATIC-OPT]`).
2. **Compuerta `[TPL-DYNAMIC-RATIONALE]` en Dry-Run (`Brecha 1`):**
   - Bajo `strict=True` y `num_dry_run_seeds >= 15`:
     - Para cada slot de distractor (`MC7` o opción falsa `MS`) cuyo `content` renderizado varíe entre semillas (`len(unique_contents) > 1`), exigir que su `error_rationale` renderizado **TAMBIÉN varíe entre semillas** (`len(unique_rationales) > 1`). Si permanece constante (`len == 1`), rechazar con `[TPL-DYNAMIC-RATIONALE]`.
     - En `check_competency_diversity` (`strict=True`), cuando el banco renderizado de la competencia tenga `>= 30` distractores totales, exigir `rationale_uniqueness_pct >= 35.0%` (`len(unique_rationales) / total_rationales >= 0.35`), fallando con `[TPL-DYNAMIC-RATIONALE]`.
3. **Verificador `cross_check_py` no trivial, `hints >= 25` chars, `TPL-D3` multimodal y calibración de `stems`:**
   - Bajo `strict=True`: rechazar por AST scripts `cross_check_py` vacíos o triviales (ej. asignar `result = True` constante sin evaluar operaciones/comparaciones sobre variables o respuesta).
   - Bajo `strict=True`: exigir `len(hint.strip()) >= 25` caracteres en cada pista.
   - **`TPL-D3` multimodal:** si la competencia tiene `>= 1` plantilla `MC7`, mantener exigencia de `6/6` IDs de `cta.json`; si la competencia tiene `0` plantillas `MC7` (`100% FIB + MS`), exigir `>= 2` IDs válidos de `cta.json` cuando haya `MS` (y `0` solo si es `100% FIB`).
   - **Diversidad de `stems`:** conservar la firma default `evaluate_competency_diversity(stems, min_diversity_ratio=0.5)` intacta para callers unitarios directos, pero en `check_competency_diversity` / `validate_template_file` calibrar el umbral sobre esqueletos enmascarados a `0.25` combinado con `>= 0.85` de unicidad en enunciados renderizados no enmascarados (cuando hay parámetros), de modo que `>= 3` stems genuinos pasen sin `generate_rich_stem_variants`.

### 2. `engine/invariants.py`
- Añadir validación `[KATEX-PROSE-OVERFLOW]`: rechazar cualquier bloque `\text{...}`, `\textrm{...}`, `\mathrm{...}` (con conteo balanceado de llaves) cuyo contenido interno supere `45` caracteres (usando código/tag `[KATEX-PROSE-OVERFLOW]`, jamás `"R-23"`).
- En `check_synthetic_boilerplate_distractors()` (`[R-18]`): desenvolver `\text{...}` / `\textrm{...}` dentro de `$...$` antes de extraer esqueletos estructurales para que prosa camuflada dentro de `$\text{...}$` sea auditada igual que texto plano.

### 3. `engine/assemble.py`
- En los puntos de interpolación con `is_cta=True` (`~L439, L684`): interpolar TODOS los tokens ortogonales `@var@` sin importar la longitud del identificador (`len(k) >= 1`, ej. `@n@`, `@k@`, `@c@`, `@a@`), manteniendo el filtro `len(k) > 2` **únicamente** para llaves simples legacy `{var}` de modo que expresiones LaTeX como `${k}^*$` permanezcan 100% inmunes.

### 4. `examples/{edo,edp}/templates/*.json` y 8 Suites Exclusivas
- Actualizar las plantillas JSON de ejemplo en `examples/edo/templates/` y `examples/edp/templates/` para que cumplan `strict=True` (`>= 10` claves únicas, `error_rationale` dinámico con `@var@`, `cross_check_py` no trivial, `hints >= 25` chars, `0` `\text{...} > 45` chars).
- Actualizar y ampliar las 8 suites exclusivas cubriendo `[TPL-STATIC-OPT]` (con `vars` mudas Y con `vars == {}`), `[TPL-DYNAMIC-RATIONALE]`, `[KATEX-PROSE-OVERFLOW]`, desenvoltura `\text{...}` en `[R-18]` e interpolación `@n@`/`@k@` con inmunidad `${k}^*$`.

## Verificación
Ejecuta:
```powershell
& ".venv\Scripts\python.exe" -m pytest tests/test_engine_invariants_adversarial.py tests/test_assemble_katex_and_rationale.py tests/test_assemble_sanitize_katex_r23.py tests/test_katex_prairielearn_tokens.py tests/test_c2c_error_aggregation.py tests/test_sandbox_adversarial.py tests/test_sandbox_gil_and_circuit_breaker.py tests/test_template_variability.py -q
```
Escribe `BRIEFING.md` antes de editar, `handoff.md` al terminar y notifica a `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589` con `DONE:: Stream 1D Impl completado (<N> passed)`.
