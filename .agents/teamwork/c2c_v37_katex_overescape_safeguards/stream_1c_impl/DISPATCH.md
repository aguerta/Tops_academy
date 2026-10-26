# DISPATCH — Stream 1C (Fase 1: Implementador)

- **Parent Conversation ID:** `da4d9acf-34da-4bc8-930b-6fb3d28b5744`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1c_impl`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\engine\invariants.py`
2. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\compile_shard.py`
3. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_invariants_and_shard_overescape_r23.py` `[NEW]`
4. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1c_impl\BRIEFING.md` `[NEW]`
5. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1c_impl\handoff.md` `[NEW]`

PROHIBIDO tocar cualquier otro archivo.

## Especificación Técnica

### 1. `.agents/skills/content-to-course/engine/invariants.py`
En `validate_katex_syntax(text: str, context: str, allow_template_vars: bool = False, variables: Optional[Dict[str, Any]] = None) -> List[str]`:
Añade las siguientes validaciones después de la regla 10 (línea ~451):
1. **Regla 11 (R-23 — Prohibición de `\\([a-zA-Z]+)` en memoria):**
   - Busca `re.finditer(r"\\\\([a-zA-Z]+)", text)`.
   - Por cada coincidencia `cmd_name = m_over.group(1)`, agrega:
     `f"Over-escaped LaTeX command '\\\\{cmd_name}' detected in {context} (R-23). Use single backslash '\\{cmd_name}' in memory."`
2. **Regla 12 (Invariante KaTeX Inline — Prohibición de `\\` en `$ ... $` fuera de entornos matriciales/casos):**
   - Elimina `\$` y bloques display `$$[\s\S]*?$$` (`no_disp = re.sub(r"\$\$[\s\S]*?\$\$", "", text.replace(r"\$", ""))`).
   - Para cada bloque inline `$ ... $` en `re.finditer(r"\$([^\$]+)\$", no_disp)`:
     - Suprime entornos multilineales válidos (soportando `{env}` y `{{env}}`):
       `inner_no_env = re.sub(r"\\begin\s*\{+\s*(?:[a-zA-Z]*matrix|cases|aligned|array|split|gathered)\*?\}*[\s\S]*?\\end\s*\{+\s*(?:[a-zA-Z]*matrix|cases|aligned|array|split|gathered)\*?\}*", "", m_inl.group(1))`
     - Si `re.search(r"\\\\(?![a-zA-Z])", inner_no_env)`:
       - Agrega `f"Forbidden linebreak '\\\\' inside inline math '$...$' outside matrix/cases environment in {context} (R-23)."`
3. **Regla 13 (Prohibición de `\centernot` y `_` sin escapar en `\text{...}`):**
   - Si `re.search(r"\\centernot\b", text)`:
     - Agrega `f"Unsupported LaTeX macro '\\centernot' detected in {context} (R-23); use '\\nRightarrow', '\\nrightarrow', or '\\not'."`
   - Para cada `m_txt` en `re.finditer(r"\\text\s*\{([^{}$]*)\}", text)`:
     - Si `re.search(r"(?<!\\)_", m_txt.group(1))`:
       - Agrega `f"Unescaped underscore '_' inside '\\text{{{m_txt.group(1)}}}' in {context} causes KaTeX ParseError."`

### 2. `.agents/skills/content-to-course/compile_shard.py`
En `heal_shard_source_text(source_text: str) -> Tuple[bool, str]` (líneas 84-132):
1. Cuando `is_raw` es `True` (raw strings `r"..."`), si el autor escribió accidentalmente comandos LaTeX con doble barra (`\\frac`, `\\text`, `\\to`, `\\mathbb`, `\\right`, `\\alpha`, `\\beta`, `\\theta`, `\\rho`, `\\varepsilon`, `\\times`, `\\Rightarrow`, etc.), colápsalos a una sola barra en el literal raw:
   `new_body = re.sub(r"\\\\([a-zA-Z]+)", r"\\\1", new_body)`
2. Cuando reemplaces `\implies`, `\iff` y `\centernot` dentro de `if "$" in new_body:`:
   - Usa lookbehind `(?<!\\)` en `re.sub(r"(?<!\\)\\implies\b", f"{_bs}Rightarrow", new_body)` y `re.sub(r"(?<!\\)\\iff\b", f"{_bs}Leftrightarrow", new_body)` para NO duplicar barras cuando en un string no-raw ya venían como `\\implies` o `\\iff`.
   - Convierte `\centernot\Rightarrow` / `\centernot\implies` en `\nRightarrow` (respetando `_bs`).
3. En el bloque `except Exception:` de fallback (líneas 124-131), NO apliques `re.sub(rf"(?<!\\)\\({COMBINED_LATEX})", r"\\\\\1", healed)` a todo `source_text` si el archivo contiene raw strings `r"..."` o `r'...'`, sino únicamente `heal_control_chars_in_str(source_text)`.

### 3. `tests/test_invariants_and_shard_overescape_r23.py`
Crea una suite de pruebas verificando:
- `validate_katex_syntax` y `check_instance_invariants` rechazan `\\frac`, `\\text`, `\\to`, `\\mathbb`, `\\right`, `\\alpha`, `\\beta` con diagnóstico `R-23`.
- `validate_katex_syntax` permite `\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}` y `\begin{pmatrix} a \\ b \end{pmatrix}` tanto en `$ ... $` como en `$$ ... $$` (incluyendo `\begin{{bmatrix}}` con `allow_template_vars=True`).
- `validate_katex_syntax` rechaza `$x = 1 \\ y = 2$` (salto `\\` en modo inline fuera de matriz/cases), `\centernot\Rightarrow` y `\text{textVar[barx_n] = O(n)}`.
- `heal_shard_source_text` en `compile_shard.py` cura raw strings `r"$\frac{1}{2} \implies x$"` y `r"$\\frac{1}{2}$"` y non-raw strings `"$\\frac{1}{2} \\implies x$"` produciendo al evaluar el string en Python exactamente 1 barra por comando (`\frac`, `\Rightarrow`) y 0 sobreescapes.

## Verificación
Ejecuta:
```powershell
pytest tests/test_invariants_and_shard_overescape_r23.py tests/test_engine_invariants_adversarial.py -q
```
Escribe `BRIEFING.md` antes de editar, `handoff.md` al terminar y responde con `DONE:: Stream 1C Impl completado`.
