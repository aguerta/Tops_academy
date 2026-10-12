import { checkMathEquivalence, normalizeMathExpression } from './dist/mathEquivalence_bundle.mjs';

interface TestCase {
  id: string;
  category: string;
  name: string;
  student: string;
  target: any; // string or FillBlankAnswer
  expected: boolean;
  notes?: string;
}

const testCases: TestCase[] = [
  // ==========================================
  // CATEGORY 1: Algebraic Equivalence
  // ==========================================
  {
    id: "ALG-01",
    category: "Algebraic Equivalence",
    name: "Distributed vs factored with Greek letters and multiplication: 1 - (alpha + n)*sigma vs 1 - alpha*sigma - n*sigma",
    student: "1 - (alpha + n)*sigma",
    target: "1 - alpha*sigma - n*sigma",
    expected: true
  },
  {
    id: "ALG-02",
    category: "Algebraic Equivalence",
    name: "Sign flip in subtraction: -(x - 3) vs 3 - x",
    student: "-(x - 3)",
    target: "3 - x",
    expected: true
  },
  {
    id: "ALG-03",
    category: "Algebraic Equivalence",
    name: "Difference of squares factored vs expanded: (x + 2)*(x - 2) vs x^2 - 4",
    student: "(x + 2)*(x - 2)",
    target: "x^2 - 4",
    expected: true
  },
  {
    id: "ALG-04",
    category: "Algebraic Equivalence",
    name: "Square of binomial: (a + b)^2 vs a^2 + 2*a*b + b^2",
    student: "(a + b)^2",
    target: "a^2 + 2*a*b + b^2",
    expected: true
  },
  {
    id: "ALG-05",
    category: "Algebraic Equivalence",
    name: "Distributive law: 2*(x + y) vs 2*x + 2*y",
    student: "2*(x + y)",
    target: "2*x + 2*y",
    expected: true
  },
  {
    id: "ALG-06",
    category: "Algebraic Equivalence",
    name: "Split fraction: x/2 + y/2 vs (x + y)/2",
    student: "x/2 + y/2",
    target: "(x + y)/2",
    expected: true
  },
  {
    id: "ALG-07",
    category: "Algebraic Equivalence",
    name: "Linear rearrangement: -x + 5 vs 5 - x",
    student: "-x + 5",
    target: "5 - x",
    expected: true
  },
  {
    id: "ALG-08",
    category: "Algebraic Equivalence",
    name: "Product commutativity: x*y*z vs z*y*x",
    student: "x*y*z",
    target: "z*y*x",
    expected: true
  },
  {
    id: "ALG-09",
    category: "Algebraic Equivalence",
    name: "Nested distribution: 3*(2*x - 4) vs 6*x - 12",
    student: "3*(2*x - 4)",
    target: "6*x - 12",
    expected: true
  },
  {
    id: "ALG-10",
    category: "Algebraic Equivalence",
    name: "Target object with accepted_equivalents: 1-(alpha+n)*sigma vs targetObj",
    student: "1-(alpha+n)*sigma",
    target: {
      expression: "1 - alpha*sigma - n*sigma",
      accepted_equivalents: ["1-(alpha+n)*sigma", "1 - \\alpha\\sigma - n\\sigma"]
    },
    expected: true
  },
  {
    id: "ALG-11",
    category: "Algebraic Equivalence",
    name: "Implicit multiplication with whitespace: 2 x vs 2*x",
    student: "2 x",
    target: "2*x",
    expected: true
  },
  {
    id: "ALG-12",
    category: "Algebraic Equivalence",
    name: "Implicit multiplication juxtaposed: 2x vs 2*x",
    student: "2x",
    target: "2*x",
    expected: true
  },
  {
    id: "ALG-13",
    category: "Algebraic Equivalence",
    name: "Factored binomials without asterisk: (x + 1)(x - 1) vs x^2 - 1",
    student: "(x + 1)(x - 1)",
    target: "x^2 - 1",
    expected: true
  },

  // ==========================================
  // CATEGORY 2: Number Equivalence
  // ==========================================
  {
    id: "NUM-01",
    category: "Number Equivalence",
    name: "Decimal vs fraction: 0.5 vs 1/2",
    student: "0.5",
    target: "1/2",
    expected: true
  },
  {
    id: "NUM-02",
    category: "Number Equivalence",
    name: "Decimal with trailing zeros: 0.500 vs 1/2",
    student: "0.500",
    target: "1/2",
    expected: true
  },
  {
    id: "NUM-03",
    category: "Number Equivalence",
    name: "Unreduced fraction: 2/4 vs 1/2",
    student: "2/4",
    target: "1/2",
    expected: true
  },
  {
    id: "NUM-04",
    category: "Number Equivalence",
    name: "Quarter decimal: 0.25 vs 1/4",
    student: "0.25",
    target: "1/4",
    expected: true
  },
  {
    id: "NUM-05",
    category: "Number Equivalence",
    name: "Three quarters: 0.75 vs 3/4",
    student: "0.75",
    target: "3/4",
    expected: true
  },
  {
    id: "NUM-06",
    category: "Number Equivalence",
    name: "Improper fraction: 1.5 vs 3/2",
    student: "1.5",
    target: "3/2",
    expected: true
  },
  {
    id: "NUM-07",
    category: "Number Equivalence",
    name: "Negative decimal vs fraction: -0.5 vs -1/2",
    student: "-0.5",
    target: "-1/2",
    expected: true
  },
  {
    id: "NUM-08",
    category: "Number Equivalence",
    name: "Zero representation: 0 vs 0/5",
    student: "0",
    target: "0/5",
    expected: true
  },
  {
    id: "NUM-09",
    category: "Number Equivalence",
    name: "Leading zeros: 05.5 vs 5.5",
    student: "05.5",
    target: "5.5",
    expected: true
  },
  {
    id: "NUM-10",
    category: "Number Equivalence",
    name: "Tolerance within bound: 0.333 vs target with tolerance 0.001",
    student: "0.333",
    target: { expression: "1/3", tolerance: 0.001 },
    expected: true
  },

  // ==========================================
  // CATEGORY 3: Fractions and Powers
  // ==========================================
  {
    id: "FRAC-01",
    category: "Fractions and Powers",
    name: "Power with curly braces vs plain: x^{2} vs x^2",
    student: "x^{2}",
    target: "x^2",
    expected: true
  },
  {
    id: "FRAC-02",
    category: "Fractions and Powers",
    name: "LaTeX \\frac vs slash: \\frac{1}{2} vs 1/2",
    student: "\\frac{1}{2}",
    target: "1/2",
    expected: true
  },
  {
    id: "FRAC-03",
    category: "Fractions and Powers",
    name: "Fraction with variable in numerator: \\frac{x}{2} vs (1/2)*x",
    student: "\\frac{x}{2}",
    target: "(1/2)*x",
    expected: true
  },
  {
    id: "FRAC-04",
    category: "Fractions and Powers",
    name: "Fraction with binomial: \\frac{a+b}{c} vs (a+b)/c",
    student: "\\frac{a+b}{c}",
    target: "(a+b)/c",
    expected: true
  },
  {
    id: "FRAC-05",
    category: "Fractions and Powers",
    name: "Negative power: \\frac{1}{x} vs x^(-1)",
    student: "\\frac{1}{x}",
    target: "x^(-1)",
    expected: true
  },
  {
    id: "FRAC-06",
    category: "Fractions and Powers",
    name: "Nested LaTeX fractions: \\frac{\\frac{1}{2}}{3} vs 1/6",
    student: "\\frac{\\frac{1}{2}}{3}",
    target: "1/6",
    expected: true
  },
  {
    id: "FRAC-07",
    category: "Fractions and Powers",
    name: "Power of power: (x^2)^3 vs x^6",
    student: "(x^2)^3",
    target: "x^6",
    expected: true
  },
  {
    id: "FRAC-08",
    category: "Fractions and Powers",
    name: "Algebraic fraction reduction: \\frac{2*x}{4} vs \\frac{x}{2}",
    student: "\\frac{2*x}{4}",
    target: "\\frac{x}{2}",
    expected: true
  },
  {
    id: "FRAC-09",
    category: "Fractions and Powers",
    name: "LaTeX exponential with braces: e^{x} vs e^x",
    student: "e^{x}",
    target: "e^x",
    expected: true
  },

  // ==========================================
  // CATEGORY 4: Commutativity, Spaces, Greek Letters
  // ==========================================
  {
    id: "GREEK-01",
    category: "Commutativity & Greek",
    name: "Sum of Greek letters commuted: \\alpha + \\beta vs \\beta + \\alpha",
    student: "\\alpha + \\beta",
    target: "\\beta + \\alpha",
    expected: true
  },
  {
    id: "GREEK-02",
    category: "Commutativity & Greek",
    name: "\\cdot vs * with Greek: \\sigma \\cdot \\mu vs mu * sigma",
    student: "\\sigma \\cdot \\mu",
    target: "mu * sigma",
    expected: true
  },
  {
    id: "GREEK-03",
    category: "Commutativity & Greek",
    name: "Circle area: \\pi * r^2 vs r^2 * \\pi",
    student: "\\pi * r^2",
    target: "r^2 * \\pi",
    expected: true
  },
  {
    id: "GREEK-04",
    category: "Commutativity & Greek",
    name: "Wild whitespace padding: '   1  -  ( \\alpha + n ) * \\sigma   ' vs '1 - alpha*sigma - n*sigma'",
    student: "   1  -  ( \\alpha + n ) * \\sigma   ",
    target: "1 - alpha*sigma - n*sigma",
    expected: true
  },
  {
    id: "GREEK-05",
    category: "Commutativity & Greek",
    name: "Unicode minus character (U+2212): '3 \u2212 x' vs '3 - x'",
    student: "3 \u2212 x",
    target: "3 - x",
    expected: true
  },
  {
    id: "GREEK-06",
    category: "Commutativity & Greek",
    name: "Multiple Greek letters: \\gamma + \\delta + \\epsilon vs epsilon + delta + gamma",
    student: "\\gamma + \\delta + \\epsilon",
    target: "epsilon + delta + gamma",
    expected: true
  },
  {
    id: "GREEK-07",
    category: "Commutativity & Greek",
    name: "LaTeX text wrappers: \\text{x} + 1 vs x + 1",
    student: "\\text{x} + 1",
    target: "x + 1",
    expected: true
  },
  {
    id: "GREEK-08",
    category: "Commutativity & Greek",
    name: "LaTeX delimiters \\left( x \\right) vs (x)",
    student: "\\left( x + 2 \\right)",
    target: "(x + 2)",
    expected: true
  },
  {
    id: "GREEK-09",
    category: "Commutativity & Greek",
    name: "Adjacent Greek tokens: \\alpha\\sigma vs alpha * sigma",
    student: "\\alpha\\sigma",
    target: "alpha * sigma",
    expected: true
  },
  {
    id: "GREEK-10",
    category: "Commutativity & Greek",
    name: "LaTeX expression with adjacent Greek: 1 - \\alpha\\sigma - n\\sigma vs 1 - alpha*sigma - n*sigma",
    student: "1 - \\alpha\\sigma - n\\sigma",
    target: "1 - alpha*sigma - n*sigma",
    expected: true
  },

  // ==========================================
  // CATEGORY 5: Non-Equivalent Expressions (FALSE POSITIVE CHECKS)
  // Must return FALSE!
  // ==========================================
  {
    id: "FALSE-01",
    category: "False Positive Prevention",
    name: "Sign difference: x + 1 vs x - 1",
    student: "x + 1",
    target: "x - 1",
    expected: false
  },
  {
    id: "FALSE-02",
    category: "False Positive Prevention",
    name: "Coefficient difference: 2*x vs 3*x",
    student: "2*x",
    target: "3*x",
    expected: false
  },
  {
    id: "FALSE-03",
    category: "False Positive Prevention",
    name: "Power difference: x^2 vs x^3",
    student: "x^2",
    target: "x^3",
    expected: false
  },
  {
    id: "FALSE-04",
    category: "False Positive Prevention",
    name: "Denominator difference: x/2 vs x/3",
    student: "x/2",
    target: "x/3",
    expected: false
  },
  {
    id: "FALSE-05",
    category: "False Positive Prevention",
    name: "Sign error in two variables: x + y vs x - y",
    student: "x + y",
    target: "x - y",
    expected: false
  },
  {
    id: "FALSE-06",
    category: "False Positive Prevention",
    name: "Unnegated vs negated: -(x - 3) vs x - 3",
    student: "-(x - 3)",
    target: "x - 3",
    expected: false
  },
  {
    id: "FALSE-07",
    category: "False Positive Prevention",
    name: "Different decimals: 0.5 vs 0.55",
    student: "0.5",
    target: "0.55",
    expected: false
  },
  {
    id: "FALSE-08",
    category: "False Positive Prevention",
    name: "Different fractions: 1/2 vs 1/3",
    student: "1/2",
    target: "1/3",
    expected: false
  },
  {
    id: "FALSE-09",
    category: "False Positive Prevention",
    name: "Polynomial expansion mistake: (x + 1)^2 vs x^2 + 1",
    student: "(x + 1)^2",
    target: "x^2 + 1",
    expected: false
  },
  {
    id: "FALSE-10",
    category: "False Positive Prevention",
    name: "Variable substitution mismatch: x + y vs x + z",
    student: "x + y",
    target: "x + z",
    expected: false
  },
  {
    id: "FALSE-11",
    category: "False Positive Prevention",
    name: "Alien variable introduced: x + alien vs x",
    student: "x + alien",
    target: "x",
    expected: false
  },

  // ==========================================
  // CATEGORY 6: Boundary, Malformed, and Pathological Inputs
  // ==========================================
  {
    id: "BOUND-01",
    category: "Boundary & Malformed",
    name: "Empty string student input vs valid target: '' vs 'x'",
    student: "",
    target: "x",
    expected: false
  },
  {
    id: "BOUND-02",
    category: "Boundary & Malformed",
    name: "Whitespace only student input: '   ' vs 'x'",
    student: "   ",
    target: "x",
    expected: false
  },
  {
    id: "BOUND-03",
    category: "Boundary & Malformed",
    name: "Unbalanced opening parenthesis: '((x + 1)' vs 'x + 1'",
    student: "((x + 1)",
    target: "x + 1",
    expected: false
  },
  {
    id: "BOUND-04",
    category: "Boundary & Malformed",
    name: "Reversed parentheses: ')x + 1(' vs 'x + 1'",
    student: ")x + 1(",
    target: "x + 1",
    expected: false
  },
  {
    id: "BOUND-05",
    category: "Boundary & Malformed",
    name: "Trailing operators: 'x + ' vs 'x'",
    student: "x + ",
    target: "x",
    expected: false
  },
  {
    id: "BOUND-06",
    category: "Boundary & Malformed",
    name: "Double operators: 'x ++ 2' vs 'x + 2'",
    student: "x ++ 2",
    target: "x + 2",
    expected: false
  },
  {
    id: "BOUND-07",
    category: "Boundary & Malformed",
    name: "Division by zero in student: '1/0' vs '1'",
    student: "1/0",
    target: "1",
    expected: false
  },
  {
    id: "BOUND-08",
    category: "Boundary & Malformed",
    name: "Incomplete LaTeX command: '\\frac{1}' vs '1/2'",
    student: "\\frac{1}",
    target: "1/2",
    expected: false
  },
  {
    id: "BOUND-09",
    category: "Boundary & Malformed",
    name: "Random symbols: '@#$%' vs 'x'",
    student: "@#$%",
    target: "x",
    expected: false
  },
  {
    id: "BOUND-10",
    category: "Boundary & Malformed",
    name: "Zero identity: 'x - x' vs '0'",
    student: "x - x",
    target: "0",
    expected: true
  },

  // ==========================================
  // CATEGORY 7: Decimal Tolerance, Fractions, and Spanish Comma (R7)
  // ==========================================
  {
    id: "DEC-01",
    category: "Decimal Tolerance & Spanish Comma",
    name: "Decimal comma standard: '0,8333' vs '0.8333'",
    student: "0,8333",
    target: "0.8333",
    expected: true
  },
  {
    id: "DEC-02",
    category: "Decimal Tolerance & Spanish Comma",
    name: "Decimal comma fraction equivalent: '5/6' vs '0,8333'",
    student: "5/6",
    target: "0,8333",
    expected: true
  },
  {
    id: "DEC-03",
    category: "Decimal Tolerance & Spanish Comma",
    name: "Fraction target vs 4-decimal student: '0.8333' vs '5/6'",
    student: "0.8333",
    target: "5/6",
    expected: true
  },
  {
    id: "DEC-04",
    category: "Decimal Tolerance & Spanish Comma",
    name: "Higher precision decimal student: '0.833333' vs '0.8333'",
    student: "0.833333",
    target: "0.8333",
    expected: true
  },
  {
    id: "DEC-05",
    category: "Decimal Tolerance & Spanish Comma",
    name: "Higher precision with Spanish comma: '0,833333' vs '0.8333'",
    student: "0,833333",
    target: "0.8333",
    expected: true
  },
  {
    id: "DEC-06",
    category: "Decimal Tolerance & Spanish Comma",
    name: "Boundary error rejection: '0.8334' vs '0.8333'",
    student: "0.8334",
    target: "0.8333",
    expected: false
  },
  {
    id: "DEC-07",
    category: "Decimal Tolerance & Spanish Comma",
    name: "Early truncation rejection: '0.833' vs '0.8333'",
    student: "0.833",
    target: "0.8333",
    expected: false
  },
  {
    id: "DEC-08",
    category: "Decimal Tolerance & Spanish Comma",
    name: "Target with canonical_algebraic: '0,8333' vs { canonical_algebraic: '0.8333' }",
    student: "0,8333",
    target: { canonical_algebraic: "0.8333" },
    expected: true
  },
  {
    id: "DEC-09",
    category: "Decimal Tolerance & Spanish Comma",
    name: "Target with value string: '0.8333' vs { value: '0.8333' }",
    student: "0.8333",
    target: { value: "0.8333" },
    expected: true
  },
  {
    id: "DEC-10",
    category: "Decimal Tolerance & Spanish Comma",
    name: "Target with value number: '0,25' vs { value: 0.25 }",
    student: "0,25",
    target: { value: 0.25 },
    expected: true
  },
  {
    id: "DEC-11",
    category: "Decimal Tolerance & Spanish Comma",
    name: "P-value exact with comma: '0,0030' vs '0.0030'",
    student: "0,0030",
    target: "0.0030",
    expected: true
  },
  {
    id: "DEC-12",
    category: "Decimal Tolerance & Spanish Comma",
    name: "P-value short notation: '0.003' vs '0.0030'",
    student: "0.003",
    target: "0.0030",
    expected: true
  },
  {
    id: "DEC-13",
    category: "Decimal Tolerance & Spanish Comma",
    name: "P-value difference rejection: '0.0031' vs '0.0030'",
    student: "0.0031",
    target: "0.0030",
    expected: false
  },
  {
    id: "DEC-14",
    category: "Decimal Tolerance & Spanish Comma",
    name: "Target with explicit tolerance: '0.83' vs { canonical_algebraic: '0.8333', tolerance: 0.01 }",
    student: "0.83",
    target: { canonical_algebraic: "0.8333", tolerance: 0.01 },
    expected: true
  },
  {
    id: "DEC-15",
    category: "Decimal Tolerance & Spanish Comma",
    name: "Negative decimal with comma: '-2,7182' vs '-2.7182'",
    student: "-2,7182",
    target: "-2.7182",
    expected: true
  },
  {
    id: "DEC-16",
    category: "Decimal Tolerance & Spanish Comma",
    name: "Comma inside arithmetic expression: '1 + 0,5' vs '1.5'",
    student: "1 + 0,5",
    target: "1.5",
    expected: true
  },
  {
    id: "DEC-17",
    category: "Decimal Tolerance & Spanish Comma",
    name: "Quarter fraction vs comma: '0,25' vs '1/4'",
    student: "0,25",
    target: "1/4",
    expected: true
  },
  {
    id: "DEC-18",
    category: "Decimal Tolerance & Spanish Comma",
    name: "Large statistical value with comma: '459,75' vs '459.75'",
    student: "459,75",
    target: "459.75",
    expected: true
  }
];

// Run the suite
console.log(`Starting Math Equivalence Test Suite (${testCases.length} test cases)...\n`);

let passedCount = 0;
let failedCount = 0;
const results: any[] = [];

for (const tc of testCases) {
  let actual: boolean | string = false;
  let threw = false;
  let errorMsg = '';

  try {
    actual = checkMathEquivalence(tc.student, tc.target);
  } catch (err: any) {
    threw = true;
    errorMsg = err.message || String(err);
    actual = `CRASH: ${errorMsg}`;
  }

  const passed = actual === tc.expected;
  if (passed) {
    passedCount++;
  } else {
    failedCount++;
  }

  results.push({
    id: tc.id,
    category: tc.category,
    name: tc.name,
    student: tc.student,
    target: typeof tc.target === 'object' ? JSON.stringify(tc.target) : tc.target,
    expected: tc.expected,
    actual,
    passed,
    errorMsg: threw ? errorMsg : undefined
  });

  const status = passed ? 'PASS' : 'FAIL';
  console.log(`[${status}] ${tc.id}: ${tc.name}`);
  if (!passed) {
    console.log(`   Expected: ${tc.expected}, Got: ${actual}`);
    console.log(`   Student: "${tc.student}" | Target: ${typeof tc.target === 'object' ? JSON.stringify(tc.target) : `"${tc.target}"`}`);
  }
}

console.log(`\n========================================`);
console.log(`SUMMARY: ${passedCount}/${testCases.length} Passed, ${failedCount} Failed`);
console.log(`========================================\n`);

import * as fs from 'fs';
fs.writeFileSync(
  'tests/math_adversarial_results.json',
  JSON.stringify({ total: testCases.length, passed: passedCount, failed: failedCount, results }, null, 2)
);
console.log('Results written to tests/math_adversarial_results.json');
