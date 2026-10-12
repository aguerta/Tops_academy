# Technical Analysis: Platform Math Equivalence Engine & Types Refactor (R7)

**Agent**: `explorer_survey_platform`  
**Date**: 2026-10-11  
**Target Milestone**: content-to-course v2 (R7 Platform Math Equivalence Refactor)  
**Parent Orchestrator**: `8c6e51b9-04fd-4a8c-a9ab-21b3a1985725`

---

## Executive Summary

This investigation analyzed the platform's mathematical equivalence engine (`platform/src/utils/mathEquivalence.ts`), type definitions (`platform/src/types.ts`), UI components (`PracticeSession.tsx`, `QuestionCard.tsx`), and the adversarial test harness (`tests/test_math_adversarial_suite.ts`, `tests/test_platform.py`).

The existing system correctly handles algebraic normalization and basic number equivalence, but exhibits four critical limitations preventing successful grading of numerical Fill-In-The-Blank (FIB) exercises in courses like *Estadística III* and *EDP/EDO*:
1. **Target Object Schema Incompatibility**: `checkMathEquivalence` extracts target expressions solely via `targetAnswer.expression`. In contrast, existing courses (e.g. `pde_course.json:340`) and generator pipelines provide answers keyed as `canonical_algebraic` or `value`. If `expression` is omitted, `targetExpr` becomes `undefined` (`normTarget = ''`), silently failing numerical comparisons.
2. **Crash on Spanish/European Decimal Comma**: Inputs such as `0,8333` cause `mathjs` to crash with `Unexpected operator , (char 2)` because mathjs treats commas as syntax operators (matrix/argument separators), not decimal separators.
3. **Overly Coarse Default Tolerance**: The engine hardcodes `tolerance = 0.001`, which fails to enforce the required 4-decimal place precision threshold ($\pm 0.00005$), while lacking structured comparison between equivalent fractions (e.g., $5/6$) and rounded 4-decimal representations ($0.8333$).
4. **Bundle Drift**: The test runner in Python (`tests/test_platform.py`) executes pre-compiled ESM bundle `tests/test_math_adversarial_suite.mjs`. Changes to `mathEquivalence.ts` or `test_math_adversarial_suite.ts` require re-bundling via `esbuild`.

Below are the detailed technical findings and the exact proposed implementation specification.

---

## 1. Type System Investigation (`platform/src/types.ts`)

### Current State
In `platform/src/types.ts` (lines 51–58):
```typescript
export interface FillBlankAnswer {
  expression: string;
  accepted_equivalents?: string[];
  tolerance?: number;
}

export type CorrectAnswer = string | string[] | FillBlankAnswer;
```

### Analysis of Gaps
1. **Field naming discrepancy**:
   - In `courses/pde_course.json` (lines 339–347):
     ```json
     "correct_answer": {
       "value": "6",
       "canonical_algebraic": "6",
       "accepted_equivalents": ["6", "6.0", "1 + 5"]
     }
     ```
   - In `src/validator/rules.py` (lines 209–220): The validator accepts dicts containing `value` or `expression`.
   - In the v2 design spec for *Estadística III* (`implementation_plan.md` Component 8): The course generator emits `canonical_algebraic` or `value` with optional `tolerance` and `min_decimals`.
   - `FillBlankAnswer` in `types.ts` requires `expression: string`, making objects containing only `canonical_algebraic` or `value` violate the TypeScript interface.
2. **Missing `min_decimals`**:
   - Plantillas that require minimum decimal precision (e.g. 4 decimals for p-values, t-statistics) need a declaration field in the interface.
3. **Primitive numbers in `value` and `CorrectAnswer`**:
   - `value` can be numeric (`value: 0.25`) or string (`value: "0.25"`).
   - `CorrectAnswer` should accept `number` as well as string/arrays/object.

### Proposed Interface Definition
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

---

## 2. Target Extraction & Math Engine (`platform/src/utils/mathEquivalence.ts`)

### Current Extraction Mechanism
In `mathEquivalence.ts` (line 109):
```typescript
const targetExpr = typeof targetAnswer === 'string' ? targetAnswer : targetAnswer.expression;
```
If `targetAnswer` is `{ canonical_algebraic: "0.8333", value: "0.8333" }`, `targetExpr` evaluates to `undefined`. `normalizeMathExpression(undefined)` returns `''`. Direct match fails, numeric evaluation fails, and only `accepted_equivalents` can save it.

### Proposed Extraction Helper
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
```

---

## 3. Decimal Comma Normalization Without Breaking Lists/Tuples

### Problem Statement
In Spanish and European mathematics, decimal numbers are written with a comma: `0,8333`, `-2,7182`, `459,75`. However, mathjs throws an unhandled syntax error when evaluating `0,8333`.
At the same time, normalization must not corrupt tuples, coordinate pairs, or lists such as `(1, 2)`, `[1, 2, 3]`, or function arguments `f(x, y)`.

### Lexical & Semantic Analysis
1. **Decimal Comma Syntax**:
   - A decimal comma is **strictly adjacent to digits on both sides** with no whitespace: `\d+,\d+` (e.g. `0,8333`, `12,5`).
   - Or a leading comma before digits: `(^|[^\w\d]),\d+` (e.g. `,5` or `-,5`).
2. **Tuple / List / Function Argument Syntax**:
   - In standard mathematical and programming notation, tuples, coordinate pairs, lists, and function arguments place whitespace after the comma: `(1, 2)`, `[1, 2, 3]`, `f(x, y)`.
   - In lists with decimal elements: `[0,5, 0,8]`, the element separator is followed by space `, `, whereas the decimal comma has no space `0,5`.
3. **Execution Placement**:
   - Decimal comma normalization MUST occur in `normalizeMathExpression` **before** line 90 (`s = s.replace(/\s+/g, '')`).

### Normalization Implementation
```typescript
// Replace decimal comma (e.g. '0,8333' -> '0.8333', '-2,7182' -> '-2.7182')
// 1. Commas strictly between digits without whitespace:
s = s.replace(/(?<=\d),(?=\d)/g, '.');

// 2. Leading comma before digits (e.g. ',5' -> '0.5', '-,5' -> '-0.5'):
s = s.replace(/(^|[^0-9a-zA-Z_]),(?=\d+)/g, '$10.');
```

#### Behavior Verification Matrix
| Input | Transformed String | Interpretation | Status |
|---|---|---|---|
| `0,8333` | `0.8333` | Decimal scalar | Validated |
| `-2,7182` | `-2.7182` | Negative decimal | Validated |
| `459,75` | `459.75` | Large decimal | Validated |
| `,5` | `0.5` | Leading decimal | Validated |
| `1 + 0,5` | `1 + 0.5` | Expression | Validated |
| `(1, 2)` | `(1, 2)` | Coordinate pair (space preserved) | Safe |
| `[1, 2, 3]` | `[1, 2, 3]` | Array/vector (space preserved) | Safe |
| `[0,5, 0,8]` | `[0.5, 0.8]` | Array of decimals (space preserved) | Safe |
| `f(x, y)` | `f(x, y)` | Function call | Safe |

---

## 4. Four-Decimal Place Tolerance & Fraction Evaluation

### Mathematical Requirements
1. **4 Decimal Places Half-Unit Tolerance**:
   - The standard half-unit of the 4th decimal place is:
     $$\Delta = \frac{10^{-4}}{2} = 0.00005$$
   - A student answer must satisfy:
     $$|v_{\text{student}} - v_{\text{target}}| \le 0.00005$$
   - Or an explicit `tolerance` declared on the question if provided.
2. **Equivalence of Fractions and Decimals**:
   - Target is $0.8333$ (from $5/6$ rounded). Student enters `5/6`:
     $$|5/6 - 0.8333| = |0.83333333... - 0.8333| = 0.00003333... \le 0.00005 \implies \text{PASS}$$
   - Target is $5/6$. Student enters `0.8333`:
     $$|0.8333 - 5/6| = 0.00003333... \le 0.00005 \implies \text{PASS}$$
   - Target is $0.8333$. Student enters `0.833333` (higher precision):
     $$|0.833333 - 0.8333| = 0.000033 \le 0.00005 \implies \text{PASS}$$
3. **Rejection of Insufficient Precision & Errors**:
   - Student enters `0.833` (3 decimals):
     $$|0.833 - 0.8333| = 0.00033 > 0.00005 \implies \text{FAIL}$$
   - Student enters `0.8334` (incorrect 4th digit):
     $$|0.8334 - 0.8333| = 0.0001 > 0.00005 \implies \text{FAIL}$$
   - P-value target `0.0030`, student enters `0.0031`:
     $$|0.0031 - 0.0030| = 0.0001 > 0.00005 \implies \text{FAIL}$$
   - P-value target `0.0030`, student enters `0.003` or `0.0030`:
     $$|0.003 - 0.003| = 0 \le 0.00005 \implies \text{PASS}$$

### Implementation Strategy
We introduce a robust numerical comparator in `mathEquivalence.ts`:
```typescript
function areNumericValuesEquivalent(
  studentVal: number,
  targetVal: number,
  tolerance: number
): boolean {
  // 1. Direct absolute error within tolerance
  if (Math.abs(studentVal - targetVal) <= tolerance) {
    return true;
  }

  // 2. 4-decimal place rounded comparison:
  // Supports higher precision inputs (e.g. 0.833333 vs 0.8333) or fraction evaluations (5/6 vs 0.8333)
  const round4 = (v: number) => Math.round(v * 10000) / 10000;
  const sRound = round4(studentVal);
  const tRound = round4(targetVal);

  if (Math.abs(sRound - tRound) <= 1e-9) {
    // Ensure student did not provide insufficient precision for an inexact target.
    if (Math.abs(studentVal - tRound) <= tolerance || Math.abs(sRound - targetVal) <= tolerance) {
      return true;
    }
  }

  return false;
}
```

In `checkMathEquivalence`:
```typescript
const defaultTolerance = 0.00005;
const tolerance = (typeof targetAnswer === 'object' && targetAnswer.tolerance !== undefined && targetAnswer.tolerance !== null)
  ? targetAnswer.tolerance
  : defaultTolerance;

// Evaluate main numeric target
try {
  const studentVal = math.evaluate(normStudent);
  const targetVal = math.evaluate(normTarget);
  if (typeof studentVal === 'number' && typeof targetVal === 'number' && !isNaN(studentVal) && !isNaN(targetVal)) {
    if (areNumericValuesEquivalent(studentVal, targetVal, tolerance)) {
      return true;
    }
  }
} catch {}

// Evaluate accepted equivalents numerically
for (const alt of acceptedList) {
  try {
    const studentVal = math.evaluate(normStudent);
    const altVal = math.evaluate(normalizeMathExpression(alt));
    if (typeof studentVal === 'number' && typeof altVal === 'number' && !isNaN(studentVal) && !isNaN(altVal)) {
      if (areNumericValuesEquivalent(studentVal, altVal, tolerance)) {
        return true;
      }
    }
  } catch {}
}
```

---

## 5. UI Component Integration Analysis

### `platform/src/components/PracticeSession.tsx`
Line 103:
```typescript
} else if (currentQuestion.type === 'fill_in_the_blank') {
  correct = checkMathEquivalence(fillBlankValue, currentQuestion.correct_answer as any);
}
```
- Calls `checkMathEquivalence(fillBlankValue, currentQuestion.correct_answer)`.
- If `currentQuestion.correct_answer` is a string, number, or object with `canonical_algebraic` / `value` / `expression`, `checkMathEquivalence` will now seamlessly resolve it without needing changes in `PracticeSession.tsx`.

### `platform/src/components/QuestionCard.tsx`
Lines 183–210:
- Contains the text input `<input data-testid="fill-blank-input" value={fillBlankValue} ... />`.
- Live KaTeX preview renders `$${fillBlankValue}$$`. For `0,8333`, KaTeX renders `$0,8333$` properly. For `5/6` or `\frac{5}{6}`, KaTeX renders the fraction cleanly.
- No changes required.

---

## 6. Test Suite & Build Pipeline Architecture

### Existing Test Runner Mechanism
1. `tests/test_platform.py` defines:
   ```python
   NODE_SCRIPT = REPO_ROOT / "tests" / "test_math_adversarial_suite.mjs"
   RESULTS_PATH = REPO_ROOT / "tests" / "math_adversarial_results.json"
   ```
2. Python executes `node tests/test_math_adversarial_suite.mjs`.
3. The node script runs all test cases, prints the results, and writes JSON to `tests/math_adversarial_results.json`.
4. Pytest asserts on category pass rates and overall pass rate $\ge 98\%$.

### Bundling Pipeline
Because `tests/test_math_adversarial_suite.ts` imports from `./dist/mathEquivalence_bundle.mjs` and requires `mathjs`, it is compiled using `esbuild`.
- Step 1: Bundle math equivalence engine:
  ```powershell
  npx.cmd esbuild platform/src/utils/mathEquivalence.ts --bundle --format=esm --outfile=tests/dist/mathEquivalence_bundle.mjs
  ```
- Step 2: Bundle test suite into executable Node ESM script:
  ```powershell
  npx.cmd esbuild tests/test_math_adversarial_suite.ts --bundle --format=esm --platform=node --outfile=tests/test_math_adversarial_suite.mjs
  ```

### New Test Cases to Add in `tests/test_math_adversarial_suite.ts`
We specify 18 new test cases under `Category 7: Decimal Tolerance, Fractions, and Spanish Comma (R7)`:

| ID | Name | Student | Target | Expected | Rationale |
|---|---|---|---|---|---|
| `DEC-01` | Decimal comma standard | `"0,8333"` | `"0.8333"` | `true` | Spanish decimal notation |
| `DEC-02` | Decimal comma fraction equivalent | `"5/6"` | `"0,8333"` | `true` | Fraction vs Spanish decimal |
| `DEC-03` | Fraction target vs 4-decimal student | `"0.8333"` | `"5/6"` | `true` | Rounded input for fraction |
| `DEC-04` | Higher precision decimal student | `"0.833333"` | `"0.8333"` | `true` | Student writes 6 decimals |
| `DEC-05` | Higher precision with Spanish comma | `"0,833333"` | `"0.8333"` | `true` | Student writes 6 decimals with comma |
| `DEC-06` | Boundary error rejection | `"0.8334"` | `"0.8333"` | `false` | Difference 0.0001 > 0.00005 |
| `DEC-07` | Early truncation rejection | `"0.833"` | `"0.8333"` | `false` | Insufficient precision (diff 0.00033) |
| `DEC-08` | Target with `canonical_algebraic` | `"0,8333"` | `{ canonical_algebraic: "0.8333" }` | `true` | Object key support |
| `DEC-09` | Target with `value` string | `"0.8333"` | `{ value: "0.8333" }` | `true` | Object key support |
| `DEC-10` | Target with `value` number | `"0,25"` | `{ value: 0.25 }` | `true` | Primitive numeric value |
| `DEC-11` | P-value exact with comma | `"0,0030"` | `"0.0030"` | `true` | Trailing zeros p-value |
| `DEC-12` | P-value short notation | `"0.003"` | `"0.0030"` | `true` | Equivalent float value |
| `DEC-13` | P-value difference rejection | `"0.0031"` | `"0.0030"` | `false` | Difference 0.0001 > 0.00005 |
| `DEC-14` | Target with explicit tolerance | `"0.83"` | `{ canonical_algebraic: "0.8333", tolerance: 0.01 }` | `true` | Respects explicit tolerance |
| `DEC-15` | Negative decimal with comma | `"-2,7182"` | `"-2.7182"` | `true` | Negative signed float |
| `DEC-16` | Comma inside arithmetic expression | `"1 + 0,5"` | `"1.5"` | `true` | Operator preservation |
| `DEC-17` | Quarter fraction vs comma | `"0,25"` | `"1/4"` | `true` | Fraction vs comma decimal |
| `DEC-18` | Large statistical value with comma | `"459,75"` | `"459.75"` | `true` | Regression F-statistic (EViews) |
