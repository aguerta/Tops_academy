"""Empirical Verification Runner for M2 Platform State, Shuffling, Mastery & Error Isolation.

Run directly via: python tests/e2e/empirical_verify_runner.py
"""
import json
import os
import shutil
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
COURSES_DIR = ROOT_DIR / "courses"
FIXTURES_DIR = COURSES_DIR / "test_fixtures"
BASE_URL = "http://localhost:5173"


def ensure_test_courses():
    calculus_src = FIXTURES_DIR / "valid_course_calculus.json"
    calculus_dst = COURSES_DIR / "test_differential_calculus.json"
    if calculus_src.exists() and not calculus_dst.exists():
        shutil.copy2(calculus_src, calculus_dst)

    challenge_src = FIXTURES_DIR / "valid_course_challenge.json"
    challenge_dst = COURSES_DIR / "test_course_challenge.json"
    if challenge_src.exists() and not challenge_dst.exists():
        shutil.copy2(challenge_src, challenge_dst)


def cleanup_test_courses():
    for f in [COURSES_DIR / "test_differential_calculus.json", COURSES_DIR / "test_course_challenge.json"]:
        if f.exists():
            try:
                f.unlink()
            except Exception:
                pass


def run_shuffling_investigation():
    print("\n=======================================================")
    print("PILLAR 1: EMPIRICAL SHUFFLING INVESTIGATION")
    print("=======================================================")
    ensure_test_courses()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Part A: Practice Session Question Shuffling
        print("\n--- Part A: Practice Session Question Shuffling ---")
        practice_sequences = []

        for i in range(4):
            page.goto(BASE_URL)
            page.wait_for_load_state("networkidle")

            # Click Calculus course
            page.locator("[data-testid='course-card']").first.click()
            page.wait_for_load_state("networkidle")

            # Click Practice on Limits intro
            page.locator("button:has-text('Practice')").first.click()
            page.wait_for_timeout(300)

            # Pre-exercise modal -> Let's go
            page.locator("button:has-text(\"Let's go\")").first.click()
            page.wait_for_load_state("networkidle")

            # Record question stems
            stems = []
            for q in range(4):
                stem_el = page.locator("h2").first
                stems.append(stem_el.inner_text().strip())

                skip_btn = page.locator("button:has-text('Skip')").first
                if skip_btn.is_visible() and skip_btn.is_enabled():
                    skip_btn.click()
                    page.wait_for_timeout(200)

            practice_sequences.append(stems)
            print(f"  Practice Launch {i+1} stems:")
            for idx, s in enumerate(stems):
                safe_s = s.encode("ascii", "replace").decode("ascii")
                print(f"    Q{idx+1}: {safe_s[:60]}...")

        # Part B: Quiz Session Question Shuffling
        print("\n--- Part B: Quiz Session Question Shuffling ---")
        quiz_sequences = []

        for i in range(4):
            page.goto(BASE_URL)
            page.wait_for_load_state("networkidle")
            page.locator("[data-testid='course-card']").first.click()
            page.wait_for_load_state("networkidle")

            # Click Quiz on Limits intro
            page.locator("button:has-text('Quiz')").first.click()
            page.wait_for_load_state("networkidle")

            # Record stems in quiz
            stems = []
            for q in range(4):
                stem_el = page.locator("h2").first
                stems.append(stem_el.inner_text().strip())

                skip_btn = page.locator("button:has-text('Skip')").first
                if skip_btn.is_visible() and skip_btn.is_enabled():
                    skip_btn.click()
                    page.wait_for_timeout(200)

            quiz_sequences.append(stems)
            print(f"  Quiz Launch {i+1} stems:")
            for idx, s in enumerate(stems):
                safe_s = s.encode("ascii", "replace").decode("ascii")
                print(f"    Q{idx+1}: {safe_s[:60]}...")

        # Part C: Option Shuffling & Grading Integrity
        print("\n--- Part C: Option Shuffling & Grading Integrity ---")
        option_orders = []

        for i in range(4):
            page.goto(BASE_URL)
            page.wait_for_load_state("networkidle")
            page.locator("[data-testid='course-card']:has-text('Differential Calculus')").first.click()
            page.wait_for_load_state("networkidle")
            page.locator("button:has-text('Practice')").first.click()
            page.wait_for_timeout(200)
            page.locator("button:has-text(\"Let's go\")").first.click()
            page.wait_for_timeout(300)

            opts = []
            opt_loc = page.locator("[data-testid^='option-']")
            for o in range(opt_loc.count()):
                opts.append(opt_loc.nth(o).inner_text().strip())
            option_orders.append(opts)

            # In run 4, find MCQ question with '-4', click correct answer and assert grading
            if i == 3:
                for _ in range(4):
                    correct_opt = page.locator("[data-testid^='option-']:has-text('-4'), [data-testid^='option-']:has-text('−4')")
                    if correct_opt.count() > 0 and correct_opt.first.is_visible():
                        correct_opt.first.click()
                        page.locator("button:has-text('Check')").first.click()
                        page.wait_for_timeout(300)
                        feedback = page.locator("body").inner_text()
                        graded_correct = "Good work" in feedback or "correct" in feedback.lower()
                        print(f"  Grading after option shuffling: {'PASS (Correctly graded)' if graded_correct else 'FAIL'}")
                        break
                    else:
                        skip_btn = page.locator("button:has-text('Skip'), [data-testid='skip-btn']")
                        if skip_btn.count() > 0 and skip_btn.first.is_visible() and skip_btn.first.is_enabled():
                            skip_btn.first.click()
                            page.wait_for_timeout(300)

        print("  Option orders across 4 runs:")
        for idx, opts in enumerate(option_orders):
            safe_opts = [o.encode("ascii", "replace").decode("ascii")[:15] for o in opts[:4]]
            print(f"    Run {idx+1}: {safe_opts}...")

        browser.close()

    # Empirical analysis
    practice_all_identical = all(s == practice_sequences[0] for s in practice_sequences)
    quiz_has_variation = any(s != quiz_sequences[0] for s in quiz_sequences[1:])
    options_have_variation = any(o != option_orders[0] for o in option_orders[1:])

    print(f"\n[SUMMARY PILLAR 1]:")
    print(f"  Practice Question Shuffling: Identical across all runs = {practice_all_identical}")
    print(f"  Quiz Question Shuffling: Variation present = {quiz_has_variation}")
    print(f"  Option Shuffling: Variation present = {options_have_variation}")

    return {
        "practice_all_identical": practice_all_identical,
        "quiz_has_variation": quiz_has_variation,
        "options_have_variation": options_have_variation
    }


def run_mastery_persistence_investigation():
    print("\n=======================================================")
    print("PILLAR 2: EMPIRICAL LOCALSTORAGE MASTERY PERSISTENCE")
    print("=======================================================")
    ensure_test_courses()

    results = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Step 1: Baseline check
        page.goto(BASE_URL)
        page.wait_for_load_state("networkidle")
        page.evaluate("() => localStorage.clear()")
        page.reload()
        page.wait_for_load_state("networkidle")

        page.locator("[data-testid='course-card']:has-text('Differential Calculus')").first.click()
        page.wait_for_load_state("networkidle")
        baseline_text = page.locator("body").inner_text()
        has_baseline_zero = "Course mastery: 0%" in baseline_text
        print(f"  Baseline 0% Mastery: {has_baseline_zero}")
        results["baseline_zero"] = has_baseline_zero

        # Step 2: Practice session completion with 100%
        page.locator("button:has-text('Practice')").first.click()
        page.wait_for_timeout(200)
        page.locator("button:has-text(\"Let's go\")").first.click()
        page.wait_for_load_state("networkidle")

        # Answer 4 questions correctly:
        # Q1: MCQ -> '-4'
        opt_b = page.locator("[data-testid^='option-']:has-text('-4')").first
        if opt_b.is_visible():
            opt_b.click()
            page.locator("button:has-text('Check')").first.click()
            page.wait_for_timeout(200)
            page.locator("button:has-text('Next')").first.click()
            page.wait_for_timeout(200)

        # Q2: Fill in blank -> 1-(alpha+n)*sigma
        fib_input = page.locator("input[type='text']").first
        if fib_input.is_visible():
            fib_input.fill("1-(alpha+n)*sigma")
            page.locator("button:has-text('Check')").first.click()
            page.wait_for_timeout(200)
            page.locator("button:has-text('Next')").first.click()
            page.wait_for_timeout(200)

        # Q3: Fill in blank -> 0.5
        fib_input = page.locator("input[type='text']").first
        if fib_input.is_visible():
            fib_input.fill("0.5")
            page.locator("button:has-text('Check')").first.click()
            page.wait_for_timeout(200)
            page.locator("button:has-text('Next')").first.click()
            page.wait_for_timeout(200)

        # Q4: Multiple select -> opt_a, opt_c
        opt_a = page.locator("[data-testid='option-opt_a']").first
        opt_c = page.locator("[data-testid='option-opt_c']").first
        if opt_a.is_visible() and opt_c.is_visible():
            opt_a.click()
            opt_c.click()
            page.locator("button:has-text('Check')").first.click()
            page.wait_for_timeout(200)
            page.locator("button:has-text('Next')").first.click()
            page.wait_for_timeout(300)

        # We should now be on completion screen
        completion_visible = page.locator(":text-matches('complete', 'i')").count() > 0
        print(f"  Practice session reached completion: {completion_visible}")

        # Check localStorage immediately
        storage_raw = page.evaluate("() => localStorage.getItem('khan_academic_progress_v1')")
        storage_data = json.loads(storage_raw) if storage_raw else {}
        course_rec = storage_data.get("test-differential-calculus", {})
        comp_rec = course_rec.get("competencies", {}).get("COMP-LIM-01", {})
        status_after_practice = comp_rec.get("status")
        points_after_practice = comp_rec.get("points")
        print(f"  After 100% Practice -> Status: {status_after_practice}, Points: {points_after_practice}, Course Mastery: {course_rec.get('mastery_points')}%")
        results["practice_tier"] = status_after_practice
        results["practice_points"] = points_after_practice

        # Step 3: Reload page and re-enter course -> verify persistence
        page.goto(BASE_URL)
        page.reload()
        page.wait_for_load_state("networkidle")
        page.locator("[data-testid='course-card']:has-text('Differential Calculus')").first.click()
        page.wait_for_load_state("networkidle")

        reloaded_body = page.locator("body").inner_text()
        persisted_in_ui = f"Course mastery: {course_rec.get('mastery_points')}%" in reloaded_body
        print(f"  Reloaded UI reflects persisted course mastery: {persisted_in_ui}")
        results["persisted_in_ui"] = persisted_in_ui

        # Step 4: Unit Test to reach Mastered (100 pts)
        page.locator("button:has-text('Unit test')").first.click()
        page.wait_for_load_state("networkidle")

        # Answer all 4 questions correctly in Unit Test (dynamically handling shuffled question order)
        for q_idx in range(4):
            if page.locator("[data-testid='completion-screen']").count() > 0:
                break

            # Handle MCQ, FIB, or MS
            if page.locator("[data-testid^='option-']:has-text('-4')").count() > 0:
                page.locator("[data-testid^='option-']:has-text('-4')").first.click()
            elif page.locator("[data-testid='option-opt_a']").count() > 0 and page.locator("[data-testid='option-opt_c']").count() > 0:
                page.locator("[data-testid='option-opt_a']").first.click()
                page.locator("[data-testid='option-opt_c']").first.click()
            elif page.locator("input[type='text']").count() > 0:
                stem = page.locator("h2").first.inner_text()
                if "alpha" in stem or "sigma" in stem:
                    page.locator("input[type='text']").first.fill("1-(alpha+n)*sigma")
                else:
                    page.locator("input[type='text']").first.fill("0.5")
            elif page.locator("[data-testid^='option-']").count() > 0:
                page.locator("[data-testid^='option-']").first.click()

            check_btn = page.locator("button:has-text('Check')").first
            if check_btn.is_visible() and check_btn.is_enabled():
                check_btn.click()
                page.wait_for_timeout(300)

            next_btn = page.locator("button:has-text('Next')").first
            if next_btn.is_visible():
                next_btn.click()
                page.wait_for_timeout(300)

        storage_raw2 = page.evaluate("() => localStorage.getItem('khan_academic_progress_v1')")
        storage_data2 = json.loads(storage_raw2) if storage_raw2 else {}
        course_rec2 = storage_data2.get("test-differential-calculus", {})
        comp_rec2 = course_rec2.get("competencies", {}).get("COMP-LIM-01", {})
        print(f"  After 100% Unit Test -> Status: {comp_rec2.get('status')}, Points: {comp_rec2.get('points')}, Course Mastery: {course_rec2.get('mastery_points')}%")
        results["unit_test_tier"] = comp_rec2.get("status")
        results["unit_test_points"] = comp_rec2.get("points")

        # Step 5: Test corrupt LocalStorage resilience
        page.goto(BASE_URL)
        page.evaluate("() => localStorage.setItem('khan_academic_progress_v1', 'CORRUPT_JSON_SYNTAX{{{')")
        page.reload()
        page.wait_for_load_state("networkidle")
        page.locator("[data-testid='course-card']:has-text('Differential Calculus')").first.click()
        page.wait_for_load_state("networkidle")
        corrupt_recovered = "Course mastery: 0%" in page.locator("body").inner_text()
        print(f"  Corrupt LocalStorage fallback to fresh 0%: {corrupt_recovered}")
        results["corrupt_recovered"] = corrupt_recovered

        browser.close()

    print(f"\n[SUMMARY PILLAR 2]: {results}")
    return results


def run_error_isolation_investigation():
    print("\n=======================================================")
    print("PILLAR 3: EMPIRICAL ERROR ISOLATION & DYNAMIC LOADING")
    print("=======================================================")
    ensure_test_courses()

    fixtures = [
        ("syntax_malformed", "{\n  \"course_id\": \"syntax-err\",\n  \"title\": \"Syntax Error\",\n  unterminated"),
        ("missing_competencies", "{\n  \"course_id\": \"no-comp\",\n  \"title\": \"Missing Competencies\",\n  \"questions\": [{\"id\":\"q1\",\"type\":\"multiple_choice_7_options\"}]\n}"),
        ("empty_questions", "{\n  \"course_id\": \"empty-q\",\n  \"title\": \"Empty Questions\",\n  \"competencies\": [{\"id\":\"c1\",\"code\":\"HAB-01\",\"name\":\"n\",\"category\":\"Skill\",\"description\":\"d\",\"mastery_target\":100}],\n  \"questions\": []\n}"),
        ("invalid_question_type", "{\n  \"course_id\": \"bad-type\",\n  \"title\": \"Invalid Q Type\",\n  \"competencies\": [{\"id\":\"c1\",\"code\":\"HAB-01\",\"name\":\"n\",\"category\":\"Skill\",\"description\":\"d\",\"mastery_target\":100}],\n  \"questions\": [{\"id\":\"q1\",\"competency_id\":\"c1\",\"type\":\"unsupported_essay\",\"stem\":\"stem\"}]\n}"),
        ("control_character_latex", "{\n  \"course_id\": \"ctrl-char\",\n  \"title\": \"Corrupted LaTeX\",\n  \"competencies\": [{\"id\":\"c1\",\"code\":\"HAB-01\",\"name\":\"n\",\"category\":\"Skill\",\"description\":\"d\",\"mastery_target\":100}],\n  \"questions\": [{\"id\":\"q1\",\"competency_id\":\"c1\",\"type\":\"multiple_choice_7_options\",\"stem\":\"Raw \x08 char\"}]\n}"),
    ]

    isolation_results = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for name, content in fixtures:
            bad_file = COURSES_DIR / f"test_adversarial_{name}.json"
            try:
                bad_file.write_text(content, encoding="utf-8")

                page.goto(BASE_URL)
                page.wait_for_load_state("networkidle")

                # 1. Valid course is visible
                valid_visible = page.locator("[data-testid='course-card']:has-text('Differential Calculus')").count() > 0

                # 2. Error card is visible
                error_card = page.locator("[data-testid='course-error-card']")
                error_visible = error_card.count() > 0

                # 3. Read error diagnostic
                diag_msg = error_card.first.inner_text().strip().replace("\n", " ") if error_visible else "NONE"

                # 4. Valid course can be opened and played
                can_play = False
                if valid_visible:
                    page.locator("[data-testid='course-card']:has-text('Differential Calculus')").first.click()
                    page.wait_for_load_state("networkidle")
                    can_play = "Limits" in page.locator("body").inner_text()

                print(f"  Fixture: {name}")
                print(f"    Error Card Displayed: {error_visible} ({diag_msg[:80]}...)")
                print(f"    Valid Course Functional: {valid_visible and can_play}")

                isolation_results[name] = {
                    "error_visible": error_visible,
                    "valid_functional": valid_visible and can_play,
                    "diagnostic": diag_msg[:100]
                }
            finally:
                if bad_file.exists():
                    bad_file.unlink()

        browser.close()

    print(f"\n[SUMMARY PILLAR 3]: {isolation_results}")
    return isolation_results


if __name__ == "__main__":
    try:
        shuffling = run_shuffling_investigation()
        mastery = run_mastery_persistence_investigation()
        isolation = run_error_isolation_investigation()

        print("\n=======================================================")
        print("EMPIRICAL TEST SUITE EXECUTION COMPLETE")
        print("=======================================================")
    finally:
        cleanup_test_courses()
