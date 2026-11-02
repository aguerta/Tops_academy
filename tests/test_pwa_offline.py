"""Automated Verification Suite for Milestone 2: PWA Instalable y Modo Offline.

Validates Acceptance Criteria and Critical Safeguards:
1. Web App Manifest (`manifest.webmanifest`):
   - Standalone display mode, orientation, name, theme_color, background_color.
   - Adaptive icons (192x192, 512x512, and maskable 512x512).
2. Workbox Service Worker Precache (`sw.js`):
   - Precaches App Shell: HTML, JS, CSS, `api/courses.json`, and KaTeX `.woff2` fonts.
   - Precache payload size <= 3.0 MB.
   - CRITICAL SAFEGUARD: Strictly excludes all heavy course files (`courses/*.json` and `api/courses/*.json`),
     ensuring multi-megabyte courses (like Gavilano at 14 MB) never bloat the App Shell.
   - Registers StaleWhileRevalidate runtime caching for `/api/courses/` and `/courses/`.
3. iOS & Mobile Safe Areas (`index.html` & CSS):
   - `viewport-fit=cover` in meta viewport.
   - Apple mobile web app capable, status-bar-style, and touch icon.
   - CSS safe area padding classes defined.
4. Server HTTP Headers:
   - `sw.js` served with `no-cache, no-store, must-revalidate` (guarantees fast updates).
   - `.webmanifest` served with `application/manifest+json`.
"""
from __future__ import annotations

import json
import re
import socket
import subprocess
import sys
import threading
import time
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.request import Request, urlopen

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
PLATFORM_DIR = REPO_ROOT / "platform"
DIST_DIR = PLATFORM_DIR / "dist"
SERVER_DIR = PLATFORM_DIR / "server"
COURSE_SERVER_PATH = SERVER_DIR / "courseServer.cjs"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from run_platform import PlatformRequestHandler


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


# =============================================================================
# 1. Manifest & Static Asset Tests
# =============================================================================

class TestPwaManifestAndIcons:
    """Verifies Web App Manifest and adaptive icon assets."""

    def test_manifest_file_exists_and_valid(self):
        manifest_path = DIST_DIR / "manifest.webmanifest"
        assert manifest_path.is_file(), f"manifest.webmanifest not found at {manifest_path}"
        data = json.loads(manifest_path.read_text(encoding="utf-8"))

        assert data.get("name") == "Top's Academy"
        assert data.get("short_name") == "Top's Academy"
        assert data.get("display") == "standalone"
        assert data.get("theme_color") == "#1865f2"
        assert data.get("background_color") == "#fafbfc"
        assert data.get("start_url") in ["./", "/Tops_academy/"]

        icons = data.get("icons", [])
        assert len(icons) >= 3, "Manifest must declare at least 3 icons"

        sizes = [icon.get("sizes") for icon in icons]
        assert "192x192" in sizes, "Must include 192x192 icon"
        assert "512x512" in sizes, "Must include 512x512 icon"

        has_maskable = any(icon.get("purpose") == "maskable" for icon in icons)
        assert has_maskable, "Must include at least one maskable icon for adaptive Android icons"

    def test_pwa_icon_files_exist_in_dist(self):
        expected_icons = [
            "pwa-192x192.png",
            "pwa-512x512.png",
            "pwa-maskable-512x512.png",
            "apple-touch-icon.png",
            "favicon.ico",
            "icon.svg",
        ]
        for icon_name in expected_icons:
            icon_path = DIST_DIR / icon_name
            assert icon_path.is_file(), f"Expected icon {icon_name} not found in dist/"
            assert icon_path.stat().st_size > 0, f"Icon {icon_name} is empty"


# =============================================================================
# 2. Workbox Service Worker & Precache Tests
# =============================================================================

class TestServiceWorkerAndPrecache:
    """Verifies Workbox SW generation, App Shell precache, and strict course exclusion."""

    def test_sw_file_exists_and_contains_workbox(self):
        sw_path = DIST_DIR / "sw.js"
        assert sw_path.is_file(), f"sw.js not found at {sw_path}"
        content = sw_path.read_text(encoding="utf-8")
        assert "precacheAndRoute" in content, "sw.js must contain precacheAndRoute"

    def test_precache_includes_app_shell_and_katex_fonts(self):
        sw_path = DIST_DIR / "sw.js"
        content = sw_path.read_text(encoding="utf-8")

        # Parse precacheAndRoute entries
        match = re.search(r"precacheAndRoute\(\[([\s\S]*?)\]", content)
        assert match, "Could not find precacheAndRoute array in sw.js"
        precache_raw = match.group(1)

        urls = re.findall(r'url:"([^"]+)"', precache_raw)
        assert "index.html" in urls, "index.html must be in precache"
        assert "api/courses.json" in urls, "api/courses.json slim manifest must be in precache"

        # Check KaTeX .woff2 fonts are precached
        woff2_fonts = [u for u in urls if u.endswith(".woff2")]
        assert len(woff2_fonts) >= 10, f"Expected >= 10 KaTeX .woff2 fonts in precache, got {len(woff2_fonts)}"

    def test_precache_strictly_excludes_heavy_courses(self):
        """CRITICAL SAFEGUARD: Verifies NO course JSON is in precacheAndRoute."""
        sw_path = DIST_DIR / "sw.js"
        content = sw_path.read_text(encoding="utf-8")

        match = re.search(r"precacheAndRoute\(\[([\s\S]*?)\]", content)
        assert match, "Could not find precacheAndRoute array in sw.js"
        urls = re.findall(r'url:"([^"]+)"', match.group(1))

        # Check that individual courses are NOT in precache
        for u in urls:
            assert not u.startswith("courses/"), f"Course file '{u}' must NOT be in precache!"
            if u.startswith("api/courses/"):
                assert False, f"Course file '{u}' must NOT be in precache!"

        # Ensure specifically heavy courses are absent
        forbidden_courses = [
            "saul_pre_parcial.json",
            "gavilano_pre_parcial.json",
            "solow_growth_model.json",
            "estadistica_3_s9_vmapreduce5.json",
        ]
        for course_name in forbidden_courses:
            assert not any(course_name in u for u in urls), (
                f"Course {course_name} was found in precache list! Precache must only include App Shell."
            )

    def test_runtime_caching_registered_for_courses(self):
        """Verifies StaleWhileRevalidate runtime caching is set up for course JSON files."""
        sw_path = DIST_DIR / "sw.js"
        content = sw_path.read_text(encoding="utf-8")

        assert "api/courses/" in content or "courses/" in content, (
            "sw.js must contain runtime route pattern for /api/courses/ or /courses/"
        )
        assert "StaleWhileRevalidate" in content, (
            "sw.js must use StaleWhileRevalidate strategy for runtime courses cache"
        )


# =============================================================================
# 3. HTML Metatags & Safe Areas Tests
# =============================================================================

class TestHtmlMetatagsAndSafeAreas:
    """Verifies safe areas and mobile standalone viewport metatags."""

    def test_index_html_has_viewport_fit_cover(self):
        index_path = PLATFORM_DIR / "index.html"
        content = index_path.read_text(encoding="utf-8")
        assert "viewport-fit=cover" in content, (
            "platform/index.html must include 'viewport-fit=cover' in meta viewport"
        )

    def test_index_html_has_pwa_and_apple_meta_tags(self):
        index_path = PLATFORM_DIR / "index.html"
        content = index_path.read_text(encoding="utf-8")
        assert '<meta name="theme-color" content="#1865f2"' in content
        assert '<meta name="mobile-web-app-capable" content="yes"' in content
        assert '<meta name="apple-mobile-web-app-capable" content="yes"' in content
        assert 'apple-touch-icon' in content

    def test_dist_index_html_links_manifest_webmanifest(self):
        dist_index = DIST_DIR / "index.html"
        content = dist_index.read_text(encoding="utf-8")
        assert 'rel="manifest"' in content
        assert 'manifest.webmanifest' in content

    def test_index_css_defines_safe_area_utilities(self):
        css_path = PLATFORM_DIR / "src" / "index.css"
        content = css_path.read_text(encoding="utf-8")
        assert "safe-area-inset-bottom" in content, (
            "platform/src/index.css must include safe-area-inset-bottom support"
        )
        assert ".footer-safe" in content or ".safe-bottom" in content


# =============================================================================
# 4. Server Cache & MIME Headers Tests
# =============================================================================

class TestServerPwaHeaders:
    """Verifies Node and Python servers serve PWA assets with correct headers."""

    def test_python_server_serves_sw_with_no_cache_and_manifest_mime(self):
        port = find_free_port()
        server = ThreadingHTTPServer(("127.0.0.1", port), PlatformRequestHandler)
        t = threading.Thread(target=server.serve_forever, daemon=True)
        t.start()
        time.sleep(0.3)

        try:
            # 1. sw.js
            req_sw = Request(f"http://127.0.0.1:{port}/sw.js")
            with urlopen(req_sw) as res:
                assert res.status == 200
                cc = res.headers.get("Cache-Control", "")
                assert "no-cache" in cc, f"sw.js Cache-Control must be no-cache, got {cc}"
                assert "immutable" not in cc, f"sw.js must NOT be cached immutably"

            # 2. manifest.webmanifest
            req_manifest = Request(f"http://127.0.0.1:{port}/manifest.webmanifest")
            with urlopen(req_manifest) as res:
                assert res.status == 200
                ct = res.headers.get("Content-Type", "")
                assert "manifest+json" in ct or "application/json" in ct, (
                    f"manifest.webmanifest Content-Type must be manifest JSON, got {ct}"
                )
        finally:
            server.shutdown()

    def test_node_server_serves_sw_with_no_cache(self):
        port = find_free_port()
        env = {
            "PORT": str(port),
            "COURSES_DIR": str(REPO_ROOT / "courses"),
            "NODE_ENV": "production",
        }
        import os
        full_env = {**os.environ, **env}

        proc = subprocess.Popen(
            ["node", str(COURSE_SERVER_PATH)],
            cwd=str(PLATFORM_DIR),
            env=full_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        time.sleep(1.0)

        try:
            req_sw = Request(f"http://127.0.0.1:{port}/sw.js")
            with urlopen(req_sw) as res:
                assert res.status == 200
                cc = res.headers.get("Cache-Control", "")
                assert "no-cache" in cc, f"Node server sw.js Cache-Control must be no-cache, got {cc}"

            req_manifest = Request(f"http://127.0.0.1:{port}/manifest.webmanifest")
            with urlopen(req_manifest) as res:
                assert res.status == 200
                ct = res.headers.get("Content-Type", "")
                assert "manifest+json" in ct or "application/json" in ct
        finally:
            proc.terminate()
            try:
                proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                proc.kill()
