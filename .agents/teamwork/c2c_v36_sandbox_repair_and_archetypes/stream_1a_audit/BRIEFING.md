# BRIEFING — Stream 1A (Fase 3: Auditor Forense `audit_1a`)

**Stream:** 1A — Aislamiento de Prerrequisitos por Subparte y Garantía Backward-Only en `merge_cta_parts`
**Rol:** Auditor Forense (Fase 3)
**Fecha:** 2026-10-25
**Objetivo de la Auditoría:**
Auditar de manera independiente y forense la implementación y endurecimiento realizados por el Implementador (`impl_1a`) y el Mejorador (`impr_1a`) en `.agents/skills/content-to-course/cta_merge.py` y `tests/test_cta_merge_prereq_scoping.py`.

## 1. Alcance de la Auditoría
1. **Inspección de Código (`cta_merge.py`):**
   - Verificar que `comp_id_map_by_part` aísla los identificadores locales por subparte (`_part_key`), evitando colisiones o sobreescrituras cuando subpartes (`part_01`, `part_02`) comparten IDs locales idénticos.
   - Verificar el algoritmo de ordenamiento topológico intra-parte: uso de Kahn con min-heap estable, degradación limpia ante ciclos accidentales sin loops infinitos ni pérdida de nodos.
   - Verificar el filtrado backward-only final (`comp_pos[prereq] < comp_pos[comp]`), garantizando 0 referencias hacia adelante en el DAG final.
   - Verificar preservación de prerrequisitos de cursos base existentes (`existing_competency_ids`) en modo incremental `--append`.
   - Verificar saneamiento y eliminación completa de llaves efímeras (`_part_key`, `_sort_key`) previo al guardado en disco y generación de payloads.
2. **Auditoría de Calidad de Pruebas Unitarias (`tests/test_cta_merge_prereq_scoping.py`):**
   - Confirmar que los tests no contienen aserciones triviales, falsos positivos ni mocks permisivos.
   - Verificar que validan casos adversarios, ciclos, prefijos calificados, simulación a escala y compatibilidad con `check_prerequisites_dag` y `validate_cta_rules`.
3. **Ejecución Independiente de Tests:**
   - Ejecutar la suite: `.venv\Scripts\python.exe -m pytest tests/test_cta_merge_prereq_scoping.py tests/test_cta_sweetspot_and_autoheal.py tests/test_cta_mapreduce.py -q`.
4. **Verificación de Fronteras Inviolables:**
   - Confirmar estricto Read-Only sobre producción y tests.
   - Confirmar que solo se modifican archivos de gobernanza en `stream_1a_audit/`.
