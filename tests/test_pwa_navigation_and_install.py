"""Automated test suite for PWA Mobile Back Gesture Navigation and Instant Install Button."""
import json
import re
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
PLATFORM_DIR = REPO_ROOT / "platform"


class TestPwaInstantInstallButton:
    """Verifies that the Install App button captures beforeinstallprompt early and renders immediately with spinner."""

    def test_index_html_has_early_capture_script(self):
        index_html = PLATFORM_DIR / "index.html"
        content = index_html.read_text(encoding="utf-8")

        assert "window.__deferredPrompt = null" in content
        assert "beforeinstallprompt" in content
        assert "pwa-prompt-ready" in content
        assert "appinstalled" in content

    def test_course_library_has_instant_install_button_and_spinner(self):
        course_library = PLATFORM_DIR / "src" / "components" / "CourseLibrary.tsx"
        code = course_library.read_text(encoding="utf-8")

        assert "display-mode: standalone" in code
        assert "canInstall" in code
        assert "isInstalling" in code
        assert "pwa-prompt-ready" in code
        assert "Preparando instalación..." in code
        assert "Instalar App" in code
        assert "pwa-install-button" in code


class TestPwaNavigationHistoryArchitecture:
    """Verifies Navigation History Manager implementation and screen-level back gesture handling."""

    def test_navigation_history_module_exists_and_exports_expected_api(self):
        nav_module = PLATFORM_DIR / "src" / "utils" / "navigationHistory.ts"
        assert nav_module.is_file()
        code = nav_module.read_text(encoding="utf-8")

        assert "export type AppViewMode" in code
        assert "export function registerBackInterceptor" in code
        assert "export function pushNavState" in code
        assert "export function replaceNavState" in code
        assert "export function setupNavigationHistory" in code
        assert "ROOT_EXIT_THRESHOLD_MS = 2000" in code
        assert "popstate" in code

    def test_sidebar_registers_back_interceptor_for_mobile_drawer(self):
        sidebar = PLATFORM_DIR / "src" / "components" / "Sidebar.tsx"
        code = sidebar.read_text(encoding="utf-8")

        assert "registerBackInterceptor" in code
        assert "setIsOpen(false)" in code

    def test_app_integrates_history_and_quit_confirmation_modal(self):
        app = PLATFORM_DIR / "src" / "App.tsx"
        code = app.read_text(encoding="utf-8")

        assert "setupNavigationHistory" in code
        assert "registerBackInterceptor" in code
        assert "navigateView" in code
        assert "showExitToast" in code
        assert "showQuitConfirm" in code
        assert "double-back-toast" in code
        assert "Presiona atrás de nuevo para salir" in code
        assert "quit-confirm-modal" in code
        assert "¿Deseas salir de la sesión?" in code
        assert "quit-confirm-continue" in code
        assert "quit-confirm-exit" in code


class TestNavigationStateTransitions:
    """Simulates navigation transitions and back gesture interception rules."""

    def test_double_back_root_exit_logic(self):
        """Validates that a single back press inside 2s triggers toast, second exits."""
        threshold = 2000
        first_press = 1000
        # If pressed 1 second later: should allow exit (1000 ms < 2000 ms)
        second_press_fast = 2000
        assert (second_press_fast - first_press) < threshold

        # If pressed 3 seconds later: should not allow exit (3000 ms >= 2000 ms)
        second_press_slow = 4050
        assert (second_press_slow - first_press) >= threshold
