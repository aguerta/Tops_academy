# DISPATCH — Stream 2A (Fase 2: Mejorador)

- **Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_2a_impr`
- **Impl Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_2a_impl\handoff.md`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\run.py`
2. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\SKILL.md`
3. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_prompts_contract_alignment.py`
4. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_bootstrap_and_wave_streaming.py`
5. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_run_templates_and_dispatch_repair.py`
6. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_append_workflow.py`
7. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_c2c_v321_multi_instance_and_append.py`
8. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_skill.py`
9. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_delete_course.py`
10. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_2a_impr\handoff.md` `[NEW]`

PROHIBIDO tocar cualquier otro archivo.

## Objetivos de Endurecimiento (Fase 2 — Mejorador)
1. Lee `stream_2a_impl/handoff.md` y revisa con `read_file` (bloques amplios `400-800` líneas) `run.py`, `SKILL.md` y las 7 suites de tests.
2. **Endurecimiento de Simetría `Matiz 4a` y `Matiz 3` en `run.py`:**
   - Verifica el caso borde exacto de `Matiz 4a`: si alguien fuerza `cta_mode == "mapreduce"` sobre 1 solo PDF corto de 1 parte (`len(part_files) == 1`), `merge_cta_parts` NO escribe `work/cta.json`, y `run_stage_cta` usa `needs_harmonize` para despachar `cta-reduce` e indicar `Next Stage: cta-apply` sin fallar por ausencia de `work/cta.json`. Añade un test unitario explícito que certifique este caso borde (`cta_mode="mapreduce"` con 1 sola parte `cta_part_01.json`).
   - Verifica el caso borde de `Matiz 3`: modo `--append` con 1 PDF corto en modo `direct` (`0` `part_files`, `delta_manifest.json` presente): `needs_harmonize` es `True`, llama a `prepare_harmonize_from_single_draft(self.work_dir)` y despacha `c2c_cta_harmonizer` con nodos `[BASE]` antes de pasar a `cta-apply`.
   - Verifica que `run_stage_publish` rechace publicar tanto cuando `judge_report.json` tiene `passed == False` como cuando `CoursePublisher.publish(..., strict=True)` lanza `PublishQualityGateError` (por `MPRI < 75`, `ZPD <= 0` o `P4 < 13.0`).
   - Confirma que `tests/test_skill.py` (`test_engine_zero_domain_logic`) pasa limpio verificando **0 subcadenas prohibidas** en TODOS los archivos `.py` de `.agents/skills/content-to-course/`.

## Verificación
Ejecuta:
```powershell
& ".venv\Scripts\python.exe" -m pytest tests/test_prompts_contract_alignment.py tests/test_bootstrap_and_wave_streaming.py tests/test_run_templates_and_dispatch_repair.py tests/test_append_workflow.py tests/test_c2c_v321_multi_instance_and_append.py tests/test_skill.py tests/test_delete_course.py -q
```
Escribe `handoff.md` en `stream_2a_impr/` y envía `DONE:: Stream 2A Impr completado (<N> passed)` a `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`.
