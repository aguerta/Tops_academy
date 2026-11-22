import React, { useEffect, useMemo, useRef, useState } from 'react';
import {
  AdaptiveModuleTier,
  IronDeferredReviewItem,
  IronExamQuestionDraft,
  MetacognitiveAudit,
  MetacognitiveConfidence,
  Question,
  QuestionTelemetry,
  StructuredUserAnswer,
} from '../../types';
import { QuestionCard } from '../QuestionCard';
import { MathText } from '../MathText';
import {
  ScratchBgMode,
  SCRATCHPAD_GRID_BG_STYLE,
  ScratchpadOverlay,
} from '../ScratchpadOverlay';
import {
  ActiveSessionSnapshot,
  clearActiveSession,
  saveActiveSession,
} from '../../utils/sessionStore';
import {
  computeMetacognitiveAudit,
  createInitialIronDraft,
  isDraftAnswered,
} from '../../utils/ironExamGrading';
import { extractCarriedDistractorIds } from '../../utils/distractorExtractor';
import { MetacognitiveModal } from './MetacognitiveModal';

export interface IronExamCompletionOutcome {
  metacognitiveAudit: MetacognitiveAudit;
  deferredReview: IronDeferredReviewItem[];
}

interface PersistedIronExamState {
  drafts?: Record<string, IronExamQuestionDraft>;
  itemConfidences?: Record<string, MetacognitiveConfidence>;
  flaggedIds?: Record<string, boolean>;
  stage0Phases?: Record<string, 1 | 2 | 3>;
  globalConfidence?: MetacognitiveConfidence | null;
  elapsedSeconds?: number;
  timeLimitSeconds?: number;
}

interface IronExamSessionProps {
  sessionTitle: string;
  questions: Question[];
  courseId?: string;
  courseTitle?: string;
  timeLimitSeconds?: number;
  moduleIndex?: 1 | 2;
  moduleTier?: AdaptiveModuleTier;
  submitButtonLabel?: string;
  persistSession?: boolean;
  initialSnapshot?: ActiveSessionSnapshot | null;
  onComplete: (
    score: number,
    total: number,
    telemetry?: QuestionTelemetry[],
    totalSeconds?: number,
    ironOutcome?: IronExamCompletionOutcome
  ) => void;
  onQuit: () => void;
}

function formatClock(totalSeconds: number): string {
  const mins = Math.floor(totalSeconds / 60);
  const secs = totalSeconds % 60;
  return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

export const IronExamSession: React.FC<IronExamSessionProps> = ({
  sessionTitle,
  questions,
  courseId,
  courseTitle,
  timeLimitSeconds,
  moduleIndex,
  moduleTier,
  submitButtonLabel,
  persistSession = true,
  initialSnapshot,
  onComplete,
  onQuit,
}) => {
  const restoredIron = (initialSnapshot?.ironExamState || {}) as PersistedIronExamState;

  const [currentIndex, setCurrentIndex] = useState<number>(
    () => Math.min(Math.max(0, initialSnapshot?.currentIndex ?? 0), Math.max(0, questions.length - 1))
  );
  const [drafts, setDrafts] = useState<Record<string, IronExamQuestionDraft>>(() => {
    const base: Record<string, IronExamQuestionDraft> = {};
    for (const q of questions) {
      base[q.id] = restoredIron.drafts?.[q.id] || createInitialIronDraft(q);
    }
    return base;
  });
  const [itemConfidences, setItemConfidences] = useState<Record<string, MetacognitiveConfidence>>(
    () => restoredIron.itemConfidences || {}
  );
  const [flaggedIds, setFlaggedIds] = useState<Record<string, boolean>>(
    () => restoredIron.flaggedIds || {}
  );
  const [stage0Phases, setStage0Phases] = useState<Record<string, 1 | 2 | 3>>(
    () => restoredIron.stage0Phases || {}
  );
  const [globalConfidence, setGlobalConfidence] = useState<MetacognitiveConfidence | null>(
    () => restoredIron.globalConfidence ?? null
  );
  const effectiveTimeLimit = useMemo(() => {
    const candidate =
      typeof restoredIron.timeLimitSeconds === 'number' && restoredIron.timeLimitSeconds > 0
        ? restoredIron.timeLimitSeconds
        : typeof timeLimitSeconds === 'number' && timeLimitSeconds > 0
        ? timeLimitSeconds
        : null;
    return candidate ?? Math.max(180, questions.length * 120);
  }, [restoredIron.timeLimitSeconds, timeLimitSeconds, questions.length]);
  const [elapsedSeconds, setElapsedSeconds] = useState<number>(() => {
    const baseElapsed = Math.max(
      0,
      restoredIron.elapsedSeconds ?? initialSnapshot?.elapsedSeconds ?? 0
    );
    const savedAt = initialSnapshot?.savedAt;
    const offlineDelta =
      typeof savedAt === 'number' && savedAt > 0
        ? Math.max(0, Math.floor((Date.now() - savedAt) / 1000))
        : 0;
    const combined = baseElapsed + offlineDelta;
    return effectiveTimeLimit > 0 ? Math.min(effectiveTimeLimit, combined) : combined;
  });
  const [showMetaModal, setShowMetaModal] = useState(false);
  const [scratchpadOpen, setScratchpadOpen] = useState(false);
  const [scratchpadBgMode, setScratchpadBgMode] = useState<ScratchBgMode>('transparent');

  const remainingSeconds = Math.max(0, effectiveTimeLimit - elapsedSeconds);
  const isTimeExpired = effectiveTimeLimit > 0 && remainingSeconds === 0;

  const examStartWallMsRef = useRef<number | null>(null);
  if (examStartWallMsRef.current === null) {
    examStartWallMsRef.current = Date.now() - elapsedSeconds * 1000;
  }
  const questionEnterTimeRef = useRef<number>(Date.now());
  const spentByQidRef = useRef<Record<string, number>>({});
  const mainRef = useRef<HTMLElement | null>(null);

  const total = questions.length;
  const currentQuestion = questions[currentIndex];
  const currentDraft = currentQuestion
    ? drafts[currentQuestion.id] || createInitialIronDraft(currentQuestion)
    : createInitialIronDraft({
        id: 'empty',
        competency_id: '',
        type: 'multiple_choice_7_options',
        stem: '',
        options: [],
        correct_answer: '',
        hints: [],
        solution: '',
      });

  const answeredMap = useMemo(() => {
    const map: Record<string, boolean> = {};
    for (const q of questions) {
      const d = drafts[q.id] || createInitialIronDraft(q);
      map[q.id] = isDraftAnswered(q, d);
    }
    return map;
  }, [questions, drafts]);

  const answeredCount = useMemo(
    () => questions.filter((q) => answeredMap[q.id]).length,
    [questions, answeredMap]
  );

  // Countdown timer tick (wall-clock anchored); halts once time expires or with 0 questions
  useEffect(() => {
    if (isTimeExpired || questions.length === 0) return;
    const updateElapsed = () => {
      const startMs = examStartWallMsRef.current ?? Date.now();
      const wallElapsed = Math.max(0, Math.floor((Date.now() - startMs) / 1000));
      setElapsedSeconds(
        effectiveTimeLimit > 0 ? Math.min(effectiveTimeLimit, wallElapsed) : wallElapsed
      );
    };
    const id = window.setInterval(updateElapsed, 1000);
    document.addEventListener('visibilitychange', updateElapsed);
    return () => {
      window.clearInterval(id);
      document.removeEventListener('visibilitychange', updateElapsed);
    };
  }, [isTimeExpired, effectiveTimeLimit, questions.length]);

  // Auto-open mandatory metacognitive modal when exam time expires
  useEffect(() => {
    if (isTimeExpired && questions.length > 0) {
      setShowMetaModal(true);
    }
  }, [isTimeExpired, questions.length]);

  // Persist Iron Exam snapshot across page reload (sessionStore v1)
  useEffect(() => {
    if (!persistSession || !courseId || questions.length === 0 || !currentQuestion) return;
    saveActiveSession({
      version: 1,
      courseId,
      sessionType: 'challenge',
      competencyId: null,
      unitIndex: null,
      sessionTitle,
      questions,
      currentIndex,
      selectedOption: currentDraft.selectedOption,
      selectedMultiOptions: currentDraft.selectedMultiOptions,
      fillBlankValue: currentDraft.fillBlankValue,
      structuredAnswer: currentDraft.structuredAnswer,
      matchedDiagnosticRationale: null,
      stage0Phase: stage0Phases[currentQuestion.id] || 1,
      hintsRevealed: 0,
      wrongAttemptsCount: 0,
      isExhausted: false,
      isChecked: false,
      isCorrect: null,
      isCurtainLifted: true,
      canvasInteracted: currentDraft.canvasInteracted,
      ironExamState: {
        drafts,
        itemConfidences,
        flaggedIds,
        stage0Phases,
        globalConfidence,
        elapsedSeconds,
        timeLimitSeconds: effectiveTimeLimit,
      },
      results: [],
      telemetry: [],
      elapsedSeconds,
      savedAt: Date.now(),
    });
  }, [
    courseId,
    sessionTitle,
    questions,
    currentIndex,
    currentQuestion,
    currentDraft,
    drafts,
    itemConfidences,
    flaggedIds,
    stage0Phases,
    globalConfidence,
    elapsedSeconds,
    effectiveTimeLimit,
  ]);

  const recordTimeForCurrentQuestion = () => {
    if (!currentQuestion) return;
    const now = Date.now();
    const delta = Math.max(1, Math.round((now - questionEnterTimeRef.current) / 1000));
    spentByQidRef.current[currentQuestion.id] =
      (spentByQidRef.current[currentQuestion.id] || 0) + delta;
    questionEnterTimeRef.current = now;
  };

  const navigateToIndex = (targetIdx: number) => {
    if (targetIdx < 0 || targetIdx >= total || targetIdx === currentIndex) return;
    recordTimeForCurrentQuestion();
    setCurrentIndex(targetIdx);
    if (mainRef.current) mainRef.current.scrollTop = 0;
  };

  const updateCurrentDraft = (updater: (prev: IronExamQuestionDraft) => IronExamQuestionDraft) => {
    if (!currentQuestion || isTimeExpired) return;
    setDrafts((prev) => {
      const existing = prev[currentQuestion.id] || createInitialIronDraft(currentQuestion);
      return {
        ...prev,
        [currentQuestion.id]: updater(existing),
      };
    });
  };

  const handleConfirmSubmit = () => {
    if (questions.length === 0) return;
    const allItemsCalibrated = questions.every((q) => Boolean(itemConfidences[q.id]));
    if (globalConfidence === null && !allItemsCalibrated) {
      return;
    }
    let effectiveGlobalConfidence: MetacognitiveConfidence;
    if (globalConfidence !== null) {
      effectiveGlobalConfidence = globalConfidence;
    } else {
      const confScoreMap: Record<MetacognitiveConfidence, number> = {
        low: 1,
        medium: 2,
        high: 3,
      };
      const sumScore = questions.reduce(
        (acc, q) => acc + confScoreMap[itemConfidences[q.id] || 'medium'],
        0
      );
      const avgScore = Math.round(sumScore / questions.length);
      effectiveGlobalConfidence = avgScore >= 3 ? 'high' : avgScore <= 1 ? 'low' : 'medium';
    }

    recordTimeForCurrentQuestion();
    const { audit, deferredReview, gradedResults } = computeMetacognitiveAudit(
      questions,
      drafts,
      itemConfidences,
      effectiveGlobalConfidence,
      flaggedIds
    );

    const auditByQid = new Map(audit.items.map((it) => [it.question_id, it]));
    const telemetry: QuestionTelemetry[] = questions.map((q) => {
      const graded = gradedResults[q.id];
      const carried = extractCarriedDistractorIds(q);
      const auditItem = auditByQid.get(q.id);
      return {
        question_id: q.id,
        competency_id: q.competency_id,
        is_correct: graded?.isCorrect === true,
        hints_used: 0,
        seconds_spent: Math.max(1, Math.min(300, spentByQidRef.current[q.id] || 1)),
        question_text: q.stem,
        question_type: q.type,
        wrong_attempts: 0,
        ...(graded?.matchedDistractorIds?.length
          ? { matched_distractor_ids: graded.matchedDistractorIds }
          : {}),
        ...(graded?.matchedDistractorRationales
          ? { matched_distractor_rationales: graded.matchedDistractorRationales }
          : {}),
        ...(carried.length > 0 ? { carried_distractor_ids: carried } : {}),
        ...(auditItem ? { metacognitive_quadrant: auditItem.quadrant } : {}),
      };
    });

    clearActiveSession();
    setShowMetaModal(false);
    onComplete(audit.correct_count, total, telemetry, Math.max(1, elapsedSeconds), {
      metacognitiveAudit: audit,
      deferredReview,
    });
  };

  if (!currentQuestion) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-ka-bg-canvas p-6">
        <div className="bg-white p-6 rounded-xl border border-ka-border-card text-center space-y-3">
          <p className="text-sm font-bold text-slate-800">
            No hay preguntas disponibles para el Examen Modo Hierro.
          </p>
          <button
            type="button"
            onClick={onQuit}
            className="px-4 py-2 bg-ka-blue text-white rounded text-sm font-bold cursor-pointer"
          >
            Volver al curso
          </button>
        </div>
      </div>
    );
  }

  const isFlagged = Boolean(flaggedIds[currentQuestion.id]);
  const activeConf = itemConfidences[currentQuestion.id] ?? globalConfidence;
  const isFinalMinuteWarning = remainingSeconds > 0 && remainingSeconds <= 60;
  const isFiveMinuteWarning = remainingSeconds > 60 && remainingSeconds <= 300;
  const timerColorClass =
    remainingSeconds <= 60
      ? 'text-rose-200 border-rose-500/80 bg-rose-950/80 animate-pulse'
      : remainingSeconds <= 300
      ? 'text-amber-200 border-amber-500/60 bg-amber-950/60'
      : 'text-emerald-300 border-slate-700 bg-slate-800';
  const moduleBadge =
    moduleIndex === 1
      ? {
          label: 'Módulo 1 • Diagnóstico',
          cls: 'bg-indigo-600 text-white',
        }
      : moduleIndex === 2 && moduleTier === 'advanced'
      ? {
          label: 'Módulo 2 • Avanzado',
          cls: 'bg-purple-600 text-white',
        }
      : moduleIndex === 2
      ? {
          label: 'Módulo 2 • Estándar',
          cls: 'bg-sky-600 text-white',
        }
      : {
          label: 'Modo Hierro',
          cls: 'bg-indigo-600 text-white',
        };

  return (
    <div
      data-testid="iron-exam-session"
      className="min-h-screen min-h-[100dvh] bg-ka-bg-canvas flex flex-col justify-between overflow-x-hidden"
    >
      {/* Closed-Book Dark Header */}
      <header className="bg-slate-900 text-white px-3 sm:px-6 py-2.5 flex items-center justify-between gap-2 shrink-0">
        <div className="flex items-center gap-2 sm:gap-3 min-w-0">
          <button
            type="button"
            data-testid="iron-exit-btn"
            aria-label="Salir del examen Modo Hierro"
            onClick={onQuit}
            className="w-8 h-8 rounded-full hover:bg-slate-800 flex items-center justify-center text-slate-300 hover:text-white transition-colors shrink-0 cursor-pointer"
          >
            ✕
          </button>
          <span
            data-testid="iron-module-badge"
            className={`px-2 py-0.5 rounded text-[11px] font-extrabold uppercase tracking-wider shrink-0 ${moduleBadge.cls}`}
          >
            {moduleBadge.label}
          </span>
          <h1 className="text-xs sm:text-sm font-bold truncate min-w-0">
            <MathText text={sessionTitle} inline />
          </h1>
        </div>

        <div className="flex items-center gap-2 sm:gap-3 shrink-0">
          <button
            type="button"
            data-testid="scratchpad-toggle-btn"
            aria-pressed={scratchpadOpen}
            onClick={() => setScratchpadOpen((prev) => !prev)}
            className={`px-2 py-1 rounded text-xs font-bold border transition-colors cursor-pointer ${
              scratchpadOpen
                ? 'bg-amber-400 text-slate-900 border-amber-300'
                : 'bg-slate-800 text-slate-200 border-slate-700 hover:bg-slate-700'
            }`}
          >
            ✎ Pizarra
          </button>
          <span
            data-testid="iron-progress-counter"
            className="hidden sm:inline-block px-2 py-1 rounded bg-slate-800 text-xs font-semibold text-slate-200"
          >
            {answeredCount}/{total} resp.
          </span>
          <span
            data-testid="iron-timer"
            aria-label={`Tiempo restante ${formatClock(remainingSeconds)}`}
            className={`px-2.5 py-1 rounded border font-mono text-xs sm:text-sm font-bold ${timerColorClass}`}
          >
            ⏱ {formatClock(remainingSeconds)}
            {isFinalMinuteWarning ? ' • ≤1m' : isFiveMinuteWarning ? ' • ≤5m' : ''}
          </span>
        </div>
      </header>

      {/* Question Navigator Palette & Metacognitive Flag Bar */}
      <div className="bg-white border-b border-ka-border-card px-3 sm:px-6 py-2 flex flex-wrap items-center justify-between gap-2 shrink-0 min-w-0">
        <div
          className="flex items-center gap-1.5 overflow-x-auto max-w-full py-0.5"
          aria-label="Navegador de preguntas"
        >
          {questions.map((q, idx) => {
            const active = idx === currentIndex;
            const ans = answeredMap[q.id];
            const flg = Boolean(flaggedIds[q.id]);
            return (
              <button
                key={q.id}
                type="button"
                data-testid={`iron-nav-item-${idx}`}
                aria-current={active ? 'step' : undefined}
                onClick={() => navigateToIndex(idx)}
                className={`relative w-7 h-7 sm:w-8 sm:h-8 rounded-md text-xs font-bold border transition-all shrink-0 cursor-pointer ${
                  active
                    ? 'bg-ka-blue text-white border-ka-blue ring-2 ring-blue-200'
                    : ans
                    ? 'bg-emerald-50 text-emerald-800 border-emerald-300 hover:bg-emerald-100'
                    : 'bg-slate-50 text-slate-700 border-slate-300 hover:bg-slate-100'
                }`}
              >
                {idx + 1}
                {flg && (
                  <span
                    aria-label="Marcada"
                    className="absolute -top-1 -right-1 w-2.5 h-2.5 rounded-full bg-amber-500 border border-white"
                  />
                )}
              </button>
            );
          })}
        </div>

        <div className="flex flex-wrap items-center gap-2 shrink-0">
          <div className="flex items-center gap-1 text-[11px]">
            <span className="font-semibold text-slate-500 hidden sm:inline">Certeza:</span>
            {(['high', 'medium', 'low'] as MetacognitiveConfidence[]).map((conf) => (
              <button
                key={conf}
                type="button"
                data-testid={`iron-confidence-${conf}`}
                aria-pressed={activeConf === conf}
                onClick={() =>
                  setItemConfidences((prev) => ({
                    ...prev,
                    [currentQuestion.id]: conf,
                  }))
                }
                className={`px-2 py-1 rounded border font-bold cursor-pointer ${
                  activeConf === conf
                    ? 'bg-indigo-600 text-white border-indigo-600'
                    : 'bg-white text-slate-600 border-slate-300 hover:bg-slate-50'
                }`}
              >
                {conf === 'high' ? 'Alta' : conf === 'medium' ? 'Media' : 'Baja'}
              </button>
            ))}
          </div>

          <button
            type="button"
            data-testid="iron-flag-btn"
            aria-pressed={isFlagged}
            onClick={() =>
              setFlaggedIds((prev) => ({
                ...prev,
                [currentQuestion.id]: !prev[currentQuestion.id],
              }))
            }
            className={`px-2.5 py-1 rounded border text-xs font-bold cursor-pointer ${
              isFlagged
                ? 'bg-amber-100 text-amber-900 border-amber-400'
                : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50'
            }`}
          >
            {isFlagged ? '⚑ Marcada' : '⚐ Revisar luego'}
          </button>
        </div>
      </div>

      {/* Exam Question Viewport (no feedback, no hints, no blank-first curtain) */}
      <main
        ref={mainRef}
        className="flex-1 min-w-0 overflow-y-auto overflow-x-hidden py-3 sm:py-5 px-2 sm:px-6 relative"
        style={scratchpadOpen && scratchpadBgMode === 'grid' ? SCRATCHPAD_GRID_BG_STYLE : undefined}
      >
        <div className="max-w-3xl mx-auto mb-2 px-3 sm:px-4 flex items-center justify-between text-xs text-slate-500 font-semibold">
          <span>
            Pregunta {currentIndex + 1} de {total}
          </span>
          <span className="text-indigo-700">
            Libro cerrado • Retroalimentación diferida
          </span>
        </div>

        <QuestionCard
          question={currentQuestion}
          selectedOption={currentDraft.selectedOption}
          selectedMultiOptions={currentDraft.selectedMultiOptions}
          fillBlankValue={currentDraft.fillBlankValue}
          structuredAnswer={currentDraft.structuredAnswer}
          stage0Phase={stage0Phases[currentQuestion.id] || 1}
          onSelectStage0Phase={(ph) => {
            if (isTimeExpired) return;
            setStage0Phases((prev) => ({ ...prev, [currentQuestion.id]: ph }));
          }}
          isChecked={false}
          isCorrect={null}
          hintsRevealed={0}
          onRevealHint={() => {}}
          isExhausted={false}
          blankFirstEnabled={false}
          isCurtainLifted={true}
          courseTitle={courseTitle}
          wrongAttemptsCount={0}
          isPracticeMode={false}
          ironMode={true}
          onSelectOption={(id) =>
            updateCurrentDraft((prev) => ({ ...prev, selectedOption: id }))
          }
          onToggleMultiOption={(id) =>
            updateCurrentDraft((prev) => {
              const exists = prev.selectedMultiOptions.includes(id);
              return {
                ...prev,
                selectedMultiOptions: exists
                  ? prev.selectedMultiOptions.filter((x) => x !== id)
                  : [...prev.selectedMultiOptions, id],
              };
            })
          }
          onChangeFillBlank={(val) =>
            updateCurrentDraft((prev) => ({ ...prev, fillBlankValue: val }))
          }
          onChangeStructuredAnswer={(next: StructuredUserAnswer) =>
            updateCurrentDraft((prev) => ({
              ...prev,
              structuredAnswer: next,
              canvasInteracted:
                next.kind === 'invariant_canvas' ? true : prev.canvasInteracted,
            }))
          }
        />

        <ScratchpadOverlay
          isOpen={scratchpadOpen}
          questionId={currentQuestion.id}
          bgMode={scratchpadBgMode}
          onChangeBgMode={setScratchpadBgMode}
          onClose={() => setScratchpadOpen(false)}
        />
      </main>

      {/* Bottom Exam Navigation & Submit Bar */}
      <footer className="bg-white border-t border-ka-border-card px-3 sm:px-8 py-3 flex items-center justify-between gap-2 shrink-0">
        <div className="flex items-center gap-2">
          <button
            type="button"
            data-testid="iron-prev-btn"
            disabled={currentIndex === 0}
            onClick={() => navigateToIndex(currentIndex - 1)}
            className="px-3 sm:px-4 py-2 rounded-lg border border-slate-300 text-xs sm:text-sm font-bold text-slate-700 hover:bg-slate-50 disabled:opacity-40 cursor-pointer disabled:cursor-not-allowed"
          >
            ← Anterior
          </button>
          <button
            type="button"
            data-testid="iron-next-btn"
            disabled={currentIndex >= total - 1}
            onClick={() => navigateToIndex(currentIndex + 1)}
            className="px-3 sm:px-4 py-2 rounded-lg border border-slate-300 text-xs sm:text-sm font-bold text-slate-700 hover:bg-slate-50 disabled:opacity-40 cursor-pointer disabled:cursor-not-allowed"
          >
            Siguiente →
          </button>
        </div>

        <button
          type="button"
          data-testid="iron-submit-exam-btn"
          onClick={() => setShowMetaModal(true)}
          className="px-4 sm:px-6 py-2 bg-indigo-700 hover:bg-indigo-800 text-white text-xs sm:text-sm font-bold rounded-lg shadow-sm transition-colors cursor-pointer"
        >
          {submitButtonLabel || `Entregar Examen (${answeredCount}/${total})`}
        </button>
      </footer>

      <MetacognitiveModal
        isOpen={showMetaModal}
        questions={questions}
        answeredMap={answeredMap}
        flaggedMap={flaggedIds}
        itemConfidences={itemConfidences}
        globalConfidence={globalConfidence}
        isTimeExpired={isTimeExpired}
        onSelectGlobalConfidence={setGlobalConfidence}
        onSelectItemConfidence={(qid, conf) =>
          setItemConfidences((prev) => ({ ...prev, [qid]: conf }))
        }
        onCancel={() => {
          if (!isTimeExpired) setShowMetaModal(false);
        }}
        onConfirm={handleConfirmSubmit}
      />
    </div>
  );
};
