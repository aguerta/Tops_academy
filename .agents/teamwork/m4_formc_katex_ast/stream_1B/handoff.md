# HANDOFF — STREAM 1B (Milestone 4: `compile_shard.py` & `shard_precheck.py`)

## 1. Archivos Modificados (Exclusive Write Boundary)
- `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\compile_shard.py`
- `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\shard_precheck.py`
- `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\m4_formc_katex_ast\stream_1B\BRIEFING.md`
- `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\m4_formc_katex_ast\stream_1B\handoff.md`

Ningún archivo fuera de la frontera de escritura exclusiva fue modificado ni creado.

## 2. Implementaciones Realizadas

### A. Mejoras en `compile_shard.py`
1. **Soporte Dual para `ShardCompetenceContract` (Pydantic M4.1) en `TEMPLATES`:**
   - Se implementó la función helper `normalize_form_c_template(t: Any) -> Any`:
     * Si `hasattr(t, "to_form_c_dict")` y es callable, invoca `t.to_form_c_dict()`.
     * Si `hasattr(t, "model_dump")` y es callable, invoca `t.model_dump()` y mapea `competence_id -> cid`, `archetype -> archetype`, `assumption_tested_id -> assumption_id`, `statement_variants_markdown -> stems`, `hints_markdown -> hints`, `solution_markdown -> sol`, preservando atributos/callables no serializados (`gen`, `ver`, `fmt`, `rats`, etc.).
   - Se integró la normalización en todos los puntos de ingesta y empalme de `TEMPLATES`:
     * Inicialización de `tuple_records` desde `base_templates`.
     * Reemplazo y adición en el empalme de fijaciones (`fix_templates`).
     * Bucle de verificación de paridad de competencias (`found_cids`).
     * Bucle principal de compilación de plantillas.
   - De este modo, `compile_shard.py` soporta de manera transparente (1) instancias `ShardCompetenceContract`, (2) diccionarios `Form-C` y (3) 9-tuplas `Form-B`.

2. **Auto-Exportación AST de `vars` en Generadores `Form-C` (M4.5) & Soporte Polimórfico (Callable / Code Str):**
   - Se implementó la función `inject_ast_auto_vars(code_or_fn: Any) -> Any`:
     * Si recibe un objeto callable (`callable(code_or_fn)`): extrae su código fuente mediante `inspect.getsource`, aplica la transformación AST recursiva, recompila la función en el namespace de sus globales y retorna el objeto callable transformado (o envuelto).
     * Si recibe una cadena (`isinstance(code_or_fn, str)`): analiza el AST de la función generadora mediante un `ast.NodeTransformer`.
     * Recolecta en orden las variables locales asignadas en el cuerpo (`ast.Assign`, `ast.AnnAssign`), excluyendo nombres internos/reservados (`_RESERVED_VAR_NAMES = {"rng", "r", "arch", "ans", "correct", "ds", "distractors", "options", "v1", "vl", "_"}` y variables con prefijo `_`).
     * En cada `ast.Return` que retorna un diccionario con claves de salida (`"ans"`, `"correct"`, `"ds"`, `"distractors"`, `"options"`) y carece de `"vars"`, inyecta automáticamente `"vars": {name: name, ...}` (incluyendo `"ans"` si `"ans"` o `"correct"` fue retornado).
     * Si el generador ya incluye `"vars"` o no se modificó, preserva el código intacto.
   - Se integró `inject_ast_auto_vars` en `extract_function_code` cuando `target_name == "generate_params"`.
   - Se implementó el wrapper runtime `_wrap_gen_raw_with_auto_vars(raw_fn, transformed_code)` para re-compilar la función transformada en el namespace global de `gen_raw` y asegurar que cualquier invocación en memoria durante los dry-runs (`call_with_timeout`, `res_test`, `_eval_tuple_output`, etc.) retorne `vars` auto-exportado.
   - Se añadieron salvaguardas de fallback para `"vars"` en todas las inspecciones de resultado en memoria (~2430, ~2700, ~3140, ~3315).

3. **Reporte de Columna Exacta en `pykatex_warnings` (M4.3):**
   - En `pykatex_warnings`, cuando `_pykatex.renderToString` lanza excepción:
     * Extrae la columna buscando `r"position\s+(\d+)"` en el mensaje de error o calculando la posición del carácter `\u0332` en el fragmento subrayado.
     * Si la columna está disponible, incluye `[col=N]` en el formato `[!] Warning: [PYKATEX-WARN] {context}: {msg} [col=N] (span: ...)`.
     * Mantiene compatibilidad total con la suite de pruebas `test_pykatex_warn.py`.

### B. Mejoras en `shard_precheck.py`
1. **Detección estática AST `[SYMPY-LATEX-MATRIX]`:**
   - Dentro de funciones generadoras (`gen_*`, `_gen*`), detecta literales de cadena (`ast.Constant`), f-strings (`ast.JoinedStr`), operaciones `%` (`ast.BinOp(op=ast.Mod)`) o `.format()` que contengan entornos de matrices (`\begin{bmatrix}`, `\begin{pmatrix}`, `\begin{vmatrix}`, `\begin{matrix}`) ensambladas con interpolación manual.
   - Emite advertencia temprana recomendando usar `sympy.latex()`.
2. **Detección estática AST `[KATEX-AST-CHECK]`:**
   - Detecta cualquier constante string con `\text{` que exceda 45 caracteres (mediante analizador de llaves balanceadas que soporta macros internas y caracteres de escape).
   - Detecta `\dot{` aplicado a dígitos numéricos (`r"\\dot\{\s*\d+\s*\}"`), advirtiendo que la notación newtoniana es exclusiva para variables/símbolos.

## 3. Remediación Gate 1 Audit
- **Causa raíz:** `test_inject_ast_auto_vars_scalar_locals` pasaba `sample_gen` (un objeto función callable) directamente a `inject_ast_auto_vars`.
- **Corrección:** `inject_ast_auto_vars` detecta `callable(code_or_fn)`, extrae el código con `inspect.getsource(code_or_fn)`, transforma el AST, recompila y retorna el callable listo para ejecutarse con `rng`.
- **Verificación:** `pytest -o addopts="" tests/test_milestone4_formc_katex_ast.py -v` pasa 23/23 tests (100%).

## 4. Pruebas y Verificación
Se ejecutó la suite completa de pruebas:
- `pytest -o addopts="" tests/test_milestone4_formc_katex_ast.py -v`:
  **23 passed in 1.54s (100% PASS, 0 failures, 0 skips)**
- `pytest -o addopts="" tests/test_pykatex_warn.py tests/test_c2c_author_speedups.py tests/test_compile_shard.py`:
  **26 passed in 3.65s (100% PASS)**
- `pytest -o addopts="" tests/test_sweetspot_v35_cta_and_shards.py -k "not TestCatalogAndPromptsAlignment"`:
  **11 passed, 3 deselected in 4.51s (100% PASS)**
- Script exhaustivo de sanity check que validó:
  1. Contrato dual `ShardCompetenceContract` (método `to_form_c_dict` y `model_dump`).
  2. Auto-exportación AST de `vars` tanto con string como con callable.
  3. Reporte de columna `[col=1]` en advertencias PyKaTeX.
  4. Pre-check estático de `[SYMPY-LATEX-MATRIX]`.
  5. Pre-check estático de `[KATEX-AST-CHECK]` (`\text{... > 45}` y `\dot{5}`).
  **Resultado: ALL STREAM 1B DELIVERABLES VERIFIED SUCCESSFULLY!**
