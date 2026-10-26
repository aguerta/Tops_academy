# Registro de Milestones Completados y Certificados: Tops Academy

> **Propósito:** archivo de los milestones **cerrados**. Lo pendiente o en curso vive en [`FUTURE_MILESTONES.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/FUTURE_MILESTONES.md) *(espejo de este archivo en `docs/future_milestones/MILESTONES_COMPLETED.md`)*.  
> **Convención de certificación:** cada entrada dice *quién* certificó y *cómo*. «Certificado por el usuario» = prueba manual en sus equipos. «Verificado automáticamente» = tests o E2E con nombre y resultado. Lo no verificado se declara de forma explícita.  
> **Última actualización:** 2026-10-26 (Branch: `main` = `optimizaciones_test`).

---

## Índice

| Milestone | Alcance cerrado | Certificación | Commits |
| :--- | :--- | :--- | :--- |
| **1** Ergonomía Web (Zoom-Fix, Split 50%, Remediación v3) | Laptops 14" a 150%, TUF F15 a 125%, split 50%, tablets; biblioteca de 3 columnas; prosa en fórmulas | Usuario (2026-10-26) + matriz de 7 viewports + 97 contratos | `05c8f4b`, `12042d0`, `950bd20` |
| **2a** Usabilidad móvil | Teléfono: columna única, drawer, footer en flujo | Usuario (2026-10-26) + viewport 390 × 844 en la matriz | los de M1 |
| **11** Carga de cursos — núcleo | Manifest slim, índice con caché, ETag/304/gzip, manifest inline, IndexedDB, prefetch | Automática (12 tests de API + build); ACs de cliente sin medir | `41435c5`, `b73a5ee`, `2051b8b`, `97fa2f3` |

---

## Milestone 1: Web Ergonomía para Laptops, Tablets y Split View 50% (Zoom-Fix + Remediación v3)
* **Estado:** ✅ **Completado y certificado por el usuario (2026-10-26)** en laptop de 14" a 150% de escala (referencia más exigente) y en ASUS TUF Gaming F15 de 15.6" a 125% (referencia que no debe regresar). Verificación automatizada: matriz E2E de 7 viewports, 97 contratos estáticos (`tests/test_m1_zoomfix_contract.py`), tests de teclado/calificación (39,588 casos) y auditoría visual de 200 preguntas aleatorias (50 por curso: Saúl Control Óptimo, Asyntotic Statistics, Estadística v2 Cano y Gavilano). La especificación de abajo describe el estado **final entregado**; la historia de decisiones está en «Remediación v3». Deuda de pruebas declarada: ver *Milestone 1-T* en `FUTURE_MILESTONES.md`.
* **Objetivo Crítico:** Resolver integralmente la adaptabilidad y ergonomía cognitiva tanto en laptops compactas (13"-14", resoluciones 1366×768 o 1440×900) como en escenarios de **Split View al 50% de ancho** (pantalla dividida con visor de PDF, notas o asistente socrático), donde las 7 opciones (MC7) previamente provocaban desborde vertical forzando al usuario a realizar zoom out continuo en el navegador.
* **Requisito de Arquitectura Split-View (50% de ancho de pantalla):**
  - **Superación de Media Queries rígidas:** En split view al 50%, los anchos efectivos de la ventana del navegador oscilan entre 683 px y 960 px. Por consiguiente, una media query tradicional de escritorio (`min-width: 1024px`) **nunca se activa**. La arquitectura se basa en **Container Queries nativas** (ancho del contenedor `.qc-root`), `max-height` condicional y flexbox/grid defensivos sin dependencias npm externas.
  - **Sidebar Desacoplado:** El sidebar fijo `w-64` (que a 683 px consumía el 37% de la pantalla) se transforma en Drawer off-canvas para viewports `< 1024px`, concediendo el 100% del ancho al contenido principal.
  - Plan de ejecución: [`plan.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/m1_zoomfix_split50/plan.md).
* **Matriz de Viewports y Alturas Obligatoria:**
  - `683 × 768`: Laptop 1366 split view 50% — Enunciado y 7 opciones caben en pantalla sin scroll vertical de página ni scroll horizontal (`scrollWidth <= innerWidth`); header colapsa a `h-12` por regla `@media(max-height:850px)`.
  - `720 × 900`: Laptop 1440 split view 50% — Grid de 2 columnas holgado, layout fluido, header `h-16`, cero fricción visual.
  - `800 × 900`: Monitor 1600 split view 50% — Distribución equilibrada 4+3 en 2 columnas, amplio espacio vertical.
  - `960 × 1080`: Pantalla Full HD 1920 split view 50% — Vista split óptima con altura completa de 1080 px y renderizado holgado.
  - `1366 × 768`: Laptop estándar completa — 2 columnas en MC7, header `h-12` (`height <= 850px`), sin zoom out requerido.
  - `1440 × 900`: Laptop widescreen completa — Aprovechamiento total del espacio horizontal y vertical con header `h-16`.
  - `390 × 844`: Móvil portrait — 1 columna determinista ($< 480\text{ px}$ en contenedor), dots compactados a indicador textual `n of N`, cero desborde horizontal.
  - **Comportamiento por Alturas:** En alturas bajas ($\le 850\text{ px}$, como 768 px y 844 px), convergen simultáneamente: colapso de header a `h-12` (ahorro de 16 px), Bottom Sheet en `FeedbackToast` (`max-h-[45dvh]`), contención de `CoordinatePlane` (`max-h-[30dvh]`) y variables fluidas `clamp()` indexadas a `vh`. En alturas estándar y altas (900 px y 1080 px), todos los módulos conservan su amplitud nominal sin comprimir elementos.
* **Componentes Técnicos Implementados:**
  1. **Grid Inteligente de 2 Columnas con Container Queries y Soporte 3–9 Opciones ([`QuestionCard.tsx`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/components/QuestionCard.tsx), [`index.css`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/index.css) - Stream 1A):**
     - Contenedor con `container-type: inline-size; container-name: qc;` (`.qc-root`).
     - Para reactivos MC7 (`multiple_choice_7_options`) y selección múltiple (`multiple_select`): regla `@container qc (min-width: 480px)` que activa 2 columnas con orden columna-primero (`grid-auto-flow: column; grid-template-rows: repeat(var(--qc-rows, var(--rows, 4)), auto); grid-template-columns: repeat(2, minmax(0, 1fr));`).
     - **Cálculo Dinámico de Filas ($3$ a $9$ opciones):** `--qc-rows` y `--rows` computadas dinámicamente mediante `Math.max(1, Math.ceil(optionsCount / 2))` inyectadas inline:
       - 3–4 opciones: 2 filas (2 columnas: 2+1 o 2+2).
       - 5–6 opciones: 3 filas (2 columnas: 3+2 o 3+3).
       - 7–8 opciones: 4 filas (2 columnas: 4+3 [MC7 estándar A–D izq, E–G der] o 4+4).
       - 9 opciones: 5 filas (2 columnas: 5+4).
     - **Letras y Badges:** Soporte predeterminado mediante array `OPTION_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']` con fallback algorítmico a `String.fromCharCode(65 + idx)`.
     - Fallback natural a 1 columna en anchos de contenedor $< 480\text{ px}$ (móviles o paneles ultra-estrechos).
     - Tipografía y espaciados elásticos: `--qc-gap: clamp(0.375rem, 1vh, 0.75rem);`, `--qc-pad: clamp(0.5rem, 1.5vh, 0.875rem);`, `--qc-font: clamp(0.875rem, 1.5vh, 1.125rem);`, `--qc-badge: clamp(1.5rem, 3.2vh, 2rem);`.
     - Scroll vertical interno contenido (`.qc-options-scroll`) para enunciados excepcionalmente largos (`max-height: calc(100dvh - var(--qc-chrome, 14rem))`), preservando header y footer fijos.
     - **KaTeX en línea fluye y envuelve, sin scrollbars:** el `.katex` inline ya **no** usa `overflow-x: auto` ni `display: inline-block` (provocaban barras parásitas dentro de enunciados y opciones); solo `.katex-display` (fórmula en bloque) conserva `overflow-x: auto`. `MathText.tsx` envuelve la fórmula inline en `span.inline` y extrae la prosa larga de `\text{...}` / `\mbox{...}` fuera de KaTeX (`splitMathAndProse`) para que envuelva como texto normal; `min-w-0` defensivo en flex items. **No** se debe forzar `white-space: normal` sobre KaTeX (ver «Remediación v3»).
     - **Accesibilidad y Testabilidad:** Semántica ARIA con `role="radiogroup"` (`aria-label="Answer options"`) en MCQ y `role="group"` (`aria-label="Multiple choice options"`) en selección múltiple; estados `aria-pressed={isSelected}`; foco accesible con `focus-visible:ring-2 focus-visible:ring-ka-blue` y `focus-within:ring-2`; preservación íntegra de `data-testid` (`question-card`, `option-*`, `multiselect-option`, `fill-blank-input`, `hints-toggle`).
  2. **Sidebar Drawer Off-Canvas y App Shell Accesible ([`Sidebar.tsx`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/components/Sidebar.tsx), [`App.tsx`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/App.tsx) - Stream 1B):**
     - Sidebar off-canvas en viewports $< 1024\text{ px}$ con botón flotante accesible (`data-testid="sidebar-toggle"`, `top-3 left-4 z-40`, visible en `lg:hidden`) con `aria-expanded`, `aria-controls="sidebar-drawer"` y `aria-label="Open navigation menu"`.
     - Backdrop con overlay oscuro (`bg-black/40 z-40`), cierre automático con tecla `Escape`, click fuera, redimensionamiento $\ge 1024\text{ px}$ o selección de unidad / Course Challenge.
     - **Accesibilidad WCAG 2.1 AA:** Focus trap bidireccional cíclico (`Tab` / `Shift+Tab`), restauración automática de foco al toggle button tras el cierre, body scroll lock con compensación de ancho de scrollbar para prevenir saltos de layout, y `overscroll-contain`.
     - Ancho adaptativo en escritorio: `w-56` (1024–1279 px) y `w-64` ($\ge 1280\text{ px}$).
     - Padding superior compensatorio `pt-14 lg:pt-0` y `min-w-0` en los `<main>` de `App.tsx` para evitar solapamientos y desbordes flexbox.
  3. **Bottom Sheet Toast y SVG Responsivo ([`FeedbackToast.tsx`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/components/FeedbackToast.tsx), [`CoordinatePlane.tsx`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/components/CoordinatePlane.tsx) - Stream 1C):**
     - `FeedbackToast`: en $< 1024\text{ px}$ o altura $\le 850\text{ px}$, opera como Bottom Sheet deslizable (`fixed z-30 bottom-20 inset-x-3 sm:inset-x-6 max-w-xl mx-auto max-h-[45dvh]`).
     - Posicionamiento: en viewport estrecho o bajo (`max-width: 1023px` o `max-height: 850px`) el toast se ancla a `bottom: 4.5rem` con `max-height: 45dvh`, por encima del footer **en flujo** de `PracticeSession`, sin obstruir nunca los botones de acción (`Skip`, `Check`, `Try again`, `Next question`); en pantallas altas (> 850 px, `lg`) conserva `bottom-20` anclado a la derecha con `w-96`.
     - Scroll interno propio independiente para retroalimentación diagnóstica y soluciones paso a paso, con contención anti-desborde para código y expresiones KaTeX (`.feedback-toast-root pre, code { max-width: 100% !important; overflow-x: auto !important; }`).
     - Accesibilidad de retroalimentación: botones con `aria-label="Quick redo"`, `aria-label="Close feedback"` y etiquetas descriptivas con `aria-hidden="true"` en glifos decorativos.
     - `CoordinatePlane`: SVG responsivo con `viewBox`, `w-full max-w-[340px] max-h-[30dvh] h-auto`, `aspectRatio: width/height`, `role="img"` y `aria-label` descriptivo paramétrico (`from x=${xMin} to ${xMax}, y=${yMin} to ${yMax}`), evitando que planos cartesianos fuercen scroll vertical en pantallas de baja altura.
  4. **Practice Session Shell Ergonómico ([`PracticeSession.tsx`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/components/PracticeSession.tsx) - Stream 1D):**
     - Shell de altura fija: `h-dvh flex flex-col overflow-hidden` (sin scroll fantasma en navegadores móviles); header `shrink-0`, `<main>` con `flex-1 min-h-0 overflow-y-auto overflow-x-hidden` (solo válvula de seguridad) y footer `shrink-0` **en flujo**.
     - Header compacto: colapsa a `h-12` (48 px) en alturas $\le 850\text{ px}` (`[@media(max-height:850px)]:h-12`), recuperando 16 px verticales.
     - Footer en flujo (ya no `fixed`): `h-14 sm:h-16`, y `h-12` en alturas ≤ 850 px, con padding elástico `px-4 sm:px-8`.
     - Sin `pb-20` en `<main>`: al dejar de ser `fixed` el footer, se recuperaron 80 px verticales para el reactivo; `resetScroll()` devuelve el scroll a 0 al cambiar de pregunta (Next, Skip, Redo, Retry, Restart).
     - Indicador de progreso responsivo: en $< 520\text{ px}$ los dots colapsan a indicador textual (`n of N`) con `role="status"`, evitando colisiones en el pie de página; en $\ge 520\text{ px}$, dots con `flex-wrap` y `aria-label` individual por reactivo.
     - Blindaje `overflow-x-hidden` global preservando al 100% la lógica de estado, temporizadores y navegación por teclado (`Enter`).
  5. **Adaptabilidad Global de Vistas y Blindaje KaTeX ([`CourseOverview.tsx`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/components/CourseOverview.tsx), [`CourseLibrary.tsx`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/components/CourseLibrary.tsx), [`MasteryGrid.tsx`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/components/MasteryGrid.tsx), [`MasteryLegend.tsx`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/components/MasteryLegend.tsx), [`PreExerciseModal.tsx`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/components/PreExerciseModal.tsx), [`CompletionScreen.tsx`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/components/CompletionScreen.tsx), [`CourseChallenge.tsx`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/components/CourseChallenge.tsx) - Stream 1E):**
     - Biblioteca: `grid-cols-1 min-[560px]:grid-cols-2 min-[1000px]:grid-cols-3` (3 columnas de 1000 a 1536 px, incluido 1265 px = laptop de 14" a 150% con scrollbar) y tarjetas compactas ≤ 190 px.
     - Se eliminó `[&_.katex]:overflow-x-auto` de todas las vistas (Overview, MasteryGrid, PreExerciseModal, CompletionScreen, CourseChallenge); se mantiene `min-w-0` en flex items para evitar scroll horizontal (`scrollWidth <= innerWidth`).
     - Truncamiento funcional en spans (`block min-w-0` / `inline-block align-bottom min-w-0`), soporte de `100dvh` y `shrink-0` en encabezados y pies de página de modales y pantallas de cierre.

#### Remediación v3 — Frente A (2026-10-26): requisito AC-CORE y escalas reales

**Contexto de uso real:** laptop de 14" a **150%** (≈ 1265–1280 px × ≈ 590 px de viewport; split 50% ≈ 610–640 px), ASUS TUF F15 de 15.6" a **125%** (1536 × 740, referencia que no debe regresar) y tablets de 11" a 14.9".

**AC-CORE (criterio rector):** en el **primer frame de cada pregunta** (`scrollTop = 0`, sin scroll ni interacción) deben verse a la vez el enunciado completo, las 7 opciones completas, la línea `💡 Stuck? Review related articles/videos or use a hint.` (`data-testid="hints-toggle"`) y el footer (`Skip` / `Check`), **sin scroll vertical ni horizontal**.

| Síntoma reportado | Causa raíz | Solución | Archivos |
| :--- | :--- | :--- | :--- |
| Barras horizontales parásitas en enunciados y opciones | `overflow-x: auto` + `display: inline-block` en `.katex` inline y en el wrapper de `MathText` | Eliminados; la fórmula inline fluye como texto | `index.css`, `MathText.tsx`, `FeedbackToast.tsx`, vistas |
| Una sola columna en split 50% a 150% | Umbral `@container` de 600 px vs. ≈ 586–593 px útiles (640 − 15 de scrollbar − 32 de padding) | Umbral de **480 px** (columnas ≥ 230 px) | `index.css`, `QuestionCard.tsx` |
| La última respuesta y «Stuck?» quedaban fuera de vista | Footer `fixed` + `pb-20` en `<main>`, zona de hints alta | Shell flex de altura fija, footer en flujo, línea «Stuck?» compacta, densidad escalonada por `@media (max-height: 720px)` y `(max-height: 620px)` (el TUF a 740 px conserva la densidad base) | `PracticeSession.tsx`, `index.css`, `QuestionCard.tsx` |
| La pregunta siguiente abría ya desplazada | El scroll no se reseteaba | `resetScroll()` al cambiar `currentIndex` y en los handlers | `PracticeSession.tsx` |
| Biblioteca en 2 columnas a 150% | `xl:grid-cols-3` (≥ 1280 px) vs. `innerWidth` de 1265 px (scrollbar de 15 px) | `min-[1000px]:grid-cols-3` | `CourseLibrary.tsx` |
| Saltos de layout al cargar fuentes KaTeX | Sin precarga | 4 `<link rel="preload">` de `woff2` (Main-Regular, Math-Italic, Size1, AMS) | `platform/index.html` |
| Opciones con prosa larga se salían de la tarjeta y se solapaban (p. ej. `$P = 169 \text{ porque los compradores no toleran postergar su compra}$`) | KaTeX convierte los espacios de `\text{}` en `\u00a0` y aplica `white-space: nowrap`: la frase es un bloque indivisible de 450–700 px | `splitMathAndProse` saca la prosa de KaTeX y la deja como texto que envuelve; los operadores cortos (`\text{plim}`) siguen dentro de KaTeX | `MathText.tsx` |

**Lección de regresión (no repetir):** el primer intento de arreglar la prosa fue forzar `white-space: normal` sobre `.katex`, `.katex-html`, `.base` y `.mord.text`. Rompió la tipografía matemática: subíndices, superíndices, `=` y barras de evaluación caían a líneas separadas. KaTeX **depende** de `white-space: nowrap`. Se revirtió en el commit `950bd20`; la solución correcta vive en `MathText.tsx`, no en CSS.

**Commits:** `05c8f4b` (layout responsivo), `12042d0` (prosa en `MathText`), `950bd20` (reversión de `white-space`).

---

## Milestone 2a: Usabilidad Móvil (alcance cerrado del antiguo Milestone 2)
* **Estado:** ✅ **Completado y certificado por el usuario (2026-10-26):** «ahora sí funciona el celular… ya no se tiene que pelear con la plataforma para hacer las preguntas».
* **Entregado (consecuencia directa del Milestone 1):** columna única bajo 480 px de contenedor, sidebar como drawer bajo 1024 px, indicador `n of N` en el footer, toast como bottom sheet, footer en flujo sin scroll fantasma (`h-dvh`) y cero desborde horizontal. El viewport 390 × 844 forma parte de la matriz E2E (PASS).
* **No incluido (permanece abierto como «Milestone 2: PWA Instalable y Modo Offline» en `FUTURE_MILESTONES.md`):** `vite-plugin-pwa`, manifest con iconos, safe areas (`viewport-fit=cover`) y precaching de fuentes KaTeX. Evidencia al 2026-10-26: `platform/package.json` no declara dependencias PWA y `platform/index.html` no tiene `<link rel="manifest">`.

---

## Milestone 11: Carga Rápida de Cursos — núcleo (Manifest, Índice con Caché, ETag y Prefetch)
* **Estado:** ✅ **Núcleo completado (2026-10-26)**, verificado automáticamente en servidor y build. **Lo que NO quedó cerrado** (percepción de lentitud al abrir cursos pesados, esqueleto con progreso, Web Worker, code-splitting y E2E de rendimiento) pasó a *Milestone 11b* en `FUTURE_MILESTONES.md`, junto con el diagnóstico medido (§2.2).
* **Diagnóstico Medido (Causa Raíz de Rendimiento):**
  - **Sobrecarga de Red y Disco:** Los 7 cursos ocupan 51.9 MB en disco. Una solicitud a `GET /api/courses.json` devuelve una respuesta de **43 MB en ~17.4–17.9 segundos**.
  - **Ejecución Redundante en Cada Petición:** `getCourseList()` en `courseServer.cjs` (y en el middleware de Vite) lee del disco, aplica regex de control, ejecuta `JSON.parse` y valida los 7 cursos completos en *cada* solicitud, inyectando el campo `data` con la totalidad del contenido curricular en la lista de la biblioteca (que solo requiere título, descripción y contadores).
  - **Apertura Lenta de Cursos:** `GET /api/courses/:id` re-escanea y re-parsea todos los cursos en disco (~733 ms para un curso de 1.3 MB).
  - **Cero Caché y Build Duplicado:** Sin encabezados `ETag`, sin respuestas HTTP 304 Not Modified, sin compresión gzip/brotli en respuestas de API; build estático emite cada curso 3 veces de forma redundante y en formato *pretty-printed*.
  - **Re-fetch Innecesario:** `App.tsx` re-solicita la lista completa de cursos de 43 MB cada vez que el usuario vuelve a la biblioteca desde un curso.
* **Entregado y medido:**

| Pieza | Archivo | Resultado |
| :--- | :--- | :--- |
| Manifest slim (sin `data`) | `platform/server/courseIndex.cjs` | `dist/api/courses.json`: **59,788 kB → 2.52 kB** (gzip 0.76 kB). En servidor 2,517 bytes, ≈ 2–9 ms en caliente |
| Índice persistente por `mtime + size` | `courseIndex.cjs` → `platform/.cache/course_index.json` (ignorado por git) | `buildIndex()` en caliente < 15 ms; cursos corruptos → `status: "error"` sin afectar a los demás |
| Entrega por id, sin escanear los demás | `platform/server/courseServer.cjs` | `ETag`, `304 Not Modified` y gzip. Medido (servidor local): `saul_control_optimo` 109 KB gzip en ≈ 10 ms; `gavilano_pre_parcial` 13.8 MB → 912 KB gzip en ≈ 66 ms |
| Manifest inline en el HTML | marcador `<!--COURSE_MANIFEST-->` en `platform/index.html`; `transformIndexHtml` en `platform/vite.config.ts`; inyección en `courseServer.cjs` al servir `/` | Biblioteca sin esperar la red; `</script>` y `<!--` escapados |
| Build estático | `platform/vite.config.ts` | Cursos minificados; desaparece el monolito de 59.8 MB |
| Cliente | `platform/src/utils/courseLoader.ts`, `App.tsx`, `CourseLibrary.tsx` | Manifest desde el DOM, caché en memoria + IndexedDB (`tops_academy_cache` / `courses`) por `ETag`, prefetch idle uno a uno, prioridad por `pointerenter` / `focus` / `touchstart`, deduplicación de peticiones en vuelo, sin re-petición de la lista al volver a la biblioteca |
| Pruebas | `tests/test_course_api_manifest.py` | 12/12 PASS; suite completa 1145 passed, 1 skipped; `npm run build` OK |

* **Estado real de los criterios de aceptación:**

| AC | Estado | Nota |
| :--- | :---: | :--- |
| AC-19 manifest < 50 KB, < 100 ms en caliente | ✅ | Cubierto por test |
| AC-22 `/api/courses/:id` sin escanear otros, `ETag`, `304`, compresión | ✅ | Cubierto por test |
| AC-25 cursos corruptos aislados | ✅ | Cubierto por test (directorio temporal) |
| AC-24 build sin duplicados ni pretty-print | 🟡 | Minificado sí y el monolito desapareció; **persisten 2 copias por curso** (`api/courses/<id>.json` y `courses/<archivo>`) por el fallback de candidatos del loader |
| AC-20 biblioteca pinta sin red | 🟡 | Implementado; sin medición E2E |
| AC-21 apertura ≤ 300 ms prefetched / ≤ 1.2 s en frío con esqueleto | 🟡 | Caché y prefetch sí; **sin esqueleto con progreso ni Web Worker** (`courseParse.worker.ts` no existe) |
| AC-23 volver a la biblioteca sin petición | 🟡 | Implementado; sin medición E2E (`tests/e2e_course_loading_perf.mjs` no existe) |

* **Commits:** `41435c5` (servidor + Vite), `b73a5ee` (cliente), `2051b8b` (tests), `97fa2f3` (docs).

---
*Registro de cierre. Para el estado vigente de lo pendiente, ver `FUTURE_MILESTONES.md`.*
