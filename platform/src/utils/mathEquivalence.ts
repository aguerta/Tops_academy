import * as math from 'mathjs';
import { FillBlankAnswer } from '../types';

export const MATH_BUILTINS = new Set([
  'sin', 'cos', 'tan', 'sec', 'csc', 'cot',
  'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh',
  'exp', 'log', 'ln', 'sqrt', 'abs',
  'floor', 'ceil', 'round', 'min', 'max', 'pow',
  'pi', 'e', 'Math',
]);

const MATH_FUNCS = new Set([
  'sin', 'cos', 'tan', 'sec', 'csc', 'cot',
  'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh',
  'exp', 'log', 'ln', 'sqrt', 'abs',
  'floor', 'ceil', 'round', 'min', 'max', 'pow', 'Math',
]);

const POWER_FUNCS_RE = /(?<![a-zA-Z_])(sin|cos|tan|sec|csc|cot|asin|acos|atan|sinh|cosh|tanh|log|ln)\s*\^\s*(\([^()]+\)|-?\d+)\s*\(/g;

function normalizeFunctionPowers(expr: string): string {
  let s = expr;
  let safety = 0;
  while (safety < 20) {
    safety++;
    POWER_FUNCS_RE.lastIndex = 0;
    const match = POWER_FUNCS_RE.exec(s);
    if (!match) break;

    const fnName = match[1] === 'ln' ? 'log' : match[1];
    const expStr = match[2];
    const openParenIdx = match.index + match[0].length - 1;
    let depth = 1;
    let i = openParenIdx + 1;
    while (i < s.length && depth > 0) {
      if (s[i] === '(') depth++;
      else if (s[i] === ')') depth--;
      i++;
    }
    if (depth !== 0) break;

    const arg = s.slice(openParenIdx + 1, i - 1);
    const replacement = `(${fnName}(${arg}))^${expStr}`;
    s = s.slice(0, match.index) + replacement + s.slice(i);
  }
  return s;
}

function splitConcatenatedIdentifiers(expr: string, allowedVariables?: string[]): string {
  if (!allowedVariables || allowedVariables.length === 0) return expr;

  const allowedSet = new Set(allowedVariables.map((v) => v.trim()).filter(Boolean));
  const dictTokens = Array.from(new Set([...allowedSet, ...MATH_BUILTINS]))
    .filter(Boolean)
    .sort((a, b) => b.length - a.length);

  if (dictTokens.length === 0) return expr;

  return expr.replace(/(?<![a-zA-Z_])[a-zA-Z_][a-zA-Z0-9_]*\b/g, (ident) => {
    if (allowedSet.has(ident) || MATH_BUILTINS.has(ident)) {
      return ident;
    }

    const n = ident.length;
    const dp: Array<string[] | null> = new Array(n + 1).fill(null);
    dp[0] = [];

    for (let i = 0; i < n; i++) {
      if (dp[i] === null) continue;
      for (const tok of dictTokens) {
        if (ident.startsWith(tok, i)) {
          const nextIdx = i + tok.length;
          const candidate = [...dp[i]!, tok === 'ln' ? 'log' : tok];
          if (dp[nextIdx] === null || candidate.length < dp[nextIdx]!.length) {
            dp[nextIdx] = candidate;
          }
        }
      }
    }

    const segmented = dp[n];
    if (segmented && segmented.length >= 2) {
      return segmented.join(' * ');
    }
    return ident;
  });
}

function extractMathVariables(normExpr: string): string[] {
  const matches = normExpr.match(/[a-zA-Z_][a-zA-Z0-9_]*/g) || [];
  return Array.from(new Set(matches.filter((v) => !MATH_BUILTINS.has(v))));
}

/**
 * Normalizes a LaTeX or math expression string into clean mathematical syntax.
 */
export function normalizeMathExpression(raw: string, allowedVariables?: string[]): string {
  if (!raw) return '';

  let s = raw.trim();

  // Reject malformed double operators like 'x ++ 2'
  if (/\+\+|\/\//.test(s)) {
    return 'SYNTAX_ERROR';
  }

  // Normalize Python power, LaTeX/natural log, and braced exponents centrally
  s = s.replace(/\*\*/g, '^');
  s = s.replace(/\\ln\b/g, 'log');
  s = s.replace(/(?<![a-zA-Z_])ln\s*\(/g, 'log(');
  s = s.replace(/\^\{([^{}]+)\}/g, '^($1)');

  // Replace unicode minus, multiplication/division, and Unicode Greek / sqrt symbols
  s = s.replace(/[\u2212\u2013\u2014]/g, '-');
  s = s.replace(/[×·]/g, '*').replace(/÷/g, '/').replace(/√\s*\(/g, 'sqrt(');
  s = s
    .replace(/α/g, ' alpha ')
    .replace(/β/g, ' beta ')
    .replace(/γ/g, ' gamma ')
    .replace(/δ/g, ' delta ')
    .replace(/ε/g, ' epsilon ')
    .replace(/ζ/g, ' zeta ')
    .replace(/κ/g, ' kappa ')
    .replace(/ξ/g, ' xi ')
    .replace(/ψ/g, ' psi ')
    .replace(/Δ/g, ' Delta ')
    .replace(/θ/g, ' theta ')
    .replace(/λ/g, ' lambda ')
    .replace(/μ/g, ' mu ')
    .replace(/σ/g, ' sigma ')
    .replace(/ρ/g, ' rho ')
    .replace(/φ/g, ' phi ')
    .replace(/ω/g, ' omega ')
    .replace(/η/g, ' eta ')
    .replace(/τ/g, ' tau ')
    .replace(/π/g, ' pi ');

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

  // Normalize trig/log power notation like sin^2(x) -> (sin(x))^2
  s = normalizeFunctionPowers(s);

  // Domain-aware splitting of concatenated identifiers (e.g. 2xy -> 2 * x * y, xln(x) -> x * log(x))
  s = splitConcatenatedIdentifiers(s, allowedVariables);

  // Mask scientific notation literals (e.g. 1e-5, 2.5E+3) before implicit-mul digit*letter rule
  const sciLiterals: string[] = [];
  s = s.replace(/\b\d+(?:\.\d+)?[eE][+-]?\d+\b/g, (m) => {
    const idx = sciLiterals.length;
    sciLiterals.push(m);
    return `\uE000${idx}\uE001`;
  });

  // 1. Juxtaposed parentheses: ) ( -> ) * (
  s = s.replace(/\)\s*\(/g, ') * (');

  // 2. Number or closing paren followed by opening paren: 2(x) -> 2 * (x), )( -> ) * (
  s = s.replace(/(\d)\s*\(/g, '$1 * (');

  // 3. Closing paren followed by identifier or number: )x -> ) * x, )2 -> ) * 2
  s = s.replace(/\)\s*([a-zA-Z0-9_])/g, ') * $1');

  // 4. Identifier followed by opening paren, EXCEPT if identifier is a math function:
  // e.g. x(x+1) -> x * (x+1), but sin(x) -> sin(x)
  s = s.replace(/\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\(/g, (match, id) => {
    if (MATH_FUNCS.has(id)) return match;
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
      if (MATH_FUNCS.has(id1)) return match;
      return `${id1} * ${id2}`;
    });
  }

  // Restore scientific notation literals
  s = s.replace(/\uE000(\d+)\uE001/g, (_, idx) => sciLiterals[Number(idx)] ?? '');

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
  const normTarget = normalizeMathExpression(targetExpr);
  const targetVars = extractMathVariables(normTarget);
  const normStudent = normalizeMathExpression(rawStudent, targetVars);

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
  const studentVars = extractMathVariables(normStudent);
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
