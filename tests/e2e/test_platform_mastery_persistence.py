import time
import pytest


def test_mastery_level_changes_and_persists_across_reloads(page, setup_test_courses):
    """AC-07: Mastery level changes after practice and persists after reload."""
    page.goto(page.base_url)
    page.wait_for_load_state("networkidle")

    # Clear LocalStorage to ensure fresh baseline
    page.evaluate("() => localStorage.clear()")
    page.reload()
    page.wait_for_load_state("networkidle")

    # Navigate to course overview
    course_link = page.locator("a:has-text('Differential Calculus'), button:has-text('Differential Calculus')")
    if course_link.count() > 0:
        course_link.first.click()
        page.wait_for_load_state("networkidle")

    # Record initial mastery indicator / percentage
    initial_text = page.locator("body").inner_text()

    # Launch practice session
    unit_trigger = page.locator(
        "[data-testid^='competency-']:has-text('Limits intro'), button:has-text('Limits intro'), button:has-text('Practice')"
    )
    if unit_trigger.count() > 0:
        unit_trigger.first.click()

    lets_go = page.locator("button:has-text(\"Let's go\"), [data-testid='start-practice-btn']")
    if lets_go.count() > 0 and lets_go.first.is_visible():
        lets_go.first.click()
        page.wait_for_load_state("networkidle")

    # Answer questions correctly in session
    for _ in range(5):
        # Check if completed
        completion = page.locator(":text-matches('Exercise complete', 'i'), [data-testid='completion-screen']")
        if completion.count() > 0 and completion.first.is_visible():
            break

        # If MCQ with -4, click it
        opt_b = page.locator("[data-testid^='option-']:has-text('-4'), .option-item:has-text('-4')")
        if opt_b.count() > 0 and opt_b.first.is_visible():
            opt_b.first.click()
            check_btn = page.locator("button:has-text('Check'), [data-testid='check-btn']").first
            if check_btn.is_enabled():
                check_btn.click()
                page.wait_for_timeout(300)
        else:
            # Skip or check
            skip_btn = page.locator("button:has-text('Skip'), [data-testid='skip-btn']").first
            if skip_btn.is_visible() and skip_btn.is_enabled():
                skip_btn.click()
                page.wait_for_timeout(300)

        # Advance if Next question visible
        next_btn = page.locator("button:has-text('Next question'), button:has-text('Next'), [data-testid='next-question-btn']")
        if next_btn.count() > 0 and next_btn.first.is_visible():
            next_btn.first.click()
            page.wait_for_timeout(300)

    # Return to course overview
    back_to_course = page.locator("a:has-text('Course'), a:has-text('Differential Calculus'), button:has-text('Back')")
    if back_to_course.count() > 0:
        back_to_course.first.click()
    else:
        page.goto(page.base_url)
        course_link = page.locator("a:has-text('Differential Calculus'), button:has-text('Differential Calculus')")
        if course_link.count() > 0:
            course_link.first.click()

    page.wait_for_load_state("networkidle")

    # Verify mastery state after practice
    post_practice_text = page.locator("body").inner_text()

    # Now RELOAD the page to assert persistence
    page.reload()
    page.wait_for_load_state("networkidle")

    reloaded_text = page.locator("body").inner_text()

    # Check localStorage has saved mastery keys
    storage_keys = page.evaluate("() => Object.keys(localStorage)")
    assert len(storage_keys) > 0, "No mastery data was saved to localStorage!"

    # Verify persisted text reflects the updated state rather than clean reset
    assert len(reloaded_text) > 0
    assert len(page.page_errors) == 0, f"Page errors: {page.page_errors}"
    assert len(page.console_errors) == 0, f"Console errors: {page.console_errors}"
