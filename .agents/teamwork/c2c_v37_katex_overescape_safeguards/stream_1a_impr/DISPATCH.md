# DISPATCH — Stream 1A (Fase 2: Mejorador)

- **Parent Conversation ID:** `da4d9acf-34da-4bc8-930b-6fb3d28b5744`
- **Impl Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1a_impl\handoff.md`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1a_impr`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\src\validator\lexical_scanner.py`
2. `d:\Augusto\personal_portfolio\Tops_academy\src\validator\rules.py`
3. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_katex_overescape_validator_r23.py`
4. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_validator.py`
5. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1a_impr\handoff.md` `[NEW]`

PROHIBIDO tocar cualquier otro archivo.

## Instrucciones de Endurecimiento
1. Lee el `handoff.md` del Implementador 1A, `src/validator/lexical_scanner.py`, `src/validator/rules.py` y `tests/test_katex_overescape_validator_r23.py`.
2. Revisa y endurece casos borde:
   - En `src/validator/lexical_scanner.py` y `src/validator/rules.py`:
     - Verifica qué pasa cuando un salto de fila de matriz va pegado sin espacio a un comando en la celda siguiente (`\\\frac` en memoria $\equiv$ `\\\\\\frac` con 6 barras en JSON crudo: 4 barras del salto de fila `\\` + 2 barras de `\frac`, frente a `\\\\frac` con 4 barras en JSON crudo que es `\frac` sobreescapado `\\frac`). Asegúrate de discriminar la paridad de barras para que un salto de fila compacto `\\\\\\frac` (6 barras en JSON crudo / 3 barras `\\\frac` en memoria dentro de matriz) NO sea un falso positivo, mientras que 4 barras en JSON crudo (`\\\\frac`, o 8 barras `\\\\\\\\frac`) y 2/4 barras en memoria (`(?<!\\)(?:\\\\)+([a-zA-Z]+)`) SÍ sean detectadas como `R-23` (`ERR_LATEX_OVERESCAPE`).
     - En la invariante inline de `\\` (`ERR_LATEX_INLINE_NEWLINE` en `rules.py`), verifica que limpie iterativamente entornos anidados (`pmatrix` dentro de `matrix` o `cases`) y múltiples matrices en el mismo bloque `$ ... $`, y que trate adecuadamente `\$` vs `\\$` al final de bloque (`re.sub(r"(?<!\\)(?:\\\\)*\\\$", "", text)`).
     - En `check_extended_quality_rules` (`rules.py`), verifica que `check_latex_and_templates` también se ejecute sobre `correct_answer` de preguntas `fill_in_the_blank` (tanto si `correct_answer` es `str` como si es `dict` con `value`, `expression`, `canonical_algebraic`, `accepted_equivalents`).
3. Amplía `tests/test_katex_overescape_validator_r23.py` con casos adversarios para:
   - Saltos de fila compactos `\\\frac` (3 barras en memoria / 6 barras en JSON) dentro de `\begin{bmatrix}` vs sobreescape `\\frac` (2 barras en memoria / 4 barras en JSON).
   - Matrices múltiples y anidadas dentro de un mismo bloque `$ ... $`.
   - `fill_in_the_blank` con `correct_answer` sobreescapado.
4. Ejecuta:
   ```powershell
   pytest tests/test_katex_overescape_validator_r23.py tests/test_validator.py -k "not Challenger and not Packaging" -q
   ```
5. Escribe `handoff.md` en tu carpeta `stream_1a_impr/` y finaliza con `DONE:: Stream 1A Impr completado`.
