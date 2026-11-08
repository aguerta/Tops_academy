# DISPATCH — Stream 1E (Fase B: Auditor Forense Read-Only)

- **Parent Conversation ID:** `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1e_audit`
- **Impl DISPATCH:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1e_impl\DISPATCH.md`
- **Impl Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1e_impl\handoff.md`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1e_audit\audit_report.md` `[NEW]`

PROHIBIDO tocar cualquier archivo de producción o `tests/`.

## Protocolo de Auditoría Forense (Stream 1E)
1. Verifica `git status --short` y frontera exclusiva de Stream 1E.
2. Inspecciona con `read_file`:
   - `engine/interstage_schemas.py`: `ArtifactCertificate`, `CompileAttemptRecord`, `RejectionSpec` (con normalización `REJECTED` y sincronización bidireccional `failing_shards`<->`affected_shards` y `grouped_by_rule`<->`groups`).
   - `judge.py`: verificación obligatoria pre-juez (`cross_check` + `check_instance_invariants`), default 1-seed cuando hay verificador (respetando overrides explícitos), `resolve_neuro_symbolic_verdict` con $\alpha_{\text{Kernel}} = 0$ y emisión de `judge.cert.json`.
   - `course_publisher.py` & `standardized_audit_engine.py`: emisión de `publish_rejection_spec.json` vía `RejectionSpec`, estampado `contract_version=2` / `min_archetypes=4`, `publish.cert.json`, y `ArchetypeEntropyLinter` exigiendo `4` en `contract_version >= 2` mientras preserva `3` en cursos legacy publicados.
   - Cero subcadenas Zero-Domain prohibidas en `interstage_schemas.py`, `judge.py`, `course_publisher.py`.
3. Ejecuta independientemente:
```powershell
& ".venv\Scripts\python.exe" -m pytest -o addopts="" tests/test_new_audit_linters.py tests/test_c2c_validator_prescriptive.py tests/test_dispatch_scope.py tests/test_pipeline_optimizations.py tests/test_c2c_straggler_and_postproduction_prevention.py -q
```
4. Escribe `audit_report.md` y envía `PASS:: Stream 1E (<N> passed)` o `REJECT:: Stream 1E | <archivo:línea> | <causa>` a `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`.
