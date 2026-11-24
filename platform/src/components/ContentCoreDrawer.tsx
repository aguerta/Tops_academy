import React, { useEffect, useRef, useState } from 'react';
import { ContentModule } from '../types';
import { MathText } from './MathText';

interface ContentCoreDrawerProps {
  module: ContentModule | null;
  onClose: () => void;
}

type DrawerTab = 'blocks' | 'glossary';

export const ContentCoreDrawer: React.FC<ContentCoreDrawerProps> = ({ module, onClose }) => {
  const [activeTab, setActiveTab] = useState<DrawerTab>('blocks');
  const closeButtonRef = useRef<HTMLButtonElement>(null);
  const dialogRef = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    if (!module) return;
    setActiveTab('blocks');
  }, [module?.id]);

  // Sync native modal dialog state and focus close button
  useEffect(() => {
    const el = dialogRef.current;
    if (!module) {
      if (el?.open) el.close();
      return;
    }
    if (el && !el.open) {
      el.showModal();
    }
    const timer = setTimeout(() => {
      closeButtonRef.current?.focus();
    }, 20);
    return () => {
      clearTimeout(timer);
      if (el?.open) el.close();
    };
  }, [module]);

  if (!module) return null;

  const core = module.core;
  const glossary = module.glossary || [];
  const assumptions = core?.governing_theorems_and_assumptions?.assumptions || [];
  const theoremsLatex = core?.governing_theorems_and_assumptions?.theorems_latex || [];
  const pitfalls = core?.common_exam_pitfalls || [];
  const prereqRecall = core?.prerequisite_recall?.trim() || '';
  const intuitiveAnalogy = core?.intuitive_analogy?.trim() || '';
  const workedExample = core?.worked_example;
  const hasWorkedExample = Boolean(
    workedExample &&
      (workedExample.problem_latex.trim().length > 0 ||
        workedExample.step_by_step_latex.length > 0)
  );

  return (
    <dialog
      ref={dialogRef}
      onCancel={(e) => {
        e.preventDefault();
        onClose();
      }}
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
      aria-labelledby="content-core-drawer-title"
      data-testid="content-core-drawer"
      className="m-0 ml-auto h-full max-h-none w-full max-w-[600px] bg-white shadow-2xl border-l border-ka-border-card p-0 open:flex flex-col min-w-0 backdrop:bg-black/45 backdrop:backdrop-blur-[1px]"
    >
      {/* Slide-over panel compatible with 480px-640px Split View */}
      <div className="w-full h-full flex flex-col min-w-0">
        {/* Header */}
        <header className="px-4 sm:px-6 py-4 border-b border-ka-border-subtle bg-slate-50 flex items-start justify-between gap-3 shrink-0">
          <div className="min-w-0 flex-1">
            <div className="flex flex-wrap items-center gap-2">
              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-bold uppercase tracking-wider bg-blue-100 text-ka-blue border border-blue-200">
                <span>📘</span>
                <span>Núcleo &amp; Glosario</span>
              </span>
              {module.is_prerequisite_module && (
                <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-bold uppercase tracking-wider bg-amber-100 text-amber-800 border border-amber-300">
                  <span>🧭</span>
                  <span>Unidad 0 • Get Ready</span>
                </span>
              )}
              {module.slide_range && (
                <span className="text-[11px] font-semibold text-slate-500">
                  págs. {module.slide_range[0]}–{module.slide_range[1]}
                </span>
              )}
            </div>
            <h2
              id="content-core-drawer-title"
              className="text-base sm:text-lg font-extrabold text-ka-text-primary mt-1.5 break-words [overflow-wrap:anywhere]"
            >
              <MathText text={core?.title || module.title} inline />
            </h2>
            {module.source_file && (
              <p className="text-xs text-slate-500 mt-0.5 truncate">
                📄 {module.source_file}
              </p>
            )}
          </div>

          <button
            ref={closeButtonRef}
            type="button"
            onClick={onClose}
            aria-label="Cerrar visor de núcleo y glosario"
            data-testid="content-core-close"
            className="p-2 rounded-lg text-slate-500 hover:text-slate-800 hover:bg-slate-200/70 transition-colors focus:outline-none focus:ring-2 focus:ring-ka-blue shrink-0"
          >
            <svg
              className="w-5 h-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
              aria-hidden="true"
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </header>

        {/* Tabs */}
        <div
          role="tablist"
          aria-label="Secciones del módulo"
          className="px-4 sm:px-6 border-b border-ka-border-subtle bg-white flex gap-2 shrink-0"
        >
          <button
            type="button"
            role="tab"
            id="tab-blocks"
            aria-selected={activeTab === 'blocks'}
            aria-controls="panel-blocks"
            data-testid="tab-khanmigo-blocks"
            onClick={() => setActiveTab('blocks')}
            className={`px-3 py-2.5 text-xs sm:text-sm font-bold border-b-2 transition-colors whitespace-nowrap ${
              activeTab === 'blocks'
                ? 'border-ka-blue text-ka-blue'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            5 Bloques Khanmigo
          </button>
          <button
            type="button"
            role="tab"
            id="tab-glossary"
            aria-selected={activeTab === 'glossary'}
            aria-controls="panel-glossary"
            data-testid="tab-module-glossary"
            onClick={() => setActiveTab('glossary')}
            className={`px-3 py-2.5 text-xs sm:text-sm font-bold border-b-2 transition-colors whitespace-nowrap flex items-center gap-1.5 ${
              activeTab === 'glossary'
                ? 'border-ka-blue text-ka-blue'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            <span>Glosario del Módulo</span>
            <span className="px-1.5 py-0.2 rounded-full text-[11px] bg-slate-100 text-slate-700">
              {glossary.length}
            </span>
          </button>
        </div>

        {/* Scrollable Body */}
        <div className="flex-1 overflow-y-auto overscroll-contain p-4 sm:p-6 space-y-5 min-w-0">
          {activeTab === 'blocks' ? (
            <div
              role="tabpanel"
              id="panel-blocks"
              aria-labelledby="tab-blocks"
              className="space-y-4"
            >
              {/* Bloque 1: Prerequisite Recall */}
              <section className="p-4 rounded-xl border border-amber-200 bg-amber-50/60">
                <h3 className="text-xs font-extrabold uppercase tracking-wider text-amber-900 flex items-center gap-1.5">
                  <span>1.</span>
                  <span>Prerequisite Recall</span>
                </h3>
                {prereqRecall ? (
                  <div className="mt-2 text-xs sm:text-sm text-amber-950 leading-relaxed break-words [overflow-wrap:anywhere]">
                    <MathText text={prereqRecall} />
                  </div>
                ) : (
                  <p className="mt-2 text-xs text-amber-800/80">
                    No se requieren prerrequisitos explícitos adicionales para este módulo.
                  </p>
                )}
              </section>

              {/* Bloque 2: Intuición */}
              <section className="p-4 rounded-xl border border-blue-200 bg-blue-50/50">
                <h3 className="text-xs font-extrabold uppercase tracking-wider text-blue-900 flex items-center gap-1.5">
                  <span>2.</span>
                  <span>Intuición</span>
                </h3>
                {intuitiveAnalogy ? (
                  <div className="mt-2 text-xs sm:text-sm text-slate-800 leading-relaxed break-words [overflow-wrap:anywhere]">
                    <MathText text={intuitiveAnalogy} />
                  </div>
                ) : (
                  <p className="mt-2 text-xs text-slate-500">
                    Sin resumen intuitivo registrado para este módulo.
                  </p>
                )}
              </section>

              {/* Bloque 3: Teoremas y Supuestos Explícitos */}
              <section className="p-4 rounded-xl border border-indigo-200 bg-indigo-50/40">
                <h3 className="text-xs font-extrabold uppercase tracking-wider text-indigo-900 flex items-center gap-1.5">
                  <span>3.</span>
                  <span>Teoremas y Supuestos Explícitos</span>
                </h3>

                {theoremsLatex.length > 0 && (
                  <div className="mt-2.5 space-y-2">
                    {theoremsLatex.map((thm, idx) => (
                      <div
                        key={idx}
                        className="p-3 rounded-lg bg-white border border-indigo-200 text-xs sm:text-sm text-slate-800 break-words [overflow-wrap:anywhere]"
                      >
                        <MathText text={thm} />
                      </div>
                    ))}
                  </div>
                )}

                {assumptions.length > 0 ? (
                  <div className="mt-3 space-y-2">
                    {assumptions.map((a, idx) => (
                      <div
                        key={a.id || idx}
                        className="p-3 rounded-lg bg-white border border-indigo-200/80 shadow-xs space-y-1.5"
                      >
                        <div className="flex flex-wrap items-center justify-between gap-2">
                          {a.name && (
                            <span className="text-[11px] font-bold uppercase tracking-wide text-indigo-700">
                              {a.name}
                            </span>
                          )}
                          {a.id && (
                            <span className="text-[10px] font-mono text-slate-500 bg-slate-100 px-1.5 py-0.5 rounded">
                              {a.id}
                            </span>
                          )}
                        </div>
                        <div className="text-xs sm:text-sm font-semibold text-slate-900 break-words [overflow-wrap:anywhere]">
                          <MathText text={a.statement_latex} />
                        </div>
                        {a.role_in_proof && (
                          <div className="text-xs text-indigo-900 bg-indigo-50/60 border border-indigo-100 rounded px-2.5 py-1.5 break-words [overflow-wrap:anywhere]">
                            <span className="font-bold">Rol en la prueba: </span>
                            <MathText text={a.role_in_proof} inline />
                          </div>
                        )}
                        <div className="text-xs text-rose-800 bg-rose-50 border border-rose-200 rounded px-2.5 py-1.5 break-words [overflow-wrap:anywhere]">
                          <span className="font-bold">Si se viola: </span>
                          <MathText text={a.violation_consequence} inline />
                        </div>
                      </div>
                    ))}
                  </div>
                ) : theoremsLatex.length === 0 ? (
                  <p className="mt-2 text-xs text-slate-500">
                    No hay supuestos explícitos registrados en este módulo.
                  </p>
                ) : null}
              </section>

              {/* Bloque 4: Ejemplo resuelto */}
              <section className="p-4 rounded-xl border border-emerald-200 bg-emerald-50/50">
                <h3 className="text-xs font-extrabold uppercase tracking-wider text-emerald-900 flex items-center gap-1.5">
                  <span>4.</span>
                  <span>Ejemplo resuelto</span>
                </h3>
                {hasWorkedExample && workedExample ? (
                  <div className="mt-2.5 space-y-2.5">
                    {workedExample.problem_latex && (
                      <div className="p-3 rounded-lg bg-white border border-emerald-200 text-xs sm:text-sm text-slate-900 break-words [overflow-wrap:anywhere]">
                        <div className="text-[11px] font-bold uppercase text-slate-500 mb-1">
                          Problema
                        </div>
                        <MathText text={workedExample.problem_latex} />
                      </div>
                    )}
                    {workedExample.step_by_step_latex.length > 0 && (
                      <div className="p-3 rounded-lg bg-white border border-emerald-200 text-xs sm:text-sm text-slate-800 space-y-2 break-words [overflow-wrap:anywhere]">
                        <div className="text-[11px] font-bold uppercase text-emerald-700">
                          Solución paso a paso
                        </div>
                        <ol className="space-y-1.5 list-decimal list-inside">
                          {workedExample.step_by_step_latex.map((step, sIdx) => (
                            <li key={sIdx} className="leading-relaxed">
                              <MathText text={step} inline />
                            </li>
                          ))}
                        </ol>
                      </div>
                    )}
                  </div>
                ) : (
                  <p className="mt-2 text-xs text-slate-500">
                    No hay ejemplo resuelto disponible para este módulo.
                  </p>
                )}
              </section>

              {/* Bloque 5: Trampas de examen */}
              <section className="p-4 rounded-xl border border-rose-200 bg-rose-50/50">
                <h3 className="text-xs font-extrabold uppercase tracking-wider text-rose-900 flex items-center gap-1.5">
                  <span>5.</span>
                  <span>Trampas de examen</span>
                </h3>
                {pitfalls.length > 0 ? (
                  <ul className="mt-2 space-y-2">
                    {pitfalls.map((pitfall, idx) => (
                      <li
                        key={idx}
                        className="p-2.5 rounded-lg bg-white border border-rose-200 text-xs sm:text-sm text-rose-950 flex items-start gap-2 break-words [overflow-wrap:anywhere]"
                      >
                        <span className="text-rose-600 shrink-0 mt-0.5">⚠️</span>
                        <div className="min-w-0 flex-1">
                          <MathText text={pitfall} />
                        </div>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="mt-2 text-xs text-slate-500">
                    No se han registrado trampas frecuentes en este módulo.
                  </p>
                )}
              </section>
            </div>
          ) : (
            <div
              role="tabpanel"
              id="panel-glossary"
              aria-labelledby="tab-glossary"
              className="space-y-3"
            >
              {glossary.length > 0 ? (
                glossary.map((entry, idx) => (
                  <div
                    key={`${entry.term}-${idx}`}
                    className="p-3.5 rounded-xl border border-ka-border-card bg-slate-50/70 space-y-1.5"
                  >
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <h4 className="text-sm font-bold text-ka-text-primary break-words [overflow-wrap:anywhere]">
                        <MathText text={entry.term} inline />
                      </h4>
                      {entry.related_competencies && entry.related_competencies.length > 0 && (
                        <span className="px-2 py-0.5 rounded bg-white border border-slate-200 text-[11px] font-mono font-semibold text-slate-600 shrink-0">
                          {entry.related_competencies.join(', ')}
                        </span>
                      )}
                    </div>
                    <div className="text-xs sm:text-sm text-ka-text-secondary leading-relaxed break-words [overflow-wrap:anywhere]">
                      <MathText text={entry.definition} />
                    </div>
                    {entry.formula_latex && (
                      <div className="text-xs sm:text-sm text-slate-800 bg-white px-2.5 py-1.5 rounded border border-slate-200 break-words [overflow-wrap:anywhere]">
                        <MathText text={entry.formula_latex} />
                      </div>
                    )}
                  </div>
                ))
              ) : (
                <div className="p-6 text-center rounded-xl border border-dashed border-slate-300 text-xs sm:text-sm text-slate-500">
                  Este módulo no contiene términos de glosario (Fact / Concept) registrados.
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </dialog>
  );
};
