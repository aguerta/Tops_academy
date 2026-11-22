import { Question, QuestionTelemetry, SessionType, StructuredUserAnswer } from '../types';

export const ACTIVE_SESSION_STORAGE_KEY = 'tops_active_session_v1';

export interface PersistedQuestionResult {
  questionId: string;
  isCorrect: boolean;
  skipped: boolean;
}

export interface ActiveSessionSnapshot {
  version: 1;
  courseId: string;
  sessionType: SessionType;
  competencyId: string | null;
  unitIndex: number | null;
  sessionTitle: string;
  questions: Question[];
  currentIndex: number;
  selectedOption: string | null;
  selectedMultiOptions: string[];
  fillBlankValue: string;
  structuredAnswer?: StructuredUserAnswer | null;
  matchedDiagnosticRationale?: string | null;
  stage0Phase?: 1 | 2 | 3;
  hintsRevealed: number;
  wrongAttemptsCount: number;
  isExhausted: boolean;
  isChecked: boolean;
  isCorrect: boolean | null;
  isCurtainLifted: boolean;
  canvasInteracted?: boolean;
  ironExamState?: Record<string, unknown>;
  results: PersistedQuestionResult[];
  telemetry: QuestionTelemetry[];
  elapsedSeconds: number;
  savedAt: number;
}

/**
 * Safely saves the active practice/test/challenge session snapshot to sessionStorage.
 */
export function saveActiveSession(snapshot: ActiveSessionSnapshot): boolean {
  if (typeof window === 'undefined' || !window.sessionStorage) {
    return false;
  }
  try {
    const serialized = JSON.stringify(snapshot);
    window.sessionStorage.setItem(ACTIVE_SESSION_STORAGE_KEY, serialized);
    return true;
  } catch (err) {
    console.warn('[sessionStore] Failed to save active session snapshot to sessionStorage:', err);
    return false;
  }
}

/**
 * Safely loads the active session snapshot from sessionStorage.
 * Validates version and integrity, and optionally filters by courseId.
 */
export function loadActiveSession(courseId?: string): ActiveSessionSnapshot | null {
  if (typeof window === 'undefined' || !window.sessionStorage) {
    return null;
  }
  try {
    const raw = window.sessionStorage.getItem(ACTIVE_SESSION_STORAGE_KEY);
    if (!raw) return null;

    const parsed = JSON.parse(raw);
    if (!parsed || typeof parsed !== 'object' || parsed.version !== 1) {
      return null;
    }

    if (
      !parsed.courseId ||
      !Array.isArray(parsed.questions) ||
      parsed.questions.length === 0 ||
      typeof parsed.currentIndex !== 'number'
    ) {
      return null;
    }

    if (courseId && parsed.courseId !== courseId) {
      return null;
    }

    return parsed as ActiveSessionSnapshot;
  } catch (err) {
    console.warn('[sessionStore] Failed to read active session snapshot from sessionStorage:', err);
    return null;
  }
}

/**
 * Clears the active session snapshot from sessionStorage.
 */
export function clearActiveSession(): void {
  if (typeof window === 'undefined' || !window.sessionStorage) {
    return;
  }
  try {
    window.sessionStorage.removeItem(ACTIVE_SESSION_STORAGE_KEY);
  } catch (err) {
    console.warn('[sessionStore] Failed to clear active session snapshot from sessionStorage:', err);
  }
}
