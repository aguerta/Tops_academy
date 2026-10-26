import React, { useEffect } from 'react';
import confetti from 'canvas-confetti';
import { Competency, Course } from '../types';
import { MathText } from './MathText';

interface CompletionScreenProps {
  course: Course;
  competency?: Competency;
  score: number;
  total: number;
  sessionType: 'practice' | 'quiz' | 'test' | 'challenge';
  onTryAgain: () => void;
  onUpNext: () => void;
}

export const CompletionScreen: React.FC<CompletionScreenProps> = ({
  course,
  competency,
  score,
  total,
  sessionType,
  onTryAgain,
  onUpNext,
}) => {
  useEffect(() => {
    // Launch celebratory confetti bursts!
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
  }, []);

  // Enter key navigation to advance or return to course overview
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.isComposing) return;
      if (e.key === 'Enter') {
        e.preventDefault();
        onUpNext();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [onUpNext]);

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

  return (
    <div data-testid="completion-screen" className="min-h-screen min-h-[100dvh] bg-slate-50 flex flex-col justify-between overflow-x-hidden">
      {/* Top Header */}
      <header className="h-16 bg-white border-b border-ka-border-card px-4 sm:px-6 flex items-center justify-between gap-3 min-w-0 shrink-0">
        <div className="flex items-center gap-2 min-w-0 flex-1">
          <span className="text-sm font-bold text-ka-text-primary truncate block min-w-0">
            <MathText text={competency ? competency.name : course.title} inline />
          </span>
        </div>
        <button
          type="button"
          onClick={onUpNext}
          className="text-xs font-semibold text-ka-blue hover:text-ka-blue-hover shrink-0"
        >
          Back to course
        </button>
      </header>

      {/* Main Celebratory Blue Hero Container */}
      <div className="flex-1 flex items-center justify-center p-4 sm:p-6 min-w-0">
        <div className="w-full max-w-4xl bg-ka-blue rounded-2xl p-6 sm:p-10 text-white shadow-xl flex flex-col md:flex-row items-center justify-between gap-6 sm:gap-8 relative overflow-hidden min-w-0">
          {/* Left Hero Content: Thumbs-up illustration + score */}
          <div className="flex flex-col items-center md:items-start text-center md:text-left min-w-0">
            {/* Line-art Thumbs-up Icon with radiating lines */}
            <div className="w-20 h-20 mb-4 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center text-4xl shadow-inner">
              👍
            </div>

            <h1 className="text-2xl sm:text-4xl font-extrabold tracking-tight break-words [overflow-wrap:anywhere]">
              {titlePrefix}
            </h1>
            <p className="text-xl sm:text-2xl font-bold text-blue-100 mt-2">
              {score}/{total} correct
            </p>
            <p className="text-sm text-blue-200 mt-1 max-w-sm">
              Great work! Your practice points have been recorded in your course mastery progress.
            </p>
          </div>

          {/* Right Hero Card: Summary & Level Up */}
          <div className="w-full max-w-md md:max-w-none md:w-80 bg-white text-ka-text-primary rounded-xl p-5 sm:p-6 shadow-2xl flex flex-col gap-3 min-w-0 shrink-0">
            <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-ka-blue">
              <span>🎓</span>
              <span>Mastery Summary</span>
            </div>

            <h3 className="text-lg font-bold text-ka-text-primary">
              Mastery Points Leveled Up!
            </h3>

            <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 text-xs space-y-1.5">
              <div className="flex justify-between">
                <span className="text-slate-500">Correct answers:</span>
                <span className="font-bold text-emerald-600">
                  {score} / {total}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Accuracy:</span>
                <span className="font-bold">
                  {total > 0 ? Math.round((score / total) * 100) : 0}%
                </span>
              </div>
              <div className="flex justify-between items-center pt-1 border-t border-slate-200 min-w-0">
                <span className="text-slate-500 shrink-0">Target Competency:</span>
                <span className="font-bold truncate inline-block max-w-[140px] text-right min-w-0 align-bottom">
                  {competency ? <MathText text={competency.name} inline /> : 'All Units'}
                </span>
              </div>
            </div>

            <p className="text-xs text-slate-500">
              Continue to the next lesson or repeat this practice to reach full mastery!
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
