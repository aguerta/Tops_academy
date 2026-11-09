# BRIEFING PRE-FLIGHT — STREAM 1C: SUITE EXHAUSTIVA MILESTONE 4

**Fecha:** 2026-11-08  
**Subagente:** `m4_implementer` (Stream 1C)  
**Objetivo:** Especificación, diseño y verificación de la suite exhaustiva de pruebas `tests/test_milestone4_formc_katex_ast.py` para el cierre al 100% y certificación de Milestone 4.

---

## 1. Hallazgos de Línea Base (Pre-Flight)

1. **`FUTURE_MILESTONES.md` (líneas 381–438):**
   - El Milestone 4 define la transición a un DSL composicional ultra-compacto `Form-C` (-65% tokens de salida), desacoplamiento KaTeX-Python con Pydantic, árbol inductivo `KaTeXAST` (patrón PrairieLearn), canonicalizador algebraico determinista y salvaguarda R-23 anti-sobreescapes.
   - Componentes clave a cerrar:
     * Contrato Pydantic: `ArchetypeKind(str, Enum)` con 4 arquetipos (`direct`, `inverse`, `perturbation`, `boundary_or_edge_case`) y `ShardCompetenceContract(BaseModel)`.
     * Gramática `KaTeXAST`: chequeo inductivo de invariantes (`is_valid`) que prohíbe prosa > 45 chars en `\text{...}`, guiones bajos crudos `_` en `\text{...}`, saltos `\\` fuera de entornos matriciales, llaves dobles `{{...}}`, cuantificadores vacuos (`\forall \varepsilon = 0.05`) y puntos newtonianos en dígitos (`\dot{5}`).
     * Columna exacta de error sintáctico KaTeX vía QuickJS/`pykatex`.
     * Canonicalizador algebraico determinista que colapsa coeficientes unitarios (`$1 x \to x$`, `$-1 x \to -x$`) y dobles signos (`$+ -5 \to -5$`, `$- -5 \to +5$`), con soporte `sympy.latex()`.
     * DSL `Form-C` con auto-exportación AST de `vars` en generadores, catálogo unificado de `RATS`, molde compartido `fmt` y verificadores relacionales de 1 línea `ver(c, v)`.
     * Salvaguarda R-23 anti-sobreescape verificada zero-copy en memoria y pipeline.

2. **`tests/test_pykatex_warn.py`:**
   - Verifica que `pykatex_warnings` en `compile_shard.py` emita advertencias no fatales `[PYKATEX-WARN]` ante errores de sintaxis LaTeX (ej. `\frac{1}`), respete texto plano y tokens `@var@`, y se silencie con `C2C_PYKATEX=off`.

3. **`tests/test_katex_overescape_validator_r23.py`:**
   - Suite completa de 626 líneas que valida la detección zero-copy de R-23 (`\\\\cmd` en JSON / `\\cmd` en memoria), la consolidación de errores idénticos, la permisividad de saltos legítimos `\\` en `bmatrix`/`pmatrix`/`matrix`/`cases`, la detección semántica y el chequeo en cursos publicados en producción con 0 errores R-23.

---

## 2. Contratos de los 6 Componentes Técnicos a Verificar

### Componente 1: Contrato Tipado Pydantic (`engine.katex_ast`)
- **`ArchetypeKind`**: Enum de strings con exactamente 4 miembros: `"direct"`, `"inverse"`, `"perturbation"`, `"boundary_or_edge_case"`.
- **`ShardCompetenceContract`**:
  - `competence_id: str`
  - `archetype: ArchetypeKind`
  - `assumption_tested_id: str | None` (obligatorio no vacío si `archetype == ArchetypeKind.BOUNDARY_OR_EDGE_CASE`, de lo contrario `ValidationError`).
  - `python_pure_logic: str` (valida ausencia de macros LaTeX crudos como `\frac`, `\begin{bmatrix}`; lanza `ValidationError` si contiene LaTeX).
  - `statement_variants_markdown: list[str]` (>= 4 stems con tokens `@PARAM@`).
  - `hints_markdown: list[str]` (3 a 5 pistas socráticas).
  - `solution_markdown: str` (explicación paso a paso con tokens `@PARAM@`).
  - `distractors_markdown: list[tuple[str, str, str]]` (6 3-tuplas `(did, val, rationale)`).
  - Método `.to_form_c_dict() -> dict`: exporta un diccionario compatible con el compilador `compile_shard.py`.

### Componente 2: Interpolación Declarativa `@PARAM@` y `@PARAM:fmt@` (`engine.assemble`)
- **`format_template_string(template_str, variables)`**:
  - Reemplaza `@VAR@` por su valor y `@VAR:.2f@` aplicando la especificación de formato.
  - Preserva intactas las llaves de KaTeX simples y anidadas (`\frac{1}{2}`, `\mathbb{R}`, `x^{2}`, `\dot{k}`).
  - Maneja tipos numéricos, cadenas y valores escalares sin corromper la sintaxis matemática circundante.

### Componente 3: Gramática Inductiva `KaTeXAST` y `pykatex` con Columna Exacta (`engine.katex_ast`)
- **`KaTeXAST` / `parse_katex_ast` / `validate_katex_ast`**:
  - Parsea fórmulas en un árbol inductivo de nodos AST.
  - `is_valid` / `isValid`:
    * Acepta fórmulas válidas y entornos matriciales legítimos (`\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}`, `\text{corto}`).
    * Rechaza prosa > 45 caracteres en `\text{...}` (`[KATEX-AST-PROSE-OVERFLOW]`).
    * Rechaza guión bajo crudo `_` dentro de `\text{...}` (`[KATEX-AST-RAW-UNDERSCORE]`).
    * Rechaza saltos de línea `\\` fuera de entornos matriciales o cases (`[KATEX-AST-ILLEGAL-ROWBREAK]`).
    * Rechaza llaves dobles residuales `{{...}}` (`[KATEX-AST-DOUBLE-BRACES]`).
    * Rechaza notación newtoniana sobre dígitos numéricos `\dot{5}` (`[KATEX-AST-NEWTONIAN-DIGIT]`).
    * Rechaza cuantificadores vacuos `\forall \varepsilon = 0.05` (`[KATEX-AST-VACUOUS-QUANTIFIER]`).
- **`pykatex_validate_with_column(math_str, is_display=False)`**:
  - Devuelve `(ok: bool, error_msg: str | None, col: int | None)`.
  - Ante error sintáctico (ej. `r"\frac{1}"`), devuelve `ok is False`, mensaje no nulo y `col` entero `>= 0`.

### Componente 4: Generación Simbólica `sympy.latex()` y Canonicalizador Algebraico (`engine.katex_ast` y `engine.assemble`)
- **`canonicalize_algebraic_katex(text: str) -> str`**:
  - Normaliza coeficientes unitarios: `$1 x + 3$` $\to$ `$x + 3$`, `$-1 x$` $\to$ `$-x$`, respetando `$10 x$` y `$0.1 x$`.
  - Colapsa dobles signos: `$x + -5$` $\to$ `$x - 5$`, `$x - -5$` $\to$ `$x + 5$`.
- **`sympy_to_katex(expr)` / `sympy_latex_clean(expr)`**:
  - Envuelve `sympy.latex(expr)` garantizando sintaxis válida en KaTeX y normalizando salidas algebraicas y matrices (`sympy.Matrix([[1, 2], [3, 4]])`).

### Componente 5: DSL Composicional `Form-C`, Auto-Exportación AST de `vars` y Precheck (`compile_shard.py` y `shard_precheck.py`)
- **`inject_ast_auto_vars(gen_fn)` / auto-exportación en `compile_shard.py`**:
  - Para generadores Form-C donde se definen variables locales (`tc = 250; th = 500; eta = 0.5`) y se retorna `{"ans": str(eta), "ds": [...]}` sin clave `"vars"`, la transformación exporta automáticamente `"vars": {"tc": tc, "th": th, "eta": eta}`.
- **Compilación Integral Form-C en `tmp_path`**:
  - Shard con 4 arquetipos (MC7 con `fmt=r"$\eta = @X@$"` y `rats=RATS`, 2 FIB, 1 MS con `assumption_id`, stems cartesianos `(CTX, Q)`, verificador de 1 línea `ver(c, v)`).
  - Compila con 0 errores y produce templates válidos en JSON.
- **`shard_precheck.precheck_source`**:
  - Detecta ensamble manual de matrices (`\begin{bmatrix}`) dentro de funciones `gen_*`.

### Componente 6: Salvaguarda Anti-Sobreescape R-23 (`engine.assemble` y `engine.invariants`)
- **`sanitize_katex_syntax(text: str) -> str`**:
  - Colapsa `\\frac` $\to$ `\frac`, preservando saltos legítimos `\\` en matrices y cases.
  - Corrige macros no soportadas como `\centernot\Rightarrow` $\to$ `\nRightarrow`.
- **`validate_katex_syntax`**:
  - Bloquea secuencias `\\frac` en memoria bajo R-23.

---

## 3. Plan de Construcción de `tests/test_milestone4_formc_katex_ast.py`
- Arquitectura modular con clases de test separadas para cada uno de los 6 componentes.
- Importaciones tolerantes a ejecución incremental (manejando fallbacks o mocks si Stream 1A o 1B todavía están terminando de sincronizarse, pero invocando las funciones y clases reales cuando estén presentes).
- Fixtures rápidos y ejecución determinista con tiempo objetivo `< 2 s`.
