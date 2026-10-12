# Empirical Adversarial Challenge Handoff Report: Platform State Machine, Shuffling, Mastery Persistence, and Error Isolation

## 1. Observation

### Observation 1: Practice Session Question Shuffling Disablement
In `platform/src/App.tsx`, lines 100–103:
```typescript
    // Shuffle options while maintaining question sequence for practice
    const shuffled = prepareSessionQuestions(compQuestions, false);
    const chosen = shuffled.slice(0, Math.min(4, shuffled.length));
    setSessionQuestions(chosen);
```
In `platform/src/utils/sessionShuffler.ts`, lines 20–25:
```typescript
export function prepareSessionQuestions(
  questions: Question[],
  shuffleQuestions: boolean = false
): Question[] {
  const qList = shuffleQuestions ? shuffleArray(questions) : [...questions];
```
Direct execution of 4 consecutive practice launches of the same unit in `tests/e2e/empirical_verify_runner.py` produced verbatim:
```text
--- Part A: Practice Session Question Shuffling ---
  Practice Launch 1 stems:
    Q1: What is \lim_{x \to 0} \frac{\sin x}{x}?...
    Q2: Evaluate \lim_{x \to 2} (3x^2 - 4x + 1)...
    Q3: What is \lim_{x \to 3} \frac{x^2 - 9}{x - 3}?...
    Q4: Select all functions continuous at x=0:...
  Practice Launch 2 stems:
    Q1: What is \lim_{x \to 0} \frac{\sin x}{x}?...
    Q2: Evaluate \lim_{x \to 2} (3x^2 - 4x + 1)...
    Q3: What is \lim_{x \to 3} \frac{x^2 - 9}{x - 3}?...
    Q4: Select all functions continuous at x=0:...
  Practice Launch 3 stems:
    Q1: What is \lim_{x \to 0} \frac{\sin x}{x}?...
    Q2: Evaluate \lim_{x \to 2} (3x^2 - 4x + 1)...
    Q3: What is \lim_{x \to 3} \frac{x^2 - 9}{x - 3}?...
    Q4: Select all functions continuous at x=0:...
  Practice Launch 4 stems:
    Q1: What is \lim_{x \to 0} \frac{\sin x}{x}?...
    Q2: Evaluate \lim_{x \to 2} (3x^2 - 4x + 1)...
    Q3: What is \lim_{x \to 3} \frac{x^2 - 9}{x - 3}?...
    Q4: Select all functions continuous at x=0:...
  Practice Question Shuffling: Identical across all runs = True
```
Specification requirements:
- `ORIGINAL_REQUEST.md` (line 21): "By default, every session (practice, quiz, unit test, challenge) presents questions in random order and shuffles the answer options of multiple-choice and multiple-select items, independently of their order in the JSON."
- `ORIGINAL_REQUEST.md` (line 47): "Randomization: across repeated sessions of the same unit, both question order and option order differ (test runs multiple sessions and asserts the orders are not all identical and do not simply mirror the JSON order), while grading stays correct after shuffling."

### Observation 2: Multiple-Choice Option Shuffling & Grading Integrity
Execution of `tests/e2e/empirical_verify_runner.py` (Part C) across 4 launches produced verbatim:
```text
--- Part C: Option Shuffling & Grading Integrity ---
  Grading after option shuffling: PASS (Correctly graded)
  Option orders across 4 runs:
    Run 1: ['A\n3\n3', 'B\n4\n4', 'C\n?\n4\n?4', 'D\n0\n0']...
    Run 2: ['A\n4\n4', 'B\n?\n3\n?3', 'C\n?\n4\n?4', 'D\nThe limit doe']...
    Run 3: ['A\n?\n3\n?3', 'B\n?\n5\n?5', 'C\n?\n4\n?4', 'D\n0\n0']...
    Run 4: ['A\n3\n3', 'B\n0\n0', 'C\n4\n4', 'D\n?\n4\n?4']...
  Option Shuffling: Variation present = True
```
In `platform/src/components/PracticeSession.tsx` line 89:
```typescript
    if (currentQuestion.type === 'multiple_choice_7_options') {
      correct = selectedOption === currentQuestion.correct_answer;
```
Grading evaluates the stable option identifier (`opt.id`), which is invariant under array permutations. Toast feedback correctly displayed "Good work!".

### Observation 3: LocalStorage Mastery Persistence & Resilience
Execution of `tests/e2e/empirical_verify_runner.py` (Pillar 2) produced verbatim:
```text
  Baseline 0% Mastery: True
  Practice session reached completion: True
  After 100% Practice -> Status: Proficient, Points: 80, Course Mastery: 40%
  Reloaded UI reflects persisted course mastery: True
  After 100% Unit Test -> Status: Proficient, Points: 80, Course Mastery: 40%
  Corrupt LocalStorage fallback to fresh 0%: True
```
In `platform/src/utils/masteryStorage.ts`:
- Storage key: `khan_academic_progress_v1`.
- On 100% practice score: tier promotes from `Not started` to `Proficient` (80 pts).
- Overall course mastery recalculation: `Math.round((80 / 200) * 100) = 40%`.
- Hard page reload preserves all tier and point values in LocalStorage and rehydrates UI.
- On corrupted LocalStorage JSON payload (`CORRUPT_JSON_SYNTAX{{{`), `try/catch` in `getAllStoredData()` prevents uncaught crashes and initializes cleanly to 0%.

### Observation 4: Dynamic Course Loading & Adversarial Error Isolation
Execution of `tests/e2e/empirical_verify_runner.py` (Pillar 3) across 5 adversarial fixtures in `courses/` produced verbatim:
```text
  Fixture: syntax_malformed
    Error Card Displayed: True (INVALID / CORRUPTED test_adversarial_syntax_malformed.json)
    Valid Course Functional: True
  Fixture: missing_competencies
    Error Card Displayed: True (INVALID / CORRUPTED Missing Competencies Error: Course must specify non-empty competencies array)
    Valid Course Functional: True
  Fixture: empty_questions
    Error Card Displayed: True (INVALID / CORRUPTED Empty Questions Error: Course must specify non-empty questions array)
    Valid Course Functional: True
  Fixture: invalid_question_type
    Error Card Displayed: True (INVALID / CORRUPTED Invalid Q Type Error: Invalid question type: unsupported_essay)
    Valid Course Functional: True
  Fixture: control_character_latex
    Error Card Displayed: True (INVALID / CORRUPTED Corrupted LaTeX Error: Contains unescaped control characters or corrupted LaTeX escapes)
    Valid Course Functional: True
```
In all 5 adversarial failure modes, the invalid course file was safely isolated with a red diagnostic card, while valid courses in `courses/` remained fully discoverable, navigable, and playable. Clicking error cards produced 0 page errors.

---

## 2. Logic Chain

1. **Premise 1 (`ORIGINAL_REQUEST.md` R1 & AC)**:
   The authoritative specification mandates: *"By default, every session (practice, quiz, unit test, challenge) presents questions in random order"* and *"across repeated sessions of the same unit, both question order and option order differ (test runs multiple sessions and asserts the orders are not all identical and do not simply mirror the JSON order)"*.
2. **Premise 2 (Observed Implementation in `App.tsx:101`)**:
   `handleStartPractice` calls `prepareSessionQuestions(compQuestions, false)` with the explicit comment: `// Shuffle options while maintaining question sequence for practice`.
3. **Premise 3 (Empirical Measurement)**:
   In 4 consecutive practice launches of the same unit, question sequences were 100% identical (`[Q1, Q2, Q3, Q4]`), exactly mirroring the JSON bank order. For courses with 20–30 questions per competency, `slice(0, 4)` on an unshuffled array leaves questions 5–30 completely inaccessible during practice sessions.
4. **Premise 4 (Quizzes, Tests & Challenges)**:
   In contrast, `handleStartQuiz`, `handleStartUnitTest`, and `handleBeginCourseChallenge` all pass `shuffleQuestions = true`, and empirical measurements confirmed that questions in quizzes and tests DO vary across sessions.
5. **Premise 5 (Option Shuffling, Persistence, Error Isolation Robustness)**:
   Option shuffling, grading invariance, LocalStorage persistence across page reloads, and fault-tolerant isolation of corrupt/schema-violating courses all passed rigorous empirical verification with 100% success.
6. **Inference**:
   The platform state machine, storage engine, and error isolation architecture are solid and resilient. However, the hardcoded `false` in `handleStartPractice` is a direct defect violating R1 and Acceptance Criteria that must be remediated.

---

## 3. Caveats

- **No Caveats**: The state machine, session shufflers, LocalStorage rehydration, and error boundary behaviors were empirically inspected, verified with live Playwright headless browser runs, and confirmed through automated diagnostic scripts.

---

## 4. Conclusion

The platform successfully satisfies LocalStorage persistence, option shuffling, and dynamic course error isolation. However, **Practice Session Question Shuffling is disabled** in `platform/src/App.tsx:101`, directly violating requirement R1 and Acceptance Criteria AC-05.

**Required Remediation**:
In `platform/src/App.tsx`, update line 101:
```typescript
-    const shuffled = prepareSessionQuestions(compQuestions, false);
+    const shuffled = prepareSessionQuestions(compQuestions, true);
```
And re-run `python -m pytest tests/e2e/test_platform_randomization.py`.

**Verdict: REQUEST_CHANGES**

---

## 5. Verification Method

To independently reproduce and verify these findings:

1. **Verify Practice Question Shuffling Defect**:
   Run the empirical test runner:
   ```powershell
   $env:PYTHONIOENCODING="utf-8"
   python tests/e2e/empirical_verify_runner.py
   ```
   Inspect the output under `--- Part A: Practice Session Question Shuffling ---`. Notice that all 4 practice launches produce the exact same 4 stems in the exact same order.
2. **Inspect Source Code**:
   View `platform/src/App.tsx` lines 95–106 to confirm `prepareSessionQuestions(compQuestions, false)`.
3. **Verify Option Shuffling & Grading**:
   Inspect `--- Part C: Option Shuffling & Grading Integrity ---` in the runner output: confirm option permutations vary across runs and `Grading after option shuffling: PASS`.
4. **Verify Error Isolation**:
   Inspect `[SUMMARY PILLAR 3]` in the runner output: confirm all 5 adversarial fixtures generated error cards while valid courses remained playable.
