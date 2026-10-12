## 2026-10-11T12:10:32Z

You are a Worker (worker_m4_blind_guess_fix) remediating the critical blind-guess distractor giveaways discovered by challenger_m4_blind_guess in `courses/pde_course.json` and `.agents/skills/content-to-course/batch_generator.py`.

Your Working Directory: g:\Mi unidad\Competence_analyser\.agents\teamwork\worker_m4_blind_guess_fix
Project Root: g:\Mi unidad\Competence_analyser
Authoritative Specifications & Reports:
- g:\Mi unidad\Competence_analyser\.agents\teamwork\ORIGINAL_REQUEST.md
- g:\Mi unidad\Competence_analyser\PROJECT.md
- Challenger Report: g:\Mi unidad\Competence_analyser\.agents\teamwork\challenger_m4_blind_guess\handoff.md
- Test Harness: `tests/test_blind_guess_empirical.py`

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A forensic auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Context of Challenger Finding:
In `challenger_m4_blind_guess/handoff.md`, the adversarial agent achieved a 78.00% blind-guess success rate (target <= 30.0%) due to two specific flaws:
1. In `.agents/skills/content-to-course/batch_generator.py` around lines 401-408:
   ```python
   if len_c <= min_d:
       c_clean = _append_phrase(c_clean, ", en todo el dominio.")
   if len_c >= max_d:
       longest_idx = d_lens.index(max_d)
       d_clean[longest_idx] = _append_phrase(d_clean[longest_idx], ", en todo el plano.")
   ```
   `", en todo el dominio."` was mechanically appended ONLY to `c_clean`, and never to distractors. This single giveaway leaked the correct answer in 107 out of 250 MC7 items (42.8%)!
2. In `Hab-02` (and similar candidate solution verification generators):
   Correct options ended with `= 0` (e.g. `dando 3 U - 3(U) = 0`), while distractors ended with `\neq 0` (e.g. `dando 23 U \neq 0`). The options themselves gave away the solution without solving.

Tasks to Implement:
1. Fix `.agents/skills/content-to-course/batch_generator.py`:
   - Eliminate lines 403-408 asymmetric padding. Ensure distractor balancing operates symmetrically across all options:
     If padding phrases are needed to maintain length bounds, select padding phrases from a shared, symmetric pool that applies uniformly to both correct answers and distractors, without reserving any phrase exclusively for correct answers or distractors.
   - In `Hab-02` (and any other verification MC generators):
     Format options neutrally without evaluating the equation inside the option text itself. For example:
     - Correct option: `La función $U(x,y) = e^{3 x + y}$, al satisfacer la relación característica del operador.`
     - Distractors: `La función $U(x,y) = e^{x + 3 y}$, al invertir los coeficientes característicos del operador.`
     Ensure distractors and correct options have homogeneous syntactic structure, grammatical form, and length, with zero evaluation leaks (`= 0` vs `\neq 0`).
2. Regenerate `courses/pde_course.json`:
   ```bash
   python .agents/skills/content-to-course/run.py --pdf sample_content/I__Ecuaciones_en_derivadas_parciales_2026.pdf --output-dir courses --course-id pde_course --audit-sample 10
   ```
   Validate with:
   ```bash
   python -m validator.cli courses/pde_course.json --strict
   ```
   Must pass all 16 rules with exit code 0.
3. Run Empirical Blind-Guess Test:
   ```bash
   python tests/test_blind_guess_empirical.py
   ```
   Verify that the adversarial blind-guess success rate drops strictly below the mandated 30.0% ceiling (expected ~14% to 25%).
4. Document all line diffs, generator changes, validator output, and verbatim blind-guess test results in `g:\Mi unidad\Competence_analyser\.agents\teamwork\worker_m4_blind_guess_fix\handoff.md`.
5. Send completion message back to the orchestrator (conversation ID: 7609f41d-901b-455e-a8d4-9ddd5b18b728).
