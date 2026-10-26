# BRIEFING — Stream 1D: Practice Shell

## 1. Contexto y Frontera
- **Stream**: 1D (Practice Shell Layout & Responsiveness)
- **Frontera EXCLUSIVA**: `platform/src/components/PracticeSession.tsx`
- **Carpeta de stream**: `.agents/teamwork/m1_zoomfix_split50/stream_1D/`
- **Reglas**:
  - No tocar handlers, atajos de teclado (`Enter`) ni lógica de estado.
  - Preservar todos los `data-testid` (`practice-session`, `restart-session-btn`, `skip-btn`, `next-question-btn`, `quick-redo-btn`, `check-btn`).
  - No agregar dependencias npm.
  - Usar inline style `minHeight: '100dvh'` con fallback de Tailwind `min-h-screen` (no depender de `.h-dvh-safe` de 1A).

## 2. Baseline Pre-Flight
- **TypeScript compilation**: `npx tsc --noEmit` en `platform/` ejecutado con éxito (Exit code: 0).
- **Git status**: Limpio en `platform/src/components/PracticeSession.tsx`.
- **Modo de verificación**: `npx tsc --noEmit` para evitar colisiones de `vite build` en `dist/` con otros streams paralelos.

## 3. Diagnóstico de `PracticeSession.tsx`
1. **Contenedor raíz**:
   - Actual: `className="min-h-screen bg-white flex flex-col justify-between"`. En móviles y split-screen con barra de navegación dinámica, `100vh` (`min-h-screen`) produce scroll fantasma.
   - Estado vacío: `className="min-h-screen bg-slate-50 flex flex-col items-center justify-center p-6 text-center"`.
   - Solución: Agregar `style={{ minHeight: '100dvh' }}` a ambos contenedores con `min-h-screen` como fallback.

2. **Header**:
   - Actual: `h-16 px-6`. En pantallas con altura reducida (`max-height: 850px` como laptops 768px/900px), 64px consume demasiado espacio vertical.
   - Solución: Reducir a `h-14 [@media(max-height:850px)]:h-12 px-4 sm:px-6 shrink-0` y truncar título largo para que no desborde en split view 50% (< 720px).

3. **Footer**:
   - Actual: `fixed bottom-0 left-0 right-0 h-20 bg-white border-t border-ka-border-card px-8 flex items-center justify-between z-20 shadow-sm`.
   - Problema: 80px (`h-20`) y `px-8` son excesivos en laptops 1366x768 / split view 683px / pantallas móviles.
   - Solución: `h-16 px-4 sm:px-8 shrink-0`.

4. **Padding inferior de `main`**:
   - Actual: `pb-28` (112px) pensado para un footer de 80px (`h-20`).
   - Solución: Ajustar a `pb-20` (80px), dejando 16px de margen confortable sobre el footer de 64px (`h-16`), recuperando 32px verticales para las opciones y enunciado.

5. **Progress Dots en < 520px**:
   - Actual: Renderiza todos los dots horizontalmente sin `flex-wrap` ni colapso. En viewports estrechos (< 520px o split-view 50% con muchas preguntas), los dots chocan con el contador y los botones Skip/Check provocando desborde horizontal.
   - Solución: Ocultar los dots en viewports menores a 520px (`hidden min-[520px]:flex [@media(min-width:520px)]:flex flex-wrap gap-1.5 sm:gap-2`), mostrando el contador legible (`n of N` o `Do N problems`).

## 4. Plan de Implementación
1. Modificar `platform/src/components/PracticeSession.tsx` aplicando las 5 correcciones.
2. Comprobar que todos los `data-testid` y comentarios sigan intactos.
3. Verificar con `npx tsc --noEmit` en `platform/`.
4. Documentar en `handoff.md` y enviar `DONE::` al orquestador.
