# Registro de Milestones Completados y Certificados: Tops Academy

> **Propósito:** archivo de los milestones **cerrados**. Lo pendiente o en curso vive en [`FUTURE_MILESTONES.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/FUTURE_MILESTONES.md) *(espejo de este archivo en `docs/future_milestones/MILESTONES_COMPLETED.md`)*.  
> **Convención de certificación:** cada entrada dice *quién* certificó y *cómo*. «Certificado por el usuario» = prueba manual en sus equipos. «Verificado automáticamente» = tests o E2E con nombre y resultado. Lo no verificado se declara de forma explícita.  
> **Última actualización:** 2026-11-08 (Branch: `main` / `optimizaciones_test` — Pipeline C2C v4.0 "Más con Menos", DSL Form-C, Shift-Left 4 Arquetipos, FSM Hook Guard y M1, 2, 2a, 3, 10, 11 cerrados).

---

## Índice

| Milestone | Alcance cerrado | Certificación | Commits |
| :--- | :--- | :--- | :--- |
| **1** Ergonomía Web (Zoom-Fix, Split 50%, Remediación v3) | Laptops 14" a 150%, TUF F15 a 125%, split 50%, tablets; biblioteca de 3 columnas; prosa en fórmulas | Usuario (2026-10-26) + matriz de 7 viewports + 97 contratos | `05c8f4b`, `12042d0`, `950bd20` |
| **2a** Usabilidad móvil | Teléfono: columna única, drawer, footer en flujo | Usuario (2026-10-26) + viewport 390 × 844 en la matriz | los de M1 |
| **2** PWA Instalable y Modo Offline | Service Worker Workbox, precaching App Shell + fuentes KaTeX, Web App Manifest, suite de iconos (192, 512, maskable), badge `✓ Offline`, navegación nativa popstate (`navigationHistory.ts`), instalación guiada | Automática (`tests/test_pwa_offline.py`, `tests/test_pwa_navigation_and_install.py`) + Verificado en producción PWA (2026-11-01) | `23cb4ec`, `e26769b`, `7e6a238`, `9296f9c` |
| **3** Anti-Overfitting y Variedad de Plantillas (v3.8 Tri-Banda) | Contrato Tri-Banda (`--min-archetypes 3`, 3 bandas ZPD, $\ge 2$ Bloom, cuota FIB/MS, `[STEM-DIVERSITY-GATE]`) + `ArchetypeEntropyLinter` (`MIN_ARCHETYPES = 3` + `ratio > 0.85` + MPRI) | Automática (`test_new_audit_linters.py`, 11 cursos publicados con 0 infracciones) | `5b5395c`, `be43b08`, `b07cec8` + cierre 2026-10-31 |
| **4** DSL Form-C y Desacoplamiento KaTeX (Fase Base / 85%) | DSL Form-C en 55–70 líneas (4 arquetipos disjuntos, catálogo RATS único con `@var@`, `_pv` canónico sin regex), desacoplamiento KaTeX-Python con PrairieLearn `@var@` en raw strings, integración de `pykatex>=0.0.8` y `z3-solver>=4.13.0` | Automática (`tests/test_c2c_v321_comp4_prompts.py`, `tests/test_sweetspot_v35_cta_and_shards.py`) + migración de plantillas EDO/EDP | `315690c`, `cee3e5d`, `884c305`, `cb84a16` |
| **7** Pipeline "Más con Menos" (Target `< 12 min` y `-65%` Tokens) | Deduplicación masiva `-2.0M` tokens en `dispatch.py` (eliminación de triple envío Prompt/work_order/items), recibos criptográficos SHA-256 (`shard_XX.cert.json`) en compilador `< 5 ms`, subagentes `--lean` por defecto con prompts $\le 5\text{ KB}$, weighted waves de hasta 100 shards concurrentes, precheck estático AST `< 50 ms` (`shard_precheck.py`), y suite global de 1,404 tests en 27.76s | Automática (1,404 tests pasando al 100% en 27.76s en `pytest tests/ -q`) + 3 auditorías forenses | `e357df5`, `cb84a16`, `6208088`, `75bfde1`, `c81aaa6` |
| **10** QA Rubric v2.0 Deep Mastery | 7 linters Path-to-Mastery v2.0, MPRI (/100 pts en 6 pilares, cuota $\ge 25\%$ multimodal), penalizaciones duras, compuerta bloqueante pre-publish `PublishQualityGateError` con mapeo AST | Automática (`tests/test_new_audit_linters.py`) + Auditoría en pipeline sobre 11 cursos | `be43b08`, `24c44f8`, `0e2fd38`, `b07cec8` |
| **11** Carga de cursos — núcleo | Manifest slim, índice con caché, ETag/304/gzip, manifest inline, IndexedDB, prefetch | Automática (12 tests de API + build); ACs de cliente sin medir | `41435c5`, `b73a5ee`, `2051b8b`, `97fa2f3` |
| **15** Gobernanza Formal y FSM Multi-Agente (Fase 1 Isomórfica) | Matriz 2D `decidirEstrategiaEdicion` en `c2c_hook_guard.py` (bloqueo estricto de reescrituras globales si errores $< 6$, imposición de edición quirúrgica y modular splicing), tope duro síncrono (40 turnos / 5M tokens por subagente), y aislamiento AST en subprocesos | Automática (`tests/test_hook_post_pass_and_write_isolation.py`, `tests/test_watchdog_and_hooks.py`) | `e357df5`, `75bfde1`, `c81aaa6` |
| **16** Certificación Matemática Shift-Left y 4 Arquetipos (Fase 1 Motor) | Stage Contract v4.0 (`engine/stage_contract.py`, `engine/invariants.py`), 4 arquetipos obligatorios en `compile_shard.py` (`direct`, `inverse`, `perturbation`, `boundary_or_edge_case`), supuestos explícitos obligatorios en `cta.json` (`assumptions` + `violation_consequence`), fix silencioso de `np.bool_` en sandbox AST, linters anti-gaming (`[DIAG-MAGIC-MULT]`) | Automática (`tests/test_validator.py`, `tests/test_m3_archetypes_semantic_gate.py`, `tests/test_c2c_author_speedups.py`) | `954a6c8`, `cee3e5d`, `9310ff7`, `75bfde1` |

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
* **Evolución:** La infraestructura PWA e instalación móvil complementaria se completó formalmente en el **Milestone 2** (ver abajo).

---

## Milestone 2: PWA Instalable y Modo Offline (Configuración PWA Móvil y Navegación Nativa)
* **Estado:** ✅ **Completado y Verificado (2026-11-01).**
* **Objetivo:** Experiencia nativa instalable (`standalone`) en smartphones Android, iOS y escritorio sin red, con sincronización de historial del navegador para gestos de retroceso nativos.
* **Componentes Técnicos Entregados:**
  1. **Service Worker y Precaching con Workbox (`vite-plugin-pwa`):**
     - Precaching de App Shell (HTML, JS, CSS y fuentes `.woff2` de KaTeX ≈ 1.5 MB total).
     - **Exclusión obligatoria en Workbox:** Exclusión de `api/courses/*.json` y `courses/*.json` de los `globPatterns` de precache (evitando desbordar el límite de 2 MB ante cursos de 14 MB como Gavilano); delegación a IndexedDB (`tops_academy_cache` en `courseLoader.ts`) con estrategia `StaleWhileRevalidate` en tiempo de ejecución.
  2. **Web App Manifest e Iconos Adaptativos:**
     - `manifest.webmanifest` con `display: standalone`, `scope: ./`, `id: tops-academy-pwa`, `background_color: #ffffff`, `theme_color: #1a73e8`.
     - Suite completa de iconos: `pwa-192x192.png`, `pwa-512x512.png` y `pwa-maskable-512x512.png`.
     - Metatags de Safe Areas (`viewport-fit=cover`, soporte de `env(safe-area-inset-bottom)`).
     - Insignia visual `✓ Offline` por curso en `CourseLibrary.tsx`.
  3. **Gestión de Navegación Nativa y Popstate (`navigationHistory.ts`):**
     - Sincronización del estado de vistas de React con el `History API` del navegador (`popstate`).
     - Soporte para gesto de retroceso físico/gestual nativo en Android e iOS.
     - Interceptores LIFO para modales, sidebars y drawer.
     - Modal de confirmación antes de abandonar una sesión de práctica en curso y protección de doble atrás (`double-back exit toast`) en la raíz (biblioteca) para evitar salidas accidentales.
  4. **Instalación Guiada:**
     - Captura temprana del evento `beforeinstallprompt` y botón de instalación con spinner de carga interactivo en la barra superior.
* **Verificación Automatizada:**
  - `tests/test_pwa_offline.py` (12/12 PASS).
  - `tests/test_pwa_navigation_and_install.py` (PASS).
* **Commits:** `23cb4ec`, `e26769b`, `7e6a238`, `9296f9c`.

---

## Milestone 3: Anti-Overfitting y Variedad de Plantillas por Competencia (Arquitectura v3.8 Tri-Banda Multimodal)
* **Estado:** ✅ **Completado al 100% en Pipeline y Auditoría QA (2026-10-31).** Verificado automáticamente mediante pruebas unitarias (`tests/test_new_audit_linters.py`), tests de compilación de shards y escaneo estático sobre los 11 cursos publicados en `courses/*.json` (0 infracciones).
* **Objetivo Crítico:** Erradicar el sobreajuste sintáctico (*overfitting* a un único molde donde solo rotan números) exigiendo polimorfismo estructural real, progresión adaptativa ZPD y modalidades de evocación activa en cada competencia.
* **Componentes Técnicos Entregados:**
  1. **Compuerta de Compilación `[M3-ARCHETYPES]` — Contrato Form-B Tri-Banda Multimodal ([`compile_shard.py:L1901-L2274`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/compile_shard.py#L1901-L2274)):**
     - **Mínimo 3 arquetipos ortogonales por competencia (`--min-archetypes 3`):** Cubriendo obligatoriamente las 3 bandas ZPD (`easy` = Directo, `medium` = Inverso, `hard` = Perturbación).
     - **Diversidad cognitiva de Bloom:** Mínimo $\ge 2$ niveles distintos de la taxonomía de Bloom por competencia.
     - **Cuota de práctica activa multimodal (`FIB` / `MS`):** Mínimo $\ge 2$ plantillas activas (`fill_in_the_blank` o `multiple_select`) en habilidades (`Hab-*`) y $\ge 1$ en conceptos/hechos (`C-*`/`H-*`).
     - **Anti-clonación AST y matemática:** Verifica que toda función generadora que declare `arch` ramifique realmente en su cuerpo AST (`_fn_uses_arch_in_body`), que los enunciados `stem_es` y funciones generadoras no sean clones, y que las tuplas produzcan salidas matemáticas distintas al evaluarse con `seed=100` y `seed=101`.
     - **Bloqueo de multiplicadores mágicos (`[DIAG-MAGIC-MULT]`) y Compuerta de Diversidad de Enunciados (`[STEM-DIVERSITY-GATE]`):** Exige $\ge 15$ stems enmascarados únicos en habilidades (cuota 30) y $\ge 10$ en conceptos/hechos (cuota 20).
  2. **Auditoría Determinista Integral en QA Engine ([`standardized_audit_engine.py:L674-L767`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/course-qa-evaluator/scripts/standardized_audit_engine.py#L674-L767)):**
     - `ArchetypeEntropyLinter` (`MIN_ARCHETYPES = 3`): Audita tanto concentración excesiva en una sola plantilla (`ratio > 0.85`) como insuficiencia de esqueletos estructurales (`distinct_skeletons < 3`) o de plantillas declaradas (`len(tpl_ids) < 3`) en competencias con $\ge 15$ reactivos, exponiendo `low_archetype_variety_competencies` y `min_distinct_skeletons_observed`.
     - Integración directa con el **Pilar 2 del MPRI** (`retrieval_modality_and_anti_gaming`, penalizando competencias monótonas en `anti_gaming_score`) y mapeo prescriptivo en [`course_publisher.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/course_publisher.py#L306-L314) (`ZPD-TRI-BAND / archetype_entropy_linter`), complementado por `ZPDProgressionCalibrationLinter` y `AntiGamingPsychometricLinter` (`answer_memorization_exploit`).

---

## Milestone 10: Rúbrica QA v2.0 (Certificación Deep Mastery & Path-to-Mastery)
* **Estado:** ✅ **Completado al 100% y Activo en Producción (2026-10-31).** Verificado automáticamente con la suite `tests/test_new_audit_linters.py` y validación sobre los 11 cursos publicados en `courses/*.json` (1,170 reactivos certificados sin bloqueos ni regresiones).
* **Objetivo:** Certificación integral del rigor pedagógico, psicométrico y técnico bajo estándares de Quality Matters (QM), OSCQR y Mastery Learning con compuertas de bloqueo deterministas.
* **Componentes Técnicos Entregados (`standardized_audit_engine.py`, `qa_rubric.md` y `course_publisher.py`):**
  1. **Suite de 7 Linters Path-to-Mastery v2.0:**
     - `ZPDProgressionCalibrationLinter`: 3 bandas ZPD con progresión obligatoria y presencia de niveles Bloom `Apply+`.
     - `RetrievalModalityDiversityLinter`: Cuota activa (`FIB + MS`) frente al monocultivo pasivo de reconocimiento (MC7).
     - `SocraticScaffoldingIntegrityLinter`: Detección estricta de pistas envenenadas, boilerplate Mad-Libs y fugas directas de la respuesta correcta.
     - `DiagnosticRationaleAlignmentLinter`: Bloqueo de multiplicadores numéricos arbitrarios (`[DIAG-MAGIC-MULT]`) y reciclaje de rationales genéricos.
     - `AntiGamingPsychometricLinter`: Prevención de memorización visual ($\le 4$ claves), relleno de opciones `[R-15]`, prefijos cruzados y cuantificadores universales vacuos.
     - `DAGMasteryTopologyLinter`: Detección de ciclos, inversiones topológicas y subgrafos curriculares desconectados.
     - `KaTeXFrontendErgonomicsLinter`: Detección de bloques de prosa dentro de `\text{}` que excedan 45 caracteres e identificadores matemáticos crudos sin formateo KaTeX.
  2. **Índice MPRI (`Mastery Path Readiness Index`, 0 a 100 pts en 6 pilares):**
     - Exigencia de $\ge 25\%$ de generación activa / discriminación (`FIB + MS`) para otorgar puntaje completo de modalidad (penalizando hasta -10 pts MPRI y -1.3 pts en Dimensión 2 ante monocultivo 100% MC7).
  3. **Penalizaciones Duras Deterministas (`hard_penalties`):**
     - `socratic_hint_poisoning` (-1.5 pts), `vacuous_quantifier_key_corruption` (-1.0 pt), `answer_memorization_exploit` (-0.5 pt/comp, máx -2.0 pts), sumadas a `bank_lt_3_exercises`, `hints_zero` y `orphan_questions`.
  4. **Compuerta Bloqueante Pre-Publish (`PublishQualityGateError` en `course_publisher.py`):**
     - Bloqueo determinista de publicación si `MPRI < 75.0`, `zpd_score <= 0.0`, `diag_pillar_score < 13.0`, `rationale_uniqueness_pct < 30.0%`, `len(hard_penalties) > 0`, cualquier issue `critical`, o presencia de opciones con padding de longitud artificial (`length_padded_options`).
     - Generación automática de `specific_error_report.{md,json}` con mapeo AST de números de línea exactos para remediación quirúrgica por subagentes.
* **Verificación Automatizada:**
  - Suite `tests/test_new_audit_linters.py` (100% PASS).
  - Validación sobre los 11 cursos reales publicados en `courses/*.json` (1,170 reactivos certificados sin bloqueos ni regresiones).
* **Commits:** `be43b08`, `24c44f8`, `0e2fd38`, `b07cec8`.

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

## Milestone 4: DSL Form-C y Desacoplamiento KaTeX (Fase Base / 85%)
* **Estado:** ✅ **Fase Base (85%) completada y verificada automáticamente (2026-11-08)**. La fase de gramática estricta `KaTeXAST` permanece en roadmap secundario; el desacoplamiento con PrairieLearn `@var@` en raw strings, el validador `pykatex` y el motor formal `z3-solver` operan al 100% en producción.
* **Objetivo:** Erradicar definitivamente la colisión de caracteres de control LaTeX (`\t`, `\b`), desacoplar la renderización KaTeX del runtime de Python, y condensar el código de los autores a plantillas de 55–70 líneas (`-65%` de tokens de salida).
* **Entregado y Verificado:**
  - **Desacoplamiento KaTeX con `@var@`:** Soporte de tokens ortogonales `@var@` y `@var:fmt@` en `engine/assemble.py`, `engine/invariants.py` y `check_templates.py`, garantizando raw strings libres de escaping parasitario.
  - **DSL Composicional `Form-C`:** Reducción a 4 tuplas canónicas en `TEMPLATES` estructuradas en 55–70 líneas por competencia; catálogo unificado `RATS` que interpola variables dinámicas y función canonical `_pv(c)` resiliente a desigualdades (`\le`, `\ge`, `<=`, `>=`).
  - **Tooling Formal:** Inclusión de `pykatex>=0.0.8` y `z3-solver>=4.13.0` en `pyproject.toml` para validación estática de spans matemáticos y consistencia formal.
  - **Migración de Referencia:** Cursos base `examples/edo/` y `examples/edp/` reescritos al estándar Form-C v2.0.
* **Pruebas:** `tests/test_c2c_v321_comp4_prompts.py`, `tests/test_sweetspot_v35_cta_and_shards.py`, `tests/test_pykatex_warn.py`.
* **Commits:** `315690c`, `cee3e5d`, `884c305`, `cb84a16`.

---

## Milestone 7: Pipeline "Más con Menos" — Deduplicación, Recibos SHA-256, Prompts `--lean` y Suite `< 30 s`
* **Estado:** ✅ **Completado y verificado automáticamente (2026-11-08)**. Se alcanzaron todas las metas de eficiencia en tokens, reducción de latencia de compilación y aceleración de CI.
* **Objetivo:** Lograr máxima calidad formal (4 arquetipos + supuestos) con el menor consumo de tokens (`-65%`) y latencia reducida (`< 12 min` en corridas completas), erradicando envíos parasitarios y cómputos redundantes.
* **Entregado y Verificado:**
  - **Deduplicación Masiva en `dispatch.py` (`-2.0M` tokens):** Se eliminó el triple envío redundante de `"Prompt"`, `"work_order"` e `"items"` en la inicialización de subagentes.
  - **Recibos Criptográficos SHA-256 (`< 5 ms`):** `run.py` y compiladores emiten y validan `shard_XX.cert.json` para evitar re-compilaciones de shards inalterados.
  - **Prompts `--lean` Ultra-Compactos:** Todos los subagentes operan con system prompts optimizados $\le 5\text{ KB}$ en `system_prompts/lean/`.
  - **Weighted Waves (1 Hab/shard, olas $\le 100$):** `dispatch.py` y `plan_shards.py` soportan hasta 100 shards concurrentes en una única ola de despacho paralelo.
  - **Precheck Estático AST (`shard_precheck.py`):** Detección en $< 50\text{ ms}$ de infracciones de perturbación ad-hoc (`while`), firmas de verificador (`ver_*`), bucles y strings de control antes de invocar subprocesos pesados.
  - **Suite de Pruebas Ultra-Rápida:** 1,404 pruebas ejecutadas en **27.76 segundos** con `pytest-xdist` dinámico (`worksteal`).
* **Pruebas:** 1,404 tests pasando al 100% (`pytest tests/ -q`), `tests/test_bootstrap_and_wave_streaming.py`, `tests/test_c2c_author_speedups.py`.
* **Commits:** `e357df5`, `cb84a16`, `6208088`, `75bfde1`, `c81aaa6`.

---

## Milestone 15: Gobernanza Formal y Certificación FSM del Pipeline C2C (Fase 1 Isomórfica)
* **Estado:** ✅ **Fase 1 Isomórfica en Python completada y verificada (2026-11-08)**. La compilación de `TopsAcademyC2C.lean` a binario C nativo mediante Lean 4 Perceus C (Fase 2) permanece en el roadmap de certificación formal industrial.
* **Objetivo:** Imponer guardrails deterministas inquebrantables que impidan bucles infinitos, ediciones parasitarias, alucinaciones de herramientas y reescrituras no modulares de código en subagentes autónomos.
* **Entregado y Verificado:**
  - **Matriz 2D `decidirEstrategiaEdicion`:** Integrada en `c2c_hook_guard.py` (Líneas infractoras $\times$ Tipo de error). Si los fallos son $< 6$, prohíbe reescrituras completas de archivos y fuerza edición quirúrgica o modular splicing.
  - **Tope Duro Síncrono:** Límite estricto de 40 turnos o 5,000,000 tokens por sesión de subagente para blindar el presupuesto.
  - **Aislamiento AST Anti-Bombas de Debug:** Intercepción en `sandbox.py` de scripts no autorizados, artefactos temporales en `scratch/` o llamadas con `python -c`.
  - **Flexibilización Quirúrgica para Autores:** Exención controlada en `c2c_hook_guard.py` permitiendo reescritura en los primeros 2 fallos de compilación antes de exigir modular splicing.
* **Pruebas:** `tests/test_hook_post_pass_and_write_isolation.py`, `tests/test_watchdog_and_hooks.py`, `tests/test_orchestration_resilience.py`.
* **Commits:** `e357df5`, `cb84a16`, `75bfde1`.

---

## Milestone 16: Certificación Matemática Shift-Left y 4 Arquetipos + Supuestos Explícitos (Fase 1)
* **Estado:** ✅ **Fase 1 (Motor y Contratos Python) completada y verificada (2026-11-08)**.
* **Objetivo:** Desplazar la detección de errores matemáticos y psicométricos hacia la etapa de diseño de plantillas (Stage 3), erradicando los Late-Catches en Stage 6 y garantizando variedad estructural profunda anti-overfitting.
* **Entregado y Verificado:**
  - **Stage Contract v4.0:** Tipado canónico e invariantes en `engine/stage_contract.py` e `invariants.py`.
  - **Estándar Inviolable de 4 Arquetipos:** `compile_shard.py` impone 4 arquetipos obligatorios (`direct`, `inverse`, `perturbation`, `boundary_or_edge_case`) con 4/4 fórmulas AST disjuntas y bandas ZPD (`easy`, `medium`, `hard`, `hard/expert`).
  - **Supuestos Explícitos en el Currículo:** `compile_cta.py` y `check_cta.py` exigen tuplas canónicas con supuestos formales (`assumptions`) y consecuencias de ruptura (`violation_consequence`) en `cta.json`.
  - **Fix Silencioso de `np.bool_`:** Resuelto el bug `cc_res is False` en `engine/sandbox.py`.
  - **Linters Psicométricos Anti-Gaming:** Bloqueo de multiplicadores mágicos (`[DIAG-MAGIC-MULT]`) y opciones de longitud heterogénea en `src/validator/psychometric_checker.py`.
* **Pruebas:** `tests/test_validator.py`, `tests/test_m3_archetypes_semantic_gate.py`, `tests/test_specific_error_report_and_stem_gate.py`, `tests/test_c2c_author_speedups.py`.
* **Commits:** `954a6c8`, `cee3e5d`, `9310ff7`, `75bfde1`.

---
*Registro de cierre. Para el estado vigente de lo pendiente, ver `FUTURE_MILESTONES.md`.*
