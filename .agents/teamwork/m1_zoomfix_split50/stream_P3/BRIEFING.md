# Pre-Flight Briefing — Stream P3 Frontend (Carga de cursos y rendimiento)

**Fecha:** 2026-10-26
**Stream:** P3 Frontend (Frente B — Milestone 11: Carga instantánea de cursos)
**Responsable:** Stream P3 Implementer

---

## 1. Archivos en Frontera de Escritura
1. `platform/src/types.ts`
2. `platform/src/utils/courseLoader.ts` (Nuevo)
3. `platform/src/App.tsx`
4. `platform/src/components/CourseLibrary.tsx`

---

## 2. Baseline de Verificación
- **Build de Frontend (`platform/`):**
  - Comando: `npm run build`
  - Resultado: ✅ Exitoso (`tsc && vite build`), tiempo ~6.56s.
  - Observación: `dist/api/courses.json` tiene un tamaño de ~59.8 MB en el baseline actual porque embebe los objetos completos de todos los cursos.
- **Suite de Pruebas Python (`tests/test_platform.py`):**
  - Comando: `.venv\Scripts\pytest tests/test_platform.py -q`
  - Resultado: ✅ 19 passed en 11.31s.

---

## 3. Diagnóstico de Archivos Reales

### 3.1. `platform/src/types.ts`
- `CourseSummary` ya cuenta con `data?: Course;` opcional, pero le faltan los campos `bytes?: number;` y `etag?: string;`.
- No existe el tipo `CourseManifest { generated_at: string; courses: CourseSummary[]; }`.

### 3.2. `platform/src/utils/courseLoader.ts`
- Actualmente no existe. Se creará desde cero implementando:
  - `loadManifest()` con comprobación de script inline `#course-manifest` (0 ms de red en primer frame) y fallback con fetch a endpoints candidatos.
  - Caché de doble nivel: en memoria (`Map<string, { course: Course, etag?: string }>`) + `IndexedDB` (`tops_academy_cache`, store `courses`, clave `id`).
  - `loadCourse(summary, onProgress)`: retorno instantáneo de memoria (< 16 ms) o IndexedDB si coincide ETag, o fetch con candidatos de API y reporte de progreso.
  - Deduplicación de peticiones en vuelo (`inFlightRequests` Map).
  - `prefetchCourses(summaries)`: procesamiento en background con `requestIdleCallback` / `setTimeout` no bloqueante y serial.
  - `prefetchCourse(id)`: prefetch con prioridad alta ante interacción de usuario.

### 3.3. `platform/src/App.tsx`
- Actualmente `fetchCourses()` hace fetch de `/api/courses.json` completo y se vuelve a invocar en `onBackToLibrary` (L296 y L365), violando AC-23.
- `selectCourse` no usa caché IndexedDB ni reporta progreso de carga.
- Se refactorizará para inicializar con `loadManifest()`, disparar `prefetchCourses` en idle, cargar cursos con `loadCourse`, gestionar `loadingCourseId` / `loadingProgress`, y eliminar llamadas redundantes a `fetchCourses()` al volver a la biblioteca.

### 3.4. `platform/src/components/CourseLibrary.tsx`
- No recibe `onPrefetch` ni `loadingCourseId`.
- No tiene manejadores `onPointerEnter`, `onFocus`, `onTouchStart` en las tarjetas de cursos para prefetch prioritario.
- No muestra estado "Cargando..." ni spinner en el botón de la tarjeta cuando el curso está siendo descargado.

---

## 4. Plan de Acción Inmediato
1. Actualizar `platform/src/types.ts` agregando `bytes?: number; etag?: string;` a `CourseSummary` y declarando `CourseManifest`.
2. Crear `platform/src/utils/courseLoader.ts` con manejo robusto de IndexedDB, caché en memoria, deduplicación de peticiones y prefetching idle.
3. Actualizar `platform/src/components/CourseLibrary.tsx` con soporte para `onPrefetch`, `loadingCourseId`, eventos de interacción y feedback visual de carga.
4. Refactorizar `platform/src/App.tsx` integrando el loader y eliminando re-peticiones de red al volver a la biblioteca.
5. Ejecutar `npm run build` en `platform/` y la suite de pruebas para certificar cero regresiones.
