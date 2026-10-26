# Pre-Flight Briefing — Stream 1F (MathText & KaTeX Font Preload)

**Fecha:** 2026-10-26  
**Stream:** 1F  
**Frontera exclusiva de escritura:**
- `platform/src/components/MathText.tsx`
- `platform/index.html`
- Documentación interna del stream: `.agents/teamwork/m1_zoomfix_split50/stream_1F/`

---

## 1. Baseline de Verificación

1. **TypeScript check (`platform/`):**
   - Comando: `npx tsc --noEmit`
   - Resultado: **PASS** (código 0, sin errores ni warnings).
   - Nota: Por instrucción explícita del orquestador, para evitar colisiones con streams paralelos (1A, 1C, 1D, 1E), no se usa `npm run build` en el `dist/` común; las validaciones de bundling se realizan en directorio temporal aislado (`../.tmp_1f_dist`) que se eliminará al terminar.

2. **Git Status:**
   - Archivos en frontera limpios y sin modificaciones previas en este stream.

---

## 2. Diagnóstico de Archivos en Frontera

### A. `platform/src/components/MathText.tsx` (86 líneas)
- L73: Envoltorio actual para fórmulas matemáticas:
  ```tsx
  className={displayMode ? 'block my-2 overflow-x-auto text-center' : 'inline-block mx-0.5'}
  ```
- **Problema identificado:** El uso de `inline-block` para fórmulas inline provoca que fórmulas compuestas (como `y_i = 77 + 3x_i + \epsilon_i`) se comporten como cajas atómicas rígidas o se deformen artificialmente en segmentos fracturados cuando no caben en una línea, o causen desbordes/barras de scroll en anchos reducidos (split-view 50%).
- **Solución requerida (AC-18):** Cambiar `inline-block mx-0.5` a `inline mx-0.5` para permitir salto de línea natural entre elementos de KaTeX.
- **Invariantes a preservar:** `displayMode` con `'block my-2 overflow-x-auto text-center'`, llamada a `katex.renderToString`, parseo de `$$...$$` y `$...$`, comentarios existentes y firma del componente (`text`, `className`, `inline`).

### B. `platform/index.html` (19 líneas)
- Actualmente no tiene precarga de fuentes (`<link rel="preload" ...>`).
- Las fuentes KaTeX más comunes (`KaTeX_Main-Regular.woff2`, `KaTeX_Math-Italic.woff2`, `KaTeX_Size1-Regular.woff2`, `KaTeX_AMS-Regular.woff2`) son solicitadas tardíamente tras la evaluación del CSS en tiempo de ejecución, lo que puede causar flash de texto no formateado (FOUT) o latencia de renderizado inicial.
- **Desafío técnico Vite:** Vite procesa las fuentes en build y les asigna hash en `assets/KaTeX_...-[hash].woff2`.
- **Estrategia a investigar:** Determinar el método óptimo soportado por Vite para enlazar o precargar estas 4 fuentes woff2 con sus hashes correctos sin romper desarrollo ni producción y sin tocar archivos fuera de la frontera.

---

## 3. Plan de Acción Inmediato

1. Probar en `index.html` la estrategia de importación/preload de fuentes woff2 para Vite (`/node_modules/katex/dist/fonts/...` vs import vía script/link con `?url` o ruta Vite).
2. Actualizar `platform/src/components/MathText.tsx` cambiando `inline-block mx-0.5` por `inline mx-0.5`.
3. Validar con `npx tsc --noEmit` y build temporal en `../.tmp_1f_dist`.
4. Limpiar directorio temporal y emitir `handoff.md`.
