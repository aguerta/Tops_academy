"""Comprehensive Consolidated Test Suite for Practice Platform and Server.

Consolidates:
1. Client-Side Math Equivalence Engine Tests (6 adversarial categories, pass rate >= 98%, false positive prevention)
2. Platform Course Server & API Tests (validate_platform_course, scan_courses, HTTP endpoints, SPA fallback)
3. Launcher CLI Verification (run_platform.py --scan and --help)
"""
from __future__ import annotations

import json
import socket
import subprocess
import sys
import threading
import time
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import run_platform
from run_platform import (
    PlatformRequestHandler,
    scan_courses,
    validate_platform_course,
)

NODE_SCRIPT = REPO_ROOT / "tests" / "test_math_adversarial_suite.mjs"
RESULTS_PATH = REPO_ROOT / "tests" / "math_adversarial_results.json"


# =============================================================================
# 1. Math Equivalence Engine Tests
# =============================================================================

def run_node_adversarial_suite() -> dict:
    """Executes the compiled math equivalence test suite via Node.js."""
    assert NODE_SCRIPT.is_file(), f"Node script not found at {NODE_SCRIPT}"
    cmd = ["node", str(NODE_SCRIPT)]
    res = subprocess.run(
        cmd,
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False
    )
    assert res.returncode == 0, f"Node suite crashed: {res.stderr}\nOutput: {res.stdout}"
    assert RESULTS_PATH.exists(), "math_adversarial_results.json was not generated"

    with open(RESULTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def suite_results():
    """Runs the Node test suite once and provides results to all tests in this module."""
    return run_node_adversarial_suite()


class TestMathEquivalenceEngine:
    """Parametrized verification of math equivalence across all 6 core dimensions."""

    def test_overall_pass_rate_above_98_percent(self, suite_results):
        total = suite_results["total"]
        passed = suite_results["passed"]
        rate = passed / total
        assert rate >= 0.98, f"Pass rate {rate:.2%} ({passed}/{total}) below 98% threshold!"

    def test_algebraic_equivalence_all_pass(self, suite_results):
        alg_cases = [r for r in suite_results["results"] if r["category"] == "Algebraic Equivalence"]
        assert len(alg_cases) >= 10, f"Expected at least 10 algebraic test cases, got {len(alg_cases)}"
        for tc in alg_cases:
            assert tc["passed"] is True, f"Failed {tc['id']}: {tc['name']} ({tc.get('details', '')})"

    def test_number_equivalence_all_pass(self, suite_results):
        num_cases = [r for r in suite_results["results"] if r["category"] == "Number Equivalence"]
        assert len(num_cases) >= 10
        for tc in num_cases:
            assert tc["passed"] is True, f"Failed {tc['id']}: {tc['name']} ({tc.get('details', '')})"

    def test_fractions_and_powers_all_pass(self, suite_results):
        frac_cases = [r for r in suite_results["results"] if r["category"] == "Fractions and Powers"]
        assert len(frac_cases) >= 8
        for tc in frac_cases:
            assert tc["passed"] is True, f"Failed {tc['id']}: {tc['name']} ({tc.get('details', '')})"

    def test_commutativity_and_greek_all_pass(self, suite_results):
        greek_cases = [r for r in suite_results["results"] if r["category"] == "Commutativity & Greek"]
        assert len(greek_cases) >= 8
        for tc in greek_cases:
            assert tc["passed"] is True, f"Failed {tc['id']}: {tc['name']} ({tc.get('details', '')})"

    def test_false_positive_prevention_100_percent_pass(self, suite_results):
        false_cases = [r for r in suite_results["results"] if r["category"] == "False Positive Prevention"]
        assert len(false_cases) >= 10
        for tc in false_cases:
            assert tc["passed"] is True, f"False Positive in {tc['id']}: {tc['name']} was marked equivalent!"

    def test_boundary_and_malformed_inputs_robustness(self, suite_results):
        bound_cases = [r for r in suite_results["results"] if r["category"] == "Boundary & Malformed"]
        assert len(bound_cases) >= 8
        for tc in bound_cases:
            assert tc["passed"] is True, f"Crash/Error in boundary test {tc['id']}: {tc['name']}"


# =============================================================================
# 2. Platform Server Validation & Course Discovery Tests
# =============================================================================

class TestPlatformServerLogic:
    """Tests for course validation and scanning logic in run_platform.py."""

    def test_validate_platform_course_valid(self):
        sample = {
            "course_id": "test_c",
            "title": "Test Course",
            "competencies": [{"id": "Hab-01", "name": "Skill 1"}],
            "questions": [
                {
                    "id": "Q-1",
                    "interaction_type": "multiple_choice_7_options",
                    "stem": "Solve for x",
                    "options": [{"id": "A", "content": "1", "is_correct": True}],
                }
            ],
        }
        is_valid, payload = validate_platform_course(json.dumps(sample))
        assert is_valid is True
        assert isinstance(payload, dict)

    def test_validate_platform_course_catches_control_characters(self):
        corrupted = '{"course_id": "test", "title": "Test\x0cCourse", "competencies": [], "questions": []}'
        is_valid, msg = validate_platform_course(corrupted)
        assert is_valid is False
        assert "control characters" in str(msg).lower() or "unescaped" in str(msg).lower()

    def test_validate_platform_course_missing_fields(self):
        missing_title = '{"course_id": "test", "competencies": [{"id": "H-1"}], "questions": [{"id": "Q-1", "interaction_type": "fill_in_the_blank"}]}'
        is_valid, msg = validate_platform_course(missing_title)
        assert is_valid is False
        assert "title" in str(msg).lower()

    def test_scan_courses_discovers_pde_and_courses(self):
        courses = scan_courses()
        course_ids = [c.get("id") for c in courses]
        assert len(course_ids) >= 1, "No courses found by scan_courses"

        first_record = courses[0]
        assert first_record.get("status") == "valid"
        assert first_record.get("total_questions", 0) >= 100

        if "demo_course" in course_ids:
            demo_record = next(c for c in courses if c.get("id") == "demo_course")
            assert demo_record.get("status") == "valid"
            assert demo_record.get("total_questions", 0) >= 200


# =============================================================================
# 3. Live HTTP Server API Endpoints Tests
# =============================================================================

@pytest.fixture(scope="module")
def live_server():
    """Spawns an ephemeral platform server on port 0 for testing endpoints."""
    # Find a free port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]

    httpd = ThreadingHTTPServer(("127.0.0.1", port), PlatformRequestHandler)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()
    time.sleep(0.1)

    yield f"http://127.0.0.1:{port}"

    httpd.shutdown()
    httpd.server_close()


class TestPlatformServerEndpoints:
    """Verifies all REST API endpoints and static SPA routing."""

    def test_api_courses_endpoint(self, live_server):
        url = f"{live_server}/api/courses"
        req = Request(url)
        with urlopen(req) as resp:
            assert resp.status == 200
            assert "application/json" in resp.headers.get("Content-Type", "")
            data = json.loads(resp.read().decode("utf-8"))
            assert "courses" in data
            course_ids = [c["id"] for c in data["courses"]]
            assert len(course_ids) >= 1

    def test_api_course_detail_valid_course(self, live_server):
        courses = scan_courses()
        first_id = courses[0]["id"]
        url = f"{live_server}/api/courses/{first_id}"
        with urlopen(url) as resp:
            assert resp.status == 200
            data = json.loads(resp.read().decode("utf-8"))
            assert data.get("course_id") == first_id
            assert "competencies" in data
            assert len(data.get("questions", [])) >= 100

    def test_api_course_detail_optional_demo(self, live_server):
        url = f"{live_server}/api/courses/demo_course"
        try:
            with urlopen(url) as resp:
                assert resp.status == 200
                data = json.loads(resp.read().decode("utf-8"))
                assert data.get("course_id") == "demo_course"
                assert len(data.get("questions", [])) >= 200
        except HTTPError as e:
            assert e.code == 404

    def test_api_course_detail_not_found(self, live_server):
        url = f"{live_server}/api/courses/nonexistent_course_404"
        with pytest.raises(HTTPError) as exc_info:
            urlopen(url)
        assert exc_info.value.code == 404

    def test_cors_options_preflight(self, live_server):
        url = f"{live_server}/api/courses"
        req = Request(url, method="OPTIONS")
        with urlopen(req) as resp:
            assert resp.status == 204
            assert resp.headers.get("Access-Control-Allow-Origin") == "*"

    def test_static_frontend_serving_and_spa_fallback(self, live_server):
        # GET / should return index.html
        url_root = f"{live_server}/"
        with urlopen(url_root) as resp:
            assert resp.status == 200
            body = resp.read().decode("utf-8")
            assert "<!DOCTYPE html>" in body or "<div id=\"root\">" in body or "html" in body.lower()

        # SPA Route fallback /course/pde_course should return index.html
        url_spa = f"{live_server}/course/pde_course"
        with urlopen(url_spa) as resp:
            assert resp.status == 200
            body = resp.read().decode("utf-8")
            assert "html" in body.lower()


# =============================================================================
# 4. Single-Command Launcher CLI Flags
# =============================================================================

class TestLauncherCLI:
    """Verifies python run_platform.py command-line options."""

    def test_launcher_scan_flag(self):
        proc = subprocess.run(
            [sys.executable, "run_platform.py", "--scan"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True
        )
        assert proc.returncode == 0
        stdout = proc.stdout
        assert "VALID" in stdout

    def test_launcher_help_flag(self):
        proc = subprocess.run(
            [sys.executable, "run_platform.py", "--help"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True
        )
        assert proc.returncode == 0
        stdout = proc.stdout
        assert "--port" in stdout
        assert "--host" in stdout
        assert "--scan" in stdout
