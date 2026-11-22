import {
  Card,
  CardInput,
  createEmptyCard,
  fsrs,
  Grade,
  Rating,
  State,
} from 'ts-fsrs';
import {
  CalibrationMetrics,
  FsrsCardState,
  FsrsRating,
  QuestionType,
  SrsReviewTelemetry,
} from '../types';

export const MASTERY_COOLDOWN_MS = 12 * 60 * 60 * 1000; // 12 hours
export const DECAY_THRESHOLD_MASTERED = 0.85;
export const DECAY_THRESHOLD_PROFICIENT = 0.70;
export const DECAY_DOWNGRADE_THRESHOLD = 0.50;
export const MAX_SRS_TELEMETRY_ENTRIES = 500;
export const MAX_MODALITY_LATENCY_WINDOW = 15;
export const DEFAULT_REQUEST_RETENTION = 0.90;

const MS_PER_DAY = 86_400_000;

export const MODALITY_NOMINAL_SECONDS: Record<QuestionType, number> = {
  multiple_choice_7_options: 45,
  concept_matching: 45,
  fill_in_the_blank: 90,
  open_symbolic: 90,
  multiple_select: 120,
  proof_dag: 120,
  adversarial_break: 120,
  unstructured_model: 120,
  invariant_canvas: 120,
};

function clamp01(value: number): number {
  if (!Number.isFinite(value)) return 1;
  return Math.max(0, Math.min(1, value));
}

function toIso(d: Date | string | undefined, fallback: Date): string {
  if (!d) return fallback.toISOString();
  const parsed = d instanceof Date ? d : new Date(d);
  return Number.isFinite(parsed.getTime()) ? parsed.toISOString() : fallback.toISOString();
}

function serializeCard(card: Card, fallbackNow: Date): FsrsCardState {
  const anyCard = card as Card & { elapsed_days?: number };
  return {
    due: toIso(card.due, fallbackNow),
    stability: Number.isFinite(card.stability) ? card.stability : 0,
    difficulty: Number.isFinite(card.difficulty) ? card.difficulty : 0,
    ...(typeof anyCard.elapsed_days === 'number' ? { elapsed_days: anyCard.elapsed_days } : {}),
    scheduled_days: Number.isFinite(card.scheduled_days) ? card.scheduled_days : 0,
    learning_steps: typeof card.learning_steps === 'number' ? card.learning_steps : 0,
    reps: Number.isFinite(card.reps) ? card.reps : 0,
    lapses: Number.isFinite(card.lapses) ? card.lapses : 0,
    state: (card.state ?? 0) as 0 | 1 | 2 | 3,
    ...(card.last_review ? { last_review: toIso(card.last_review, fallbackNow) } : {}),
  };
}

function toTsFsrsCard(state: FsrsCardState, now: Date): CardInput {
  return {
    due: new Date(state.due || now.toISOString()),
    stability: state.stability,
    difficulty: state.difficulty,
    scheduled_days: state.scheduled_days,
    reps: state.reps,
    lapses: state.lapses,
    learning_steps: state.learning_steps ?? 0,
    state: state.state as State,
    ...(state.last_review ? { last_review: new Date(state.last_review) } : {}),
  };
}

/**
 * Creates a fresh serialized FSRS card state for an unpracticed competency.
 */
export function createInitialFsrsCard(now: Date = new Date()): FsrsCardState {
  return serializeCard(createEmptyCard(now), now);
}

/**
 * Computes current Retrievability R(t) in [0, 1] for an FSRS card at `now`.
 * Cards without a prior review return 1 (no forgetting yet).
 */
export function computeRetrievability(
  card: FsrsCardState | undefined,
  now: Date = new Date()
): number {
  if (!card || card.state === 0 || !card.last_review || card.stability <= 0) {
    return 1;
  }
  const lastReviewMs = Date.parse(card.last_review);
  if (Number.isFinite(lastReviewMs) && now.getTime() <= lastReviewMs) {
    return 1;
  }
  const scheduler = fsrs({ request_retention: DEFAULT_REQUEST_RETENTION });
  const r = scheduler.retrievability(toTsFsrsCard(card, now), now);
  return clamp01(typeof r === 'number' ? r : Number(r));
}

/**
 * Returns the learner's personal median latency (in seconds) for a modality
 * ONLY when >= 3 historical observations exist; otherwise returns null.
 */
export function getPersonalMedianLatency(
  modalityLatencies: Partial<Record<QuestionType, number[]>> | undefined,
  questionType: QuestionType | undefined
): number | null {
  if (!modalityLatencies || !questionType) return null;
  const raw = modalityLatencies[questionType];
  if (!Array.isArray(raw) || raw.length < 3) return null;
  const sorted = raw
    .filter((v) => typeof v === 'number' && Number.isFinite(v) && v > 0)
    .sort((a, b) => a - b);
  if (sorted.length < 3) return null;
  const mid = Math.floor(sorted.length / 2);
  return sorted.length % 2 === 1
    ? sorted[mid]
    : (sorted[mid - 1] + sorted[mid]) / 2;
}

export interface AutomaticRatingInput {
  ratio: number;
  hintsUsed: number;
  totalWrongAttempts: number;
  hasLuckyGuess?: boolean;
  hasLowConfidence?: boolean;
  priorReviews: number;
  speedRatio: number | null;
  hasPersonalBaseline: boolean;
}

/**
 * Maps objective telemetry to FSRS Rating (1..4) without student self-grading.
 * Latency NEVER penalizes to Hard (2): only partial correctness, >=2 hints,
 * >=1 wrong attempt before succeeding, or Iron Exam lucky_guess trigger Hard.
 */
export function computeAutomaticFsrsRating(input: AutomaticRatingInput): {
  rating: FsrsRating;
  speedRatio: number | null;
} {
  const {
    ratio,
    hintsUsed,
    totalWrongAttempts,
    hasLuckyGuess = false,
    hasLowConfidence = false,
    priorReviews,
    speedRatio,
    hasPersonalBaseline,
  } = input;

  if (ratio < 0.75) {
    return { rating: 1, speedRatio };
  }

  if (
    ratio < 1.0 ||
    hintsUsed >= 2 ||
    totalWrongAttempts >= 1 ||
    hasLuckyGuess
  ) {
    return { rating: 2, speedRatio };
  }

  if (
    ratio === 1.0 &&
    hintsUsed === 0 &&
    totalWrongAttempts === 0 &&
    hasPersonalBaseline &&
    speedRatio !== null &&
    speedRatio < 0.7 &&
    priorReviews >= 3 &&
    !hasLowConfidence
  ) {
    return { rating: 4, speedRatio };
  }

  return { rating: 3, speedRatio };
}

/**
 * Runs one FSRS-5/6 review step at `now` and returns the updated serialized card
 * along with the pre-review predicted retrievability and elapsed delta_t_days.
 */
export function scheduleFsrsReview(
  prevCard: FsrsCardState | undefined,
  rating: FsrsRating,
  now: Date = new Date(),
  requestRetention: number = DEFAULT_REQUEST_RETENTION
): {
  nextCard: FsrsCardState;
  predictedR: number;
  deltaTDays: number;
} {
  const baseCard = prevCard ?? createInitialFsrsCard(now);
  const predictedR = computeRetrievability(baseCard, now);

  let deltaTDays = 0;
  if (baseCard.last_review) {
    const prevMs = Date.parse(baseCard.last_review);
    if (Number.isFinite(prevMs) && now.getTime() > prevMs) {
      deltaTDays = (now.getTime() - prevMs) / MS_PER_DAY;
    }
  }

  const scheduler = fsrs({ request_retention: requestRetention });
  const gradeMap: Record<FsrsRating, Grade> = {
    1: Rating.Again,
    2: Rating.Hard,
    3: Rating.Good,
    4: Rating.Easy,
  };

  const tsInput = toTsFsrsCard(baseCard, now);
  const result = scheduler.next(tsInput, now, gradeMap[rating]);
  const nextCard = serializeCard(result.card, now);

  return {
    nextCard,
    predictedR,
    deltaTDays,
  };
}

/**
 * Returns remaining milliseconds in the 12-hour per-competency cooldown window
 * for promoting Proficient -> Mastered (0 when eligible).
 */
export function getCooldownRemainingMs(
  lastPromotionAt: string | undefined,
  now: Date = new Date()
): number {
  if (!lastPromotionAt) return 0;
  const promotedMs = Date.parse(lastPromotionAt);
  if (!Number.isFinite(promotedMs)) return 0;
  const elapsed = now.getTime() - promotedMs;
  if (elapsed >= MASTERY_COOLDOWN_MS) return 0;
  return Math.max(0, MASTERY_COOLDOWN_MS - elapsed);
}

/**
 * Formats cooldown milliseconds into a concise human-readable duration (e.g. "6h 20m").
 */
export function formatCooldownRemaining(ms: number): string {
  if (ms <= 0) return '0m';
  const totalMinutes = Math.ceil(ms / 60_000);
  const hours = Math.floor(totalMinutes / 60);
  const minutes = totalMinutes % 60;
  if (hours <= 0) return `${minutes}m`;
  if (minutes === 0) return `${hours}h`;
  return `${hours}h ${minutes}m`;
}

/**
 * Computes longitudinal empirical calibration metrics (Brier Score & Log-Loss)
 * over spaced reviews (delta_t_days > 0).
 */
export function computeCalibrationMetrics(
  telemetry: SrsReviewTelemetry[] | undefined
): CalibrationMetrics {
  const spaced = (telemetry || []).filter(
    (e) =>
      Number.isFinite(e.delta_t_days) &&
      e.delta_t_days > 0 &&
      Number.isFinite(e.predicted_r)
  );
  const n = spaced.length;
  if (n === 0) {
    return {
      n: 0,
      brierScore: null,
      logLoss: null,
      meanPredictedR: null,
      meanActual: null,
      bias: null,
      isReliable: false,
    };
  }

  let sumBrier = 0;
  let sumLogLoss = 0;
  let sumR = 0;
  let sumY = 0;

  for (const ev of spaced) {
    const r = clamp01(ev.predicted_r);
    const y = ev.actual_correct ? 1 : 0;
    const clippedR = Math.max(1e-6, Math.min(1 - 1e-6, r));

    sumBrier += (r - y) * (r - y);
    sumLogLoss += -(y * Math.log(clippedR) + (1 - y) * Math.log(1 - clippedR));
    sumR += r;
    sumY += y;
  }

  const meanPredictedR = sumR / n;
  const meanActual = sumY / n;

  return {
    n,
    brierScore: sumBrier / n,
    logLoss: sumLogLoss / n,
    meanPredictedR,
    meanActual,
    bias: meanPredictedR - meanActual,
    isReliable: n >= 20,
  };
}
