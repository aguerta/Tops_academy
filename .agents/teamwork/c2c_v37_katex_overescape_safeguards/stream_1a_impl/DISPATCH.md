# DISPATCH — Stream 1A (Fase 1: Implementador)

- **Parent Conversation ID:** `da4d9acf-34da-4bc8-930b-6fb3d28b5744`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1a_impl`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\src\validator\lexical_scanner.py`
2. `d:\Augusto\personal_portfolio\Tops_academy\src\validator\rules.py`
3. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_katex_overescape_validator_r23.py` `[NEW]`
4. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_validator.py` (autorizado por resolución BLOCKER Tier A para corregir sobreescape en línea 686)
5. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1a_impl\BRIEFING.md` `[NEW]`
6. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1a_impl\handoff.md` `[NEW]`

PROHIBIDO tocar cualquier otro archivo.

## Especificación Técnica

### 1. `src/validator/lexical_scanner.py`
En `scan_lexical(raw_text: str, consolidate: bool = False)`:
- En la sección donde se procesan escapes dentro de un string literal (`if ch == "\\":`), cuando `next_ch == "\\"` (línea ~236):
  - Antes de hacer `pos += 1; continue`, verifica si `raw_text[pos + 1:]` comienza con `r"^\\\\([a-zA-Z]+)"` (es decir, 4 barras invertidas seguidas inmediatamente de caracteres alfabéticos en el texto JSON crudo, como `\\\\frac`, `\\\\text`, `\\\\to`, `\\\\mathbb`, `\\\\right`, `\\\\alpha`, `\\\\beta`, `\\\\theta`, `\\\\rho`, `\\\\varepsilon`, `\\\\times`, `\\\\Rightarrow`).
  - Si coincide (`over_m = re.match(r"^\\\\([a-zA-Z]+)", raw_text[pos + 1:])`):
    - Calcula `line, col = get_line_col(raw_text, esc_pos)`.
    - Registra `ValidationError`:
      - `rule_id="R-23"`
      - `code="ERR_LATEX_OVERESCAPE"`
      - `message=f"Over-escaped LaTeX command '\\\\\\\\{cmd_word}' at line {line}, col {col} evaluates to '\\\\{cmd_word}' (linebreak + literal text in KaTeX). Must be encoded as '\\\\{cmd_word}' in JSON"`
      - `line=line, col=col`
    - Avanza `pos += 1 + over_m.end()` y haz `continue`.
  - Si NO coincide (por ejemplo, `\\\\ ` seguido de espacio, dígito, signo `-`/`+`, `[` en un salto de fila de `\begin{bmatrix}`, `\begin{pmatrix}`, `\begin{cases}`), mantén el comportamiento actual (`pos += 1; continue`).

### 2. `src/validator/rules.py`
En `check_latex_and_templates(text: str, q_id: str, field_desc: str) -> list[ValidationError]` (dentro de `check_extended_quality_rules`):
- Añade las siguientes validaciones al final de `check_latex_and_templates`:
  1. **Regla `R-23` (`ERR_LATEX_OVERESCAPE`) en memoria:**
     - Busca `re.finditer(r"\\\\([a-zA-Z]+)", text)`.
     - Por cada coincidencia `cmd_word = m.group(1)`, agrega `ValidationError(rule_id="R-23", code="ERR_LATEX_OVERESCAPE", message=f"Question '{q_id}' in {field_desc}: Over-escaped LaTeX command '\\\\{cmd_word}' detected in memory (renders as linebreak + literal '{cmd_word}' in KaTeX)", item_id=q_id)`.
  2. **Regla `R-23` (`ERR_LATEX_INLINE_NEWLINE`) — Invariante KaTeX Inline:**
     - Elimina primero escapes `\$` y bloques display `$$[\s\S]*?$$` (`no_disp = re.sub(r"\$\$[\s\S]*?\$\$", "", text.replace(r"\$", ""))`).
     - Para cada bloque inline `m_inl` en `re.finditer(r"\$([^\$]+)\$", no_disp)`:
       - Enmascara/elimina del interior `inner = m_inl.group(1)` cualquier entorno multilineal válido:
         `inner_no_env = re.sub(r"\\begin\s*\{+\s*(?:[a-zA-Z]*matrix|cases|aligned|array|split|gathered)\*?\}*[\s\S]*?\\end\s*\{+\s*(?:[a-zA-Z]*matrix|cases|aligned|array|split|gathered)\*?\}*", "", inner)`
       - También elimina comandos de sobrecarga ya reportados `r"\\\\[a-zA-Z]+"` para no duplicar si ya se reportó como `ERR_LATEX_OVERESCAPE`, o verifica si queda algún `r"\\\\"` (salto de línea `\\` en modo inline fuera de matriz/cases).
       - Si `re.search(r"\\\\(?![a-zA-Z])", inner_no_env)`:
         - Agrega `ValidationError(rule_id="R-23", code="ERR_LATEX_INLINE_NEWLINE", message=f"Question '{q_id}' in {field_desc}: Forbidden linebreak '\\\\' inside inline math '$...$' outside matrix/cases environment", item_id=q_id)`.
  3. **Detección de macro no soportada `\centernot` y `_` sin escapar en `\text{...}` (`R-20` / `R-23`):**
     - Si `re.search(r"\\centernot\b", text)`:
       - Agrega `ValidationError(rule_id="R-23", code="ERR_LATEX_UNSUPPORTED_MACRO", message=f"Question '{q_id}' in {field_desc}: Unsupported LaTeX package macro '\\centernot' detected in KaTeX web bundle (use '\\nRightarrow', '\\nrightarrow', or '\\not')", item_id=q_id)`.
     - Para cada `m_txt` en `re.finditer(r"\\text\s*\{([^{}$]*)\}", text)`:
       - Si `re.search(r"(?<!\\)_", m_txt.group(1))`:
         - Agrega `ValidationError(rule_id="R-20", code="ERR_LATEX_SYNTAX", message=f"Question '{q_id}' in {field_desc}: Unescaped underscore '_' inside '\\text{{{m_txt.group(1)}}}' causes KaTeX ParseError", item_id=q_id)`.

### 3. `tests/test_katex_overescape_validator_r23.py`
Crea una suite de tests completa que verifique:
- `scan_lexical` detecta `R-23` (`ERR_LATEX_OVERESCAPE`) en `\\\\frac`, `\\\\text`, `\\\\to`, `\\\\mathbb`, `\\\\right`, `\\\\alpha`, `\\\\beta`, `\\\\theta`, `\\\\rho`, `\\\\varepsilon`, `\\\\times`, `\\\\Rightarrow` (incluyendo consolidación con `consolidate=True`).
- `scan_lexical` y `check_extended_quality_rules` permiten con 0 errores saltos de fila legítimos `\\\\ ` en `\begin{bmatrix}`, `\begin{pmatrix}`, `\begin{matrix}`, `\begin{cases}`.
- `check_extended_quality_rules` detecta `R-23` en memoria (`\\frac`), `ERR_LATEX_INLINE_NEWLINE` en `$a \\ b$` fuera de matriz, `ERR_LATEX_UNSUPPORTED_MACRO` en `\centernot\Rightarrow` y `ERR_LATEX_SYNTAX` en `\text{textVar[barx_n] = O(n)}`.
- **Test de Regresión Multi-Curso Real:** Carga los 4 cursos publicados en `courses/*.json` (`saul_control_optimo.json`, `gavilano_pre_parcial.json`, `asyntotic_estatistics_v7.json`, `solow_growth_model.json`) y verifica que `scan_lexical` y `validate_course_content(..., strict=True)` reportan **0 errores R-23**.

## Verificación
Ejecuta:
```powershell
pytest tests/test_katex_overescape_validator_r23.py tests/test_validator.py -q
```
Escribe `BRIEFING.md` antes de editar, `handoff.md` al terminar y responde con `DONE:: Stream 1A Impl completado`.
