# DISPATCH — Stream 1A (Fase 1: Implementador `impl_1a`)

## 1. Rol y Frontera Exclusiva de Escritura (`Exclusive Write Boundaries`)
Eres el **Implementador del Stream 1A** bajo `/flash-triad-orchestrator`.
- **Carpeta de Gobernanza:** `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1a_impl/`
- **Archivos de Producción Permitidos (ÚNICOS que puedes modificar):**
  1. `.agents/skills/content-to-course/cta_merge.py`
  2. `tests/test_cta_merge_prereq_scoping.py`
- **Artefactos de Gobernanza Permitidos:**
  - `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1a_impl/BRIEFING.md`
  - `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1a_impl/handoff.md`
- **PROHIBIDO** editar cualquier otro archivo del repositorio. Nunca pases `ArtifactMetadata` a `write_file` o `edit_file`.

## 2. Paso 0 Obligatorio (*Pre-Flight Sanity Check*)
Antes de realizar cualquier edición:
1. Lee `.agents/skills/content-to-course/cta_merge.py` (líneas 668–988) y `tests/test_cta_sweetspot_and_autoheal.py` (para conocer las convenciones de pruebas sobre `cta_merge.py`).
2. Escribe `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1a_impl/BRIEFING.md` confirmando líneas y firmas reales. Si detectas un bloqueo fuera de tu frontera, detén ediciones y envía `BLOCKER:: <archivo:línea> | <causa> | <opciones>` al Orquestador (`d603756a-7e58-4466-b883-cbc391586154`).

## 3. Especificación Técnica de Implementación

### A. Aislar el Mapeo `comp_id_map` por Subparte (`part_key`) en `merge_cta_parts` (`cta_merge.py:729-911`)
1. **Problema Raíz Detectado:**
   - Cuando `part_01.json` y `part_02.json` son generados en paralelo por los CTA Architects, ambos numeran sus competencias locales empezando en `C-01`, `H-01`, `Hab-01`.
   - En `merge_cta_parts` (`cta_merge.py:857-902`), se utilizaba un único diccionario plano `comp_id_map: Dict[str, str] = {}`. Cuando el bucle procesaba `part_02`, los IDs locales `"C-01"`, `"H-01"`, `"Hab-01"` de `part_02` (renumerados a `"C-06"`, `"H-04"`, `"Hab-05"`) **sobrescribían** las entradas de `part_01` en `comp_id_map`.
   - Luego, al reescribir `prerequisites` en las líneas 894–901 (`mapped = comp_id_map.get(p, p)`), los prerrequisitos locales de `part_01` (que apuntaban a `"C-01"`, `"H-01"`, `"Hab-01"` de `part_01`) eran reemplazados por `"C-06"`, `"H-04"`, `"Hab-05"` de `part_02`, creando **prerrequisitos hacia adelante (`Forward Prerequisites`)** inválidos!
2. **Solución Exacta en `merge_cta_parts`:**
   - Al cargar cada competencia `c` de `p_file` (alrededor de línea 829), guarda temporalmente `c["_part_key"] = stem` (además de `c["_sort_key"] = (sp_idx, f_idx, page_int, orig_idx)`).
   - **Ordenamiento Topológico Estable Intra-Parte (antes de renumerar IDs en línea 860):**
     - Después de ordenar `combined_competencies.sort(key=lambda c: c["_sort_key"])`, dentro de cada subparte (`_part_key`), si una competencia `A` declara en `prerequisites` el `id` original de otra competencia `B` de la **misma subparte** (`_part_key`) que quedó posicionada después de `A` (por ejemplo, por diferencia de página), aplica un ordenamiento topológico estable por subparte (Kahn / inserción estable respetando el orden `_sort_key` como desempate) para que `B` aparezca antes que `A` dentro de esa subparte antes de asignar los nuevos IDs secuenciales `H-01..`, `C-01..`, `Hab-01..`.
   - **Mapeo de IDs con Scope por Subparte (`comp_id_map_by_part`):**
     - Mantén `comp_id_map_by_part: Dict[str, Dict[str, str]] = {}` (donde `comp_id_map_by_part.setdefault(part_key, {})[old_cid] = new_cid`) además del diccionario plano `comp_id_map: Dict[str, str]` (en `comp_id_map`, guarda `comp_id_map[f"{part_key}:{old_cid}"] = new_cid` y, para compatibilidad hacia atrás con tests de una sola parte o IDs disjuntos, guarda `comp_id_map[old_cid] = new_cid` si `old_cid` aún no estaba en `comp_id_map`, o mantén el primer mapeo canónico y expón `"by_part": comp_id_map_by_part` dentro de `id_map_payload`). Wait: verifica qué esperan los tests existentes en `tests/test_cta_merge.py` sobre `id_map.json`! (Lee `tests/test_cta_merge.py` en tu Paso 0 para mantener 100% compatibilidad con `id_map_payload`).
   - **Reescritura de `prerequisites` con Garantía Estricta `Backward-Only` (`pos[prereq] < pos[comp]`):**
     - Para cada `comp` en `combined_competencies` (con `part_key = comp.pop("_part_key", "")`), resuelve cada prerrequisito `p`:
       1. Si `p` tiene prefijo explícito de parte (ej. `"part_01:C-01"`), búscalo en `comp_id_map`.
       2. Si `p` existe en `comp_id_map_by_part.get(part_key, {})`, usa `comp_id_map_by_part[part_key][p]`.
       3. En caso contrario, usa `comp_id_map.get(p, p)`.
     - Una vez mapeados todos los IDs, calcula `comp_pos = {c["id"]: idx for idx, c in enumerate(combined_competencies)}` (y respeta `existing_comp_ids` si estamos en modo delta/append).
     - Filtra `new_prereqs` para garantizar que todo prerrequisito `mapped` que pertenezca a `comp_pos` cumpla estrictamente `comp_pos[mapped] < idx` (eliminando cualquier referencia hacia adelante o auto-referencia residual).

## 4. Verificación y Entrega
1. Crea `tests/test_cta_merge_prereq_scoping.py` con pruebas exhaustivas que verifiquen:
   - Dos partes (`part_01.json` y `part_02.json`) que usan ambas IDs locales `C-01`, `H-01`, `Hab-01`: al ejecutar `merge_cta_parts`, los prerrequisitos de `part_01` apuntan a las competencias de `part_01` (`C-01`, `H-01`) y **jamás** son sobrescritos por `C-06` o `H-04` de `part_02`.
   - Que `0` competencias en el `cta.json` resultante tienen prerrequisitos hacia adelante (`comp_pos[prereq] < comp_pos[comp]` para el 100% de las competencias).
   - Que si dentro de una misma parte una competencia en página 2 depende de una en página 3, el ordenamiento topológico estable intra-parte las ordena sin producir prerrequisitos hacia adelante ni romper la monotonicidad de IDs (`H-01, H-02...`, `C-01, C-02...`).
2. Ejecuta `.venv\Scripts\python.exe -m pytest tests/test_cta_merge_prereq_scoping.py tests/test_cta_merge.py tests/test_cta_sweetspot_and_autoheal.py -q`.
3. Escribe `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1a_impl/handoff.md` y envía `DONE:: Stream 1A Implementer completado` a `d603756a-7e58-4466-b883-cbc391586154`.
