# Pre-Flight Sanity Check — Stream 1A (Implementador `impl_1a`)

**Fecha/Hora:** 2026-10-25
**Objetivo:** Aislamiento de mapeo `comp_id_map` por subparte (`part_key`), ordenamiento topológico intra-parte y garantía estricta backward-only en `merge_cta_parts`.

---

## 1. Inspección de Código Real y Firmas

### Archivo `.agents/skills/content-to-course/cta_merge.py`
- **Firma de la función:**
  `def merge_cta_parts(work_dir: Union[str, Path]) -> Dict[str, Any]:` (Línea 668)
- **Carga de subpartes y armado de `combined_competencies`:**
  - Líneas 729–831 iteran sobre `part_files`.
  - Línea 829 asigna `c["_sort_key"] = (sp_idx, f_idx, page_int, orig_idx)` pero actualmente **no** asigna `c["_part_key"]`.
  - Línea 836 ejecuta `combined_competencies.sort(key=lambda c: c["_sort_key"])` y luego elimina `_sort_key`.
- **Renumeración y diccionarios de mapeo actuales:**
  - Línea 857 define `comp_id_map: Dict[str, str] = {}` plano.
  - Líneas 860–892 iteran sobre `combined_competencies`. Si `old_cid` se repite entre subpartes (`part_01`, `part_02`), la última subparte sobreescribe la entrada en `comp_id_map`.
- **Reescritura de prerrequisitos:**
  - Líneas 894–902 reescriben prerrequisitos con `comp_id_map.get(p, p)`. Al estar sobrescrito por `part_02`, genera referencias hacia adelante (Forward Prerequisites). Además no valida `comp_pos[prereq] < comp_pos[comp]`.
- **Generación de `id_map.json`:**
  - Líneas 907–910 crean `id_map_payload = {"competencies": comp_id_map, "distractors": dist_id_map}`. Requiere agregar `"by_part": comp_id_map_by_part`.

---

## 2. Inspección de Pruebas Existentes
- `tests/test_cta_sweetspot_and_autoheal.py` (10 tests pasando en 0.34s).
- `tests/test_cta_mapreduce.py` (18 tests pasando en 5.23s).
- `tests/test_fast_ingest_and_cta_append.py::TestContinuousIdsAppendAndHarmonize::test_merge_cta_parts_append_continuous_ids` verifica el modo append con `delta_manifest.json` y `pre_cta_manifest.json`.

---

## 3. Plan de Cambios Quirúrgicos en `cta_merge.py`
1. **Etiquetado de subparte:**
   En el bucle de carga de `part_files` (línea ~829), registrar `c["_part_key"] = stem`.
2. **Ordenamiento topológico intra-parte antes de reasignar IDs:**
   Tras ordenar `combined_competencies` por `_sort_key`, agrupar competencias por `_part_key`. Para cada subparte, construir el grafo de dependencias intra-parte y aplicar ordenamiento topológico estable (Kahn con min-heap sobre índice original). Así, si una competencia en pág 2 depende de otra en pág 3 de la misma parte, la de pág 3 se moverá antes que la de pág 2 sin alterar el orden relativo de los demás elementos ni generar prerrequisitos hacia adelante.
3. **Mapeo de IDs scoped (`comp_id_map_by_part`) y plano retrocompatible:**
   - `comp_id_map_by_part: Dict[str, Dict[str, str]] = {}`
   - Registrar `comp_id_map_by_part[part_key][old_cid] = new_cid`. Si `part_key` tiene alias como `part_01`, indexar también bajo el alias.
   - En `comp_id_map` plano, registrar `comp_id_map[f"{part_key}:{old_cid}"] = new_cid` y `comp_id_map.setdefault(old_cid, new_cid)` para preservar el primer mapeo canónico y compatibilidad de una sola parte.
   - Incluir `"by_part": comp_id_map_by_part` en `id_map_payload`.
4. **Reescritura y Garantía Estricta Backward-Only:**
   - Mapear cada prerrequisito `p`:
     - Si `":" in p`: buscar en `comp_id_map`.
     - Si `part_key in comp_id_map_by_part` y `p in comp_id_map_by_part[part_key]`: usar `comp_id_map_by_part[part_key][p]`.
     - De lo contrario: `comp_id_map.get(p, p)`.
   - Limpiar `_part_key`.
   - Calcular `comp_pos = {c["id"]: idx for idx, c in enumerate(combined_competencies)}` y recolectar `existing_comp_ids` si `delta_info` existe.
   - Filtrar prerrequisitos: todo prerrequisito `mapped` que esté en `comp_pos` DEBE cumplir `comp_pos[mapped] < idx`. Si `comp_pos[mapped] >= idx`, se descarta como forward reference. Prerrequisitos externos de cursos base (`existing_comp_ids`) se preservan.

---

## 4. Plan de Pruebas en `tests/test_cta_merge_prereq_scoping.py`
- Test 1: Dos partes (`part_01` y `part_02`) con IDs locales coincidentes (`C-01`, `H-01`, `Hab-01`). Comprobar que `part_01` mantiene sus dependencias en `part_01` y no son reescritas a `part_02`.
- Test 2: Cero competencias en el `cta.json` final tienen `comp_pos[prereq] >= comp_pos[comp]`.
- Test 3: Dependencia intra-parte inversa (pág 2 depende de pág 3): verificar ordenamiento topológico estable que produce secuencia ordenada de IDs sin forward prereqs y con monotonicidad estricta.
- Test 4: Prefijo explícito inter-parte (`part_01:C-01` desde `part_02`) se resuelve correctamente al ID canónico de `part_01`.

---

## 5. Diagnóstico de Bloqueos
No hay bloqueos (`BLOCKER::`). El alcance está perfectamente delimitado dentro de `cta_merge.py` y `tests/test_cta_merge_prereq_scoping.py`.
