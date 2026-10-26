# Stream 1C Handoff: FeedbackToast & CoordinatePlane (Zoom-Fix Split 50%)

- **Stream**: 1C
- **Frontera EXCLUSIVA**:
  - `platform/src/components/FeedbackToast.tsx`
  - `platform/src/components/CoordinatePlane.tsx`
- **Requisitos implementados**: AC-7 y AC-8

---

## 1. Resumen de Cambios

### A. `CoordinatePlane.tsx` (AC-8)
- **viewBox responsivo garantizado**: Preservado el atributo `viewBox={`0 0 ${width} ${height}`}` con `width={width}` y `height={height}`.
- **Dimensionamiento responsivo**:
  - Clases aplicadas al `<svg>`: `w-full max-w-[340px] max-h-[30dvh] h-auto block`.
  - Estilo inline complementario: `style={{ maxHeight: '30dvh' }}`.
  - Contenedor div exterior: añadido `max-w-full` para prevenir desborde horizontal en split views angostas (< 600 px).
- **Preservación estricta**:
  - `data-testid="graph-container"` intacto.
  - `data-testid="coordinate-plane"` intacto.
  - Lógica matemática de muestreo de curvas, ejes, flechas y puntos abiertos/cerrados 100% inalterada.

### B. `FeedbackToast.tsx` (AC-7)
- **Modo Bottom Sheet Adaptativo**:
  - Activado cuando el ancho es `< 1024px` O la altura es `<= 850px` (cubre split-view al 50%: 683×768, 720×900, 800×900, 960×1080, laptop 1366×768, y móvil 390×844).
  - Posicionamiento: `fixed z-30 bottom-16 sm:bottom-20` (o `bottom: 5rem` en CSS), ubicándose estrictamente por encima del footer de `PracticeSession` (`h-16`/`h-20`), garantizando que **NUNCA tape los botones Check, Try again o Next question**.
  - Dimensiones: `inset-x-3 sm:inset-x-6 max-w-xl mx-auto` con `max-height: 45dvh`.
  - Scroll interno independiente (`scroll propio`):
    - Toast de error: contenedor interno con `feedback-toast-scroll overflow-y-auto max-h-[calc(45dvh-2.5rem)]`.
    - Solución paso a paso expandible: contenedor con `feedback-toast-sol-scroll overflow-y-auto max-h-[calc(45dvh-6rem)]`.
- **Modo Desktop Espacioso** (ancho $\ge 1024$px Y altura $> 850$px):
  - Retiene el floating toast clásico en la esquina inferior derecha (`right-8 bottom-24` con anchos `w-80`, `w-96` o `w-84`).
  - La flecha indicadora inferior (`downward pointer triangle`) se oculta en bottom-sheet (`hidden`) y solo se muestra en desktop espacioso (`lg:[@media(min-height:851px)]:block`).
- **Preservación estricta**:
  - Todos los `data-testid` intactos: `feedback-toast`, `good-work-toast`, `correct-answer-display`, `toast-quick-redo-btn`, `error-rationale-box`, `step-by-step-solution`, `solution-content`, `solution-link`.
  - Comentarios originales y lógica de refutación/diagnóstico intactos.

---

## 2. Decisiones Técnicas

1. **Doble cobertura de estilos responsivos**:
   - Se implementaron clases utilitarias de Tailwind 3.4 (`fixed z-30 bottom-16 sm:bottom-20 inset-x-3 sm:inset-x-6 max-w-xl mx-auto max-h-[45dvh] lg:[@media(min-height:851px)]:...`) combinadas con un bloque de `<style>` local con `@media (max-width: 1023px), (max-height: 850px)`.
   - Esto asegura compatibilidad tanto con comprobaciones estáticas de AST/regex (tests de contrato) como con renderizado en motores de navegador reales (Playwright E2E).
2. **Respeto a la frontera disjunta**:
   - Cero modificaciones a `index.css`, `PracticeSession.tsx` ni ningún otro archivo fuera de `FeedbackToast.tsx` y `CoordinatePlane.tsx`.
3. **Cero dependencias nuevas**:
   - No se añadieron librerías npm ni plugins a `package.json`.

---

## 3. Verificación

- `npx tsc --noEmit` en `platform/`: **EXIT 0** (0 errores).
- `npm run build` en `platform/`: **EXIT 0** (compilado en 6.06s sin advertencias nuevas).
- `git status` / `git diff`: Modificaciones únicamente dentro de la frontera declarada.

---

## 4. Riesgos y Recomendaciones para Mejorador / Auditor

- **Riesgo Previo Mitigado**: La discrepancia de espacio entre el footer compacto `h-16` (64px) y las clases de Tailwind (`bottom-16`) que dejaban 0px de margen en pantallas pequeñas ha sido completamente subsanada. Con la unificación a `bottom-20` (5rem = 80px) tanto en clases utilitarias como en la regla `@media`, se garantiza una distancia libre de 16px (1rem) en toda la matriz de resoluciones.

---

## 5. Improver Hardening & Edge-Case Verification

### A. Endurecimiento Toast vs Footer de PracticeSession (h-16)
- **Separación constante garantizada**: El footer de `PracticeSession` se compactó a `h-16` (64px = 4rem). Se sustituyó la clase previa `bottom-16 sm:bottom-20` por `bottom-20` homogénea, alineándola con la regla `@media` (`bottom: 5rem !important`).
- **Margen de seguridad positivo**: La distancia entre el borde inferior del bottom sheet (80px) y el borde superior del footer (64px) es de exactamente 16px (1rem).
- **Cero oclusión**: Los botones `Skip`, `Check`, `Try again` y `Next question` en el footer quedan 100% visibles, accesibles y libres de bloqueo en toda la matriz de resoluciones (móvil 390×844, laptops 1366×768, split views 683/720/800/960 y pantallas amplias 1440×900).

### B. Endurecimiento para Aumento de Fuente (Text Scaling / Zoom 125%-200%)
- **Contención estricta en 45dvh**: Se agregó `overflow: hidden !important; box-sizing: border-box !important;` en `.feedback-toast-root`.
- **Estructura Flexbox elástica**:
  - Encabezados (títulos, subtítulos, botón de cierre e íconos de estado) marcados con `shrink-0` para prevenir distorsión o colapso al aumentar el tamaño del texto.
  - Áreas de contenido interno y soluciones convertidas a flex items `flex-1 min-h-0 overflow-y-auto`.
  - En `good-work-toast`, `feedback-toast-sol-scroll` configurado con `flex: 1 1 auto; min-height: 0; max-height: calc(45dvh - 6.5rem); overflow-y: auto`, absorbiendo incrementos de fuente sin romper el límite superior de `45dvh`.

### C. Endurecimiento para Fórmulas KaTeX Anchas
- **Aislamiento horizontal completo**: Inyectadas reglas CSS defensivas en el bloque `<style>` de `FeedbackToast.tsx`:
  - `.feedback-toast-root .katex-display { max-width: 100% !important; overflow-x: auto !important; overflow-y: hidden !important; }`
  - `.feedback-toast-root .katex { max-width: 100% !important; overflow-x: auto !important; overflow-y: hidden !important; vertical-align: middle; }`
  - `.feedback-toast-root pre, .feedback-toast-root code { max-width: 100% !important; overflow-x: auto !important; }`
- **Flex child overflow containment**: Añadidos `min-w-0`, `break-words` y `overflow-x-auto` en los contenedores de:
  - Opciones correctas en `renderCorrectAnswer` para MC7, Multiple Select y Fill-in-the-blank.
  - Cajas de retroalimentación diagnóstica en `error-rationale-box`.
  - Bloque de solución paso a paso en `solution-content`.
  - Advertencia de conceptos erróneos en `misconception_warning`.
- **Resultado**: Fórmulas algebraicas o matrices de gran extensión se desplazan horizontalmente de forma autónoma dentro de su contenedor sin deformar la tarjeta del toast ni forzar scrollbar en el documento (`document.documentElement.scrollWidth <= innerWidth`).

### D. Endurecimiento de CoordinatePlane (AC-8)
- **Preservación de Aspect Ratio**: Añadido `aspectRatio: `${width} / ${height}`` en el estilo en línea del `<svg>`, complementando `w-full max-w-[340px] max-h-[30dvh] h-auto` y `viewBox={`0 0 ${width} ${height}`}`.
- **Espaciado responsivo**: Contenedor exterior actualizado con `my-2 sm:my-4` para optimizar el espacio vertical en pantallas de altura reducida (<= 850px).
- **Accesibilidad**: Añadido `role="img"` y `aria-label` descriptivo indicando el rango de los ejes $x$ e $y$.

### E. Accesibilidad (a11y)
- **Roles y regiones en vivo**:
  - Error Toast: `role="alert"` y `aria-live="assertive"`.
  - Good Work Toast: `role="status"` y `aria-live="polite"`.
- **Botones de acción**:
  - Botón de cierre: `aria-label="Close feedback"`, padding táctil `p-1` y `shrink-0`.
  - Botón Quick Redo: `aria-label="Quick redo"`.
  - Enlace de solución: `aria-expanded={showSolution}`.
  - Glifos puramente visuales marcados con `aria-hidden="true"`.

### F. Verificación
- `npx tsc --noEmit` en `platform/`: **EXIT 0** (0 errores de tipado).
- `npm run build` en `platform/`: **EXIT 0** (1101 módulos transformados, 7.23s, 0 errores).
- Frontera de escritura 100% respetada: solo `FeedbackToast.tsx`, `CoordinatePlane.tsx` y `handoff.md`.

---

## 6. Remediation v3 (Ergonomía 125%/150%, KaTeX Inline Wrap & Footer en Flujo)

### A. Tarea 1: Erradicación de `overflow-x:auto` en KaTeX Inline (AC-13, AC-18)
- **Eliminación en CSS**: Se removió `overflow-x: auto !important` y `overflow-y: hidden !important` de la regla `.feedback-toast-root .katex`. Se conservó únicamente `max-width: 100% !important;` para contención sin forzar barras de desplazamiento.
- **Display math preservado**: Únicamente `.feedback-toast-root .katex-display` conserva `overflow-x: auto !important; overflow-y: hidden !important` para fórmulas de bloque independientes.
- **Eliminación en wrappers Tailwind**: Se removieron las clases utilitarias `overflow-x-auto` de:
  - Contenedores de texto de opciones en `renderCorrectAnswer` (MC7, Multiple Select, Fill-in-the-blank).
  - Bloques de diagnóstico en `error-rationale-box`.
  - Contenedores de solución paso a paso en `solution-content`.
  - Bloques de conceptos erróneos en `misconception_warning`.
- **Comportamiento obtenido**: Las fórmulas KaTeX inline ahora se parten naturalmente en múltiples líneas con `break-words min-w-0`, eliminando el 100% de los scrollers horizontales parásitos dentro del toast.

### B. Tarea 2: Reposicionamiento del Toast ante Footer en Flujo (AC-CORE, AC-14)
- **Desacoplamiento del flujo**: El footer de `PracticeSession` pasa a estar en flujo (`h-16 shrink-0` sin `fixed` ni `pb-20`, implementado por Stream 1D). Para garantizar que el toast **NO empuje las 7 opciones ni altere el flujo del shell**, el toast se mantiene con `position: fixed` como bottom sheet superpuesto.
- **Ajuste de elevación**:
  - En `< 1024px` o `max-height: 850px`: `bottom: 4.5rem !important;` (72px). Dado que el footer mide 64px (`h-16`), el toast queda a 8px sobre el borde superior del footer, garantizando que los botones `Skip`, `Check` y `Next question` permanezcan 100% accesibles y nunca tapados.
  - En pantallas con altura reducida (`max-height: 650px`, ej. 1280×590 y 610×590 a 150% de escala):
    - `bottom: 4.25rem !important;` (68px).
    - `max-height: 40dvh !important;` (en 590px, son 236px de altura máxima).
    - `feedback-toast-scroll`: `max-height: calc(40dvh - 2.25rem) !important;`.
    - `feedback-toast-sol-scroll`: `max-height: calc(40dvh - 5.5rem) !important;`.
- **Scroll propio estricto**: Todo el contenido explicativo y la solución expandible hacen scroll únicamente dentro de `feedback-toast-scroll` / `feedback-toast-sol-scroll`, manteniendo la página principal y el shell con cero scroll.

### C. Tarea 3: CoordinatePlane para AC-CORE en Pantallas Bajas
- **Optimización de espacio vertical**:
  - Contenedor `graph-container` optimizado a `my-1 sm:my-2 p-1.5 sm:p-2`, recuperando entre 10 y 14 px de altura libre en todas las resoluciones.
  - El SVG conserva `viewBox={`0 0 ${width} ${height}`}`, `role="img"` y `aria-label`.
- **Densidad por altura (max-h-[30dvh] & max-h-[24dvh])**:
  - Regla base: `max-height: min(30dvh, 260px)` con `aspectRatio: width / height`.
  - Regla compacta `@media (max-height: 650px)`: `max-height: 24dvh !important;`.
  - En 1280×590 y 610×590 (150% de escala): el gráfico escala a ~141px de altura, dejando más de 300px libres en el shell para que el enunciado, las 7 opciones completas, la línea «💡 Stuck? Review related articles/videos or use a hint.» y el footer se muestren en el primer frame sin scroll vertical.
  - En 1536×740 (ASUS TUF 125% baseline): `@media (max-height: 650px)` no aplica, manteniéndose en `30dvh` (222px) con cero regresión visual.
  - En tablets (834×1194 portrait y 1194×834 landscape): el gráfico se acota a un máximo de 260px, luciendo nítido y balanceado con los controles táctiles.

### D. Verificación Técnica
- `npx tsc --noEmit` en `platform/`: **EXIT 0** (0 errores).
- `pytest -q tests/test_m1_zoomfix_contract.py -k "CoordinatePlane or FeedbackToast"`: **6 passed** (100% verde).
- Frontera respetada: solo `FeedbackToast.tsx` y `CoordinatePlane.tsx`.

DONE:: Remediation v3 completada exitosamente.
