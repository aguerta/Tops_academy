import React from 'react';
import { UnstructuredModelSpec } from '../types';
import { MathText } from './MathText';
import { SymbolicInput } from './SymbolicInput';

export interface Stage0AnswerState {
  phase1Roles: Record<string, string>;
  phase2SelectedIds: string[];
  phase3SelectedId: string | null;
  phase3Expression: string;
}

interface Stage0ModelerProps {
  spec: UnstructuredModelSpec;
  activePhase: 1 | 2 | 3;
  value: Stage0AnswerState;
  disabled?: boolean;
  isChecked?: boolean;
  isCorrect?: boolean | null;
  onChange: (next: Stage0AnswerState) => void;
}

const ROLE_LABELS: Record<string, string> = {
  parametro_conocido: 'Parámetro conocido',
  parametro: 'Parámetro conocido',
  incognita: 'Incógnita / variable a resolver',
  variable_estado: 'Variable de estado',
  variable_control: 'Variable de decisión',
  distractor_irrelevante: 'Dato irrelevante / distractor',
  irrelevante: 'Dato irrelevante',
};

function formatRoleLabel(role: string): string {
  return ROLE_LABELS[role] || role.replace(/_/g, ' ');
}

export const Stage0Modeler: React.FC<Stage0ModelerProps> = ({
  spec,
  activePhase,
  value,
  disabled = false,
  isChecked = false,
  isCorrect = null,
  onChange,
}) => {
  const phases = [
    { num: 1 as const, label: 'Fase 1: Variables' },
    { num: 2 as const, label: 'Fase 2: Supuestos' },
    { num: 3 as const, label: 'Fase 3: Formulación' },
  ];

  return (
    <div data-testid="stage0-modeler-root" className="space-y-4">
      {/* Sequential Locked Stepper Header */}
      <div className="grid grid-cols-3 gap-2" role="tablist" aria-label="Fases de modelado">
        {phases.map((p) => {
          const isDone = activePhase > p.num || (isChecked && isCorrect === true);
          const isCurrent = activePhase === p.num && !(isChecked && isCorrect === true);
          const isLocked = activePhase < p.num;

          return (
            <div
              key={p.num}
              data-testid={`stage0-phase-${p.num}`}
              data-phase-state={isDone ? 'completed' : isCurrent ? 'active' : 'locked'}
              className={`px-2.5 py-2 rounded-lg border text-xs font-bold flex items-center justify-between gap-1 ${
                isDone
                  ? 'bg-emerald-50 border-ka-green-border text-ka-green-text'
                  : isCurrent
                  ? 'bg-blue-50 border-ka-blue text-ka-blue shadow-2xs'
                  : 'bg-slate-100 border-slate-200 text-slate-400'
              }`}
            >
              <span className="truncate">{p.label}</span>
              <span aria-hidden="true" className="shrink-0">
                {isDone ? '✓' : isLocked ? '🔒' : '●'}
              </span>
            </div>
          );
        })}
      </div>

      {/* Phase 1: Classify Variables & Filter Irrelevant Data */}
      {activePhase === 1 && (
        <div data-testid="stage0-phase1-body" className="space-y-3 p-3.5 rounded-xl border border-slate-200 bg-white">
          <div className="text-xs sm:text-sm font-bold text-ka-text-primary">
            <MathText text={spec.phase1_variables.prompt} inline />
          </div>
          <div className="space-y-2.5">
            {spec.phase1_variables.items.map((item) => (
              <div
                key={item.id}
                className="p-2.5 rounded-lg bg-slate-50 border border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-2"
              >
                <div className="text-xs sm:text-sm text-slate-800 font-medium min-w-0">
                  <MathText text={item.label} inline />
                </div>
                <select
                  data-testid={`stage0-select-${item.id}`}
                  aria-label={`Rol para ${item.label}`}
                  disabled={disabled}
                  value={value.phase1Roles[item.id] || ''}
                  onChange={(e) =>
                    onChange({
                      ...value,
                      phase1Roles: { ...value.phase1Roles, [item.id]: e.target.value },
                    })
                  }
                  className="text-xs sm:text-sm px-2.5 py-1.5 rounded border border-slate-300 bg-white text-slate-800 outline-none focus:border-ka-blue shrink-0"
                >
                  <option value="">-- Selecciona rol --</option>
                  {spec.phase1_variables.roles.map((r) => (
                    <option key={r} value={r}>
                      {formatRoleLabel(r)}
                    </option>
                  ))}
                </select>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Phase 2: Select Active Domain Assumptions */}
      {activePhase === 2 && (
        <div data-testid="stage0-phase2-body" className="space-y-3 p-3.5 rounded-xl border border-slate-200 bg-white">
          <div className="text-xs sm:text-sm font-bold text-ka-text-primary">
            <MathText text={spec.phase2_assumptions.prompt} inline />
          </div>
          <div className="space-y-2">
            {spec.phase2_assumptions.options.map((opt) => {
              const checked = value.phase2SelectedIds.includes(opt.id);
              return (
                <label
                  key={opt.id}
                  data-testid={`stage0-p2-${opt.id}`}
                  className={`p-3 rounded-lg border-2 flex items-start gap-2.5 cursor-pointer transition-all ${
                    checked
                      ? 'border-ka-blue bg-blue-50/60'
                      : 'border-slate-200 bg-slate-50/50 hover:border-slate-300'
                  }`}
                >
                  <input
                    type="checkbox"
                    disabled={disabled}
                    checked={checked}
                    onChange={() => {
                      const nextIds = checked
                        ? value.phase2SelectedIds.filter((id) => id !== opt.id)
                        : [...value.phase2SelectedIds, opt.id];
                      onChange({ ...value, phase2SelectedIds: nextIds });
                    }}
                    className="mt-0.5 w-4 h-4 accent-ka-blue shrink-0"
                  />
                  <div className="text-xs sm:text-sm text-slate-800 min-w-0 flex-1">
                    <MathText text={opt.content} inline />
                  </div>
                </label>
              );
            })}
          </div>
        </div>
      )}

      {/* Phase 3: Formal Translation */}
      {activePhase === 3 && (
        <div data-testid="stage0-phase3-body" className="space-y-3 p-3.5 rounded-xl border border-slate-200 bg-white">
          <div className="text-xs sm:text-sm font-bold text-ka-text-primary">
            <MathText text={spec.phase3_formulation.prompt} inline />
          </div>

          {spec.phase3_formulation.input_mode === 'select' ? (
            <div className="space-y-2" role="radiogroup" aria-label="Formulación formal">
              {(spec.phase3_formulation.options || []).map((opt) => {
                const selected = value.phase3SelectedId === opt.id;
                return (
                  <button
                    key={opt.id}
                    type="button"
                    disabled={disabled}
                    role="radio"
                    aria-checked={selected}
                    data-testid={`stage0-p3-${opt.id}`}
                    onClick={() =>
                      onChange({
                        ...value,
                        phase3SelectedId: selected ? null : opt.id,
                      })
                    }
                    className={`w-full text-left p-3 rounded-lg border-2 transition-all text-xs sm:text-sm cursor-pointer ${
                      selected
                        ? 'border-ka-blue bg-blue-50/70 text-ka-text-primary'
                        : 'border-slate-200 bg-slate-50 hover:border-slate-300 text-slate-800'
                    }`}
                  >
                    <MathText text={opt.content} inline />
                  </button>
                );
              })}
            </div>
          ) : (
            <SymbolicInput
              value={value.phase3Expression}
              disabled={disabled}
              isChecked={isChecked}
              isCorrect={isCorrect}
              onChange={(expr) => onChange({ ...value, phase3Expression: expr })}
              placeholder="Traduce el modelo a una ecuación simbólica..."
            />
          )}
        </div>
      )}
    </div>
  );
};
