# DISPATCH — Stream 1D (Fase 2: Mejorador `impr_1d`)

## 1. Rol y Frontera Exclusiva de Escritura (`Exclusive Write Boundaries`)
Eres el **Mejorador (Fase 2) del Stream 1D** bajo `/flash-triad-orchestrator`.
- **Carpeta de Gobernanza:** `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1d_impr/`
- **Archivos de Producción Permitidos (ÚNICOS que puedes modificar):**
  1. `.agents/skills/content-to-course/compile_shard.py`
  2. `.agents/skills/content-to-course/system_prompts/prompt_shard_author.md`
  3. `.agents/skills/content-to-course/system_prompts/lean/prompt_shard_author.md`
  4. `tests/test_m3_archetypes_semantic_gate.py`
- **Artefactos de Gobernanza Permitidos:**
  - `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1d_impr/BRIEFING.md`
  - `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1d_impr/handoff.md`
- **PROHIBIDO** editar cualquier otro archivo del repositorio. Nunca pases `ArtifactMetadata` a `write_file` o `edit_file`.

## 2. Paso 0 Obligatorio (*Pre-Flight*)
1. Lee `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1d_impl/handoff.md`, `.agents/skills/content-to-course/compile_shard.py` (líneas 1640–1760), `.agents/skills/content-to-course/system_prompts/prompt_shard_author.md` (líneas 240–320), `.agents/skills/content-to-course/system_prompts/lean/prompt_shard_author.md` y `tests/test_m3_archetypes_semantic_gate.py`.
2. Escribe `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1d_impr/BRIEFING.md`.

## 3. Tareas de Endurecimiento (Hardening & Edge Cases)
1. En `compile_shard.py` (compuerta `[M3-ARCHETYPES]`):
   - **Caso Borde 1 — Modular Merging (`shard_fixes/<CID>.py`):** Si una competencia fue sobrescrita mediante un archivo modular `shard_fixes/<CID>.py`, el código fuente real de su función `_gen_*` proviene del archivo modular y no necesariamente del `source_text` original de `shard_XX_data.py` (o está en el `generator_code` compilado de las tuplas en `tpls`). Asegúrate de que la inspección AST de si `arch` es utilizado en `_gen_*` inspeccione el AST de `t.get("generator_code", "")` (o el módulo efectivo donde está definida `_gen_*`) para que el fix modular `shard_fixes/<CID>.py` también sea validado correctamente y nunca produzca falsos positivos si `shard_XX_data.py` tenía un `_gen_*` antiguo que fue reemplazado por `shard_fixes/<CID>.py`!
   - **Caso Borde 2 — Evasión Trivial (`_ = arch` o `arch == arch`):** Si una función `_gen_*(rng, arch=1)` intenta burlar el chequeo AST leyendo `arch` sin variar nada (o si 4 generadores sin argumento `arch` producen exactamente el mismo diccionario `(correct, vars)` en las semillas de prueba), verifica en `[M3-ARCHETYPES]` (cuando `strict_mode` y `eff_min_arch >= 4` y `len(tpls) >= 4`) ejecutando/comparando los resultados ya evaluados o mediante una corrida ligera en `seed=100` (o comparando el AST/salida) que las 4 tuplas de la competencia produzcan al menos **2 salidas distintas** `(correct, vars)` para una misma semilla, rechazando clones matemáticos puros donde las 4 tuplas devuelven exactamente el mismo `correct` y `vars`!
2. Amplía `tests/test_m3_archetypes_semantic_gate.py` con tests adversarios para:
   - Un shard donde `_gen_h01(rng, arch=1)` incluye un dummy `_ = arch` pero devuelve exactamente el mismo `vars` y `correct` en las 4 tuplas -> rechazado por `[M3-ARCHETYPES]`.
   - Un shard roto que es reparado mediante `shard_fixes/H-01.py` con 4 arquetipos genuinos -> aprueba `PASS` limpiamente.
3. Ejecuta `.venv\Scripts\python.exe -m pytest tests/test_m3_archetypes_semantic_gate.py tests/test_shard06_and_dry_archetypes.py tests/test_compile_shard.py tests/test_shard_compiler_hardening.py -q`.
4. Escribe `.agents/teamwork/c2c_v36_sandbox_repair_and_archetypes/stream_1d_impr/handoff.md` y envía `DONE:: Stream 1D Improver completado` a `d603756a-7e58-4466-b883-cbc391586154`.
