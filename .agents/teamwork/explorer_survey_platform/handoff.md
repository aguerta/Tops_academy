# Handoff Report: Platform Math Equivalence Engine & Types Refactor (R7)

**Sender**: `explorer_survey_platform`  
**Recipient**: Parent Orchestrator (`8c6e51b9-04fd-4a8c-a9ab-21b3a1985725`)  
**Type**: Hard Handoff (Investigation & Specification Complete)  
**Date**: 2026-10-11T20:54:00Z  

---

## 1. Observation

1. **`platform/src/types.ts` (lines 51–58)**:
   ```typescript
   export interface FillBlankAnswer {
     expression: string;
     accepted_equivalents?: string[];
     tolerance?: number;
   }

   export type CorrectAnswer = string | string[] | FillBlankAnswer;
   ```
   Direct observation: `FillBlankAnswer` requires a mandatory `expression: string` field. It has no definition for `canonical_algebraic`, `value`, or `min_decimals`.

2. **Existing Course JSONs (`courses/pde_course.json` lines 339–347)**:
   ```json
   "correct_answer": {
     "value": "6",
     "canonical_algebraic": "6",
     "accepted_equivalents": [
       "6",
       "6.0",
       "1 + 5"
     ]
   }
   ```
   Direct observation: Courses omit `expression` and supply `canonical_algebraic` and `value`.

3. **`platform/src/utils/mathEquivalence.ts` (lines 109–112, 131–144)**:
   ```typescript
   const targetExpr = typeof targetAnswer === 'string' ? targetAnswer : targetAnswer.expression;
   ```
   ```typescript
   const tolerance = (typeof targetAnswer === 'object' && targetAnswer.tolerance) || 0.001;
   if (Math.abs(studentVal - targetVal) <= tolerance) {
     return true;
   }
   ```
   Direct observation:
   - When `targetAnswer` lacks `expression`, `targetExpr` evaluates to `undefined`, yielding `normTarget = ''`.
   - Default `tolerance` is hardcoded to `0.001` (coarse).
   - In `normalizeMathExpression`, decimal commas are not replaced before stripping spaces.

4. **Verbatim Error on Comma Input (`mathjs`)**:
   Command: `node -e "const math = require('./platform/node_modules/mathjs'); console.log(math.evaluate('0,8333'));"`
   Verbatim Output:
   ```text
   Unexpected operator , (char 2)
   ```
   Direct observation: Any input with a comma causes `mathjs` evaluation to crash and fail.

5. **`tests/test_platform.py` (lines 34–57)**:
   ```python
   NODE_SCRIPT = REPO_ROOT / "tests" / "test_math_adversarial_suite.mjs"
   RESULTS_PATH = REPO_ROOT / "tests" / "math_adversarial_results.json"
   ```
   Direct observation: Python runs `node tests/test_math_adversarial_suite.mjs` which reads the pre-bundled file. Current test suite passes 63/63 tests in `test_math_adversarial_suite.mjs` and 19/19 in `test_platform.py`.

---

## 2. Logic Chain

1. **Step 1 (From Observation 1 & 2)**:
   - Observation 2 proves that valid course answer objects specify `canonical_algebraic` and `value`, rather than `expression`.
   - Observation 1 proves that `FillBlankAnswer` in `platform/src/types.ts` does not type-check these properties.
   - Observation 3 proves that line 109 of `mathEquivalence.ts` only reads `.expression`, leaving `targetExpr` undefined when given legitimate course questions.
   - *Inference*: `types.ts` must be expanded to make `expression`, `canonical_algebraic`, and `value` optional fields, and `mathEquivalence.ts` must fall back across `expression -> canonical_algebraic -> value`.

2. **Step 2 (From Observation 4)**:
   - In Spanish course content (*Estadística III*), students input numerical answers using decimal commas (e.g. `0,8333`).
   - Observation 4 proves that `math.evaluate('0,8333')` crashes with `Unexpected operator , (char 2)` because mathjs interprets `,` as a delimiter, not a radix point.
   - *Inference*: `normalizeMathExpression` must normalize decimal commas into dots (`.`) prior to whitespace removal. To prevent breaking tuples/lists `(1, 2)` or arrays `[1, 2]`, the regex must require strictly adjacent digits without whitespace: `/(?<=\d),(?=\d)/g` and `/(^|[^0-9a-zA-Z_]),(?=\d+)/g`.

3. **Step 3 (From Observation 3 & R7 Requirements)**:
   - Requirement R7 mandates a 4-decimal tolerance threshold: $|v_{\text{student}} - v_{\text{target}}| \le 0.00005$ or explicit `tolerance`.
   - Observation 3 shows the existing default tolerance is $0.001$, which would allow answers that are incorrect at the 3rd and 4th decimal place (e.g. accepting $0.832$ when target is $0.8333$).
   - When target is a rounded decimal ($0.8333$) and student enters an exact fraction ($5/6 = 0.8333333...$), $|5/6 - 0.8333| = 0.00003333... \le 0.00005$. Both direct tolerance checking and 4-decimal rounded comparison ($round4(5/6) = 0.8333$) evaluate to true.
   - When student enters insufficient precision ($0.833$), $|0.833 - 0.8333| = 0.00033 > 0.00005$, rejecting the answer.
   - *Inference*: Default tolerance must be set to `0.00005`, and numerical evaluation must use `areNumericValuesEquivalent(studentVal, targetVal, tolerance)` supporting 4-decimal rounding and fraction equivalence.

4. **Step 4 (From Observation 5)**:
   - The project test runner executes compiled `.mjs` artifacts (`tests/dist/mathEquivalence_bundle.mjs` and `tests/test_math_adversarial_suite.mjs`).
   - *Inference*: After modifying `types.ts`, `mathEquivalence.ts`, and `test_math_adversarial_suite.ts`, the implementer must execute `esbuild` to re-bundle both `.mjs` files so that `python -m pytest tests/test_platform.py` executes the updated logic and passes.

---

## 3. Caveats

1. **Tuples and Coordinate Pairs**: As observed across all course files (`courses/pde_course.json`, fixtures), no current FIB questions expect tuple or list answers. However, the proposed regex `(?<=\d),(?=\d)` preserves tuples with whitespace `(1, 2)` and bracketed vectors `[1, 2]` safely.
2. **Read-only Investigation**: In accordance with the Explorer archetype and workflow protocol, no source files were modified during this investigation. All file edits are specified below for the subsequent implementation worker.

---

## 4. Conclusion

The refactor for R7 requires precise, localized modifications to three files plus re-bundling:
1. `platform/src/types.ts`: Update `FillBlankAnswer` to support `expression`, `canonical_algebraic`, `value`, `tolerance`, `min_decimals`.
2. `platform/src/utils/mathEquivalence.ts`:
   - Add decimal comma normalization in `normalizeMathExpression`.
   - Add target extraction fallback (`expression -> canonical_algebraic -> value`).
   - Implement `areNumericValuesEquivalent` with default tolerance `0.00005` (half-unit of 4th decimal place) and 4-decimal rounding.
3. `tests/test_math_adversarial_suite.ts`:
   - Append Category 7 (`DEC-01` to `DEC-18`) testing Spanish comma, fractions vs decimals, 4-decimal tolerance boundaries, higher precision, and p-values.
4. Build Bundles:
   - Run `esbuild` to update `tests/dist/mathEquivalence_bundle.mjs` and `tests/test_math_adversarial_suite.mjs`.

### Exact Code Specifications

#### File A: `platform/src/types.ts`
Replace lines 51–58 with:
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

#### File B: `platform/src/utils/mathEquivalence.ts`
1. In `normalizeMathExpression`, insert before line 48 (before implicit multiplication):
```typescript
  // Replace decimal comma (e.g. 0,8333 -> 0.8333, -2,7182 -> -2.7182)
  s = s.replace(/(?<=\d),(?=\d)/g, '.');
  s = s.replace(/(^|[^0-9a-zA-Z_]),(?=\d+)/g, '$10.');
```

2. Add extraction and comparison helpers:
```typescript
export function extractTargetExpression(targetAnswer: FillBlankAnswer | string | number): string {
  if (typeof targetAnswer === 'string') return targetAnswer;
  if (typeof targetAnswer === 'number') return String(targetAnswer);
  if (targetAnswer && typeof targetAnswer === 'object') {
    if (targetAnswer.expression !== undefined && targetAnswer.expression !== null && String(targetAnswer.expression).trim() !== '') {
      return String(targetAnswer.expression);
    }
    if (targetAnswer.canonical_algebraic !== undefined && targetAnswer.canonical_algebraic !== null && String(targetAnswer.canonical_algebraic).trim() !== '') {
      return String(targetAnswer.canonical_algebraic);
    }
    if (targetAnswer.value !== undefined && targetAnswer.value !== null && String(targetAnswer.value).trim() !== '') {
      return String(targetAnswer.value);
    }
  }
  return '';
}

export function areNumericValuesEquivalent(
  studentVal: number,
  targetVal: number,
  tolerance: number
): boolean {
  if (Math.abs(studentVal - targetVal) <= tolerance) {
    return true;
  }
  const round4 = (v: number) => Math.round(v * 10000) / 10000;
  const sRound = round4(studentVal);
  const tRound = round4(targetVal);

  if (Math.abs(sRound - tRound) <= 1e-9) {
    if (Math.abs(studentVal - tRound) <= tolerance || Math.abs(sRound - targetVal) <= tolerance) {
      return true;
    }
  }
  return false;
}
```

3. In `checkMathEquivalence`:
```typescript
  const targetExpr = extractTargetExpression(targetAnswer as any);
  const acceptedList = typeof targetAnswer === 'object' && (targetAnswer as any).accepted_equivalents
    ? (targetAnswer as any).accepted_equivalents
    : [];

  const defaultTolerance = 0.00005;
  const tolerance = (typeof targetAnswer === 'object' && (targetAnswer as any).tolerance !== undefined && (targetAnswer as any).tolerance !== null)
    ? (targetAnswer as any).tolerance
    : defaultTolerance;

  // Numeric evaluation
  try {
    const studentVal = math.evaluate(normStudent);
    const targetVal = math.evaluate(normTarget);
    if (
      typeof studentVal === 'number' &&
      typeof targetVal === 'number' &&
      !isNaN(studentVal) &&
      !isNaN(targetVal)
    ) {
      if (areNumericValuesEquivalent(studentVal, targetVal, tolerance)) {
        return true;
      }
    }
  } catch {}

  for (const alt of acceptedList) {
    try {
      const studentVal = math.evaluate(normStudent);
      const altVal = math.evaluate(normalizeMathExpression(alt));
      if (
        typeof studentVal === 'number' &&
        typeof altVal === 'number' &&
        !isNaN(studentVal) &&
        !isNaN(altVal) &&
        areNumericValuesEquivalent(studentVal, altVal, tolerance)
      ) {
        return true;
      }
    } catch {}
  }
```

---

## 5. Verification Method

To verify the implementation once applied:

1. **Re-bundle via esbuild**:
   ```powershell
   npx.cmd esbuild platform/src/utils/mathEquivalence.ts --bundle --format=esm --outfile=tests/dist/mathEquivalence_bundle.mjs
   npx.cmd esbuild tests/test_math_adversarial_suite.ts --bundle --format=esm --platform=node --outfile=tests/test_math_adversarial_suite.mjs
   ```
   *Expected outcome*: Both bundles generated cleanly without syntax or bundling errors.

2. **Execute Math Adversarial Suite**:
   ```powershell
   node tests/test_math_adversarial_suite.mjs
   ```
   *Expected outcome*: 81/81 test cases PASS (100% pass rate, 0 failed), output written to `tests/math_adversarial_results.json`.

3. **Execute Platform Pytest Suite**:
   ```powershell
   python -m pytest tests/test_platform.py -v
   ```
   *Expected outcome*: 19/19 passed in ~2.5 seconds.

4. **Frontend TypeScript & Production Build Verification**:
   ```powershell
   cd platform
   npm.cmd run build
   ```
   *Expected outcome*: `tsc` succeeds with 0 errors and `vite build` creates `platform/dist/`.
