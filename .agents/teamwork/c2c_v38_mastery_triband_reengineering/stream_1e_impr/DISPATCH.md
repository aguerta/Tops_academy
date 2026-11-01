# DISPATCH — Stream 1E (Fase 2: Mejorador)

- **Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1e_impr`
- **Impl Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1e_impl\handoff.md`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\repair_loop.py`
2. `d:\Augusto\personal_portfolio\Tops_academy\src\validator\psychometric_checker.py`
3. `d:\Augusto\personal_portfolio\Tops_academy\src\validator\rules.py`
4. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_validator.py`
5. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_katex_overescape_validator_r23.py`
6. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1e_impr\handoff.md` `[NEW]`

PROHIBIDO tocar cualquier otro archivo.

## Objetivos de Endurecimiento (Fase 2 — Mejorador)
1. Lee `stream_1e_impl/handoff.md` y revisa con `read_file` los cambios en `repair_loop.py`, `psychometric_checker.py`, `rules.py` y las 2 suites de tests.
2. **Casos borde en `[KATEX-PROSE-OVERFLOW]` (`src/validator/rules.py`):**
   - Verifica el conteo balanceado de llaves anidadas (ej. `\text{valor de $x_{i}$ en el límite asintótico cuando la muestra diverge}` con llaves `{i}` internas) para que no trunque prematuramente en la primera `}` interna.
   - Verifica las 3 variantes `\text{...}`, `\textrm{...}` y `\mathrm{...}`, que `len == 45` pase limpio y `len == 46` falle con `rule_id="R-20"`, `code="ERR_KATEX_PROSE_OVERFLOW"` y tag `[KATEX-PROSE-OVERFLOW]` (jamás `R-23`), sin romper los checks sobre cursos publicados en `courses/*.json`.
3. **Casos borde en `repair_loop.py` y `[R-16]` / `[R-18]`:**
   - Confirma que `RepairLoop` preserva intactos todos los atributos/firmas esperados por `run.py` y suites de integración (`run()`, `sanitize_latex_escapes`, contadores/reportes de retorno), sin mutar jamás textos ni valores de opciones, y con **0 subcadenas Zero-Domain prohibidas** (`edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`).
   - En `[R-18]`, confirma que tanto prosa repetitiva camuflada en `$\text{...}$` como muletillas de padding (`"bajo las premisas y condiciones del modelo"`, `"Opción alterna "`, `"Distractor homogéneo "`) son rechazadas determinísticamente.
   - En `[R-16]`, confirma que empates simbólicos cortos (`len_c == max_d == min_d`) pasan limpios mientras outliers genuinos largos/cortos siguen detectándose.
4. Amplía tests adversarios reales (llaves anidadas en `\text{...}`, límite exacto 45 vs 46, invariancia de opciones bajo `RepairLoop.run()`).

## Verificación
Ejecuta (sin usar `--help` sobre scripts de `content-to-course/` ni `python -c` leyendo `"content-to-course/"`):
```powershell
& ".venv\Scripts\python.exe" -m pytest tests/test_validator.py tests/test_katex_overescape_validator_r23.py -q
```
Escribe `handoff.md` en `stream_1e_impr/` y envía `DONE:: Stream 1E Impr completado (<N> passed)` a `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`.
