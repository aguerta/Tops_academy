# DISPATCH — Stream 1A (Fase 3: Auditor Forense `audit_1a`)

## 1. Rol y Frontera Exclusiva de Escritura
Eres el **Auditor Forense del Stream 1A** bajo `/flash-triad-orchestrator`.
- **Carpeta de Gobernanza (ÚNICA donde puedes escribir):** `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1a_audit/` (`BRIEFING.md` y `handoff.md`).
- **PROHIBIDO** modificar cualquier archivo de producción o de tests.

## 2. Checklist de Auditoría Forense
1. Lee `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1a_impl/handoff.md` y `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1a_impr/handoff.md`. Escribe `BRIEFING.md`.
2. Inspecciona `git diff -- .agents/skills/content-to-course/engine/assemble.py` y `tests/test_assemble_katex_and_rationale.py`:
   - Confirma que Stream 1A no modificó ningún archivo fuera de su frontera exclusiva.
   - Verifica que `sanitize_katex_syntax` no corrompa nunca `\frac{(b_{IV} - b_{LS})^2}{\text{Var}[b_{IV}] + \text{Var}[b_{LS}]}` ni expresiones con subíndices/superíndices múltiples dentro de `\frac`/`\dfrac`/`\tfrac`, y que siga reparando `\frac` genuinamente desbalanceados.
   - Verifica que `assemble_question` preserve el `error_rationale` explícito del autor y haga fallback seguro a `cta.json` validando `validate_katex_syntax`.
   - Verifica que el código sea 100% agnóstico al dominio (sin referencias hardcodeadas a cursos).
3. Ejecuta independientemente `.venv\Scripts\python.exe -m pytest tests/test_assemble_katex_and_rationale.py tests/test_katex_prairielearn_tokens.py tests/test_latex_engine.py tests/test_engine_invariants_adversarial.py`.
4. Escribe `handoff.md` en `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1a_audit/` y envía `PASS:: Stream 1A Audit aprobado` (o `REJECT:: <archivo:línea> | <causa>`) a `526cfac0-d37b-49c9-bf09-00b5c520add2`.
