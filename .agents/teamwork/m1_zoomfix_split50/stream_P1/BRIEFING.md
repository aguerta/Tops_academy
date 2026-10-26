# Pre-Flight Briefing — Stream P1 Server (Frente B)

**Fecha:** 2026-10-26  
**Rol:** Implementador Stream P1 Server  
**Frontera de escritura autorizada:**
- `platform/server/courseIndex.cjs` (nuevo)
- `platform/server/courseServer.cjs` (refactor)
- `.agents/teamwork/m1_zoomfix_split50/stream_P1/BRIEFING.md`
- `.agents/teamwork/m1_zoomfix_split50/stream_P1/handoff.md`

---

## 1. Baseline del entorno

- **Node.js:** v24.14.0
- **npm run build en `platform/`:** EXITOSO (6.92s). Se observa que actualmente `dist/api/courses.json` genera 59,788.11 kB (~60 MB) sin comprimir.
- **pytest en `.venv`:** `.venv\Scripts\pytest -q tests/test_platform.py` -> 19 passed in 12.97s.
- **Git status:** Limpio (únicamente `.gitignore` con modificaciones locales no relacionadas).

---

## 2. Hallazgos en el código actual

1. **`courseServer.cjs`:**
   - Lee y valida todos los archivos `.json` de `courses/` en **cada** solicitud HTTP a `/api/courses`.
   - La respuesta de `/api/courses` incluye el campo `data` con el árbol JSON íntegro de cada curso (decenas de megabytes en memoria y en la red).
   - `/api/courses/:id` re-escanea y re-parsea todos los cursos antes de filtrar por `id`/`filename`.
   - No utiliza compresión (ni `gzip` ni `deflate`).
   - No maneja cabeceras de caché condicional (`ETag`, `If-None-Match`, 304 Not Modified).
   - Sirve archivos estáticos de `platform/dist` sin compresión y sin inyección de manifest inline en `index.html`.
   - Falta el endpoint de resiliencia `/healthz` y un manejo de errores robusto (`uncaughtException`, `EADDRINUSE`).

2. **Requisitos de `courseIndex.cjs`:**
   - Persistir caché en `platform/.cache/course_index.json`.
   - Invalidación inteligente basada en `mtimeMs` y `size`.
   - Validar y parsear solo archivos nuevos o modificados.
   - Generar manifest slim (< 50 KB, warm < 100 ms) **SIN** campo `data`.
   - Exportar contrato claro:
     - `buildIndex()`
     - `getManifest()`
     - `getCoursePath(id)`
     - `getCourseData(id)`
     - `getCourseRaw(id)`
     - `getSafeManifestHtmlScript()`
     - Contadores para telemetría/tests (`getStats()`).

---

## 3. Plan de acción inmediato

1. Diseñar e implementar `platform/server/courseIndex.cjs` con caché en disco `platform/.cache/course_index.json`, cálculo de ETag rápido (hash o timestamp/size), y las funciones requeridas.
2. Refactorizar `platform/server/courseServer.cjs` para importar `courseIndex.cjs`, soportar `/api/courses` slim con ETag/304, `/api/courses/:id` con ETag/304 y compresión gzip, inyección inline en `index.html`, compresión gzip en estáticos, y endpoint `/healthz`.
3. Validar sintaxis y performance con suite de test Node / script temporal y verificar `npm run build`.
