# DISPATCH — Stream 1D (Fase B: Auditor Forense Read-Only)

- **Parent Conversation ID:** `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1d_audit`
- **Impl DISPATCH:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1d_impl\DISPATCH.md`
- **Impl Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1d_impl\handoff.md`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1d_audit\audit_report.md` `[NEW]`

PROHIBIDO tocar cualquier archivo de producción o `tests/`.

## Protocolo de Auditoría Forense (Stream 1D)
1. Verifica `git status --short` y frontera exclusiva de Stream 1D.
2. Inspecciona con `read_file`:
   - `plan_shards.py`: `min_archetypes = 4`, tope ponderado `1` `Skill` por shard y propagación de `assumptions`.
   - `dispatch.py`: deduplicación real de `"work_order"` (sin copiar el texto completo de `"Prompt"` ni triplicar `"items"` en `judge`), persistencia de `author_snapshot.json` antes del return anticipado, `/__pycache__/` anidados y `*.cert.json` en `_is_allowed_path`, *Competence Slicing* `< 2 KB` en `dispatch_repair` (cero `cta.json` en `read_paths` de `repair`), `min_archetypes = 4` y `--lean` `True` por defecto.
   - `subagent_types.json`: verifica por código que tenga **0 bytes `\r` (100% LF `\n`)**.
   - `system_prompts/lean/prompt_shard_author.md`: verifica por código `len(read_bytes()) <= 4750`, presencia de **4 arquetipos genuinos no clonados (`1 MC7 + 2 FIB + 1 MS`)**, 16 stems composicionales, `RATS` con `@var@`, `assumption_id` y verificadores `ver_*` que refutan distractores (cero `Form-A` en `prompt_shard_author.md`).
   - Cero subcadenas Zero-Domain prohibidas en `plan_shards.py` y `dispatch.py`.
3. Ejecuta independientemente:
```powershell
& ".venv\Scripts\python.exe" -m pytest -o addopts="" tests/test_dispatch_turn0_and_milestone3_prompts.py tests/test_c2c_v321_comp4_prompts.py tests/test_c2c_v321_comp3_dispatch.py tests/test_weighted_sharding_m7.py tests/test_skill_v3.py tests/test_orchestration_resilience.py -q
```
4. Escribe `audit_report.md` y envía `PASS:: Stream 1D (<N> passed)` o `REJECT:: Stream 1D | <archivo:línea> | <causa>` a `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`.
