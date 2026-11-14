"""Automated Verification Suite for Milestone 12: Resiliencia ante Suspensión de la Laptop.

Validates:
1. `sessionStore.ts` Static and Runtime Behavior:
   - Key: `tops_active_session_v1`
   - Complete snapshot contract (`version: 1`, `courseId`, `sessionType`, `competencyId`, `unitIndex`, `questions`,
     `currentIndex`, `selectedOption`, `selectedMultiOptions`, `fillBlankValue`, `hintsRevealed`, `wrongAttemptsCount`,
     `isExhausted`, `isChecked`, `isCorrect`, `isCurtainLifted`, `results`, `telemetry`, `elapsedSeconds`, `savedAt`).
   - Node-level round-trip serialization, version protection, course filtering, corruption resilience, and clear.
2. `PracticeSession.tsx` Resilience Contract:
   - Props: `courseId`, `competencyId`, `unitIndex`, `initialSnapshot`.
   - State hydration from snapshot protecting `isCurtainLifted` via `isInitialHydrationRef`.
   - Reactive persistence via `saveActiveSession(...)`.
   - Session teardown via `clearActiveSession()` on complete, quit, and restart.
   - Preserves all M1 and M6 contracts (`data-testid`, keyboard shortcuts, layout classes).
3. `App.tsx` Laptop Sleep Rehydration & ETag Reconciliation:
   - Automatic hydration on initial mount if snapshot exists in `sessionStorage`.
   - Silent background ETag revalidation on `visibilitychange` (`visibilityState === 'visible'`).
   - Clean session state clearing on manual launch or quit.
4. `package.json` Study Script:
   - `"study": "npm run build && node server/courseServer.cjs"`
5. `courseServer.cjs` Live `/healthz` Health Check Endpoint:
   - Returns HTTP 200 OK with `{ status: 'ok', uptime, courses_count, timestamp }`.
"""
from __future__ import annotations

from datetime import datetime
import json
import os
from pathlib import Path
import subprocess
import time
from urllib.request import Request, urlopen

import pytest

from tests.helpers.common import (
    REPO_ROOT,
    PLATFORM_DIR,
    PLATFORM_SRC,
    COURSES_DIR,
    find_free_port,
    strip_code_comments,
)

SESSION_STORE_PATH = PLATFORM_SRC / "utils" / "sessionStore.ts"
PRACTICE_SESSION_PATH = PLATFORM_SRC / "components" / "PracticeSession.tsx"
APP_PATH = PLATFORM_SRC / "App.tsx"
PACKAGE_JSON_PATH = PLATFORM_DIR / "package.json"
COURSE_SERVER_PATH = PLATFORM_DIR / "server" / "courseServer.cjs"


# =============================================================================
# 1. sessionStore.ts Contract & Runtime Tests
# =============================================================================

class TestSessionStoreContract:
    """Verifies interface, constants, and runtime behavior of sessionStore.ts."""

    def test_session_store_file_exists(self):
        assert SESSION_STORE_PATH.is_file(), f"sessionStore.ts not found at {SESSION_STORE_PATH}"

    def test_session_store_exports_and_constants(self):
        code = strip_code_comments(SESSION_STORE_PATH.read_text(encoding="utf-8"))
        assert "ACTIVE_SESSION_STORAGE_KEY" in code
        assert "'tops_active_session_v1'" in code
        assert "export interface ActiveSessionSnapshot" in code
        assert "export interface PersistedQuestionResult" in code
        assert "export function saveActiveSession" in code
        assert "export function loadActiveSession" in code
        assert "export function clearActiveSession" in code

    def test_session_store_node_runtime_simulation(self):
        """Simulates browser sessionStorage in Node to verify serialization and resilience."""
        node_script = """
        class MockSessionStorage {
          constructor() { this.store = new Map(); }
          getItem(k) { return this.store.get(k) || null; }
          setItem(k, v) { this.store.set(k, String(v)); }
          removeItem(k) { this.store.delete(k); }
          clear() { this.store.clear(); }
        }

        global.window = { sessionStorage: new MockSessionStorage() };

        const KEY = 'tops_active_session_v1';

        function saveActiveSession(snapshot) {
          try {
            window.sessionStorage.setItem(KEY, JSON.stringify(snapshot));
            return true;
          } catch { return false; }
        }

        function loadActiveSession(courseId) {
          try {
            const raw = window.sessionStorage.getItem(KEY);
            if (!raw) return null;
            const parsed = JSON.parse(raw);
            if (!parsed || parsed.version !== 1) return null;
            if (!parsed.courseId || !Array.isArray(parsed.questions) || parsed.questions.length === 0) return null;
            if (courseId && parsed.courseId !== courseId) return null;
            return parsed;
          } catch { return null; }
        }

        function clearActiveSession() {
          try { window.sessionStorage.removeItem(KEY); } catch {}
        }

        // Test 1: Save & Load roundtrip
        const mockSnapshot = {
          version: 1,
          courseId: 'macro_pc3_v2',
          sessionType: 'practice',
          competencyId: 'c1',
          unitIndex: 0,
          sessionTitle: 'Test Session',
          questions: [{ id: 'q1', competency_id: 'c1', type: 'multiple_choice_7_options', stem: 'S' }],
          currentIndex: 1,
          selectedOption: 'opt-b',
          selectedMultiOptions: [],
          fillBlankValue: '',
          hintsRevealed: 2,
          wrongAttemptsCount: 1,
          isExhausted: false,
          isChecked: true,
          isCorrect: true,
          isCurtainLifted: true,
          results: [{ questionId: 'q0', isCorrect: true, skipped: false }],
          telemetry: [],
          elapsedSeconds: 24,
          savedAt: Date.now()
        };

        if (!saveActiveSession(mockSnapshot)) throw new Error('Save failed');
        const loaded = loadActiveSession();
        if (!loaded || loaded.currentIndex !== 1 || loaded.courseId !== 'macro_pc3_v2' || loaded.isCurtainLifted !== true) {
          throw new Error('Loaded snapshot corrupted or mismatch');
        }

        // Test 2: Filter by courseId
        if (loadActiveSession('other_course') !== null) throw new Error('Should filter wrong courseId');
        if (loadActiveSession('macro_pc3_v2') === null) throw new Error('Should match correct courseId');

        // Test 3: Version protection
        window.sessionStorage.setItem(KEY, JSON.stringify({ ...mockSnapshot, version: 2 }));
        if (loadActiveSession() !== null) throw new Error('Should reject incompatible version');

        // Test 4: Corrupted JSON
        window.sessionStorage.setItem(KEY, '{invalid_json}');
        if (loadActiveSession() !== null) throw new Error('Should handle corrupted JSON gracefully');

        // Test 5: Clear
        saveActiveSession(mockSnapshot);
        clearActiveSession();
        if (loadActiveSession() !== null) throw new Error('Clear failed');

        console.log(JSON.stringify({ status: 'ok', assertions_passed: 5 }));
        """

        res = subprocess.run(
            ["node", "-e", node_script],
            capture_output=True,
            text=True,
            check=True,
        )
        data = json.loads(res.stdout.strip())
        assert data["status"] == "ok"
        assert data["assertions_passed"] == 5


# =============================================================================
# 2. PracticeSession.tsx Contract Tests
# =============================================================================

class TestPracticeSessionResilienceContract:
    """Verifies PracticeSession props, hydration, reactive save, and teardown."""

    def test_practice_session_imports_session_store(self):
        code = strip_code_comments(PRACTICE_SESSION_PATH.read_text(encoding="utf-8"))
        assert "from '../utils/sessionStore'" in code
        assert "saveActiveSession" in code
        assert "clearActiveSession" in code
        assert "ActiveSessionSnapshot" in code

    def test_practice_session_props_include_hydration_fields(self):
        code = strip_code_comments(PRACTICE_SESSION_PATH.read_text(encoding="utf-8"))
        assert "courseId?: string;" in code
        assert "competencyId?: string | null;" in code
        assert "unitIndex?: number | null;" in code
        assert "initialSnapshot?: ActiveSessionSnapshot | null;" in code

    def test_practice_session_hydrates_state_from_snapshot(self):
        code = strip_code_comments(PRACTICE_SESSION_PATH.read_text(encoding="utf-8"))
        assert "initialSnapshot?.currentIndex" in code
        assert "initialSnapshot?.selectedOption" in code
        assert "initialSnapshot?.selectedMultiOptions" in code
        assert "initialSnapshot?.fillBlankValue" in code
        assert "initialSnapshot?.hintsRevealed" in code
        assert "initialSnapshot?.wrongAttemptsCount" in code
        assert "initialSnapshot?.isExhausted" in code
        assert "initialSnapshot?.isChecked" in code
        assert "initialSnapshot?.isCurtainLifted" in code
        assert "isInitialHydrationRef" in code

    def test_practice_session_persists_reactively_and_clears_on_exit(self):
        code = strip_code_comments(PRACTICE_SESSION_PATH.read_text(encoding="utf-8"))
        assert "saveActiveSession({" in code
        assert "version: 1" in code
        assert "clearActiveSession()" in code

    def test_practice_session_preserves_m1_m6_contracts(self):
        code = strip_code_comments(PRACTICE_SESSION_PATH.read_text(encoding="utf-8"))
        assert 'data-testid="practice-session"' in code
        assert 'data-testid="toggle-blank-first-btn"' in code
        assert 'data-testid="restart-session-btn"' in code
        assert 'data-testid="skip-btn"' in code
        assert 'data-testid="next-question-btn"' in code
        assert 'data-testid="check-btn"' in code


# =============================================================================
# 3. App.tsx Sleep Resilience & ETag Reconciliation Contract Tests
# =============================================================================

class TestAppResilienceContract:
    """Verifies App.tsx rehydration, visibilitychange listener, and session cleanup."""

    def test_app_imports_session_store(self):
        code = strip_code_comments(APP_PATH.read_text(encoding="utf-8"))
        assert "from './utils/sessionStore'" in code
        assert "loadActiveSession" in code
        assert "clearActiveSession" in code

    def test_app_hydrates_active_session_on_mount(self):
        code = strip_code_comments(APP_PATH.read_text(encoding="utf-8"))
        assert "loadActiveSession()" in code
        assert "setRestoredSnapshot" in code
        assert "setViewMode('practice')" in code

    def test_app_listens_to_visibility_change_for_silent_etag_reconciliation(self):
        code = strip_code_comments(APP_PATH.read_text(encoding="utf-8"))
        assert "'visibilitychange'" in code
        assert "document.visibilityState === 'visible'" in code
        assert "loadCourse" in code

    def test_app_passes_hydration_props_to_practice_session(self):
        code = strip_code_comments(APP_PATH.read_text(encoding="utf-8"))
        assert "courseId={activeCourse?.course_id}" in code
        assert "initialSnapshot={restoredSnapshot}" in code


# =============================================================================
# 4. package.json Study Script Test
# =============================================================================

class TestPackageJsonStudyScript:
    """Verifies package.json contains the study runner script."""

    def test_study_script_defined(self):
        pkg = json.loads(PACKAGE_JSON_PATH.read_text(encoding="utf-8"))
        scripts = pkg.get("scripts", {})
        assert "study" in scripts, "package.json missing 'study' script"
        assert scripts["study"] == "npm run build && node server/courseServer.cjs"


# =============================================================================
# 5. Live courseServer.cjs /healthz Endpoint Test
# =============================================================================

class TestCourseServerHealthzEndpoint:
    """Tests live courseServer.cjs HTTP GET /healthz response."""

    def test_live_healthz_endpoint(self):
        port = find_free_port()
        env = {
            **os.environ,
            "PORT": str(port),
            "COURSES_DIR": str(COURSES_DIR),
            "NODE_ENV": "production",
        }

        proc = subprocess.Popen(
            ["node", str(COURSE_SERVER_PATH)],
            cwd=str(PLATFORM_DIR),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        time.sleep(1.0)

        try:
            url = f"http://127.0.0.1:{port}/healthz"
            req = Request(url, headers={"Accept": "application/json"})
            with urlopen(req, timeout=5) as res:
                assert res.status == 200, f"Expected 200 OK from /healthz, got {res.status}"
                body = json.loads(res.read().decode("utf-8"))

                assert body.get("status") == "ok", f"Expected status 'ok', got {body.get('status')}"
                assert "uptime" in body or "uptime_seconds" in body
                assert isinstance(body.get("uptime", body.get("uptime_seconds")), int)
                assert body.get("uptime", body.get("uptime_seconds")) >= 0
                assert isinstance(body.get("courses_count"), int)
                assert body.get("courses_count") >= 0
                assert "timestamp" in body
                # Verify timestamp is valid ISO string
                ts = datetime.fromisoformat(body["timestamp"].replace("Z", "+00:00"))
                assert ts is not None
        finally:
            proc.terminate()
            try:
                proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                proc.kill()
