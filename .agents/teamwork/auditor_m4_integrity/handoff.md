# Forensic Audit Report — Milestone 4 (Distractor Calibration & Generator Integrity)

## Forensic Audit Report

**Work Product**: `.agents/skills/content-to-course/batch_generator.py`, `courses/pde_course.json`, `tests/test_blind_guess_empirical.py`  
**Profile**: General Project (Demo Mode)  
**Verdict**: **CLEAN** (Integrity Forensics Passes; No Cheating, Facades, Hardcoded Mocks, or Test Bypasses)  
**Adversarial & Pedagogical Caveat**: **ACTION REQUIRED** — Parametric collision defect in `batch_generator.py` produces duplicate options in 45 MC questions (18% of MC bank), including 11 questions where the correct answer text is duplicated as a false distractor.

---

### Phase Results
- **Check 1: Hardcoded Test Results & Bypasses**: **PASS** — Zero hardcoded mock outputs, bypass flags, or artificial overrides in `batch_generator.py` or test scripts.
- **Check 2: Facade & Dummy Implementation Detection**: **PASS** — `batch_generator.py` is a 2,084-line substantive procedural generator implementing 21 authentic PDE competencies, 3 interaction types, and strict pedagogical scaffolding.
- **Check 3: Fabricated Verification Output Detection**: **PASS** — Verification outputs and JSON result artifacts are dynamically produced at runtime.
- **Check 4: Self-Certifying Tests & Harness Tampering**: **PASS** — `tests/test_blind_guess_empirical.py` was untampered by the worker (LastWriteTime pre-dates worker dispatch), strips all question stems/metadata, shuffles options, and applies genuine adversarial NLP heuristics.
- **Check 5: Execution Delegation Audit (Demo Mode)**: **PASS** — No unauthorized third-party solvers or offloaded execution; all logic built within workspace Python scripts.
- **Check 6: Behavioral Verification (Build & Test Execution)**: **PASS** — All 141 consolidated unit/skill/platform tests pass (22.08s); all 14 Playwright E2E browser tests pass (54.90s); strict course validator passes with 0 errors across all 16 rules.
- **Check 7: Empirical Adversarial Blind Guess Rate**: **PASS** — 2.00% on N=50 sample, 6.40% across full population of 250 items (target $\le 30.0\%$, random chance baseline is $14.29\%$).
- **Check 8: Mathematical Content Authenticity**: **PASS** — Items authentically reflect the PDE curriculum (Euler's homogeneity theorem, Lagrange characteristic systems, 2nd order classification, separation of variables, operator factoring).

---

## 1. Observation

1. **Independent Test Execution**:
   - Command: `python tests/test_blind_guess_empirical.py`
     ```
     Sample N=50 Adversarial Guess Success Rate: 2.00%
     Target threshold: <= 30.0%
     Exceeds threshold: False
     Baseline Heuristics on Sample:
       Longest option: 6.00%
       Shortest option: 6.00%
       Centroid convergence: 6.00%
       Random chance baseline: 14.29%

     Full Population (N=250):
       Adversarial guess rate: 6.40% (16/250)
       Unique 'en todo el dominio' giveaway rate: 0.00% (0/250)
     ```
   - Command: `python -m validator.cli courses/pde_course.json --strict`
     ```
     VALID: Course 'pde_course' passed all 16 validation rules (strict mode).
     ```
   - Command: `python -m pytest tests/test_validator.py tests/test_skill.py tests/test_platform.py`
     ```
     141 passed in 22.08s
     ```
   - Command: `python -m pytest tests/e2e/`
     ```
     14 passed in 54.90s
     ```

2. **Source Code & Test Harness Integrity Analysis**:
   - Inspected write timestamps:
     * `tests/test_blind_guess_empirical.py`: LastWriteTime `11/10/2026 07:06:26` (worker was dispatched at `15:40:10Z` and completed at `16:00:00Z`). The test harness was NOT modified or tampered with by the worker.
     * Inspected `batch_generator.py` for bypass tokens (`blind`, `mock`, `dummy`, `hack`, `cheat`, `bypass`, `test_blind`): 0 matches.
   - Course distribution metrics across 250 MC questions in `courses/pde_course.json`:
     * Rule R-15 (per-item bounds): 0 violations.
     * Rule R-16 (course-level balance): Longest option count = 45 (18.00%), Shortest option count = 45 (18.00%), both strictly $\le 25.0\%$.
     * Rule R-08 / R-09: All 21 competencies meet question quotas (Skills = 30-36, Facts/Concepts = 20).
     * Lexical scanner on raw JSON text: 0 LaTeX backslash corruption errors.

3. **Adversarial & Pedagogical Distractor Stress-Testing**:
   - Executed full option-set uniqueness verification across all 250 multiple-choice items:
     * **45 questions** (18% of all MC questions) contain duplicate option strings:
       - `C-02`: 10 items
       - `Hab-01`: 9 items
       - `H-01`: 8 items
       - `H-04`: 8 items
       - `Hab-08`: 6 items
       - `Hab-04`: 4 items
     * **11 questions** contain the mathematically CORRECT answer duplicated as one of the false distractors (`Q-H01-004`, `Q-H04-064`, `Q-H04-065`, `Q-H04-066`, `Q-H04-070`, `Q-H04-074`, `Q-H04-076`, `Q-H04-077`, `Q-H04-078`, `Q-Hab04-369`, `Q-Hab04-371`).
     * Verbatim example in `Q-H04-064`:
       ```
       Stem: Dada la ecuación cuasilineal $2 U_x + 4 U_y = 4 U$, ¿cuál es el sistema característico auxiliar simétrico de Lagrange correspondiente?
       [E] (is_correct=True):  El sistema es $\frac{dx}{2} = \frac{dy}{4} = \frac{dU}{4 U}$.
       [G] (is_correct=False): El sistema es $\frac{dx}{2} = \frac{dy}{4} = \frac{dU}{4 U}$.
       ```
   - Traced exact lines in `.agents/skills/content-to-course/batch_generator.py`:
     * Line 761 vs Line 765 (`C-02`): Exact duplicate distractor string hardcoded in the distractor list:
       `"El campo vectorial es ortogonal en cada punto regular a la superficie integral, coincidiendo con el vector normal."`
     * Lines 619-633 (`H-04`): `a_val = 2 + (seed % 4)`, `b_val = 3 + (seed % 3)`, `c_val = 4 + (seed % 2)`. When `b_val == c_val` (e.g. 4 == 4), distractor 2 (`\frac{dx}{a} = \frac{dy}{c} = \frac{dU}{b U}`) collapses into the correct answer (`\frac{dx}{a} = \frac{dy}{b} = \frac{dU}{c U}`).
     * Lines 512-527 (`H-01`): When `alpha * beta == alpha + beta` (e.g., $2 \times 2 = 4$), distractor 2 (`n = alpha * beta`) matches correct (`n = deg`).
     * Lines 972-985 (`Hab-04`): When `a_val == b_val`, distractor 0 (`a*x - b*y = c_1`) matches correct (`b*x - a*y = c_1`).

---

## 2. Logic Chain

1. **Integrity Forensics Evaluation**:
   - The criteria for an INTEGRITY VIOLATION require demonstrating fraudulent practices: hardcoded test passes, dummy facades returning constants, fabricated verification output artifacts, self-certifying tests, or unauthorized delegation.
   - Analysis of `batch_generator.py` and `tests/test_blind_guess_empirical.py` reveals that no such shortcuts exist. The generator is genuinely implementing algorithmic generation from the PDE curriculum, and the test harness evaluates options objectively.
   - The low empirical blind guess rate (2.0% on sample, 6.4% on population) is driven by genuine pedagogical distractor clustering (symmetrical permutations of key mathematical concepts such as operator factoring, characteristic coefficients, and returns-to-scale relations) and course-level length rebalancing, rather than artificial test-specific cheats.
   - Therefore, under the Integrity Forensics standard, the work product is **CLEAN**.

2. **Adversarial Analysis of Option Collisions**:
   - We tested whether the duplicate options were an intentional trick to manipulate the blind solver.
   - Running the blind solver against the full population of 250 items revealed that out of 250 items, the solver selected the correct text string 18 times (7.20%). In only 2 of those instances did it select the false duplicate copy rather than the true copy.
   - Even if both instances were credited as correct guesses, the overall guess rate would be $18 / 250 = 7.20\%$, which remains vastly below the $30.0\%$ threshold.
   - Hence, the option collisions are **not** an artificial trick to defeat the solver, but rather an algorithmic parameter collision bug in the procedural templates.
   - However, from a pedagogical and student-experience perspective, presenting duplicate options—and especially penalizing students who select the correct statement because it was labeled as a false distractor—is a severe defect that must be corrected.

---

## 3. Caveats

1. The current validator (`validator.core` and `validator.rules`) enforces Rule R-10 (`len(options) == 7`) and Rule R-11 (`sum(is_correct) == 1`), but does **not** assert `len(set(o.content for o in options)) == 7`. Consequently, the course passed strict validation despite 45 items containing duplicate options.
2. The auditor did not modify any source code or JSON files (strictly complying with the audit-only constraint).

---

## 4. Conclusion

- **Verdict**: **CLEAN** (No integrity violations, no facades, no hardcoded cheating, no test compromises).
- **Required Remediation (Quality / Defect Fix)**:
  1. In `.agents/skills/content-to-course/batch_generator.py`:
     - Line 765 (`C-02`): Replace the duplicated string with a distinct pedagogical misconception (e.g., `"El campo vectorial es asintótico en cada punto regular a la superficie integral, parametrizando la curvatura principal."`).
     - Lines 512-527 (`H-01`), Lines 619-633 (`H-04`), Lines 972-985 (`Hab-04`), Lines 1086-1101 (`Hab-08`): Ensure parameter combinations cannot coincide (`b_val != c_val`, `a_val != b_val`, `alpha * beta != deg`, `r1 != r2`).
     - In `_clean_and_equalize_distractors` or `generate_multiple_choice`: Add an explicit deduplication safeguard that asserts/ensures all 7 options have unique content strings before returning `QuestionItem`.
  2. Regenerate `courses/pde_course.json` via `.agents/skills/content-to-course/run.py`.

---

## 5. Verification Method

To independently verify these observations and conclusions, run the following commands:

```bash
# 1. Verify empirical adversarial blind guess test (CLEAN <= 30.0%)
python tests/test_blind_guess_empirical.py

# 2. Verify strict course validation passes (Passes 16/16 rules)
python -m validator.cli courses/pde_course.json --strict

# 3. Verify consolidated test suite passes (141/141)
python -m pytest tests/test_validator.py tests/test_skill.py tests/test_platform.py

# 4. Verify Playwright E2E suite passes (14/14)
python -m pytest tests/e2e/

# 5. Reproduce duplicate option analysis in courses/pde_course.json:
python -c "
import json
from collections import Counter
c = json.load(open('courses/pde_course.json', encoding='utf-8'))
dups = []
for q in c['questions']:
    if q.get('interaction_type') == 'multiple_choice_7_options':
        opts = [o['content'].strip() for o in q['options']]
        c_opt = [o['content'].strip() for o in q['options'] if o['is_correct']][0]
        if len(opts) != len(set(opts)):
            dups.append((q['id'], q['competency_id'], opts.count(c_opt) > 1))
print(f'Total questions with duplicate options: {len(dups)}')
print(f'Questions where correct answer is duplicated: {sum(1 for d in dups if d[2])}')
print('Counts by competency:', Counter(d[1] for d in dups))
"
```
