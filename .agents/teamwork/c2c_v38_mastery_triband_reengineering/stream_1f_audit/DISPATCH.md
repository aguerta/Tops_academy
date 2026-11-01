# DISPATCH — Stream 1F (Fase 3: Auditor Forense Read-Only)

- **Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1f_audit`
- **Impl Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1f_impl\handoff.md`
- **Impr Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1f_impr\handoff.md`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1f_audit\audit_report.md` `[NEW]`

PROHIBIDO tocar cualquier archivo de producción o `tests/`.

## Protocolo de Auditoría Forense (Stream 1F)
*(Nota de concurrencia Gate 1: los Streams paralelos `1A, 1B, 1C, 1D` están ejecutándose simultáneamente sobre sus fronteras disjuntas, por lo que `git status` mostrará cambios legítimos en sus archivos).*

1. **Higiene y Frontera de Stream 1F:**
   - Ejecuta `git status --short` y verifica que no existan scripts sueltos ni `.c2c_subagent_lock.json` activos en el workspace, y que los archivos de `Stream 1F` correspondan únicamente a `judge.py`, `course_publisher.py`, `tests/test_new_audit_linters.py`, `tests/test_c2c_validator_prescriptive.py`, `tests/test_dispatch_scope.py` y `tests/test_pipeline_optimizations.py`.
2. **Inspección de Código en Producción (`read_file`):**
   - `judge.py`: confirma `seeds=(101, 202, 303)` e `items_per_competency=0` por defecto (3 semillas en el 100% de las plantillas), escaneo de `work/judges/judge_*.json`, desenvolvimiento de `evaluations`/`responses`/`items`, bloqueo `passed = False` ante `total == 0` o lotes incompletos, exigencia de `100%` de acuerdo por cada `template_id` (`failed_templates` y `failed_competencies` en `judge_report.json`) y `"TypeName": "c2c_judge"` en `emit_judge_redispatch`.
   - `course_publisher.py`:
     - Confirma `PublishQualityGateError(ValueError)`, persistencia de `work/audit_gate_report.json` y bloqueo bajo `strict=True` ante: `mpri_score < 75.0` (`>= 20` preguntas), `zpd_adaptive_progression <= 0.0`, **`diagnostic_remediation_alignment < 13.0` o `rationale_uniqueness_pct < 30.0`** (`total_rationales >= 60`), `hard_penalties > 0`, `severity == "critical"` o `length_padded_options > 0`.
     - Confirma similitud determinista compuesta en `--append` (`content_stem_jaccard >= 0.38` sobre raíces de 5 caracteres sin stopwords, o `content_stem_jaccard >= 0.28 and math_symbol_jaccard >= 0.50`), remapeo limpio de `prerequisites` (sin auto-ciclos ni duplicados, conservando log `"FALLBACK REMAP"`) y `check_prerequisites_dag` post-merge.
   - Confirma **0 subcadenas Zero-Domain prohibidas** en `judge.py` y `course_publisher.py` (`edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`).
3. **Inspección de Tests y Ejecución Independiente:**
   - Verifica en las 4 suites que los tests adversarios sean genuinos y sin mocks falsos.
   - Ejecuta:
     ```powershell
     & ".venv\Scripts\python.exe" -m pytest tests/test_new_audit_linters.py tests/test_c2c_validator_prescriptive.py tests/test_dispatch_scope.py tests/test_pipeline_optimizations.py -q
     ```
4. Escribe `audit_report.md` en `stream_1f_audit/` y envía `PASS:: Stream 1F (<N> passed)` o `REJECT:: Stream 1F | <archivo:línea> | <causa>` a `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`.
