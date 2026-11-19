import React from 'react';
import { ProofStep } from '../types';
import { hasRawLatex, toPlainOptionLabel } from '../utils/latexOptionLabel';
import { MathText } from './MathText';

interface StepTileProps {
  step: ProofStep;
  placedIndex?: number;
  totalPlaced?: number;
  disabled?: boolean;
  requireJustification?: boolean;
  justificationBank?: string[];
  selectedJustification?: string;
  onAdd?: () => void;
  onRemove?: () => void;
  onMoveUp?: () => void;
  onMoveDown?: () => void;
  onChangeJustification?: (val: string) => void;
}

export const StepTile: React.FC<StepTileProps> = ({
  step,
  placedIndex,
  totalPlaced = 0,
  disabled = false,
  requireJustification = false,
  justificationBank = [],
  selectedJustification = '',
  onAdd,
  onRemove,
  onMoveUp,
  onMoveDown,
  onChangeJustification,
}) => {
  const isPlaced = typeof placedIndex === 'number';

  return (
    <div
      data-testid={isPlaced ? `proof-placed-${step.id}` : `proof-tile-${step.id}`}
      className={`p-3 rounded-lg border transition-all flex flex-col gap-2 ${
        isPlaced
          ? 'bg-white border-ka-blue/60 shadow-xs'
          : 'bg-slate-50 hover:bg-blue-50/50 border-slate-200'
      }`}
    >
      <div className="flex items-start justify-between gap-2.5 min-w-0">
        <div className="flex items-start gap-2.5 min-w-0 flex-1">
          {isPlaced && (
            <span className="w-6 h-6 rounded-full bg-ka-blue text-white text-xs font-bold flex items-center justify-center shrink-0 mt-0.5">
              {placedIndex + 1}
            </span>
          )}
          <div className="text-sm text-ka-text-primary leading-relaxed min-w-0 flex-1">
            <MathText text={step.content} inline />
          </div>
        </div>

        <div className="flex items-center gap-1 shrink-0">
          {!isPlaced ? (
            <button
              type="button"
              disabled={disabled}
              data-testid={`proof-add-${step.id}`}
              onClick={onAdd}
              className="px-2.5 py-1 text-xs font-bold bg-ka-blue hover:bg-ka-blue-hover text-white rounded transition-colors cursor-pointer disabled:opacity-50"
            >
              + Añadir
            </button>
          ) : (
            <>
              <button
                type="button"
                disabled={disabled || placedIndex === 0}
                data-testid={`proof-up-${step.id}`}
                aria-label="Subir paso"
                onClick={onMoveUp}
                className="px-2 py-1 text-xs font-bold bg-slate-100 hover:bg-slate-200 border border-slate-300 rounded text-slate-700 cursor-pointer disabled:opacity-40"
              >
                ↑
              </button>
              <button
                type="button"
                disabled={disabled || placedIndex >= totalPlaced - 1}
                data-testid={`proof-down-${step.id}`}
                aria-label="Bajar paso"
                onClick={onMoveDown}
                className="px-2 py-1 text-xs font-bold bg-slate-100 hover:bg-slate-200 border border-slate-300 rounded text-slate-700 cursor-pointer disabled:opacity-40"
              >
                ↓
              </button>
              <button
                type="button"
                disabled={disabled}
                data-testid={`proof-remove-${step.id}`}
                aria-label="Quitar paso"
                onClick={onRemove}
                className="px-2 py-1 text-xs font-bold bg-rose-50 hover:bg-rose-100 border border-rose-200 rounded text-rose-700 cursor-pointer disabled:opacity-40"
              >
                ✕
              </button>
            </>
          )}
        </div>
      </div>

      {isPlaced && requireJustification && (
        <div className="flex flex-wrap items-center gap-2 pt-1 border-t border-slate-100">
          <label
            htmlFor={`proof-just-${step.id}`}
            className="text-xs font-semibold text-slate-600"
          >
            Justificación:
          </label>
          <select
            id={`proof-just-${step.id}`}
            data-testid={`proof-just-${step.id}`}
            disabled={disabled}
            value={selectedJustification}
            onChange={(e) => onChangeJustification?.(e.target.value)}
            className="text-xs px-2.5 py-1.5 rounded border border-slate-300 bg-white text-slate-800 outline-none focus:border-ka-blue"
          >
            <option value="">-- Selecciona regla --</option>
            {justificationBank.map((rule, rIdx) => (
              <option key={rule} value={rule}>
                {toPlainOptionLabel(rule, `Regla ${rIdx + 1}`)}
              </option>
            ))}
          </select>
          {selectedJustification && hasRawLatex(selectedJustification) && (
            <span
              data-testid={`proof-just-preview-${step.id}`}
              className="text-xs px-2 py-0.5 rounded bg-blue-50 border border-blue-200 text-slate-800"
            >
              <MathText text={selectedJustification} inline />
            </span>
          )}
        </div>
      )}
    </div>
  );
};
