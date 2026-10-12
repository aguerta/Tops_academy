import React, { useEffect } from 'react';
import { Course } from '../types';

interface CourseChallengeProps {
  course: Course;
  totalQuestions: number;
  onStart: () => void;
  onBack: () => void;
}

export const CourseChallenge: React.FC<CourseChallengeProps> = ({
  course,
  totalQuestions,
  onStart,
  onBack,
}) => {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.isComposing) return;
      if (e.key === 'Enter') {
        e.preventDefault();
        onStart();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [onStart]);

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col justify-between">
      {/* Top Header */}
      <header className="h-16 bg-white border-b border-ka-border-card px-6 flex items-center justify-between">
        <button
          onClick={onBack}
          className="w-9 h-9 rounded-full hover:bg-slate-100 flex items-center justify-center text-ka-text-secondary text-lg transition-colors"
          title="Back to Course Overview"
        >
          ←
        </button>
        <div className="text-sm font-bold text-ka-text-primary uppercase tracking-wider">
          COURSE CHALLENGE • {course.title}
        </div>
        <div className="w-9" />
      </header>

      {/* Main Challenge Hero Container */}
      <div className="flex-1 flex flex-col items-center justify-center p-6">
        <div className="w-full max-w-2xl bg-ka-blue rounded-xl p-8 sm:p-12 text-center text-white relative overflow-hidden shadow-xl flex flex-col items-center justify-between min-h-[420px]">
          <div>
            <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight">
              Ready for a challenge?
            </h1>
            <p className="text-base sm:text-lg text-blue-100 mt-3 font-medium max-w-md mx-auto leading-relaxed">
              Test yourself on the skills in this course and earn mastery points for what you
              already know!
            </p>
            <div className="mt-6 inline-block px-5 py-2 bg-white/20 backdrop-blur-sm rounded-full text-sm font-extrabold tracking-wide">
              {totalQuestions} questions • 30 - 45 minutes
            </div>
          </div>

          {/* Notebook & Pencil Artwork */}
          <div className="mt-8 flex items-center justify-center">
            <svg width="120" height="110" viewBox="0 0 120 110" className="drop-shadow-lg">
              {/* Notebook base */}
              <rect x="25" y="15" width="70" height="85" rx="6" fill="#ffffff" />
              <rect x="25" y="15" width="12" height="85" rx="3" fill="#38bdf8" />
              {/* Binder rings */}
              <circle cx="31" cy="30" r="3" fill="#1e293b" />
              <circle cx="31" cy="50" r="3" fill="#1e293b" />
              <circle cx="31" cy="70" r="3" fill="#1e293b" />
              {/* Notebook lines */}
              <line x1="45" y1="35" x2="85" y2="35" stroke="#cbd5e1" strokeWidth="2.5" strokeLinecap="round" />
              <line x1="45" y1="50" x2="85" y2="50" stroke="#cbd5e1" strokeWidth="2.5" strokeLinecap="round" />
              <line x1="45" y1="65" x2="85" y2="65" stroke="#cbd5e1" strokeWidth="2.5" strokeLinecap="round" />
              {/* Pencil */}
              <g transform="rotate(35 85 45)">
                <rect x="75" y="10" width="10" height="50" rx="2" fill="#f59e0b" />
                <polygon points="75,60 85,60 80,72" fill="#fde68a" />
                <polygon points="78,68 82,68 80,72" fill="#1e293b" />
                <rect x="75" y="8" width="10" height="8" rx="2" fill="#f43f5e" />
              </g>
              {/* Decorative sparks */}
              <path d="M 12 30 L 16 34 M 16 30 L 12 34" stroke="#fef08a" strokeWidth="3" strokeLinecap="round" />
              <path d="M 105 20 L 110 25 M 110 20 L 105 25" stroke="#fef08a" strokeWidth="3" strokeLinecap="round" />
            </svg>
          </div>
        </div>
      </div>

      {/* Bottom Footer Bar */}
      <footer className="h-20 bg-white border-t border-ka-border-card px-8 flex items-center justify-between">
        <button
          onClick={onBack}
          className="w-10 h-10 rounded-full border border-ka-border-card hover:bg-slate-50 flex items-center justify-center text-ka-text-secondary text-base transition-colors"
        >
          ←
        </button>

        <button
          data-testid="start-challenge-btn"
          onClick={onStart}
          className="px-8 py-3 bg-ka-blue hover:bg-ka-blue-hover text-white text-base font-bold rounded shadow-md transition-colors"
        >
          Let's go
        </button>
      </footer>
    </div>
  );
};
