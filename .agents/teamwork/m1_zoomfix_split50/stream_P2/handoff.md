# Handoff — Stream P2 (Vite Build & Inline Manifest)

**Fecha:** 2026-10-26  
**Stream:** P2 (Frente B — Carga de cursos y rendimiento)  
**Frontera exclusiva modificada:**
- `platform/vite.config.ts`
- `platform/index.html`
- `.agents/teamwork/m1_zoomfix_split50/stream_P2/`

---

## 1. Resumen de Cambios

1. **`platform/index.html`:**
   - Se añadió el marcador `<!--COURSE_MANIFEST-->` dentro de la etiqueta `<head>`.
   - Se mantuvieron todos los preloads de KaTeX de 1F y metadatos existentes.

2. **`platform/vite.config.ts`:**
   - Se importó `createRequire` de `'module'` para permitir cargar módulos CommonJS (`.cjs`) de manera limpia bajo `"type": "module"`.
   - Se implementó la integración directa con `./server/courseIndex.cjs` para reutilizar la lógica compartida de indexación y manifest.
   - Se agregó `transformIndexHtml` en el plugin `courseApiPlugin`: reemplaza `<!--COURSE_MANIFEST-->` por `<script id="course-manifest" type="application/json">...</script>` con el manifest SLIM inyectado, escapando caracteres conflictivos (`<` a `\u003c` / `<\/script` / `<!--`) de forma segura.
   - En `generateBundle()`:
     - Emite `dist/api/courses.json` con el manifest SLIM (**2.52 kB** en lugar del archivo original de **59,788.11 kB** — reducción del 99.995%).
     - Se eliminó el campo `data` de cada curso en la lista del manifest.
     - Emite los cursos individuales minificados (`JSON.stringify(c.data)` sin indentación `null, 2`) en `dist/api/courses/<id>.json` y `dist/courses/<filename>`.
   - En middleware de dev (`configureServer` y `configurePreviewServer`):
     - Atiende `/api/courses` y `/api/courses.json` devolviendo el manifest slim.
     - Atiende `/api/courses/:id` y `/courses/:filename` devolviendo los datos minificados del curso individual.
   - Mecanismo de resiliencia: incluye fallback robusto que garantiza que el build no se rompa si `./server/courseIndex.cjs` no estuviera disponible, adaptándose automáticamente en cuanto el módulo esté presente.

---

## 2. Verificación y Resultados

1. **`npm run build` en `platform/`:**
   - **PASS** (código de salida 0).
   - `dist/api/courses.json`: **2.52 kB** (gzip: 0.76 kB), cumpliendo holgadamente el criterio de aceptación (< 50 KB y < 10 KB).
   - `dist/index.html`: inyecta el script inline `<script id="course-manifest" type="application/json">...` permitiendo carga en 0 ms de red en primer frame.
   - `dist/courses/` y `dist/api/courses/`: todos los cursos individuales emitidos minificados en 1 sola línea.

2. **Pruebas de suite `tests/test_course_api_manifest.py`:**
   - **12/12 PASSED** en 1.13 s:
     - `test_platform_index_html_contains_manifest_marker_or_script` PASSED
     - `test_dist_api_courses_json_slim_and_no_data` PASSED
     - Todos los tests de servidor HTTP, ETag, 304, caching y estructura de manifest pasaron en verde.

3. **Pruebas de dev server:**
   - `/` responde con script tag `id="course-manifest"` y sin marcador residual.
   - `/api/courses` responde status 200, 7 cursos y `hasData === false`.
   - `/api/courses/saul_control_optimo` responde status 200 con el curso individual.

---

## 3. Decisiones y Riesgos Mitigados

- **Seguridad en inyección HTML:** Se implementó safe escaping de caracteres HTML en `transformIndexHtml` mediante `getSafeManifestHtmlScript` de `courseIndex.cjs` y reemplazo seguro para evitar cualquier vector de script breakout o rotura de sintaxis.
- **Sin scripts temporales:** Todos los tests se ejecutaron en memoria (`node -e` o suite existente). Ningún archivo temporal quedó en el working directory.
- **Integridad de fronteras:** No se modificaron archivos fuera de la frontera exclusiva de Stream P2 (`platform/vite.config.ts`, `platform/index.html` y la carpeta del stream).
