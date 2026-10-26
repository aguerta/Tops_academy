# HANDOFF — Stream 1C (Fase 1: Implementador)

- **Parent Conversation ID:** `da4d9acf-34da-4bc8-930b-6fb3d28b5744`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1c_impl`
- **Timestamp:** 2026-10-25T18:45:30-05:00

## 1. Resumen de Implementación

Se completaron todas las directivas de `DISPATCH.md` con precisión quirúrgica:

### 1.1 `.agents/skills/content-to-course/engine/invariants.py`
1. **Regla 2 (Double Curly Braces en Plantillas):**
   - Se condicionó la validación de llaves dobles residuales a `if not allow_template_vars:` para permitir legítimamente `\begin{{bmatrix}}` en plantillas antes de su renderizado.
2. **Regla 11 (R-23 — Prohibición de `\\([a-zA-Z]+)` en memoria):**
   - Agregada en `validate_katex_syntax`: detecta comandos LaTeX sobre-escapados (`\\frac`, `\\text`, `\\to`, `\\alpha`, etc.) emitiendo:
     `Over-escaped LaTeX command '\\{cmd_name}' detected in {context} (R-23). Use single backslash '\{cmd_name}' in memory.`
3. **Regla 12 (Invariante KaTeX Inline — Prohibición de `\\` en `$ ... $` fuera de matriz/casos):**
   - Limpia display math `$$...$$` y `\$`.
   - En bloques `$ ... $`, suprime entornos multilínea permitidos (`bmatrix`, `pmatrix`, `cases`, `aligned`, `array`, `split`, `gathered`) soportando tanto `{env}` como `{{env}}`.
   - Detecta saltos de línea ilegales `\\\\(?![a-zA-Z])` fuera de dichos entornos emitiendo:
     `Forbidden linebreak '\\' inside inline math '$...$' outside matrix/cases environment in {context} (R-23).`
4. **Regla 13 (Prohibición de `\centernot` y `_` sin escapar en `\text{...}`):**
   - Detecta `\centernot` y emite diagnóstico prescriptivo sugiriendo `\nRightarrow`, `\nrightarrow` o `\not`.
   - Revisa bloques `\text{...}` para prohibir guiones bajos `_` que no estén escapados como `\_`.

### 1.2 `.agents/skills/content-to-course/compile_shard.py`
1. **Colapso de doble barra en literales raw (`is_raw`):**
   - En `heal_shard_source_text`, si el autor escribió accidentalmente `\\frac`, `\\text`, etc. dentro de `r"..."`, se colapsa a una sola barra en el literal: `new_body = re.sub(r"\\\\([a-zA-Z]+)", r"\\\1", new_body)`.
2. **Normalización y deduplicación de flechas y macros:**
   - Se definió `_bs = r"\\"` para raw strings (genera 1 barra en el literal raw) y `_bs = r"\\\\"` para non-raw (genera 2 barras en el literal normal, evaluando a 1 barra en memoria).
   - Se reemplazan `\centernot\Rightarrow` y `\centernot\implies` por `\nRightarrow` respetando `_bs`.
   - Se usa `(?<!\\)\\+implies\b` y `(?<!\\)\\+iff\b` para prevenir duplicación o triplicación de barras cuando ya venían escapadas.
3. **Fallback seguro en excepciones:**
   - En el bloque `except Exception:`, se verifica `has_raw = bool(re.search(r'\br["\']', source_text, re.IGNORECASE))`. Si el archivo contiene raw strings, NO se ejecuta la sustitución global de `COMBINED_LATEX`, previniendo sobre-escapes destructivos.

### 1.3 `tests/test_invariants_and_shard_overescape_r23.py` `[NEW]`
Se creó una suite exhaustiva con 28 casos de prueba organizados en 4 clases:
- `TestKaTeXOverescapedCommandsR23`: valida que `validate_katex_syntax` y `check_instance_invariants` rechacen `\\frac`, `\\text`, `\\to`, `\\mathbb`, `\\right`, `\\alpha`, `\\beta` con diagnóstico `R-23`.
- `TestKaTeXMatrixAndCasesAllowedR23`: valida que `\begin{bmatrix}` y `\begin{pmatrix}` estén permitidos en `$ ... $` y `$$ ... $$`, incluyendo `\begin{{bmatrix}}` con `allow_template_vars=True`, así como `cases` y `aligned`.
- `TestKaTeXForbiddenInlineLinebreakAndBadMacrosR23`: valida el rechazo de saltos `\\` en línea, macro `\centernot` y `_` sin escapar en `\text{...}`, así como la aceptación de `\_`.
- `TestCompileShardHealingR23`: valida que `heal_shard_source_text` cure raw y non-raw strings produciendo al evaluar en Python exactamente 1 barra por comando (`\frac`, `\Rightarrow`) y 0 sobre-escapes en memoria.

## 2. Resultados de Verificación (Pytest)

Ejecución focalizada:
```powershell
.venv\Scripts\pytest.exe tests/test_invariants_and_shard_overescape_r23.py tests/test_engine_invariants_adversarial.py -v
```
Resultado:
- **81 passed in 1.89s** (28 tests R-23 + 53 tests adversariales de engine/invariants).
- 0 fallos, 0 errores, 0 regresiones.

## 3. Verificación de Frontera de Escritura
Archivos modificados/creados exclusivamente dentro de la frontera:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\engine\invariants.py`
2. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\compile_shard.py`
3. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_invariants_and_shard_overescape_r23.py`
4. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1c_impl\BRIEFING.md`
5. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1c_impl\handoff.md`

Ningún archivo fuera de esta frontera fue modificado o creado por este stream.
