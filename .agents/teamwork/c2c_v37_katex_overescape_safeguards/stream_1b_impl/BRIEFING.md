# BRIEFING — Stream 1B (Implementador)

- **Parent Conversation ID:** `da4d9acf-34da-4bc8-930b-6fb3d28b5744`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1b_impl`
- **Fecha y Hora:** 2026-10-25

---

## 1. Verificación de Exclusive Write Boundary
Solo se modificarán/crearán los 4 archivos autorizados en `DISPATCH.md`:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\engine\assemble.py` (modificación)
2. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_assemble_sanitize_katex_r23.py` (creación)
3. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1b_impl\BRIEFING.md` (creación)
4. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1b_impl\handoff.md` (creación)

Ningún archivo fuera de esta frontera será creado ni modificado.

---

## 2. Hallazgos del Pre-Flight Sanity Check

### 2.1 Estado Actual de `assemble.py`
- En `assemble.py`, la función `sanitize_katex_syntax(text: str) -> str` (línea 224) maneja:
  - Normalización de `$$$` a `$$`.
  - Normalización de dobles llaves residuales de f-strings `{{var}}` -> `{var}` preservando anidamientos legítimos.
  - Auto-cierre de macros de acentos/estilos/raíces desbalanceadas (`\hat{\boldsymbol{\beta}}`).
  - Auto-reparación de llaves faltantes en numeradores/denominadores de `\frac`.
- Actualmente, `sanitize_katex_syntax` **no** cuenta con:
  - Fase determinista anti-sobreescape para comandos como `\\frac`, `\\text`, `\\\\frac`, etc. (R-23).
  - Normalización de macros externas no soportadas por KaTeX web como `\centernot` (`\centernot\Rightarrow`, etc.).
  - Reparación de contaminación en `\text{textVar[barx_n] = O(n)}` o escape de `_` dentro de `\text{...}` plano.

---

## 3. Plan Quirúrgico de Implementación

### 3.1 Modificaciones en `assemble.py` (`sanitize_katex_syntax`)
Insertar inmediatamente después de `if not isinstance(text, str): return text`:

1. **Colapso determinista de comandos LaTeX sobreescapados (`R-23`):**
   ```python
   # 1. Deterministic collapse of overescaped LaTeX commands (R-23)
   # Collapses \\frac, \\\frac, \\\\frac -> \frac for any command name while preserving
   # legitimate matrix/system row breaks (\\ followed by space, digit, sign, newline, or '[').
   while True:
       new_text = re.sub(r"\\{2,}([a-zA-Z]+)", r"\\\1", text)
       if new_text == text:
           break
       text = new_text
   ```
   - Preserva al 100% saltos de línea de matriz/sistema: `\\ ` (espacio), `\\\n` (salto de línea), `\\1` (dígito), `\\-` (signo), `\\[4pt]` (espaciador vertical), ya que el grupo solo matchea si hay `[a-zA-Z]+` inmediatamente después de 2 o más barras.

2. **Mapeo determinista de macros externas no soportadas en KaTeX web (`\centernot`):**
   ```python
   # 2. Deterministic mapping of unsupported external KaTeX macros (\centernot)
   text = re.sub(r"\\centernot\s*\\(?:Rightarrow|implies)\b", r"\\nRightarrow", text)
   text = re.sub(r"\\centernot\s*\\(?:Leftarrow|impliedby)\b", r"\\nLeftarrow", text)
   text = re.sub(r"\\centernot\s*\\(?:Leftrightarrow|iff)\b", r"\\nLeftrightarrow", text)
   text = re.sub(r"\\centernot\s*\\(?:rightarrow|to)\b", r"\\nrightarrow", text)
   text = re.sub(r"\\centernot\s*\\(?:leftarrow|gets)\b", r"\\nleftarrow", text)
   text = re.sub(r"\\centernot\s*\\leftrightarrow\b", r"\\nleftrightarrow", text)
   text = re.sub(r"\\centernot\b", r"\\not", text)
   ```

3. **Reparación determinista de contaminación `\text{..._...}`:**
   ```python
   # 3. Deterministic repair of \text{..._...} contamination
   text = re.sub(
       r"\\text\s*\{\s*text(Var|Cov|Corr|E)\s*\[\s*bar([a-zA-Z0-9]+)_([a-zA-Z0-9]+)\s*\]\s*=\s*([^{}]+?)\s*\}",
       r"\\text{\1}[\\bar{\2}_{\3}] = \4",
       text,
   )

   def _escape_text_underscores(match: re.Match) -> str:
       inner = match.group(1)
       return f"\\text{{{inner.replace('_', r'\_')}}}"

   text = re.sub(r"\\text\s*\{([^{}$\\]*_[^{}$\\]*)\}", _escape_text_underscores, text)
   ```

### 3.2 Creación de `tests/test_assemble_sanitize_katex_r23.py`
Pruebas exhaustivas unitarias y de integración:
- Comandos sobreescapados de evidencia forense (`saul_control_optimo`, `gavilano_pre_parcial`, `asyntotic_estatistics_v7`):
  `\\frac`, `\\text`, `\\Rightarrow`, `\\right`, `\\alpha`, `\\mathbb`, `\\to`, `\\beta`, `\\neq`, `\\times`, `\\forall`, `\\begin`, `\\rho`, `\\varepsilon`, `\\theta`, `\\bar`.
- Preservación exacta de matrices y sistemas (`\begin{bmatrix}`, `\begin{pmatrix}`, `\begin{cases}`, `\\[4pt]`, `\\ \text{...}`).
- Mapeo de `\centernot` (`\centernot\Rightarrow` -> `\nRightarrow`, `\\centernot\\Rightarrow` -> `\nRightarrow`, `\centernot\to` -> `\nrightarrow`, etc.).
- Reparación de `\text{textVar[barx_n] = O(n)}` y escape de `\text{metric_foo_bar}` a `\text{metric\_foo\_bar}`.
- Pruebas E2E con `assemble_question` para `multiple_choice_7_options`, `fill_in_the_blank` y `multiple_select`.

---

## 4. Estrategia de Ejecución de Tests
Ejecución mediante `.venv\Scripts\python -m pytest tests/test_assemble_sanitize_katex_r23.py tests/test_latex_engine.py -q`.
No se detectan bloqueadores. Procediendo a Fase de Implementación.
