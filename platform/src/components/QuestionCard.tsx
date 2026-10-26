import React, { useState } from 'react';
import { Question } from '../types';
import { MathText } from './MathText';
import { CoordinatePlane } from './CoordinatePlane';
import { isOptionCorrect } from '../utils/questionUtils';

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
}) => {
  const [showHintsSection, setShowHintsSection] = useState(false);

  const totalHints = question.hints ? question.hints.length : 0;

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
    <div data-testid="question-card" className="qc-root max-w-3xl mx-auto py-3 sm:py-5 px-3 sm:px-4">
      {/* Question Stem */}
      <h2
        className="qc-stem max-w-none text-lg font-medium text-ka-text-primary leading-relaxed"
        style={{ fontSize: 'var(--qc-font)' }}
      >
        <MathText text={question.stem} />
      </h2>

      {/* Optional Coordinate Plane Graph */}
      {question.graph && (
        <div className="my-4 text-center">
          <CoordinatePlane graph={question.graph} />
        </div>
      )}

      {/* Interaction Prompt */}
      <div className="mt-3 mb-2 sm:mt-4 sm:mb-2.5 text-sm font-bold text-ka-text-secondary">
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
                  className={`option-item answer-option qc-option-item w-full min-w-0 text-left p-3.5 rounded-lg flex items-center gap-3.5 transition-all focus:outline-none focus-visible:ring-2 focus-visible:ring-ka-blue ${containerClasses} ${
                    isExhausted ? 'cursor-not-allowed opacity-75' : ''
                  }`}
                  style={{
                    padding: 'var(--qc-pad)',
                    gap: 'var(--qc-gap)',
                  }}
                >
                  <div
                    className={`qc-badge w-8 h-8 rounded-full flex items-center justify-center text-xs flex-shrink-0 transition-all ${badgeClasses}`}
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
                    className="flex-1 min-w-0 text-base"
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
                  className={`option-item answer-option qc-option-item w-full min-w-0 text-left p-3.5 rounded-lg border flex items-center gap-3.5 transition-all focus-within:ring-2 focus-within:ring-ka-blue ${
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
                    className={`w-5 h-5 rounded border-slate-300 text-ka-blue focus:ring-ka-blue ${
                      isExhausted ? 'cursor-not-allowed' : 'cursor-pointer'
                    }`}
                  />
                  <span className="w-6 text-xs font-bold text-slate-500 flex-shrink-0">
                    {letter}
                  </span>
                  <div
                    className="flex-1 min-w-0 text-base text-ka-text-primary"
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
            type="text"
            data-testid="fill-blank-input"
            aria-label="Your answer"
            value={fillBlankValue}
            disabled={(isChecked && isCorrect === true) || isExhausted}
            onChange={(e) => onChangeFillBlank(e.target.value)}
            placeholder="Type your answer or mathematical expression..."
            className={`w-full max-w-md p-3.5 text-base border-2 rounded-lg outline-none transition-all ${
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

      {/* Progressive Hints Accordion */}
      <div className="mt-6 sm:mt-8 pt-3 sm:pt-4 border-t border-ka-border-subtle">
        <button
          data-testid="hints-toggle"
          aria-expanded={showHintsSection}
          aria-controls="hints-container"
          onClick={() => setShowHintsSection(!showHintsSection)}
          className="text-xs font-semibold text-ka-blue hover:text-ka-blue-hover flex items-center gap-1.5 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-ka-blue rounded"
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
            className="mt-4 p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-3"
          >
            {hintsRevealed < totalHints && !isChecked && (
              <button
                data-testid="reveal-hint-btn"
                onClick={onRevealHint}
                className="px-3.5 py-1.5 bg-ka-blue hover:bg-ka-blue-hover text-white text-xs font-bold rounded shadow-sm transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-ka-blue focus-visible:ring-offset-1"
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
                className="hint-content p-3 bg-white border border-slate-200 rounded-lg text-sm text-ka-text-primary leading-relaxed shadow-sm animate-in fade-in duration-200"
              >
                <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
                  Hint {hIdx + 1} of {totalHints}
                </span>
                <MathText text={hint} />
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
