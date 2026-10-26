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
} from './utils/courseLoader';
import { Sidebar } from './components/Sidebar';
import { CourseOverview } from './components/CourseOverview';
import { PreExerciseModal } from './components/PreExerciseModal';
import { PracticeSession } from './components/PracticeSession';
import { CompletionScreen } from './components/CompletionScreen';
import { CourseChallenge } from './components/CourseChallenge';
import { CourseLibrary } from './components/CourseLibrary';

type ViewMode =
  | 'library'
  | 'overview'
  | 'pre_exercise'
  | 'practice'
  | 'completed'
  | 'challenge';

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

  const [activeCourse, setActiveCourse] = useState<Course | null>(null);
  const [mastery, setMastery] = useState<CourseMasteryRecord | null>(null);

  const [viewMode, setViewMode] = useState<ViewMode>('library');
  const [selectedUnitIndex, setSelectedUnitIndex] = useState<number | null>(null);

  // Active session parameters
  const [sessionCompetency, setSessionCompetency] = useState<Competency | null>(null);
  const [sessionType, setSessionType] = useState<'practice' | 'quiz' | 'test' | 'challenge'>('practice');
  const [sessionQuestions, setSessionQuestions] = useState<Question[]>([]);
  const [sessionScore, setSessionScore] = useState(0);
  const [sessionTotal, setSessionTotal] = useState(0);
  const [sessionKey, setSessionKey] = useState(0);

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
        setViewMode('overview');
      }
    } catch (err) {
      console.error(`Failed to load course ${summary.id}:`, err);
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
      setViewMode('practice');
    } else {
      setViewMode('pre_exercise');
    }
  };

  // Launch Practice Pre-Exercise
  const handleStartPractice = (comp: Competency) => {
    launchSession('practice', comp, false);
  };

  // Start Practice from Pre-Exercise Modal
  const handleBeginPracticeSession = () => {
    setViewMode('practice');
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
    setViewMode('challenge');
  };

  // Start Course Challenge Session
  const handleBeginCourseChallenge = () => {
    launchSession('challenge', null, true);
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

    setViewMode('completed');
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
      setViewMode('overview');
      return;
    }

    const currentIdx = activeCourse.competencies.findIndex(
      (c) => c.id === sessionCompetency.id
    );
    if (currentIdx >= 0 && currentIdx < activeCourse.competencies.length - 1) {
      const nextComp = activeCourse.competencies[currentIdx + 1];
      handleStartPractice(nextComp);
    } else {
      setViewMode('overview');
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
        />
      )}

      {viewMode === 'overview' && activeCourse && mastery && (
        <div className="flex min-h-screen">
          <Sidebar
            course={activeCourse}
            selectedUnitIndex={selectedUnitIndex}
            isCourseChallengeActive={false}
            onSelectUnit={(idx) => {
              setSelectedUnitIndex(idx);
              handleStartPractice(activeCourse.competencies[idx]);
            }}
            onSelectCourseChallenge={handleOpenCourseChallenge}
            onBackToLibrary={() => {
              setActiveCourse(null);
              setViewMode('library');
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
          onBack={() => setViewMode('overview')}
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
          onQuit={() => setViewMode('overview')}
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
            selectedUnitIndex={null}
            isCourseChallengeActive={true}
            onSelectUnit={(idx) => {
              setSelectedUnitIndex(idx);
              setViewMode('overview');
            }}
            onSelectCourseChallenge={() => {}}
            onBackToLibrary={() => {
              setActiveCourse(null);
              setViewMode('library');
            }}
          />
          <main className="flex-1 min-w-0 overflow-y-auto pt-14 lg:pt-0">
            <CourseChallenge
              course={activeCourse}
              totalQuestions={Math.min(30, activeCourse.questions.length)}
              onStart={handleBeginCourseChallenge}
              onBack={() => setViewMode('overview')}
            />
          </main>
        </div>
      )}
    </div>
  );
};
export default App;
