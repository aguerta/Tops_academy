# Handoff — Stream 1D (Phase 2: Improver `impr_1d`)

## 1. Resumen Ejecutivo
Como Mejorador (Phase 2 Improver) del Stream 1D (**Prompts & Dispatch Sweet-Spot + Milestone 3 Anti-1-Tuple Hardening**), se completó la auditoría y endurecimiento técnico de los artefactos de prompt y despacho para erradicar definitivamente las 3 causas raíz que permitieron a ciertos shards emitir 1 tupla en lugar de 4 arquetipos disjuntos o escribir 400–470 líneas redundantes.

## 2. Acciones y Mejoras Implementadas

### A. Eliminación del Escape Hatch y Patrón Compacto en Prompts
1. **`prompt_shard_author.md` (Full):**
   - Eliminada la frase permisiva `"(o 1 tupla por competencia en casos de evaluación atómica básica)"`.
   - Introducida la regla obligatoria `[M3-ARCHETYPES]`: cada competencia debe definir obligatoriamente $\ge 4$ tuplas en `TEMPLATES` (1. Directo, 2. Inverso, 3. Perturbación, 4. Frontera). Se prohíbe emitir 1 sola tupla o agrupar variantes dentro de una tupla.
   - Refactorizado el `Ejemplo 1 (H-01)` al **Patrón Compacto de 4 Arquetipos** (~50–65 líneas/competencia):
     - Helper compartido `def _gen_h01(rng, arch=1):` que computa variables y ramifica por arquetipo.
     - 4 wrappers de 1 línea: `gen_h01_1(rng)`, `gen_h01_2(rng)`, `gen_h01_3(rng)`, `gen_h01_4(rng)`.
     - Verificador auto-contenido `ver_h01(res)` asegurando compatibilidad en ejecución sandboxed de cross-check.
     - 4 tuplas compactas en `TEMPLATES` con 6 distractor IDs en tupla 0 y `[]` en tuplas 1..3 aprovechando la auto-herencia desde `cta.json`.
2. **`lean/prompt_shard_author.md`:**
   - Actualizado para documentar `[M3-ARCHETYPES]` y el patrón compacto `_gen_h01(rng, arch=1)` + `gen_h01_1..4` + 4 tuplas.
   - Optimización de prosa redundante para cumplir holgadamente la cota presupuestaria:
     - **Tamaño final: 4,725 bytes** (límite estricto: $\le 4,750$ bytes; margen: 25 bytes).
     - Conservadas todas las subcadenas requeridas por las suites de contrato (`test_prompts_contract_alignment.py`, `test_c2c_v321_comp4_prompts.py`).

### B. Endurecimiento de `dispatch.py` (`dispatch_authors`)
1. **Estampado de Manifiesto:**
   - Al cargar `pre_shard_manifest.json`, `dispatch_authors` estampa `"min_archetypes": 4` a nivel raíz y en cada shard dentro de `manifest_data["shards"]` si no estaba previamente fijado.
   - Persiste de inmediato a disco con formato legible (`ensure_ascii=False`, `indent=2`).
2. **Bandera de Compilación `--min-archetypes 4`:**
   - Inyectado `--min-archetypes 4` en `compile_cmd`:
     `{venv_py} .agents/skills/content-to-course/compile_shard.py {shard_py_rel} --work {work_rel} --shard {shard_id} --strict --min-archetypes 4`
3. **Instrucción 2 al Shard Author:**
   - Actualizada para exigir de forma imperativa `4 Arquetipos Disjuntos OBLIGATORIOS por Competencia ([M3-ARCHETYPES])` indicando el uso del patrón helper `_gen_<cid>(rng, arch)` + 4 wrappers para mantener el código en ~55–75 líneas por competencia.

### C. Cobertura de Pruebas Unitarias
- Ampliada la suite `tests/test_dispatch_turn0_and_milestone3_prompts.py` con `test_stream_1d_improver_milestone3_archetypes_and_dispatch_hardening`:
  - Verifica la ausencia de `"(o 1 tupla por competencia"` en `prompt_shard_author.md`.
  - Verifica la presencia de `[M3-ARCHETYPES]` y `_gen_h01` en `prompt_shard_author.md`.
  - Verifica `[M3-ARCHETYPES]`, `gen_h01_1`..`gen_h01_4` y cota $\le 4,750$ bytes en `lean/prompt_shard_author.md`.
  - Verifica `--min-archetypes 4` en `compile_cmd` y presencia de `[M3-ARCHETYPES]` en las directivas de `dispatch_authors`.
  - Verifica el estampado persistido de `"min_archetypes": 4` en `pre_shard_manifest.json`.

## 3. Verificación de Resultados de Pruebas
Ejecución de la batería completa asociada al stream:
- `tests/test_dispatch_turn0_and_milestone3_prompts.py`: 13 passed
- `tests/test_dispatch_scope.py`: 10 passed
- `tests/test_prompts_contract_alignment.py`: 16 passed
- `tests/test_c2c_v321_comp4_prompts.py`: 5 passed
**Total: 44 passed in 1.64s (100% éxito)**

## 4. Normalización e Integridad
- Formato de saltos de línea normalizado a LF (sin presencia de `\r`) en todos los archivos modificados.
- Frontera de escritura 100% respetada.
- No se modificó `subagent_types.json` ni archivos fuera del boundary del Stream 1D.
