import React, { useState, useRef, useEffect } from 'react';
import { Question } from '../types';
import { MathText } from './MathText';
import { CoordinatePlane } from './CoordinatePlane';
import { isOptionCorrect } from '../utils/questionUtils';
import { buildSocraticPrompt } from '../utils/socraticPrompt';

interface QuestionCardProps {
  question: Question;
  selectedOption: string | null;
  selectedMultiOptions: string[];
  fillBlankValue: string;
  isChecked: boolean;
  isCorrect: boolean | null;
  onSelectOption: (id: string) => void;
  onToggleMultiOption: (id: string) => void;
  onChangeFillBlank: (val: string) => void;
  hintsRevealed: number;
  onRevealHint: () => void;
  isExhausted?: boolean;
  // Milestone 6: Blank-First Curtain and Socratic Transfer
  blankFirstEnabled?: boolean;
  isCurtainLifted?: boolean;
  onLiftCurtain?: () => void;
  courseTitle?: string;
  wrongAttemptsCount?: number;
  isPracticeMode?: boolean;
}

const OPTION_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'];

export const QuestionCard: React.FC<QuestionCardProps> = ({
  question,
  selectedOption,
  selectedMultiOptions,
  fillBlankValue,
  isChecked,
  isCorrect,
  onSelectOption,
  onToggleMultiOption,
  onChangeFillBlank,
  hintsRevealed,
  onRevealHint,
  isExhausted = false,
  blankFirstEnabled = true,
  isCurtainLifted = true,
  onLiftCurtain,
  courseTitle = 'Tops Academy',
  wrongAttemptsCount = 0,
  isPracticeMode = true,
}) => {
  const [showHintsSection, setShowHintsSection] = useState(false);
  const [hasCopiedPrompt, setHasCopiedPrompt] = useState(false);
  const fillInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (
      question.type === 'fill_in_the_blank' &&
      (!blankFirstEnabled || isCurtainLifted) &&
      !isChecked &&
      !isExhausted
    ) {
      fillInputRef.current?.focus({ preventScroll: true });
    }
  }, [question.id, question.type, isCurtainLifted, blankFirstEnabled, isChecked, isExhausted]);

  const totalHints = question.hints ? question.hints.length : 0;
  const minAttemptsNeeded = totalHints > 0 ? 3 : 2;
  const isSocraticUnlocked =
    isPracticeMode && (isExhausted || wrongAttemptsCount >= minAttemptsNeeded);

  const handleCopySocraticPrompt = async () => {
    let selectedContent: string | undefined;
    let errorRationale: string | undefined;

    if (question.type === 'multiple_choice_7_options' && selectedOption) {
      const opt = question.options?.find((o) => o.id === selectedOption);
      selectedContent = opt ? opt.content : selectedOption;
      errorRationale = (opt?.error_rationale as string) || question.misconception_warning;
    } else if (question.type === 'multiple_select' && selectedMultiOptions.length > 0) {
      const opts = question.options?.filter((o) => selectedMultiOptions.includes(o.id));
      selectedContent = opts?.map((o) => o.content).join('; ') || selectedMultiOptions.join(', ');
      errorRationale =
        opts
          ?.map((o) => o.error_rationale)
          .filter(Boolean)
          .join('; ') || question.misconception_warning;
    } else if (question.type === 'fill_in_the_blank' && fillBlankValue) {
      selectedContent = fillBlankValue;
      errorRationale = question.misconception_warning;
    }

    const promptText = buildSocraticPrompt({
      courseTitle,
      question,
      selectedOptionContent: selectedContent,
      errorRationale: errorRationale || question.misconception_warning,
      hintsRevealed,
    });

    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(promptText);
      } else {
        const textarea = document.createElement('textarea');
        textarea.value = promptText;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
      }
      setHasCopiedPrompt(true);
      setTimeout(() => {
        setHasCopiedPrompt(false);
      }, 2500);
    } catch (err) {
      console.error('Failed to copy socratic prompt:', err);
    }
  };

  // Determine correct answer keys for styling
  const isMcqCorrectOpt = (optId: string) => {
    return isChecked && isOptionCorrect(question, optId);
  };

  const isMultiCorrectOpt = (optId: string) => {
    return isChecked && isOptionCorrect(question, optId);
  };

  const optionsCount = Array.isArray(question.options) ? question.options.length : 0;
  const mcqRowCount = Math.max(1, Math.ceil(optionsCount / 2));
  const multiRowCount = Math.max(1, Math.ceil(optionsCount / 2));

  return (
    <div data-testid="question-card" className="qc-root max-w-3xl mx-auto py-1.5 sm:py-2.5 px-3 sm:px-4">
      {/* Question Stem */}
      <h2
        className="qc-stem max-w-none text-base sm:text-lg font-medium text-ka-text-primary leading-snug sm:leading-relaxed"
        style={{ fontSize: 'var(--qc-font)' }}
      >
        <MathText text={question.stem} />
      </h2>

      {/* Optional Coordinate Plane Graph */}
      {question.graph && (
        <div className="my-2 sm:my-3 text-center">
          <CoordinatePlane graph={question.graph} />
        </div>
      )}

      {/* Milestone 6: Blank-First Curtain (Free Recall) */}
      {blankFirstEnabled && !isCurtainLifted ? (
        <div
          data-testid="blank-first-curtain"
          className="my-3 sm:my-4 p-5 sm:p-6 bg-gradient-to-b from-blue-50/70 via-indigo-50/40 to-slate-50/80 border border-blue-200/80 rounded-xl text-center shadow-sm animate-in fade-in duration-200"
        >
          <div className="w-10 h-10 mx-auto mb-2 bg-blue-100 text-ka-blue rounded-full flex items-center justify-center text-xl shadow-xs">
            🧠
          </div>
          <h3 className="text-sm sm:text-base font-bold text-slate-800">
            Fase de Evocación Libre (Blank-First)
          </h3>
          <p className="text-xs sm:text-sm text-slate-600 mt-1 max-w-md mx-auto leading-relaxed">
            Plantea o deduce la respuesta mentalmente o en tu papel antes de ver las alternativas.
          </p>
          <button
            type="button"
            data-testid="lift-curtain-btn"
            onClick={onLiftCurtain}
            className="mt-4 px-5 py-2.5 bg-ka-blue hover:bg-ka-blue-hover text-white text-xs sm:text-sm font-bold rounded-lg shadow-sm transition-all inline-flex items-center gap-2 cursor-pointer focus:outline-none focus:ring-2 focus:ring-ka-blue focus:ring-offset-1"
          >
            <span>💡 Ya tengo mi planteamiento</span>
            <kbd className="px-2 py-0.5 bg-blue-700/60 text-white rounded text-[11px] font-mono border border-blue-400/40">
              ↵ Enter
            </kbd>
          </button>
        </div>
      ) : (
        <>
          {/* Interaction Prompt */}
          <div className="mt-2 mb-1 sm:mt-2.5 sm:mb-1.5 text-xs sm:text-sm font-bold text-ka-text-secondary">
            {question.type === 'multiple_choice_7_options' && 'Choose 1 answer:'}
            {question.type === 'multiple_select' && 'Choose all answers that apply:'}
            {question.type === 'fill_in_the_blank' &&
              (question.stem.includes('alpha') || question.stem.includes('sigma')
                ? 'Enter your answer (in terms of alpha, n, sigma; L = ...):'
                : 'Enter your answer:')}
          </div>

      {/* Type 1: MCQ with 7 options */}
      {question.type === 'multiple_choice_7_options' && (
        <div className="qc-options-scroll">
          <div
            className="qc-options"
            role="radiogroup"
            aria-label="Answer options"
            style={{
              ['--qc-rows' as any]: mcqRowCount,
              ['--rows' as any]: mcqRowCount,
            }}
          >
            {question.options.map((opt, idx) => {
              const isSelected = selectedOption === opt.id;
              const letter = OPTION_LETTERS[idx] || String.fromCharCode(65 + idx);

              // Check styling states
              const correctOpt = isMcqCorrectOpt(opt.id);
              const wrongSelected = isChecked && isSelected && !isCorrect;

              let containerClasses =
                'border border-ka-border-card hover:bg-slate-50 text-ka-text-primary';
              let badgeClasses =
                'border-2 border-slate-400 text-slate-600 bg-white';
              let badgeContent: React.ReactNode = letter;

              if (isChecked) {
                if (isCorrect && correctOpt) {
                  // Correct answer state (Screen 4 / good_answer.png) - only illuminated when user selected and approved
                  containerClasses =
                    'border-2 border-ka-green-border bg-emerald-50/50 text-ka-green-text';
                  badgeClasses =
                    'bg-ka-green-badge border-ka-green-badge text-white font-bold';
                  badgeContent = `✓ ${letter}`;
                } else if (wrongSelected) {
                  // Wrong selected option
                  containerClasses =
                    'border-2 border-red-500 bg-red-50/50 text-red-800';
                  badgeClasses =
                    'bg-red-600 border-red-600 text-white font-bold';
                  badgeContent = `✕ ${letter}`;
                }
              } else if (isSelected) {
                // Selected prior to check
                containerClasses =
                  'border-2 border-ka-blue bg-ka-blue-light text-ka-blue font-medium';
                badgeClasses =
                  'bg-ka-blue border-ka-blue text-white font-bold';
              }

              return (
                <button
                  key={opt.id}
                  data-testid={`option-${opt.id}`}
                  aria-pressed={isSelected}
                  disabled={(isChecked && isCorrect === true) || isExhausted}
                  onClick={() => onSelectOption(opt.id)}
                  className={`option-item answer-option qc-option-item w-full min-w-0 text-left rounded-lg flex items-center transition-all focus:outline-none focus-visible:ring-2 focus-visible:ring-ka-blue ${containerClasses} ${
                    isExhausted ? 'cursor-not-allowed opacity-75' : ''
                  }`}
                  style={{
                    padding: 'var(--qc-pad)',
                    gap: 'var(--qc-gap)',
                  }}
                >
                  <div
                    className={`qc-badge rounded-full flex items-center justify-center text-xs flex-shrink-0 transition-all ${badgeClasses}`}
                    style={{
                      width: 'var(--qc-badge)',
                      height: 'var(--qc-badge)',
                      minWidth: 'var(--qc-badge)',
                      minHeight: 'var(--qc-badge)',
                    }}
                  >
                    {badgeContent}
                  </div>
                  <div
                    className="flex-1 min-w-0 break-words leading-snug"
                    style={{ fontSize: 'var(--qc-font)' }}
                  >
                    <MathText text={opt.content} inline />
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      )}

      {/* Type 2: Multiple Select */}
      {question.type === 'multiple_select' && (
        <div className="qc-options-scroll">
          <div
            className="qc-options"
            role="group"
            aria-label="Multiple choice options"
            style={{
              ['--qc-rows' as any]: multiRowCount,
              ['--rows' as any]: multiRowCount,
            }}
          >
            {question.options.map((opt, idx) => {
              const isSelected = selectedMultiOptions.includes(opt.id);
              const letter = OPTION_LETTERS[idx] || String.fromCharCode(65 + idx);
              const isTargetCorrect = isMultiCorrectOpt(opt.id);

              let borderClass = 'border-ka-border-card';
              if (isChecked) {
                if (isCorrect && isTargetCorrect && isSelected) {
                  borderClass = 'border-2 border-ka-green-border bg-emerald-50/50';
                } else if (!isCorrect && isSelected) {
                  borderClass = 'border-2 border-red-500 bg-red-50/50';
                }
              } else if (isSelected) {
                borderClass = 'border-2 border-ka-blue bg-ka-blue-light';
              }

              return (
                <label
                  key={opt.id}
                  data-testid={`option-${opt.id}`}
                  className={`option-item answer-option qc-option-item w-full min-w-0 text-left rounded-lg border flex items-center transition-all focus-within:ring-2 focus-within:ring-ka-blue ${
                    isExhausted ? 'cursor-not-allowed opacity-75' : 'cursor-pointer'
                  } ${borderClass}`}
                  style={{
                    padding: 'var(--qc-pad)',
                    gap: 'var(--qc-gap)',
                  }}
                >
                  <input
                    type="checkbox"
                    data-testid="multiselect-option"
                    checked={isSelected}
                    disabled={(isChecked && isCorrect === true) || isExhausted}
                    onChange={() => onToggleMultiOption(opt.id)}
                    className={`w-4 h-4 sm:w-5 sm:h-5 rounded border-slate-300 text-ka-blue focus:ring-ka-blue ${
                      isExhausted ? 'cursor-not-allowed' : 'cursor-pointer'
                    }`}
                  />
                  <span className="w-5 sm:w-6 text-xs font-bold text-slate-500 flex-shrink-0">
                    {letter}
                  </span>
                  <div
                    className="flex-1 min-w-0 break-words leading-snug text-ka-text-primary"
                    style={{ fontSize: 'var(--qc-font)' }}
                  >
                    <MathText text={opt.content} inline />
                  </div>
                </label>
              );
            })}
          </div>
        </div>
      )}

      {/* Type 3: Fill in the blank */}
      {question.type === 'fill_in_the_blank' && (
        <div className="space-y-3">
          <input
            ref={fillInputRef}
            type="text"
            data-testid="fill-blank-input"
            aria-label="Your answer"
            value={fillBlankValue}
            disabled={(isChecked && isCorrect === true) || isExhausted}
            onChange={(e) => onChangeFillBlank(e.target.value)}
            placeholder="Type your answer or mathematical expression..."
            className={`w-full max-w-md p-3 text-sm sm:text-base border-2 rounded-lg outline-none transition-all ${
              isExhausted
                ? 'border-red-400 bg-slate-100 text-slate-600 cursor-not-allowed'
                : isChecked
                ? isCorrect
                  ? 'border-ka-green-border bg-emerald-50/40 text-ka-green-text'
                  : 'border-red-500 bg-red-50/40 text-red-800'
                : 'border-slate-300 focus:border-ka-blue focus:ring-2 focus:ring-blue-100'
            }`}
          />

          {/* Live KaTeX Preview */}
          {fillBlankValue.trim() && (
            <div className="p-2.5 bg-slate-50 border border-slate-200 rounded-lg max-w-md text-sm text-slate-700">
              <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
                Math preview:
              </span>
              <MathText text={`$${fillBlankValue}$`} />
            </div>
          )}
        </div>
      )}

      {/* Progressive Hints Section: Compact single-line toggle always visible below options */}
      <div className="mt-1.5 sm:mt-2 pt-1 border-t border-ka-border-subtle/40">
        <button
          data-testid="hints-toggle"
          aria-expanded={showHintsSection}
          aria-controls="hints-container"
          onClick={() => setShowHintsSection(!showHintsSection)}
          className="text-xs font-semibold text-ka-blue hover:text-ka-blue-hover inline-flex items-center gap-1.5 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-ka-blue rounded py-0.5"
        >
          <span>💡</span>
          <span>Stuck? Review related articles/videos or use a hint.</span>
        </button>

        {showHintsSection && (
          <div
            id="hints-container"
            data-testid="hints-container"
            role="region"
            aria-label="Hints"
            className="mt-2 p-3 bg-slate-50 border border-slate-200 rounded-lg space-y-2 max-h-48 sm:max-h-56 overflow-y-auto"
            style={{ maxHeight: 'clamp(120px, 25vh, 220px)' }}
          >
            <div className="flex items-center justify-between border-b border-slate-200 pb-1 mb-1">
              <span className="text-xs font-bold text-slate-700">💡 Clues & Hints</span>
              <button
                type="button"
                onClick={() => setShowHintsSection(false)}
                className="text-slate-400 hover:text-slate-600 text-xs px-1.5 py-0.5 rounded"
                aria-label="Close hints"
              >
                ✕ Close
              </button>
            </div>

            {hintsRevealed < totalHints && !isChecked && (
              <button
                data-testid="reveal-hint-btn"
                onClick={onRevealHint}
                className="px-3 py-1 bg-ka-blue hover:bg-ka-blue-hover text-white text-xs font-bold rounded shadow-sm transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-ka-blue"
              >
                {hintsRevealed === 0
                  ? `Get hint (1 of ${totalHints})`
                  : `Get next hint (${hintsRevealed + 1} of ${totalHints})`}
              </button>
            )}

            {hintsRevealed === 0 && (
              <p className="text-xs text-slate-500 italic">
                No hints revealed yet. Click "Get hint" to view sequential clues.
              </p>
            )}

            {/* Revealed hints rendered sequentially in order */}
            {question.hints.slice(0, hintsRevealed).map((hint, hIdx) => (
              <div
                key={hIdx}
                data-testid="hint-item"
                className="hint-content p-2.5 bg-white border border-slate-200 rounded-lg text-xs sm:text-sm text-ka-text-primary leading-relaxed shadow-sm animate-in fade-in duration-200"
              >
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-0.5">
                  Hint {hIdx + 1} of {totalHints}
                </span>
                <MathText text={hint} />
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Milestone 6: Socratic Transfer ($0 API) Gate */}
      {isSocraticUnlocked && (
        <div
          data-testid="socratic-tutor-container"
          className="mt-3 p-3 sm:p-3.5 bg-gradient-to-r from-indigo-50/90 via-blue-50/70 to-slate-50 border border-indigo-200/90 rounded-lg shadow-xs flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2.5 animate-in fade-in duration-200"
        >
          <div className="flex items-start gap-2 min-w-0">
            <span className="text-lg shrink-0 mt-0.5" aria-hidden="true">
              🤖
            </span>
            <div className="text-xs">
              <span className="font-bold text-indigo-950 block">
                ¿Atascado tras tus intentos autónomos?
              </span>
              <span className="text-slate-600 block mt-0.5">
                Haz click en el botón y Copia y pega el text en tu IA favorita para ayuda especializada para que te ayude.
              </span>
            </div>
          </div>
          <button
            type="button"
            data-testid="copy-socratic-prompt-btn"
            onClick={handleCopySocraticPrompt}
            className={`px-3 py-1.5 text-xs font-bold rounded-lg shadow-sm transition-all inline-flex items-center gap-1.5 shrink-0 cursor-pointer ${
              hasCopiedPrompt
                ? 'bg-emerald-600 text-white'
                : 'bg-indigo-600 hover:bg-indigo-700 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500'
            }`}
          >
            {hasCopiedPrompt ? (
              <>
                <span aria-hidden="true">✓</span>
                <span>¡Prompt copiado!</span>
              </>
            ) : (
              <>
                <span aria-hidden="true">📋</span>
                <span>Copiar Prompt Socrático</span>
              </>
            )}
          </button>
        </div>
      )}
    </>
  )}
</div>
);
};
