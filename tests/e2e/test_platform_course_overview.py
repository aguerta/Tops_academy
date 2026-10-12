import pytest


def navigate_to_calculus_course(page):
    """Helper to navigate to the calculus course overview."""
    page.goto(page.base_url)
    page.wait_for_load_state("networkidle")

    # If already on course overview (e.g. single-course auto-select), verify or click link
    course_link = page.locator(
        "a:has-text('Differential Calculus'), button:has-text('Differential Calculus'), [data-testid='course-card']:has-text('Differential Calculus')"
    )
    if course_link.count() > 0:
        course_link.first.click()
        page.wait_for_load_state("networkidle")


def test_course_overview_structure_and_legend(page, setup_test_courses):
    """AC-03: Course overview shows one unit per competency, mastery legend, and course mastery %."""
    navigate_to_calculus_course(page)

    body_text = page.locator("body").inner_text()

    # 1. Verify Course Mastery %
    assert (
        "Course mastery" in body_text
        or "mastery:" in body_text.lower()
        or "%" in body_text
    ), "Course mastery percentage metric not found on Course Overview!"

    # 2. Verify Mastery Legend elements
    # Legend should list Mastered, Proficient, Familiar, Attempted, Not started, Quiz, Unit test
    expected_legend_terms = [
        "Mastered",
        "Proficient",
        "Familiar",
        "Attempted",
        "Not started"
    ]
    for term in expected_legend_terms:
        assert term in body_text, f"Mastery legend item '{term}' not found in Course Overview!"

    # Verify quiz and unit test markers in legend or grid
    assert (
        "Quiz" in body_text or "⚡" in body_text
    ), "Quiz indicator not present in Mastery Legend / Matrix!"
    assert (
        "Unit test" in body_text or "★" in body_text or "Test" in body_text
    ), "Unit test indicator not present in Mastery Legend / Matrix!"

    # 3. Verify One Unit Per Competency
    # For valid_course_calculus, competencies are "Limits intro" and "Derivative definitions"
    assert "Limits intro" in body_text, "Unit for 'Limits intro' competency missing from Course Overview!"
    assert "Derivative definitions" in body_text, "Unit for 'Derivative definitions' competency missing!"

    # Verify Unit Completion Tracker Summary and Status Badges
    completion_summary = page.locator("[data-testid='completion-tracker-summary']")
    assert completion_summary.count() > 0, "Competency / Unit completion tracker summary not found!"
    assert "Unit Completion Status" in body_text or "Units Completed" in body_text, (
        "Unit Completion Status text not found on Course Overview!"
    )
    unit_statuses = page.locator("[data-testid^='unit-status-']")
    assert unit_statuses.count() >= 2, "Unit completion status badges missing from competency blocks!"
    status_text = unit_statuses.first.inner_text()
    assert (
        "Not Started" in status_text or "Completed" in status_text or "In Progress" in status_text
    ), f"Unexpected unit status text: {status_text}"

    # 4. Verify Left Sidebar with Units
    sidebar = page.locator("[data-testid='sidebar'], aside, nav")
    assert sidebar.count() > 0, "Navigation sidebar not found on Course Overview!"
    sidebar_text = sidebar.first.inner_text()
    assert (
        "Limits" in sidebar_text or "UNIT" in sidebar_text or "Calculus" in sidebar_text
    ), "Sidebar does not display course or unit navigation hierarchy!"

    # 5. Verify Zero Console Errors
    assert len(page.page_errors) == 0, f"Page errors: {page.page_errors}"
    assert len(page.console_errors) == 0, f"Console errors: {page.console_errors}"
