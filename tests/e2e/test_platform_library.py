import time
import shutil
import pytest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
COURSES_DIR = ROOT_DIR / "courses"
FIXTURES_DIR = COURSES_DIR / "test_fixtures"


def test_library_lists_all_courses(page, setup_test_courses):
    """AC-01: Verify that the Library lists every course in the courses/ folder."""
    page.goto(page.base_url)
    page.wait_for_load_state("networkidle")

    # The course list should contain test_differential_calculus and test_course_challenge
    body_text = page.locator("body").inner_text()
    assert (
        "Differential Calculus" in body_text
        or "test-differential-calculus" in body_text
        or "Limits" in body_text
    ), f"Expected course not listed on homepage. Body text: {body_text[:300]}"

    # Verify Completed badge tracking functionality in Library
    page.evaluate("""() => {
        const testMastery = {
            'test-differential-calculus': {
                course_id: 'test-differential-calculus',
                mastery_points: 100,
                competencies: {
                    'COMP-LIM-01': { status: 'Mastered', points: 100, last_practiced: '', history: [] },
                    'COMP-DER-01': { status: 'Mastered', points: 100, last_practiced: '', history: [] }
                }
            }
        };
        localStorage.setItem('khan_academic_progress_v1', JSON.stringify(testMastery));
    }""")
    page.reload()
    page.wait_for_load_state("networkidle")
    completed_badge = page.locator("[data-testid='course-completed-badge']")
    assert completed_badge.count() > 0, "Course completed badge not visible for 100% mastered course in library!"
    assert "Completed" in completed_badge.first.inner_text(), "Completed badge text missing!"
    page.evaluate("() => localStorage.clear()")
    page.reload()
    page.wait_for_load_state("networkidle")

    # Verify no unhandled exceptions occurred
    assert len(page.page_errors) == 0, f"Page errors encountered: {page.page_errors}"
    assert len(page.console_errors) == 0, f"Console errors encountered: {page.console_errors}"


def test_dynamic_course_hot_reload(page, setup_test_courses):
    """AC-01: Copying a new valid course file into courses/ makes it appear after reload with no code change."""
    dynamic_course_path = COURSES_DIR / "hot_reloaded_course.json"
    try:
        # Load library before adding new course
        page.goto(page.base_url)
        page.wait_for_load_state("networkidle")

        initial_text = page.locator("body").inner_text()
        assert "Hot Reloaded Dynamic Course" not in initial_text

        # Create a new course file dynamically in courses/
        shutil.copy2(FIXTURES_DIR / "valid_course_calculus.json", dynamic_course_path)
        with open(dynamic_course_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("Differential Calculus (Test Fixture)", "Hot Reloaded Dynamic Course")
        content = content.replace("test-differential-calculus", "hot-reloaded-course")
        with open(dynamic_course_path, "w", encoding="utf-8") as f:
            f.write(content)

        # Reload the page
        time.sleep(0.5)  # allow disk sync
        page.reload()
        page.wait_for_load_state("networkidle")

        # Verify the new course now appears in the library
        updated_text = page.locator("body").inner_text()
        assert "Hot Reloaded Dynamic Course" in updated_text, (
            "Dynamically added course did not appear after page reload!"
        )

        assert len(page.page_errors) == 0, f"Page errors: {page.page_errors}"
    finally:
        if dynamic_course_path.exists():
            dynamic_course_path.unlink()


def test_invalid_course_isolated_with_error(page, setup_test_courses):
    """AC-02: An invalid course file shows an error for that course while other courses still work."""
    invalid_course_path = COURSES_DIR / "z_corrupted_test_course.json"
    try:
        # Copy corrupt fixture into courses/
        shutil.copy2(FIXTURES_DIR / "invalid_corrupt_course.json", invalid_course_path)

        page.goto(page.base_url)
        page.wait_for_load_state("networkidle")

        body_text = page.locator("body").inner_text()

        # 1. Check that the valid course still displays and is accessible
        assert (
            "Differential Calculus" in body_text
            or "test-differential-calculus" in body_text
        ), "Valid course disappeared when an invalid course was added!"

        # 2. Check that the invalid course displays an error state / warning card
        error_indicators = page.locator(
            "[data-testid='course-error-card'], .course-error, :text-matches('Error', 'i'), :text-matches('Invalid', 'i'), :text-matches('Corrupted', 'i')"
        )
        assert error_indicators.count() > 0 or "Error" in body_text or "corrupt" in body_text.lower(), (
            "No error indicator displayed for invalid course!"
        )

        # 3. Verify valid course can still be opened/clicked
        valid_card = page.locator(
            "[data-testid='course-card']:has-text('Differential Calculus'), a:has-text('Differential Calculus'), button:has-text('Differential Calculus')"
        )
        if valid_card.count() > 0:
            valid_card.first.click()
            page.wait_for_load_state("networkidle")
            # Should enter course overview
            assert "Limits" in page.locator("body").inner_text()

    finally:
        if invalid_course_path.exists():
            invalid_course_path.unlink()
