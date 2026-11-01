# DISPATCH — Stream 1A (Fase 1: Implementador)

- **Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1a_impl`

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
14. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1a_impl\BRIEFING.md` `[NEW]`
15. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1a_impl\handoff.md` `[NEW]`

PROHIBIDO modificar cualquier otro archivo.

## Reglas Pre-Flight y Guardias de Entorno
- **Hooks:** Prohibido ejecutar `run.py --help` / `ingest.py --help` / `prepare.py --help` o `python -c` mencionando `"content-to-course/"` junto con `open(`, `read_text`, `ingest.py`, `prepare.py`, `run.py`, `dispatch.py`. Usa `read_file` para leer código y `& ".venv\Scripts\python.exe" -m pytest <archivos_test> -q` para pruebas.
- **Zero-Domain (`test_skill.py`):** En NINGÚN `.py` de `content-to-course/` pueden aparecer (ni siquiera en comentarios) las subcadenas en minúsculas: `edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`. ¡Cuidado en español con `puedo`, `quedo`, `heredo` (`edo`) o `regresión` (`regresi`)! Usa inglés en comentarios de `.py`.
- **Tag KaTeX:** Usa `[KATEX-PROSE-OVERFLOW]`, NUNCA `"R-23"`.

## Especificación Técnica

### 1. `partition_corpus.py` (`slice_pdf_lossless` & `update_pre_cta_manifest`)
- Cuando `num_pages > 25`, escalar `k_parts = max(2, math.ceil(num_pages / 20))` eliminando el antiguo tope `min(4, ...)` (ej. un PDF de 120 páginas produce 6 slices de ~20 páginas respetando outlines semánticos cuando existan).
- En los metadatos de cada subpart emitidos en `slice_pdf_lossless` / `update_pre_cta_manifest`, incluir el conjunto completo de claves compatibles con `dispatch.py` y `cta_merge.py`:
  `subpart_id`, `source_doc`, `slice_file`, `doc`, `file_index`, `path`, `slice_path`, `total_pages`, `page_range`, `page_map`.

### 2. `ingest.py` y `prepare.py`
- Fijar `MAX_DIRECT_PAGES = 25`.
- En `ingest_course()` (manteniendo kwargs existentes y añadiendo `force_direct: bool = False`):
  - Si `not force_direct` y (`total_pages > 25` o `len(pdf_files) > 1` o `len(sources) > 1`), promover `mode` (`"auto"` o `"direct"`) a `"mapreduce"`.
  - En modo `"mapreduce"`, subdividir físicamente con `slice_pdf_lossless` cualquier PDF con `num_pages > 25` hacia `work/slices/` y poblar `pre_cta_manifest.json` (`subparts`) con las claves compatibles completas; los PDFs `<= 25` páginas de un corpus multi-PDF entran como subparts individuales con las mismas claves compatibles.
- En `prepare.py` (modo `--append`): al escribir `delta_manifest.json` desde un curso base existente, incluir además de `existing_competency_ids` la clave `"existing_competencies"` con resúmenes de solo lectura: `[{"id": cid, "name": cname, "type": ctype, "prerequisites": prereqs, "distractor_names": [...]}]`.

### 3. `cta_merge.py` (Simetría 100% `1A <-> 2A` y `--append` en Stage 1)
- **`find_duplicate_candidates()`:** bajar `JACCARD_DUPLICATE_THRESHOLD = 0.30` (antes `0.60`), eliminar la restricción `type1 == type2` para detectar duplicados cruzados (`C-*` vs `Hab-*`), y cuando exista `delta_manifest.json` con `existing_competencies`, calcular también candidatos delta-vs-base (`>= 0.30`, marcados con `"against_base": True`).
- **Simetría absoluta en `merge_cta_parts()` (`Matiz 4a`):**
  - **ELIMINAR por completo cualquier escritura de `work/cta.json` y `work/cta.md` dentro de `merge_cta_parts()`**, sin importar si `len(part_files)` es `1` o `>= 2`.
  - Escribir siempre `work/cta_draft.json`, `work/cta_outline.json`, `work/duplicate_candidates.json`, `work/cta_order.json` e `id_map.json`.
  - Si existe `delta_manifest.json`, incluir las competencias base como entradas `read_only_base: True` en `cta_outline.json` para que `c2c_cta_harmonizer` las vea y pueda fusionar duplicados o enlazar prerrequisitos hacia IDs `[BASE]`.
- **Nuevo helper `prepare_harmonize_from_single_draft(work_dir: Path) -> dict`:**
  - Para flujos `direct` de 1 PDF corto cuando `--append` está activo (o si `run.py` requiere armonizar un draft único): toma el CTA compilado único (`work/cta.json` o `work/cta_draft.json`), lo guarda en `work/cta_draft.json` (removiendo `work/cta.json` temporalmente hasta que corra `apply_harmonize`), y genera `work/cta_outline.json` (incluyendo nodos `read_only_base: True` de `delta_manifest.json`) y `work/duplicate_candidates.json` (`>= 0.30`).
- **`apply_harmonize()`:**
  - Leer fusiones tanto desde `"duplicate_decisions"` (ítems con `decision == "merge"`, soportando `keep_id`/`drop_id` o `drop_ids` o `pair`+`keep` o `source_id`/`target_id`) como desde `"merges"` y `"merge"`.
  - Soportar absorción hacia un ID `[BASE]` existente en modo `--append`: si `keep_id` pertenece a `existing_competency_ids` (`[BASE]`) y `drop_id` es una competencia delta de `cta_draft.json`, descartar `drop_id` del delta y redirigir cualquier prerrequisito delta que apuntara a `drop_id` hacia `keep_id`.
  - **Eliminar el candado** `if sorted_pair not in allowed_candidates_set: raise ValueError(...)` para permitir al armonizador fusionar cualquier duplicado semántico de `cta_outline.json` aunque su Jaccard léxico sea `< 0.30`.
  - Soportar adición/actualización de prerrequisitos (`add_prerequisites`, `prerequisite_additions`, `prerequisite_updates`).
  - Invocar `check_prerequisites_dag(competencies, allowed_prereq_ids=existing_competency_ids)` y `validate_cta_rules(..., allowed_prereq_ids=existing_competency_ids)`, y escribir `work/cta.json` (y `work/cta.md`).

### 4. `check_cta.py` y `compile_cta.py` (Fail-Fast `[KATEX-PROSE-OVERFLOW]` Stage 1 + Conexidad DAG)
- **Fail-Fast `[KATEX-PROSE-OVERFLOW]` en Stage 1 (`Matiz 2`):**
  - Implementar `check_cta_prose_overflow(text: str, ctx: str) -> list[str]` que escanee bloques `\text{...}`, `\textrm{...}`, `\mathrm{...}` (con conteo balanceado de llaves) y rechace cualquier bloque cuyo contenido interno tenga `len > 45` caracteres con etiqueta `[KATEX-PROSE-OVERFLOW]`.
  - Integrarlo tanto en `validate_distractor_math()` como en `check_cta_katex()`, cubriendo `name`, `description`, `description_latex`, `source_examples` y **los 6 campos textuales de cada distractor** (`manifestation`, `remediation_hint`, `wrong_belief`, `correct_belief`, `omitted_step`, `trigger`), deduplicando mensajes de error para que `compile_cta.py` (`check_cta_part` y `validate_cta_rules`) falle de inmediato en Stage 1 con contexto/línea exacta.
- **Conexidad y ratio de raíces en `check_prerequisites_dag(competencies, allowed_prereq_ids=None)`:**
  - Para `N = len(competencies) >= 2`:
    - Exigir `connected_components == 1` sobre el grafo no dirigido. Cuando `allowed_prereq_ids` sea no vacío (`--append`), agregar un nodo ancla virtual `"__BASE_COURSE__"` conectado a toda competencia delta que referencie al menos un ID en `allowed_prereq_ids` (de modo que dos nodos delta enlazados a competencias base distintas queden conectados a través del curso base sin inflar islas).
    - Exigir `num_roots <= max(1, math.floor(0.20 * N))` donde una raíz es una competencia con `0` prerrequisitos totales (ni delta ni en `allowed_prereq_ids`).
- En `compile_cta.py`: asegurar que `validate_cta_rules()` reciba `allowed_prereq_ids=existing_comp_ids` cuando exista `delta_manifest.json`.

### 5. Actualización y Ampliación de las 7 Suites de Tests Exclusivas
Actualiza los fixtures de las 7 suites asignadas al nuevo contrato simétrico (`merge_cta_parts` -> `cta_draft.json` -> `apply_harmonize` -> `cta.json`, DAG conexo, promoción `mapreduce > 25` págs) y añade tests unitarios explícitos para:
- Promoción automática a `mapreduce` + `slice_pdf_lossless` (`k_parts = ceil(P/20)`) para PDFs `> 25` págs y multi-PDF.
- Simetría `merge_cta_parts` con 1 parte y N partes (jamás crea `work/cta.json` antes de `apply_harmonize`).
- `apply_harmonize` leyendo `"duplicate_decisions"` sin candado Jaccard, más absorción hacia nodos `[BASE]` y `prepare_harmonize_from_single_draft` en `--append`.
- Fail-fast `[KATEX-PROSE-OVERFLOW]` en `check_cta.py` / `compile_cta.py` sobre `\text{...} > 45` chars en cualquiera de los 6 campos de distractor o descripción.
- Rechazo de islas (`connected_components > 1`) y exceso de raíces (`root_ratio > 0.20`) en `check_prerequisites_dag`.

## Verificación
Ejecuta:
```powershell
& ".venv\Scripts\python.exe" -m pytest tests/test_cta_mapreduce.py tests/test_cta_merge_prereq_scoping.py tests/test_c2c_v321_comp1_cta.py tests/test_cta_healing.py tests/test_cta_sweetspot_and_autoheal.py tests/test_fast_ingest_and_cta_append.py tests/test_handouts.py -q
```
Escribe `BRIEFING.md` antes de editar, `handoff.md` al terminar y notifica a `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589` con `DONE:: Stream 1A Impl completado (<N> passed)`.
