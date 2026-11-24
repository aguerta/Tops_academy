import React, { useId, useRef, useState } from 'react';
import { InvariantCanvasSpec } from '../types';
import { hasRawLatex } from '../utils/latexOptionLabel';
import { evaluateCartesianExpression } from './canvas/TopologyValidator';
import { MathText } from './MathText';

export interface InvariantCanvasAnswerState {
  sliderValues: Record<string, number>;
  pointPositions: Record<string, { x: number; y: number }>;
  selectedEdgeIds: string[];
  infoSets: string[][];
  inequalityStyle?: 'solid' | 'dashed';
  inequalityShade?: 'above' | 'below' | 'none';
}

interface InvariantCanvasProps {
  spec: InvariantCanvasSpec;
  value: InvariantCanvasAnswerState;
  disabled?: boolean;
  onChange: (next: InvariantCanvasAnswerState) => void;
}

function buildInitialCartesianState(spec: InvariantCanvasSpec): InvariantCanvasAnswerState {
  const sliderValues: Record<string, number> = {};
  for (const sl of spec.sliders || []) {
    sliderValues[sl.id] = sl.initial ?? (sl.min + sl.max) / 2;
  }
  const pointPositions: Record<string, { x: number; y: number }> = {};
  for (const pt of spec.interactive_points || []) {
    pointPositions[pt.id] = { x: pt.x, y: pt.y };
  }
  return {
    sliderValues,
    pointPositions,
    selectedEdgeIds: [],
    infoSets: [],
    inequalityStyle: spec.inequality?.initial_style ?? 'solid',
    inequalityShade: spec.inequality?.initial_shade ?? 'above',
  };
}

function evalNumExpr(raw: number | string | undefined, scope: Record<string, number>): number | null {
  if (raw === undefined || raw === null) return null;
  if (typeof raw === 'number') return Number.isFinite(raw) ? raw : null;
  return evaluateCartesianExpression(String(raw), scope);
}

function computeNiceTicks(minVal: number, maxVal: number, preferredStep?: number): number[] {
  const span = Math.max(1e-6, maxVal - minVal);
  let tickStep = preferredStep && preferredStep > 0 ? preferredStep : Math.max(1, Math.round(span / 10));
  while (span / tickStep > 18) {
    tickStep *= 2;
  }
  const ticks: number[] = [];
  const start = Math.ceil(minVal / tickStep - 1e-9) * tickStep;
  for (let t = start; t <= maxVal + 1e-9; t += tickStep) {
    ticks.push(Number(t.toFixed(4)));
  }
  return ticks;
}

export const InvariantCanvas: React.FC<InvariantCanvasProps> = ({
  spec,
  value,
  disabled = false,
  onChange,
}) => {
  const uid = useId().replace(/:/g, '');
  const svgRef = useRef<SVGSVGElement>(null);
  const [draggingPointId, setDraggingPointId] = useState<string | null>(null);
  const [focusedPointId, setFocusedPointId] = useState<string | null>(null);
  const [draftGroupNodes, setDraftGroupNodes] = useState<string[]>([]);

  if (spec.mode === 'tree') {
    const W = spec.width || 520;
    const H = spec.height || 320;
    const nodes = spec.nodes || [];
    const edges = spec.edges || [];
    const nodeById = new Map(nodes.map((n) => [n.id, n]));
    const interactionMode = spec.interaction_mode || 'both';
    const selectedSet = new Set(value.selectedEdgeIds || []);

    const toggleEdge = (eid: string) => {
      if (disabled || interactionMode === 'info_sets') return;
      const next = selectedSet.has(eid)
        ? value.selectedEdgeIds.filter((x) => x !== eid)
        : [...value.selectedEdgeIds, eid];
      onChange({ ...value, selectedEdgeIds: next });
    };

    const toggleDraftNode = (nid: string) => {
      if (disabled || interactionMode === 'edges') return;
      setDraftGroupNodes((prev) =>
        prev.includes(nid) ? prev.filter((x) => x !== nid) : [...prev, nid]
      );
    };

    const commitInfoSet = () => {
      if (disabled || draftGroupNodes.length < 2) return;
      const sortedNew = Array.from(new Set(draftGroupNodes)).sort();
      const key = sortedNew.join(',');
      const exists = (value.infoSets || []).some(
        (grp) => grp.toSorted().join(',') === key
      );
      if (!exists) {
        onChange({ ...value, infoSets: [...(value.infoSets || []), sortedNew] });
      }
      setDraftGroupNodes([]);
    };

    const removeInfoSet = (idx: number) => {
      if (disabled) return;
      onChange({
        ...value,
        infoSets: (value.infoSets || []).filter((_, i) => i !== idx),
      });
    };

    return (
      <div data-testid="invariant-canvas-root" className="space-y-3 max-w-2xl">
        <div className="p-2 bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
          <svg
            data-testid="invariant-canvas-svg"
            viewBox={`0 0 ${W} ${H}`}
            className="w-full h-auto block select-none"
            role="img"
            aria-label="Árbol interactivo de decisión"
          >
            {/* Dashed Information-Set Ovals */}
            {(value.infoSets || []).map((grp, idx) => {
              const pts = grp.map((nid) => nodeById.get(nid)).filter(Boolean);
              if (pts.length === 0) return null;
              const xs = pts.map((p) => p!.x);
              const ys = pts.map((p) => p!.y);
              const minX = Math.min(...xs) - 24;
              const maxX = Math.max(...xs) + 24;
              const minY = Math.min(...ys) - 22;
              const maxY = Math.max(...ys) + 22;
              return (
                <rect
                  key={`is-${idx}`}
                  data-testid={`tree-infoset-${idx}`}
                  x={minX}
                  y={minY}
                  width={Math.max(40, maxX - minX)}
                  height={Math.max(40, maxY - minY)}
                  rx={18}
                  fill="rgba(24, 101, 242, 0.08)"
                  stroke="#1865f2"
                  strokeWidth={2}
                  strokeDasharray="6 4"
                />
              );
            })}

            {/* Clickable Tree Edges (wide invisible hit target + visual stroke) */}
            {edges.map((ed) => {
              const nFrom = nodeById.get(ed.from);
              const nTo = nodeById.get(ed.to);
              if (!nFrom || !nTo) return null;
              const isSel = selectedSet.has(ed.id);
              const mx = (nFrom.x + nTo.x) / 2;
              const my = (nFrom.y + nTo.y) / 2;
              return (
                <g
                  key={ed.id}
                  data-testid={`tree-edge-${ed.id}`}
                  onClick={() => toggleEdge(ed.id)}
                  className={interactionMode !== 'info_sets' && !disabled ? 'cursor-pointer' : ''}
                >
                  <line
                    x1={nFrom.x}
                    y1={nFrom.y}
                    x2={nTo.x}
                    y2={nTo.y}
                    stroke="transparent"
                    strokeWidth={16}
                  />
                  <line
                    x1={nFrom.x}
                    y1={nFrom.y}
                    x2={nTo.x}
                    y2={nTo.y}
                    stroke={isSel ? '#1865f2' : '#94a3b8'}
                    strokeWidth={isSel ? 4 : 2}
                    strokeLinecap="round"
                  />
                  {ed.label && (
                    hasRawLatex(ed.label) ? (
                      <foreignObject
                        x={mx - 70}
                        y={my - 26}
                        width={140}
                        height={24}
                        className="overflow-visible pointer-events-none"
                      >
                        <div
                          className={`text-[11px] text-center leading-tight px-1 rounded bg-white/85 ${
                            isSel ? 'font-bold text-ka-blue' : 'font-medium text-slate-700'
                          }`}
                        >
                          <MathText text={ed.label} inline />
                        </div>
                      </foreignObject>
                    ) : (
                      <text
                        x={mx}
                        y={my - 7}
                        textAnchor="middle"
                        fontSize={12}
                        fontWeight={isSel ? 700 : 500}
                        fill={isSel ? '#1865f2' : '#334155'}
                      >
                        {ed.label}
                      </text>
                    )
                  )}
                </g>
              );
            })}

            {/* Decision / Terminal Nodes */}
            {nodes.map((nd) => {
              const inDraft = draftGroupNodes.includes(nd.id);
              const nodeLabel = nd.label || nd.id;
              return (
                <g
                  key={nd.id}
                  data-testid={`tree-node-${nd.id}`}
                  onClick={() => !nd.terminal && toggleDraftNode(nd.id)}
                  className={!nd.terminal && interactionMode !== 'edges' && !disabled ? 'cursor-pointer' : ''}
                >
                  <circle
                    cx={nd.x}
                    cy={nd.y}
                    r={nd.terminal ? 8 : 14}
                    fill={inDraft ? '#dbeafe' : nd.terminal ? '#f8fafc' : '#ffffff'}
                    stroke={inDraft ? '#1865f2' : '#0f172a'}
                    strokeWidth={inDraft ? 3 : 2}
                  />
                  {hasRawLatex(nodeLabel) ? (
                    <foreignObject
                      x={nd.x - 65}
                      y={nd.terminal ? nd.y + 8 : nd.y - 12}
                      width={130}
                      height={24}
                      className="overflow-visible pointer-events-none"
                    >
                      <div className="text-[11px] font-bold text-slate-900 text-center leading-tight">
                        <MathText text={nodeLabel} inline />
                      </div>
                    </foreignObject>
                  ) : (
                    <text
                      x={nd.x}
                      y={nd.y + (nd.terminal ? 20 : 4)}
                      textAnchor="middle"
                      fontSize={11}
                      fontWeight={700}
                      fill="#0f172a"
                    >
                      {nodeLabel}
                    </text>
                  )}
                  {nd.payoff && (
                    hasRawLatex(nd.payoff) ? (
                      <foreignObject
                        x={nd.x - 65}
                        y={nd.y + 22}
                        width={130}
                        height={24}
                        className="overflow-visible pointer-events-none"
                      >
                        <div className="text-[11px] text-slate-600 text-center leading-tight">
                          <MathText text={nd.payoff} inline />
                        </div>
                      </foreignObject>
                    ) : (
                      <text
                        x={nd.x}
                        y={nd.y + 34}
                        textAnchor="middle"
                        fontSize={11}
                        fill="#475569"
                      >
                        {nd.payoff}
                      </text>
                    )
                  )}
                </g>
              );
            })}
          </svg>
        </div>

        {/* Accessible Controls for Branches & Information Sets */}
        <div className="flex flex-wrap gap-3 text-xs">
          {interactionMode !== 'info_sets' && (
            <div className="flex-1 min-w-[200px] p-2.5 bg-slate-50 border border-slate-200 rounded-lg space-y-1.5">
              <div className="font-bold text-slate-700">Ramas / Acciones seleccionadas:</div>
              <div className="flex flex-wrap gap-1.5">
                {edges.map((ed) => {
                  const isSel = selectedSet.has(ed.id);
                  return (
                    <button
                      key={ed.id}
                      type="button"
                      disabled={disabled}
                      data-testid={`tree-edge-btn-${ed.id}`}
                      onClick={() => toggleEdge(ed.id)}
                      className={`px-2.5 py-1 rounded border font-semibold cursor-pointer ${
                        isSel
                          ? 'bg-ka-blue text-white border-ka-blue'
                          : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-100'
                      }`}
                    >
                      <MathText text={ed.label || ed.id} inline /> ({ed.from}→{ed.to})
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {interactionMode !== 'edges' && (
            <div className="flex-1 min-w-[220px] p-2.5 bg-slate-50 border border-slate-200 rounded-lg space-y-2">
              <div className="font-bold text-slate-700">Conjuntos de información:</div>
              <div className="flex flex-wrap items-center gap-1.5">
                {nodes
                  .filter((nd) => !nd.terminal)
                  .map((nd) => {
                    const active = draftGroupNodes.includes(nd.id);
                    return (
                      <button
                        key={nd.id}
                        type="button"
                        disabled={disabled}
                        data-testid={`tree-node-toggle-${nd.id}`}
                        onClick={() => toggleDraftNode(nd.id)}
                        className={`px-2 py-1 rounded border font-semibold cursor-pointer ${
                          active
                            ? 'bg-indigo-600 text-white border-indigo-600'
                            : 'bg-white text-slate-700 border-slate-300'
                        }`}
                      >
                        <MathText text={nd.label || nd.id} inline />
                      </button>
                    );
                  })}
                <button
                  type="button"
                  disabled={disabled || draftGroupNodes.length < 2}
                  data-testid="tree-create-infoset-btn"
                  onClick={commitInfoSet}
                  className="px-2.5 py-1 rounded bg-ka-blue text-white font-bold disabled:opacity-40 cursor-pointer"
                >
                  + Agrupar
                </button>
              </div>
              {(value.infoSets || []).length > 0 && (
                <div className="flex flex-wrap gap-1.5">
                  {(value.infoSets || []).map((grp, idx) => (
                    <span
                      key={idx}
                      className="inline-flex items-center gap-1 px-2 py-0.5 bg-blue-100 text-blue-900 rounded-full font-mono"
                    >
                      {'{' + grp.join(', ') + '}'}
                      <button
                        type="button"
                        disabled={disabled}
                        data-testid={`tree-remove-infoset-${idx}`}
                        onClick={() => removeInfoSet(idx)}
                        className="text-rose-700 font-bold cursor-pointer ml-1"
                        aria-label="Eliminar conjunto"
                      >
                        ×
                      </button>
                    </span>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    );
  }

  // mode === 'cartesian'
  const W = spec.width || 540;
  const H = spec.height || 340;
  const PAD = 38;
  const [xMin, xMax] = spec.x_range || [0, 100];
  const [yMin, yMax] = spec.y_range || [0, 220];
  const ySpan = Math.max(1e-6, yMax - yMin);
  const defaultSnap = spec.snap ?? 0.5;

  const toSvgX = (x: number) => PAD + ((x - xMin) / Math.max(1e-9, xMax - xMin)) * (W - 2 * PAD);
  const toSvgY = (y: number) => H - PAD - ((y - yMin) / Math.max(1e-9, yMax - yMin)) * (H - 2 * PAD);
  const toMathX = (sx: number) => xMin + ((sx - PAD) / Math.max(1e-9, W - 2 * PAD)) * (xMax - xMin);
  const toMathY = (sy: number) => yMin + ((H - PAD - sy) / Math.max(1e-9, H - 2 * PAD)) * (yMax - yMin);

  const hasZeroX = xMin <= 0 && xMax >= 0;
  const hasZeroY = yMin <= 0 && yMax >= 0;
  const yAxisSvgX = hasZeroX ? toSvgX(0) : PAD;
  const xAxisSvgY = hasZeroY ? toSvgY(0) : H - PAD;

  // Unified scope combining sliders + interactive control point coordinates
  const evalScope: Record<string, number> = {};
  for (const sl of spec.sliders || []) {
    evalScope[sl.id] = value.sliderValues[sl.id] ?? sl.initial ?? (sl.min + sl.max) / 2;
  }
  for (const [k, v] of Object.entries(value.sliderValues || {})) {
    evalScope[k] = v;
  }
  const interPts = spec.interactive_points || [];
  for (const pt of interPts) {
    const pos = value.pointPositions[pt.id] || { x: pt.x, y: pt.y };
    evalScope[`${pt.id}_x`] = pos.x;
    evalScope[`${pt.id}_y`] = pos.y;
  }
  if (interPts.length === 1) {
    const p0 = value.pointPositions[interPts[0].id] || { x: interPts[0].x, y: interPts[0].y };
    evalScope.x = p0.x;
    evalScope.y = p0.y;
  }

  const allCurves = [...(spec.fixed_curves || []), ...(spec.interactive_curves || [])];
  const curveById = new Map(allCurves.filter((c) => c.id).map((c) => [c.id!, c]));

  const buildCurvePaths = (expr: string, domain?: [number, number]) => {
    const dMin = domain ? Math.max(xMin, domain[0]) : xMin;
    const dMax = domain ? Math.min(xMax, domain[1]) : xMax;
    const samples = 200;
    const segments: string[] = [];
    let activeCmd = '';
    let prevY: number | null = null;
    for (let i = 0; i <= samples; i++) {
      const x = dMin + (i / samples) * (dMax - dMin);
      const y = evaluateCartesianExpression(expr, { ...evalScope, x });
      if (y === null || y < yMin - ySpan * 2 || y > yMax + ySpan * 2) {
        if (activeCmd) {
          segments.push(activeCmd);
          activeCmd = '';
        }
        prevY = null;
        continue;
      }
      if (prevY !== null && Math.abs(y - prevY) > ySpan * 1.4) {
        if (activeCmd) {
          segments.push(activeCmd);
          activeCmd = '';
        }
      }
      const sx = toSvgX(x).toFixed(1);
      const sy = toSvgY(y).toFixed(1);
      activeCmd += activeCmd ? ` L ${sx} ${sy}` : `M ${sx} ${sy}`;
      prevY = y;
    }
    if (activeCmd) segments.push(activeCmd);
    return segments;
  };

  const ineqStyle: 'solid' | 'dashed' =
    value.inequalityStyle ?? spec.inequality?.initial_style ?? 'solid';
  const ineqShade: 'above' | 'below' | 'none' =
    value.inequalityShade ?? spec.inequality?.initial_shade ?? 'above';

  const buildHalfPlanePath = (curveId: string, side: 'above' | 'below') => {
    const cv = curveById.get(curveId);
    const expr = cv?.expression || cv?.fn;
    if (!expr) return '';
    const dMin = cv?.domain ? Math.max(xMin, cv.domain[0]) : xMin;
    const dMax = cv?.domain ? Math.min(xMax, cv.domain[1]) : xMax;
    const edgePts: Array<[number, number]> = [];
    const samples = 90;
    for (let i = 0; i <= samples; i++) {
      const x = dMin + (i / samples) * (dMax - dMin);
      const y = evaluateCartesianExpression(expr, { ...evalScope, x });
      if (y !== null) {
        const clampedY = Math.max(yMin - ySpan * 0.25, Math.min(yMax + ySpan * 0.25, y));
        edgePts.push([toSvgX(x), toSvgY(clampedY)]);
      }
    }
    if (edgePts.length < 2) return '';
    const boundY = side === 'above' ? toSvgY(yMax + ySpan * 0.2) : toSvgY(yMin - ySpan * 0.2);
    const firstX = edgePts[0][0].toFixed(1);
    const lastX = edgePts[edgePts.length - 1][0].toFixed(1);
    const lineCmd = edgePts.map(([sx, sy], idx) => `${idx === 0 ? 'M' : 'L'} ${sx.toFixed(1)} ${sy.toFixed(1)}`).join(' ');
    return `${lineCmd} L ${lastX} ${boundY.toFixed(1)} L ${firstX} ${boundY.toFixed(1)} Z`;
  };

  const buildShadedBandPath = (
    topCurveId: string | undefined,
    botCurveId: string | undefined,
    topConst: number | string | undefined,
    botConst: number | string | undefined,
    domain?: [number | string, number | string]
  ) => {
    const d0 = domain ? (evalNumExpr(domain[0], evalScope) ?? xMin) : xMin;
    const d1 = domain ? (evalNumExpr(domain[1], evalScope) ?? xMax) : xMax;
    const dMin = Math.max(xMin, Math.min(d0, d1));
    const dMax = Math.min(xMax, Math.max(d0, d1));
    if (dMax - dMin <= 1e-6) return '';
    const topCv = topCurveId ? curveById.get(topCurveId) : undefined;
    const botCv = botCurveId ? curveById.get(botCurveId) : undefined;
    const topExpr = topCv?.expression || topCv?.fn;
    const botExpr = botCv?.expression || botCv?.fn;
    const topPts: Array<[number, number]> = [];
    const botPts: Array<[number, number]> = [];
    const samples = 72;
    for (let i = 0; i <= samples; i++) {
      const x = dMin + (i / samples) * (dMax - dMin);
      const localScope = { ...evalScope, x };
      const yt = topExpr ? evaluateCartesianExpression(topExpr, localScope) : evalNumExpr(topConst, localScope);
      const yb = botExpr ? evaluateCartesianExpression(botExpr, localScope) : evalNumExpr(botConst, localScope);
      if (yt !== null && yb !== null) {
        topPts.push([toSvgX(x), toSvgY(yt)]);
        botPts.push([toSvgX(x), toSvgY(yb)]);
      }
    }
    if (topPts.length < 2) return '';
    const fwd = topPts.map(([sx, sy], idx) => `${idx === 0 ? 'M' : 'L'} ${sx.toFixed(1)} ${sy.toFixed(1)}`).join(' ');
    const rev = botPts.toReversed().map(([sx, sy]) => `L ${sx.toFixed(1)} ${sy.toFixed(1)}`).join(' ');
    return `${fwd} ${rev} Z`;
  };

  const clampAndSnap = (rawVal: number, minV: number, maxV: number, inc: number) => {
    const snapped = Math.round(rawVal / inc) * inc;
    return Math.min(maxV, Math.max(minV, Number(snapped.toFixed(3))));
  };

  const movePointByDelta = (ptId: string, dx: number, dy: number) => {
    if (disabled) return;
    const ptSpec = interPts.find((p) => p.id === ptId);
    if (!ptSpec) return;
    const inc = ptSpec.snap ?? defaultSnap;
    const cur = value.pointPositions[ptSpec.id] || { x: ptSpec.x, y: ptSpec.y };
    const nextX = ptSpec.lock_x ? cur.x : clampAndSnap(cur.x + dx * inc, ptSpec.min_x ?? xMin, ptSpec.max_x ?? xMax, inc);
    const nextY = ptSpec.lock_y ? cur.y : clampAndSnap(cur.y + dy * inc, ptSpec.min_y ?? yMin, ptSpec.max_y ?? yMax, inc);
    onChange({
      ...value,
      pointPositions: { ...value.pointPositions, [ptSpec.id]: { x: nextX, y: nextY } },
    });
  };

  const handleSvgPointerMove = (e: React.PointerEvent<SVGSVGElement>) => {
    if (!draggingPointId || disabled || !svgRef.current) return;
    const ptSpec = interPts.find((p) => p.id === draggingPointId);
    if (!ptSpec) return;
    const inc = ptSpec.snap ?? defaultSnap;
    const rect = svgRef.current.getBoundingClientRect();
    const sx = ((e.clientX - rect.left) / Math.max(1, rect.width)) * W;
    const sy = ((e.clientY - rect.top) / Math.max(1, rect.height)) * H;
    const nextX = ptSpec.lock_x
      ? (value.pointPositions[ptSpec.id]?.x ?? ptSpec.x)
      : clampAndSnap(toMathX(sx), ptSpec.min_x ?? xMin, ptSpec.max_x ?? xMax, inc);
    const nextY = ptSpec.lock_y
      ? (value.pointPositions[ptSpec.id]?.y ?? ptSpec.y)
      : clampAndSnap(toMathY(sy), ptSpec.min_y ?? yMin, ptSpec.max_y ?? yMax, inc);
    onChange({
      ...value,
      pointPositions: {
        ...value.pointPositions,
        [ptSpec.id]: { x: nextX, y: nextY },
      },
    });
  };

  const toggleIneqStyle = () => {
    if (disabled || !spec.inequality) return;
    onChange({ ...value, inequalityStyle: ineqStyle === 'solid' ? 'dashed' : 'solid' });
  };

  const toggleIneqShade = () => {
    if (disabled || !spec.inequality) return;
    onChange({ ...value, inequalityShade: ineqShade === 'above' ? 'below' : 'above' });
  };

  const xTicks = computeNiceTicks(xMin, xMax, spec.step);
  const yTicks = computeNiceTicks(yMin, yMax, spec.step && xMax - xMin === yMax - yMin ? spec.step : undefined);
  const clipId = `ic-clip-${uid}`;
  const arrowId = `ic-arrow-${uid}`;
  const activePointId = draggingPointId || focusedPointId;

  const legendItems: Array<{ key: string; label: string; color: string; dashed?: boolean; fill?: string }> = [];
  allCurves.forEach((cv, idx) => {
    if (cv.label) {
      const isIneqBoundary = spec.inequality?.curve_id && cv.id === spec.inequality.curve_id;
      legendItems.push({
        key: `cv-${cv.id || idx}`,
        label: cv.label,
        color: cv.color || (idx === 0 ? '#1865f2' : '#0f766e'),
        dashed: isIneqBoundary ? ineqStyle === 'dashed' : cv.style === 'dashed',
      });
    }
  });
  (spec.polygons || []).forEach((pg, idx) => {
    if (pg.label) {
      legendItems.push({
        key: `pg-${pg.id || idx}`,
        label: pg.label,
        color: pg.stroke || '#059669',
        fill: pg.fill || 'rgba(16, 185, 129, 0.25)',
      });
    }
  });
  (spec.shaded_regions || []).forEach((sr, idx) => {
    if (sr.label) {
      legendItems.push({
        key: `sr-${sr.id || idx}`,
        label: sr.label,
        color: '#1865f2',
        fill: sr.fill || 'rgba(24, 101, 242, 0.22)',
      });
    }
  });

  return (
    <div data-testid="invariant-canvas-root" className="space-y-3 max-w-2xl">
      <div className="p-2 bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
        <svg
          ref={svgRef}
          data-testid="invariant-canvas-svg"
          viewBox={`0 0 ${W} ${H}`}
          className="w-full h-auto block touch-none select-none"
          role="img"
          aria-label="Plano cartesiano interactivo"
          onPointerMove={handleSvgPointerMove}
          onPointerUp={() => setDraggingPointId(null)}
          onPointerCancel={() => setDraggingPointId(null)}
          onPointerLeave={() => setDraggingPointId(null)}
        >
          <defs>
            <clipPath id={clipId}>
              <rect x={PAD} y={PAD} width={W - 2 * PAD} height={H - 2 * PAD} />
            </clipPath>
            <marker
              id={arrowId}
              viewBox="0 0 10 10"
              refX="7"
              refY="5"
              markerWidth="6"
              markerHeight="6"
              orient="auto-start-reverse"
            >
              <path d="M 0 1.5 L 8.5 5 L 0 8.5 z" fill="#334155" />
            </marker>
          </defs>

          {/* Grid Lines */}
          {xTicks.map((gx) => (
            <line
              key={`gx-${gx}`}
              x1={toSvgX(gx)}
              y1={PAD}
              x2={toSvgX(gx)}
              y2={H - PAD}
              stroke={Math.abs(gx) < 1e-9 ? '#cbd5e1' : '#e2e8f0'}
              strokeWidth={1}
            />
          ))}
          {yTicks.map((gy) => (
            <line
              key={`gy-${gy}`}
              x1={PAD}
              y1={toSvgY(gy)}
              x2={W - PAD}
              y2={toSvgY(gy)}
              stroke={Math.abs(gy) < 1e-9 ? '#cbd5e1' : '#e2e8f0'}
              strokeWidth={1}
            />
          ))}

          {/* Clipped Graphic Layer: Shaded Regions, Inequality Half-Plane, Polygons, Segments & Curves */}
          <g clipPath={`url(#${clipId})`}>
            {/* Explicit Shaded Regions */}
            {(spec.shaded_regions || []).map((sr, idx) => {
              const d = buildShadedBandPath(sr.curve_top, sr.curve_bottom, sr.y_top, sr.y_bottom, sr.domain);
              if (!d) return null;
              return (
                <path
                  key={`sr-${sr.id || idx}`}
                  data-testid={sr.id ? `canvas-region-${sr.id}` : undefined}
                  d={d}
                  fill={sr.fill || 'rgba(24, 101, 242, 0.16)'}
                />
              );
            })}

            {/* Inequality Half-Plane Shade */}
            {spec.inequality && ineqShade !== 'none' && (
              <path
                data-testid="canvas-inequality-shade"
                d={buildHalfPlanePath(spec.inequality.curve_id, ineqShade)}
                fill={spec.inequality.color || 'rgba(24, 101, 242, 0.16)'}
              />
            )}

            {/* Dynamic Polygons (Triangles, Surplus Areas, Geometric Shapes) */}
            {(spec.polygons || []).map((pg, idx) => {
              const pts = (pg.vertices || [])
                .map(([vx, vy]) => {
                  const nx = evalNumExpr(vx, evalScope);
                  const ny = evalNumExpr(vy, evalScope);
                  return nx !== null && ny !== null ? `${toSvgX(nx).toFixed(1)},${toSvgY(ny).toFixed(1)}` : null;
                })
                .filter(Boolean) as string[];
              if (pts.length < 3 || pts.length !== (pg.vertices || []).length) return null;
              return (
                <polygon
                  key={`pg-${pg.id || idx}`}
                  data-testid={pg.id ? `canvas-polygon-${pg.id}` : undefined}
                  points={pts.join(' ')}
                  fill={pg.fill || 'rgba(16, 185, 129, 0.18)'}
                  stroke={pg.stroke || '#059669'}
                  strokeWidth={2}
                  strokeLinejoin="round"
                />
              );
            })}

            {/* Segments & Asymptotes */}
            {(spec.segments || []).map((seg, idx) => {
              const fx = evalNumExpr(seg.from?.[0], evalScope);
              const fy = evalNumExpr(seg.from?.[1], evalScope);
              const tx = evalNumExpr(seg.to?.[0], evalScope);
              const ty = evalNumExpr(seg.to?.[1], evalScope);
              if (fx === null || fy === null || tx === null || ty === null) return null;
              return (
                <g key={`seg-${seg.id || idx}`}>
                  <line
                    x1={toSvgX(fx)}
                    y1={toSvgY(fy)}
                    x2={toSvgX(tx)}
                    y2={toSvgY(ty)}
                    stroke={seg.color || '#64748b'}
                    strokeWidth={2}
                    strokeDasharray={seg.style === 'dashed' ? '6 4' : undefined}
                  />
                  {seg.label && (
                    <text
                      x={(toSvgX(fx) + toSvgX(tx)) / 2 + 6}
                      y={(toSvgY(fy) + toSvgY(ty)) / 2 - 6}
                      fontSize={10}
                      fontWeight={600}
                      fill={seg.color || '#475569'}
                    >
                      {seg.label}
                    </text>
                  )}
                </g>
              );
            })}

            {/* Fixed & Interactive Curves */}
            {allCurves.map((cv, cIdx) => {
              const expr = cv.expression || cv.fn || '';
              const segs = buildCurvePaths(expr, cv.domain);
              const stroke = cv.color || (cIdx === 0 ? '#1865f2' : '#0f766e');
              const isIneqBoundary = Boolean(spec.inequality?.curve_id && cv.id === spec.inequality.curve_id);
              const dashPattern = isIneqBoundary
                ? ineqStyle === 'dashed'
                  ? '8 5'
                  : undefined
                : cv.style === 'dashed'
                  ? '6 4'
                  : undefined;

              return segs.map((d, sIdx) => (
                <g key={`cv-${cv.id || cIdx}-${sIdx}`}>
                  {isIneqBoundary && !disabled && (
                    <path
                      d={d}
                      fill="none"
                      stroke="transparent"
                      strokeWidth={16}
                      className="cursor-pointer"
                      onClick={toggleIneqStyle}
                    />
                  )}
                  <path
                    data-testid={cv.id && sIdx === 0 ? `canvas-curve-${cv.id}` : undefined}
                    d={d}
                    fill="none"
                    stroke={stroke}
                    strokeWidth={2.75}
                    strokeLinecap="round"
                    strokeDasharray={dashPattern}
                    className={isIneqBoundary && !disabled ? 'cursor-pointer' : undefined}
                    onClick={isIneqBoundary ? toggleIneqStyle : undefined}
                  />
                </g>
              ));
            })}

            {/* Active Drag/Focus Crosshair Guide Lines */}
            {activePointId && (() => {
              const pt = interPts.find((p) => p.id === activePointId);
              if (!pt) return null;
              const pos = value.pointPositions[pt.id] || { x: pt.x, y: pt.y };
              const sx = toSvgX(pos.x);
              const sy = toSvgY(pos.y);
              const col = pt.color || '#1865f2';
              return (
                <g opacity={0.55} pointerEvents="none">
                  <line x1={sx} y1={sy} x2={sx} y2={xAxisSvgY} stroke={col} strokeWidth={1.25} strokeDasharray="4 3" />
                  <line x1={sx} y1={sy} x2={yAxisSvgX} y2={sy} stroke={col} strokeWidth={1.25} strokeDasharray="4 3" />
                </g>
              );
            })()}
          </g>

          {/* Axes Passing Through Origin (when in range) with Directional Arrows & Ticks */}
          <line
            x1={PAD}
            y1={xAxisSvgY}
            x2={W - PAD}
            y2={xAxisSvgY}
            stroke="#334155"
            strokeWidth={1.6}
            markerEnd={`url(#${arrowId})`}
            markerStart={xMin < 0 ? `url(#${arrowId})` : undefined}
          />
          <line
            x1={yAxisSvgX}
            y1={H - PAD}
            x2={yAxisSvgX}
            y2={PAD}
            stroke="#334155"
            strokeWidth={1.6}
            markerEnd={`url(#${arrowId})`}
            markerStart={yMin < 0 ? `url(#${arrowId})` : undefined}
          />

          {/* Tick Labels along Axes */}
          {xTicks.map((gx) => {
            if (hasZeroX && hasZeroY && Math.abs(gx) < 1e-9) return null;
            const ly = Math.min(H - 12, xAxisSvgY + 14);
            return (
              <text key={`tx-${gx}`} x={toSvgX(gx)} y={ly} textAnchor="middle" fontSize={10} fill="#64748b">
                {gx}
              </text>
            );
          })}
          {yTicks.map((gy) => {
            if (hasZeroX && hasZeroY && Math.abs(gy) < 1e-9) return null;
            const lx = yAxisSvgX > PAD + 20 ? yAxisSvgX - 6 : PAD - 6;
            return (
              <text key={`ty-${gy}`} x={lx} y={toSvgY(gy) + 3.5} textAnchor="end" fontSize={10} fill="#64748b">
                {gy}
              </text>
            );
          })}
          {hasZeroX && hasZeroY && (
            <text x={yAxisSvgX - 6} y={Math.min(H - 12, xAxisSvgY + 14)} textAnchor="end" fontSize={10} fill="#64748b">
              0
            </text>
          )}

          {/* Axis Variable Labels */}
          <text
            x={W - PAD + 4}
            y={Math.max(PAD + 12, xAxisSvgY - 8)}
            textAnchor="end"
            fontSize={11}
            fontWeight={700}
            fill="#1e293b"
          >
            {spec.x_label || 'x'}
          </text>
          <text
            x={Math.min(W - PAD - 12, yAxisSvgX + 10)}
            y={PAD + 6}
            textAnchor="start"
            fontSize={11}
            fontWeight={700}
            fill="#1e293b"
          >
            {spec.y_label || 'y'}
          </text>

          {/* Fixed Non-Draggable Reference Points */}
          {(spec.fixed_points || []).map((fp, idx) => {
            const fx = evalNumExpr(fp.x, evalScope);
            const fy = evalNumExpr(fp.y, evalScope);
            if (fx === null || fy === null) return null;
            const sx = toSvgX(fx);
            const sy = toSvgY(fy);
            const color = fp.color || '#334155';
            const placeLeft = sx > W - PAD - 70;
            return (
              <g key={`fp-${fp.id || idx}`} pointerEvents="none">
                <circle
                  cx={sx}
                  cy={sy}
                  r={5}
                  fill={fp.style === 'open' ? '#ffffff' : color}
                  stroke={color}
                  strokeWidth={2}
                />
                {fp.label && (
                  <text
                    x={placeLeft ? sx - 8 : sx + 8}
                    y={sy - 7}
                    textAnchor={placeLeft ? 'end' : 'start'}
                    fontSize={10.5}
                    fontWeight={700}
                    fill="#1e293b"
                  >
                    {fp.label}
                  </text>
                )}
              </g>
            );
          })}

          {/* Draggable Mafs-Style Control Handles */}
          {interPts.map((pt) => {
            const pos = value.pointPositions[pt.id] || { x: pt.x, y: pt.y };
            const sx = toSvgX(pos.x);
            const sy = toSvgY(pos.y);
            const col = pt.color || '#1865f2';
            const isHot = draggingPointId === pt.id || focusedPointId === pt.id;
            const placeLeft = sx > W - PAD - 95;
            const placeBelow = sy < PAD + 26;
            return (
              <g
                key={pt.id}
                data-testid={`canvas-point-${pt.id}`}
                tabIndex={disabled ? -1 : 0}
                role="slider"
                aria-label={`${pt.label || pt.id}: x=${pos.x}, y=${pos.y}`}
                onPointerDown={(e) => {
                  if (disabled) return;
                  svgRef.current?.setPointerCapture?.(e.pointerId);
                  setDraggingPointId(pt.id);
                }}
                onPointerEnter={() => setFocusedPointId(pt.id)}
                onPointerLeave={() => {
                  if (focusedPointId === pt.id) setFocusedPointId(null);
                }}
                onFocus={() => setFocusedPointId(pt.id)}
                onBlur={() => {
                  if (focusedPointId === pt.id) setFocusedPointId(null);
                }}
                onKeyDown={(e) => {
                  if (disabled) return;
                  if (e.key === 'ArrowRight') { e.preventDefault(); movePointByDelta(pt.id, 1, 0); }
                  else if (e.key === 'ArrowLeft') { e.preventDefault(); movePointByDelta(pt.id, -1, 0); }
                  else if (e.key === 'ArrowUp') { e.preventDefault(); movePointByDelta(pt.id, 0, 1); }
                  else if (e.key === 'ArrowDown') { e.preventDefault(); movePointByDelta(pt.id, 0, -1); }
                }}
                className={disabled ? 'outline-none' : 'cursor-grab active:cursor-grabbing outline-none'}
              >
                <circle
                  cx={sx}
                  cy={sy}
                  r={isHot ? 16 : 12}
                  fill={col}
                  fillOpacity={isHot ? 0.22 : 0.1}
                />
                <circle
                  cx={sx}
                  cy={sy}
                  r={7.5}
                  fill={col}
                  stroke="#ffffff"
                  strokeWidth={2.5}
                />
                <text
                  x={placeLeft ? sx - 12 : sx + 12}
                  y={placeBelow ? sy + 18 : sy - 10}
                  textAnchor={placeLeft ? 'end' : 'start'}
                  fontSize={11}
                  fontWeight={700}
                  fill="#0f172a"
                >
                  {pt.label || pt.id} ({pos.x}, {pos.y})
                </text>
              </g>
            );
          })}
        </svg>

        {/* Legend & Inequality / Reset Controls inside card footer */}
        {(legendItems.length > 0 || spec.inequality || (spec.sliders || []).length > 0 || interPts.length > 0) && (
          <div className="px-2 pt-2 pb-1 mt-1 border-t border-slate-100 flex flex-wrap items-center justify-between gap-2 text-xs">
            <div className="flex flex-wrap items-center gap-3 min-w-0">
              {legendItems.map((it) => (
                <span key={it.key} className="inline-flex items-center gap-1.5 text-slate-700 font-medium">
                  {it.fill ? (
                    <span
                      className="inline-block w-3 h-3 rounded-xs border"
                      style={{ backgroundColor: it.fill, borderColor: it.color }}
                    />
                  ) : (
                    <span
                      className="inline-block w-4 border-t-2"
                      style={{
                        borderColor: it.color,
                        borderTopStyle: it.dashed ? 'dashed' : 'solid',
                      }}
                    />
                  )}
                  <MathText text={it.label} inline />
                </span>
              ))}
            </div>

            <div className="flex flex-wrap items-center gap-1.5">
              {spec.inequality && (
                <>
                  <button
                    type="button"
                    disabled={disabled}
                    data-testid="canvas-ineq-style-btn"
                    onClick={toggleIneqStyle}
                    className={`px-2.5 py-1 rounded-md border font-semibold cursor-pointer transition-colors ${
                      ineqStyle === 'dashed'
                        ? 'bg-amber-50 border-amber-300 text-amber-900 hover:bg-amber-100'
                        : 'bg-blue-50 border-blue-300 text-blue-900 hover:bg-blue-100'
                    }`}
                  >
                    Frontera: {ineqStyle === 'dashed' ? 'Punteada (<, >)' : 'Sólida (≤, ≥)'}
                  </button>
                  <button
                    type="button"
                    disabled={disabled}
                    data-testid="canvas-ineq-shade-btn"
                    onClick={toggleIneqShade}
                    className="px-2.5 py-1 rounded-md border border-indigo-300 bg-indigo-50 text-indigo-900 font-semibold hover:bg-indigo-100 cursor-pointer transition-colors"
                  >
                    Sombreado: {ineqShade === 'above' ? 'Arriba (y >)' : 'Abajo (y <)'}
                  </button>
                </>
              )}
              <button
                type="button"
                disabled={disabled}
                data-testid="canvas-reset-btn"
                onClick={() => onChange(buildInitialCartesianState(spec))}
                className="px-2 py-1 rounded-md border border-slate-300 bg-white text-slate-600 hover:bg-slate-100 font-semibold cursor-pointer"
                title="Restaurar posiciones iniciales"
              >
                ↺ Reiniciar
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Sliders & Precision Coordinate Inputs */}
      {(spec.sliders || []).length > 0 && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
          {(spec.sliders || []).map((sl) => {
            const cur = value.sliderValues[sl.id] ?? sl.initial ?? sl.min;
            return (
              <div key={sl.id} className="p-2.5 rounded-lg border border-slate-200 bg-slate-50 space-y-1">
                <div className="flex items-center justify-between text-xs font-bold text-slate-700">
                  <MathText text={sl.label || sl.id} inline />
                  <span className="font-mono text-ka-blue">
                    {cur} {sl.unit || ''}
                  </span>
                </div>
                <input
                  type="range"
                  data-testid={`canvas-slider-${sl.id}`}
                  aria-label={sl.label || sl.id}
                  disabled={disabled}
                  min={sl.min}
                  max={sl.max}
                  step={sl.step || 1}
                  value={cur}
                  onChange={(e) =>
                    onChange({
                      ...value,
                      sliderValues: { ...value.sliderValues, [sl.id]: Number(e.target.value) },
                    })
                  }
                  className="w-full accent-ka-blue"
                />
              </div>
            );
          })}
        </div>
      )}

      {interPts.length > 0 && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
          {interPts.map((pt) => {
            const pos = value.pointPositions[pt.id] || { x: pt.x, y: pt.y };
            const ptSnap = pt.snap ?? defaultSnap;
            return (
              <div
                key={`ctrl-${pt.id}`}
                className="p-2 rounded-lg border border-slate-200 bg-slate-50 flex flex-wrap items-center gap-2 text-xs"
              >
                <span className="font-bold text-slate-700 inline-flex items-center gap-1.5">
                  <span
                    className="inline-block w-2.5 h-2.5 rounded-full"
                    style={{ backgroundColor: pt.color || '#1865f2' }}
                  />
                  {pt.label || pt.id}:
                </span>
                <label className="flex items-center gap-1">
                  <span>x</span>
                  <input
                    type="number"
                    data-testid={`canvas-pt-${pt.id}-x`}
                    aria-label={`${pt.label || pt.id} coordenada x`}
                    disabled={disabled || pt.lock_x}
                    step={ptSnap}
                    min={pt.min_x ?? xMin}
                    max={pt.max_x ?? xMax}
                    value={pos.x}
                    onChange={(e) =>
                      onChange({
                        ...value,
                        pointPositions: {
                          ...value.pointPositions,
                          [pt.id]: { ...pos, x: Number(e.target.value) },
                        },
                      })
                    }
                    className="w-16 p-1 border border-slate-300 rounded font-mono bg-white"
                  />
                </label>
                <label className="flex items-center gap-1">
                  <span>y</span>
                  <input
                    type="number"
                    data-testid={`canvas-pt-${pt.id}-y`}
                    aria-label={`${pt.label || pt.id} coordenada y`}
                    disabled={disabled || pt.lock_y}
                    step={ptSnap}
                    min={pt.min_y ?? yMin}
                    max={pt.max_y ?? yMax}
                    value={pos.y}
                    onChange={(e) =>
                      onChange({
                        ...value,
                        pointPositions: {
                          ...value.pointPositions,
                          [pt.id]: { ...pos, y: Number(e.target.value) },
                        },
                      })
                    }
                    className="w-16 p-1 border border-slate-300 rounded font-mono bg-white"
                  />
                </label>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
