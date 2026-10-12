import time
import pytest
from pathlib import Path

SCREENSHOTS_DIR = Path(__file__).resolve().parent / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


def test_capture_six_canonical_states(page, setup_test_courses):
    """Visual Fidelity Parity Runner:
    Systematically traverses the application and captures high-fidelity screenshots
    corresponding to each of the 6 canonical reference images:
    1. Courser_overview.png -> 01_course_overview.png
    2. pre_exercise.png -> 02_pre_exercise.png
    3. multiple_answer_question.png -> 03_question_with_graph.png
    4. good_answer.png -> 04_good_answer_toast.png
    5. exercise_completed.png -> 05_exercise_complete_confetti.png
    6. course_challenge.png -> 06_course_challenge.png
    """
    page.set_viewport_size({"width": 1280, "height": 800})

    # --- STATE 1: Course Overview ---
    page.goto(page.base_url)
    page.wait_for_load_state("networkidle")

    # Enter differential calculus course
    course_link = page.locator("a:has-text('Differential Calculus'), button:has-text('Differential Calculus')")
    if course_link.count() > 0:
        course_link.first.click()
        page.wait_for_load_state("networkidle")

    page.wait_for_timeout(500)
    state1_path = SCREENSHOTS_DIR / "01_course_overview.png"
    page.screenshot(path=str(state1_path), full_page=True)
    assert state1_path.exists(), "Failed to save 01_course_overview.png"

    # --- STATE 2: Pre-Exercise Screen ("Ready to practice?") ---
    unit_trigger = page.locator(
        "[data-testid^='competency-']:has-text('Limits intro'), button:has-text('Limits intro'), button:has-text('Practice')"
    )
    if unit_trigger.count() > 0:
        unit_trigger.first.click()
        page.wait_for_timeout(500)

    state2_path = SCREENSHOTS_DIR / "02_pre_exercise.png"
    page.screenshot(path=str(state2_path))
    assert state2_path.exists(), "Failed to save 02_pre_exercise.png"

    # --- STATE 3: Question with Graph ---
    lets_go = page.locator("button:has-text(\"Let's go\"), [data-testid='start-practice-btn']")
    if lets_go.count() > 0 and lets_go.first.is_visible():
        lets_go.first.click()
        page.wait_for_load_state("networkidle")

    # Navigate to question with graph if not on first item
    for _ in range(4):
        has_graph = page.locator(
            "[data-testid='coordinate-plane'], svg.coordinate-plane, svg circle, svg path"
        ).count() > 0
        if has_graph:
            break
        skip_btn = page.locator("button:has-text('Skip'), [data-testid='skip-btn']")
        if skip_btn.is_visible() and skip_btn.is_enabled():
            skip_btn.click()
            page.wait_for_timeout(300)

    page.wait_for_timeout(500)
    state3_path = SCREENSHOTS_DIR / "03_question_with_graph.png"
    page.screenshot(path=str(state3_path))
    assert state3_path.exists(), "Failed to save 03_question_with_graph.png"

    # --- STATE 4: Correct Answer Feedback Toast ("Good work!") ---
    # Select correct option ($-4$)
    opt_correct = page.locator("[data-testid^='option-']:has-text('-4'), .option-item:has-text('-4')")
    if opt_correct.count() > 0:
        opt_correct.first.click()
    else:
        # Fallback to second option
        options = page.locator("[data-testid^='option-'], .option-item")
        if options.count() >= 2:
            options.nth(1).click()

    check_btn = page.locator("button:has-text('Check'), [data-testid='check-btn']").first
    if check_btn.is_enabled():
        check_btn.click()
        page.wait_for_timeout(600)

    state4_path = SCREENSHOTS_DIR / "04_good_answer_toast.png"
    page.screenshot(path=str(state4_path))
    assert state4_path.exists(), "Failed to save 04_good_answer_toast.png"

    # --- STATE 5: Exercise Complete Screen with Confetti ---
    # Step through remaining questions to completion
    for _ in range(8):
        completion = page.locator(
            "[data-testid='completion-screen'], :text-matches('Exercise complete', 'i')"
        )
        if completion.count() > 0 and completion.first.is_visible():
            break

        next_btn = page.locator("button:has-text('Next question'), button:has-text('Next'), [data-testid='next-question-btn']")
        if next_btn.count() > 0 and next_btn.first.is_visible():
            next_btn.first.click()
            page.wait_for_timeout(300)
            continue

        skip_btn = page.locator("button:has-text('Skip'), [data-testid='skip-btn']")
        if skip_btn.count() > 0 and skip_btn.first.is_visible() and skip_btn.first.is_enabled():
            skip_btn.first.click()
            page.wait_for_timeout(300)

    page.wait_for_timeout(600)
    state5_path = SCREENSHOTS_DIR / "05_exercise_complete_confetti.png"
    page.screenshot(path=str(state5_path))
    assert state5_path.exists(), "Failed to save 05_exercise_complete_confetti.png"

    # --- STATE 6: Course Challenge Overview ---
    # Navigate to Comprehensive Challenge Course
    page.goto(page.base_url)
    page.wait_for_load_state("networkidle")

    challenge_course_link = page.locator(
        "a:has-text('Comprehensive Challenge'), button:has-text('Comprehensive Challenge')"
    )
    if challenge_course_link.count() > 0:
        challenge_course_link.first.click()
        page.wait_for_load_state("networkidle")

    # Click Course Challenge entry
    challenge_trigger = page.locator(
        "[data-testid='course-challenge-card'], a:has-text('Course challenge'), button:has-text('Course challenge')"
    )
    if challenge_trigger.count() > 0:
        challenge_trigger.first.click()
        page.wait_for_timeout(500)

    state6_path = SCREENSHOTS_DIR / "06_course_challenge.png"
    page.screenshot(path=str(state6_path))
    assert state6_path.exists(), "Failed to save 06_course_challenge.png"

    # Verify all 6 screenshots exist
    all_screenshots = [state1_path, state2_path, state3_path, state4_path, state5_path, state6_path]
    for s in all_screenshots:
        assert s.exists() and s.stat().st_size > 0, f"Screenshot file {s.name} is missing or empty!"
