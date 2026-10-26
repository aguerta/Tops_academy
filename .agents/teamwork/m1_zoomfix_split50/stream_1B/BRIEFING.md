# BRIEFING — Stream 1B: Sidebar Drawer & App Shell

## 1. Identificación del Stream
- **Stream**: 1B — Sidebar drawer
- **Carpeta de stream**: `.agents/teamwork/m1_zoomfix_split50/stream_1B/`
- **Frontera EXCLUSIVA**:
  - `platform/src/components/Sidebar.tsx`
  - `platform/src/App.tsx`

## 2. Baseline de Verificación
- **Comando ejecutado**: `npx tsc --noEmit` en `platform/`
- **Resultado baseline**: Exit code 0 (sin errores de compilación ni tipos TypeScript).
- **Git status inicial**:
  - Rama: `optimizaciones_test`
  - Archivos modificados previos: `FUTURE_MILESTONES.md`
  - Archivos sin seguimiento: `.agents/teamwork/m1_zoomfix_split50/`
  - Archivos en frontera (`Sidebar.tsx`, `App.tsx`): 100% limpios/sin modificaciones previas.

## 3. Diagnóstico de Archivos en Frontera

### `platform/src/components/Sidebar.tsx`
- **Línea 27**: `className="w-64 flex-shrink-0 bg-white border-r border-ka-border-subtle min-h-screen py-6 flex flex-col"`
  - Ancho rígido `w-64` (256 px) incondicional.
  - En split-view a 50% de 1366 px (683 px), consume 256 px (37% del ancho total), estrangulando el contenido.
  - No existe lógica de apertura/cierre, ni botón hamburguesa, ni accesibilidad ARIA para drawer off-canvas.
- **Data-testids existentes**:
  - `data-testid="sidebar"` en `<aside>`. Debe ser estrictamente preservado.

### `platform/src/App.tsx`
- **Línea 284-309** (`viewMode === 'overview'`):
  - Contenedor `<div className="flex min-h-screen">`
  - `<main className="flex-1 overflow-y-auto">` carece de padding superior para botón de hamburguesa (`pt-14 lg:pt-0`).
- **Línea 353-377** (`viewMode === 'challenge'`):
  - Contenedor `<div className="flex min-h-screen">`
  - `<main className="flex-1 overflow-y-auto">` carece de padding superior para botón de hamburguesa (`pt-14 lg:pt-0`).
- Lógica de estado y handlers existentes deben mantenerse intactos (AC-10, AC-11).

## 4. Plan de Implementación Detallado

1. **`platform/src/components/Sidebar.tsx`**:
   - Agregar botón hamburguesa fijo en móvil / viewport < 1024 px:
     - `data-testid="sidebar-toggle"`
     - Posición: `fixed top-3 left-4 z-40 lg:hidden`
     - Accesibilidad: `aria-expanded={isOpen}`, `aria-controls="sidebar"`, `aria-label="Abrir/Cerrar menú lateral"`.
   - Backdrop / overlay:
     - Visible solo cuando `isOpen && < 1024px`: `lg:hidden fixed inset-0 bg-black/40 z-40`.
     - Click en backdrop cierra el drawer (`setIsOpen(false)`).
   - Atajo de teclado:
     - Listener global de `Escape` mientras `isOpen === true` para cerrar drawer y devolver foco al toggle.
   - Manejo de foco:
     - Foco al primer elemento enfocable o botón de cierre al abrir; regreso al toggle button al cerrar.
   - Cierre automático al seleccionar:
     - Al invocar `onSelectUnit`, `onSelectCourseChallenge` o `onBackToLibrary`, cerrar drawer en modo móvil.
   - Dimensiones responsivas del `<aside id="sidebar" data-testid="sidebar">`:
     - Clases: `fixed lg:static inset-y-0 left-0 z-50 w-64 max-w-[85vw] lg:w-56 xl:w-64 flex-shrink-0 bg-white border-r border-ka-border-subtle min-h-screen py-6 flex flex-col transition-transform duration-200 ease-in-out shadow-xl lg:shadow-none`.
     - Transformación: `isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'`.
     - En ≥ 1024 px (`lg:`): estático en el flujo, `w-56` (1024–1279 px) y `xl:w-64` (≥ 1280 px).

2. **`platform/src/App.tsx`**:
   - Ajustar `<main className="flex-1 overflow-y-auto">` en las vistas `overview` y `challenge` a `<main className="flex-1 overflow-y-auto pt-14 lg:pt-0">`.
   - Cero alteración a estado, atajos ni otras vistas.

3. **Verificación**:
   - `npx tsc --noEmit` en `platform/`
   - Validar que no queden residuos ni modificaciones fuera de frontera.
