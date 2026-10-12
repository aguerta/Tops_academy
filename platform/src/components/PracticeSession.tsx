import React, { useState, useEffect, useRef } from 'react';
import confetti from 'canvas-confetti';
import { Question } from '../types';
import { QuestionCard } from './QuestionCard';
import { FeedbackToast } from './FeedbackToast';
import { MathText } from './MathText';
import { checkMathEquivalence } from '../utils/mathEquivalence';
import { isOptionCorrect, getCorrectOptionIds } from '../utils/questionUtils';

interface PracticeSessionProps {
  sessionTitle: string;
  questions: Question[];
  onComplete: (score: number, total: number) => void;
  onQuit: () => void;
  onRestart?: () => void;
}

interface QuestionResult {
  questionId: string;
  isCorrect: boolean;
  skipped: boolean;
}

export const PracticeSession: React.FC<PracticeSessionProps> = ({
  sessionTitle,
  questions,
  onComplete,
  onQuit,
  onRestart,
}) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [selectedMultiOptions, setSelectedMultiOptions] = useState<string[]>([]);
  const [fillBlankValue, setFillBlankValue] = useState<string>('');
  const [hintsRevealed, setHintsRevealed] = useState(0);

  const [wrongAttemptsCount, setWrongAttemptsCount] = useState<number>(0);
  const [isExhausted, setIsExhausted] = useState<boolean>(false);

  const [isChecked, setIsChecked] = useState(false);
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null);
  const [results, setResults] = useState<QuestionResult[]>([]);
  const autoAdvanceTimerRef = useRef<NodeJS.Timeout | null>(null);

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
      <div className="min-h-screen bg-slate-50 flex flex-col items-center justify-center p-6 text-center">
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

  // Determine if student has input an answer to enable Check button
  const hasAnswer =
    currentQuestion.type === 'multiple_choice_7_options'
      ? selectedOption !== null
      : currentQuestion.type === 'multiple_select'
      ? selectedMultiOptions.length > 0
      : fillBlankValue.trim().length > 0;

  const handleSelectOption = (id: string) => {
    if (isExhausted || (isChecked && isCorrect === true)) return;
    setSelectedOption(id);
    if (isChecked && !isCorrect) {
      setIsChecked(false);
      setIsCorrect(null);
    }
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
    }

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

      if (nextWrongCount >= 3) {
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
    setIsChecked(false);
    setIsCorrect(null);
  };

  const handleRetry = () => {
    if (isExhausted) return;
    clearAutoAdvanceTimer();
    setIsChecked(false);
    setIsCorrect(null);
    if (currentQuestion.type === 'multiple_choice_7_options') {
      setSelectedOption(null);
    }
  };

  const handleNext = (overrideIsCorrect?: boolean) => {
    clearAutoAdvanceTimer();
    const correctVal = overrideIsCorrect !== undefined ? overrideIsCorrect : isCorrect === true;
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
      const finalScore = newResults.filter((r) => r.isCorrect).length;
      onComplete(finalScore, total);
    } else {
      setCurrentIndex((prev) => prev + 1);
      setSelectedOption(null);
      setSelectedMultiOptions([]);
      setFillBlankValue('');
      setHintsRevealed(0);
      setIsChecked(false);
      setIsCorrect(null);
      setWrongAttemptsCount(0);
      setIsExhausted(false);
    }
  };

  const handleSkip = () => {
    clearAutoAdvanceTimer();
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
      const finalScore = newResults.filter((r) => r.isCorrect).length;
      onComplete(finalScore, total);
    } else {
      setCurrentIndex((prev) => prev + 1);
      setSelectedOption(null);
      setSelectedMultiOptions([]);
      setFillBlankValue('');
      setHintsRevealed(0);
      setIsChecked(false);
      setIsCorrect(null);
      setWrongAttemptsCount(0);
      setIsExhausted(false);
    }
  };

  // Keyboard navigation: Enter checks answer, advances if correct, or allows retry
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.isComposing) return;

      if (e.key === 'Enter') {
        e.preventDefault();

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
  ]);

  return (
    <div data-testid="practice-session" className="min-h-screen bg-white flex flex-col justify-between">
      {/* Top Header */}
      <header className="h-16 border-b border-ka-border-subtle px-6 flex items-center justify-between">
        <button
          onClick={() => {
            clearAutoAdvanceTimer();
            onQuit();
          }}
          className="w-9 h-9 rounded-full hover:bg-slate-100 flex items-center justify-center text-ka-text-secondary text-base transition-colors"
          title="Quit practice"
        >
          ✕
        </button>
        <div className="text-sm font-bold text-ka-text-primary text-center">
          <MathText text={sessionTitle} inline />
        </div>
        {onRestart ? (
          <button
            onClick={() => {
              clearAutoAdvanceTimer();
              onRestart();
            }}
            data-testid="restart-session-btn"
            className="text-xs font-semibold text-ka-blue hover:text-ka-blue-hover flex items-center gap-1.5 transition-colors px-3 py-1.5 rounded-lg border border-slate-200 hover:bg-slate-50 shadow-sm cursor-pointer"
            title="Restart session with new shuffled questions"
          >
            <span>🔄</span>
            <span className="hidden sm:inline">Restart</span>
          </button>
        ) : (
          <div className="w-9" />
        )}
      </header>

      {/* Main Question Surface */}
      <main className="flex-1 overflow-y-auto pb-28">
        <QuestionCard
          question={currentQuestion}
          selectedOption={selectedOption}
          selectedMultiOptions={selectedMultiOptions}
          fillBlankValue={fillBlankValue}
          isChecked={isChecked}
          isCorrect={isCorrect}
          isExhausted={isExhausted}
          onSelectOption={handleSelectOption}
          onToggleMultiOption={handleToggleMultiOption}
          onChangeFillBlank={handleChangeFillBlank}
          hintsRevealed={hintsRevealed}
          onRevealHint={() => setHintsRevealed((prev) => prev + 1)}
        />
      </main>

      {/* Floating Feedback Toast */}
      {isChecked && isCorrect !== null && (
        <FeedbackToast
          isCorrect={isCorrect}
          question={currentQuestion}
          onRedo={handleRedo}
          isExhausted={isExhausted}
          wrongAttemptsCount={wrongAttemptsCount}
        />
      )}

      {/* Fixed Bottom Action & Progress Bar */}
      <footer className="fixed bottom-0 left-0 right-0 h-20 bg-white border-t border-ka-border-card px-8 flex items-center justify-between z-20 shadow-sm">
        {/* Left Side: Counter & Progress Indicator Dots */}
        <div className="flex items-center gap-4">
          <span className="text-lg text-slate-400">🔄</span>

          <span className="text-xs sm:text-sm font-bold text-ka-text-primary min-w-[70px]">
            {currentIndex === 0 && !isChecked
              ? `Do ${total} problems`
              : `${currentIndex + 1} of ${total}`}
          </span>

          {/* Progress Indicator Dots */}
          <div className="flex items-center gap-2">
            {questions.map((_, idx) => {
              const res = results[idx];
              const isCurrent = idx === currentIndex;

              if (res) {
                if (res.isCorrect) {
                  return (
                    <div
                      key={idx}
                      className="w-4 h-4 rounded-full bg-ka-green-badge text-white flex items-center justify-center text-[10px] font-bold"
                    >
                      ✓
                    </div>
                  );
                } else {
                  return (
                    <div
                      key={idx}
                      className="w-3.5 h-3.5 rounded-full bg-red-500 flex items-center justify-center text-[9px] text-white font-bold"
                    >
                      ✕
                    </div>
                  );
                }
              }

              if (isCurrent && isChecked) {
                if (isCorrect) {
                  return (
                    <div
                      key={idx}
                      className="w-4 h-4 rounded-full bg-ka-green-badge text-white flex items-center justify-center text-[10px] font-bold"
                    >
                      ✓
                    </div>
                  );
                } else {
                  return (
                    <div
                      key={idx}
                      className="w-3.5 h-3.5 rounded-full bg-red-500 flex items-center justify-center text-[9px] text-white font-bold"
                    >
                      ✕
                    </div>
                  );
                }
              }

              return (
                <div
                  key={idx}
                  className={`w-3 h-3 rounded-full border-2 transition-all ${
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
        <div className="flex items-center gap-4">
          <button
            data-testid="skip-btn"
            disabled={(isChecked && isCorrect === true) || isExhausted}
            onClick={handleSkip}
            className={`text-sm font-semibold transition-colors ${
              (isChecked && isCorrect === true) || isExhausted
                ? 'text-slate-300 cursor-not-allowed'
                : 'text-ka-blue hover:text-ka-blue-hover'
            }`}
          >
            Skip
          </button>

          {isExhausted ? (
            <button
              data-testid="next-question-btn"
              onClick={() => handleNext(false)}
              className="px-6 py-2.5 bg-ka-blue hover:bg-ka-blue-hover text-white text-sm font-bold rounded shadow-md transition-colors flex items-center gap-2 cursor-pointer"
            >
              <span>Next question</span>
              <kbd className="hidden sm:inline-block px-1.5 py-0.5 text-[10px] bg-blue-700/60 text-white rounded font-mono border border-blue-400/30">↵ Enter</kbd>
            </button>
          ) : isChecked && isCorrect ? (
            <button
              data-testid="next-question-btn"
              onClick={() => handleNext(true)}
              className="px-6 py-2.5 bg-ka-blue hover:bg-ka-blue-hover text-white text-sm font-bold rounded shadow-md transition-colors flex items-center gap-2 cursor-pointer"
            >
              <span>Next question</span>
              <kbd className="hidden sm:inline-block px-1.5 py-0.5 text-[10px] bg-blue-700/60 text-white rounded font-mono border border-blue-400/30">↵ Enter</kbd>
            </button>
          ) : isChecked && !isCorrect ? (
            <div className="flex items-center gap-2">
              <button
                data-testid="quick-redo-btn"
                onClick={handleRedo}
                className="px-4 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-sm font-bold rounded border border-slate-300 transition-colors flex items-center gap-1.5 cursor-pointer"
                title="Clear input and re-attempt question"
              >
                <span>↺</span>
                <span>Quick Redo</span>
              </button>
              <button
                data-testid="check-btn"
                onClick={handleRetry}
                className="px-6 py-2.5 bg-ka-blue hover:bg-ka-blue-hover text-white text-sm font-bold rounded shadow-md transition-colors cursor-pointer flex items-center gap-2"
              >
                <span>Try again</span>
                <kbd className="hidden sm:inline-block px-1.5 py-0.5 text-[10px] bg-blue-700/60 text-white rounded font-mono border border-blue-400/30">↵ Enter</kbd>
              </button>
            </div>
          ) : (
            <button
              data-testid="check-btn"
              disabled={!hasAnswer}
              onClick={() => handleCheck(true)}
              className={`px-6 py-2.5 text-sm font-bold rounded transition-colors flex items-center gap-2 ${
                hasAnswer
                  ? 'bg-ka-blue hover:bg-ka-blue-hover text-white cursor-pointer shadow-md'
                  : 'bg-slate-300 text-white cursor-not-allowed'
              }`}
            >
              <span>Check</span>
              {hasAnswer && (
                <kbd className="hidden sm:inline-block px-1.5 py-0.5 text-[10px] bg-blue-700/60 text-white rounded font-mono border border-blue-400/30">↵ Enter</kbd>
              )}
            </button>
          )}
        </div>
      </footer>
    </div>
  );
};
