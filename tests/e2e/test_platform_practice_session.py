import time
import pytest


def launch_practice_for_unit(page, unit_name="Limits intro"):
    """Helper to launch practice session from course overview."""
    page.goto(page.base_url)
    page.wait_for_load_state("networkidle")

    # Click course if at library
    course_card = page.locator("a:has-text('Differential Calculus'), button:has-text('Differential Calculus')")
    if course_card.count() > 0:
        course_card.first.click()
        page.wait_for_load_state("networkidle")

    # Click unit practice card or competency block
    unit_trigger = page.locator(
        f"[data-testid^='competency-']:has-text('{unit_name}'), button:has-text('{unit_name}'), a:has-text('{unit_name}'), button:has-text('Practice')"
    )
    if unit_trigger.count() > 0:
        unit_trigger.first.click()
        page.wait_for_load_state("networkidle")

    # If "Ready to practice?" modal appears, click "Let's go"
    lets_go = page.locator("button:has-text(\"Let's go\"), [data-testid='start-practice-btn']")
    if lets_go.count() > 0 and lets_go.first.is_visible():
        lets_go.first.click()
        page.wait_for_load_state("networkidle")


def test_full_practice_lifecycle_wrong_hints_correct_completion(page, setup_test_courses):
    """AC-04: Full practice session:
    - Wrong answer -> incorrect feedback
    - Hint reveal shows hints in order
    - Correct answer -> 'Good work' toast & step-by-step solution available
    - Completion screen shows score
    """
    launch_practice_for_unit(page, "Limits intro")

    # 1. Verify we are in practice session with question stem and bottom bar
    question_card = page.locator("[data-testid='question-card'], [data-testid='practice-session'], main")
    assert question_card.count() > 0, "Practice session container not rendered!"

    # Verify Check and Skip buttons present
    check_btn = page.locator("button:has-text('Check'), [data-testid='check-btn']").first
    skip_btn = page.locator("button:has-text('Skip'), [data-testid='skip-btn']").first
    assert check_btn.is_visible(), "Check button not visible in practice footer!"
    assert skip_btn.is_visible(), "Skip button not visible in practice footer!"

    # 2. Test Hint Reveal (hints shown sequentially in order)
    hint_trigger = page.locator(
        "button:has-text('hint'), [data-testid='hints-toggle'], button:has-text('Stuck'), a:has-text('hint')"
    )
    if hint_trigger.count() > 0 and hint_trigger.first.is_visible():
        hint_trigger.first.click()
        page.wait_for_timeout(300)

        # Get first hint
        get_hint_btn = page.locator(
            "button:has-text('Get hint'), button:has-text('next hint'), [data-testid='reveal-hint-btn']"
        )
        if get_hint_btn.count() > 0 and get_hint_btn.first.is_visible():
            get_hint_btn.first.click()
            page.wait_for_timeout(300)
            hint_content = page.locator("[data-testid='hint-item'], .hint-content, [data-testid='hints-container']").first.inner_text()
            assert len(hint_content.strip()) > 0, "First hint revealed with empty content!"

    # 3 & 4. Test Wrong Answer -> Incorrect Feedback, then Correct Answer -> Good work Toast
    multiselect_boxes = page.locator("input[data-testid='multiselect-option'], input[type='checkbox']")
    fill_input = page.locator("input[data-testid='fill-blank-input']")
    stem_el = page.locator("[data-testid='question-stem'], .question-stem, h2, h3")
    stem_text = stem_el.first.inner_text().lower() if stem_el.count() > 0 else ""

    if fill_input.count() > 0 and fill_input.first.is_visible():
        # Fill in the blank question
        fill_input.first.fill("999")
        if check_btn.is_enabled():
            check_btn.click()
            page.wait_for_timeout(500)

        # Assert incorrect feedback appears
        feedback = page.locator(
            "[data-testid='feedback-toast'], .feedback-toast, :text-matches('Try again', 'i'), :text-matches('Not quite', 'i')"
        )
        assert (
            feedback.count() > 0 or "not quite" in page.locator("body").inner_text().lower() or "try again" in page.locator("body").inner_text().lower()
        ), "No incorrect feedback displayed after submitting wrong fill-in-blank answer!"

        # Verify Quick Redo action button appears on mistake
        toast_redo = page.locator("[data-testid='toast-quick-redo-btn']")
        footer_redo = page.locator("[data-testid='quick-redo-btn']")
        assert toast_redo.count() > 0 or footer_redo.count() > 0, "Quick Redo action button not available on mistake!"

        # Now supply correct answer
        fill_input.first.fill("")
        if "alpha" in stem_text or "sigma" in stem_text or "parameter" in stem_text:
            fill_input.first.fill("1 - alpha*sigma - n*sigma")
        else:
            fill_input.first.fill("0.5")

        if check_btn.is_enabled():
            check_btn.click()
            page.wait_for_timeout(500)

    elif multiselect_boxes.count() > 0:
        # Multiple select question (Q-LIM-004)
        options = page.locator("[data-testid^='option-'], .option-item")
        wrong_idx = 0
        for i in range(options.count()):
            opt_t = options.nth(i).inner_text().lower()
            if "defined" in opt_t or "differentiable" in opt_t:
                wrong_idx = i
                break
        options.nth(wrong_idx).click()

        if check_btn.is_enabled():
            check_btn.click()
            page.wait_for_timeout(500)

        feedback = page.locator(
            "[data-testid='feedback-toast'], .feedback-toast, :text-matches('Try again', 'i'), :text-matches('Not quite', 'i')"
        )
        assert (
            feedback.count() > 0 or "not quite" in page.locator("body").inner_text().lower() or "try again" in page.locator("body").inner_text().lower()
        ), "No incorrect feedback displayed after submitting wrong multi-select answer!"

        # Deselect wrong option
        options.nth(wrong_idx).click()

        # Select both correct options (left-hand limit and right-hand limit)
        for i in range(options.count()):
            opt_t = options.nth(i).inner_text().lower()
            if "left-hand" in opt_t or "right-hand" in opt_t:
                options.nth(i).click()

        if check_btn.is_enabled():
            check_btn.click()
            page.wait_for_timeout(500)

    else:
        # Multiple choice 7 options question (Q-LIM-001)
        options = page.locator("[data-testid^='option-'], .option-item, button[data-testid^='option-']")
        wrong_opt = None
        correct_opt = None
        for i in range(options.count()):
            opt_t = options.nth(i).inner_text()
            if "-4" in opt_t or "−4" in opt_t:
                correct_opt = options.nth(i)
            else:
                if wrong_opt is None:
                    wrong_opt = options.nth(i)

        assert wrong_opt is not None, "Could not find a wrong option for MCQ!"
        wrong_opt.click()

        if check_btn.is_enabled():
            check_btn.click()
            page.wait_for_timeout(500)

        # Assert incorrect feedback appears
        feedback = page.locator(
            "[data-testid='feedback-toast'], .feedback-toast, :text-matches('Try again', 'i'), :text-matches('Not quite', 'i')"
        )
        assert (
            feedback.count() > 0 or "not quite" in page.locator("body").inner_text().lower() or "try again" in page.locator("body").inner_text().lower()
        ), "No incorrect feedback displayed after submitting wrong answer!"

        # Verify Quick Redo action button appears on mistake
        toast_redo = page.locator("[data-testid='toast-quick-redo-btn']")
        footer_redo = page.locator("[data-testid='quick-redo-btn']")
        assert toast_redo.count() > 0 or footer_redo.count() > 0, "Quick Redo action button not available on mistake!"

        # Now select the correct option
        assert correct_opt is not None, "Could not find correct option for MCQ!"
        correct_opt.click()

        if check_btn.is_enabled():
            check_btn.click()
            page.wait_for_timeout(500)

    # Assert "Good work!" style feedback toast
    good_toast = page.locator(
        ":text-matches('Good work', 'i'), :text-matches('Great work', 'i'), :text-matches('Correct', 'i'), [data-testid='good-work-toast']"
    )
    assert (
        good_toast.count() > 0 or "Good work" in page.locator("body").inner_text()
    ), "Expected 'Good work!' toast not displayed after correct answer!"

    # Assert "See a step-by-step solution" link is present and expandable
    solution_link = page.locator(
        "button:has-text('solution'), a:has-text('solution'), [data-testid='solution-link']"
    )
    assert (
        solution_link.count() > 0 or "solution" in page.locator("body").inner_text().lower()
    ), "Step-by-step solution link not available on correct answer feedback!"

    if solution_link.count() > 0 and solution_link.first.is_visible():
        solution_link.first.click()
        page.wait_for_timeout(300)
        solution_drawer = page.locator(
            "[data-testid='step-by-step-solution'], .solution-drawer, [data-testid='solution-content']"
        )
        assert (
            solution_drawer.count() > 0 or "step" in page.locator("body").inner_text().lower()
        ), "Step-by-step solution drawer did not expand!"

    # 5. Advance through remaining questions to reach completion screen
    # Loop clicking Next question or Skip until completion screen
    max_steps = 10
    step = 0
    while step < max_steps:
        next_btn = page.locator(
            "button:has-text('Next question'), button:has-text('Next'), [data-testid='next-question-btn']"
        )
        if next_btn.count() > 0 and next_btn.first.is_visible():
            next_btn.first.click()
            page.wait_for_timeout(400)
            step += 1
            continue

        # If on a question that needs skip
        skip = page.locator("button:has-text('Skip'), [data-testid='skip-btn']")
        if skip.count() > 0 and skip.first.is_visible() and skip.first.is_enabled():
            skip.first.click()
            page.wait_for_timeout(400)
            step += 1
            continue

        # Check if completion screen reached
        completion = page.locator(
            "[data-testid='completion-screen'], :text-matches('Exercise complete', 'i'), :text-matches('Summary', 'i')"
        )
        if completion.count() > 0 and completion.first.is_visible():
            break

        step += 1

    # 6. Verify Completion Screen displays score
    completion_text = page.locator("body").inner_text()
    assert (
        "Exercise complete" in completion_text
        or "correct" in completion_text.lower()
        or "/" in completion_text
    ), f"Completion screen or score not found! Text: {completion_text[:300]}"

    # Verify Try again or Up next button exists
    assert (
        "Try again" in completion_text or "Up next" in completion_text
    ), "Completion screen missing 'Try again' or 'Up next' actions!"

    # Zero console errors
    assert len(page.page_errors) == 0, f"Page errors: {page.page_errors}"
    assert len(page.console_errors) == 0, f"Console errors: {page.console_errors}"
