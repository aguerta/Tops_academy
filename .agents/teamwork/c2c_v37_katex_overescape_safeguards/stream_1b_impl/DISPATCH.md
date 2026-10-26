# DISPATCH — Stream 1B (Fase 1: Implementador)

- **Parent Conversation ID:** `da4d9acf-34da-4bc8-930b-6fb3d28b5744`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1b_impl`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\engine\assemble.py`
2. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_assemble_sanitize_katex_r23.py` `[NEW]`
3. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1b_impl\BRIEFING.md` `[NEW]`
4. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1b_impl\handoff.md` `[NEW]`

PROHIBIDO tocar cualquier otro archivo.

## Especificación Técnica

### 1. `.agents/skills/content-to-course/engine/assemble.py`
En `sanitize_katex_syntax(text: str) -> str` (línea ~224):
Añade una fase determinista de saneamiento anti-sobreescape y compatibilidad KaTeX web al inicio de `sanitize_katex_syntax` (justo después de `if not isinstance(text, str): return text`):

1. **Colapso determinista de comandos LaTeX sobreescapados (`R-23`):**
   - `text = re.sub(r"\\\\([a-zA-Z]+)", r"\\\1", text)` (aplicado iterativamente o hasta punto fijo para que incluso `\\\\\\frac` o `\\\\frac` colapsen limpiamente a `\frac`, `\text`, `\to`, `\mathbb`, `\right`, `\alpha`, `\beta`, `\theta`, `\rho`, `\varepsilon`, `\times`, `\Rightarrow`, `\bar`, `\tilde`, `\tau`, `\nabla`, `\boldsymbol`, `\neq`, `\forall`, `\begin`, `\end`).
   - Verifica que los saltos de fila legítimos de matrices y sistemas (`\\ ` seguidos de espacio, dígito, signo `-`/`+`, `[` como `\\[4pt]` o salto de línea) **se preserven intactos** al 100%.
2. **Mapeo determinista de macros externas no soportadas en KaTeX web (`\centernot`):**
   - Después de colapsar barras sobreescapadas, reemplaza:
     - `r"\\centernot\s*\\(?:Rightarrow|implies)\b"` -> `r"\\nRightarrow"`
     - `r"\\centernot\s*\\(?:Leftarrow|impliedby)\b"` -> `r"\\nLeftarrow"`
     - `r"\\centernot\s*\\(?:Leftrightarrow|iff)\b"` -> `r"\\nLeftrightarrow"`
     - `r"\\centernot\s*\\(?:rightarrow|to)\b"` -> `r"\\nrightarrow"`
     - `r"\\centernot\s*\\(?:leftarrow|gets)\b"` -> `r"\\nleftarrow"`
     - `r"\\centernot\s*\\leftrightarrow\b"` -> `r"\\nleftrightarrow"`
     - `r"\\centernot\b"` -> `r"\\not"`
3. **Reparación determinista de contaminación `\text{..._...}`:**
   - Repara el patrón de contaminación forense `\text{textVar[barx_n] = O(n)}` y variantes análogas `\text{textVar[bar<var>_<sub>] = <rhs>}`:
     `text = re.sub(r"\\text\s*\{\s*text(Var|Cov|Corr|E)\s*\[\s*bar([a-zA-Z0-9]+)_([a-zA-Z0-9]+)\s*\]\s*=\s*([^{}]+?)\s*\}", r"\\text{\1}[\\bar{\2}_{\3}] = \4", text)`
   - Además, para cualquier `\text{...}` plano residual sin `$` ni macros internos que contenga `_` sin escapar (`r"\\text\s*\{([^{}$\\]*_[^{}$\\]*)\}"`), escapa los guiones bajos internos (`_` -> `\_`) para evitar el `ParseError: Expected 'EOF', got '_'` en KaTeX.

### 2. `tests/test_assemble_sanitize_katex_r23.py`
Crea una suite de pruebas exhaustiva verificando:
- Colapso de todos los comandos sobreescapados registrados en la evidencia forense de `saul_control_optimo`, `gavilano_pre_parcial` y `asyntotic_estatistics_v7` (`\\frac`, `\\text`, `\\Rightarrow`, `\\right`, `\\alpha`, `\\mathbb`, `\\to`, `\\beta`, `\\neq`, `\\times`, `\\forall`, `\\begin`, `\\rho`, `\\varepsilon`, `\\theta`, `\\bar`).
- Preservación exacta de saltos de fila `\\ ` en matrices `\begin{bmatrix}`, `\begin{pmatrix}` y `\begin{cases}`.
- Conversión de `\centernot\Rightarrow` (y `\\centernot\\Rightarrow`) a `\nRightarrow`.
- Reparación de `\text{textVar[barx_n] = O(n)}` a `\text{Var}[\bar{x}_n] = O(n)` y escape de `\text{foo_bar}` a `\text{foo\_bar}`.
- Integración de extremo a extremo con `assemble_question` para reactivos `multiple_choice_7_options`, `fill_in_the_blank` y `multiple_select`.

## Verificación
Ejecuta:
```powershell
pytest tests/test_assemble_sanitize_katex_r23.py tests/test_latex_engine.py -q
```
Escribe `BRIEFING.md` antes de editar, `handoff.md` al terminar y responde con `DONE:: Stream 1B Impl completado`.
