# DISPATCH — Stream 1B (Fase 3: Auditor Forense `audit_1b`)

## 1. Rol y Frontera Exclusiva de Escritura
Eres el **Auditor Forense del Stream 1B** bajo `/flash-triad-orchestrator`.
- **Carpeta de Gobernanza (ÚNICA donde puedes escribir):** `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1b_audit/` (`BRIEFING.md` y `handoff.md`).
- **PROHIBIDO** modificar cualquier archivo de producción o de tests.

## 2. Checklist de Auditoría Forense
1. Lee `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1b_impl/handoff.md` y `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1b_impr/handoff.md`. Escribe `BRIEFING.md`.
2. Inspecciona `git diff -- .agents/skills/content-to-course/compile_shard.py .agents/skills/content-to-course/check_templates.py` y `tests/test_shard06_and_dry_archetypes.py`:
   - Confirma que Stream 1B no tocó ningún archivo fuera de su frontera exclusiva y que no existan archivos temporales en la raíz.
   - Verifica la herencia DRY de distractores (tuplas de 2/3 elementos y dicts compactos sin `error_rationale`), la creación/limpieza de `.check_attempts/pass_<shard_id>.json`, el recibo `--output <path>.json`, la priorización de `targets` en `render_compact_aggregated_errors`, y el diagnóstico `R-20` quirúrgico.
   - Verifica que el código de producción sea 100% agnóstico al dominio.
3. Ejecuta independientemente `.venv\Scripts\python.exe -m pytest tests/test_shard06_and_dry_archetypes.py tests/test_compile_shard.py tests/test_shard_compiler_hardening.py tests/test_c2c_case_2b_mastery.py`.
4. Escribe `handoff.md` en `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1b_audit/` y envía `PASS:: Stream 1B Audit aprobado` (o `REJECT:: <archivo:línea> | <causa>`) a `526cfac0-d37b-49c9-bf09-00b5c520add2`.
