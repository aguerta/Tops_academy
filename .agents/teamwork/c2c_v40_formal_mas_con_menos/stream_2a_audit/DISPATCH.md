# DISPATCH — Stream 2A (Fase B: Auditor Forense Read-Only — Gate 2)

- **Parent Conversation ID:** `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_2a_audit`
- **Impl DISPATCH:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_2a_impl\DISPATCH.md`
- **Impl Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_2a_impl\handoff.md`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_2a_audit\audit_report.md` `[NEW]`

PROHIBIDO tocar cualquier archivo de producción o `tests/`.

## Protocolo de Auditoría Forense (Stream 2A)
1. Verifica `git status --short` y frontera exclusiva de Stream 2A (`run.py`, `SKILL.md`, `.agents/rules/c2c-quality-invariants.md` y sus 7 suites).
2. Inspecciona con `read_file`:
   - `run.py`: fast-path `< 5 ms` por `shard_XX.cert.json` en `--stage templates` y `--stage certify` (validando hashes SHA-256 de source, cta y cada template JSON), `--stage gates` ejecutando `build + verify + auditoría QA + repair-matrix`, `--stage repair-matrix` leyendo `grouped_by_rule` + `diagnostics_by_competency` + `failing_shards`, lock `.c2c_subagent_lock.json` con campos FSM/presupuesto, y cero subcadenas Zero-Domain en `run.py`.
   - `SKILL.md` y `.agents/rules/c2c-quality-invariants.md` alineados al contrato C2C v4.0.
3. Ejecuta independientemente:
```powershell
& ".venv\Scripts\python.exe" -m pytest -o addopts="" tests/test_prompts_contract_alignment.py tests/test_bootstrap_and_wave_streaming.py tests/test_run_templates_and_dispatch_repair.py tests/test_append_workflow.py tests/test_c2c_v321_multi_instance_and_append.py tests/test_skill.py tests/test_delete_course.py -q
```
4. Escribe `audit_report.md` y envía `PASS:: Stream 2A (<N> passed)` o `REJECT:: Stream 2A | <archivo:línea> | <causa>` a `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`.
