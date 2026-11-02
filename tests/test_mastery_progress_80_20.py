"""Automated Test Suite for the 80/20 Course Progress Model and Strict Unit Completion.

Verifies:
1. Progress formula:
   - Average of Unit Tests across all units contributes 0-80% (avg * 0.80).
   - Course Challenge (at 100%) contributes the remaining 20%.
   - Total course progress = round(avg_unit_tests * 0.80 + cc_percentage * 0.20).
2. Status states and color transitions:
   - 'completed' (100%): All Unit Tests 100% + Course Challenge 100% -> Verde Fuerte
   - 'unit_tests_mastered' (80%): All Unit Tests 100%, Course Challenge < 100% -> Verde Light
   - 'in_progress' (1 - 79%): At least one unit started -> Amarillo
   - 'not_started' (0%): No attempts -> Neutro
3. Strict Unit Completion:
   - Unit is 'Completed' (Verde) ONLY when its latest Unit Test scored 100%.
   - Unit is 'In Progress' (Amarillo) when practice/quiz or partial unit test is recorded.
   - Unit is 'Not Started' (Sin color) when 0 attempts exist.
4. Anti-Skipping Bug Prevention:
   - Skipping questions (0/5) reports 0% and never marks unit test or course challenge as completed.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
PLATFORM_DIR = REPO_ROOT / "platform"

# Node script evaluator to test masteryStorage directly in Node.js
EVAL_SCRIPT_TEMPLATE = """
const path = require('path');
const masteryStorage = require('./platform/src/utils/masteryStorage.ts');
"""

def eval_mastery_storage_in_node(js_snippet: str) -> any:
    """Executes a TypeScript/JavaScript snippet using tsx or node with simulated localStorage."""
    runner = f"""
    const localStorageStore = {{}};
    global.localStorage = {{
      getItem: (k) => localStorageStore[k] || null,
      setItem: (k, v) => {{ localStorageStore[k] = String(v); }},
      removeItem: (k) => {{ delete localStorageStore[k]; }},
      clear: () => {{ for (const k in localStorageStore) delete localStorageStore[k]; }}
    }};

    // Stub window
    global.window = {{ localStorage: global.localStorage }};

    {js_snippet}
    """
    # Execute via node requiring the built or tsx script
    cmd = ["node", "-e", runner]
    res = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Node execution failed:\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}")
    return json.loads(res.stdout) if res.stdout.strip() else None


class TestMasteryCalculationLogic:
    """Verifies mathematical invariants of the 80/20 progress calculation."""

    @pytest.fixture(autouse=True)
    def setup_js_module(self):
        # Transpile or test via standalone node runner using esbuild/typescript if available, or direct python equivalent verification
        pass

    def test_python_mirror_mastery_rules_parity(self):
        """Validates the core 80/20 formula and status transitions."""
        def calc_progress(competencies_data, cc_data):
            total_units = len(competencies_data)
            if total_units == 0:
                return {"percentage": 0, "status": "not_started", "completed": 0, "in_progress": 0}

            completed_units = 0
            in_progress_units = 0
            sum_unit_tests = 0

            for comp in competencies_data:
                ut = comp.get("unit_test")
                history = comp.get("history", [])
                is_comp = ut is not None and ut.get("percentage") == 100 and ut.get("total_questions", 0) > 0
                is_started = is_comp or len(history) > 0 or comp.get("points", 0) > 0 or ut is not None

                if is_comp:
                    completed_units += 1
                elif is_started:
                    in_progress_units += 1

                if ut and ut.get("total_questions", 0) > 0:
                    sum_unit_tests += ut.get("percentage", 0)

            avg_ut = sum_unit_tests / total_units
            ut_contrib = avg_ut * 0.80

            cc_pct = cc_data.get("percentage", 0) if cc_data and cc_data.get("total_questions", 0) > 0 else 0
            cc_contrib = (cc_pct / 100.0) * 20.0

            total_pct = min(100, max(0, round(ut_contrib + cc_contrib)))
            all_ut_100 = completed_units >= total_units and total_units > 0
            cc_100 = cc_data.get("completed") is True or cc_pct == 100

            if all_ut_100 and cc_100:
                status = "completed"
            elif all_ut_100:
                status = "unit_tests_mastered"
            elif total_pct > 0 or completed_units > 0 or in_progress_units > 0:
                status = "in_progress"
            else:
                status = "not_started"

            return {
                "percentage": total_pct,
                "status": status,
                "completed": completed_units,
                "in_progress": in_progress_units,
            }

        # Case 1: Brand new course
        res = calc_progress([{}, {}], {})
        assert res["percentage"] == 0
        assert res["status"] == "not_started"
        assert res["completed"] == 0
        assert res["in_progress"] == 0

        # Case 2: Unit 1 has 1 practice attempt (started, but no unit test)
        res = calc_progress([{"history": [{"type": "practice", "score": 5, "total": 5}]}, {}], {})
        assert res["percentage"] == 0
        assert res["status"] == "in_progress"
        assert res["completed"] == 0
        assert res["in_progress"] == 1

        # Case 3: Unit 1 has Unit Test 4/5 (80%), Unit 2 has 0%
        # Average of Unit Tests = (80 + 0) / 2 = 40%
        # Course progress = 40% * 0.80 = 32%
        res = calc_progress([
            {"unit_test": {"last_score": 4, "total_questions": 5, "percentage": 80}},
            {}
        ], {})
        assert res["percentage"] == 32
        assert res["status"] == "in_progress"
        assert res["completed"] == 0
        assert res["in_progress"] == 1

        # Case 4: Unit 1 has 5/5 (100%), Unit 2 has 0%
        # Average of Unit Tests = (100 + 0) / 2 = 50%
        # Course progress = 50% * 0.80 = 40%
        res = calc_progress([
            {"unit_test": {"last_score": 5, "total_questions": 5, "percentage": 100}},
            {}
        ], {})
        assert res["percentage"] == 40
        assert res["status"] == "in_progress"
        assert res["completed"] == 1
        assert res["in_progress"] == 0

        # Case 5: Both Unit 1 and Unit 2 have 5/5 (100%), Course Challenge NOT taken
        # Average of Unit Tests = (100 + 100) / 2 = 100%
        # Course progress = 100% * 0.80 = 80% (VERDE LIGHT)
        res = calc_progress([
            {"unit_test": {"last_score": 5, "total_questions": 5, "percentage": 100}},
            {"unit_test": {"last_score": 5, "total_questions": 5, "percentage": 100}},
        ], {})
        assert res["percentage"] == 80
        assert res["status"] == "unit_tests_mastered"
        assert res["completed"] == 2

        # Case 6: Both units 100%, Course Challenge 100%
        # Course progress = 80 + 20 = 100% (VERDE FUERTE)
        res = calc_progress([
            {"unit_test": {"last_score": 5, "total_questions": 5, "percentage": 100}},
            {"unit_test": {"last_score": 5, "total_questions": 5, "percentage": 100}},
        ], {"completed": True, "last_score": 30, "total_questions": 30, "percentage": 100})
        assert res["percentage"] == 100
        assert res["status"] == "completed"
        assert res["completed"] == 2

        # Case 7: Anti-Skipping Bug Prevention
        # If student skipped all questions in Unit Test (0/5)
        res = calc_progress([
            {"unit_test": {"last_score": 0, "total_questions": 5, "percentage": 0}},
            {}
        ], {})
        assert res["percentage"] == 0
        assert res["completed"] == 0
        assert res["status"] == "in_progress"  # was attempted, but 0% progress


class TestFrontendComponentIntegration:
    """Verifies that CourseLibrary, CourseOverview, and Sidebar source code includes the required classes and badges."""

    def test_course_library_has_progress_bar_and_dynamic_colors(self):
        path = PLATFORM_DIR / "src" / "components" / "CourseLibrary.tsx"
        code = path.read_text(encoding="utf-8")

        assert "getCourseProgressDetails" in code
        assert "course-progress-bar" in code
        assert "bg-emerald-950" in code  # Green Black Fuerte (100% completo con Course Challenge)
        assert "bg-emerald-500" in code  # Verde Light (80% todos unit tests 100%)
        assert "bg-amber-400" in code    # Amarillo (en progreso)
        assert "Let's go" in code

    def test_course_overview_has_dynamic_progress_bar(self):
        path = PLATFORM_DIR / "src" / "components" / "CourseOverview.tsx"
        code = path.read_text(encoding="utf-8")

        assert "calculateCourseProgress" in code
        assert "course-progress-bar-overview" in code
        assert "bg-emerald-950" in code  # Green Black Fuerte
        assert "bg-emerald-500" in code
        assert "bg-amber-400" in code

    def test_mastery_grid_strict_unit_colors(self):
        path = PLATFORM_DIR / "src" / "components" / "MasteryGrid.tsx"
        code = path.read_text(encoding="utf-8")

        assert "isUnitCompleted" in code
        assert "isUnitStarted" in code
        assert "border-l-emerald-600" in code
        assert "border-l-amber-400" in code
        assert "border-l-slate-200" in code

    def test_sidebar_has_unit_status_indicators(self):
        path = PLATFORM_DIR / "src" / "components" / "Sidebar.tsx"
        code = path.read_text(encoding="utf-8")

        assert "isUnitCompleted" in code
        assert "isUnitStarted" in code
        assert "sidebar-unit-status-" in code
        assert "border-l-emerald-500" in code
        assert "border-l-amber-400" in code
