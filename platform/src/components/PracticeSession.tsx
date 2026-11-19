import React, { useState, useEffect, useRef } from 'react';
import confetti from 'canvas-confetti';
import { Question, QuestionTelemetry, StructuredUserAnswer } from '../types';
import { QuestionCard } from './QuestionCard';
import { FeedbackToast } from './FeedbackToast';
import { MathText } from './MathText';
import {
  ScratchBgMode,
  SCRATCHPAD_GRID_BG_STYLE,
  ScratchpadOverlay,
} from './ScratchpadOverlay';
import { checkMathEquivalence } from '../utils/mathEquivalence';
import {
  isOptionCorrect,
  getCorrectOptionIds,
  requiresBlankFirstCurtain,
  createInitialStructuredAnswer,
} from '../utils/questionUtils';
import {
  validateAdversarialSubmission,
  validateConceptMatchingSubmission,
  validateProofDagSubmission,
  validateStage0Phase,
  validateSymbolicAnswer,
} from '../services/symbolicValidator';
import {
  validateCartesianInvariants,
  validateTreeInvariants,
} from './canvas/TopologyValidator';
import {
  saveActiveSession,
  clearActiveSession,
  ActiveSessionSnapshot,
} from '../utils/sessionStore';

interface PracticeSessionProps {
  sessionTitle: string;
  questions: Question[];
  onComplete: (
    score: number,
    total: number,
    telemetry?: QuestionTelemetry[],
    totalSeconds?: number
  ) => void;
  onQuit: () => void;
  onRestart?: () => void;
  sessionType?: 'practice' | 'quiz' | 'test' | 'challenge';
  courseId?: string;
  competencyId?: string | null;
  unitIndex?: number | null;
  initialSnapshot?: ActiveSessionSnapshot | null;
}

interface QuestionResult {
  questionId: string;
  isCorrect: boolean;
  skipped: boolean;
}

const isTypingTarget = (t: EventTarget | null): boolean => {
  const el = t as HTMLElement | null;
  return (
    !!el &&
    (el.tagName === 'INPUT' ||
      el.tagName === 'TEXTAREA' ||
      el.tagName === 'SELECT' ||
      el.isContentEditable)
  );
};

export const PracticeSession: React.FC<PracticeSessionProps> = ({
  sessionTitle,
  questions,
  onComplete,
  onQuit,
  onRestart,
  sessionType,
  courseId,
  competencyId,
  unitIndex,
  initialSnapshot,
}) => {
  const [currentIndex, setCurrentIndex] = useState(() => initialSnapshot?.currentIndex ?? 0);
  const [selectedOption, setSelectedOption] = useState<string | null>(() => initialSnapshot?.selectedOption ?? null);
  const [selectedMultiOptions, setSelectedMultiOptions] = useState<string[]>(() => initialSnapshot?.selectedMultiOptions ?? []);
  const [fillBlankValue, setFillBlankValue] = useState<string>(() => initialSnapshot?.fillBlankValue ?? '');
  const [structuredAnswer, setStructuredAnswer] = useState<StructuredUserAnswer | null>(
    () =>
      initialSnapshot?.structuredAnswer ??
      createInitialStructuredAnswer(questions[initialSnapshot?.currentIndex ?? 0])
  );
  const [matchedDiagnosticRationale, setMatchedDiagnosticRationale] = useState<string | null>(
    () => initialSnapshot?.matchedDiagnosticRationale ?? null
  );
  const [stage0Phase, setStage0Phase] = useState<1 | 2 | 3>(
    () => initialSnapshot?.stage0Phase ?? 1
  );
  const [stage0PhaseNotice, setStage0PhaseNotice] = useState<string | null>(null);
  const [canvasInteracted, setCanvasInteracted] = useState<boolean>(
    () => initialSnapshot?.canvasInteracted ?? false
  );
  const [hintsRevealed, setHintsRevealed] = useState(() => initialSnapshot?.hintsRevealed ?? 0);

  const [wrongAttemptsCount, setWrongAttemptsCount] = useState<number>(() => initialSnapshot?.wrongAttemptsCount ?? 0);
  const [isExhausted, setIsExhausted] = useState<boolean>(() => initialSnapshot?.isExhausted ?? false);

  // Milestone 6: Blank-First Curtain and Socratic Transfer (enabled for Practice, Quizzes, Unit Tests, and Challenges)
  const [blankFirstEnabled, setBlankFirstEnabled] = useState<boolean>(() => {
    try {
      return sessionStorage.getItem('tops_blank_first_enabled') !== 'false';
    } catch {
      return true;
    }
  });
  const [isCurtainLifted, setIsCurtainLifted] = useState<boolean>(() => initialSnapshot?.isCurtainLifted ?? false);
  const [scratchpadOpen, setScratchpadOpen] = useState<boolean>(false);
  const [scratchpadBgMode, setScratchpadBgMode] = useState<ScratchBgMode>('transparent');

  const handleToggleBlankFirst = () => {
    setBlankFirstEnabled((prev) => {
      const nextVal = !prev;
      try {
        sessionStorage.setItem('tops_blank_first_enabled', String(nextVal));
      } catch {}
      return nextVal;
    });
  };

  const [isChecked, setIsChecked] = useState(() => initialSnapshot?.isChecked ?? false);
  const [isCorrect, setIsCorrect] = useState<boolean | null>(() => initialSnapshot ? initialSnapshot.isCorrect : null);
  const [results, setResults] = useState<QuestionResult[]>(() => initialSnapshot?.results ?? []);
  const autoAdvanceTimerRef = useRef<NodeJS.Timeout | null>(null);
  const mainRef = useRef<HTMLElement | null>(null);
  const questionStartTimeRef = useRef<number>(Date.now());
  const telemetryRef = useRef<QuestionTelemetry[]>(initialSnapshot?.telemetry ? [...initialSnapshot.telemetry] : []);
  const isInitialHydrationRef = useRef<boolean>(!!initialSnapshot);

  const resetScroll = () => {
    window.scrollTo(0, 0);
    document.documentElement.scrollTop = 0;
    document.body.scrollTop = 0;
    if (mainRef.current) {
      mainRef.current.scrollTop = 0;
    }
  };

  useEffect(() => {
    resetScroll();
    if (isInitialHydrationRef.current) {
      isInitialHydrationRef.current = false;
      return;
    }
    setIsCurtainLifted(false);
    setCanvasInteracted(false);
    questionStartTimeRef.current = Date.now();
  }, [currentIndex]);

  // Milestone 12: Reactive session snapshot persistence
  useEffect(() => {
    if (!courseId || questions.length === 0) return;
    const currentQ = questions[currentIndex];
    if (!currentQ) return;

    saveActiveSession({
      version: 1,
      courseId,
      sessionType: sessionType || 'practice',
      competencyId: competencyId ?? null,
      unitIndex: unitIndex ?? null,
      sessionTitle,
      questions,
      currentIndex,
      selectedOption,
      selectedMultiOptions,
      fillBlankValue,
      structuredAnswer,
      matchedDiagnosticRationale,
      stage0Phase,
      hintsRevealed,
      wrongAttemptsCount,
      isExhausted,
      isChecked,
      isCorrect,
      isCurtainLifted,
      canvasInteracted,
      results,
      telemetry: telemetryRef.current,
      elapsedSeconds: Math.max(1, Math.round((Date.now() - questionStartTimeRef.current) / 1000)),
      savedAt: Date.now(),
    });
  }, [
    courseId,
    competencyId,
    unitIndex,
    sessionType,
    sessionTitle,
    questions,
    currentIndex,
    selectedOption,
    selectedMultiOptions,
    fillBlankValue,
    structuredAnswer,
    matchedDiagnosticRationale,
    stage0Phase,
    hintsRevealed,
    wrongAttemptsCount,
    isExhausted,
    isChecked,
    isCorrect,
    isCurtainLifted,
    canvasInteracted,
    results,
  ]);

  const clearAutoAdvanceTimer = () => {
    if (autoAdvanceTimerRef.current) {
      clearTimeout(autoAdvanceTimerRef.current);
      autoAdvanceTimerRef.current = null;
    }
  };

  const currentQuestion = questions[currentIndex];
  const total = questions.length;

  if (!currentQuestion || total === 0) {
    return (
      <div
        className="h-dvh-safe h-screen h-dvh bg-slate-50 flex flex-col items-center justify-center p-6 text-center w-full overflow-hidden"
        style={{ height: '100dvh', maxHeight: '100dvh' }}
      >
        <div className="w-16 h-16 bg-amber-100 text-amber-700 rounded-full flex items-center justify-center text-2xl mb-4 shadow-sm">
          ⚠️
        </div>
        <h2 className="text-xl font-bold text-ka-text-primary">
          No questions available
        </h2>
        <p className="text-sm text-ka-text-secondary mt-2 max-w-md">
          There are currently no questions registered for this competency.
        </p>
        <button
          onClick={onQuit}
          className="mt-6 px-6 py-2.5 bg-ka-blue hover:bg-ka-blue-hover text-white text-sm font-bold rounded shadow-md transition-colors cursor-pointer"
        >
          Back to Course Overview
        </button>
      </div>
    );
  }

  const effectiveCurtainActive =
    blankFirstEnabled && !isCurtainLifted && requiresBlankFirstCurtain(currentQuestion);

  // Determine if student has input an answer to enable Check button
  const hasAnswer = (() => {
    switch (currentQuestion.type) {
      case 'multiple_choice_7_options':
        return selectedOption !== null;
      case 'multiple_select':
        return selectedMultiOptions.length > 0;
      case 'fill_in_the_blank':
        return fillBlankValue.trim().length > 0;
      case 'open_symbolic':
        return (
          structuredAnswer?.kind === 'open_symbolic' &&
          structuredAnswer.expression.trim().length > 0
        );
      case 'proof_dag':
        return (
          structuredAnswer?.kind === 'proof_dag' &&
          structuredAnswer.orderedStepIds.length > 0 &&
          (!currentQuestion.proof_dag?.require_justification ||
            structuredAnswer.orderedStepIds.every(
              (sid) => Boolean(structuredAnswer.justifications[sid])
            ))
        );
      case 'adversarial_break': {
        if (structuredAnswer?.kind !== 'adversarial_break') return false;
        const spec = currentQuestion.adversarial_break;
        if (!spec) return false;
        if (spec.mode === 'find_fallacy') {
          const hasStep = structuredAnswer.selectedStepId !== null;
          const needsReason = (spec.reason_options || []).length > 0;
          return hasStep && (!needsReason || structuredAnswer.selectedReasonId !== null);
        }
        return (spec.inputs || []).every((inp) => {
          const iid = inp.id || inp.name || '';
          return Boolean((structuredAnswer.witnessValues[iid] || '').trim());
        });
      }
      case 'unstructured_model': {
        if (structuredAnswer?.kind !== 'unstructured_model') return false;
        const spec = currentQuestion.unstructured_model;
        if (!spec) return false;
        if (stage0Phase === 1) {
          return spec.phase1_variables.items.every(
            (it) => Boolean(structuredAnswer.phase1Roles[it.id])
          );
        }
        if (stage0Phase === 2) {
          return structuredAnswer.phase2SelectedIds.length > 0;
        }
        return spec.phase3_formulation.input_mode === 'select'
          ? structuredAnswer.phase3SelectedId !== null
          : structuredAnswer.phase3Expression.trim().length > 0;
      }
      case 'invariant_canvas':
        return structuredAnswer?.kind === 'invariant_canvas' && canvasInteracted;
      case 'concept_matching': {
        if (structuredAnswer?.kind !== 'concept_matching') return false;
        const premises = currentQuestion.concept_matching?.premises || [];
        return (
          premises.length > 0 &&
          premises.every((pr) => Boolean(structuredAnswer.pairs[pr.id]))
        );
      }
      default:
        return false;
    }
  })();

  const handleChangeStructuredAnswer = (next: StructuredUserAnswer) => {
    if (isExhausted || (isChecked && isCorrect === true)) return;
    if (next.kind === 'invariant_canvas') {
      setCanvasInteracted(true);
    }
    setStructuredAnswer(next);
    setStage0PhaseNotice(null);
    if (isChecked && !isCorrect) {
      setIsChecked(false);
      setIsCorrect(null);
      setMatchedDiagnosticRationale(null);
    }
  };

  const handleSelectOption = (id: string) => {
    if (isExhausted || (isChecked && isCorrect === true)) return;
    if (isChecked && !isCorrect) {
      setIsChecked(false);
      setIsCorrect(null);
    }
    setSelectedOption((prev) => (prev === id ? null : id));
  };

  const handleToggleMultiOption = (id: string) => {
    if (isExhausted || (isChecked && isCorrect === true)) return;
    if (isChecked && !isCorrect) {
      setIsChecked(false);
      setIsCorrect(null);
    }
    if (selectedMultiOptions.includes(id)) {
      setSelectedMultiOptions(selectedMultiOptions.filter((item) => item !== id));
    } else {
      setSelectedMultiOptions([...selectedMultiOptions, id]);
    }
  };

  const handleChangeFillBlank = (val: string) => {
    if (isExhausted || (isChecked && isCorrect === true)) return;
    setFillBlankValue(val);
    if (isChecked && !isCorrect) {
      setIsChecked(false);
      setIsCorrect(null);
    }
  };

  const handleCheck = (autoAdvance: boolean = false) => {
    if (!hasAnswer || isChecked || isExhausted) return;

    let correct = false;
    let diagRationale: string | null = null;
    setStage0PhaseNotice(null);

    if (currentQuestion.type === 'multiple_choice_7_options') {
      correct = selectedOption !== null && isOptionCorrect(currentQuestion, selectedOption);
    } else if (currentQuestion.type === 'multiple_select') {
      // Strictly all-or-nothing grading using canonical correct IDs
      const correctIds = getCorrectOptionIds(currentQuestion).sort();
      const sSorted = [...selectedMultiOptions].sort();

      correct =
        sSorted.length === correctIds.length &&
        sSorted.every((val, idx) => val === correctIds[idx]);
    } else if (currentQuestion.type === 'fill_in_the_blank') {
      correct = checkMathEquivalence(fillBlankValue, currentQuestion.correct_answer as any);
      if (!correct && currentQuestion.diagnostic_distractors?.length) {
        const res = validateSymbolicAnswer(
          fillBlankValue,
          currentQuestion.correct_answer,
          currentQuestion.diagnostic_distractors,
          currentQuestion.symbolic_config
        );
        diagRationale = res.diagnosticRationale || null;
      }
    } else if (currentQuestion.type === 'open_symbolic') {
      const expr = structuredAnswer?.kind === 'open_symbolic' ? structuredAnswer.expression : '';
      const res = validateSymbolicAnswer(
        expr,
        currentQuestion.correct_answer,
        currentQuestion.diagnostic_distractors,
        currentQuestion.symbolic_config
      );
      correct = res.isCorrect;
      diagRationale = res.diagnosticRationale || res.syntaxError || null;
    } else if (currentQuestion.type === 'proof_dag' && currentQuestion.proof_dag) {
      const sVal =
        structuredAnswer?.kind === 'proof_dag'
          ? structuredAnswer
          : { orderedStepIds: [], justifications: {} };
      const res = validateProofDagSubmission(
        sVal.orderedStepIds,
        sVal.justifications,
        currentQuestion.proof_dag
      );
      correct = res.isCorrect;
      diagRationale = res.diagnosticRationale || null;
    } else if (
      currentQuestion.type === 'adversarial_break' &&
      currentQuestion.adversarial_break
    ) {
      const aVal =
        structuredAnswer?.kind === 'adversarial_break'
          ? structuredAnswer
          : { selectedStepId: null, selectedReasonId: null, witnessValues: {} };
      const res = validateAdversarialSubmission(aVal, currentQuestion.adversarial_break);
      correct = res.isCorrect;
      diagRationale = res.diagnosticRationale || null;
    } else if (
      currentQuestion.type === 'unstructured_model' &&
      currentQuestion.unstructured_model
    ) {
      const uVal =
        structuredAnswer?.kind === 'unstructured_model'
          ? structuredAnswer
          : {
              phase1Roles: {},
              phase2SelectedIds: [],
              phase3SelectedId: null,
              phase3Expression: '',
            };
      const res = validateStage0Phase(stage0Phase, uVal, currentQuestion.unstructured_model);
      if (res.isCorrect && stage0Phase < 3) {
        const nextPhase = (stage0Phase + 1) as 1 | 2 | 3;
        setStage0Phase(nextPhase);
        setStage0PhaseNotice(`✓ Fase ${stage0Phase} completada — Fase ${nextPhase} desbloqueada`);
        setMatchedDiagnosticRationale(null);
        setIsChecked(false);
        setIsCorrect(null);
        return;
      }
      correct = res.isCorrect;
      diagRationale = res.diagnosticRationale || null;
    } else if (
      currentQuestion.type === 'invariant_canvas' &&
      currentQuestion.invariant_canvas
    ) {
      const cVal =
        structuredAnswer?.kind === 'invariant_canvas'
          ? structuredAnswer
          : {
              sliderValues: {},
              pointPositions: {},
              selectedEdgeIds: [],
              infoSets: [],
              inequalityStyle: currentQuestion.invariant_canvas.inequality?.initial_style ?? 'solid',
              inequalityShade: currentQuestion.invariant_canvas.inequality?.initial_shade ?? 'above',
            };
      const res =
        currentQuestion.invariant_canvas.mode === 'tree'
          ? validateTreeInvariants(
              { selectedEdgeIds: cVal.selectedEdgeIds, infoSets: cVal.infoSets },
              currentQuestion.invariant_canvas
            )
          : validateCartesianInvariants(
              {
                sliderValues: cVal.sliderValues,
                pointPositions: cVal.pointPositions,
                inequalityStyle: cVal.inequalityStyle,
                inequalityShade: cVal.inequalityShade,
              },
              currentQuestion.invariant_canvas
            );
      correct = res.isCorrect;
      diagRationale = res.diagnosticRationale || null;
    } else if (currentQuestion.type === 'concept_matching' && currentQuestion.concept_matching) {
      const pVal = structuredAnswer?.kind === 'concept_matching' ? structuredAnswer.pairs : {};
      const res = validateConceptMatchingSubmission(pVal, currentQuestion.concept_matching);
      correct = res.isCorrect;
      diagRationale = res.diagnosticRationale || null;
    }

    setMatchedDiagnosticRationale(diagRationale);
    setIsChecked(true);
    setIsCorrect(correct);

    if (correct) {
      // Confetti burst on correct answer!
      try {
        confetti({
          particleCount: 25,
          spread: 40,
          origin: { x: 0.85, y: 0.85 },
        });
      } catch {}

      if (autoAdvance) {
        clearAutoAdvanceTimer();
        autoAdvanceTimerRef.current = setTimeout(() => {
          handleNext(true);
        }, 900);
      }
    } else {
      const nextWrongCount = wrongAttemptsCount + 1;
      setWrongAttemptsCount(nextWrongCount);

      if (nextWrongCount >= 4) {
        setIsExhausted(true);
        // Register question as failed (isCorrect: false, skipped: false)
        setResults((prev) => {
          const existingIdx = prev.findIndex((r) => r.questionId === currentQuestion.id);
          if (existingIdx >= 0) {
            const updated = [...prev];
            updated[existingIdx] = {
              questionId: currentQuestion.id,
              isCorrect: false,
              skipped: false,
            };
            return updated;
          }
          return [
            ...prev,
            {
              questionId: currentQuestion.id,
              isCorrect: false,
              skipped: false,
            },
          ];
        });
      }
    }
  };

  const handleRedo = () => {
    if (isExhausted) return;
    clearAutoAdvanceTimer();
    setSelectedOption(null);
    setSelectedMultiOptions([]);
    setFillBlankValue('');
    setMatchedDiagnosticRationale(null);
    setStage0PhaseNotice(null);
    if (currentQuestion.type !== 'unstructured_model') {
      setStructuredAnswer(createInitialStructuredAnswer(currentQuestion));
    }
    setCanvasInteracted(false);
    setIsChecked(false);
    setIsCorrect(null);
    resetScroll();
  };

  const handleRetry = () => {
    if (isExhausted) return;
    clearAutoAdvanceTimer();
    setIsChecked(false);
    setIsCorrect(null);
    setMatchedDiagnosticRationale(null);
    if (currentQuestion.type === 'multiple_choice_7_options') {
      setSelectedOption(null);
    }
    resetScroll();
  };

  const handleNext = (overrideIsCorrect?: boolean) => {
    clearAutoAdvanceTimer();
    resetScroll();
    const correctVal = overrideIsCorrect !== undefined ? overrideIsCorrect : isCorrect === true;
    const now = Date.now();
    const elapsedMs = now - questionStartTimeRef.current;
    const spentSeconds = Math.min(300, Math.max(1, Math.round(elapsedMs / 1000)));

    const qTelemetry: QuestionTelemetry = {
      question_id: currentQuestion.id,
      competency_id: currentQuestion.competency_id,
      is_correct: correctVal,
      hints_used: hintsRevealed,
      seconds_spent: spentSeconds,
      question_text: currentQuestion.stem,
    };

    const existingTelIdx = telemetryRef.current.findIndex((t) => t.question_id === currentQuestion.id);
    if (existingTelIdx >= 0) {
      telemetryRef.current[existingTelIdx] = qTelemetry;
    } else {
      telemetryRef.current.push(qTelemetry);
    }

    let newResults = results;
    const existingIdx = results.findIndex((r) => r.questionId === currentQuestion.id);
    if (existingIdx >= 0) {
      newResults = [...results];
      newResults[existingIdx] = {
        questionId: currentQuestion.id,
        isCorrect: correctVal,
        skipped: false,
      };
    } else {
      newResults = [
        ...results,
        {
          questionId: currentQuestion.id,
          isCorrect: correctVal,
          skipped: false,
        },
      ];
    }
    setResults(newResults);

    if (currentIndex + 1 >= total) {
      clearActiveSession();
      const finalScore = newResults.filter((r) => r.isCorrect).length;
      const totalSessionSeconds = telemetryRef.current.reduce((acc, t) => acc + t.seconds_spent, 0);
      onComplete(finalScore, total, [...telemetryRef.current], totalSessionSeconds);
    } else {
      const nextQ = questions[currentIndex + 1];
      setCurrentIndex((prev) => prev + 1);
      setSelectedOption(null);
      setSelectedMultiOptions([]);
      setFillBlankValue('');
      setStructuredAnswer(createInitialStructuredAnswer(nextQ));
      setMatchedDiagnosticRationale(null);
      setStage0Phase(1);
      setStage0PhaseNotice(null);
      setHintsRevealed(0);
      setIsChecked(false);
      setIsCorrect(null);
      setWrongAttemptsCount(0);
      setIsExhausted(false);
      setIsCurtainLifted(false);
      setCanvasInteracted(false);
    }
  };

  const handleSkip = () => {
    clearAutoAdvanceTimer();
    resetScroll();

    const now = Date.now();
    const elapsedMs = now - questionStartTimeRef.current;
    const spentSeconds = Math.min(300, Math.max(1, Math.round(elapsedMs / 1000)));

    const qTelemetry: QuestionTelemetry = {
      question_id: currentQuestion.id,
      competency_id: currentQuestion.competency_id,
      is_correct: false,
      hints_used: hintsRevealed,
      seconds_spent: spentSeconds,
      question_text: currentQuestion.stem,
    };

    const existingTelIdx = telemetryRef.current.findIndex((t) => t.question_id === currentQuestion.id);
    if (existingTelIdx >= 0) {
      telemetryRef.current[existingTelIdx] = qTelemetry;
    } else {
      telemetryRef.current.push(qTelemetry);
    }

    const newResults = [
      ...results,
      {
        questionId: currentQuestion.id,
        isCorrect: false,
        skipped: true,
      },
    ];
    setResults(newResults);

    if (currentIndex + 1 >= total) {
      clearActiveSession();
      const finalScore = newResults.filter((r) => r.isCorrect).length;
      const totalSessionSeconds = telemetryRef.current.reduce((acc, t) => acc + t.seconds_spent, 0);
      onComplete(finalScore, total, [...telemetryRef.current], totalSessionSeconds);
    } else {
      const nextQ = questions[currentIndex + 1];
      setCurrentIndex((prev) => prev + 1);
      setSelectedOption(null);
      setSelectedMultiOptions([]);
      setFillBlankValue('');
      setStructuredAnswer(createInitialStructuredAnswer(nextQ));
      setMatchedDiagnosticRationale(null);
      setStage0Phase(1);
      setStage0PhaseNotice(null);
      setHintsRevealed(0);
      setIsChecked(false);
      setIsCorrect(null);
      setWrongAttemptsCount(0);
      setIsExhausted(false);
      setIsCurtainLifted(false);
      setCanvasInteracted(false);
    }
  };

  // Keyboard navigation: Enter checks answer, advances if correct, or allows retry
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.isComposing) return;

      const typing = isTypingTarget(e.target);

      if (
        !typing &&
        !e.altKey &&
        !e.ctrlKey &&
        !e.metaKey &&
        e.key.toLowerCase() === 'p'
      ) {
        e.preventDefault();
        setScratchpadOpen((prev) => !prev);
        return;
      }

      if (
        (e.key === 's' || e.key === 'S') &&
        !e.altKey &&
        (e.ctrlKey || e.metaKey)
      ) {
        e.preventDefault();
        if (!(isChecked && isCorrect === true) && !isExhausted) {
          handleSkip();
        }
        return;
      }

      if (e.key === 'Enter') {
        if (scratchpadOpen) return;
        const targetEl = e.target as HTMLElement | null;
        if (targetEl?.tagName === 'SELECT') return;
        e.preventDefault();

        // Milestone 6 / 20: If Smart Blank-First curtain is active, Enter lifts the curtain
        if (effectiveCurtainActive) {
          setIsCurtainLifted(true);
          return;
        }

        if (isExhausted) {
          clearAutoAdvanceTimer();
          handleNext(false);
        } else if (!isChecked) {
          if (hasAnswer) {
            handleCheck(true);
          }
        } else if (isCorrect === true) {
          clearAutoAdvanceTimer();
          handleNext(true);
        } else if (isCorrect === false) {
          clearAutoAdvanceTimer();
          handleRetry();
        }
        return;
      }

      // Mouseless hotkeys for option selection (A-I and 1-9)
      if (!typing && !scratchpadOpen && !e.altKey && !e.ctrlKey && !e.metaKey && !isChecked && !effectiveCurtainActive) {
        const OPTION_KEYS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'];
        const NUMBER_KEYS = ['1', '2', '3', '4', '5', '6', '7', '8', '9'];

        const keyLower = e.key.toLowerCase();
        let optIdx = OPTION_KEYS.indexOf(keyLower);
        if (optIdx === -1) {
          optIdx = NUMBER_KEYS.indexOf(keyLower);
        }

        if (optIdx !== -1 && currentQuestion.options && optIdx < currentQuestion.options.length) {
          const targetOpt = currentQuestion.options[optIdx];
          if (currentQuestion.type === 'multiple_choice_7_options') {
            e.preventDefault();
            handleSelectOption(targetOpt.id);
            return;
          } else if (currentQuestion.type === 'multiple_select') {
            e.preventDefault();
            handleToggleMultiOption(targetOpt.id);
            return;
          }
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      clearAutoAdvanceTimer();
    };
  }, [
    isChecked,
    isCorrect,
    hasAnswer,
    currentQuestion,
    selectedOption,
    selectedMultiOptions,
    fillBlankValue,
    results,
    currentIndex,
    total,
    isExhausted,
    wrongAttemptsCount,
    blankFirstEnabled,
    isCurtainLifted,
    scratchpadOpen,
  ]);

  return (
    <div
      data-testid="practice-session"
      className="h-screen h-dvh h-dvh-safe bg-white flex flex-col overflow-hidden w-full relative"
      style={{ height: '100dvh', maxHeight: '100dvh' }}
    >
      {/* Top Header */}
      <header className="h-16 [@media(max-height:850px)]:h-12 border-b border-ka-border-subtle px-4 sm:px-6 flex items-center justify-between shrink-0">
        <button
          onClick={() => {
            clearAutoAdvanceTimer();
            clearActiveSession();
            setScratchpadOpen(false);
            onQuit();
          }}
          className="w-8 h-8 sm:w-9 sm:h-9 rounded-full hover:bg-slate-100 flex items-center justify-center text-ka-text-secondary text-base transition-colors shrink-0"
          title="Quit practice"
          aria-label="Quit practice"
        >
          <span aria-hidden="true">✕</span>
        </button>
        <div className="text-sm font-bold text-ka-text-primary text-center truncate px-2 min-w-0">
          <MathText text={sessionTitle} inline />
        </div>
        <div className="flex items-center gap-2 shrink-0">
          <button
            type="button"
            data-testid="toggle-scratchpad-btn"
            onClick={() => setScratchpadOpen((prev) => !prev)}
            aria-pressed={scratchpadOpen}
            title="Activar pizarra de apuntes (P)"
            className={`text-xs font-semibold px-2 sm:px-2.5 py-1 sm:py-1.5 rounded-lg border transition-all flex items-center gap-1 cursor-pointer ${
              scratchpadOpen
                ? 'bg-emerald-50 border-emerald-400 text-emerald-800 hover:bg-emerald-100 shadow-xs'
                : 'bg-slate-50 border-slate-200 text-slate-600 hover:bg-slate-100'
            }`}
          >
            <span aria-hidden="true">✏️</span>
            <span className="hidden sm:inline text-[11px]">
              {scratchpadOpen ? 'Pizarra: ON' : 'Pizarra'}
            </span>
          </button>

          <button
            type="button"
            data-testid="toggle-blank-first-btn"
            onClick={handleToggleBlankFirst}
            aria-pressed={blankFirstEnabled}
            title={
              blankFirstEnabled
                ? 'Modo Blank-First activo: oculta las opciones hasta que formulas tu respuesta (clic para desactivar)'
                : 'Modo Blank-First desactivado (clic para activar)'
            }
            className={`text-xs font-semibold px-2 sm:px-2.5 py-1 sm:py-1.5 rounded-lg border transition-all flex items-center gap-1 cursor-pointer ${
              blankFirstEnabled
                ? 'bg-blue-50 border-blue-300 text-ka-blue hover:bg-blue-100'
                : 'bg-slate-50 border-slate-200 text-slate-500 hover:bg-slate-100'
            }`}
          >
            <span aria-hidden="true">🧠</span>
            <span className="hidden sm:inline text-[11px]">
              {blankFirstEnabled ? 'Blank-First: ON' : 'Blank-First: OFF'}
            </span>
          </button>

          {onRestart ? (
            <button
              onClick={() => {
                clearAutoAdvanceTimer();
                clearActiveSession();
                setScratchpadOpen(false);
                resetScroll();
                onRestart();
              }}
              data-testid="restart-session-btn"
              className="text-xs font-semibold text-ka-blue hover:text-ka-blue-hover flex items-center gap-1.5 transition-colors px-2.5 sm:px-3 py-1 sm:py-1.5 rounded-lg border border-slate-200 hover:bg-slate-50 shadow-sm cursor-pointer shrink-0"
              title="Restart session with new shuffled questions"
              aria-label="Restart practice session"
            >
              <span aria-hidden="true">🔄</span>
              <span className="hidden sm:inline">Restart</span>
            </button>
          ) : (
            <div className="w-2 sm:w-3 shrink-0" />
          )}
        </div>
      </header>

      {/* Main Question Surface + Khan Academy Scratchpad Workspace */}
      <div
        data-testid="practice-workspace"
        className="flex-1 min-h-0 relative flex flex-col overflow-hidden transition-[background] duration-150"
        style={scratchpadOpen && scratchpadBgMode === 'grid' ? SCRATCHPAD_GRID_BG_STYLE : undefined}
      >
        <main
          ref={mainRef}
          className={`flex-1 min-h-0 overflow-y-auto overflow-x-hidden ${
            scratchpadOpen ? 'pb-24' : ''
          }`}
        >
          <QuestionCard
            question={currentQuestion}
            selectedOption={selectedOption}
            selectedMultiOptions={selectedMultiOptions}
            fillBlankValue={fillBlankValue}
            structuredAnswer={structuredAnswer}
            matchedDiagnosticRationale={matchedDiagnosticRationale}
            stage0Phase={stage0Phase}
            stage0PhaseNotice={stage0PhaseNotice}
            isChecked={isChecked}
            isCorrect={isCorrect}
            isExhausted={isExhausted}
            onSelectOption={handleSelectOption}
            onToggleMultiOption={handleToggleMultiOption}
            onChangeFillBlank={handleChangeFillBlank}
            onChangeStructuredAnswer={handleChangeStructuredAnswer}
            hintsRevealed={hintsRevealed}
            onRevealHint={() => setHintsRevealed((prev) => prev + 1)}
            blankFirstEnabled={blankFirstEnabled}
            isCurtainLifted={isCurtainLifted}
            onLiftCurtain={() => setIsCurtainLifted(true)}
            courseTitle={sessionTitle}
            wrongAttemptsCount={wrongAttemptsCount}
            isPracticeMode={true}
          />
        </main>
        <ScratchpadOverlay
          isOpen={scratchpadOpen}
          questionId={currentQuestion.id}
          bgMode={scratchpadBgMode}
          onChangeBgMode={setScratchpadBgMode}
          onClose={() => setScratchpadOpen(false)}
        />
      </div>

      {/* Floating Feedback Toast */}
      {isChecked && isCorrect !== null && (
        <FeedbackToast
          isCorrect={isCorrect}
          question={currentQuestion}
          selectedOption={selectedOption}
          selectedMultiOptions={selectedMultiOptions}
          matchedDiagnosticRationale={matchedDiagnosticRationale}
          onRedo={handleRedo}
          isExhausted={isExhausted}
          wrongAttemptsCount={wrongAttemptsCount}
        />
      )}

      {/* Bottom Action & Progress Bar (in normal flex flow) */}
      <footer className="h-14 sm:h-16 [@media(max-height:850px)]:h-12 bg-white border-t border-ka-border-card px-4 sm:px-8 flex items-center justify-between z-20 shadow-sm shrink-0">
        {/* Left Side: Counter & Progress Indicator Dots */}
        <div className="flex items-center gap-2 sm:gap-4 min-w-0">
          <span className="text-base sm:text-lg text-slate-400 shrink-0" aria-hidden="true">🔄</span>

          <span className="text-xs sm:text-sm font-bold text-ka-text-primary shrink-0 min-w-[60px] sm:min-w-[70px]">
            {currentIndex === 0 && !isChecked
              ? `Do ${total} problems`
              : `${currentIndex + 1} of ${total}`}
          </span>

          {/* Progress Indicator Dots */}
          <div
            className="hidden min-[520px]:flex [@media(min-width:520px)]:flex items-center gap-1.5 sm:gap-2 flex-wrap"
            role="status"
            aria-label={`Progress: question ${currentIndex + 1} of ${total}`}
          >
            {questions.map((_, idx) => {
              const res = results[idx];
              const isCurrent = idx === currentIndex;

              if (res) {
                if (res.isCorrect) {
                  return (
                    <div
                      key={idx}
                      aria-label={`Question ${idx + 1}: correct`}
                      className="w-4 h-4 rounded-full bg-ka-green-badge text-white flex items-center justify-center text-[10px] font-bold shrink-0"
                    >
                      <span aria-hidden="true">✓</span>
                    </div>
                  );
                } else {
                  return (
                    <div
                      key={idx}
                      aria-label={`Question ${idx + 1}: incorrect`}
                      className="w-3.5 h-3.5 rounded-full bg-red-500 flex items-center justify-center text-[9px] text-white font-bold shrink-0"
                    >
                      <span aria-hidden="true">✕</span>
                    </div>
                  );
                }
              }

              if (isCurrent && isChecked) {
                if (isCorrect) {
                  return (
                    <div
                      key={idx}
                      aria-label={`Question ${idx + 1}: correct`}
                      className="w-4 h-4 rounded-full bg-ka-green-badge text-white flex items-center justify-center text-[10px] font-bold shrink-0"
                    >
                      <span aria-hidden="true">✓</span>
                    </div>
                  );
                } else {
                  return (
                    <div
                      key={idx}
                      aria-label={`Question ${idx + 1}: incorrect`}
                      className="w-3.5 h-3.5 rounded-full bg-red-500 flex items-center justify-center text-[9px] text-white font-bold shrink-0"
                    >
                      <span aria-hidden="true">✕</span>
                    </div>
                  );
                }
              }

              return (
                <div
                  key={idx}
                  aria-label={
                    isCurrent
                      ? `Question ${idx + 1}: current`
                      : `Question ${idx + 1}: pending`
                  }
                  className={`w-3 h-3 rounded-full border-2 transition-all shrink-0 ${
                    isCurrent
                      ? 'border-slate-800 scale-125'
                      : 'border-slate-300'
                  }`}
                />
              );
            })}
          </div>
        </div>

        {/* Right Side: Skip & Check / Next Button */}
        <div className="flex items-center gap-2 sm:gap-4 shrink-0">
          <button
            data-testid="skip-btn"
            disabled={(isChecked && isCorrect === true) || isExhausted}
            onClick={handleSkip}
            aria-label="Skip question"
            title="Skip (Ctrl+S)"
            className={`text-sm font-semibold transition-colors px-1 sm:px-2 ${
              (isChecked && isCorrect === true) || isExhausted
                ? 'text-slate-300 cursor-not-allowed'
                : 'text-ka-blue hover:text-ka-blue-hover'
            }`}
          >
            Skip <kbd className="hidden sm:inline text-[10px] font-bold px-1 bg-slate-100 border border-slate-300 rounded text-slate-600">S</kbd>
          </button>

          {isExhausted ? (
            <button
              data-testid="next-question-btn"
              onClick={() => handleNext(false)}
              aria-label="Next question"
              className="px-4 sm:px-6 py-1.5 sm:py-2 [@media(min-height:851px)]:sm:py-2.5 bg-ka-blue hover:bg-ka-blue-hover text-white text-sm font-bold rounded shadow-md transition-colors flex items-center gap-2 cursor-pointer"
            >
              <span>Next question</span>
              <kbd className="hidden sm:inline-block px-1.5 py-0.5 text-[10px] bg-blue-700/60 text-white rounded font-mono border border-blue-400/30" aria-hidden="true">↵ Enter</kbd>
            </button>
          ) : isChecked && isCorrect ? (
            <button
              data-testid="next-question-btn"
              onClick={() => handleNext(true)}
              aria-label="Next question"
              className="px-4 sm:px-6 py-1.5 sm:py-2 [@media(min-height:851px)]:sm:py-2.5 bg-ka-blue hover:bg-ka-blue-hover text-white text-sm font-bold rounded shadow-md transition-colors flex items-center gap-2 cursor-pointer"
            >
              <span>Next question</span>
              <kbd className="hidden sm:inline-block px-1.5 py-0.5 text-[10px] bg-blue-700/60 text-white rounded font-mono border border-blue-400/30" aria-hidden="true">↵ Enter</kbd>
            </button>
          ) : isChecked && !isCorrect ? (
            <div className="flex items-center gap-2">
              <button
                data-testid="quick-redo-btn"
                onClick={handleRedo}
                aria-label="Quick redo: clear input and re-attempt question"
                className="px-3 sm:px-4 py-1.5 sm:py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs sm:text-sm font-bold rounded border border-slate-300 transition-colors flex items-center gap-1.5 cursor-pointer"
                title="Clear input and re-attempt question"
              >
                <span aria-hidden="true">↺</span>
                <span className="hidden min-[420px]:inline">Quick Redo</span>
              </button>
              <button
                data-testid="check-btn"
                onClick={handleRetry}
                aria-label="Try again"
                className="px-4 sm:px-6 py-1.5 sm:py-2 [@media(min-height:851px)]:sm:py-2.5 bg-ka-blue hover:bg-ka-blue-hover text-white text-sm font-bold rounded shadow-md transition-colors cursor-pointer flex items-center gap-2"
              >
                <span>Try again</span>
                <kbd className="hidden sm:inline-block px-1.5 py-0.5 text-[10px] bg-blue-700/60 text-white rounded font-mono border border-blue-400/30" aria-hidden="true">↵ Enter</kbd>
              </button>
            </div>
          ) : (
            <button
              data-testid="check-btn"
              disabled={effectiveCurtainActive ? false : !hasAnswer}
              onClick={() => {
                if (effectiveCurtainActive) {
                  setIsCurtainLifted(true);
                } else {
                  handleCheck(true);
                }
              }}
              aria-label={
                effectiveCurtainActive
                  ? 'Reveal options'
                  : currentQuestion.type === 'unstructured_model' && stage0Phase < 3
                  ? `Verify phase ${stage0Phase}`
                  : 'Check answer'
              }
              className={`px-4 sm:px-6 py-1.5 sm:py-2 [@media(min-height:851px)]:sm:py-2.5 text-sm font-bold rounded transition-colors flex items-center gap-2 ${
                effectiveCurtainActive || hasAnswer
                  ? 'bg-ka-blue hover:bg-ka-blue-hover text-white cursor-pointer shadow-md'
                  : 'bg-slate-300 text-white cursor-not-allowed'
              }`}
            >
              <span>
                {effectiveCurtainActive
                  ? 'Reveal options'
                  : currentQuestion.type === 'unstructured_model' && stage0Phase < 3
                  ? `Verify phase ${stage0Phase}`
                  : 'Check'}
              </span>
              {(effectiveCurtainActive || hasAnswer) && (
                <kbd className="hidden sm:inline-block px-1.5 py-0.5 text-[10px] bg-blue-700/60 text-white rounded font-mono border border-blue-400/30" aria-hidden="true">↵ Enter</kbd>
              )}
            </button>
          )}
        </div>
      </footer>
    </div>
  );
};
