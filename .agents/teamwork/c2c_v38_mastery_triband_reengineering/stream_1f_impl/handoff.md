# HANDOFF — Stream 1F (Fase 1: Implementador)

- **Stream:** Stream 1F — Blind Judge Zero-Tolerance, Pre-Publish Quality Gate & Append Composite Paraphrase Merging
- **Fase:** Fase 1 (Implementador)
- **Status:** COMPLETED
- **Target Deliverables:** `judge.py`, `course_publisher.py`, and test suites `test_new_audit_linters.py`, `test_c2c_validator_prescriptive.py`, `test_dispatch_scope.py`, `test_pipeline_optimizations.py`.

---

## 1. Archivos Modificados en la Frontera Exclusiva

| Archivo | Resumen de Cambios |
| :--- | :--- |
| `.agents/skills/content-to-course/judge.py` | - Defaults actualizados a `seeds=(101, 202, 303)` e `items_per_competency=0` (cobertura 100% de plantillas sin sesgo de truncamiento).<br>- `emit_judge_redispatch`: emite `"TypeName": "c2c_judge"`.<br>- `compare_judge_responses`: auto-descubrimiento en `work/judges/judge_*.json` y desenvolvimiento de respuestas tipo `list` o dict con clave `evaluations`/`responses`/`items`/`results`.<br>- Tolerancia cero a lotes vacíos (`total == 0`), lotes incompletos (`not all_complete`), y exigencia de 100% de acuerdo en cada `template_id` con reporte de `failed_templates` y `failed_competencies`. |
| `.agents/skills/content-to-course/course_publisher.py` | - Declaración de `PublishQualityGateError(ValueError)`.<br>- Carga dinámica de `run_full_audit` desde `standardized_audit_engine.py` (`_load_run_full_audit`).<br>- Compuerta bloquente pre-publicación bajo `strict=True` que evalúa MPRI (<75 para >=20 preguntas), colapso ZPD (<=0 para >=6 preguntas), Pilar 4 de remediación diagnóstica (<13 o unicidad <30% para >=60 rationales), penalidades duras / fallas críticas, y clusters de riesgo con `length_padded_options`. Escritura de `audit_gate_report.json` en `work/`.<br>- Detector determinista compuesto para `--append`: `_strip_accents`, `_extract_content_stems` (con stopwords académicas y normalización a raíces de 5 caracteres), `_extract_math_symbols` (LaTeX commands y variables $...$), y similitud Jaccard compuesta (`content_stem_j >= 0.38` o `content_stem_j >= 0.28 and math_j >= 0.50`).<br>- Remapeo consistente de `prerequisites` en todas las competencias fusionadas tras reasignación de IDs y validación post-merge con `check_prerequisites_dag`. |
| `tests/test_new_audit_linters.py` | Añadidas pruebas unitarias exhaustivas para la compuerta de calidad:<br>- `test_publish_quality_gate_mpri_low`: rechazo por MPRI < 75.<br>- `test_publish_quality_gate_zpd_collapsed`: rechazo por ZPD <= 0.<br>- `test_publish_quality_gate_p4_diagnostic_remediation`: rechazo por reciclaje estático de rationales (< 30% unicidad / < 13 pts).<br>- `test_publish_quality_gate_length_padded`: rechazo por presencia de opciones infladas.<br>- `test_publish_quality_gate_hard_penalties`: rechazo por penalidades duras / severidad crítica.<br>- `test_publish_quality_gate_healthy_course_passes`: pase limpio ante banco Tri-Banda saludable. |
| `tests/test_c2c_validator_prescriptive.py` | Añadida clase `TestCoursePublisherQualityGateStrict`:<br>- `test_course_publisher_strict_false_bypasses_quality_gate`: modo no estricto permite publicación de micro-fixtures de prueba sin lanzar `PublishQualityGateError`.<br>- `test_course_publisher_strict_true_enforces_gate_and_writes_audit_report`: modo estricto detiene publicación y persiste `work/audit_gate_report.json`. |
| `tests/test_dispatch_scope.py` | Añadidas pruebas de contrato:<br>- `test_emit_judge_redispatch_emits_c2c_judge`: verifica emisión de `TypeName == "c2c_judge"`.<br>- `test_compare_judge_responses_judges_dir_and_evaluations_wrapper`: auto-descubrimiento en subdirectorio `judges/` y desenvolvimiento de wrapper `{"evaluations": [...]}`. |
| `tests/test_pipeline_optimizations.py` | Añadidas pruebas de optimización y tolerancia cero:<br>- `test_judge_sampling_three_seeds_full_template_coverage`: muestreo de 3 semillas (101, 202, 303) en el 100% de las plantillas (T-01..T-04) con registro obligatorio de `template_id` y `competency_id`.<br>- `test_judge_zero_tolerance_rejection_empty_or_incomplete`: rechazo ante lotes vacíos o incompletos.<br>- `test_judge_zero_tolerance_single_template_disagreement`: rechazo ante desacuerdo en una sola plantilla registrando `failed_templates` y `failed_competencies`.<br>- `test_course_publisher_append_paraphrase_detection_and_prereqs_remap`: fusión de paráfrasis reales (Jaccard 0.40–0.54) con remapeo íntegro de prerequisitos y validación DAG limpia. |

---

## 2. Verificación de Suites de Pruebas

### Comando Asignado en DISPATCH.md:
```powershell
& ".venv\Scripts\python.exe" -m pytest tests/test_new_audit_linters.py tests/test_c2c_validator_prescriptive.py tests/test_dispatch_scope.py tests/test_pipeline_optimizations.py -q
```

### Salida Exacta:
```
..................................................                       [100%]
50 passed in 1.95s
```

### Pruebas de Regresión Adicionales:
- `tests/test_append_workflow.py`: `10 passed in 0.52s`
- Zero-Domain Rule (`tests/test_skill.py -k test_engine_zero_domain_logic`): `1 passed, 32 deselected in 0.27s` (100% libre de términos de dominio en `.agents/skills/content-to-course/`).

---

## 3. Contratos Cumplidos

1. **`P0.6` (Arbitraje Ciego Tolerancia-Cero en 100% de Plantillas):**
   - Muestreo sin sesgo de truncamiento con semillas deterministas `(101, 202, 303)`.
   - Si cualquier plantilla presenta acuerdo < 1.0, el reporte falla (`passed = False`) y se indexa en `failed_templates` y `failed_competencies`.
   - Lotes vacíos o con respuestas faltantes son rechazados inmediatamente.
2. **`Brecha 1` (Compuerta Bloqueante Pre-Publish con `standardized_audit_engine.py`):**
   - Ejecuta `run_full_audit` antes de escribir en disco bajo `strict=True`.
   - Lanza `PublishQualityGateError` detallado ante violaciones de MPRI, colapso ZPD, degradación en diagnóstico P4 o clusters de longitud inflada.
   - Preserva `strict=False` para micro-fixtures de testing sin romper contratos legados.
3. **`Matiz 3` (Detector Determinista Compuesto en `--append`):**
   - Fusión robusta de paráfrasis conceptuales en el rango 0.40–0.54 mediante análisis simultáneo de raíces léxicas normalizadas y símbolos matemáticos LaTeX.
   - Remapeo completo de `c["prerequisites"]` asegurando la aciclicidad del DAG mediante `check_prerequisites_dag`.
