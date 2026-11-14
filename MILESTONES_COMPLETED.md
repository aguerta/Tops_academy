# Registro de Milestones Completados y Certificados: Tops Academy

> **Propósito:** Archivo histórico y bitácora forense de los milestones **cerrados y certificados**.  
> **Hoja de Ruta Activa:** Lo pendiente, en curso o en backlog vive en [`FUTURE_MILESTONES.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/FUTURE_MILESTONES.md) *(espejo en `docs/future_milestones/FUTURE_MILESTONES.md`)*.  
> **Conocimiento Tribal y Arquitectura:** La explicación causal de por qué los sistemas funcionan así vive en [`CONOCIMIENTO_TRIBAL.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/CONOCIMIENTO_TRIBAL.md).  
> **Convención de Certificación:** Cada entrada declara *quién* certificó y *cómo*. «Certificado por el usuario» = prueba manual en sus equipos. «Verificado automáticamente» = tests unitarios, contratos o suites E2E con nombre y resultado.  
> **Última Actualización:** 2026-11-14 (Branch: `main` / `optimizaciones_test` — Pipeline C2C v4.0 "Más con Menos", DSL Form-C y KaTeXAST, Shift-Left 4 Arquetipos, FSM Hook Guard y M1, 1-T, 2, 2a, 3, 4, 6, 7, 9 [Quick Wins], 10, 11 [núcleo], 12, 13, 14, 15 [F1], 16 [F1] cerrados).

---

## Índice de Milestones Cerrados

| Milestone | Alcance cerrado | Certificación | Commits |
| :--- | :--- | :--- | :--- |
| **1** Ergonomía Web (Zoom-Fix, Split 50%, Remediación v3) | Laptops 14" a 150%, TUF F15 a 125%, split 50%, tablets; biblioteca de 3 columnas; prosa en fórmulas | Usuario (2026-10-26) + matriz de 7 viewports + 97 contratos | `05c8f4b`, `12042d0`, `950bd20` |
| **1-T** Deuda de Pruebas de Ergonomía E2E (Matriz 12 Viewports y AC-CORE) | Matriz ampliada a 12 viewports (incluyendo 1280×590, 610×590, 1536×740, 768×1024, 1024×768); doble validación AC-CORE bajo `Blank-First: ON` y `OFF`; distribución 4+3 y vertical 7; sin desborde horizontal | Automática (`tests/e2e_m1_viewport_matrix.mjs` [12/12 PASS]) | `main` |
| **2a** Usabilidad móvil | Teléfono: columna única, drawer, footer en flujo | Usuario (2026-10-26) + viewport 390 × 844 en la matriz | los de M1 |
| **2** PWA Instalable y Modo Offline | Service Worker Workbox, precaching App Shell + fuentes KaTeX, Web App Manifest, suite de iconos (192, 512, maskable), badge `✓ Offline`, navegación nativa popstate (`navigationHistory.ts`), instalación guiada | Automática (`tests/test_pwa_offline.py`, `tests/test_pwa_navigation_and_install.py`) + Verificado en producción PWA (2026-11-01) | `23cb4ec`, `e26769b`, `7e6a238`, `9296f9c` |
| **3** Anti-Overfitting y Variedad de Plantillas (v3.8 Tri-Banda) | Contrato Tri-Banda (`--min-archetypes 3`, 3 bandas ZPD, $\ge 2$ Bloom, cuota FIB/MS, `[STEM-DIVERSITY-GATE]`) + `ArchetypeEntropyLinter` (`MIN_ARCHETYPES = 3` + `ratio > 0.85` + MPRI) | Automática (`test_new_audit_linters.py`, 11 cursos publicados con 0 infracciones) | `5b5395c`, `be43b08`, `b07cec8` + cierre 2026-10-31 |
| **4** DSL Form-C, Desacoplamiento KaTeX, Pydantic y Gramática KaTeXAST (100%) | Contrato Pydantic `ShardCompetenceContract` y `ArchetypeKind`, validación inductiva `KaTeXAST` + `pykatex_validate_with_column`, canonicalizador algebraico `canonicalize_algebraic_katex` + `sympy_to_katex` en `engine/katex_ast.py`, DSL `Form-C` en 55–70 líneas con auto-exportación AST de `vars` en `compile_shard.py`, PrairieLearn `@var@` en raw strings, precheck `[SYMPY-LATEX-MATRIX]` y migración EDO/EDP | Automática (`tests/test_milestone4_formc_katex_ast.py` [23/23 PASS], `tests/test_c2c_v321_comp4_prompts.py`, `tests/test_sweetspot_v35_cta_and_shards.py`) + migración de plantillas EDO/EDP | `315690c`, `cee3e5d`, `884c305`, `cb84a16`, `6208088` |
| **6** Antigravity Study Harness 2.0 (Blank-First, Navegación Mouseless y Transferencia Socrática $0 API) | Cortina Blank-First pura (oculta opciones para Free Recall, tecla `Enter`), navegación 100% mouseless con hotkeys `A`–`G` / `1`–`7` (toggle-deselección y auto-foco en fill-in-the-blank), persistencia `sessionStorage` (`tops_blank_first_enabled`), toggle de cabecera, compuerta socrática adaptativa (3er fallo con hints / 2do sin hints), tope ampliado a 4 intentos (`4/4`) y generador de prompt anti-giveaway en 1-clic | Automática (`tests/test_m6_study_harness_contract.py` [3/3 PASS], `tests/test_m1_zoomfix_contract.py` [97/97 PASS], build Vite limpio) | `main` |
| **7** Pipeline "Más con Menos" (Target `< 12 min` y `-65%` Tokens) | Deduplicación masiva `-2.0M` tokens en `dispatch.py` (eliminación de triple envío Prompt/work_order/items), recibos criptográficos SHA-256 (`shard_XX.cert.json`) en compilador $< 5\text{ ms}$, subagentes `--lean` por defecto con prompts $\le 5\text{ KB}$, weighted waves de hasta 100 shards concurrentes, precheck estático AST $< 50\text{ ms}$ (`shard_precheck.py`), y suite global de 1,404 tests en 27.76s | Automática (1,404 tests pasando al 100% en 27.76s en `pytest tests/ -q`) + 3 auditorías forenses | `e357df5`, `cb84a16`, `6208088`, `75bfde1`, `c81aaa6` |
| **9 (Quick Wins)** Jerarquía PPT, Unidad 0 `PRE-XX`, `ContentCoreDrawer` y Backfill | Propagación `evidence`/`assumptions`/`session` en `run.py`, soporte `PRE-XX` en schemas/`compile_cta.py`/`cta_merge.py`, `hierarchyAdapter.ts`, visor `ContentCoreDrawer.tsx` (5 bloques Khanmigo + Glosario), badges en `CourseOverview`/`MasteryGrid`/`Sidebar`, fix ETag en `courseLoader.ts` y backfill determinista de 8 cursos (237 competencias) | Automática (`tests/pipeline/test_m9_cta_modules.py`, `tests/platform/test_m9_hierarchy.py`, `tests/platform/` [238 PASS], pipeline/engine [256 PASS], build Vite limpio) + Verificación visual por usuario (`http://localhost:5173`) | `1bc0b4c` |
| **10** QA Rubric v2.0 Deep Mastery | 7 linters Path-to-Mastery v2.0, MPRI (/100 pts en 6 pilares, cuota $\ge 25\%$ multimodal), penalizaciones duras, compuerta bloqueante pre-publish `PublishQualityGateError` con mapeo AST | Automática (`tests/test_new_audit_linters.py`) + Auditoría en pipeline sobre 11 cursos | `be43b08`, `24c44f8`, `0e2fd38`, `b07cec8` |
| **11** Carga de cursos — núcleo | Manifest slim, índice con caché, ETag/304/gzip, manifest inline, IndexedDB, prefetch | Automática (12 tests de API + build); ACs de cliente sin medir | `41435c5`, `b73a5ee`, `2051b8b`, `97fa2f3` |
| **12** Resiliencia ante Suspensión de la Laptop (SessionStorage & ETag) | Persistencia continua en `sessionStore.ts` (`tops_active_session_v1`), rehidratación reactiva en `PracticeSession.tsx` y `App.tsx`, reconciliación silenciosa `ETag` en `visibilitychange`, endpoint `GET /healthz` en `courseServer.cjs`, script `npm run study` | Automática (`tests/platform/test_m12_session_resilience.py` [14/14 PASS], `platform/dist/` rebuilt) | `main` |
| **13** Consolidación del Repositorio, Higiene de Artefactos y 4 Dominios de Tests | 4 dominios aislados (`tests/{quality,engine,platform,pipeline}/` + `tests/helpers/`), política Clean Artifacts, `.gitignore` endurecido, purga de 76 volcados JSON huérfanos y 8 scratch scripts; 1,526 tests pasando al 100% en ~51s | Automática (1,526 tests en `tests/{quality,engine,platform,pipeline}/` pasando en ~51s) | `main` |
| **14** Motor de Maestría Integral 2.0 Estilo Khan Academy | Calibración bidireccional en Challenge/Test/Quiz, degradación por fallo, barra híbrida 80/20, Hint-Cap, Red Dot, fluidez de tiempos y motor 'Up Next for You' (5 niveles) | Automática (`tests/platform/test_mastery_calibration_bidirectional.py` [3/3 PASS], `tests/platform/test_mastery_progress_80_20.py` [5/5 PASS]) | `main` |
| **15** Gobernanza Formal y FSM Multi-Agente (Fase 1 Isomórfica) | Matriz 2D `decidirEstrategiaEdicion` en `c2c_hook_guard.py` (bloqueo estricto de reescrituras globales si errores $< 6$, imposición de edición quirúrgica y modular splicing), tope duro síncrono (40 turnos / 5M tokens por subagente), y aislamiento AST en subprocesos | Automática (`tests/test_hook_post_pass_and_write_isolation.py`, `tests/test_watchdog_and_hooks.py`) | `e357df5`, `75bfde1`, `c81aaa6` |
| **16** Certificación Matemática Shift-Left y 4 Arquetipos (Fase 1 Motor) | Stage Contract v4.0 (`engine/stage_contract.py`, `engine/invariants.py`), 4 arquetipos obligatorios en `compile_shard.py` (`direct`, `inverse`, `perturbation`, `boundary_or_edge_case`), supuestos explícitos obligatorios en `cta.json` (`assumptions` + `violation_consequence`), fix silencioso de `np.bool_` en sandbox AST, linters anti-gaming (`[DIAG-MAGIC-MULT]`) | Automática (`tests/test_validator.py`, `tests/test_m3_archetypes_semantic_gate.py`, `tests/test_c2c_author_speedups.py`) | `954a6c8`, `cee3e5d`, `9310ff7`, `75bfde1` |

---

## Milestone 1: Web Ergonomía para Laptops, Tablets y Split View 50% (Zoom-Fix + Remediación v3)
* **Estado:** ✅ **Completado y certificado por el usuario (2026-10-26)** en laptop de 14" a 150% de escala (referencia más exigente) y en ASUS TUF Gaming F15 de 15.6" a 125% (referencia que no debe regresar). Verificación automatizada: matriz E2E de 7 viewports, 97 contratos estáticos (`tests/test_m1_zoomfix_contract.py`), tests de teclado/calificación (39,588 casos) y auditoría visual de 200 preguntas aleatorias (50 por curso).
* **Objetivo Crítico:** Resolver integralmente la adaptabilidad y ergonomía cognitiva tanto en laptops compactas (13"-14", 1366×768 o 1440×900) como en escenarios de **Split View al 50% de ancho** (pantalla dividida con visor de PDF, notas o asistente socrático), donde las 7 opciones (MC7) previamente provocaban desborde vertical forzando zoom out continuo.
* **Componentes Técnicos Implementados:**
  1. Grid Inteligente de 2 Columnas con Container Queries (`@container qc (min-width: 480px)` en `QuestionCard.tsx`, `index.css`).
  2. Sidebar Drawer Off-Canvas y App Shell Accesible (`Sidebar.tsx`, `App.tsx`) con botón flotante accesible en `< 1024px`.
  3. Bottom Sheet Toast y SVG Responsivo (`FeedbackToast.tsx`, `CoordinatePlane.tsx`) con límite vertical elástico `max-h-[45dvh]`.
  4. Practice Session Shell Ergonómico (`PracticeSession.tsx`): flex `h-dvh`, footer en flujo, recuperación de 80 px verticales y `resetScroll()` automático entre preguntas.
  5. Prosa fuera de KaTeX (`splitMathAndProse` en `MathText.tsx`) para permitir envoltura de texto sin romper `white-space: nowrap`.
* **Commits:** `05c8f4b`, `12042d0`, `950bd20`.

---

## Milestone 2a: Usabilidad Móvil
* **Estado:** ✅ **Completado y certificado por el usuario (2026-10-26):** «ahora sí funciona el celular… ya no se tiene que pelear con la plataforma para hacer las preguntas».
* **Entregado:** Columna única bajo 480 px, sidebar drawer bajo 1024 px, indicador textual `n of N` en footer, toast como bottom sheet y cero desborde horizontal. Viewport 390 × 844 verificado en la matriz E2E.
* **Commits:** Los mismos de M1.

---

## Milestone 2: PWA Instalable y Modo Offline
* **Estado:** ✅ **Completado y Verificado (2026-11-01).**
* **Objetivo:** Experiencia nativa instalable (`standalone`) en smartphones Android, iOS y escritorio sin red, con sincronización de historial del navegador para gestos de retroceso nativos.
* **Componentes Técnicos Entregados:**
  1. Service Worker Workbox con precaching de App Shell y fuentes KaTeX (`.woff2` ≈ 1.5 MB). Delegación de cursos masivos a IndexedDB (`tops_academy_cache`).
  2. Web App Manifest e iconos adaptativos (192, 512, maskable) con Safe Areas y badge visual `✓ Offline`.
  3. Gestión de Navegación Nativa y Popstate (`navigationHistory.ts`): soporte de retroceso gestual en Android/iOS, modal de confirmación antes de abandonar sesiones de práctica y doble atrás de protección en biblioteca.
  4. Instalación guiada con captura de evento `beforeinstallprompt`.
* **Pruebas:** `tests/test_pwa_offline.py` (12/12 PASS), `tests/test_pwa_navigation_and_install.py` (PASS).
* **Commits:** `23cb4ec`, `e26769b`, `7e6a238`, `9296f9c`.

---

## Milestone 3: Anti-Overfitting y Variedad de Plantillas por Competencia (v3.8 Tri-Banda)
* **Estado:** ✅ **Completado al 100% en Pipeline y Auditoría QA (2026-10-31).**
* **Objetivo:** Erradicar el sobreajuste sintáctico (*overfitting* a un único molde donde solo rotan números) exigiendo polimorfismo estructural real, progresión adaptativa ZPD y modalidades de evocación activa.
* **Componentes Técnicos Entregados:**
  1. Compuerta de Compilación `[M3-ARCHETYPES]` (`compile_shard.py`): mínimo 3 arquetipos ortogonales (`--min-archetypes 3`), $\ge 2$ niveles Bloom, cuota multimodal activa ($\ge 2$ plantillas `FIB` o `MS`), anti-clonación AST y comisiones `[STEM-DIVERSITY-GATE]`.
  2. Auditoría Determinista en QA Engine (`standardized_audit_engine.py`): `ArchetypeEntropyLinter` integrado con Pilar 2 del MPRI, penalizando concentración excesiva en un solo molde.
* **Pruebas:** `tests/test_new_audit_linters.py`, validación sobre 11 cursos en `courses/*.json` (0 infracciones).
* **Commits:** `5b5395c`, `be43b08`, `b07cec8`.

---

## Milestone 10: Rúbrica QA v2.0 (Certificación Deep Mastery)
* **Estado:** ✅ **Completado al 100% y Activo en Producción (2026-10-31).**
* **Objetivo:** Certificación integral del rigor pedagógico, psicométrico y técnico bajo estándares de Quality Matters (QM), OSCQR y Mastery Learning con compuertas de bloqueo deterministas.
* **Componentes Técnicos Entregados:**
  1. Suite de 7 Linters Path-to-Mastery v2.0 en `standardized_audit_engine.py`.
  2. Índice MPRI (0 a 100 pts en 6 pilares) con exigencia de $\ge 25\%$ de generación activa / discriminación (`FIB + MS`).
  3. Penalizaciones duras deterministas (`hard_penalties`).
  4. Compuerta Bloqueante Pre-Publish (`PublishQualityGateError` en `course_publisher.py`) con reporte de errores y números de línea AST.
* **Pruebas:** `tests/test_new_audit_linters.py` (100% PASS), 11 cursos certificados.
* **Commits:** `be43b08`, `24c44f8`, `0e2fd38`, `b07cec8`.

---

## Milestone 11: Carga Rápida de Cursos — Núcleo (Manifest Slim, Caché, ETag y Prefetch)
* **Estado:** ✅ **Núcleo completado (2026-10-26)**. Lo pendiente (percepción de carga en equipos lentos) pasó al Milestone 11b.
* **Entregado y Medido:**
  - Manifest slim (`platform/server/courseIndex.cjs`): de 59.8 MB a 2.52 KB (gzip 0.76 KB).
  - Índice persistente por `mtime + size` en `.cache/course_index.json`.
  - Entrega por ID con `ETag`, `304 Not Modified` y gzip.
  - Manifest inline en HTML para pintar la biblioteca sin esperar a la red.
  - Cliente con IndexedDB (`tops_academy_cache`) y prefetch idle en segundo plano.
* **Pruebas:** `tests/test_course_api_manifest.py` (12/12 PASS).
* **Commits:** `41435c5`, `b73a5ee`, `2051b8b`, `97fa2f3`.

---

## Milestone 4: DSL Form-C, Desacoplamiento KaTeX, Pydantic y Gramática KaTeXAST (100% Cerrado)
* **Estado:** ✅ **Completado y verificado automáticamente al 100% (2026-11-08)**.
* **Objetivo:** Erradicar definitivamente la colisión de caracteres de control LaTeX (`\t`, `\b`), desacoplar la renderización KaTeX del runtime de Python, imponer contratos formales de tipado Pydantic con validación inductiva del árbol AST matemático, y condensar el código de los autores a plantillas de 55–70 líneas (`-65%` de tokens de salida).
* **Componentes Técnicos Entregados:**
  1. **Contrato de Autoría Tipado Pydantic (`engine/katex_ast.py`):** Modelos `ShardCompetenceContract` y `ArchetypeKind` con retrocompatibilidad dual y validación estricta de 4 arquetipos y supuestos evaluados.
  2. **Árbol Inductivo `KaTeXAST` y QuickJS (`pykatex`):** `KaTeXAST.is_valid` con invariantes inductivos (§7.2 `TopsAcademyC2C.lean`) que prohíben por construcción prosa $> 45$ chars o guiones bajos crudos dentro de `\text{...}`, saltos `\\` fuera de entornos matriciales y llaves dobles `{{...}}`. Validador `pykatex_validate_with_column` con reporte de columna exacta a $> 15,000$ fórmulas/s.
  3. **Canonicalizador Algebraico KaTeX y SymPy Bridge:** `canonicalize_algebraic_katex` en `engine/katex_ast.py` que colapsa coeficientes unitarios y dobles signos (`1 x` $\to$ `x`, `+ -` $\to$ `-`), y puente `sympy_to_katex` para generación simbólica garantizada.
  4. **Precheck Estático `[SYMPY-LATEX-MATRIX]`:** Integrado en `shard_precheck.py` para bloquear en $< 50\text{ ms}$ matrices o polinomios ensamblados manualmente en Python.
  5. **DSL Composicional `Form-C` y Auto-Exportación AST de `vars`:** Molde compartido de opción (`fmt`), catálogo unificado `RATS`, función canonical `_pv(c)` y auto-exportación de variables AST en `compile_shard.py` vía `inject_ast_auto_vars`.
  6. **Desacoplamiento KaTeX con PrairieLearn `@var@`:** Soporte integral en `engine/assemble.py`, `engine/invariants.py` y `check_templates.py`, eliminando escaping parasitario y llaves dobles.
  7. **Tooling Formal:** Inclusión de `pykatex>=0.0.8` y `z3-solver>=4.13.0` en `pyproject.toml`.
  8. **Salvaguardas R-23 Zero-Copy y Migración de Referencia:** Escáner léxico $O(1)$ zero-copy en `src/validator/lexical_scanner.py` y cursos base `examples/edo/` y `examples/edp/` al 100%.
* **Pruebas:** `tests/test_milestone4_formc_katex_ast.py` (23/23 PASS), `tests/test_c2c_v321_comp4_prompts.py`, `tests/test_sweetspot_v35_cta_and_shards.py`, `tests/test_pykatex_warn.py`.
* **Commits:** `315690c`, `cee3e5d`, `884c305`, `cb84a16`, `6208088`.

---

## Milestone 6: "Antigravity Study Harness 2.0" (Modo Blank-First y Transferencia Khanmigo $0 API)
* **Estado:** ✅ **Completado y verificado automáticamente (2026-11-08).**
* **Objetivo:** Convertir la plataforma en una estación de ultra-aprendizaje en split-view (1/3 y 1/2 de pantalla horizontal) erradicando la trampa del reconocimiento asistido y conectando la tutoría socrática externa con Gemini Pro a $0 costo marginal de API sin riesgo de regresión en los 97 contratos de ergonomía de la plataforma.
* **Componentes Técnicos Entregados:**
  1. **Cortina *Blank-First* en `QuestionCard.tsx` y `PracticeSession.tsx`:** Oculta las alternativas de respuesta al iniciar cada pregunta para forzar la evocación activa (*Free Recall*) en memoria o papel físico, manteniendo siempre visibles el enunciado KaTeX y los gráficos SVG.
  2. **Control por Teclado Unificado (`Enter`):** La tecla `Enter` y el botón central `[ 💡 Ya tengo mi planteamiento ]` (`data-testid="lift-curtain-btn"`) repliegan suavemente la cortina y revelan las opciones. El botón primario inferior derecho (`data-testid="check-btn"`) refleja reactivamente el estado "Reveal options ↵ Enter".
  3. **Selector Accesible en Cabecera (`toggle-blank-first-btn`):** Permite alternar la modalidad `[🧠 Blank-First: ON/OFF]` con persistencia reactiva en `sessionStorage` (`tops_blank_first_enabled`).
  4. **Compuerta Socrática Adaptativa y Transferencia Khanmigo ($0 API):** Botón `[ 🤖 Copiar Prompt Socrático ]` (`data-testid="copy-socratic-prompt-btn"`) activado bajo compuerta adaptativa: se desbloquea al **tercer fallo** si la pregunta tiene pistas, o al **segundo fallo** si no tiene pistas, extendiendo el tope a 4 intentos (`Maximum attempts reached (4/4)`) para permitir consulta con IA externa sin revelar la respuesta prematuramente. Banner con texto directo: *"Haz click en el botón y Copia y pega el text en tu IA favorita para ayuda especializada para que te ayude."*
  5. **Navegación 100% Mouseless y Hotkeys Ergonómicos:** Teclas `A`–`G` y `1`–`7` para marcar alternativas; pulsar la misma tecla deselecciona la opción en opción única (MC7) o conmuta su estado en opción múltiple. Autofoco inmediato en campo de texto de `fill_in_the_blank` sin requerir clic de ratón.
  6. **Generador Riguroso Anti-Giveaway (`platform/src/utils/socraticPrompt.ts`):** Empaqueta el enunciado KaTeX, la opción elegida, el diagnóstico del error y la restricción socrática estricta de formular exactamente una pregunta conceptual de primer principio sin regalar la respuesta ni la letra.
* **Pruebas:** `tests/test_m6_study_harness_contract.py` (3/3 PASS), `tests/test_m1_zoomfix_contract.py` (97/97 PASS), compilación limpia en `npm run build` (tsc + vite + pwa).
* **Commits:** `main`.

---

## Milestone 7: Pipeline "Más con Menos" — Deduplicación, Recibos SHA-256, Prompts `--lean` y Suite `< 30 s`
* **Estado:** ✅ **Completado y verificado automáticamente al 100% (2026-11-08)**.
* **Objetivo:** Lograr máxima calidad formal (4 arquetipos + supuestos) con el menor consumo de tokens (`-65%`) y latencia reducida (`< 12 min` en corridas completas), erradicando envíos parasitarios y cómputos redundantes.
* **Componentes Técnicos Entregados:**
  1. **Deduplicación Masiva en `dispatch.py` (`-2.0M` tokens):** Se eliminó el triple envío redundante de `"Prompt"`, `"work_order"` e `"items"` en la inicialización de subagentes.
  2. **Recibos Criptográficos SHA-256 (`< 5 ms`):** `run.py` y compiladores emiten y validan `shard_XX.cert.json` para evitar re-compilaciones de shards inalterados.
  3. **Prompts `--lean` Ultra-Compactos:** Todos los subagentes operan con system prompts optimizados $\le 5\text{ KB}$ en `system_prompts/lean/`.
  4. **Weighted Waves (1 Hab/shard, olas $\le 100$):** `dispatch.py` y `plan_shards.py` soportan hasta 100 shards concurrentes en una única ola de despacho paralelo.
  5. **Precheck Estático AST (`shard_precheck.py`):** Detección en $< 50\text{ ms}$ de infracciones de perturbación ad-hoc (`while`), firmas de verificador (`ver_*`), bucles y strings de control antes de invocar subprocesos pesados.
  6. **Suite de Pruebas Ultra-Rápida:** 1,404 pruebas ejecutadas en **27.76 segundos** con `pytest-xdist` dinámico (`worksteal`).
* **Pruebas:** 1,404 tests pasando al 100% (`pytest tests/ -q`), `tests/test_bootstrap_and_wave_streaming.py`, `tests/test_c2c_author_speedups.py`.
* **Commits:** `e357df5`, `cb84a16`, `6208088`, `75bfde1`, `c81aaa6`.

---

## Milestone 15: Gobernanza Formal y Certificación FSM del Pipeline C2C (Fase 1 Isomórfica)
* **Estado:** ✅ **Fase 1 Isomórfica en Python completada y verificada (2026-11-08)**. La compilación de `TopsAcademyC2C.lean` a binario C nativo mediante Lean 4 Perceus C (Fase 2) permanece en el roadmap activo ([`FUTURE_MILESTONES.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/FUTURE_MILESTONES.md) y [`docs/specs/m15_m18_formal_lean4.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/m15_m18_formal_lean4.md)).
* **Objetivo:** Imponer guardrails deterministas inquebrantables que impidan bucles infinitos, ediciones parasitarias, alucinaciones de herramientas y reescrituras no modulares de código en subagentes autónomos.
* **Componentes Técnicos Entregados:**
  1. **Matriz 2D `decidirEstrategiaEdicion`:** Integrada en `c2c_hook_guard.py` (Líneas infractoras $\times$ Tipo de error). Si los fallos son $< 6$, prohíbe reescrituras completas de archivos y fuerza edición quirúrgica o modular splicing.
  2. **Tope Duro Síncrono:** Límite estricto de 40 turnos o 5,000,000 tokens por sesión de subagente para blindar el presupuesto.
  3. **Aislamiento AST Anti-Bombas de Debug:** Intercepción en `sandbox.py` de scripts no autorizados, artefactos temporales en `scratch/` o llamadas con `python -c`.
  4. **Flexibilización Quirúrgica para Autores:** Exención controlada en `c2c_hook_guard.py` permitiendo reescritura en los primeros 2 fallos de compilación antes de exigir modular splicing.
* **Pruebas:** `tests/test_hook_post_pass_and_write_isolation.py`, `tests/test_watchdog_and_hooks.py`, `tests/test_orchestration_resilience.py`.
* **Commits:** `e357df5`, `cb84a16`, `75bfde1`.

---

## Milestone 16: Certificación Matemática Shift-Left y 4 Arquetipos + Supuestos Explícitos (Fase 1)
* **Estado:** ✅ **Fase 1 (Motor y Contratos Python) completada y verificada (2026-11-08)**. La deducción algebraica automática con Z3/Lean 4 (Fase 2) permanece en el roadmap activo ([`FUTURE_MILESTONES.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/FUTURE_MILESTONES.md) y [`docs/specs/m15_m18_formal_lean4.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/m15_m18_formal_lean4.md)).
* **Objetivo:** Desplazar la detección de errores matemáticos y psicométricos hacia la etapa de diseño de plantillas (Stage 3), erradicando los Late-Catches en Stage 6 y garantizando variedad estructural profunda anti-overfitting.
* **Componentes Técnicos Entregados:**
  1. **Stage Contract v4.0:** Tipado canónico e invariantes en `engine/stage_contract.py` e `invariants.py`.
  2. **Estándar Inviolable de 4 Arquetipos:** `compile_shard.py` impone 4 arquetipos obligatorios (`direct`, `inverse`, `perturbation`, `boundary_or_edge_case`) con 4/4 fórmulas AST disjuntas y bandas ZPD (`easy`, `medium`, `hard`, `hard/expert`).
  3. **Supuestos Explícitos en el Currículo:** `compile_cta.py` y `check_cta.py` exigen tuplas canónicas con supuestos formales (`assumptions`) y consecuencias de ruptura (`violation_consequence`) en `cta.json`.
  4. **Fix Silencioso de `np.bool_`:** Resuelto el bug `cc_res is False` en `engine/sandbox.py`.
  5. **Linters Psicométricos Anti-Gaming:** Bloqueo de multiplicadores mágicos (`[DIAG-MAGIC-MULT]`) y opciones de longitud heterogénea en `src/validator/psychometric_checker.py`.
* **Pruebas:** `tests/test_validator.py`, `tests/test_m3_archetypes_semantic_gate.py`, `tests/test_specific_error_report_and_stem_gate.py`, `tests/test_c2c_author_speedups.py`.
* **Commits:** `954a6c8`, `cee3e5d`, `9310ff7`, `75bfde1`.

---

## Milestone 14: Motor de Maestría Integral 2.0 Estilo Khan Academy (Calibración Bidireccional, Híbrido 80/20, Fluidez y Motor 'Up Next')
* **Estado:** ✅ **COMPLETADO / VERIFICADO (Nov 2026) — Componentes Core, Fluidez y Recomendantes.**
* **Objetivo:** Elevar el motor de maestría ([`masteryStorage.ts`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/utils/masteryStorage.ts)) al estándar completo de Khan Academy: evaluación formativa bidireccional, degradación obligatoria ante fallo, fórmula híbrida de progreso, sistema de fluidez de tiempos (mejor/último tiempo por pregunta), diagnóstico granular consolidado por unidad y motor persistente de recomendación pedagógica *"Up Next for You"*.
* **Criterios de Aceptación Cumplidos (AC-32 a AC-36):**
  - **AC-32:** Calibración granular por `competency_id` en Course Challenge, Unit Tests y Quizzes intercalados (`updateCourseChallengeWithSkillCalibration`).
  - **AC-33:** Todo fallo en `Mastered` degrada a `Proficient` ($-20$ pts); en `Proficient` degrada a `Familiar` ($-30$ pts); en `Familiar` degrada a `Attempted` ($-25$ pts).
  - **AC-34:** Promoción escalonada ante acierto; ningún Challenge individual promueve de `Not started` a `Mastered` directamente (*Assessment, Not Full Mastery*).
  - **AC-35:** `CompletionScreen.tsx` despliega paneles diferenciados `Leveled Up` (verde), `Leveled Down` (rojo) y `No change` (gris) basados estrictamente en `TIER_POINTS`, con acceso directo a práctica correctiva, resumen de fluidez y consolidación por unidad de áreas a reforzar.
  - **AC-36:** Trazabilidad histórica completa `{ date, score, total, type, previous_tier, new_tier, total_seconds, avg_seconds_per_question }`.
  - **Extensiones Implementadas:** Barra híbrida 80/20 en `calculateCourseProgress`, tope en `Familiar` si se usan pistas (Pistas 2–5), indicador *Red Dot* (`needs_review`), pantalla previa unificada `PreExerciseModal.tsx` con metas de récord de tiempo, y telemetría de latencia por reactivo en `PracticeSession.tsx`.
  - **Motor Persistente 'Up Next for You' (Jerarquía de 5 Niveles en `CourseOverview.tsx`):**
    1. *Prioridad 1 (Remediación):* Si hay unidades con `needs_review: true` (rojo/ámbar), recomienda `"Repasar ahora ➔"` para la primera unidad afectada.
    2. *Prioridad 2 (Nueva Unidad):* Recomienda la primera unidad en orden ordinal no iniciada (`Not started`) con `"Comenzar práctica ➔"`.
    3. *Prioridad 3 (Unit Test Pendiente):* Si todas están iniciadas pero alguna no tiene Unit Test al 100%, recomienda `"Rendir Unit Test ➔"`.
    4. *Prioridad 4 (Course Challenge):* Si todos los Unit Tests están al 100%, recomienda `"Rendir Course Challenge ➔"`.
    5. *Prioridad 5 (Maestría Total 100%):* Banner celebratorio con `"Darle otra repasada ➔"`.
* **Componentes Obviados / Postergados en esta Sesión de Desarrollo:**
  - ⏳ **Simulador Cronometrado Adaptativo de Examen Parcial en 2 Módulos (SAT Bluebook):** Postergado y desacoplado hacia **Milestone 14-B**. Se obvió el enrutamiento dinámico a mitad de prueba (Módulo 1 diagnóstico $\to$ Módulo 2 Estándar vs. Avanzado) y el temporizador con reloj de cuenta regresiva de examen universitario para priorizar el motor psicométrico, la telemetría de fluidez y la UX de remediación.
  - ⏳ **Modelo de Decaimiento Temporal Ebbinghaus en Memoria (SRS):** Obviado de este hito; pertenece formalmente a la especificación de **Milestone 8** (degradación a los 14 y 45 días sin práctica).
  - ⏳ **Tarjeta 'Mastery Challenge' de 6 Reactivos con Cooldown de 12 Horas:** Obviado de este hito; reservado para **Milestone 8**.
* **Suite de Verificación:** [`tests/platform/test_mastery_calibration_bidirectional.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/tests/platform/test_mastery_calibration_bidirectional.py) (3/3 PASS) + [`tests/platform/test_mastery_progress_80_20.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/tests/platform/test_mastery_progress_80_20.py) (5/5 PASS).
> 📄 **Especificación Técnica Completa:** Consultar [`docs/specs/m14_khan_mastery_engine.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/m14_khan_mastery_engine.md) para la matriz psicométrica de 12 filas, interfaces y registro de decisiones.

---

## Milestone 1-T: Deuda de Pruebas de Ergonomía E2E (Matriz 12 Viewports y AC-CORE en Doble Modo)
* **Estado:** ✅ **Completado y verificado automáticamente al 100% (2026-11-14).**
* **Objetivo:** Automatizar la verificación exhaustiva contra regresiones visuales y de usabilidad en escenarios reales de laptops de alta densidad (125% y 150%), tablets y pantallas divididas (Split-View 50%), comprobando que el contrato AC-CORE se mantenga inviolable tanto en modo estándar como bajo la cortina de evocación libre (*Blank-First*).
* **Componentes Técnicos Entregados:**
  1. **Matriz Expandida de 12 Viewports (`tests/e2e_m1_viewport_matrix.mjs`):**
     - *Standard & Split Desktop:* `683x768` (Split 1366), `720x900` (Split 1440), `800x900` (Split 1600), `960x1080` (Split 1080p), `1366x768` (Laptop HD), `1440x900` (Desktop), `390x844` (Móvil).
     - *High-DPI Zoom & Tablets:* `1280x590` (Laptop 14" al 150%), `610x590` (Split 50% en Laptop 14" al 150%), `1536x740` (ASUS TUF 15.6" al 125%), `768x1024` (Tablet Vertical / Portrait), `1024x768` (Tablet Horizontal / Landscape).
  2. **Verificación Dual-Mode AC-CORE (24 Validaciones Totales):**
     - *Modo Blank-First: ON (Default):* Cortina y botón de levantamiento visibles, opciones completamente ocultas al inicio, cero desborde horizontal (`scrollWidth <= clientWidth`), KaTeX contenido dentro de sus límites geométricos, botón `Check` inferior visible, pulsación de `Enter` o botón repliega la cortina revelando exactamente 7 alternativas, toast de feedback posicionado sin solapar elementos críticos.
     - *Modo Blank-First: OFF (Estándar):* Alternado reactivamente vía botón de cabecera; 7 opciones renderizadas inmediatamente con distribución 4+3 en dos columnas (o 7 en columna única bajo 480 px), validación estricta de no-scroll y visibilidad de controles.
  3. **Aserciones No-Triviales Hardened:**
     - Validación geométrica de distribución 4+3 por coordenadas de píxeles: Columna 1 contiene items 0..3 apilados verticalmente; Columna 2 contiene items 4..6 apilados verticalmente a la derecha; o 7 items en columna única en `390x844`.
     - Resiliencia de puertos dinámicos (`find_free_port`), ciclo de vida del servidor gestionado y limpieza forzosa en Windows.
* **Pruebas:** [`tests/e2e_m1_viewport_matrix.mjs`](file:///d:/Augusto/personal_portfolio/Tops_academy/tests/e2e_m1_viewport_matrix.mjs) (12/12 PASS en ambos modos).
* **Commits:** `main`.

---

## Milestone 12: Resiliencia ante Suspensión de la Laptop (SessionStorage & ETag Reconciliation)
* **Estado:** ✅ **Completado y verificado automáticamente al 100% (2026-11-14).**
* **Objetivo:** Garantizar que si el estudiante suspende la laptop, cierra la tapa o el sistema operativo purga la memoria de la pestaña en segundo plano, la sesión de práctica restaure con precisión de milisegundo la pregunta exacta en curso, las opciones marcadas, el estado de la cortina *Blank-First* y la telemetría acumulada, reconciliando silenciosamente el estado del curso vía `ETag` sin recargas destructivas de HMR.
* **Componentes Técnicos Entregados:**
  1. **Almacenamiento Continuo de Sesión (`platform/src/utils/sessionStore.ts`):** Clave `tops_active_session_v1` en `sessionStorage` con interfaz tipada `ActiveSessionSnapshot` (`version: 1`, `courseId`, `sessionType`, `competencyId`, `unitIndex`, `questions`, `currentIndex`, `selectedOption`, `selectedMultiOptions`, `fillBlankValue`, `hintsRevealed`, `wrongAttemptsCount`, `isExhausted`, `isChecked`, `isCorrect`, `isCurtainLifted`, `results`, `telemetry`, `elapsedSeconds`, `savedAt`). Funciones `saveActiveSession`, `loadActiveSession` (con filtrado por curso y validación de versión) y `clearActiveSession`.
  2. **Hidratación Reactiva en `PracticeSession.tsx`:** Soporte de prop opcional `initialSnapshot`. Hidratación segura protegiendo el estado `isCurtainLifted` con `isInitialHydrationRef` para evitar que la cortina se repliegue al montar; sincronización reactiva inmediata en cada respuesta o interacción; desmontaje limpio en `clearActiveSession` al finalizar la sesión, volver a la biblioteca o reiniciar.
  3. **Rehidratación y Reconciliación en `App.tsx`:** Detección de sesión activa en montaje inicial para saltar directo a la práctica activa; listener en evento `visibilitychange` (`document.visibilityState === 'visible'`) que ejecuta una revalidación silenciosa con `ETag` contra `/api/courses/:id` para detectar si el curso fue modificado en el servidor mientras la máquina dormía, preservando la sesión si el contenido es idéntico (`304 Not Modified`).
  4. **Health Check Endpoint en `courseServer.cjs`:** Endpoint `GET /healthz` de baja latencia que devuelve `{ status: 'ok', uptime: process.uptime(), courses_count, timestamp }` con código HTTP 200 para monitoreo de estado.
  5. **Script de Estudio Desacoplado de HMR:** Inclusión de `"study": "npm run build && node server/courseServer.cjs"` en `platform/package.json` para permitir sesiones de estudio de alto rendimiento sin sobrecarga de sockets Vite HMR ni interferencias por desconexión en sleep. Reconstrucción completa de producción en `platform/dist/`.
* **Pruebas:** [`tests/platform/test_m12_session_resilience.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/tests/platform/test_m12_session_resilience.py) (14/14 PASS), compilación limpia en `npm run build` (tsc + vite + pwa).
* **Commits:** `main`.

---

## Milestone 13: Consolidación del Repositorio, Higiene de Artefactos y Suite de 4 Dominios
* **Estado:** ✅ **Completado y verificado automáticamente al 100% (2026-11-14).**
* **Objetivo:** Erradicar definitivamente la proliferación caótica de artefactos efímeros (*repo bloat*), desacoplar scripts temporales de depuración, blindar `.gitignore` contra volcados JSON gigantes y reestructurar la totalidad de los 1,526 tests del ecosistema en una jerarquía clara de 4 dominios gobernados por contratos arquitectónicos.
* **Componentes Técnicos Entregados:**
  1. **Política Estricta *Clean Artifacts* y Endurecimiento de `.gitignore`:**
     - Exclusión permanente de payloads efímeros de auditoría: `reports/**/qa_payload.json`, `reports/qa_audits/*_payload.json`, `reports/audits_archive/**/qa_payload.json`, `reports/c2c_audits/**/orchestrator_payload.json` y volcados de trazas `.system_generated/`.
     - Des-indexación y eliminación de 76 archivos `qa_payload.json` obsoletos que inflaban el árbol Git.
     - Purga total de 8 scripts de scratch y depuración huérfana en la raíz (`scratch_inspect.py`, `scratch_orchestrator_steps.py`, `scratch_stages.py`, `scratch_details.py`, `diagnose_repair_loop.py`, `inspect_solow_h05.py`, `debug_step.py`, `transcripts_shard_28_and_repair_h05.md` y `tests/blind_guess_empirical_results.json`).
  2. **Arquitectura Consolidada de 4 Dominios de Pruebas:**
     - `tests/quality/` (129 tests): Certificación de calidad pedagógica, linters MPRI v2.0, auditoría semántica de arquetipos, análisis de distractores a ciegas y compuertas de regresión AB20/AB30/AB40.
     - `tests/engine/` (506 tests): Validador central, invariantes del sandbox AST, canonicalizador algebraico SymPy, motor LaTeX, gramática `KaTeXAST` y QuickJS.
     - `tests/platform/` (234 tests): Resiliencia de sesión M12 (`test_m12_session_resilience.py`), contratos de ergonomía M1/M6, PWA offline, navegación popstate, API de cursos y calificación de preguntas.
     - `tests/pipeline/` (657 tests): Compiladores `compile_cta.py` y `compile_shard.py`, FSM Hook Guard, MapReduce de competencias, deduplicación de prerrequisitos, watchdog de subagentes y weighted sharding M7.
  3. **Módulo de Soporte Compartido (`tests/helpers/common.py`):**
     - Funciones de utilidad desacopladas (`find_free_port`, `strip_code_comments`, rutas canónicas de proyecto) y configuración global en `tests/conftest.py`.
  4. **Rendimiento Global de la Suite:**
     - 1,526 pruebas automatizadas ejecutadas en aproximadamente **51 segundos** con `pytest-xdist` dinámico en paralelo.
* **Pruebas:** 1,526 tests pasando al 100% en `pytest tests/` (129 quality, 506 engine, 234 platform, 657 pipeline).
* **Commits:** `main`.

---

## Milestone 9 (Fase Quick Wins): Jerarquía PPT, Unidad 0 `PRE-XX`, `ContentCoreDrawer` y Backfill
* **Estado:** ✅ **Completado, verificado automáticamente y validado visualmente por el usuario (2026-11-14).** *(Resta Paso 4 End-to-End en [`FUTURE_MILESTONES.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/FUTURE_MILESTONES.md#milestone-9-arquitectura-jerárquica-de-contenido-ppt--glosario-contentcore-khanmigo-en-5-bloques-y-unidad-0-pre-xx)).*
* **Componentes Técnicos Entregados:**
  1. **Schemas & Pipeline C2C (Stream QW-A):** Soporte de prefijo `PRE-XX` e `is_prerequisite` en `cta.schema.json`, `schema_validator.py`, `compile_cta.py`, `cta_merge.py` y `prompt_cta_architect.md`; propagación de `session`, `unit_index`, `evidence`, `assumptions`, `source_examples` e `is_prerequisite` en `run.py` (`_instantiate_single_comp`).
  2. **Plataforma React & Adaptador (Stream QW-B):** Contratos en `platform/src/types.ts`, adaptador puro retrocompatible `hierarchyAdapter.ts`, visor Split 50% `ContentCoreDrawer.tsx` (5 bloques Khanmigo + `ExplicitAssumption` + Glosario), agrupación por documento/rango de páginas y badges `PRE-XX` / evidencia / supuestos en `CourseOverview.tsx`, `MasteryGrid.tsx` y `Sidebar.tsx`, más fix de invalidación `ETag` en `courseLoader.ts`.
  3. **Backfill Determinista & Contratos (Stream QW-C):** `scripts/backfill_m9_hierarchy.py` hidrató 8 cursos en `courses/*.json` (237 competencias) con validación `strict=True`, acompañado de `tests/pipeline/test_m9_cta_modules.py` y `tests/platform/test_m9_hierarchy.py`.
* **Pruebas:** `tests/pipeline/` + `tests/engine/` (256 PASS), `tests/platform/` (238 PASS), `npm --prefix platform run build` (exit 0).
* **Commits:** `1bc0b4c`.

---
*Fin del Registro de Milestones Completados. Para consultar la hoja de ruta pendiente, ver `FUTURE_MILESTONES.md`.*
