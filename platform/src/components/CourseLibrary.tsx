import React from 'react';
import { CourseSummary } from '../types';
import { getCourseMasteryRecord, isCourseCompleted } from '../utils/masteryStorage';
import { MathText } from './MathText';

interface CourseLibraryProps {
  courses: CourseSummary[];
  loading: boolean;
  onSelectCourse: (course: CourseSummary) => void;
  onPrefetch?: (id: string) => void;
  loadingCourseId?: string | null;
}

export const CourseLibrary: React.FC<CourseLibraryProps> = ({
  courses,
  loading,
  onSelectCourse,
  onPrefetch,
  loadingCourseId,
}) => {
  return (
    <div className="w-full max-w-6xl mx-auto px-4 sm:px-6 py-6 sm:py-10 overflow-x-hidden">
      {/* Page Header */}
      <div className="mb-8">
        <div className="flex items-center gap-2 text-ka-blue font-bold text-sm mb-2">
          <span>📚</span>
          <span>Top's Academy Platform</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-ka-text-primary tracking-tight break-words [overflow-wrap:anywhere]">
          Course Library
        </h1>
        <p className="text-sm text-ka-text-secondary mt-1 max-w-2xl break-words">
          Explore and practice competency-based courses loaded directly from your exercise bank.
        </p>
      </div>

      {loading ? (
        <div className="py-12 text-center text-slate-400">
          <div className="w-8 h-8 border-4 border-ka-blue border-t-transparent rounded-full animate-spin mx-auto mb-3" />
          <p className="text-sm font-medium">Scanning courses directory...</p>
        </div>
      ) : courses.length === 0 ? (
        <div className="py-12 text-center bg-white rounded-xl border border-dashed border-slate-300 p-8">
          <p className="text-base font-bold text-ka-text-primary">No courses found</p>
          <p className="text-xs text-ka-text-secondary mt-1">
            Place valid course JSON files in the <code className="bg-slate-100 px-1 rounded">courses/</code> directory to start practicing.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 min-[560px]:grid-cols-2 min-[1000px]:grid-cols-3 gap-4 sm:gap-6 min-w-0">
          {courses.map((c) => {
            if (c.status === 'error') {
              // Fault-Tolerant Error Isolation Card (AC-02)
              return (
                <div
                  key={c.filename || c.id}
                  data-testid="course-error-card"
                  className="course-error min-w-0 p-4 bg-red-50/50 rounded-xl border-2 border-red-300 shadow-sm flex flex-col justify-between"
                >
                  <div>
                    <div className="flex items-center justify-between gap-2 mb-2">
                      <span className="px-2 py-0.5 bg-red-100 text-red-800 text-[11px] font-bold rounded uppercase tracking-wider shrink-0">
                        Invalid / Corrupted
                      </span>
                      <span className="text-xs text-red-600 font-mono truncate max-w-[140px] shrink-0">
                        {c.filename}
                      </span>
                    </div>

                    <h3 className="text-sm sm:text-base font-bold text-red-900 leading-tight break-words [overflow-wrap:anywhere] line-clamp-2">
                      {c.title || c.filename}
                    </h3>

                    <p className="text-xs text-red-700 mt-1 bg-white/70 p-2 rounded border border-red-200 font-mono break-all leading-snug line-clamp-2">
                      <strong>Error:</strong> {c.error_message || 'Schema or LaTeX escape validation failed.'}
                    </p>
                  </div>

                  <div className="mt-2.5 pt-2 border-t border-red-200 text-[11px] text-red-600 font-medium">
                    This course cannot be loaded. Other valid courses remain fully functional.
                  </div>
                </div>
              );
            }

            // Valid Course Card
            const courseId = c.id || c.data?.course_id || '';
            const record = getCourseMasteryRecord(courseId);
            const isCompleted = isCourseCompleted(courseId, c.total_competencies);
            const masteryPercent = record?.mastery_points || 0;
            const isLoadingThis = loadingCourseId === c.id;

            return (
              <div
                key={c.id}
                data-testid="course-card"
                onClick={() => onSelectCourse(c)}
                onPointerEnter={() => onPrefetch?.(c.id)}
                onFocus={() => onPrefetch?.(c.id)}
                onTouchStart={() => onPrefetch?.(c.id)}
                className={`cursor-pointer min-w-0 p-4 bg-white rounded-xl border shadow-sm hover:shadow-md transition-all flex flex-col justify-between ${
                  isCompleted
                    ? 'border-emerald-300 ring-2 ring-emerald-100 hover:border-emerald-500'
                    : 'border-ka-border-card hover:border-ka-blue'
                }`}
              >
                <div className="min-w-0">
                  <div className="flex items-center justify-between gap-1.5 mb-1.5">
                    <div className="flex items-center gap-1.5 flex-wrap min-w-0">
                      <span className="px-2 py-0.5 bg-ka-blue-light text-ka-blue text-[11px] font-bold rounded shrink-0">
                        {c.total_competencies || 0} Units
                      </span>
                      {isCompleted ? (
                        <span
                          data-testid="course-completed-badge"
                          className="px-2.5 py-0.5 bg-emerald-100 text-emerald-800 text-[11px] font-bold rounded-full border border-emerald-300 flex items-center gap-1 shadow-sm shrink-0"
                        >
                          <span>✓</span>
                          <span>Completed</span>
                        </span>
                      ) : masteryPercent > 0 ? (
                        <span
                          data-testid="course-progress-badge"
                          className="px-2 py-0.5 bg-amber-50 text-amber-700 text-[11px] font-bold rounded-full border border-amber-200 shrink-0"
                        >
                          {masteryPercent}% Mastery
                        </span>
                      ) : null}
                    </div>
                    <span className="text-xs text-slate-400 font-medium shrink-0">
                      {c.total_questions || 0} Questions
                    </span>
                  </div>

                  <h3 className="text-xs sm:text-sm font-bold text-ka-text-primary leading-tight hover:text-ka-blue transition-colors line-clamp-1 break-words [overflow-wrap:anywhere]">
                    <MathText text={c.title} inline />
                  </h3>

                  <div className="text-xs text-ka-text-secondary mt-0.5 line-clamp-2 leading-tight break-words [overflow-wrap:anywhere]">
                    <MathText text={c.description || 'Interactive practice course.'} />
                  </div>
                </div>

                <div className="mt-2 pt-1.5 border-t border-ka-border-subtle flex items-center justify-between min-w-0">
                  <button
                    type="button"
                    disabled={isLoadingThis}
                    onClick={(e) => {
                      e.stopPropagation();
                      onSelectCourse(c);
                    }}
                    className={`w-full py-2 px-3 text-white text-xs sm:text-sm font-bold rounded shadow-sm transition-colors text-center flex items-center justify-center gap-1.5 min-w-0 ${
                      isLoadingThis
                        ? 'bg-ka-blue/70 cursor-wait'
                        : isCompleted
                        ? 'bg-emerald-600 hover:bg-emerald-700'
                        : 'bg-ka-blue hover:bg-ka-blue-hover'
                    }`}
                  >
                    {isLoadingThis ? (
                      <>
                        <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin shrink-0" />
                        <span className="truncate block min-w-0">Cargando...</span>
                      </>
                    ) : (
                      <>
                        {isCompleted && <span className="shrink-0">✓</span>}
                        <span className="truncate block min-w-0"><MathText text={c.title} inline /></span>
                      </>
                    )}
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
