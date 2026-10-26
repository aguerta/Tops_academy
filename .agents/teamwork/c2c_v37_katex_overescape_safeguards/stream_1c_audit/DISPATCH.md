# DISPATCH — Stream 1C (Fase 3: Auditor Forense)

- **Parent Conversation ID:** `da4d9acf-34da-4bc8-930b-6fb3d28b5744`
- **Impl Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1c_impl\handoff.md`
- **Impr Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1c_impr\handoff.md`
- **Audit Folder (ÚNICA carpeta de escritura):** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1c_audit`

## Regla de Solo Lectura en Producción y Tests
Tienes PROHIBIDO modificar cualquier archivo de producción o de `tests/`. Tu única escritura permitida es `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1c_audit\audit_report.md`.

## Frontera Exclusiva de Stream 1C a Auditar
- `.agents/skills/content-to-course/engine/invariants.py`
- `.agents/skills/content-to-course/compile_shard.py`
- `tests/test_invariants_and_shard_overescape_r23.py`

## Checklist de Auditoría Forense
1. Inspecciona `git diff -- .agents/skills/content-to-course/engine/invariants.py .agents/skills/content-to-course/compile_shard.py` y el contenido de `tests/test_invariants_and_shard_overescape_r23.py`.
2. Verifica que no existan archivos basura o scripts temporales en `.agents/teamwork/c2c_v37_katex_overescape_safeguards/stream_1c_impl/` ni `stream_1c_impr/`.
3. Verifica que `validate_katex_syntax` en `invariants.py` y `heal_shard_source_text` en `compile_shard.py` cumplan al 100% con la especificación R-23, invariante inline de `\\`, detección de `\centernot` y `_` en `\text{...}`, y preservación de saltos de fila en matrices.
4. Ejecuta de forma independiente:
   ```powershell
   pytest tests/test_invariants_and_shard_overescape_r23.py tests/test_engine_invariants_adversarial.py tests/test_katex_prairielearn_tokens.py tests/test_shard_compiler_hardening.py -q
   ```
5. Escribe `audit_report.md` en `stream_1c_audit/` y emite `PASS:: Stream 1C` o `REJECT:: <archivo:línea> | <defecto>`.
