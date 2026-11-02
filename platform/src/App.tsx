import React, { useState, useEffect } from 'react';
import {
  Course,
  CourseSummary,
  Competency,
  Question,
  CourseMasteryRecord,
} from './types';
import { loadCourseMastery, updateCompetencyScore, updateCourseChallengeCompleted } from './utils/masteryStorage';
import { buildInterleavedSessionQuestions } from './utils/sessionShuffler';
import { normalizeQuestion } from './utils/questionUtils';
import {
  loadManifest,
  loadCourse,
  prefetchCourses,
  prefetchCourse,
  getCachedCourseIds,
  onCourseCacheChanged,
} from './utils/courseLoader';
import { Sidebar } from './components/Sidebar';
import { CourseOverview } from './components/CourseOverview';
import { PreExerciseModal } from './components/PreExerciseModal';
import { PracticeSession } from './components/PracticeSession';
import { CompletionScreen } from './components/CompletionScreen';
import { CourseChallenge } from './components/CourseChallenge';
import { CourseLibrary } from './components/CourseLibrary';
import {
  AppViewMode as ViewMode,
  NavigationState,
  pushNavState,
  replaceNavState,
  setupNavigationHistory,
  registerBackInterceptor,
} from './utils/navigationHistory';

// Instant manifest detection for 0ms initial render
const getInitialManifest = (): CourseSummary[] | null => {
  if (typeof document !== 'undefined') {
    const el = document.getElementById('course-manifest');
    if (el && el.textContent) {
      try {
        const parsed = JSON.parse(el.textContent.trim());
        if (parsed && Array.isArray(parsed.courses)) {
          return parsed.courses as CourseSummary[];
        }
      } catch {}
    }
  }
  return null;
};

export const App: React.FC = () => {
  const initialCourses = getInitialManifest();
  const [courses, setCourses] = useState<CourseSummary[]>(initialCourses || []);
  const [loadingCourses, setLoadingCourses] = useState(initialCourses === null);
  const [loadingCourseId, setLoadingCourseId] = useState<string | null>(null);
  const [cachedCourseIds, setCachedCourseIds] = useState<Set<string>>(new Set());

  const [activeCourse, setActiveCourse] = useState<Course | null>(null);
  const [mastery, setMastery] = useState<CourseMasteryRecord | null>(null);

  const [viewMode, setViewMode] = useState<ViewMode>('library');
  const [selectedUnitIndex, setSelectedUnitIndex] = useState<number | null>(null);

  // Mobile Back Navigation & Safety states
  const [showExitToast, setShowExitToast] = useState(false);
  const [showQuitConfirm, setShowQuitConfirm] = useState(false);

  // Active session parameters
  const [sessionCompetency, setSessionCompetency] = useState<Competency | null>(null);
  const [sessionType, setSessionType] = useState<'practice' | 'quiz' | 'test' | 'challenge'>('practice');
  const [sessionQuestions, setSessionQuestions] = useState<Question[]>([]);
  const [sessionScore, setSessionScore] = useState(0);
  const [sessionTotal, setSessionTotal] = useState(0);
  const [sessionKey, setSessionKey] = useState(0);

  // Navigation helper synchronized with History API
  const navigateView = (
    newMode: ViewMode,
    options?: { replace?: boolean; competencyId?: string; courseId?: string }
  ) => {
    setViewMode(newMode);
    const navState: NavigationState = {
      viewMode: newMode,
      courseId: options?.courseId || activeCourse?.course_id,
      competencyId: options?.competencyId || sessionCompetency?.id,
    };
    if (options?.replace) {
      replaceNavState(navState);
    } else {
      pushNavState(navState);
    }
  };

  // Setup browser popstate listener for native mobile back gesture
  useEffect(() => {
    const unregister = setupNavigationHistory({
      getCurrentState: () => ({
        viewMode,
        courseId: activeCourse?.course_id,
        competencyId: sessionCompetency?.id,
      }),
      onNavigate: (target) => {
        if (target.viewMode === 'library') {
          setActiveCourse(null);
          setViewMode('library');
        } else {
          setViewMode(target.viewMode);
        }
      },
      onDoubleBackToast: () => {
        setShowExitToast(true);
        setTimeout(() => setShowExitToast(false), 2000);
      },
    });
    return unregister;
  }, [viewMode, activeCourse, sessionCompetency]);

  // Intercept back gesture during active practice/challenge sessions
  useEffect(() => {
    if (viewMode !== 'practice' && viewMode !== 'challenge') {
      setShowQuitConfirm(false);
      return;
    }

    const unregister = registerBackInterceptor(() => {
      if (showQuitConfirm) {
        // Second back gesture: dismiss confirm modal and remain in session
        setShowQuitConfirm(false);
        return true;
      } else {
        // First back gesture: open confirm modal
        setShowQuitConfirm(true);
        return true;
      }
    });

    return unregister;
  }, [viewMode, showQuitConfirm]);

  // Load cached course IDs on mount and subscribe to updates
  useEffect(() => {
    getCachedCourseIds().then(setCachedCourseIds);
    const unsubscribe = onCourseCacheChanged((ids) => {
      setCachedCourseIds(new Set(ids));
    });
    return unsubscribe;
  }, []);

  // Load manifest instantly (0 ms if inline, or fallback fetch) and start idle prefetch
  useEffect(() => {
    let isMounted = true;
    loadManifest()
      .then((manifest) => {
        if (!isMounted) return;
        setCourses(manifest.courses);
        setLoadingCourses(false);
        prefetchCourses(manifest.courses);
      })
      .catch((err) => {
        console.error('Failed to load course manifest', err);
        if (isMounted) setLoadingCourses(false);
      });

    return () => {
      isMounted = false;
    };
  }, []);

  const selectCourse = async (summary: CourseSummary) => {
    if (summary.status === 'error') return;

    try {
      setLoadingCourseId(summary.id);
      const fullCourse = await loadCourse(summary);
      if (fullCourse) {
        const normalizedCourse: Course = {
          ...fullCourse,
          questions: (fullCourse.questions || []).map(normalizeQuestion),
        };
        setActiveCourse(normalizedCourse);
        const m = loadCourseMastery(normalizedCourse);
        setMastery(m);
        setSelectedUnitIndex(0);
        navigateView('overview', { courseId: normalizedCourse.course_id });
      }
    } catch (err) {
      console.error(`Failed to load course ${summary.id}:`, err);
      if (typeof navigator !== 'undefined' && !navigator.onLine) {
        alert("Este curso no se encuentra disponible sin conexión. Conéctate a internet para cargarlo y guardarlo para uso offline.");
      }
    } finally {
      setLoadingCourseId(null);
    }
  };

  // Unified session launcher with ZPD difficulty calibration and pedagogical interleaving for Quiz & Unit Test
  const launchSession = (
    type: 'practice' | 'quiz' | 'test' | 'challenge',
    comp: Competency | null,
    directToPractice: boolean = true
  ) => {
    if (!activeCourse) return;

    let targetComp = comp;
    // In practice/quiz/test, if comp is not passed, attempt recovery from sessionCompetency or selectedUnitIndex
    if (!targetComp && type !== 'challenge') {
      if (sessionCompetency) {
        targetComp = sessionCompetency;
      } else if (selectedUnitIndex !== null && activeCourse.competencies[selectedUnitIndex]) {
        targetComp = activeCourse.competencies[selectedUnitIndex];
      }
    }

    setSessionCompetency(targetComp);
    setSessionType(type);

    if (type !== 'challenge' && !targetComp) {
      console.error(`[launchSession] Cannot launch ${type} session without a specific competency/unit.`);
      setSessionQuestions([]);
      return;
    }

    const currentTier =
      targetComp && mastery?.competencies?.[targetComp.id]
        ? mastery.competencies[targetComp.id].status
        : undefined;

    const chosen = buildInterleavedSessionQuestions(
      activeCourse.questions,
      activeCourse.competencies,
      type,
      targetComp,
      currentTier
    );

    if (chosen.length === 0 && targetComp) {
      console.warn(
        `[launchSession] No questions found matching competency ${targetComp.id} (${targetComp.name}). Pool is empty.`
      );
      setSessionQuestions([]);
      return;
    }

    setSessionQuestions(chosen);
    setSessionKey((prev) => prev + 1);

    if (directToPractice) {
      const shouldReplace = viewMode === 'pre_exercise' || viewMode === 'completed';
      navigateView('practice', { competencyId: targetComp?.id, replace: shouldReplace });
    } else {
      navigateView('pre_exercise', { competencyId: targetComp?.id });
    }
  };

  // Launch Practice Pre-Exercise
  const handleStartPractice = (comp: Competency) => {
    launchSession('practice', comp, false);
  };

  // Start Practice from Pre-Exercise Modal (replaces modal in history)
  const handleBeginPracticeSession = () => {
    navigateView('practice', { replace: true });
  };

  // Launch Unit Quiz
  const handleStartQuiz = (comp: Competency) => {
    launchSession('quiz', comp, true);
  };

  // Launch Unit Test
  const handleStartUnitTest = (comp: Competency) => {
    launchSession('test', comp, true);
  };

  // Open Course Challenge screen
  const handleOpenCourseChallenge = () => {
    navigateView('challenge');
  };

  // Start Course Challenge Session
  const handleBeginCourseChallenge = () => {
    launchSession('challenge', null, true);
  };

  // Safe quit from session: replaces current transient state with overview so back never re-enters quizzes
  const handleQuitSession = () => {
    setShowQuitConfirm(false);
    setViewMode('overview');
    replaceNavState({
      viewMode: 'overview',
      courseId: activeCourse?.course_id,
    });
  };

  // Handle Practice Session Completion
  const handleCompleteSession = (score: number, total: number) => {
    setSessionScore(score);
    setSessionTotal(total);

    if (activeCourse) {
      if (sessionType === 'challenge') {
        const updated = updateCourseChallengeCompleted(activeCourse, score, total);
        setMastery({ ...updated });
      } else if (sessionCompetency) {
        const updated = updateCompetencyScore(
          activeCourse,
          sessionCompetency.id,
          score,
          total,
          sessionType
        );
        setMastery({ ...updated });
      }
    }

    // Replace practice with completed so you cannot back into questions
    navigateView('completed', { replace: true });
  };

  // Handle "Try again" from Completion - preserves sessionType and performs fresh reshuffle directly
  const handleTryAgain = () => {
    if (!activeCourse) return;
    let targetComp = sessionCompetency;
    if (!targetComp && sessionType !== 'challenge' && sessionQuestions.length > 0) {
      const qCompId = sessionQuestions[0].competency_id;
      targetComp = activeCourse.competencies.find((c) => c.id === qCompId) || null;
    }
    launchSession(sessionType, targetComp, true);
  };

  // Handle "Up next" from Completion
  const handleUpNext = () => {
    if (!activeCourse || !sessionCompetency) {
      navigateView('overview');
      return;
    }

    const currentIdx = activeCourse.competencies.findIndex(
      (c) => c.id === sessionCompetency.id
    );
    if (currentIdx >= 0 && currentIdx < activeCourse.competencies.length - 1) {
      const nextComp = activeCourse.competencies[currentIdx + 1];
      handleStartPractice(nextComp);
    } else {
      navigateView('overview');
    }
  };

  return (
    <div className="min-h-screen bg-ka-bg-canvas text-ka-text-primary flex flex-col font-sans">
      {viewMode === 'library' && (
        <CourseLibrary
          courses={courses}
          loading={loadingCourses}
          onSelectCourse={selectCourse}
          onPrefetch={(id) => prefetchCourse(id)}
          loadingCourseId={loadingCourseId}
          cachedCourseIds={cachedCourseIds}
        />
      )}

      {viewMode === 'overview' && activeCourse && mastery && (
        <div className="flex min-h-screen">
          <Sidebar
            course={activeCourse}
            mastery={mastery}
            selectedUnitIndex={selectedUnitIndex}
            isCourseChallengeActive={false}
            onSelectUnit={(idx) => {
              setSelectedUnitIndex(idx);
              handleStartPractice(activeCourse.competencies[idx]);
            }}
            onSelectCourseChallenge={handleOpenCourseChallenge}
            onBackToLibrary={() => {
              setActiveCourse(null);
              navigateView('library');
            }}
          />
          <main className="flex-1 min-w-0 overflow-y-auto pt-14 lg:pt-0">
            <CourseOverview
              course={activeCourse}
              mastery={mastery}
              onStartPractice={handleStartPractice}
              onStartQuiz={handleStartQuiz}
              onStartUnitTest={handleStartUnitTest}
              onStartCourseChallenge={handleOpenCourseChallenge}
            />
          </main>
        </div>
      )}

      {viewMode === 'pre_exercise' && sessionCompetency && (
        <PreExerciseModal
          competency={sessionCompetency}
          questionCount={sessionQuestions.length}
          onStart={handleBeginPracticeSession}
          onBack={() => navigateView('overview')}
        />
      )}

      {viewMode === 'practice' && (
        <PracticeSession
          key={sessionKey}
          sessionTitle={
            sessionType === 'challenge'
              ? 'Course challenge'
              : sessionType === 'quiz'
              ? `Quiz • ${sessionCompetency?.name || 'Unit'}`
              : sessionType === 'test'
              ? `Unit test • ${sessionCompetency?.name || 'Unit'}`
              : sessionCompetency?.name || 'Practice'
          }
          questions={sessionQuestions}
          onRestart={() => launchSession(sessionType, sessionCompetency, true)}
          onComplete={handleCompleteSession}
          onQuit={() => setShowQuitConfirm(true)}
        />
      )}

      {viewMode === 'completed' && activeCourse && (
        <CompletionScreen
          course={activeCourse}
          competency={sessionCompetency || undefined}
          score={sessionScore}
          total={sessionTotal}
          sessionType={sessionType}
          onTryAgain={handleTryAgain}
          onUpNext={handleUpNext}
        />
      )}

      {viewMode === 'challenge' && activeCourse && (
        <div className="flex min-h-screen">
          <Sidebar
            course={activeCourse}
            mastery={mastery}
            selectedUnitIndex={null}
            isCourseChallengeActive={true}
            onSelectUnit={(idx) => {
              setSelectedUnitIndex(idx);
              navigateView('overview');
            }}
            onSelectCourseChallenge={() => {}}
            onBackToLibrary={() => {
              setActiveCourse(null);
              navigateView('library');
            }}
          />
          <main className="flex-1 min-w-0 overflow-y-auto pt-14 lg:pt-0">
            <CourseChallenge
              course={activeCourse}
              totalQuestions={Math.min(30, activeCourse.questions.length)}
              onStart={handleBeginCourseChallenge}
              onBack={() => setShowQuitConfirm(true)}
            />
          </main>
        </div>
      )}

      {/* Toast: Presiona atrás de nuevo para salir */}
      {showExitToast && (
        <div
          data-testid="double-back-toast"
          role="status"
          aria-live="polite"
          className="fixed bottom-8 left-1/2 -translate-x-1/2 z-50 bg-slate-900/95 text-white text-xs sm:text-sm font-semibold px-4 py-2.5 rounded-full shadow-2xl backdrop-blur-md transition-all duration-300 flex items-center gap-2 pointer-events-none"
        >
          <span aria-hidden="true">↩️</span>
          <span>Presiona atrás de nuevo para salir</span>
        </div>
      )}

      {/* Modal: Confirmación de abandono de práctica/examen */}
      {showQuitConfirm && (
        <div
          role="dialog"
          aria-modal="true"
          aria-labelledby="quit-dialog-title"
          data-testid="quit-confirm-modal"
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
        >
          <div className="bg-white rounded-2xl max-w-sm w-full p-6 shadow-2xl text-center border border-slate-200">
            <div className="w-12 h-12 rounded-full bg-amber-100 text-amber-600 flex items-center justify-center mx-auto mb-4 text-2xl font-bold">
              ⚠️
            </div>
            <h3 id="quit-dialog-title" className="text-lg font-bold text-ka-text-primary mb-2">
              ¿Deseas salir de la sesión?
            </h3>
            <p className="text-sm text-ka-text-secondary mb-6 leading-relaxed">
              El progreso actual de esta práctica o examen no se guardará si decides salir ahora.
            </p>
            <div className="flex gap-3">
              <button
                type="button"
                data-testid="quit-confirm-continue"
                onClick={() => setShowQuitConfirm(false)}
                className="flex-1 py-2.5 px-4 bg-slate-100 hover:bg-slate-200 text-ka-text-primary font-bold text-sm rounded-xl transition-colors cursor-pointer"
              >
                Continuar
              </button>
              <button
                type="button"
                data-testid="quit-confirm-exit"
                onClick={handleQuitSession}
                className="flex-1 py-2.5 px-4 bg-rose-600 hover:bg-rose-700 text-white font-bold text-sm rounded-xl transition-colors shadow-sm cursor-pointer"
              >
                Salir
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
export default App;
