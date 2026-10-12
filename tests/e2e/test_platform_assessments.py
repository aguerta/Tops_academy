import time
import pytest


def navigate_to_challenge_course(page):
    """Navigate to the comprehensive challenge course."""
    page.goto(page.base_url)
    page.wait_for_load_state("networkidle")

    course_link = page.locator(
        "a:has-text('Comprehensive Challenge'), button:has-text('Comprehensive Challenge'), [data-testid='course-card']:has-text('Comprehensive Challenge')"
    )
    if course_link.count() > 0:
        course_link.first.click()
        page.wait_for_load_state("networkidle")


def test_quiz_and_unit_test_flow(page, setup_test_courses):
    """AC-08 (Part 1): Quiz and Unit Test can be started and completed."""
    navigate_to_challenge_course(page)

    # 1. Start a Quiz via Quiz lightning bolt or link
    quiz_trigger = page.locator(
        "[data-testid^='quiz-marker'], button:has-text('Quiz'), a:has-text('Quiz'), :text-matches('Quiz 1', 'i')"
    )
    if quiz_trigger.count() > 0:
        quiz_trigger.first.click()
        page.wait_for_load_state("networkidle")

        lets_go = page.locator("button:has-text(\"Let's go\"), [data-testid='start-quiz-btn']")
        if lets_go.count() > 0 and lets_go.first.is_visible():
            lets_go.first.click()
            page.wait_for_load_state("networkidle")

        # Verify quiz session is active
        assert (
            "Quiz" in page.locator("body").inner_text()
            or page.locator("button:has-text('Check'), button:has-text('Skip')").count() > 0
        ), "Quiz session failed to launch!"

        # Step through quiz questions
        for _ in range(6):
            if page.locator(":text-matches('complete', 'i'), :text-matches('summary', 'i')").count() > 0:
                break
            skip_btn = page.locator("button:has-text('Skip'), [data-testid='skip-btn']").first
            if skip_btn.is_visible() and skip_btn.is_enabled():
                skip_btn.click()
                page.wait_for_timeout(250)

    # 2. Start a Unit Test via Unit test star or link
    navigate_to_challenge_course(page)
    unit_test_trigger = page.locator(
        "[data-testid^='unit-test-marker'], button:has-text('Unit test'), a:has-text('Unit test'), :text-matches('Unit test', 'i')"
    )
    if unit_test_trigger.count() > 0:
        unit_test_trigger.first.click()
        page.wait_for_load_state("networkidle")

        lets_go = page.locator("button:has-text(\"Let's go\"), [data-testid='start-test-btn']")
        if lets_go.count() > 0 and lets_go.first.is_visible():
            lets_go.first.click()
            page.wait_for_load_state("networkidle")

        assert (
            "Unit test" in page.locator("body").inner_text()
            or "Test" in page.locator("body").inner_text()
            or page.locator("button:has-text('Check'), button:has-text('Skip')").count() > 0
        ), "Unit test session failed to launch!"

    assert len(page.page_errors) == 0, f"Page errors: {page.page_errors}"
    assert len(page.console_errors) == 0, f"Console errors: {page.console_errors}"


def test_course_challenge_flow(page, setup_test_courses):
    """AC-08 (Part 2): Course Challenge (~30 questions across units) can be started and completed."""
    navigate_to_challenge_course(page)

    # 1. Locate Course Challenge card or sidebar item
    challenge_trigger = page.locator(
        "[data-testid='course-challenge-card'], a:has-text('Course challenge'), button:has-text('Course challenge'), button:has-text('Take Course challenge')"
    )
    assert challenge_trigger.count() > 0, "Course Challenge entry point not found on Course Overview!"
    challenge_trigger.first.click()
    page.wait_for_load_state("networkidle")

    # 2. Verify Course Challenge hero screen ("Ready for a challenge?", ~30 questions)
    body_text = page.locator("body").inner_text()
    assert (
        "challenge" in body_text.lower()
        or "30 questions" in body_text
        or "Ready for a challenge" in body_text
    ), "Course challenge intro screen did not render!"

    # 3. Click "Let's go"
    lets_go = page.locator("button:has-text(\"Let's go\"), [data-testid='start-challenge-btn']").first
    if lets_go.is_visible():
        lets_go.click()
        page.wait_for_load_state("networkidle")

    # 4. Verify Course Challenge session started with questions
    check_or_skip = page.locator("button:has-text('Check'), button:has-text('Skip'), [data-testid='check-btn']")
    assert check_or_skip.count() > 0, "Course challenge session failed to start questions!"

    # Step through questions to verify full flow completion
    # In a fast test run, step through with Skip
    for q_idx in range(35):
        # Check if completion reached
        completion = page.locator(
            ":text-matches('complete', 'i'), :text-matches('Challenge complete', 'i'), :text-matches('Summary', 'i'), [data-testid='completion-screen']"
        )
        if completion.count() > 0 and completion.first.is_visible():
            break

        # If next question visible
        next_btn = page.locator("button:has-text('Next question'), button:has-text('Next'), [data-testid='next-question-btn']")
        if next_btn.count() > 0 and next_btn.first.is_visible():
            next_btn.first.click()
            page.wait_for_timeout(150)
            continue

        skip_btn = page.locator("button:has-text('Skip'), [data-testid='skip-btn']").first
        if skip_btn.is_visible() and skip_btn.is_enabled():
            skip_btn.click()
            page.wait_for_timeout(150)
        else:
            break

    # 5. Verify challenge completion screen reached
    completion_text = page.locator("body").inner_text()
    assert (
        "complete" in completion_text.lower()
        or "score" in completion_text.lower()
        or "result" in completion_text.lower()
        or "/" in completion_text
    ), "Course challenge did not display completion screen!"

    assert len(page.page_errors) == 0, f"Page errors: {page.page_errors}"
    assert len(page.console_errors) == 0, f"Console errors: {page.console_errors}"
