# Pre-Flight Briefing — Stream 1C (Fase 1: Implementador)

- **Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1c_impl`
- **Fecha:** 2026-10-31

---

## 1. Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
Archivos de producción autorizados:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\plan_shards.py`
2. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\dispatch.py`
3. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\subagent_types.json`
4. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\system_prompts\*.md`
5. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\system_prompts\lean\*.md`

Archivos de tests autorizados:
6. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_dispatch_turn0_and_milestone3_prompts.py`
7. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_c2c_v321_comp4_prompts.py`
8. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_c2c_v321_comp3_dispatch.py`
9. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_weighted_sharding_m7.py`
10. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_skill_v3.py`
11. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_orchestration_resilience.py`

Documentación de Stream autorizada:
12. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1c_impl\BRIEFING.md`
13. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1c_impl\handoff.md`

---

## 2. Inspección de Archivos de Producción y Líneas Exactas

### A. `plan_shards.py`
- **Líneas 62–281 (`DSL_REFERENCE`):**
  - Contiene actualmente referencias a "Caso 2B: 4 arquetipos" y ejemplos antiguos con `multiple_choice_7_options`, `fill_in_the_blank`, `multiple_select`.
  - **Contrato objetivo:** Form-B Tri-Banda (`min_archetypes = 3`):
    - 9-tupla `(tpl_id, cid, qtype, gen_fn, ver_fn, (difficulty, bloom), stems, hints, solution)`.
    - Cobertura Tri-Banda: `("easy", ...)`, `("medium", ...)`, `("hard", ...)` con `>= 2` Bloom levels y práctica activa multimodal (`FIB` sin `$` externos, `MS`, `MC7`).
    - Distractores `MC7` como 3-tuplas obligatorias `(did, val, rationale_con_@var@)` con `len(rationale) >= 20`.
    - Opciones falsas `MS` con `"error_rationale"` interpolando `@var@`.
    - Verificadores reales no triviales (`return True` prohibido).
    - Mínimo 3 `stems` y 3..5 `hints` socráticos (`>= 25` caracteres cada uno).
  - **Preservación:** Conservar claves del diccionario requeridas por `test_weighted_sharding_m7.py`: `"orthogonal_tokens_raw_strings"`, `"tpl_var_mandatory"`, `"modular_per_comp_overrides"`.

### B. `dispatch.py`
- **Líneas 948–970 (`dispatch_authors`):**
  - Estampaba `min_archetypes = 4` en `shard_manifest_data`.
  - Línea 1133: Invocaba `compile_shard.py` con `--strict --min-archetypes 4`.
  - Líneas 1157–1166: Prompt instruía 4 arquetipos y omitir `error_rationale` vía herencia DRY, con mal ejemplo `r"$\text{Avar} = @d1@$"`.
  - **Contrato objetivo:**
    - Cambiar `min_archetypes = 3` y compilar con `--strict --min-archetypes 3`.
    - Instruir Form-B Tri-Banda Multimodal (`easy` + `medium` + `hard`, `>= 2` Bloom, `>= 2` plantillas `FIB`/`MS` en `Hab-*`, `>= 1` `FIB`/`MS` en `C-*`/`H-*`).
    - Ordenar explícitamente 3-tuplas `(did, val, error_rationale_con_@var@)` (`[TPL-DYNAMIC-RATIONALE]`).
    - Prohibir `\text{...} > 45` chars (`[KATEX-PROSE-OVERFLOW]`) y colocar prosa fuera de `$...$`.
- **Líneas 1515–1556 (`cta-reduce`):**
  - Actualmente `cta-reduce` estaba sólo como bloque en `build_dispatch`, sin función `dispatch_cta_reduce()` independiente.
  - Generaba `work/dispatch/items/cta_harmonize_01.json` sin soporte estructurado de pointer prompt ni aseguramiento de `c2c_cta_harmonizer.json`.
  - **Contrato objetivo:**
    - Crear `dispatch_cta_reduce(work_dir, pointer=True)` y subcomando CLI `dispatch-cta-reduce`.
    - Escribir `work/dispatch/items/cta_reduce_01.json` (asegurando `work/dispatch/types/c2c_cta_harmonizer.json`) con `"TypeName": "c2c_cta_harmonizer"`.
    - Instruir deduplicación semántica sobre todo `work/cta_outline.json`, soporte de absorción hacia nodos `[BASE]` (`read_only_base: true`) con `delta_manifest.json` (`--append`), y uso de `add_prerequisites` hasta garantizar `connected_components == 1` y `root_ratio <= 0.20`, emitiendo `"duplicate_decisions"` + `"add_prerequisites"` en `work/cta_harmonize.json`.
- **Líneas 1688–1697 y 1860–1863 (`dispatch_repair`):**
  - Actualmente solo leía `jr.get("disagreements")` de `judge_report.json`.
  - `compile_cmd` no incluía `--strict --min-archetypes 3`.
  - **Contrato objetivo:**
    - Acumular todas las discordancias y fallos por competencia desde `judge_report.json` (`failed_templates`, `failed_competencies`, `disagreements`) en bullets diagnósticos completos.
    - Asegurar que el comando de compilación instruya `--strict --min-archetypes 3`.

### C. `system_prompts/` y `system_prompts/lean/`
- **`prompt_shard_author.md` (raíz y `lean/`):**
  - Actualizar al contrato único Form-B Tri-Banda (`easy`/`medium`/`hard`, `>= 2` Bloom, `FIB`/`MS` obligatorio).
  - Distractores en 3-tupla `(did, val, rationale_@var@)` con interpolación `@var@` requerida (`[TPL-DYNAMIC-RATIONALE]`).
  - `FIB` sin `$` externos en el valor esperado (`answer_contract`).
  - Verificador real no trivial (prohibido `return True`).
  - `>= 3` stems y `3..5` hints socráticos `>= 25` chars.
  - Prohibido `\text{...} > 45` chars (`[KATEX-PROSE-OVERFLOW]`).
  - **Presupuesto estricto:** `lean/prompt_shard_author.md` DEBE pesar **`<= 4,750` bytes** con saltos LF `\n`.
  - Preservar cadenas requeridas por suites: `"## 0. SCOPE-LOCK"`, `"DONE:"`, `"compile_shard.py"`, `"Física"`, `"Sistemas Distribuidos"`, `"línea"`.
- **`prompt_repair.md` (raíz y `lean/`):**
  - Alinear con Form-B Tri-Banda y diagnósticos multi-fallo.
  - `lean/prompt_repair.md` DEBE pesar **`<= 5,000` bytes** (LF `\n`).
- **`prompt_cta_architect.md` (raíz y `lean/`):**
  - Erradicar ejemplos con `\text{...} > 45` chars en tuplas de distractores (reemplazar prosa dentro de `\text{...}` por texto normal fuera de `$...$`).
  - Exigir DAG conexo (`connected_components == 1`, `root_ratio <= 0.20`).
  - `lean/prompt_cta_architect.md` DEBE pesar **`<= 5,000` bytes** (LF `\n`).
- **`prompt_cta_harmonizer.md` (raíz y `lean/`):**
  - Instruir fusión semántica libre sobre todo `cta_outline.json`.
  - Soporte de nodos `read_only_base: true` (`[BASE]`) en `--append`.
  - Cierre de componentes desconectados e islas con `add_prerequisites` (`connected_components == 1`, `root_ratio <= 0.20`).
  - `lean/prompt_cta_harmonizer.md` DEBE pesar **`<= 5,000` bytes** (LF `\n`).
- **`subagent_types.json`:**
  - Regenerar idéntico byte-a-byte a `json.dumps(dispatch.get_type_definitions(lean=False), indent=2, ensure_ascii=False) + "\n"`.
  - Exactamente 4 tipos base (`c2c_cta_architect`, `c2c_shard_author`, `c2c_judge`, `c2c_repair`).
  - Guardar con LF `\n` puro (`0` `\r\n`).

### D. Suites de Tests (6 archivos autorizados)
- Actualizar `test_dispatch_turn0_and_milestone3_prompts.py` para validar `min_archetypes == 3`, `--min-archetypes 3`, Form-B Tri-Banda, 3-tupla `(did, val, rationale)`, y budget `<= 4,750 B`.
- Actualizar `test_c2c_v321_comp4_prompts.py` y `test_c2c_v321_comp3_dispatch.py` para validar `dispatch_cta_reduce`, `TypeName == "c2c_cta_harmonizer"`, Pointer Mode en `cta_reduce_01.json`, y multi-fallo en repair.
- Extender `test_weighted_sharding_m7.py`, `test_skill_v3.py`, y `test_orchestration_resilience.py` para verificar contratos actualizados.

---

## 3. Riesgos Detectados y Mitigaciones
1. **Regla Zero-Domain en `.py`:**
   - Palabras como `puedo`, `quedo`, `heredo`, `regresión`, `método` pueden colisionar con `edo`, `regresi`, etc.
   - Mitigación: Escribir comentarios en inglés limpio y verificar con `tests/test_skill.py`.
2. **Presupuesto de Bytes en `lean/prompt_shard_author.md` (`<= 4,750 B`):**
   - El archivo actual mide 4625 bytes. Cualquier adición de Form-B debe compensarse eliminando redundancias, manteniendo las cadenas requeridas (`## 0. SCOPE-LOCK`, `DONE:`, `compile_shard.py`, etc.).
3. **Paridad LF en `subagent_types.json`:**
   - En Windows, `write_text()` por defecto puede insertar CRLF si no se controla o si se usa el encoding estándar sin `newline="\n"`.
   - Mitigación: Usar `write_bytes(payload.encode("utf-8"))` asegurando que el string contenga únicamente `\n`.
4. **Disrupción de firmas existentes:**
   - `generate_define_subagent_specs(work_dir)` debe seguir retornando `len(result["types"]) == 4`.

---
Plan de ejecución trazado y verificado. Procedemos con la Fase de Implementación.
