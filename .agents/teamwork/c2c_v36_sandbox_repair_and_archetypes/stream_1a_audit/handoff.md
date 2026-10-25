# Handoff — Stream 1A (Fase 3: Auditor Forense `audit_1a`)

**Stream:** 1A — Aislamiento de Prerrequisitos por Subparte y Garantía Backward-Only en `merge_cta_parts`  
**Rol:** Auditor Forense (Fase 3)  
**Fecha/Hora:** 2026-10-25  
**Dictamen:** **PASS (APROBADO)**  

---

## 1. Resumen de la Auditoría Forense

Se completó la auditoría forense independiente sobre los cambios implementados y mejorados en:
1. `.agents/skills/content-to-course/cta_merge.py` (función `merge_cta_parts`)
2. `tests/test_cta_merge_prereq_scoping.py` (suite de 8 pruebas de integración y adversarias)

Se verificó el cumplimiento estricto del protocolo:
- **Restricción Read-Only:** Cumplida al 100%. Solo se modificaron los archivos de gobernanza en `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1a_audit/` (`BRIEFING.md` y `handoff.md`).
- **Aislamiento por Subparte:** Verificado a nivel algorítmico y en disco.
- **Garantía Backward-Only:** Verificada matemáticamente y empíricamente con 0 violaciones DAG.
- **Ausencia de Regresiones:** Validada contra las suites preexistentes `test_cta_sweetspot_and_autoheal.py` y `test_cta_mapreduce.py`.

---

## 2. Inspección Detallada de Código de Producción (`cta_merge.py`)

1. **Aislamiento de Scope por Subparte (`comp_id_map_by_part`):**
   - Cada subparte recibe un tag determinista `_part_key = stem` y `_sort_key = (sp_idx, f_idx, page_int, orig_idx)` (L830-831).
   - El mapeo canónico se aísla por subparte en `comp_id_map_by_part[part_key][old_cid] = new_cid` y alias normalizado `part_XX` (L977-982).
   - Se mantiene `comp_id_map` plano para retrocompatibilidad y mapeos calificados `f"{part_key}:{old_cid}"`.
   - Se expone `"by_part": comp_id_map_by_part` en `id_map_payload` / `id_map.json` (L1074).

2. **Ordenamiento Topológico Intra-Parte Estable:**
   - Previo a la reasignación secuencial de IDs canónicos, las competencias de cada subparte se ordenan de acuerdo a sus dependencias locales intra-parte usando el algoritmo de Kahn con min-heap sobre el índice original (L843-899).
   - Estabilidad determinista: nodos independientes preservan rigurosamente el orden de `_sort_key`.
   - Si una competencia en página 2 depende de una en página 3 de la misma parte, la de página 3 se posiciona antes, logrando que al renumerar reciba un ID anterior (`C-01`) y la dependiente el posterior (`C-02`).

3. **Degradación Limpia ante Ciclos Accidentales:**
   - Si se introducen dependencias circulares locales (`A <-> B`), el fallback no entra en bucle infinito y garantiza la preservación del 100% de los nodos (`len(visited_indices) == len(part_comps)`) siguiendo el orden determinista original (L900-909).
   - El filtro backward-only posterior (`comp_pos[prereq] < idx`) purga de forma exacta la arista hacia adelante residual (L1036-1060), convirtiendo el grafo resultante en un DAG estrictamente acíclico y garantizando que `check_prerequisites_dag` pase con 0 errores.

4. **Soporte Incremental (`--append` / `delta_manifest.json`):**
   - Se consolida de forma exhaustiva `existing_comp_ids` desde `delta`, `existing_course`, `delta_manifest`, archivo `delta_manifest.json` y `existing_competency_ids` (L919-940).
   - Se soporta resolución de prefijos explícitos de curso base (`"existing:"`, `"base:"`, `"course:"`, `"delta:"`).
   - Se previene que un prerrequisito a una competencia de curso base colisione o sea sobreescrito por el mapeo de otra subparte que reutilice el mismo ID local (L1026-1027).
   - Se preservan intactos los prerrequisitos hacia competencias del curso base (L1052-1059).

5. **Saneamiento Total de Llaves Privadas Temporales:**
   - En L1062-1065 se ejecutan `comp.pop("_part_key", None)` y `comp.pop("_sort_key", None)` sobre la totalidad de las competencias antes de generar cualquier JSON (`cta_draft.json`, `cta.json`, `cta_outline.json`). Ningún residuo interno se fuga a disco ni a payloads públicos.

---

## 3. Inspección Forense de la Suite de Pruebas (`test_cta_merge_prereq_scoping.py`)

Se auditó línea por línea el archivo `tests/test_cta_merge_prereq_scoping.py` (639 líneas, 8 tests):
- **Cero aserciones vacías o tautológicas:** Cada test realiza aserciones puntuales sobre los IDs reasignados, los arreglos de prerrequisitos, las posiciones relativas y las estructuras JSON en disco.
- **Cobertura de Casos Extremos y Adversarios:**
  - `test_two_parts_identical_local_ids_scoping`: Colisión de IDs idénticos `C-01, H-01, Hab-01` en múltiples partes. Verifica que `part_01` jamás apunte a `part_02` y viceversa.
  - `test_explicit_cross_part_prerequisite_prefix`: Mapeo explícito `part_01:C-01` inter-parte.
  - `test_intra_part_topological_sort_inverts_order`: Inversión de orden previa a la reasignación de IDs.
  - `test_strict_backward_only_guarantee_drops_unresolvable_forward_prereqs`: Purga de aristas hacia adelante imposibles de resolver.
  - `test_full_dag_validation_with_check_prerequisites_dag`: 3 partes complejas con validación formal DAG.
  - `test_intra_part_cycle_fallback_deterministic_dag`: Ciclo mutuo `A <-> B`, no divergencia, preservación de nodos, ausencia de fugas de `_part_key`/`_sort_key`.
  - `test_incremental_append_preserves_base_course_prereqs`: Modo `--append` con curso base y validación cruzada con `validate_cta_rules`.
  - `test_asymptotic_statistics_v6_scale_simulation`: Simulación realista del caso de producción a escala (25 competencias: 8 facts, 9 concepts, 8 skills) validado bajo `check_prerequisites_dag` y `validate_cta_rules`.

---

## 4. Ejecución Independiente de Tests

Comando ejecutado:
```powershell
.venv\Scripts\python.exe -m pytest tests/test_cta_merge_prereq_scoping.py tests/test_cta_sweetspot_and_autoheal.py tests/test_cta_mapreduce.py -q
```

Resultado obtenido:
```
....................................                                     [100%]
36 passed in 4.79s
```

Estado de salida: `Exit code: 0`. Cero fallas, cero advertencias no controladas, cero regresiones.

---

## 5. Dictamen Final

**PASS:: Stream 1A Auditor aprobado**
El aislamiento de prerrequisitos por subparte, el ordenamiento topológico intra-parte y la garantía 100% backward-only en `merge_cta_parts` cumplen con los más altos estándares de calidad, resiliencia y estabilidad del sistema Top's Academy.
