# Pre-Flight Briefing — Stream 2A: Contract Tests (Milestone 1 Zoom-Fix & Split-View 50%)

- **Stream**: 2A (Contract tests)
- **Frontera exclusiva de escritura**: `tests/test_m1_zoomfix_contract.py`, `.agents/teamwork/m1_zoomfix_split50/stream_2A/BRIEFING.md`, `.agents/teamwork/m1_zoomfix_split50/stream_2A/handoff.md`.
- **Frontera de lectura**: `platform/src/components/QuestionCard.tsx`, `platform/src/index.css`, `platform/src/components/Sidebar.tsx`, `platform/src/components/PracticeSession.tsx`, `platform/src/components/CoordinatePlane.tsx`, `platform/src/components/FeedbackToast.tsx`, `platform/src/App.tsx`.

---

## 1. Baseline Checks

1. **Platform Build**:
   - Comando: `npm run build` en `platform/`
   - Resultado: **EXIT 0** (transformó 1101 módulos, built en ~6.98s sin errores de TypeScript ni Vite).
2. **Pytest Baseline**:
   - Comando: `.\pytest.cmd -q tests/test_platform.py`
   - Resultado: **19 passed** en 12.69s.
3. **Git Status**:
   - Rama activa: `optimizaciones_test`
   - Estado de frontera: Archivo `tests/test_m1_zoomfix_contract.py` aún no existe (se creará de forma limpia en este stream).

---

## 2. Hallazgos del Código Real (Gate 1 Inspeccionado)

| Archivo | Verificaciones Observadas en Código Real |
|---|---|
| `platform/src/index.css` | Define `.qc-root { container-type: inline-size; container-name: qc; }`. Define `.qc-options` con grid y `@container qc (min-width: 600px)` con `grid-template-columns: repeat(2, minmax(0, 1fr))` y `grid-auto-flow: column; grid-template-rows: repeat(var(--qc-rows, var(--rows, 4)), auto);`. Define tokens `clamp(...)` en `:root` (`--qc-gap`, `--qc-pad`, `--qc-font`, `--qc-badge`). Define `.qc-options-scroll` con `100dvh` y clase `.h-dvh-safe` con fallback `100vh` + `100dvh`. KaTeX overflow guards presentes. |
| `platform/src/components/QuestionCard.tsx` | Aplica `.qc-root`, `.qc-stem`, `.qc-options-scroll`, `.qc-options`, `.qc-option-item`, `.qc-badge`. Setea inline styles `--qc-rows` y `--rows` calculados como `Math.max(1, Math.ceil(optionsCount / 2))`. Conserva data-testids: `question-card`, `option-${opt.id}`, `multiselect-option`, `fill-blank-input`, `hints-toggle`, `hints-container`, `reveal-hint-btn`, `hint-item`. |
| `platform/src/components/Sidebar.tsx` | Implementa comportamiento responsive con breakpoint `1024` (`lg`): drawer off-canvas en `< 1024px`, botón toggle hamburguesa (`data-testid="sidebar-toggle"`, `lg:hidden`), backdrop overlay, aside con `data-testid="sidebar"`, responsive sizing `w-64 max-w-[85vw] lg:w-56 xl:w-64` y `-translate-x-full lg:translate-x-0`. Escape key y focus trap implementados. Cero `w-64` incondicional sin layout adaptativo. |
| `platform/src/components/PracticeSession.tsx` | Utiliza `.h-dvh-safe` y `style={{ minHeight: '100dvh' }}`. Cero ocurrencias residuales de `100vh` en el código ejecutable. Data-testids preservados: `practice-session`, `restart-session-btn`, `skip-btn`, `next-question-btn`, `quick-redo-btn`, `check-btn`. Header compacto en `[@media(max-height:850px)]:h-12`. |
| `platform/src/components/CoordinatePlane.tsx` | Contiene SVG responsivo con atributo `viewBox`, `data-testid="coordinate-plane"`, `data-testid="graph-container"`, clases `w-full max-w-[340px] max-h-[30dvh]`. |
| `platform/src/components/FeedbackToast.tsx` | Responsivo a `< 1024px` y `max-height: 850px` como bottom sheet con `max-height: 45dvh` y scroll propio. Data-testids preservados: `feedback-toast`, `good-work-toast`, `toast-quick-redo-btn`, `error-rationale-box`, `correct-answer-display`, `step-by-step-solution`, `solution-content`, `solution-link`. |
| `platform/src/App.tsx` | Soporta el sidebar drawer en `< 1024px` con padding superior en main `pt-14 lg:pt-0` para no colisionar con el toggle hamburguesa, permitiendo ancho 100% en split view 50%. |

---

## 3. Plan de Pruebas de Contrato (Adversarial Static Analysis)

1. **Parser de código limpio**: Utilizar extractor/stripper robusto de comentarios (eliminar `// ...`, `/* ... */`, `{/* ... */}`) para evitar falsos positivos o falsos negativos si un patrón aparece solo en comentarios.
2. **Suite granular en pytest**:
   - `test_index_css_container_queries`: Verifica `.qc-root`, `container-type`, `@container qc`, `repeat(2`, `grid-auto-flow: column`.
   - `test_index_css_fluid_clamp_tokens`: Verifica `clamp(` en variables de espaciado y tipografía.
   - `test_index_css_dynamic_viewport_height`: Verifica `.h-dvh-safe` y `100dvh`.
   - `test_question_card_contract_and_testids`: Verifica uso de clases `qc-*`, estilos dinámicos `--qc-rows`, y todos los `data-testid`.
   - `test_sidebar_responsive_breakpoint_and_toggle`: Verifica breakpoint `lg`, `sidebar-toggle`, drawer classes, `aria-expanded`, y ausencia de `w-64` rígido e incondicional.
   - `test_practice_session_no_residual_100vh_and_testids`: Verifica ausencia de `100vh` residual fuera de fallback seguro, presencia de `100dvh`/`h-dvh-safe`, y todos los `data-testid`.
   - `test_coordinate_plane_responsive_viewbox`: Verifica `viewBox`, `max-w-[340px]`, `max-h-[30dvh]`, y `data-testid`.
   - `test_feedback_toast_responsive_bottom_sheet_and_testids`: Verifica `45dvh`, media query responsive, y todos los `data-testid`.
   - `test_app_layout_responsive_padding`: Verifica `pt-14 lg:pt-0` en `main`.
   - `test_comment_stripping_adversarial_guard`: Verifica que el stripper de comentarios detecte y descarte patrones espurios dentro de comentarios.
