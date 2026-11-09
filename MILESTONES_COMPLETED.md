# Registro de Milestones Completados y Certificados: Tops Academy

> **Propósito:** Archivo histórico y bitácora forense de los milestones **cerrados y certificados**.  
> **Hoja de Ruta Activa:** Lo pendiente, en curso o en backlog vive en [`FUTURE_MILESTONES.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/FUTURE_MILESTONES.md) *(espejo en `docs/future_milestones/FUTURE_MILESTONES.md`)*.  
> **Conocimiento Tribal y Arquitectura:** La explicación causal de por qué los sistemas funcionan así vive en [`CONOCIMIENTO_TRIBAL.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/CONOCIMIENTO_TRIBAL.md).  
> **Convención de Certificación:** Cada entrada declara *quién* certificó y *cómo*. «Certificado por el usuario» = prueba manual en sus equipos. «Verificado automáticamente» = tests unitarios, contratos o suites E2E con nombre y resultado.  
> **Última Actualización:** 2026-11-08 (Branch: `main` / `optimizaciones_test` — Pipeline C2C v4.0 "Más con Menos", DSL Form-C y KaTeXAST, Shift-Left 4 Arquetipos, FSM Hook Guard y M1, 2, 2a, 3, 4, 7, 10, 11 [núcleo], 15 [F1], 16 [F1] cerrados).

---

## Índice de Milestones Cerrados

| Milestone | Alcance cerrado | Certificación | Commits |
| :--- | :--- | :--- | :--- |
| **1** Ergonomía Web (Zoom-Fix, Split 50%, Remediación v3) | Laptops 14" a 150%, TUF F15 a 125%, split 50%, tablets; biblioteca de 3 columnas; prosa en fórmulas | Usuario (2026-10-26) + matriz de 7 viewports + 97 contratos | `05c8f4b`, `12042d0`, `950bd20` |
| **2a** Usabilidad móvil | Teléfono: columna única, drawer, footer en flujo | Usuario (2026-10-26) + viewport 390 × 844 en la matriz | los de M1 |
| **2** PWA Instalable y Modo Offline | Service Worker Workbox, precaching App Shell + fuentes KaTeX, Web App Manifest, suite de iconos (192, 512, maskable), badge `✓ Offline`, navegación nativa popstate (`navigationHistory.ts`), instalación guiada | Automática (`tests/test_pwa_offline.py`, `tests/test_pwa_navigation_and_install.py`) + Verificado en producción PWA (2026-11-01) | `23cb4ec`, `e26769b`, `7e6a238`, `9296f9c` |
| **3** Anti-Overfitting y Variedad de Plantillas (v3.8 Tri-Banda) | Contrato Tri-Banda (`--min-archetypes 3`, 3 bandas ZPD, $\ge 2$ Bloom, cuota FIB/MS, `[STEM-DIVERSITY-GATE]`) + `ArchetypeEntropyLinter` (`MIN_ARCHETYPES = 3` + `ratio > 0.85` + MPRI) | Automática (`test_new_audit_linters.py`, 11 cursos publicados con 0 infracciones) | `5b5395c`, `be43b08`, `b07cec8` + cierre 2026-10-31 |
| **4** DSL Form-C, Desacoplamiento KaTeX, Pydantic y Gramática KaTeXAST (100%) | Contrato Pydantic `ShardCompetenceContract` y `ArchetypeKind`, validación inductiva `KaTeXAST` + `pykatex_validate_with_column`, canonicalizador algebraico `canonicalize_algebraic_katex` + `sympy_to_katex` en `engine/katex_ast.py`, DSL `Form-C` en 55–70 líneas con auto-exportación AST de `vars` en `compile_shard.py`, PrairieLearn `@var@` en raw strings, precheck `[SYMPY-LATEX-MATRIX]` y migración EDO/EDP | Automática (`tests/test_milestone4_formc_katex_ast.py` [23/23 PASS], `tests/test_c2c_v321_comp4_prompts.py`, `tests/test_sweetspot_v35_cta_and_shards.py`) + migración de plantillas EDO/EDP | `315690c`, `cee3e5d`, `884c305`, `cb84a16`, `6208088` |
| **7** Pipeline "Más con Menos" (Target `< 12 min` y `-65%` Tokens) | Deduplicación masiva `-2.0M` tokens en `dispatch.py` (eliminación de triple envío Prompt/work_order/items), recibos criptográficos SHA-256 (`shard_XX.cert.json`) en compilador $< 5\text{ ms}$, subagentes `--lean` por defecto con prompts $\le 5\text{ KB}$, weighted waves de hasta 100 shards concurrentes, precheck estático AST $< 50\text{ ms}$ (`shard_precheck.py`), y suite global de 1,404 tests en 27.76s | Automática (1,404 tests pasando al 100% en 27.76s en `pytest tests/ -q`) + 3 auditorías forenses | `e357df5`, `cb84a16`, `6208088`, `75bfde1`, `c81aaa6` |
| **10** QA Rubric v2.0 Deep Mastery | 7 linters Path-to-Mastery v2.0, MPRI (/100 pts en 6 pilares, cuota $\ge 25\%$ multimodal), penalizaciones duras, compuerta bloqueante pre-publish `PublishQualityGateError` con mapeo AST | Automática (`tests/test_new_audit_linters.py`) + Auditoría en pipeline sobre 11 cursos | `be43b08`, `24c44f8`, `0e2fd38`, `b07cec8` |
| **11** Carga de cursos — núcleo | Manifest slim, índice con caché, ETag/304/gzip, manifest inline, IndexedDB, prefetch | Automática (12 tests de API + build); ACs de cliente sin medir | `41435c5`, `b73a5ee`, `2051b8b`, `97fa2f3` |
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
*Fin del Registro de Milestones Completados. Para consultar la hoja de ruta pendiente, ver `FUTURE_MILESTONES.md`.*
