# DISPATCH — Stream 2A (Fase 1: Implementador)

- **Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_2a_impl`

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
10. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_2a_impl\BRIEFING.md` `[NEW]`
11. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_2a_impl\handoff.md` `[NEW]`

PROHIBIDO modificar cualquier otro archivo.

## Reglas Pre-Flight y Guardias de Entorno
- Usa `read_file` en bloques amplios (`400-800` líneas por llamada) para máxima velocidad.
- **Hooks:** Prohibido ejecutar `run.py --help` / `dispatch.py --help` / `prepare.py --help` / `ingest.py --help` o `python -c` mencionando `"content-to-course/"` junto con `open(`, `read_text`, `run.py`, `prepare.py`, `ingest.py`, `dispatch.py`. Ejecuta tests únicamente con `& ".venv\Scripts\python.exe" -m pytest <archivos_test> -q`.
- **Zero-Domain (`tests/test_skill.py`):** En `run.py` (y en todo `.py` de `content-to-course/`), PROHIBIDO incluir (ni en comentarios ni en strings) las subcadenas en minúsculas: `edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`. ¡Cuidado en español con `puedo`, `quedo`, `heredo` (`edo`) o `regresión` (`regresi`)! Usa comentarios en inglés limpio en `run.py`.

## Especificación Técnica (Integración sobre Gate 1 Completado)
*(Nota: Todos los módulos de Gate 1 — `partition_corpus.py`, `ingest.py`, `prepare.py`, `cta_merge.py`, `compile_cta.py`, `check_cta.py`, `compile_shard.py`, `plan_shards.py`, `dispatch.py`, `check_templates.py`, `repair_loop.py`, `judge.py`, `course_publisher.py` — ya fueron implementados y certificados con `6/6 PASS::`. Lee sus firmas actuales en Pre-Flight).*

### 1. `run.py` (`Matiz 3` y `Matiz 4a` — Orquestación Simétrica)
1. **Registro de `"cta-reduce"` en `AUXILIARY_STAGES` y soporte de `--stage cta-reduce`:**
   - Añadir `"cta-reduce"` a `AUXILIARY_STAGES` y conectar su handler para generar el despacho de `c2c_cta_harmonizer` (`dispatch_cta_reduce` desde `dispatch.py`) sobre `work/cta_outline.json` + `work/duplicate_candidates.json`.
2. **`run_stage_prepare()` (`~L405-445`):**
   - Pasar la lista completa `sources` a `ingest_course(...)` (sin truncar al primer archivo) y sincronizar `self.cta_mode` cuando `ingest_course` promueva automáticamente a `"mapreduce"` (`> 25` págs o multi-PDF), preservando intacto el banner de estado esperado por tests (`~L410`).
3. **Predicado 100% Simétrico en `run_stage_cta()` (`Matiz 3` y `Matiz 4a`):**
   - Evaluar el predicado único compartido con `cta_merge.py`:
     `needs_harmonize = (self.cta_mode == "mapreduce") or bool(part_files) or bool(is_append_mode)`
     (donde `is_append_mode` es `bool(getattr(self, "append", False)) or (self.work_dir / "delta_manifest.json").is_file()`).
   - Cuando `needs_harmonize` sea `True`:
     - Si aún NO existe `work/cta_harmonize.json`:
       - Si hay `part_files`, ejecutar `merge_cta_parts(self.work_dir)` (que ahora escribe `cta_draft.json`, `cta_outline.json` y `duplicate_candidates.json`, y **jamás** escribe `work/cta.json`);
       - Si NO hay `part_files` (modo `direct` de 1 PDF corto bajo `--append`), invocar `prepare_harmonize_from_single_draft(self.work_dir)` desde `cta_merge.py`;
       - Emitir el despacho de `c2c_cta_harmonizer` (`dispatch_cta_reduce(self.work_dir)`), indicar `Next Stage: cta-apply` y retornar éxito **sin buscar un `work/cta.json` que aún no debe existir**.
     - Si `work/cta_harmonize.json` YA existe y aún no se ha generado `work/cta.json` (o al correr `--stage cta-apply`), invocar `apply_harmonize(self.work_dir)` para producir y validar `work/cta.json`.
4. **Alineación Stage 3 / Stage 5 / Stage 6 en `run.py`:**
   - Usar `min_archetypes = 3` (`--min-archetypes 3`) en compilación/despacho de shards y reparaciones.
   - En `run_stage_verify()` / `run_stage_judge_generate()`: invocar `generate_judge_batch(self.work_dir, seeds=(101, 202, 303), items_per_competency=0, ...)`.
   - En `run_stage_publish()`: bloquear publicación siempre que `judge_report.json` exista con `not jr_data.get("passed", False)` (lanzando error / retornando fallo antes de publicar), y delegar la validación bloqueante `strict=True` a `CoursePublisher.publish(...)` (`PublishQualityGateError`).

### 2. `SKILL.md`
- Actualizar `.agents/skills/content-to-course/SKILL.md` reflejando:
  - Promoción automática a `mapreduce` + `slice_pdf_lossless` (`k = ceil(P/20)`) para `> 25` páginas o multi-PDF.
  - Flujo simétrico `cta -> cta-reduce (c2c_cta_harmonizer) -> cta-apply` (incluyendo modo `--append` con nodos `[BASE]` de solo lectura) y Fail-Fast `[KATEX-PROSE-OVERFLOW]` (`\text{...} > 45` chars) desde Stage 1.
  - Contrato único `Form-B` Tri-Banda Multimodal (`--min-archetypes 3`, bandas `easy/medium/hard`, `>= 2` Bloom, `>= 2` `FIB`/`MS` en `Hab-*`, `>= 1` `FIB`/`MS` en `C-*`/`H-*`, 3-tuplas obligatorias `(did, val, rationale_@var@)` `[TPL-DYNAMIC-RATIONALE]`, `[TPL-STATIC-OPT]` incluso con `vars == {}`).
  - Arbitraje ciego tolerancia-cero con 3 semillas `(101, 202, 303)` en el 100% de las plantillas (`100%` acuerdo por `template_id`) y compuerta bloqueante pre-publish `PublishQualityGateError` (`MPRI >= 75`, `ZPD > 0`, `P4 >= 13.0/15`, `rationale_uniqueness_pct >= 30%`, `0` hard penalties, `0` padded options).

### 3. Actualización y Ampliación de las 7 Suites Exclusivas
Migra los fixtures legacy de las 7 suites al contrato C2C v3.8 (`Form-B` Tri-Banda con 3-tuplas `@var@`, `min_archetypes=3`, flujo `needs_harmonize` simétrico en `mapreduce` de 1 o N partes y en `--append`, `seeds=(101, 202, 303)` en `judge`, bloqueo `PublishQualityGateError` en `run_stage_publish`) y verifica que `test_prompts_contract_alignment.py` y `test_skill.py` (incluyendo `test_engine_zero_domain_logic`) pasen al 100%.

## Verificación
Ejecuta:
```powershell
& ".venv\Scripts\python.exe" -m pytest tests/test_prompts_contract_alignment.py tests/test_bootstrap_and_wave_streaming.py tests/test_run_templates_and_dispatch_repair.py tests/test_append_workflow.py tests/test_c2c_v321_multi_instance_and_append.py tests/test_skill.py tests/test_delete_course.py -q
```
Escribe `BRIEFING.md` antes de editar, `handoff.md` al terminar y notifica a `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589` con `DONE:: Stream 2A Impl completado (<N> passed)`.
