# DISPATCH — Stream 2A (Fase 2: Mejorador `impr_2a`)

- **Rol:** Mejorador (Fase 2 de la Tríada Secuencial — Etapa 2 Post-Gate 1)
- **Orquestador Conversation ID:** `526cfac0-d37b-49c9-bf09-00b5c520add2`
- **Handoff Previo (Lectura Obligatoria):** `.agents/teamwork/c2c_v34_variance_and_shard06/stream_2a_impl/handoff.md`
- **Directorio de Gobernanza:** `.agents/teamwork/c2c_v34_variance_and_shard06/stream_2a_impr/`

## 1. Frontera de Escritura Exclusiva (`Exclusive Write Boundary`)
Tienes permiso de escritura **ÚNICAMENTE** sobre:
1. `.agents/skills/content-to-course/subagent_types.json`
2. `courses/asyntotic_estatistics_v4/work/shards/shard_06_data.py`
3. `courses/asyntotic_estatistics_v4/work/shards/shard_06.json`
4. `courses/asyntotic_estatistics_v4/work/templates/Hab-06.json`
5. `courses/asyntotic_estatistics_v4/work/.check_attempts/*` (para limpieza/regeneración limpia de `pass_shard_06.json`)
6. `tests/test_forensic_shard06_and_variance_v34.py`
7. `tests/test_shard06_and_dry_archetypes.py` (únicamente L638–L640 en `test_compile_real_shard_06_strict_pass` para soportar el contenedor multi-arquetipo `payload["templates"]` de Milestone 3)
8. `.agents/teamwork/c2c_v34_variance_and_shard06/stream_2a_impr/BRIEFING.md`
9. `.agents/teamwork/c2c_v34_variance_and_shard06/stream_2a_impr/handoff.md`

**PROHIBIDO** modificar cualquier otro archivo del repositorio.

## 2. Hallazgos de Auditoría sobre `impl_2a` que DEBES Endurecer (Hardening)

### A. Endurecer aserciones permisivas (`or` -> `and`) en `tests/test_forensic_shard06_and_variance_v34.py`
En `tests/test_forensic_shard06_and_variance_v34.py`, `impl_2a` dejó varias aserciones con `or` que deben ser estrictas (`and`):
1. **Línea 436 (`test_surgical_r20_diagnostic_pinpoints_field_and_counts`):**
   - Exige simultáneamente que `diag.field_name == "options[1].error_rationale (distractor D-Hab06-02)"` **Y** que `"options[1].error_rationale (distractor D-Hab06-02)" in diag.cause` **Y** `"open=" in diag.cause and "close=" in diag.cause`.
2. **Línea 455 (`test_surgical_r20_detects_inverted_subscript_pattern`):**
   - Exige simultáneamente `"patrón invertido" in diag.cause` **Y** `"open=" in diag.cause` **Y** `"_}{" in diag.cause`.
3. **Línea 468 (`test_render_compact_aggregated_errors_uses_real_relative_path`):**
   - La condición `assert "work/templates/Hab-06.json" not in rendered or "courses/" in rendered` era débil porque `"courses/asyntotic_estatistics_v4/work/templates/Hab-06.json"` contiene `"courses/"`.
   - Reemplázala verificando explícitamente que el encabezado `[FILE ...]` contenga `"courses/asyntotic_estatistics_v4/work/templates/Hab-06.json"` y que **ninguna** línea empiece por `[FILE work/templates/Hab-06.json`.
4. **Líneas 563–564 (`test_dispatch_authors_turn0_rich_context_and_anti_pdf_reading`):**
   - Cambia `or` por `and`: exige que TANTO la etiqueta (`"Creencia Correcta"` o `"correct_belief"`) COMO la fórmula `r"$F(b) - F(a)$"` estén presentes en `prompt`, y que TANTO `"Remediation Hint"` COMO `"Invierta el orden de evaluación."` estén presentes en `prompt`.

### B. Preservar Test de Regresión del `shard_06_data.py` Original + Elevar `shard_06_data.py` de Producción a Milestone 3 (4 Arquetipos Disjuntos con DRY Distractors)
1. En `tests/test_forensic_shard06_and_variance_v34.py`, añade un test explícito `test_legacy_shard06_exact_code_compiles_cleanly(tmp_path)` que copie el código original de 1 tupla de `shard_06_data.py` (el que falló 10 veces en la corrida `0b8b5084`) junto con la entrada `Hab-06` de `courses/asyntotic_estatistics_v4/work/cta.json`, ejecute `compile_shard(..., strict=True, seeds=50)` y verifique que compila con `success is True` y `0` errores, preservando el `error_rationale` explícito del autor (`"Suma las varianzas en el denominador del estadistico de Hausman."`) sin corromper `b_{LS}` a `b_}{LS}`.
2. En `courses/asyntotic_estatistics_v4/work/shards/shard_06_data.py`, actualiza el archivo para que cumpla al 100% con **Milestone 3 (4 arquetipos disjuntos para `Hab-06`: 1. Directo/Frontal, 2. Inverso/Diagnóstico, 3. Perturbación/Estática Comparativa, 4. Frontera/Casos Límite)** usando el formato compacto DRY de distractores (tuplas de 2 elementos `("D-Hab06-01", r"...")` o dicts con `error_rationale` limpio) y fórmulas LaTeX bien formadas:
   - Limpia previamente `courses/asyntotic_estatistics_v4/work/.check_attempts/compile_shard_06.json` y `pass_shard_06.json` para recompilar desde cero.
   - Ejecuta:
     `.venv\Scripts\python.exe .agents/skills/content-to-course/compile_shard.py --input courses/asyntotic_estatistics_v4/work/shards/shard_06_data.py --output courses/asyntotic_estatistics_v4/work/shards/shard_06.json --cta courses/asyntotic_estatistics_v4/work/cta.json --manifest courses/asyntotic_estatistics_v4/work/shards/pre_shard_manifest.json --strict`
   - Ejecuta:
     `.venv\Scripts\python.exe .agents/skills/content-to-course/check_templates.py courses/asyntotic_estatistics_v4/work/templates/Hab-06.json --cta courses/asyntotic_estatistics_v4/work/cta.json --strict`
   - Verifica en `test_real_hab06_template_instantiation_and_invariants` que `Hab-06.json` ahora contiene los 4 arquetipos (`len(tpl_data["templates"]) == 4`) y que los 4 instancian preguntas válidas sin errores de invariantes ni de KaTeX.

### C. Verificación Global de Regresión
- Ejecuta las 6 suites de la etapa:
  `.venv\Scripts\python.exe -m pytest tests/test_forensic_shard06_and_variance_v34.py tests/test_assemble_katex_and_rationale.py tests/test_shard06_and_dry_archetypes.py tests/test_dispatch_turn0_and_milestone3_prompts.py tests/test_hook_post_pass_and_write_isolation.py tests/test_prompts_contract_alignment.py`
- Verifica `git status --short` para asegurar que no quede ningún archivo temporal.

## 3. Protocolo de Ejecución y Cierre
1. Antes de editar, escribe `.agents/teamwork/c2c_v34_variance_and_shard06/stream_2a_impr/BRIEFING.md`.
2. Al finalizar con `0` errores, escribe `.agents/teamwork/c2c_v34_variance_and_shard06/stream_2a_impr/handoff.md`.
3. Envía un mensaje con `send_message` a `526cfac0-d37b-49c9-bf09-00b5c520add2` con prefijo `DONE::` resumiendo tus mejoras y el conteo de tests.
