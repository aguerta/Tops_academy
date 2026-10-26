# Handoff — Stream 1E: Resto de vistas responsivas

- **Stream**: 1E
- **Fecha**: 2026-10-26
- **Archivos modificados (frontera 100% exclusiva)**:
  1. `platform/src/components/CourseLibrary.tsx`
  2. `platform/src/components/CourseOverview.tsx`
  3. `platform/src/components/MasteryGrid.tsx`
  4. `platform/src/components/MasteryLegend.tsx`
  5. `platform/src/components/PreExerciseModal.tsx`
  6. `platform/src/components/CompletionScreen.tsx`
  7. `platform/src/components/CourseChallenge.tsx`

---

## 1. Resumen de Cambios por Componente

### `CourseLibrary.tsx`
- **Grid responsivo 50% split-view**: Cambiado de `grid-cols-1 md:grid-cols-2 lg:grid-cols-3` a `grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4 sm:gap-6`. Con esto, a 683px (pantalla dividida al 50% en laptop de 1366px), se activan 2 columnas de manera óptima sin desborde.
- **Defensa anti-desborde en tarjetas**: Añadido `min-w-0` a las tarjetas y contenedores flex internos; `break-words` en títulos y errores; `truncate` en el botón principal con `shrink-0` en el checkmark.
- **Paddings elásticos**: `px-4 sm:px-6 py-6 sm:py-10` en contenedor principal y `p-4 sm:p-6` en tarjetas.

### `CourseOverview.tsx`
- **Contenedor raíz elástico**: `flex-1 min-w-0 w-full max-w-5xl mx-auto px-4 sm:px-6 py-6 sm:py-8`.
- **Breadcrumb defensivo**: `flex-wrap`, `min-w-0` y límite `max-w-[200px] sm:max-w-md` con `truncate` en el título del curso.
- **Títulos y textos**: `break-words` en h1 y descripción.
- **Tooltip de Mastery**: `w-72 sm:w-80 max-w-[calc(100vw-2rem)]` para prevenir overflow en 390px.
- **Tracker y Challenge Card**: `min-w-0` en bloques hijos flex; `flex-wrap` en cabeceras de unidades y badges; botones con `shrink-0`.

### `MasteryGrid.tsx`
- **Flex-1 anti-desborde**: `flex-1 min-w-0` en la información de la unidad (evita que fórmulas KaTeX o nombres extensos fuercen la tarjeta fuera del viewport).
- **Paddings elásticos y envoltura**: `p-4 sm:p-5`, `flex-wrap` en labels de unidades, `break-words` en nombres y descripciones.
- **Acciones y disparadores**: `shrink-0` en el contenedor de botones de práctica, quiz y unit test.

### `MasteryLegend.tsx`
- **Espaciado elástico**: `gap-x-4 sm:gap-x-6 gap-y-2 py-3 sm:py-4` para empaquetamiento limpio en 390px y 683px sin provocar scroll horizontal.

### `PreExerciseModal.tsx`
- **Soporte DVH**: `min-h-screen min-h-[100dvh]` y `overflow-x-hidden`.
- **Header responsivo**: `px-4 sm:px-6`, título con `truncate min-w-0 flex-1`, botones con `shrink-0`.
- **Hero azul adaptable**: Padding `p-6 sm:p-10`, `min-h-[340px] sm:min-h-[380px]`, `overflow-hidden` en contenedor de mascotas SVG.
- **Footer adaptable**: `h-16 sm:h-20 px-4 sm:px-8`, botón de inicio responsivo.

### `CompletionScreen.tsx`
- **Soporte DVH**: `min-h-screen min-h-[100dvh]` y `overflow-x-hidden`.
- **Header y Footer con límite de ancho de botón**: Botón de "Up next" / "Back to course" con `truncate max-w-[200px] sm:max-w-xs md:max-w-none` para evitar que títulos largos rompan el footer a 390px o 683px.
- **Hero card en columna/fila elástica**: `min-w-0` en ambos paneles, `break-words` en h1, paddings elásticos `p-6 sm:p-10`.

### `CourseChallenge.tsx`
- **Soporte DVH**: `min-h-screen min-h-[100dvh]` y `overflow-x-hidden`.
- **Header truncado**: `truncate text-center min-w-0 px-2 flex-1` en el título del challenge.
- **Hero y Footer**: Paddings elásticos `p-6 sm:p-10`, `h-16 sm:h-20 px-4 sm:px-8`.

---

## 2. Decisiones Técnicas
- **Breakpoints**: En Tailwind `sm:` es 640px y `md:` es 768px. En split view al 50% de 1366px (683px), `sm:` está activo pero `md:` no. Diseñar los grids con `sm:grid-cols-2` y `xl:grid-cols-3` garantiza 2 columnas en split view (683px, 720px, 800px) y 1 columna en móvil (390px).
- **Preservación total de contratos**: Todos los `data-testid` (`course-card`, `course-error-card`, `completion-tracker-summary`, `course-challenge-card`, `competency-block-*`, `competency-*`, `quiz-marker-*`, `unit-test-marker-*`, `start-practice-btn`, `completion-screen`, `start-challenge-btn`) intactos.
- **Atajos de teclado y estado**: No se modificó ningún hook `useEffect`, navegación por teclado (Enter) ni lógica de cálculo.
- **Cero dependencias nuevas**: Solo clases nativas Tailwind y utilidades estándar CSS.

---

## 3. Riesgos y Verificación
- **Riesgo**: Nombres de cursos o competencias extremadamente largos con fórmulas KaTeX.
  - **Mitigación**: `min-w-0` en todos los contenedores flex y `truncate` / `break-words` aplicados consistentemente.
- **Verificación**: `npx tsc --noEmit` en `platform/` pasa con código de salida 0 (limpio).

---

## 4. Mejoras del Improver

### Endurecimiento Técnico Aplicado:
1. **Fórmulas KaTeX Anchas en Títulos y Descripciones**:
   - En `CourseLibrary.tsx`, `CourseOverview.tsx`, `MasteryGrid.tsx`, `PreExerciseModal.tsx`, `CompletionScreen.tsx`, `CourseChallenge.tsx`:
   - Se inyectó contención CSS granular: `[&_.katex]:max-w-full [&_.katex]:overflow-x-auto [&_.katex]:overflow-y-hidden [&_span.inline-block]:max-w-full` y `[overflow-wrap:anywhere]`.
   - Garantiza que fórmulas matemáticas extensas (inline o display) no desborden horizontalmente las tarjetas ni provoquen `scrollWidth > innerWidth` en ningún ancho de la matriz (390px, 683px, 720px, 800px, 960px, 1366px, 1440px).

2. **Truncamiento Real en Elementos Inline (`<span>`)**:
   - Los elementos `<span>` por defecto son `display: inline`, ignorando `text-overflow: ellipsis` y `max-width`.
   - Se corrigieron los spans con `truncate` añadiendo `block min-w-0` o `inline-block align-bottom min-w-0` en:
     - Botón principal de tarjeta en `CourseLibrary.tsx`.
     - Breadcrumb del curso en `CourseOverview.tsx`.
     - Header bar y fila de Target Competency en `CompletionScreen.tsx`.

3. **Matriz de Alturas Críticas (768px, 844px, 900px, 1080px)**:
   - En `PreExerciseModal`, `CompletionScreen` y `CourseChallenge`:
   - Headers y footers blindados con `shrink-0` para prevenir colapso vertical en laptops con viewport de 768px de alto.
   - Ajuste elástico de alturas mínimas en paneles Hero (`min-h-[320px] sm:min-h-[380px]` y `min-h-[340px] sm:min-h-[400px]`) evitando scrolls verticales forzados en pantallas de baja altura.

4. **Matriz de Anchos Extremos (390px móvil y 683px Split-View 50%)**:
   - En `MasteryLegend.tsx`: `min-w-0` en contenedor y `shrink-0` en los 7 chips de leyenda (Mastered, Proficient, Familiar, Attempted, Not started, Quiz, Unit test) para envolver ordenadamente en 2–3 filas sin provocar desborde horizontal.
   - En `CourseOverview.tsx`: tooltip de mastery reforzado con `break-words [overflow-wrap:anywhere]` y card de Course Challenge con `min-w-0` e icono `shrink-0`.
   - En `CourseLibrary.tsx`: contenedor raíz blindado con `overflow-x-hidden`.

5. **Accesibilidad y Buenas Prácticas**:
   - Atributo explícito `type="button"` asignado a todos los elementos `<button>` (incluyendo triggers de `MasteryGrid`, botones de retorno `←`, tooltips `ⓘ` y botones de acción en pie de página).
   - Atributos `aria-label` añadidos en botones iconográficos para lectores de pantalla.

6. **Verificación y Contratos**:
   - `npx tsc --noEmit` en `platform/` ejecuta limpio (exit code 0).
   - Los 19 `data-testid` declarados se encuentran 100% preservados e intactos.
   - Frontera exclusiva de Stream 1E estrictamente respetada (0 modificaciones fuera de los 7 archivos).

DONE::
