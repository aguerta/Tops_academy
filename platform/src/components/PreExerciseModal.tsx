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
    <div className="min-h-screen bg-slate-50 flex flex-col justify-between">
      {/* Top Header Bar */}
      <header className="h-16 bg-white border-b border-ka-border-card px-6 flex items-center justify-between">
        <button
          onClick={onBack}
          className="w-9 h-9 rounded-full hover:bg-slate-100 flex items-center justify-center text-ka-text-secondary text-lg transition-colors"
          title="Back to Course Overview"
        >
          ←
        </button>
        <h1 className="text-lg font-bold text-ka-text-primary text-center">
          <MathText text={competency.name} inline />
        </h1>
        <div className="w-9 text-right text-xs text-ka-blue font-semibold cursor-pointer">
          Share
        </div>
      </header>

      {/* Main Container */}
      <div className="flex-1 flex flex-col items-center justify-center p-4">
        {/* Info Banner */}
        <div className="w-full max-w-2xl mb-4 bg-white border border-ka-border-card rounded-lg p-3 text-xs text-ka-text-secondary flex items-center gap-2 shadow-sm">
          <span className="text-ka-blue font-bold text-sm">ⓘ</span>
          <span>
            Practice session for <strong><MathText text={competency.name} inline /></strong> ({competency.category}).
            Complete questions to earn mastery points!
          </span>
        </div>

        {/* Blue Hero Panel (#1865f2) */}
        <div className="w-full max-w-2xl bg-ka-blue rounded-xl p-8 sm:p-12 text-center text-white relative overflow-hidden shadow-lg flex flex-col items-center justify-between min-h-[380px]">
          <div>
            <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight">
              Ready to practice?
            </h2>
            <p className="text-lg sm:text-xl text-blue-100 mt-2 font-medium">
              Okay, show us what you can do!
            </p>
            <div className="mt-5 inline-block px-4 py-1.5 bg-white/20 backdrop-blur-sm rounded-full text-sm font-bold tracking-wide">
              {questionCount} questions
            </div>
          </div>

          {/* Polygon Mascot Illustrations with smiling eyes */}
          <div className="mt-8 flex items-end justify-center gap-4">
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
      <footer className="h-20 bg-white border-t border-ka-border-card px-8 flex items-center justify-between">
        <button
          onClick={onBack}
          className="w-10 h-10 rounded-full border border-ka-border-card hover:bg-slate-50 flex items-center justify-center text-ka-text-secondary text-base transition-colors"
        >
          ←
        </button>

        <button
          data-testid="start-practice-btn"
          onClick={onStart}
          className="px-8 py-3 bg-ka-blue hover:bg-ka-blue-hover text-white text-base font-bold rounded shadow-md transition-colors"
        >
          Let's go
        </button>
      </footer>
    </div>
  );
};
