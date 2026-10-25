# DISPATCH — Stream 1D (Fase 1: Implementador `impl_1d`)

## 1. Rol y Frontera Exclusiva de Escritura (`Exclusive Write Boundaries`)
Eres el **Implementador del Stream 1D** bajo `/flash-triad-orchestrator`.
- **Carpeta de Gobernanza:** `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1d_impl/`
- **Archivos de Producción Permitidos (ÚNICOS que puedes modificar):**
  1. `.agents/skills/content-to-course/dispatch.py`
  2. `.agents/skills/content-to-course/system_prompts/lean/prompt_cta_architect.md`
  3. `.agents/skills/content-to-course/system_prompts/prompt_cta_architect.md`
  4. `.agents/skills/content-to-course/system_prompts/lean/prompt_shard_author.md`
  5. `.agents/skills/content-to-course/system_prompts/prompt_shard_author.md`
  6. `.agents/skills/content-to-course/system_prompts/lean/prompt_repair.md`
  7. `.agents/skills/content-to-course/system_prompts/prompt_repair.md`
  8. `tests/test_dispatch_turn0_and_milestone3_prompts.py`
- **Artefactos de Gobernanza Permitidos:**
  - `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1d_impl/BRIEFING.md`
  - `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1d_impl/handoff.md`
- **PROHIBIDO** editar cualquier otro archivo del repositorio (no edites `subagent_types.json`; eso pertenece al Stream 2A en Gate 2). Nunca pases `ArtifactMetadata` a `write_file` o `edit_file`.

## 2. Paso 0 Obligatorio (*Pre-Flight Sanity Check*)
Antes de realizar cualquier edición:
1. Lee los 7 archivos de prompts/dispatch de tu frontera y `tests/test_dispatch_turn0_and_milestone3_prompts.py`.
2. Verifica las invariantes existentes en `tests/test_dispatch_turn0_and_milestone3_prompts.py` (en particular las frases requeridas y los límites de tamaño `lean/prompt_shard_author.md <= 4,750` bytes y todos los `lean/*.md <= 5,000` bytes).
3. Escribe `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1d_impl/BRIEFING.md` confirmando líneas y tamaños actuales en bytes. Si detectas un bloqueo fuera de tu frontera, detén ediciones y envía `BLOCKER:: <archivo:línea> | <causa> | <opciones>` al Orquestador (`7d2e6386-9933-4c70-9e50-a3cf214925f6`).

## 3. Especificación Técnica de Implementación

### A. Prompts de CTA (`lean/prompt_cta_architect.md` y `prompt_cta_architect.md`)
1. **Problema Raíz en `lean/prompt_cta_architect.md` (L14):**
   - Actualmente dice: `🚫 Incremental micro-edits; write entire module in ONE atomic write_file(Overwrite=True)`. Cuando se interrogó a los CTA Architects en `v5` sobre por qué reescribieron todo el archivo con `write_file`, citaron textualmente esa línea!
2. **Solución en `lean/prompt_cta_architect.md` (manteniendo tamaño `<= 5,000` bytes):**
   - En `WRITE permitted`: añadir `<work_dir>/cta_fixes/<cid>.py` (o `<work_dir>/cta_parts/cta_fixes/<cid>.py`).
   - Reemplazar la prohibición ambigua de L14 por:
     `🚫 Incremental creation with Append=True (Turn 1 creation must be ONE atomic write_file(Overwrite=True))`
     `🚫 Post-compile full write_file rewrite when errors < 6 (1..5 errors MUST use surgical edit_file / replace_file_content)`
   - En `## 3. EXECUTION FLOW`:
     - Explicitar la **Regla del Umbral Oficial `< 6` (`edit_file` vs `write_file`)**:
       - **Turn 1 (Initial Creation):** Emit full `COMPETENCIES = [...]` in ONE atomic `write_file(Overwrite=True)`.
       - **Post-Compile Repair (`< 6` errors, i.e., `1..5` errors):** Mandatory surgical `edit_file` (`replace_file_content`) in 1 parallel turn on the exact Python lines reported by `compile_cta.py` (`write_file` is blocked by hook guard when `errors < 6`).
       - **Post-Compile Repair (`>= 6` errors):** Write modular override `cta_fixes/<CID>.py` via `write_file(Overwrite=True)` (if localized to `1–2` competencies) or 1 full `write_file(Overwrite=True)` (if systemic across `>= 3` competencies or `SyntaxError`).
       - **Post-PASS Cut:** Upon `PASS`, stop all edits immediately and output `DONE: ...`.
3. **Solución en `prompt_cta_architect.md` (Full):**
   - En `## 0. SCOPE-LOCK` (`WRITE permitido`): añadir `<work_dir>/cta_fixes/<cid>.py` y `<work_dir>/cta_parts/cta_fixes/<cid>.py`. En `PROHIBIDO`: añadir `tests/**`, `git log` y `Get-ChildItem -Recurse` sobre `courses/`.
   - En `## 9. Protocolo de Creación Atómica y Límites de Edición` y `## 10. Resumen de Flujo de Ejecución Canónico`: documentar con total claridad el **Umbral Oficial `< 6` Errores (`edit_file` vs `write_file`)**:
     - `< 6` errores (`1..5` errores): obligatorio `edit_file` (`replace_file_content`) quirúrgico sobre las líneas exactas de `cta_data.py` / `part_XX_data.py` (bloqueado `write_file` completo por `c2c_hook_guard.py`).
     - `>= 6` errores: parche modular `cta_fixes/<CID>.py` (`1–2` competencias) o `write_file(Overwrite=True)` completo (`>= 3` competencias o `SyntaxError`).

### B. Prompts de Shard Author y Repair (`lean/prompt_shard_author.md`, `prompt_shard_author.md`, `lean/prompt_repair.md`, `prompt_repair.md`)
1. **Umbral Oficial `< 6` Errores (`edit_file` vs `write_file`):**
   - Tanto en `prompt_shard_author.md` (Full y Lean) como en `prompt_repair.md` (Full y Lean), sustituir el criterio antiguo basado solo en líneas (`<= 15 lines`) por el **Umbral Oficial `< 6` Errores**:
     - **`1..5` errores (`errores < 6`, sin `SyntaxError`):** Uso **OBLIGATORIO** de `edit_file` (`replace_file_content`) quirúrgico en 1 turno paralelo sobre las líneas exactas `StartLine..EndLine` de `<shard_id>_data.py`. Prohibido reescribir todo el archivo con `write_file`.
     - **`>= 6` errores acotados a `1–2` competencias:** Escribir bloque modular aislado en `<work_dir>/shards/shard_fixes/<CID>.py` con `write_file(Overwrite=True)`.
     - **`>= 6` errores sistémicos (`>= 3` competencias) o `SyntaxError`:** Permitido `write_file(Overwrite=True)` atómico completo o `shard_fixes/<CID>.py`.
2. **Dimensionamiento Compacto Clean-Room Anti-Bloat (`<= 80–110` líneas/competencia, `<= 180–220` líneas/shard):**
   - En `prompt_shard_author.md` (Full y Lean): mantener intactas las frases requeridas por los tests de Milestone 3 (`4 arquetipos disjuntos`, `1. Directo / Frontal`, `2. Inverso / Diagnóstico`, `3. Perturbación / Estática Comparativa`, `4. Frontera / Casos Límite`, `Formato DRY Compacto de Distractores`, `Autosuficiencia Turn-0 (Cero Lectura Innecesaria de PDFs)`, `Corte Inmediato Post-PASS` en Full; y `Milestone 3 (4 Disjoint Archetypes)`, `1. Directo, 2. Inverso, 3. Perturbación, 4. Frontera`, `DRY Compact Distractors`, `Turn-0 Autosufficiency`, `Post-PASS Cut` en Lean), pero especificar que cada función generadora debe ser **ultra-concisa (~12–18 líneas)** usando tuplas DRY de 2 elementos `("D-XX-01", r"$@d1@$")`, manteniendo el archivo en **`<= 80–110` líneas por competencia (`<= 180–220` líneas totales por shard)** y prohibiendo repetir párrafos de `error_rationale` o ensayos extensos dentro de `\text{...}`.
3. **Bloqueo Explícito de Fugas Pre-Compilación y Corrección de Manifiesto en Repair:**
   - En `PROHIBIDO` de `prompt_shard_author.md` y `prompt_repair.md` (Full y Lean): prohibir leer `tests/**`, ejecutar `git log` y listar `courses/` con `Get-ChildItem -Recurse`.
   - En `prompt_repair.md` (Full L60 y Lean L23): actualizar `--manifest <work>/pre_cta_manifest.json` a `--manifest <work>/shards/pre_shard_manifest.json`.
   - **Cota estricta de bytes:** Verificar que `lean/prompt_shard_author.md <= 4,750` bytes y todos los archivos en `system_prompts/lean/*.md <= 5,000` bytes.

### C. Actualización de `dispatch.py` (`ROLE_SPECS`, `dispatch_cta`, `dispatch_authors`)
1. En `ROLE_SPECS`:
   - Añadir `"work/cta_fixes/**"` y `"work/cta_parts/cta_fixes/**"` en `"write"` de `"cta"`, `"cta-direct"` y `"cta-map"`.
   - Añadir `"tests/**"` en `"forbidden"` de `"cta"`, `"cta-direct"`, `"cta-map"`, `"author"` y `"repair"`.
2. En `dispatch_cta` (modo `mapreduce` L604, L640 y modo `direct` L745, L781):
   - Añadir `f"{work_rel}/cta_fixes/<CID>.py"` (o `f"{work_rel}/cta_parts/cta_fixes/<CID>.py"`) a `write_paths`.
   - Actualizar la directiva 4 para explicitar el **umbral oficial `< 6` errores**:
     `4. Si el compilador reporta < 6 errores (1..5 errores), corrígelos OBLIGATORIAMENTE de forma quirúrgica con edit_file (replace_file_content) sobre {out_py} en 1 turno paralelo (PROHIBIDO write_file completo cuando hay < 6 errores). Si reporta >= 6 errores, usa cta_fixes/<CID>.py (1-2 comps) o write_file(Overwrite=True).`
3. En `dispatch_authors` (L1081–L1128):
   - Añadir `"tests/**"` en `forbidden_paths`.
   - En la instrucción 1 (L1119): cambiar `(<= 150-250 líneas por competencia, estándar Clean-Room shard_08)` por `(<= 80-110 líneas por competencia, <= 180-220 líneas totales por shard, funciones gen_* concisas de ~15 líneas)`.
   - En la instrucción 6 (L1127): explicitar el **umbral oficial `< 6` errores** conservando la subcadena `"NO reescribas todo el archivo desde cero con \`write_file\`"`:
     `6. Si reporta < 6 errores (1..5 errores), corrígelos OBLIGATORIAMENTE de forma quirúrgica con edit_file (replace_file_content) sobre las líneas exactas de {out_py}; si reporta >= 6 errores, escribe en {work_rel}/shards/shard_fixes/<CID>.py (1-2 comps) o reescribe con write_file. Para < 6 errores, NO reescribas todo el archivo desde cero con \`write_file\`.`

## 4. Verificación y Entrega
1. Amplía `tests/test_dispatch_turn0_and_milestone3_prompts.py` para verificar:
   - Que `dispatch_cta` (direct y mapreduce) y `dispatch_authors` inyectan la regla del umbral oficial `< 6` errores (`< 6 errores`, `edit_file`, `cta_fixes/<CID>.py` / `shard_fixes/<CID>.py`) y el nuevo límite compacto `<= 80-110 líneas por competencia`.
   - Que `prompt_cta_architect.md` (Full y Lean), `prompt_shard_author.md` (Full y Lean) y `prompt_repair.md` (Full y Lean) documentan el umbral `< 6` errores, que `lean/prompt_cta_architect.md` ya NO prohíbe `edit_file` en reparaciones, que `prompt_repair.md` referencia `pre_shard_manifest.json`, y que todos los tamaños en `lean/*.md` cumplen `<= 5,000` bytes (`lean/prompt_shard_author.md <= 4,750` bytes).
2. Ejecuta `.venv\Scripts\python.exe -m pytest tests/test_dispatch_turn0_and_milestone3_prompts.py tests/test_dispatch.py -q`.
3. Escribe `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1d_impl/handoff.md` y envía `DONE:: Stream 1D Implementer completado` a `7d2e6386-9933-4c70-9e50-a3cf214925f6`.
