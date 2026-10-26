# Pre-Flight Briefing — Stream P2 (Vite Build & Inline Manifest)

**Fecha:** 2026-10-26  
**Stream:** P2 (Frente B — Carga de cursos y rendimiento)  
**Frontera exclusiva de escritura:**
- `platform/vite.config.ts`
- `platform/index.html`
- Documentación interna: `.agents/teamwork/m1_zoomfix_split50/stream_P2/`

---

## 1. Baseline de Verificación

1. **Build baseline (`platform/`):**
   - Comando: `npm run build` (`tsc && vite build`)
   - Resultado: **PASS** (código 0, completado en 6.41 s).
   - **Tamaño actual de artefactos emitidos:**
     - `dist/api/courses.json`: **59,788.11 kB** (~59.8 MB) — archivo monstruoso con todos los cursos incrustados con `null, 2`.
     - `dist/api/courses/<id>.json` y `dist/courses/<filename>`: emitidos con `JSON.stringify(c.data, null, 2)` (pretty-printed, sumando decenas de MB).
     - `dist/index.html`: 1.46 kB (sin marcador `<!--COURSE_MANIFEST-->`).

2. **Git status:**
   - Archivos en frontera limpios.

---

## 2. Diagnóstico de Archivos en Frontera

### A. `platform/index.html` (23 líneas)
- Contiene los preloads de KaTeX de 1F y metadatos básicos.
- **Faltante:** Marcador `<!--COURSE_MANIFEST-->` dentro de `<head>` para ser transformado por Vite / servidor.

### B. `platform/vite.config.ts` (223 líneas)
- `generateBundle()` emite `api/courses.json` con `source: JSON.stringify({ courses }, null, 2)` donde cada item en `courses` incluye `data: check.data` (59.8 MB).
- Emite cursos individuales con `null, 2` (sin minificar).
- No tiene hook `transformIndexHtml` para inyectar `<script id="course-manifest" type="application/json">...</script>`.
- El middleware de desarrollo (`handleApiMiddleware`) duplica la lógica de validación/escaneo de cursos y devuelve el objeto con `data` incrustado en `/api/courses`.
- **Faltante:**
  - Integración con `./server/courseIndex.cjs` para reutilizar la lógica compartida de indexación y manifiesto.
  - Generación de manifiesto SLIM (< 10 KB, sin campo `data`).
  - Minificación de cursos individuales (`JSON.stringify(c.data)`).
  - Inyección de manifest inline en `transformIndexHtml` reemplazando `<!--COURSE_MANIFEST-->` con escape seguro de `\u003c`.
  - Endpoint dev `/api/courses` devolviendo manifest slim y `/api/courses/:id` devolviendo curso individual.
  - Resiliencia de ejecución concurrente: si `courseIndex.cjs` aún no ha sido escrito por Stream P1 en el momento del build, fallback limpio que cumple exactamente la misma firma y especificación.

---

## 3. Criterios de Aceptación Objetivos
- **AC-20:** `platform/index.html` con `<!--COURSE_MANIFEST-->` transformado a `<script id="course-manifest" type="application/json">` con manifest slim.
- **AC-24:** `dist/api/courses.json` pasa de ~60 MB a < 50 KB (< 10 KB real).
- Cursos individuales emitidos minificados en `dist/api/courses/<id>.json` y `dist/courses/<filename>`.
- `npm run build` verde y sin regresiones.
