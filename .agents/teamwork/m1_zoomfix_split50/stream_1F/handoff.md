# Handoff — Stream 1F (MathText & KaTeX Font Preload)

**Fecha:** 2026-10-26  
**Stream:** 1F  
**Rol:** Implementador & Mejorador (Hardened)  
**Estado:** COMPLETADO  
**Frontera exclusiva de escritura:**
- `platform/src/components/MathText.tsx`
- `platform/index.html`
- `.agents/teamwork/m1_zoomfix_split50/stream_1F/`

---

## 1. Resumen de Cambios Realizados (Implementador)

### A. `platform/src/components/MathText.tsx`
- **Línea 73:** Se cambió la clase del contenedor de fórmula inline de `'inline-block mx-0.5'` a `'inline mx-0.5'`.
  ```tsx
  // Antes:
  className={displayMode ? 'block my-2 overflow-x-auto text-center' : 'inline-block mx-0.5'}
  // Ahora:
  className={displayMode ? 'block my-2 overflow-x-auto text-center' : 'inline mx-0.5'}
  ```
- **Impacto (AC-18):** Las fórmulas inline ya no se comportan como cajas atómicas rígidas con salto de línea forzado o fragmentación anómala. Al renderizarse como `inline`, el navegador puede realizar saltos de línea naturales entre subelementos KaTeX (`.mord`, `.mbin`, `.mrel`), previniendo desbordes horizontales y barras de scroll en viewports estrechos (split 50% / anchos reducidos).
- **Invariantes preservados:**
  - El display math (`displayMode: true`) mantiene intacta la clase `'block my-2 overflow-x-auto text-center'`.
  - La lógica del parser de `$$...$$` y `$...$` no fue alterada.
  - La API del componente (`text`, `className`, `inline`) y el manejo de fallback por error (`text-red-500 font-mono`) se mantienen al 100%.

### B. `platform/index.html`
- Se agregaron las etiquetas de precarga `<link rel="preload">` para las cuatro fuentes KaTeX más utilizadas:
  ```html
  <link rel="preload" href="/node_modules/katex/dist/fonts/KaTeX_Main-Regular.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="preload" href="/node_modules/katex/dist/fonts/KaTeX_Math-Italic.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="preload" href="/node_modules/katex/dist/fonts/KaTeX_Size1-Regular.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="preload" href="/node_modules/katex/dist/fonts/KaTeX_AMS-Regular.woff2" as="font" type="font/woff2" crossorigin />
  ```
- **Resolución de nombres y hashes en Vite:**
  - En modo desarrollo (`vite dev`), Vite resuelve y sirve directamente las fuentes desde `/node_modules/katex/dist/fonts/`.
  - En modo producción (`vite build`), el plugin HTML nativo de Vite detecta las referencias en `<link rel="preload">`, emite los archivos de fuentes en `dist/assets/` con sus hashes de contenido correspondientes y reescribe automáticamente los atributos `href`:
    - `KaTeX_Main-Regular.woff2` -> `./assets/KaTeX_Main-Regular-B22Nviop.woff2`
    - `KaTeX_Math-Italic.woff2` -> `./assets/KaTeX_Math-Italic-t53AETM-.woff2`
    - `KaTeX_Size1-Regular.woff2` -> `./assets/KaTeX_Size1-Regular-mCD8mA8B.woff2`
    - `KaTeX_AMS-Regular.woff2` -> `./assets/KaTeX_AMS-Regular-BQhdFMY1.woff2`
  - Esto garantiza que el navegador precargue las fuentes inmediatamente en paralelo con la carga del HTML y CSS, eliminando el FOUT (Flash of Unstyled Text) sin rutas rotas ni discrepancias de hash.
- **Alcance respetado:**
  - No se agregó ningún marcador del Frente B (`<!--COURSE_MANIFEST-->`).
  - No se tocaron archivos de otros streams.

---

## 2. Verificaciones Iniciales (Implementador)

1. **Type Checking:**
   - Comando: `npx tsc --noEmit` en `platform/`
   - Resultado: Salida limpia, código 0, sin errores de tipos.

2. **Bundle & Hash Test en Directorio Temporal:**
   - Comando: `npx vite build --outDir ../.tmp_1f_dist --emptyOutDir`
   - Resultado: Compilación exitosa en 7.92s.
   - Verificación de `../.tmp_1f_dist/index.html`: Se confirmó que los 4 enlaces `<link rel="preload">` apuntan exactamente a los archivos `.woff2` emitidos en `assets/` con sus hashes.
   - Limpieza: El directorio temporal `.tmp_1f_dist` fue eliminado inmediatamente con `Remove-Item -Recurse -Force`. Se verificó `Test-Path .tmp_1f_dist` devolviendo `False`.

3. **Git Diff y Frontera:**
   - Solo modificados dentro de nuestra frontera: `platform/src/components/MathText.tsx` y `platform/index.html`.
   - Cero dependencias npm agregadas.

---

## 3. Riesgos y Mitigaciones

- **Compatibilidad con Safari / Chromium antiguo:** El atributo `crossorigin` es requerido por la especificación para precargas de fuentes web con CORS anónimo (`crossorigin="anonymous"` / `crossorigin`), lo cual fue incluido en los 4 links.
- **Prioridad de ancho de banda:** Solo se precargan las 4 fuentes esenciales (Regular, Math-Italic, Size1, AMS), evitando saturar el ancho de banda con fuentes decorativas o poco frecuentes (Bold, Fraktur, SansSerif, Typewriter).

---

## 4. Endurecimiento y Verificación del Mejorador (Improver)

El Mejorador ejecutó un conjunto exhaustivo de pruebas automatizadas en Chromium v1243 vía Playwright 1.63.0 (`%LOCALAPPDATA%\ms-playwright\chromium-1243\chrome-win64\chrome.exe`) cubriendo todos los casos borde del stream:

### A. Verificación en Vite Dev (`vite dev` + Playwright)
- Se levantó una instancia dedicada de Vite Dev (`npx vite --port 5183 --strictPort` desde `platform/`).
- Se verificó la resolución HTTP de las 4 fuentes precargadas:
  - `KaTeX_Main-Regular.woff2` -> **HTTP 200 OK**
  - `KaTeX_Math-Italic.woff2` -> **HTTP 200 OK**
  - `KaTeX_Size1-Regular.woff2` -> **HTTP 200 OK**
  - `KaTeX_AMS-Regular.woff2` -> **HTTP 200 OK**
- Se esperó un periodo de inactividad de 4 segundos tras el evento `load`:
  - **0 advertencias** en consola relativas a preloads no utilizados (*"preload not used within a few seconds"*).
  - **0 errores** de consola y **0 peticiones fallidas** (404/500).

### B. Verificación de Compatibilidad de Base Relativa (`base: './'`)
- Se realizó un build completo a un outDir temporal (`../.tmp_1f_verify_dist`) con `base: './'`.
- Se validó que el archivo `index.html` resultante reescribió las 4 rutas a `./assets/KaTeX_*.woff2` y que todos los binarios existen físicamente en disco con tamaños íntegros (~5 KB a ~28 KB).
- Se ejecutó `vite preview --outDir ../.tmp_1f_verify_dist --port 5184 --strictPort`.
- Con Playwright se confirmó que la aplicación carga perfectamente en modo producción con base relativa, resolviendo las 4 fuentes con **HTTP 200 OK** y **0 errores de red o consola**.
- El directorio temporal `.tmp_1f_verify_dist` fue eliminado inmediatamente y se verificó su inexistencia.

### C. Endurecimiento de Casos Borde en `MathText` (`inline` vs `inline-block`)
Se evaluó el comportamiento del componente `MathText` en el contexto real del navegador (con estilos Tailwind y KaTeX compilados):
1. **Fórmulas con fracciones (`\frac{a+b}{c+d}`):**
   - Estilo computado: `display: inline`, `margin-left: 2px`, `margin-right: 2px` (aportados por `mx-0.5`).
   - Fluyen en línea con el texto sin romper palabras precedentes ni subsiguientes.
2. **Subíndices y Superíndices (`$x_i^2 + y_{n-1}^{k+1}$`):**
   - Estilo computado: `display: inline`, `margin-left: 2px`, `margin-right: 2px`.
   - Se alinean correctamente a la línea base tipográfica.
3. **Display Math (`$$...$$`):**
   - Estilo computado: `display: block`, `text-align: center`, `overflow-x: auto`.
   - Mantiene la presentación en bloque centrado con contención de desborde horizontal para fórmulas ultra-anchas.
4. **Partición de línea en contenedores estrechos (260 px):**
   - Texto mezclado con fórmulas complejas (`\hat{\beta} = (X'X)^{-1}X'y`):
   - `scrollWidth: 260px`, `clientWidth: 260px`, `height: 68px` (partición multilínea fluida sin desborde horizontal ni scrollbars indeseadas).
5. **Preservación de Espaciado (`mx-0.5`):**
   - Se verificó que las fórmulas inline consecutivas o alternadas con texto mantienen `mx-0.5` activo, evitando que los símbolos matemáticos se peguen a las palabras adyacentes.
6. **Accesibilidad (a11y):**
   - Se confirmó que el markup generado por KaTeX asigna `aria-hidden="true"` al contenedor visual `.katex-html` y preserva `.katex-mathml` para lectores de pantalla.
7. **Soporte para 3 a 9 opciones (MC7 y multiple_select):**
   - Se verificó la suite real de cursos en `courses/`, incluyendo preguntas MC7 (p. ej. `Q-H01-001` en `asyntotic_estatistics_v7.json`) donde las 7 opciones contienen fórmulas LaTeX avanzadas (`\operatorname{plim}`, matrices, inversas, fracciones).
   - Se validó en toda la matriz de viewports (683×768, 720×900, 800×900, 960×1080, 1366×768, 1440×900, 390×844) que las opciones y el stem tienen `scrollWidth <= clientWidth` (cero desbordes horizontales).
8. **Invarianza de API:**
   - La firma de props (`text: string`, `className?: string`, `inline?: boolean`) se mantiene 100% idéntica.

### D. Verificación Final de Compilación (Fase Previa)
- `npx tsc --noEmit` en `platform/`: **Exit code 0** (0 errores de tipos).
- `npm run build` en `platform/`: **Exit code 0** (compilación limpia con Vite v6.4.4).
- `git diff`: **0 archivos modificados fuera de la frontera exclusiva** (`platform/src/components/MathText.tsx`, `platform/index.html`, `stream_1F/handoff.md`).

---

## 5. Remediation Task — Frente A: KaTeX \text{} Long Prose Wrapping

### A. Diagnóstico del Problema Visual
En cursos como `gavilano_pre_parcial.json`, `asyntotic_estatistics_v7.json`, `estadistica_3_pre_parcial.json`:
- Las opciones de respuesta contenían prosa explicativa dentro del delimitador inline math `$...$`, como por ejemplo:
  - `$P = 169 \text{ porque los compradores no toleran postergar su compra}$`
  - `$y_i = \hat{\beta}_0 + \hat{\beta}_1 x_i + \varepsilon_i \text{ con estimadores muestrales}$`
  - `$\text{plim}_{n \to \infty} \left(\frac{X'X}{6772}\right) = Q \text{ con todos } \lambda_j > 0 \text{ y } \det(Q) > 0$`
- KaTeX convierte los espacios dentro de `\text{...}` en `\u00a0` (`&nbsp;` non-breaking spaces) y aplica `white-space: nowrap` en sus elementos `.katex-html` y `.katex .base`.
- Esto causaba que la fórmula y la explicación en español formaran una sola línea indivisible de 450px a 700px de ancho. En las tarjetas de opciones de 2 columnas (~260px-320px), el texto desbordaba la tarjeta, solapando la columna contigua y cortándose en el extremo derecho.

### B. Solución Implementada en `platform/src/components/MathText.tsx`
1. **Función auxiliar pura `splitMathAndProse(latex: string)`:**
   - Emplea un algoritmo con balanceo recursivo de llaves para localizar bloques `\text{...}` y `\mbox{...}`.
   - Si el contenido interior `innerContent` contiene espacios en blanco (`/\s/.test(...)`) o tiene longitud mayor a 15 caracteres (prosa):
     - El contenido matemático anterior se limpia de barras invertidas terminales (`replace(/[\\~]+$/, '')`) y se emite como `{ type: 'inline-math', content: cleanedMath }`.
     - El contenido en prosa se emite como `{ type: 'text', content: innerContent }`, preservando espacios limítrofes si existían en la fuente LaTeX.
   - Si el contenido interior no contiene espacios y es corto (p. ej. `\text{plim}`, `\text{max}`, `\text{Var}`), se preserva dentro del bloque matemático para que KaTeX lo renderice en tipografía romana de operador matemático.
2. **Integración en el parser:**
   - En el loop de procesamiento de `inline-math` (`$...$`), el contenido se fragmenta con `splitMathAndProse(rawInlineMath)` antes de agregar las sub-partes a la lista final de renderizado.
3. **Mapeo de elementos DOM:**
   - Cada parte de tipo `text` se renderiza como `<span key={index} className="inline break-words">{part.content}</span>`.
   - Para las partes `inline-math`, se ejecuta `katex.renderToString` con `displayMode: false` y se neutraliza cualquier `\u00a0` residual mediante `html.replace(/\u00a0/g, ' ')`, renderizándose en `<span key={index} className="inline mx-0.5" dangerouslySetInnerHTML={{ __html: html }} />`.

### C. Solución CSS en `platform/src/index.css`
Se reforzaron las reglas CSS de contención en `.qc-root` y `.qc-options`:
```css
.qc-root .katex,
.qc-options .katex {
  max-width: 100%;
  white-space: normal;
}
.qc-root .katex-html,
.qc-options .katex-html {
  white-space: normal;
}
.qc-root .katex .base,
.qc-options .katex .base {
  white-space: normal;
}
.qc-root .katex .mord.text,
.qc-options .katex .mord.text {
  white-space: normal;
  word-break: normal;
  overflow-wrap: break-word;
}
```

### D. Verificación y Resultados de Pruebas
1. **Pruebas de Contrato en `tests/test_m1_zoomfix_contract.py`:**
   - Se incorporó la clase `TestMathTextProseSplittingContract` validando el contrato estático de `MathText.tsx`, las reglas de `index.css` y la ejecución en tiempo real de `splitMathAndProse` vía Node.js para los 4 casos de las capturas y operadores romanos (`\text{plim}`, `\text{Var}`).
   - Ejecución: `.\pytest.cmd -q tests/test_m1_zoomfix_contract.py` -> **97 passed in 0.67s (100% PASS)**.
2. **Compilación de Producción:**
   - Ejecución: `npm run build` en `platform/` -> **Exit code 0** (tsc + vite build en 18.46s).
3. **Suite E2E de Matriz de Viewports:**
   - Ejecución: `node tests/e2e_m1_viewport_matrix.mjs` -> **100% PASS en los 7 viewports** (683×768, 720×900, 800×900, 960×1080, 1366×768, 1440×900, 390×844) verificando que las opciones distribuyen en 4+3 columna-primero, los botones de acción no quedan ocultos y no existe ningún desborde horizontal (`scrollWidth <= clientWidth`).

