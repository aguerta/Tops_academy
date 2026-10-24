# DISPATCH — Stream 1A (Fase 2: Mejorador `impr_1a`)

## 1. Rol y Frontera Exclusiva de Escritura (`Exclusive Write Boundaries`)
Eres el **Mejorador (Improver) del Stream 1A** bajo `/flash-triad-orchestrator`.
- **Carpeta de Gobernanza:** `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1a_impr/`
- **Archivos de Producción Permitidos (ÚNICOS que puedes modificar):**
  1. `.agents/skills/content-to-course/engine/assemble.py`
  2. `tests/test_assemble_katex_and_rationale.py`
- **Artefactos de Gobernanza Permitidos:**
  - `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1a_impr/BRIEFING.md`
  - `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1a_impr/handoff.md`

## 2. Instrucciones de Endurecimiento
1. Lee `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1a_impl/handoff.md`, `.agents/skills/content-to-course/engine/assemble.py` y `tests/test_assemble_katex_and_rationale.py`. Escribe `BRIEFING.md`.
2. Audita y endurece casos borde en `engine/assemble.py`:
   - Prueba expresiones complejas anidadas dentro de `\frac`, `\dfrac`, `\tfrac`, `\cfrac` con múltiples subíndices y superíndices (`b_{IV}`, `b_{LS}`, `\hat{\beta}_{2SLS}`, `X'_{i}X_{i}`, matrices y `\text{Var}[b_{IV}]`) tanto cuando las llaves globales están balanceadas como cuando hay otra llave desbalanceada fuera del `\frac`.
   - Verifica que `_resolve_distractor_rationale` (o equivalente) funcione idénticamente tanto para `multiple_choice_7_options` como para `multiple_select`, y que valide `validate_katex_syntax` sobre el string final tras interpolar variables y aplicar `sanitize_katex_syntax`.
   - Verifica que no exista ninguna referencia hardcodeada a un curso específico en `engine/assemble.py`.
3. Amplía `tests/test_assemble_katex_and_rationale.py` con casos adversarios adicionales y ejecuta `.venv\Scripts\python.exe -m pytest tests/test_assemble_katex_and_rationale.py tests/test_katex_prairielearn_tokens.py tests/test_latex_engine.py tests/test_engine_invariants_adversarial.py`.
4. Escribe `handoff.md` y envía `DONE:: Stream 1A Improver completado` a `526cfac0-d37b-49c9-bf09-00b5c520add2`.
