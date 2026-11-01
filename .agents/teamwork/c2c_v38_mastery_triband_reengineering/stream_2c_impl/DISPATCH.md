# DISPATCH — Stream 2C (Fase 1: Implementador — Suites Forensic Replays)

- **Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_2c_impl`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre (**0 archivos de producción**):
1. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_forensic_replay_ab30cf91.py`
2. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_forensic_shard06_and_variance_v34.py`
3. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_sweetspot_v35_cta_and_shards.py`
4. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_2c_impl\BRIEFING.md` `[NEW]`
5. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_2c_impl\handoff.md` `[NEW]`

PROHIBIDO modificar cualquier archivo de producción o cualquier otro test. Si detectas un bug real en producción que impida pasar un test válido, usa `BLOCKER:: <archivo:línea> | <causa> | <opciones>`.

## Reglas Pre-Flight y Eficiencia
- Usa `read_file` en bloques amplios (`400-800` líneas por llamada) y ejecuta primero `pytest` sobre las 3 suites para ver de inmediato los fallos exactos por cambio de contrato v3.5 -> v3.8.
- **Hooks:** Prohibido ejecutar `run.py --help` / `dispatch.py --help` o `python -c` mencionando `"content-to-course/"` junto con `open(`, `read_text`, `run.py`, `prepare.py`, `ingest.py`, `dispatch.py`. Usa únicamente `& ".venv\Scripts\python.exe" -m pytest <archivos_test> -q`.
- *(Nota de concurrencia Gate 2: `Stream 2A` está actualizando `run.py` en paralelo; si algún replay invoca `run.py`, ten presente el predicado simétrico `needs_harmonize` en `mapreduce` y `--append`).*

## Especificación Técnica (Adaptación de Replays Forenses a C2C v3.8)
Adapta los fixtures y aserciones de los 3 replays forenses (`ab30cf91`, `v34`, `v35`) al contrato C2C v3.8 preservando intactas todas las verificaciones de resiliencia, aislamiento por shard, paridad LF de `subagent_types.json` y byte-budgets Lean (`<= 4,750 B` en `lean/prompt_shard_author.md`):
1. **`min_archetypes` y Contrato `Form-B` Tri-Banda Multimodal:**
   - Donde los replays esperaban `min_archetypes == 4` por defecto desde `dispatch.py` o `compile_shard.py`, el nuevo default de v3.8 es `min_archetypes == 3` (`--min-archetypes 3`).
   - Los fixtures de shards que deben compilar con `strict=True` deben usar 9-tuplas `Form-B` con `(difficulty, bloom)` explícita cubriendo `{"easy", "medium", "hard"}`, `>= 2` niveles `bloom`, modalidad activa (`>= 2` `FIB`/`MS` en `Hab-*`/`Skill`, `>= 1` `FIB`/`MS` en `C-*`/`H-*`), 3-tuplas de distractores `(did, val, rationale_con_@var@)` (`len >= 20`, unicidad `>= 35%`), `FIB` sin `$` externos, `ver_fn` con comparación real (no `return True`), `>= 3` `stems` genuinos (no `>= 30` sintéticos) y `3..5` `hints >= 25` chars.
   - Si un test en `v35` o `v34` verificaba textos literales antiguos de `prompt_shard_author.md` o `dispatch.py` (como ejemplos de 2-tupla `(did, val)` o `4 arquetipos MC7`), actualízalo para verificar las nuevas directivas v3.8 (Tri-Banda `easy/medium/hard`, `FIB`/`MS`, 3-tupla `@var@`, `[KATEX-PROSE-OVERFLOW]`).
2. **Ingesta `> 25` páginas y `CTA MapReduce` Simétrico:**
   - Donde `test_sweetspot_v35_cta_and_shards.py` o `ab30cf91` probaban PDFs `> 25` páginas (ej. 30-45 págs) esperando modo `direct`, ahora v3.8 promueve determinísticamente todo corpus `> 25` páginas o multi-PDF a `mapreduce` + `slice_pdf_lossless` (`k = max(2, ceil(P/20))`), salvo `force_direct=True` explícito.
   - `merge_cta_parts` genera `cta_draft.json` + `cta_outline.json` (nunca `cta.json` directo) y `apply_harmonize` escribe `cta.json` validando DAG conexo (`connected_components == 1`, `root_ratio <= 0.20`) y `0` `\text{...} > 45` chars.

## Verificación
Ejecuta:
```powershell
& ".venv\Scripts\python.exe" -m pytest tests/test_forensic_replay_ab30cf91.py tests/test_forensic_shard06_and_variance_v34.py tests/test_sweetspot_v35_cta_and_shards.py -q
```
Escribe `BRIEFING.md` antes de editar, `handoff.md` al terminar y notifica a `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589` con `DONE:: Stream 2C Impl completado (<N> passed)`.
