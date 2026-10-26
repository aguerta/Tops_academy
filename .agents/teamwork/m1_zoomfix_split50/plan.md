# Plan — Milestone 1: Web Ergonomía Laptop + Split-View 50% (Zoom-Fix)

Skill: `flash-triad-orchestrator` · prefijo de subagentes: `m1zf` · Model=`flash` · Frontera de escritura: `platform/src/**` + `tests/` (solo archivos listados).

## 1. Diagnóstico (código real leído)

| # | Hallazgo | Archivo |
|---|----------|---------|
| D1 | Opciones en `space-y-2` vertical, `p-3.5`, badge `w-8 h-8`: 7 opciones ≈ 600 px solo de opciones → desborde en 768 px de alto. | `QuestionCard.tsx` L77, L142 |
| D2 | **Sidebar fijo `w-64` (256 px)** en overview/challenge. A 50% de 1366 px (683 px) consume el 37% del ancho. | `Sidebar.tsx` L27, `App.tsx` L284/L353 |
| D3 | Premisa original del spec (`min-width:1024px`) es **incorrecta para split view**: a 50% el viewport mide 683–960 px, la media query nunca se activaría. Hay que usar **container queries** (ancho del contenedor) + `max-height`, no el ancho de pantalla. | spec M1 |
| D4 | Footer `fixed h-20` + `pb-28` en main: ~112 px de alto perdidos; `min-h-screen` (100vh) sobreestima con barra del navegador. | `PracticeSession.tsx` L319, L354, L385 |
| D5 | `FeedbackToast` (12 KB) flotante: puede tapar opciones/footer en pantallas bajas y estrechas. | `FeedbackToast.tsx` |
| D6 | `CoordinatePlane` SVG sin `viewBox` responsivo garantizado. | `CoordinatePlane.tsx` |
| D7 | Stem `max-w-3xl` y `px-8` del footer no se adaptan; Tailwind `sm:` (640) se activa a 683 px pero `md:` (768) no. | varios |
| D8 | Tailwind 3.4 sin plugin de container queries; se usará **CSS nativo** en `index.css` (`container-type: inline-size`, `@container`) para no agregar dependencias. | `index.css` |

## 2. Requisitos (criterios de aceptación medibles)

Matriz de viewports obligatoria: **683×768, 720×900, 800×900, 960×1080, 1366×768, 1440×900, 390×844 (móvil)**.

- **AC-1** Sin scroll horizontal en ninguna vista (library, overview, challenge, pre_exercise, practice, completed) en toda la matriz.
- **AC-2** MC7 en contenedor ≥ 600 px de ancho: 2 columnas, orden columna-primero (4 izq + 3 der), usando `grid-auto-flow: column; grid-template-rows: repeat(var(--rows), auto)` con `--rows = ceil(n/2)`. Aplica también a `multiple_select`.
- **AC-3** En 683×768 y 1366×768 (`max-height: 850px`), enunciado corto + 7 opciones + header + footer caben sin scroll vertical de página (scroll interno del bloque de opciones solo si el enunciado es largo; header y footer fijos).
- **AC-4** Contenedor < 600 px: 1 columna (móvil).
- **AC-5** Sidebar: ≥ 1024 px viewport → fijo (`w-64`, o `w-56` si < 1280); < 1024 px → drawer off-canvas con botón hamburguesa, overlay, cierre con Esc/click fuera. Con 50% de pantalla el contenido principal usa el 100% del ancho.
- **AC-6** Tipografía/espaciado elásticos: `clamp(0.875rem, 1.5vh, 1.125rem)` para padding/gap de opciones y stem; badge `clamp(1.5rem, 3.2vh, 2rem)`.
- **AC-7** `FeedbackToast` en < 1024 px o `max-height: 850px`: bottom sheet con `max-height: 45dvh`, scroll propio, sin tapar el botón Check/Next.
- **AC-8** `CoordinatePlane`: `viewBox` + `w-full max-w-[340px]` y `max-height: 30dvh` en pantallas bajas.
- **AC-9** `100dvh` en lugar de `100vh`/`min-h-screen` en `PracticeSession` (teclado virtual).
- **AC-10** Cero regresión: `npm run build` (tsc + vite) verde; `data-testid` existentes intactos (`question-card`, `option-*`, `check-btn`, `next-question-btn`, `skip-btn`, `sidebar`, `practice-session`, `hints-toggle`…); suite `pytest` existente sin nuevos fallos.
- **AC-11** Navegación por teclado (Enter = check/next) y lógica de estado de `PracticeSession` **no se tocan**.

## 3. Diseño técnico (contrato compartido entre streams)

Contrato CSS (lo define 1A en `index.css`, lo consumen 1D/1E por nombres de clase; nadie más escribe `index.css`):

```css
.qc-root      { container-type: inline-size; container-name: qc; }
.qc-options   { display:grid; gap: var(--qc-gap); grid-template-columns: minmax(0,1fr); }
@container qc (min-width: 600px) {
  .qc-options { grid-template-columns: repeat(2, minmax(0,1fr));
                grid-auto-flow: column; grid-template-rows: repeat(var(--qc-rows,4), auto); }
}
:root { --qc-gap: clamp(.375rem,1vh,.75rem); --qc-pad: clamp(.5rem,1.5vh,.875rem);
        --qc-font: clamp(.875rem,1.5vh,1.125rem); --qc-badge: clamp(1.5rem,3.2vh,2rem); }
.qc-options-scroll { overflow-y:auto; max-height: calc(100dvh - var(--qc-chrome,14rem)); }
.katex-display, .qc-options .katex { max-width:100%; overflow-x:auto; overflow-y:hidden; }
```

Clase de utilidad para layout de pantalla completa: `.h-dvh-safe { min-height:100vh; min-height:100dvh; }` (1A la define; 1D la usa).

## 4. Gates y Streams (fronteras de escritura 100% disjuntas)

### GATE 0 — Pre-Flight (solo lectura, 1 worker `m1zf_implementer` por stream, escribe `BRIEFING.md`)
Cada Implementador lee archivos reales + `git status` y registra baseline: `npm run build` y `pytest -q -x` (conteo de tests) en su `BRIEFING.md`.

### GATE 1 — Implementación UI (4 streams en paralelo, sin dependencias entre sí)

| Stream | Escribe SOLO | Entrega |
|--------|--------------|---------|
| **1A** Question grid | `platform/src/components/QuestionCard.tsx`, `platform/src/index.css` | Clases `qc-*`, `--qc-rows` inline style, grid 2 col columna-primero para MC7/MS, clamp(), scroll interno `qc-options-scroll`, stem `max-w-none` dentro de contenedor, katex overflow guard, utilidad `.h-dvh-safe`. Mantener `data-testid` y comentarios. |
| **1B** Sidebar drawer | `platform/src/components/Sidebar.tsx`, `platform/src/App.tsx` | Drawer < 1024 px (hamburguesa fija arriba-izq, overlay, Esc, `aria-expanded`, foco), `w-56/w-64` en desktop, `main` con `pt-14 lg:pt-0`, `data-testid="sidebar"` preservado, `data-testid="sidebar-toggle"` nuevo. |
| **1C** Toast & SVG | `platform/src/components/FeedbackToast.tsx`, `platform/src/components/CoordinatePlane.tsx` | Bottom sheet responsivo (AC-7) y SVG responsivo (AC-8). |
| **1D** Practice shell | `platform/src/components/PracticeSession.tsx` | `h-dvh-safe` + layout flex-col con `main` scrollable, header `h-12` en `max-h-850`, footer compacto (`h-16`, `px-4 sm:px-8`), `pb` calculado al footer, progress dots con `flex-wrap`/colapso a "n of N" en < 520 px; **sin tocar handlers/estado**. |
| **1E** Resto de vistas | `platform/src/components/{CourseOverview,MasteryGrid,MasteryLegend,CourseLibrary,PreExerciseModal,CompletionScreen,CourseChallenge}.tsx` | Auditar y corregir a 683 px: grids `grid-cols-1 sm:grid-cols-2 xl:grid-cols-3`, `min-w-0`, `truncate`, paddings elásticos, cero overflow-x. |

Dependencia: 1D/1E usan `.h-dvh-safe` de 1A. Para mantener disjunción se acuerda el nombre; si 1A no lo ha publicado, 1D usa utilidades Tailwind equivalentes `min-h-screen` + style `minHeight:'100dvh'` inline (sin esperar).

Cada stream ejecuta Tríada completa: **Implementador → Mejorador → Auditor** (`m1zf_auditor` escribe solo en `.agents/teamwork/m1_zoomfix_split50/stream_XX_audit/`).

### GATE 2 — Pruebas y verificación (tras PASS de Gate 1; 3 streams disjuntos)

| Stream | Escribe SOLO | Entrega |
|--------|--------------|---------|
| **2A** Contract tests | `tests/test_m1_zoomfix_contract.py` | Tests pytest estáticos sobre el código fuente: existen `qc-options`, `@container`, `repeat(2`, `grid-auto-flow: column`, `clamp(`, `dvh`, `data-testid` preservados, Sidebar con breakpoint `lg`, ausencia de `w-64` incondicional, ningún `100vh` residual en PracticeSession, `viewBox` en CoordinatePlane. Adversarios: falsos positivos por comentarios. |
| **2B** Browser matrix | `tests/e2e_m1_viewport_matrix.mjs` (Playwright **verificado**: Chromium v1243 ya instalado en `%LOCALAPPDATA%\ms-playwright`; usar `npx -y playwright@1.63.0` — es la versión que coincide con ese build — sin tocar `package.json` y SIN `playwright install`. Para importar la API desde el `.mjs`, ejecutar con `npx -y -p playwright@1.63.0 node tests/e2e_m1_viewport_matrix.mjs` o `createRequire` sobre el cache de npx; si falla, fallback `SKIPPED` documentado) | Para cada viewport de la matriz: levantar `vite preview`, abrir un curso, entrar a práctica con un MC7, medir `document.documentElement.scrollWidth <= innerWidth`, que `#check-btn` esté dentro del viewport, y guardar screenshots en `.agents/teamwork/m1_zoomfix_split50/screens/`. |
| **2C** Docs | `FUTURE_MILESTONES.md` (solo §7 Milestone 1 y fila de la matriz §6 línea 200) | Reescribir spec M1 con: container queries (no `min-width:1024px`), objetivo 50% ancho, sidebar drawer, matriz de viewports, estado ✅/🛠️ según resultado. Preservar el resto del documento. |

Tríada por stream (Implementador → Mejorador → Auditor). El Mejorador de 2A/2B endurece casos borde (rutas Windows, puertos ocupados, timeouts).

### GATE 3 — Auditoría de integración final (solo lectura)
Un auditor global `m1zf_auditor` ejecuta: `npm run build`, `pytest -q` completo, `git status`/`git diff --stat` verificando que **solo** se tocaron archivos de las fronteras declaradas, 0 residuos (`*.tmp`, lockfiles, `node_modules` nuevos), y revisa screenshots de 2B contra AC-1…AC-9. Emite `PASS::` o `REJECT:: <archivo:línea>`.

## 5. Protocolo BLOCKER
- **Tier A** (p. ej. un stream necesita una clase CSS de otra frontera): el Orquestador reasigna ownership sin solapamiento.
- **Tier B** (p. ej. cambiar comportamiento de Enter/estado, agregar dependencia npm como `@tailwindcss/container-queries` o Playwright en `package.json`): escalar al usuario.

## 6. Riesgos y mitigaciones
| Riesgo | Mitigación |
|--------|-----------|
| Opciones con fórmulas anchas rompen la columna a 683 px | `minmax(0,1fr)` + overflow-x contenido en `.katex`; fallback automático a 1 col si `< 600px`. |
| Orden de lectura en 2 col (columna-primero) confunde con atajos A–G | Letras de badge se mantienen; orden visual 4+3 es el acordado en el spec. |
| `@container` no soportado en navegadores viejos | Soporte Chrome/Edge 105+, Safari 16+, FF 110+; fallback natural = 1 columna. |
| Edición concurrente de `index.css` | Único dueño: 1A. |

## 7. Definición de Hecho
Todos los AC-1…AC-11 verificados por el Auditor de Gate 3, `GATE_STATUS.md` en PASS, y fila de Milestone 1 marcada ✅ en `FUTURE_MILESTONES.md`.
