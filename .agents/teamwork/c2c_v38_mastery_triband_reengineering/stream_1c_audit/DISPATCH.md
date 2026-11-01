# DISPATCH — Stream 1C (Fase 3: Auditor Forense Read-Only)

- **Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1c_audit`
- **Impl Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1c_impl\handoff.md`
- **Impr Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1c_impr\handoff.md`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1c_audit\audit_report.md` `[NEW]`

PROHIBIDO tocar cualquier archivo de producción o `tests/`.

## Protocolo de Auditoría Forense (Stream 1C)
*(Nota de concurrencia Gate 1: los Streams paralelos `1B` y `1D` siguen activos sobre sus fronteras disjuntas; `git status` mostrará cambios legítimos en sus archivos).*

1. **Higiene y Frontera de Stream 1C:**
   - Ejecuta `git status --short` y verifica cero scripts temporales sueltos ni `.c2c_subagent_lock.json` activos en el workspace, y que los archivos de `Stream 1C` se limiten a `plan_shards.py`, `dispatch.py`, `subagent_types.json`, `system_prompts/{lean/,}*.md` y sus 6 suites asignadas.
2. **Inspección de Código, Bytes LF y Contratos (`read_file` en bloques amplios):**
   - `plan_shards.py`: confirma `DSL_REFERENCE` actualizado a `Form-B` Tri-Banda (`min_archetypes = 3`), 3-tuplas `(did, val, rationale_@var@)` y `FIB`/`MS` sin romper claves esperadas por `test_weighted_sharding_m7.py`.
   - `dispatch.py`: confirma `"min_archetypes": 3` y `--min-archetypes 3`, instrucción obligatoria de 3-tuplas con `@var@` (`[TPL-DYNAMIC-RATIONALE]`), prohibición de `\text{...} > 45` chars, `dispatch_cta_reduce` + CLI `dispatch-cta-reduce` escribiendo `work/dispatch/items/cta_reduce_01.json` con `"TypeName": "c2c_cta_harmonizer"` (e instruyendo fusión libre + nodos `[BASE]` en `--append` + `connected_components == 1`), agregación multi-fallo en `dispatch-repair`, y `len(generate_define_subagent_specs(tmp)["types"]) == 4` + 5 archivos `.json` en `dispatch/types/`.
   - **Verificación estricta LF y Byte-Budget Lean:**
     - `subagent_types.json` tiene **0 bytes `\r\n`** (LF `\n` puro) y coincide exactamente con `dispatch.get_type_definitions(lean=False)`.
     - `system_prompts/lean/prompt_shard_author.md` pesa **`<= 4,750` bytes UTF-8** y todos los demás `system_prompts/lean/*.md` **`<= 5,000` bytes UTF-8**, todos en LF `\n` puro.
     - `prompt_shard_author.md` (raíz y `lean/`) preserva `"## 0. SCOPE-LOCK"`, `"DONE:"`, `"compile_shard.py"`, `"Física"`, `"Sistemas Distribuidos"`, `"línea"`.
   - Confirma **0 subcadenas Zero-Domain prohibidas** en `plan_shards.py` y `dispatch.py` (`edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`).
3. **Ejecución Independiente de Tests (incluyendo `test_dispatch_scope.py` de verificación cruzada):**
   ```powershell
   & ".venv\Scripts\python.exe" -m pytest tests/test_dispatch_turn0_and_milestone3_prompts.py tests/test_c2c_v321_comp4_prompts.py tests/test_c2c_v321_comp3_dispatch.py tests/test_weighted_sharding_m7.py tests/test_skill_v3.py tests/test_orchestration_resilience.py tests/test_dispatch_scope.py -q
   ```
4. Escribe `audit_report.md` en `stream_1c_audit/` y envía `PASS:: Stream 1C (<N> passed)` o `REJECT:: Stream 1C | <archivo:línea> | <causa>` a `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`.
