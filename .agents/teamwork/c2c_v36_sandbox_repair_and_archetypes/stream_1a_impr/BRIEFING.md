# BRIEFING — Stream 1A (Fase 2: Mejorador `impr_1a`)

**Stream:** 1A — Aislamiento de Prerrequisitos por Subparte y Garantía Backward-Only en `merge_cta_parts`  
**Rol:** Mejorador (Fase 2)  
**Fecha:** 2026-10-25  

---

## 1. Diagnóstico del Estado Recibido (Handoff Implementador)
El implementador de Stream 1A completó satisfactoriamente la Fase 1:
- Se implementó el etiquetado `_part_key` y el ordenamiento topológico intra-parte estable mediante min-heap con algoritmo de Kahn.
- Se implementó `comp_id_map_by_part: Dict[str, Dict[str, str]]` y se preservó retrocompatibilidad plana en `comp_id_map`.
- Se implementó la reescritura de prerrequisitos con resolución de ámbito (prefijo explícito -> scope local de subparte -> fallback global).
- Se implementó la garantía estricta backward-only (`comp_pos[p] < idx`).
- 33 tests pasando en `tests/test_cta_merge_prereq_scoping.py`, `tests/test_cta_sweetspot_and_autoheal.py` y `tests/test_cta_mapreduce.py`.

---

## 2. Casos Borde Identificados para Endurecimiento (Hardening)

1. **Ciclos intra-parte accidentales (`A <-> B`):**
   - Si dos competencias de la misma subparte declaran dependencias mutuas circulares (o ciclos complejos de longitud $\ge 2$), el algoritmo de Kahn no puede desencolar ningún nodo del ciclo en `ready` (todos quedan con `in_degree > 0`).
   - El fallback actual agrega los nodos no visitados en su orden original, pero debemos garantizar que la ruptura del ciclo sea completamente determinista (preservando el orden canónico pre-determinado por `_sort_key`), que ninguna competencia se descarte, y que el filtro backward-only subsiguiente elimine con precisión la arista dirigida hacia adelante resultante. Esto asegura 0 errores en `check_prerequisites_dag`.

2. **Modo Incremental (`--append` / `delta_manifest.json`):**
   - En el handoff actual, si una subparte `part_01` referencia un ID del curso base preexistente (definido en `delta_info["existing_competency_ids"]`), pero `part_02` genera una nueva competencia con el mismo ID local (ej. `H-01`), el fallback global `comp_id_map.get(p, p)` corría el riesgo de mapear el prerrequisito del curso base a la nueva competencia de `part_02` (`H-02`), transformándolo erróneamente en un forward prerequisite que luego era descartado.
   - Solución: Intercalar explícitamente la resolución contra `existing_comp_ids` antes del fallback global a otras subpartes, admitir prefijos explícitos de curso base (`existing:`, `base:`, `course:`, `delta:`), y garantizar en el paso backward-only que los IDs de `existing_comp_ids` no se descarten jamás.

3. **Limpieza estricta de llaves internas temporales:**
   - Garantizar que ni `_part_key` ni `_sort_key` queden en ningún objeto persistido en `cta_draft.json`, `cta_outline.json`, `cta.json` ni en el diccionario de retorno.

---

## 3. Plan de Pruebas Adversarias Adicionales
En `tests/test_cta_merge_prereq_scoping.py`:
1. `test_intra_part_cycle_fallback_deterministic_dag`:
   - Dos competencias con ciclo mutuo `C-01 <-> C-02` dentro de `part_01`.
   - Verificar que no hay loop infinito, se preservan ambas competencias, se rompe el ciclo determinísticamente y `check_prerequisites_dag` pasa con 0 errores.
2. `test_incremental_append_preserves_base_course_prereqs`:
   - Modo `--append` con `delta` (`existing_competency_ids: ["C-01", "H-01"]`, `next_numbers_by_prefix: {"C": 2, "H": 2, "Hab": 1}`).
   - `part_01` y `part_02` con IDs locales reutilizados y referencias tanto al curso base (`H-01`, `base:C-01`) como a competencias locales y cruzadas.
   - Verificar que los prerrequisitos base se conservan intactos y no colisionan ni se descartan como forward prereqs.
3. `test_asymptotic_statistics_v6_scale_simulation`:
   - 25 competencias completas (12 en `part_01`, 13 en `part_02`) con distractores conformes CTA-D1/D2, evidencia válida y numeración idéntica desde `C-01, H-01, Hab-01`.
   - Validar 0 forward prerequisites, 0 violaciones DAG y `validate_cta_rules` == `True`.
   - Validar ausencia total de `_part_key` y `_sort_key` en `cta_draft.json` y `cta.json`.

---

## 4. Frontera Exclusiva de Escritura
- Modificaciones limitadas estrictamente a:
  1. `.agents/skills/content-to-course/cta_merge.py`
  2. `tests/test_cta_merge_prereq_scoping.py`
  3. Gobernanza: `stream_1a_impr/BRIEFING.md` y `stream_1a_impr/handoff.md`.
