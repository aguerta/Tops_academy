import React, { useEffect, useRef } from 'react';
import { MetacognitiveConfidence, Question } from '../../types';

interface MetacognitiveModalProps {
  isOpen: boolean;
  questions: Question[];
  answeredMap: Record<string, boolean>;
  flaggedMap: Record<string, boolean>;
  itemConfidences: Record<string, MetacognitiveConfidence>;
  globalConfidence: MetacognitiveConfidence | null;
  isTimeExpired?: boolean;
  onSelectGlobalConfidence: (conf: MetacognitiveConfidence) => void;
  onSelectItemConfidence: (questionId: string, conf: MetacognitiveConfidence) => void;
  onCancel: () => void;
  onConfirm: () => void;
}

const CONF_OPTIONS: Array<{
  value: MetacognitiveConfidence;
  label: string;
  desc: string;
}> = [
  {
    value: 'high',
    label: 'Alta certeza',
    desc: 'Seguro de mi planteamiento y resultado',
  },
  {
    value: 'medium',
    label: 'Certeza media',
    desc: 'Razonamiento parcial o con dudas menores',
  },
  {
    value: 'low',
    label: 'Baja certeza / Conjetura',
    desc: 'Estimación exploratoria o hipótesis abierta',
  },
];

export const MetacognitiveModal: React.FC<MetacognitiveModalProps> = ({
  isOpen,
  questions,
  answeredMap,
  flaggedMap,
  itemConfidences,
  globalConfidence,
  isTimeExpired = false,
  onSelectGlobalConfidence,
  onSelectItemConfidence,
  onCancel,
  onConfirm,
}) => {
  const dialogRef = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    const el = dialogRef.current;
    if (!isOpen) {
      if (el?.open) el.close();
      return;
    }
    if (el && !el.open) {
      el.showModal();
    }
    return () => {
      if (el?.open) el.close();
    };
  }, [isOpen]);

  if (!isOpen) return null;

  const total = questions.length;
  const answeredCount = questions.filter((q) => answeredMap[q.id]).length;
  const unansweredCount = total - answeredCount;
  const flaggedCount = questions.filter((q) => flaggedMap[q.id]).length;
  const allItemsCalibrated =
    total > 0 && questions.every((q) => Boolean(itemConfidences[q.id]));
  const canConfirm = total > 0 && (globalConfidence !== null || allItemsCalibrated);

  return (
    <dialog
      ref={dialogRef}
      onCancel={(e) => {
        e.preventDefault();
        if (!isTimeExpired) onCancel();
      }}
      onClick={(e) => {
        if (e.target === e.currentTarget && !isTimeExpired) onCancel();
      }}
      aria-labelledby="metacognitive-modal-title"
      data-testid="metacognitive-modal"
      className="m-auto w-[calc(100%-1.5rem)] sm:w-[calc(100%-2rem)] max-w-lg bg-white rounded-xl border border-slate-200 shadow-2xl p-4 sm:p-6 max-h-[92dvh] overflow-y-auto min-w-0 backdrop:bg-slate-900/60"
    >
      <div className="space-y-4">
        <div className="space-y-1">
          <div className="text-[11px] font-extrabold uppercase tracking-wider text-indigo-700">
            Auditoría Metacognitiva Pre-Calificación
          </div>
          <h2
            id="metacognitive-modal-title"
            className="text-lg sm:text-xl font-extrabold text-slate-900 break-words"
          >
            Calibra tu nivel de certeza antes de ver resultados
          </h2>
          <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
            Registrar tu confianza previa permite detectar{' '}
            <strong>ilusiones de competencia</strong> (alta seguridad + error) frente a{' '}
            <strong>dominio calibrado</strong>.
          </p>
        </div>

        {isTimeExpired && (
          <div
            role="alert"
            data-testid="iron-time-expired-banner"
            className="p-2.5 rounded-lg bg-rose-50 border border-rose-300 text-rose-900 text-xs font-bold"
          >
            Tiempo agotado: el examen se cerró automáticamente. Selecciona tu nivel de certeza para calificar y ver resultados.
          </div>
        )}

        {/* Completeness summary */}
        <div className="grid grid-cols-3 gap-2 text-center text-xs">
          <div className="p-2 rounded-lg bg-slate-50 border border-slate-200">
            <div className="text-base font-extrabold text-slate-900">
              {answeredCount}/{total}
            </div>
            <div className="text-slate-600">Respondidas</div>
          </div>
          <div
            className={`p-2 rounded-lg border ${
              unansweredCount > 0
                ? 'bg-amber-50 border-amber-300 text-amber-900'
                : 'bg-emerald-50 border-emerald-200 text-emerald-900'
            }`}
          >
            <div className="text-base font-extrabold">{unansweredCount}</div>
            <div>Sin responder</div>
          </div>
          <div className="p-2 rounded-lg bg-slate-50 border border-slate-200">
            <div className="text-base font-extrabold text-slate-900">{flaggedCount}</div>
            <div className="text-slate-600">Marcadas</div>
          </div>
        </div>

        {/* Global fallback confidence selector */}
        <div className="space-y-2">
          <div className="text-xs font-bold uppercase tracking-wider text-slate-700">
            Certeza global predeterminada del examen
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
            {CONF_OPTIONS.map((opt) => {
              const active = globalConfidence === opt.value;
              return (
                <button
                  key={opt.value}
                  type="button"
                  data-testid={`meta-global-confidence-${opt.value}`}
                  aria-pressed={active}
                  onClick={() => onSelectGlobalConfidence(opt.value)}
                  className={`p-2.5 rounded-lg border-2 text-left transition-all cursor-pointer ${
                    active
                      ? 'border-ka-blue bg-blue-50 text-ka-blue'
                      : 'border-slate-200 bg-white text-slate-800 hover:border-slate-300'
                  }`}
                >
                  <div className="text-xs font-bold">{opt.label}</div>
                  <div className="text-[11px] text-slate-600 mt-0.5 leading-snug">{opt.desc}</div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Per-item confidence fine-tuning */}
        {questions.length > 0 && (
          <div className="space-y-1.5">
            <div className="text-xs font-bold uppercase tracking-wider text-slate-600">
              Ajuste fino por ítem (opcional)
            </div>
            <div className="max-h-40 overflow-y-auto divide-y divide-slate-100 border border-slate-200 rounded-lg bg-slate-50">
              {questions.map((q, idx) => {
                const eff = itemConfidences[q.id] ?? globalConfidence;
                return (
                  <div
                    key={q.id}
                    className="px-2.5 py-1.5 flex items-center justify-between gap-2 text-xs"
                  >
                    <span className="font-medium text-slate-700 truncate min-w-0">
                      #{idx + 1} • {answeredMap[q.id] ? 'Respondida' : 'En blanco'}
                      {flaggedMap[q.id] ? ' • ⚑' : ''}
                    </span>
                    <div className="flex items-center gap-1 shrink-0">
                      {(['high', 'medium', 'low'] as MetacognitiveConfidence[]).map((c) => (
                        <button
                          key={c}
                          type="button"
                          onClick={() => onSelectItemConfidence(q.id, c)}
                          className={`px-2 py-0.5 rounded border text-[11px] font-bold cursor-pointer ${
                            eff === c
                              ? 'bg-ka-blue text-white border-ka-blue'
                              : 'bg-white text-slate-600 border-slate-300'
                          }`}
                        >
                          {c === 'high' ? 'Alta' : c === 'medium' ? 'Media' : 'Baja'}
                        </button>
                      ))}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {!canConfirm && (
          <p
            data-testid="metacognitive-required-notice"
            className="text-xs font-semibold text-amber-800 bg-amber-50 border border-amber-200 rounded-lg px-3 py-2"
          >
            Selecciona tu nivel de certeza global o por ítem antes de ver resultados.
          </p>
        )}

        <div className="flex flex-col-reverse sm:flex-row sm:justify-end gap-2 pt-2 border-t border-slate-200">
          {!isTimeExpired && (
            <button
              type="button"
              data-testid="metacognitive-cancel-btn"
              onClick={onCancel}
              className="px-4 py-2 rounded-lg border border-slate-300 text-xs sm:text-sm font-bold text-slate-700 hover:bg-slate-50 cursor-pointer"
            >
              Volver al examen
            </button>
          )}
          <button
            type="button"
            data-testid="metacognitive-confirm-btn"
            disabled={!canConfirm}
            onClick={onConfirm}
            className="px-5 py-2 rounded-lg bg-ka-blue hover:bg-ka-blue-hover disabled:bg-slate-300 disabled:text-slate-500 disabled:cursor-not-allowed text-white text-xs sm:text-sm font-bold shadow-sm cursor-pointer"
          >
            Confirmar y ver resultados
          </button>
        </div>
      </div>
    </dialog>
  );
};
