import React, { useEffect } from 'react';
import { Competency } from '../types';
import { MathText } from './MathText';

interface PreExerciseModalProps {
  competency: Competency;
  questionCount: number;
  onStart: () => void;
  onBack: () => void;
}

export const PreExerciseModal: React.FC<PreExerciseModalProps> = ({
  competency,
  questionCount,
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
      {/* Top Header Bar */}
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
        <h1 className="text-sm sm:text-lg font-bold text-ka-text-primary text-center truncate min-w-0 px-2 flex-1 [&_.katex]:max-w-full">
          <MathText text={competency.name} inline />
        </h1>
        <div className="w-9 shrink-0 text-right text-xs text-ka-blue font-semibold cursor-pointer">
          Share
        </div>
      </header>

      {/* Main Container */}
      <div className="flex-1 flex flex-col items-center justify-center p-4 min-w-0">
        {/* Info Banner */}
        <div className="w-full max-w-2xl mb-4 bg-white border border-ka-border-card rounded-lg p-3 text-xs text-ka-text-secondary flex items-center gap-2 shadow-sm min-w-0">
          <span className="text-ka-blue font-bold text-sm shrink-0">ⓘ</span>
          <span className="min-w-0 break-words [overflow-wrap:anywhere] [&_.katex]:max-w-full [&_.katex]:overflow-x-auto [&_.katex]:overflow-y-hidden [&_span.inline-block]:max-w-full">
            Practice session for <strong><MathText text={competency.name} inline /></strong> ({competency.category}).
            Complete questions to earn mastery points!
          </span>
        </div>

        {/* Blue Hero Panel (#1865f2) */}
        <div className="w-full max-w-2xl bg-ka-blue rounded-xl p-6 sm:p-10 text-center text-white relative overflow-hidden shadow-lg flex flex-col items-center justify-between min-h-[320px] sm:min-h-[380px] min-w-0">
          <div className="min-w-0">
            <h2 className="text-2xl sm:text-4xl font-extrabold tracking-tight break-words">
              Ready to practice?
            </h2>
            <p className="text-base sm:text-xl text-blue-100 mt-2 font-medium break-words">
              Okay, show us what you can do!
            </p>
            <div className="mt-5 inline-block px-4 py-1.5 bg-white/20 backdrop-blur-sm rounded-full text-sm font-bold tracking-wide">
              {questionCount} questions
            </div>
          </div>

          {/* Polygon Mascot Illustrations with smiling eyes */}
          <div className="mt-6 sm:mt-8 flex items-end justify-center gap-3 sm:gap-4 max-w-full overflow-hidden">
            {/* Mascot 1: Navy/Indigo angled polygon */}
            <svg width="84" height="84" viewBox="0 0 100 100" className="drop-shadow-md">
              <polygon points="15,85 85,85 95,30 50,10 5,40" fill="#1e3a8a" />
              {/* Cartoon Eyes looking up */}
              <circle cx="42" cy="45" r="7" fill="#ffffff" />
              <circle cx="44" cy="43" r="3.5" fill="#1e1b4b" />
              <circle cx="62" cy="45" r="7" fill="#ffffff" />
              <circle cx="64" cy="43" r="3.5" fill="#1e1b4b" />
              {/* Smiling mouth */}
              <path d="M 46 62 Q 53 70 60 62" stroke="#ffffff" strokeWidth="3" fill="none" strokeLinecap="round" />
            </svg>

            {/* Mascot 2: Cyan rounded trapezoid (smiling) */}
            <svg width="100" height="100" viewBox="0 0 100 100" className="drop-shadow-md">
              <polygon points="10,90 90,90 80,20 20,20" fill="#06b6d4" />
              {/* Cute Eyes */}
              <circle cx="38" cy="48" r="8" fill="#ffffff" />
              <circle cx="40" cy="46" r="4" fill="#083344" />
              <circle cx="62" cy="48" r="8" fill="#ffffff" />
              <circle cx="64" cy="46" r="4" fill="#083344" />
              {/* Blushing cheeks */}
              <circle cx="28" cy="58" r="4" fill="#fda4af" opacity="0.8" />
              <circle cx="72" cy="58" r="4" fill="#fda4af" opacity="0.8" />
              {/* Big happy smile */}
              <path d="M 42 63 Q 50 74 58 63" stroke="#083344" strokeWidth="3.5" fill="#ffffff" strokeLinecap="round" />
            </svg>

            {/* Mascot 3: Lavender/Periwinkle polygon */}
            <svg width="80" height="80" viewBox="0 0 100 100" className="drop-shadow-md">
              <polygon points="20,85 80,85 90,40 50,15 10,40" fill="#818cf8" />
              {/* Eyes */}
              <circle cx="40" cy="45" r="6.5" fill="#ffffff" />
              <circle cx="42" cy="43" r="3" fill="#312e81" />
              <circle cx="60" cy="45" r="6.5" fill="#ffffff" />
              <circle cx="62" cy="43" r="3" fill="#312e81" />
              {/* Smile */}
              <path d="M 45 60 Q 51 67 57 60" stroke="#312e81" strokeWidth="2.5" fill="none" strokeLinecap="round" />
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
          data-testid="start-practice-btn"
          onClick={onStart}
          className="px-6 sm:px-8 py-2.5 sm:py-3 bg-ka-blue hover:bg-ka-blue-hover text-white text-sm sm:text-base font-bold rounded shadow-md transition-colors shrink-0"
        >
          Let's go
        </button>
      </footer>
    </div>
  );
};
