# Pre-Flight Sanity Check — Stream 1A (Implementer)

## 1. Confirmación de Entorno y Fronteras
- **Componente:** Stream 1A (`impl_1a`)
- **Frontera exclusiva de producción:**
  - `.agents/skills/content-to-course/engine/assemble.py`
  - `tests/test_assemble_katex_and_rationale.py` (nuevo)
- **Frontera exclusiva de gobernanza:**
  - `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1a_impl/BRIEFING.md`
  - `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1a_impl/handoff.md`
- **Archivos fuera de frontera:** Todos intactos, lectura exclusiva de `.agents/skills/content-to-course/engine/invariants.py`.

## 2. Inspección de Código Real

### A. KaTeX Sanitization (`assemble.py` líneas 280-322)
- Función: `sanitize_katex_syntax(text: str) -> str`
- Hallazgo del bug:
  - Línea 289-293: `frac_inner_fix` y líneas 295-298: `frac_simple_fix` se ejecutan incondicionalmente sin verificar si las llaves ya están balanceadas (`text.count("{") > text.count("}")`).
  - El regex `frac_inner_fix` (`r"(\\(?:frac|dfrac|tfrac|cfrac)\s*\{[^{}]*(?:\\[a-zA-Z]+|[_^])\s*\{[^{}]*\}[^{}\\]*)\{"`) no restringe `_` o `^` en su segmento final `[^{}\\]*`. En expresiones como `$H = \frac{(b_{IV} - b_{LS})^2}{\text{Var}[b_{IV}] + \text{Var}[b_{LS}]}$`, captura hasta `b_` y toma la `{` de `{LS}` reemplazándola por `}{`, produciendo `b_}{LS}`.
  - Plan de corrección:
    1. Condicionar `frac_inner_fix` y `frac_simple_fix` a `text.count("{") > text.count("}")`.
    2. En `frac_inner_fix`, prohibir que el carácter previo a `\{` sea `_` o `^` (`[^{}\\_^]*\{`), asegurando que no confunda subíndices/superíndices con numeradores incompletos.
    3. Revertir cambios de estos regex si introducen `_}{` o `^}{` o si empeoran el balanceo de llaves.

### B. Respeto al `error_rationale` del Autor y Fallback Seguro (`assemble.py` líneas 520-535 y 630-655)
- Función: `assemble_question(...)`
- Hallazgo del bug:
  - En `multiple_choice_7_options` (L521-529) y `multiple_select` (L639-643), si `d_id in cta_distractors_map`, se sobreescribe incondicionalmente el `error_rationale` provisto por el autor con `d_entry.get("manifestation")`.
  - Además, `manifestation` puede contener LaTeX con llaves desbalanceadas que no era validado con `validate_katex_syntax`.
  - Plan de corrección:
    1. Importar `validate_katex_syntax` desde `engine.invariants` (con fallback a `.invariants`).
    2. Implementar función auxiliar `_resolve_distractor_rationale(...)` que:
       - Extraiga el `error_rationale` del autor.
       - Si es explícito y no es placeholder genérico (`"Opción incorrecta."`, `"Distractor."`, `"Incorrecto."`, etc.), preservarlo.
       - Si no hay `error_rationale` explícito del autor, heredar desde `cta_distractors_map` evaluando campos válidos (`wrong_belief`, `omitted_step`, `manifestation`, `remediation_hint`) y validando que el candidato pase `validate_katex_syntax` tras `sanitize_katex_syntax`.
       - Integrar en los bloques de `multiple_choice_7_options` y `multiple_select`.

## 3. Estado del Pre-Flight
- **Bloqueos:** Cero (0). No se requiere escalamiento `BLOCKER`.
- **Alineación:** 100% agnóstico al dominio, Milestone 3 compliant.
- **Acción inmediata:** Proceder a la implementación en `assemble.py` y creación de `tests/test_assemble_katex_and_rationale.py`.
