# BRIEFING — Stream 2A (Fase 1: Implementador)
**Fecha:** 2026-10-31
**Stream:** Stream 2A — Orquestación Simétrica, Sincronización CLI, SKILL.md y Verificación de Suites
**Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`

---

## 1. Archivos Inspeccionados y Frontera Exclusiva de Escritura
Se inspeccionaron detalladamente los siguientes archivos:
1. `run.py` (~2,049 líneas) — Runner modular CLI.
2. `SKILL.md` (~297 líneas) — Especificación operativa del skill C2C.
3. `tests/test_prompts_contract_alignment.py` (~439 líneas).
4. `tests/test_bootstrap_and_wave_streaming.py` (~925 líneas).
5. `tests/test_run_templates_and_dispatch_repair.py` (~417 líneas).
6. `tests/test_append_workflow.py` (~564 líneas).
7. `tests/test_c2c_v321_multi_instance_and_append.py` (~274 líneas).
8. `tests/test_skill.py` (~902 líneas).
9. `tests/test_delete_course.py` (~472 líneas).

Módulos de Gate 1 consultados (solo lectura):
- `cta_merge.py` (`merge_cta_parts`, `prepare_harmonize_from_single_draft`, `apply_harmonize`).
- `dispatch.py` (`dispatch_cta_reduce`, `dispatch_shards`, `dispatch_repair`).
- `ingest.py` (`ingest_course`).
- `judge.py` (`generate_judge_batch`).
- `course_publisher.py` (`CoursePublisher.publish`, `PublishQualityGateError`).

---

## 2. Puntos Exactos de Modificación en `run.py`
- **L227-241 (`AUXILIARY_STAGES`):**
  - Añadir `"cta-reduce": "run_stage_cta_reduce"` a `AUXILIARY_STAGES`.
  - Añadir método `run_stage_cta_reduce(self)` que invoca `dispatch_cta_reduce(self.work_dir)` y genera la orden de trabajo para `c2c_cta_harmonizer`.
  - Añadir `"cta-reduce"` a `stage_choices` en `main()`.
- **L406-488 (`run_stage_prepare`):**
  - Pasar la lista completa `sources` (no `input_target`) a `prepare_course(input_path=sources, ...)`.
  - Sincronizar `self.cta_mode = prep_res.get("cta_mode", self.cta_mode)` para auto-promoción a `mapreduce` cuando `total_pages > 25` o `len(sources) > 1`.
  - Preservar intacto el banner: `[STAGE 0: PREPARE] Stage 0: Lossless source partitioning & pre_cta_manifest generation`.
- **L494-647 (`run_stage_cta` — Matiz 3 y Matiz 4a):**
  - Evaluar predicado unificado:
    `is_append_mode = bool(getattr(self, "append", False)) or (self.work_dir / "delta_manifest.json").is_file()`
    `part_files = sorted(list((self.work_dir / "cta_parts").glob("part_*.json")) + list((self.work_dir / "cta").glob("cta_shard_*.json")))`
    `needs_harmonize = (self.cta_mode == "mapreduce") or bool(part_files) or bool(is_append_mode)`
  - Si `needs_harmonize`:
    - Si no existe `work/cta_harmonize.json`:
      - Si hay `part_files`, ejecutar `merge_cta_parts(self.work_dir)`.
      - Si no hay `part_files` (modo directo en append), invocar `prepare_harmonize_from_single_draft(self.work_dir)`.
      - Despachar `dispatch_cta_reduce(self.work_dir)`.
      - Indicar `Next Stage: cta-apply` y retornar `{ "status": "needs_harmonize", "next_stage": "cta-apply" }` sin exigir `cta.json`.
    - Si `work/cta_harmonize.json` ya existe y no existe `cta.json`, ejecutar `apply_harmonize(self.work_dir)`.
- **L724-830 (`run_stage_templates`):**
  - Pasar `--min-archetypes 3` a llamadas de compilación de shard.
- **L1074-1135 (`run_stage_verify`):**
  - Invocar `generate_judge_batch(templates_path=templates_dir, work_dir=self.work_dir, cta_path=..., seeds=(101, 202, 303), items_per_competency=0)`.
- **L1140-1250 (`run_stage_publish`):**
  - Bloquear publicación si `judge_report.json` existe con `not jr_data.get("passed", False)` o estatus distinto de `"pass"|"passed"`.
  - Pasar `work_dir=self.work_dir` a `publisher.publish(...)` permitiendo que `PublishQualityGateError` opere como compuerta bloqueante bajo `strict=True`.
- **L1740-1760 (`run_stage_judge_generate`):**
  - Invocar `generate_judge_batch(templates_path=templates_dir, work_dir=self.work_dir, cta_path=..., seeds=(101, 202, 303), items_per_competency=0, ready_only=self.ready_only)`.

---

## 3. Actualización de `SKILL.md`
- Documentar:
  - Promoción automática a `mapreduce` + `slice_pdf_lossless` (`k = ceil(P/20)`) para `> 25` páginas o multi-PDF.
  - Flujo simétrico `cta -> cta-reduce (c2c_cta_harmonizer) -> cta-apply` con nodos `[BASE]` de solo lectura y fail-fast `[KATEX-PROSE-OVERFLOW]` (`\text{...} > 45` caracteres).
  - Contrato único `Form-B` Tri-Banda Multimodal (`--min-archetypes 3`, bandas `easy/medium/hard`, `>= 2` Bloom, `>= 2` `FIB`/`MS` en `Hab-*`, `>= 1` `FIB`/`MS` en `C-*`/`H-*`, 3-tuplas `(did, val, rationale_con_@var@)` `[TPL-DYNAMIC-RATIONALE]`, `[TPL-STATIC-OPT]`).
  - Arbitraje ciego 100% de plantillas con 3 semillas `(101, 202, 303)` y compuerta bloqueante pre-publish `PublishQualityGateError` (`MPRI >= 75`, `ZPD > 0`, `P4 >= 13.0/15`, `rationale_uniqueness_pct >= 30%`, 0 hard penalties, 0 padded options).

---

## 4. Diagnóstico de Tests y Plan de Ajuste
- `tests/test_prompts_contract_alignment.py`:
  - `test_execution_example_h01_full_author_prompt`: La prueba parseaba `TEMPLATES[0]` asumiendo Form-A (índice 2 = stem, índice 7 = dids). Con Form-B Tri-Banda (9 elementos), el índice 6 es `stems`, índice 5 es `(diff, bloom)`, e índice 2 es el tipo de interacción. Además, las tuplas en `prompt_shard_author.md` generan distractores como 3-tuplas dinámicas. Actualizar el desempaquetado de la tupla Form-B en el test.
  - `test_execution_example_lean_author_prompt`: Regex buscaba `import math` en el bloque python lean, pero `lean/prompt_shard_author.md` inicia directamente con `def _gen_h01(...)`. Actualizar regex y desempaquetado Form-B.
- `tests/test_run_templates_and_dispatch_repair.py`:
  - `test_dispatch_repair_injects_templates_report_errors`: Esperaba el encabezado legacy `"### Errores Diagnosticados en Templates:"`. `dispatch.py` ahora genera `"### Diagnóstico Consolidado de Fallos y Discordancias:"`. Ajustar la aserción en el test.
- Verificación de la Regla Zero-Domain:
  - Prohibidas subcadenas en minúsculas: `edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi` en cualquier `.py` de `.agents/skills/content-to-course/`.
  - Asegurar comentarios en inglés limpio y verificar que `test_skill.py::test_engine_zero_domain_logic` pase al 100%.

---

## 5. Riesgos Detectados y Mitigación
1. **Riesgo Zero-Domain:** Palabras en español como `heredo`, `puedo`, `quedo` o `regresión` pueden disparar fallos en `test_engine_zero_domain_logic`.
   - *Mitigación:* Escribir todo código y comentarios en `run.py` en inglés estricto sin esas subcadenas.
2. **Riesgo de truncamiento en stdout de `run.py`:**
   - *Mitigación:* Se preserva `format_compact_json_stdout` y `cap_stdout_to_log` con límites <= 1,450 bytes.
3. **Frontera de escritura estricta:** Ningún archivo fuera de los 11 autorizados será tocado.
