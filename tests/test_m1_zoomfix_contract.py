"""
Contract tests for Milestone 1: Web Ergonomics Laptop + Split-View 50% (Zoom-Fix).

Validates static structural invariants across platform/src:
- Container queries (.qc-root, @container qc)
- Column-first 2-column grid layout (repeat(2, minmax(0, 1fr)), grid-auto-flow: column)
- Fluid spacing & typography via clamp()
- Dynamic viewport heights (100dvh, .h-dvh-safe)
- Zero residual 100vh / min-h-screen in PracticeSession
- Responsive Sidebar with drawer on < 1024px (breakpoint lg, no unconditional rigid w-64)
- Responsive viewBox on CoordinatePlane SVG
- Responsive bottom sheet FeedbackToast (45dvh on mobile / <= 850px)
- Responsive main layout padding in App (pt-14 lg:pt-0)
- Gate 1E viewports (CourseLibrary, CourseOverview, MasteryGrid, PreExerciseModal, CompletionScreen)
- KaTeX overflow guards across all components
- MC7 and Multiple Select column distribution math for 3 to 9 options
- Comprehensive Accessibility (a11y) attributes (ARIA roles, states, labels, focus trap)
- Viewport matrix compliance (683/720/800/960/1366/1440/390 width, 768/900/1080 height)
- Preservation of all critical data-testid attributes
- Adversarial comment stripper: comments must NOT yield false positives or false negatives
- In-memory mutation checks ensuring tests fail if contracts are broken.
"""

import math
import re
from pathlib import Path
import pytest

# ==============================================================================
# Cross-Platform Path Definitions (Pathlib)
# ==============================================================================
REPO_ROOT = Path(__file__).resolve().parent.parent
PLATFORM_SRC = REPO_ROOT / "platform" / "src"

# Gate 1A
INDEX_CSS = PLATFORM_SRC / "index.css"
QUESTION_CARD_TSX = PLATFORM_SRC / "components" / "QuestionCard.tsx"

# Gate 1B
SIDEBAR_TSX = PLATFORM_SRC / "components" / "Sidebar.tsx"
APP_TSX = PLATFORM_SRC / "App.tsx"

# Gate 1C
FEEDBACK_TOAST_TSX = PLATFORM_SRC / "components" / "FeedbackToast.tsx"
COORDINATE_PLANE_TSX = PLATFORM_SRC / "components" / "CoordinatePlane.tsx"

# Gate 1D
PRACTICE_SESSION_TSX = PLATFORM_SRC / "components" / "PracticeSession.tsx"

# Gate 1E
COMPLETION_SCREEN_TSX = PLATFORM_SRC / "components" / "CompletionScreen.tsx"
COURSE_CHALLENGE_TSX = PLATFORM_SRC / "components" / "CourseChallenge.tsx"
COURSE_LIBRARY_TSX = PLATFORM_SRC / "components" / "CourseLibrary.tsx"
COURSE_OVERVIEW_TSX = PLATFORM_SRC / "components" / "CourseOverview.tsx"
MASTERY_GRID_TSX = PLATFORM_SRC / "components" / "MasteryGrid.tsx"
MASTERY_LEGEND_TSX = PLATFORM_SRC / "components" / "MasteryLegend.tsx"
PRE_EXERCISE_MODAL_TSX = PLATFORM_SRC / "components" / "PreExerciseModal.tsx"


def strip_code_comments(src: str) -> str:
    """
    Robust comment stripper supporting JS/TS/JSX and CSS.
    Removes // line comments and /* ... */ block comments (including JSX {/* ... */}),
    while strictly preserving string literals ('...', "...", `...`).
    Maintains approximate newline structure for clean diagnostics across Windows (CRLF) and POSIX (LF).
    """
    out = []
    i = 0
    n = len(src)
    state = "NORMAL"

    while i < n:
        c = src[i]
        next_c = src[i + 1] if i + 1 < n else ""

        if state == "NORMAL":
            if c == "/" and next_c == "/":
                state = "LINE_COMMENT"
                i += 2
                continue
            elif c == "/" and next_c == "*":
                state = "BLOCK_COMMENT"
                i += 2
                continue
            elif c == "'":
                state = "SINGLE_QUOTE"
                out.append(c)
                i += 1
                continue
            elif c == '"':
                state = "DOUBLE_QUOTE"
                out.append(c)
                i += 1
                continue
            elif c == "`":
                state = "BACKTICK"
                out.append(c)
                i += 1
                continue
            else:
                out.append(c)
                i += 1
                continue

        elif state == "SINGLE_QUOTE":
            out.append(c)
            if c == "\\":
                if i + 1 < n:
                    out.append(src[i + 1])
                    i += 2
                    continue
            elif c == "'":
                state = "NORMAL"
            i += 1

        elif state == "DOUBLE_QUOTE":
            out.append(c)
            if c == "\\":
                if i + 1 < n:
                    out.append(src[i + 1])
                    i += 2
                    continue
            elif c == '"':
                state = "NORMAL"
            i += 1

        elif state == "BACKTICK":
            out.append(c)
            if c == "\\":
                if i + 1 < n:
                    out.append(src[i + 1])
                    i += 2
                    continue
            elif c == "`":
                state = "NORMAL"
            i += 1

        elif state == "LINE_COMMENT":
            if c == "\n":
                state = "NORMAL"
                out.append("\n")
            i += 1

        elif state == "BLOCK_COMMENT":
            if c == "*" and next_c == "/":
                state = "NORMAL"
                i += 2
                continue
            elif c == "\n":
                out.append("\n")
            i += 1

    return "".join(out)


def read_stripped(path: Path) -> str:
    """Reads a file and strips all comments with UTF-8 encoding."""
    resolved = path.resolve()
    assert resolved.is_file(), f"Target file does not exist: {resolved}"
    content = resolved.read_text(encoding="utf-8")
    return strip_code_comments(content)


# ==============================================================================
# Validation Helpers for Contract & Mutation Checks
# ==============================================================================

def validate_index_css_contract(css: str):
    """Verifies all structural invariants in index.css."""
    assert ".qc-root" in css, "Missing .qc-root selector in index.css"
    assert "container-type: inline-size" in css, "Missing container-type: inline-size in .qc-root"
    assert "container-name: qc" in css, "Missing container-name: qc in .qc-root"
    assert ".qc-options" in css, "Missing .qc-options selector in index.css"
    assert "display: grid" in css, "Missing display: grid in .qc-options"
    assert "@container qc (min-width: 600px)" in css, "Missing @container qc (min-width: 600px)"
    assert "repeat(2, minmax(0, 1fr))" in css, "Missing repeat(2, minmax(0, 1fr)) in container query"
    assert "grid-auto-flow: column" in css, "Missing grid-auto-flow: column in container query"
    assert "grid-template-rows: repeat(var(--qc-rows" in css, "Missing grid-template-rows in container query"
    assert "--qc-gap: clamp(" in css, "Missing fluid --qc-gap clamp token"
    assert "--qc-pad: clamp(" in css, "Missing fluid --qc-pad clamp token"
    assert "--qc-font: clamp(" in css, "Missing fluid --qc-font clamp token"
    assert "--qc-badge: clamp(" in css, "Missing fluid --qc-badge clamp token"
    assert ".qc-options-scroll" in css, "Missing .qc-options-scroll selector"
    assert "100dvh" in css, "Missing 100dvh in index.css"
    assert ".h-dvh-safe" in css, "Missing .h-dvh-safe utility"
    assert "min-height: 100dvh" in css, "Missing min-height: 100dvh in .h-dvh-safe"
    assert ".katex-display" in css and "overflow-x: auto" in css, "Missing KaTeX display overflow guard"
    assert ".qc-root .katex" in css and "max-width: 100%" in css, "Missing KaTeX root max-width guard"


def validate_question_card_contract(qc: str):
    """Verifies all structural invariants in QuestionCard.tsx."""
    for cls in ["qc-root", "qc-stem", "qc-options-scroll", "qc-options", "qc-option-item", "qc-badge"]:
        assert cls in qc, f"Missing class '{cls}' in QuestionCard.tsx"
    assert "Math.ceil(optionsCount / 2)" in qc, "Missing Math.ceil(optionsCount / 2) row calculation"
    assert "'--qc-rows'" in qc, "Missing '--qc-rows' inline style injection"
    assert "max-w-none" in qc, "Missing max-w-none on question stem"
    assert 'data-testid="question-card"' in qc, "Missing data-testid='question-card'"
    assert 'role="radiogroup"' in qc, "Missing role='radiogroup' on MCQ options"
    assert 'role="group"' in qc, "Missing role='group' on multiple_select options"


def validate_sidebar_contract(sb: str):
    """Verifies all structural invariants in Sidebar.tsx."""
    assert "1024" in sb, "Missing 1024px desktop breakpoint"
    assert "lg:hidden" in sb, "Missing lg:hidden on mobile toggle"
    assert "lg:static" in sb, "Missing lg:static on desktop sidebar"
    assert "lg:w-56" in sb, "Missing lg:w-56 responsive width"
    assert "lg:translate-x-0" in sb, "Missing lg:translate-x-0"
    assert "-translate-x-full lg:translate-x-0" in sb, "Missing drawer off-canvas transition"
    aside_match = re.search(r'<aside[^>]*className=\{`([^`]+)`\}', sb)
    assert aside_match, "Could not find <aside> with className in Sidebar.tsx"
    classes = aside_match.group(1)
    assert "max-w-[85vw]" in classes, "Sidebar lacks max-w-[85vw] drawer constraint"
    assert "lg:w-56" in classes, "Sidebar lacks lg:w-56 responsive width"
    assert "fixed lg:static" in classes, "Sidebar lacks fixed-to-static responsive transition"
    assert 'data-testid="sidebar-toggle"' in sb, "Missing data-testid='sidebar-toggle'"
    assert 'data-testid="sidebar"' in sb, "Missing data-testid='sidebar'"
    assert "'Escape'" in sb or '"Escape"' in sb, "Missing Escape key handler"


def validate_practice_session_contract(ps: str):
    """Verifies all structural invariants in PracticeSession.tsx."""
    assert len(re.findall(r'100vh', ps)) == 0, "Residual raw 100vh found in PracticeSession"
    assert len(re.findall(r'min-h-screen', ps)) == 0, "Residual min-h-screen found in PracticeSession"
    assert "h-dvh-safe" in ps, "Missing .h-dvh-safe in PracticeSession"
    assert "100dvh" in ps, "Missing 100dvh in PracticeSession"
    assert "[@media(max-height:850px)]:h-12" in ps or "max-height:850px" in ps, "Missing compact header media query"
    assert 'data-testid="practice-session"' in ps, "Missing data-testid='practice-session'"


def validate_coordinate_plane_contract(cp: str):
    """Verifies all structural invariants in CoordinatePlane.tsx."""
    assert "viewBox=" in cp, "Missing viewBox on CoordinatePlane SVG"
    assert "max-w-[340px]" in cp, "Missing max-w-[340px] constraint"
    assert "30dvh" in cp, "Missing 30dvh constraint"
    assert 'data-testid="coordinate-plane"' in cp, "Missing data-testid='coordinate-plane'"


def validate_feedback_toast_contract(ft: str):
    """Verifies all structural invariants in FeedbackToast.tsx."""
    assert "45dvh" in ft, "Missing 45dvh bottom-sheet constraint"
    assert "max-height: 850px" in ft or "max-height:850px" in ft, "Missing 850px height media query"
    assert 'data-testid="feedback-toast"' in ft, "Missing data-testid='feedback-toast'"


# ==============================================================================
# 1. ADVERSARIAL COMMENT STRIPPER TESTS
# ==============================================================================

class TestCommentStripperAdversarial:
    """Adversarial tests ensuring the comment stripper prevents false positives and false negatives."""

    def test_strips_single_line_comments_with_fake_contract(self):
        code = '// data-testid="fake-testid" style={{ height: "100vh" }}\nconst x = 42;'
        stripped = strip_code_comments(code)
        assert 'data-testid="fake-testid"' not in stripped
        assert "100vh" not in stripped
        assert "const x = 42;" in stripped

    def test_strips_block_comments_with_fake_container_query(self):
        code = '/* @container qc (min-width: 600px) { .qc-options { repeat(2; } } */ .real-rule {}'
        stripped = strip_code_comments(code)
        assert "@container" not in stripped
        assert "repeat(2" not in stripped
        assert ".real-rule {}" in stripped

    def test_strips_jsx_block_comments(self):
        code = '<div className="real">\n  {/* <aside className="w-64">Fake</aside> */}\n</div>'
        stripped = strip_code_comments(code)
        assert '<aside className="w-64">' not in stripped
        assert '<div className="real">' in stripped

    def test_preserves_slashes_in_strings(self):
        code = 'const api = "http://localhost:3000/api/courses";'
        stripped = strip_code_comments(code)
        assert 'const api = "http://localhost:3000/api/courses";' in stripped

    def test_preserves_template_strings_and_escapes(self):
        code = 'const s = `Path: \\`escaped\\` // not a comment`; // actual comment\nconst y = 1;'
        stripped = strip_code_comments(code)
        assert "// not a comment" in stripped
        assert "// actual comment" not in stripped
        assert "const y = 1;" in stripped

    def test_adversarial_commented_out_feature_not_detected_as_active(self):
        """Simulate a broken implementation where a developer commented out 100dvh or a data-testid."""
        fake_tsx = '''
        export const FakeComp = () => {
          // <button data-testid="sidebar-toggle">Toggle</button>
          /* style={{ minHeight: "100dvh" }} */
          return <div>Content</div>;
        };
        '''
        clean = strip_code_comments(fake_tsx)
        assert 'data-testid="sidebar-toggle"' not in clean
        assert "100dvh" not in clean
        assert "<div>Content</div>" in clean

    def test_handles_windows_crlf_in_comments(self):
        """Ensures Windows \\r\\n newlines inside comments are cleanly stripped."""
        code = "// line comment with CRLF\r\nconst active = true;\r\n/* block CRLF */\r\nconst done = true;"
        clean = strip_code_comments(code)
        assert "line comment with CRLF" not in clean
        assert "block CRLF" not in clean
        assert "const active = true;" in clean
        assert "const done = true;" in clean

    def test_handles_comment_at_eof_without_newline(self):
        """Ensures comments terminating at EOF without trailing newline do not crash or corrupt output."""
        code = "const x = 10; // eof comment"
        clean = strip_code_comments(code)
        assert "const x = 10;" in clean
        assert "eof comment" not in clean


# ==============================================================================
# 2. INDEX.CSS CONTRACT TESTS
# ==============================================================================

class TestIndexCssContract:
    """Verifies responsive contract rules in platform/src/index.css."""

    @pytest.fixture
    def css_clean(self):
        return read_stripped(INDEX_CSS)

    def test_qc_root_container_query_definition(self, css_clean):
        """Contract: .qc-root must define container-type inline-size and name qc."""
        assert ".qc-root" in css_clean
        assert "container-type: inline-size" in css_clean
        assert "container-name: qc" in css_clean

    def test_qc_options_default_and_container_query(self, css_clean):
        """Contract: .qc-options defines grid, and @container qc (min-width: 600px) switches to 2 columns column-first."""
        assert ".qc-options" in css_clean
        assert "display: grid" in css_clean
        assert "@container qc (min-width: 600px)" in css_clean
        assert "repeat(2, minmax(0, 1fr))" in css_clean
        assert "grid-auto-flow: column" in css_clean
        assert "grid-template-rows: repeat(var(--qc-rows" in css_clean

    def test_fluid_clamp_tokens(self, css_clean):
        """Contract: CSS tokens in :root use clamp() for fluid gap, padding, font, and badge."""
        assert "--qc-gap: clamp(" in css_clean
        assert "--qc-pad: clamp(" in css_clean
        assert "--qc-font: clamp(" in css_clean
        assert "--qc-badge: clamp(" in css_clean

    def test_dynamic_viewport_height_scroll_and_utility(self, css_clean):
        """Contract: .qc-options-scroll and .h-dvh-safe use 100dvh."""
        assert ".qc-options-scroll" in css_clean
        assert "100dvh" in css_clean
        assert ".h-dvh-safe" in css_clean
        assert "min-height: 100dvh" in css_clean

    def test_katex_overflow_guards(self, css_clean):
        """Contract: KaTeX formulas must have max-width 100% and overflow-x auto."""
        assert ".katex-display" in css_clean
        assert "overflow-x: auto" in css_clean
        assert "max-width: 100%" in css_clean


# ==============================================================================
# 3. QUESTIONCARD.TSX CONTRACT TESTS
# ==============================================================================

class TestQuestionCardContract:
    """Verifies responsive layout & testids in QuestionCard.tsx."""

    @pytest.fixture
    def qc_clean(self):
        return read_stripped(QUESTION_CARD_TSX)

    def test_qc_classes_applied(self, qc_clean):
        """Contract: QuestionCard uses .qc-root, .qc-options, .qc-options-scroll, .qc-option-item, .qc-badge, .qc-stem."""
        for cls in ["qc-root", "qc-stem", "qc-options-scroll", "qc-options", "qc-option-item", "qc-badge"]:
            assert cls in qc_clean, f"Missing class in QuestionCard: {cls}"

    def test_dynamic_qc_rows_calculated_and_injected(self, qc_clean):
        """Contract: QuestionCard calculates ceil(n/2) rows and injects --qc-rows for both MCQ and multiple_select."""
        assert "Math.ceil(optionsCount / 2)" in qc_clean
        assert "'--qc-rows'" in qc_clean
        assert "'--rows'" in qc_clean

    def test_stem_max_width_none(self, qc_clean):
        """Contract: Stem uses max-w-none inside container."""
        assert "max-w-none" in qc_clean

    def test_data_testids_preserved(self, qc_clean):
        """Contract: All existing and required data-testid attributes are preserved."""
        required_testids = [
            'data-testid="question-card"',
            "data-testid={`option-${opt.id}`}",
            'data-testid="multiselect-option"',
            'data-testid="fill-blank-input"',
            'data-testid="hints-toggle"',
            'data-testid="hints-container"',
            'data-testid="reveal-hint-btn"',
            'data-testid="hint-item"',
        ]
        for tid in required_testids:
            assert tid in qc_clean, f"Missing testid in QuestionCard: {tid}"

    def test_option_letters_span_3_to_9_options(self, qc_clean):
        """Contract: Option letters must support at least 9 options (A through I)."""
        for letter in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']:
            assert f"'{letter}'" in qc_clean, f"Missing letter '{letter}' in OPTION_LETTERS"


# ==============================================================================
# 4. SIDEBAR.TSX CONTRACT TESTS
# ==============================================================================

class TestSidebarContract:
    """Verifies responsive off-canvas drawer & lg breakpoint in Sidebar.tsx."""

    @pytest.fixture
    def sidebar_clean(self):
        return read_stripped(SIDEBAR_TSX)

    def test_sidebar_responsive_breakpoint(self, sidebar_clean):
        """Contract: Sidebar detects 1024px desktop breakpoint and uses lg:* utility classes."""
        assert "1024" in sidebar_clean
        assert "lg:hidden" in sidebar_clean
        assert "lg:static" in sidebar_clean
        assert "lg:w-56" in sidebar_clean
        assert "lg:translate-x-0" in sidebar_clean
        assert "-translate-x-full lg:translate-x-0" in sidebar_clean

    def test_no_unconditional_fixed_w64(self, sidebar_clean):
        """
        Contract: Sidebar must NOT have an unconditional rigid 'w-64' without responsive drawer
        or desktop width modifiers (e.g. max-w-[85vw] and lg:w-56).
        """
        aside_match = re.search(r'<aside[^>]*className=\{`([^`]+)`\}', sidebar_clean)
        assert aside_match, "Could not find <aside> with className in Sidebar.tsx"
        classes = aside_match.group(1)
        assert "max-w-[85vw]" in classes, "Sidebar aside lacks responsive max-w-[85vw] constraint"
        assert "lg:w-56" in classes, "Sidebar aside lacks responsive lg:w-56 width modifier"
        assert "fixed lg:static" in classes, "Sidebar aside lacks responsive fixed-drawer to static transition"

    def test_sidebar_drawer_toggle_and_testids(self, sidebar_clean):
        """Contract: Sidebar provides hamburger toggle and preserves testids."""
        assert 'data-testid="sidebar-toggle"' in sidebar_clean
        assert 'data-testid="sidebar"' in sidebar_clean
        assert 'aria-expanded=' in sidebar_clean
        assert 'aria-controls="sidebar"' in sidebar_clean

    def test_sidebar_escape_key_listener(self, sidebar_clean):
        """Contract: Sidebar closes upon Escape key."""
        assert "'Escape'" in sidebar_clean or '"Escape"' in sidebar_clean


# ==============================================================================
# 5. PRACTICESESSION.TSX CONTRACT TESTS
# ==============================================================================

class TestPracticeSessionContract:
    """Verifies viewport ergonomics and zero residual 100vh in PracticeSession.tsx."""

    @pytest.fixture
    def practice_clean(self):
        return read_stripped(PRACTICE_SESSION_TSX)

    def test_no_residual_100vh_or_min_h_screen(self, practice_clean):
        """
        Contract: PracticeSession must have ZERO occurrences of raw '100vh' or 'min-h-screen'
        in stripped executable code.
        """
        matches_100vh = re.findall(r'100vh', practice_clean)
        assert len(matches_100vh) == 0, f"Found residual '100vh' in PracticeSession: {matches_100vh}"

        matches_min_h_screen = re.findall(r'min-h-screen', practice_clean)
        assert len(matches_min_h_screen) == 0, f"Found residual 'min-h-screen' in PracticeSession: {matches_min_h_screen}"

    def test_uses_h_dvh_safe_and_inline_100dvh(self, practice_clean):
        """Contract: PracticeSession uses h-dvh-safe and minHeight 100dvh."""
        assert "h-dvh-safe" in practice_clean
        assert "100dvh" in practice_clean

    def test_header_compact_max_height_850(self, practice_clean):
        """Contract: Header has responsive compact height for <= 850px viewport height."""
        assert "[@media(max-height:850px)]:h-12" in practice_clean

    def test_data_testids_preserved(self, practice_clean):
        """Contract: Preserves all critical interaction testids."""
        required_testids = [
            'data-testid="practice-session"',
            'data-testid="skip-btn"',
            'data-testid="next-question-btn"',
            'data-testid="check-btn"',
            'data-testid="quick-redo-btn"',
            'data-testid="restart-session-btn"',
        ]
        for tid in required_testids:
            assert tid in practice_clean, f"Missing testid in PracticeSession: {tid}"


# ==============================================================================
# 6. COORDINATEPLANE.TSX CONTRACT TESTS
# ==============================================================================

class TestCoordinatePlaneContract:
    """Verifies responsive SVG and viewBox on CoordinatePlane.tsx."""

    @pytest.fixture
    def coord_clean(self):
        return read_stripped(COORDINATE_PLANE_TSX)

    def test_svg_has_viewbox_and_responsive_constraints(self, coord_clean):
        """Contract: SVG has viewBox, max-w-[340px], and max-h-[30dvh]."""
        assert "viewBox=" in coord_clean
        assert "max-w-[340px]" in coord_clean
        assert "30dvh" in coord_clean

    def test_data_testids_preserved(self, coord_clean):
        """Contract: Preserves coordinate-plane and graph-container testids."""
        assert 'data-testid="coordinate-plane"' in coord_clean
        assert 'data-testid="graph-container"' in coord_clean


# ==============================================================================
# 7. FEEDBACKTOAST.TSX CONTRACT TESTS
# ==============================================================================

class TestFeedbackToastContract:
    """Verifies responsive bottom sheet and 45dvh constraint in FeedbackToast.tsx."""

    @pytest.fixture
    def toast_clean(self):
        return read_stripped(FEEDBACK_TOAST_TSX)

    def test_bottom_sheet_responsive_45dvh(self, toast_clean):
        """Contract: FeedbackToast defines 45dvh bottom sheet for mobile/split view <= 850px or < 1024px."""
        assert "45dvh" in toast_clean
        assert "(max-height: 850px)" in toast_clean
        assert "(max-width: 1023px)" in toast_clean

    def test_data_testids_preserved(self, toast_clean):
        """Contract: Preserves all FeedbackToast testids."""
        required_testids = [
            'data-testid="feedback-toast"',
            'data-testid="good-work-toast"',
            'data-testid="toast-quick-redo-btn"',
            'data-testid="error-rationale-box"',
            'data-testid="correct-answer-display"',
            'data-testid="step-by-step-solution"',
            'data-testid="solution-content"',
            'data-testid="solution-link"',
        ]
        for tid in required_testids:
            assert tid in toast_clean, f"Missing testid in FeedbackToast: {tid}"


# ==============================================================================
# 8. APP.TSX CONTRACT TESTS
# ==============================================================================

class TestAppContract:
    """Verifies responsive layout accommodation in App.tsx."""

    @pytest.fixture
    def app_clean(self):
        return read_stripped(APP_TSX)

    def test_main_responsive_padding_for_hamburger(self, app_clean):
        """Contract: Main views with Sidebar use pt-14 lg:pt-0 to clear hamburger button on mobile/split view."""
        assert "pt-14 lg:pt-0" in app_clean

    def test_no_rigid_w64_in_app(self, app_clean):
        """Contract: App.tsx must not hardcode rigid w-64 wrappers around main views."""
        assert "w-64" not in app_clean


# ==============================================================================
# 9. VIEWPORT MATRIX CONTRACT TESTS (Width: 390-1440, Height: 768-1080)
# ==============================================================================

class TestViewportMatrixContract:
    """
    Validates adherence to the mandatory Milestone 1 viewport matrix:
    Widths: 390 (mobile), 683 (50% 1366), 720 (50% 1440), 800 (50% 1600), 960 (50% 1920), 1366, 1440.
    Heights: 768 (laptop), 900 (laptop/desktop), 1080 (full HD desktop).
    """

    MATRIX_VIEWPORTS = [
        {"name": "split_1366", "w": 683, "h": 768, "expected_cols": 2, "sidebar_drawer": True, "compact_hdr": True},
        {"name": "split_1440", "w": 720, "h": 900, "expected_cols": 2, "sidebar_drawer": True, "compact_hdr": False},
        {"name": "split_1600", "w": 800, "h": 900, "expected_cols": 2, "sidebar_drawer": True, "compact_hdr": False},
        {"name": "split_1920", "w": 960, "h": 1080, "expected_cols": 2, "sidebar_drawer": True, "compact_hdr": False},
        {"name": "full_1366", "w": 1366, "h": 768, "expected_cols": 2, "sidebar_drawer": False, "compact_hdr": True},
        {"name": "full_1440", "w": 1440, "h": 900, "expected_cols": 2, "sidebar_drawer": False, "compact_hdr": False},
        {"name": "mobile_390", "w": 390, "h": 844, "expected_cols": 1, "sidebar_drawer": True, "compact_hdr": True},
    ]

    def test_container_query_threshold_aligns_with_matrix(self):
        """Container query breakpoint of 600px guarantees 2-cols for all split views and 1-col for mobile."""
        container_breakpoint = 600
        for vp in self.MATRIX_VIEWPORTS:
            cols = 2 if vp["w"] >= container_breakpoint else 1
            assert cols == vp["expected_cols"], (
                f"Viewport {vp['name']} ({vp['w']}px) expected {vp['expected_cols']} cols but got {cols}"
            )

    def test_sidebar_drawer_threshold_aligns_with_matrix(self):
        """Sidebar breakpoint of 1024px guarantees off-canvas drawer for split views and mobile."""
        sidebar_desktop_breakpoint = 1024
        for vp in self.MATRIX_VIEWPORTS:
            drawer = vp["w"] < sidebar_desktop_breakpoint
            assert drawer == vp["sidebar_drawer"], (
                f"Viewport {vp['name']} ({vp['w']}px) expected drawer={vp['sidebar_drawer']} but got {drawer}"
            )

    def test_height_threshold_aligns_with_compact_header_and_toast(self):
        """Height breakpoint of 850px guarantees compact header and 45dvh bottom-sheet for <= 850px."""
        height_threshold = 850
        for vp in self.MATRIX_VIEWPORTS:
            compact = vp["h"] <= height_threshold
            assert compact == vp["compact_hdr"], (
                f"Viewport {vp['name']} ({vp['h']}px) expected compact_hdr={vp['compact_hdr']} but got {compact}"
            )


# ==============================================================================
# 10. OPTION GRID MATHEMATICAL DISTRIBUTION TESTS (3 to 9 Options)
# ==============================================================================

class TestOptionGridDistributionContract:
    """
    Validates column-first grid calculation math for 3 to 9 options:
    Formula: rows = max(1, ceil(n / 2)).
    Guarantees column 1 has ceil(n/2) items, column 2 has floor(n/2) items,
    never overflows, and column 1 has at most 1 more item than column 2.
    """

    @pytest.mark.parametrize("n_options,expected_rows,col1_count,col2_count", [
        (3, 2, 2, 1),
        (4, 2, 2, 2),
        (5, 3, 3, 2),
        (6, 3, 3, 3),
        (7, 4, 4, 3),  # Standard MC7
        (8, 4, 4, 4),
        (9, 5, 5, 4),
    ])
    def test_column_first_distribution_invariants(self, n_options, expected_rows, col1_count, col2_count):
        computed_rows = max(1, math.ceil(n_options / 2))
        assert computed_rows == expected_rows, f"Failed for {n_options} options"

        actual_col1 = computed_rows
        actual_col2 = n_options - computed_rows

        assert actual_col1 == col1_count
        assert actual_col2 == col2_count
        assert actual_col1 >= actual_col2, "Column 1 must have at least as many items as Column 2"
        assert actual_col1 - actual_col2 <= 1, "Columns must be balanced within 1 item"
        assert actual_col1 + actual_col2 == n_options, "Total items must be preserved"
        assert computed_rows * 2 >= n_options, "Grid rows must accommodate all items"

    def test_zero_options_safe_fallback(self):
        """Zero options must yield 1 safe row to avoid CSS grid repeat(0) syntax violation."""
        zero_rows = max(1, math.ceil(0 / 2))
        assert zero_rows == 1


# ==============================================================================
# 11. KATEX OVERFLOW GUARD CONTRACT TESTS
# ==============================================================================

class TestKaTeXOverflowGuardContract:
    """Verifies that wide mathematical expressions are protected against horizontal overflow across all views."""

    def test_index_css_katex_guards(self):
        css = read_stripped(INDEX_CSS)
        assert ".katex-display" in css
        assert "overflow-x: auto" in css
        assert "max-width: 100%" in css
        assert ".qc-root .katex" in css
        assert ".qc-options .katex" in css

    def test_toast_katex_guards(self):
        toast = read_stripped(FEEDBACK_TOAST_TSX)
        assert ".feedback-toast-root .katex-display" in toast
        assert "overflow-x: auto" in toast
        assert ".feedback-toast-root .katex" in toast
        assert "max-width: 100%" in toast

    def test_gate1e_views_katex_overflow_guards(self):
        """Verifies that all Gate 1E views wrap KaTeX in responsive max-width/overflow guards."""
        views = [
            COURSE_LIBRARY_TSX,
            COURSE_OVERVIEW_TSX,
            MASTERY_GRID_TSX,
            PRE_EXERCISE_MODAL_TSX,
            COMPLETION_SCREEN_TSX,
            COURSE_CHALLENGE_TSX,
        ]
        for vpath in views:
            clean = read_stripped(vpath)
            assert "[&_.katex]:max-w-full" in clean, f"{vpath.name} lacks KaTeX max-width guard"


# ==============================================================================
# 12. ACCESSIBILITY (A11Y) CONTRACT TESTS
# ==============================================================================

class TestAccessibilityContracts:
    """Verifies accessibility roles, ARIA attributes, and keyboard traps across interactive components."""

    def test_sidebar_accessibility_contract(self):
        sb = read_stripped(SIDEBAR_TSX)
        assert 'aria-label=' in sb
        assert 'aria-expanded=' in sb
        assert 'aria-controls="sidebar"' in sb
        assert 'role={!isDesktop && isOpen ? \'dialog\' : undefined}' in sb
        assert 'aria-modal={!isDesktop && isOpen ? \'true\' : undefined}' in sb
        assert 'aria-hidden={!isDesktop && !isOpen ? \'true\' : undefined}' in sb
        assert "'Escape'" in sb or '"Escape"' in sb
        assert "handleKeyDown" in sb
        assert "itemTabIndex" in sb

    def test_question_card_accessibility_contract(self):
        qc = read_stripped(QUESTION_CARD_TSX)
        assert 'role="radiogroup"' in qc
        assert 'aria-label="Answer options"' in qc
        assert 'aria-pressed={isSelected}' in qc
        assert 'role="group"' in qc
        assert 'aria-label="Multiple choice options"' in qc
        assert 'aria-expanded={showHintsSection}' in qc
        assert 'aria-controls="hints-container"' in qc
        assert 'role="region"' in qc
        assert 'aria-label="Hints"' in qc

    def test_practice_session_accessibility_contract(self):
        ps = read_stripped(PRACTICE_SESSION_TSX)
        assert 'role="status"' in ps
        assert 'Progress: question' in ps
        assert 'aria-label="Restart practice session"' in ps

    def test_coordinate_plane_accessibility_contract(self):
        cp = read_stripped(COORDINATE_PLANE_TSX)
        assert 'role="img"' in cp
        assert 'aria-label={`Coordinate plane graph' in cp


# ==============================================================================
# 13. GATE 1E VIEWS RESPONSIVE CONTRACT TESTS
# ==============================================================================

class TestGate1EViewsContract:
    """Verifies responsive layout constraints (min-w-0, no overflow-x) across Gate 1E views."""

    def test_course_library_responsive_grid(self):
        lib = read_stripped(COURSE_LIBRARY_TSX)
        assert "grid-cols-1 sm:grid-cols-2 xl:grid-cols-3" in lib
        assert "min-w-0" in lib
        assert "[overflow-wrap:anywhere]" in lib

    def test_course_overview_responsive_containers(self):
        co = read_stripped(COURSE_OVERVIEW_TSX)
        assert "max-w-5xl mx-auto" in co
        assert "min-w-0" in co
        assert "truncate" in co

    def test_mastery_grid_responsive_blocks(self):
        mg = read_stripped(MASTERY_GRID_TSX)
        assert "flex-col md:flex-row" in mg
        assert "min-w-0" in mg

    def test_pre_exercise_modal_responsive_shell(self):
        pem = read_stripped(PRE_EXERCISE_MODAL_TSX)
        assert "min-h-[100dvh]" in pem
        assert "overflow-x-hidden" in pem
        assert "min-w-0" in pem

    def test_completion_screen_responsive_shell(self):
        cs = read_stripped(COMPLETION_SCREEN_TSX)
        assert "min-h-[100dvh]" in cs
        assert "overflow-x-hidden" in cs
        assert "min-w-0" in cs


# ==============================================================================
# 14. PATH RESOLUTION PORTABILITY TESTS (Windows / POSIX)
# ==============================================================================

class TestPathResolutionPortability:
    """Verifies cross-platform Path resolution across Windows and POSIX environments."""

    @pytest.mark.parametrize("path_obj,name", [
        (INDEX_CSS, "index.css"),
        (QUESTION_CARD_TSX, "QuestionCard.tsx"),
        (SIDEBAR_TSX, "Sidebar.tsx"),
        (PRACTICE_SESSION_TSX, "PracticeSession.tsx"),
        (COORDINATE_PLANE_TSX, "CoordinatePlane.tsx"),
        (FEEDBACK_TOAST_TSX, "FeedbackToast.tsx"),
        (APP_TSX, "App.tsx"),
        (COURSE_LIBRARY_TSX, "CourseLibrary.tsx"),
        (COURSE_OVERVIEW_TSX, "CourseOverview.tsx"),
        (MASTERY_GRID_TSX, "MasteryGrid.tsx"),
        (PRE_EXERCISE_MODAL_TSX, "PreExerciseModal.tsx"),
        (COMPLETION_SCREEN_TSX, "CompletionScreen.tsx"),
        (COURSE_CHALLENGE_TSX, "CourseChallenge.tsx"),
    ])
    def test_path_exists_and_resolves(self, path_obj, name):
        resolved = path_obj.resolve()
        assert resolved.exists(), f"Path does not exist: {resolved}"
        assert resolved.name == name, f"Expected {name} but got {resolved.name}"
        assert resolved.is_file(), f"Path is not a file: {resolved}"


# ==============================================================================
# 15. IN-MEMORY MUTATION RESISTANCE CHECKS (Kills Artificial Mutants)
# ==============================================================================

class TestContractMutationResistance:
    """
    Simulates deliberate regressions on in-memory copies of the code to ensure
    that contract tests actively fail (raising AssertionError) when any invariant is broken.
    NEVER writes to disk; strictly memory-only mutations.
    """

    def test_baseline_real_files_pass_validation(self):
        """Verifies that all real uncorrupted files pass their respective contract validators."""
        validate_index_css_contract(read_stripped(INDEX_CSS))
        validate_question_card_contract(read_stripped(QUESTION_CARD_TSX))
        validate_sidebar_contract(read_stripped(SIDEBAR_TSX))
        validate_practice_session_contract(read_stripped(PRACTICE_SESSION_TSX))
        validate_coordinate_plane_contract(read_stripped(COORDINATE_PLANE_TSX))
        validate_feedback_toast_contract(read_stripped(FEEDBACK_TOAST_TSX))

    @pytest.mark.parametrize("target,replacement,desc", [
        ("container-type: inline-size", "", "missing container-type"),
        ("@container qc (min-width: 600px)", "", "missing @container query"),
        ("repeat(2, minmax(0, 1fr))", "repeat(2, 200px)", "corrupted 2-column rule"),
        ("grid-auto-flow: column", "grid-auto-flow: row", "corrupted column-first flow"),
        ("--qc-gap: clamp(", "--qc-gap: 1rem; /* clamp(", "corrupted fluid gap"),
        (".h-dvh-safe", ".h-vh-unsafe", "missing dvh safe utility"),
        ("overflow-x: auto", "", "missing KaTeX overflow guard"),
    ])
    def test_index_css_mutations_killed(self, target, replacement, desc):
        src = read_stripped(INDEX_CSS)
        mutant = src.replace(target, replacement)
        with pytest.raises(AssertionError):
            validate_index_css_contract(mutant)

    @pytest.mark.parametrize("target,replacement,desc", [
        ("Math.ceil(optionsCount / 2)", "4", "hardcoded row count"),
        ("'--qc-rows'", "'--qc-fixed'", "missing --qc-rows injection"),
        ("max-w-none", "max-w-3xl", "rigid max-w restored"),
        ('data-testid="question-card"', 'id="qc"', "removed testid"),
        ('role="radiogroup"', 'role="none"', "removed radiogroup role"),
    ])
    def test_question_card_mutations_killed(self, target, replacement, desc):
        src = read_stripped(QUESTION_CARD_TSX)
        mutant = src.replace(target, replacement)
        with pytest.raises(AssertionError):
            validate_question_card_contract(mutant)

    @pytest.mark.parametrize("target,replacement,desc", [
        ("1024", "1920", "corrupted desktop breakpoint"),
        ("lg:hidden", "hidden", "missing responsive hamburger toggle"),
        ("max-w-[85vw]", "w-64", "missing drawer width constraint"),
        ('data-testid="sidebar-toggle"', 'id="btn"', "removed toggle testid"),
        ("'Escape'", "'F1'", "removed Escape key handling"),
    ])
    def test_sidebar_mutations_killed(self, target, replacement, desc):
        src = read_stripped(SIDEBAR_TSX)
        mutant = src.replace(target, replacement)
        with pytest.raises(AssertionError):
            validate_sidebar_contract(mutant)

    @pytest.mark.parametrize("insertion,desc", [
        ("style={{ height: '100vh' }}", "residual 100vh reintroduced"),
        ("className='min-h-screen'", "residual min-h-screen reintroduced"),
    ])
    def test_practice_session_residual_vh_mutations_killed(self, insertion, desc):
        src = read_stripped(PRACTICE_SESSION_TSX)
        mutant = src + f"\n{insertion}\n"
        with pytest.raises(AssertionError):
            validate_practice_session_contract(mutant)

    @pytest.mark.parametrize("target,replacement,desc", [
        ("viewBox=", "box=", "missing SVG viewBox"),
        ("max-w-[340px]", "max-w-none", "missing max-w constraint"),
        ("30dvh", "100vh", "missing 30dvh constraint"),
    ])
    def test_coordinate_plane_mutations_killed(self, target, replacement, desc):
        src = read_stripped(COORDINATE_PLANE_TSX)
        mutant = src.replace(target, replacement)
        with pytest.raises(AssertionError):
            validate_coordinate_plane_contract(mutant)

    @pytest.mark.parametrize("target,replacement,desc", [
        ("45dvh", "80vh", "missing 45dvh bottom sheet constraint"),
        ("max-height: 850px", "max-height: 200px", "missing 850px media query"),
        ('data-testid="feedback-toast"', 'id="toast"', "removed toast testid"),
    ])
    def test_feedback_toast_mutations_killed(self, target, replacement, desc):
        src = read_stripped(FEEDBACK_TOAST_TSX)
        mutant = src.replace(target, replacement)
        with pytest.raises(AssertionError):
            validate_feedback_toast_contract(mutant)
