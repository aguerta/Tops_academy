# Test Suite Ready: Top's Academy

**Date**: 2026-10-11  
**Status**: TEST READY (All Platform Acceptance Criteria Covered)  
**Author**: E2E Test Suite Writer (`test_writer_e2e`)

---

## 1. Quick Start / Single Execution Commands

The automated E2E headless browser test suite can be run directly with a single command from the project root:

### Primary Python Runner (pytest + Playwright):
```powershell
# Run all 14 headless E2E acceptance tests
python -m pytest tests/e2e -v

# Run visual fidelity screenshot capture (generates the 6 platform states)
python -m pytest tests/e2e/test_visual_fidelity_capture.py -v

# Run specific functional test module
python -m pytest tests/e2e/test_platform_practice_session.py -v
```

### TypeScript / Node Runner (Playwright Test):
```powershell
# Run Playwright test suite in headless mode
npx.cmd playwright test --config=tests/e2e/playwright.config.ts

# Or via npm script
npm.cmd run test:e2e
```

---

## 2. Test Architecture & Environment

- **Browser**: Chromium (headless mode `chromium-1243` / `chromium-headless-shell`).
- **Resolution**: 1280 × 800 standard desktop viewport.
- **Console Monitoring**: Strict event listeners on `page.on("console", ...)` and `page.on("pageerror", ...)`. Unhandled JavaScript runtime errors or React error boundary explosions immediately fail the test.
- **Server Orchestration**: Fixture in `tests/e2e/conftest.py` automatically detects or starts the platform server on `http://localhost:5173` or `http://localhost:3000`.

---

## 3. Platform Acceptance Criteria Feature Checklist

| # | Acceptance Criterion | Test Target | Status |
|:---:|:---|:---|:---:|
| **AC-01** | **Course Library & Dynamic Discovery**<br>Library lists every course in `courses/` folder; copying a new valid course file into the folder makes it appear after reload with zero code change. | `test_platform_library.py::test_library_lists_all_courses`<br>`test_platform_library.py::test_dynamic_course_hot_reload` | ✅ Ready |
| **AC-02** | **Fault-Tolerant Error Isolation**<br>An invalid course file shows an error for that course while other courses still work. | `test_platform_library.py::test_invalid_course_isolated_with_error` | ✅ Ready |
| **AC-03** | **Course Overview Structure**<br>Course overview shows one unit per competency, mastery legend (Mastered, Proficient, Familiar, Attempted, Not started, Quiz, Unit test), and course mastery %. | `test_platform_course_overview.py::test_course_overview_structure_and_legend` | ✅ Ready |
| **AC-04** | **Full Practice Lifecycle**<br>Wrong answer -> incorrect feedback; hint reveal shows hints in order; correct answer -> "Good work" toast & step-by-step solution available; completion screen shows score. | `test_platform_practice_session.py::test_full_practice_lifecycle_wrong_hints_correct_completion` | ✅ Ready |
| **AC-05** | **Session Randomization & Non-Mirroring**<br>Across repeated sessions of the same unit, both question order and option order differ (orders are not identical and do not mirror JSON order), while grading stays correct after shuffling. | `test_platform_randomization.py::test_session_question_and_option_shuffling_and_grading` | ✅ Ready |
| **AC-06** | **Multi-Type Grading & Math Equivalence**<br>Each interaction type graded correctly, including equivalent algebraic answers (`1-(alpha+n)*sigma` accepted for `1 - \alpha\sigma - n\sigma`; `0.5` accepted for `1/2`) and all-or-nothing for multiple-select. | `test_platform_grading_types.py::test_mcq_7_options_grading`<br>`test_platform_grading_types.py::test_fill_in_the_blank_math_equivalence`<br>`test_platform_grading_types.py::test_multiple_select_all_or_nothing` | ✅ Ready |
| **AC-07** | **Mastery Progression & Persistence**<br>Mastery level changes after practice and persists in LocalStorage after browser reload. | `test_platform_mastery_persistence.py::test_mastery_level_changes_and_persists_across_reloads` | ✅ Ready |
| **AC-08** | **Comprehensive Assessments**<br>Quiz, unit test, and course challenge (~30 questions drawn across units) can be started and completed. | `test_platform_assessments.py::test_quiz_and_unit_test_flow`<br>`test_platform_assessments.py::test_course_challenge_flow` | ✅ Ready |
| **AC-09** | **SVG Coordinate Plane Graph Rendering**<br>Question with graph renders Cartesian coordinate plane (verified via DOM/SVG elements: axes, curves, open/closed points). | `test_platform_graphs.py::test_coordinate_plane_svg_rendering` | ✅ Ready |
| **AC-10** | **Clean Console & Error Resilience**<br>No console errors during test run; all tests pass. | Monitored across all 14 tests in `conftest.py` page fixture. | ✅ Ready |
| **AC-11** | **3-Strikes Solution Reveal Safeguard**<br>Tracking consecutive wrong attempts; after 3 failures, locks inputs ("Maximum attempts reached 3/3"), reveals correct answer and step-by-step solution, and scores 0 credit. | `platform/src/components/PracticeSession.tsx`<br>`tests/test_platform.py` | ✅ Ready |
| **AC-12** | **Extended Math Equivalence & Comma Notation**<br>Accepts Spanish comma decimal notation (`0,8333` $\equiv$ `0.8333`), fraction conversions (`5/6` $\equiv$ `0,8333`), negative powers, and Greek variables. | `tests/test_math_adversarial_suite.mjs` (81 cases) | ✅ Ready |
| **VF-01** | **Visual Fidelity 6-State Capture**<br>Automated capture of all 6 platform states corresponding to reference screenshots for visual reviewer audit. | `test_visual_fidelity_capture.py::test_capture_six_canonical_states` | ✅ Ready |

---

## 4. Test Fixtures Inventory (`courses/test_fixtures/`)

1. **`valid_course_calculus.json`**:
   - Course ID: `test-differential-calculus`
   - Units: "Limits intro" (Skill) and "Derivative definitions" (Concept).
   - Features: 7-option MCQ with SVG coordinate plane ($[-7, 7] \times [-7, 7]$, curves, hole at $(3, -4)$); fill-in-the-blank with algebraic equivalence (`1-(alpha+n)*sigma`) and decimal/fraction equivalence (`0.5` for `1/2`); multiple-select with all-or-nothing grading (`["opt_a", "opt_c"]`).
2. **`valid_course_challenge.json`**:
   - Course ID: `test-course-challenge`
   - Units: 3 units across calculus foundations.
   - Questions: Exactly 30 questions evenly distributed across units to support unit quizzes, unit tests, and the comprehensive ~30-question Course Challenge.
3. **`invalid_corrupt_course.json`**:
   - Corrupted course JSON designed to test AC-02 fault-tolerant error isolation.

---

## 5. Visual Fidelity Artifact Output

Running `python -m pytest tests/e2e/test_visual_fidelity_capture.py` outputs the following screenshots to `tests/e2e/screenshots/`:
- `01_course_overview.png` (matches `Courser_overview.png`)
- `02_pre_exercise.png` (matches `pre_exercise.png`)
- `03_question_with_graph.png` (matches `multiple_answer_question.png`)
- `04_good_answer_toast.png` (matches `good_answer.png`)
- `05_exercise_complete_confetti.png` (matches `exercise_completed.png`)
- `06_course_challenge.png` (matches `course_challenge.png`)

These screenshots are ready for comparison by the Reviewer Agent against `Khan_academy_images_references/`.
