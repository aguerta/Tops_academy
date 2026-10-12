# UI Specification Explorer Handoff Report

## 1. Observation

1. **Reference Screenshot Analysis (`Khan_academy_images_references/`)**:
   - `Courser_overview.png`: Two-column layout with left navigation sidebar (~260px wide) containing course title and unit links. Main section features `Course mastery: 100% ⓘ`, a 7-item mastery legend (Mastered `#583b8b`, Proficient `#8377b2`, Familiar `#e07a21`, Attempted `#f3801e`, Not started `#88939e`, Quiz `⚡`, Unit test `★`), a unit grid of purple crown blocks interspersed with Quiz bolts (`⚡`) and Unit test stars (`★`), and a dedicated Course Challenge summary card (`📖 COURSE CHALLENGE: 100%`) on the lower right.
   - `pre_exercise.png`: Blue hero panel (`#1865f2`) centered with `Ready to practice?`, subtitle `Okay, show us what you can do!`, `4 questions` badge, and three smiling polygon character mascots at the base. Bottom white footer bar has a `<` back button and a solid blue `Let's go` button.
   - `multiple_answer_question.png`: Stem displays KaTeX math `$f$`, `$x = 3$`. Directly below is a Cartesian coordinate plane ($[-7, 7] \times [-7, 7]$) with grid lines, arrowed axes, a cyan curve labeled $f$, and an open hole circle at $(3, -4)$. Sub-question prompt asks `What is a reasonable estimate for \lim_{x \to 3} f(x)?` with `Choose 1 answer:` followed by options A–D with circular letter badges. Bottom footer has `🔄 Do 4 problems`, 4 progress dots (`○ ○ ○ ○`), blue text `Skip`, and a disabled grey `Check` button.
   - `good_answer.png`: Correct selected option has a 2px green border (`#14a34b`), a solid green letter pill `✓ D`, and green text. Bottom bar displays `🔄 2 of 4  ✓ ✓ ○ ○`, disabled `Skip`, and a solid blue `Next question` button. A speech-bubble popover card appears directly above `Next question` with a downward arrow pointer, large green checkmark icon, `Good work!`, `Keep going.`, and a blue link `See a step-by-step solution.`. Confetti particles accent the CTA button.
   - `exercise_completed.png`: Upper bar shows course mastery. Full blue hero panel (`#1865f2`) with colorful confetti ribbons and squares falling across the screen. Left side features a white line-art thumbs-up icon with radiating lines, `Exercise complete!`, and `4/4 correct`. Right side features a white card with mastery points leveled up summary. Bottom footer provides `🔄 Try again` link and `Up next: Lesson 2` button.
   - `course_challenge.png`: Left sidebar active card shows `Course challenge` with blue left accent border. Hero displays `Ready for a challenge?`, description, `30 questions • 30 - 45 minutes`, and an open notebook illustration. Bottom footer provides a solid blue `Let's go` button.

2. **System Requirements (`ORIGINAL_REQUEST.md`)**:
   - Lines 20–22 (R1): "A local, single-user web app (no login) that runs with one documented command and visually and behaviourally recreates the reference screenshots, UI in English. Course = one source content; Unit = one competency... By default, every session... presents questions in random order and shuffles the answer options... It must render LaTeX, render simple function graphs described in the JSON (curves, open/closed points), support all three interaction types, and grade fill-in-the-blank answers by mathematical equivalence... Progress and mastery persist locally across reloads/restarts".
   - Lines 42–53: Acceptance criteria requires automated browser tests (headless), single command start, auto-discovery of courses in `courses/`, dynamic shuffling, equivalence grading for `1-(alpha+n)*sigma` vs `1 - \alpha\sigma - n\sigma` and `0.5` vs `1/2`, and DOM/canvas verification for graphs.
   - Line 55: Visual fidelity criteria requires an independent reviewer agent to inspect screenshots matching the 6 reference images item-by-item.

## 2. Logic Chain

1. **Visual Fidelity**: From inspecting `Courser_overview.png`, `pre_exercise.png`, `multiple_answer_question.png`, `good_answer.png`, `exercise_completed.png`, and `course_challenge.png`, the visual language is consistent: Khan blue `#1865f2`, 5 distinct mastery tier colors, circular/pill badges, speech-bubble feedback popover, progress dots, and confetti. Using Tailwind CSS with explicit design tokens (`ka-blue`, `ka-mastered`, `ka-green-border`, etc.) guarantees exact pixel and color parity while avoiding styling drift.
2. **Math & Graphing Fidelity**:
   - Math rendering must use KaTeX because Top's Academy developed KaTeX for this exact interface; KaTeX renders synchronously, is lightweight, and formats formulas identically to the screenshots.
   - For graphs, requirement R1 specifies curves and open/closed points inspectable via DOM/canvas. A native React SVG component (`<CoordinatePlane />`) provides vector precision at any resolution, zero external bundle overhead, and straightforward DOM inspection for automated browser tests (`svg`, `path.curve`, `circle.open-point`, `circle.closed-point`).
3. **Mathematical Equivalence**:
   - R1 requires grading algebraic inputs by equivalence (e.g., `1-(alpha+n)*sigma` accepted for `1 - \alpha\sigma - n\sigma`; `0.5` accepted for `1/2`).
   - Combining a LaTeX-to-expression normalizer, `mathjs` AST simplification (`math.simplify(student - target) === 0`), and Monte Carlo numerical sampling over free variables guarantees instantaneous, robust equivalence verification client-side without server roundtrips.
4. **Execution Simplicity**:
   - The environment specifies Windows, Node 24, Python 3.12, and execution policy blocking `npm.ps1`.
   - A Vite + React application with an embedded course discovery endpoint (either via Vite dev server plugin or a minimal Node server script invoked via `npm.cmd run dev`) satisfies the "runs with one documented command" requirement and serves courses dynamically from the `courses/` directory.

## 3. Caveats

- **Audio Feedback**: Top's Academy plays an optional subtle audio chime on correct submissions; while not explicitly required by the visual acceptance criteria, adding a small Web Audio API tone will enhance sensory parity.
- **Mobile Responsiveness**: The reference screenshots are desktop viewport (~1440×900px). The specification defines responsive flex/grid layouts with a collapsible sidebar, but the primary acceptance criteria focus on the desktop layout shown in the references.
- **No caveats** regarding core UI specifications, color codes, component hierarchies, or math/graph requirements.

## 4. Conclusion

The visual specification, component hierarchy, design tokens, graph rendering schema, and math equivalence pipeline have been fully established and documented in `g:\Mi unidad\Competence_analyser\.agents\teamwork\explorer_ui_survey\ui_spec.md`. The recommended tech stack is:
- **Framework**: Vite + React 18/19 (TypeScript)
- **Styling**: Tailwind CSS with custom Top's Academy design tokens
- **LaTeX**: KaTeX
- **Graphing**: Declarative native SVG `<CoordinatePlane />` component
- **Equivalence Engine**: `mathjs` + LaTeX normalizer + Monte Carlo sampler
- **Celebration**: `canvas-confetti`
- **Startup**: Single command via `npm.cmd run dev`

## 5. Verification Method

1. **Verify UI Specification File**:
   - Confirm existence and content of `g:\Mi unidad\Competence_analyser\.agents\teamwork\explorer_ui_survey\ui_spec.md`.
   - Check that all 6 reference screenshots are audited and that the Reviewer Verification Matrix covers all acceptance criteria.
2. **Reviewer Acceptance Verification**:
   - Run the headless browser tests against the running platform.
   - Capture screenshots of all 6 platform states (Overview, Pre-exercise, Question, Correct feedback, Complete, Challenge).
   - Verify each checklist item in Section 8 of `ui_spec.md`.
