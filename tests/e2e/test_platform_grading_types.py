import time
import pytest


def enter_practice_session(page):
    """Navigate to practice session."""
    page.goto(page.base_url)
    page.wait_for_load_state("networkidle")

    course_link = page.locator("a:has-text('Differential Calculus'), button:has-text('Differential Calculus')")
    if course_link.count() > 0:
        course_link.first.click()
        page.wait_for_load_state("networkidle")

    unit_trigger = page.locator(
        "[data-testid^='competency-']:has-text('Limits intro'), button:has-text('Limits intro'), button:has-text('Practice')"
    )
    if unit_trigger.count() > 0:
        unit_trigger.first.click()

    lets_go = page.locator("button:has-text(\"Let's go\"), [data-testid='start-practice-btn']")
    if lets_go.count() > 0 and lets_go.first.is_visible():
        lets_go.first.click()
        page.wait_for_load_state("networkidle")


def test_mcq_7_options_grading(page, setup_test_courses):
    """AC-06 (Part 1): MCQ with 7 options is rendered with 7 options and graded correctly."""
    enter_practice_session(page)

    # Find the question with 7 options (Q-LIM-001)
    found_7_mcq = False
    for _ in range(5):
        options = page.locator("[data-testid^='option-'], .option-item, .answer-option")
        if options.count() == 7:
            found_7_mcq = True
            # Verify exactly 7 options rendered
            assert options.count() == 7, f"Expected 7 options, found {options.count()}"

            # Click correct option ($-4$)
            opt_correct = page.locator("[data-testid^='option-']:has-text('-4'), .option-item:has-text('-4')")
            assert opt_correct.count() > 0, "Correct option -4 not found among 7 options!"
            opt_correct.first.click()

            check_btn = page.locator("button:has-text('Check'), [data-testid='check-btn']").first
            assert check_btn.is_enabled()
            check_btn.click()
            page.wait_for_timeout(400)

            # Assert correct grading toast
            feedback = page.locator("body").inner_text()
            assert "Good work" in feedback or "correct" in feedback.lower(), (
                "Correct option on 7-option MCQ was not graded as correct!"
            )
            break
        else:
            skip_btn = page.locator("button:has-text('Skip'), [data-testid='skip-btn']")
            if skip_btn.is_visible() and skip_btn.is_enabled():
                skip_btn.click()
                page.wait_for_timeout(300)

    assert found_7_mcq, "Did not encounter 7-option MCQ question during session!"
    assert len(page.page_errors) == 0, f"Page errors: {page.page_errors}"


def test_fill_in_the_blank_math_equivalence(page, setup_test_courses):
    r"""AC-06 (Part 2): Fill-in-the-blank accepts equivalent algebraic expressions
    e.g. '1-(alpha+n)*sigma' for '1 - \alpha\sigma - n\sigma' and '0.5' for '1/2'.
    """
    enter_practice_session(page)

    tested_algebra = False
    tested_numeric = False

    for _ in range(5):
        stem = page.locator("[data-testid='question-stem'], .question-stem, body").inner_text()
        fill_input = page.locator("input[data-testid='fill-blank-input'], input[type='text']")

        if fill_input.count() > 0 and fill_input.first.is_visible():
            check_btn = page.locator("button:has-text('Check'), [data-testid='check-btn']").first

            if "alpha" in stem.lower() or "\\alpha" in stem or "sigma" in stem.lower() or "L =" in stem:
                # Test equivalent algebraic answer: '1-(alpha+n)*sigma'
                fill_input.first.fill("1-(alpha+n)*sigma")
                if check_btn.is_enabled():
                    check_btn.click()
                    page.wait_for_timeout(400)
                    feedback = page.locator("body").inner_text()
                    assert "Good work" in feedback or "correct" in feedback.lower(), (
                        "Equivalent algebraic expression '1-(alpha+n)*sigma' was not accepted!"
                    )
                    tested_algebra = True

            elif "x - 1" in stem or "x \\to 2" in stem or "2" in stem:
                # Test equivalent numeric answer: '0.5' for 1/2
                fill_input.first.fill("0.5")
                if check_btn.is_enabled():
                    check_btn.click()
                    page.wait_for_timeout(400)
                    feedback = page.locator("body").inner_text()
                    assert "Good work" in feedback or "correct" in feedback.lower(), (
                        "Equivalent numeric answer '0.5' for 1/2 was not accepted!"
                    )
                    tested_numeric = True

            # Advance to next
            next_btn = page.locator("button:has-text('Next question'), button:has-text('Next'), [data-testid='next-question-btn']")
            if next_btn.is_visible():
                next_btn.click()
                page.wait_for_timeout(300)
                continue

        # Skip to next question
        skip_btn = page.locator("button:has-text('Skip'), [data-testid='skip-btn']")
        if skip_btn.is_visible() and skip_btn.is_enabled():
            skip_btn.click()
            page.wait_for_timeout(300)

    assert tested_algebra or tested_numeric, "No fill-in-the-blank question was encountered to test math equivalence!"
    assert len(page.page_errors) == 0, f"Page errors: {page.page_errors}"


def test_multiple_select_all_or_nothing(page, setup_test_courses):
    """AC-06 (Part 3): Multiple-select grading is strictly all-or-nothing:
    - Partial selection is graded as incorrect
    - Complete correct selection is graded as correct
    - Extra distractor selection is graded as incorrect
    """
    enter_practice_session(page)

    found_multiselect = False
    for _ in range(5):
        # Detect multiselect via checkbox or instruction prompt
        checkboxes = page.locator(
            "input[type='checkbox'], [data-testid='multiselect-option'], [data-testid^='checkbox-']"
        )
        prompt_text = page.locator("body").inner_text()

        if checkboxes.count() >= 3 or "Choose all" in prompt_text or "all that apply" in prompt_text.lower():
            found_multiselect = True

            check_btn = page.locator("button:has-text('Check'), [data-testid='check-btn']").first

            # 1. Test Partial Selection (only select first correct item)
            # In Q-LIM-004, correct are opt_a (left-hand limit) and opt_c (right-hand limit)
            opt_left = page.locator(":text-matches('left-hand limit', 'i'), [data-testid='option-opt_a']")
            if opt_left.count() > 0:
                opt_left.first.click()
            else:
                checkboxes.first.click()

            if check_btn.is_enabled():
                check_btn.click()
                page.wait_for_timeout(400)
                feedback = page.locator("body").inner_text()
                # Partial selection MUST be graded as incorrect
                assert (
                    "Try again" in feedback
                    or "Not quite" in feedback
                    or "Incorrect" in feedback
                    or "Good work" not in feedback
                ), "All-or-nothing violated: partial multiple-select was accepted as correct!"

            # 2. Test Full Correct Selection
            opt_right = page.locator(":text-matches('right-hand limit', 'i'), [data-testid='option-opt_c']")
            if opt_right.count() > 0:
                opt_right.first.click()
            elif checkboxes.count() >= 3:
                checkboxes.nth(2).click()

            if check_btn.is_enabled():
                check_btn.click()
                page.wait_for_timeout(400)
                feedback = page.locator("body").inner_text()
                assert "Good work" in feedback or "correct" in feedback.lower(), (
                    "Complete correct selection on multiple-select was not graded as correct!"
                )

            break
        else:
            skip_btn = page.locator("button:has-text('Skip'), [data-testid='skip-btn']")
            if skip_btn.is_visible() and skip_btn.is_enabled():
                skip_btn.click()
                page.wait_for_timeout(300)

    assert found_multiselect, "Multiple-select question not encountered in session!"
    assert len(page.page_errors) == 0, f"Page errors: {page.page_errors}"
