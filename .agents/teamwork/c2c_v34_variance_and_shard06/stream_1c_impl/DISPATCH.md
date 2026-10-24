# DISPATCH — Stream 1C (Fase 1: Implementador `impl_1c`)

## 1. Rol y Frontera Exclusiva de Escritura (`Exclusive Write Boundaries`)
Eres el **Implementador del Stream 1C** bajo `/flash-triad-orchestrator`.
- **Carpeta de Gobernanza:** `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1c_impl/`
- **Archivos de Producción Permitidos (ÚNICOS que puedes modificar):**
  1. `.agents/skills/content-to-course/dispatch.py`
  2. `.agents/skills/content-to-course/system_prompts/lean/prompt_shard_author.md`
  3. `.agents/skills/content-to-course/system_prompts/prompt_shard_author.md`
  4. `.agents/skills/content-to-course/system_prompts/lean/prompt_repair.md`
  5. `.agents/skills/content-to-course/system_prompts/prompt_repair.md`
  6. `tests/test_dispatch_turn0_and_milestone3_prompts.py` *(nuevo archivo de tests unitarios)*
- **Artefactos de Gobernanza Permitidos:**
  - `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1c_impl/BRIEFING.md`
  - `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1c_impl/handoff.md`
- **PROHIBIDO** editar cualquier otro archivo del repositorio (no edites `subagent_types.json`; eso corresponde a la Etapa 2).

## 2. Paso 0 Obligatorio (*Pre-Flight Sanity Check*)
Antes de realizar cualquier edición:
1. Lee `.agents/skills/content-to-course/dispatch.py` (especialmente `dispatch_authors` L980–L1135 y `dispatch_repair` L1560–L1690) y los 4 archivos de prompts dentro de tu frontera (`system_prompts/lean/prompt_shard_author.md`, `system_prompts/prompt_shard_author.md`, `system_prompts/lean/prompt_repair.md`, `system_prompts/prompt_repair.md`).
2. Lee también (solo lectura) `tests/test_prompts_contract_alignment.py` y `tests/test_c2c_v321_comp4_prompts.py` para conocer todas las invariantes que los tests existentes exigen sobre esos archivos de prompts (como el límite de tamaño `<= 5 KB` en `system_prompts/lean/*.md` y palabras clave requeridas).
3. Escribe `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1c_impl/BRIEFING.md`. Si encuentras cualquier bloqueo fuera de tu frontera, detén ediciones y envía `BLOCKER:: <archivo:línea> | <causa> | <opciones>` al Orquestador (`526cfac0-d37b-49c9-bf09-00b5c520add2`).

## 3. Especificación Técnica de Implementación (100% Agnóstica + Milestone 3)

### A. Contexto Matemático Turn-0 Completo y Directriz Anti-Lectura Innecesaria de PDFs en `dispatch.py`
1. **Inyección de `correct_belief`, `manifestation` y `remediation_hint` en `dispatch_authors` (`dispatch.py` L1012–L1028):**
   - Actualmente, al construir `comp_blocks` para `author_XX.json`, `dispatch_authors` solo formatea `wrong_belief` y `omitted_step`, omitiendo `correct_belief`, `manifestation` y `remediation_hint` de `cta.json`.
   - Actualiza el formateo de cada distractor `d` en `comp_blocks` para incluir:
     - `correct_belief` (si existe en el primer distractor o a nivel competencia, muéstralo una vez como `- Modelo/Fórmula Correcta Canónica (correct_belief): ...` en la cabecera de la competencia para no repetirlo 6 veces si es idéntico en los 6 distractores).
     - En cada distractor `D-XX-01..06`: mostrar `wrong_belief`, `omitted_step`, `manifestation` (si está presente) y `remediation_hint` (si está presente).
2. **Directriz Turn-0 Autosuficiente (100% Agnóstica al Dominio) en `author_XX.json` (`dispatch.py` L1075–L1095):**
   - En las instrucciones de `work_order` de `dispatch_authors`:
     - Indicar claramente: `"AUTOSUFICIENCIA TURN-0 (CERO LECTURA INNECESARIA DE PDFs): La Sección 2 de esta orden ya contiene el 100% de las definiciones, fórmulas canónicas (correct_belief), manifestaciones de error (manifestation) y distractores de cta.json. NO abras ni leas los documentos fuente de content/ en Turno 1; empieza directamente escribiendo <shard_id>_data.py."`
     - Armonizar las instrucciones #1 y #2 de `work_order` (L1083–L1085) con el **Milestone 3**:
       - Instruir explícitamente escribir los **4 arquetipos disjuntos por competencia** (`1. Directo / Frontal`, `2. Inverso / Diagnóstico`, `3. Perturbación / Estática Comparativa`, `4. Frontera / Casos Límite`) utilizando el **formato DRY compacto de distractores** `("D-XX-01", f"...")` o `{"distractor_id": "D-XX-01", "value": f"..."}` (donde `compile_shard.py` hereda automáticamente `error_rationale` desde `cta.json`), y exigiendo usar `edit_file` quirúrgico (nunca reescribir el archivo entero con `write_file`) si se requiere corregir un error tras compilar.
3. **Limpieza de `pass_<shard_id>.json` en `dispatch_repair` (`dispatch.py` L1625–L1642):**
   - En `dispatch_repair`, donde ya se limpian los archivos `.check_attempts/` para el shard/competencia a reparar, asegúrate de que también se elimine `pass_<shard_id>.json` (y cualquier `pass_*` asociado al shard), para que la guarda Post-PASS no bloquee al agente `c2c_repair`.

### B. Armonización de `prompt_shard_author.md` (Full + Lean) y `prompt_repair.md` (Full + Lean)
1. **En `system_prompts/lean/prompt_shard_author.md` y `system_prompts/prompt_shard_author.md`:**
   - Eliminar la frase ambigua `"1 tupla por competencia (o 4 arquetipos disjuntos)"` y establecer con claridad la regla **Milestone 3**: **4 arquetipos disjuntos por competencia** (`1. Directo`, `2. Inverso`, `3. Perturbación`, `4. Frontera`).
   - Mostrar cómo escribir los arquetipos de manera **ultra-compacta (DRY)**: en la lista `dists` de cada función `gen_*`, basta pasar tuplas `("D-C01-01", f"$...$")` o dicts `{"distractor_id": "D-C01-01", "value": f"$...$"}` sin repetir los 6 párrafos de `error_rationale` en cada arquetipo (pues `compile_shard.py` los inyecta automáticamente desde `cta.json`, aunque se permite pasar `"error_rationale"` explícito si se desea personalizar).
   - Añadir la regla de **Autosuficiencia Turn-0** (no leer PDFs de `content/` porque `author_XX.json` ya contiene `correct_belief`, `manifestation` y los 6 distractores) y la regla de **Corte Inmediato Post-PASS** (al obtener `[+] PASS`, emitir `DONE:` inmediatamente sin hacer ediciones adicionales).
   - Preservar **todas** las reglas existentes requeridas por los tests (`r"..."` con `@var@` / `@var:fmt@`, prohibición de `rf"..."` y `{{{`, `stem_variants` de 3–5 variantes, `shard_fixes/<CID>.py`, prohibición de `ArtifactMetadata`, y tamaño de `lean/prompt_shard_author.md <= 5000` bytes).
2. **En `system_prompts/lean/prompt_repair.md` y `system_prompts/prompt_repair.md`:**
   - Documentar que para reparar `[R-20]` o `error_rationale` pueden definir explícitamente `"error_rationale": r"..."` en el distractor afectado o usar `shard_fixes/<CID>.py` con `edit_file` quirúrgico, y mantener `lean/prompt_repair.md <= 5000` bytes.

## 4. Verificación y Entrega
1. Crea `tests/test_dispatch_turn0_and_milestone3_prompts.py` verificando:
   - Que `dispatch_authors` inyecte `correct_belief`, `manifestation` y `remediation_hint` en `author_XX.json` y la directriz de no leer PDFs en Turno 1.
   - Que `dispatch_repair` elimine `.check_attempts/pass_<shard_id>.json` cuando exista.
   - Que `prompt_shard_author.md` (Full + Lean) especifique los 4 arquetipos del Milestone 3 con formato DRY de distractores y que todos los archivos en `system_prompts/lean/*.md` pesen `<= 5000` bytes.
2. Ejecuta `.venv\Scripts\python.exe -m pytest tests/test_dispatch_turn0_and_milestone3_prompts.py tests/test_prompts_contract_alignment.py tests/test_c2c_v321_comp3_dispatch.py tests/test_c2c_v321_comp4_prompts.py`.
3. Escribe `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1c_impl/handoff.md` y envía `DONE:: Stream 1C Implementer completado` a `526cfac0-d37b-49c9-bf09-00b5c520add2`.
