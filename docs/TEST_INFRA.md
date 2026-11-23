# Test Infrastructure Specification: Top's Academy

## 1. Test Philosophy & Principles

The test suite for the **Top's Academy** platform is constructed upon the following fundamental testing tenets:

1. **Opaque-Box Requirement-Driven Verification**:
   Tests are written strictly against observable behavioral specifications and visual/psychometric design contracts. The test runner interacts with the system exclusively through standard browser mechanisms (DOM navigation, mouse clicks, keyboard text entry, local/session storage inspection, and console log capture) or formal CLI / engine interfaces. Tests do NOT inspect private module internals or rely on mock frontends.

2. **Zero-Facade / Ground-Truth Validation**:
   Tests execute real user workflows against actual rendered DOM trees and SVG graphic surfaces. Facade tests that trivially assert truth without exercising real interactive state transitions (e.g. grading arithmetic, hint drawer toggling, coordinate plane SVG element verification) are strictly prohibited.

3. **Adversarial & Boundary Rigor**:
   Tests systematically probe boundary edge cases:
   - Malformed / corrupted course JSON files dynamically placed into the courses repository.
   - Mathematical expressions with permutations of spacing, parenthesis, Greek characters, and Spanish comma notation.
   - Multiple-select questions requiring exact all-or-nothing selection.
   - Dynamic session shuffling to prove non-mirroring of the underlying JSON order while preserving grading integrity.
   - AST sandbox security, blocking unauthorized built-ins, recursion bombs, and memory exhaustion.

4. **Self-Contained & Isolated Execution**:
   Each test case sets up its own isolated context, initializes or clears local/session storage, and cleans up dynamic fixture files. Tests run individually or as a complete suite without execution-order coupling.

5. **Visual Fidelity Parity Assurance**:
   The test harness automates verification across the entire platform lifecycle: Course Overview, Pre-Exercise, Question with SVG Graph, Feedback Toast, Exercise Complete celebration, and Course Challenge, alongside high-density multi-viewport responsiveness matrices.

---

## 2. 4-Domain Test Architecture & Consolidation (Milestone 13)

Under **Milestone 13 (Higiene del Repositorio y Consolidación de Tests)**, all tests across the repository are strictly structured into **4 functional domains** with a dedicated helpers layer, eliminating root clutter and enforcing clean separation of concerns:

```
tests/
├── conftest.py                       # Configuración global pytest y fixtures
├── helpers/
│   ├── __init__.py
│   └── common.py                     # Utilidades compartidas (find_free_port, strip_code_comments, paths)
├── quality/                          # DOMINIO 1: Calidad Pedagógica, Psicométrica y Regresión (129 tests)
│   ├── test_ab20_regression_gates.py
│   ├── test_ab30_remediations.py
│   ├── test_ab40_gate_patches.py
│   ├── test_blind_guess_empirical.py
│   ├── test_forensic_replay_ab30cf91.py
│   ├── test_m3_archetypes_semantic_gate.py
│   ├── test_new_audit_linters.py
│   ├── test_specific_error_report_and_stem_gate.py
│   └── test_template_variability.py
├── engine/                           # DOMINIO 2: Motor Simbólico, Sandbox AST y KaTeX (506 tests)
│   ├── test_assemble_katex_and_rationale.py
│   ├── test_assemble_sanitize_katex_r23.py
│   ├── test_c2c_validator_prescriptive.py
│   ├── test_engine_invariants_adversarial.py
│   ├── test_invariants_and_shard_overescape_r23.py
│   ├── test_katex_overescape_validator_r23.py
│   ├── test_katex_prairielearn_tokens.py
│   ├── test_latex_engine.py
│   ├── test_milestone4_formc_katex_ast.py
│   ├── test_pykatex_warn.py
│   ├── test_sandbox_adversarial.py
│   ├── test_sandbox_gil_and_circuit_breaker.py
│   └── test_validator.py
├── platform/                         # DOMINIO 3: Frontend Web, PWA, Ergonomía y Resiliencia (234 tests)
│   ├── test_c2c_case_2b_mastery.py
│   ├── test_course_api_manifest.py
│   ├── test_keyboard_navigation.mjs
│   ├── test_m1_zoomfix_contract.py
│   ├── test_m6_study_harness_contract.py
│   ├── test_m12_session_resilience.py
│   ├── test_mastery_calibration_bidirectional.py
│   ├── test_mastery_progress_80_20.py
│   ├── test_math_adversarial_suite.mjs
│   ├── test_math_adversarial_suite.ts
│   ├── test_platform.py
│   ├── test_platform_katex_admission_guard.py
│   ├── test_pwa_navigation_and_install.py
│   ├── test_pwa_offline.py
│   ├── test_question_grading.mjs
│   └── test_unit_isolation.mjs
├── pipeline/                         # DOMINIO 4: Pipeline C2C, Orquestación y Compiladores (657 tests)
│   ├── test_append_workflow.py
│   ├── test_bootstrap_and_wave_streaming.py
│   ├── test_c2c_author_speedups.py
│   ├── test_c2c_error_aggregation.py
│   ├── test_c2c_remediation_optimization.py
│   ├── test_c2c_solow2_architectural_improvements.py
│   ├── test_c2c_straggler_and_postproduction_prevention.py
│   ├── test_c2c_v31_adversarial_plan.py
│   ├── test_c2c_v321_comp1_cta.py
│   ├── test_c2c_v321_comp2_shard.py
│   ├── test_c2c_v321_comp3_dispatch.py
│   ├── test_c2c_v321_comp4_prompts.py
│   ├── test_c2c_v321_multi_instance_and_append.py
│   ├── test_c2c_v40_formal_certification.py
│   ├── test_compile_cta_error_specificity.py
│   ├── test_compile_shard.py
│   ├── test_compile_shard_fail_total.py
│   ├── test_compile_shard_watchdog.py
│   ├── test_cta_duplicate_detection_v2.py
│   ├── test_cta_healing.py
│   ├── test_cta_mapreduce.py
│   ├── test_cta_merge_prereq_scoping.py
│   ├── test_cta_sweetspot_and_autoheal.py
│   ├── test_delete_course.py
│   ├── test_dispatch_scope.py
│   ├── test_dispatch_turn0_and_milestone3_prompts.py
│   ├── test_fast_ingest_and_cta_append.py
│   ├── test_forensic_shard06_and_variance_v34.py
│   ├── test_handouts.py
│   ├── test_hook_post_pass_and_write_isolation.py
│   ├── test_orchestration_resilience.py
│   ├── test_pipeline_optimizations.py
│   ├── test_pipeline_reparations.py
│   ├── test_prompts_contract_alignment.py
│   ├── test_run_templates_and_dispatch_repair.py
│   ├── test_shard06_and_dry_archetypes.py
│   ├── test_shard_compiler_hardening.py
│   ├── test_skill.py
│   ├── test_skill_v3.py
│   ├── test_sweetspot_v35_cta_and_shards.py
│   ├── test_system_prompts_compile_clean.py
│   ├── test_watchdog_and_hooks.py
│   └── test_weighted_sharding_m7.py
└── e2e_m1_viewport_matrix.mjs        # Suite E2E Dual-Mode Playwright (12 Viewports)
```

### Resumen de Pruebas por Dominio (1,526 Tests Python en ~51 s)

| Dominio | Directorio | Tests | Alcance Principal |
| :--- | :--- | :---: | :--- |
| **Calidad** | `tests/quality/` | **129** | Linters Path-to-Mastery v2.0, índice MPRI (6 pilares), comisiones `[STEM-DIVERSITY-GATE]`, compuertas de regresión AB20/AB30/AB40, entropía de arquetipos y test adversarial de adivinanza a ciegas. |
| **Motor** | `tests/engine/` | **506** | Validador canónico RFC 8259, reglas R-01..R-23, invariantes inductivos `KaTeXAST` (§7.2 `TopsAcademyC2C.lean`), validador QuickJS por columna, SymPy algebraic canonicalizer, seguridad del AST sandbox y circuit breakers GIL. |
| **Plataforma** | `tests/platform/` | **234** | Resiliencia de sesión ante suspensión M12 (`test_m12_session_resilience.py`), contratos de ergonomía M1 (Zoom-Fix y Split 50%), arnés M6 (Blank-First, mouseless, socrático), PWA offline, historial de navegación popstate y API manifest. |
| **Pipeline** | `tests/pipeline/` | **657** | Compiladores `compile_cta.py` y `compile_shard.py`, FSM Hook Guard (`c2c_hook_guard.py`), weighted waves de hasta 100 shards concurrentes, deduplicación de prerrequisitos en `cta_merge.py`, recibos SHA-256 y watchdog. |
| **Total Global** | `tests/` | **1,526** | **100% PASS en ~51 segundos** con ejecución distribuida `pytest-xdist` (`worksteal`). |

---

## 3. Comandos de Ejecución de la Suite

### 3.1 Ejecución Completa de la Suite Python

```powershell
# Ejecución global en paralelo con pytest-xdist auto-detect
.venv\Scripts\python.exe -m pytest -q

# Ejecución de un dominio específico
.venv\Scripts\python.exe -m pytest tests/quality/ -v
.venv\Scripts\python.exe -m pytest tests/engine/ -v
.venv\Scripts\python.exe -m pytest tests/platform/ -v
.venv\Scripts\python.exe -m pytest tests/pipeline/ -v

# Ejecución de un archivo de prueba específico
.venv\Scripts\python.exe -m pytest tests/platform/test_m12_session_resilience.py -v
```

### 3.2 Ejecución de Suites Node.js y E2E Playwright

```powershell
# Matriz E2E de 12 Viewports en Doble Modo (Blank-First ON / OFF)
node tests/e2e_m1_viewport_matrix.mjs

# Suite adversarial de equivalencia matemática client-side
node tests/platform/test_math_adversarial_suite.mjs

# Suite de calificación y normalización de opciones
node tests/platform/test_question_grading.mjs

# Accesibilidad de navegación mouseless
node tests/platform/test_keyboard_navigation.mjs
```

---

## 4. Matriz E2E Playwright de 12 Viewports (Milestone 1-T)

La suite [`tests/e2e_m1_viewport_matrix.mjs`](file:///d:/Augusto/personal_portfolio/Tops_academy/tests/e2e_m1_viewport_matrix.mjs) valida la plataforma de forma determinista contra **12 viewports representativos** de dispositivos reales, ejecutando una verificación dual exhaustiva bajo ambos estados de la cortina *Blank-First* (**24 configuraciones completas**):

```
+---------------------------------------------------------------------------------------+
|                       MATRIZ E2E EXPANDIDA (12 VIEWPORTS)                             |
+-----------------------------------+---------------------------------------------------+
| Viewport / Escenario              | Resolución y Dispositivo                          |
+-----------------------------------+---------------------------------------------------+
| 0. Split 50% en Laptop 1366       | 683 × 768 px                                      |
| 1. Split 50% en Monitor 1440      | 720 × 900 px                                      |
| 2. Split 50% en Monitor 1600      | 800 × 900 px                                      |
| 3. Split 50% en Monitor 1080p     | 960 × 1080 px                                     |
| 4. Laptop HD Completa             | 1366 × 768 px                                     |
| 5. Desktop Completa               | 1440 × 900 px                                     |
| 6. Smartphone Móvil               | 390 × 844 px (iPhone 13 / Android)                |
| 7. Laptop 14" con Zoom 150%       | 1280 × 590 px (Viewport real renderizado)         |
| 8. Split 50% Laptop 14" Zoom 150% | 610 × 590 px (Escenario más exigente)             |
| 9. Laptop Gaming TUF con Zoom 125%| 1536 × 740 px (ASUS TUF 15.6" 125%)               |
| 10. Tablet Vertical (Portrait)    | 768 × 1024 px (iPad / Android Tablet)             |
| 11. Tablet Horizontal (Landscape) | 1024 × 768 px (iPad / Android Tablet)             |
+-----------------------------------+---------------------------------------------------+
```

### Verificación Dual AC-CORE por Viewport:

1. **Modo `Blank-First: ON` (Por Defecto):**
   - Cortina de evocación libre y botón `[ 💡 Ya tengo mi planteamiento ]` (`lift-curtain-btn`) visibles.
   - Las 7 alternativas permanecen completamente ocultas antes del levantamiento.
   - Validación AC-CORE bajo la cortina: cero desborde horizontal (`scrollWidth <= clientWidth`), KaTeX contenido dentro de márgenes y botón inferior de acción visible.
   - Tecla `Enter` o clic en el botón repliega la cortina y revela inmediatamente las 7 opciones con distribución matemática 4+3 (o columna única en móvil).
   - Toast de feedback (`FeedbackToast.tsx`) posicionado sin solapar elementos interactivos ni causar scroll vertical forzado.

2. **Modo `Blank-First: OFF` (Estándar):**
   - Alternado mediante selector accesible de cabecera (`[data-testid="toggle-blank-first-btn"]`).
   - Cortina ausente; las 7 opciones se renderizan de forma inmediata.
   - Distribución geométrica de 2 columnas: Columna 1 contiene alternativas 0..3 apiladas verticalmente; Columna 2 contiene alternativas 4..6 apiladas a la derecha. En pantallas `< 480 px` (móvil `390x844`), las 7 alternativas se apilan verticalmente en columna única.
   - Verificación de no-scroll horizontal, delimitación estricta de KaTeX y visibilidad del botón de calificación (`check-btn`).

**Resultado de Certificación:** ✅ **12 / 12 PASS (100% de éxito).**

---

## 5. Resiliencia ante Suspensión de la Laptop (Milestone 12)

La suite [`tests/platform/test_m12_session_resilience.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/tests/platform/test_m12_session_resilience.py) certifica la continuidad pedagógica cuando el sistema operativo suspende la laptop o descarga la pestaña de memoria:

1. **Contrato de Almacenamiento Reactivo (`sessionStore.ts`):**
   - Clave `tops_active_session_v1` en `sessionStorage`.
   - Snapshot tipado: versión, curso, tipo de sesión, competencia, unidad, listado de preguntas, índice activo, opciones seleccionadas, entradas numéricas, pistas reveladas, intentos fallidos, estado de la cortina *Blank-First*, resultados acumulados y telemetría de tiempos por reactivo.
   - Protección contra corrupción de JSON y migración de esquemas.

2. **Hidratación y Protección de Estado (`PracticeSession.tsx`):**
   - Hidratación segura del estado inicial mediante `initialSnapshot`.
   - Salvaguarda `isInitialHydrationRef` para evitar que la cortina se repliegue prematuramente al restaurar una sesión activa.
   - Persistencia reactiva continua en cada interacción del estudiante.
   - Desmontaje y limpieza total de la sesión (`clearActiveSession`) al finalizar o abandonar la práctica.

3. **Reconciliación Silenciosa con `ETag` (`App.tsx`):**
   - Listener de visibilidad de ventana (`visibilitychange`): detecta el retorno tras la suspensión (`visibilityState === 'visible'`).
   - Envío de cabecera `If-None-Match` al servidor local: respuesta `304 Not Modified` confirma que el curso en disco no cambió y reanuda la práctica sin recarga de página. Si el curso fue modificado en disco, se notifica y actualiza de forma controlada.

4. **Infraestructura de Estudio Desacoplada de HMR:**
   - Endpoint de monitoreo de salud `GET /healthz` en `courseServer.cjs` (devuelve HTTP 200 con `{ status: 'ok', uptime, courses_count, timestamp }`).
   - Script `"study": "npm run build && node server/courseServer.cjs"` en `platform/package.json` para sesiones de estudio de alto rendimiento inmunes a desconexiones de WebSockets de Vite HMR durante la suspensión.

**Resultado de Certificación:** ✅ **14 / 14 PASS (100% de éxito).**

---

## 6. Suites Client-Side y Verificación Estándar

| Suite File | Casos / Aserciones | Estado | Foco Principal |
| :--- | :---: | :---: | :--- |
| `tests/platform/test_math_adversarial_suite.mjs` | 81 casos | **100% PASS** | Equivalencia algebraica y numérica con coma decimal española (`0,8333`), fracciones, expresiones con letras griegas y tolerancias. |
| `tests/platform/test_question_grading.mjs` | 1,048 aserciones | **100% PASS** | Evaluación rigurosa de respuestas de opción múltiple (MC7) y opción multiselección (MS) en cursos activos e históricos. |
| `tests/platform/test_keyboard_navigation.mjs` | Todas | **100% PASS** | Accesibilidad 100% sin ratón (teclas `A`–`G` / `1`–`7` para marcar/desmarcar opciones, `Enter` para Check/Next). |
| `tests/platform/test_unit_isolation.mjs` | Todas | **100% PASS** | Aislamiento estricto de unidades y límites de shuffling independiente entre sesiones repetidas. |
| `tests/quality/test_blind_guess_empirical.py` | 50 sample / 250 pop | **100% PASS** | Prueba adversarial empírica de distractores a ciegas (4.0% éxito muestral, 8.0% poblacional frente a cota máxima $\le 30\%$). |

---
*Especificación canónica de infraestructura de pruebas. Cualquier alteración de dominios, contratos de evaluación o matrices de viewport debe actualizarse en este documento.*
