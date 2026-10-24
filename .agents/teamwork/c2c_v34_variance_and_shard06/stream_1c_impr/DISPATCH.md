# DISPATCH — Stream 1C (Fase 2: Mejorador `impr_1c`)

## 1. Rol y Frontera Exclusiva de Escritura (`Exclusive Write Boundaries`)
Eres el **Mejorador (Improver) del Stream 1C** bajo `/flash-triad-orchestrator`.
- **Carpeta de Gobernanza:** `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1c_impr/`
- **Archivos de Producción Permitidos (ÚNICOS que puedes modificar):**
  1. `.agents/skills/content-to-course/dispatch.py`
  2. `.agents/skills/content-to-course/system_prompts/lean/prompt_shard_author.md`
  3. `.agents/skills/content-to-course/system_prompts/prompt_shard_author.md`
  4. `.agents/skills/content-to-course/system_prompts/lean/prompt_repair.md`
  5. `.agents/skills/content-to-course/system_prompts/prompt_repair.md`
  6. `tests/test_dispatch_turn0_and_milestone3_prompts.py`
- **Artefactos de Gobernanza Permitidos:**
  - `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1c_impr/BRIEFING.md`
  - `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1c_impr/handoff.md`

## 2. Instrucciones de Endurecimiento
1. Lee `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1c_impl/handoff.md` y los archivos dentro de tu frontera. Escribe `BRIEFING.md`.
2. Revisa y endurece casos borde:
   - Verifica en `dispatch.py` qué ocurre cuando en `cta.json` un distractor no tiene `correct_belief` o `manifestation` (o son `None`/vacíos) para que nunca se imprima `"None"` literal en `author_XX.json`.
   - Verifica que en `dispatch_repair` se limpien tanto `pass_{shard_id}.json` como archivos `pass_*.json` relacionados con las competencias reparadas, sin lanzar excepción si `.check_attempts` no existe o está bloqueado temporalmente.
   - Verifica que todos los snippets de código en `prompt_shard_author.md` (Full + Lean) sean 100% válidos sintácticamente en Python y que `lean/prompt_shard_author.md` tenga un margen seguro bajo el límite de 4,750 / 5,000 bytes.
   - Asegúrate de que no exista ninguna mención hardcodeada a un curso o libro específico (100% agnóstico al dominio).
3. Amplía `tests/test_dispatch_turn0_and_milestone3_prompts.py` con estos casos borde y ejecuta `.venv\Scripts\python.exe -m pytest tests/test_dispatch_turn0_and_milestone3_prompts.py tests/test_prompts_contract_alignment.py tests/test_c2c_v321_comp3_dispatch.py tests/test_c2c_v321_comp4_prompts.py tests/test_dispatch_scope.py`.
4. Escribe `handoff.md` y envía `DONE:: Stream 1C Improver completado` a `526cfac0-d37b-49c9-bf09-00b5c520add2`.
