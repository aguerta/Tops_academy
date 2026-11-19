import React, { useState } from 'react';
import { ConceptMatchingSpec } from '../types';
import { MathText } from './MathText';

interface ConceptMatchingProps {
  spec: ConceptMatchingSpec;
  pairs: Record<string, string>;
  disabled?: boolean;
  onChange: (nextPairs: Record<string, string>) => void;
}

export const ConceptMatching: React.FC<ConceptMatchingProps> = ({
  spec,
  pairs,
  disabled = false,
  onChange,
}) => {
  const [activePremiseId, setActivePremiseId] = useState<string | null>(
    spec.premises[0]?.id ?? null
  );

  const targetById = new Map(spec.targets.map((t) => [t.id, t]));

  const handleAssign = (premiseId: string, targetId: string) => {
    if (disabled) return;
    if (!targetId) {
      const next = { ...pairs };
      delete next[premiseId];
      onChange(next);
      return;
    }
    onChange({ ...pairs, [premiseId]: targetId });
    const nextUnpaired = spec.premises.find((p) => p.id !== premiseId && !pairs[p.id]);
    if (nextUnpaired) {
      setActivePremiseId(nextUnpaired.id);
    }
  };

  return (
    <div data-testid="concept-matching-root" className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
      {/* Left Column: Premises */}
      <div className="space-y-2">
        <div className="text-xs font-bold text-slate-600 uppercase tracking-wider">
          {spec.left_title || 'Premisas'}
        </div>
        {spec.premises.map((pr, idx) => {
          const isActive = activePremiseId === pr.id;
          const assignedTid = pairs[pr.id] || '';
          const assignedTarget = assignedTid ? targetById.get(assignedTid) : null;

          return (
            <div
              key={pr.id}
              data-testid={`matching-premise-${pr.id}`}
              onClick={() => !disabled && setActivePremiseId(pr.id)}
              className={`p-3 rounded-lg border-2 transition-all space-y-2 ${
                isActive
                  ? 'border-ka-blue bg-blue-50/70'
                  : assignedTarget
                  ? 'border-ka-green-border/70 bg-emerald-50/40'
                  : 'border-slate-200 bg-white'
              } ${disabled ? '' : 'cursor-pointer'}`}
            >
              <div className="flex items-start gap-2 min-w-0">
                <span className="w-5 h-5 rounded-full bg-slate-200 text-slate-800 text-xs font-bold flex items-center justify-center shrink-0 mt-0.5">
                  {idx + 1}
                </span>
                <div className="text-xs sm:text-sm text-ka-text-primary min-w-0 flex-1">
                  <MathText text={pr.content} inline />
                </div>
              </div>

              <div className="flex items-center gap-2">
                <select
                  data-testid={`matching-select-${pr.id}`}
                  aria-label={`Emparejar premisa ${idx + 1}`}
                  disabled={disabled}
                  value={assignedTid}
                  onClick={(e) => e.stopPropagation()}
                  onChange={(e) => handleAssign(pr.id, e.target.value)}
                  className="w-full text-xs px-2 py-1.5 rounded border border-slate-300 bg-white text-slate-800 outline-none focus:border-ka-blue"
                >
                  <option value="">-- Selecciona correspondencia --</option>
                  {spec.targets.map((tg, tIdx) => (
                    <option key={tg.id} value={tg.id}>
                      {String.fromCharCode(65 + tIdx)}. {tg.content}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          );
        })}
      </div>

      {/* Right Column: Targets (click after selecting a premise) */}
      <div className="space-y-2">
        <div className="text-xs font-bold text-slate-600 uppercase tracking-wider">
          {spec.right_title || 'Consecuencias / Diagnósticos'}
        </div>
        {spec.targets.map((tg, tIdx) => {
          const usedByPremise = Object.entries(pairs).find(([, tid]) => tid === tg.id)?.[0];
          return (
            <button
              key={tg.id}
              type="button"
              disabled={disabled}
              data-testid={`matching-target-${tg.id}`}
              onClick={() => activePremiseId && handleAssign(activePremiseId, tg.id)}
              className={`w-full text-left p-3 rounded-lg border transition-all flex items-start gap-2.5 cursor-pointer disabled:cursor-not-allowed ${
                usedByPremise
                  ? 'border-ka-blue/60 bg-blue-50/40'
                  : 'border-slate-200 bg-slate-50 hover:bg-blue-50/40 hover:border-slate-300'
              }`}
            >
              <span className="px-2 py-0.5 rounded bg-white border border-slate-300 text-xs font-bold text-slate-700 shrink-0 mt-0.5">
                {String.fromCharCode(65 + tIdx)}
              </span>
              <div className="text-xs sm:text-sm text-ka-text-primary min-w-0 flex-1">
                <MathText text={tg.content} inline />
              </div>
              {usedByPremise && (
                <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-ka-blue text-white shrink-0">
                  #{spec.premises.findIndex((p) => p.id === usedByPremise) + 1}
                </span>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
};
