# Pre-Flight Briefing — Stream 2B (Browser Viewport Matrix E2E)

**Fecha:** 2026-10-26  
**Stream:** 2B  
**Frontera exclusiva de escritura:**
- `tests/e2e_m1_viewport_matrix.mjs` (nuevo script de prueba e2e)
- `.agents/teamwork/m1_zoomfix_split50/screens/` (screenshots de evidencia por viewport)
- `.agents/teamwork/m1_zoomfix_split50/stream_2B/` (documentación: BRIEFING.md, handoff.md)

---

## 1. Baseline de Verificación

1. **Build Frontend (`platform/`):**
   - Comando: `npm run build`
   - Resultado: **PASS** (`tsc && vite build` completado exitosamente en 6.23s, chunks generados y api JSONs emitidos en `dist/`).

2. **Pytest Suite (`Tops_academy/`):**
   - Comando: `.\pytest.cmd -q -x`
   - Resultado: 44 tests pasados, 1 fallo preexistente en `tests/test_assemble_sanitize_katex_r23.py` (idempotency check en strings con caracteres especiales en cursos antiguos, consistente con Gate 1).

3. **Playwright & Chromium Environment:**
   - Binario verificado: `C:\Users\augus\AppData\Local\ms-playwright\chromium-1243\chrome-win64\chrome.exe` existente y funcional.
   - Paquete Playwright: disponible a través de `npx -y playwright@1.63.0` en `C:\Users\augus\AppData\Local\npm-cache\_npx\*\node_modules\playwright`.
   - Carga dinámica comprobada: Node puede requerir playwright directamente resolviendo desde la caché de `npx` y lanzar chromium headless apuntando a `chromium-1243` sin descargas adicionales ni modificar `package.json`.

---

## 2. Diagnóstico y Especificación del Stream 2B

### A. Matriz de Viewports Obligatoria
De acuerdo con `plan.md` y `ORIGINAL_REQUEST.md`:
- `683x768` (Split view 50% en laptop HD 1366x768)
- `720x900` (Split view 50% en pantalla 1440x900)
- `800x900` (Split view 50% en pantalla 1600x900)
- `960x1080` (Split view 50% en pantalla Full HD 1920x1080)
- `1366x768` (Laptop HD full width)
- `1440x900` (Laptop 1440x900 full width)
- `390x844` (Móvil moderno / split estrecho)

### B. Criterios de Aceptación a Medir por Viewport
1. **AC-1 No scroll horizontal:** En cada viewport y en cada vista clave (overview, práctica), verificar que `document.documentElement.scrollWidth <= window.innerWidth`.
2. **AC-2 Grid MC7 en contenedor >= 600px:** Para MC7 en práctica, si el contenedor de la pregunta es >= 600px de ancho, las opciones deben organizarse en 2 columnas.
3. **AC-3 / Visibilidad de botones:** `#check-btn` / `button[data-testid="check-btn"]` debe estar dentro del viewport visible sin scroll de página o accesible adecuadamente en el contenedor visible.
4. **AC-4 Contenedor < 600px (móvil):** En 390x844, las opciones deben mostrarse en 1 columna.
5. **AC-5 Sidebar responsivo:** En viewports < 1024px (`683x768`, `720x900`, `800x900`, `960x1080`, `390x844`), en `CourseOverview`:
   - El botón `[data-testid="sidebar-toggle"]` debe existir.
   - El sidebar (`[data-testid="sidebar"]`) no debe ocupar ancho horizontal en el flujo normal (off-canvas drawer cerrado por defecto).
   - En viewports >= 1024px (`1366x768`, `1440x900`), el sidebar es visible/fijo.

### C. Estrategia de Servidor y Aislamiento
- Usar un servidor HTTP embebido o el servidor estático/preview `node server/courseServer.cjs` en un puerto no conflictivo (ej: 5188) para servir la app construida (`platform/dist`) y la API de cursos (`courses/*.json`).
- Levantar browser Chromium headless, recorrer la matriz, ejecutar aserciones, capturar screenshots PNG de alta calidad en `.agents/teamwork/m1_zoomfix_split50/screens/`.
- Apagar el servidor y cerrar el navegador de forma determinista y segura en bloques `finally`.
