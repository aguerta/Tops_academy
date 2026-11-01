# DISPATCH — Stream 2C (Fase 3: Auditor Forense Read-Only — Forensic Replays)

- **Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_2c_audit`
- **Impl Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_2c_impl\handoff.md`
- **Impr Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_2c_impr\handoff.md`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_2c_audit\audit_report.md` `[NEW]`

PROHIBIDO tocar cualquier archivo de producción o `tests/`.

## Protocolo de Auditoría Forense (Stream 2C)
1. **Higiene y Frontera de Stream 2C:**
   - Ejecuta `git status --short` y verifica cero scripts temporales sueltos ni `.c2c_subagent_lock.json` activos en el workspace, y que `Stream 2C` haya tocado únicamente sus 3 suites (`test_forensic_replay_ab30cf91.py`, `test_forensic_shard06_and_variance_v34.py`, `test_sweetspot_v35_cta_and_shards.py`) y `0` archivos de producción.
2. **Inspección de Tests Forenses (`read_file` en bloques amplios):**
   - Verifica que no se hayan debilitado aserciones forenses, que las 3 suites validen el contrato C2C v3.8 (`min_archetypes == 3`, `Form-B` Tri-Banda Multimodal, 3-tuplas `@var@` `[TPL-DYNAMIC-RATIONALE]`, `[TPL-STATIC-OPT]` con `vars == {}`, `[KATEX-PROSE-OVERFLOW]` en Stage 1, promoción `> 25` págs a `mapreduce`, LF en `subagent_types.json`, `<= 4,750 B` en `lean/prompt_shard_author.md`).
3. **Ejecución Independiente de las 3 Suites:**
   ```powershell
   & ".venv\Scripts\python.exe" -m pytest tests/test_forensic_replay_ab30cf91.py tests/test_forensic_shard06_and_variance_v34.py tests/test_sweetspot_v35_cta_and_shards.py -q
   ```
4. Escribe `audit_report.md` en `stream_2c_audit/` y envía `PASS:: Stream 2C (<N> passed)` o `REJECT:: Stream 2C | <archivo:línea> | <causa>` a `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`.
