# DISPATCH — Stream 1B (Fase B: Auditor Forense Read-Only)

- **Parent Conversation ID:** `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1b_audit`
- **Impl DISPATCH:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1b_impl\DISPATCH.md`
- **Impl Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1b_impl\handoff.md`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1b_audit\audit_report.md` `[NEW]`

PROHIBIDO tocar cualquier archivo de producción o `tests/`.

## Protocolo de Auditoría Forense (Stream 1B)
1. Verifica `git status --short`: cero scripts temporales, cero `.c2c_subagent_lock.json` sueltos fuera de `tmp_path` y frontera exclusiva respetada (`engine/stage_contract.py`, `compile_shard.py`, `c2c_hook_guard.py`, `budget_guard.py` y sus 9 suites).
2. Inspecciona con `read_file` en bloques amplios (`400-800` líneas):
   - `stage_contract.py`: `CONTRACT_VERSION = 2`, `MIN_ARCHETYPES = 4`, `ARCHETYPE_KINDS`.
   - `compile_shard.py`: soporte dual `Form-C` (`fmt`, `RATS`/`rats`, stems cartesianos `2x2`, firma 2-arg `ver(cand, v)`) + `Form-B`, vínculo `assumption_id` (`[TPL-ASSUMPTION-LINK]`), Triple Contrato `ver_*` (`[VERIFIER-TAUTOLOGY-DETECTED]` refutando los 6 distractores, `[VERIFIER-SWALLOWED-EXCEPTION]`, `[TPL-DEBUG-ARTIFACT]`, `[TPL-AD-HOC-PERTURBATION]`), no-clonación `4/4` de fórmulas en `Skill`, `ast.Div` en `[DIAG-MAGIC-MULT]` + `SymPy`/`Z3`, bloqueo de cuantificadores vacuos / fuga en pistas 1–2 / paréntesis delatores, poda AST de `<CID>.json`, `affected_line_count` y emisión de `shard_XX.cert.json`.
   - `c2c_hook_guard.py`: 100% stdlib pura, `try...except BaseException:` + `sys.exit(0)`, Regla B reparada (`status.upper()` + `failing_shards` $\cup$ `affected_shards`), Matriz 2D `decidir_estrategia_edicion` (`affected_line_count > 5 -> ModularSplicing`), contadores síncronos en `.c2c_subagent_lock.json` y `[REPAIR-NO-FULL-CTA]`.
   - Cero subcadenas Zero-Domain prohibidas en los 4 `.py` de producción.
3. Ejecuta independientemente:
```powershell
& ".venv\Scripts\python.exe" -m pytest -o addopts="" tests/test_m3_archetypes_semantic_gate.py tests/test_compile_shard.py tests/test_shard_compiler_hardening.py tests/test_shard06_and_dry_archetypes.py tests/test_invariants_and_shard_overescape_r23.py tests/test_latex_engine.py tests/test_hook_post_pass_and_write_isolation.py tests/test_watchdog_and_hooks.py tests/test_specific_error_report_and_stem_gate.py -q
```
4. Escribe `audit_report.md` y envía `PASS:: Stream 1B (<N> passed)` o `REJECT:: Stream 1B | <archivo:línea> | <causa>` a `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`.
