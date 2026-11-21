import {
  CompetencyMastery,
  CourseMasteryRecord,
  TimingStats,
  UnitTestRecord,
} from '../types';

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

export function clearSyncConfig(): void {
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

  return {
    status: winner.status,
    points: winner.points,
    last_practiced: winner.last_practiced,
    unit_test: mergeUnitTest(localComp.unit_test, remoteComp.unit_test),
    history: mergedHistory,
    timing: mergeCompetencyTiming(localComp.timing, remoteComp.timing, localWins),
  };
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
    let totalPoints = 0;

    for (const compId of allCompIds) {
      const mergedComp = mergeCompetencyMastery(
        lRec.competencies?.[compId],
        rRec.competencies?.[compId]
      );
      mergedCompetencies[compId] = mergedComp;
      totalPoints += mergedComp.points || 0;
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

    merged[courseId] = {
      course_id: courseId,
      mastery_points: totalPoints,
      competencies: mergedCompetencies,
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

let activeSyncPromise: Promise<SyncResult> | null = null;
let debounceTimer: ReturnType<typeof setTimeout> | null = null;

/**
 * Synchronizes localStorage mastery progress with the configured private GitHub Gist.
 * Creates the private Gist automatically if `gistId` is empty.
 */
export async function syncWithGist(overrideConfig?: GistSyncConfig): Promise<SyncResult> {
  if (activeSyncPromise && !overrideConfig) {
    return activeSyncPromise;
  }

  const run = async (): Promise<SyncResult> => {
    const cfg = overrideConfig || getSyncConfig();
    if (!cfg || !cfg.token) {
      return { status: 'unconfigured' };
    }

    const headers: Record<string, string> = {
      Authorization: `Bearer ${cfg.token}`,
      Accept: 'application/vnd.github+json',
      'Content-Type': 'application/json',
    };

    const localData = readLocalProgress();

    try {
      // First-time setup: create a new private (secret) Gist
      if (!cfg.gistId) {
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
        const now = new Date().toISOString();
        saveSyncConfig({
          token: cfg.token,
          gistId: created.id,
          lastSyncedAt: now,
        });
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
      const remoteRaw = gistJson?.files?.[GIST_FILENAME]?.content;
      let remoteData: Record<string, CourseMasteryRecord> = {};
      if (typeof remoteRaw === 'string' && remoteRaw.trim()) {
        try {
          remoteData = JSON.parse(remoteRaw);
        } catch {
          remoteData = {};
        }
      }

      const merged = mergeAllMasteryData(localData, remoteData);
      const mergedSerialized = JSON.stringify(merged, null, 2);
      const localSerialized = JSON.stringify(localData, null, 2);
      const remoteSerialized = JSON.stringify(remoteData, null, 2);

      if (mergedSerialized !== localSerialized) {
        writeLocalProgress(merged);
      }

      if (mergedSerialized !== remoteSerialized || !gistJson?.files?.[GIST_FILENAME]) {
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

  if (overrideConfig) {
    return run();
  }

  activeSyncPromise = run().finally(() => {
    activeSyncPromise = null;
  });
  return activeSyncPromise;
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
    void syncWithGist();
  }, 800);
}
