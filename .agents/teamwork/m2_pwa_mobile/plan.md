# Plan — Milestone 2: PWA Móvil y Modo Offline

Skill: `flash-triad-orchestrator` · prefijo de subagentes: `m2pwa` · Model=`flash` · Orquestador Dispatch-Only.
Frontera global de escritura: `platform/{package.json,package-lock.json,vite.config.ts,index.html}`, `platform/public/**`, `platform/src/{main.tsx,pwa/**,index.css,vite-env.d.ts}`, `platform/scripts/**`, `tests/test_m2_pwa_contract.py`, `tests/e2e_m2_pwa_offline.mjs`, `FUTURE_MILESTONES.md` (solo §7 M2 + fila matriz línea 201).
Ningún stream toca `QuestionCard/Sidebar/PracticeSession/...` (territorio M1).

## 1. Diagnóstico (a verificar en Pre-Flight)

| # | Hallazgo | Archivo |
|---|----------|---------|
| D1 | No existe `platform/public/`, ni manifest, ni service worker, ni iconos. | `platform/` |
| D2 | `index.html` sin `viewport-fit=cover`, `theme-color`, ni metatags iOS (`apple-mobile-web-app-*`, `apple-touch-icon`). | `index.html` |
| D3 | `base: process.env.VITE_BASE_PATH \|\| './'` (soporta GitHub Pages en subruta) → `scope`, `start_url` y registro del SW deben ser **relativos**. | `vite.config.ts` |
| D4 | `courseApiPlugin` sirve `/api/courses` en dev/preview y emite JSON estáticos en build (`generateBundle`) + copia `404.html` en `closeBundle`. Los cursos pesan hasta ~14 MB → **no** precachear; usar runtime caching. | `vite.config.ts` |
| D5 | KaTeX CSS referencia fuentes `.woff2` (hash de Vite); deben entrar al precache (`globPatterns` con `woff2`). | `index.css` / `main.tsx` |
| D6 | Footer `fixed` y barras inferiores no consideran `env(safe-area-inset-bottom)` (notch/home indicator iOS). | `index.css` |
| D7 | `package.json` sin `vite-plugin-pwa` ni `workbox-window`. | `package.json` |

## 2. Criterios de aceptación (medibles)

- **AC-1** `vite-plugin-pwa` instalado (devDependency), `registerType: 'autoUpdate'`, SW generado en `npm run build` (`dist/sw.js`, `dist/manifest.webmanifest`).
- **AC-2** Manifest: `name`, `short_name`, `display: standalone`, `orientation: any`, `theme_color` `#1865f2`, `background_color`, `start_url: './'`, `scope: './'`, `lang: es`, iconos `192x192`, `512x512` (`purpose: any`) y `512x512` `purpose: maskable` (safe zone 80%).
- **AC-3** `index.html`: `viewport` con `viewport-fit=cover`; `theme-color`; `apple-mobile-web-app-capable`, `apple-mobile-web-app-status-bar-style=black-translucent`, `apple-mobile-web-app-title`; `<link rel="apple-touch-icon" href="apple-touch-icon.png">` (180×180). Sin romper `<title>`/og tags existentes.
- **AC-4** Safe areas: utilidades CSS `.pb-safe`, `.pt-safe`, `.px-safe` con `env(safe-area-inset-*)` y fallback; `--safe-bottom` en `:root`. Se publican en `index.css` (consumo en componentes queda como nota para M1/siguiente, **no** se editan componentes).
- **AC-5** Precache: bundles JS/CSS/HTML + **todas** las fuentes KaTeX (`woff2`; excluir `woff`/`ttf` redundantes) + iconos. `navigateFallback: 'index.html'` (compatible subruta).
- **AC-6** Runtime cache de cursos: `/api/courses*` y `courses/*.json` con `NetworkFirst` (timeout 3 s, `maxEntries: 20`, `maxAgeSeconds` 30 d); respuestas `0,200` cacheables.
- **AC-7** Offline: tras primera visita online, con red cortada la app carga la biblioteca y abre un curso previamente visitado y KaTeX renderiza (fuentes no caen a fallback).
- **AC-8** Registro del SW con prompt mínimo no intrusivo: `registerSW({ immediate: true })`; `devOptions.enabled: false` (no interferir con `vite dev`); indicador discreto "Offline" opcional (`pwa/OfflineBadge`) solo si cabe sin tocar componentes M1 (montado desde `main.tsx`).
- **AC-9** Cero regresión: `npm run build` (tsc + vite) verde; `courseApiPlugin` y `closeBundle` intactos; `data-testid` intactos; suite `pytest` sin nuevos fallos.
- **AC-10** Lighthouse PWA / instalabilidad: Chromium reporta manifest instalable (`installability errors = []`) vía Playwright CDP `Page.getInstallabilityErrors`.

## 3. Contrato compartido entre streams

- Rutas de iconos (producidas por 1A, referenciadas por 1B): `platform/public/icons/{icon-192.png,icon-512.png,icon-maskable-512.png}` y `platform/public/apple-touch-icon.png` (todas relativas, sin `/` inicial).
- Nombre de manifest: `manifest.webmanifest` (generado por el plugin; `index.html` NO debe duplicar un `<link rel="manifest">` — lo inyecta el plugin).
- Nombre de utilidades CSS: `.pt-safe`, `.pb-safe`, `.px-safe`.
- `registerSW` vive en `platform/src/pwa/register.ts`; `main.tsx` solo hace `import './pwa/register'`.

## 4. Gates y Streams (fronteras 100% disjuntas)

### GATE 0 — Pre-Flight (lectura; cada Implementador escribe `BRIEFING.md`)
Registra baseline: `npm run build` OK, conteo `pytest -q`, estado de `git status`, versión de Node/npm, confirmar si el entorno permite `npm install` (BLOCKER Tier B si no hay red).

### GATE 1 — Implementación (3 streams en paralelo)

| Stream | Escribe SOLO | Entrega |
|--------|--------------|---------|
| **1A** Assets e iconos | `platform/public/**`, `platform/scripts/make_icons.mjs` | Icono fuente SVG (capa/estrella azul `#1865f2`, coherente con favicon actual) y script determinista que rasteriza a PNG 192/512/maskable/180 (usar `sharp` vía `npx -y -p sharp`, sin añadirlo a `package.json`). PNGs commiteados. |
| **1B** Plugin PWA + config | `platform/package.json`, `platform/package-lock.json`, `platform/vite.config.ts` | `npm i -D vite-plugin-pwa workbox-window`; `VitePWA({...})` con manifest (AC-2), workbox (AC-5/6), `devOptions.enabled=false`; **no** modificar `courseApiPlugin`; el plugin se agrega a `plugins: [react(), courseApiPlugin(), VitePWA(...)]`; verificar que `closeBundle` 404.html sigue funcionando; `base` respetado. |
| **1C** HTML, safe areas y registro | `platform/index.html`, `platform/src/index.css` (solo bloque nuevo al final marcado `/* M2-PWA */`), `platform/src/main.tsx`, `platform/src/pwa/**`, `platform/src/vite-env.d.ts` | Metatags (AC-3), utilidades safe-area (AC-4), `register.ts` con `virtual:pwa-register` (AC-8), tipos `vite-plugin-pwa/client`. Coordinar `index.css` con M1 (append-only, sin tocar reglas existentes). |

Dependencias: 1B necesita los PNG de 1A solo para el build final → 1B puede usar rutas del contrato y el Auditor verifica tras unir. 1C depende de 1B solo para tipos virtuales (`vite-plugin-pwa/client`); si 1B no terminó, declarar `/// <reference>` y verificar en Gate 2.

Cada stream corre Tríada: **Implementador → Mejorador → Auditor** (`m2pwa_auditor` escribe solo en `.agents/teamwork/m2_pwa_mobile/stream_XX_audit/`).

### GATE 2 — Integración y pruebas (tras PASS de Gate 1; 3 streams disjuntos)

| Stream | Escribe SOLO | Entrega |
|--------|--------------|---------|
| **2A** Contract tests | `tests/test_m2_pwa_contract.py` | Pytest estático: manifest tiene iconos 192/512/maskable y existen en disco (dimensiones PNG leídas del header), `viewport-fit=cover`, `apple-touch-icon`, `woff2` en `globPatterns`, `NetworkFirst` para cursos, `devOptions.enabled` falso, `courseApiPlugin` intacto, ausencia de `<link rel="manifest">` duplicado, rutas relativas. Adversarios: comentarios que simulen configuración, base path con subruta. |
| **2B** E2E offline | `tests/e2e_m2_pwa_offline.mjs` | Playwright (`npx -y -p playwright@1.63.0`, Chromium ya instalado, sin `playwright install`; fallback `SKIPPED`): `npm run build` + `vite preview`; visita online → espera `navigator.serviceWorker.ready` → `context.setOffline(true)` → reload → verifica biblioteca, abre un curso, un `.katex` renderizado y fuentes `woff2` servidas desde SW; `getInstallabilityErrors` vacío; emulación iPhone 390×844. |
| **2C** Docs | `FUTURE_MILESTONES.md` (solo §7 M2 y fila línea 201) | Reescribir spec M2 con estado, estrategia de caché (precache vs runtime), safe areas, limitaciones iOS (A2HS manual, sin `beforeinstallprompt`, cuota de caché), cómo instalar. Preservar resto del documento. |

## 5. Protocolo BLOCKER

- **Tier A** (resolver Orquestador): conflicto de append en `index.css` con M1, versión de plugin incompatible con Vite 6, ajuste de globs.
- **Tier B** (escalar al usuario): sin red para `npm install`; HTTPS/hosting de destino desconocido (SW requiere HTTPS o localhost); decidir si precachear cursos completos (>14 MB) en vez de runtime.

## 6. Estimación de tiempo

| Fase | Duración (wall-clock) |
|------|----------------------|
| Gate 0 Pre-Flight | 5–8 min |
| Gate 1 (3 streams paralelos × tríada) | 25–40 min |
| Gate 2 (3 streams paralelos × tríada, incl. build + E2E Chromium) | 25–40 min |
| Remediación REJECT / integración final | 10–20 min |
| **Total** | **~1 h 15 min – 1 h 50 min** (consistente con el 1–2 h del spec) |

Riesgos que alargan: Playwright E2E offline (SW + timing), compatibilidad `vite-plugin-pwa` ↔ `base: './'`, y colisión de `index.css` si M1 aún se ejecuta (mitigar: correr M2 después de M1 o append-only).

## 7. Definition of Done

AC-1…AC-10 verdes, `PASS::` de los 6 Auditores, `npm run build` y `pytest` sin regresión, `GATE_STATUS.md` cerrado.
