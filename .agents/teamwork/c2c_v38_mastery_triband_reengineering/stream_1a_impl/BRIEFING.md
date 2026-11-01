# BRIEFING Pre-Flight — Stream 1A: Ingest, Partition, CTA Merge & Rules Reengineering

- **Agent:** `c2c38_implementer` (Flash Triad Phase 1)
- **Target Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1a_impl`
- **Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`
- **Date:** 2026-10-31

---

## 1. Alcance y Frontera Exclusiva de Escritura
Se ha verificado la lista exclusiva de 15 archivos:
1. `partition_corpus.py`
2. `ingest.py`
3. `prepare.py`
4. `compile_cta.py`
5. `cta_merge.py`
6. `check_cta.py`
7. `tests/test_cta_mapreduce.py`
8. `tests/test_cta_merge_prereq_scoping.py`
9. `tests/test_c2c_v321_comp1_cta.py`
10. `tests/test_cta_healing.py`
11. `tests/test_cta_sweetspot_and_autoheal.py`
12. `tests/test_fast_ingest_and_cta_append.py`
13. `tests/test_handouts.py`
14. `stream_1a_impl/BRIEFING.md`
15. `stream_1a_impl/handoff.md`

Ningún archivo fuera de esta frontera será tocado. No se crearán scripts temporales.

---

## 2. Inspección de Archivos de Producción y Líneas Exactas de Intervención

### A. `partition_corpus.py` (573 líneas)
- **Líneas 196-207 (`slice_pdf_lossless`):**
  - Actualmente limita `k_parts`:
    ```python
    if k_parts is None:
        if total_pages <= 4: k_parts = 2
        elif total_pages <= 12: k_parts = 3
        else: k_parts = 4
    k_parts = max(2, min(4, k_parts))
    ```
  - Contrato nuevo: cuando `total_pages > 25`, si `k_parts is None`, escalar `k_parts = max(2, math.ceil(total_pages / 20))`, eliminando el tope `min(4, ...)`. Si `total_pages <= 25`, mantener subdivisión suave en 2..4 o respetar `k_parts` explícito.
- **Líneas 249-267 & 477-488 (`slice_pdf_lossless` & `update_pre_cta_manifest`):**
  - Ambos diccionarios de manifest/subpart deben contener el conjunto completo de claves compatibles con `dispatch.py` y `cta_merge.py`:
    `subpart_id`, `source_doc`, `slice_file`, `doc`, `file_index`, `path`, `slice_path`, `total_pages`, `page_range`, `page_map`.

### B. `ingest.py` (408 líneas)
- **Constantes:** Agregar `MAX_DIRECT_PAGES = 25`.
- **Líneas 201-246 (`ingest_course`):**
  - Añadir kwarg `force_direct: bool = False`.
  - Promover `mode` a `"mapreduce"` si `not force_direct` y (`total_pages > 25` o `len(target_files) > 1` o múltiples fuentes).
  - En modo `"mapreduce"`, para cada PDF con `num_pages > 25`, subdividir físicamente usando `slice_pdf_lossless(fpath, parts_dir, k_parts=None)` poblando `subparts_manifest` con todas las claves compatibles. Si `num_pages <= 25` en corpus multi-PDF, entra como subpart individual con todas las claves compatibles.

### C. `prepare.py` (371 líneas)
- **Líneas 210-305 (`prepare_course` en modo `--append`):**
  - Al generar `delta_info` y guardarlo en `delta_manifest.json` y `pre_cta_manifest.json`, incluir además de `existing_competency_ids`:
    `existing_competencies`: resúmenes de solo lectura con `id`, `name`, `type`, `prerequisites`, `distractor_names`.

### D. `cta_merge.py` (1677 líneas)
- **Línea 44:** Bajar `JACCARD_DUPLICATE_THRESHOLD = 0.30` (antes `0.60`).
- **Líneas 606-672 (`find_duplicate_candidates`):**
  - Eliminar restricción `type1 != type2` (permitir comparar Fact/Concept vs Skill para detectar solapes conceptuales/habilidades).
  - Si existe `delta_manifest.json` con `existing_competencies`, evaluar también duplicados delta-vs-base (`>= 0.30`, marcados con `"against_base": True`).
- **Líneas 1132-1140 (`merge_cta_parts`):**
  - Matiz 4a: ELIMINAR la escritura de `work/cta.json` y `work/cta.md` dentro de `merge_cta_parts()`. Solo escribir `cta_draft.json`, `cta_outline.json`, `duplicate_candidates.json`, `cta_order.json`, `id_map.json`.
  - En `cta_outline.json`, si existe `delta_manifest.json`, incluir las competencias base con `read_only_base: True`.
- **Nuevo helper:** `prepare_harmonize_from_single_draft(work_dir: Path) -> dict`:
  - Lee `work/cta.json` o `work/cta_draft.json`, asegura `work/cta_draft.json`, remueve `work/cta.json` hasta `apply_harmonize`, genera `cta_outline.json` y `duplicate_candidates.json`.
- **Líneas 1159-1528 (`apply_harmonize`):**
  - Soportar fusiones desde `"duplicate_decisions"`, `"merges"`, `"merge"`. Formatos `keep_id`/`drop_id`, `drop_ids`, `pair`+`keep`, `source_id`/`target_id`.
  - Absorción hacia ID base (`[BASE]`): si `keep_id` es base y `drop_id` es delta, descartar `drop_id` del delta y redirigir prerrequisitos delta hacia `keep_id`.
  - Eliminar el candado `sorted_pair not in allowed_candidates_set` para permitir fusiones semánticas dictadas por el armonizador.
  - Soportar `add_prerequisites`, `prerequisite_additions`, `prerequisite_updates`.
  - Validar DAG conexo y escribir `work/cta.json` y `work/cta.md`.

### E. `check_cta.py` y `compile_cta.py`
- **Fail-Fast `[KATEX-PROSE-OVERFLOW]`:**
  - Implementar `check_cta_prose_overflow(text: str, ctx: str) -> list[str]` para escanear `\text{...}`, `\textrm{...}`, `\mathrm{...}` con balance de llaves. Rechazar si `len(interior) > 45` con tag `[KATEX-PROSE-OVERFLOW]`.
  - Integrar en `validate_distractor_math()` y `check_cta_katex()` cubriendo los 6 campos textuales de distractores, `name`, `description`, `description_latex` y `source_examples`.
- **Conexidad y Ratio de Raíces en `check_prerequisites_dag`:**
  - Para `N >= 2`:
    - Grafo no dirigido conexo (`connected_components == 1`). Si `allowed_prereq_ids` no es vacío, nodo ancla virtual `"__BASE_COURSE__"` conectado a nodos delta que referencien `allowed_prereq_ids`.
    - `num_roots <= max(1, math.floor(0.20 * N))` donde raíz es in-degree 0 (sin prerrequisitos totales).
- **En `compile_cta.py`:**
  - Asegurar que `validate_cta_rules` reciba `allowed_prereq_ids=existing_comp_ids` cuando exista `delta_manifest.json`.

---

## 3. Riesgos Detectados y Mitigaciones
1. **Regla Zero-Domain:** Prohibidas subcadenas `edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`.
   - *Mitigación:* Todos los comentarios, docstrings y strings en archivos `.py` se redactarán en inglés limpio, vigilando palabras en español como `puede`, `quedó`, `hereda`, `regresión`.
2. **Sincronización de Tests:**
   - En `test_cta_mapreduce.py`, `test_cta_merge_prereq_scoping.py`, etc., los tests que invocaban `merge_cta_parts` asumían que generaba `cta.json`. Al cambiar al contrato simétrico, `merge_cta_parts` genera `cta_draft.json`, y luego `apply_harmonize` genera `cta.json`.
   - Las pruebas deben actualizarse para llamar a `apply_harmonize` cuando esperen `cta.json` o verificar que `cta_draft.json` se creó y `cta.json` no existe hasta la armonización.
   - Las cadenas de prerrequisitos en fixtures deben ser conexas (`connected_components == 1`) y con raíces `<= 20%`.
3. **Compatibilidad Windows / KaTeX:**
   - Las guardias de KaTeX (`[KATEX-PROSE-OVERFLOW]`) no deben colisionar con regexes de saltos de línea Windows (`\r\n`).

Pre-Flight completado satisfactoriamente. Iniciando implementación.
