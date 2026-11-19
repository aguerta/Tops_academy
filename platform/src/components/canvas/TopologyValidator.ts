import * as math from 'mathjs';
import { InvariantCanvasSpec } from '../../types';
import {
  DiagnosticGradingResult,
  evaluateSafePredicate,
  normalizeSymbolicInput,
} from '../../services/symbolicValidator';

export interface CartesianCanvasState {
  sliderValues: Record<string, number>;
  pointPositions: Record<string, { x: number; y: number }>;
  inequalityStyle?: 'solid' | 'dashed';
  inequalityShade?: 'above' | 'below' | 'none';
}

export interface TreeCanvasState {
  selectedEdgeIds: string[];
  infoSets: string[][];
}

export interface CanvasValidationResult extends DiagnosticGradingResult {
  failedInvariants: string[];
}

/**
 * Evaluates a Cartesian curve expression safely via `mathjs` (ZERO `new Function()` or `eval()`).
 * Supports piecewise ternary expressions (`x < 50 ? 200 - 2*x : 150 - x`), `min/max/abs`, and Python `**`.
 */
export function evaluateCartesianExpression(
  expr: string,
  scope: Record<string, number>
): number | null {
  if (!expr || typeof expr !== 'string') return null;
  const clean = expr
    .trim()
    .replace(/\*\*/g, '^')
    .replace(/[\u2212\u2013\u2014]/g, '-')
    .replace(/[×·]/g, '*')
    .replace(/÷/g, '/')
    .replace(/\bln\s*\(/g, 'log(');
  if (!clean) return null;
  try {
    const out = math.evaluate(clean, { ...scope });
    return typeof out === 'number' && Number.isFinite(out) ? out : null;
  } catch {
    try {
      const fallback = normalizeSymbolicInput(clean);
      if (!fallback || fallback === 'SYNTAX_ERROR' || fallback === clean) return null;
      const out = math.evaluate(fallback, { ...scope });
      return typeof out === 'number' && Number.isFinite(out) ? out : null;
    } catch {
      return null;
    }
  }
}

/**
 * Evaluates a curve (fixed or interactive) at `x` under current slider scope.
 */
export function evaluateCurveAtX(
  curveId: string | undefined,
  x: number,
  sliderScope: Record<string, number>,
  spec: InvariantCanvasSpec
): number | null {
  const allCurves = [...(spec.fixed_curves || []), ...(spec.interactive_curves || [])];
  const curve = curveId ? allCurves.find((c) => c.id === curveId) : allCurves[0];
  if (!curve) return null;
  if (Array.isArray(curve.domain) && (x < curve.domain[0] - 1e-9 || x > curve.domain[1] + 1e-9)) {
    return null;
  }
  const rawExpr = curve.expression || curve.fn || '';
  return evaluateCartesianExpression(rawExpr, { ...sliderScope, x });
}

function buildCartesianScope(
  state: CartesianCanvasState,
  spec: InvariantCanvasSpec
): Record<string, number> {
  const scope: Record<string, number> = {};
  for (const sl of spec.sliders || []) {
    scope[sl.id] = state.sliderValues[sl.id] ?? sl.initial ?? (sl.min + sl.max) / 2;
  }
  for (const [k, v] of Object.entries(state.sliderValues || {})) {
    scope[k] = v;
  }
  const points = spec.interactive_points || [];
  for (const pt of points) {
    const pos = state.pointPositions[pt.id] || { x: pt.x, y: pt.y };
    scope[`${pt.id}_x`] = pos.x;
    scope[`${pt.id}_y`] = pos.y;
  }
  if (points.length === 1) {
    const first = state.pointPositions[points[0].id] || { x: points[0].x, y: points[0].y };
    scope.x = first.x;
    scope.y = first.y;
  }
  return scope;
}

function evalTargetNumber(
  rawTarget: number | string | undefined,
  scope: Record<string, number>
): number | null {
  if (rawTarget === undefined || rawTarget === null) return null;
  if (typeof rawTarget === 'number') return Number.isFinite(rawTarget) ? rawTarget : null;
  return evaluateCartesianExpression(String(rawTarget), scope);
}

/**
 * Validates geometric, analytical, piecewise-kink, and parametric invariants on `cartesian` canvas.
 */
export function validateCartesianInvariants(
  state: CartesianCanvasState,
  spec: InvariantCanvasSpec
): CanvasValidationResult {
  const invariants = spec.invariants || [];
  if (invariants.length === 0) {
    return { isCorrect: true, failedInvariants: [] };
  }

  const scope = buildCartesianScope(state, spec);
  const failedInvariants: string[] = [];
  let firstRationale: string | undefined;
  let firstDid: string | undefined;

  for (let idx = 0; idx < invariants.length; idx++) {
    const inv = invariants[idx];
    const invId = inv.id || `INV${idx + 1}`;
    const tol = typeof inv.tolerance === 'number' ? inv.tolerance : 0.25;
    let passed = false;

    const ptPos = inv.point_id ? state.pointPositions[inv.point_id] : undefined;

    switch (inv.kind) {
      case 'point_on_curve': {
        if (ptPos) {
          const yCurve = evaluateCurveAtX(inv.curve_id, ptPos.x, scope, spec);
          if (yCurve !== null && Math.abs(ptPos.y - yCurve) <= tol) {
            passed = true;
          }
        }
        break;
      }

      case 'point_coords': {
        if (ptPos) {
          const tx = evalTargetNumber(inv.target_x, scope);
          const ty = evalTargetNumber(inv.target_y, scope);
          const xOk = tx === null || Math.abs(ptPos.x - tx) <= tol;
          const yOk = ty === null || Math.abs(ptPos.y - ty) <= tol;
          passed = xOk && yOk;
        }
        break;
      }

      case 'slider_eq': {
        if (inv.slider_id) {
          const sVal = scope[inv.slider_id];
          const tVal = evalTargetNumber(
            inv.expr ?? inv.target ?? inv.target_value ?? inv.expected,
            scope
          );
          if (typeof sVal === 'number' && tVal !== null && Math.abs(sVal - tVal) <= tol) {
            passed = true;
          }
        }
        break;
      }

      case 'slider_range': {
        if (inv.slider_id) {
          const sVal = scope[inv.slider_id];
          if (typeof sVal === 'number') {
            const minOk = inv.min === undefined || sVal >= inv.min - tol;
            const maxOk = inv.max === undefined || sVal <= inv.max + tol;
            passed = minOk && maxOk;
          }
        }
        break;
      }

      case 'expr_true': {
        if (inv.expr) {
          try {
            passed = evaluateSafePredicate(inv.expr, scope);
          } catch {
            passed = false;
          }
        }
        break;
      }

      case 'point_in_region': {
        if (inv.expr && ptPos) {
          try {
            passed = evaluateSafePredicate(inv.expr, { ...scope, x: ptPos.x, y: ptPos.y });
          } catch {
            passed = false;
          }
        }
        break;
      }

      case 'curves_intersect_at': {
        const xVal = evalTargetNumber(inv.x ?? inv.target_x, scope);
        if (xVal !== null) {
          const ya = evaluateCurveAtX(inv.curve_a, xVal, scope, spec);
          const yb = evaluateCurveAtX(inv.curve_b, xVal, scope, spec);
          if (ya !== null && yb !== null && Math.abs(ya - yb) <= tol) {
            passed = true;
          }
        }
        break;
      }

      case 'slope_at': {
        const xVal = evalTargetNumber(inv.x ?? inv.target_x, scope);
        const expectedSlope = evalTargetNumber(inv.target ?? inv.expr, scope);
        if (xVal !== null && expectedSlope !== null) {
          const h = 0.01;
          const y1 = evaluateCurveAtX(inv.curve_id, xVal - h, scope, spec);
          const y2 = evaluateCurveAtX(inv.curve_id, xVal + h, scope, spec);
          if (y1 !== null && y2 !== null) {
            const slope = (y2 - y1) / (2 * h);
            if (Math.abs(slope - expectedSlope) <= tol) {
              passed = true;
            }
          }
        }
        break;
      }

      case 'kink_at': {
        const xVal = evalTargetNumber(inv.x ?? inv.target_x, scope);
        if (xVal !== null) {
          const h = 0.02;
          const yMid = evaluateCurveAtX(inv.curve_id, xVal, scope, spec);
          const yLeft = evaluateCurveAtX(inv.curve_id, xVal - h, scope, spec);
          const yRight = evaluateCurveAtX(inv.curve_id, xVal + h, scope, spec);
          if (yMid !== null && yLeft !== null && yRight !== null) {
            const leftSlope = (yMid - yLeft) / h;
            const rightSlope = (yRight - yMid) / h;
            const minJump = typeof inv.target === 'number' ? inv.target : 0.05;
            if (Math.abs(leftSlope - rightSlope) >= minJump) {
              passed = true;
            }
          }
        }
        break;
      }

      case 'inequality_state': {
        const styleOk = !inv.expected_style || state.inequalityStyle === inv.expected_style;
        const shadeOk = !inv.expected_shade || state.inequalityShade === inv.expected_shade;
        passed = styleOk && shadeOk;
        break;
      }
    }

    if (!passed) {
      failedInvariants.push(invId);
      if (!firstRationale && inv.error_rationale) {
        firstRationale = inv.error_rationale;
        firstDid = inv.distractor_id;
      }
    }
  }

  return {
    isCorrect: failedInvariants.length === 0,
    failedInvariants,
    matchedDistractorId: firstDid,
    diagnosticRationale: firstRationale,
  };
}

/**
 * Validates extensive-form decision/game tree invariants:
 * - Selected branch set (`required_edges`)
 * - Equivalence classes for information sets (`required_info_sets`), order-independent
 */
export function validateTreeInvariants(
  state: TreeCanvasState,
  spec: InvariantCanvasSpec
): CanvasValidationResult {
  const ti = spec.tree_invariants || {};
  const mode = spec.interaction_mode || 'both';
  const failedInvariants: string[] = [];
  let firstRationale: string | undefined;
  const did = ti.distractor_id;

  const reqEdges = Array.from(new Set(ti.required_edges || [])).sort();
  if (mode !== 'info_sets' && reqEdges.length > 0) {
    const selEdges = Array.from(new Set(state.selectedEdgeIds || [])).sort();
    const edgesMatch =
      selEdges.length === reqEdges.length && selEdges.every((e, idx) => e === reqEdges[idx]);
    if (!edgesMatch) {
      failedInvariants.push('TREE_EDGES');
      firstRationale =
        ti.edge_error_rationale ||
        'La selección de estrategias o ramas en el árbol no corresponde al equilibrio requerido.';
    }
  }

  const reqInfoSets = (ti.required_info_sets || [])
    .map((grp) => Array.from(new Set(grp)).sort())
    .filter((grp) => grp.length > 0)
    .map((grp) => grp.join(','))
    .sort();

  if (mode !== 'edges' && reqInfoSets.length > 0) {
    const subInfoSets = (state.infoSets || [])
      .map((grp) => Array.from(new Set(grp)).sort())
      .filter((grp) => grp.length > 0)
      .map((grp) => grp.join(','))
      .sort();
    const infoMatch =
      subInfoSets.length === reqInfoSets.length &&
      subInfoSets.every((g, idx) => g === reqInfoSets[idx]);
    if (!infoMatch) {
      failedInvariants.push('TREE_INFO_SETS');
      if (!firstRationale) {
        firstRationale =
          ti.info_set_error_rationale ||
          'Los conjuntos de información trazados no agrupan correctamente los nodos indistinguibles.';
      }
    }
  }

  return {
    isCorrect: failedInvariants.length === 0,
    failedInvariants,
    matchedDistractorId: failedInvariants.length > 0 ? did : undefined,
    diagnosticRationale: firstRationale,
  };
}
