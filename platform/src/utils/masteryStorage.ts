import { Course, CourseMasteryRecord, CompetencyMastery, MasteryTier } from '../types';

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
  let newTier: MasteryTier = prev.status;

  if (sessionType === 'practice') {
    if (ratio === 1) {
      // 100% in practice promotes to Proficient (or stays Mastered)
      if (prev.status !== 'Mastered') {
        newTier = 'Proficient';
      }
    } else if (ratio >= 0.7) {
      // >= 70% promotes to Familiar if below
      if (prev.status === 'Not started' || prev.status === 'Attempted') {
        newTier = 'Familiar';
      }
    } else {
      // < 70% marks as Attempted if Not started
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
  } else if (sessionType === 'test' || sessionType === 'challenge') {
    if (ratio === 1) {
      newTier = 'Mastered';
    } else if (ratio >= 0.8) {
      newTier = 'Proficient';
    } else if (ratio >= 0.6) {
      newTier = 'Familiar';
    } else if (ratio < 0.5 && prev.status === 'Mastered') {
      // Demote on poor performance
      newTier = 'Proficient';
    }
  }

  record.competencies[competencyId] = {
    status: newTier,
    points: TIER_POINTS[newTier],
    last_practiced: new Date().toISOString(),
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

  // Recalculate total course mastery %
  const totalComp = course.competencies.length;
  if (totalComp > 0) {
    const sumPoints = course.competencies.reduce((acc, c) => {
      const tier = record.competencies[c.id]?.status || 'Not started';
      return acc + TIER_POINTS[tier];
    }, 0);
    record.mastery_points = Math.round((sumPoints / (totalComp * 100)) * 100);
  }

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

  record.course_challenge = {
    completed: true,
    last_score: score,
    total_questions: total,
    completed_at: new Date().toISOString(),
  };

  all[course.course_id] = record;
  saveAllStoredData(all);
  return record;
}

export function getCourseMasteryRecord(courseId: string): CourseMasteryRecord | undefined {
  const all = getAllStoredData();
  return all[courseId];
}

export function isCompetencyCompleted(compMastery?: CompetencyMastery): boolean {
  if (!compMastery) return false;
  return (
    compMastery.status === 'Mastered' ||
    compMastery.status === 'Proficient' ||
    compMastery.points >= 80
  );
}

export function isCourseCompleted(courseId: string, totalCompetencies?: number): boolean {
  const all = getAllStoredData();
  const record = all[courseId];
  if (!record) return false;

  // 1. Overall course mastery points reaches 100%
  if (record.mastery_points >= 100) {
    return true;
  }

  // 2. All competencies in the course are mastered
  const compValues = Object.values(record.competencies || {});
  if (compValues.length > 0) {
    const allMastered = compValues.every((c) => c.status === 'Mastered');
    if (allMastered && (!totalCompetencies || compValues.length >= totalCompetencies)) {
      return true;
    }
  }

  return false;
}
