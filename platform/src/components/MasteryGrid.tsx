import React from 'react';
import { Course, CourseMasteryRecord, Competency, MasteryTier } from '../types';
import { TIER_COLORS } from '../utils/masteryStorage';
import { MathText } from './MathText';

interface MasteryGridProps {
  course: Course;
  mastery: CourseMasteryRecord;
  onStartPractice: (competency: Competency) => void;
  onStartQuiz: (competency: Competency) => void;
  onStartUnitTest: (competency: Competency) => void;
}

export const MasteryGrid: React.FC<MasteryGridProps> = ({
  course,
  mastery,
  onStartPractice,
  onStartQuiz,
  onStartUnitTest,
}) => {
  const competencies = course.competencies;

  return (
    <div className="space-y-6 my-6">
      {competencies.map((unit, idx) => {
        const compMastery = mastery.competencies[unit.id];
        const tier: MasteryTier = compMastery?.status || 'Not started';
        const colors = TIER_COLORS[tier];

        const isCompleted =
          tier === 'Mastered' || tier === 'Proficient' || (compMastery?.points ?? 0) >= 80;
        const isInProgress =
          !isCompleted &&
          (tier === 'Familiar' || tier === 'Attempted' || (compMastery?.points ?? 0) > 0);
        const statusLabel = isCompleted ? 'Completed' : isInProgress ? 'In Progress' : 'Not Started';

        return (
          <div
            key={unit.id}
            data-testid={`competency-block-${unit.id}`}
            className={`p-4 sm:p-5 bg-white rounded-lg border border-ka-border-card shadow-sm hover:shadow-md transition-shadow border-l-4 min-w-0 ${
              isCompleted
                ? 'border-l-emerald-500'
                : isInProgress
                ? 'border-l-amber-500'
                : 'border-l-slate-300'
            }`}
          >
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 min-w-0">
              {/* Unit Info */}
              <div className="flex-1 min-w-0">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-slate-500 min-w-0 flex-wrap">
                    <span>Unit {idx + 1}</span>
                    <span>•</span>
                    <span>{unit.category}</span>
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
                  <span>Quiz {idx + 1}</span>
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
