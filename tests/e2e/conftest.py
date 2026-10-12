import os
import sys
import time
import shutil
import subprocess
import socket
import pytest
from pathlib import Path
from playwright.sync_api import sync_playwright, Browser, Page, BrowserContext

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
COURSES_DIR = ROOT_DIR / "courses"
FIXTURES_DIR = COURSES_DIR / "test_fixtures"
SCREENSHOTS_DIR = ROOT_DIR / "tests" / "e2e" / "screenshots"

SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


def is_port_open(port: int, host: str = "127.0.0.1") -> bool:
    """Check if server port is open and listening."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) == 0


@pytest.fixture(scope="session")
def platform_server():
    """Ensure the platform server is running.
    If already running on port 5173 or 3000, use it.
    Otherwise, attempts to launch run_platform.py or npm.cmd run dev.
    """
    ports_to_check = [5173, 3000, 8080]
    for port in ports_to_check:
        if is_port_open(port):
            yield f"http://localhost:{port}"
            return

    # Attempt to start platform via run_platform.py if present
    run_platform_script = ROOT_DIR / "run_platform.py"
    proc = None
    target_port = 5173

    if run_platform_script.exists():
        proc = subprocess.Popen(
            [sys.executable, str(run_platform_script)],
            cwd=str(ROOT_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )
    elif (ROOT_DIR / "platform" / "package.json").exists():
        proc = subprocess.Popen(
            ["npm.cmd", "run", "dev"],
            cwd=str(ROOT_DIR / "platform"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )

    # Wait up to 15 seconds for server to be responsive
    start_time = time.time()
    base_url = None
    while time.time() - start_time < 15:
        for port in ports_to_check:
            if is_port_open(port):
                base_url = f"http://localhost:{port}"
                break
        if base_url:
            break
        time.sleep(0.5)

    if not base_url:
        # Default fallback to 5173 (standard Vite port)
        base_url = "http://localhost:5173"

    yield base_url

    if proc:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except Exception:
            proc.kill()


@pytest.fixture(scope="session")
def browser_instance():
    """Create a headless Chromium browser instance."""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--window-size=1280,800"
            ]
        )
        yield browser
        browser.close()


@pytest.fixture
def page(browser_instance: Browser, platform_server: str):
    """Create a fresh isolated browser page with strict console error interception."""
    context = browser_instance.new_context(
        viewport={"width": 1280, "height": 800},
        ignore_https_errors=True
    )
    page = context.new_page()

    console_errors = []
    page_errors = []

    def handle_console(msg):
        if msg.type == "error":
            # Ignore harmless favicon/css missing errors during tests
            text = msg.text
            if "favicon.ico" not in text:
                console_errors.append(text)

    def handle_page_error(exc):
        page_errors.append(str(exc))

    page.on("console", handle_console)
    page.on("pageerror", handle_page_error)

    # Attach tracking lists to page for test assertion
    page.console_errors = console_errors
    page.page_errors = page_errors
    page.base_url = platform_server

    yield page

    context.close()


@pytest.fixture
def setup_test_courses():
    """Fixture ensuring sample courses are present in courses/ during tests."""
    COURSES_DIR.mkdir(parents=True, exist_ok=True)
    created_files = []

    # Copy calculus fixture to root courses/
    calculus_src = FIXTURES_DIR / "valid_course_calculus.json"
    calculus_dst = COURSES_DIR / "test_differential_calculus.json"
    if calculus_src.exists() and not calculus_dst.exists():
        shutil.copy2(calculus_src, calculus_dst)
        created_files.append(calculus_dst)

    # Copy challenge fixture to root courses/
    challenge_src = FIXTURES_DIR / "valid_course_challenge.json"
    challenge_dst = COURSES_DIR / "test_course_challenge.json"
    if challenge_src.exists() and not challenge_dst.exists():
        shutil.copy2(challenge_src, challenge_dst)
        created_files.append(challenge_dst)

    yield {
        "calculus_path": calculus_dst,
        "challenge_path": challenge_dst
    }

    # Clean up temporarily placed fixture files
    for f in created_files:
        try:
            if f.exists():
                f.unlink()
        except Exception:
            pass
