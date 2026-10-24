# BRIEFING — Stream 1A (Fase 2: Mejorador `impr_1a`)

## 1. Identificación y Frontera Exclusiva
- **Rol:** Mejorador (Improver) de la Tríada Flash Stream 1A (`impr_1a`).
- **Frontera Exclusiva de Escritura:**
  - `.agents/skills/content-to-course/engine/assemble.py`
  - `tests/test_assemble_katex_and_rationale.py`
  - `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1a_impr/` (Gobernanza)

## 2. Inspección Pre-Flight de Cambios del Implementador
- **Implementador:** `impl_1a` entregó modificaciones en `engine/assemble.py` y creó `tests/test_assemble_katex_and_rationale.py`.
- **Hallazgos Clave:**
  1. `sanitize_katex_syntax`: Restringió `frac_inner_fix` y `frac_simple_fix` a `text.count("{") > text.count("}")`, impidiendo que `_` o `^` antecedan inmediatamente a `{`, e incorporó guardas contra `_}{` y `^}{`.
  2. `_resolve_distractor_rationale`: Añadió lógica prioritaria para autor no genérico y herencia segura desde CTA.
  3. Los 84 tests en las suites combinadas (`test_assemble_katex_and_rationale.py`, `test_katex_prairielearn_tokens.py`, `test_latex_engine.py`, `test_engine_invariants_adversarial.py`) pasan al 100%.

## 3. Plan de Endurecimiento (Auditoría de Casos Borde)
1. **Endurecimiento KaTeX de Fracciones Anidadas Complejas:**
   - Auditar expresiones con matrices, operadores, y subíndices/superíndices anidados como `(X'_{i}X_{i})^{-1}`, `\hat{\beta}_{2SLS}`, `\text{Var}[b_{IV}]`, `\begin{pmatrix}...`, tanto cuando la expresión está balanceada como cuando hay llaves desbalanceadas fuera de la fracción en cualquier parte del texto.
   - Asegurar que la sanitización nunca corrompa ninguna fracción válida ni genere artefactos KaTeX.
2. **Validación KaTeX Estricta de la Cadena Final de `error_rationale`:**
   - Unificar `_resolve_distractor_rationale` para que opere de forma 100% idéntica y simétrica en `multiple_choice_7_options` y `multiple_select`.
   - Garantizar que `validate_katex_syntax` sea evaluado sobre la cadena final tras la interpolación de variables del sandbox y tras la sanitización con `sanitize_katex_syntax`.
   - Si la cadena resultante de un rationale de autor o de CTA contiene KaTeX inválido que no pueda ser reparado, realizar fallback seguro a una formulación válida antes de inyectarlo en el objeto pregunta, previniendo cualquier fallo en los invariantes de plataforma.
3. **Agnosticismo al Dominio:**
   - Confirmar la ausencia total de nombres o identificadores de cursos específicos en `assemble.py`.
4. **Ampliación de Casos Adversarios en Tests:**
   - Añadir tests unitarios adversarios cubriendo:
     - Fracciones complejas con matrices y operadores anidados.
     - Llaves desbalanceadas concurrentes en prefijos y sufijos externos a la fracción.
     - Fallback seguro ante interpolaciones de variables con sintaxis rota en rationale.
     - Equivalencia estricta de comportamiento entre MC7 y MS para preservación/herencia de rationales.
