"""Tests for Course API Slim Manifest and Caching (Frente B).

Validates Acceptance Criteria AC-19, AC-22, AC-24, AC-25:
1. `platform/server/courseIndex.cjs`:
   - getManifest() returns { generated_at, courses }
   - JSON payload is < 50 KB (target < 10 KB)
   - NO element in courses contains 'data'
   - Required fields exist: id, filename, title, description, status,
     total_competencies, total_questions, bytes, etag
   - getCourseData(id) returns full course with questions for valid course
   - buildIndex() executes in < 100 ms when cache is warm
   - Corrupted JSON (syntax error or control chars) is reported as status: "error"
     without crashing or corrupting valid courses
2. HTTP Server (`courseServer.cjs`):
   - GET /api/courses and GET /api/courses.json return slim manifest with ETag
   - GET /api/courses/:id returns single course with ETag
   - Request with matching If-None-Match returns 304 Not Modified
   - GET /healthz returns 200 with status and metrics
3. Build and Templates:
   - platform/index.html contains <!--COURSE_MANIFEST--> or <script id="course-manifest"
   - dist/api/courses.json weighs < 100 KB and contains no embedded 'data'
"""
from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
PLATFORM_DIR = REPO_ROOT / "platform"
SERVER_DIR = PLATFORM_DIR / "server"
COURSE_INDEX_PATH = SERVER_DIR / "courseIndex.cjs"
COURSE_SERVER_PATH = SERVER_DIR / "courseServer.cjs"


# =============================================================================
# Helper: Node script evaluator for courseIndex.cjs
# =============================================================================

def run_node_eval(expr: str) -> any:
    """Executes a JS snippet in Node requiring courseIndex.cjs and returning parsed JSON output."""
    course_index_str = COURSE_INDEX_PATH.as_posix()
    script = f"""
    const path = require('path');
    const courseIndex = require('{course_index_str}');
    try {{
      const result = (function() {{ {expr} }})();
      process.stdout.write(JSON.stringify(result));
    }} catch (err) {{
      process.stderr.write(err.stack || err.message);
      process.exit(1);
    }}
    """
    res = subprocess.run(
        ["node", "-"],
        input=script,
        text=True,
        encoding="utf-8",
        capture_output=True,
        cwd=str(REPO_ROOT),
        check=False,
    )
    if res.returncode != 0:
        raise RuntimeError(
            f"Node evaluation failed (code {res.returncode}):\n{res.stderr}\nScript:\n{script}"
        )
    return json.loads(res.stdout)


# =============================================================================
# 1. Verification of platform/server/courseIndex.cjs Contract
# =============================================================================

class TestCourseIndexContract:
    """Rigorous contract verification of courseIndex.cjs."""

    def test_course_index_file_exists(self):
        assert COURSE_INDEX_PATH.is_file(), f"courseIndex.cjs not found at {COURSE_INDEX_PATH}"

    def test_get_manifest_structure_and_size(self):
        """Validates AC-19: manifest < 50 KB, slim schema without 'data'."""
        manifest = run_node_eval("return courseIndex.getManifest();")

        assert isinstance(manifest, dict), "getManifest() must return an object"
        assert "courses" in manifest, "Manifest missing 'courses' field"
        assert isinstance(manifest["courses"], list), "'courses' must be a list"
        assert len(manifest["courses"]) >= 1, "Expected at least 1 course in manifest"

        # Check total JSON size
        manifest_json = json.dumps(manifest)
        json_bytes = len(manifest_json.encode("utf-8"))
        assert json_bytes < 50 * 1024, (
            f"Manifest size {json_bytes} bytes exceeds 50 KB threshold (AC-19)"
        )

        # Expected target is < 10 KB
        assert json_bytes < 10 * 1024, (
            f"Manifest size {json_bytes} bytes exceeds 10 KB target"
        )

        # Validate course items schema
        required_fields = {
            "id",
            "filename",
            "title",
            "description",
            "status",
            "total_competencies",
            "total_questions",
            "bytes",
            "etag",
        }

        for c in manifest["courses"]:
            # Strict criterion: NO element has 'data'
            assert "data" not in c, f"Course '{c.get('id')}' must NOT contain 'data' field"

            # Check presence of all required fields
            for field in required_fields:
                assert field in c, f"Course item missing required field '{field}': {c}"

            # Type and sanity checks
            assert isinstance(c["id"], str) and len(c["id"]) > 0
            assert isinstance(c["filename"], str) and c["filename"].endswith(".json")
            assert isinstance(c["title"], str) and len(c["title"]) > 0
            assert c["status"] in ("valid", "error")
            assert isinstance(c["total_competencies"], int)
            assert isinstance(c["total_questions"], int)
            assert isinstance(c["bytes"], int)
            assert isinstance(c["etag"], str) and len(c["etag"]) > 0

    def test_get_course_data_valid_course(self):
        """Verifies getCourseData(id) returns full course with questions."""
        manifest = run_node_eval("return courseIndex.getManifest();")
        valid_courses = [c for c in manifest["courses"] if c["status"] == "valid"]
        assert len(valid_courses) > 0, "No valid courses found in manifest"

        first_id = valid_courses[0]["id"]
        result = run_node_eval(f"return courseIndex.getCourseData('{first_id}');")

        assert result is not None, f"getCourseData('{first_id}') returned null"
        assert result.get("status") == "valid"
        assert result.get("etag") is not None
        assert "data" in result, "getCourseData result must include 'data'"

        course_data = result["data"]
        assert isinstance(course_data, dict)
        assert course_data.get("course_id") == first_id or course_data.get("id") == first_id
        assert "competencies" in course_data
        assert isinstance(course_data["competencies"], list)
        assert len(course_data["competencies"]) > 0
        assert "questions" in course_data
        assert isinstance(course_data["questions"], list)
        assert len(course_data["questions"]) > 0

    def test_build_index_warm_cache_performance(self):
        """Validates AC-19: buildIndex() executes in < 100 ms when cache is warm."""
        # Warm up the cache once
        run_node_eval("return courseIndex.buildIndex();")

        # Measure warm buildIndex() execution time
        stats_and_time = run_node_eval(
            """
            courseIndex.resetStats();
            const t0 = Date.now();
            courseIndex.buildIndex();
            const elapsed = Date.now() - t0;
            return { elapsed, stats: courseIndex.getStats() };
            """
        )

        elapsed_ms = stats_and_time["elapsed"]
        assert elapsed_ms < 100, (
            f"buildIndex() warm execution time {elapsed_ms}ms exceeded 100 ms threshold"
        )

        # Also verify cache hits were used
        stats = stats_and_time["stats"]
        assert stats.get("cachedHits", 0) > 0, "Warm buildIndex should record cache hits"
        assert stats.get("parseCount", 0) == 0, "Warm buildIndex should not reparse files"

    def test_corrupted_json_handled_gracefully(self, tmp_path):
        """Validates AC-25: malformed JSON reports status: 'error' without crashing."""
        temp_courses_dir = tmp_path / "courses"
        temp_courses_dir.mkdir()
        temp_cache_file = tmp_path / "cache.json"

        # 1. A valid course
        valid_json = {
            "course_id": "clean_course",
            "title": "Clean Valid Course",
            "description": "A well formed course",
            "competencies": ["comp_1"],
            "questions": [
                {
                    "id": "q1",
                    "type": "multiple_choice_7_options",
                    "question": "What is 1+1?",
                    "options": ["1", "2", "3", "4", "5", "6", "7"],
                    "correct_answer": "2",
                }
            ],
        }
        (temp_courses_dir / "clean_course.json").write_text(
            json.dumps(valid_json), encoding="utf-8"
        )

        # 2. A malformed syntax JSON
        (temp_courses_dir / "broken_syntax.json").write_text(
            '{"title": "Broken", "course_id": "broken", invalid_syntax...',
            encoding="utf-8",
        )

        # 3. A JSON with illegal control character
        corrupt_raw = '{"course_id": "ctrl_char", "title": "Ctrl \x07 Char", "competencies": ["c"], "questions": []}'
        (temp_courses_dir / "broken_control.json").write_text(
            corrupt_raw, encoding="utf-8"
        )

        courses_dir_posix = temp_courses_dir.as_posix()
        cache_file_posix = temp_cache_file.as_posix()

        eval_code = f"""
        const res = courseIndex.buildIndex({{
          coursesDir: '{courses_dir_posix}',
          cacheFile: '{cache_file_posix}',
          force: true
        }});
        return res.entries;
        """
        entries = run_node_eval(eval_code)

        assert isinstance(entries, dict)
        assert len(entries) == 3, f"Expected 3 entries in index, got {len(entries)}"

        # Clean course must be valid
        clean_entry = entries.get("clean_course.json")
        assert clean_entry is not None
        assert clean_entry["status"] == "valid"
        assert clean_entry["total_questions"] == 1

        # Broken syntax must be flagged as error
        broken_syntax_entry = entries.get("broken_syntax.json")
        assert broken_syntax_entry is not None
        assert broken_syntax_entry["status"] == "error"
        assert broken_syntax_entry["error_message"] is not None
        assert "syntax" in broken_syntax_entry["error_message"].lower()

        # Broken control char must be flagged as error
        broken_ctrl_entry = entries.get("broken_control.json")
        assert broken_ctrl_entry is not None
        assert broken_ctrl_entry["status"] == "error"
        assert broken_ctrl_entry["error_message"] is not None


# =============================================================================
# 2. Verification of Live HTTP Server (courseServer.cjs)
# =============================================================================

@pytest.fixture(scope="module")
def live_course_server():
    """Spawns an ephemeral instance of courseServer.cjs on an open port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]

    env = os.environ.copy()
    env["PORT"] = str(port)

    proc = subprocess.Popen(
        ["node", str(COURSE_SERVER_PATH)],
        cwd=str(REPO_ROOT),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    base_url = f"http://127.0.0.1:{port}"
    deadline = time.time() + 8.0
    ready = False

    while time.time() < deadline:
        if proc.poll() is not None:
            stdout, stderr = proc.communicate()
            raise RuntimeError(
                f"courseServer.cjs terminated prematurely (code {proc.returncode}):\n{stderr}\n{stdout}"
            )
        try:
            req = Request(f"{base_url}/healthz")
            with urlopen(req, timeout=1.0) as resp:
                if resp.status == 200:
                    ready = True
                    break
        except Exception:
            time.sleep(0.1)

    if not ready:
        proc.kill()
        stdout, stderr = proc.communicate()
        raise TimeoutError(f"courseServer.cjs did not become ready in 8s:\n{stderr}\n{stdout}")

    yield base_url

    proc.terminate()
    try:
        proc.wait(timeout=3.0)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()


class TestCourseServerHttp:
    """Verifies HTTP endpoints, caching, ETags, and 304 handling."""

    def test_get_api_courses_and_courses_json_slim(self, live_course_server):
        """Verifies GET /api/courses and GET /api/courses.json return slim manifest with ETag."""
        endpoints = ["/api/courses", "/api/courses.json"]

        for ep in endpoints:
            url = f"{live_course_server}{ep}"
            req = Request(url)
            with urlopen(req, timeout=5.0) as resp:
                assert resp.status == 200
                assert "application/json" in resp.headers.get("Content-Type", "")

                etag = resp.headers.get("ETag")
                assert etag is not None and len(etag) > 0, f"Missing ETag on {ep}"

                body = resp.read()
                assert len(body) < 50 * 1024, f"Payload on {ep} exceeds 50 KB"

                data = json.loads(body.decode("utf-8"))
                assert "courses" in data
                assert isinstance(data["courses"], list)
                assert len(data["courses"]) >= 1

                for c in data["courses"]:
                    assert "data" not in c, f"Found unexpected 'data' in course {c.get('id')} from {ep}"

    def test_get_single_course_detail_with_etag(self, live_course_server):
        """Verifies GET /api/courses/:id returns single course with ETag."""
        # 1. Fetch manifest to find a valid course ID
        url_manifest = f"{live_course_server}/api/courses"
        with urlopen(url_manifest) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            valid_courses = [c for c in data["courses"] if c["status"] == "valid"]
            assert len(valid_courses) > 0

        first_course = valid_courses[0]
        course_id = first_course["id"]

        # 2. Fetch single course
        url_course = f"{live_course_server}/api/courses/{course_id}"
        req = Request(url_course)
        with urlopen(req, timeout=5.0) as resp:
            assert resp.status == 200
            assert "application/json" in resp.headers.get("Content-Type", "")

            etag = resp.headers.get("ETag")
            assert etag is not None and len(etag) > 0

            body = resp.read()
            course_obj = json.loads(body.decode("utf-8"))
            assert course_obj.get("course_id") == course_id or course_obj.get("id") == course_id
            assert "questions" in course_obj
            assert len(course_obj["questions"]) > 0

    def test_conditional_if_none_match_returns_304(self, live_course_server):
        """Verifies AC-22: matching If-None-Match header returns 304 Not Modified."""
        # Test on manifest endpoint
        manifest_url = f"{live_course_server}/api/courses"
        req1 = Request(manifest_url)
        with urlopen(req1) as resp1:
            etag = resp1.headers.get("ETag")
            assert etag is not None

        # Request again with If-None-Match
        req2 = Request(manifest_url, headers={"If-None-Match": etag})
        try:
            with urlopen(req2) as resp2:
                assert resp2.status == 304
        except HTTPError as err:
            assert err.code == 304, f"Expected 304 Not Modified, got {err.code}"

        # Test on single course endpoint
        with urlopen(manifest_url) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            first_id = data["courses"][0]["id"]

        detail_url = f"{live_course_server}/api/courses/{first_id}"
        with urlopen(detail_url) as resp_det:
            detail_etag = resp_det.headers.get("ETag")
            assert detail_etag is not None

        req_detail_cond = Request(detail_url, headers={"If-None-Match": detail_etag})
        try:
            with urlopen(req_detail_cond) as resp_det304:
                assert resp_det304.status == 304
        except HTTPError as err:
            assert err.code == 304, f"Expected 304 Not Modified on course detail, got {err.code}"

    def test_healthz_endpoint(self, live_course_server):
        """Verifies /healthz endpoint uptime and metrics."""
        url = f"{live_course_server}/healthz"
        with urlopen(url) as resp:
            assert resp.status == 200
            data = json.loads(resp.read().decode("utf-8"))
            assert data.get("status") == "ok"
            assert "pid" in data
            assert "uptime_seconds" in data
            assert data.get("courses_count", 0) >= 1

    def test_non_existent_course_returns_404(self, live_course_server):
        """Verifies requesting non-existent course returns 404."""
        url = f"{live_course_server}/api/courses/does_not_exist_404"
        with pytest.raises(HTTPError) as exc_info:
            urlopen(url)
        assert exc_info.value.code == 404


# =============================================================================
# 3. Verification of Build Artifacts and Templates
# =============================================================================

class TestBuildAndTemplates:
    """Verifies index.html template and dist/ build artifacts."""

    def test_platform_index_html_contains_manifest_marker_or_script(self):
        """Verifies platform/index.html includes <!--COURSE_MANIFEST--> or the manifest script."""
        index_html_path = PLATFORM_DIR / "index.html"
        assert index_html_path.is_file(), f"index.html not found at {index_html_path}"
        content = index_html_path.read_text(encoding="utf-8")

        has_marker = "<!--COURSE_MANIFEST-->" in content
        has_script = '<script id="course-manifest" type="application/json">' in content

        assert has_marker or has_script, (
            "platform/index.html must contain either '<!--COURSE_MANIFEST-->' "
            "or '<script id=\"course-manifest\" type=\"application/json\">'"
        )

    def test_dist_api_courses_json_slim_and_no_data(self):
        """Validates AC-24: dist/api/courses.json < 100 KB and contains no embedded data."""
        dist_manifest = PLATFORM_DIR / "dist" / "api" / "courses.json"

        # If dist has not been generated, trigger build
        if not dist_manifest.exists():
            subprocess.run(
                ["npm", "run", "build"],
                cwd=str(PLATFORM_DIR),
                shell=True,
                check=True,
            )

        assert dist_manifest.is_file(), f"dist/api/courses.json not found at {dist_manifest}"

        file_size = dist_manifest.stat().st_size
        assert file_size < 100 * 1024, (
            f"dist/api/courses.json is {file_size} bytes (exceeds 100 KB limit; previous was ~59 MB)"
        )

        content = dist_manifest.read_text(encoding="utf-8")
        parsed = json.loads(content)

        assert "courses" in parsed, "dist/api/courses.json missing 'courses' field"
        assert isinstance(parsed["courses"], list)

        for c in parsed["courses"]:
            assert "data" not in c, (
                f"dist/api/courses.json course '{c.get('id')}' contains embedded 'data' field!"
            )
