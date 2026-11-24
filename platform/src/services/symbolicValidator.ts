import * as math from 'mathjs';
import {
  AdversarialBreakSpec,
  AdversarialReadoutSpec,
  ConceptMatchingSpec,
  CorrectAnswer,
  DiagnosticDistractor,
  FillBlankAnswer,
  ProofDagSpec,
  SymbolicConfig,
  UnstructuredModelSpec,
} from '../types';
import { checkMathEquivalence, normalizeMathExpression } from '../utils/mathEquivalence';

export interface SymbolicSyntaxResult {
  valid: boolean;
  normalized: string;
  latexPreview: string;
  error?: string;
}

export interface DiagnosticGradingResult {
  isCorrect: boolean;
  matchedDistractorId?: string;
  diagnosticRationale?: string;
  syntaxError?: string;
}

const UNICODE_TO_IDENT: Array<[RegExp, string]> = [
  [/θ/g, 'theta'],
  [/π/g, 'pi'],
  [/λ/g, 'lambda'],
  [/α/g, 'alpha'],
  [/β/g, 'beta'],
  [/γ/g, 'gamma'],
  [/δ/g, 'delta'],
  [/ε/g, 'epsilon'],
  [/ζ/g, 'zeta'],
  [/κ/g, 'kappa'],
  [/ξ/g, 'xi'],
  [/ψ/g, 'psi'],
  [/Δ/g, 'Delta'],
  [/σ/g, 'sigma'],
  [/μ/g, 'mu'],
  [/ρ/g, 'rho'],
  [/φ/g, 'phi'],
  [/ω/g, 'omega'],
  [/η/g, 'eta'],
  [/τ/g, 'tau'],
  [/√\s*\(/g, 'sqrt('],
  [/×|·/g, '*'],
  [/÷/g, '/'],
  [/[\u2212\u2013\u2014]/g, '-'],
];

const MATH_BUILTINS = new Set([
  'sin',
  'cos',
  'tan',
  'sec',
  'csc',
  'cot',
  'asin',
  'acos',
  'atan',
  'sinh',
  'cosh',
  'tanh',
  'exp',
  'log',
  'sqrt',
  'abs',
  'floor',
  'ceil',
  'round',
  'min',
  'max',
  'pow',
  'pi',
  'e',
  'true',
  'false',
  'and',
  'or',
  'not',
]);

/**
 * Normalizes student symbolic input (Unicode Greek, natural log `ln(...)`, `**` power,
 * implicit multiplication via `normalizeMathExpression`) into clean `mathjs` syntax.
 */
export function normalizeSymbolicInput(raw: string, allowedVariables?: string[]): string {
  if (!raw) return '';
  let s = raw.trim();
  for (const [pat, repl] of UNICODE_TO_IDENT) {
    s = s.replace(pat, repl);
  }
  s = normalizeMathExpression(s, allowedVariables);
  // Restore log(...) after normalizeMathExpression just in case
  s = s.replace(/\bln\(/g, 'log(');
  return s;
}

const FUNCTION_ONLY_BUILTINS = new Set([
  'sin', 'cos', 'tan', 'sec', 'csc', 'cot',
  'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh',
  'exp', 'log', 'sqrt', 'abs', 'floor', 'ceil', 'round', 'min', 'max', 'pow',
]);

/**
 * Validates symbolic syntax without eval/Function and generates a live KaTeX preview string.
 */
export function checkSymbolicSyntax(
  input: string,
  allowedVariables?: string[]
): SymbolicSyntaxResult {
  const trimmed = (input || '').trim();
  if (!trimmed) {
    return { valid: false, normalized: '', latexPreview: '', error: 'Expresión vacía.' };
  }
  const normalized = normalizeSymbolicInput(trimmed, allowedVariables);
  if (!normalized || normalized === 'SYNTAX_ERROR') {
    return { valid: false, normalized: '', latexPreview: '', error: 'Operador o sintaxis matemática inválida.' };
  }
  try {
    const ast = math.parse(normalized);
    const bareFunctions: string[] = [];
    const unknownVars: string[] = [];
    const allowedSet = allowedVariables && allowedVariables.length > 0
      ? new Set(allowedVariables.map((v) => v.trim()))
      : null;

    ast.traverse((node: math.MathNode, _path: string, parent: math.MathNode | null) => {
      if (node.type === 'SymbolNode') {
        const isFnHead = Boolean(parent && parent.type === 'FunctionNode' && (parent as math.FunctionNode).fn === node);
        const sym = (node as math.SymbolNode).name;
        if (!isFnHead && FUNCTION_ONLY_BUILTINS.has(sym)) {
          bareFunctions.push(sym);
          return;
        }
        if (allowedSet && !MATH_BUILTINS.has(sym) && !allowedSet.has(sym)) {
          unknownVars.push(sym);
        }
      }
    });

    if (bareFunctions.length > 0) {
      return {
        valid: false,
        normalized,
        latexPreview: ast.toTex(),
        error: `Uso inválido de función sin argumento: ${Array.from(new Set(bareFunctions)).join(', ')}`,
      };
    }

    if (unknownVars.length > 0) {
      return {
        valid: false,
        normalized,
        latexPreview: ast.toTex(),
        error: `Variable no declarada en el dominio: ${Array.from(new Set(unknownVars)).join(', ')}`,
      };
    }
    return { valid: true, normalized, latexPreview: ast.toTex() };
  } catch (err) {
    return {
      valid: false,
      normalized,
      latexPreview: '',
      error: err instanceof Error ? err.message : 'Sintaxis matemática inválida.',
    };
  }
}

function extractExprVariables(normExpr: string): string[] {
  try {
    const ast = math.parse(normExpr);
    const vars = new Set<string>();
    ast.traverse((node: math.MathNode, _path: string, parent: math.MathNode | null) => {
      if (node.type === 'SymbolNode') {
        // Ignore function call head symbols like sin in sin(x)
        if (parent && parent.type === 'FunctionNode' && (parent as math.FunctionNode).fn === node) {
          return;
        }
        const name = (node as math.SymbolNode).name;
        if (!MATH_BUILTINS.has(name)) {
          vars.add(name);
        }
      }
    });
    return Array.from(vars);
  } catch {
    return [];
  }
}

/**
 * Checks mathematical equivalence across multi-variable symbolic and numeric expressions
 * using AST simplification plus 12 non-collinear deterministic test points in mathjs scope.
 */
export function areSymbolicExpressionsEquivalent(
  studentRaw: string,
  targetAnswer: FillBlankAnswer | string | number,
  allowedVariables?: string[]
): boolean {
  let normalizedTarget: FillBlankAnswer | string | number = targetAnswer;
  if (typeof targetAnswer === 'string') {
    normalizedTarget = normalizeSymbolicInput(targetAnswer, allowedVariables);
  } else if (typeof targetAnswer === 'object' && targetAnswer !== null) {
    const rawMain =
      targetAnswer.expression ?? targetAnswer.canonical_algebraic ?? targetAnswer.value ?? '';
    const eqs = Array.isArray(targetAnswer.accepted_equivalents)
      ? targetAnswer.accepted_equivalents.map((e) => normalizeSymbolicInput(String(e), allowedVariables))
      : undefined;
    normalizedTarget = {
      ...targetAnswer,
      expression: normalizeSymbolicInput(String(rawMain), allowedVariables),
      ...(targetAnswer.canonical_algebraic !== undefined
        ? { canonical_algebraic: normalizeSymbolicInput(String(targetAnswer.canonical_algebraic), allowedVariables) }
        : {}),
      ...(eqs ? { accepted_equivalents: eqs } : {}),
    };
  }

  const targetMainStr =
    typeof normalizedTarget === 'string'
      ? normalizedTarget
      : typeof normalizedTarget === 'number'
        ? String(normalizedTarget)
        : String(
            normalizedTarget.expression ||
              normalizedTarget.canonical_algebraic ||
              normalizedTarget.value ||
              ''
          );
  const targetExtractedVars = extractExprVariables(targetMainStr);
  const effectiveVars = Array.from(new Set([...(allowedVariables || []), ...targetExtractedVars]));

  const normStudent = normalizeSymbolicInput(studentRaw, effectiveVars);
  if (!normStudent || normStudent === 'SYNTAX_ERROR') {
    return false;
  }

  if (checkMathEquivalence(normStudent, normalizedTarget)) {
    return true;
  }

  // Fallback non-collinear AST compiled probe (handles cases with e^x vs exp(x), ln vs log, multi-vars)
  const targetStr =
    typeof normalizedTarget === 'string'
      ? normalizedTarget
      : typeof normalizedTarget === 'number'
        ? String(normalizedTarget)
        : String(
            normalizedTarget.expression ||
              normalizedTarget.canonical_algebraic ||
              normalizedTarget.value ||
              ''
          );
  const tol =
    typeof normalizedTarget === 'object' &&
    normalizedTarget !== null &&
    typeof normalizedTarget.tolerance === 'number'
      ? Math.max(normalizedTarget.tolerance, 1e-4)
      : 1e-4;

  const candidates = [targetStr];
  if (
    typeof normalizedTarget === 'object' &&
    normalizedTarget !== null &&
    Array.isArray(normalizedTarget.accepted_equivalents)
  ) {
    for (const eq of normalizedTarget.accepted_equivalents) {
      if (eq && !candidates.includes(eq)) {
        candidates.push(eq);
      }
    }
  }

  let sCompiled: math.EvalFunction;
  try {
    sCompiled = math.compile(normStudent);
  } catch {
    return false;
  }

  const sVars = extractExprVariables(normStudent);
  const allowedSet = allowedVariables && allowedVariables.length > 0 ? new Set(allowedVariables) : null;

  for (const cand of candidates) {
    if (!cand) continue;
    let cCompiled: math.EvalFunction;
    try {
      cCompiled = math.compile(cand);
    } catch {
      continue;
    }

    const cVars = extractExprVariables(cand);
    const validVarSet = allowedSet ? new Set([...cVars, ...allowedSet]) : new Set(cVars);
    if (cVars.length > 0 && sVars.some((v) => !validVarSet.has(v))) {
      continue;
    }

    const allVars = Array.from(new Set([...sVars, ...cVars]));
    if (allVars.length === 0) {
      try {
        const sv = sCompiled.evaluate({});
        const cv = cCompiled.evaluate({});
        if (
          typeof sv === 'number' &&
          typeof cv === 'number' &&
          Number.isFinite(sv) &&
          Number.isFinite(cv) &&
          Math.abs(sv - cv) <= tol
        ) {
          return true;
        }
      } catch {
        continue;
      }
      continue;
    }

    let validSamples = 0;
    let allMatch = true;
    for (let i = 0; i < 12; i++) {
      const scope: Record<string, number> = {};
      allVars.forEach((v, idx) => {
        const primeJitter = ((i * 17 + idx * 29 + i * idx * 7) % 23) * 0.27;
        scope[v] = 1.25 + primeJitter + idx * 0.19;
      });
      try {
        const sv = sCompiled.evaluate(scope);
        const cv = cCompiled.evaluate(scope);
        if (typeof sv !== 'number' || typeof cv !== 'number' || !Number.isFinite(sv) || !Number.isFinite(cv)) {
          continue;
        }
        validSamples++;
        if (Math.abs(sv - cv) > Math.max(tol, Math.abs(cv) * 1e-6)) {
          allMatch = false;
          break;
        }
      } catch {
        allMatch = false;
        break;
      }
    }
    if (allMatch && validSamples >= 8) {
      return true;
    }
  }

  return false;
}

/**
 * Grades open_symbolic OR fill_in_the_blank answers and checks `diagnostic_distractors`
 * on mismatch to surface targeted misconception feedback without visible option lists.
 */
export function validateSymbolicAnswer(
  userInput: string,
  correctAnswer: CorrectAnswer,
  diagnosticDistractors?: DiagnosticDistractor[],
  symbolicConfig?: SymbolicConfig
): DiagnosticGradingResult {
  const trimmed = (userInput || '').trim();
  if (!trimmed) {
    return { isCorrect: false, syntaxError: 'Ingresa una respuesta antes de comprobar.' };
  }

  const target = correctAnswer as FillBlankAnswer | string | number;
  const isEq = areSymbolicExpressionsEquivalent(trimmed, target, symbolicConfig?.variables);
  if (isEq) {
    return { isCorrect: true };
  }

  // Check diagnostic distractors to diagnose specific algebraic/conceptual traps
  if (Array.isArray(diagnosticDistractors) && diagnosticDistractors.length > 0) {
    const normInput = normalizeSymbolicInput(trimmed, symbolicConfig?.variables);
    for (const dd of diagnosticDistractors) {
      if (!dd) continue;
      if (dd.match_type === 'regex' && typeof dd.expression === 'string') {
        try {
          if (new RegExp(dd.expression, 'i').test(trimmed)) {
            return {
              isCorrect: false,
              matchedDistractorId: dd.distractor_id,
              diagnosticRationale: dd.error_rationale,
            };
          }
        } catch {
          // ignore malformed regex
        }
        continue;
      }

      const trapObj: FillBlankAnswer = {
        ...(dd.expression !== undefined ? { expression: dd.expression } : {}),
        ...(dd.value !== undefined ? { value: dd.value } : {}),
        ...(dd.accepted_equivalents ? { accepted_equivalents: dd.accepted_equivalents } : {}),
        ...(dd.tolerance !== undefined ? { tolerance: dd.tolerance } : {}),
      };
      const trapTargetExpr = dd.expression ?? dd.value ?? '';
      if (
        (typeof trapTargetExpr === 'string' &&
          normalizeSymbolicInput(trapTargetExpr, symbolicConfig?.variables) === normInput) ||
        areSymbolicExpressionsEquivalent(trimmed, trapObj, symbolicConfig?.variables)
      ) {
        return {
          isCorrect: false,
          matchedDistractorId: dd.distractor_id,
          diagnosticRationale: dd.error_rationale,
        };
      }
    }
  }

  return { isCorrect: false };
}

/**
 * Validates a ProofDAG submission in O(V + E) (< 5 ms):
 * - Immediately diagnoses included fallacy tiles
 * - Ensures all non-fallacy required steps are present
 * - Verifies topological precedence across every DAG edge `[u, v]` (multiple valid orders supported)
 * - Verifies step justifications when `require_justification` is active
 */
export function validateProofDagSubmission(
  orderedStepIds: string[],
  justificationsByStepId: Record<string, string>,
  dagSpec: ProofDagSpec
): DiagnosticGradingResult {
  if (!orderedStepIds || orderedStepIds.length === 0) {
    return {
      isCorrect: false,
      diagnosticRationale: 'Ordena los pasos válidos en la zona de demostración antes de comprobar.',
    };
  }

  const stepById = new Map(dagSpec.steps.map((s) => [s.id, s]));

  // 1. Detect included fallacy steps first with tailored misconception rationale
  for (const sid of orderedStepIds) {
    const st = stepById.get(sid);
    if (st?.is_fallacy) {
      return {
        isCorrect: false,
        matchedDistractorId: st.distractor_id,
        diagnosticRationale:
          st.error_rationale ||
          `El paso "${st.content}" introduce una deducción inválida y no pertenece a la demostración.`,
      };
    }
  }

  // 2. Check duplicate or missing required valid steps
  const validSteps = dagSpec.steps.filter((s) => !s.is_fallacy);
  const pos = new Map<string, number>();
  for (let i = 0; i < orderedStepIds.length; i++) {
    const sid = orderedStepIds[i];
    if (!stepById.has(sid) || pos.has(sid)) {
      return {
        isCorrect: false,
        diagnosticRationale: 'La secuencia contiene identificadores duplicados o inválidos.',
      };
    }
    pos.set(sid, i);
  }

  for (const vs of validSteps) {
    if (!pos.has(vs.id)) {
      return {
        isCorrect: false,
        diagnosticRationale: `Falta incluir un paso deductivo necesario en la demostración (${validSteps.length} requeridos).`,
      };
    }
  }

  if (orderedStepIds.length !== validSteps.length) {
    return {
      isCorrect: false,
      diagnosticRationale: 'La demostración debe contener exactamente los pasos válidos requeridos.',
    };
  }

  // 3. Check all topological precedence constraints edges: [u, v] => pos(u) < pos(v)
  for (const [u, v] of dagSpec.edges || []) {
    const pu = pos.get(u);
    const pv = pos.get(v);
    if (pu === undefined || pv === undefined || pu >= pv) {
      return {
        isCorrect: false,
        diagnosticRationale:
          'El orden lógico viola una dependencia causal: un paso consecuente aparece antes de su premisa necesaria.',
      };
    }
  }

  // 4. Verify optional justification rules per step
  if (dagSpec.require_justification) {
    for (const vs of validSteps) {
      const submittedJust = (justificationsByStepId[vs.id] || '').trim();
      const expectedJust = (vs.justification || '').trim();
      if (!submittedJust) {
        return {
          isCorrect: false,
          diagnosticRationale: 'Asigna la regla o justificación matemática a cada paso colocado.',
        };
      }
      if (submittedJust !== expectedJust) {
        return {
          isCorrect: false,
          diagnosticRationale: `La justificación elegida ("${submittedJust}") no respalda la transición lógica del paso seleccionado.`,
        };
      }
    }
  }

  return { isCorrect: true };
}

/**
 * Expands Python-style chained comparisons like `a <= x <= b` into `(a <= x) and (x <= b)`
 * so mathjs evaluates them mathematically rather than comparing boolean <= number.
 */
function expandChainedComparisons(expr: string): string {
  const ops = ['<=', '>=', '==', '!=', '<', '>'];
  const tokens: Array<{ value: string; op?: string }> = [];
  let depth = 0;
  let i = 0;
  let start = 0;

  while (i < expr.length) {
    const ch = expr[i];
    if (ch === '(') depth++;
    else if (ch === ')') depth = Math.max(0, depth - 1);
    else if (depth === 0) {
      const matchedOp = ops.find((op) => expr.startsWith(op, i));
      if (matchedOp) {
        tokens.push({ value: expr.slice(start, i).trim(), op: matchedOp });
        i += matchedOp.length;
        start = i;
        continue;
      }
    }
    i++;
  }
  tokens.push({ value: expr.slice(start).trim() });

  if (tokens.length <= 2) {
    return expr;
  }
  const parts: string[] = [];
  for (let k = 0; k < tokens.length - 1; k++) {
    parts.push(`((${tokens[k].value}) ${tokens[k].op} (${tokens[k + 1].value}))`);
  }
  return parts.join(' and ');
}

function splitTopLevelLogical(expr: string, keyword: 'and' | 'or'): string[] {
  const out: string[] = [];
  let depth = 0;
  let lastSplit = 0;
  const re = keyword === 'and' ? /\band\b/g : /\bor\b/g;
  // Walk tracking paren depth so inside parens won't split incorrectly
  for (let i = 0; i < expr.length; i++) {
    if (expr[i] === '(') depth++;
    else if (expr[i] === ')') depth = Math.max(0, depth - 1);
    else if (depth === 0) {
      re.lastIndex = i;
      const m = re.exec(expr);
      if (m && m.index === i) {
        const beforeOk = i === 0 || !/[a-zA-Z0-9_]/.test(expr[i - 1]);
        const afterIdx = i + keyword.length;
        const afterOk = afterIdx >= expr.length || !/[a-zA-Z0-9_]/.test(expr[afterIdx]);
        if (beforeOk && afterOk) {
          out.push(expr.slice(lastSplit, i).trim());
          lastSplit = afterIdx;
          i = afterIdx - 1;
        }
      }
    }
  }
  out.push(expr.slice(lastSplit).trim());
  return out.filter(Boolean);
}

/**
 * Evaluates a boolean predicate string safely via mathjs AST without `Function`/`eval`.
 */
export function evaluateSafePredicate(expr: string, scope: Record<string, number>): boolean {
  let clean = (expr || '').trim();
  if (!clean) return false;
  clean = clean.replace(/&&/g, ' and ').replace(/\|\|/g, ' or ').replace(/\*\*/g, '^');
  clean = clean.replace(/\bln\s*\(/g, 'log(');
  for (const [pat, repl] of UNICODE_TO_IDENT) {
    clean = clean.replace(pat, repl);
  }

  // Recursively evaluate top-level `or` -> `and` -> comparisons / mathjs expression
  const orParts = splitTopLevelLogical(clean, 'or');
  if (orParts.length > 1) {
    return orParts.some((p) => evaluateSafePredicate(p, scope));
  }
  const andParts = splitTopLevelLogical(clean, 'and');
  if (andParts.length > 1) {
    return andParts.every((p) => evaluateSafePredicate(p, scope));
  }

  let single = andParts[0];
  if (single.startsWith('(') && single.endsWith(')')) {
    // Strip redundant balanced outer parens
    let depth = 0;
    let balancedOuter = true;
    for (let i = 0; i < single.length - 1; i++) {
      if (single[i] === '(') depth++;
      else if (single[i] === ')') {
        depth--;
        if (depth === 0) {
          balancedOuter = false;
          break;
        }
      }
    }
    if (balancedOuter) {
      return evaluateSafePredicate(single.slice(1, -1), scope);
    }
  }

  if (/^not\b/i.test(single)) {
    return !evaluateSafePredicate(single.slice(3).trim(), scope);
  }

  single = expandChainedComparisons(single);
  if (splitTopLevelLogical(single, 'and').length > 1) {
    return evaluateSafePredicate(single, scope);
  }

  const res = math.evaluate(single, { ...scope });
  return Boolean(res);
}

/**
 * Validates `adversarial_break` submissions across both `find_fallacy` and `counterexample` submodes.
 */
export function validateAdversarialSubmission(
  submission: {
    selectedStepId?: string | null;
    selectedReasonId?: string | null;
    witnessValues?: Record<string, string>;
  },
  spec: AdversarialBreakSpec
): DiagnosticGradingResult {
  if (spec.mode === 'find_fallacy') {
    const steps = spec.steps || [];
    const fallacyStep = steps.find((s) => s.is_fallacy);
    if (!submission.selectedStepId) {
      return {
        isCorrect: false,
        diagnosticRationale: 'Selecciona el paso de la derivación donde se comete la falacia.',
      };
    }
    if (!fallacyStep || submission.selectedStepId !== fallacyStep.id) {
      const picked = steps.find((s) => s.id === submission.selectedStepId);
      return {
        isCorrect: false,
        matchedDistractorId: fallacyStep?.distractor_id,
        diagnosticRationale: picked?.valid_explanation
          ? `Ese paso es lógicamente válido: ${picked.valid_explanation}`
          : 'El paso seleccionado es consistente; inspecciona dónde se viola una hipótesis o condición de regularidad.',
      };
    }

    const reasons = spec.reason_options || [];
    if (reasons.length > 0) {
      if (!submission.selectedReasonId) {
        return {
          isCorrect: false,
          diagnosticRationale: 'Identificaste el paso falaz; ahora selecciona la justificación exacta del fallo.',
        };
      }
      const pickedReason = reasons.find((r) => r.id === submission.selectedReasonId);
      if (!pickedReason || !pickedReason.is_correct) {
        return {
          isCorrect: false,
          matchedDistractorId: pickedReason?.distractor_id || fallacyStep.distractor_id,
          diagnosticRationale:
            pickedReason?.error_rationale ||
            fallacyStep.error_rationale ||
            'Identificaste el paso incorrecto, pero la justificación elegida no explica la ruptura matemática real.',
        };
      }
    }

    return { isCorrect: true };
  }

  // mode === 'counterexample'
  const inputs = spec.inputs || [];
  const witnessValues = submission.witnessValues || {};
  const scope: Record<string, number> = {};

  for (const inp of inputs) {
    const iid = inp.id || inp.name || '';
    const rawVal = (witnessValues[iid] ?? '').trim();
    if (!rawVal) {
      return {
        isCorrect: false,
        diagnosticRationale: `Ingresa un valor numérico para "${inp.label || iid}".`,
      };
    }
    const normalizedNum = normalizeSymbolicInput(rawVal);
    let numVal: number;
    try {
      const evalRes = math.evaluate(normalizedNum);
      if (typeof evalRes !== 'number' || !Number.isFinite(evalRes)) {
        return {
          isCorrect: false,
          diagnosticRationale: `El valor para "${inp.label || iid}" debe ser numérico finito.`,
        };
      }
      numVal = evalRes;
    } catch {
      return {
        isCorrect: false,
        diagnosticRationale: `No se pudo interpretar "${rawVal}" como número real.`,
      };
    }

    if (inp.type === 'integer' && !Number.isInteger(numVal)) {
      return {
        isCorrect: false,
        diagnosticRationale: `El parámetro "${inp.label || iid}" exige un número entero.`,
      };
    }
    if (inp.min !== undefined && numVal < inp.min - 1e-9) {
      return {
        isCorrect: false,
        diagnosticRationale: `"${inp.label || iid}" debe ser mayor o igual a ${inp.min}.`,
      };
    }
    if (inp.max !== undefined && numVal > inp.max + 1e-9) {
      return {
        isCorrect: false,
        diagnosticRationale: `"${inp.label || iid}" debe ser menor o igual a ${inp.max}.`,
      };
    }
    scope[iid] = numVal;
  }

  for (const trap of spec.trap_predicates || []) {
    try {
      const triggered = evaluateSafePredicate(trap.expr, scope);
      if (triggered) {
        return {
          isCorrect: false,
          matchedDistractorId: trap.distractor_id,
          diagnosticRationale:
            trap.error_rationale ||
            trap.failure_rationale ||
            'El testigo propuesto cae en una trampa conceptual conocida.',
        };
      }
    } catch {
      // Unparseable/un-evaluable trap predicate with partial inputs does not pass/fail by itself
    }
  }

  for (const pred of spec.predicates || []) {
    try {
      const ok = evaluateSafePredicate(pred.expr, scope);
      if (!ok) {
        return {
          isCorrect: false,
          matchedDistractorId: pred.distractor_id,
          diagnosticRationale: pred.failure_rationale || pred.error_rationale,
        };
      }
    } catch {
      return {
        isCorrect: false,
        matchedDistractorId: pred.distractor_id,
        diagnosticRationale:
          pred.failure_rationale ||
          pred.error_rationale ||
          'Error al evaluar la condición del contraejemplo.',
      };
    }
  }

  return { isCorrect: true };
}

export interface EvaluatedReadoutItem {
  id: string;
  label: string;
  value: number | null;
  formatted: string;
  unit?: string;
}

/**
 * Safely evaluates `adversarial_break.computed_readouts` using mathjs from live student input strings.
 */
export function evaluateAdversarialReadouts(
  readouts: AdversarialReadoutSpec[] | undefined,
  witnessValues: Record<string, string>
): EvaluatedReadoutItem[] {
  if (!readouts || readouts.length === 0) return [];
  const scope: Record<string, number> = {};
  for (const [k, raw] of Object.entries(witnessValues || {})) {
    const trimmed = String(raw ?? '').trim();
    if (!trimmed) continue;
    try {
      const val = math.evaluate(normalizeSymbolicInput(trimmed));
      if (typeof val === 'number' && Number.isFinite(val)) {
        scope[k] = val;
      }
    } catch {
      // ignore invalid partial inputs
    }
  }

  return readouts.map((ro, idx) => {
    const id = ro.id || `ro-${idx}`;
    try {
      const evaluated = math.evaluate(normalizeSymbolicInput(ro.expr), scope);
      if (typeof evaluated === 'number' && Number.isFinite(evaluated)) {
        const rounded = Math.round(evaluated * 10000) / 10000;
        return {
          id,
          label: ro.label,
          value: evaluated,
          formatted: Number.isInteger(rounded) ? String(rounded) : rounded.toFixed(4).replace(/\.?0+$/, ''),
          unit: ro.unit,
        };
      }
      if (typeof evaluated === 'boolean') {
        return {
          id,
          label: ro.label,
          value: evaluated ? 1 : 0,
          formatted: evaluated ? 'Verdadero' : 'Falso',
          unit: ro.unit,
        };
      }
    } catch {
      // incomplete scope
    }
    return {
      id,
      label: ro.label,
      value: null,
      formatted: '—',
      unit: ro.unit,
    };
  });
}

/**
 * Validates Stage 0 (`unstructured_model`) sequential phase submissions.
 */
export function validateStage0Phase(
  phase: 1 | 2 | 3,
  answer: {
    phase1Roles: Record<string, string>;
    phase2SelectedIds: string[];
    phase3SelectedId: string | null;
    phase3Expression: string;
  },
  spec: UnstructuredModelSpec
): DiagnosticGradingResult {
  if (phase === 1) {
    const items = spec.phase1_variables.items || [];
    for (const item of items) {
      const chosen = answer.phase1Roles[item.id];
      if (!chosen) {
        return {
          isCorrect: false,
          diagnosticRationale: `Asigna un rol a cada magnitud o elemento listado ("${item.label}").`,
        };
      }
      if (chosen !== item.correct_role) {
        return {
          isCorrect: false,
          matchedDistractorId: item.distractor_id,
          diagnosticRationale:
            item.error_rationale ||
            `El rol asignado a "${item.label}" no corresponde a su función en el modelo.`,
        };
      }
    }
    return { isCorrect: true };
  }

  if (phase === 2) {
    const opts = spec.phase2_assumptions.options || [];
    const requiredSet = new Set(opts.filter((o) => o.is_required).map((o) => o.id));
    const selectedSet = new Set(answer.phase2SelectedIds || []);
    if (selectedSet.size === 0) {
      return {
        isCorrect: false,
        diagnosticRationale: 'Selecciona los supuestos o restricciones indispensables para el modelo.',
      };
    }

    for (const sid of selectedSet) {
      if (!requiredSet.has(sid)) {
        const opt = opts.find((o) => o.id === sid);
        return {
          isCorrect: false,
          matchedDistractorId: opt?.distractor_id,
          diagnosticRationale:
            opt?.error_rationale ||
            `El supuesto seleccionado ("${opt?.content || sid}") es inválido o innecesario para este planteamiento.`,
        };
      }
    }

    for (const rid of requiredSet) {
      if (!selectedSet.has(rid)) {
        const opt = opts.find((o) => o.id === rid);
        return {
          isCorrect: false,
          matchedDistractorId: opt?.distractor_id,
          diagnosticRationale:
            opt?.error_rationale ||
            'Falta incluir al menos una condición de regularidad o supuesto activo esencial.',
        };
      }
    }

    return { isCorrect: true };
  }

  // Phase 3: Formal formulation
  const p3 = spec.phase3_formulation;
  if (p3.input_mode === 'select') {
    const opts = p3.options || [];
    if (!answer.phase3SelectedId) {
      return {
        isCorrect: false,
        diagnosticRationale: 'Selecciona la formulación formal que traduce el problema.',
      };
    }
    const picked = opts.find((o) => o.id === answer.phase3SelectedId);
    if (!picked || !picked.is_correct) {
      return {
        isCorrect: false,
        matchedDistractorId: picked?.distractor_id,
        diagnosticRationale:
          picked?.error_rationale ||
          'La expresión o modelo seleccionado no respeta las variables y supuestos de las fases anteriores.',
      };
    }
    return { isCorrect: true };
  }

  if (!p3.correct_expression) {
    return { isCorrect: false, diagnosticRationale: 'Configuración de formulación incompleta.' };
  }
  return validateSymbolicAnswer(
    answer.phase3Expression,
    p3.correct_expression,
    p3.diagnostic_distractors
  );
}

/**
 * Validates `concept_matching` 2-column premise->target associations.
 */
export function validateConceptMatchingSubmission(
  pairs: Record<string, string>,
  spec: ConceptMatchingSpec
): DiagnosticGradingResult {
  const premises = spec.premises || [];
  const targetById = new Map((spec.targets || []).map((t) => [t.id, t]));

  for (const pr of premises) {
    const pickedTid = pairs[pr.id];
    if (!pickedTid) {
      return {
        isCorrect: false,
        diagnosticRationale: 'Asocia cada premisa con un elemento antes de comprobar.',
      };
    }
    const expectedTid = spec.correct_pairs[pr.id];
    if (pickedTid !== expectedTid) {
      const customRat = spec.pair_rationales?.[`${pr.id}:${pickedTid}`];
      const target = targetById.get(pickedTid);
      return {
        isCorrect: false,
        matchedDistractorId: target?.distractor_id,
        diagnosticRationale:
          customRat ||
          target?.error_rationale ||
          `La asociación elegida para "${pr.content}" no corresponde a su consecuencia correcta.`,
      };
    }
  }

  return { isCorrect: true };
}
