# Original Request (`c2c_v37_katex_overescape_safeguards`)

Implementar específicamente lo señalado en el comentario de `FUTURE_MILESTONES.md` (Milestone 4.5 — Salvaguarda Anti-Sobreescape y Validación Léxica KaTeX en JSON: Lección Aprendida Multi-Curso `saul_control_optimo`, `gavilano_pre_parcial` y `asyntotic_estatistics_v7`) aplicando `/flash-triad-orchestrator`:

1. **Regla R-23 en Linter Léxico (`src/validator/lexical_scanner.py` & `src/validator/rules.py` & `engine/invariants.py`):**
   - Prohibir estrictamente secuencias de sobreescape de comandos LaTeX (`\\\\([a-zA-Z]+)` en JSON crudo / `\\([a-zA-Z]+)` en memoria), discriminando con 0 falsos positivos los saltos de fila legítimos en matrices o sistemas (`\\ ` dentro de entornos `\begin{bmatrix|matrix|pmatrix|cases|aligned|array|split}`).
   - Detectar macros externas no soportadas en KaTeX web (`\centernot`) y guiones bajos sin escapar en modo texto (`\text{..._...}`).
2. **Paso de Normalización en `engine/assemble.py` (`sanitize_katex_syntax`) y Prevención en Origen en `compile_shard.py`:**
   - Añadir fase determinista que colapse automáticamente `re.sub(r'\\\\([a-zA-Z]+)', r'\\\1', text)` antes de la serialización del curso, mapee macros externas (`\centernot\Rightarrow` -> `\nRightarrow`, etc.) y repare contaminación `\text{..._...}`.
3. **Invariante KaTeX Inline en CI/CD:**
   - Comprobar en tiempo de compilación y validación que ningún bloque matemático delimitado por un solo `$` contenga el comando de salto de línea `\\` fuera de entornos multilineales válidos.
4. **Guardián de Admisión en Runtime (`run_platform.py` / `validate_platform_course`):**
   - Bloquear en `validate_platform_course` o auto-reparar en `scan_courses` cualquier JSON que contenga secuencias de sobreescape antes de servirlo al cliente web, y actualizar el estado en `FUTURE_MILESTONES.md`.
