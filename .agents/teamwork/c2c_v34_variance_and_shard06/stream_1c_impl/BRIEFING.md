# Pre-Flight Sanity Check: Stream 1C Implementer (`impl_1c`)

- **Fecha:** 2026-10-24
- **Agente:** Implementador Stream 1C (`impl_1c`)
- **Orquestador:** `526cfac0-d37b-49c9-bf09-00b5c520add2`
- **Frontera Exclusiva de Escritura:**
  1. `.agents/skills/content-to-course/dispatch.py`
  2. `.agents/skills/content-to-course/system_prompts/lean/prompt_shard_author.md`
  3. `.agents/skills/content-to-course/system_prompts/prompt_shard_author.md`
  4. `.agents/skills/content-to-course/system_prompts/lean/prompt_repair.md`
  5. `.agents/skills/content-to-course/system_prompts/prompt_repair.md`
  6. `tests/test_dispatch_turn0_and_milestone3_prompts.py`
  7. `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1c_impl/BRIEFING.md`
  8. `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1c_impl/handoff.md`

---

## 1. Verificación de Código Real y Firmas

### A. `dispatch.py`
- **`dispatch_authors` (L980–L1135):**
  - Actualmente itera sobre `c_ids` en `shards/pre_shard_manifest.json` y extrae `c_obj` desde `cta.json`.
  - Construye `comp_blocks` formateando `distractors` (`wrong_belief`, `omitted_step`, `common_misconception_warning`), pero omite `correct_belief`, `manifestation` y `remediation_hint`.
  - En la cabecera de la orden `work_order` (L1082–L1093), menciona "cubre los 4 arquetipos" pero no declara explícitamente la autosuficiencia Turn-0 (cero lectura de PDFs) ni detalla el formato DRY compacto de distractores heredados desde `cta.json`.
- **`dispatch_repair` (L1560–L1690):**
  - Limpia archivos en `.check_attempts/` que coincidan con `shard_id` o `cid` (L1628–L1639).
  - Actualmente elimina archivos que contienen `norm_s_id`, `norm_cid`, `shard_id`, `cid` (como `compile_<shard>.json` o `circuit_breaker_<shard>.json`), pero debe asegurar la eliminación explícita de `pass_<shard_id>.json` y cualquier `pass_*` asociado al shard para evitar que la guarda Post-PASS bloquee a `c2c_repair`.

### B. Prompts de Autor y Reparación (`prompt_shard_author.md`, `prompt_repair.md`)
- **`system_prompts/lean/prompt_shard_author.md`:**
  - Tamaño actual: 4,707 bytes (debe mantenerse strictly `<= 5,120` bytes y preferentemente `<= 4,750` bytes para cumplir `test_lean_author_prompt_headroom_under_4750_bytes`).
  - Requiere: armonización con Milestone 3 (4 arquetipos disjuntos, formato DRY compacto de distractores, directriz Turn-0 autosuficiente y corte inmediato Post-PASS con `DONE:`).
- **`system_prompts/prompt_shard_author.md`:**
  - Requiere: armonización con Milestone 3 sin romper invariantes de tests existentes (`1 tupla paramétrica por competencia` vs `4 arquetipos disjuntos`, tokens `@var@`, no `rf"..."`, longitud balanceada de opciones, `shard_fixes/`, prohibición de `ArtifactMetadata`).
- **`system_prompts/lean/prompt_repair.md` & `system_prompts/prompt_repair.md`:**
  - `lean/prompt_repair.md` actual: 1,658 bytes. Actualizar para documentar el formateo de distractores, reparación de `R-20`, `error_rationale` y corte Post-PASS manteniendo `<=` 5,000 bytes.
  - Crear `prompt_repair.md` (versión completa) con las especificaciones de reparación quirúrgica, uso de `shard_fixes/<CID>.py`, y formato DRY.

### C. Invariantes de Tests Existentes
- `tests/test_prompts_contract_alignment.py`: 12 tests pasando. Exige tamaño de prompts lean <= 5,120 bytes, author lean <= 4,750 bytes, `ArtifactMetadata` prohibido, ausencia de `rf"..."` y `{{{`, ejecución de ejemplos H-01 y H-02 con 50 semillas sin errores.
- `tests/test_c2c_v321_comp3_dispatch.py`: 6 tests pasando. Exige que `dispatch_authors` inyecte contexto Turn-0 y que `generate_define_subagent_specs` mantenga los tipos esperados.
- `tests/test_c2c_v321_comp4_prompts.py`: 8 tests pasando. Exige presencia de "1 tupla por competencia" (o compatible), tokens KaTeX, etc.

---

## 2. Plan de Modificaciones

1. **`dispatch.py`:**
   - Inyectar `correct_belief` en la cabecera de la competencia en `dispatch_authors` si existe.
   - En cada distractor `D-XX-01..06`: incluir `wrong_belief`, `omitted_step`, `manifestation` (si presente) y `remediation_hint` (si presente).
   - En `work_order` de `dispatch_authors`: agregar directriz `"AUTOSUFICIENCIA TURN-0 (CERO LECTURA INNECESARIA DE PDFs)"` y explicitar los 4 arquetipos disjuntos con formato DRY de distractores `("D-XX-01", f"...")` o `{"distractor_id": "D-XX-01", "value": f"..."}` y corrección quirúrgica con `edit_file`.
   - En `dispatch_repair`: en la limpieza de `.check_attempts/`, asegurar que se limpie `pass_{shard_id}.json` y cualquier `pass_{norm_s_id}*.json`.
2. **Prompts:**
   - Actualizar `system_prompts/lean/prompt_shard_author.md` (garantizando peso <= 4,750 bytes).
   - Actualizar `system_prompts/prompt_shard_author.md`.
   - Actualizar `system_prompts/lean/prompt_repair.md` (garantizando peso <= 5,000 bytes).
   - Crear `system_prompts/prompt_repair.md` (versión completa).
3. **Tests:**
   - Crear `tests/test_dispatch_turn0_and_milestone3_prompts.py` cubriendo todas las nuevas especificaciones.
4. **Verificación:**
   - Ejecutar la suite completa de tests relevantes con `.venv\Scripts\python.exe -m pytest`.
