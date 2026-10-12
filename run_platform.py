#!/usr/bin/env python3
"""Run Platform - Single launcher for the Top's Academy practice platform.

Starts the application on port 5173 (or 3000) and serves both the dynamic
course discovery API and the frontend application.
"""
from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import sys
import threading
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent
COURSES_DIR = ROOT_DIR / "courses"
PLATFORM_DIR = ROOT_DIR / "platform"
DIST_DIR = PLATFORM_DIR / "dist"

# Ensure MIME types are properly initialized
mimetypes.init()
mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("text/javascript", ".js")
mimetypes.add_type("text/css", ".css")
mimetypes.add_type("image/svg+xml", ".svg")
mimetypes.add_type("font/woff2", ".woff2")


def validate_platform_course(content: str) -> tuple[bool, dict | str]:
    """Validate a course JSON string for platform runtime compatibility."""
    # Pass 1: Raw lexical check for corrupted LaTeX escapes / silent control characters
    control_char_regex = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
    if control_char_regex.search(content):
        return False, "Contains unescaped control characters or corrupted LaTeX escapes"

    # Pass 2: JSON Syntax check
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON syntax at line {e.lineno}, col {e.colno}: {e.msg}"

    if not isinstance(data, dict):
        return False, "Course root element must be a JSON object"

    # Pass 3: Required metadata check
    course_id = data.get("course_id")
    if not course_id or not isinstance(course_id, str):
        return False, "Missing or invalid 'course_id' string"

    title = data.get("title") or data.get("course_title")
    if not title or not isinstance(title, str):
        return False, "Missing or invalid course 'title'"

    competencies = data.get("competencies")
    if not isinstance(competencies, list) or len(competencies) == 0:
        return False, "Course must specify non-empty 'competencies' array"

    questions = data.get("questions")
    if not isinstance(questions, list) or len(questions) == 0:
        return False, "Course must specify non-empty 'questions' array"

    # Pass 4: Question type validity
    valid_types = {"multiple_choice_7_options", "multiple_select", "fill_in_the_blank"}
    for q in questions:
        if not isinstance(q, dict):
            return False, "Question items must be JSON objects"
        q_type = q.get("type") or q.get("interaction_type")
        if q_type not in valid_types:
            return False, f"Invalid question type '{q_type}'"

    return True, data


def scan_courses() -> list[dict]:
    """Dynamically scan courses/ directory and return all discovered course records."""
    if not COURSES_DIR.exists():
        return []

    course_files = [f for f in COURSES_DIR.iterdir() if f.is_file() and f.suffix.lower() == ".json"]
    # Sort files deterministically
    course_files.sort(key=lambda p: p.name)

    results: list[dict] = []
    for f in course_files:
        try:
            content = f.read_text(encoding="utf-8")
            is_valid, payload = validate_platform_course(content)

            if is_valid and isinstance(payload, dict):
                results.append({
                    "id": payload.get("course_id"),
                    "filename": f.name,
                    "title": payload.get("title") or payload.get("course_title", f.stem),
                    "description": payload.get("description", ""),
                    "status": "valid",
                    "total_competencies": len(payload.get("competencies", [])),
                    "total_questions": len(payload.get("questions", [])),
                    "data": payload,
                })
            else:
                # Attempt to extract title for display on error card
                fallback_title = f.stem
                try:
                    partial = json.loads(content)
                    if isinstance(partial, dict) and (partial.get("title") or partial.get("course_title")):
                        fallback_title = str(partial.get("title") or partial.get("course_title"))
                except Exception:
                    pass

                results.append({
                    "id": f.stem,
                    "filename": f.name,
                    "title": fallback_title,
                    "description": "Corrupted or malformed course file",
                    "status": "error",
                    "error_message": str(payload) if not is_valid else "Validation failed",
                })
        except Exception as err:
            results.append({
                "id": f.stem,
                "filename": f.name,
                "title": f.stem,
                "description": "I/O error reading course file",
                "status": "error",
                "error_message": str(err),
            })

    return results


class PlatformRequestHandler(SimpleHTTPRequestHandler):
    """HTTP Request Handler serving both the Dynamic Course API and the frontend."""

    def end_headers(self):
        # Enable CORS for local integration
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(HTTPStatus.NO_CONTENT)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = unquote(parsed.path)

        # Endpoint: GET /api/courses
        if path == "/api/courses":
            self.handle_api_courses()
            return

        # Endpoint: GET /api/courses/<id>
        if path.startswith("/api/courses/"):
            requested_id = path[len("/api/courses/"):]
            self.handle_api_course_detail(requested_id)
            return

        # Static Frontend File Serving
        self.handle_static_files(path)

    def handle_api_courses(self):
        courses = scan_courses()
        body = json.dumps({"courses": courses}, ensure_ascii=False).encode("utf-8")

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.end_headers()
        self.wfile.write(body)

    def handle_api_course_detail(self, requested_id: str):
        courses = scan_courses()
        found = None
        for c in courses:
            if (
                c.get("id") == requested_id
                or c.get("filename") == requested_id
                or c.get("filename") == f"{requested_id}.json"
            ):
                found = c
                break

        if not found:
            body = json.dumps({"error": f"Course '{requested_id}' not found"}).encode("utf-8")
            self.send_response(HTTPStatus.NOT_FOUND)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if found.get("status") == "error":
            body = json.dumps({
                "error": found.get("error_message", "Course is invalid"),
                "status": "error"
            }).encode("utf-8")
            self.send_response(HTTPStatus.BAD_REQUEST)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        body = json.dumps(found.get("data", {}), ensure_ascii=False).encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def handle_static_files(self, path: str):
        if not (DIST_DIR / "index.html").exists():
            msg = (
                b"<!DOCTYPE html><html><head><meta charset='utf-8'><title>Platform Not Built</title></head>"
                b"<body style='font-family:system-ui,-apple-system,sans-serif;padding:40px;line-height:1.6;max-width:600px;margin:auto;'>"
                b"<h2 style='color:#b91c1c;'>Platform build directory (platform/dist) not found</h2>"
                b"<p>The platform frontend has not been compiled yet.</p>"
                b"<p>Run the build command from your terminal:</p>"
                b"<pre style='background:#f1f5f9;padding:12px;border-radius:6px;font-size:14px;'>python run_platform.py --build</pre>"
                b"</body></html>"
            )
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(msg)))
            self.end_headers()
            self.wfile.write(msg)
            return

        # Normalize relative path
        rel_path = path.lstrip("/")
        target_file = DIST_DIR / rel_path

        # If file exists in dist, serve it
        if rel_path and target_file.is_file():
            self.serve_file(target_file)
            return

        # SPA Fallback: serve index.html for all client-side routes
        index_file = DIST_DIR / "index.html"
        if index_file.is_file():
            self.serve_file(index_file)
        else:
            self.send_error(HTTPStatus.NOT_FOUND, "index.html not found")

    def serve_file(self, file_path: Path):
        content_type, _ = mimetypes.guess_type(str(file_path))
        if not content_type:
            content_type = "application/octet-stream"

        try:
            data = file_path.read_bytes()
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            # Add cache headers
            if file_path.suffix in {".js", ".css", ".woff2", ".svg", ".png"}:
                self.send_header("Cache-Control", "public, max-age=31536000, immutable")
            else:
                self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(data)
        except Exception as e:
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, f"Error reading file: {e}")

    def log_message(self, format: str, *args):
        # Suppress verbose HTTP access logs in test runs
        pass


def build_frontend() -> bool:
    """Build the frontend application into platform/dist.

    Uses a temporary directory on the local system drive to avoid virtual filesystem
    locking/concurrency issues (e.g. Google Drive, network mounts) during npm extraction.
    """
    import shutil
    import subprocess
    import tempfile

    npm_bin = shutil.which("npm.cmd") if sys.platform == "win32" else shutil.which("npm")
    if not npm_bin:
        npm_bin = shutil.which("npm")
    if not npm_bin:
        print("[ERROR] 'npm' was not found in PATH. Please install Node.js.")
        return False

    print("=" * 72)
    print("Building frontend assets into platform/dist...")
    temp_dir = Path(tempfile.gettempdir()) / "platform_build"
    try:
        if temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)
        shutil.copytree(
            PLATFORM_DIR,
            temp_dir,
            ignore=shutil.ignore_patterns("node_modules", "dist", ".git", "server"),
        )
        print("  * Installing npm dependencies...")
        subprocess.run([npm_bin, "install"], cwd=str(temp_dir), check=True, capture_output=True)
        print("  * Running Vite build...")
        subprocess.run([npm_bin, "run", "build"], cwd=str(temp_dir), check=True, capture_output=True)

        built_dist = temp_dir / "dist"
        if built_dist.exists() and (built_dist / "index.html").exists():
            if DIST_DIR.exists():
                shutil.rmtree(DIST_DIR, ignore_errors=True)
            shutil.copytree(built_dist, DIST_DIR)
            print("  * Frontend built successfully into platform/dist.")
            print("=" * 72)
            return True
        else:
            print("[ERROR] Build output (dist/index.html) was not generated.")
            print("=" * 72)
            return False
    except subprocess.CalledProcessError as err:
        stderr_msg = err.stderr.decode("utf-8", errors="replace") if err.stderr else str(err)
        print(f"[ERROR] Frontend build command failed:\n{stderr_msg}")
        print("=" * 72)
        return False
    except Exception as exc:
        print(f"[ERROR] Unexpected error while building frontend: {exc}")
        print("=" * 72)
        return False
    finally:
        if temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)


def run(port: int = 5173, host: str = "127.0.0.1"):
    if not (DIST_DIR / "index.html").exists():
        print("Platform build directory (platform/dist) not found. Building now...")
        build_frontend()

    server_address = (host, port)
    httpd = ThreadingHTTPServer(server_address, PlatformRequestHandler)
    discovered = scan_courses()
    valid_count = sum(1 for c in discovered if c.get("status") == "valid")
    print("=" * 72)
    print(f"  Top's Academy Platform Server Running")
    print(f"  Access URL: http://{host}:{port}")
    print(f"  Open your browser to: http://localhost:{port}")
    print("=" * 72)
    print(f"Discovered {len(discovered)} course(s) ({valid_count} valid):")
    for c in discovered:
        status_tag = "[VALID]" if c.get("status") == "valid" else f"[ERROR: {c.get('error_message')}]"
        print(f"  * {c.get('filename')} -> '{c.get('title')}' ({c.get('total_questions', 0)} questions, {c.get('total_competencies', 0)} competencies) {status_tag}")
    print("=" * 72)
    print("Press Ctrl+C to stop the platform server.\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        httpd.server_close()


def print_course_scan() -> None:
    """Print course scan results and validation status."""
    courses = scan_courses()
    print("=" * 72)
    print(f"Scanning courses in '{COURSES_DIR}'...")
    print(f"Found {len(courses)} course file(s):")
    print("-" * 72)
    for c in courses:
        status_str = "VALID" if c.get("status") == "valid" else f"INVALID: {c.get('error_message')}"
        print(f"File:         {c.get('filename')}")
        print(f"ID:           {c.get('id')}")
        print(f"Title:        {c.get('title')}")
        print(f"Status:       {status_str}")
        print(f"Competencies: {c.get('total_competencies', 0)}")
        print(f"Questions:    {c.get('total_questions', 0)}")
        print("-" * 72)
    print("Scan complete.")
    print("=" * 72)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start Top's Academy Platform")
    parser.add_argument("--port", type=int, default=5173, help="Port to listen on (default: 5173)")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host address (default: 127.0.0.1)")
    parser.add_argument("--scan", action="store_true", help="Scan and validate courses in courses/ directory without starting server")
    parser.add_argument("--build", action="store_true", help="Compile and build frontend assets into platform/dist")
    args = parser.parse_args()

    if args.scan:
        print_course_scan()
    elif args.build:
        success = build_frontend()
        sys.exit(0 if success else 1)
    else:
        run(port=args.port, host=args.host)

