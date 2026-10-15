import { Competency, MasteryTier, Question, QuestionOption } from '../types';
import { normalizeQuestion } from './questionUtils';

/**
 * Standard Fisher-Yates array shuffling algorithm.
 */
export function shuffleArray<T>(items: T[]): T[] {
  const result = [...items];
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

/**
 * Stratifies a shuffled question list into Zone of Proximal Development (ZPD)
 * priority bands according to the learner's current MasteryTier, while preserving
 * full Fisher-Yates randomness within each band so repeated sessions never
 * present identical question sequences.
 *
 * - 'Not started' / 'Attempted': Band 1 = shuffled(easy + medium), Band 2 = shuffled(hard)
 * - 'Familiar': Band 1 = shuffled(medium + half of easy + half of hard), Band 2 = remainder
 * - 'Proficient' / 'Mastered': Band 1 = shuffled(hard + medium), Band 2 = shuffled(easy)
 */
export function calibrateByMasteryDifficulty(
  questions: Question[],
  masteryTier?: MasteryTier
): Question[] {
  if (!masteryTier || questions.length <= 1) {
    return questions;
  }

  const easy: Question[] = [];
  const medium: Question[] = [];
  const hard: Question[] = [];

  for (const q of questions) {
    const diff = (q.difficulty || 'medium').toLowerCase();
    if (diff === 'easy') {
      easy.push(q);
    } else if (diff === 'hard') {
      hard.push(q);
    } else {
      medium.push(q);
    }
  }

  // If all questions belong to a single difficulty tier, keep the shuffled order as-is
  const nonEmptyBands = [easy.length > 0, medium.length > 0, hard.length > 0].filter(Boolean).length;
  if (nonEmptyBands <= 1) {
    return questions;
  }

  if (masteryTier === 'Not started' || masteryTier === 'Attempted') {
    const primaryBand = shuffleArray([...easy, ...medium]);
    const secondaryBand = shuffleArray(hard);
    return [...primaryBand, ...secondaryBand];
  }

  if (masteryTier === 'Familiar') {
    const shuffledEasy = shuffleArray(easy);
    const shuffledMedium = shuffleArray(medium);
    const shuffledHard = shuffleArray(hard);
    const easyMid = Math.ceil(shuffledEasy.length / 2);
    const hardMid = Math.ceil(shuffledHard.length / 2);

    const primaryBand = shuffleArray([
      ...shuffledMedium,
      ...shuffledEasy.slice(0, easyMid),
      ...shuffledHard.slice(0, hardMid),
    ]);
    const secondaryBand = shuffleArray([
      ...shuffledEasy.slice(easyMid),
      ...shuffledHard.slice(hardMid),
    ]);
    return [...primaryBand, ...secondaryBand];
  }

  // 'Proficient' | 'Mastered'
  const primaryBand = shuffleArray([...hard, ...medium]);
  const secondaryBand = shuffleArray(easy);
  return [...primaryBand, ...secondaryBand];
}

/**
 * Prepares a practice session from a list of questions:
 * 1. Filters to target competency (string) or allowed competencies (string[]) if provided.
 * 2. Shuffles question order and applies ZPD difficulty calibration when masteryTier is provided.
 * 3. Normalizes option IDs, correctness indicators, solution fallbacks, and answer keys.
 * 4. Shuffles options for all multiple-choice and multiple-select items.
 */
export function prepareSessionQuestions(
  questions: Question[],
  shuffleQuestions: boolean = false,
  expectedCompetencyId?: string | string[],
  masteryTier?: MasteryTier
): Question[] {
  let validatedList = questions;

  if (typeof expectedCompetencyId === 'string' && expectedCompetencyId.trim() !== '') {
    const target = expectedCompetencyId.trim().toLowerCase();
    validatedList = questions.filter((q) => {
      const qComp = (q.competency_id || '').trim().toLowerCase();
      return qComp === target;
    });
  } else if (Array.isArray(expectedCompetencyId) && expectedCompetencyId.length > 0) {
    const allowedSet = new Set(
      expectedCompetencyId.map((id) => String(id).trim().toLowerCase()).filter(Boolean)
    );
    validatedList = questions.filter((q) => {
      const qComp = (q.competency_id || '').trim().toLowerCase();
      return allowedSet.has(qComp);
    });
  }

  let qList = shuffleQuestions ? shuffleArray(validatedList) : [...validatedList];
  if (shuffleQuestions && masteryTier) {
    qList = calibrateByMasteryDifficulty(qList, masteryTier);
  }

  return qList.map((rawQ) => {
    const q = normalizeQuestion(rawQ);
    if (q.options && q.options.length > 0) {
      return {
        ...q,
        options: shuffleArray<QuestionOption>(q.options),
      };
    }
    return q;
  });
}

/**
 * Builds a pedagogical session question set according to session type:
 * - 'practice' (4 items): Strictly isolated to `targetComp` (blocked initial acquisition),
 *   calibrated to `masteryTier`.
 * - 'quiz' (5 items): Interleaves `targetComp` (~60%, 3 items) with up to 2 preceding
 *   or prerequisite competencies (~40%, 2 items) to train discriminative retrieval.
 * - 'test' (9 items): Cumulative Unit Test interleaving `targetComp` (~55%, 5 items)
 *   with all preceding/prerequisite competencies in the course (~45%, 4 items).
 * - 'challenge' (up to 30 items): Full-course interleaved sampling across all competencies.
 */
export function buildInterleavedSessionQuestions(
  allQuestions: Question[],
  competencies: Competency[],
  sessionType: 'practice' | 'quiz' | 'test' | 'challenge',
  targetComp: Competency | null,
  masteryTier?: MasteryTier
): Question[] {
  if (sessionType === 'challenge') {
    const shuffled = prepareSessionQuestions(allQuestions, true, undefined, masteryTier);
    return shuffled.slice(0, Math.min(30, shuffled.length));
  }

  if (!targetComp) {
    return [];
  }

  const targetId = targetComp.id.trim().toLowerCase();
  const targetCode = (targetComp.code || '').trim().toLowerCase();
  const matchesComp = (q: Question, comp: Competency): boolean => {
    if (!q.competency_id) return false;
    const qComp = q.competency_id.trim().toLowerCase();
    const cId = comp.id.trim().toLowerCase();
    const cCode = (comp.code || '').trim().toLowerCase();
    return qComp === cId || (cCode !== '' && qComp === cCode);
  };

  const targetPool = allQuestions.filter((q) => matchesComp(q, targetComp));
  if (targetPool.length === 0) {
    return [];
  }

  const totalCount =
    sessionType === 'test'
      ? 9
      : sessionType === 'quiz'
      ? 5
      : 4;

  // Practice sessions remain 100% isolated to targetComp for focused skill acquisition
  if (sessionType === 'practice') {
    const preparedTarget = prepareSessionQuestions(
      targetPool,
      true,
      targetId || targetCode,
      masteryTier
    );
    return preparedTarget.slice(0, Math.min(totalCount, preparedTarget.length));
  }

  // Determine preceding and prerequisite competencies for interleaved Quiz / Unit Test
  const unitIdx = competencies.findIndex(
    (c) => c.id.trim().toLowerCase() === targetId
  );
  const prereqSet = new Set(
    (targetComp.prerequisites || []).map((p) => p.trim().toLowerCase()).filter(Boolean)
  );

  let priorComps: Competency[] = [];
  if (sessionType === 'quiz') {
    // Up to 2 immediately preceding competencies + any explicit prerequisites
    const precedingSlice =
      unitIdx > 0 ? competencies.slice(Math.max(0, unitIdx - 2), unitIdx) : [];
    const explicitPrereqs = competencies.filter(
      (c) =>
        c.id.trim().toLowerCase() !== targetId &&
        (prereqSet.has(c.id.trim().toLowerCase()) ||
          (c.code && prereqSet.has(c.code.trim().toLowerCase())))
    );
    const mergedMap = new Map<string, Competency>();
    for (const c of [...explicitPrereqs, ...precedingSlice]) {
      mergedMap.set(c.id.trim().toLowerCase(), c);
    }
    priorComps = Array.from(mergedMap.values()).slice(-2);
  } else if (sessionType === 'test') {
    // All preceding competencies up to unitIdx + any explicit prerequisites
    const precedingAll = unitIdx > 0 ? competencies.slice(0, unitIdx) : [];
    const explicitPrereqs = competencies.filter(
      (c) =>
        c.id.trim().toLowerCase() !== targetId &&
        (prereqSet.has(c.id.trim().toLowerCase()) ||
          (c.code && prereqSet.has(c.code.trim().toLowerCase())))
    );
    const mergedMap = new Map<string, Competency>();
    for (const c of [...precedingAll, ...explicitPrereqs]) {
      mergedMap.set(c.id.trim().toLowerCase(), c);
    }
    priorComps = Array.from(mergedMap.values());
  }

  const priorPool =
    priorComps.length > 0
      ? allQuestions.filter((q) => priorComps.some((c) => matchesComp(q, c)))
      : [];

  // If no prior competencies exist (e.g., Unit 1), gracefully draw all items from targetPool
  if (priorPool.length === 0) {
    const preparedTarget = prepareSessionQuestions(
      targetPool,
      true,
      targetId || targetCode,
      masteryTier
    );
    return preparedTarget.slice(0, Math.min(totalCount, preparedTarget.length));
  }

  const allowedPriorIds = Array.from(
    new Set(
      priorComps.flatMap((c) => [c.id, c.code || '']).filter(Boolean)
    )
  );

  const preparedTarget = prepareSessionQuestions(
    targetPool,
    true,
    targetId || targetCode,
    masteryTier
  );
  const preparedPrior = prepareSessionQuestions(
    priorPool,
    true,
    allowedPriorIds,
    masteryTier
  );

  // Target split: Quiz = 3 target + 2 prior (60/40); Unit Test = 5 target + 4 prior (55/45)
  const desiredTargetCount = sessionType === 'quiz' ? 3 : 5;
  const desiredPriorCount = totalCount - desiredTargetCount;

  const chosenTarget = preparedTarget.slice(0, desiredTargetCount);
  const chosenPrior = preparedPrior.slice(0, desiredPriorCount);

  let combined = [...chosenTarget, ...chosenPrior];

  // Top up from remaining target or prior questions if either pool had fewer items than desired
  if (combined.length < totalCount) {
    const usedIds = new Set(combined.map((q) => q.id));
    const remainingTarget = preparedTarget.filter((q) => !usedIds.has(q.id));
    const remainingPrior = preparedPrior.filter((q) => !usedIds.has(q.id));
    for (const extra of [...remainingTarget, ...remainingPrior]) {
      if (combined.length >= totalCount) break;
      combined.push(extra);
    }
  }

  // Shuffle the combined interleaved session so the learner must discriminate which concept applies
  return shuffleArray(combined);
}
