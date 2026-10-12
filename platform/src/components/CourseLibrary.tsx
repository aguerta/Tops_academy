import React from 'react';
import { CourseSummary } from '../types';
import { getCourseMasteryRecord, isCourseCompleted } from '../utils/masteryStorage';
import { MathText } from './MathText';

interface CourseLibraryProps {
  courses: CourseSummary[];
  loading: boolean;
  onSelectCourse: (course: CourseSummary) => void;
}

export const CourseLibrary: React.FC<CourseLibraryProps> = ({
  courses,
  loading,
  onSelectCourse,
}) => {
  return (
    <div className="max-w-6xl mx-auto px-6 py-10">
      {/* Page Header */}
      <div className="mb-8">
        <div className="flex items-center gap-2 text-ka-blue font-bold text-sm mb-2">
          <span>📚</span>
          <span>Top's Academy Platform</span>
        </div>
        <h1 className="text-3xl font-extrabold text-ka-text-primary tracking-tight">
          Course Library
        </h1>
        <p className="text-sm text-ka-text-secondary mt-1 max-w-2xl">
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
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {courses.map((c) => {
            if (c.status === 'error') {
              // Fault-Tolerant Error Isolation Card (AC-02)
              return (
                <div
                  key={c.filename || c.id}
                  data-testid="course-error-card"
                  className="course-error p-6 bg-red-50/50 rounded-xl border-2 border-red-300 shadow-sm flex flex-col justify-between"
                >
                  <div>
                    <div className="flex items-center justify-between gap-2 mb-2">
                      <span className="px-2 py-0.5 bg-red-100 text-red-800 text-[11px] font-bold rounded uppercase tracking-wider">
                        Invalid / Corrupted
                      </span>
                      <span className="text-xs text-red-600 font-mono truncate max-w-[140px]">
                        {c.filename}
                      </span>
                    </div>

                    <h3 className="text-lg font-bold text-red-900 leading-snug">
                      {c.title || c.filename}
                    </h3>

                    <p className="text-xs text-red-700 mt-2 bg-white/70 p-2.5 rounded border border-red-200 font-mono break-words leading-relaxed">
                      <strong>Error:</strong> {c.error_message || 'Schema or LaTeX escape validation failed.'}
                    </p>
                  </div>

                  <div className="mt-4 pt-3 border-t border-red-200 text-[11px] text-red-600 font-medium">
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

            return (
              <div
                key={c.id}
                data-testid="course-card"
                onClick={() => onSelectCourse(c)}
                className={`cursor-pointer p-6 bg-white rounded-xl border shadow-sm hover:shadow-md transition-all flex flex-col justify-between ${
                  isCompleted
                    ? 'border-emerald-300 ring-2 ring-emerald-100 hover:border-emerald-500'
                    : 'border-ka-border-card hover:border-ka-blue'
                }`}
              >
                <div>
                  <div className="flex items-center justify-between gap-2 mb-3">
                    <div className="flex items-center gap-1.5 flex-wrap">
                      <span className="px-2 py-0.5 bg-ka-blue-light text-ka-blue text-[11px] font-bold rounded">
                        {c.total_competencies || 0} Units
                      </span>
                      {isCompleted ? (
                        <span
                          data-testid="course-completed-badge"
                          className="px-2.5 py-0.5 bg-emerald-100 text-emerald-800 text-[11px] font-bold rounded-full border border-emerald-300 flex items-center gap-1 shadow-sm"
                        >
                          <span>✓</span>
                          <span>Completed</span>
                        </span>
                      ) : masteryPercent > 0 ? (
                        <span
                          data-testid="course-progress-badge"
                          className="px-2 py-0.5 bg-amber-50 text-amber-700 text-[11px] font-bold rounded-full border border-amber-200"
                        >
                          {masteryPercent}% Mastery
                        </span>
                      ) : null}
                    </div>
                    <span className="text-xs text-slate-400 font-medium">
                      {c.total_questions || 0} Questions
                    </span>
                  </div>

                  <h3 className="text-xl font-bold text-ka-text-primary leading-snug hover:text-ka-blue transition-colors">
                    <MathText text={c.title} inline />
                  </h3>

                  <div className="text-xs text-ka-text-secondary mt-2 line-clamp-3 leading-relaxed">
                    <MathText text={c.description || 'Interactive practice course.'} />
                  </div>
                </div>

                <div className="mt-6 pt-4 border-t border-ka-border-subtle flex items-center justify-between">
                  <button
                    onClick={() => onSelectCourse(c)}
                    className={`w-full py-2.5 px-4 text-white text-sm font-bold rounded shadow-sm transition-colors text-center flex items-center justify-center gap-1.5 ${
                      isCompleted
                        ? 'bg-emerald-600 hover:bg-emerald-700'
                        : 'bg-ka-blue hover:bg-ka-blue-hover'
                    }`}
                  >
                    {isCompleted && <span>✓</span>}
                    <span><MathText text={c.title} inline /></span>
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
