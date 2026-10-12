import React from 'react';
import { Course } from '../types';
import { MathText } from './MathText';

interface SidebarProps {
  course: Course;
  selectedUnitIndex: number | null;
  isCourseChallengeActive: boolean;
  onSelectUnit: (index: number) => void;
  onSelectCourseChallenge: () => void;
  onBackToLibrary: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  course,
  selectedUnitIndex,
  isCourseChallengeActive,
  onSelectUnit,
  onSelectCourseChallenge,
  onBackToLibrary,
}) => {
  const units = course.competencies;

  return (
    <aside
      data-testid="sidebar"
      className="w-64 flex-shrink-0 bg-white border-r border-ka-border-subtle min-h-screen py-6 flex flex-col"
    >
      {/* Back to courses */}
      <button
        onClick={onBackToLibrary}
        className="px-6 mb-4 text-xs font-semibold text-ka-blue hover:text-ka-blue-hover flex items-center gap-1.5 transition-colors"
      >
        <span>←</span>
        <span>Course Library</span>
      </button>

      {/* Course Header */}
      <div className="px-6 pb-5 border-b border-ka-border-subtle">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-cyan-500 text-white flex items-center justify-center font-bold text-lg shadow-sm">
            {course.title.charAt(0)}
          </div>
          <div className="flex-1 min-w-0">
            <h2 className="text-sm font-bold text-ka-text-primary leading-tight truncate">
              <MathText text={course.title} inline />
            </h2>
            <div className="mt-1">
              <span className="inline-block px-2 py-0.5 bg-slate-100 text-slate-700 text-[11px] font-bold rounded">
                {units.length} UNITS
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Units List */}
      <nav className="flex-1 overflow-y-auto py-2">
        {units.map((unit, idx) => {
          const isActive = selectedUnitIndex === idx && !isCourseChallengeActive;
          return (
            <button
              key={unit.id}
              onClick={() => onSelectUnit(idx)}
              className={`w-full text-left px-6 py-3 border-b border-ka-border-subtle transition-colors flex flex-col justify-center ${
                isActive
                  ? 'bg-ka-blue-light border-l-4 border-l-ka-blue text-ka-blue'
                  : 'hover:bg-slate-50 text-ka-text-primary'
              }`}
            >
              <span className="text-[11px] font-bold tracking-wider text-slate-500 uppercase">
                UNIT {idx + 1}
              </span>
              <span
                className={`text-sm font-medium mt-0.5 truncate ${
                  isActive ? 'text-ka-blue font-semibold' : 'text-ka-text-primary'
                }`}
              >
                <MathText text={unit.name} inline />
              </span>
            </button>
          );
        })}

        {/* Course Challenge Item */}
        <button
          onClick={onSelectCourseChallenge}
          className={`w-full text-left px-6 py-3 mt-2 border-t border-b border-ka-border-subtle transition-colors flex items-start gap-3 ${
            isCourseChallengeActive
              ? 'bg-ka-blue-light border-l-4 border-l-ka-blue text-ka-blue'
              : 'hover:bg-slate-50 text-ka-text-primary'
          }`}
        >
          <span className="text-xl leading-none">📖</span>
          <div>
            <span className="block text-sm font-bold text-ka-text-primary">
              Course challenge
            </span>
            <span className="block text-xs text-ka-text-secondary mt-0.5 line-clamp-1">
              Test your knowledge of the skills in this course.
            </span>
          </div>
        </button>
      </nav>
    </aside>
  );
};
