# DISPATCH — Stream 1C (Fase 2: Mejorador)

- **Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1c_impr`
- **Impl Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1c_impl\handoff.md`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\plan_shards.py`
2. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\dispatch.py`
3. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\subagent_types.json`
4. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\system_prompts\*.md`
5. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\system_prompts\lean\*.md`
6. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_dispatch_turn0_and_milestone3_prompts.py`
7. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_c2c_v321_comp4_prompts.py`
8. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_c2c_v321_comp3_dispatch.py`
9. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_weighted_sharding_m7.py`
10. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_skill_v3.py`
11. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_orchestration_resilience.py`
12. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1c_impr\handoff.md` `[NEW]`

PROHIBIDO tocar cualquier otro archivo.

## Objetivos de Endurecimiento (Fase 2 — Mejorador)
1. Lee `stream_1c_impl/handoff.md` y revisa con `read_file` los cambios en `plan_shards.py`, `dispatch.py`, `subagent_types.json`, `system_prompts/{lean/,}*.md` y las 6 suites de tests.
2. **Invariantes Críticos de Paridad LF, Bytes y Contratos Externos (Gate 2 & Gate 3):**
   - **LF en `subagent_types.json` y `system_prompts/**/*.md`:** verifica en un test explícito leyendo `.read_bytes()` que `subagent_types.json` y todos los `.md` de `system_prompts/` y `system_prompts/lean/` contengan **`0` ocurrencias de `b"\r\n"`** (LF `\n` puro). *(Ojo: `edit_file` en Windows puede introducir CRLF si el archivo tenía CRLF o si no se reescribe con LF; asegúrate de que `subagent_types.json` sea idéntico byte-a-byte a `(json.dumps(dispatch.get_type_definitions(lean=False), indent=2, ensure_ascii=False) + "\n").encode("utf-8")`)*.
   - **Presupuestos Lean estrictos:**
     - `len(Path(".../system_prompts/lean/prompt_shard_author.md").read_bytes()) <= 4750`
     - Todos los demás `system_prompts/lean/*.md` `<= 5000` bytes.
   - **Strings obligatorios para suites externas (`test_dispatch_scope.py` y `test_prompts_contract_alignment.py`):**
     - `prompt_shard_author.md` (raíz y `lean/`): contiene `"## 0. SCOPE-LOCK"`, `"DONE:"`, `"compile_shard.py"`, `"Física"`, `"Sistemas Distribuidos"`, `"línea"`.
     - `generate_define_subagent_specs(tmp_dir)`: retorna `len(res["types"]) == 4`, mientras escribe los 5 archivos `.json` en `tmp_dir / "dispatch" / "types"` incluyendo `c2c_cta_harmonizer.json`.
3. **Alineación Inter-Stream con `1A` (`cta_merge.py`), `1B` (`compile_shard.py`) y `1F` (`judge.py`):**
   - Confirma que `dispatch_cta_reduce(work_dir, ...)` y el subcomando CLI `dispatch-cta-reduce` sean invocables tanto desde Python (`run.py` en `Stream 2A`) como por CLI, escribiendo `work/dispatch/items/cta_reduce_01.json` con `"TypeName": "c2c_cta_harmonizer"` e instruyendo el esquema exacto aceptado por `apply_harmonize` (`"duplicate_decisions"` con `decision: "merge"`, `keep_id`, `drop_id` — soportando IDs `[BASE]` de `read_only_base: true` en `--append` — y `"add_prerequisites"`).
   - Confirma que `dispatch_repair` / `dispatch-repair` consuma `failed_templates`, `failed_competencies` y `disagreements` de `judge_report.json` (`Stream 1F`) sin truncar al primer fallo, y emita `--strict --min-archetypes 3`.
   - Confirma **0 subcadenas Zero-Domain prohibidas** en `plan_shards.py` y `dispatch.py` (`edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`).

## Verificación
Ejecuta (sin usar `--help` sobre scripts de `content-to-course/` ni `python -c` leyendo `"content-to-course/"`):
```powershell
& ".venv\Scripts\python.exe" -m pytest tests/test_dispatch_turn0_and_milestone3_prompts.py tests/test_c2c_v321_comp4_prompts.py tests/test_c2c_v321_comp3_dispatch.py tests/test_weighted_sharding_m7.py tests/test_skill_v3.py tests/test_orchestration_resilience.py -q
```
Escribe `handoff.md` en `stream_1c_impr/` y envía `DONE:: Stream 1C Impr completado (<N> passed)` a `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`.
