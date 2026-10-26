import React, { useState, useEffect } from 'react';
import { Question } from '../types';
import { MathText } from './MathText';
import { isOptionCorrect } from '../utils/questionUtils';

interface FeedbackToastProps {
  isCorrect: boolean;
  question: Question;
  selectedOption?: string | null;
  selectedMultiOptions?: string[];
  onClose?: () => void;
  onRedo?: () => void;
  isExhausted?: boolean;
  wrongAttemptsCount?: number;
}

interface DiagnosticRationaleItem {
  optionId: string;
  content: string;
  rationale: string;
}

export const FeedbackToast: React.FC<FeedbackToastProps> = ({
  isCorrect,
  question,
  selectedOption = null,
  selectedMultiOptions = [],
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

  const getDiagnosticRationales = (): DiagnosticRationaleItem[] => {
    if (isCorrect || !question || !question.options) {
      return [];
    }

    if (question.type === 'multiple_choice_7_options' && selectedOption) {
      const chosenOpt = question.options.find((opt) => opt.id === selectedOption);
      if (
        chosenOpt &&
        !isOptionCorrect(question, chosenOpt.id) &&
        typeof chosenOpt.error_rationale === 'string' &&
        chosenOpt.error_rationale.trim() !== ''
      ) {
        return [
          {
            optionId: chosenOpt.option_id || chosenOpt.id,
            content: chosenOpt.content,
            rationale: chosenOpt.error_rationale.trim(),
          },
        ];
      }
    } else if (
      question.type === 'multiple_select' &&
      Array.isArray(selectedMultiOptions) &&
      selectedMultiOptions.length > 0
    ) {
      return question.options
        .filter(
          (opt) =>
            selectedMultiOptions.includes(opt.id) &&
            !isOptionCorrect(question, opt.id) &&
            typeof opt.error_rationale === 'string' &&
            opt.error_rationale.trim() !== ''
        )
        .map((opt) => ({
          optionId: opt.option_id || opt.id,
          content: opt.content,
          rationale: (opt.error_rationale || '').trim(),
        }));
    }

    return [];
  };

  const diagnosticRationales = getDiagnosticRationales();
  const resolvedSolution =
    question.solution || question.detailed_solution || '';
  const resolvedMisconception =
    question.misconception_warning || question.common_misconception_warning || '';

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
              <div key={opt.id} className="flex items-start gap-2 min-w-0">
                <span className="w-5 h-5 rounded-full bg-ka-green-badge text-white flex items-center justify-center font-bold text-xs flex-shrink-0 mt-0.5" aria-hidden="true">
                  ✓
                </span>
                <div className="text-sm text-slate-800 font-medium min-w-0 flex-1 overflow-x-auto">
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
              <div key={opt.id} className="flex items-start gap-2 min-w-0">
                <span className="w-5 h-5 rounded-full bg-ka-green-badge text-white flex items-center justify-center font-bold text-xs flex-shrink-0 mt-0.5" aria-hidden="true">
                  ✓
                </span>
                <div className="text-sm text-slate-800 font-medium min-w-0 flex-1 overflow-x-auto">
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
          <div className="flex items-center gap-2 min-w-0">
            <span className="w-5 h-5 rounded-full bg-ka-green-badge text-white flex items-center justify-center font-bold text-xs flex-shrink-0" aria-hidden="true">
              ✓
            </span>
            <div className="text-sm font-semibold text-slate-800 min-w-0 flex-1 overflow-x-auto">
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
        role="alert"
        aria-live="assertive"
        className={`feedback-toast feedback-toast-root fixed z-30 bottom-20 inset-x-3 sm:inset-x-6 max-w-xl mx-auto max-h-[45dvh] lg:[@media(min-height:851px)]:inset-x-auto lg:[@media(min-height:851px)]:right-8 lg:[@media(min-height:851px)]:bottom-20 lg:[@media(min-height:851px)]:mx-0 lg:[@media(min-height:851px)]:max-w-none ${
          isExhausted || diagnosticRationales.length > 0
            ? 'lg:[@media(min-height:851px)]:w-96 lg:[@media(min-height:851px)]:max-h-[80vh]'
            : 'lg:[@media(min-height:851px)]:w-80'
        } bg-white border border-red-200 rounded-xl shadow-2xl p-4 sm:p-5 flex flex-col overflow-hidden animate-in fade-in slide-in-from-bottom-2 duration-200`}
      >
        {/* Responsive bottom-sheet & KaTeX overflow protection styles */}
        <style>{`
          .feedback-toast-root .katex-display {
            max-width: 100% !important;
            overflow-x: auto !important;
            overflow-y: hidden !important;
          }
          .feedback-toast-root .katex {
            max-width: 100% !important;
            overflow-x: auto !important;
            overflow-y: hidden !important;
            vertical-align: middle;
          }
          .feedback-toast-root pre,
          .feedback-toast-root code {
            max-width: 100% !important;
            overflow-x: auto !important;
          }
          @media (max-width: 1023px), (max-height: 850px) {
            .feedback-toast-root {
              position: fixed !important;
              left: 0.75rem !important;
              right: 0.75rem !important;
              bottom: 5rem !important;
              max-width: 36rem !important;
              margin-left: auto !important;
              margin-right: auto !important;
              max-height: 45dvh !important;
              box-sizing: border-box !important;
              overflow: hidden !important;
            }
            .feedback-toast-pointer {
              display: none !important;
            }
            .feedback-toast-scroll {
              max-height: calc(45dvh - 2.5rem) !important;
              overflow-y: auto !important;
            }
            .feedback-toast-sol-scroll {
              flex: 1 1 auto !important;
              min-height: 0 !important;
              max-height: calc(45dvh - 6.5rem) !important;
              overflow-y: auto !important;
            }
          }
        `}</style>
        <div className="feedback-toast-scroll overflow-y-auto max-h-[calc(45dvh-2.5rem)] lg:[@media(min-height:851px)]:max-h-[calc(80vh-2.5rem)] pr-1 flex-1 min-h-0">
          <div className="flex items-start justify-between gap-3 shrink-0">
            <div className="flex items-start gap-3 min-w-0">
              <div className="w-8 h-8 rounded-full bg-red-600 text-white flex items-center justify-center font-bold text-lg flex-shrink-0" aria-hidden="true">
                ✕
              </div>
              <div className="min-w-0">
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
                      aria-label="Quick redo"
                      className="px-3 py-1.5 bg-red-600 hover:bg-red-700 text-white text-xs font-bold rounded-md shadow-sm transition-colors flex items-center gap-1.5 cursor-pointer"
                    >
                      <span aria-hidden="true">↺</span>
                      <span>Quick Redo</span>
                    </button>
                  </div>
                )}
              </div>
            </div>
            {onClose && (
              <button
                onClick={onClose}
                aria-label="Close feedback"
                className="text-slate-400 hover:text-slate-600 text-sm font-bold shrink-0 p-1"
              >
                ✕
              </button>
            )}
          </div>

          {/* Immediate Diagnostic Error Rationale (Refutation Feedback) */}
          {diagnosticRationales.length > 0 && (
            <div
              data-testid="error-rationale-box"
              className="mt-3.5 p-3 bg-rose-50/90 border border-rose-200 rounded-lg text-xs text-rose-950 space-y-1.5 min-w-0 overflow-hidden"
            >
              <span className="font-bold text-rose-800 uppercase tracking-wider text-[10px] block">
                Diagnostic feedback on your selection:
              </span>
              {diagnosticRationales.map((item, idx) => (
                <div key={idx} className="leading-relaxed text-slate-800 min-w-0 break-words overflow-x-auto">
                  <MathText text={item.rationale} />
                </div>
              ))}
            </div>
          )}

          {/* Solution & Correct Answer Drawer for Exhausted Attempts */}
          {(isExhausted || showSolution) && (
            <div
              data-testid="step-by-step-solution"
              className="mt-4 pt-4 border-t border-ka-border-subtle text-xs text-ka-text-primary space-y-3 min-w-0"
            >
              {renderCorrectAnswer()}

              <div className="min-w-0">
                <span className="font-bold text-slate-800 uppercase tracking-wider text-[11px] block mb-1">
                  Step-by-step solution:
                </span>
                <div data-testid="solution-content" className="bg-slate-50 p-3 rounded-lg leading-relaxed text-slate-800 min-w-0 break-words overflow-x-auto">
                  <MathText text={resolvedSolution} />
                </div>
              </div>

              {resolvedMisconception && (
                <div className="p-2.5 bg-amber-50 border border-amber-200 rounded-lg text-amber-900 min-w-0 break-words overflow-x-auto">
                  <span className="font-bold block mb-0.5">Common Misconception:</span>
                  <MathText text={resolvedMisconception} />
                </div>
              )}
            </div>
          )}
        </div>

        {/* Downward pointer triangle */}
        <div className="feedback-toast-pointer hidden lg:[@media(min-height:851px)]:block absolute -bottom-2 right-12 w-4 h-4 bg-white border-r border-b border-red-200 transform rotate-45" />
      </div>
    );
  }

  return (
    <div
      data-testid="good-work-toast"
      role="status"
      aria-live="polite"
      className="feedback-toast feedback-toast-root fixed z-30 bottom-20 inset-x-3 sm:inset-x-6 max-w-xl mx-auto max-h-[45dvh] lg:[@media(min-height:851px)]:inset-x-auto lg:[@media(min-height:851px)]:right-8 lg:[@media(min-height:851px)]:bottom-20 lg:[@media(min-height:851px)]:mx-0 lg:[@media(min-height:851px)]:max-w-none lg:[@media(min-height:851px)]:w-84 bg-white border border-ka-border-card rounded-xl shadow-2xl p-4 sm:p-5 flex flex-col overflow-hidden animate-in fade-in slide-in-from-bottom-2 duration-200"
    >
      {/* Responsive bottom-sheet & KaTeX overflow protection styles */}
      <style>{`
        .feedback-toast-root .katex-display {
          max-width: 100% !important;
          overflow-x: auto !important;
          overflow-y: hidden !important;
        }
        .feedback-toast-root .katex {
          max-width: 100% !important;
          overflow-x: auto !important;
          overflow-y: hidden !important;
          vertical-align: middle;
        }
        .feedback-toast-root pre,
        .feedback-toast-root code {
          max-width: 100% !important;
          overflow-x: auto !important;
        }
        @media (max-width: 1023px), (max-height: 850px) {
          .feedback-toast-root {
            position: fixed !important;
            left: 0.75rem !important;
            right: 0.75rem !important;
            bottom: 5rem !important;
            max-width: 36rem !important;
            margin-left: auto !important;
            margin-right: auto !important;
            max-height: 45dvh !important;
            box-sizing: border-box !important;
            overflow: hidden !important;
          }
          .feedback-toast-pointer {
            display: none !important;
          }
          .feedback-toast-scroll {
            max-height: calc(45dvh - 2.5rem) !important;
            overflow-y: auto !important;
          }
          .feedback-toast-sol-scroll {
            flex: 1 1 auto !important;
            min-height: 0 !important;
            max-height: calc(45dvh - 6.5rem) !important;
            overflow-y: auto !important;
          }
        }
      `}</style>
      <div className="flex items-start justify-between gap-3 shrink-0">
        <div className="flex items-start gap-3 min-w-0">
          {/* Green checkmark circle */}
          <div className="w-9 h-9 rounded-full bg-ka-green-badge text-white flex items-center justify-center font-bold text-xl flex-shrink-0 shadow-sm" aria-hidden="true">
            ✓
          </div>
          <div className="min-w-0">
            <h4 className="text-lg font-bold text-ka-text-primary leading-tight">
              Good work!
            </h4>
            <p className="text-xs text-ka-text-secondary mt-0.5">
              Keep going.
            </p>
            <button
              data-testid="solution-link"
              aria-expanded={showSolution}
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
            aria-label="Close feedback"
            className="text-slate-400 hover:text-slate-600 text-sm font-bold shrink-0 p-1"
          >
            ✕
          </button>
        )}
      </div>

      {/* Expandable Step-by-step solution drawer */}
      {showSolution && (
        <div
          data-testid="step-by-step-solution"
          className="feedback-toast-sol-scroll mt-3 pt-3 border-t border-ka-border-subtle text-xs text-ka-text-primary space-y-3 max-h-[calc(45dvh-6.5rem)] lg:[@media(min-height:851px)]:max-h-60 overflow-y-auto min-h-0 flex-1 min-w-0 pr-1"
        >
          <div className="min-w-0">
            <span className="font-bold text-slate-800 uppercase tracking-wider text-[11px] block mb-1">
              Step-by-step solution:
            </span>
            <div data-testid="solution-content" className="bg-slate-50 p-3 rounded-lg leading-relaxed min-w-0 break-words overflow-x-auto">
              <MathText text={resolvedSolution} />
            </div>
          </div>

          {resolvedMisconception && (
            <div className="p-2.5 bg-amber-50 border border-amber-200 rounded-lg text-amber-900 min-w-0 break-words overflow-x-auto">
              <span className="font-bold block mb-0.5">Common Misconception:</span>
              <MathText text={resolvedMisconception} />
            </div>
          )}
        </div>
      )}

      {/* Downward pointer triangle */}
      <div className="feedback-toast-pointer hidden lg:[@media(min-height:851px)]:block absolute -bottom-2 right-12 w-4 h-4 bg-white border-r border-b border-ka-border-card transform rotate-45" />
    </div>
  );
};
