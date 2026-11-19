import React, { useMemo } from 'react';
import { AdversarialBreakSpec } from '../types';
import { evaluateAdversarialReadouts } from '../services/symbolicValidator';
import { MathText } from './MathText';

export interface AdversarialAnswerState {
  selectedStepId: string | null;
  selectedReasonId: string | null;
  witnessValues: Record<string, string>;
}

interface AdversarialArenaProps {
  spec: AdversarialBreakSpec;
  value: AdversarialAnswerState;
  disabled?: boolean;
  onChange: (next: AdversarialAnswerState) => void;
}

export const AdversarialArena: React.FC<AdversarialArenaProps> = ({
  spec,
  value,
  disabled = false,
  onChange,
}) => {
  if (spec.mode === 'find_fallacy') {
    const steps = spec.steps || [];
    const reasons = spec.reason_options || [];

    return (
      <div data-testid="adversarial-arena-root" className="space-y-4">
        {spec.prompt && (
          <div className="text-xs sm:text-sm font-semibold text-ka-text-secondary">
            <MathText text={spec.prompt} inline />
          </div>
        )}

        <div className="space-y-2" role="radiogroup" aria-label="Pasos de la derivación">
          {steps.map((st, idx) => {
            const selected = value.selectedStepId === st.id;
            return (
              <button
                key={st.id}
                type="button"
                disabled={disabled}
                role="radio"
                aria-checked={selected}
                data-testid={`adv-step-${st.id}`}
                onClick={() =>
                  onChange({
                    ...value,
                    selectedStepId: selected ? null : st.id,
                  })
                }
                className={`w-full text-left p-3 rounded-lg border-2 transition-all flex items-start gap-3 cursor-pointer disabled:cursor-not-allowed ${
                  selected
                    ? 'border-ka-blue bg-blue-50/70 shadow-xs'
                    : 'border-slate-200 bg-white hover:border-slate-300'
                }`}
              >
                <span
                  className={`px-2 py-0.5 rounded text-xs font-bold shrink-0 mt-0.5 ${
                    selected ? 'bg-ka-blue text-white' : 'bg-slate-100 text-slate-700'
                  }`}
                >
                  {st.label || `Paso ${idx + 1}`}
                </span>
                <div className="text-sm text-ka-text-primary leading-relaxed min-w-0 flex-1">
                  <MathText text={st.content} inline />
                </div>
              </button>
            );
          })}
        </div>

        {reasons.length > 0 && (
          <div className="space-y-2 pt-2 border-t border-slate-200">
            <div className="text-xs font-bold text-slate-600 uppercase tracking-wider">
              Justifica por qué ese paso falla:
            </div>
            <div className="space-y-1.5" role="radiogroup" aria-label="Razón de la falacia">
              {reasons.map((r) => {
                const selected = value.selectedReasonId === r.id;
                return (
                  <button
                    key={r.id}
                    type="button"
                    disabled={disabled}
                    role="radio"
                    aria-checked={selected}
                    data-testid={`adv-reason-${r.id}`}
                    onClick={() =>
                      onChange({
                        ...value,
                        selectedReasonId: selected ? null : r.id,
                      })
                    }
                    className={`w-full text-left p-2.5 rounded-lg border transition-all text-xs sm:text-sm cursor-pointer disabled:cursor-not-allowed ${
                      selected
                        ? 'border-ka-blue bg-blue-50/70 text-ka-text-primary font-medium'
                        : 'border-slate-200 bg-slate-50 hover:bg-slate-100 text-slate-700'
                    }`}
                  >
                    <MathText text={r.content} inline />
                  </button>
                );
              })}
            </div>
          </div>
        )}
      </div>
    );
  }

  // mode === 'counterexample'
  const inputs = spec.inputs || [];
  const readouts = useMemo(
    () => evaluateAdversarialReadouts(spec.computed_readouts, value.witnessValues),
    [spec.computed_readouts, value.witnessValues]
  );

  return (
    <div data-testid="adversarial-arena-root" className="space-y-4 max-w-xl">
      {spec.prompt && (
        <div className="text-xs sm:text-sm font-semibold text-ka-text-secondary">
          <MathText text={spec.prompt} inline />
        </div>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {inputs.map((inp) => {
          const iid = inp.id || inp.name || '';
          const val = value.witnessValues[iid] ?? '';
          return (
            <div
              key={iid}
              className="p-3 rounded-lg border border-slate-200 bg-white space-y-1.5"
            >
              <label
                htmlFor={`adv-input-${iid}`}
                className="block text-xs font-bold text-slate-700"
              >
                <MathText text={inp.label || iid} inline />
                {(inp.min !== undefined || inp.max !== undefined) && (
                  <span className="ml-1.5 font-normal text-slate-500">
                    [{inp.min ?? '-∞'}, {inp.max ?? '+∞'}]
                    {inp.type === 'integer' ? ' (entero)' : ''}
                  </span>
                )}
              </label>
              <input
                id={`adv-input-${iid}`}
                data-testid={`adv-input-${iid}`}
                type="text"
                inputMode="decimal"
                disabled={disabled}
                value={val}
                placeholder={inp.placeholder || 'Valor numérico'}
                onChange={(e) =>
                  onChange({
                    ...value,
                    witnessValues: { ...value.witnessValues, [iid]: e.target.value },
                  })
                }
                className="w-full p-2 text-sm font-mono border border-slate-300 rounded outline-none focus:border-ka-blue focus:ring-2 focus:ring-blue-100"
              />
            </div>
          );
        })}
      </div>

      {readouts.length > 0 && (
        <div
          data-testid="adv-computed-readouts"
          className="p-3 rounded-lg border border-slate-200 bg-slate-50 space-y-2"
        >
          <div className="text-[11px] font-bold uppercase tracking-wider text-slate-600">
            Lectura computada en vivo
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {readouts.map((ro, idx) => (
              <div
                key={ro.id}
                data-testid={`adv-readout-${idx}`}
                className="flex items-center justify-between gap-2 px-2.5 py-1.5 rounded bg-white border border-slate-200 text-xs"
              >
                <span className="font-semibold text-slate-700 min-w-0">
                  <MathText text={ro.label} inline />
                </span>
                <span className="font-mono font-bold text-ka-blue shrink-0">
                  {ro.formatted}
                  {ro.unit ? ` ${ro.unit}` : ''}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
