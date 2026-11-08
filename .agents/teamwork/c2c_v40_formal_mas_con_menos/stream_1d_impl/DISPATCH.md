# DISPATCH — Stream 1D (Fase A: Implementador Ortogonal)

- **Parent Conversation ID:** `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1d_impl`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\plan_shards.py`
2. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\dispatch.py`
3. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\subagent_types.json`
4. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\system_prompts\prompt_shard_author.md`
5. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\system_prompts\prompt_cta_architect.md`
6. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\system_prompts\prompt_repair.md`
7. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\system_prompts\prompt_blind_judge.md`
8. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\system_prompts\lean\prompt_shard_author.md`
9. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\system_prompts\lean\prompt_cta_architect.md`
10. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\system_prompts\lean\prompt_repair.md`
11. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\system_prompts\lean\prompt_blind_judge.md`
12. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_dispatch_turn0_and_milestone3_prompts.py`
13. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_c2c_v321_comp4_prompts.py`
14. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_c2c_v321_comp3_dispatch.py`
15. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_weighted_sharding_m7.py`
16. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_skill_v3.py`
17. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_orchestration_resilience.py`
18. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1d_impl\BRIEFING.md` `[NEW]`
19. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1d_impl\handoff.md` `[NEW]`

PROHIBIDO tocar cualquier otro archivo.

## Guardias Obligatorias
- **Zero-Domain (`test_skill.py`):** En NINGÚN `.py` de `content-to-course/` (`plan_shards.py`, `dispatch.py`) pueden aparecer (ni siquiera en comentarios) las subcadenas en minúsculas: `edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`. Escribe comentarios en inglés.
- **Presupuesto de Bytes y Saltos LF:**
  * `system_prompts/lean/prompt_shard_author.md` DEBE pesar **`<= 4,750` bytes** (`len(path.read_bytes()) <= 4750`).
  * `subagent_types.json` DEBE escribirse estrictamente con saltos de línea Unix **LF (`\n`)**, cero `\r\n`!
- **Pytest sin contención de CPU:** Usa `-o addopts=""` al correr tus 6 suites.

## Especificación Técnica (Fase 1 + Fase 2: `MIN_ARCHETYPES=4`, Deduplicación `-2M` Tokens, Slicing `< 2 KB`, `author_snapshot.json` y Prompts `Form-C`)

1. **`plan_shards.py` (`MIN_ARCHETYPES = 4` + Particionado Ponderado + `assumptions`):**
   - Actualiza `DSL_REFERENCE["min_archetypes"] = 4` (referenciando `MIN_ARCHETYPES` de `engine.stage_contract`, con fallback `4`) y actualiza descripciones/comentarios de `3` arquetipos a **4 arquetipos ortogonales** (`direct`, `inverse`, `perturbation`, `boundary_or_edge_case`).
   - Asegura el tope ponderado: máximo `1` competencia `Skill` (`Hab-*`) por shard (o máximo `2` de `Concept`/`Misconception`), e incluye el campo `"assumptions"` de cada competencia dentro de cada slice del manifiesto `pre_shard_manifest.json` para que el autor conozca en Turno 0 los supuestos a romper en el Arquetipo 4!

2. **`dispatch.py` ("Más con Menos": `-2.0M` Tokens, `author_snapshot.json`, *Competence Slicing* `< 2 KB` y `--lean` Default):**
   - **a) Deduplicación 2x–3x del Payload (`L689, 831, 984, 1359, 1643, 2373`):**
     * Hoy cada spec de invocación serializa el texto íntegro del prompt dentro de `"Prompt"` **y una segunda copia idéntica** dentro de `"work_order"` (y en `judge` una tercera copia de `"items"`).
     * Elimina el texto duplicado gigante dentro de `"work_order"` (reemplaza cualquier string redundante de prompt completo en `"work_order"` por metadatos estructurados compactos y `"prompt_sha256"`, y en `judge` no tripliques la lista completa `"items"` si ya va en el archivo de lote / prompt, dejando solo `"item_ids"` o conteo compacto salvo claves escalares requeridas por tests como `role`, `shard_id`, `write_paths`, `read_paths`, `compile_cmd`, `min_archetypes`, `batch_id`).
   - **b) Fix `author_snapshot.json` y `_is_allowed_path` (`L1707, L2409, L2496`):**
     * En `dispatch_authors`, guarda `work/dispatch/author_snapshot.json` ANTES del `return` anticipado (`~L1707`) usando el mismo helper de snapshot de `L2409`!
     * En `_is_allowed_path` (`~L2496`), permite directorios `/__pycache__/` anidados en cualquier subruta de `work/` (ej. `shards/__pycache__/*.pyc`, `shard_fixes/**/__pycache__/*.pyc`), archivos `*.cert.json` y `cta_fixes/*.py`, eliminando al 100% los falsos positivos `237 non-standard files found`.
   - **c) *Competence Slicing* Estricto `< 2 KB` en `dispatch_repair` (`~L2267`):**
     * Remueve `cta_rel` (`work/cta.json`) y `pre_shard_manifest.json` de `ROLE_SPECS["repair"]["read"]` y de `read_paths` en `dispatch_repair`!
     * En su lugar, extrae únicamente el *Competence Slice* compacto (`< 2 KB`: `id`, `title`, `description`, `assumptions`, 6 `distractors` de `cta.json` + diagnóstico exacto y rango de líneas / bloque de `shard_XX_data.py`), guárdalo en `work/dispatch/repair_slices/<shard_id>_<cid>.json` (añadido a `read_paths`) e inyéctalo compacto en la orden de reparación, instruyendo usar la Matriz 2D (`edit_file` si `errores < 6` y `lineas <= 5`; `ModularSplicing` `shard_fixes/<shard>/<CID>.py` si `errores >= 6` o `lineas > 5`).
   - **d) Estampado `min_archetypes = 4` y `--lean` por Defecto (`~L1120, L1306, L1331, L2604`):**
     * Estampa `min_archetypes = 4` (`--min-archetypes 4` en `compile_cmd`).
     * En `define-types` (`~L2604`), haz que `lean` sea **`True` por defecto** (manteniendo `--lean` como flag idempotente compatible con CLI existente y añadiendo `--full-prompts` / `lean=False` para optar por los prompts largos). Regenera `subagent_types.json` con `lean=True` y saltos de línea estrictamente **LF (`\n`)**!

3. **Reescritura Canónica `Form-C` de `system_prompts/lean/*.md` y `system_prompts/*.md`:**
   - **`system_prompts/lean/prompt_shard_author.md` (`<= 4,750 B` ESTRICTO):**
     * Reemplaza el ejemplo roto `H-01` (`L23-53`) por un ejemplo canónico **100% compilable en `Form-C`** (compatible también con `Form-B`) con **4 arquetipos reales (`min_archetypes = 4`)** sobre una competencia física/matemática limpia (ej. rendimiento térmico reversible Carnot `Hab-01` con supuesto explícito `A-Hab01-01` de cuasi-estaticidad sin irreversibilidades disipativas $\sigma_{\text{irr}} = 0$):
       1) `direct` (`MC7`, `("easy", "Apply")`, `fmt=r"$\eta = @X@$"`, $\eta = 1 - T_C/T_H$),
       2) `inverse` (`FIB`, `("medium", "Apply")`, despejar $T_H = T_C / (1 - \eta)$ sin `$` externos en `FIB`),
       3) `perturbation` (`FIB`, `("hard", "Analyze")`, escalamiento de $T_C' = T_C/2 \implies \eta' = (1 + \eta)/2$),
       4) `boundary_or_edge_case` (`MS`, `("hard", "Evaluate")`, `"assumption_id": "A-Hab01-01"`, ruptura de reversibilidad $\sigma_{\text{irr}} > 0$ donde $\eta_{\text{real}} < 1 - T_C/T_H$).
     * Con diccionario único `RATS` (`>= 25` chars con `@tc@` / `@th@`), stems composicionales `(2 contextos, 2 preguntas)` $\to 4 \times 4 = 16$ stems, `3` pistas socráticas `>= 25` chars sin filtrar la clave, y verificadores relacionales genuinos `ver_*(cand, v)` que refutan los 6 distractores (cero `_clean_ds`, cero `return True` trivial).
     * Verifica que el archivo completo pese **`<= 4,750` bytes** y conserve los placeholders de contrato (`<<S4_...>>` / `min_archetypes = 4`) requeridos.
   - **`system_prompts/prompt_shard_author.md`:** Elimina todo rastro de `Form-A` obsoleta (`L72-196`), documenta `Form-C` (recomendado por `-65%` tokens) y `Form-B` con `min_archetypes = 4`, `assumptions`, prohibición de `_clean_ds` y refutación estricta `ver_*`.
   - **`prompt_cta_architect.md` & `lean/prompt_cta_architect.md`:** Documenta la 7-tupla con `assumptions: [(id, statement_latex, violation_consequence)]` y `CTA_CONTRACT_VERSION = 2`.
   - **`prompt_repair.md` & `lean/prompt_repair.md` y `prompt_blind_judge.md` & `lean/prompt_blind_judge.md`:** Alinea `repair` con Matriz 2D (`edit_file` vs `ModularSplicing`) + *Competence Slice* (prohibido leer `cta.json`), y `blind_judge` con evaluación de **Suficiencia Epistémica** y no-giveaway semántico.

4. **Actualización y Ampliación de tus 6 Suites Exclusivas:**
   - Actualiza las aserciones que verificaban `min_archetypes == 3` a `min_archetypes == 4`, verifica la deduplicación de `work_order`, persistencia de `author_snapshot.json`, ausencia de `cta.json` en `repair` `read_paths`, `--lean` por defecto, LF en `subagent_types.json` y presupuesto `<= 4,750 B` de `lean/prompt_shard_author.md`.

## Verificación y Entrega
```powershell
& ".venv\Scripts\python.exe" -m pytest -o addopts="" tests/test_dispatch_turn0_and_milestone3_prompts.py tests/test_c2c_v321_comp4_prompts.py tests/test_c2c_v321_comp3_dispatch.py tests/test_weighted_sharding_m7.py tests/test_skill_v3.py tests/test_orchestration_resilience.py -q
```
Escribe `BRIEFING.md` antes de editar, `handoff.md` al terminar, y envía `DONE:: Stream 1D (<N> passed)` a `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`.
