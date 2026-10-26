# DISPATCH — Stream 1B (Fase 2: Mejorador)

- **Parent Conversation ID:** `da4d9acf-34da-4bc8-930b-6fb3d28b5744`
- **Impl Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1b_impl\handoff.md`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1b_impr`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\engine\assemble.py`
2. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_assemble_sanitize_katex_r23.py`
3. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1b_impr\handoff.md` `[NEW]`

PROHIBIDO tocar cualquier otro archivo.

## Instrucciones de Endurecimiento
1. Lee el `handoff.md` del Implementador 1B, `engine/assemble.py` y `tests/test_assemble_sanitize_katex_r23.py`.
2. Revisa y endurece casos borde en `sanitize_katex_syntax`:
   - ¿Qué ocurre si un salto de fila de matriz `\\` va seguido de un comando en la siguiente celda sin espacio o con espacio, por ejemplo `\begin{bmatrix} 1 & 2 \\ \frac{3}{4} & 5 \end{bmatrix}` (es decir, `\\ \frac` con espacio vs `\\\frac` con 3 barras invertidas donde 2 barras son salto de fila y la 3ª barra es `\frac`)?
   - ¡CUIDADO CRÍTICO!: Si alguien escribe `\begin{bmatrix} 1 & 2 \\\frac{3}{4} & 5 \end{bmatrix}` (3 barras: `\\` salto de línea + `\frac`), `re.sub(r"\\\\([a-zA-Z]+)", r"\\\1", text)` en una sola pasada convertiría `\\\frac` (3 barras) en `\\frac` (2 barras), y en una segunda pasada convertiría `\\frac` en `\frac` (1 barra), ¡destruyendo el salto de fila si tenía 3 barras! En cambio, si solo se colapsan secuencias de número PAR de barras o exactamente `(?<!\\)\\\\([a-zA-Z]+)` (2 barras no precedidas por otra barra), o `\\\\([a-zA-Z]+)` cuando son 2 o 4 barras: verifica y blinda este caso borde en `sanitize_katex_syntax` y en los tests.
   - ¿Qué ocurre si `\text{...}` tiene un guión bajo YA escapado `\_` como `\text{foo\_bar}` o múltiples guiones bajos `\text{a_b_c}`? Asegúrate de que `\text{foo\_bar}` NO se convierta en `\text{foo\\_bar}` y que `\text{a_b_c}` se convierta limpiamente en `\text{a\_b\_c}`.
   - Verifica que los 224 campos con matrices reales de los 4 cursos publicados en `courses/*.json` pasen por `sanitize_katex_syntax` siendo **100% idempotentes** (`sanitize_katex_syntax(val) == val`). Añade un test en `tests/test_assemble_sanitize_katex_r23.py` que verifique idempotencia sobre los 4 cursos reales de `courses/*.json`.
3. Ejecuta:
   ```powershell
   pytest tests/test_assemble_sanitize_katex_r23.py tests/test_latex_engine.py -q
   ```
4. Escribe `handoff.md` en tu carpeta `stream_1b_impr/` y finaliza con `DONE:: Stream 1B Impr completado`.
