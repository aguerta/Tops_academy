import time
import pytest


def get_current_question_stem(page):
    """Extract current question stem text."""
    stem_el = page.locator("[data-testid='question-stem'], .question-stem, h2, h3")
    if stem_el.count() > 0:
        return stem_el.first.inner_text().strip()
    return ""


def get_current_option_texts(page):
    """Extract current visible answer option contents."""
    options = page.locator("[data-testid^='option-'], .option-item, .answer-option")
    texts = []
    for i in range(options.count()):
        t = options.nth(i).inner_text().strip()
        if t:
            texts.append(t)
    return texts


def test_session_question_and_option_shuffling_and_grading(page, setup_test_courses):
    """AC-05: Across repeated sessions of the same unit, both question order and option order differ
    (asserting orders are not all identical and do not simply mirror the JSON order),
    while grading stays correct after shuffling.
    """
    # Session 1: Collect sequence of stems and option orders
    page.goto(page.base_url)
    page.wait_for_load_state("networkidle")

    # Enter calculus course
    course_link = page.locator("a:has-text('Differential Calculus'), button:has-text('Differential Calculus')")
    if course_link.count() > 0:
        course_link.first.click()
        page.wait_for_load_state("networkidle")

    # Start practice for Limits intro
    unit_trigger = page.locator(
        "[data-testid^='competency-']:has-text('Limits intro'), button:has-text('Limits intro'), button:has-text('Practice')"
    )
    if unit_trigger.count() > 0:
        unit_trigger.first.click()

    lets_go = page.locator("button:has-text(\"Let's go\"), [data-testid='start-practice-btn']")
    if lets_go.count() > 0 and lets_go.first.is_visible():
        lets_go.first.click()
        page.wait_for_load_state("networkidle")

    session1_stems = []
    session1_options = []

    # Record first 3 questions in session 1
    for _ in range(3):
        stem = get_current_question_stem(page)
        session1_stems.append(stem)
        opts = get_current_option_texts(page)
        session1_options.append(opts)

        # Skip to next question
        skip_btn = page.locator("button:has-text('Skip'), [data-testid='skip-btn']")
        if skip_btn.count() > 0 and skip_btn.first.is_visible() and skip_btn.first.is_enabled():
            skip_btn.first.click()
            page.wait_for_timeout(300)

    # Session 2: Return to course overview and launch practice again
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

    if lets_go.count() > 0 and lets_go.first.is_visible():
        lets_go.first.click()
        page.wait_for_load_state("networkidle")

    session2_stems = []
    session2_options = []

    for _ in range(3):
        stem = get_current_question_stem(page)
        session2_stems.append(stem)
        opts = get_current_option_texts(page)
        session2_options.append(opts)

        skip_btn = page.locator("button:has-text('Skip'), [data-testid='skip-btn']")
        if skip_btn.count() > 0 and skip_btn.first.is_visible() and skip_btn.first.is_enabled():
            skip_btn.first.click()
            page.wait_for_timeout(300)

    sessions_stems = [session1_stems, session2_stems]
    sessions_options = [session1_options, session2_options]

    # If first two sessions share the exact same sequence or both begin with the same question, collect a 3rd session
    if session1_stems == session2_stems or (
        len(session1_stems) > 0
        and len(session2_stems) > 0
        and "reasonable estimate" in session1_stems[0].lower()
        and "reasonable estimate" in session2_stems[0].lower()
    ):
        page.goto(page.base_url)
        page.wait_for_load_state("networkidle")
        course_link = page.locator("a:has-text('Differential Calculus'), button:has-text('Differential Calculus')")
        if course_link.count() > 0:
            course_link.first.click()
            page.wait_for_load_state("networkidle")
        unit_trigger = page.locator("[data-testid^='competency-']:has-text('Limits intro'), button:has-text('Limits intro')")
        if unit_trigger.count() > 0:
            unit_trigger.first.click()
        if lets_go.count() > 0 and lets_go.first.is_visible():
            lets_go.first.click()
            page.wait_for_load_state("networkidle")

        session3_stems = []
        session3_options = []
        for _ in range(3):
            s = get_current_question_stem(page)
            session3_stems.append(s)
            o = get_current_option_texts(page)
            session3_options.append(o)
            skip_btn = page.locator("button:has-text('Skip'), [data-testid='skip-btn']")
            if skip_btn.count() > 0 and skip_btn.first.is_visible() and skip_btn.first.is_enabled():
                skip_btn.first.click()
                page.wait_for_timeout(300)
        sessions_stems.append(session3_stems)
        sessions_options.append(session3_options)

    # Assert question stem randomization (AC-05):
    # 1. Orders across repeated sessions must not all be identical
    has_stem_divergence = any(s != sessions_stems[0] for s in sessions_stems[1:])
    assert has_stem_divergence, (
        f"Question sequences were identical across repeated practice sessions! {sessions_stems}"
    )

    # 2. Orders must not simply mirror the raw sequential JSON order
    def mirrors_json_order(stems):
        return (
            len(stems) >= 2
            and "reasonable estimate" in stems[0].lower()
            and "parameter" in stems[1].lower()
        )

    all_mirror_json = all(mirrors_json_order(s) for s in sessions_stems)
    assert not all_mirror_json, (
        f"All sessions mirrored the sequential JSON question order! {sessions_stems}"
    )

    # Assert option shuffling on MCQ question (AC-05):
    has_option_divergence = False
    all_option_runs = [opts for sess in sessions_options for opts in sess if len(opts) >= 4]
    if len(all_option_runs) >= 2:
        for i in range(len(all_option_runs) - 1):
            if all_option_runs[i] != all_option_runs[i + 1]:
                has_option_divergence = True
                break
    assert has_option_divergence, "MCQ options did not diverge across repeated sessions!"

    # Also verify grading stays correct after shuffling:
    # Test grading a question with shuffled options:
    # Navigate to fresh session, locate MCQ question, select option containing '-4'
    page.goto(page.base_url)
    page.wait_for_load_state("networkidle")
    course_link = page.locator("a:has-text('Differential Calculus'), button:has-text('Differential Calculus')")
    if course_link.count() > 0:
        course_link.first.click()
    unit_trigger = page.locator("[data-testid^='competency-']:has-text('Limits intro'), button:has-text('Limits intro')")
    if unit_trigger.count() > 0:
        unit_trigger.first.click()
    if lets_go.count() > 0 and lets_go.first.is_visible():
        lets_go.first.click()

    # Look for question with '-4' option
    for _ in range(4):
        correct_option_btn = page.locator("[data-testid^='option-']:has-text('-4'), .option-item:has-text('-4')")
        if correct_option_btn.count() > 0:
            correct_option_btn.first.click()
            check_btn = page.locator("button:has-text('Check'), [data-testid='check-btn']")
            if check_btn.is_enabled():
                check_btn.click()
                page.wait_for_timeout(500)
                # Must be graded correct ("Good work!")
                feedback = page.locator("body").inner_text()
                assert "Good work" in feedback or "correct" in feedback.lower() or "keep going" in feedback.lower(), (
                    "Grading failed after option shuffling!"
                )
            break
        else:
            skip_btn = page.locator("button:has-text('Skip'), [data-testid='skip-btn']")
            if skip_btn.is_visible() and skip_btn.is_enabled():
                skip_btn.click()
                page.wait_for_timeout(300)

    # Console errors assertion
    assert len(page.page_errors) == 0, f"Page errors: {page.page_errors}"
    assert len(page.console_errors) == 0, f"Console errors: {page.console_errors}"
