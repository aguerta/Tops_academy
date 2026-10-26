# DISPATCH — Stream 1C (Fase 2: Mejorador)

- **Parent Conversation ID:** `da4d9acf-34da-4bc8-930b-6fb3d28b5744`
- **Impl Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1c_impl\handoff.md`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1c_impr`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\engine\invariants.py`
2. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\compile_shard.py`
3. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_invariants_and_shard_overescape_r23.py`
4. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1c_impr\handoff.md` `[NEW]`

PROHIBIDO tocar cualquier otro archivo.

## Instrucciones de Endurecimiento
1. Lee el `handoff.md` del Implementador 1C, `engine/invariants.py`, `compile_shard.py` y `tests/test_invariants_and_shard_overescape_r23.py`.
2. Revisa y endurece:
   - En `engine/invariants.py`:
     - Verifica que la Regla 2 (`Residual double curly braces`) siga detectando `{{var}}` y `{{` cuando `allow_template_vars=False` (comportamiento original intacto), y que cuando `allow_template_vars=True` permita `\begin{{bmatrix}}` o `{{var}}` de plantilla según corresponda sin romper ningún test existente.
     - En la Regla 11 (`R-23`), ¿qué ocurre si en una matriz alguien escribió `\\\frac{1}{2}` (3 barras: `\\` salto de fila de matriz + `\frac` sin espacio intermedio) dentro de `\begin{bmatrix} 1 & 2 \\\frac{3}{4} & 5 \end{bmatrix}`? Asegúrate de discriminar `(?<!\\)\\\\([a-zA-Z]+)` o entornos matriciales si hay 3 barras vs 2 barras (`\\frac`), de modo que `\\frac` (2 barras) siempre sea rechazado como R-23 pero un salto de fila legítimo `\\ \frac` sea aceptado.
     - En la Regla 12 (Invariante KaTeX Inline), verifica que soporte múltiples entornos matriciales dentro de un mismo bloque `$ ... $` (ej. `$\text{plim } A = \begin{pmatrix} 6 & 0 \\ 0 & 9 \end{pmatrix}, \text{plim } b = \begin{pmatrix} 47 \\ 49 \end{pmatrix}$` como ocurre en `asyntotic_estatistics_v7.json` pregunta 530).
     - Añade un test en `tests/test_invariants_and_shard_overescape_r23.py` que valide con `validate_katex_syntax` las preguntas con matrices de los 4 cursos reales en `courses/*.json` verificando **0 falsos positivos**.
   - En `compile_shard.py`:
     - Verifica que `heal_shard_source_text` preserve intactos los saltos de fila `\\ ` dentro de `\begin{bmatrix} ... \end{bmatrix}` tanto en raw strings `r"..."` como en strings estándar `"..."`.
3. Ejecuta:
   ```powershell
   pytest tests/test_invariants_and_shard_overescape_r23.py tests/test_engine_invariants_adversarial.py tests/test_katex_prairielearn_tokens.py -q
   ```
4. Escribe `handoff.md` en tu carpeta `stream_1c_impr/` y finaliza con `DONE:: Stream 1C Impr completado`.
