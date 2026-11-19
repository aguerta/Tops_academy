import React, { useState, useRef, useEffect } from 'react';
import { Question, StructuredUserAnswer } from '../types';
import { MathText } from './MathText';
import { CoordinatePlane } from './CoordinatePlane';
import { SymbolicInput } from './SymbolicInput';
import { ProofDAG } from './ProofDAG';
import { AdversarialArena, AdversarialAnswerState } from './AdversarialArena';
import { Stage0Modeler, Stage0AnswerState } from './Stage0Modeler';
import { InvariantCanvas, InvariantCanvasAnswerState } from './InvariantCanvas';
import { ConceptMatching } from './ConceptMatching';
import { MathKeypadPopover } from './MathKeypadPopover';
import { isOptionCorrect, requiresBlankFirstCurtain } from '../utils/questionUtils';
import { buildSocraticPrompt } from '../utils/socraticPrompt';

interface QuestionCardProps {
  question: Question;
  selectedOption: string | null;
  selectedMultiOptions: string[];
  fillBlankValue: string;
  structuredAnswer?: StructuredUserAnswer | null;
  matchedDiagnosticRationale?: string | null;
  stage0Phase?: 1 | 2 | 3;
  stage0PhaseNotice?: string | null;
  isChecked: boolean;
  isCorrect: boolean | null;
  onSelectOption: (id: string) => void;
  onToggleMultiOption: (id: string) => void;
  onChangeFillBlank: (val: string) => void;
  onChangeStructuredAnswer?: (next: StructuredUserAnswer) => void;
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
  ironMode?: boolean;
  onSelectStage0Phase?: (phase: 1 | 2 | 3) => void;
}

const OPTION_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'];

export const QuestionCard: React.FC<QuestionCardProps> = ({
  question,
  selectedOption,
  selectedMultiOptions,
  fillBlankValue,
  structuredAnswer = null,
  matchedDiagnosticRationale = null,
  stage0Phase = 1,
  stage0PhaseNotice = null,
  isChecked,
  isCorrect,
  onSelectOption,
  onToggleMultiOption,
  onChangeFillBlank,
  onChangeStructuredAnswer,
  hintsRevealed,
  onRevealHint,
  isExhausted = false,
  blankFirstEnabled = true,
  isCurtainLifted = true,
  onLiftCurtain,
  courseTitle = 'Tops Academy',
  wrongAttemptsCount = 0,
  isPracticeMode = true,
  ironMode = false,
  onSelectStage0Phase,
}) => {
  const [showHintsSection, setShowHintsSection] = useState(false);
  const [hasCopiedPrompt, setHasCopiedPrompt] = useState(false);
  const fillInputRef = useRef<HTMLInputElement>(null);

  const showBlankFirstCurtain =
    !ironMode && blankFirstEnabled && !isCurtainLifted && requiresBlankFirstCurtain(question);

  useEffect(() => {
    if (
      question.type === 'fill_in_the_blank' &&
      !showBlankFirstCurtain &&
      !isChecked &&
      !isExhausted
    ) {
      fillInputRef.current?.focus({ preventScroll: true });
    }
  }, [question.id, question.type, showBlankFirstCurtain, isChecked, isExhausted]);

  const totalHints = question.hints ? question.hints.length : 0;
  const minAttemptsNeeded = totalHints > 0 ? 3 : 2;
  const isSocraticUnlocked =
    !ironMode && isPracticeMode && (isExhausted || wrongAttemptsCount >= minAttemptsNeeded);

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
      errorRationale = matchedDiagnosticRationale || question.misconception_warning;
    } else if (matchedDiagnosticRationale) {
      errorRationale = matchedDiagnosticRationale;
    }

    const promptText = buildSocraticPrompt({
      courseTitle,
      question,
      selectedOptionContent: selectedContent,
      structuredAnswer,
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

      {/* Milestone 6 / 20 Smart Blank-First Curtain (Free Recall for option-based / DAG / matching items only) */}
      {showBlankFirstCurtain ? (
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
            {question.type === 'open_symbolic' && 'Formula la expresión matemática o científica equivalente:'}
            {question.type === 'proof_dag' && 'Construye la demostración lógica omitiendo pasos falaces:'}
            {question.type === 'adversarial_break' &&
              (question.adversarial_break?.mode === 'counterexample'
                ? 'Propón un contraejemplo numérico explícito:'
                : 'Identifica la falacia escondida en la derivación:')}
            {question.type === 'unstructured_model' && 'Resuelve secuencialmente las 3 fases de modelado formal:'}
            {question.type === 'invariant_canvas' && 'Configura el sistema gráfico hasta satisfacer todos los invariantes:'}
            {question.type === 'concept_matching' && 'Asocia cada premisa con su consecuencia correcta:'}
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
          <div className="relative max-w-md">
            <input
              ref={fillInputRef}
              type="text"
              data-testid="fill-blank-input"
              aria-label="Your answer"
              value={fillBlankValue}
              disabled={(isChecked && isCorrect === true) || isExhausted}
              onChange={(e) => onChangeFillBlank(e.target.value)}
              placeholder="Type your answer or mathematical expression..."
              className={`w-full p-3 pr-12 text-sm sm:text-base border-2 rounded-lg outline-none transition-all ${
                isExhausted
                  ? 'border-red-400 bg-slate-100 text-slate-600 cursor-not-allowed'
                  : isChecked
                  ? isCorrect
                    ? 'border-ka-green-border bg-emerald-50/40 text-ka-green-text'
                    : 'border-red-500 bg-red-50/40 text-red-800'
                  : 'border-slate-300 focus:border-ka-blue focus:ring-2 focus:ring-blue-100'
              }`}
            />
            <div className="absolute right-2 top-1/2 -translate-y-1/2">
              <MathKeypadPopover
                disabled={(isChecked && isCorrect === true) || isExhausted}
                onInsert={(token, cursorOffsetBack = 0) => {
                  const el = fillInputRef.current;
                  if (!el) {
                    onChangeFillBlank(`${fillBlankValue}${token}`);
                    return;
                  }
                  const start = el.selectionStart ?? fillBlankValue.length;
                  const end = el.selectionEnd ?? fillBlankValue.length;
                  const next = `${fillBlankValue.slice(0, start)}${token}${fillBlankValue.slice(end)}`;
                  onChangeFillBlank(next);
                  requestAnimationFrame(() => {
                    el.focus();
                    const pos = Math.max(0, start + token.length - cursorOffsetBack);
                    el.setSelectionRange(pos, pos);
                  });
                }}
                onBackspace={() => {
                  if (!fillBlankValue) return;
                  const el = fillInputRef.current;
                  if (!el) {
                    onChangeFillBlank(fillBlankValue.slice(0, -1));
                    return;
                  }
                  const start = el.selectionStart ?? fillBlankValue.length;
                  const end = el.selectionEnd ?? fillBlankValue.length;
                  let next = fillBlankValue;
                  let nextPos = start;
                  if (start !== end) {
                    next = `${fillBlankValue.slice(0, start)}${fillBlankValue.slice(end)}`;
                    nextPos = start;
                  } else if (start > 0) {
                    next = `${fillBlankValue.slice(0, start - 1)}${fillBlankValue.slice(end)}`;
                    nextPos = start - 1;
                  }
                  onChangeFillBlank(next);
                  requestAnimationFrame(() => {
                    el.focus();
                    el.setSelectionRange(nextPos, nextPos);
                  });
                }}
              />
            </div>
          </div>

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

      {/* Type 4: Open Symbolic */}
      {question.type === 'open_symbolic' && (
        <SymbolicInput
          value={structuredAnswer?.kind === 'open_symbolic' ? structuredAnswer.expression : ''}
          config={question.symbolic_config}
          disabled={(isChecked && isCorrect === true) || isExhausted}
          isChecked={isChecked}
          isCorrect={isCorrect}
          onChange={(expr) =>
            onChangeStructuredAnswer?.({ kind: 'open_symbolic', expression: expr })
          }
        />
      )}

      {/* Type 5: ProofDAG */}
      {question.type === 'proof_dag' && question.proof_dag && (
        <ProofDAG
          spec={question.proof_dag}
          orderedStepIds={
            structuredAnswer?.kind === 'proof_dag' ? structuredAnswer.orderedStepIds : []
          }
          justifications={
            structuredAnswer?.kind === 'proof_dag' ? structuredAnswer.justifications : {}
          }
          disabled={(isChecked && isCorrect === true) || isExhausted}
          onChange={(orderedStepIds, justifications) =>
            onChangeStructuredAnswer?.({
              kind: 'proof_dag',
              orderedStepIds,
              justifications,
            })
          }
        />
      )}

      {/* Type 6: Adversarial Break */}
      {question.type === 'adversarial_break' && question.adversarial_break && (
        <AdversarialArena
          spec={question.adversarial_break}
          value={
            structuredAnswer?.kind === 'adversarial_break'
              ? {
                  selectedStepId: structuredAnswer.selectedStepId,
                  selectedReasonId: structuredAnswer.selectedReasonId,
                  witnessValues: structuredAnswer.witnessValues,
                }
              : { selectedStepId: null, selectedReasonId: null, witnessValues: {} }
          }
          disabled={(isChecked && isCorrect === true) || isExhausted}
          onChange={(next: AdversarialAnswerState) =>
            onChangeStructuredAnswer?.({
              kind: 'adversarial_break',
              ...next,
            })
          }
        />
      )}

      {/* Type 7: Unstructured Model (Stage 0) */}
      {question.type === 'unstructured_model' && question.unstructured_model && (
        <div className="space-y-2.5">
          {stage0PhaseNotice && (
            <div
              data-testid="stage0-phase-notice"
              className="px-3 py-2 rounded-lg bg-emerald-50 border border-emerald-300 text-emerald-900 text-xs font-bold"
            >
              {stage0PhaseNotice}
            </div>
          )}
          <Stage0Modeler
            spec={question.unstructured_model}
            activePhase={stage0Phase}
            ironMode={ironMode}
            onSelectPhase={onSelectStage0Phase}
            value={
              structuredAnswer?.kind === 'unstructured_model'
                ? {
                    phase1Roles: structuredAnswer.phase1Roles,
                    phase2SelectedIds: structuredAnswer.phase2SelectedIds,
                    phase3SelectedId: structuredAnswer.phase3SelectedId,
                    phase3Expression: structuredAnswer.phase3Expression,
                  }
                : {
                    phase1Roles: {},
                    phase2SelectedIds: [],
                    phase3SelectedId: null,
                    phase3Expression: '',
                  }
            }
            disabled={(isChecked && isCorrect === true) || isExhausted}
            isChecked={isChecked}
            isCorrect={isCorrect}
            onChange={(next: Stage0AnswerState) =>
              onChangeStructuredAnswer?.({
                kind: 'unstructured_model',
                ...next,
              })
            }
          />
        </div>
      )}

      {/* Type 8: Invariant Canvas */}
      {question.type === 'invariant_canvas' && question.invariant_canvas && (
        <InvariantCanvas
          spec={question.invariant_canvas}
          value={
            structuredAnswer?.kind === 'invariant_canvas'
              ? {
                  sliderValues: structuredAnswer.sliderValues,
                  pointPositions: structuredAnswer.pointPositions,
                  selectedEdgeIds: structuredAnswer.selectedEdgeIds,
                  infoSets: structuredAnswer.infoSets,
                  inequalityStyle: structuredAnswer.inequalityStyle,
                  inequalityShade: structuredAnswer.inequalityShade,
                }
              : {
                  sliderValues: {},
                  pointPositions: {},
                  selectedEdgeIds: [],
                  infoSets: [],
                  inequalityStyle: question.invariant_canvas.inequality?.initial_style ?? 'solid',
                  inequalityShade: question.invariant_canvas.inequality?.initial_shade ?? 'above',
                }
          }
          disabled={(isChecked && isCorrect === true) || isExhausted}
          onChange={(next: InvariantCanvasAnswerState) =>
            onChangeStructuredAnswer?.({
              kind: 'invariant_canvas',
              ...next,
            })
          }
        />
      )}

      {/* Type 9: Concept Matching */}
      {question.type === 'concept_matching' && question.concept_matching && (
        <ConceptMatching
          key={question.id}
          spec={question.concept_matching}
          pairs={
            structuredAnswer?.kind === 'concept_matching' ? structuredAnswer.pairs : {}
          }
          disabled={(isChecked && isCorrect === true) || isExhausted}
          onChange={(pairs) =>
            onChangeStructuredAnswer?.({
              kind: 'concept_matching',
              pairs,
            })
          }
        />
      )}

      {/* Progressive Hints Section: Hidden in Iron Exam closed-book mode */}
      {!ironMode && (
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
      )}

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
