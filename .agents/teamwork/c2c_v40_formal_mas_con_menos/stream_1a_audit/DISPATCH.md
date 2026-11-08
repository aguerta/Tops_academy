# DISPATCH — Stream 1A (Fase B: Auditor Forense Read-Only)

- **Parent Conversation ID:** `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1a_audit`
- **Impl DISPATCH:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1a_impl\DISPATCH.md`
- **Impl Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1a_impl\handoff.md`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1a_audit\audit_report.md` `[NEW]`

PROHIBIDO tocar cualquier archivo de producción o `tests/`.

## Protocolo de Auditoría Forense (Stream 1A)
*(Nota: otros streams paralelos de Gate 1 `1B..1F` están trabajando en sus propios archivos disjuntos).*
1. Verifica `git status --short`: cero scripts temporales, cero `.c2c_subagent_lock.json` sueltos y que Stream 1A solo haya tocado `schemas/cta.schema.json`, `compile_cta.py`, `cta_merge.py`, `check_cta.py` y sus 7 suites.
2. Inspecciona en bloques amplios (`400-800` líneas) con `read_file`:
   - Soporte de `assumptions` en 7-tuplas/dicts y bloqueo `[CTA-ASSUMPTIONS-MISSING]` con mapeo de línea exacta cuando `require_assumptions=True` o `CTA_CONTRACT_VERSION >= 2`.
   - `affected_line_count`, `has_syntax_error`, `error_sha256` en `.check_attempts/compile_cta*.json`, splicing `cta_fixes/<CID>.py` y emisión de `cta.cert.json`.
   - Saneamiento KaTeX no-destructivo sobre `r"P(Y \ge $\delta) ...$"` + `pykatex` con limpieza `"\u0332"` -> `"^"`.
   - Detección de ciclos exactos en DAG y monotonicidad $K_t \subseteq K_{t+1}$ en `--append`.
   - Cero subcadenas Zero-Domain prohibidas (`edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`) en `compile_cta.py`, `cta_merge.py`, `check_cta.py`.
3. Ejecuta independientemente:
```powershell
& ".venv\Scripts\python.exe" -m pytest -o addopts="" tests/test_cta_mapreduce.py tests/test_cta_merge_prereq_scoping.py tests/test_c2c_v321_comp1_cta.py tests/test_cta_healing.py tests/test_cta_sweetspot_and_autoheal.py tests/test_fast_ingest_and_cta_append.py tests/test_handouts.py -q
```
4. Escribe `audit_report.md` y envía `PASS:: Stream 1A (<N> passed)` o `REJECT:: Stream 1A | <archivo:línea> | <causa>` a `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`.
