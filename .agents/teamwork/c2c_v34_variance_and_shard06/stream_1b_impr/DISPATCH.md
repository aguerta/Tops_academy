# DISPATCH — Stream 1B (Fase 2: Mejorador `impr_1b`)

## 1. Rol y Frontera Exclusiva de Escritura (`Exclusive Write Boundaries`)
Eres el **Mejorador (Improver) del Stream 1B** bajo `/flash-triad-orchestrator`.
- **Carpeta de Gobernanza:** `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1b_impr/`
- **Archivos de Producción Permitidos (ÚNICOS que puedes modificar):**
  1. `.agents/skills/content-to-course/compile_shard.py`
  2. `.agents/skills/content-to-course/check_templates.py`
  3. `tests/test_shard06_and_dry_archetypes.py`
- **Artefactos de Gobernanza Permitidos:**
  - `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1b_impr/BRIEFING.md`
  - `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1b_impr/handoff.md`

## 2. Instrucciones de Endurecimiento
1. Lee `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1b_impl/handoff.md`, `.agents/skills/content-to-course/compile_shard.py`, `.agents/skills/content-to-course/check_templates.py` y `tests/test_shard06_and_dry_archetypes.py`. Escribe `BRIEFING.md`.
2. Revisa y endurece casos borde:
   - Verifica que en `compile_shard.py` la compilación real de `courses/asyntotic_estatistics_v4/work/shards/shard_06_data.py` contra `courses/asyntotic_estatistics_v4/work/cta.json` (puedes probarla en un `tmp_path` copiando `shard_06_data.py`, `cta.json` y `pre_shard_manifest.json` dentro de un test en `tests/test_shard06_and_dry_archetypes.py` sin tocar los archivos reales de `courses/` todavía) pase con **0 errores en modo `--strict`**!
   - Verifica que la herencia DRY de distractores funcione tanto cuando `gen_*` retorna un `dict` (`{"vars": ..., "correct": ..., "distractors": [...]}`) como cuando retorna una `tuple` de 3 elementos `(vars_dict, ans_str, dists_list)`.
   - Verifica que el marcador `.check_attempts/pass_<shard_id>.json` se elimine limpiamente si una compilación posterior falla.
   - Verifica que no quede ningún archivo temporal suelto en el repositorio (`git status --short`).
3. Ejecuta `.venv\Scripts\python.exe -m pytest tests/test_shard06_and_dry_archetypes.py tests/test_compile_shard.py tests/test_shard_compiler_hardening.py tests/test_c2c_case_2b_mastery.py`.
4. Escribe `handoff.md` y envía `DONE:: Stream 1B Improver completado` a `526cfac0-d37b-49c9-bf09-00b5c520add2`.
