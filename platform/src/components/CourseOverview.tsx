import React, { useState } from 'react';
import { Course, CourseMasteryRecord, Competency } from '../types';
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
}

export const CourseOverview: React.FC<CourseOverviewProps> = ({
  course,
  mastery,
  onStartPractice,
  onStartQuiz,
  onStartUnitTest,
  onStartCourseChallenge,
}) => {
  const [showTooltip, setShowTooltip] = useState(false);

  const challengeCompleted = mastery.course_challenge?.completed;
  const challengePercent = challengeCompleted ? 100 : 0;

  const totalUnits = course.competencies.length;
  const completedUnits = course.competencies.filter((c) => {
    const cm = mastery.competencies[c.id];
    return cm && (cm.status === 'Mastered' || cm.status === 'Proficient' || cm.points >= 80);
  }).length;
  const inProgressUnits = course.competencies.filter((c) => {
    const cm = mastery.competencies[c.id];
    const isComp = cm && (cm.status === 'Mastered' || cm.status === 'Proficient' || cm.points >= 80);
    return !isComp && cm && (cm.status === 'Familiar' || cm.status === 'Attempted' || cm.points > 0);
  }).length;
  const notStartedUnits = totalUnits - completedUnits - inProgressUnits;

  return (
    <div className="flex-1 min-w-0 w-full max-w-5xl mx-auto px-4 sm:px-6 py-6 sm:py-8">
      {/* Breadcrumb */}
      <nav className="flex items-center flex-wrap gap-2 text-xs font-semibold text-ka-blue mb-3 min-w-0">
        <span className="text-base">🏠</span>
        <span className="text-slate-400">·</span>
        <span className="hover:underline cursor-pointer">Math</span>
        <span className="text-slate-400">·</span>
        <span className="text-slate-600 truncate block min-w-0 max-w-[200px] sm:max-w-md"><MathText text={course.title} inline /></span>
      </nav>

      {/* Course Title Header */}
      <h1 className="text-2xl sm:text-3xl font-extrabold text-ka-text-primary tracking-tight break-words [overflow-wrap:anywhere] [&_.katex]:max-w-full [&_.katex]:overflow-x-auto [&_.katex]:overflow-y-hidden [&_span.inline-block]:max-w-full">
        <MathText text={course.title} inline />
      </h1>
      <div className="text-sm text-ka-text-secondary mt-1 max-w-3xl break-words [overflow-wrap:anywhere] [&_.katex]:max-w-full [&_.katex]:overflow-x-auto [&_.katex]:overflow-y-hidden [&_span.inline-block]:max-w-full">
        <MathText text={course.description} />
      </div>

      {/* Course Mastery Percentage Line */}
      <div className="mt-4 flex items-center gap-2 relative">
        <span className="text-base font-bold text-ka-text-primary">
          Course mastery: {mastery.mastery_points}%
        </span>
        <button
          type="button"
          aria-label="How Course Mastery is calculated"
          onClick={() => setShowTooltip(!showTooltip)}
          onMouseEnter={() => setShowTooltip(true)}
          onMouseLeave={() => setShowTooltip(false)}
          className="text-slate-400 hover:text-slate-600 transition-colors text-sm"
          title="Click to view mastery point calculation rules"
        >
          ⓘ
        </button>

        {showTooltip && (
          <div className="absolute left-0 top-8 z-30 w-72 sm:w-80 max-w-[calc(100vw-2rem)] p-3 bg-white text-xs text-ka-text-secondary rounded-lg shadow-xl border border-ka-border-card break-words [overflow-wrap:anywhere]">
            <p className="font-bold text-ka-text-primary mb-1">How Course Mastery is calculated:</p>
            <p>
              Mastery points are earned by practicing skills, passing quizzes, and conquering unit
              tests. Mastered = 100 pts, Proficient = 80 pts, Familiar = 50 pts, Attempted = 25 pts.
            </p>
          </div>
        )}
      </div>

      {/* Competency Blocks / Units Completion Status Overview */}
      <div
        data-testid="completion-tracker-summary"
        className="mt-4 p-4 bg-slate-50 rounded-xl border border-ka-border-subtle flex flex-col sm:flex-row sm:items-center justify-between gap-4"
      >
        <div className="min-w-0">
          <div className="text-xs font-bold text-slate-500 uppercase tracking-wider">
            Unit Completion Status
          </div>
          <div className="text-base font-extrabold text-ka-text-primary mt-0.5">
            {completedUnits} of {totalUnits} Units Completed ({totalUnits > 0 ? Math.round((completedUnits / totalUnits) * 100) : 0}%)
          </div>
          <div className="flex flex-wrap items-center gap-2 mt-2">
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
        </div>

        {/* Progress Bar */}
        <div className="w-full sm:w-48 flex flex-col gap-1.5 shrink-0">
          <div className="flex justify-between text-[11px] font-semibold text-slate-500">
            <span>Overall completion</span>
            <span>{totalUnits > 0 ? Math.round((completedUnits / totalUnits) * 100) : 0}%</span>
          </div>
          <div className="w-full bg-slate-200 rounded-full h-2.5 overflow-hidden">
            <div
              className="bg-emerald-600 h-2.5 rounded-full transition-all duration-300"
              style={{
                width: `${totalUnits > 0 ? (completedUnits / totalUnits) * 100 : 0}%`,
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
