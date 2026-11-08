# DISPATCH — Stream 1B (Fase A: Implementador Ortogonal)

- **Parent Conversation ID:** `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1b_impl`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\engine\stage_contract.py`
2. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\compile_shard.py`
3. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\c2c_hook_guard.py`
4. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\budget_guard.py`
5. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_m3_archetypes_semantic_gate.py`
6. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_compile_shard.py`
7. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_shard_compiler_hardening.py`
8. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_shard06_and_dry_archetypes.py`
9. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_invariants_and_shard_overescape_r23.py`
10. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_latex_engine.py`
11. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_hook_post_pass_and_write_isolation.py`
12. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_watchdog_and_hooks.py`
13. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_specific_error_report_and_stem_gate.py`
14. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1b_impl\BRIEFING.md` `[NEW]`
15. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1b_impl\handoff.md` `[NEW]`

PROHIBIDO tocar cualquier otro archivo.

## Guardias Obligatorias
- **Seguridad `c2c_hook_guard.py`:** Mantenlo 100% en librería estándar de Python (`stdlib` pura, CERO imports externos como `sympy`, `z3` o `pydantic` dentro de `c2c_hook_guard.py`), con `try ... except BaseException:` global y `sys.exit(0)`. Prohibido dejar `.c2c_subagent_lock.json` activo fuera de `tmp_path`.
- **Zero-Domain (`test_skill.py`):** En NINGÚN `.py` de `content-to-course/` pueden aparecer (ni siquiera en comentarios o docstrings) las subcadenas en minúsculas: `edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`. Escribe todos los comentarios en inglés.
- **Windows `cp1252` Safety:** Al capturar `pykatex.ParseError`, limpia `str(exc).replace("\u0332", "^")` para evitar `UnicodeEncodeError`.
- **Pytest sin contención de CPU:** Usa siempre `-o addopts=""` al correr tus 9 suites.

## Especificación Técnica (Fase 1 + Fase 2: `MIN_ARCHETYPES=4`, DSL `Form-C`, Triple `ver_*`, `SymPy`/`Z3`, Poda AST y Hook 2D)

### 1. `engine/stage_contract.py` (EDITAR PRIMERO)
- Sube `CONTRACT_VERSION = 2` y **`MIN_ARCHETYPES = 4`**.
- Exporta `ARCHETYPE_KINDS = ("direct", "inverse", "perturbation", "boundary_or_edge_case")`.
- Mantén intactas las firmas de todas las funciones existentes (`is_skill_type`, `quota_for_type`, `required_unique_stems`, `competency_contract`, `global_contract`, `stems_advice`, `stems_advice_text`, `contract_tokens`, `render_contract_tokens`, `contract_drift`).

### 2. `compile_shard.py`
1. **DSL Composicional Ultra-Compacto `Form-C` (Retrocompatible 100% con 9-tuplas `Form-B`):**
   - Mantén el rechazo de `Form-A` legacy, conservando soporte 100% para 9-tuplas `Form-B` `(tpl_id, cid, qtype, gen_fn, ver_fn, (difficulty, bloom), stems, hints, solution)`.
   - Añade soporte nativo para entradas `dict` **`Form-C`** en `TEMPLATES`:
     * Claves soportadas: `"id"` (o `"tpl_id"`), `"cid"`, `"qtype"` (`"MC7"|"FIB"|"MS"` o nombres largos), `"gen"`, `"ver"`, `"band"` (`(difficulty, bloom)`), `"stems"`, `"hints"`, `"sol"` (o `"solution"`), y opcionales `"archetype"` (`in ARCHETYPE_KINDS`), `"assumption_id"` (`str | None`), `"fmt"` (`str` con `@X@`, ej. `r"$\eta = @X@$"`), `"rats"` (`dict[str, str]`).
     * **Stems composicionales:** Si `stems` (en `Form-C` o `Form-B`) es una 2-tupla de dos listas/tuplas `(contexts, questions)` donde ambos elementos son secuencias de strings (`len >= 2`), expándelos al producto cartesiano `[f"{c.strip()} {q.strip()}" for c in contexts for q in questions]`.
     * **Wrapper `fmt` + Catálogo `rats` / `RATS` + Firma 2-arg `ver(cand, v)`:**
       - Permite que `gen(rng)` en `Form-C` devuelva compacto `{"ans": bare_ans, "ds": [(did, bare_val), ...], "vars": {...}}` (además del dict estándar `{"correct": ..., "distractors": ..., "vars": ...}`).
       - Si existe `"fmt"` con `@X@` (en `MC7`), envuelve `ans` y cada valor de `ds` usando `fmt.replace("@X@", str(val))` (si aún no están envueltos por `fmt`), garantizando simetría `R-15`/`R-16` por construcción.
       - Si un distractor es 2-tupla `(did, val)` **únicamente cuando** `"rats"` (en el dict `Form-C`) o un dict `RATS` a nivel del módulo `shard_XX_data.py` contiene `did`, expándelo automáticamente a la 3-tupla `(did, wrapped_val, rats_map[did])`! *(Importante: si NO hay `rats`/`RATS` con ese `did`, una 2-tupla `(did, val)` en `--strict` sigue siendo rechazada igual que en v3.8 para preservar los tests existentes de rechazo de 2-tuplas).*
       - Permite que `ver` tenga **2 argumentos `ver(cand, v)`** (donde `cand` es el string/valor candidato `result["correct"]` y `v` es `result["vars"]`) o **1 argumento `ver(result)`**. Al serializar `<CID>.json`, genera un wrapper limpio dentro de `generator_code` / `verifier_code` para que el JSON exportado cumpla al 100% el contrato estándar `generate(rng) -> {"correct", "distractors", "vars"}` y `cross_check(rng, result) -> bool`!
   - **Validación de `archetype` y `assumption_id`:** Si una competencia en `cta.json` declara `"assumptions"` no vacío y las plantillas usan `Form-C` con `eff_min_arch >= 4`, exige que se cubran los 4 `ARCHETYPE_KINDS` y que la plantilla `"boundary_or_edge_case"` referencie un `"assumption_id"` válido presente en `cta_comp["assumptions"]` (`[TPL-ASSUMPTION-LINK]`).
2. **Triple Contrato Anti-Trampas en Verificadores (`ver_*`) y Higiene AST:**
   - **a) Soundness Positiva Estricta:** Convierte `np.generic` con `.item()` y exige `res_ver is True` (rechaza `False`, `np.bool_(False)`, `None`, `0`).
   - **b) Refutación Estricta de Distractores (`[VERIFIER-TAUTOLOGY-DETECTED]`):** En el dry-run de compilación (sobre las primeras 3–5 semillas), para cada distractor `d_i` en `MC7` (y para cada opción `is_correct=False` cuando `ver_fn` evalúa opciones o en `MC7`/`FIB` si hubiera alternativas), construye `mutated = {**result, "correct": d_val}` (o llama `ver_fn(d_val, result["vars"])` en modo 2-arg) y exige que devuelva `False` (o lance `ValueError`/`ArithmeticError` capturada como `False`). Si el verificador devuelve `True` para CUALQUIER distractor falso (ej. `return v["a"] > 0` o `return True`), aborta inmediatamente con `[VERIFIER-TAUTOLOGY-DETECTED]`.
   - **c) Inspección AST Dura:**
     * Rechaza `try: ... except ...: return True` en `ver_*` con `[VERIFIER-SWALLOWED-EXCEPTION]`.
     * Rechaza artefactos de depuración (`raise RuntimeError`, `breakpoint(`, `import pdb`, `print(`) en funciones generadoras/verificadoras con `[TPL-DEBUG-ARTIFACT]`.
     * Rechaza bucles de perturbación ad-hoc (`def _clean_ds` o `while ...:` que muten candidatos de distractores sumando constantes flotantes arbitrarias para ocultar colisiones) con `[TPL-AD-HOC-PERTURBATION]`.
3. **No-Clonación Algebraica (`eff_min_arch` Fórmulas Disjuntas) y Verificación Simbólica `SymPy` / `Z3`:**
   - Corrige la brecha de clonación (`~L2249`): cuando `eff_min_arch >= 3`, para competencias `Skill` (`Hab-*` o `is_skill_type`), exige que las huellas de salida evaluadas en semilla fija (`valid_100`) sean **todas distintas entre sí** (`len(set(valid_100)) == len(valid_100)`), impidiendo que 3 o 4 plantillas calculen exactamente la misma fórmula!
   - Cuando `eff_min_arch >= 4`, exige cobertura de las 3 bandas `{"easy", "medium", "hard"}`, `>= 2` niveles `bloom` (con al menos 1 en `{"Apply", "Analyze", "Evaluate", "Create"}` para `Skill`), y multimodalidad (`>= 2` en `{"FIB", "MS"}` incluyendo `>= 1 "FIB"` para `Skill` cuando `eff_min_arch >= 4`; `>= 1` en `{"FIB", "MS"}` para `Concept`/`Misconception`).
   - Extiende `[DIAG-MAGIC-MULT]` (`~L2451`): además de `ast.Mult`, detecta divisiones constantes **`ast.Div` (`ans / 3`, `ans / 2`, `correct / k`)** y usa `SymPy` / `z3` (sobre variables extraídas de `rng.randint(a, b)` cuando las expresiones sean algebraicas puras) para verificar `Zero_Magic_Mult_Universal` ($d_i(\theta) / \text{correct}(\theta) \notin \mathbb{Q}\setminus\{0,1\}$) y `TPL_D4_Universal` (reportando testigo exacto $\theta^*$ si existe colisión algebraica idéntica en todo el dominio o dentro de la caja `randint`), sin disparar falsos positivos sobre coeficientes dentro de strings LaTeX intermedios.
4. **Cierre de Brechas Shift-Left Adicionales + Poda AST de `<CID>.json` + `shard_XX.cert.json`:**
   - Bloquea en `--strict`: cuantificadores vacuos (`\forall \varepsilon = 0.05`, `\exists \delta = ` seguidos de literal numérico), fuga de `correct` (`len >= 15` chars no triviales) en `hints[0]` o `hints[1]` (`[TPL-HINT-LEAK]`), paréntesis delatores en texto de opciones (`(sesgo...)`, `(confusión...)`, `(error...)` -> `[TPL-TELLTALE-PAREN]`), y valida spans matemáticos con `pykatex.renderToString` (con limpieza `\u0332` -> `^`).
   - **Poda AST de `<CID>.json` (`177 KB -> ~10 KB`):** En lugar de incrustar el texto completo de `shard_XX_data.py` dos veces en `generator_code` y `verifier_code`, extrae con `ast` únicamente los `import`/`from`, constantes globales referenciadas y las funciones helper/target alcanzables desde `gen_fn` (para `generator_code`) y desde `ver_fn` (para `verifier_code`)!
   - En `.check_attempts/compile_<shard>.json`, persiste siempre `"affected_line_count": int`, `"has_syntax_error": bool`, `"error_sha256": str`.
   - Al aprobar (`ok == True`), emite `work/shards/<shard_id>.cert.json` con `{"schema_version": 1, "stage": "shard", "artifact_id": shard_id, "source_sha256": ..., "cta_sha256": ..., "compiler_sha256": ..., "contract_version": 2, "template_shas": {...}, "passed_50_seeds": True, "created_at": ...}`.

### 3. `c2c_hook_guard.py` y `budget_guard.py`
1. **Fix Regla B Exención Post-PASS (`c2c_hook_guard.py:L677-L680`):**
   - Normaliza `str(spec.get("status", "")).upper() in ("REJECTED", "FAIL", "FAILED")` y toma la unión `set(spec.get("failing_shards") or []) | set(spec.get("affected_shards") or [])` tanto en `publish_rejection_spec.json` como en `template_failures.json`. Así `c2c_repair` puede editar legítimamente un shard rechazado aguas abajo aunque exista `pass_shard_XX.json`, mientras otros shards aprobados permanecen 100% blindados!
2. **Matriz Certificada 2D `decidir_estrategia_edicion(error_count, affected_line_count, has_syntax_error)` (`c2c_hook_guard.py:L850-L881`):**
   - Lee `error_count`, `affected_line_count` (fallback a `error_count` si no existe) y `has_syntax_error` desde `.check_attempts/compile_*.json`:
     * Si `has_syntax_error` o creación inicial (`existing_lines < 40`): permite `write_file`.
     * Si `1 <= error_count < 6` **y** `affected_line_count <= 5`: exige `edit_file` (bloquea `write_file` monolítico).
     * Si (`error_count >= 6` **o** `affected_line_count > 5`) sin `SyntaxError` sobre un archivo `shard_XX_data.py` o `cta_data.py` existente (`>= 40` líneas): bloquea `write_file` monolítico (y bloquea bucles repetitivos de `edit_file` in-place tras `>= 2` intentos fallidos sobre ese mismo intento) redirigiendo con mensaje claro a **`ModularSplicing`** (`work/shard_fixes/<shard>/<CID>.py` o `work/cta_fixes/<CID>.py`)!
3. **Gobernanza Síncrona de Presupuesto y `[REPAIR-NO-FULL-CTA]` (solo cuando `.c2c_subagent_lock.json` tiene `"active": True`):**
   - Actualiza/lee de forma atómica y segura en `.c2c_subagent_lock.json`: `turn_count` (`<= max_turns`, default `40`), `est_tokens` (`<= max_tokens`, default `5_000_000`) y `error_sha256_streak` (`< max_error_streak`, default `3`). Si se supera cualquiera de los tres umbrales cuando el lock está activo, emite bloqueo duro determinista (`HARD_ABORT`) para que el subagente se detenga y reporte al orquestador. Sincroniza constantes/helpers en `budget_guard.py`.
   - Añade bloqueo `[REPAIR-NO-FULL-CTA]`: cuando el lock activo tenga `role == "repair"` (o exista orden de `repair` activa sin autoría inicial), bloquea lecturas de `work/cta.json` completo (`> 20 KB`) o `pre_shard_manifest.json`, indicando usar el *Competence Slice* provisto.
   - Actualiza el texto guía de `[M3-ARCHETYPES]` en `c2c_hook_guard.py` para reflejar `min_archetypes = 4` y `Form-C` / `Form-B`.

### 4. Actualización y Ampliación de tus 9 Suites Exclusivas
- Actualiza las aserciones/fixtures que asumían default `MIN_ARCHETYPES == 3` cuando no pasaban `min_archetypes` explícito (o ajusta fixtures de 4 arquetipos en `test_m3_archetypes_semantic_gate.py`, etc.), manteniendo todos los tests parametrizados.
- Añade pruebas unitarias exhaustivas para: `Form-C` (`fmt`, `RATS`, stems cartesianos `2x2`, `ver(cand, v)` 2-arg), `[VERIFIER-TAUTOLOGY-DETECTED]` (refutación de los 6 distractores), `[VERIFIER-SWALLOWED-EXCEPTION]`, `[TPL-DEBUG-ARTIFACT]` (`raise RuntimeError`), `[TPL-AD-HOC-PERTURBATION]` (`_clean_ds`), `ast.Div` magic divisor (`ans / 3`), poda AST de `<CID>.json` (`< 15 KB`), emisión de `shard_XX.cert.json`, Regla B con `"status": "rejected"` + `"failing_shards"`, Matriz 2D (`affected_line_count > 5 -> ModularSplicing`) y tope síncrono de turnos/tokens/streak en `.c2c_subagent_lock.json`.

## Verificación y Entrega
```powershell
& ".venv\Scripts\python.exe" -m pytest -o addopts="" tests/test_m3_archetypes_semantic_gate.py tests/test_compile_shard.py tests/test_shard_compiler_hardening.py tests/test_shard06_and_dry_archetypes.py tests/test_invariants_and_shard_overescape_r23.py tests/test_latex_engine.py tests/test_hook_post_pass_and_write_isolation.py tests/test_watchdog_and_hooks.py tests/test_specific_error_report_and_stem_gate.py -q
```
Escribe `BRIEFING.md` antes de editar, `handoff.md` al terminar, y envía `DONE:: Stream 1B (<N> passed)` a `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`.
