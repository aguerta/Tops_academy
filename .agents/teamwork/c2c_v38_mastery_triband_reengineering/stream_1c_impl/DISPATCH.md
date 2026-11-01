# DISPATCH — Stream 1C (Fase 1: Implementador)

- **Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1c_impl`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\plan_shards.py`
2. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\dispatch.py`
3. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\subagent_types.json`
4. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\system_prompts\*.md` (los archivos `.md` existentes en `system_prompts/`)
5. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\system_prompts\lean\*.md` (los archivos `.md` existentes en `system_prompts/lean/`)
6. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_dispatch_turn0_and_milestone3_prompts.py`
7. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_c2c_v321_comp4_prompts.py`
8. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_c2c_v321_comp3_dispatch.py`
9. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_weighted_sharding_m7.py`
10. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_skill_v3.py`
11. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_orchestration_resilience.py`
12. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1c_impl\BRIEFING.md` `[NEW]`
13. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1c_impl\handoff.md` `[NEW]`

PROHIBIDO modificar cualquier otro archivo.

## Reglas Pre-Flight y Trampas Críticas de Bytes/LF
- **Hooks:** Prohibido ejecutar `dispatch.py --help` / `run.py --help` o `python -c` mencionando `"content-to-course/"` junto con `open(`, `read_text`, `run.py`, `prepare.py`, `ingest.py`, `dispatch.py`. Usa `read_file` y `& ".venv\Scripts\python.exe" -m pytest <archivos_test> -q`.
- **Zero-Domain (`test_skill.py`):** En `plan_shards.py` y `dispatch.py` (cualquier `.py` de `content-to-course/`), PROHIBIDO incluir (ni en comentarios ni en strings) las subcadenas en minúsculas: `edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`. ¡Cuidado en español con `puedo`, `quedo`, `heredo` (`edo`) o `regresión` (`regresi`)!
- **Paridad Byte-a-Byte LF de `subagent_types.json` y Presupuestos `lean/`:**
  - `system_prompts/lean/prompt_shard_author.md` DEBE pesar **`<= 4,750` bytes UTF-8** (con saltos LF `\n`, cero `\r\n`).
  - Todos los demás `system_prompts/lean/*.md` DEBEN pesar **`<= 5,000` bytes UTF-8** (LF `\n`).
  - `subagent_types.json` DEBE guardarse con **LF `\n` exacto (cero `\r\n`)**, manteniendo `len == 4` tipos base (`c2c_cta_architect`, `c2c_shard_author`, `c2c_judge`, `c2c_repair`) e idéntico byte-a-byte a `json.dumps(dispatch.get_type_definitions(lean=False), indent=2, ensure_ascii=False) + "\n"`.
  - En `generate_define_subagent_specs(work_dir)`: mantener `len(result["types"]) == 4` (requerido por `test_dispatch_scope.py`), mientras se sigue escribiendo `c2c_cta_harmonizer.json` como 5.º archivo en `work/dispatch/types/`.
  - En `prompt_shard_author.md` (raíz y `lean/`), conservar las cadenas requeridas por suites externas: `"## 0. SCOPE-LOCK"`, `"DONE:"`, `"compile_shard.py"`, `"Física"`, `"Sistemas Distribuidos"`, `"línea"`.

## Especificación Técnica

### 1. `plan_shards.py`
- Actualizar `DSL_REFERENCE` (conservando las claves del diccionario/estructura requeridas por `test_weighted_sharding_m7.py`) al contrato `Form-B` Tri-Banda (`min_archetypes = 3`), mostrando:
  - 9-tupla `(tpl_id, cid, qtype, gen_fn, ver_fn, (difficulty, bloom), stems, hints, solution)`;
  - cobertura Tri-Banda `("easy", ...)`, `("medium", ...)`, `("hard", ...)` y práctica activa `FIB` (sin `$` externos) / `MS` / `MC7`;
  - distractores `MC7` como **3-tuplas obligatorias `(did, val, rationale_con_@var@)`** (`len >= 20`) y opciones falsas `MS` con `"error_rationale"` interpolando `@var@`;
  - `ver_fn` real no trivial y `>= 3` `stems` / `3..5` `hints` (`>= 25` chars).

### 2. `dispatch.py`
- **`dispatch_authors()`:**
  - Cambiar `"min_archetypes": 3` y el comando de compilación a `--strict --min-archetypes 3`.
  - Instruir el contrato `Form-B` Tri-Banda Multimodal (`easy` + `medium` + `hard`, `>= 2` niveles Bloom, `>= 2` plantillas `FIB`/`MS` en `Hab-*`, `>= 1` `FIB`/`MS` en `C-*`/`H-*`).
  - **Ordenar explícitamente 3-tuplas `(did, val, error_rationale_con_@var@)`** (`[TPL-DYNAMIC-RATIONALE]`), eliminando la vieja instrucción que decía omitir `error_rationale` y eliminando el mal ejemplo `r"$\text{Avar} = @d1@$"`. Prohibir `\text{...} > 45` chars (`[KATEX-PROSE-OVERFLOW]`).
- **`dispatch_cta_reduce()` + subcomando CLI `dispatch-cta-reduce`:**
  - Soportar Pointer Mode escribiendo `work/dispatch/items/cta_reduce_01.json` (y asegurando `work/dispatch/types/c2c_cta_harmonizer.json`), usando `"TypeName": "c2c_cta_harmonizer"` (corrigiendo cualquier typo previo).
  - Instruir deduplicación semántica sobre TODO `work/cta_outline.json` (no solo `duplicate_candidates.json`), soporte de absorción hacia nodos `[BASE]` (`read_only_base: true`) cuando exista `delta_manifest.json` (`--append`), y uso de `add_prerequisites` hasta garantizar `connected_components == 1` y `root_ratio <= 0.20`, emitiendo `"duplicate_decisions"` + `"add_prerequisites"` en `work/cta_harmonize.json`.
- **`dispatch_repair()` / `dispatch-repair`:**
  - Acumular TODAS las discordancias/razones por competencia desde `judge_report.json` (`failed_templates`, `failed_competencies`, `disagreements`) en bullets diagnósticos completos, e instruir compilación con `--strict --min-archetypes 3`.

### 3. `system_prompts/` (`lean/` y raíz) + `subagent_types.json`
- Actualizar `prompt_shard_author.md` (raíz y `lean/ <= 4,750 B` LF) y `prompt_repair.md` (raíz y `lean/ <= 5,000 B` LF):
  - Contrato único `Form-B` Tri-Banda (`easy`/`medium`/`hard`, `>= 2` Bloom, `FIB`/`MS` obligatorio), 3-tupla `(did, val, rationale_@var@)` con interpolación obligatoria `@var@`, `FIB` sin `$` externos, `ver_*` real (prohibido `return True`), `>= 3` stems y `3..5` hints socráticos `>= 25` chars, cero `\text{...} > 45` chars.
- Actualizar `prompt_cta_architect.md` (raíz y `lean/ <= 5,000 B` LF):
  - Erradicar ejemplos de prosa dentro de `\text{...}` (`> 45` chars falla en Stage 1 con `[KATEX-PROSE-OVERFLOW]`), exigir prosa fuera de `$...$` y DAG conexo (`connected_components == 1`, `root_ratio <= 0.20`).
- Actualizar `prompt_cta_harmonizer.md` (raíz y `lean/ <= 5,000 B` LF):
  - Instruir fusión semántica libre sobre todo `cta_outline.json`, soporte de nodos `read_only_base: true` (`[BASE]`) en `--append` y cierre de islas con `add_prerequisites` (`connected_components == 1`, `root_ratio <= 0.20`).
- Regenerar `subagent_types.json` en LF `\n` puro (`0` `\r\n`) coincidiendo exactamente con `dispatch.get_type_definitions(lean=False)`.

### 4. Actualización y Ampliación de las 6 Suites de Tests Exclusivas
Actualiza y amplía las 6 suites verificando `min_archetypes == 3`, Pointer Mode de `dispatch-cta-reduce` (`TypeName == "c2c_cta_harmonizer"`), agregación multi-fallo en `dispatch-repair`, presupuestos `<= 4,750 B` / `<= 5,000 B` en `lean/*.md`, LF puro en `subagent_types.json`, y presencia de las reglas Tri-Banda + `[TPL-DYNAMIC-RATIONALE]` + `[KATEX-PROSE-OVERFLOW]`.

## Verificación
Ejecuta:
```powershell
& ".venv\Scripts\python.exe" -m pytest tests/test_dispatch_turn0_and_milestone3_prompts.py tests/test_c2c_v321_comp4_prompts.py tests/test_c2c_v321_comp3_dispatch.py tests/test_weighted_sharding_m7.py tests/test_skill_v3.py tests/test_orchestration_resilience.py -q
```
Escribe `BRIEFING.md` antes de editar, `handoff.md` al terminar y notifica a `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589` con `DONE:: Stream 1C Impl completado (<N> passed)`.
