import { M22AttemptEvent, MasteryTier } from '../types';

export const M22_TELEMETRY_STORAGE_KEY = 'tops_m22_event_log_v1';
export const M22_TELEMETRY_MAX_EVENTS = 5000;

export interface M22BucketStats {
  n: number;
  first_attempt_accuracy: number | null;
  final_accuracy: number | null;
  hint_rate: number | null;
  avg_hints: number | null;
}

export interface M22HypothesisSummary {
  total_events: number;
  h1_tier_calibration: {
    not_started: M22BucketStats;
    familiar_plus: M22BucketStats;
    accuracy_gap: number | null;
    hint_rate_gap: number | null;
  };
  h2_trap_recurrence: {
    total_4_strike_events: number;
    followed_exposures: number;
    recurrences: number;
    recurrence_rate: number | null;
  };
  h3_unlabeled_transfer: {
    labeled: M22BucketStats;
    unlabeled_probe: M22BucketStats;
    accuracy_delta: number | null;
  };
  h4_hint_dependence: {
    proficient_mastered_cold: M22BucketStats;
    proficient_mastered_hint_assisted: M22BucketStats;
    accuracy_delta: number | null;
    hint_assisted_share: number | null;
  };
}

export interface M22ExportPayload {
  schema_version: 'm22_phase0_v1';
  exported_at: string;
  course_id: string | null;
  total_events: number;
  summary: M22HypothesisSummary;
  events: M22AttemptEvent[];
}

function getSafeStorage(): Storage | null {
  try {
    if (typeof globalThis !== 'undefined' && 'localStorage' in globalThis && globalThis.localStorage) {
      return globalThis.localStorage;
    }
  } catch {
    return null;
  }
  return null;
}

function readAllRawEvents(): M22AttemptEvent[] {
  const storage = getSafeStorage();
  if (!storage) return [];
  try {
    const raw = storage.getItem(M22_TELEMETRY_STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) return [];
    return parsed.filter(
      (item): item is M22AttemptEvent =>
        Boolean(item) && typeof item === 'object' && typeof item.id === 'string' && typeof item.question_id === 'string'
    );
  } catch {
    return [];
  }
}

function writeAllRawEvents(events: M22AttemptEvent[]): void {
  const storage = getSafeStorage();
  if (!storage) return;
  try {
    const capped =
      events.length > M22_TELEMETRY_MAX_EVENTS
        ? events.slice(events.length - M22_TELEMETRY_MAX_EVENTS)
        : events;
    storage.setItem(M22_TELEMETRY_STORAGE_KEY, JSON.stringify(capped));
  } catch {
    // Ignore storage quota or security errors
  }
}

/**
 * Loads persisted M22 attempt events, optionally filtered by course_id.
 */
export function loadM22Events(courseId?: string): M22AttemptEvent[] {
  const all = readAllRawEvents();
  if (!courseId) return all;
  return all.filter((e) => e.course_id === courseId);
}

/**
 * Appends one or more M22 attempt events with FIFO capping at 5,000 events.
 */
export function appendM22Events(events: M22AttemptEvent[]): M22AttemptEvent[] {
  if (!Array.isArray(events) || events.length === 0) {
    return readAllRawEvents();
  }
  const existing = readAllRawEvents();
  const combined = [...existing, ...events];
  const capped =
    combined.length > M22_TELEMETRY_MAX_EVENTS
      ? combined.slice(combined.length - M22_TELEMETRY_MAX_EVENTS)
      : combined;
  writeAllRawEvents(capped);
  return capped;
}

/**
 * Clears persisted M22 attempt events (all courses, or only a specific courseId).
 */
export function clearM22Events(courseId?: string): void {
  const storage = getSafeStorage();
  if (!storage) return;
  if (!courseId) {
    try {
      storage.removeItem(M22_TELEMETRY_STORAGE_KEY);
    } catch {
      // Ignore storage errors
    }
    return;
  }
  const remaining = readAllRawEvents().filter((e) => e.course_id !== courseId);
  writeAllRawEvents(remaining);
}

function computeBucketStats(events: M22AttemptEvent[]): M22BucketStats {
  const n = events.length;
  if (n === 0) {
    return {
      n: 0,
      first_attempt_accuracy: null,
      final_accuracy: null,
      hint_rate: null,
      avg_hints: null,
    };
  }
  let firstCorrect = 0;
  let finalCorrect = 0;
  let withHints = 0;
  let totalHints = 0;

  for (const e of events) {
    if (e.first_attempt_correct) firstCorrect += 1;
    if (e.final_correct) finalCorrect += 1;
    if (e.hints_used > 0) withHints += 1;
    totalHints += Math.max(0, e.hints_used || 0);
  }

  return {
    n,
    first_attempt_accuracy: firstCorrect / n,
    final_accuracy: finalCorrect / n,
    hint_rate: withHints / n,
    avg_hints: totalHints / n,
  };
}

const FAMILIAR_PLUS_TIERS = new Set<MasteryTier>(['Familiar', 'Proficient', 'Mastered']);
const PROFICIENT_MASTERED_TIERS = new Set<MasteryTier>(['Proficient', 'Mastered']);

/**
 * Computes N=1 diagnostic indicators for M22 Phase 0 hypotheses H1–H4.
 */
export function computeM22HypothesisSummary(events: M22AttemptEvent[]): M22HypothesisSummary {
  const list = Array.isArray(events) ? events : [];

  // H1: Not started vs Familiar+ first-attempt accuracy & hint rate
  const notStarted = list.filter((e) => e.mastery_tier_before === 'Not started');
  const familiarPlus = list.filter((e) => FAMILIAR_PLUS_TIERS.has(e.mastery_tier_before));
  const h1NotStarted = computeBucketStats(notStarted);
  const h1FamiliarPlus = computeBucketStats(familiarPlus);

  const h1AccuracyGap =
    h1FamiliarPlus.first_attempt_accuracy !== null && h1NotStarted.first_attempt_accuracy !== null
      ? h1FamiliarPlus.first_attempt_accuracy - h1NotStarted.first_attempt_accuracy
      : null;
  const h1HintRateGap =
    h1NotStarted.hint_rate !== null && h1FamiliarPlus.hint_rate !== null
      ? h1NotStarted.hint_rate - h1FamiliarPlus.hint_rate
      : null;

  // H2: Exact D-XX-YY trap recurrence on the next encounter after exhausted_4_strikes
  const chronological = [...list].sort((a, b) =>
    String(a.timestamp || '').localeCompare(String(b.timestamp || ''))
  );
  const eventsByComp = new Map<string, M22AttemptEvent[]>();
  for (const ev of chronological) {
    const compKey = `${ev.course_id}::${ev.competency_id}`;
    const bucket = eventsByComp.get(compKey) || [];
    bucket.push(ev);
    eventsByComp.set(compKey, bucket);
  }

  let total4StrikeEvents = 0;
  let followedExposures = 0;
  let recurrences = 0;

  for (const compEvents of eventsByComp.values()) {
    for (let i = 0; i < compEvents.length; i++) {
      const ev = compEvents[i];
      if (!ev.exhausted_4_strikes) continue;
      total4StrikeEvents += 1;

      const trapIds = Array.from(
        new Set((ev.triggered_distractor_ids || []).map((id) => id.trim()).filter(Boolean))
      );
      if (trapIds.length === 0) continue;

      const nextEncounter = compEvents[i + 1];
      if (!nextEncounter) continue;

      followedExposures += 1;
      const nextTrapSet = new Set(
        (nextEncounter.triggered_distractor_ids || []).map((id) => id.trim()).filter(Boolean)
      );
      if (trapIds.some((id) => nextTrapSet.has(id))) {
        recurrences += 1;
      }
    }
  }

  // H3: Labeled practice vs unlabeled cold transfer probe accuracy delta
  const labeled = list.filter((e) => !e.is_unlabeled_probe);
  const unlabeled = list.filter((e) => e.is_unlabeled_probe);
  const h3Labeled = computeBucketStats(labeled);
  const h3Unlabeled = computeBucketStats(unlabeled);
  const h3AccuracyDelta =
    h3Labeled.first_attempt_accuracy !== null && h3Unlabeled.first_attempt_accuracy !== null
      ? h3Labeled.first_attempt_accuracy - h3Unlabeled.first_attempt_accuracy
      : null;

  // H4: Proficient/Mastered hint-assisted vs cold performance
  const profMastered = list.filter((e) => PROFICIENT_MASTERED_TIERS.has(e.mastery_tier_before));
  const profCold = profMastered.filter((e) => (e.hints_used || 0) === 0);
  const profHinted = profMastered.filter((e) => (e.hints_used || 0) > 0);
  const h4Cold = computeBucketStats(profCold);
  const h4Hinted = computeBucketStats(profHinted);
  const h4AccuracyDelta =
    h4Hinted.first_attempt_accuracy !== null && h4Cold.first_attempt_accuracy !== null
      ? h4Hinted.first_attempt_accuracy - h4Cold.first_attempt_accuracy
      : null;
  const h4HintAssistedShare =
    profMastered.length > 0 ? profHinted.length / profMastered.length : null;

  return {
    total_events: list.length,
    h1_tier_calibration: {
      not_started: h1NotStarted,
      familiar_plus: h1FamiliarPlus,
      accuracy_gap: h1AccuracyGap,
      hint_rate_gap: h1HintRateGap,
    },
    h2_trap_recurrence: {
      total_4_strike_events: total4StrikeEvents,
      followed_exposures: followedExposures,
      recurrences,
      recurrence_rate: followedExposures > 0 ? recurrences / followedExposures : null,
    },
    h3_unlabeled_transfer: {
      labeled: h3Labeled,
      unlabeled_probe: h3Unlabeled,
      accuracy_delta: h3AccuracyDelta,
    },
    h4_hint_dependence: {
      proficient_mastered_cold: h4Cold,
      proficient_mastered_hint_assisted: h4Hinted,
      accuracy_delta: h4AccuracyDelta,
      hint_assisted_share: h4HintAssistedShare,
    },
  };
}

/**
 * Exports persisted M22 events (optionally scoped to a courseId) and H1–H4 summary as JSON.
 */
export function exportM22EventsAsJson(courseId?: string): string {
  const events = loadM22Events(courseId);
  const payload: M22ExportPayload = {
    schema_version: 'm22_phase0_v1',
    exported_at: new Date().toISOString(),
    course_id: courseId || null,
    total_events: events.length,
    summary: computeM22HypothesisSummary(events),
    events,
  };
  return JSON.stringify(payload, null, 2);
}
