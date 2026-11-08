# DISPATCH — Stream 1C (Fase B: Auditor Forense Read-Only)

- **Parent Conversation ID:** `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1c_audit`
- **Impl DISPATCH:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1c_impl\DISPATCH.md`
- **Impl Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1c_impl\handoff.md`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1c_audit\audit_report.md` `[NEW]`

PROHIBIDO tocar cualquier archivo de producción o `tests/`.

## Protocolo de Auditoría Forense (Stream 1C)
1. Verifica `git status --short` y respeto estricto de frontera de Stream 1C.
2. Inspecciona con `read_file` en bloques amplios (`400-800` líneas):
   - `engine/sandbox.py`: desenrollado `cc_res.item()` + `if cc_res is not True:` en ambos caminos (`execute_sandbox_instance` y `execute_sandbox_batch`) bloqueando `np.bool_(False)`, `False`, `None`, `0`, y soporte de verificadores 2-arg `(cand, v)`.
   - `engine/instantiate.py`: *Rejection Sampling* determinista por sub-semilla con tope de seguridad anti-clonación (`<= 20%` reintentos, max 8 sub-semillas).
   - `engine/invariants.py` & `assemble.py`: integración `pykatex.renderToString` con caché LRU y limpieza `"\u0332"` -> `"^"`, invariantes `KaTeXAST` (prosa `\text{}` `<= 45`, cuantificadores vacuos, `\dot{5}`) y canonicalizador `+ -5` -> `- 5`.
   - `check_templates.py`: fix caché fría (`L3361` sin `and shard_py is None`), retiro del bypass `0.25` (`div_ratio >= 0.50`), `R-16` activo, refutación estricta de distractores en `check_single_template` y agregación compacta de reportes por semilla.
   - `examples/edo/` y `examples/edp/`: 4 arquetipos reales, `assumptions` en `cta.json` y verificador genuino en `Hab-01.json` ($x>0, y>0, a \ge 2$).
   - Cero subcadenas Zero-Domain prohibidas en los `.py` de Stream 1C.
3. Ejecuta independientemente:
```powershell
& ".venv\Scripts\python.exe" -m pytest -o addopts="" tests/test_sandbox_adversarial.py tests/test_sandbox_gil_and_circuit_breaker.py tests/test_engine_invariants_adversarial.py tests/test_assemble_katex_and_rationale.py tests/test_assemble_sanitize_katex_r23.py tests/test_katex_prairielearn_tokens.py tests/test_c2c_error_aggregation.py tests/test_template_variability.py tests/test_blind_guess_empirical.py -q
```
4. Escribe `audit_report.md` y envía `PASS:: Stream 1C (<N> passed)` o `REJECT:: Stream 1C | <archivo:línea> | <causa>` a `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`.
