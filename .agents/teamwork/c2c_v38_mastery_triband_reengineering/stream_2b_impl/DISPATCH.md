# DISPATCH — Stream 2B (Fase 1: Implementador — Suites de Integración Multi-Módulo)

- **Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_2b_impl`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre (**0 archivos de producción**):
1. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_c2c_solow2_architectural_improvements.py`
2. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_c2c_remediation_optimization.py`
3. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_c2c_v31_adversarial_plan.py`
4. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_c2c_case_2b_mastery.py`
5. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_c2c_v321_comp2_shard.py`
6. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_pipeline_reparations.py`
7. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_2b_impl\BRIEFING.md` `[NEW]`
8. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_2b_impl\handoff.md` `[NEW]`

PROHIBIDO modificar cualquier archivo de producción o cualquier otro test. Si detectas un bug real en producción que impida pasar un test válido, usa `BLOCKER:: <archivo:línea> | <causa> | <opciones>`.

## Reglas Pre-Flight y Eficiencia
- Usa `read_file` en bloques amplios (`400-800` líneas por llamada) y ejecuta primero `pytest` sobre las 6 suites para identificar de inmediato qué tests requieren migración de contratos v3.8.
- **Hooks:** Prohibido ejecutar `run.py --help` / `dispatch.py --help` o `python -c` mencionando `"content-to-course/"` junto con `open(`, `read_text`, `run.py`, `prepare.py`, `ingest.py`, `dispatch.py`. Usa únicamente `& ".venv\Scripts\python.exe" -m pytest <archivos_test> -q`.

## Especificación Técnica (Migración de Suites de Integración a Contratos C2C v3.8)
Adapta los fixtures e invariantes de las 6 suites a las nuevas compuertas de C2C v3.8 (sin debilitar aserciones):
1. **Contrato `Form-B` Tri-Banda Multimodal y `[TPL-DYNAMIC-RATIONALE]`:**
   - Toda tupla en `TEMPLATES` debe ser 9-tupla `Form-B`: `(tpl_id, cid, qtype, gen_fn, ver_fn, (difficulty, bloom), stems, hints, solution)` con `[5]` como 2-tupla explícita `(difficulty, bloom)`.
   - Cobertura Tri-Banda `{"easy", "medium", "hard"}`, `>= 2` niveles `bloom`, `>= 2` plantillas `FIB`/`MS` en `Hab-*`/`Skill` y `>= 1` en `C-*`/`H-*` (`min_archetypes = 3`).
   - Distractores `MC7` como **3-tuplas `(did, val, rationale_con_@var@)`** (`len >= 20`, interpolando `@var@` para variar entre semillas y superar `35%` de unicidad) y opciones falsas `MS` con `"error_rationale"` dinámico `@var@`; `FIB` sin `$` externos; `ver_fn` con comparación real (no `return True` trivial); `>= 3` `stems` genuinos (no esperar `>= 30` stems sintéticos de `generate_rich_stem_variants`) y `3..5` `hints` explícitas `>= 25` chars (sin auto-poblado desde `wrong_belief`).
   - En `test_c2c_v321_comp2_shard.py`: preservar intacta la verificación de inmunidad LaTeX `${k}^*$` junto con interpolación de tokens cortos `@k@` / `@n@`.
2. **Contratos Stage 1 (`CTA` / DAG) y Stage 5 (`RepairLoop` / `Judge`):**
   - `merge_cta_parts()` genera `cta_draft.json` + `cta_outline.json` (y `apply_harmonize()` escribe `cta.json`); `check_prerequisites_dag` exige `connected_components == 1` y `root_ratio <= 0.20` para `N >= 2`; `check_cta.py` bloquea `\text{...} > 45` chars (`[KATEX-PROSE-OVERFLOW]`).
   - `RepairLoop` ya NO muta longitudes (`shared_pads`) ni valores numéricos de opciones: ejecuta solo el Módulo A (`sanitize_latex_escapes`). Si algún test en `test_c2c_remediation_optimization.py` o `test_pipeline_reparations.py` probaba la antigua inyección de `shared_pads` o mutadores C-F como comportamiento esperado, actualízalo para certificar que `RepairLoop` preserva intactas las opciones mientras sanea escapes LaTeX, y que el validador bloquea muletillas de padding.
   - `judge.py` muestrea `seeds=(101, 202, 303)` en el 100% de las plantillas y exige `100%` de acuerdo por `template_id`.

## Verificación
Ejecuta:
```powershell
& ".venv\Scripts\python.exe" -m pytest tests/test_c2c_solow2_architectural_improvements.py tests/test_c2c_remediation_optimization.py tests/test_c2c_v31_adversarial_plan.py tests/test_c2c_case_2b_mastery.py tests/test_c2c_v321_comp2_shard.py tests/test_pipeline_reparations.py -q
```
Escribe `BRIEFING.md` antes de editar, `handoff.md` al terminar y notifica a `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589` con `DONE:: Stream 2B Impl completado (<N> passed)`.
