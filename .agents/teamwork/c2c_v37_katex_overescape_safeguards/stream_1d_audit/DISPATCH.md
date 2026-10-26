# DISPATCH — Stream 1D (Fase 3: Auditor Forense)

- **Parent Conversation ID:** `da4d9acf-34da-4bc8-930b-6fb3d28b5744`
- **Impl Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1d_impl\handoff.md`
- **Impr Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1d_impr\handoff.md`
- **Audit Folder (ÚNICA carpeta de escritura):** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1d_audit`

## Regla de Solo Lectura en Producción y Tests
Tienes PROHIBIDO modificar cualquier archivo de producción o de `tests/`. Tu única escritura permitida es `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1d_audit\audit_report.md`.

## Frontera Exclusiva de Stream 1D a Auditar
- `run_platform.py`
- `FUTURE_MILESTONES.md`
- `docs/future_milestones/FUTURE_MILESTONES.md`
- `tests/test_platform_katex_admission_guard.py`

## Checklist de Auditoría Forense
1. Inspecciona `git diff -- run_platform.py FUTURE_MILESTONES.md docs/future_milestones/FUTURE_MILESTONES.md` y el contenido de `tests/test_platform_katex_admission_guard.py`.
2. Verifica que no existan archivos basura o scripts temporales en `.agents/teamwork/c2c_v37_katex_overescape_safeguards/stream_1d_impl/` ni `stream_1d_impr/`.
3. Verifica que `FUTURE_MILESTONES.md` y `docs/future_milestones/FUTURE_MILESTONES.md` estén 100% sincronizados byte a byte.
4. Verifica que `validate_platform_course`, `repair_platform_course_katex` y `scan_courses` cumplan al 100% con el Punto 4 del Protocolo de Protección Definitivo y que `python run_platform.py --scan` reporte `VALID` para los 4 cursos publicados en `courses/`.
5. Ejecuta de forma independiente:
   ```powershell
   pytest tests/test_platform_katex_admission_guard.py tests/test_platform.py -q
   python run_platform.py --scan
   ```
6. Escribe `audit_report.md` en `stream_1d_audit/` y emite `PASS:: Stream 1D` o `REJECT:: <archivo:línea> | <defecto>`.
