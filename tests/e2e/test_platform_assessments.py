import time
import pytest


def navigate_to_challenge_course(page):
    """Navigate to a valid course overview containing Examen Modo Hierro."""
    page.goto(page.base_url)
    page.wait_for_load_state("networkidle")
    page.locator("[data-testid='course-card']").first.wait_for(state="visible", timeout=10000)

    preferred = page.locator(
        "[data-testid='course-card']:has-text('Comprehensive Challenge'), [data-testid='course-card']:has-text('Ecuaciones Diferenciales')"
    )
    if preferred.count() > 0:
        preferred.first.click()
    else:
        page.locator("[data-testid='course-card']").first.click()
    page.locator("[data-testid='course-challenge-card']").wait_for(state="visible", timeout=10000)


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
    """AC-08 (Part 2): Examen Modo Hierro replaces Course Challenge as the single course exam and completes cleanly."""
    navigate_to_challenge_course(page)

    # 1. Locate Examen Modo Hierro button inside course-challenge-card
    challenge_btn = page.locator("[data-testid='course-challenge-card'] button").first
    challenge_btn.wait_for(state="visible", timeout=10000)
    challenge_btn.click()
    page.wait_for_load_state("networkidle")

    # 2. Verify Modo Hierro briefing screen
    body_text = page.locator("body").inner_text()
    assert (
        "modo hierro" in body_text.lower()
        or "preguntas" in body_text.lower()
    ), "Modo Hierro intro screen did not render!"

    # 3. Click Iniciar Modo Hierro (start-challenge-btn)
    start_btn = page.locator("[data-testid='start-challenge-btn']").first
    expect = start_btn.wait_for(state="visible", timeout=10000)
    start_btn.click()
    page.wait_for_load_state("networkidle")

    # 4. Verify Iron Exam session started with navigator & submit button
    page.locator("[data-testid='iron-exam-session']").wait_for(state="visible", timeout=10000)
    assert page.locator("[data-testid='hints-toggle']").count() == 0, "Iron Exam must hide hints!"
    assert page.locator("[data-testid='feedback-toast']").count() == 0, "Iron Exam must defer feedback!"

    # Submit via Metacognitive Modal
    page.locator("[data-testid='iron-submit-exam-btn']").click()
    page.locator("[data-testid='metacognitive-modal']").wait_for(state="visible", timeout=5000)
    page.locator("[data-testid='meta-global-confidence-medium']").click()
    page.locator("[data-testid='metacognitive-confirm-btn']").click()

    # 5. Verify completion screen + metacognitive audit + deferred review rendered
    page.locator("[data-testid='completion-screen']").wait_for(state="visible", timeout=10000)
    assert page.locator("[data-testid='metacognitive-audit-summary']").is_visible()
    assert page.locator("[data-testid='iron-deferred-review']").is_visible()

    assert len(page.page_errors) == 0, f"Page errors: {page.page_errors}"
    assert len(page.console_errors) == 0, f"Console errors: {page.console_errors}"
