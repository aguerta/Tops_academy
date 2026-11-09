import React, { useEffect, useMemo } from 'react';
import confetti from 'canvas-confetti';
import {
  Competency,
  Course,
  ChallengeExecutionSummary,
  MasteryTier,
} from '../types';
import { MathText } from './MathText';
import { formatTimingSeconds, TIER_COLORS, TIER_POINTS } from '../utils/masteryStorage';

interface CompletionScreenProps {
  course: Course;
  competency?: Competency;
  score: number;
  total: number;
  sessionType: 'practice' | 'quiz' | 'test' | 'challenge';
  onTryAgain: () => void;
  onUpNext: () => void;
  onBackToCourse: () => void;
  onRemediateCompetency?: (comp: Competency) => void;
  challengeSummary?: ChallengeExecutionSummary | null;
  timingData?: {
    totalSeconds?: number;
    avgSeconds?: number;
    isNewRecord?: boolean;
    previousTier?: MasteryTier;
    newTier?: MasteryTier;
  };
  misconceptions?: Array<{
    question_id: string;
    competency_id: string;
    competency_name?: string;
    text: string;
  }>;
}

export const CompletionScreen: React.FC<CompletionScreenProps> = ({
  course,
  competency,
  score,
  total,
  sessionType,
  onTryAgain,
  onUpNext,
  onBackToCourse,
  onRemediateCompetency,
  challengeSummary,
  timingData,
  misconceptions,
}) => {
  const isPerfect = total > 0 && score === total;
  const isZero = score === 0;
  const resultEmoji = isPerfect ? '🤩' : isZero ? '😢' : '🙂';
  const resultMessage = isPerfect
    ? 'Great work! Your practice points have been recorded in your course mastery progress.'
    : isZero
    ? "Don't give up! Review the material and try again."
    : 'Good effort! Review the missed concepts below to reach full mastery.';

  useEffect(() => {
    // Confetti only for a perfect score
    if (!isPerfect) return;
    const end = Date.now() + 1500;
    const colors = ['#1865f2', '#14a34b', '#e07a21', '#583b8b', '#06b6d4'];

    const frame = () => {
      confetti({
        particleCount: 3,
        angle: 60,
        spread: 55,
        origin: { x: 0 },
        colors,
      });
      confetti({
        particleCount: 3,
        angle: 120,
        spread: 55,
        origin: { x: 1 },
        colors,
      });

      if (Date.now() < end) {
        requestAnimationFrame(frame);
      }
    };
    frame();
  }, [isPerfect]);

  // Enter key navigation to advance or return to course overview
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.isComposing) return;
      if (e.key === 'Enter') {
        e.preventDefault();
        onUpNext();
      } else if (
        e.key === 'Escape' ||
        (e.key.toLowerCase() === 'v' && (e.ctrlKey || e.metaKey) && !e.altKey)
      ) {
        if (e.key === 'Escape' && document.querySelector('[role="dialog"]')) return;
        e.preventDefault();
        onBackToCourse();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [onUpNext, onBackToCourse]);

  const titlePrefix =
    sessionType === 'challenge'
      ? 'Course challenge complete!'
      : sessionType === 'test'
      ? 'Unit test complete!'
      : sessionType === 'quiz'
      ? 'Quiz complete!'
      : 'Exercise complete!';

  // Find next competency if available
  const currentIndex = competency
    ? course.competencies.findIndex((c) => c.id === competency.id)
    : -1;
  const nextCompetency =
    currentIndex >= 0 && currentIndex < course.competencies.length - 1
      ? course.competencies[currentIndex + 1]
      : null;

  const leveledUpList = challengeSummary?.skills_leveled_up || [];
  const leveledDownList = challengeSummary?.skills_leveled_down || [];
  const skillsMaintainedList = challengeSummary?.skills_maintained || [];
  const activeMisconceptions =
    challengeSummary?.misconceptions || misconceptions || [];

  // Consolidate misconceptions by competency/unit to avoid repeating the same unit multiple times
  const consolidatedAreas = useMemo(() => {
    const map = new Map<
      string,
      {
        competency_id: string;
        competency_name: string;
        count: number;
        targetComp?: Competency;
      }
    >();

    for (const m of activeMisconceptions) {
      const id = m.competency_id || (competency ? competency.id : 'unknown');
      const name = m.competency_name || (competency ? competency.name : 'Unidad');
      const existing = map.get(id);
      if (existing) {
        existing.count += 1;
      } else {
        const targetComp =
          course.competencies.find((c) => c.id === id) ||
          (competency?.id === id ? competency : undefined);
        map.set(id, {
          competency_id: id,
          competency_name: name,
          count: 1,
          targetComp,
        });
      }
    }

    return Array.from(map.values());
  }, [activeMisconceptions, course.competencies, competency]);

  return (
    <div
      data-testid="completion-screen"
      className="min-h-screen min-h-[100dvh] bg-slate-50 flex flex-col justify-between overflow-x-hidden"
    >
      {/* Top Header */}
      <header className="h-16 bg-white border-b border-ka-border-card px-4 sm:px-6 flex items-center justify-between gap-3 min-w-0 shrink-0">
        <div className="flex items-center gap-2 min-w-0 flex-1">
          <span className="text-sm font-bold text-ka-text-primary truncate block min-w-0">
            <MathText text={competency ? competency.name : course.title} inline />
          </span>
        </div>
        <button
          type="button"
          onClick={onBackToCourse}
          title="Back to course (Ctrl+V)"
          className="text-xs font-semibold text-ka-blue hover:text-ka-blue-hover shrink-0 flex items-center gap-1.5"
        >
          Back to course
          <kbd className="hidden sm:inline px-1.5 py-0.5 text-[10px] font-bold bg-slate-100 border border-slate-300 rounded text-slate-600">
            Ctrl+V
          </kbd>
        </button>
      </header>

      <p
        className="bg-blue-50 text-ka-blue text-xs text-center py-1.5 px-4 border-b border-blue-100"
        data-testid="shortcut-hint"
      >
        💡 Press <kbd className="px-1 font-bold bg-white border border-blue-200 rounded">Enter</kbd>{' '}
        {nextCompetency
          ? `for the next ${sessionType === 'quiz' ? 'quiz' : sessionType === 'test' ? 'unit test' : 'practice'}`
          : 'to go back to the course'}
        , or <kbd className="px-1 font-bold bg-white border border-blue-200 rounded">Ctrl+V</kbd> to go back to the course.
      </p>

      {/* Main Celebratory Container */}
      <div className="flex-1 flex items-center justify-center p-4 sm:p-6 min-w-0">
        <div className="w-full max-w-4xl bg-ka-blue rounded-2xl p-6 sm:p-8 text-white shadow-xl flex flex-col lg:flex-row items-center lg:items-start justify-between gap-6 sm:gap-8 relative overflow-hidden min-w-0">
          {/* Left Hero Content: Result Emoji, score & Timing Metrics */}
          <div className="flex flex-col items-center lg:items-start text-center lg:text-left min-w-0 flex-1">
            <div className="w-16 h-16 sm:w-20 sm:h-20 mb-3 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center text-3xl sm:text-4xl shadow-inner">
              {resultEmoji}
            </div>

            <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight break-words [overflow-wrap:anywhere]">
              {titlePrefix}
            </h1>
            <p className="text-xl sm:text-2xl font-bold text-blue-100 mt-1">
              {score}/{total} correct ({total > 0 ? Math.round((score / total) * 100) : 0}%)
            </p>
            <p className="text-xs sm:text-sm text-blue-200 mt-1 max-w-sm">
              {resultMessage}
            </p>

            {/* Timing & Fluency Badge */}
            <div className="mt-4 p-3 bg-white/10 backdrop-blur-md rounded-xl border border-white/20 text-xs text-left w-full max-w-sm space-y-1">
              <div className="flex items-center justify-between font-bold">
                <span className="flex items-center gap-1 text-blue-100">
                  <span>⏱️</span>
                  <span>Tiempo promedio:</span>
                </span>
                <span className="text-white text-sm">
                  {timingData?.avgSeconds !== undefined ? `${timingData.avgSeconds}s/preg` : '--'}
                </span>
              </div>
              <div className="flex items-center justify-between text-blue-200">
                <span>Tiempo total:</span>
                <span>{formatTimingSeconds(timingData?.totalSeconds)}</span>
              </div>
              {timingData?.isNewRecord && (
                <div className="mt-1 pt-1.5 border-t border-white/20 flex items-center gap-1.5 text-amber-300 font-extrabold text-[11px] animate-pulse">
                  <span>🏆</span>
                  <span>¡Nuevo Récord Personal registrado!</span>
                </div>
              )}
            </div>
          </div>

          {/* Right Hero Card: Psychometric Breakdown */}
          <div className="w-full max-w-md bg-white text-ka-text-primary rounded-xl p-5 sm:p-6 shadow-2xl flex flex-col gap-3 min-w-0 shrink-0 max-h-[500px] overflow-y-auto">
            <div className="flex items-center justify-between text-xs font-bold uppercase tracking-wider text-ka-blue border-b border-slate-100 pb-2">
              <span className="flex items-center gap-1.5">
                <span>🎓</span>
                <span>Mastery Summary</span>
              </span>
              <span>{sessionType.toUpperCase()}</span>
            </div>

            {/* Single Session Tier Transition */}
            {timingData?.previousTier && timingData?.newTier && (
              <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 text-xs">
                <div className="text-slate-500 font-semibold mb-1">Estatus de Maestría:</div>
                <div className="flex items-center gap-2 flex-wrap">
                  <span
                    className="px-2 py-0.5 rounded font-bold text-white text-[11px]"
                    style={{ backgroundColor: TIER_COLORS[timingData.previousTier].bg }}
                  >
                    {timingData.previousTier}
                  </span>
                  <span className="text-slate-400 font-bold">➔</span>
                  <span
                    className="px-2 py-0.5 rounded font-bold text-white text-[11px]"
                    style={{ backgroundColor: TIER_COLORS[timingData.newTier].bg }}
                  >
                    {timingData.newTier}
                  </span>
                  {TIER_POINTS[timingData.newTier] > TIER_POINTS[timingData.previousTier] ? (
                    <span className="text-xs font-bold text-emerald-600">
                      ⬆️ Leveled Up
                    </span>
                  ) : TIER_POINTS[timingData.newTier] < TIER_POINTS[timingData.previousTier] ? (
                    <span className="text-xs font-bold text-rose-600">
                      🔻 Leveled Down
                    </span>
                  ) : (
                    <span className="text-xs font-bold text-slate-500">
                      ⏸️ No change
                    </span>
                  )}
                </div>
              </div>
            )}

            {/* Challenge Breakdown: Leveled Up */}
            {leveledUpList.length > 0 && (
              <div className="space-y-1.5">
                <h4 className="text-xs font-bold text-emerald-700 uppercase tracking-wide flex items-center gap-1">
                  <span>⬆️</span>
                  <span>Leveled Up ({leveledUpList.length})</span>
                </h4>
                <div className="space-y-1 max-h-28 overflow-y-auto pr-1">
                  {leveledUpList.map((skill) => (
                    <div
                      key={skill.competency_id}
                      className="p-1.5 bg-emerald-50 border border-emerald-200 rounded text-xs flex items-center justify-between"
                    >
                      <span className="truncate font-semibold text-emerald-950 max-w-[170px]">
                        <MathText text={skill.competency_name} inline />
                      </span>
                      <span className="font-bold text-emerald-700 text-[11px] shrink-0">
                        {skill.previous_tier} ➔ {skill.new_tier} (+{skill.delta_points})
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Challenge Breakdown: Leveled Down */}
            {leveledDownList.length > 0 && (
              <div className="space-y-1.5">
                <h4 className="text-xs font-bold text-rose-700 uppercase tracking-wide flex items-center gap-1">
                  <span>🔻</span>
                  <span>Leveled Down ({leveledDownList.length})</span>
                </h4>
                <div className="space-y-1.5 max-h-36 overflow-y-auto pr-1">
                  {leveledDownList.map((skill) => {
                    const targetComp = course.competencies.find(
                      (c) => c.id === skill.competency_id
                    );
                    return (
                      <div
                        key={skill.competency_id}
                        className="p-2 bg-rose-50 border border-rose-200 rounded text-xs flex flex-col gap-1"
                      >
                        <div className="flex items-center justify-between">
                          <span className="truncate font-bold text-rose-950 max-w-[170px]">
                            <MathText text={skill.competency_name} inline />
                          </span>
                          <span className="font-bold text-rose-700 text-[11px] shrink-0">
                            {skill.previous_tier} ➔ {skill.new_tier} ({skill.delta_points})
                          </span>
                        </div>
                        {targetComp && onRemediateCompetency && (
                          <button
                            type="button"
                            onClick={() => onRemediateCompetency(targetComp)}
                            className="self-end px-2 py-0.5 bg-rose-600 hover:bg-rose-700 text-white rounded text-[10px] font-bold shadow-sm transition-colors"
                          >
                            Practicar para recuperar ➔
                          </button>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Challenge Breakdown: Maintained / No Change */}
            {skillsMaintainedList.length > 0 && (
              <div className="space-y-1.5">
                <h4 className="text-xs font-bold text-slate-600 uppercase tracking-wide flex items-center gap-1">
                  <span>⏸️</span>
                  <span>No change ({skillsMaintainedList.length})</span>
                </h4>
                <div className="space-y-1 max-h-24 overflow-y-auto pr-1">
                  {skillsMaintainedList.map((skill) => (
                    <div
                      key={skill.competency_id}
                      className="p-1.5 bg-slate-50 border border-slate-200 rounded text-xs flex items-center justify-between"
                    >
                      <span className="truncate font-medium text-slate-700 max-w-[200px]">
                        <MathText text={skill.competency_name} inline />
                      </span>
                      <span className="font-semibold text-slate-500 text-[11px] shrink-0">
                        {skill.new_tier} (0 pts)
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Unidades / Áreas a reforzar consolidadas */}
            {consolidatedAreas.length > 0 && (
              <div className="space-y-1.5 pt-1 border-t border-slate-100">
                <h4 className="text-xs font-bold text-slate-700 flex items-center gap-1">
                  <span>⚠️</span>
                  <span>
                    {consolidatedAreas.length === 1
                      ? 'Unidad a reforzar:'
                      : `Unidades a reforzar (${consolidatedAreas.length}):`}
                  </span>
                </h4>
                <div className="space-y-1.5 max-h-36 overflow-y-auto pr-1">
                  {consolidatedAreas.map((area) => (
                    <div
                      key={area.competency_id}
                      className="p-2 bg-amber-50 border border-amber-200 rounded text-xs flex flex-col gap-1"
                    >
                      <div className="flex items-center justify-between gap-2">
                        <span className="font-bold text-amber-950 truncate" title={area.competency_name}>
                          <MathText text={area.competency_name} inline />
                        </span>
                        <span className="px-1.5 py-0.5 bg-amber-200/80 text-amber-900 rounded text-[10px] font-extrabold shrink-0">
                          {area.count} {area.count === 1 ? 'error' : 'errores'}
                        </span>
                      </div>
                      {area.targetComp && onRemediateCompetency && (
                        <button
                          type="button"
                          onClick={() => onRemediateCompetency(area.targetComp!)}
                          className="self-end px-2 py-0.5 bg-amber-600 hover:bg-amber-700 text-white rounded text-[10px] font-bold shadow-sm transition-colors"
                        >
                          Repasar esta unidad ➔
                        </button>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            <p className="text-[11px] text-slate-500 pt-1 border-t border-slate-100">
              {isPerfect
                ? '¡Dominio confirmado! Continúa al siguiente desafío.'
                : 'La práctica deliberada consolida la retención a largo plazo.'}
            </p>
          </div>
        </div>
      </div>

      {/* Bottom Footer Action Bar */}
      <footer className="h-16 sm:h-20 bg-white border-t border-ka-border-card px-4 sm:px-8 flex items-center justify-between gap-4 shrink-0">
        <button
          type="button"
          onClick={onTryAgain}
          className="text-sm font-semibold text-ka-blue hover:text-ka-blue-hover flex items-center gap-2 transition-colors shrink-0"
        >
          <span>🔄</span>
          <span>Try again</span>
        </button>

        <button
          type="button"
          role="button"
          onClick={onUpNext}
          className="px-4 sm:px-6 py-2.5 bg-ka-blue hover:bg-ka-blue-hover text-white text-sm font-bold rounded shadow-md transition-colors cursor-pointer inline-block text-center truncate max-w-[200px] sm:max-w-xs md:max-w-none shrink-0"
        >
          {nextCompetency ? (
            <span className="truncate block min-w-0">
              Up next: <MathText text={nextCompetency.name} inline />
            </span>
          ) : (
            'Back to course'
          )}
        </button>
      </footer>
    </div>
  );
};
