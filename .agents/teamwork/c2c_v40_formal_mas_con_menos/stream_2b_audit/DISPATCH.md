# DISPATCH — Stream 2B (Fase B: Auditor Forense Read-Only — Gate 2)

- **Parent Conversation ID:** `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_2b_audit`
- **Impl DISPATCH:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_2b_impl\DISPATCH.md`
- **Impl Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_2b_impl\handoff.md`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_2b_audit\audit_report.md` `[NEW]`

PROHIBIDO tocar cualquier archivo de producción o `tests/`.

## Protocolo de Auditoría Forense (Stream 2B + Tier A 2B Fix)
1. Verifica `git status --short`, `stream_2b_impl/handoff.md` y `tier_a_2b_fix/handoff.md`: confirma que Stream 2B solo haya modificado sus 7 suites de test y que `tier_a_2b_fix` solo haya tocado `compile_shard.py`, `system_prompts/lean/prompt_shard_author.md`, `system_prompts/prompt_shard_author.md` y `subagent_types.json` (verificando LF puro en `subagent_types.json` y `lean/prompt_shard_author.md <= 4,750` bytes).
2. Inspecciona con `read_file`:
   - Que ninguna aserción en las 6 suites de integración haya sido debilitada ni marcada `skip`.
   - Que `tests/test_system_prompts_compile_clean.py` extraiga genuinamente el código de `system_prompts/lean/prompt_shard_author.md`, lo compile en frío con `compile_shard.py --strict` (`min_archetypes=4`), ensamble las preguntas y valide con `validate_course_content(..., strict=True)` y `standardized_audit_engine.run_full_audit` sin errores.
3. Ejecuta independientemente:
```powershell
& ".venv\Scripts\python.exe" -m pytest -o addopts="" tests/test_c2c_solow2_architectural_improvements.py tests/test_c2c_remediation_optimization.py tests/test_c2c_v31_adversarial_plan.py tests/test_c2c_case_2b_mastery.py tests/test_c2c_v321_comp2_shard.py tests/test_pipeline_reparations.py tests/test_system_prompts_compile_clean.py -q
```
4. Escribe `audit_report.md` y envía `PASS:: Stream 2B (<N> passed)` o `REJECT:: Stream 2B | <archivo:línea> | <causa>` a `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`.
