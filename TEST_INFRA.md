# Test Infrastructure Specification: Top's Academy

## 1. Test Philosophy & Principles

The test suite for the **Top's Academy** platform is constructed upon the following fundamental testing tenets:

1. **Opaque-Box Requirement-Driven Verification**:
   Tests are written strictly against the observable behavioral specification defined in `ORIGINAL_REQUEST.md` and the UI visual design contract in `ui_spec.md`. The test runner interacts with the system exclusively through standard browser mechanisms (DOM navigation, mouse clicks, keyboard text entry, local storage inspection, and console log capture). Tests do NOT inspect private module internals or rely on mock frontends.

2. **Zero-Facade / Ground-Truth Validation**:
   Tests execute real user workflows against actual rendered DOM trees and SVG graphic surfaces. Facade tests that trivially assert truth without exercising real interactive state transitions (e.g. grading arithmetic, hint drawer toggling, coordinate plane SVG element verification) are prohibited.

3. **Adversarial & Boundary Rigor**:
   Tests systematically probe boundary edge cases:
   - Malformed / corrupted course JSON files dynamically placed into the courses repository.
   - Mathematical expressions with permutations of spacing, parenthesis, and Greek characters (e.g. `1-(alpha+n)*sigma` vs `1 - \alpha\sigma - n\sigma`).
   - Multiple-select questions requiring exact all-or-nothing selection.
   - Dynamic session shuffling to prove non-mirroring of the underlying JSON order while preserving grading integrity.

4. **Self-Contained & Isolated Execution**:
   Each test case sets up its own isolated browser context, initializes or clears local state (mastery storage), and cleans up any dynamic fixture files. Tests can run individually or as a complete suite without execution-order coupling.

5. **Visual Fidelity Parity Assurance**:
   In addition to functional assertion logic, the test harness provides automated visual state captures across the 6 platform states (Course Overview, Pre-Exercise, Question with Graph, Good Answer Toast, Exercise Complete with Confetti, and Course Challenge) for automated screenshot comparison by the Reviewer Agent.

---

## 2. Feature Inventory Mapping to Test Tiers

The 10 platform acceptance criteria from `ORIGINAL_REQUEST.md` map to the 4-tier test architecture as follows:

| Feature / Acceptance Criterion | Description | Test Tier | Test File |
| :--- | :--- | :--- | :--- |
| **AC-01: Library Course Discovery & Hot-Reload** | Lists all courses in `courses/`; dynamic addition of valid course appears upon reload with zero code change. | **Tier 1** | `test_platform_library.py::test_library_lists_all_courses`<br>`test_platform_library.py::test_dynamic_course_hot_reload` |
| **AC-02: Fault-Tolerant Error Isolation** | Invalid/corrupted course file displays an explicit diagnostic error card without breaking other valid courses. | **Tier 2** | `test_platform_library.py::test_invalid_course_isolated_with_error` |
| **AC-03: Course Overview & Mastery Matrix** | Shows one unit per competency, full mastery legend (Mastered, Proficient, Familiar, Attempted, Not started, Quiz, Unit test), and course mastery %. | **Tier 1** | `test_platform_course_overview.py::test_course_overview_structure_and_legend` |
| **AC-04: Full Practice Session Lifecycle** | Wrong answer → incorrect feedback; sequential hint reveal (hints 1..N in order); correct answer → "Good work!" speech-bubble toast with step-by-step solution expansion; completion screen with score. | **Tier 1** | `test_platform_practice_session.py::test_full_practice_lifecycle_wrong_hints_correct_completion` |
| **AC-05: Session Shuffling & Non-Mirroring** | Across repeated sessions of same unit, question and option orders differ from JSON order and from each other; grading remains correct after shuffling. | **Tier 3** | `test_platform_randomization.py::test_session_question_and_option_shuffling_and_grading` |
| **AC-06: Multi-Type Interactive Grading** | All 3 types graded correctly: MCQ 7 options; algebraic equivalence (`1-(alpha+n)*sigma` for `1 - \alpha\sigma - n\sigma`, `0.5` for `1/2`); all-or-nothing multi-select. | **Tier 2** | `test_platform_grading_types.py::test_mcq_7_options_grading`<br>`test_platform_grading_types.py::test_fill_in_the_blank_math_equivalence`<br>`test_platform_grading_types.py::test_multiple_select_all_or_nothing` |
| **AC-07: Mastery Progression & Persistence** | Mastery level increments upon successful practice and persists in LocalStorage across browser reloads. | **Tier 3** | `test_platform_mastery_persistence.py::test_mastery_level_changes_and_persists_across_reloads` |
| **AC-08: Quizzes, Unit Tests & Course Challenge** | Launch and completion of Unit Quiz, Unit Test, and Course Challenge (~30 questions across units). | **Tier 4** | `test_platform_assessments.py::test_quiz_and_unit_test_flow`<br>`test_platform_assessments.py::test_course_challenge_flow` |
| **AC-09: SVG / Vector Graph Rendering** | Questions with graph specifications render Cartesian axes, curves, and open/closed points in DOM/SVG. | **Tier 1** | `test_platform_graphs.py::test_coordinate_plane_svg_rendering` |
| **AC-10: Clean Console / Zero Unhandled Errors** | Zero runtime JavaScript exceptions, unhandled rejections, or React error boundaries during the entire test suite. | **Cross-Tier** | Monitored continuously across all test runs via `conftest.py` page fixture. |
| **VF-01: Visual Fidelity Screenshot Capture** | Automated capture of the 6 canonical platform states matching reference screenshots. | **Tier 4** | `test_visual_fidelity_capture.py::test_capture_six_canonical_states` |

---

## 3. Test Architecture & Runner Setup

### 3.1 Framework Selection: Playwright on Windows
- **Engine**: Playwright for Python (`playwright>=1.49.0`, `pytest-playwright>=0.7.0`) and/or Node Playwright (`@playwright/test`).
- **Browser**: Chromium in headless mode (`--headless=new`).
- **Operating System Compatibility**: Native Windows execution (`win64`).
- **Console Monitoring**: Strict event handler on `page.on("console", ...)` and `page.on("pageerror", ...)` recording all console errors and failing tests if unhandled errors occur.

### 3.2 Single-Command Execution

The test suite can be run directly with a single command from the repository root:

```powershell
# Run full E2E test suite in headless mode
python -m pytest tests/e2e/ -v

# Run specific tier or test file
python -m pytest tests/e2e/test_platform_practice_session.py -v

# Run visual fidelity screenshot generation
python -m pytest tests/e2e/test_visual_fidelity_capture.py -v
```

Additionally, an npm wrapper is defined in `package.json`:
```powershell
npm.cmd run test:e2e
```

### 3.3 Server Lifecycle & Orchestration
The test harness in `conftest.py` manages the web application lifecycle:
1. **Server Probe / Auto-Spawn**: Checks if the platform development server or static runner is already listening on `http://localhost:5173` or `http://localhost:3000`. If not running, launches the platform server in a managed background subprocess and polls until HTTP 200 is received.
2. **Dynamic Fixtures Directory**: Pointed at `courses/` and `courses/test_fixtures/`. Temporary fixture files injected during hot-reload tests are automatically unlinked upon test completion.
3. **Storage Isolation**: Browser contexts start with fresh `localStorage` or inject deterministic seed states where explicitly required.

---

## 4. 4-Tier Test Methodology

```
+-------------------------------------------------------------------------------+
|  TIER 4: Real-World Scenarios & Full Student Workflows                         |
|  - Comprehensive Course Challenge (~30 questions across units)                |
|  - Multi-unit Quiz and Unit Test flows                                        |
|  - 6-State Visual Fidelity artifact generation                                |
+-------------------------------------------------------------------------------+
|  TIER 3: Cross-Feature State & Combinations                                   |
|  - Random question order + randomized option order + correct grading          |
|  - Repeated session order divergence (non-mirroring verification)              |
|  - Mastery level calculation + persistent LocalStorage reload survival        |
+-------------------------------------------------------------------------------+
|  TIER 2: Boundary, Corner Cases & Fault Isolation                             |
|  - Corrupted course JSON error cards while valid courses remain active        |
|  - Symbolic math equivalence variations (whitespace, signs, fractions)        |
|  - Multiple-select all-or-nothing grading boundary (partial = incorrect)     |
+-------------------------------------------------------------------------------+
|  TIER 1: Primary Feature Coverage & Core Happy Paths                          |
|  - Course library navigation & dynamic file hot-reload                        |
|  - Course overview, units, mastery legend, course %                           |
|  - Pre-exercise screen ("Ready to practice?" & question count)                |
|  - Question card with inline KaTeX math & SVG coordinate plane                |
|  - Correct feedback toast ("Good work!") & step-by-step solution expansion    |
|  - Sequential progressive hint reveal                                         |
|  - "Exercise complete!" celebration screen with score                         |
+-------------------------------------------------------------------------------+
```

### Tier 1: Primary Feature Coverage
Verifies that all standard user journeys function smoothly from start to finish:
- Landing on the course library and navigating into a course.
- Inspecting the course overview with unit competency cards and mastery blocks.
- Launching practice for a competency and completing questions.
- Revealing sequential hints in numerical order (Hint 1 -> Hint 2 -> Hint 3).
- Observing the correct answer feedback toast with the downward speech-bubble pointer and opening the full step-by-step solution.

### Tier 2: Boundary & Corner Cases
Probes failure modes and edge cases:
- Adding a syntactically malformed JSON file to `courses/`: the server and UI isolate the faulty course with an error indicator, while existing valid courses remain fully playable.
- Fill-in-the-blank math engine: verifies that algebraic expressions like `1-(alpha+n)*sigma`, `1 - \alpha\sigma - n\sigma`, `1 - \sigma\alpha - \sigma n` and fractions/decimals like `1/2` vs `0.5` evaluate to correct answers.
- Multiple-select questions: selects subset of correct options, asserts evaluation is strictly incorrect (all-or-nothing).

### Tier 3: Cross-Feature Combinations
Verifies multi-system interactions:
- Shuffling & Non-Mirroring: runs two independent practice sessions of the same unit. Records the presented question sequence and option sequence for each item. Asserts:
  1. The presented order does not mirror the raw order in the JSON file.
  2. Successive sessions do not have identical question order.
  3. Option shuffling properly preserves the correct answer mapping so the student is graded accurately regardless of option position.
- Mastery Progression & LocalStorage: completes a practice session with all correct answers. Asserts that the competency mastery moves from "Not started" / "Attempted" to "Familiar" or "Proficient". Reloads the browser page and asserts that the updated mastery tier persists.

### Tier 4: Real-World Application Scenarios
Simulates realistic student learning sessions:
- Starting and completing a unit quiz and unit test.
- Starting and completing the full Course Challenge (~30 questions drawn across all course competencies).
- Capturing high-resolution screenshots for the 6 visual reference states and outputting them to `tests/e2e/screenshots/` for reviewer audit.

---

## 5. Pass/Fail Criteria & Diagnostic Reporting

- **Strict Pass Criterion**: 100% of test assertions must pass. Any unhandled browser exception (`pageerror` or `console.error`) immediately fails the test.
- **Diagnostic Logging**:
  - Failure screenshots are automatically captured in `tests/e2e/reports/failures/`.
  - DOM snapshots on failure are saved alongside screenshots.
  - Verbatim browser console messages are captured and printed in the test traceback.

---

## 6. Comprehensive Automated Test Matrix (Python + Node.js)

In addition to the Playwright browser suite, the repository includes a multi-tiered automated test matrix covering the validator engine, pipeline optimizations, sandboxed runtime, and client-side mathematical evaluation:

### 6.1 Python Automated Test Suites (367 items / 363 passed, 4 skipped in 18.05s)

```powershell
.venv\Scripts\python.exe -m pytest -v
```

| Test Suite File | Items | Focus / Coverage |
| :--- | :---: | :--- |
| `tests/test_validator.py` | 144 | Scanner léxico, RFC 8259, R-01..R-16, R-17..R-20, R-22, S-01..S-03, KaTeX arity, entornos, llaves residuales |
| `tests/test_engine_invariants_adversarial.py` | 51 | Invariantes psicométricos, verificación de ensamblaje en sandbox, anti-giveaway |
| `tests/test_sandbox_adversarial.py` | 49 | Seguridad del AST sandbox, bloqueo de imports prohibidos, memoria y timeouts |
| `tests/test_skill.py` | 33 | Extracción de contenido, taxonomía CTA, batch generator, SymPy Tier 1, Blind solver Tier 2 |
| `tests/test_platform.py` | 19 | Endpoints HTTP del servidor, enrutamiento SPA estático, flags CLI (`--scan`, `--help`) |
| `tests/test_cta_mapreduce.py` | 16 | Partición seccional de corpus, `cta_merge.py`, DAG de prerrequisitos, deduplicación |
| `tests/test_c2c_validator_prescriptive.py` | 12 | Sugerencias prescriptivas del validador y conformidad de esquema |
| `tests/test_dispatch_scope.py` | 10 | Segregación de roles de subagentes y contratos de prompts |
| `tests/test_delete_course.py` | 8 | Eliminación segura de cursos (<300ms), preservación de auditorías históricas, inmutabilidad de `content/` |
| `tests/test_handouts.py` | 8 | Procesamiento y fallback de handouts visuales |
| `tests/test_pipeline_optimizations.py` | 6 | Validaciones de rendimiento, optimizaciones de pipeline y multi-core `ProcessPoolExecutor` |
| `tests/test_skill_v3.py` | 6 | Runner de pipeline de alta velocidad v3 y gates de etapa |
| `tests/test_template_variability.py` | 5 | Regla `TPL-VAR`, validación de `stem_variants >= 3` y ratio de diversidad $\ge 0.50$ |

### 6.2 Client-Side & Standalone Verification Suites

| Suite File | Items / Tests | Status | Focus |
| :--- | :---: | :---: | :--- |
| `tests/test_math_adversarial_suite.mjs` | 81 cases | **100% PASS** | Equivalencia algebraica y numérica con coma española (`0,8333`), fracciones, letras griegas, tolerancias |
| `tests/test_question_grading.mjs` | 1,048 assertions | **100% PASS** | Evaluación y normalización de opciones MC y MS en cursos activos e históricos |
| `tests/test_keyboard_navigation.mjs` | All assertions | **100% PASS** | Accesibilidad de teclado (1-7 para opciones, Enter para Check/Next) |
| `tests/test_unit_isolation.mjs` | All assertions | **100% PASS** | Aislamiento de unidades y límites de shuffling independiente |
| `tests/test_blind_guess_empirical.py` | 50 sample / 250 pop | **100% PASS** | Prueba adversarial empírica de distractores a ciegas (4.0% éxito muestral, 8.0% poblacional vs $\le 30\%$) |

