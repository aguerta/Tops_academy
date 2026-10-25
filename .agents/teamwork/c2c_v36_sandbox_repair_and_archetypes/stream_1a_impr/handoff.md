# Handoff — Stream 1A (Fase 2: Mejorador `impr_1a`)

**Stream:** 1A — Aislamiento de Prerrequisitos por Subparte y Garantía Backward-Only en `merge_cta_parts`  
**Rol:** Mejorador (Fase 2)  
**Fecha/Hora:** 2026-10-25  
**Estado:** COMPLETADO CON ÉXITO (36 tests en verde, 100% PASS)  

---

## 1. Resumen de Endurecimiento y Mejoras Implementadas

### A. Endurecimiento en `.agents/skills/content-to-course/cta_merge.py`
1. **Resolución Determinista de Ciclos Intra-Parte Accidentales (`A <-> B`):**
   - Se preservó `_sort_key` durante el ordenamiento topológico intra-parte para que el fallback ante ciclos preserve de manera determinista el orden relativo original (`(sp_idx, f_idx, page_int, orig_idx)`).
   - Se agregó logging de advertencia y se garantizó que ningún nodo se descarte en el ordenamiento topológico (`visited_indices` contiene el 100% de los nodos de la subparte).
   - El filtro backward-only posterior (`comp_pos[prereq] < idx`) elimina de forma exacta la arista hacia adelante residual generada por el ciclo, convirtiendo el grafo en un DAG estrictamente acíclico y garantizando que `check_prerequisites_dag` pase con 0 errores.

2. **Modo Incremental (`--append` / `delta_manifest.json`):**
   - Se extrajo el conjunto canónico `existing_comp_ids` consolidando `manifest_data["delta"]`, `manifest_data["existing_course"]`, `manifest_data["delta_manifest"]`, archivo `delta_manifest.json` y `manifest_data["existing_competency_ids"]`.
   - Se integró la resolución de prefijos explícitos de curso base (`"existing:"`, `"base:"`, `"course:"`, `"delta:"`).
   - Se intercaló la verificación `p in existing_comp_ids` en la reescritura de prerrequisitos, previniendo que un prerrequisito a una competencia del curso base existente colisione o sea sobreescrito por el mapeo de otra subparte que reuse el mismo ID local.
   - En el filtrado backward-only, se garantizó que cualquier prerrequisito perteneciente a `existing_comp_ids` sea preservado intacto.

3. **Garantía Total de Limpieza de Llaves Temporales:**
   - Se implementó un bucle final explícito de saneamiento que elimina `_part_key` y `_sort_key` de todas las competencias antes de generar `id_map_payload`, `draft_payload`, `outline_payload`, `cta_draft.json` y `cta.json`.
   - Ninguna llave interna privada se filtra al archivo ni a disco.

---

## 2. Ampliación de Tests Adversarios en `tests/test_cta_merge_prereq_scoping.py`

Se agregaron 3 nuevos tests adversarios de alta exigencia:
1. `test_intra_part_cycle_fallback_deterministic_dag`:
   - Simula un ciclo mutuo circular `C-01 <-> C-02` dentro de `part_01.json`.
   - Verifica que el fallback se ejecuta sin loop infinito, no se pierde ninguna competencia, la arista hacia adelante es purgada determinísticamente, `check_prerequisites_dag` pasa con 0 errores y las llaves `_part_key`/`_sort_key` no quedan en disco.
2. `test_incremental_append_preserves_base_course_prereqs`:
   - Simula una ejecución en modo `--append` con `delta` (`existing_competency_ids: ["C-01", "H-01"]`, `next_numbers_by_prefix: {"C": 2, "H": 2, "Hab": 1}`).
   - `part_01` y `part_02` reúsan IDs locales y apuntan a competencias base como `H-01` y `base:C-01`.
   - Verifica que las dependencias hacia el curso base se conservan intactas, las locales se renumeran sin colisión, `check_prerequisites_dag` pasa con 0 errores y `validate_cta_rules` retorna `(True, [])`.
3. `test_asymptotic_statistics_v6_scale_simulation`:
   - Simulación a escala real del caso de producción `asymptotic_statistics_v6` con 2 partes (12 y 13 competencias respectivamente, total 25 competencias) donde ambas numeran localmente desde `C-01, H-01, Hab-01`.
   - Valida 8 hechos (`H-01`..`H-08`), 9 conceptos (`C-01`..`C-09`), 8 habilidades (`Hab-01`..`Hab-08`), 0 forward prerequisites en toda la secuencia, 0 errores en `check_prerequisites_dag`, `validate_cta_rules` == `True` y ausencia total de llaves temporales.

---

## 3. Resultados de la Suite de Pruebas

Ejecución oficial requerida:
```bash
.venv\Scripts\python.exe -m pytest tests/test_cta_merge_prereq_scoping.py tests/test_cta_sweetspot_and_autoheal.py tests/test_cta_mapreduce.py -q
```
Resultado:
```
....................................                                     [100%]
36 passed in 5.04s
```
Desglose de `tests/test_cta_merge_prereq_scoping.py` (8 tests):
- `test_two_parts_identical_local_ids_scoping`: PASSED
- `test_explicit_cross_part_prerequisite_prefix`: PASSED
- `test_intra_part_topological_sort_inverts_order`: PASSED
- `test_strict_backward_only_guarantee_drops_unresolvable_forward_prereqs`: PASSED
- `test_full_dag_validation_with_check_prerequisites_dag`: PASSED
- `test_intra_part_cycle_fallback_deterministic_dag`: PASSED
- `test_incremental_append_preserves_base_course_prereqs`: PASSED
- `test_asymptotic_statistics_v6_scale_simulation`: PASSED

---

## 4. Verificación de Fronteras Exclusivas de Escritura
- Archivos de producción modificados (únicos permitidos):
  1. `.agents/skills/content-to-course/cta_merge.py`
  2. `tests/test_cta_merge_prereq_scoping.py`
- Archivos de gobernanza modificados:
  - `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1a_impr/BRIEFING.md`
  - `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1a_impr/handoff.md`
- Ningún otro archivo del repositorio fue modificado.
