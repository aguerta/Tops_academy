# Handoff — Stream 2B: Browser Viewport Matrix E2E Test Suite

**Stream:** 2B  
**Fecha:** 2026-10-26  
**Frontera exclusiva cumplida:**
- `tests/e2e_m1_viewport_matrix.mjs` (nuevo script de prueba end-to-end con Playwright)
- `.agents/teamwork/m1_zoomfix_split50/screens/` (21 screenshots de evidencia correspondientes a los 7 viewports evaluados)
- `.agents/teamwork/m1_zoomfix_split50/stream_2B/` (documentación: BRIEFING.md y handoff.md)

---

## 1. Resumen de Entregas y Ejecución

Se implementó el script de verificación automatizado en navegador real Chromium `tests/e2e_m1_viewport_matrix.mjs` bajo las especificaciones de `plan.md` y `ORIGINAL_REQUEST.md`.

### Aspectos Técnicos Destacados:
1. **Zero Dependencies / No tocar `package.json`:**
   - La suite carga dinámicamente Playwright desde la caché global de `npx` (`AppData/Local/npm-cache/_npx/.../playwright`).
   - Reutiliza el binario Chromium v1243 preinstalado en `%LOCALAPPDATA%\ms-playwright\chromium-1243\chrome-win64\chrome.exe` sin requerir descargas ni comandos `playwright install`.
2. **Aislamiento y Ciclo de Vida del Servidor:**
   - Gestiona automáticamente el ciclo de vida del servidor backend/frontend (`platform/server/courseServer.cjs`) en un puerto libre dinámico sin colisionar con otros procesos.
   - Garantiza el apagado determinista tanto del servidor como del navegador en bloques `finally`.
3. **Flujo de Usuario Completo Probado:**
   - Carga la librería de cursos (`CourseLibrary`).
   - Abre un curso con banco real de ejercicios (`Saul Control Optimo`, con 350 preguntas MC7).
   - Verifica el layout y la responsividad del `Sidebar` en `CourseOverview`.
   - Inicia una sesión de práctica desde el botón de competencia, transiciona a través de `PreExerciseModal` y entra a `PracticeSession`.
   - Evalúa el grid de 7 opciones (MC7) bajo container queries (`@container`).
   - Verifica la visibilidad de los controles de acción (`#check-btn`) dentro de los límites del viewport.
   - Interactúa seleccionando una opción y ejecutando el chequeo para validar el estado post-respuesta y la capa de feedback.

---

## 2. Resultados por Viewport (Matriz E2E)

Todos los viewports requeridos alcanzaron una tasa de éxito del **100% (PASS)**:

| Viewport | Tipo de Pantalla | Overview (No-Scroll) | Sidebar Drawer (<1024px) / Fijo (>=1024px) | Practice (No-Scroll) | Check Button Visible | Columnas MC7 (Esperado) | Answered (No-Scroll) | Estado Final |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **683×768** | Split View 50% (Laptop 1366) | ✅ PASS | ✅ PASS (Off-canvas) | ✅ PASS | ✅ PASS (En viewport) | 2 col (2) | ✅ PASS | **PASS** |
| **720×900** | Split View 50% (Laptop 1440) | ✅ PASS | ✅ PASS (Off-canvas) | ✅ PASS | ✅ PASS (En viewport) | 2 col (2) | ✅ PASS | **PASS** |
| **800×900** | Split View 50% (Laptop 1600) | ✅ PASS | ✅ PASS (Off-canvas) | ✅ PASS | ✅ PASS (En viewport) | 2 col (2) | ✅ PASS | **PASS** |
| **960×1080** | Split View 50% (Desktop 1080p) | ✅ PASS | ✅ PASS (Off-canvas) | ✅ PASS | ✅ PASS (En viewport) | 2 col (2) | ✅ PASS | **PASS** |
| **1366×768** | Full-width Laptop HD | ✅ PASS | ✅ PASS (Fijo en flujo) | ✅ PASS | ✅ PASS (En viewport) | 2 col (2) | ✅ PASS | **PASS** |
| **1440×900** | Full-width Desktop | ✅ PASS | ✅ PASS (Fijo en flujo) | ✅ PASS | ✅ PASS (En viewport) | 2 col (2) | ✅ PASS | **PASS** |
| **390×844** | Móvil (iPhone 12/13/14) | ✅ PASS | ✅ PASS (Off-canvas) | ✅ PASS | ✅ PASS (En viewport) | 1 col (1) | ✅ PASS | **PASS** |

---

## 3. Verificación de Criterios de Aceptación (AC)

- **AC-1 (Zero scroll horizontal):** Cumplido en el 100% de las pantallas tanto en `CourseOverview`, `PracticeSession`, como en estado respondido (`document.documentElement.scrollWidth <= window.innerWidth`).
- **AC-2 & AC-4 (Grid dinámico MC7):**
  - En anchos split view laptop y desktop (683px, 720px, 800px, 960px, 1366px, 1440px), el contenedor de la pregunta supera los 600px y las opciones se organizan automáticamente en 2 columnas con orden columna-primero.
  - En móvil (390px), el contenedor mide < 600px y las opciones colapsan automáticamente a 1 columna.
- **AC-3 (Visibilidad de controles en laptops bajas):** A 768px de altura (683×768 y 1366×768), el botón `check-btn` permanece completamente visible dentro de los límites del viewport en el footer fijo sin recorte alguno.
- **AC-5 (Sidebar responsivo):**
  - A `< 1024px`, el botón `sidebar-toggle` está presente y visible, mientras que el `sidebar` se mantiene oculto off-canvas (clases `fixed -translate-x-full`), permitiendo que el área de contenido principal aproveche el 100% del ancho split view.
  - A `>= 1024px`, el botón `sidebar-toggle` permanece oculto y el `sidebar` se ubica estáticamente ocupando su columna normal.
- **AC-10 (Cero regresiones):**
  - `npm run build` en `platform/` ejecuta `tsc && vite build` exitosamente en 7.20s con código de salida 0.

---

## 4. Evidencia Visual Capturada

Se generaron 21 capturas PNG en `.agents/teamwork/m1_zoomfix_split50/screens/`:
- `overview_683x768.png`, `overview_720x900.png`, `overview_800x900.png`, `overview_960x1080.png`, `overview_1366x768.png`, `overview_1440x900.png`, `overview_390x844.png`
- `practice_683x768.png`, `practice_720x900.png`, `practice_800x900.png`, `practice_960x1080.png`, `practice_1366x768.png`, `practice_1440x900.png`, `practice_390x844.png`
- `answered_683x768.png`, `answered_720x900.png`, `answered_800x900.png`, `answered_960x1080.png`, `answered_1366x768.png`, `answered_1440x900.png`, `answered_390x844.png`

---

## 5. Instrucciones de Reproducción

Para re-ejecutar la suite en cualquier momento de forma determinista:
```bash
node tests/e2e_m1_viewport_matrix.mjs
```
El script detectará automáticamente los puertos disponibles, iniciará el servidor, ejecutará los 7 viewports y registrará la tabla de resultados en stdout con código de retorno 0.


---

## 6. Improver — Endurecimiento y Validación Robusta

**Fecha:** 2026-10-26  
**Rol:** Mejorador Stream 2B (`m1zf_improver`)  
**Frontera respetada:** Únicamente `tests/e2e_m1_viewport_matrix.mjs` y `.agents/teamwork/m1_zoomfix_split50/screens/`.

### 6.1 Endurecimientos Implementados en `tests/e2e_m1_viewport_matrix.mjs`

1. **Asserts no triviales de distribución geométrica (4+3 por posición):**
   - Validación estricta de que la pregunta contiene exactamente 7 opciones (`options.length === 7`).
   - Para viewports con `expectColumns === 2` (contenedor >= 600px):
     - **Columna 1 (izquierda):** opciones [0, 1, 2, 3] (4 opciones) comparten la coordenada X (`col1X`) con tolerancia <= 15px y orden vertical estricto descendente ($y_0 < y_1 < y_2 < y_3$).
     - **Columna 2 (derecha):** opciones [4, 5, 6] (3 opciones) comparten la coordenada X (`col2X`) con $col2X \ge col1X + 40\text{px}$ y orden vertical estricto descendente ($y_4 < y_5 < y_6$).
     - **Alineación fila 1:** alineación horizontal entre opción 0 y opción 4 ($|y_0 - y_4| \le 35\text{px}$).
   - Para móvil `390x844` (`expectColumns === 1`):
     - Todas las 7 opciones comparten la misma columna X y se ordenan estrictamente de forma vertical ($y_0 < y_1 < \dots < y_6$).

2. **Detección de puertos ocupados y reintento resiliente:**
   - Función `startServerWithRetry(maxRetries = 3)` con detección dinámica de puertos libres en `127.0.0.1`.
   - Manejo anticipado de colisiones (`EADDRINUSE` o salida prematura) con reintento automático en puertos alternativos.

3. **Timeouts robustos y diagnóstico granular:**
   - Constantes configuradas: `SERVER_START_TIMEOUT = 15000ms`, `PAGE_NAV_TIMEOUT = 15000ms`, `SELECTOR_TIMEOUT = 12000ms`.
   - Sondeo de disponibilidad del servidor cada 200ms hasta 15 segundos.

4. **Cierre determinista de procesos en `finally` (Tree-Kill Windows):**
   - Función `killProcessTree(pid)` usando `taskkill /pid <PID> /T /F` en Windows para evitar procesos huérfanos de Node.js o servidores Vite.
   - Handlers globales registrados para `SIGINT`, `SIGTERM`, `uncaughtException` y `unhandledRejection` con invocación de `globalCleanup()`.
   - Bloque `finally` en `runMatrix` asegurando cierre secuencial de contextos, navegador y servidor.
   - Verificado con `netstat` y `Get-Process`: cero puertos o procesos node/vite remanentes.

5. **Resolución resiliente de rutas Windows:**
   - Búsqueda recursiva multirruta de Playwright y Chromium v1243 considerando `%LOCALAPPDATA%`, `%USERPROFILE%` y variables de entorno estándar.

6. **Caso con enunciado largo y KaTeX denso:**
   - Verificación de la renderización activa de fórmulas matemáticas con KaTeX (`.katex` y `.katex-display`).
   - Guarda de desbordamiento horizontal: asegura que ningún elemento KaTeX sobrepase los límites de la pantalla ($rect.right \le window.innerWidth + 2$ y $rect.left \ge -2$).
   - Generación de captura específica `katex_dense_683x768.png` con enunciados que superan los 240 caracteres e integrales LaTeX.

7. **Viewport 683×768 con FeedbackToast y controles visibles:**
   - Se probó la interacción completa de respuesta con error intencional (opción 0) para activar el toast de retroalimentación diagnóstica (`[data-testid="feedback-toast"]`).
   - Se verificó que el botón de acción en el footer (`[data-testid="check-btn"]` / `[data-testid="quick-redo-btn"]` / `[data-testid="next-question-btn"]`) permanezca completamente dentro de los límites del viewport ($y + height \le 768\text{px}$ y $x + width \le 683\text{px}$).
   - Se verificó que el toast flotante no ocluya el botón del footer ($toastBox.y + toastBox.height \le actionBtnBox.y + 2\text{px}$, dejando un margen vertical libre).
   - Generación de captura específica `toast_feedback_683x768.png`.

---

### 6.2 Resultados de la Re-ejecución Completa

```
================================================================
 STARTING MILESTONE 1 VIEWPORT MATRIX E2E SUITE (HARDENED)
================================================================

[Playwright] Using Chromium executable: C:\Users\augus\AppData\Local\ms-playwright\chromium-1243\chrome-win64\chrome.exe
[E2E-Server] Attempt 1/3: Launching courseServer on http://127.0.0.1:62505...
[Server] Course server running at http://127.0.0.1:62505
[E2E-Server] courseServer is up and answering at http://127.0.0.1:62505 (PID: 7556)

Testing Viewport: 683x768 (Split 50% 1366) -> ✅ PASS
Testing Viewport: 720x900 (Split 50% 1440) -> ✅ PASS
Testing Viewport: 800x900 (Split 50% 1600) -> ✅ PASS
Testing Viewport: 960x1080 (Split 50% 1080p) -> ✅ PASS
Testing Viewport: 1366x768 (Laptop HD Full) -> ✅ PASS
Testing Viewport: 1440x900 (Desktop Full) -> ✅ PASS
Testing Viewport: 390x844 (Mobile Phone) -> ✅ PASS

================================================================
 MATRIX SUMMARY (HARDENED)
================================================================
┌─────────┬────────────┬──────────┬─────────┬──────────┬────────┬──────────────────────────────────────────┬───────────┬────────┬─────────────────┬──────────┬────────┐
│ (index) │ Viewport   │ Overview │ Sidebar │ Practice │ KaTeX  │ Distribution                             │ Check-Btn │ Toast  │ Btn-After-Toast │ Answered │ Status │
├─────────┼────────────┼──────────┼─────────┼──────────┼────────┼──────────────────────────────────────────┼───────────┼────────┼─────────────────┼──────────┼────────┤
│ 0       │ '683x768'  │ 'PASS'   │ 'PASS'  │ 'PASS'   │ 'PASS' │ '4 left + 3 right (column-first) (PASS)' │ 'PASS'    │ 'PASS' │ 'PASS'          │ 'PASS'   │ 'PASS' │
│ 1       │ '720x900'  │ 'PASS'   │ 'PASS'  │ 'PASS'   │ 'PASS' │ '4 left + 3 right (column-first) (PASS)' │ 'PASS'    │ 'PASS' │ 'PASS'          │ 'PASS'   │ 'PASS' │
│ 2       │ '800x900'  │ 'PASS'   │ 'PASS'  │ 'PASS'   │ 'PASS' │ '4 left + 3 right (column-first) (PASS)' │ 'PASS'    │ 'PASS' │ 'PASS'          │ 'PASS'   │ 'PASS' │
│ 3       │ '960x1080' │ 'PASS'   │ 'PASS'  │ 'PASS'   │ 'PASS' │ '4 left + 3 right (column-first) (PASS)' │ 'PASS'    │ 'PASS' │ 'PASS'          │ 'PASS'   │ 'PASS' │
│ 4       │ '1366x768' │ 'PASS'   │ 'PASS'  │ 'PASS'   │ 'PASS' │ '4 left + 3 right (column-first) (PASS)' │ 'PASS'    │ 'PASS' │ 'PASS'          │ 'PASS'   │ 'PASS' │
│ 5       │ '1440x900' │ 'PASS'   │ 'PASS'  │ 'PASS'   │ 'PASS' │ '4 left + 3 right (column-first) (PASS)' │ 'PASS'    │ 'PASS' │ 'PASS'          │ 'PASS'   │ 'PASS' │
│ 6       │ '390x844'  │ 'PASS'   │ 'PASS'  │ 'PASS'   │ 'PASS' │ '7 vertical single-column (PASS)'        │ 'PASS'    │ 'PASS' │ 'PASS'          │ 'PASS'   │ 'PASS' │
└─────────┴────────────┴──────────┴─────────┴──────────┴────────┴──────────────────────────────────────────┴───────────┴────────┴─────────────────┴──────────┴────────┘

Matrix suite PASSED 100% across all 7 viewports with non-trivial hardened assertions!
```

---

### 6.3 Verificación de Compilación y Estado Git

- `npm run build` en `platform/`:
  - `tsc && vite build`: Exitoso, 0 errores, tiempo de construcción 5.70s.
- Procesos activos: Cero procesos o servidores colgados (apagado limpio verificado).
- Frontera de archivos: Solo modificados `tests/e2e_m1_viewport_matrix.mjs` y `.agents/teamwork/m1_zoomfix_split50/screens/`.

DONE:: Stream 2B Mejorador completado con éxito.
