# DISPATCH — Stream 1A (Fase 2: Mejorador)

- **Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1a_impr`
- **Impl Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1a_impl\handoff.md`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\partition_corpus.py`
2. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\ingest.py`
3. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\prepare.py`
4. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\compile_cta.py`
5. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\cta_merge.py`
6. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\check_cta.py`
7. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_cta_mapreduce.py`
8. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_cta_merge_prereq_scoping.py`
9. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_c2c_v321_comp1_cta.py`
10. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_cta_healing.py`
11. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_cta_sweetspot_and_autoheal.py`
12. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_fast_ingest_and_cta_append.py`
13. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_handouts.py`
14. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1a_impr\handoff.md` `[NEW]`

PROHIBIDO tocar cualquier otro archivo.

## Objetivos de Endurecimiento (Fase 2 — Mejorador)
1. Lee `stream_1a_impl/handoff.md` y revisa con `read_file` los 6 módulos de producción de `Stream 1A` y las 7 suites asignadas.
2. **Contratos Inter-Stream con `Stream 1C` (`dispatch.py`) y `Stream 2A` (`run.py`) (`Matiz 3` y `Matiz 4a`):**
   - Confirma que `merge_cta_parts(work_dir)` **JAMÁS** escribe `work/cta.json` ni `work/cta.md` tanto cuando `len(part_files) == 1` como cuando `len(part_files) >= 2`.
   - Confirma que `prepare_harmonize_from_single_draft(work_dir)` esté exportado limpiamente en `cta_merge.py` con firma clara `prepare_harmonize_from_single_draft(work_dir: Path | str) -> dict`, normalizando `Path(work_dir)`, eliminando `work/cta.json` si aún no se ha aplicado armonización, preservando `work/cta_draft.json`, `work/cta_outline.json` (con nodos `read_only_base: True` cuando exista `delta_manifest.json`) y `work/duplicate_candidates.json` (`>= 0.30`).
   - Confirma que `cta_merge.py` también soporte invocación CLI si `run.py` lo invoca como módulo/función o subcomando (revisa CLI `main()` de `cta_merge.py` por si conviene exponer `--prepare-single-draft` además de la función Python).
   - En `apply_harmonize()`, verifica todos los formatos plausibles que un subagente `c2c_cta_harmonizer` (`flash`) puede emitir en `work/cta_harmonize.json`:
     - `"duplicate_decisions"`: entradas con `decision == "merge"` usando `keep_id` + `drop_id` / `drop_ids`, `id1` + `id2` + `keep_id`, o `source_id` / `target_id`;
     - `"merges"` / `"merge"`;
     - `"add_prerequisites"` / `"prerequisite_additions"` / `"prerequisite_updates"` (tanto lista de `{"id": ..., "add": [...]}` / `{"competency_id": ..., "prerequisites": [...]}` como dict `{cid: [prereqs]}`);
     - Absorción hacia un ID `[BASE]` de `existing_competency_ids`: descarta el nodo delta duplicado, redirige prerrequisitos de otros nodos delta al ID `[BASE]`, evita auto-ciclos `cid in prereqs`, y pasa `allowed_prereq_ids=existing_competency_ids` tanto a `check_prerequisites_dag` como a `validate_cta_rules`.
3. **Endurecimiento de Fail-Fast `[KATEX-PROSE-OVERFLOW]` en Stage 1 (`Matiz 2`):**
   - Verifica en `check_cta.py` el conteo balanceado de llaves anidadas en `\text{...}`, `\textrm{...}`, `\mathrm{...}`, límite exacto `45` (pasa) vs `46` (falla con `[KATEX-PROSE-OVERFLOW]`, nunca `R-23`), cobertura de `name`, `description`, `description_latex`, `source_examples` y los 6 campos de cada distractor (`manifestation`, `remediation_hint`, `wrong_belief`, `correct_belief`, `omitted_step`, `trigger`), y cero mensajes duplicados entre `validate_distractor_math` y `check_cta_katex`.
4. **Endurecimiento de Rutas Windows/POSIX y Regla Zero-Domain:**
   - Verifica normalización `.as_posix()` en `pre_cta_manifest.json` (`partition_corpus.py` e `ingest.py`).
   - Escanea los 6 archivos `.py` de `Stream 1A` confirmando **0 subcadenas Zero-Domain prohibidas** (`edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi` — atención a `puedo`/`quedo`/`heredo`/`regresión`).

## Verificación
Ejecuta (sin usar `--help` sobre scripts de `content-to-course/` ni `python -c` leyendo `"content-to-course/"`):
```powershell
& ".venv\Scripts\python.exe" -m pytest tests/test_cta_mapreduce.py tests/test_cta_merge_prereq_scoping.py tests/test_c2c_v321_comp1_cta.py tests/test_cta_healing.py tests/test_cta_sweetspot_and_autoheal.py tests/test_fast_ingest_and_cta_append.py tests/test_handouts.py -q
```
Escribe `handoff.md` en `stream_1a_impr/` y envía `DONE:: Stream 1A Impr completado (<N> passed)` a `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`.
