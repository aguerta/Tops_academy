import { Course, CourseManifest, CourseSummary } from '../types';

/**
 * In-memory cache for fast course access (< 16 ms / 1 frame render).
 */
interface MemoryRecord {
  course: Course;
  etag?: string;
}

const memoryCache = new Map<string, MemoryRecord>();
const inFlightRequests = new Map<string, Promise<Course>>();
const summaryMap = new Map<string, CourseSummary>();
let cachedManifest: CourseManifest | null = null;

// IndexedDB configuration
const DB_NAME = 'tops_academy_cache';
const DB_VERSION = 1;
const STORE_NAME = 'courses';

interface CachedCourseRecord {
  id: string;
  course: Course;
  etag?: string;
  saved_at: number;
}

/**
 * Open IndexedDB database with graceful fallback if unavailable.
 */
function openDatabase(): Promise<IDBDatabase | null> {
  if (typeof window === 'undefined' || !window.indexedDB) {
    return Promise.resolve(null);
  }

  return new Promise((resolve) => {
    try {
      const request = window.indexedDB.open(DB_NAME, DB_VERSION);

      request.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result;
        if (!db.objectStoreNames.contains(STORE_NAME)) {
          db.createObjectStore(STORE_NAME, { keyPath: 'id' });
        }
      };

      request.onsuccess = () => resolve(request.result);

      request.onerror = () => {
        console.warn('[courseLoader] Failed to open IndexedDB:', request.error);
        resolve(null);
      };
    } catch (err) {
      console.warn('[courseLoader] IndexedDB open error:', err);
      resolve(null);
    }
  });
}

/**
 * Retrieve cached course record from IndexedDB.
 */
async function getFromIndexedDB(id: string): Promise<CachedCourseRecord | null> {
  const db = await openDatabase();
  if (!db) return null;

  return new Promise((resolve) => {
    try {
      const tx = db.transaction(STORE_NAME, 'readonly');
      const store = tx.objectStore(STORE_NAME);
      const req = store.get(id);

      req.onsuccess = () => resolve(req.result || null);
      req.onerror = () => resolve(null);
    } catch {
      resolve(null);
    }
  });
}

/**
 * Persist course record into IndexedDB.
 */
async function saveToIndexedDB(id: string, course: Course, etag?: string): Promise<void> {
  const db = await openDatabase();
  if (!db) return;

  return new Promise((resolve) => {
    try {
      const tx = db.transaction(STORE_NAME, 'readwrite');
      const store = tx.objectStore(STORE_NAME);
      const record: CachedCourseRecord = {
        id,
        course,
        etag,
        saved_at: Date.now(),
      };
      store.put(record);

      tx.oncomplete = () => resolve();
      tx.onerror = () => resolve();
    } catch {
      resolve();
    }
  });
}

/**
 * Register summaries in internal map for fast lookup during prefetching.
 */
function updateSummaryMap(summaries: CourseSummary[]) {
  for (const s of summaries) {
    summaryMap.set(s.id, s);
    if (s.filename) {
      summaryMap.set(s.filename.replace(/\.json$/, ''), s);
    }
  }
}

/**
 * 1. loadManifest():
 * - First looks for <script id="course-manifest" type="application/json"> in DOM (0 ms network, 1st frame).
 * - If absent, fetches /api/courses.json (or candidate URLs).
 */
export async function loadManifest(): Promise<CourseManifest> {
  if (cachedManifest) {
    return cachedManifest;
  }

  // 1. Check DOM inline script
  if (typeof document !== 'undefined') {
    const inlineScript = document.getElementById('course-manifest');
    if (inlineScript && inlineScript.textContent) {
      try {
        const raw = inlineScript.textContent.trim();
        const parsed = JSON.parse(raw);
        if (parsed && Array.isArray(parsed.courses)) {
          const manifest: CourseManifest = {
            generated_at: parsed.generated_at || new Date().toISOString(),
            courses: parsed.courses,
          };
          cachedManifest = manifest;
          updateSummaryMap(manifest.courses);
          return manifest;
        }
      } catch (e) {
        console.warn('[courseLoader] Failed to parse inline course-manifest script:', e);
      }
    }
  }

  // 2. Fetch candidates from server
  const rawBase =
    (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.BASE_URL) || './';
  const base = rawBase.endsWith('/') ? rawBase.slice(0, -1) : rawBase;

  const candidates = [
    `${base}/api/courses.json`,
    `${base}/api/courses`,
    '/api/courses.json',
    '/api/courses',
  ];

  for (const url of candidates) {
    try {
      const res = await fetch(url);
      if (res.ok) {
        const data = await res.json();
        let courses: CourseSummary[] = [];
        let generated_at = new Date().toISOString();

        if (data && Array.isArray(data.courses)) {
          courses = data.courses;
          if (data.generated_at) generated_at = data.generated_at;
        } else if (Array.isArray(data)) {
          courses = data;
        }

        const manifest: CourseManifest = {
          generated_at,
          courses,
        };
        cachedManifest = manifest;
        updateSummaryMap(courses);
        return manifest;
      }
    } catch {
      // Try next candidate
    }
  }

  const fallbackManifest: CourseManifest = {
    generated_at: new Date().toISOString(),
    courses: [],
  };
  cachedManifest = fallbackManifest;
  return fallbackManifest;
}

/**
 * 2. loadCourse(summary, onProgress):
 * 1. If in memory, return immediately.
 * 2. If in IndexedDB and etag matches (or is fresh), return immediately.
 * 3. Fetch from /api/courses/${encodeURIComponent(summary.id)}.json.
 * 4. Save to memory and IndexedDB.
 * 5. Return full course.
 */
export async function loadCourse(
  summary: CourseSummary,
  onProgress?: (percent: number) => void
): Promise<Course> {
  // If request is already in-flight for this course ID, return shared promise
  if (inFlightRequests.has(summary.id)) {
    return inFlightRequests.get(summary.id)!;
  }

  // Register summary in map
  summaryMap.set(summary.id, summary);

  // 1. Check memory cache
  const mem = memoryCache.get(summary.id);
  if (mem) {
    if (!summary.etag || !mem.etag || mem.etag === summary.etag) {
      onProgress?.(100);
      return mem.course;
    }
  }

  // If summary already embedded complete data and etag matches
  if (summary.data && (!summary.etag || !mem?.etag || mem?.etag === summary.etag)) {
    memoryCache.set(summary.id, { course: summary.data, etag: summary.etag });
    saveToIndexedDB(summary.id, summary.data, summary.etag).catch(() => {});
    onProgress?.(100);
    return summary.data;
  }

  // 2. Check IndexedDB
  const idbRecord = await getFromIndexedDB(summary.id);
  if (idbRecord && idbRecord.course) {
    if (!summary.etag || !idbRecord.etag || idbRecord.etag === summary.etag) {
      memoryCache.set(summary.id, {
        course: idbRecord.course,
        etag: idbRecord.etag,
      });
      onProgress?.(100);
      return idbRecord.course;
    }
  }

  // 3. Network fetch with candidate fallbacks and optional progress reporting
  const fetchTask = (async () => {
    const rawBase =
      (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.BASE_URL) || './';
    const base = rawBase.endsWith('/') ? rawBase.slice(0, -1) : rawBase;
    const encodedId = encodeURIComponent(summary.id);
    const filenameNoExt = summary.filename
      ? encodeURIComponent(summary.filename.replace(/\.json$/, ''))
      : encodedId;

    const candidates = [
      `${base}/api/courses/${encodedId}.json`,
      `${base}/api/courses/${encodedId}`,
      `/api/courses/${encodedId}.json`,
      `/api/courses/${encodedId}`,
      `${base}/courses/${encodedId}.json`,
      `/courses/${encodedId}.json`,
    ];

    if (filenameNoExt !== encodedId) {
      candidates.push(
        `${base}/api/courses/${filenameNoExt}.json`,
        `${base}/api/courses/${filenameNoExt}`,
        `/api/courses/${filenameNoExt}.json`,
        `/api/courses/${filenameNoExt}`,
        `${base}/courses/${filenameNoExt}.json`,
        `/courses/${filenameNoExt}.json`
      );
    }

    let response: Response | null = null;
    for (const url of candidates) {
      try {
        const res = await fetch(url);
        if (res.ok) {
          response = res;
          break;
        }
      } catch {
        // Try next candidate
      }
    }

    if (!response) {
      throw new Error(`Failed to load course '${summary.id}' from any candidate URL.`);
    }

    let resolvedEtag = summary.etag;
    const headerEtag = response.headers.get('ETag');
    if (headerEtag) {
      resolvedEtag = headerEtag.replace(/^W\//, '').replace(/"/g, '');
    }

    let course: Course;
    const contentLength =
      Number(response.headers.get('content-length')) || summary.bytes || 0;

    if (
      onProgress &&
      response.body &&
      contentLength > 0 &&
      typeof ReadableStream !== 'undefined'
    ) {
      const reader = response.body.getReader();
      let receivedBytes = 0;
      const chunks: Uint8Array[] = [];

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        if (value) {
          chunks.push(value);
          receivedBytes += value.length;
          const pct = Math.min(99, Math.round((receivedBytes / contentLength) * 100));
          onProgress(pct);
        }
      }

      const totalLength = chunks.reduce((acc, chunk) => acc + chunk.length, 0);
      const combined = new Uint8Array(totalLength);
      let offset = 0;
      for (const chunk of chunks) {
        combined.set(chunk, offset);
        offset += chunk.length;
      }

      const text = new TextDecoder('utf-8').decode(combined);
      course = JSON.parse(text);
    } else {
      course = await response.json();
    }

    onProgress?.(100);

    // 4. Save to memory & IndexedDB
    memoryCache.set(summary.id, { course, etag: resolvedEtag });
    await saveToIndexedDB(summary.id, course, resolvedEtag);

    return course;
  })();

  inFlightRequests.set(summary.id, fetchTask);

  try {
    const loaded = await fetchTask;
    return loaded;
  } finally {
    inFlightRequests.delete(summary.id);
  }
}

// Prefetch queue for background loading
const prefetchQueue: CourseSummary[] = [];
let isPrefetchWorkerRunning = false;

function processNextPrefetch() {
  if (prefetchQueue.length === 0) {
    isPrefetchWorkerRunning = false;
    return;
  }

  const schedule =
    typeof window !== 'undefined' && 'requestIdleCallback' in window
      ? (cb: () => void) => (window as any).requestIdleCallback(cb, { timeout: 3000 })
      : (cb: () => void) => setTimeout(cb, 150);

  schedule(async () => {
    const nextSummary = prefetchQueue.shift();
    if (nextSummary && nextSummary.status === 'valid') {
      try {
        const mem = memoryCache.get(nextSummary.id);
        if (!mem || (nextSummary.etag && mem.etag !== nextSummary.etag)) {
          const idbRecord = await getFromIndexedDB(nextSummary.id);
          if (
            idbRecord &&
            idbRecord.course &&
            (!nextSummary.etag || idbRecord.etag === nextSummary.etag)
          ) {
            memoryCache.set(nextSummary.id, {
              course: idbRecord.course,
              etag: idbRecord.etag,
            });
          } else {
            await loadCourse(nextSummary);
          }
        }
      } catch (err) {
        console.debug(
          `[courseLoader] Background prefetch ignored/failed for ${nextSummary.id}:`,
          err
        );
      }
    }
    processNextPrefetch();
  });
}

/**
 * Background prefetch using requestIdleCallback (or setTimeout) without blocking UI.
 */
export function prefetchCourses(summaries: CourseSummary[]): void {
  if (!Array.isArray(summaries)) return;

  for (const s of summaries) {
    summaryMap.set(s.id, s);
    if (s.status === 'valid' && !memoryCache.has(s.id)) {
      if (!prefetchQueue.some((item) => item.id === s.id)) {
        prefetchQueue.push(s);
      }
    }
  }

  if (!isPrefetchWorkerRunning && prefetchQueue.length > 0) {
    isPrefetchWorkerRunning = true;
    processNextPrefetch();
  }
}

/**
 * Priority prefetch triggered by pointerEnter, focus or touchStart.
 */
export async function prefetchCourse(id: string): Promise<Course | null> {
  const mem = memoryCache.get(id);
  if (mem) {
    return mem.course;
  }

  // If in background queue, remove it from queue so priority takes over
  const qIdx = prefetchQueue.findIndex((item) => item.id === id);
  if (qIdx !== -1) {
    prefetchQueue.splice(qIdx, 1);
  }

  let summary = summaryMap.get(id);
  if (!summary) {
    summary = {
      id,
      filename: `${id}.json`,
      title: id,
      description: '',
      status: 'valid',
    };
  }

  try {
    return await loadCourse(summary);
  } catch (err) {
    console.debug(`[courseLoader] Priority prefetch failed for ${id}:`, err);
    return null;
  }
}

/**
 * Check if a course is already available synchronously in memory cache (< 16 ms).
 */
export function isCourseCached(id: string): boolean {
  return memoryCache.has(id);
}

/**
 * Get synchronously from memory cache if available.
 */
export function getCourseFromCache(id: string): Course | null {
  return memoryCache.get(id)?.course || null;
}

/**
 * Clear course caches (in memory and IndexedDB) - useful for testing and refresh.
 */
export async function clearCourseCache(): Promise<void> {
  memoryCache.clear();
  inFlightRequests.clear();
  prefetchQueue.length = 0;
  cachedManifest = null;

  const db = await openDatabase();
  if (!db) return;

  return new Promise((resolve) => {
    try {
      const tx = db.transaction(STORE_NAME, 'readwrite');
      const store = tx.objectStore(STORE_NAME);
      const req = store.clear();
      req.onsuccess = () => resolve();
      req.onerror = () => resolve();
    } catch {
      resolve();
    }
  });
}
