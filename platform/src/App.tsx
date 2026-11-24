import React, { useState, useEffect, useRef } from 'react';
import {
  AdaptiveExamSummary,
  AdaptiveModuleResult,
  Course,
  CourseSummary,
  Competency,
  Question,
  CourseMasteryRecord,
  QuestionTelemetry,
  ChallengeExecutionSummary,
  M22AttemptEvent,
  MasteryTier,
  MetacognitiveAudit,
  SessionType,
} from './types';
import {
  loadCourseMastery,
  updateCompetencyScore,
  updateCourseChallengeCompleted,
  updateCourseChallengeWithSkillCalibration,
  updateSessionWithCrossSkillCalibration,
  getActiveMisconceptions,
  getTimingForCompetency,
  getTimingForChallenge,
  isUnitCompleted,
  isUnitStarted,
} from './utils/masteryStorage';
import {
  buildAdaptiveModule1,
  buildAdaptiveModule2,
  buildColdTransferProbeQuestions,
  buildInterleavedSessionQuestions,
  buildMasteryChallengeQuestions,
  buildMisconceptionSession,
  computeAdaptiveExamSummary,
} from './utils/sessionShuffler';
import { appendM22Events } from './utils/m22Telemetry';
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
import {
  IronExamCompletionOutcome,
  IronExamSession,
} from './components/session/IronExamSession';
import { CompletionScreen } from './components/CompletionScreen';
import { ShortcutHelp } from './components/ShortcutHelp';
import { CourseChallenge } from './components/CourseChallenge';
import { CourseLibrary } from './components/CourseLibrary';
import { ProgressLogView } from './components/ProgressLogView';
import {
  AppViewMode as ViewMode,
  NavigationState,
  parseUrlToState,
  pushNavState,
  replaceNavState,
  setupNavigationHistory,
  registerBackInterceptor,
} from './utils/navigationHistory';
import {
  loadActiveSession,
  clearActiveSession,
  ActiveSessionSnapshot,
} from './utils/sessionStore';
import {
  getSyncConfig,
  PROGRESS_SYNCED_EVENT,
  syncWithGist,
} from './utils/cloudSync';

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
  const [focusCompetencyId, setFocusCompetencyId] = useState<string | null>(null);
  const quitDialogRef = useRef<HTMLDialogElement>(null);

  // Mobile Back Navigation & Safety states
  const [showExitToast, setShowExitToast] = useState(false);
  const [showQuitConfirm, setShowQuitConfirm] = useState(false);

  // Active session parameters
  const [sessionCompetency, setSessionCompetency] = useState<Competency | null>(null);
  const [sessionType, setSessionType] = useState<SessionType>('practice');
  const [sessionQuestions, setSessionQuestions] = useState<Question[]>([]);
  const [sessionScore, setSessionScore] = useState(0);
  const [sessionTotal, setSessionTotal] = useState(0);
  const [sessionKey, setSessionKey] = useState(0);
  const [restoredSnapshot, setRestoredSnapshot] = useState<ActiveSessionSnapshot | null>(null);

  const resolveCourseSummary = (courseId: string): CourseSummary => {
    return (
      courses.find((c) => c.id === courseId) || {
        id: courseId,
        title: courseId,
        filename: `${courseId}.json`,
        description: '',
        status: 'valid',
      }
    );
  };

  // Milestone 14, 14-B & 20: Timing, Telemetry, Challenge Execution Summary & Iron Exam Outcome
  const [challengeSummary, setChallengeSummary] = useState<ChallengeExecutionSummary | null>(null);
  const [ironOutcome, setIronOutcome] = useState<IronExamCompletionOutcome | null>(null);
  const [adaptiveSummary, setAdaptiveSummary] = useState<AdaptiveExamSummary | null>(null);
  const [adaptiveExamState, setAdaptiveExamState] = useState<{
    phase: 'module1' | 'routing' | 'module2';
    mod1Questions: Question[];
    mod1Result?: AdaptiveModuleResult;
    mod1Outcome?: IronExamCompletionOutcome;
    mod1Telemetry?: QuestionTelemetry[];
    mod2Tier?: 'standard' | 'advanced';
    mod2Questions?: Question[];
  } | null>(null);
  const [latestTimingData, setLatestTimingData] = useState<{
    totalSeconds?: number;
    avgSeconds?: number;
    isNewRecord?: boolean;
    previousTier?: MasteryTier;
    newTier?: MasteryTier;
  }>({});
  const [latestMisconceptions, setLatestMisconceptions] = useState<Array<{
    question_id: string;
    competency_id: string;
    competency_name?: string;
    text: string;
  }>>([]);

  // Navigation helper synchronized with History API
  const navigateView = (
    newMode: ViewMode,
    options?: { replace?: boolean; competencyId?: string; courseId?: string; sessionType?: string }
  ) => {
    setViewMode(newMode);
    const navState: NavigationState = {
      viewMode: newMode,
      courseId: options?.courseId || activeCourse?.course_id,
      competencyId: options?.competencyId || sessionCompetency?.id,
      sessionType: options?.sessionType || sessionType,
    };
    if (options?.replace) {
      replaceNavState(navState);
    } else {
      pushNavState(navState);
    }
  };

  // Automatic background GitHub Gist sync on startup & live refresh on remote merge
  useEffect(() => {
    if (getSyncConfig()) {
      void syncWithGist();
    }
  }, []);

  useEffect(() => {
    const handleSynced = () => {
      if (activeCourse) {
        setMastery(loadCourseMastery(activeCourse));
      }
    };
    window.addEventListener(PROGRESS_SYNCED_EVENT, handleSynced);
    return () => window.removeEventListener(PROGRESS_SYNCED_EVENT, handleSynced);
  }, [activeCourse]);

  // Sync document.title with the active subpage so browser history, tabs, and screen readers distinguish entries
  useEffect(() => {
    const courseTitle = activeCourse?.title;
    if (viewMode === 'library' || !courseTitle) {
      document.title = "Top's Academy";
      return;
    }
    if (viewMode === 'progress_log') {
      document.title = `Bitácora · ${courseTitle} | Top's Academy`;
    } else if (viewMode === 'challenge') {
      document.title = `Course Challenge · ${courseTitle} | Top's Academy`;
    } else if (viewMode === 'practice' || viewMode === 'pre_exercise' || viewMode === 'completed') {
      const label = sessionCompetency?.name || sessionType;
      document.title = `${label} · ${courseTitle} | Top's Academy`;
    } else {
      document.title = `${courseTitle} | Top's Academy`;
    }
  }, [viewMode, activeCourse, sessionCompetency, sessionType]);

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
          return;
        }
        if (target.courseId && (!activeCourse || activeCourse.course_id !== target.courseId)) {
          const summary = resolveCourseSummary(target.courseId);
          loadCourse(summary)
            .then((fullCourse) => {
              if (!fullCourse) return;
              const normalizedCourse: Course = {
                ...fullCourse,
                questions: (fullCourse.questions || []).map(normalizeQuestion),
              };
              setActiveCourse(normalizedCourse);
              setMastery(loadCourseMastery(normalizedCourse));
              setViewMode(target.viewMode);
            })
            .catch((err) => {
              console.warn('[App] Failed to load course on popstate:', err);
              setActiveCourse(null);
              setViewMode('library');
            });
          return;
        }
        if (target.viewMode === 'overview' && sessionCompetency) {
          setFocusCompetencyId(sessionCompetency.id);
        }
        setViewMode(target.viewMode);
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
      if (!showQuitConfirm && document.querySelector('[data-testid="iron-time-expired-banner"]')) {
        return true;
      }
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

  // Sync quit confirmation native <dialog>
  useEffect(() => {
    const el = quitDialogRef.current;
    if (!el) return;
    if (showQuitConfirm && !el.open) {
      el.showModal();
    } else if (!showQuitConfirm && el.open) {
      el.close();
    }
  }, [showQuitConfirm]);

  // Esc opens the quit confirmation; a second Esc confirms the exit (handled by <dialog> onCancel)
  useEffect(() => {
    if (viewMode !== 'practice') return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key !== 'Escape' || e.isComposing || e.repeat || e.defaultPrevented) return;
      if (showQuitConfirm) return;
      if (document.querySelector('dialog[open], [role="dialog"]')) return;
      e.preventDefault();
      setShowQuitConfirm(true);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  });

  // Enter on the course overview: Unit Test of the first unit (course order) that has
  // activity but is not completed; otherwise Practice of the first unit.
  useEffect(() => {
    if (viewMode !== 'overview' || !activeCourse) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key !== 'Enter' || e.isComposing || e.repeat || e.defaultPrevented) return;
      if (e.ctrlKey || e.metaKey || e.altKey || e.shiftKey) return;
      if (document.querySelector('dialog[open], [role="dialog"]') || document.body.style.overflow === 'hidden') return;
      const t = e.target as HTMLElement | null;
      if (t && t !== document.body && /^(BUTTON|A|INPUT|TEXTAREA|SELECT)$/.test(t.tagName)) return;
      const comps = activeCourse.competencies;
      if (comps.length === 0) return;
      e.preventDefault();
      const pending = comps.find((c) => {
        const m = mastery?.competencies?.[c.id];
        return isUnitStarted(m) && !isUnitCompleted(m);
      });
      if (pending) {
        // 25+ mastery points = perfect practice already done -> Unit Test; otherwise Practice
        const pts = mastery?.competencies?.[pending.id]?.points ?? 0;
        if (pts >= 25) handleStartUnitTest(pending);
        else handleStartPractice(pending);
      }
      else handleStartPractice(comps[0]);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  });

  // Esc on the course overview returns to the course library;
  // Esc on the progress log returns to the course overview.
  useEffect(() => {
    if (viewMode !== 'overview' && viewMode !== 'progress_log') return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key !== 'Escape' || e.isComposing || e.repeat || e.defaultPrevented) return;
      // Let open dialogs / the mobile sidebar consume Esc first
      if (document.querySelector('dialog[open], [role="dialog"]') || document.body.style.overflow === 'hidden') return;
      e.preventDefault();
      if (viewMode === 'progress_log') {
        navigateView('overview');
        return;
      }
      setActiveCourse(null);
      navigateView('library');
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  });

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

  // Milestone 12 + Subpage Routing: Hydrate active session snapshot OR current URL route on mount
  useEffect(() => {
    const snapshot = loadActiveSession();
    if (snapshot && snapshot.courseId && snapshot.questions && snapshot.questions.length > 0) {
      let isMounted = true;
      const summary = resolveCourseSummary(snapshot.courseId);

      loadCourse(summary)
        .then((fullCourse) => {
          if (!isMounted || !fullCourse) return;
          const normalizedCourse: Course = {
            ...fullCourse,
            questions: (fullCourse.questions || []).map(normalizeQuestion),
          };
          setActiveCourse(normalizedCourse);
          const m = loadCourseMastery(normalizedCourse);
          setMastery(m);
          setSessionType(snapshot.sessionType);
          const comp = snapshot.competencyId
            ? normalizedCourse.competencies.find((c) => c.id === snapshot.competencyId) || null
            : null;
          setSessionCompetency(comp);
          setSelectedUnitIndex(snapshot.unitIndex ?? 0);
          setSessionQuestions(snapshot.questions.map(normalizeQuestion));
          setRestoredSnapshot(snapshot);
          setViewMode('practice');
          replaceNavState({
            viewMode: 'practice',
            courseId: normalizedCourse.course_id,
            competencyId: comp?.id,
            sessionType: snapshot.sessionType,
          });
        })
        .catch((err) => {
          console.warn('[App] Failed to hydrate active session from snapshot:', err);
        });

      return () => {
        isMounted = false;
      };
    }

    const initialRoute = parseUrlToState();
    if (initialRoute.viewMode === 'library' || !initialRoute.courseId) {
      return;
    }

    let isMounted = true;
    const summary = resolveCourseSummary(initialRoute.courseId);

    loadCourse(summary)
      .then((fullCourse) => {
        if (!isMounted || !fullCourse) return;
        const normalizedCourse: Course = {
          ...fullCourse,
          questions: (fullCourse.questions || []).map(normalizeQuestion),
        };
        setActiveCourse(normalizedCourse);
        const m = loadCourseMastery(normalizedCourse);
        setMastery(m);

        if (initialRoute.viewMode === 'pre_exercise' && initialRoute.sessionType) {
          const validType = initialRoute.sessionType as SessionType;
          const targetComp = initialRoute.competencyId
            ? normalizedCourse.competencies.find((c) => c.id === initialRoute.competencyId) || null
            : null;
          if (targetComp) {
            const idx = normalizedCourse.competencies.findIndex((c) => c.id === targetComp.id);
            if (idx >= 0) setSelectedUnitIndex(idx);
          }
          setSessionCompetency(targetComp);
          setSessionType(validType);

          if (validType === 'mastery_challenge') {
            const chosen = buildMasteryChallengeQuestions(normalizedCourse, m, new Date(), 6);
            if (chosen.length > 0) {
              setSessionQuestions(chosen);
              setViewMode('practice');
              replaceNavState({ ...initialRoute, viewMode: 'practice' });
              return;
            }
          } else if (validType === 'misconception_drill') {
            const activeIds = getActiveMisconceptions(m).map((e) => e.distractor_id);
            const chosen = buildMisconceptionSession(normalizedCourse, activeIds, 6);
            if (chosen.length > 0) {
              setSessionQuestions(chosen);
              setViewMode('practice');
              replaceNavState({ ...initialRoute, viewMode: 'practice' });
              return;
            }
          } else if (validType === 'challenge' || targetComp) {
            const currentTier =
              targetComp && m?.competencies?.[targetComp.id]
                ? m.competencies[targetComp.id].status
                : undefined;
            const chosen = buildInterleavedSessionQuestions(
              normalizedCourse.questions,
              normalizedCourse.competencies,
              validType,
              targetComp,
              currentTier
            );
            if (chosen.length > 0) {
              setSessionQuestions(chosen);
              setViewMode('pre_exercise');
              replaceNavState(initialRoute);
              return;
            }
          }
          setViewMode('overview');
          replaceNavState({ viewMode: 'overview', courseId: normalizedCourse.course_id });
          return;
        }

        setViewMode(initialRoute.viewMode);
        replaceNavState(initialRoute);
      })
      .catch((err) => {
        console.warn('[App] Failed to hydrate route from URL:', err);
        if (isMounted) {
          setActiveCourse(null);
          setViewMode('library');
          replaceNavState({ viewMode: 'library' });
        }
      });

    return () => {
      isMounted = false;
    };
  }, []);

  // Milestone 12: Silent ETag reconciliation on laptop sleep wake-up
  useEffect(() => {
    const handleVisibilityChange = () => {
      if (document.visibilityState === 'visible' && activeCourse) {
        const summary = resolveCourseSummary(activeCourse.course_id);
        loadCourse(summary).catch((err) => {
          console.warn('[App] Silent ETag reconciliation on wake-up failed:', err);
        });
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, [activeCourse, courses]);

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
        setFocusCompetencyId(null);
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
    type: SessionType,
    comp: Competency | null,
    directToPractice: boolean = true
  ) => {
    if (!activeCourse) return;

    clearActiveSession();
    setRestoredSnapshot(null);
    setIronOutcome(null);
    setAdaptiveExamState(null);
    setAdaptiveSummary(null);

    if (type === 'mastery_challenge') {
      const mRecord = mastery ?? loadCourseMastery(activeCourse);
      const chosen = buildMasteryChallengeQuestions(activeCourse, mRecord, new Date(), 6);
      setSessionCompetency(null);
      setFocusCompetencyId(null);
      setSessionType('mastery_challenge');
      setSessionQuestions(chosen);
      setSessionKey((prev) => prev + 1);
      if (chosen.length === 0) return;
      const shouldReplace = viewMode === 'pre_exercise' || viewMode === 'completed';
      if (directToPractice) {
        navigateView('practice', { replace: shouldReplace, sessionType: 'mastery_challenge' });
      } else {
        navigateView('pre_exercise', { sessionType: 'mastery_challenge' });
      }
      return;
    }

    if (type === 'misconception_drill') {
      const mRecord = mastery ?? loadCourseMastery(activeCourse);
      const activeIds = getActiveMisconceptions(mRecord).map((e) => e.distractor_id);
      const chosen = buildMisconceptionSession(activeCourse, activeIds, 6);
      setSessionCompetency(null);
      setFocusCompetencyId(null);
      setSessionType('misconception_drill');
      setSessionQuestions(chosen);
      setSessionKey((prev) => prev + 1);
      if (chosen.length === 0) return;
      const shouldReplace = viewMode === 'pre_exercise' || viewMode === 'completed';
      if (directToPractice) {
        navigateView('practice', { replace: shouldReplace, sessionType: 'misconception_drill' });
      } else {
        navigateView('pre_exercise', { sessionType: 'misconception_drill' });
      }
      return;
    }

    if (type === 'cold_transfer_probe') {
      const chosen = buildColdTransferProbeQuestions(activeCourse.questions, 8);
      setSessionCompetency(null);
      setFocusCompetencyId(null);
      setSessionType('cold_transfer_probe');
      setSessionQuestions(chosen);
      setSessionKey((prev) => prev + 1);
      if (chosen.length === 0) return;
      const shouldReplace = viewMode === 'pre_exercise' || viewMode === 'completed';
      if (directToPractice) {
        navigateView('practice', { replace: shouldReplace, sessionType: 'cold_transfer_probe' });
      } else {
        navigateView('pre_exercise', { sessionType: 'cold_transfer_probe' });
      }
      return;
    }

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
    setFocusCompetencyId(null);
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
      navigateView('practice', { competencyId: targetComp?.id, replace: shouldReplace, sessionType: type });
    } else {
      navigateView('pre_exercise', { competencyId: targetComp?.id, sessionType: type });
    }
  };

  const handleStartMasteryChallenge = () => {
    launchSession('mastery_challenge', null, true);
  };

  const handleStartMisconceptionDrill = () => {
    launchSession('misconception_drill', null, true);
  };

  const handleStartColdTransferProbe = () => {
    launchSession('cold_transfer_probe', null, true);
  };

  const handleOpenProgressLog = () => {
    navigateView('progress_log');
  };

  // Launch Practice Pre-Exercise
  const handleStartPractice = (comp: Competency) => {
    launchSession('practice', comp, false);
  };

  // Start Practice from Pre-Exercise Modal (replaces modal in history)
  const handleBeginPracticeSession = () => {
    navigateView('practice', { replace: true });
  };

  // Launch Unit Quiz (unified pre-exercise modal)
  const handleStartQuiz = (comp: Competency) => {
    launchSession('quiz', comp, false);
  };

  // Launch Unit Test (unified pre-exercise modal)
  const handleStartUnitTest = (comp: Competency) => {
    launchSession('test', comp, false);
  };

  // Open Course Challenge screen
  const handleOpenCourseChallenge = () => {
    navigateView('challenge');
  };

  // Start Examen Modo Hierro directly after briefing screen
  const handleBeginCourseChallenge = () => {
    launchSession('challenge', null, true);
  };

  // Start M14-B Adaptive 2-Module Exam inside Modo Hierro
  const handleBeginAdaptiveChallenge = () => {
    if (!activeCourse) return;
    clearActiveSession();
    setRestoredSnapshot(null);
    setIronOutcome(null);
    setAdaptiveSummary(null);
    setSessionCompetency(null);
    setFocusCompetencyId(null);
    setSessionType('challenge');

    const mod1Questions = buildAdaptiveModule1(activeCourse, 12);
    if (mod1Questions.length === 0) {
      setSessionQuestions([]);
      return;
    }
    setAdaptiveExamState({
      phase: 'module1',
      mod1Questions,
    });
    setSessionQuestions(mod1Questions);
    setSessionKey((prev) => prev + 1);
    const shouldReplace = viewMode === 'pre_exercise' || viewMode === 'completed';
    navigateView('practice', { replace: shouldReplace });
  };

  const handleStartAdaptiveModule2 = () => {
    if (!adaptiveExamState?.mod2Questions || adaptiveExamState.mod2Questions.length === 0) return;
    setAdaptiveExamState((prev) => (prev ? { ...prev, phase: 'module2' } : null));
    setSessionQuestions(adaptiveExamState.mod2Questions);
    setSessionKey((prev) => prev + 1);
  };

  // Safe quit from session: replaces current transient state with overview so back never re-enters quizzes
  const handleQuitSession = () => {
    clearActiveSession();
    setRestoredSnapshot(null);
    setIronOutcome(null);
    setAdaptiveExamState(null);
    setAdaptiveSummary(null);
    setShowQuitConfirm(false);
    setFocusCompetencyId(sessionType === 'challenge' ? null : sessionCompetency?.id ?? null);
    setViewMode('overview');
    replaceNavState({
      viewMode: 'overview',
      courseId: activeCourse?.course_id,
    });
  };

  const buildM22AttemptEvents = (
    course: Course,
    telemetryList: QuestionTelemetry[],
    questionsList: Question[],
    tierSnapshotBefore: Record<string, MasteryTier>,
    mode: SessionType | 'iron_exam'
  ): M22AttemptEvent[] => {
    const qById = new Map<string, Question>();
    for (const q of course.questions) qById.set(q.id, q);
    for (const q of questionsList) qById.set(q.id, q);
    const nowIso = new Date().toISOString();
    const isProbe = mode === 'cold_transfer_probe';

    return telemetryList.map((t, idx) => {
      const q = qById.get(t.question_id);
      const cid = t.competency_id || q?.competency_id || 'unknown';
      const wrongAttempts = Math.max(0, t.wrong_attempts ?? (t.is_correct ? 0 : 1));
      const hintsUsed = Math.max(0, t.hints_used ?? 0);
      return {
        id: `m22_${Date.now()}_${idx}_${Math.random().toString(36).slice(2, 8)}`,
        timestamp: nowIso,
        course_id: course.course_id,
        competency_id: cid,
        question_id: t.question_id,
        ...(q?.archetype ? { archetype: q.archetype } : {}),
        modality: t.question_type || q?.type || 'multiple_choice_7_options',
        ...(q?.difficulty ? { difficulty: q.difficulty } : {}),
        mastery_tier_before: tierSnapshotBefore[cid] ?? 'Not started',
        session_mode: mode,
        is_unlabeled_probe: isProbe,
        first_attempt_correct: Boolean(t.is_correct) && wrongAttempts === 0,
        final_correct: Boolean(t.is_correct),
        wrong_attempts: wrongAttempts,
        exhausted_4_strikes: wrongAttempts >= 4,
        hints_used: hintsUsed,
        triggered_distractor_ids: Array.from(new Set(t.matched_distractor_ids || [])),
        seconds_spent: Math.max(0, t.seconds_spent ?? 0),
      };
    });
  };

  // Handle Practice / Iron Exam Session Completion with Milestone 14, 14-B & 20 Telemetry
  const handleCompleteSession = (
    score: number,
    total: number,
    telemetryData?: QuestionTelemetry[],
    totalSeconds?: number,
    ironOutcomeParam?: IronExamCompletionOutcome
  ) => {
    clearActiveSession();
    setRestoredSnapshot(null);
    const sec = totalSeconds ?? 0;

    // M22 Phase 0: Snapshot mastery_tier_before BEFORE any masteryStorage mutation
    const tierSnapshotBefore: Record<string, MasteryTier> = {};
    if (activeCourse) {
      for (const comp of activeCourse.competencies) {
        tierSnapshotBefore[comp.id] = mastery?.competencies?.[comp.id]?.status ?? 'Not started';
      }
    }

    // M14-B Module 1 -> Routing Gate -> Module 2
    if (sessionType === 'challenge' && activeCourse && adaptiveExamState?.phase === 'module1') {
      const mod1Pct = total > 0 ? Math.round((score / total) * 100) : 0;
      const mod1Result: AdaptiveModuleResult = {
        moduleIndex: 1,
        tier: 'diagnostic',
        score,
        total,
        percentage: mod1Pct,
        elapsedSeconds: sec,
      };
      const usedIds = new Set(adaptiveExamState.mod1Questions.map((q) => q.id));
      const missedCompIds = new Set(
        (telemetryData || []).filter((t) => !t.is_correct).map((t) => t.competency_id)
      );
      const mod2Plan = buildAdaptiveModule2(activeCourse, mod1Pct, usedIds, missedCompIds, 12);
      setAdaptiveExamState({
        phase: 'routing',
        mod1Questions: adaptiveExamState.mod1Questions,
        mod1Result,
        mod1Outcome: ironOutcomeParam,
        mod1Telemetry: telemetryData || [],
        mod2Tier: mod2Plan.tier,
        mod2Questions: mod2Plan.questions,
      });
      return;
    }

    // M14-B Module 2 Completion -> Merge Module 1 + Module 2 & Compute University Projection
    if (
      sessionType === 'challenge' &&
      activeCourse &&
      adaptiveExamState?.phase === 'module2' &&
      adaptiveExamState.mod1Result
    ) {
      const mod2Tier = adaptiveExamState.mod2Tier || 'standard';
      const mod2Pct = total > 0 ? Math.round((score / total) * 100) : 0;
      const mod2Result: AdaptiveModuleResult = {
        moduleIndex: 2,
        tier: mod2Tier,
        score,
        total,
        percentage: mod2Pct,
        elapsedSeconds: sec,
      };
      const combinedTelemetry = [
        ...(adaptiveExamState.mod1Telemetry || []),
        ...(telemetryData || []),
      ];
      const combinedQuestions = [
        ...adaptiveExamState.mod1Questions,
        ...sessionQuestions,
      ];
      const mod1Outcome = adaptiveExamState.mod1Outcome;
      let mergedOutcome: IronExamCompletionOutcome | null = ironOutcomeParam ?? mod1Outcome ?? null;
      if (mod1Outcome && ironOutcomeParam) {
        const mergedItems = [
          ...mod1Outcome.metacognitiveAudit.items,
          ...ironOutcomeParam.metacognitiveAudit.items,
        ];
        const totalItems = Math.max(1, mergedItems.length);
        const calCount = mergedItems.filter((i) => i.quadrant === 'calibrated_mastery').length;
        const knownGaps = mergedItems.filter((i) => i.quadrant === 'known_gap').length;
        const mergedAudit: MetacognitiveAudit = {
          global_confidence: ironOutcomeParam.metacognitiveAudit.global_confidence,
          total_questions: mergedItems.length,
          answered_count:
            mod1Outcome.metacognitiveAudit.answered_count +
            ironOutcomeParam.metacognitiveAudit.answered_count,
          correct_count:
            mod1Outcome.metacognitiveAudit.correct_count +
            ironOutcomeParam.metacognitiveAudit.correct_count,
          calibrated_mastery_count: calCount,
          illusions_of_competence_count:
            mod1Outcome.metacognitiveAudit.illusions_of_competence_count +
            ironOutcomeParam.metacognitiveAudit.illusions_of_competence_count,
          lucky_guesses_count:
            mod1Outcome.metacognitiveAudit.lucky_guesses_count +
            ironOutcomeParam.metacognitiveAudit.lucky_guesses_count,
          known_gaps_count: knownGaps,
          calibration_score: Math.round(((calCount + knownGaps) / totalItems) * 100),
          items: mergedItems,
        };
        mergedOutcome = {
          metacognitiveAudit: mergedAudit,
          deferredReview: [...mod1Outcome.deferredReview, ...ironOutcomeParam.deferredReview],
        };
      }

      const combinedScore = adaptiveExamState.mod1Result.score + score;
      const combinedTotal = adaptiveExamState.mod1Result.total + total;
      const combinedSeconds = adaptiveExamState.mod1Result.elapsedSeconds + sec;

      if (combinedTelemetry.length > 0) {
        appendM22Events(
          buildM22AttemptEvents(
            activeCourse,
            combinedTelemetry,
            combinedQuestions,
            tierSnapshotBefore,
            'iron_exam'
          )
        );
      }

      const summary = updateCourseChallengeWithSkillCalibration(
        activeCourse,
        combinedTelemetry,
        combinedSeconds
      );
      const adaptiveReport = computeAdaptiveExamSummary(
        activeCourse,
        adaptiveExamState.mod1Result,
        mod2Result,
        combinedTelemetry,
        combinedQuestions
      );

      setIronOutcome(mergedOutcome);
      setAdaptiveSummary(adaptiveReport);
      setAdaptiveExamState(null);
      setSessionScore(combinedScore);
      setSessionTotal(combinedTotal);
      setMastery({ ...summary.record });
      setChallengeSummary(summary);
      setLatestTimingData({
        totalSeconds: summary.total_seconds,
        avgSeconds: summary.avg_seconds_per_question,
        isNewRecord: summary.is_new_record,
      });
      setLatestMisconceptions(summary.misconceptions);
      navigateView('completed', { replace: true });
      return;
    }

    setAdaptiveSummary(null);
    setAdaptiveExamState(null);
    setIronOutcome(sessionType === 'challenge' ? (ironOutcomeParam ?? null) : null);
    setSessionScore(score);
    setSessionTotal(total);

    if (activeCourse) {
      if (telemetryData && telemetryData.length > 0) {
        appendM22Events(
          buildM22AttemptEvents(
            activeCourse,
            telemetryData,
            sessionQuestions,
            tierSnapshotBefore,
            sessionType === 'challenge' ? 'iron_exam' : sessionType
          )
        );
      }

      if (
        (sessionType === 'challenge' ||
          sessionType === 'mastery_challenge' ||
          sessionType === 'misconception_drill') &&
        telemetryData &&
        telemetryData.length > 0
      ) {
        const summary = updateSessionWithCrossSkillCalibration(
          activeCourse,
          telemetryData,
          sec,
          sessionType
        );
        setMastery({ ...summary.record });
        setChallengeSummary(summary);
        setLatestTimingData({
          totalSeconds: summary.total_seconds,
          avgSeconds: summary.avg_seconds_per_question,
          isNewRecord: summary.is_new_record,
        });
        setLatestMisconceptions(summary.misconceptions);
      } else if (sessionCompetency) {
        const distinctCompIds = new Set(
          (telemetryData || []).map((t) => t.competency_id).filter(Boolean)
        );
        const isInterleavedMultiSkill =
          (sessionType === 'quiz' || sessionType === 'test') && distinctCompIds.size > 1;
        const prevTier = mastery?.competencies?.[sessionCompetency.id]?.status;

        if (telemetryData && telemetryData.length > 0) {
          const summary = updateSessionWithCrossSkillCalibration(
            activeCourse,
            telemetryData,
            sec,
            sessionType,
            { targetCompetencyId: sessionCompetency.id }
          );
          const nextTier = summary.record.competencies[sessionCompetency.id]?.status;
          setMastery({ ...summary.record });
          setChallengeSummary(isInterleavedMultiSkill ? summary : null);
          setLatestTimingData({
            totalSeconds: summary.total_seconds,
            avgSeconds: summary.avg_seconds_per_question,
            isNewRecord: summary.is_new_record,
            previousTier: prevTier,
            newTier: nextTier,
          });
          setLatestMisconceptions(summary.misconceptions);
        } else {
          setChallengeSummary(null);
          const hints = (telemetryData || []).reduce((acc, t) => acc + t.hints_used, 0);
          const updated = updateCompetencyScore(
            activeCourse,
            sessionCompetency.id,
            score,
            total,
            sessionType,
            { totalSeconds: sec, hintsUsed: hints },
            telemetryData
          );
          setMastery({ ...updated });
          setLatestTimingData({
            totalSeconds: updated.totalSeconds,
            avgSeconds: updated.avgSeconds,
            isNewRecord: updated.isNewRecord,
            previousTier: updated.previousTier,
            newTier: updated.newTier,
          });
          setLatestMisconceptions([]);
        }
      } else if (sessionType === 'cold_transfer_probe') {
        setChallengeSummary(null);
        setLatestTimingData({
          totalSeconds: sec,
          avgSeconds: total > 0 ? sec / total : 0,
        });
        setLatestMisconceptions([]);
      }
    }

    // Replace practice with completed so you cannot back into questions
    navigateView('completed', { replace: true });
  };

  // Handle "Try again" from Completion - preserves sessionType and performs fresh reshuffle directly
  const handleTryAgain = () => {
    if (!activeCourse) return;
    if (sessionType === 'challenge' && adaptiveSummary) {
      handleBeginAdaptiveChallenge();
      return;
    }
    if (
      sessionType === 'mastery_challenge' ||
      sessionType === 'misconception_drill' ||
      sessionType === 'cold_transfer_probe'
    ) {
      launchSession(sessionType, null, true);
      return;
    }
    let targetComp = sessionCompetency;
    if (!targetComp && sessionType !== 'challenge' && sessionQuestions.length > 0) {
      const qCompId = sessionQuestions[0].competency_id;
      targetComp = activeCourse.competencies.find((c) => c.id === qCompId) || null;
    }
    launchSession(sessionType, targetComp, true);
  };

  // Handle "Up next" from Completion
  const handleUpNext = () => {
    if (
      !activeCourse ||
      !sessionCompetency ||
      sessionType === 'mastery_challenge' ||
      sessionType === 'misconception_drill' ||
      sessionType === 'cold_transfer_probe' ||
      sessionType === 'challenge'
    ) {
      navigateView('overview');
      return;
    }

    const currentIdx = activeCourse.competencies.findIndex(
      (c) => c.id === sessionCompetency.id
    );
    if (currentIdx >= 0 && currentIdx < activeCourse.competencies.length - 1) {
      const nextComp = activeCourse.competencies[currentIdx + 1];
      if (sessionType === 'quiz' || sessionType === 'test') {
        launchSession(sessionType, nextComp, true);
      } else {
        handleStartPractice(nextComp);
      }
    } else {
      setFocusCompetencyId(sessionCompetency.id);
      navigateView('overview');
    }
  };

  return (
    <div className="min-h-screen bg-ka-bg-canvas text-ka-text-primary flex flex-col font-sans">
      <ShortcutHelp />
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
            isProgressLogActive={false}
            activeMisconceptionCount={getActiveMisconceptions(mastery ?? undefined).length}
            onSelectUnit={(idx) => {
              setSelectedUnitIndex(idx);
              handleStartPractice(activeCourse.competencies[idx]);
            }}
            onSelectProgressLog={handleOpenProgressLog}
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
              focusCompetencyId={focusCompetencyId}
              onStartPractice={handleStartPractice}
              onStartQuiz={handleStartQuiz}
              onStartUnitTest={handleStartUnitTest}
              onStartCourseChallenge={handleOpenCourseChallenge}
              onStartMasteryChallenge={handleStartMasteryChallenge}
              onStartMisconceptionDrill={handleStartMisconceptionDrill}
              onStartColdTransferProbe={handleStartColdTransferProbe}
              onOpenProgressLog={handleOpenProgressLog}
            />
          </main>
        </div>
      )}

      {viewMode === 'progress_log' && activeCourse && mastery && (
        <div className="flex min-h-screen">
          <Sidebar
            course={activeCourse}
            mastery={mastery}
            selectedUnitIndex={null}
            isCourseChallengeActive={false}
            isProgressLogActive={true}
            activeMisconceptionCount={getActiveMisconceptions(mastery ?? undefined).length}
            onSelectUnit={(idx) => {
              setSelectedUnitIndex(idx);
              setFocusCompetencyId(activeCourse.competencies[idx]?.id ?? null);
              navigateView('overview');
            }}
            onSelectProgressLog={() => {}}
            onSelectCourseChallenge={handleOpenCourseChallenge}
            onBackToLibrary={() => {
              setActiveCourse(null);
              navigateView('library');
            }}
          />
          <main className="flex-1 min-w-0 overflow-y-auto pt-14 lg:pt-0">
            <ProgressLogView
              course={activeCourse}
              mastery={mastery}
              onBackToCourse={() => navigateView('overview')}
              onStartMasteryChallenge={handleStartMasteryChallenge}
              onStartMisconceptionDrill={handleStartMisconceptionDrill}
              onStartColdTransferProbe={handleStartColdTransferProbe}
            />
          </main>
        </div>
      )}

      {viewMode === 'pre_exercise' && (
        <PreExerciseModal
          sessionType={sessionType}
          competency={sessionCompetency}
          questionCount={sessionQuestions.length}
          courseTitle={activeCourse?.title}
          timingRecord={
            sessionType === 'challenge'
              ? (activeCourse ? getTimingForChallenge(activeCourse.course_id) : undefined)
              : (activeCourse && sessionCompetency
                  ? getTimingForCompetency(
                      activeCourse.course_id,
                      sessionCompetency.id,
                      sessionType as 'practice' | 'quiz' | 'test'
                    )
                  : undefined)
          }
          onStart={handleBeginPracticeSession}
          onBack={() => {
            setFocusCompetencyId(sessionCompetency?.id ?? null);
            navigateView(sessionType === 'challenge' ? 'challenge' : 'overview');
          }}
        />
      )}

      {viewMode === 'practice' && sessionType === 'challenge' && adaptiveExamState?.phase === 'routing' && (
        <div className="min-h-screen flex items-center justify-center bg-slate-950 p-4 sm:p-6">
          <div
            data-testid="adaptive-routing-card"
            className="w-full max-w-xl bg-slate-900 text-white rounded-2xl border border-indigo-500/40 shadow-2xl p-6 sm:p-8 text-center space-y-5"
          >
            <span className="inline-block px-3 py-1 rounded-full bg-indigo-500/30 border border-indigo-400/40 text-indigo-200 text-xs font-extrabold uppercase tracking-wider">
              Enrutamiento Adaptativo • Corte 70%
            </span>
            <h2 className="text-2xl sm:text-3xl font-extrabold">
              Módulo 1 Completado: {adaptiveExamState.mod1Result?.percentage ?? 0}%
            </h2>
            <p className="text-sm text-slate-300 leading-relaxed">
              Obtuviste{' '}
              <strong>
                {adaptiveExamState.mod1Result?.score}/{adaptiveExamState.mod1Result?.total}
              </strong>{' '}
              aciertos.{' '}
              {adaptiveExamState.mod2Tier === 'advanced' ? (
                <>
                  Superaste el corte de 70% y avanzas al{' '}
                  <span className="text-purple-300 font-bold">Módulo 2 Avanzado</span> (ZPD experto,
                  escala hasta 20/20).
                </>
              ) : (
                <>
                  Tu desempeño (&lt; 70%) te enruta al{' '}
                  <span className="text-sky-300 font-bold">Módulo 2 Estándar</span> (consolidación
                  y refuerzo de brechas detectadas).
                </>
              )}
            </p>
            <div className="flex items-center justify-center gap-3 pt-2">
              <button
                type="button"
                onClick={handleQuitSession}
                className="px-4 py-2.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs sm:text-sm font-bold cursor-pointer"
              >
                Salir
              </button>
              <button
                type="button"
                data-testid="start-adaptive-module2-btn"
                onClick={handleStartAdaptiveModule2}
                className={`px-6 py-2.5 rounded-lg text-white text-sm font-bold shadow-md cursor-pointer ${
                  adaptiveExamState.mod2Tier === 'advanced'
                    ? 'bg-purple-600 hover:bg-purple-700'
                    : 'bg-sky-600 hover:bg-sky-700'
                }`}
              >
                Iniciar Módulo 2 ({adaptiveExamState.mod2Tier === 'advanced' ? 'Avanzado' : 'Estándar'}) ➔
              </button>
            </div>
          </div>
        </div>
      )}

      {viewMode === 'practice' && sessionType === 'challenge' && adaptiveExamState?.phase !== 'routing' && (
        <IronExamSession
          key={sessionKey}
          sessionTitle={
            restoredSnapshot?.sessionTitle ||
            (adaptiveExamState
              ? `Simulador Parcial • ${activeCourse?.title || 'Curso'}`
              : `Examen Modo Hierro • ${activeCourse?.title || 'Curso'}`)
          }
          questions={sessionQuestions}
          courseId={activeCourse?.course_id}
          courseTitle={activeCourse?.title}
          moduleIndex={
            adaptiveExamState?.phase === 'module2'
              ? 2
              : adaptiveExamState?.phase === 'module1'
              ? 1
              : undefined
          }
          moduleTier={
            adaptiveExamState?.phase === 'module2'
              ? adaptiveExamState.mod2Tier || 'standard'
              : adaptiveExamState?.phase === 'module1'
              ? 'diagnostic'
              : undefined
          }
          timeLimitSeconds={
            adaptiveExamState ? Math.max(180, sessionQuestions.length * 90) : undefined
          }
          submitButtonLabel={
            adaptiveExamState?.phase === 'module1' ? 'Finalizar Módulo 1' : undefined
          }
          persistSession={!adaptiveExamState}
          initialSnapshot={restoredSnapshot}
          onComplete={handleCompleteSession}
          onQuit={() => setShowQuitConfirm(true)}
        />
      )}

      {viewMode === 'practice' && sessionType !== 'challenge' && (
        <PracticeSession
          key={sessionKey}
          sessionTitle={
            restoredSnapshot?.sessionTitle ||
            (sessionType === 'cold_transfer_probe'
              ? 'Sonda de Transferencia Fría (Sin Etiqueta)'
              : sessionType === 'mastery_challenge'
              ? `Mastery Challenge • ${activeCourse?.title || 'Curso'}`
              : sessionType === 'misconception_drill'
              ? `Practicar mis Trampas • ${activeCourse?.title || 'Curso'}`
              : sessionType === 'quiz'
              ? `Quiz • ${sessionCompetency?.name || 'Unit'}`
              : sessionType === 'test'
              ? `Unit test • ${sessionCompetency?.name || 'Unit'}`
              : sessionCompetency?.name || 'Practice')
          }
          sessionType={sessionType}
          isColdTransferProbe={sessionType === 'cold_transfer_probe'}
          questions={sessionQuestions}
          courseId={activeCourse?.course_id}
          competencyId={sessionCompetency?.id ?? null}
          unitIndex={selectedUnitIndex}
          initialSnapshot={restoredSnapshot}
          onRestart={() => {
            clearActiveSession();
            setRestoredSnapshot(null);
            launchSession(sessionType, sessionCompetency, true);
          }}
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
          challengeSummary={challengeSummary}
          adaptiveSummary={adaptiveSummary}
          metacognitiveAudit={ironOutcome?.metacognitiveAudit}
          deferredReview={ironOutcome?.deferredReview}
          timingData={latestTimingData}
          misconceptions={latestMisconceptions}
          onRemediateCompetency={(comp) => {
            launchSession('practice', comp, true);
          }}
          onTryAgain={handleTryAgain}
          onUpNext={handleUpNext}
          onBackToCourse={() => {
            if (sessionCompetency && activeCourse) {
              const idx = activeCourse.competencies.findIndex((c) => c.id === sessionCompetency.id);
              if (idx >= 0) setSelectedUnitIndex(idx);
            }
            setFocusCompetencyId(sessionType === 'challenge' ? null : sessionCompetency?.id ?? null);
            navigateView('overview');
          }}
        />
      )}

      {viewMode === 'challenge' && activeCourse && (
        <div className="flex min-h-screen">
          <Sidebar
            course={activeCourse}
            mastery={mastery}
            selectedUnitIndex={null}
            isCourseChallengeActive={true}
            isProgressLogActive={false}
            activeMisconceptionCount={getActiveMisconceptions(mastery ?? undefined).length}
            onSelectUnit={(idx) => {
              setSelectedUnitIndex(idx);
              navigateView('overview');
            }}
            onSelectProgressLog={handleOpenProgressLog}
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
              onStartAdaptive={handleBeginAdaptiveChallenge}
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
      <dialog
        ref={quitDialogRef}
        onCancel={(e) => {
          e.preventDefault();
          handleQuitSession();
        }}
        onClick={(e) => {
          if (e.target === e.currentTarget) setShowQuitConfirm(false);
        }}
        aria-labelledby="quit-dialog-title"
        data-testid="quit-confirm-modal"
        className="m-auto w-[calc(100%-2rem)] max-w-sm bg-white rounded-2xl p-6 shadow-2xl text-center border border-slate-200 backdrop:bg-black/60 backdrop:backdrop-blur-sm"
      >
        {showQuitConfirm && (
          <div>
            <div className="w-12 h-12 rounded-full bg-amber-100 text-amber-600 flex items-center justify-center mx-auto mb-4 text-2xl font-bold">
              ⚠️
            </div>
            <h3 id="quit-dialog-title" className="text-lg font-bold text-ka-text-primary mb-2">
              ¿Deseas salir de la sesión?
            </h3>
            <p className="text-sm text-ka-text-secondary mb-6 leading-relaxed">
              El progreso actual de esta práctica o examen no se guardará si decides salir ahora.
            </p>
            <p className="text-xs text-slate-500 -mt-4 mb-5">
              Press <kbd className="px-1 font-bold bg-slate-100 border border-slate-300 rounded">Esc</kbd> again to exit.
            </p>
            <div className="flex gap-3">
              <button
                type="button"
                autoFocus
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
        )}
      </dialog>
    </div>
  );
};
export default App;
