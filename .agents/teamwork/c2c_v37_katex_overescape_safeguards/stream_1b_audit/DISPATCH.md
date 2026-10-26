# DISPATCH — Stream 1B (Fase 3: Auditor Forense)

- **Parent Conversation ID:** `da4d9acf-34da-4bc8-930b-6fb3d28b5744`
- **Impl Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1b_impl\handoff.md`
- **Impr Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1b_impr\handoff.md`
- **Audit Folder (ÚNICA carpeta de escritura):** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1b_audit`

## Regla de Solo Lectura en Producción y Tests
Tienes PROHIBIDO modificar cualquier archivo de producción o de `tests/`. Tu única escritura permitida es `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1b_audit\audit_report.md`.

## Frontera Exclusiva de Stream 1B a Auditar
- `.agents/skills/content-to-course/engine/assemble.py`
- `tests/test_assemble_sanitize_katex_r23.py`

## Checklist de Auditoría Forense
1. Inspecciona `git diff -- .agents/skills/content-to-course/engine/assemble.py` y el contenido de `tests/test_assemble_sanitize_katex_r23.py`.
2. Verifica que no existan archivos basura o scripts temporales en `.agents/teamwork/c2c_v37_katex_overescape_safeguards/stream_1b_impl/` ni `stream_1b_impr/`.
3. Verifica que `sanitize_katex_syntax`:
   - Colapse deterministamente todos los comandos sobreescapados (`\\frac`, `\\text`, `\\to`, `\\mathbb`, `\\right`, `\\alpha`, `\\beta`, `\\theta`, `\\rho`, `\\varepsilon`, `\\times`, `\\Rightarrow`, etc.).
   - Maneje limpiamente secuencias impares `\\\frac` -> `\\ \frac` en matrices sin perder el salto de fila.
   - Reemplace `\centernot\Rightarrow` / `\centernot\implies` -> `\nRightarrow` y variantes.
   - Repare `\text{textVar[barx_n] = O(n)}` -> `\text{Var}[\bar{x}_n] = O(n)` y escape `_` no escapados en `\text{...}` sin duplicar `\_`.
   - Sea 100% idempotente sobre los 4 cursos reales de `courses/*.json`.
4. Ejecuta de forma independiente:
   ```powershell
   pytest tests/test_assemble_sanitize_katex_r23.py tests/test_latex_engine.py tests/test_forensic_shard06_and_variance_v34.py -q
   ```
5. Escribe `audit_report.md` en `stream_1b_audit/` y emite `PASS:: Stream 1B` o `REJECT:: <archivo:línea> | <defecto>`.
