# Pre-Flight Briefing — Stream 2C (Documentation & Spec Update)

**Fecha:** 2026-10-26  
**Stream:** 2C  
**Frontera exclusiva de escritura:**
- `FUTURE_MILESTONES.md` (únicamente §6 fila Milestone 1 y §7 especificación Milestone 1)
- `docs/future_milestones/FUTURE_MILESTONES.md` (espejo idéntico byte a byte)
- Documentación interna del stream: `.agents/teamwork/m1_zoomfix_split50/stream_2C/`

---

## 1. Baseline de Verificación

1. **Compilación Frontend (`platform/`):**
   - Comando: `npm run build`
   - Resultado: **PASS** (1101 módulos transformados, 0 errores, salida exitosa en 6.91s).
   - `tsc && vite build` completado limpiamente.

2. **Test de Paridad Byte a Byte (`tests/test_platform_katex_admission_guard.py`):**
   - Comando: `.venv\Scripts\pytest.exe tests/test_platform_katex_admission_guard.py -k TestFutureMilestonesParity`
   - Resultado: **FAIL pre-flight esperado** (`AssertionError: FUTURE_MILESTONES.md and docs/future_milestones/FUTURE_MILESTONES.md are not identical byte-by-byte`).
   - Causa: Edición previa en el archivo raíz agregando una línea sobre Split-View que no se sincronizó en el espejo `docs/future_milestones/FUTURE_MILESTONES.md`.

3. **Git Status:**
   - Rama: `optimizaciones_test`
   - Estado de los archivos en frontera: `FUTURE_MILESTONES.md` modificado sin commitear en working tree (línea 219 insertada); `docs/future_milestones/FUTURE_MILESTONES.md` sin modificaciones en working tree.

---

## 2. Diagnóstico de Archivos en Frontera

### A. `FUTURE_MILESTONES.md` y `docs/future_milestones/FUTURE_MILESTONES.md`
- **Línea 200 (Matriz §6):**
  - Actualmente indica:
    ```markdown
    | **Milestone 1: Web Ergonomía para Laptops (Zoom-Fix)** | Frontend / UX | **Elimina la fricción visual inmediata.** Grid de 2 columnas para 7 opciones en laptops de 13"-14", eliminando la necesidad de zoom out. | 2 a 4 h | 🎯 **Prioridad Inmediata** |
    ```
  - Debe actualizarse al estado de implementación real tras Gate 1: `🛠️ Implementado, pendiente verificación visual` (conforme a las instrucciones del orquestador, ya que la verificación visual en navegador corresponde a Stream 2B).
- **Línea 217-232 (§7 Especificación Milestone 1):**
  - La especificación actual arrastra la premisa técnica obsoleta de `min-width: 1024px` y `max-height: 850px` para activar 2 columnas. En split view al 50% (683 px a 960 px), una media query de `min-width: 1024px` nunca se activaría.
  - No describe los componentes realmente implementados por los streams 1A–1E:
    - **1A:** Container Queries nativas (`@container qc (min-width: 600px)`), variables elásticas `clamp()`, orden columna-primero (`grid-auto-flow: column; grid-template-rows: repeat(var(--qc-rows), auto)`), scroll interno de opciones (`.qc-options-scroll`), utilidades `.h-dvh-safe` y aislamiento KaTeX.
    - **1B:** Sidebar Drawer off-canvas para `< 1024px` con botón hamburguesa accesible (`sidebar-toggle`), overlay con click-outside, focus trap accesible, cierre con `Escape` y resize, dimensiones responsivas (`lg:w-56 xl:w-64`).
    - **1C:** Bottom Sheet responsivo en `FeedbackToast.tsx` (`< 1024px` o `<= 850px` alto) con `max-height: 45dvh`, scroll propio y margen de 16px sobre el footer (`bottom-20`), y SVG responsivo en `CoordinatePlane.tsx` (`viewBox`, `max-w-[340px]`, `max-h-[30dvh]`, `aspect-ratio`).
    - **1D:** Practice Shell con header adaptable (`h-12` en `max-height: 850px`), footer compacto (`h-16`, `px-4 sm:px-8`), padding compensatorio en `main` (`pb-20`), progress dots colapsables en `< 520px` y erradicación de `min-h-screen`/`100vh` en favor de `h-dvh-safe` / `100dvh`.
    - **1E:** Resto de vistas (`CourseLibrary`, `CourseOverview`, `MasteryGrid`, `MasteryLegend`, `PreExerciseModal`, `CompletionScreen`, `CourseChallenge`) con grids adaptativos (`sm:grid-cols-2 xl:grid-cols-3`), `min-w-0`, paddings elásticos y protección contra overflow KaTeX en títulos y tarjetas.
  - Debe incluir la **matriz de viewports obligatoria**: 683×768 (Laptop 1366 50%), 720×900 (Laptop 1440 50%), 800×900 (1600 50%), 960×1080 (FHD 50%), 1366×768 (Laptop full), 1440×900 (Laptop full), 390×844 (Móvil).

---

## 3. Plan de Acción Inmediato

1. Editar `FUTURE_MILESTONES.md`:
   - Actualizar la fila de Milestone 1 en la matriz §6 (línea 200 aprox.).
   - Reescribir la sección §7 Milestone 1 integrando el objetivo 50% split view, container queries nativas, matriz de viewports, detalles técnicos de todos los componentes implementados (1A–1E) y el estado formal `🛠️ Implementado, pendiente verificación visual`.
   - Preservar escrupulosamente el resto del documento y formato LF.
2. Copiar exactamente en bytes `FUTURE_MILESTONES.md` hacia `docs/future_milestones/FUTURE_MILESTONES.md`.
3. Ejecutar y certificar `pytest tests/test_platform_katex_admission_guard.py -k TestFutureMilestonesParity`.
4. Ejecutar `npm run build` en `platform/` para certificar cero regresión general.
5. Elaborar `handoff.md` en `stream_2C/`.
