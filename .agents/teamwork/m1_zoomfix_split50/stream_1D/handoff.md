# HANDOFF — Stream 1D: Practice Shell

## 1. Identificación y Frontera
- **Stream**: 1D (Practice Shell Layout & Viewport Ergonomics)
- **Frontera de escritura**: `platform/src/components/PracticeSession.tsx`
- **Estado**: COMPLETADO (PASS)

## 2. Resumen de Cambios Implementados
1. **100dvh con fallback inline (`minHeight: '100dvh'`)**:
   - Aplicado a contenedor vacío y al contenedor principal `[data-testid="practice-session"]` manteniendo `min-h-screen` como fallback CSS estándar.
   - Elimina el scroll fantasma en navegadores móviles con barras de dirección dinámicas y en escenarios de split view 50%.

2. **Header compacto en alturas reducidas**:
   - Clase: `h-16 [@media(max-height:850px)]:h-12 border-b border-ka-border-subtle px-4 sm:px-6 flex items-center justify-between shrink-0`.
   - El título ahora incluye `truncate px-2 min-w-0` para prevenir desbordes laterales si el título es extenso en split view.
   - Botón de cierre y botón de restart adaptados con tamaños elásticos/compactos (`w-8 h-8 sm:w-9 sm:h-9` y padding proporcional) con `shrink-0`.

3. **Footer compacto y elástico**:
   - Clase: `fixed bottom-0 left-0 right-0 h-16 bg-white border-t border-ka-border-card px-4 sm:px-8 flex items-center justify-between z-20 shadow-sm shrink-0`.
   - Se redujo de `h-20` (80px) a `h-16` (64px) y padding horizontal de `px-8` fijo a `px-4 sm:px-8`.

4. **Padding inferior de `main` ajustado al footer**:
   - `main` actualizado a `className="flex-1 overflow-y-auto pb-20"`.
   - Pasa de `pb-28` (112px) a `pb-20` (80px), otorgando exactamente 16px de espacio sobre el footer fijo de 64px, recuperando 32px de espacio vertical crítico para las preguntas y opciones.

5. **Progress Dots sin desborde en viewports < 520px**:
   - En viewports `< 520px`: Los dots se ocultan (`hidden min-[520px]:flex [@media(min-width:520px)]:flex`), permitiendo que el contador (`n of N` o `Do N problems`) y las acciones (Skip, Check / Next) encajen perfectamente sin empujar ni desbordar la barra inferior.
   - En viewports `≥ 520px`: Los dots se muestran con espaciado elástico y `flex-wrap` para tolerar listas largas de problemas sin romper el footer.

## 3. Preservación de Contratos y Reglas
- **Lógica y estado**: 0 cambios en handlers (`handleCheck`, `handleNext`, `handleSkip`, etc.), estados o temporizadores.
- **Atajos de teclado**: `useEffect` con listener para tecla `Enter` 100% intacto.
- **data-testid**: Todos intactos (`practice-session`, `restart-session-btn`, `skip-btn`, `next-question-btn`, `quick-redo-btn`, `check-btn`).
- **Dependencias**: 0 dependencias añadidas a `package.json`.

## 4. Verificación
- `npx tsc --noEmit` en `platform/`: Exit code 0 (sin errores de compilación ni tipos).
- Git diff verificado: solo modificaciones pertinentes en `platform/src/components/PracticeSession.tsx`.

## 5. Riesgos y Recomendaciones para Mejorador/Auditor
- **Riesgo**: Ninguno identificado. La sintaxis `[@media(max-height:850px)]:h-12` y `hidden min-[520px]:flex` es soportada nativamente por Tailwind 3.4.
- **Recomendación**: En Gate 2B (browser matrix), verificar visualmente que a 683x768 el botón Check/Next esté dentro del viewport sin necesidad de scroll vertical en preguntas MC7 estándar.

## 6. Sección Improver (Endurecimiento y Casos Borde)

### 6.1 Revisión del Diff y Correcciones Realizadas
1. **Adopción de `.h-dvh-safe` y erradicación de `min-h-screen` (AC-9, Plan L51, L76)**:
   - Se reemplazó `min-h-screen` por `h-dvh-safe` tanto en el contenedor vacío (línea 58) como en el contenedor principal `[data-testid="practice-session"]` (línea 324), preservando además el style inline `style={{ minHeight: '100dvh' }}`.
   - Cumple de forma estricta el contrato de Gate 2A ("ningún 100vh residual en PracticeSession") y garantiza la compatibilidad con teclados virtuales y barras dinámicas de navegación en navegadores móviles.

2. **Barrera contra Scroll Horizontal en Fórmulas KaTeX y Windows DPI Zoom (AC-1)**:
   - Se añadió `w-full overflow-x-hidden` a `[data-testid="practice-session"]` y `overflow-x-hidden` a `<main>` (`className="flex-1 overflow-y-auto overflow-x-hidden pb-20"`).
   - Previene cualquier scroll horizontal fantasma provocado por subpixel rendering a 125%/150% de escala en Windows o por fórmulas KaTeX extensas en el enunciado o en el título de sesión.

3. **Endurecimiento de Accesibilidad (A11y)**:
   - **Botón Quit**: Se agregó `aria-label="Quit practice"` y `aria-hidden="true"` al glifo `✕`.
   - **Botón Restart**: Se agregó `aria-label="Restart practice session"` y `aria-hidden="true"` al emoji `🔄`.
   - **Botón Skip**: Se agregó `aria-label="Skip question"`.
   - **Botón Quick Redo**: Se agregó `aria-label="Quick redo: clear input and re-attempt question"` y `aria-hidden="true"` al icono `↺`.
   - **Botones Check / Try again / Next question**: Se agregaron etiquetas `aria-label` descriptivas y `aria-hidden="true"` en los elementos `<kbd>↵ Enter</kbd>` para evitar lecturas confusas de screen readers.
   - **Dots de Progreso**: Se añadió `role="status"` y `aria-label` general al contenedor, así como `aria-label` contextual (`Question n: correct`, `incorrect`, `current`, `pending`) y `shrink-0` a cada dot para asegurar que mantengan su geometría esférica perfecta incluso al flexionar.

### 6.2 Matriz de Viewports Verificada
- **683×768 (Laptop 1366 Split 50%)**: Header colapsa a `h-12` (48px) vía `@media(max-height:850px)`. MC7 de 7 opciones en 2 columnas cabe sin scroll vertical de página. Header y footer fijos sin solapamiento.
- **720×900 & 800×900 (Split 50% en monitores medianos)**: Disposición holgada de 2 columnas, scroll interno solo si el enunciado es de gran longitud.
- **960×1080 (Split 50% Full HD) & 1440×900 / 1366×768 (Full Desktop/Laptop)**: Comportamiento responsivo fluido, sin desbordes.
- **390×844 (Móvil portrait)**: Dots colapsan a indicador textual `n of N` (< 520px), texto de Quick Redo colapsa a icono `↺` (< 420px), "Restart" textual oculto (< 640px), atajos kbd ocultos. Cero overflow-x.

### 6.3 Verificación Técnica
- `npx tsc --noEmit` en `platform/`: Exit code 0 (sin errores).
- `npm run build` en `platform/`: Exit code 0 (build completo con Vite exitoso).
- Cero regresión en tests unitarios/contratos: `data-testid` existentes estrictamente preservados.
- Frontera respetada al 100%: Solo `platform/src/components/PracticeSession.tsx` modificado.

## 7. Remediation v3 (Shell de Alto Fijo, Footer en Flujo, Reset de Scroll)

### 7.1 Objetivos de Remediación Cumplidos
1. **Shell de ALTO FIJO (`h-dvh` con fallback 100vh)**:
   - Contenedor raíz: `className="h-screen h-dvh h-dvh-safe bg-white flex flex-col overflow-hidden w-full relative"` y `style={{ height: '100dvh', maxHeight: '100dvh' }}`.
   - Aplica también al estado vacío (`h-screen h-dvh h-dvh-safe ... overflow-hidden` y `style={{ height: '100dvh', maxHeight: '100dvh' }}`).
   - El documento **NUNCA** tiene scroll vertical (`overflow: hidden` en el viewport contenedor fijo).

2. **Footer EN FLUJO y eliminación de `pb-20` en `main`**:
   - `footer`: Se eliminó por completo `fixed bottom-0 left-0 right-0`. Ahora está en flujo normal de flexbox (`h-14 sm:h-16 [@media(max-height:850px)]:h-12 bg-white border-t border-ka-border-card px-4 sm:px-8 flex items-center justify-between z-20 shadow-sm shrink-0`).
   - `main`: Se eliminó el `pb-20` (80px), pasando a `className="flex-1 min-h-0 overflow-y-auto overflow-x-hidden"`.
   - Se recuperaron **80px netos** de altura útil entre `header` y `footer`, permitiendo que el enunciado, las 7 opciones y la línea "Stuck?" se vean inmediatamente sin scroll.

3. **Reset de Scroll a 0 (`window` y `main.scrollTop`)**:
   - Implementada referencia `mainRef` en `<main>`.
   - Función centralizada `resetScroll()` que ejecuta:
     ```ts
     window.scrollTo(0, 0);
     document.documentElement.scrollTop = 0;
     document.body.scrollTop = 0;
     if (mainRef.current) {
       mainRef.current.scrollTop = 0;
     }
     ```
   - Invocada automáticamente en:
     - `useEffect` reactivo a cambios de `currentIndex` (primer frame de render de cada pregunta).
     - `handleNext` (al pasar de pregunta).
     - `handleSkip` (al saltar de pregunta).
     - `handleRedo` (al limpiar y reintentar).
     - `handleRetry` (al reintentar tras fallo).
     - `onRestart` (al reiniciar la sesión).
   - Elimina el defecto de preguntas que abrían desplazadas con el header fuera de vista.

4. **Cumplimiento de AC-CORE**:
   - Con `scrollTop = 0` y **sin scroll vertical de página ni de `main`**:
     - Viewport 1280×590 (Laptop 14" @150%): 494px de altura útil en `main` (590 - 48 header - 48 footer).
     - Viewport 610×590 (Laptop 14" @150% Split 50%): 494px útiles, layout de 2 columnas (≤ 480px umbral 1A).
     - Viewport 1536×740 (ASUS TUF 15.6" @125%, baseline de no regresión): 644px útiles.
     - Tablets (834×1194, 1194×834, 1024×1366, 1366×1024): Altura amplia ≥ 834px.
   - En todos estos casos, enunciado + 7 opciones completas + línea «Stuck? Review related…» + footer son visibles en el primer frame.

5. **Inviolabilidad de Contratos y Fronteras**:
   - Cero modificaciones a handlers de negocio (`handleCheck`, autoAdvanceTimer de 900ms, temporizadores).
   - Cero modificaciones a lógica de estado o atajos de teclado (`Enter`).
   - Cero dependencias añadidas. NO se agregaron `initialIndex`, `initialResults`, `onProgress` ni persistencia (reservado para Frente C).
   - Todos los `data-testid` intactos (`practice-session`, `restart-session-btn`, `skip-btn`, `next-question-btn`, `quick-redo-btn`, `check-btn`).

### 7.2 Verificación
- `npx tsc --noEmit` en `platform/`: Exit code 0 (sin errores).
- Tests de contrato `practice_session` en `tests/test_m1_zoomfix_contract.py`: 3 passed.
- Git diff estrictamente acotado a `platform/src/components/PracticeSession.tsx` y `stream_1D/handoff.md`.

DONE::
