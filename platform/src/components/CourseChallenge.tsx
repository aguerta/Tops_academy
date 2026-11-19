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
    <div className="min-h-screen min-h-[100dvh] bg-slate-50 flex flex-col justify-between overflow-x-hidden">
      {/* Top Header */}
      <header className="h-16 bg-white border-b border-ka-border-card px-4 sm:px-6 flex items-center justify-between gap-2 shrink-0">
        <button
          type="button"
          aria-label="Back to Course Overview"
          onClick={onBack}
          className="w-9 h-9 shrink-0 rounded-full hover:bg-slate-100 flex items-center justify-center text-ka-text-secondary text-lg transition-colors"
          title="Back to Course Overview"
        >
          ←
        </button>
        <div className="text-xs sm:text-sm font-bold text-ka-text-primary uppercase tracking-wider truncate text-center min-w-0 px-2 flex-1">
          MODO HIERRO • {course.title}
        </div>
        <div className="w-9 shrink-0" />
      </header>

      {/* Main Iron Exam Briefing Container */}
      <div className="flex-1 flex flex-col items-center justify-center p-4 sm:p-6 min-w-0">
        <div
          data-testid="iron-briefing-card"
          className="w-full max-w-2xl bg-slate-900 rounded-xl p-6 sm:p-10 text-center text-white relative overflow-hidden shadow-xl flex flex-col items-center justify-between min-h-[340px] sm:min-h-[400px] min-w-0 border border-indigo-500/30"
        >
          <div className="min-w-0">
            <span className="inline-block px-3 py-1 rounded-full bg-indigo-500/30 border border-indigo-400/40 text-indigo-200 text-xs font-extrabold uppercase tracking-wider mb-3">
              Evaluación Integradora a Libro Cerrado
            </span>
            <h1 className="text-2xl sm:text-4xl font-extrabold tracking-tight break-words [overflow-wrap:anywhere]">
              Examen Modo Hierro
            </h1>
            <p className="text-sm sm:text-base text-slate-200 mt-3 font-medium max-w-lg mx-auto leading-relaxed break-words">
              Demuestra dominio real sin pistas, sin retroalimentación inmediata y con navegación libre. Al finalizar realizarás una auditoría metacognitiva diferida (20% del progreso + calibración de competencias).
            </p>
            <div className="mt-5 flex flex-wrap items-center justify-center gap-2 text-xs font-bold">
              <span className="px-3.5 py-1.5 bg-white/15 rounded-full">
                {totalQuestions} preguntas
              </span>
              <span className="px-3.5 py-1.5 bg-white/15 rounded-full">
                Sin pistas ni feedback inmediato
              </span>
              <span className="px-3.5 py-1.5 bg-indigo-500/40 rounded-full">
                Revisión diferida + calibración
              </span>
            </div>
          </div>

          {/* Iron Shield & Pencil Artwork */}
          <div className="mt-8 flex items-center justify-center">
            <svg width="120" height="110" viewBox="0 0 120 110" className="drop-shadow-lg">
              <rect x="25" y="15" width="70" height="85" rx="6" fill="#ffffff" />
              <rect x="25" y="15" width="12" height="85" rx="3" fill="#6366f1" />
              <circle cx="31" cy="30" r="3" fill="#0f172a" />
              <circle cx="31" cy="50" r="3" fill="#0f172a" />
              <circle cx="31" cy="70" r="3" fill="#0f172a" />
              <line x1="45" y1="35" x2="85" y2="35" stroke="#cbd5e1" strokeWidth="2.5" strokeLinecap="round" />
              <line x1="45" y1="50" x2="85" y2="50" stroke="#cbd5e1" strokeWidth="2.5" strokeLinecap="round" />
              <line x1="45" y1="65" x2="85" y2="65" stroke="#cbd5e1" strokeWidth="2.5" strokeLinecap="round" />
              <g transform="rotate(35 85 45)">
                <rect x="75" y="10" width="10" height="50" rx="2" fill="#f59e0b" />
                <polygon points="75,60 85,60 80,72" fill="#fde68a" />
                <polygon points="78,68 82,68 80,72" fill="#1e293b" />
                <rect x="75" y="8" width="10" height="8" rx="2" fill="#6366f1" />
              </g>
            </svg>
          </div>
        </div>
      </div>

      {/* Bottom Footer Bar */}
      <footer className="h-16 sm:h-20 bg-white border-t border-ka-border-card px-4 sm:px-8 flex items-center justify-between gap-4 shrink-0">
        <button
          type="button"
          aria-label="Back to Course Overview"
          onClick={onBack}
          className="w-10 h-10 rounded-full border border-ka-border-card hover:bg-slate-50 flex items-center justify-center text-ka-text-secondary text-base transition-colors shrink-0"
        >
          ←
        </button>

        <button
          type="button"
          data-testid="start-challenge-btn"
          onClick={onStart}
          className="px-6 sm:px-8 py-2.5 sm:py-3 bg-indigo-700 hover:bg-indigo-800 text-white text-sm sm:text-base font-bold rounded shadow-md transition-colors shrink-0 cursor-pointer"
        >
          Iniciar Modo Hierro
        </button>
      </footer>
    </div>
  );
};
