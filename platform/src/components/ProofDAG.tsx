import React from 'react';
import { ProofDagSpec } from '../types';
import { MathText } from './MathText';
import { StepTile } from './StepTile';

interface ProofDAGProps {
  spec: ProofDagSpec;
  orderedStepIds: string[];
  justifications: Record<string, string>;
  disabled?: boolean;
  onChange: (orderedStepIds: string[], justifications: Record<string, string>) => void;
}

export const ProofDAG: React.FC<ProofDAGProps> = ({
  spec,
  orderedStepIds,
  justifications,
  disabled = false,
  onChange,
}) => {
  const placedSet = new Set(orderedStepIds);
  const stepMap = new Map(spec.steps.map((s) => [s.id, s]));
  const availableSteps = spec.steps.filter((s) => !placedSet.has(s.id));

  const addStep = (sid: string) => {
    if (disabled || placedSet.has(sid)) return;
    onChange([...orderedStepIds, sid], justifications);
  };

  const removeStep = (sid: string) => {
    if (disabled) return;
    const nextJust = { ...justifications };
    delete nextJust[sid];
    onChange(
      orderedStepIds.filter((id) => id !== sid),
      nextJust
    );
  };

  const moveStep = (idx: number, delta: -1 | 1) => {
    if (disabled) return;
    const targetIdx = idx + delta;
    if (targetIdx < 0 || targetIdx >= orderedStepIds.length) return;
    const next = [...orderedStepIds];
    const tmp = next[idx];
    next[idx] = next[targetIdx];
    next[targetIdx] = tmp;
    onChange(next, justifications);
  };

  const updateJustification = (sid: string, rule: string) => {
    if (disabled) return;
    onChange(orderedStepIds, { ...justifications, [sid]: rule });
  };

  return (
    <div data-testid="proof-dag-root" className="space-y-4">
      {spec.goal && (
        <div className="p-2.5 bg-blue-50/70 border border-blue-200 rounded-lg text-xs sm:text-sm text-slate-800">
          <span className="font-bold text-ka-blue mr-1.5">Meta:</span>
          <MathText text={spec.goal} inline />
        </div>
      )}

      <div className="space-y-2">
        <div className="flex items-center justify-between text-xs font-bold text-slate-600 uppercase tracking-wider">
          <span>Cadena deductiva ordenada ({orderedStepIds.length})</span>
          <span className="text-[11px] font-normal normal-case text-slate-500">
            Omite pasos falaces y respeta precedencia lógica
          </span>
        </div>

        <div
          data-testid="proof-dropzone"
          className="p-3 rounded-xl border-2 border-dashed border-slate-300 bg-slate-50/60 space-y-2 min-h-[84px]"
        >
          {orderedStepIds.length === 0 ? (
            <p className="text-xs text-slate-500 text-center py-3">
              Añade pasos desde el banco inferior en orden lógico de demostración.
            </p>
          ) : (
            orderedStepIds.map((sid, idx) => {
              const st = stepMap.get(sid);
              if (!st) return null;
              return (
                <StepTile
                  key={sid}
                  step={st}
                  placedIndex={idx}
                  totalPlaced={orderedStepIds.length}
                  disabled={disabled}
                  requireJustification={spec.require_justification}
                  justificationBank={spec.justification_bank || []}
                  selectedJustification={justifications[sid] || ''}
                  onRemove={() => removeStep(sid)}
                  onMoveUp={() => moveStep(idx, -1)}
                  onMoveDown={() => moveStep(idx, 1)}
                  onChangeJustification={(val) => updateJustification(sid, val)}
                />
              );
            })
          )}
        </div>
      </div>

      <div className="space-y-2">
        <div className="text-xs font-bold text-slate-600 uppercase tracking-wider">
          Banco de pasos disponibles ({availableSteps.length})
        </div>
        <div className="grid grid-cols-1 gap-2">
          {availableSteps.map((st) => (
            <StepTile
              key={st.id}
              step={st}
              disabled={disabled}
              onAdd={() => addStep(st.id)}
            />
          ))}
        </div>
      </div>
    </div>
  );
};
