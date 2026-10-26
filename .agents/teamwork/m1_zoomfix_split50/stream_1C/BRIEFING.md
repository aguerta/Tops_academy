# Stream 1C Pre-Flight Briefing

- **Stream**: 1C (Toast & SVG)
- **Frontera EXCLUSIVA**:
  - `platform/src/components/FeedbackToast.tsx`
  - `platform/src/components/CoordinatePlane.tsx`
- **Criterios de Aceptación asignados**:
  - **AC-7**: `FeedbackToast` en `< 1024px` o `max-height: 850px`: bottom sheet responsivo con `max-height: 45dvh`, scroll propio, sin tapar botón Check/Next (el footer de `PracticeSession` mide ~h-16/h-20 fijo).
  - **AC-8**: `CoordinatePlane`: `viewBox` responsivo + `w-full max-w-[340px]` y `max-height: 30dvh` en pantallas bajas.

## Baseline de Verificación
- `npx tsc --noEmit` en `platform/`: **EXIT 0** (0 errores de tipado).
- `pytest -q`: 1034 passed, 2 pre-existing failures (`test_future_milestones_byte_parity` y `test_assemble_sanitize_katex_r23.py` previos), 1 skipped.

## Hallazgos de Archivos Reales

### 1. `FeedbackToast.tsx`
- Actualmente implementa dos estados:
  - Fallo (`!isCorrect`): contenedor `<div data-testid="feedback-toast" className="feedback-toast absolute right-8 bottom-24 z-30 ...">` con puntero decorativo rotado a 45°.
  - Acierto (`isCorrect`): contenedor `<div data-testid="good-work-toast" className="absolute right-8 bottom-24 z-30 w-84 ...">` con puntero decorativo rotado a 45°.
- En pantallas angostas (< 1024 px) o de baja altura (<= 850 px), el toast en `right-8 bottom-24` con ancho fijo de `w-80` / `w-96` desborda horizontalmente o tapa el área de contenido / footer.
- Solución AC-7:
  - Modo Bottom Sheet activado en `< 1024px` de ancho o `<= 850px` de alto (utilizando clases responsivas de Tailwind `fixed` o estilos responsivos con media queries / clases combinadas).
  - En bottom sheet: anclado encima del footer (`bottom-20` o `bottom-16 sm:bottom-20`), centrado con márgenes (`inset-x-3 sm:inset-x-6 max-w-xl mx-auto`), `max-h-[45dvh]`, con `overflow-y-auto` en el contenedor interno de contenido.
  - En desktop espacioso (ancho >= 1024px Y alto > 850px): mantiene el floating card flotante clásico en `right-8 bottom-24` con su flecha inferior.
  - Ocultar la flecha decorativa (`bottom-pointer`) en modo bottom-sheet para que no flote de forma antiestética en el aire.

### 2. `CoordinatePlane.tsx`
- Actualmente: `<svg data-testid="coordinate-plane" className="coordinate-plane block" width={width} height={height} viewBox={`0 0 ${width} ${height}`}>`.
- El contenedor exterior tiene: `inline-block my-4 p-2 bg-white rounded-lg border border-ka-border-card shadow-sm ${className}`.
- En split-view (683 px) o pantallas bajas (<= 850 px):
  - El SVG de 360 px excede el 50% de la columna si hay padding o container ajustado.
  - Solución AC-8:
    - Contenedor con `max-w-full flex justify-center`.
    - SVG responsivo: preservar `viewBox={`0 0 ${width} ${height}`}`, añadir clases `w-full max-w-[340px] max-h-[30dvh] h-auto block` y `style={{ maxHeight: '30dvh' }}`.
    - Asegurar preservación de todos los `data-testid` (`graph-container`, `coordinate-plane`) y elementos de renderizado de puntos/curvas.

## Plan de Ejecución
1. Actualizar `CoordinatePlane.tsx` con viewBox + clases responsivas `w-full max-w-[340px] max-h-[30dvh]`.
2. Actualizar `FeedbackToast.tsx` con layout adaptativo bottom-sheet / desktop toast, preservando todos los `data-testid` y atajos.
3. Verificar con `npx tsc --noEmit` en `platform/`.
4. Documentar en `handoff.md` y enviar señal `DONE::`.
