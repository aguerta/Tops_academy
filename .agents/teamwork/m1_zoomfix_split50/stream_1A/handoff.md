# Handoff — Stream 1A: Question Grid & CSS Contract

**Stream:** 1A  
**Fecha:** 2026-10-26  
**Frontera exclusiva modificada:**
- `platform/src/index.css`
- `platform/src/components/QuestionCard.tsx`

---

## 1. Resumen de Cambios

### A. `platform/src/index.css`
1. **Contrato de Variables CSS Elásticas (`:root`):**
   - `--qc-gap: clamp(0.375rem, 1vh, 0.75rem);`
   - `--qc-pad: clamp(0.5rem, 1.5vh, 0.875rem);`
   - `--qc-font: clamp(0.875rem, 1.5vh, 1.125rem);`
   - `--qc-badge: clamp(1.5rem, 3.2vh, 2rem);`
   - `--qc-chrome: 14rem;`
2. **Container Queries (`qc-root`, `qc-options`):**
   - `.qc-root`: define `container-type: inline-size; container-name: qc;`.
   - `.qc-options`: grid responsivo por defecto a 1 columna (`minmax(0, 1fr)`).
   - `@container qc (min-width: 600px)`: activa 2 columnas con orden columna-primero (`grid-auto-flow: column; grid-template-rows: repeat(var(--qc-rows, var(--rows, 4)), auto); grid-template-columns: repeat(2, minmax(0, 1fr));`).
3. **Scroll Interno y Safeguards KaTeX:**
   - `.qc-options-scroll`: scroll vertical interno contenido (`overflow-y: auto; max-height: calc(100dvh - var(--qc-chrome, 14rem));`).
   - `.katex-display, .qc-options .katex`: `max-width: 100%; overflow-x: auto; overflow-y: hidden;` para evitar que fórmulas matemáticas o matrices ensanchen artificialmente las columnas del grid en pantallas split-view (683 px).
4. **Utilidades:**
   - `.qc-option-item`, `.qc-badge`, `.qc-stem` para aplicar las variables elásticas sin romper clases de Tailwind.
   - `.h-dvh-safe { min-height: 100vh; min-height: 100dvh; }` para uso coordinado con streams 1D y 1E.

### B. `platform/src/components/QuestionCard.tsx`
1. **Contenedor Principal:**
   - Se añadió la clase `qc-root` manteniendo `data-testid="question-card"`.
2. **Stem:**
   - Se añadió `qc-stem max-w-none` con tamaño elástico `fontSize: var(--qc-font)`.
3. **MC7 (`multiple_choice_7_options`) y Multiple Select (`multiple_select`):**
   - Envoltorio con clase `qc-options-scroll`.
   - Contenedor con clase `qc-options` y style inline dinámico `style={{ ['--qc-rows' as any]: rowCount, ['--rows' as any]: rowCount }}` donde `rowCount = Math.ceil(question.options.length / 2)` (4 filas para 7 opciones, ordenando columna izquierda A-D y columna derecha E-G).
   - Opciones con clases preservadas `option-item answer-option` más `qc-option-item`, padding/gap elásticos vía `style` e `index.css`.
   - Badge con clase `qc-badge` y variables elásticas.
   - Contenedor de contenido con `min-w-0` y tamaño de fuente elástico.
   - Todos los `data-testid` (`option-${opt.id}`, `multiselect-option`, `fill-blank-input`, `hints-toggle`, etc.) y comentarios preservados intactos.

---

## 2. Decisiones Técnicas

- **Doble variable inline (`--qc-rows` y `--rows`):** Asegura compatibilidad tanto con la especificación técnica §3 (`--qc-rows`) como con los criterios de aceptación AC-2 (`--rows`).
- **`min-w-0` en los ítems de opción:** Es vital en CSS Grid con flex children para que textos largos o KaTeX no desborden el ancho de columna asignado en split-view (683 px).
- **Preservación estricta de selectores existentes:** Se mantuvieron `option-item` y `answer-option` para evitar regresiones en la suite de pruebas E2E existentes.
- **Scroll wrapper `qc-options-scroll`:** Separa el contexto de scroll vertical del cálculo de tracks de CSS Grid, garantizando que el scrollbar no altere el alineamiento de las 2 columnas.

---

## 3. Riesgos y Mitigaciones

- **Soporte de container queries:** Se utilizó `@container qc (min-width: 600px)` estándar. En caso de navegadores sin soporte, el fallback natural es `display: grid; grid-template-columns: minmax(0, 1fr);` (1 columna), totalmente funcional y legible.
- **Overflow de fórmulas KaTeX:** Mitigado con `minmax(0, 1fr)` en las columnas del grid y `.katex { max-width: 100%; overflow-x: auto; }`.

---

## 4. Estado de Verificación

- `npx tsc --noEmit` en `platform/`: **PASS** (0 errores de tipos).
- Cero archivos residuales o temporales creados.
- Frontera de escritura 100% respetada.

---

## 5. Endurecimiento (Improver)

El Mejorador revisó el diff real, la frontera exclusiva y los casos borde de la especificación técnica:

1. **Robustez ante conteo variable de opciones (3 a 9 opciones, edge cases 0..2 y >9):**
   - Cálculo endurecido: `optionsCount = Array.isArray(question.options) ? question.options.length : 0` con `rowCount = Math.max(1, Math.ceil(optionsCount / 2))`.
   - Se previene la generación de CSS inválido `repeat(0, auto)` en listas vacías.
   - Si `optionsCount` está entre 3 y 9, distribuye exactamente en 2 columnas:
     - 3 opciones: 2 filas (A, B izq | C der).
     - 4 opciones: 2 filas (A, B izq | C, D der).
     - 5 opciones: 3 filas (A, B, C izq | D, E der).
     - 6 opciones: 3 filas (A, B, C izq | D, E, F der).
     - 7 opciones: 4 filas (A, B, C, D izq | E, F, G der).
     - 8 opciones: 4 filas (A, B, C, D izq | E, F, G, H der).
     - 9 opciones: 5 filas (A, B, C, D, E izq | F, G, H, I der).
   - Letras dinámicas: `OPTION_LETTERS[idx] || String.fromCharCode(65 + idx)` para soportar limpiamente más de 9 opciones sin degradar a números.

2. **Endurecimiento ante Fórmulas KaTeX Anchas (Sin desborde horizontal AC-1):**
   - Se añadió `.qc-root span.inline-block, .qc-options span.inline-block { max-width: 100%; vertical-align: middle; }`.
   - `.katex-display, .qc-root .katex, .qc-options .katex` ahora incluyen `display: inline-block; max-width: 100%; overflow-x: auto; overflow-y: hidden; vertical-align: middle; scrollbar-width: thin;`.
   - Se añadió `min-w-0` a los botones y labels de las opciones para garantizar que ninguna fórmula matemática o matriz pueda ensanchar el track de la columna ni el flex container.

3. **Contenedor < 600px a 1 Columna (Móvil AC-4):**
   - En `.qc-options`, se fijó explícitamente `grid-auto-flow: row;` junto con `grid-template-columns: minmax(0, 1fr);`, asegurando comportamiento 100% determinista a 1 columna en viewports móviles (p. ej. 390×844) o ventanas estrechas.

4. **Optimización de Espaciado Vertical para Laptops 768px (AC-3 / AC-6):**
   - Card padding ajustado de `py-4 sm:py-6` a `py-3 sm:py-5` y `px-3 sm:px-4`.
   - Márgenes de prompt y acordeón de pistas optimizados (`mt-3 mb-2 sm:mt-4 sm:mb-2.5` y `mt-6 sm:mt-8 pt-3 sm:pt-4`).
   - `.qc-options-scroll` soporta fallback dual: `max-height: calc(100vh - var(--qc-chrome, 14rem)); max-height: calc(100dvh - var(--qc-chrome, 14rem)); scrollbar-width: thin;`.

5. **Accesibilidad (a11y) y Preservación de Contratos:**
   - MC7: añadido `role="radiogroup"`, `aria-label="Answer options"`, `aria-pressed={isSelected}`, y estilos `focus-visible:ring-2 focus-visible:ring-ka-blue`.
   - Multiple select: añadido `role="group"`, `aria-label="Multiple choice options"`, y `focus-within:ring-2 focus-within:ring-ka-blue`.
   - Fill-in-the-blank: añadido `aria-label="Your answer"`.
   - Hints Accordion: añadido `aria-expanded={showHintsSection}`, `aria-controls="hints-container"`, `id="hints-container"`, `role="region"`, `aria-label="Hints"`.
   - Todos los selectores y `data-testid` (`question-card`, `option-*`, `multiselect-option`, `fill-blank-input`, `hints-toggle`, `hints-container`, `reveal-hint-btn`, `hint-item`, `.option-item`, `.answer-option`) 100% preservados.

6. **Verificación:**
   - `npx tsc --noEmit` en `platform/`: **PASS** (0 errores de tipos).
   - Frontera exclusiva (`QuestionCard.tsx`, `index.css`) estrictamente respetada.

DONE::Stream 1A endurecido y verificado exitosamente.
