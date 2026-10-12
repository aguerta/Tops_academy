# DISPATCH — challenger_m4_blind_guess

## Mission
Conduct an adversarial blind-guess distractor test on a random sample of at least 40 multiple-choice questions from `courses/pde_course.json`.
Only the options are evaluated (stems, solutions, and hints stripped and options shuffled).
Verify that guessing the correct answer from bare options alone achieves <=30% accuracy (chance is ~14%).
Document all tested items, guesses, rationales, and results.


## 2026-10-11T11:59:54Z
You are an adversarial Challenger (challenger_m4_blind_guess) testing the anti-giveaway guarantees of the official PDE course deliverable (`courses/pde_course.json`).

Your Working Directory: g:\Mi unidad\Competence_analyser\.agents\teamwork\challenger_m4_blind_guess
Project Root: g:\Mi unidad\Competence_analyser
Authoritative Specifications:
- g:\Mi unidad\Competence_analyser\.agents\teamwork\ORIGINAL_REQUEST.md
- g:\Mi unidad\Competence_analyser\PROJECT.md
- Course File: `courses/pde_course.json`

Context & Acceptance Criteria:
"Blind-guess test: an independent agent that is shown only the options (no stem, no solution, no hints) of >=40 randomly sampled multiple-choice items, shuffled, guesses the correct one in <=30% of them (chance is ~14%). Items it guessed correctly are reviewed for cues and rewritten if a cue is found; repeat until the threshold is met."

Your Tasks:
1. Load `courses/pde_course.json` and extract at least 40 multiple-choice questions (`multiple_choice_7_options`).
2. For each question:
   - Completely strip the question stem, context, hints, solution, and misconception warning.
   - Shuffle the 7 options so their position is randomized.
   - Act as an adversarial student attempting to guess the correct answer purely by inspecting option text:
     * Look for giveaways: longest option, shortest option, asymmetric justification, grammatical tells, qualifier cues (always, never), unique mathematical formatting.
     * Record your blind guess option.
   - Reveal the true answer key and record whether your blind guess was correct.
3. Compute the overall blind-guess success rate:
   - Target: <=30.0% (random baseline is 1/7 = 14.3%).
4. For any item guessed correctly, analyze whether it was a lucky guess or if an actual cue/giveaway existed.
5. Document the full test protocol, list of 40+ questions, options, guesses, outcomes, and cue analysis in `g:\Mi unidad\Competence_analyser\.agents\teamwork\challenger_m4_blind_guess\handoff.md`.
6. Provide an explicit verdict in `handoff.md`:
   - Conclude with `Verdict: APPROVE (guess rate = X%)` or `Verdict: REQUEST_CHANGES`.
7. Send a completion message back to the orchestrator (conversation ID: 7609f41d-901b-455e-a8d4-9ddd5b18b728).
