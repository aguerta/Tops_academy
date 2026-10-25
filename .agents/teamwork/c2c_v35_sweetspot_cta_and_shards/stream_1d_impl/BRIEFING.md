# Pre-Flight Sanity Check — Stream 1D (`impl_1d`)

**Fecha/Hora:** 2026-10-24T20:37:00-05:00  
**Implementador:** `impl_1d`  
**Objetivo:** Modificaciones en Prompts y Dispatch para Sweet-Spot CTA y Shards (Umbral < 6 errores, Dimensionamiento Compacto Clean-Room, y blindaje de introspección / fugas).

---

## 1. Verificación de Archivos en Frontera Exclusiva de Escritura

| Archivo | Líneas Actuales | Tamaño Actual (bytes) | Estado Pre-Flight |
| :--- | :--- | :--- | :--- |
| `dispatch.py` | 2113 | 97,164 | Leído y validado |
| `lean/prompt_cta_architect.md` | 60 | 3,416 | Leído (L14 prohíbe micro-edits; pendiente actualizar L14, L36-41) |
| `prompt_cta_architect.md` | 358 | 24,848 | Leído (L19-22, L26-32, L345, L355 pendientes de actualizar) |
| `lean/prompt_shard_author.md` | 74 | 4,713 | Leído (Headroom actual: 37 bytes para límite 4,750 bytes) |
| `prompt_shard_author.md` | 413 | 30,589 | Leído (L41-46, L375-385, L410-412 pendientes de actualizar) |
| `lean/prompt_repair.md` | 26 | 2,492 | Leído (L18-19, L23 referencia pre_cta_manifest.json pendiente a pre_shard_manifest.json) |
| `prompt_repair.md` | 71 | 5,064 | Leído (L43-44, L60 referencia pre_cta_manifest.json pendiente a pre_shard_manifest.json) |
| `tests/test_dispatch_turn0_and_milestone3_prompts.py` | 485 | 25,235 | Leído (20 tests pasando limpiamente en suite) |

---

## 2. Invariantes y Headroom Verificados
1. **Límites de tamaño en Prompts Lean:**
   - `lean/prompt_shard_author.md`: Actualmente 4,713 bytes $\le$ 4,750 bytes.
   - `lean/prompt_cta_architect.md`: Actualmente 3,416 bytes $\le$ 5,000 bytes.
   - `lean/prompt_repair.md`: Actualmente 2,492 bytes $\le$ 5,000 bytes.
   - Todos los `system_prompts/lean/*.md` deben mantenerse estrictamente $\le$ 5,000 bytes.
2. **Invariantes de Contenido de Pruebas:**
   - Frases requeridas en `prompt_shard_author.md` (Full y Lean) se mantendrán 100% intactas.
   - Frases requeridas en `prompt_repair.md` (Full y Lean) se mantendrán 100% intactas.
   - Subcadena `"NO reescribas todo el archivo desde cero con \`write_file\`"` en `dispatch_authors` L1127 se mantendrá intacta.
3. **Bloqueos Detectados:**
   - Ninguno. Todos los archivos necesarios están dentro de la frontera exclusiva permitida.
   - Sin dependencias externas que requieran escalamiento BLOCKER.

---

## 3. Plan de Edición Secuencial
1. **A. Prompts de CTA:**
   - `lean/prompt_cta_architect.md`: agregar `cta_fixes/<cid>.py` a WRITE permitted, remover prohibición ambigua en L14, actualizar sección 3/4 con regla `< 6` errores (`edit_file` vs `write_file`).
   - `prompt_cta_architect.md`: agregar `cta_fixes/<cid>.py` a WRITE, prohibir `tests/**`, `git log`, `Get-ChildItem -Recurse`, documentar umbral oficial `< 6` errores en secciones 9 y 10.
2. **B. Prompts de Shard Author y Repair:**
   - `lean/prompt_shard_author.md`: prohibir `tests/**`, `git log`, `courses/` recursivo; reemplazar regla `<= 15 lines` por regla umbral `< 6` errores; concisión `gen_*` manteniendo tamaño $\le$ 4,750 bytes.
   - `prompt_shard_author.md`: prohibir `tests/**`, `git log`, `courses/` recursivo; explicitar `<= 80–110` líneas/comp y `<= 180–220` líneas/shard; reemplazar regla `<= 15 lines` por umbral `< 6` errores.
   - `lean/prompt_repair.md`: prohibir `tests/**`, `git log`, `courses/` recursivo; actualizar `--manifest pre_shard_manifest.json`; actualizar umbral `< 6` errores.
   - `prompt_repair.md`: prohibir `tests/**`, `git log`, `courses/` recursivo; actualizar `--manifest pre_shard_manifest.json`; actualizar umbral `< 6` errores.
3. **C. `dispatch.py`:**
   - `ROLE_SPECS`: añadir `work/cta_fixes/**` y `work/cta_parts/cta_fixes/**` en `write` de `cta`, `cta-direct`, `cta-map`; añadir `tests/**` en `forbidden` de `cta`, `cta-direct`, `cta-map`, `author`, `repair`.
   - `dispatch_cta`: `write_paths` con `cta_fixes/<CID>.py`; directiva 4 con umbral `< 6` errores (en `mapreduce` y `direct`).
   - `dispatch_authors`: `forbidden_paths` con `tests/**`; instrucción 1 con `<= 80-110 líneas por competencia, <= 180-220 líneas totales por shard`; instrucción 6 con umbral `< 6` errores preservando substring.
4. **D. Tests y Verificación:**
   - Extender `tests/test_dispatch_turn0_and_milestone3_prompts.py` con pruebas para todas las nuevas invariantes del Stream 1D.
   - Ejecutar pytest enfocado.
   - Generar `handoff.md`.
