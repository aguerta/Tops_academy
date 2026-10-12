## 2026-10-11T02:08:02Z
You are the Milestone 2 Worker for the "Top's Academy" project.
Your working directory is: g:\Mi unidad\Competence_analyser\.agents\teamwork\worker_m2_platform
Read g:\Mi unidad\Competence_analyser\.agents\teamwork\ORIGINAL_REQUEST.md immediately.
Read g:\Mi unidad\Competence_analyser\PROJECT.md.
Read g:\Mi unidad\Competence_analyser\.agents\teamwork\explorer_ui_survey\ui_spec.md.
Read g:\Mi unidad\Competence_analyser\TEST_READY.md and g:\Mi unidad\Competence_analyser\TEST_INFRA.md.

Write ownership: You exclusively own `platform/` and `run_platform.py`.

Environment note: On Windows, PowerShell execution policy blocks `npm.ps1`. Always use `npm.cmd` or `npx.cmd` in commands!

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Your task:
1. Build the complete, local, single-user Top's Academy Practice Platform web app under `platform/`:
   - Frontend stack: React, Vite, TypeScript, Tailwind CSS, KaTeX (`katex`), `mathjs`, `canvas-confetti`.
   - Backend course discovery: A lightweight server (Node in `platform/server/courseServer.cjs` or embedded in Vite plugin / Python in `run_platform.py`) that discovers all `.json` files in `courses/` directory.
     * Dynamic reload: copying a new valid course JSON into `courses/` makes it appear immediately after reload without code changes.
     * Fault-tolerant isolation: an invalid course JSON file displays a clear error badge/message for that course while all valid courses continue to work.
   - Root launcher `run_platform.py`: single documented command (`python run_platform.py`) that starts the application on port 5173 (or 3000) and serves both the API and frontend.
   - Recreate the Top's Academy look & feel across all 6 reference screens:
     * Screen 1: Course Overview (`Courser_overview.png`): left sidebar with course and unit navigation; course mastery %; unit cards with mastery grid; mastery legend (Mastered `#583b8b`, Proficient `#8377b2`, Familiar `#e07a21`, Attempted `#f3801e`, Not started `#88939e`, Quiz `⚡`, Unit test `★`); Course Challenge summary card.
     * Screen 2: "Ready to practice?" modal (`pre_exercise.png`): blue hero panel (`#1865f2`), question count badge, smiling polygon character mascots, and "Let's go" button.
     * Screen 3: Question presentation (`multiple_answer_question.png`): stem with KaTeX LaTeX math ($...$ and $$...$$); native SVG vector `<CoordinatePlane />` component rendering Cartesian axes ($[-7, 7] \times [-7, 7]$), grid, curves, labels, and open/closed points; 3 interaction types:
       - `multiple_choice_7_options`: 7 options with circular letter badges A–G.
       - `multiple_select`: 4–6 options with checkboxes, all-or-nothing grading.
       - `fill_in_the_blank`: text/math input graded by mathematical equivalence (using `mathjs` AST simplification + Monte Carlo numerical sampling: accepting `1-(alpha+n)*sigma` for `1 - \alpha\sigma - n\sigma`, and `0.5` for `1/2`).
       - Bottom footer: progress indicator dots (`○ ○ ○ ○`), Skip and Check buttons.
     * Screen 4: Correct answer state (`good_answer.png`): 2px green border (`#14a34b`), green check badge, bottom bar with check marks and "Next question" button, downward speech-bubble popover toast ("Good work!", "Keep going.", and blue link "See a step-by-step solution" that expands the solution steps).
     * Screen 5: "Exercise complete!" screen (`exercise_completed.png`): blue hero panel, `canvas-confetti` animation, thumbs-up line art, score fraction, mastery level-up summary card, "Try again" link, and "Up next" button.
     * Screen 6: Course Challenge start screen (`course_challenge.png`): ~30 questions drawn across all course units, 30–45 minutes estimate, start button.
   - Shuffling & Randomization: By default, every session (practice, quiz, unit test, challenge) presents questions in random order and shuffles options independently of JSON order (verifiable by asserting repeated sessions do not mirror JSON order while grading remains accurate).
   - Mastery Persistence: LocalStorage persistence of competency mastery levels across browser reloads.
2. Run and verify the automated E2E test suite:
   - `python -m pytest tests/e2e -v` (must pass all 14 headless browser tests with 0 failures and 0 console errors).
   - `python -m pytest tests/e2e/test_visual_fidelity_capture.py -v` (captures all 6 platform screenshots into `tests/e2e/screenshots/` for reviewer comparison).
3. Document all implementation details, test outputs, and commands in `g:\Mi unidad\Competence_analyser\.agents\teamwork\worker_m2_platform\handoff.md`.
4. Send a message to parent when complete.
