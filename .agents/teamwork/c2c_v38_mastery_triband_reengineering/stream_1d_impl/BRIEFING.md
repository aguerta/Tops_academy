# BRIEFING — Pre-Flight Stream 1D (Implementador)

- **Fase:** Fase 1 (Implementador) — Stream 1D
- **Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`
- **Fecha:** 2026-10-31
- **Frontera Exclusiva de Escritura:**
  1. `.agents/skills/content-to-course/check_templates.py`
  2. `.agents/skills/content-to-course/engine/invariants.py`
  3. `.agents/skills/content-to-course/engine/assemble.py`
  4. `.agents/skills/content-to-course/examples/edo/templates/*.json`
  5. `.agents/skills/content-to-course/examples/edp/templates/*.json`
  6. `tests/test_engine_invariants_adversarial.py`
  7. `tests/test_assemble_katex_and_rationale.py`
  8. `tests/test_assemble_sanitize_katex_r23.py`
  9. `tests/test_katex_prairielearn_tokens.py`
  10. `tests/test_c2c_error_aggregation.py`
  11. `tests/test_sandbox_adversarial.py`
  12. `tests/test_sandbox_gil_and_circuit_breaker.py`
  13. `tests/test_template_variability.py`
  14. `.agents/teamwork/c2c_v38_mastery_triband_reengineering/stream_1d_impl/BRIEFING.md`
  15. `.agents/teamwork/c2c_v38_mastery_triband_reengineering/stream_1d_impl/handoff.md`

---

## 1. Inspección de Archivos de Producción y Líneas Exactas

### 1.1 `check_templates.py`
- **Líneas ~2236–2580 (`check_single_template`):**
  - Actualmente valida AST de `generate_py` y `cross_check_py`, pero permite `cross_check_py` trivial (`def verify(res): return True`).
  - No valida longitud mínima de pistas (`hints`). Se implementará exigencia de `len(hint.strip()) >= 25` bajo `strict=True`.
  - Recolecta instancias en dry-run (50 semillas por defecto) e invoca `assemble_question` y `check_instance_invariants`.
  - **Nueva compuerta `[TPL-STATIC-OPT]`:**
    - Recolectar respuestas correctas normalizadas a lo largo de `N = min(20, num_dry_run_seeds)` semillas.
    - Para `MC7` y `fill_in_the_blank`: valor normalizado de la respuesta correcta (`re.sub(r"\s+", " ", str(correct)).strip()`).
    - Para `multiple_select`: conjunto congelado (`frozenset`) de opciones correctas `(content, is_correct)`.
    - **Mono-clave incondicional:** Si `N >= 2` y `len(unique_correct) == 1`, rechazar SIEMPRE con `[TPL-STATIC-OPT]`, aun si `vars == {}` o no hay parámetros.
    - Cuando `num_dry_run_seeds >= 15`: exigir `len(unique_correct) >= min(10, max(4, N // 2))` en plantillas cuantitativas/simbólicas o de competencias `Skill`/`Hab-*`, y `>= 4` en rotación conceptual. Para `multiple_select`, exigir `len(unique_option_sets) > 1`.
  - **Nueva compuerta `[TPL-DYNAMIC-RATIONALE]`:**
    - Cuando `strict=True` y `num_dry_run_seeds >= 15`: para cada slot de distractor (`MC7` o falsa en `MS`) cuyo `content` renderizado varíe entre semillas (`len(unique_contents) > 1`), exigir que su `error_rationale` renderizado también varíe (`len(unique_rationales) > 1`). Si permanece constante (`len == 1`), rechazar con `[TPL-DYNAMIC-RATIONALE]`.
- **Líneas ~2582–2739 (`check_competency_diversity`):**
  - Bajo `strict=True`: si el pool de reactivos es `>= 20`, verificar que ninguna clave correcta concentre `> 20%` (`0.20`) de las instancias (`[TPL-STATIC-OPT]`).
  - Bajo `strict=True`: si el banco tiene `>= 30` distractores totales, exigir `rationale_uniqueness_pct >= 35.0%` (`[TPL-DYNAMIC-RATIONALE]`).
  - Calibración de diversidad de stems: si `div_ratio < 0.5`, calcular `unmasked_ratio = len(set(stems)) / len(stems)`. Si `div_ratio >= 0.25` y `unmasked_ratio >= 0.85`, pasar la compuerta para permitir plantillas con `>= 3` stems genuinos parametrizados.
- **Líneas ~2983–3006 (`TPL-D3` en `check_templates_file_or_dir`):**
  - Cobertura multimodal de distractores:
    - Si la competencia tiene `>= 1` plantilla `MC7`: exigir `6/6` distractores declarados en `cta.json`.
    - Si la competencia tiene `0` plantillas `MC7`: si tiene `multiple_select`, exigir `>= 2` distractores válidos de `cta.json`; si es `100% FIB`, exigir `0`.

### 1.2 `engine/invariants.py`
- **Líneas ~67–105 (`check_synthetic_boilerplate_distractors` / `[R-18]`):**
  - Actualmente ignora opciones con `< 10` caracteres de prosa fuera de `$...$`. Opciones redactadas enteramente dentro de `$\text{...}$` evaden la detección de esqueletos sintéticos.
  - Se añadirá desenvolvimiento de `\text{...}` y `\textrm{...}` de adentro de `$...$` antes de extraer `_skeleton` y evaluar longitud de prosa.
- **Líneas ~270–500 (`validate_katex_syntax`):**
  - Se añadirá la regla `[KATEX-PROSE-OVERFLOW]`: inspección con conteo balanceado de llaves en macros `\text{...}`, `\textrm{...}`, `\mathrm{...}`.
  - Si el contenido interno supera 45 caracteres (`len(inner) > 45`), emitir error con código explícito `[KATEX-PROSE-OVERFLOW]` (prohibido usar `"R-23"`).

### 1.3 `engine/assemble.py`
- **Líneas ~130–216 (`format_template_string`), ~437–444 (`_format_and_sanitize_candidate`), ~683–691 (`common_misconception_warning`):**
  - Se actualizará `format_template_string` para aceptar `is_cta: bool = False`.
  - En la fase de reemplazo PrairieLearn (`@var@` y `@var:fmt@`), se interpolarán TODOS los identificadores sin restricción de longitud (`len(k) >= 1`), cubriendo `@n@`, `@k@`, `@c@`, `@a@`.
  - El filtro `len(k) > 2` se aplicará exclusivamente a llaves legacy `{var}` cuando `is_cta=True`, preservando total inmunidad para expresiones LaTeX como `${k}^*$`.

### 1.4 `examples/{edo,edp}/templates/*.json`
- `examples/edo/templates/C-02.json`:
  - `T-C02-01`: Expandir rango de parámetros aleatorios para generar `>= 10` claves únicas, incorporar variables en `error_rationale` de distractores con `@var@`.
  - `T-C02-02`: Actualizar hints para que superen `>= 25` caracteres.
  - `T-C02-03`: Convertir `cross_check_py` trivial (`return True`) en verificación real con operadores sobre `options` y variables.
- `examples/edo/templates/Hab-02.json`:
  - `T-Hab02-01`: Parametrizar rationales dinámicos con `@a@` y `@b@`, ampliar semillas únicas.
  - `T-Hab02-03`: Sustituir `cross_check_py` trivial por validación lógica de autovalores o traza/determinante.
- `examples/edp/templates/C-01.json`:
  - `T-C01-01`: Incorporar rationales dinámicos con parámetros `@delta@` y `@B@`, ampliar combinaciones numéricas a `>= 10`.
  - `T-C01-03`: `cross_check_py` no trivial y rationales dinámicos.
- `examples/edp/templates/Hab-01.json`:
  - `T-Hab01-01`: Dynamic rationales en distractores con variables.
  - `T-Hab01-03`: `cross_check_py` no trivial evaluando las opciones generadas.

---

## 2. Línea Base de Pruebas
- Ejecución previa de las 8 suites asignadas:
  `pytest tests/test_engine_invariants_adversarial.py tests/test_assemble_katex_and_rationale.py tests/test_assemble_sanitize_katex_r23.py tests/test_katex_prairielearn_tokens.py tests/test_c2c_error_aggregation.py tests/test_sandbox_adversarial.py tests/test_sandbox_gil_and_circuit_breaker.py tests/test_template_variability.py -q`
  **Resultado actual:** `186 passed in 30.19s`.

---

## 3. Matriz de Riesgos y Contratos Inviolables

1. **Regla Zero-Domain:**
   - Prohibido incluir las subcadenas `edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi` en cualquier archivo `.py` bajo `.agents/skills/content-to-course/`.
   - Cuidado especial con palabras en español como `metodo` (contiene `edo`), `puedo`, `quedo`.
   - Todos los comentarios en los archivos de producción modificados se redactarán en inglés limpio.
2. **Compatibilidad `strict=False`:**
   - Todas las nuevas compuertas (`[TPL-STATIC-OPT]`, `[TPL-DYNAMIC-RATIONALE]`, AST `cross_check_py`, `hints >= 25`) se condicionarán estrictamente a `strict=True` para preservar compatibilidad con fixtures legacy.
3. **Tag KaTeX:**
   - La nueva regla de overflow de prosa debe emitir explícitamente `[KATEX-PROSE-OVERFLOW]`, nunca `"R-23"`.
4. **Frontera de Escritura:**
   - No se modificará ningún archivo fuera de la lista declarada en `Exclusive Write Boundary`.
