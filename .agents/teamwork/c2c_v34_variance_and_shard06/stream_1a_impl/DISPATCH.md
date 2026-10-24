# DISPATCH — Stream 1A (Fase 1: Implementador `impl_1a`)

## 1. Rol y Frontera Exclusiva de Escritura (`Exclusive Write Boundaries`)
Eres el **Implementador del Stream 1A** bajo `/flash-triad-orchestrator`.
- **Carpeta de Gobernanza:** `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1a_impl/`
- **Archivos de Producción Permitidos (ÚNICOS que puedes modificar):**
  1. `.agents/skills/content-to-course/engine/assemble.py`
  2. `tests/test_assemble_katex_and_rationale.py` *(nuevo archivo de tests unitarios)*
- **Artefactos de Gobernanza Permitidos:**
  - `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1a_impl/BRIEFING.md`
  - `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1a_impl/handoff.md`
- **PROHIBIDO** editar cualquier otro archivo del repositorio.

## 2. Paso 0 Obligatorio (*Pre-Flight Sanity Check*)
Antes de realizar cualquier edición:
1. Lee `.agents/skills/content-to-course/engine/assemble.py` (especialmente `sanitize_katex_syntax` en líneas 280–325 y `assemble_question` en líneas 490–680) y `.agents/skills/content-to-course/engine/invariants.py` (solo lectura para ver cómo funciona `validate_katex_syntax`).
2. Escribe `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1a_impl/BRIEFING.md` confirmando las líneas exactas y firmas reales. Si encuentras cualquier bloqueo fuera de tu frontera, detén ediciones y envía `BLOCKER:: <archivo:línea> | <causa> | <opciones>` al Orquestador (`526cfac0-d37b-49c9-bf09-00b5c520add2`).

## 3. Especificación Técnica de Implementación (100% Agnóstica al Dominio)

### A. Blindaje de `sanitize_katex_syntax` (`.agents/skills/content-to-course/engine/assemble.py` L280–L322)
1. **Causa raíz del bug `b_}{LS}`:**
   - En `sanitize_katex_syntax`, `frac_inner_fix` se ejecuta incondicionalmente incluso cuando `text.count("{") == text.count("}")` (llaves perfectamente balanceadas).
   - Además, el patrón actual `r"(\\(?:frac|dfrac|tfrac|cfrac)\s*\{[^{}]*(?:\\[a-zA-Z]+|[_^])\s*\{[^{}]*\}[^{}\\]*)\{"` permite que el tramo `[^{}\\]*` termine en `_` o `^` justo antes de `\{`. En cualquier expresión como `$H = \frac{(b_{IV} - b_{LS})^2}{\text{Var}[b_{IV}] + \text{Var}[b_{LS}]}$`, toma la `{` del segundo subíndice `{LS}` y la reemplaza por `}{`, corrompiendo `b_{LS}` en `b_}{LS}`!
2. **Corrección requerida:**
   - Ejecutar `frac_inner_fix` y `frac_simple_fix` **únicamente** cuando `text.count("{") > text.count("}")`.
   - Además, dentro de `frac_inner_fix`, prohibir que el carácter inmediatamente anterior a `\{` sea `_` o `^` cambiando `[^{}\\]*\{` por `[^{}\\_^]*\{`, y asegurar que solo repare un `\frac` cuando realmente le falte el cierre `}` de su numerador (nunca rompiendo un `\frac{...}{...}` que ya tiene su `}{` o cuyos subíndices están dentro de paréntesis `( ... )`).
   - Si tras aplicar una pasada de `frac_inner_fix` o `frac_simple_fix` el resultado empeora o introduce una secuencia inválida como `_}{` o `^}{`, revertir al texto previo antes del reemplazo.

### B. Respeto al `error_rationale` del Autor y Fallback Seguro en `assemble_question` (`.agents/skills/content-to-course/engine/assemble.py` L515–L535 y L634–L654)
1. **Causa raíz de la sobreescritura silenciosa:**
   - En `assemble_question` (tanto en `multiple_choice_7_options` L521–L529 como en `multiple_select` L639–L643), el código toma `rationale = d.get("error_rationale") or d.get("rationale") or ...`, e inmediatamente después, si `d_id in cta_distractors_map`, **sobreescribe incondicionalmente** `rationale` con `d_entry.get("manifestation") or d_entry.get("wrong_belief") or d_entry.get("omitted_step") or rationale`.
   - Esto impedía que el autor o el agente `c2c_repair` corrigieran `error_rationale` en `<shard_id>_data.py`, e inyectaba `manifestation` crudo sin validar sus llaves KaTeX.
2. **Corrección requerida:**
   - Definir una función auxiliar limpia (ej. `_resolve_distractor_rationale(d_dict, d_id, cta_distractors_map, default_fallback)`):
     - Extraer el rationale provisto por el autor: `author_rat = (d_dict.get("error_rationale") or d_dict.get("rationale") or "").strip()`.
     - Considerar `author_rat` como explícito y válido si no está vacío y no es un placeholder genérico por defecto (como `"Opción incorrecta."`, `"Distractor."`, `"Incorrecto."`).
     - **Si `author_rat` es explícito y válido:** **preservar `author_rat`** como base. Si `cta_distractors_map` tiene `remediation_hint` y ese texto no está ya contenido en `author_rat`, se conserva la adición limpia de `remediation_hint` tal como ya hace el código en L531–L533.
     - **Si `author_rat` está vacío o es genérico (modo DRY inheritance desde `cta.json`):** construir `rationale` desde `d_entry = cta_distractors_map.get(d_id, {})` prefiriendo una combinación segura o el primer campo válido entre `wrong_belief`, `omitted_step`, `manifestation`, `remediation_hint`, pero **verificando con `validate_katex_syntax` (de `engine.invariants`)** que si se usa `manifestation`, este pase `validate_katex_syntax` tras `sanitize_katex_syntax` (si `manifestation` tiene LaTeX desbalanceado, caer automáticamente a `wrong_belief` o `omitted_step` o `remediation_hint`).
   - Aplicar esta misma lógica tanto en `multiple_choice_7_options` (L520–L535) como en `multiple_select` (L636–L653).

## 4. Verificación y Entrega
1. Crea `tests/test_assemble_katex_and_rationale.py` probando exhaustivamente:
   - Que `sanitize_katex_syntax` deje 100% intacta `$H = \frac{(b_{IV} - b_{LS})^2}{\text{Var}(b_{IV}) - \text{Var}(b_{LS})}$` y `$H = \frac{(b_{IV} - b_{LS})^2}{\text{Var}[b_{IV}] + \text{Var}[b_{LS}]}$`, así como múltiples subíndices/superíndices dentro de `\frac`, `\dfrac`, `\tfrac`, incluso si en otra parte del string hubiese una llave suelta.
   - Que `sanitize_katex_syntax` siga reparando casos genuinos de `\frac{a_{1}{b}` (donde realmente falta `}` antes de `{b}`).
   - Que `assemble_question` preserve el `error_rationale` explícito del autor cuando se provee en el distractor, incluso si `cta_distractors_map` tiene un `manifestation` distinto o con LaTeX roto.
   - Que `assemble_question` herede automáticamente desde `cta_distractors_map` cuando el autor omita `error_rationale` (`None` o `""`), saltando `manifestation` si su LaTeX está roto y usando `wrong_belief` / `omitted_step` / `remediation_hint`.
2. Ejecuta `.venv\Scripts\python.exe -m pytest tests/test_assemble_katex_and_rationale.py tests/test_katex_prairielearn_tokens.py tests/test_latex_engine.py`.
3. Escribe `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1a_impl/handoff.md` y envía `DONE:: Stream 1A Implementer completado` a `526cfac0-d37b-49c9-bf09-00b5c520add2`.
