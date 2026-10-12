import * as math from 'mathjs';
import { FillBlankAnswer } from '../types';

/**
 * Normalizes a LaTeX or math expression string into clean mathematical syntax.
 */
export function normalizeMathExpression(raw: string): string {
  if (!raw) return '';

  let s = raw.trim();

  // Reject malformed double operators like 'x ++ 2'
  if (/\+\+|\/\//.test(s)) {
    return 'SYNTAX_ERROR';
  }

  // Replace unicode minus and special dashes
  s = s.replace(/[\u2212\u2013\u2014]/g, '-');

  // Replace LaTeX multiplication
  s = s.replace(/\\cdot/g, '*').replace(/\\times/g, '*');

  // Normalize common Greek letters with spacing around tokens so adjacent tokens don't concatenate
  // e.g. \alpha\sigma -> alpha * sigma, 2\alpha -> 2 * alpha
  const greekPattern = /\\(alpha|beta|gamma|delta|epsilon|zeta|eta|theta|iota|kappa|lambda|mu|nu|xi|pi|rho|sigma|tau|upsilon|phi|chi|psi|omega)(?![a-zA-Z])/g;
  s = s.replace(greekPattern, ' $1 ');

  // Replace LaTeX fractions: \frac{a}{b} -> ((a)/(b))
  // Iterate to handle nested fractions
  let prev = '';
  while (prev !== s) {
    prev = s;
    s = s.replace(/\\frac\{([^{}]+)\}\{([^{}]+)\}/g, ' (($1)/($2)) ');
  }

  // Remove \left and \right delimiters
  s = s.replace(/\\left\s*/g, '').replace(/\\right\s*/g, '');

  // Remove \text{...} wrappers
  s = s.replace(/\\text\{([^{}]+)\}/g, ' $1 ');

  // Remove lingering curly braces
  s = s.replace(/[{}]/g, '');

  // Remove remaining backslashes
  s = s.replace(/\\/g, '');

  // Replace decimal comma (e.g. 0,8333 -> 0.8333, -2,7182 -> -2.7182)
  s = s.replace(/(?<=\d),(?=\d)/g, '.');
  s = s.replace(/(^|[^0-9a-zA-Z_]),(?=\d+)/g, '$10.');

  // Handle implicit multiplication cleanly:
  const mathFuncs = new Set([
    'sin', 'cos', 'tan', 'sec', 'csc', 'cot',
    'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh',
    'exp', 'log', 'ln', 'sqrt', 'abs', 'Math'
  ]);

  // 1. Juxtaposed parentheses: ) ( -> ) * (
  s = s.replace(/\)\s*\(/g, ') * (');

  // 2. Number or closing paren followed by opening paren: 2(x) -> 2 * (x), )( -> ) * (
  s = s.replace(/(\d)\s*\(/g, '$1 * (');

  // 3. Closing paren followed by identifier or number: )x -> ) * x, )2 -> ) * 2
  s = s.replace(/\)\s*([a-zA-Z0-9_])/g, ') * $1');

  // 4. Identifier followed by opening paren, EXCEPT if identifier is a math function:
  // e.g. x(x+1) -> x * (x+1), but sin(x) -> sin(x)
  s = s.replace(/\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\(/g, (match, id) => {
    if (mathFuncs.has(id)) return match;
    return `${id} * (`;
  });

  // 5. Digit followed by letter/variable: e.g. 2x -> 2 * x, 2 x -> 2 * x, 2 alpha -> 2 * alpha
  s = s.replace(/(\d)\s*([a-zA-Z_])/g, '$1 * $2');

  // 6. Letter/variable followed by digit with whitespace: e.g. x 2 -> x * 2, alpha 2 -> alpha * 2
  s = s.replace(/([a-zA-Z_])\s+(\d)/g, '$1 * $2');

  // 7. Adjacent identifiers separated by whitespace:
  // e.g. alpha sigma -> alpha * sigma, n sigma -> n * sigma, 1 - alpha sigma -> 1 - alpha * sigma
  // Loop to handle chains like alpha sigma n
  prev = '';
  while (prev !== s) {
    prev = s;
    s = s.replace(/\b([a-zA-Z_][a-zA-Z0-9_]*)\s+([a-zA-Z_][a-zA-Z0-9_]*)\b/g, (match, id1, id2) => {
      if (mathFuncs.has(id1)) return match;
      return `${id1} * ${id2}`;
    });
  }

  // Remove remaining spaces
  s = s.replace(/\s+/g, '');

  return s;
}

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

/**
 * Compares two math expressions for mathematical equivalence using:
 * 1. Normalized string comparison
 * 2. Pre-configured accepted equivalents
 * 3. Numeric evaluation (for fractions, decimals)
 * 4. mathjs AST symbolic difference simplification
 * 5. Monte Carlo numerical sampling for algebraic expressions with variables
 */
export function checkMathEquivalence(
  studentInput: string,
  targetAnswer: FillBlankAnswer | string | number
): boolean {
  if (!studentInput) return false;

  const targetExpr = extractTargetExpression(targetAnswer);
  const acceptedList = typeof targetAnswer === 'object' && targetAnswer !== null && targetAnswer.accepted_equivalents
    ? targetAnswer.accepted_equivalents
    : [];

  const defaultTolerance = 0.00005;
  const tolerance = (typeof targetAnswer === 'object' && targetAnswer !== null && targetAnswer.tolerance !== undefined && targetAnswer.tolerance !== null)
    ? targetAnswer.tolerance
    : defaultTolerance;

  const rawStudent = studentInput.trim();
  const normStudent = normalizeMathExpression(rawStudent);
  const normTarget = normalizeMathExpression(targetExpr);

  // 1. Direct match with target or any accepted equivalent
  if (normStudent === normTarget) {
    return true;
  }

  for (const alt of acceptedList) {
    if (normStudent === normalizeMathExpression(alt)) {
      return true;
    }
  }

  // 2. Numeric evaluation (e.g. 0.5 vs 1/2 or 2/4)
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
  } catch {
    // Non-numeric expressions will fail evaluate without scope, proceed to symbolic/sampling
  }

  // Check each accepted alternative numerically
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

  // 3. Symbolic simplification of difference (normStudent - normTarget)
  try {
    const diff = math.simplify(`(${normStudent}) - (${normTarget})`);
    if (diff.toString() === '0') {
      return true;
    }
  } catch {}

  for (const alt of acceptedList) {
    try {
      const normAlt = normalizeMathExpression(alt);
      const diff = math.simplify(`(${normStudent}) - (${normAlt})`);
      if (diff.toString() === '0') {
        return true;
      }
    } catch {}
  }

  // 4. Monte Carlo Numerical Sampling
  // Extract all alphabetic variable names (e.g., alpha, sigma, n, x)
  const extractVars = (expr: string): string[] => {
    const matches = expr.match(/[a-zA-Z_][a-zA-Z0-9_]*/g) || [];
    // Exclude mathematical constants and built-ins
    const mathBuiltins = new Set(['sin', 'cos', 'tan', 'exp', 'log', 'sqrt', 'abs', 'pi', 'e', 'Math']);
    return Array.from(new Set(matches.filter((v) => !mathBuiltins.has(v))));
  };

  const studentVars = extractVars(normStudent);
  const targetVars = extractVars(normTarget);
  const allVars = Array.from(new Set([...studentVars, ...targetVars]));

  if (allVars.length > 0) {
    // If student expression introduced completely alien variables not in target, not equivalent
    const targetVarSet = new Set(targetVars);
    const hasAlienVars = studentVars.some((v) => !targetVarSet.has(v));

    if (!hasAlienVars) {
      let allPassed = true;
      const sampleCount = 10;

      for (let i = 0; i < sampleCount; i++) {
        // Sample random positive values between 1.5 and 7.5 to avoid divisions by zero or edge poles
        const scope: Record<string, number> = {};
        allVars.forEach((v, idx) => {
          scope[v] = 1.5 + (idx * 0.7) + (i * 0.35);
        });

        try {
          const sVal = math.evaluate(normStudent, scope);
          const tVal = math.evaluate(normTarget, scope);

          if (
            typeof sVal !== 'number' ||
            typeof tVal !== 'number' ||
            isNaN(sVal) ||
            isNaN(tVal) ||
            Math.abs(sVal - tVal) > 1e-4
          ) {
            allPassed = false;
            break;
          }
        } catch {
          allPassed = false;
          break;
        }
      }

      if (allPassed) {
        return true;
      }
    }
  }

  return false;
}
