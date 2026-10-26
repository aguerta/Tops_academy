# Pre-Flight Briefing — Stream 2D (Tests Frente B: Carga de Cursos y Rendimiento)

**Fecha:** 2026-10-26  
**Stream:** 2D (Tests automatizados Frente B)  
**Frontera exclusiva de escritura:**
- `tests/test_course_api_manifest.py` (nuevo)
- `.agents/teamwork/m1_zoomfix_split50/stream_2D/BRIEFING.md`
- `.agents/teamwork/m1_zoomfix_split50/stream_2D/handoff.md`

---

## 1. Baseline de Verificación del Entorno

1. **Build baseline (`platform/`):**
   - Comando: `npm run build` (`tsc && vite build`)
   - Resultado: **EXITOSO** (código 0, transcurrido 6.31s).
   - Generación de artefactos de producción y assets KaTeX verificados.

2. **Pytest baseline:**
   - Comando: `.\pytest.cmd -q tests/test_platform.py`
   - Resultado: **19 passed** en 11.55s.

3. **Node.js:**
   - Versión: v24.14.0

---

## 2. Inspección de Archivos y Contratos Reales

### A. `platform/server/courseIndex.cjs`
- Implementa `buildIndex(options)` con soporte para caché persistente en disco (`platform/.cache/course_index.json`) e invalidación basada en `mtimeMs` y `size`.
- `getManifest()` entrega `{ generated_at, courses }`.
- Cada elemento en `courses` posee: `id`, `filename`, `title`, `description`, `status`, `total_competencies`, `total_questions`, `bytes`, `etag`, `error_message`.
- Se comprueba que **ningún** elemento incluye la clave `data` (manifest slim).
- `getCourseData(id)` retorna `{ data, etag, status, error_message }`.
- `getCourseRaw(id)` retorna `{ raw, etag, status, error_message, filePath }` permitiendo streaming directo sin parseo repetido.
- `getSafeManifestHtmlScript()` escapa secuencias peligrosas como `</script>` y `<!--`.
- `getStats()` y `resetStats()` para monitoreo de conteo de parseos y hits de caché.
- Si un archivo JSON está corrupto, la función lo marca con `status: "error"` sin lanzar excepciones fatales.

### B. `platform/server/courseServer.cjs`
- Servidor HTTP Node.js que importa `courseIndex.cjs`.
- Rutas implementadas:
  - `GET /healthz` -> JSON con status, pid, uptime, conteo de cursos y estadísticas.
  - `GET /api/courses` y `GET /api/courses.json` -> Manifiesto slim con cabecera `ETag`, soporte de compresión `gzip` y respuesta `304 Not Modified` ante `If-None-Match`.
  - `GET /api/courses/:id` -> Detalle de curso individual con streaming comprimido `gzip`, header `ETag` y respuesta `304 Not Modified` ante `If-None-Match`.
  - Fallback a `index.html` con inyección segura de manifest inline.

### C. `platform/index.html`
- Contiene el marcador `<!--COURSE_MANIFEST-->` listo para la inyección del script JSON.

### D. `platform/dist/api/courses.json`
- Se verificará en el test que, de existir tras build, sea un manifiesto slim (< 100 KB) sin incrustar `data`.

---

## 3. Plan de Pruebas Automatizadas en `tests/test_course_api_manifest.py`

Estructura modular con Pytest:
1. **TestCourseIndexContract (Direct Node/Python Bridge o ejecución de scripts node/subprocess):**
   - Ejecución de `courseIndex.cjs` mediante Node subprocess o harness JSON.
   - Validación de `getManifest()`: estructura, tamaño JSON (< 50 KB, target < 10 KB), ausencia estricta de propiedad `data`, existencia de campos requeridos (`id`, `filename`, `title`, `description`, `status`, `total_competencies`, `total_questions`, `bytes`, `etag`).
   - Validación de `getCourseData(id)` para curso válido: entrega objeto completo con `competencies` y `questions`.
   - Medición de performance de `buildIndex()` en caliente: < 100 ms.
   - Resiliencia ante JSON corrupto en directorio temporal: curso corrupto marcado con `status: "error"`, cursos válidos preservados intactos.

2. **TestCourseServerHttp (Live Ephemeral Node Server):**
   - Spawnea `node platform/server/courseServer.cjs` en un puerto libre efímero asignado dinámicamente (`PORT=0` o socket asignado).
   - Verifica `GET /api/courses` y `GET /api/courses.json`: devuelve manifest slim, sin propiedad `data` en ningún curso, cabecera `ETag` presente.
   - Verifica `GET /api/courses/:id`: devuelve curso individual con cabecera `ETag`.
   - Verifica que petición condicional con `If-None-Match` coincidente devuelve status `304 Not Modified` sin payload.
   - Verifica endpoint `/healthz` devolviendo status `200` y campos esperados.

3. **TestBuildAndTemplates:**
   - Verifica que `platform/index.html` contiene el marcador `<!--COURSE_MANIFEST-->` o la etiqueta `<script id="course-manifest" type="application/json">`.
   - Si `dist/api/courses.json` existe (o tras build), verifica que su tamaño sea < 100 KB y que no contenga `data` anidado en los elementos de cursos.

---
