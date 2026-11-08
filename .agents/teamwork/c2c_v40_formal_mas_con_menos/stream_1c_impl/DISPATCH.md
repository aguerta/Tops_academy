# DISPATCH — Stream 1C (Fase A: Implementador Ortogonal)

- **Parent Conversation ID:** `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1c_impl`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\engine\sandbox.py`
2. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\engine\instantiate.py`
3. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\engine\invariants.py`
4. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\engine\assemble.py`
5. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\check_templates.py`
6. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\schemas\template.schema.json`
7. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\examples\edo\cta.json`
8. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\examples\edo\templates\C-02.json`
9. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\examples\edo\templates\Hab-02.json`
10. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\examples\edp\cta.json`
11. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\examples\edp\templates\C-01.json`
12. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\examples\edp\templates\Hab-01.json`
13. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_sandbox_adversarial.py`
14. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_sandbox_gil_and_circuit_breaker.py`
15. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_engine_invariants_adversarial.py`
16. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_assemble_katex_and_rationale.py`
17. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_assemble_sanitize_katex_r23.py`
18. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_katex_prairielearn_tokens.py`
19. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_c2c_error_aggregation.py`
20. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_template_variability.py`
21. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_blind_guess_empirical.py`
22. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1c_impl\BRIEFING.md` `[NEW]`
23. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1c_impl\handoff.md` `[NEW]`

PROHIBIDO tocar cualquier otro archivo.

## Guardias Obligatorias
- **Zero-Domain (`test_skill.py`):** En NINGÚN `.py` de `content-to-course/` pueden aparecer (ni siquiera en comentarios o docstrings) las subcadenas en minúsculas: `edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`. Escribe comentarios/docstrings en `.py` en inglés! *(Nota: los archivos JSON en `examples/edo/` y `examples/edp/` sí contienen ejemplos de ecuaciones diferenciales, pero los archivos `.py` JAMÁS deben contener esas palabras).*
- **Windows `cp1252` Safety:** `pykatex.ParseError` incluye `"\u0332"` en su mensaje; reemplaza siempre `"\u0332"` por `"^"` al convertir `ParseError` a string.
- **Pytest sin contención de CPU:** Usa `-o addopts=""` al correr tus 9 suites.

## Especificación Técnica (Fase 1 + Fase 2: Fix `np.bool_`, *Rejection Sampling*, `pykatex`/`KaTeXAST`, Paridad `check_templates` y Ejemplos 4 Arquetipos)

1. **Corrección Crítica `np.bool_(False) is False` y Verificadores 2-Arg en `engine/sandbox.py` (`L542` y `L671`):**
   - En ambos caminos de ejecución de `cross_check` (`execute_sandbox_instance` y `execute_sandbox_batch`), desenrolla escalares NumPy (`if hasattr(cc_res, "item") and callable(getattr(cc_res, "item", None)): cc_res = cc_res.item()`) y exige **`if cc_res is not True:`** lanzando `SandboxExecutionError(f"Cross-check verification failed (returned {cc_res!r}).")`. Así quedan estrictamente bloqueados `False`, `np.bool_(False)`, `None`, `0` o cualquier no-booleano!
   - Soporta invocación flexible de `cross_check` / `ver_*`: si la función verificadora acepta `(rng, result)` (2 params cuyo 1er param se llama `rng`), pásale `(rng_cc, result)`; si acepta `(cand, v)` (2 params donde el 1er param NO es `rng`), pásale `(result.get("correct"), result.get("vars", {}))`; si acepta 1 param `(result,)`, pásale `(result,)`.

2. ***Rejection Sampling* Determinista por Sub-Semilla en `engine/instantiate.py` (y helper en `sandbox.py`):**
   - Cuando al instanciar una semilla primaria `seed` ocurre una colisión numérica incidental entre `correct` y un distractor o entre dos distractores (`TPL-D4` / opciones duplicadas), en lugar de obligar al autor a meter hacks `_clean_ds`, reintenta deterministamente hasta `MAX_SUBSEED_ATTEMPTS = 8` sub-semillas (`seed` para `k=0`, y `(seed * 1009 + k) & 0x7FFFFFFF` para `k=1..7`).
   - **Salvaguarda Anti-Clonación:** Si una plantilla falla los 8 sub-intentos en una semilla, o si más del `20%` de las semillas requieren reintento (indicando dos distractores algebraicamente idénticos), lanza el error de colisión `TPL-D4` inmediatamente! Exporta un helper público `instantiate_verified_seed(template, seed, ...)` que `judge.py` también pueda reutilizar.

3. **`pykatex` + Invariantes Inductivos `KaTeXAST` y Canonicalizador Algebraico (`engine/invariants.py` y `engine/assemble.py`):**
   - En `engine/invariants.py` (`validate_katex_syntax` / `check_instance_invariants`):
     * Integra `pykatex.renderToString(math_content, is_display)` sobre cada bloque `$...$` y `$$...$$` (con caché LRU `functools.lru_cache(maxsize=8192)` para mantener velocidad `< 1 ms` y limpiando `"\u0332"` -> `"^"` en `pykatex.ParseError`!).
     * Valida invariantes `KaTeXAST`: prohíbe prosa `> 45` caracteres o `_` crudo sin escapar dentro de `\text{...}` (salvo bloques cortos legítimos ya permitidos sin `_`), prohíbe `{{...}}` dobles vacíos/huérfanos, prohíbe cuantificadores vacuos (`r"\\(?:forall|exists)\s+[a-zA-Z\\]+\s*=\s*[-+]?\d"`), y prohíbe punto newtoniano sobre dígitos (`r"\\dot\{\s*\d+\s*\}"`).
   - En `engine/assemble.py` (`sanitize_katex_syntax`):
     * Añade canonicalización algebraica segura dentro de bloques matemáticos `$...$` / `$$...$$` para colapsar signos dobles de interpolación (`+ -5` $\to$ `- 5`, `- -5` $\to$ `+ 5`), preservando intactos todos los comandos LaTeX y la velocidad zero-copy de R-23.

4. **Reparación de Caché Fría, Paridad Shift-Left y Agregación de Reportes en `check_templates.py` + `schemas/template.schema.json`:**
   - Extiende `schemas/template.schema.json` para permitir campos opcionales `"archetype"`, `"assumption_tested_id"` y `"contract_version"`.
   - **Fix Caché Fría (`check_templates.py:L3361`):** Cambia `if cta_p is not None and shard_py is None:` para que también escriba `.validation_cache/<cid>_<hash>.ok.pkl` cuando `shard_py is not None` (de modo que `compile_shard.py` deje caliente la caché para etapas posteriores!).
   - **Paridad Shift-Left 100% con Stage 4/6:**
     * Elimina el bypass `passes_calibrated` (`div_ratio >= 0.25` en `~L3065`); exige `div_ratio >= MIN_DIVERSITY_RATIO` (`0.50`) igual que Stage 4!
     * Detecta `Skill` con `is_skill_type(comp.get("type") or comp.get("category")) or cid.startswith("Hab-")`.
     * Deja de saltar `R-16` (`ERR_GIVEAWAY_COURSE`) en `~L2254` cuando se valida un conjunto suficiente de instancias.
     * Reemplaza el código muerto `_is_trivial_cross_check` (`L2322-L2352`) por verificación real de **Refutación Estricta de Distractores** en `check_single_template` (cuando `verifier_code` / `cross_check_py` esté presente en un template `MC7`, verifica en la primera semilla que sustituir `correct` por cada distractor devuelva `False` / falle la verificación!).
     * En plantillas paramétricas (`vars` no vacío) de `Concept` o `MS`, exige `>= 5` claves/configuraciones correctas únicas a lo largo de las 50 semillas (salvo plantillas explícitamente estáticas con `vars == {}`).
   - **Agregación Compacta de Diagnósticos (`~L3883-L3888`):** Agrupa errores repetidos en múltiples semillas por `(rule_id, template_id, normalized_msg)` reportando `affected_seeds_count` y `sample_seed` en lugar de volcar 50 entradas idénticas (`82 KB -> < 1.5 KB`).

5. **Actualización de Ejemplos Canónicos `examples/edo/` y `examples/edp/` (4 Arquetipos + `assumptions` + Verificador Real en `Hab-01.json`):**
   - Añade `"assumptions"` explícitos a las competencias en `examples/edo/cta.json` y `examples/edp/cta.json`.
   - En `examples/edp/templates/Hab-01.json`: corrige la ambigüedad matemática ($x > 0, y > 0$ explícitos en los stems, restringe $a \ge 2$ para que $a \neq 1$ jamás iguale $y/x^b$ con $x^b/y$, y reemplaza el verificador tautológico `return v['a'] > 0 and v['b'] > 0` por un verificador algebraico genuino con `sympy` que compruebe la PDE/invariante sobre `result['correct']` y devuelva `False` en los 6 distractores!).
   - Amplía `examples/edo/templates/{C-02,Hab-02}.json` y `examples/edp/templates/{C-01,Hab-01}.json` a **4 plantillas ortogonales** (`direct`, `inverse`, `perturbation`, `boundary_or_edge_case`) que pasen `check_templates_file_or_dir` al 100% (y limpia archivos `.validation_cache` obsoletos dentro de `examples/{edo,edp}/.validation_cache/` si interfieren, o actualízalos).

## Verificación y Entrega
```powershell
& ".venv\Scripts\python.exe" -m pytest -o addopts="" tests/test_sandbox_adversarial.py tests/test_sandbox_gil_and_circuit_breaker.py tests/test_engine_invariants_adversarial.py tests/test_assemble_katex_and_rationale.py tests/test_assemble_sanitize_katex_r23.py tests/test_katex_prairielearn_tokens.py tests/test_c2c_error_aggregation.py tests/test_template_variability.py tests/test_blind_guess_empirical.py -q
```
Escribe `BRIEFING.md` antes de editar, `handoff.md` al terminar, y envía `DONE:: Stream 1C (<N> passed)` a `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`.
