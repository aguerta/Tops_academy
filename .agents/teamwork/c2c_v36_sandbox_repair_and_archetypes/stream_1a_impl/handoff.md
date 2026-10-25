# Handoff — Stream 1A (Fase 1: Implementador `impl_1a`)

**Stream:** 1A — Aislamiento de Prerrequisitos por Subparte y Garantía Backward-Only en `merge_cta_parts`
**Fecha/Hora:** 2026-10-25
**Estado:** COMPLETADO CON ÉXITO (33 tests en verde)

---

## 1. Resumen de Implementación

### A. Modificaciones en `.agents/skills/content-to-course/cta_merge.py`
1. **Etiquetado de Subparte (`_part_key`):**
   - En el bucle de carga de `part_files`, se asigna `c["_part_key"] = stem` antes de agregar la competencia a `combined_competencies`.
2. **Ordenamiento Topológico Estable Intra-Parte:**
   - Previo a la reasignación secuencial de IDs canónicos, las competencias de cada subparte se ordenan de acuerdo a sus dependencias locales intra-parte.
   - Implementado mediante algoritmo de Kahn con min-heap sobre el índice original (`initial_idx`), garantizando estabilidad determinista sin alterar el orden cuando no hay dependencias directas o adelantadas.
   - Si una competencia en página 2 depende de una en página 3 de la misma parte, la de página 3 se posiciona antes, logrando que al renumerar reciba un ID anterior (`C-01`) y la dependiente reciba el posterior (`C-02`).
3. **Mapeo de IDs Aislado por Subparte (`comp_id_map_by_part`):**
   - Se mantiene `comp_id_map_by_part: Dict[str, Dict[str, str]]` indexando `[part_key][old_cid] = new_cid` (y alias normalizados `part_XX`).
   - Se mantiene el diccionario plano `comp_id_map` con mapeos calificados `f"{part_key}:{old_cid}"` y primer mapeo sin calificar `comp_id_map.setdefault(old_cid, new_cid)` para preservar 100% retrocompatibilidad con tests existentes.
   - Se expone `"by_part": comp_id_map_by_part` en `id_map_payload` / `id_map.json`.
4. **Reescritura de Prerrequisitos con Scope y Garantía Estricta Backward-Only:**
   - La resolución de prerrequisitos evalúa en orden:
     1. Prefijo calificado explícito (`"part_01:C-01"`).
     2. Scope local de la subparte actual (`comp_id_map_by_part[part_key]`).
     3. Fallback global en `comp_id_map`.
   - Posterior al mapeo, se valida `comp_pos = {c["id"]: idx for idx, c in enumerate(combined_competencies)}`.
   - Se eliminan referencias circulares (`p == comp["id"]`) y cualquier prerrequisito donde `comp_pos[p] >= idx` (forward prerequisites), asegurando que el 100% de las dependencias sean estrictamente hacia atrás (`comp_pos[p] < idx`). Prerrequisitos externos de cursos base (delta/append) son respetados y preservados.

---

## 2. Pruebas Creadas y Ejecutadas

### Archivo de Pruebas Creado: `tests/test_cta_merge_prereq_scoping.py`
1. `test_two_parts_identical_local_ids_scoping`: Dos partes con IDs locales idénticos (`C-01`, `H-01`, `Hab-01`). Confirma que los prerrequisitos de `part_01` apuntan a `part_01` y jamás son sobreescritos por `part_02`.
2. `test_explicit_cross_part_prerequisite_prefix`: Prefijos cruzados explícitos (`part_01:C-01` referenciado desde `part_02`) se resuelven correctamente.
3. `test_intra_part_topological_sort_inverts_order`: Competencia en pág 2 que depende de pág 3 es reordenada establemente antes de asignar IDs, preservando la monotonicidad y eliminando referencias hacia adelante.
4. `test_strict_backward_only_guarantee_drops_unresolvable_forward_prereqs`: Referencias hacia adelante no resolubles o ciclos inter-parte son eliminados garantizando 0 violaciones DAG.
5. `test_full_dag_validation_with_check_prerequisites_dag`: Escenario complejo multi-parte valida con 0 errores bajo `check_prerequisites_dag`.

### Resultado de Tests:
```
tests/test_cta_merge_prereq_scoping.py ..... [100%] (5 passed)
tests/test_cta_sweetspot_and_autoheal.py .......... [100%] (10 passed)
tests/test_cta_mapreduce.py .................. [100%] (18 passed)
Total: 33 passed in 4.76s
```

---

## 3. Verificación de Fronteras Exclusivas de Escritura
- Archivos de producción modificados:
  - `.agents/skills/content-to-course/cta_merge.py` (Únicamente en `merge_cta_parts` e imports)
  - `tests/test_cta_merge_prereq_scoping.py` (Creado)
- Archivos de gobernanza:
  - `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1a_impl/BRIEFING.md`
  - `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1a_impl/handoff.md`
- Ningún otro archivo fuera de la frontera fue modificado.
