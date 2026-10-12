# Technical Context — Generation 3

## Project State
- Project: Top's Academy
- Root: `g:\Mi unidad\Competence_analyser`
- Python environment: Python 3.12, Windows
- Key Components:
  1. Validator: `src/validator/` + `validator.cli` (Rule 1-16 including R2 length-giveaway checks).
  2. Platform: `platform/` (React, Vite, TypeScript, Tailwind, KaTeX, Lucide, MathQuill/Desmos/FunctionGrapher). Fast Redo and completed course tracking in `PracticeSession.tsx`, `CourseOverview.tsx`, `CourseLibrary.tsx`.
  3. Skill: `.agents/skills/content-to-course/` (`run.py`, `batch_generator.py`, `cta_analyzer.py`, `pdf_extractor.py`, `verifier.py`, `course_publisher.py`).
  4. Test Suites: Consolidated into `tests/test_validator.py`, `tests/test_skill.py`, `tests/test_platform.py`, `tests/e2e/`, `tests/test_blind_guess_empirical.py`.
  5. Courses: `courses/pde_course.json` (500 questions) and `courses/demo_course.json` (230 questions).

## The Blind-Guess Calibration Issue
- Acceptance Criterion:
  "Blind-guess test: an independent agent that is shown only the options (no stem, no solution, no hints) of >=40 randomly sampled multiple-choice items, shuffled, guesses the correct one in <=30% of them (chance is ~14%). Items it guessed correctly are reviewed for cues and rewritten if a cue is found; repeat until the threshold is met."
- Current Status:
  Initial rate was 78%. Gen 2 worker reduced it to 40.4% by fixing asymmetric padding, but needs one final calibration on distractor centroid clustering to reach <=30% (chance ~14.3% with 7 options).
- The solution requires calibrating how distractors are generated so options have homogeneous token overlap, vocabulary, and length distributions, preventing heuristic solvers from pinpointing the answer.
