# Top's Academy: Comprehensive UI/UX Specification & Frontend Architecture

**Document Version**: 1.0.0  
**Author**: UI Specification Explorer (`explorer_ui_survey`)  
**Target Milestone**: R1 & Visual Fidelity Acceptance Criteria  
**Generated Date**: 2026-10-11  

---

## 1. Executive Summary & Reference Screenshot Audit

This specification establishes the complete visual design system, component hierarchy, interactive behaviors, and technical stack required to faithfully reproduce the Top's Academy learning experience. The analysis is derived from pixel-level inspection of the six reference screenshots in `Khan_academy_images_references/` and the system requirements in `ORIGINAL_REQUEST.md`.

### Screenshot Audit Summary

| Reference Image | Screen / State | Key Visual & Interactive Features Identified |
| :--- | :--- | :--- |
| **`Courser_overview.png`** | Course Hub & Mastery Matrix | • Two-column layout: sticky left sidebar (~260px) + main course dashboard.<br>• Left sidebar: circular course badge, course title, "6 UNITS" badge, unit list with dividers.<br>• Main header: breadcrumb (`🏠 · Math`), large bold title, `Course mastery: 100% ⓘ`.<br>• Mastery Legend: Mastered (purple solid), Proficient (lavender solid), Familiar (amber bottom-half), Attempted (amber outline), Not started (grey outline), Quiz (`⚡`), Unit test (`★`).<br>• Mastery Grid: Units 1–4 (col 1), Units 5–6 + Course Challenge card (col 2). Crown blocks grouped with Quiz bolts and Unit Test star.<br>• Course Challenge Card: rounded border, `📖 COURSE CHALLENGE: 100%`, `✓ a year ago`, action link. |
| **`pre_exercise.png`** | Pre-Exercise / "Ready to practice?" | • Top nav: Skill title (`Limits intro`), Microsoft Teams & Share links.<br>• Top notification banner: grey info icon `ⓘ` with mastery level notice.<br>• Hero container: deep royal blue (`#1865f2`), centered white text (`Ready to practice?`, `Okay, show us what you can do!`, `4 questions`).<br>• Bottom illustration: playful geometric mascot polygons with smiling cartoon eyes.<br>• Bottom bar: white footer, `<` back button, solid blue `Let's go` CTA button. |
| **`multiple_answer_question.png`** | Question Interaction & Graph Rendering | • Question stem with inline KaTeX math ($f$, $x = 3$).<br>• Cartesian coordinate graph ($[-7, 7] \times [-7, 7]$ grid): black axes with arrowheads, cyan function curve, open hole circle at $(3, -4)$, italic curve label $f$.<br>• Sub-stem question prompt with display limit: $\lim_{x \to 3} f(x)$.<br>• Options list: `Choose 1 answer:`, lettered circles (A, B, C, D), subtle dividers.<br>• Bottom footer bar: reload icon `🔄`, `Do 4 problems`, 4 progress dots (`○ ○ ○ ○`), blue text `Skip`, disabled grey `Check` button. |
| **`good_answer.png`** | Correct Feedback & Popover Toast | • Selected correct option: 2px solid green border (`#14a34b`), green letter pill with checkmark `✓ D`, dark green text.<br>• Floating feedback popover ("toast"): white card with speech-bubble pointer pointing down to `Next question` button; green circle checkmark `✓`, bold header `Good work!`, subtitle `Keep going.`, blue link `See a step-by-step solution.`, close `✕`.<br>• Confetti accents bursting around CTA button.<br>• Bottom bar: `🔄 2 of 4  ✓ ✓ ○ ○`, disabled `Skip`, solid blue `Next question` button. |
| **`exercise_completed.png`** | Exercise Complete & Celebration | • Top bar: skill title and course mastery bar.<br>• Blue hero container (`#1865f2`): full celebration canvas with multicolored confetti particles (streamers, ribbons, triangles, squares).<br>• Left hero content: white line-art thumbs-up icon with radiating lines, large `Exercise complete!`, bold score `4/4 correct`.<br>• Right hero card: white rounded card with shadow, icon, next steps / summary.<br>• Bottom footer: left blue link `🔄 Try again`, right blue CTA button `Up next: Lesson 2`. |
| **`course_challenge.png`** | Course Challenge Overview | • Left sidebar active state: book icon, `< COURSE: DIFFERENTIAL CALCULUS Course challenge >`, highlighted blue card with left border, notebook illustration.<br>• Main hero (royal blue `#1865f2`): `Ready for a challenge?`, `Test yourself on the skills in this course...`, `30 questions • 30 - 45 minutes`.<br>• Illustration: open notebook with pencil and geometric stars.<br>• Bottom footer: solid blue `Let's go` button. |

---

## 2. Design System & Tokens

### 2.1 Color Palette

```css
:root {
  /* Brand / Primary */
  --ka-blue: #1865f2;              /* Primary buttons, links, active borders */
  --ka-blue-hover: #1456c7;        /* Button hover state */
  --ka-blue-light: #f0f7ff;        /* Sidebar active background, selected tint */
  --ka-blue-hero: #1865f2;         /* Pre-exercise and celebration hero background */

  /* Mastery Levels */
  --ka-mastered: #583b8b;          /* Deep royal purple (Mastered) */
  --ka-proficient: #8377b2;        /* Lavender purple (Proficient) */
  --ka-familiar: #e07a21;          /* Warm amber/orange (Familiar) */
  --ka-attempted: #f3801e;         /* Warm amber border (Attempted) */
  --ka-not-started: #88939e;       /* Neutral grey border (Not started) */
  --ka-quiz-bolt: #59606d;         /* Lightning bolt grey */
  --ka-test-star: #59606d;         /* Unit test star grey */

  /* Feedback & Validation */
  --ka-green-border: #14a34b;      /* Correct answer card border */
  --ka-green-badge: #008a00;       /* Correct answer pill / check circle */
  --ka-green-text: #0b6b2d;        /* Correct answer label */
  --ka-red-border: #d92938;        /* Incorrect answer card border */
  --ka-red-badge: #dc2626;         /* Incorrect answer pill */
  --ka-red-text: #991b1b;          /* Incorrect answer label */

  /* Neutrals & Text */
  --ka-text-primary: #21242c;      /* Primary headings, body text */
  --ka-text-secondary: #59606d;    /* Subtitles, instructions, metadata */
  --ka-text-muted: #88939e;        /* Disabled text, unattempted dots */
  --ka-bg-white: #ffffff;          /* Card backgrounds, header */
  --ka-bg-canvas: #fafbfc;         /* Page background */
  --ka-border-subtle: #eaedf1;     /* Dividers, option rows */
  --ka-border-card: #e4e7eb;       /* Card borders */
  --ka-border-disabled: #d1d5db;   /* Disabled button background */

  /* Graph Colors */
  --ka-graph-curve: #00a2e8;       /* Primary curve (cyan/blue) */
  --ka-graph-curve-alt: #e07a21;   /* Secondary curve (orange) */
  --ka-graph-grid: #e2e8f0;        /* Coordinate grid lines */
  --ka-graph-axis: #21242c;        /* Coordinate axes & tick marks */
  --ka-graph-open-point: #ffffff;  /* Interior of open hole */
}
```

### 2.2 Typography Scale

The font family should use standard modern sans-serif:  
`font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;`  
Mathematical expressions use KaTeX’s bundled fonts (`KaTeX_Main`, `KaTeX_Math`, `KaTeX_Size1`).

| Level | Size | Weight | Line Height | Usage |
| :--- | :--- | :--- | :--- | :--- |
| **Hero Heading** | 32px – 36px | 700 (Bold) | 1.2 | "Ready to practice?", "Exercise complete!", "Differential Calculus" |
| **Section Heading** | 22px – 24px | 700 (Bold) | 1.3 | Unit titles, Course challenge header |
| **Question Stem** | 18px – 20px | 400 (Regular) / 600 (Semibold) | 1.5 | Problem statement, mathematical definitions |
| **Prompt / Sub-stem** | 16px – 18px | 700 (Bold) | 1.4 | "What is a reasonable estimate...", "Choose 1 answer:" |
| **Body / Option** | 16px | 400 (Regular) | 1.4 | Multiple choice options, explanation text |
| **Meta / Small** | 13px – 14px | 500 (Medium) | 1.4 | Hints titles, progress label `2 of 4`, footer hints |
| **Micro / Badge** | 11px – 12px | 700 (Bold) | 1.2 | `UNIT 1`, `6 UNITS`, option letter badges |

### 2.3 Spacing, Borders & Shadows
- **Card Border Radius**: 8px (default cards), 6px (options, input fields), 4px (action buttons), 9999px (circular badges and progress dots).
- **Divider Lines**: `1px solid var(--ka-border-subtle)` (`#eaedf1`).
- **Popover Toast Shadow**: `box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12), 0 1px 3px rgba(0, 0, 0, 0.08);`.
- **Button Padding**: `10px 24px` for primary CTA; `8px 16px` for secondary buttons.

---

## 3. Comprehensive Component Specifications

### 3.1 Course Overview & Navigation (`Courser_overview.png`)

```
+----------------------------------------------------------------------------------------------------+
|  LEFT SIDEBAR (~260px)       |  MAIN CONTENT AREA                                                  |
|                              |                                                                    |
|  [O] Differential Calculus   |  🏠 · Math                                                          |
|      6 UNITS                 |  Differential Calculus                                             |
|  --------------------------- |  Course mastery: 100% ⓘ                                            |
|  UNIT 1                      |                                                                    |
|  Limits and continuity       |  [👑] Mastered [👑] Proficient [ ] Familiar [ ] Attempted ...       |
|  --------------------------- |  ----------------------------------------------------------------  |
|  UNIT 2                      |  Unit 1:  [👑][👑][👑][👑][⚡][👑][👑][👑][⚡][★]                  |
|  Derivatives: basic rules    |  Unit 2:  [👑][👑][👑][👑][⚡][👑][👑][⚡][★]                      |
|  --------------------------- |  Unit 3:  [👑][👑][👑][⚡][👑][👑][⚡][★]                          |
|  UNIT 3                      |  Unit 4:  [👑][👑][👑][👑][⚡][👑][👑][⚡][★]                      |
|  Chain rule & advanced       |  ----------------------------------------------------------------  |
|  ...                         |  Unit 5:  [👑][👑][👑][👑][⚡][★]                                  |
|                              |  Unit 6:  [👑][👑][👑][⚡][★]                                      |
|                              |  +--------------------------------------------------------------+  |
|                              |  | 📖 COURSE CHALLENGE: 100%       ✓ a year ago                 |  |
|                              |  | Test your knowledge of the skills in this course.             |  |
|                              |  | Take Course challenge again                                   |  |
|                              |  +--------------------------------------------------------------+  |
+----------------------------------------------------------------------------------------------------+
```

#### Detailed Element Specifications:
1. **Left Navigation Sidebar**:
   - Width: 260px fixed width on desktop, collapsible on mobile.
   - Top Header item: Circular icon with teal background (`#00a2e8`), course title (`font-weight: 700`), unit count badge (`6 UNITS`).
   - Active state: background `#f0f7ff`, left border `4px solid #1865f2`.
   - Unit List: Each item displays uppercase unit index `UNIT <N>` (font size 11px, grey `#637381`) and unit title (font size 14px, `#21242c`). Separated by 1px dividers.
2. **Main Breadcrumb & Header**:
   - Blue home icon `🏠` followed by clickable breadcrumb `· Math`.
   - Heading `<h1>`: 32px bold, `#21242c`.
   - Course Mastery line: `Course mastery: <X>%` with an information icon `ⓘ` providing a tooltip explaining mastery point calculation.
3. **Mastery Legend Row**:
   - Flex row displaying all 7 states:
     - **Mastered**: Purple solid rectangle (`#583b8b`) with white crown `👑`.
     - **Proficient**: Lavender solid rectangle (`#8377b2`) with white crown `👑`.
     - **Familiar**: Amber rectangle (`#e07a21`) with half-filled bottom.
     - **Attempted**: White rectangle with amber border (`#f3801e`).
     - **Not started**: White rectangle with grey border (`#88939e`).
     - **Quiz**: Lightning bolt icon `⚡` + "Quiz".
     - **Unit test**: Star icon `★` + "Unit test".
4. **Mastery Matrix (Units 1 to N)**:
   - Grouped into two visual columns (Units 1–4 left, Units 5–6 right).
   - Each unit row displays the unit label (`Unit 1`), followed by an inline wrapped cluster of mastery blocks:
     - Size: 26px × 26px rounded square (border-radius 4px).
     - Competency blocks show the crown icon in the color corresponding to that competency's mastery status.
     - Interspersed Quiz markers (`⚡` in grey badge) placed every 4–5 competencies.
     - Unit test marker (`★` in grey badge) placed at the end of the unit.
     - **Hover Interaction**: Displays an accessible tooltip with the competency ID, title, and current mastery level.
     - **Click Interaction**: Clicking any competency block launches that competency's practice session. Clicking a Quiz or Unit Test marker launches that assessment session.
5. **Course Challenge Card**:
   - Sits at the bottom of the right column.
   - Border: `1px solid #e4e7eb`, border radius 8px, padding 20px.
   - Title: `📖 COURSE CHALLENGE: <X>%`.
   - Subtitle: `Test your knowledge of the skills in this course.`.
   - Status: `✓ Completed` / `Not completed`.
   - Action: Blue link button `Take Course challenge` / `Take Course challenge again`.

---

### 3.2 Pre-Exercise Screen ("Ready to practice?") (`pre_exercise.png`)

1. **Top Bar**:
   - Competency / skill title centered: e.g. "Limits intro" (`font-weight: 700`, 20px).
   - Action links: "Share link" with icon.
   - Back button: circular `<` button on top-left to return to Course Overview.
2. **Alert Banner** (conditional):
   - If user already mastered the skill: `ⓘ You're already a master of this skill — there are no more levels to reach on this practice!`.
   - Background `#ffffff` or `#f0f7ff`, border `1px solid #e4e7eb`, border-radius 6px, padding 12px 16px.
3. **Blue Hero Canvas**:
   - Background: `background-color: var(--ka-blue-hero);` (`#1865f2`).
   - Dimensions: minimum height 420px, flexbox column, align center, justify center.
   - Content:
     - Title: `Ready to practice?` (`font-size: 36px; font-weight: 700; color: #ffffff;`).
     - Subtitle: `Okay, show us what you can do!` (`font-size: 18px; color: #ffffff; margin-top: 8px;`).
     - Problem count: `4 questions` (or `N questions`, `font-size: 16px; font-weight: 600; color: #ffffff; margin-top: 16px;`).
   - **Playful Character Mascots**:
     - Three polygon character illustrations sitting at the bottom of the blue hero.
     - Mascot 1: Deep textured blue polygon with smiling cartoon eyes looking up.
     - Mascot 2: Mint/cyan rounded polygon with smiling cartoon eyes.
     - Mascot 3: Periwinkle polygon with smiling cartoon eyes.
     - Implemented as inline SVG vector graphics for crisp scaling and zero external assets.
4. **Bottom Footer Bar**:
   - Fixed or sticky at bottom of viewport, height 72px, background `#ffffff`, border-top `1px solid #e4e7eb`.
   - Left: Return back `<` button.
   - Right: Primary CTA button `Let's go`:
     - Background: `#1865f2`, color: `#ffffff`, font-size: 16px, font-weight: 600, border-radius 4px, padding: 10px 24px.
     - Hover: background `#1456c7`.

---

### 3.3 Question Interaction Screen (`multiple_answer_question.png`)

```
+-----------------------------------------------------------------------------------+
|  The function f is defined for all real numbers except for x = 3.                 |
|                                                                                   |
|                                 y                                                 |
|                                 ↑                                                 |
|                           7 +---|---+                                             |
|                           6 +---|---+                                             |
|                        f  5 +---|---+                                             |
|                      \    4 +---|---o (3, -4)                                     |
|                       \   3 +---|---+                                             |
|                        \  2 +---|---+                                             |
|                         \ 1 +---|---+                                             |
|                  <--------+---+---+---+--------> x                                |
|                  -7 -6 -5 -4 -3 -2 -1   1 2 3 4 5 6 7                             |
|                                                                                   |
|  What is a reasonable estimate for lim_{x -> 3} f(x)?                             |
|                                                                                   |
|  Choose 1 answer:                                                                 |
|  -------------------------------------------------------------------------------  |
|  ( A )   3                                                                        |
|  -------------------------------------------------------------------------------  |
|  ( B )  -4                                                                        |
|  -------------------------------------------------------------------------------  |
|  ( C )  -3                                                                        |
|  -------------------------------------------------------------------------------  |
|  ( D )   The limit doesn't exist                                                  |
+-----------------------------------------------------------------------------------+
|  [🔄] Do 4 problems   ○ ○ ○ ○                                    Skip   [ Check ] |
+-----------------------------------------------------------------------------------+
```

#### Detailed Question Layout:
1. **Question Stem**:
   - Clear typography, 18px font size, `#21242c`.
   - Supports inline LaTeX ($...$) and block LaTeX ($$...$$) rendered via KaTeX.
2. **Interactive / Coordinate Graph Widget**:
   - Placed directly between stem and sub-question when the question JSON contains a `graph` specification.
   - Square aspect ratio (typically 360px × 360px or 400px × 400px).
   - Crisp vector Cartesian grid (labels, ticks, arrows, curves, open/closed points). Detailed schema in Section 4.
3. **Sub-stem & Interaction Prompt**:
   - Sub-stem: 18px bold font, e.g. `What is a reasonable estimate for \lim_{x \to 3} f(x)?`.
   - Interaction prompt: 14px semibold grey text (`#59606d`), e.g. `Choose 1 answer:` or `Choose all answers that apply:`.
4. **Answer Options & Input Types**:
   - **Type A: `multiple_choice_7_options`**:
     - Exactly 7 options rendered as stacked list items.
     - Each item is enclosed between 1px divider lines (`#eaedf1`).
     - Padding: 16px 20px.
     - Circular badge on left: 32px diameter, border `2px solid #88939e`, letter A through G inside (`#59606d`, bold 14px).
     - Selection state (prior to check): light blue background (`#f0f7ff`), border `2px solid #1865f2`, circle badge filled with `#1865f2` and white letter.
     - Hover state: light background `#fafbfc`.
     - Shuffled order: The presentation order must be randomized dynamically on session start!
   - **Type B: `multiple_select`**:
     - 4 to 6 options rendered as stacked list items.
     - Left indicator: Square checkbox (border radius 4px) with letter badge inside.
     - Multiple items can be checked/unchecked.
     - Selected state: blue border, checked checkbox icon.
   - **Type C: `fill_in_the_blank`**:
     - Large clean text/math input field:
       - Border: `2px solid #88939e`, border-radius 6px, padding 14px 18px, font-size 18px.
       - Focus state: `border-color: #1865f2; box-shadow: 0 0 0 3px rgba(24, 101, 242, 0.2);`.
       - Placeholder: informative hint (e.g. `1 - (alpha + n)*sigma` or `0.5`).
       - Live LaTeX preview below input field: renders student's typed expression in formatted KaTeX math so the student can verify their input syntax.
5. **Progressive Hints System**:
   - Link below the question: `💡 Stuck? Review related articles/videos or use a hint.` (blue link).
   - Clicking opens the hint accordion / drawer.
   - Each question has 3 to 5 progressive hints (`hints` array in JSON).
   - Students can reveal hints one by one (`Get hint (1 of 4)`, `Get next hint (2 of 4)`).
   - Top's Academy rule: Using hints marks the question as "attempted with hint", which does not award full mastery points for that session.
6. **Bottom Action & Progress Bar**:
   - Layout: Fixed bottom bar, height 70px, background `#ffffff`, border-top `1px solid #e4e7eb`, flex items-center justify-between, padding `0 32px`.
   - **Left / Center**:
     - Session reload icon: `🔄` (svg icon, 18px).
     - Counter label: `Do 4 problems` (or `2 of 4` after progress).
     - **Progress Dots**:
       - Row of dots corresponding to the session length (e.g. 4 dots).
       - Size: 10px diameter, margin `0 4px`.
       - State 1 (Unanswered): `border: 2px solid #88939e; background: transparent;`.
       - State 2 (Current question): `border: 2px solid #21242c; background: transparent; transform: scale(1.15);`.
       - State 3 (Answered Correctly): Solid green circle with white checkmark `✓` (`background: #14a34b;`).
       - State 4 (Answered Incorrectly / Skipped): Solid grey circle with red dot or `✗` (`background: #dc2626;`).
   - **Right**:
     - `Skip` button: Text link in blue (`#1865f2`), clickable when unchecked. Disabled when checked.
     - `Check` button:
       - Disabled state: background `#d1d5db`, color `#ffffff`, cursor `not-allowed`.
       - Enabled state: background `#1865f2`, color `#ffffff`, cursor `pointer`, font-weight 600, border-radius 4px, padding `10px 24px`.
       - Hover state: background `#1456c7`.

---

### 3.4 Correct Answer Feedback State (`good_answer.png`)

```
+-----------------------------------------------------------------------------------+
|  [✓ D]  The limit doesn't exist                                                   |
|  (Container: 2px solid #14a34b, letter pill: solid #008a00 with white checkmark)  |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|                                                       +-------------------------+ |
|                                                       | [✓]  Good work!       ✕ | |
|                                                       |      Keep going.        | |
|                                                       |                         | |
|                                                       | See a step-by-step      | |
|                                                       | solution.               | |
|                                                       +------------V------------+ |
|  [🔄] 2 of 4   ✓ ✓ ○ ○                                   Skip   [ Next question ] |
+-----------------------------------------------------------------------------------+
```

#### Detailed Feedback Specifications:
1. **Option Container Transformation**:
   - Border: changes to `2px solid #14a34b` with border radius 6px.
   - Badge on left: transforms from neutral circle into a solid green pill (`#008a00` or `#14a34b`) displaying `✓ <Letter>`.
   - Content typography: colored `#0b6b2d`.
2. **Bottom Bar State Transformation**:
   - Progress dots: the current dot converts to a solid green checkmark `✓`.
   - Label updates from `Do 4 problems` to `2 of 4`.
   - `Skip` button: becomes disabled (`color: #d1d5db; pointer-events: none;`).
   - `Check` button: transforms into `Next question` button (Khan blue `#1865f2`, white text, font-weight 600).
   - Enter key listener: pressing `Enter` automatically advances to the next question.
3. **Floating Toast / Popover Card ("Good work!")**:
   - **Positioning**: Absolute or fixed popover anchored directly above the `Next question` button.
   - **Pointer / Arrow**: Downward triangle pointer pointing directly at the top center of the `Next question` button (`width: 16px; height: 8px;`).
   - **Card Styling**:
     - Background: `#ffffff`.
     - Border: `1px solid #e4e7eb`.
     - Border-radius: 8px.
     - Box shadow: `0 4px 20px rgba(0, 0, 0, 0.12)`.
     - Width: ~280px to 320px.
     - Padding: 16px 20px.
     - Close button `✕` at top right.
   - **Header Row**:
     - Large green circular icon: 32px diameter, background `#14a34b`, containing a bold white checkmark `✓`.
     - Title: `Good work!` (bold 18px, `#21242c`).
     - Subtitle: `Keep going.` (14px, `#59606d`).
   - **Step-by-step Solution Link**:
     - Blue text link: `See a step-by-step solution.`.
     - Clicking this expands an inline modal or collapsible drawer displaying the full analytical step-by-step derivation (`detailed_solution` from the question JSON) and any common misconception warning (`common_misconception_warning`).
4. **Confetti Accents**:
   - A burst of colorful confetti particles shoots up from the bottom right around the `Next question` button!

---

### 3.5 Incorrect Answer Feedback State

For completeness (and matching Top's Academy behavior when an incorrect answer is submitted):
1. **Option Container**:
   - If single choice: selected wrong option gets a `2px solid #dc2626` border, letter pill turns red with `✗ <Letter>`.
2. **Toast Popover**:
   - Positioned above the action button.
   - Icon: Red circle with `✗` or neutral yellow lightbulb `💡`.
   - Title: `Not quite yet.` or `Try again`.
   - Subtitle: `Get help or try another answer.`.
   - Action buttons inside toast:
     - `Get a hint` (reveals the first hint).
     - `Try again` (allows clearing selection and picking again).
3. **Bottom Bar**:
   - Button label remains `Check` or becomes `Try again` until correct answer is achieved or skipped.
   - Progress dot: marked as incorrect (red dot or `✗`).

---

### 3.6 Exercise Complete Screen (`exercise_completed.png`)

1. **Top Header & Course Mastery**:
   - Shows current course and competency title ("Limits intro").
   - Course mastery summary bar: `Course mastery: <X>% ⓘ`.
   - Unit mastery row with updated crown indicators.
2. **Royal Blue Hero Container (`#1865f2`)**:
   - Full container width, minimum height 450px.
   - Background: `background: #1865f2;`.
   - Multi-colored confetti animation running continuously across the hero canvas.
   - **Left Content**:
     - Large white line-art illustration: Thumbs-up hand with radiating lines (`👍` style).
     - Heading: `Exercise complete!` (font-size 36px, font-weight 700, color white).
     - Score display: `4/4 correct` (or `X/N correct`, font-size 22px, font-weight 700, color white).
   - **Right Content Card**:
     - White card with rounded corners (12px), soft shadow, padding 28px, width ~380px.
     - Icon: Graduation cap or mastery badge.
     - Title: `Mastery Points Leveled Up!`.
     - Breakdown: Points earned, new mastery tier reached (e.g. `Familiar → Proficient`).
3. **Bottom Action Footer Bar**:
   - Fixed at bottom, height 72px, background `#ffffff`, border-top `1px solid #e4e7eb`.
   - Left side: Blue text button with refresh icon `🔄 Try again`:
     - Resets the practice session and pulls a fresh randomized batch of questions for this competency.
   - Right side: Primary CTA button `Up next: <Next Competency Title>`:
     - Blue solid button `#1865f2`, white text, bold, padding 10px 24px.
     - Advances directly to the next unmastered competency in the course.

---

### 3.7 Course Challenge Interface (`course_challenge.png`)

1. **Sidebar State**:
   - Course title: `Differential Calculus`.
   - Navigation subheader: `< COURSE: DIFFERENTIAL CALCULUS Course challenge >`.
   - Highlighted active card:
     - Border left: `4px solid #1865f2`.
     - Background: `#f0f7ff`.
     - Title: `Course challenge` (bold blue `#1865f2`).
     - Subtitle: `Test your knowledge of the skills in this course.`.
   - Illustration: Open notebook and pencil line art.
2. **Main Challenge Hero (Royal Blue `#1865f2`)**:
   - Heading: `Ready for a challenge?` (font-size 36px, bold, white).
   - Subtitle: `Test yourself on the skills in this course and earn mastery points for what you already know!` (font-size 18px, white).
   - Session Metrics: `30 questions • 30 - 45 minutes` (font-size 16px, bold, white).
   - Illustration: Open notebook with writing hand and decorative sparks.
3. **Bottom Action Bar**:
   - Right CTA: `Let's go` button in solid blue `#1865f2`.
4. **Active Challenge Session**:
   - Presents ~30 questions sampled uniformly across all competencies in the course.
   - Progress dots: 30 dots (or paginated indicator).
   - Calculates comprehensive mastery updates across all tested competencies upon completion.

---

## 4. Graph Widget Specification (Perseus-style Vector Graphing)

The reference screenshots (`multiple_answer_question.png`, `good_answer.png`) show a clean mathematical coordinate plane. The platform must render these dynamically from a declarative JSON schema.

### 4.1 Coordinate Plane Visual Standards
- **Grid Range**: Typically $[-7, 7] \times [-7, 7]$ or $[-10, 10] \times [-10, 10]$.
- **Grid Lines**: Spaced every 1 unit, stroke `#e2e8f0`, stroke-width 1px.
- **Axes**: $x$-axis and $y$-axis with black stroke `#21242c`, stroke-width 2px. Arrowheads on both ends.
- **Labels**: Numeric labels on tick marks (e.g. $-7, -6, \dots, 6, 7$), font size 12px, font-family serif/math (`KaTeX_Math` or Times New Roman).
- **Curves**: Smooth line path, stroke `#00a2e8`, stroke-width 3px.
- **Open Points (Holes)**: Circle at $(x_0, y_0)$, radius 5px, stroke `#00a2e8`, stroke-width 2.5px, fill `#ffffff` (white).
- **Closed Points (Filled)**: Circle at $(x_1, y_1)$, radius 5px, fill `#00a2e8`.
- **Curve Label**: Italic label (e.g. $f$, $g$, $h$) placed adjacent to curve.

### 4.2 Declarative Graph JSON Schema
The question JSON format should support an optional `graph` object:

```json
{
  "graph": {
    "type": "cartesian",
    "x_range": [-7, 7],
    "y_range": [-7, 7],
    "step": 1,
    "width": 360,
    "height": 360,
    "curves": [
      {
        "id": "curve-f",
        "label": "f",
        "label_pos": [-4, 2],
        "color": "#00a2e8",
        "expression": "0.08 * Math.pow(x - 3, 3) - 4",
        "domain": [-6, 7]
      }
    ],
    "points": [
      {
        "x": 3,
        "y": -4,
        "type": "open",
        "color": "#00a2e8"
      },
      {
        "x": 0,
        "y": 5,
        "type": "closed",
        "color": "#00a2e8"
      }
    ]
  }
}
```

### 4.3 Rendering Recommendation
**Native React SVG Component (`<CoordinatePlane />`)**:
- Zero external runtime library dependencies.
- Perfect crispness on High-DPI screens.
- Completely accessible and testable via DOM queries (`svg`, `path`, `circle.open-point`, `circle.closed-point`).
- Eliminates canvas blurry rendering or WebAssembly startup overhead.

---

## 5. Mathematical Equivalence Engine Specification

Requirement R1 states:
> *"grade fill-in-the-blank answers by mathematical equivalence (not just string match), e.g. `1-(alpha+n)*sigma` accepted for `1 - \alpha\sigma - n\sigma`; `0.5` accepted for `1/2`"*

### 5.1 Architecture & Pipeline

```
  Student Input String
         │
         ▼
 ┌──────────────────────────┐
 │ 1. LaTeX-to-ASCII        │  Converts `\alpha` -> `alpha`, `\frac{a}{b}` -> `((a)/(b))`
 │    Normalizer            │  Replaces unicode minus `−` with `-`, removes spaces & `\text{}`
 └─────────────┬────────────┘
               │
               ▼
 ┌──────────────────────────┐
 │ 2. Exact & Alias Match   │  Checks `target_value` and `accepted_equivalents` array
 └─────────────┬────────────┘
               │ (if no exact match)
               ▼
 ┌──────────────────────────┐
 │ 3. Algebraic AST         │  Using mathjs (`math.parse`), simplify difference:
 │    Canonicalizer         │  exprDiff = math.simplify(`(${student}) - (${target})`)
 └─────────────┬────────────┘  If exprDiff.toString() === "0" -> EQUIVALENT
               │ (if symbolic simplification inconclusive)
               ▼
 ┌──────────────────────────┐
 │ 4. Monte Carlo Numerical │  Identify all free variables (e.g. `alpha`, `sigma`, `n`).
 │    Evaluation Engine     │  Sample N=10 random tuples (avoiding singularities).
 └─────────────┬────────────┘  If max(|student(x) - target(x)|) < 1e-7 -> EQUIVALENT
               │
               ▼
      Boolean Result (True/False)
```

### 5.2 Implementation Strategy (JavaScript / mathjs)
Using `mathjs` directly in the frontend:
1. **Fraction and Numeric Normalization**: `1/2` evaluates to `0.5`, `2/4` evaluates to `0.5`.
2. **Algebraic Symbol Equivalence**: `1-(alpha+n)*sigma` vs `1 - alpha*sigma - n*sigma`.
   - Monte Carlo test: Substitute `alpha = 2.31`, `n = 4.15`, `sigma = 0.87`.
   - Target evaluates to: `1 - (2.31 + 4.15) * 0.87 = 1 - 5.6202 = -4.6202`.
   - Student evaluates to: `1 - (2.31*0.87) - (4.15*0.87) = -4.6202`.
   - Difference $< 10^{-7} \implies$ **CORRECT**.
3. **Security & Sandboxing**: `mathjs` provides a safe expression compiler that does not execute arbitrary JavaScript (`eval` is never used).

---

## 6. Top's Academy Mastery Model & Local Persistence

### 6.1 Mastery Levels & Progression Rules

Top's Academy uses a 5-tier mastery ladder:

```
[Not started] ──(Any practice attempted)──> [Attempted]
                                                  │
                                          (≥70% correct)
                                                  │
                                                  ▼
                                            [Familiar]
                                                  │
                             (100% in Practice OR ≥80% in Quiz)
                                                  │
                                                  ▼
                                            [Proficient]
                                                  │
                              (100% in Unit Test OR Course Challenge)
                                                  │
                                                  ▼
                                             [Mastered]
```

- **Not started**: 0% progress, unattempted.
- **Attempted**: The user has practiced the skill but scored $< 70\%$ (or used hints on all questions).
- **Familiar**: The user scored $\ge 70\%$ on a practice session.
- **Proficient**: The user scored $100\%$ on a practice session without hints, or passed the Unit Quiz.
- **Mastered**: The user achieved a perfect score on the skill during a Unit Test or Course Challenge.
- **Degradation / Demotion**: Getting questions wrong during a Unit Test or Course Challenge drops a skill by one tier (e.g. Mastered $\to$ Proficient).
- **Course Mastery % Calculation**:
  $$\text{Course Mastery \%} = \frac{\sum_{i=1}^N \text{tier\_points}(\text{skill}_i)}{N \times 100} \times 100\%$$
  where Not started = 0 pts, Attempted = 25 pts, Familiar = 50 pts, Proficient = 80 pts, Mastered = 100 pts.

### 6.2 Local Persistence (`localStorage`)
All state persists in `localStorage` under key `khan_academic_progress_v1`:

```json
{
  "active_course_id": "TEMA_02_SISTEMAS_EDOS_MACRO",
  "courses": {
    "TEMA_02_SISTEMAS_EDOS_MACRO": {
      "mastery_points": 85,
      "competencies": {
        "Hab-01": {
          "status": "Mastered",
          "points": 100,
          "last_practiced": "2026-10-10T19:30:00Z",
          "history": [{ "date": "2026-10-10T19:30:00Z", "score": 4, "total": 4 }]
        },
        "Hab-02": {
          "status": "Proficient",
          "points": 80,
          "last_practiced": "2026-10-10T20:10:00Z",
          "history": [{ "date": "2026-10-10T20:10:00Z", "score": 4, "total": 4 }]
        }
      },
      "course_challenge": {
        "completed": true,
        "last_score": 30,
        "total_questions": 30,
        "completed_at": "2026-10-09T15:00:00Z"
      }
    }
  }
}
```

---

## 7. Frontend Architecture Recommendations

### 7.1 Recommended Tech Stack

| Domain | Recommendation | Justification |
| :--- | :--- | :--- |
| **Framework & Build** | **Vite + React 18 / 19 (TypeScript)** | • Instant cold start (<300ms) with zero build overhead.<br>• Runs on Node 24 with standard `npm.cmd run dev`.<br>• Modular component architecture (Sidebar, Grid, QuestionCard, Toast, Graph). |
| **Styling** | **Tailwind CSS + Custom Khan Tokens** | • Exact color matching using Tailwind config (`ka-blue`, `ka-mastered`, etc.).<br>• Rapid flexbox and grid alignment matching screenshots.<br>• Clean CSS utility classes with scoped component styles for popover arrows. |
| **LaTeX Rendering** | **KaTeX (`katex` npm package)** | • Originally created by Top's Academy for this exact UI.<br>• Synchronous, ultra-fast math rendering without MathJax layout delays.<br>• Inline and block math support ($...$ and $$...$$). |
| **Graph Rendering** | **Native SVG Component (`<CoordinatePlane />`)** | • Lightweight, zero external dependencies.<br>• Pixel-perfect Cartesian grids with arrows, ticks, open/closed circles.<br>• DOM-inspectable for headless automated testing. |
| **Math Equivalence** | **`mathjs` + LaTeX Normalizer** | • Parses algebraic ASTs, expands and simplifies symbolic differences.<br>• Monte Carlo sampling for bulletproof equivalence verification.<br>• Runs client-side in browser without server roundtrips. |
| **Celebration / Confetti** | **`canvas-confetti`** | • Standard lightweight particle canvas library.<br>• Produces identical confetti streams, ribbons, and particle bursts. |
| **Course Discovery Server** | **Lightweight Node server (Vite dev server plugin or Express/Fastify)** | • Exposes `GET /api/courses` and `GET /api/courses/:id`.<br>• Automatically scans `courses/` directory.<br>• Single command startup (`npm.cmd run dev`) runs frontend + API together. |

---

## 8. Visual Fidelity Acceptance Checklist (Reviewer Matrix)

This checklist provides the exact criteria for the independent reviewer agent to verify against the 6 reference images:

- [ ] **1. Courser_overview.png**:
  - [ ] Left sidebar contains course circular badge, course title, and unit count badge.
  - [ ] Unit items in sidebar are separated by 1px dividers with uppercase `UNIT N` labels.
  - [ ] Main header shows breadcrumb (`🏠 · Math`), course title, and `Course mastery: X% ⓘ`.
  - [ ] Mastery legend shows all 7 states (Mastered purple, Proficient lavender, Familiar amber, Attempted outline, Not started grey, Quiz bolt, Unit test star).
  - [ ] Mastery grid displays competency blocks grouped by unit with interspersed Quiz markers and Unit Test markers.
  - [ ] Course Challenge card is displayed with book icon, completion status, description, and action link.
- [ ] **2. pre_exercise.png**:
  - [ ] Centered competency title with share links.
  - [ ] Blue hero panel (`#1865f2`) with centered white typography: `Ready to practice?`, `Okay, show us what you can do!`, and question count badge.
  - [ ] Polygon character mascot illustrations with smiling eyes at the bottom of the blue hero.
  - [ ] White footer bar with `<` back button and solid blue `Let's go` button.
- [ ] **3. multiple_answer_question.png**:
  - [ ] Question stem cleanly renders text and KaTeX math.
  - [ ] Cartesian graph displays axes, arrows, ticks, function curve, open/closed points, and curve label.
  - [ ] Multiple-choice options display circular letter badges (A, B, C, D) separated by dividers.
  - [ ] Bottom bar displays reload icon `🔄`, `Do 4 problems`, progress dots (`○ ○ ○ ○`), blue `Skip` text, and disabled `Check` button.
- [ ] **4. good_answer.png**:
  - [ ] Selected correct option is highlighted with 2px solid green border (`#14a34b`), green letter badge with checkmark (`✓ D`), and green text.
  - [ ] Progress dots show green checkmark `✓` for completed questions (`🔄 2 of 4  ✓ ✓ ○ ○`).
  - [ ] Floating speech-bubble toast popover appears directly above the CTA button with down-arrow pointer.
  - [ ] Toast displays green circular checkmark icon, `Good work!`, `Keep going.`, and blue link `See a step-by-step solution.`.
  - [ ] Confetti particles accent the bottom right action button.
  - [ ] Action button label transitions from `Check` to `Next question`.
- [ ] **5. exercise_completed.png**:
  - [ ] Full celebratory blue hero panel with multicolored confetti particles falling.
  - [ ] Left side displays thumbs-up illustration with radiating lines, `Exercise complete!`, and score `4/4 correct`.
  - [ ] Right side displays white card with mastery points leveled up summary.
  - [ ] Bottom footer bar displays `🔄 Try again` link on left and `Up next: [Skill]` blue button on right.
- [ ] **6. course_challenge.png**:
  - [ ] Sidebar displays active Course challenge item with blue accent border and notebook line art.
  - [ ] Blue hero displays `Ready for a challenge?`, description, and `30 questions • 30 - 45 minutes`.
  - [ ] Open notebook and pencil illustration on blue hero canvas.
  - [ ] Bottom footer displays solid blue `Let's go` button.
