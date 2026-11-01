# DISPATCH — Stream 1F (Fase 1: Implementador)

- **Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1f_impl`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\judge.py`
2. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\course_publisher.py`
3. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_new_audit_linters.py`
4. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_c2c_validator_prescriptive.py`
5. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_dispatch_scope.py`
6. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_pipeline_optimizations.py`
7. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1f_impl\BRIEFING.md` `[NEW]`
8. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1f_impl\handoff.md` `[NEW]`

PROHIBIDO modificar cualquier otro archivo.

## Reglas Pre-Flight y Guardias de Entorno
- **Hooks:** Prohibido ejecutar `run.py --help` / `dispatch.py --help` o `python -c` mencionando `"content-to-course/"` junto con `open(`, `read_text`, `run.py`, `prepare.py`, `ingest.py`, `dispatch.py`. Usa `read_file` y `& ".venv\Scripts\python.exe" -m pytest <archivos_test> -q`.
- **Zero-Domain (`test_skill.py`):** En `judge.py` y `course_publisher.py`, PROHIBIDO incluir (ni en comentarios ni en strings) las subcadenas en minúsculas: `edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`. ¡Cuidado en español con `puedo`, `quedo`, `heredo` (`edo`) o `regresión` (`regresi`)! Usa inglés en comentarios de `.py`.

## Especificación Técnica

### 1. `judge.py` (`P0.6` — Arbitraje Ciego Tolerancia-Cero en el 100% de las Plantillas)
- **`generate_judge_batch(work_dir, seeds=(101, 202, 303), items_per_competency=0, ...)`:**
  - Cambiar defaults a `seeds=(101, 202, 303)` e `items_per_competency=0`.
  - Cuando `items_per_competency <= 0` (default), muestrear las `3` semillas `(101, 202, 303)` para **el 100% de las plantillas (`template_id`) de todas las competencias** (eliminando el punto ciego que truncaba tras `T-XX-01` y `T-XX-02`). Si un test unitario pasa explícitamente `items_per_competency > 0`, respetar ese tope explícito.
  - Garantizar que cada ítem en `judge_batch.json` y `answer_key.json` registre `template_id` y `competency_id`.
- **`compare_judge_responses(work_dir, ...)`:**
  - Escanear respuestas tanto en `work/judge_*.json` como en `work/judges/judge_*.json` (excluyendo `judge_batch*.json` y `judge_report.json`).
  - Desenvolver payloads en forma de `list` directa o dict con clave `"evaluations"`, `"responses"` o `"items"`.
  - **Tolerancia cero a lotes vacíos o truncados:** si `total == 0` o falta respuesta para cualquier `item_id` del batch (`not all_complete`), fijar `passed = False`.
  - **Exigir `100%` de acuerdo (`1.0`) en CADA `template_id`:** calcular acuerdo por `template_id` (y por `competency_id`); si cualquier `template_id` tiene `< 1.0` de acuerdo, agregarlo a `"failed_templates"` y su competencia a `"failed_competencies"`, fijando `passed = False`. Exportar `"failed_templates"`, `"failed_competencies"` y `"disagreements"` detallados en `judge_report.json`.
- **`emit_judge_redispatch(...)`:** emitir `"TypeName": "c2c_judge"` (corrigiendo `"c2c_blind_judge"`).

### 2. `course_publisher.py` (`P0.6` + `Brecha 1` + `Matiz 3`)
1. **Compuerta Bloqueante Pre-Publish con `standardized_audit_engine.py` (`strict=True`, `Brecha 1`):**
   - Declarar `class PublishQualityGateError(ValueError): pass`.
   - Cargar dinámicamente `run_full_audit` desde `.agents/skills/course-qa-evaluator/scripts/standardized_audit_engine.py` (`importlib.util.spec_from_file_location`).
   - En `CoursePublisher.publish(..., strict: bool = True)`: ejecutar `audit_report = run_full_audit(parsed)` antes de escribir `courses/<course_id>.json`, guardando `work/audit_gate_report.json` cuando `work_dir` esté disponible.
   - Bajo `strict=True`, lanzar `PublishQualityGateError` con diagnóstico detallado antes de escribir `courses/<course_id>.json` si se cumple cualquiera de:
     - `len(questions) >= 20` y `mpri_score < 75.0`;
     - `len(questions) >= 6` y `pillars["zpd_adaptive_progression"]["score"] <= 0.0` (y si `len(questions) >= 20`, también cuando `pillars["zpd_adaptive_progression"]["score"] <= 0.0` incondicionalmente);
     - `total_rationales >= 60` y (`pillars["diagnostic_remediation_alignment"]["score"] < 13.0` o `rationale_uniqueness_pct < 30.0`);
     - `len(hard_penalties) > 0` o `any(i.get("severity") == "critical" for i in all_issues)`;
     - `len(risk_clusters.get("length_padded_options", [])) > 0`.
   - Cuando `strict=False` (usado por micro-fixtures sintéticos de tests unitarios), no bloquear por `PublishQualityGateError` salvo errores estructurales básicos ya existentes.
2. **Detector Determinista Compuesto en `--append` (`Matiz 3`):**
   - Reemplazar la heurística cruda `Jaccard >= 0.55` en el merge `--append` por una similitud determinista compuesta en dos ejes:
     - `content_stem_jaccard`: normalizar acentos/minúsculas, eliminar stopwords españolas/académicas (`de, la, el, en, los, las, un, una, del, al, para, por, con, sin, sobre, entre, mediante, hacia, desde, como, calculo, analisis, aplicacion, propiedad, propiedades, estudio, uso, concepto, metodo, modelo, teorema, definicion`), conservar palabras alfabéticas `len >= 3` y truncar cada palabra a su raíz de 5 caracteres (`tok[:5]`), calculando Jaccard de conjuntos de raíces.
     - `math_symbol_jaccard`: extraer comandos/símbolos matemáticos normalizados (ej. comandos `\alpha`, `\beta`, `\varepsilon`, `\sigma`, `\hat`, identificadores dentro de `$...$`), calculando Jaccard cuando ambos nombres/descripciones contienen símbolos matemáticos.
     - Detectar competencia duplicada y fusionar/remapear cuando **`content_stem_jaccard >= 0.38`** O **`(content_stem_jaccard >= 0.28 and math_symbol_jaccard >= 0.50)`** (capturando paráfrasis reales con Jaccard léxico crudo `0.40–0.54` como `0.444`).
   - Cuando `comp_id_remap` renombre cualquier ID en `--append`, actualizar `c["prerequisites"]` en todas las competencias fusionadas hacia los IDs definitivos (manteniendo el log `"FALLBACK REMAP"` esperado por tests) y validar `check_prerequisites_dag(merged_comps)` post-merge.

### 3. Actualización y Ampliación de las 4 Suites Exclusivas
Actualiza y amplía las 4 suites asignadas (`test_new_audit_linters.py`, `test_c2c_validator_prescriptive.py`, `test_dispatch_scope.py`, `test_pipeline_optimizations.py`) añadiendo pruebas explícitas para:
- `judge.py`: muestreo de 3 semillas `(101, 202, 303)` en el 100% de las plantillas (`T-01..T-04`), rechazo `total == 0` / incompleto, rechazo ante 1 desacuerdo en cualquier `template_id`, lectura desde `work/judges/judge_*.json` + wrapper `{"evaluations": [...]}` y `TypeName == "c2c_judge"`.
- `course_publisher.py`: bloqueo `PublishQualityGateError` por `MPRI < 75`, `ZPD <= 0`, **`P4 < 13.0` / `rationale_uniqueness_pct < 30%`** (caso tipo reciclaje estático), `length_padded_options > 0` y `hard_penalties > 0`, más pase limpio de un banco sano Tri-Banda con rationales dinámicos.
- `course_publisher.py --append`: detección y fusión de paráfrasis reales en el rango `0.40–0.54` (ej. dos competencias de un mismo concepto con redacción distinta y símbolos compartidos) + actualización de `prerequisites` tras `comp_id_remap`.
- *(Nota sobre `test_dispatch_scope.py`: solo edítalo si necesita algún ajuste menor, respetando que `dispatch.py` está siendo editado en paralelo por Stream `1C` manteniendo sus invariantes de 4 tipos base y strings de `prompt_shard_author.md`).*

## Verificación
Ejecuta:
```powershell
& ".venv\Scripts\python.exe" -m pytest tests/test_new_audit_linters.py tests/test_c2c_validator_prescriptive.py tests/test_dispatch_scope.py tests/test_pipeline_optimizations.py -q
```
Escribe `BRIEFING.md` antes de editar, `handoff.md` al terminar y notifica a `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589` con `DONE:: Stream 1F Impl completado (<N> passed)`.
