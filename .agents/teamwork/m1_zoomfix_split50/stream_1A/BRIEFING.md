# Pre-Flight Briefing — Stream 1A (Question Grid & CSS Contract)

**Fecha:** 2026-10-26  
**Stream:** 1A  
**Frontera exclusiva de escritura:**
- `platform/src/components/QuestionCard.tsx`
- `platform/src/index.css`
- Documentación interna del stream: `.agents/teamwork/m1_zoomfix_split50/stream_1A/`

---

## 1. Baseline de Verificación

1. **TypeScript check (`platform/`):**
   - Comando: `npx tsc --noEmit`
   - Resultado: **PASS** (0 errores, código de salida 0).
   - Nota: Se usa `npx tsc --noEmit` durante streams paralelos para prevenir conflictos en `platform/dist`.

2. **Pytest suite baseline (`Tops_academy/`):**
   - Comando: `.\pytest.cmd -q -x`
   - Resultado: 44 tests pasados, 1 fallo preexistente en `tests/test_assemble_sanitize_katex_r23.py` (diferencia de tilde/encoding en descripción de competencias de cursos ya publicados).

3. **Git Status:**
   - Rama: `optimizaciones_test`
   - Estado de los archivos en frontera: limpios (sin cambios sin guardar).

---

## 2. Diagnóstico de Archivos en Frontera

### A. `platform/src/index.css` (35 líneas)
- Importa KaTeX CSS y directivas `@tailwind`.
- Define `:root` (font-family, colors) y animación de `feedback-toast`.
- **Faltante:**
  - Definición de variables CSS elásticas (`--qc-gap`, `--qc-pad`, `--qc-font`, `--qc-badge`).
  - Container query setup: `.qc-root { container-type: inline-size; container-name: qc; }`.
  - Grid de opciones: `.qc-options` con fallback a 1 columna y `@container qc (min-width: 600px)` con 2 columnas, `grid-auto-flow: column; grid-template-rows: repeat(var(--qc-rows, 4), auto);`.
  - Contenedor de scroll para opciones: `.qc-options-scroll`.
  - KaTeX overflow protection: `.katex-display, .qc-options .katex`.
  - Utilidad `.h-dvh-safe` (`min-height: 100vh; min-height: 100dvh;`).

### B. `platform/src/components/QuestionCard.tsx` (272 líneas)
- Contenedor raíz: `<div data-testid="question-card" className="max-w-3xl mx-auto py-6 px-4">`.
- Opciones: Ambos tipos (`multiple_choice_7_options` y `multiple_select`) usan `<div className="space-y-2">` vertical estricto, `p-3.5`, `gap-3.5`, badge `w-8 h-8`.
- Con 7 opciones en pantalla de laptop (768 px alto o split-view 50% = 683 px), las opciones consumen ~600 px verticales, provocando desborde con el stem y el header/footer.
- **Faltante:**
  - Agregar clase `qc-root` al contenedor principal.
  - Stem con `max-w-none` para aprovechar el ancho disponible de la tarjeta.
  - Para MC7 y multiple_select: contenedor con clase `qc-options` y style inline `--qc-rows: Math.ceil(question.options.length / 2)`.
  - Envolver o dotar de scroll interno con `.qc-options-scroll` para cuando el enunciado o fórmulas sean extensos.
  - Aplicar variables elásticas en badges y opciones preservando intactos todos los `data-testid`, clases existentes (`option-item`, `answer-option`) y lógica de interacción/atajos.

---

## 3. Plan de Acción Inmediato

1. Actualizar `platform/src/index.css` con el contrato CSS acordado (§3 del plan).
2. Actualizar `platform/src/components/QuestionCard.tsx` para implementar el grid de 2 columnas columna-primero, cálculo dinámico de `--qc-rows`, clases elásticas y protección contra overflow KaTeX.
3. Verificar con `npx tsc --noEmit` en `platform/`.
4. Documentar decisiones en `handoff.md`.
