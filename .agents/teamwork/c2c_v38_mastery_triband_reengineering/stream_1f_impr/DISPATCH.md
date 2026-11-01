# DISPATCH — Stream 1F (Fase 2: Mejorador)

- **Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1f_impr`
- **Impl Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1f_impl\handoff.md`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\judge.py`
2. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\course_publisher.py`
3. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_new_audit_linters.py`
4. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_c2c_validator_prescriptive.py`
5. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_dispatch_scope.py`
6. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_pipeline_optimizations.py`
7. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1f_impr\handoff.md` `[NEW]`

PROHIBIDO tocar cualquier otro archivo.

## Objetivos de Endurecimiento (Fase 2 — Mejorador)
1. Lee `stream_1f_impl/handoff.md` y revisa con `read_file` los cambios en `judge.py`, `course_publisher.py` y las 4 suites asignadas.
2. **Endurecimiento en `judge.py`:**
   - Verifica que `compare_judge_responses` maneje correctamente múltiples archivos de jueces ciegos (`judge_01.json`, `judge_02.json` o `work/judges/judge_*.json`), duplicados de `item_id` entre réplicas, respuestas malformadas/vacías (`total == 0` -> `passed = False`) y falta de `template_id` en legacy items (derivándolo desde `answer_key.json` si no viene en la respuesta del juez).
   - Confirma que `judge_report.json` incluye `passed`, `total`, `all_complete`, `failed_templates`, `failed_competencies` y `disagreements` con formato consumible por `dispatch.py` (`dispatch-repair`) y `run.py`.
3. **Endurecimiento en `course_publisher.py`:**
   - Verifica que `work/audit_gate_report.json` se escriba con UTF-8 limpio tanto cuando el gate pasa como antes de lanzar `PublishQualityGateError` (para dejar trazabilidad forense cuando aborta!).
   - Verifica empíricamente en un test adversario el caso real de `Matiz 3` (dos competencias paráfrasis tipo Semana 9 con Jaccard léxico crudo ~`0.44` y símbolos matemáticos compartidos `$\hat{\beta}$` / `$\varepsilon$` -> fusionadas por `content_stem_jaccard >= 0.38` o `stem >= 0.28 + math >= 0.50`, frente a dos competencias genuinamente distintas del mismo tema -> NO fusionadas).
   - Verifica que el remapeo de `prerequisites` en `--append` no introduzca auto-dependencias (`cid in c["prerequisites"]`) ni duplicados en la lista `prerequisites` cuando una competencia delta dependía de la competencia base con la que se fusionó.
   - Verifica **0 subcadenas Zero-Domain prohibidas** en `judge.py` y `course_publisher.py` (`edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`).

## Verificación
Ejecuta (respetando las guardias de hooks: nunca `--help` sobre scripts C2C ni `python -c` leyendo `"content-to-course/"`):
```powershell
& ".venv\Scripts\python.exe" -m pytest tests/test_new_audit_linters.py tests/test_c2c_validator_prescriptive.py tests/test_dispatch_scope.py tests/test_pipeline_optimizations.py -q
```
Escribe `handoff.md` en `stream_1f_impr/` y envía `DONE:: Stream 1F Impr completado (<N> passed)` a `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`.
