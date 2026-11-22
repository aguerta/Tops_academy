import React, { useState } from 'react';
import { Course, CourseMasteryRecord, Competency, MasteryTier } from '../types';
import {
  getCompetencyRetrievability,
  isUnitCompleted,
  isUnitStarted,
  TIER_COLORS,
} from '../utils/masteryStorage';
import { formatCooldownRemaining, getCooldownRemainingMs } from '../utils/fsrsEngine';
import { MathText } from './MathText';

interface MasteryGridProps {
  course: Course;
  mastery: CourseMasteryRecord;
  onStartPractice: (competency: Competency) => void;
  onStartQuiz: (competency: Competency) => void;
  onStartUnitTest: (competency: Competency) => void;
  competenciesOverride?: Competency[];
}

export const MasteryGrid: React.FC<MasteryGridProps> = ({
  course,
  mastery,
  onStartPractice,
  onStartQuiz,
  onStartUnitTest,
  competenciesOverride,
}) => {
  const [expandedAssumptions, setExpandedAssumptions] = useState<Record<string, boolean>>({});
  const competencies = competenciesOverride ?? course.competencies;

  const toggleAssumptions = (unitId: string) => {
    setExpandedAssumptions((prev) => ({ ...prev, [unitId]: !prev[unitId] }));
  };

  return (
    <div className="space-y-6 my-6">
      {competencies.map((unit, idx) => {
        const globalIdx = course.competencies.findIndex((c) => c.id === unit.id);
        // Numbering follows pedagogical order (position in course.competencies).
        // `unit_index` is a source PDF page number, so it must not be used here.
        const displayIdx = globalIdx >= 0 ? globalIdx : idx;
        const compMastery = mastery.competencies[unit.id];
        const tier: MasteryTier = compMastery?.status || 'Not started';
        const colors = TIER_COLORS[tier];

        const isCompleted = isUnitCompleted(compMastery);
        const isInProgress = !isCompleted && isUnitStarted(compMastery);
        const statusLabel = isCompleted ? 'Completed' : isInProgress ? 'In Progress' : 'Not Started';

        const isPrereq = unit.is_prerequisite === true || unit.id.startsWith('PRE-');
        const firstEvidence = unit.evidence?.[0];
        const evidenceDocRaw = firstEvidence?.doc || firstEvidence?.pdf;
        const evidenceDoc = evidenceDocRaw
          ? evidenceDocRaw.split(/[\\/]/).pop() || evidenceDocRaw
          : undefined;
        const evidencePage =
          firstEvidence?.page ?? firstEvidence?.slide ?? firstEvidence?.pages?.[0];
        const hasAssumptions = Boolean(unit.assumptions && unit.assumptions.length > 0);
        const isAssumptionsOpen = Boolean(expandedAssumptions[unit.id]);
        const isDecayReview = Boolean(
          compMastery?.needs_review && compMastery.review_reason === 'decay'
        );
        const hasFsrsCard = Boolean(
          compMastery?.fsrs && compMastery.fsrs.state !== 0 && compMastery.fsrs.last_review
        );
        const retrievabilityPct = hasFsrsCard
          ? Math.round(getCompetencyRetrievability(compMastery) * 100)
          : null;
        const cooldownMs =
          tier === 'Proficient'
            ? getCooldownRemainingMs(
                compMastery?.last_tier_promotion_at || compMastery?.last_practiced
              )
            : 0;

        return (
          <div
            key={unit.id}
            data-testid={`competency-block-${unit.id}`}
            className={`p-4 sm:p-5 bg-white rounded-lg border border-ka-border-card shadow-sm hover:shadow-md transition-shadow border-l-4 min-w-0 ${
              isCompleted
                ? 'border-l-emerald-600'
                : isInProgress
                ? 'border-l-amber-400'
                : 'border-l-slate-200'
            }`}
          >
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 min-w-0">
              {/* Unit Info */}
              <div className="flex-1 min-w-0">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-slate-500 min-w-0 flex-wrap">
                    <span>Unit {displayIdx + 1}</span>
                    <span>•</span>
                    <span>{unit.category}</span>
                    {isPrereq && (
                      <span
                        data-testid={`prereq-badge-${unit.id}`}
                        className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-extrabold bg-amber-100 text-amber-900 border border-amber-300"
                      >
                        🧭 UNIDAD 0 • GET READY
                      </span>
                    )}
                    {firstEvidence && (
                      <span
                        data-testid={`evidence-badge-${unit.id}`}
                        className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-semibold normal-case tracking-normal bg-slate-100 text-slate-700 border border-slate-200 max-w-full truncate"
                      >
                        <span>📄</span>
                        <span className="truncate">
                          {evidenceDoc || 'Documento'}
                          {evidencePage !== undefined ? ` • pág. ${evidencePage}` : ''}
                        </span>
                      </span>
                    )}
                    {compMastery?.needs_review && (
                      <span
                        data-testid={`red-dot-${unit.id}`}
                        className={`w-2.5 h-2.5 rounded-full inline-block shadow-sm animate-pulse ${
                          isDecayReview ? 'bg-amber-500' : 'bg-rose-500'
                        }`}
                        title={
                          isDecayReview
                            ? `Repaso espaciado sugerido (R(t) ${retrievabilityPct ?? '--'}%)`
                            : 'Requiere repaso (laguna conceptual detectada)'
                        }
                      />
                    )}
                  </div>
                  {/* Unit Completion Status Badge */}
                  {isCompleted ? (
                    <span
                      data-testid={`unit-status-${unit.id}`}
                      className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-300 shadow-sm"
                    >
                      <span>✓</span>
                      <span>Completed</span>
                    </span>
                  ) : isInProgress ? (
                    <span
                      data-testid={`unit-status-${unit.id}`}
                      className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-bold bg-amber-100 text-amber-800 border border-amber-300"
                    >
                      <span>⏳</span>
                      <span>In Progress</span>
                    </span>
                  ) : (
                    <span
                      data-testid={`unit-status-${unit.id}`}
                      className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-bold bg-slate-100 text-slate-600 border border-slate-300"
                    >
                      <span>○</span>
                      <span>Not Started</span>
                    </span>
                  )}
                </div>
                <h3 className="text-base sm:text-lg font-bold text-ka-text-primary mt-1 break-words [overflow-wrap:anywhere]">
                  <MathText text={unit.name} inline />
                </h3>
                <div className="text-xs text-ka-text-secondary mt-1 break-words [overflow-wrap:anywhere]">
                  <MathText text={unit.description} />
                </div>

                {/* Mastery Status Pill & Status Text */}
                <div className="mt-3 flex flex-wrap items-center gap-2">
                  <span
                    className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded text-xs font-bold"
                    style={{
                      backgroundColor: colors.bg,
                      color: colors.text,
                      border: `1.5px solid ${colors.border}`,
                    }}
                  >
                    <span>👑</span>
                    <span>{tier}</span>
                  </span>
                  <span className="text-xs text-slate-500 font-medium">
                    {compMastery?.points || 0} / 100 mastery points
                  </span>
                  <span className="text-slate-300">•</span>
                  <span
                    className={`text-xs font-semibold ${
                      isCompleted
                        ? 'text-emerald-700'
                        : isInProgress
                        ? 'text-amber-700'
                        : 'text-slate-500'
                    }`}
                  >
                    Status: {statusLabel}
                  </span>
                </div>

                {/* Milestone 14: Fluency Timing line and Needs Review Badge */}
                {(() => {
                  const allTimings = Object.values(compMastery?.timing || {});
                  const bestAvg = allTimings
                    .map((t) => t.best_avg_seconds_per_question)
                    .filter((n): n is number => n !== undefined)
                    .sort((a, b) => a - b)[0];
                  const lastAvg = allTimings
                    .map((t) => t.last_avg_seconds_per_question)
                    .filter((n): n is number => n !== undefined)[0];

                  if (
                    bestAvg === undefined &&
                    lastAvg === undefined &&
                    !compMastery?.needs_review &&
                    retrievabilityPct === null &&
                    cooldownMs <= 0
                  ) {
                    return null;
                  }

                  return (
                    <div className="mt-2.5 flex flex-wrap items-center gap-2 text-xs text-slate-500">
                      {bestAvg !== undefined && (
                        <span className="inline-flex items-center gap-1 font-semibold text-slate-700 bg-slate-100 px-2 py-0.5 rounded border border-slate-200">
                          <span>⏱️ Récord:</span>
                          <strong className="text-slate-900">{bestAvg}s/preg</strong>
                        </span>
                      )}
                      {lastAvg !== undefined && (
                        <span className="text-slate-500 font-medium text-[11px]">
                          Último: {lastAvg}s/preg
                        </span>
                      )}
                      {retrievabilityPct !== null && (
                        <span
                          data-testid={`fsrs-retention-pill-${unit.id}`}
                          className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-semibold border ${
                            retrievabilityPct >= 85
                              ? 'bg-emerald-50 text-emerald-800 border-emerald-200'
                              : retrievabilityPct >= 50
                              ? 'bg-amber-50 text-amber-900 border-amber-200'
                              : 'bg-rose-50 text-rose-800 border-rose-200'
                          }`}
                        >
                          <span>🧠 R(t) {retrievabilityPct}%</span>
                        </span>
                      )}
                      {cooldownMs > 0 && (
                        <span
                          data-testid={`cooldown-pill-${unit.id}`}
                          className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-semibold bg-indigo-50 text-indigo-800 border border-indigo-200"
                          title="Ventana mínima de consolidación antes de poder ascender a Mastered"
                        >
                          <span>⏳ Cooldown 12h ({formatCooldownRemaining(cooldownMs)})</span>
                        </span>
                      )}
                      {compMastery?.needs_review && (
                        <span
                          data-testid={`needs-review-badge-${unit.id}`}
                          className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-bold border ${
                            isDecayReview
                              ? 'bg-amber-100 text-amber-900 border-amber-300'
                              : 'bg-rose-100 text-rose-800 border-rose-300'
                          }`}
                        >
                          <span>
                            {isDecayReview
                              ? `⏳ Repaso FSRS (${retrievabilityPct ?? '--'}%)`
                              : '🔴 Requiere repaso'}
                          </span>
                        </span>
                      )}
                    </div>
                  );
                })()}

                {/* Lightweight Collapsible for Explicit Assumptions */}
                {hasAssumptions && (
                  <div className="mt-2.5">
                    <button
                      type="button"
                      onClick={() => toggleAssumptions(unit.id)}
                      aria-expanded={isAssumptionsOpen}
                      data-testid={`assumptions-toggle-${unit.id}`}
                      className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded text-xs font-semibold bg-indigo-50 hover:bg-indigo-100 text-indigo-800 border border-indigo-200 transition-colors"
                    >
                      <span>⚖️ Supuestos explícitos ({unit.assumptions!.length})</span>
                      <span className="text-[10px]">{isAssumptionsOpen ? '▲' : '▼'}</span>
                    </button>
                    {isAssumptionsOpen && (
                      <div className="mt-2 space-y-1.5 pl-3 border-l-2 border-indigo-200">
                        {unit.assumptions!.map((a, aIdx) => (
                          <div
                            key={a.id || aIdx}
                            className="p-2 rounded bg-indigo-50/50 border border-indigo-100 text-xs space-y-1 break-words [overflow-wrap:anywhere]"
                          >
                            <div className="font-semibold text-slate-900">
                              <MathText text={a.statement_latex} inline />
                            </div>
                            <div className="text-rose-800">
                              <span className="font-bold">Si se viola: </span>
                              <MathText text={a.violation_consequence} inline />
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>

              {/* Assessment & Practice Triggers */}
              <div className="flex flex-wrap items-center gap-2 pt-3 md:pt-0 border-t md:border-t-0 border-ka-border-subtle shrink-0">
                {/* Competency Mastery Block / Practice Trigger */}
                <button
                  type="button"
                  data-testid={`competency-${unit.id}`}
                  onClick={() => onStartPractice(unit)}
                  className="px-4 py-2 bg-ka-blue hover:bg-ka-blue-hover text-white text-sm font-semibold rounded shadow-sm flex items-center gap-2 transition-colors shrink-0"
                >
                  <span>Practice</span>
                </button>

                {/* Quiz Trigger */}
                <button
                  type="button"
                  data-testid={`quiz-marker-${unit.id}`}
                  onClick={() => onStartQuiz(unit)}
                  className="px-3 py-2 bg-slate-100 hover:bg-slate-200 text-slate-800 text-sm font-semibold rounded border border-slate-200 flex items-center gap-1.5 transition-colors shrink-0"
                >
                  <span className="text-amber-500">⚡</span>
                  <span>Quiz {displayIdx + 1}</span>
                </button>

                {/* Unit Test Trigger */}
                <button
                  type="button"
                  data-testid={`unit-test-marker-${unit.id}`}
                  onClick={() => onStartUnitTest(unit)}
                  className="px-3 py-2 bg-slate-100 hover:bg-slate-200 text-slate-800 text-sm font-semibold rounded border border-slate-200 flex items-center gap-1.5 transition-colors shrink-0"
                >
                  <span className="text-purple-600">★</span>
                  <span>Unit test</span>
                </button>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};
