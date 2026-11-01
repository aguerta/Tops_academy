# DISPATCH — Stream 2A (Fase 3: Auditor Forense Read-Only)

- **Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_2a_audit`
- **Impl Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_2a_impl\handoff.md`
- **Impr Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_2a_impr\handoff.md`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_2a_audit\audit_report.md` `[NEW]`

PROHIBIDO tocar cualquier archivo de producción o `tests/`.

## Protocolo de Auditoría Forense (Stream 2A)
1. **Higiene y Frontera de Stream 2A:**
   - Ejecuta `git status --short` y verifica cero scripts temporales sueltos ni `.c2c_subagent_lock.json` activos en el workspace, y que los archivos de `Stream 2A` correspondan a `run.py`, `SKILL.md` y sus 7 suites asignadas.
2. **Inspección de Código en Producción (`read_file` en bloques amplios `400-800` líneas):**
   - `run.py`:
     - Confirma predicado simétrico `needs_harmonize = (self.cta_mode == "mapreduce") or bool(part_files) or bool(is_append_mode)` en `run_stage_cta` (`Matiz 3` y `Matiz 4a`), invocando `merge_cta_parts` cuando hay `part_files` o `prepare_harmonize_from_single_draft` en modo `direct` `--append`, y despachando `c2c_cta_harmonizer` (`cta-reduce`) hacia `cta-apply` sin exigir un `work/cta.json` prematuro.
     - Confirma `"cta-reduce"` en `AUXILIARY_STAGES`, paso de `sources` completo en `run_stage_prepare` (preservando el banner de estado), `min_archetypes = 3`, `seeds=(101, 202, 303), items_per_competency=0` en `judge` y bloqueo en `run_stage_publish` ante `not jr_data.get("passed", False)` o `PublishQualityGateError`.
   - `SKILL.md`: confirma documentación actualizada al contrato C2C v3.8 (`> 25` págs -> `mapreduce`, `cta -> cta-reduce -> cta-apply`, `Form-B` Tri-Banda Multimodal con 3-tuplas `@var@`, 3 semillas/plantilla y gate `MPRI >= 75` + `P4 >= 13.0/15`).
3. **Ejecución Independiente de las 7 Suites (incluyendo `test_skill.py` Zero-Domain y `test_prompts_contract_alignment.py`):**
   ```powershell
   & ".venv\Scripts\python.exe" -m pytest tests/test_prompts_contract_alignment.py tests/test_bootstrap_and_wave_streaming.py tests/test_run_templates_and_dispatch_repair.py tests/test_append_workflow.py tests/test_c2c_v321_multi_instance_and_append.py tests/test_skill.py tests/test_delete_course.py -q
   ```
4. Escribe `audit_report.md` en `stream_2a_audit/` y envía `PASS:: Stream 2A (<N> passed)` o `REJECT:: Stream 2A | <archivo:línea> | <causa>` a `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`.
