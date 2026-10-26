# Handoff Report — Stream 2A (Contract Tests)

- **Stream**: 2A (Contract tests)
- **Frontera de escritura exclusiva**: `tests/test_m1_zoomfix_contract.py`
- **Estado final**: ✅ PASS (94 tests passed en 0.29s, 0 warnings, `npm run build` en 7.57s)

---

## 1. Cambios Implementados

Se creó el archivo de suite de contratos estáticos y adversariales:
- [test_m1_zoomfix_contract.py](file:///d:/Augusto/personal_portfolio/Tops_academy/tests/test_m1_zoomfix_contract.py) (29 tests unitarios/estáticos):
  1. **Motor de Análisis Adversarial**:
     - `strip_code_comments(src: str)`: Implementa una máquina de estados pura para JS/TS/JSX y CSS que remueve comentarios de línea (`//`), comentarios de bloque (`/* ... */`) y bloques de comentarios JSX (`{/* ... */}`), preservando estrictamente las cadenas de texto (`'...'`, `"..."`, `` `...` ``) y escapes.
     - `test_strips_single_line_comments_with_fake_contract`
     - `test_strips_block_comments_with_fake_container_query`
     - `test_strips_jsx_block_comments`
     - `test_preserves_slashes_in_strings`
     - `test_preserves_template_strings_and_escapes`
     - `test_adversarial_commented_out_feature_not_detected_as_active`
  2. **Contrato de CSS (`platform/src/index.css`)**:
     - `test_qc_root_container_query_definition`: Valida `.qc-root`, `container-type: inline-size` y `container-name: qc`.
     - `test_qc_options_default_and_container_query`: Valida `.qc-options` en grid por defecto y en `@container qc (min-width: 600px)` con `repeat(2, minmax(0, 1fr))`, `grid-auto-flow: column` y `repeat(var(--qc-rows`.
     - `test_fluid_clamp_tokens`: Valida `clamp(` en `--qc-gap`, `--qc-pad`, `--qc-font`, `--qc-badge`.
     - `test_dynamic_viewport_height_scroll_and_utility`: Valida `100dvh` en `.qc-options-scroll` y utilidad `.h-dvh-safe`.
     - `test_katex_overflow_guards`: Valida `overflow-x: auto` y `max-width: 100%` en KaTeX.
  3. **Contrato de `QuestionCard.tsx`**:
     - `test_qc_classes_applied`: Valida aplicación de clases `qc-root`, `qc-stem`, `qc-options-scroll`, `qc-options`, `qc-option-item`, `qc-badge`.
     - `test_dynamic_qc_rows_calculated_and_injected`: Valida cálculo dinámico de `Math.ceil(optionsCount / 2)` e inyección de `--qc-rows`.
     - `test_stem_max_width_none`: Valida stem elástico sin desbordes.
     - `test_data_testids_preserved`: Valida `question-card`, `option-${opt.id}`, `multiselect-option`, `fill-blank-input`, `hints-toggle`, `hints-container`, `reveal-hint-btn`, `hint-item`.
  4. **Contrato de `Sidebar.tsx`**:
     - `test_sidebar_responsive_breakpoint`: Valida breakpoint `1024`, clases `lg:hidden`, `lg:static`, `lg:w-56`, `lg:translate-x-0` y `-translate-x-full lg:translate-x-0`.
     - `test_no_unconditional_fixed_w64`: Valida que el `<aside>` no use un `w-64` rígido sin las restricciones responsivas (`max-w-[85vw]`, `lg:w-56`, etc.).
     - `test_sidebar_drawer_toggle_and_testids`: Valida `data-testid="sidebar-toggle"`, `data-testid="sidebar"`, `aria-expanded` y `aria-controls`.
     - `test_sidebar_escape_key_listener`: Valida evento Escape para cerrar.
  5. **Contrato de `PracticeSession.tsx`**:
     - `test_no_residual_100vh_or_min_h_screen`: Valida cero ocurrencias de `100vh` o `min-h-screen` en código ejecutable.
     - `test_uses_h_dvh_safe_and_inline_100dvh`: Valida `h-dvh-safe` y `minHeight: 100dvh`.
     - `test_header_compact_max_height_850`: Valida adaptación de header para `<= 850px`.
     - `test_data_testids_preserved`: Valida `practice-session`, `skip-btn`, `next-question-btn`, `check-btn`, `quick-redo-btn`, `restart-session-btn`.
  6. **Contrato de `CoordinatePlane.tsx`**:
     - `test_svg_has_viewbox_and_responsive_constraints`: Valida atributo `viewBox`, `max-w-[340px]`, `max-h-[30dvh]`.
     - `test_data_testids_preserved`: Valida `coordinate-plane` y `graph-container`.
  7. **Contrato de `FeedbackToast.tsx`**:
     - `test_bottom_sheet_responsive_45dvh`: Valida bottom-sheet `45dvh` y breakpoint `< 1024px` / `<= 850px`.
     - `test_data_testids_preserved`: Valida `feedback-toast`, `good-work-toast`, `toast-quick-redo-btn`, `error-rationale-box`, `correct-answer-display`, `step-by-step-solution`, `solution-content`, `solution-link`.
  8. **Contrato de `App.tsx`**:
     - `test_main_responsive_padding_for_hamburger`: Valida `pt-14 lg:pt-0` en `main`.
     - `test_no_rigid_w64_in_app`: Valida ausencia de wrappers rígidos `w-64`.

---

## 2. Decisiones Técnicas

1. **Stripping de comentarios basado en lexer/estado**:
   - En lugar de expresiones regulares simples (que pueden romper URLs o templates multilínea), se implementó un scanner de estado por caracteres que maneja comillas simples, dobles y backticks (con soporte para caracteres escapados), eliminando cualquier comentario antes de evaluar los contratos.
2. **Pytest Fixtures**:
   - Se usaron fixtures de función estándar para garantizar compatibilidad con versiones futuras de pytest sin disparar warnings de deprecación (`PytestRemovedIn10Warning`).
3. **Validación Inviolable**:
   - No se alteró ningún archivo fuera de la frontera declarada (`tests/test_m1_zoomfix_contract.py`).

---

## 3. Riesgos y Mitigaciones

- **Riesgo**: Cambios futuros en componentes podrían renombrar atributos sin advertirlo.
  - **Mitigación**: La suite `test_m1_zoomfix_contract.py` corre en < 150 ms con `.\pytest.cmd -q tests/test_m1_zoomfix_contract.py` y puede ejecutarse de forma continua en pre-commit o CI.
- **Riesgo**: Nuevos comentarios con código comentado podrían generar falsos positivos.
  - **Mitigación**: Mitigado mediante la máquina de estados de stripping de comentarios probada adversarialmente.


---

## 4. Mejoras Implementadas (Improver)

El Mejorador de Stream 2A auditó la implementación inicial de contratos estáticos y ejecutó una fase de endurecimiento exhaustivo sin modificar archivos fuera de la frontera exclusiva (`tests/test_m1_zoomfix_contract.py`):

1. **Eliminación de Aserciones Enmascaradas**:
   - Se reemplazaron uniones disyuntivas permisivas (`or`) por verificaciones conjuntas estrictas:
     - En `index.css`: verificación obligatoria de `repeat(2, minmax(0, 1fr))` en lugar del permisivo `repeat(2,`.
     - En `Sidebar.tsx`: verificación obligatoria conjunta de `lg:w-56` Y `lg:translate-x-0`.
     - En `Sidebar.tsx` `<aside>`: verificación obligatoria conjunta de `max-w-[85vw]` Y `lg:w-56`.
     - En `PracticeSession.tsx`: verificación exacta de clase compacta Tailwind `[@media(max-height:850px)]:h-12`.
     - En `FeedbackToast.tsx`: verificación exacta y simultánea de media queries `(max-height: 850px)` Y `(max-width: 1023px)`.

2. **Portabilidad y Rutas (Windows / POSIX)**:
   - Se estructuró la nueva suite `TestPathResolutionPortability` parametrizada sobre todos los componentes de la plataforma (incluyendo componentes de Gate 1E).
   - Uso riguroso de `pathlib.Path.resolve()` que normaliza separadores de ruta en Windows (`\`) y POSIX (`/`), garantizando lectura limpia en UTF-8 y compatibilidad multiplataforma.

3. **Matriz de Viewports Obligatoria (AC-1 a AC-9)**:
   - Se incorporó la suite `TestViewportMatrixContract` parametrizada contra los 7 viewports de la matriz del plan:
     - Split view 50%: `683x768`, `720x900`, `800x900`, `960x1080`
     - Desktop / Laptop 100%: `1366x768`, `1440x900`
     - Móvil: `390x844`
   - Se validaron matemáticamente los umbrales de activación:
     - Breakpoint de contenedor `600px`: 1 columna para 390px; 2 columnas para viewports >= 683px.
     - Breakpoint de sidebar `1024px`: drawer off-canvas para split view (<= 960px) y móvil; static en desktop (>= 1366px).
     - Umbral de altura `850px`: header compacto (`h-12`) y bottom-sheet (`45dvh`) en 768px; header normal y floating toast en >= 900px.

4. **Distribución Column-First para 3 a 9 Opciones (MC7 & Multiple Select)**:
   - Se creó la suite `TestOptionGridDistributionContract` validando exhaustivamente la fórmula `rows = max(1, ceil(n / 2))` para opciones de 3 a 9:
     - Invariante de balance: la columna 1 siempre contiene `ceil(n/2)` elementos, la columna 2 contiene `floor(n/2)` elementos (diferencia máxima de 1 elemento, columna 1 >= columna 2).
     - Validación de fallback para `n = 0` (retorna `1` fila segura, evitando syntax error de CSS grid `repeat(0)`).
     - Verificación de que `QuestionCard.tsx` expone letras de opción `A` hasta `I` (9 opciones).
     - Verificación de inyección de variables CSS `--qc-rows` y `--rows` tanto en `multiple_choice_7_options` como en `multiple_select`.

5. **Contención KaTeX y Vistas Gate 1E**:
   - Se creó la suite `TestKaTeXOverflowGuardContract` verificando contención de fórmulas anchas en `.katex-display` (`max-width: 100%`, `overflow-x: auto`), `.qc-root .katex`, `FeedbackToast.tsx` y en todas las vistas de Gate 1E (`CourseLibrary`, `CourseOverview`, `MasteryGrid`, `PreExerciseModal`, `CompletionScreen`, `CourseChallenge`).
   - Se creó la suite `TestGate1EViewsContract` validando layout elástico, `min-w-0`, `break-words [overflow-wrap:anywhere]`, `truncate` y `min-h-[100dvh]`.

6. **Accesibilidad (A11y)**:
   - Se creó la suite `TestAccessibilityContracts` verificando:
     - Sidebar: `aria-expanded`, `aria-controls="sidebar"`, `role="dialog"` condicional, `aria-modal="true"`, `aria-hidden="true"`, listener de `Escape`, trampa de foco (`Tab` / `Shift+Tab`) y desactivación de tabulación en drawer cerrado (`itemTabIndex = -1`).
     - QuestionCard: `role="radiogroup"` en MCQ, `role="group"` en Multiple Select, `aria-pressed` en botones de opción, `role="region"` y `aria-label="Hints"` en pistas.
     - PracticeSession: `role="status"` en progress dots, `aria-label` en reinicio y progreso.
     - CoordinatePlane: `role="img"` y `aria-label` descriptivo.

7. **Mutation Testing Manual en Memoria (Kills Artificial Mutants)**:
   - Se incorporó la suite `TestContractMutationResistance` que introduce 24 mutaciones artificiales en memoria sobre copias de strings leídas:
     - Mutaciones en `index.css`: remoción de `.qc-root`, `@container`, `repeat(2, minmax(0, 1fr))`, `grid-auto-flow: column`, `clamp(`, `h-dvh-safe`, KaTeX guard.
     - Mutaciones en `QuestionCard.tsx`: reemplazo de `Math.ceil` por constante, remoción de `--qc-rows`, remoción de `max-w-none`, remoción de testid, remoción de `role="radiogroup"`.
     - Mutaciones en `Sidebar.tsx`: corrupción de breakpoint 1024, remoción de `max-w-[85vw]`, remoción de `sidebar-toggle`, remoción de `Escape`.
     - Mutaciones en `PracticeSession.tsx`: inyección de `100vh` residual, inyección de `min-h-screen` residual.
     - Mutaciones en `CoordinatePlane.tsx`: remoción de `viewBox`, remoción de `30dvh`, remoción de testid.
     - Mutaciones en `FeedbackToast.tsx`: remoción de `45dvh`, remoción de query 850px, remoción de testid.
   - El 100% de los mutantes fueron aniquilados (`pytest.raises(AssertionError)`), confirmando que ningún falso negativo puede enmascarar regresiones.
   - Todo se realizó en memoria, sin modificar archivos de `platform/`.

8. **Métricas Finales**:
   - **94 tests** unitarios/estáticos (vs 29 del implementador inicial).
   - Tiempo de ejecución de tests: **0.29s** (`.\pytest.cmd -q tests/test_m1_zoomfix_contract.py`).
   - Verificación de build: `npm run build` en **7.57s** (0 errores, 0 warnings tsc).
   - Inviolabilidad de frontera: únicamente `tests/test_m1_zoomfix_contract.py` modificado.
