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
  SessionType,
  ReviewReason,
  MisconceptionEntry,
  QuestionType,
  SrsReviewTelemetry,
} from '../types';
import { scheduleBackgroundSync } from './cloudSync';
import {
  computeAutomaticFsrsRating,
  computeRetrievability,
  DECAY_DOWNGRADE_THRESHOLD,
  DECAY_THRESHOLD_MASTERED,
  DECAY_THRESHOLD_PROFICIENT,
  getCooldownRemainingMs,
  getPersonalMedianLatency,
  MAX_MODALITY_LATENCY_WINDOW,
  MAX_SRS_TELEMETRY_ENTRIES,
  scheduleFsrsReview,
} from './fsrsEngine';

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
  sessionType: SessionType,
  hintsUsed: number = 0,
  options?: { canPromoteToMastered?: boolean }
): MasteryTier {
  if (total <= 0) return prevTier;
  const ratio = score / total;
  const isHintCapped = hintsUsed >= 2;
  const isMasterySession = sessionType === 'challenge' || sessionType === 'mastery_challenge';
  const canPromoteToMastered = isMasterySession && options?.canPromoteToMastered !== false;

  // Single question evaluation (Course Challenge / Mastery Challenge slice or single item)
  if (total === 1) {
    if (score === 0) {
      return getTierDowngrade(prevTier);
    }
    if (isHintCapped) {
      if (prevTier === 'Not started' || prevTier === 'Attempted') {
        return 'Familiar';
      }
      return prevTier;
    }
    switch (prevTier) {
      case 'Not started':
        return 'Familiar';
      case 'Attempted':
        return 'Familiar';
      case 'Familiar':
        return 'Proficient';
      case 'Proficient':
        return canPromoteToMastered ? 'Mastered' : 'Proficient';
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
    if (isMasterySession) {
      if (ratio === 1 && prevTier === 'Proficient') {
        return canPromoteToMastered ? 'Mastered' : 'Proficient';
      }
      if (prevTier === 'Mastered') return 'Mastered';
      if (prevTier === 'Not started') return 'Familiar';
      return 'Proficient';
    }
    // Practice, quiz, unit test, misconception drill: cap upward promotion at Proficient
    // (Unit Test 100% still marks unit completed for the 80/20 course progress formula).
    if (ratio === 1) {
      return prevTier === 'Mastered' ? 'Mastered' : 'Proficient';
    }
    return prevTier === 'Not started' || prevTier === 'Attempted' ? 'Familiar' : prevTier;
  }

  if (ratio >= 0.5) {
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

function saveAllStoredData(data: Record<string, CourseMasteryRecord>, triggerCloudSync: boolean = true) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    if (triggerCloudSync) {
      scheduleBackgroundSync();
    }
  } catch (err) {
    console.error('Failed to save mastery data to localStorage', err);
  }
}

/**
 * Evaluates longitudinal FSRS retrievability R(t) across all competencies of a record
 * at timestamp `now`. Marks `review_reason: 'decay'` when crossing soft thresholds and
 * downgrades Mastered->Proficient or Proficient->Familiar under extreme forgetting (<0.50)
 * WITHOUT altering `unit_test` records (preserving the 80/20 course progress invariant).
 */
export function evaluateCourseDecay(
  record: CourseMasteryRecord,
  now: Date = new Date()
): { changed: boolean; downgraded: boolean } {
  let changed = false;
  let downgraded = false;
  const competencies = record.competencies || {};

  for (const compId of Object.keys(competencies)) {
    const comp = competencies[compId];
    if (!comp || !comp.fsrs || comp.fsrs.state === 0 || !comp.fsrs.last_review) {
      continue;
    }

    const r = computeRetrievability(comp.fsrs, now);

    if (
      r < DECAY_DOWNGRADE_THRESHOLD &&
      (comp.status === 'Mastered' || comp.status === 'Proficient')
    ) {
      const nextTier: MasteryTier = comp.status === 'Mastered' ? 'Proficient' : 'Familiar';
      const nextReason: ReviewReason = comp.review_reason === 'error' ? 'error' : 'decay';
      competencies[compId] = {
        ...comp,
        status: nextTier,
        points: TIER_POINTS[nextTier],
        needs_review: true,
        review_reason: nextReason,
        ...(nextTier === 'Proficient' ? { last_tier_promotion_at: now.toISOString() } : {}),
      };
      changed = true;
      downgraded = true;
      continue;
    }

    const needsDecayWarning =
      (comp.status === 'Mastered' && r < DECAY_THRESHOLD_MASTERED) ||
      (comp.status === 'Proficient' && r < DECAY_THRESHOLD_PROFICIENT);

    if (needsDecayWarning) {
      const nextReason: ReviewReason = comp.review_reason === 'error' ? 'error' : 'decay';
      if (!comp.needs_review || comp.review_reason !== nextReason) {
        competencies[compId] = {
          ...comp,
          needs_review: true,
          review_reason: nextReason,
        };
        changed = true;
      }
    }
  }

  return { changed, downgraded };
}

export function loadCourseMastery(
  course: Course,
  now: Date = new Date()
): CourseMasteryRecord {
  const all = getAllStoredData();
  const existing = all[course.course_id];
  const nowIso = now.toISOString();

  if (existing) {
    let added = false;
    course.competencies.forEach((c) => {
      if (!existing.competencies[c.id]) {
        existing.competencies[c.id] = {
          status: 'Not started',
          points: 0,
          last_practiced: nowIso,
          history: [],
        };
        added = true;
      }
    });
    const decay = evaluateCourseDecay(existing, now);
    if (decay.changed || added) {
      all[course.course_id] = existing;
      saveAllStoredData(all, false);
    }
    return existing;
  }

  const initialComp: Record<string, CompetencyMastery> = {};
  course.competencies.forEach((c) => {
    initialComp[c.id] = {
      status: 'Not started',
      points: 0,
      last_practiced: nowIso,
      history: [],
    };
  });

  const record: CourseMasteryRecord = {
    course_id: course.course_id,
    mastery_points: 0,
    competencies: initialComp,
  };

  all[course.course_id] = record;
  saveAllStoredData(all, false);
  return record;
}

function appendModalityLatencies(
  prevMap: Partial<Record<QuestionType, number[]>> | undefined,
  questions: QuestionTelemetry[]
): Partial<Record<QuestionType, number[]>> | undefined {
  let nextMap: Partial<Record<QuestionType, number[]>> | undefined = prevMap
    ? { ...prevMap }
    : undefined;

  for (const q of questions) {
    if (!q.question_type) continue;
    const sec = Math.min(300, Math.max(1, Math.round(q.seconds_spent || 0)));
    if (!Number.isFinite(sec) || sec <= 0) continue;
    if (!nextMap) nextMap = {};
    const existing = Array.isArray(nextMap[q.question_type]) ? nextMap[q.question_type]! : [];
    nextMap[q.question_type] = [...existing, sec].slice(-MAX_MODALITY_LATENCY_WINDOW);
  }

  return nextMap;
}

function computeCompetencySpeedRatio(
  prevMap: Partial<Record<QuestionType, number[]>> | undefined,
  questions: QuestionTelemetry[]
): { speedRatio: number | null; hasPersonalBaseline: boolean } {
  if (!questions || questions.length === 0) {
    return { speedRatio: null, hasPersonalBaseline: false };
  }
  const ratios: number[] = [];
  for (const q of questions) {
    if (!q.question_type) {
      return { speedRatio: null, hasPersonalBaseline: false };
    }
    const median = getPersonalMedianLatency(prevMap, q.question_type);
    if (median === null || median <= 0) {
      return { speedRatio: null, hasPersonalBaseline: false };
    }
    const spent = Math.min(300, Math.max(1, q.seconds_spent || 0));
    ratios.push(spent / median);
  }
  const avg = ratios.reduce((acc, v) => acc + v, 0) / ratios.length;
  return { speedRatio: avg, hasPersonalBaseline: true };
}

function updateLedgerFromTelemetries(
  ledger: Record<string, MisconceptionEntry>,
  questions: QuestionTelemetry[],
  competencyId: string,
  nowIso: string
): void {
  for (const qTel of questions) {
    const matchedIds = qTel.matched_distractor_ids || [];
    const matchedSet = new Set(matchedIds);

    for (const did of matchedIds) {
      if (!did) continue;
      const existing = ledger[did];
      const rationale =
        qTel.matched_distractor_rationales?.[did] ||
        existing?.rationale ||
        qTel.question_text ||
        did;
      ledger[did] = {
        distractor_id: did,
        competency_id: competencyId,
        rationale,
        count: (existing?.count ?? 0) + 1,
        last_seen: nowIso,
        resolved_streak: 0,
      };
    }

    const cleanAutonomous =
      qTel.is_correct && qTel.hints_used === 0 && (qTel.wrong_attempts ?? 0) === 0;
    if (cleanAutonomous && qTel.carried_distractor_ids?.length) {
      for (const carriedDid of qTel.carried_distractor_ids) {
        if (!carriedDid || matchedSet.has(carriedDid)) continue;
        const entry = ledger[carriedDid];
        if (entry && entry.resolved_streak < 2) {
          ledger[carriedDid] = {
            ...entry,
            resolved_streak: entry.resolved_streak + 1,
          };
        }
      }
    }
  }
}

export interface CrossSkillUpdateOptions {
  targetCompetencyId?: string;
  now?: Date;
}

/**
 * Unified cross-skill calibrator for Quiz, Unit Test, Mastery Challenge,
 * Course Challenge / Iron Exam, and Misconception Drills.
 * Updates each competency's MasteryTier, 12h per-skill cooldown, FSRS-5/6 DSR card,
 * modality latency medians, srs_telemetry (capped at 500), and Misconception Ledger.
 */
export function updateSessionWithCrossSkillCalibration(
  course: Course,
  telemetry: QuestionTelemetry[],
  totalSeconds: number,
  sessionType: SessionType,
  options?: CrossSkillUpdateOptions
): ChallengeExecutionSummary {
  const now = options?.now ?? new Date();
  const nowIso = now.toISOString();
  const all = getAllStoredData();
  const record = loadCourseMastery(course, now);

  const overallTotal = telemetry.length;
  const overallScore = telemetry.filter((t) => t.is_correct).length;
  const overallRatio = overallTotal > 0 ? overallScore / overallTotal : 0;
  const overallPercentage = Math.round(overallRatio * 100);
  const isCompleted = overallRatio === 1 && overallTotal > 0;

  // Group telemetry by competency_id
  const byComp: Record<
    string,
    { total: number; correct: number; hintsUsed: number; questions: QuestionTelemetry[] }
  > = {};
  for (const t of telemetry) {
    const cid = t.competency_id;
    if (!cid) continue;
    if (!byComp[cid]) {
      byComp[cid] = { total: 0, correct: 0, hintsUsed: 0, questions: [] };
    }
    byComp[cid].total += 1;
    if (t.is_correct) byComp[cid].correct += 1;
    byComp[cid].hintsUsed += t.hints_used || 0;
    byComp[cid].questions.push(t);
  }

  const ledger: Record<string, MisconceptionEntry> = {
    ...(record.misconception_ledger || {}),
  };
  const srsTelemetry: SrsReviewTelemetry[] = [...(record.srs_telemetry || [])];

  const skillsLeveledUp: ChallengeSkillResult[] = [];
  const skillsLeveledDown: ChallengeSkillResult[] = [];
  const skillsMaintained: ChallengeSkillResult[] = [];
  const misconceptions: ChallengeExecutionSummary['misconceptions'] = [];

  const isMasterySession = sessionType === 'challenge' || sessionType === 'mastery_challenge';

  const compNameMap = new Map<string, string>(
    course.competencies.map((c) => [c.id, c.name])
  );
  const orderedCompIds = [
    ...course.competencies.map((c) => c.id).filter((id) => Boolean(byComp[id])),
    ...Object.keys(byComp).filter((id) => !compNameMap.has(id)),
  ];

  const safeTotalSeconds = Math.min(totalSeconds, Math.max(1, overallTotal) * 300);
  const overallAvgSeconds = overallTotal > 0 ? Math.round(safeTotalSeconds / overallTotal) : 0;

  for (const compId of orderedCompIds) {
    const compData = byComp[compId];
    if (!compData) continue;

    const prev = record.competencies[compId] || {
      status: 'Not started' as MasteryTier,
      points: 0,
      last_practiced: nowIso,
      history: [],
    };
    const prevTier = prev.status;

    const cooldownRefAt =
      prev.last_tier_promotion_at || (prevTier === 'Proficient' ? prev.last_practiced : undefined);
    const cooldownRemainingMs =
      isMasterySession && prevTier === 'Proficient'
        ? getCooldownRemainingMs(cooldownRefAt, now)
        : 0;
    const canPromoteToMastered = isMasterySession && cooldownRemainingMs === 0;

    const newTier = calculateTierTransition(
      prevTier,
      compData.correct,
      compData.total,
      sessionType,
      compData.hintsUsed,
      { canPromoteToMastered }
    );

    const prevPoints = TIER_POINTS[prevTier];
    const newPoints = TIER_POINTS[newTier];
    const deltaPoints = newPoints - prevPoints;

    let direction: 'up' | 'down' | 'maintained' = 'maintained';
    if (deltaPoints > 0) direction = 'up';
    else if (deltaPoints < 0) direction = 'down';

    const hitCooldownGate =
      isMasterySession &&
      prevTier === 'Proficient' &&
      newTier === 'Proficient' &&
      compData.correct === compData.total &&
      compData.hintsUsed < 2 &&
      cooldownRemainingMs > 0;

    const skillResult: ChallengeSkillResult = {
      competency_id: compId,
      competency_name: compNameMap.get(compId) || compId,
      total_questions: compData.total,
      correct_questions: compData.correct,
      previous_tier: prevTier,
      new_tier: newTier,
      direction,
      delta_points: deltaPoints,
      ...(hitCooldownGate ? { cooldown_remaining_ms: cooldownRemainingMs } : {}),
    };

    if (direction === 'up') skillsLeveledUp.push(skillResult);
    else if (direction === 'down') skillsLeveledDown.push(skillResult);
    else skillsMaintained.push(skillResult);

    // Collect session misconceptions summary
    for (const q of compData.questions) {
      if (!q.is_correct) {
        misconceptions.push({
          question_id: q.question_id,
          competency_id: compId,
          competency_name: compNameMap.get(compId) || compId,
          text: q.question_text || q.question_id,
        });
      }
    }

    // Update Misconception Ledger
    updateLedgerFromTelemetries(ledger, compData.questions, compId, nowIso);

    // FSRS rating & review (1 aggregated review per competency per session)
    const compRatio = compData.total > 0 ? compData.correct / compData.total : 0;
    const { speedRatio, hasPersonalBaseline } = computeCompetencySpeedRatio(
      prev.modality_latencies,
      compData.questions
    );
    const totalWrongAttempts = compData.questions.reduce(
      (acc, q) => acc + (q.wrong_attempts ?? 0),
      0
    );
    const hasLuckyGuess = compData.questions.some(
      (q) => q.is_correct && q.metacognitive_quadrant === 'lucky_guess'
    );
    const hasLowConfidence = compData.questions.some(
      (q) =>
        q.metacognitive_quadrant === 'lucky_guess' || q.metacognitive_quadrant === 'known_gap'
    );

    const { rating } = computeAutomaticFsrsRating({
      ratio: compRatio,
      hintsUsed: compData.hintsUsed,
      totalWrongAttempts,
      hasLuckyGuess,
      hasLowConfidence,
      priorReviews: prev.fsrs?.reps ?? 0,
      speedRatio,
      hasPersonalBaseline,
    });

    const { nextCard, predictedR, deltaTDays } = scheduleFsrsReview(prev.fsrs, rating, now);
    srsTelemetry.push({
      date: nowIso,
      competency_id: compId,
      delta_t_days: deltaTDays,
      predicted_r: predictedR,
      actual_correct: compData.total > 0 && compData.correct === compData.total,
      rating,
    });

    const updatedModalityLatencies = appendModalityLatencies(
      prev.modality_latencies,
      compData.questions
    );

    // Tier promotion timestamp tracking (for 12h per-skill cooldown)
    let nextLastTierPromotionAt = prev.last_tier_promotion_at;
    if (
      (newTier === 'Proficient' && prevTier !== 'Proficient') ||
      newTier === 'Mastered'
    ) {
      nextLastTierPromotionAt = nowIso;
    }

    // Needs review & error vs decay reason
    const hasErrors = compData.correct < compData.total;
    let nextNeedsReview = prev.needs_review || false;
    let nextReviewReason = prev.review_reason;
    let recentMisconceptions = prev.recent_misconceptions ? [...prev.recent_misconceptions] : [];

    if (hasErrors) {
      nextNeedsReview = true;
      nextReviewReason = 'error';
      const failedItems = compData.questions
        .filter((t) => !t.is_correct)
        .map((f) => ({
          date: nowIso,
          question_id: f.question_id,
          concept_name: f.question_text || f.question_id,
        }));
      recentMisconceptions = [...recentMisconceptions, ...failedItems].slice(-5);
    } else {
      // Clean 100% pass on this competency heals review flags
      nextNeedsReview = false;
      nextReviewReason = undefined;
      recentMisconceptions = [];
    }

    const compSeconds = compData.questions.reduce(
      (acc, q) => acc + Math.min(300, Math.max(1, q.seconds_spent || 0)),
      0
    );
    const compAvgSeconds = compData.total > 0 ? Math.round(compSeconds / compData.total) : 0;

    record.competencies[compId] = {
      ...prev,
      status: newTier,
      points: newPoints,
      last_practiced: nowIso,
      ...(nextLastTierPromotionAt ? { last_tier_promotion_at: nextLastTierPromotionAt } : {}),
      fsrs: nextCard,
      ...(updatedModalityLatencies ? { modality_latencies: updatedModalityLatencies } : {}),
      needs_review: nextNeedsReview,
      ...(nextReviewReason ? { review_reason: nextReviewReason } : { review_reason: undefined }),
      recent_misconceptions: recentMisconceptions,
      history: [
        ...prev.history,
        {
          date: nowIso,
          score: compData.correct,
          total: compData.total,
          type: sessionType,
          total_seconds: compSeconds,
          avg_seconds_per_question: compAvgSeconds,
          previous_tier: prevTier,
          new_tier: newTier,
        },
      ],
    };
  }

  // Record global unit_test and session timing on targetCompetencyId when applicable
  let targetIsNewRecord = false;
  if (
    options?.targetCompetencyId &&
    (sessionType === 'practice' || sessionType === 'quiz' || sessionType === 'test')
  ) {
    const targetId = options.targetCompetencyId;
    const targetComp = record.competencies[targetId] || {
      status: 'Not started' as MasteryTier,
      points: 0,
      last_practiced: nowIso,
      history: [],
    };
    const timing = targetComp.timing ? { ...targetComp.timing } : {};
    const currentTiming = timing[sessionType] ? { ...timing[sessionType] } : {};
    if (overallTotal > 0 && overallScore === overallTotal) {
      if (
        currentTiming.best_avg_seconds_per_question === undefined ||
        overallAvgSeconds < currentTiming.best_avg_seconds_per_question
      ) {
        currentTiming.best_avg_seconds_per_question = overallAvgSeconds;
        currentTiming.best_total_seconds = safeTotalSeconds;
        targetIsNewRecord = true;
      }
    }
    currentTiming.last_avg_seconds_per_question = overallAvgSeconds;
    currentTiming.last_total_seconds = safeTotalSeconds;
    timing[sessionType] = currentTiming;

    let unitTestRecord: UnitTestRecord | undefined = targetComp.unit_test;
    if (sessionType === 'test') {
      unitTestRecord = {
        last_score: overallScore,
        total_questions: overallTotal,
        percentage: overallPercentage,
        completed_at: nowIso,
      };
    }

    record.competencies[targetId] = {
      ...targetComp,
      timing,
      ...(unitTestRecord ? { unit_test: unitTestRecord } : {}),
    };
  }

  // Update challenge or mastery_challenge timestamps
  let challengeIsNewRecord = false;
  if (sessionType === 'challenge') {
    const prevCc = record.course_challenge;
    const timing: TimingStats = prevCc?.timing ? { ...prevCc.timing } : {};
    if (isCompleted) {
      if (
        timing.best_avg_seconds_per_question === undefined ||
        overallAvgSeconds < timing.best_avg_seconds_per_question
      ) {
        timing.best_avg_seconds_per_question = overallAvgSeconds;
        timing.best_total_seconds = safeTotalSeconds;
        challengeIsNewRecord = true;
      }
    }
    timing.last_avg_seconds_per_question = overallAvgSeconds;
    timing.last_total_seconds = safeTotalSeconds;

    record.course_challenge = {
      completed: isCompleted,
      last_score: overallScore,
      total_questions: overallTotal,
      percentage: overallPercentage,
      completed_at: nowIso,
      timing,
    };
  } else if (sessionType === 'mastery_challenge') {
    record.last_mastery_challenge_at = nowIso;
  }

  record.misconception_ledger = ledger;
  record.srs_telemetry = srsTelemetry.slice(-MAX_SRS_TELEMETRY_ENTRIES);

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
    avg_seconds_per_question: overallAvgSeconds,
    is_new_record: sessionType === 'challenge' ? challengeIsNewRecord : targetIsNewRecord,
    skills_leveled_up: skillsLeveledUp,
    skills_leveled_down: skillsLeveledDown,
    skills_maintained: skillsMaintained,
    misconceptions,
  };
}

export function updateCompetencyScore(
  course: Course,
  competencyId: string,
  score: number,
  total: number,
  sessionType: SessionType,
  timingData?: { totalSeconds: number; hintsUsed?: number },
  questionTelemetries?: QuestionTelemetry[],
  now: Date = new Date()
): CourseMasteryRecord & {
  isNewRecord?: boolean;
  previousTier?: MasteryTier;
  newTier?: MasteryTier;
  totalSeconds?: number;
  avgSeconds?: number;
} {
  const nowIso = now.toISOString();
  const hintsUsed = timingData?.hintsUsed ?? 0;
  const rawSec = timingData?.totalSeconds ?? 0;
  const safeTotalSeconds = Math.min(rawSec, Math.max(1, total) * 300);
  const avgSeconds = total > 0 ? Math.round(safeTotalSeconds / total) : 0;

  // When rich per-question telemetry is present, run unified cross-skill + FSRS + Ledger pipeline
  if (questionTelemetries && questionTelemetries.length > 0) {
    const prevRecord = loadCourseMastery(course, now);
    const prevTier = prevRecord.competencies[competencyId]?.status || 'Not started';
    const summary = updateSessionWithCrossSkillCalibration(
      course,
      questionTelemetries,
      safeTotalSeconds,
      sessionType,
      { targetCompetencyId: competencyId, now }
    );
    const updatedTier = summary.record.competencies[competencyId]?.status || prevTier;
    return {
      ...summary.record,
      isNewRecord: summary.is_new_record,
      previousTier: prevTier,
      newTier: updatedTier,
      totalSeconds: summary.total_seconds,
      avgSeconds: summary.avg_seconds_per_question,
    };
  }

  // Fallback path when called directly without questionTelemetries (e.g. unit tests)
  const all = getAllStoredData();
  const record = loadCourseMastery(course, now);

  const prev = record.competencies[competencyId] || {
    status: 'Not started' as MasteryTier,
    points: 0,
    last_practiced: nowIso,
    history: [],
  };

  const ratio = total > 0 ? score / total : 0;
  const percentage = Math.round(ratio * 100);
  const previousTier = prev.status;
  const isMasterySession = sessionType === 'challenge' || sessionType === 'mastery_challenge';
  const cooldownRefAt =
    prev.last_tier_promotion_at || (previousTier === 'Proficient' ? prev.last_practiced : undefined);
  const canPromoteToMastered =
    isMasterySession && getCooldownRemainingMs(cooldownRefAt, now) === 0;

  const newTier = calculateTierTransition(previousTier, score, total, sessionType, hintsUsed, {
    canPromoteToMastered,
  });

  let unitTestRecord: UnitTestRecord | undefined = prev.unit_test;
  if (sessionType === 'test') {
    unitTestRecord = {
      last_score: score,
      total_questions: total,
      percentage,
      completed_at: nowIso,
    };
  }

  let isNewRecord = false;
  const timing = prev.timing ? { ...prev.timing } : {};
  if (sessionType === 'practice' || sessionType === 'quiz' || sessionType === 'test') {
    const currentTiming = timing[sessionType] ? { ...timing[sessionType] } : {};
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

  let needsReview = prev.needs_review || false;
  let reviewReason = prev.review_reason;
  let recentMisconceptions = prev.recent_misconceptions ? [...prev.recent_misconceptions] : [];
  if (total > 0 && score < total) {
    needsReview = true;
    reviewReason = 'error';
  } else if (total > 0 && score === total) {
    needsReview = false;
    reviewReason = undefined;
    recentMisconceptions = [];
  }

  const { rating } = computeAutomaticFsrsRating({
    ratio,
    hintsUsed,
    totalWrongAttempts: 0,
    priorReviews: prev.fsrs?.reps ?? 0,
    speedRatio: null,
    hasPersonalBaseline: false,
  });
  const { nextCard, predictedR, deltaTDays } = scheduleFsrsReview(prev.fsrs, rating, now);

  let nextLastTierPromotionAt = prev.last_tier_promotion_at;
  if (
    (newTier === 'Proficient' && previousTier !== 'Proficient') ||
    newTier === 'Mastered'
  ) {
    nextLastTierPromotionAt = nowIso;
  }

  record.competencies[competencyId] = {
    ...prev,
    status: newTier,
    points: TIER_POINTS[newTier],
    last_practiced: nowIso,
    ...(nextLastTierPromotionAt ? { last_tier_promotion_at: nextLastTierPromotionAt } : {}),
    unit_test: unitTestRecord,
    timing,
    fsrs: nextCard,
    needs_review: needsReview,
    ...(reviewReason ? { review_reason: reviewReason } : { review_reason: undefined }),
    recent_misconceptions: recentMisconceptions,
    history: [
      ...prev.history,
      {
        date: nowIso,
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

  record.srs_telemetry = [
    ...(record.srs_telemetry || []),
    {
      date: nowIso,
      competency_id: competencyId,
      delta_t_days: deltaTDays,
      predicted_r: predictedR,
      actual_correct: total > 0 && score === total,
      rating,
    },
  ].slice(-MAX_SRS_TELEMETRY_ENTRIES);

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
  totalSeconds: number,
  now: Date = new Date()
): ChallengeExecutionSummary {
  return updateSessionWithCrossSkillCalibration(course, telemetry, totalSeconds, 'challenge', {
    now,
  });
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

  const progress = calculateCourseProgress(record, course.competencies.length);
  record.mastery_points = progress.percentage;

  all[course.course_id] = record;
  saveAllStoredData(all, false);
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

export function getCompetencyRetrievability(
  compMastery?: CompetencyMastery,
  now: Date = new Date()
): number {
  return computeRetrievability(compMastery?.fsrs, now);
}

export function getActiveMisconceptions(record?: CourseMasteryRecord): MisconceptionEntry[] {
  const entries = Object.values(record?.misconception_ledger || {});
  return entries
    .filter((e) => e.resolved_streak < 2)
    .sort((a, b) => {
      if (b.count !== a.count) return b.count - a.count;
      return Date.parse(b.last_seen) - Date.parse(a.last_seen);
    });
}

export function getResolvedMisconceptions(record?: CourseMasteryRecord): MisconceptionEntry[] {
  const entries = Object.values(record?.misconception_ledger || {});
  return entries
    .filter((e) => e.resolved_streak >= 2)
    .sort((a, b) => Date.parse(b.last_seen) - Date.parse(a.last_seen));
}

export interface MasteryChallengeReadiness {
  startedCount: number;
  decayDueCount: number;
  proficientEligibleCount: number;
  proficientInCooldownCount: number;
  lowestRetrievabilityCompId: string | null;
  lowestRetrievability: number;
}

export function getMasteryChallengeReadiness(
  course: Course,
  record?: CourseMasteryRecord,
  now: Date = new Date()
): MasteryChallengeReadiness {
  let startedCount = 0;
  let decayDueCount = 0;
  let proficientEligibleCount = 0;
  let proficientInCooldownCount = 0;
  let lowestRetrievabilityCompId: string | null = null;
  let lowestRetrievability = 1;

  for (const c of course.competencies) {
    const m = record?.competencies?.[c.id];
    if (!isUnitStarted(m)) continue;
    startedCount += 1;

    const r = computeRetrievability(m?.fsrs, now);
    if (m?.fsrs && m.fsrs.state !== 0 && r < lowestRetrievability) {
      lowestRetrievability = r;
      lowestRetrievabilityCompId = c.id;
    }

    if (m?.needs_review && m.review_reason === 'decay') {
      decayDueCount += 1;
    }

    if (m?.status === 'Proficient') {
      const refAt = m.last_tier_promotion_at || m.last_practiced;
      if (getCooldownRemainingMs(refAt, now) === 0) {
        proficientEligibleCount += 1;
      } else {
        proficientInCooldownCount += 1;
      }
    }
  }

  return {
    startedCount,
    decayDueCount,
    proficientEligibleCount,
    proficientInCooldownCount,
    lowestRetrievabilityCompId,
    lowestRetrievability,
  };
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
 * Calculates course progress using the points-based 80/20 model:
 * - Average of mastery points (0-100) across all competencies contributes 0-80% (avgPoints * 0.80).
 * - Course Challenge (0-100%) contributes the remaining 0-20% (ccPercentage * 0.20).
 * - Total = round(pointsContribution + ccContribution).
 * - Status is 'completed' only when percentage === 100 (all skills Mastered 100 pts + Course Challenge 100%).
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
  let sumPoints = 0;

  for (const comp of compList) {
    if (isUnitCompleted(comp)) {
      completedUnits++;
    } else if (isUnitStarted(comp)) {
      inProgressUnits++;
    }

    const pts = typeof comp.points === 'number' ? comp.points : TIER_POINTS[comp.status] ?? 0;
    sumPoints += Math.min(100, Math.max(0, pts));
  }

  const notStartedUnits = Math.max(0, totalUnits - completedUnits - inProgressUnits);

  const avgPoints = sumPoints / totalUnits;
  const pointsContribution = avgPoints * 0.8;

  const cc = record.course_challenge;
  const ccPercentage =
    cc && cc.total_questions > 0
      ? (cc.percentage ?? (cc.completed ? 100 : Math.round((cc.last_score / cc.total_questions) * 100)))
      : 0;
  const ccContribution = (ccPercentage / 100) * 20;

  const rawPercentage = Math.round(pointsContribution + ccContribution);
  const percentage = Math.min(100, Math.max(0, rawPercentage));

  const allUnitTests100 = completedUnits >= totalUnits && totalUnits > 0;

  let status: CourseProgressStatus = 'not_started';
  if (percentage === 100) {
    status = 'completed';
  } else if (allUnitTests100) {
    status = 'unit_tests_mastered';
  } else if (percentage > 0 || completedUnits > 0 || inProgressUnits > 0) {
    status = 'in_progress';
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
