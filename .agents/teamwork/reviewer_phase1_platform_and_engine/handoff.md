# Review & Adversarial Challenge Report: Phase 1 Platform & Engine (R1, R3, R7)

**Reviewer / Adversarial Critic**: `reviewer_phase1_platform_and_engine`  
**Parent Orchestrator**: `8c6e51b9-04fd-4a8c-a9ab-21b3a1985725`  
**Date**: 2026-10-11T21:44:30Z  
**Gate Verdict**: **APPROVE**  
**Overall Risk Assessment**: LOW  

---

## 1. Observation

### 1.1 Platform Refactor (R7) Inspection
- **`platform/src/types.ts` (lines 55–65)**:
  `FillBlankAnswer` declared with optional fields:
  ```typescript
  export interface FillBlankAnswer {
    expression?: string;
    canonical_algebraic?: string;
    value?: string | number;
    accepted_equivalents?: string[];
    tolerance?: number;
    min_decimals?: number;
  }
  export type CorrectAnswer = string | number | string[] | FillBlankAnswer;
  ```
- **`platform/src/utils/mathEquivalence.ts` (lines 48–51, 99–114, 116–134, 150–160)**:
  - Comma normalization:
    ```typescript
    s = s.replace(/(?<=\d),(?=\d)/g, '.');
    s = s.replace(/(^|[^0-9a-zA-Z_]),(?=\d+)/g, '$10.');
    ```
  - Target expression fallback:
    Resolves `expression` -> `canonical_algebraic` -> `value` safely handling null, undefined, empty strings, and numeric zeros.
  - 4-decimal tolerance & fraction equivalence:
    `defaultTolerance = 0.00005` (half-unit of 4th decimal place).
    `areNumericValuesEquivalent(studentVal, targetVal, tolerance)` evaluates raw difference $\le$ tolerance or rounded 4th-decimal equivalence within tolerance.
  - Direct evaluate, symbolic simplification (`math.simplify`), and Monte Carlo parameter sampling are preserved for algebraic expressions.

### 1.2 Generic Parametric Engine & Schemas (R1, R3) Inspection
- **`.agents/skills/content-to-course/engine/`**:
  - `sandbox.py`: AST validation enforcing whitelist (`math`, `fractions`, `statistics`, `sympy`, `numpy`, `scipy`, `random`, `decimal`, `engine`). Blocks dangerous names (`open`, `eval`, `exec`, `compile`, `__import__`, `os`, `sys`, `subprocess`, `socket`, `pathlib`, `io`, etc.) and all dunder attributes (`attr.startswith('__')` and `id.startswith('__') and id.endswith('__')`). Enforces 2.0s subprocess timeout.
  - `render.py`: Formats KaTeX `bmatrix` (`\begin{bmatrix} ... \end{bmatrix}`), `table_array` (`\begin{array}{...} ... \end{array}`), `fmt` (up to 4 decimals), and `latex_frac`.
  - `invariants.py`: Evaluates 100% of generated instances for single correct answer, distinct distractors (TPL-D4), non-empty answers, MS bounds ($1 \le \text{correct} \le n-1$), hints (3-5), and anti-giveaway length ratios ($0.80 \times \min(D) \le \text{len}(C) \le 1.20 \times \max(D)$).
  - `diversity.py`: Masks numbers, fractions, matrices, and computes `unique(masked_stems) / total >= 0.5`.
  - `assemble.py`: Shuffles options A-G, associates misconception warnings from CTA distractor `remediation_hint`, and checks course-wide giveaway distribution ($\le 25\%$ longest, $\le 25\%$ shortest).
  - `instantiate.py`: Enforces quotas ($\ge 30$ Skill, $\ge 20$ Fact/Concept), sweeps seeds deterministically, and deduplicates parameter tuples and rendered stems.
- **Zero Domain Keywords**:
  Ripgrep query `edo|pde|derivadas|jacobiana|eigen|euler|cobb_douglas|lotka|lagrange` and `regresi` in `.agents/skills/content-to-course/engine/` returned **0 matches**. The engine contains zero hardcoded subject logic.
- **Schemas in `.agents/skills/content-to-course/schemas/`**:
  - `pages.schema.json`: Valid Draft-07 schema for manifest items and tiling.
  - `cta.schema.json`: Valid Draft-07 schema for Knowledge Triad, Bloom levels, and fused distractors.
  - `template.schema.json`: Valid Draft-07 schema for parametric templates (`generate_py`, `cross_check_py`, hints, solution).

### 1.3 Independent Execution Results
1. `node tests/test_math_adversarial_suite.mjs`:
   `SUMMARY: 81/81 Passed, 0 Failed` (exit code 0).
2. `python -m pytest tests/test_platform.py -v`:
   `19 passed in 2.48s` (exit code 0).
3. `npm.cmd --prefix platform run build`:
   `tsc` 0 errors, Vite production build succeeded in 17.71s (exit code 0).
4. `python -m pytest tests/test_validator.py -v`:
   `95 passed in 13.40s` (exit code 0).
5. `python .agents/teamwork/worker_m1b_engine/test_engine_full.py`:
   `ALL VERIFICATION SUITE TESTS PASSED SUCCESSFULLY!` (exit code 0).
6. `python -m pytest tests/test_skill.py -v`:
   `32 passed in 53.36s` (exit code 0).
7. `python -m validator.cli courses/pde_course.json --strict`:
   `VALID: Course 'pde_course' passed all 16 validation rules (strict mode)` (exit code 0).
8. `python -m validator.cli courses/sistemas_edos.json --strict`:
   `VALID: Course 'sistemas_edos' passed all 16 validation rules (strict mode)` (exit code 0).

---

## 2. Logic Chain

1. **Step 1 (Integrity Audit)**:
   Source code review confirms that neither `platform/src/utils/mathEquivalence.ts` nor `.agents/skills/content-to-course/engine/` contains hardcoded test outputs, facade/dummy logic, or synthetic bypasses. The math engine genuinely parses and evaluates inputs via `mathjs`, AST analysis, and numerical algorithms. No integrity violations exist.
2. **Step 2 (Platform R7 Equivalence Robustness)**:
   Observation of lines 48–51 and 116–134 in `mathEquivalence.ts` and test execution of `DEC-01` through `DEC-18` show that decimal commas (`0,8333` vs `0.8333`), fraction-to-decimal comparisons (`5/6` vs `0.8333`), higher-precision entries (`0.833333`), and fallback resolution (`canonical_algebraic`, `value`) evaluate as mathematically equivalent, while invalid precision (`0.833`, `0.8334`) and incorrect p-values (`0.0031` vs `0.0030`) are consistently rejected.
3. **Step 3 (Sandbox Security & AST Enforcement)**:
   `sandbox.py` combines static AST validation with isolated subprocess execution and 2.0s timeouts. Prohibiting all dunder attributes (`__`), dangerous builtins, and unwhitelisted root modules successfully thwarts breakout attempts (verified by tests in `TestSandboxSecurity`).
4. **Step 4 (Anti-Overfitting & Architecture Generalization)**:
   The zero-keyword audit confirms the generic parametric engine is completely agnostic to subject domain. It generates questions strictly from generic template definitions without domain-specific branches.
5. **Step 5 (Full Regression Protection)**:
   All legacy courses (`pde_course.json`, `sistemas_edos.json`) continue passing strict validation. Platform builds and all test suites pass with a 100% success rate.

---

## 3. Adversarial Stress-Test Findings

| Challenge ID | Target Subsystem | Stress Scenario / Hypothesis | Predicted / Actual Outcome | Verdict |
|---|---|---|---|---|
| **ADV-01** | AST Sandbox | Attacker attempts sandbox escape using `().__class__.__bases__[0].__subclasses__()` | AST validator flags dunder attribute access `__class__` and raises `SecurityViolationError` before execution. | PASS (Blocked) |
| **ADV-02** | AST Sandbox | Malicious template attempts infinite loop (`while True: pass`) | Worker process killed by OS subprocess timeout after 2.0s, raising `SandboxTimeoutError`. | PASS (Blocked) |
| **ADV-03** | Math Equivalence | Student inputs Spanish decimal with leading comma (`",5"`) or expression (`"1 + 0,5"`) | RegEx replaces leading and digit-adjacent commas; evaluates to `0.5` and `1.5`, matching target. | PASS (Accepted) |
| **ADV-04** | Math Equivalence | Boundary error: student inputs imprecise value (`"0.833"` or `"0.8334"` for `"0.8333"`) | Tolerance of $0.00005$ strictly rejects differences of $0.00033$ and $0.00010$. | PASS (Rejected) |
| **ADV-05** | Math Equivalence | Student introduces alien variable (`x + alien` vs `x`) | Extracted variables detect alien variable; Monte Carlo returns `false`. | PASS (Rejected) |
| **ADV-06** | Engine Assembly | MC7 correct option is disproportionately long compared to distractors | `check_instance_invariants` enforces $0.80 \times \min(D) \le \text{len}(C) \le 1.20 \times \max(D)$; rejects offending instance. | PASS (Enforced) |
| **ADV-07** | Engine Diversity | Template generates repetitive stems with only numbers altered | `diversity.py` masks numbers and enforces `unique(masked) / total >= 0.5`. | PASS (Enforced) |

---

## 4. Caveats

- **No Caveats**: All code was inspected directly in repository files, all tests were independently executed in the environment, and all assertions were verified against the authoritative specifications in `ORIGINAL_REQUEST.md` (R1, R3, R7).

---

## 5. Conclusion

The implementation of Milestone 1 / Phase 1 by workers `worker_m1a_platform` and `worker_m1b_engine` satisfies all requirements:
- **Zero Integrity Violations**: No hardcoded test responses, facades, or cheated verifications.
- **Platform R7 Fully Operational**: Comma normalization, fallback target extraction, 4-decimal tolerance ($0.00005$), and fraction equivalence pass 100% of tests.
- **Engine R1 & R3 Fully Operational**: AST sandbox security, KaTeX renderers, invariants, diversity, assembly, and schemas are complete with zero domain keywords.
- **Zero Regressions**: 81/81 math adversarial tests, 19/19 platform tests, 95/95 validator tests, 32/32 skill tests, and Vite production build pass without error.
- **Gate Verdict**: **APPROVE**. Phase 1 code is ready to freeze for Phase 2 course generation.

---

## 6. Verification Method

To independently reproduce this verification:

1. **Math Adversarial Suite**:
   ```powershell
   node tests/test_math_adversarial_suite.mjs
   ```
   *Expected outcome*: `SUMMARY: 81/81 Passed, 0 Failed` (exit code 0).

2. **Platform Pytest Suite**:
   ```powershell
   python -m pytest tests/test_platform.py -v
   ```
   *Expected outcome*: `19 passed` (exit code 0).

3. **Platform TypeScript & Vite Production Build**:
   ```powershell
   npm.cmd --prefix platform run build
   ```
   *Expected outcome*: `tsc` and `vite build` complete with exit code 0.

4. **Validator & Skill Regression Suites**:
   ```powershell
   python -m pytest tests/test_validator.py tests/test_skill.py -v
   ```
   *Expected outcome*: `127 passed` (exit code 0).

5. **Existing Courses Strict Validation**:
   ```powershell
   python -m validator.cli courses/pde_course.json --strict
   python -m validator.cli courses/sistemas_edos.json --strict
   ```
   *Expected outcome*: `VALID: Course '...' passed all 16 validation rules (strict mode)` (exit code 0).
