import {
  CompetencyMastery,
  CourseMasteryRecord,
  FsrsCardState,
  MisconceptionEntry,
  QuestionType,
  SrsReviewTelemetry,
  TimingStats,
  UnitTestRecord,
} from '../types';
import { MAX_MODALITY_LATENCY_WINDOW, MAX_SRS_TELEMETRY_ENTRIES } from './fsrsEngine';

const PROGRESS_STORAGE_KEY = 'tops_academic_progress_v1';
const SYNC_CONFIG_KEY = 'tops_gist_sync_v1';
const GIST_FILENAME = 'tops_progress.json';

export const PROGRESS_SYNCED_EVENT = 'tops-progress-synced';

export interface GistSyncConfig {
  token: string;
  gistId: string;
  lastSyncedAt?: string;
}

export type SyncResult =
  | { status: 'unconfigured' }
  | { status: 'created'; gistId: string; lastSyncedAt: string }
  | { status: 'synced'; gistId: string; lastSyncedAt: string }
  | { status: 'error'; message: string };

export function getSyncConfig(): GistSyncConfig | null {
  if (typeof window === 'undefined' || !window.localStorage) return null;
  try {
    const raw = window.localStorage.getItem(SYNC_CONFIG_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    if (!parsed || typeof parsed.token !== 'string' || !parsed.token.trim()) return null;
    return {
      token: parsed.token.trim(),
      gistId: typeof parsed.gistId === 'string' ? parsed.gistId.trim() : '',
      lastSyncedAt: typeof parsed.lastSyncedAt === 'string' ? parsed.lastSyncedAt : undefined,
    };
  } catch {
    return null;
  }
}

export function saveSyncConfig(config: GistSyncConfig): void {
  if (typeof window === 'undefined' || !window.localStorage) return;
  window.localStorage.setItem(
    SYNC_CONFIG_KEY,
    JSON.stringify({
      token: config.token.trim(),
      gistId: config.gistId.trim(),
      lastSyncedAt: config.lastSyncedAt,
    })
  );
}

let syncEpoch = 0;
let activeSyncPromise: Promise<SyncResult> | null = null;
let pendingResync = false;
let debounceTimer: ReturnType<typeof setTimeout> | null = null;

export function clearSyncConfig(): void {
  syncEpoch += 1;
  pendingResync = false;
  if (debounceTimer) {
    clearTimeout(debounceTimer);
    debounceTimer = null;
  }
  if (typeof window === 'undefined' || !window.localStorage) return;
  window.localStorage.removeItem(SYNC_CONFIG_KEY);
}

function parseTimestamp(iso?: string): number {
  if (!iso) return 0;
  const ms = Date.parse(iso);
  return Number.isFinite(ms) ? ms : 0;
}

function mergeTimingStats(
  a?: TimingStats,
  b?: TimingStats,
  aIsNewer?: boolean
): TimingStats | undefined {
  if (!a && !b) return undefined;
  if (!a) return b;
  if (!b) return a;

  const minDefined = (x?: number, y?: number): number | undefined => {
    if (x === undefined) return y;
    if (y === undefined) return x;
    return Math.min(x, y);
  };

  const newer = aIsNewer ? a : b;
  const older = aIsNewer ? b : a;

  return {
    best_avg_seconds_per_question: minDefined(
      a.best_avg_seconds_per_question,
      b.best_avg_seconds_per_question
    ),
    best_total_seconds: minDefined(a.best_total_seconds, b.best_total_seconds),
    last_avg_seconds_per_question:
      newer.last_avg_seconds_per_question ?? older.last_avg_seconds_per_question,
    last_total_seconds: newer.last_total_seconds ?? older.last_total_seconds,
  };
}

function mergeCompetencyTiming(
  a?: CompetencyMastery['timing'],
  b?: CompetencyMastery['timing'],
  aIsNewer?: boolean
): CompetencyMastery['timing'] {
  if (!a && !b) return undefined;
  if (!a) return b;
  if (!b) return a;
  return {
    practice: mergeTimingStats(a.practice, b.practice, aIsNewer),
    quiz: mergeTimingStats(a.quiz, b.quiz, aIsNewer),
    test: mergeTimingStats(a.test, b.test, aIsNewer),
  };
}

function mergeUnitTest(a?: UnitTestRecord, b?: UnitTestRecord): UnitTestRecord | undefined {
  if (!a) return b;
  if (!b) return a;
  return parseTimestamp(a.completed_at) >= parseTimestamp(b.completed_at) ? a : b;
}

function mergeFsrsCard(
  a?: FsrsCardState,
  b?: FsrsCardState
): FsrsCardState | undefined {
  if (!a) return b;
  if (!b) return a;
  const aMs = parseTimestamp(a.last_review);
  const bMs = parseTimestamp(b.last_review);
  if (aMs !== bMs) return aMs > bMs ? a : b;
  return (a.reps ?? 0) >= (b.reps ?? 0) ? a : b;
}

function mergeModalityLatencies(
  a?: Partial<Record<QuestionType, number[]>>,
  b?: Partial<Record<QuestionType, number[]>>
): Partial<Record<QuestionType, number[]>> | undefined {
  if (!a && !b) return undefined;
  const merged: Partial<Record<QuestionType, number[]>> = {};
  const keys = new Set<QuestionType>([
    ...((Object.keys(a || {}) as QuestionType[]) || []),
    ...((Object.keys(b || {}) as QuestionType[]) || []),
  ]);
  for (const k of keys) {
    const arrA = a?.[k] || [];
    const arrB = b?.[k] || [];
    const combined = arrA.length >= arrB.length ? [...arrB, ...arrA] : [...arrA, ...arrB];
    merged[k] = combined.slice(-MAX_MODALITY_LATENCY_WINDOW);
  }
  return merged;
}

function maxTimestampIso(a?: string, b?: string): string | undefined {
  if (!a) return b;
  if (!b) return a;
  return parseTimestamp(a) >= parseTimestamp(b) ? a : b;
}

function mergeMisconceptionLedger(
  a?: Record<string, MisconceptionEntry>,
  b?: Record<string, MisconceptionEntry>
): Record<string, MisconceptionEntry> | undefined {
  if (!a && !b) return undefined;
  const merged: Record<string, MisconceptionEntry> = {};
  const allIds = new Set([...Object.keys(a || {}), ...Object.keys(b || {})]);
  for (const id of allIds) {
    const l = a?.[id];
    const r = b?.[id];
    if (!l && r) {
      merged[id] = r;
      continue;
    }
    if (l && !r) {
      merged[id] = l;
      continue;
    }
    if (!l || !r) continue;
    const lMs = parseTimestamp(l.last_seen);
    const rMs = parseTimestamp(r.last_seen);
    const newer = lMs >= rMs ? l : r;
    merged[id] = {
      ...newer,
      count: Math.max(l.count, r.count),
    };
  }
  return Object.keys(merged).length > 0 ? merged : undefined;
}

function mergeSrsTelemetry(
  a?: SrsReviewTelemetry[],
  b?: SrsReviewTelemetry[]
): SrsReviewTelemetry[] | undefined {
  if (!a && !b) return undefined;
  const combined = [...(a || []), ...(b || [])];
  if (combined.length === 0) return undefined;
  const seen = new Set<string>();
  const deduped: SrsReviewTelemetry[] = [];
  for (const ev of combined) {
    const key = `${ev.date}|${ev.competency_id}`;
    if (!seen.has(key)) {
      seen.add(key);
      deduped.push(ev);
    }
  }
  deduped.sort((x, y) => parseTimestamp(x.date) - parseTimestamp(y.date));
  return deduped.slice(-MAX_SRS_TELEMETRY_ENTRIES);
}

function mergeCompetencyMastery(
  localComp?: CompetencyMastery,
  remoteComp?: CompetencyMastery
): CompetencyMastery {
  if (!localComp) return remoteComp!;
  if (!remoteComp) return localComp;

  // Deduplicate and merge attempt histories chronologically
  const combinedHistory = [...(localComp.history || []), ...(remoteComp.history || [])];
  const seen = new Set<string>();
  const mergedHistory: CompetencyMastery['history'] = [];
  for (const item of combinedHistory) {
    const key = `${item.date}|${item.type}|${item.score}|${item.total}`;
    if (!seen.has(key)) {
      seen.add(key);
      mergedHistory.push(item);
    }
  }
  mergedHistory.sort((x, y) => parseTimestamp(x.date) - parseTimestamp(y.date));

  const localHasWork = (localComp.history?.length || 0) > 0 || localComp.status !== 'Not started';
  const remoteHasWork = (remoteComp.history?.length || 0) > 0 || remoteComp.status !== 'Not started';

  let localWins: boolean;
  if (localHasWork !== remoteHasWork) {
    localWins = localHasWork;
  } else {
    localWins = parseTimestamp(localComp.last_practiced) >= parseTimestamp(remoteComp.last_practiced);
  }

  const winner = localWins ? localComp : remoteComp;
  const mergedFsrs = mergeFsrsCard(localComp.fsrs, remoteComp.fsrs);
  const mergedPromoAt = maxTimestampIso(
    localComp.last_tier_promotion_at,
    remoteComp.last_tier_promotion_at
  );
  const mergedLatencies = mergeModalityLatencies(
    localComp.modality_latencies,
    remoteComp.modality_latencies
  );

  return {
    status: winner.status,
    points: winner.points,
    last_practiced: winner.last_practiced,
    unit_test: mergeUnitTest(localComp.unit_test, remoteComp.unit_test),
    history: mergedHistory,
    timing: mergeCompetencyTiming(localComp.timing, remoteComp.timing, localWins),
    ...(winner.needs_review !== undefined ? { needs_review: winner.needs_review } : {}),
    ...(winner.needs_review && winner.review_reason
      ? { review_reason: winner.review_reason }
      : {}),
    ...(mergedPromoAt ? { last_tier_promotion_at: mergedPromoAt } : {}),
    ...(mergedFsrs ? { fsrs: mergedFsrs } : {}),
    ...(mergedLatencies ? { modality_latencies: mergedLatencies } : {}),
    ...(winner.recent_misconceptions !== undefined
      ? { recent_misconceptions: winner.recent_misconceptions }
      : {}),
  };
}

function computeCourseProgressPercentage(
  competencies: Record<string, CompetencyMastery>,
  courseChallenge?: CourseMasteryRecord['course_challenge']
): number {
  const compList = Object.values(competencies || {});
  const totalUnits = compList.length;
  if (totalUnits === 0) return 0;

  let sumUnitTestPercentages = 0;
  for (const comp of compList) {
    if (comp.unit_test && comp.unit_test.total_questions > 0) {
      sumUnitTestPercentages += comp.unit_test.percentage;
    }
  }

  const avgUnitTests = sumUnitTestPercentages / totalUnits;
  const unitTestsContribution = avgUnitTests * 0.8;

  const cc = courseChallenge;
  const ccPercentage =
    cc && cc.total_questions > 0
      ? (cc.percentage ??
          (cc.completed ? 100 : Math.round((cc.last_score / cc.total_questions) * 100)))
      : 0;
  const ccContribution = (ccPercentage / 100) * 20;

  const rawPercentage = Math.round(unitTestsContribution + ccContribution);
  return Math.min(100, Math.max(0, rawPercentage));
}

/**
 * Merges two full progress maps course-by-course and competency-by-competency
 * without overwriting independent progress made on different machines.
 */
export function mergeAllMasteryData(
  local: Record<string, CourseMasteryRecord>,
  remote: Record<string, CourseMasteryRecord>
): Record<string, CourseMasteryRecord> {
  const allCourseIds = new Set([...Object.keys(local || {}), ...Object.keys(remote || {})]);
  const merged: Record<string, CourseMasteryRecord> = {};

  for (const courseId of allCourseIds) {
    const lRec = local?.[courseId];
    const rRec = remote?.[courseId];

    if (!lRec && rRec) {
      merged[courseId] = rRec;
      continue;
    }
    if (lRec && !rRec) {
      merged[courseId] = lRec;
      continue;
    }
    if (!lRec || !rRec) continue;

    const allCompIds = new Set([
      ...Object.keys(lRec.competencies || {}),
      ...Object.keys(rRec.competencies || {}),
    ]);
    const mergedCompetencies: Record<string, CompetencyMastery> = {};

    for (const compId of allCompIds) {
      const mergedComp = mergeCompetencyMastery(
        lRec.competencies?.[compId],
        rRec.competencies?.[compId]
      );
      mergedCompetencies[compId] = mergedComp;
    }

    let mergedChallenge = lRec.course_challenge || rRec.course_challenge;
    if (lRec.course_challenge && rRec.course_challenge) {
      const lChallengeNewer =
        parseTimestamp(lRec.course_challenge.completed_at) >=
        parseTimestamp(rRec.course_challenge.completed_at);
      const winnerChallenge = lChallengeNewer ? lRec.course_challenge : rRec.course_challenge;
      mergedChallenge = {
        ...winnerChallenge,
        timing: mergeTimingStats(
          lRec.course_challenge.timing,
          rRec.course_challenge.timing,
          lChallengeNewer
        ),
      };
    }

    const mergedLastMasteryAt = maxTimestampIso(
      lRec.last_mastery_challenge_at,
      rRec.last_mastery_challenge_at
    );
    const mergedLedger = mergeMisconceptionLedger(
      lRec.misconception_ledger,
      rRec.misconception_ledger
    );
    const mergedSrsTelemetry = mergeSrsTelemetry(lRec.srs_telemetry, rRec.srs_telemetry);

    merged[courseId] = {
      course_id: courseId,
      mastery_points: computeCourseProgressPercentage(mergedCompetencies, mergedChallenge),
      competencies: mergedCompetencies,
      ...(mergedLastMasteryAt ? { last_mastery_challenge_at: mergedLastMasteryAt } : {}),
      ...(mergedLedger ? { misconception_ledger: mergedLedger } : {}),
      ...(mergedSrsTelemetry ? { srs_telemetry: mergedSrsTelemetry } : {}),
      ...(mergedChallenge ? { course_challenge: mergedChallenge } : {}),
    };
  }

  return merged;
}

function readLocalProgress(): Record<string, CourseMasteryRecord> {
  if (typeof window === 'undefined' || !window.localStorage) return {};
  try {
    const raw = window.localStorage.getItem(PROGRESS_STORAGE_KEY);
    return raw ? JSON.parse(raw) : {};
  } catch {
    return {};
  }
}

function writeLocalProgress(data: Record<string, CourseMasteryRecord>): void {
  if (typeof window === 'undefined' || !window.localStorage) return;
  window.localStorage.setItem(PROGRESS_STORAGE_KEY, JSON.stringify(data));
  window.dispatchEvent(new CustomEvent(PROGRESS_SYNCED_EVENT));
}

/**
 * Synchronizes localStorage mastery progress with the configured private GitHub Gist.
 * Creates the private Gist automatically if `gistId` is empty.
 */
export async function syncWithGist(overrideConfig?: GistSyncConfig): Promise<SyncResult> {
  if (activeSyncPromise && !overrideConfig) {
    return activeSyncPromise;
  }

  const myEpoch = syncEpoch;

  while (activeSyncPromise) {
    await activeSyncPromise.catch(() => undefined);
  }

  const run = async (): Promise<SyncResult> => {
    if (myEpoch !== syncEpoch) {
      return { status: 'unconfigured' };
    }

    const cfg = overrideConfig || getSyncConfig();
    if (!cfg || !cfg.token) {
      return { status: 'unconfigured' };
    }

    const headers: Record<string, string> = {
      Authorization: `Bearer ${cfg.token}`,
      Accept: 'application/vnd.github+json',
      'Content-Type': 'application/json',
    };

    try {
      // First-time setup: create a new private (secret) Gist
      if (!cfg.gistId) {
        const localData = readLocalProgress();
        const res = await fetch('https://api.github.com/gists', {
          method: 'POST',
          headers,
          body: JSON.stringify({
            description: "Top's Academy Mastery Progress Sync",
            public: false,
            files: {
              [GIST_FILENAME]: {
                content: JSON.stringify(localData, null, 2),
              },
            },
          }),
        });

        if (!res.ok) {
          const errText = await res.text().catch(() => res.statusText);
          return { status: 'error', message: `GitHub API (${res.status}): ${errText}` };
        }

        const created = await res.json();
        if (!created || typeof created.id !== 'string' || !created.id.trim()) {
          return {
            status: 'error',
            message: 'GitHub API no devolvió un Gist ID válido al crear el respaldo.',
          };
        }
        if (myEpoch !== syncEpoch) {
          return { status: 'unconfigured' };
        }

        const now = new Date().toISOString();
        saveSyncConfig({
          token: cfg.token,
          gistId: created.id,
          lastSyncedAt: now,
        });
        if (typeof window !== 'undefined') {
          window.dispatchEvent(new CustomEvent(PROGRESS_SYNCED_EVENT));
        }
        return { status: 'created', gistId: created.id, lastSyncedAt: now };
      }

      // Existing Gist: fetch remote, merge per-competency, update local & remote if needed
      const getRes = await fetch(`https://api.github.com/gists/${encodeURIComponent(cfg.gistId)}`, {
        method: 'GET',
        headers,
        cache: 'no-store',
      });

      if (!getRes.ok) {
        const errText = await getRes.text().catch(() => getRes.statusText);
        return { status: 'error', message: `GitHub API (${getRes.status}): ${errText}` };
      }

      const gistJson = await getRes.json();
      const gistFile = gistJson?.files?.[GIST_FILENAME];
      let remoteRaw: unknown = gistFile?.content;
      if (gistFile?.truncated && typeof gistFile?.raw_url === 'string' && gistFile.raw_url) {
        const rawRes = await fetch(gistFile.raw_url, {
          method: 'GET',
          cache: 'no-store',
        });
        if (!rawRes.ok) {
          const errText = await rawRes.text().catch(() => rawRes.statusText);
          return {
            status: 'error',
            message: `GitHub Raw Gist (${rawRes.status}): ${errText}`,
          };
        }
        remoteRaw = await rawRes.text();
      }

      let remoteData: Record<string, CourseMasteryRecord> = {};
      if (typeof remoteRaw === 'string' && remoteRaw.trim()) {
        try {
          const parsed = JSON.parse(remoteRaw);
          if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) {
            return {
              status: 'error',
              message:
                'El archivo remoto del Gist no contiene un objeto JSON válido; se abortó la sincronización para proteger tus datos.',
            };
          }
          remoteData = parsed as Record<string, CourseMasteryRecord>;
        } catch {
          return {
            status: 'error',
            message:
              'El archivo remoto del Gist contiene JSON inválido; se abortó la sincronización para proteger tus datos.',
          };
        }
      }

      if (myEpoch !== syncEpoch) {
        return { status: 'unconfigured' };
      }

      // Re-read localStorage AFTER the GET round-trip so progress saved in-flight is preserved
      const latestLocalData = readLocalProgress();
      const merged = mergeAllMasteryData(latestLocalData, remoteData);
      const mergedSerialized = JSON.stringify(merged, null, 2);
      const localSerialized = JSON.stringify(latestLocalData, null, 2);
      const remoteSerialized = JSON.stringify(remoteData, null, 2);

      if (mergedSerialized !== localSerialized) {
        writeLocalProgress(merged);
      }

      if (mergedSerialized !== remoteSerialized || !gistFile) {
        const patchRes = await fetch(
          `https://api.github.com/gists/${encodeURIComponent(cfg.gistId)}`,
          {
            method: 'PATCH',
            headers,
            body: JSON.stringify({
              files: {
                [GIST_FILENAME]: {
                  content: mergedSerialized,
                },
              },
            }),
          }
        );

        if (!patchRes.ok) {
          const errText = await patchRes.text().catch(() => patchRes.statusText);
          return { status: 'error', message: `GitHub PATCH (${patchRes.status}): ${errText}` };
        }
      }

      if (myEpoch !== syncEpoch) {
        return { status: 'unconfigured' };
      }

      const now = new Date().toISOString();
      saveSyncConfig({
        token: cfg.token,
        gistId: cfg.gistId,
        lastSyncedAt: now,
      });
      return { status: 'synced', gistId: cfg.gistId, lastSyncedAt: now };
    } catch (err) {
      return {
        status: 'error',
        message: err instanceof Error ? err.message : 'Network error syncing with GitHub Gist',
      };
    }
  };

  const promise = run().finally(() => {
    if (activeSyncPromise === promise) {
      activeSyncPromise = null;
    }
    if (pendingResync && getSyncConfig()) {
      pendingResync = false;
      void syncWithGist();
    }
  });
  activeSyncPromise = promise;
  return promise;
}

/**
 * Debounced background sync triggered automatically after local mastery updates.
 */
export function scheduleBackgroundSync(): void {
  if (!getSyncConfig()) return;
  if (debounceTimer) {
    clearTimeout(debounceTimer);
  }
  debounceTimer = setTimeout(() => {
    debounceTimer = null;
    if (activeSyncPromise) {
      pendingResync = true;
      return;
    }
    void syncWithGist();
  }, 800);
}
