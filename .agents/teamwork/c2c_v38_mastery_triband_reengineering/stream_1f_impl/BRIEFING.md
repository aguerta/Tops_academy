# BRIEFING — Stream 1F (Fase 1: Implementador)
**Subagent:** `c2c38_implementer`  
**Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`  
**Date:** 2026-10-31  

---

## 1. Archivos Inspeccionados y Líneas Exactas

### 1.1 Producción
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\judge.py` (1148 líneas):
   - Líneas 163–304: `generate_judge_batch(...)` — Parámetros actuales `seeds=(101, 202)` e `items_per_competency=2`. Cuando `items_per_competency > 0`, estratifica truncando; cuando `<= 0`, itera plantillas. Debe cambiar a `seeds=(101, 202, 303)` e `items_per_competency=0` por defecto, garantizando muestreo de las 3 semillas en el 100% de las plantillas de todas las competencias sin truncamiento. Cada ítem debe registrar `template_id` y `competency_id` en `judge_batch.json` y `judge_ground_truth.json` / `answer_key.json`.
   - Líneas 779–794: `emit_judge_redispatch(...)` — Línea 784 emite `"TypeName": "c2c_blind_judge"`, que debe corregirse a `"c2c_judge"`.
   - Líneas 804–1033: `compare_judge_responses(...)` — Actualmente solo escanea `judge_responses_*.json`. Debe extender el escaneo a `work/judge_*.json` y `work/judges/judge_*.json` (desenvolviendo payloads `list` o dicts con `"evaluations"`, `"responses"`, `"items"`).
   - Líneas 885–997: Tolerancia cero a lotes vacíos (`total == 0`) o incompletos (`missing response`). Exigir 100% de acuerdo (`1.0`) por cada `template_id` (y `competency_id`). Si cualquier plantilla tiene `< 1.0`, registrar en `failed_templates` y `failed_competencies`, fijando `passed = False`.
2. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\course_publisher.py` (543 líneas):
   - Línea 56: Declaración de dataclass `PublicationResult`.
   - Línea 98: `CoursePublisher.publish(...)`.
   - Líneas 156–314: Lógica de merge en modo `append=True`. Actualmente compara `inc_name == ex_name` y colisiones brutas. Debe incorporar el detector determinista compuesto en dos ejes (`content_stem_jaccard` y `math_symbol_jaccard`) con umbrales `>= 0.38` o (`>= 0.28` y `math_symbol_jaccard >= 0.50`), actualización de `prerequisites` tras `comp_id_remap` y validación de DAG post-merge.
   - Compuerta Pre-Publish: Crear `PublishQualityGateError(ValueError)` y cargar dinámicamente `run_full_audit` desde `.agents/skills/course-qa-evaluator/scripts/standardized_audit_engine.py`. Bajo `strict=True`, ejecutar `run_full_audit(parsed)` antes de escribir `courses/<course_id>.json`, guardar `work/audit_gate_report.json`, y abortar con `PublishQualityGateError` si se violan los 5 criterios del gate.

### 1.2 Suites de Test Asignadas
1. `tests/test_new_audit_linters.py` (352 líneas): Pruebas de linters deterministas. Se ampliará con pruebas del gate de publicación y detección de bloqueos MPRI/ZPD/P4/padded.
2. `tests/test_c2c_validator_prescriptive.py` (299 líneas): Pruebas prescriptivas y herméticas. Se ampliará con pruebas de `PublishQualityGateError` y ejecución hermética.
3. `tests/test_dispatch_scope.py` (344 líneas): Pruebas de scope y contratos de subagentes. Se preservará la compatibilidad con `dispatch.py` (4 tipos, prompts sin truncar) y se añadirán pruebas para `split_judge_batch`, lectura de `work/judges/judge_*.json` y `TypeName == "c2c_judge"`.
4. `tests/test_pipeline_optimizations.py` (251 líneas): Pruebas de optimizaciones de pipeline. Se ampliará con pruebas de tolerancia cero en `judge.py` (3 semillas, 100% templates, rechazo total==0 e incompleto, fallo por 1 desacuerdo en template) y detección de paráfrasis en `course_publisher.py --append`.

---

## 2. Contratos y Especificación Técnica

### 2.1 `judge.py`
- **`generate_judge_batch(templates_path, work_dir, cta_path=None, seeds=(101, 202, 303), items_per_competency=0, ready_only=False)`**:
  - Si `items_per_competency <= 0` (default): generar exactamente `len(seeds)` instancias para cada plantilla de todas las competencias.
  - Si `items_per_competency > 0`: mantener estratificación respetando el límite por competencia.
  - Guardar `judge_batch.json`, `judge_ground_truth.json` y `answer_key.json` registrando `template_id` y `competency_id` en cada ítem.
- **`compare_judge_responses(responses=None, ground_truth=None, cycle=1, work_dir=None)`**:
  - Escanear archivos `judge_*.json` y `judges/judge_*.json` además de `judge_responses_*.json`, excluyendo `judge_batch*`, `judge_report*`, `judge_ground_truth*`, `judge_redispatch*`, `evaluated_competencies*`.
  - Normalizar respuestas tanto si vienen en dict directo `{id: ans}` o con llaves `"evaluations"`, `"responses"`, `"items"`, `"results"`, o listas de objetos.
  - Si `total == 0` o `missing response` para cualquier `item_id`: `passed = False`.
  - Si para cualquier `template_id` el acuerdo es `< 1.0` (100%): `passed = False`. Registrar en `failed_templates` y `failed_competencies`.
- **`emit_judge_redispatch(work_dir, ...)`**:
  - Subagents generados deben tener `"TypeName": "c2c_judge"`.

### 2.2 `course_publisher.py`
- **`PublishQualityGateError(ValueError)`**:
  - Excepción exportada a nivel de módulo.
- **Carga dinámica de `standardized_audit_engine`**:
  - Usar `importlib.util.spec_from_file_location` apuntando a `.agents/skills/course-qa-evaluator/scripts/standardized_audit_engine.py` de forma hermética.
- **Compuerta Bloqueante en `CoursePublisher.publish(...)`**:
  - Si `strict=True`:
    - Ejecutar `audit_report = run_full_audit(parsed)`.
    - Si `work_dir` disponible, escribir `audit_gate_report.json`.
    - Evaluar 5 condiciones:
      1. `len(questions) >= 20 and mpri_score < 75.0`
      2. `len(questions) >= 6 and zpd_score <= 0.0`
      3. `total_rationales >= 60 and (diag_pillar_score < 13.0 or rationale_uniqueness_pct < 30.0)`
      4. `len(hard_penalties) > 0 or any(severity == "critical")`
      5. `len(risk_clusters.get("length_padded_options", [])) > 0`
    - Si se viola cualquiera: lanzar `PublishQualityGateError` ANTES de persistir el JSON.
  - Si `strict=False`: no bloquear por MPRI/ZPD/P4/padded.
- **Detector Determinista Compuesto en `--append`**:
  - Función de similitud compuesta con stopwords académicas en español normalizadas (sin tildes, minúsculas, palabras len >= 3, truncamiento a 5 caracteres).
  - Jaccard de símbolos matemáticos LaTeX extraídos de fórmulas `$ ... $` y comandos `\cmd`.
  - Criterio de match: `content_stem_jaccard >= 0.38` O `(content_stem_jaccard >= 0.28 and math_symbol_jaccard >= 0.50)`.
  - Actualización de `prerequisites` en competencias remapeadas y validación de DAG cíclico post-merge. Mantener log de `"FALLBACK REMAP"` para colisiones de ID sin match de contenido.

---

## 3. Riesgos Detectados y Mitigaciones

1. **Regla Zero-Domain (`test_skill.py:705-725`):**
   - Palabras prohibidas en minúsculas en cualquier archivo `.py` de la skill: `edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`.
   - *Mitigación:* Todos los comentarios, docstrings y nombres de variables en `judge.py` y `course_publisher.py` se escribirán en inglés limpio, evitando palabras en español como "puedo", "quedo", "heredo" o "regresión".
2. **Compatibilidad con tests existentes:**
   - En `test_append_workflow.py`, `test_course_publisher_warned_fallback_remap_when_unaware_of_delta` espera que se registre `[WARN] FALLBACK REMAP` cuando dos competencias con el mismo ID tienen nombres completamente distintos. El detector compuesto debe preservar este comportamiento si la similitud está por debajo del umbral.
   - En `test_dispatch_scope.py`, `compare_judge_responses` espera llaves existentes (`agreement_rate`, `passed`, `discordances`, `affected_template_ids`). Debemos enriquecer el reporte agregando `failed_templates` y `failed_competencies` sin eliminar las llaves históricas.
3. **Guardias de Hooks:**
   - No ejecutar comandos prohibidos de hooks (`run.py --help`, scripts temporales). Ejecutar siempre `& ".venv\Scripts\python.exe" -m pytest <test_files> -q`.

---

## 4. Plan de Acción Inmediato
1. Implementar modificaciones en `judge.py`.
2. Implementar modificaciones en `course_publisher.py`.
3. Actualizar y ampliar las suites de test (`test_new_audit_linters.py`, `test_c2c_validator_prescriptive.py`, `test_dispatch_scope.py`, `test_pipeline_optimizations.py`).
4. Ejecutar validación pytest sobre las 4 suites + `test_skill.py` + `test_append_workflow.py`.
5. Redactar `handoff.md` y notificar al Orquestador con `DONE::`.
