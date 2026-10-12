import React from 'react';
import { GraphSpec } from '../types';

interface CoordinatePlaneProps {
  graph: GraphSpec;
  className?: string;
}

export const CoordinatePlane: React.FC<CoordinatePlaneProps> = ({ graph, className = '' }) => {
  const width = graph.width || 360;
  const height = graph.height || 360;
  const padding = 28;

  const [xMin, xMax] = graph.x_range || [-7, 7];
  const [yMin, yMax] = graph.y_range || [-7, 7];
  const step = graph.step || 1;

  const plotWidth = width - 2 * padding;
  const plotHeight = height - 2 * padding;

  const toSvgX = (x: number) => padding + ((x - xMin) / (xMax - xMin)) * plotWidth;
  const toSvgY = (y: number) => padding + ((yMax - y) / (yMax - yMin)) * plotHeight;

  // Generate grid values
  const xGridValues: number[] = [];
  for (let x = Math.ceil(xMin); x <= Math.floor(xMax); x += step) {
    xGridValues.push(x);
  }

  const yGridValues: number[] = [];
  for (let y = Math.ceil(yMin); y <= Math.floor(yMax); y += step) {
    yGridValues.push(y);
  }

  // Curve paths generator
  const renderCurves = () => {
    if (!graph.curves || graph.curves.length === 0) return null;

    return graph.curves.map((curve, idx) => {
      const color = curve.color || '#00a2e8';
      const exprStr = curve.expression || curve.fn;
      const domain = curve.domain || [xMin, xMax];

      if (!exprStr) return null;

      // Compile or evaluate expression safely
      let evalFn: (x: number) => number;
      try {
        // Safe evaluation of mathematical curve function
        evalFn = new Function('x', `with (Math) { return (${exprStr}); }`) as (x: number) => number;
      } catch {
        return null;
      }

      const points: Array<[number, number]> = [];
      const samples = 140;
      const dMin = Math.max(domain[0], xMin);
      const dMax = Math.min(domain[1], xMax);
      const dx = (dMax - dMin) / samples;

      for (let i = 0; i <= samples; i++) {
        const x = dMin + i * dx;
        try {
          const y = evalFn(x);
          if (typeof y === 'number' && !isNaN(y) && isFinite(y)) {
            if (y >= yMin - 2 && y <= yMax + 2) {
              points.push([toSvgX(x), toSvgY(y)]);
            }
          }
        } catch {}
      }

      if (points.length < 2) return null;

      const pathData = points.reduce((acc, [px, py], i) => {
        return i === 0 ? `M ${px.toFixed(1)} ${py.toFixed(1)}` : `${acc} L ${px.toFixed(1)} ${py.toFixed(1)}`;
      }, '');

      const labelPos = curve.label_pos
        ? [toSvgX(curve.label_pos[0]), toSvgY(curve.label_pos[1])]
        : points[Math.floor(points.length * 0.3)];

      return (
        <g key={curve.id || idx}>
          <path
            d={pathData}
            fill="none"
            stroke={color}
            strokeWidth="3"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
          {curve.label && labelPos && (
            <text
              x={labelPos[0] - 14}
              y={labelPos[1] - 8}
              fill={color}
              fontSize="16"
              fontStyle="italic"
              fontWeight="bold"
            >
              {curve.label}
            </text>
          )}
        </g>
      );
    });
  };

  // Render open and closed points
  const renderPoints = () => {
    if (!graph.points || graph.points.length === 0) return null;

    return graph.points.map((pt, idx) => {
      const cx = toSvgX(pt.x);
      const cy = toSvgY(pt.y);
      const color = pt.color || '#00a2e8';

      return (
        <g key={idx}>
          {pt.type === 'open' ? (
            <circle
              cx={cx}
              cy={cy}
              r="5.5"
              fill="#ffffff"
              stroke={color}
              strokeWidth="2.5"
              className="open-point"
            />
          ) : (
            <circle
              cx={cx}
              cy={cy}
              r="5.5"
              fill={color}
              className="closed-point"
            />
          )}
          {pt.label && (
            <text
              x={cx + 8}
              y={cy - 8}
              fill="#21242c"
              fontSize="12"
              fontWeight="500"
            >
              {pt.label}
            </text>
          )}
        </g>
      );
    });
  };

  const originX = toSvgX(0);
  const originY = toSvgY(0);

  return (
    <div
      data-testid="graph-container"
      className={`inline-block my-4 p-2 bg-white rounded-lg border border-ka-border-card shadow-sm ${className}`}
    >
      <svg
        data-testid="coordinate-plane"
        className="coordinate-plane block"
        width={width}
        height={height}
        viewBox={`0 0 ${width} ${height}`}
      >
        <defs>
          <marker
            id="axis-arrow"
            viewBox="0 0 10 10"
            refX="6"
            refY="5"
            markerWidth="6"
            markerHeight="6"
            orient="auto-start-reverse"
          >
            <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#21242c" />
          </marker>
        </defs>

        {/* Grid lines */}
        {xGridValues.map((x) => (
          <line
            key={`grid-x-${x}`}
            x1={toSvgX(x)}
            y1={padding}
            x2={toSvgX(x)}
            y2={height - padding}
            stroke="#e2e8f0"
            strokeWidth="1"
          />
        ))}
        {yGridValues.map((y) => (
          <line
            key={`grid-y-${y}`}
            x1={padding}
            y1={toSvgY(y)}
            x2={width - padding}
            y2={toSvgY(y)}
            stroke="#e2e8f0"
            strokeWidth="1"
          />
        ))}

        {/* X Axis */}
        <line
          x1={padding - 6}
          y1={originY}
          x2={width - padding + 8}
          y2={originY}
          stroke="#21242c"
          strokeWidth="2"
          markerEnd="url(#axis-arrow)"
        />

        {/* Y Axis */}
        <line
          x1={originX}
          y1={height - padding + 6}
          x2={originX}
          y2={padding - 8}
          stroke="#21242c"
          strokeWidth="2"
          markerEnd="url(#axis-arrow)"
        />

        {/* Axis Labels */}
        <text
          x={width - padding + 12}
          y={originY + 4}
          fontSize="13"
          fontStyle="italic"
          fontWeight="bold"
          fill="#21242c"
        >
          x
        </text>
        <text
          x={originX - 4}
          y={padding - 14}
          fontSize="13"
          fontStyle="italic"
          fontWeight="bold"
          fill="#21242c"
        >
          y
        </text>

        {/* Tick labels on X axis */}
        {xGridValues
          .filter((x) => x !== 0 && x % 2 === 0)
          .map((x) => (
            <text
              key={`tick-x-${x}`}
              x={toSvgX(x)}
              y={originY + 16}
              fontSize="11"
              fill="#59606d"
              textAnchor="middle"
            >
              {x}
            </text>
          ))}

        {/* Tick labels on Y axis */}
        {yGridValues
          .filter((y) => y !== 0 && y % 2 === 0)
          .map((y) => (
            <text
              key={`tick-y-${y}`}
              x={originX - 8}
              y={toSvgY(y) + 4}
              fontSize="11"
              fill="#59606d"
              textAnchor="end"
            >
              {y}
            </text>
          ))}

        {/* Curves */}
        {renderCurves()}

        {/* Points (Open and Closed) */}
        {renderPoints()}
      </svg>
    </div>
  );
};
