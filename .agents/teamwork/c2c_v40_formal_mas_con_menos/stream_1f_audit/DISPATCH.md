# DISPATCH — Stream 1F (Fase B: Auditor Forense Read-Only)

- **Parent Conversation ID:** `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1f_audit`
- **Impl DISPATCH:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1f_impl\DISPATCH.md`
- **Impl Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1f_impl\handoff.md`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1f_audit\audit_report.md` `[NEW]`

PROHIBIDO tocar cualquier archivo de producción o `tests/`.

## Protocolo de Auditoría Forense (Stream 1F)
1. Verifica `git status --short` y frontera exclusiva de Stream 1F.
2. Inspecciona con `read_file`:
   - `src/validator/rules.py` y `psychometric_checker.py`: reglas `R-24` (`check_vacuous_quantifiers`), `R-25` (`check_hint_answer_leak`), `R-26` (`check_option_parenthetical_telltale`), `R-27` (`check_numeric_newton_dot`) implementadas limpiamente sin romper cursos publicados ni degradar el scanner zero-copy `< 10 s`.
   - `repair_loop.py`: lectura tolerante `grouped_by_rule`/`groups` y `failing_shards`/`affected_shards`, *Competence Slicing* `< 2 KB` y recomendación de Matriz 2D, más cero subcadenas Zero-Domain prohibidas en `repair_loop.py`.
3. Ejecuta independientemente:
```powershell
& ".venv\Scripts\python.exe" -m pytest -o addopts="" tests/test_validator.py tests/test_katex_overescape_validator_r23.py -q
```
4. Escribe `audit_report.md` y envía `PASS:: Stream 1F (<N> passed)` o `REJECT:: Stream 1F | <archivo:línea> | <causa>` a `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`.
