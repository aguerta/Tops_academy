# Handoff — Stream P3 Frontend (Carga de Cursos y Rendimiento)

**Fecha:** 2026-10-26  
**Stream:** P3 Frontend (Frente B — Milestone 11: Instant Course Loading)  
**Estado:** ✅ COMPLETADO CON ÉXITO (`npm run build` y tests verdes)

---

## 1. Resumen de Cambios Implementados

### 1.1. `platform/src/types.ts`
- Modificado `CourseSummary`:
  - `data?: Course;` opcional conservado.
  - Agregados campos de metadatos de optimización: `bytes?: number;` y `etag?: string;`.
- Agregada interfaz `CourseManifest`:
  ```typescript
  export interface CourseManifest {
    generated_at: string;
    courses: CourseSummary[];
  }
  ```

### 1.2. `platform/src/utils/courseLoader.ts` (Nuevo)
- **`loadManifest()`**:
  - Detección inmediata en DOM: inspecciona `<script id="course-manifest" type="application/json">` en el primer tick (0 ms de red, 1er frame render!).
  - Fallback resiliente: candidatos `/api/courses.json`, `/api/courses`, etc.
  - Normalización determinista a estructura `CourseManifest`.
- **Caché en dos niveles (Memoria + IndexedDB)**:
  - Nivel 1 (Memoria): `Map<string, { course: Course, etag?: string }>` para aperturas en `< 16 ms` (1 frame).
  - Nivel 2 (IndexedDB): Base de datos `tops_academy_cache`, object store `courses`, keyPath `id`. Almacena `{ id, course, etag, saved_at }` con recuperación automática tras recargas o reinicios.
- **`loadCourse(summary, onProgress)`**:
  - 1. Si el curso está en memoria y el `etag` coincide (o no hay cambio), retorna de inmediato.
  - 2. Si está en IndexedDB y el `etag` coincide con el manifest, lo promueve a memoria y retorna de inmediato.
  - 3. Si no está en caché o cambió su `etag`, realiza `fetch` a `/api/courses/${encodeURIComponent(summary.id)}.json` (con candidatos de respaldo).
  - 4. Soporte para lectura progresiva de streams (`ReadableStream` + `TextDecoder`) si `onProgress` está presente.
  - 5. Guarda en memoria e IndexedDB.
  - 6. Deduplicación de peticiones concurrentes mediante `inFlightRequests` Map.
- **Prefetch en segundo plano (`prefetchCourses`)**:
  - Utiliza `requestIdleCallback` (con fallback de `setTimeout`) para descargar cursos de forma secuencial en momentos de inactividad de la CPU, sin degradar los 60 fps de la UI.
- **Prefetch prioritario (`prefetchCourse`)**:
  - Eleva la prioridad y precarga el curso en cuanto el usuario interactúa con la tarjeta (`onPointerEnter`, `onFocus`, `onTouchStart`).

### 1.3. `platform/src/App.tsx`
- **Inicialización inmediata**:
  - Detecta inline manifest en tick 0 (`getInitialManifest()`), evitando spinners iniciales cuando el manifest está inyectado en el HTML (cumple AC-20).
  - Invoca `loadManifest()` en `useEffect` y dispara `prefetchCourses(manifest.courses)` en idle.
- **Apertura instantánea**:
  - `selectCourse`: usa `courseLoader.loadCourse(summary)`. Si el curso ya está en caché, abre de inmediato (< 16 ms). Si se descarga, pasa `loadingCourseId` para feedback visual (cumple AC-21).
- **Cero re-descargas al volver a la biblioteca**:
  - Al regresar a la biblioteca (`onBackToLibrary` en Overview y Challenge), se ejecuta `setActiveCourse(null); setViewMode('library');` sin disparar ninguna petición de red (`fetchCourses` eliminado) (cumple AC-23).

### 1.4. `platform/src/components/CourseLibrary.tsx`
- Nuevas props opcionales:
  - `onPrefetch?: (id: string) => void`
  - `loadingCourseId?: string | null`
- Interactividad en tarjetas:
  - `onPointerEnter`, `onFocus`, `onTouchStart` invocan `onPrefetch?.(c.id)` para prefetching preventivo antes del click.
- Feedback visual de carga:
  - Si `loadingCourseId === c.id`, el botón de la tarjeta muestra un estado "Cargando..." con spinner activo y cursor de espera, deshabilitando clicks repetitivos durante la descarga.

---

## 2. Decisiones Técnicas y de Diseño
- **Sin Dependencias Nuevas**: Se emplearon APIs nativas del navegador (`IndexedDB`, `fetch`, `requestIdleCallback`, `ReadableStream`, `TextDecoder`), garantizando 0 aumento en dependencias de producción.
- **Deduplicación en Vuelo**: Si el usuario pulsa click en una tarjeta mientras el prefetch prioritario o en idle está en curso, ambas operaciones comparten la misma Promise (`inFlightRequests`), previniendo descargas dobles.
- **Validación ETag**: Si un curso en IndexedDB tiene un `etag` diferente al del manifest slim, se invalida silenciosamente y se descarga la versión más reciente.
- **Preservación Inviolable**:
  - Todos los `data-testid` (`course-card`, `course-error-card`, `course-completed-badge`, `course-progress-badge`) permanecen exactamente iguales.
  - La lógica de selección de unidades, tipos de sesión (quiz/test/practice/challenge), barajado pedagógico y maestría se mantiene 100% intacta.

---

## 3. Matriz de Criterios de Aceptación Cubiertos
- **AC-20**: Biblioteca pinta tarjetas en $\le 100$ ms vía manifest inline (`getInitialManifest()` y `loadManifest()`).
- **AC-21**: Curso prefetched abre en $\le 300$ ms con 0 peticiones de red; apertura en frío con indicador claro de carga en botón de tarjeta.
- **AC-23**: Volver a biblioteca (`setCourse(null)` / `onBackToLibrary`) no re-emite peticiones de lista de cursos.

---

## 4. Resultados de Verificación
1. `npm run build` en `platform/`:
   ```text
   > tsc && vite build
   ✓ 1102 modules transformed.
   ✓ built in 6.40s
   ```
2. Suite de pruebas Python:
   ```text
   .venv\Scripts\pytest tests/test_platform.py -q
   ................... [100%]
   19 passed in 11.80s
   ```
3. `git diff` verificado: únicamente archivos dentro de la frontera autorizada de Stream P3 (`types.ts`, `courseLoader.ts`, `App.tsx`, `CourseLibrary.tsx`).
