import React, { useCallback, useEffect, useRef, useState } from 'react';
import {
  Eraser,
  Grid3X3,
  Highlighter,
  Minus,
  MousePointerClick,
  Pencil,
  Redo2,
  Trash2,
  Undo2,
  X,
} from 'lucide-react';

export type ScratchTool = 'pen' | 'highlighter' | 'line' | 'eraser';
export type ScratchBgMode = 'transparent' | 'grid' | 'solid';

interface StrokePoint {
  x: number;
  y: number;
  pressure?: number;
}

interface Stroke {
  tool: ScratchTool;
  color: string;
  width: number;
  points: StrokePoint[];
}

interface QuestionCanvasHistory {
  strokes: Stroke[];
  undoStack: Stroke[][];
  redoStack: Stroke[][];
}

export interface ScratchpadOverlayProps {
  isOpen: boolean;
  questionId: string;
  bgMode?: ScratchBgMode;
  onChangeBgMode?: (next: ScratchBgMode) => void;
  onClose: () => void;
}

const PALETTE: Array<{ id: string; label: string; hex: string }> = [
  { id: 'slate', label: 'Pizarra', hex: '#1e293b' },
  { id: 'blue', label: 'Azul', hex: '#1865f2' },
  { id: 'red', label: 'Rojo', hex: '#dc2626' },
  { id: 'green', label: 'Verde', hex: '#059669' },
  { id: 'amber', label: 'Ámbar', hex: '#d97706' },
  { id: 'purple', label: 'Morado', hex: '#7c3aed' },
];

const WIDTHS: Array<{ val: number; label: string; dotPx: number }> = [
  { val: 2, label: 'Fino', dotPx: 4 },
  { val: 4, label: 'Medio', dotPx: 7 },
  { val: 8, label: 'Grueso', dotPx: 11 },
];

const BG_CYCLE: ScratchBgMode[] = ['transparent', 'grid', 'solid'];
const BG_LABELS: Record<ScratchBgMode, string> = {
  transparent: 'Superpuesta',
  grid: 'Cuadrícula',
  solid: 'Blanca',
};

/**
 * Grid background placed behind the question/solution workspace so grid lines stay crisp
 * without veiling the problem stem or step-by-step solution underneath ink strokes.
 */
export const SCRATCHPAD_GRID_BG_STYLE: React.CSSProperties = {
  backgroundColor: '#ffffff',
  backgroundImage:
    'linear-gradient(to right, rgba(71, 85, 105, 0.45) 1.5px, transparent 1.5px), ' +
    'linear-gradient(to bottom, rgba(71, 85, 105, 0.45) 1.5px, transparent 1.5px), ' +
    'linear-gradient(to right, rgba(100, 116, 139, 0.38) 1px, transparent 1px), ' +
    'linear-gradient(to bottom, rgba(100, 116, 139, 0.38) 1px, transparent 1px)',
  backgroundSize: '96px 96px, 96px 96px, 24px 24px, 24px 24px',
};

function createEmptyHistory(): QuestionCanvasHistory {
  return { strokes: [], undoStack: [], redoStack: [] };
}

function drawStroke(ctx: CanvasRenderingContext2D, stroke: Stroke) {
  const pts = stroke.points;
  if (!pts || pts.length === 0) return;

  ctx.save();
  ctx.lineCap = 'round';
  ctx.lineJoin = 'round';

  if (stroke.tool === 'eraser') {
    ctx.globalCompositeOperation = 'destination-out';
    ctx.strokeStyle = 'rgba(0, 0, 0, 1)';
    ctx.fillStyle = 'rgba(0, 0, 0, 1)';
    ctx.lineWidth = stroke.width * 3.2;
  } else if (stroke.tool === 'highlighter') {
    ctx.globalCompositeOperation = 'source-over';
    ctx.globalAlpha = 0.32;
    ctx.strokeStyle = stroke.color;
    ctx.fillStyle = stroke.color;
    ctx.lineWidth = stroke.width * 3.5;
  } else {
    ctx.globalCompositeOperation = 'source-over';
    ctx.strokeStyle = stroke.color;
    ctx.fillStyle = stroke.color;
    ctx.lineWidth = stroke.width;
  }

  if (pts.length === 1) {
    ctx.beginPath();
    ctx.arc(pts[0].x, pts[0].y, ctx.lineWidth / 2, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
    return;
  }

  if (stroke.tool === 'line') {
    const start = pts[0];
    const end = pts[pts.length - 1];
    ctx.beginPath();
    ctx.moveTo(start.x, start.y);
    ctx.lineTo(end.x, end.y);
    ctx.stroke();
    ctx.restore();
    return;
  }

  if (stroke.tool === 'pen') {
    const pressures = pts.map((p) => p.pressure).filter((p): p is number => p !== undefined && p > 0 && p !== 0.5);
    if (pressures.length > 0) {
      const avgP = pressures.reduce((a, b) => a + b, 0) / pressures.length;
      ctx.lineWidth = Math.max(1, stroke.width * (0.75 + 0.5 * avgP));
    }
  }

  ctx.beginPath();
  ctx.moveTo(pts[0].x, pts[0].y);
  for (let i = 1; i < pts.length - 1; i++) {
    const midX = (pts[i].x + pts[i + 1].x) / 2;
    const midY = (pts[i].y + pts[i + 1].y) / 2;
    ctx.quadraticCurveTo(pts[i].x, pts[i].y, midX, midY);
  }
  const last = pts[pts.length - 1];
  ctx.lineTo(last.x, last.y);
  ctx.stroke();
  ctx.restore();
}

export const ScratchpadOverlay: React.FC<ScratchpadOverlayProps> = ({
  isOpen,
  questionId,
  bgMode: controlledBgMode,
  onChangeBgMode,
  onClose,
}) => {
  const [tool, setTool] = useState<ScratchTool>('pen');
  const [color, setColor] = useState<string>(PALETTE[1].hex);
  const [width, setWidth] = useState<number>(4);
  const [internalBgMode, setInternalBgMode] = useState<ScratchBgMode>('transparent');
  const effectiveBgMode = controlledBgMode ?? internalBgMode;
  const [passthrough, setPassthrough] = useState<boolean>(false);
  const [, setHistoryVersion] = useState<number>(0);

  const containerRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const historiesRef = useRef<Map<string, QuestionCanvasHistory>>(new Map());
  const activeStrokeRef = useRef<Stroke | null>(null);
  const activePointerIdRef = useRef<number | null>(null);

  const getHistory = useCallback(
    (qid: string): QuestionCanvasHistory => {
      let existing = historiesRef.current.get(qid);
      if (!existing) {
        existing = createEmptyHistory();
        historiesRef.current.set(qid, existing);
      }
      return existing;
    },
    []
  );

  const redrawCanvas = useCallback(() => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

    const rect = container.getBoundingClientRect();
    const cssW = Math.max(1, Math.floor(rect.width));
    const cssH = Math.max(1, Math.floor(rect.height));
    const dpr = typeof window !== 'undefined' ? window.devicePixelRatio || 1 : 1;

    const targetW = Math.floor(cssW * dpr);
    const targetH = Math.floor(cssH * dpr);
    if (canvas.width !== targetW || canvas.height !== targetH) {
      canvas.width = targetW;
      canvas.height = targetH;
    }

    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, cssW, cssH);

    const hist = getHistory(questionId);
    for (const s of hist.strokes) {
      drawStroke(ctx, s);
    }
    if (activeStrokeRef.current) {
      drawStroke(ctx, activeStrokeRef.current);
    }
  }, [getHistory, questionId]);

  useEffect(() => {
    if (!isOpen) return;
    activeStrokeRef.current = null;
    activePointerIdRef.current = null;
    redrawCanvas();

    const container = containerRef.current;
    if (!container || typeof ResizeObserver === 'undefined') return;
    const ro = new ResizeObserver(() => redrawCanvas());
    ro.observe(container);
    return () => ro.disconnect();
  }, [isOpen, questionId, redrawCanvas]);

  const handleUndo = useCallback(() => {
    const hist = getHistory(questionId);
    if (hist.undoStack.length === 0) return;
    const prev = hist.undoStack[hist.undoStack.length - 1];
    hist.undoStack = hist.undoStack.slice(0, -1);
    hist.redoStack = [...hist.redoStack, hist.strokes];
    hist.strokes = prev;
    redrawCanvas();
    setHistoryVersion((v) => v + 1);
  }, [getHistory, questionId, redrawCanvas]);

  const handleRedo = useCallback(() => {
    const hist = getHistory(questionId);
    if (hist.redoStack.length === 0) return;
    const next = hist.redoStack[hist.redoStack.length - 1];
    hist.redoStack = hist.redoStack.slice(0, -1);
    hist.undoStack = [...hist.undoStack, hist.strokes];
    hist.strokes = next;
    redrawCanvas();
    setHistoryVersion((v) => v + 1);
  }, [getHistory, questionId, redrawCanvas]);

  const handleClear = useCallback(() => {
    const hist = getHistory(questionId);
    if (hist.strokes.length === 0) return;
    hist.undoStack = [...hist.undoStack, hist.strokes];
    hist.redoStack = [];
    hist.strokes = [];
    redrawCanvas();
    setHistoryVersion((v) => v + 1);
  }, [getHistory, questionId, redrawCanvas]);

  const onCloseRef = useRef(onClose);
  onCloseRef.current = onClose;

  useEffect(() => {
    if (!isOpen) return;
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.isComposing) return;
      const target = e.target as HTMLElement | null;
      const typing =
        !!target &&
        (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA' || target.isContentEditable);

      if (e.key === 'Escape') {
        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();
        onCloseRef.current();
        return;
      }

      if (typing || passthrough) return;
      if ((e.ctrlKey || e.metaKey) && !e.altKey) {
        const lower = e.key.toLowerCase();
        if (lower === 'z' && !e.shiftKey) {
          e.preventDefault();
          handleUndo();
        } else if (lower === 'y' || (lower === 'z' && e.shiftKey)) {
          e.preventDefault();
          handleRedo();
        }
      }
    };
    window.addEventListener('keydown', onKeyDown, true);
    return () => window.removeEventListener('keydown', onKeyDown, true);
  }, [isOpen, passthrough, handleUndo, handleRedo]);

  if (!isOpen) return null;

  const currentHistory = getHistory(questionId);
  const canUndo = currentHistory.undoStack.length > 0;
  const canRedo = currentHistory.redoStack.length > 0;
  const canClear = currentHistory.strokes.length > 0;

  const getLocalPoint = (e: React.PointerEvent<HTMLCanvasElement>): StrokePoint => {
    const canvas = canvasRef.current!;
    const rect = canvas.getBoundingClientRect();
    return {
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
      pressure: e.pressure,
    };
  };

  const handlePointerDown = (e: React.PointerEvent<HTMLCanvasElement>) => {
    if (passthrough || e.button === 2) return;
    e.preventDefault();
    const canvas = canvasRef.current;
    if (canvas && canvas.setPointerCapture) {
      try {
        canvas.setPointerCapture(e.pointerId);
      } catch {
        // Ignore if pointer cannot be captured
      }
    }
    activePointerIdRef.current = e.pointerId;
    const pt = getLocalPoint(e);
    activeStrokeRef.current = {
      tool,
      color,
      width,
      points: [pt],
    };
    redrawCanvas();
  };

  const handlePointerMove = (e: React.PointerEvent<HTMLCanvasElement>) => {
    if (!activeStrokeRef.current || activePointerIdRef.current !== e.pointerId) return;
    e.preventDefault();
    const pt = getLocalPoint(e);
    const active = activeStrokeRef.current;
    if (active.tool === 'line') {
      active.points = [active.points[0], pt];
    } else {
      const prev = active.points[active.points.length - 1];
      if (!prev || Math.hypot(pt.x - prev.x, pt.y - prev.y) >= 1.5) {
        active.points.push(pt);
      }
    }
    redrawCanvas();
  };

  const finishStroke = (e: React.PointerEvent<HTMLCanvasElement>) => {
    if (!activeStrokeRef.current || activePointerIdRef.current !== e.pointerId) return;
    const canvas = canvasRef.current;
    if (canvas && canvas.releasePointerCapture) {
      try {
        canvas.releasePointerCapture(e.pointerId);
      } catch {
        // Ignore if already released
      }
    }
    const committed = activeStrokeRef.current;
    activeStrokeRef.current = null;
    activePointerIdRef.current = null;

    const hist = getHistory(questionId);
    hist.undoStack = [...hist.undoStack, hist.strokes];
    hist.redoStack = [];
    hist.strokes = [...hist.strokes, committed];
    redrawCanvas();
    setHistoryVersion((v) => v + 1);
  };

  const cycleBgMode = () => {
    const idx = BG_CYCLE.indexOf(effectiveBgMode);
    const next = BG_CYCLE[(idx + 1) % BG_CYCLE.length];
    if (onChangeBgMode) {
      onChangeBgMode(next);
    } else {
      setInternalBgMode(next);
    }
  };

  // Only solid ('Blanca') covers the question layer; 'transparent' and 'grid' keep the overlay clear
  // while the grid pattern renders behind the workspace container in PracticeSession.
  const bgStyle: React.CSSProperties =
    effectiveBgMode === 'solid'
      ? { backgroundColor: '#ffffff' }
      : { backgroundColor: 'transparent' };

  return (
    <div
      ref={containerRef}
      data-testid="scratchpad-root"
      aria-label="Pizarra interactiva de apuntes"
      className="absolute inset-0 z-30 pointer-events-none select-none overflow-hidden"
    >
      {/* Background Paper Layer (kept behind transparent ink canvas so eraser does not punch through paper) */}
      <div
        data-testid="scratchpad-paper"
        aria-hidden="true"
        className="absolute inset-0 pointer-events-none transition-colors duration-150"
        style={bgStyle}
      />

      {/* Drawing Canvas */}
      <canvas
        ref={canvasRef}
        data-testid="scratchpad-canvas"
        onPointerDown={handlePointerDown}
        onPointerMove={handlePointerMove}
        onPointerUp={finishStroke}
        onPointerCancel={finishStroke}
        className={`absolute inset-0 w-full h-full block ${
          passthrough ? 'pointer-events-none' : 'pointer-events-auto cursor-crosshair'
        }`}
        style={{
          touchAction: passthrough ? 'auto' : 'none',
          pointerEvents: passthrough ? 'none' : 'auto',
        }}
      />

      {/* Floating Khan-Academy-Inspired Toolbar (Bottom-Center below Hints) */}
      <div
        data-testid="scratchpad-toolbar"
        role="toolbar"
        aria-label="Herramientas de pizarra"
        className="pointer-events-auto absolute bottom-3 left-1/2 -translate-x-1/2 z-40 max-w-[calc(100%-16px)] flex flex-wrap items-center justify-center gap-1 sm:gap-1.5 px-2.5 py-1.5 bg-white/95 backdrop-blur-md border border-slate-200 rounded-xl shadow-lg text-xs"
      >
        {/* Drawing Tools */}
        <div className="flex items-center gap-0.5 pr-1.5 border-r border-slate-200">
          <button
            type="button"
            data-testid="scratchpad-tool-pen"
            onClick={() => {
              setTool('pen');
              if (passthrough) setPassthrough(false);
            }}
            aria-pressed={tool === 'pen' && !passthrough}
            title="Lápiz"
            className={`p-1.5 rounded-lg transition-colors cursor-pointer ${
              tool === 'pen' && !passthrough
                ? 'bg-ka-blue text-white shadow-sm'
                : 'text-slate-600 hover:bg-slate-100'
            }`}
          >
            <Pencil className="w-3.5 h-3.5" />
          </button>
          <button
            type="button"
            data-testid="scratchpad-tool-highlighter"
            onClick={() => {
              setTool('highlighter');
              if (passthrough) setPassthrough(false);
            }}
            aria-pressed={tool === 'highlighter' && !passthrough}
            title="Resaltador"
            className={`p-1.5 rounded-lg transition-colors cursor-pointer ${
              tool === 'highlighter' && !passthrough
                ? 'bg-ka-blue text-white shadow-sm'
                : 'text-slate-600 hover:bg-slate-100'
            }`}
          >
            <Highlighter className="w-3.5 h-3.5" />
          </button>
          <button
            type="button"
            data-testid="scratchpad-tool-line"
            onClick={() => {
              setTool('line');
              if (passthrough) setPassthrough(false);
            }}
            aria-pressed={tool === 'line' && !passthrough}
            title="Regla / Línea recta"
            className={`p-1.5 rounded-lg transition-colors cursor-pointer ${
              tool === 'line' && !passthrough
                ? 'bg-ka-blue text-white shadow-sm'
                : 'text-slate-600 hover:bg-slate-100'
            }`}
          >
            <Minus className="w-3.5 h-3.5 -rotate-45" />
          </button>
          <button
            type="button"
            data-testid="scratchpad-tool-eraser"
            onClick={() => {
              setTool('eraser');
              if (passthrough) setPassthrough(false);
            }}
            aria-pressed={tool === 'eraser' && !passthrough}
            title="Borrador"
            className={`p-1.5 rounded-lg transition-colors cursor-pointer ${
              tool === 'eraser' && !passthrough
                ? 'bg-ka-blue text-white shadow-sm'
                : 'text-slate-600 hover:bg-slate-100'
            }`}
          >
            <Eraser className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* Palette Swatches */}
        <div className="flex items-center gap-1 pr-1.5 border-r border-slate-200">
          {PALETTE.map((swatch) => {
            const selected = color === swatch.hex && tool !== 'eraser';
            return (
              <button
                key={swatch.id}
                type="button"
                data-testid={`scratchpad-color-${swatch.id}`}
                onClick={() => {
                  setColor(swatch.hex);
                  if (tool === 'eraser') setTool('pen');
                  if (passthrough) setPassthrough(false);
                }}
                aria-label={`Color ${swatch.label}`}
                aria-pressed={selected}
                title={swatch.label}
                className={`w-4 h-4 rounded-full transition-transform cursor-pointer ${
                  selected ? 'ring-2 ring-offset-1 ring-slate-800 scale-110' : 'hover:scale-110'
                }`}
                style={{ backgroundColor: swatch.hex }}
              />
            );
          })}
        </div>

        {/* Stroke Widths */}
        <div className="flex items-center gap-0.5 pr-1.5 border-r border-slate-200">
          {WIDTHS.map((w) => {
            const active = width === w.val;
            return (
              <button
                key={w.val}
                type="button"
                data-testid={`scratchpad-width-${w.val}`}
                onClick={() => setWidth(w.val)}
                aria-label={`Grosor ${w.label}`}
                aria-pressed={active}
                title={`Grosor ${w.label}`}
                className={`w-6 h-6 rounded-lg flex items-center justify-center transition-colors cursor-pointer ${
                  active ? 'bg-slate-200 text-slate-900' : 'hover:bg-slate-100 text-slate-600'
                }`}
              >
                <span
                  className="rounded-full bg-current inline-block"
                  style={{ width: `${w.dotPx}px`, height: `${w.dotPx}px` }}
                />
              </button>
            );
          })}
        </div>

        {/* Background Mode & Interact Underneath */}
        <div className="flex items-center gap-1 pr-1.5 border-r border-slate-200">
          <button
            type="button"
            data-testid="scratchpad-bg-btn"
            onClick={cycleBgMode}
            title="Alternar fondo (Superpuesta / Cuadrícula / Blanca)"
            className="px-2 py-1 rounded-lg border border-slate-200 bg-slate-50 hover:bg-slate-100 text-slate-700 font-semibold flex items-center gap-1 cursor-pointer"
          >
            <Grid3X3 className="w-3.5 h-3.5 text-slate-500" />
            <span className="hidden sm:inline">{BG_LABELS[effectiveBgMode]}</span>
          </button>

          <button
            type="button"
            data-testid="scratchpad-passthrough-btn"
            onClick={() => setPassthrough((p) => !p)}
            aria-pressed={passthrough}
            title="Permite interactuar con las opciones o gráfico debajo sin ocultar tus trazos"
            className={`px-2 py-1 rounded-lg border font-semibold flex items-center gap-1 transition-colors cursor-pointer ${
              passthrough
                ? 'bg-emerald-50 border-emerald-400 text-emerald-800 hover:bg-emerald-100'
                : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100'
            }`}
          >
            <MousePointerClick className="w-3.5 h-3.5" />
            <span className="hidden md:inline">Interactuar</span>
          </button>
        </div>

        {/* History Actions & Close */}
        <div className="flex items-center gap-0.5">
          <button
            type="button"
            data-testid="scratchpad-undo-btn"
            disabled={!canUndo}
            onClick={handleUndo}
            title="Deshacer (Ctrl+Z)"
            aria-label="Deshacer"
            className="p-1.5 rounded-lg text-slate-600 hover:bg-slate-100 disabled:opacity-35 disabled:cursor-not-allowed cursor-pointer"
          >
            <Undo2 className="w-3.5 h-3.5" />
          </button>
          <button
            type="button"
            data-testid="scratchpad-redo-btn"
            disabled={!canRedo}
            onClick={handleRedo}
            title="Rehacer (Ctrl+Y)"
            aria-label="Rehacer"
            className="p-1.5 rounded-lg text-slate-600 hover:bg-slate-100 disabled:opacity-35 disabled:cursor-not-allowed cursor-pointer"
          >
            <Redo2 className="w-3.5 h-3.5" />
          </button>
          <button
            type="button"
            data-testid="scratchpad-clear-btn"
            disabled={!canClear}
            onClick={handleClear}
            title="Limpiar pizarra"
            aria-label="Limpiar pizarra"
            className="p-1.5 rounded-lg text-rose-600 hover:bg-rose-50 disabled:opacity-35 disabled:cursor-not-allowed cursor-pointer"
          >
            <Trash2 className="w-3.5 h-3.5" />
          </button>
          <button
            type="button"
            data-testid="scratchpad-close-btn"
            onClick={onClose}
            title="Cerrar pizarra (Esc / P)"
            aria-label="Cerrar pizarra"
            className="p-1.5 ml-0.5 rounded-lg text-slate-500 hover:bg-slate-100 hover:text-slate-800 cursor-pointer"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </div>
  );
};
