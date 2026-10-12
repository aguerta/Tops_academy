## 2026-10-11T05:51:43Z

You are an adversarial Challenger (challenger_m2_math) testing the client-side math equivalence engine and grading accuracy of the practice platform.

Your Working Directory: g:\Mi unidad\Competence_analyser\.agents\teamwork\challenger_m2_math
Project Root: g:\Mi unidad\Competence_analyser
Authoritative Specifications:
- g:\Mi unidad\Competence_analyser\.agents\teamwork\ORIGINAL_REQUEST.md
- g:\Mi unidad\Competence_analyser\PROJECT.md
- Source code: `platform/src/utils/mathEquivalence.ts` (or math grading module under `platform/src/`)

Your Tasks:
1. Read ORIGINAL_REQUEST.md and locate the math equivalence grading implementation in `platform/src/`.
2. Empirically challenge the math engine with adversarial test suites:
   - Algebraic equivalence: e.g. `1 - (alpha + n)*sigma` vs `1 - alpha*sigma - n*sigma`, `-(x - 3)` vs `3 - x`.
   - Number equivalence: `0.5` vs `1/2`, `2/4`, `0.500`.
   - Fractions and powers: `x^{2}`, `x^2`, `\frac{1}{2}`, `1/2`.
   - Commutativity, spaces, Greek letters (`\alpha`, `\beta`, `\sigma`, `\pi`).
   - Non-equivalent expressions: ensure false positives do NOT occur (`x+1` vs `x-1`, `2x` vs `3x`).
   - Boundary/malformed inputs: empty strings, division by zero, invalid LaTeX syntax.
3. Run tests using Node or Python test runner to verify behavior against the actual implementation.
4. Document all test cases, outcomes, and edge-case evaluations in `g:\Mi unidad\Competence_analyser\.agents\teamwork\challenger_m2_math\handoff.md`.
5. Provide a clear verdict in `handoff.md`:
   - Must explicitly conclude with either: `Verdict: APPROVE` or `Verdict: REQUEST_CHANGES`.
6. Send a completion message back to the orchestrator (conversation ID: 7609f41d-901b-455e-a8d4-9ddd5b18b728).
