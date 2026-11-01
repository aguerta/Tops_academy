# DISPATCH — Stream 2C (Fase 2: Mejorador — Forensic Replays)

- **Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_2c_impr`
- **Impl Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_2c_impl\handoff.md`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre (**0 archivos de producción**):
1. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_forensic_replay_ab30cf91.py`
2. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_forensic_shard06_and_variance_v34.py`
3. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_sweetspot_v35_cta_and_shards.py`
4. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_2c_impr\handoff.md` `[NEW]`

PROHIBIDO tocar cualquier archivo de producción o cualquier otro test.

## Objetivos de Endurecimiento (Fase 2 — Mejorador)
1. Lee `stream_2c_impl/handoff.md` y revisa con `read_file` (bloques amplios `400-800` líneas) los 3 archivos de replay forense.
2. Verifica que ninguna aserción forense haya sido debilitada artificialmente y añade cobertura adversaria dentro de las 3 suites para certificar los cierres de la síntesis forense:
   - En `test_sweetspot_v35_cta_and_shards.py`: certifica que un corpus `> 25` páginas (ej. 30 o 59 págs) promueve automáticamente a `mapreduce`, que `check_cta.py` bloquea Fail-Fast `[KATEX-PROSE-OVERFLOW]` (`\text{...} > 45` chars) ya en Stage 1, y que `subagent_types.json` mantiene LF `\n` puro (`0` `\r\n`).
   - En `test_forensic_shard06_and_variance_v34.py`: certifica que `[TPL-STATIC-OPT]` bloquea `len(unique_correct) == 1` incluso cuando `vars = {}` está vacío (`Matiz 4b`), y que `[TPL-DYNAMIC-RATIONALE]` bloquea distractores con `error_rationale` estático sin `@var@` (`Brecha 1`).
   - En `test_forensic_replay_ab30cf91.py`: certifica que `lean/prompt_shard_author.md <= 4,750` bytes y el contrato Tri-Banda Multimodal (`min_archetypes == 3`).

## Verificación
Ejecuta:
```powershell
& ".venv\Scripts\python.exe" -m pytest tests/test_forensic_replay_ab30cf91.py tests/test_forensic_shard06_and_variance_v34.py tests/test_sweetspot_v35_cta_and_shards.py -q
```
Escribe `handoff.md` en `stream_2c_impr/` y envía `DONE:: Stream 2C Impr completado (<N> passed)` a `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`.
