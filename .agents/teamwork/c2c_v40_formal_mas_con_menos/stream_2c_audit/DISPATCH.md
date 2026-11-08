# DISPATCH — Stream 2C (Fase B: Auditor Forense Read-Only — Gate 2)

- **Parent Conversation ID:** `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_2c_audit`
- **Impl DISPATCH:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_2c_impl\DISPATCH.md`
- **Impl Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_2c_impl\handoff.md`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_2c_audit\audit_report.md` `[NEW]`

PROHIBIDO tocar cualquier archivo de producción o `tests/`.

## Protocolo de Auditoría Forense (Stream 2C)
1. Verifica `git status --short` y que Stream 2C solo haya tocado sus 4 suites de test.
2. Inspecciona con `read_file`:
   - Que las 3 suites de replay forense mantengan intacto su rigor histórico actualizado a `MIN_ARCHETYPES = 4`.
   - Que `tests/test_c2c_v40_formal_certification.py` pruebe genuinamente `np.bool_(False)` en `sandbox.py`, Triple Contrato `ver_*`, DSL `Form-C` (`<= 65` líneas, `< 15 KB` JSON), `Z3`/`SymPy` `ast.Div`, pruebas basadas en propiedades con `hypothesis` y Regla B con `RejectionSpec`.
3. Ejecuta independientemente:
```powershell
& ".venv\Scripts\python.exe" -m pytest -o addopts="" tests/test_forensic_replay_ab30cf91.py tests/test_forensic_shard06_and_variance_v34.py tests/test_sweetspot_v35_cta_and_shards.py tests/test_c2c_v40_formal_certification.py -q
```
4. Escribe `audit_report.md` y envía `PASS:: Stream 2C (<N> passed)` o `REJECT:: Stream 2C | <archivo:línea> | <causa>` a `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`.
