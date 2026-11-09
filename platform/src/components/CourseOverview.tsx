import React, { useState, useLayoutEffect, useEffect, useRef } from 'react';
import { Course, CourseMasteryRecord, Competency } from '../types';
import { calculateCourseProgress, isUnitCompleted, isUnitStarted } from '../utils/masteryStorage';
import { MasteryLegend } from './MasteryLegend';
import { MasteryGrid } from './MasteryGrid';
import { MathText } from './MathText';

interface CourseOverviewProps {
  course: Course;
  mastery: CourseMasteryRecord;
  onStartPractice: (competency: Competency) => void;
  onStartQuiz: (competency: Competency) => void;
  onStartUnitTest: (competency: Competency) => void;
  onStartCourseChallenge: () => void;
  focusCompetencyId?: string | null;
}

export const CourseOverview: React.FC<CourseOverviewProps> = ({
  course,
  mastery,
  onStartPractice,
  onStartQuiz,
  onStartUnitTest,
  onStartCourseChallenge,
  focusCompetencyId,
}) => {
  const [showTooltip, setShowTooltip] = useState(false);
  const [showStickyBar, setShowStickyBar] = useState(false);
  const summaryRef = useRef<HTMLDivElement>(null);
  const rootRef = useRef<HTMLDivElement>(null);
  const [barBox, setBarBox] = useState<{ left: number; width: number }>({ left: 0, width: 0 });

  // Keep the fixed bar aligned with the overview column (sidebar / centered layout)
  useEffect(() => {
    const update = () => {
      const r = rootRef.current?.getBoundingClientRect();
      if (r) setBarBox({ left: r.left, width: r.width });
    };
    update();
    window.addEventListener('resize', update);
    window.addEventListener('scroll', update, true);
    return () => {
      window.removeEventListener('resize', update);
      window.removeEventListener('scroll', update, true);
    };
  }, []);

  // Show the compact sticky progress bar once the full summary card scrolls out above the viewport
  useEffect(() => {
    const el = summaryRef.current;
    if (!el || typeof IntersectionObserver === 'undefined') return;
    const obs = new IntersectionObserver(([entry]) => {
      setShowStickyBar(!entry.isIntersecting && entry.boundingClientRect.top < 0);
    });
    obs.observe(el);
    return () => obs.disconnect();
  }, []);

  // Focus rules: furthest completed unit (course order); else furthest unit with any
  // progress (Attempted+); else no progress at all -> show the top of the course.
  useLayoutEffect(() => {
    let completedId: string | null = null;
    let startedId: string | null = null;
    for (const c of course.competencies) {
      const m = mastery.competencies?.[c.id];
      if (isUnitCompleted(m)) completedId = c.id;
      if (isUnitStarted(m)) startedId = c.id;
    }
    const targetId =
      (focusCompetencyId &&
      course.competencies.some((c) => c.id === focusCompetencyId)
        ? focusCompetencyId
        : null) ??
      completedId ??
      startedId;
    const el = targetId
      ? document.querySelector<HTMLElement>(`[data-testid="competency-block-${targetId}"]`)
      : null;
    if (el) {
      el.scrollIntoView({ block: 'center', behavior: 'auto' });
    } else {
      window.scrollTo(0, 0);
      document.querySelector<HTMLElement>('main')?.scrollTo?.(0, 0);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [course.course_id, focusCompetencyId]);

  const totalUnits = course.competencies.length;
  const progressDetails = calculateCourseProgress(mastery, totalUnits);
  const { percentage, status, completedUnits, inProgressUnits, notStartedUnits } = progressDetails;
  const isCompletedStrong = status === 'completed';
  const isCompletedLight = status === 'unit_tests_mastered';
  const isInProgress = status === 'in_progress';

  const challengeCompleted = mastery.course_challenge?.completed;
  const challengePercent = challengeCompleted ? 100 : (mastery.course_challenge?.percentage || 0);
  const challengeState: 'mastered' | 'in_progress' | 'not_attempted' = challengeCompleted
    ? 'mastered'
    : mastery.course_challenge && (mastery.course_challenge.total_questions ?? 0) > 0
    ? 'in_progress'
    : 'not_attempted';

  return (
    <div ref={rootRef} className="flex-1 min-w-0 w-full max-w-5xl mx-auto px-4 sm:px-6 pt-6 sm:pt-8 pb-20 sm:pb-[88px]">
      {/* Compact progress bar fixed to the top of the viewport (aligned with this column) */}
      <div
        className="fixed bottom-0 z-40"
        style={{ left: barBox.left, width: barBox.width }}
      >
        {showStickyBar && (
          <div
            data-testid="sticky-completion-bar"
            className="pl-4 pr-16 sm:pl-6 py-3.5 sm:py-4 bg-white/95 backdrop-blur border-t border-ka-border-subtle shadow-[0_-2px_8px_rgba(0,0,0,0.06)] flex items-center gap-3 min-w-0"
          >
            <div className="min-w-0 flex-1">
              <div className="flex items-baseline justify-between gap-2 text-xs sm:text-sm font-bold text-slate-500 uppercase tracking-wider">
                <span className="truncate">Course Mastery Status</span>
                <span className="shrink-0 normal-case text-sm sm:text-base font-extrabold text-slate-700">
                  {percentage}%
                </span>
              </div>
              <div className="w-full bg-slate-200 rounded-full h-3 overflow-hidden mt-2">
                <div
                  className={`h-3 rounded-full ${
                    isCompletedStrong
                      ? 'bg-emerald-950'
                      : isCompletedLight
                      ? 'bg-emerald-500'
                      : isInProgress
                      ? 'bg-emerald-400'
                      : 'bg-slate-300'
                  }`}
                  style={{ width: `${percentage}%` }}
                />
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Breadcrumb */}
      <nav className="flex items-center flex-wrap gap-2 text-xs font-semibold text-ka-blue mb-3 min-w-0">
        <span className="text-base">🏠</span>
        <span className="text-slate-400">·</span>
        <span className="hover:underline cursor-pointer">Math</span>
        <span className="text-slate-400">·</span>
        <span className="text-slate-600 truncate block min-w-0 max-w-[200px] sm:max-w-md"><MathText text={course.title} inline /></span>
      </nav>

      {/* Course Title Header */}
      <h1 className="text-2xl sm:text-3xl font-extrabold text-ka-text-primary tracking-tight break-words [overflow-wrap:anywhere]">
        <MathText text={course.title} inline />
      </h1>
      <div className="text-sm text-ka-text-secondary mt-1 max-w-3xl break-words [overflow-wrap:anywhere]">
        <MathText text={course.description} />
      </div>

      {/* Up Next for You — Persistent Pedagogical Recommender (Milestone 14) */}
      {(() => {
        if (!course.competencies || course.competencies.length === 0) return null;

        // Priority 1: Remediation (needs_review / lagunas detectadas)
        const needsReviewComp = course.competencies.find(
          (c) => mastery.competencies?.[c.id]?.needs_review
        );
        if (needsReviewComp) {
          return (
            <div
              data-testid="up-next-banner"
              className="mt-4 p-4 bg-rose-50 border border-rose-200 rounded-xl flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-sm"
            >
              <div className="flex items-center gap-3 min-w-0">
                <span className="text-2xl shrink-0">🩹</span>
                <div className="min-w-0">
                  <div className="text-xs font-bold uppercase tracking-wide text-rose-800">
                    Up Next for You • Reparar Maestría
                  </div>
                  <div className="text-sm font-bold text-rose-950 truncate">
                    <MathText text={needsReviewComp.name} inline />
                  </div>
                  <p className="text-xs text-rose-700 mt-0.5">
                    Se detectaron errores en esta competencia. Repásala para restaurar tu nivel antes de continuar.
                  </p>
                </div>
              </div>
              <button
                type="button"
                onClick={() => onStartPractice(needsReviewComp)}
                className="px-4 py-2 bg-rose-600 hover:bg-rose-700 text-white text-xs sm:text-sm font-bold rounded shadow-sm transition-colors whitespace-nowrap self-start sm:self-auto shrink-0"
              >
                Repasar ahora ➔
              </button>
            </div>
          );
        }

        // Priority 2: Siguiente unidad no iniciada (Menor orden ordinal no empezado)
        const nextNotStartedComp = course.competencies.find((c) => {
          const m = mastery.competencies?.[c.id];
          return !m || m.status === 'Not started' || !isUnitStarted(m);
        });
        if (nextNotStartedComp) {
          return (
            <div
              data-testid="up-next-banner"
              className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-xl flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-sm"
            >
              <div className="flex items-center gap-3 min-w-0">
                <span className="text-2xl shrink-0">🚀</span>
                <div className="min-w-0">
                  <div className="text-xs font-bold uppercase tracking-wide text-ka-blue">
                    Up Next for You • Siguiente Unidad
                  </div>
                  <div className="text-sm font-bold text-blue-950 truncate">
                    <MathText text={nextNotStartedComp.name} inline />
                  </div>
                  <p className="text-xs text-blue-700 mt-0.5">
                    Comienza la práctica de esta nueva unidad para ganar tus primeros puntos de maestría.
                  </p>
                </div>
              </div>
              <button
                type="button"
                onClick={() => onStartPractice(nextNotStartedComp)}
                className="px-4 py-2 bg-ka-blue hover:bg-ka-blue-hover text-white text-xs sm:text-sm font-bold rounded shadow-sm transition-colors whitespace-nowrap self-start sm:self-auto shrink-0"
              >
                Comenzar práctica ➔
              </button>
            </div>
          );
        }

        // Priority 3: Rendir Unit Test (Todas las unidades fueron iniciadas, pero faltan Unit Tests al 100%)
        const nextIncompleteTestComp = course.competencies.find((c) => {
          const m = mastery.competencies?.[c.id];
          return !isUnitCompleted(m);
        });
        if (nextIncompleteTestComp) {
          return (
            <div
              data-testid="up-next-banner"
              className="mt-4 p-4 bg-amber-50 border border-amber-200 rounded-xl flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-sm"
            >
              <div className="flex items-center gap-3 min-w-0">
                <span className="text-2xl shrink-0">📝</span>
                <div className="min-w-0">
                  <div className="text-xs font-bold uppercase tracking-wide text-amber-800">
                    Up Next for You • Unit Test Pendiente
                  </div>
                  <div className="text-sm font-bold text-amber-950 truncate">
                    <MathText text={nextIncompleteTestComp.name} inline />
                  </div>
                  <p className="text-xs text-amber-700 mt-0.5">
                    Lleva esta unidad al 100% rindiendo su Unit Test para consolidar tu avance.
                  </p>
                </div>
              </div>
              <button
                type="button"
                onClick={() => onStartUnitTest(nextIncompleteTestComp)}
                className="px-4 py-2 bg-amber-600 hover:bg-amber-700 text-white text-xs sm:text-sm font-bold rounded shadow-sm transition-colors whitespace-nowrap self-start sm:self-auto shrink-0"
              >
                Rendir Unit Test ➔
              </button>
            </div>
          );
        }

        // Priority 4: Course Challenge (Todos los Unit Tests completados al 100%, pero Challenge pendiente)
        const isChallengeCompleted = mastery.course_challenge?.completed === true;
        if (!isChallengeCompleted) {
          return (
            <div
              data-testid="up-next-banner"
              className="mt-4 p-4 bg-purple-50 border border-purple-200 rounded-xl flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-sm"
            >
              <div className="flex items-center gap-3 min-w-0">
                <span className="text-2xl shrink-0">🏆</span>
                <div className="min-w-0">
                  <div className="text-xs font-bold uppercase tracking-wide text-purple-800">
                    Up Next for You • Desafío del Curso
                  </div>
                  <div className="text-sm font-bold text-purple-950 truncate">
                    Course Challenge: <MathText text={course.title} inline />
                  </div>
                  <p className="text-xs text-purple-700 mt-0.5">
                    ¡Todos los Unit Tests están dominados! Rinde el Course Challenge para completar el curso al 100%.
                  </p>
                </div>
              </div>
              <button
                type="button"
                onClick={onStartCourseChallenge}
                className="px-4 py-2 bg-purple-700 hover:bg-purple-800 text-white text-xs sm:text-sm font-bold rounded shadow-sm transition-colors whitespace-nowrap self-start sm:self-auto shrink-0"
              >
                Rendir Course Challenge ➔
              </button>
            </div>
          );
        }

        // Priority 5: Maestría Total 100% (Curso completado)
        return (
          <div
            data-testid="up-next-banner"
            className="mt-4 p-4 bg-emerald-50 border border-emerald-200 rounded-xl flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-sm"
          >
            <div className="flex items-center gap-3 min-w-0">
              <span className="text-2xl shrink-0">🎓</span>
              <div className="min-w-0">
                <div className="text-xs font-bold uppercase tracking-wide text-emerald-800">
                  Up Next for You • ¡Maestría Total Conquistada!
                </div>
                <div className="text-sm font-bold text-emerald-950 truncate">
                  ¡Felicitaciones! Has logrado completar este curso al 100%
                </div>
                <p className="text-xs text-emerald-700 mt-0.5">
                  Has dominado todos los conceptos y exámenes. Mantén tu fluidez dándole otra repasada cuando quieras.
                </p>
              </div>
            </div>
            <button
              type="button"
              onClick={onStartCourseChallenge}
              className="px-4 py-2 bg-emerald-700 hover:bg-emerald-800 text-white text-xs sm:text-sm font-bold rounded shadow-sm transition-colors whitespace-nowrap self-start sm:self-auto shrink-0"
            >
              Darle otra repasada ➔
            </button>
          </div>
        );
      })()}

      {/* Competency Blocks / Units Completion Status Overview */}
      <div
        ref={summaryRef}
        data-testid="completion-tracker-summary"
        className="mt-4 p-4 bg-slate-50 rounded-xl border border-ka-border-subtle flex flex-col sm:flex-row sm:items-center justify-between gap-4"
      >
        <div className="min-w-0">
          <div className="relative flex items-center gap-1.5 text-xs font-extrabold text-black uppercase tracking-wider">
            <span>Course Mastery Status</span>
            <button
              type="button"
              aria-label="How Course Mastery is calculated"
              onClick={() => setShowTooltip(!showTooltip)}
              onMouseEnter={() => setShowTooltip(true)}
              onMouseLeave={() => setShowTooltip(false)}
              className="text-slate-400 hover:text-slate-600 transition-colors text-sm normal-case"
              title="Click to view mastery point calculation rules"
            >
              ⓘ
            </button>
            {showTooltip && (
              <div className="absolute left-0 top-7 z-30 w-72 sm:w-80 max-w-[calc(100vw-2rem)] p-3 bg-white text-xs normal-case font-normal text-ka-text-secondary rounded-lg shadow-xl border border-ka-border-card break-words [overflow-wrap:anywhere]">
                <p className="font-bold text-ka-text-primary mb-1">How Course Mastery is calculated:</p>
                <p>
                  Mastery points are earned by practicing skills, passing quizzes, and conquering unit
                  tests. Mastered = 100 pts, Proficient = 80 pts, Familiar = 50 pts, Attempted = 25 pts.
                </p>
              </div>
            )}
          </div>
          <div className="text-base font-extrabold text-ka-text-primary mt-0.5">
            {percentage}%
          </div>
          <div className="flex flex-wrap items-center gap-x-4 gap-y-2 mt-2">
            {/* Units group */}
            <div className="flex flex-wrap items-center gap-1.5">
              <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider mr-0.5">Units</span>
              <span
                data-testid="summary-completed-count"
                className="inline-flex items-center gap-1 px-2.5 py-0.5 bg-emerald-100 text-emerald-800 text-xs font-bold rounded-full border border-emerald-200"
              >
                <span>✓</span>
                <span>{completedUnits} Completed</span>
              </span>
              <span
                data-testid="summary-in-progress-count"
                className="inline-flex items-center gap-1 px-2.5 py-0.5 bg-amber-100 text-amber-800 text-xs font-bold rounded-full border border-amber-200"
              >
                <span>⏳</span>
                <span>{inProgressUnits} In Progress</span>
              </span>
              <span
                data-testid="summary-not-started-count"
                className="inline-flex items-center gap-1 px-2.5 py-0.5 bg-slate-200 text-slate-700 text-xs font-bold rounded-full border border-slate-300"
              >
                <span>○</span>
                <span>{notStartedUnits} Not Started</span>
              </span>
            </div>
            {/* Course Challenge group */}
            <div className="flex items-center gap-1.5">
              <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider mr-0.5">Challenge</span>
              <span
                data-testid="summary-course-challenge-status"
                className={`inline-flex items-center px-2.5 py-0.5 text-xs font-bold rounded-full border ${
                  challengeState === 'mastered'
                    ? 'bg-purple-100 text-purple-800 border-purple-300'
                    : challengeState === 'in_progress'
                    ? 'bg-amber-100 text-amber-800 border-amber-200'
                    : 'bg-slate-200 text-slate-700 border-slate-300'
                }`}
              >
                {challengeState === 'mastered'
                  ? 'Mastered'
                  : challengeState === 'in_progress'
                  ? 'In Progress'
                  : 'Not Attempted'}
              </span>
            </div>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="w-full sm:w-48 flex flex-col gap-1.5 shrink-0">
          <div className="flex justify-between text-[11px] font-semibold text-slate-500">
            <span>Course mastery</span>
            <span>{percentage}%</span>
          </div>
          <div className="w-full bg-slate-200 rounded-full h-2.5 overflow-hidden">
            <div
              data-testid="course-progress-bar-overview"
              className={`h-2.5 rounded-full transition-all duration-300 ${
                isCompletedStrong
                  ? 'bg-emerald-950'
                  : isCompletedLight
                  ? 'bg-emerald-500'
                  : isInProgress
                  ? 'bg-emerald-400'
                  : 'bg-slate-300'
              }`}
              style={{
                width: `${percentage}%`,
              }}
            />
          </div>
        </div>
      </div>

      {/* Mastery Legend */}
      <div className="mt-4">
        <MasteryLegend />
      </div>

      {/* Main Units / Competencies Matrix */}
      <div className="mt-6">
        <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
          <div className="flex items-center gap-2 sm:gap-3 flex-wrap">
            <h2 className="text-xl font-bold text-ka-text-primary">Units</h2>
            <span className="px-2.5 py-0.5 text-xs font-bold rounded-full bg-slate-100 text-slate-700 border border-slate-200">
              {completedUnits} / {totalUnits} Completed
            </span>
          </div>
          <span className="text-xs text-ka-text-secondary">
            {totalUnits} units total
          </span>
        </div>
        <MasteryGrid
          course={course}
          mastery={mastery}
          onStartPractice={onStartPractice}
          onStartQuiz={onStartQuiz}
          onStartUnitTest={onStartUnitTest}
        />
      </div>

      {/* Course Challenge Summary Card */}
      <div
        data-testid="course-challenge-card"
        className="mt-8 p-4 sm:p-6 bg-white rounded-lg border-2 border-ka-border-card hover:border-ka-blue transition-colors shadow-sm min-w-0"
      >
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 min-w-0">
          <div className="flex items-start gap-3 min-w-0">
            <span className="text-3xl leading-none shrink-0">📖</span>
            <div className="min-w-0">
              <div className="flex items-center gap-2 flex-wrap">
                <h3 className="text-base font-bold text-ka-text-primary uppercase tracking-wide">
                  COURSE CHALLENGE: {challengePercent}%
                </h3>
                {challengeCompleted && (
                  <span className="px-2 py-0.5 bg-emerald-100 text-emerald-800 text-xs font-bold rounded shrink-0">
                    ✓ Completed
                  </span>
                )}
                {mastery.course_challenge?.timing?.best_avg_seconds_per_question !== undefined && (
                  <span className="px-2 py-0.5 bg-slate-100 text-slate-700 text-xs font-semibold rounded border border-slate-200 shrink-0">
                    ⏱️ Récord: {mastery.course_challenge.timing.best_avg_seconds_per_question}s/preg
                  </span>
                )}
              </div>
              <p className="text-sm text-ka-text-secondary mt-1 break-words">
                Test your knowledge of the skills in this course.
              </p>
            </div>
          </div>

          <button
            type="button"
            aria-label={challengeCompleted ? 'Take Course challenge again' : 'Take Course challenge'}
            onClick={onStartCourseChallenge}
            className="px-5 py-2.5 bg-ka-blue hover:bg-ka-blue-hover text-white font-semibold text-sm rounded shadow-sm transition-colors whitespace-nowrap self-start sm:self-auto shrink-0"
          >
            {challengeCompleted ? 'Take Course challenge again' : 'Take Course challenge'}
          </button>
        </div>
      </div>
    </div>
  );
};
