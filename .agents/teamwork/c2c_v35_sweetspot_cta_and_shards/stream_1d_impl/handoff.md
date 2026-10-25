# Handoff — Stream 1D (Fase 1: Implementador `impl_1d`)

**Fecha/Hora:** 2026-10-24T20:48:00-05:00  
**Emisor:** `impl_1d` (Fase 1 Implementador)  
**Receptor:** `mej_1d` (Fase 2 Mejorador) y Orquestador (`7d2e6386-9933-4c70-9e50-a3cf214925f6`)  
**Stream:** 1D — Prompts & Dispatch Sweet-Spot Updates  
**Estado:** COMPLETADO CON ÉXITO (`PASS` en suite completa)

---

## 1. Resumen Ejecutivo de Cambios Implementados

Dentro de la estricta **Frontera Exclusiva de Escritura** asignada en `DISPATCH.md`, se ejecutaron las siguientes mejoras arquitectónicas:

### A. Prompts de CTA (`lean/prompt_cta_architect.md` y `prompt_cta_architect.md`)
- **Desbloqueo de `edit_file` en reparaciones menores:** Se eliminó la prohibición ambigua de L14 en `lean/prompt_cta_architect.md` que provocaba reescrituras completas de archivos en `v5`. Se añadió explícitamente `cta_fixes/<cid>.py` y `cta_parts/cta_fixes/<cid>.py` en `WRITE permitted`.
- **Regla del Umbral Oficial `< 6` Errores (`edit_file` vs `write_file`):**
  - `< 6` errores (`1..5` errores): OBLIGATORIO uso quirúrgico de `edit_file` / `replace_file_content` sobre las líneas exactas señaladas por `compile_cta.py` (bloqueado `write_file` completo por `c2c_hook_guard.py`).
  - `>= 6` errores: anulación modular en `cta_fixes/<CID>.py` (1–2 competencias) o `write_file(Overwrite=True)` completo (si es sistémico o `SyntaxError`).
  - Post-PASS Cut: Cese inmediato de ediciones tras obtener `PASS`.
- **Blindaje anti-fugas:** En `PROHIBIDO`, se bloquearon expresamente lecturas de `tests/**`, comandos `git log` y listados recursivos con `Get-ChildItem -Recurse` sobre `courses/`.

### B. Prompts de Shard Author y Repair (`lean/prompt_shard_author.md`, `prompt_shard_author.md`, `lean/prompt_repair.md`, `prompt_repair.md`)
- **Regla del Umbral Oficial `< 6` Errores:** Sustitución unificada del criterio antiguo (`<= 15 lines`):
  - `1..5` errores (`< 6` errores, sin `SyntaxError`): OBLIGATORIO uso quirúrgico de `edit_file` (`replace_file_content`) sobre líneas exactas `StartLine..EndLine`. Prohibido reescribir con `write_file`.
  - `>= 6` errores: anulación modular en `shard_fixes/<CID>.py` (1–2 competencias) o reescritura completa (sistémico o `SyntaxError`).
- **Dimensionamiento Compacto Clean-Room Anti-Bloat:**
  - Especificado `<= 80–110` líneas por competencia, `<= 180–220` líneas totales por shard.
  - Funciones generadoras `gen_*` ultra-concisas (~12–18 líneas) mediante tuplas DRY compactas de 2 elementos `("D-XX-01", r"$@d1@$")`.
  - Prohibición de repetir párrafos de `error_rationale` o ensayos extensos en `\text{...}`.
- **Blindaje y Corrección de Manifiestos:**
  - Prohibido en todos los prompts: leer `tests/**`, ejecutar `git log`, listar recursivamente `courses/`.
  - Corregido `--manifest <work>/pre_cta_manifest.json` a `--manifest <work>/shards/pre_shard_manifest.json` en `prompt_repair.md` (Full y Lean).
- **Headroom Estricto de Bytes:**
  - `lean/prompt_shard_author.md`: **4,727 bytes** (cumple $\le$ 4,750 bytes).
  - `lean/prompt_cta_architect.md`: 3,892 bytes (cumple $\le$ 5,000 bytes).
  - `lean/prompt_repair.md`: 2,760 bytes (cumple $\le$ 5,000 bytes).
  - Todos los `system_prompts/lean/*.md` cumplen estrictamente $\le$ 5,000 bytes.

### C. `dispatch.py` (`ROLE_SPECS`, `dispatch_cta`, `dispatch_authors`)
- **`ROLE_SPECS`:**
  - Añadido `"work/cta_fixes/**"` y `"work/cta_parts/cta_fixes/**"` en `"write"` de `"cta"`, `"cta-direct"` y `"cta-map"`.
  - Añadido `"tests/**"` en `"forbidden"` de `"cta"`, `"cta-direct"`, `"cta-map"`, `"author"` y `"repair"`.
- **`dispatch_cta` (direct y mapreduce):**
  - Añadido `f"{work_rel}/cta_fixes/<CID>.py"` / `cta_parts/cta_fixes/<CID>.py` a `write_paths`.
  - Directiva 4 actualizada inyectando el umbral oficial `< 6` errores (`edit_file` obligatorio en 1..5 errores, `cta_fixes/<CID>.py` en $\ge 6$ errores).
- **`dispatch_authors`:**
  - Añadido `"tests/**"` en `forbidden_paths`.
  - Instrucción 1: Actualizada a `(<= 80-110 líneas por competencia, <= 180-220 líneas totales por shard, funciones gen_* concisas de ~15 líneas)`.
  - Instrucción 6: Actualizada con umbral oficial `< 6` errores preservando la subcadena `"NO reescribas todo el archivo desde cero con \`write_file\`"`.

### D. Ampliación de Pruebas Unitarias (`tests/test_dispatch_turn0_and_milestone3_prompts.py`)
- Se añadieron 3 métodos de prueba exhaustivos:
  1. `test_dispatch_cta_injects_official_threshold_and_cta_fixes`: Valida inyección del umbral `< 6` y rutas `cta_fixes` en modos direct y mapreduce.
  2. `test_role_specs_contains_cta_fixes_and_forbidden_tests`: Valida `write_paths` y `forbidden` en `ROLE_SPECS`.
  3. `test_stream_1d_prompts_document_official_threshold_clean_room_and_manifests`: Valida todas las invariantes en los 6 prompts (Full y Lean), tamaños de archivo y headroom $\le$ 4,750 bytes en lean author.

---

## 2. Resultados de Verificación

1. **Pruebas Focalizadas de Stream 1D:**
   ```bash
   .venv\Scripts\python.exe -m pytest tests/test_dispatch_turn0_and_milestone3_prompts.py tests/test_dispatch_scope.py -q
   ```
   **Resultado:** `23 passed in 0.51s` (100% aprobado).

2. **Regresión General en Módulos de Dispatch y Prompts:**
   ```bash
   .venv\Scripts\python.exe -m pytest tests/ -k "dispatch or prompt" -q
   ```
   **Resultado:** `84 passed, 737 deselected in 2.84s` (100% aprobado).

3. **Verificación de Frontera de Escritura:**
   - Modificados exactamente los 8 archivos permitidos en `DISPATCH.md`.
   - `subagent_types.json` NO fue modificado (preservado para Stream 2A en Gate 2).

---

## 3. Puntos de Atención para el Mejorador (`mej_1d`)
- Verificar que las frases requeridas por `test_prompts_contract_alignment.py` y `test_c2c_v321_comp4_prompts.py` sigan intactas ante cualquier refactorización.
- Mantener la estricta cota de tamaño `lean/prompt_shard_author.md <= 4,750` bytes (actualmente 4,727 bytes, 23 bytes de margen).
- Asegurar que no se filtre ninguna modificación a `subagent_types.json` ni a archivos de otros streams.
