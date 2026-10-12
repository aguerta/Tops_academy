import React, { useState, useEffect } from 'react';
import { Question } from '../types';
import { MathText } from './MathText';
import { isOptionCorrect } from '../utils/questionUtils';

interface FeedbackToastProps {
  isCorrect: boolean;
  question: Question;
  onClose?: () => void;
  onRedo?: () => void;
  isExhausted?: boolean;
  wrongAttemptsCount?: number;
}

export const FeedbackToast: React.FC<FeedbackToastProps> = ({
  isCorrect,
  question,
  onClose,
  onRedo,
  isExhausted = false,
  wrongAttemptsCount = 0,
}) => {
  const [showSolution, setShowSolution] = useState(isExhausted);

  useEffect(() => {
    if (isExhausted) {
      setShowSolution(true);
    }
  }, [isExhausted]);

  const renderCorrectAnswer = () => {
    if (question.type === 'multiple_choice_7_options') {
      const correctOpts = question.options.filter((opt) => isOptionCorrect(question, opt.id));
      return (
        <div data-testid="correct-answer-display" className="p-3 bg-emerald-50 border border-emerald-300 rounded-lg text-emerald-950">
          <span className="font-bold text-emerald-800 uppercase tracking-wider text-[11px] block mb-1">
            Correct answer:
          </span>
          <div className="space-y-1.5">
            {correctOpts.map((opt) => (
              <div key={opt.id} className="flex items-start gap-2">
                <span className="w-5 h-5 rounded-full bg-ka-green-badge text-white flex items-center justify-center font-bold text-xs flex-shrink-0 mt-0.5">
                  ✓
                </span>
                <div className="text-sm text-slate-800 font-medium">
                  <MathText text={opt.content} inline />
                </div>
              </div>
            ))}
          </div>
        </div>
      );
    } else if (question.type === 'multiple_select') {
      const correctOpts = question.options.filter((opt) => isOptionCorrect(question, opt.id));
      return (
        <div data-testid="correct-answer-display" className="p-3 bg-emerald-50 border border-emerald-300 rounded-lg text-emerald-950">
          <span className="font-bold text-emerald-800 uppercase tracking-wider text-[11px] block mb-1">
            Correct answer(s):
          </span>
          <div className="space-y-1.5">
            {correctOpts.map((opt) => (
              <div key={opt.id} className="flex items-start gap-2">
                <span className="w-5 h-5 rounded-full bg-ka-green-badge text-white flex items-center justify-center font-bold text-xs flex-shrink-0 mt-0.5">
                  ✓
                </span>
                <div className="text-sm text-slate-800 font-medium">
                  <MathText text={opt.content} inline />
                </div>
              </div>
            ))}
          </div>
        </div>
      );
    } else if (question.type === 'fill_in_the_blank') {
      let ansText = '';
      if (
        typeof question.correct_answer === 'object' &&
        question.correct_answer !== null &&
        !Array.isArray(question.correct_answer)
      ) {
        const ansObj = question.correct_answer as any;
        ansText = ansObj.expression || ansObj.value || ansObj.canonical_algebraic || '';
      } else {
        ansText = String(question.correct_answer ?? '');
      }

      return (
        <div data-testid="correct-answer-display" className="p-3 bg-emerald-50 border border-emerald-300 rounded-lg text-emerald-950">
          <span className="font-bold text-emerald-800 uppercase tracking-wider text-[11px] block mb-1">
            Correct answer:
          </span>
          <div className="flex items-center gap-2">
            <span className="w-5 h-5 rounded-full bg-ka-green-badge text-white flex items-center justify-center font-bold text-xs flex-shrink-0">
              ✓
            </span>
            <div className="text-sm font-semibold text-slate-800">
              <MathText text={`$${ansText}$`} inline />
            </div>
          </div>
        </div>
      );
    }
    return null;
  };

  if (!isCorrect) {
    return (
      <div
        data-testid="feedback-toast"
        className={`feedback-toast absolute right-8 bottom-24 z-30 ${
          isExhausted ? 'w-96 max-h-[80vh]' : 'w-80'
        } bg-white border border-red-200 rounded-xl shadow-2xl p-5 flex flex-col animate-in fade-in slide-in-from-bottom-2 duration-200`}
      >
        <div className="overflow-y-auto max-h-[calc(80vh-2.5rem)] pr-1">
          <div className="flex items-start justify-between gap-3">
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-full bg-red-600 text-white flex items-center justify-center font-bold text-lg flex-shrink-0">
                ✕
              </div>
              <div>
                <h4 className="text-base font-bold text-ka-text-primary leading-tight">
                  {isExhausted
                    ? 'Maximum attempts reached (3/3)'
                    : 'Not quite yet.'}
                </h4>
                <p className="text-xs text-ka-text-secondary mt-1">
                  {isExhausted
                    ? 'Review the correct answer and step-by-step solution below.'
                    : 'Try again or check a hint for help!'}
                </p>
                {!isExhausted && onRedo && (
                  <div className="mt-3">
                    <button
                      data-testid="toast-quick-redo-btn"
                      onClick={onRedo}
                      className="px-3 py-1.5 bg-red-600 hover:bg-red-700 text-white text-xs font-bold rounded-md shadow-sm transition-colors flex items-center gap-1.5 cursor-pointer"
                    >
                      <span>↺</span>
                      <span>Quick Redo</span>
                    </button>
                  </div>
                )}
              </div>
            </div>
            {onClose && (
              <button
                onClick={onClose}
                className="text-slate-400 hover:text-slate-600 text-sm font-bold"
              >
                ✕
              </button>
            )}
          </div>

          {/* Solution & Correct Answer Drawer for Exhausted Attempts */}
          {(isExhausted || showSolution) && (
            <div
              data-testid="step-by-step-solution"
              className="mt-4 pt-4 border-t border-ka-border-subtle text-xs text-ka-text-primary space-y-3"
            >
              {renderCorrectAnswer()}

              <div>
                <span className="font-bold text-slate-800 uppercase tracking-wider text-[11px] block mb-1">
                  Step-by-step solution:
                </span>
                <div data-testid="solution-content" className="bg-slate-50 p-3 rounded-lg leading-relaxed text-slate-800">
                  <MathText text={question.solution} />
                </div>
              </div>

              {question.misconception_warning && (
                <div className="p-2.5 bg-amber-50 border border-amber-200 rounded-lg text-amber-900">
                  <span className="font-bold block mb-0.5">Common Misconception:</span>
                  <MathText text={question.misconception_warning} />
                </div>
              )}
            </div>
          )}
        </div>

        {/* Downward pointer triangle */}
        <div className="absolute -bottom-2 right-12 w-4 h-4 bg-white border-r border-b border-red-200 transform rotate-45" />
      </div>
    );
  }

  return (
    <div
      data-testid="good-work-toast"
      className="absolute right-8 bottom-24 z-30 w-84 bg-white border border-ka-border-card rounded-xl shadow-2xl p-5 animate-in fade-in slide-in-from-bottom-2 duration-200"
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-3">
          {/* Green checkmark circle */}
          <div className="w-9 h-9 rounded-full bg-ka-green-badge text-white flex items-center justify-center font-bold text-xl flex-shrink-0 shadow-sm">
            ✓
          </div>
          <div>
            <h4 className="text-lg font-bold text-ka-text-primary leading-tight">
              Good work!
            </h4>
            <p className="text-xs text-ka-text-secondary mt-0.5">
              Keep going.
            </p>
            <button
              data-testid="solution-link"
              onClick={() => setShowSolution(!showSolution)}
              className="mt-2 text-xs font-semibold text-ka-blue hover:text-ka-blue-hover hover:underline text-left block"
            >
              See a step-by-step solution.
            </button>
          </div>
        </div>
        {onClose && (
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-600 text-sm font-bold"
          >
            ✕
          </button>
        )}
      </div>

      {/* Expandable Step-by-step solution drawer */}
      {showSolution && (
        <div
          data-testid="step-by-step-solution"
          className="mt-4 pt-4 border-t border-ka-border-subtle text-xs text-ka-text-primary space-y-3 max-h-60 overflow-y-auto"
        >
          <div>
            <span className="font-bold text-slate-800 uppercase tracking-wider text-[11px] block mb-1">
              Step-by-step solution:
            </span>
            <div data-testid="solution-content" className="bg-slate-50 p-3 rounded-lg leading-relaxed">
              <MathText text={question.solution} />
            </div>
          </div>

          {question.misconception_warning && (
            <div className="p-2.5 bg-amber-50 border border-amber-200 rounded-lg text-amber-900">
              <span className="font-bold block mb-0.5">Common Misconception:</span>
              <MathText text={question.misconception_warning} />
            </div>
          )}
        </div>
      )}

      {/* Downward pointer triangle */}
      <div className="absolute -bottom-2 right-12 w-4 h-4 bg-white border-r border-b border-ka-border-card transform rotate-45" />
    </div>
  );
};
