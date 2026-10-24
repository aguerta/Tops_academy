# DISPATCH — Stream 2A (Fase 1: Implementador Integrador `impl_2a`)

## 1. Rol y Frontera Exclusiva de Escritura (`Exclusive Write Boundaries`)
Eres el **Implementador Integrador del Stream 2A (Etapa 2 Post-Gate 1)** bajo `/flash-triad-orchestrator`.
- **Carpeta de Gobernanza:** `.agents/teamwork/c2c_v34_variance_and_shard06/stream_2a_impl/`
- **Archivos Permitidos:**
  1. `.agents/skills/content-to-course/subagent_types.json`
  2. `courses/asyntotic_estatistics_v4/work/templates/Hab-06.json`
  3. `courses/asyntotic_estatistics_v4/work/shards/shard_06.json`
  4. `courses/asyntotic_estatistics_v4/work/.check_attempts/*` *(generados por `compile_shard.py`)*
  5. `tests/test_forensic_shard06_and_variance_v34.py` *(nuevo archivo E2E)*
  6. Limpieza de `out_compile.txt` en la raíz si existe.
- **Artefactos de Gobernanza Permitidos:**
  - `.agents/teamwork/c2c_v34_variance_and_shard06/stream_2a_impl/BRIEFING.md`
  - `.agents/teamwork/c2c_v34_variance_and_shard06/stream_2a_impl/handoff.md`

## 2. Paso 0 Obligatorio (*Pre-Flight Sanity Check*)
1. Lee los handoffs de las 4 auditorías del Gate 1 (`stream_1a_audit/handoff.md`, `stream_1b_audit/handoff.md`, `stream_1c_audit/handoff.md`, `stream_1d_audit/handoff.md`) y escribe `BRIEFING.md`.
2. Si existe `out_compile.txt` suelto en la raíz del proyecto, elimínalo.

## 3. Especificación Técnica de Integración y Certificación
1. **Sincronización de `.agents/skills/content-to-course/subagent_types.json`:**
   - Regenera `.agents/skills/content-to-course/subagent_types.json` invocando `generate_define_subagent_specs` (de `dispatch.py`, con `lean=False` para el archivo estático o como lo espere `tests/test_prompts_contract_alignment.py` — verifica primero cómo `dispatch.py` o `tests/test_prompts_contract_alignment.py` valida `subagent_types.json`).
2. **Compilación y Certificación Estricta de `shard_06` (`Hab-06`) en `courses/asyntotic_estatistics_v4`:**
   - Ejecuta el comando exacto de compilación sobre `shard_06_data.py`:
     `.venv\Scripts\python.exe .agents/skills/content-to-course/compile_shard.py --input courses/asyntotic_estatistics_v4/work/shards/shard_06_data.py --output courses/asyntotic_estatistics_v4/work/shards/shard_06.json --cta courses/asyntotic_estatistics_v4/work/cta.json --manifest courses/asyntotic_estatistics_v4/work/pre_cta_manifest.json --strict`
   - Ejecuta también `check_templates.py`:
     `.venv\Scripts\python.exe .agents/skills/content-to-course/check_templates.py courses/asyntotic_estatistics_v4/work/templates/Hab-06.json --cta courses/asyntotic_estatistics_v4/work/cta.json --strict`
   - Comprueba que `Hab-06.json` se genera con **0 errores**, que `shard_06.json` tiene `"compiled_status": "PASS"` y que `.check_attempts/pass_shard_06.json` existe con `"status": "PASS"`.
3. **Suite E2E `tests/test_forensic_shard06_and_variance_v34.py`:**
   - Crea `tests/test_forensic_shard06_and_variance_v34.py` verificando integradamente los 6 hallazgos forenses (`F-01` a `F-06`):
     - **F-01 & F-02:** `sanitize_katex_syntax` y `assemble_question` sobre `Hab-06` real (`b_{IV} - b_{LS}` intacto y prioridad de `error_rationale` del autor + fallback seguro).
     - **F-03:** Compilación de los 4 arquetipos disjuntos del Milestone 3 usando formato DRY compacto de distractores sin repetir 24x `error_rationale`.
     - **F-04:** Diagnóstico `R-20` quirúrgico, rutas reales en `render_compact_aggregated_errors`, recibo `--output` y marcador `pass_shard_06.json`.
     - **F-05:** `dispatch_authors` con inyección Turn-0 completa (`correct_belief`, `manifestation`, `remediation_hint`) y directriz anti-lectura innecesaria de PDFs (100% agnóstica al dominio), más limpieza de `pass_<shard_id>.json` en `dispatch_repair`.
     - **F-06:** `c2c_hook_guard.py` bloqueando scripts `.py` ad-hoc (`test_debug.py`), bloqueando ediciones Post-PASS (`pass_<shard_id>.json`) y bloqueando `write_file` monolítico `> 250` líneas tras fallo previo.
4. Ejecuta todas las suites relevantes con `.venv\Scripts\python.exe -m pytest tests/test_forensic_shard06_and_variance_v34.py tests/test_assemble_katex_and_rationale.py tests/test_shard06_and_dry_archetypes.py tests/test_dispatch_turn0_and_milestone3_prompts.py tests/test_hook_post_pass_and_write_isolation.py tests/test_prompts_contract_alignment.py`.
5. Escribe `handoff.md` y envía `DONE:: Stream 2A Implementer completado` a `526cfac0-d37b-49c9-bf09-00b5c520add2`.
