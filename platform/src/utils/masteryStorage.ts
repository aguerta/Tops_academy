import {
  Course,
  CourseMasteryRecord,
  CompetencyMastery,
  MasteryTier,
  UnitTestRecord,
  CourseProgressDetails,
  CourseProgressStatus,
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
  sessionType: 'practice' | 'quiz' | 'test' | 'challenge'
): CourseMasteryRecord {
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
  let newTier: MasteryTier = prev.status;

  let unitTestRecord: UnitTestRecord | undefined = prev.unit_test;

  if (sessionType === 'test') {
    // Record latest Unit Test attempt
    unitTestRecord = {
      last_score: score,
      total_questions: total,
      percentage,
      completed_at: new Date().toISOString(),
    };

    if (ratio === 1) {
      newTier = 'Mastered';
    } else if (ratio >= 0.8) {
      newTier = 'Proficient';
    } else if (ratio >= 0.5) {
      newTier = 'Familiar';
    } else {
      newTier = 'Attempted';
    }
  } else if (sessionType === 'practice') {
    if (ratio === 1) {
      if (prev.status !== 'Mastered') {
        newTier = 'Proficient';
      }
    } else if (ratio >= 0.7) {
      if (prev.status === 'Not started' || prev.status === 'Attempted') {
        newTier = 'Familiar';
      }
    } else {
      if (prev.status === 'Not started') {
        newTier = 'Attempted';
      }
    }
  } else if (sessionType === 'quiz') {
    if (ratio >= 0.8) {
      if (prev.status !== 'Mastered') {
        newTier = 'Proficient';
      }
    } else if (ratio >= 0.6) {
      if (prev.status === 'Not started' || prev.status === 'Attempted') {
        newTier = 'Familiar';
      }
    }
  }

  record.competencies[competencyId] = {
    status: newTier,
    points: TIER_POINTS[newTier],
    last_practiced: new Date().toISOString(),
    unit_test: unitTestRecord,
    history: [
      ...prev.history,
      {
        date: new Date().toISOString(),
        score,
        total,
        type: sessionType,
      },
    ],
  };

  // Recalculate total course progress using the 80/20 formula
  const progress = calculateCourseProgress(record, course.competencies.length);
  record.mastery_points = progress.percentage;

  all[course.course_id] = record;
  saveAllStoredData(all);
  return record;
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
  };

  // Recalculate total course progress using the 80/20 formula
  const progress = calculateCourseProgress(record, course.competencies.length);
  record.mastery_points = progress.percentage;

  all[course.course_id] = record;
  saveAllStoredData(all);
  return record;
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
