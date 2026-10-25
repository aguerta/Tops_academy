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
          isExhausted || diagnosticRationales.length > 0 ? 'w-96 max-h-[80vh]' : 'w-80'
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

          {/* Immediate Diagnostic Error Rationale (Refutation Feedback) */}
          {diagnosticRationales.length > 0 && (
            <div
              data-testid="error-rationale-box"
              className="mt-3.5 p-3 bg-rose-50/90 border border-rose-200 rounded-lg text-xs text-rose-950 space-y-1.5"
            >
              <span className="font-bold text-rose-800 uppercase tracking-wider text-[10px] block">
                Diagnostic feedback on your selection:
              </span>
              {diagnosticRationales.map((item, idx) => (
                <div key={idx} className="leading-relaxed text-slate-800">
                  <MathText text={item.rationale} />
                </div>
              ))}
            </div>
          )}

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
                  <MathText text={resolvedSolution} />
                </div>
              </div>

              {resolvedMisconception && (
                <div className="p-2.5 bg-amber-50 border border-amber-200 rounded-lg text-amber-900">
                  <span className="font-bold block mb-0.5">Common Misconception:</span>
                  <MathText text={resolvedMisconception} />
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
              <MathText text={resolvedSolution} />
            </div>
          </div>

          {resolvedMisconception && (
            <div className="p-2.5 bg-amber-50 border border-amber-200 rounded-lg text-amber-900">
              <span className="font-bold block mb-0.5">Common Misconception:</span>
              <MathText text={resolvedMisconception} />
            </div>
          )}
        </div>
      )}

      {/* Downward pointer triangle */}
      <div className="absolute -bottom-2 right-12 w-4 h-4 bg-white border-r border-b border-ka-border-card transform rotate-45" />
    </div>
  );
};
