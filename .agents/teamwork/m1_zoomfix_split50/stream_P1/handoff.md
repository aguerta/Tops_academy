# Handoff — Stream P1 Server (Frente B)

**Fecha:** 2026-10-26  
**Stream:** P1 Server (Carga de cursos y rendimiento)  
**Estado:** COMPLETADO CON ÉXITO  

---

## 1. Archivos modificados y creados

| Archivo | Tipo de cambio | Propósito |
|---|---|---|
| `platform/server/courseIndex.cjs` | **Nuevo** | Módulo de indexación incremental con persistencia en caché en disco (`platform/.cache/course_index.json`), invalidación basada en `mtimeMs` y `size`, generación de manifest SLIM (< 50 KB) sin campo `data`, resolución rápida de cursos individuales con ETags, y escape seguro de HTML `<script>`. |
| `platform/server/courseServer.cjs` | **Refactorizado** | Integración de `courseIndex.cjs`, soporte de `/api/courses` slim con ETag y 304 Not Modified, endpoint `/api/courses/:id` con streaming y compresión gzip (`zlib.createGzip()`), inyección del manifest inline en `index.html`, compresión gzip en estáticos (`.js`, `.css`, `.json`), endpoint `/healthz`, y hardening ante `EADDRINUSE` y excepciones no capturadas. |

---

## 2. Contrato público exportado de `courseIndex.cjs`

Para consumo por `platform/server/courseServer.cjs`, `platform/vite.config.ts` (Stream P2), y tests automatizados (Stream 2D):

```javascript
const courseIndex = require('./courseIndex.cjs');

// Rutas
courseIndex.COURSES_DIR; // path.resolve(__dirname, '../../courses')
courseIndex.CACHE_FILE;  // path.resolve(__dirname, '../.cache/course_index.json')

// Métodos principales
courseIndex.buildIndex(options);
// options: { force?: boolean, coursesDir?: string, cacheFile?: string }
// Retorna: { version: 1, generated_at: string, entries: { [filename]: CourseEntry } }

courseIndex.getManifest();
// Retorna: {
//   generated_at: string,
//   courses: [
//     {
//       id: string,
//       filename: string,
//       title: string,
//       description: string,
//       status: 'valid' | 'error',
//       total_competencies: number,
//       total_questions: number,
//       bytes: number,
//       etag: string,
//       error_message: string | null
//     }
//   ]
// }
// NOTA: cursos garantizados SIN campo "data".

courseIndex.getManifestEtag();
// Retorna: string (ej: '"e26cab1cfe03b753"')

courseIndex.getCoursePath(id);
// id: course_id o filename (con o sin .json)
// Retorna: string (ruta absoluta) | null

courseIndex.getCourseData(id);
// Retorna: { data: object|null, etag: string, status: 'valid'|'error', error_message: string|null } | null

courseIndex.getCourseRaw(id);
// Retorna: { raw: string|null, etag: string, status: 'valid'|'error', error_message: string|null, filePath: string } | null

courseIndex.getSafeManifestHtmlScript(manifest?);
// Retorna: '<script id="course-manifest" type="application/json">...</script>'
// Con escape seguro de '</script>' a '<\/script>' y '<!--' a '\u003c!--'

// Telemetría y utilidades de testing
courseIndex.getStats();       // { parseCount: number, cachedHits: number, lastBuildDurationMs: number }
courseIndex.resetStats();     // Resetea los contadores
courseIndex.invalidateCache(); // Limpia caché en memoria y archivo .cache
```

---

## 3. Criterios de Aceptación Cumplidos

- **AC-19:** `/api/courses` responde manifest SLIM de **2.5 KB** (objetivo era < 50 KB, antes medía 59.7 MB!). Tiempo warm medido: **2 ms** (objetivo < 100 ms). **Cero** campo `data`.
- **AC-22:** `/api/courses/:id` no re-escanea ni re-parsea todos los cursos; resuelve por índice y transmite directamente con cabeceras `ETag`, `304 Not Modified`, `Cache-Control`, y compresión `gzip` vía `zlib.createGzip()`.
- **Inline Manifest en HTML:** `/` e `/index.html` inyectan el bloque `<script id="course-manifest" type="application/json">` automáticamente, con escape de caracteres peligrosos.
- **Compresión de estáticos:** Archivos `.js`, `.css`, `.json`, `.svg`, `.html` se sirven con compresión gzip si el cliente envía `Accept-Encoding: gzip`.
- **Resiliencia & Hardening:** `/healthz` implementado (reporta uptime, PID, estado del índice); captura de `EADDRINUSE` con mensaje diagnóstico claro; `keepAliveTimeout` configurado a 65 s.

---

## 4. Verificación y Resultados de Pruebas

1. **Test unitario y de endpoints HTTP (script Node con servidor efímero en puerto libre):**
   - Healthz: 200 OK con uptime y stats.
   - `/api/courses`: 200 OK en 2 ms, tamaño 2,517 bytes (< 3 KB), campo `data` inexistente.
   - Soporte 304 Not Modified en manifest verificado con ETag `e26cab1cfe03b753`.
   - Soporte gzip en manifest verificado (Content-Encoding: gzip, descompresión idéntica).
   - `/api/courses/:id`: 200 OK, streaming con ETag `3675f1-1a1754ed1c8`, 304 verificado, gzip verificado (de 3.5 MB a 235 KB).
   - `/` (HTML): contiene `<script id="course-manifest" type="application/json">`.
   - Curso inexistente: responde 404 Not Modified / Not Found.
   - 0 scripts temporales residuales.
2. **`npm run build` en `platform/`:** EXITOSO en 5.62s. `dist/api/courses.json` se redujo de 59,788 kB a **2.52 kB** (gzip: 0.76 kB).
3. **`pytest tests/test_platform.py`:** 19 passed in 12.35s.

---

## 5. Riesgos y mitigaciones

- **Concurrencia de streams:** Stream P2 (`vite.config.ts`) y Stream P3 (`App.tsx`/`courseLoader.ts`) consumen el mismo contrato aquí documentado. La API de `courseIndex.cjs` soporta fallbacks y métodos independientes.
