# Handoff — Stream 2C: Documentación & Actualización de Especificación

**Stream:** 2C  
**Fecha:** 2026-10-26  
**Frontera exclusiva modificada:**
- `FUTURE_MILESTONES.md` (únicamente fila Milestone 1 en §6 y especificación detallada de Milestone 1 en §7)
- `docs/future_milestones/FUTURE_MILESTONES.md` (espejo idéntico byte a byte)

---

## 1. Resumen de Cambios

### A. Matriz Maestra de Priorización de Ingeniería (§6, línea 200)
- Se actualizó el impacto operativo incorporando el soporte de split view 50%.
- Se actualizó el estado de ejecución a: `🛠️ Implementado, pendiente verificación visual` (conforme a la regla de no marcar ✅ hasta que Stream 2B certifique la matriz visual con Playwright).

### B. Especificación Técnica Detallada (§7 Milestone 1)
- **Eliminación de Premisas Técnicas Obsoletas:** Se erradicó la regla de `min-width: 1024px` para la activación del grid de 2 columnas, documentando que en split view al 50% los viewports miden entre 683 px y 960 px, por lo que una media query de escritorio estándar nunca se activaría.
- **Arquitectura de Container Queries:** Se formalizó la estrategia basada en Container Queries nativas (`@container qc (min-width: 600px)`), `max-height` condicional y flexbox/grid elásticos sin dependencias npm externas.
- **Matriz de Viewports Obligatoria:** Documentada explícitamente para pruebas y verificación:
  - `683 × 768`: Laptop 1366 split view 50%.
  - `720 × 900`: Laptop 1440 split view 50%.
  - `800 × 900`: Monitor 1600 split view 50%.
  - `960 × 1080`: Pantalla Full HD 1920 split view 50%.
  - `1366 × 768`: Laptop estándar completa.
  - `1440 × 900`: Laptop widescreen completa.
  - `390 × 844`: Móvil portrait.
- **Componentes Realmente Implementados (Streams 1A–1E):**
  1. **Question Grid (1A):** `.qc-root` (`container-type: inline-size`), `.qc-options` con 2 columnas columna-primero (`grid-auto-flow: column; grid-template-rows: repeat(var(--qc-rows), auto)`), variables elásticas `clamp()`, scroll vertical interno `.qc-options-scroll`, contención anti-desborde KaTeX y utilidad `.h-dvh-safe`.
  2. **Sidebar Drawer (1B):** Sidebar off-canvas en `< 1024px`, botón accesible `sidebar-toggle`, backdrop con overlay, focus trap WCAG 2.1, scroll lock compensado, cierre con `Escape` y `pt-14 lg:pt-0` en `App.tsx`.
  3. **Toast & CoordinatePlane (1C):** `FeedbackToast` adaptado a Bottom Sheet deslizable en `< 1024px` o `height <= 850px` con `max-height: 45dvh`, scroll propio, elevado a `bottom-20` (80 px, garantizando 16 px sobre el footer de 64 px de `PracticeSession` sin obstruir botones de acción); y `CoordinatePlane` con `viewBox`, `max-h-[30dvh]` y aspect ratio.
  4. **Practice Shell (1D):** Layout con `.h-dvh-safe` / `100dvh`, header colapsable a `h-12` en `max-height: 850px`, footer compacto a `h-16`, padding `pb-20` en `main`, dots colapsables a indicador textual en `< 520px` y blindaje `overflow-x-hidden`.
  5. **Vistas Globales (1E):** Grids reconfigurados a `sm:grid-cols-2 xl:grid-cols-3` (activo a 683 px), contención KaTeX estricta, `min-w-0` defensivo, truncamiento corregido en elementos `<span>` y soporte `100dvh`.

### C. Paridad Byte a Byte
- Se sincronizó `FUTURE_MILESTONES.md` con su espejo `docs/future_milestones/FUTURE_MILESTONES.md`.
- Tamaño: exactamente 68,146 bytes en ambos archivos.
- SHA-256: idéntico en ambos archivos.
- Saltos de línea: preservados en LF puro (`\n`), UTF-8 sin BOM.

---

## 2. Decisiones Técnicas

- **Estado Intermedio Riguroso:** Se mantuvo `🛠️ Implementado, pendiente verificación visual` para no usurpar la responsabilidad de Stream 2B ni falsear la aprobación antes del test visual Playwright.
- **Preservación Inviolable del Documento:** No se alteró ninguna otra sección de `FUTURE_MILESTONES.md` (Milestones 2 al 10, apéndices y diagramas permanecieron 100% inalterados).
- **Copia Binaria:** Se utilizó copia exacta de archivo para asegurar que no existan discrepancias de saltos de línea (CRLF vs LF) que rompan el test de paridad.

---

## 3. Verificación de Suites y Compilación

1. **Test de Paridad Byte a Byte:**
   - Comando: `.venv\Scripts\pytest.exe tests/test_platform_katex_admission_guard.py -k TestFutureMilestonesParity -v`
   - Resultado: **PASSED (1 passed)**.
2. **Tests de Contrato Zoom-Fix:**
   - Comando: `.venv\Scripts\pytest.exe tests/test_m1_zoomfix_contract.py -v`
   - Resultado: **PASSED (29 passed)**.
3. **Compilación Frontend:**
   - Comando: `npm run build` en `platform/`
   - Resultado: **PASS** (1101 módulos transformados, 0 errores).

---

## 4. Riesgos y Recomendaciones

- **Sincronización Futura:** Cualquier edición manual futura en `FUTURE_MILESTONES.md` debe sincronizarse inmediatamente a `docs/future_milestones/FUTURE_MILESTONES.md` para evitar fallos en `TestFutureMilestonesParity`.
- **Transición a Done:** Una vez que Stream 2B verifique visualmente la matriz de viewports, la fila de Milestone 1 podrá ser promovida a `✅ Completado`.

---

## 5. Endurecimiento del Mejorador (Improver)

### A. Exactitud Técnica vs Código Real (`platform/src`)
1. **Soporte Dinámico para Opciones Arbitrarias ($3$ a $9$):**
   - Se contrastó la lógica en [`QuestionCard.tsx`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/components/QuestionCard.tsx): la inyección dinámica de `--qc-rows` y `--rows` mediante `Math.max(1, Math.ceil(optionsCount / 2))` asegura que el layout de 2 columnas en orden columna-primero divida equitativamente cualquier número de reactivos (3-4 opciones $\to$ 2 filas; 5-6 opciones $\to$ 3 filas; 7-8 opciones $\to$ 4 filas [MC7 estándar]; 9 opciones $\to$ 5 filas).
   - Se documentó el array `OPTION_LETTERS = ['A'..'I']` que cubre nativamente hasta 9 opciones, con fallback algorítmico a `String.fromCharCode(65 + idx)`.
2. **Blindaje KaTeX Integral en 3 Capas:**
   - Capa 1 (CSS Global): En [`index.css`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/index.css), `.katex-display, .qc-root .katex, .qc-options .katex { display: inline-block; max-width: 100%; overflow-x: auto; overflow-y: hidden; vertical-align: middle; scrollbar-width: thin; }`.
   - Capa 2 (Contenedor Inline): `.qc-root span.inline-block, .qc-options span.inline-block { max-width: 100%; }`.
   - Capa 3 (Vistas Globales Gate 1E): Selectores Tailwind arbitrarios `[&_.katex]:max-w-full [&_.katex]:overflow-x-auto` combinados con `min-w-0` defensivo en flex items para asegurar `document.documentElement.scrollWidth <= window.innerWidth` en todas las pantallas.
3. **Accesibilidad WCAG 2.1 AA / ARIA:**
   - **Sidebar Drawer:** Botón accesible con `aria-expanded`, `aria-controls="sidebar-drawer"`, focus trap bidireccional cíclico (`Tab` / `Shift+Tab`), tecla `Escape`, retorno de foco al toggle button al cerrar, y body scroll lock con compensación de scrollbar.
   - **QuestionCard:** Semántica con `role="radiogroup"` (`aria-label="Answer options"`) en MCQ y `role="group"` (`aria-label="Multiple choice options"`) en `multiple_select`, estados `aria-pressed`, focos accesibles con `focus-visible:ring-2` y `focus-within:ring-2`.
   - **FeedbackToast:** Botones de acción con `aria-label="Quick redo"` y `aria-label="Close feedback"`, glifos decorativos con `aria-hidden="true"`.
   - **CoordinatePlane:** Elemento `<svg>` con `role="img"` y `aria-label` descriptivo paramétrico con los límites de los ejes.
   - **PracticeSession:** Indicador de progreso con `role="status"` y `aria-label`, botones de salida y reinicio con labels accesibles.

### B. Matriz de Viewports y Comportamiento por Alturas
- Se cubrieron exhaustivamente los anchos requeridos: 683, 720, 800, 960, 1366, 1440, 390 px.
- Se documentó la diferenciación por alturas:
  - En alturas bajas ($\le 850\text{ px}$, como 768 px y 844 px): convergen el colapso del header a `h-12` (`[@media(max-height:850px)]:h-12`), el Bottom Sheet en `FeedbackToast` (`max-h-[45dvh]`), la cota en `CoordinatePlane` (`max-h-[30dvh]`), y los tokens de espaciado/tipografía `clamp()` indexados a `vh`.
  - En alturas estándar y altas (900 px y 1080 px): se preserva la holgura nominal completa (header `h-16`, cero scroll vertical de página).

### C. Enlaces Válidos y Paridad Byte a Byte
- Se corrigió el enlace al plan a formato estándar clickable: [`plan.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/m1_zoomfix_split50/plan.md).
- Se verificó que el enlace a `App.tsx` apunte a la ubicación real (`platform/src/App.tsx`).
- Se aseguró la paridad binaria exacta entre `FUTURE_MILESTONES.md` y `docs/future_milestones/FUTURE_MILESTONES.md` (exactamente 70,860 bytes, LF puro, UTF-8 sin BOM, diff idéntico).

### D. Verificación Final
- `pytest tests/test_platform_katex_admission_guard.py -k TestFutureMilestonesParity`: **PASSED** (1 passed).
- `pytest tests/test_m1_zoomfix_contract.py`: **PASSED** (94 passed).
- `npm run build` en `platform/`: **PASS** (1101 módulos transformados en 7.77s, 0 errores).

