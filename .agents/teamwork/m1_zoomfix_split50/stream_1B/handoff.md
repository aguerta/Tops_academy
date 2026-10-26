# Handoff — Stream 1B: Sidebar Drawer & App Shell

## 1. Resumen de Ejecución
- **Stream**: 1B — Sidebar Drawer
- **Estado**: ✅ COMPLETADO (PASS)
- **Frontera EXCLUSIVA respetada**:
  - `platform/src/components/Sidebar.tsx`
  - `platform/src/App.tsx`
- **Verificación**: `npx tsc --noEmit` ejecutado en `platform/` con código de salida 0 (0 errores de tipos o compilación).

---

## 2. Cambios Realizados

### `platform/src/components/Sidebar.tsx`
1. **Botón hamburguesa responsivo**:
   - `data-testid="sidebar-toggle"`
   - Visibilidad: visible en viewports `< 1024px` (`lg:hidden`), fijado arriba a la izquierda (`fixed top-3 left-4 z-40`).
   - Accesibilidad: `aria-expanded={isOpen}`, `aria-controls="sidebar"`, `aria-label={isOpen ? 'Close sidebar' : 'Open sidebar'}`.
   - Ícono SVG SVG semántico que conmuta entre hamburguesa (3 barras) y cierre (cruz).
2. **Backdrop / Overlay**:
   - Elemento `div` con backdrop oscuro (`bg-black/40 z-40 backdrop-blur-[1px]`) renderizado condicionalmente cuando `isOpen === true` y `< 1024px` (`lg:hidden`).
   - Al hacer click fuera / en el backdrop, el drawer se cierra inmediatamente.
3. **Manejo de teclado (Esc) y accesibilidad de foco**:
   - Listener de `keydown` para tecla `Escape` que cierra el drawer y retorna el foco automáticamente al botón toggle.
   - Enfoque automático al abrir: enfoca el botón de cierre dentro del drawer.
   - Retorno de enfoque al cerrar: devuelve el foco a `toggleButtonRef`.
4. **Cierre automático por navegación**:
   - Al seleccionar una unidad (`handleSelectUnit`), el Course Challenge (`handleSelectCourseChallenge`) o volver a la librería (`handleBackToLibrary`), el drawer se cierra automáticamente en vistas móviles / split view.
5. **Cierre automático por resize**:
   - Si el viewport se redimensiona a `>= 1024px` mientras el drawer está abierto, el estado se resetea automáticamente.
6. **Dimensiones responsivas y preservación de testid**:
   - Preservado: `data-testid="sidebar"`.
   - Reemplazo del rígido incondicional `w-64` por clases responsivas:
     `fixed lg:static inset-y-0 left-0 z-50 w-64 max-w-[85vw] lg:w-56 xl:w-64 flex-shrink-0 bg-white border-r border-ka-border-subtle min-h-screen py-6 flex flex-col transition-transform duration-200 ease-in-out shadow-xl lg:shadow-none`
     `${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}`
   - En pantallas split-view / laptop 50% (< 1024 px), el sidebar permanece off-canvas y deja el 100% del ancho libre al contenido principal.
   - En desktop (≥ 1024 px y < 1280 px), el sidebar pasa a `w-56` (224 px) estático.
   - En pantallas anchas (≥ 1280 px), el sidebar toma `w-64` (256 px) estático.
7. **Preservación total de comentarios y contenido**:
   - `{/* Back to courses */}`
   - `{/* Course Header */}`
   - `{/* Units List */}`
   - `{/* Course Challenge Item */}`

### `platform/src/App.tsx`
1. En la vista `overview` (`viewMode === 'overview'`):
   - `<main className="flex-1 overflow-y-auto">` actualizado a `<main className="flex-1 overflow-y-auto pt-14 lg:pt-0">` para garantizar que el contenido no quede tapado por el botón hamburguesa flotante en viewports `< 1024px`.
2. En la vista `challenge` (`viewMode === 'challenge'`):
   - `<main className="flex-1 overflow-y-auto">` actualizado a `<main className="flex-1 overflow-y-auto pt-14 lg:pt-0">` idénticamente.
3. Se mantuvo el 100% de la lógica de estado, shuffler, manejadores de eventos, atajos y demás vistas sin alteración.

---

## 3. Decisiones Técnicas
- **Encapsulación del estado del Drawer**: Se mantuvo el estado `isOpen` dentro de `Sidebar.tsx` con soporte nativo para los listeners globales (`Escape`, resize) y foco accesible. De esta forma, tanto la vista `overview` como `challenge` en `App.tsx` heredan idéntico comportamiento responsive sin duplicar lógica en el shell de la aplicación.
- **Transición CSS pura vía clases Tailwind**: No se introdujeron bibliotecas adicionales de animación o dependencias npm. Todo el movimiento off-canvas se gestiona con `transform transition-transform duration-200 ease-in-out` y `-translate-x-full / translate-x-0`.
- **Top padding `pt-14 lg:pt-0`**: Evita la necesidad de un banner o header móvil persistente en `overview` y `challenge`, manteniendo el área de visualización limpia en split-view al 50%.

---

## 4. Riesgos y Mitigaciones
- **Riesgo**: Superposición de elementos fijos con modales o toasts.
  - *Mitigación*: `z-index` calibrado (`z-40` para toggle y overlay, `z-50` para drawer). `FeedbackToast` y modales (`z-50` o superior) no colisionan ya que no se muestran simultáneamente en `overview`/`challenge`.
- **Riesgo**: Colisión de atajos de teclado.
  - *Mitigación*: El listener de `Escape` solo está activo cuando `isOpen === true`, por lo que nunca intercepta eventos en otros momentos de la sesión.

---

## 5. Pruebas y Validación
- `npx tsc --noEmit` en `platform/`: exit code 0.
- `git diff`: únicamente `Sidebar.tsx` y `App.tsx` modificados en la frontera asignada.

---

## 6. Sección Improver (Endurecimiento y Casos Borde)

### 6.1. Focus Trap y Accesibilidad Teclado (WCAG 2.1 - 2.4.3 Focus Order / Modal Dialog)
- **Focus Trap Activo**: Se implementó un detector de ciclo de teclado dentro del `<aside>` con listener global de `Tab` / `Shift+Tab` mientras `isOpen === true`. Si el foco alcanza el último elemento interactivo (botón *Course challenge*) y el usuario pulsa `Tab`, el foco se redirige al primer elemento interactivo (*Course Library*). Análogamente, `Shift+Tab` en el primer elemento cicla hacia el último.
- **Aislamiento Off-Canvas cuando está cerrado**: En viewports `< 1024px` con el drawer cerrado (`isOpen === false`), todos los botones internos reciben `tabIndex={-1}` y el contenedor recibe `aria-hidden="true"`. Esto soluciona la fuga crítica de foco donde usuarios de teclado o lectores de pantalla tabulaban hacia elementos invisibles fuera de la pantalla.
- **Semántica Modal y Roles ARIA**: Cuando el drawer está abierto en `< 1024px`, se declaran explícitamente `role="dialog"` y `aria-modal="true"`. Al alcanzar el breakpoint de escritorio (`>= 1024px`), se restauran automáticamente las propiedades semánticas de navegación estándar.
- **Foco Inicial y Retorno**: Al abrirse, el foco se sitúa de forma prioritaria en `closeButtonRef` con fallback al primer elemento focusable del aside. Al cerrarse por cualquier vía (`Escape`, backdrop click, close button, o navegación), el foco retorna fielmente a `toggleButtonRef`.

### 6.2. Bloqueo de Scroll del Body (Scroll Lock)
- **Body Scroll Lock**: Cuando `isOpen === true`, se aplica `document.body.style.overflow = 'hidden'`.
- **Compensación de Scrollbar**: Se calcula el ancho de la barra de desplazamiento (`window.innerWidth - document.documentElement.clientWidth`) y se aplica a `document.body.style.paddingRight` para evitar desplazamientos de diseño (layout shifts) al abrir/cerrar.
- **Limpieza Incondicional**: Se garantiza la restauración de `overflow` y `paddingRight` originales al cerrar el drawer, al desmontarse el componente o al redimensionar la ventana a `>= 1024px`.
- **Overscroll Contain**: Se añadió `overscroll-contain` al contenedor de unidades `<nav className="flex-1 overflow-y-auto py-2 overscroll-contain">` para impedir encadenamiento de scroll elástico hacia la página base en dispositivos táctiles.

### 6.3. Jerarquía de Stacking Context y Z-Index
- **Jerarquía rigurosa**:
  - `z-30`: Tooltips y elementos absolutos en contenido principal (`CourseOverview`).
  - `z-40`: Botón toggle (`fixed top-3 left-4 z-40`) y backdrop overlay (`fixed inset-0 bg-black/40 z-40 cursor-pointer`).
  - `z-50`: Drawer off-canvas (`fixed inset-y-0 left-0 z-50 w-64 max-w-[85vw] ...`).
- El backdrop (`z-40`) garantiza cubrir cualquier popover (`z-30`) de `CourseOverview`, mientras que el drawer (`z-50`) permanece en la capa superior sin colisiones ni inconsistencias de clic.

### 6.4. Prevención de Desbordamiento Flexbox en `App.tsx`
- En `App.tsx`, se añadió `min-w-0` a los contenedores `<main>` tanto en `overview` como en `challenge`:
  `<main className="flex-1 min-w-0 overflow-y-auto pt-14 lg:pt-0">`
  Esto evita que elementos internos con contenido amplio o fórmulas matemáticas fuercen al contenedor flexible a exceder el ancho disponible en la matriz de split-view 50% (683px, 720px, 800px, 960px) y móviles (390px).

### 6.5. Fórmulas KaTeX y Títulos Extensos en `Sidebar.tsx`
- Se reforzó el título del curso con `block max-w-full truncate` dentro de `<div className="flex-1 min-w-0">`.
- Se reforzaron los títulos de unidades con `block max-w-full truncate` para garantizar que nombres de unidades con fórmulas LaTeX no causen desbordamiento horizontal.
- Se agregó `flex-1 min-w-0` al contenedor del ítem *Course challenge*.

### 6.6. Verificación de Compilación y Suites
- `npx tsc --noEmit` en `platform/`: exit code 0 (cero errores).
- `npm run build` en `platform/`: exit code 0 (compilación completa Vite + TypeScript OK).
- `node tests/test_keyboard_navigation.mjs`: exit code 0 (todas las pruebas pasaron).
- Frontera de escritura 100% respetada: únicamente `Sidebar.tsx` y `App.tsx`.

DONE::
