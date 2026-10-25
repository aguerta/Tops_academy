# DISPATCH — Stream 1C (Fase 3: Auditor Forense `audit_1c`)

## 1. Rol y Frontera Exclusiva de Escritura
Eres el **Auditor Forense del Stream 1C** bajo `/flash-triad-orchestrator`.
- **Carpeta de Gobernanza (ÚNICA donde puedes escribir):** `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1c_audit/` (`BRIEFING.md` y `handoff.md`).
- **PROHIBIDO** modificar cualquier archivo de producción o de tests.

## 2. Checklist de Auditoría Forense
1. Lee `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1c_impl/handoff.md` y `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1c_impr/handoff.md`. Escribe `BRIEFING.md`.
2. Inspecciona `git diff` sobre los archivos del Stream 1C (`.agents/skills/content-to-course/dispatch.py`, `system_prompts/lean/prompt_shard_author.md`, `system_prompts/prompt_shard_author.md`, `system_prompts/lean/prompt_repair.md`, `system_prompts/prompt_repair.md`, `tests/test_dispatch_turn0_and_milestone3_prompts.py`):
   - Confirma que Stream 1C no tocó ningún archivo fuera de su frontera exclusiva.
   - Verifica que `dispatch_authors` inyecte `correct_belief`, `manifestation` y `remediation_hint` en `author_XX.json` con la directriz Turn-0 autosuficiente (cero lectura innecesaria de PDFs en Turno 1) y 100% agnóstico al dominio (sin referencias hardcodeadas a cursos o libros).
   - Verifica que `prompt_shard_author.md` (Full + Lean) especifique los 4 arquetipos disjuntos del Milestone 3 con formato DRY de distractores y que `lean/*.md` respete los límites de tamaño en bytes.
   - Verifica que `dispatch_repair` limpie `pass_<shard_id>.json`.
3. Ejecuta independientemente `.venv\Scripts\python.exe -m pytest tests/test_dispatch_turn0_and_milestone3_prompts.py tests/test_prompts_contract_alignment.py tests/test_c2c_v321_comp3_dispatch.py tests/test_c2c_v321_comp4_prompts.py tests/test_dispatch_scope.py`.
4. Escribe `handoff.md` en `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1c_audit/` y envía `PASS:: Stream 1C Audit aprobado` (o `REJECT:: <archivo:línea> | <causa>`) a `526cfac0-d37b-49c9-bf09-00b5c520add2`.
