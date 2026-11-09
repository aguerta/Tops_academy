import {
  Course,
  CourseMasteryRecord,
  CompetencyMastery,
  MasteryTier,
  UnitTestRecord,
  CourseProgressDetails,
  CourseProgressStatus,
  TimingStats,
  QuestionTelemetry,
  ChallengeSkillResult,
  ChallengeExecutionSummary,
} from '../types';

const STORAGE_KEY = 'tops_academic_progress_v1';
const LEGACY_STORAGE_KEY = 'khan_academic_progress_v1';

export const TIER_POINTS: Record<MasteryTier, number> = {
  'Not started': 0,
  'Attempted': 25,
  'Familiar': 50,
  'Proficient': 80,
  'Mastered': 100,
};

export const TIER_COLORS: Record<MasteryTier, { bg: string; border: string; text: string }> = {
  'Mastered': { bg: '#583b8b', border: '#583b8b', text: '#ffffff' },
  'Proficient': { bg: '#8377b2', border: '#8377b2', text: '#ffffff' },
  'Familiar': { bg: '#e07a21', border: '#e07a21', text: '#ffffff' },
  'Attempted': { bg: '#ffffff', border: '#f3801e', text: '#f3801e' },
  'Not started': { bg: '#ffffff', border: '#88939e', text: '#88939e' },
};

export function formatTimingSeconds(seconds?: number): string {
  if (seconds === undefined || seconds === null || isNaN(seconds)) return '--';
  if (seconds < 60) return `${seconds}s`;
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return secs === 0 ? `${mins}m` : `${mins}m ${secs}s`;
}

export function getTierDowngrade(tier: MasteryTier): MasteryTier {
  switch (tier) {
    case 'Mastered':
      return 'Proficient';
    case 'Proficient':
      return 'Familiar';
    case 'Familiar':
      return 'Attempted';
    case 'Attempted':
      return 'Attempted';
    case 'Not started':
    default:
      return 'Attempted';
  }
}

export function calculateTierTransition(
  prevTier: MasteryTier,
  score: number,
  total: number,
  sessionType: 'practice' | 'quiz' | 'test' | 'challenge',
  hintsUsed: number = 0
): MasteryTier {
  if (total <= 0) return prevTier;
  const ratio = score / total;
  const isHintCapped = hintsUsed >= 2;

  // Single question evaluation (Course Challenge slice or single item)
  if (total === 1) {
    if (score === 0) {
      // Degradación obligatoria ante fallo individual
      return getTierDowngrade(prevTier);
    }
    // Acierto (score === 1)
    if (isHintCapped) {
      if (prevTier === 'Not started' || prevTier === 'Attempted') {
        return 'Familiar';
      }
      return prevTier; // Capped at Familiar
    }
    switch (prevTier) {
      case 'Not started':
        return 'Familiar'; // Aceleración diagnóstica
      case 'Attempted':
        return 'Familiar';
      case 'Familiar':
        return 'Proficient';
      case 'Proficient':
        return sessionType === 'test' ? 'Mastered' : 'Proficient';
      case 'Mastered':
        return 'Mastered';
    }
  }

  // Multi-question evaluation
  if (ratio >= 0.8) {
    if (isHintCapped) {
      if (prevTier === 'Not started' || prevTier === 'Attempted') {
        return 'Familiar';
      }
      return prevTier;
    }
    if (sessionType === 'test') {
      if (ratio === 1) return 'Mastered';
      return 'Proficient';
    }
    if (sessionType === 'challenge') {
      if (ratio === 1 && prevTier === 'Proficient') return 'Mastered';
      if (prevTier === 'Mastered') return 'Mastered';
      if (prevTier === 'Not started') return 'Familiar';
      return 'Proficient';
    }
    // Practice or quiz
    if (ratio === 1) {
      return prevTier === 'Mastered' ? 'Mastered' : 'Proficient';
    }
    return prevTier === 'Not started' || prevTier === 'Attempted' ? 'Familiar' : prevTier;
  }

  if (ratio >= 0.5) {
    // Si estaba en Mastered, cualquier error en evaluación acumulativa degrada a Proficient
    if (prevTier === 'Mastered') {
      return 'Proficient';
    }
    if (prevTier === 'Not started') {
      return 'Attempted';
    }
    return prevTier;
  }

  // ratio < 0.5: Degradación estricta de 1 nivel hacia abajo
  return getTierDowngrade(prevTier);
}

function getAllStoredData(): Record<string, CourseMasteryRecord> {
  try {
    const raw = localStorage.getItem(STORAGE_KEY) || localStorage.getItem(LEGACY_STORAGE_KEY);
    if (!raw) return {};
    return JSON.parse(raw);
  } catch {
    return {};
  }
}

function saveAllStoredData(data: Record<string, CourseMasteryRecord>) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  } catch (err) {
    console.error('Failed to save mastery data to localStorage', err);
  }
}

export function loadCourseMastery(course: Course): CourseMasteryRecord {
  const all = getAllStoredData();
  const existing = all[course.course_id];

  if (existing) {
    // Ensure all competencies exist in the record
    course.competencies.forEach((c) => {
      if (!existing.competencies[c.id]) {
        existing.competencies[c.id] = {
          status: 'Not started',
          points: 0,
          last_practiced: new Date().toISOString(),
          history: [],
        };
      }
    });
    return existing;
  }

  // Initialize fresh record
  const initialComp: Record<string, CompetencyMastery> = {};
  course.competencies.forEach((c) => {
    initialComp[c.id] = {
      status: 'Not started',
      points: 0,
      last_practiced: new Date().toISOString(),
      history: [],
    };
  });

  const record: CourseMasteryRecord = {
    course_id: course.course_id,
    mastery_points: 0,
    competencies: initialComp,
  };

  all[course.course_id] = record;
  saveAllStoredData(all);
  return record;
}

export function updateCompetencyScore(
  course: Course,
  competencyId: string,
  score: number,
  total: number,
  sessionType: 'practice' | 'quiz' | 'test' | 'challenge',
  timingData?: { totalSeconds: number; hintsUsed?: number },
  questionTelemetries?: QuestionTelemetry[]
): CourseMasteryRecord & {
  isNewRecord?: boolean;
  previousTier?: MasteryTier;
  newTier?: MasteryTier;
  totalSeconds?: number;
  avgSeconds?: number;
} {
  const all = getAllStoredData();
  const record = loadCourseMastery(course);

  const prev = record.competencies[competencyId] || {
    status: 'Not started',
    points: 0,
    last_practiced: new Date().toISOString(),
    history: [],
  };

  const ratio = total > 0 ? score / total : 0;
  const percentage = Math.round(ratio * 100);
  const hintsUsed = timingData?.hintsUsed ?? 0;
  const previousTier = prev.status;
  const newTier = calculateTierTransition(previousTier, score, total, sessionType, hintsUsed);

  let unitTestRecord: UnitTestRecord | undefined = prev.unit_test;
  if (sessionType === 'test') {
    unitTestRecord = {
      last_score: score,
      total_questions: total,
      percentage,
      completed_at: new Date().toISOString(),
    };
  }

  // Timing recording
  const rawSec = timingData?.totalSeconds ?? 0;
  const safeTotalSeconds = Math.min(rawSec, Math.max(1, total) * 300);
  const avgSeconds = total > 0 ? Math.round(safeTotalSeconds / total) : 0;
  let isNewRecord = false;

  const timing = prev.timing ? { ...prev.timing } : {};
  if (sessionType !== 'challenge') {
    const currentTiming = timing[sessionType] ? { ...timing[sessionType] } : {};
    // Only update best time in sessions with 100% approval
    if (total > 0 && score === total) {
      if (
        currentTiming.best_avg_seconds_per_question === undefined ||
        avgSeconds < currentTiming.best_avg_seconds_per_question
      ) {
        currentTiming.best_avg_seconds_per_question = avgSeconds;
        currentTiming.best_total_seconds = safeTotalSeconds;
        isNewRecord = true;
      }
    }
    currentTiming.last_avg_seconds_per_question = avgSeconds;
    currentTiming.last_total_seconds = safeTotalSeconds;
    timing[sessionType] = currentTiming;
  }

  // Needs review & Misconceptions:
  let needsReview = prev.needs_review || false;
  let recentMisconceptions = prev.recent_misconceptions ? [...prev.recent_misconceptions] : [];
  if (total > 0 && score < total) {
    needsReview = true;
    if (questionTelemetries && questionTelemetries.length > 0) {
      const failed = questionTelemetries.filter((t) => !t.is_correct);
      const newItems = failed.map((f) => ({
        date: new Date().toISOString(),
        question_id: f.question_id,
        concept_name: f.question_text || f.question_id,
      }));
      recentMisconceptions = [...recentMisconceptions, ...newItems].slice(-5);
    }
  } else if (total > 0 && score === total) {
    // 100% clean session heals the competency
    needsReview = false;
    recentMisconceptions = [];
  }

  record.competencies[competencyId] = {
    status: newTier,
    points: TIER_POINTS[newTier],
    last_practiced: new Date().toISOString(),
    unit_test: unitTestRecord,
    timing,
    needs_review: needsReview,
    recent_misconceptions: recentMisconceptions,
    history: [
      ...prev.history,
      {
        date: new Date().toISOString(),
        score,
        total,
        type: sessionType,
        total_seconds: safeTotalSeconds,
        avg_seconds_per_question: avgSeconds,
        previous_tier: previousTier,
        new_tier: newTier,
      },
    ],
  };

  // Recalculate total course progress using the 80/20 formula
  const progress = calculateCourseProgress(record, course.competencies.length);
  record.mastery_points = progress.percentage;

  all[course.course_id] = record;
  saveAllStoredData(all);

  return {
    ...record,
    isNewRecord,
    previousTier,
    newTier,
    totalSeconds: safeTotalSeconds,
    avgSeconds,
  };
}

export function updateCourseChallengeWithSkillCalibration(
  course: Course,
  telemetry: QuestionTelemetry[],
  totalSeconds: number
): ChallengeExecutionSummary {
  const all = getAllStoredData();
  const record = loadCourseMastery(course);

  const overallTotal = telemetry.length;
  const overallScore = telemetry.filter((t) => t.is_correct).length;
  const overallRatio = overallTotal > 0 ? overallScore / overallTotal : 0;
  const overallPercentage = Math.round(overallRatio * 100);
  const isCompleted = overallRatio === 1 && overallTotal > 0;

  // Group by competency_id
  const byComp: Record<
    string,
    { total: number; correct: number; hintsUsed: number; questions: QuestionTelemetry[] }
  > = {};
  for (const t of telemetry) {
    if (!byComp[t.competency_id]) {
      byComp[t.competency_id] = { total: 0, correct: 0, hintsUsed: 0, questions: [] };
    }
    byComp[t.competency_id].total++;
    if (t.is_correct) byComp[t.competency_id].correct++;
    byComp[t.competency_id].hintsUsed += t.hints_used;
    byComp[t.competency_id].questions.push(t);
  }

  const skillsLeveledUp: ChallengeSkillResult[] = [];
  const skillsLeveledDown: ChallengeSkillResult[] = [];
  const skillsMaintained: ChallengeSkillResult[] = [];
  const misconceptions: ChallengeExecutionSummary['misconceptions'] = [];

  for (const comp of course.competencies) {
    const compData = byComp[comp.id];
    if (!compData) continue;

    const prev = record.competencies[comp.id] || {
      status: 'Not started',
      points: 0,
      last_practiced: new Date().toISOString(),
      history: [],
    };
    const prevTier = prev.status;
    const newTier = calculateTierTransition(
      prevTier,
      compData.correct,
      compData.total,
      'challenge',
      compData.hintsUsed
    );

    const prevPoints = TIER_POINTS[prevTier];
    const newPoints = TIER_POINTS[newTier];
    const deltaPoints = newPoints - prevPoints;

    let direction: 'up' | 'down' | 'maintained' = 'maintained';
    if (deltaPoints > 0) direction = 'up';
    else if (deltaPoints < 0) direction = 'down';

    const skillResult: ChallengeSkillResult = {
      competency_id: comp.id,
      competency_name: comp.name,
      total_questions: compData.total,
      correct_questions: compData.correct,
      previous_tier: prevTier,
      new_tier: newTier,
      direction,
      delta_points: deltaPoints,
    };

    if (direction === 'up') skillsLeveledUp.push(skillResult);
    else if (direction === 'down') skillsLeveledDown.push(skillResult);
    else skillsMaintained.push(skillResult);

    // Collect misconceptions
    for (const q of compData.questions) {
      if (!q.is_correct) {
        misconceptions.push({
          question_id: q.question_id,
          competency_id: comp.id,
          competency_name: comp.name,
          text: q.question_text || q.question_id,
        });
      }
    }

    // Update competency record
    const hasErrors = compData.correct < compData.total;
    record.competencies[comp.id] = {
      ...prev,
      status: newTier,
      points: newPoints,
      last_practiced: new Date().toISOString(),
      needs_review: hasErrors ? true : prev.needs_review && direction === 'maintained',
      history: [
        ...prev.history,
        {
          date: new Date().toISOString(),
          score: compData.correct,
          total: compData.total,
          type: 'challenge',
          previous_tier: prevTier,
          new_tier: newTier,
        },
      ],
    };
  }

  // Update course challenge record & timing
  const prevCc = record.course_challenge;
  const timing: TimingStats = prevCc?.timing ? { ...prevCc.timing } : {};
  const safeTotalSeconds = Math.min(totalSeconds, Math.max(1, overallTotal) * 300);
  const avgSeconds = overallTotal > 0 ? Math.round(safeTotalSeconds / overallTotal) : 0;
  let isNewRecord = false;

  // Only update best time in sessions with 100% approval
  if (isCompleted) {
    if (
      timing.best_avg_seconds_per_question === undefined ||
      avgSeconds < timing.best_avg_seconds_per_question
    ) {
      timing.best_avg_seconds_per_question = avgSeconds;
      timing.best_total_seconds = safeTotalSeconds;
      isNewRecord = true;
    }
  }
  timing.last_avg_seconds_per_question = avgSeconds;
  timing.last_total_seconds = safeTotalSeconds;

  record.course_challenge = {
    completed: isCompleted,
    last_score: overallScore,
    total_questions: overallTotal,
    percentage: overallPercentage,
    completed_at: new Date().toISOString(),
    timing,
  };

  // Recalculate course progress
  const progress = calculateCourseProgress(record, course.competencies.length);
  record.mastery_points = progress.percentage;

  all[course.course_id] = record;
  saveAllStoredData(all);

  return {
    record,
    overall_score: overallScore,
    overall_total: overallTotal,
    overall_percentage: overallPercentage,
    total_seconds: safeTotalSeconds,
    avg_seconds_per_question: avgSeconds,
    is_new_record: isNewRecord,
    skills_leveled_up: skillsLeveledUp,
    skills_leveled_down: skillsLeveledDown,
    skills_maintained: skillsMaintained,
    misconceptions,
  };
}

export function updateCourseChallengeCompleted(
  course: Course,
  score: number,
  total: number
): CourseMasteryRecord {
  const all = getAllStoredData();
  const record = loadCourseMastery(course);

  const ratio = total > 0 ? score / total : 0;
  const percentage = Math.round(ratio * 100);
  const isCompleted = ratio === 1 && total > 0;

  record.course_challenge = {
    completed: isCompleted,
    last_score: score,
    total_questions: total,
    percentage,
    completed_at: new Date().toISOString(),
    timing: record.course_challenge?.timing,
  };

  // Recalculate total course progress using the 80/20 formula
  const progress = calculateCourseProgress(record, course.competencies.length);
  record.mastery_points = progress.percentage;

  all[course.course_id] = record;
  saveAllStoredData(all);
  return record;
}

export function getTimingForCompetency(
  courseId: string,
  competencyId: string,
  sessionType: 'practice' | 'quiz' | 'test'
): TimingStats | undefined {
  const all = getAllStoredData();
  return all[courseId]?.competencies?.[competencyId]?.timing?.[sessionType];
}

export function getTimingForChallenge(courseId: string): TimingStats | undefined {
  const all = getAllStoredData();
  return all[courseId]?.course_challenge?.timing;
}

export function getCourseMasteryRecord(courseId: string): CourseMasteryRecord | undefined {
  const all = getAllStoredData();
  return all[courseId];
}

/**
 * A unit is completed (Verde) ONLY when its latest Unit Test scored 100%.
 */
export function isUnitCompleted(compMastery?: CompetencyMastery): boolean {
  if (!compMastery || !compMastery.unit_test) return false;
  return (
    compMastery.unit_test.percentage === 100 &&
    compMastery.unit_test.total_questions > 0
  );
}

/**
 * A unit is started (Amarillo) when it has at least one practice, quiz or unit test attempt.
 */
export function isUnitStarted(compMastery?: CompetencyMastery): boolean {
  if (!compMastery) return false;
  if (isUnitCompleted(compMastery)) return true;
  return (
    (compMastery.history && compMastery.history.length > 0) ||
    compMastery.status !== 'Not started' ||
    compMastery.points > 0 ||
    !!compMastery.unit_test
  );
}

export function isCompetencyCompleted(compMastery?: CompetencyMastery): boolean {
  return isUnitCompleted(compMastery);
}

/**
 * Calculates course progress using the strict 80/20 model:
 * - Average of Unit Tests across all units contributes 0-80% (avg * 0.80).
 * - Course Challenge (100% required) contributes the remaining 0-20% (cc_pct * 0.20).
 * - Total = round(unitTestsContribution + ccContribution).
 */
export function calculateCourseProgress(
  record?: CourseMasteryRecord,
  totalCompetencies?: number
): CourseProgressDetails {
  if (!record) {
    const total = totalCompetencies || 0;
    return {
      percentage: 0,
      status: 'not_started',
      completedUnits: 0,
      inProgressUnits: 0,
      notStartedUnits: total,
      totalUnits: total,
    };
  }

  const compList = Object.values(record.competencies || {});
  const totalUnits = totalCompetencies || compList.length || 0;

  if (totalUnits === 0) {
    return {
      percentage: 0,
      status: 'not_started',
      completedUnits: 0,
      inProgressUnits: 0,
      notStartedUnits: 0,
      totalUnits: 0,
    };
  }

  let completedUnits = 0;
  let inProgressUnits = 0;
  let sumUnitTestPercentages = 0;

  for (const comp of compList) {
    if (isUnitCompleted(comp)) {
      completedUnits++;
    } else if (isUnitStarted(comp)) {
      inProgressUnits++;
    }

    if (comp.unit_test && comp.unit_test.total_questions > 0) {
      sumUnitTestPercentages += comp.unit_test.percentage;
    }
  }

  const notStartedUnits = Math.max(0, totalUnits - completedUnits - inProgressUnits);

  // 80/20 Formula:
  const avgUnitTests = sumUnitTestPercentages / totalUnits;
  const unitTestsContribution = avgUnitTests * 0.8;

  const cc = record.course_challenge;
  const ccPercentage =
    cc && cc.total_questions > 0
      ? (cc.percentage ?? (cc.completed ? 100 : Math.round((cc.last_score / cc.total_questions) * 100)))
      : 0;
  const ccContribution = (ccPercentage / 100) * 20;

  const rawPercentage = Math.round(unitTestsContribution + ccContribution);
  const percentage = Math.min(100, Math.max(0, rawPercentage));

  const allUnitTests100 = completedUnits >= totalUnits && totalUnits > 0;
  const cc100 = cc?.completed === true || ccPercentage === 100;

  let status: CourseProgressStatus = 'not_started';
  if (allUnitTests100 && cc100) {
    status = 'completed'; // Verde Fuerte (100%)
  } else if (allUnitTests100) {
    status = 'unit_tests_mastered'; // Verde Light (80%)
  } else if (percentage > 0 || completedUnits > 0 || inProgressUnits > 0) {
    status = 'in_progress'; // Amarillo
  }

  return {
    percentage,
    status,
    completedUnits,
    inProgressUnits,
    notStartedUnits,
    totalUnits,
  };
}

export function getCourseProgressDetails(
  courseId: string,
  totalCompetencies?: number
): CourseProgressDetails {
  const all = getAllStoredData();
  const record = all[courseId];
  return calculateCourseProgress(record, totalCompetencies);
}

export function isCourseCompleted(courseId: string, totalCompetencies?: number): boolean {
  const details = getCourseProgressDetails(courseId, totalCompetencies);
  return details.status === 'completed' || details.status === 'unit_tests_mastered';
}
